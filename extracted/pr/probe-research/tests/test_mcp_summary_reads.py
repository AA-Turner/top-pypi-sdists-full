"""The recorder's reads: an entity's sessions newest first, the summary's
history, `overview.markdown`, and the honest transcript note on a scoped search.

Through the service AND the wire (`_wire`): `continuation.page` rebuilds the
envelope after the service, so a payload key or cursor that the service emits
can still be stripped on delivery (#2191) -- the walk is asserted on what an
MCP client receives.
"""

from __future__ import annotations

import json
import uuid

import pytest

from probe.mcp.contract import EntityType, View
from probe.mcp.server import create_server
from probe.mcp.service import _VIEW_OPTIONS, _VIEWS, ResearchReadService
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors
from test_mcp_delivery import _bounded, _wire
from test_mcp_read_gaps import _CreatedSource, _hiding
from tests.conftest import search_response

PAGE = 50


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


def _session(i: int, *, title: str | None = None, direct: bool = True) -> dict:
    """A LinkedSessionsOut row as the server shapes it, newest first by `i`."""
    sid = f"{i:08d}-0000-0000-0000-000000000000"
    return {
        "session_id": sid,
        "agent": "claude_code",
        "name": title or f"Claude Code · Oct 1, {i % 24:02d}:00",
        "title": title,
        "owner_name": "Ada",
        "owner_email": None,
        "device_label": None,
        "device_hostname": None,
        "first_seen_at": "2026-10-01T00:00:00Z",
        "last_seen_at": f"2026-10-{1 + i % 28:02d}T{i % 24:02d}:00:00Z",
        "direct": direct,
        "src_type": None if direct else "run",
        "src_id": None if direct else str(uuid.uuid4()),
    }


def _anchor(client, kind: str) -> dict:
    project = client.create_project("summary-parent", kind="general")
    if kind == "project":
        return project
    return client.create_experiment(
        "summary-child", "Summary child", question="what?", project_id=project["id"]
    )


def _seed_sessions(app, kind: str, entity_id: str, rows: list[dict]) -> None:
    store = app.project_sessions if kind == "project" else app.experiment_sessions
    store[entity_id] = rows


def _session_requests(app) -> list:
    return [r for r in app.requests if r.url.path.endswith("/sessions")]


# -- view="sessions" on a project / experiment --------------------------------


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_sessions_are_newest_first_and_walk_the_route_past_its_page(client, app, kind):
    entity = _anchor(client, kind)
    rows = [_session(60 - i, title="Fix the scorer" if i == 0 else None) for i in range(60)]
    rows[3] = _session(57, direct=False)
    _seed_sessions(app, kind, entity["id"], rows)
    service = _service(client)
    first = service.get_entity(f"{kind}:{entity['id']}", view="sessions", token_budget=100_000)
    data = first["data"]
    assert data["view"] == "sessions" and data["entity_type"] == kind
    assert data["session_total"] == 60
    assert len(data["sessions"]) == PAGE and "completeness" not in first
    lead = data["sessions"][0]
    assert lead["uuid"] == "session:claude_code/00000060-0000-0000-0000-000000000000"
    assert lead["title"] == "Fix the scorer" and lead["name"] == "Fix the scorer"
    assert lead["owner_name"] == "Ada" and "direct" not in lead
    assert data["sessions"][3]["direct"] is False
    assert "title" not in data["sessions"][1], "an untitled row carries no null title"
    # The route was asked for the newest page, no resume key.
    [request] = _session_requests(app)
    assert request.url.params["order"] == "newest"
    assert request.url.params["limit"] == str(PAGE)
    assert "after" not in request.url.params
    # The walk: the next page resumes past the last row SENT, on its id.
    second = service.get_entity(
        f"{kind}:{entity['id']}", view="sessions", token_budget=100_000, cursor=first["next_cursor"]
    )
    assert len(second["data"]["sessions"]) == 10 and "next_cursor" not in second
    assert second["data"]["session_total"] == 60
    assert _session_requests(app)[-1].url.params["after"] == rows[PAGE - 1]["session_id"]
    seen = [r["uuid"] for r in data["sessions"] + second["data"]["sessions"]]
    assert len(seen) == len(set(seen)) == 60


def test_an_entity_no_session_touched_has_no_sessions(client, app):
    entity = _anchor(client, "project")
    out = _service(client).get_entity(f"project:{entity['id']}", view="sessions")
    assert out["data"]["sessions"] == [] and out["data"]["session_total"] == 0
    assert "completeness" not in out and "next_cursor" not in out


