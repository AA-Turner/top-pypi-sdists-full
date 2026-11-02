"""the Review & install step: every capability this run changes, scoped to the chosen agents, then Install."""

from __future__ import annotations

# Read at import: MENU_COPY and AUTO_UPDATE_COPY below are built when this module loads.
from probe.cli.wizard.agents import MARKETPLACE_AGENT_SOURCES, agent_label, instruction_files
from probe.cli.wizard.state.state import Capability


#: The shared footer supplies the arrow. This label names the install action
#: and gives the forward button the same width as Back and the earlier Next.
INSTALL_TITLE = "Install"


def confirm_rows(
    agent_sources: tuple[str, ...] | list[str] | str,
    *,
    plugins_available: bool = True,
    unavailable: tuple[str, ...] = (),
    spaced: bool = True,
) -> list[str]:
    """The disclosure block of the confirm screen: every capability this
    install turns on, one bullet each, capture's data grant included.

    THIS BLOCK IS THE CONSENT SURFACE the capability picker used to be. The
    rows are built from the same `menu_copy` the picker used, so the capture
    bullet still says what it sends and where — and the render test asserts it
    fits, whole, on a real 80x24 screen before the confirming keystroke.

    `plugins_available=False` is the GPU-pod shape: neither `claude` nor
    `codex` is on PATH, so promising plugin rows would promise work this run
    cannot do. The degraded block names what still happens (the CLI and the
    sign-in) and is honest about the future: nothing is queued — the way the
    plugins arrive later is re-running the wizard and picking Install.

    `plugins_available` is computed upstream from `MARKETPLACE_AGENT_SOURCES`
    only (see `main.py`'s `plugin_promising_sources`), so it can be False
    while `agent_sources` still names pi -- a run selecting Claude Code and pi
    on a machine with no `claude` on PATH. pi's install never depended on
    that binary (see `pi_config`), and `apply_tracking`'s force-on reaches pi
    regardless of this flag, so the degraded early-return below must not say
    "nothing is queued" about it -- see the `"pi" in normalized` branch.
    """
    from probe.cli.wizard import terminal as tui

    normalized = (agent_sources,) if isinstance(agent_sources, str) else tuple(agent_sources)
    indent = "  "
    detail_indent = "      "
    # The room a bullet's detail actually has: the framed block is CONTENT_WIDTH
    # wide and centred, so what bounds a line is the block, or the terminal when
    # the terminal is the narrower of the two -- not `columns() - 8`, which was
    # a guess that happened to be right at 84 columns and threw four columns
    # away at 80. Four columns is a wrapped line, and a wrapped line on this
    # screen is a row of the capture disclosure pushed under the fold.
    room = max(20, min(tui.CONTENT_WIDTH, tui.columns()) - len(detail_indent))
    lines: list[str] = []

    def bullet(title: str, details: tuple[str, ...]) -> None:
        if lines and spaced:
            lines.append("")
        lines.append(f"{indent}• {title}")
        for detail in details:
            lines.extend(f"{detail_indent}{wrapped}" for wrapped in tui.wrap(detail, room))

    if not plugins_available:
        bullet(
            "Probe CLI + sign-in",
            ("Approve this device in your browser.",),
        )
        if "pi" in normalized:
            # pi never depended on the `claude`/`codex` binary this screen is
            # degraded over -- its install is one settings.json `packages`
            # entry, not a marketplace plugin (see pi_config's module
            # docstring), and tracking's force-on reaches it the same as any
            # other run. Saying "skipped" about pi here, the way the bullet
            # below correctly does for the missing marketplace agent, would
            # be describing marketplace-plugin work pi's install does not do.
            bullet(
                "pi extension, skills and MCP",
                ("One entry in pi's settings.json.",),
            )
        marketplace_sources = tuple(source for source in normalized if source in MARKETPLACE_AGENT_SOURCES)
        if marketplace_sources:
            bullet(
                "Coding-agent plugins — skipped",
                ("No Claude Code or Codex found. Install one, then run probe wizard › Install Probe.",),
            )
        return lines

    # Capture LAST, deliberately: on a terminal shorter than the block,
    # prompt_toolkit keeps the cursor's end visible and cuts the TOP — so the
    # bullet nearest the question survives folding longest, and the one that
    # must is the data grant.
    copy = menu_copy(agent_sources)
    for capability in (Capability.TRACKING, Capability.AGENT_RULES):
        title, details = copy[capability]
        bullet(title, details)
    _, auto_update_detail = auto_update_copy(agent_sources)
    bullet("Automatic updates", (auto_update_detail,))
    title, details = copy[Capability.CAPTURE]
    bullet(title, details)
    # A PARTIAL miss: some selected agent's CLI is not on this machine, so its
    # plugin half cannot happen this run. Said here, on the screen making the
    # promises, rather than discovered as a skipped step after the keystroke.
    for source in unavailable:
        bullet(
            f"{agent_label(source)} plugins — skipped",
            (f"{agent_label(source)} is not on this machine. Install it, then run probe wizard › Install Probe.",),
        )
    return lines


