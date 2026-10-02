"""Recovery through persisted coverage state, with only synthetic local inputs."""

from pathlib import Path

import pytest

from probe.cli import backfill_reconstruction as reconstruction
from probe.cli.backfill import Agent
from probe.cli.backfill_coverage import Coverage, Scope


class Client:
    def __init__(self):
        self.transport = self
        self.status = {"state": "stale", "has_summary": False}
        self.generation = {}
        self.posts = []
        self.fail_post = False
        self.post_error = None

    def presign_download_batch(self, ids):
        return {"items": {ident: {"download_url": "https://example.invalid/blob"} for ident in ids}}

    def get_project(self, project_id):
        return {"document": "", "metadata": {"summary": {"generation": self.generation}}}

    def get(self, path):
        if path.endswith("/overview/status"):
            from probe.sdk.errors import NotFoundError

            raise NotFoundError("Legacy-only synthetic server", status=404)
        assert path.endswith("/summary/status")
        return self.status

    def post(self, path, body, *, idempotent):
        assert path.endswith("/summary/regenerate")
        assert idempotent is False
        self.posts.append(path)
        if self.fail_post:
            raise ConnectionError("synthetic connection failure before server acceptance")
        if self.post_error is not None:
            raise self.post_error
        self.status = {"state": "generating", "has_summary": False, "detail": "pending"}
        return {"state": "generating"}


def open_coverage(directory: Path) -> Coverage:
    directory.mkdir(exist_ok=True)
    return Coverage(directory, Scope("https://example.invalid", "synthetic", "workspace"), "source")


def accept_file(coverage, path, project_id, *, changed=False):
    project = {
        "id": project_id,
        "slug": project_id,
        "customer_id": coverage.scope.customer_id,
        "workspace_id": coverage.scope.workspace_id,
    }
    coverage.approve({path: project}, changed=changed)
    row = next(row for row in coverage.rows() if row["path"] == path)
    intent = coverage.intend(row, reference=False)
    coverage.accept_receipt(
        intent["correlation"],
        {
            "correlation": intent["correlation"],
            "state": "delivered",
            "status": "complete",
            "artifact_id": f"artifact-{project_id}",
            "anchor": "project",
            "anchor_id": project_id,
            "name": path,
            "content_hash": row["approved_hash"],
            "size_bytes": row["size"],
            "is_reference": False,
            "readable": True,
        },
    )


def test_restarted_bounded_pass_reaches_later_projects_and_revisits_changed_inputs(
    tmp_path, monkeypatch
):
    folder = tmp_path / "files"
    folder.mkdir()
    paths = [f"file-{index:02d}.txt" for index in range(21)]
    for path in paths:
        (folder / path).write_text(f"Initial contents of {path}.\n")
    directory = tmp_path / "coverage"
    generated = []

    def generate(inputs, directory, *, agent):
        generated.append(inputs["project_id"])
        return inputs["sources"]["F001"]["text"]

    monkeypatch.setattr(reconstruction, "_generate", generate)
    client = Client()
    with open_coverage(directory).writer() as coverage:
        coverage.observe(folder, paths)
        for index, path in enumerate(paths):
            accept_file(coverage, path, f"project-{index:02d}")
        lines = reconstruction.complete_reconstruction(
            client, folder, coverage, None, agent=Agent.CLAUDE, interactive=False, yes=True
        )
        original = coverage.meta("reconstruction:project-00")
        assert len(generated) == reconstruction.MAX_PROJECTS
        assert coverage.meta("reconstruction:project-20") is None
        assert any("rerun to continue" in line for line in lines)

    # Reopen the actual SQLite coverage store and change a previously completed
    # input: both the deferred project and the changed earlier one must run.
    (folder / paths[0]).write_text("Revised evidence for the earlier project.\n")
    with open_coverage(directory).writer() as coverage:
        coverage.observe(folder, paths)
        accept_file(coverage, paths[0], "project-00", changed=True)
        before = len(generated)
        reconstruction.complete_reconstruction(
            client, folder, coverage, None, agent=Agent.CLAUDE, interactive=False, yes=True
        )
        assert generated[before:] == ["project-20", "project-00"]
        assert all(coverage.meta(f"reconstruction:project-{index:02d}") for index in range(21))
        updated = coverage.meta("reconstruction:project-00")
        assert updated["input_id"] != original["input_id"]
        assert Path(updated["draft_path"]).read_text() == (folder / paths[0]).read_text()
        assert coverage.meta(f"reconstruction:project-00:{original['input_id']}") == original

    with open_coverage(directory).writer() as coverage:
        before = len(generated)
        reconstruction.complete_reconstruction(
            client, folder, coverage, None, agent=Agent.CLAUDE, interactive=False, yes=True
        )
        assert len(generated) == before  # unchanged drafts still avoid another model call
    assert client.posts == []


