"""Auto-generated stub for module: session."""
from typing import Any

# Constants
logger: Any

# Classes
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

class SessionError:
    # The session cannot run this manifest against this stream.
    #
    #     Always raised at **setup**, never per frame (``09`` §5).  Every condition it covers --
    #     an unimplemented primitive, a missing geometry requirement, a zone name that collides
    #     with the ``global`` bucket -- would otherwise produce a stream of plausible zeros, and a
    #     plausible zero is indistinguishable from a quiet camera.

    ...
