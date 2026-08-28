"""THE wire format for py_analytics, declared exactly once.

Normative source: ``_contracts/07-tobe-canonical-contract.md`` (the spec),
``_contracts/06-vocabularies.md`` (every legal enum value) and
``_contracts/12-defect-register.md`` (why the ugly parts stay ugly).

This module is the **only** place the shape of an outgoing payload is
declared.  Objective **O1**: three divergent ``results-agg`` builders
(``analytics/engine.py``, ``utils/legacy_analytics_bridge.py``,
``analytics/analytics_publisher.py`` -- defect PY-3) collapse into one.

Four surfaces are covered:

======  ==================================  ==========================
Code    Surface                             Model
======  ==================================  ==========================
S1      ``results-agg`` Redis stream        :class:`AggregationResult`
S2      ``incident_res`` Redis stream       :class:`IncidentMessage`
S3      the per-frame return value          :class:`FrameResult`
S4      the ``stream_info`` input dict      :class:`StreamInfo`
======  ==================================  ==========================

Universal rules enforced here (contract Section 1):

1. snake_case everywhere except the four frozen camelCase fields
   (:data:`ALLOWED_CAMELCASE_FIELDS`).
2. Timestamps are RFC3339 with a ``Z`` suffix -- :func:`to_rfc3339z` --
   except ``stream_time``, which uses the media format
   :func:`to_stream_time`.
3. Validate before emitting.  The backend validates almost nothing.
4. Never emit an unknown enum value.  Every enum here is closed.
5. The root ``input_timestamp`` is always set (mitigates BE-5, where the
   backend otherwise falls back to Go map iteration order).
6. Numbers are numbers.  ``data`` is a float, ``count`` is an int, and a
   numeric *string* is rejected outright.
7. No ``None`` in place of a string -- emit ``""``.  The Go parser drops
   the whole message when a declared string arrives as ``null``.

Serialisation is deliberately not exposed here: payload dicts are built in
one place only, :mod:`matrice_analytics.engine.contract.emit`.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping
from datetime import datetime, timezone
from enum import Enum
from math import isfinite
from typing import Annotated, Any, Final, Literal, Union

from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

logger = logging.getLogger(__name__)

__all__ = [
    "ALLOWED_CAMELCASE_FIELDS",
    "AggType",
    "AggregationResult",
    "BoundingBox",
    "Category",
    "Detection",
    "FrameResult",
    "FrameSummaryEntry",
    "FrameTrackingStats",
    "GLOBAL_ZONE",
    "IDENTITY_SEPARATOR",
    "UNASSIGNED_ZONE",
    "Incident",
    "IncidentMessage",
    "IncidentStatus",
    "InputStreamEntry",
    "InputStreamInfo",
    "INTERNAL_SEVERITY_ALIASES",
    "MetricEntry",
    "RFC3339Z_FORMAT",
    "ResultValue",
    "ResultWrapper",
    "SEVERITY_RANK",
    "STREAM_TIME_FORMATS",
    "Severity",
    "StreamInfo",
    "StreamInfoError",
    "TrackingCount",
    "TrackingStats",
    "ZoneConfig",
    "derive_incident_status",
    "is_rfc3339z",
    "is_stream_time",
    "now_rfc3339z",
    "parse_agg_type",
    "parse_category",
    "parse_incident_category",
    "parse_rfc3339z",
    "parse_severity",
    "parse_stream_time",
    "to_rfc3339z",
    "to_stream_time",
    "zone_identity",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GLOBAL_ZONE: Final[str] = "global"
"""The single-bucket zone id.

Never ``"__global__"``: the sentinel becomes ``raw_analytics.zoneId``, so the
two spellings split an app's ClickHouse history into two unrelated series
(defect PY-6 / vocabulary divergence V2).
"""

UNASSIGNED_ZONE: Final[str] = "unassigned"
"""The bucket for detections that fall inside no configured zone.

Declared here, beside :data:`GLOBAL_ZONE`, because two Stage B primitives needed
it and defined it independently -- ``primitives/geometry.py`` and a hardcoded
literal in ``primitives/dwell.py``. Two spellings of a zone id silently split a
series in ClickHouse exactly the way ``"__global__"`` vs ``"global"`` does
(defect PY-6), so there is one definition.

The legacy engine had no such bucket: detections outside every zone were dropped
with no counter (defect PY-10), which is why nobody could tell a quiet camera
from a mis-drawn zone.
"""

IDENTITY_SEPARATOR: Final[str] = "."
"""The separator that splits a composite output key, e.g. ``per_zone.<zone>.count``."""


def zone_identity(zone_name: str) -> str:
    """The identity a zone is keyed by, everywhere. **This is the Q1 seam.**

    Backlog **Q1** (``05`` §8) asks whether the engine keeps name-as-identity for ML
    zones or introduces stable ids. Today the name *is* the identity: the fe-streaming
    payload keys geometry by the human-drawn name, so renaming ``"Polygon 1"`` in the UI
    changes ``raw_analytics.zoneId`` and orphans every row that came before -- the chart
    splits into two series with no link between them.

    Q1 does not block the geometry maths, so this builds against names as today. What it
    must not do is scatter that assumption: **every** place a zone name becomes an output
    key, a state key or an assignment bucket goes through this function. When Q1 lands,
    the body becomes a lookup of the stable id and the callers do not change.

    Grep for ``zone_identity`` to see the complete blast radius of that decision.

    It lives *here*, in the contract layer, rather than in ``primitives/geometry.py``
    where it was first written, because both the manifest and the primitives need it and
    ``manifest`` must not import ``primitives``. Duplicating the rule instead is precisely
    how two spellings of a zone id reach ClickHouse (defect **PY-6**) -- and it had already
    started: ``ZoneOccupancyConfig.output_names()`` declared ``per_zone.Gate 1.2.count``
    while the primitive published ``per_zone.Gate 1_2.count``, so the manifest's declared
    output never resolved.

    **The one transformation applied today** is that a dot becomes an underscore. Zone
    names are operator-drawn in a UI that accepts ``"Gate 1.2"``, and a dot inside a zone
    identity breaks the ``per_zone.<zone>.count`` key it is spliced into.

    Two names that collide under the substitution (``"Gate 1.2"`` and ``"Gate 1_2"`` on one
    camera) are rejected at setup, because silently merging two zones' counts into one
    series is worse than refusing to start.

    Args:
        zone_name: The zone name as drawn in the streaming UI, e.g. ``"Polygon 1"``.

    Returns:
        The identity to key by: the name, with any dot replaced by an underscore.
    """
    return zone_name.replace(IDENTITY_SEPARATOR, "_")


ALLOWED_CAMELCASE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "locationId",  # FROZEN-1, S1 envelope
        "imageUrl",  # FROZEN-3, S2 incidents[]
        "_eventType",  # backend SSE only, never produced here
        # FROZEN-6 -- the frame-address tuple, byte-identical across
        # be-analytics, be-media-server and fe-analytics.
        "rtp",
        "cameraId",
        "date",
        "hour",
    }
)
"""Every camelCase key that may legally appear on the wire.

Contract Section 6.  Any other camelCase field is a bug -- see
:func:`matrice_analytics.engine.contract.conformance.check_no_stray_camelcase`.
"""

RFC3339Z_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%SZ"
"""Second-precision RFC3339-with-``Z``, matching the contract's examples."""

STREAM_TIME_FORMATS: Final[tuple[str, ...]] = (
    "%Y-%m-%d-%H:%M:%S.%f UTC",
    "%Y-%m-%d-%H:%M:%S UTC",
)
"""``stream_time`` layouts, in the order the Go side tries them.

``be-analytics/internal/utils/frame_helper.go:56-75`` tries
``2006-01-02-15:04:05.000000`` then ``2006-01-02-15:04:05``.  This is *not*
RFC3339 (contract Section 3.3) -- do not "fix" it.
"""

