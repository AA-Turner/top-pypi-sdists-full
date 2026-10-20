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
    assert all(row["pending"] is None and row["lastReceived"] is None for row in result["agents"])
    monkeypatch.setattr(client, "call", lambda *a, **k: (_ for _ in ()).throw(OSError()))
    assert all(row["activeAgents"] is None for row in d.snapshot_delivery()["agents"])


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
    assert all(job["report"] == [] for job in first["jobs"] + first["activeJobs"])
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
