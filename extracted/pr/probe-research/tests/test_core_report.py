"""`probe.core.report`: one diagnostic report to the Probe team, sent once.

Real boundaries: the `python -I -m probe.core.run report` child the Probe
service runs, a real HTTP server standing in for the API (`Stub`), the state
files on disk. What it protects: no credential, home folder, login or other
account's session leaves the machine; the gate and the dedupe hold for every
automatic report; each server answer maps to the contract's word; the
`report` read's params and answer are exactly what the service (PR 2b) sends
and reads. What it does not claim: what the real server accepts.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from typer.testing import CliRunner

from probe.core import report, requests
from probe.core.requests import ActionName, ReportRequest, RequestError

SID = "11111111-2222-4333-8444-555555555555"
OTHER_SID = "99999999-8888-4777-8666-555555555555"
#: Planted credentials, each in a different place; none may leave.
CLI_TOKEN = "probe_pat_" + "c1" * 16
DAEMON_KEY = "probe_pat_" + "d2" * 16
GITHUB_TOKEN = "ghp_" + "Z9y8X7w6V5u4T3s2R1q0" + "AbCdEfGhIjKlMnOp"


# ---------------------------------------------------------------------------
# A real HTTP server standing in for the API
# ---------------------------------------------------------------------------


class Stub:
    """Records every request; answers from `routes` ((method, path) -> callable
    or (status, body, headers))."""

    def __init__(self) -> None:
        self.requests: list[dict] = []
        self.routes: dict[tuple[str, str], object] = {}
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args) -> None:
                pass

            def _serve(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                seen = {"method": self.command, "path": self.path, "headers": dict(self.headers), "body": body}
                stub.requests.append(seen)
                answer = stub.routes.get((self.command, self.path))
                if callable(answer):
                    answer = answer(seen)
                status, payload, headers = answer if answer else (404, {"detail": "not found"}, {})
                data = json.dumps(payload).encode()
                self.send_response(status)
                for name, value in (headers or {}).items():
                    self.send_header(name, value)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            do_GET = do_POST = do_PUT = _serve

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def bodies(self, path: str) -> list[dict]:
        return [json.loads(r["body"]) for r in self.requests if r["path"] == path and r["body"]]

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def stub():
    server = Stub()
    yield server
    server.close()


def _closed_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture
def machine(monkeypatch, stub):
    """A signed-in machine (CLI token and daemon key) pointed at the stub, whose
    backend counts as Probe's hosted service (the gate's last check)."""
    from probe.sdk.config import save_context

    monkeypatch.setenv("PROBE_BASE_URL", stub.url)
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    save_context({"base_url": stub.url, "token": CLI_TOKEN, "companion_token": DAEMON_KEY})
    import probe.sdk._telemetry_core as core

    monkeypatch.setattr(core, "hosted_base_url", lambda url: True)
    # Room for a loaded machine: the tests of the budget set their own.
    monkeypatch.setattr(report, "STAFF_SOURCE_BUDGET_S", 30.0)
    return stub


def _accept(stub: Stub, report_id: str = "7f3c9a2e-1111-4222-8333-444455556666") -> str:
    stub.routes[("POST", report.ROUTE)] = (201, {"id": report_id}, {})
    return report_id


def _state() -> Path:
    return report.state_root()


def _bind(sid: str, key: str = DAEMON_KEY, url: str | None = None) -> None:
    """The session's daemon trace folder, recorded under this server and key."""
    folder = _state() / "daemon" / "sessions" / sid
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "meta.json").write_text(json.dumps({
        "base_url": (url or report.base_url()).rstrip("/"),
        "key": hashlib.sha256(key.encode()).hexdigest()[:16],
    }))


def _service_dir() -> Path:
    from probe.service import paths

    folder = paths.service_dir()
    folder.mkdir(parents=True, exist_ok=True)
    return folder


# ---------------------------------------------------------------------------
# The `report` read: params and answer, exactly as the contract says
# ---------------------------------------------------------------------------


def test_the_report_reads_params_are_the_contracts():
    request = requests.parse(ActionName.REPORT, {
        "auto": True, "family": "worker", "reason": "gave_up_exit_3", "sid": SID,
        "env": {"PROBE_TELEMETRY": "on"}, "facts": {"exits": [3, 3]},
    })
    assert request == ReportRequest(family="worker", reason="gave_up_exit_3", auto=True, sid=SID,
                                    env={"PROBE_TELEMETRY": "on"}, facts={"exits": [3, 3]})
    # Defaults: an automatic machine report with no facts.
    bare = requests.parse(ActionName.REPORT, {"family": "service_crash", "reason": "unclean_exit", "sid": None})
    assert (bare.auto, bare.sid, bare.env, bare.facts) == (True, None, {}, {})
    # PR 2b sends these six fields and no others.
    assert set(requests._FIELDS[ActionName.REPORT]) == {"auto", "family", "reason", "sid", "env", "facts"}
    # A report is a read: never one of the service's actions.
    from probe.service.protocol import ACTIONS

    assert ActionName.REPORT.value not in {str(a) for a in ACTIONS}


@pytest.mark.parametrize("payload", [
    {"family": "worker"},  # no reason
    {"family": "Worker!", "reason": "x"},  # not a slug
    {"family": "worker", "reason": "x", "sid": "not-a-uuid"},
    {"family": "worker", "reason": "x", "sid": 7},
    {"family": "worker", "reason": "x", "auto": "true"},
    {"family": "worker", "reason": "x", "env": {"PROBE_TELEMETRY": 0}},
    {"family": "worker", "reason": "x", "env": []},
    {"family": "worker", "reason": "x", "facts": {"tb": "x" * (64 * 1024)}},
    {"family": "worker", "reason": "x", "extra": 1},
], ids=["no-reason", "bad-slug", "bad-sid", "int-sid", "string-auto", "env-int", "env-list", "facts-too-big",
        "unknown-field"])
def test_the_report_read_refuses_what_it_would_have_to_guess_at(payload):
    with pytest.raises(RequestError):
        requests.parse(ActionName.REPORT, payload)


