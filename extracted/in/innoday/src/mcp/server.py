"""
InnoDay MCP Server

Provides Model Context Protocol integration for InnoDay platform,
enabling Claude Code and VS Code extensions to interact with InnoDay's
repository, ticket, and board management systems.
"""

import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, Field

from src.cli.config import DEFAULT_API_URL, CLIConfig

# The status vocabulary's single source of truth. Imported rather than
# restated so the tool descriptions cannot drift from the enum the API
# validates against -- the drift is what GH #630 was.
from src.domain.ticket import TicketStatus

# Writes to **stderr**, never stdout. In stdio mode stdout is the MCP protocol
# channel, so a stray print corrupts the framing -- this logger is left
# unconfigured on purpose, which sends it to `logging.lastResort` (stderr,
# WARNING and above) rather than to any handler the API process installs.
logger = logging.getLogger(__name__)


class InnoConfig(BaseModel):
    """Configuration for InnoDay MCP server"""

    # The last resort, and only that. `load_config()` fills this from the CLI
    # config the same way it fills the token and the team secret, so the value
    # here is reached only when constructing a `CLIConfig` raised outright --
    # a process with no identity either, which is going to fail at the first
    # call whatever URL it holds.
    #
    # It stays `DEFAULT_API_URL` rather than localhost so that the three ways
    # to answer "where is InnoDay" cannot disagree. Until #731 they did:
    # `load_config()` read five things from `CLIConfig` and never
    # `get_api_url()`, so `innoday config set api-url` moved the CLI and left
    # MCP behind -- and this field, not the config, was the effective URL.
    api_url: str = Field(default=DEFAULT_API_URL, description="InnoDay API URL")
    organization_id: Optional[str] = Field(
        default=None, description="Default organization ID"
    )
    project_id: Optional[str] = Field(default=None, description="Default project ID")
    user_id: Optional[str] = Field(default=None, description="Default user ID")
    cli_token: Optional[str] = Field(
        default=None,
        description="User API token sent as Authorization: Bearer — the identity",
    )
    team_secret: Optional[str] = Field(
        default=None, description="Team access secret sent as X-Team-Secret"
    )
    verbose: bool = Field(default=False, description="Enable verbose logging")


def build_cli_config(allow_legacy_context: bool = False) -> CLIConfig:
    """The CLIConfig this server reads identity and cwd context from.

    **Constructed once.** This used to build a throwaway ``CLIConfig()`` purely
    to peek at ``default_profile``, then build the real one -- so every
    construction-time side effect ran twice, on *every* MCP tool call
    (``get_config()`` reloads per call). On stdio transport anything a
    construction writes to stdout corrupts the JSON-RPC stream, and #610's
    config purge did exactly that before its notices moved to stderr (#611).

    ``default_profile`` must still win over ``current_profile`` -- MCP contexts
    must not follow whatever an unrelated interactive ``config profile use``
    last set, and ``_resolve_profile`` ranks ``current_profile`` first. Hence
    the rebuild below, which happens only when the two pointers genuinely
    disagree: a rebuild for a different profile, never a peek.

    ``detect_cwd_context=True`` mirrors the CLI's own resolution
    (``src/cli/main.py``'s ``execute_command``): the cwd's
    ``.innoday/project.yml`` is the primary source of org/project context, and
    Claude Code spawns this server with the cwd the user launched it from.
    """
    cli_config = CLIConfig(
        detect_cwd_context=True, allow_legacy_context=allow_legacy_context
    )
    default_profile = cli_config.get_default_profile()
    if (
        default_profile
        and default_profile != cli_config.get_current_profile()
        and default_profile in cli_config.list_profiles()
    ):
        cli_config = CLIConfig(
            profile=default_profile,
            detect_cwd_context=True,
            allow_legacy_context=allow_legacy_context,
        )
    return cli_config


def load_config() -> InnoConfig:
    """Load configuration from CLI config or environment"""
    config = InnoConfig()

    # Try to load from CLI config first (~/.innoday/config.json).
    try:
        # allow_legacy_context: the MCP server must never hard-exit on an
        # outdated .innoday/project.yml (it runs long-lived and callers can pass
        # org/project explicitly) — it just proceeds without cwd context.
        cli_config = build_cli_config(allow_legacy_context=True)
        # Where InnoDay is, from the same file the CLI reads it from (#731).
        # Without this the MCP server had no way to learn the configured URL:
        # the field default above was the effective address and only
        # `INNODAY_API_URL` could move it, so `innoday config set api-url`
        # pointed the CLI somewhere and silently left MCP where it was. Every
        # "the CLI works but MCP 401s / shows different data" report starts
        # there.
        api_url = cli_config.get_api_url()
        if api_url:
            config.api_url = api_url
        user_id = cli_config.get_user_id()
        if user_id:
            config.user_id = user_id
        org_alias = cli_config.get_current_organization()
        if org_alias:
            org_id = cli_config.get_organization_id(org_alias)
            if org_id:
                config.organization_id = org_id
        project_id = cli_config.get_current_project_id()
        if project_id:
            config.project_id = project_id
        team_secret = cli_config.get_team_secret()
        if team_secret:
            config.team_secret = team_secret
        # The user API token — same keyring/config the CLI reads. This is the
        # identity; X-User-ID is not sent any more.
        cli_token = cli_config.get_cli_token()
        if cli_token:
            config.cli_token = cli_token
    except Exception:
        pass

    # Override with environment variables if present. Org/project context is
    # NOT included here -- .innoday/project.yml (via detect_cwd_context above)
    # is the sole resolution mechanism, matching the CLI; pass organization_id/
    # project_id explicitly to a tool call to override for that one call
    # instead of a standing env var that silently shadows cwd resolution.
    if os.getenv("INNODAY_API_URL"):
        config.api_url = os.getenv("INNODAY_API_URL")
    if os.getenv("INNODAY_USER_ID"):
        config.user_id = os.getenv("INNODAY_USER_ID")
    if os.getenv("INNODAY_TEAM_SECRET"):
        config.team_secret = os.getenv("INNODAY_TEAM_SECRET")
    if os.getenv("INNODAY_TOKEN"):
        config.cli_token = os.getenv("INNODAY_TOKEN")

    return config


# Initialize configuration. This module-level `config` is a live snapshot,
# refreshed by get_config() below rather than frozen at import -- the MCP
# server is a long-lived process, and ~/.innoday/config.json can change under
# it (e.g. `innoday config set team-secret`, a fresh install populating the
# profile after the server already started). Reading it only once at import
# meant a config update never took effect without `/mcp reconnect`, which was
# the recurring cause of `401 Missing or invalid X-Team-Secret` from MCP tools
# even when the CLI (which re-reads config every invocation) worked fine.
config = load_config()


def get_config() -> InnoConfig:
    """Return the current config, re-reading it from disk each call so a
    long-lived MCP process picks up config changes (identity, team_secret,
    cwd project context) without needing to be restarted. Updates the
    module-level `config` in place so any lingering references stay current."""
    global config
    config = load_config()
    return config


def get_user_headers() -> Dict[str, str]:
    """Request headers for every call to the InnoDay API.

    Identity is the **user API token** on `Authorization: Bearer`, exactly as the
    CLI sends it (src/cli/client.py). This server used to send `X-User-ID`
    instead -- a bare, unverified assertion of who the caller is, which meant
    anyone holding the shared team secret could name any user id and be treated
    as them. It was the last consumer of that path.

    `X-Team-Secret` is still sent when configured: it is a deployment door key,
    not identity, and is orthogonal to the token.

    Raises if no token resolves, rather than silently degrading to an
    unauthenticated (or impersonating) request.
    """
    cfg = get_config()
    if not cfg.cli_token:
        raise ValueError(
            "No InnoDay API token configured. Run `innoday login` "
            "(or set INNODAY_TOKEN)."
        )
    headers = {"Authorization": f"Bearer {cfg.cli_token}"}
    if cfg.team_secret:
        headers["X-Team-Secret"] = cfg.team_secret
    return headers


def user_headers_or_error(what: str):
    """``(headers, None)`` or ``(None, {"error": ...})`` for a tool that used to
    resolve its credential some other way.

    `get_user_headers` raises, which is the right contract for a helper. But an
    MCP tool that raises is a *protocol-level* failure -- the caller sees a
    transport error rather than a message it can act on -- and every other
    failure in these tools returns `{"error": ...}`. The three sync tools that
    #611 moved onto this helper had a dict on their credential-missing path
    before, so raising was a change they did not need; `register_board`'s new
    error path (a dict) is the shape to match.
    """
    try:
        return get_user_headers(), None
    except ValueError as exc:
        return None, {"error": f"{what}: {exc}"}


# How a *returned* API failure describes itself. Every non-200 used to become
# `{"error": ...}` and come back as a **successful** tool result, so a 404 from a
# stale URL was indistinguishable from the route refusing the request on its merits.
# That is how this server's POST to `…/repositories/{id}/sync` -- a path no route has
# ever served -- survived long enough to be found by an audit rather than by a user
# (#652).
#
# **There are deliberately only two.** A transport failure and a 404 are not kinds of
# returned failure at all: they raise `ToolError` and never reach a payload, so a
# `"transport"` or `"not_found"` constant would name a value nothing can ever
# produce. Two such constants were written here and were dead the moment the raising
# branches went in; a name for a state the code cannot enter is the beginning of
# believing it can.
ERROR_SERVER = "server_error"
ERROR_REFUSED = "refused"


def _api_failure(
    kind: str,
    message: str,
    *,
    method: str,
    path: str,
    status: Optional[int] = None,
    details: str = "",
) -> Dict[str, Any]:
    """The shape a failed API call reports itself in.

    `error` stays first and keeps its name because eleven call sites in this
    module branch on `"error" in result`. Everything else is added information:
    `error_kind` says *which kind* of failure, and `method`/`path` make a wrong
    URL visible in the result itself instead of requiring a server-side log.
    """
    payload: Dict[str, Any] = {
        "error": message,
        "error_kind": kind,
        "method": method,
        "path": path,
    }
    if status is not None:
        payload["status"] = status
    if details:
        payload["details"] = details
    return payload


def _handle_api_response(
    response: httpx.Response,
    *,
    method: str,
    path: str,
    ok: tuple = (200,),
) -> Any:
    """Decode a successful response, or report the failure honestly.

    Which failures raise and which return is a deliberate split:

    * **404 raises `ToolError`.** A 404 is not a decision the route made about
      the request's content -- either the path is wrong or the entity is gone --
      and returning it as a dict made it a *successful* tool result. `ToolError`
      is FastMCP's message-only error: the client is shown the text, never a
      traceback, so this does not start putting stack traces in front of users.
    * **Everything else returns a dict.** A 4xx refusal or a 5xx is the route
      answering; several tools here branch on `"error" in result` and some
      legitimately act on a 4xx, so converting those to exceptions would change
      behaviour far beyond the bug. They are still labelled, which is what was
      missing -- `error_kind` and `status` distinguish a refusal from a 500.

    Transport failures are handled by `_request` below, which never reaches here.
    """
    if response.status_code in ok:
        return response.json()
    if response.status_code == 404:
        # Logged as well as raised. The raise tells whoever made this call; the log
        # is what makes the *class* findable, because the overwhelmingly likely cause
        # is a client-side path this server builds wrongly for everyone, not a
        # missing entity for one caller. Nothing logged a 404 before, which is the
        # other half of why a permanently-404ing tool went unnoticed for months.
        logger.warning(
            "MCP client route defect or missing entity: %s %s returned 404",
            method,
            path,
        )
        raise ToolError(
            f"{method} {path} returned 404. Either no route serves that path "
            f"(a client bug) or the entity does not exist. Body: {response.text[:500]}"
        )
    kind = ERROR_SERVER if response.status_code >= 500 else ERROR_REFUSED
    return _api_failure(
        kind,
        f"API error {response.status_code}",
        method=method,
        path=path,
        status=response.status_code,
        details=response.text,
    )


def _project_context(project_dir: Optional[str]) -> Optional[Dict[str, Any]]:
    """The org and project a directory belongs to, from its `.innoday/project.yml`.

    The same file the CLI reads for `--dir`, so a tool call and a shell command
    pointed at one workspace resolve identically. Returns None -- never raises --
    when the directory has no project file or the file cannot be read: a bad
    hint should fall through to the configured default, not fail the call.
    """
    if not project_dir:
        return None
    try:
        from src.cli.utils.project_context import load_project_context

        return load_project_context(Path(project_dir))
    except Exception as exc:  # noqa: BLE001 - a hint is never worth the call
        logger.warning("Could not read a project context from %s: %s", project_dir, exc)
        return None


