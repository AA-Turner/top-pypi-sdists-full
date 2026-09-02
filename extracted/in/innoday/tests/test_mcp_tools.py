"""Request/response behaviour of the MCP tools, with every URL resolved against
the real route table.

This file used to mock `httpx.AsyncClient` wholesale: an `AsyncMock` whose verb
methods returned one canned response for *any* URL. A wrong path therefore
passed identically to a right one, and that is how `sync_repository`'s POST to
`…/repositories/{id}/sync` -- a path no route has ever served -- survived for
months (#652).

Two things replace it, and the split matters for reading what is covered here:

* `tests/test_client_route_contract.py` covers URL *existence*, **statically**,
  for every client-built URL in the repo. That is the guard against a stale
  path, and it needs nothing from this file.
* This file's job is narrower: the MCP tools' request/response *behaviour* --
  headers, body shape, query params, list-wrapping under a dict output schema,
  and the `error_kind` classification `_API` puts on a failure. `routed()` runs
  each call through a real `httpx.AsyncClient` over an `httpx.MockTransport`
  that resolves the outgoing `(method, path)` against that same route table
  before answering, so an unserved path gets a real 404 and a wrong method on a
  real path a real 405. A stale path cannot pass here either -- but the
  systematic coverage of that is the contract test's job, not this file's.

Four groups below deliberately stay mocked *beneath* the HTTP layer, patching
`mcp_module._api` rather than the transport, because what they exercise happens
after the response is decoded and no transport mock can observe it:

* `TestListBoardsWrapsList` and `TestListReturningToolsWrapList` (`_api.get`) --
  the bare-JSON-array endpoints wrapped into `{"boards": [...], "count": n}`,
  and an error dict passed through unchanged.
* `TestUpdateTicketUsesApiPut` (`_api.put`) -- the assertion *is* that the tool
  goes through `_API` at all, for the fresh api_url and the timeout.
* `TestCreateTicketRelease` (`_api.post`) -- the request body built for a field
  that the API, not the tool, validates.

`TestSetupOrgWithEnvSlugValidation` does not route either: one case asserts no
client was constructed at all, the other makes construction raise, and neither
sends a request. None of these five claim URL coverage; the contract test
supplies it for the paths they build.
"""

import inspect
import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastmcp.exceptions import ToolError

import src.mcp.server as mcp_module
from src.cli.config import DEFAULT_API_URL
from tests.test_client_route_contract import ROUTES

# The real load_config, captured before the autouse reset_config fixture
# patches it. TestLoadConfigTeamSecret exercises load_config itself, so it
# must call the genuine implementation, not the fixture's in-memory stand-in.
_real_load_config = mcp_module.load_config


@pytest.fixture(autouse=True)
def reset_config():
    """Reset MCP config state between tests, defaulting to the org_id/user_id
    nearly every test in this file needs -- individual tests still override
    to None or a different value where that's the actual thing under test
    (e.g. TestGetAllWork's org_id-override test, or the various
    test_returns_error_when_no_*_id tests).

    get_config() re-reads config from disk on every call (so a long-lived MCP
    process picks up config changes without a restart -- see server.py). To
    keep these in-memory config mutations authoritative under that behavior,
    patch load_config() to return the module-level `config` object the tests
    manipulate, rather than reading the real ~/.innoday/config.json."""
    original_user_id = mcp_module.config.user_id
    original_org_id = mcp_module.config.organization_id
    original_api_url = mcp_module.config.api_url
    original_team_secret = mcp_module.config.team_secret
    original_cli_token = mcp_module.config.cli_token
    mcp_module.config.user_id = "user-abc"
    mcp_module.config.organization_id = "org-123"
    mcp_module.config.team_secret = None
    # Identity is the Bearer token; every tool call needs one.
    mcp_module.config.cli_token = "idt_test0.secret"
    with patch.object(mcp_module, "load_config", lambda: mcp_module.config):
        yield
    mcp_module.config.user_id = original_user_id
    mcp_module.config.organization_id = original_org_id
    mcp_module.config.api_url = original_api_url
    mcp_module.config.team_secret = original_team_secret
    mcp_module.config.cli_token = original_cli_token


# In FastMCP v3, @app.tool() returns the original (async) function, so the
# decorated name is directly the callable (v2 wrapped it in a FunctionTool
# whose underlying callable was `.fn`).
_get_all_work = mcp_module.get_all_work
_update_release = mcp_module.update_release
_create_release = mcp_module.create_release
_list_releases = mcp_module.list_releases
_check_status = mcp_module.check_status
_get_release = mcp_module.get_release
_get_scrum_summary = mcp_module.get_scrum_summary
_get_assignment_summary = mcp_module.get_assignment_summary
_get_board_summary_data = mcp_module.get_board_summary_data
_save_board_summary = mcp_module.save_board_summary
_save_project_summary = mcp_module.save_project_summary
_setup_organization = mcp_module.setup_organization
_list_organizations = mcp_module.list_organizations
_list_boards = mcp_module.list_boards
_get_repository_issues = mcp_module.get_repository_issues
_list_tickets = mcp_module.list_tickets
_get_board_lists = mcp_module.get_board_lists
_setup_org_with_env = mcp_module.setup_org_with_env
_update_ticket = mcp_module.update_ticket
_create_ticket = mcp_module.create_ticket
_sync_repository = mcp_module.sync_repository
_analyze_temporal_patterns = mcp_module.analyze_temporal_patterns


# The genuine class, captured before anything patches the name: `routed()` builds
# a real AsyncClient, and constructing one while `httpx.AsyncClient` is patched
# would recurse into the patch.
_REAL_ASYNC_CLIENT = httpx.AsyncClient

# Distinguishes "no body" from a body that is literally `null`.
_NO_BODY = object()


@dataclass(frozen=True)
class Canned:
    """The response the transport gives back -- but only once the route table has
    agreed that a route serves the request.

    Built fresh on every call rather than held as an `httpx.Response`, so one
    spec can answer several requests without a consumed stream.
    """

    status: int = 200
    json: Any = _NO_BODY
    text: str = ""

    def build(self) -> httpx.Response:
        if self.json is not _NO_BODY:
            return httpx.Response(self.status, json=self.json)
        return httpx.Response(self.status, text=self.text)


def _route_failure(method: str, path: str) -> Optional[httpx.Response]:
    """A real 404 or 405 when the app's own route table does not serve this
    request; `None` when it does and the canned response applies.

    Matching is by each route's compiled starlette regex rather than by string
    equality, because a stale literal segment can be *absorbed* by a `{param}`
    -- `…/tickets/refresh` lands in `{ticket_id}` and is therefore a 405, not a
    404 -- and the two need different fixes (#652).
    """
    matches = [route for route in ROUTES if route.regex.match(path)]
    if not matches:
        return httpx.Response(404, json={"detail": f"no route serves the path {path}"})
    if not any(method in route.methods for route in matches):
        allowed = sorted({m for route in matches for m in route.methods})
        return httpx.Response(
            405,
            json={"detail": f"{path} serves {', '.join(allowed)}, not {method}"},
        )
    return None


def _as_responder(spec) -> Callable[[httpx.Request], Canned]:
    """Normalise what a test passed to `routed()` into one callable."""
    if isinstance(spec, Canned):
        return lambda request: spec
    if isinstance(spec, dict):
        return lambda request: spec[request.method]
    if callable(spec):
        return spec
    queue = list(spec)
    if not queue:
        raise ValueError("routed() needs at least one Canned response")

    def next_in_order(request: httpx.Request) -> Canned:
        # The last entry repeats, so a test only lists the responses it cares
        # about ordering between.
        return queue.pop(0) if len(queue) > 1 else queue[0]

    return next_in_order


class RoutedCalls:
    """The requests that reached the transport, for assertions about what was
    actually sent. `constructor` is the patched `httpx.AsyncClient` itself, so a
    test can assert that no client was ever opened.
    """

    def __init__(self, responder: Callable[[httpx.Request], Canned]) -> None:
        self._responder = responder
        self.requests: List[httpx.Request] = []
        self.constructor: Any = None

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        failure = _route_failure(request.method, request.url.path)
        if failure is not None:
            return failure
        return self._responder(request).build()

    # -- what went out ------------------------------------------------------
    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    def path(self, index: int = -1) -> str:
        return self.requests[index].url.path

    def paths(self) -> List[str]:
        return [request.url.path for request in self.requests]

    def headers(self, index: int = -1) -> httpx.Headers:
        return self.requests[index].headers

    def params(self, index: int = -1) -> Dict[str, str]:
        return dict(self.requests[index].url.params)

    def body(self, index: int = -1) -> Any:
        return json.loads(self.requests[index].content)