#: The source tree under test: the child imports `probe` from HERE, never from
#: whatever the venv has installed (another worktree, an older release).
_SRC = str(Path(report.__file__).resolve().parents[2])
#: `python -I -m probe.core.run report`, with the tree under test first on the path.
_RUN = "import sys; sys.path.insert(0, sys.argv.pop(1)); from probe.core.run import main; raise SystemExit(main())"


def _child(stdin: str, **env: str) -> subprocess.CompletedProcess:
    """The `report` read as the service spawns it (`-I`: isolated), running the
    source tree under test."""
    child_env = {k: v for k, v in os.environ.items() if k not in ("PROBE_TOKEN",)}
    child_env.update(env)
    return subprocess.run([sys.executable, "-I", "-c", _RUN, _SRC, "report"], input=stdin, text=True,
                          capture_output=True, env=child_env, cwd=os.environ["HOME"], timeout=120)


def test_the_child_runs_the_tree_under_test():
    probe_file = subprocess.run(
        [sys.executable, "-I", "-c", "import sys; sys.path.insert(0, sys.argv[1]); import probe; print(probe.__file__)",
         _SRC], capture_output=True, text=True, timeout=60).stdout.strip()
    assert Path(probe_file).resolve().parent == Path(report.__file__).resolve().parents[1]


def test_the_report_child_writes_one_answer_object(monkeypatch, stub):
    """What the service's `children.run_read("report", ...)` parses: stdout is
    exactly one JSON object with the contract's four keys."""
    monkeypatch.setenv("PROBE_BASE_URL", stub.url)
    done = _child(json.dumps({"family": "worker", "reason": "gave_up_exit_3", "sid": SID,
                              "env": {"PROBE_TELEMETRY": "off"}, "facts": {}}))
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout) == {"sent": False, "id": None, "skipped": "disabled:telemetry_off", "path": None}
    assert len(done.stdout.strip().splitlines()) == 1
    assert stub.requests == []  # nothing was collected, nothing was sent

    refused = _child(json.dumps({"family": "worker", "reason": "x", "bogus": True}))
    assert refused.returncode == 2


def test_the_report_child_sends_a_manual_report_and_names_its_copy(monkeypatch, stub):
    from probe.sdk.config import save_context

    monkeypatch.setenv("PROBE_BASE_URL", stub.url)
    save_context({"base_url": stub.url, "token": CLI_TOKEN})
    report_id = _accept(stub)
    done = _child(json.dumps({"auto": False, "family": "worker", "reason": "gave_up_exit_3", "sid": SID}))
    assert done.returncode == 0, done.stderr
    answer = json.loads(done.stdout)
    assert answer["sent"] is True and answer["id"] == report_id and answer["skipped"] is None
    assert Path(answer["path"]).is_file()
    (body,) = stub.bodies(report.ROUTE)
    assert body["kind"] == "manual" and body["family"] == "worker" and body["session_ids"] == [SID]


# ---------------------------------------------------------------------------
# Consent (automatic only) and dedupe
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("env", "why"), [
    ({"PROBE_TELEMETRY": "off"}, "disabled:telemetry_off"),
    ({"PROBE_DIAGNOSTICS": "off"}, "disabled:diagnostics_off"),
    # Here PROBE_DIAGNOSTICS=on does not override telemetry-off: the data goes to Probe.
    ({"PROBE_TELEMETRY": "off", "PROBE_DIAGNOSTICS": "on"}, "disabled:telemetry_off"),
])
def test_an_automatic_report_needs_the_sessions_consent(machine, env, why):
    _accept(machine)
    answer = report.send(auto=True, family="worker", reason="gave_up", sid=SID, env=env)
    assert answer.as_json() == {"sent": False, "id": None, "skipped": why, "path": None}
    assert machine.requests == []


def test_an_automatic_report_never_goes_to_a_self_hosted_server(machine, monkeypatch):
    import probe.sdk._telemetry_core as core

    monkeypatch.setattr(core, "hosted_base_url", lambda url: False)
    _accept(machine)
    assert report.send(auto=True, family="worker", reason="x", env={}).skipped == "disabled:not_hosted"
    assert machine.requests == []


def test_a_manual_report_is_the_persons_own_choice(machine):
    """`probe doctor --send`: no consent gate (telemetry off here) and no dedupe."""
    report_id = _accept(machine)
    os.environ["PROBE_TELEMETRY"] = "off"  # the suite's own default, said out loud
    first = report.send(auto=False, family=report.MANUAL_FAMILY, reason=report.MANUAL_REASON)
    second = report.send(auto=False, family=report.MANUAL_FAMILY, reason=report.MANUAL_REASON)
    assert first.sent and second.sent and first.id == report_id
    assert len(machine.bodies(report.ROUTE)) == 2


def test_one_automatic_report_per_family_and_session_per_window(machine):
    _accept(machine)
    now = time.time()
    first = report.send(auto=True, family="worker", reason="gave_up", sid=SID, env={}, now=now)
    again = report.send(auto=True, family="worker", reason="crash_loop", sid=SID, env={}, now=now + 60)
    other_session = report.send(auto=True, family="worker", reason="gave_up", sid=OTHER_SID, env={}, now=now)
    other_family = report.send(auto=True, family="recorder", reason="failing", sid=SID, env={}, now=now)
    machine_wide = report.send(auto=True, family="worker", reason="gave_up", env={}, now=now)
    later = report.send(auto=True, family="worker", reason="gave_up", sid=SID, env={},
                        now=now + report.DEDUPE_WINDOW_S)
    assert first.sent and other_session.sent and other_family.sent and machine_wide.sent and later.sent
    assert again.as_json() == {"sent": False, "id": None, "skipped": "deduped", "path": None}
    assert len(machine.bodies(report.ROUTE)) == 5


