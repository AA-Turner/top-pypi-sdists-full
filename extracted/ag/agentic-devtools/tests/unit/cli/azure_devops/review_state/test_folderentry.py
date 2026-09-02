"""Tests for FolderEntry backward-compatible alias.

FolderEntry is now an alias for FolderGroup. These tests verify the alias works.
"""

from agentic_devtools.cli.azure_devops.review_state import FolderEntry, FolderGroup


class TestFolderEntry:
    """Tests for FolderEntry (alias for FolderGroup)."""

    def test_folder_entry_is_folder_group(self):
        """Test that FolderEntry is an alias for FolderGroup."""
        assert FolderEntry is FolderGroup

    def test_creation_with_defaults(self):
        """Test creation with default files list."""
        f = FolderEntry()
        assert f.files == []

    def test_creation_with_files(self):
        """Test creation with explicit files list."""
        files = ["/mgmt-backend/SomeFile.cs", "/mgmt-backend/OtherFile.cs"]
        f = FolderEntry(files=files)
        assert f.files == files

    def test_to_dict(self):
        """Test serialization to dictionary."""
        files = ["/mgmt-backend/SomeFile.cs"]
        f = FolderEntry(files=files)
        d = f.to_dict()
        assert d == {
            "files": ["/mgmt-backend/SomeFile.cs"],
        }

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "files": ["/mgmt-backend/SomeFile.cs"],
        }
        f = FolderEntry.from_dict(data)
        assert f.files == ["/mgmt-backend/SomeFile.cs"]

    def test_from_dict_defaults(self):
        """Test from_dict with missing optional fields uses defaults."""
        data = {}
        f = FolderEntry.from_dict(data)
        assert f.files == []

    def test_roundtrip(self):
        """Test to_dict/from_dict round-trips correctly."""
        original = FolderEntry(files=["/a/b.py", "/a/c.py"])
        restored = FolderEntry.from_dict(original.to_dict())
        assert restored.files == ["/a/b.py", "/a/c.py"]

    def test_files_default_is_independent(self):
        """Test that default files lists are independent per instance."""
        f1 = FolderEntry()
        f2 = FolderEntry()
        f1.files.append("/some/file.cs")
        assert f2.files == []

    def test_from_dict_normalizes_file_paths(self):
        """Test that from_dict normalizes file paths with leading slash."""
        data = {
            "files": ["mgmt-backend/SomeFile.cs", "/mgmt-backend/OtherFile.cs"],
        }
        f = FolderEntry.from_dict(data)
        assert f.files == ["/mgmt-backend/SomeFile.cs", "/mgmt-backend/OtherFile.cs"]
