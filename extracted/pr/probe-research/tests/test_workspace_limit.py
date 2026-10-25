"""This computer's workspace limit: set, stored, sent, forwarded, refused, explained.

A client-side LIMITER (`probe.sdk.workspace_limit`): the computer stores "limit
to workspace W" beside its filing pin and every request it makes carries
`X-Probe-Workspace-Limit` (+ `-Team-Items`); the API narrows that request's reads.
These pin the client half: what sets it (`probe workspace limit`, the service
action, the desktop op), what sends it (the SDK transport, the hosted MCP's
forward, the static MCP copies), what it refuses (pin moves, the daemon), and
what it says when it hid something. Real boundaries: the HTTP wire (an
`httpx.MockTransport`), the config file, the CLI's exit status and output.
"""

from __future__ import annotations

import asyncio
import json
import tempfile
from pathlib import Path

import httpx
import pytest

from probe import cli
from probe.sdk import errors, workspace_limit as wl
from probe.sdk.client import Client
from probe.sdk.config import Settings, load_context, resolve, save_context
from probe.sdk.journal import Journal
from probe.sdk.transport import Transport

from tests.conftest import _WS_MINE, _WS_OTHER, make_client

LIMIT = wl.LIMIT_HEADER.lower()
ITEMS = wl.TEAM_ITEMS_HEADER.lower()


def _limit_this_computer(workspace: str = _WS_MINE, **extra) -> None:
    save_context(
        {
            "base_url": "http://test",
            "token": "probe_pat_test",
            "workspace": {"id": workspace, "project": None, "limit": True, "name": "Mine", "slug": "mine", **extra},
        }
    )


class Wire:
    """A Probe that records every request and answers from `routes`."""

    def __init__(self, routes: dict | None = None) -> None:
        self.seen: list[httpx.Request] = []
        self.routes = routes or {}

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.seen.append(request)
        answer = self.routes.get((request.method, request.url.path))
        if callable(answer):
            return answer(request)
        if answer is not None:
            status, body, *headers = answer
            return httpx.Response(status, json=body, headers=headers[0] if headers else None)
        if request.url.path == "/v1/workspaces":
            return httpx.Response(200, json=[{"id": _WS_MINE, "slug": "mine", "name": "Mine", "kind": "team"},
                                             {"id": _WS_OTHER, "slug": "teammate", "name": "Teammate", "kind": "team"}])
        return httpx.Response(200, json={})

    def transport(self, settings: Settings) -> Transport:
        return Transport(settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(self.handler)))

    def limits(self) -> list[tuple[str, str | None, str | None]]:
        return [(r.url.path, r.headers.get(LIMIT), r.headers.get(ITEMS)) for r in self.seen]


# -- the SDK transport: what every CLI, SDK and daemon request carries ----------


def test_a_limited_computer_sends_both_headers_on_every_request():
    _limit_this_computer(team_items="hide")
    wire = Wire()
    transport = wire.transport(resolve())

    transport.get("/v1/runs")
    transport.post("/v1/projects", {"slug": "p", "kind": "general"})

    assert wire.limits() == [("/v1/runs", _WS_MINE, "hide"), ("/v1/projects", _WS_MINE, "hide")]


@pytest.mark.parametrize("workspace", [None, {"id": _WS_MINE}, {"id": _WS_MINE, "limit": False}])
def test_the_whole_team_sends_no_limit(workspace):
    """No pin, the pin alone, or `limit: false`: the whole team, no header."""
    save_context({"base_url": "http://test", "token": "probe_pat_test", "workspace": workspace})
    wire = Wire()
    assert resolve().workspace_limit is None
    wire.transport(resolve()).get("/v1/runs")
    assert wire.limits() == [("/v1/runs", None, None)]


def test_capture_uploads_never_carry_the_limit():
    """`/ingest` is capture: not limited."""
    _limit_this_computer()
    settings = resolve()
    settings.ingest_token = "ros_ing_test"
    wire = Wire()
    wire.transport(settings).post("/ingest/v1/sessions", {})
    assert wire.limits() == [("/ingest/v1/sessions", None, None)]


def test_the_pickers_list_is_never_limited():
    _limit_this_computer()
    wire = Wire()
    transport = wire.transport(resolve())
    with wl.without_limit():
        transport.get("/v1/workspaces")
    transport.get("/v1/workspaces")
    assert wire.limits() == [("/v1/workspaces", None, None), ("/v1/workspaces", _WS_MINE, "show")]


def test_an_environment_slug_is_looked_up_once_without_the_limit(monkeypatch):
    monkeypatch.setattr(wl, "_RESOLVED", {})
    monkeypatch.setenv(wl.LIMIT_ENV, "teammate")
    save_context({"base_url": "http://test", "token": "probe_pat_test"})
    wire = Wire()
    transport = wire.transport(resolve())

    transport.get("/v1/runs")
    transport.get("/v1/runs")

    assert wire.limits() == [
        ("/v1/workspaces", None, None),
        ("/v1/runs", _WS_OTHER, "show"),
        ("/v1/runs", _WS_OTHER, "show"),
    ]


def test_an_unknown_environment_slug_refuses_rather_than_widening(monkeypatch):
    monkeypatch.setattr(wl, "_RESOLVED", {})
    monkeypatch.setenv(wl.LIMIT_ENV, "nope")
    save_context({"base_url": "http://test", "token": "probe_pat_test"})
    wire = Wire()

    with pytest.raises(errors.WorkspaceLimitUnknown, match="PROBE_WORKSPACE_LIMIT='nope'"):
        wire.transport(resolve()).get("/v1/runs")
    assert [path for path, *_ in wire.limits()] == ["/v1/workspaces"]  # nothing sent unlimited


