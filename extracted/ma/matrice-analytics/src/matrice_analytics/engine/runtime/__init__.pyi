"""Stub file for engine.runtime directory."""
from typing import Any, List

# Constants
logger: Any = ...  # From session
logger: Any = ...  # From stream_info
logger: Any = ...  # From window

# Functions
# From stream_info
def parse_stream_info(raw: Any[str, Any] | None) -> Any:
    """
    :func:`resolve_stream_info` when the caller only wants the value.
    
        Args:
            raw: The untyped ``stream_info`` dict.
    
        Returns:
            The validated :class:`StreamInfo`.
    
        Raises:
            StreamInfoError: As :func:`resolve_stream_info`.
    """
    ...

# From stream_info
def resolve_stream_info(raw: Any[str, Any] | None) -> Any:
    """
    Parse ``stream_info`` into a validated :class:`StreamInfo`, reporting every fallback.
    
        Args:
            raw: The ``stream_info`` dict the inference worker handed to the session.  ``None``
                or a non-mapping is an error, not an empty default -- a session with no stream
                info has no camera to attribute its numbers to.
    
        Returns:
            The :class:`StreamInfoParse`: the typed value plus where each field came from.
    
        Raises:
            StreamInfoError: A required field (:data:`REQUIRED_FIELDS`) is absent from every
                scope, or the assembled value fails :class:`StreamInfo` validation -- most often
                ``resolution`` missing while ``zone_config`` declares zones, which must fail
                loudly rather than silently disable zone processing (contract §5).
    """
    ...

# From window
def collapse(samples: Any[float], agg_type: Any | str) -> float:
    """
    Collapse per-frame samples with ``agg_type``.
    
        Used for ``custom`` stages **only** -- see the module docstring.  A registered
        primitive's ``window()`` has already aggregated, and applying this on top of it is
        **PY-1**.
    
        Args:
            samples: The per-frame values, in frame order.
            agg_type: The metric's declared aggregation.  ``MetricSpec.agg_type`` is a *string*
                literal while ``MetricEntry.agg_type`` is the :class:`AggType` enum, so both are
                accepted and coerced through :func:`parse_agg_type` -- an ``is`` comparison against
                the enum silently matched nothing when handed the manifest's string, and the
                fall-through published a ``last`` for every metric.
    
        Returns:
            The collapsed value; ``0.0`` for no samples, which reads as "a quiet camera" rather
            than dropping the metric and leaving a gap in the series.
    
        Raises:
            ValueError: ``agg_type`` is not one of the five legal values.  Never a fallback: an
                ``agg_type`` that quietly degrades to ``sum`` is exactly **PY-1**.
    """
    ...

# From window
def collapse_zones(samples: Any[float], how: str) -> float:
    """
    Collapse one metric's per-zone readings into a single number, by ``across_zones``.
    
        Deliberately **not** :func:`collapse`, which collapses a metric over *time* and is selected
        by ``agg_type``. The two axes are independent and a manifest routinely wants different
        answers on each -- ``max_time_in_zone_seconds`` is ``agg_type: last`` (the window's own last
        reading, because ``dwell`` already aggregated it) and ``across_zones: max`` (the worst
        zone). Sharing one function would have forced them together.
    
        Lives here rather than in ``session.py`` because both surfaces now need it -- the flat
        per-frame ``result['metrics']`` map and ``zone: collapsed`` on ``results-agg`` -- and a key
        that meant one thing per frame and another per window would be worse than either.
    
        *samples* is never empty: the caller drops a metric no zone resolved rather than collapsing
        nothing into a ``0`` (``09`` §3).
    """
    ...

# From window
def derived_plan(manifest: Any) -> tuple[Any, ...]:
    """
    Resolve every ``derived[].expr`` against the pipeline, once.
    
        Uses the loader's own function
        (:func:`~matrice_analytics.engine.manifest.models.resolve_derived`), so the scope the
        runtime evaluates in is by construction the scope the manifest validated -- and an operand
        that does not resolve raises here exactly as it would at load, rather than becoming a
        metric that reads zero forever (``09`` §3).
    
        Raises:
            ValueError: An operand does not resolve, or the declared scope is impossible.  It
                cannot happen for a manifest that came through the loader
                (:meth:`AppManifest._check_derived` already ran) but a manifest built in Python
                can skip that.
    """
    ...

