"""The SDK speaks the experiment API, and never the leaf door for the experiment itself.

Light experiments, R4 (task X15). From the server's R4 refusal on, an SDK older
than its experiment floor that addresses an experiment through its PROJECT
address (`/v1/projects/{E}`, `GET /v1/projects?kind=experiment|slug=`) is
answered 410 `client_too_old`. This client reads and writes the experiment
itself through `/v1/projects/{P}/experiments[/{E}]` and finds an experiment's
project through `GET /v1/scopes/{E}`.

A strict recorder answers exactly the routes each test expects; anything else
is an AssertionError naming the request, so a stray leaf-door call fails here
rather than passing against a forgiving fake.
"""

from __future__ import annotations

import json
from collections.abc import Callable

import httpx
import pytest

from probe.sdk import errors
from tests.conftest import make_client

P = "aaaaaaaa-0000-4000-8000-000000000001"
P2 = "aaaaaaaa-0000-4000-8000-000000000002"
E = "aaaaaaaa-0000-4000-8000-0000000000e1"
E2 = "aaaaaaaa-0000-4000-8000-0000000000e2"
R = "bbbbbbbb-0000-4000-8000-000000000001"


def _experiment(eid: str = E, project: str = P, slug: str = "lr-sweep", **extra) -> dict:
    return {
        "id": eid,
        "project_id": project,
        "slug": slug,
        "legacy_slug": None,
        "name": "LR sweep",
        "question": "Is lr 3e-4 best?",
        "run_count": 2,
        "created_at": "2026-10-01T00:00:01Z",
        "updated_at": "2026-10-01T00:00:02Z",
        "created_by": None,
        **extra,
    }


def _detail(**extra) -> dict:
    return {
        **_experiment(**extra),
        "notes": "n",
        "notes_version": 3,
        "notes_updated_at": None,
        "summary": {"content": "fresh", "job": "idle", "blurb": "b", "version": 2},
    }


Route = Callable[[httpx.Request], httpx.Response]


class Recorder:
    """Answers `(METHOD, path)` from a table; records every request."""

    def __init__(self, routes: dict[tuple[str, str], Route | dict | list | tuple]) -> None:
        self.routes = routes
        self.requests: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        key = (request.method, request.url.path)
        if key not in self.routes:
            raise AssertionError(f"unexpected request {request.method} {request.url}")
        answer = self.routes[key]
        if callable(answer):
            return answer(request)
        if isinstance(answer, tuple):
            status, body = answer
            return httpx.Response(status, json=body)
        return httpx.Response(200, json=answer)

    @property
    def calls(self) -> list[str]:
        return [f"{r.method} {r.url.path}" for r in self.requests]

    def body(self, index: int) -> dict:
        return json.loads(self.requests[index].content)

    def params(self, index: int) -> dict:
        return dict(self.requests[index].url.params)


def _client(routes):
    recorder = Recorder(routes)
    return make_client(recorder), recorder


def _scope(eid: str = E, project: str = P) -> dict:
    return {"id": eid, "kind": "experiment", "project_id": project, "experiment_id": eid, "run_id": None}


# -- reads ---------------------------------------------------------------------


def test_get_experiment_finds_its_project_through_scopes():
    client, rec = _client(
        {
            ("GET", f"/v1/scopes/{E}"): _scope(),
            ("GET", f"/v1/projects/{P}/experiments/{E}"): _detail(),
        }
    )
    row = client.get_experiment(E)
    assert rec.calls == [f"GET /v1/scopes/{E}", f"GET /v1/projects/{P}/experiments/{E}"]
    # The new names, and the old vocabulary beside them.
    assert row["project_id"] == row["parent_project_id"] == P
    assert row["question"] == row["description"] == "Is lr 3e-4 best?"
    assert row["kind"] == "experiment"
    assert row["notes_version"] == 3
    # The detail's `summary` is the PAGE's status, not headline metrics.
    assert "summary" not in row
    assert row["overview_status"]["content"] == "fresh"


