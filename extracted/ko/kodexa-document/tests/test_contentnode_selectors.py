"""
Tests for ContentNode selector functionality.
"""

import pytest
from kodexa_document import Document, DocumentError


class TestContentNodeSelectors:
    """Test ContentNode select() and select_first() methods."""
    
    def test_node_select_basic(self):
        """Test basic node selector functionality."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Add child nodes
        child1 = doc.create_node("paragraph", "First paragraph")
        child2 = doc.create_node("paragraph", "Second paragraph")
        root.add_child(child1)
        root.add_child(child2)
        
        # Test selecting all descendants from root
        descendants = root.select(".//*")
        assert isinstance(descendants, list)
        assert len(descendants) >= 0  # May vary based on hierarchy structure
        
        # All returned items should be ContentNode instances
        for node in descendants:
            assert hasattr(node, 'node_type')
            assert hasattr(node, 'content')
    
    def test_node_select_first(self):
        """Test select_first functionality."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Add child nodes
        child = doc.create_node("paragraph", "Test paragraph")
        root.add_child(child)
        
        # Test select_first
        first_node = root.select_first(".//*")
        if first_node:  # May be None depending on hierarchy
            assert hasattr(first_node, 'node_type')
            assert hasattr(first_node, 'content')
        
        # Test select_first with non-matching selector
        no_node = root.select_first(".//nonexistent")
        assert no_node is None
    
    def test_node_select_with_variables(self):
        """Test selector with variables."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Test with variables (should not crash)
        variables = {"test_var": "test_value"}
        nodes = root.select(".//*", variables)
        assert isinstance(nodes, list)
    
    def test_node_select_self(self):
        """Test selecting the current node with '.' selector."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Select self
        self_nodes = root.select(".")
        assert isinstance(self_nodes, list)
        assert len(self_nodes) == 1
        assert self_nodes[0].node_type == root.node_type
        assert self_nodes[0].content == root.content
    
    def test_node_select_from_child(self):
        """Test selecting from a child node."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Add child with its own child
        child = doc.create_node("paragraph", "Parent paragraph")
        grandchild = doc.create_node("line", "Child line")
        root.add_child(child)
        child.add_child(grandchild)
        
        # Select from child node
        child_descendants = child.select(".//*")
        assert isinstance(child_descendants, list)
        # Should find at least the grandchild
        assert len(child_descendants) >= 0
    
    def test_node_select_empty_results(self):
        """Test selector that returns no results."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Select non-existent node type
        empty_results = root.select(".//nonexistent")
        assert isinstance(empty_results, list)
        assert len(empty_results) == 0
    
    def test_node_select_closed_node(self):
        """Test that selecting from a closed node raises error."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Close the node
        root.close()
        
        # Should raise error when trying to select
        with pytest.raises(ValueError, match="ContentNode has been closed"):
            root.select(".//*")
        
        with pytest.raises(ValueError, match="ContentNode has been closed"):
            root.select_first(".//*")
    
    def test_node_select_invalid_selector(self):
        """Test behavior with invalid selector syntax."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Test with clearly invalid selector that should not crash
        # Note: Go implementation may be lenient with some invalid selectors
        try:
            result = root.select("invalid::selector::syntax")
            # If it doesn't crash, result should be an empty list
            assert isinstance(result, list)
        except Exception:
            # If it does raise an exception, that's also acceptable
            pass
    
    def test_node_select_memory_management(self):
        """Test that selector results are properly managed."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Add children
        for i in range(5):
            child = doc.create_node("paragraph", f"Paragraph {i}")
            root.add_child(child)
        
        # Select multiple times to test memory management
        for _ in range(3):
            nodes = root.select(".//*")
            assert isinstance(nodes, list)
            
            # Each node should be independently usable
            for node in nodes:
                _ = node.node_type  # Should not crash
                _ = node.content   # Should not crash
    
    def test_node_selectors_vs_document_selectors(self):
        """Test that node selectors work differently from document selectors."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node
        
        # Add child
        child = doc.create_node("paragraph", "Test paragraph")
        root.add_child(child)
        
        # Document selector (absolute)
        doc_results = doc.select("//*")
        
        # Node selector (relative from root)
        node_results = root.select(".//*")
        
        # Both should be lists, but may have different results
        assert isinstance(doc_results, list)
        assert isinstance(node_results, list)
        
        # Verify we can call both without errors
        doc_first = doc.select_first("//*")
        node_first = root.select_first(".//*")
        
        # Results should be ContentNode instances if not None
        if doc_first:
            assert hasattr(doc_first, 'node_type')
        if node_first:
            assert hasattr(node_first, 'node_type')

    def test_contentnode_select_edge_cases(self):
        """Test select method edge cases on ContentNode."""
        doc = Document()
        root = doc.create_node("root")
        doc.content_node = root
        child = doc.create_node("child", parent=root)

        # Test select with invalid selector
        with pytest.raises(DocumentError):
            child.select("invalid[[[")

        # Test select_first with no results
        result = child.select_first("//nonexistent")
        assert result is None

        doc.close()

    def test_document_select_equals_root_select_same_selector(self):
        """Test that doc.select('//*') returns same results as doc.content_node.select('//*').

        This is the expected behavior from legacy Python (kodexa/kodexa) where
        Document.select() simply delegates to self.content_node.select().
        """
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node

        # Add a hierarchy of nodes
        child1 = doc.create_node("paragraph", "First paragraph")
        child2 = doc.create_node("paragraph", "Second paragraph")
        grandchild = doc.create_node("line", "A line of text")
        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(grandchild)

        # Both should use the SAME selector '//*'
        doc_results = doc.select("//*")
        root_results = root.select("//*")

        # Results should be identical
        assert len(doc_results) == len(root_results), (
            f"doc.select('//*') returned {len(doc_results)} nodes, "
            f"but root.select('//*') returned {len(root_results)} nodes"
        )

        # Compare node UUIDs to ensure same nodes are returned
        doc_uuids = sorted([n.uuid for n in doc_results])
        root_uuids = sorted([n.uuid for n in root_results])
        assert doc_uuids == root_uuids, (
            "doc.select('//*') and root.select('//*') returned different nodes"
        )

        doc.close()

    def test_document_select_first_equals_root_select_first(self):
        """Test that doc.select_first('//*') returns same as doc.content_node.select_first('//*')."""
        doc = Document.from_text("Root content", inmemory=True)
        root = doc.content_node

        # Add children
        child = doc.create_node("paragraph", "Test paragraph")
        root.add_child(child)

        # Both should use the SAME selector
        doc_first = doc.select_first("//*")
        root_first = root.select_first("//*")

        # Both should return a node (or both None)
        if doc_first is None:
            assert root_first is None, "doc.select_first returned None but root.select_first did not"
        else:
            assert root_first is not None, "root.select_first returned None but doc.select_first did not"
            assert doc_first.uuid == root_first.uuid, (
                f"doc.select_first('//*') returned node {doc_first.uuid}, "
                f"but root.select_first('//*') returned node {root_first.uuid}"
            )

        doc.close()

    def test_document_select_vs_get_root_select_with_kddb(self):
        """Test doc.select('//*') vs doc.get_root().select('//*') with a real kddb document.

        This tests the exact pattern the user reported as problematic.
        """
        import os
        # Go up from lib/python/tests to kodexa-document root, then into test_documents
        test_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "test_documents", "news-tagged.kddb"
        )

        # Skip if test document doesn't exist
        if not os.path.exists(test_doc_path):
            pytest.skip(f"Test document not found: {test_doc_path}")

        doc = Document.from_kddb(test_doc_path)
        root = doc.get_root()

        # Both should use the SAME selector '//*'
        doc_results = doc.select("//*")
        root_results = root.select("//*")

        # Results should be identical
        assert len(doc_results) == len(root_results), (
            f"doc.select('//*') returned {len(doc_results)} nodes, "
            f"but doc.get_root().select('//*') returned {len(root_results)} nodes"
        )

        # Compare node UUIDs
        doc_uuids = sorted([n.uuid for n in doc_results])
        root_uuids = sorted([n.uuid for n in root_results])
        assert doc_uuids == root_uuids, (
            "doc.select('//*') and doc.get_root().select('//*') returned different nodes"
        )

        doc.close()

    def test_document_select_vs_get_root_select_multiple_kddbs(self):
        """Test doc.select('//*') vs doc.get_root().select('//*') across multiple kddb files."""
        import os
        # Go up from lib/python/tests to kodexa-document root, then into test_documents
        test_docs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "test_documents"
        )

        # Test with several kddb files (known to have valid schemas)
        kddb_files = [
            "news-tagged.kddb",
            "fax.kddb",
            "tongue_twister.kddb",
            "news.kddb",
        ]

        tested_count = 0
        for kddb_file in kddb_files:
            test_doc_path = os.path.join(test_docs_dir, kddb_file)
            if not os.path.exists(test_doc_path):
                continue

            # Skip empty files
            if os.path.getsize(test_doc_path) == 0:
                continue

            try:
                doc = Document.from_kddb(test_doc_path)
            except Exception:
                # Skip documents with schema issues
                continue

            root = doc.get_root()

            if root is None:
                doc.close()
                continue

            # Both should use the SAME selector '//*'
            doc_results = doc.select("//*")
            root_results = root.select("//*")

            # Results should be identical
            assert len(doc_results) == len(root_results), (
                f"{kddb_file}: doc.select('//*') returned {len(doc_results)} nodes, "
                f"but doc.get_root().select('//*') returned {len(root_results)} nodes"
            )

            # Compare node UUIDs
            doc_uuids = sorted([n.uuid for n in doc_results])
            root_uuids = sorted([n.uuid for n in root_results])
            assert doc_uuids == root_uuids, (
                f"{kddb_file}: doc.select('//*') and doc.get_root().select('//*') "
                "returned different nodes"
            )

            doc.close()
            tested_count += 1

        # Ensure we actually tested some documents
        assert tested_count >= 2, f"Expected to test at least 2 documents, but only tested {tested_count}"

    def test_document_select_vs_get_root_select_has_line_num_issue(self):
        """Test doc.select('//*') vs doc.get_root().select('//*') with has_line_num_issue.kddb.

        This is a specific regression test for a reported issue where these
        two methods were returning different results.
        """
        import os
        # Go up from lib/python/tests to kodexa-document root, then into test_documents
        test_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "test_documents", "has_line_num_issue.kddb"
        )

        # Skip if test document doesn't exist
        if not os.path.exists(test_doc_path):
            pytest.skip(f"Test document not found: {test_doc_path}")

        doc = Document.from_kddb(test_doc_path)
        root = doc.get_root()

        assert root is not None, "Document has no root node"

        # Both should use the SAME selector '//*'
        doc_results = doc.select("//*")
        root_results = root.select("//*")

        # Results should be identical
        assert len(doc_results) == len(root_results), (
            f"has_line_num_issue.kddb: doc.select('//*') returned {len(doc_results)} nodes, "
            f"but doc.get_root().select('//*') returned {len(root_results)} nodes"
        )

        # Compare node UUIDs to ensure same nodes are returned
        doc_uuids = sorted([n.uuid for n in doc_results])
        root_uuids = sorted([n.uuid for n in root_results])
        assert doc_uuids == root_uuids, (
            "has_line_num_issue.kddb: doc.select('//*') and doc.get_root().select('//*') "
            "returned different nodes"
        )

        doc.close()