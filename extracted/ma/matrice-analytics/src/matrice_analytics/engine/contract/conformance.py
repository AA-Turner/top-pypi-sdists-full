"""The six conformance checks from contract Section 7.

A payload conforms when:

1. It round-trips through ``ParseKafkaAnalyticsMessageFromJSON`` (S1) or
   unmarshals to ``CameraEventIncoming`` (S2) with no field loss --
   :func:`check_required_fields`.
2. Every enum value appears in ``06-vocabularies.md`` --
   :func:`check_enum_values`.
3. Every timestamp parses as RFC3339 -- except ``stream_time``, which parses
   as the media format -- :func:`check_timestamps`.
4. ``tracking_stats`` is zone-keyed and every zone value carries all four
   count lists -- :func:`check_tracking_stats_shape`.
5. No camelCase field outside the frozen four --
   :func:`check_no_stray_camelcase`.
6. At least one of ``tracking_stats`` / ``metrics`` is non-empty --
   :func:`check_payload_not_empty`.

These six are exactly what the auto-generated per-app tests assert
(objective **O5**), so every function here is importable, side-effect free,
and returns structured :class:`ConformanceError` records naming the offending
field rather than raising.  :func:`assert_conforms` is the raising wrapper
used on the emit path.

Everything operates on **plain payload dicts**, not models -- the checks have
to be able to police a dict produced anywhere, including one round-tripped
back from Redis or handed over by a test fixture.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from itertools import pairwise
from typing import Any, Callable, Final

from matrice_analytics.engine.contract.schemas import (
    ALLOWED_CAMELCASE_FIELDS,
    AggType,
    Category,
    Severity,
    is_rfc3339z,
    is_stream_time,
)

__all__ = [
    "CHECKS",
    "COUNT_LIST_FIELDS",
    "ConformanceError",
    "ConformanceViolation",
    "Surface",
    "assert_conforms",
    "check_enum_values",
    "check_no_stray_camelcase",
    "check_payload_not_empty",
    "check_required_fields",
    "check_timestamps",
    "check_tracking_stats_shape",
    "conformance_errors",
    "conforms",
]


class Surface(str, Enum):
    """The three outbound surfaces a payload can be validated against."""

    results_agg = "results-agg"
    """S1 -- the ``results-agg`` Redis stream."""

    incident_res = "incident_res"
    """S2 -- the ``incident_res`` Redis stream."""

    frame_result = "frame_result"
    """S3 -- the per-frame return value."""


COUNT_LIST_FIELDS: Final[tuple[str, ...]] = (
    "current_counts",
    "current_new_counts",
    "total_counts",
    "total_current_counts",
)
"""The four count lists, all of which must be present in every zone (FROZEN-5).