_RFC3339Z_RE: Final[re.Pattern[str]] = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?Z$")


# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------


def _as_utc_datetime(value: datetime | int | float) -> datetime:
    """Coerce a datetime or epoch-seconds value to an aware UTC datetime."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            # Contract Section 1 rule 2: timestamps are UTC.  A naive datetime is
            # assumed UTC rather than silently taking the host's local zone,
            # which would mis-bucket every row (backend defect BE-6 makes this
            # invisible downstream).
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    if isinstance(value, bool):  # bool is an int subclass; never a timestamp.
        raise TypeError("timestamp must be a datetime, epoch seconds or a string")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    raise TypeError(f"timestamp must be a datetime, epoch seconds or a string, got {type(value).__name__}")


def _parse_rfc3339_any(text: str) -> datetime:
    """Parse RFC3339 allowing either ``Z`` or a numeric UTC offset."""
    candidate = text.strip()
    if not candidate:
        raise ValueError("empty timestamp is not RFC3339")
    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except ValueError as exc:  # pragma: no cover - message pass-through
        raise ValueError(f"{text!r} is not a parseable RFC3339 timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def to_rfc3339z(value: datetime | int | float | str) -> str:
    """Format any instant as RFC3339 UTC with a literal ``Z`` suffix.

    This is the only timestamp formatter for the contract, ``stream_time``
    excepted (:func:`to_stream_time`).

    Accepts a :class:`datetime` (naive is treated as UTC), epoch seconds, or
    an existing timestamp string.  Passing a string normalises the ``+00:00``
    offset form to ``Z`` -- every other timestamp in the system uses ``Z``
    and defect PY-16 exists precisely because one path did not.

    Args:
        value: The instant to format.

    Returns:
        e.g. ``"2026-03-16T00:05:00Z"``.

    Raises:
        TypeError: The value is not a datetime, number or string.
        ValueError: A string value does not parse as RFC3339.
    """
    if isinstance(value, str):
        return _parse_rfc3339_any(value).strftime(RFC3339Z_FORMAT)
    return _as_utc_datetime(value).strftime(RFC3339Z_FORMAT)


def now_rfc3339z() -> str:
    """Current UTC instant as RFC3339 with ``Z``."""
    return to_rfc3339z(datetime.now(tz=timezone.utc))


def parse_rfc3339z(text: str) -> datetime:
    """Parse a contract timestamp, requiring the ``Z`` suffix.

    Args:
        text: The wire value.

    Returns:
        An aware UTC datetime.

    Raises:
        ValueError: Not RFC3339, or RFC3339 with a numeric offset rather than
            ``Z``.  Both are contract violations (Section 1 rule 2); the
            backend would accept either and silently mis-bucket the row
            (BE-6).
    """
    if not isinstance(text, str) or not _RFC3339Z_RE.match(text.strip()):
        raise ValueError(f"{text!r} is not RFC3339 with a 'Z' suffix (expected e.g. '2026-03-16T00:05:00Z')")
    return _parse_rfc3339_any(text)


def is_rfc3339z(text: object) -> bool:
    """Whether ``text`` is a well-formed RFC3339-with-``Z`` timestamp."""
    try:
        parse_rfc3339z(text)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False
    return True


def to_stream_time(value: datetime | int | float) -> str:
    """Format ``stream_time`` in the media format -- *not* RFC3339.

    ``"YYYY-MM-DD-HH:mm:ss.ffffff UTC"``, e.g.
    ``"2026-03-10-15:30:45.123456 UTC"``.  Contract Section 3.3; the Go side
    parses it at ``be-analytics/internal/utils/frame_helper.go:56-75``.
    Emitting RFC3339 here loses the frame anchor.

    Args:
        value: The instant to format.

    Returns:
        The media-format timestamp string.
    """
    return _as_utc_datetime(value).strftime(STREAM_TIME_FORMATS[0])


def parse_stream_time(text: str) -> datetime:
    """Parse a ``stream_time`` value using the two accepted media layouts.

    Args:
        text: The wire value.

    Returns:
        An aware UTC datetime.

    Raises:
        ValueError: The value matches neither layout in
            :data:`STREAM_TIME_FORMATS`.
    """
    if isinstance(text, str):
        candidate = text.strip()
        for layout in STREAM_TIME_FORMATS:
            try:
                return datetime.strptime(candidate, layout).replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    raise ValueError(
        f"{text!r} is not a valid stream_time; expected the media format "
        f"'YYYY-MM-DD-HH:mm:ss.ffffff UTC' (contract Section 3.3), not RFC3339"
    )


def is_stream_time(text: object) -> bool:
    """Whether ``text`` is a well-formed ``stream_time`` value."""
    try:
        parse_stream_time(text)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False
    return True


# ---------------------------------------------------------------------------
# Enums and their parsers
#
# Every enum is closed (contract Section 1 rule 4).  Each parser raises a
# ValueError naming the legal replacement, because the single worst failure
# mode in this system is an unknown value being silently accepted.
# ---------------------------------------------------------------------------


class Category(str, Enum):
    """Analytics category for a metric or an incident.

    ``VOLUME`` / ``SAFETY`` / ``QUALITY`` only (vocabulary Section 1).

    ``IDENTITY`` and ``SPECIAL`` are py_analytics-internal *processor*
    categories with no backend meaning (divergence V7).  A metric tagged with
    one lands in ClickHouse as a literal string that no UI surface groups by,
    so they are rejected here rather than passed through.
    """

    VOLUME = "VOLUME"
    SAFETY = "SAFETY"
    QUALITY = "QUALITY"


class AggType(str, Enum):
    """How the backend collapses a metric across a rollup window.

    ``sum`` / ``mean`` / ``min`` / ``max`` / ``last``, matching the backend
    vocabulary at ``entities/raw_business_metrics_clickhouse.go:31-38``.

    Notably absent:

    * ``avg`` -- the backend spells it ``mean``.  py_analytics' current
      dispatch knows only ``avg`` and **falls back to ``sum``** for anything
      else (``analytics/base_processor.py:353-365``), so every manifest
      declaring ``mean`` publishes a *sum* of per-frame values today.  A
      60-second window at 25 fps can emit a "compliance percentage" of
      150,000.  That is defect PY-1, a live production bug, and it is the
      reason an unknown ``agg_type`` must raise rather than fall back.
    * ``median`` -- accepted by the backend but it silently returns the mean
      (BE-1, acknowledged in a code comment).  Declaring it would publish a
      value that does not mean what it says.
    """

    sum = "sum"
    mean = "mean"
    min = "min"
    max = "max"
    last = "last"


class Severity(str, Enum):
    """Incident severity, lowercase on the wire.

    Vocabulary Section 2.  ``significant`` is deliberately *not* a member:
    py_analytics uses it internally and it must never reach the wire
    (FROZEN-7).  The backend has no such level, does not validate severity,
    and would store the literal string -- which then sorts and scores as an
    unknown value.  Use :func:`parse_severity`, which maps it to ``high``.
    """

    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


SEVERITY_RANK: Final[dict[Severity, int]] = {
    Severity.info: 0,
    Severity.low: 1,
    Severity.medium: 2,
    Severity.high: 3,
    Severity.critical: 4,
}
"""Ascending severity order (BE ``service/incident_clickhouse_service.go:178``).

The backend does find-or-create with **up-only escalation** (contract Section
3.4): same severity is a no-op, de-escalation is not representable.  Emit on
transition only.
"""

INTERNAL_SEVERITY_ALIASES: Final[dict[str, Severity]] = {
    "significant": Severity.high,  # FROZEN-7
    "information": Severity.info,
    "informational": Severity.info,
    "none": Severity.info,
}
"""Internal / legacy spellings mapped onto wire values.

