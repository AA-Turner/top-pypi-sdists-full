"""Tests for load_corpus in rederive_deferral_variants."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.scripts.rederive_deferral_variants import record, rederive, round_, suppressed_body


def _write(tmp_path: Path, *lines: str) -> Path:
    path = tmp_path / "corpus.jsonl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_round_trips_a_record(tmp_path: Path) -> None:
    """A record survives serialisation and reload unchanged."""
    original = record(
        round_(review_id=5, body=suppressed_body("specs/1/spec.md"), posted_paths=("specs/1/plan.md",)),
        number=42,
        changed_files=("specs/1/spec.md",),
    )
    path = _write(tmp_path, json.dumps(rederive.record_to_json(original)))
    assert rederive.load_corpus(path) == [original]


def test_skips_blank_lines(tmp_path: Path) -> None:
    """Blank lines in the corpus file are ignored."""
    payload = json.dumps(rederive.record_to_json(record(round_(body=suppressed_body("specs/1/spec.md")))))
    path = _write(tmp_path, payload, "", "   ", payload)
    assert len(rederive.load_corpus(path)) == 2


def test_rejects_a_line_that_is_not_a_record(tmp_path: Path) -> None:
    """A malformed corpus is an error, not a silently shorter corpus."""
    path = _write(tmp_path, json.dumps({"rounds": []}))
    with pytest.raises(ValueError, match="not a pull request record"):
        rederive.load_corpus(path)


def test_rejects_a_non_list_rounds_field(tmp_path: Path) -> None:
    """'rounds' must be a list; anything else names the offending PR."""
    path = _write(tmp_path, json.dumps({"number": 42, "rounds": {}}))
    with pytest.raises(ValueError, match="PR #42"):
        rederive.load_corpus(path)


def test_defaults_missing_optional_fields(tmp_path: Path) -> None:
    """A sparse round still loads when changed_files is an explicit empty list."""
    path = _write(tmp_path, json.dumps({"number": 42, "changed_files": [], "rounds": [{}]}))
    loaded = rederive.load_corpus(path)[0]
    assert loaded.changed_files == ()
    assert loaded.rounds[0] == rederive.Round(review_id=0, submitted_at="", body="", posted_paths=())


def test_rejects_missing_changed_files(tmp_path: Path) -> None:
    """A record without changed_files must be rejected; defaulting to () silently bypasses condition 10."""
    path = _write(tmp_path, json.dumps({"number": 42, "rounds": []}))
    with pytest.raises(ValueError, match="changed_files"):
        rederive.load_corpus(path)


def test_rejects_non_string_changed_file_entries(tmp_path: Path) -> None:
    """Each changed_files entry must already be a path string, not an arbitrary JSON value."""
    path = _write(tmp_path, json.dumps({"number": 42, "changed_files": [None], "rounds": []}))
    with pytest.raises(ValueError, match="changed_files\\[0\\]"):
        rederive.load_corpus(path)


def test_rejects_non_object_round_entries(tmp_path: Path) -> None:
    """Each round must be an object so malformed corpus rows fail fast with context."""
    path = _write(tmp_path, json.dumps({"number": 42, "changed_files": [], "rounds": ["bad"]}))
    with pytest.raises(ValueError, match="rounds\\[0\\]"):
        rederive.load_corpus(path)


def test_rejects_non_list_posted_paths(tmp_path: Path) -> None:
    """posted_paths must be a list of path strings, not a scalar that would iterate incorrectly."""
    path = _write(tmp_path, json.dumps({"number": 42, "changed_files": [], "rounds": [{"posted_paths": "abc"}]}))
    with pytest.raises(ValueError, match="posted_paths"):
        rederive.load_corpus(path)


@pytest.mark.parametrize("falsey_non_list", [{}, "", 0, False])
def test_rejects_falsey_non_list_posted_paths(tmp_path: Path, falsey_non_list: object) -> None:
    """Falsey non-list values must be rejected, not silently replaced by an empty list."""
    path = _write(
        tmp_path,
        json.dumps({"number": 42, "changed_files": [], "rounds": [{"posted_paths": falsey_non_list}]}),
    )
    with pytest.raises(ValueError, match="posted_paths"):
        rederive.load_corpus(path)
