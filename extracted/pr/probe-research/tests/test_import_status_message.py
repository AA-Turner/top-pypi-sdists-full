"""A session import's status line names the walk position, and only during the walk.

A resumed import holds its bar at the count Probe already confirmed while the
worker re-checks every approved session, so the position is the one thing on
screen that moves. The worker test in test_backfill_transcripts_upload.py drives
the real walk; these pin the states that test cannot reach cheaply.
"""

from probe.cli import import_jobs as jobs, import_jobs_ui as ui


def _walking(**progress):
    """A running session import mid-walk: 3,855 confirmed, 3,200 re-checked."""
    return {
        "id": "walk", "kind": jobs.Kind.TRANSCRIPTS, "state": jobs.State.RUNNING,
        "label": "Sessions", "error": None,
        "progress": {
            "message": "Checking upload status", "session_id": "session", "source": "codex",
            "completed": 3200, "total": 3857,
            "completion_completed": 3855, "completion_total": 3857, "completion_ids": [],
            **progress,
        },
    }


def test_both_status_views_show_the_walk_position_in_the_bar_format():
    job = _walking()
    details = ui._summary(job)
    assert details[1].endswith("  3855/3857")
    assert details[2] == "  Checking upload status · 3200/3857 processed"
    # Re-running the same approval lands on the status page mid-walk.
    assert "Checking upload status · 3200/3857 processed" in ui._started_summary(job)


def test_no_position_where_the_bar_already_counts_the_walk_or_there_is_nothing_to_count():
    legacy = _walking()
    # A worker older than completion counters fills the bar from `completed`.
    for key in ("completion_completed", "completion_total", "completion_ids"):
        del legacy["progress"][key]
    empty = _walking(completed=0, total=0)
    folder = {**_walking(), "kind": jobs.Kind.FOLDER}
    for job in (legacy, empty, folder):
        assert ui._status_message(job) == "Checking upload status"


def test_updates_outside_the_walk_drop_session_id_so_their_counts_are_never_positions():
    """The start, cancel, connection-wait and final updates are written through
    `_progress_message` and `_ProgressEstimate.update`, which carry `completed`
    and `total` forward but not `session_id`. Keeping it would label the final
    update's upload count, or a stale position, as walk progress."""
    walk = _walking()["progress"]
    updates = {
        "Starting the approved import.": jobs._progress_message(walk, "Starting the approved import."),
        "Canceling import…": jobs._progress_message(walk, "Canceling import…"),
        "Waiting for connection. Retrying in 5s.": jobs._ProgressEstimate().update(
            walk, {"waiting_for_connection": True, "retry_in": 5, "network_retries": 1},
        ),
        "Connection retry: resuming saved import progress.": jobs._ProgressEstimate().update(walk, {}),
        "Session import finished": jobs._ProgressEstimate().update(walk, {
            "completed": 3690, "total": 3857, "uploaded": 3690, "failed": 0, "skipped_legacy": 158,
            "completion_completed": 3855, "completion_total": 3857, "completion_ids": [],
        }),
    }
    for message, progress in updates.items():
        assert "session_id" not in progress, message
        job = {**_walking(), "progress": {**progress, "message": message}}
        assert ui._status_message(job) == message
    assert ui._status_message({**_walking(), "state": jobs.State.INTERRUPTED}) == "Checking upload status"
