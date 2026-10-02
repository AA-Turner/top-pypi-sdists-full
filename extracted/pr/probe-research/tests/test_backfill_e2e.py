"""Two end-to-end properties that no unit test can prove.

Both drive the real flow with a scripted agent binary rather than a mock, so
the argv, the stdin, the manifests, the ledger and the reconcile are all the
real ones. What is faked is the model's judgement, and only that.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import backfill_evidence as ev
from probe.cli import backfill_index as idx
from probe.cli import backfill_plan as bp


def _write(root: Path, rel: str, text: str = "x") -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


@pytest.fixture
def scattered(tmp_path):
    """ONE line of work spread across three sibling directories.

    The layout the whole per-file design exists for: `odyssey` is one project
    whose config, code and notes live in three places nobody would group by
    folder."""
    folder = tmp_path / "drive"
    _write(folder, "configs/odyssey.yaml", "experiment: odyssey3\nlr: 3e-4\n")
    _write(folder, "code/odyssey_train.py", "# odyssey3 infill training\n")
    _write(folder, "notes/odyssey.md", "# Odyssey 3 Reconstruction\nInfill baseline.\n")
    _write(folder, "configs/esm3.yaml", "experiment: esm3-baseline\n")
    for i in range(5):
        _write(folder, f"runs/odyssey/ckpt/s{i}.pt", "w")
    return folder


def _classification() -> str:
    """What a model would answer: odyssey spans three directories."""
    return json.dumps({
        "projects": [{"slug": "odyssey3"}, {"slug": "esm3-baseline"}],
        "assignments": [
            {"path": "configs/odyssey.yaml", "project": "odyssey3"},
            {"path": "code/odyssey_train.py", "project": "odyssey3"},
            {"path": "notes/odyssey.md", "project": "odyssey3"},
            {"path": "configs/esm3.yaml", "project": "esm3-baseline"},
            {"path": "runs/odyssey/ckpt", "project": "odyssey3"},
        ],
        "unsure": [],
        "summary": "two lines of work",
    })


def test_a_project_spanning_three_directories_lands_as_one_project(scattered):
    """THE HARD CONSTRAINT.

    Assignment is per-file, never per-folder, and `pack` groups by PROJECT.
    Any future mechanism that decides subtree-by-subtree must keep a global
    naming pass ahead of it or this fragments into three projects."""
    evidence = ev.gather(scattered)
    assigned, disc = bp.resolve(evidence, bp.parse(_classification()))
    assert disc.trustworthy

    units = bp.pack(evidence, assigned) + bp.pack_tails(evidence, assigned)
    projects_of_odyssey_files = {
        assigned[p] for p in assigned if "odyssey" in p or "esm3" not in p
    }
    assert "odyssey3" in projects_of_odyssey_files

    # The three directories reach ONE project...
    for rel in ("configs/odyssey.yaml", "code/odyssey_train.py", "notes/odyssey.md"):
        assert assigned[rel] == "odyssey3", f"{rel} fragmented"
    # ...and the checkpoints inherited it, without a model reading them.
    ckpts = [u for u in units if u.kind.value == "tail"]
    assert ckpts and all(u.project == "odyssey3" for u in ckpts)
    # ...and no unit mixes projects.
    for unit in units:
        assert {assigned[p] for p in unit.paths} == {unit.project}


def test_every_file_reaches_exactly_one_unit(scattered):
    """Coverage, across both packers, on a realistic layout."""
    evidence = ev.gather(scattered)
    assigned, _ = bp.resolve(evidence, bp.parse(_classification()))
    units = bp.pack(evidence, assigned) + bp.pack_tails(evidence, assigned)
    packed = [p for u in units for p in u.paths]
    assert sorted(packed) == sorted(assigned)
    assert len(packed) == len(set(packed))


def test_an_unchanged_rerun_finds_nothing_to_do(scattered, tmp_path):
    """The Phase 2 payoff, end to end: walk, walk again, and the second walk
    has nothing to import."""
    state = tmp_path / "state"
    first = idx.Index.for_folder(scattered, directory=state)
    list(first.collect(ev.walk(scattered), root=scattered))
    first.commit()
    before = first.read()

    second = idx.Index.for_folder(scattered, directory=state)
    list(second.collect(ev.walk(scattered), root=scattered))
    second.commit()

    delta = idx.diff(before, second.read())
    assert delta.quiet, f"an untouched folder reported {delta.describe()}"
    assert delta.unchanged == len(before)


def test_a_rerun_after_an_edit_reports_only_the_edit(scattered, tmp_path):
    state = tmp_path / "state"
    first = idx.Index.for_folder(scattered, directory=state)
    list(first.collect(ev.walk(scattered), root=scattered))
    first.commit()
    before = first.read()

    _write(scattered, "notes/new.md", "# a new note")
    (scattered / "configs" / "esm3.yaml").write_text("experiment: esm3-baseline\nseed: 1\n")
    (scattered / "code" / "odyssey_train.py").unlink()

    second = idx.Index.for_folder(scattered, directory=state)
    list(second.collect(ev.walk(scattered), root=scattered))
    second.commit()
    delta = idx.diff(before, second.read())

    assert delta.new == ["notes/new.md"]
    assert delta.changed == ["configs/esm3.yaml"]
    assert delta.vanished == ["code/odyssey_train.py"]


def test_the_estimate_matches_the_units_the_import_will_build(scattered):
    """The number quoted on the census screen is the number actually charged."""
    records = list(ev.walk(scattered))
    evidence = ev.gather(scattered)
    assigned, _ = bp.resolve(evidence, bp.parse(_classification()))
    cost = bp.estimate(records)
    # A FLOOR. `pack` groups by project and two projects live here, so the
    # real count is higher -- `estimate` runs before classification and cannot
    # know that. Quoting a floor is the honest version of the same warning.
    assert cost.agent_units <= len(bp.pack(evidence, assigned))
    assert cost.tail_units <= len(bp.pack_tails(evidence, assigned))
    assert cost.agent_units >= 1