def test_get_experiment_with_its_project_is_one_request():
    client, rec = _client({("GET", f"/v1/projects/{P}/experiments/lr-sweep"): _detail()})
    assert client.get_experiment("lr-sweep", project_id=P)["id"] == E
    assert rec.calls == [f"GET /v1/projects/{P}/experiments/lr-sweep"]


def test_a_project_id_is_not_an_experiment():
    client, _ = _client(
        {
            ("GET", f"/v1/scopes/{P}"): {
                "id": P, "kind": "project", "project_id": P, "experiment_id": None, "run_id": None,
            }
        }
    )
    with pytest.raises(errors.NotFoundError, match="is a project"):
        client.get_experiment(P)


def test_list_experiments_puts_the_project_in_the_path():
    """The old list sent `?project_id=` to `GET /v1/projects`, which declares no
    such parameter, so it was silently dropped (plan task X15)."""
    client, rec = _client(
        {
            ("GET", f"/v1/projects/{P}/experiments"): {
                "items": [_experiment()], "total": 3, "limit": 1, "offset": 0, "next_offset": 1,
            }
        }
    )
    page = client.list_experiments(project_id=P, limit=1)
    assert rec.calls == [f"GET /v1/projects/{P}/experiments"]
    assert rec.params(0) == {"limit": "1", "offset": "0"}
    assert [row["id"] for row in page.items] == [E]
    assert page.items[0]["parent_project_id"] == P
    assert page.next_cursor == "1"
    client.list_experiments(project_id=P, limit=1, cursor=page.next_cursor)
    assert rec.params(1) == {"limit": "1", "offset": "1"}


def test_list_experiments_without_a_project_walks_every_project():
    older = _experiment(E2, P2, slug="kl", created_at="2026-09-01T00:00:00Z")
    client, rec = _client(
        {
            ("GET", "/v1/projects"): [{"id": P, "slug": "p1"}, {"id": P2, "slug": "p2"}],
            ("GET", f"/v1/projects/{P}/experiments"): {
                "items": [_experiment()], "total": 1, "limit": 500, "offset": 0, "next_offset": None,
            },
            ("GET", f"/v1/projects/{P2}/experiments"): {
                "items": [older], "total": 1, "limit": 500, "offset": 0, "next_offset": None,
            },
        }
    )
    page = client.list_experiments(limit=1)
    assert [row["id"] for row in page.items] == [E]  # newest first
    assert page.next_cursor == "1"
    rest = client.list_experiments(limit=1, cursor=page.next_cursor)
    assert [row["id"] for row in rest.items] == [E2]
    assert rest.next_cursor is None
    # No tenant-wide experiment listing exists any more: the project list never
    # asks for experiments.
    assert all("kind" not in dict(r.url.params) for r in rec.requests)


def test_list_experiments_refuses_what_it_cannot_filter():
    client, rec = _client({})
    with pytest.raises(ValueError, match="read-only"):
        client.list_experiments(project_id=P, tags=["x"])
    with pytest.raises(ValueError, match="created_by_kind"):
        client.list_experiments(project_id=P, created_by_kind="user")
    assert rec.requests == []


def test_resolve_experiment_in_a_project_is_one_request():
    client, rec = _client({("GET", f"/v1/projects/{P}/experiments/lr-sweep"): _detail()})
    assert client.resolve_experiment("lr-sweep", project_id=P)["id"] == E
    assert rec.calls == [f"GET /v1/projects/{P}/experiments/lr-sweep"]


@pytest.mark.parametrize(
    "status,body",
    [(404, {"detail": "experiment not found"}), (410, {"detail": "in_trash", "message": "in the trash"})],
)
def test_resolve_experiment_reads_absent_and_trashed_as_none(status, body):
    client, _ = _client({("GET", f"/v1/projects/{P}/experiments/gone"): (status, body)})
    assert client.resolve_experiment("gone", project_id=P) is None


def test_resolve_experiment_accepts_the_slug_it_had_before_a_rename():
    row = _detail(slug="lr-sweep-2", legacy_slug="lr-sweep")
    client, _ = _client({("GET", f"/v1/projects/{P}/experiments/lr-sweep"): row})
    assert client.resolve_experiment("lr-sweep", project_id=P)["slug"] == "lr-sweep-2"


