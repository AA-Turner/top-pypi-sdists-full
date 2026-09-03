"""Unit tests for the _iter_frames helper (protected_storage.py)."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    _iter_frames,
)


def test_iter_frames_returns_nothing_for_missing_path(tmp_path: Path) -> None:
    assert list(_iter_frames(tmp_path / "missing.ndjson", skip_invalid=True)) == []


def test_iter_frames_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "frames.ndjson"
    path.write_text(
        '\n{"version": 1, "salt": "aa==", "nonce": "bb==", "ciphertext": "cc==", "tag": "dd=="}\n', encoding="utf-8"
    )
    frames = list(_iter_frames(path, skip_invalid=True))
    assert len(frames) == 1


def test_iter_frames_skips_malformed_line_when_skip_invalid_true(tmp_path: Path) -> None:
    path = tmp_path / "frames.ndjson"
    path.write_text("not valid json\n", encoding="utf-8")
    assert list(_iter_frames(path, skip_invalid=True)) == []


def test_iter_frames_raises_on_malformed_line_when_not_skipping(tmp_path: Path) -> None:
    path = tmp_path / "frames.ndjson"
    path.write_text("not valid json\n", encoding="utf-8")
    with pytest.raises(Exception):  # noqa: B017 - json.JSONDecodeError or KeyError, implementation detail
        list(_iter_frames(path, skip_invalid=False))
