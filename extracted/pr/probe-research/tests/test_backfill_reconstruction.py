"""Durable drafts, explicit review and independent summary stages."""

import hashlib
import json
import sqlite3
from dataclasses import dataclass

import pytest

from probe.cli import backfill_reconstruction as rec
from probe.cli.backfill_reconstruction import _generate as generate_draft


@dataclass
class Scope:
    customer_id: str = "tenant"
    workspace_id: str = "workspace"
    backend: str = "https://api.invalid"


class Coverage:
    def __init__(self, root):
        self.directory = root / "state"
        self.directory.mkdir()
        self.source_id = "source"
        self.scope = Scope()
        self.conn = sqlite3.connect(self.directory / "coverage.sqlite")
        self.conn.execute("CREATE TABLE versions(correlation TEXT, receipt TEXT)")
        self.conn.execute("CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT)")
        content = "The model uses a frozen encoder. No experiment measurements have been recorded."
        (root / "design.md").write_text(content)
        digest = hashlib.sha256(content.encode()).hexdigest()
        self.file_rows = [
            {
                "path": "design.md",
                "approved_hash": digest,
                "project_id": "p",
                "project_slug": "project",
                "correlation": "c",
            }
        ]
        receipt = {
            "state": "delivered",
            "status": "complete",
            "anchor_id": "p",
            "content_hash": digest,
            "artifact_id": "artifact",
            "readable": True,
            "is_reference": False,
        }
        self.conn.execute("INSERT INTO versions VALUES ('c',?)", (json.dumps(receipt),))
        self.pending = []

    def rows(self):
        return self.file_rows

    def report(self):
        return {"queued": self.pending}

    def meta(self, key, default=None):
        row = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def put_meta(self, key, value):
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, json.dumps(value)))


class Client:
    def __init__(self):
        self.transport = self
        self.document = "Teammate's prose"
        self.writes = []
        self.summary = {}
        self.capabilities = [rec.CAPABILITY]
        self.readable = True
        self.lost_ack = False

    def presign_download_batch(self, ids):
        return (
            {
                "items": {
                    ident: {"download_url": "https://secret.invalid/temporary"} for ident in ids
                }
            }
            if self.readable
            else {}
        )

    def get_project(self, project):
        return {
            "id": project,
            "document": self.document,
            "metadata": {"summary": self.summary},
        }

    def me(self):
        return {"capabilities": self.capabilities}

    def patch(self, path, body):
        assert path.endswith("/summary-markdown")
        assert body["expected_document"] == self.document
        self.writes.append((path, body))
        self.document = body["document"]
        if self.lost_ack:
            self.lost_ack = False
            raise TimeoutError()
        return {"document": self.document}

    def post(self, path, body, **kw):
        self.writes.append((path, body))
        return {"state": "generating"}

    def get(self, path):
        if path.endswith("/overview/status"):
            from probe.sdk.errors import NotFoundError

            raise NotFoundError("Legacy-only synthetic server", status=404)
        assert path.endswith("/summary/status")
        return {
            "state": "fresh" if self.summary else "generating",
            "has_summary": bool(self.summary),
        }


@pytest.fixture
def setup(tmp_path, monkeypatch):
    coverage, client = Coverage(tmp_path), Client()
    calls = []

    def generate(inputs, directory, *, agent):
        calls.append(inputs)
        return rec._render(
            json.dumps(
                {
                    "sections": [
                        {
                            "title": "Purpose",
                            "claims": [{"text": "The encoder is frozen.", "sources": ["F001"]}],
                        }
                    ]
                }
            ),
            inputs,
        )

    monkeypatch.setattr(rec, "_generate", generate)
    return tmp_path, coverage, client, calls


def run(setup, **options):
    root, coverage, client, _ = setup
    return rec.complete_reconstruction(
        client,
        root,
        coverage,
        options.get("git_bundle"),
        agent=None,
        interactive=options.get("interactive", False),
        yes=options.get("yes", False),
    )


