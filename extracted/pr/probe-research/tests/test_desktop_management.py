"""Desktop review pins real transcript bytes and account identity before durable admission."""
from contextlib import nullcontext
import json
from uuid import uuid4

import pytest
from typer.testing import CliRunner

from probe.cli import desktop as d, backfill_transcripts as t, capabilities, import_jobs
from tests.test_import_jobs import queued as queued
from tests.test_backfill_scoped_orchestration import make_harness


@pytest.fixture
def reviewed(tmp_path, monkeypatch, queued):
    h = make_harness(tmp_path, monkeypatch)
    monkeypatch.setattr(d, "_client", lambda: nullcontext(h.client))
    sid = str(uuid4())
    path = tmp_path / "session.jsonl"
    path.write_text(json.dumps({"sessionId": sid, "message": {"role": "user", "content": "Research"}})+"\n")
    row = t.Transcript(path, sid, "claude_code", "/research/model", path.stat().st_size, path.stat().st_mtime)
    monkeypatch.setattr(d, "_sources", lambda: t.Census(candidates=[row]))
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda source: ("capture-secret", "https://test.invalid"))
    monkeypatch.setattr(capabilities, "capture_device_id", lambda source: "device")
    return h, row, queued


def test_review_pins_selected_prefix_and_enqueues_once_without_credentials(reviewed):
    h, row, launches = reviewed
    preview = d.dispatch({"op": "preview_backfill", "sessionIds": [f"claude_code:{row.session_id}"], "folders": []})
    assert not launches
    saved = json.loads(d._preview_path(preview["id"]).read_text())
    assert saved["transcripts"]["files"][0]["size"] == row.size
    assert saved["transcripts"]["files"][0]["sha256"] == t.prefix_hash(row.path, row.size)
    assert "capture-secret" not in json.dumps(saved)
    # New bytes never expand the reviewed approval.
    row.path.write_text(row.path.read_text()+'{"new":"unreviewed"}\n')
    result = d.dispatch({"op": "start_backfill", "previewId": preview["id"]})
    assert len(result) == len(launches) == 1
    payload = import_jobs.get_job(result[0]["id"])["payload"]
    assert payload["files"][0]["size"] == row.size
    assert d.start_backfill(preview["id"])[0]["id"] == result[0]["id"]
    assert len(launches) == 1
    history = d.dispatch({"op": "jobs"})
    assert history["jobs"][0]["id"] == result[0]["id"]
    assert history["scope"] == {"userId": "user", "customerId": "tenant"}
    assert "payload" not in result[0]


def test_account_change_refuses_admission_and_hides_history(reviewed, monkeypatch):
    h, row, launches = reviewed
    p = d.preview_backfill({"sessionIds": [f"claude_code:{row.session_id}"]})
    job = d.start_backfill(p["id"])[0]
    monkeypatch.setattr(h.client, "me", lambda: {"customer_id": "different", "user_id": "user"})
    history = d.dispatch({"op": "jobs"})
    assert history["jobs"] == []
    assert history["scope"] == {"userId": "user", "customerId": "different"}
    with pytest.raises(ValueError, match="another account"):
        d.dispatch({"op": "cancel_job", "id": job["id"]})
    with pytest.raises(ValueError, match="account or destination changed"):
        d.start_backfill(p["id"])
    assert len(launches) == 1


def test_missing_selection_and_expired_review_never_start_workers(reviewed):
    _, row, launches = reviewed
    with pytest.raises(ValueError, match="changed or is no longer"):
        d.preview_backfill({"sessionIds": ["claude_code:missing"]})
    p = d.preview_backfill({"sessionIds": [f"claude_code:{row.session_id}"]})
    path = d._preview_path(p["id"])
    saved = json.loads(path.read_text())
    saved["created"] = 0
    path.write_text(json.dumps(saved))
    with pytest.raises(ValueError, match="expired"):
        d.start_backfill(p["id"])
    assert not launches


def test_closed_request_refuses_unknown_fields_and_unsafe_capture_scope():
    for request in ({"op": "jobs", "token": "x"}, {"op": "shell", "argv": ["rm"]},
                    {"op": "preview_backfill", "folders": [True]}):
        with pytest.raises(ValueError):
            d.dispatch(request)
    with pytest.raises(ValueError, match="affects every local agent"):
        d.dispatch({"op": "set_capture", "source": "pi", "enabled": False})