def test_the_dedupe_claim_is_atomic_across_racing_reporters(machine):
    """Two reporters for one incident: exactly one claims the window."""
    results: list[bool] = []
    barrier = threading.Barrier(8)

    def race() -> None:
        barrier.wait()
        results.append(report.claim("service_crash", "machine"))

    threads = [threading.Thread(target=race) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sorted(results) == [False] * 7 + [True]


# ---------------------------------------------------------------------------
# What the server answers -> the contract's words; the local copy either way
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("status", "headers", "skipped"), [
    (429, {"Retry-After": "120"}, "rate_limited"),
    (413, {}, "too_large"),
    (422, {}, "server"),
    (404, {}, "server"),
    (500, {}, "server"),
    (503, {}, "server"),
])
def test_every_refusal_is_final_and_keeps_the_local_copy(machine, status, headers, skipped):
    machine.routes[("POST", report.ROUTE)] = (status, {"detail": "no"}, headers)
    answer = report.send(auto=False, family="worker", reason="x")
    assert (answer.sent, answer.id, answer.skipped) == (False, None, skipped)
    # No retry loop: one request per credential that was not refused for auth.
    assert len([r for r in machine.requests if r["path"] == report.ROUTE]) == 1
    kept = json.loads(Path(answer.path).read_text())
    assert kept["outcome"]["skipped"] == skipped and kept["body"]["family"] == "worker"


@pytest.mark.parametrize(("refusal", "skipped", "window_kept"), [
    ((503, {"detail": "no"}, {}), "server", False),
    ((500, {"detail": "no"}, {}), "server", False),
    ((429, {"detail": "slow down"}, {"Retry-After": "60"}), "rate_limited", False),
    (None, "offline", False),
    ((413, {"detail": "too big"}, {}), "too_large", True),
    ((401, {"detail": "who"}, {}), "unauthorized", True),
])
def test_a_failed_automatic_send_gives_its_dedupe_window_back_when_a_retry_can_help(
    machine, monkeypatch, refusal, skipped, window_kept,
):
    """Delta review #2 (PR 2b): the stamp was claimed before the POST, so the
    Probe service's retry half an hour later answered `deduped` and the report
    was never sent. A failure a retry can fix (offline, the server, its rate
    limit) gives the window back; one it cannot (too large, refused) keeps it."""
    now = time.time() // report.DEDUPE_WINDOW_S * report.DEDUPE_WINDOW_S + 60  # both tries in one window
    if refusal is None:
        monkeypatch.setenv("PROBE_BASE_URL", f"http://127.0.0.1:{_closed_port()}")
    else:
        machine.routes[("POST", report.ROUTE)] = refusal
    first = report.send(auto=True, family="update_rejected", reason="switched_back", env={}, now=now)
    assert (first.sent, first.skipped) == (False, skipped)
    monkeypatch.setenv("PROBE_BASE_URL", machine.url)
    report_id = _accept(machine)
    retry = report.send(auto=True, family="update_rejected", reason="switched_back", env={}, now=now + 1800)
    if window_kept:
        assert retry.skipped == "deduped"
    else:
        assert retry.sent and retry.id == report_id


def test_offline_is_offline(machine, monkeypatch):
    monkeypatch.setenv("PROBE_BASE_URL", f"http://127.0.0.1:{_closed_port()}")
    answer = report.send(auto=False, family="worker", reason="x")
    assert (answer.sent, answer.skipped) == (False, "offline")
    assert Path(answer.path).is_file()


def test_the_cli_token_first_then_the_daemon_key(machine):
    def by_key(seen: dict):
        token = seen["headers"].get("Authorization", "").split()[-1]
        return (201, {"id": "a1b2c3d4-0000-4000-8000-000000000001"}, {}) if token == DAEMON_KEY else (
            401, {"detail": "invalid token"}, {})

    machine.routes[("POST", report.ROUTE)] = by_key
    answer = report.send(auto=False, family="worker", reason="x")
    assert answer.sent and answer.id == "a1b2c3d4-0000-4000-8000-000000000001"
    sent_with = [r["headers"]["Authorization"].split()[-1] for r in machine.requests]
    assert sent_with == [CLI_TOKEN, DAEMON_KEY]
    # The SDK transport's machine header rides along.
    assert all(r["headers"].get("X-Probe-Device") for r in machine.requests)


def test_refused_with_both_credentials_is_unauthorized(machine):
    machine.routes[("POST", report.ROUTE)] = (401, {"detail": "invalid token"}, {})
    assert report.send(auto=False, family="worker", reason="x").skipped == "unauthorized"
    assert len(machine.requests) == 2


def test_signed_out_is_unauthorized_without_a_request(monkeypatch, stub):
    monkeypatch.setenv("PROBE_BASE_URL", stub.url)
    assert report.send(auto=False, family="worker", reason="x").skipped == "unauthorized"
    assert stub.requests == []


def test_only_the_newest_five_copies_stay_and_they_are_private(machine):
    _accept(machine)
    for _ in range(7):
        report.send(auto=False, family="worker", reason="x")
    copies = sorted(report.reports_dir().glob("report-*.json"))
    assert len(copies) == report.KEEP_REPORTS
    if os.name == "posix":
        assert {oct(p.stat().st_mode & 0o777) for p in copies} == {"0o600"}


# ---------------------------------------------------------------------------
# What a report may carry
# ---------------------------------------------------------------------------


def _plant_logs() -> dict[str, str]:
    """Logs holding this report's session, another session, a hook host's raw
    stderr, and a credential in each."""
    home = str(Path.home())
    state = _state()
    state.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    (state / "daemon-errors.log").write_text(
        f"{stamp} session {SID}: the daemon crashed (RuntimeError: PROBE_TOKEN={CLI_TOKEN} in {home}/proj)\n"
        f"{stamp} session {OTHER_SID}: SOMEONE ELSE'S ERROR\n"
        f"2001-01-01T00:00:00 session {SID}: AN ERROR FROM LONG AGO\n"
    )
    service_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (_service_dir() / "service.log").write_text(
        f"[{service_stamp}] probe-service[42]: recorder {SID} failed: Authorization: Bearer {DAEMON_KEY}\n"
        f"[{service_stamp}] probe-service[42]: recorder {OTHER_SID} failed: ANOTHER ACCOUNT'S LINE\n"
        f"[{service_stamp}] probe-service-guard[43]: the new service started\n"
        "Traceback (most recent call last): A HOOK HOST'S RAW STDERR\n"
    )
    worker = state / "daemon" / "sessions" / SID
    worker.mkdir(parents=True, exist_ok=True)
    (worker / "worker.log").write_text(f"worker log line with {GITHUB_TOKEN}\n")
    (state / "daemon" / f"{SID}.log").write_text("worker output line\n")
    return {"home": home}


