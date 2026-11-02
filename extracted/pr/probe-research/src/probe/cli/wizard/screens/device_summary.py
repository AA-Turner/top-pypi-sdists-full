"""the one-glance device summary above the menu: one row per agent (logo, MCP, capture) and the Versions verdict."""

from __future__ import annotations
from collections.abc import Iterable
from probe.cli.wizard.state.state import (
    Capabilities,
    McpState)
from probe.cli.wizard.terminal.terminal import CONTENT_WIDTH
from probe.shared.updates.updates import VersionStatus
from probe.shared.updates.updates import overall as overall_version_status


#: Components the wizard names in its version rows, and what to call them in a
#: 45-column value. `sdk` is deliberately absent: it ships inside the CLI
#: distribution, so it is the same number by construction and would spend a third
#: of the line restating the one above it. `probe doctor` still lists all four.
_VERSION_LABELS = {"cli": "CLI", "plugin": "plugin", "tap": "tap"}

#: The label column of the device summary: its longest label, "Last update
#: attempt", plus a space. Agents carry an icon rather than a name since
#: 2026-10-05, so nothing longer has to fit.
_STATE_LABEL_WIDTH = 20

#: What is left of a CONTENT_WIDTH row after "  " + the label + a space.
_STATE_VALUE_WIDTH = CONTENT_WIDTH - 3 - _STATE_LABEL_WIDTH

#: Each agent's MCP answer in a few words. `Capabilities.mcp_status` is the
#: sentence `probe doctor` prints; at up to 53 characters it wrapped every agent
#: row here onto a second line that read as a row of its own.
_MCP_WORDS = {
    McpState.ON: "on",
    McpState.LOGIN_NEEDED: "login needed",
    McpState.DAEMON: "off (daemon reads)",
    McpState.NOT_INSTALLED: "not installed",
    McpState.NOT_OFFERED: "not offered",
    McpState.UNKNOWN: "unknown",
}

#: A manifest older than this grades the verdict against a list that may predate
#: several releases, so "up to date" stops being a claim worth making plainly.
#: Same threshold `probe doctor` warns at, for the same reason.
_MANIFEST_STALE_S = 86400


def _state_row(label: str, value: str, style: str = "") -> str:
    """One aligned row of the device summary, optionally carrying a TUI style.

    Clipped, never wrapped: a wrapped value loses its alignment and reads as a
    new row with a blank label (see `_fit`)."""
    from probe.cli.wizard import terminal as tui

    return tui.StyledLine(f"  {label:<{_STATE_LABEL_WIDTH}} {value}", style=style, clip=True)


def _capture_word(snapshot: Capabilities) -> str:
    """The menu's capture state. A sign-in's pending lock says what lifts it:
    it read "killswitch set", the words for a deliberate off, and a person who
    picked Update instead of Install was never told why nothing recorded."""
    if snapshot.capture_awaiting_confirmation:
        return "off (finish Install)"
    if snapshot.capture_killswitched:
        return "off (killswitch set)"
    return "on" if snapshot.capture_on else "off"


def _agent_rows(caps_by_source: dict[str, Capabilities], images=None) -> list[str]:
    """One row per agent: its logo (or its name), then MCP and capture in
    aligned columns.

    `images` is the terminal's `tui.ImageProtocol`. With one, each agent is its
    logo, two cells wide, and pointing at the row shows its name; without one
    (Terminal.app, tmux, a pipe) the name stands in the logo's column. One
    agent without a logo gets names for every row, so the columns still line up.
    """
    from probe.cli.wizard import terminal as tui

    names = {source: agent_label(source) for source in caps_by_source}
    logos = {source: agent_logo(source) for source in caps_by_source} if images else {}
    drawn = bool(logos) and all(logos.values())
    lead = 2 if drawn else max(map(len, names.values()), default=0)
    mcp = {
        source: f"MCP {_MCP_WORDS.get(snapshot.mcp_state, snapshot.mcp_state)}"
        for source, snapshot in caps_by_source.items()
    }
    mcp_width = max(map(len, mcp.values()), default=0)
    rows: list[str] = []
    for index, (source, snapshot) in enumerate(caps_by_source.items()):
        capture = _capture_word(snapshot)
        label = "" if drawn else names[source]
        text = f"  {label:<{lead}}  {mcp[source]:<{mcp_width}}   capture {capture}"
        if drawn:
            # Drawn over the two blank cells before column 4, once that column is.
            logo = tui.image_escape(logos[source], images, cells=2, image_id=tui.IMAGE_ID_BASE + index)
            rows.append(tui.StyledLine(text, clip=True, escapes=((4, logo),), hover=names[source]))
        else:
            rows.append(tui.StyledLine(text, clip=True))
    return rows


