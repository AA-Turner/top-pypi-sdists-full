"""probe statusline install/uninstall/status/show: the tracked segment in the agent's status line (through StatusLineSlot)."""

from __future__ import annotations
import os
import sys
from pathlib import Path

import typer
from ....sdk.settings.settings import resolve
from ....sdk import agent_session, session_marker
from ....shared.harness.harnesses.claude_code import statusline


# -- expression views (read-time computed panels, research-os 0088) ---------
# The AUTHORING surface. The dashboard renders, renames and deletes views but
# never composes one: an expression comes from a researcher's agent session or
# their own script, so the door it comes through is here and the SDK's
# `probe.expr`. --spec-file is literally that path — a script writes JSON, this
# uploads it.
# -- statusline -------------------------------------------------------------
# The coding-agent status line is ONE global slot in the agent's settings, with
# no plugin manifest field for it, so getting our segment there means editing a
# file we do not own. That makes it an explicit, reversible command rather than
# something the wizard does silently -- see probe.shared.harness.harnesses.claude_code.statusline.
statusline_app = typer.Typer(
    no_args_is_help=True, help="the tracked/untracked segment in Claude Code's status line"
)


@statusline_app.command("install")
def statusline_install(
    plugin_root: str = typer.Option(
        None, "--plugin-root", help="the probe-research plugin directory (auto-detected)"
    ),
    agent: str = typer.Option(
        None, "--agent", help="whose status line: kimi_code or claude_code (default: the agent running this shell)"
    ),
) -> None:
    """Add the Probe segment to Claude Code's status line, keeping what is there.

    Chains after any existing command rather than replacing it, and feeds both
    sides the status-line payload -- see the module docstring for why a plain
    `a; b` chain silently starves the second command of stdin.
    """
    # Codex HAS a status line, but it is a PICKER over built-in items
    # (`/statusline` — "Select which items to display"; `tui.status_line` is a
    # sequence, and an unrecognised entry is ignored rather than executed). There
    # is no command hook, so no segment can render there — the same information
    # goes out as an on-change NOTICE instead. Turning that on is what `install`
    # means under Codex, so one command does the right thing per agent.
    #
    # Both surfaces, never a refusal: someone may perfectly well be configuring
    # Claude Code from a Codex shell, and picking one on ambient environment
    # would break that. So Codex ADDS the notice rather than replacing the
    # install, and the reply says plainly which surface got what.
    detected = agent_session.detect_agent()
    named = agent  # an agent named on the command line wins over the shell's
    under_codex = named is None and detected is not None and detected.label == "codex"
    notice = str(statusline.enable_notice()) if under_codex else None
    if under_codex:
        print(
            "note: Codex's status line selects from built-in items and cannot run a "
            "command, so this enabled the on-change notice there and configured the "
            "segment for Claude Code.",
            file=sys.stderr,
        )

    # Run from inside Kimi Code, the slot is Kimi's footer settings (the registry says
    # which slot each agent has).
    from probe.foundation.harness_registry import get_registry
    from probe.foundation.harness_registry import harness_registry as harness_registry

    row = get_registry().find(named) if named is not None else None
    if named is not None and (row is None or not row.statusline):
        print(f"{named!r} has no status line Probe can install into", file=sys.stderr)
        raise typer.Exit(2)
    target = row.id if row is not None else (detected.label if detected is not None else None)
    target_row = get_registry().find(target) if target is not None else None
    kimi_slot = target_row is not None and target_row.statusline == harness_registry.STATUSLINE_KIMI_TUI_TOML
    root = Path(plugin_root) if plugin_root else statusline.discover_plugin_root(
        target if kimi_slot else None
    )
    if root is None:
        print(
            "could not find the probe-research plugin — install it with "
            "`/plugin install probe-research@research-os-agent`, or pass --plugin-root",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    if kimi_slot:
        try:
            _print_json({**statusline.install_kimi(root), "notice": notice})
        except (OSError, ValueError) as exc:
            print(f"Kimi Code's status line was not changed: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
        return
    try:
        result = statusline.install(root)
    except (OSError, ValueError) as exc:
        print(f"Claude Code's status line was not changed: {exc}", file=sys.stderr)
        raise typer.Exit(1) from exc
    _print_json({**result, "notice": notice})


@statusline_app.command("uninstall")
def statusline_uninstall() -> None:
    """Remove the Probe segment and the on-change notice, restoring what was wrapped."""
    result = statusline.uninstall()
    if statusline.kimi_installed():
        result = {**result, "kimi": statusline.uninstall_kimi()}
    _print_json({**result, "notice_disabled": statusline.disable_notice()})


@statusline_app.command("status")
def statusline_status() -> None:
    """Whether the segment is installed, and what else shares the slot."""
    _print_json({**statusline.status(), "notice_enabled": statusline.notice_enabled()})


@statusline_app.command("show")
def statusline_show(
    session: str = typer.Option(
        None, "--session", help="session id (defaults to this shell's coding-agent session)"
    ),
) -> None:
    """Print the segment this session would render right now.

    The debugging door: it answers "why is it saying untracked" without making
    anyone re-render a status line, and it reads the same marker file the
    renderer does rather than a second code path that could disagree -- with the
    daemon's `<session>.scope` over its project, as the renderer reads it.
    """
    session_id = session or os.environ.get("CLAUDE_CODE_SESSION_ID") or ""
    if not session_id:
        print("no session id: pass --session, or run inside a coding agent", file=sys.stderr)
        raise typer.Exit(1)
    state = session_marker.read(session_id)
    settings = resolve()
    signal = session_marker.tracking_signal(session_id)
    if signal is not None:
        # The session signal is the live state. Do not walk folder defaults
        # after it exists: config changes apply only to new sessions.
        tracking = session_marker.is_tracking(signal)
    else:
        # This is a shell debugging command, not a host hook with a payload, so
        # the process cwd is the best and only cwd it owns.
        tracking, _source = session_marker.resolve_tracking_default(None)
    print(
        session_marker.render(
            state,
            configured=bool(settings.token or settings.mcp_token),
            tracking=tracking,
            live=tracking and session_marker.is_live(state),
        )
    )
    _print_json(
        {
            "session_id": session_id,
            "marker": str(session_marker.marker_path(session_id)),
            "state": state,
        }
    )
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
