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


def equal_list_repr(g1, g2):
    n1 = len(g1)
    n2 = len(g2)
    if n1 != n2:
        return False
    for v in range(n1):
        heads1 = g1[v]
        heads2 = g2[v]
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


# In many applications we would like to name vertices by strings or tuples, rather than identifiers.
# For this purpose we propose to use a class Graph that permits to maintaining the mapping between
# vertex names and vertex identifiers.
class Graph:
    def __init__(self):
        self.neighbors = []  # out-edges (successors)
        self.name2node = {}  # dict
        self.node2name = []  # list
        self.weight = []  # optional weights (list of lists)

    def __len__(self):
        return len(self.node2name)

    # 'for v in G[w]' supports traversing the out-edges (G[w] are the heads of the tail w)
    def __getitem__(self, v):
        return self.neighbors[v]

    # returns the index
    def add_node(self, name):
        assert name not in self.name2node
        new_index = len(self.name2node)
        self.name2node[name] = new_index
        self.node2name.append(name)
        self.neighbors.append([])
        self.weight.append({})
        return new_index

    # add undirected (symmetric) edge
    def add_edge(self, name_u, name_v, weight_uv=None):
        # undirected graph
        self.add_arc(name_u, name_v, weight_uv)
        self.add_arc(name_v, name_u, weight_uv)

    # add directed edge
    def add_arc(self, name_u, name_v, weight_uv=None):
        u = self.name2node[name_u]
        v = self.name2node[name_v]
        self.neighbors[u].append(v)
        self.weight[u][v] = weight_uv


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


def main():
    xs = [3, 7, 4, 1, 9]
    print(f'{xs} sorted is {sort(xs)}')
    g1 = get_edge_list_example()
    g2 = get_example_list_repr()
    print(f'The graphs are identical: {equal_list_repr(g1, g2)}')


if __name__ == '__main__':
    main()
