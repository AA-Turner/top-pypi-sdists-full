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
            # The create takes no document: a PATCH on the experiment API writes
            # it right after (server X21), and its answer echoes what it wrote.
            ("PATCH", f"/v1/projects/{P}/experiments/{E}"): {**_experiment(), "document": doc},
        }
    )
    row = client.create_experiment("lr-sweep", question="q", project_id=P, document=doc)
    # The create's answer names the project: no scope lookup in between.
    assert rec.calls == [
        f"POST /v1/projects/{P}/experiments",
        f"PATCH /v1/projects/{P}/experiments/{E}",
    ]
    assert rec.body(1) == {"document": doc}
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


def test_the_mcp_reads_an_experiment_document_from_the_experiment_detail():
    from probe.mcp.source import ResearchOSSource

    client, rec = _client(
        {("GET", f"/v1/projects/{P}/experiments/{E}"): _detail(document="# Plan")}
    )
    assert ResearchOSSource(client).experiment_document(E, project_id=P) == "# Plan"
    assert rec.calls == [f"GET /v1/projects/{P}/experiments/{E}"]


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
            ("PATCH", f"/v1/projects/{P}/experiments/{E}"): (
                503,
                {"detail": "object storage is unavailable"},
            ),
        }
    )
    with pytest.raises(errors.DocumentNotWritten) as raised:
        client.create_experiment("lr-sweep", question="q", project_id=P, document="# Plan")
    message = str(raised.value)
    assert E in message and "probe experiment set lr-sweep --summary" in message
    assert raised.value.experiment["id"] == E
    assert isinstance(raised.value.__cause__, errors.ServerError)


def test_an_edit_with_a_document_is_one_patch_that_lands_whole():
    """The name, the question and the document travel in ONE PATCH (server
    X21), so the edit lands whole or not at all: there is no half-landed edit
    to explain any more."""
    client, rec = _client(
        {
            ("PATCH", f"/v1/projects/{P}/experiments/{E}"): {
                **_experiment(name="New"),
                "notes_version": 1,
                "document": "# Doc",
            },
        }
    )
    row = client.update_experiment(E, project_id=P, name="New", document="# Doc")
    assert rec.calls == [f"PATCH /v1/projects/{P}/experiments/{E}"]
    assert rec.body(0) == {"name": "New", "document": "# Doc"}
    assert row["name"] == "New" and row["document"] == "# Doc"


def test_an_edit_that_fails_is_the_plain_error():
    client, _ = _client(
        {("PATCH", f"/v1/projects/{P}/experiments/{E}"): (503, {"detail": "down"})}
    )
    with pytest.raises(errors.ServerError):
        client.update_experiment(E, project_id=P, name="New", document="# Doc")


def test_a_document_the_server_did_not_echo_is_refused():
    """The write's own answer must carry the document it wrote: a 2xx that
    dropped it is a backend that cannot hold it, said out loud."""
    client, _ = _client(
        {("PATCH", f"/v1/projects/{P}/experiments/{E}"): {**_experiment(), "document": None}}
    )
    with pytest.raises(errors.RosError, match="did not store it"):
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


# -- an experiment's children (server X21) -----------------------------------------
#
# Runs, groups, edges, lineage, manifests, reproduce, code, files and uploads,
# sub-notes and notes writes go to `/v1/projects/{P}/experiments/{E}/<child>`.
# None of them reaches the leaf door (`/v1/projects/{E}/...`), which R6 removes.

_BASE = f"/v1/projects/{P}/experiments/{E}"


def _placed(routes: dict) -> dict:
    """`routes`, plus the one `GET /v1/scopes/{E}` that places E."""
    return {("GET", f"/v1/scopes/{E}"): _scope(), **routes}


