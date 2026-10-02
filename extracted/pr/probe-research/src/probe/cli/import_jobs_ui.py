"""The installer and main menu share one live view of durable imports."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from probe._compat import StrEnum
import math

from . import import_jobs, import_progress, tui


class Navigation(StrEnum):
    CONTINUE = "continue"
    MENU = "menu"
    EXIT = "exit"
    DETAILS = "details"
    RESUME = "resume"
    CANCEL = "cancel"
    BACK = "back"


STATE_LABELS = {
    import_jobs.State.QUEUED: "Queued",
    import_jobs.State.RUNNING: "Importing",
    import_jobs.State.SUCCEEDED: "Complete",
    import_jobs.State.FAILED: "Needs attention",
    import_jobs.State.INTERRUPTED: "Interrupted",
    import_jobs.State.CANCELED: "Canceled",
}


def _state_label(job: dict) -> str:
    state = job["state"]
    progress = job.get("progress") or {}
    if state == import_jobs.State.SUCCEEDED:
        completed, total = import_progress.counts(job)
        if completed is not None and total is not None and completed < total:
            return "Partially complete"
    if state == import_jobs.State.RUNNING:
        if progress.get("waiting_for_connection"):
            return "Waiting for connection"
        if progress.get("phase") == "scanning":
            return "Scanning"
    return STATE_LABELS.get(state, state)


def _status_lines(job: dict) -> list[str]:
    """The shared state and progress indicator for one saved import."""
    state = job["state"]
    progress = job.get("progress") or {}
    label = _state_label(job)
    mark, style = {
        import_jobs.State.QUEUED: ("·", "class:instruction"),
        import_jobs.State.RUNNING: ("»", "class:pointer"),
        import_jobs.State.SUCCEEDED: ("✔", "class:selected"),
        import_jobs.State.FAILED: ("✗", "class:instruction"),
        import_jobs.State.INTERRUPTED: ("!", "class:instruction"),
        import_jobs.State.CANCELED: ("·", "class:instruction"),
    }.get(state, ("·", "class:instruction"))
    if state == import_jobs.State.RUNNING and progress.get("waiting_for_connection"):
        label, mark, style = "Waiting for connection", "·", "class:instruction"
    if label == "Partially complete":
        mark, style = "!", "class:instruction"

    completed, total = import_progress.counts(job)
    measured = all(
        isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
        for value in (completed, total)
    ) and completed >= 0 and total > 0
    counter = f"  {completed:g}/{total:g}" if measured else ""
    if not import_progress.completion_known(job):
        counter = "  Completion unavailable"
    if state == import_jobs.State.SUCCEEDED and label != "Partially complete":
        bar = tui.progress_bar(1)
    elif measured:
        bar = tui.progress_bar(min(.99, completed / total))
    elif state in {import_jobs.State.QUEUED, import_jobs.State.RUNNING}:
        bar = tui.progress_bar(0)
    else:
        bar = tui.progress_bar(0)

    return [
        tui.StyledLine(f"{mark} {label}", style=style),
        tui.StyledLine(bar + counter, style=style),
    ]


def _started_summary(job: dict) -> list[str]:
    """Lead the handoff with the worker's current state and measured progress."""
    lines = [*_status_lines(job), job["label"]]
    remaining = _time_left(import_progress.summarize([job], job.get("kind"), _estimates))
    if remaining:
        lines[0] = tui.StyledLine(f"{lines[0]} · {remaining}", style=lines[0].style)
    progress = job.get("progress") or {}
    label = _state_label(job)
    if (job["state"] == import_jobs.State.RUNNING and progress.get("phase") == "scanning"
            and not progress.get("waiting_for_connection")):
        completed, total = (import_progress.number(progress.get(field)) for field in ("completed", "total"))
        if completed is not None and total and progress.get("stage"):
            lines[0] = tui.StyledLine(f"» Scanning · {completed:g}/{total:g} steps", style=lines[0].style)
    for message, shown in ((progress.get("message"), _status_message(job)), (job.get("error"), job.get("error"))):
        if message and message not in {label, f"{label}."}:
            lines.extend(tui.wrap(str(shown), width=70))
    return lines


def _status_message(job: dict) -> str:
    """The worker's message, plus how many sessions a running import has processed.

    The bar counts sessions Probe has confirmed, carried across attempts. A
    resumed import re-checks every approved session from the start, so the bar
    can hold at its old mark for the whole pass and read as hung; the walk
    position is the part that moves. Only the per-session walk publishes
    `session_id`: the start, lifecycle and final updates do not, and the final
    one's `completed` counts uploads. A worker without completion counters
    already fills the bar from `completed`, so it gets no repeat of it here.
    The count uses the bar's number format so the two lines read alike.
    """
    progress = job.get("progress") or {}
    message = str(progress.get("message") or "")
    processed, total = (import_progress.number(progress.get(field)) for field in ("completed", "total"))
    if (message and job["state"] == import_jobs.State.RUNNING
            and job.get("kind") == import_jobs.Kind.TRANSCRIPTS and progress.get("session_id")
            and import_progress.number(progress.get("completion_completed")) is not None
            and processed is not None and total):
        return f"{message} · {processed:g}/{total:g} processed"
    return message


