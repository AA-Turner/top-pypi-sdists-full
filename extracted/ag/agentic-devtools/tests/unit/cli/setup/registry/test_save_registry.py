"""Tests for save_registry."""

import json
from pathlib import Path

from agentic_devtools.cli.setup import registry
from agentic_devtools.cli.setup.registry import (
    ArtifactEntry,
    ContextEntry,
    RegistryData,
    load_registry,
    save_registry,
)


class TestSaveRegistry:
    """Tests for save_registry."""

    def test_writes_deterministic_sorted_json(self, tmp_path: Path) -> None:
        """The serialized file uses sorted keys and a trailing newline."""
        path = tmp_path / "registry.json"
        data = RegistryData(
            contexts={"ctxA": ContextEntry(path="/a", last_setup_utc="t", artifacts=["h1"])},
            artifacts={"h1": ArtifactEntry(type="npmrc", path="/n", content_hash="h1", referenced_by=["ctxA"])},
        )
        save_registry(data, path)
        text = path.read_text(encoding="utf-8")
        assert text.endswith("\n")
        assert json.loads(text) == data.to_dict()
        assert text == json.dumps(data.to_dict(), indent=2, sort_keys=True) + "\n"

    def test_output_is_byte_identical_across_saves(self, tmp_path: Path) -> None:
        """Saving identical data twice produces byte-identical output (NFR-005)."""
        first = tmp_path / "one.json"
        second = tmp_path / "two.json"
        data = RegistryData(
            artifacts={"h1": ArtifactEntry(type="npmrc", path="/n", content_hash="h1", referenced_by=["ctxB", "ctxA"])},
        )
        save_registry(data, first)
        save_registry(data, second)
        assert first.read_bytes() == second.read_bytes()

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Missing parent directories are created."""
        path = tmp_path / "nested" / "dir" / "registry.json"
        save_registry(RegistryData(), path)
        assert path.is_file()

    def test_uses_default_path_when_omitted(self, tmp_path: Path, monkeypatch) -> None:
        """When registry_path is omitted, get_registry_path is consulted."""
        default_path = tmp_path / "default" / "registry.json"
        monkeypatch.setattr(registry, "get_registry_path", lambda: default_path)
        save_registry(RegistryData())
        assert load_registry(default_path) == RegistryData()
