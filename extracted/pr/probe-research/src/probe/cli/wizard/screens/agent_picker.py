"""the Coding agents step: choose every agent this wizard pass acts on, with per-action copy."""

from __future__ import annotations
from probe.cli.wizard.screens.install_steps import STEP_AGENTS, install_header, step_title


#: What every agent row on step 1 says under its title, per source -- NOT one
#: shared string: claude_code/codex go through a plugin marketplace AND pair
#: source-bound capture, but pi's install is a single settings.json `packages`
#: entry (extension + skills + MCP manifest), never a marketplace, so the old
#: one-size copy ("Install plugins and pair source-bound capture.") became
#: inaccurate for pi's row the moment pi could appear in this picker at all.
#: A table, not a ternary -- the same reason `AGENT_LABELS` is one: correct
#: only while there were exactly two sources, silently wrong for whichever
#: third one shows up. Module-level because the row is BUILT once and
#: REPAINTED on every toggle, and the two spellings drifted the moment they
#: were separate literals -- a divergence that only shows up mid-interaction,
#: after the first keystroke, which is the worst place to find it.
AGENT_ROW_DETAIL: dict[str, tuple[str, ...]] = {
    "claude_code": ("Plugins and session capture.",),
    "codex": ("Plugins and session capture.",),
    "pi": ("Extension, skills and MCP, via settings.json.",),
    "kimi_code": ("Plugins and session capture.",),
}


# -- the coding-agent picker, per action ------------------------------------
#
# The picker is NOT the install's step 1 alone. `wizard()` opens it for every
# action scoped to a coding agent, and states that gate as exclusions -- not in
# `IMPORT_ACTIONS`, not in `DEVICE_ACTIONS` -- so uninstall, update, diagnose
# and the manual instructions all land on it too, and any action added to
# neither set will land on it without an edit here.
#
# It was written as if only Install could reach it. Picking "Uninstall Probe"
# opened a screen headed `Install Probe — step 1 of 2` asking "Which coding
# agents should Probe connect?" over rows reading "Install plugins and pair
# source-bound capture." -- four lines describing the opposite of the next
# keypress, on the one path in the product that destroys something.
#
# Keyed by `Action`, which is a StrEnum, so the plain value works as a key and
# this table costs no import of `actions` at module scope (see that module's
# docstring for why it stays out of `probe log`'s path).


#: Title, lede, question -- the three slots of the framed block, per action.
#: Only Install is NUMBERED: `INSTALL_STEPS` counts the install's screens, and
#: no other action walks them. Uninstall's second screen is `confirm_removal`,
#: which carries no number either; update and diagnose have no second screen at
#: all, so "step 1 of 2" there was a position in a flow that does not exist.
#:
#: WIDTH BUDGET on the question: it shares its row with the picker's
#: instruction, so at 80 columns -- the floor every terminal clears -- a longer
#: one wraps, and the wrapped row eats the blank that separates the question
#: from the `-- Coding agents` heading. The install's question is the budget,
#: pinned by a test rather than by a number counted here.
AGENT_SCREEN_COPY: dict[str, tuple[str, str, str]] = {
    "configure": (
        step_title(STEP_AGENTS),
        "Probe sets up each one you pick.",
        "Which coding agents?",
    ),
    "uninstall": (
        "Uninstall Probe",
        "Removes Probe from each one you pick.",
        "Which coding agents?",
    ),
    "update": (
        "Update Probe",
        "Updates the CLI and each agent's plugins.",
        "Which coding agents?",
    ),
    "diagnose": (
        "Diagnose a problem",
        "Checks each agent you pick.",
        "Which coding agents?",
    ),
    "manual": (
        "Set up manually",
        "Prints the commands for each one you pick.",
        "Which coding agents?",
    ),
}

#: What an unlisted action gets. Deliberately says nothing about what happens
#: next: a new action inheriting GENERIC copy is a screen that is merely thin,
#: and one inheriting the INSTALL's copy is a screen that lies. The drift guard
#: in the tests is what turns thin into named; nothing here can do it, because
#: the whole failure mode is an action nobody remembered to come and describe.
GENERIC_AGENT_SCREEN_COPY: tuple[str, str, str] = (
    "Coding agents",
    "Runs on each one you pick.",
    "Which coding agents?",
)