def test_team_in_the_environment_lifts_the_stored_limit_and_items_override_it(monkeypatch):
    _limit_this_computer(team_items="hide")
    monkeypatch.setenv(wl.LIMIT_ENV, "team")
    assert resolve().workspace_limit is None
    monkeypatch.delenv(wl.LIMIT_ENV)
    monkeypatch.setenv(wl.TEAM_ITEMS_ENV, "show")
    wire = Wire()
    wire.transport(resolve()).get("/v1/runs")
    assert wire.limits() == [("/v1/runs", _WS_MINE, "show")]


def test_a_team_items_value_that_is_not_show_or_hide_refuses(monkeypatch):
    _limit_this_computer()
    monkeypatch.setenv(wl.TEAM_ITEMS_ENV, "maybe")
    with pytest.raises(errors.InvalidWorkspaceLimit, match="PROBE_WORKSPACE_LIMIT_TEAM_ITEMS='maybe'"):
        Wire().transport(resolve()).get("/v1/runs")


def test_an_environment_limit_files_new_projects_into_its_workspace(monkeypatch):
    """A job limited by PROBE_WORKSPACE_LIMIT must not file work it then cannot see."""
    save_context({"base_url": "http://test", "token": "probe_pat_test", "workspace": {"id": _WS_OTHER}})
    monkeypatch.setenv(wl.LIMIT_ENV, _WS_MINE)
    assert resolve().workspace == _WS_MINE
    monkeypatch.setenv("PROBE_WORKSPACE", _WS_OTHER)
    assert resolve().workspace == _WS_OTHER  # an explicit filing choice still wins


def test_settings_built_by_hand_carry_no_limit():
    """Sign-in, key checks and logout build their own Settings: a stale limit must
    never stop a person fixing it."""
    _limit_this_computer()
    assert Settings(base_url="http://test", token="t").workspace_limit is None
    assert resolve().workspace_limit is not None


def test_the_hosted_forward_overrides_this_processes_own():
    """The hosted MCP binds the CALLER's headers per request; `{}` (they sent none)
    must never fall back to the process's own."""
    _limit_this_computer()
    wire = Wire()
    transport = wire.transport(resolve())
    with wl.forwarded_scope({wl.LIMIT_HEADER: _WS_OTHER, wl.TEAM_ITEMS_HEADER: "hide"}):
        transport.get("/v1/runs")
    with wl.forwarded_scope({}):
        transport.get("/v1/runs")
    assert wire.limits() == [("/v1/runs", _WS_OTHER, "hide"), ("/v1/runs", None, None)]


# -- what the client says when the limit hid something -------------------------


def test_a_limited_404_says_the_limit_hid_it():
    _limit_this_computer()
    wire = Wire({("GET", "/v1/runs/r1"): (404, {"detail": "run not found"}, {wl.APPLIED_HEADER: _WS_MINE})})
    with pytest.raises(errors.NotFoundError) as caught:
        wire.transport(resolve()).get("/v1/runs/r1")
    assert str(caught.value) == "run not found (hidden by this computer's workspace limit: Mine)"
    assert caught.value.workspace_limit_applied == _WS_MINE


def test_a_404_the_api_did_not_limit_is_unchanged():
    wire = Wire({("GET", "/v1/runs/r1"): (404, {"detail": "run not found"})})
    with pytest.raises(errors.NotFoundError) as caught:
        wire.transport(Settings(base_url="http://test", token="t")).get("/v1/runs/r1")
    assert str(caught.value) == "run not found" and caught.value.workspace_limit_applied is None


@pytest.mark.parametrize(
    "status,code,kind",
    [(422, errors.WORKSPACE_LIMIT_UNKNOWN, errors.WorkspaceLimitUnknown),
     (400, errors.INVALID_WORKSPACE_LIMIT, errors.InvalidWorkspaceLimit)],
)
def test_a_refused_limit_names_the_fix(status, code, kind):
    exc = errors.error_for(status, {"code": code, "message": "This computer's limit is gone."})
    assert isinstance(exc, kind) and isinstance(exc, errors.ValidationError)
    assert "probe workspace limit --team" in str(exc)
    # The server's own sentence already names it: not said twice.
    server = errors.error_for(status, {"code": code, "message": "Run `probe workspace limit --team` or pick another."})
    assert str(server).count("probe workspace limit") == 1


def test_the_outbox_keeps_a_limit_refusal_queued():
    """Every queued write fails the same way until the limit is fixed: transient,
    never dead-lettered one by one."""
    from probe.sdk.journal import classify

    assert classify(errors.error_for(422, {"code": errors.WORKSPACE_LIMIT_UNKNOWN, "message": "x"})) == "transient"
    assert classify(errors.error_for(422, {"detail": "a real validation error"})) == "permanent"


def _client_for(wire: Wire, settings: Settings) -> Client:
    return Client(settings=settings, transport=wire.transport(settings), async_writes=False, fail_open=False,
                  journal=Journal(tempfile.mkdtemp(prefix="probe-test-journal-"),
                                  context={"name": None, "base_url": settings.base_url}))


def test_init_names_the_limit_when_the_slug_is_taken_outside_it():
    """`probe.init(project=...)`: the slug lookup finds nothing (hidden) and the
    create answers 409 (the slug is tenant-wide)."""
    _limit_this_computer()
    conflict = (409, {"detail": {"message": "slug taken", "existing_id": None}})
    wire = Wire({("GET", "/v1/projects"): (200, []), ("POST", "/v1/projects"): conflict})
    with pytest.raises(errors.ConflictError, match="exists outside this computer's workspace limit Mine"):
        _client_for(wire, resolve()).ensure_project("their-project")