@contextmanager
def routed(spec):
    """Patch `httpx.AsyncClient` with a *real* client over a route-resolving mock
    transport, and yield the `RoutedCalls` recorder.

    `spec` says what to answer a request the route table serves: one `Canned`, a
    sequence of them (consumed in order, the last repeating), a dict keyed by
    HTTP method, or a `callable(request) -> Canned`. Raising an
    `httpx.RequestError` from that callable exercises the transport-failure path.

    A real client with a fake transport, rather than a mocked client, is the
    point: httpx's own URL construction, query-string encoding, body
    serialisation and header handling all run, so the path the route table is
    asked about is the path that would have gone on the wire. Arbitrary
    constructor kwargs are accepted and ignored -- `server.py` builds clients
    both bare and with `timeout=`.
    """
    calls = RoutedCalls(_as_responder(spec))
    constructor = MagicMock(
        side_effect=lambda *args, **kwargs: _REAL_ASYNC_CLIENT(
            transport=httpx.MockTransport(calls.handle)
        )
    )
    calls.constructor = constructor
    with patch("httpx.AsyncClient", constructor):
        yield calls


# Called directly rather than through FastMCP (which resolves them), an omitted
# tool parameter arrives as a `FieldInfo`, not its declared default. That used to
# be invisible: the blanket mock never serialised anything. The routed transport
# does, so a leaked `FieldInfo` now reaches the query string as its repr -- so
# tools with several optional params get them spelled out. Same reason as the
# `setdefault` blocks in the summary tests.
_ALL_WORK_ARGS = {
    "status": None,
    "priority": None,
    "source_platform": None,
    "assignee": None,
    "limit": 50,
}


class TestOrgToolsSendTeamSecret:
    """The org-management tools that build headers manually (rather than via
    get_user_headers/_api.resolve_org) must still resolve config per request
    and attach X-Team-Secret when configured -- otherwise they 401 on a gated
    API even after the team secret is seeded. Regression guard for #338's
    follow-up: these three tools were the ones reading the import-time config
    snapshot and never sending the team secret."""

    @pytest.mark.asyncio
    async def test_setup_organization_sends_team_secret(self):
        mcp_module.config.user_id = "user-abc"
        mcp_module.config.team_secret = "shh-secret"
        with routed(Canned(201, json={"id": "org-new"})) as calls:
            await _setup_organization(
                name="Acme",
                slug=None,
                description=None,
                github_url=None,
                jira_url=None,
                user_id="user-abc",
            )

        assert calls.path() == "/api/v1/organizations"
        assert calls.headers()["Authorization"] == "Bearer idt_test0.secret"
        assert "X-User-ID" not in calls.headers()
        assert calls.headers()["X-Team-Secret"] == "shh-secret"

    @pytest.mark.asyncio
    async def test_list_organizations_sends_team_secret(self):
        mcp_module.config.user_id = "user-abc"
        mcp_module.config.team_secret = "shh-secret"
        with routed(Canned(json=[])) as calls:
            await _list_organizations(user_id="user-abc")

        assert calls.path() == "/api/v1/organizations"
        assert calls.headers()["X-Team-Secret"] == "shh-secret"

    @pytest.mark.asyncio
    async def test_omits_team_secret_when_not_configured(self):
        mcp_module.config.user_id = "user-abc"
        mcp_module.config.team_secret = None
        with routed(Canned(json=[])) as calls:
            await _list_organizations(user_id="user-abc")

        assert "X-Team-Secret" not in calls.headers()


class TestListBoardsWrapsList:
    """The /boards endpoint returns a bare JSON array, but the tool's declared
    output schema is an object -- FastMCP rejects a top-level list
    ("structured_content must be a dict"). list_boards must wrap it in a dict;
    error dicts from _api.get must pass through unchanged."""

    @pytest.mark.asyncio
    async def test_bare_list_is_wrapped_in_dict(self):
        mcp_module.config.organization_id = "org-1"
        boards = [{"id": "b1", "board_name": "PixelFuel"}]
        with patch.object(mcp_module._api, "get", AsyncMock(return_value=boards)):
            result = await _list_boards(organization_id="org-1")
        assert isinstance(result, dict)
        assert result["boards"] == boards
        assert result["count"] == 1
        assert result["organization_id"] == "org-1"

    @pytest.mark.asyncio
    async def test_error_dict_passes_through(self):
        mcp_module.config.organization_id = "org-1"
        err = {"error": "API error 500", "details": "boom"}
        with patch.object(mcp_module._api, "get", AsyncMock(return_value=err)):
            result = await _list_boards(organization_id="org-1")
        assert result == err


class TestListReturningToolsWrapList:
    """Sibling tools to list_boards that also hit bare-JSON-array endpoints
    under a dict output schema -- each must wrap its list so FastMCP doesn't
    reject it ("structured_content must be a dict"), and pass _api.get error
    dicts through unchanged. Same class of bug fixed for list_boards in #343."""

    @pytest.mark.asyncio
    async def test_get_repository_issues_wraps_list(self):
        mcp_module.config.organization_id = "org-1"
        issues = [{"id": 1, "title": "bug"}]
        with patch.object(mcp_module._api, "get", AsyncMock(return_value=issues)):
            result = await _get_repository_issues(
                registration_id="repo-1", organization_id="org-1", status=None, limit=50
            )
        assert isinstance(result, dict)
        assert result["issues"] == issues
        assert result["count"] == 1
        assert result["repository_id"] == "repo-1"

    @pytest.mark.asyncio
    async def test_get_repository_issues_error_passes_through(self):
        mcp_module.config.organization_id = "org-1"
        err = {"error": "API error 404", "details": "no repo"}
        with patch.object(mcp_module._api, "get", AsyncMock(return_value=err)):
            result = await _get_repository_issues(
                registration_id="repo-1", organization_id="org-1", status=None, limit=50
            )
        assert result == err

    @pytest.mark.asyncio
    async def test_list_tickets_wraps_list(self):
        mcp_module.config.organization_id = "org-1"
        tickets = [{"id": "t1"}, {"id": "t2"}]
        with patch.object(mcp_module._api, "get", AsyncMock(return_value=tickets)):
            result = await _list_tickets(
                organization_id="org-1", status=None, assignee=None, limit=100
            )
        assert isinstance(result, dict)
        assert result["tickets"] == tickets
        assert result["count"] == 2
        assert result["organization_id"] == "org-1"

    @pytest.mark.asyncio
    async def test_get_board_lists_wraps_list(self):
        mcp_module.config.organization_id = "org-1"
        lists = [{"id": "l1", "name": "Todo"}]
        with patch.object(mcp_module._api, "get", AsyncMock(return_value=lists)):
            result = await _get_board_lists(board_id="board-1")
        assert isinstance(result, dict)
        assert result["lists"] == lists
        assert result["count"] == 1
        assert result["board_id"] == "board-1"


class TestGetUserHeaders:
    def test_returns_header_when_user_configured(self):
        headers = mcp_module.get_user_headers()
        assert headers == {"Authorization": "Bearer idt_test0.secret"}

    def test_raises_when_no_token_configured(self):
        """Identity is the token now — no silent fallback to X-User-ID."""
        mcp_module.config.cli_token = None
        with pytest.raises(ValueError, match="No InnoDay API token configured"):
            mcp_module.get_user_headers()

    def test_includes_team_secret_when_configured(self):
        """The door key rides alongside the token; it is not identity."""
        mcp_module.config.team_secret = "shh-secret"
        headers = mcp_module.get_user_headers()
        assert headers == {
            "Authorization": "Bearer idt_test0.secret",
            "X-Team-Secret": "shh-secret",
        }

    def test_omits_team_secret_when_not_configured(self):
        headers = mcp_module.get_user_headers()
        assert "X-Team-Secret" not in headers