``significant`` is the load-bearing one (FROZEN-7,
``analytics/incident_lifecycle.py:39``).  ``information`` /
``informational`` are the extra spellings fe-analytics accepts
(``services/alertsService.ts:480``); normalising them here means the wire
only ever carries the canonical five.
"""


class IncidentStatus(str, Enum):
    """Incident status -- **derived by the backend, never sent**.

    ``resolved`` if ``end_time`` parses, else ``active``
    (``incident_clickhouse_service.go:245-248``).  Declared here so engine
    code can reason about lifecycle state, but a payload carrying a
    ``status`` field is a conformance error: sending it implies a control
    the producer does not have.
    """

    active = "active"
    resolved = "resolved"


def derive_incident_status(end_time: str) -> IncidentStatus:
    """Reproduce the backend's status derivation, for local reasoning only.

    Args:
        end_time: The incident's ``end_time`` wire value (``""`` while open).

    Returns:
        :attr:`IncidentStatus.resolved` when ``end_time`` parses as RFC3339,
        otherwise :attr:`IncidentStatus.active`.
    """
    return IncidentStatus.resolved if is_rfc3339z(end_time) else IncidentStatus.active


def parse_agg_type(value: object) -> AggType:
    """Coerce a manifest/legacy ``agg_type`` to a legal :class:`AggType`.

    Args:
        value: The declared aggregation type.

    Returns:
        The matching :class:`AggType`.

    Raises:
        ValueError: The value is not legal.  ``avg`` and ``median`` get a
            message naming ``mean`` as the replacement.  This must never
            degrade to a silent fallback -- that fallback is defect PY-1 and
            it is publishing wrong numbers in production right now.
    """
    if isinstance(value, AggType):
        return value
    if not isinstance(value, str):
        raise ValueError(f"agg_type must be a string, got {type(value).__name__}; legal values: {_legal(AggType)}")
    text = value.strip().lower()
    if text in AggType.__members__:
        return AggType(text)
    if text in {"avg", "average"}:
        raise ValueError(
            f"agg_type {value!r} is not legal -- use 'mean' instead. The backend "
            "vocabulary is 'mean'; py_analytics' old dispatch only knew 'avg' and "
            "silently summed everything else (PY-1). "
            f"Legal values: {_legal(AggType)}"
        )
    if text == "median":
        raise ValueError(
            f"agg_type {value!r} is not legal -- use 'mean' instead. The backend "
            "accepts 'median' but silently returns the mean (BE-1), so declaring it "
            "publishes a value that does not mean what it says. "
            f"Legal values: {_legal(AggType)}"
        )
    raise ValueError(
        f"agg_type {value!r} is not legal. An unrecognised agg_type is a "
        "manifest-load validation error, never a runtime fallback (PY-1). "
        f"Legal values: {_legal(AggType)}"
    )


def parse_category(value: object) -> Category:
    """Coerce a manifest/legacy category to a legal :class:`Category`.

    Args:
        value: The declared category (case-insensitive).

    Returns:
        The matching :class:`Category`.

    Raises:
        ValueError: The value is not legal.  ``IDENTITY`` and ``SPECIAL`` get
            a message explaining that they are processor-internal and have no
            backend meaning (divergence V7).
    """
    if isinstance(value, Category):
        return value
    if not isinstance(value, str):
        raise ValueError(f"category must be a string, got {type(value).__name__}; legal values: {_legal(Category)}")
    text = value.strip().upper()
    if text in Category.__members__:
        return Category(text)
    if text in {"IDENTITY", "SPECIAL"}:
        raise ValueError(
            f"category {value!r} is not legal on the wire -- it is a "
            "py_analytics-internal processor category with no backend meaning (V7). "
            "A metric tagged with it lands in ClickHouse as a literal string that no "
            f"UI surface groups by. Map it to one of: {_legal(Category)}"
        )
    raise ValueError(f"category {value!r} is not legal. Legal values: {_legal(Category)}")


def parse_incident_category(value: object) -> Union[Category, Literal[""]]:
    """Like :func:`parse_category` but also accepts ``""`` (untagged).

    The S2 envelope's ``category`` is optional and the backend's own
    vocabulary includes the empty string for untagged incidents
    (vocabulary Section 1).

    Args:
        value: The declared category, ``""`` or ``None``.

    Returns:
        A :class:`Category`, or ``""`` when untagged.

    Raises:
        ValueError: The value is a non-empty illegal category.
    """
    if value is None:
        return ""
    if isinstance(value, str) and not value.strip():
        return ""
    return parse_category(value)


def parse_severity(value: object) -> Severity:
    """Coerce any internal / manifest / legacy severity to a wire value.

    Handles the four spellings of the same ladder catalogued in vocabulary
    Section 2: manifests use ``HIGH``/``MEDIUM`` uppercase, the lifecycle
    state machine uses ``significant``, and fe-analytics accepts three
    spellings of "info".

    Args:
        value: The severity in any accepted spelling.

    Returns:
        The canonical lowercase :class:`Severity`.

    Raises:
        ValueError: The value maps to nothing legal.  Severity is *not*
            validated anywhere on ingest and an unknown string defaults the
            backend's escalation check to "escalation = true"
            (``incident_clickhouse_service.go:184``), so it must be caught
            here.
    """
    if isinstance(value, Severity):
        return value
    if not isinstance(value, str):
        raise ValueError(
            f"severity_level must be a string, got {type(value).__name__}; legal values: {_legal(Severity)}"
        )
    text = value.strip().lower()
    if text in Severity.__members__:
        return Severity(text)
    if text in INTERNAL_SEVERITY_ALIASES:
        # FROZEN-7: 'significant' is internal-only and is mapped, not passed
        # through.  The backend would store the literal string.
        return INTERNAL_SEVERITY_ALIASES[text]
    raise ValueError(
        f"severity_level {value!r} is not legal. Legal wire values: "
        f"{_legal(Severity)} (internal aliases: "
        f"{', '.join(sorted(INTERNAL_SEVERITY_ALIASES))})"
    )


def _legal(enum_cls: type[Enum]) -> str:
    """Render an enum's members as a stable, comma-separated list."""
    return ", ".join(repr(member.value) for member in enum_cls)


# ---------------------------------------------------------------------------
# Field-level validators shared by every model
# ---------------------------------------------------------------------------


def _none_to_empty(value: object) -> object:
    """Map ``None`` onto ``""`` for declared string fields.

    Contract Section 1 rule 7.  The Go parser rejects a ``null`` where a
    string is declared and **loses the whole message**, so a ``None`` slipping
    through is not a missing field -- it is a dropped payload.
    """
    return "" if value is None else value


def _reject_numeric_string(value: object) -> object:
    """Reject numeric strings and booleans where a number is declared.

    Contract Section 1 rule 6: ``data`` is a float, ``count`` is an int,
    never a numeric string.  Pydantic would happily coerce ``"3"`` to ``3``;
    the Go DTO would not, and the whole message unmarshals to nothing.
    """
    if isinstance(value, str):
        raise ValueError(
            f"expected a number, got the string {value!r}; numeric strings are rejected (contract Section 1 rule 6)"
        )
    if isinstance(value, bool):
        raise ValueError("expected a number, got a bool")
    return value