def test_registry_counts_are_live_processes_not_imported_history(monkeypatch):
    from probe.service import client
    monkeypatch.setattr(client, "call", lambda *a, **k: {"sessions": [
        {"harness": "claude_code", "alive": True}, {"harness": "claude_code", "alive": False},
        {"harness": "codex", "alive": True}, {"harness": "codex", "alive": True},
    ]})
    result = d.snapshot_delivery()
    rows = {row["source"]: row for row in result["agents"]}
    assert result["available"] and rows["claude_code"]["activeAgents"] == 1
    assert rows["codex"]["activeAgents"] == 2
    monkeypatch.setattr(client, "call", lambda *a, **k: (_ for _ in ()).throw(OSError()))
    assert all(row["activeAgents"] is None for row in d.snapshot_delivery()["agents"])


def _service(monkeypatch, *, listing=None, status=None):
    """`client.call` answering per method: a value is returned, an exception raised."""
    from probe.service import client
    from probe.service.protocol import Method
    asked = []

    def call(method, *args, **kwargs):
        asked.append(method)
        answer = {Method.SESSION_LIST: listing, Method.STATUS: status}[method]
        if isinstance(answer, BaseException):
            raise answer
        return answer

    monkeypatch.setattr(client, "call", call)
    return asked


def _status(state="running", in_progress=False):
    return {"state": state, "update": {"in_progress": in_progress}, "sessions": 1}


@pytest.mark.parametrize("listing, status, state, available, words", [
    (FileNotFoundError(), None, d.ServiceState.NOT_RUNNING, False, "probe service start"),
    (ConnectionRefusedError(), None, d.ServiceState.NOT_RUNNING, False, "not running"),
    (PermissionError(), None, d.ServiceState.REFUSED, False, "not private to this user"),
    (TimeoutError(), None, d.ServiceState.UNREACHABLE, False, "did not answer in time"),
    (OSError("broken pipe"), None, d.ServiceState.UNREACHABLE, False, "the connection failed (broken pipe)"),
    ({"sessions": "x"}, _status(), d.ServiceState.UNREACHABLE, False, "its answer could not be read"),
    ({"sessions": []}, _status("discovering"), d.ServiceState.STARTING, True, "still checking in"),
    ({"sessions": []}, _status(in_progress=True), d.ServiceState.UPDATING, True, "installing an update"),
    ({"sessions": []}, _status(), d.ServiceState.RUNNING, True, "live-session registry"),
    ({"sessions": []}, OSError(), d.ServiceState.RUNNING, True, "live-session registry"),
    ({"sessions": "x"}, _status(in_progress=True), d.ServiceState.UPDATING, False, "Try again in a minute"),
    ({"sessions": "x"}, _status("discovering"), d.ServiceState.STARTING, False, "Try again in a few seconds"),
], ids=["no-socket", "refused-connect", "foreign-folder", "timeout", "broken", "unreadable", "discovering",
        "updating", "running", "running-no-status", "updating-unlisted", "starting-unlisted"])
def test_the_overview_says_why_its_counts_are_missing_or_partial(monkeypatch, listing, status, state, available, words):
    """D30: "unavailable" alone told nobody what to do."""
    asked = _service(monkeypatch, listing=listing, status=status)
    result = d.snapshot_delivery()
    assert (result["serviceState"], result["available"]) == (state, available)
    assert words in result["reason"]
    if isinstance(listing, (FileNotFoundError, PermissionError, TimeoutError)):
        assert len(asked) == 1, "nothing there to ask what it is doing: no second call"


def test_a_refusal_says_what_the_service_said(monkeypatch):
    from probe.service import client
    _service(monkeypatch, listing=client.ServiceError(-32013, "unsupported_api"), status=client.ServiceError(-32013, "x"))
    result = d.snapshot_delivery()
    assert result["serviceState"] == d.ServiceState.REFUSED and "(unsupported_api)" in result["reason"]


def test_windows_asks_the_service_too(monkeypatch):
    """R3: the service runs on Windows (its named pipe), so the app's live
    counts come from it there as everywhere."""
    import os
    asked = _service(monkeypatch, listing={"sessions": []}, status={"state": "running"})
    with monkeypatch.context() as windows:
        windows.setattr(os, "name", "nt")
        result = d.snapshot_delivery()
    assert result["serviceState"] != d.ServiceState.UNSUPPORTED and asked