def test_the_sessions_walk_survives_the_wire_at_a_small_budget(client, app):
    """Every page an MCP client receives is bounded, carries rows, and the
    cursors chain to the whole list: delivery adds nothing and drops nothing."""
    entity = _anchor(client, "project")
    rows = [_session(80 - i) for i in range(80)]
    _seed_sessions(app, "project", entity["id"], rows)
    service = _service(client)
    args = {"refs": [f"project:{entity['id']}"], "view": "sessions", "token_budget": 512}
    seen, cursor = [], None
    for _ in range(200):
        page = _bounded(_wire(service, "entity", {**args, **({"cursor": cursor} if cursor else {})}))
        assert page["data"]["view"] == "sessions"
        assert page["data"]["sessions"], "a page always makes progress"
        seen += [r["uuid"] for r in page["data"]["sessions"]]
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    else:
        pytest.fail("the walk never ended")
    assert seen == [f"session:claude_code/{r['session_id']}" for r in rows]


def test_the_watched_session_is_left_out_and_the_total_says_what_it_can(client, app):
    """Under `X-Probe-Hide-Session-Work` (the daemon's reader) the session it
    reads beside is left out. On the page: the total drops by one. Not on the
    page while more pages follow: the count is a floor."""
    entity = _anchor(client, "project")
    rows = [_session(60 - i) for i in range(60)]
    _seed_sessions(app, "project", entity["id"], rows)
    service = ResearchReadService(_CreatedSource(client, {"project_ids": [], "run_ids": []}))
    on_page, off_page = rows[5]["session_id"], rows[55]["session_id"]
    with _hiding(on_page):
        out = service.get_entity(f"project:{entity['id']}", view="sessions", token_budget=100_000)
    assert out["data"]["session_total"] == 59
    assert len(out["data"]["sessions"]) == PAGE - 1
    assert all(on_page not in r["uuid"] for r in out["data"]["sessions"])
    with _hiding(off_page):
        out = service.get_entity(f"project:{entity['id']}", view="sessions", token_budget=100_000)
    assert out["data"]["session_total_at_least"] == 59 and "session_total" not in out["data"]
    assert len(out["data"]["sessions"]) == PAGE


@pytest.mark.parametrize("watched_index", [PAGE - 1, 55])
def test_the_hidden_walk_survives_the_wire(client, app, watched_index):
    """At the wire (#2191): the watched session as the LAST row the route
    fetched (its id is what the cursor would carry) and as a row on a later
    page. Every delivered page carries a total, the walk reaches every other
    session once, and the watched one never appears."""
    entity = _anchor(client, "project")
    rows = [_session(60 - i) for i in range(60)]
    _seed_sessions(app, "project", entity["id"], rows)
    service = ResearchReadService(_CreatedSource(client, {"project_ids": [], "run_ids": []}))
    watched = rows[watched_index]["session_id"]
    args = {"refs": [f"project:{entity['id']}"], "view": "sessions", "token_budget": 512}
    seen, totals, cursor = [], [], None
    with _hiding(watched):
        for _ in range(200):
            page = _bounded(_wire(service, "entity", {**args, **({"cursor": cursor} if cursor else {})}))
            data = page["data"]
            totals.append({k: v for k, v in data.items() if k.startswith("session_total")})
            seen += [r["uuid"] for r in data["sessions"]]
            cursor = page.get("next_cursor")
            if cursor is None:
                break
        else:
            pytest.fail("the walk never ended")
    assert all(watched not in uuid_ for uuid_ in seen)
    assert seen == [f"session:claude_code/{r['session_id']}" for r in rows if r["session_id"] != watched]
    assert all(len(t) == 1 and next(iter(t.values())) == 59 for t in totals), totals
    # On the route page that held it the count is exact; on any other page
    # whether it was counted is unknowable from there, so the count is a floor.
    assert "session_total" in totals[0] if watched_index < PAGE else "session_total_at_least" in totals[0]


