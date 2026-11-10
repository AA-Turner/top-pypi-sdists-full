"""Identity: the canonical scenario encoding and the task, sample and group ids derived from it (DESIGN.md §3.5).

Pure and stdlib-only past the value types, so the server, the SDK and a hand-written client all agree.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from datetime import datetime, timezone
from uuid import UUID, uuid5

from .task import ScenarioFile, ScenarioTime, validate_scenario

#: uuid5(NAMESPACE_URL, "https://prbe.ai/probe/samples/task"), fixed forever: every task id hangs off it.
TASK_NAMESPACE = UUID("7f5e102b-3691-5cc7-80e7-fb8243fe6665")


def encode_number(value: int | float) -> str:
    """Shortest round-trip form; an integral float is an int, so `1` and `1.0` encode alike."""
    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        raise ValueError("a scenario number must be finite")
    if value.is_integer():
        return str(int(value))
    mantissa, _, exponent = repr(value).partition("e")
    return f"{mantissa}e{int(exponent)}" if exponent else mantissa


def encode_time(value: datetime) -> str:
    """UTC `YYYY-MM-DDTHH:MM:SS[.ffffff]Z`; a naive time is refused (it names no instant)."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("a scenario time needs a zone")
    utc = value.astimezone(timezone.utc)
    text = (f"{utc.year:04d}-{utc.month:02d}-{utc.day:02d}"
            f"T{utc.hour:02d}:{utc.minute:02d}:{utc.second:02d}")
    return f"{text}.{utc.microsecond:06d}Z" if utc.microsecond else f"{text}Z"


def encode_value(value: object) -> str:
    """One scenario value, canonical. bool is tested before int: in Python a bool IS an int."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return encode_number(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, datetime):
        return '{"time":' + json.dumps(encode_time(value)) + "}"
    if isinstance(value, ScenarioTime):
        return '{"time":' + json.dumps(encode_time(value.time)) + "}"
    if isinstance(value, ScenarioFile):
        return '{"sha256":' + json.dumps(value.sha256.lower()) + "}"
    raise TypeError(f"not a scenario value: {type(value).__name__}")


def encode_scenario(scenario: Mapping[str, object]) -> str:
    """Compact JSON with sorted keys; times in UTC; numbers shortest with 1 == 1.0; files by sha256 only."""
    checked = validate_scenario(dict(scenario))
    body = ",".join(f"{json.dumps(key)}:{encode_value(checked[key])}" for key in sorted(checked))
    return "{" + body + "}"


def derive_task_id(task_key: str, scenario: Mapping[str, object]) -> UUID:
    """The task instance id: the same key and scenario give the same id in every run (arms, evals, teachers)."""
    return uuid5(TASK_NAMESPACE, task_key + encode_scenario(scenario))


def derive_sample_id(run_id: UUID, write_epoch: int, key: str) -> UUID:
    """One attempt in one write epoch: a retry lands on the same row, a resumed attempt never collides."""
    return uuid5(run_id, f"{write_epoch}:{key}")


def derive_attempt_id(run_id: UUID, write_epoch: int, attempt_key: str) -> UUID:
    """A live attempt's own row: its attempt parts are keyed by the attempt key, so it is that key's sample id."""
    return derive_sample_id(run_id, write_epoch, attempt_key)


def derive_group_id(run_id: UUID, write_epoch: int, group_key: str) -> UUID:
    """One task's attempts at one step, in its own namespace so a group never shares a sample's id."""
    return uuid5(uuid5(run_id, "groups"), f"{write_epoch}:{group_key}")
