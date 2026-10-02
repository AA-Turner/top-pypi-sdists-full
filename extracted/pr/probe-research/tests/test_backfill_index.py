"""The walk, written down: determinism, the diff, and what it refuses to do.

The index exists so a re-run can answer "what is new since last time". Every
test here is about that answer being trustworthy -- a diff that is wrong is
worse than no diff, because it drives what gets imported.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.cli import backfill_evidence as ev
from probe.cli import backfill_index as idx


def _write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def _index_walk(folder: Path, state: Path):
    index = idx.Index.for_folder(folder, directory=state)
    records = list(index.collect(ev.walk(folder), root=folder))
    index.commit()
    return index, records


def test_the_walk_is_written_down_and_reads_back(tmp_path):
    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    _write(folder, "sub/b.py", "y")
    index, records = _index_walk(folder, state)
    assert len(records) == 2, "the generator still yields every record it was given"
    assert sorted(r.path for r in index.read()) == ["a.md", "sub/b.py"]


def test_rows_are_sorted_whatever_order_the_filesystem_gave(tmp_path):
    """Not tidiness. The sampler's smallest-first sort is stable, so ties at
    the budget broke on filesystem order and two runs over one unchanged
    folder could sample a different 600 files."""
    folder, state = tmp_path / "f", tmp_path / "state"
    for name in ("z.md", "a.md", "m.md"):
        _write(folder, name, "x")
    index, _ = _index_walk(folder, state)
    paths = [r.path for r in index.read()]
    assert paths == sorted(paths)


def test_an_unchanged_folder_has_the_same_walk_id(tmp_path):
    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    first, _ = _index_walk(folder, state)
    first_id = first.walk_id()
    second, _ = _index_walk(folder, state)
    assert second.walk_id() == first_id


def test_a_changed_file_changes_the_walk_id(tmp_path):
    folder, state = tmp_path / "f", tmp_path / "state"
    f = _write(folder, "a.md", "x")
    before, _ = _index_walk(folder, state)
    before_id = before.walk_id()
    f.write_text("xx")
    after, _ = _index_walk(folder, state)
    assert after.walk_id() != before_id


# -- the diff ----------------------------------------------------------------


def _rows(*spec):
    return [idx.Row(path=p, size=s, mtime=m) for p, s, m in spec]


def test_the_three_classes_are_separated(tmp_path):
    before = _rows(("keep.md", 1, 100.0), ("edit.md", 1, 100.0), ("gone.md", 1, 100.0))
    after = _rows(("keep.md", 1, 100.0), ("edit.md", 2, 200.0), ("new.md", 1, 100.0))
    got = idx.diff(before, after)
    assert got.new == ["new.md"]
    assert got.changed == ["edit.md"]
    assert got.vanished == ["gone.md"]
    assert got.unchanged == 1


def test_a_changed_file_is_reported_not_silently_reimported():
    """Same-name artifacts COEXIST in Probe rather than superseding, so a
    re-upload is a duplicate beside the original. Until versioning is decided,
    saying so is the honest answer."""
    got = idx.diff(_rows(("a.md", 1, 100.0)), _rows(("a.md", 2, 100.0)))
    text = " ".join(got.describe())
    assert "changed" in text and "not re-imported" in text
    assert "beside the original" in text


def test_a_vanished_file_retires_nothing():
    got = idx.diff(_rows(("a.md", 1, 100.0)), [])
    text = " ".join(got.describe())
    assert "nothing was retired" in text
    assert "unmounted" in text, "an absent drive is the likelier explanation"


def test_a_recopied_drive_is_not_a_full_reimport():
    """Every inode changes on a recopy or a remount while content is
    identical. Inode in the identity would make that a full re-import with a
    duplicate of every artifact."""
    before = [idx.Row(path="a.pt", size=10, mtime=100.0, inode=1)]
    after = [idx.Row(path="a.pt", size=10, mtime=100.0, inode=99999)]
    assert idx.diff(before, after).quiet


def test_sub_second_mtime_drift_is_not_a_change():
    """Filesystems disagree about sub-second resolution, so a copy between two
    of them changes a float that means nothing has changed."""
    before = [idx.Row(path="a.md", size=1, mtime=100.4)]
    after = [idx.Row(path="a.md", size=1, mtime=100.9)]
    assert idx.diff(before, after).quiet


def test_a_quiet_diff_says_nothing(tmp_path):
    assert idx.diff([], []).describe() == []


# -- refusing to guess -------------------------------------------------------


def test_an_unknown_schema_reads_as_absent(tmp_path):
    """One re-walk is cheap. Diffing against rows whose meaning we cannot
    vouch for is how a folder gets re-imported wholesale."""
    p = tmp_path / "i.jsonl"
    p.write_text(json.dumps({"schema": "something.else/9"}) + "\n")
    assert idx.Index(p).read() == []


def test_a_missing_index_reads_as_absent(tmp_path):
    assert idx.Index(tmp_path / "nope.jsonl").read() == []


def test_one_truncated_row_does_not_lose_the_index(tmp_path):
    """A killed process leaves a half-written final line. That should cost the
    line, not the whole diff."""
    p = tmp_path / "i.jsonl"
    p.write_text(
        json.dumps({"schema": idx.SCHEMA, "rows": 2}) + "\n"
        + json.dumps({"path": "a.md", "size": 1, "mtime": 1.0}) + "\n"
        + '{"path": "b.md", "si'
    )
    assert [r.path for r in idx.Index(p).read()] == ["a.md"]


def test_a_crash_mid_write_leaves_the_previous_index_intact(tmp_path):
    """Written to a sibling and renamed. A half-file would diff as
    "everything vanished" and re-import the folder."""
    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    index, _ = _index_walk(folder, state)
    good = index.read()

    def explode(_records):
        raise OSError("disk full")

    with pytest.raises(OSError):
        list(index.collect(_boom(), root=folder))
    assert index.read() == good


def _boom():
    yield from ()
    raise OSError("disk full")


def test_the_index_lives_beside_the_ledger(tmp_path):
    """One folder's bookkeeping in one place, so PROBE_BACKFILL_STATE_DIR
    moves all of it at once."""
    from probe.cli import backfill_ledger as ledger_mod

    folder = tmp_path / "f"
    folder.mkdir()
    index = idx.Index.for_folder(folder, directory=tmp_path / "state")
    ledger = ledger_mod.Ledger.for_folder(folder, directory=tmp_path / "state")
    assert index.path.parent == ledger.path.parent
    assert index.path != ledger.path


# -- naming what was dropped -------------------------------------------------


def test_the_shortfall_is_named_not_just_counted(tmp_path):
    """"N unaccounted for" tells a reader something went missing and gives
    them no way to find out what. Both sides are local: the index is what was
    walked, the manifests are what the import claimed."""
    from probe.cli.backfill_run import UnitOutcome, write_unaccounted
    from probe.cli.backfill_ledger import Unit

    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "kept.md", "x")
    _write(folder, "dropped.md", "y")
    index, _ = _index_walk(folder, state)

    work = tmp_path / "work"
    work.mkdir()
    manifest = work / "u1.jsonl"
    manifest.write_text(json.dumps({"path": "kept.md"}) + "\n")
    outcome = UnitOutcome(
        unit=Unit(unit_id="u1", project="p", paths=("kept.md",)),
        ok=True, manifest=manifest, rows=1,
    )

    out = write_unaccounted(index, work, [outcome])
    assert out is not None
    assert out.read_text().split() == ["dropped.md"]


def test_nothing_missing_writes_no_file(tmp_path):
    """An empty file reads as a failed write. No file is the clearer answer."""
    from probe.cli.backfill_run import UnitOutcome, write_unaccounted
    from probe.cli.backfill_ledger import Unit

    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    index, _ = _index_walk(folder, state)
    work = tmp_path / "work"
    work.mkdir()
    manifest = work / "u1.jsonl"
    manifest.write_text(json.dumps({"path": "a.md"}) + "\n")
    outcome = UnitOutcome(
        unit=Unit(unit_id="u1", project="p", paths=("a.md",)),
        ok=True, manifest=manifest, rows=1,
    )
    assert write_unaccounted(index, work, [outcome]) is None


def test_a_unit_that_died_leaves_its_files_in_the_list(tmp_path):
    """The failure this is actually for: a unit crashed, so its files were
    never manifested and would otherwise vanish into a subtraction."""
    from probe.cli.backfill_run import UnitOutcome, write_unaccounted
    from probe.cli.backfill_ledger import Unit

    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    _write(folder, "b.md", "y")
    index, _ = _index_walk(folder, state)
    work = tmp_path / "work"
    work.mkdir()
    dead = UnitOutcome(
        unit=Unit(unit_id="u1", project="p", paths=("a.md", "b.md")),
        ok=False, manifest=None, rows=0,
    )
    out = write_unaccounted(index, work, [dead])
    assert sorted(out.read_text().split()) == ["a.md", "b.md"]


# -- what the index refuses to record ----------------------------------------


def test_a_cancelled_run_does_not_advance_the_index(tmp_path):
    """THE SILENT DROP. Writing the index during the walk made it the record of
    the last walk rather than the last IMPORT, so a run cancelled at the
    approval prompt still advanced it -- and the next run compared the folder
    against files that were never imported, found no difference, and dropped
    everything added in between."""
    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    first = idx.Index.for_folder(folder, directory=state)
    list(first.collect(ev.walk(folder), root=folder))
    first.commit()

    _write(folder, "train_v2.py", "new work")
    cancelled = idx.Index.for_folder(folder, directory=state)
    list(cancelled.collect(ev.walk(folder), root=folder))
    # no commit(): the user cancelled at the gate

    third = idx.Index.for_folder(folder, directory=state)
    assert idx.diff(third.read(), _rows_from(ev.walk(folder), folder)).new == [
        "train_v2.py"
    ], "the new file must still read as new"


def _rows_from(records, root):
    return [
        idx.Row(path=str(Path(f.path).relative_to(root)), size=f.size, mtime=f.mtime)
        for f in records
    ]


def test_an_unmounted_drive_does_not_wipe_the_index(tmp_path):
    """Zero records is what an unreadable root and an unmounted drive both
    look like. Replacing a good index with an empty one destroys the record of
    the last real walk, after which every file reads as new."""
    folder, state = tmp_path / "f", tmp_path / "state"
    _write(folder, "a.md", "x")
    index = idx.Index.for_folder(folder, directory=state)
    list(index.collect(ev.walk(folder), root=folder))
    index.commit()
    good = index.read()
    assert good

    empty = idx.Index.for_folder(folder, directory=state)
    list(empty.collect(iter(()), root=folder))
    empty.commit()
    assert empty.read() == good, "an empty walk must not overwrite a real one"


def test_the_index_does_not_collide_with_the_ledger_glob(tmp_path):
    """`find_resumable` globs *.jsonl here and read_text()s every hit -- ~24MB
    per 200k-file index, on every resumable scan, to conclude it is not a
    ledger."""
    folder = tmp_path / "f"
    folder.mkdir()
    index = idx.Index.for_folder(folder, directory=tmp_path / "state")
    assert not index.path.name.endswith(".jsonl")
