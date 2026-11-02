"""Claude Code's plugin update: refresh and update through `claude plugin`, verified against its install ledger."""

from __future__ import annotations
import json
import shutil
from pathlib import Path
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import TAP_PLUGIN_ID


# -- plugin (installed) version, for the H1 post-condition ------------------
def _ledger_version(plugin_id: str) -> str | None:
    """The newest version Claude Code's install ledger records for `plugin_id`."""
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        data = json.loads(path.read_text())
        entries = (data.get("plugins") or {}).get(plugin_id) or []
        best: str | None = None
        for entry in entries:
            v = entry.get("version") if isinstance(entry, dict) else None
            if v and (best is None or is_newer(v, best)):
                best = v
        return best
    except Exception:
        return None


def installed_plugin_version() -> str | None:
    return _ledger_version(tracking_plugin_id())


def installed_tap_version() -> str | None:
    """The tap Claude Code has DOWNLOADED (its ledger), which is what an update
    moves. `versions.local_versions` prefers the copy that last RAN, which an
    update cannot move until a session restarts, so it grades this number
    whenever it is the newer of the two."""
    return _ledger_version(TAP_PLUGIN_ID)


def _ledger_readable() -> bool:
    """Claude Code's install ledger can be read: absent (nothing installed) or
    a JSON object. `_ledger_version` reads an unreadable one as "not
    installed", which `nothing_installed` must not take at its word."""
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return True
    except Exception:  # noqa: BLE001 - permissions, a half-written file, bad JSON
        return False
    return isinstance(data, dict) and isinstance(data.get("plugins") or {}, dict)


def _ledger_ids() -> list[str]:
    path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    try:
        plugins = json.loads(path.read_text()).get("plugins") or {}
    except Exception:
        return []
    return [key for key, entries in plugins.items() if isinstance(key, str) and entries]


def update_plugin(target_latest: str | None) -> PluginResult:
    """Update the Claude Code plugin via `claude`, then VERIFY it actually advanced (H1).

    The child is spawned with no TTY and captured output (H2) so a raw-mode TUI
    crash writes to a pipe, never the parent terminal. A zero exit is NOT trusted;
    we confirm by re-reading the installed plugin version.
    """
    claude = shutil.which("claude")
    if not claude:
        # The ledger is a file, readable without `claude`: what is installed
        # rides along, so a report can say "tap 0.9.3, and `claude` was not on
        # PATH" rather than just the second half.
        tap = installed_tap_version()
        return PluginResult(
            False, False, False, None, None, "`claude` not found on PATH (skipping plugin update)",
            tap_before=tap, tap_after=tap, missing_binary=True,
            legacy_ids=legacy_plugin_ids(),
        )

    before = installed_plugin_version()
    tap_before = installed_tap_version()
    readable_before = _ledger_readable()
    # Both go through claude_cli, which carries the DEVNULL this step always
    # needed -- no TTY -> no raw-mode on the parent terminal. The refresh goes
    # through plugin_cli so it gets the same REFRESH_TIMEOUT_S every other
    # refresh does; it had its own 90s here, which cut off a slow clone 30s
    # before Claude's own 120s bound would have.
    refresh = plugin_cli.refresh_marketplace(plugin_cli.CLAUDE, MARKETPLACE)
    failed_run = None if refresh.ok else refresh
    if failed_run is None:
        result = claude_cli.run(
            ["plugin", "update", tracking_plugin_id()], timeout=claude_cli.CAPTURE_TIMEOUT_S
        )
        failed_run = None if result.ok else result
    failure = _failed(failed_run) if failed_run is not None else ""
    completed = failed_run is None

    # The tap, best-effort and deliberately OUTSIDE `completed`: it is a
    # separate plugin that many users do not have, so `claude` failing here
    # means "not installed" far more often than "update broken". Letting that
    # flip `completed` would report the whole update as failed to everyone
    # without a tap. It is only the install step, so it is skipped when the
    # refresh failed: there is nothing new to install, and a dead network
    # would cost a second timeout for nothing. Its OUTCOME is not discarded:
    # the versions read on either side of it, and why it did not move, go back
    # on the result, and `perform_update` prints them and fails loudly on a tap
    # left behind the manifest (`tap_verdict`). Reading nothing back is how a
    # stale tap went unreported.
    #
    # A failed refresh is the tap's reason too. With the plugin already
    # current, the plugin's own line never mentions the refresh, and a bare
    # "skipped" left the reason, and a blocked git's fix, off the screen.
    tap_detail = failure
    if refresh.ok:
        tap_run = claude_cli.run(
            ["plugin", "update", TAP_PLUGIN_ID], timeout=claude_cli.CAPTURE_TIMEOUT_S
        )
        tap_detail = "" if tap_run.ok else _failed(tap_run)
    tap_after = installed_tap_version()
    if not tap_detail and not is_newer(tap_after, tap_before):
        # Exit 0 and nothing moved: the same reading the plugin's `completed`
        # branch gives its own version below.
        tap_detail = TAP_NOOP
    tap = {
        "tap_before": tap_before,
        "tap_after": tap_after,
        "tap_detail": tap_detail,
        # Only the refresh runs git, and its failure is on screen wherever the
        # manual commands would be: the plugin's line when that is unconfirmed,
        # the tap's when it is behind. Keyed on a later step, a plugin already
        # current could hide the commands with the fix nowhere in sight.
        "git_blocked": not refresh.ok and bool(git_blocker(refresh.detail)),
        "refresh_failed": not refresh.ok,
        "command_failed": not completed,
        "list_unreadable": not (readable_before and _ledger_readable()),
        "legacy_ids": legacy_plugin_ids(),
    }

    after = installed_plugin_version()
    changed = is_newer(after, before)
    # H1: trust the observed version, not claude's exit code. "Confirmed" = the plugin
    # is at (or past) the target, or it strictly advanced this run.
    at_target = bool(target_latest and after and not is_newer(target_latest, after))
    if at_target or changed:
        msg = f"plugin updated to {after}" if changed else f"plugin already at the latest ({after})"
        return PluginResult(True, True, changed, before, after, msg, **tap)
    if completed:
        return PluginResult(
            True,
            False,
            False,
            before,
            after,
            "`claude` returned success but the plugin version did not advance "
            "(it may have run inside a Claude Code session, which no-ops)",
            **tap,
        )
    return PluginResult(True, False, False, before, after, failure, **tap)


def manual_plugin_commands() -> str:
    return (
        f"claude plugin marketplace update {MARKETPLACE}\n"
        f"claude plugin update {tracking_plugin_id()}\n"
        f"claude plugin update {TAP_PLUGIN_ID}  # skip if you do not have the tap"
    )
from probe.shared.harness.plugin_update import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    MARKETPLACE,
    PluginResult,
    TAP_NOOP,
    _failed,
    git_blocker,
    is_newer,
    legacy_plugin_ids,
    tracking_plugin_id,
)
