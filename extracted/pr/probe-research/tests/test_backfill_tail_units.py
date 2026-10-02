"""TAIL units are fulfilled by code, and still land in the same places.

The cost fix is only safe if coverage is identical: every tail file must still
reach a manifest, still be enqueued, and still be resumable. What changes is
who writes the row, not whether it exists.
"""

from __future__ import annotations

import json

import pytest

from probe.cli import backfill_ledger as ledger_mod
from probe.cli import backfill_plan as plan_mod
from probe.cli import backfill_run
from probe.cli.backfill_ledger import Unit, UnitKind


@pytest.fixture
def tail_unit():
    return Unit(
        unit_id="tail01",
        project="odyssey3",
        paths=("ckpt/step_10.pt", "ckpt/step_20.pt"),
        kind=UnitKind.TAIL,
    )


def test_a_tail_unit_writes_its_manifest_without_an_agent(tail_unit, tmp_path, monkeypatch):
    """The whole point. `launch_agent` must never be reached."""
    def explode(*_a, **_k):
        raise AssertionError("a TAIL unit must not start an agent")

    monkeypatch.setattr(backfill_run.bf, "launch_agent", explode)
    ledger = ledger_mod.Ledger(tmp_path / "l.jsonl")
    out = backfill_run.run_unit(
        tmp_path, tail_unit, agent=backfill_run.bf.Agent.CLAUDE,
        ledger=ledger, work_dir=tmp_path, sizes={},
    )
    assert out.ok and out.rows == 2
    rows = [json.loads(x) for x in out.manifest.read_text().splitlines()]
    assert [r["path"] for r in rows] == ["ckpt/step_10.pt", "ckpt/step_20.pt"]


def test_a_tail_row_carries_no_invented_notes(tail_unit):
    """A generated sentence about a checkpoint is a guess wearing a fact's
    clothes. The import prompt has always allowed a row without notes."""
    rows = plan_mod.tail_manifest(tail_unit, {})
    assert all("notes" not in r for r in rows)


def test_a_huge_tail_file_uploads_by_reference(tail_unit):
    sizes = {"ckpt/step_10.pt": plan_mod.REFERENCE_ABOVE_BYTES * 100,
             "ckpt/step_20.pt": 1024}
    rows = {r["path"]: r for r in plan_mod.tail_manifest(tail_unit, sizes)}
    assert rows["ckpt/step_10.pt"]["reference"] is True
    assert rows["ckpt/step_10.pt"]["allow_missing"] is True
    assert rows["ckpt/step_20.pt"]["reference"] is False
    assert "allow_missing" not in rows["ckpt/step_20.pt"]


def test_a_tail_unit_is_an_ordinary_ledger_unit(tail_unit, tmp_path):
    """Resume, delivery tracking and lost-enqueue recovery all read the ledger.
    A unit that never appears there is a unit those three cannot see."""
    ledger = ledger_mod.Ledger(tmp_path / "l.jsonl")
    ledger.record_plan([tail_unit], ["odyssey3"])
    backfill_run.run_unit(
        tmp_path, tail_unit, agent=backfill_run.bf.Agent.CLAUDE,
        ledger=ledger, work_dir=tmp_path, sizes={},
    )
    state = ledger.read()
    record = state.units.get("tail01")
    assert record is not None and record.enqueued == 2


def test_the_kind_survives_the_ledger_round_trip(tmp_path):
    """A resumed tail unit that came back as an AGENT unit would be handed to a
    model -- the exact cost this change removes, reappearing only on resume."""
    ledger = ledger_mod.Ledger(tmp_path / "l.jsonl")
    units = [
        Unit(unit_id="a1", project="p", paths=("x.py",)),
        Unit(unit_id="t1", project="p", paths=("y.pt",), kind=UnitKind.TAIL),
    ]
    ledger.record_plan(units, ["p"])
    back = ledger.read().units
    assert back["a1"].unit.kind is UnitKind.AGENT
    assert back["t1"].unit.kind is UnitKind.TAIL


def test_a_ledger_written_before_tails_existed_reads_as_agent_work(tmp_path):
    """Absent `kind` must mean AGENT: everything was agent work then."""
    path = tmp_path / "old.jsonl"
    path.write_text(json.dumps({
        "t": "plan", "schema": 1, "projects": ["p"],
        "units": [{"unit_id": "u1", "project": "p", "paths": ["a.py"]}],
    }) + "\n")
    back = ledger_mod.Ledger(path).read().units
    assert back["u1"].unit.kind is UnitKind.AGENT


def test_a_resumed_tail_unit_stats_its_sizes_back(tmp_path):
    """The resume path never re-walks, so there is no evidence to read sizes
    from -- and an unknown size reads as "small", which would send a 10GB
    checkpoint by value."""
    big = tmp_path / "big.pt"
    big.write_bytes(b"x" * 4096)
    unit = Unit(unit_id="t1", project="p", paths=("big.pt",), kind=UnitKind.TAIL)
    sizes = backfill_run.sizes_for_tails(tmp_path, None, [unit])
    assert sizes["big.pt"] == 4096


def test_a_vanished_tail_file_does_not_break_the_stat_back(tmp_path):
    unit = Unit(unit_id="t1", project="p", paths=("gone.pt",), kind=UnitKind.TAIL)
    assert backfill_run.sizes_for_tails(tmp_path, None, [unit]) == {}


def test_the_kinds_are_distinguishable(tmp_path):
    """A stray `@dataclass` on the enum made every member compare and hash
    equal -- `UnitKind.AGENT == UnitKind.TAIL` was True and the repr was
    `UnitKind()`. Every call site used `is` so nothing broke, which is exactly
    what makes it a landmine: the first `==` or `in {...}` routes every unit
    down the tail path."""
    assert UnitKind.AGENT != UnitKind.TAIL
    assert len({UnitKind.AGENT, UnitKind.TAIL}) == 2
    assert "tail" in repr(UnitKind.TAIL)


def test_a_unit_is_hashable_and_frozen():
    unit = Unit(unit_id="u1", project="p", paths=("a.md",))
    assert hash(unit)
    with pytest.raises(Exception):
        unit.project = "other"


def test_a_tail_unit_respects_the_byte_cap(tmp_path):
    """Files under the reference threshold upload by VALUE, so 400 99MB shards
    in one unit is a 39GB enqueue whose failure costs all of it."""
    from probe.cli import backfill_evidence as ev_mod
    from probe.cli import backfill_plan as bp

    for i in range(6):
        p = tmp_path / f"s{i}.pt"
        p.write_bytes(b"w")
    evidence = ev_mod.gather(tmp_path)
    big = 1000
    evidence.files = [
        ev_mod.FileEvidence(path=f.path, size=big, mtime=f.mtime, tier=f.tier)
        for f in evidence.files
    ]
    assigned = {p: "p" for p in bp.relative_paths(evidence)}
    units = bp.pack_tails(evidence, assigned, max_files=1000, max_bytes=2500)
    assert len(units) == 3, "six 1000-byte tails at 2500 bytes per unit"
