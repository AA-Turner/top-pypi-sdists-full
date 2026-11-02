"""The scheduler's review-flag raiser (review flags, 0117) — author marks + engine auto-flags.

The run carries on and SUCCEEDS; each flag is one awaited single-row write through the ONE
``workflow.run_log`` writer (``matrx_graph.run_log.write_run_log``) and NEVER raises.

Where the scheduler raises them (labels are stable — they are the issue signature):

* ``data.review`` on a step → ``review.label`` or ``flagged_step.<node_id>`` (source
  ``flagged_step``) each time an attempt STARTS — after ``node_started``, never for a
  replayed outcome.
* ``data.review`` on a connection → ``review.label`` or ``flagged_path.<edge_id>`` (source
  ``flagged_path``, node = the TARGET) each time the connection is TAKEN — a delivered
  binding, a back-edge re-fire or an edge fan-out; never a prune. Edge routing is
  synchronous, so these are QUEUED during the canonical routing pass and flushed right after
  it; a run-ahead (partial) routing never queues, and a routing pass that fails discards.
* engine: ``engine.retry`` (a retry was scheduled), ``engine.caught_failure`` (a failure
  routed down an ERROR connection), ``engine.optional_step_failed`` (an optional step failed
  and the run went on), ``engine.item_skipped`` (a fan-out item became a hole),
  ``engine.output_shape`` (output did not match its kind, or its declared kind could not be
  checked, and the run went on),
  ``engine.mapping_read_nothing`` (a connection's mapped path was not in this output, so the
  input arrived absent — once per (run, connection, path); ``Scheduler._queue_mapping_miss``).

REPLAY / RESUME (no double flag for one occurrence): every flag carries an ``occurrence_key``
built from its full correlation identity (node, step, attempt, dispatch, item, firing, edge).
In-process the key is remembered; across a crash/resume the writer finds the row with the
same key and does not write it twice. A replayed outcome never re-raises a step / retry /
failure flag at all — those are raised only on the fresh-execution path.

A runaway (a fan-out of thousands of holes) must not eat the run's whole ``run_log`` budget
and starve "Record a Problem": at most the ``workflow.review_flags.max_flags_per_issue_per_run`` knob's flags per
(node, connection, label) per run; the rest are counted in the log only.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)



@dataclass(frozen=True)
class ReviewFlag:
    node_id: str
    step: int
    attempt: int
    label: str
    message: str
    category: str
    source: str
    occurrence_key: str
    edge_id: str | None = None
    severity: str = "warning"
    payload: dict[str, Any] | None = None


def occurrence_key(
    *,
    node_id: str,
    step: int,
    attempt: int,
    dispatch_id: str = "",
    item_index: int = 0,
    firing: int = 0,
    edge_id: str | None = None,
    label: str,
) -> str:
    return f"{label}|{node_id}|{edge_id or ''}|s{step}|a{attempt}|{dispatch_id}:{item_index}|f{firing}"


@dataclass
class ReviewFlagger:
    organization_id: str | None
    user_id: str | None
    _pending: list[ReviewFlag] = field(default_factory=list)
    _seen: set[str] = field(default_factory=set)
    _per_signature: dict[tuple[str, str, str], int] = field(default_factory=dict)

    def queue(self, flag: ReviewFlag) -> None:
        self._pending.append(flag)

    def discard_pending(self) -> None:
        self._pending.clear()

    async def flush(self, run_id: str) -> None:
        pending, self._pending = self._pending, []
        for flag in pending:
            await self.raise_flag(run_id, flag)

    async def raise_flag(self, run_id: str, flag: ReviewFlag) -> bool:
        """Write one flag. Never raises; returns whether a row landed (or already had)."""
        try:
            if flag.occurrence_key in self._seen:
                return True
            self._seen.add(flag.occurrence_key)
            signature = (flag.node_id, flag.edge_id or "", flag.label)
            count = self._per_signature.get(signature, 0) + 1
            self._per_signature[signature] = count
            from matrx_graph.knobs import review_flag_policy

            per_issue = (await review_flag_policy()).max_flags_per_issue_per_run
            if count > per_issue:
                if count == per_issue + 1:
                    logger.warning(
                        "[wf:%s node=%s] review flag '%s' raised %d times this run — "
                        "further occurrences are not recorded (the issue already shows it).",
                        run_id[:8], flag.node_id, flag.label, per_issue,
                    )
                return False
            from matrx_graph import run_log

            entry = await run_log.write_run_log(
                run_id=run_id,
                node_id=flag.node_id,
                step=flag.step,
                attempt=flag.attempt,
                label=flag.label,
                message=flag.message,
                severity=flag.severity,
                payload=flag.payload,
                organization_id=self.organization_id,
                user_id=self.user_id,
                needs_review=True,
                category=flag.category,
                source=flag.source,
                edge_id=flag.edge_id,
                occurrence_key=flag.occurrence_key,
            )
            return bool(entry.recorded)
        except Exception:  # noqa: BLE001 — a flag never fails the run
            logger.exception("[wf:%s] review flag '%s' could not be raised", run_id[:8], flag.label)
            return False


__all__ = [
    "ReviewFlag",
    "ReviewFlagger",
    "occurrence_key",
]