@pytest.mark.parametrize(
    ("call", "method", "suffix", "params"),
    [
        (lambda c: c.list_groups(E), "GET", "/groups", {}),
        (lambda c: c.experiment_edges(E, limit=5), "GET", "/edges", {"limit": "5"}),
        (lambda c: c.experiment_lineage(E, limit=7), "GET", "/lineage", {"limit": "7"}),
        (lambda c: c.list_experiment_versions(E), "GET", "/versions", {}),
        (lambda c: c.get_experiment_version(E, 2), "GET", "/versions/2", {}),
        (lambda c: c.experiment_reproduce(E, version=1), "GET", "/reproduce", {"version": "1"}),
        (lambda c: c.get_experiment_code(E), "GET", "/code", {}),
        (lambda c: c.list_experiment_artifacts(E), "GET", "/artifacts", {}),
        (lambda c: c.list_sub_notes("experiment", E), "GET", "/sub-notes", {}),
    ],
    ids=["groups", "edges", "lineage", "versions", "version", "reproduce", "code", "artifacts", "sub-notes"],
)
def test_every_child_read_is_the_experiment_api_s(call, method, suffix, params):
    client, rec = _client(_placed({(method, f"{_BASE}{suffix}"): []}))
    call(client)
    assert rec.calls == [f"GET /v1/scopes/{E}", f"{method} {_BASE}{suffix}"]
    assert rec.params(1) == params


def test_a_known_project_saves_the_scope_lookup():
    client, rec = _client(
        {
            ("GET", f"{_BASE}/groups"): [],
            ("GET", f"{_BASE}/edges"): [],
            ("GET", f"{_BASE}/lineage"): {"edges": [], "nodes": []},
        }
    )
    client.list_groups(E, project_id=P)
    client.experiment_edges(E, project_id=P)
    client.experiment_lineage(E, project_id=P)
    assert rec.calls == [f"GET {_BASE}/groups", f"GET {_BASE}/edges", f"GET {_BASE}/lineage"]


def test_an_experiment_is_placed_once_per_client():
    client, rec = _client(
        _placed({("GET", f"{_BASE}/groups"): [], ("GET", f"{_BASE}/versions"): []})
    )
    client.list_groups(E)
    client.list_experiment_versions(E)
    assert rec.calls == [
        f"GET /v1/scopes/{E}",
        f"GET {_BASE}/groups",
        f"GET {_BASE}/versions",
    ]


def test_a_moved_experiment_is_placed_again_after_its_404():
    """The remembered home went stale (the experiment moved to P2): the child
    route's 404 asks `/v1/scopes` once more and the call is made again."""
    scopes = iter([_scope(), _scope(project=P2)])
    client, rec = _client(
        {
            ("GET", f"/v1/scopes/{E}"): lambda _r: httpx.Response(200, json=next(scopes)),
            ("GET", f"{_BASE}/groups"): [],
            ("GET", f"{_BASE}/versions"): (404, {"detail": "experiment not found in this project"}),
            ("GET", f"/v1/projects/{P2}/experiments/{E}/versions"): [{"version": 1}],
        }
    )
    client.list_groups(E)
    assert client.list_experiment_versions(E) == [{"version": 1}]
    assert rec.calls == [
        f"GET /v1/scopes/{E}",
        f"GET {_BASE}/groups",
        f"GET {_BASE}/versions",
        f"GET /v1/scopes/{E}",
        f"GET /v1/projects/{P2}/experiments/{E}/versions",
    ]


def test_a_404_on_a_fresh_placement_is_not_retried():
    client, rec = _client(
        _placed({("GET", f"{_BASE}/groups"): (404, {"detail": "experiment not found in this project"})})
    )
    with pytest.raises(errors.NotFoundError):
        client.list_groups(E)
    assert rec.calls == [f"GET /v1/scopes/{E}", f"GET {_BASE}/groups"]