def _summary(job: dict) -> list[str]:
    state = _state_label(job)
    progress = job.get("progress") or {}
    if job["state"] == import_jobs.State.RUNNING and progress.get("waiting_for_connection"):
        state = "Waiting for connection"
    lines = [f"{job['label']} · {state}"]
    lines.extend(_status_lines(job)[1:])
    if progress.get("message"):
        lines.extend(f"  {part}" for part in tui.wrap(_status_message(job), width=70))
    if job.get("error"):
        lines.extend(f"  {part}" for part in tui.wrap(job["error"], width=70))
    return lines


def show_started_import(job: dict) -> dict:
    """Show the saved import until the user chooses to continue.

    Staying here is the wait mode: the shared review refreshes the live status
    without another keypress. Leaving never stops or re-enqueues the worker.
    Return a fresh snapshot so a completed import is not reported as queued.
    """
    latest = job
    setup = bool(tui.onboarding_header())
    continue_label = "Continue setup (import continues)" if setup else "Continue"
    folder = job.get("kind") == import_jobs.Kind.FOLDER
    subject = "folder" if folder else "session"

    def status():
        nonlocal latest
        try:
            latest = import_jobs.get_job(job["id"])
        except import_jobs.JobError as exc:
            return [
                tui.StyledLine("! Status unavailable", style="class:instruction"),
                tui.StyledLine(tui.progress_bar(0), style="class:instruction"),
                "Saved, but its current status is unavailable.",
                str(exc), "", "Continue and check Existing imports later.",
            ]
        state = latest["state"]
        if _state_label(latest) == "Partially complete":
            guidance = ["This import stopped with some items unfinished.",
                        "See Existing imports before starting another."]
        elif state == import_jobs.State.SUCCEEDED:
            guidance = [f"Your {subject} import is complete."]
        elif state == import_jobs.State.CANCELED:
            guidance = ["Import canceled. Imported work is kept.",
                        "Resume it from Existing imports."]
        elif state in {import_jobs.State.FAILED, import_jobs.State.INTERRUPTED}:
            guidance = [
                "This import needs attention.",
                "Review or resume it from Existing imports.",
            ]
        else:
            guidance = [
                "Scanning and importing continue in the background."
                if folder and (latest.get("payload") or {}).get("auto_approve") else
                "The import continues in the background.",
                "Continue, or stay here to watch it finish.",
                "Progress: main menu → Existing imports.",
            ]
        return [*_started_summary(latest), "", *guidance]

    action = tui.review(
        f"{subject.capitalize()} import status", status, [(continue_label, Navigation.CONTINUE)],
        instruction="enter continue · tab read · pgup/dn · esc continue",
    )
    if action is None:
        raise KeyboardInterrupt
    # Escape continues too: leaving retains the approved import's saved work.
    # Refresh once more before returning the report.
    try:
        return import_jobs.get_job(job["id"])
    except import_jobs.JobError:
        return latest


_estimates = import_progress.Estimates()


def _time_left(summary: import_progress.Summary) -> str:
    if summary.state in {"Complete", "Not started"}:
        return ""
    if "attention" in summary.state or "connection" in summary.state:
        return ""
    if not summary.measured:
        return ""
    if summary.eta is not None and summary.eta > 0:
        minutes = max(1, math.ceil(summary.eta / 60))
        estimate = f"{minutes} min" if minutes < 60 else f"{minutes // 60} hr {minutes % 60} min"
        return f"~{estimate} left"
    if "Scanning" in summary.state:
        return "time estimate after scan"
    return "estimating time…" if summary.active else ""


def _category_lines(summary: import_progress.Summary) -> list[str]:
    style = ("class:selected" if summary.state == "Complete" else "class:pointer"
             if summary.active and "attention" not in summary.state and "connection" not in summary.state
             else "class:instruction")
    heading = f"{summary.title} · {summary.state}"
    remaining = _time_left(summary)
    if remaining:
        heading += f" · {remaining}"
    if not summary.measured:
        counter = "Completion unavailable"
    elif summary.total is None and summary.state == "Complete":
        counter = "Complete · count unavailable"
    elif summary.total is None:
        counter = f"{summary.completed:,.0f} {summary.unit} complete · total pending"
    elif summary.state == "Not started":
        counter = f"0 {summary.unit}"
    else:
        counter = f"{summary.completed:,.0f}/{summary.total:,.0f} {summary.unit} · {int(summary.fraction * 100)}%"
    room = max(20, min(tui.CONTENT_WIDTH, tui.columns() - tui.left_pad() - 1))
    width = max(8, min(28, room - len(counter) - 2))
    return [
        tui.StyledLine(heading, style=style),
        tui.StyledLine(f"{tui.progress_bar(summary.fraction, width=width)}  {counter}", style=style),
    ]


