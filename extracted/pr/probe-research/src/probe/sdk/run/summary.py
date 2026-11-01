"""The run's headline scalars under both wire names, plus finish accounting (W&B wandb_summary)."""

from __future__ import annotations
from typing import Any
from .. import errors


def _summary_wire(summary: dict | None) -> dict[str, dict]:
    """The headline-scalar map under BOTH wire names, for any body that carries it.

    `summary_metrics` is the real field; `summary` is the alias the server still
    accepts. Sending both is what makes this client safe in either direction, and
    neither hazard is hypothetical:

    * send only `summary` and the server can never drop the alias, because doing so
      would silently discard the map from every client still in the field;
    * send only `summary_metrics` and a server OLDER than the rename discards it
      just as silently -- and prod ran a pre-rename image for ~30 minutes on
      2026-09-21 while a failing post-upgrade hook rolled releases back.

    Both keys cost a few bytes and close both holes: every input schema resolves
    `AliasChoices("summary_metrics", "summary")`, taking the new name when present,
    and none sets `extra="forbid"`, so the spare key is ignored rather than refused
    -- including by a future server that has dropped the alias entirely.
    """
    return {"summary_metrics": summary, "summary": summary}


def _one_summary(summary_metrics: dict | None, summary: dict | None) -> dict | None:
    """Resolve the new kwarg against its deprecated spelling.

    `summary_metrics` is the field's real name: headline scalars the run ACHIEVED,
    which read as prose under the old name beside `summary_markdown` and the
    generated AI summary. `summary` is still accepted so a script written against an
    older SDK keeps working; passing both is a contradiction, not a merge.

    ON THE WIRE the map is sent under BOTH names -- see `_summary_wire`.
    """
    if summary_metrics is not None and summary is not None:
        raise errors.ValidationError(
            "pass summary_metrics or summary, not both: they are the same field, and "
            "silently preferring either is how a run ends up with the wrong numbers"
        )
    return summary_metrics if summary_metrics is not None else summary


def _with_finish_accounting(summary: dict | None, facts: dict[str, Any]) -> dict:
    """``summary`` with ``facts`` added to its ``probe_finish`` map, never in
    place of it: a caller's own close accounting (a reinit's ``closed_by``)
    survives the deferred and dead-letter branches, which write theirs into
    the same key."""
    accounting = (summary or {}).get("probe_finish")
    return {
        **(summary or {}),
        "probe_finish": {**(accounting if isinstance(accounting, dict) else {}), **facts},
    }
