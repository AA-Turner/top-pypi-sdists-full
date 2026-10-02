"""Rollup depth follows the content, not a constant.

A fixed ROLLUP_MAX_DEPTH is wrong in both directions: shallow trees get
over-detailed rows, deep ones collapse whole phases of work into a single row
carrying a count and nothing else. Only SAMPLELESS rows are affected -- a file
with a sample is emitted individually at full path whatever its depth, which is
why this is a granularity fix and not a planner rewrite.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import backfill_evidence as ev


def _write(root: Path, rel: str, text: str = "w") -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def _rollup_dirs(folder: Path) -> set[str]:
    rows = [json.loads(line) for line in ev.to_jsonl(ev.gather(folder)).splitlines()]
    return {r["dir"] for r in rows if "dir" in r}


def test_a_deep_mixed_tree_splits_past_the_fixed_cap(folder_deep):
    """The weakness. At depth 4 both runs collapse into one row the classifier
    cannot split at any confidence."""
    dirs = _rollup_dirs(folder_deep)
    assert any(d.count("/") >= ev.ROLLUP_MAX_DEPTH for d in dirs), (
        f"nothing refined past the cap: {sorted(dirs)}"
    )


@pytest.fixture
def folder_deep(tmp_path):
    """`<person>/<project>/<phase>/<run>/checkpoints/` -- five levels, which is
    one more than the cap, and a routine ML layout."""
    for run in ("run1", "run2"):
        for i in range(30):
            _write(tmp_path, f"michael/odyssey/infill/{run}/ckpt/s{i}.pt")
        for i in range(4):
            _write(tmp_path, f"michael/odyssey/infill/{run}/logs/s{i}.png")
            _write(tmp_path, f"michael/odyssey/infill/{run}/logs/s{i}.npy")
            _write(tmp_path, f"michael/odyssey/infill/{run}/logs/s{i}.pkl")
    return tmp_path


def test_a_homogeneous_checkpoint_directory_is_not_split(tmp_path):
    """One directory of one kind of file is one decision either way. Splitting
    it is rows for nothing, which is the cost the cap exists to control."""
    for i in range(50):
        _write(tmp_path, f"proj/ckpt/s{i:04d}.pt")
    dirs = _rollup_dirs(tmp_path)
    assert dirs == {"proj/ckpt"}


def test_a_flat_folder_is_untouched(tmp_path):
    for i in range(20):
        _write(tmp_path, f"s{i}.pt")
    assert _rollup_dirs(tmp_path) == {"."}


def test_a_wide_directory_splits_on_size_alone(tmp_path):
    """Size is the other trigger: a row standing for thousands of files is
    hiding structure whether or not the extensions vary."""
    for i in range(ev.ROLLUP_SPLIT_FILES + 10):
        _write(tmp_path, f"a/b/c/d/e/part{i % 3}/s{i}.pt")
    dirs = _rollup_dirs(tmp_path)
    assert len(dirs) > 1, f"a {ev.ROLLUP_SPLIT_FILES}+ file row stayed whole: {dirs}"


def test_refinement_stops_at_a_ceiling(tmp_path):
    """Unbounded splitting reproduces the row explosion the cap exists to
    prevent -- measured at 15,842 rows and ~800k tokens on a real tree."""
    deep = "/".join(f"L{i}" for i in range(15))
    for i in range(ev.ROLLUP_SPLIT_FILES + 5):
        _write(tmp_path, f"{deep}/part{i % 4}/s{i}.pt")
    for d in _rollup_dirs(tmp_path):
        assert d.count("/") < ev.ROLLUP_REFINE_MAX_DEPTH


def test_splitting_never_loses_a_file(tmp_path):
    """The coverage guarantee. Every file is still counted by exactly one row."""
    for run in ("r1", "r2"):
        for i in range(20):
            _write(tmp_path, f"p/proj/phase/{run}/ckpt/s{i}.pt")
            _write(tmp_path, f"p/proj/phase/{run}/img/s{i}.png")
            _write(tmp_path, f"p/proj/phase/{run}/arr/s{i}.npy")
            _write(tmp_path, f"p/proj/phase/{run}/pk/s{i}.pkl")
    evidence = ev.gather(tmp_path)
    rows = [json.loads(line) for line in ev.to_jsonl(evidence).splitlines()]
    counted = sum(r.get("files", 0) for r in rows if "dir" in r)
    individual = sum(1 for r in rows if "path" in r)
    assert counted + individual == evidence.total_files


def test_a_single_child_does_not_loop_forever(tmp_path):
    """Every file sharing the next component means the split split nothing;
    re-adding it would spin to the depth ceiling for no gain."""
    for i in range(ev.ROLLUP_SPLIT_FILES + 5):
        _write(tmp_path, f"a/b/c/d/only/s{i}.pt")
    dirs = _rollup_dirs(tmp_path)
    assert dirs, "it terminated"