def progress_lines(jobs: Sequence[dict], *, hide_empty: bool = False) -> list[str]:
    """Two current completion bars; older completed jobs stay behind Details."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)
    summaries = [
        import_progress.summarize(jobs, kind, _estimates, completed_since=cutoff)
        for kind in (import_jobs.Kind.TRANSCRIPTS, import_jobs.Kind.FOLDER)
    ]
    unreadable = sum(job.get("readable") is False for job in jobs)
    if hide_empty and not unreadable and all(summary.state == "Not started" for summary in summaries):
        return []
    lines = []
    for summary in summaries:
        if lines:
            lines.append("")
        lines.extend(_category_lines(summary))
    if unreadable:
        lines.append(tui.StyledLine("A saved import needs attention. View details.", style="class:instruction"))
    return lines


def active_progress_lines(jobs: Sequence[dict] | None = None) -> list[str]:
    """Show unfinished imports and completions from the last 24 hours."""
    saved = import_jobs.list_jobs() if jobs is None else jobs
    return progress_lines(saved, hide_empty=True) if saved else []


def _all_imports(*, onboarding: bool = False) -> list[str]:
    return progress_lines(import_jobs.list_jobs())


def _read_detail(job_id: str) -> tuple[dict | None, list[str]]:
    try:
        job = import_jobs.get_job(job_id)
    except import_jobs.JobError as exc:
        return None, [
            "Import details are unavailable.", str(exc), "",
            "The saved job was retained.",
        ]
    lines = [*_summary(job), "", f"Started: {job.get('started_at') or 'Waiting'}"]
    if job.get("finished_at"):
        lines.append(f"Finished: {job['finished_at']}")
    if job.get("report"):
        lines.extend(["", "Result", *job["report"]])
    lines.extend(["", f"Job: {job['id']}", f"Log: {job['log_path']}"])
    return job, lines


def _detail(job_id: str) -> list[str]:
    return _read_detail(job_id)[1]


def _can_resume(job: dict) -> bool:
    return not job.get("cancel_requested") and job["state"] in {
        import_jobs.State.FAILED, import_jobs.State.INTERRUPTED, import_jobs.State.CANCELED,
    }


def _detail_choices(job: dict | None) -> list[tuple[str, Navigation]]:
    choices = []
    if job is not None:
        if _can_resume(job):
            choices.append(("Resume import", Navigation.RESUME))
        if job["state"] not in {import_jobs.State.SUCCEEDED, import_jobs.State.CANCELED}:
            choices.append(("Cancel import", Navigation.CANCEL))
    return [*choices, ("Back to all imports", Navigation.BACK)]


def _choose_import(notices: Sequence[str] = ()) -> None:
    jobs = import_jobs.list_jobs()
    if not jobs:
        tui.review("Import details", [*notices, "", "No saved imports."], [("Back", Navigation.BACK)])
        return
    picked = tui.review(
        "Existing imports",
        ["Pick an import to view, resume or cancel.",
         *(["", "Import details", *notices] if notices else [])],
        [(f"{job['label']} · {_state_label(job)}", job["id"]) for job in jobs]
        + [("Back to all imports", Navigation.BACK)],
    )
    if picked is None or picked is tui.BACK or picked == Navigation.BACK:
        return
    while True:
        try:
            job = import_jobs.get_job(picked)
        except import_jobs.JobError as exc:
            tui.review("Import needs attention", [str(exc)], [("Back", Navigation.BACK)])
            return
        latest = job

        def detail():
            nonlocal latest
            latest, lines = _read_detail(picked)
            return lines

        action = tui.review(
            job["label"], detail, lambda: _detail_choices(latest),
            copy_text=job["log_path"], copy_label="log path",
            instruction="↑↓ · enter · c copy log path · tab read · esc back",
            fallback=Navigation.BACK,
        )
        if action not in {Navigation.RESUME, Navigation.CANCEL}:
            return
        try:
            # The live document can change while this prompt stays open.
            # Recheck when Enter is pressed: a job may have finished while the
            # user was choosing Cancel. Resume never restarts active work.
            current = import_jobs.get_job(picked)
            if action == Navigation.CANCEL:
                if current["state"] not in {import_jobs.State.SUCCEEDED, import_jobs.State.CANCELED}:
                    import_jobs.cancel(picked)
            elif _can_resume(current):
                import_jobs.resume(picked)
        except import_jobs.JobError as exc:
            tui.review("Import needs attention", [str(exc)], [("Back", Navigation.BACK)])
            return


def show_imports(*, onboarding: bool = False, notices: Sequence[str] = ()) -> Navigation:
    """Monitor every import and return to the main menu without stopping work."""
    import_jobs.recover_jobs()
    while True:
        choices = [
            ("View details or resume", Navigation.DETAILS),
            ("Return to main menu", Navigation.MENU),
        ]
        action = tui.review(
            "Your imports", lambda: _all_imports(onboarding=onboarding), choices,
            instruction="↑↓ · enter · esc menu",
        )
        if action == Navigation.DETAILS:
            _choose_import(notices)
            continue
        if action == Navigation.EXIT or action is None:
            return Navigation.EXIT
        return Navigation.MENU