def test_yes_creates_reviewable_draft_without_publishing_or_summary_request(setup):
    lines = run(setup, interactive=True, yes=True)
    root, coverage, client, calls = setup
    assert not client.writes and len(calls) == 1
    assert any("Draft saved:" in line for line in lines)
    state = coverage.meta("reconstruction:p")
    draft = (root / state["draft_path"]).read_text()
    assert "[F001](/artifacts/artifact)" in draft
    assert "temporary" not in json.dumps(calls)
    run(setup)
    assert len(calls) == 1


def test_unreadable_receipt_or_pending_delivery_blocks_draft_and_recovers(setup):
    _, coverage, client, calls = setup
    coverage.pending = ["design.md"]
    run(setup)
    assert not calls
    coverage.pending = []
    client.readable = False
    run(setup)
    assert not calls
    client.readable = True
    run(setup)
    assert len(calls) == 1  # a saved error without input_id must not strand recovery


def test_local_source_mutation_refuses_old_version_claim(setup):
    root, _, _, calls = setup
    (root / "design.md").write_text("replacement")
    run(setup)
    assert not calls


def test_explicit_review_appends_without_erasing_prose_and_lost_ack_converges(setup, monkeypatch):
    _, coverage, client, calls = setup
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Publish" in prompt)
    client.lost_ack = True
    run(setup, interactive=True)
    # A PLAIN marker, not an HTML comment: the document lives in the Overview
    # page now and the copy-in's sanitiser drops comments, so a comment marker
    # could never be found again and every rerun appended another copy.
    assert client.document.startswith("Teammate's prose\n\n[probe-backfill:")
    assert coverage.meta("reconstruction:p")["publication"]["state"] == "pending"
    run(setup, interactive=True)
    assert len(client.writes) == 1 and len(calls) == 1
    assert coverage.meta("reconstruction:p")["publication"]["state"] == "published"


def test_old_backend_never_receives_ignored_cas_field(setup, monkeypatch):
    _, _, client, _ = setup
    client.capabilities = []
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Publish" in prompt)
    lines = run(setup, interactive=True)
    assert not client.writes and any("lacks safe" in line for line in lines)


def test_mixed_pod_old_route_refusal_has_no_legacy_fallback(setup, monkeypatch):
    _, coverage, client, _ = setup
    requests = []

    def old_pod(path, body):
        requests.append(path)
        assert path == "/v1/projects/p/summary-markdown"
        raise RuntimeError("404 old pod")

    monkeypatch.setattr(client, "patch", old_pod)
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Publish" in prompt)
    run(setup, interactive=True)  # /me capability came from a newer pod
    assert requests == ["/v1/projects/p/summary-markdown"]
    assert client.document == "Teammate's prose" and not client.writes
    assert coverage.meta("reconstruction:p")["publication"]["state"] == "pending"


def test_publication_conflict_prevents_new_summary_request(setup, monkeypatch):
    _, coverage, client, _ = setup
    monkeypatch.setattr(rec, "_confirm", lambda prompt: True)

    def conflict(path, body):
        client.document += "\nConcurrent teammate edit"
        raise RuntimeError("409 changed")

    monkeypatch.setattr(client, "patch", conflict)
    run(setup, interactive=True)
    assert not client.writes
    assert coverage.meta("reconstruction:p")["publication"]["state"] == "pending"
    assert coverage.meta("reconstruction:p")["summary"]["state"] == "not_requested"
    assert "Concurrent teammate edit" in client.document


def test_draft_failure_prevents_new_summary_request(setup, monkeypatch):
    _, _, client, _ = setup
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Summary refresh" in prompt)

    def fail(*args, **kwargs):
        raise ValueError("invalid generated citations")

    monkeypatch.setattr(rec, "_generate", fail)
    run(setup, interactive=True)
    assert not client.writes