def _reject_non_finite(value: object) -> object:
    """Reject NaN and +/-Infinity before they can reach the transport.

    ``json.dumps`` serialises these as the bare tokens ``NaN``, ``Infinity``
    and ``-Infinity``, which are not valid JSON.  Go's ``encoding/json``
    refuses them, so the backend drops **the entire 60-second window**, not
    just the offending metric -- and nothing upstream reports an error.

    The trigger is ordinary arithmetic, not an exotic input: any rate or
    percentage computed as ``numerator / denominator`` produces NaN the
    moment the denominator is zero (an empty frame, a camera seeing nobody).
    A primitive is free to compute one; it must not be able to publish one.

    Found by the Stage A verification pass as finding F1.
    """
    if isinstance(value, float) and not isfinite(value):
        raise ValueError(
            f"non-finite number {value!r} cannot go on the wire: json.dumps emits "
            "the bare token NaN/Infinity, Go's encoding/json rejects it, and the "
            "backend loses the whole message. Guard the division that produced it "
            "-- a zero denominator usually means 'no data', which is 0.0 or a "
            "skipped metric, not NaN"
        )
    return value


def _wire_number(value: object) -> object:
    """Every numeric wire field passes through both guards."""
    return _reject_non_finite(_reject_numeric_string(value))


WireStr = Annotated[str, BeforeValidator(_none_to_empty)]
"""A string that is never ``None`` on the wire (Section 1 rule 7)."""

WireInt = Annotated[int, BeforeValidator(_wire_number)]
"""An integer that refuses numeric strings (Section 1 rule 6)."""

WireFloat = Annotated[float, BeforeValidator(_wire_number)]
"""A float that refuses numeric strings (Section 1 rule 6)."""

AggTypeField = Annotated[AggType, BeforeValidator(parse_agg_type)]
CategoryField = Annotated[Category, BeforeValidator(parse_category)]
IncidentCategoryField = Annotated[Union[Category, Literal[""]], BeforeValidator(parse_incident_category)]
SeverityField = Annotated[Severity, BeforeValidator(parse_severity)]