def _fit(parts: list[str], limit: int = _STATE_VALUE_WIDTH) -> str:
    """Join what fits on ONE row, marking the rest rather than wrapping.

    A wrapped value in this block loses its alignment and reads as a new row with
    a blank label, which in a summary of what is installed is worse than saying
    less. The dropped tail is never the headline: callers order these worst-first,
    and the room for the ellipsis is only reserved once something is actually
    being dropped -- charging for it up front is what made a list that fits
    exactly render as a truncated one.
    """
    whole = " · ".join(parts)
    if len(whole) <= limit:
        return whole
    kept: list[str] = []
    for part in parts:
        if kept and len(" · ".join([*kept, part])) + 2 > limit:
            break
        kept.append(part)
    return (" · ".join(kept) + " …") if kept else ""


#: mark, wording and style per verdict. Amber (`class:instruction`) for anything
#: needing a decision and green (`class:selected`) only for the one row that
#: needs none -- the same pairing the import rows in this menu already use.
_VERDICT_COPY = {
    VersionStatus.CURRENT: ("✔", "Up to date", "class:selected"),
    VersionStatus.UPDATE: ("·", "Update available", "class:instruction"),
    VersionStatus.NEEDED: ("!", "Update needed — features may misbehave", "class:instruction"),
    VersionStatus.REQUIRED: ("✗", "Update required — no longer supported", "class:instruction"),
    VersionStatus.UNKNOWN: ("·", "Not checked", "class:instruction"),
}


def describe_versions(caps: Capabilities) -> list[str]:
    """"Am I current?" — the verdict, then the numbers behind it.

    The rows around this one say what is switched ON. None of them say whether
    what is switched on is the version we publish, and until now the only surface
    that did was `probe doctor` -- a command you have to already suspect
    something to run. The comparison is the same one (`probe.shared.updates.updates`), so
    the two can disagree only by being differently WORDED, never differently
    graded.

    An unreadable or absent manifest gets its own wording rather than falling
    through to the good-news branch. That is the invariant versions.py is built
    around: "nothing was wrong" and "nothing was checked" must not render alike.
    """
    rows, verdict = version_verdict(caps)
    mark, text, style = _VERDICT_COPY[verdict]

    age = caps.version_manifest_age_s
    stale = age is not None and age > _MANIFEST_STALE_S
    if stale and verdict is VersionStatus.CURRENT:
        # The one verdict an old manifest can silently falsify: everything else
        # here only gets MORE true as the published list moves on. Said on the
        # verdict line, not tucked below it, and not in green.
        text = f"{text} · checked {_describe_age(age)}"
        style = "class:instruction"

    lines = [_state_row("Versions", f"{mark} {text}", style)]
    detail = _version_detail(rows, verdict)
    if detail:
        lines.append(_state_row("", detail))
    return lines


def version_verdict(caps: Capabilities) -> tuple[list, VersionStatus]:
    """The components the Versions row grades (CLI, plugin, tap) and its
    verdict on them -- `describe_versions` and `probe status` alike."""
    rows = [row for row in caps.version_rows if getattr(row, "kind", "") in _VERSION_LABELS]
    return rows, overall_version_status(rows) if rows else VersionStatus.UNKNOWN


