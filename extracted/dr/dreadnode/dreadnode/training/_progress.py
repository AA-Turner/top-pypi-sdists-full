"""Hosted training progress push helper.

Client-side counterpart to the ``/training/jobs/{id}/progress`` endpoint.
Mirrors ``dreadnode.optimization.jobs._post_progress_update`` — one async
helper the sandbox SDK calls on every lifecycle event. Non-terminal events
are best-effort (single attempt, log-and-continue). Terminal events
(``training_end`` / ``training_error``) are authoritative and retry a
bounded number of times with exponential backoff, because a lost terminal
push would leave the API polling until the timeout deadline.

The helper **never raises**: the controller's sandbox-liveness probe is the
safety net for a genuinely lost close. See
``app.training._launch.wait_for_terminal_status``.
"""

import asyncio
import logging
import typing as t

from dreadnode import Dreadnode
from dreadnode.app.api.models import (
    TERMINAL_TRAINING_PROGRESS_EVENTS,
    TrainingJob,
    TrainingJobProgressUpdateRequest,
)

logger = logging.getLogger(__name__)

_TERMINAL_PROGRESS_RETRY_ATTEMPTS = 3
_TERMINAL_PROGRESS_RETRY_BACKOFF_SEC = 0.5


async def push_progress_update(
    *,
    dn: Dreadnode,
    job_id: str,
    request: TrainingJobProgressUpdateRequest,
) -> TrainingJob | None:
    """Post one hosted training progress update back to the API.

    Returns the updated :class:`TrainingJob` on success, or ``None`` if the
    push was dropped (missing org/workspace on the client, or all attempts
    exhausted). Never raises — the caller doesn't need a try/except around
    it; the liveness-probe failsafe in the controller handles lost closes.
    """
    organization = dn.organization
    workspace = dn.workspace
    if not isinstance(organization, str) or not isinstance(workspace, str):
        logger.warning(
            "Skipping training progress update event_type=%s — missing org/workspace on dn",
            request.event_type,
        )
        return None

    is_terminal = request.event_type in TERMINAL_TRAINING_PROGRESS_EVENTS
    attempts = _TERMINAL_PROGRESS_RETRY_ATTEMPTS if is_terminal else 1

    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            result = await asyncio.to_thread(
                dn.api.post_training_job_progress,
                organization,
                workspace,
                job_id,
                request,
            )
        except Exception as exc:
            last_error = exc
            if attempt >= attempts:
                break
            backoff = _TERMINAL_PROGRESS_RETRY_BACKOFF_SEC * (2 ** (attempt - 1))
            logger.warning(
                "Terminal training progress failed attempt=%d/%d event_type=%s job_id=%s: %s: %s; retrying in %.1fs",
                attempt,
                attempts,
                request.event_type,
                job_id,
                type(exc).__name__,
                exc,
                backoff,
            )
            await asyncio.sleep(backoff)
            continue

        if is_terminal and attempt > 1:
            logger.info(
                "Terminal training progress landed on attempt=%d event_type=%s job_id=%s",
                attempt,
                request.event_type,
                job_id,
            )
        return result

    if last_error is not None:
        logger.warning(
            "Training progress failed event_type=%s job_id=%s: %s: %s",
            request.event_type,
            job_id,
            type(last_error).__name__,
            last_error,
        )
    return None