def test_init_without_a_limit_keeps_the_plain_conflict():
    conflict = (409, {"detail": {"message": "slug taken", "existing_id": None}})
    wire = Wire({("GET", "/v1/projects"): (200, []), ("POST", "/v1/projects"): conflict})
    settings = Settings(base_url="http://test", token="t", workspace=_WS_MINE)
    with pytest.raises(errors.ConflictError) as caught:
        _client_for(wire, settings).ensure_project("their-project")
    assert "workspace limit" not in str(caught.value)


def test_a_missing_project_under_a_limit_says_it_may_be_elsewhere():
    _limit_this_computer()
    wire = Wire({("GET", "/v1/projects"): (200, [])})
    with pytest.raises(errors.NotFoundError, match="this computer's workspace limit is Mine: it may be in another"):
        _client_for(wire, resolve()).resolve_or_raise("project", "elsewhere")


# -- `probe workspace limit` ----------------------------------------------------


@pytest.fixture
def limited_cli(app, monkeypatch, tmp_path):
    """The CLI against the fake API, its client carrying the config's limit as
    `resolve()` would."""

    def factory(**_kw):
        client = make_client(app, tmp_spool=tmp_path / "spool")
        client.settings.workspace_limit = resolve().workspace_limit
        return client

    monkeypatch.setattr(cli, "Client", factory)
    save_context({"base_url": "http://test", "token": "probe_pat_test", "workspace": {"id": _WS_OTHER, "project": "p"}})
    return app


def _run(capsys, *argv: str) -> tuple[int, str, str]:
    code = cli.main(list(argv))
    out = capsys.readouterr()
    return code, out.out, out.err


def test_setting_a_limit_resolves_it_without_the_limit_and_moves_the_pin(limited_cli, capsys):
    _limit_this_computer(_WS_OTHER, name="Teammate", slug="teammate")  # limited elsewhere already
    code, out, _ = _run(capsys, "workspace", "limit", "mine", "--team-items", "hide", "--json")

    assert code == 0
    assert json.loads(out) == {
        "ok": True,
        "workspace_limit": {"id": _WS_MINE, "name": "Mine", "slug": "mine", "team_items": "hide"},
    }
    assert load_context()["workspace"] == {
        "id": _WS_MINE, "project": None, "limit": True, "team_items": "hide", "name": "Mine", "slug": "mine",
    }
    lists = [r for r in limited_cli.requests if r.url.path == "/v1/workspaces"]
    assert lists and all(r.headers.get(LIMIT) is None for r in lists)


@pytest.mark.parametrize("ref", [_WS_MINE, f"id:{_WS_MINE}", "mine", "slug:mine", "MINE"])
def test_a_workspace_is_named_by_id_slug_or_name(limited_cli, capsys, ref):
    code, out, _ = _run(capsys, "workspace", "limit", ref, "--json")
    assert code == 0 and json.loads(out)["workspace_limit"]["id"] == _WS_MINE


def test_the_human_output_names_the_workspace_and_what_is_hidden(limited_cli, capsys):
    code, out, _ = _run(capsys, "workspace", "limit", "teammate", "--team-items", "hide", "--yes")
    assert code == 0
    assert "limited to workspace Teammate (teammate)" in out
    assert "every other workspace is hidden" in out
    assert "team-wide items (the team note, the All workspaces summary, GitHub docs) are hidden" in out
    assert "the shared folder and datasets stay visible" in out


def test_team_clears_the_limit_and_keeps_the_pin(limited_cli, capsys):
    _limit_this_computer(team_items="hide")
    code, out, _ = _run(capsys, "workspace", "limit", "--team", "--json")
    assert (code, json.loads(out)) == (0, {"ok": True, "workspace_limit": None})
    assert load_context()["workspace"] == {"id": _WS_MINE, "project": None}


def test_no_arguments_shows_the_current_limit_without_the_network(limited_cli, capsys):
    _limit_this_computer()
    before = len(limited_cli.requests)
    code, out, _ = _run(capsys, "workspace", "limit", "--json")
    assert json.loads(out)["workspace_limit"] == {"id": _WS_MINE, "name": "Mine", "slug": "mine", "team_items": "show"}
    assert code == 0 and len(limited_cli.requests) == before
    code, out, _ = _run(capsys, "workspace", "limit")
    assert "limited to workspace Mine (mine)" in out


def test_team_items_alone_changes_only_them(limited_cli, capsys):
    _limit_this_computer()
    code, out, _ = _run(capsys, "workspace", "limit", "--team-items", "hide", "--json")
    assert code == 0 and json.loads(out)["workspace_limit"]["team_items"] == "hide"
    assert load_context()["workspace"]["id"] == _WS_MINE


@pytest.mark.parametrize(
    "argv,code,error",
    [
        (["nope"], 1, "workspace_not_found"),
        (["mine", "--team"], 2, "usage"),
        (["--team", "--team-items", "hide"], 2, "usage"),
        (["mine", "--team-items", "maybe"], 2, "usage"),
        (["--team-items", "hide"], 2, "usage"),  # not limited: nothing to change
    ],
)
def test_a_refusal_is_one_json_object_and_changes_nothing(limited_cli, capsys, argv, code, error):
    before = load_context()
    got, out, _ = _run(capsys, "workspace", "limit", *argv, "--json")
    body = json.loads(out)
    assert (got, body["ok"], body["code"]) == (code, False, error) and body["message"]
    assert load_context() == before


