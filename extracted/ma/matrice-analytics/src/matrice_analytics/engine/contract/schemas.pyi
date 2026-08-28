"""Auto-generated stub for module: schemas."""
from typing import Any, Union

# Constants
AggTypeField: Any
CategoryField: Any
IncidentCategoryField: Any
SeverityField: Any
WireFloat: Any
WireInt: Any
WireStr: Any
logger: Any

# Functions
def derive_incident_status(end_time: str) -> Any:
    """
    Reproduce the backend's status derivation, for local reasoning only.
    
        Args:
            end_time: The incident's ``end_time`` wire value (``""`` while open).
    
        Returns:
            :attr:`IncidentStatus.resolved` when ``end_time`` parses as RFC3339,
            otherwise :attr:`IncidentStatus.active`.
    """
    ...
def is_rfc3339z(text: Any) -> bool:
    """
    Whether ``text`` is a well-formed RFC3339-with-``Z`` timestamp.
    """
    ...
def is_stream_time(text: Any) -> bool:
    """
    Whether ``text`` is a well-formed ``stream_time`` value.
    """
    ...
def now_rfc3339z() -> str:
    """
    Current UTC instant as RFC3339 with ``Z``.
    """
    ...
def parse_agg_type(value: Any) -> Any:
    """
    Coerce a manifest/legacy ``agg_type`` to a legal :class:`AggType`.
    
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
    ...
def parse_category(value: Any) -> Any:
    """
    Coerce a manifest/legacy category to a legal :class:`Category`.
    
        Args:
            value: The declared category (case-insensitive).
    
        Returns:
            The matching :class:`Category`.
    
        Raises:
            ValueError: The value is not legal.  ``IDENTITY`` and ``SPECIAL`` get
                a message explaining that they are processor-internal and have no
                backend meaning (divergence V7).
    """
    ...
def parse_incident_category(value: Any) -> Union[Any, Any['']]:
    """
    Like :func:`parse_category` but also accepts ``""`` (untagged).
    
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
    ...
def parse_rfc3339z(text: str) -> Any:
    """
    Parse a contract timestamp, requiring the ``Z`` suffix.
    
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
    ...
def parse_severity(value: Any) -> Any:
    """
    Coerce any internal / manifest / legacy severity to a wire value.
    
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
    ...
def parse_stream_time(text: str) -> Any:
    """
    Parse a ``stream_time`` value using the two accepted media layouts.
    
        Args:
            text: The wire value.
    
        Returns:
            An aware UTC datetime.
    
        Raises:
            ValueError: The value matches neither layout in
                :data:`STREAM_TIME_FORMATS`.
    """
    ...
def to_rfc3339z(value: Any | int | float | str) -> str:
    """
    Format any instant as RFC3339 UTC with a literal ``Z`` suffix.
    
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
    ...
def to_stream_time(value: Any | int | float) -> str:
    """
    Format ``stream_time`` in the media format -- *not* RFC3339.
    
        ``"YYYY-MM-DD-HH:mm:ss.ffffff UTC"``, e.g.
        ``"2026-03-10-15:30:45.123456 UTC"``.  Contract Section 3.3; the Go side
        parses it at ``be-analytics/internal/utils/frame_helper.go:56-75``.
        Emitting RFC3339 here loses the frame anchor.
    
        Args:
            value: The instant to format.
    
        Returns:
            The media-format timestamp string.
    """
    ...
def zone_identity(zone_name: str) -> str:
    """
    The identity a zone is keyed by, everywhere. **This is the Q1 seam.**
    
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
    ...