def test_draft_failure_still_observes_an_existing_unpublished_request(setup, monkeypatch):
    _, coverage, client, _ = setup
    run(setup)
    saved = coverage.meta("reconstruction:p")
    saved.update(
        state="pending", summary={"state": "unknown", "requested_at": "2026-01-01T00:00:00Z"}
    )
    coverage.put_meta("reconstruction:p", saved)
    client.summary = {
        "generation": {"prompt_version": "test", "generated_at": "2099-01-01T00:00:00Z"}
    }

    def fail(*args, **kwargs):
        raise rec.DraftValidationError("repair_exhausted", "bounded repair already attempted")

    monkeypatch.setattr(rec, "_generate", fail)
    monkeypatch.setattr(
        rec, "_confirm", lambda _: pytest.fail("unpublished generation cannot prompt")
    )
    lines = run(setup, interactive=True)
    assert coverage.meta("reconstruction:p")["summary"]["state"] == "complete"
    assert "Optional AI Summary request: generated; review separately." in lines
    assert not client.writes


def test_declined_publication_never_offers_optional_generation(setup, monkeypatch):
    _, coverage, client, _ = setup
    prompts = []
    monkeypatch.setattr(rec, "_confirm", lambda prompt: prompts.append(prompt) or False)
    lines = run(setup, interactive=True)
    assert len(prompts) == 1 and "Publish" in prompts[0]
    assert not client.writes
    state = coverage.meta("reconstruction:p")
    assert state["state"] == "drafted" and state["summary"]["state"] == "not_requested"
    assert any("publish the reviewed write-up" in line for line in lines)


def test_exhausted_actual_draft_repair_never_requests_summary(setup, monkeypatch):
    _, coverage, client, _ = setup
    launches = []

    def invalid_draft(directory, prompt, **kwargs):
        launches.append(kwargs["label"])
        (directory / "response.json").write_text(
            json.dumps(
                {
                    "sections": [
                        {
                            "title": "Purpose",
                            "claims": [
                                {"text": "Frozen encoder.", "sources": ["F001"]} for _ in range(28)
                            ],
                        }
                    ]
                }
            )
        )
        return True, ""

    monkeypatch.setattr(rec, "_generate", generate_draft)
    monkeypatch.setattr(rec.bf, "launch_agent", invalid_draft)
    monkeypatch.setattr(
        rec, "_confirm", lambda _: pytest.fail("unreviewable draft cannot request generation")
    )
    run(setup, interactive=True)
    run(setup, interactive=True)
    assert launches == ["drafting file reconstruction", "repairing file reconstruction"]
    assert not client.writes
    assert coverage.meta("reconstruction:p")["error_code"] == "repair_exhausted"


def test_controlled_draft_diagnostic_is_saved_then_cleared_after_recovery(setup, monkeypatch):
    _, coverage, client, _ = setup
    generate = rec._generate

    def fail(*args, **kwargs):
        raise rec.DraftValidationError("claim_count", "draft contains 28 claims; maximum is 24")

    monkeypatch.setattr(rec, "_generate", fail)
    lines = run(setup)
    state = coverage.meta("reconstruction:p")
    assert state["error_code"] == "claim_count"
    assert state["error_detail"] == "draft contains 28 claims; maximum is 24"
    assert any(state["error_detail"] in line for line in lines)
    assert not client.writes
    monkeypatch.setattr(rec, "_generate", generate)
    run(setup)
    state = coverage.meta("reconstruction:p")
    assert state["state"] == "drafted"
    assert not any(field in state for field in ("error", "error_code", "error_detail"))


def test_uncontrolled_exception_cannot_expose_details_or_leave_stale_diagnostic(setup, monkeypatch):
    _, coverage, _, _ = setup
    run(setup)
    state = coverage.meta("reconstruction:p")
    state.update(state="pending", error_code="old", error_detail="old diagnostic")
    coverage.put_meta("reconstruction:p", state)

    def fail(*args, **kwargs):
        raise ValueError("SECRET source body or signed transport URL")

    monkeypatch.setattr(rec, "_generate", fail)
    lines = run(setup)
    state = coverage.meta("reconstruction:p")
    assert state["error"] == "ValueError"
    assert "error_detail" not in state and "error_code" not in state
    assert "SECRET" not in json.dumps([lines, state])
    assert any("ValueError" in line for line in lines)


