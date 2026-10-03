"""The reads the dashboard assistant had and this MCP lacked, for every agent.

Three surfaces gained them:

  * `browse` -- four flat listings beside the tree: runs (newest first, with a
    liveness filter), workspaces, the notes catalog, and the files in Shared or
    one workspace;
  * `entity` -- a run's saved `views`, its sandbox `diff` and its `sessions`, an
    artifact's `sessions`, a project's `readme`, and one `sub_note` whole;
  * `metrics` -- `series`, several runs x keys in one read.

Every test drives the real tool layer (or the service directly where the point
is the view's shape) against the FakeApp backend, and each guards a failure an
agent would otherwise read as an answer: a skipped row, a dropped filter, a
truncation reported as complete, or a refusal in words about a field the caller
never wrote.
"""

from __future__ import annotations

import asyncio
import base64
import itertools
import json
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from probe.mcp import accounting
from probe.mcp import server as server_mod
from probe.mcp import service as service_module
from probe.mcp.contract import BrowseMode, MetricMode, MissingMarker, View
from probe.mcp.server import create_server
from probe.mcp.service import ResearchReadService, _supported_views
from probe.mcp.source import ResearchOSSource
from probe.sdk import errors


def _service(client) -> ResearchReadService:
    return ResearchReadService(ResearchOSSource(client))


def _server(client):
    return create_server(_service(client))


def _call(server, tool: str, args: dict) -> dict:
    """Invoke a tool the way an MCP client does, and parse the one text block."""
    result = asyncio.run(server.call_tool(tool, args))
    payload = result[1] if isinstance(result, tuple) else result
    if isinstance(payload, list):
        return json.loads(payload[0].text)
    return payload


def _error(server, tool: str, args: dict) -> str:
    with pytest.raises(ToolError) as excinfo:
        _call(server, tool, args)
    return str(excinfo.value)


def _walk(server, tool: str, args: dict, key: str, *, max_pages: int = 60):
    """Follow `next_cursor` to the end: (every row delivered, every page)."""
    rows: list = []
    pages: list[dict] = []
    cursor = None
    for _ in range(max_pages):
        out = _call(server, tool, {**args, **({"cursor": cursor} if cursor else {})})
        pages.append(out)
        rows.extend(out["data"][key])
        cursor = out.get("next_cursor")
        if not cursor:
            return rows, pages
    raise AssertionError(f"{tool} walk did not end in {max_pages} pages")


def _params(app, path: str) -> list[dict]:
    """Every request's query params to one path, oldest first."""
    return [dict(r.url.params.multi_items()) for r in app.requests if r.url.path == path]


# -- browse(mode="runs") ------------------------------------------------------


_PROJECT = "33333333-3333-3333-3333-333333333333"
_EXPERIMENT = "44444444-4444-4444-4444-444444444444"

#: Each seeded run is created a little after the last, to the microsecond, so
#: the runs list's (created_at, id) keyset has distinct, exact keys to resume on.
_CLOCK = itertools.count(1)
_T0 = datetime(2026, 9, 30, tzinfo=timezone.utc)


def _created_at() -> str:
    moment = _T0 + timedelta(microseconds=next(_CLOCK) * 1_000 + 7)
    return moment.isoformat().replace("+00:00", "Z")


def _newest_first(ids: list[str]) -> list[str]:
    """Seed order reversed: the runs list answers newest first."""
    return [f"run:{rid}" for rid in reversed(ids)]


def _seed_run(app, name: str, *, status: str = "completed", stale: bool = False, **extra) -> str:
    rid = str(uuid.uuid4())
    app.runs[rid] = {
        "id": rid,
        "customer_id": "lab-42",
        "name": name,
        "slug": f"{name}-7",
        "status": status,
        "source": "sdk",
        "project_id": extra.pop("project_id", _PROJECT),
        "experiment_id": extra.pop("experiment_id", None),
        "created_at": _created_at(),
        "updated_at": "2026-09-30T00:00:00Z",
        "summary": {},
        "tags": extra.pop("tags", []),
        **({"_stale": True} if stale else {}),
        **extra,
    }
    return rid


def test_runs_mode_lists_runs_flat_in_backend_order_with_both_addresses(client, app):
    ids = [_seed_run(app, f"run-{i}") for i in range(3)]
    out = _call(_server(client), "browse", {"mode": "runs"})

    rows = out["data"]["runs"]
    # The backend's order (newest first) is the answer; nothing re-sorts it.
    assert [row["uuid"] for row in rows] == _newest_first(ids)
    assert rows[-1]["slug"] == "run:run-0-7"
    assert rows[-1]["status"] == "completed"
    assert "id" not in rows[0]  # the browse address contract: slug + uuid only
    assert out["data"]["available_views"] == {"run": _supported_views("run")}
    assert "completeness" not in out and "next_cursor" not in out
    assert _params(app, "/v1/runs")[-1]["limit"] == "10"


def test_runs_mode_with_no_runs_is_an_empty_list_not_an_error(client, app):
    out = _call(_server(client), "browse", {"mode": "runs"})
    assert out["data"]["runs"] == []
    assert "completeness" not in out and "next_cursor" not in out


def test_active_sends_the_servers_liveness_filter_and_keeps_only_live_runs(client, app):
    live = _seed_run(app, "live", status="running")
    _seed_run(app, "stale", status="running", stale=True)
    _seed_run(app, "done")
    out = _call(_server(client), "browse", {"mode": "runs", "active": True})
    assert [row["uuid"] for row in out["data"]["runs"]] == [f"run:{live}"]
    assert _params(app, "/v1/runs")[-1]["active"] == "true"


def test_runs_ref_narrows_by_parent_and_a_slug_is_refused_in_the_callers_words(client, app):
    mine = _seed_run(app, "mine", experiment_id=_EXPERIMENT)
    _seed_run(app, "elsewhere", project_id=str(uuid.uuid4()))
    server = _server(client)

    out = _call(server, "browse", {"mode": "runs", "ref": f"project:{_PROJECT}"})
    assert [row["uuid"] for row in out["data"]["runs"]] == [f"run:{mine}"]
    assert _params(app, "/v1/runs")[-1]["project_id"] == _PROJECT

    _call(server, "browse", {"mode": "runs", "ref": f"experiment:{_EXPERIMENT}"})
    assert _params(app, "/v1/runs")[-1]["experiment_id"] == _EXPERIMENT

    message = _error(server, "browse", {"mode": "runs", "ref": "project:bird-sql"})
    assert "`project:<uuid>` or `experiment:<uuid>`" in message
    assert "slugs go to `entity`" in message


def test_a_budget_cut_run_list_walks_every_run_exactly_once(client, app):
    """The listing sends whole rows only and continues from the last one SENT:
    a cursor resuming from the end of the fetched page would skip the rows the
    budget left out, and nothing on the page would say so."""
    ids = [_seed_run(app, f"r{i:02d}", description="d" * 150) for i in range(12)]
    rows, pages = _walk(
        _server(client), "browse", {"mode": "runs", "limit": 50, "token_budget": 512}, "runs"
    )
    assert [row["uuid"] for row in rows] == _newest_first(ids)
    assert len(pages) > 1
    for page in pages[:-1]:
        assert page["completeness"]["missing"] == [MissingMarker.TRUNCATED_BY_TOKEN_BUDGET]
    assert "completeness" not in pages[-1]


def test_a_run_list_cursor_survives_the_real_json_rpc_boundary(client, app):
    """The walk above, through an MCP client session: the delivery cursor has to
    come back through JSON-RPC argument parsing intact for the next page to
    resume where the last one stopped."""
    from mcp.shared.memory import create_connected_server_and_client_session

    ids = [_seed_run(app, f"r{i:02d}", description="d" * 150) for i in range(6)]

    async def walk() -> list[str]:
        seen: list[str] = []
        async with create_connected_server_and_client_session(_server(client)) as session:
            arguments: dict = {"mode": "runs", "token_budget": 512}
            for _ in range(20):
                result = await session.call_tool("browse", arguments)
                assert not result.isError, result.content[0].text
                page = json.loads(result.content[0].text)
                seen += [row["uuid"] for row in page["data"]["runs"]]
                if not page.get("next_cursor"):
                    return seen
                arguments = {**arguments, "cursor": page["next_cursor"]}
        raise AssertionError("walk did not end")

    assert asyncio.run(walk()) == _newest_first(ids)


def test_a_full_page_with_more_behind_it_is_pagination_not_truncation(client, app):
    """`limit` is the backend page; reaching its end with more beyond is an
    ordinary cursor, state complete -- the `entity` rule. Only a BUDGET cut is
    partial."""
    ids = [_seed_run(app, f"r{i:02d}") for i in range(7)]
    server = _server(client)
    first = _call(server, "browse", {"mode": "runs", "limit": 3})
    assert len(first["data"]["runs"]) == 3
    assert "completeness" not in first and first["next_cursor"]
    rows, _ = _walk(server, "browse", {"mode": "runs", "limit": 3}, "runs")
    assert [row["uuid"] for row in rows] == _newest_first(ids)


#: The field that names a row, per flat listing.
_ROW_NAME = {"runs": "uuid", "notes": "uuid", "files": "name", "workspaces": "workspace_id"}