def _sent_text(stub: Stub) -> str:
    return "\n".join(r["body"].decode() for r in stub.requests if r["path"] == report.ROUTE)


def test_no_credential_home_or_other_session_leaves_in_a_session_report(machine):
    planted = _plant_logs()
    _bind(SID)
    _accept(machine)
    facts = {"api_key": "sk-live-" + "q" * 24, "traceback": f"File {planted['home']}/x.py\nghp token {GITHUB_TOKEN}"}
    answer = report.send(auto=True, family="worker", reason="gave_up", sid=SID, env={}, facts=facts)
    assert answer.sent
    sent = _sent_text(machine)
    local = Path(answer.path).read_text()
    for text in (sent, local):
        for secret in (CLI_TOKEN, DAEMON_KEY, GITHUB_TOKEN, "sk-live-" + "q" * 24):
            assert secret not in text
        assert planted["home"] not in text
        assert "SOMEONE ELSE'S ERROR" not in text and "ANOTHER ACCOUNT'S LINE" not in text
        assert "A HOOK HOST'S RAW STDERR" not in text and "AN ERROR FROM LONG AGO" not in text
    logs = json.loads(sent)["report"]["logs"]
    # The report's own lines did arrive, scrubbed: the home folder is `~`.
    assert "the daemon crashed" in logs["daemon_errors"] and "~/proj" in logs["daemon_errors"]
    assert f"recorder {SID} failed" in logs["service_log"] and "the new service started" in logs["service_log"]
    assert "worker log line" in logs["worker_log"] and "worker output line" in logs["worker_output"]


def test_another_accounts_session_is_withheld(machine):
    """A session recorded under another daemon key: its logs never leave."""
    _plant_logs()
    _bind(SID, key="probe_pat_" + "e3" * 16)
    _accept(machine)
    assert report.send(auto=True, family="worker", reason="gave_up", sid=SID, env={}).sent
    body = json.loads(_sent_text(machine))
    assert "worker_log" not in body["report"]["logs"] and "worker_output" not in body["report"]["logs"]
    assert "not recorded under this server and daemon key" in body["report"]["withheld"]
    # Its lines in the shared logs are gone too.
    assert SID not in body["report"]["logs"].get("daemon_errors", "")


def test_the_report_never_reads_a_store_or_an_approval(machine):
    """Allowlisted sources only: a daemon store and a trace sit beside the
    worker log and never reach the report."""
    _plant_logs()
    _bind(SID)
    daemon = _state() / "daemon"
    (daemon / f"{SID}.sqlite").write_bytes(b"SQLite format 3\x00 STORE CONTENT")
    (daemon / "sessions" / SID / "reader.jsonl").write_text('{"prompt": "TRACE CONTENT"}\n')
    _accept(machine)
    assert report.send(auto=False, family="worker", reason="x", sid=SID).sent
    sent = _sent_text(machine)
    assert "STORE CONTENT" not in sent and "TRACE CONTENT" not in sent


def test_a_report_is_capped_and_says_it_was_trimmed(machine, monkeypatch):
    _bind(SID)
    worker = _state() / "daemon" / "sessions" / SID
    worker.mkdir(parents=True, exist_ok=True)
    (worker / "worker.log").write_text("".join(f"line {i} {'x' * 100}\n" for i in range(2000)))
    monkeypatch.setattr(report, "REPORT_MAX_BYTES", 64 * 1024)
    _accept(machine)
    assert report.send(auto=False, family="worker", reason="x", sid=SID).sent
    body = json.loads(_sent_text(machine))
    assert len(json.dumps(body["report"]).encode()) <= 64 * 1024
    assert body["report"]["trimmed"] is True
    # The newest lines are the ones kept.
    assert "line 1999" in body["report"]["logs"]["worker_log"]


def test_the_wire_body_is_the_contracts(machine):
    _accept(machine)
    assert report.send(auto=True, family="service_crash", reason="unclean_exit", env={}).sent
    (body,) = machine.bodies(report.ROUTE)
    assert set(body) >= {"schema", "kind", "family", "reason", "cli_version", "os", "harnesses", "session_ids",
                         "report"}
    assert body["schema"] == 1 and body["kind"] == "auto"
    assert len(body["cli_version"]) <= 32 and len(body["os"]) <= 128
    assert len(body["harnesses"]) <= 8 and len(body["session_ids"]) <= 50
    assert len(json.dumps(body).encode()) <= 640 * 1024


def test_a_source_that_hangs_costs_only_itself(machine, monkeypatch):
    monkeypatch.setattr(report, "STAFF_SOURCE_BUDGET_S", 0.2)
    monkeypatch.setattr(report, "install_facts", lambda: time.sleep(5))
    _accept(machine)
    started = time.monotonic()
    assert report.send(auto=False, family="worker", reason="x").sent
    assert time.monotonic() - started < 4
    body = json.loads(_sent_text(machine))
    assert body["report"]["install"] is None
    assert body["report"]["skipped"]["install"].startswith("timed out")


# ---------------------------------------------------------------------------
# Disclosure: the doctor row and `probe doctor --send`
# ---------------------------------------------------------------------------


def test_the_doctor_row_says_on_off_and_the_last_report(machine, monkeypatch):
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    assert report.doctor_row() == "off (PROBE_TELEMETRY is off)"
    monkeypatch.delenv("PROBE_TELEMETRY")
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "off")
    assert report.doctor_row() == "off (PROBE_DIAGNOSTICS is off)"
    monkeypatch.delenv("PROBE_DIAGNOSTICS")
    assert report.doctor_row() == "on · none sent yet"
    report_id = _accept(machine)
    report.send(auto=False, family="worker", reason="x")
    assert report.doctor_row().startswith("on · last sent ") and report.doctor_row().endswith(f"({report_id})")

    from probe.cli import doctor

    assert any("Diagnostic reports" in row and report_id in row for row in doctor._daemon_rows())