def test_child_writes_are_the_experiment_api_s():
    from probe.sdk.client import Anchor

    group = {"id": "g1", "experiment_id": E, "project_id": P, "name": "g", "kind": "sweep",
             "notes": None}
    client, rec = _client(
        _placed(
            {
                ("POST", f"{_BASE}/groups"): (201, group),
                ("POST", f"{_BASE}/versions"): (201, {"version": 1}),
                ("POST", f"{_BASE}/artifacts"): (201, {"id": "a1"}),
                ("POST", f"{_BASE}/artifacts/uploads"): (201, {"artifact_id": "a2", "have": True}),
                ("POST", f"{_BASE}/sub-notes"): (201, {"id": "s1", "title": "t"}),
                ("PATCH", f"{_BASE}/sub-notes"): {"id": "s1", "title": "t", "notes_version": 2},
                ("PATCH", _BASE): {**_experiment(), "notes_version": 4},
            }
        )
    )
    client.create_group(E, "g", kind="sweep")
    client.experiment_version(E, label="v1", strict=True)
    client.create_anchored_reference(Anchor.EXPERIMENT, E, {"name": "x", "uri": "s3://b/x"})
    client._presign_anchored(Anchor.EXPERIMENT, E, {"name": "y", "content_hash": "a" * 64})
    client._create_sub_note("experiment", E, "t", "b")
    client._replace_sub_note_by_title("experiment", E, "t", "b2", base_version=1, op_key="k1")
    client._replace_notes("experiment", E, "new notes", base_version=3, op_key="k2")
    client._replace_notes("experiment", E, "forced", base_version=None, op_key="k3")
    assert rec.calls == [
        f"GET /v1/scopes/{E}",
        f"POST {_BASE}/groups",
        f"POST {_BASE}/versions",
        f"POST {_BASE}/artifacts",
        f"POST {_BASE}/artifacts/uploads",
        f"POST {_BASE}/sub-notes",
        f"PATCH {_BASE}/sub-notes",
        f"PATCH {_BASE}",
        f"PATCH {_BASE}",
    ]
    assert rec.body(1) == {"name": "g", "kind": "sweep", "spec": {}}
    assert rec.body(6) == {"note_title": "t", "body": "b2", "op_key": "k1", "base_version": 1}
    # The experiment API's PATCH is a CLOSED body with no `op_key`.
    assert rec.body(7) == {"notes": "new notes", "base_version": 3}
    assert rec.body(8) == {"notes": "forced", "force": True}


def test_a_run_starts_under_the_experiment_s_project(app):
    """`probe.init` / `run()` start a run at `/v1/projects/{P}/experiments/{E}/runs`,
    with the project the experiment row already names: no scope lookup, and no
    leaf-door address at all."""
    client = make_client(app)
    exp = app.seed_experiment("lr-sweep")
    run = client.run(experiment="lr-sweep", project=None, name="r1", heartbeat=False)
    run.finish()
    starts = [r for r in app.experiment_api_requests if r.endswith("/runs")]
    assert starts == [f"POST /v1/projects/{exp['project_id']}/experiments/{exp['id']}/runs"]
    leaf = f"/v1/projects/{exp['id']}/"
    assert not [r for r in app.requests if r.url.path.startswith(leaf)]
    assert not any(r.url.path == f"/v1/scopes/{exp['id']}" for r in app.requests)


def test_the_detail_carries_the_document_and_the_notes_headroom():
    client, rec = _client(
        _placed(
            {
                ("GET", _BASE): _detail(
                    document="# Plan", notes_limit_chars=100000, notes_remaining_chars=99999
                )
            }
        )
    )
    assert client.get_experiment_document(E) == "# Plan"
    leaf = client.get_experiment_leaf(E, project_id=P)
    assert (leaf["notes_limit_chars"], leaf["notes_remaining_chars"]) == (100000, 99999)
    # Never the leaf door (`GET /v1/projects/{E}`), which 0.209.0 read these from.
    assert rec.calls == [f"GET /v1/scopes/{E}", f"GET {_BASE}", f"GET {_BASE}"]


# -- the service-token Reader (server X21) ------------------------------------------


def _reader(routes):
    from probe.sdk.reader import Reader

    client, rec = _client(routes)
    return Reader(client.transport), rec


def test_the_reader_reads_experiments_through_the_experiment_api():
    page = {"items": [_experiment()], "total": 1, "limit": 500, "offset": 0, "next_offset": None}
    reader, rec = _reader(
        {
            ("GET", f"/v1/projects/{P}/experiments"): page,
            ("GET", "/v1/scopes"): _scope(),
            ("GET", f"/v1/scopes/{E}"): _scope(),
            ("GET", _BASE): _detail(),
            ("GET", f"{_BASE}/groups"): [{"id": "g1", "experiment_id": E, "project_id": P}],
        }
    )
    rows = reader.experiments(project_id=P)
    assert [(r["id"], r["project_id"], r["parent_project_id"]) for r in rows] == [(E, P, P)]
    assert [r["id"] for r in reader.experiments(slug="lr-sweep")] == [E]
    assert reader.experiment(E)["question"] == "Is lr 3e-4 best?"
    assert reader.groups(E) == [{"id": "g1", "experiment_id": E, "project_id": P}]
    assert rec.calls == [
        f"GET /v1/projects/{P}/experiments",
        "GET /v1/scopes",
        f"GET {_BASE}",
        f"GET /v1/scopes/{E}",
        f"GET {_BASE}",
        f"GET /v1/scopes/{E}",
        f"GET {_BASE}/groups",
    ]
    assert not [r for r in rec.requests if r.url.path.startswith(f"/v1/projects/{E}")]
    with pytest.raises(ValueError, match="no tags"):
        reader.experiments(tags=["a"])