def _walk_mutating(server, args: dict, key: str, mutate) -> list[str]:
    """Walk a listing, calling `mutate(rows_sent_so_far)` between every page --
    the world changing under a paged read."""
    seen: list[str] = []
    cursor = None
    for _ in range(40):
        page = _call(server, "browse", {**args, **({"cursor": cursor} if cursor else {})})
        seen += [row[_ROW_NAME[key]] for row in page["data"][key]]
        cursor = page.get("next_cursor")
        if not cursor:
            return seen
        mutate(seen)
    raise AssertionError("walk did not end")


def test_an_active_run_that_ends_mid_walk_does_not_skip_a_live_one(client, app):
    """Review of #2216, reproduced: with `active=true`, a run that stops being
    live between two pages used to shift every later row by one, because the
    next page re-read the same backend page and skipped the count already sent.
    2 of 4 still-running runs were never delivered. Resuming after the last run
    SENT (its own keyset) cannot skip one."""
    ids = [_seed_run(app, f"r{i:02d}", status="running", description="d" * 150) for i in range(8)]

    def end_the_first_sent(seen: list[str]) -> None:
        for uuid_ref in seen:
            app.runs[uuid_ref.removeprefix("run:")]["status"] = "completed"

    seen = _walk_mutating(
        _server(client),
        {"mode": "runs", "active": True, "limit": 50, "token_budget": 512},
        "runs",
        end_the_first_sent,
    )
    assert seen == _newest_first(ids)  # every run, each once, in order


def test_a_run_deleted_between_pages_drops_nothing_else(client, app):
    ids = [_seed_run(app, f"r{i:02d}", description="d" * 150) for i in range(8)]

    def delete_the_first_sent(seen: list[str]) -> None:
        app.runs.pop(seen[0].removeprefix("run:"), None)

    seen = _walk_mutating(
        _server(client),
        {"mode": "runs", "limit": 50, "token_budget": 512},
        "runs",
        delete_the_first_sent,
    )
    assert seen == _newest_first(ids)


def test_the_run_list_resumes_on_its_own_keyset_cursor(client, app):
    """The cursor the server is sent after a budget cut is the list's own
    `(created_at, id)` keyset of the last row SENT -- not a re-read of the page."""
    ids = [_seed_run(app, f"r{i:02d}", description="d" * 150) for i in range(8)]
    server = _server(client)
    first = _call(server, "browse", {"mode": "runs", "limit": 50, "token_budget": 512})
    last_sent = first["data"]["runs"][-1]
    _call(
        server,
        "browse",
        {"mode": "runs", "limit": 50, "token_budget": 512, "cursor": first["next_cursor"]},
    )
    sent = _params(app, "/v1/runs")[-1]["cursor"]
    at, _, rid = base64.urlsafe_b64decode(sent).decode().partition("|")
    assert f"run:{rid}" == last_sent["uuid"]
    created = app.runs[rid]["created_at"].replace("Z", "+00:00")
    assert datetime.fromisoformat(at) == datetime.fromisoformat(created)
    assert len(ids) == 8


def test_a_cursor_from_another_listing_is_refused_not_reinterpreted(client, app):
    _seed_run(app, "a")
    service = _service(client)
    runs_cursor = service._list_cursor(BrowseMode.RUNS, "elsewhere")
    with pytest.raises(errors.ValidationError, match="does not continue browse"):
        service.browse_list(BrowseMode.WORKSPACES, cursor=runs_cursor)


# -- browse(mode="workspaces") ------------------------------------------------


def test_workspaces_mode_names_every_workspace_by_its_scoping_argument(client, app):
    out = _call(_server(client), "browse", {"mode": "workspaces"})
    rows = out["data"]["workspaces"]
    by_id = {row["workspace_id"]: row for row in rows}
    assert set(by_id) == set(app.workspaces)
    for wid, row in by_id.items():
        assert row["name"] == app.workspaces[wid]["name"]
        assert row["kind"] == app.workspaces[wid]["kind"]
    # Not an entity: nothing to advertise for `entity`.
    assert "available_views" not in out["data"]


def test_workspaces_limit_pages_the_whole_list(client, app):
    rows, pages = _walk(_server(client), "browse", {"mode": "workspaces", "limit": 1}, "workspaces")
    assert len(pages) == len(app.workspaces)
    assert sorted(row["workspace_id"] for row in rows) == sorted(app.workspaces)


# -- browse(mode="notes") -----------------------------------------------------


def _seed_notes(client, app) -> dict:
    project = client.create_project("scoring", kind="general")
    app.projects[project["id"]]["notes"] = "Scorer v2 replaced the regex scorer."
    rid = _seed_run(app, "eval", project_id=project["id"])
    app.runs[rid]["notes"] = "Distrust step 400: the scorer cache was stale."
    shared_id = str(uuid.uuid4())
    sub_id = str(uuid.uuid4())
    app.sub_notes[sub_id] = {
        "id": sub_id,
        "parent_kind": "artifact",
        "parent_id": shared_id,
        "title": "Scorer caveat",
        "body": "Relative paths only. " * 60,
        "notes_version": 1,
        "created_at": "2026-09-30T00:00:00Z",
        "updated_at": "2026-09-30T00:00:00Z",
    }
    app.team_note["body"] = "## Cluster\n\nGPUs are oversubscribed on weekdays.\n"
    return {"project": project["id"], "run": rid, "sub_note": sub_id, "artifact": shared_id}


def test_notes_mode_lists_every_note_with_an_address_entity_opens(client, app):
    seeded = _seed_notes(client, app)
    out = _call(_server(client), "browse", {"mode": "notes", "token_budget": 8000})
    rows = {row["uuid"]: row for row in out["data"]["notes"]}
    assert set(rows) == {
        "team-note",
        f"project:{seeded['project']}",
        f"run:{seeded['run']}",
        f"sub_note:{seeded['sub_note']}",
    }
    sub = rows[f"sub_note:{seeded['sub_note']}"]
    assert sub["entity_type"] == "sub_note" and sub["title"] == "Scorer caveat"
    assert sub["ancestors"] == [{"uuid": f"artifact:{seeded['artifact']}", "title": "P"}]
    assert out["data"]["available_views"]["sub_note"] == ["card"]
    sent = _params(app, "/v1/notes")[-1]
    # A limit selects the flat listing (a bare call is the explorer's root tree),
    # and sub-notes are opted in because they are openable here now.
    assert sent["limit"] == "10" and sent["include_sub_notes"] == "true"


def test_notes_query_is_sent_and_narrows_the_catalog(client, app):
    seeded = _seed_notes(client, app)
    out = _call(_server(client), "browse", {"mode": "notes", "query": "stale"})
    assert [row["uuid"] for row in out["data"]["notes"]] == [f"run:{seeded['run']}"]
    assert out["data"]["query"] == "stale"
    assert _params(app, "/v1/notes")[-1]["query"] == "stale"


def test_notes_query_with_no_match_is_an_empty_answer(client, app):
    _seed_notes(client, app)
    out = _call(_server(client), "browse", {"mode": "notes", "query": "nothing-says-this"})
    assert out["data"]["notes"] == []
    assert "completeness" not in out and "next_cursor" not in out


def test_notes_walk_follows_the_catalogs_own_cursor(client, app):
    _seed_notes(client, app)
    rows, pages = _walk(_server(client), "browse", {"mode": "notes", "limit": 1}, "notes")
    # The team note rides the first page OUTSIDE its limit, as the real catalog
    # serves it: four notes in three pages, each exactly once.
    assert len(pages) == 3 and len(rows) == 4 and len({row["uuid"] for row in rows}) == 4
    # Every continuation is the catalog's own keyset cursor, passed through.
    cursors = [p.get("cursor") for p in _params(app, "/v1/notes")]
    assert cursors[0] is None and all(cursors[1:])


def _seed_run_notes(app, n: int, *, text: str = "x" * 150) -> list[str]:
    ids = []
    for i in range(n):
        rid = _seed_run(app, f"noted-{i:02d}")
        app.runs[rid]["notes"] = f"note {i}: {text}"
        ids.append(rid)
    return ids


def test_a_note_emptied_between_pages_drops_nothing_else(client, app):
    """The notes walk resumes after the last row SENT, found again by identity
    in its catalog page -- not by skipping a count of rows, which a note that
    disappears in between turns into a skipped row."""
    ids = _seed_run_notes(app, 8)

    def empty_the_first_sent(seen: list[str]) -> None:
        app.runs[seen[0].removeprefix("run:")]["notes"] = ""

    seen = _walk_mutating(
        _server(client),
        {"mode": "notes", "limit": 50, "token_budget": 512},
        "notes",
        empty_the_first_sent,
    )
    assert seen == _newest_first(ids)


def test_a_walk_whose_last_sent_note_is_emptied_carries_on(client, app):
    """The resume position is the catalog's own keyset built from the last row
    sent, so that row disappearing moves nothing: the walk used to refuse."""
    ids = _seed_run_notes(app, 8)

    def empty_the_last_sent(seen: list[str]) -> None:
        app.runs[seen[-1].removeprefix("run:")]["notes"] = ""

    seen = _walk_mutating(
        _server(client),
        {"mode": "notes", "limit": 50, "token_budget": 512},
        "notes",
        empty_the_last_sent,
    )
    assert seen == _newest_first(ids)