def test_a_cursor_from_another_entity_is_refused_not_restarted(client, app):
    """The route's 422 for an `after` that is not a row of THIS entity reaches
    the wire as the per-ref gap, never as page one again."""
    a = client.create_project("sessions-a", kind="general")
    b = client.create_project("sessions-b", kind="general")
    _seed_sessions(app, "project", a["id"], [_session(70 - i) for i in range(70)])
    _seed_sessions(app, "project", b["id"], [_session(5 - i) for i in range(5)])
    service = _service(client)
    cursor = service.get_entity(f"project:{a['id']}", view="sessions", token_budget=100_000)[
        "next_cursor"
    ]
    out = _bounded(
        _wire(service, "entity", {"refs": [f"project:{b['id']}"], "view": "sessions", "cursor": cursor})
    )
    [gap] = out["missing"]
    assert gap["ref"] == f"project:{b['id']}" and out["rows"] == []
    assert gap["reason"].startswith("ValidationError:") and "`after`" in gap["reason"]


def test_an_uncursored_page_from_an_older_server_keeps_the_beyond_limit_marker(client, app):
    """The hosted MCP and the API deploy apart. A server before the paged routes
    ignores `order`/`after` and answers the leaf door's oldest-first 50 with no
    `next_after` key: read as a page that would claim a 60-session entity
    complete at 50 rows, so it is read as the capped list it is."""
    entity = _anchor(client, "project")
    rows = [_session(60 - i) for i in range(60)]
    _seed_sessions(app, "project", entity["id"], rows)
    app.sessions_route_uncursored = True
    out = _bounded(
        _wire(
            _service(client),
            "entity",
            {"refs": [f"project:{entity['id']}"], "view": "sessions", "token_budget": 8000},
        ),
        limit=8000,
    )
    assert len(out["data"]["sessions"]) == PAGE and out["data"]["session_total"] == 60
    assert "next_cursor" not in out
    assert out["completeness"]["state"] == "partial"
    assert "sessions_beyond_server_limit" in out["completeness"]["missing"]


def test_the_sessions_view_takes_no_options(client, app):
    entity = _anchor(client, "project")
    with pytest.raises(errors.ValidationError, match="accepts no view options"):
        _service(client).get_entity(
            f"project:{entity['id']}", view="sessions", filters={"grep": "scorer"}
        )


# -- view="summary_history" ----------------------------------------------------


def _version(n: int, **extra) -> dict:
    return {
        "version": n,
        "created_at": f"2026-10-{1 + n % 28:02d}T00:00:00Z",
        "created_by": "Ada" if n % 2 else None,
        "source": "agent",
        "via": "daemon",
        "mode": "summary",
        "session_title": f"session {n}",
        "size_chars": 100 * n,
        "markdown": f"# v{n}\n\nwhat happened in version {n}",
        **extra,
    }


def _seed_summary(app, kind: str, entity_id: str, versions: int) -> None:
    app.summaries[(kind, entity_id)] = {
        "markdown": f"# v{versions}\n\nwhat happened in version {versions}",
        "version": versions,
        "edited_by": "Ada",
        "via": "daemon",
        "versions": [_version(n) for n in range(1, versions + 1)],
    }


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_summary_history_lists_versions_newest_first_without_their_text(client, app, kind):
    entity = _anchor(client, kind)
    _seed_summary(app, kind, entity["id"], 3)
    out = _service(client).get_entity(f"{kind}:{entity['id']}", view="summary_history")
    assert out["data"]["view"] == "summary_history"
    rows = out["data"]["versions"]
    assert [r["version"] for r in rows] == [3, 2, 1]
    assert rows[0] == {
        "version": 3,
        "created_at": "2026-10-04T00:00:00Z",
        "created_by": "Ada",
        "source": "agent",
        "via": "daemon",
        "mode": "summary",
        "session_title": "session 3",
        "size_chars": 300,
    }
    assert "created_by" not in rows[1], "a null is absent, not null"
    assert all("markdown" not in r for r in rows)
    assert "next_cursor" not in out and "completeness" not in out


def test_summary_history_walks_the_routes_before_cursor(client, app):
    entity = _anchor(client, "project")
    _seed_summary(app, "project", entity["id"], 60)
    service = _service(client)
    first = service.get_entity(
        f"project:{entity['id']}", view="summary_history", token_budget=100_000
    )
    assert [r["version"] for r in first["data"]["versions"]] == list(range(60, 10, -1))
    second = service.get_entity(
        f"project:{entity['id']}",
        view="summary_history",
        token_budget=100_000,
        cursor=first["next_cursor"],
    )
    assert [r["version"] for r in second["data"]["versions"]] == list(range(10, 0, -1))
    assert "next_cursor" not in second
    [_, resumed] = [r for r in app.requests if r.url.path.endswith("/summary/versions")]
    assert resumed.url.params["before"] == "11" and resumed.url.params["limit"] == "50"


