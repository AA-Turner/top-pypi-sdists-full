"""the import step inside the wizard: select and run the reviewed import lanes, past sessions included."""

from __future__ import annotations
from collections.abc import Callable, Sequence


def _select_and_run_imports(
    *,
    caps,
    base_now,
    folder,
    selected_agents,
    telemetry,
    agent_screen_shown: bool = True,
    progress_header: Callable[[float], Sequence[str]] | None = None,
):
    """Keep Back navigation inside optional imports, after installation."""
    from probe.cli import wizard as setup
    from probe.cli.wizard import terminal as tui

    from probe import analytics as telemetry_mod

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    defaults = None
    while True:
        tui.clear()
        imports = setup.run_backfill_offer(
            selected_agents,
            defaults=defaults,
            agent_screen_shown=agent_screen_shown,
            onboarding=progress_header is not None,
            back_to_menu=True,
        )
        # The convergence point for both entry paths -- guided install and the
        # main-menu selector -- and the only place the answer exists as a
        # value. Emitted for EVERY answer including the empty set: skipping is
        # the most common thing to do here, and an event that only fired when a
        # box was ticked would leave the skip completely invisible.
        tel.emit(
            telemetry_mod.EVENT_WIZARD_IMPORTS_CHOSEN,
            choices=(
                sorted(str(choice) for choice in imports)
                if isinstance(imports, (set, frozenset))
                else []
            ),
            choice_count=len(imports) if isinstance(imports, (set, frozenset)) else 0,
            navigation=(
                "quit"
                if imports is None
                else "back"
                if imports is tui.BACK
                else "skip"
                if not imports
                else "continue"
            ),
            onboarding=progress_header is not None,
            offered_again=defaults is not None,
        )
        if imports is None:
            _exit_wizard()
        if imports is tui.BACK or not imports:
            return imports
        completed = set()
        navigation = _run_selected_imports(
            imports,
            caps=caps,
            base_now=base_now,
            folder=folder,
            selected_agents=selected_agents,
            telemetry=telemetry,
            progress_header=progress_header,
            completed=completed,
        )
        if navigation is not tui.BACK:
            return imports
        # Keep the unanswered choices. Lanes already started or explicitly
        # skipped must not run again just because a later page went Back.
        defaults = set(imports) - completed


def _run_selected_imports(
    imports,
    *,
    caps,
    base_now,
    folder,
    selected_agents,
    telemetry,
    progress_header: Callable[[float], Sequence[str]] | None = None,
    completed: set | None = None,
):
    """The same reviewed import lanes for setup and the main-menu selector."""
    from probe.cli.imports.jobs import ui as import_jobs_ui
    from probe.cli import wizard as setup
    from probe.cli.wizard import terminal as tui
    from probe.cli.wizard.actions.onboarding import Action

    notices: list[str] = []
    show_status = False
    completed = set() if completed is None else completed
    with tui.onboarding(lambda: progress_header(0.0) if progress_header else []):
        if setup.BackfillChoice.PAST_SESSIONS in imports:
            session_lines = _import_past_sessions(
                interactive=True,
                background=True,
                back_to_selection=True,
            )
            if session_lines is tui.BACK:
                return tui.BACK
            completed.add(setup.BackfillChoice.PAST_SESSIONS)
            show_status = session_lines is not None
            if session_lines:
                notices.extend([*session_lines, ""])
        if setup.BackfillChoice.PROJECT_FOLDER in imports:
            folder_lines = _run_wizard_action(
                Action.BACKFILL,
                caps=caps,
                base_now=base_now,
                yes=False,
                tracking=None,
                capture=None,
                auto_update=None,
                agent_rules=None,
                uninstall=False,
                configured=True,
                folder=folder,
                # The selector already asked about session history separately.
                transcripts=False,
                selected_agents=selected_agents,
                telemetry=telemetry,
                back_to_selection=True,
            )
            if folder_lines is tui.BACK:
                return tui.BACK
            completed.add(setup.BackfillChoice.PROJECT_FOLDER)
            show_status = show_status or folder_lines is not None
            if folder_lines:
                notices.extend([*folder_lines, ""])
    if progress_header is not None or not show_status:
        # Setup finishes with the dashboard handoff page, even if imports were
        # skipped. The main-menu import path still opens the live monitor.
        return
    with tui.onboarding(lambda: progress_header(1.0) if progress_header else []):
        navigation = import_jobs_ui.show_imports(
            onboarding=progress_header is not None,
            notices=notices,
        )
    if navigation is import_jobs_ui.Navigation.EXIT:
        _exit_wizard()


def _import_past_sessions(
    *,
    interactive: bool,
    background: bool = False,
    back_to_selection: bool = False,
):
    """Run the transcript import lane.

    Shared by onboarding, the main-menu import selector, and the legacy
    transcript-only command. Each uses the same census, review and receipts.

    It used to resolve a local coding agent to summarize with first. That is
    gone with the server-side digest lane: there is no agent to pick, no
    picker to back out of, and the lane always runs.
    """
    from probe.cli.imports import transcripts as transcripts_mod

    return transcripts_mod.run_lane(
        client=_backfill_client(),
        interactive=interactive,
        background=background,
        back_to_selection=back_to_selection,
    )
from probe.cli.connection import _backfill_client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.actions import _run_wizard_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.session import _exit_wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
