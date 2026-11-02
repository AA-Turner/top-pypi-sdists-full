"""the Import existing work step: choose research work to import after install or from the menu."""

from __future__ import annotations
from probe.foundation.compat.compat import StrEnum


# -- choose and run imports after setup succeeds ----------------------------


class BackfillChoice(StrEnum):
    """One optional import selected during onboarding or from the main menu."""

    PAST_SESSIONS = "past_sessions"
    PROJECT_FOLDER = "project_folder"


#: Row copy for the offer, `MENU_COPY`-shaped. PAST_SESSIONS is a data grant
#: like capture, so its detail says what leaves the machine and at what pace.
BACKFILL_OFFER_COPY: dict[BackfillChoice, tuple[str, tuple[str, ...]]] = {
    BackfillChoice.PAST_SESSIONS: (
        "Import past coding sessions",
        (
            "Reads selected agents' transcripts; asks before anything uploads.",
        ),
    ),
    BackfillChoice.PROJECT_FOLDER: (
        "Import a folder of project work",
        ("An agent reads, uploads and describes it.",),
    ),
}

#: The offer's forward label. Continuing with nothing ticked is a real answer —
#: skipping is not a failure state, so the band never refuses.
OFFER_TITLE = "Continue  ›"


def run_backfill_offer(
    agent_sources: tuple[str, ...] | list[str] | str,
    *,
    defaults: set[BackfillChoice] | None = None,
    agent_screen_shown: bool = True,
    onboarding: bool = True,
    back_to_menu: bool = False,
):
    """Choose research work to import after installation or from the main menu.

    Checkbox rows over the same picker machinery as the settings screen.
    Both rows start selected unless explicit defaults are supplied. Returns
    None (Ctrl-C), tui.BACK, or a set of BackfillChoice. An empty set skips imports.
    """
    import questionary

    from probe.cli.wizard import terminal as tui
    from probe.cli.wizard.actions.onboarding import ACTION_COPY, Action

    tui.use_checkmarks()

    defaults = set(BackfillChoice) if defaults is None else defaults
    indent = tui.body_indent()
    rows: dict[BackfillChoice, questionary.Choice] = {}
    choices: list = []
    for choice, (title, detail) in BACKFILL_OFFER_COPY.items():
        choices.append(questionary.Separator(" "))
        row = questionary.Choice(
            title=_menu_row(title, detail, checked=choice in defaults, indent=indent),
            value=choice,
            checked=choice in defaults,
        )
        rows[choice] = row
        choices.append(row)
    choices.extend(nav_footer(forward=True, next_title=OFFER_TITLE,
                              back_title="‹  Main menu" if back_to_menu else BACK_TITLE))
    message = tui.framed(
        ACTION_COPY[Action.IMPORT_RESEARCH][0],
        [],
        "What should be imported?",
    )
    instruction = "(enter picks this row · ↑ to change)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    control = _bind_menu_keys(question, rows, copy=BACKFILL_OFFER_COPY, indent=indent)
    if control is None:
        choices = without_nav(choices)
        instruction = "(space to toggle, enter to continue)"
        question = tui.checkbox(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
    else:
        dress_band(question, control)

    if back_to_menu and hasattr(question, "_probe_content"):
        question._probe_content["instruction"] = (
            "↑↓ choose · space toggle · enter · esc main menu"
        )
    picked = tui.ask(
        question, height=tui.content_height(message, choices, instruction=instruction),
        progress=(install_header(STEP_IMPORTS, agent_screen_shown=agent_screen_shown)
                  if onboarding else []), margin=1,
    )
    if picked is None:
        return None
    if picked is tui.BACK:
        return tui.BACK
    return {choice for choice in picked if isinstance(choice, BackfillChoice)}
from probe.cli.wizard.screens.install_steps import STEP_IMPORTS, install_header  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.nav_band import BACK_TITLE, dress_band, nav_footer, without_nav  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.picker_keys import _bind_menu_keys, _menu_row  # noqa: E402 -- pieces need each other; the front door loads this one first