def test_an_ambiguous_name_asks_for_the_slug(limited_cli, capsys):
    for ws in (_WS_MINE, _WS_OTHER):
        limited_cli.workspaces[ws]["name"] = "Lab"
    code, out, _ = _run(capsys, "workspace", "limit", "lab", "--json")
    body = json.loads(out)
    assert (code, body["code"]) == (1, "workspace_ambiguous") and "Pass its slug" in body["message"]
    code, out, _ = _run(capsys, "workspace", "limit", "teammate", "--json")  # the slug decides
    assert (code, json.loads(out)["workspace_limit"]["id"]) == (0, _WS_OTHER)


def test_not_signed_in_is_refused(app, monkeypatch, capsys):
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(app))
    code, out, _ = _run(capsys, "workspace", "limit", "mine", "--json")
    assert (code, json.loads(out)["code"]) == (1, "not_signed_in")


# -- the pin may not move off a limited workspace (D-g) --------------------------


@pytest.mark.parametrize(
    "argv",
    [["workspace", "use", "teammate"], ["workspace", "use", "--clear"], ["workspace", "create", "new-one", "--use"]],
)
def test_pin_moves_are_refused_while_limited(limited_cli, capsys, argv):
    _limit_this_computer()
    before = load_context()["workspace"]
    code, _, err = _run(capsys, *argv)
    assert code == 1 and "probe workspace limit" in err
    assert load_context()["workspace"] == before
    assert not any(r.method == "POST" and r.url.path == "/v1/workspaces" for r in limited_cli.requests)


def test_using_the_limited_workspace_keeps_the_limit(limited_cli, capsys):
    _limit_this_computer(team_items="hide")
    code, _, _ = _run(capsys, "workspace", "use", "mine")
    assert code == 0
    anchor = load_context()["workspace"]
    assert (anchor["id"], anchor["limit"], anchor["team_items"]) == (_WS_MINE, True, "hide")


def test_project_use_refuses_a_project_of_another_workspace(limited_cli, capsys, tmp_path):
    other = make_client(limited_cli, tmp_spool=tmp_path / "other").create_project(
        "theirs", kind="general", workspace_id=_WS_OTHER)
    mine = make_client(limited_cli, tmp_spool=tmp_path / "mine").create_project(
        "ours", kind="general", workspace_id=_WS_MINE)
    _limit_this_computer()

    code, _, err = _run(capsys, "project", "use", f"id:{other['id']}")
    assert code == 1 and "limited to workspace Mine" in err
    code, _, _ = _run(capsys, "project", "use", f"id:{mine['id']}")
    assert code == 0
    anchor = load_context()["workspace"]
    assert (anchor["project"], anchor["limit"]) == (f"id:{mine['id']}", True)


def test_deleting_the_limited_workspace_lifts_the_limit(limited_cli, capsys):
    limited_cli.workspaces[_WS_MINE]["project_count"] = 0
    _limit_this_computer()
    code, _, err = _run(capsys, "workspace", "delete", "mine", "--yes")
    # A limit naming a deleted workspace would refuse every request: it goes with the pin.
    assert code == 0, err
    assert load_context().get("workspace") is None
    assert "sees the whole team again" in err


def test_context_show_resolves_the_limit(limited_cli, capsys):
    _limit_this_computer()
    code, out, _ = _run(capsys, "context", "show")
    assert code == 0 and json.loads(out)["resolved"]["workspace_limit"]["id"] == _WS_MINE


def test_a_slug_lookup_miss_under_a_limit_says_it_may_be_elsewhere(limited_cli, capsys):
    _limit_this_computer()
    code, _, err = _run(capsys, "workspace", "get", "nowhere")
    assert code == 2 and "it may be in another workspace" in err


# -- the daemon may not change it (D-d) -------------------------------------------


@pytest.mark.parametrize("argv", [["workspace", "limit", "mine", "--yes"], ["workspace", "limit", "--team"],
                                  ["workspace", "limit"]])
def test_the_daemon_is_refused_workspace_limit(tmp_path, argv):
    from probe.daemon import precheck

    assert precheck.OWNERS["workspace limit"] == precheck.RESEARCHER
    block = precheck.check(precheck.parse(argv), cwd=tmp_path)
    assert block is not None and "isn't the daemon's to run" in block.why


# -- `probe mcp headers` --------------------------------------------------------


def test_mcp_headers_carry_the_limit(capsys):
    save_context({"mcp_token": "probe_pat_read", "workspace": {"id": _WS_MINE, "limit": True, "team_items": "hide"}})
    code, out, _ = _run(capsys, "mcp", "headers")
    assert code == 0
    assert json.loads(out) == {"Authorization": "Bearer probe_pat_read", wl.LIMIT_HEADER: _WS_MINE,
                               wl.TEAM_ITEMS_HEADER: "hide"}


def test_mcp_headers_fail_closed_when_a_slug_cannot_be_looked_up(capsys, monkeypatch):
    """Offline, an environment slug cannot become a uuid: it is sent as found (the
    API refuses it), never dropped -- and the helper still authenticates."""
    monkeypatch.setattr(wl, "_RESOLVED", {})
    monkeypatch.setenv(wl.LIMIT_ENV, "eng")
    monkeypatch.setenv("PROBE_BASE_URL", "http://127.0.0.1:9")
    save_context({"mcp_token": "probe_pat_read"})
    code, out, err = _run(capsys, "mcp", "headers")
    assert code == 0 and "warning:" in err
    assert json.loads(out) == {"Authorization": "Bearer probe_pat_read", wl.LIMIT_HEADER: "eng",
                               wl.TEAM_ITEMS_HEADER: "show"}


