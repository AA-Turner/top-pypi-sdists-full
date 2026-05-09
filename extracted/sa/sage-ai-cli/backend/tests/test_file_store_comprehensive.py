"""Comprehensive tests for backend/file_store.py."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


class TestFileStoreConstants:
    """Tests for file store constants."""

    def test_max_file_size(self):
        """MAX_FILE_SIZE is defined."""
        from backend.file_store import MAX_FILE_SIZE

        assert MAX_FILE_SIZE == 10 * 1024 * 1024  # 10MB

    def test_text_mime_types(self):
        """TEXT_MIME_TYPES contains expected types."""
        from backend.file_store import TEXT_MIME_TYPES

        assert "text/plain" in TEXT_MIME_TYPES
        assert "text/html" in TEXT_MIME_TYPES
        assert "application/json" in TEXT_MIME_TYPES

    def test_preview_length(self):
        """PREVIEW_LENGTH is defined."""
        from backend.file_store import PREVIEW_LENGTH

        assert PREVIEW_LENGTH == 500


class TestFileStoreInit:
    """Tests for FileStore initialization."""

    def test_create_with_default_path(self):
        """Create with default path."""
        from backend.file_store import FileStore

        store = FileStore()
        assert store.base_dir is not None

    def test_create_with_custom_path(self, tmp_path):
        """Create with custom path."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path / "files")
        assert store.base_dir == tmp_path / "files"
        assert store.base_dir.exists()

    def test_creates_directories(self, tmp_path):
        """Creates required directories."""
        from backend.file_store import FileStore

        base = tmp_path / "test_store"
        store = FileStore(base_dir=base)

        assert store.metadata_dir.exists()
        assert store.content_dir.exists()


class TestFileStoreSave:
    """Tests for FileStore.save method."""

    def test_save_file(self, tmp_path):
        """Save a file successfully."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Hello, World!"
        file_id = store.save(content, "test.txt", "text/plain")

        assert file_id is not None
        assert len(file_id) > 0

    def test_save_file_custom_id(self, tmp_path):
        """Save file with custom ID."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Test content"
        file_id = store.save(content, "test.txt", "text/plain", file_id="custom-id")

        assert file_id == "custom-id"

    def test_save_empty_file_raises(self, tmp_path):
        """Empty content raises ValueError."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        with pytest.raises(ValueError, match="empty"):
            store.save(b"", "empty.txt", "text/plain")

    def test_save_too_large_raises(self, tmp_path):
        """File exceeding size limit raises ValueError."""
        from backend.file_store import FileStore, MAX_FILE_SIZE

        store = FileStore(base_dir=tmp_path)
        content = b"x" * (MAX_FILE_SIZE + 1)

        with pytest.raises(ValueError, match="exceeds maximum size"):
            store.save(content, "large.txt", "text/plain")

    def test_save_creates_content_file(self, tmp_path):
        """Save creates content file."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Test content"
        file_id = store.save(content, "test.txt", "text/plain")

        content_path = store._content_path(file_id)
        assert content_path.exists()
        assert content_path.read_bytes() == content

    def test_save_creates_metadata_file(self, tmp_path):
        """Save creates metadata file."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Test content"
        file_id = store.save(content, "test.txt", "text/plain")

        metadata_path = store._metadata_path(file_id)
        assert metadata_path.exists()

        metadata = json.loads(metadata_path.read_text())
        assert metadata["file_id"] == file_id
        assert metadata["filename"] == "test.txt"
        assert metadata["mime_type"] == "text/plain"
        assert metadata["size_bytes"] == len(content)

    def test_save_generates_preview_for_text(self, tmp_path):
        """Save generates preview for text files."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Hello, this is preview text"
        file_id = store.save(content, "test.txt", "text/plain")

        metadata_path = store._metadata_path(file_id)
        metadata = json.loads(metadata_path.read_text())
        assert metadata["content_preview"] == "Hello, this is preview text"

    def test_save_no_preview_for_binary(self, tmp_path):
        """No preview for binary files."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"\x00\x01\x02\x03"
        file_id = store.save(content, "binary.bin", "application/octet-stream")

        metadata_path = store._metadata_path(file_id)
        metadata = json.loads(metadata_path.read_text())
        assert metadata["content_preview"] is None


class TestFileStoreGet:
    """Tests for FileStore.get method."""

    def test_get_file(self, tmp_path):
        """Get saved file."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Test content"
        file_id = store.save(content, "test.txt", "text/plain")

        result = store.get(file_id)
        assert result["content"] == content
        assert result["filename"] == "test.txt"
        assert result["mime_type"] == "text/plain"
        assert result["size_bytes"] == len(content)

    def test_get_nonexistent_raises(self, tmp_path):
        """Get non-existent file raises KeyError."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        with pytest.raises(KeyError, match="not found"):
            store.get("nonexistent-id")

    def test_get_corrupt_metadata_raises(self, tmp_path):
        """Get with corrupt metadata raises KeyError."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        # Create content file but corrupt metadata
        file_id = "test-id"
        content_path = store._content_path(file_id)
        content_path.write_bytes(b"test")
        metadata_path = store._metadata_path(file_id)
        metadata_path.write_text("invalid json")

        with pytest.raises(KeyError, match="corrupted"):
            store.get(file_id)


