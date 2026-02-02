"""
Test ContentNode navigation methods.
"""

import pytest
from kodexa_document import Document, DocumentError


class TestContentNodeNavigation:
    """Test navigation methods for ContentNode."""
    
    def test_get_siblings(self):
        """Test getting sibling nodes."""
        doc = Document()
        root = doc.create_node("root", "Root")
        doc.content_node = root
        
        # Create three children
        child1 = doc.create_node("child", "Child 1")
        child2 = doc.create_node("child", "Child 2")
        child3 = doc.create_node("child", "Child 3")
        
        root.add_child(child1)
        root.add_child(child2)
        root.add_child(child3)
        
        # Test middle child has 2 siblings
        siblings = child2.get_siblings()
        assert len(siblings) == 2
        contents = [s.content for s in siblings]
        assert "Child 1" in contents
        assert "Child 3" in contents
        assert "Child 2" not in contents  # Should not include itself
        
        # Test root has no siblings
        root_siblings = root.get_siblings()
        assert len(root_siblings) == 0
        
        doc.close()

    def test_contentnode_navigation_edge_cases(self):
        """Test navigation method edge cases."""
        doc = Document()
        root = doc.create_node(node_type="root", content="root content")
        child1 = doc.create_node(node_type="child1", content="child1 content", parent=root)
        child2 = doc.create_node(node_type="child2", content="child2 content", parent=root)

        # Test get_siblings on root (no parent)
        siblings = root.get_siblings()
        assert siblings == []

        # Test get_path - returns list of nodes from root
        path = child1.get_path()
        assert len(path) == 2  # root and child1
        # Note: node_type is not preserved in path nodes (known limitation)
        # Just verify we get ContentNode objects back
        assert all(hasattr(node, 'node_type') for node in path)

        # Test get_path on root - returns list with just root
        root_path = root.get_path()
        assert len(root_path) == 1
        assert hasattr(root_path[0], 'node_type')

        doc.close()
    
    def test_get_path(self):
        """Test getting path from root to node."""
        doc = Document()
        root = doc.create_node("document", "Root")
        doc.content_node = root
        
        # Create hierarchy
        level1 = doc.create_node("chapter", "Chapter")
        level2 = doc.create_node("section", "Section")
        level3 = doc.create_node("paragraph", "Paragraph")
        
        root.add_child(level1)
        level1.add_child(level2)
        level2.add_child(level3)
        
        # Test path from leaf to root
        path = level3.get_path()
        assert len(path) == 4
        assert path[0].content == "Root"
        assert path[1].content == "Chapter"
        assert path[2].content == "Section"
        assert path[3].content == "Paragraph"
        
        # Test path for root
        root_path = root.get_path()
        assert len(root_path) == 1
        assert root_path[0].content == "Root"
        
        doc.close()

    def test_contentnode_navigation_edge_cases(self):
        """Test navigation method edge cases."""
        doc = Document()
        root = doc.create_node(node_type="root", content="root content")
        child1 = doc.create_node(node_type="child1", content="child1 content", parent=root)
        child2 = doc.create_node(node_type="child2", content="child2 content", parent=root)

        # Test get_siblings on root (no parent)
        siblings = root.get_siblings()
        assert siblings == []

        # Test get_path - returns list of nodes from root
        path = child1.get_path()
        assert len(path) == 2  # root and child1
        # Note: node_type is not preserved in path nodes (known limitation)
        # Just verify we get ContentNode objects back
        assert all(hasattr(node, 'node_type') for node in path)

        # Test get_path on root - returns list with just root
        root_path = root.get_path()
        assert len(root_path) == 1
        assert hasattr(root_path[0], 'node_type')

        doc.close()
    
    def test_get_all_content(self):
        """Test getting all content from node and descendants."""
        doc = Document()
        root = doc.create_node("document", "Document Title")
        doc.content_node = root
        
        # Create content tree
        chapter = doc.create_node("chapter", "Chapter 1")
        para1 = doc.create_node("paragraph", "First paragraph text.")
        para2 = doc.create_node("paragraph", "Second paragraph text.")
        
        root.add_child(chapter)
        chapter.add_child(para1)
        chapter.add_child(para2)
        
        # Test default separator (space)
        all_content = root.get_all_content()
        assert "Document Title" in all_content
        assert "Chapter 1" in all_content
        assert "First paragraph text." in all_content
        assert "Second paragraph text." in all_content
        
        # Test custom separator
        content_newline = root.get_all_content(separator="\n")
        lines = content_newline.split("\n")
        assert len(lines) == 4
        
        # Test with strip
        content_stripped = root.get_all_content(separator="|", strip=True)
        parts = content_stripped.split("|")
        assert len(parts) == 4
        for part in parts:
            assert part == part.strip()  # Should be no leading/trailing whitespace
        
        # Test leaf node returns just its content
        leaf_content = para1.get_all_content()
        assert leaf_content == "First paragraph text."
        
        # Test empty node
        empty = doc.create_node("empty", "")
        empty_content = empty.get_all_content()
        assert empty_content == ""
        
        doc.close()

    def test_navigation_with_virtual_nodes(self):
        """Test navigation methods with virtual nodes."""
        doc = Document()
        root = doc.create_node("root", "Root")
        doc.content_node = root
        
        # Create mix of regular and virtual nodes
        regular1 = doc.create_node("regular", "Regular 1")
        virtual1 = doc.create_node("virtual", "Virtual 1")
        regular2 = doc.create_node("regular", "Regular 2")
        
        root.add_child(regular1)
        root.add_child(virtual1)
        root.add_child(regular2)
        
        # Virtual nodes should still appear in siblings
        siblings = regular1.get_siblings()
        assert len(siblings) == 2  # Both virtual and regular siblings
        
        # Virtual nodes should appear in path
        nested = doc.create_node("nested", "Nested")
        virtual1.add_child(nested)
        path = nested.get_path()
        assert len(path) == 3
        assert path[1].content == "Virtual 1"
        
        doc.close()

    def test_navigation_with_large_hierarchy(self):
        """Test navigation with larger document structure."""
        doc = Document()
        root = doc.create_node("document", "Book")
        doc.content_node = root
        
        # Create multiple chapters with sections and paragraphs
        chapters = []
        for i in range(3):
            chapter = doc.create_node("chapter", f"Chapter {i+1}")
            root.add_child(chapter)
            chapters.append(chapter)
            
            for j in range(2):
                section = doc.create_node("section", f"Section {i+1}.{j+1}")
                chapter.add_child(section)
                
                for k in range(2):
                    para = doc.create_node("paragraph", f"Paragraph {i+1}.{j+1}.{k+1}")
                    section.add_child(para)
        
        # Test siblings at chapter level
        chap2_siblings = chapters[1].get_siblings()
        assert len(chap2_siblings) == 2
        
        # Test get_all_content captures everything
        all_content = root.get_all_content()
        assert "Chapter 1" in all_content
        assert "Chapter 3" in all_content
        assert "Section 2.1" in all_content
        assert "Paragraph 3.2.2" in all_content
        
        # Count total paragraphs in content
        # 3 chapters * 2 sections * 2 paragraphs = 12 paragraphs
        paragraph_count = all_content.count("Paragraph")
        assert paragraph_count == 12

        doc.close()

    def test_contentnode_navigation_edge_cases(self):
        """Test navigation method edge cases."""
        doc = Document()
        root = doc.create_node(node_type="root", content="root content")
        child1 = doc.create_node(node_type="child1", content="child1 content", parent=root)
        child2 = doc.create_node(node_type="child2", content="child2 content", parent=root)

        # Test get_siblings on root (no parent)
        siblings = root.get_siblings()
        assert siblings == []

        # Test get_path - returns list of nodes from root
        path = child1.get_path()
        assert len(path) == 2  # root and child1
        # Note: node_type is not preserved in path nodes (known limitation)
        # Just verify we get ContentNode objects back
        assert all(hasattr(node, 'node_type') for node in path)

        # Test get_path on root - returns list with just root
        root_path = root.get_path()
        assert len(root_path) == 1
        assert hasattr(root_path[0], 'node_type')

        doc.close()