def test_the_reader_walks_every_project_without_one():
    page = {"items": [_experiment()], "total": 1, "limit": 500, "offset": 0, "next_offset": None}
    reader, rec = _reader(
        {
            ("GET", "/v1/projects"): [{"id": P}],
            ("GET", f"/v1/projects/{P}/experiments"): page,
        }
    )
    assert [r["id"] for r in reader.experiments()] == [E]
    assert rec.calls == ["GET /v1/projects", f"GET /v1/projects/{P}/experiments"]


# -- the CLI's run move, and offline replay -------------------------------------------


def test_offline_replay_starts_its_run_under_the_experiment_s_project(app):
    from probe.sdk import offline

    client = make_client(app)
    exp = app.seed_experiment("offline-exp")
    path = offline._home_path(client, {"experiment": "offline-exp", "question": None}, "k1")
    assert path == f"/v1/projects/{exp['project_id']}/experiments/{exp['id']}/runs"


def test_the_daemon_retries_experiment_writes_again():
    """The server's Idempotency-Key allowlist names the experiment API's
    writes since X21, so these commands are retried with their key again."""
    from probe.daemon.tools import IDEMPOTENT_COMMANDS

    assert {"experiment create", "experiment set", "experiment move"} <= IDEMPOTENT_COMMANDS


def test_the_mcp_reads_a_saved_experiment_note_version_on_the_experiment_api():
    """A resumed MCP read of an experiment's notes pins the version it started
    on and reads it back from the experiment API's note history (server X21),
    under the project the experiment row names -- not the leaf door."""
    import hashlib

    from probe.mcp.delivery_context import delivery_context
    from probe.mcp.source import ResearchOSSource

    body = "the notes as they were"
    client, rec = _client(
        {("GET", f"{_BASE}/notes/versions/2"): {"version": 2, "body": body}}
    )
    snapshot = {
        "source": f"notes:experiment:{E}",
        "end": len(body),
        "sha256": hashlib.sha256(body.encode()).hexdigest(),
        "version": 2,
    }
    entity = {"id": E, "project_id": P, "notes": body + " and later", "notes_version": 3}
    with delivery_context(snapshot):
        text, version = ResearchOSSource(client).notes_document("experiment", entity)
    assert rec.calls == [f"GET {_BASE}/notes/versions/2"]
    assert text.startswith(body) and version == 2


# -- a supplied project is checked too; an old server says so (review of #2286) -----


def test_a_stale_supplied_project_is_placed_again_on_its_404():
    """`Run.child` and `run()` hand over the project a row named. If the
    experiment moved since, its 404 asks `/v1/scopes` once and goes there."""
    client, rec = _client(
        {
            ("GET", f"/v1/projects/{P2}/experiments/{E}/groups"): (
                404,
                {"detail": "experiment not found in this project"},
            ),
            ("GET", f"/v1/scopes/{E}"): _scope(),
            ("GET", f"{_BASE}/groups"): [{"id": "g1"}],
        }
    )
    assert client.list_groups(E, project_id=P2) == [{"id": "g1"}]
    assert rec.calls == [
        f"GET /v1/projects/{P2}/experiments/{E}/groups",
        f"GET /v1/scopes/{E}",
        f"GET {_BASE}/groups",
    ]


def test_a_supplied_project_in_the_trash_is_placed_again():
    client, rec = _client(
        {
            ("GET", f"/v1/projects/{P2}/experiments/{E}/code"): (
                410,
                {"detail": "in_trash", "message": "this project is in the trash"},
            ),
            ("GET", f"/v1/scopes/{E}"): _scope(),
            ("GET", f"{_BASE}/code"): {"sources": []},
        }
    )
    assert client.get_experiment_code(E, project_id=P2) == {"sources": []}
    assert rec.calls[-2:] == [f"GET /v1/scopes/{E}", f"GET {_BASE}/code"]


