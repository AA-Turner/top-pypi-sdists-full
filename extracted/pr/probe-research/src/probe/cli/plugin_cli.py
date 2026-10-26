"""One source-aware interface for the hook-plugin harnesses' plugin commands.

Claude Code and Codex expose the same plugin lifecycle with a few spelling
differences: Claude uses ``install``/``uninstall``/``marketplace update`` while
Codex uses ``add``/``remove``/``marketplace upgrade`` and can return JSON from
``list``. Kimi Code has no plugin command a shell can run, so its install,
uninstall and list go to ``kimi_config``, which edits Kimi's own plugin list.
Keeping those differences here prevents setup, doctor, capture, and updater from
each growing their own subprocess wrapper and verb table.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
import subprocess  # noqa: F401 - tests patch `plugin_cli.subprocess.run`; the call is `claude_cli.capture`

from probe.cli import claude_cli

CLAUDE = "claude_code"
CODEX = "codex"
KIMI = "kimi_code"


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
    if source == KIMI:
        return "kimi"
    raise ValueError(
        f"plugin_cli has no binary for agent source {source!r} -- claude_code, codex "
        "and kimi_code only; pi routes through pi_config, never a marketplace CLI"
    )


def available(source: str) -> bool:
    return shutil.which(binary_name(source)) is not None


def run(source: str, args: list[str], *, timeout: float) -> claude_cli.Result:
    """Run an agent CLI with captured output and closed stdin. A source with no
    marketplace CLI is refused by name: falling through to `claude` once ran
    Claude Code's plugin commands on a pi device's behalf."""
    binary_name(source)  # raises for anything but the hook-plugin harnesses
    if source == KIMI:
        raise ValueError("Kimi Code has no plugin command; kimi_config edits its plugin list")
    if source == CLAUDE:
        return claude_cli.run(args, timeout=timeout)
    command = " ".join(["codex", *args])
    binary = shutil.which("codex")
    if not binary:
        return claude_cli.Result(
            ok=False, detail="`codex` not found on PATH", reachable=False, command=command
        )
    return claude_cli.run_binary(binary, args, timeout=timeout, command=command)


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
    if source == KIMI:
        return _kimi().list_plugins()
    return run(source, list(_verb(source, "list")), timeout=claude_cli.LIST_TIMEOUT_S)


def _kimi():
    from probe.cli import kimi_config  # noqa: PLC0415

    return kimi_config


#: Codex's refusal when a checkout for the name is on disk but its config entry
#: is missing or points elsewhere. Lowercased; matched against lowercased output.
_CODEX_DIFFERENT_SOURCE = "already added from a different source"


def add_marketplace(source: str, location: str, *, name: str | None = None) -> claude_cli.Result:
    """Add a marketplace. On Codex, given its `name`, repair an ORPHANED checkout.

    Deleting the `[marketplaces.<name>]` table from `~/.codex/config.toml` (or
    the whole file) leaves `~/.codex/.tmp/marketplaces/<name>` behind, and
    `add` then refuses forever with "already added from a different source".
    `upgrade` fails as "not configured as a Git marketplace", every install
    fails as "not found in marketplace", and re-running the installer cannot
    fix any of it. `marketplace remove` clears the stale checkout even with no
    config entry, so the orphan is removed and `add` retried once.

    Only an orphan. A name Codex still lists is a source somebody configured
    (a fork, a local checkout under development) and is left alone; the
    refusal comes back with the command that would replace it.
    """
    if source == KIMI:
        return _kimi().refresh()
    args = ["plugin", "marketplace", "add", location]
    result = run(source, args, timeout=claude_cli.REFRESH_TIMEOUT_S)
    if (
        result.ok
        or source != CODEX
        or name is None
        or _CODEX_DIFFERENT_SOURCE not in (result.detail or "").lower()
    ):
        return result
    listed, configured = codex_marketplace_source(name)
    if not listed:
        return claude_cli.Result(
            ok=False,
            detail=(
                f"{result.detail} (could not list Codex's marketplaces to check whether `{name}` "
                f"is a stale checkout; `codex plugin marketplace remove {name}` clears it)"
            ),
            command=result.command,
        )
    if configured is not None:
        return claude_cli.Result(
            ok=False,
            detail=(
                f"Codex's `{name}` marketplace is configured from {configured or 'another source'}, "
                f"not {location}; run `codex plugin marketplace remove {name}` to use the published one"
            ),
            command=result.command,
        )
    removed = run(
        source, ["plugin", "marketplace", "remove", name], timeout=claude_cli.REFRESH_TIMEOUT_S
    )
    if not removed.ok:
        return claude_cli.Result(
            ok=False,
            detail=(
                f"a stale `{name}` checkout with no config entry blocks `marketplace add`, and "
                f"removing it failed: {removed.detail}"
            ),
            command=removed.command,
        )
    return run(source, args, timeout=claude_cli.REFRESH_TIMEOUT_S)


def codex_marketplace_source(name: str) -> tuple[bool, str | None]:
    """Whether Codex's marketplace listing was readable, and the source it has
    CONFIGURED for `name`: None for no entry, "" for an entry with no source.

    Unreadable is its own answer, not "no entry": the caller removes only a
    name with no entry, and a failed listing must never delete a fork.
    """
    result = run(
        CODEX, ["plugin", "marketplace", "list", "--json"], timeout=claude_cli.LIST_TIMEOUT_S
    )
    if not result.ok:
        return False, None
    try:
        payload = json.loads(result.detail)
    except (TypeError, ValueError):
        return False, None
    entries = payload.get("marketplaces") if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        return False, None
    for entry in entries:
        if isinstance(entry, dict) and entry.get("name") == name:
            src = entry.get("marketplaceSource")
            return True, str(src.get("source") or "") if isinstance(src, dict) else ""
    return True, None


def marketplace_checkout(source: str, name: str) -> Path | None:
    """Where `source` keeps its clone of the marketplace `name` (it need not
    exist), or None for a source with no clone. Claude Code: its plugins folder
    (`capabilities.claude_plugin_ledger`), `marketplaces/<name>`; Codex:
    `$CODEX_HOME/.tmp/marketplaces/<name>`."""
    if source == CLAUDE:
        from probe.cli.capabilities import claude_plugin_ledger  # noqa: PLC0415 - imports this module

        return claude_plugin_ledger().parent / "marketplaces" / name
    if source == CODEX:
        from probe.cli.codex_config import codex_home  # noqa: PLC0415

        return codex_home() / ".tmp" / "marketplaces" / name
    return None


def refresh_marketplace(source: str, marketplace: str) -> claude_cli.Result:
    if source == KIMI:
        return _kimi().refresh()
    return run(
        source,
        ["plugin", "marketplace", refresh_verb(source), marketplace],
        timeout=claude_cli.REFRESH_TIMEOUT_S,
    )


def install(source: str, plugin_id: str) -> claude_cli.Result:
    if source == KIMI:
        return _kimi().install_plugin(plugin_id.split("@", 1)[0])
    return run(
        source,
        ["plugin", install_verb(source), plugin_id],
        timeout=claude_cli.INSTALL_TIMEOUT_S,
    )


def uninstall(source: str, plugin_id: str) -> claude_cli.Result:
    if source == KIMI:
        return _kimi().uninstall_plugin(plugin_id.split("@", 1)[0])
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
