from collections import deque


def bread_first_search(graph, start_vertex):
    closure_dist = {start_vertex: 0}  # closure keep track of shortest path distance (layer)
    # work_list = [start_vertex]  # queue used to process vertices (enqueue = append(x), dequeue = pop(0))
    work_queue = deque([start_vertex])  # enqueue=append(x), dequeue=popleft()
    while len(work_queue) > 0:
        v = work_queue.popleft()
        for w in graph[v]:
            if w not in closure_dist:
                closure_dist[w] = closure_dist[v] + 1  # mark w explored
                work_queue.append(w)
    return closure_dist


# stack-based impl of DFS
def depth_first_search(graph, start_vertex):
    closure_no = {start_vertex: 1}
    work_stack = [start_vertex]
    next_no = 2
    while len(work_stack) > 0:
        v = work_stack.pop()
        # NOTE: incident edges need to be reversed in order to be searched in same order as recursive DFS
        for w in reversed(graph[v]):
            if w not in closure_no:
                closure_no[w] = next_no  # mark w explored
                next_no += 1
                work_stack.append(w)
    return closure_no


def is_undirected(graph):
    """Check that graph represents a simple undirected graph."""
    for v in graph:
        # no self-loops
        if v in graph[v]:
            return False
        # all relations (edges) are symmetric
        for w in graph[v]:
            if v not in graph[w]:
                return False
    return True


# NOTE: One can compute connected components of undirected graph using BFS or DFS
#       using outer loop (and global marked/explored structure)
# compute the pieces (connected components) of an undirected graph using BFS
def scc_undirected(graph):
    assert is_undirected(graph)
    closure_group = {}  # empty dict to mark explored vertices
    group_no = 1
    # outer loop
    for v in graph:
        if v not in closure_group:
            # compute vertices findable (reachable) from v
            closure_dist = bread_first_search(graph, v)
            # add the connected components using same group no
            for x in closure_dist:
                closure_group[x] = group_no  # mark the group explored
            group_no += 1
    return closure_group


# recursive impl of DFS
def depth_first_search2(graph, start_vertex):
    closure_no = {start_vertex: 1}
    _dfs_recursive(graph, start_vertex, closure_no, 2)
    return closure_no


def _dfs_recursive(graph, vertex, closure_no, next_no):
    for w in graph[vertex]:
        if w not in closure_no:
            closure_no[w] = next_no  # mark w explored
            _dfs_recursive(graph, w, closure_no, next_no + 1)


# Compute topological ordering using DFS (of DAG = directed acyclic graph)
# NOTE: every DAG has at least one sink vertex (i.e. with out-degree zero)
# NOTE: The sink vertices are candidates for the final vertices in the topological ordering
# NOTE: We need to compute the (contracted) graph G-{v}, where v is any such sink vertex, and recurse (i.e.
#       divide and conquer)

def topological_sort(graph):
    explored = set()
    closure_order = {}  # NOTE: As of python 3.7 dict is an insertion ordered collection
    # (BTW set is not insertion order preserving)
    next_order = len(graph)  # The first 'sink' vertex get the highest order
    # outer loop
    for v in graph:
        # if v not yet explored
        if v not in explored:
            # perform DFS starting at v
            next_order = _topological_sort_dfs(graph, v, explored, closure_order, next_order)
    # You can always traverse this collection from highest order to lowest order (because dict is insertion ordered)
    # That is the reversed(closure_order) is the topological order
    return closure_order


# DFS is the inner-loop sub-routine
def _topological_sort_dfs(graph, vertex, explored, closure_order, next_order):
    explored.add(vertex)
    for v in graph[vertex]:
        # if v not yet explored
        if v not in explored:
            # perform DFS starting at v (recursively)
            next_order = _topological_sort_dfs(graph, v, explored, closure_order, next_order)
    closure_order[vertex] = next_order  # update the order
    return next_order - 1