def test_cli_envelope_is_versioned_and_contains_no_traceback():
    result = CliRunner().invoke(d.app, ["--json"], input='{"op":"shell"}')
    assert result.exit_code == 1
    assert json.loads(result.stdout) == {"v": 1, "ok": False, "error": "Unknown desktop operation."}


def test_terminal_setup_lock_blocks_admission_before_account_or_worker_access(tmp_path, monkeypatch):
    import os
    import subprocess
    import sys
    import time
    from probe.cli import wizard_lock
    marker = tmp_path / "held"
    proc = subprocess.Popen([sys.executable, "-c", "from probe.cli import wizard_lock; import sys,time; "
        "ctx=wizard_lock.held(); ctx.__enter__(); open(sys.argv[1],'w').close(); time.sleep(30)", str(marker)],
        env=os.environ.copy())
    try:
        deadline = time.monotonic() + 10
        while not marker.exists() and time.monotonic() < deadline:
            time.sleep(.01)
        assert marker.exists()
        monkeypatch.setattr(d, "_client", lambda: pytest.fail("Busy must not inspect another account"))
        with pytest.raises(wizard_lock.Busy):
            d.dispatch({"op": "start_backfill", "previewId": uuid4().hex})
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_registered_cli_group_reads_json_stdin_and_reports_supported_envelope():
    import importlib
    main = importlib.import_module("probe.cli.main")
    result = CliRunner().invoke(main.app, ["desktop", "request", "--json"], input='{"op":"shell"}')
    assert result.exit_code == 1
    assert json.loads(result.stdout)["v"] == 1
    assert json.loads(result.stdout)["error"] == "Unknown desktop operation."


def test_repeated_json_fields_are_refused_before_admission():
    result = CliRunner().invoke(d.app, ["--json"], input='{"op":"jobs","op":"start_backfill"}')
    assert result.exit_code == 1
    assert json.loads(result.stdout)["error"] == "Desktop request contains a repeated field."


def test_folder_review_refuses_changed_workspace_or_replaced_folder_before_scanning(reviewed, monkeypatch):
    from probe.cli import backfill
    h, _, launches = reviewed
    monkeypatch.setattr(backfill, "available_agents", lambda: [backfill.Agent.CLAUDE])
    p = d.preview_backfill({"folders": [str(h.folder)]})
    assert h.classified == h.created == h.manifested == []
    h.client.settings.workspace = "other-workspace"
    with pytest.raises(ValueError, match="workspace changed"):
        d.start_backfill(p["id"])
    h.client.settings.workspace = "workspace"
    old = h.folder.with_name("moved")
    h.folder.rename(old)
    h.folder.mkdir()
    with pytest.raises(ValueError, match="folder was replaced"):
        d.start_backfill(p["id"])
    assert not launches


def _history_job(index, identity, *, state="succeeded"):
    return {"id": f"{index:032x}", "kind": "transcripts", "label": f"Backfill {index}",
            "state": state, "created_at": f"2026-10-19T00:{index // 60:02}:{index % 60:02}+00:00",
            "updated_at": "2026-10-19T01:00:00+00:00", "payload": {"account": identity},
            "progress": {"completion_completed": 1, "completion_total": 2},
            "error": None, "report": ["verbose report " + "x" * 5000] * 300}


def test_history_is_paginated_without_reports_and_partial_details_are_bounded(reviewed, monkeypatch):
    h, _, _ = reviewed
    identity = d._identity(h.client)
    jobs = [_history_job(index, identity, state="running" if index == 0 else "succeeded")
            for index in range(123)]
    monkeypatch.setattr(import_jobs, "list_jobs", lambda: jobs)
    monkeypatch.setattr(import_jobs, "get_job", lambda key: next(job for job in jobs if job["id"] == key))
    first = d.dispatch({"op": "jobs"})
    assert first["total"] == 123 and len(first["jobs"]) == 50 and first["hasMore"]
    assert first["activeTotal"] == 1 and first["activeJobs"][0]["id"] == jobs[0]["id"]
    assert all(job["report"] == job["activity"] == [] for job in first["jobs"] + first["activeJobs"])
    assert len(json.dumps(first).encode()) < 100_000
    assert all(job["partial"] for job in first["jobs"])
    seen = [job["id"] for job in first["jobs"]]
    cursor = first["nextCursor"]
    # A worker finishing between pages must not change cursor order.
    jobs[0]["state"] = "succeeded"
    while cursor:
        assert len(cursor) <= 256
        page = d.dispatch({"op": "jobs", "cursor": cursor})
        assert page["scope"] == first["scope"]
        seen.extend(job["id"] for job in page["jobs"])
        cursor = page["nextCursor"]
    assert seen == [job["id"] for job in reversed(jobs)] and len(set(seen)) == 123
    detail = d.dispatch({"op": "job", "id": jobs[0]["id"]})
    assert detail["partial"] and detail["scope"] == first["scope"]
    assert detail["reportTruncated"] and len(detail["report"]) == 200
    assert all(len(line) <= 2000 for line in detail["report"])
    assert len(json.dumps(detail).encode()) < 1_000_000


