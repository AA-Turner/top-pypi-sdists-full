"""Goldens for the outbox worker's loop (`outbox._run_leased`): given the drain reports a scripted
`drain` returns, every decision it takes -- passes, sleeps, lingers, waits for new work, the
telemetry outcome, what it prints and its exit code."""

from __future__ import annotations

import pytest

from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.outbox import outbox as outbox_module
from probe.sdk.delivery.outbox.drain.report import DrainReport, LaneStall
from probe.sdk.delivery.outbox.linger import LingerEnd
from tests.sdk.delivery.goldens.recorder import Normaliser, check


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))


def report(**fields) -> DrainReport:
    out = DrainReport()
    for name, value in fields.items():
        setattr(out, name, value)
    return out


def run_loop(tmp_path, monkeypatch, capsys, reports, *, lingers=(None,), paused_at=None, stop_at=None,
             arrived=(), status=None):
    norm = Normaliser(tmp_path)
    journal = Journal(tmp_path / "outbox")
    journal._ensure()
    log: list = []
    queue = list(reports)
    passes = {"n": 0}

    def fake_drain(j, **kwargs):
        passes["n"] += 1
        log.append(["drain", sorted(map(str, kwargs["skip_runs"] or ())), kwargs["credential_queues"]])
        return queue.pop(0) if queue else report()

    linger_answers = list(lingers)
    arrived_answers = list(arrived)
    monkeypatch.setattr("probe.sdk.delivery.outbox.drain.drain.drain", fake_drain)
    monkeypatch.setattr(outbox_module.time, "sleep", lambda s: log.append(["sleep", round(s, 2)]))
    monkeypatch.setattr(outbox_module, "_linger", lambda j, waiting: (
        log.append(["linger", waiting]), linger_answers.pop(0) if linger_answers else None)[1])
    monkeypatch.setattr(outbox_module, "_work_arrived", lambda j, fresh: (
        log.append(["arrived?"]), arrived_answers.pop(0) if arrived_answers else False)[1])
    monkeypatch.setattr(outbox_module, "_sleep_until_new_work", lambda j, seen, lanes, seconds: log.append(
        ["wait-for-work", round(seconds, 2)]))
    monkeypatch.setattr(outbox_module, "_asked_to_stop", lambda j: passes["n"] == stop_at)
    monkeypatch.setattr(Journal, "paused", property(lambda self: passes["n"] == paused_at))
    if status is not None:
        monkeypatch.setattr(Journal, "read_status", staticmethod(lambda *a, **k: dict(status)))
    import probe.analytics as telemetry

    monkeypatch.setattr(telemetry, "emit_outbox_drained", lambda **kw: log.append(
        ["telemetry", {k: ("<s>" if k == "duration_s" else v) for k, v in sorted(kw.items())}]))
    code = outbox_module._run_leased(journal)
    printed = [norm.text(line) for line in capsys.readouterr().out.splitlines()]
    return {"exit": code, "log": norm.value(log), "printed": printed}


def stalled(run: str, error: str = "ServerError: 503", **kw) -> dict:
    return {run: LaneStall(error, **kw)}


SCENARIOS = {
    "drained_then_linger_ends": dict(reports=[report(delivered=3)]),
    "linger_finds_more": dict(reports=[report(delivered=1), report(delivered=2)], lingers=[LingerEnd.WORK, None]),
    "linger_waiting": dict(reports=[report(delivered=1), report()], lingers=[LingerEnd.WAITING, None]),
    "work_arrived_on_exit": dict(reports=[report(delivered=1), report(delivered=1)], arrived=[True, False]),
    "waiting_uploads_on_exit": dict(reports=[report(), report()], status={"waiting": 1}),
    "auth_stopped": dict(reports=[report(remaining=4, queue_auth_stopped=True, auth_blocked=True)]),
    "paused_before_any_pass": dict(reports=[], paused_at=0, status={"pending": 7}),
    "paused_after_a_pass": dict(reports=[report(delivered=1, remaining=2)], paused_at=1),
    "replaced_by_newer_producer": dict(reports=[report(delivered=1, remaining=2)], stop_at=1),
    "credential_held_only": dict(reports=[report(remaining=2, credential_held=2)]),
    "held_back_until_patience_runs_out": dict(reports=[report(remaining=1, held_back=1)] * 25),
    "progress_resets_backoff": dict(reports=[
        report(remaining=2, stopped_transient=True, errors=["e1"]),
        report(remaining=1, delivered=1),
        report(remaining=1, stopped_transient=True, errors=["e2"]),
        report(remaining=0, delivered=1)]),
    "transient_backoff_grows_to_cap": dict(reports=[
        report(remaining=1, stopped_transient=True, errors=[f"e{n}"]) for n in range(12)]
        + [report(delivered=1)]),
    "transient_honours_retry_after": dict(reports=[
        report(remaining=1, stopped_transient=True, retry_after=42.0, errors=["slow"]), report(delivered=1)]),
    "lane_backoff_waits_for_new_work": dict(reports=[
        report(remaining=2, stopped_transient=True, stalled_runs=stalled("r1"), errors=["e"]),
        report(remaining=1, delivered=1),
        report(delivered=1)]),
    "unreachable_ignores_lane_wake": dict(reports=[
        report(remaining=2, stopped_transient=True, unreachable=True, stalled_runs=stalled("r1"), errors=["down"]),
        report(delivered=2)]),
    "dead_letters_counted_by_status": dict(reports=[report(dead_lettered=3, dead_letter_records=[
        {"status": 404, "no_such_run": True}, {"status": 422}, {}])]),
    "in_progress_multipart": dict(reports=[report(remaining=1, in_progress=1), report(delivered=1)]),
}


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_outbox_worker_golden(name, tmp_path, monkeypatch, capsys):
    check(f"outbox_worker/{name}", run_loop(tmp_path, monkeypatch, capsys, **SCENARIOS[name]))