class TestFileStoreGetMetadata:
    """Tests for FileStore.get_metadata method."""

    def test_get_metadata(self, tmp_path):
        """Get file metadata."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Test content"
        file_id = store.save(content, "test.txt", "text/plain")

        metadata = store.get_metadata(file_id)
        assert metadata["file_id"] == file_id
        assert metadata["filename"] == "test.txt"
        assert metadata["mime_type"] == "text/plain"

    def test_get_metadata_nonexistent_raises(self, tmp_path):
        """Get metadata for non-existent file raises KeyError."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        with pytest.raises(KeyError, match="not found"):
            store.get_metadata("nonexistent-id")

    def test_get_metadata_corrupt_raises(self, tmp_path):
        """Get corrupt metadata raises KeyError."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        file_id = "test-id"
        metadata_path = store._metadata_path(file_id)
        metadata_path.write_text("{invalid json")

        with pytest.raises(KeyError, match="corrupted"):
            store.get_metadata(file_id)


class TestFileStoreDelete:
    """Tests for FileStore.delete method."""

    def test_delete_file(self, tmp_path):
        """Delete file removes both content and metadata."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Test content"
        file_id = store.save(content, "test.txt", "text/plain")

        content_path = store._content_path(file_id)
        metadata_path = store._metadata_path(file_id)

        assert content_path.exists()
        assert metadata_path.exists()

        store.delete(file_id)

        assert not content_path.exists()
        assert not metadata_path.exists()

    def test_delete_nonexistent_no_error(self, tmp_path):
        """Delete non-existent file doesn't raise."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        # Should not raise
        store.delete("nonexistent-id")


class TestFileStoreListAll:
    """Tests for FileStore.list_all method."""

    def test_list_empty(self, tmp_path):
        """List empty store."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        files = store.list_all()
        assert files == []

    def test_list_files(self, tmp_path):
        """List saved files."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        store.save(b"Content 1", "file1.txt", "text/plain")
        store.save(b"Content 2", "file2.txt", "text/plain")

        files = store.list_all()
        assert len(files) == 2

        filenames = [f["filename"] for f in files]
        assert "file1.txt" in filenames
        assert "file2.txt" in filenames

    def test_list_skips_corrupt_metadata(self, tmp_path):
        """List skips files with corrupt metadata."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        store.save(b"Good content", "good.txt", "text/plain")

        # Create corrupt metadata
        corrupt_path = store.metadata_dir / "corrupt.json"
        corrupt_path.write_text("invalid json")

        files = store.list_all()
        assert len(files) == 1
        assert files[0]["filename"] == "good.txt"


