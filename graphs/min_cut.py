from itertools import repeat
from re import sub
from random import randint
from copy import deepcopy

# List representation of adjacency list
#  * the vertices of a graph with n nodes will be numbered from 0 to n-1
#  * vertex labels can be stored in separate list
#  * edge weights must be stored in 'dict of dicts' wss where wss[u][v] is the weight of (u,v)

# Dictionary representation of adjacency list
#  * all vertices each have an id/key/label into the dictionary
#  * edge weights must be stored in 'list of lists' wss where wss[u][v] is the weight of (u,v)

# Internally an undirected graph is represented as a directed graph, where every edge (u,v)
# generates the two arcs (u,v) and (v,u).

# Undirected graph has Neighbors (edges) and Degree = len(edges)
# Directed graph has Successors/OutEdges (outgoing edges), Predecessors/InEdges (ingoing edges), and OutDegree/InDegree

# How do we identify/index a vertex (aka node)

# edge-list representation
#    G = {e=(u,v)} for all e in E


# dict-of_dicts (V = {key_1, key_2, ..., key_n})
def get_example_dict_repr():
    g = {"Alice": ["Bob", "Claire", "Frank"],
         "Bob": ["Alice"],
         "Claire": ["Alice", "Dennis", "Esther", "Frank"],
         "Dennis": ["Claire", "Esther", "George"],
         "Esther": ["Claire", "Dennis"],
         "Frank": ["Alice", "Claire", "George"],
         "George": ["Dennis", "Frank"]
         }
    return g


# list-of-lists repr (V = {0, 1, 2, ..., n-1})
def get_example_list_repr():
    # n = 7, m = 9
    # it is not a requirement that the neighbor-lists are all sorted (but this make binary searches possible)
    graph = [[1, 2, 5],  # neighbors of 0
             [0],  # neighbors of 1
             [0, 3, 4, 5],  # neighbors of 2
             [2, 4, 6],  # neighbors of 3
             [2, 3],  # neighbors of 4
             [0, 2, 6],  # neighbors of 5
             [3, 5]]  # neighbors of 6
    return graph


def get_edge_list_example():
    # n = 7, m = 9
    graph = directed_edge_list([(0, 1), (0, 2), (0, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 6), (5, 6)])
    return graph


def equal_graphs(g1, g2):
    # len works on dict too!!!
    n1 = len(g1)
    n2 = len(g2)
    if n1 != n2:
        return False
    # convert to vertices list (i.e. the keys abstraction)
    if isinstance(g1, dict) and isinstance(g2, dict):
        vertices = g1.keys()
    elif isinstance(g1, list) and isinstance(g2, list):
        vertices = range(len(g1))
    else:
        raise TypeError('Graph is of wrong type')

    for vertex in vertices:
        heads1 = g1[vertex]
        heads2 = g2[vertex]
        if len(heads1) != len(heads2):
            return False
        sorted_heads1 = sort(heads1)
        sorted_heads2 = sort(heads2)
        if sorted_heads1 != sorted_heads2:
            return False
    return True


# insertion sort done in-place of copied array of distinct indices
def sort(xs):
    ys = xs[:]
    # in-place insertion sort
    for i in range(2, len(ys)):
        j = i
        while j > 0 and ys[j] < ys[j - 1]:
            ys[j], ys[j - 1] = ys[j - 1], ys[j]
            j -= 1
    return ys


# factory method (from_edge_list) to create an undirected graph
def directed_edge_list(es):
    n = vertex_count(es)
    # allocate list of empty neighbors
    g = []
    for i in range(n):
        g.append([])
    # add edges
    for e in es:
        u = e[0]
        v = e[1]
        g[u].append(v)
        g[v].append(u)
    return g


def vertex_count(es):
    m = -1
    for e in es:
        if e[0] > m:
            m = e[0]
        if e[1] > m:
            m = e[1]
    return m + 1


#
# Graph methods
#


# Load the file into a graph represented by a dict of lists
def graph_from_file(fn):
    g = {}

    f = open(fn)
    lines = f.readlines()
    f.close()

    # replace any whitespace with a single space and trim leading/trailing whitespace
    lines = map(lambda s: sub(r'\s+', ' ', str(s.strip('\r\n'))).strip(), lines)
    # then convert each line to a list of words
    list_of_words = map(lambda s: s.split(' '), lines)

    # parse each word of every line as an integer
    for words in list_of_words:
        g[int(words[0])] = list(map(lambda s: int(s), words[1:]))  # list() forces iterator evaluation

    return g


# one-liner for load graph
def load_graph():
    return {int(line.rstrip().split()[0]): [int(i) for i in line.rstrip().split()[1:]] for line in
            open("kargerMinCut.txt")}


def print_graph(graph):
    for key in graph:
        print("{}: {}".format(key, graph[key]))

# TODO: dot file printer


# this all symmetric arcs (only half of them is the edge count)
def get_arc_list(graph):
    return [(v, w) for v in graph for w in graph[v]]


def get_edge_list(graph):
    return [(v, w) for v in graph for w in graph[v] if v < w]


