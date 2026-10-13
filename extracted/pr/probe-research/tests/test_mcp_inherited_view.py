"""`view="inherited"`: what a fork reads live from its source (CONTRACT.md, Forks).

Through the SDK and the fake backend, which mirrors `app/experiments/fork_reads.py`:
the `forked_from` chain, the source's runs as they were at the fork, or those
runs' files, paged by id on the route's own `after`.
"""

from __future__ import annotations

import json

import pytest

import probe.mcp.service as service_module
from probe.mcp.service import ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors
from tests.test_mcp_delivery import _bounded, _wire


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


def _forked(client, app, *, files: int = 3):
    """Experiment A with one run and `files` files on it; experiment B forked
    from A (the server-only `forked_from` link, written as the fork route does)."""
    project = client.create_project("folding", kind="general")
    client.create_experiment(
        "warmup-a", "warmup-a", question="does warmup 500 help?", project_id=project["id"]
    )
    run = client.run(project="folding", experiment="warmup-a", name="eval-1")
    rid = run.id
    source = app.runs[rid]["experiment_id"]
    app.artifacts[rid] = [
        {
            "id": f"00000000-0000-0000-0000-00000000000{i}",
            "run_id": rid,
            "name": f"ckpt-{i}.pt",
            "kind": "checkpoint",
            "status": "complete",
            "created_at": "2026-10-12T00:00:00Z",
        }
        for i in range(1, files + 1)
    ]
    fork = client.create_experiment(
        "warmup-b", "warmup-b", question="does lr 3e-4 help?", project_id=project["id"]
    )
    app.edges.append(
        {
            "id": "edge-fork",
            "source_type": "experiment",
            "source_id": fork["id"],
            "relation": "forked_from",
            "target_type": "experiment",
            "target_id": source,
            "created_at": "2999-01-01T00:00:00Z",
        }
    )
    return source, fork["id"], rid


def test_a_fork_lists_its_sources_run_files_by_default(client, app):
    source, fork, rid = _forked(client, app)
    data = _service(client).get_entity(f"experiment:{fork}", view="inherited")["data"]
    assert data["kind"] == "files"
    assert [s["id"] for s in data["sources"]] == [source]
    assert data["sources"][0]["slug"] == "warmup-a"
    assert data["sources"][0]["forked_at"]
    assert data["total"] == 3
    assert sorted(f["name"] for f in data["files"]) == ["ckpt-1.pt", "ckpt-2.pt", "ckpt-3.pt"]
    assert {f["run_id"] for f in data["files"]} == {rid}
    # A short files list is not the whole story past the retention window.
    assert "retention window" in data["note"]


def test_runs_true_lists_the_source_runs(client, app):
    source, fork, rid = _forked(client, app)
    data = _service(client).get_entity(
        f"experiment:{fork}", view="inherited", filters={"runs": True}
    )["data"]
    assert data["kind"] == "runs"
    assert [r["id"] for r in data["runs"]] == [rid]
    assert all(r["source_experiment_id"] == source for r in data["runs"])
    assert "note" not in data


def test_an_experiment_that_is_no_fork_says_so(client, app):
    source, _fork, _rid = _forked(client, app)
    data = _service(client).get_entity(f"experiment:{source}", view="inherited")["data"]
    assert data["sources"] == []
    assert data.get("files", []) == []
    assert data["note"].startswith("Not a fork")


@pytest.mark.parametrize("value", ["yes", 1, ["runs"]])
def test_runs_must_be_a_boolean(client, app, value):
    _source, fork, _rid = _forked(client, app)
    with pytest.raises(errors.ValidationError, match="runs must be true"):
        _service(client).get_entity(f"experiment:{fork}", view="inherited", filters={"runs": value})


def test_an_unregistered_option_is_refused_naming_runs(client, app):
    _source, fork, _rid = _forked(client, app)
    with pytest.raises(errors.ValidationError, match=r"\['runs'\]"):
        _service(client).get_entity(f"experiment:{fork}", view="inherited", filters={"kind": "x"})


def test_pages_resume_on_the_routes_own_cursor_and_lose_nothing(client, app, monkeypatch):
    """One route page per call; the next cursor names the last row sent, so a
    continuation asks the route for the rows after it."""
    monkeypatch.setattr(service_module, "_PAGE_FETCH", 2)
    _source, fork, _rid = _forked(client, app, files=5)
    service = _service(client)
    seen: list[str] = []
    cursor = None
    for _ in range(5):
        out = service.get_entity(
            f"experiment:{fork}", view="inherited", cursor=cursor, token_budget=8000
        )
        seen += [f["id"] for f in out["data"]["files"]]
        cursor = out.get("next_cursor")
        if cursor is None:
            break
    assert len(seen) == len(set(seen)) == 5


def test_the_inherited_view_survives_the_real_mcp_boundary(client, app):
    _source, fork, _rid = _forked(client, app)
    result = _wire(
        _service(client),
        "entity",
        {"refs": [f"experiment:{fork}"], "view": "inherited", "token_budget": 2000},
        transport="memory",
    )
    body = _bounded(result, 2000)
    text = json.dumps(body)
    assert "ckpt-1.pt" in text and "ckpt-3.pt" in text


def test_a_page_the_readers_own_session_work_empties_still_moves_on(client, app, monkeypatch):
    """The daemon's reader hides work its own session created. When that empties
    a whole route page, the walk resumes past the rows FETCHED; resuming from
    where the page began would ask the route for the same rows forever."""
    from probe.mcp import accounting

    monkeypatch.setattr(service_module, "_PAGE_FETCH", 2)
    _source, fork, _rid = _forked(client, app, files=5)
    first_page = {f"00000000-0000-0000-0000-00000000000{i}" for i in (1, 2)}
    monkeypatch.setattr(accounting, "session_work_to_hide", lambda: "reader-session")
    monkeypatch.setattr(
        ResearchReadService, "_session_created_ids", lambda self, sid: (set(first_page), False)
    )
    service = _service(client)
    first = service.get_entity(f"experiment:{fork}", view="inherited", token_budget=8000)
    assert first["data"].get("files", []) == []
    cursor = first["next_cursor"]
    second = service.get_entity(
        f"experiment:{fork}", view="inherited", cursor=cursor, token_budget=8000
    )
    assert [f["id"] for f in second["data"]["files"]] == [
        "00000000-0000-0000-0000-000000000003",
        "00000000-0000-0000-0000-000000000004",
    ]
    assert second["next_cursor"] != cursor