def test_job_sources_are_approved_producers_without_payload_or_worker_inference():
    job = _history_job(1, {})
    job["label"] = "Codex and pi"  # Presentation never determines the producers.
    job["payload"]["files"] = [
        {"agent": "claude_code", "path": "/private/research.jsonl"},
        {"agent": "codex"}, {"agent": "claude"}, {"agent": "codex"},
        {"agent": "pi"}, {"agent": "kimi_code"}, {"agent": "new_agent"},
        {"agent": "not an agent"}, {"agent": "x" * 65}, {"agent": True}, None,
    ]
    result = d._public_job(job)
    assert result["sources"] == ["claude_code", "codex", "pi", "kimi_code", "new_agent"]
    assert "payload" not in result and "/private/research.jsonl" not in json.dumps(result)
    assert d._public_job(job, summary=True)["sources"] == result["sources"]
    job["kind"] = "folder"
    job["payload"]["agent"] = "codex"
    assert d._public_job(job)["sources"] == []
    job["kind"] = "transcripts"
    del job["payload"]["files"]
    assert d._public_job(job)["sources"] == []


def test_source_and_activity_metadata_never_cross_account_filter(reviewed, monkeypatch):
    h, _, _ = reviewed
    identity = d._identity(h.client)
    mine = _history_job(1, identity)
    mine["payload"]["files"] = [{"agent": "codex"}]
    other = _history_job(2, {**identity, "user_id": "another-user"})
    other["payload"]["files"] = [{"agent": "private_agent"}]
    other["activity"] = [{"at": "now", "state": "running", "message": "Private progress"}]
    monkeypatch.setattr(import_jobs, "list_jobs", lambda: [mine, other])
    monkeypatch.setattr(import_jobs, "get_job", lambda key: other)
    result = d.dispatch({"op": "jobs"})
    assert result["jobs"][0]["sources"] == ["codex"]
    assert "private_agent" not in json.dumps(result)
    with pytest.raises(ValueError, match="another account"):
        d.dispatch({"op": "job", "id": other["id"]})


def test_old_worker_activity_is_only_its_current_public_progress_not_raw_log(tmp_path):
    job = _history_job(1, {}, state="running")
    raw = tmp_path / "output.log"
    raw.write_text("Never return raw coding-agent output or transcript bytes")
    job["log_path"] = str(raw)
    job["progress"]["message"] = "Uploading approved sessions"
    result = d._public_job(job)
    assert result["activity"] == [
        "2026-10-19T01:00:00+00:00 running: Uploading approved sessions"
    ]
    assert not result["activityTruncated"]
    assert "Never return" not in json.dumps(result)
    assert result["report"]  # The existing final-result contract stays separate.


def test_public_activity_is_bounded_redacted_and_does_not_duplicate_progress():
    job = _history_job(1, {}, state="running")
    secret = "ghp_" + "A1b2C3d4E5" * 3 + "A1b2C3"
    job["activity"] = [
        {"at": "2026-10-19T01:00:00+00:00", "state": "running", "message": f"Uploading {index}"}
        for index in range(205)
    ]
    job["activity"][-1]["message"] = "Latest " + secret
    job["progress"]["message"] = job["activity"][-1]["message"]
    result = d._public_job(job)
    assert result["activityTruncated"] and len(result["activity"]) == 200
    assert "Uploading 5" in result["activity"][0]
    assert "Latest" in result["activity"][-1] and secret not in json.dumps(result["activity"])
    job["progress"]["message"] = "x" * 5000
    job["activity"].append({"at": "now", "state": {}, "message": "malformed"})
    result = d._public_job(job)
    assert len(result["activity"]) <= 200 and result["activityTruncated"]
    assert all(len(line) <= 2000 for line in result["activity"])


