from pydantic import BaseModel, Field, PrivateAttr, ValidationError, model_validator, field_validator
from typing import Any, Optional, Dict, Literal, List, Union
from datetime import datetime, timezone
from dataclasses import dataclass, field


class _Base(BaseModel):
    model_config = dict(extra="forbid", validate_default=True)


class Attachment(BaseModel):
    type: Literal["code", "text", "image", "iframe"]
    value: str  # URL, raw code, etc.
    name: Optional[str] = None  # e.g. "Generated SQL"
    role: Optional[Literal["input", "output", "context"]] = None
    language: Optional[str] = None  # for code snippets

    @model_validator(mode="after")
    def _require_value(self):
        if not self.value:
            raise ValueError("value must be non-empty.")
        return self


class TrackEvent(_Base):
    event_id: Optional[str] = None
    user_id: str
    event: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0)
    )
    attachments: Optional[List[Attachment]] = None

    @field_validator("user_id", "event")
    def _non_empty(cls, v, info):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            raise ValueError(f"'{info.field_name}' must be a non-empty string.")
        return v


class AIData(_Base):
    model: Optional[str]
    input: Optional[str]
    output: Optional[str]
    convo_id: Optional[str]

    @model_validator(mode="after")
    def _require_input_or_output(self):
        if not (self.input or self.output):
            raise ValueError("Either 'input' or 'output' must be non-empty.")
        return self


class TrackAIEvent(_Base):
    event_id: Optional[str] = None
    user_id: str
    event: str
    ai_data: AIData
    properties: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )
    attachments: Optional[List[Attachment]] = None

    # Ensure user_id and event are non-empty strings
    @field_validator("user_id", "event")
    def _non_empty(cls, v, info):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            raise ValueError(f"'{info.field_name}' must be a non-empty string.")
        return v

    # No need to duplicate input/output check here; AIData already enforces it
    # but keep method to return values unchanged so that pydantic doesn't complain about unused return


# --- Signal Tracking Models --- #


class BaseSignal(_Base):
    """Base model for signal events, containing common fields."""

    event_id: str
    signal_name: str
    timestamp: datetime = Field(
        # Return a datetime object; Pydantic's model_dump will handle serialization to string
        default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0)
    )
    properties: Dict[str, Any] = Field(default_factory=dict)
    attachment_id: Optional[str] = None
    sentiment: Optional[Literal["POSITIVE", "NEGATIVE"]] = None

    @field_validator("event_id", "signal_name")
    def _non_empty_strings(cls, v, info):
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"'{info.field_name}' must be a non-empty string.")
        return v


class DefaultSignal(BaseSignal):
    """Model for default signal events."""

    signal_type: Literal["default"] = "default"


class FeedbackSignal(BaseSignal):
    """Model for feedback signal events, requiring a comment."""

    signal_type: Literal["feedback"]

    @model_validator(mode="after")
    def _check_comment_in_properties(self):
        # Check properties safely after potential initialization
        props = self.properties
        if not isinstance(props, dict):
            raise ValueError("'properties' must be a dictionary for feedback signals.")
        comment = props.get("comment")
        if not comment or not isinstance(comment, str) or not comment.strip():
            raise ValueError(
                "'properties' must contain a non-empty string 'comment' for feedback signals."
            )
        return self


class EditSignal(BaseSignal):
    """Model for edit signal events, requiring after content."""

    signal_type: Literal["edit"]

    @model_validator(mode="after")
    def _check_after_in_properties(self):
        # Check properties safely after potential initialization
        props = self.properties
        if not isinstance(props, dict):
            raise ValueError("'properties' must be a dictionary for edit signals.")
        after = props.get("after")
        if not after or not isinstance(after, str) or not after.strip():
            raise ValueError(
                "'properties' must contain a non-empty string 'after' for edit signals."
            )
        return self


# Discriminated Union for Signal Events
# Pydantic will automatically use the 'signal_type' field to determine which model to use.
SignalEvent = Union[DefaultSignal, FeedbackSignal, EditSignal]

# --- End Signal Tracking Models --- #


class PartialAIData(_Base):
    """Looser version for incremental updates."""

    model: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    convo_id: Optional[str] = None


class PartialTrackAIEvent(_Base):
    """Accepts *any subset* of TrackAIEvent fields."""

    event_id: str  # always required for merge-key
    user_id: Optional[str] = None
    event: Optional[str] = None
    ai_data: Optional[PartialAIData] = None
    timestamp: Optional[datetime] = None
    properties: Optional[Dict[str, Any]] = None
    attachments: Optional[List[Attachment]] = None
    is_pending: Optional[bool] = True

    # The caller's timestamp exactly as given: an ISO-8601 string is the
    # event's start and goes on the wire unchanged (CONTRACT 9.1), not
    # re-serialized from the parsed datetime.
    _raw_timestamp: Optional[str] = PrivateAttr(default=None)
    # The event's start, stamped on the request when this update is sent.
    _start: Optional[str] = PrivateAttr(default=None)

    @model_validator(mode="wrap")
    @classmethod
    def _keep_raw_timestamp(cls, data: Any, handler: Any) -> "PartialTrackAIEvent":
        obj = handler(data)
        raw = data.get("timestamp") if isinstance(data, dict) else None
        if isinstance(raw, str) and raw.strip():
            obj._raw_timestamp = raw.strip()
        return obj


@dataclass
class FlushResult:
    """What an explicit ``flush()`` or ``shutdown()`` achieved (CONTRACT 1.2.1).

    Safe to ignore: the call never raises, and ignoring this changes nothing.
    Truthy when everything enqueued before the call was handed to ingest.
    A payload ingest rejected permanently (a non-429, non-408 4xx) counts as
    delivered: it was rejected, not lost in transit.
    """

    delivered: bool = True
    """Everything enqueued before the call was handed to ingest."""
    pending: int = 0
    """Payloads still queued for the background sender (flush deadline hit)."""
    dropped: int = 0
    """Payloads lost: cut off mid-flight at the deadline, out of retries, or
    left over when shutdown's deadline passed."""
    timed_out: bool = False
    """The deadline passed before everything was delivered."""

    def __bool__(self) -> bool:
        return self.delivered
