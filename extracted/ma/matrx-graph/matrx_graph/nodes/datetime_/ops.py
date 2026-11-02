"""Datetime nodes: now, parse, format, add.

All values cross the node boundary as ISO-8601 strings. Native ``datetime``
objects don't round-trip through JSON without a custom encoder, and the
channel system is JSON-only by contract.

``datetime.now`` is declared NON_DETERMINISTIC + ``re_execute_on_resume=True``
— its whole purpose is to capture the current instant, so re-using a
cached value on resume would be the wrong answer.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


def _tz_facts(dt: datetime) -> tuple[bool, int | None]:
    """Whether ``dt`` carries a UTC offset, and that offset in seconds."""
    offset = dt.utcoffset()
    return (offset is not None, int(offset.total_seconds()) if offset is not None else None)


def _resolve_naive_as_utc(dt: datetime) -> tuple[datetime, bool]:
    """Resolve a parsed value to an UNAMBIGUOUS instant, UTC-assumed if naive.

    Returns ``(resolved, input_had_timezone)``.

    Python's ``datetime.timestamp()`` on a NAIVE value silently assumes the
    WORKER's local timezone, so the same workflow answered differently on
    different machines — a portability bug, not a display detail (Arman's
    ruling, 2026-08-21: "a workflow's answer must not depend on which box ran
    it"). A timezone-less input is now read as UTC.

    The ambiguity is still REPORTED rather than hidden: the caller emits
    ``has_timezone=False`` whenever the input text carried no offset, so a
    consumer can always tell an assumed UTC from a stated one.
    """
    if dt.tzinfo is not None and dt.utcoffset() is not None:
        return dt, True
    return dt.replace(tzinfo=UTC), False


# ---------------------------------------------------------------------------
# datetime.now
# ---------------------------------------------------------------------------


class NowInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NowConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timezone: Literal["utc", "local"] = Field(
        default="utc",
        description="'utc' returns tz-aware UTC; 'local' uses the worker's tz.",
    )


class NowOutput(KindModel, kind="datetime_snapshot"):
    iso: str = Field(description="Current instant as an ISO-8601 string.")
    unix_ms: int = Field(description="Current instant as Unix milliseconds.")
    unix_seconds: float = Field(description="Current instant as Unix seconds (fractional).")
    year: int = Field(description="Calendar year.")
    month: int = Field(description="Month, 1–12.")
    day: int = Field(description="Day of the month, 1–31.")
    hour: int = Field(description="Hour, 0–23.")
    minute: int = Field(description="Minute, 0–59.")
    second: int = Field(description="Second, 0–59.")
    weekday: int = Field(description="Day of the week — Monday=0 … Sunday=6.")


class DatetimeNowExecutor:
    """Capture the current instant as ISO string + unix timestamps."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="datetime.now",
        category=NodeCategory.DATA,
        display_name="Current Date & Time",
        description="Get the current date and time.",
        input_schema=NowInput,
        output_schema=NowOutput,
        config_schema=NowConfig,
        output_kind="datetime_snapshot",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        # Re-execute on resume — capturing "now" is the whole point.
        re_execute_on_resume=True,
        icon="clock",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: NowInput,
        config: NowConfig,
    ) -> NodeResult[NowOutput]:
        _ = ctx, inputs
        if config.timezone == "utc":
            dt = datetime.now(UTC)
        else:
            dt = datetime.now().astimezone()
        return success(
            NowOutput(
                iso=dt.isoformat(),
                unix_ms=int(dt.timestamp() * 1000),
                unix_seconds=dt.timestamp(),
                year=dt.year,
                month=dt.month,
                day=dt.day,
                hour=dt.hour,
                minute=dt.minute,
                second=dt.second,
                weekday=dt.weekday(),
            )
        )


# ---------------------------------------------------------------------------
# datetime.parse
# ---------------------------------------------------------------------------


class ParseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, description="Date/time string to parse.")


class ParseConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    format: str | None = Field(
        default=None,
        description=(
            "Optional ``strptime`` format. If omitted, attempts ISO 8601 via "
            "``fromisoformat`` which accepts most well-formed inputs."
        ),
    )


class ParseOutput(KindModel, kind="parsed_datetime"):
    """Success payload (Node Result System) — a parse failure is a node
    Failure (``code='parse_failed'``), never an ok=false payload. The old
    ``ok``/``error`` payload fields are gone."""

    iso: str = Field(description="The parsed datetime as ISO-8601.")
    unix_ms: int = Field(
        description=(
            "The parsed datetime as Unix milliseconds. Absolute only when "
            "``has_timezone`` is true — a naive input is interpreted in the "
            "worker's local timezone."
        )
    )
    source_text: str | None = Field(
        default=None, description="The string that was parsed, kept as provenance."
    )
    has_timezone: bool | None = Field(
        default=None, description="Whether the parsed value carried a UTC offset."
    )
    utc_offset_seconds: int | None = Field(
        default=None, description="That offset in seconds; null for a naive value."
    )


class DatetimeParseExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="datetime.parse",
        category=NodeCategory.DATA,
        display_name="Read a Date",
        description="Turn a written date or time into a standard format.",
        input_schema=ParseInput,
        output_schema=ParseOutput,
        config_schema=ParseConfig,
        input_kind="text",
        output_kind="parsed_datetime",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="calendar",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ParseInput,
        config: ParseConfig,
    ) -> NodeResult[ParseOutput]:
        _ = ctx
        try:
            if config.format:
                dt = datetime.strptime(inputs.text, config.format)
            else:
                dt = datetime.fromisoformat(inputs.text)
        except (ValueError, TypeError) as e:
            return failure("parse_failed", f"{type(e).__name__}: {e}")

        resolved, had_tz = _resolve_naive_as_utc(dt)
        _, offset_seconds = _tz_facts(resolved)
        return success(
            ParseOutput(
                iso=resolved.isoformat(),
                unix_ms=int(resolved.timestamp() * 1000),
                source_text=inputs.text,
                has_timezone=had_tz,
                utc_offset_seconds=offset_seconds,
            )
        )


# ---------------------------------------------------------------------------
# datetime.format
# ---------------------------------------------------------------------------


class FormatInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    iso: str = Field(min_length=1, description="ISO-8601 date/time string.")


class FormatConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="strftime format string.",
    )


class FormatOutput(KindModel, kind="formatted_datetime"):
    """Success payload (Node Result System) — bad ISO input / bad format
    string are node Failures (``parse_failed`` / ``format_failed``). The old
    ``ok``/``error`` payload fields are gone."""

    text: str = Field(
        description=(
            "The datetime rendered with the strftime format. Lossy by design — "
            "never re-parse it; use ``iso``."
        )
    )
    iso: str | None = Field(
        default=None,
        description="The instant it was rendered from, so the value stays sortable.",
    )
    format: str | None = Field(
        default=None, description="The strftime pattern used, so it can be re-rendered."
    )


class DatetimeFormatExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="datetime.format",
        category=NodeCategory.DATA,
        display_name="Format a Date",
        description="Show a date and time in the format you choose.",
        input_schema=FormatInput,
        output_schema=FormatOutput,
        config_schema=FormatConfig,
        output_kind="formatted_datetime",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="calendar-days",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: FormatInput,
        config: FormatConfig,
    ) -> NodeResult[FormatOutput]:
        _ = ctx
        try:
            dt = datetime.fromisoformat(inputs.iso)
        except (ValueError, TypeError) as e:
            return failure("parse_failed", f"invalid ISO date: {e}")

        try:
            return success(
                FormatOutput(
                    text=dt.strftime(config.format),
                    iso=dt.isoformat(),
                    format=config.format,
                )
            )
        except (ValueError, TypeError) as e:
            return failure("format_failed", f"bad format string: {e}")


# ---------------------------------------------------------------------------
# datetime.add
# ---------------------------------------------------------------------------


class AddInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    iso: str = Field(min_length=1, description="Starting ISO-8601 datetime.")


class AddConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    days: int = Field(default=0, description="Days to add (negative subtracts).")
    hours: int = Field(default=0, description="Hours to add (negative subtracts).")
    minutes: int = Field(default=0, description="Minutes to add (negative subtracts).")
    seconds: int = Field(default=0, description="Seconds to add (negative subtracts).")
    weeks: int = Field(default=0, description="Weeks to add (negative subtracts).")


class AddOutput(KindModel, kind="shifted_datetime"):
    iso: str = Field(description="The shifted datetime as an ISO-8601 string.")
    unix_ms: int = Field(
        description=(
            "The shifted datetime as Unix milliseconds. Absolute only when "
            "``has_timezone`` is true (same caveat as ``datetime.parse``)."
        )
    )
    source_iso: str | None = Field(
        default=None, description="The instant that was shifted, kept as provenance."
    )
    has_timezone: bool | None = Field(
        default=None, description="Whether the value carried a UTC offset."
    )
    utc_offset_seconds: int | None = Field(
        default=None, description="That offset in seconds; null for a naive value."
    )


class DatetimeAddExecutor:
    """Add a timedelta to an ISO datetime. Negative values allowed."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="datetime.add",
        category=NodeCategory.DATA,
        display_name="Add to a Date",
        description="Add or subtract days, hours, or minutes from a date.",
        input_schema=AddInput,
        output_schema=AddOutput,
        config_schema=AddConfig,
        output_kind="shifted_datetime",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="calendar-plus",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: AddInput,
        config: AddConfig,
    ) -> NodeResult[AddOutput]:
        _ = ctx
        try:
            dt = datetime.fromisoformat(inputs.iso)
        except (ValueError, TypeError) as e:
            return failure("parse_failed", f"invalid ISO date: {e}")

        delta = timedelta(
            days=config.days,
            hours=config.hours,
            minutes=config.minutes,
            seconds=config.seconds,
            weeks=config.weeks,
        )
        shifted = dt + delta
        resolved, had_tz = _resolve_naive_as_utc(shifted)
        _, offset_seconds = _tz_facts(resolved)
        return success(
            AddOutput(
                iso=resolved.isoformat(),
                unix_ms=int(resolved.timestamp() * 1000),
                source_iso=dt.isoformat(),
                has_timezone=had_tz,
                utc_offset_seconds=offset_seconds,
            )
        )