def test_probe_doctor_send_prints_the_id(machine):
    import importlib

    main = importlib.import_module("probe.cli.main")
    report_id = _accept(machine)
    result = CliRunner().invoke(main.app, ["doctor", "--send"])
    assert result.exit_code == 0, result.output
    assert f"Sent diagnostic report {report_id} to the Probe team" in result.output


def test_probe_doctor_send_says_why_not_and_where_the_copy_is(machine):
    import importlib

    main = importlib.import_module("probe.cli.main")
    machine.routes[("POST", report.ROUTE)] = (429, {"detail": "slow down"}, {"Retry-After": "60"})
    result = CliRunner().invoke(main.app, ["doctor", "--send"])
    assert result.exit_code == 1
    assert "too many reports" in result.output and "A copy is at " in result.output


# ---------------------------------------------------------------------------
# daemon-errors.log (plan B7)
# ---------------------------------------------------------------------------


def test_daemon_errors_rotate_past_a_mebibyte_and_lose_their_credentials(monkeypatch):
    from probe.daemon import worker

    path = worker._state_base() / "daemon-errors.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("old line\n" * (worker.DEVICE_ERRORS_MAX_BYTES // 9 + 10))
    try:
        raise RuntimeError(f"connect failed with PROBE_TOKEN={CLI_TOKEN} in {Path.home()}/proj")
    except RuntimeError as exc:
        worker._device_error(f"session {SID}: the daemon crashed ({worker._crash_detail(exc)}); x")
    assert path.with_name("daemon-errors.log.1").stat().st_size > worker.DEVICE_ERRORS_MAX_BYTES
    line = path.read_text()
    assert line.count("\n") == 1 and "the daemon crashed (RuntimeError: " in line
    assert CLI_TOKEN not in line and str(Path.home()) not in line and "~/proj" in line


def test_the_crash_detail_is_scrubbed_before_it_is_clipped():
    from probe.daemon import worker

    # The token straddles the 300-character clip: clipped first, its tail
    # would read as a shorter, unrecognised string.
    message = "x" * 290 + " " + CLI_TOKEN
    detail = worker._crash_detail(RuntimeError(message))
    assert CLI_TOKEN[:12] not in detail


# ---------------------------------------------------------------------------
# Review of #3326: each of these failed on 1bd55e3f4
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("argv", "expected"), [
    (["/usr/local/bin/claude", "-p", "refactor the billing module for ACME"], ["claude", "-p", "<arg>"]),
    (["bash", "-c", 'probe ask "what did ACME train"'], ["bash", "-c", "<arg>"]),
    (["codex", "exec", "write the private roadmap"], ["codex", "<arg>", "<arg>"]),
    (["probe", "ask", "what did ACME train last week"], ["probe", "ask", "<arg>"]),
    (["probe", "feedback", "send", "the secret plan"], ["probe", "feedback", "<arg>", "<arg>"]),
    (["mysql", "-uroot", "-phunter2Secret", "probe_db"], ["mysql", "-u<arg>", "-p<arg>", "<arg>"]),
    (["sshpass", "-p", "hunter2", "ssh", "host"], ["sshpass", "-p", "<arg>", "<arg>", "<arg>"]),
    (["curl", "--user=me:hunter2", "https://x"], ["curl", "--user=<arg>", "<arg>"]),
    # The allow-list: harmless flags and values a diagnosis needs.
    (["/opt/py/bin/python3", "-I", "-m", "probe.core.run", "report"],
     ["python3", "-I", "-m", "probe.core.run", "report"]),
    (["python", "-m", "secret_tool", "x"], ["python", "-m", "<arg>", "<arg>"]),
    (["claude", "--model", "opus", "--version"], ["claude", "--model", "<arg>", "--version"]),
    (["claude", "--model=sonnet"], ["claude", "--model=<arg>"]),
])
def test_a_command_line_keeps_only_its_program_and_flag_names(argv, expected):
    """Prompts and inline passwords live in positional arguments and flag
    values: every one of them is replaced, whatever it looks like."""
    assert report.redact_argv(argv, report.Scope.LOCAL) == expected
    assert report.redact_argv(argv, report.Scope.STAFF) == expected


def test_an_automatic_reports_facts_lose_command_lines_and_header_values(machine):
    _accept(machine)
    facts = {"argv": ["claude", "-p", "refactor the billing module"],
             "worker": {"cmdline": ["mysql", "-phunter2Secret"]},
             "env": {"DB_PASS": "plainpass", "MYSQL_PWD": "pw2", "GH_PAT": "pat3",
                     "OTEL_EXPORTER_OTLP_HEADERS": "x-honeycomb-team=hc-value-1,x-other=two"}}
    assert report.send(auto=True, family="worker", reason="gave_up", env={}, facts=facts).sent
    sent = _sent_text(machine)
    for leaked in ("billing module", "hunter2Secret", "plainpass", "pw2", "pat3", "hc-value-1"):
        assert leaked not in sent
    kept = json.loads(sent)["report"]["facts"]
    assert kept["argv"] == ["claude", "-p", "<arg>"]
    assert kept["env"]["OTEL_EXPORTER_OTLP_HEADERS"] == "x-honeycomb-team=<redacted>,x-other=<redacted>"


@pytest.mark.parametrize("name", ["DB_PASS", "MYSQL_PWD", "GH_PAT", "DATABASE_DSN", "SSH_PRIVATE", "BEARER",
                                  "SESSION_JWT", "PASSWORD"])
def test_more_credential_names(name):
    assert report.credential_name(name)


@pytest.mark.parametrize("name", ["PWD", "OLDPWD", "PATH", "PROBE_SERVICE_KEEPER", "model"])
def test_names_that_are_not_credentials(name):
    assert not report.credential_name(name)


