"""Plan 1.12 (client half): a training process reports its delivery counts.

Counts only, deltas since its last report, every 15 min while it writes and at
each close -- so a tenant losing data shows up in our alerts within minutes,
not in a support ticket. Never a key, body, name or path; nothing at all with
the telemetry opt-out set or on a backend that is not ours.
"""

from __future__ import annotations

import errno
import threading
import warnings

import pytest

from probe._shared import telemetry
from probe.sdk import journal as journal_mod

from tests.conftest import make_client, open_run


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TELEMETRY", raising=False)
    for var in (*journal_mod._GLOBAL_RANK_VARS, "LOCAL_RANK", "PROBE_OUTBOX_WORKER"):
        monkeypatch.delenv(var, raising=False)


class _Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


class _Sent(list):
    """What the client handed to `emit_delivery_summary`; `wait()` for its
    thread."""

    def __init__(self):
        super().__init__()
        self.done = threading.Event()
        self.timeout = 5.0

    def wait(self) -> bool:
        ok = self.done.wait(self.timeout)
        self.done.clear()
        return ok


@pytest.fixture
def sent(monkeypatch):
    calls = _Sent()

    def record(*, base_url, flush=False, **props):
        calls.append({"base_url": base_url, **props})
        calls.done.set()

    monkeypatch.setattr(telemetry, "emit_delivery_summary", record)
    return calls


def _client(app, tmp_path):
    clock = _Clock()
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    client._notices.clock = clock
    client._notice_polled_at = client._reported_at = clock.now
    return client, clock


def test_a_close_reports_counts_only(app, tmp_path, monkeypatch, sent):
    client, _ = _client(app, tmp_path)
    run = open_run(client, experiment="report")
    for step in range(3):
        run.log({"loss": float(step)}, step=step)

    def refuse(*a, **kw):
        raise OSError(errno.EROFS, "Read-only file system")

    monkeypatch.setattr(client.journal, "append_http", refuse)
    run.log({"loss": 9.0}, step=3)  # dropped
    run.finish(flush_timeout=0)
    assert sent.wait()
    (report,) = sent
    assert report["final"] is True
    assert report["attempted"] >= 4 and report["dropped"] >= 1
    values = [v for k, v in report.items() if k != "base_url"]
    assert all(v is None or isinstance(v, (bool, int, float, dict)) for v in values), report
    assert run.id not in repr(report) and "metrics" not in repr(report), "no names, no paths"
    client.close()


def test_reports_carry_deltas_and_skip_quiet_intervals(app, tmp_path, sent):
    client, clock = _client(app, tmp_path)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    clock.now += 901
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert sent.wait()
    assert sent[-1]["attempted"] == 2 and sent[-1]["final"] is False

    clock.now += 901
    client._poll_delivery()  # nothing written since: nothing to say
    assert len(sent) == 1

    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    clock.now += 901
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    assert sent.wait()
    assert sent[-1]["attempted"] == 2, "a delta, not the running total"
    client.close()


def test_the_event_takes_counts_and_nothing_else(monkeypatch):
    puts: list = []

    class _Sender:
        def put(self, record):
            puts.append(record)

    monkeypatch.setattr(telemetry, "_ensure_sender", lambda: _Sender())
    telemetry.emit_delivery_summary(
        base_url="https://api.research.prbe.ai", attempted=3, path="/v1/runs/r-1/metrics"
    )
    (record,) = puts
    assert record["event"] == telemetry.EVENT_DELIVERY_SUMMARY
    assert record["properties"]["attempted"] == 3
    assert "path" not in record["properties"]


@pytest.mark.parametrize(
    ("setting", "base_url"),
    [("off", "https://api.research.prbe.ai"), (None, "https://probe.example.edu")],
    ids=["opted-out", "self-hosted"],
)
def test_opted_out_or_self_hosted_sends_nothing(monkeypatch, setting, base_url):
    if setting:
        monkeypatch.setenv("PROBE_TELEMETRY", setting)
    puts: list = []

    class _Sender:
        def put(self, record):
            puts.append(record)

    monkeypatch.setattr(telemetry, "_ensure_sender", lambda: _Sender())
    telemetry.emit_delivery_summary(base_url=base_url, attempted=3)
    assert puts == []


def test_a_report_cannot_raise_under_W_error(app, tmp_path, monkeypatch):
    client, _ = _client(app, tmp_path)

    def broken(**kw):
        raise RuntimeError("telemetry down")

    monkeypatch.setattr(telemetry, "emit_delivery_summary", broken)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        client._report_delivery(final=True)
    client.close()


def test_an_offline_client_reports_nothing(app, tmp_path, sent):
    """Plan 2.12: an offline run touches no network, telemetry included."""
    client, _ = _client(app, tmp_path)
    client._drains_by_hand = True
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    client._report_delivery(final=True)
    sent.timeout = 0.5
    assert not sent.wait() and list(sent) == []
    client.close()



# -- review of #2056: the close's report leaves the process ------------------------


class _FakePostHog:
    """A local PostHog: records every batch it is sent."""

    def __init__(self):
        import json as _json
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        self.batches: list = []
        outer = self

        class H(BaseHTTPRequestHandler):
            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0)
                try:
                    outer.batches.append(_json.loads(self.rfile.read(n)))
                except ValueError:
                    pass
                self.send_response(200)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"{}")

            def log_message(self, *a):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.server.daemon_threads = True
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def summaries(self) -> list[dict]:
        return [
            e
            for batch in self.batches
            for e in (batch.get("batch") or [])
            if e.get("event") == telemetry.EVENT_DELIVERY_SUMMARY
        ]

    def close(self):
        self.server.shutdown()
        self.server.server_close()