# Classes
class AggType:
    # How the backend collapses a metric across a rollup window.
    #
    #     ``sum`` / ``mean`` / ``min`` / ``max`` / ``last``, matching the backend
    #     vocabulary at ``entities/raw_business_metrics_clickhouse.go:31-38``.
    #
    #     Notably absent:
    #
    #     * ``avg`` -- the backend spells it ``mean``.  py_analytics' current
    #       dispatch knows only ``avg`` and **falls back to ``sum``** for anything
    #       else (``analytics/base_processor.py:353-365``), so every manifest
    #       declaring ``mean`` publishes a *sum* of per-frame values today.  A
    #       60-second window at 25 fps can emit a "compliance percentage" of
    #       150,000.  That is defect PY-1, a live production bug, and it is the
    #       reason an unknown ``agg_type`` must raise rather than fall back.
    #     * ``median`` -- accepted by the backend but it silently returns the mean
    #       (BE-1, acknowledged in a code comment).  Declaring it would publish a
    #       value that does not mean what it says.

    last: str
    max: str
    mean: str
    min: str
    sum: str

class AggregationResult:
    # S1 -- the ``results-agg`` message (contract Section 2).
    #
    #     Emitted once per 60-second window per camera via
    #     ``XADD results-agg {"data": <json>}``.
    #
    #     Field order matches the worked example in contract Section 2.4 so that a
    #     serialised payload is byte-comparable with the spec.

    ...
class BoundingBox:
    # A **normalized 0-1** bounding box.
    #
    #     Contract Section 4, "Coordinate space": normalized 0-1, always, no
    #     exceptions.  The consumers cannot be fixed from here (D5) -- fe-streaming
    #     *guesses* between normalized, model and source space per detection with a
    #     one-sided guard that can apply two different mappings inside one frame
    #     (BE-10), and be-media-server's MPR1 ingest assumes a hardcoded 640x640
    #     (BE-12).  Emitting anything but 0-1 feeds both bugs; the range check here
    #     makes the classic 1920x error impossible to ship.

    ...
class Category:
    # Analytics category for a metric or an incident.
    #
    #     ``VOLUME`` / ``SAFETY`` / ``QUALITY`` only (vocabulary Section 1).
    #
    #     ``IDENTITY`` and ``SPECIAL`` are py_analytics-internal *processor*
    #     categories with no backend meaning (divergence V7).  A metric tagged with
    #     one lands in ClickHouse as a literal string that no UI surface groups by,
    #     so they are rejected here rather than passed through.

    QUALITY: str
    SAFETY: str
    VOLUME: str

class Detection:
    # One detection inside a zone's frame-path ``tracking_stats``.
    #
    #     ``confidence`` is required on purpose: be-media-server rewrites a
    #     confidence of 0 with a non-empty category to 1.0 (BE-12), so an omitted
    #     field is indistinguishable from full confidence in stored playback.

    ...
class FrameResult:
    # S3 -- the per-frame **return value** (contract Section 4).
    #
    #     py_analytics does *not* write this stream.  It returns a dict and a worker
    #     outside this workspace publishes it to
    #     ``<cameraId>_<appDeploymentId>_output_topic``.  We own exactly two keys:
    #     ``agg_summary`` and the detections inside it.  Everything else on that
    #     wire -- ``frame_id``, ``rtp_timestamp``, ``metadata.input_size`` -- is
    #     stamped by the pipeline and cannot be changed from here (backlog Q5).
    #
    #     ``agg_summary`` appears twice, nested under ``result.value`` and hoisted
    #     to the top level, because consumers probe both paths
    #     (be-analytics tries seven).  The two are guaranteed identical by
    #     :meth:`_hoisted_matches_nested`.

    ...
class FrameSummaryEntry:
    # One zone's entry in ``agg_summary`` (contract Section 4).
    #
    #     ``agg_summary`` is keyed by **zone**, consistently.  Today the key is
    #     ``"<int>"``, ``"None"``, ``"current_frame"`` or a zone name depending on
    #     which file you land in (PY-5); four consumers cope four different ways
    #     and three break on multi-zone payloads.  Zone-keying matches S1 and is the
    #     only form that works for multi-zone apps -- but it is a **visible
    #     behaviour change for three consumers and must be announced, not slipped
    #     in**.

    ...