def test_newer_notes_do_not_push_the_resume_point_off_its_page(client, app):
    """Review of 2980f4e74, reproduced: limit=10, a budget cut after 9, then 3
    new notes -- the 9th was pushed off the re-read first page and the walk
    refused with "restart". A keyset cursor names a position, not a page."""
    ids = _seed_run_notes(app, 10, text="y" * 20)
    server = _server(client)
    args = {"mode": "notes", "limit": 10, "token_budget": 560}
    first = _call(server, "browse", args)
    sent = [row["uuid"] for row in first["data"]["notes"]]
    assert 1 < len(sent) < len(ids) and first["next_cursor"]
    # Newer notes now fill the whole re-read first page, so the last one sent is
    # no longer on it (the review hit this with 3 new notes and 9 sent).
    _seed_run_notes(app, 10, text="new")
    rest, _ = _walk(server, "browse", {**args, "cursor": first["next_cursor"]}, "notes")
    assert sent + [row["uuid"] for row in rest] == _newest_first(ids)


def test_a_note_kind_with_no_known_rank_still_resumes_by_finding_its_row(client, app, monkeypatch):
    """A catalog kind this client has no rank for cannot be named by the
    keyset; it resumes by finding its row again, and says "restart" -- never
    guesses -- when that row is gone."""
    from probe.mcp import source as source_module

    monkeypatch.setattr(
        source_module,
        "_NOTE_KIND_RANK",
        {k: v for k, v in source_module._NOTE_KIND_RANK.items() if k != "run"},
    )
    ids = _seed_run_notes(app, 8)
    server = _server(client)
    args = {"mode": "notes", "limit": 50, "token_budget": 512}
    rows, _ = _walk(server, "browse", args, "notes")
    assert [row["uuid"] for row in rows] == _newest_first(ids)
    first = _call(server, "browse", args)
    app.runs[first["data"]["notes"][-1]["uuid"].removeprefix("run:")]["notes"] = ""
    message = _error(server, "browse", {**args, "cursor": first["next_cursor"]})
    assert "source_changed" in message and "restart" in message


def test_a_notes_row_opens_the_whole_sub_note(client, app):
    seeded = _seed_notes(client, app)
    server = _server(client)
    [row] = _call(server, "browse", {"mode": "notes", "query": "Scorer caveat"})["data"]["notes"]
    card = _call(server, "entity", {"refs": [row["uuid"]], "token_budget": 8000})
    assert card["data"]["entity"]["body"] == app.sub_notes[seeded["sub_note"]]["body"]


# -- browse(mode="files") -----------------------------------------------------


def _file(name: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "customer_id": "lab-42",
        "name": name,
        "kind": "file",
        "status": "complete",
        "is_reference": False,
        "size_bytes": 10,
        "created_at": "2026-09-30T00:00:00Z",
    }


def test_files_mode_without_a_workspace_lists_the_shared_folder(client, app):
    scorer, checkpoint = _file("scorer.py"), _file("checkpoints/step-2000.pt")
    app.artifacts["shared:team"] = [scorer, checkpoint]
    out = _call(_server(client), "browse", {"mode": "files"})
    # The route's order (`ORDER BY name`), not the order they were written in.
    assert [row["uuid"] for row in out["data"]["files"]] == [
        f"artifact:{checkpoint['id']}",
        f"artifact:{scorer['id']}",
    ]
    assert out["data"]["available_views"] == {"artifact": _supported_views("artifact")}
    assert "workspace_id" not in out["data"]

    narrowed = _call(_server(client), "browse", {"mode": "files", "prefix": "checkpoints"})
    assert [row["name"] for row in narrowed["data"]["files"]] == ["checkpoints/step-2000.pt"]
    assert _params(app, "/v1/shared/files")[-1]["prefix"] == "checkpoints"


def test_files_mode_with_a_workspace_reads_that_workspaces_files(client, app):
    wid = next(iter(app.workspaces))
    app.artifacts[f"workspace:{wid}"] = [_file("protocol.md")]
    out = _call(_server(client), "browse", {"mode": "files", "workspace_id": wid})
    assert [row["name"] for row in out["data"]["files"]] == ["protocol.md"]
    assert out["data"]["workspace_id"] == wid
    assert any(r.url.path == f"/v1/workspaces/{wid}/files" for r in app.requests)

    message = _error(_server(client), "browse", {"mode": "files", "workspace_id": "mine"})
    assert "workspace_id must be a workspace UUID" in message


def test_files_page_with_a_lookahead_and_walk_every_file(client, app):
    """The file routes take no cursor: each page asks for one row past its
    window, so "there is more" is a fact rather than a full-page guess."""
    rows = [_file(f"f{i}.txt") for i in range(5)]
    app.artifacts["shared:team"] = rows
    delivered, pages = _walk(_server(client), "browse", {"mode": "files", "limit": 2}, "files")
    assert [row["name"] for row in delivered] == [r["name"] for r in rows]
    assert len(pages) == 3
    # A continuation reads the route's whole ceiling and resumes after the last
    # NAME sent; only the first page can size its read to the window.
    assert [p["limit"] for p in _params(app, "/v1/shared/files")] == ["3", "1000", "1000"]


@pytest.mark.parametrize("which", ["first", "last"])
def test_a_file_deleted_between_pages_drops_nothing_else(client, app, which):
    """Resuming after the last NAME sent: a deleted file -- an earlier one, or
    the very one the page ended on -- moves no other file's position. Seeded
    OUT of name order: the route sorts `ORDER BY name`, and so does the fake."""
    rows = [_file(f"f{i}.txt") for i in (4, 0, 6, 2, 5, 1, 3)]
    app.artifacts["shared:team"] = list(rows)

    def delete_one(seen: list[str]) -> None:
        name = seen[0] if which == "first" else seen[-1]
        app.artifacts["shared:team"] = [
            r for r in app.artifacts["shared:team"] if r["name"] != name
        ]

    seen = _walk_mutating(_server(client), {"mode": "files", "limit": 2}, "files", delete_one)
    assert seen == sorted(r["name"] for r in rows)


def test_a_workspace_deleted_between_pages_drops_nothing_else(client, app):
    for i in range(4):
        wid = str(uuid.uuid4())
        app.workspaces[wid] = {
            "id": wid,
            "customer_id": "lab-42",
            "name": f"ws-{i}",
            "slug": f"ws-{i}",
            "kind": "team",
            "created_at": "2026-09-30T00:00:00Z",
        }
    expected = _call(_server(client), "browse", {"mode": "workspaces", "limit": 50})
    order = [row["workspace_id"] for row in expected["data"]["workspaces"]]

    def delete_the_first_sent(seen: list[str]) -> None:
        app.workspaces.pop(seen[0], None)

    seen = _walk_mutating(
        _server(client), {"mode": "workspaces", "limit": 2}, "workspaces", delete_the_first_sent
    )
    assert seen == order


@pytest.mark.parametrize("new_name", ["aaa-first", "zzz-last", "Mid"])
def test_a_workspace_renamed_between_pages_skips_no_other(client, app, new_name):
    """Review of 2980f4e74, reproduced: the route sorts `lower(name), id`, so a
    renamed workspace MOVES -- and resuming after wherever the last-sent id now
    sat ended the walk early (4 of 6 never sent) or repeated rows. Resuming
    past the last-sent SORT KEY sends every other workspace exactly once."""
    app.workspaces.clear()
    for name in ("Bravo", "alpha", "Delta", "charlie", "echo", "Foxtrot"):
        wid = str(uuid.uuid4())
        app.workspaces[wid] = {
            "id": wid,
            "customer_id": "lab-42",
            "name": name,
            "slug": name.lower(),
            "kind": "team",
            "created_at": "2026-09-30T00:00:00Z",
        }
    order = [
        row["workspace_id"]
        for row in _call(_server(client), "browse", {"mode": "workspaces", "limit": 50})["data"][
            "workspaces"
        ]
    ]
    renamed: list[str] = []

    def rename_the_last_sent(seen: list[str]) -> None:
        if not renamed:
            renamed.append(seen[-1])
            app.workspaces[seen[-1]]["name"] = new_name

    seen = _walk_mutating(
        _server(client), {"mode": "workspaces", "limit": 2}, "workspaces", rename_the_last_sent
    )
    others = [wid for wid in order if wid not in renamed]
    assert [wid for wid in seen if wid not in renamed] == others  # none skipped or repeated
    assert renamed[0] in seen


def test_the_workspace_order_folds_only_ascii_case(client, app):
    """Postgres `lower()` under the C collation folds ASCII letters only, so
    `Émile` keeps its capital É (U+00C9) and sorts BEFORE `éa` (U+00E9...);
    Python's `str.lower` would fold it to `émile` and sort it after."""
    key = ResearchReadService._workspace_key
    assert key({"name": "Émile", "id": "1"}) < key({"name": "éa", "id": "2"})
    assert key({"name": "ALPHA", "id": "1"}) == ("alpha", "1")


def test_files_past_the_routes_read_ceiling_are_reported_not_hidden(client, app, monkeypatch):
    monkeypatch.setattr(ResearchReadService, "_FILES_BACKEND_MAX", 3)
    app.artifacts["shared:team"] = [_file(f"f{i}.txt") for i in range(5)]
    out = _call(_server(client), "browse", {"mode": "files"})
    assert len(out["data"]["files"]) == 3 and "next_cursor" not in out
    assert out["completeness"]["missing"] == [MissingMarker.FILES_BEYOND_BACKEND_LIMIT]


