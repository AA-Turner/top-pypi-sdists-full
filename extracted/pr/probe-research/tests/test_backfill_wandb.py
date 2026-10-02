"""Real SDK HTTP serialization and SQLite recovery; the remote service is fake.

The backend integration suite separately proves the canonical source reservation
against real databases. These tests exercise the producer, not a second backend.
"""

import copy
import json
import sqlite3
from uuid import uuid4

import httpx
import pytest

from probe.cli import backfill_wandb as wb
from probe.cli.backfill_coverage import Coverage, CoverageError, Scope
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.transport import Transport

PROJECT = "00000000-0000-4000-8000-000000000001"
OTHER = "00000000-0000-4000-8000-000000000002"
CONNECTION = "00000000-0000-4000-8000-000000000003"
WORKSPACE = "00000000-0000-4000-8000-000000000004"
SOURCE = "00000000-0000-4000-8000-000000000005"
ATTACHMENT = "00000000-0000-4000-8000-000000000006"


class Remote:
    def __init__(self, path):
        self.path = path
        self.requests = []
        self.attachments = {}
        self.jobs = {}
        self.lose = None
        self.override = None
        self.bound_project = None
        self.unavailable = False

    def saved(self):
        with sqlite3.connect(self.path) as conn:
            row = conn.execute("SELECT value FROM meta WHERE key=?", (wb.KEY,)).fetchone()
        return json.loads(row[0]) if row else None

    def respond(self, request):
        path = request.url.path
        body = json.loads(request.content) if request.content else None
        self.requests.append((request.method, path, body))
        assert "x-probe-agent-session" not in request.headers
        assert "x-probe-agent" not in request.headers
        assert "x-probe-session" not in request.headers
        if self.unavailable:
            return httpx.Response(503, json={"detail": "synthetic outage"})
        if path == "/v1/integrations/mirror/connections":
            return httpx.Response(
                200,
                json=[
                    {
                        "id": CONNECTION,
                        "source": "wandb",
                        "status": "active",
                        "has_credential": True,
                        "features": ["project_attachments"],
                    },
                    {
                        "id": str(uuid4()),
                        "source": "benchling",
                        "status": "active",
                        "has_credential": True,
                        "features": ["initial_sweep"],
                    },
                ],
            )
        if path.endswith("/scope-options"):
            return httpx.Response(
                200,
                json=[
                    {
                        "external_id": "lab/training",
                        "label": "training",
                        "attachment_id": ATTACHMENT if self.bound_project else None,
                        "project_id": self.bound_project,
                        "state": "active",
                    }
                ],
            )
        project = path.split("/")[3]
        if request.method == "POST":
            # Read a separate SQLite connection AT the HTTP boundary: an
            # in-memory intent cannot satisfy this prerequisite.
            saved = self.saved()
            assert saved and saved["scope"]["customer_id"] == "synthetic"
            intent = next(i for i in saved["imports"] if i["project_id"] == project)
            if path.endswith("/wandb-sources"):
                assert body == {
                    "connection_id": intent["connection_id"],
                    "external_id": intent["external_id"],
                }
                if self.bound_project and self.bound_project != project:
                    return httpx.Response(409, json={"detail": "source belongs to another project"})
                row = self.attachments.setdefault(
                    intent["external_id"],
                    {
                        "id": ATTACHMENT,
                        "connection_id": CONNECTION,
                        "project_id": project,
                        "external_id": intent["external_id"],
                        "state": "active",
                        "sync_enabled": True,
                        "features": ["backfill", "live_sync"],
                    },
                )
                operation = "attach"
            else:
                assert intent["attachment_id"] == ATTACHMENT
                assert body == {"idempotency_key": intent["idempotency_key"]}
                assert path.endswith("/backfills") or path.endswith("/retry")
                row = self.jobs.setdefault(
                    body["idempotency_key"],
                    {
                        "id": str(uuid4()),
                        "attachment_id": ATTACHMENT,
                        "project_id": project,
                        "connection_id": CONNECTION,
                        "source": "wandb",
                        "workspace_id": WORKSPACE,
                        "scope": [{"external_id": intent["external_id"], "label": "training"}],
                        "state": "queued",
                        "counts": {},
                        "warnings": [],
                        "processed_count": 0,
                    },
                )
                operation = "launch"
            if self.lose == operation:
                self.lose = None
                raise httpx.ReadTimeout("response lost after acceptance", request=request)
            response = copy.deepcopy(row)
            if self.override:
                response.update(self.override)
            return httpx.Response(201, json=response)
        assert request.method == "GET" and "/backfills/" in path
        row = next(job for job in self.jobs.values() if job["id"] == path.rsplit("/", 1)[1])
        return httpx.Response(200, json={**row, **(self.override or {})})


