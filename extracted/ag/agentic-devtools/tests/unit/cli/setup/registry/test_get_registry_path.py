"""Tests for get_registry_path."""

from pathlib import Path

from agentic_devtools.cli.setup import registry


class TestGetRegistryPath:
    """Tests for get_registry_path."""

    def test_returns_agdt_registry_under_home(self, monkeypatch, tmp_path: Path) -> None:
        """Returns ``~/.agdt/registry.json`` anchored at the user home directory."""
        monkeypatch.setattr(registry.Path, "home", classmethod(lambda cls: tmp_path))
        assert registry.get_registry_path() == tmp_path / ".agdt" / "registry.json"