class TestConfigRefreshedPerRequest:
    """Regression test for #338: get_user_headers() must reflect the current
    on-disk config, not a snapshot cached at module import. The MCP server is
    a long-lived process; if the team secret is seeded into the config *after*
    the server starts, tools were 401ing because the cached config never saw
    it. get_config() (called by get_user_headers) now re-reads per request."""

    def test_team_secret_added_after_start_is_picked_up_without_reimport(self):
        # Simulate the on-disk config gaining a team secret between two calls,
        # the way `innoday config set team-secret` (or a fresh install seed)
        # would, while the MCP process keeps running.
        disk = mcp_module.InnoConfig(
            user_id="user-abc", cli_token="idt_test0.secret", team_secret=None
        )
        with patch.object(mcp_module, "load_config", lambda: disk):
            first = mcp_module.get_user_headers()
            assert "X-Team-Secret" not in first

            # Config changes on disk; no re-import, no reconnect.
            disk.team_secret = "now-seeded"
            second = mcp_module.get_user_headers()
            assert second["X-Team-Secret"] == "now-seeded"

    def test_resolve_org_reflects_current_config(self):
        disk = mcp_module.InnoConfig(
            user_id="user-abc", cli_token="idt_test0.secret", organization_id=None
        )
        with patch.object(mcp_module, "load_config", lambda: disk):
            assert mcp_module._API.resolve_org(None) is None
            disk.organization_id = "org-late"
            assert mcp_module._API.resolve_org(None) == "org-late"
            # An explicit argument still wins over the resolved config value.
            assert mcp_module._API.resolve_org("explicit") == "explicit"

    @pytest.mark.asyncio
    async def test_api_get_uses_fresh_api_url(self):
        """_API.get must build the request URL from get_config() (fresh), not a
        stale module-global api_url set at import. Simulate the on-disk api_url
        changing after start (as `innoday config set api-url` would) and assert
        the next call targets the NEW base URL."""
        disk = mcp_module.InnoConfig(
            user_id="user-abc", cli_token="idt_test0.secret", api_url="http://old:8000"
        )

        with patch.object(mcp_module, "load_config", lambda: disk):
            # A real path (`/api/v1/public/status`), not the `/api/v1/ping` this
            # used to call: the routed transport 404s anything the route table
            # does not serve and a 404 now raises, so what is under test here --
            # which *host* the request went to -- needs a servable path to reach.
            with routed(Canned(json={})) as calls:
                disk.api_url = "http://new:9000"  # changed after "start"
                await mcp_module._api.get("/api/v1/public/status")

        assert str(calls.last.url).startswith("http://new:9000"), calls.last.url

    def test_no_tool_reads_stale_module_global_api_url(self):
        """Structural guard: every request-URL site must read
        get_config().api_url, never the stale module-global `config.api_url`.
        The only permitted raw `config.api_url` is load_config()'s own
        assignment. Prevents reintroducing the divergence the _API docstring
        promises against."""
        import inspect

        src = inspect.getsource(mcp_module)
        offenders = [
            line.strip()
            for line in src.splitlines()
            # a raw read like `config.api_url` not via get_config(), and not the
            # `config.api_url =` assignment in load_config()
            if "config.api_url" in line
            and "get_config()" not in line
            and "config.api_url =" not in line
        ]
        assert offenders == [], f"stale config.api_url reads: {offenders}"


class TestLoadConfigTeamSecret:
    def test_reads_team_secret_from_cli_config(self):
        mock_cli_config = MagicMock()
        mock_cli_config._raw = {}
        mock_cli_config.get_user_id.return_value = "user-abc"
        mock_cli_config.get_current_organization.return_value = None
        mock_cli_config.get_current_project_id.return_value = None
        mock_cli_config.get_team_secret.return_value = "cli-secret"

        with (
            patch.object(mcp_module, "CLIConfig", return_value=mock_cli_config),
            patch.dict("os.environ", {}, clear=True),
        ):
            loaded = _real_load_config()

        assert loaded.team_secret == "cli-secret"

    def test_env_var_overrides_cli_config(self):
        mock_cli_config = MagicMock()
        mock_cli_config._raw = {}
        mock_cli_config.get_user_id.return_value = "user-abc"
        mock_cli_config.get_current_organization.return_value = None
        mock_cli_config.get_current_project_id.return_value = None
        mock_cli_config.get_team_secret.return_value = "cli-secret"

        with (
            patch.object(mcp_module, "CLIConfig", return_value=mock_cli_config),
            patch.dict("os.environ", {"INNODAY_TEAM_SECRET": "env-secret"}, clear=True),
        ):
            loaded = _real_load_config()

        assert loaded.team_secret == "env-secret"


