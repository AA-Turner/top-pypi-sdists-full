import shutil
import tempfile
from pathlib import Path
from typing import Optional

import pytest

from abstra_internals.repositories.code_markers.models import CodeMarker
from abstra_internals.repositories.code_markers.providers.base import CodeMarkerProvider
from abstra_internals.repositories.code_markers.repository import (
    LocalCodeMarkersRepository,
    ProductionCodeMarkersRepository,
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


class MockProvider(CodeMarkerProvider):
    def __init__(
        self, name: str, markers: list, supported_types: Optional[list] = None
    ):
        self._name = name
        self._markers = markers
        self._supported_types = supported_types or ["python"]

    @property
    def name(self) -> str:
        return self._name

    def get_markers(self, code: str) -> list:
        return self._markers

    def supports_file_type(self, file_type: str) -> bool:
        return file_type in self._supported_types


class TestLocalCodeMarkersRepository:
    def setup_method(self):
        self.test_dir = setup_test_dir()

    def teardown_method(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_markers_aggregates_from_all_providers(self):
        repo = LocalCodeMarkersRepository()

        # Test with valid Python code - should return empty or some markers
        markers = repo.get_markers("x = 1")
        assert isinstance(markers, list)

    def test_get_markers_returns_empty_for_valid_code(self):
        repo = LocalCodeMarkersRepository()
        code = """
def hello():
    print("Hello")
"""
        markers = repo.get_markers(code)
        # Valid code should return no syntax errors
        # Requirements markers depend on what's in requirements.txt
        syntax_markers = [m for m in markers if m.source == "syntax"]
        assert len(syntax_markers) == 0

    def test_get_markers_returns_syntax_errors(self):
        repo = LocalCodeMarkersRepository()
        code = "if True"  # Missing colon
        markers = repo.get_markers(code)
        syntax_markers = [m for m in markers if m.source == "syntax"]
        assert len(syntax_markers) > 0

    def test_register_provider(self):
        repo = LocalCodeMarkersRepository()
        initial_count = len(repo._providers)

        mock_marker = CodeMarker(
            line=1,
            column=1,
            until_line=1,
            until_column=5,
            message="Test marker",
            severity="info",
            source="test",
        )
        mock_provider = MockProvider("test", [mock_marker])
        repo.register_provider(mock_provider)

        assert len(repo._providers) == initial_count + 1

        markers = repo.get_markers("x = 1")
        test_markers = [m for m in markers if m.source == "test"]
        assert len(test_markers) == 1

    def test_filters_by_file_type(self):
        repo = LocalCodeMarkersRepository()

        # Clear existing providers
        repo._providers = []

        python_marker = CodeMarker(
            line=1,
            column=1,
            until_line=1,
            until_column=5,
            message="Python marker",
            severity="info",
            source="python_provider",
        )
        json_marker = CodeMarker(
            line=1,
            column=1,
            until_line=1,
            until_column=5,
            message="JSON marker",
            severity="info",
            source="json_provider",
        )

        repo.register_provider(
            MockProvider("python_provider", [python_marker], ["python"])
        )
        repo.register_provider(MockProvider("json_provider", [json_marker], ["json"]))

        python_markers = repo.get_markers("x = 1", file_type="python")
        assert len(python_markers) == 1
        assert python_markers[0].source == "python_provider"

        json_markers = repo.get_markers("{}", file_type="json")
        assert len(json_markers) == 1
        assert json_markers[0].source == "json_provider"


class TestProductionCodeMarkersRepository:
    def test_get_markers_raises_not_implemented(self):
        repo = ProductionCodeMarkersRepository()
        with pytest.raises(NotImplementedError):
            repo.get_markers("x = 1")
