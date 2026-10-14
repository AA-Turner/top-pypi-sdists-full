"""Finish terminal onboarding by handing off to the dashboard."""

from __future__ import annotations

import webbrowser
from collections.abc import Callable, Sequence

from probe.sdk.links import dashboard_base_url

from . import import_jobs, import_jobs_ui, import_progress, tui


def _needs_attention(jobs: list[dict]) -> bool:
    summaries = [import_progress.summarize(jobs, kind)
                 for kind in (import_jobs.Kind.TRANSCRIPTS, import_jobs.Kind.FOLDER)]
    return (any(job.get("readable") is False for job in jobs)
            or any("attention" in summary.state or summary.state == "Partially complete"
                   for summary in summaries))


def show(
    base_url: str,
    next_steps: Sequence[str] = (),
    open_apps: Sequence[tuple[str, Callable[[], bool]]] = (),
) -> bool | import_jobs_ui.Navigation:
    """Return true for dashboard, false for main menu, or Navigation.EXIT.

    Opening the dashboard and exiting the wizard both leave approved background
    imports running, with their saved progress available in Existing imports.

    `next_steps` are what the researcher still has to do by hand: the steps
    that put Probe inside a cloud agent (Capy), which no command can do. The
    install's progress page is replaced by the import offer before anyone can
    read it, so this last page is where they stay on screen. `open_apps` are
    (name, opener) pairs: an app this machine can open on that step's screen,
    offered as an action and opened only when chosen.
    """
    base = dashboard_base_url(base_url)
    url = f"{base}/projects" if base else None
    open_failed = False
    app_results: dict[str, bool] = {}

    def status():
        jobs = import_jobs.list_jobs()
        lines = ["Probe is installed."]
        if next_steps:
            lines.extend(["", *next_steps])
        for name, opened in app_results.items():
            lines.append(
                f"{name} is open on that screen: Continue, then the step above."
                if opened
                else f"Couldn't open {name}. Follow the step above in {name}."
            )
        progress = import_jobs_ui.active_progress_lines(jobs)
        if progress:
            if tui.rows() < 32:
                # Keep both bars above the fold on a standard 24-row terminal.
                lines = [*progress, "", *lines]
            else:
                lines.extend(["", tui.StyledLine("Import progress", style="class:question"),
                              "", *progress])
        if any(job.get("state") in {import_jobs.State.QUEUED, import_jobs.State.RUNNING}
               for job in jobs):
            lines.extend(["", "Imports keep running in the background."])
        if _needs_attention(jobs):
            lines.extend(["", "Some imports need attention. See Existing imports."])
        if url:
            lines.extend(["", url])
        else:
            lines.extend(["", "Open your Probe dashboard in your browser."])
        if open_failed:
            lines.extend(["", "Couldn't open your browser. Use the link above."])
        return lines

    while True:
        choices = [(f"Open {name} >", ("app", index)) for index, (name, _opener) in enumerate(open_apps)]
        choices.extend([("Open dashboard >", "dashboard")] if url else [])
        choices.extend([("Return to main menu", "menu"), ("Exit", "exit")])
        action = tui.review(
            "Onboarding complete", status, choices,
            instruction="↑↓ · Enter · → Dashboard · PgUp/Dn read · Esc Menu" if url else
            "↑↓ · Enter · PgUp/Dn read · Esc Menu",
            next_value="dashboard" if url else None,
            compact_actions=tui.rows() < 32,
        )
        if action is None:
            raise KeyboardInterrupt
        if action == "exit":
            return import_jobs_ui.Navigation.EXIT
        if isinstance(action, tuple):
            name, opener = open_apps[action[1]]
            app_results[name] = bool(opener())
            continue
        if action != "dashboard":
            return False
        try:
            if webbrowser.open(url):
                return True
        except (webbrowser.Error, OSError):
            pass
        open_failed = True