class TestLoadConfigApiUrl:
    """Where the MCP server thinks InnoDay is (#731).

    It read identity, org, project, team secret and token from the CLI config
    and **never** `get_api_url()`, so `innoday config set api-url` moved the
    CLI and left the MCP server pointed wherever `InnoConfig.api_url`'s field
    default or `INNODAY_API_URL` said. The two surfaces silently disagreed, and
    that is the first thing to check behind any "the CLI works but MCP 401s or
    shows different data".

    Precedence is the same as every other value here: field default, then the
    CLI config, then the environment.
    """

    def _cli_config(self, api_url):
        mock = MagicMock()
        mock._raw = {}
        mock.get_api_url.return_value = api_url
        mock.get_user_id.return_value = "user-abc"
        mock.get_current_organization.return_value = None
        mock.get_current_project_id.return_value = None
        mock.get_team_secret.return_value = None
        mock.get_cli_token.return_value = None
        return mock

    def test_reads_api_url_from_cli_config(self):
        with (
            patch.object(
                mcp_module,
                "CLIConfig",
                return_value=self._cli_config("http://localhost:8000"),
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            loaded = _real_load_config()

        assert loaded.api_url == "http://localhost:8000"

    def test_a_configured_deployment_reaches_the_server_too(self):
        """Not just localhost: the direction that was actually broken is a
        config pointing somewhere the field default does not."""
        with (
            patch.object(
                mcp_module,
                "CLIConfig",
                return_value=self._cli_config("https://innoday-dev.up.railway.app"),
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            loaded = _real_load_config()

        assert loaded.api_url == "https://innoday-dev.up.railway.app"

    def test_env_var_overrides_cli_config(self):
        with (
            patch.object(
                mcp_module,
                "CLIConfig",
                return_value=self._cli_config("https://www.inno.day"),
            ),
            patch.dict(
                "os.environ", {"INNODAY_API_URL": "http://localhost:9999"}, clear=True
            ),
        ):
            loaded = _real_load_config()

        assert loaded.api_url == "http://localhost:9999"

    def test_an_unreadable_cli_config_falls_back_to_the_default(self):
        """The field default is the last resort, and the only thing that
        reaches it is a `CLIConfig` that would not construct at all."""
        with (
            patch.object(mcp_module, "CLIConfig", side_effect=OSError("no config")),
            patch.dict("os.environ", {}, clear=True),
        ):
            loaded = _real_load_config()

        assert loaded.api_url == DEFAULT_API_URL


class TestGetAllWork:
    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _get_all_work(organization_id=None)
        assert "error" in result
        assert "Organization ID" in result["error"]

    @pytest.mark.asyncio
    async def test_uses_configured_org_id(self):
        work = [
            {"id": 1, "summary": "Fix login bug", "status": "open"},
            {"id": 2, "summary": "Add dark mode", "status": "todo"},
        ]

        with routed(Canned(json=work)) as calls:
            result = await _get_all_work(**_ALL_WORK_ARGS, organization_id=None)

        assert calls.path() == "/api/v1/organizations/org-123/work"
        assert result["count"] == 2
        assert result["organization_id"] == "org-123"
        assert len(result["work_items"]) == 2

    @pytest.mark.asyncio
    async def test_org_id_parameter_overrides_config(self):
        mcp_module.config.organization_id = "config-org"

        with routed(Canned(json=[])) as calls:
            result = await _get_all_work(
                **_ALL_WORK_ARGS, organization_id="override-org"
            )

        assert result["organization_id"] == "override-org"
        assert calls.path() == "/api/v1/organizations/override-org/work"

    @pytest.mark.asyncio
    async def test_returns_error_on_api_failure(self):
        with routed(Canned(500, text="Internal Server Error")) as calls:
            result = await _get_all_work(**_ALL_WORK_ARGS, organization_id="org-123")

        assert "error" in result
        # A 5xx is the route answering, so it returns rather than raising -- and
        # it says which kind of failure it was, which is what used to be missing.
        assert result["error_kind"] == "server_error"
        assert result["status"] == 500
        assert result["path"] == calls.path()


class TestUpdateRelease:
    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _update_release(
            version="v1.0.0", notes="some notes", organization_id=None
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_a_missing_release_raises_rather_than_returning(self):
        """The lookup 404s, and `_API`'s contract raises on a 404.

        This used to assert `"error" in result`: the 404 came back as a
        *successful* tool result, indistinguishable from the route refusing the
        request on its merits. It is now a `ToolError`, and the version still has
        to be legible in the message -- that is the part a caller acts on.
        """
        with routed(Canned(404, text="no such release")) as calls:
            with pytest.raises(ToolError) as raised:
                await _update_release(
                    version="v9.9.9",
                    notes="notes",
                    project_id="proj-1",
                    organization_id=None,
                )

        assert "v9.9.9" in str(raised.value)
        assert calls.paths() == [
            "/api/v1/organizations/org-123/releases/by-version/v9.9.9"
        ]

    @pytest.mark.asyncio
    async def test_returns_error_for_synthetic_release(self):
        # 200 with no 'id' key -- a release the API synthesised from tags.
        with routed(Canned(json={"version": "v1.0.0"})) as calls:
            result = await _update_release(
                version="v1.0.0",
                notes="notes",
                project_id="proj-1",
                organization_id=None,
            )

        assert "error" in result
        assert "synthetic" in result["error"].lower() or "id" in result["error"].lower()
        # Refused after the lookup and before any write: one request, a GET.
        assert [request.method for request in calls.requests] == ["GET"]

    @pytest.mark.asyncio
    async def test_patches_notes_successfully(self):
        by_method = {
            "GET": Canned(json={"id": "release-xyz", "version": "v1.4.0"}),
            "PATCH": Canned(
                json={
                    "id": "release-xyz",
                    "version": "v1.4.0",
                    "notes": "Release notes here",
                    "status": "released",
                }
            ),
        }

        with routed(by_method) as calls:
            result = await _update_release(
                version="v1.4.0",
                notes="Release notes here",
                project_id="proj-1",
                organization_id=None,
            )

        assert result["notes"] == "Release notes here"
        assert result["version"] == "v1.4.0"
        # Looked up by version, written by id -- two different routes.
        assert calls.paths() == [
            "/api/v1/organizations/org-123/releases/by-version/v1.4.0",
            "/api/v1/organizations/org-123/releases/release-xyz",
        ]
        assert calls.body() == {"notes": "Release notes here"}


class TestCreateRelease:
    @pytest.mark.asyncio
    async def test_returns_error_when_organization_id_missing(self):
        mcp_module.config.organization_id = None
        result = await _create_release(version="v1.0.0", organization_id=None)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_creates_release_with_required_fields(self):
        created = Canned(
            201,
            json={"id": "release-xyz", "version": "v1.0.0", "status": "planned"},
        )

        with routed(created) as calls:
            result = await _create_release(
                version="v1.0.0",
                name=None,
                description=None,
                notes=None,
                project_id="proj-1",
                status="planned",
                released_at=None,
                organization_id="org-123",
            )

        assert result["version"] == "v1.0.0"
        assert result["status"] == "planned"
        assert calls.path() == "/api/v1/organizations/org-123/releases"
        assert calls.body() == {
            "version": "v1.0.0",
            "status": "planned",
            "project_id": "proj-1",
        }

    @pytest.mark.asyncio
    async def test_passes_optional_fields_when_provided(self):
        created = Canned(201, json={"id": "release-xyz", "version": "v1.4.0"})

        with routed(created) as calls:
            await _create_release(
                version="v1.4.0",
                name="Spring Release",
                description="A description",
                notes="Some notes",
                project_id="proj-1",
                status="planned",
                released_at="2026-07-01T00:00:00Z",
                organization_id="org-123",
            )

        payload = calls.body()
        assert payload["name"] == "Spring Release"
        assert payload["description"] == "A description"
        assert payload["notes"] == "Some notes"
        assert payload["project_id"] == "proj-1"
        assert payload["released_at"] == "2026-07-01T00:00:00Z"

    @pytest.mark.asyncio
    async def test_surfaces_409_conflict_as_error(self):
        conflict = Canned(409, text="Release 'v1.0.0' already exists")

        with routed(conflict) as calls:
            result = await _create_release(
                version="v1.0.0",
                name=None,
                description=None,
                notes=None,
                project_id="proj-1",
                status="planned",
                released_at=None,
                organization_id="org-123",
            )

        assert "error" in result
        # A 409 is a decision about the request's content, not a wrong URL: it
        # returns, labelled `refused`, and tools branch on `"error" in result`.
        assert result["error_kind"] == "refused"
        assert result["status"] == 409
        assert result["path"] == calls.path()


class TestListReleases:
    @pytest.mark.asyncio
    async def test_returns_error_when_organization_id_missing(self):
        mcp_module.config.organization_id = None
        result = await _list_releases(organization_id=None)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_lists_releases_returns_count_and_org_id(self):
        releases = [
            {"id": "1", "version": "v1.0.0"},
            {"id": "2", "version": "v1.1.0"},
            {"id": "3", "version": "v1.2.0"},
        ]

        with routed(Canned(json=releases)) as calls:
            result = await _list_releases(
                project_id=None, status=None, organization_id="org-123"
            )

        assert calls.path() == "/api/v1/organizations/org-123/releases"
        assert result["count"] == 3
        assert result["organization_id"] == "org-123"
        assert len(result["releases"]) == 3

    @pytest.mark.asyncio
    async def test_filters_by_project_and_status(self):
        with routed(Canned(json=[])) as calls:
            await _list_releases(
                project_id="proj-1", status="released", organization_id="org-123"
            )

        # Read off the URL httpx built, not off the kwargs handed to a mock: the
        # filters only reach the API if they survive query-string encoding.
        assert calls.params() == {"project_id": "proj-1", "status": "released"}


class TestGetRelease:
    @pytest.mark.asyncio
    async def test_returns_error_when_organization_id_missing(self):
        mcp_module.config.organization_id = None
        result = await _get_release(
            version="v1.0.0", release_id=None, organization_id=None
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_returns_error_when_neither_version_nor_release_id_given(self):
        result = await _get_release(
            version=None, release_id=None, organization_id="org-123"
        )
        assert result == {"error": "Provide either version or release_id"}

    @pytest.mark.asyncio
    async def test_returns_error_when_both_version_and_release_id_given(self):
        result = await _get_release(
            version="v1.0.0", release_id="abc", organization_id="org-123"
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_by_version_calls_by_version_endpoint(self):
        with routed(Canned(json={"version": "v1.4.0"})) as calls:
            result = await _get_release(
                version="v1.4.0",
                release_id=None,
                project_id="proj-1",
                organization_id="org-123",
            )

        assert calls.path() == (
            "/api/v1/organizations/org-123/releases/by-version/v1.4.0"
        )
        assert result["version"] == "v1.4.0"

    @pytest.mark.asyncio
    async def test_get_by_release_id_calls_id_endpoint(self):
        with routed(Canned(json={"id": "abc"})) as calls:
            result = await _get_release(
                version=None,
                release_id="abc",
                project_id="proj-1",
                organization_id="org-123",
            )

        assert calls.path() == "/api/v1/organizations/org-123/releases/abc"
        assert result["id"] == "abc"


class TestCheckStatus:
    @pytest.mark.asyncio
    async def test_returns_structured_status_on_200(self):
        mcp_module.config.organization_id = None
        mcp_module.config.user_id = None

        status = Canned(
            json={
                "status": "operational",
                "environment": "dev",
                "port": 8002,
                "env_file": ".env.dev",
                "db_host": "aws-1-us-west-2.pooler.supabase.com",
                "version": "0.110.0-beta",
                "uptime_seconds": 123.4,
            }
        )

        with routed(status) as calls:
            result = await _check_status(organization_id=None)

        assert calls.paths() == ["/api/v1/public/status"]

        expected_keys = {
            "api_url",
            "status",
            "environment",
            "port",
            "env_file",
            "db_host",
            "version",
            "uptime_seconds",
            "user_id",
            "organization_id",
            "assigned_tickets_count",
        }
        assert expected_keys.issubset(result.keys())
        assert result["status"] == "operational"
        assert result["port"] == 8002
        assert result["env_file"] == ".env.dev"
        assert result["db_host"] == "aws-1-us-west-2.pooler.supabase.com"
        assert result["assigned_tickets_count"] is None

    @pytest.mark.asyncio
    async def test_returns_unreachable_on_connect_error(self):
        def refuse(request):
            raise httpx.ConnectError("connection refused")

        with routed(refuse):
            result = await _check_status(organization_id=None)

        assert result["status"] == "unreachable"
        assert result["api_url"] == mcp_module.config.api_url
        assert "connection refused" in result["error"]

    @pytest.mark.asyncio
    async def test_returns_unreachable_on_non_200(self):
        with routed(Canned(503, text="Service Unavailable")):
            result = await _check_status(organization_id=None)

        assert result["status"] == "unreachable"
        assert "503" in result["error"]

    @pytest.mark.asyncio
    async def test_includes_user_and_org_from_config(self):
        # Two calls, two routes: the public status probe, then the ticket count.
        with routed([Canned(json={"status": "operational"}), Canned(json=[])]) as calls:
            result = await _check_status(organization_id=None)

        assert result["user_id"] == "user-abc"
        assert result["organization_id"] == "org-123"
        assert calls.paths() == [
            "/api/v1/public/status",
            "/api/v1/organizations/org-123/tickets",
        ]
        assert calls.params(1) == {"assigned_to": "user-abc", "limit": "500"}

    @pytest.mark.asyncio
    async def test_assigned_tickets_count_null_when_no_identity(self):
        mcp_module.config.user_id = None
        mcp_module.config.organization_id = None

        with routed(Canned(json={"status": "operational"})) as calls:
            result = await _check_status(organization_id=None)

        assert result["assigned_tickets_count"] is None
        # No identity to count against, so the ticket call is never made.
        assert calls.paths() == ["/api/v1/public/status"]

    @pytest.mark.asyncio
    async def test_assigned_tickets_count_counts_tickets(self):
        with routed(
            [
                Canned(json={"status": "operational"}),
                Canned(json=[{"id": 1}, {"id": 2}, {"id": 3}]),
            ]
        ):
            result = await _check_status(organization_id=None)

        assert result["assigned_tickets_count"] == 3


class TestGetScrumSummary:
    """PF-398: this now calls the summary engine, not a ticket-status regroup.

    The old shape counted tickets by status client-side, which could not tell
    "assigned but nothing happened" from "nobody is on it" and had no notion of
    a window at all. It now proxies `GET .../summary-data` and stays a thin
    proxy -- most of what these tests protect is that it does not start
    interpreting, narrating, or reshaping what the engine returned.
    """

    @staticmethod
    def _assembly(**kw):
        base = {
            "outcome": "assembled",
            "window_spec": "3d",
            "synced": False,
            "active": [{"ticket_ref": "PF-1"}],
            "active_total": 1,
            "no_work_detected": [],
            "unassigned_work_happening": [],
            "up_next": [],
            "footer": "1 of 1 active shown",
            "source_fingerprint": {"commits": [], "tickets": []},
            "body_markdown": None,
        }
        base.update(kw)
        return base

    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _get_scrum_summary(project_id="proj-1", organization_id=None)
        assert "error" in result

    async def _call(self, payload, **kwargs):
        # Every argument is passed explicitly: called directly (rather than
        # through FastMCP, which resolves them) an omitted parameter arrives as
        # a `FieldInfo`, not its default. Same convention as the other tool
        # tests in this file.
        kwargs.setdefault("scope", "scrum")
        kwargs.setdefault("window", "3d")
        kwargs.setdefault("release", None)
        with routed(Canned(json=payload)) as calls:
            result = await _get_scrum_summary(
                project_id="proj-1", organization_id="org-123", **kwargs
            )
        return result, calls

    @pytest.mark.asyncio
    async def test_calls_the_engine_not_the_ticket_list(self):
        _, calls = await self._call(self._assembly())
        assert calls.path() == (
            "/api/v1/organizations/org-123/projects/proj-1/summary-data"
        )

    def test_team_scope_is_the_declared_default(self):
        signature = inspect.signature(mcp_module.get_scrum_summary)
        assert signature.parameters["scope"].default.default == "scrum"
        assert signature.parameters["window"].default.default == "3d"

    @pytest.mark.asyncio
    async def test_team_scope_names_nobody(self):
        """user_id absent is what makes it the team roll-up, not a bug."""
        _, calls = await self._call(self._assembly(), scope="scrum")
        assert calls.params()["summary_type"] == "scrum"
        assert "user_id" not in calls.params()

    @pytest.mark.asyncio
    async def test_personal_scope_defers_to_the_token_for_who_me_is(self):
        """'me' is resolved server-side, so the MCP server never asserts an identity."""
        _, calls = await self._call(self._assembly(), scope="me")
        assert calls.params()["summary_type"] == "personal"
        assert calls.params()["user_id"] == "me"

    @pytest.mark.asyncio
    async def test_personal_scope_tells_the_caller_which_id_to_echo_back(self):
        """The resolved id has to reach `save_project_summary`, or the write
        lands in the team slot. Naming it in `progress` is what makes the
        round trip discoverable rather than folklore."""
        result, _ = await self._call(self._assembly(user_id="user-abc"), scope="me")
        assert any("user_id=user-abc" in step for step in result["progress"])

    @pytest.mark.asyncio
    async def test_team_scope_says_nothing_about_echoing_a_user_id(self):
        result, _ = await self._call(self._assembly(), scope="scrum")
        assert not any("Echo user_id" in step for step in result["progress"])

    @pytest.mark.asyncio
    async def test_window_is_passed_through_verbatim(self):
        _, calls = await self._call(self._assembly(), window="2w")
        assert calls.params()["window_spec"] == "2w"

    @pytest.mark.asyncio
    async def test_a_release_scope_replaces_the_window(self):
        """A release narrows the ticket universe; a duration cannot express it.

        Sending both would leave the server to guess which scope was meant, so
        the release wins and the window is not sent at all.
        """
        _, calls = await self._call(self._assembly(), release="current")
        assert calls.params()["release"] == "current"
        assert "window_spec" not in calls.params()

    def test_release_is_declared_and_defaults_to_no_scope(self):
        signature = inspect.signature(mcp_module.get_scrum_summary)
        assert signature.parameters["release"].default.default is None

    @pytest.mark.asyncio
    async def test_the_assembled_blocks_are_returned_unreshaped(self):
        result, _ = await self._call(self._assembly())
        assert result["active"] == [{"ticket_ref": "PF-1"}]
        assert result["source_fingerprint"] == {"commits": [], "tickets": []}

    @pytest.mark.asyncio
    async def test_assembled_asks_the_caller_to_write_the_prose(self):
        result, _ = await self._call(self._assembly())
        assert any("🚀" in step for step in result["progress"])
        assert any("save_project_summary" in step for step in result["progress"])

    @pytest.mark.asyncio
    async def test_unchanged_does_not_ask_for_new_prose(self):
        result, _ = await self._call(
            self._assembly(outcome="unchanged", body_markdown="Still true.")
        )
        assert not any("write the prose" in step for step in result["progress"])

    @pytest.mark.asyncio
    async def test_an_api_error_is_surfaced_not_dressed_up_as_a_summary(self):
        """A 5xx, not the 404 this used to send: a 404 now raises rather than
        returning (`_handle_api_response`), so it could not exercise the
        "returned an error dict instead of a summary" path at all."""
        with routed(Canned(500, text="engine blew up")):
            result = await _get_scrum_summary(
                project_id="nope",
                organization_id="org-123",
                scope="scrum",
                window="3d",
                release=None,
            )
        assert "error" in result
        assert "progress" not in result


class TestSaveProjectSummary:
    """PF-398: the write half. A plain persistence call, never an LLM call."""

    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _save_project_summary(
            project_id="proj-1",
            window_spec="3d",
            summary="text",
            organization_id=None,
        )
        assert "error" in result

    async def _call(self, **kwargs):
        # Explicit for the same reason as above: a direct call gets `FieldInfo`
        # for anything omitted, never the declared default.
        kwargs.setdefault("scope", "scrum")
        kwargs.setdefault("user_id", None)
        kwargs.setdefault("items", None)
        kwargs.setdefault("source_fingerprint", None)
        kwargs.setdefault("highlights", None)
        kwargs.setdefault("concerns", None)
        kwargs.setdefault("notes", None)
        kwargs.setdefault("clear_notes", False)
        # Pre-existing omission, surfaced by
        # `test_the_payload_is_json_serialisable`: without this every test in
        # this class posted `generated_by=FieldInfo(...)`, which the httpx mock
        # happily accepted because it never serialises the body.
        kwargs.setdefault("generated_by", "agent")
        with routed(Canned(201, json={"id": "summary-1"})) as calls:
            result = await _save_project_summary(
                project_id="proj-1", organization_id="org-123", **kwargs
            )
        return result, calls

    @pytest.mark.asyncio
    async def test_posts_to_the_project_summaries_endpoint(self):
        _, calls = await self._call(window_spec="3d", summary="Shipped audit log.")
        assert calls.path() == "/api/v1/organizations/org-123/projects/proj-1/summaries"
        assert calls.body()["body_markdown"] == "Shipped audit log."

    @pytest.mark.asyncio
    async def test_a_note_is_forwarded_when_the_person_gave_one(self):
        _, calls = await self._call(
            window_spec="3d", summary="x", notes="Ken is out until Thursday."
        )
        assert calls.body()["notes_markdown"] == "Ken is out until Thursday."

    @pytest.mark.asyncio
    @pytest.mark.parametrize("blank", ["", "   ", None])
    async def test_a_blank_note_is_omitted_rather_than_clearing(self, blank):
        """`""` deletes a note at the API. An LLM emits `""` for an empty
        optional string all the time, so the destructive reading must not be
        reachable that way -- blank means "say nothing about notes", which
        inherits.
        """
        _, calls = await self._call(window_spec="3d", summary="x", notes=blank)
        assert "notes_markdown" not in calls.body()

    @pytest.mark.asyncio
    async def test_clearing_takes_the_explicit_flag(self):
        _, calls = await self._call(window_spec="3d", summary="x", clear_notes=True)
        assert calls.body()["notes_markdown"] == ""

    @pytest.mark.asyncio
    async def test_an_unresolved_field_default_does_not_clear(self):
        """`FieldInfo` is truthy, and this tool has already leaked one.

        `generated_by` shipped that way unnoticed for the life of this class.
        On a flag whose only job is deleting somebody's words, "probably a
        bool" is not good enough — hence `is True` rather than truthiness.
        """
        from pydantic.fields import FieldInfo

        _, calls = await self._call(
            window_spec="3d", summary="x", clear_notes=FieldInfo(default=False)
        )
        assert "notes_markdown" not in calls.body()

    @pytest.mark.asyncio
    async def test_a_note_sent_with_clear_is_refused_not_resolved(self):
        """ "Replace my note with X" reasonably produces both flags.

        Letting `clear` win would delete the old note, drop the replacement,
        and return success — the worst of the three outcomes and invisible to
        whoever asked. Refusing is the only honest answer on a destructive path.
        """
        result, calls = await self._call(
            window_spec="3d", summary="x", notes="the new text", clear_notes=True
        )
        assert "error" in result
        # Refused before the request: nothing was sent at all.
        assert calls.requests == []

    @pytest.mark.asyncio
    async def test_the_payload_is_json_serialisable(self):
        """Guards the FieldInfo trap this helper's own comment warns about.

        Every optional parameter needs a `setdefault` here or a direct call
        receives `FieldInfo` and posts it. The old blanket httpx mock never
        serialised the body, so such a payload looked fine until something real
        did; the routed transport serialises for real, so a leaked `FieldInfo`
        now fails at request time rather than here. This stays as the assertion
        that names *why*.
        """
        import json as _json

        _, calls = await self._call(window_spec="3d", summary="x")
        _json.dumps(calls.body())

    @pytest.mark.asyncio
    async def test_the_window_spec_is_sent_exactly_as_given(self):
        """It is the cache key -- a re-spelling writes a summary nothing reads back."""
        _, calls = await self._call(window_spec="12h", summary="x")
        assert calls.body()["window_spec"] == "12h"

    @pytest.mark.asyncio
    async def test_the_fingerprint_round_trips(self):
        fingerprint = {"commits": ["abc"], "tickets": [["1", "todo", ""]]}
        _, calls = await self._call(
            window_spec="3d", summary="x", source_fingerprint=fingerprint
        )
        assert calls.body()["source_fingerprint"] == fingerprint

    @pytest.mark.asyncio
    async def test_team_scope_carries_no_user_id_at_all(self):
        """user_id IS NULL is what makes a summary the team roll-up."""
        _, calls = await self._call(window_spec="3d", summary="x")
        assert calls.body()["summary_type"] == "scrum"
        assert "user_id" not in calls.body()

    @pytest.mark.asyncio
    async def test_personal_scope_names_the_person(self):
        _, calls = await self._call(
            window_spec="3d", summary="x", scope="me", user_id="user-abc"
        )
        assert calls.body()["summary_type"] == "personal"
        assert calls.body()["user_id"] == "user-abc"

    @pytest.mark.asyncio
    async def test_personal_scope_without_a_user_id_is_refused_not_forwarded(self):
        """The defect this closes: `scope='me'` with no `user_id` posted
        ``summary_type=personal, user_id=None``, and `user_id IS NULL` is
        exactly what the *team* roll-up means -- so every personal summary was
        stored as the team's. The personal cache gate then never hit and
        ``summaries/latest?user_id=me`` could never find the row just written.

        No test at any layer exercised `scope='me'` on this tool: `_call`
        hardcoded ``scope='scrum'``.
        """
        result, calls = await self._call(
            window_spec="3d", summary="x", scope="me", user_id=None
        )
        assert "error" in result
        assert "user_id" in result["error"]
        # Refused before the request, not after: nothing was posted at all.
        assert calls.requests == []

    @pytest.mark.asyncio
    async def test_per_ticket_prose_is_carried_through(self):
        items = [{"ticket_id": 7, "body_markdown": "Still in review."}]
        _, calls = await self._call(window_spec="3d", summary="x", items=items)
        assert calls.body()["items"] == items

    @pytest.mark.asyncio
    async def test_never_touches_claude_api(self):
        with patch("src.api.claude_api.ClaudeAPI") as mock_claude_cls:
            await self._call(window_spec="3d", summary="x")
            mock_claude_cls.assert_not_called()


class TestGetAssignmentSummary:
    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _get_assignment_summary(
            project_id="proj-1", organization_id=None
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_groups_open_tickets_by_assignee(self):
        tickets = [
            {
                "id": 1,
                "summary": "A",
                "status": "in progress",
                "assignee": "alice",
                "url": None,
            },
            {
                "id": 2,
                "summary": "B",
                "status": "todo",
                "assignee": "alice",
                "url": None,
            },
            {
                "id": 3,
                "summary": "C",
                "status": "in review",
                "assignee": "bob",
                "url": None,
            },
            {"id": 4, "summary": "D", "status": "todo", "assignee": None, "url": None},
            {
                "id": 5,
                "summary": "E (done, excluded)",
                "status": "done",
                "assignee": "alice",
                "url": None,
            },
        ]

        with routed(Canned(json=tickets)) as calls:
            result = await _get_assignment_summary(
                project_id="proj-1", organization_id="org-123"
            )

        assert calls.path() == ("/api/v1/organizations/org-123/projects/proj-1/tickets")
        assert result["assignee_counts"]["alice"] == 2
        assert result["assignee_counts"]["bob"] == 1
        assert result["assignee_counts"]["unassigned"] == 1
        assert result["total_open"] == 4


class TestGetBoardSummaryData:
    """HS-297: fetches raw structured summary data -- no Anthropic call.

    Replaces the old `summarize_board` behavior, which called Anthropic
    server-side. This tool only calls the new data-only backend endpoint;
    the calling Claude Code session is responsible for writing the actual
    summary text from the returned data.
    """

    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _get_board_summary_data(board_id="board-1", organization_id=None)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_fetches_structured_data_via_get(self):
        mcp_module.config.organization_id = "org-123"
        mcp_module.config.user_id = "user-abc"

        data = Canned(
            json={
                "board_name": "Test Board",
                "summary_type": "status",
                "stats": {"total_tickets": 3, "in_progress": 1},
                "active_tickets": [],
                "recent_completions": [],
                "messages": ["Board: Test Board"],
                "prompt": "Analyze the board...",
            }
        )

        with routed(data) as calls:
            result = await _get_board_summary_data(
                board_id="board-1",
                organization_id=None,
                summary_type="status",
                since_version=None,
                github_org=None,
            )

        # Data-fetch tool must use GET, never POST -- there is no side effect and
        # no Anthropic call in this step. The route table only serves GET on
        # summary-data, so a POST would come back 405 rather than succeed.
        assert calls.last.method == "GET"
        assert calls.path() == (
            "/api/v1/organizations/org-123/boards/board-1/summary-data"
        )
        assert calls.params() == {"summary_type": "status"}
        assert result["stats"]["total_tickets"] == 3
        assert "prompt" in result
        assert "messages" in result

    @pytest.mark.asyncio
    async def test_never_touches_claude_api(self):
        """Regression guard: this tool must never call ClaudeAPI/summarize_conversation."""
        mcp_module.config.organization_id = "org-123"
        mcp_module.config.user_id = "user-abc"

        data = Canned(json={"stats": {}, "messages": [], "prompt": ""})

        with routed(data):
            with patch("src.api.claude_api.ClaudeAPI") as mock_claude_cls:
                await _get_board_summary_data(
                    board_id="board-1",
                    organization_id=None,
                    summary_type="status",
                    since_version=None,
                    github_org=None,
                )
                mock_claude_cls.assert_not_called()


class TestSaveBoardSummary:
    """HS-297: persists a Claude-Code-written summary via the new endpoint."""

    @pytest.mark.asyncio
    async def test_returns_error_when_no_org_id(self):
        mcp_module.config.organization_id = None
        result = await _save_board_summary(
            board_id="board-1",
            summary_type="status",
            summary="Some summary text",
            organization_id=None,
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_posts_summary_to_persistence_endpoint(self):
        mcp_module.config.organization_id = "org-123"
        mcp_module.config.user_id = "user-abc"

        saved = Canned(
            json={
                "id": "summary-1",
                "summary": "Written by Claude Code",
                "stats": {"total_tickets": 3},
                "motivational_message": "Nice work!",
            }
        )

        # `highlights`/`concerns` spelled out: the tool adds any value that is
        # `not None`, so an omitted one would put a `FieldInfo` in the body --
        # which the routed transport, unlike the old mock, actually serialises.
        with routed(saved) as calls:
            result = await _save_board_summary(
                board_id="board-1",
                summary_type="status",
                summary="Written by Claude Code",
                organization_id=None,
                stats={"total_tickets": 3},
                highlights=None,
                concerns=None,
            )

        assert calls.path() == (
            "/api/v1/organizations/org-123/boards/board-1/summaries"
        )
        assert calls.body()["summary"] == "Written by Claude Code"
        assert calls.body()["summary_type"] == "status"
        assert calls.body()["stats"] == {"total_tickets": 3}
        assert result["summary"] == "Written by Claude Code"

    @pytest.mark.asyncio
    async def test_never_touches_claude_api(self):
        mcp_module.config.organization_id = "org-123"
        mcp_module.config.user_id = "user-abc"

        with routed(Canned(json={"id": "summary-1"})):
            with patch("src.api.claude_api.ClaudeAPI") as mock_claude_cls:
                await _save_board_summary(
                    board_id="board-1",
                    summary_type="status",
                    summary="text",
                    organization_id=None,
                    stats=None,
                    highlights=None,
                    concerns=None,
                )
                mock_claude_cls.assert_not_called()


class TestSetupOrgWithEnvSlugValidation:
    """setup_org_with_env uses `slug` as a filename (env/orgs/<slug>); a slug
    that isn't a plain org alias must be rejected BEFORE any state is created,
    so it can't traverse out of env/orgs/ or otherwise write to an unexpected
    path."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "bad_slug",
        ["../etc", "a/b", "..", "ACME", "a_b", "x.y", "", "-lead", "has space"],
    )
    async def test_rejects_unsafe_slug_before_any_api_call(self, bad_slug):
        with routed(Canned(201, json={"id": "org-1"})) as calls:
            result = await _setup_org_with_env(
                slug=bad_slug,
                org_name="Acme",
                project_name="Proj",
                project_alias="PF",
                board_type="skip",
            )
        # Rejected early: an error is returned and NO HTTP client was opened.
        assert "error" in result
        assert "slug" in result["error"].lower()
        calls.constructor.assert_not_called()
        assert calls.requests == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize("good_slug", ["acme", "pf", "pf-1", "a1b2"])
    async def test_accepts_valid_slug(self, good_slug):
        # A valid slug passes validation and proceeds to open the client (which
        # we stub to fail fast on the first POST, proving we got past the guard
        # without needing a real API or touching the filesystem).
        with patch("httpx.AsyncClient", side_effect=RuntimeError("reached-api")):
            with pytest.raises(RuntimeError, match="reached-api"):
                await _setup_org_with_env(
                    slug=good_slug,
                    org_name="Acme",
                    project_name="Proj",
                    project_alias="PF",
                    board_type="skip",
                )


class TestSetupOrgWithEnvPartialStatus:
    """When board registration fails but the org/project were created, the
    result must be flagged partial -- a caller must not read the populated
    summary as full success and go straight to sync_all_boards."""

    @pytest.mark.asyncio
    async def test_board_failure_yields_partial_status(self, tmp_path, monkeypatch):
        mcp_module.config.user_id = "user-abc"
        # Run in a temp cwd so env/orgs/<slug> is written under it, not the repo.
        monkeypatch.chdir(tmp_path)

        # org create OK, project create OK, board register FAILS (500) -- in
        # order, and each against a path the route table has to serve.
        responses = [
            Canned(201, json={"id": "org-1"}),
            Canned(201, json={"id": "proj-1"}),
            Canned(500, text="boom"),
        ]
        with routed(responses) as calls:
            # Pass every optional arg explicitly: calling the tool's raw .fn
            # bypasses pydantic, so an omitted arg stays a Field() sentinel
            # (truthy) rather than defaulting to None.
            result = await _setup_org_with_env(
                slug="acme",
                org_name="Acme",
                project_name="Proj",
                project_alias="PF",
                board_type="linear",
                board_url="https://linear.app/acme",
                board_api_token="lin_api_xxx",
                board_api_email=None,
                board_name=None,
                github_org=None,
                github_topic=None,
                user_id=None,
                organization_id=None,
            )

        assert result["status"] == "partial"
        assert result["summary"]["status"] == "partial"
        assert result["summary"]["board_id"] is None
        assert "board_warning" in result
        assert "register_board" in result["summary"]["next_step"]
        assert calls.paths() == [
            "/api/v1/organizations",
            "/api/v1/organizations/org-1/projects",
            "/api/v1/organizations/org-1/boards",
        ]

    @pytest.mark.asyncio
    async def test_env_file_permissions_restricted(self, tmp_path, monkeypatch):
        """The env file holds a cleartext credential; it must be owner-only."""
        import os
        import stat

        mcp_module.config.user_id = "user-abc"
        monkeypatch.chdir(tmp_path)

        responses = [
            Canned(201, json={"id": "org-1"}),
            Canned(201, json={"id": "proj-1"}),
            Canned(201, json={"id": "board-1"}),
        ]
        with routed(responses):
            result = await _setup_org_with_env(
                slug="acme",
                org_name="Acme",
                project_name="Proj",
                project_alias="PF",
                board_type="linear",
                board_url="https://linear.app/acme",
                board_api_token="lin_api_xxx",
                board_api_email=None,
                board_name=None,
                github_org=None,
                github_topic=None,
                user_id=None,
                organization_id=None,
            )

        env_file = tmp_path / "env" / "orgs" / "acme"
        assert env_file.is_file()
        assert "BOARD_API_TOKEN=lin_api_xxx" in env_file.read_text()
        mode = stat.S_IMODE(os.stat(env_file).st_mode)
        assert mode == 0o600, f"expected 0600, got {oct(mode)}"
        assert result["status"] == "ok"


class TestUpdateTicketUsesApiPut:
    """update_ticket must route through _API.put (fresh api_url + timeout),
    not a hand-rolled timeout-less httpx call."""

    @pytest.mark.asyncio
    async def test_routes_through_api_put(self):
        mcp_module.config.user_id = "user-abc"
        mcp_module.config.organization_id = "org-123"
        with patch.object(
            mcp_module._api,
            "put",
            AsyncMock(return_value={"id": "t-1", "status": "DONE"}),
        ) as mock_put:
            result = await _update_ticket(
                ticket_id="t-1",
                status="DONE",
                assignee=None,
                summary=None,
                description=None,
                release=None,
                organization_id=None,
                project_id=None,
            )
        mock_put.assert_awaited_once()
        # path is the tickets endpoint; body carries the changed field
        call = mock_put.await_args
        assert "/tickets/t-1" in call.args[0]
        assert call.kwargs["json"]["status"] == "DONE"
        assert result["id"] == "t-1"

    @pytest.mark.asyncio
    async def test_no_fields_returns_error_without_calling_put(self):
        mcp_module.config.organization_id = "org-123"
        # Every optional field explicitly None (the raw .fn bypasses pydantic's
        # Field() defaults), so update_data is genuinely empty.
        with patch.object(mcp_module._api, "put", AsyncMock()) as mock_put:
            result = await _update_ticket(
                ticket_id="t-1",
                status=None,
                assignee=None,
                summary=None,
                description=None,
                release=None,
                organization_id=None,
                project_id=None,
            )
        assert "error" in result
        mock_put.assert_not_called()


class TestCreateTicketRelease:
    """`create_ticket` had no `release` parameter at all, so an agent could set a
    ticket's release only by creating it and then updating it. The API validates
    the value, so nothing is checked here -- the 422 body is what the agent reads.
    """

    @pytest.mark.asyncio
    async def test_release_is_forwarded_in_the_post_body(self):
        mcp_module.config.organization_id = "org-123"
        with patch.object(
            mcp_module._api, "post", AsyncMock(return_value={"id": 1})
        ) as mock_post:
            await _create_ticket(
                summary="Fix the closer",
                description=None,
                status="TODO",
                assignee=None,
                release="v1.11.0",
                organization_id=None,
                project_id="proj-1",
            )
        assert mock_post.await_args.kwargs["json"]["release"] == "v1.11.0"

    @pytest.mark.asyncio
    async def test_the_key_is_absent_when_no_release_is_given(self):
        mcp_module.config.organization_id = "org-123"
        with patch.object(
            mcp_module._api, "post", AsyncMock(return_value={"id": 1})
        ) as mock_post:
            await _create_ticket(
                summary="No release",
                description=None,
                status="TODO",
                assignee=None,
                release=None,
                organization_id=None,
                project_id="proj-1",
            )
        assert "release" not in mock_post.await_args.kwargs["json"]

    def test_both_tool_descriptions_point_the_agent_at_the_option_list(self):
        """An agent that cannot see the vocabulary can only guess at it; the 422
        then costs a turn. `list_releases` is where the options are."""
        for tool in (mcp_module.create_ticket, mcp_module.update_ticket):
            text = inspect.getdoc(tool) or ""
            assert "outstanding" in text.lower(), tool.__name__
            assert "list_releases" in text, tool.__name__


class TestApiErrorContract:
    """`_API`'s four failure kinds, and the two stale paths #652 found.

    Every non-200 used to become `{"error": ...}` and return as a *successful*
    tool result, so a 404 from a URL no route serves read exactly like the route
    refusing the request on its merits -- which is how `sync_repository` POSTed
    to a nonexistent path for months. These pin the distinction, and they pin it
    through the routed transport: a stale path 404s on its own there, with
    nothing canned, so the two regression tests below cannot pass against the
    old paths.
    """

    @pytest.mark.asyncio
    async def test_a_404_raises_rather_than_returning(self):
        """Nothing is canned for the 404 -- the route table produces it, which is
        the mechanism this whole file now rests on."""
        with routed(Canned(json={})) as calls:
            with pytest.raises(ToolError) as raised:
                await mcp_module._api.get("/api/v1/organizations/org-123/nope")

        assert "404" in str(raised.value)
        assert "/api/v1/organizations/org-123/nope" in str(raised.value)
        assert calls.paths() == ["/api/v1/organizations/org-123/nope"]

    @pytest.mark.asyncio
    async def test_a_transport_failure_raises(self):
        """A raw `httpx.ConnectError` reached the MCP client as a traceback; it is
        a message now, but still an error rather than a result."""

        def refuse(request):
            raise httpx.ConnectError("connection refused")

        with routed(refuse):
            with pytest.raises(ToolError) as raised:
                await mcp_module._api.get("/api/v1/public/status")

        assert "Could not reach the InnoDay API" in str(raised.value)
        assert "connection refused" in str(raised.value)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [400, 403, 409])
    async def test_a_4xx_refusal_returns_labelled_refused(self, status):
        """These are the route answering about the request's content. Eleven call
        sites branch on `"error" in result` and some act on a 4xx, so they must
        keep returning -- labelled, which is what was missing."""
        with routed(Canned(status, text="nope")) as calls:
            result = await mcp_module._api.post(
                "/api/v1/organizations/org-123/releases", json={"version": "v1.0.0"}
            )

        assert result["error_kind"] == "refused"
        assert result["status"] == status
        assert result["method"] == "POST"
        assert result["path"] == calls.path()
        assert "error" in result

    @pytest.mark.asyncio
    async def test_a_5xx_returns_labelled_server_error(self):
        with routed(Canned(500, text="boom")) as calls:
            result = await mcp_module._api.get("/api/v1/organizations/org-123/work")

        assert result["error_kind"] == "server_error"
        assert result["status"] == 500
        assert result["method"] == "GET"
        assert result["path"] == calls.path()

    @pytest.mark.asyncio
    async def test_a_real_path_with_the_wrong_method_is_405_not_404(self):
        """`…/tickets/refresh` is why matching has to be by regex: the literal
        `refresh` is absorbed by `{ticket_id}`, so a stale path of that shape is
        a 405. A 405 is not the 404 contract -- it returns, labelled."""
        with routed(Canned(json={})) as calls:
            result = await mcp_module._api.post(
                "/api/v1/organizations/org-123/tickets/refresh"
            )

        assert result["status"] == 405
        assert result["error_kind"] == "refused"
        assert calls.paths() == ["/api/v1/organizations/org-123/tickets/refresh"]

    @pytest.mark.asyncio
    async def test_sync_repository_reaches_a_path_a_route_serves(self):
        """The #652 regression, pinned at the boundary that used to hide it.

        `…/repositories/{id}/sync` has never been served by any route, and neither
        is the `…/github-registrations/{id}/sync` it was corrected to -- #658
        deleted that route with the org-wide import behind it. Under the routed
        transport both 404, and the 404 contract raises, so this cannot pass against
        either old path.

        `github_label` travels in the **query string**, because the discover route
        declares it with `Query(...)` and takes no body at all -- and FastAPI drops
        an undeclared body silently, so a JSON `github_label` would have been
        ignored and the project's alias used instead.
        """
        with routed(Canned(json={"status": "completed", "repositories_synced": 3})) as (
            calls
        ):
            result = await _sync_repository(
                project_id="proj-1", organization_id="org-123", github_label="pf"
            )

        assert calls.last.method == "POST"
        assert calls.path() == (
            "/api/v1/organizations/org-123/projects/proj-1/repositories/discover"
        )
        assert calls.params() == {"github_label": "pf"}
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_analyze_temporal_patterns_posts_to_the_analyze_route(self):
        """`/api/v1/ai/analyze-temporal` never existed. The temporal analysis
        lives behind `POST /api/v1/ai/analyze`, which branches on
        `analysis_type`, and that route's model names the body keys -- so the
        window is words rather than a bare number.
        """
        messages = [{"content": "shipped the guard", "timestamp": "2026-08-15T09:00"}]

        with routed(Canned(json={"analysis": "steady"})) as calls:
            result = await _analyze_temporal_patterns(
                messages=messages, window_hours=12
            )

        assert calls.last.method == "POST"
        assert calls.path() == "/api/v1/ai/analyze"
        assert calls.body() == {
            "data": messages,
            "analysis_type": "temporal",
            "time_window": "12 hours",
        }
        assert result["analysis"] == "steady"
