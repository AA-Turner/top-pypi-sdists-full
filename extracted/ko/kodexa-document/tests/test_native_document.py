"""
Test native document functionality for storing binary documents (PDF, Excel, Word, etc.).
"""

import pytest
from kodexa_document import Document


class TestNativeDocument:
    """Test native document methods."""

    def test_create_and_get_native_document(self):
        """Test creating and retrieving a native document."""
        document = Document(inmemory=True)

        # Create a native document
        test_data = b"This is test PDF content"
        doc_id = document.create_native_document(
            filename="test.pdf",
            mime_type="application/pdf",
            data=test_data,
            checksum="sha256:abc123"
        )

        assert doc_id > 0, "Should return a valid document ID"

        # Get by ID
        retrieved = document.get_native_document_by_id(doc_id)
        assert retrieved is not None
        assert retrieved["id"] == doc_id
        assert retrieved["filename"] == "test.pdf"
        assert retrieved["mime_type"] == "application/pdf"
        assert retrieved["size"] == len(test_data)
        assert retrieved["checksum"] == "sha256:abc123"

        # Get data separately
        data = document.get_native_document_data(doc_id)
        assert data == test_data

        document.close()

    def test_create_native_document_without_checksum(self):
        """Test creating a native document without a checksum."""
        document = Document(inmemory=True)

        test_data = b"Excel content here"
        doc_id = document.create_native_document(
            filename="spreadsheet.xlsx",
            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            data=test_data
        )

        assert doc_id > 0

        retrieved = document.get_native_document_by_id(doc_id)
        assert retrieved["filename"] == "spreadsheet.xlsx"
        # Checksum may be None or empty string
        assert retrieved["checksum"] in (None, "")

        document.close()

    def test_get_native_document_by_filename(self):
        """Test getting a native document by filename."""
        document = Document(inmemory=True)

        test_data = b"Word document content"
        doc_id = document.create_native_document(
            filename="document.docx",
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            data=test_data
        )

        # Get by filename
        retrieved = document.get_native_document_by_filename("document.docx")
        assert retrieved is not None
        assert retrieved["id"] == doc_id
        assert retrieved["filename"] == "document.docx"

        # Non-existent filename should return None
        non_existent = document.get_native_document_by_filename("nonexistent.pdf")
        assert non_existent is None

        document.close()

    def test_get_first_native_document(self):
        """Test getting the first native document."""
        document = Document(inmemory=True)

        # First should be None when empty
        first = document.get_first_native_document()
        assert first is None

        # Create some documents
        doc_id1 = document.create_native_document("first.pdf", "application/pdf", b"first")
        document.create_native_document("second.pdf", "application/pdf", b"second")

        # First should return the first one
        first = document.get_first_native_document()
        assert first is not None
        assert first["id"] == doc_id1
        assert first["filename"] == "first.pdf"

        document.close()

    def test_get_native_documents(self):
        """Test getting all native documents."""
        document = Document(inmemory=True)

        # Initially empty
        docs = document.get_native_documents()
        assert docs == []

        # Create multiple documents
        document.create_native_document("doc1.pdf", "application/pdf", b"content1")
        document.create_native_document("doc2.xlsx", "application/vnd.ms-excel", b"content2")
        document.create_native_document("doc3.html", "text/html", b"<html>content3</html>")

        # Get all
        docs = document.get_native_documents()
        assert len(docs) == 3

        filenames = [d["filename"] for d in docs]
        assert "doc1.pdf" in filenames
        assert "doc2.xlsx" in filenames
        assert "doc3.html" in filenames

        document.close()

    def test_delete_native_document(self):
        """Test deleting a native document."""
        document = Document(inmemory=True)

        # Create a document
        doc_id = document.create_native_document("deleteme.txt", "text/plain", b"delete me")

        # Verify it exists
        assert document.get_native_document_by_id(doc_id) is not None

        # Delete it
        result = document.delete_native_document(doc_id)
        assert result is True

        # Verify it's gone
        assert document.get_native_document_by_id(doc_id) is None

        document.close()

    def test_delete_all_native_documents(self):
        """Test deleting all native documents."""
        document = Document(inmemory=True)

        # Create multiple documents
        for i in range(5):
            document.create_native_document(f"doc{i}.txt", "text/plain", f"content{i}".encode())

        # Verify they exist
        assert len(document.get_native_documents()) == 5

        # Delete all
        result = document.delete_all_native_documents()
        assert result is True

        # Verify all gone
        assert len(document.get_native_documents()) == 0

        document.close()

    def test_binary_data_integrity(self):
        """Test that binary data is preserved correctly."""
        document = Document(inmemory=True)

        # Create data with all possible byte values (0-255)
        test_data = bytes(range(256))

        doc_id = document.create_native_document(
            filename="binary.bin",
            mime_type="application/octet-stream",
            data=test_data
        )

        # Retrieve and verify
        retrieved_data = document.get_native_document_data(doc_id)
        assert retrieved_data == test_data
        assert len(retrieved_data) == 256

        # Verify each byte
        for i in range(256):
            assert retrieved_data[i] == i

        document.close()

    def test_large_binary_data(self):
        """Test storing large binary data (1MB)."""
        document = Document(inmemory=True)

        # Create 1MB of test data
        test_data = bytes([i % 256 for i in range(1024 * 1024)])

        doc_id = document.create_native_document(
            filename="large.bin",
            mime_type="application/octet-stream",
            data=test_data
        )

        # Retrieve and verify
        retrieved_data = document.get_native_document_data(doc_id)
        assert len(retrieved_data) == len(test_data)
        assert retrieved_data == test_data

        # Verify metadata
        doc_info = document.get_native_document_by_id(doc_id)
        assert doc_info["size"] == len(test_data)

        document.close()

    def test_common_mime_types(self):
        """Test storing documents with common MIME types."""
        document = Document(inmemory=True)

        mime_types = [
            ("document.pdf", "application/pdf"),
            ("spreadsheet.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("page.html", "text/html"),
            ("data.json", "application/json"),
            ("image.png", "image/png"),
            ("image.jpeg", "image/jpeg"),
            ("archive.zip", "application/zip"),
            ("plain.txt", "text/plain"),
            ("data.csv", "text/csv"),
        ]

        for filename, mime_type in mime_types:
            doc_id = document.create_native_document(filename, mime_type, b"test content")
            assert doc_id > 0, f"Failed to create document with MIME type {mime_type}"

            retrieved = document.get_native_document_by_filename(filename)
            assert retrieved is not None
            assert retrieved["mime_type"] == mime_type

        document.close()

    def test_special_filenames(self):
        """Test storing documents with special characters in filenames."""
        document = Document(inmemory=True)

        filenames = [
            "simple.pdf",
            "file with spaces.pdf",
            "file-with-dashes.pdf",
            "file_with_underscores.pdf",
            "file.multiple.dots.pdf",
            "UPPERCASE.PDF",
            "MixedCase.Pdf",
        ]

        for filename in filenames:
            doc_id = document.create_native_document(filename, "application/pdf", b"test")
            assert doc_id > 0, f"Failed to create document with filename '{filename}'"

            retrieved = document.get_native_document_by_filename(filename)
            assert retrieved is not None, f"Failed to retrieve document with filename '{filename}'"
            assert retrieved["filename"] == filename

        document.close()

    def test_unicode_filenames(self):
        """Test storing documents with Unicode filenames."""
        document = Document(inmemory=True)

        unicode_filenames = [
            "日本語ファイル.pdf",
            "файл.pdf",
            "αρχείο.pdf",
            "文件.pdf",
        ]

        for filename in unicode_filenames:
            doc_id = document.create_native_document(filename, "application/pdf", b"test")
            assert doc_id > 0, f"Failed to create document with filename '{filename}'"

            retrieved = document.get_native_document_by_filename(filename)
            assert retrieved is not None, f"Failed to retrieve document with filename '{filename}'"
            assert retrieved["filename"] == filename

        document.close()

    def test_get_nonexistent_document(self):
        """Test getting a non-existent document."""
        document = Document(inmemory=True)

        # Get by non-existent ID
        result = document.get_native_document_by_id(99999)
        assert result is None

        # Get data for non-existent ID
        data = document.get_native_document_data(99999)
        assert data is None

        document.close()

    def test_empty_document_list(self):
        """Test operations on empty document list."""
        document = Document(inmemory=True)

        # All operations should work on empty list
        docs = document.get_native_documents()
        assert docs == []

        first = document.get_first_native_document()
        assert first is None

        by_filename = document.get_native_document_by_filename("nonexistent.pdf")
        assert by_filename is None

        # Delete all on empty should succeed
        result = document.delete_all_native_documents()
        assert result is True

        document.close()

    def test_multiple_documents_same_type(self):
        """Test storing multiple documents of the same type."""
        document = Document(inmemory=True)

        # Create multiple PDFs
        for i in range(10):
            doc_id = document.create_native_document(
                f"document_{i}.pdf",
                "application/pdf",
                f"PDF content {i}".encode()
            )
            assert doc_id > 0

        # Verify all 10 exist
        docs = document.get_native_documents()
        assert len(docs) == 10

        # Verify each can be retrieved
        for i in range(10):
            retrieved = document.get_native_document_by_filename(f"document_{i}.pdf")
            assert retrieved is not None
            data = document.get_native_document_data(retrieved["id"])
            assert data == f"PDF content {i}".encode()

        document.close()