def test_header_values_are_redacted_and_their_names_kept():
    env = {"ANTHROPIC_CUSTOM_HEADERS": "X-Gateway-Key: gk-123456\nX-Team: research",
           "OTEL_EXPORTER_OTLP_HEADERS": "x-honeycomb-team=hc-abcdef"}
    clean = report.redact_env(env, report.Scope.LOCAL)
    # A credential-like header name (`X-Gateway-Key`) takes its whole line.
    assert clean == {"ANTHROPIC_CUSTOM_HEADERS": "<redacted>\nX-Team: <redacted>",
                     "OTEL_EXPORTER_OTLP_HEADERS": "x-honeycomb-team=<redacted>"}
    tree = report.redact_tree({"headers": {"X-Api": "v1", "X-Other": "v2"}}, report.Scope.LOCAL)
    assert tree == {"headers": {"X-Api": "<redacted>", "X-Other": "<redacted>"}}


def test_mcp_args_lose_their_values():
    config = {"mcpServers": {"supabase": {"command": "npx", "args": ["-y", "@supabase/mcp", "--access-token",
                                                                      "sbp_0123456789abcdef"]}}}
    clean = report.redact_tree(config, report.Scope.LOCAL)
    assert clean["mcpServers"]["supabase"]["args"] == ["-y", "<arg>", "--access-token", "<arg>"]
    assert clean["mcpServers"]["supabase"]["command"] == "npx"


def test_oauth_and_account_blocks_are_dropped_whole():
    clean = report.redact_tree({"oauthAccount": {"emailAddress": "a@b.test"}, "account": {"email": "c@d.test"},
                                "projects": {"/p": {"history": [{"display": "a prompt"}]}}}, report.Scope.LOCAL)
    text = json.dumps(clean)
    assert "a@b.test" not in text and "c@d.test" not in text and "a prompt" not in text


def test_the_report_fits_the_servers_cap_as_the_transport_encodes_it(machine):
    """Non-ASCII text grows when the transport escapes it (`json.dumps`'s
    default): the cap is measured that way, so the body stays under 640 KiB."""
    _plant_logs()
    _bind(SID)
    from probe.harness import get_registry

    wide = "".join(f"{i} 训练运行失败了，请检查日志 ✓\n" for i in range(40000))
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    state = _state()
    tap_log = get_registry().get("claude_code").capture.state_dir() / "logs" / f"{SID}.log"
    tap_log.parent.mkdir(parents=True, exist_ok=True)
    for path in (state / "daemon-errors.log", state / "daemon" / f"{SID}.log", tap_log,
                 state / "daemon" / "sessions" / SID / "worker.log", _service_dir() / "update.log"):
        path.write_text(wide, encoding="utf-8")
    (_service_dir() / "service.log").write_text("".join(f"[{stamp}] probe-service[1]: {line}\n"
                                                         for line in wide.splitlines()), encoding="utf-8")
    _accept(machine)
    assert report.send(auto=False, family="worker", reason="x", sid=SID).sent
    (raw,) = [r["body"] for r in machine.requests if r["path"] == report.ROUTE]
    assert len(raw) <= 640 * 1024


def test_the_worker_log_never_carries_an_audit_reports_text(monkeypatch, caplog):
    pytest.importorskip("pydantic_ai")  # the daemon extra (`audit` imports the agent); agent-ci runs without it
    import logging
    from types import SimpleNamespace

    from probe.daemon import audit, mailbox

    monkeypatch.setattr(mailbox, "enabled", lambda **_k: False)
    lane = SimpleNamespace(w=SimpleNamespace(session=SimpleNamespace(source="kimi_code")), sid=SID)
    with caplog.at_level(logging.INFO, logger=audit.log.name):
        audit.AuditLane.report(lane, "the researcher's run 42 on the ACME data changed its config")
    assert caplog.records and "ACME" not in caplog.text


def test_a_report_answers_even_when_its_folder_cannot_be_written(machine):
    reports = report.reports_dir()
    reports.parent.mkdir(parents=True, exist_ok=True)
    reports.write_text("a file where the folder should be")
    _accept(machine)
    auto = report.send(auto=True, family="worker", reason="gave_up", env={})
    assert auto.as_json() == {"sent": False, "id": None, "skipped": "server", "path": None}
    manual = report.send(auto=False, family="worker", reason="x")
    assert manual.sent and manual.path is None


def test_an_automatic_session_report_needs_the_sessions_environment():
    with pytest.raises(RequestError):
        requests.parse(ActionName.REPORT, {"auto": True, "family": "worker", "reason": "x", "sid": SID})
    # A machine family's consent is the service's: `env` may be left out.
    assert requests.parse(ActionName.REPORT, {"family": "service_crash", "reason": "x"}).env == {}
    # A manual one needs no consent at all.
    assert requests.parse(ActionName.REPORT, {"auto": False, "family": "worker", "reason": "x", "sid": SID})


def test_the_keepers_lines_stay_in_the_service_log(machine):
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (_service_dir() / "service.log").write_text(
        f"[{stamp}] probe-service-keeper[77]: the service did not answer; starting it\n")
    _accept(machine)
    assert report.send(auto=False, family="worker", reason="x").sent
    assert "probe-service-keeper[77]" in json.loads(_sent_text(machine))["report"]["logs"]["service_log"]


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no FIFOs here")
def test_a_fifo_where_a_log_should_be_never_blocks_a_report(machine, monkeypatch):
    _state().mkdir(parents=True, exist_ok=True)
    os.mkfifo(_state() / "daemon-errors.log")
    monkeypatch.setattr(report, "STAFF_SOURCE_BUDGET_S", 1.0)
    _accept(machine)
    assert report.send(auto=False, family="worker", reason="x").sent
    assert "logs" not in json.loads(_sent_text(machine))["report"]["skipped"]


# ---------------------------------------------------------------------------
# Delta review of 8eccea95b: each of these failed on 8eccea95b
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("config", "leaked"), [
    ({"command": "SLACK_TOKEN=xoxb-plainsecret ~/.claude/hooks/notify.sh"}, "xoxb-plainsecret"),
    ({"command": "MYPASS=hunter2 python3 hook.py"}, "hunter2"),
    ({"command": "OPENAI_API_KEY=sk-proj-abcdefghijklmnop"}, "sk-proj-abcdefghijklmnop"),
    ({"args": "sk-ant-api03-abcdefghijklmnop"}, "sk-ant-api03-abcdefghijklmnop"),
    ({"command": "https://user:hunter2@example.com/hook"}, "hunter2"),
    ({"notify": ["bash", "-c", "curl https://h?k=plainsecretT1"]}, "plainsecretT1"),
    ({"args": ["--token", "plainsecret", 1]}, "plainsecret"),
], ids=["leading-assignment", "assignment-then-program", "single-assignment", "single-arg", "url-command",
        "codex-notify", "mixed-list"])