class _WireModel(BaseModel):
    """Base for every model that reaches the wire.

    ``extra="forbid"`` is the point: an undeclared field is how the three
    divergent builders of PY-3 drifted apart (one of them added
    ``inferencePipelineId`` and ``deployment_instance_id`` and omitted
    ``metrics`` entirely).  If a field is not in this module, it does not go
    out.

    Serialisation lives in :mod:`matrice_analytics.engine.contract.emit` --
    payload dicts are constructed in exactly one place.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
        validate_assignment=True,
        use_enum_values=False,
    )


# ---------------------------------------------------------------------------
# S1 -- results-agg
# ---------------------------------------------------------------------------


class MetricEntry(_WireModel):
    """One entry in ``results-agg.metrics[]``.

    Contract Section 2.3.  Lands in ClickHouse as a ``raw_business_metrics``
    row.
    """

    key: WireStr = Field(
        description=(
            "The metric namespace. Producer-defined and unvalidated anywhere "
            "downstream: a rename silently empties every chart and alert rule "
            "built on it (vocabulary Section 13). Treat as versioned."
        ),
    )
    data: WireFloat = Field(description="The metric value. A float, never a string.")
    agg_type: AggTypeField = Field(
        description="How the backend collapses this metric across a rollup window.",
    )
    category: CategoryField = Field(description="VOLUME, SAFETY or QUALITY.")
    zone: WireStr = Field(
        default=GLOBAL_ZONE,
        validation_alias=AliasChoices("zone", "zone_id"),
        description=(
            "Zone id. Emitted as 'zone', only ever 'zone' (PY-8). The Go DTO "
            "accepts both 'zone' and 'zone_id' with 'zone' winning "
            "(dtos/tracker_dtos.go:40-41); 'zone_id' is accepted on input for "
            "legacy callers but is never emitted."
        ),
    )

    @field_validator("key")
    @classmethod
    def _key_must_be_non_empty(cls, value: str) -> str:
        """A metric with no key is an unqueryable row nobody will ever notice."""
        if not value.strip():
            raise ValueError("metrics[].key must be non-empty")
        return value

    @field_validator("zone")
    @classmethod
    def _zone_must_be_non_empty(cls, value: str) -> str:
        """Reject the legacy ``"__global__"`` sentinel and empty zones (PY-6)."""
        if not value.strip():
            raise ValueError(f"metrics[].zone must be non-empty; use {GLOBAL_ZONE!r} for single-bucket apps")
        if value == "__global__":
            raise ValueError(
                "zone '__global__' is the legacy sentinel (PY-6); use 'global'. "
                "The two spellings split an app's ClickHouse history into two "
                "unrelated series."
            )
        return value


class TrackingCount(_WireModel):
    """``{"category": "person", "count": 3}`` -- one entry in a count list.

    ``category`` here is the **ML class name** (``person``, ``vehicle``, ...),
    not an analytics :class:`Category`.  Vocabulary Section 13: it is a free
    string with no enum.
    """

    category: WireStr = Field(description="ML class name, e.g. 'person'.")
    count: WireInt = Field(description="An int, never a numeric string.")


class TrackingStats(_WireModel):
    """The per-zone value of ``results-agg.tracking_stats`` (contract 2.2).

    All four count lists are always present -- **FROZEN-5**.
    ``current_new_counts`` and ``total_counts`` are ignored on the main
    ingestion path (``tracker_clickhouse_service.go:626-687`` reads only
    ``current_counts`` and ``total_current_counts``) but the instant-metric
    path and ``dataField`` resolution depend on them.  Do not "optimise" them
    away; declaring them with list defaults guarantees they serialise even
    when empty.

    **``current_counts`` means one thing here and another on the frame
    surface, and that is deliberate (BE-16).**  ``raw_analytics`` is a *delta
    plus level* schema: ``count`` is "how many arrived since the previous
    reading", ``totalCount`` is "how many were there at the reading", and the
    five-minute rollup is ``argMin(totalCount, t) + sum(count) -
    argMin(count, t)``
    (``10_aggregated_analytics_totals_schema.sql:7``).  On **this** class --
    S1, one row per 60-second window -- ``current_counts`` is therefore the
    window's **arrival delta**; a level there makes the rollup add up
    occupancy readings and publish several times the true footfall.  On
    :class:`FrameTrackingStats` it is the frame's level, because a frame has
    no interval to take a delta over and be-analytics reads it as
    ``total_count`` / ``category_total_count``, i.e. "how many objects right
    now" (``tracker_clickhouse_service.go:1097-1120``).
    :class:`~matrice_analytics.engine.runtime.window.ZoneCounters` builds both
    from the same four quantities.
    """

    input_timestamp: WireStr = Field(
        description="RFC3339 Z. Event time for this zone's counts.",
    )
    reset_timestamp: WireStr = Field(
        default="",
        description="RFC3339 Z. When this zone's cumulative counters last reset.",
    )
    current_counts: list[TrackingCount] = Field(
        default_factory=list,
        description=(
            "Feeds raw_analytics.count -- the primary series. On S1 (results-agg) "
            "this is the WINDOW'S ARRIVAL DELTA: unique objects first seen during "
            "the window, because the backend's rollup sums this column (BE-16). On "
            "S3 (FrameTrackingStats) it is the frame's level, which is what the "
            "instant-metric 'total_count' dataField reads. See the class docstring."
        ),
    )
    current_new_counts: list[TrackingCount] = Field(
        default_factory=list,
        description=(
            "New unique objects first seen in this window. FROZEN-5: ignored on "
            "the main path, read by the instant-metric formula path. On S1 this is "
            "the same quantity as current_counts under a second name -- a window "
            "IS its reporting interval, so 'new in this window' and 'the interval's "
            "arrival delta' are one number."
        ),
    )
    total_counts: list[TrackingCount] = Field(
        default_factory=list,
        description=(
            "Cumulative unique since process start. FROZEN-4: 'since last "
            "restart' -- the backend's totalCount rollup formula assumes the "
            "producer's counters reset on restart, so making this durable is a "
            "coordinated change, not a local one (D6). FROZEN-5: ignored on the "
            "main path."
        ),
    )
    total_current_counts: list[TrackingCount] = Field(
        default_factory=list,
        description=(
            "Occupancy carry: previous window's last-frame current + this "
            "window's new arrivals. Feeds raw_analytics.totalCount, the reading "
            "the rollup takes argMin() of -- which is why it has to INCLUDE this "
            "window's arrivals: the formula subtracts them back out again. PY-4: "
            "this is NOT a copy of current_counts -- the base-class version that "
            "set them equal produces wrong rollups."
        ),
    )

    @field_validator("input_timestamp")
    @classmethod
    def _input_timestamp_is_rfc3339z(cls, value: str) -> str:
        """An unparseable timestamp silently becomes "now" downstream (BE-6)."""
        if not is_rfc3339z(value):
            raise ValueError(
                f"tracking_stats.input_timestamp {value!r} must be RFC3339 with a "
                "'Z' suffix; the backend silently rewrites an unparseable "
                "timestamp to 'now' (BE-6)"
            )
        return value

    @field_validator("reset_timestamp")
    @classmethod
    def _reset_timestamp_is_rfc3339z_or_blank(cls, value: str) -> str:
        """``reset_timestamp`` is optional, but if present it must parse."""
        if value and not is_rfc3339z(value):
            raise ValueError(f"tracking_stats.reset_timestamp {value!r} must be RFC3339 with a 'Z' suffix, or ''")
        return value


class AggregationResult(_WireModel):
    """S1 -- the ``results-agg`` message (contract Section 2).

    Emitted once per 60-second window per camera via
    ``XADD results-agg {"data": <json>}``.

    Field order matches the worked example in contract Section 2.4 so that a
    serialised payload is byte-comparable with the spec.
    """

    camera_id: WireStr = Field(
        description=("Drives team resolution and zone lookup. Empty means the row is ingested with teamId=''."),
    )
    camera_name: WireStr
    app_deployment_id: WireStr = Field(
        description="Stored; not used for analytics filtering.",
    )
    app_id: WireStr = Field(
        description="The primary read-scope key for every dashboard query.",
    )
    camera_group: WireStr = Field(default="", description="'' if unknown.")
    location_id: WireStr = Field(
        default="",
        validation_alias=AliasChoices("location_id", "locationId"),
        serialization_alias="locationId",
        description=(
            "FROZEN-1. Emitted as camelCase 'locationId' in an otherwise "
            "snake_case payload (dtos/tracker_dtos.go:75, "
            "mappers/kafka_analytics_results_agg.go:17). Renaming it to "
            "'location_id' breaks ingestion SILENTLY -- the field arrives empty "
            "and every row gets _idLocation = ''."
        ),
    )
    location: WireStr = Field(
        default="",
        description=(
            "Location name. Backfilled server-side for analytics rows but NOT "
            "for business-metrics rows, so send it correctly."
        ),
    )
    application_name: WireStr
    application_key_name: WireStr
    application_version: WireStr
    input_timestamp: WireStr = Field(
        description=(
            "RFC3339 Z. ALWAYS set. Without it the backend falls back to 'the "
            "first zone's timestamp', where 'first' is Go map iteration order -- "
            "nondeterministic (BE-5)."
        ),
    )
    rtp_number: WireStr = Field(default="", description="Media anchor.")
    tracking_stats: dict[str, TrackingStats] = Field(
        default_factory=dict,
        description=(
            "FROZEN-2. Keyed by ZONE ID, never flat. The parser treats every "
            "top-level key as a zone id "
            "(mappers/kafka_analytics_results_agg.go:67). The flat form -- which "
            "the backend's own contract doc incorrectly shows -- creates zones "
            "named 'current_counts' and fails to unmarshal the entire message. "
            "Single-bucket apps use the literal key 'global' (PY-6)."
        ),
    )
    metrics: list[MetricEntry] = Field(default_factory=list)

    @field_validator("input_timestamp")
    @classmethod
    def _root_input_timestamp_required(cls, value: str) -> str:
        """BE-5 mitigation: the root ``input_timestamp`` is unconditional."""
        if not value:
            raise ValueError(
                "input_timestamp must always be set: without it the backend "
                "picks 'the first zone's timestamp' in Go map iteration order, "
                "which is nondeterministic (BE-5)"
            )
        if not is_rfc3339z(value):
            raise ValueError(
                f"input_timestamp {value!r} must be RFC3339 with a 'Z' suffix; an "
                "unparseable timestamp is silently rewritten to 'now' by the "
                "backend (BE-6)"
            )
        return value

    @field_validator("tracking_stats", mode="before")
    @classmethod
    def _zone_keys_are_zone_ids(cls, value: Any) -> Any:
        """Catch the flat form *before* type coercion (FROZEN-2).

        ``mode="before"`` matters: the flat form's keys would otherwise be
        coerced to :class:`TrackingStats` first and the caller would get
        ``tracking_stats.current_counts.input_timestamp: Field required``
        instead of an explanation.
        """
        if not isinstance(value, Mapping):
            return value
        count_list_names = {
            "current_counts",
            "current_new_counts",
            "total_counts",
            "total_current_counts",
            "input_timestamp",
            "reset_timestamp",
        }
        offending = sorted(count_list_names & set(value))
        if offending:
            raise ValueError(
                "tracking_stats must be keyed by zone id, not flat (FROZEN-2). "
                f"Found count-list name(s) {offending} used as zone keys; the Go "
                "parser would create zones with those names and fail to unmarshal "
                "the entire message."
            )
        for zone in value:
            if not zone.strip():
                raise ValueError("tracking_stats zone id must be non-empty")
            if zone == "__global__":
                raise ValueError("zone '__global__' is the legacy sentinel (PY-6); use 'global'")
        return value

    @model_validator(mode="after")
    def _blank_camera_name_when_equal_to_id(self) -> AggregationResult:
        """FROZEN-8 on S1, mirroring :class:`IncidentMessage`.

        The rule was only ever written on S2, so the same camera showed a blank
        name on its incidents and a raw ObjectID on its dashboard rows. It is the
        same defect on both surfaces -- ``stream_info.py:97-104`` names it: "the
        pipeline stamps ``camera_name`` with the camera's ObjectId when it does not
        know the name, and preferring the root would then publish that id as a
        display name on every dashboard".

        The id reaches here legitimately: ``StreamInfo.from_raw`` refuses a stream
        whose ``camera_name`` is empty, so ``backends.py`` must gap-fill it with the
        camera id to get an engine session at all. Blanking at the emit boundary --
        here -- is what lets that gap-fill stay while the wire stays honest. An
        empty name is a legal S1 value; see ``_S1_OPTIONAL_STRINGS``.
        """
        if self.camera_name and self.camera_name == self.camera_id:
            # validate_assignment is on, so write through __dict__ rather than
            # re-entering validation from inside the validator.
            self.__dict__["camera_name"] = ""
        return self


# ---------------------------------------------------------------------------
# S2 -- incident_res
# ---------------------------------------------------------------------------


class Incident(_WireModel):
    """One entry in ``incident_res.incidents[]`` (contract Section 3.2)."""

    incident_id: WireStr = Field(
        description=(
            "Stable across the incident's life. UUID4 -- must not reset on "
            "restart, because the backend does find-or-create on it."
        ),
    )
    incident_type: WireStr = Field(
        description="Free snake_case string; the UI Title-Cases it.",
    )
    severity_level: SeverityField = Field(
        description=(
            "Lowercase. FROZEN-7: the internal 'significant' maps to 'high' and "
            "must never reach the wire -- the backend has no such level, does "
            "not validate severity, and would store the literal string."
        ),
    )
    human_text: WireStr = Field(description="Becomes the alert name.")
    start_time: WireStr = Field(
        description="RFC3339 Z. Stable across updates for the same incident_id.",
    )
    end_time: WireStr = Field(
        default="",
        description=(
            "'' while open; RFC3339 Z to close. Status is DERIVED by the backend "
            "from this field, never sent. Nothing else closes an incident, and "
            "incidents are never auto-resolved on the alert side."
        ),
    )
    image_url: WireStr = Field(
        default="",
        validation_alias=AliasChoices("image_url", "imageUrl"),
        serialization_alias="imageUrl",
        description=(
            "FROZEN-3. camelCase, unlike every sibling field in the same struct "
            "(be-analytics/internal/dtos/incident_dtos.go:23). Renaming it loses "
            "the image."
        ),
    )

    @field_validator("incident_id", "incident_type", "human_text")
    @classmethod
    def _required_strings_non_empty(cls, value: str) -> str:
        """These three are required and nothing downstream checks them."""
        if not value.strip():
            raise ValueError("required incident field must be non-empty")
        return value

    @field_validator("start_time")
    @classmethod
    def _start_time_is_rfc3339z(cls, value: str) -> str:
        if not is_rfc3339z(value):
            raise ValueError(f"incidents[].start_time {value!r} must be RFC3339 with a 'Z' suffix")
        return value

    @field_validator("end_time")
    @classmethod
    def _end_time_is_rfc3339z_or_blank(cls, value: str) -> str:
        """``""`` means open; anything else must parse or the incident never closes."""
        if value and not is_rfc3339z(value):
            raise ValueError(f"incidents[].end_time {value!r} must be '' (open) or RFC3339 with a 'Z' suffix (close)")
        return value


class IncidentMessage(_WireModel):
    """S2 -- the ``incident_res`` message (contract Section 3).

    ``XADD incident_res {"data": <json>}``, emitted on a severity
    **transition**, never per frame.

    The field naming deliberately differs from S1: ``application_id`` rather
    than ``app_id``, ``location_name`` rather than ``location``.  Both are
    frozen -- they match a different Go DTO (``CameraEventIncoming``).
    """

    camera_id: WireStr
    camera_name: WireStr = Field(
        default="",
        description=(
            "FROZEN-8: blanked when it equals camera_id "
            "(utils/incident_res_format.py:203). Deliberate -- it prevents the "
            "UI showing a raw ObjectID as a camera name."
        ),
    )
    app_deployment_id: WireStr
    application_id: WireStr = Field(
        description="Note: 'application_id', NOT 'app_id' as in S1.",
    )
    application_name: WireStr = ""
    location_name: WireStr = Field(
        default="",
        description="Note: 'location_name', NOT 'location' as in S1.",
    )
    frame_id: WireStr = Field(default="", description="Legacy Redis frame key.")
    rtp_number: WireStr = Field(default="", description="Preferred media anchor.")
    stream_time: WireStr = Field(
        default="",
        description=(
            "Media format 'YYYY-MM-DD-HH:mm:ss.ffffff UTC' (contract Section 3.3), NOT RFC3339. Do not 'fix' it."
        ),
    )
    category: IncidentCategoryField = Field(
        default="",
        description="SAFETY, QUALITY, VOLUME or '' (untagged).",
    )
    incidents: list[Incident] = Field(
        default_factory=list,
        description="At least one entry; an empty list is a wasted message.",
    )

    @field_validator("camera_id", "app_deployment_id", "application_id")
    @classmethod
    def _required_ids_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required incident_res identity field must be non-empty")
        return value

    @field_validator("stream_time")
    @classmethod
    def _stream_time_is_media_format(cls, value: str) -> str:
        if value and not is_stream_time(value):
            raise ValueError(
                f"stream_time {value!r} must use the media format "
                "'YYYY-MM-DD-HH:mm:ss.ffffff UTC' (contract Section 3.3), not "
                "RFC3339"
            )
        return value

    @model_validator(mode="after")
    def _blank_camera_name_when_equal_to_id(self) -> IncidentMessage:
        """FROZEN-8 -- enforce structurally so no caller can forget.

        ``camera_name`` is blanked when it equals ``camera_id`` so the UI never
        renders a raw ObjectID as a camera name
        (``incident_res_format.py:203``, ``engine_session.py:377``).
        """
        if self.camera_name and self.camera_name == self.camera_id:
            # validate_assignment is on, so write through __dict__ rather than
            # re-entering validation from inside the validator.
            self.__dict__["camera_name"] = ""
        return self


# ---------------------------------------------------------------------------
# S3 -- the per-frame return value
# ---------------------------------------------------------------------------


class BoundingBox(_WireModel):
    """A **normalized 0-1** bounding box.

    Contract Section 4, "Coordinate space": normalized 0-1, always, no
    exceptions.  The consumers cannot be fixed from here (D5) -- fe-streaming
    *guesses* between normalized, model and source space per detection with a
    one-sided guard that can apply two different mappings inside one frame
    (BE-10), and be-media-server's MPR1 ingest assumes a hardcoded 640x640
    (BE-12).  Emitting anything but 0-1 feeds both bugs; the range check here
    makes the classic 1920x error impossible to ship.
    """

    xmin: WireFloat
    ymin: WireFloat
    xmax: WireFloat
    ymax: WireFloat

    @model_validator(mode="after")
    def _normalized_and_ordered(self) -> BoundingBox:
        for name in ("xmin", "ymin", "xmax", "ymax"):
            value = getattr(self, name)
            if not -1e-6 <= value <= 1.0 + 1e-6:
                raise ValueError(
                    f"bounding_box.{name}={value} is outside 0-1. Bounding boxes "
                    "are normalized 0-1, always (contract Section 4). A "
                    "pixel-space box is silently mis-rendered by fe-streaming "
                    "(BE-10) and wraps to garbage in MPR1 storage (BE-12)."
                )
        if self.xmax < self.xmin or self.ymax < self.ymin:
            raise ValueError(
                "bounding_box is inverted (xmax < xmin or ymax < ymin); "
                "fe-streaming skips it and be-media-server stores garbage"
            )
        return self


class WireSegmentationMask(_WireModel):
    """A detection's mask on the wire, RLE-encoded (contract ``04`` §5.1).

    Deliberately narrow: the only shape this engine ever emits or decodes, matching
    :func:`~matrice_analytics.engine.primitives.segmentation_area.decode_simple_rle_area`. A
    detection whose mask came in as a polygon or a precomputed area (no ``rle`` string) never
    gets a wire ``segmentation`` -- this engine does not rasterize/encode one for the wire
    (no numpy/cv2, **PY-20**), so there is nothing ready-to-emit to put here.
    """

    encoding: WireStr = Field(description="Always 'simple_rle', the only encoding decoded.")
    counts: WireStr = Field(description="Base64 simple_rle run lengths, byte for byte as sent.")
    size: tuple[int, int] = Field(
        description="[height, width] of the mask's own array in model input space -- the "
        "coverage fraction's denominator."
    )


class Detection(_WireModel):
    """One detection inside a zone's frame-path ``tracking_stats``.

    ``confidence`` is required on purpose: be-media-server rewrites a
    confidence of 0 with a non-empty category to 1.0 (BE-12), so an omitted
    field is indistinguishable from full confidence in stored playback.
    """

    category: WireStr = Field(description="ML class name; the overlay label.")
    confidence: WireFloat = Field(description="0-1.")
    bounding_box: BoundingBox = Field(description="Normalized 0-1.")
    track_id: int | None = Field(
        default=None,
        description="Stable per-object tracker id; omitted from the payload when unknown.",
    )
    segmentation: WireSegmentationMask | None = Field(
        default=None,
        description=(
            "This detection's mask, RLE-encoded, when the producer sent one as a ready-to-emit "
            "encoding. Absent for a detector-only stream and for a polygon/area-only mask -- "
            "never a decoded polygon or pixel array (contract 04 §5.1)."
        ),
    )

    @field_validator("confidence")
    @classmethod
    def _confidence_in_range(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"detection confidence {value} is outside 0-1")
        return value


class FrameTrackingStats(TrackingStats):
    """The frame-path ``tracking_stats``, i.e. S1's plus display fields.

    **This subclass is the fix for PY-2**, the single most important
    correction on the frame surface.  Today the frame-path ``TrackingStats``
    carries only ``human_text`` and ``detections``
    (``analytics/schemas.py:280-289``), so be-analytics' instant-metric
    extractor -- whose ``hasTrackingStats`` tests only the four count lists
    (``tracker_clickhouse_service.go:1049-1054``) -- finds nothing on all
    seven of its probe paths and **every instant metric evaluates against
    zero**.  It also empties fe-streaming's live incident panel and degrades
    the live counter to "number of boxes drawn".

    Inheriting from :class:`TrackingStats` means the count lists cannot be
    dropped from this surface again.

    **One field is read differently here (BE-16).**  ``current_counts`` on this
    surface is the frame's **level** -- how many objects are in view right now.
    be-analytics resolves its ``total_count`` and ``category_total_count``
    instant-metric dataFields from it
    (``tracker_clickhouse_service.go:1097-1120``), so an arrival delta here
    would make every occupancy alert rule read approximately zero.  The parent
    class's ``current_counts`` -- S1, once per window -- is the arrival delta
    instead, because it lands in ``raw_analytics.count`` and the backend sums
    that column.  Same name, two surfaces, two consumers, two readings; see
    :class:`~matrice_analytics.engine.runtime.window.ZoneCounters`, which
    builds both.
    """

    detections: list[Detection] = Field(
        default_factory=list,
        description=(
            "The app-filtered detections for this zone. be-media-server's MPR1 "
            "storage reads ONLY this list (prediction_service.go:1053-1057). "
            "Emit each detection exactly once -- fe-streaming dedupes by bbox "
            "string key because duplicates used to arrive here and in a "
            "top-level detections array, and that dedupe collapses two genuine "
            "objects at identical coordinates."
        ),
    )
    human_text: WireStr = Field(default="", description="Display string, e.g. '3 people'.")


class FrameSummaryEntry(_WireModel):
    """One zone's entry in ``agg_summary`` (contract Section 4).

    ``agg_summary`` is keyed by **zone**, consistently.  Today the key is
    ``"<int>"``, ``"None"``, ``"current_frame"`` or a zone name depending on
    which file you land in (PY-5); four consumers cope four different ways
    and three break on multi-zone payloads.  Zone-keying matches S1 and is the
    only form that works for multi-zone apps -- but it is a **visible
    behaviour change for three consumers and must be announced, not slipped
    in**.
    """

    tracking_stats: FrameTrackingStats
    business_analytics: dict[str, Any] = Field(default_factory=dict)
    alerts: list[dict[str, Any]] = Field(default_factory=list)
    incidents: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Per-zone incident snapshot for fe-streaming's live panel. "
            "Authoritative incident delivery is S2 (incident_res); this is a "
            "display echo."
        ),
    )


class InputStreamInfo(_WireModel):
    """``input_streams[].input_stream`` -- the pipeline's stream metadata echo."""

    original_fps: WireFloat = 0.0


