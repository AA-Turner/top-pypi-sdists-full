"""write the agent's own files: the global instruction pointer, the status-line segment (StatusLineSlot), the team-note seed, auto-update."""

from __future__ import annotations

from probe.cli.wizard.apply import agent_rules
from probe.shared.updates import autoupdate
from probe.cli.wizard.state.agent_identity import (
    agent_source,
    agent_target)


def _instruction_file_lock(path):
    """The lock the team-note sync holds while it reads and writes `path`.

    The wizard's own writes take it too: otherwise a sync that read the pointer
    as present could write the note back the moment after an opt-out removed
    both, and report nothing.
    """
    from probe.shared.notes.team_note.render import instruction_lock_path
    from probe.foundation.durable.durable import file_lock

    return file_lock(instruction_lock_path(path))


def apply_auto_update(want: bool) -> list[str]:
    try:
        autoupdate.save(enabled=want)
    except OSError as exc:
        # Said, never swallowed: the Probe service may read the other answer.
        return [f"! {exc}: automatic updates may still be {'on' if not want else 'off'} (check the folder's permissions)"]
    if not want:
        return ["Auto-update off. You'll still get a nudge when a release lands."]
    return ["Auto-update on."]


def statusline_installed() -> bool:
    """Whether the tracking segment is already in the agent's status line."""
    try:
        from probe.shared.harness.harnesses.claude_code import statusline

        return bool(statusline.status().get("installed"))
    except Exception:  # noqa: BLE001 - a probe that fails must not block the wizard
        return False


def apply_statusline() -> list[str]:
    """Register the tracking segment in the agent's status line.

    THE REASON THIS IS A WIZARD STEP AND NOT A README LINE. `statusLine` is a
    single key in the researcher's own settings, so nothing in a release can put
    the segment there -- it has to be written on their machine, once. Left to a
    documented `probe statusline install`, it is a feature almost nobody ends up
    with, and the ones who do are the people who read the changelog.

    Chains rather than claims: whatever was already configured keeps rendering,
    and `probe statusline uninstall` restores it exactly. Failure is reported and
    never fatal -- a status line is not worth failing an install over.
    """
    from probe.shared.harness.harnesses.claude_code import statusline

    source = agent_source()
    root = statusline.discover_plugin_root(source)
    if root is None:
        return [
            "Status line: skipped — the plugin is not on disk yet.",
            "  Run the wizard's Install again once it is.",
        ]
    try:
        # The slot the registry names: Claude Code's settings.json or Kimi
        # Code's footer settings (a running Kimi shows it from its next start).
        result = statusline.install_for(source, root)
    except (OSError, ValueError) as exc:
        return [f"Status line: not configured ({exc}). Nothing else was affected."]
    if result.get("chained_after"):
        return ["Status line: on, chained after the command you already had."]
    return ["Status line: on."]


def statusline_catch_up_due(source: str | None) -> bool:
    """The one-time footer catch-up would do something now: owed, not already
    there, and the plugin it renders from is on disk."""
    from probe.shared.harness.harnesses.claude_code import statusline

    if not source or not statusline.catch_up_owed(source):
        return False
    if statusline.installed_for(source):
        return False
    return statusline.discover_plugin_root(source) is not None


def catch_up_statusline(source: str | None = None) -> list[str]:
    """Kimi Code's footer for a machine whose rules predate it: the footer is
    written by the rules step (`apply_agent_rules`), which a machine with current
    rules never runs again, so upgrading to 0.214.0 left every existing Kimi
    machine without it. Once per agent (`statusline.mark_caught_up`): whatever
    happens here, a later uninstall is never undone. Not once the plugin is
    missing from disk (a later run tries again)."""
    from probe.shared.harness.harnesses.claude_code import statusline
    from probe.cli.wizard.state.agent_identity import agent_target

    selected = source or agent_source()
    if not statusline.catch_up_owed(selected):
        return []
    if statusline.installed_for(selected):
        statusline.mark_caught_up(selected)
        return []
    if statusline.discover_plugin_root(selected) is None:
        return []
    with agent_target(selected):
        lines = apply_statusline()
    statusline.mark_caught_up(selected)
    return [f"{agent_label(selected)} {line[0].lower()}{line[1:]}" if i == 0 else line
            for i, line in enumerate(lines)]


def remove_statusline() -> list[str]:
    """Take the tracking segment out of Claude Code's status line, restoring
    exactly what it wrapped: Uninstall's half of `apply_statusline` (R3). Left
    behind, the status line keeps running a renderer nobody maintains."""
    from probe.shared.harness.harnesses.claude_code import statusline

    source = agent_source()
    try:
        result = statusline.uninstall_for(source)
    except (OSError, ValueError) as exc:
        return [f"! left the status line in place ({exc}); remove Probe's status-line command from "
                f"{statusline.slot_path(source)} by hand."]
    if not result.get("removed"):
        return []
    if result.get("restored"):
        return ["Status line: back to the command you had before."]
    return ["Status line: removed."]