class _API:
    """Thin httpx wrapper for MCP tools — centralises org resolution and request pattern."""

    @staticmethod
    def resolve_org(
        organization_id: Optional[str], project_dir: Optional[str] = None
    ) -> Optional[str]:
        """The organization to act in: explicit, then `project_dir`, then config.

        **`project_dir` before config, and this ordering is the whole point.**
        The config's organization comes from wherever this server was started,
        which for a long-lived MCP server is one directory forever. Ask it about
        a project in a different organization and it answers with the wrong one
        -- and because the project id *was* right, the request reaches the API
        looking well-formed and is refused with "Project belongs to a different
        organization", which reads as a permissions problem rather than a
        resolution one.
        """
        if organization_id:
            return organization_id
        context = _project_context(project_dir)
        if context and context.get("org_id"):
            return context["org_id"]
        return get_config().organization_id

    @staticmethod
    def resolve_project(
        project_id: Optional[str], project_dir: Optional[str] = None
    ) -> Optional[str]:
        """The project to act on: explicit, then `project_dir`, then config."""
        if project_id:
            return project_id
        context = _project_context(project_dir)
        if context and context.get("project_id"):
            return context["project_id"]
        return get_config().project_id

    # Read the API URL via get_config() (fresh per call) rather than the stale
    # module-global `config` -- the header/org resolution above already resolves
    # fresh, and the URL must never diverge from the identity the request is
    # made under (e.g. after `innoday config set api-url` under a long-lived
    # server). Every raw-httpx tool below follows the same rule.
    @staticmethod
    async def _request(
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        ok: tuple = (200,),
    ) -> Any:
        """One request, with transport failure and 404 raised rather than returned.

        `httpx.RequestError` (connect refused, DNS, timeout) used to propagate out
        of these helpers as a raw exception, so the MCP client saw an
        `httpx.ConnectError` traceback. `ToolError` carries the same information
        as a message the caller can act on.
        """
        url = f"{get_config().api_url}{path}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method,
                    url,
                    headers=get_user_headers(),
                    params=params or {},
                    json=json,
                    timeout=30.0,
                )
        except httpx.RequestError as exc:
            logger.warning(
                "MCP could not reach the InnoDay API: %s %s (%s)",
                method,
                url,
                type(exc).__name__,
            )
            raise ToolError(
                f"Could not reach the InnoDay API at {url} "
                f"({type(exc).__name__}: {exc}). Check `innoday status`."
            ) from exc
        return _handle_api_response(response, method=method, path=path, ok=ok)

    @staticmethod
    async def get(path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return await _API._request("GET", path, params=params)

    @staticmethod
    async def post(path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return await _API._request("POST", path, json=json or {}, ok=(200, 201))

    @staticmethod
    async def patch(path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return await _API._request("PATCH", path, json=json or {})

    @staticmethod
    async def put(path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return await _API._request("PUT", path, json=json or {})


_api = _API()

#: What a host is told before it sees a single tool name.
#:
#: **There were none.** The server offered 48 tools and no guidance, so a model
#: deciding how to answer "what shipped in this release" saw a list of names and
#: no reason to prefer them over the shell it already had. It reached for `gh`,
#: which is right there, needs no ids, and works.
#:
#: Every line below is a mistake that has actually been made against this server,
#: not a statement of principle.
_INSTRUCTIONS = """\
InnoDay is the source of truth for this team's work: projects, tickets, boards,
repositories, pull requests, releases and summaries. Ask it, and prefer a tool
here over any other way of finding out.

**Never reach for `gh`, the GitHub API, or a board's own API to answer a
question these tools cover.** Two things go wrong, and the second is worse:

1. **You will use the wrong credential.** InnoDay holds each organisation's
   GitHub credential and uses it server-side. `gh auth token` is the *person's*
   own login — a release must not be cut with someone's personal credential, and
   it carries whatever scopes that account happens to have rather than what the
   work needs. **Never export `GH_TOKEN` to make a release command run.**
2. **You will hide a defect.** Routing around a failing InnoDay call produces a
   correct-looking answer assembled outside the product, so nobody learns the
   product is broken and its own data stays stale. **A failing InnoDay call is
   the finding.** Report it. Do not work around it and present the result as
   though InnoDay produced it.

Reading GitHub directly is legitimate for exactly one thing: *verifying* what
InnoDay reported, or establishing ground truth while debugging — and say that is
what you are doing.

## Writing a summary

The server assembles; **you narrate**. No route here generates prose, so a
summary appears only because you wrote one.

1. `sync_board` / `sync_repository` — only if the data may be stale. Syncing is
   slow and a run may already be in flight.
2. `get_scrum_summary` (or `get_work_summary`, `get_board_summary_data`) — the
   assembled facts: tickets, branches, pull requests, who moved what.

   **For a release, `get_release_content` instead.** It is a different payload,
   not the same one filtered: it carries every pull request that delivered each
   ticket, what merged, what is missing, and what shipped with no ticket at all.
   `get_scrum_summary` assembles ticket *movement* and sees at most one pull
   request each, so a release narrated from it cannot say whether anything
   landed. It also reports `board_sync` — if that says stale, ask whether to
   `sync_board` before narrating, rather than syncing unprompted or writing over
   tickets that may be hours behind.
3. Write the prose yourself from exactly that payload, so the narrative and the
   numbers cannot disagree.
4. `save_project_summary` — store it, echoing back the window you were given.

## Which project you are talking about

Org and project resolve from the directory the server was launched in, which is
often **not** the project being discussed. When the conversation is about a
different project, pass `project_id` (and `organization_id`) explicitly rather
than relying on the default.
"""

# Create the MCP app
app = FastMCP("innoday-mcp", instructions=_INSTRUCTIONS)


#: The status vocabulary, derived from the enum rather than restated (GH #630).
#: `TicketStatus` member NAMES are uppercase with underscores while its VALUES are
#: lowercase with spaces ("in progress"), and these descriptions were written from
#: the names while the API validated values -- so `create_ticket`'s own default of
#: "TODO" was rejected by its own API on the simplest call the tool has. Derived
#: here so a member added or renamed cannot leave the descriptions behind.
_STATUS_NAMES = ", ".join(status.name for status in TicketStatus)


def _note_unapplied_status(result: Any, requested: Optional[str]) -> Any:
    """Say so when the status that came back is not the status that was asked for.

    **A create whose status transition fails still answers 200.** Pushing a new
    ticket to an external board is two operations -- create the issue, then
    transition it -- and the second is best-effort by design, so a board outage
    cannot cost you the ticket. But the failure was only ever written to a server
    log: the caller received a perfectly ordinary ticket, sitting in the board's
    default state, with nothing to indicate that the status it asked for had been
    dropped. That is the same "looks like it worked and did not" shape the
    `release` field carried on this path before it was fixed.

    Nothing here retries or overrides -- the board's answer stands. This only
    makes it visible, in the one place a caller reads.
    """
    if not requested or not isinstance(result, dict) or "error" in result:
        return result

    actual = result.get("status")
    if not isinstance(actual, str):
        return result

    def _canonical(value: str) -> str:
        return " ".join(
            value.strip().lower().replace("_", " ").replace("-", " ").split()
        )

    if _canonical(actual) == _canonical(requested):
        return result

    return {
        **result,
        "warning": (
            f"Status '{requested}' was not applied -- the ticket is '{actual}'. "
            "The board has no workflow state matching that name, so the issue "
            "stayed in the board's default state. Rename the state on the board, "
            "or set the status with update_ticket."
        ),
    }


# =============================================================================
# Diagnostics Tools
# =============================================================================


async def _get_assigned_tickets_count(org_id: Optional[str]) -> Optional[int]:
    """Best-effort count of tickets assigned to the configured user. Never raises.

    Filters on `assigned_to` -- the `users.id` FK. This used to pass the same
    user id as `assignee`, which is the board's display-name column, so the
    comparison was a UUID against a name and the count was always 0 (PF-398).
    """
    if not org_id or not config.user_id:
        return None
    try:
        tickets = await _api.get(
            f"/api/v1/organizations/{org_id}/tickets",
            params={"assigned_to": config.user_id, "limit": 500},
        )
        if isinstance(tickets, dict) and "error" in tickets:
            return None
        return len(tickets) if isinstance(tickets, list) else None
    except Exception:
        return None


@app.tool()
async def check_status(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Check InnoDay API connectivity and status without leaving the session.

    Calls GET /api/v1/public/status on the configured api_url and returns a
    structured report: environment, port, env_file, db_host, version,
    uptime, and (if identity is configured) the current user/org and their
    assigned ticket count. Never raises — returns {"status": "unreachable"}
    on any connection failure so a broken connection never crashes the
    MCP session.
    """
    org_id = _api.resolve_org(organization_id)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{get_config().api_url}/api/v1/public/status")
    except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError) as e:
        return {
            "status": "unreachable",
            "api_url": get_config().api_url,
            "error": str(e),
        }

    if r.status_code != 200:
        return {
            "status": "unreachable",
            "api_url": get_config().api_url,
            "error": f"API returned {r.status_code}: {r.text[:200]}",
        }

    data = r.json()

    result: Dict[str, Any] = {
        "api_url": get_config().api_url,
        "status": data.get("status"),
        "environment": data.get("environment"),
        "port": data.get("port"),
        "env_file": data.get("env_file"),
        "db_host": data.get("db_host"),
        "version": data.get("version"),
        "uptime_seconds": data.get("uptime_seconds"),
        "user_id": config.user_id,
        "organization_id": org_id,
    }

    result["assigned_tickets_count"] = await _get_assigned_tickets_count(org_id)

    return result


# =============================================================================
# Repository Management Tools
# =============================================================================


@app.tool()
async def list_repositories(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    platform_type: Optional[str] = Field(
        default=None, description="Filter by platform: github, jira_git"
    ),
    include_archived: bool = Field(
        default=False, description="Include archived repositories"
    ),
) -> Dict[str, Any]:
    """
    List all Git repositories registered with InnoDay.

    Returns repository information including sync status, issue counts,
    and archive/deletion status.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {}
    if platform_type:
        params["platform_type"] = platform_type
    if not include_archived:
        params["active_only"] = True

    result = await _api.get(
        f"/api/v1/organizations/{org_id}/repositories", params=params
    )
    if "error" in result:
        return result
    return {"repositories": result, "count": len(result), "organization_id": org_id}


@app.tool()
async def sync_repository(
    project_id: str = Field(
        description="Project whose repositories to sync — UUID, alias, or name"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    github_label: Optional[str] = Field(
        default=None,
        description=(
            "GitHub topic to search for; defaults to the project's alias, lowercased"
        ),
    ),
) -> Dict[str, Any]:
    """
    Sync a project's repositories from GitHub by topic label.

    Every repository on GitHub carrying the project's topic (its alias,
    lowercased, unless `github_label` says otherwise) is registered if new,
    relinked if it had been retired, and retired if the topic is gone. Safe to
    call repeatedly.

    **This is the only way repositories are attached to a project.** There is no
    manual link step, and InnoDay does not import every repository an
    organization owns — the topic is the whole selector.

    The org's GitHub credential is resolved server-side from Vault; no token is
    read here or sent.
    """
    # The subject used to be a `GitHubOrgRegistration`, and the route it posted to
    # walked every repository in the GitHub org (#658). That path produced 0 of 36
    # repositories in dev while topic discovery produced all 36, and it is gone --
    # so this tool takes the project whose topic selects them instead.
    #
    # It also used to read `GITHUB_TOKEN` off the MCP server's own environment and
    # send it as `x-integration-token` -- one process-wide value shared by every
    # tenant, so an org with no credential of its own silently synced on the
    # operator's (#554/#611). The endpoint resolves it with
    # `get_github_credentials` instead.
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    headers, error = user_headers_or_error("Repository sync failed")
    if error:
        return error

    path = f"/api/v1/organizations/{org_id}/projects/{project_id}/repositories/discover"
    # `github_label` is a **query** parameter, not a body field: the route declares
    # it with `Query(...)` and takes no request body at all, and FastAPI drops an
    # undeclared body silently -- so a JSON `github_label` would have been ignored
    # and the project's alias used regardless.
    params = {"github_label": github_label} if github_label else None
    # 60s, not httpx's 5s default: this searches a GitHub organization's
    # repositories server-side and then reads each match's topics.
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{get_config().api_url}{path}",
                params=params,
                headers=headers,
            )
    except httpx.RequestError as exc:
        logger.warning(
            "MCP could not reach the InnoDay API to sync repositories (%s)",
            type(exc).__name__,
        )
        raise ToolError(
            f"Could not reach the InnoDay API to sync repositories "
            f"({type(exc).__name__}: {exc}). Check `innoday status`."
        ) from exc
    return _handle_api_response(response, method="POST", path=path)


@app.tool()
async def get_repository_issues(
    registration_id: str = Field(description="Repository ID"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    status: Optional[str] = Field(
        default=None, description="Filter by status: open, closed, all"
    ),
    limit: int = Field(default=50, description="Maximum number of issues to return"),
) -> Dict[str, Any]:
    """
    Get issues for a specific repository.

    Returns repository issues with their current status, assignees,
    and other metadata.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {"limit": limit}
    if status:
        params["status"] = status

    result = await _api.get(
        f"/api/v1/organizations/{org_id}/repositories/{registration_id}/issues",
        params=params,
    )
    # Endpoint returns a bare JSON array; this tool's output schema is an
    # object, so FastMCP rejects a top-level list. Wrap it. _api.get returns
    # an {"error": ...} dict on non-200 -- pass that through unchanged.
    if isinstance(result, list):
        return {
            "issues": result,
            "count": len(result),
            "repository_id": registration_id,
        }
    return result


# =============================================================================
# Ticket Management Tools
# =============================================================================


@app.tool()
async def list_tickets(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    status: Optional[str] = Field(
        default=None,
        description=f"Filter by status: {_STATUS_NAMES}. Either spelling of a "
        "member works. If omitted, DRAFT tickets are excluded by default.",
    ),
    assignee: Optional[str] = Field(default=None, description="Filter by assignee"),
    release: Optional[str] = Field(
        default=None,
        description="Filter by version, e.g. 'v1.9.0', or 'current' for whatever "
        "the project is cutting now. Scopes the call to one project, since a "
        "version only means something within a project.",
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Scope to one project. Resolved from the launch directory when "
        "omitted. Required to use `release`.",
    ),
    limit: int = Field(default=100, description="Maximum number of tickets to return"),
) -> Dict[str, Any]:
    """
    List tickets for an organization, or for one project.

    Returns tickets with their current status, assignees, and metadata.
    DRAFT tickets are excluded unless status="DRAFT" is explicitly requested.

    `release` filters by version and **scopes the call to a single project**, because
    a version string only means something inside one: PF's v1.9.0 and BPAI's v1.9.0
    are unrelated releases that happen to share a name. Pass `current` to get
    whatever the project is cutting now without knowing the version. Both forms need
    a project — resolved from the launch directory, or passed explicitly.

    A version nothing carries returns an empty list rather than an error: the
    ticket/release join is free text with no foreign key, so that is a true answer.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {"limit": limit}
    if status:
        params["status"] = status
    if assignee:
        params["assignee"] = assignee

    # `release` only exists on the project-scoped route -- there is no
    # organization-wide version filter, deliberately.
    if release:
        resolved_project_id = _api.resolve_project(project_id)
        if not resolved_project_id:
            return {
                "error": "release requires a project -- a version only means "
                "something within one. Pass project_id, or launch from a directory "
                "with .innoday/project.yml."
            }
        params["release"] = release
        result = await _api.get(
            f"/api/v1/organizations/{org_id}/projects/{resolved_project_id}/tickets",
            params=params,
        )
        if isinstance(result, dict) and "error" in result:
            return result
        return {
            "tickets": result,
            "count": len(result),
            "organization_id": org_id,
            "project_id": resolved_project_id,
            "release": release,
        }

    if project_id:
        resolved_project_id = _api.resolve_project(project_id)
        result = await _api.get(
            f"/api/v1/organizations/{org_id}/projects/{resolved_project_id}/tickets",
            params=params,
        )
    else:
        result = await _api.get(
            f"/api/v1/organizations/{org_id}/tickets", params=params
        )
    # Endpoint returns a bare JSON array; wrap it so FastMCP's dict output
    # schema is satisfied. Error dicts from _api.get pass through unchanged.
    if isinstance(result, list):
        return {"tickets": result, "count": len(result), "organization_id": org_id}
    return result


@app.tool()
async def create_ticket(
    summary: str = Field(description="Ticket title/summary"),
    description: Optional[str] = Field(
        default=None, description="Detailed ticket description"
    ),
    status: str = Field(
        # The enum's own value, not the member name spelled by hand. A `default=`
        # is never validated client-side before being sent, which is exactly how
        # the invalid "TODO" survived here.
        default=TicketStatus.TODO.value,
        description=(
            "Initial status. Accepts either spelling of any member -- "
            f"'IN_REVIEW', 'in review' and 'in-review' are one status: {_STATUS_NAMES}"
        ),
    ),
    assignee: Optional[str] = Field(default=None, description="Assignee username"),
    release: Optional[str] = Field(
        default=None,
        description="Release version to plan this ticket into. Must be one of "
        "the project's outstanding releases, or 'current' for the version being "
        "cut; call list_releases to see them",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID to attach this ticket to (uses default if not provided)",
    ),
) -> Dict[str, Any]:
    """
    Create a new ticket in InnoDay.

    Creates a ticket with the specified details and returns the created ticket.

    `release` must name one of the project's **outstanding** releases (planned or
    in progress) -- `list_releases` gives the options, and `current` means the
    version being cut without having to know its number. Matching is exact and
    case-sensitive; a version nothing is planning into is rejected with a 422
    whose message lists the valid ones, so a wrong guess is correctable in one
    turn rather than silently creating a ticket no release will ever close.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "Project ID required but not configured -- a ticket must "
            "belong to a project. Pass project_id explicitly, or launch from a directory with "
            ".innoday/project.yml so it resolves automatically."
        }

    ticket_data: Dict[str, Any] = {
        "summary": summary,
        "description": description,
        "status": status,
        "project_id": resolved_project_id,
    }
    if assignee:
        ticket_data["assignee"] = assignee
    # `is not None`, not truthiness: "" is a meaningful value on the update tool
    # ("take this ticket out of its release") and the two must not diverge.
    if release is not None:
        ticket_data["release"] = release

    created = await _api.post(
        f"/api/v1/organizations/{org_id}/tickets", json=ticket_data
    )
    return _note_unapplied_status(created, status)


@app.tool()
async def update_ticket(
    ticket_id: str = Field(description="Ticket ID to update"),
    status: Optional[str] = Field(
        default=None,
        description=(
            "New status (e.g. DRAFT -> TODO to approve a draft ticket). Accepts "
            "either spelling of any member -- 'IN_REVIEW', 'in review' and "
            f"'in-review' are one status: {_STATUS_NAMES}"
        ),
    ),
    assignee: Optional[str] = Field(default=None, description="New assignee username"),
    summary: Optional[str] = Field(default=None, description="New summary/title"),
    description: Optional[str] = Field(default=None, description="New description"),
    release: Optional[str] = Field(
        default=None,
        description="Release version to move this ticket to. Must be one of the "
        "project's outstanding releases, or 'current' for the version being cut; "
        'call list_releases to see them. Pass "" to take the ticket out of its '
        "release",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    project_id: Optional[str] = Field(
        default=None, description="New project ID to (re)attach this ticket to"
    ),
) -> Dict[str, Any]:
    """
    Update an existing ticket.

    Updates specified fields of a ticket and returns the updated ticket.

    `release` must name one of the project's **outstanding** releases (planned or
    in progress), or `current` for the version being cut -- `list_releases` gives
    the options. Matching is exact and case-sensitive, and `""` clears the field.
    Setting `project_id` and `release` in the same call validates the version
    against the *destination* project.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    update_data: Dict[str, Any] = {}
    if status:
        update_data["status"] = status
    if assignee is not None:
        update_data["assignee"] = assignee
    if summary:
        update_data["summary"] = summary
    if description is not None:
        update_data["description"] = description
    if release is not None:
        update_data["release"] = release
    if project_id is not None:
        update_data["project_id"] = project_id

    if not update_data:
        return {"error": "No fields to update"}

    # Route through _API.put (fresh api_url + a 30s timeout) rather than a
    # hand-rolled client -- the previous inline PUT had no timeout, so a hung
    # API connection would block this long-lived MCP server indefinitely.
    return await _api.put(
        f"/api/v1/organizations/{org_id}/tickets/{ticket_id}", json=update_data
    )


# =============================================================================
# Board Management Tools
# =============================================================================


@app.tool()
async def list_boards(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    board_type: Optional[str] = Field(
        default=None, description="Filter by type: trello, jira, linear, notion"
    ),
) -> Dict[str, Any]:
    """
    List all boards registered with InnoDay.

    Returns board information including sync status and ticket counts.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {}
    if board_type:
        params["board_type"] = board_type

    result = await _api.get(f"/api/v1/organizations/{org_id}/boards", params=params)
    # The API returns a bare JSON array, but this tool's declared output schema
    # is an object -- FastMCP rejects a top-level list ("structured_content must
    # be a dict"). Wrap it. _api.get already returns an {"error": ...} dict on a
    # non-200, so pass that through unchanged.
    if isinstance(result, list):
        return {"boards": result, "count": len(result), "organization_id": org_id}
    return result


@app.tool()
async def sync_board(
    board_id: str = Field(description="Board registration ID to sync"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    full_sync: bool = Field(
        default=False, description="Perform full sync vs incremental"
    ),
    dry_run: bool = Field(
        default=False, description="Preview sync without making changes"
    ),
    force: bool = Field(
        default=False, description="Force sync even if one is already in progress"
    ),
) -> Dict[str, Any]:
    """
    Synchronize a Jira or Trello board with InnoDay.

    Fetches latest tickets from the board and updates InnoDay's database.

    The board's credential is resolved server-side from Vault, so no token is
    supplied from here. A board with nothing stored gets a 400 naming the
    remedy: register it with a token, or `innoday board set-credential`.
    """
    # This used to build `X-Integration-Token` from the MCP server's own
    # `BOARD_API_EMAIL`/`BOARD_API_TOKEN`, which **overrode** the board's stored
    # credential (a supplied header wins over Vault) and was one process-wide
    # value shared by every tenant, not type-checked against the board -- the
    # shape that sent a GitHub PAT to `api.trello.com` in #562. Same removal
    # #610 made in the CLI (#611).
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    headers, error = user_headers_or_error("Board sync failed")
    if error:
        return error

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/boards/{board_id}/sync",
            json={"full_sync": full_sync, "dry_run": dry_run, "force": force},
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Board sync failed: {response.status_code}",
                "details": response.text,
            }


@app.tool()
async def get_board_summary_data(
    board_id: str = Field(
        description="Board registration ID to fetch summary data for"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    summary_type: str = Field(
        default="status",
        description="Type of summary: status, daily, sprint, weekly, release, custom",
    ),
    since_version: Optional[str] = Field(
        default=None,
        description="Git tag baseline for release summaries, e.g. 'v1.4.0'. Only used when summary_type=release.",
    ),
    github_org: Optional[str] = Field(
        default=None,
        description="GitHub org to fetch commits from for release summaries. Defaults to the org's alias.",
    ),
) -> Dict[str, Any]:
    """
    Fetch the raw structured data (active tickets, recent completions, stats,
    and a suggested prompt) needed to write a board summary. This tool does
    NOT call Claude/Anthropic and does NOT write a summary itself.

    YOU (the calling Claude Code session) are expected to read the returned
    `messages`/`prompt`/`stats` and write the actual summary prose yourself,
    then call `save_board_summary` with the text you wrote to persist it.

    For release summaries (summary_type='release'), provide since_version to get
    commit history across all GitHub repos since that tag, combined with all
    completed Jira/Trello tickets. Requires GITHUB_TOKEN env var for commit history.

    Other summary types provide status, daily standup, sprint health, or weekly roundup.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {"summary_type": summary_type}
    if since_version:
        params["since_version"] = since_version
    if github_org:
        params["github_org"] = github_org

    return await _api.get(
        f"/api/v1/organizations/{org_id}/boards/{board_id}/summary-data",
        params=params,
    )


@app.tool()
async def save_board_summary(
    board_id: str = Field(description="Board registration ID the summary is for"),
    summary_type: str = Field(
        description="Type of summary: status, daily, sprint, weekly, release, custom"
    ),
    summary: str = Field(
        description="The summary text YOU (Claude Code) wrote from get_board_summary_data's output"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    stats: Optional[Dict[str, Any]] = Field(
        default=None,
        description="The stats payload from get_board_summary_data, echoed back for the historical record",
    ),
    highlights: Optional[List[str]] = Field(
        default=None, description="Key positive points to highlight"
    ),
    concerns: Optional[List[str]] = Field(
        default=None, description="Issues or blockers requiring attention"
    ),
) -> Dict[str, Any]:
    """
    Persist a board summary that YOU (Claude Code) already wrote -- after
    calling get_board_summary_data and composing the summary text yourself
    -- to InnoDay's `summaries` table.

    This is the second half of the two-step summarize flow: no Anthropic
    call happens here either, it's a plain persistence call. Once saved,
    the summary is retrievable via list_board_summaries / summary-latest
    exactly like summaries written under the old flow.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    payload: Dict[str, Any] = {
        "summary_type": summary_type,
        "summary": summary,
        "stats": stats or {},
    }
    if highlights is not None:
        payload["highlights"] = highlights
    if concerns is not None:
        payload["concerns"] = concerns

    return await _api.post(
        f"/api/v1/organizations/{org_id}/boards/{board_id}/summaries",
        json=payload,
    )


# =============================================================================
# Ticket Creation Tools
# =============================================================================


@app.tool()
async def parse_text_to_tickets(
    text: str = Field(
        description="Text to parse into tickets (meeting notes, requirements, etc.)"
    ),
    context: Optional[str] = Field(
        default=None, description="Additional context about the text"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    board_type: Optional[str] = Field(
        default="jira", description="Target board type: trello or jira"
    ),
    max_tickets: int = Field(
        default=10, description="Maximum number of tickets to generate"
    ),
) -> Dict[str, Any]:
    """
    Parse unstructured text into structured tickets using Claude AI.

    Converts meeting notes, requirements, or conversations into actionable tickets
    with titles, descriptions, priorities, and other metadata.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    return await _api.post(
        f"/api/v1/organizations/{org_id}/tickets/parse",
        json={
            "text": text,
            "context": context,
            "board_type": board_type,
            "max_tickets": max_tickets,
        },
    )


@app.tool()
async def create_board_ticket(
    board_id: str = Field(description="Board registration ID to create ticket on"),
    summary: str = Field(description="Ticket title/summary"),
    description: Optional[str] = Field(
        default=None, description="Detailed description"
    ),
    assignee: Optional[str] = Field(
        default=None, description="Assignee email or username"
    ),
    labels: Optional[List[str]] = Field(
        default=None, description="Labels/tags for the ticket"
    ),
    priority: Optional[str] = Field(
        default=None, description="Priority: low, medium, high, critical"
    ),
    list_id: Optional[str] = Field(
        default=None, description="Trello list ID (required for Trello)"
    ),
    project_key: Optional[str] = Field(default=None, description="Jira project key"),
    issue_type: str = Field(
        default="Task", description="Jira issue type: Task, Bug, Story, Epic"
    ),
    status: Optional[str] = Field(
        default=None,
        description=(
            "Initial status/workflow-state (e.g. 'Todo', 'In Progress', "
            "'Done'). Defaults to 'TODO' when omitted. Matched "
            "case-insensitively against the board's own state names."
        ),
    ),
) -> Dict[str, Any]:
    """
    Create a ticket directly on a Trello, Jira, or Linear board.

    Creates the ticket on the external board and syncs it to InnoDay. The
    board's credential is resolved server-side (Vault, falling back to
    other configured sources) -- no token needs to be supplied here.
    """
    org_id = _api.resolve_org(None)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    ticket_data = {
        "summary": summary,
        "description": description,
        "assignee": assignee,
        "labels": labels or [],
        "priority": priority,
        "list_id": list_id,
        "project_key": project_key,
        "issue_type": issue_type,
        "status": status,
    }

    return await _api.post(
        f"/api/v1/organizations/{org_id}/boards/{board_id}/tickets", json=ticket_data
    )


@app.tool()
async def parse_and_create_tickets(
    board_id: str = Field(description="Board registration ID to create tickets on"),
    text: str = Field(description="Text to parse into tickets"),
    context: Optional[str] = Field(default=None, description="Additional context"),
    auto_create: bool = Field(
        default=False, description="Automatically create parsed tickets on board"
    ),
    default_list_id: Optional[str] = Field(
        default=None, description="Default Trello list ID"
    ),
    default_assignee: Optional[str] = Field(
        default=None, description="Default assignee"
    ),
    max_tickets: int = Field(default=10, description="Maximum tickets to create"),
) -> Dict[str, Any]:
    """
    Parse text into tickets using Claude AI and optionally create them on a board.

    This combines text parsing with ticket creation. Set auto_create=true to
    automatically create the parsed tickets, or false to just preview them.
    The board's credential is resolved server-side if auto_create needs one.
    """
    org_id = _api.resolve_org(None)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    return await _api.post(
        f"/api/v1/organizations/{org_id}/boards/{board_id}/tickets/parse-and-create",
        json={
            "text": text,
            "context": context,
            "auto_create": auto_create,
            "board_id": board_id,
            "default_list_id": default_list_id,
            "default_assignee": default_assignee,
            "max_tickets": max_tickets,
        },
    )


@app.tool()
async def get_board_lists(
    board_id: str = Field(description="Board registration ID"),
) -> Dict[str, Any]:
    """
    Get available lists/columns for a board.

    For Trello, returns the lists. For Jira, returns issue types.
    Useful for determining where to create tickets. The board's credential
    is resolved server-side -- no token needs to be supplied here.
    """
    org_id = _api.resolve_org(None)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    result = await _api.get(f"/api/v1/organizations/{org_id}/boards/{board_id}/lists")
    # Endpoint returns a bare JSON array (Trello lists / Jira issue types);
    # wrap it for FastMCP's dict output schema. Error dicts pass through.
    if isinstance(result, list):
        return {"lists": result, "count": len(result), "board_id": board_id}
    return result


# =============================================================================
# AI Analysis Tools
# =============================================================================


@app.tool()
async def analyze_conversations(
    messages: List[Dict[str, Any]] = Field(
        description="List of messages with 'content' and optional 'timestamp'"
    ),
    recency_weight: float = Field(
        default=0.3, description="Weight for recent messages (0.0-1.0)"
    ),
) -> Dict[str, Any]:
    """
    Analyze conversations using Claude AI.

    Provides conversation summarization with configurable recency weighting.
    """
    return await _api.post(
        "/api/v1/ai/summarize",
        json={"messages": messages, "recency_weight": recency_weight},
    )


@app.tool()
async def analyze_temporal_patterns(
    messages: List[Dict[str, Any]] = Field(
        description="List of messages with 'content' and 'timestamp'"
    ),
    window_hours: int = Field(
        default=24, description="Time window for pattern analysis in hours"
    ),
) -> Dict[str, Any]:
    """
    Analyze temporal patterns in messages.

    Identifies patterns, trends, and anomalies in time-stamped message data.
    """
    # `/api/v1/ai/analyze-temporal` never existed -- the temporal analysis lives
    # behind `POST /api/v1/ai/analyze`, which branches on `analysis_type ==
    # "temporal"` (src/routers/ai.py). The body changes with the path: the route
    # takes `AnalysisRequest`, whose fields are `data` / `analysis_type` /
    # `time_window`, and `time_window` is free text interpolated into the prompt,
    # so the window is expressed in words rather than as a bare number (#652).
    return await _api.post(
        "/api/v1/ai/analyze",
        json={
            "data": messages,
            "analysis_type": "temporal",
            "time_window": f"{window_hours} hours",
        },
    )


# =============================================================================
# Resource Providers
# =============================================================================


@app.resource("repositories://list")
async def get_repositories_resource() -> str:
    """
    Provide a list of all repositories as a resource.

    This allows Claude Code to access repository information directly.
    """
    result = await list_repositories(include_archived=True)
    if "error" in result:
        return f"Error: {result['error']}"

    repos = result.get("repositories", [])
    output = f"# InnoDay Repositories ({len(repos)} total)\n\n"

    for repo in repos:
        status = "ACTIVE"
        if repo.get("deleted"):
            status = "DELETED"
        elif repo.get("archived_at"):
            status = "ARCHIVED"

        output += f"## {repo['repo_full_name']} [{status}]\n"
        output += f"- Platform: {repo['platform_type']}\n"
        output += f"- URL: {repo['repo_url']}\n"
        output += f"- Last Sync: {repo.get('last_sync_at', 'Never')}\n"
        output += f"- Sync Issues: {repo.get('sync_issues', False)}\n"
        output += f"- Sync PRs: {repo.get('sync_pull_requests', False)}\n\n"

    return output


@app.resource("tickets://list")
async def get_tickets_resource() -> str:
    """
    Provide a list of active tickets as a resource.

    This allows Claude Code to access ticket information directly.
    """
    result = await list_tickets(status="IN_PROGRESS")
    if "error" in result:
        result = await list_tickets(status="TODO")

    if "error" in result:
        return f"Error: {result['error']}"

    tickets = result if isinstance(result, list) else []
    output = f"# InnoDay Active Tickets ({len(tickets)} total)\n\n"

    for ticket in tickets:
        output += f"## {ticket['summary']}\n"
        output += f"- Status: {ticket['status']}\n"
        output += f"- ID: {ticket['id']}\n"
        if ticket.get("assignee"):
            output += f"- Assignee: {ticket['assignee']}\n"
        if ticket.get("description"):
            output += f"- Description: {ticket['description'][:200]}...\n"
        output += "\n"

    return output


# =============================================================================
# Prompt Templates
# =============================================================================


@app.prompt()
async def project_overview() -> str:
    """
    Provide a comprehensive overview of the InnoDay project state.

    Includes repository status, active tickets, and recent activity.
    """
    repos = await get_repositories_resource()
    tickets = await get_tickets_resource()

    return f"""# InnoDay Project Overview

{repos}

{tickets}

## Quick Actions
- Use `sync_repository` to attach a project's repositories by GitHub topic
- Use `create_ticket` to add new work items
- Use `update_ticket` to change ticket status
- Use `sync_board` to update from Trello/Jira
- Use `analyze_conversations` for AI-powered insights
"""


@app.prompt()
async def development_status() -> str:
    """
    Provide current development status and work in progress.
    """
    in_progress = await list_tickets(status="IN_PROGRESS")
    todo = await list_tickets(status="TODO", limit=10)

    output = "# Current Development Status\n\n"

    if not isinstance(in_progress, dict) or "error" not in in_progress:
        tickets = in_progress if isinstance(in_progress, list) else []
        output += f"## In Progress ({len(tickets)} items)\n"
        for ticket in tickets[:5]:
            output += f"- {ticket['summary']}"
            if ticket.get("assignee"):
                output += f" (@{ticket['assignee']})"
            output += "\n"

    if not isinstance(todo, dict) or "error" not in todo:
        tickets = todo if isinstance(todo, list) else []
        output += f"\n## TODO Queue ({len(tickets)} items)\n"
        for ticket in tickets[:5]:
            output += f"- {ticket['summary']}\n"

    return output


# =============================================================================
# Scope Management Tools
# =============================================================================


@app.tool()
async def create_scope_document(
    project_id: str = Field(..., description="Project ID"),
    requirements: str = Field(..., description="Initial requirements from client"),
    created_by: str = Field(default="mcp", description="Creator ID (default: mcp)"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Create an initial scope document for a project.

    This starts the scope refinement workflow by capturing the initial
    requirements from the client.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    return await _api.post(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/scope",
        json={"requirements": requirements, "created_by": created_by},
    )


@app.tool()
async def get_current_scope(
    project_id: str = Field(..., description="Project ID"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Get the current active scope document for a project.

    Returns the latest version of the scope document with all refinements.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    result = await _api.get(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/scope"
    )
    if "error" in result:
        return result
    return result if result else {"message": "No scope document found for this project"}


@app.tool()
async def update_scope_document(
    project_id: str = Field(..., description="Project ID"),
    scope_id: str = Field(..., description="Scope document ID"),
    refined_scope: Optional[str] = Field(None, description="Refined scope text"),
    deliverables: Optional[str] = Field(None, description="Deliverables list"),
    estimated_hours: Optional[int] = Field(None, description="Estimated hours"),
    confidence_score: Optional[float] = Field(
        None, description="Confidence score (0-1)"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Update a scope document with refined information.

    Used to iteratively refine the scope based on clarifications and feedback.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    data: Dict[str, Any] = {}
    if refined_scope:
        data["refined_scope"] = refined_scope
    if deliverables:
        data["deliverables"] = deliverables
    if estimated_hours is not None:
        data["estimated_hours"] = estimated_hours
    if confidence_score is not None:
        data["confidence_score"] = confidence_score

    if not data:
        return {"error": "No updates provided"}

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/projects/{project_id}/scope/{scope_id}",
            json=data,
            headers=get_user_headers(),
        )
        if response.status_code == 200:
            return response.json()
        return {"error": f"Failed to update scope: {response.text}"}


@app.tool()
async def add_project_update(
    project_id: str = Field(..., description="Project ID"),
    update_type: str = Field(
        ...,
        description="Type of update: requirement, clarification, feedback, question, answer",
    ),
    content: str = Field(..., description="Update content"),
    created_by: str = Field(default="mcp", description="Creator ID (default: mcp)"),
    requires_client_input: bool = Field(
        default=False, description="Whether this update requires client input"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Add an update to the project requirements workflow.

    Use this to add clarifications, questions, feedback, or new requirements
    during the scope refinement process.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    return await _api.post(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/updates",
        json={
            "update_type": update_type.upper(),
            "content": content,
            "created_by": created_by,
            "requires_client_input": requires_client_input,
        },
    )


@app.tool()
async def get_project_updates(
    project_id: str = Field(..., description="Project ID"),
    pending_only: bool = Field(default=False, description="Show only pending updates"),
    requires_input: bool = Field(
        default=False, description="Show only updates requiring client input"
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Get project updates for the requirements workflow.

    Returns all updates, questions, and clarifications for the project scope.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {}
    if pending_only:
        params["pending_only"] = "true"
    if requires_input:
        params["requires_input"] = "true"

    result = await _api.get(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/updates",
        params=params,
    )
    if "error" in result:
        return result
    return {"updates": result}


@app.tool()
async def finalize_scope(
    project_id: str = Field(..., description="Project ID"),
    scope_id: str = Field(..., description="Scope document ID"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Finalize a scope document, marking it as ready for approval.

    Once finalized, the scope cannot be edited and is ready for
    project status approval.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    result = await _api.post(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/scope/{scope_id}/finalize",
    )
    if "error" in result:
        return result
    return {"message": "Scope finalized and ready for approval", "scope": result}


@app.tool()
async def update_project_status(
    project_id: str = Field(..., description="Project ID"),
    status: str = Field(..., description="New status: planning, active, or archived"),
    description: str = Field(..., description="Reason for status change"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Update project status (e.g., approve scope by setting status to active).

    This is used for the approval workflow at the project level.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/projects/{project_id}/status/{status}",
            json={
                "date": datetime.now(timezone.utc).isoformat(),
                "description": description,
            },
            headers=get_user_headers(),
        )
        if response.status_code == 200:
            return response.json()
        return {"error": f"Failed to update status: {response.text}"}


# =============================================================================
# Unified Work Tools
# =============================================================================


@app.tool()
async def get_all_work(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    status: Optional[str] = Field(
        default=None,
        description="Filter by status: todo, in progress, in test, done, open, closed",
    ),
    priority: Optional[str] = Field(
        default=None,
        description="Filter by priority: urgent, high, medium, low, no_priority",
    ),
    source_platform: Optional[str] = Field(
        default=None,
        description="Filter by platform: trello, jira, notion, linear, github",
    ),
    assignee: Optional[str] = Field(
        default=None, description="Filter by assignee name"
    ),
    limit: int = Field(default=50, description="Maximum number of items to return"),
) -> Dict[str, Any]:
    """
    Get all work items (tickets + GitHub issues) across all boards and repositories.

    Use this to understand the full scope of work in flight across every
    connected platform. Returns tickets from Trello, Jira, Notion, and Linear
    alongside GitHub issues — all in one unified list.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    params: Dict[str, Any] = {"limit": limit}
    if status:
        params["status"] = status
    if priority:
        params["priority"] = priority
    if source_platform:
        params["source_platform"] = source_platform
    if assignee:
        params["assignee"] = assignee

    items = await _api.get(f"/api/v1/organizations/{org_id}/work", params=params)
    if "error" in items:
        return items
    return {
        "work_items": items,
        "count": len(items),
        "organization_id": org_id,
        "filters_applied": {k: v for k, v in params.items() if k != "limit"},
    }


@app.tool()
async def sync_linear_board(
    board_registration_id: str = Field(
        description="Board registration ID for the Linear team"
    ),
    token: str = Field(description="Linear personal API key (lin_api_...)"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    full_sync: bool = Field(
        default=False, description="Force full re-sync instead of incremental"
    ),
) -> Dict[str, Any]:
    """
    Sync a registered Linear team board with InnoDay.

    Fetches issues from Linear and upserts them into InnoDay's central ticket
    store. Uses incremental sync by default (only issues updated since last sync).
    Use full_sync=True to re-import everything.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/boards/{board_registration_id}/sync",
            json={"full_sync": full_sync, "dry_run": False, "force": False},
            headers={"x-linear-token": token},
        )
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "board_registration_id": board_registration_id,
                "tickets_found": result.get("tickets_found", 0),
                "tickets_created": result.get("tickets_created", 0),
                "tickets_updated": result.get("tickets_updated", 0),
                "sync_type": "full" if full_sync else "incremental",
            }
        return {
            "error": f"Sync failed: {response.status_code}",
            "details": response.text,
        }


@app.tool()
async def get_work_summary(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    Get a structured summary of all work grouped by platform and status.

    Use this at the start of a session to orient yourself on the team's
    current work across all connected boards and repositories. Returns
    counts and highlights so you can quickly understand where things stand.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    items = await _api.get(
        f"/api/v1/organizations/{org_id}/work", params={"limit": 500}
    )
    if "error" in items:
        return items

    by_platform: Dict[str, Dict[str, int]] = {}
    urgent_items = []

    for item in items:
        platform = item.get("source_platform", "unknown")
        item_status = item.get("status", "unknown")

        if platform not in by_platform:
            by_platform[platform] = {}
        by_platform[platform][item_status] = (
            by_platform[platform].get(item_status, 0) + 1
        )

        if item.get("priority") == "urgent":
            urgent_items.append(
                {
                    "summary": item["summary"],
                    "platform": platform,
                    "status": item_status,
                    "url": item.get("url"),
                }
            )

    highlights = []
    for platform, statuses in by_platform.items():
        in_progress = statuses.get("in progress", 0) + statuses.get("open", 0)
        done = statuses.get("done", 0) + statuses.get("closed", 0)
        total = sum(statuses.values())
        highlights.append(
            f"{platform}: {total} total, {in_progress} in progress, {done} done"
        )

    return {
        "total_work_items": len(items),
        "by_platform": by_platform,
        "highlights": highlights,
        "urgent_items": urgent_items[:10],
        "organization_id": org_id,
    }


# =============================================================================
# Project-Centric Ticket Creation Tool
# =============================================================================


@app.tool()
async def create_tickets_from_text(
    text: str = Field(
        description=(
            "Free-form text describing the work to be done. Can be a feature request, "
            "meeting notes, a requirements doc, a user story, or any description. "
            "Claude will break this into individual actionable tickets."
        )
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID to tag tickets with (uses default if not provided) "
        "-- required, a ticket must always belong to a project.",
    ),
    repo_context: Optional[str] = Field(
        default=None,
        description=(
            "Repository name or layer context to help assign tickets to the right area "
            "(e.g. 'api', 'frontend', 'org/repo-name'). Helps Claude label tickets correctly."
        ),
    ),
    dry_run: bool = Field(
        default=False,
        description=(
            "If true, parse and return the proposed tickets without creating them. "
            "Use to preview before committing."
        ),
    ),
    max_tickets: int = Field(
        default=10,
        description="Maximum number of tickets to create (1–20).",
        ge=1,
        le=20,
    ),
    default_status: str = Field(
        default="BACKLOG",
        description="Initial status for all created tickets: BACKLOG, TODO, IN_PROGRESS",
    ),
) -> Dict[str, Any]:
    """
    Break a block of text into individual tickets and create them in InnoDay.

    This is the primary tool for turning requirements, meeting notes, or a
    feature description into structured tickets. It calls InnoDay's AI parsing
    endpoint, groups tickets by theme, and creates them in the database.

    Tickets are created in InnoDay only — not written to external boards
    (Jira/Trello/Linear). Use sync_all_boards separately if you want to push
    tickets to an external board. Every created ticket is tagged with the
    resolved project_id -- a ticket must always belong to a project.

    Examples:
    - Paste a user story → get 3-5 acceptance-criteria tickets
    - Paste meeting notes → get action item tickets
    - Describe a feature → get a breakdown into frontend/backend/data tasks
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "Project ID required but not configured -- tickets must "
            "belong to a project. Pass project_id explicitly, or launch from a directory with "
            ".innoday/project.yml so it resolves automatically."
        }
    project_id = resolved_project_id

    # Build context hint for AI parser
    context_parts = []
    if project_id:
        context_parts.append(f"Project ID: {project_id}")
    if repo_context:
        context_parts.append(f"Repository/layer context: {repo_context}")
    context_hint = " | ".join(context_parts) if context_parts else None

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Step 1: Parse text into ticket structures via AI endpoint
        parse_resp = await client.post(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/tickets/parse",
            json={
                "text": text,
                "context": context_hint,
                "max_tickets": max_tickets,
            },
        )

        if parse_resp.status_code != 200:
            return {
                "error": f"Failed to parse text into tickets: {parse_resp.status_code}",
                "details": parse_resp.text,
                "hint": "Ensure the InnoDay API is running and CLAUDE_API_KEY is set in .env",
            }

        parsed = parse_resp.json()
        tickets_to_create = (
            parsed.get("tickets", parsed) if isinstance(parsed, dict) else parsed
        )

        if not tickets_to_create:
            return {
                "parsed": 0,
                "message": "No tickets could be parsed from the provided text.",
                "hint": "Try providing more specific, actionable text.",
            }

        if dry_run:
            return {
                "dry_run": True,
                "parsed_count": len(tickets_to_create),
                "tickets": tickets_to_create,
                "message": "Preview only — no tickets created. Set dry_run=false to create.",
            }

        # Step 2: Create each parsed ticket in InnoDay
        created = []
        errors = []
        for t in tickets_to_create[:max_tickets]:
            ticket_payload: Dict[str, Any] = {
                "summary": t.get("summary")
                or t.get("title")
                or t.get("name", "Untitled"),
                "description": t.get("description") or t.get("body") or "",
                "status": default_status,
                "project_id": project_id,
                # Bulk/parse flow: do NOT synchronously push each parsed ticket
                # to the external board -- that would be one blocking Linear/
                # Jira round-trip per ticket in a single MCP call (timeout risk).
                # These land as InnoDay-only rows; a board sync reconciles them.
                "push_to_board": False,
            }
            if t.get("priority"):
                ticket_payload["priority"] = t["priority"]
            if t.get("assignee"):
                ticket_payload["assignee"] = t["assignee"]
            if t.get("labels") or t.get("tags"):
                ticket_payload["labels"] = t.get("labels") or t.get("tags")

            create_resp = await client.post(
                f"{get_config().api_url}/api/v1/organizations/{org_id}/tickets",
                json=ticket_payload,
            )
            if create_resp.status_code in [200, 201]:
                created.append(create_resp.json())
            else:
                errors.append(
                    {
                        "summary": ticket_payload["summary"],
                        "error": create_resp.status_code,
                        "details": create_resp.text[:200],
                    }
                )

    return {
        "created": len(created),
        "errors": len(errors),
        "tickets": [
            {
                "id": t.get("id"),
                "summary": t.get("summary"),
                "status": t.get("status"),
                "priority": t.get("priority"),
            }
            for t in created
        ],
        "failed": errors,
        "organization_id": org_id,
        "project_id": project_id,
    }


# =============================================================================
# Organization & Project Setup Tools
# =============================================================================


@app.tool()
async def setup_organization(
    name: str = Field(description="Organization name (e.g. 'Acme Corp')"),
    slug: Optional[str] = Field(
        default=None,
        description="URL slug — auto-generated from name if omitted (e.g. 'acme-corp')",
    ),
    description: Optional[str] = Field(default=None, description="Short description"),
    github_url: Optional[str] = Field(
        default=None, description="GitHub org URL (e.g. https://github.com/acme)"
    ),
    jira_url: Optional[str] = Field(
        default=None, description="Jira base URL (e.g. https://acme.atlassian.net)"
    ),
    user_id: Optional[str] = Field(
        default=None,
        description="User ID to set as owner (uses INNODAY_USER_ID env var if omitted)",
    ),
) -> Dict[str, Any]:
    """
    Create a new organization in InnoDay.

    The specified user (or INNODAY_USER_ID) becomes the org owner. Returns
    the created organization including its ID, which you'll need for subsequent
    setup_project and sync_all_boards calls.

    Requires INNODAY_USER_ID to be set (or pass user_id explicitly).
    """
    cfg = get_config()
    uid = user_id or cfg.user_id
    if not uid:
        return {
            "error": "User ID required. Set INNODAY_USER_ID env var or pass user_id.",
            "hint": "Find your user ID via: GET /api/v1/users (or check INNODAY_USER_ID in .env)",
        }

    payload: Dict[str, Any] = {"name": name}
    if slug:
        # API request body key is "alias" -- Organization's domain model has
        # no separate "slug" field; this tool's own "slug" parameter name is
        # kept for backward compatibility with existing MCP clients.
        payload["alias"] = slug
    if description:
        payload["description"] = description
    if github_url:
        payload["github_url"] = github_url
    if jira_url:
        payload["jira_url"] = jira_url

    headers = get_user_headers()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{cfg.api_url}/api/v1/organizations",
            json=payload,
            headers=headers,
        )

        if response.status_code in [200, 201]:
            org = response.json()
            return {
                "created": True,
                "organization": org,
                "next_step": f"Call setup_project(organization_id='{org['id']}', ...) to create a project.",
            }
        elif response.status_code == 409:
            return {
                "error": "Organization with this slug already exists.",
                "hint": "Use a different slug or retrieve the existing org via list_organizations.",
            }
        else:
            return {
                "error": f"Failed to create organization: {response.status_code}",
                "details": response.text,
            }


@app.tool()
async def list_organizations(
    user_id: Optional[str] = Field(
        default=None,
        description="Filter to orgs this user belongs to (uses INNODAY_USER_ID if omitted)",
    ),
) -> Dict[str, Any]:
    """
    List all organizations, optionally filtered to those the current user belongs to.

    Use this to find your organization_id if you don't have it yet.
    """
    cfg = get_config()
    user_id or cfg.user_id
    headers = get_user_headers()
    if cfg.team_secret:
        headers["X-Team-Secret"] = cfg.team_secret

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{cfg.api_url}/api/v1/organizations",
            headers=headers,
        )
        if response.status_code == 200:
            orgs = response.json()
            return {
                "organizations": orgs,
                "count": len(orgs),
                "hint": "Use organization.id as organization_id in other tools.",
            }
        return {
            "error": f"Failed to list organizations: {response.status_code}",
            "details": response.text,
        }


@app.tool()
async def setup_project(
    name: str = Field(description="Project name"),
    alias: str = Field(
        description="Short uppercase ticket prefix, e.g. PF, HS — required, unique within the org"
    ),
    description: str = Field(description="What this project does"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    goals: Optional[str] = Field(
        default=None,
        description="Markdown-formatted goals and milestones for the project",
    ),
    scope_limitations: Optional[str] = Field(
        default=None, description="What is explicitly out of scope"
    ),
    tags: Optional[List[str]] = Field(
        default=None,
        description="Optional tags (e.g. ['backend', 'api', 'v2'])",
    ),
) -> Dict[str, Any]:
    """
    Create a new project inside an organization.

    Projects are the central organizing unit — boards and repositories attach
    to projects. After creating a project, register a board with register_board
    and trigger sync_all_boards to pull in tickets.

    Returns the project ID needed for scope and board operations.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    payload: Dict[str, Any] = {
        "name": name,
        "alias": alias,
        "description": description,
    }
    if goals:
        payload["goals"] = goals
    if scope_limitations:
        payload["scope_limitations"] = scope_limitations
    if tags:
        payload["tags"] = tags

    result = await _api.post(f"/api/v1/organizations/{org_id}/projects", json=payload)
    if "error" in result:
        return result
    return {
        "created": True,
        "project": result,
        "next_steps": [
            f"Register a board: register_board(organization_id='{org_id}', project_id='{result['id']}', ...)",
            f"Update project scope: update_project_scope(project_id='{result['id']}', ...)",
        ],
    }


@app.tool()
async def setup_project_workspace(
    org_alias: str = Field(description="Organization alias, e.g. 'hs'"),
    project_alias: Optional[str] = Field(
        default=None,
        description="Project alias, e.g. 'pf'. Omit to onboard the org's default project.",
    ),
    path: Optional[str] = Field(
        default=None,
        description="Workspace directory override (default: ~/workspaces/<org>/<proj>)",
    ),
    no_clone: bool = Field(
        default=False, description="Write .innoday/project.yml only; skip git clone"
    ),
    no_hooks: bool = Field(
        default=False,
        description="Skip installing the pixelfuel-managed pre-commit hook per repo",
    ),
) -> Dict[str, Any]:
    """
    Onboard OR refresh a project workspace by alias — the programmatic
    equivalent of the pixelfuel-claude `onboard-project` skill, now inside
    InnoDay (auth P4). Shares ONE algorithm with `innoday init`/`refresh`:

      1. detect fresh vs refresh (does <ws>/.innoday/project.yml exist?)
      2. archive the prior project.yml + CLAUDE.md (<ws>/.innoday/archive/)
      3. clone new repos / pull existing; `mv` repos removed from the GitHub
         topic to <ws>/archived/ (never deleted)
      4. regenerate .innoday/project.yml (preserving blastoff-owned
         release_configs version fields)
      5. regenerate the workspace CLAUDE.md

    Resolution happens via the InnoDay API (server has DB + GitHub token); the
    git + file work runs LOCALLY, so this must run on the machine where the
    workspace lives.
    """
    # Resolve org/project + repo list via the API (server has DB + GitHub token).
    params: Dict[str, Any] = {"org": org_alias}
    if project_alias:
        params["project"] = project_alias
    resolved = await _api.get("/api/v1/onboarding/resolve", params=params)
    if not resolved or "error" in resolved or "org" not in resolved:
        return resolved or {"error": "resolution failed"}

    # Reuse the CLI's onboard/refresh algorithm helpers so there is one impl.
    from src.cli.commands.workspace import (
        CONTEXT_TEMPLATE_VERSION,
        _archive_prior_context,
        _archive_removed_repos,
        _clone_or_pull,
        _extract_custom_content,
        _install_git_hooks,
        _load_existing_yml,
        _union_custom_content,
        _workspace_path,
        _write_project_yml,
        _write_timeline_snapshot,
        _write_workspace_claude_md,
    )

    workspace = _workspace_path(org_alias, project_alias, path)
    existing = _load_existing_yml(workspace)
    mode = "refresh" if existing else "onboard"
    workspace.mkdir(parents=True, exist_ok=True)

    # 2. archive prior context
    _archive_prior_context(workspace)

    repos = resolved.get("repos", [])
    resolved_names = [r["name"] for r in repos]
    actions = []
    archived_repos: list = []
    unexplained_repos: list = []
    hooks_installed = 0
    hook_issues: list = []  # non-"installed" statuses, surfaced for CLI parity
    if not no_clone:
        # 3a. clone/pull resolved repos (+ install the pre-commit hook per repo)
        for repo in repos:
            action = _clone_or_pull(repo, workspace)
            actions.append({"name": repo["name"], "action": action})
            if not no_hooks and action in ("cloned", "pulled"):
                hook_status = _install_git_hooks(workspace / repo["name"])
                if hook_status == "installed":
                    hooks_installed += 1
                else:
                    # e.g. "skipped (foreign hook)" / "error: ..." — the CLI
                    # prints these as warnings; surface them here too so an
                    # MCP caller isn't left guessing why a hook is missing.
                    hook_issues.append({"name": repo["name"], "hook": hook_status})
        # 3b. archive ONLY what the server recorded as removed. This used to
        # archive anything in the local project.yml that the resolve response
        # did not list, with not even the CLI's all-empty guard — so a GitHub
        # hiccup moved working directories. See `_archive_removed_repos`.
        # Excluding anything in `resolved_names` is load-bearing, not defensive:
        # a repo that has just regained its topic is listed by the live GitHub
        # search AND still flagged removed in the DB until a sync catches up, so
        # without this it would be cloned and archived on every run.
        removed_names = [
            r.get("name")
            for r in (resolved.get("removed_repos") or [])
            if isinstance(r, dict)
            and r.get("name")
            and r.get("name") not in resolved_names
        ]
        archived_repos = _archive_removed_repos(workspace, removed_names)
        old_names = [
            r.get("name")
            for r in (existing.get("repos") or [])
            if isinstance(r, dict) and r.get("name")
        ]
        unexplained_repos = [
            n
            for n in old_names
            if n not in resolved_names
            and n not in removed_names
            and n not in archived_repos
        ]
    else:
        actions = [{"name": r["name"], "action": "skipped"} for r in repos]

    # 4. merge hand-written notes (read the local tail before regenerating)
    claude_file = workspace / "CLAUDE.md"
    local_custom = _extract_custom_content(claude_file) if claude_file.exists() else ""
    merged_custom = _union_custom_content(
        local_custom, resolved.get("additional_context") or ""
    )

    # 5. regenerate every derived file
    yml_path = _write_project_yml(workspace, resolved)
    claude_path, generated = _write_workspace_claude_md(
        workspace, resolved, merged_custom
    )
    timeline = resolved.get("timeline") or []
    timeline_path = _write_timeline_snapshot(workspace, timeline)

    # 6. store the context back on the project (best-effort, like the CLI)
    context_stored = False
    project_alias_resolved = (resolved.get("project") or {}).get("alias")
    if project_alias_resolved:
        push = await _api.post(
            "/api/v1/onboarding/context",
            {
                "org": (resolved.get("org") or {}).get("alias") or org_alias,
                "project": project_alias_resolved,
                "project_context": generated,
                "template_version": CONTEXT_TEMPLATE_VERSION,
                "additional_context": merged_custom,
            },
        )
        context_stored = bool(push) and "error" not in push

    return {
        "onboarded": True,
        "mode": mode,
        "org": resolved["org"],
        "project": resolved.get("project"),
        "github_topic": resolved.get("github_topic"),
        "workspace_path": str(workspace),
        "project_yml": str(yml_path),
        "claude_md": str(claude_path),
        "timeline_md": str(timeline_path) if timeline_path else None,
        "timeline_entries": len(timeline),
        "repos": actions,
        "archived_repos": archived_repos,
        # Present in the workspace, not listed by the server, not recorded as
        # removed — left alone deliberately. Usually a token or topic problem.
        "unexplained_repos": unexplained_repos,
        "context_stored": context_stored,
        "hooks_installed": hooks_installed,
        "hook_issues": hook_issues,
    }


@app.tool()
async def update_project_scope(
    project_id: str = Field(description="Project ID to update scope for"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    goals: Optional[str] = Field(
        default=None,
        description="Updated goals and milestones (Markdown)",
    ),
    scope_limitations: Optional[str] = Field(
        default=None, description="What is explicitly out of scope"
    ),
    description: Optional[str] = Field(
        default=None, description="Updated project description"
    ),
    status: Optional[str] = Field(
        default=None,
        description="Project status: planning, active, on_hold, completed, cancelled",
    ),
    tags: Optional[List[str]] = Field(default=None, description="Updated tags"),
) -> Dict[str, Any]:
    """
    Update a project's scope, goals, description, or status.

    Use this to refine the project after initial setup — add goals, clarify
    what's out of scope, or mark a project active once tickets are synced.
    Only fields you provide are updated; omitted fields are left unchanged.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    update_data: Dict[str, Any] = {}
    if goals is not None:
        update_data["goals"] = goals
    if scope_limitations is not None:
        update_data["scope_limitations"] = scope_limitations
    if description is not None:
        update_data["description"] = description
    if status is not None:
        update_data["status"] = status
    if tags is not None:
        update_data["tags"] = tags

    if not update_data:
        return {"error": "No fields provided to update"}

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/projects/{project_id}",
            json=update_data,
            headers=get_user_headers(),
        )
        if response.status_code == 200:
            return {"updated": True, "project": response.json()}
        return {
            "error": f"Failed to update project: {response.status_code}",
            "details": response.text,
        }


@app.tool()
async def clear_board(
    board_id: str = Field(description="Board registration ID to clear"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    dry_run: bool = Field(
        default=False,
        description="If true, report how many tickets would be cleared without clearing",
    ),
) -> Dict[str, Any]:
    """Logically delete all tickets synced from a board (sets deleted_at). The
    board stays registered and active. Reversible via re-sync -- tickets still
    present at source are revived on the next sync. Use dry_run=true to preview.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    query = "?dry_run=true" if dry_run else ""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/boards/{board_id}/clear{query}",
            json={},
            headers=get_user_headers(),
        )
        if response.status_code == 200:
            return response.json()
        return {
            "error": f"Failed to clear board (HTTP {response.status_code})",
            "detail": response.text,
        }


@app.tool()
async def register_board(
    board_url: str = Field(
        description=(
            "Full URL to the board. "
            "Trello: https://trello.com/b/<id>/<name>  "
            "Jira: https://company.atlassian.net/jira/software/projects/<KEY>/boards  "
            "Linear: https://linear.app/<workspace>/team/<TEAM_ID>  "
            "Notion: https://www.notion.so/<workspace>/<db-id>"
        )
    ),
    board_name: str = Field(description="Display name for this board in InnoDay"),
    board_type: str = Field(description="Board type: trello, jira, linear, notion"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    integration_token: Optional[str] = Field(
        default=None,
        description=(
            "API token for this board. Required — board access is validated "
            "before registration, and this is the value stored in Vault. "
            "There is no environment-variable fallback: pass it explicitly."
        ),
    ),
    user_id: Optional[str] = Field(
        default=None,
        description="User ID registering the board (uses INNODAY_USER_ID if omitted)",
    ),
    sync: bool = Field(
        default=False,
        description="If true, sync the board immediately after registering. "
        "A failed sync leaves the board registered (not atomic).",
    ),
) -> Dict[str, Any]:
    """
    Register an external board (Trello, Jira, Linear, Notion, GitHub) with InnoDay.

    `integration_token` must be passed explicitly — registration is the one
    legitimate moment a credential is supplied, and there is no environment-
    variable fallback. The token is validated against the real provider and
    stored as an encrypted Supabase Vault secret, which every later sync
    resolves from. After registration, call sync_all_boards to pull tickets
    into InnoDay.

    Board URL formats:
    - Trello:  https://trello.com/b/abc123/board-name
    - Jira:    https://company.atlassian.net/jira/software/projects/KEY/boards
    - Linear:  https://linear.app/workspace/team/TEAM-ID
    - Notion:  https://www.notion.so/workspace/<database-id>
    - GitHub:  https://github.com/org/repo
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    uid = user_id or config.user_id
    if not uid:
        return {
            "error": "User ID required. Set INNODAY_USER_ID env var or pass user_id.",
        }

    # The credential comes from the caller, or not at all. There is deliberately
    # no env fallback (#611): the MCP server's environment holds one value for
    # every tenant it serves, so falling back to it registers somebody else's
    # board credential into this org's Vault.
    token = integration_token
    if not token:
        return {
            "error": f"integration_token is required to register a {board_type} board.",
            "hint": (
                "Pass the board's own API token as integration_token — it is "
                "validated against the provider and stored in Vault, so no "
                "later call needs it."
            ),
        }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/boards",
            json={
                "board_url": board_url,
                "board_name": board_name,
                "board_type": board_type.lower(),
            },
            headers={
                **get_user_headers(),
                "X-Integration-Token": token,
            },
        )

        if response.status_code in [200, 201]:
            board = response.json()
            if sync:
                sync_result = await sync_board(
                    board_id=board["id"], organization_id=org_id
                )
                board["sync"] = sync_result
            return {
                "registered": True,
                "board": board,
                "next_step": f"Call sync_all_boards(organization_id='{org_id}') to pull tickets.",
            }
        elif response.status_code == 409:
            return {
                "error": "Board already registered for this organization.",
                "hint": "Use list_boards() to see existing boards and their IDs.",
            }
        elif response.status_code == 403:
            return {
                "error": "Board access denied — token is invalid or lacks permissions.",
                "hint": f"Check your {board_type.upper()} token has read access to this board.",
            }
        else:
            return {
                "error": f"Failed to register board: {response.status_code}",
                "details": response.text,
            }


@app.tool()
async def sync_all_boards(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    board_type: Optional[str] = Field(
        default=None,
        description="Only sync boards of this type: trello, jira, linear, notion. Omit to sync all.",
    ),
) -> Dict[str, Any]:
    """
    Sync all registered boards for an organization, pulling latest tickets into InnoDay.

    Iterates every active board registration and triggers a sync. Each board's
    credential is resolved server-side from Vault — no token is read here or
    sent (#611). Returns a per-board result summary.

    Call this after register_board or whenever you want fresh ticket data.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    headers, error = user_headers_or_error("Board sync failed")
    if error:
        return error

    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. List boards
        list_resp = await client.get(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/boards",
            params={"board_type": board_type} if board_type else {},
            headers=headers,
        )
        if list_resp.status_code != 200:
            return {
                "error": f"Failed to list boards: {list_resp.status_code}",
                "details": list_resp.text,
            }

        boards = list_resp.json()
        if not boards:
            return {
                "synced": 0,
                "message": "No boards registered for this organization.",
                "hint": "Use register_board() to connect a Trello, Jira, or Linear board.",
            }

        # 2. Sync each board. The endpoint resolves each board's own credential
        # from Vault, so nothing is attached here -- see `sync_board` for what
        # sending one from this process's environment cost (#611). This loop
        # picked its token out of a board_type map, so the Jira entry could
        # reach a Linear board.
        results = []

        for board in boards:
            bid = board.get("id")
            btype = board.get("board_type", "").lower()
            bname = board.get("board_name", bid)

            sync_resp = await client.post(
                f"{get_config().api_url}/api/v1/organizations/{org_id}/boards/{bid}/sync",
                headers=headers,
                json={},
            )

            if sync_resp.status_code == 200:
                data = sync_resp.json()
                results.append(
                    {
                        "board_id": bid,
                        "board_name": bname,
                        "board_type": btype,
                        "status": "ok",
                        "tickets_synced": data.get(
                            "tickets_synced", data.get("count", "?")
                        ),
                    }
                )
            else:
                results.append(
                    {
                        "board_id": bid,
                        "board_name": bname,
                        "board_type": btype,
                        "status": "error",
                        "code": sync_resp.status_code,
                        "details": sync_resp.text[:200],
                    }
                )

    synced_count = sum(1 for r in results if r["status"] == "ok")
    return {
        "total_boards": len(boards),
        "synced": synced_count,
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "results": results,
        "organization_id": org_id,
    }


# =============================================================================
# Board Probe Tool — test connectivity before sync
# =============================================================================


@app.tool()
async def probe_board(
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
    board_id: Optional[str] = Field(
        default=None,
        description=(
            "Board registration ID. If omitted, probes the first registered board for the org."
        ),
    ),
    user_id: Optional[str] = Field(
        default=None,
        description="User ID (uses INNODAY_USER_ID if omitted)",
    ),
) -> Dict[str, Any]:
    """
    Test that a board is reachable and credentials are valid before running a full sync.

    Calls POST /organizations/{org_id}/boards/{board_id}/probe which:
    1. Validates the stored board registration exists
    2. Makes a lightweight API call to the board provider to confirm auth works
    3. Returns the top 5 tickets that are actively in progress (not done, todo, or backlog)
       so you can visually confirm the right board is connected

    Use this after setup_org_with_env or register_board to confirm the org is wired
    correctly before calling sync_all_boards.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    user_id or config.user_id
    headers = get_user_headers()

    async with httpx.AsyncClient(timeout=20.0) as client:
        # If no board_id given, discover the first board for this org
        if not board_id:
            list_resp = await client.get(
                f"{get_config().api_url}/api/v1/organizations/{org_id}/boards",
                headers=headers,
            )
            if list_resp.status_code != 200:
                return {
                    "error": f"Could not list boards: {list_resp.status_code}",
                    "details": list_resp.text,
                }
            boards = list_resp.json()
            if not boards:
                return {
                    "error": "No boards registered for this organization.",
                    "hint": "Call register_board() or setup_org_with_env() first.",
                }
            board_id = boards[0]["id"]
            board_meta = boards[0]
        else:
            # Fetch just this board's metadata
            b_resp = await client.get(
                f"{get_config().api_url}/api/v1/organizations/{org_id}/boards/{board_id}",
                headers=headers,
            )
            board_meta = b_resp.json() if b_resp.status_code == 200 else {}

        # Call the probe endpoint
        probe_resp = await client.post(
            f"{get_config().api_url}/api/v1/organizations/{org_id}/boards/{board_id}/probe",
            headers=headers,
            timeout=20.0,
        )

        if probe_resp.status_code == 200:
            result = probe_resp.json()
            return {
                "status": "ok",
                "board_id": board_id,
                "board_name": board_meta.get("board_name"),
                "board_type": board_meta.get("board_type"),
                "credentials_valid": result.get("credentials_valid", True),
                "active_tickets": result.get("active_tickets", []),
                "active_ticket_count": len(result.get("active_tickets", [])),
                "message": result.get(
                    "message", "Board is reachable and credentials are valid."
                ),
            }
        elif probe_resp.status_code == 403:
            return {
                "status": "auth_failed",
                "board_id": board_id,
                "board_name": board_meta.get("board_name"),
                "board_type": board_meta.get("board_type"),
                "error": "Board credentials are invalid or expired.",
                "hint": "Update the token with register_board() or re-run setup_org_with_env().",
            }
        else:
            return {
                "status": "error",
                "board_id": board_id,
                "error": f"Probe failed: {probe_resp.status_code}",
                "details": probe_resp.text[:300],
            }


# =============================================================================
# Org Onboarding Tool (combined setup + env file)
# =============================================================================


@app.tool()
async def setup_org_with_env(
    slug: str = Field(description="Org slug, e.g. 'acme'. Used as the env file name."),
    org_name: str = Field(description="Human-readable org name, e.g. 'Acme Corp'"),
    project_name: str = Field(description="First project name"),
    project_alias: str = Field(
        description="Short uppercase ticket prefix for the first project, e.g. PF, HS — required, unique within the org"
    ),
    board_type: str = Field(
        description="Board type: jira, linear, trello, notion. Pass 'skip' to skip board setup."
    ),
    board_url: Optional[str] = Field(
        default=None,
        description="Full board URL. Required unless board_type='skip'.",
    ),
    board_api_token: Optional[str] = Field(
        default=None,
        description="Board API token. Required unless board_type='skip'.",
    ),
    board_api_email: Optional[str] = Field(
        default=None,
        description="Board API email. Required for Jira (basic auth: email:token).",
    ),
    board_name: Optional[str] = Field(
        default=None,
        description="Board display name in InnoDay. Defaults to project_name.",
    ),
    github_org: Optional[str] = Field(
        default=None, description="GitHub org name for this org's repos."
    ),
    github_topic: Optional[str] = Field(
        default=None,
        description="GitHub topic label that identifies repos for this org. Defaults to slug.",
    ),
    user_id: Optional[str] = Field(
        default=None,
        description="User ID to set as org owner. Uses INNODAY_USER_ID if omitted.",
    ),
    organization_id: Optional[str] = Field(
        default=None,
        description="If set, skip org creation and use this existing org ID.",
    ),
) -> Dict[str, Any]:
    """
    Full org onboarding in one call: creates the org, creates a first project,
    optionally registers a board, and writes env/orgs/<slug>.

    This is the MCP equivalent of `innoday orgs env-setup`. Call it when setting
    up a new client org from scratch. After this, call sync_all_boards to pull
    tickets.

    Returns org_id, project_id, board_id (if created), and the env file path.
    """
    cfg = get_config()
    uid = user_id or cfg.user_id
    if not uid:
        return {
            "error": "User ID required. Set INNODAY_USER_ID or pass user_id.",
            "hint": "Run platform setup or pass user_id explicitly.",
        }

    headers = get_user_headers()

    # `slug` is used as a filename (env/orgs/<slug>); reject anything that could
    # escape that directory (path traversal) or is otherwise not a plausible
    # org alias. Org aliases are lowercase alphanumeric + hyphen, same shape the
    # API enforces -- validate before any state is created so we fail fast.
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        return {
            "error": (
                f"Invalid slug {slug!r}: must be lowercase alphanumeric/hyphen "
                "(it names the env/orgs/<slug> file, so path separators and "
                "traversal are rejected)."
            )
        }

    skip_board = board_type.lower() == "skip"
    if not skip_board and not board_api_token:
        return {"error": "board_api_token is required when board_type is not 'skip'"}
    if not skip_board and not board_url:
        return {"error": "board_url is required when board_type is not 'skip'"}

    results: Dict[str, Any] = {}

    async with httpx.AsyncClient(timeout=30.0) as client:
        # --- Step 1: Create or reuse org ---
        if organization_id:
            org_id = organization_id
            results["org"] = {"id": org_id, "reused": True}
        else:
            org_resp = await client.post(
                f"{cfg.api_url}/api/v1/organizations",
                # API request body key is "alias" -- Organization's domain
                # model has no separate "slug" field; this tool's own "slug"
                # parameter name is kept (used as the env/orgs/<slug> file
                # name, matching `innoday orgs env-setup`'s convention).
                json={"name": org_name, "alias": slug},
                headers=headers,
            )
            if org_resp.status_code not in (200, 201):
                return {
                    "error": f"Failed to create organization: {org_resp.status_code}",
                    "details": org_resp.text,
                }
            org_data = org_resp.json()
            org_id = org_data["id"]
            results["org"] = org_data

        # --- Step 2: Create project ---
        proj_resp = await client.post(
            f"{cfg.api_url}/api/v1/organizations/{org_id}/projects",
            json={
                "name": project_name,
                "alias": project_alias,
                "description": project_name,
            },
            headers=headers,
        )
        if proj_resp.status_code not in (200, 201):
            return {
                "error": f"Failed to create project: {proj_resp.status_code}",
                "details": proj_resp.text,
                "org_id": org_id,
            }
        proj_data = proj_resp.json()
        project_id = proj_data["id"]
        results["project"] = proj_data

        # --- Step 3: Register board (optional) ---
        board_id = None
        board_failed = False
        if not skip_board:
            effective_board_name = board_name or project_name
            btype = board_type.lower()
            integration_token = (
                f"{board_api_email}:{board_api_token}"
                if btype == "jira" and board_api_email
                else board_api_token
            )
            board_resp = await client.post(
                f"{cfg.api_url}/api/v1/organizations/{org_id}/boards",
                json={
                    "board_url": board_url,
                    "board_name": effective_board_name,
                    "board_type": btype,
                },
                headers={**headers, "X-Integration-Token": integration_token},
            )
            if board_resp.status_code in (200, 201):
                board_data = board_resp.json()
                board_id = board_data.get("id")
                results["board"] = board_data
            else:
                board_failed = True
                results["board_warning"] = (
                    f"Board registration failed ({board_resp.status_code}): {board_resp.text[:200]}"
                )

    # --- Step 4: Write env/orgs/<alias> ---
    env_dir = Path("env") / "orgs"
    env_dir.mkdir(parents=True, exist_ok=True)
    env_file = env_dir / slug

    effective_github_topic = github_topic or slug
    lines = [
        f"ORG_ALIAS={slug}",
        f"ORG_NAME={org_name}",
        f"GITHUB_ORG={github_org or ''}",
        f"GITHUB_TOPIC={effective_github_topic}",
    ]
    if not skip_board:
        lines += [
            f"BOARD_TYPE={board_type.lower()}",
            f"BOARD_URL={board_url}",
            f"BOARD_API_TOKEN={board_api_token}",
            f"BOARD_API_EMAIL={board_api_email or ''}",
        ]
    else:
        lines += ["BOARD_TYPE=", "BOARD_URL=", "BOARD_API_TOKEN=", "BOARD_API_EMAIL="]

    env_file.write_text("\n".join(lines) + "\n")
    # The file holds a live board credential in cleartext -- restrict it to the
    # owner (0600) so it isn't world/group-readable like a default-umask file.
    # If chmod can't take effect (Windows, some network mounts), don't silently
    # report success: surface a warning so the operator knows the credential
    # file may be group/other-readable and can lock it down themselves.
    if not skip_board:
        try:
            env_file.chmod(0o600)
        except OSError as exc:
            results["env_file_permissions_warning"] = (
                f"Could not restrict {env_file} to 0600 ({exc}). It contains a "
                "cleartext board credential -- secure its permissions manually."
            )

    results["env_file"] = str(env_file)

    # Distinguish a fully-wired org from a partial one. When the board half
    # failed, the org/project still exist and the env file is written, but the
    # board is NOT registered -- surface that as a top-level status so a caller
    # (human or LLM) can't read the populated summary as full success and go
    # straight to sync_all_boards against a board that was never registered.
    partial = board_failed
    results["status"] = "partial" if partial else "ok"
    if partial:
        next_step = (
            "Board registration FAILED (see board_warning). The org and project "
            f"were created. Fix the board credential/URL and call "
            f"register_board(organization_id='{org_id}') before sync_all_boards."
        )
    elif not skip_board:
        next_step = f"Call sync_all_boards(organization_id='{org_id}') to pull tickets."
    else:
        next_step = "Board skipped. Register one later with register_board()."

    results["summary"] = {
        "status": results["status"],
        "org_id": org_id,
        "project_id": project_id,
        "board_id": board_id,
        "env_file": str(env_file),
        "next_step": next_step,
    }
    return results


# =============================================================================
# Release Tools
# =============================================================================


@app.tool()
async def create_release(
    version: str = Field(
        ...,
        description="Version string, e.g. 'v1.4.0'. Must be unique per project.",
    ),
    name: Optional[str] = Field(
        default=None, description="Human-readable release name"
    ),
    description: Optional[str] = Field(default=None, description="Release description"),
    notes: Optional[str] = Field(
        default=None, description="Narrative summary / release notes"
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID this release belongs to (uses default if not "
        "provided) -- required, a release must always belong to a project.",
    ),
    status: str = Field(
        default="planned",
        description="Release status: planned, in_progress, released, archived",
    ),
    released_at: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp when released (only meaningful if status=released)",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    Create a new release record in InnoDay.

    Requires DEVELOPER role or higher in the organization. Version must be
    unique per project (the same version string can exist as separate
    releases in different projects) — creating a duplicate version within
    the same project returns an error (the underlying API returns 409
    Conflict).

    Use this at the start of a release cycle to register the version before
    work begins, or call it from a release automation flow instead of
    constructing a raw POST to /releases.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "project_id required but not configured -- a release must "
            "belong to a project. Pass project_id explicitly, or launch from a directory with "
            ".innoday/project.yml so it resolves automatically."
        }

    payload: Dict[str, Any] = {
        "version": version,
        "status": status,
        "project_id": resolved_project_id,
    }
    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    if notes:
        payload["notes"] = notes
    if released_at:
        payload["released_at"] = released_at

    return await _api.post(f"/api/v1/organizations/{org_id}/releases", json=payload)


@app.tool()
async def list_releases(
    project_id: Optional[str] = Field(
        default=None, description="Filter to releases for this project"
    ),
    status: Optional[str] = Field(
        default=None,
        description="Filter by status: planned, in_progress, released, archived",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    List releases for an organization, optionally filtered by project and status.

    Returns each release with aggregate ticket_count and open_ticket_count,
    ordered by version descending. Use this to see release history or find
    the most recent release for a project.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    params: Dict[str, Any] = {}
    if project_id:
        params["project_id"] = project_id
    if status:
        params["status"] = status

    result = await _api.get(f"/api/v1/organizations/{org_id}/releases", params=params)
    if isinstance(result, dict) and "error" in result:
        return result
    return {"releases": result, "count": len(result), "organization_id": org_id}


@app.tool()
async def get_current_release_tickets(
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID. Resolved from the launch directory's "
        ".innoday/project.yml when omitted, which is the normal case.",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    Every ticket in the release this project is currently cutting.

    **This is the call to build a release summary from.** It takes no filters and
    needs no version: one request returns the current release plus its complete
    ticket list, so a summary is a matter of narrating the response rather than
    assembling one from several tools. Launched inside a project workspace it needs
    no arguments at all.

    "Current" is the project's IN_PROGRESS release — slot 1 of the two-slot
    pipeline, the version the release engine cuts next. It is resolved server-side
    by the same helper the dashboard and the Releases tab use, so this tool can
    never report a different version than the UI shows.

    Returns the release (version, name, notes, summary, status, ticket counts) and
    `tickets`: id, external_ticket_id, summary, status, assignee, priority, url.
    The ticket list is complete, not truncated — a partial list would misreport
    what is in the release.

    Use `get_release(version=...)` instead when you need a *specific* version, and
    `list_releases` to see the whole history. An error is returned when the project
    has no upcoming release: that happens on a project that has never shipped and
    never synced, and is different from a release with no tickets in it.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "project_id required but not configured -- each project runs "
            "its own release pipeline. Pass project_id explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically."
        }

    return await _api.get(
        f"/api/v1/organizations/{org_id}/releases/current/tickets",
        params={"project_id": resolved_project_id},
    )


@app.tool()
async def get_release_content(
    version: Optional[str] = Field(
        default=None,
        description=(
            "Release to assemble. Omitted means the one this project is "
            "currently cutting -- which is what you want unless you are "
            "reporting on a release already shipped, where the version is "
            "required because 'current' will have moved on."
        ),
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID. Resolved from the launch directory when omitted.",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    🚀 The release as tickets, each with the pull requests that delivered it.

    **This is what a release summary is written from**, and until now there was no
    way to reach it here -- so an MCP session fell back to `get_scrum_summary`,
    which assembles ticket *movement* and sees at most one pull request per
    ticket. Two sessions asking the same question through different doors got two
    different artifacts, and neither was wrong about its own payload.

    What comes back, and they answer different questions:
      • `items` — one entry per ticket on the release, with `state` and `gaps`
      • `included` — merged pull requests, by repository
      • `unticketed` — merged pull requests naming no ticket
      • `outstanding` / `abandoned` — open, and closed-unmerged
      • `off_release` — tickets carrying **no release at all**, each with the
        command that would fix it. `shipped_untagged` has merged code;
        `release_candidate` has an open pull request; `started_untagged` has
        neither. Candidates are offered only for the release being *cut* --
        "started, on no release" is a fact about the project, not about a version
      • `conflicts` — tickets unfinished on a version that has already shipped.
        Not candidates: they have a release, and it went out without them
      • `planned` — present and true when the version asked for is the slot being
        *filled*. It borrows no window, so `window` is null and `included`,
        `unticketed` and `off_release` are empty. That is "nothing has been put on
        this yet", which is not "nothing shipped" and not "we could not look"
      • `unknown_version` — the version asked for, when this project keeps
        releases and that is not one of them. Nothing is proposed onto it
      • `totals` — drive `with_gaps` to zero before cutting
      • `board_sync` — when the tickets were last refreshed

    **A `contested` pull request is never attached on your say-so.** A reference
    resolving is not the same as it being right: a pull request can match a
    ticket cleanly and belong to a different person and a different piece of
    work. The entry carries `contested` with the reasons; report them and let a
    person choose.

    **Read `board_sync` before you narrate anything.** A stale board and a quiet
    release are the same shape on screen: both say nothing moved. When
    `board_sync.stale` is true, *ask the caller whether to sync* and offer
    `sync_board` -- do not sync unprompted (a board pull is slow and may already
    be running) and do not narrate over it silently. The pull-request half of this
    payload comes from GitHub and is unaffected, so the report is still worth
    reading; it is the ticket half that may be behind.

    Prose is yours. Nothing here writes any.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required -- pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }
    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "project_id required but not configured. Pass project_id "
            "explicitly, or launch from a directory with .innoday/project.yml."
        }

    params: Dict[str, Any] = {}
    if version:
        params["version"] = version

    content = await _api.get(
        f"/api/v1/organizations/{org_id}/projects/{resolved_project_id}"
        "/release/content",
        params=params or None,
    )

    # The prompt is built rather than left to the tool description, because a
    # description is read once when the tool loads and this has to be true of
    # *this* response.
    if isinstance(content, dict):
        sync = content.get("board_sync") or {}
        if sync.get("stale"):
            age = sync.get("age_seconds")
            # **Stale is not only about age.** A run that FAILED two minutes ago
            # is stale with `age_seconds = 120`, and the old expression fell
            # through to the literal "synced over an hour ago" -- a branch
            # reachable only for a recent failure, so it was wrong every time it
            # fired, and told the narrating agent a false fact about the board.
            if sync.get("synced_at") is None:
                when = "never synced"
            elif not isinstance(age, (int, float)):
                when = "last synced at an unknown time"
            elif age >= 3600:
                when = f"last synced {int(age) // 3600}h ago"
            else:
                when = f"last synced {max(1, int(age) // 60)}m ago"
            content["sync_advice"] = (
                f"This project's board was {when}"
                + (f" and the last run {sync['status']}" if sync.get("status") else "")
                + ". Ask whether to run sync_board before narrating the ticket "
                "half of this release -- stale tickets read exactly like a quiet "
                "release. The pull requests above are unaffected."
            )

    return content


@app.tool()
async def get_release(
    version: Optional[str] = Field(
        default=None,
        description="Version string to look up, e.g. 'v1.4.0'. Use this OR release_id. "
        "Requires project_id, since version strings are unique per project.",
    ),
    release_id: Optional[str] = Field(
        default=None, description="Release ID to look up directly. Use this OR version."
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID (uses default if not provided) -- required when "
        "looking up by version.",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    Get a single release by version string or by ID, including its tickets.

    Provide exactly one of `version` or `release_id`. Looking up by version
    returns a synthetic release summary (with tickets but no persisted id)
    if no Release row exists yet but tickets already reference that version —
    this happens for versions that came from Jira/Linear before InnoDay
    registered them explicitly.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    if not version and not release_id:
        return {"error": "Provide either version or release_id"}
    if version and release_id:
        return {"error": "Provide only one of version or release_id, not both"}

    if release_id:
        return await _api.get(f"/api/v1/organizations/{org_id}/releases/{release_id}")

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "project_id required but not configured -- version strings "
            "are unique per project. Pass project_id explicitly, or launch from a directory with "
            ".innoday/project.yml so it resolves automatically."
        }

    return await _api.get(
        f"/api/v1/organizations/{org_id}/releases/by-version/{version}",
        params={"project_id": resolved_project_id},
    )


@app.tool()
async def update_release(
    version: str = Field(..., description="Release version string, e.g. 'v1.4.0'"),
    notes: str = Field(..., description="Release summary narrative to attach"),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID (uses default if not provided) -- required, "
        "since version strings are unique per project.",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> dict:
    """
    Attach or update a release summary narrative for a given version.

    Looks up the release by version string and patches the notes field.
    Use this after running a sync or writing release notes to record them
    against the release record. The release must already exist (created
    automatically during ticket sync or via github-ops).
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "project_id required but not configured -- version strings "
            "are unique per project. Pass project_id explicitly, or launch from a directory with "
            ".innoday/project.yml so it resolves automatically."
        }

    release = await _api.get(
        f"/api/v1/organizations/{org_id}/releases/by-version/{version}",
        params={"project_id": resolved_project_id},
    )
    if "error" in release:
        return {"error": f"Release '{version}' not found for org '{org_id}'"}

    release_id = release.get("id")
    if not release_id:
        return {
            "error": f"Release '{version}' exists but has no id (synthetic release — trigger a sync first)"
        }

    return await _api.patch(
        f"/api/v1/organizations/{org_id}/releases/{release_id}", json={"notes": notes}
    )


@app.tool()
async def blastoff(
    release: bool = Field(
        default=False,
        description="False (default) = preview only, nothing tagged or recorded. "
        "True = tag every repository and record the release. Preview first, show "
        "the caller, then call again with release=True once they approve.",
    ),
    hotfix: bool = Field(
        default=False,
        description="Patch the last released version instead of cutting the next "
        "planned one.",
    ),
    summary: Optional[str] = Field(
        default=None,
        description="Client-facing prose for this release, used verbatim. Write it "
        "from the facts a preview returns, unless the release already has one.",
    ),
    topics: Optional[str] = Field(
        default=None,
        description="Override the GitHub topics used to find repositories "
        "(comma-separated). Default: the project's own.",
    ),
    repo: Optional[str] = Field(
        default=None,
        description="Hotfix only this repository. Hotfix only — a release covers "
        "the whole project.",
    ),
    commit: Optional[str] = Field(
        default=None,
        description="Hotfix this exact commit SHA. Requires hotfix and repo.",
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
    project_id: Optional[str] = Field(
        default=None,
        description="Project ID this release belongs to (uses default if omitted).",
    ),
) -> Dict[str, Any]:
    """
    Deploy: tag a project's repositories and record the release.

    **Preview, then narrate, then execute.** Call with ``release=False`` first:
    that returns the assembled facts and tags nothing. Write the summary from
    those facts -- unless the release already carries one, in which case use it --
    show the caller the report and the prose together, and only call again with
    ``release=True`` and that ``summary`` once they approve.

    That order is the point. The engine assembles and the caller narrates; a
    summary is the only part of a release a client reads, and it should not be
    improvised at the moment of tagging.

    **No alias.** The project comes from the launch directory, like every other
    tool here. The GitHub account and topics are resolved from InnoDay, which
    already computes them -- they used to be read from a hand-maintained block in
    project.yml, keyed by an alias that had to match on both sides.

    ``repo`` and ``commit`` are **hotfix-only**. A release covers the project:
    narrowing it records that the version shipped for the whole group while the
    other repositories never got the tag, and leaves each of them counting the
    same work again in the next release.

    Returns the release **data** -- version, repos, pull requests, tagging
    results -- not the printed report. A caller writing prose needs the facts,
    not a page formatted for a human to read.

    NOTE: a real release needs a GitHub token (``GH_TOKEN``) in the MCP server's
    environment. Its absence is surfaced in ``error`` rather than crashing.
    """
    import contextlib
    import io
    import json
    from types import SimpleNamespace

    from src.cli.commands.release_proxy import (
        ReleaseProxyCommands,
        _build_store,
    )

    # ------------------------------------------------------------------ #
    # Resolve org / project (matching every other release tool).
    # ------------------------------------------------------------------ #
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    resolved_project_id = _api.resolve_project(project_id)
    if not resolved_project_id:
        return {
            "error": "project_id required but not configured -- a release must "
            "belong to a project. Pass project_id explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically."
        }

    # Scope rules first — the same ones the CLI enforces, because a tool call is
    # no less capable of tagging the wrong thing than a person is.
    scope_error = ReleaseProxyCommands._check_scope(
        SimpleNamespace(repo=repo, commit=commit), hotfix
    )
    if scope_error:
        return {"error": scope_error}

    # ------------------------------------------------------------------ #
    # Resolve the GitHub account and topics from InnoDay -- the same answer
    # `innoday init` uses, rather than a hand-maintained copy in project.yml.
    # ------------------------------------------------------------------ #
    from src.cli.commands.release_proxy import _resolve_release_target

    try:
        target = await _resolve_release_target(
            build_cli_config(), org_id, resolved_project_id
        )
    except Exception as e:  # noqa: BLE001 -- never raise out of an MCP tool
        return {"error": f"Could not resolve this project from InnoDay: {e}"}
    if target is None:
        return {
            "error": "Could not resolve this project's GitHub account and topics "
            "from InnoDay. Launch the MCP server from inside the project "
            "workspace, or pass organization_id and project_id."
        }
    resolved_alias, github_org, resolved_topics = target
    if topics:
        resolved_topics = [t.strip() for t in topics.split(",") if t.strip()]
    prerelease = None

    # ------------------------------------------------------------------ #
    # Build a CLI-style InnoDayAPIClient for the store (the store speaks the
    # CLI client's request contract, NOT the MCP _api wrapper), then the store.
    # ------------------------------------------------------------------ #
    try:
        from src.cli.client import InnoDayAPIClient

        # Same single construction as load_config() -- see build_cli_config.
        # This site had the throwaway-peek shape too (#611).
        api_client = InnoDayAPIClient(build_cli_config())
    except Exception as e:  # noqa: BLE001
        return {
            "error": f"Failed to build InnoDay API client for release: {e}",
            "alias": resolved_alias,
            "released": release,
        }

    store = _build_store(
        api_client=api_client,
        org_id=org_id,
        project_id=resolved_project_id,
        github_org=github_org,
        topics=resolved_topics,
        prerelease=prerelease,
    )

    # Best-effort read of the target version for the result (blastoff resolves
    # it again authoritatively through the store inside its own run()).
    target_version: Optional[str] = None
    loaded_config = None
    try:
        loaded_config = store.load_org_config(resolved_alias)
        target_version = loaded_config.next_version
    except Exception:  # noqa: BLE001 -- non-fatal; blastoff will resolve it too
        target_version = None

    # ------------------------------------------------------------------ #
    # Drive blastoff in-process with the store injected, exactly like the CLI
    # proxy's _drive_release/_invoke_blastoff. Do NOT pass -t: blastoff loads
    # the version from the injected store (the corrected contract). CRITICAL:
    # blastoff prints to stdout via print(); this MCP server uses stdio
    # transport where stdout IS the JSON-RPC channel, so those prints would
    # corrupt the protocol. Capture stdout for the whole run and return it in
    # the result dict — never let it reach the real process stdout.
    # ------------------------------------------------------------------ #
    from blastoff.hotfix import Hotfix
    from blastoff.release import Release

    engine = Hotfix if hotfix else Release
    brief = {
        "name": resolved_alias,
        "github_org": github_org,
        "topics": resolved_topics,
        "version": target_version,
        "previous_version": getattr(loaded_config, "last_released_version", None),
        "previous_released_at": getattr(loaded_config, "last_released", None),
    }
    picture = ReleaseProxyCommands._ticket_picture(store, target_version)
    if picture is not None:
        brief["ticket_count"], brief["open_ticket_count"] = picture

    if hotfix:
        argv = ["-c", resolved_alias, "-o", github_org]
        argv += ["--topics", ",".join(resolved_topics)]
        if repo:
            argv += ["--repo", repo]
        if commit:
            argv += ["--commit", commit]
        brief_stdin = None
    else:
        argv = ["--brief", "-"]
        brief_stdin = json.dumps(brief)

    if summary:
        argv += ["--summary", summary]
    if release:
        argv.append("--release")
    else:
        # **Facts, not the printed page.** A caller writing prose needs the
        # numbers; handing it a formatted report means reverse-engineering them
        # back out of section rules and bullet characters.
        argv.append("--json")

    captured = io.StringIO()
    retcode = 1
    error: Optional[str] = None
    try:
        with contextlib.redirect_stdout(captured):
            retcode = ReleaseProxyCommands._invoke_blastoff(
                engine, argv, store, stdin=brief_stdin
            )
    except Exception as e:  # noqa: BLE001 -- never raise out of an MCP tool
        error = str(e)
    finally:
        # api_client owns an httpx.AsyncClient; close it so we don't leak it.
        try:
            await api_client.close()
        except Exception:  # noqa: BLE001
            pass

    output = captured.getvalue()

    if error is not None:
        return {
            "error": f"blastoff failed: {error}",
            "alias": resolved_alias,
            "released": release,
            "version": target_version,
            "org_id": org_id,
            "project_id": resolved_project_id,
            "output": output,
        }

    if retcode and retcode != 0:
        return {
            "error": (
                f"blastoff exited with code {retcode}. "
                + (
                    "A real release requires a GitHub token (GH_TOKEN) in the "
                    "MCP server's environment; check that it is configured. "
                    if release
                    else ""
                )
                + "See 'output' for details."
            ),
            "alias": resolved_alias,
            "released": release,
            "version": target_version,
            "org_id": org_id,
            "project_id": resolved_project_id,
            "output": output,
        }

    result: Dict[str, Any] = {
        "status": "released" if release else "preview",
        "alias": resolved_alias,
        "released": release,
        "hotfix": hotfix,
        "version": target_version,
        "org_id": org_id,
        "project_id": resolved_project_id,
    }

    # **The facts, parsed, not the printed page.** On a preview the engine emits
    # one JSON document; hand that straight over so the caller can write the
    # summary from numbers rather than from a formatted report. `output` stays
    # for the execute path (which streams per-repo tagging results) and as a
    # fallback if the document does not parse.
    if not release:
        try:
            result["data"] = json.loads(output)
        except (ValueError, TypeError):
            result["output"] = output
            result["warning"] = (
                "Could not parse the engine's JSON. Something printed above it — "
                "see 'output'."
            )
        else:
            if summary:
                result["data"]["summary"] = summary
            result["next_step"] = (
                "Write the summary from data.repos unless data.summary is "
                "already set, show it to the caller with the report, and call "
                "again with release=True and that summary once they approve."
            )
    else:
        result["output"] = output

    return result


@app.tool()
async def get_scrum_summary(
    project_id: str = Field(description="Project ID or alias to summarize"),
    scope: str = Field(
        default="scrum",
        description="'scrum' for the whole team, 'me' for the caller's own work",
    ),
    window: str = Field(
        default="3d",
        description=(
            "How far back to look: a duration like '3d', '12h' or '2w', or "
            "'day'/'week'. Normalised server-side. Ignored when `release` is set."
        ),
    ),
    release: Optional[str] = Field(
        default=None,
        description=(
            "Scope to one release instead of a window: a version string, or "
            "'current' for the version this project is cutting. Tickets on any "
            "other release — and tickets on none, which is most of them — are "
            "not assembled at all, so this replaces `window` rather than "
            "narrowing it."
        ),
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    🚀 Assemble what actually moved on a project — tickets, branches, PRs — over
    a window, for the whole team (`scope="scrum"`) or just you (`scope="me"`).

    Pass `release` to scope the summary to one version instead of a window. It is
    a **narrower ticket universe**, not a filter to apply afterwards: what comes
    back is only that release's work, and `tickets_without_release_count` tells
    you how much of the project it left out. Say that boundary once in your prose
    — a slice reported without it reads as the whole project.

    This calls InnoDay's summary engine, which runs three gates before it does
    any work: it skips syncing if the boards are under an hour fresh, returns a
    cached summary if one was written in the last hour, and reuses the existing
    prose when the source fingerprint says nothing changed.

    **It does not write prose, and no LLM runs server-side.** You are the
    narrator: read `active` / `no_work_detected` / `unassigned_work_happening`
    / `up_next`, write the words, then call `save_project_summary` to persist
    them. Same two-step split as get_board_summary_data / save_board_summary.

    `outcome` tells you whether there is anything to write:
      • `assembled` — fresh data, needs narrating 🚀
      • `unchanged` — same fingerprint; `body_markdown` is still accurate
      • `cached`    — written under an hour ago; reuse it
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    params: Dict[str, Any] = {
        "summary_type": "scrum" if scope == "scrum" else "personal",
    }
    # A release and a window are alternative scopes, so exactly one is sent:
    # passing both would leave which one won up to the server to decide.
    if release:
        params["release"] = release
    else:
        params["window_spec"] = window
    if scope != "scrum":
        # The engine resolves 'me' against the bearer token, so the MCP server
        # never has to know (or assert) which user it is acting for.
        params["user_id"] = "me"

    data = await _api.get(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/summary-data",
        params=params,
    )
    if isinstance(data, dict) and "error" in data:
        return data

    outcome = data.get("outcome")
    steps = [
        f"🚀 Gates cleared — synced: {bool(data.get('synced'))}",
        f"🚀 Window {data.get('window_spec')} · scope {scope} · outcome {outcome}",
        f"🚀 {data.get('footer')}",
    ]
    if outcome == "assembled":
        steps.append("🚀 Your turn: write the prose, then save_project_summary")
    else:
        steps.append("🚀 Nothing changed — the cached prose still stands")
    if scope != "scrum":
        # The id the engine resolved 'me' to. save_project_summary needs it
        # back verbatim; without it the personal summary is written into the
        # team slot and the personal cache never hits again.
        steps.append(f"🚀 Echo user_id={data.get('user_id')} back when you save")

    data["progress"] = steps
    data["scope"] = scope
    return data


@app.tool()
async def save_project_summary(
    project_id: str = Field(description="Project ID or alias the summary is for"),
    window_spec: str = Field(
        description=(
            "The window this covers, echoed back from get_scrum_summary — a "
            "duration like '3d', '12h' or '2w', or 'day'/'week'. Required: it "
            "is the cache key. Spelling is normalised server-side, so '3D' and "
            "'day' are safe, but echoing back what you were given is still the "
            "only way to be sure you are writing the window you summarised."
        )
    ),
    summary: str = Field(
        description="The summary prose YOU wrote from get_scrum_summary's output"
    ),
    notes: Optional[str] = Field(
        default=None,
        description=(
            "A person's own words to store beside your prose — their comment on "
            "the stand-up, not yours. Kept in a separate field so regenerating "
            "the summary never overwrites it. Omit (or send blank) to leave any "
            "existing note untouched. Do not put your own narration here."
        ),
    ),
    clear_notes: bool = Field(
        default=False,
        description=(
            "Delete the existing note. Only set this when the person asked you "
            "to remove it — it is the one way to destroy a note, and it is a "
            "separate flag precisely so that no blank string can do it by "
            "accident."
        ),
    ),
    scope: str = Field(
        default="scrum",
        description="'scrum' for the team roll-up, 'me' for one person's summary",
    ),
    user_id: Optional[str] = Field(
        default=None,
        description=(
            "Whose summary this is. **Required when scope='me'** — echo back "
            "the `user_id` get_scrum_summary returned, which is the id it "
            "resolved for you. Omit only for the team roll-up (scope='scrum')."
        ),
    ),
    items: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description=(
            "Per-ticket lines, echoed from the assembled blocks with your "
            "per-ticket prose in `body_markdown`. This is what makes tomorrow's "
            "summary read as a continuation rather than a fresh description. "
            "**Echo each line's `ticket_id`, `ticket_ref` and `assignee_user_id` "
            "unchanged** -- they are what tie your prose to a ticket and a "
            "person. A line that arrives without them is stored as work on no "
            "ticket, owned by nobody, and is shown that way."
        ),
    ),
    source_fingerprint: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "**Leave this out.** The server recomputes it. It is every ticket "
            "id + status and every commit sha in the window — tens of thousands "
            "of tokens of hex to carry a value the server just calculated. Pass "
            "one only if you specifically need the fingerprint frozen at "
            "assemble time rather than at save time."
        ),
    ),
    generated_by: str = Field(
        default="agent",
        description=(
            "Who wrote the prose: 'agent' if you wrote it unattended, 'hybrid' "
            "if the person edited your draft, 'human' if they wrote it. Say "
            "which you saved."
        ),
    ),
    highlights: Optional[List[str]] = Field(
        default=None, description="Key positive points worth surfacing"
    ),
    concerns: Optional[List[str]] = Field(
        default=None, description="Blockers or risks that need attention"
    ),
    project_dir: Optional[str] = Field(
        default=None,
        description=(
            "Path to the project's workspace directory. Read for the org and "
            "project in its `.innoday/project.yml`, exactly as the CLI's --dir "
            "does. Pass this whenever the project is not the one this server "
            "was started in: the configured organization comes from that "
            "startup directory and is wrong for every other project, which "
            "surfaces as 'Project belongs to a different organization'."
        ),
    ),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID (uses default if not provided)"
    ),
) -> Dict[str, Any]:
    """
    🚀 Persist the project summary YOU just wrote. The second half of the
    two-step flow — no LLM call happens here, it is a plain write.

    The previous live summary for this scope and window is *superseded*, not
    overwritten: it keeps a `superseded_by_id` pointing at this one, so the
    history survives and "the current summary" stays expressible.

    Echo `window_spec` back exactly as get_scrum_summary returned it — it is
    the cache key, and a re-spelling is a permanent cache miss.
    `source_fingerprint` is **not** yours to carry: omit it and the server
    computes it. It used to be required back, which meant shuttling ~28 KB of
    shas through the narrator to hand the server a value it had just produced.

    A `scrum` save also writes one `scrum_summary` entry to the project
    timeline, **one per calendar day**, rewritten in place on a second run — a
    stand-up is a snapshot, not an event that happened twice. A `me` save
    writes no timeline entry: one person's read of their own work is not a
    project event. Read either back with `get_project_timeline`.
    """
    org_id = _api.resolve_org(organization_id, project_dir)
    if not org_id:
        return {"error": "Organization ID required but not configured"}

    if scope != "scrum" and not user_id:
        # Refused here rather than forwarded. `user_id=None` alongside
        # `summary_type=personal` is not "a personal summary for whoever is
        # calling" -- `user_id IS NULL` is exactly what the *team* roll-up
        # means, so the row lands in the team slot and no personal read ever
        # finds it again. The route answers 422 for the same reason; this is
        # the earlier, more useful message, naming where to get the value.
        return {
            "error": (
                "scope='me' needs a user_id — echo back the `user_id` field "
                "get_scrum_summary returned (it resolves 'me' against your "
                "token). Without it the summary is stored as the team roll-up "
                "and no personal read will ever find it."
            )
        }

    payload: Dict[str, Any] = {
        "summary_type": "scrum" if scope == "scrum" else "personal",
        "window_spec": window_spec,
        "body_markdown": summary,
        "items": items or [],
        "source_fingerprint": source_fingerprint or {},
        "generated_by": generated_by,
    }
    if scope != "scrum":
        payload["user_id"] = user_id
    if highlights is not None:
        payload["highlights"] = highlights
    if concerns is not None:
        payload["concerns"] = concerns

    # **A blank `notes` is never destructive here.** The API treats `""` as
    # "clear it", which is the right primitive for a program but the wrong one
    # to hand an LLM: a model filling in an optional string it has nothing for
    # routinely emits `""`, and that would silently delete a note somebody
    # typed. So blank is dropped from the payload (= inherit), and deleting
    # takes the explicit `clear_notes` flag, which nothing emits by accident.
    # `is True`, not truthiness. An unresolved pydantic `FieldInfo` default is
    # truthy, and this tool has already shipped one such leak unnoticed
    # (`generated_by`) -- on a flag whose whole job is deleting somebody's
    # words, "probably a bool" is not good enough.
    wants_clear = clear_notes is True
    has_note = isinstance(notes, str) and notes.strip()
    if wants_clear and has_note:
        # Refused rather than resolved. "Replace my note with X" reasonably
        # produces both, and silently letting `clear` win would delete the old
        # note, drop the replacement, and return success -- the worst of the
        # three possible outcomes, and invisible to whoever asked.
        return {
            "error": (
                "clear_notes=true was sent together with a note. Send the new "
                "text in `notes` to replace one, or clear_notes=true alone to "
                "delete it — not both."
            )
        }
    if wants_clear:
        payload["notes_markdown"] = ""
    elif has_note:
        payload["notes_markdown"] = notes

    result = await _api.post(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/summaries",
        json=payload,
    )
    if isinstance(result, dict) and "error" not in result:
        result["progress"] = [
            f"🚀 Saved — {window_spec} {payload['summary_type']} summary",
            f"🚀 {len(payload['items'])} item(s) recorded; previous summary superseded",
        ]
    return result


@app.tool()
async def get_project_timeline(
    project_id: str = Field(description="Project ID or alias"),
    event_type: Optional[str] = Field(
        default=None,
        description=(
            "Only this kind of event: scrum_summary, release, release_created, "
            "release_updated, meeting, spec_update, repo_added, repo_removed, "
            "ticket_sync, board_attached"
        ),
    ),
    limit: int = Field(default=20, description="How many entries (max 200)"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    📋 A project's curated event history, newest first — releases, board
    attachments, ticket syncs, repo changes, and the daily scrum summary.

    This is the answer to "what has actually happened on this project", as
    opposed to `get_all_work` (what is open now) or `get_scrum_summary` (what
    moved in a window). Entries are written by the mutations they describe, so
    each one landed in the same transaction as the change it records — the feed
    cannot claim a release that did not happen.

    Read-only. There is no MCP tool to append an entry, deliberately: a feed
    anyone can write becomes a notes field, and `add_project_update` /
    `update_project_scope` already own that job.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    params: Dict[str, Any] = {"limit": max(1, min(200, limit))}
    if event_type:
        params["event_type"] = str(event_type).lower()

    data = await _api.get(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/timeline",
        params=params,
    )
    if isinstance(data, dict) and "error" in data:
        return data

    entries = data.get("entries") or []
    data["progress"] = [
        f"📋 {len(entries)} timeline entr{'y' if len(entries) == 1 else 'ies'}"
        + (f" of type {event_type}" if event_type else ""),
    ]
    if data.get("next_cursor"):
        data["progress"].append("📋 More exist — raise `limit` to see further back")
    return data


@app.tool()
async def get_assignment_summary(
    project_id: str = Field(description="Project ID to summarize"),
    organization_id: Optional[str] = Field(
        default=None, description="Organization ID or slug (uses default if omitted)"
    ),
) -> Dict[str, Any]:
    """
    Get a project's open tickets grouped by assignee.

    Groups non-done tickets by their `assignee` field (falling back to
    "unassigned" when not set) so you can see who's working on what.
    Assignee is returned as the raw identifier stored on the ticket
    (name or external-board username) — this tool does not resolve it
    to a user record.
    """
    org_id = _api.resolve_org(organization_id)
    if not org_id:
        return {
            "error": "organization_id required — pass it explicitly, or launch from a "
            "directory with .innoday/project.yml so it resolves automatically"
        }

    tickets = await _api.get(
        f"/api/v1/organizations/{org_id}/projects/{project_id}/tickets"
    )
    if isinstance(tickets, dict) and "error" in tickets:
        return tickets

    by_assignee: Dict[str, List[Dict[str, Any]]] = {}
    for t in tickets:
        if t.get("status") == "done":
            continue
        assignee = t.get("assignee") or "unassigned"
        by_assignee.setdefault(assignee, []).append(
            {
                "id": t.get("id"),
                "summary": t.get("summary"),
                "status": t.get("status"),
                "url": t.get("url"),
            }
        )

    return {
        "project_id": project_id,
        "organization_id": org_id,
        "by_assignee": by_assignee,
        "assignee_counts": {k: len(v) for k, v in by_assignee.items()},
        "total_open": sum(len(v) for v in by_assignee.values()),
    }


# =============================================================================
# Server Runner
# =============================================================================


def run_server():
    """Run the MCP server"""
    import logging

    # Configure logging
    if config.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Run the FastMCP server
    app.run(transport="stdio")


if __name__ == "__main__":
    run_server()