class FrameTrackingStats:
    # The frame-path ``tracking_stats``, i.e. S1's plus display fields.
    #
    #     **This subclass is the fix for PY-2**, the single most important
    #     correction on the frame surface.  Today the frame-path ``TrackingStats``
    #     carries only ``human_text`` and ``detections``
    #     (``analytics/schemas.py:280-289``), so be-analytics' instant-metric
    #     extractor -- whose ``hasTrackingStats`` tests only the four count lists
    #     (``tracker_clickhouse_service.go:1049-1054``) -- finds nothing on all
    #     seven of its probe paths and **every instant metric evaluates against
    #     zero**.  It also empties fe-streaming's live incident panel and degrades
    #     the live counter to "number of boxes drawn".
    #
    #     Inheriting from :class:`TrackingStats` means the count lists cannot be
    #     dropped from this surface again.
    #
    #     **One field is read differently here (BE-16).**  ``current_counts`` on this
    #     surface is the frame's **level** -- how many objects are in view right now.
    #     be-analytics resolves its ``total_count`` and ``category_total_count``
    #     instant-metric dataFields from it
    #     (``tracker_clickhouse_service.go:1097-1120``), so an arrival delta here
    #     would make every occupancy alert rule read approximately zero.  The parent
    #     class's ``current_counts`` -- S1, once per window -- is the arrival delta
    #     instead, because it lands in ``raw_analytics.count`` and the backend sums
    #     that column.  Same name, two surfaces, two consumers, two readings; see
    #     :class:`~matrice_analytics.engine.runtime.window.ZoneCounters`, which
    #     builds both.

    ...
class Incident:
    # One entry in ``incident_res.incidents[]`` (contract Section 3.2).

    ...
class IncidentMessage:
    # S2 -- the ``incident_res`` message (contract Section 3).
    #
    #     ``XADD incident_res {"data": <json>}``, emitted on a severity
    #     **transition**, never per frame.
    #
    #     The field naming deliberately differs from S1: ``application_id`` rather
    #     than ``app_id``, ``location_name`` rather than ``location``.  Both are
    #     frozen -- they match a different Go DTO (``CameraEventIncoming``).

    ...
class IncidentStatus:
    # Incident status -- **derived by the backend, never sent**.
    #
    #     ``resolved`` if ``end_time`` parses, else ``active``
    #     (``incident_clickhouse_service.go:245-248``).  Declared here so engine
    #     code can reason about lifecycle state, but a payload carrying a
    #     ``status`` field is a conformance error: sending it implies a control
    #     the producer does not have.

    active: str
    resolved: str

class InputStreamEntry:
    # Wrapper preserving the pipeline's ``input_streams`` shape.

    ...
class InputStreamInfo:
    # ``input_streams[].input_stream`` -- the pipeline's stream metadata echo.

    ...
class MetricEntry:
    # One entry in ``results-agg.metrics[]``.
    #
    #     Contract Section 2.3.  Lands in ClickHouse as a ``raw_business_metrics``
    #     row.

    ...
class ResultValue:
    # ``result.value`` -- streams plus the zone-keyed summary.

    ...
class ResultWrapper:
    # ``result`` -- the pipeline's envelope around :class:`ResultValue`.

    ...
class Severity:
    # Incident severity, lowercase on the wire.
    #
    #     Vocabulary Section 2.  ``significant`` is deliberately *not* a member:
    #     py_analytics uses it internally and it must never reach the wire
    #     (FROZEN-7).  The backend has no such level, does not validate severity,
    #     and would store the literal string -- which then sorts and scores as an
    #     unknown value.  Use :func:`parse_severity`, which maps it to ``high``.

    critical: str
    high: str
    info: str
    low: str
    medium: str

