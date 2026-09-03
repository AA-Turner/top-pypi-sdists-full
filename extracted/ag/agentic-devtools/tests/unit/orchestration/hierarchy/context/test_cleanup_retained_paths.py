"""Unit tests for context injection records and trace event_detail serialization."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.orchestration.hierarchy.context import (
    cleanup_retained_paths,
)


def test_cleanup_retained_paths_uses_delete_when_available() -> None:
    class _Deletable:
        def __init__(self, *, result: bool) -> None:
            self.result = result
            self.calls = 0

        def delete(self) -> bool:
            self.calls += 1
            return self.result

    kept = _Deletable(result=False)
    removed = _Deletable(result=True)
    deleted = cleanup_retained_paths((kept, removed))
    assert deleted == (removed,)
    assert kept.calls == 1
    assert removed.calls == 1


def test_cleanup_retained_paths_deletes_existing_paths(tmp_path: Path) -> None:
    retained = tmp_path / "retained.ndjson"
    retained.write_text("data", encoding="utf-8")
    missing = tmp_path / "missing.ndjson"
    assert cleanup_retained_paths((retained, missing)) == (retained,)
    assert not retained.exists()
