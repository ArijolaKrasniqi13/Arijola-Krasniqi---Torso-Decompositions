import tempfile
import unittest
from pathlib import Path

from torso_decomposition.graph import Graph, read_edge_list


class GraphTests(unittest.TestCase):
    def test_from_edges_is_undirected_and_deduplicates(self):
        graph = Graph.from_edges([(0, 1), (1, 0), (1, 2)], 3)
        self.assertEqual(graph.adjacency[0], frozenset({1}))
        self.assertEqual(graph.adjacency[1], frozenset({0, 2}))

    def test_rejects_loop_and_out_of_range_vertex(self):
        with self.assertRaises(ValueError):
            Graph.from_edges([(0, 0)], 1)
        with self.assertRaises(ValueError):
            Graph.from_edges([(0, 2)], 2)

    def test_reads_edge_list_and_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "graph.txt"
            path.write_text("# sample\n0 1\n1 2 # tail\n", encoding="utf-8")
            graph = read_edge_list(path)
        self.assertEqual(graph.vertex_count, 3)
        self.assertEqual(graph.adjacency[1], frozenset({0, 2}))


if __name__ == "__main__":
    unittest.main()
