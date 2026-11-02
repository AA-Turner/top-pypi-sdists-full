"""Tests for durable single-finding dispatch attempt records."""

import json
import os
from pathlib import Path

import pytest

from agentic_devtools.cli.github import single_finding_dispatch_attempt_store as module
from agentic_devtools.cli.github.single_finding_dispatch import AcceptancePersistenceError


def test_write_attempt_record_atomically_persists_json(tmp_path: Path) -> None:
    path = tmp_path / "attempts" / "attempt.json"
    expected = {"attempt_id": "attempt-1", "outcome": "in_flight"}

    module.write_attempt_record(path, expected, 1)

    assert json.loads(path.read_text(encoding="utf-8")) == expected
    assert list(path.parent.glob("*.tmp")) == []


def test_write_attempt_record_cleans_temp_file_when_replace_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "attempt.json"

    def fail_replace(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
        raise OSError("replace failed")

    monkeypatch.setattr(module.os, "replace", fail_replace)

    with pytest.raises(AcceptancePersistenceError, match="replace failed"):
        module.write_attempt_record(path, {"outcome": "in_flight"}, 1)

    assert not path.exists()
    assert list(tmp_path.glob("*.tmp")) == []


def test_write_attempt_record_skips_directory_sync_on_windows_without_directory_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "attempt.json"
    with monkeypatch.context() as patch:
        patch.setattr(module, "_SKIP_DIRECTORY_FSYNC", True)

        module.write_attempt_record(path, {"outcome": "in_flight"}, 1)

    assert json.loads(path.read_text(encoding="utf-8")) == {"outcome": "in_flight"}
