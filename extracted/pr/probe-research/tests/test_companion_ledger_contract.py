"""The daemon's ledger is written by the tap worker and read by `probe companion`.

The CLI reads the SQLite file directly, so the two must agree on the format
version and the tables the reader touches. This writes a ledger with the tap's
own module and reads it with the CLI's reader.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from probe.cli import companion

TAP_ROOT = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
SID = "11111111-2222-3333-4444-555555555555"
RUN = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


@pytest.fixture
def ledger_mod(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    spec = importlib.util.spec_from_file_location(
        "_tap_companion_ledger", TAP_ROOT / "tap" / "companion_ledger.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["_tap_companion_ledger"] = module
    spec.loader.exec_module(module)
    yield module
    sys.modules.pop("_tap_companion_ledger", None)


def test_the_cli_knows_the_workers_format(ledger_mod):
    assert ledger_mod.LEDGER_VERSION in companion.KNOWN_LEDGER_VERSIONS
    assert ledger_mod.ledger_path(SID) == companion.ledger_path(SID)


def test_the_cli_reads_what_the_worker_wrote(ledger_mod):
    ledger = ledger_mod.Ledger(SID)
    ledger.record_boundary(byte_offset=10, from_writer="agent", to_writer="daemon", reason="daemon")
    cycle = ledger.start_cycle(byte_start=10, byte_end=90, events=4)
    ledger.add_proposal(
        idem_key="k1", cycle=cycle, kind="note", target_type="run", target_id=RUN,
        payload={"title": "companion: plateau", "body": "0.41"},
        evidence={"from": 20, "to": 80, "why": "loss flat", "_op": ["POST", "/x", {}]},
        status="published",
    )
    ledger.add_proposal(
        idem_key="k2", cycle=cycle, kind="edge", target_type="run", target_id=RUN,
        payload={}, evidence={}, status="held", reason="edge source was never seen in this session",
    )
    ledger.finish_cycle(cycle, outcome="2 decided", input_tokens=100, output_tokens=20)
    ledger.set_watermark(90)
    ledger.close()

    conn = companion.open_ledger(SID)
    log = companion.read_log(conn)
    assert [d["status"] for d in log] == ["published", "held"]
    assert "_op" not in log[0]["evidence"]
    report = companion.read_report(conn)
    assert report["writer_now"] == "daemon"
    assert report["decided_through_offset"] == 90
    assert report["published_by_kind"] == {"note": 1}
    assert report["tokens"] == {"input": 100, "output": 20}
    conn.close()


def test_an_unknown_format_is_refused_not_guessed(ledger_mod):
    ledger = ledger_mod.Ledger(SID)
    ledger._set_meta("format_version", "99")
    ledger.close()
    with pytest.raises(companion.LedgerUnreadable, match="upgrade the CLI"):
        companion.open_ledger(SID)


def test_feedback_lands_where_the_worker_reads_it(ledger_mod, monkeypatch, capsys):
    ledger = ledger_mod.Ledger(SID)
    ledger.add_proposal(
        idem_key="k1", cycle=1, kind="note", target_type="run", target_id=RUN,
        payload={"title": "t"}, evidence={}, status="published",
    )
    ledger.close()
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    companion.feedback_cmd(decision=1, wrong=True, noise=False, note="not what happened", session=SID)
    ledger = ledger_mod.Ledger(SID)
    assert [f["verdict"] for f in ledger.unconsumed_feedback()] == ["wrong"]
    ledger.close()


def test_doctor_reads_what_the_workers_spend_file_holds(ledger_mod):
    spend = ledger_mod.DeviceSpend()
    spend.add(1234)
    spend.close()
    assert companion.tokens_today() == 1234


def test_a_file_that_is_not_a_ledger_is_refused_cleanly(ledger_mod):
    path = companion.ledger_path(SID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"not a database at all" * 100)
    with pytest.raises(companion.LedgerUnreadable):
        companion.open_ledger(SID)


def test_log_and_report_run_as_commands(ledger_mod, monkeypatch):
    from typer.testing import CliRunner

    import importlib

    main = importlib.import_module("probe.cli.main")
    ledger = ledger_mod.Ledger(SID)
    ledger.add_proposal(
        idem_key="k1", cycle=1, kind="note", target_type="run", target_id=RUN,
        payload={"title": "t"}, evidence={}, status="held", reason="shadow",
    )
    ledger.close()
    runner = CliRunner()
    out = runner.invoke(main.app, ["companion", "log", SID, "--status", "held"])
    assert out.exit_code == 0, out.output
    assert '"reason": "shadow"' in out.output or '"reason":"shadow"' in out.output
    out = runner.invoke(main.app, ["companion", "report", SID])
    assert out.exit_code == 0, out.output
    out = runner.invoke(main.app, ["companion", "log", "22222222-3333-4444-5555-666666666666"])
    assert out.exit_code == 1


def test_the_cli_prints_the_exact_rounds_the_worker_traced(ledger_mod):
    ledger = ledger_mod.Ledger(SID)
    cycle = ledger.start_cycle(byte_start=0, byte_end=90, events=2)
    request = [{"role": "system", "content": "FRAMING"}, {"role": "user", "content": "NEW TRANSCRIPT\n[assistant @5]\nx"}]
    ledger.add_trace(cycle=cycle, round=0, request=request, error="Retryable: 503 down")
    ledger.add_trace(cycle=cycle, round=1, request=request, response={"content": '{"proposals": []}'})
    ledger.close()

    conn = companion.open_ledger(SID)
    rounds = companion.read_trace(conn, cycle)
    conn.close()
    assert [r["round"] for r in rounds] == [0, 1]
    assert rounds[0]["request"] == request and rounds[0]["error"].startswith("Retryable")
    assert rounds[1]["response"] == {"content": '{"proposals": []}'}


def test_a_ledger_from_an_older_worker_gains_the_new_tables_and_every_reader_still_reads_it(ledger_mod):
    import sqlite3

    ledger = ledger_mod.Ledger(SID)
    ledger.set_watermark(42)
    ledger.conn.execute("DROP TABLE traces")
    ledger.conn.execute("DROP TABLE judgments")
    ledger.close()
    conn = companion.open_ledger(SID)  # the CLI reads a ledger without the new tables
    assert companion.read_trace(conn, 1) == []
    conn.close()
    reopened = ledger_mod.Ledger(SID)
    assert reopened.watermark == 42
    # Additive tables keep the format: a released CLI and an older tap still open it.
    assert reopened.conn.execute("SELECT value FROM meta WHERE key = 'format_version'").fetchone()[0] == "1"
    reopened.close()
    assert sqlite3.connect(str(ledger_mod.ledger_path(SID))).execute("SELECT COUNT(*) FROM traces").fetchone() == (0,)


def test_traces_are_bounded_by_size_oldest_first(ledger_mod, monkeypatch):
    import os

    monkeypatch.setattr(ledger_mod, "TRACE_KEEP_BYTES", 4000)
    ledger = ledger_mod.Ledger(SID)
    for i in range(10):
        ledger.add_trace(cycle=i, round=0, request=[{"role": "user", "content": os.urandom(600).hex()}])
    kept = [r[0] for r in ledger.conn.execute("SELECT cycle FROM traces ORDER BY id")]
    assert kept and kept[-1] == 9 and kept[0] > 0
    assert ledger.conn.execute("SELECT SUM(bytes) FROM traces").fetchone()[0] <= 4000
    ledger.close()


def test_the_cli_names_the_workers_trace_retention(ledger_mod):
    assert companion.TRACE_KEEP_DAYS * 24 * 3600 == ledger_mod.TRACE_KEEP_SECONDS
    assert companion.TRACE_KEEP_MB * 1024 * 1024 == ledger_mod.TRACE_KEEP_BYTES


def test_trace_runs_as_a_command_listing_cycles_and_printing_one(ledger_mod):
    import importlib
    import json

    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")
    ledger = ledger_mod.Ledger(SID)
    decided = ledger.start_cycle(byte_start=0, byte_end=90, events=2)
    ledger.finish_cycle(decided, outcome="1 decided", input_tokens=10, output_tokens=2)
    refused = ledger.start_cycle(byte_start=90, byte_end=200, events=3)
    ledger.finish_cycle(refused, outcome="skipped: gateway refused (422)")
    ledger.add_trace(cycle=refused, round=0, request=[{"role": "user", "content": "x"}], error="Rejected: 422")
    ledger.close()
    runner = CliRunner()
    out = runner.invoke(main.app, ["companion", "trace", "--session", SID])
    assert out.exit_code == 0, out.output
    cycles = json.loads(out.output)["cycles"]
    # A cycle that decided nothing is listed too: it is the one a trace is for.
    assert [(c["cycle"], c["outcome"], c["traced_rounds"]) for c in cycles] == [
        (decided, "1 decided", 0), (refused, "skipped: gateway refused (422)", 1)]
    out = runner.invoke(main.app, ["companion", "trace", str(refused), "--session", SID])
    assert out.exit_code == 0, out.output
    assert json.loads(out.output)["rounds"][0]["error"] == "Rejected: 422"
    out = runner.invoke(main.app, ["companion", "trace", "999", "--session", SID])
    assert out.exit_code == 1 and "no trace for cycle 999" in out.output