# -- browse: each mode refuses what it does not read --------------------------


@pytest.mark.parametrize(
    ("args", "refused", "reader"),
    [
        ({"query": "grpo"}, "query", "notes"),
        ({"active": True}, "active", "runs"),
        ({"prefix": "ckpt"}, "prefix", "files"),
        ({"mode": "runs", "depth": 2}, "depth", "tree"),
        ({"mode": "runs", "workspace_id": str(uuid.uuid4())}, "workspace_id", "files or tree"),
        ({"mode": "notes", "ref": f"project:{_PROJECT}"}, "ref", "runs or tree"),
        ({"mode": "workspaces", "status": "running"}, "status", "runs or tree"),
        ({"mode": "files", "tags": ["x"]}, "tags", "runs or tree"),
    ],
)
def test_an_argument_the_mode_does_not_read_is_refused_never_dropped(
    client, app, args, refused, reader
):
    message = _error(_server(client), "browse", args)
    mode = args.get("mode", "tree")
    assert f"mode={mode} does not read {refused}" in message
    assert f"read by mode={reader}" in message
    # REFUSED before any listing was read.
    assert not any(r.url.path in ("/v1/runs", "/v1/notes", "/v1/browse") for r in app.requests)


def test_a_files_ref_points_at_the_entity_view_that_lists_an_entitys_files(client, app):
    message = _error(_server(client), "browse", {"mode": "files", "ref": f"run:{uuid.uuid4()}"})
    assert 'entity(view="artifacts")' in message


@pytest.mark.parametrize(
    "args",
    [
        {"mode": "notes", "active": False, "tags": [], "prefix": ""},
        {"mode": "files", "query": "", "active": False},
        {"mode": "workspaces", "tags": [], "query": "", "prefix": ""},
        {"mode": "runs", "query": "", "prefix": ""},
    ],
)
def test_an_argument_that_asks_for_nothing_is_accepted_in_every_mode(client, app, args):
    """`active=false`, `tags=[]`, `query=""` are the same request as leaving
    them out; refusing them refused a correct call."""
    out = _call(_server(client), "browse", args)
    assert "data" in out


def test_the_tree_accepts_an_argument_that_asks_for_nothing(client, app):
    # The tree's own fixture is the backend browse payload; the check under test
    # runs before it, so it is driven directly.
    for args in ({"active": False}, {"tags": []}, {"query": ""}, {"prefix": ""}):
        server_mod._browse_args_for_mode(BrowseMode.TREE, args)
    with pytest.raises(ToolError, match="does not read active"):
        server_mod._browse_args_for_mode(BrowseMode.TREE, {"active": True})


def test_query_and_prefix_reach_the_listing_as_the_caller_typed_them(client, app):
    """FastMCP JSON-parses a string argument unless its annotation is plain
    `str`: `query="null"` arrived as None (and slipped past the tree's
    refusal), and `query="[1e-4, 3e-4]"` arrived as a list and was refused."""
    server = _server(client)
    message = _error(server, "browse", {"query": "null"})
    assert "mode=tree does not read query" in message
    _call(server, "browse", {"mode": "notes", "query": "[1e-4, 3e-4]"})
    assert _params(app, "/v1/notes")[-1]["query"] == "[1e-4, 3e-4]"
    app.artifacts["shared:team"] = [_file("[ablation]/run.txt")]
    _call(server, "browse", {"mode": "files", "prefix": "[ablation]"})
    assert _params(app, "/v1/shared/files")[-1]["prefix"] == "[ablation]"


def test_an_explicit_null_query_or_prefix_means_absent(client, app):
    """Typing them plain `str` closed the "null"-string trap and refused an
    explicit JSON null; null is the absent value, as "" is."""
    _seed_run_notes(app, 2)
    app.artifacts["shared:team"] = [_file("a.txt")]
    server = _server(client)
    notes = _call(server, "browse", {"mode": "notes", "query": None})
    assert len(notes["data"]["notes"]) == 2 and "query" not in _params(app, "/v1/notes")[-1]
    files = _call(server, "browse", {"mode": "files", "prefix": None, "query": None})
    assert [row["name"] for row in files["data"]["files"]] == ["a.txt"]
    assert "prefix" not in _params(app, "/v1/shared/files")[-1]


def test_the_runs_mode_says_it_lists_filed_runs_and_where_unfiled_ones_are(client):
    """GET /v1/runs answers FILED runs only (0260), so "every run" overstated
    what mode=runs returns; unfiled runs are on the browse root."""
    tools = asyncio.run(_server(client).list_tools())
    description = next(t for t in tools if t.name == "browse").description
    assert "every run filed under a project" in description
    assert "the team's last N runs" in description
    assert "Unfiled runs are in browse with no `ref`" in description
    assert "my last N runs" not in description


def test_runs_mode_does_not_list_unfiled_runs(client, app):
    filed = _seed_run(app, "filed")
    _seed_run(app, "floating", project_id=None)
    out = _call(_server(client), "browse", {"mode": "runs"})
    assert [row["uuid"] for row in out["data"]["runs"]] == [f"run:{filed}"]


def test_browse_mode_tables_and_signature_are_the_same_set(client):
    """Every browse parameter is read by SOME mode, and no table names one the
    signature lacks -- the structural pair `metrics` has, for the same reason."""
    tools = asyncio.run(_server(client).list_tools())
    spec = next(t for t in tools if t.name == "browse")
    common = {"mode", "cursor", "token_budget"}
    declared = set(spec.inputSchema["properties"]) - common
    assert set(server_mod._BROWSE_MODE_ARGS) == set(BrowseMode)
    assert set().union(*server_mod._BROWSE_MODE_ARGS.values()) == declared


# -- browse: the caller's own session work stays out --------------------------


@contextmanager
def _hiding(session: str) -> Iterator[None]:
    state = accounting.begin_request("claude_code", session, {}, hide_session_work=True)
    try:
        yield
    finally:
        accounting.end_request(state)


class _CreatedSource(ResearchOSSource):
    def __init__(self, client, created):
        super().__init__(client)
        self.created = created

    def session_created(self, session_id):
        if self.created is None:
            raise errors.NotFoundError("no such route")
        return self.created


def test_runs_mode_hides_the_runs_the_callers_session_created(client, app):
    session = str(uuid.uuid4())
    mine, theirs = _seed_run(app, "mine"), _seed_run(app, "theirs")
    service = ResearchReadService(_CreatedSource(client, {"project_ids": [], "run_ids": [mine]}))
    with _hiding(session):
        out = service.browse_list(BrowseMode.RUNS)
    assert [row["uuid"] for row in out["data"]["runs"]] == [f"run:{theirs}"]
    assert _params(app, "/v1/runs")[-1]["exclude_origin_session"] == session
    # The private positions still line up with the rows that were KEPT.
    assert len(out["_list_after"]) == 1


def test_an_unverifiable_exclusion_is_said_out_loud(client, app):
    _seed_run(app, "a")
    service = ResearchReadService(_CreatedSource(client, None))
    with _hiding(str(uuid.uuid4())):
        out = service.browse_list(BrowseMode.RUNS)
    assert MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED in out["completeness"]["missing"]


def test_a_notes_page_of_only_hidden_rows_reads_on_to_the_next(client, app):
    """Hidden rows are dropped AFTER the catalog cut its page, so a page of the
    caller's own work used to come back empty with no marker -- an answer that
    reads as "nothing written down". The listing reads on until it has a row."""
    theirs = _seed_run_notes(app, 2)
    mine = _seed_run_notes(app, 4)  # newer: the catalog's first pages
    service = ResearchReadService(_CreatedSource(client, {"project_ids": [], "run_ids": mine}))
    with _hiding(str(uuid.uuid4())):
        out = service.browse_list(BrowseMode.NOTES, limit=2)
    assert [row["uuid"] for row in out["data"]["notes"]] == _newest_first(theirs)
    assert "completeness" not in out


def test_too_many_hidden_pages_stop_with_a_marker_and_a_cursor(client, app, monkeypatch):
    monkeypatch.setattr(ResearchReadService, "_HIDDEN_FILL_PAGES", 2)
    theirs = _seed_run_notes(app, 1)
    mine = _seed_run_notes(app, 6)
    service = ResearchReadService(_CreatedSource(client, {"project_ids": [], "run_ids": mine}))
    with _hiding(str(uuid.uuid4())):
        first = service.browse_list(BrowseMode.NOTES, limit=2)
        assert first["data"]["notes"] == []
        assert first["completeness"]["missing"] == [MissingMarker.PAGE_HIDDEN_AS_OWN_SESSION_WORK]
        second = service.browse_list(BrowseMode.NOTES, limit=2, cursor=first["next_cursor"])
    assert [row["uuid"] for row in second["data"]["notes"]] == _newest_first(theirs)


# -- entity: a run's saved views, sandbox diff and sessions --------------------


def _run(client, app) -> str:
    project = client.create_project("folding", kind="general")
    client.create_experiment("dockq", "dockq", question="q", project_id=project["id"])
    return client.run(project="folding", experiment="dockq", name="eval-1").id


