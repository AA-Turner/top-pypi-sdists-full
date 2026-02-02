"""
Test pretty print and lines functionality.
"""

import pytest
from kodexa_document import Document


class TestGetLines:
    """Test document get_lines method.

    Note: get_lines() returns ALL nodes in hierarchical order, not just "line" type nodes.
    It's a recursive tree traversal that returns each node with its level, type, and content.
    """

    def test_get_lines_empty_document(self):
        """Test that documents with only auto-root return one line."""
        document = Document(inmemory=True)
        lines = document.get_lines()
        # Documents now have an auto-created root node
        assert len(lines) == 1
        assert lines[0]["nodeType"] == "root"
        assert lines[0]["content"] == ""
        document.close()

    def test_get_lines_returns_all_nodes(self):
        """Test that get_lines returns all nodes, not just 'line' type nodes."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        para = document.create_node("paragraph", content="Some content")
        root.add_child(para)

        lines = document.get_lines()

        # Should return both nodes (root and paragraph)
        assert len(lines) == 2

        # First node is the root (level 0)
        assert lines[0]["nodeType"] == "root"
        assert lines[0]["level"] == 0

        # Second node is the paragraph (level 1)
        assert lines[1]["nodeType"] == "paragraph"
        assert lines[1]["level"] == 1
        assert lines[1]["content"] == "Some content"

        document.close()

    def test_get_lines_with_line_nodes(self):
        """Test document with line nodes returns them along with other nodes."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        line1 = document.create_node("line", content="First line content")
        page.add_child(line1)

        line2 = document.create_node("line", content="Second line content")
        page.add_child(line2)

        lines = document.get_lines()

        # Should have 4 nodes: root, page, line1, line2
        assert len(lines) == 4

        # Check structure of returned line data
        node_types = [l.get("nodeType", "") for l in lines]
        assert "root" in node_types
        assert "page" in node_types
        assert node_types.count("line") == 2

        # Check line content
        line_contents = [l.get("content", "") for l in lines if l.get("nodeType") == "line"]
        assert "First line content" in line_contents
        assert "Second line content" in line_contents

        document.close()

    def test_get_lines_nested_structure(self):
        """Test get_lines with nested page/line structure shows hierarchy."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        # Page 1 with 2 lines
        page1 = document.create_node("page")
        root.add_child(page1)

        line1 = document.create_node("line", content="Page 1 Line 1")
        page1.add_child(line1)

        line2 = document.create_node("line", content="Page 1 Line 2")
        page1.add_child(line2)

        # Page 2 with 1 line
        page2 = document.create_node("page")
        root.add_child(page2)

        line3 = document.create_node("line", content="Page 2 Line 1")
        page2.add_child(line3)

        lines = document.get_lines()

        # Should have 6 nodes: root, page1, line1, line2, page2, line3
        assert len(lines) == 6

        # Verify hierarchy via levels
        levels = [l["level"] for l in lines]
        assert levels[0] == 0  # document
        # Pages are at level 1, lines at level 2

        document.close()

    def test_get_lines_includes_all_fields(self):
        """Test that get_lines returns expected fields."""
        document = Document(inmemory=True)

        # Use auto-created root node and set content
        root = document.content_node
        root.content = "Root content"

        lines = document.get_lines()
        assert len(lines) == 1

        line = lines[0]
        # Check all expected fields
        assert "id" in line
        assert "level" in line
        assert "typeId" in line
        assert "nodeType" in line
        assert "content" in line

        assert line["nodeType"] == "root"
        assert line["content"] == "Root content"
        assert line["level"] == 0

        document.close()

    def test_get_lines_after_document_close(self):
        """Test that get_lines raises error on closed document."""
        document = Document(inmemory=True)
        document.close()

        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.get_lines()


class TestPrettyPrint:
    """Test document pretty print methods."""

    def test_get_pretty_page_empty_document(self):
        """Test get_pretty_page on document with no pages raises error."""
        from kodexa_document.errors import DocumentError

        document = Document(inmemory=True)

        # Document has auto-root but no page children, so page index 0 is out of range
        with pytest.raises(DocumentError, match="out of range"):
            document.get_pretty_page(0)

        document.close()

    def test_get_pretty_pages_empty_document(self):
        """Test get_pretty_pages on empty document returns empty string."""
        document = Document(inmemory=True)

        result = document.get_pretty_pages()
        assert result == ""

        document.close()

    def test_get_pretty_page_single_page(self):
        """Test get_pretty_page on a document with one page."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        line = document.create_node("line", content="Test line")
        page.add_child(line)

        word = document.create_node("word", content="Hello")
        line.add_child(word)

        # Get pretty page - may or may not have content depending on bbox
        result = document.get_pretty_page(0)
        # Result is a string (may be empty if no bboxes)
        assert isinstance(result, str)

        document.close()

    def test_get_pretty_pages_multiple_pages(self):
        """Test get_pretty_pages with multiple pages."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        # Create 3 pages
        for i in range(3):
            page = document.create_node("page")
            root.add_child(page)

            line = document.create_node("line", content=f"Line on page {i+1}")
            page.add_child(line)

        result = document.get_pretty_pages()
        assert isinstance(result, str)

        document.close()

    def test_get_pretty_page_invalid_index_raises_error(self):
        """Test get_pretty_page with invalid page index raises error."""
        from kodexa_document.errors import DocumentError

        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        # Invalid index (only page 0 exists) - should raise error
        with pytest.raises(DocumentError, match="out of range"):
            document.get_pretty_page(99)

        document.close()

    def test_get_pretty_page_negative_index_raises_error(self):
        """Test get_pretty_page with negative index raises error."""
        from kodexa_document.errors import DocumentError

        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        # Negative index should raise error
        with pytest.raises(DocumentError, match="out of range"):
            document.get_pretty_page(-1)

        document.close()

    def test_get_pretty_page_with_words_and_bbox(self):
        """Test get_pretty_page with words that have bounding boxes."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        line = document.create_node("line")
        page.add_child(line)

        # Create words with content
        word1 = document.create_node("word", content="Hello")
        line.add_child(word1)

        word2 = document.create_node("word", content="World")
        line.add_child(word2)

        # Set bounding boxes on words
        word1.set_bbox([0, 0, 50, 20])
        word2.set_bbox([60, 0, 110, 20])

        result = document.get_pretty_page(0)
        assert isinstance(result, str)
        # Output should have content (line info at minimum)
        assert len(result) > 0

        document.close()

    def test_get_pretty_pages_with_words_and_bbox(self):
        """Test get_pretty_pages with words that have bounding boxes."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        # Create two pages
        for page_num in range(2):
            page = document.create_node("page")
            root.add_child(page)

            line = document.create_node("line")
            page.add_child(line)

            word = document.create_node("word", content=f"Page{page_num+1}")
            line.add_child(word)
            word.set_bbox([0, 0, 50, 20])

        result = document.get_pretty_pages()
        assert isinstance(result, str)

        # Should contain page separators and content
        assert len(result) > 0
        assert "Page 1" in result or "Page1" in result
        assert "Page 2" in result or "Page2" in result

        document.close()

    def test_get_pretty_page_after_document_close(self):
        """Test that get_pretty_page raises error on closed document."""
        document = Document(inmemory=True)
        document.close()

        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.get_pretty_page(0)

    def test_get_pretty_pages_after_document_close(self):
        """Test that get_pretty_pages raises error on closed document."""
        document = Document(inmemory=True)
        document.close()

        with pytest.raises(RuntimeError, match="Document has been closed"):
            document.get_pretty_pages()

    def test_pretty_print_returns_string_with_content(self):
        """Test that pretty print returns a string with content for valid pages."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        line = document.create_node("line")
        page.add_child(line)

        # Create words with specific horizontal positions
        word_left = document.create_node("word", content="Left")
        line.add_child(word_left)
        word_left.set_bbox([10, 0, 50, 20])

        word_right = document.create_node("word", content="Right")
        line.add_child(word_right)
        word_right.set_bbox([200, 0, 250, 20])

        result = document.get_pretty_page(0)

        # Should return a string with some content (at least line info)
        assert isinstance(result, str)
        assert len(result) > 0

        document.close()