class InputStreamEntry(_WireModel):
    """Wrapper preserving the pipeline's ``input_streams`` shape."""

    input_stream: InputStreamInfo = Field(default_factory=InputStreamInfo)


class ResultValue(_WireModel):
    """``result.value`` -- streams plus the zone-keyed summary."""

    input_streams: list[InputStreamEntry] = Field(default_factory=list)
    agg_summary: dict[str, FrameSummaryEntry] = Field(default_factory=dict)


class ResultWrapper(_WireModel):
    """``result`` -- the pipeline's envelope around :class:`ResultValue`."""

    value: ResultValue = Field(default_factory=ResultValue)


class FrameResult(_WireModel):
    """S3 -- the per-frame **return value** (contract Section 4).

    py_analytics does *not* write this stream.  It returns a dict and a worker
    outside this workspace publishes it to
    ``<cameraId>_<appDeploymentId>_output_topic``.  We own exactly two keys:
    ``agg_summary`` and the detections inside it.  Everything else on that
    wire -- ``frame_id``, ``rtp_timestamp``, ``metadata.input_size`` -- is
    stamped by the pipeline and cannot be changed from here (backlog Q5).

    ``agg_summary`` appears twice, nested under ``result.value`` and hoisted
    to the top level, because consumers probe both paths
    (be-analytics tries seven).  The two are guaranteed identical by
    :meth:`_hoisted_matches_nested`.
    """

    result: ResultWrapper = Field(default_factory=ResultWrapper)
    agg_summary: dict[str, FrameSummaryEntry] = Field(
        default_factory=dict,
        description="Hoisted copy of result.value.agg_summary; consumers probe both.",
    )

    @model_validator(mode="after")
    def _hoisted_matches_nested(self) -> FrameResult:
        """The hoisted and nested copies must never diverge."""
        nested = self.result.value.agg_summary
        if set(nested) != set(self.agg_summary):
            raise ValueError(
                "FrameResult.agg_summary must be the same zone set as "
                f"result.value.agg_summary; got {sorted(self.agg_summary)} vs "
                f"{sorted(nested)}"
            )
        return self


