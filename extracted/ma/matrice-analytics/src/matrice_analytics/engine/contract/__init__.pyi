"""Stub file for engine.contract directory."""
from typing import Any, Set, Union

# Constants
logger: Any = ...  # From emit
AggTypeField: Any = ...  # From schemas
CategoryField: Any = ...  # From schemas
IncidentCategoryField: Any = ...  # From schemas
SeverityField: Any = ...  # From schemas
WireFloat: Any = ...  # From schemas
WireInt: Any = ...  # From schemas
WireStr: Any = ...  # From schemas
logger: Any = ...  # From schemas

# Functions
# From conformance
def assert_conforms(payload: Any[str, Any], surface: Any | str) -> None:
    """
    Raise unless ``payload`` conforms to ``surface``.
    
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
    ...

# From conformance
def check_enum_values(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 2: every enum value appears in ``06-vocabularies.md``.
    
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
    ...

# From conformance
def check_no_stray_camelcase(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 5: no camelCase field name outside contract Section 6.
    
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
    ...

# From conformance
def check_payload_not_empty(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 6: at least one of ``tracking_stats`` / ``metrics`` is non-empty.
    
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
    ...

# From conformance
def check_required_fields(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 1: the payload round-trips the Go parser's expectations.
    
        Every required field is present, spelled and cased exactly as the Go DTO
        declares it, non-empty, and never ``null`` where a string is declared
        (contract Section 1 rule 7 -- a ``null`` loses the whole message).
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
    """
    ...

