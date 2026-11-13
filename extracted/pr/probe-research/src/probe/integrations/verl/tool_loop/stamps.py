"""What a verl agent loop carries to the trainer and to its reward worker, and how: every stamp is a JSON STRING
(F5: a dict in `reward_extra_info` crashes `process_validation_metrics`), each under its own key so the V0 batch,
which turns `extra_fields` and `reward_extra_info` keys into one set of columns, never merges two of them."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

#: A training loop's capture (`RolloutCapture.export`), in its last output's `extra_fields` (V1 hands it to
#: `_update_actor`; V0 makes it a column).
ROLLOUT_FIELD = "probe_rollout"
#: A validation loop's capture, in `reward_extra_info` (what `_validate` hands on, V1 and V0). Every validation loop
#: carries it, `""` when it has none: the V0 postprocess reads the first row's keys from every row (`agent_loop.py:1196`).
ROLLOUT_EVAL_FIELD = "probe_rollout_eval"
#: The rollout's handle (`RolloutCapture.to_handle`) for the reward worker, in `extra_fields` while verl scores the
#: loop (it reaches `RewardLoopWorker.compute_score` as `tool_extra_fields`, `agent_loop.py:1098`); taken off after.
HANDLE_FIELD = "probe_rollout_handle"
#: The files a reward worker attached, back in that call's `reward_extra_info`; taken off before verl reads it.
FILES_FIELD = "probe_files"
#: A key verl's capture adds beside the export's own: the loop ended past `response_length` (F4), so its sample's
#: finish reason is `length` whatever the engine said.
FINISH_FIELD = "finish_reason"


def to_stamp(payload: Mapping[str, Any] | None) -> str:
    """``payload`` as one JSON string; `""` for nothing."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False, default=str) if payload else ""


def read_stamp(value: Any) -> dict | None:
    """A stamp back as a dict; None for none (V1 fills a key one loop lacked with None, V0 with None or `""`), and
    for anything that is not one (a dict a caller wrote by hand is taken as it is)."""
    if isinstance(value, Mapping):
        return dict(value)
    item = getattr(value, "item", None)  # a 0-d numpy object cell
    if callable(item) and not isinstance(value, (str, bytes)):
        try:
            value = item()
        except Exception:  # noqa: BLE001 -- not a scalar
            return None
    if not isinstance(value, str) or not value:
        return None
    try:
        found = json.loads(value)
    except ValueError:
        return None
    return found if isinstance(found, dict) else None