def test_activity_scrubs_preclipped_vendor_tokens_and_credential_url_context():
    job = _history_job(1, {}, state="running")
    full_token = "ghp_" + "A1b2C3d4E5" * 3 + "A1b2C3"
    # The existing worker progress path clips at 1500 before persisting. Its
    # retained token fragment no longer matches the full vendor signature.
    clipped = import_jobs._clean("Uploading " + "x" * 1466 + " " + full_token)
    fragment = clipped[clipped.index("ghp_"):]
    assert 16 <= len(fragment) < len(full_token)
    job["progress"]["message"] = clipped
    result = d._public_job(job)
    assert fragment not in json.dumps(result["activity"])
    assert "<redacted>" in result["activity"][-1]
    job["progress"]["message"] = (
        "Retry https://user:password@example.test/receive?token=private-token#api_key=fragment-secret"
    )
    result = d._public_job(job)
    assert all(secret not in json.dumps(result["activity"]) for secret in (
        "user:password", "private-token", "fragment-secret",
    ))
    assert "example.test/receive" in result["activity"][-1]


def test_scope_is_captured_once_and_old_cursor_cannot_cross_accounts(reviewed, monkeypatch):
    h, _, _ = reviewed
    identity = d._identity(h.client)
    jobs = [_history_job(index, identity) for index in range(51)]
    calls = []
    def me():
        calls.append(True)
        return {"customer_id": "tenant", "user_id": "user"}
    monkeypatch.setattr(h.client, "me", me)
    def listing():
        monkeypatch.setattr(h.client, "me", lambda: {"customer_id": "new-tenant", "user_id": "other"})
        return jobs
    monkeypatch.setattr(import_jobs, "list_jobs", listing)
    result = d.dispatch({"op": "jobs"})
    assert len(calls) == 1
    assert result["scope"] == {"customerId": "tenant", "userId": "user"}
    assert len(result["jobs"]) == 50
    with pytest.raises(ValueError, match="cursor is invalid"):
        d.dispatch({"op": "jobs", "cursor": result["nextCursor"]})
    assert d.dispatch({"op": "jobs"})["jobs"] == []


def test_client_pins_settings_and_context_instead_of_ambient_refresh(tmp_path, monkeypatch):
    from probe.sdk import config
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setattr(config, "current_context_name", lambda: "initial")
    def resolve(**kwargs):
        assert kwargs == {"context": "initial"}
        return config.Settings(base_url="https://test.invalid", token="fixed-token")
    monkeypatch.setattr(config, "resolve", resolve)
    with d._client() as client:
        assert client._ambient_credentials is False
        monkeypatch.setattr(config, "current_context_name", lambda: "new")
        monkeypatch.setattr(client, "me", lambda: {"customer_id": "tenant", "user_id": "user"})
        assert d._identity(client)["context"] == "initial"
        assert client.settings.token == "fixed-token"


def test_backend_comparison_preserves_path_case_but_normalizes_host(reviewed):
    h, _, _ = reviewed
    identity = {**d._identity(h.client), "base_url": "https://API.example.com/Probe/"}
    folder = {"payload": {"scope": {"customer_id": "tenant", "backend": "https://api.example.com/Probe"},
                          "user_id": "user", "context": identity["context"]}}
    assert d._job_matches(folder, identity)
    folder["payload"]["scope"]["backend"] = "https://api.example.com/probe"
    assert not d._job_matches(folder, identity)
    transcript = {"payload": {"account": {**identity, "base_url": "https://api.example.com/Probe"}}}
    assert d._job_matches(transcript, identity)


def test_delivery_scope_uses_the_same_authenticated_identity(reviewed, monkeypatch):
    from probe.service import client
    monkeypatch.setattr(client, "call", lambda *a, **k: {"sessions": []})
    result = d.dispatch({"op": "delivery"})
    assert result["scope"] == {"customerId": "tenant", "userId": "user"}


@pytest.mark.parametrize("cursor", ["", "?", "x" * 257, "e30"])
def test_history_refuses_bad_cursors(reviewed, cursor):
    with pytest.raises(ValueError, match="cursor is invalid"):
        d.dispatch({"op": "jobs", "cursor": cursor})


