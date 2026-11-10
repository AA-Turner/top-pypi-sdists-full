"""Task: one thing a sample attempts, posed in a scenario: the outside values that are part of its identity."""

from __future__ import annotations

import math
import numbers
import re
from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    JsonValue,
    field_validator,
)

from ..records import Record
from .provenance import Sha256

#: The same cap as metric labels.
MAX_SCENARIO_KEYS = 32
MAX_SCENARIO_TEXT_CHARS = 256
MAX_TASK_KEY_CHARS = 512
#: Text over this goes to R2 whole, with a pointer + sha256 on the row (D2).
MAX_INLINE_TEXT_BYTES = 64 * 1024
#: No dots, so `--where scenario.<key>=...` parses with no quoting.
SCENARIO_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_\-]{0,63}$")


class ScenarioTime(BaseModel):
    """A point in time (an as-of date). A zone is required; identity reads it in UTC."""

    model_config = ConfigDict(extra="forbid")

    time: datetime

    @field_validator("time")
    @classmethod
    def _zoned(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("a scenario time needs a zone (an ISO-8601 offset or Z)")
        return value


class ScenarioFile(BaseModel):
    """Large outside data (a market snapshot). Identity reads the sha256 only: the uri may move."""

    model_config = ConfigDict(extra="forbid")

    sha256: Sha256
    uri: str | None = Field(default=None, max_length=2048)


#: A scenario value: number, text, bool, time, or file pointer. JSON times are `{"time": ...}`.
ScenarioValue = bool | int | float | str | ScenarioTime | ScenarioFile


def validate_scenario(values: dict[str, Any]) -> dict[str, Any]:
    """The shape guard every scenario passes: key names and count, value types, short text, finite numbers.

    A `datetime` becomes a time, and the JSON forms `{"time": ...}` / `{"sha256": ...}` their value types.
    """
    if not isinstance(values, dict):
        raise ValueError("a scenario is an object of named values")
    if len(values) > MAX_SCENARIO_KEYS:
        raise ValueError(f"a scenario may have at most {MAX_SCENARIO_KEYS} keys")
    return {key: _check_value(key, value) for key, value in values.items()}


def _check_value(key: Any, value: Any) -> ScenarioValue:
    if not isinstance(key, str) or not SCENARIO_KEY.match(key):
        raise ValueError(f"scenario key {key!r} must match {SCENARIO_KEY.pattern}")
    if isinstance(value, numbers.Integral) and not isinstance(value, (bool, int)):
        value = int(value)  # numpy and pandas integers
    elif isinstance(value, numbers.Real) and not isinstance(value, (bool, int, float)):
        value = float(value)
    if isinstance(value, datetime):
        value = ScenarioTime(time=value)
    elif isinstance(value, dict):
        value = (ScenarioTime if "time" in value else ScenarioFile).model_validate(value)
    if not isinstance(value, (bool, int, float, str, ScenarioTime, ScenarioFile)):
        raise ValueError(f"scenario value {key!r} must be a number, text, bool, time or file pointer")
    if isinstance(value, str) and len(value) > MAX_SCENARIO_TEXT_CHARS:
        raise ValueError(f"scenario value {key!r} is over {MAX_SCENARIO_TEXT_CHARS} characters")
    if isinstance(value, str) and not value.isascii():
        # A union member skips pydantic's own UTF-8 check, and uuid5 cannot hash a lone surrogate.
        value.encode("utf-8")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"scenario value {key!r} must be finite (identity cannot hash NaN or inf)")
    return value


#: Scenario values, checked wherever the type is used (a projection keeps the check).
Scenario = Annotated[dict[str, ScenarioValue], BeforeValidator(validate_scenario)]


def check_inline_text(value: str) -> str:
    """Text a row holds inline: at most 64 KiB of UTF-8, else the producer sends a blob."""
    if len(value.encode("utf-8")) > MAX_INLINE_TEXT_BYTES:
        raise ValueError("text is over 64 KiB: send it as a blob (BlobRef)")
    return value


InlineText = Annotated[str, AfterValidator(check_inline_text)]


class DatasetRow(BaseModel):
    """Where the task came from: a dataset file (by sha256, as the data catalog records it) and a row."""

    file_sha256: Sha256
    row: int | None = Field(default=None, ge=0)


class BlobRef(BaseModel):
    """Text over 64 KiB, stored whole in R2: the row keeps the pointer and the sha256."""

    sha256: Sha256
    size_bytes: int = Field(ge=0)
    #: Filled by the server once the blob's artifact row is known.
    artifact_id: UUID | None = None


class Task(Record):
    """One task instance: a key plus a scenario. Stored once per run per instance (`sample_tasks`)."""

    #: uuid5 of key + canonical scenario, derived by the server (`identity.derive_task_id`). Run-independent.
    task_id: UUID
    run_id: UUID | None = None
    task_key: str = Field(min_length=1, max_length=MAX_TASK_KEY_CHARS)
    scenario: Scenario = Field(default_factory=dict)
    prompt: InlineText | None = None
    prompt_blob: BlobRef | None = None
    dataset: DatasetRow | None = None
    #: The reference answer or grading spec (Miles `label`, verl `gts`, SkyRL's reward spec).
    label: JsonValue | None = None
    #: The full reward for this task, when it is not the plan's (`Plan.reward_max`).
    reward_max: float | None = None
