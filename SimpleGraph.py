from collections import defaultdict

class SimpleGraph:
    """
    Object container for a simple unweighted graph.
    """
    def __init__(self):
        self.graph = {}
        self.__sorted = True

    def _add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def _add_edge(self, u, v):
        if v not in self.graph[u]:
            self.graph[u].append(v)
            self.__sorted = False

    def _undirectional_edge(self, u, v):
        self._add_edge(u, v)
        self._add_edge(v, u)

    def _sort(self):
        for node in self.graph:
            self.graph[node].sort()
        self.__sorted = True

    def populate(self, array, *, directional = True): # Assume Directional by default until told otherwise.
        nodes = {node for node, _ in array} | {edge for _, edges in array for edge in edges}

        for node in nodes:
            self._add_node(node)

        for node, edges in array:
            for edge in edges:
                if directional:
                    self._add_edge(node, edge)
                else:
                    self._undirectional_edge(node, edge)

        
    def get_neighbours(self, node):
        if not self.__sorted:
            self._sort()

        return self.graph.get(node, [])
    
    def __str__(self):
        if not self.__sorted:
            self._sort()
            
        entries = []
        edge_count = 0
        node_count = len(self.graph)
        for node, edges in sorted(self.graph.items()):
            string = f"{node}: {' '.join(edges)}"
            entries.append(string)
            edge_count += len(edges)
        entries.append(f"Total Node Count: {node_count} | Total Edge Count: {edge_count}")
        return "\n".join(entries)
    
class WeightedGraph(SimpleGraph):
    def __getitem__(self, items):
        return self.graph[items]
    
    def __contains__(self, A):
        return A in self.graph
    
    def _add_node(self, node):
        # if node not in self.graph:
        #     self[node] = {}
        self.graph.setdefault(node, {})

    def _add_edge(self, u, v, *, w = None):
        # if u in self.graph[v]:
        if u in self[v]:
            # if self.graph[v].get(u, None) != None:
            if self[v].get(u, None) != None:
                # w = self.graph[v][u]
                w = self[v][u]
        # self.graph[u].setdefault(v, w)
            else:
                self[v][u] = self[u].get(v, w)
        self[u].setdefault(v, w)
    
    def _undirectional_edge(self, u, v, *, w):
        self._add_edge(u, v, w=w)
        self._add_edge(v, u, w=w)

    def populate(self, array, *, directional=True):
        nodes = {node for node, _ in array} | {edge.split(",")[0] for _, edges in array for edge in edges}

        for node in nodes:
            self._add_node(node)

        for node, edges in array:
            for edge in edges:
                # entry = edge.split(",")
                # print(entry, len(entry))
                # if len(entry) == 1:
                #     w = None
                # else:
                #     w = entry[-1]
                line = edge.split(",") + [None]
                entry, w = line[:2]

                if directional:
                    # self._add_edge(node, entry[0], w=w)
                    self._add_edge(node, entry, w=w)
                else:
                    # self._undirectional_edge(node, entry[0], w=w)
                    self._undirectional_edge(node, entry, w=w)

    def __str__(self):
        entries = []
        edge_count = 0
        node_count = len(self.graph)
        for node, edges in sorted(self.graph.items()):
            # string = f"{node}: {' '.join(sorted(edges))}"
            string = f"{node}: {' '.join([edge + '=' + str(self[node][edge]) for edge in sorted(edges)])}"
            entries.append(string)
            edge_count += len(edges)
        entries.append(f"Total Node Count: {node_count} | Total Edge Count: {edge_count}")
        return "\n".join(entries)
        # return super().__str__()

def load_file(filename):
    array = []
    i = 0
    with open(filename) as f:
        for line in f:
            if i == 0:
                i += 1
                continue
            string_array = line.strip("\n").split(" ")
            # entry = [string_array[0], string_array[1:]]
            entry = [string_array[0], (string_array[1:] if string_array[1] != '' else [])]
            array.append(entry)
    print(array)
    return array
        
    

if __name__ == "__main__":
    # import unittest

    # class TestGraph(unittest.TestCase):
    #     def test_addition(self):
    #         g = SimpleGraph()
    #         # array = [["A", ["B", "C"]], ["B", ["C", "D"]], ["C", ["E", "F"]]] 
    #         array = [["A", ["C", "B"]], ["C", ["F", "E"]], ["B", ["C", "D"]]] 
    #         # array = [["A", ["C", "B"]], ["C", ["F", "E"]], ["B", ["C", "D"]], ["F", []]] 
    #         g.populate(array)
    #         self.assertIn("A", g.graph)
    #         # self.assertIn("F", g.get_neighbours("C"))
    #         print(g)
    
    # unittest.main()
    # g = WeightedGraph()
    # array = [["A", ["B", "C"]], ["B", ["C", "D"]], ["C", ["E", "F"]]]
    # # g.populate(array)
    # array = [["A", ["C,2", "B"]], ["C", ["F", "E", "A,3"]], ["B", ["C", "D"]]] 
    # array = [["A", ["C", "B"]], ["C", ["F", "E", "A,3"]], ["B", ["C", "D"]]] 
    # g.populate(array, directional=True)
    # print(g)
    # print(g["A"])
    # print(g["C"])
    # print("F" in g)
    array = load_file("test_data.txt")
    g = WeightedGraph()
    g.populate(array)
    print(g)