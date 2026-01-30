from unittest import TestCase

from .graph import Edge, Graph, Node


class TestGraph(TestCase):
    def test_from_primitives_creates_graph(self):
        """Test that from_primitives creates a valid graph"""
        nodes = [Node(id="a"), Node(id="b"), Node(id="c")]
        edges = [
            Edge(source_id="a", target_id="b"),
            Edge(source_id="b", target_id="c"),
        ]

        graph = Graph.from_primitives(nodes, edges)

        self.assertEqual(len(graph.cache), 3)
        self.assertEqual(len(graph.cache["a"].points_to), 1)
        self.assertEqual(graph.cache["a"].points_to[0].id, "b")
        self.assertEqual(len(graph.cache["b"].points_to), 1)
        self.assertEqual(graph.cache["b"].points_to[0].id, "c")

    def test_from_primitives_handles_orphan_target_edge(self):
        """Test that orphan edges with non-existent target are skipped gracefully"""
        nodes = [Node(id="a"), Node(id="b")]
        edges = [
            Edge(source_id="a", target_id="b"),  # Valid
            Edge(
                source_id="a", target_id="non-existent"
            ),  # Orphan - target doesn't exist
        ]

        # Should not raise, should ignore orphan edge
        graph = Graph.from_primitives(nodes, edges)

        self.assertEqual(len(graph.cache), 2)
        self.assertEqual(len(graph.cache["a"].points_to), 1)  # Only valid edge
        self.assertEqual(graph.cache["a"].points_to[0].id, "b")

    def test_from_primitives_handles_orphan_source_edge(self):
        """Test that orphan edges with non-existent source are skipped gracefully"""
        nodes = [Node(id="a"), Node(id="b")]
        edges = [
            Edge(source_id="a", target_id="b"),  # Valid
            Edge(
                source_id="non-existent", target_id="b"
            ),  # Orphan - source doesn't exist
        ]

        # Should not raise, should ignore orphan edge
        graph = Graph.from_primitives(nodes, edges)

        self.assertEqual(len(graph.cache), 2)
        self.assertEqual(len(graph.cache["b"].is_pointed_by), 1)  # Only valid edge
        self.assertEqual(graph.cache["b"].is_pointed_by[0].id, "a")

    def test_from_primitives_handles_all_orphan_edges(self):
        """Test that when ALL edges are orphans, graph still loads correctly"""
        nodes = [Node(id="a"), Node(id="b")]
        edges = [
            Edge(source_id="x", target_id="y"),  # Both non-existent
            Edge(source_id="a", target_id="z"),  # Target non-existent
            Edge(source_id="w", target_id="b"),  # Source non-existent
        ]

        # Should not raise, should create graph with no edges
        graph = Graph.from_primitives(nodes, edges)

        self.assertEqual(len(graph.cache), 2)
        self.assertEqual(len(graph.cache["a"].points_to), 0)
        self.assertEqual(len(graph.cache["a"].is_pointed_by), 0)
        self.assertEqual(len(graph.cache["b"].points_to), 0)
        self.assertEqual(len(graph.cache["b"].is_pointed_by), 0)

    def test_from_primitives_empty_inputs(self):
        """Test that empty nodes and edges work correctly"""
        graph = Graph.from_primitives([], [])

        self.assertEqual(len(graph.cache), 0)

    def test_next_to(self):
        """Test next_to returns correct nodes"""
        nodes = [Node(id="a"), Node(id="b"), Node(id="c")]
        edges = [
            Edge(source_id="a", target_id="b"),
            Edge(source_id="a", target_id="c"),
        ]

        graph = Graph.from_primitives(nodes, edges)

        next_nodes = graph.next_to("a")
        self.assertEqual(len(next_nodes), 2)
        next_ids = [n.id for n in next_nodes]
        self.assertIn("b", next_ids)
        self.assertIn("c", next_ids)

    def test_previous_to(self):
        """Test previous_to returns correct nodes"""
        nodes = [Node(id="a"), Node(id="b"), Node(id="c")]
        edges = [
            Edge(source_id="a", target_id="c"),
            Edge(source_id="b", target_id="c"),
        ]

        graph = Graph.from_primitives(nodes, edges)

        prev_nodes = graph.previous_to("c")
        self.assertEqual(len(prev_nodes), 2)
        prev_ids = [n.id for n in prev_nodes]
        self.assertIn("a", prev_ids)
        self.assertIn("b", prev_ids)

    def test_all_neighbors(self):
        """Test all_neighbors returns both incoming and outgoing nodes"""
        nodes = [Node(id="a"), Node(id="b"), Node(id="c")]
        edges = [
            Edge(source_id="a", target_id="b"),
            Edge(source_id="b", target_id="c"),
        ]

        graph = Graph.from_primitives(nodes, edges)

        neighbors = graph.all_neighbors("b")
        self.assertEqual(len(neighbors), 2)
        neighbor_ids = [n.id for n in neighbors]
        self.assertIn("a", neighbor_ids)  # Points to b
        self.assertIn("c", neighbor_ids)  # b points to c