# From window
def human_text_for(counts: Any[str, int]) -> str:
    """
    A display string for a zone, e.g. ``"3 person, 1 vehicle"``.
    
        Display only: nothing parses this, and be-analytics reads the count lists rather than the
        text.  Deliberately not pluralised -- "3 persons" and "3 people" are both wrong for some
        entity name, and an entity name is whatever the app author mapped, so the count and the
        name are given unchanged.
    """
    ...

# From window
def metric_plan(manifest: Any) -> tuple[Any, ...]:
    """
    Resolve every ``metrics[].source`` against the pipeline, once.
    
        Raises:
            ValueError: A source does not resolve.  It cannot happen for a manifest that came
                through the loader -- :meth:`AppManifest._check_metric_sources` already ran -- but
                a manifest built in Python can skip that, and an unresolvable source must be an
                error rather than a metric that reads zero forever (``09`` §3).
    """
    ...

# From window
def stage_key_map(manifest: Any) -> dict[str, str]:
    """
    Map every name a ``metrics[].source`` may use onto the real stage name.
    
        ``resolve_source`` accepts a stage's ``name:`` *or* its primitive name while that is
        unambiguous, so ``source: custom.served`` resolves against a stage named ``queue``.  The
        pipeline outputs are keyed by stage name only, so the two have to be joined here -- with
        the same rule ``manifest.resolve_source`` uses, or a metric would validate at load and
        fail to resolve at runtime.
    """
    ...

# Classes
# From session
class FrameOutcome:
    # Everything one frame produced, for the caller and for tests.

    def payload(self: Any) -> dict[str, Any]:
        """
        The S3 return dict, or ``{}`` when frame summaries are switched off.
        
                py_analytics does **not** publish this: it returns it, and an inference worker outside
                this workspace XADDs it to ``<cameraId>_<appDeploymentId>_output_topic``.  We own
                ``agg_summary`` and the detections inside it and nothing else in that envelope
                (backlog **Q5**).
        """
        ...