class TestFileStoreGetContentForChat:
    """Tests for FileStore.get_content_for_chat method."""

    def test_text_file_formatted(self, tmp_path):
        """Text file is formatted for chat."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"print('Hello')"
        file_id = store.save(content, "script.py", "text/x-python")

        chat_content = store.get_content_for_chat(file_id)
        assert "[File: script.py]" in chat_content
        assert "print('Hello')" in chat_content
        assert "```" in chat_content

    def test_binary_file_indicator(self, tmp_path):
        """Binary file shows indicator."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"\x00\x01\x02\x03"
        file_id = store.save(content, "data.bin", "application/octet-stream")

        chat_content = store.get_content_for_chat(file_id)
        assert "[Binary file: data.bin" in chat_content
        assert "4 bytes" in chat_content

    def test_nonexistent_file_raises(self, tmp_path):
        """Non-existent file raises KeyError."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)

        with pytest.raises(KeyError):
            store.get_content_for_chat("nonexistent")


class TestFileStoreSanitizeFilename:
    """Tests for filename sanitization."""

    def test_simple_filename(self, tmp_path):
        """Simple filename unchanged."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        result = store._sanitize_filename("test.txt")
        assert result == "test.txt"

    def test_removes_path_components(self, tmp_path):
        """Removes path components."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        result = store._sanitize_filename("/path/to/test.txt")
        assert result == "test.txt"

    def test_removes_parent_directory(self, tmp_path):
        """Removes parent directory traversal."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        result = store._sanitize_filename("../../../etc/passwd")
        assert ".." not in result
        assert "/" not in result

    def test_empty_becomes_unnamed(self, tmp_path):
        """Empty filename becomes 'unnamed'."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        result = store._sanitize_filename("")
        assert result == "unnamed"


class TestFileStoreIsTextType:
    """Tests for _is_text_type method."""

    def test_text_plain(self, tmp_path):
        """text/plain is text type."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        assert store._is_text_type("text/plain") is True

    def test_text_html(self, tmp_path):
        """text/html is text type."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        assert store._is_text_type("text/html") is True

    def test_application_json(self, tmp_path):
        """application/json is text type."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        assert store._is_text_type("application/json") is True

    def test_binary_type(self, tmp_path):
        """application/octet-stream is not text type."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        assert store._is_text_type("application/octet-stream") is False

    def test_text_prefix(self, tmp_path):
        """Any text/* is text type."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        assert store._is_text_type("text/custom") is True


class TestFileStoreGeneratePreview:
    """Tests for _generate_preview method."""

    def test_short_text_full_preview(self, tmp_path):
        """Short text gets full preview."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        content = b"Short text"
        preview = store._generate_preview(content, "text/plain")
        assert preview == "Short text"

    def test_long_text_truncated(self, tmp_path):
        """Long text is truncated."""
        from backend.file_store import FileStore, PREVIEW_LENGTH

        store = FileStore(base_dir=tmp_path)
        content = b"x" * (PREVIEW_LENGTH + 100)
        preview = store._generate_preview(content, "text/plain")

        assert len(preview) == PREVIEW_LENGTH + 3  # +3 for "..."
        assert preview.endswith("...")

    def test_binary_no_preview(self, tmp_path):
        """Binary content returns None."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        preview = store._generate_preview(b"\x00\x01", "application/octet-stream")
        assert preview is None

    def test_invalid_utf8_no_preview(self, tmp_path):
        """Invalid UTF-8 returns None."""
        from backend.file_store import FileStore

        store = FileStore(base_dir=tmp_path)
        invalid_utf8 = b"\xff\xfe"
        preview = store._generate_preview(invalid_utf8, "text/plain")
        assert preview is None


class TestGlobalFileStore:
    """Tests for global file_store instance."""

    def test_global_instance_exists(self):
        """Global file_store instance exists."""
        from backend.file_store import file_store

        assert file_store is not None

    def test_global_instance_is_filestore(self):
        """Global instance is FileStore."""
        from backend.file_store import file_store, FileStore

        assert isinstance(file_store, FileStore)
