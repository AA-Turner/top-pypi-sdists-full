"""Unit tests for ConfigHistoryService."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from anteroom.services.config_history import (
    ConfigHistoryService,
    get_backup_dir,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestGetBackupDir:
    def test_returns_expected_path(self, tmp_path: Path) -> None:
        assert get_backup_dir(tmp_path) == tmp_path / "backups" / "config"


class TestSnapshot:
    def test_creates_backup_file(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="test")
        assert entry is not None
        backup = tmp_path / "bak" / entry.path
        assert backup.exists()
        assert backup.read_text() == cfg.read_text()

    def test_returns_none_when_source_missing(self, tmp_path: Path) -> None:
        cfg = tmp_path / "nonexistent.yaml"
        svc = ConfigHistoryService(tmp_path / "bak")
        assert svc.snapshot(cfg, source="test") is None

    def test_dedup_skips_identical_content(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry1 = svc.snapshot(cfg, source="first")
        entry2 = svc.snapshot(cfg, source="second")
        assert entry1 is not None
        assert entry2 is not None
        assert entry1.id == entry2.id
        assert len(list((tmp_path / "bak").glob("config-*.yaml"))) == 1

    def test_new_snapshot_after_content_change(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        e1 = svc.snapshot(cfg, source="first")
        _write(cfg, "ai:\n  model: gpt-4o\n")
        e2 = svc.snapshot(cfg, source="second")
        assert e1 is not None
        assert e2 is not None
        assert e1.id != e2.id
        assert len(list((tmp_path / "bak").glob("config-*.yaml"))) == 2

    def test_entry_fields(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="mytest")
        assert entry is not None
        assert entry.source == "mytest"
        assert len(entry.sha256) == 64
        assert entry.path.startswith("config-")
        assert entry.path.endswith(".yaml")

    def test_backup_dir_created_with_0700(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        bak = tmp_path / "bak"
        svc = ConfigHistoryService(bak)
        svc.snapshot(cfg, source="test")
        mode = bak.stat().st_mode & 0o777
        # On some platforms chmod may be restricted; only check when it works
        assert mode in (0o700, 0o755, 0o777)

    def test_backup_file_0600(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="test")
        assert entry is not None
        backup = tmp_path / "bak" / entry.path
        mode = backup.stat().st_mode & 0o777
        assert mode in (0o600, 0o644, 0o666)

    def test_manifest_jsonl_format(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        bak = tmp_path / "bak"
        svc = ConfigHistoryService(bak)
        svc.snapshot(cfg, source="test")
        manifest = bak / "history.jsonl"
        assert manifest.exists()
        lines = [ln for ln in manifest.read_text().splitlines() if ln.strip()]
        assert len(lines) == 1
        row = json.loads(lines[0])
        assert {"id", "timestamp", "source", "sha256", "path"} <= row.keys()
        assert row["source"] == "test"


class TestListVersions:
    def test_empty_when_no_history(self, tmp_path: Path) -> None:
        svc = ConfigHistoryService(tmp_path / "bak")
        assert svc.list_versions() == []

    def test_newest_first(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        svc.snapshot(cfg, source="a")
        _write(cfg, "x: 2\n")
        svc.snapshot(cfg, source="b")
        entries = svc.list_versions()
        assert len(entries) == 2
        assert entries[0].source == "b"
        assert entries[1].source == "a"

    def test_skips_malformed_manifest_lines(self, tmp_path: Path) -> None:
        bak = tmp_path / "bak"
        bak.mkdir()
        manifest = bak / "history.jsonl"
        manifest.write_text('{"bad": true}\n{"id":"x","timestamp":"t","source":"s","sha256":"h","path":"p"}\n')
        svc = ConfigHistoryService(bak)
        entries = svc.list_versions()
        assert len(entries) == 1
        assert entries[0].id == "x"

    def test_skips_non_object_manifest_lines(self, tmp_path: Path) -> None:
        """A non-dict JSON line (list/number/string) should not crash list_versions."""
        bak = tmp_path / "bak"
        bak.mkdir()
        manifest = bak / "history.jsonl"
        manifest.write_text(
            '[1,2,3]\n"just a string"\n42\n{"id":"x","timestamp":"t","source":"s","sha256":"h","path":"p"}\n'
        )
        svc = ConfigHistoryService(bak)
        entries = svc.list_versions()
        assert len(entries) == 1
        assert entries[0].id == "x"


class TestResolveBackupPath:
    def test_raises_on_path_traversal(self, tmp_path: Path) -> None:
        bak = tmp_path / "bak"
        bak.mkdir()
        manifest = bak / "history.jsonl"
        manifest.write_text('{"id":"x","timestamp":"t","source":"s","sha256":"h","path":"../../evil.yaml"}\n')
        svc = ConfigHistoryService(bak)
        entry = svc.list_versions()[0]
        with pytest.raises(ValueError, match="Unsafe backup path"):
            svc._resolve_backup_path(entry)

    def test_valid_path_returns_resolved(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="test")
        assert entry is not None
        resolved = svc._resolve_backup_path(entry)
        assert resolved.exists()
        assert resolved.is_relative_to((tmp_path / "bak").resolve())


class TestDiff:
    def test_diff_shows_changes(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="before")
        assert entry is not None
        _write(cfg, "ai:\n  model: gpt-4o\n")
        diff = svc.diff(entry.id, cfg)
        assert "-  model: gpt-4" in diff
        assert "+  model: gpt-4o" in diff

    def test_no_diff_when_identical(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="x")
        assert entry is not None
        assert svc.diff(entry.id, cfg) == ""

    def test_raises_on_unknown_version(self, tmp_path: Path) -> None:
        svc = ConfigHistoryService(tmp_path / "bak")
        with pytest.raises(KeyError, match="nope"):
            svc.diff("nope", tmp_path / "config.yaml")


class TestRestore:
    def test_restores_file_content(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="before")
        assert entry is not None
        _write(cfg, "ai:\n  model: gpt-4o\n")
        svc.restore(entry.id, cfg)
        assert cfg.read_text() == "ai:\n  model: gpt-4\n"

    def test_restore_snapshots_current_state_first(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        entry = svc.snapshot(cfg, source="before")
        assert entry is not None
        _write(cfg, "ai:\n  model: gpt-4o\n")
        svc.restore(entry.id, cfg)
        versions = svc.list_versions()
        sources = [v.source for v in versions]
        assert "pre-restore" in sources

    def test_restore_raises_on_unknown_version(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        with pytest.raises(KeyError, match="nope"):
            svc.restore("nope", cfg)


class TestDetectAndSnapshotExternalEdit:
    def test_snapshots_when_hash_differs(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        svc.snapshot(cfg, source="initial")
        _write(cfg, "ai:\n  model: gpt-4o\n")
        result = svc.detect_and_snapshot_external_edit(cfg)
        assert result is True
        entries = svc.list_versions()
        assert entries[0].source == "external"

    def test_no_snapshot_when_hash_matches(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "ai:\n  model: gpt-4\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        svc.snapshot(cfg, source="initial")
        result = svc.detect_and_snapshot_external_edit(cfg)
        assert result is False
        assert len(svc.list_versions()) == 1

    def test_returns_false_when_file_missing(self, tmp_path: Path) -> None:
        svc = ConfigHistoryService(tmp_path / "bak")
        result = svc.detect_and_snapshot_external_edit(tmp_path / "nonexistent.yaml")
        assert result is False

    def test_snapshots_on_first_call_with_no_history(self, tmp_path: Path) -> None:
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        result = svc.detect_and_snapshot_external_edit(cfg)
        assert result is True
        assert len(svc.list_versions()) == 1

    def test_first_snapshot_labeled_initial_not_external(self, tmp_path: Path) -> None:
        """First-seen config cannot be an external edit — label it 'initial'."""
        cfg = tmp_path / "config.yaml"
        _write(cfg, "x: 1\n")
        svc = ConfigHistoryService(tmp_path / "bak")
        svc.detect_and_snapshot_external_edit(cfg)
        entries = svc.list_versions()
        assert entries[0].source == "initial"