def test_summary_lost_ack_is_reconciled_without_second_paid_request(setup, monkeypatch):
    _, coverage, client, _ = setup
    run(setup)
    saved = coverage.meta("reconstruction:p")
    saved["publication"]["state"] = "published"
    coverage.put_meta("reconstruction:p", saved)
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Summary refresh" in prompt)

    def lost_ack(path, body, **kwargs):
        client.writes.append((path, body))
        raise TimeoutError()

    monkeypatch.setattr(client, "post", lost_ack)
    run(setup, interactive=True)
    assert coverage.meta("reconstruction:p")["summary"]["state"] == "unknown"
    run(setup, interactive=True)
    assert len(client.writes) == 1
    client.summary = {
        "generation": {"prompt_version": "v1", "generated_at": "2099-01-01T00:00:00Z"}
    }
    run(setup)
    assert coverage.meta("reconstruction:p")["summary"]["state"] == "complete"


def test_completed_model_response_survives_checkpoint_crash(tmp_path, monkeypatch):
    inputs = {"sources": {"F001": {"url": "/artifacts/a"}}, "inventory_count": 1, "gaps": []}
    response = {
        "sections": [
            {"title": "Purpose", "claims": [{"text": "Frozen encoder.", "sources": ["F001"]}]}
        ]
    }
    (tmp_path / "response.json").write_text(json.dumps(response))

    def forbidden(*args, **kwargs):
        raise AssertionError("must reuse completed response")

    monkeypatch.setattr(rec.bf, "launch_agent", forbidden)
    assert "Frozen encoder." in rec._generate(inputs, tmp_path, agent=None)


def test_summary_is_explicit_separate_and_verified_on_resume(setup, monkeypatch):
    _, coverage, client, _ = setup
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Publish" in prompt)
    first = run(setup, interactive=True)
    assert len(client.writes) == 1 and client.writes[0][0].endswith("/summary-markdown")
    assert any("file import and publication are unaffected" in line for line in first)
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Summary refresh" in prompt)
    run(setup, interactive=True)
    assert len(client.writes) == 2 and client.writes[1][0].endswith("/summary/regenerate")
    state = coverage.meta("reconstruction:p")
    client.summary = {
        "generation": {
            "prompt_version": "current-server-prompt",
            "generated_at": "2099-01-01T00:00:00+00:00",
        }
    }
    lines = run(setup)
    assert len(client.writes) == 2
    assert coverage.meta("reconstruction:p")["summary"]["state"] == "complete"
    assert state["publication"]["state"] == "published"
    assert "Optional AI Summary request: generated; review separately." in lines


def test_overview_reconciliation_keeps_published_input_and_draft_without_generation(
    setup, monkeypatch
):
    _, coverage, client, _ = setup
    run(setup)
    state = coverage.meta("reconstruction:p")
    original = (state["input_id"], state["draft_hash"], state["draft_path"])
    state["publication"]["state"] = "published"
    state["summary"] = {"state": "pending", "requested_at": "2026-09-08T10:00:00Z"}
    coverage.put_meta("reconstruction:p", state)

    def no_generation(*args, **kwargs):
        raise AssertionError("existing draft must remain cached")

    def overview(path):
        assert path == "/v1/projects/p/overview/status"
        return {
            "anchor_type": "project",
            "anchor_id": "p",
            "content": "fresh",
            "job": "idle",
            "source": "lane",
            "generated_at": "2026-09-08T10:00:02Z",
            "prompt_version": "4",
        }

    monkeypatch.setattr(rec, "_generate", no_generation)
    monkeypatch.setattr(client, "get", overview)
    run(setup)
    updated = coverage.meta("reconstruction:p")
    assert (updated["input_id"], updated["draft_hash"], updated["draft_path"]) == original
    assert updated["publication"] == state["publication"]
    assert updated["summary"]["state"] == "complete" and updated["summary"]["lane"] == "overview"
    assert not client.writes