``current_new_counts`` and ``total_counts`` are ignored on the main ingestion
path but are read by the instant-metric formula path and ``dataField``
resolution.  Do not "optimise" them away.
"""

# ---------------------------------------------------------------------------
# Per-surface field tables
# ---------------------------------------------------------------------------

_S1_REQUIRED: Final[tuple[str, ...]] = (
    "camera_id",
    "app_id",
    "app_deployment_id",
    "application_name",
    "application_key_name",
    "application_version",
    "input_timestamp",
)

_S1_OPTIONAL_STRINGS: Final[tuple[str, ...]] = (
    # ``camera_name`` is a display string, not a query key. The "row nothing can
    # query" rationale below belongs to ``camera_id`` and ``app_id``; a blank name
    # costs a label on a chart, and the Go mapper copies the field verbatim with no
    # validation and no backfill (``kafka_analytics_results_agg.go``) -- unlike
    # ``Location``, which has ``backfillLocationName``. ``camera_group`` and
    # ``location`` are optional here for exactly the same reason.
    #
    # Requiring it non-empty is what forced the engine to publish the camera's
    # ObjectId as its name: S2's FROZEN-8 blanking had no S1 counterpart because a
    # blank would have raised here and lost the whole 60-second window -- strictly
    # worse than a wrong label. With this moved, ``AggregationResult`` can apply the
    # same blanking S2 has always had.
    #
    # Still type-checked: ``required=False`` rejects ``None`` and non-strings, so
    # Section 1 rule 7 (never a null where a string is declared) is untouched.
    "camera_name",
    "camera_group",
    "locationId",
    "location",
    "rtp_number",
)

_S1_WRONG_NAMES: Final[dict[str, str]] = {
    # FROZEN-1 -- the single most dangerous rename in the contract.
    "location_id": "locationId",
    # S2 spellings that must not leak onto S1.
    "application_id": "app_id",
    "location_name": "location",
    # PY-3: the third legacy builder added these and omitted metrics entirely.
    "inferencePipelineId": "(nothing -- do not emit)",
    "deployment_instance_id": "(nothing -- do not emit)",
}

_S2_REQUIRED: Final[tuple[str, ...]] = (
    "camera_id",
    "app_deployment_id",
    "application_id",
)

_S2_OPTIONAL_STRINGS: Final[tuple[str, ...]] = (
    "camera_name",
    "application_name",
    "location_name",
    "frame_id",
    "rtp_number",
    "stream_time",
    "category",
)

_S2_WRONG_NAMES: Final[dict[str, str]] = {
    # S1 spellings that must not leak onto S2 -- they match a different Go DTO.
    "app_id": "application_id",
    "location": "location_name",
    "locationId": "location_name",
}

_INCIDENT_REQUIRED: Final[tuple[str, ...]] = (
    "incident_id",
    "incident_type",
    "severity_level",
    "human_text",
    "start_time",
)
"""Required and non-empty. ``end_time`` is handled separately: it is
required-*present* but legitimately ``""`` while the incident is open."""

_INCIDENT_WRONG_NAMES: Final[dict[str, str]] = {
    "image_url": "imageUrl",  # FROZEN-3
    "imageURL": "imageUrl",
    "severity": "severity_level",
}

_METRIC_REQUIRED: Final[tuple[str, ...]] = ("key", "data", "agg_type", "category", "zone")


# ---------------------------------------------------------------------------
# Error records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ConformanceError:
    """A single named contract violation.

    Attributes:
        check: The check function that produced it, e.g.
            ``"check_required_fields"``.
        field: A dotted path to the offending field, e.g.
            ``"tracking_stats.global.total_counts"``.  Never empty -- the
            whole point is that the message names what is wrong.
        message: Human-readable explanation, citing the defect id where one
            applies.
        surface: The surface the payload was validated against.
    """

    check: str
    field: str
    message: str
    surface: str = ""

    def __str__(self) -> str:
        prefix = f"[{self.surface}] " if self.surface else ""
        return f"{prefix}{self.check}: {self.field}: {self.message}"


class ConformanceViolation(ValueError):  # noqa: N818 - a violation is what it reports
    """Raised by :func:`assert_conforms` when a payload does not conform.

    Attributes:
        surface: The surface validated against.
        errors: Every :class:`ConformanceError` found, not just the first --
            one malformed zone fails the whole message on the Go side (BE-7),
            so it is worth reporting everything at once.
    """

    def __init__(self, surface: Surface, errors: Sequence[ConformanceError]) -> None:
        self.surface = surface
        self.errors: list[ConformanceError] = list(errors)
        detail = "\n  - ".join(str(error) for error in self.errors)
        super().__init__(
            f"payload does not conform to the {surface.value} contract "
            f"({len(self.errors)} problem(s)):\n  - {detail}"
        )


@dataclass
class _Collector:
    """Accumulates errors for one check, so call sites stay readable."""

    check: str
    surface: Surface
    errors: list[ConformanceError] = field(default_factory=list)

    def add(self, path: str, message: str) -> None:
        self.errors.append(
            ConformanceError(
                check=self.check,
                field=path,
                message=message,
                surface=self.surface.value,
            )
        )


def _coerce_surface(surface: Surface | str) -> Surface:
    """Accept either the enum or its wire string."""
    if isinstance(surface, Surface):
        return surface
    try:
        return Surface(surface)
    except ValueError as exc:
        legal = ", ".join(repr(member.value) for member in Surface)
        raise ValueError(f"unknown surface {surface!r}; legal values: {legal}") from exc


def _as_mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _agg_summary_of(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return the S3 zone map, preferring the nested copy.

    Consumers probe both ``result.value.agg_summary`` and the hoisted
    top-level ``agg_summary`` (be-analytics tries seven paths in total), so
    either is acceptable input here.
    """
    result = _as_mapping(payload.get("result")) or {}
    value = _as_mapping(result.get("value")) or {}
    nested = _as_mapping(value.get("agg_summary"))
    if nested is not None:
        return nested
    return _as_mapping(payload.get("agg_summary")) or {}


# ---------------------------------------------------------------------------
# Check 1 -- required fields, right names, right casing, no nulls
# ---------------------------------------------------------------------------