def run_confirm_install(
    agent_sources: tuple[str, ...] | list[str] | str,
    *,
    step: int | None = None,
    plugins_available: bool = True,
    unavailable: tuple[str, ...] = (),
    defaults: "DefaultsPick | None" = None,
):
    """The confirm screen: features followed by the shared Back / Install band.

    Returns True (install), tui.BACK, or None (Ctrl-C).

    The capability rows are STATIC — they live in the framed message, like the
    state block above the action menu, because they are not choices: the
    install is complete by design (see the module docstring). Install is the
    forward end of the same navigation band used by the earlier step; Back and
    Escape return to the previous choices.

    `step` is supplied when the agent screen was shown. Otherwise review is
    step 2 of 3: import choices, review and installation remain.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    agent_screen_shown = step is not None
    progress = install_header(STEP_CONFIRM, agent_screen_shown=agent_screen_shown)
    rows = confirm_rows(
        agent_sources, plugins_available=plugins_available, unavailable=unavailable
    )
    if defaults is not None:
        # The Defaults step's picks, which this keystroke applies. The daemon's
        # full consent was on that step; one line here says what it does.
        from probe.sdk import session_marker

        rows.extend([
            "",
            f"  {RECORDER_ROW_TITLE}: {defaults.recorder}  ·  "
            f"New sessions: {session_marker.state_label(setting_state(defaults.session_state))}",
        ])
        if defaults.recorder == session_marker.RECORDER_DAEMON:
            rows.extend(
                f"  {line}" for line in tui.wrap("The daemon records as you and sends session parts to an AI model.")
            )
    rows.append("")
    rows.extend(
        f"  {line}"
        for line in tui.wrap("Undo anytime: probe wizard › Uninstall Probe.")
    )
    rows.extend(["", "  One browser approval covers everything above."])
    message = tui.framed(
        "Features",
        rows,
        "Ready to install?",
    )

    choices = nav_footer(next_title=INSTALL_TITLE)
    instruction = "(enter selects · ← back · → install)"
    question = tui.select(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    # The forward end must return the install decision, never the nav sentinel.
    control = _wire_picker(question, single=True, on_leave=lambda _control: True)
    if control is None:
        # Without custom bindings, each option still returns the decision it
        # names through questionary's ordinary select.
        choices = [
            questionary.Choice(INSTALL_TITLE, value=True),
            questionary.Choice(BACK_TITLE, value=tui.BACK),
        ]
        instruction = "(enter selects · esc goes back)"
        question = tui.select(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
        tui.bind_step_keys(question, on_back=lambda event: event.app.exit(result=tui.BACK))
    else:
        tui.point_at(control, lambda value: value == NAV_BAND)
        dress_band(question, control)
    return tui.ask(
        question,
        height=tui.content_height(message, choices, instruction=instruction),
        margin=0,
        progress=progress,
    )


def menu_copy(
    sources: tuple[str, ...] | list[str] | str,
) -> dict[Capability, tuple[str, tuple[str, ...]]]:
    """Capability copy scoped to the agents this run will actually configure."""
    agents = agent_label(sources)
    rules = instruction_files(sources)
    return {
        Capability.TRACKING: (
            "CLI + MCP",
            ("Track runs and search your team's work.",),
        ),
        Capability.CAPTURE: (
            "Session capture",
            (f"Sends this device's {agents} sessions to your team.",),
        ),
        Capability.AGENT_RULES: (
            f"Rules in your global {rules}",
            (f"Prompts {agents} to search and track research in Probe.",),
        ),
    }


# Backwards-compatible default for non-interactive consumers that only need
# capability titles. Interactive callers always request copy for their targets.
MENU_COPY = menu_copy(("claude_code", "codex"))
# The picker is a picker. The full disclosure of what leaves the machine --
# prompts, assistant replies, shell commands, and the client-side redaction that
# is a filter rather than a guarantee -- lives on the BROWSER APPROVAL screen,
# which is where the grant is actually made and where research-os asserts the
# wording verbatim. Repeating three lines of it here made the shortest menu in
# the product the densest thing to read.


#: Copy for automatic updates. Once its own wizard step; now only the DETAIL
#: half has a production consumer (`confirm_rows`). The question half is kept
#: for the copy tests that measure it, nothing else.
def auto_update_copy(sources: tuple[str, ...] | list[str] | str) -> tuple[str, str]:
    return (
        "Keep it up to date automatically?",
        "Updates the CLI and plugins at session start.",
    )


AUTO_UPDATE_COPY = auto_update_copy(("claude_code", "codex"))
from probe.cli.wizard.screens.install_steps import STEP_CONFIRM, install_header  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.nav_band import BACK_TITLE, NAV_BAND, dress_band, nav_footer  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.picker_keys import _wire_picker  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.settings.defaults import DefaultsPick, RECORDER_ROW_TITLE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.settings.settings import setting_state  # noqa: E402 -- pieces need each other; the front door loads this one first