# NOTE: strongly connected components are a subset of vertices of the (di-)graph, where
#       you can get from anywhere in the subset to everywhere in the subset.
# NOTE: 'strongly connected' and 'connected/findable/reachable' means the same thing for undirected graphs.
# Definition: The SCC's of a digraph G are the equivalence classes of the relation (the exists a
#             path from u to v and a path from v to u in G.
# NOTE: If you call DFS from the right place (a vertex of a 'sink' SCC of the digraph) it will give you the right result
# NOTE: If you call DFS from the wrong place (e.g. a vertex of another SCC from where you can reach the sink) you
#       get the wrong result (a union of some of the pieces)
# TODO: Compute strongly connected components (SCC) of directed graph (digraph) using two nested DFS sub-routine calls
# Kosaraju's Two-Pass Algorithm
# step 1: reverse all arcs to compute G-reversed
# step 2: run DFS-loop on G-reversed (this computes "magical" ordering of the vertices)
#       - Let f(v) = "finishing time" of each v (this is the assigned at the bottom
#         of the recursion before wr back-track)
# step 3: run DFS-loop on G (discovers the SCC's using the "magical" order)
#       - processing nodes in decreasing order of "finishing times"
def kosaraju_scc(graph):
    assert not is_undirected(graph)
    # step 1
    g_rev = reversed_graph(graph)

    # step 2
    # topological sort gives the reversed finishing times: n finishes first, n-1 finishes next, ...,1 finishes last
    magic_order = topological_sort(g_rev)

    # step 3: traverse the reversed magic order in the outer loop of DFS
    closure_leaders = {}
    leaders = []
    for v in reversed(magic_order):
        # if v not yet explored
        if v not in closure_leaders:
            leaders.append(v)
            # perform DFS starting at v
            _kosaraju_scc_dfs(graph, v, closure_leaders, v)

    # SCC's have same leader value...here we use dict of scc-lists
    result = {x: [] for x in leaders}
    for key, val in closure_leaders.items():
        result[val].append(key)

    return result


# DFS is the inner-loop sub-routine
def _kosaraju_scc_dfs(graph, vertex, closure_leaders, leader):
    closure_leaders[vertex] = None  # mark vertex explored
    for v in graph[vertex]:
        # if v not yet explored
        if v not in closure_leaders:
            # perform DFS starting at v (recursively)
            _kosaraju_scc_dfs(graph, v, closure_leaders, leader)
    closure_leaders[vertex] = leader  # update the order


# utility function
def reversed_graph(graph):
    rev_g = {v: [] for v in graph}
    for v in graph:
        for w in graph[v]:
            rev_g[w].append(v)
    return rev_g


# TODO: dot file printer function

def main():
    # noinspection DuplicatedCode
    g = {1: [2, 3, 4, 7],
         2: [1, 3, 4],
         3: [1, 2, 4],
         4: [1, 2, 3, 5],
         5: [4, 6, 7, 8],
         6: [5, 7, 8],
         7: [1, 5, 6, 8],
         8: [5, 6, 7]
         }
    closure_dist = bread_first_search(g, 1)
    for v in closure_dist:
        print(f'{v}, dist({v}) = {closure_dist[v]}')
    closure_no = depth_first_search(g, 1)
    for v in closure_no:
        print(f'{v}, no({v}) = {closure_no[v]}')

    # older-than relation (meeting oldest first order)
    # requirement-for
    # precedence relation (precede in order/rank, comes before, be more important, priority etc)
    plan = \
        {"Morten": ["Janne", "Caroline", "Mona"],
         "Janne": ["Caroline", "Mona"],
         "Caroline": ["Mona"],
         "Mona": []  # sink = youngest
         }
    order = topological_sort(plan)
    for v in order:
        print(f'order({v}) = {order[v]}')

    # causal order of expression tree:
    #    c = a + b
    #    f = d + e
    #    g = c + f
    causal = \
        {"a": ["c"],
         "b": ["c"],
         "c": ["g"],
         "d": ["f"],
         "e": ["f"],
         "f": ["g"],
         "g": []  # sink = result
         }
    causal_order = topological_sort(causal)
    for v in causal_order:
        print(f'causal_order({v}) = {causal_order[v]}')

    # test case SCCs = ('a-b-c', 'd', 'e-f-g', 'h-i-j-k')
    dg = \
        {"a": ["c", "d"],
         "b": ["a"],
         "c": ["b", "h", "j"],
         "d": ["e", "f"],
         "e": ["g"],
         "f": ["e"],
         "g": ["f"],
         "h": ["f", "i", "k"],
         "i": ["g", "k"],
         "j": ["h"],
         "k": ["j"]
         }
    scc = kosaraju_scc(dg)
    for v in scc:
        print(f'scc({v}) = {scc[v]}')


if __name__ == '__main__':
    main()