# -- the team note: hidden team items take it out, showing them brings it back ----


@pytest.fixture
def instruction(monkeypatch, tmp_path):
    """Claude Code's CLAUDE.md with Probe's pointer block, and the note's paths here."""
    from probe.cli import agent_rules

    claude = tmp_path / "claude"
    claude.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    path = agent_rules.memory_path("claude_code")
    agent_rules.install(path)
    return path


def _note_block(path: Path) -> bool:
    from probe.cli import agent_rules

    return agent_rules.has_block(path, agent_rules.NOTE_BLOCK)


def test_hidden_team_items_take_the_note_block_out_and_keep_the_pointer(instruction):
    from probe.cli import agent_rules, team_note_file

    save_context({"base_url": "http://test", "token": "probe_pat_test"})
    team_note_file.render_blocks("## Conventions\n\nUse worktrees.\n", settings=resolve(), sources=("claude_code",))
    assert _note_block(instruction)

    _limit_this_computer(team_items="hide")
    report = team_note_file.render_blocks("## Conventions\n\nUse worktrees.\n", settings=resolve(),
                                          sources=("claude_code",))
    assert report.hidden == ("claude_code",) and report.ok
    assert not _note_block(instruction) and agent_rules.has_block(instruction, agent_rules.POINTER_BLOCK)

    _limit_this_computer(team_items="show")
    report = team_note_file.render_blocks("## Conventions\n\nUse worktrees.\n", settings=resolve(),
                                          sources=("claude_code",))
    assert report.written == ("claude_code",) and _note_block(instruction)


def test_notes_sync_sends_and_fetches_nothing_while_team_items_are_hidden(instruction, capsys, monkeypatch):
    from probe.cli import team_note_file

    save_context({"base_url": "http://test", "token": "probe_pat_test"})
    team_note_file.render_blocks("## A note\n", settings=resolve(), sources=("claude_code",))
    _limit_this_computer(team_items="hide")
    monkeypatch.setattr(team_note_file, "RENDER_SOURCES", ("claude_code",))
    monkeypatch.setattr(cli, "Client", lambda **kw: pytest.fail("no client: nothing is synced"))

    code, out, _ = _run(capsys, "notes", "sync")
    body = json.loads(out)
    assert code == 0 and body["detail"] == team_note_file.HIDDEN_DETAIL
    assert body["render_hidden_by_limit"] == ["claude_code"] and not _note_block(instruction)
    assert team_note_file.advisory_for_source("claude_code", settings=resolve()) == ""


# -- the static MCP copies follow a change (as a token rotation does) -------------


def test_codex_follows_a_limit_change(monkeypatch, tmp_path):
    from probe._compat import tomllib
    from probe.cli import codex_config, plugin_cli, setup

    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    save_context({"base_url": "https://api.research.prbe.ai", "mcp_token": "probe_pat_read"})
    url = "https://mcp.research.prbe.ai/mcp"
    codex_config.write_mcp_bearer(setup.CODEX_MCP_NAME, url=url, token="probe_pat_read")
    monkeypatch.setattr(setup, "daemon_records", lambda _source: False)
    monkeypatch.setattr(codex_config, "plugin_mcp_url", lambda *_a, **_k: url)
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: codex_config.BEARER_STATUS)
    assert setup.codex_mcp_token_drifted() is False

    def table() -> dict:
        text = codex_config.config_path().read_text(encoding="utf-8")
        return tomllib.loads(text)["mcp_servers"][setup.CODEX_MCP_NAME]["http_headers"]

    _limit_this_computer(team_items="hide")
    save_context({"base_url": "https://api.research.prbe.ai", "mcp_token": "probe_pat_read"})
    assert setup.codex_mcp_token_drifted() is True
    assert setup.sync_codex_mcp_token() == ["Codex MCP updated to this computer's workspace limit (restart Codex to load it)."]
    assert wl.limit_headers_of(table()) == {wl.LIMIT_HEADER: _WS_MINE, wl.TEAM_ITEMS_HEADER: "hide"}
    assert table()["Authorization"] == "Bearer probe_pat_read"
    assert setup.sync_codex_mcp_token() == []

    from probe.cli import workspace_limit_cmd

    workspace_limit_cmd.apply(None, team=True)  # `probe workspace limit --team` re-renders it
    assert wl.limit_headers_of(table()) == {}


# -- the hosted MCP forwards the caller's limit -----------------------------------


def _asgi(app, headers: list) -> dict:
    out: dict = {}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]

    scope = {"type": "http", "method": "POST", "path": "/mcp", "headers": headers}
    asyncio.run(app(scope, receive, send))
    return out