# ---------------------------------------------------------------------------
# S4 -- the typed input contract
# ---------------------------------------------------------------------------


class StreamInfoError(ValueError):
    """A required ``stream_info`` field is missing or unusable.

    Contract Section 5: *a missing required field is a startup error, not a
    silent default*.  Today an absent ``resolution`` silently disables zone
    processing, which presents to an operator as "the numbers are wrong"
    rather than "the config is broken".
    """

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("stream_info is not usable:\n  - " + "\n  - ".join(self.problems))


class ZoneConfig(BaseModel):
    """Normalized 0-1 geometry: named lines and polygons.

    **One** ``ZoneConfig``, one convention (PY-7).  Two classes with the same
    name in the same package used opposite units -- ``analytics/schemas.py``
    normalized, ``post_processing/core/config.py`` pixels -- which is the most
    likely source of a silent 1920x error during migration.  Coordinates are
    normalized here; pixels are derived internally by whatever needs them,
    using :attr:`StreamInfo.resolution`.
    """

    model_config = ConfigDict(extra="ignore")

    lines: dict[str, list[float] | list[list[float]]] = Field(
        default_factory=dict,
        description="Named lines: [x, y] or [[x1,y1],[x2,y2]] segment endpoints.",
    )
    zones: dict[str, list[list[float]]] = Field(
        default_factory=dict,
        description="Named polygons as lists of [x, y] vertices.",
    )

    @model_validator(mode="after")
    def _coordinates_are_normalized(self) -> ZoneConfig:
        def check(name: str, coords: Any) -> None:
            if isinstance(coords, (int, float)) and not isinstance(coords, bool):
                if not -1e-6 <= float(coords) <= 1.0 + 1e-6:
                    raise ValueError(
                        f"zone_config {name} coordinate {coords} is outside 0-1. "
                        "ZoneConfig is normalized 0-1; pixels are derived "
                        "internally from StreamInfo.resolution (PY-7)."
                    )
                return
            if isinstance(coords, (list, tuple)):
                for item in coords:
                    check(name, item)

        for line_name, line in self.lines.items():
            check(f"lines[{line_name!r}]", line)
        for zone_name, polygon in self.zones.items():
            check(f"zones[{zone_name!r}]", polygon)
            if len(polygon) < 3:
                raise ValueError(
                    f"zone_config zones[{zone_name!r}] has {len(polygon)} vertices; a polygon needs at least 3"
                )
        return self


