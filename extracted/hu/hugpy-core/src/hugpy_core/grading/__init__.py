"""Grading: what every model is asked, and what the call log says came of it.

    queries   the queries Core starts with, by task, in tiers (the grading table's own rows), and its media files
    read      the table, every model's schedule, the graded calls and their verdicts: reads of the call log by
              its grading marker, worked out when asked for
    rounds    a mass shot of grading calls (a test fire of a wrapper, a grading of chosen models): what was asked
              is kept, what came of it is the call log's

A grading call is an ordinary call: its body carries {"metadata": {"grading": {"query", "tier", "round"}}}, the
wrapper keeps the body in its call log, and Core finds the call, and its answer, by that marker.
"""
from .. import sql
from . import queries, read, rounds


def prepare() -> None:
    """The grading table's own rows as this version defines them, and the rounds that were being sent when Core
    last stopped noted as ended. Run once, when Core starts, after sql.prepare()."""
    conn = sql.writer()
    try:
        with conn:
            queries.seed(conn)
    finally:
        conn.close()
    rounds.close_interrupted()


__all__ = ['prepare', 'queries', 'read', 'rounds']