@pytest.mark.parametrize(
    "sent,forwarded",
    [
        ([(b"x-probe-workspace-limit", _WS_OTHER.encode()), (b"x-probe-workspace-limit-team-items", b"hide")],
         (_WS_OTHER, "hide")),
        ([], (None, None)),  # the caller sent none: the pod's own never stands in
        ([(b"x-probe-workspace-limit", b"bad\xffvalue")], (wl.UNREADABLE_FORWARD, None)),  # refused upstream
    ],
)
def test_the_hosted_mcp_forwards_the_callers_limit_on_its_api_calls(monkeypatch, sent, forwarded):
    from probe.mcp import server

    _limit_this_computer()  # the POD's own config: must never leak into a caller's request
    wire = Wire()
    transport = wire.transport(resolve())
    identities: list = []

    async def inner(scope, receive, send):
        transport.get("/v1/runs")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"{}"})

    async def accepts(_token):
        return False

    monkeypatch.setattr(server, "identity_for_token", lambda _t: {"distinct_id": "u1", "workspace_id": None})
    monkeypatch.setattr(server.accounting, "emit", lambda acct, identity: identities.append(identity))
    app = server.with_auth_and_health(inner, mcp_path="/mcp", token_rejected=accepts)

    assert _asgi(app, [(b"authorization", b"Bearer probe_pat_read"), *sent])["status"] == 200
    assert wire.limits() == [("/v1/runs", *forwarded)]
    assert identities[0]["workspace_id"] == (_WS_OTHER if forwarded[0] == _WS_OTHER else None)


def test_a_tool_error_under_the_callers_limit_says_so_whatever_wraps_it():
    from probe.mcp import server

    hidden = errors.NotFoundError("no run r1")
    hidden.workspace_limit_applied = _WS_OTHER
    try:
        try:
            raise hidden
        except errors.NotFoundError as exc:
            raise RuntimeError("Error executing tool entity: " + "x" * 900) from exc
    except RuntimeError as wrapped:
        text = server._bounded_error_text(wrapped)
    assert len(text) <= 600 and text.endswith(f"(hidden by this computer's workspace limit: workspace {_WS_OTHER})")


# -- the desktop app's picker and the Probe service's action ----------------------


def test_the_desktop_workspaces_op_lists_every_workspace_without_the_limit(limited_cli, monkeypatch):
    from probe.cli import desktop

    _limit_this_computer(team_items="hide")
    monkeypatch.setattr(desktop, "_client", lambda: cli.Client())
    text, code = desktop.respond(json.dumps({"op": "workspaces"}).encode())
    body = json.loads(text)
    assert (code, body["ok"]) == (0, True)
    assert body["data"] == {
        "workspaces": [
            {"id": _WS_MINE, "name": "Mine", "slug": "mine", "kind": limited_cli.workspaces[_WS_MINE]["kind"]},
            {"id": _WS_OTHER, "name": "Teammate", "slug": "teammate",
             "kind": limited_cli.workspaces[_WS_OTHER]["kind"]},
        ],
        "workspace_limit": {"id": _WS_MINE, "name": "Mine", "slug": "mine", "team_items": "hide"},
    }
    lists = [r for r in limited_cli.requests if r.url.path == "/v1/workspaces"]
    assert lists and all(r.headers.get(LIMIT) is None for r in lists)


def test_the_desktop_profile_is_read_without_the_limit(limited_cli, monkeypatch):
    """The app's shell opens on `profile`; a limit naming a deleted workspace makes
    the API refuse every limited request, and Settings -- where the limit is fixed --
    sits behind that shell. The account read carries no limit."""
    from probe.cli import desktop

    _limit_this_computer(team_items="hide")
    monkeypatch.setattr(desktop, "_client", lambda: cli.Client())
    desktop.respond(json.dumps({"op": "profile"}).encode())
    reads = [r for r in limited_cli.requests if r.url.path == "/v1/desktop/profile"]
    assert reads and all(r.headers.get(LIMIT) is None for r in reads)


def test_the_service_action_answers_the_clis_json_object(limited_cli, monkeypatch):
    import importlib

    import probe.core
    from probe.core.requests import WorkspaceLimitRequest

    # The action runs the CLI's own client factory outside `cli.main`'s seam.
    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "Client", cli.Client)

    got: list[dict] = []
    assert probe.core.workspace_limit(WorkspaceLimitRequest("teammate", "hide"), got.append) == 0
    (result,) = [event for event in got if event.get("event") == "result"]
    assert (result["action"], result["complete"]) == ("workspace_limit", True)
    (row,) = result["agents"]
    assert row["agent"] is None and row["ok"] is True
    assert row["requested"] == {"workspace": "teammate", "team_items": "hide"}
    assert row["actual"] == {"ok": True, "workspace_limit": {"id": _WS_OTHER, "name": "Teammate",
                                                             "slug": "teammate", "team_items": "hide"}}
    assert got[-1]["event"] == "done" and got[-1]["ok"] is True

    got.clear()
    assert probe.core.workspace_limit(WorkspaceLimitRequest(None), got.append) == 0
    (row,) = next(event for event in got if event.get("event") == "result")["agents"]
    assert row["actual"] == {"ok": True, "workspace_limit": None}
    assert load_context()["workspace"]["id"] == _WS_OTHER  # the pin stays

    got.clear()
    assert probe.core.workspace_limit(WorkspaceLimitRequest("nope"), got.append) == 1
    (row,) = next(event for event in got if event.get("event") == "result")["agents"]
    assert row["ok"] is False and row["actual"]["code"] == "workspace_not_found"


@pytest.mark.parametrize(
    "params,ok",
    [({"workspace": "eng"}, True), ({"workspace": None}, True), ({"workspace": "eng", "team_items": "hide"}, True),
     ({}, False), ({"workspace": None, "team_items": "hide"}, False), ({"workspace": "eng", "team_items": "no"}, False),
     ({"workspace": 3}, False), ({"workspace": "eng", "extra": 1}, False)],
)
def test_the_service_action_checks_its_params(params, ok):
    from probe.core import requests

    if ok:
        assert isinstance(requests.parse("workspace_limit", params), requests.WorkspaceLimitRequest)
    else:
        with pytest.raises(requests.RequestError):
            requests.parse("workspace_limit", params)