class StreamInfo(BaseModel):
    """S4 -- the typed ``stream_info`` input (contract Section 5).

    **Not owned by py_analytics** -- it arrives as an untyped dict from the
    inference worker and must be parsed defensively.  Today
    ``engine_session.py:263-389`` reverse-engineers it across five nested
    lookup paths in two casings; that function is the de-facto input contract.
    This model replaces it with an explicit schema and
    :meth:`from_raw`, whose fallbacks are logged.

    ``extra="ignore"``: the worker sends more than we need, and rejecting the
    extras would break every deployment.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    # --- Identity ---
    camera_id: WireStr
    camera_name: WireStr
    camera_group: WireStr = Field(default="", description="'' if unknown.")

    app_id: WireStr
    app_deployment_id: WireStr
    application_name: WireStr
    application_key_name: WireStr
    application_version: WireStr

    # --- Location (emitted as camelCase locationId on S1 -- FROZEN-1) ---
    location_id: WireStr = Field(
        default="",
        validation_alias=AliasChoices("location_id", "locationId"),
        serialization_alias="locationId",
        description="FROZEN-1: reaches the wire as 'locationId'.",
    )
    location: WireStr = ""

    # --- Timing and geometry ---
    original_fps: WireFloat = Field(
        default=0.0,
        description=(
            "The producer's declared source rate, or 0.0 when it does not know. "
            "METADATA ONLY: no primitive divides by it -- every duration in the engine "
            "comes from frame_ts deltas (PY-13). It reaches the wire in the S3 "
            "input_streams echo, whose own model has always defaulted it to 0.0."
        ),
    )
    resolution: tuple[int, int] = Field(
        default=(0, 0),
        description=(
            "[width, height] in pixels. Required when zones are configured: "
            "normalized-to-pixel conversion needs it, and zone processing must "
            "fail loudly without it rather than silently skipping."
        ),
    )

    # --- Media anchoring ---
    rtp_number: WireStr = ""
    stream_time: WireStr = Field(
        default="",
        description="Media format, contract Section 3.3.",
    )
    frame_id: WireStr = ""

    zone_config: ZoneConfig | None = None

    @field_validator("camera_id", "app_id", "app_deployment_id")
    @classmethod
    def _identity_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "stream_info identity field must be non-empty; an empty camera_id "
                "means the row is ingested with teamId='' and is invisible to "
                "every dashboard"
            )
        return value

    @field_validator("original_fps")
    @classmethod
    def _fps_not_negative(cls, value: float) -> float:
        """Zero means "the producer does not know"; only a negative rate is a parse error.

        This rejected ``0`` until INF-2606, on the stated grounds that "window and dwell
        maths divide by it". Nothing does -- ``grep`` finds no ``/ fps`` anywhere in
        ``engine/`` outside the synthetic ``migration/harness.py``, because **PY-13**
        moved every duration onto ``frame_ts`` deltas. The stale claim had a cost: it is
        quoted verbatim in py_inference's ``_original_fps_for`` as the reason that node
        withholds the field rather than send a rate it cannot vouch for, and the refusal
        that followed took every camera on an affected node off the air (INF-2606 #2).
        """
        if value < 0:
            raise ValueError(f"original_fps must not be negative, got {value}; zero means unknown")
        return value

    @model_validator(mode="after")
    def _resolution_required_when_zoned(self) -> StreamInfo:
        """Zone processing must fail loudly without a resolution (Section 5)."""
        if self.zone_config is not None and self.zone_config.zones:
            width, height = self.resolution
            if width <= 0 or height <= 0:
                raise ValueError(
                    f"resolution {list(self.resolution)} is required when "
                    f"zone_config declares zones ({sorted(self.zone_config.zones)}); "
                    "normalized-to-pixel conversion needs it. An absent resolution "
                    "must fail loudly, not silently disable zone processing."
                )
        return self

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any] | None) -> StreamInfo:
        """Parse the untyped worker dict, with explicit, logged fallbacks.

        Flattens the nested shapes the worker actually sends
        (``camera_info{...}``, ``input_settings{original_fps,...}``,
        ``stream_resolution{width,height}``) and accepts the camelCase
        spellings seen in the wild.

        Args:
            raw: The ``stream_info`` dict handed to ``process_frame``.

        Returns:
            A validated :class:`StreamInfo`.

        Raises:
            StreamInfoError: One or more required fields are missing or
                unusable.  Deliberately loud: contract Section 5.
        """
        if raw is None:
            raise StreamInfoError(["stream_info is None"])
        if not isinstance(raw, Mapping):
            raise StreamInfoError([f"stream_info must be a mapping, got {type(raw).__name__}"])

        nested: list[Mapping[str, Any]] = [raw]
        for container in ("camera_info", "cameraInfo", "input_settings", "inputSettings"):
            value = raw.get(container)
            if isinstance(value, Mapping):
                nested.append(value)

        def lookup(*names: str) -> Any:
            for scope_index, scope in enumerate(nested):
                for name in names:
                    if name in scope and scope[name] is not None:
                        if scope_index:
                            logger.debug(
                                "stream_info: %r resolved from nested scope #%d",
                                name,
                                scope_index,
                            )
                        return scope[name]
            return None

        fields: dict[str, Any] = {
            "camera_id": lookup("camera_id", "cameraId"),
            "camera_name": lookup("camera_name", "cameraName"),
            "camera_group": lookup("camera_group", "cameraGroup"),
            "app_id": lookup("app_id", "appId", "application_id", "applicationId"),
            "app_deployment_id": lookup("app_deployment_id", "appDeploymentId"),
            "application_name": lookup("application_name", "applicationName"),
            "application_key_name": lookup("application_key_name", "applicationKeyName"),
            "application_version": lookup("application_version", "applicationVersion"),
            "location_id": lookup("location_id", "locationId"),
            "location": lookup("location", "location_name", "locationName"),
            "original_fps": lookup("original_fps", "originalFps", "fps"),
            "rtp_number": lookup("rtp_number", "rtpNumber"),
            "stream_time": lookup("stream_time", "streamTime"),
            "frame_id": lookup("frame_id", "frameId"),
            "zone_config": lookup("zone_config", "zoneConfig"),
        }

        resolution = lookup("resolution", "stream_resolution", "streamResolution")
        if isinstance(resolution, Mapping):
            resolution = [resolution.get("width", 0), resolution.get("height", 0)]
        if isinstance(resolution, (list, tuple)) and len(resolution) == 2:
            fields["resolution"] = (int(resolution[0] or 0), int(resolution[1] or 0))
        elif resolution is not None:
            logger.warning(
                "stream_info: ignoring unusable resolution %r; expected [w, h]",
                resolution,
            )

        # rtp_number is coerced to str by the worker in some paths and left an
        # int in others; the wire declares a string (Section 1 rule 7).
        if fields["rtp_number"] is not None and not isinstance(fields["rtp_number"], str):
            fields["rtp_number"] = str(fields["rtp_number"])

        missing = [
            name
            for name in (
                "camera_id",
                "camera_name",
                "app_id",
                "app_deployment_id",
                "application_name",
                "application_key_name",
                "application_version",
            )
            if fields.get(name) in (None, "")
        ]
        if missing:
            raise StreamInfoError([f"required field {name!r} is missing" for name in missing])

        try:
            return cls.model_validate({k: v for k, v in fields.items() if v is not None})
        except ValueError as exc:
            raise StreamInfoError([str(exc)]) from exc