class StreamInfo:
    # S4 -- the typed ``stream_info`` input (contract Section 5).
    #
    #     **Not owned by py_analytics** -- it arrives as an untyped dict from the
    #     inference worker and must be parsed defensively.  Today
    #     ``engine_session.py:263-389`` reverse-engineers it across five nested
    #     lookup paths in two casings; that function is the de-facto input contract.
    #     This model replaces it with an explicit schema and
    #     :meth:`from_raw`, whose fallbacks are logged.
    #
    #     ``extra="ignore"``: the worker sends more than we need, and rejecting the
    #     extras would break every deployment.

    model_config: Any

    def from_raw(cls: Any, raw: Any[str, Any] | None) -> Any:
        """
        Parse the untyped worker dict, with explicit, logged fallbacks.
        
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
        ...

class StreamInfoError:
    # A required ``stream_info`` field is missing or unusable.
    #
    #     Contract Section 5: *a missing required field is a startup error, not a
    #     silent default*.  Today an absent ``resolution`` silently disables zone
    #     processing, which presents to an operator as "the numbers are wrong"
    #     rather than "the config is broken".

    def __init__(self: Any, problems: list[str]) -> None: ...

class TrackingCount:
    # ``{"category": "person", "count": 3}`` -- one entry in a count list.
    #
    #     ``category`` here is the **ML class name** (``person``, ``vehicle``, ...),
    #     not an analytics :class:`Category`.  Vocabulary Section 13: it is a free
    #     string with no enum.

    ...
class TrackingStats:
    # The per-zone value of ``results-agg.tracking_stats`` (contract 2.2).
    #
    #     All four count lists are always present -- **FROZEN-5**.
    #     ``current_new_counts`` and ``total_counts`` are ignored on the main
    #     ingestion path (``tracker_clickhouse_service.go:626-687`` reads only
    #     ``current_counts`` and ``total_current_counts``) but the instant-metric
    #     path and ``dataField`` resolution depend on them.  Do not "optimise" them
    #     away; declaring them with list defaults guarantees they serialise even
    #     when empty.
    #
    #     **``current_counts`` means one thing here and another on the frame
    #     surface, and that is deliberate (BE-16).**  ``raw_analytics`` is a *delta
    #     plus level* schema: ``count`` is "how many arrived since the previous
    #     reading", ``totalCount`` is "how many were there at the reading", and the
    #     five-minute rollup is ``argMin(totalCount, t) + sum(count) -
    #     argMin(count, t)``
    #     (``10_aggregated_analytics_totals_schema.sql:7``).  On **this** class --
    #     S1, one row per 60-second window -- ``current_counts`` is therefore the
    #     window's **arrival delta**; a level there makes the rollup add up
    #     occupancy readings and publish several times the true footfall.  On
    #     :class:`FrameTrackingStats` it is the frame's level, because a frame has
    #     no interval to take a delta over and be-analytics reads it as
    #     ``total_count`` / ``category_total_count``, i.e. "how many objects right
    #     now" (``tracker_clickhouse_service.go:1097-1120``).
    #     :class:`~matrice_analytics.engine.runtime.window.ZoneCounters` builds both
    #     from the same four quantities.

    ...
class WireSegmentationMask:
    # A detection's mask on the wire, RLE-encoded (contract ``04`` §5.1).
    #
    #     Deliberately narrow: the only shape this engine ever emits or decodes, matching
    #     :func:`~matrice_analytics.engine.primitives.segmentation_area.decode_simple_rle_area`. A
    #     detection whose mask came in as a polygon or a precomputed area (no ``rle`` string) never
    #     gets a wire ``segmentation`` -- this engine does not rasterize/encode one for the wire
    #     (no numpy/cv2, **PY-20**), so there is nothing ready-to-emit to put here.

    ...
class ZoneConfig:
    # Normalized 0-1 geometry: named lines and polygons.
    #
    #     **One** ``ZoneConfig``, one convention (PY-7).  Two classes with the same
    #     name in the same package used opposite units -- ``analytics/schemas.py``
    #     normalized, ``post_processing/core/config.py`` pixels -- which is the most
    #     likely source of a silent 1920x error during migration.  Coordinates are
    #     normalized here; pixels are derived internally by whatever needs them,
    #     using :attr:`StreamInfo.resolution`.

    model_config: Any