# From session
class Session:
    # One camera running one app.
    #
    #     Built once per ``(camera, app deployment)`` and fed frames in order.  Everything that can
    #     fail because of a bad manifest/installation combination fails in the constructor:
    #     unimplemented primitives, missing zone or line geometry, a zone name that collides with
    #     the ``global`` bucket, an incident rule that could never fire.
    #
    #     Example:
    #         >>> from matrice_analytics.engine.manifest.loader import load_app_bundle
    #         >>> app = load_app_bundle("apps/people_counting")           # doctest: +SKIP
    #         >>> session = Session.from_loaded_app(app, stream_info)     # doctest: +SKIP
    #         >>> outcome = session.process_frame(detections, frame_ts=1_700_000_000.0)
    #         >>> outcome.aggregation is None      # no window boundary yet    # doctest: +SKIP
    #         True

    def __init__(self: Any, manifest: Any, stream: Any) -> None:
        """
        Build the pipelines for every zone this app runs in.
        
                Args:
                    manifest: The validated manifest, from
                        :func:`~matrice_analytics.engine.manifest.loader.load_app`.
                    stream: The typed input (surface S4).  Use
                        :func:`~matrice_analytics.engine.runtime.stream_info.parse_stream_info` to get
                        one from the worker's untyped dict, so the fallbacks it took are logged.
                    state: The root state scope.  Defaults to a fresh
                        :class:`~matrice_analytics.engine.state.memory.InMemoryStateStore`; pass one in
                        to share a backing between sessions or to assert on keys in a test.
                    clock: The session's clock.  Defaults to a
                        :class:`~matrice_analytics.engine.primitives.base.FrameClock`, which advances
                        only when a frame says so -- never ``time.time()`` (**PY-13**).
                    registry: Primitive registry.  Defaults to the process-wide
                        :data:`~matrice_analytics.engine.primitives.base.REGISTRY`.
                    custom: ``stage name -> CustomImpl`` from
                        :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle`.  Required
                        when the pipeline declares a ``custom`` stage: the manifest can name one, but
                        only the loader can import it.
                    publisher: Where ``results-agg`` and ``incident_res`` go.  ``None`` means the
                        session builds and validates payloads and hands them back on
                        :class:`FrameOutcome` without publishing -- which is exactly what a test wants.
                    started_at: Process/session start, epoch seconds, used as every zone's
                        ``reset_timestamp`` (**FROZEN-4**: totals mean "since this instant").  Defaults
                        to the first frame's timestamp.
        
                Raises:
                    SessionError: The manifest cannot be run against this stream.
        """
        ...

    def buckets(self: Any) -> tuple[str, ...]:
        """
        Every bucket a pipeline runs in: ``global`` first, then the zones.
        """
        ...

    def emission_zones(self: Any) -> tuple[str, ...]:
        """
        The zones that appear in ``tracking_stats`` / ``agg_summary`` (**PY-5**).
        """
        ...

    def flush(self: Any) -> Any | None:
        """
        Close a partial window at the end of a stream.
        
                Returns:
                    The ``results-agg`` message for the frames observed since the last boundary, or
                    ``None`` when no frame has arrived since (or when the window is empty and
                    ``emit_empty_windows`` is false).
        """
        ...

    def from_loaded_app(cls: Any, app: 'Any', stream_info: Any[str, Any] | Any | None, **kwargs: Any) -> 'Session':
        """
        Build a session from a loaded app bundle and the worker's raw ``stream_info``.
        
                The whole chain from ``STAGE_BC_PLAN`` §4 in one call::
        
                    load_app_bundle(ref) -> Session.from_loaded_app(app, stream_info)
                                         -> session.process_frame(detections, frame_ts=...)
        
                Args:
                    app: What :func:`~...loader.load_app_bundle` returned -- its ``manifest`` and its
                        already-imported ``custom`` implementations.
                    stream_info: The untyped worker dict (parsed and logged by
                        :func:`~...runtime.stream_info.resolve_stream_info`) or an already-typed
                        :class:`StreamInfo`.
                    **kwargs: Passed through to :class:`Session`.
        
                Returns:
                    The ready session.
        
                Raises:
                    StreamInfoError: A required ``stream_info`` field is missing.
                    SessionError: The manifest cannot be run against this stream.
        """
        ...

    def geometry(self: Any) -> Any:
        """
        The camera's geometry, resolved to pixels **once**, here (**PY-7**).
        """
        ...

    def manifest(self: Any) -> Any: ...

    def process_frame(self: Any, detections: Any[Any]) -> Any:
        """
        Run one frame through every bucket's pipeline.
        
                Args:
                    detections: This frame's detections.  Accepts
                        :class:`~matrice_analytics.engine.primitives.base.PipelineDetection`,
                        :class:`~matrice_analytics.engine.contract.schemas.Detection`, or the plain
                        dicts the pipeline actually sends (see :func:`_to_detection` for the spellings
                        accepted).  Bounding boxes are **normalized 0-1** (contract §4).
                    frame_ts: The frame's real timestamp, epoch seconds.  Omit it only when
                        ``stream_time`` (here or on the stream) carries the media anchor -- there is
                        no fallback to ``time.time()``, because that fallback is **PY-13**.
                    frame_id: This frame's media key, if it changes per frame.
                    stream_time: This frame's media anchor in the §3.3 format.
                    rtp_number: This frame's RTP timestamp, the anchor the media server resolves the
                        alert image from.  Per frame like the two above, **not** per session: left at
                        the session's first value every incident on the camera resolves to the same
                        thumbnail and the same looked-up wall-clock time.
        
                Returns:
                    The :class:`FrameOutcome`.
        
                Raises:
                    SessionError: A detection cannot be read, or no frame timestamp is available.
                    ValueError: ``frame_ts`` goes backwards -- :class:`FrameClock` refuses to reopen a
                        window it already published.  Drop the frame, or reset the clock explicitly.
        """
        ...

    def stage_names(self: Any) -> tuple[str, ...]:
        """
        Stage names in pipeline order -- the keys of ``ctx.previous``.
        """
        ...

    def stream(self: Any) -> Any:
        """
        The typed per-camera input.  Passed into every :class:`FrameContext`.
        """
        ...

    def window(self: Any) -> Any:
        """
        The open aggregation window.
        """
        ...