def test_attachment_provenance_does_not_regenerate_or_publish_identical_evidence(
    setup, monkeypatch
):
    from probe.cli.backfill_github import GitEvidence, GitEvidenceBundle

    root, coverage, client, calls = setup
    entry = GitEvidence(
        "org/repo",
        "main",
        local_folder=str(root),
        state="ok",
        access="installation",
        installation_id=17,
        bounds_verified=True,
        items=[{"sha": "a" * 40, "subject": "Frozen encoder", "run_count": 0}],
        details=[{"sha": "a" * 40, "body": "Initial design", "runs": []}],
    )
    bundle = GitEvidenceBundle([entry])
    monkeypatch.setattr(rec, "_confirm", lambda prompt: "Publish" in prompt)
    run(setup, git_bundle=bundle, interactive=True)
    input_id = coverage.meta("reconstruction:p")["input_id"]
    assert len(calls) == len(client.writes) == 1
    entry.source_id, entry.project_id = "attached-source", "p"
    entry.access, entry.installation_id = "unknown", None
    entry.fetched_at, entry.local_head = "later", "new-checkout-head"
    entry.items[0]["run_count"] = 3
    entry.details[0]["runs"] = [{"run_id": "local-project-decoration"}]
    run(setup, git_bundle=bundle, interactive=True)
    assert coverage.meta("reconstruction:p")["input_id"] == input_id
    assert len(calls) == len(client.writes) == 1
    assert client.document.count("[probe-backfill:") == 1
    assert "local-project-decoration" not in json.dumps(calls)
    entry.start_sha = "b" * 40
    run(setup, git_bundle=bundle)
    assert len(calls) == 2 and coverage.meta("reconstruction:p")["input_id"] != input_id
    assert len(client.writes) == 1  # changed evidence still requires a new explicit review


@pytest.mark.parametrize("refs", [["invented"], [], ["F001", "unknown"]])
def test_fabricated_or_uncited_sources_cannot_be_published(refs):
    raw = json.dumps(
        {
            "sections": [
                {"title": "Purpose", "claims": [{"text": "Invented claim", "sources": refs}]}
            ]
        }
    )
    with pytest.raises(ValueError):
        rec._render(raw, {"sources": {"F001": {"url": "/artifacts/a"}}})


@pytest.mark.parametrize("agent", list(rec.bf.DIGEST_MODEL))
def test_reconstruction_launch_records_its_selected_model_and_reuses_valid_output(
    tmp_path, monkeypatch, agent
):
    root, coverage, client = tmp_path, Coverage(tmp_path), Client()
    calls = []

    def launch(directory, prompt, **options):
        inputs = json.loads((directory / "evidence.json").read_text())
        calls.append((inputs, options))
        (directory / "response.json").write_text(json.dumps({"sections": []}))
        return True, ""

    monkeypatch.setattr(rec.bf, "launch_agent", launch)
    for _ in range(2):
        rec.complete_reconstruction(
            client, root, coverage, None, agent=agent, interactive=False, yes=False
        )
    assert len(calls) == 1 and not client.writes
    expected = "sonnet" if agent is rec.bf.Agent.CLAUDE else rec.bf.DIGEST_MODEL[agent]
    assert calls[0][1]["model"] == expected
    assert calls[0][0]["model"] == (expected or "configured_default")
    assert coverage.meta("reconstruction:p")["model"] == (expected or "configured_default")
    if agent is rec.bf.Agent.CLAUDE:
        previous = coverage.meta("reconstruction:p")["input_id"]
        monkeypatch.setitem(rec.MODEL, agent, "opus")
        rec.complete_reconstruction(
            client, root, coverage, None, agent=agent, interactive=False, yes=False
        )
        assert len(calls) == 2 and calls[1][1]["model"] == "opus"
        assert coverage.meta("reconstruction:p")["input_id"] != previous
        assert coverage.meta("reconstruction:p:" + previous)["model"] == "sonnet"