def seed_team_note_block() -> list[str]:
    """Render the team note into the instruction files at INSTALL time.

    A fresh machine otherwise waits a whole session for its first note. The
    harness reads CLAUDE.md / AGENTS.md before any hook of ours runs, so a block
    written by the first session's sync only reaches the SECOND session. The
    wizard runs before any session at all, which is the one moment that gap can
    be closed -- and closing it is what let the session-start hook stop carrying
    the note as a fallback.

    FAIL-OPEN IN EVERY DIRECTION: no credential, no network, a backend that has
    never heard of this team. Each of those means the block arrives on the next
    sync instead, which is exactly what happened before this existed. A wizard
    that cannot reach the API must still install everything else.
    """
    try:
        from probe.shared.notes import team_note as team_note_file
        from probe.sdk.client.client import Client
        from probe.sdk.settings.settings import resolve
        from probe.foundation.request_identity.surface import Surface

        settings = resolve()
        if not getattr(settings, "token", None):
            return []
        if team_note_file.hidden_by_limit(settings):
            # Team-wide items are hidden by this computer's workspace limit.
            team_note_file.remove_blocks()
            return []
        where = team_note_file.paths_for(settings)
        with Client(
            settings=settings, async_writes=False, surface=Surface.CLI.value
        ) as client:
            _, text = team_note_file.reconcile(client, where)
        report = team_note_file.render_blocks(text, settings=settings)
    except Exception:  # noqa: BLE001 - offline is a later sync, not a failed install
        return []
    if report.failures:
        return [f"! Team note: {report.failures[0]}"]
    if report.written or report.pointer_only:
        return ["Team note written into your instruction file."]
    return []


def apply_agent_rules(want: bool, *, stale: bool = False) -> list[str]:
    """Write or drop the selected agent's global instruction pointer.

    `stale` re-writes an already-installed block whose version moved, which is
    the only way a wording fix reaches a machine that ticked this once and never
    re-ran the wizard.
    """
    path = agent_rules.memory_path()
    # The status line rides along with the rules rather than asking its own
    # question. They are one concern -- make this machine's agent aware that
    # tracking exists -- and a separate checkbox for a one-line segment is a
    # worse trade than doing it and saying so. Additive and reversible
    # (`probe statusline uninstall` restores whatever was there), and it can ONLY
    # happen on the machine: `statusLine` is a key in the researcher's own
    # settings, so no release can put the segment there.
    # Only for a harness that has Probe's status line (Claude Code): on a pi or
    # Codex run this used to write Claude Code's settings.json.
    extra = apply_statusline() if want and _current_harness().statusline else []
    try:
        with _instruction_file_lock(path):
            if want:
                # The block of this agent's profile: a re-run must not swap the
                # daemon profile's blurb for the agent profile's section.
                changed = agent_rules.install(path, block=agent_rules.render_block(profile=agent_profile()))
            else:
                changed = agent_rules.remove_all(path)
    except agent_rules.DamagedBlock as exc:
        return [
            f"! Left {path} alone: {exc}.",
            "  Delete the stray probe-research marker by hand, then re-run this.",
        ]
    except (OSError, UnicodeDecodeError) as exc:
        # UnicodeDecodeError is a ValueError, so the OSError guard never caught
        # it: one latin-1 character in a researcher's own CLAUDE.md took the
        # whole wizard down with a traceback, mid-install. "Nothing else was
        # affected" is only true because the write is atomic.
        return [f"Could not update {path}: {exc}. Nothing else was affected."]

    # Seeded HERE, not on the first session, because the harness reads the
    # instruction file before any hook of ours runs -- a block written by the
    # first session's sync only reaches the second one. AFTER the pointer: the
    # note renders only into a file that carries it (`render_blocks`).
    if want:
        extra = extra + seed_team_note_block()

    if not want:
        return [f"Removed the Probe block from your global {path.name}."] if changed else []
    if stale and changed:
        return [f"Refreshed the Probe block in {short_path(path)}."] + extra
    if changed:
        # One line, because it is one bullet in a summary. The reassurance this
        # used to carry -- that the rest of the file is untouched -- is a
        # property of the writer, not news to report on every install.
        return [f"Probe tracking rule added to {short_path(path)}."] + extra
    return extra
from probe.cli.wizard.agents import agent_label, short_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.apply import _current_harness, agent_profile  # noqa: E402 -- pieces need each other; the front door loads this one first
