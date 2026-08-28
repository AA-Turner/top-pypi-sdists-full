# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Consistent Ray dashboard names for Geneva tasks and actors.

The Ray dashboard, the state API (``ray list tasks|actors``) and the worker log
prefixes all show two strings: a task's ``name`` and an actor's ``repr``.
Building both through one formatter means every row carries the same fields --
component, table, column and ``job_id`` -- so a row on the dashboard can be
matched back to its row in the ``_geneva_jobs`` history table.

Names look like::

    job=8f1c4d02-... backfill.driver(videos.embedding)
    job=8f1c4d02-... applier.run(videos.embedding) frag=12 off=4096

The job id leads: it is the field that links the row back to the history
table, and leading it is what keeps it out of reach of the length cap, which
can only ever trim the trailing scope.

Actor *names* (``.options(name=...)``) are deliberately not built here: a Ray
actor name is a cluster-unique handle used for lookups, so it stays a stable
identifier while the human-readable detail goes in the actor's ``repr``.

This module has no Ray or Geneva imports so it stays importable from anywhere.
"""

import re

# Keep any single field short enough that a dashboard column stays readable,
# and cap the whole name so a pathological table/UDF name can't produce a
# multi-KB string on every task.
_MAX_PART_LEN = 48
_MAX_NAME_LEN = 200

# Control characters break log-prefix and dashboard rendering; newlines and
# tabs inside a table or UDF name would split a name across lines.
_CONTROL = re.compile(r"[\x00-\x1f\x7f]+")
_WHITESPACE = re.compile(r"\s+")


def _clean(
    value: object | None,
    limit: int = _MAX_PART_LEN,
    *,
    keep_spaces: bool = False,
) -> str | None:
    """Normalize one name field, returning None when there is nothing to show.

    ``keep_spaces`` is for fields this module composes itself (the ``detail``
    scope), where a space separates sub-fields; identifiers coming from user
    data collapse their whitespace to underscores instead.
    """
    if value is None:
        return None
    text = _WHITESPACE.sub(" " if keep_spaces else "_", _CONTROL.sub(" ", str(value)))
    text = text.strip(" _")
    if not text:
        return None
    if len(text) > limit:
        text = text[: limit - 1] + "~"
    return text


def ray_name(
    component: str,
    *,
    table: str | None = None,
    column: str | None = None,
    job_id: str | None = None,
    detail: str | None = None,
) -> str:
    """Build a Ray task name / actor repr for one unit of Geneva work.

    Parameters
    ----------
    component
        What the unit is, e.g. ``"backfill.driver"`` or ``"applier.run"``.
    table
        Destination table the work writes to.
    column
        Column (or UDF) the work produces.
    job_id
        Job history id. Printed first, so it survives the length cap and is
        the first thing to copy into a ``_geneva_jobs`` lookup.
    detail
        Free-form scoping such as ``"frag=12 off=4096"``. Must not carry row
        values -- a name is displayed in the dashboard, served by the state
        API and stamped onto worker log lines. Identify a partition by
        column and ordinal or by a digest, never by the value itself.
    """
    name = _clean(component) or "geneva"
    scope = ".".join(p for p in (_clean(table), _clean(column)) if p)
    if scope:
        name = f"{name}({scope})"
    if (extra := _clean(detail, limit=_MAX_PART_LEN * 2, keep_spaces=True)) is not None:
        name = f"{name} {extra}"
    if (job := _clean(job_id, limit=_MAX_PART_LEN)) is not None:
        name = f"job={job} {name}"
    # Every field is individually capped well inside the budget, so the job
    # prefix and the component always fit; only the trailing scope can be cut.
    return name[:_MAX_NAME_LEN]


def job_tracker_name(job_id: str, *, prefix: str = "jobtracker") -> str:
    """Return the cluster-unique Ray actor name for a job's JobTracker.

    Kept stable (``jobtracker-<job_id>``) because it is a lookup handle; the
    tracker's ``repr`` carries the readable detail.
    """
    return f"{prefix}-{job_id}"