def check_required_fields(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Check 1: the payload round-trips the Go parser's expectations.

    Every required field is present, spelled and cased exactly as the Go DTO
    declares it, non-empty, and never ``null`` where a string is declared
    (contract Section 1 rule 7 -- a ``null`` loses the whole message).

    Args:
        payload: The candidate wire payload.
        surface: Which contract to validate against.

    Returns:
        A list of :class:`ConformanceError`; empty when the check passes.
    """
    resolved = _coerce_surface(surface)
    collector = _Collector("check_required_fields", resolved)

    if not isinstance(payload, Mapping):
        collector.add("<payload>", f"expected an object, got {type(payload).__name__}")
        return collector.errors

    if resolved is Surface.results_agg:
        _required_strings(collector, payload, "", _S1_REQUIRED, required=True)
        _required_strings(collector, payload, "", _S1_OPTIONAL_STRINGS, required=False)
        _wrong_names(collector, payload, "", _S1_WRONG_NAMES)
        _check_metric_fields(collector, payload)

    elif resolved is Surface.incident_res:
        _required_strings(collector, payload, "", _S2_REQUIRED, required=True)
        _required_strings(collector, payload, "", _S2_OPTIONAL_STRINGS, required=False)
        _wrong_names(collector, payload, "", _S2_WRONG_NAMES)
        _check_incident_fields(collector, payload)

    else:  # Surface.frame_result
        _check_frame_structure(collector, payload)

    return collector.errors


def _required_strings(
    collector: _Collector,
    node: Mapping[str, Any],
    prefix: str,
    names: Iterable[str],
    *,
    required: bool,
) -> None:
    for name in names:
        path = f"{prefix}{name}"
        if name not in node:
            if required:
                collector.add(path, "required field is missing")
            continue
        value = node[name]
        if value is None:
            collector.add(
                path,
                "is null; emit \"\" instead -- the Go parser rejects a null where "
                "a string is declared and loses the whole message "
                "(contract Section 1 rule 7)",
            )
        elif not isinstance(value, str):
            collector.add(path, f"must be a string, got {type(value).__name__}")
        elif required and not value.strip():
            collector.add(
                path,
                "is empty; the backend accepts it silently and produces a row "
                "nothing can query (contract Section 1 rule 3)",
            )


def _wrong_names(
    collector: _Collector,
    node: Mapping[str, Any],
    prefix: str,
    wrong: Mapping[str, str],
) -> None:
    for bad, good in wrong.items():
        if bad in node:
            collector.add(
                f"{prefix}{bad}",
                f"is not a field on this surface; use {good!r}",
            )


def _check_metric_fields(collector: _Collector, payload: Mapping[str, Any]) -> None:
    metrics = payload.get("metrics", [])
    if metrics is None:
        collector.add("metrics", "is null; emit [] instead")
        return
    if not isinstance(metrics, Sequence) or isinstance(metrics, (str, bytes)):
        collector.add("metrics", f"must be an array, got {type(metrics).__name__}")
        return
    for index, entry in enumerate(metrics):
        path = f"metrics[{index}]"
        mapping = _as_mapping(entry)
        if mapping is None:
            collector.add(path, f"must be an object, got {type(entry).__name__}")
            continue
        for name in _METRIC_REQUIRED:
            if name not in mapping:
                collector.add(f"{path}.{name}", "required field is missing")
        if "zone_id" in mapping:
            collector.add(
                f"{path}.zone_id",
                "use 'zone', only ever 'zone' (PY-8). The Go DTO accepts both "
                "with 'zone' winning, but two names for one concept is how the "
                "field drifts.",
            )
        if isinstance(mapping.get("data"), str):
            collector.add(
                f"{path}.data",
                f"is the string {mapping['data']!r}; data is a float, never a "
                "numeric string (contract Section 1 rule 6)",
            )
        elif isinstance(mapping.get("data"), bool) or not isinstance(
            mapping.get("data", 0), (int, float)
        ):
            collector.add(f"{path}.data", "must be a number")
        zone = mapping.get("zone")
        if zone == "__global__":
            collector.add(
                f"{path}.zone",
                "'__global__' is the legacy sentinel (PY-6); use 'global'. The "
                "two spellings split an app's ClickHouse history.",
            )


def _check_incident_fields(collector: _Collector, payload: Mapping[str, Any]) -> None:
    incidents = payload.get("incidents")
    if incidents is None:
        collector.add("incidents", "required field is missing")
        return
    if not isinstance(incidents, Sequence) or isinstance(incidents, (str, bytes)):
        collector.add("incidents", f"must be an array, got {type(incidents).__name__}")
        return
    if not incidents:
        collector.add(
            "incidents",
            "is empty; incident_res is emitted on a severity transition, so an "
            "empty message is wasted work (contract Section 3.4)",
        )
    for index, entry in enumerate(incidents):
        path = f"incidents[{index}]"
        mapping = _as_mapping(entry)
        if mapping is None:
            collector.add(path, f"must be an object, got {type(entry).__name__}")
            continue
        _required_strings(
            collector, mapping, f"{path}.", _INCIDENT_REQUIRED, required=True
        )
        # end_time must be PRESENT (the backend derives status from it) but may
        # legitimately be "" while the incident is open -- contract Section 3.2.
        if "end_time" not in mapping:
            collector.add(
                f"{path}.end_time",
                "required field is missing; the backend derives status from it "
                "('resolved' if it parses, else 'active'), so emit \"\" while the "
                "incident is open",
            )
        else:
            _required_strings(collector, mapping, f"{path}.", ("end_time",), required=False)
        _wrong_names(collector, mapping, f"{path}.", _INCIDENT_WRONG_NAMES)
        if "status" in mapping:
            collector.add(
                f"{path}.status",
                "must not be sent: status is DERIVED by the backend from "
                "end_time ('resolved' if it parses, else 'active'). Sending it "
                "implies a control the producer does not have.",
            )


def _check_frame_structure(collector: _Collector, payload: Mapping[str, Any]) -> None:
    result = _as_mapping(payload.get("result"))
    value = _as_mapping(result.get("value")) if result is not None else None
    nested_summary = _as_mapping(value.get("agg_summary")) if value is not None else None
    if result is None:
        collector.add("result", "required field is missing or not an object")
    elif value is None:
        collector.add("result.value", "required field is missing or not an object")
    elif nested_summary is None:
        collector.add(
            "result.value.agg_summary",
            "required field is missing or not an object; absent means MPR1 "
            "stores 0 detections per frame with no fallback",
        )

    hoisted = _as_mapping(payload.get("agg_summary"))
    if hoisted is None:
        collector.add(
            "agg_summary",
            "the hoisted copy is missing or not an object; consumers probe both "
            "result.value.agg_summary and the top-level agg_summary",
        )
    elif nested_summary is not None and set(nested_summary) != set(hoisted):
        collector.add(
            "agg_summary",
            f"diverges from result.value.agg_summary: {sorted(hoisted)} vs "
            f"{sorted(nested_summary)}. Consumers probe both paths and would "
            "see different data depending on which one they picked.",
        )

    summary = _agg_summary_of(payload)
    for zone, entry in summary.items():
        mapping = _as_mapping(entry)
        if mapping is None:
            collector.add(
                f"agg_summary.{zone}", f"must be an object, got {type(entry).__name__}"
            )
            continue
        stats = mapping.get("tracking_stats")
        if not isinstance(stats, Mapping):
            collector.add(
                f"agg_summary.{zone}.tracking_stats",
                "must be an object; the legacy list default from "
                "post_processing/core/base.py:689 fails every consumer's "
                "map assertion silently",
            )
            continue
        detections = stats.get("detections")
        if detections is None:
            collector.add(
                f"agg_summary.{zone}.tracking_stats.detections",
                "is missing; be-media-server's MPR1 storage reads only this list "
                "and stores an empty frame without it",
            )
        elif not isinstance(detections, Sequence) or isinstance(detections, (str, bytes)):
            collector.add(
                f"agg_summary.{zone}.tracking_stats.detections",
                f"must be an array, got {type(detections).__name__}",
            )


# ---------------------------------------------------------------------------
# Check 2 -- every enum value is legal
# ---------------------------------------------------------------------------


def check_enum_values(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Check 2: every enum value appears in ``06-vocabularies.md``.

    All enums are closed (contract Section 1 rule 4).  Nothing downstream
    validates them -- an unknown ``agg_type`` is silently summed (PY-1), an
    unknown severity defaults the backend's escalation check to "escalation =
    true", and an ``IDENTITY`` category lands in ClickHouse as an unfilterable
    literal (V7).

    Args:
        payload: The candidate wire payload.
        surface: Which contract to validate against.

    Returns:
        A list of :class:`ConformanceError`; empty when the check passes.
    """
    resolved = _coerce_surface(surface)
    collector = _Collector("check_enum_values", resolved)
    if not isinstance(payload, Mapping):
        collector.add("<payload>", f"expected an object, got {type(payload).__name__}")
        return collector.errors

    legal_agg = {member.value for member in AggType}
    legal_category = {member.value for member in Category}
    legal_severity = {member.value for member in Severity}

    if resolved is Surface.results_agg:
        metrics = payload.get("metrics") or []
        if isinstance(metrics, Sequence) and not isinstance(metrics, (str, bytes)):
            for index, entry in enumerate(metrics):
                mapping = _as_mapping(entry)
                if mapping is None:
                    continue
                path = f"metrics[{index}]"
                agg = mapping.get("agg_type")
                if agg not in legal_agg:
                    hint = ""
                    if agg in {"avg", "average"}:
                        hint = (
                            " -- use 'mean'; the backend vocabulary is 'mean' and "
                            "py_analytics' old dispatch silently summed anything "
                            "it did not recognise (PY-1)"
                        )
                    elif agg == "median":
                        hint = (
                            " -- use 'mean'; the backend's 'median' silently "
                            "returns the mean (BE-1)"
                        )
                    collector.add(
                        f"{path}.agg_type",
                        f"{agg!r} is not a legal agg_type{hint}. Legal values: "
                        f"{_sorted(legal_agg)}",
                    )
                category = mapping.get("category")
                if category not in legal_category:
                    hint = ""
                    if category in {"IDENTITY", "SPECIAL"}:
                        hint = (
                            " -- it is a py_analytics-internal processor category "
                            "with no backend meaning (V7)"
                        )
                    collector.add(
                        f"{path}.category",
                        f"{category!r} is not a legal category{hint}. Legal "
                        f"values: {_sorted(legal_category)}",
                    )

    elif resolved is Surface.incident_res:
        category = payload.get("category", "")
        if category not in legal_category and category != "":
            collector.add(
                "category",
                f"{category!r} is not a legal category. Legal values: "
                f"{_sorted(legal_category)} or '' (untagged)",
            )
        incidents = payload.get("incidents") or []
        if isinstance(incidents, Sequence) and not isinstance(incidents, (str, bytes)):
            for index, entry in enumerate(incidents):
                mapping = _as_mapping(entry)
                if mapping is None:
                    continue
                severity = mapping.get("severity_level")
                if severity in legal_severity:
                    continue
                if severity == "significant":
                    collector.add(
                        f"incidents[{index}].severity_level",
                        "'significant' is a py_analytics-internal level and must "
                        "never reach the wire (FROZEN-7); map it to 'high'. The "
                        "backend has no such level, does not validate severity, "
                        "and would store the literal string.",
                    )
                else:
                    collector.add(
                        f"incidents[{index}].severity_level",
                        f"{severity!r} is not a legal severity. Legal values "
                        f"(lowercase): {_sorted(legal_severity)}",
                    )

    return collector.errors


def _sorted(values: Iterable[str]) -> str:
    return ", ".join(repr(value) for value in sorted(values))


# ---------------------------------------------------------------------------
# Check 3 -- timestamps parse
# ---------------------------------------------------------------------------


def check_timestamps(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Check 3: every timestamp parses as RFC3339-with-``Z``.

    ``stream_time`` is the one exception -- it uses the media format
    ``"YYYY-MM-DD-HH:mm:ss.ffffff UTC"`` (contract Section 3.3).

    This check exists because ``parseRFC3339Time`` on the backend silently
    rewrites an unparseable timestamp to *now* (BE-6): the producer sees no
    error anywhere and the data is simply mis-bucketed.

    Args:
        payload: The candidate wire payload.
        surface: Which contract to validate against.

    Returns:
        A list of :class:`ConformanceError`; empty when the check passes.
    """
    resolved = _coerce_surface(surface)
    collector = _Collector("check_timestamps", resolved)
    if not isinstance(payload, Mapping):
        collector.add("<payload>", f"expected an object, got {type(payload).__name__}")
        return collector.errors

    def rfc3339(path: str, value: Any, *, allow_blank: bool) -> None:
        if value is None:
            collector.add(path, 'is null; emit "" instead')
            return
        if allow_blank and value == "":
            return
        if not is_rfc3339z(value):
            collector.add(
                path,
                f"{value!r} is not RFC3339 with a 'Z' suffix (expected e.g. "
                "'2026-03-16T00:05:00Z'); the backend silently rewrites an "
                "unparseable timestamp to 'now' (BE-6)",
            )

    if resolved is Surface.results_agg:
        if "input_timestamp" not in payload:
            collector.add(
                "input_timestamp",
                "must always be set: without it the backend falls back to 'the "
                "first zone's timestamp' in Go map iteration order, which is "
                "nondeterministic (BE-5)",
            )
        else:
            rfc3339("input_timestamp", payload["input_timestamp"], allow_blank=False)
        for zone, stats in (_as_mapping(payload.get("tracking_stats")) or {}).items():
            mapping = _as_mapping(stats)
            if mapping is None:
                continue
            rfc3339(
                f"tracking_stats.{zone}.input_timestamp",
                mapping.get("input_timestamp"),
                allow_blank=False,
            )
            if "reset_timestamp" in mapping:
                rfc3339(
                    f"tracking_stats.{zone}.reset_timestamp",
                    mapping["reset_timestamp"],
                    allow_blank=True,
                )

    elif resolved is Surface.incident_res:
        stream_time = payload.get("stream_time", "")
        if stream_time is None:
            collector.add("stream_time", 'is null; emit "" instead')
        elif stream_time != "" and not is_stream_time(stream_time):
            collector.add(
                "stream_time",
                f"{stream_time!r} does not parse as the media format "
                "'YYYY-MM-DD-HH:mm:ss.ffffff UTC' (contract Section 3.3). It is "
                "deliberately NOT RFC3339 -- do not 'fix' it.",
            )
        incidents = payload.get("incidents") or []
        if isinstance(incidents, Sequence) and not isinstance(incidents, (str, bytes)):
            for index, entry in enumerate(incidents):
                mapping = _as_mapping(entry)
                if mapping is None:
                    continue
                rfc3339(
                    f"incidents[{index}].start_time",
                    mapping.get("start_time"),
                    allow_blank=False,
                )
                rfc3339(
                    f"incidents[{index}].end_time",
                    mapping.get("end_time", ""),
                    allow_blank=True,
                )

    else:  # Surface.frame_result
        for zone, entry in _agg_summary_of(payload).items():
            stats = _as_mapping((_as_mapping(entry) or {}).get("tracking_stats"))
            if stats is None:
                continue
            if "input_timestamp" in stats:
                rfc3339(
                    f"agg_summary.{zone}.tracking_stats.input_timestamp",
                    stats["input_timestamp"],
                    allow_blank=False,
                )
            if "reset_timestamp" in stats:
                rfc3339(
                    f"agg_summary.{zone}.tracking_stats.reset_timestamp",
                    stats["reset_timestamp"],
                    allow_blank=True,
                )

    return collector.errors


# ---------------------------------------------------------------------------
# Check 4 -- tracking_stats is zone-keyed with all four count lists
# ---------------------------------------------------------------------------


def check_tracking_stats_shape(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Check 4: ``tracking_stats`` is zone-keyed and complete.

    **FROZEN-2**: the parser treats every top-level key of ``tracking_stats``
    as a zone id (``mappers/kafka_analytics_results_agg.go:67``).  The flat
    form -- which the backend's own contract doc incorrectly shows -- creates
    zones named ``current_counts`` and **fails to unmarshal the entire
    message**.

    **FROZEN-5**: all four count lists must be present in every zone, even
    though two of them are ignored on the main ingestion path.

    On S3 the same rule applies to each ``agg_summary`` zone's
    ``tracking_stats``, which is the fix for **PY-2** -- without the count
    lists, be-analytics' ``hasTrackingStats`` fails on all seven probe paths
    and every instant metric evaluates against zero.

    Args:
        payload: The candidate wire payload.
        surface: Which contract to validate against.

    Returns:
        A list of :class:`ConformanceError`; empty when the check passes.
        Always empty for :attr:`Surface.incident_res`, which has no
        ``tracking_stats``.
    """
    resolved = _coerce_surface(surface)
    collector = _Collector("check_tracking_stats_shape", resolved)
    if not isinstance(payload, Mapping):
        collector.add("<payload>", f"expected an object, got {type(payload).__name__}")
        return collector.errors

    if resolved is Surface.incident_res:
        return collector.errors

    if resolved is Surface.results_agg:
        raw = payload.get("tracking_stats", {})
        if raw is None:
            collector.add("tracking_stats", "is null; emit {} instead")
            return collector.errors
        zones = _as_mapping(raw)
        if zones is None:
            collector.add(
                "tracking_stats",
                f"must be an object keyed by zone id, got {type(raw).__name__} "
                "(FROZEN-2)",
            )
            return collector.errors
        flat = sorted(set(COUNT_LIST_FIELDS) & set(zones)) + sorted(
            {"input_timestamp", "reset_timestamp"} & set(zones)
        )
        if flat:
            collector.add(
                "tracking_stats",
                f"is FLAT, not zone-keyed: found {flat} at the top level. The Go "
                "parser treats every top-level key as a zone id (FROZEN-2), so "
                "this creates zones with those names and fails to unmarshal the "
                'entire message. Wrap it: {"global": {...}}.',
            )
            return collector.errors
        prefix = "tracking_stats"
    else:  # Surface.frame_result
        zones = _agg_summary_of(payload)
        prefix = "agg_summary"

    for zone, node in zones.items():
        if not str(zone).strip():
            collector.add(f"{prefix}.<empty>", "zone id must be non-empty")
        if str(zone) == "__global__":
            collector.add(
                f"{prefix}.__global__",
                "'__global__' is the legacy sentinel (PY-6); use 'global'. The "
                "sentinel becomes raw_analytics.zoneId, so migrating an app "
                "between the two spellings splits its ClickHouse history into "
                "two unrelated series.",
            )
        stats = _as_mapping(node)
        if resolved is Surface.frame_result:
            stats = _as_mapping((stats or {}).get("tracking_stats"))
            zone_path = f"{prefix}.{zone}.tracking_stats"
        else:
            zone_path = f"{prefix}.{zone}"
        if stats is None:
            collector.add(zone_path, "must be an object")
            continue
        for name in COUNT_LIST_FIELDS:
            path = f"{zone_path}.{name}"
            if name not in stats:
                collector.add(
                    path,
                    "is missing; all four count lists must be present in every "
                    "zone (FROZEN-5). current_new_counts and total_counts are "
                    "ignored on the main ingestion path but the instant-metric "
                    "path and dataField resolution depend on them.",
                )
                continue
            _check_count_list(collector, path, stats[name])

    return collector.errors


def _check_count_list(collector: _Collector, path: str, value: Any) -> None:
    if value is None:
        collector.add(path, "is null; emit [] instead")
        return
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        collector.add(path, f"must be an array, got {type(value).__name__}")
        return
    for index, entry in enumerate(value):
        item_path = f"{path}[{index}]"
        mapping = _as_mapping(entry)
        if mapping is None:
            collector.add(
                item_path,
                f'must be an object {{"category": str, "count": int}}, got '
                f"{type(entry).__name__}",
            )
            continue
        category = mapping.get("category")
        if not isinstance(category, str) or not category:
            collector.add(
                f"{item_path}.category", "must be a non-empty ML class-name string"
            )
        count = mapping.get("count")
        if isinstance(count, str):
            collector.add(
                f"{item_path}.count",
                f"is the string {count!r}; count is an int, never a numeric "
                "string (contract Section 1 rule 6)",
            )
        elif isinstance(count, bool) or not isinstance(count, int):
            collector.add(f"{item_path}.count", "must be an int")


# ---------------------------------------------------------------------------
# Check 5 -- no camelCase outside the frozen four
# ---------------------------------------------------------------------------


def check_no_stray_camelcase(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Check 5: no camelCase field name outside contract Section 6.

    snake_case everywhere except :data:`~...schemas.ALLOWED_CAMELCASE_FIELDS`.
    There are exactly four entries (one of which is the four-name
    frame-address tuple, FROZEN-6); any other camelCase field is a bug.

    The walk is **structure-aware**: dictionary keys that carry *data* rather
    than field names -- zone ids in ``tracking_stats`` / ``agg_summary``, and
    everything inside the opaque ``business_analytics`` / ``alerts`` /
    ``incidents`` display blobs -- are never inspected.  A zone legitimately
    called ``"zoneA"`` is not a violation.

    Args:
        payload: The candidate wire payload.
        surface: Which contract to validate against.

    Returns:
        A list of :class:`ConformanceError`; empty when the check passes.
    """
    resolved = _coerce_surface(surface)
    collector = _Collector("check_no_stray_camelcase", resolved)
    if not isinstance(payload, Mapping):
        collector.add("<payload>", f"expected an object, got {type(payload).__name__}")
        return collector.errors

    def inspect(node: Any, path: str) -> None:
        """Flag camelCase keys on ``node``; keys here are field names."""
        mapping = _as_mapping(node)
        if mapping is None:
            return
        for key in mapping:
            if _is_stray_camelcase(str(key)):
                collector.add(
                    f"{path}{key}" if path else str(key),
                    "is camelCase. The contract is snake_case everywhere except "
                    f"{sorted(ALLOWED_CAMELCASE_FIELDS)} (contract Section 6). "
                    "Any other camelCase field is a bug.",
                )

    def inspect_each(items: Any, path_fmt: str) -> None:
        if isinstance(items, Sequence) and not isinstance(items, (str, bytes)):
            for index, item in enumerate(items):
                inspect(item, path_fmt.format(index=index))

    if resolved is Surface.results_agg:
        inspect(payload, "")
        for zone, stats in (_as_mapping(payload.get("tracking_stats")) or {}).items():
            inspect(stats, f"tracking_stats.{zone}.")
            for name in COUNT_LIST_FIELDS:
                inspect_each(
                    (_as_mapping(stats) or {}).get(name),
                    f"tracking_stats.{zone}.{name}[{{index}}].",
                )
        inspect_each(payload.get("metrics"), "metrics[{index}].")

    elif resolved is Surface.incident_res:
        inspect(payload, "")
        inspect_each(payload.get("incidents"), "incidents[{index}].")

    else:  # Surface.frame_result
        inspect(payload, "")
        result = _as_mapping(payload.get("result")) or {}
        inspect(result, "result.")
        value = _as_mapping(result.get("value")) or {}
        inspect(value, "result.value.")
        streams = value.get("input_streams")
        if isinstance(streams, Sequence) and not isinstance(streams, (str, bytes)):
            for index, entry in enumerate(streams):
                inspect(entry, f"result.value.input_streams[{index}].")
                inspect(
                    (_as_mapping(entry) or {}).get("input_stream"),
                    f"result.value.input_streams[{index}].input_stream.",
                )
        for zone, entry in _agg_summary_of(payload).items():
            # 'business_analytics', 'alerts' and 'incidents' are opaque display
            # blobs; their inner keys are data, not contract field names.
            inspect(entry, f"agg_summary.{zone}.")
            stats = _as_mapping((_as_mapping(entry) or {}).get("tracking_stats"))
            inspect(stats, f"agg_summary.{zone}.tracking_stats.")
            for name in COUNT_LIST_FIELDS:
                inspect_each(
                    (stats or {}).get(name),
                    f"agg_summary.{zone}.tracking_stats.{name}[{{index}}].",
                )
            detections = (stats or {}).get("detections")
            if isinstance(detections, Sequence) and not isinstance(
                detections, (str, bytes)
            ):
                for index, detection in enumerate(detections):
                    base = f"agg_summary.{zone}.tracking_stats.detections[{index}]."
                    inspect(detection, base)
                    inspect(
                        (_as_mapping(detection) or {}).get("bounding_box"),
                        f"{base}bounding_box.",
                    )

    return collector.errors


def _is_stray_camelcase(name: str) -> bool:
    """Whether ``name`` is camelCase and not on the frozen allowlist."""
    if name in ALLOWED_CAMELCASE_FIELDS:
        return False
    return any(
        previous.islower() or previous.isdigit()
        for previous, current in pairwise(name)
        if current.isupper()
    )


# ---------------------------------------------------------------------------
# Check 6 -- the payload carries something
# ---------------------------------------------------------------------------


def check_payload_not_empty(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Check 6: at least one of ``tracking_stats`` / ``metrics`` is non-empty.

    The backend drops a message with neither, logging *"message has neither
    tracking_stats nor metrics"* (``kafka_analytics_results_agg.go:77``).

    On S3 the equivalent is: ``agg_summary`` has at least one zone.

    Args:
        payload: The candidate wire payload.
        surface: Which contract to validate against.

    Returns:
        A list of :class:`ConformanceError`; empty when the check passes.
        Always empty for :attr:`Surface.incident_res`, whose emptiness is
        covered by :func:`check_required_fields`.
    """
    resolved = _coerce_surface(surface)
    collector = _Collector("check_payload_not_empty", resolved)
    if not isinstance(payload, Mapping):
        collector.add("<payload>", f"expected an object, got {type(payload).__name__}")
        return collector.errors

    if resolved is Surface.results_agg:
        if not payload.get("tracking_stats") and not payload.get("metrics"):
            collector.add(
                "tracking_stats|metrics",
                "at least one must be non-empty, or the backend drops the "
                'message with "message has neither tracking_stats nor metrics" '
                "(kafka_analytics_results_agg.go:77)",
            )
    elif resolved is Surface.frame_result:
        if not _agg_summary_of(payload):
            collector.add(
                "agg_summary",
                "is empty; the frame surface must carry at least one zone "
                "(use 'global' for single-bucket apps)",
            )

    return collector.errors


# ---------------------------------------------------------------------------
# Aggregate entry points
# ---------------------------------------------------------------------------

CHECKS: Final[
    tuple[Callable[[Mapping[str, Any], Any], list[ConformanceError]], ...]
] = (
    check_required_fields,
    check_enum_values,
    check_timestamps,
    check_tracking_stats_shape,
    check_no_stray_camelcase,
    check_payload_not_empty,
)
"""The six checks, in contract Section 7 order."""


def conformance_errors(
    payload: Mapping[str, Any], surface: Surface | str
) -> list[ConformanceError]:
    """Run all six checks and return every violation found.

    Args:
        payload: The candidate wire payload.
        surface: :class:`Surface` or its wire string.

    Returns:
        Every :class:`ConformanceError`, in check order.  Empty means the
        payload conforms.
    """
    resolved = _coerce_surface(surface)
    errors: list[ConformanceError] = []
    for check in CHECKS:
        errors.extend(check(payload, resolved))
    return errors


def conforms(payload: Mapping[str, Any], surface: Surface | str) -> bool:
    """Whether ``payload`` passes all six checks."""
    return not conformance_errors(payload, surface)


def assert_conforms(payload: Mapping[str, Any], surface: Surface | str) -> None:
    """Raise unless ``payload`` conforms to ``surface``.

    Called on every emit path (see
    :mod:`matrice_analytics.engine.contract.emit`) because the engine
    validates its own output -- nothing downstream will (contract Section 1
    rule 3).

    Args:
        payload: The candidate wire payload.
        surface: :class:`Surface` or its wire string.

    Raises:
        ConformanceViolation: Listing every problem found, not just the first.
    """
    resolved = _coerce_surface(surface)
    errors = conformance_errors(payload, resolved)
    if errors:
        raise ConformanceViolation(resolved, errors)