def _slug_scope(slug: str = "lr-sweep", eid: str = E, project: str = P) -> Route:
    def answer(request: httpx.Request) -> httpx.Response:
        assert dict(request.url.params) == {"slug": slug}
        return httpx.Response(200, json=_scope(eid, project))

    return answer


def test_resolve_experiment_without_a_project_is_one_lookup_then_the_row():
    client, rec = _client(
        {
            ("GET", "/v1/scopes"): _slug_scope(),
            ("GET", f"/v1/projects/{P}/experiments/{E}"): _detail(),
        }
    )
    assert client.resolve_experiment("lr-sweep")["id"] == E
    # Never a walk of the tenant's projects.
    assert rec.calls == ["GET /v1/scopes", f"GET /v1/projects/{P}/experiments/{E}"]


def test_get_experiment_by_slug_without_a_project_places_it_in_one_request():
    client, rec = _client(
        {
            ("GET", "/v1/scopes"): _slug_scope(),
            ("GET", f"/v1/projects/{P}/experiments/{E}"): _detail(),
        }
    )
    assert client.get_experiment("lr-sweep")["id"] == E
    assert rec.calls == ["GET /v1/scopes", f"GET /v1/projects/{P}/experiments/{E}"]


@pytest.mark.parametrize(
    "status,body",
    [
        (404, {"detail": "no project or experiment with this slug"}),
        (410, {"detail": "in_trash", "message": "in the trash since ..."}),
    ],
)
def test_a_slug_nothing_live_holds_resolves_to_none(status, body):
    client, rec = _client({("GET", "/v1/scopes"): (status, body)})
    assert client.resolve_experiment("lr-sweep") is None
    assert rec.calls == ["GET /v1/scopes"]


def test_a_slug_a_project_holds_is_not_an_experiment():
    project_scope = {"id": P, "kind": "project", "project_id": P, "experiment_id": None, "run_id": None}
    client, _ = _client({("GET", "/v1/scopes"): project_scope})
    assert client.resolve_experiment("lr-sweep") is None
    with pytest.raises(errors.NotFoundError):
        client.get_experiment("lr-sweep")


def _older_server_routes(extra: dict | None = None) -> dict:
    """A server older than GET /v1/scopes?slug=: FastAPI's own "Not Found"."""
    renamed = _experiment(E2, P2, slug="other", legacy_slug="lr-sweep")
    return {
        ("GET", "/v1/scopes"): (404, {"detail": "Not Found"}),
        ("GET", "/v1/projects"): [{"id": P2, "slug": "p2"}, {"id": P, "slug": "p1"}],
        ("GET", f"/v1/projects/{P2}/experiments"): {
            "items": [renamed], "total": 1, "limit": 500, "offset": 0, "next_offset": None,
        },
        ("GET", f"/v1/projects/{P}/experiments"): {
            "items": [_experiment()], "total": 1, "limit": 500, "offset": 0, "next_offset": None,
        },
        **(extra or {}),
    }


def test_an_older_server_falls_back_to_the_walk_and_a_live_slug_wins():
    client, rec = _client(
        _older_server_routes({("GET", f"/v1/projects/{P}/experiments/{E}"): _detail()})
    )
    assert client.resolve_experiment("lr-sweep")["id"] == E
    assert rec.calls[0] == "GET /v1/scopes"
    assert client.get_experiment("lr-sweep")["id"] == E


def test_an_older_server_s_walk_resolves_a_legacy_slug_last():
    routes = _older_server_routes()
    routes[("GET", f"/v1/projects/{P}/experiments")] = {
        "items": [], "total": 0, "limit": 500, "offset": 0, "next_offset": None,
    }
    client, _ = _client(routes)
    assert client.resolve_experiment("lr-sweep")["id"] == E2


def test_the_walk_skips_a_project_that_went_into_the_trash_mid_walk():
    routes = _older_server_routes()
    routes[("GET", f"/v1/projects/{P2}/experiments")] = (
        410, {"detail": "in_trash", "message": "in the trash since ..."},
    )
    client, _ = _client(routes)
    page = client.list_experiments()
    assert [row["id"] for row in page.items] == [E]


