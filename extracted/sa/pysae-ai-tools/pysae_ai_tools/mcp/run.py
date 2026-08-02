"""``pysae-ai-tools mcp run <server>`` — the MCP resolver shim.

Resolves the named server's secrets at launch (env → AWS Secrets Manager → CLI),
runs any idempotent side effects it needs (a dedicated kubeconfig, a browser
profile dir), then **execs** the real MCP server. No secret is ever written to
disk: the plugin manifest (Claude) and the Codex config only ever carry
``pysae-ai-tools mcp run <server>``.

``os.execvpe`` (POSIX) replaces this process image with the real server — same
PID, one long-lived stdio process per session exactly like a direct config, and
the orphan-cleanup hook still matches the real command line. Windows has no
reliable ``exec`` and no orphan cleanup, so there we spawn-and-wait, forwarding
stdio through inherited handles.

Resolution output would corrupt the MCP stdio protocol, so it runs under
``silence_trace()`` — nothing but the server's own bytes ever reach stdout.
"""

import json
import os
import subprocess
import sys
from typing import Annotated, NoReturn

import typer

from ..common.winpath import spawnable

# JSON-RPC application error code, matching what Claude shows when a stdio MCP
# server dies before the handshake (``-32000``). We reuse it so the shim's
# initialize-error reply reads as the same class of failure — only with a
# message instead of a bare "Connection closed".
_MCP_SERVER_ERROR = -32000


def _find_mcp_tool(server: str):  # type: ignore[no-untyped-def]
    """Return the ``McpTool`` instance owning ``server``, or None."""
    from ..install.registry import TOOLS, Category, _instance

    for entry in TOOLS:
        if entry.category is not Category.MCP:
            continue
        try:
            instance = _instance(entry.module)
        except Exception:  # noqa: BLE001
            continue
        if server in instance.mcp_server_names():
            return instance
    return None


def _missing_config_message(server: str, tool: object, missing: list[str]) -> str:
    """A self-contained, actionable message for a server whose secrets are unset."""
    help_map: dict[str, str] = getattr(tool, "env_help", {})
    lines = [
        f"MCP server '{server}' not configured: set {', '.join(missing)} "
        f"(run: pysae-ai-tools env resolve {missing[0]}) "
        f"or deselect it via `pysae-ai-tools tools install`."
    ]
    lines += [f"  {var}: {help_map[var]}" for var in missing if help_map.get(var)]
    return "\n".join(lines)


def _reply_mcp_initialize_error(message: str) -> None:
    """Best-effort: answer the MCP ``initialize`` request with a JSON-RPC error.

    A server that just closes its pipe leaves Claude showing a bare ``-32000
    Connection closed`` in the ``/mcp`` summary. By reading the client's first
    message and replying with a JSON-RPC error carrying ``message``, we give
    Claude a reason to show instead. Never raises and never blocks beyond the
    first line: a no-op when there is no MCP client on stdin (e.g. a plain CLI
    invocation or a test)."""
    try:
        # Only a real MCP client talks to us over a pipe. On an interactive
        # terminal (a developer running `mcp run <server>` by hand), reading
        # stdin would block waiting for keyboard input instead of exiting.
        if sys.stdin is None or sys.stdin.isatty():
            return
        # readline() returns as soon as one line is available (no read-ahead
        # buffering, so we never wait past the client's initialize).
        while True:
            raw = sys.stdin.readline()
            if raw == "":  # EOF — client closed without initializing
                return
            line = raw.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                return
            if isinstance(request, dict) and request.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": _MCP_SERVER_ERROR, "message": message},
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            return
    except Exception:  # noqa: BLE001
        return


def _fail(message: str) -> NoReturn:
    """Report a startup failure to both the logs (stderr) and — best effort — the
    MCP client (an initialize error), then exit non-zero."""
    typer.echo(message, err=True)
    _reply_mcp_initialize_error(message)
    raise typer.Exit(code=1)


def main(
    server: Annotated[str, typer.Argument(help="MCP server name (e.g. gitlab, datadog, kubernetes-dev)")],
) -> None:
    """Resolve ``server``'s secrets and exec the real MCP server."""
    from ..env import trace
    from ..env.resolve import try_auto_resolve

    tool = _find_mcp_tool(server)
    if tool is None:
        _fail(f"mcp run: unknown MCP server '{server}'")

    with trace.silence_trace():
        for var in tool.env_required:
            if not os.environ.get(var):
                try_auto_resolve(var)

    # A missing required var is the common, actionable failure — name it explicitly
    # instead of letting build_config raise a terse "VAR must be set".
    missing = [var for var in tool.env_required if not os.environ.get(var)]
    if missing:
        _fail(_missing_config_message(server, tool, missing))

    try:
        with trace.silence_trace():
            tool.prepare()
            config = tool.build_config()
    except Exception as exc:  # noqa: BLE001
        _fail(f"MCP server '{server}' could not start: {exc}")

    command = config["command"]
    args = [str(a) for a in config.get("args", [])]
    child_env = {**os.environ, **{k: str(v) for k, v in config.get("env", {}).items()}}

    if os.name == "posix":
        try:
            os.execvpe(command, [command, *args], child_env)
        except OSError as exc:
            typer.echo(f"mcp run: failed to exec '{command}': {exc}", err=True)
            raise typer.Exit(code=1) from exc
    else:
        # Windows: no reliable exec — spawn the server inheriting our stdio and
        # mirror its exit code so the MCP client sees a single stdio process.
        #
        # ``npx`` launches all but one of our MCP servers and is a ``.cmd`` shim,
        # which ``CreateProcess`` cannot spawn by bare name — see ``spawnable``.
        launcher = spawnable(command)
        try:
            completed = subprocess.run([launcher, *args], env=child_env, check=False)
        except OSError as exc:
            typer.echo(f"mcp run: failed to launch '{command}': {exc}", err=True)
            raise typer.Exit(code=1) from exc
        sys.exit(completed.returncode)
