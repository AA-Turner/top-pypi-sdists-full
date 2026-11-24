"""What a trainer integration knows about its run, sent once per run per process as an automatic declaration (0515,
D3/D4): its type (TRL's SFTTrainer is `sft`) and its total steps (HF/TRL `max_steps`, Lightning
`estimated_stepping_batches`, Miles `num_rollout` x updates per rollout, verl/SkyRL `total_training_steps`). Automatic
means the server fills only what nobody set. Never raises: a fact Probe cannot send never costs the training.

`total_steps` is the step the run's last point is logged at, on the run's own step axis, because the run's
`current_step` is the newest step it logged: a finished run then reads total/total whatever its trainer counts
from. A trainer that counts from 1 (HF, TRL, verl, SkyRL) ends at its count; one that counts from 0 (Miles' rollout
ids, Lightning's logged step) ends at its count less 1, which only the integration knows."""

from __future__ import annotations

import logging
from typing import Any

from ..values.total_steps import read_total_steps

logger = logging.getLogger(__name__)

#: (run id, fact) pairs this process already sent, or the server refused for good (a 4xx).
_SENT: set[tuple[str, str]] = set()


def send_total_steps(run: Any, value: Any, *, is_zero_based: bool = False) -> None:
    """Fill ``run``'s total steps from the trainer's own step count, unless the count is unknown (None, 0, -1, inf).
    ``is_zero_based``: the trainer logs its steps 0..count-1, so its last step is count - 1 (a one-step run of
    such a trainer ends at step 0, which no total can say: it stays unknown)."""
    total = read_total_steps(value)
    if total is not None and is_zero_based:
        total = read_total_steps(total - 1)
    if total is not None:
        _send_once(run, "total_steps", lambda: run.set_total_steps(total, is_automatic=True))


def send_run_type(run: Any, run_type: str) -> None:
    """Fill ``run``'s type when nobody declared one (a run the script opened itself and the trainer adopted)."""
    _send_once(run, "run_type", lambda: run.set_run_type(run_type, is_automatic=True))


def _send_once(run: Any, fact: str, send: Any) -> None:
    run_id = str(getattr(run, "id", "") or "")
    if not run_id or (run_id, fact) in _SENT:
        return
    try:
        send()
    except Exception as exc:  # noqa: BLE001 -- fail open
        logger.debug("probe: could not send %s for run %s (%s: %s)", fact, run_id, type(exc).__name__, exc)
        status = getattr(exc, "status", None)
        if not (isinstance(status, int) and 400 <= status < 500):
            return  # transient: the next call tries again
    _SENT.add((run_id, fact))