def test_a_refusal_is_not_read_as_absent():
    """Only the trash notice means "not there"; a client_too_old 410 (or any
    other) is raised, never swallowed into a create."""
    refusal = (410, {"detail": "moved", "code": "client_too_old", "min_version": "0.209.0"})
    client, _ = _client(
        {
            ("GET", f"/v1/projects/{P}/experiments/lr-sweep"): refusal,
            ("GET", "/v1/scopes"): refusal,
        }
    )
    with pytest.raises(errors.ClientTooOldError):
        client.resolve_experiment("lr-sweep", project_id=P)
    with pytest.raises(errors.ClientTooOldError):
        client.resolve_experiment("lr-sweep")


def test_scope_and_workspace_reads():
    client, rec = _client(
        {
            ("GET", f"/v1/scopes/{R}"): {
                "id": R, "kind": "run", "project_id": P, "experiment_id": E, "run_id": R,
            },
            ("GET", f"/v1/projects/{P}/workspace"): {"project_id": P, "runs": {"ids": [R]}},
        }
    )
    assert client.get_scope(R)["experiment_id"] == E
    client.get_project_workspace(P, scope=f"experiment:{E}", runs_limit=50, include_experiments=False)
    assert rec.params(1) == {
        "scope": f"experiment:{E}", "runs_limit": "50", "include_experiments": "false",
    }


def test_the_overview_reads_go_to_the_experiment_routes():
    client, rec = _client(
        {
            ("GET", f"/v1/projects/{P}/experiments/{E}/overview"): {"html": "<p>x</p>"},
            ("GET", f"/v1/projects/{P}/experiments/{E}/overview/status"): {"content": "fresh"},
        }
    )
    assert client.get_experiment_overview(E, project_id=P)["html"] == "<p>x</p>"
    assert client.get_experiment_overview(E, project_id=P, status_only=True)["content"] == "fresh"
    assert rec.calls == [
        f"GET /v1/projects/{P}/experiments/{E}/overview",
        f"GET /v1/projects/{P}/experiments/{E}/overview/status",
    ]


# -- writes --------------------------------------------------------------------


def test_create_experiment_posts_a_closed_body_under_its_project(monkeypatch):
    monkeypatch.delenv("PROBE_AGENT_SESSION_ID", raising=False)
    client, rec = _client(
        {("POST", f"/v1/projects/{P}/experiments"): (201, {**_experiment(), "notes_version": 0})}
    )
    row = client.create_experiment("lr-sweep", "LR sweep", question="Is lr 3e-4 best?", project_id=P)
    assert rec.calls == [f"POST /v1/projects/{P}/experiments"]
    body = rec.body(0)
    # Exactly the experiment API's fields: no kind, no parent, no description.
    assert set(body) <= {"slug", "name", "question", "authored_by"}
    assert (body["slug"], body["name"], body["question"]) == ("lr-sweep", "LR sweep", "Is lr 3e-4 best?")
    assert row["project_id"] == P and row["kind"] == "experiment"


def test_create_experiment_writes_its_document_and_checks_it_landed():
    doc = "# Plan\n\nSetup."
    client, rec = _client(
        {
            ("POST", f"/v1/projects/{P}/experiments"): (201, _experiment()),
            # The one write still at the project address: the experiment API has
            # no field for the Overview page's authored block yet.
            ("PATCH", f"/v1/projects/{E}"): {"id": E, "document": doc},
        }
    )
    row = client.create_experiment("lr-sweep", question="q", project_id=P, document=doc)
    assert rec.calls[-1] == f"PATCH /v1/projects/{E}"
    assert rec.body(1)["document"] == doc
    assert row["document"] == doc


@pytest.mark.parametrize(
    "kwargs,match",
    [({"tags": ["a"]}, "read-only"), ({"description": "d"}, "QUESTION")],
)
def test_create_experiment_refuses_retired_fields_before_sending(kwargs, match):
    client, rec = _client({})
    with pytest.raises(ValueError, match=match):
        client.create_experiment("lr-sweep", question="q", project_id=P, **kwargs)
    assert rec.requests == []