def test_run_views_lists_the_saved_metric_views_with_their_edit_precondition(client, app):
    rid = _run(client, app)
    app.views[rid] = [
        {
            "id": "view-1",
            "run_id": rid,
            "name": "loss ratio",
            "spec": {"expr": "a / b"},
            "created_by": "user:test",
            "created_at": "2026-09-30T00:00:00Z",
            "updated_at": "2026-09-30T01:00:00Z",
        }
    ]
    out = _service(client).get_entity(f"run:{rid}", view="views")
    assert out["data"]["views"] == [
        {
            "id": "view-1",
            "name": "loss ratio",
            "spec": {"expr": "a / b"},
            "created_by": "user:test",
            "created_at": "2026-09-30T00:00:00Z",
            "updated_at": "2026-09-30T01:00:00Z",
        }
    ]
    assert "completeness" not in out


def test_a_run_with_no_saved_views_says_so_with_an_empty_list(client, app):
    rid = _run(client, app)
    out = _service(client).get_entity(f"run:{rid}", view="views")
    assert out["data"]["views"] == [] and "completeness" not in out


_COUNTS = {
    "added": 1,
    "modified": 3,
    "deleted": 1,
    "unchanged": 9,
    "begin_files": 13,
    "end_files": 13,
}


def _seed_diff(app, rid: str, trial: str, n: int) -> list[str]:
    paths = [f"src/f{i:02d}.py" for i in range(n)]
    app.sandbox_diffs[(rid, trial)] = {
        "entries": [
            {"path": p, "status": "modified", "type": "f", "symlink_target": None} for p in paths
        ],
        "counts": _COUNTS,
    }
    return paths


def test_run_diff_needs_its_trial_and_says_where_trial_names_come_from(client, app):
    rid = _run(client, app)
    with pytest.raises(errors.ValidationError) as excinfo:
        _service(client).get_entity(f"run:{rid}", view="diff")
    assert "view_options.trial" in str(excinfo.value)
    assert "attempt_ref" in str(excinfo.value)
    assert not app.sandbox_diff_calls  # refused before any request


def test_run_diff_serves_changed_paths_as_rows_and_whole_scan_counts(client, app):
    rid = _run(client, app)
    paths = _seed_diff(app, rid, "t-1", 3)
    out = _service(client).get_entity(
        f"run:{rid}", view="diff", filters={"trial": "t-1", "path_prefix": "src/"}
    )
    data = out["data"]
    assert [e["path"] for e in data["entries"]] == paths
    assert "symlink_target" not in data["entries"][0]  # nulls dropped from rows
    assert data["counts"] == _COUNTS and data["trial"] == "t-1"
    assert app.sandbox_diff_calls[-1]["path_prefix"] == "src/"
    assert "completeness" not in out


def test_run_diff_resumes_on_the_routes_own_path_cursor(client, app, monkeypatch):
    """Each page is ONE route page, read from the path the last page ENDED on --
    the route's own cursor. It used to re-walk the diff from its first path on
    every page and skip the ones already sent, re-reading the trial's manifests
    from storage each time."""
    monkeypatch.setattr(service_module, "_PAGE_FETCH", 2)
    rid = _run(client, app)
    paths = _seed_diff(app, rid, "t-1", 5)
    service = _service(client)
    seen: list[str] = []
    cursor = None
    for _ in range(10):
        out = service.get_entity(f"run:{rid}", view="diff", filters={"trial": "t-1"}, cursor=cursor)
        seen += [e["path"] for e in out["data"]["entries"]]
        assert out["data"]["counts"] == _COUNTS  # every page: the whole scan's totals
        cursor = out.get("next_cursor")
        if not cursor:
            break
    assert seen == paths
    # One route call per page, each starting after the previous page's last path.
    assert [call.get("cursor") for call in app.sandbox_diff_calls] == [None, paths[1], paths[3]]


def test_run_diff_budget_cut_resumes_after_the_last_path_sent(client, app):
    """A budget that holds fewer paths than the route page carried resumes
    after the last path SENT, not after the route page's last path."""
    rid = _run(client, app)
    paths = _seed_diff(app, rid, "t-1", 40)
    service = _service(client)
    first = service.get_entity(
        f"run:{rid}", view="diff", filters={"trial": "t-1"}, token_budget=200
    )
    sent = [e["path"] for e in first["data"]["entries"]]
    assert 0 < len(sent) < len(paths)
    service.get_entity(
        f"run:{rid}",
        view="diff",
        filters={"trial": "t-1"},
        token_budget=200,
        cursor=first["next_cursor"],
    )
    assert app.sandbox_diff_calls[-1]["cursor"] == sent[-1]


def test_a_diff_of_long_paths_reserves_room_for_its_cursor(client, app):
    """Review of 2980f4e74, reproduced: the diff cursor carries the last PATH,
    and rows fitted on a chars/4 estimate with no room for it made every page
    of long paths overflow once the cursor landed -- delivered as fragments: 29
    calls for these 60 entries, where the old offset cursor took 22. Fitted
    exactly, cursor included, no page is split."""
    rid = _run(client, app)
    paths = [f"src/{'deep/' * 48}f{i:02d}.py" for i in range(60)]
    assert all(len(p) > 240 for p in paths)
    app.sandbox_diffs[(rid, "t-1")] = {
        "entries": [{"path": p, "status": "modified", "type": "f"} for p in paths],
        "counts": _COUNTS,
    }
    server = _server(client)
    args = {"refs": [f"run:{rid}"], "view": "diff", "view_options": {"trial": "t-1"}}
    seen: list[str] = []
    calls, cursor = 0, None
    while True:
        page = _call(
            server,
            "entity",
            {**args, "token_budget": 700, **({"cursor": cursor} if cursor else {})},
        )
        calls += 1
        assert "format" not in page["data"], f"page {calls} was split into fragments"
        seen += [e["path"] for e in page["data"]["entries"]]
        cursor = page.get("next_cursor")
        if not cursor:
            break
    assert seen == paths
    assert calls < 22


def test_a_resume_view_that_sends_no_rows_keeps_its_place(client, app, monkeypatch):
    """A `resume_key` view whose page sends nothing while more exists must
    carry the position it was read from; an offset-0 cursor with no `after`
    would restart the walk from its first row."""
    from probe.mcp.service import _ViewData

    rid = _run(client, app)
    seen_after: list = []

    def empty_page(self, entity, request):
        seen_after.append(request.after)
        return _ViewData(rows=[], rows_key="entries", more_beyond=True, resume_key="path")

    monkeypatch.setattr(ResearchReadService, "_view_run_diff", empty_page)
    service = _service(client)
    cursor = service_module._join_get_cursor("diff", 0, after="src/m.py")
    out = service.get_entity(f"run:{rid}", view="diff", filters={"trial": "t"}, cursor=cursor)
    again = service.get_entity(
        f"run:{rid}", view="diff", filters={"trial": "t"}, cursor=out["next_cursor"]
    )
    assert seen_after == ["src/m.py", "src/m.py"]
    assert again["next_cursor"] == out["next_cursor"]


def test_run_diff_for_an_unknown_trial_is_the_routes_404(client, app):
    rid = _run(client, app)
    with pytest.raises(errors.NotFoundError):
        _service(client).get_entity(f"run:{rid}", view="diff", filters={"trial": "nope"})


def _session(i: int, agent: str = "claude_code") -> dict:
    return {
        "session_id": f"{i:08d}-0000-0000-0000-000000000000",
        "agent": agent,
        "owner_name": "Dev",
        "name": f"session {i}",
        "first_seen_at": "2026-09-30T00:00:00Z",
        "last_seen_at": "2026-09-30T01:00:00Z",
        "direct": True,
    }


def test_run_sessions_names_who_made_the_run_as_openable_rows(client, app):
    rid = _run(client, app)
    app.run_sessions[rid] = [_session(1), _session(2, agent="cursor")]
    out = _service(client).get_entity(f"run:{rid}", view="sessions")
    first, second = out["data"]["sessions"]
    assert first["uuid"] == "session:claude_code/00000001-0000-0000-0000-000000000000"
    assert first["owner_name"] == "Dev" and "direct" not in first
    # An agent the transcript read does not know gets the bare, probing form.
    assert second["uuid"] == "session:00000002-0000-0000-0000-000000000000"
    assert out["data"]["session_total"] == 2 and "completeness" not in out


def test_run_sessions_past_the_bundles_cap_are_reported_with_the_true_total(client, app):
    rid = _run(client, app)
    app.run_sessions[rid] = [_session(i) for i in range(60)]
    out = _service(client).get_entity(f"run:{rid}", view="sessions", token_budget=100_000)
    assert len(out["data"]["sessions"]) == 50
    assert out["data"]["session_total"] == 60
    assert out["completeness"]["missing"] == [MissingMarker.SESSIONS_BEYOND_SERVER_LIMIT]


def test_a_run_no_session_touched_has_no_sessions(client, app):
    rid = _run(client, app)
    out = _service(client).get_entity(f"run:{rid}", view="sessions")
    assert out["data"]["sessions"] == [] and out["data"]["session_total"] == 0
    assert "completeness" not in out


# -- entity: an artifact's sessions -------------------------------------------