#: `AGENT_ROW_DETAIL` is the INSTALL's row detail; every other action needs its
#: own, for the same per-source reason that table exists (pi has no
#: marketplace, so it can neither gain nor lose a plugin).
AGENT_ROW_DETAIL_BY_ACTION: dict[str, dict[str, tuple[str, ...]]] = {
    "configure": AGENT_ROW_DETAIL,
    "uninstall": {
        "claude_code": ("Remove plugins and stop capture.",),
        "codex": ("Remove plugins and stop capture.",),
        "kimi_code": ("Remove plugins and stop capture.",),
        "pi": ("Remove its settings.json entry.",),
    },
    "update": {
        "claude_code": ("Update the plugins.",),
        "codex": ("Update the plugins.",),
        "kimi_code": ("Update the plugins.",),
        # Not a hedge: `upgrading.py` skips pi outright and says so in its own
        # output. Promising an upgrade here that the apply then declines is the
        # same class of mismatch as the install copy this table replaces.
        "pi": ("Update it through pi.",),
    },
    "diagnose": {
        "claude_code": ("Check setup, sign-in and updates.",),
        "codex": ("Check setup, sign-in and updates.",),
        "kimi_code": ("Check setup, sign-in and updates.",),
        "pi": ("Check setup, sign-in and updates.",),
    },
    "manual": {
        "claude_code": ("Print the setup commands.",),
        "codex": ("Print the setup commands.",),
        "kimi_code": ("Print the setup commands.",),
        "pi": ("Print the setup commands.",),
    },
}

#: The row detail an unlisted action gets. Names the agent's role in what
#: follows without claiming what that is -- see `GENERIC_AGENT_SCREEN_COPY`.
GENERIC_AGENT_ROW_DETAIL: tuple[str, ...] = ("Include this coding agent.",)


def agent_screen_copy(action: str | None) -> tuple[str, str, str]:
    """Title, lede and question for the picker, for the action that opened it.

    `None` is the caller that did not say -- a direct call, or a seam in a test
    -- and it gets the install, because that is the flow the picker was built
    for and the only one that reaches it without going through `wizard()`.
    """
    if action is None:
        return AGENT_SCREEN_COPY["configure"]
    return AGENT_SCREEN_COPY.get(str(action), GENERIC_AGENT_SCREEN_COPY)


def agent_row_detail(action: str | None, source: str) -> tuple[str, ...]:
    """What one agent row says under its title, for this action and source."""
    if action is None:
        return AGENT_ROW_DETAIL[source]
    detail = AGENT_ROW_DETAIL_BY_ACTION.get(str(action), {})
    return detail.get(source, GENERIC_AGENT_ROW_DETAIL)