def test_update_experiment_edits_identity_through_the_experiment_route():
    client, rec = _client(
        {
            ("GET", f"/v1/scopes/{E}"): _scope(),
            ("PATCH", f"/v1/projects/{P}/experiments/{E}"): {**_experiment(name="New"), "notes_version": 3},
        }
    )
    row = client.update_experiment(E, name="New", question="Is 1e-4 better?", authored_by="agent")
    assert rec.calls == [f"GET /v1/scopes/{E}", f"PATCH /v1/projects/{P}/experiments/{E}"]
    assert rec.body(1) == {"name": "New", "question": "Is 1e-4 better?", "authored_by": "agent"}
    assert row["name"] == "New"


@pytest.mark.parametrize("field", ["tags", "metadata", "summary", "description"])
def test_update_experiment_refuses_fields_the_server_keeps_read_only(field):
    client, rec = _client({})
    value = "x" if field == "description" else (["x"] if field == "tags" else {"x": 1})
    with pytest.raises(ValueError):
        client.update_experiment(E, **{field: value})
    assert rec.requests == []


def test_move_experiment_patches_the_project_id():
    client, rec = _client(
        {("PATCH", f"/v1/projects/{P}/experiments/{E}"): {**_experiment(project=P2), "notes_version": 3}}
    )
    row = client.move_experiment(E, P2, from_project_id=P)
    assert rec.calls == [f"PATCH /v1/projects/{P}/experiments/{E}"]
    assert rec.body(0) == {"project_id": P2}
    assert row["project_id"] == P2


def test_delete_experiment_moves_it_to_the_trash():
    receipt = {"trashed": True, "type": "experiment", "id": E, "restorable_until": "2026-10-26T00:00:00Z"}
    client, rec = _client({("DELETE", f"/v1/projects/{P}/experiments/{E}"): receipt})
    assert client.delete_experiment(E, project_id=P)["trashed"] is True
    client.delete_experiment(E, project_id=P, dry_run=True, reason="cleanup")
    assert rec.params(1) == {"dry_run": "true", "reason": "cleanup"}


# -- create-or-get: the 409 names the holder -------------------------------------


def _conflict(kind: str, parent: str | None) -> tuple[int, dict]:
    return 409, {
        "detail": {
            "message": "slug taken",
            "existing_id": E2,
            "suggestion": "lr-sweep-2",
            "existing": {"id": E2, "kind": kind, "parent_project_id": parent, "workspace_id": None},
        }
    }


def _ensure_routes(conflict) -> dict:
    return {
        ("GET", f"/v1/projects/{P}/experiments/lr-sweep"): (404, {"detail": "experiment not found"}),
        # The near-miss guard reads the tenant's experiments first.
        ("GET", "/v1/projects"): [{"id": P, "slug": "p1"}],
        ("GET", f"/v1/projects/{P}/experiments"): {
            "items": [], "total": 0, "limit": 500, "offset": 0, "next_offset": None,
        },
        ("POST", f"/v1/projects/{P}/experiments"): conflict,
        ("GET", f"/v1/projects/{P}/experiments/{E2}"): _detail(eid=E2),
    }


def test_ensure_adopts_a_create_race_winner_in_the_same_project():
    client, _ = _client(_ensure_routes(_conflict("experiment", P)))
    assert client.ensure_experiment("lr-sweep", question="q", project_id=P)["id"] == E2


def test_ensure_refuses_the_same_slug_in_another_project():
    client, _ = _client(_ensure_routes(_conflict("experiment", P2)))
    with pytest.raises(errors.ValidationError, match="another project"):
        client.ensure_experiment("lr-sweep", question="q", project_id=P)


def test_ensure_never_adopts_a_project_holding_the_slug():
    client, _ = _client(_ensure_routes(_conflict("project", None)))
    with pytest.raises(errors.ConflictError) as raised:
        client.ensure_experiment("lr-sweep", question="q", project_id=P)
    assert raised.value.existing["kind"] == "project"


# -- the refusal, as a caller meets it ---------------------------------------------