def test_the_service_runs_it_as_a_mutating_action():
    from probe.core.requests import ActionName
    from probe.service.protocol import ACTIONS, DESKTOP_READS, Action, DesktopOp

    assert Action.WORKSPACE_LIMIT == ActionName.WORKSPACE_LIMIT.value and Action.WORKSPACE_LIMIT in ACTIONS
    assert DesktopOp.WORKSPACES in DESKTOP_READS


def test_the_team_items_vocabulary_is_one():
    from probe.core.requests import TeamItems

    assert TeamItems is wl.TeamItems


def test_workspace_use_of_another_is_refused_before_any_lookup(limited_cli, capsys):
    """Under the limit the API lists only the limited workspace: the refusal must
    not depend on resolving the other one."""
    _limit_this_computer()
    before = len(limited_cli.requests)
    code, _, err = _run(capsys, "workspace", "use", "teammate")
    assert code == 1 and "probe workspace limit" in err and len(limited_cli.requests) == before
    for ref in ("mine", "slug:mine", f"id:{_WS_MINE}"):  # a bare id is a slug to `use`
        assert _run(capsys, "workspace", "use", ref)[0] == 0, ref


def test_an_unknown_workspace_names_every_choice_not_just_the_limited_one(limited_cli, capsys):
    _limit_this_computer()
    code, out, _ = _run(capsys, "workspace", "limit", "nope", "--json")
    assert code == 1 and json.loads(out)["message"] == "'nope' is not a workspace on this team; its workspaces: mine, teammate"


# -- round 2 (pre-merge review) ----------------------------------------------------


@pytest.fixture
def codex_copy(monkeypatch, tmp_path):
    """A Codex MCP table for this deployment, and a way to read its limit headers."""
    from probe._compat import tomllib
    from probe.cli import codex_config, plugin_cli, setup

    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    url = "http://test/mcp"
    monkeypatch.setattr(setup, "daemon_records", lambda _source: False)
    monkeypatch.setattr(codex_config, "plugin_mcp_url", lambda *_a, **_k: url)
    status = {"now": codex_config.BEARER_STATUS}
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: status["now"])

    def headers() -> dict:
        parsed = tomllib.loads(codex_config.config_path().read_text(encoding="utf-8"))
        return parsed["mcp_servers"][setup.CODEX_MCP_NAME].get("http_headers") or {}

    def write(limit_headers: dict, *, bearer: str | None = "probe_pat_read") -> None:
        path = codex_config.config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        if bearer is None:  # an OAuth install: `codex mcp login`, no static bearer
            status["now"] = "o_auth"
            path.write_text(f'[mcp_servers.{setup.CODEX_MCP_NAME}]\nurl = "{url}"\n', encoding="utf-8")
            if limit_headers:
                codex_config.write_limit_headers(setup.CODEX_MCP_NAME, limit_headers)
            return
        codex_config.write_mcp_bearer(setup.CODEX_MCP_NAME, url=url, token=bearer, limit_headers=limit_headers)

    return type("CodexCopy", (), {"headers": staticmethod(headers), "write": staticmethod(write)})


_COPY = {wl.LIMIT_HEADER: _WS_MINE, wl.TEAM_ITEMS_HEADER: "show"}


def test_deleting_the_limited_workspace_re_renders_the_static_copies(limited_cli, capsys, codex_copy):
    limited_cli.workspaces[_WS_MINE]["project_count"] = 0
    _limit_this_computer()
    save_context({"mcp_token": "probe_pat_read"})
    codex_copy.write(_COPY)

    assert _run(capsys, "workspace", "delete", "mine", "--yes")[0] == 0
    assert wl.limit_headers_of(codex_copy.headers()) == {}


def test_the_wizard_lifting_a_stale_limit_re_renders_the_static_copies(app, monkeypatch, codex_copy, real_computer_workspace):
    from probe.cli import computer_workspace as cw

    monkeypatch.setenv("PROBE_TOKEN", "ros_pat_deadbeef")
    monkeypatch.setattr("probe.sdk.client.Client", lambda **kw: make_client(app, workspace=kw["settings"].workspace))
    monkeypatch.setattr(cw, "run_picker", lambda rows, selected: _WS_OTHER)
    gone = "99999999-9999-9999-9999-999999999999"
    save_context({"base_url": "http://test", "mcp_token": "probe_pat_read",
                  "workspace": {"id": gone, "project": None, "limit": True}})
    codex_copy.write({wl.LIMIT_HEADER: gone, wl.TEAM_ITEMS_HEADER: "show"})

    cw.choose(asking=True)

    assert wl.limit_headers_of(codex_copy.headers()) == {}


def test_team_repairs_a_stale_copy_even_with_nothing_stored(limited_cli, capsys, codex_copy):
    """Idempotent repair: the config already says whole team, a copy does not."""
    save_context({"mcp_token": "probe_pat_read"})
    codex_copy.write(_COPY)

    code, out, _ = _run(capsys, "workspace", "limit", "--team", "--json")

    assert (code, json.loads(out)) == (0, {"ok": True, "workspace_limit": None})
    assert wl.limit_headers_of(codex_copy.headers()) == {}


