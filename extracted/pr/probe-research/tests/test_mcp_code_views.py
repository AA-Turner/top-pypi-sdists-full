"""The phase-6 code views: `(experiment, code)` and `(run, code)`.

Both ride the existing `view=` seam — the thin-harness move — and both are
served from canned FakeApp payloads because the real assembly is SQL over
stored link rows the fake has no tables for (the backend unit suite proves
that assembly; this file proves the MCP surface: dispatch, filter contract,
payload shaping, and the envelope).
"""

from __future__ import annotations

import pytest

from probe.mcp.contract import View
from probe.mcp.service import ResearchReadService, _VIEW_OPTIONS, _VIEWS, EntityType
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


def _seeded(client, app):
    """A project/experiment/run trio, the same two commands a real user runs."""
    project = client.create_project("folding", kind="general")
    client.create_experiment(
        "dockq-path", "dockq-path", question="q", project_id=project["id"]
    )
    run = client.run(project="folding", experiment="dockq-path", name="eval-1")
    experiment_id = app.runs[run.id]["experiment_id"]
    return project["id"], experiment_id, run.id


_SHA_A = "a" * 40
_SHA_B = "b" * 40


def _experiment_code_payload(experiment_id, project_id, run_id) -> dict:
    return {
        "experiment_id": experiment_id,
        "project_id": project_id,
        "sources": [
            {
                "id": "src-1",
                "project_id": project_id,
                "repo": "acme/train",
                "ref": "main",
                "path_prefix": "",
                "status": "active",
                "status_reason": None,
                "attached_via": "dashboard",
                "head_sha": _SHA_B,
                "html_url": "https://github.com/acme/train/tree/main",
            }
        ],
        "runs": [
            {
                "run_id": run_id,
                "slug": "eval-1",
                "status": "running",
                "state": "resolved",
                "repo": "acme/train",
                "sha": _SHA_A,
                "short_sha": _SHA_A[:7],
                "source_attached": True,
            }
        ],
        "windows": [
            {
                "repo": "acme/train",
                "source_attached": True,
                "from_sha": _SHA_A,
                "to_sha": _SHA_B,
                "from_run_id": run_id,
                "to_run_id": run_id,
                "commits": [
                    {"sha": _SHA_A, "short_sha": _SHA_A[:7], "run_count": 1},
                    {"sha": _SHA_B, "short_sha": _SHA_B[:7], "run_count": 2},
                ],
                "commits_truncated": True,
            }
        ],
    }


def test_experiment_code_view_serves_sources_windows_and_run_rows(client, app):
    project_id, experiment_id, run_id = _seeded(client, app)
    app.experiment_code[experiment_id] = _experiment_code_payload(
        experiment_id, project_id, run_id
    )
    result = _service(client).get_entity(f"experiment:{experiment_id}", view="code")
    data = result["data"]
    assert "completeness" not in result
    # Sources are trimmed to the shared key set; empty/None values drop.
    assert data["sources"] == [
        {
            "id": "src-1",
            "repo": "acme/train",
            "ref": "main",
            "status": "active",
            "attached_via": "dashboard",
            "head_sha": _SHA_B,
            "html_url": "https://github.com/acme/train/tree/main",
        }
    ]
    # Windows compact commits to short shas and keep the truncation flag —
    # the full rows stay on the HTTP read.
    assert data["windows"] == [
        {
            "repo": "acme/train",
            "source_attached": True,
            "from_sha": _SHA_A,
            "to_sha": _SHA_B,
            "commits": [_SHA_A[:7], _SHA_B[:7]],
            "commits_truncated": True,
        }
    ]
    # Runs are the ROWS (budget-bounded, cursor-walkable).
    assert [r["run_id"] for r in data["runs"]] == [run_id]


def test_experiment_code_view_with_nothing_attached_answers_empty(client, app):
    """Zero sources and zero resolved runs is an ANSWER, not a degradation."""
    project_id, experiment_id, _ = _seeded(client, app)
    result = _service(client).get_entity(f"experiment:{experiment_id}", view="code")
    assert "completeness" not in result
    assert result["data"]["sources"] == []
    assert result["data"]["windows"] == []
    assert result["data"]["runs"] == []


