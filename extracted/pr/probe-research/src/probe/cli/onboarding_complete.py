"""Finish terminal onboarding by handing off to the dashboard."""

from __future__ import annotations

import webbrowser

from probe.sdk.links import dashboard_base_url

from . import import_jobs, import_jobs_ui, import_progress, tui


def _needs_attention(jobs: list[dict]) -> bool:
    summaries = [import_progress.summarize(jobs, kind)
                 for kind in (import_jobs.Kind.TRANSCRIPTS, import_jobs.Kind.FOLDER)]
    return (any(job.get("readable") is False for job in jobs)
            or any("attention" in summary.state or summary.state == "Partially complete"
                   for summary in summaries))


def show(base_url: str) -> bool | import_jobs_ui.Navigation:
    """Return true for dashboard, false for main menu, or Navigation.EXIT.

    Opening the dashboard and exiting the wizard both leave approved background
    imports running, with their saved progress available in Existing imports.
    """
    base = dashboard_base_url(base_url)
    url = f"{base}/projects" if base else None
    open_failed = False

    def status():
        jobs = import_jobs.list_jobs()
        lines = ["Probe is installed."]
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
        choices = [("Open dashboard >", "dashboard")] if url else []
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
        if action != "dashboard":
            return False
        try:
            if webbrowser.open(url):
                return True
        except (webbrowser.Error, OSError):
            pass
        open_failed = True
