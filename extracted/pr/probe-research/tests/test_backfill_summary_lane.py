"""Real SDK status/error handling, synthetic HTTP responses, and persisted recovery."""

import copy

import httpx
import pytest

from probe.cli import backfill_reconstruction as rec
from probe.cli.backfill_coverage import Coverage, Scope
from probe.sdk.config import Settings
from probe.sdk.errors import AuthError, NotFoundError, ServerError, TransportError
from probe.sdk.transport import Transport

PROJECT = "00000000-0000-4000-8000-000000000001"
REQUESTED = "2026-09-08T10:00:00+00:00"
GENERATED = "2026-09-08T10:00:02Z"
PAGE = {
    "anchor_type": "project",
    "anchor_id": PROJECT,
    "content": "fresh",
    "job": "idle",
    "source": "lane",
    "generated_at": GENERATED,
    "prompt_version": "4",
}


@pytest.fixture
def harness(tmp_path):
    scope = Scope("https://api.invalid", "synthetic", "workspace", PROJECT)
    with Coverage(tmp_path, scope, "source").writer() as coverage:
        state = {
            "project_id": PROJECT,
            "input_id": "unchanged-draft-input",
            "summary": {"state": "pending", "requested_at": REQUESTED},
        }
        coverage.put_meta("reconstruction", state)
        requests = []
        behavior = {"page": copy.deepcopy(PAGE), "code": 200}

        def respond(request):
            requests.append((request.method, request.url.path))
            assert (
                "x-probe-agent-session" not in request.headers
                and "x-probe-agent" not in request.headers
            )
            if request.url.path.endswith("/overview/status"):
                if behavior.get("exception"):
                    raise behavior["exception"]
                return httpx.Response(behavior["code"], json=behavior["page"])
            if request.url.path.endswith("/summary/status"):
                return httpx.Response(200, json={"state": "fresh", "has_summary": True})
            if request.url.path == f"/v1/projects/{PROJECT}":
                return httpx.Response(
                    200,
                    json={
                        "metadata": {
                            "summary": {
                                "generation": {
                                    "generated_at": GENERATED,
                                    "prompt_version": "legacy-1",
                                }
                            }
                        }
                    },
                )
            pytest.fail("Unexpected request: " + request.method + " " + request.url.path)

        with httpx.Client(
            base_url="https://api.invalid", transport=httpx.MockTransport(respond)
        ) as http:
            transport = Transport(
                Settings(base_url="https://api.invalid", token="synthetic"),
                client=http,
                max_retries=0,
                attribution="backfill",
            )

            class Client:
                def get_project(self, project):
                    return transport.get(f"/v1/projects/{project}")

            client = Client()
            client.transport = transport
            yield client, coverage, state, behavior, requests


def run(harness, **options):
    client, coverage, _, _, _ = harness
    state = coverage.meta("reconstruction")
    return rec._summary(
        client,
        coverage,
        "reconstruction",
        state,
        interactive=options.get("interactive", False),
        yes=False,
    )


def test_overview_completion_uses_current_lane_and_persists_across_restart(harness):
    _, coverage, _, _, requests = harness
    assert run(harness) == "Optional AI Summary request: generated; review separately."
    saved = coverage.meta("reconstruction")
    assert saved["input_id"] == "unchanged-draft-input"
    assert saved["summary"] == {
        "state": "complete",
        "requested_at": REQUESTED,
        "lane": "overview",
        "prompt_version": "4",
        "generated_at": GENERATED,
    }
    # Read through a separate connection, then resume with deserialized state.
    # A retained Python dict cannot supply the completion evidence.
    import json
    import sqlite3
    from contextlib import closing

    with closing(sqlite3.connect(coverage.path)) as reopened:
        persisted = json.loads(
            reopened.execute("SELECT value FROM meta WHERE key='reconstruction'").fetchone()[0]
        )
    assert persisted == saved
    rec._summary(harness[0], coverage, "reconstruction", persisted, interactive=False, yes=False)
    assert coverage.meta("reconstruction") == saved
    assert requests == [("GET", f"/v1/projects/{PROJECT}/overview/status")] * 2


@pytest.mark.parametrize("previous", ["pending", "unknown", "failed"])
def test_unpublished_prior_request_still_reconciles_without_publication_or_paid_retry(
    harness, monkeypatch, previous
):
    _, coverage, state, behavior, requests = harness
    state["summary"]["state"] = previous
    coverage.put_meta("reconstruction", state)
    behavior["page"].update(content="stale")
    monkeypatch.setattr(
        rec, "_confirm", lambda _: pytest.fail("unpublished retry cannot be offered")
    )
    assert "publish the reviewed write-up" in run(harness, interactive=True)
    assert coverage.meta("reconstruction")["summary"]["lane"] == "overview"
    behavior["page"].update(content="fresh")
    assert (
        run(harness, interactive=True)
        == "Optional AI Summary request: generated; review separately."
    )
    assert coverage.meta("reconstruction")["summary"]["state"] == "complete"
    assert requests == [("GET", f"/v1/projects/{PROJECT}/overview/status")] * 2


def test_later_editor_page_preserves_prior_generation_receipt_without_new_request(
    harness, monkeypatch
):
    _, coverage, _, behavior, requests = harness
    run(harness)
    original = coverage.meta("reconstruction")
    behavior["page"].update(
        source="agent", generated_at="2026-09-08T11:00:00Z", prompt_version="agent"
    )
    monkeypatch.setattr(
        rec, "_confirm", lambda _: pytest.fail("completed generation cannot be retried")
    )
    assert (
        run(harness, interactive=True)
        == "Optional AI Summary request: generated; review separately."
    )
    assert coverage.meta("reconstruction") == original
    assert requests == [("GET", f"/v1/projects/{PROJECT}/overview/status")] * 2


