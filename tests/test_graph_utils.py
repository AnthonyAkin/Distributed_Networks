import unittest
import os
import random
from graph_utils import GraphGenerator
from SimpleGraph import load_file

class TestGraphGenerator(unittest.TestCase):
    def setUp(self):
        # return super().setUp()
        self.filename = "temp_file.txt"
        # self.readfile = "test_file.json"
        random.seed()

    def tearDown(self):
        # return super().tearDown()
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_node_count(self):
        n = random.randint(2, 32)
        p = random.random()
        nodes, _ = GraphGenerator.generate_edges(n, p)
        self.assertEqual(len(nodes), n)

    def test_edge_labels(self):
        cases = ["S", "N", "H", "L"]
        n = random.randint(0, 32)
        p = random.random()

        for case in cases:
            with self.subTest(label_case=case):
                nodes, _ = GraphGenerator.generate_edges(n, p, labels=case)

                if case == "S":
                    self.assertTrue(all(isinstance(x, int) for x in nodes))
                else:
                    if not nodes:
                        self.assertEqual(n, 0, "Node list is empty but n isn't 0")
                    else:   
                        expected_length = len(nodes[0])
                        for x in nodes:
                            self.assertIsInstance(x, str)
                            self.assertEqual(len(x), expected_length, f"Node {x} has inconsistent length")

    def test_read_write_file(self):
        n = random.randint(2, 12)
        p = random.random()
        nodes, edges = GraphGenerator.generate_edges(n, p)
        GraphGenerator.save_by_nodes(self.filename, nodes, edges)
        n_count = 0
        e_count = 0
        # with open(self.filename, 'r') as f:
        #     for line in f:
        #         n_count += 1
        #         array = line.strip("\n").split(" ")
        #         print(array)
        array = load_file(self.filename)
        for _, neigbours in array:
            n_count += 1
            # print(">", neigbours)
            e_count += len(neigbours)
    
        # self.assertEqual(n_count, n+1)
        # print(">", edges)
        # print(len(edges))
        self.assertEqual(n_count, n)
        self.assertEqual(e_count, len(edges) - sum(bool(edge[1] == None) for edge in edges))
        GraphGenerator.save_by_edges(self.filename, nodes, edges)
        # with open(self.filename, 'r') as f:
        #     for _ in f:
        #         e_count += 1
        # self.assertEqual(e_count, len(edges)+1)
        with open(self.filename, 'r') as f:
            i = 0
            for line in f:
                if i == 0:
                    line_array = line.strip("\n").split(" ")
                    print("> ", line_array)
                    self.assertEqual(int(line_array[0]), n_count)
                    self.assertEqual(int(line_array[1]), e_count)
                    i += 1
        

    def test_weights(self):
        n = random.randint(2, 12)
        w = random.randint(0, 10)
        p = random.random()

        nodes, edges = GraphGenerator.generate_edges(n, p, weighted = w)
        self.assertTrue(all(edge[2] != None for edge in edges))