def test_an_oauth_codex_install_gets_the_limit_headers_alone(limited_cli, codex_copy):
    """`codex mcp login` leaves no static bearer: the limit must still ride along."""
    from probe.cli import setup

    save_context({"mcp_token": "probe_pat_read"})
    codex_copy.write({}, bearer=None)
    _limit_this_computer(team_items="hide")
    save_context({"mcp_token": "probe_pat_read"})

    assert setup.codex_mcp_token_drifted() is True
    setup.sync_codex_mcp_token()
    headers = codex_copy.headers()
    assert headers == {wl.LIMIT_HEADER: _WS_MINE, wl.TEAM_ITEMS_HEADER: "hide"}  # no Authorization written
    assert setup.codex_mcp_token_drifted() is False

    from probe.cli import workspace_limit_cmd

    workspace_limit_cmd.apply(None, team=True)
    assert wl.limit_headers_of(codex_copy.headers()) == {}


def test_each_session_polls_with_its_own_configs_limit(monkeypatch, tmp_path):
    """The service polls for many sessions, each with its own CLI config: the limit
    is the session config's, never the service's own."""
    from probe.service import alertpoll, hints

    _limit_this_computer(_WS_OTHER)  # the SERVICE's own config
    session = tmp_path / "session-config.json"
    session.write_text(json.dumps({"current_context": "default", "contexts": {"default": {
        "base_url": "http://test", "companion_token": "pk_daemon", "token": "probe_pat_s",
        "workspace": {"id": _WS_MINE, "limit": True, "team_items": "hide"}}}}))

    ep = alertpoll.endpoint(str(session))
    assert dict(ep.limit_headers) == {wl.LIMIT_HEADER: _WS_MINE, wl.TEAM_ITEMS_HEADER: "hide"}
    sent: list[dict] = []
    fetcher = alertpoll.Fetcher("0.0.0")
    monkeypatch.setattr(fetcher, "_get", lambda ep, path, headers, deadline: sent.append(headers) or ("none", None))
    fetcher(ep, "s1")
    assert (sent[0].get(wl.LIMIT_HEADER), sent[0].get(wl.TEAM_ITEMS_HEADER)) == (_WS_MINE, "hide")

    # A session whose config has no limit sends none, whatever the service's says.
    session.write_text(json.dumps({"base_url": "http://test", "companion_token": "pk_daemon"}))
    sent.clear()
    fetcher(alertpoll.endpoint(str(session)), "s1")
    assert wl.LIMIT_HEADER not in sent[0]

    # The hint lane reads the session's environment too.
    env = {"PROBE_CONFIG_PATH": str(session), wl.LIMIT_ENV: _WS_OTHER}
    session.write_text(json.dumps({"base_url": "http://test", "token": "probe_pat_s", "mcp_token": "probe_pat_r"}))
    assert dict(hints.credentials(env).limit_headers) == {wl.LIMIT_HEADER: _WS_OTHER, wl.TEAM_ITEMS_HEADER: "show"}


def test_a_limit_refusal_never_expires_into_a_dead_letter(tmp_path, monkeypatch):
    """Transient forever while the limit is misconfigured: the 24 h / 50-attempt
    promotion would dead-letter every queued write one by one."""
    from probe.sdk import journal as journal_module
    from probe.sdk.journal import drain

    monkeypatch.setenv("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC", "0")
    monkeypatch.setattr(journal_module, "MIN_TRANSIENT_ATTEMPTS", 1)
    journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": "http://test"})
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})

    class _Refused:
        class transport:  # noqa: N801 -- the shape drain uses
            @staticmethod
            def request(*a, **k):
                raise errors.error_for(422, {"code": errors.WORKSPACE_LIMIT_UNKNOWN, "message": "gone."})

        def close(self):
            pass

    for _ in range(5):
        drain(journal, client_factory=lambda ctx: _Refused())
    (waiting,) = [op for _, op in journal.pending()]
    assert waiting["attempts"] == 5 and journal.failed() == []


def test_an_environment_slug_resolves_per_account_on_one_api(monkeypatch):
    """Two tenants on one API can both have an `eng` workspace."""
    monkeypatch.setattr(wl, "_RESOLVED", {})
    monkeypatch.setenv(wl.LIMIT_ENV, "eng")
    tenants = {"Bearer probe_pat_a": _WS_MINE, "Bearer probe_pat_b": _WS_OTHER}

    def listing(request):
        return httpx.Response(200, json=[{"id": tenants[request.headers["authorization"]], "slug": "eng"}])

    sent = []
    for token in ("probe_pat_a", "probe_pat_b"):
        save_context({"base_url": "http://test", "token": token})
        wire = Wire({("GET", "/v1/workspaces"): listing})
        wire.transport(resolve()).get("/v1/runs")
        sent.append(wire.seen[-1].headers.get(LIMIT))
    assert sent == [_WS_MINE, _WS_OTHER]


def test_a_plugin_only_oauth_codex_is_said_to_be_unlimited_and_left_working(limited_cli, capsys, codex_copy):
    """No user-level table: the plugin's own manifest declares the MCP with OAuth.
    A user-level table OVERRIDES the plugin's entry (codex_config), so writing one
    would drop its OAuth sign-in: leave it connected, and say it is not limited."""
    from probe.cli import codex_config, setup

    assert not codex_config.config_path().exists()
    save_context({"mcp_token": "probe_pat_read"})

    code, out, _ = _run(capsys, "workspace", "limit", "mine", "--yes")

    assert code == 0
    assert setup.CODEX_UNLIMITED_NOTICE in out
    assert not codex_config.config_path().exists()  # nothing written over the plugin's OAuth
    assert setup.sync_codex_mcp_token() == [setup.CODEX_UNLIMITED_NOTICE]
    _run(capsys, "workspace", "limit", "--team")
    assert setup.sync_codex_mcp_token() == []  # whole team: nothing to say