@pytest.fixture
def harness(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_SESSION_ID", "ambient-session-must-not-link")
    monkeypatch.setenv("CODEX_THREAD_ID", "ambient-session-must-not-link")
    scope = Scope("https://api.invalid", "synthetic", WORKSPACE, None)
    coverage = Coverage(tmp_path / "coverage", scope, SOURCE)
    coverage.directory.mkdir()
    with coverage.writer():
        for name, project in [("one.py", PROJECT), ("two.py", OTHER)]:
            coverage.conn.execute(
                "INSERT INTO files(path,project_id,project_slug) VALUES (?,?,?)",
                (name, project, name.removesuffix(".py")),
            )
        coverage.conn.commit()
        remote = Remote(coverage.path)
        settings = Settings(base_url="https://api.invalid", token="synthetic")
        with httpx.Client(
            base_url=settings.base_url, transport=httpx.MockTransport(remote.respond)
        ) as http:
            transport = Transport(settings, client=http, max_retries=0, attribution="backfill")
            with Client(
                settings=settings,
                transport=transport,
                async_writes=True,
                auto_drain=False,
                drain_interval=9999,
                spool_dir=tmp_path / "outbox",
            ) as client:
                yield client, coverage, remote


def admit(harness, **kw):
    client, coverage, _ = harness
    return wb.admit_reviewed_history(
        client,
        coverage,
        project_id=kw.get("project_id", PROJECT),
        connection_id=CONNECTION,
        external_id=kw.get("external_id", "lab/training"),
    )


def answer(monkeypatch, responses):
    responses = iter(responses)
    seen = []

    def review(title, lines, choices):
        seen.append((title, lines, choices))
        response = next(responses)
        return choices[response][1] if isinstance(response, int) else response

    monkeypatch.setattr(wb.tui, "review", review)
    return seen


@pytest.mark.parametrize("lost", ["attach", "launch"])
def test_lost_ack_reuses_committed_mapping_and_source_job_after_sqlite_reload(harness, lost):
    client, coverage, remote = harness
    remote.lose = lost
    with pytest.raises(Exception):
        admit(harness)
    saved = remote.saved()
    key = saved["imports"][0]["idempotency_key"]
    before = len(remote.requests)
    wb.run(client, coverage)  # Unknown admission is retained headlessly, not resubmitted.
    assert len(remote.requests) == before
    result = admit(harness)
    assert result["idempotency_key"] == key
    assert len(remote.attachments) == len(remote.jobs) == 1
    before = len(remote.requests)
    admit(harness)
    assert [method for method, _, _ in remote.requests[before:]] == ["GET"]
    assert not client.journal.pending()  # strict API responses cannot be replaced by queue ACKs


def test_response_received_but_local_receipt_commit_fails_then_same_job_recovers(
    harness, monkeypatch
):
    _, coverage, remote = harness
    original = coverage.put_meta

    def fail_receipt(key, state):
        if key == wb.KEY and state["imports"][0].get("job_id"):
            raise OSError("synthetic failed commit")
        original(key, state)

    monkeypatch.setattr(coverage, "put_meta", fail_receipt)
    with pytest.raises(OSError):
        admit(harness)
    assert len(remote.jobs) == 1
    assert remote.saved()["imports"][0]["job_id"] is None
    monkeypatch.setattr(coverage, "put_meta", original)
    assert admit(harness)["job_id"] == next(iter(remote.jobs.values()))["id"]
    assert len(remote.jobs) == 1


def test_failed_intent_commit_never_sends_even_through_interactive_lane(harness, monkeypatch):
    client, coverage, remote = harness
    answer(monkeypatch, ["wandb", 1, 1, 1, "import"])
    monkeypatch.setattr(coverage, "put_meta", lambda *a: (_ for _ in ()).throw(OSError("disk")))
    lines = wb.run(client, coverage, interactive=True, offer=True)
    assert "pending" in " ".join(lines)
    assert not [r for r in remote.requests if r[0] != "GET"]
    assert not remote.attachments and not remote.jobs


def test_picker_maps_to_explicit_second_project_and_preserves_live_source(harness, monkeypatch):
    client, coverage, remote = harness
    screens = answer(monkeypatch, ["wandb", 1, 1, 2, "import"])
    wb.run(client, coverage, interactive=True, offer=True)
    row = remote.saved()["imports"][0]
    assert row["project_id"] == OTHER
    assert remote.attachments["lab/training"]["sync_enabled"] is True
    assert len(remote.jobs) == 1
    assert all(method not in {"PATCH", "DELETE"} for method, _, _ in remote.requests)
    assert screens[-1][0] == "Review W&B history import"
    assert f"Probe destination: two · {OTHER}" in screens[-1][1]
    assert "W&B source: lab/training" in screens[-1][1]
    assert screens[-1][2][0][1] == "skip"


@pytest.mark.parametrize("stage", range(5))
@pytest.mark.parametrize("response", [0, wb.tui.BACK, None], ids=["default-skip", "escape", "ctrl-c"])
def test_optional_gate_cancellation_never_saves_or_admits_history(
    harness, monkeypatch, stage, response
):
    client, coverage, remote = harness
    proceed = ["wandb", 1, 1, 1]
    answer(monkeypatch, [*proceed[:stage], response])
    if response is None:
        with pytest.raises(KeyboardInterrupt):
            wb.run(client, coverage, interactive=True, offer=True)
    else:
        assert wb.run(client, coverage, interactive=True, offer=True) == []
    assert coverage.meta(wb.KEY) is None
    assert not remote.attachments and not remote.jobs
    assert all(method == "GET" for method, _, _ in remote.requests)


def test_source_already_bound_elsewhere_is_not_moved_or_duplicated(harness, monkeypatch):
    client, coverage, remote = harness
    remote.bound_project = OTHER
    answer(monkeypatch, ["wandb", 1, 1, 1])
    lines = wb.run(client, coverage, interactive=True, offer=True)
    assert "already attached" in " ".join(lines)
    assert not remote.saved() and not remote.attachments and not remote.jobs


@pytest.mark.parametrize("interactive,yes", [(False, False), (False, True), (True, True)])
def test_no_saved_selection_means_no_headless_offer_or_provider_calls(
    harness, monkeypatch, interactive, yes
):
    client, coverage, remote = harness
    monkeypatch.setattr(wb.tui, "review", lambda *a, **kw: pytest.fail("implicit offer"))
    assert wb.run(client, coverage, interactive=interactive, yes=yes, offer=True) == []
    assert not remote.requests and coverage.meta(wb.KEY) is None


@pytest.mark.parametrize(
    "override",
    [
        {"project_id": OTHER},
        {"experiment_id": OTHER},
        {"connection_id": OTHER},
        {"external_id": "other/project"},
        {"state": "revoked"},
    ],
)
def test_attachment_identity_mismatch_never_advances_to_history(harness, override):
    _, _, remote = harness
    remote.override = override
    with pytest.raises(CoverageError):
        admit(harness)
    assert not remote.jobs
    assert remote.saved()["imports"][0]["attachment_id"] is None


@pytest.mark.parametrize(
    "override",
    [
        {"project_id": OTHER},
        {"experiment_id": OTHER},
        {"workspace_id": OTHER},
        {"attachment_id": OTHER},
        {"scope": [{"external_id": "other/project"}]},
        {"state": "unknown"},
    ],
)
def test_job_identity_mismatch_retains_unknown_admission(harness, override):
    _, _, remote = harness
    remote.lose = "launch"
    with pytest.raises(Exception):
        admit(harness)
    remote.override = override
    with pytest.raises(CoverageError):
        admit(harness)
    assert len(remote.jobs) == 1 and remote.saved()["imports"][0]["job_id"] is None


def test_job_failure_is_status_only_until_explicit_retry_and_retry_key_is_durable(
    harness, monkeypatch
):
    client, coverage, remote = harness
    original = admit(harness)
    remote.jobs[original["idempotency_key"]]["state"] = "failed"
    before = len(remote.requests)
    wb.run(client, coverage)
    assert [r[0] for r in remote.requests[before:]] == ["GET"]
    answer(monkeypatch, ["skip", "retry"])
    wb.run(client, coverage, interactive=True, offer=True)
    current = remote.saved()["imports"][0]
    assert len(remote.jobs) == 2 and current["retry_of"] == original["job_id"]
    assert current["idempotency_key"] != original["idempotency_key"]
    assert current["previous_jobs"][0]["receipt"]["id"] == original["job_id"]
    assert remote.requests[-1][1].endswith("/retry")


@pytest.mark.parametrize("response", [0, wb.tui.BACK, None], ids=["default-skip", "escape", "ctrl-c"])
def test_retry_cancellation_preserves_the_existing_job(harness, monkeypatch, response):
    client, coverage, remote = harness
    original = admit(harness)
    remote.jobs[original["idempotency_key"]]["state"] = "failed"
    before = len(remote.requests)
    answer(monkeypatch, ["skip", response])
    if response is None:
        with pytest.raises(KeyboardInterrupt):
            wb.run(client, coverage, interactive=True, offer=True)
    else:
        wb.run(client, coverage, interactive=True, offer=True)
    current = remote.saved()["imports"][0]
    assert current["job_id"] == original["job_id"]
    assert current["idempotency_key"] == original["idempotency_key"]
    assert len(remote.jobs) == 1
    assert [request[0] for request in remote.requests[before:]] == ["GET"]


def test_scope_change_refuses_saved_mapping_before_any_remote_call(harness):
    client, coverage, remote = harness
    admit(harness)
    saved = coverage.meta(wb.KEY)
    saved["scope"]["customer_id"] = "other"
    coverage.put_meta(wb.KEY, saved)
    before = len(remote.requests)
    assert "needs review" in " ".join(wb.run(client, coverage))
    assert len(remote.requests) == before


def test_outage_remains_visible_and_does_not_change_file_or_reconstruction_state(harness):
    client, coverage, remote = harness
    admit(harness)
    coverage.put_meta("last_verified_complete", True)
    coverage.put_meta("reconstruction:test", {"input_id": "retained", "publication": "published"})
    files = coverage.rows()
    remote.unavailable = True
    assert "File delivery continues" in " ".join(wb.run(client, coverage))
    assert coverage.rows() == files and coverage.meta("last_verified_complete") is True
    assert coverage.meta("reconstruction:test")["input_id"] == "retained"


def test_completed_history_reports_source_backed_access_not_copied_metrics(harness):
    client, coverage, remote = harness
    item = admit(harness)
    remote.jobs[item["idempotency_key"]]["state"] = "completed"
    text = " ".join(wb.run(client, coverage))
    assert "History discovery completed" in text and "connected W&B source" in text
    assert not any("/metrics" in path or "/artifacts" in path for _, path, _ in remote.requests)


@pytest.mark.parametrize("replacement", [None, OTHER])
def test_saved_experiment_destination_cannot_be_replaced_on_restart(harness, replacement):
    _, coverage, remote = harness
    selected = wb.record_reviewed_selection(
        coverage, project_id=PROJECT, connection_id=CONNECTION,
        external_id="lab/training", experiment_id=SOURCE,
    )
    with pytest.raises(CoverageError, match="different saved mapping"):
        wb.record_reviewed_selection(
            coverage, project_id=PROJECT, connection_id=CONNECTION,
            external_id="lab/training", experiment_id=replacement,
        )
    assert remote.saved()["imports"] == [selected]
    assert not remote.requests