def test_no_word_of_a_configured_command_is_kept_raw(config, leaked):
    clean = json.dumps(report.redact_tree(config, report.Scope.LOCAL))
    assert leaked not in clean


def test_a_leading_assignment_keeps_its_name():
    clean = report.redact_tree({"command": "SLACK_TOKEN=xoxb-plainsecret ~/.claude/hooks/notify.sh"},
                               report.Scope.LOCAL)
    assert clean["command"] == "SLACK_TOKEN=<arg> notify.sh"


@pytest.mark.parametrize(("argv", "expected"), [
    (["probe", "--api-key", "sk-live1234", "doctor"], ["probe", "--api-key", "<arg>", "<arg>"]),
    (["python", "-m", "probe", "--token", "hunter2pass", "ask"],
     ["python", "-m", "probe", "--token", "<arg>", "<arg>"]),
    (["git", "commit", "-m", "probe:hunter2"], ["git", "<arg>", "-m", "<arg>"]),
    (["claude", "--model=sk-ant-api03-abcdefghijklmnop"], ["claude", "--model=<arg>"]),
    ([r"C:\Program Files\nodejs\node.exe", "server.js"], ["node.exe", "<arg>"]),
    (["/Applications/Claude Code.app/Contents/MacOS/claude", "-p", "a prompt"], ["claude", "-p", "<arg>"]),
])
def test_flag_values_never_take_the_subcommand_slot_and_kept_values_are_scrubbed(argv, expected):
    assert report.redact_argv(argv) == expected


def test_header_strings_lose_everything_after_each_name():
    env = {"ANTHROPIC_CUSTOM_HEADERS": "Authorization: Bearer abc123, def456\nloose-secret-line\nX-Team: research",
           "OTEL_EXPORTER_OTLP_HEADERS": "x-honeycomb-team=hc-1,x-other=two"}
    clean = report.redact_env(env, report.Scope.LOCAL)
    assert clean["ANTHROPIC_CUSTOM_HEADERS"] == "<redacted>\nX-Team: <redacted>"
    assert clean["OTEL_EXPORTER_OTLP_HEADERS"] == "x-honeycomb-team=<redacted>,x-other=<redacted>"


def test_a_json_config_with_a_byte_order_mark_is_parsed(tmp_path):
    path = tmp_path / "settings.json"
    path.write_bytes(b"\xef\xbb\xbf" + json.dumps({"model": "opus", "apiKey": "k-123"}).encode())
    clean, why = report.read_config(path)
    assert why is None and json.loads(clean) == {"model": "opus", "apiKey": "<redacted>"}


def test_a_config_past_eight_mebibytes_is_only_listed(tmp_path):
    path = tmp_path / "big.json"
    path.write_text(json.dumps({"blob": "x" * (8 * 1024 * 1024 + 1)}))
    clean, why = report.read_config(path)
    assert clean is None and "MiB" in why


def test_redacting_a_big_tree_checks_in_as_it_goes():
    """A config walk calls its check every so many nodes: the debug log's
    collector can stop an abandoned walk there."""
    calls = []

    def check():
        calls.append(1)
        if len(calls) >= 3:
            raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        report.redact_tree({str(i): {"v": i} for i in range(20000)}, report.Scope.LOCAL, check=check)
    assert len(calls) == 3


def test_the_session_filter_ignores_a_uuid_in_the_home_folders_path(machine, monkeypatch, tmp_path):
    """A home under a folder named by a UUID (a scratchpad, a CI job): its
    path is not another session's id, and the report's own lines stay."""
    home = tmp_path / "11111111-aaaa-4bbb-8ccc-000000000000" / "home"
    home.mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))  # Path.home() on Windows
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    _state().mkdir(parents=True, exist_ok=True)
    (_state() / "daemon-errors.log").write_text(f"{stamp} session {SID}: crashed in {home}/proj\n")
    _bind(SID)
    _accept(machine)
    assert report.send(auto=False, family="worker", reason="x", sid=SID).sent
    assert "crashed in ~/proj" in json.loads(_sent_text(machine))["report"]["logs"]["daemon_errors"]


# ---------------------------------------------------------------------------
# Second delta review of e0e5bb31d: each of these failed on e0e5bb31d
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("argv", "expected"), [
    (["probe", "--json", "ask", "hunter2"], ["probe", "--json", "<arg>", "<arg>"]),
    (["probe", "hunter2"], ["probe", "<arg>"]),
    (["probe", "ask", "run"], ["probe", "ask", "<arg>"]),
    (["claude", "--model", "opus"], ["claude", "--model", "<arg>"]),
    (["claude", "--model=sonnet"], ["claude", "--model=<arg>"]),
    (["python3", "-I", "-m", "probe.core.run", "report"], ["python3", "-I", "-m", "probe.core.run", "report"]),
    (["python3", "-m", "probe", "--json", "ask"], ["python3", "-m", "probe", "--json", "<arg>"]),
    (["python3", "-m", "probe_evil.x", "status"], ["python3", "-m", "<arg>", "<arg>"]),
    (["node", "-m", "probe"], ["node", "-m", "<arg>"]),
    ([7, "status"], ["<arg>", "<arg>"]),
], ids=["flag-before-word", "not-a-subcommand", "one-word-only", "model-value", "model-assignment",
        "core-run-action", "flag-after-module", "not-a-probe-module", "not-python", "non-string-program"])
def test_the_argv_rule_keeps_program_flag_names_one_known_subcommand(argv, expected):
    assert report.redact_argv(argv) == expected