def test_a_404_where_the_experiment_really_is_is_not_sent_twice():
    """A real 404 (an unknown version) at the right project: one scope check,
    which names the same project, and the original error -- no second send."""
    client, rec = _client(
        {
            ("GET", f"{_BASE}/versions/9"): (404, {"detail": "experiment version not found"}),
            ("GET", f"/v1/scopes/{E}"): _scope(),
        }
    )
    with pytest.raises(errors.NotFoundError, match="version not found"):
        client.get_experiment_version(E, 9, project_id=P)
    assert rec.calls == [f"GET {_BASE}/versions/9", f"GET /v1/scopes/{E}"]


def test_a_run_child_with_a_stale_project_lands_where_the_experiment_is(app):
    client = make_client(app)
    exp = app.seed_experiment("child-exp")
    other = client.create_project("elsewhere", kind="general")["id"]
    run = client.create_run(exp["id"], "r1", project_id=other, heartbeat=False)
    assert run.experiment_id == exp["id"]
    starts = [r for r in app.experiment_api_requests if r.endswith("/runs")]
    assert starts == [
        f"POST /v1/projects/{other}/experiments/{exp['id']}/runs",
        f"POST /v1/projects/{exp['project_id']}/experiments/{exp['id']}/runs",
    ]
    run.finish()


def test_a_route_absent_child_route_says_the_server_predates_x21():
    client, rec = _client(_placed({("GET", f"{_BASE}/groups"): (404, {"detail": "Not Found"})}))
    with pytest.raises(errors.CapabilityUnavailable, match=r"predates .*#2282"):
        client.list_groups(E)
    # Not taken for a move: no second placement.
    assert rec.calls == [f"GET /v1/scopes/{E}", f"GET {_BASE}/groups"]


# -- queued writes name the experiment alone (review of #2286) ------------------------


def _async_client(routes):
    recorder = Recorder(routes)
    client = make_client(recorder, async_writes=True)
    assert client.async_writes
    return client, recorder


def test_a_queued_experiment_write_needs_no_network_and_is_placed_at_drain():
    """Under async writes a manifest mint, a notes write and a sub-note write
    are QUEUED: by the experiment alone (`/v1/projects/~/experiments/{E}/...`),
    with no request -- not even the scope lookup -- and a drain places them."""
    from probe.sdk.journal import drain

    client, rec = _async_client({})
    client.experiment_version(E, label="v1")
    client._write_notes("experiment", E, {"notes": "n", "base_version": 1})
    client._write_sub_note_by_title("experiment", E, {"note_title": "t", "body": "b"})
    assert rec.requests == []
    paths = sorted(op["path"] for _, op in client.journal.pending())
    assert paths == sorted(
        [
            f"/v1/projects/~/experiments/{E}/versions",
            f"/v1/projects/~/experiments/{E}",
            f"/v1/projects/~/experiments/{E}/sub-notes",
        ]
    )
    drainer, sent = _client(
        _placed(
            {
                ("POST", f"{_BASE}/versions"): (201, {"version": 1}),
                ("PATCH", _BASE): {**_experiment(), "notes_version": 2},
                ("PATCH", f"{_BASE}/sub-notes"): {"id": "s1", "title": "t", "notes_version": 1},
            }
        )
    )
    assert drain(client.journal, client_factory=lambda _ctx: drainer).clean
    assert sent.calls.count(f"GET /v1/scopes/{E}") == 1
    assert sorted(c for c in sent.calls if not c.startswith("GET /v1/scopes")) == sorted(
        [f"POST {_BASE}/versions", f"PATCH {_BASE}", f"PATCH {_BASE}/sub-notes"]
    )


def test_a_write_queued_with_its_project_is_journaled_by_the_experiment():
    """A sync write that fell back to the queue (fail-open) was sent with its
    project; the journal still files it by the experiment alone."""
    from probe.sdk.journal import unplaced_experiment_path

    assert unplaced_experiment_path(f"{_BASE}/versions") == f"/v1/projects/~/experiments/{E}/versions"
    assert unplaced_experiment_path(_BASE) == f"/v1/projects/~/experiments/{E}"
    # Not an experiment child route: unchanged.
    for path in (f"/v1/projects/{P}/experiments", f"/v1/projects/{P}/artifacts", f"/v1/runs/{R}"):
        assert unplaced_experiment_path(path) == path