def test_pre_send_failure_can_be_reviewed_and_retried_after_restart(tmp_path, monkeypatch):
    directory = tmp_path / "coverage"
    client = Client()
    client.fail_post = True
    prompts = []

    def confirm(prompt):
        prompts.append(prompt)
        return True

    monkeypatch.setattr(reconstruction, "_confirm", confirm)
    key = "reconstruction:project"
    with open_coverage(directory).writer() as coverage:
        state = {"project_id": "project", "publication": {"state": "published"}}
        with pytest.raises(ConnectionError):
            reconstruction._summary(client, coverage, key, state, interactive=True, yes=False)
        assert coverage.meta(key)["summary"]["state"] == "unknown"

    client.fail_post = False
    with open_coverage(directory).writer() as coverage:
        state = coverage.meta(key)
        result = reconstruction._summary(client, coverage, key, state, interactive=True, yes=False)
        assert "refresh requested" in result
        assert "no active refresh" in prompts[-1]
        assert "Retry" in prompts[-1]
        assert coverage.meta(key)["summary"]["state"] == "pending"
    assert len(client.posts) == 2


@pytest.mark.parametrize(
    "interactive,yes,consent", [(False, False, True), (True, True, True), (True, False, False)]
)
def test_uncertain_request_never_retries_without_explicit_review(
    tmp_path, monkeypatch, interactive, yes, consent
):
    client = Client()
    prompts = []

    def confirm(prompt):
        prompts.append(prompt)
        return consent

    monkeypatch.setattr(reconstruction, "_confirm", confirm)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {
            "project_id": "project",
            "publication": {"state": "published"},
            "summary": {"state": "unknown", "requested_at": "2026-01-01T00:00:00+00:00"},
        }
        reconstruction._summary(client, coverage, "key", state, interactive=interactive, yes=yes)
        assert coverage.meta("key")["summary"]["state"] == "unknown"
    assert client.posts == []
    assert bool(prompts) == (interactive and not yes)


@pytest.mark.parametrize("state", ["unknown", "pending", "failed"])
@pytest.mark.parametrize(
    "status",
    [
        {"state": "generating", "detail": "pending"},
        {"state": "stale", "detail": "gateway_down"},
        {"state": "future_status"},
    ],
)
def test_active_or_unverifiable_request_never_offers_duplicate_refresh(
    tmp_path, monkeypatch, state, status
):
    client = Client()
    client.status = status

    def unexpected_confirmation(prompt):
        pytest.fail("an active or unverifiable refresh must not offer another request")

    monkeypatch.setattr(reconstruction, "_confirm", unexpected_confirmation)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        saved = {
            "project_id": "project",
            "summary": {"state": state, "requested_at": "2026-01-01T00:00:00+00:00"},
        }
        reconstruction._summary(client, coverage, "key", saved, interactive=True, yes=False)
    assert client.posts == []


def test_accepted_lost_ack_reconciles_completion_without_retry(tmp_path, monkeypatch):
    client = Client()
    client.status = {"state": "fresh", "has_summary": True}
    client.generation = {"generated_at": "2026-01-02T00:00:00+00:00", "prompt_version": "test"}

    def unexpected_confirmation(prompt):
        pytest.fail("the accepted request already completed")

    monkeypatch.setattr(reconstruction, "_confirm", unexpected_confirmation)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {
            "project_id": "project",
            "summary": {"state": "unknown", "requested_at": "2026-01-01T00:00:00+00:00"},
        }
        reconstruction._summary(client, coverage, "key", state, interactive=True, yes=False)
        assert coverage.meta("key")["summary"]["state"] == "complete"
    assert client.posts == []


def _refusal(detail):
    from probe.sdk.errors import error_for

    return error_for(409, detail)


def _paused_refusal():
    from probe.sdk.errors import GENERATION_PAUSED

    # A server message the CLI must NOT print: it says its own sentence.
    return _refusal({"code": GENERATION_PAUSED, "message": "\x1b[2Jserver text\nrefresh requested"})


def test_a_paused_refusal_is_a_definite_answer_not_a_pending_request(tmp_path, monkeypatch):
    """The team's page generation is switched off (research-os 0245): the server
    refused the press and queued nothing. That is recorded as `paused` and said
    in the CLI's own words -- never the server's text on the terminal."""
    client = Client()
    client.post_error = _paused_refusal()
    monkeypatch.setattr(reconstruction, "_confirm", lambda prompt: True)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {"project_id": "project", "publication": {"state": "published"}}
        result = reconstruction._summary(client, coverage, "key", state, interactive=True, yes=False)
        saved = coverage.meta("key")["summary"]
    assert result == (
        "project: Optional AI Summary not requested: page updates are paused for your team. "
        "Nothing was queued."
    )
    assert "server text" not in result and "\x1b" not in result
    assert saved["state"] == "paused"
    assert "requested_at" not in saved
    assert len(client.posts) == 1