class ProgressPushCallback:
    """Tinker trainer callback that emits step / eval / checkpoint events.

    Aggregates metrics into the axis-step shape the API merge function
    expects (``steps: [n]`` + ``train/loss: [x]``) and posts one event per
    step. Runs on the sync worker thread that drives Tinker's training loop
    so it uses :func:`push_progress_update_sync` — terminal events still
    flow through :func:`push_progress_update` from ``run_job_by_id``.
    """

    def __init__(self, *, dn: Dreadnode, job_id: str) -> None:
        self._dn = dn
        self._job_id = job_id

    def on_step_start(self, step: int, state: t.Any) -> None:
        del step, state

    def on_step_end(
        self, step: int, state: t.Any, metrics: dict[str, float]
    ) -> None:
        # Shape the per-step metric dict into the axis-step layout the merge
        # function expects: one-element axis + one-element series arrays.
        series: dict[str, list[float]] = {}
        for key, value in metrics.items():
            if not key.startswith("train/"):
                continue
            series[f"train/{key.split('/')[-1]}"] = [value]
        # Skip the push entirely if there are no train-scoped metrics — the
        # bare ``steps`` axis alone isn't worth a round-trip.
        if not series:
            return
        payload: dict[str, t.Any] = {"steps": [step], **series}
        push_progress_update_sync(
            dn=self._dn,
            job_id=self._job_id,
            request=TrainingJobProgressUpdateRequest(
                event_type="step_complete",
                metrics=payload,
                data={"step": step},
            ),
        )

    def on_checkpoint(
        self, checkpoint_num: int, checkpoint_path: str, state: t.Any
    ) -> None:
        del state
        push_progress_update_sync(
            dn=self._dn,
            job_id=self._job_id,
            request=TrainingJobProgressUpdateRequest(
                event_type="checkpoint_saved",
                message=f"checkpoint {checkpoint_num} saved",
                artifacts={"latest_checkpoint": checkpoint_path},
                data={"checkpoint_num": checkpoint_num},
            ),
        )

    def on_evaluation(
        self,
        state: t.Any,
        metrics: dict[str, float],
        *,
        step: int | None = None,
    ) -> None:
        """Push an ``eval_complete`` event with the supplied metrics.

        ``step`` is optional. When omitted the metrics are pushed as
        scalars — the UI auto-discovery panel surfaces them as highlight
        tiles. When provided, they're shaped into the axis-step layout
        (``eval/steps: [step]`` + ``eval/<metric>: [value]``) so each call
        appends to the running array; the metrics panel groups them by
        base name on the chart card alongside the matching ``train/<metric>``
        series.
        """
        del state
        if not metrics:
            return
        eval_metrics: dict[str, t.Any] = {}
        if step is not None:
            eval_metrics["eval/steps"] = [step]
        for key, value in metrics.items():
            normalized_key = f"eval/{key.split('/')[-1]}"
            eval_metrics[normalized_key] = [value] if step is not None else value
        push_progress_update_sync(
            dn=self._dn,
            job_id=self._job_id,
            request=TrainingJobProgressUpdateRequest(
                event_type="eval_complete",
                message="evaluation complete",
                metrics=eval_metrics,
            ),
        )


def push_progress_update_sync(
    *,
    dn: Dreadnode,
    job_id: str,
    request: TrainingJobProgressUpdateRequest,
) -> TrainingJob | None:
    """Synchronous best-effort sibling of :func:`push_progress_update`.

    Designed for calling from non-async contexts — specifically the Tinker
    trainer's sync ``TrainingCallback`` hooks, which run on a worker thread
    with no event loop. One attempt, swallows all errors, returns ``None``
    on failure. **Non-terminal events only** — terminal lifecycle events
    must go through the async helper so the retry ladder kicks in.
    """
    organization = dn.organization
    workspace = dn.workspace
    if not isinstance(organization, str) or not isinstance(workspace, str):
        logger.warning(
            "Skipping training progress update event_type=%s — missing org/workspace on dn",
            request.event_type,
        )
        return None

    if request.event_type in TERMINAL_TRAINING_PROGRESS_EVENTS:
        raise ValueError(
            "push_progress_update_sync is for non-terminal events; use "
            "push_progress_update (async) for training_end / training_error"
        )

    try:
        return dn.api.post_training_job_progress(
            organization, workspace, job_id, request
        )
    except Exception as exc:
        logger.warning(
            "Training progress failed (sync) event_type=%s job_id=%s: %s: %s",
            request.event_type,
            job_id,
            type(exc).__name__,
            exc,
        )
        return None


__all__ = [
    "ProgressPushCallback",
    "push_progress_update",
    "push_progress_update_sync",
]