@pytest.mark.parametrize("kind", ["project", "experiment"])
@pytest.mark.parametrize("version", [2, "2"])
def test_one_version_reads_its_markdown(client, app, kind, version):
    entity = _anchor(client, kind)
    _seed_summary(app, kind, entity["id"], 3)
    out = _service(client).get_entity(
        f"{kind}:{entity['id']}", view="summary_history", filters={"version": version}
    )
    assert "versions" not in out["data"]
    assert out["data"]["summary_version"] == {
        "version": 2,
        "created_at": "2026-10-03T00:00:00Z",
        "created_by": None,
        "source": "agent",
        "via": "daemon",
        "mode": "summary",
        "markdown": "# v2\n\nwhat happened in version 2",
    }
    [request] = [r for r in app.requests if r.url.path.endswith("/summary/versions/2")]
    assert request.url.path.startswith("/v1/")


def test_one_version_survives_the_wire_whole(client, app):
    entity = _anchor(client, "project")
    _seed_summary(app, "project", entity["id"], 1)
    app.summaries[("project", entity["id"])]["versions"][0]["markdown"] = "科学 evidence " * 1500
    service = _service(client)
    args = {
        "refs": [f"project:{entity['id']}"],
        "view": "summary_history",
        "view_options": {"version": 1},
        "token_budget": 512,
    }
    pieces, cursor = [], None
    for _ in range(100):
        page = _bounded(_wire(service, "entity", {**args, **({"cursor": cursor} if cursor else {})}))
        assert page["data"]["format"] == "json_fragment"
        pieces.append(page["data"]["text"])
        cursor = page.get("next_cursor")
        if cursor is None:
            assert page["data"]["complete"] is True
            break
    else:
        pytest.fail("the walk never ended")
    assert len(pieces) > 1, "a long version is fragmented, never cut"
    # Never cut: the fragments reassemble to the whole version, byte for byte.
    whole = json.loads("".join(pieces))["data"]
    assert whole["view"] == "summary_history" and whole["entity_type"] == "project"
    assert whole["summary_version"]["markdown"] == "科学 evidence " * 1500
    assert whole["summary_version"]["version"] == 1


def test_summary_history_refuses_another_branches_arguments(client, app):
    """The per-branch allowlist (#735): `grep` belongs to the transcript view.
    Accepted here it would be dropped and the list returned as if narrowed."""
    entity = _anchor(client, "project")
    _seed_summary(app, "project", entity["id"], 3)
    with pytest.raises(errors.ValidationError, match=r"\['version'\]"):
        _service(client).get_entity(
            f"project:{entity['id']}", view="summary_history", filters={"grep": "scorer"}
        )
    # "²" and "①" are digits `str.isdigit` accepts and `int()` refuses: a 422,
    # never an unhandled ValueError; 2**31 binds to no int4 column.
    for bad in (-1, "x", True, 1.5, "²", "①", 2**31):
        with pytest.raises(errors.ValidationError, match="whole number"):
            _service(client).get_entity(
                f"project:{entity['id']}", view="summary_history", filters={"version": bad}
            )


@pytest.mark.parametrize("version", [0, "0"])
def test_version_zero_is_a_recorded_version(client, app, version):
    """Pages written before the counter existed sit at version 0 and the list
    shows them (`app/overviews/history.py`); the read must open them too."""
    entity = _anchor(client, "project")
    _seed_summary(app, "project", entity["id"], 2)
    app.summaries[("project", entity["id"])]["versions"].append(
        _version(0, created_by=None, session_title=None, markdown="# seeded\n\nbefore 0200")
    )
    service = _service(client)
    rows = service.get_entity(f"project:{entity['id']}", view="summary_history")["data"]["versions"]
    assert [r["version"] for r in rows] == [2, 1, 0]
    out = service.get_entity(
        f"project:{entity['id']}", view="summary_history", filters={"version": version}
    )
    assert out["data"]["summary_version"]["version"] == 0
    assert out["data"]["summary_version"]["markdown"] == "# seeded\n\nbefore 0200"