@pytest.mark.parametrize("value", ["off", "0", "false", "no", "disabled", " FALSE "])
def test_analytics_policy_honors_opt_out_without_credentials_or_network(reviewed, monkeypatch, value):
    monkeypatch.setenv("PROBE_TELEMETRY", value)
    monkeypatch.setattr(d, "_client", lambda: pytest.fail("Policy must not authenticate"))
    assert d.dispatch({"op":"analytics_policy"}) == {"enabled":False,"resolved":True}


@pytest.mark.parametrize("base,allowed", [
    ("https://api.research.prbe.ai", True), ("https://prbe.ai", True),
    ("http://api.research.prbe.ai", False), ("https://evil-notprbe.ai", False),
    ("https://prbe.ai.evil.example", False), ("https://self-host.example", False),
])
def test_analytics_policy_uses_active_context_and_env_backend(reviewed, monkeypatch, base, allowed):
    import os
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    path = os.environ["PROBE_CONFIG_PATH"]
    from pathlib import Path
    Path(path).write_text(json.dumps({"version":2,"current_context":"private", "contexts":{
        "default":{"base_url":"https://api.research.prbe.ai"},
        "private":{"base_url":base,"token":"never-return-this"},
    }}))
    monkeypatch.setattr(d, "_client", lambda: pytest.fail("Policy must not authenticate"))
    assert d.dispatch({"op":"analytics_policy"}) == {"enabled":allowed,"resolved":True}
    monkeypatch.setenv("PROBE_BASE_URL", "https://self-host.example")
    assert d.dispatch({"op":"analytics_policy"}) == {"enabled":False,"resolved":True}


def test_analytics_policy_fails_closed_on_unreadable_configuration(reviewed, monkeypatch):
    from pathlib import Path
    import os
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    Path(os.environ["PROBE_CONFIG_PATH"]).write_text("not-json")
    assert d.dispatch({"op":"analytics_policy"}) == {"enabled":False,"resolved":False}


def test_desktop_admission_stamps_origin_without_passing_marker_to_worker(reviewed, monkeypatch):
    from probe.cli import telemetry
    h, row, launches = reviewed
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setenv("PROBE_DESKTOP_HUMAN", "1")
    records = []
    class Sender:
        def put(self, record): records.append(record)
    monkeypatch.setattr(telemetry, "_ensure_sender", lambda: Sender())
    p = d.preview_backfill({"sessionIds":[f"claude_code:{row.session_id}"]})
    result = d.dispatch({"op":"start_backfill","previewId":p["id"]})
    origin = import_jobs.get_job(result[0]["id"])["origin"]
    assert origin["invoked_by"] == "human" and origin["surface"] == "desktop"
    assert "PROBE_DESKTOP_HUMAN" not in launches[0][1]["env"]
    assert records[0]["event"] == telemetry.EVENT_IMPORT_JOB_ENQUEUED


def _journal_session(tmp_path, monkeypatch, lines=3):
    """A session its recorder delivered (a real journal under this HOME's
    default folder), plus one line the server has not taken yet."""
    from probe.tap_core.session_journal import Journal
    from tests.test_transcript_protocol3 import CUSTOMER, DoorWire, _drain, _session, _start, _user, _write

    monkeypatch.setenv("HOME", str(tmp_path))
    door = DoorWire(offers=True)
    sid, path = _session(tmp_path, [_user("x", f"turn {i}", i) for i in range(lines)])
    journal = Journal(door.base_url, CUSTOMER, door.source, directory=tmp_path / ".probe" / "transcripts-v2")
    assert journal.claim_live(sid)  # its recorder runs: the journal it holds is the one read
    _start(journal, door, sid, path)
    _drain(journal, door, sid)
    _write(path, [_user(sid, "waiting", 99)])
    return sid, journal