def test_a_client_too_old_refusal_says_how_to_upgrade():
    client, _ = _client(
        {
            ("GET", f"/v1/projects/{P}/experiments/{E}"): (
                410,
                {"detail": "This experiment moved to its own record.", "code": "client_too_old",
                 "min_version": "0.209.0"},
            )
        }
    )
    with pytest.raises(errors.ClientTooOldError) as raised:
        client.get_experiment(E, project_id=P)
    assert raised.value.min_version == "0.209.0"
    assert "pip install -U probe-research" in str(raised.value)
    assert "0.209.0" in str(raised.value)


def test_a_refusal_that_names_the_command_is_left_as_the_server_wrote_it():
    detail = (
        "This experiment moved to its own record. Upgrade to probe-research 0.209.0 "
        "or later: `pip install -U probe-research`."
    )
    client, _ = _client(
        {("GET", f"/v1/projects/{P}/experiments/{E}"): (410, {"detail": detail, "code": "client_too_old",
                                                             "min_version": "0.209.0"})}
    )
    with pytest.raises(errors.ClientTooOldError) as raised:
        client.get_experiment(E, project_id=P)
    assert str(raised.value).count("pip install") == 1


def test_a_trash_410_is_not_a_refusal():
    client, _ = _client(
        {("GET", f"/v1/projects/{P}/experiments/{E}"): (410, {"detail": "in_trash", "message": "in the trash"})}
    )
    with pytest.raises(errors.RosError) as raised:
        client.get_experiment(E, project_id=P)
    assert not isinstance(raised.value, errors.ClientTooOldError)


# -- the CLI ---------------------------------------------------------------------


def test_probe_experiment_move_sends_the_target_project(app, tmp_path, monkeypatch):
    from probe import cli

    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    source = app.seed_experiment("lr-sweep")
    home = source["project_id"]
    target = make_client(app).create_project("target", kind="general")
    assert cli.main(["experiment", "move", "lr-sweep", "--to", "target"]) == 0
    assert app.experiments[source["id"]]["project_id"] == target["id"]
    assert app.experiment_api_requests[-1] == f"PATCH /v1/projects/{home}/experiments/{source['id']}"


# -- every first-party PAT caller names itself -----------------------------------


def test_the_daemon_s_api_client_sends_the_cli_pair():
    """From the server's R4 refusal on, a PAT request naming no client is
    answered as an old CLI where it reaches an experiment by its project
    address -- which the daemon's delete preview does."""
    import asyncio

    from probe import __version__
    from probe.client_headers import client_version_headers
    from probe.daemon import probe_api

    async def headers() -> dict:
        async with await probe_api._client({"PROBE_TOKEN": "t"}) as client:
            return dict(client.headers)

    sent = asyncio.run(headers())
    expected = client_version_headers("cli", __version__)
    assert expected, "the installed package reports no SemVer version"
    for key, value in expected.items():
        assert sent[key.lower()] == value


# -- the MCP -----------------------------------------------------------------------


def test_the_mcp_lists_a_project_s_experiments_through_the_experiment_api():
    from probe.mcp.source import ResearchOSSource

    client, rec = _client(
        {
            ("GET", f"/v1/projects/{P}/experiments"): {
                "items": [_experiment()], "total": 1, "limit": 100, "offset": 0, "next_offset": None,
            }
        }
    )
    rows = ResearchOSSource(client).experiments(project_id=P, limit=100)
    assert [row["id"] for row in rows] == [E]
    assert rec.calls == [f"GET /v1/projects/{P}/experiments"]


def test_the_mcp_reads_an_experiment_document_only_in_its_summary_view():
    from probe.mcp.source import ResearchOSSource

    client, rec = _client({("GET", f"/v1/projects/{E}"): {"id": E, "document": "# Plan"}})
    assert ResearchOSSource(client).experiment_document(E) == "# Plan"
    assert rec.calls == [f"GET /v1/projects/{E}"]


# -- one walk per top-level call -------------------------------------------------


