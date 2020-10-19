from re import sub
from random import randint


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


def contract_edge(graph, edge):
    v = edge[0]  # tail
    w = edge[1]  # head
    # replace vertex v and w with new merged super-vertex
    # (i.e. merge w into v and remove w from graph)
    graph[v].extend(graph[w])
    del graph[w]
    # replace all occurrences of w with v
    for k, heads in graph.items():
        graph[k] = [v if x == w else x for x in heads]
    # Remove all edges of v to itself (i.e. remove self-loops)
    # graph[v].remove(v)  # TODO: remove_all (multi-graph has parallel edges)
    graph[v] = [x for x in graph[v] if x != v]


# this will finally report the cut size, when only two vertices remain
def get_edge_length(graph):
    return sum(len(vs) for vs in graph)


def get_edge(graph, edge_index):
    for vertex_key, heads in graph:
        l = len(heads)
        if edge_index < l:
            tail = vertex_key
            head = heads[edge_index]
            return tail, head
        else:
            edge_index -= l
    raise IndexError('index is out of range.')


# pick a random edge (=pair)
def get_random_edge(graph):
    edge_index = randint(0, graph.get_edge_length() - 1)
    return graph.get_edge(edge_index)


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
    # Keep contracting the graph until we have 2 vertices
    while len(graph) > 2:
        random_edge = get_random_edge(graph)
        contract_edge(graph, random_edge)

    # TODO: How do we keep track of subset/cut???

    # the size is the length of any of thw two adjacency lists (of same length)
    size = len(graph[graph.keys()[0]])
    return size


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


if __name__ == '__main__':
    main()
