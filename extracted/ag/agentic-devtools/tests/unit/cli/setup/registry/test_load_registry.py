"""Tests for load_registry."""

from pathlib import Path

import pytest

from agentic_devtools.cli.setup import registry
from agentic_devtools.cli.setup.registry import RegistryData, RegistryError, load_registry, save_registry


class TestLoadRegistry:
    """Tests for load_registry."""

    def test_returns_empty_registry_when_file_missing(self, tmp_path: Path) -> None:
        """A missing registry file yields an empty RegistryData."""
        assert load_registry(tmp_path / "registry.json") == RegistryData()

    def test_round_trips_a_saved_registry(self, tmp_path: Path) -> None:
        """A registry saved with save_registry loads back equal."""
        path = tmp_path / "registry.json"
        data = RegistryData()
        save_registry(data, path)
        assert load_registry(path) == data

    def test_raises_on_corrupt_json(self, tmp_path: Path) -> None:
        """Invalid JSON raises RegistryError."""
        path = tmp_path / "registry.json"
        path.write_text("{ not valid json", encoding="utf-8")
        with pytest.raises(RegistryError, match="Could not read registry"):
            load_registry(path)

    def test_raises_on_os_error(self, tmp_path: Path) -> None:
        """An unreadable path (a directory) raises RegistryError."""
        path = tmp_path / "registry.json"
        path.mkdir()  # reading a directory as text raises OSError
        with pytest.raises(RegistryError, match="Could not read registry"):
            load_registry(path)

    def test_uses_default_path_when_omitted(self, tmp_path: Path, monkeypatch) -> None:
        """When registry_path is omitted, get_registry_path is consulted."""
        default_path = tmp_path / "default" / "registry.json"
        monkeypatch.setattr(registry, "get_registry_path", lambda: default_path)
        assert load_registry() == RegistryData()