def run_agent_menu(defaults: tuple[str, ...], *, action: str | None = None):
    """Choose every coding agent this one wizard pass acts on.

    `action` is what OPENED the picker, and it is the whole reason this screen
    is not a constant: `wizard()` shows it for uninstall, update, diagnose and
    the manual instructions too (see `AGENT_SCREEN_COPY`), and it used to greet
    every one of them with the install's title, lede and row detail. Omitted
    means the install -- the flow this screen is step 1 of.
    """
    import questionary

    from probe.cli.wizard import terminal as tui
    from probe.cli.wizard.actions.onboarding import Action

    title, lede, question_text = agent_screen_copy(action)

    tui.use_checkmarks()  # the fallback path, if we cannot take the box over

    indent = tui.body_indent()
    rows = {
        source: questionary.Choice(
            title=_menu_row(
                AGENT_LABELS[source],
                agent_row_detail(action, source),
                checked=source in defaults,
                indent=indent,
            ),
            value=source,
            checked=source in defaults,
        )
        # `detectable_sources()`, not MARKETPLACE_AGENT_SOURCES: this step
        # auto-detects a coding-agent CLI, and pi IS one -- `shutil.which("pi")`
        # finds its binary exactly the way `plugin_cli.available` finds
        # `claude`/`codex` (see that function's docstring for the "pi has no
        # CLI" claim this replaces). Called fresh here rather than trusting
        # `defaults` to double as the row set: `defaults` is `agent_defaults`,
        # which a Codex session pins to `("codex",)` regardless of what else
        # this machine has -- using it for row VISIBILITY too would hide a
        # present Claude Code or pi row for a reason that has nothing to do
        # with whether they are actually here.
        for source in detectable_sources()
    }
    choices: list = []
    for index, row in enumerate(rows.values()):
        if index:
            # Same reason as every other menu here: without a blank row an
            # option's title sits directly under the previous option's
            # description, and two entries read as one paragraph.
            choices.append(questionary.Separator(" "))
        choices.append(row)
    choices.extend(nav_footer())
    progress = install_header(STEP_AGENTS) if action in (None, Action.CONFIGURE) else None
    message = tui.framed("Coding agents" if progress else title, tui.wrap(lede), question_text)
    instruction = "(enter picks this row · ↑ to change)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
        # KEPT, even though our own Enter binding never reaches it. questionary
        # only runs `validate` on ITS submit -- the path `_wire_picker` replaces
        # -- so on the happy path this is dead weight. It is the FALLBACK's
        # guard: when questionary's internals move and `checkbox_control()`
        # comes back None, `_wire_picker` installs no bindings at all and the
        # library's own enter-submits wins, `can_submit` never runs, and an
        # empty selection sails through. Downstream that is not a cosmetic
        # degradation: `wizard()` indexes `agent_sources[0]` and the whole
        # command dies with an IndexError.
        validate=lambda answer: bool(answer) or "Choose at least one coding agent.",
    )
    own_boxes = tui.draw_own_boxes(question)

    def redraw(control) -> None:
        """Repaint the boxes, and the Next row's reason for refusing.

        The empty selection is the only state this step can be in that it
        cannot leave, so it is the only one that has to explain itself. Saying
        it on the Next row -- the row you are pressing -- beats a validation
        error under a prompt that no longer exists, and beats the alternative
        this replaced, which was a key that silently did nothing.

        `own_boxes` is False only when `checkbox_control()` returned None, and
        `_wire_picker` bails on that same condition BEFORE it ever calls this --
        so this function only ever runs with the boxes ours to draw. The
        fallback is guarded by `validate=` above instead, which is the one
        thing questionary still runs when we cannot reach its control.
        """
        for source, row in rows.items():
            row.title = _menu_row(
                AGENT_LABELS[source],
                agent_row_detail(action, source),
                checked=source in control.selected_options,
                indent=indent,
            )
        chosen = [value for value in control.selected_options if value in rows]
        band = nav_row(choices)
        if band is not None:
            # The right half carries the refusal. It is the only place this step
            # can say why Enter on `Next ›` is doing nothing, and it sits under
            # the cursor's own column rather than in an error line below a
            # prompt. Set on the row's INGREDIENTS, not on its rendered title:
            # `_paint_boxes` rebuilds the band's text every frame and would
            # overwrite a title written here on the very next render.
            band.nav["forward"] = "→" if chosen else "choose at least one agent —"

    control = _wire_picker(
        question,
        redraw=redraw,
        can_submit=lambda control: any(value in rows for value in control.selected_options),
        on_leave=lambda control: [v for v in control.selected_options if v in rows],
    )
    if control is None:
        # Same call as step 2's: an unwirable band is a row that says Back and
        # does something else. `validate=` above is what guards this path.
        choices = without_nav(choices)
        instruction = "(space to toggle, enter to continue · esc goes back)"
        question = tui.checkbox(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
            validate=lambda answer: bool(answer) or "Choose at least one coding agent.",
        )
    elif not own_boxes:
        # questionary is drawing its own indicator in front of a title that
        # already carries one, so strip ours rather than ship `✔ ✔ Claude Code`.
        for source, row in rows.items():
            row.title = _menu_row(
                AGENT_LABELS[source],
                agent_row_detail(action, source),
                checked=False,
                indent=indent,
            ).split(" ", 1)[1]
    tui.point_at(control, lambda value: value == NAV_BAND)
    dress_band(question, control)

    picked = tui.ask(
        question,
        height=tui.content_height(message, choices, instruction=instruction),
        margin=1 if progress is not None else tui.MARGIN,
        progress=progress,
    )
    if picked is None or picked is tui.BACK:
        return picked
    # `rows`, not MARKETPLACE_AGENT_SOURCES: it is exactly the set this run
    # OFFERED (see the row-building loop above), in the same order, so a
    # checked pi box survives instead of being filtered back out by a tuple
    # that never knew pi could be a row at all.
    chosen = tuple(source for source in rows if source in picked)
    # NEVER an empty tuple. `wizard()` reads `agent_sources[0]` straight after
    # this, so "answered with nothing" has to be a non-answer here rather than
    # an IndexError three frames up. Unreachable while `validate=` holds; this
    # is the second lock on the same door, because the first one lives inside a
    # library we have already had to guard against six times.
    return chosen or tui.BACK
from probe.cli.wizard.agents import AGENT_LABELS, detectable_sources  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.nav_band import NAV_BAND, dress_band, nav_footer, nav_row, without_nav  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.picker_keys import _menu_row, _wire_picker  # noqa: E402 -- pieces need each other; the front door loads this one first