def test_artifact_sessions_reads_the_files_own_route(client, app):
    shared = _file("scorer.py")
    app.artifacts["shared:team"] = [shared]
    app.artifact_sessions[shared["id"]] = [_session(1)]
    out = _service(client).get_entity("artifact:scorer.py", view="sessions")
    assert [row["uuid"] for row in out["data"]["sessions"]] == [
        "session:claude_code/00000001-0000-0000-0000-000000000000"
    ]
    [request] = [r for r in app.requests if r.url.path.endswith("/sessions")]
    assert request.url.path == f"/v1/artifacts/{shared['id']}/sessions"
    assert request.url.params["limit"] == "50"


def test_artifact_sessions_on_an_unknown_artifact_is_not_found(client, app):
    with pytest.raises(errors.NotFoundError):
        _service(client).get_entity("artifact:no-such-file.py", view="sessions")


def test_a_capped_session_list_without_the_watched_session_reports_a_floor(client, app):
    """The server lists 50 of 60 and counts all 60. With the watched session
    hidden and not among the 50, whether those 60 included it is unknowable:
    `session_total: 60` could be one too many, so the count becomes a floor."""
    rid = _run(client, app)
    sessions = [_session(i) for i in range(60)]
    app.run_sessions[rid] = sessions
    watched = sessions[55]["session_id"]  # past the server's cap
    with _hiding(watched):
        out = _service(client).get_entity(f"run:{rid}", view="sessions", token_budget=100_000)
    assert "session_total" not in out["data"]
    assert out["data"]["session_total_at_least"] == 59
    assert len(out["data"]["sessions"]) == 50
    assert MissingMarker.SESSIONS_BEYOND_SERVER_LIMIT in out["completeness"]["missing"]


def test_the_watched_session_is_left_out_of_both_sessions_views(client, app):
    """Under `X-Probe-Hide-Session-Work` every other view leaves out the work of
    the session the reader watches; a `sessions` view answering "who made this"
    with that very session was the one that did not."""
    rid = _run(client, app)
    watched, other = _session(1), _session(2)
    app.run_sessions[rid] = [watched, other]
    shared = _file("scorer.py")
    app.artifacts["shared:team"] = [shared]
    app.artifact_sessions[shared["id"]] = [watched, other]
    service = _service(client)
    with _hiding(watched["session_id"].upper()):
        for ref in (f"run:{rid}", "artifact:scorer.py"):
            out = service.get_entity(ref, view="sessions")
            assert [row["uuid"] for row in out["data"]["sessions"]] == [
                f"session:claude_code/{other['session_id']}"
            ]
            assert out["data"]["session_total"] == 1
    # Without the opt-in, the same read lists both.
    out = service.get_entity(f"run:{rid}", view="sessions")
    assert out["data"]["session_total"] == 2


def test_run_sessions_and_handoff_read_a_source_backed_run(client, app):
    """A W&B-mirrored run's bundle answers 422 unless the read names the
    coverage contract (app/read_models/router.py); both bundle views 422'd on
    exactly the imported runs."""
    rid = _run(client, app)
    app.source_backed_runs.add(rid)
    app.run_sessions[rid] = [_session(1)]
    service = _service(client)
    out = service.get_entity(f"run:{rid}", view="sessions")
    assert out["data"]["session_total"] == 1
    service.get_entity(f"run:{rid}", view="handoff")
    bundle_reads = [r for r in app.requests if r.url.path.endswith("/bundle")]
    assert all(r.url.params["source_read_contract"] == "coverage-v1" for r in bundle_reads)


# -- entity: a project's README -----------------------------------------------


def test_project_readme_serves_the_text_and_where_it_came_from(client, app):
    project = client.create_project("folding", kind="general")
    app.project_readmes[project["id"]] = {
        "state": "snapshot",
        "repo": "acme/folding",
        "path": "README.md",
        "commit_sha": "c" * 40,
        "markdown": "# Folding\n",
        "reason": None,
    }
    out = _service(client).get_entity(f"project:{project['id']}", view="readme")
    assert out["data"]["readme"] == {
        "state": "snapshot",
        "repo": "acme/folding",
        "path": "README.md",
        "commit_sha": "c" * 40,
        "markdown": "# Folding\n",
    }


def test_a_project_without_a_repository_says_so(client, app):
    """`none` -- what production answers for a project with no repository --
    carries no text and no reason, so the view says what it means."""
    project = client.create_project("folding", kind="general")
    out = _service(client).get_entity(f"project:{project['id']}", view="readme")
    assert out["data"]["readme"] == {
        "state": "none",
        "note": "No repository is attached to this project, so it has no README.",
    }


@pytest.mark.parametrize(
    ("served", "says"),
    [
        (
            {
                "state": "live",
                "repo": "acme/folding",
                "html_url": "https://github.com/acme/folding",
            },
            "Probe holds no copy",
        ),
        (
            {"state": "unavailable", "repo": "acme/folding", "reason": "not_found_or_no_access"},
            "GitHub answered 404",
        ),
        ({"state": "unavailable", "reason": "rate_limited"}, "rate-limited"),
        ({"state": "unavailable", "reason": "upstream_error"}, "did not answer"),
        ({"state": "unavailable", "reason": "app_permission_required"}, "Contents permission"),
        ({"state": "unavailable", "reason": "something_new"}, "could not be read"),
    ],
)
def test_every_readme_state_without_text_says_why(client, app, served, says):
    project = client.create_project("folding", kind="general")
    app.project_readmes[project["id"]] = served
    readme = _service(client).get_entity(f"project:{project['id']}", view="readme")["data"][
        "readme"
    ]
    assert readme["state"] == served["state"]
    assert says in readme["note"]
    assert "markdown" not in readme


def test_a_readme_snapshot_carries_no_note(client, app):
    project = client.create_project("folding", kind="general")
    app.project_readmes[project["id"]] = {"state": "snapshot", "markdown": "# Folding\n"}
    readme = _service(client).get_entity(f"project:{project['id']}", view="readme")["data"][
        "readme"
    ]
    assert readme == {"state": "snapshot", "markdown": "# Folding\n"}


def test_a_long_readme_arrives_as_text_fragments_that_rejoin_exactly(client, app):
    """A document view: the markdown pages as TEXT, and the first fragment says
    which repo and commit it is -- a fragment of prose with no provenance would
    be a document with no source."""
    project = client.create_project("folding", kind="general")
    markdown = "".join(
        f"## Section {i}\n\nThe evaluation step {i} is described here.\n" for i in range(200)
    )
    app.project_readmes[project["id"]] = {
        "state": "snapshot",
        "repo": "acme/folding",
        "commit_sha": "c" * 40,
        "markdown": markdown,
    }
    server = _server(client)
    args = {"refs": [f"project:{project['id']}"], "view": "readme", "token_budget": 1000}
    first = _call(server, "entity", args)
    assert first["data"]["format"] == "text_fragment"
    assert first["data"]["context"]["readme"] == {
        "state": "snapshot",
        "repo": "acme/folding",
        "commit_sha": "c" * 40,
    }
    text, page = first["data"]["text"], first
    while page.get("next_cursor"):
        page = _call(server, "entity", {**args, "cursor": page["next_cursor"]})
        text += page["data"]["text"]
    assert text == markdown


# -- entity: one sub-note, whole ----------------------------------------------


def _seed_sub_note(app, body: str) -> str:
    sub_id = str(uuid.uuid4())
    app.sub_notes[sub_id] = {
        "id": sub_id,
        "parent_kind": "run",
        "parent_id": str(uuid.uuid4()),
        "title": "Scorer caveat",
        "body": body,
        "notes_version": 4,
        "created_at": "2026-09-30T00:00:00Z",
        "updated_at": "2026-09-30T00:00:00Z",
    }
    return sub_id


def test_a_sub_note_card_is_the_whole_document(client, app):
    body = "Relative paths only: absolute ones score zero. " * 40  # past the 700 excerpt
    sub_id = _seed_sub_note(app, body)
    out = _service(client).get_entity(f"sub_note:{sub_id}", token_budget=8000)
    entity = out["data"]["entity"]
    assert entity["body"] == body
    assert entity["title"] == "Scorer caveat"
    assert entity["chars"] == len(body) and entity["limit_chars"] == 4000
    assert entity["notes_version"] == 4
    assert out["data"]["available_views"] == [View.CARD]


def test_a_sub_note_has_no_separate_record_view(client, app):
    sub_id = _seed_sub_note(app, "x")
    with pytest.raises(errors.ValidationError, match="sub_note supports"):
        _service(client).get_entity(f"sub_note:{sub_id}", view="record")


def test_an_unknown_or_malformed_sub_note_id_is_refused(client, app):
    service = _service(client)
    with pytest.raises(errors.NotFoundError):
        service.get_entity(f"sub_note:{uuid.uuid4()}")
    with pytest.raises(errors.ValidationError, match="is not a sub-note id"):
        service.get_entity("sub_note:../runs/x")
    # Refused before the id reached a URL path.
    assert not any("/runs/x" in r.url.path for r in app.requests)


def test_the_notes_view_hands_out_each_sub_notes_address(client, app):
    rid = _run(client, app)
    long_body = "Distrust step 400. " * 60
    page = client._create_sub_note("run", rid, "Caveat", long_body)
    out = _service(client).get_entity(f"run:{rid}", view="notes", token_budget=8000)
    [item] = out["data"]["sub_notes"]
    assert item["uuid"] == f"sub_note:{page['id']}"
    assert item["truncated"] is True and item["read_all"] == "entity(refs=[uuid])"
    whole = _service(client).get_entity(item["uuid"], token_budget=8000)
    assert whole["data"]["entity"]["body"] == long_body


