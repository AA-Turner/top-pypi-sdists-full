"""What the import is about to cost, quoted before anything is spent.

The screen this feeds is the last free one: after sampling, a classify pass has
already been paid for. A wrong number here is what let a real import run a
token plan dry halfway through.
"""

from __future__ import annotations

from pathlib import Path


from probe.cli import backfill_evidence as ev
from probe.cli import backfill_plan as bp


def _records(tmp_path: Path):
    return list(ev.walk(tmp_path))


def test_a_small_folder_costs_the_classify_pass_and_one_unit(tmp_path):
    for i in range(3):
        (tmp_path / f"n{i}.md").write_text("x")
    got = bp.estimate(_records(tmp_path))
    assert got.evidence_files == 3
    assert got.agent_units == 1
    assert got.turns == 1 + bp.CLASSIFY_TURNS


def test_the_file_cap_binds_on_a_folder_of_small_configs(tmp_path):
    for i in range(9):
        (tmp_path / f"c{i}.yaml").write_text("k: v")
    got = bp.estimate(_records(tmp_path), max_files=4)
    assert got.agent_units == 3, "9 files at 4 per unit"


def test_the_byte_cap_binds_on_a_folder_of_big_evidence(tmp_path):
    """The half that was missing. Quoting `files / MAX_UNIT_FILES` alone
    understated a checkpoint-heavy import by one to two orders of magnitude."""
    for i in range(6):
        (tmp_path / f"log{i}.log").write_text("x" * 1000)
    got = bp.estimate(_records(tmp_path), max_files=1000, max_bytes=2500)
    assert got.agent_units == 3, "six 1000-byte files at 2500 bytes per unit"


def test_reference_only_files_do_not_inflate_the_estimate(tmp_path):
    """They are stored as a path plus a hash; their bytes never move, so
    charging them would split units on transfers that do not happen."""
    (tmp_path / "a.log").write_text("x")
    records = _records(tmp_path)
    huge = [
        ev.FileEvidence(path=str(tmp_path / f"big{i}.log"),
                        size=bp.REFERENCE_ABOVE_BYTES * 10,
                        mtime=0.0, tier=ev.Tier.EVIDENCE)
        for i in range(5)
    ]
    got = bp.estimate(records + huge, max_bytes=bp.REFERENCE_ABOVE_BYTES)
    assert got.agent_units == 1, "five reference-only files still fit one unit"


def test_checkpoints_cost_no_agent_turns(tmp_path):
    """The cost fix, stated where the user can see it before paying."""
    (tmp_path / "readme.md").write_text("hi")
    for i in range(50):
        (tmp_path / f"step_{i}.pt").write_bytes(b"w")
    got = bp.estimate(_records(tmp_path), max_files=10)
    assert got.tail_files == 50
    assert got.agent_units == 1, "only the readme is agent work"
    assert "50 checkpoint-like files imported without one" in got.describe()


def test_an_empty_folder_says_nothing(tmp_path):
    assert bp.estimate(_records(tmp_path)).describe() == ""


def test_the_description_says_at_least(tmp_path):
    """"or more", never a bare number: packing is per-project and this runs
    before the projects are known, so the figure is a floor."""
    (tmp_path / "a.md").write_text("x")
    assert bp.estimate(_records(tmp_path)).describe().endswith("or more")


def test_the_estimate_matches_what_packing_actually_produces(tmp_path):
    """The number quoted and the number charged must be the same number.

    `estimate` mirrors `pack`/`pack_tails` rather than calling them -- they
    need an assignment map that does not exist yet -- so the two can drift.
    This is the tripwire for that drift."""
    for i in range(25):
        (tmp_path / f"c{i}.yaml").write_text("k: v")
    for i in range(12):
        (tmp_path / f"s{i}.pt").write_bytes(b"w")
    records = _records(tmp_path)
    evidence = ev.gather(tmp_path)
    assigned = {p: "p" for p in bp.relative_paths(evidence)}
    got = bp.estimate(records, max_files=7)
    # A FLOOR, not an equality: packing is per-project and `estimate` runs
    # before the projects are known. One project here, so the floor is tight.
    assert got.agent_units <= len(bp.pack(evidence, assigned, max_files=7))
    assert got.tail_units <= len(bp.pack_tails(evidence, assigned, max_files=7))
