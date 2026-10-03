"""One source-aware interface for Claude Code and Codex plugin commands.

The two agents expose the same plugin lifecycle with a few spelling differences:
Claude uses ``install``/``uninstall``/``marketplace update`` while Codex uses
``add``/``remove``/``marketplace upgrade`` and can return JSON from ``list``.
Keeping those differences here prevents setup, doctor, capture, and updater from
each growing their own subprocess wrapper and verb table.
"""

from __future__ import annotations

import json
import shutil
import subprocess

from probe.cli import claude_cli

CLAUDE = "claude_code"
CODEX = "codex"


def binary_name(source: str) -> str:
    # Fail loud, never fall through to "claude": this module is the
    # claude/codex MARKETPLACE shim, and every non-codex source silently
    # resolving to the claude binary is the exact bug class the pi audit
    # closed (capture.py's uninstall used to run `claude plugin uninstall`
    # for a pi device through exactly this fallthrough). pi installs go
    # through pi_config's settings.json entry and must branch before ever
    # reaching this module.
    if source == CLAUDE:
        return "claude"
    if source == CODEX:
        return "codex"
    raise ValueError(
        f"plugin_cli has no binary for agent source {source!r} -- claude_code and "
        "codex only; pi routes through pi_config, never a marketplace CLI"
    )


def available(source: str) -> bool:
    return shutil.which(binary_name(source)) is not None


def run(source: str, args: list[str], *, timeout: float) -> claude_cli.Result:
    """Run an agent CLI with captured output and closed stdin. A source with no
    marketplace CLI is refused by name: falling through to `claude` once ran
    Claude Code's plugin commands on a pi device's behalf."""
    binary_name(source)  # raises for anything but the two marketplace harnesses
    if source == CLAUDE:
        return claude_cli.run(args, timeout=timeout)
    command = " ".join(["codex", *args])
    binary = shutil.which("codex")
    if not binary:
        return claude_cli.Result(
            ok=False, detail="`codex` not found on PATH", reachable=False, command=command
        )
    try:
        completed = subprocess.run(  # noqa: S603 - fixed binary, no shell
            [binary, *args],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return claude_cli.Result(
            ok=False, detail=f"timed out after {timeout:.0f}s", reachable=False, command=command
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return claude_cli.Result(ok=False, detail=str(exc), reachable=False, command=command)
    out = (completed.stdout or "").strip()
    err = (completed.stderr or "").strip()
    if completed.returncode != 0:
        return claude_cli.Result(ok=False, detail=err or out, command=command)
    return claude_cli.Result(ok=True, detail=out, command=command)


#: Each marketplace CLI's own verbs. A dialect of the two binaries, so it lives
#: here and nowhere else; `binary_name` refuses any other source first.
_VERBS = {
    CLAUDE: {"refresh": "update", "install": "install", "uninstall": "uninstall", "list": ("plugin", "list")},
    CODEX: {"refresh": "upgrade", "install": "add", "uninstall": "remove", "list": ("plugin", "list", "--json")},
}


def _verb(source: str, action: str):
    binary_name(source)
    return _VERBS[source][action]


def refresh_verb(source: str) -> str:
    return _verb(source, "refresh")


def install_verb(source: str) -> str:
    return _verb(source, "install")


def list_plugins(source: str) -> claude_cli.Result:
    return run(source, list(_verb(source, "list")), timeout=claude_cli.LIST_TIMEOUT_S)


def add_marketplace(source: str, location: str) -> claude_cli.Result:
    return run(
        source,
        ["plugin", "marketplace", "add", location],
        timeout=claude_cli.REFRESH_TIMEOUT_S,
    )


def refresh_marketplace(source: str, marketplace: str) -> claude_cli.Result:
    return run(
        source,
        ["plugin", "marketplace", refresh_verb(source), marketplace],
        timeout=claude_cli.REFRESH_TIMEOUT_S,
    )


def install(source: str, plugin_id: str) -> claude_cli.Result:
    return run(
        source,
        ["plugin", install_verb(source), plugin_id],
        timeout=claude_cli.INSTALL_TIMEOUT_S,
    )


def uninstall(source: str, plugin_id: str) -> claude_cli.Result:
    return run(
        source,
        ["plugin", _verb(source, "uninstall"), plugin_id],
        timeout=claude_cli.INSTALL_TIMEOUT_S,
    )


def codex_mcp_auth_status(name: str) -> str | None:
    """Return Codex's auth status for one installed MCP, if observable."""
    result = run(CODEX, ["mcp", "list", "--json"], timeout=claude_cli.LIST_TIMEOUT_S)
    if not result.ok:
        return None
    try:
        servers = json.loads(result.detail)
    except (TypeError, ValueError):
        return None
    if not isinstance(servers, list):
        return None
    for server in servers:
        if isinstance(server, dict) and server.get("name") == name:
            status = server.get("auth_status")
            return str(status) if status is not None else None
    return None


def login_codex_mcp(name: str) -> claude_cli.Result:
    """Run Codex's supported OAuth flow for a plugin-provided MCP server."""
    return run(CODEX, ["mcp", "login", name], timeout=180.0)