# From conformance
def check_timestamps(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 3: every timestamp parses as RFC3339-with-``Z``.
    
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
    ...

# From conformance
def check_tracking_stats_shape(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 4: ``tracking_stats`` is zone-keyed and complete.
    
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
    ...

# From conformance
def conformance_errors(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Run all six checks and return every violation found.
    
        Args:
            payload: The candidate wire payload.
            surface: :class:`Surface` or its wire string.
    
        Returns:
            Every :class:`ConformanceError`, in check order.  Empty means the
            payload conforms.
    """
    ...

# From conformance
def conforms(payload: Any[str, Any], surface: Any | str) -> bool:
    """
    Whether ``payload`` passes all six checks.
    """
    ...

# From emit
def build_aggregation(stream_info: Any) -> Any:
    """
    Build and validate one ``results-agg`` message (S1).
    
        Args:
            stream_info: The typed per-stream context (S4).  Supplies every
                envelope identity field, including ``location_id``, which is
                emitted as ``locationId`` (FROZEN-1).
            input_timestamp: The window's event time.  Set **unconditionally** --
                without a root ``input_timestamp`` the backend falls back to "the
                first zone's timestamp", where "first" is Go map iteration order
                and therefore nondeterministic (BE-5).  Accepts anything
                :func:`~...schemas.to_rfc3339z` accepts.
            tracking_stats: Zone id -> :class:`~...schemas.TrackingStats`
                (FROZEN-2: keyed by zone, never flat).  Single-bucket apps use the
                literal key ``"global"``.
            metrics: The window's ``metrics[]`` entries.
    
        Returns:
            A conforming :class:`~...schemas.AggregationResult`.
    
        Raises:
            pydantic.ValidationError: A field is structurally wrong (illegal enum,
                numeric string, bad timestamp).
            ConformanceViolation: The assembled payload fails one of the six
                checks -- most commonly "at least one of tracking_stats / metrics
                must be non-empty", which the backend answers by dropping the
                whole message.
    """
    ...

# From emit
def build_frame_result() -> Any:
    """
    Build and validate the per-frame return value (S3).
    
        py_analytics does not publish this -- it returns a dict and an inference
        worker outside this workspace XADDs it to
        ``<cameraId>_<appDeploymentId>_output_topic``.  We own ``agg_summary`` and
        the detections inside it; the worker stamps everything else.
    
        Three properties are guaranteed here:
    
        * ``agg_summary`` is **keyed by zone** (PY-5).  Today the key is
          ``"<int>"``, ``"None"``, ``"current_frame"`` or a zone name depending
          on the file.  This is a visible behaviour change for three consumers
          and must be announced, not slipped in.
        * Each zone's ``tracking_stats`` carries **all four count lists** (PY-2),
          guaranteed by :class:`~...schemas.FrameTrackingStats` inheriting from
          :class:`~...schemas.TrackingStats`.  Without them be-analytics'
          ``hasTrackingStats`` fails on all seven probe paths and every instant
          metric evaluates against zero.
        * Detections appear **once**, inside the zone that owns them.  There is
          no top-level ``detections`` echo: the duplicate copies are why
          fe-streaming dedupes by bbox string key, a dedupe that silently
          collapses two genuine objects at identical coordinates.
    
        ``agg_summary`` is emitted twice -- nested under ``result.value`` and
        hoisted to the top level -- because consumers probe both paths.  The two
        are the same data by construction.
    
        Args:
            agg_summary: Zone id -> :class:`~...schemas.FrameSummaryEntry`.
            original_fps: Source frame rate, echoed in
                ``result.value.input_streams``.
    
        Returns:
            A conforming :class:`~...schemas.FrameResult`.
    
        Raises:
            pydantic.ValidationError: A field is structurally wrong (e.g. a
                bounding box outside 0-1).
            ConformanceViolation: The assembled payload fails one of the six
                checks.
    """
    ...

# From emit
def build_incident(stream_info: Any) -> Any:
    """
    Build and validate one ``incident_res`` message (S2).
    
        Emit on a severity **transition** only.  The backend does find-or-create
        with up-only escalation: re-sending the same severity is a no-op,
        de-escalation is not representable, and only a non-empty ``end_time``
        closes an incident (contract Section 3.4).
    
        Note the deliberate naming divergence from S1: this surface carries
        ``application_id`` (not ``app_id``) and ``location_name`` (not
        ``location``).  Both are frozen -- they match a different Go DTO.
    
        Args:
            stream_info: The typed per-stream context (S4).
            incidents: One or more :class:`~...schemas.Incident` entries.
            category: ``SAFETY`` / ``QUALITY`` / ``VOLUME`` or ``""`` (untagged).
            frame_id: Legacy Redis frame key; falls back to
                ``stream_info.frame_id``.
            stream_time: Media anchor in the §3.3 format.  A datetime or epoch is
                formatted by :func:`~...schemas.to_stream_time`; a string is
                passed through and validated.  Falls back to
                ``stream_info.stream_time``.
            rtp_number: The frame's RTP timestamp -- the anchor the backend
                resolves the alert thumbnail and the looked-up wall-clock time
                from.  Falls back to ``stream_info.rtp_number``.  Present for the
                same reason ``frame_id`` is: all three are per-frame, and a
                builder that overrode only two invited callers to publish a
                current frame's id beside a stale image anchor.
    
        Returns:
            A conforming :class:`~...schemas.IncidentMessage`.  ``camera_name`` is
            blanked when it equals ``camera_id`` (FROZEN-8).
    
        Raises:
            pydantic.ValidationError: A field is structurally wrong (e.g. a
                severity that is not one of the five lowercase wire values).
            ConformanceViolation: The assembled payload fails one of the six
                checks.
    """
    ...

# From emit
def publish_aggregation(publisher: Any, result: Any) -> None:
    """
    Serialise and publish an ``results-agg`` message.
    
        Re-validates on the way out: :func:`build_aggregation` validated at build
        time, but a model is mutable and this is the last point at which a
        non-conforming payload can be stopped.
    
        Args:
            publisher: The transport.
            result: The message to send.
    
        Raises:
            ConformanceViolation: The payload no longer conforms.
    """
    ...

# From emit
def publish_incident(publisher: Any, message: Any) -> None:
    """
    Serialise and publish an ``incident_res`` message.
    
        Args:
            publisher: The transport.
            message: The message to send.
    
        Raises:
            ConformanceViolation: The payload no longer conforms.
    """
    ...

# From emit
def to_payload(model: Any | Any | Any) -> dict[str, Any]:
    """
    Serialise a contract model to its wire dict.
    
        ``by_alias=True`` is what emits the frozen camelCase names -- ``locationId``
        (FROZEN-1) and ``imageUrl`` (FROZEN-3).  Dumping without it silently
        produces ``location_id``/``image_url``, which breaks ingestion with no
        error anywhere: the row simply arrives with ``_idLocation = ""``.  That is
        the reason this lives in exactly one function.
    
        ``mode="json"`` renders enums as their string values and keeps every
        number JSON-native.  ``exclude_none=True`` guarantees rule 7 -- no
        ``None`` ever reaches the wire (every declared string already defaults to
        ``""``; the only nullable field in the contract is ``detections[].track_id``,
        which is omitted rather than sent as ``null``).
    
        Args:
            model: A validated contract model.
    
        Returns:
            A plain JSON-serialisable dict.
    """
    ...

# From schemas
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

# From schemas
def is_rfc3339z(text: Any) -> bool:
    """
    Whether ``text`` is a well-formed RFC3339-with-``Z`` timestamp.
    """
    ...

# From schemas
def is_stream_time(text: Any) -> bool:
    """
    Whether ``text`` is a well-formed ``stream_time`` value.
    """
    ...

# From schemas
def now_rfc3339z() -> str:
    """
    Current UTC instant as RFC3339 with ``Z``.
    """
    ...

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
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
# From conformance
class ConformanceError:
    # A single named contract violation.
    #
    #     Attributes:
    #         check: The check function that produced it, e.g.
    #             ``"check_required_fields"``.
    #         field: A dotted path to the offending field, e.g.
    #             ``"tracking_stats.global.total_counts"``.  Never empty -- the
    #             whole point is that the message names what is wrong.
    #         message: Human-readable explanation, citing the defect id where one
    #             applies.
    #         surface: The surface the payload was validated against.

    ...

# From conformance
class ConformanceViolation:
    # Raised by :func:`assert_conforms` when a payload does not conform.
    #
    #     Attributes:
    #         surface: The surface validated against.
    #         errors: Every :class:`ConformanceError` found, not just the first --
    #             one malformed zone fails the whole message on the Go side (BE-7),
    #             so it is worth reporting everything at once.

    def __init__(self: Any, surface: Any, errors: Any[Any]) -> None: ...


# From conformance
class Surface:
    # The three outbound surfaces a payload can be validated against.

    frame_result: str
    incident_res: str
    results_agg: str


# From emit
class Publisher:
    # Anything that can put a payload on a named stream.
    #
    #     Intentionally minimal.  **No Redis here** -- transport, connection
    #     management, retry and the ``_message_key`` partitioning hint belong to a
    #     separate workstream.  The contract module's job ends when a validated
    #     dict has been handed over.
    #
    #     Implementations must not mutate ``payload``.

    def publish(self: Any, stream: str, payload: dict[str, Any]) -> None:
        """
        Publish ``payload`` to ``stream``.
        
                Args:
                    stream: :data:`STREAM_RESULTS_AGG` or :data:`STREAM_INCIDENT_RES`.
                    payload: A conforming wire dict from :func:`to_payload`.
        """
        ...


# From schemas
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


# From schemas
class AggregationResult:
    # S1 -- the ``results-agg`` message (contract Section 2).
    #
    #     Emitted once per 60-second window per camera via
    #     ``XADD results-agg {"data": <json>}``.
    #
    #     Field order matches the worked example in contract Section 2.4 so that a
    #     serialised payload is byte-comparable with the spec.

    ...

# From schemas
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

# From schemas
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


# From schemas
class Detection:
    # One detection inside a zone's frame-path ``tracking_stats``.
    #
    #     ``confidence`` is required on purpose: be-media-server rewrites a
    #     confidence of 0 with a non-empty category to 1.0 (BE-12), so an omitted
    #     field is indistinguishable from full confidence in stored playback.

    ...

# From schemas
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

# From schemas
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

# From schemas
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

# From schemas
class Incident:
    # One entry in ``incident_res.incidents[]`` (contract Section 3.2).

    ...

# From schemas
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

# From schemas
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


# From schemas
class InputStreamEntry:
    # Wrapper preserving the pipeline's ``input_streams`` shape.

    ...

# From schemas
class InputStreamInfo:
    # ``input_streams[].input_stream`` -- the pipeline's stream metadata echo.

    ...

# From schemas
class MetricEntry:
    # One entry in ``results-agg.metrics[]``.
    #
    #     Contract Section 2.3.  Lands in ClickHouse as a ``raw_business_metrics``
    #     row.

    ...

# From schemas
class ResultValue:
    # ``result.value`` -- streams plus the zone-keyed summary.

    ...

# From schemas
class ResultWrapper:
    # ``result`` -- the pipeline's envelope around :class:`ResultValue`.

    ...

# From schemas
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


# From schemas
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


# From schemas
class StreamInfoError:
    # A required ``stream_info`` field is missing or unusable.
    #
    #     Contract Section 5: *a missing required field is a startup error, not a
    #     silent default*.  Today an absent ``resolution`` silently disables zone
    #     processing, which presents to an operator as "the numbers are wrong"
    #     rather than "the config is broken".

    def __init__(self: Any, problems: list[str]) -> None: ...


# From schemas
class TrackingCount:
    # ``{"category": "person", "count": 3}`` -- one entry in a count list.
    #
    #     ``category`` here is the **ML class name** (``person``, ``vehicle``, ...),
    #     not an analytics :class:`Category`.  Vocabulary Section 13: it is a free
    #     string with no enum.

    ...

# From schemas
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

# From schemas
class WireSegmentationMask:
    # A detection's mask on the wire, RLE-encoded (contract ``04`` §5.1).
    #
    #     Deliberately narrow: the only shape this engine ever emits or decodes, matching
    #     :func:`~matrice_analytics.engine.primitives.segmentation_area.decode_simple_rle_area`. A
    #     detection whose mask came in as a polygon or a precomputed area (no ``rle`` string) never
    #     gets a wire ``segmentation`` -- this engine does not rasterize/encode one for the wire
    #     (no numpy/cv2, **PY-20**), so there is nothing ready-to-emit to put here.

    ...

# From schemas
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


from . import conformance, emit, schemas