"""Age-based retention cleanup for the web-editor PostgreSQL backend.

Run once at editor-pod boot (the editor is unique per project — Knative
``min 0/max 1`` — so there is no concurrency). Replaces the old heartbeat-staleness
``reset_repositories()`` total wipe with a granular 24h retention. NOT run on the
workers.
"""

DEFAULT_RETENTION_HOURS = 24


def delete_old_records(retention_hours: int = DEFAULT_RETENTION_HOURS) -> None:
    """Delete logs/executions/tasks older than ``retention_hours``.

    Logs are aged by ``db_inserted_at`` (DB clock); executions and tasks by their
    application ``created_at``. Indexed columns → cheap.
    """
    from .connection import get_pool

    interval = f"{int(retention_hours)} hours"
    with get_pool().connection() as conn, conn.cursor() as cur:
        cur.execute(
            "DELETE FROM execution_logs WHERE db_inserted_at < now() - %s::interval",
            (interval,),
        )
        cur.execute(
            "DELETE FROM executions WHERE created_at < now() - %s::interval",
            (interval,),
        )
        cur.execute(
            "DELETE FROM tasks WHERE created_at < now() - %s::interval",
            (interval,),
        )