def test_a_cursor_whose_after_is_not_a_version_is_refused_not_restarted(client, app):
    """A hand-built cursor (the token is base64, not sealed) with a non-version
    `after` must be a 422 like every other malformed cursor, never the first
    page again under a fresh cursor -- that walk would never end."""
    from probe.mcp.service import _join_get_cursor

    entity = _anchor(client, "project")
    _seed_summary(app, "project", entity["id"], 3)
    for after in ("not-a-version", "²", "-1"):
        forged = _join_get_cursor("summary_history", 0, after=after)
        with pytest.raises(errors.ValidationError, match="malformed cursor"):
            _service(client).get_entity(
                f"project:{entity['id']}", view="summary_history", cursor=forged
            )


def test_a_version_that_does_not_exist_names_the_version_not_the_entity(client, app):
    """The entity resolved a moment ago; the per-ref `missing` row must say the
    VERSION is what is absent, on a server with the routes."""
    entity = _anchor(client, "project")
    _seed_summary(app, "project", entity["id"], 3)
    out = _bounded(
        _wire(
            _service(client),
            "entity",
            {
                "refs": [f"project:{entity['id']}"],
                "view": "summary_history",
                "view_options": {"version": 99},
            },
        )
    )
    [gap] = out["missing"]
    assert gap["ref"] == f"project:{entity['id']}" and out["rows"] == []
    assert gap["reason"].startswith("NotFoundError: no version 99 of this project's summary")


def test_summary_history_on_a_server_without_the_route_says_so(client, app):
    entity = _anchor(client, "project")
    app.summary_route_absent = True
    out = _bounded(
        _wire(
            _service(client),
            "entity",
            {"refs": [f"project:{entity['id']}"], "view": "summary_history"},
        )
    )
    [gap] = out["missing"]
    assert gap["reason"].startswith("NotFoundError: no summary history for this project")
    assert "predates the summary routes" in gap["reason"]


def test_the_new_pairs_are_declared_and_allowlisted_exactly():
    for kind in (EntityType.PROJECT, EntityType.EXPERIMENT):
        assert (kind, View.SESSIONS) in _VIEWS and (kind, View.SUMMARY_HISTORY) in _VIEWS
        assert _VIEW_OPTIONS[(kind, View.SUMMARY_HISTORY)] == {"version"}
        assert (kind, View.SESSIONS) not in _VIEW_OPTIONS


# -- view="overview" gains markdown --------------------------------------------


def _seed_page(app, kind: str, entity_id: str) -> dict:
    page = {
        "html": "<h1>Generated overview</h1><p>evidence</p>",
        "series": {"manifest": [], "data": {}},
        "saved_page_readable": True,
        "version": 7,
        "source": "lane",
    }
    app.__dict__.setdefault("overviews", {})[(kind, entity_id)] = page
    return page


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_overview_carries_the_summary_markdown_beside_the_html(client, app, kind):
    entity = _anchor(client, kind)
    page = _seed_page(app, kind, entity["id"])
    _seed_summary(app, kind, entity["id"], 2)
    out = _service(client).get_entity(f"{kind}:{entity['id']}", view="overview")
    saved = out["data"]["overview"]
    assert saved["html"] == page["html"] and saved["version"] == 7
    assert saved["markdown"] == "# v2\n\nwhat happened in version 2"


@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_overview_leaves_markdown_out_on_a_server_without_the_route(client, app, kind):
    entity = _anchor(client, kind)
    page = _seed_page(app, kind, entity["id"])
    app.summary_route_absent = True
    out = _service(client).get_entity(f"{kind}:{entity['id']}", view="overview")
    saved = out["data"]["overview"]
    assert saved["html"] == page["html"]
    assert "markdown" not in saved, "absent says the server cannot say; null would say none"
    assert "completeness" not in out


def test_a_page_with_no_summary_yet_reads_as_an_empty_markdown(client, app):
    entity = _anchor(client, "project")
    _seed_page(app, "project", entity["id"])
    out = _service(client).get_entity(f"project:{entity['id']}", view="overview")
    assert out["data"]["overview"]["markdown"] == ""


# -- search: transcripts are not project-scoped ----------------------------------


