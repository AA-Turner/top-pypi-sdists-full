"""
Test get_source() utility function for accessing native document data.
"""

import io
import pytest
from kodexa_document import Document, get_source


class TestGetSource:
    """Test get_source() function."""

    def test_get_source_with_native_document(self):
        """Test get_source returns BytesIO with native document data."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        # Add a native document using the correct API
        test_content = b"Hello, this is test PDF content"
        doc.create_native_document("test.pdf", "application/pdf", test_content)

        # Get source
        source = get_source(doc)

        # Verify it's a BytesIO with correct content
        assert isinstance(source, io.BytesIO)
        assert source.read() == test_content

        doc.close()

    def test_get_source_no_native_document(self):
        """Test get_source raises ValueError when no native document exists."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        with pytest.raises(ValueError, match="No native document found"):
            get_source(doc)

        doc.close()

    def test_get_source_returns_first_native_document(self):
        """Test get_source returns the first native document when multiple exist."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        # Add multiple native documents
        first_content = b"First document content"
        second_content = b"Second document content"
        doc.create_native_document("first.pdf", "application/pdf", first_content)
        doc.create_native_document("second.pdf", "application/pdf", second_content)

        # Should return first
        source = get_source(doc)
        assert source.read() == first_content

        doc.close()

    def test_get_source_seekable(self):
        """Test that returned BytesIO is seekable."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        test_content = b"Seekable content test"
        doc.create_native_document("test.txt", "text/plain", test_content)

        source = get_source(doc)

        # Read partial content
        partial = source.read(8)
        assert partial == b"Seekable"

        # Seek back and read again
        source.seek(0)
        full = source.read()
        assert full == test_content

        doc.close()

    def test_get_source_persists_through_serialization(self):
        """Test get_source works after document serialization."""
        doc = Document(inmemory=True)
        root = doc.create_node("document")
        doc.content_node = root

        test_content = b"Persistent PDF content"
        doc.create_native_document("test.pdf", "application/pdf", test_content)

        # Serialize and deserialize
        kddb_bytes = doc.to_kddb()
        doc.close()

        doc2 = Document.from_kddb(kddb_bytes)

        # Get source from reloaded document
        source = get_source(doc2)
        assert source.read() == test_content

        doc2.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
