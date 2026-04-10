import random
import json
import math

class GraphGenerator:
    @staticmethod #This is a "toolbox" class, used to help parse information rather than directly store it.
    def generate_edges(num_nodes, p, *, directional = True, labels = "S", weighted = False):

        # if (num_nodes < 1) and (num_nodes % 1 == 0):
        #     print("Please request a graph size with a natural number larger than 2")
        #     return 0
        
        edges   = []
        nodes   = None
        # weights = []
        
        match labels: #Option set for label alphabet
            case "S":
                print("Standard Numbered")
                nodes = list(range(num_nodes))
                char_set = list(range(num_nodes))
            case "N":
                print("Fixed-Length Numbered")
                char_set = "0123456789"
            case "H":
                print("Hexadecimal")
                char_set = "0123456789ABCDEF"
            case "L":
                print("Latin Alphabet")
                char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            case _:
                print("Invalid label argument")
                return 0
        
        if not nodes:
            nodes = GraphGenerator.__generate_labels(num_nodes, char_set)

        for i in range(num_nodes):
            start_index = 0 if directional else i + 1

            for j in range(start_index, num_nodes):
                if j == i:
                    continue
                
                w = random.randint(0, weighted) if weighted else None

                if random.random() < p:
                    u, v  = nodes[i], nodes[j]
                    edges.append((u, v, w))
                    if not directional:
                        edges.append((v, u, w))
    
        # print("Nodes: ", nodes, "\nEdges: ", edges)
        for node in nodes:
            if not any(node in edge for edge in edges):
                edges.append((node, None, None))
                # print(edges)
                print((node, None, None))

        return nodes, edges
    
    @staticmethod
    def __generate_labels(num_nodes, label_set):
        base = len(label_set)
        width = math.ceil(math.log(num_nodes, base)) if num_nodes > 1 else 1
        format = [base**i for i in reversed(range(width))]
        casting = ["".join([label_set[(num // label) % base] for label in format]) for num in range(num_nodes)]
        return casting   
    
    # @staticmethod
    # def save_as_json(filepath, nodes, edges):
    #     """
    #     Saves in your 'populate' format: [[node, [neighbors]], ...]
    #     """
    #     # Group edges by source
    #     adj = {node: [] for node in nodes}
    #     for u, v in edges:
    #         adj[u].append(v)
            
    #     # Convert to the nested list format your SimpleGraph.populate expects
    #     formatted_data = [[node, neighbors] for node, neighbors in adj.items()]
        
    #     with open(filepath, 'w') as f:
    #         json.dump(formatted_data, f, indent=4)

    @staticmethod
    def save_by_nodes(filepath, nodes, edges):
        """
        Saves in your 'populate' format: [[node, [neighbors]], ...]
        """
        # Group edges by source
        # adj = {node: [] for node in nodes}
        adj = {node: {} for node in nodes}
        for u, v, w in edges:
            # adj[u].append(v)
            # if v == None:
                # continue
            adj[u][v] = w

        # print(adj.items())
        # for _, neighbours in adj.items():
        #     for edge, weight in neighbours.items():
        #         if weight == None:
        #             print("passed")
        #         print([edge, weight])
        # print(','.join(['01']))
        # print(str(None))

        # Convert to the nested list format your SimpleGraph.populate expects
        # formatted_data = [[node, neighbors] for node, neighbors in adj.items()]

        with open(filepath, 'w') as f:
            f.write(f"{len(nodes)} {len(edges) - sum(bool(edge[1] == None) for edge in edges)}\n")
            for node, neighbours in adj.items():
                # f.write(f"{node} {' '.join(map(str, neighbours))}\n")
                # f.write(f"{node} {' '.join([','.join(map(str, [edge, weight]) if weight != None else str(edge)) for edge, weight in neighbours.items()])}\n")
                f.write(f"{node} {' '.join([','.join(map(str, [edge, weight]) if weight != None else [str(edge) if edge != None else '']) for edge, weight in neighbours.items()])}\n")
                # f.write(f"{node} {' '.join([','.join(map(str, [edge, weight]) if weight != None else(str(edge) if edge != None else '')) for edge, weight in neighbours.items()])}\n")

    @staticmethod
    def save_by_edges(filepath, nodes, edges):
        """
        Saves in C++ friendly format:
        Nodes Edges
        u v
        """
        with open(filepath, 'w') as f:
            f.write(f"{len(nodes)} {len(edges) - sum(bool(edge[1] == None) for edge in edges)}\n")
            for u, v, w in edges:
                f.write(f"{u} {v if v != None else ''}{',' + str(w) if w != None else ''}\n")









if __name__ == "__main__":
    nodes, edges = GraphGenerator.generate_edges(16, 0.1, labels="L", weighted=10)
    # GraphGenerator.save_as_json("graph_data.json", nodes, edges)
    print(edges)
    # GraphGenerator.save_by_edges("graph_data.txt", nodes, edges)
    GraphGenerator.save_by_nodes("test_data.txt", nodes, edges)
    # GraphGenerator.save_by_edges("test_data.txt", nodes, edges)