def test_run_walks_the_tenant_once_for_its_near_miss_guard(app, monkeypatch):
    """`run()` asks the near-miss guard before it commits a parent project and
    again inside the create: one walk serves both."""
    client = make_client(app)
    project = client.create_project("folding", kind="general")
    app.seed_experiment("other-exp", project_id=project["id"])
    walks_before = sum(r.endswith(f"/v1/projects/{project['id']}/experiments") for r in app.experiment_api_requests)
    run = client.run(project="folding", experiment="brand-new", question="does it fold?", name="r1")
    run.finish()
    walks = sum(r.endswith(f"/v1/projects/{project['id']}/experiments") for r in app.experiment_api_requests)
    # One list read for the guard; the create is a POST to the same path.
    lists = [r for r in app.experiment_api_requests if r == f"GET /v1/projects/{project['id']}/experiments"]
    assert len(lists) == 1, app.experiment_api_requests
    assert walks - walks_before == 2  # the walk's GET and the create's POST


def test_resolve_or_raise_names_near_misses_from_the_whole_tenant(app):
    client = make_client(app)
    app.seed_experiment("lr-sweep-big")
    with pytest.raises(errors.NotFoundError, match="lr-sweep-big"):
        client.resolve_or_raise("experiment", "lr-sweep-bgi")


# -- a create whose document write fails -------------------------------------------


def test_a_create_whose_document_fails_names_the_experiment_and_the_fix():
    client, _ = _client(
        {
            ("POST", f"/v1/projects/{P}/experiments"): (201, _experiment()),
            ("PATCH", f"/v1/projects/{E}"): (503, {"detail": "object storage is unavailable"}),
        }
    )
    with pytest.raises(errors.DocumentNotWritten) as raised:
        client.create_experiment("lr-sweep", question="q", project_id=P, document="# Plan")
    message = str(raised.value)
    assert E in message and "probe experiment set lr-sweep --summary" in message
    assert raised.value.experiment["id"] == E
    assert isinstance(raised.value.__cause__, errors.ServerError)


def test_an_edit_whose_document_fails_after_the_name_landed_says_so():
    client, _ = _client(
        {
            ("PATCH", f"/v1/projects/{P}/experiments/{E}"): {**_experiment(name="New"), "notes_version": 1},
            ("PATCH", f"/v1/projects/{E}"): (503, {"detail": "down"}),
        }
    )
    with pytest.raises(errors.DocumentNotWritten, match="name changed"):
        client.update_experiment(E, project_id=P, name="New", document="# Doc")


def test_a_document_only_edit_that_fails_is_the_plain_error():
    client, _ = _client({("PATCH", f"/v1/projects/{E}"): (503, {"detail": "down"})})
    with pytest.raises(errors.ServerError):
        client.update_experiment(E, project_id=P, document="# Doc")


# -- the CLI's active project ------------------------------------------------------


def test_the_cli_looks_in_the_active_project_first(app, tmp_path, monkeypatch):
    import importlib

    from probe import cli

    cli_main = importlib.import_module("probe.cli.main")

    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    exp = app.seed_experiment("lr-sweep")
    monkeypatch.setattr(cli_main, "_ambient_project", lambda explicit, **kw: f"id:{exp['project_id']}")
    before = len(app.experiment_api_requests)
    assert cli.main(["experiment", "get", "lr-sweep"]) == 0
    assert app.experiment_api_requests[before:] == [
        f"GET /v1/projects/{exp['project_id']}/experiments/lr-sweep",
        f"GET /v1/projects/{exp['project_id']}/experiments/{exp['id']}",
    ]


# -- probe backfill's count reads every page ----------------------------------------


def test_backfill_counts_every_experiment_page():
    from probe.cli.backfill import count_landed
    from probe.sdk.transport import Page

    class Stub:
        def __init__(self):
            self.pages = 0

        def list_anchored(self, anchor, anchor_id, **kw):
            return []

        def list_experiments(self, project_id=None, limit=None, cursor=None):
            self.pages += 1
            if cursor is None:
                return Page(items=[{"id": f"e{i}"} for i in range(500)], next_cursor="500")
            return Page(items=[{"id": "e500"}], next_cursor=None)

    stub = Stub()
    import probe.cli.backfill as backfill

    original = backfill._project_id
    backfill._project_id = lambda client, project: P
    try:
        total, _ = count_landed(stub, "p1")
    finally:
        backfill._project_id = original
    assert stub.pages == 2 and total == 0