def test_a_long_sub_note_pages_as_text_with_its_title_in_front(client, app):
    body = "".join(f"Line {i}: the scorer reads relative paths only.\n" for i in range(150))
    sub_id = _seed_sub_note(app, body)
    server = _server(client)
    args = {"refs": [f"sub_note:{sub_id}"], "token_budget": 600}
    first = _call(server, "entity", args)
    assert first["data"]["format"] == "text_fragment"
    assert first["data"]["context"]["entity"]["title"] == "Scorer caveat"
    assert "body" not in first["data"]["context"]["entity"]
    text, page = first["data"]["text"], first
    while page.get("next_cursor"):
        page = _call(server, "entity", {**args, "cursor": page["next_cursor"]})
        text += page["data"]["text"]
    assert text == body


# -- metrics(mode="series") ---------------------------------------------------


def _runs_with_series(client, app, n: int = 2, *, points: int = 3) -> list[str]:
    ids = []
    for i in range(n):
        rid = str(uuid.uuid4())
        app.seed_series(rid, "loss", {s: 1.0 / (s + 1) for s in range(points)})
        app.seed_series(rid, "reward", {s: float(s) for s in range(points)})
        ids.append(rid)
    return ids


def test_series_reads_several_runs_in_one_call_as_positional_points(client, app):
    first, second = _runs_with_series(client, app)
    out = _call(
        _server(client),
        "metrics",
        {"mode": "series", "run_ids": [f"run:{first}", second], "keys": ["loss"]},
    )
    data = out["data"]
    assert data["point_fields"] == ["step_index", "value"]
    assert data["max_points"] == 100 and data["series_total"] == 2
    assert [(row["run_id"], row["key"]) for row in data["series"]] == [
        (first, "loss"),
        (second, "loss"),
    ]
    assert data["series"][0]["points"] == [[0, 1.0], [1, 0.5], [2, 1.0 / 3]]
    assert data["series"][0]["point_count"] == 3
    assert "read_provenance" not in data["series"][0]  # an exact read says nothing
    assert "completeness" not in out and "next_cursor" not in out
    # ONE backend read, the `run:` prefix stripped, the default bound named.
    assert app.series_queries == [
        {
            "run_ids": [first, second],
            "keys": ["loss"],
            "max_points": 100,
            "source_read_contract": "coverage-v1",
        }
    ]


def test_series_forwards_its_window_and_smoothing_and_says_when_it_sampled(client, app):
    [rid] = _runs_with_series(client, app, 1, points=10)
    out = _call(
        _server(client),
        "metrics",
        {
            "mode": "series",
            "run_ids": [rid],
            "keys": ["reward"],
            "smoothing": "ema",
            "step_from": 1,
            "step_to": 8,
            "max_points": 3,
        },
    )
    sent = app.series_queries[-1]
    assert (sent["smoothing"], sent["step_from"], sent["step_to"], sent["max_points"]) == (
        "ema",
        1,
        8,
        3,
    )
    data = out["data"]
    assert data["point_fields"] == ["step_index", "value", "smoothed"]
    [row] = data["series"]
    # 8 points in the window, cut to max_points=3 by the min-max downsample:
    # with an odd bound that is the two endpoints, which IS a cut series.
    assert row["point_count"] == 2
    assert row["read_provenance"] == {
        "source": "probe",
        "coverage": "sampled",
        "exactness": "sampled",
        "warning": "Probe downsampled this local series for display",
    }


def test_only_a_series_the_downsample_can_have_cut_is_labelled_sampled(client, app):
    """The API stamps EVERY local series of a read that sends `max_points` as
    downsampled (provider_reads.local_read_provenance), and the MCP always sends
    one -- so every row said "sampled", including a 3-point series read whole.
    A row keeps the label only when the series has LOGGED more points than the
    bound (the catalog's count, one `series/latest` call): only then can the
    downsample have run."""
    short = str(uuid.uuid4())
    app.seed_series(short, "loss", {s: 1.0 / (s + 1) for s in range(3)})
    long = str(uuid.uuid4())
    app.seed_series(long, "loss", {s: float((s * 37) % 101) for s in range(250)})
    mirrored = str(uuid.uuid4())
    app.seed_series(mirrored, "loss", {s: 0.5 for s in range(3)})
    app.source_backed_runs.add(mirrored)
    out = _call(
        _server(client),
        "metrics",
        {
            "mode": "series",
            "run_ids": [short, long, mirrored],
            "keys": ["loss"],
            "token_budget": 8000,
        },
    )
    rows = {row["run_id"]: row for row in out["data"]["series"]}
    assert rows[short]["point_count"] == 3 and "read_provenance" not in rows[short]
    # Cut, and SHORTER than the bound: an endpoint doubled as a bucket's extreme.
    # Its count alone could not have said it was sampled.
    assert rows[long]["point_count"] < 100
    assert rows[long]["read_provenance"]["exactness"] == "sampled"
    # A provider's own receipt is never dropped, however short the series.
    assert rows[mirrored]["read_provenance"]["source"] == "wandb"


def test_an_unknown_logged_count_keeps_the_sampled_label(client, app):
    """No catalog answer (an older server, a failed read) is not evidence the
    series is whole: the label stays, so unsure reads as "may be sampled"."""
    rid = str(uuid.uuid4())
    app.seed_series(rid, "loss", {s: float(s) for s in range(3)})
    app.fail_paths = {"/v1/series/latest"}
    out = _call(_server(client), "metrics", {"mode": "series", "run_ids": [rid], "keys": ["loss"]})
    [row] = out["data"]["series"]
    assert row["read_provenance"]["coverage"] == "sampled"


def test_a_wall_clock_series_keeps_its_timestamps_under_a_step_window(client, app):
    """A step window drops every stepless point server-side, so a timestamp
    column chosen by "does any point lack a step" vanished exactly when a
    wall-clock series was in the read. The column follows the series' axis."""
    rid = str(uuid.uuid4())
    app.seed_series(rid, "loss", {s: float(s) for s in range(4)})
    app.series_points[rid].append(
        {
            "run_id": rid,
            "key": "gpu_util",
            "kind": "model",
            "x_axis": "wall_clock",
            "dimensions": {},
            "points": [{"step_index": None, "value": 0.9, "wall_clock": "2026-07-27T00:00:00Z"}],
        }
    )
    out = _call(
        _server(client),
        "metrics",
        {"mode": "series", "run_ids": [rid], "keys": ["loss", "gpu_util"], "step_from": 1},
    )
    assert out["data"]["point_fields"] == ["step_index", "value", "wall_clock"]
    loss = next(row for row in out["data"]["series"] if row["key"] == "loss")
    assert loss["points"][0] == [1, 1.0, "2026-07-27T00:00:00Z"]


def test_series_with_no_matching_key_is_an_empty_complete_answer(client, app):
    [rid] = _runs_with_series(client, app, 1)
    out = _call(_server(client), "metrics", {"mode": "series", "run_ids": [rid], "keys": ["acc"]})
    assert out["data"]["series"] == [] and out["data"]["series_total"] == 0
    assert "completeness" not in out


def test_a_budget_cut_series_read_walks_every_series_exactly_once(client, app):
    ids = _runs_with_series(client, app, 8, points=8)
    args = {"mode": "series", "run_ids": ids, "keys": ["loss"], "token_budget": 512}
    rows, pages = _walk(_server(client), "metrics", args, "series")
    assert [row["run_id"] for row in rows] == ids
    assert len(pages) > 1
    for page in pages[:-1]:
        assert MissingMarker.TRUNCATED_BY_TOKEN_BUDGET in page["completeness"]["missing"]
        # Whole series only: a cut page is never a fragment of one.
        assert "format" not in page["data"]
    assert "completeness" not in pages[-1]


def test_series_read_failures_and_the_point_ceiling_are_reported(client, app):
    [rid] = _runs_with_series(client, app, 1)
    app.series_result_extra = {
        "truncated": True,
        "errors": [
            {"run_id": rid, "source": "wandb", "code": "source_unavailable", "message": "W&B down"}
        ],
    }
    out = _call(_server(client), "metrics", {"mode": "series", "run_ids": [rid], "keys": ["loss"]})
    assert out["completeness"]["state"] == "partial"
    assert set(out["completeness"]["missing"]) == {
        MissingMarker.METRIC_POINTS_BEYOND_BACKEND_LIMIT,
        MissingMarker.SERIES_READ_ERRORS,
    }
    assert out["data"]["errors"][0]["message"] == "W&B down"


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ({"run_id": "r"}, "does not read run_id"),
        ({"key": "loss"}, "does not read key"),
        ({"by": ["rank"]}, "does not read by"),
    ],
)
def test_series_refuses_the_single_run_arguments(client, app, args, expected):
    message = _error(
        _server(client),
        "metrics",
        {"mode": "series", "run_ids": [str(uuid.uuid4())], "keys": ["loss"], **args},
    )
    assert expected in message
    assert not app.series_queries