def test_a_later_run_asks_afresh_after_a_paused_refusal(tmp_path, monkeypatch):
    """`paused` is not a previous request: with nothing running, the next run
    asks the ordinary question (never "Retry"), and a new request starts with
    no leftover diagnostic."""
    client = Client()
    prompts = []

    def confirm(prompt):
        prompts.append(prompt)
        return True

    monkeypatch.setattr(reconstruction, "_confirm", confirm)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {
            "project_id": "project",
            "publication": {"state": "published"},
            "summary": {"state": "paused", "detail": "generation_paused"},
        }
        result = reconstruction._summary(client, coverage, "key", state, interactive=True, yes=False)
        saved = coverage.meta("key")["summary"]
    assert "refresh requested" in result
    assert prompts and "Retry" not in prompts[-1] and "Request a separate" in prompts[-1]
    assert saved["state"] == "pending" and "detail" not in saved
    assert len(client.posts) == 1


@pytest.mark.parametrize(
    "status,said",
    [
        ({"state": "generating", "detail": "pending"}, "already in progress"),
        ({"state": "stale", "detail": "gateway_down"}, "could not be confirmed"),
        ({"state": "future_status"}, "could not be confirmed"),
    ],
)
def test_a_paused_record_never_requests_beside_work_already_running(
    tmp_path, monkeypatch, status, said
):
    """Once generation is back on, the automatic lane or a teammate may already
    be refreshing: a paused record is reconciled first, like a previous
    request, and does not pay for a second refresh -- nor claims that job as
    its own."""
    client = Client()
    client.status = status

    def unexpected_confirmation(prompt):
        pytest.fail("work already in flight must not be offered another request")

    monkeypatch.setattr(reconstruction, "_confirm", unexpected_confirmation)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {
            "project_id": "project",
            "publication": {"state": "published"},
            "summary": {"state": "paused", "detail": "generation_paused"},
        }
        result = reconstruction._summary(client, coverage, "key", state, interactive=True, yes=False)
        assert coverage.meta("key")["summary"]["state"] == "paused"
    # Only a job the server reports is "in progress"; an outage or an unknown
    # shape is said as uncertainty, not as work to wait on.
    assert said in result
    assert client.posts == []


def test_a_paused_refusal_is_not_re_requested_without_review(tmp_path, monkeypatch):
    client = Client()

    def unexpected_confirmation(prompt):
        pytest.fail("a non-interactive run must not ask")

    monkeypatch.setattr(reconstruction, "_confirm", unexpected_confirmation)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {
            "project_id": "project",
            "publication": {"state": "published"},
            "summary": {"state": "paused", "detail": "generation_paused"},
        }
        result = reconstruction._summary(client, coverage, "key", state, interactive=False, yes=False)
    assert "not requested" in result
    assert client.posts == []


def test_a_retry_that_meets_the_pause_ends_paused_and_is_not_offered_again(tmp_path, monkeypatch):
    """The retry path: an `unknown` request, no active refresh, the retry is
    confirmed -- and generation is switched off. It ends `paused` without its
    old requested_at, and the next run asks the ordinary question."""
    directory = tmp_path / "coverage"
    client = Client()
    client.post_error = _paused_refusal()
    prompts = []

    def confirm(prompt):
        prompts.append(prompt)
        return True

    monkeypatch.setattr(reconstruction, "_confirm", confirm)
    key = "reconstruction:project"
    with open_coverage(directory).writer() as coverage:
        state = {
            "project_id": "project",
            "publication": {"state": "published"},
            "summary": {"state": "unknown", "requested_at": "2026-01-01T00:00:00+00:00"},
        }
        reconstruction._summary(client, coverage, key, state, interactive=True, yes=False)
        saved = coverage.meta(key)["summary"]
        assert saved["state"] == "paused" and "requested_at" not in saved
    assert "Retry" in prompts[-1]

    client.post_error = None
    with open_coverage(directory).writer() as coverage:
        state = coverage.meta(key)
        reconstruction._summary(client, coverage, key, state, interactive=True, yes=False)
    assert "Retry" not in prompts[-1] and "Request a separate" in prompts[-1]


@pytest.mark.parametrize(
    "detail",
    [{"code": "something_else", "message": "conflict"}, "upstream conflict", None],
    ids=["other-code", "text-body", "no-body"],
)
def test_any_other_conflict_is_still_an_unknown_request(tmp_path, monkeypatch, detail):
    """Only the paused code is a definite answer; any other 409 -- another
    code, a non-JSON body, no body -- keeps the reconcile-before-retry path."""
    from probe.sdk.errors import ConflictError

    client = Client()
    client.post_error = _refusal(detail)
    monkeypatch.setattr(reconstruction, "_confirm", lambda prompt: True)
    with open_coverage(tmp_path / "coverage").writer() as coverage:
        state = {"project_id": "project", "publication": {"state": "published"}}
        with pytest.raises(ConflictError):
            reconstruction._summary(client, coverage, "key", state, interactive=True, yes=False)
        assert coverage.meta("key")["summary"]["state"] == "unknown"
