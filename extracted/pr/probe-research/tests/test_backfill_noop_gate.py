"""Skipping the work needs BOTH halves: folder unchanged AND import finished.

The walk alone is not enough. A run that crashed halfway leaves the folder
identical and the import incomplete, and skipping on the walk alone reports a
half-finished import as done -- the exact silent drop the index was added to
make impossible.
"""

from __future__ import annotations

from pathlib import Path

from probe.cli import backfill_index as idx
from probe.cli import backfill_ledger as ledger_mod
from probe.cli.backfill_ledger import Unit


def _rows(*paths):
    return [idx.Row(path=p, size=1, mtime=100.0) for p in paths]


def _closed_ledger(tmp_path: Path) -> ledger_mod.Ledger:
    """A ledger whose import ran to completion and was delivered."""
    ledger = ledger_mod.Ledger(tmp_path / "l.jsonl")
    unit = Unit(unit_id="u1", project="p", paths=("a.md",))
    ledger.record_plan([unit], ["p"])
    ledger.record_approval()
    ledger.start_unit("u1")
    ledger.finish_unit("u1", ok=True, enqueued=1)
    ledger.record_enqueued("u1", 1)
    return ledger


def test_an_unchanged_folder_after_a_finished_import_is_a_no_op(tmp_path):
    state = _closed_ledger(tmp_path).read()
    delta = idx.diff(_rows("a.md"), _rows("a.md"))
    assert delta.quiet
    assert state.planned and not state.outstanding() and not state.unenqueued()


def test_an_unchanged_folder_after_a_CRASH_is_not_a_no_op(tmp_path):
    """The case the walk alone gets wrong."""
    ledger = ledger_mod.Ledger(tmp_path / "l.jsonl")
    unit = Unit(unit_id="u1", project="p", paths=("a.md",))
    ledger.record_plan([unit], ["p"])
    ledger.record_approval()
    ledger.start_unit("u1")  # started, never finished: the crash signal
    state = ledger.read()
    assert idx.diff(_rows("a.md"), _rows("a.md")).quiet, "the folder IS unchanged"
    assert state.outstanding(), "but the import is not finished, so do not skip"


def test_an_unchanged_folder_with_a_lost_enqueue_is_not_a_no_op(tmp_path):
    """Units done, manifests written, nothing delivered. Skipping here strands
    the whole folder in the state the recovery path exists to fix."""
    ledger = ledger_mod.Ledger(tmp_path / "l.jsonl")
    unit = Unit(unit_id="u1", project="p", paths=("a.md",))
    ledger.record_plan([unit], ["p"])
    ledger.record_approval()
    ledger.start_unit("u1")
    ledger.finish_unit("u1", ok=True, enqueued=1)
    state = ledger.read()
    assert idx.diff(_rows("a.md"), _rows("a.md")).quiet
    assert state.unenqueued(), "delivery never happened, so do not skip"


def test_a_changed_folder_is_never_a_no_op(tmp_path):
    state = _closed_ledger(tmp_path).read()
    assert not state.outstanding()
    assert not idx.diff(_rows("a.md"), _rows("a.md", "b.md")).quiet


def test_a_first_run_has_no_previous_index_and_is_never_a_no_op():
    """`previous` empty means we have never walked this folder. An empty diff
    against nothing must not read as "unchanged"."""
    assert idx.diff([], _rows("a.md")).new == ["a.md"]


def test_a_net_zero_change_is_not_unchanged():
    """The bug the index digest fixes, and it was pre-existing.

    The gate compared the census COUNT and total BYTES. One file added and
    another deleted nets to the same count, and an edit can preserve the total
    size -- so a folder that genuinely moved on reported "nothing has changed
    on disk" and the new file was never imported. The comment above that gate
    used to concede the gap and defer "a real path/size/mtime digest" to
    TODOS; the index is that digest."""
    before = _rows("keep.md", "gone.md")
    after = _rows("keep.md", "added.md")
    assert len(before) == len(after), "the count is identical, which is the trap"
    delta = idx.diff(before, after)
    assert not delta.quiet
    assert delta.new == ["added.md"] and delta.vanished == ["gone.md"]


def test_an_in_place_edit_that_preserves_size_is_still_a_change():
    """Same path, same byte count, different mtime. Bytes alone missed it."""
    before = [idx.Row(path="a.md", size=10, mtime=100.0)]
    after = [idx.Row(path="a.md", size=10, mtime=900.0)]
    assert idx.diff(before, after).changed == ["a.md"]


def test_the_diff_uses_current_content_and_only_classifies_new_files(tmp_path, monkeypatch):
    """A committed old stat index cannot make the current census a no-op."""
    from test_backfill_scoped_orchestration import make_harness

    h = make_harness(tmp_path, monkeypatch)
    h.run()
    h.drain()
    h.run()
    assert h.report()["delivered"] == ["a.py"]
    (h.folder / "new.md").write_text("new evidence")
    h.run()
    assert h.classified == [["a.py"], ["new.md"]]
    assert h.report()["delivered"] == ["a.py"]
    assert h.report()["queued"] == ["new.md"]