def test_the_subcommand_allow_list_is_the_clis_own():
    """Derived from the code: the CLI's top-level commands and the
    `probe.core.run` actions, nothing guessed."""
    import importlib

    main = importlib.import_module("probe.cli.main")
    names = {group.name for group in main.app.registered_groups if group.name}
    names |= {(c.name or c.callback.__name__.replace("_", "-")) for c in main.app.registered_commands}
    names |= {action.value for action in ActionName}
    assert report.PROBE_SUBCOMMANDS == frozenset(names)


@pytest.mark.parametrize(("command", "expected", "secrets"), [
    ('PASSWORD="correct horse battery" ./run.sh --flag v', "PASSWORD=<arg> run.sh --flag <arg>",
     ("correct", "horse", "battery")),
    ("MSG='tell bob hunter2' notify.sh", "MSG=<arg> notify.sh", ("bob", "hunter2")),
])
def test_a_config_command_string_is_split_like_a_shell(command, expected, secrets):
    clean = report.redact_tree({"command": command}, report.Scope.LOCAL)["command"]
    assert clean == expected
    for secret in secrets:
        assert secret not in clean


@pytest.mark.parametrize(("value", "expected"), [
    ("dXNlcjpwYXNzd29yZA==", "<redacted>"),
    ("X-Api-Keys: k1==,key2BBBB==", "<redacted>"),
    ("sk-ant-api03-abcdefghijklmnopqrst: x", "<redacted>"),
    ("Authorization: Bearer abc, def", "<redacted>"),
    ("x-honeycomb-team=hc-1,x-other=two", "x-honeycomb-team=<redacted>,x-other=<redacted>"),
    ("X-Team: research\nno header here", "X-Team: <redacted>"),
])
def test_a_header_line_keeps_only_a_plain_header_name(value, expected):
    assert report.redact_env({"OTEL_EXPORTER_OTLP_HEADERS": value}, report.Scope.LOCAL)[
        "OTEL_EXPORTER_OTLP_HEADERS"] == expected


def test_a_credential_name_wins_over_a_header_name():
    assert report.redact_env({"AUTH_HEADER_VALUE": "dXNlcjpwYXNzd29yZA=="}, report.Scope.LOCAL) == {
        "AUTH_HEADER_VALUE": "<redacted>"}
    assert report.redact_tree({"AUTH_HEADER_VALUE": "dXNlcjpwYXNzd29yZA=="}, report.Scope.LOCAL) == {
        "AUTH_HEADER_VALUE": "<redacted>"}


@pytest.mark.parametrize("name", ["deep.json", "deep.toml"])
def test_a_config_nested_past_pythons_recursion_limit_is_only_listed(tmp_path, name):
    path = tmp_path / name
    path.write_text("[" * 5000 + "]" * 5000 if name.endswith(".json") else "a = " + "[" * 5000 + "]" * 5000)
    clean, why = report.read_config(path)
    assert clean is None and why == "not parsed"


def test_an_automatic_report_refused_with_every_key_says_so_by_telemetry(machine, monkeypatch):
    """The machine whose every key is dead is the one this report is about,
    and the report cannot reach us: `service.report_undeliverable` can (a
    PostHog destination posts it). Once per family per dedupe window: the
    refused try keeps its claim, so the service's retry answers `deduped`."""
    from probe._shared import telemetry

    said: list = []
    monkeypatch.setattr(telemetry, "emit_report_undeliverable",
                        lambda **kwargs: said.append(kwargs) or True)
    machine.routes[("POST", report.ROUTE)] = (401, {"detail": "invalid token"}, {})
    now = time.time() // report.DEDUPE_WINDOW_S * report.DEDUPE_WINDOW_S + 60
    first = report.send(auto=True, family="outbox_stuck", reason="credential_refused", env={}, now=now)
    retry = report.send(auto=True, family="outbox_stuck", reason="credential_refused", env={}, now=now + 1800)
    assert (first.skipped, retry.skipped) == ("unauthorized", "deduped")
    assert said == [{"family": "outbox_stuck", "reason": "credential_refused", "base_url": machine.url}]


def test_one_outage_refused_for_many_sessions_is_one_undeliverable_event_per_family(machine, monkeypatch):
    """C1 reviews: the report's claim is per session, so each session's
    report of one outage emitted its own event: up to 64 #eng-alerts posts a day."""
    from probe._shared import telemetry

    said: list = []
    monkeypatch.setattr(telemetry, "emit_report_undeliverable", lambda **kwargs: said.append(kwargs) or True)
    machine.routes[("POST", report.ROUTE)] = (401, {"detail": "invalid token"}, {})
    now = time.time() // report.DEDUPE_WINDOW_S * report.DEDUPE_WINDOW_S + 60
    for sid in ("11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222"):
        assert report.send(auto=True, family="recorder", reason="failing", sid=sid, env={}, now=now).skipped \
            == "unauthorized"
    report.send(auto=True, family="worker", reason="hung", env={}, now=now)
    assert [s["family"] for s in said] == ["recorder", "worker"]


def test_a_signed_out_machine_sends_no_undeliverable_event(machine, monkeypatch):
    """No key held is a person who signed out, not a dead one: no alert."""
    from probe._shared import telemetry

    said: list = []
    monkeypatch.setattr(telemetry, "emit_report_undeliverable", lambda **kwargs: said.append(kwargs) or True)
    monkeypatch.setattr(report, "credentials", lambda: [])
    assert report.send(auto=True, family="worker", reason="x", env={}).skipped == "unauthorized"
    assert said == []


def test_a_manual_or_offline_report_sends_no_undeliverable_event(machine, monkeypatch):
    from probe._shared import telemetry

    said: list = []
    monkeypatch.setattr(telemetry, "emit_report_undeliverable", lambda **kwargs: said.append(kwargs) or True)
    machine.routes[("POST", report.ROUTE)] = (401, {"detail": "invalid token"}, {})
    assert report.send(auto=False, family="worker", reason="x").skipped == "unauthorized"
    monkeypatch.setenv("PROBE_BASE_URL", f"http://127.0.0.1:{_closed_port()}")
    assert report.send(auto=True, family="worker", reason="x", env={}).skipped == "offline"
    assert said == []