def contract_edge(graph, super_vertices, edge):
    v = edge[0]  # tail
    w = edge[1]  # head
    # replace vertex v and w with new merged super-vertex
    # (i.e. merge w into v and remove w from graph)
    graph[v].extend(graph[w])
    del graph[w]
    # replace all occurrences of w with v
    # TODO: replace_all(xs, before, after)

    # Because edges are symmetrical (bi-directional, undirected), we can search all successors of w for the edges
    # for x in graph[w]:
    #     graph[x].remove(w)
    #     graph[x].append(v)

    for k, heads in graph.items():
        graph[k] = [v if x == w else x for x in heads]

    # Remove all edges of v to itself (i.e. remove self-loops)
    # graph[v].remove(v)  # TODO: remove_all(xs, val) (multi-graph has parallel edges)
    graph[v] = [x for x in graph[v] if x != v]

    # union-add
    super_vertices[v].update(super_vertices[w])
    del super_vertices[w]


# this will finally report the cut size, when only two vertices remain
def get_arc_length(graph):
    head_count = sum(len(vs) for vs in graph.values())
    return head_count


# (1, 3) and (3, 1) are counted as one (normalized) edge
def get_edge_length(graph):
    return get_arc_length(graph) // 2


# arc_index means all (non-normalized) edges
def get_arc(graph, arc_index):
    for vertex_key, heads in graph.items():
        l = len(heads)
        if arc_index < l:
            tail = vertex_key
            head = heads[arc_index]
            return tail, head
        else:
            arc_index -= l
    raise IndexError('index is out of range.')


# arc vs edge
# pick a random edge (=pair)
def get_random_edge(graph):
    c = get_arc_length(graph)
    edge_index = randint(0, c - 1)
    return get_arc(graph, edge_index)


# The answer should be : the number of min cuts is 2 and the cuts are at edges [(1,7), (4,5)]
def get_test_case_graph():
    # n = 8, m = 14
    # NOTE: each edge is represented 2 times for undirected graph
    # (edge_length = sum(len(heads) for heads in graph.values()) / 2)
    g = {1: [2, 3, 4, 7],
         2: [1, 3, 4],
         3: [1, 2, 4],
         4: [1, 2, 3, 5],
         5: [4, 6, 7, 8],
         6: [5, 7, 8],
         7: [1, 5, 6, 8],
         8: [5, 6, 7]
         }
    return g


# single run of contraction algorithm (NOTE: This mutates the graph)
def karger_single_run(graph):
    # dict of singleton sets with original vertex labels/ids
    super_vertices = {v: {v} for v in graph}
    # Keep contracting the graph until we have 2 vertices
    while len(graph) > 2:
        random_edge = get_random_edge(graph)
        contract_edge(graph, super_vertices, random_edge)

    # the size is the length of any of the two adjacency lists (of same length)
    keys = list(graph.keys())
    size = len(graph[keys[0]])

    # return the cut-size and the cut-groupings
    return size, list(super_vertices.values())


def is_crossing(edge, cut):
    v = edge[0]
    w = edge[1]
    first_group = cut[0]
    second_group = cut[1]
    return (v in first_group and w in second_group) or (v in second_group and w in first_group)


def is_valid_cut(graph, cut):
    first_group = cut[0]
    second_group = cut[1]
    return first_group.isdisjoint(second_group) and first_group.union(second_group) == {v for v in graph}


def get_crossing_edge_list(graph, cut):
    assert is_valid_cut(graph, cut)
    return [e for e in get_edge_list(graph) if is_crossing(e, cut)]


def karger(graph):
    # Repeat 20*n^2 times
    # n = len(graph)
    # TODO: Problem that each repetition is slow for the kargerMinCut.txt graph
    repetitions = 100  # 20 * n * n
    min_size = get_edge_length(graph)  # NOTE: This can be any (BIG) number
    i = 1
    for _ in repeat(None, repetitions):
        g = deepcopy(graph)
        size, cut = karger_single_run(g)
        print(i)
        if size < min_size:
            min_size = size
            min_cut = cut
        i += 1
    # noinspection PyUnboundLocalVariable
    return min_cut, min_size

#
# General purpose Graph Methods
#


# Each function's input graph G should be represented in such a way that "for v in G" loops through the vertices,
# and "G[v]" produces a list of the neighbors of v; for instance, G may be a dictionary mapping each vertex to
# its neighbor set.
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


def max_degree(graph):
    """Return the maximum vertex (out)degree of a graph."""
    return max([len(graph[v]) for v in graph])


def min_degree(graph):
    """Return the minimum vertex (out)degree of a graph."""
    return min([len(graph[v]) for v in graph])


#
# Graph Class (suitable for contraction algorithm)
#


#
# Main
#

def main():
    xs = [3, 7, 4, 1, 9]
    print(f'{xs} sorted is {sort(xs)}')
    g3 = get_edge_list_example()
    g4 = get_example_list_repr()
    print(f'The graphs are identical: {equal_graphs(g3, g4)}')

    g3 = get_test_case_graph()
    g4 = graph_from_file('test.txt')
    print(f'The graphs are identical: {equal_graphs(g3, g4)}')
    print(f'The edge-list is {get_edge_list(g3)}')

    min_cut, min_size = karger(g3)
    print(f'The minimum cut {min_cut} has crossing edge-list {get_crossing_edge_list(g3, min_cut)} of size {min_size}.')

    g5 = graph_from_file('kargerMinCut.txt')
    print(f'n = {len(g5)}, m = {get_edge_length(g5)}')

    # The correct answer should be 17
    min_cut2, min_size2 = karger(g5)
    print(f'The minimum cut {min_cut2} has crossing edge-list {get_crossing_edge_list(g5, min_cut2)} ',
          f'of size {min_size2}.')


if __name__ == '__main__':
    main()
