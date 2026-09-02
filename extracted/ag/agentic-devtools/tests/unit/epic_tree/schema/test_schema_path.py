"""Tests for SCHEMA_PATH constant."""

from pathlib import Path

from agentic_devtools.epic_tree.schema import SCHEMA_PATH


class TestSchemaPath:
    """Tests for the SCHEMA_PATH constant."""

    def test_is_path_object(self):
        """SCHEMA_PATH is a Path instance."""
        assert isinstance(SCHEMA_PATH, Path)

    def test_points_to_existing_file(self):
        """SCHEMA_PATH points to a file that exists on disk."""
        assert SCHEMA_PATH.exists()
        assert SCHEMA_PATH.is_file()

    def test_file_has_json_extension(self):
        """Schema file has a .json extension."""
        assert SCHEMA_PATH.suffix == ".json"

    def test_file_is_under_schemas_directory(self):
        """Schema file is located under the schemas/ directory."""
        assert "schemas" in SCHEMA_PATH.parts

    def test_file_name(self):
        """Schema file is named epic-tree.schema.json."""
        assert SCHEMA_PATH.name == "epic-tree.schema.json"
