import shutil
import tempfile
from pathlib import Path

from abstra_internals.repositories.code_markers.providers.requirements import (
    RequirementsMarkerProvider,
)
from abstra_internals.repositories.project.project import LocalProjectRepository
from abstra_internals.settings import SettingsController


def setup_test_dir():
    """Set up a temporary test directory with proper settings."""
    path = Path(tempfile.mkdtemp())
    SettingsController.set_root_path(path.as_posix())
    SettingsController.set_public_url("test")
    SettingsController.set_server_port(3000)
    LocalProjectRepository().initialize()
    # Create an empty requirements.txt
    (path / "requirements.txt").write_text("")
    return path


class TestRequirementsMarkerProvider:
    def setup_method(self):
        self.test_dir = setup_test_dir()
        self.provider = RequirementsMarkerProvider()

    def teardown_method(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_name(self):
        assert self.provider.name == "requirements"

    def test_supports_python(self):
        assert self.provider.supports_file_type("python") is True

    def test_does_not_support_json(self):
        assert self.provider.supports_file_type("json") is False

    def test_builtin_import_returns_no_markers(self):
        code = """
import os
import sys
from collections import defaultdict
"""
        markers = self.provider.get_markers(code)
        # Built-in modules should not generate markers
        assert all(
            "os" not in m.message
            and "sys" not in m.message
            and "collections" not in m.message
            for m in markers
        )

    def test_marker_has_correct_structure(self):
        # Use a module that's definitely not installed and not in requirements
        code = "import some_definitely_not_existing_module_xyz123"
        markers = self.provider.get_markers(code)
        if len(markers) > 0:
            marker = markers[0]
            assert hasattr(marker, "line")
            assert hasattr(marker, "column")
            assert hasattr(marker, "until_line")
            assert hasattr(marker, "until_column")
            assert hasattr(marker, "message")
            assert hasattr(marker, "severity")
            assert hasattr(marker, "source")
            assert marker.source == "requirements"
            assert marker.severity == "warning"

    def test_marker_to_dict(self):
        code = "import some_definitely_not_existing_module_xyz123"
        markers = self.provider.get_markers(code)
        if len(markers) > 0:
            marker_dict = markers[0].to_dict()
            assert "line" in marker_dict
            assert "column" in marker_dict
            assert "until_line" in marker_dict
            assert "until_column" in marker_dict
            assert "message" in marker_dict
            assert "severity" in marker_dict
            assert "source" in marker_dict
            assert marker_dict["source"] == "requirements"

    def test_syntax_error_returns_empty_markers(self):
        # If code has syntax errors, requirements checker should return empty
        code = "import ("
        markers = self.provider.get_markers(code)
        assert len(markers) == 0

    def test_missing_requirement_generates_marker(self):
        # Test with a module that definitely doesn't exist
        code = "import nonexistent_module_abc123"
        markers = self.provider.get_markers(code)
        assert len(markers) == 1
        assert markers[0].source == "requirements"
        assert markers[0].severity == "warning"
        assert "nonexistent_module_abc123" in markers[0].message
