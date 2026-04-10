import unittest
from SimpleGraph import SimpleGraph
from graph_utils import GraphGenerator

class TestSimpleGraph(unittest.TestCase):
    def setUp(self):
        self.g = SimpleGraph()
        self.test_file = "test_file.json"
        # return super().setUp()

    # def tearDown(self):
        # return super().tearDown()

    def test_inferred_nodes(self):
        self.g.populate([["A", ["B"]]])
        self.assertIn("A", self.g.graph)
        self.assertIn("B", self.g.graph)

    def test_undirectional(self):
        self.g.populate([["A", ["B"]]], directional = False)
        self.assertIn("A", self.g.get_neighbours("B"))

    def test_sorting_neigbours(self):
        self.g.populate([["A", ["Z", "S", "B", "W"]]])
        self.assertEqual(self.g.get_neighbours("A"), ["B", "S", "W", "Z"])