def _join_names(names: list[str]) -> str:
    """`a`, `a and b`, `a, b and c` -- a list a person reads, not a CSV."""
    if len(names) <= 1:
        return "".join(names)
    return f"{', '.join(names[:-1])} and {names[-1]}"


def _describe_age(seconds: float) -> str:
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def _version_detail(rows: list, verdict: VersionStatus) -> str:
    """The numbers under the verdict: what to update, or what you are running."""
    if verdict is VersionStatus.UNKNOWN:
        if not rows:
            return "no published version list cached yet"
        return "installed versions could not be read"
    behind = [row for row in rows if row.behind]
    if behind:
        moves = [
            f"{_VERSION_LABELS[row.kind]} {row.installed} → {row.latest}"
            for row in behind
            if row.installed and row.latest
        ]
        # Comma-separated, where the rest of the block uses "·": each move
        # already carries a spaced arrow, and a middle dot between two of those
        # reads as a third one. The two columns it saves are also what let a PAIR
        # of moves fit -- "CLI 0.161.0 → 0.162.0, plugin 0.80.0 → 0.81.0" is
        # exactly the width of the row.
        if len(", ".join(moves)) <= _STATE_VALUE_WIDTH:
            return ", ".join(moves)
        # Every version number, or none of them. A truncated list of moves reads
        # as "the CLI is behind" while silently dropping the components that are
        # behind as well, so past the row's width it degrades to naming them all
        # -- complete, and still one line. `probe doctor` prints the numbers.
        names = [_VERSION_LABELS[row.kind] for row in behind]
        return _fit([f"{_join_names(names)} behind"])
    return _fit([f"{_VERSION_LABELS[row.kind]} {row.installed}" for row in rows if row.installed])


def describe_state(
    caps: Capabilities | dict[str, Capabilities],
    installed: Iterable[str] | None = None,
    images=None,
) -> list[str]:
    """A one-glance summary printed above the menu on a re-run.

    The wizard already knows all of this, so showing it means the user picks an
    action against real state rather than guessing which one they need.

    `installed` limits the agent rows to the agents found on this machine
    (`detectable_sources`); None shows every agent in `caps`. The device rows
    still come off the first snapshot either way. `images` draws each agent as
    its logo (`_agent_rows`).
    """
    if isinstance(caps, dict):
        found = None if installed is None else set(installed)
        agents = {source: snapshot for source, snapshot in caps.items() if found is None or source in found}
        lines: list[str] = _agent_rows(agents, images) if agents else [
            _state_row("Coding agents", "none found on this device")
        ]
        first = next(iter(caps.values()), None)
        if first is not None:
            lines.append("")
            # Directly under the agents, above the update settings: what you are
            # running, then whether it keeps itself current, then when it last
            # tried. The version rows are device-wide -- one CLI, one plugin
            # ledger -- so they come off the first snapshot like the rows below.
            lines.extend(describe_versions(first))
            lines.append(_state_row("Automatic updates", "on" if first.auto_update_enabled else "off"))
            # ALWAYS, signed in or not. Printed only when an email resolved,
            # "not signed in" was the one state this summary could not show --
            # so the machine that most needs the account row was the machine
            # that never got one.
            lines.append(_state_row("Account", first.logged_in_as or "not signed in"))
            if first.last_update_attempt_summary:
                lines.append(_state_row("Last update attempt", first.last_update_attempt_summary))
        return lines

    lines = [
        _state_row(
            "CLI + MCP",
            caps.mcp_status() + (f"  ({caps.logged_in_as})" if caps.logged_in_as else ""),
        )
    ]
    lines.append(_state_row("Session capture", _capture_word(caps)))
    lines.extend(describe_versions(caps))
    lines.append(_state_row("Automatic updates", "on" if caps.auto_update_enabled else "off"))
    if caps.last_update_attempt_summary:
        lines.append(_state_row("Last update attempt", caps.last_update_attempt_summary))
    return lines
from probe.cli.wizard.agents import agent_label, agent_logo  # noqa: E402 -- pieces need each other; the front door loads this one first
