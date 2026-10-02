"""A unit that fails every attempt is reported, not retried forever.

`attempts` was counted in the ledger and never read, so a unit that failed the
same way on every run was re-queued indefinitely and the import could never
report complete. These pin what replaced that: a cap, a terminal state, and one
explicit way back.
"""

from __future__ import annotations

import pytest

from probe.cli import backfill_ledger as ledger_mod
from probe.cli.backfill_ledger import Ledger, MAX_UNIT_ATTEMPTS, Unit, UnitState

from test_backfill_scoped_orchestration import Harness  # noqa: F401 -- fixture source


@pytest.fixture
def h(tmp_path, monkeypatch):
    return Harness(tmp_path, monkeypatch)


def _ledger(tmp_path, unit_id="u1", paths=("a.py",)):
    ledger = Ledger(tmp_path / "units.jsonl")
    ledger.open_import(tmp_path, files=len(paths), bytes_=1)
    ledger.record_plan([Unit(unit_id, "project", tuple(paths))], ["project"])
    ledger.record_approval()
    return ledger


def test_a_unit_is_offered_again_until_its_attempts_run_out(tmp_path):
    ledger = _ledger(tmp_path)
    for attempt in range(MAX_UNIT_ATTEMPTS - 1):
        ledger.start_unit("u1")
        ledger.finish_unit("u1", ok=False, error="the agent never answered")
        state = ledger.read()
        assert state.outstanding(), f"still retryable after {attempt + 1} attempts"
        assert not state.exhausted()


def test_the_last_failure_makes_it_exhausted(tmp_path):
    ledger = _ledger(tmp_path)
    for _ in range(MAX_UNIT_ATTEMPTS):
        ledger.start_unit("u1")
        ledger.finish_unit("u1", ok=False, error="the agent never answered")
    state = ledger.read()
    assert [r.unit.unit_id for r in state.exhausted()] == ["u1"]
    assert state.units["u1"].attempts == MAX_UNIT_ATTEMPTS


def test_retiring_it_takes_it_out_of_the_resume_set(tmp_path):
    ledger = _ledger(tmp_path)
    for _ in range(MAX_UNIT_ATTEMPTS):
        ledger.start_unit("u1")
        ledger.finish_unit("u1", ok=False, error="boom")
    ledger.retire_unit("u1", reason="u1: boom")
    state = ledger.read()
    assert state.outstanding() == []
    assert [r.unit.unit_id for r in state.dead()] == ["u1"]
    assert state.units["u1"].state is UnitState.DEAD
    assert "boom" in state.units["u1"].error


def test_the_reason_survives_being_read_back_from_disk(tmp_path):
    ledger = _ledger(tmp_path)
    ledger.start_unit("u1")
    ledger.finish_unit("u1", ok=False, error="cannot open weights.pt")
    ledger.retire_unit("u1", reason="u1: cannot open weights.pt")
    reopened = Ledger(tmp_path / "units.jsonl").read()
    assert "weights.pt" in reopened.units["u1"].error


def test_a_dead_unit_never_asks_to_be_enqueued(tmp_path):
    ledger = _ledger(tmp_path)
    ledger.start_unit("u1")
    ledger.finish_unit("u1", ok=True, enqueued=3)
    ledger.retire_unit("u1", reason="u1: gave up")
    assert ledger.read().unenqueued() == []


def test_the_cap_is_a_module_constant_not_a_literal():
    """So the ledger, the import and the report cannot disagree about it."""
    assert isinstance(ledger_mod.MAX_UNIT_ATTEMPTS, int)
    assert ledger_mod.MAX_UNIT_ATTEMPTS >= 2


# -- the wiring the import uses ----------------------------------------------


def test_retirement_marks_exactly_the_files_that_never_landed(tmp_path, monkeypatch):
    """What `_deliver_approved` does when a unit runs out of attempts.

    Driven directly rather than through a folder run: the harness cannot
    produce a genuinely exhausted unit, because a unit that reports failure
    still leaves a manifest and its files still land. That is correct, and it
    means the interesting case is the one where no manifest was ever written.
    """
    from probe.cli.backfill_coverage import Coverage, Scope

    folder = tmp_path / "folder"
    folder.mkdir()
    for name in ("landed.py", "lost.py"):
        (folder / name).write_text(f"# {name}\n")
    scope = Scope("https://test.invalid", "tenant", "workspace", None)
    project = {"id": "p1", "slug": "project", "customer_id": "tenant", "workspace_id": "workspace"}

    ledger = _ledger(tmp_path, paths=("landed.py", "lost.py"))
    for _ in range(MAX_UNIT_ATTEMPTS):
        ledger.start_unit("u1")
        ledger.finish_unit("u1", ok=False, error="the agent never answered")

    store = Coverage.for_folder(folder, scope, directory=tmp_path / "state")
    with store.writer() as state:
        state.observe(folder, ["landed.py", "lost.py"])
        state.approve({"landed.py": project, "lost.py": project})
        row = next(r for r in state.rows() if r["path"] == "landed.py")
        intent = state.intend(row, reference=False)
        state.accept_receipt(intent["correlation"], {
            "correlation": intent["correlation"], "state": "delivered", "status": "complete",
            "artifact_id": "a1", "anchor": "project", "anchor_id": "p1",
            "name": "landed.py", "content_hash": intent["content_hash"],
            "size_bytes": intent["size_bytes"], "is_reference": False,
            "uri": None, "readable": True,
        })

        # The retirement loop, exactly as the import runs it.
        retired = []
        for record in ledger.read().exhausted():
            reason = f"{record.unit.unit_id}: {record.error}"
            ledger.retire_unit(record.unit.unit_id, reason=reason)
            retired.extend(state.mark_dead(record.unit.paths, reason))

        assert retired == ["lost.py"], "a delivered file must never be marked dead"
        report = state.report()
        assert report["delivered"] == ["landed.py"]
        assert report["dead"] == ["lost.py"]
        assert report["new"] == [], "a dead file must not read as never-seen work"
        assert ledger.read().outstanding() == []

        # And the one way back.
        assert state.clear_dead(["lost.py"]) == 1
        assert state.report()["dead"] == []


def test_the_report_tells_the_reader_how_to_get_them_back(tmp_path):
    from probe.cli import backfill_delivery as delivery
    from probe.cli.backfill_coverage import Coverage, Scope

    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "lost.py").write_text("x = 1\n")
    scope = Scope("https://test.invalid", "tenant", "workspace", None)
    project = {"id": "p1", "slug": "project", "customer_id": "tenant", "workspace_id": "workspace"}
    store = Coverage.for_folder(folder, scope, directory=tmp_path / "state")
    with store.writer() as state:
        state.observe(folder, ["lost.py"])
        state.approve({"lost.py": project})
        state.mark_dead(["lost.py"], "u1: the agent never answered")
        lines = delivery.lines(state)
    joined = "\n".join(lines)
    assert "failed every attempt" in joined
    assert "--retry-dead" in joined