def test_a_project_scoped_transcript_search_says_so(client, app):
    app.search_response = search_response()
    app.echoes_project_scope = True
    project = client.create_project("scoped", kind="general")
    service = _service(client)
    page = _bounded(
        _wire(
            service,
            "search",
            {"query": "scorer", "search_in": ["transcripts"], "project_id": project["id"]},
        ),
        limit=2000,
    )
    note = page["data"]["note"]
    assert note.startswith("transcripts are not project-scoped")
    assert "view=sessions" in note and "view_options.grep" in note
    # Named beside other corpora the scope DOES apply to: still said.
    page = _bounded(
        _wire(
            service,
            "search",
            {"query": "scorer", "search_in": ["experiments", "transcripts"], "project_id": project["id"]},
        ),
        limit=2000,
    )
    assert "note" in page["data"]
    # `search_in` omitted asks for every corpus, transcripts included: the
    # same hits are dropped, so the same note is said.
    page = _bounded(
        _wire(service, "search", {"query": "scorer", "project_id": project["id"]}), limit=2000
    )
    assert page["data"]["note"] == note


@pytest.mark.parametrize(
    "arguments",
    [
        {"search_in": ["files"], "project_id": "p-1"},
        {"search_in": ["transcripts"]},
        {},
    ],
)
def test_other_searches_carry_no_note(client, app, arguments):
    app.search_response = search_response()
    app.echoes_project_scope = True
    page = _bounded(_wire(_service(client), "search", {"query": "scorer", **arguments}), limit=2000)
    assert "note" not in page["data"]


def test_the_project_id_parameter_says_it_in_the_schema():
    """The schema channel is delivered verbatim; the description is capped."""
    import anyio

    tools = anyio.run(create_server(object()).list_tools)
    search = next(t for t in tools if t.name == "search")
    doc = search.inputSchema["properties"]["project_id"]["description"]
    assert "transcripts" in doc and "view=sessions" in doc
    entity = next(t for t in tools if t.name == "entity")
    options = entity.inputSchema["properties"]["view_options"]["description"]
    assert "version" in options and "summary_history" in options


# -- the SDK methods the views ride -------------------------------------------


def test_sdk_session_pages_send_the_routes_own_parameters(client, app):
    project = client.create_project("sdk-sessions", kind="general")
    experiment = client.create_experiment("e", "e", question="q", project_id=project["id"])
    app.project_sessions[project["id"]] = [_session(3), _session(2), _session(1)]
    app.experiment_sessions[experiment["id"]] = [_session(9)]
    page = client.list_project_sessions(project["id"], order="newest", limit=2)
    assert [r["session_id"] for r in page["sessions"]] == [_session(3)["session_id"], _session(2)["session_id"]]
    assert page["session_total"] == 3 and page["next_after"] == _session(2)["session_id"]
    rest = client.list_project_sessions(project["id"], order="newest", after=page["next_after"], limit=2)
    assert [r["session_id"] for r in rest["sessions"]] == [_session(1)["session_id"]]
    assert rest["next_after"] is None
    oldest = client.list_project_sessions(project["id"])
    assert [r["session_id"] for r in oldest["sessions"]] == [
        _session(1)["session_id"],
        _session(2)["session_id"],
        _session(3)["session_id"],
    ]
    assert _session_requests(app)[-1].url.params["order"] == "oldest"
    xpage = client.list_experiment_sessions(experiment["id"], project_id=project["id"], order="newest")
    assert [r["session_id"] for r in xpage["sessions"]] == [_session(9)["session_id"]]
    assert _session_requests(app)[-1].url.path == (
        f"/v1/projects/{project['id']}/experiments/{experiment['id']}/sessions"
    )
    with pytest.raises(errors.NotFoundError):
        client.list_project_sessions(str(uuid.uuid4()))


def test_sdk_summary_reads_take_either_anchor(client, app):
    project = client.create_project("sdk-summary", kind="general")
    experiment = client.create_experiment("e", "e", question="q", project_id=project["id"])
    _seed_summary(app, "project", project["id"], 3)
    _seed_summary(app, "experiment", experiment["id"], 2)
    assert client.get_summary(project=project["id"])["version"] == 3
    assert client.get_summary(experiment=experiment["id"], project=project["id"])["version"] == 2
    assert client.get_summary(experiment=experiment["id"])["version"] == 2, "located by the SDK"
    versions = client.list_summary_versions(project=project["id"], before=3, limit=1)
    assert [v["version"] for v in versions["versions"]] == [2] and versions["next_before"] == 2
    assert client.get_summary_version(1, experiment=experiment["id"], project=project["id"])[
        "markdown"
    ].startswith("# v1")
    with pytest.raises(ValueError, match="name the anchor"):
        client.get_summary()
    app.summary_route_absent = True
    with pytest.raises(errors.NotFoundError):
        client.get_summary(project=project["id"])