# From session
class SessionError:
    # The session cannot run this manifest against this stream.
    #
    #     Always raised at **setup**, never per frame (``09`` §5).  Every condition it covers --
    #     an unimplemented primitive, a missing geometry requirement, a zone name that collides
    #     with the ``global`` bucket -- would otherwise produce a stream of plausible zeros, and a
    #     plausible zero is indistinguishable from a quiet camera.

    ...

# From stream_info
class FieldSource:
    # Where one field's value came from.
    #
    #     Attributes:
    #         field: The canonical field name, e.g. ``"camera_name"``.
    #         path: The dotted path it was read from -- ``""`` for the root dict,
    #             ``"input_settings.stream_config"`` for a nested scope, or a named repair such as
    #             ``"topic"``.  Combined with :attr:`alias` this is enough to reproduce the lookup.
    #         alias: The key that actually held it, e.g. ``"cameraName"``.
    #         fallback: ``True`` when this was *not* the canonical spelling at the root scope --
    #             i.e. when the input drifted from what the contract declares.

    def where(self: Any) -> str:
        """
        Human-readable ``path.alias``, for a log line or an error message.
        """
        ...


# From stream_info
class StreamInfoParse:
    # A validated :class:`StreamInfo` plus the audit trail of how it was found.
    #
    #     The audit trail is the whole point of this module: it turns "the input shape drifted"
    #     from an invisible condition into :attr:`fallbacks`, which a caller can log once per
    #     session, assert on in a test, or surface on a health endpoint.

    def describe(self: Any) -> str:
        """
        One line per fallback, suitable for a log or a test failure message.
        """
        ...

    def fallbacks(self: Any) -> tuple[Any, ...]:
        """
        The subset of :attr:`sources` that did not come from the canonical root key.
        """
        ...