def test_series_requires_both_lists(client, app):
    message = _error(_server(client), "metrics", {"mode": "series", "run_ids": [str(uuid.uuid4())]})
    assert "requires keys" in message
    message = _error(_server(client), "metrics", {"mode": "series", "keys": ["loss"]})
    assert "requires run_ids" in message


def test_the_single_run_grains_still_require_run_id(client, app):
    message = _error(_server(client), "metrics", {"mode": "coordinates"})
    assert "requires run_id" in message


def test_series_refuses_a_slug_with_how_to_get_the_id(client, app):
    message = _error(
        _server(client),
        "metrics",
        {"mode": "series", "run_ids": ["tunneling-sambar-254"], "keys": ["loss"]},
    )
    assert "takes run UUIDs" in message and 'entity(refs=["run:<slug>"])' in message
    assert not app.series_queries


def test_series_list_bounds_are_the_routes_own(client, app):
    with pytest.raises(ToolError, match="run_ids takes 1 to 50 entries"):
        server_mod._metric_args_for_mode(
            MetricMode.SERIES, {"run_ids": [str(i) for i in range(51)], "keys": ["loss"]}
        )
    with pytest.raises(ToolError, match="must be a list of strings"):
        server_mod._metric_args_for_mode(MetricMode.SERIES, {"run_ids": "abc", "keys": ["loss"]})


@pytest.mark.parametrize("points", range(2, 16, 3))
def test_a_series_page_is_sized_for_the_cursor_delivery_puts_on_it(client, app, points):
    """The service fits whole series to the budget BEFORE delivery swaps its
    short native cursor for a longer bound one (which also carries the read's
    identity hash). Sized without that, a page that fits by a few tokens
    overflows once the real cursor lands and goes out as a JSON fragment."""
    ids = _runs_with_series(client, app, 5, points=points)
    args = {"mode": "series", "run_ids": ids, "keys": ["loss"], "token_budget": 512}
    rows, pages = _walk(_server(client), "metrics", args, "series")
    assert [row["run_id"] for row in rows] == ids
    assert all("format" not in page["data"] for page in pages)


def test_a_series_too_big_for_the_budget_is_refused_with_the_budget_it_needs(client, app):
    """A series is never split across responses: on a still-logging run the
    re-read for its second half is a DIFFERENT series (more points, other
    picks), so fragments could not be joined and the read failed mid-way.
    The refusal names the budget that carries it whole; re-asking with it works
    even though the run logged more in between."""
    rid = str(uuid.uuid4())
    app.seed_series(rid, "loss", {s: float((s * 37) % 101) for s in range(400)})
    server = _server(client)
    args = {"mode": "series", "run_ids": [rid], "keys": ["loss"], "token_budget": 512}
    refused = _call(server, "metrics", args)
    assert refused["data"]["series"] == []
    assert refused["completeness"]["missing"] == [MissingMarker.FIRST_RESULT_EXCEEDS_BUDGET]
    needed = refused["data"]["min_token_budget"]
    assert 512 < needed <= 8000 and "next_cursor" not in refused
    # Rounded up past the measured cost, like every other budget hint.
    assert needed % 100 == 0 and needed >= refused["data"]["next_series_tokens"] * 1.1
    # The run keeps logging.
    app.series_points[rid][0]["points"].extend(
        {"step_index": s, "value": float(s % 7), "wall_clock": "2026-07-27T00:00:00Z"}
        for s in range(400, 420)
    )
    whole = _call(server, "metrics", {**args, "token_budget": needed})
    [row] = whole["data"]["series"]
    assert 90 < row["point_count"] <= 100 and "completeness" not in whole


@pytest.mark.parametrize("seed", range(12))
def test_the_budget_hint_holds_when_a_noisy_run_logs_before_the_retry(client, app, seed):
    """Review of 2980f4e74, reproduced: a refusal's `min_token_budget` was the
    exact measured cost, and on a still-logging run with noisy values the
    retry at that budget was refused again in 7 of 12 seeds."""
    import random

    noise = random.Random(seed)
    rid = str(uuid.uuid4())
    app.seed_series(
        rid, "loss", {s: noise.random() * noise.choice((1, 1e-3, 1e4)) for s in range(400)}
    )
    server = _server(client)
    args = {"mode": "series", "run_ids": [rid], "keys": ["loss"], "token_budget": 512}
    hint = _call(server, "metrics", args)["data"]["min_token_budget"]
    app.series_points[rid][0]["points"].extend(
        {
            "step_index": s,
            "value": noise.random() * noise.choice((1, 1e-3, 1e4)),
            "wall_clock": "2026-07-27T00:00:00Z",
        }
        for s in range(400, 400 + noise.randint(1, 60))
    )
    whole = _call(server, "metrics", {**args, "token_budget": hint})
    assert len(whole["data"]["series"]) == 1, whole["data"]


def test_a_series_too_big_for_any_budget_names_the_max_points_that_fits(client, app):
    rid = str(uuid.uuid4())
    app.seed_series(rid, "loss", {s: float((s * 37) % 1001) / 3 for s in range(5000)})
    refused = _call(
        _server(client),
        "metrics",
        {"mode": "series", "run_ids": [rid], "keys": ["loss"], "max_points": 5000},
    )
    fits = refused["data"]["fits_max_points"]
    assert 2 <= fits < 5000 and "min_token_budget" not in refused["data"]
    whole = _call(
        _server(client),
        "metrics",
        {
            "mode": "series",
            "run_ids": [rid],
            "keys": ["loss"],
            "max_points": fits,
            "token_budget": 8000,
        },
    )
    assert len(whole["data"]["series"]) == 1


def test_a_series_read_whose_series_change_between_pages_says_restart(client, app):
    """Each page re-runs the query and its cursor is an index into the rows.
    A series that vanishes between pages -- a W&B read that fails on page 2 --
    shifted that index and skipped a series with nothing saying so."""
    ids = _runs_with_series(client, app, 6, points=8)
    server = _server(client)
    args = {"mode": "series", "run_ids": ids, "keys": ["loss"], "token_budget": 512}
    first = _call(server, "metrics", args)
    assert first["next_cursor"]
    app.series_points.pop(ids[0])  # the provider read failed this time
    app.series_result_extra = {
        "errors": [
            {"run_id": ids[0], "source": "wandb", "code": "source_unavailable", "message": "down"}
        ]
    }
    message = _error(server, "metrics", {**args, "cursor": first["next_cursor"]})
    assert "source_changed" in message and "restart" in message


def test_a_still_logging_run_pages_its_series_without_a_restart(client, app):
    """Points are not part of a series' identity: a run that logs between two
    pages changes what the next page shows, never which series it is."""
    ids = _runs_with_series(client, app, 6, points=8)
    server = _server(client)
    args = {"mode": "series", "run_ids": ids, "keys": ["loss"], "token_budget": 512}
    page = _call(server, "metrics", args)
    seen = [row["run_id"] for row in page["data"]["series"]]
    while page.get("next_cursor"):
        for rid in ids:
            app.series_points[rid][0]["points"].append(
                {"step_index": 99, "value": 0.1, "wall_clock": "2026-07-27T00:00:00Z"}
            )
        page = _call(server, "metrics", {**args, "cursor": page["next_cursor"]})
        seen += [row["run_id"] for row in page["data"]["series"]]
    assert seen == ids


def test_one_unencodable_path_does_not_fail_a_whole_diff_read(client, app):
    """A page whose cursor (the last row's path) is too long to encode cannot
    end there; the read must still deliver a page that ends elsewhere. The long
    path sits where the page-size search probes first (row 100 of 200)."""
    import random as _random
    import string as _string

    rid = _run(client, app)
    rnd = _random.Random(2)
    huge = "p098z" + "".join(rnd.choice(_string.ascii_letters + _string.digits) for _ in range(3400)) + ".py"
    paths = sorted([f"p{i:03d}.py" for i in range(260)] + [huge])
    assert paths.index(huge) == 99
    app.sandbox_diffs[(rid, "t-1")] = {
        "entries": [{"path": p, "status": "modified", "type": "f"} for p in paths],
        "counts": _COUNTS,
    }
    out = _call(
        _server(client),
        "entity",
        {"refs": [f"run:{rid}"], "view": "diff", "view_options": {"trial": "t-1"}, "token_budget": 8000},
    )
    assert out["data"]["entries"], out
    assert out.get("next_cursor"), "the rest of the diff must stay reachable"


def test_a_workspace_walk_ends_when_the_route_sorts_differently(client, app):
    """Delta review of 2200a6960: on a database that is not datcollate=C (a
    stock en_US postgres) the route's order differs from the resume key, and
    resuming in the route's order handed back the same page forever."""
    app.workspaces.clear()
    for name in ("ab", "a-c", "a-d"):
        wid = str(uuid.uuid4())
        app.workspaces[wid] = {
            "id": wid,
            "customer_id": "lab-42",
            "name": name,
            "slug": name,
            "kind": "team",
            "created_at": "2026-09-30T00:00:00Z",
        }
    # en_US-like: punctuation ignored, so ab < a-c < a-d.
    app.workspace_sort = lambda w: (w["name"].replace("-", ""), w["id"])
    rows, _ = _walk(_server(client), "browse", {"mode": "workspaces", "limit": 2}, "workspaces", max_pages=6)
    assert sorted(row["name"] for row in rows) == ["a-c", "a-d", "ab"]
