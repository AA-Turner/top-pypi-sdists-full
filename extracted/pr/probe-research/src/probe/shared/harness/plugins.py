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
import re
import shutil
from pathlib import Path
import subprocess  # tests patch `plugin_cli.subprocess.run`; the calls are `claude_cli.capture`

from probe.shared.harness.harness import PluginCli, get_integration
from probe.shared.harness.harnesses.claude_code import binary as claude_cli

CLAUDE = "claude_code"
CODEX = "codex"
KIMI = "kimi_code"


def _get_plugin_cli(source: str) -> PluginCli:
    # Fail loud, never fall through to "claude": this module is the
    # claude/codex MARKETPLACE shim, and every non-codex source silently
    # resolving to the claude binary is the exact bug class the pi audit
    # closed (capture.py's uninstall used to run `claude plugin uninstall`
    # for a pi device through exactly this fallthrough). pi installs go
    # through pi_config's settings.json entry and must branch before ever
    # reaching this module. An exact registry id only, never an alias.
    integration = get_integration(source)
    facet = integration.plugin_cli if integration is not None else None
    if facet is None:
        raise ValueError(
            f"plugin_cli has no binary for agent source {source!r} -- claude_code, codex "
            "and kimi_code only; pi routes through pi_config, never a marketplace CLI"
        )
    return facet


def _get_plugin_list(source: str):
    """The module that edits an agent's own plugin list (Kimi Code has no plugin command), else None."""
    integration = get_integration(source)
    facet = integration.plugin_cli if integration is not None else None
    return facet.plugin_list() if facet is not None and facet.plugin_list is not None else None


def binary_name(source: str) -> str:
    return _get_plugin_cli(source).binary


def available(source: str) -> bool:
    return shutil.which(binary_name(source)) is not None


def run(source: str, args: list[str], *, timeout: float) -> claude_cli.Result:
    """Run an agent CLI with captured output and closed stdin. A source with no
    marketplace CLI is refused by name: falling through to `claude` once ran
    Claude Code's plugin commands on a pi device's behalf."""
    facet = _get_plugin_cli(source)  # raises for anything but the hook-plugin harnesses
    if facet.no_command:
        raise ValueError(facet.no_command)
    if facet.run is not None:
        return facet.run(args, timeout=timeout)
    command = " ".join([facet.binary, *args])
    binary = shutil.which(facet.binary)
    if not binary:
        return claude_cli.Result(
            ok=False, detail=f"`{facet.binary}` not found on PATH", reachable=False, command=command
        )
    return claude_cli.run_binary(binary, args, timeout=timeout, command=command)


def _verb(source: str, action: str):
    """The marketplace CLI's own verb (`PluginCli.verbs`): a dialect of each binary."""
    return _get_plugin_cli(source).verbs[action]


def refresh_verb(source: str) -> str:
    return _verb(source, "refresh")


def install_verb(source: str) -> str:
    return _verb(source, "install")


def list_plugins(source: str) -> claude_cli.Result:
    plugin_list = _get_plugin_list(source)
    if plugin_list is not None:
        return plugin_list.list_plugins()
    return run(source, list(_verb(source, "list")), timeout=claude_cli.LIST_TIMEOUT_S)


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

    On Codex the add is sparse (`_codex_sparse_args`).
    """
    plugin_list = _get_plugin_list(source)
    if plugin_list is not None:
        return plugin_list.refresh()
    args = ["plugin", "marketplace", "add", location]
    if source == CODEX:
        args += _codex_sparse_args(name)
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
    integration = get_integration(source)
    facet = integration.plugin_cli if integration is not None else None
    return facet.checkout(name) if facet is not None and facet.checkout is not None else None


def refresh_marketplace(source: str, marketplace: str) -> claude_cli.Result:
    plugin_list = _get_plugin_list(source)
    if plugin_list is not None:
        return plugin_list.refresh()
    if source == CODEX and _git_can_sparse():
        _sparse_codex_marketplace(marketplace)
    return run(
        source,
        ["plugin", "marketplace", refresh_verb(source), marketplace],
        timeout=claude_cli.REFRESH_TIMEOUT_S,
    )


#: `git sparse-checkout`, which Codex runs for a marketplace with
#: `sparse_paths`, first shipped in git 2.25.0: an older git (RHEL/CentOS 7's
#: 1.8.3, Ubuntu 18.04's 2.17) fails every sparse clone, where the full one works.
SPARSE_GIT = (2, 25)


def _git_can_sparse() -> bool:
    """Whether the `git` Codex will run (the first on PATH) has `sparse-checkout`."""
    git = shutil.which("git")
    if not git:
        return False
    try:
        out = claude_cli.capture([git, "--version"], timeout=10).stdout or ""
    except (OSError, subprocess.SubprocessError):
        return False
    found = re.search(r"(\d+)\.(\d+)", out)
    return found is not None and (int(found[1]), int(found[2])) >= SPARSE_GIT


def _codex_sparse_args(name: str | None) -> list[str]:
    """`--sparse` arguments for Codex's `marketplace add`. Codex refuses an add
    whose paths differ from the entry's as "already added from a different
    source", so an existing entry gets its own paths (after moving one added
    before `--sparse` onto ours); a new one ours, unless git is too old."""
    from probe.shared.harness.harnesses.codex import config as codex_config  # noqa: PLC0415

    sparse = _git_can_sparse()
    configured = None
    if name is not None:
        if sparse:
            _sparse_codex_marketplace(name)
        configured = codex_config.marketplace_sparse_paths(name)
    if configured is None:
        configured = list(codex_config.MARKETPLACE_SPARSE_PATHS) if sparse else []
    return [arg for each in configured for arg in ("--sparse", each)]


def _sparse_codex_marketplace(name: str) -> None:
    """Move an install added before `add --sparse` onto the sparse clone, so
    its next `upgrade` is not a full clone racing Codex's 30 s git timeout
    (`codex_config.MARKETPLACE_SPARSE_PATHS`). Best-effort: a config this cannot
    edit keeps the full clone, as before."""
    from probe.shared.harness.harnesses.codex import config as codex_config  # noqa: PLC0415
    from probe.cli.wizard.state.state import MARKETPLACE_REPO  # noqa: PLC0415 - imports this module

    try:
        codex_config.write_marketplace_sparse_paths(name, MARKETPLACE_REPO)
    except (codex_config.ConfigError, OSError):
        pass


def install(source: str, plugin_id: str) -> claude_cli.Result:
    plugin_list = _get_plugin_list(source)
    if plugin_list is not None:
        return plugin_list.install_plugin(plugin_id.split("@", 1)[0])
    return run(
        source,
        ["plugin", install_verb(source), plugin_id],
        timeout=claude_cli.INSTALL_TIMEOUT_S,
    )


def uninstall(source: str, plugin_id: str) -> claude_cli.Result:
    plugin_list = _get_plugin_list(source)
    if plugin_list is not None:
        return plugin_list.uninstall_plugin(plugin_id.split("@", 1)[0])
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