class TestPrettyPrintIntegration:
    """Integration tests for pretty print with more complex documents."""

    def test_multiline_page(self):
        """Test pretty printing a page with multiple lines."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        # Create multiple lines with words
        for i in range(3):
            line = document.create_node("line")
            page.add_child(line)

            for j in range(2):
                word = document.create_node("word", content=f"L{i}W{j}")
                line.add_child(word)
                word.set_bbox([j * 60, i * 25, j * 60 + 50, i * 25 + 20])

        result = document.get_pretty_page(0)
        assert isinstance(result, str)

        # Should have content for each line (line info at minimum)
        # Count newlines - should have at least 3 lines worth of content
        assert result.count("\n") >= 3

        document.close()

    def test_lines_and_pretty_print_consistency(self):
        """Test that get_lines and pretty print work on same document."""
        document = Document(inmemory=True)

        # Use auto-created root node
        root = document.content_node

        page = document.create_node("page")
        root.add_child(page)

        for i in range(5):
            line = document.create_node("line", content=f"Line {i+1}")
            page.add_child(line)

            word = document.create_node("word", content=f"Word{i+1}")
            line.add_child(word)
            word.set_bbox([0, i * 25, 50, i * 25 + 20])

        # Both methods should work on the same document
        lines = document.get_lines()
        pretty = document.get_pretty_page(0)

        # get_lines returns all nodes: root + page + 5 lines + 5 words = 12
        assert len(lines) == 12
        assert isinstance(pretty, str)
        assert len(pretty) > 0

        document.close()
