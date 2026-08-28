"""Auto-generated stub for module: emit."""
from typing import Any, Set

# Constants
logger: Any

# Functions
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

# Classes
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