def test_actual_sdk_404_uses_legacy_status_and_metadata(harness):
    _, coverage, _, behavior, requests = harness
    behavior.update(code=404, page={"detail": "Not Found"})
    assert run(harness) == "Optional AI Summary request: generated; review separately."
    assert coverage.meta("reconstruction")["summary"]["lane"] == "summary"
    assert coverage.meta("reconstruction")["summary"]["prompt_version"] == "legacy-1"
    assert requests == [
        ("GET", f"/v1/projects/{PROJECT}/overview/status"),
        ("GET", f"/v1/projects/{PROJECT}/summary/status"),
        ("GET", f"/v1/projects/{PROJECT}"),
    ]


@pytest.mark.parametrize("job", ["queued", "generating"])
@pytest.mark.parametrize("content", ["absent", "fresh"])
def test_active_overview_never_uses_legacy_stale_state_or_offers_retry(
    harness, monkeypatch, job, content
):
    _, coverage, _, behavior, requests = harness
    behavior["page"].update(job=job, content=content)
    if content == "absent":
        behavior["page"].update(generated_at=None, prompt_version=None, source=None)
    prompts = []
    monkeypatch.setattr(rec, "_confirm", lambda prompt: prompts.append(prompt) or True)
    assert run(harness, interactive=True) == "Optional AI Summary: pending."
    assert coverage.meta("reconstruction")["summary"]["lane"] == "overview"
    assert not prompts and requests == [("GET", f"/v1/projects/{PROJECT}/overview/status")]


@pytest.mark.parametrize("code,error", [(401, AuthError), (500, ServerError)])
def test_auth_and_server_errors_never_fall_back_or_offer_retry(harness, monkeypatch, code, error):
    _, coverage, _, behavior, requests = harness
    before = coverage.meta("reconstruction")
    behavior.update(code=code, page={"detail": "unavailable"})
    prompts = []
    monkeypatch.setattr(rec, "_confirm", lambda prompt: prompts.append(prompt) or True)
    with pytest.raises(error):
        run(harness, interactive=True)
    assert coverage.meta("reconstruction") == before and not prompts and len(requests) == 1


def test_transient_timeout_never_falls_back_or_offers_retry(harness, monkeypatch):
    _, coverage, _, behavior, requests = harness
    before = coverage.meta("reconstruction")
    behavior["exception"] = httpx.ConnectTimeout("synthetic")
    monkeypatch.setattr(rec, "_confirm", lambda _: pytest.fail("must not offer retry"))
    with pytest.raises(TransportError):
        run(harness, interactive=True)
    assert coverage.meta("reconstruction") == before and len(requests) == 1


@pytest.mark.parametrize(
    "patch",
    [
        {"anchor_id": "foreign"},
        {"anchor_type": "experiment"},
        {"content": "unknown"},
        {"job": "unknown"},
        {"source": "unknown"},
        {"generated_at": "invalid"},
        {"generated_at": "2026-09-08T10:00:02"},
        {"generated_at": None},
        {"prompt_version": None},
        {"prompt_version": []},
    ],
)
def test_malformed_or_foreign_status_cannot_complete_fall_back_or_offer_retry(
    harness, monkeypatch, patch
):
    _, coverage, _, behavior, requests = harness
    before = coverage.meta("reconstruction")
    behavior["page"].update(patch)
    monkeypatch.setattr(rec, "_confirm", lambda _: pytest.fail("must not offer retry"))
    with pytest.raises(ValueError, match="Overview"):
        run(harness, interactive=True)
    assert coverage.meta("reconstruction") == before and len(requests) == 1


@pytest.mark.parametrize(
    "patch",
    [
        {"generated_at": "2026-09-08T09:59:59Z"},
        {"source": "agent"},
        {"content": "stale"},
        {"content": "absent", "generated_at": None, "prompt_version": None, "source": None},
        {"job": "failed"},
    ],
)
def test_old_agent_written_stale_absent_or_failed_page_is_not_completion(harness, patch):
    _, coverage, _, behavior, requests = harness
    behavior["page"].update(patch)
    run(harness)
    assert coverage.meta("reconstruction")["summary"]["state"] != "complete"
    assert coverage.meta("reconstruction")["summary"]["lane"] == "overview"
    assert requests == [("GET", f"/v1/projects/{PROJECT}/overview/status")]


def test_previously_observed_overview_404_is_uncertain_not_legacy_idle(harness, monkeypatch):
    _, coverage, state, behavior, requests = harness
    state["summary"]["lane"] = "overview"
    coverage.put_meta("reconstruction", state)
    behavior.update(code=404, page={"detail": "Not Found"})
    monkeypatch.setattr(rec, "_confirm", lambda _: pytest.fail("must not offer retry"))
    with pytest.raises(NotFoundError):
        run(harness, interactive=True)
    assert coverage.meta("reconstruction") == state and len(requests) == 1


def test_arbitrary_exception_with_404_attribute_is_not_legacy_capability(harness, monkeypatch):
    class Unrelated(Exception):
        status = 404

    monkeypatch.setattr(harness[0].transport, "get", lambda _: (_ for _ in ()).throw(Unrelated()))
    with pytest.raises(Unrelated):
        run(harness)