def test_an_experiment_reference_is_queued_with_no_request(tmp_path):
    client, rec = _async_client({})
    client.enqueue_artifact_reference(
        correlation="ref:1", anchor="experiment", anchor_id=E, name="x.pt", uri="s3://b/x.pt"
    )
    assert rec.requests == []


# -- the experiment's project is remembered from any placement (review of #2286) --


def test_a_placement_by_the_detail_read_serves_the_child_routes():
    client, rec = _client(
        {
            ("GET", f"/v1/scopes/{E}"): _scope(),
            ("GET", _BASE): _detail(),
            ("GET", f"{_BASE}/groups"): [],
        }
    )
    client.get_experiment(E)
    client.list_groups(E)
    assert rec.calls == [f"GET /v1/scopes/{E}", f"GET {_BASE}", f"GET {_BASE}/groups"]


def test_list_anchored_takes_the_experiment_s_project():
    from probe.sdk.client import Anchor

    client, rec = _client({("GET", f"{_BASE}/artifacts"): []})
    client.list_anchored(Anchor.EXPERIMENT, E, project_id=P, limit=5)
    assert rec.calls == [f"GET {_BASE}/artifacts"] and rec.params(0) == {"limit": "5"}


def test_the_reader_skips_a_project_gone_mid_walk_but_not_a_named_one():
    page = {"items": [_experiment()], "total": 1, "limit": 500, "offset": 0, "next_offset": None}
    reader, _ = _reader(
        {
            ("GET", "/v1/projects"): [{"id": P2}, {"id": P}],
            ("GET", f"/v1/projects/{P2}/experiments"): (404, {"detail": "project not found"}),
            ("GET", f"/v1/projects/{P}/experiments"): page,
        }
    )
    assert [r["id"] for r in reader.experiments()] == [E]
    with pytest.raises(errors.NotFoundError):
        reader.experiments(project_id=P2)


# -- the last children (server X21b): W&B sources, and moving a run in -----------------
#
# An experiment's W&B sources are `/v1/projects/{P}/experiments/{E}/wandb-sources[...]`
# and a run moves into it by `experiment_id`; neither reaches the leaf door.


def test_an_experiment_s_wandb_sources_are_the_experiment_api_s():
    source = {"id": "s1", "project_id": P, "experiment_id": E, "state": "active"}
    client, rec = _client(
        _placed(
            {
                ("GET", f"{_BASE}/wandb-sources"): [source],
                ("POST", f"{_BASE}/wandb-sources"): (201, source),
                ("PATCH", f"{_BASE}/wandb-sources/s1"): source,
                ("DELETE", f"{_BASE}/wandb-sources/s1"): (204, None),
            }
        )
    )
    assert client.list_experiment_wandb_sources(E) == [source]
    assert client.attach_experiment_wandb_source(E, connection_id="c1", external_id="lab/x") == source
    client.patch_experiment_wandb_source(E, "s1", sync_enabled=True, expected_revision=0)
    client.detach_experiment_wandb_source(E, "s1")
    assert rec.calls == [
        f"GET /v1/scopes/{E}",
        f"GET {_BASE}/wandb-sources",
        f"POST {_BASE}/wandb-sources",
        f"PATCH {_BASE}/wandb-sources/s1",
        f"DELETE {_BASE}/wandb-sources/s1",
    ]
    assert rec.body(2) == {"connection_id": "c1", "external_id": "lab/x"}
    assert rec.body(3) == {"sync_enabled": True, "expected_revision": 0}


def test_an_experiment_wandb_attach_with_its_project_is_one_request():
    """The CLI's reviewed mapping names the project: no scope lookup."""
    source = {"id": "s1", "project_id": P, "experiment_id": E}
    client, rec = _client({("POST", f"{_BASE}/wandb-sources"): (201, source)})
    client.attach_experiment_wandb_source(E, connection_id="c1", external_id="lab/x", project_id=P)
    assert rec.calls == [f"POST {_BASE}/wandb-sources"]


def test_a_run_moves_into_an_experiment_as_an_experiment():
    moved = {"id": R, "project_id": P, "experiment_id": E, "group_id": None}
    client, rec = _client({("PATCH", f"/v1/runs/{R}"): moved})
    assert client.move_run(R, experiment_id=E) == moved
    assert rec.calls == [f"PATCH /v1/runs/{R}"]
    assert rec.body(0) == {"experiment_id": E}