# From window
class AggregationWindow:
    # One camera's open aggregation window.
    #
    #     Owned by :class:`~matrice_analytics.engine.runtime.session.Session`, which feeds it every
    #     frame and asks it, on the frame clock, whether the window is due.  The window does not
    #     call the primitives -- the session owns those -- so :meth:`build` is handed the
    #     :class:`WindowOutput` map it needs.  That split keeps this class testable with plain
    #     dicts and keeps "who owns the primitives" answered once.
    #
    #     Example:
    #         >>> window = AggregationWindow(manifest, stream, clock, state,      # doctest: +SKIP
    #         ...                            emission_zones=("global",))
    #         >>> window.observe(1_700_000_000.0, {"global": outputs}, {"global": detections})
    #         >>> window.is_due()
    #         False

    def __init__(self: Any, manifest: Any, stream: Any, clock: Any, state: Any) -> None:
        """
        Open a window for one camera.
        
                Args:
                    manifest: The validated app manifest.  ``emission.window_seconds`` sets the
                        cadence and ``emission.emit_empty_windows`` decides whether a silent window
                        publishes.
                    stream: The typed :class:`~matrice_analytics.engine.contract.schemas.StreamInfo`;
                        supplies every S1 envelope identity field and ``original_fps``.
                    clock: The session's clock.  A
                        :class:`~matrice_analytics.engine.primitives.base.FrameClock` in production
                        and in replay (**PY-13**); ``WallClock`` only where wall-clock is genuinely
                        meant.
                    state: The session's **root** scope.  ``end_window()`` is called on it, so it
                        must be the scope that contains every primitive's subtree.
                    emission_zones: The zones that appear in ``tracking_stats`` -- the drawn zones
                        for a zoned app, else ``("global",)``.  Never both: a payload carrying zone
                        series *and* a ``global`` series double-counts in any dashboard that sums
                        zones.
                    reset_timestamp: RFC3339 instant at which this camera's cumulative counters last
                        reset, i.e. process start (**FROZEN-4**).  Writable afterwards: the session
                        anchors it to the *first frame* rather than to its own construction, because a
                        session built minutes before the stream starts would otherwise claim a reset
                        that no counter was affected by.
        """
        ...

    def build(self: Any, zone_window_outputs: Any[str, Any[str, Any]]) -> Any | None:
        """
        Build the ``results-agg`` message for the closing window.
        
                Args:
                    zone_window_outputs: ``zone -> stage -> WindowOutput``, from the session calling
                        each primitive's ``window()``.  Values are used **as-is** (§6b coupling 4).
        
                Returns:
                    The validated :class:`AggregationResult`, or ``None`` when the window is empty
                    and ``emission.emit_empty_windows`` is false.
        
                Raises:
                    ValueError: The window is not open -- there is nothing to publish, and silently
                        returning ``None`` would hide a caller bug behind the same value that means
                        "deliberately empty".
                    ConformanceViolation: The assembled payload fails one of the six checks.
        """
        ...

    def counters_for(self: Any, zone: str) -> Any:
        """
        This zone's :class:`ZoneCounters`, created and loaded on first use.
        
                Public because the **frame** surface needs the same four count lists as the window
                surface (**PY-2**), from the same numbers.  The session reads them from here rather
                than maintaining a second set, which is how the frame path and the window path came to
                disagree in the first place.
        """
        ...

    def frames_for(self: Any, zone: str, stage: str) -> tuple[Any, ...]:
        """
        The per-frame outputs retained for one stage in one zone, in frame order.
        
                This is what the session passes to ``primitive.window(frames)``.
        """
        ...

    def is_due(self: Any, now: float | None = None) -> bool:
        """
        Whether ``window_seconds`` have elapsed **on the frame clock** (**PY-13**).
        
                Args:
                    now: Override the clock, for tests.  Production passes nothing: the session
                        advances the :class:`FrameClock` from ``frame_ts`` and this reads it, which
                        is what makes a replayed hour produce the live run's windows.
        """
        ...

    def is_open(self: Any) -> bool:
        """
        Whether at least one frame has been observed since the last boundary.
        """
        ...

    def last_ts(self: Any) -> float:
        """
        Frame timestamp of the most recent frame.
        """
        ...

    def observe(self: Any, frame_ts: float, zone_outputs: Any[str, Any[str, Any]], zone_detections: Any[str, Any[Any]]) -> None:
        """
        Fold one frame's per-zone results into the open window.
        
                The first frame **opens** the window, and its timestamp -- not the process start --
                is the window's origin.  A camera that starts publishing at 00:00:37 gets its first
                boundary at 00:01:37, not a 23-second stub, and a replay of the same footage gets the
                same boundaries (**PY-13**).
        
                Args:
                    frame_ts: This frame's time, epoch seconds.
                    zone_outputs: Each bucket's per-stage output for this frame.
                    zone_detections: Each bucket's detections for this frame.
                    stream: This frame's stream context.  When given, the window **re-anchors** its
                        S1 envelope to it, so the published ``rtp_number`` names a frame this window
                        actually contains rather than the one the session was constructed from.  The
                        identity fields are the same object either way -- only the media anchors move
                        -- and :meth:`build` already publishes ``input_timestamp`` from the last
                        observed frame, so this makes the two agree.  ``None`` leaves the anchor
                        alone, which is what a caller that has no per-frame stream wants.
        """
        ...

    def rollover(self: Any) -> None:
        """
        Close the window: carry the tail forward, then clear WINDOW state.
        
                Order matters.  :meth:`ZoneCounters.rollover` writes the carry values the next
                window's ``total_current_counts`` needs (**PY-4**) *before*
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window` runs, and it
                writes them ``PERSISTENT`` so the clear cannot take them with it.
        
                ``end_window()`` on the session's root scope is the one call that clears every
                primitive's window-scoped keys -- peaks, per-window sums, "new this window" -- and
                cannot touch a cumulative total, because the lifetime was declared at write time
                (``09`` §4 rule 2).  ``clear()`` here would be the bug that whole design prevents.
        """
        ...

    def start_ts(self: Any) -> float | None:
        """
        Frame timestamp of the first frame in this window, or ``None``.
        """
        ...


