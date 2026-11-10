"""Sample parts as `POST /v1/runs/{id}/samples/batch` takes them (twin: app/runs/samples): the body's
lists checked against the contract (`probe.generated.samples`), the scrub of logs and turns, and the
4 KiB log tail and 1 MiB log cap."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from ....foundation.compat.compat import StrEnum
from ...values.unstorable import ESCAPE as NUL_ESCAPE
from ...values.unstorable import NUL
from ....generated.samples import (
    CommitIn,
    GroupIn,
    LiveTurnIn,
    PlanIn,
    SamplePartIn,
    SealIn,
    TaskIn,
    WeightVersionIn,
)


class BatchList(StrEnum):
    """The lists a samples batch body carries (`SampleBatchIn`); the drain concatenates each when
    it merges ops. `plan` is one object, not a list: ops with different plans never merge."""

    TASKS = "tasks"
    SAMPLES = "samples"
    GROUPS = "groups"
    SEALS = "seals"
    COMMITS = "commits"
    WEIGHTS = "weights"
    LIVE_TURNS = "live_turns"


#: Each list's item, as the contract shapes it: every item is checked here before it is journaled,
#: so a part sending a field its role does not own is dropped alone, never 422s its whole batch.
ITEM_MODELS: dict[BatchList, type[BaseModel]] = {
    BatchList.TASKS: TaskIn,
    BatchList.SAMPLES: SamplePartIn,
    BatchList.GROUPS: GroupIn,
    BatchList.SEALS: SealIn,
    BatchList.COMMITS: CommitIn,
    BatchList.WEIGHTS: WeightVersionIn,
    BatchList.LIVE_TURNS: LiveTurnIn,
}
#: The batch's one plan-change object (`PlanIn`).
PLAN_FIELD = "plan"
PLAN_FIELDS = tuple(PlanIn.model_fields)


def to_wire_item(name: BatchList, item: Mapping[str, Any]) -> tuple[dict, BaseModel]:
    """``item`` checked against its contract model; its JSON as sent (only the fields set) and the
    model. Raises the model's ValidationError."""
    model = ITEM_MODELS[name].model_validate(item)
    return model.model_dump(mode="json", exclude_unset=True), model


def to_wire_plan(plan: Mapping[str, Any]) -> dict:
    """A plan change checked against `PlanIn`: only the fields given."""
    return PlanIn.model_validate(plan).model_dump(mode="json", exclude_unset=True)


#: Text a row holds inline; longer goes whole to R2 as a blob (D2).
MAX_INLINE_TEXT_BYTES = 64 * 1024
#: The log tail kept on the row.
MAX_LOG_TAIL_BYTES = 4 * 1024
#: One sample's full log in its bundle, keeping the tail (§3.3b).
MAX_LOG_BYTES = 1024 * 1024
MAX_ERROR_MESSAGE_CHARS = 1024

#: Task fields a generator sample may carry; the SDK lifts them into one `tasks` item per task.
TASK_FIELDS = ("prompt", "label", "dataset", "reward_max")
#: SDK-only input names, never sent as such: the full log, the per-token arrays.
LOG_INPUTS = ("log_text",)
TOKEN_INPUTS = {"tokens": "token_arrays", "trainer_tokens": "trainer_token_arrays"}


def to_plain(value: Any) -> dict:
    """A sample given as a dict or a pydantic model, as a plain dict with no None fields."""
    if isinstance(value, Mapping):
        return {key: item for key, item in value.items() if item is not None}
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        return dump(mode="json", exclude_none=True)
    raise TypeError(f"a sample is a dict or a model, not {type(value).__name__}")


def cut_tail(text: str, limit: int) -> tuple[str, bool]:
    """The last ``limit`` bytes of ``text`` (on a character boundary) and whether it was cut."""
    raw = text.encode("utf-8")
    if len(raw) <= limit:
        return text, False
    return raw[-limit:].decode("utf-8", errors="ignore"), True


def scrub_part(part: dict, scrub) -> dict:
    """Logs, the error line and every turn's message text through the credential scrubber
    (``scrub``: str -> str), before anything is journaled: tool output can carry keys. The turns
    are copied first: the caller's own objects are never rewritten. A scrubbed tail is cut to
    4 KiB again (a redaction marker can be longer than the key it replaced)."""
    for name in ("log_text", "log_tail", "error_message"):
        if isinstance(part.get(name), str):
            part[name] = scrub(part[name])
    if isinstance(part.get("log_tail"), str):
        part["log_tail"] = cut_tail(part["log_tail"], MAX_LOG_TAIL_BYTES)[0]
    turns = part.get("turns")
    if isinstance(turns, list):
        part["turns"] = [_scrub_turn(turn, scrub) for turn in turns]
    return part


def _scrub_turn(turn: Any, scrub) -> Any:
    if not isinstance(turn, Mapping):
        return turn
    copied = dict(turn)
    messages = copied.get("messages")
    if isinstance(messages, list):
        copied["messages"] = [
            {**message, "content": scrub(message["content"])}
            if isinstance(message, Mapping) and isinstance(message.get("content"), str)
            else message
            for message in messages
        ]
    return copied


def replace_nul_text(value: Any) -> Any:
    """Every string in ``value`` with NUL written as a literal `\\0`: the outbox refuses a whole op
    over one NUL (a model can emit one), which would cost every sample in it."""
    if isinstance(value, str):
        return value.replace(NUL, NUL_ESCAPE) if NUL in value else value
    if isinstance(value, Mapping):
        return {key: replace_nul_text(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_nul_text(item) for item in value]
    return value


def split_log(part: dict) -> str | None:
    """Take the full log off ``part`` (``log_text``, or ``log`` given as text): sets ``log_tail``
    when the caller set none and returns the log to bundle, capped at 1 MiB keeping the tail."""
    text = part.pop("log_text", None)
    if isinstance(part.get("log"), str):
        text = part.pop("log")
    if not isinstance(text, str) or not text:
        return None
    if "log_tail" not in part:
        part["log_tail"] = cut_tail(text, MAX_LOG_TAIL_BYTES)[0]
    return text


def cap_error_message(part: dict) -> None:
    """One line, at most 1,024 characters (the contract's cap)."""
    message = part.get("error_message")
    if isinstance(message, str):
        line = " ".join(message.split())
        part["error_message"] = line[:MAX_ERROR_MESSAGE_CHARS]


def get_default_seal_step(part: Mapping[str, Any]) -> int | None:
    """The step a part counts toward when the caller names none: its consuming step, else its
    scheduled step."""
    for name in ("consumed_step", "scheduled_step"):
        value = part.get(name)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def measure_bytes(value: Any) -> int:
    """The JSON size of ``value`` (what the batch caps count)."""
    return len(json.dumps(value, default=str))
