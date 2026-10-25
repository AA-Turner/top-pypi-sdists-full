"""`probe mcp tools` / `probe mcp call`: the hosted Probe MCP from the shell, for
`/probe inline` only.

WHY A BRIDGE. Where the Probe daemon records (the lean `probe-research-daemon`
plugin), the agent has no Probe MCP tools: the daemon reads for it. When the
researcher types `/probe inline` the daemon stops and the agent reads Probe
itself -- but a coding agent cannot gain MCP tools mid-session (Codex and Kimi
ignore `notifications/tools/list_changed`; only Claude Code refetches), and most
of the read surface (`browse`, `search`, `entity`, `metrics`,
`query_sql`, `find_papers`) has no CLI command. So the CLI proxies the hosted MCP
itself, over the same streamable HTTP an MCP client uses.

A PURE PROXY: no per-tool code. `tools` prints what the server lists (its
`instructions`, each tool's name, description and input schema) and `call`
prints what the tool returned, so a new hosted tool appears here with no CLI
release and the read surface never forks: ONE read method, the MCP's.

NOT THERE OUTSIDE INLINE. Both commands are hidden from `--help`, and both
refuse (exit 2, one line) unless the calling coding-agent session is inline
(`session_marker.is_inline`): an agent the daemon reads for asks it
(`probe ask`), and everywhere else the Probe MCP tools are the read surface. The
check lives here, in the CLI, so it holds however the call is wrapped
(`probe exec`, `bash -lc`, a script), like the switch refusals.

THE CALLER IS NAMED. Every request carries the MCP read token (`mcp_token`, the
same resolution as `probe mcp headers`) and this session's `X-Probe-Agent` /
`X-Probe-Agent-Session`, but never `X-Probe-Hide-Session-Work`: that opt-in is
the daemon reader's, and an inline agent's own records are its work to read.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from ..sdk import agent_session, session_marker

#: Exit code for a refusal: the command is not available in this session (the
#: same code as `probe session state inline` refused inside an agent).
EXIT_NOT_INLINE = 2

#: The refusal outside `/probe inline` where no daemon reads for the agent: the
#: agent profile (it has the Probe MCP tools), or no coding agent session at all.
NOT_INLINE_DENY = (
    "`{matched}` was refused before it ran: it exists only for a session the researcher set to "
    "`/probe inline`. Everywhere else the Probe MCP tools are the read surface."
)

#: Seconds the WHOLE command may take -- connect, initialize, every page, the
#: call and the cleanup -- inside the two minutes a coding agent's shell call
#: gets by default. Read at call time (tests shorten it).
TOTAL_TIMEOUT_S = 100.0
#: Per-request bounds, never past the total.
CONNECT_TIMEOUT_S = 30.0
READ_TIMEOUT_S = TOTAL_TIMEOUT_S


class BridgeError(Exception):
    """A failure to report as one `error: ...` line (exit 1)."""


def refusal(matched: str, env: Mapping[str, str] | None = None) -> str | None:
    """Why `matched` (`probe mcp tools` / `probe mcp call`) may not run in this
    shell, or None when the session is inline. The ONE gate both commands use."""
    resolved = agent_session.session_agent_from_env(env)
    if resolved is None:
        return NOT_INLINE_DENY.format(matched=matched)
    agent, session_id = resolved
    state = session_marker.session_state(session_id)
    if session_marker.is_inline(session_id, state):
        return None
    if state == session_marker.STATE_OFF:
        return session_marker.DENY_REASON_OFF.format(matched=matched)
    if state == session_marker.STATE_DAEMON or session_marker.daemon_session(session_id, agent):
        # The daemon reads for this session: the guard's own answer (`probe ask`).
        return session_marker.DAEMON_PROFILE_DENY.format(matched=matched)
    return NOT_INLINE_DENY.format(matched=matched)


@dataclass(frozen=True)
class Target:
    """Where the bridge sends its requests, and the headers it sends."""

    url: str
    headers: dict[str, str]


def target(base_url: str | None = None, env: Mapping[str, str] | None = None) -> Target:
    """The hosted MCP for this device's context (`mcp_url`, which honours
    `PROBE_MCP_URL`) and its headers: the read token (`PROBE_MCP_TOKEN`, then the
    context's `mcp_token`), this session, and the CLI's version."""
    from .. import __version__
    from ..client_headers import client_version_headers
    from ..sdk.config import mcp_url, resolve

    settings = resolve(base_url=base_url)
    url = mcp_url(settings.base_url)
    if not url:
        raise BridgeError(
            f"no Probe MCP is known for {settings.base_url}: set PROBE_MCP_URL to its MCP endpoint"
        )
    if not settings.mcp_token:
        raise BridgeError(
            f"no MCP token: set PROBE_MCP_TOKEN, or the wizard's Install mints one ({session_marker.WIZARD_HINT})"
        )
    headers = {"Authorization": f"Bearer {settings.mcp_token}"}
    resolved = agent_session.session_agent_from_env(env)
    if resolved is not None:
        headers[agent_session.AGENT_HEADER] = resolved[0]
        headers[agent_session.AGENT_SESSION_HEADER] = resolved[1]
    headers.update(client_version_headers("cli", __version__))
    # This computer's workspace limit: the hosted MCP forwards it on its API calls.
    from ..sdk.workspace_limit import headers_or_fail_closed

    headers.update(headers_or_fail_closed(settings, bearer=settings.mcp_token))
    return Target(url=url, headers=headers)


@asynccontextmanager
async def _session(where: Target) -> AsyncIterator[tuple[Any, Any]]:
    """An initialized MCP `ClientSession` on `where`, and the server's
    `InitializeResult` (its `instructions`)."""
    import httpx
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    from ..sdk.tls import ssl_context

    timeout = httpx.Timeout(CONNECT_TIMEOUT_S, read=READ_TIMEOUT_S)
    async with httpx.AsyncClient(headers=dict(where.headers), timeout=timeout, verify=ssl_context()) as http:
        async with streamable_http_client(where.url, http_client=http) as (read, write, _):
            async with ClientSession(read, write) as session:
                yield session, await session.initialize()


async def _list(where: Target) -> tuple[str, list[Any]]:
    import anyio
    from mcp import types

    with anyio.fail_after(TOTAL_TIMEOUT_S):
        async with _session(where) as (session, init):
            tools: list[Any] = []
            cursor: str | None = None
            while True:
                page = await session.list_tools(
                    params=types.PaginatedRequestParams(cursor=cursor) if cursor else None
                )
                tools.extend(page.tools)
                cursor = page.nextCursor
                if not cursor:
                    break
            return (init.instructions or "", tools)


async def _call(where: Target, name: str, arguments: dict) -> Any:
    import anyio

    with anyio.fail_after(TOTAL_TIMEOUT_S):
        async with _session(where) as (session, _init):
            return await session.call_tool(name, arguments)


def _run(coro_fn: Any, *args: Any) -> Any:
    """Run one bridge request, turning every transport failure into a BridgeError."""
    import anyio

    try:
        return anyio.run(coro_fn, *args)
    except BridgeError:
        raise
    except BaseException as exc:  # noqa: BLE001 -- task groups wrap the cause
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        raise BridgeError(_describe(exc)) from exc


def _describe(exc: BaseException) -> str:
    """One line for what went wrong: the innermost cause a task group wrapped,
    an HTTP status as the server gave it, an MCP error as its message."""
    import httpx

    while isinstance(getattr(exc, "exceptions", None), (list, tuple)) and exc.exceptions:  # type: ignore[attr-defined]
        exc = exc.exceptions[0]  # type: ignore[attr-defined]
    if isinstance(exc, ModuleNotFoundError):
        return f"this install has no MCP client (missing: {exc.name}): pip install 'probe-research[all]'"
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        hint = " (`probe mcp status` checks the token)" if status in (401, 403) else ""
        return f"the Probe MCP answered HTTP {status} {exc.response.reason_phrase}{hint}"
    if isinstance(exc, (TimeoutError, httpx.ReadTimeout, httpx.WriteTimeout, httpx.PoolTimeout)):
        return f"the Probe MCP did not answer within {TOTAL_TIMEOUT_S:g} s"
    if isinstance(exc, httpx.TransportError):
        return f"could not reach the Probe MCP: {type(exc).__name__}: {exc}"
    try:
        from mcp.shared.exceptions import McpError

        if isinstance(exc, McpError):
            return f"the Probe MCP refused the request: {exc.error.message}"
    except ImportError:  # pragma: no cover -- mcp is a dependency of every install that has this
        pass
    return f"{type(exc).__name__}: {exc}" if str(exc) else type(exc).__name__


def list_tools(where: Target) -> tuple[str, list[Any]]:
    """`(instructions, tools)` exactly as the server sends them."""
    return _run(_list, where)


def call_tool(where: Target, name: str, arguments: dict) -> Any:
    """The tool's `CallToolResult`, exactly as the server sends it."""
    return _run(_call, where, name, arguments)


def parse_arguments(raw: str | None) -> dict:
    """The tool's arguments: a JSON object (none given is `{}`)."""
    if raw is None or not raw.strip():
        return {}
    try:
        value = json.loads(raw)
    except ValueError as exc:
        raise ValueError(f"the arguments are not JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"the arguments must be a JSON object, got {type(value).__name__}")
    return value


def result_text(result: Any) -> str:
    """What the tool returned, verbatim: text blocks as they are, any other block
    as its JSON, and the structured content as JSON when that is all there is."""
    parts: list[str] = []
    for block in result.content or []:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
        else:
            parts.append(json.dumps(block.model_dump(mode="json", by_alias=True, exclude_none=True)))
    if not parts and result.structuredContent is not None:
        parts.append(json.dumps(result.structuredContent, indent=2))
    return "\n".join(parts)


def _argument_line(schema: Mapping[str, Any]) -> str:
    properties = schema.get("properties") if isinstance(schema, Mapping) else None
    names = list(properties) if isinstance(properties, Mapping) else []
    required = set(schema.get("required") or []) if isinstance(schema, Mapping) else set()
    if not names:
        return "arguments: none"
    return "arguments: " + ", ".join(f"{name} (required)" if name in required else name for name in names)


def render_tools(instructions: str, tools: Sequence[Any], names: Sequence[str] = ()) -> str:
    """The listing `probe mcp tools` prints.

    Every tool, with no names: the server's `instructions` once at the top, then
    each tool's name, argument names and description. The full input schemas
    together run past what a coding agent's shell shows (~38 KB for six tools),
    so a tool's schema prints when it is named: `probe mcp tools <tool>`.
    Raises KeyError naming a tool the server does not serve.
    """
    by_name = {tool.name: tool for tool in tools}
    missing = [name for name in names if name not in by_name]
    if missing:
        raise KeyError(", ".join(missing))
    out: list[str] = []
    if not names:
        if instructions.strip():
            out += ["# How to read Probe (the Probe MCP's instructions)", "", instructions.strip(), ""]
        out += [
            "# Tools",
            "",
            "Run one: probe mcp call <tool> '<json args>'. Its full input schema: probe mcp tools <tool>.",
            "",
        ]
        for tool in tools:
            out += [f"## {tool.name}", _argument_line(tool.inputSchema), "", (tool.description or "").strip(), ""]
    else:
        for name in names:
            tool = by_name[name]
            out += [
                f"## {tool.name}",
                "",
                (tool.description or "").strip(),
                "",
                "input schema:",
                json.dumps(tool.inputSchema, indent=2),
                "",
            ]
    return "\n".join(out).rstrip("\n")