# From window
class DerivedOperand:
    # One ``<stage>.<value>`` operand of a derived expression, joined to the pipeline.

    ...

# From window
class DerivedPlan:
    # One ``derived[]`` entry, parsed and joined to the pipeline, ready to evaluate.
    #
    #     Built once at session setup: the parse and the stage join are pure manifest arithmetic,
    #     and a 25fps stream across six buckets is the wrong place to be re-parsing a string.

    def window_aggregated(self: Any) -> bool:
        """
        ``True`` when this value must be published **as-is** (**PY-1**, §6b coupling 4).
        """
        ...


# From window
class MetricPlan:
    # One declared metric, joined to the stage and value name that produce it.
    #
    #     Resolved once at setup rather than per window (or, in the session, per frame): the join is
    #     pure manifest arithmetic and doing it on the hot path is the kind of cost that only shows
    #     up at 25 fps across six buckets.

    ...

# From window
class ZoneCounters:
    # The four count lists for one zone, maintained frame by frame.
    #
    #     All four are always emitted (**FROZEN-5**) even though ``current_new_counts`` and
    #     ``total_counts`` are ignored on the backend's main ingestion path: the instant-metric
    #     formula path and ``dataField`` resolution read them, and on the frame surface their
    #     absence is **PY-2** -- ``hasTrackingStats`` fails on all seven probe paths and every
    #     instant metric evaluates against zero.
    #
    #     **The same four names mean different things on the two surfaces, because the two
    #     surfaces are read by different consumers (BE-16).**  There are therefore two builders:
    #     :meth:`window_count_lists` for S1 and :meth:`count_lists` for S3.  Both read the same
    #     four quantities; they differ only in which quantity ``current_counts`` carries.
    #
    #     :meth:`window_count_lists` -- **S1**, ``results-agg``, once per window:
    #
    #     ==========================  =======================================================
    #     List                        What this class puts in it
    #     ==========================  =======================================================
    #     ``current_counts``          per-entity uniques **first seen during this window** --
    #                                 an arrival *delta*, because it lands in
    #                                 ``raw_analytics.count`` and the backend's rollup sums it
    #     ``current_new_counts``      the same arrivals.  On a window surface "new in this
    #                                 window" and "the window's arrival delta" are one number
    #     ``total_counts``            per-entity uniques since process start (FROZEN-4)
    #     ``total_current_counts``    previous window's last-frame count + this window's new
    #                                 arrivals (**PY-4**: *not* a copy of ``current_counts``)
    #     ==========================  =======================================================
    #
    #     :meth:`count_lists` -- **S3**, the per-frame return value:
    #
    #     ==========================  =======================================================
    #     ``current_counts``          the **last observed frame's** per-entity count -- a level
    #     ``current_new_counts``      per-entity uniques first seen during this window
    #     ``total_counts``            per-entity uniques since process start (FROZEN-4)
    #     ``total_current_counts``    the same occupancy carry as S1
    #     ==========================  =======================================================
    #
    #     **Why ``current_counts`` differs (BE-16).**  ``raw_analytics`` is a *delta plus level*
    #     schema: each row says how many arrived since the previous reading (``count``) and how
    #     many were there at the reading (``totalCount``), and the five-minute rollup is
    #     ``argMin(totalCount, t) + sum(count) - argMin(count, t)``
    #     (``10_aggregated_analytics_totals_schema.sql:7``).  Put a level in ``count`` and that
    #     sum adds up occupancy readings: on the six-window sequence in
    #     ``tests/unit/engine/test_runtime_window.py::TestTheBackendRollupFormula`` it publishes
    #     **28 people through a shop that ten walked through**.  The legacy engine already got
    #     this right on its default path -- ``legacy_analytics_bridge:2811`` sets
    #     ``current_counts = window_new_sum``.  S3 has no interval to take a delta over, and
    #     be-analytics' instant-metric extractor reads its ``current_counts`` as
    #     ``total_count``/``category_total_count``, i.e. "how many objects right now"
    #     (``tracker_clickhouse_service.go:1097-1120``) -- so there the level is correct and must
    #     stay.
    #
    #     ``current_counts``, ``current_new_counts`` and ``total_counts`` all come from a
    #     ``unique_count`` stage's ``per_category.<entity>`` values -- the only stage that knows
    #     what "distinct" means.  An app without one publishes zero arrivals rather than guessing:
    #     a per-frame count summed over a window is not a unique count, and publishing it as one
    #     is the error this whole engine exists to stop.  :meth:`AggregationWindow.build` says so
    #     out loud, once, because on S1 that also means the app has no volume series.

    def __init__(self: Any, zone: str, entities: Any[str]) -> None: ...

    def count_lists(self: Any) -> dict[str, list[Any]]:
        """
        The four count lists for the **frame** surface (S3), ready for
                :class:`~matrice_analytics.engine.contract.schemas.FrameTrackingStats`.
        
                ``current_counts`` is the frame's *level* here, deliberately: be-analytics'
                instant-metric ``dataField`` resolution reads it as ``total_count`` /
                ``category_total_count``, i.e. "how many objects right now"
                (``tracker_clickhouse_service.go:1097-1120``).  A frame is an instant, so there is
                no interval for an arrival delta to be a delta *over*.  The window surface is the
                one that needs the delta -- :meth:`window_count_lists`.
        
                ``total_current_counts`` is the occupancy-carry formula (``_occupancy_carry``) UNLESS
                a stage published an explicit live snapshot (``live_category.*``) this frame, in which
                case it is the same reading as ``current_counts``, verbatim. The carry formula answers
                "what should the backend's rollup treat as the running level", which presupposes
                ``current_counts`` means "arrivals" -- not true here, where it means "how many are in
                this live category right now" and there is nothing to carry across a window boundary.
        """
        ...

    def current(self: Any) -> Any[str, int]:
        """
        The last observed frame's per-entity counts.
        """
        ...

    def load(self: Any, state: Any) -> None:
        """
        Read the two cross-window values from the store.
        """
        ...

    def new(self: Any) -> Any[str, int]:
        """
        Per-entity uniques first seen during this window -- the arrival delta.
        """
        ...

    def observe(self: Any, detections: Any[Any], outputs: Any[str, Any]) -> None:
        """
        Fold one frame in.
        
                Args:
                    detections: This zone's detections for the frame, after entity remapping.
                    outputs: This zone's stage outputs for the frame, keyed by stage name.  Scanned
                        for ``per_category.<entity>`` values rather than for a stage literally named
                        ``unique_count``, because a manifest may run it under its own ``name:``.
        """
        ...

    def rollover(self: Any, state: Any) -> None:
        """
        Carry this window's tail into the next one (**PY-4**) and rebase ``new``.
        
                Both writes are :attr:`~matrice_analytics.engine.state.store.Lifetime.PERSISTENT`:
                they are facts about the window that just closed, and ``end_window()`` is about to
                delete everything that is a measurement *of* it.
        """
        ...

    def saw_anything(self: Any) -> bool:
        """
        Whether any detection was counted in this window (drives ``emit_empty_windows``).
        """
        ...

    def window_count_lists(self: Any) -> dict[str, list[Any]]:
        """
        The four count lists for the **window** surface (S1), ready for
                :class:`~matrice_analytics.engine.contract.schemas.TrackingStats`.
        
                ``current_counts`` is this window's **arrival delta** (**BE-16**).  It lands in
                ``raw_analytics.count``, which the backend sums; a level there makes the
                five-minute rollup add up occupancy readings and publish several times the true
                footfall.  See the class docstring for the arithmetic.
        
                ``current_counts`` and ``total_current_counts`` are built over **one shared key
                set**, because the ingest mapper iterates ``current_counts`` and looks each
                category up in ``total_current_counts`` (``tracker_clickhouse_service.go:659-679``):
                a category missing from the first list drops its occupancy carry on the floor.  An
                entity that is zero in *both* is left out entirely -- there is nothing to say about
                it, and a twenty-class model would otherwise write twenty empty rows a minute.
        """
        ...

    def zone(self: Any) -> str: ...


from . import session, stream_info, window