_PRELUDE = """
from probe.sdk import _telemetry_core as core
assert core.POSTHOG_HOST.startswith("http://127.0.0.1"), core.POSTHOG_HOST  # never real PostHog
core.hosted_base_url = lambda *_a, **_k: True  # the fake API is not *.prbe.ai
import probe
"""

_BODIES = {
    "explicit_finish": """
run = probe.init(experiment="e1", name="r1")
run.log({"loss": 1.0}, step=0)
run.finish()
""",
    "with_block": """
with probe.init(experiment="e1", name="r1") as run:
    run.log({"loss": 1.0}, step=0)
""",
    "atexit_auto_close": """
run = probe.init(experiment="e1", name="r1")
run.log({"loss": 1.0}, step=0)
""",
}


def _run_child(app, posthog, body, **extra):
    import subprocess
    import sys

    from tests.served_fake_app import child_env, serve

    with serve(app) as url:
        env = child_env(url, PROBE_TELEMETRY_HOST=posthog.url, **extra)
        env.pop("PROBE_TELEMETRY", None)
        proc = subprocess.run(
            [sys.executable, "-c", _PRELUDE + body],
            env=env, capture_output=True, text=True, timeout=120,
        )
    return proc


@pytest.mark.parametrize("path", list(_BODIES))
def test_a_real_process_sends_its_close_report(app, path):
    """Review of #2056 (P1): the close's report went out from a daemon thread
    the interpreter shut down under: 0 of 3 real processes delivered it on any
    exit path. It is handed to the sender on the calling thread now."""
    app.seed_experiment("e1")
    posthog = _FakePostHog()
    try:
        proc = _run_child(app, posthog, _BODIES[path])
        assert proc.returncode == 0, proc.stderr[-3000:]
        finals = [e for e in posthog.summaries() if e["properties"].get("final")]
        assert len(finals) == 1, (path, posthog.summaries(), proc.stderr[-2000:])
        assert finals[0]["properties"]["attempted"] >= 1
    finally:
        posthog.close()


def test_a_disabled_run_reports_nothing(app):
    """`PROBE_MODE=disabled` (plan 2.5): nothing is recorded, nothing is sent."""
    app.seed_experiment("e1")
    posthog = _FakePostHog()
    try:
        proc = _run_child(app, posthog, _BODIES["explicit_finish"], PROBE_MODE="disabled")
        assert proc.returncode == 0, proc.stderr[-3000:]
        assert posthog.summaries() == []
    finally:
        posthog.close()


def test_the_close_report_counts_dead_letters_the_poll_had_not_seen(app, tmp_path, sent):
    """Review of #2056 (P1): the close's report used the last 15 s poll, so
    writes dead-lettered since read as 0. It re-reads the outbox first."""
    client, _ = _client(app, tmp_path)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    journal = client.journal
    (journal.failed_dir / "000000000009-1-dead1.json").write_text("{}")
    journal._write_status_locked(
        recount=False,
        new_dead_letters=[{"run_ref": "r-1", "op_id": "dead1", "error": "422", "status": 422}],
    )
    client._report_delivery(final=True)
    (report,) = sent
    assert report["dead_lettered"] == 1 and report["dead_lettered_by_status"] == {"422": 1}
    client.close()


def test_the_close_report_counts_a_refused_credential_as_auth_blocked(app, tmp_path, sent):
    """Since #2041 a refused credential's writes are set aside by fingerprint
    and the queue-wide `auth_blocked_since` stays empty for stamped writes;
    the report's `auth_blocked_s` read only that, so a job whose token was
    revoked reported no auth block."""
    import json
    from datetime import datetime, timedelta, timezone

    client, _ = _client(app, tmp_path)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    fingerprint = sorted(client._credential_fingerprints)[0]
    since = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
    status = json.loads(client.journal.status_file.read_text())
    status["refused_fingerprints"] = {fingerprint: since, "someone-else": since}
    client.journal.status_file.write_text(json.dumps(status))
    client._report_delivery(final=True)
    (report,) = sent
    assert report["auth_blocked_s"] is not None and report["auth_blocked_s"] >= 120, report
    client.close()


def test_the_auth_gauge_counts_from_the_first_refusal(app, tmp_path, sent):
    """The drain restamps a refusal at every retry: read from the latest
    stamp, `auth_blocked_s` never passed 300 s."""
    import json
    from datetime import datetime, timedelta, timezone

    client, clock = _client(app, tmp_path)
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})
    fingerprint = sorted(client._credential_fingerprints)[0]

    def refused(minutes_ago):
        at = (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat()
        status = json.loads(client.journal.status_file.read_text())
        status["refused_fingerprints"] = {fingerprint: at}
        client.journal.status_file.write_text(json.dumps(status))

    refused(30)
    clock.now += 16
    client.write("POST", "/v1/runs/r-1/metrics", {"points": []})  # the poll sees it
    refused(1)  # a later retry restamps it
    client._report_delivery(final=True)
    report = sent[-1]
    assert report["auth_blocked_s"] >= 30 * 60, report
    client.close()