def test_experiment_code_view_accepts_no_filters(client, app):
    _, experiment_id, _ = _seeded(client, app)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(
            f"experiment:{experiment_id}", view="code", filters={"compare_to": "x"}
        )
    assert "accepts no view options" in str(excinfo.value)


def test_run_code_view_serves_the_stored_resolution(client, app):
    _, _, run_id = _seeded(client, app)
    app.run_code[run_id] = {
        "state": "resolved",
        "repo": "acme/train",
        "sha": _SHA_A,
        "short_sha": _SHA_A[:7],
        "branch": "main",
        "dirty": False,
        "resolvable": None,
        "source_attached": True,
    }
    result = _service(client).get_entity(f"run:{run_id}", view="code")
    assert "completeness" not in result
    assert result["data"]["code"]["repo"] == "acme/train"
    assert result["data"]["code"]["state"] == "resolved"


def test_run_code_compare_filter_strips_the_ref_prefix_and_delegates(client, app):
    """`compare_to` takes `run:<ref>` or a bare ref; both reach the backend
    as the bare value (the fake is keyed on exactly what the query carries)."""
    _, _, run_id = _seeded(client, app)
    other = client.run(project="folding", experiment="dockq-path", name="eval-2")
    canned = {
        "state": "comparable",
        "base": {"run_id": run_id, "code": {"state": "resolved", "sha": _SHA_A}},
        "head": {"run_id": other.id, "code": {"state": "resolved", "sha": _SHA_B}},
        "swapped": False,
        "repo": "acme/train",
        "identical": False,
        "commits": [{"sha": _SHA_B, "short_sha": _SHA_B[:7], "run_count": 1}],
        "commits_truncated": False,
    }
    app.run_code_compare[(run_id, other.id)] = canned
    service = _service(client)
    for spelling in (f"run:{other.id}", other.id):
        result = service.get_entity(
            f"run:{run_id}", view="code", filters={"compare_to": spelling}
        )
        assert "completeness" not in result
        assert result["data"]["compare"] == canned


def test_run_code_view_rejects_unknown_filters(client, app):
    _, _, run_id = _seeded(client, app)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(f"run:{run_id}", view="code", filters={"to": "x"})
    assert "compare_to" in str(excinfo.value)


def test_cards_advertise_the_code_view(client, app):
    """Discovery rides `available_views` on the cheap read — the card itself
    stays untouched (the backend experiment read carries no code facts, so a
    hint would cost an extra call on the cheapest read)."""
    _, experiment_id, run_id = _seeded(client, app)
    service = _service(client)
    for ref in (f"experiment:{experiment_id}", f"run:{run_id}"):
        views = service.get_entity(ref)["data"]["available_views"]
        assert "code" in views


def test_project_code_view_filters_are_actually_accepted():
    """Regression for the dead-switch this phase found: `_view_project_code`
    documents `commit`/`source`/`cursor`/`author`/`path`/`include_excluded`,
    but `(project, code)` had no `_VIEW_OPTIONS` entry, so `_checked_view_options`
    refused every one of them with "accepts no filters"."""
    allowed = _VIEW_OPTIONS[(EntityType.PROJECT, View.CODE)]
    assert allowed == {
        "commit", "source", "cursor", "author", "path", "include_excluded"
    }
    checked = ResearchReadService._checked_view_options(
        ResearchReadService.__new__(ResearchReadService),
        EntityType.PROJECT,
        View.CODE,
        {"commit": "abc1234", "include_excluded": True},
    )
    assert checked == {"commit": "abc1234", "include_excluded": True}


def test_every_code_pair_served_is_in_the_shared_matrix():
    """The dead-switch guard, aimed at exactly this change: each (kind, code)
    pair the server dispatches must exist in the generated vocabulary."""
    from probe.mcp.contract import VIEW_MATRIX

    for kind in (EntityType.PROJECT, EntityType.EXPERIMENT, EntityType.RUN):
        assert (kind, View.CODE) in _VIEWS
        assert View.CODE in VIEW_MATRIX[kind]