def test_last_received_and_pending_are_the_live_sessions_journal(monkeypatch, tmp_path):
    """D29: what the service lists per session, from the recorder's journal --
    never the protocol-1 `state.db`, whose outbox stopped moving at #1415."""
    import sqlite3

    from probe.harness import get_registry
    from probe.service import client

    sid, journal = _journal_session(tmp_path, monkeypatch)
    # An old protocol-1 store with an outbox and a last post: never read again.
    claude = next(row for row in get_registry().captured() if row.id == "claude_code")
    state = claude.capture.state_dir()
    state.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(state / "state.db")
    conn.executescript(
        "CREATE TABLE outbox (id INTEGER PRIMARY KEY, session_id TEXT); CREATE TABLE meta (k TEXT PRIMARY KEY, v TEXT);"
        "INSERT INTO outbox (session_id) VALUES ('a'), ('b');"
        "INSERT INTO meta VALUES ('last_successful_post_at', '1761100000');"
    )
    conn.commit()
    conn.close()
    # A service from before receipts: the CLI reads the journal itself.
    monkeypatch.setattr(client, "call", lambda *a, **k: {"sessions": [
        {"sid": sid, "harness": "claude_code", "alive": True}]})
    result = d.snapshot_delivery()
    rows = {row["source"]: row for row in result["agents"]}
    assert rows["claude_code"]["pending"] == 1
    assert rows["claude_code"]["lastReceived"] is not None and rows["claude_code"]["lastReceived"] != "2025-10-22T02:26:40Z"
    assert rows["codex"]["pending"] is None and rows["codex"]["lastReceived"] is None
    assert "recorder's own" in result["reason"]
    journal.close()


def test_receipts_the_service_lists_are_used_as_they_are(monkeypatch, tmp_path):
    from probe.service import client, receipts

    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(receipts, "read", lambda *a: (_ for _ in ()).throw(AssertionError("read again")))

    def found(at, lines):
        return {"last_line": 4, "received_bytes": 10, "received_at": at, "pending_bytes": 5, "pending_lines": lines,
                "pending_batch": False, "finalized": False, "retrying": False}

    monkeypatch.setattr(client, "call", lambda *a, **k: {"sessions": [
        {"sid": "a", "harness": "codex", "alive": True, "receipts": found(1761100000.0, 2)},
        {"sid": "b", "harness": "codex", "alive": False, "receipts": found(1761100060.0, 3)},
        {"sid": "c", "harness": "pi", "alive": True, "receipts": None},
    ]})
    result = d.snapshot_delivery()
    rows = {row["source"]: row for row in result["agents"]}
    assert (rows["codex"]["lastReceived"], rows["codex"]["pending"], rows["codex"]["activeAgents"]) == (
        "2025-10-22T02:27:40Z", 5, 1)
    assert (rows["pi"]["lastReceived"], rows["pi"]["pending"], rows["pi"]["activeAgents"]) == (None, None, 1)
    # No service, no sessions: nothing is known, and the reason says so.
    monkeypatch.setattr(client, "call", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    unknown = d.snapshot_delivery()
    assert all((a["lastReceived"], a["pending"]) == (None, None) for a in unknown["agents"])
    assert "receipts are unavailable" in unknown["reason"]


def test_the_cli_command_and_the_service_child_share_one_responder():
    text, code = d.respond(b'{"op":"shell"}')
    assert (json.loads(text), code) == ({"v": 1, "ok": False, "error": "Unknown desktop operation."}, 1)
    result = CliRunner().invoke(d.app, ["--json"], input='{"op":"shell"}')
    assert (result.stdout.strip(), result.exit_code) == (text, code)
    assert d.respond(b"x" * (d.MAX_INPUT + 1))[0] == json.dumps(
        {"v": 1, "ok": False, "error": "Desktop request exceeds 1 MiB."})


def test_delivery_counts_only_the_signed_in_accounts_receipts(monkeypatch, tmp_path):
    """Each receipt carries its journal's scope; the delivery op overlays only
    the ones of the account it answers for (`identity`)."""
    from probe.service import client

    def found(customer, lines):
        return {"last_line": 4, "received_bytes": 10, "received_at": 1761100000.0, "pending_bytes": 5,
                "pending_lines": lines, "pending_batch": False, "finalized": False, "retrying": False,
                "scope": {"backend": "api.example.invalid", "customer": customer}}

    monkeypatch.setattr(client, "call", lambda *a, **k: {"sessions": [
        {"sid": "a", "harness": "codex", "alive": True, "receipts": found("mine", 2)},
        {"sid": "b", "harness": "codex", "alive": True, "receipts": found("someone-else", 900)},
    ]})
    identity = {"customer_id": "mine", "user_id": "u", "base_url": "https://API.example.invalid/", "context": "x"}
    rows = {row["source"]: row for row in d.snapshot_delivery(identity)["agents"]}
    assert rows["codex"]["pending"] == 2
    other = {**identity, "customer_id": "nobody"}
    rows = {row["source"]: row for row in d.snapshot_delivery(other)["agents"]}
    assert (rows["codex"]["pending"], rows["codex"]["lastReceived"]) == (None, None)
