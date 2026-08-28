"""Single per-frame post-processing entrypoint for inference workers.

``PostProcRunner`` is the one SDK seam the ml-codebases inference workers call
per frame. It owns what those workers reimplement today, three times over:

* choosing which implementation serves this app, and constructing it,
* a dedicated, persistent asyncio event loop (one loop per runner instance),
* canonical ``stream_info`` construction (superset of the worker builders),
* driving the ASYNC ``process`` from a SYNC facade, and
* normalizing the ``agg_summary`` unwrap variance into one stable dict shape.

Two implementations, one interface
----------------------------------
An application is either a legacy use case or a manifest app the new engine runs
from an ``app.yaml``. The worker cannot tell which: it calls :meth:`run` and gets
the same dict either way. The choice is made once at construction by
:func:`~matrice_analytics.engine.routing.route_app` and lives in
:mod:`matrice_analytics.runtime.backends`.

Routing is a *positive* gate -- an app goes to the engine only when its manifest
loads and every primitive it names is implemented. Everything else is legacy,
which today means every production app, unchanged and byte-identical. An app
moves by a manifest appearing where routing can find it; it moves back by the
manifest going away, or by ``MATRICE_ANALYTICS_FLOW=old``.

Threading contract
-------------------
A ``PostProcRunner`` owns exactly one event loop and must be used from a single
thread (the per-worker-thread model the pipeline already uses). Do NOT share a
runner or its loop across threads. Create one runner per worker thread.

bbox contract
-------------
The runner does NOT perform letterbox/CUDA-space bbox math -- that depends on
preprocessing parameters the SDK does not hold. Callers must supply detections
already in SOURCE-PIXEL coordinates (the same thing the workers do before
calling ``process`` today). ``PostProcessor`` returns normalized (0-1) nested
detections as it already does. A pure :meth:`normalize_detections` helper is
provided for callers that need to re-normalize analytics-emitted pixel bboxes
given the source dimensions.
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Matches the wall-clock UTC stream-time format the workers build.
_STREAM_TIME_FMT = "%Y-%m-%d-%H:%M:%S.%f UTC"

#: How long a retryably-refused camera is skipped before its readiness is re-tested.
#:
#: Monotonic, not wall clock: this is I/O rate-limiting, not analytics cadence, so PY-13 does not
#: apply -- and monotonic is immune to an NTP step that would otherwise defer a camera for hours.
#: Deliberately shorter than the geometry refresh default so the re-check lands on fresh state
#: rather than repeatedly asking before the resolver has looked again.
_DEFERRED_RECHECK_SECONDS = 60.0

#: How often a camera that keeps failing per-frame post-processing is re-reported.
#:
#: Monotonic and interval-based rather than "every Nth failure", because N is frame-rate
#: dependent: it would log almost never at 1 fps and flood at 30. Mirrors the same choice
#: in ``AnalyticsPublisher._DROP_LOG_INTERVAL_S``.
_PROCESS_FAILURE_LOG_INTERVAL_S = 60.0


def build_stream_info(
    camera_id: str,
    *,
    frame_id: Optional[str] = None,
    rtp_number: Optional[Any] = None,
    stream_time: Optional[str] = None,
    start_frame: Optional[int] = None,
    end_frame: Optional[int] = None,
    original_fps: float = 30.0,
    camera_name: Optional[str] = None,
    camera_group: str = "default",
    location: str = "unknown",
    camera_info: Optional[Dict[str, Any]] = None,
    app_deployment_id: Optional[str] = None,
    application_id: Optional[str] = None,
    application_name: Optional[str] = None,
    application_key_name: Optional[str] = None,
    application_version: Optional[str] = None,
    source_dims: Optional[Tuple[int, int]] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build the canonical ``stream_info`` dict the inference workers construct.

    This is the union/superset of the two ml-codebases builders
    (``yolo_code_base`` legacy + ultralytics, and ``fr_code_base``). It is a
    pure function -- no I/O, no clocks unless ``stream_time`` is omitted.

    Args:
        camera_id: Stream/camera identifier (required).
        frame_id: Per-frame id (e.g. ``shm_<cam>_<n>``). Empty string if absent.
        rtp_number: Per-frame RTP number; coerced to ``str`` (``""`` when falsy).
        stream_time: Pre-formatted stream time. Defaults to current UTC in the
            ``%Y-%m-%d-%H:%M:%S.%f UTC`` format the workers use.
        start_frame / end_frame: Frame window for ``input_settings``. ``end_frame``
            defaults to ``start_frame``; both default to 0.
        original_fps: Source FPS hint for ``input_settings``.
        camera_name: Display name; defaults to ``camera_id``.
        camera_group / location: ``camera_info`` fields (worker defaults kept).
        camera_info: Optional pre-built ``camera_info`` dict; when supplied it is
            used as the base and any missing keys are filled from the args.
        app_deployment_id / application_id / application_name /
        application_key_name / application_version: Identity fields. Only added
            when provided (ultralytics omits them; legacy/FR include them). The
            analytics engine requires all five and refuses a stream without
            them; the legacy flow does not care.
        source_dims: Optional ``(width, height)``; when given adds
            ``stream_resolution`` so downstream consumers can normalize.
        extra: Optional extra top-level keys merged last (caller escape hatch).

    Returns:
        A ``stream_info`` dict matching the worker-built shape.
    """
    if stream_time is None:
        stream_time = datetime.now(timezone.utc).strftime(_STREAM_TIME_FMT)

    if start_frame is None:
        start_frame = 0
    if end_frame is None:
        end_frame = start_frame

    resolved_camera_info: Dict[str, Any] = {
        "camera_id": camera_id,
        "camera_name": camera_name if camera_name is not None else camera_id,
        "camera_group": camera_group,
        "location": location,
    }
    if camera_info:
        # Caller-supplied camera_info wins; fill any gaps from the resolved base.
        merged = dict(resolved_camera_info)
        merged.update(camera_info)
        resolved_camera_info = merged

    stream_info: Dict[str, Any] = {
        "camera_id": camera_id,
        "frame_id": frame_id if frame_id is not None else "",
        "rtp_number": str(rtp_number) if rtp_number else "",
        "stream_time": stream_time,
        "input_settings": {
            "start_frame": start_frame,
            "end_frame": end_frame,
            "original_fps": original_fps,
            "stream_time": stream_time,
            "stream_info": {"stream_time": stream_time},
        },
        "camera_info": resolved_camera_info,
    }

    # Identity fields are only present in the legacy/FR builders; include them
    # only when supplied so the shape stays faithful to each caller.
    #
    # The analytics engine REQUIRES all five (they become the results-agg envelope, and a
    # fabricated default would land in ClickHouse as real identity). It refuses a stream that
    # lacks them, naming each one -- so omitting them is safe for a legacy app and a loud
    # startup error for an engine app, which is the right way round.
    for key, value in (
        ("app_deployment_id", app_deployment_id),
        ("application_id", application_id),
        ("application_name", application_name),
        ("application_key_name", application_key_name),
        ("application_version", application_version),
    ):
        if value is not None:
            stream_info[key] = value

    if source_dims is not None:
        width, height = source_dims
        stream_info["stream_resolution"] = {"width": width, "height": height}

    if extra:
        stream_info.update(extra)

    return stream_info


def _unwrap_agg_summary(result: Any) -> Optional[Dict[str, Any]]:
    """Normalize the agg_summary unwrap variance the workers handle by hand.

    Handles ``.to_dict()``-style results, ``.result``-dict-style results, and
    plain dict ``.data`` payloads. Returns the agg_summary dict or ``None``.
    """
    # .to_dict() style (ProcessingResult).
    to_dict = getattr(result, "to_dict", None)
    if callable(to_dict):
        try:
            d = to_dict()
        except Exception:  # pragma: no cover - defensive
            d = None
        if isinstance(d, dict):
            data = d.get("data")
            if isinstance(data, dict) and "agg_summary" in data:
                return data.get("agg_summary")
            if "agg_summary" in d:
                return d.get("agg_summary")

    # .result dict style.
    res = getattr(result, "result", None)
    if isinstance(res, dict):
        data = res.get("data")
        if isinstance(data, dict) and "agg_summary" in data:
            return data.get("agg_summary")
        if "agg_summary" in res:
            return res.get("agg_summary")

    # Plain .data dict style.
    data = getattr(result, "data", None)
    if isinstance(data, dict) and "agg_summary" in data:
        return data.get("agg_summary")

    return None


def _result_as_dict(result: Any) -> Dict[str, Any]:
    """Return a plain-dict view of a ProcessingResult-like object."""
    to_dict = getattr(result, "to_dict", None)
    if callable(to_dict):
        try:
            d = to_dict()
        except Exception:  # pragma: no cover - defensive
            d = None
        if isinstance(d, dict):
            return d
    res = getattr(result, "result", None)
    if isinstance(res, dict):
        return res
    if isinstance(result, dict):
        return result
    data = getattr(result, "data", None)
    if isinstance(data, dict):
        return {"data": data}
    return {}


def _empty_result() -> Dict[str, Any]:
    """Safe empty result matching the worker fallback tolerance."""
    return {"result": {}, "agg_summary": None}


def _app_reference(app_name: Optional[str], post_processing_config: Any) -> Optional[str]:
    """What to ask routing about: the app's name, or the ``usecase`` it configures.

    ``route_app`` resolves a bare id, a display name, a folder path or a zip URL, so whichever of
    these the worker happened to pass is enough. ``None`` is a legitimate answer -- routing reads
    it as "no manifest", which is the legacy path.
    """
    if app_name:
        return app_name
    if isinstance(post_processing_config, dict):
        usecase = post_processing_config.get("usecase")
        if isinstance(usecase, str) and usecase.strip():
            return usecase.strip()
    return None


class PostProcRunner:
    """Single per-frame post-processing entrypoint for an inference worker.

    Constructs and holds ONE :class:`PostProcessor` and ONE dedicated asyncio
    event loop. Use from a single thread only (see module docstring).
    """

    def __init__(
        self,
        *,
        post_processing_config: Optional[Any] = None,
        app_name: Optional[str] = None,
        index_to_category: Optional[Dict[int, str]] = None,
        target_categories: Optional[List[str]] = None,
        redis_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._app_ref = _app_reference(app_name, post_processing_config)
        self._backend: Optional[Any] = None
        self._backend_error: Optional[str] = None
        # Camera ids whose readiness has been settled, and those settled as UNUSABLE. Both are
        # per-camera because one runner serves every camera its worker owns.
        self._stream_checked: set = set()
        self._refused_cameras: set = set()
        # Cameras refused for a condition that can resolve on its own, and when each was last
        # judged. Separate from `_refused_cameras` because that set is never cleared -- correct
        # for "this stream cannot say how big its frames are", wrong for "the zone has not been
        # drawn yet". See `BackendError.retryable`.
        self._deferred_cameras: Dict[str, float] = {}
        self._deferral_reports: Dict[str, int] = {}
        self._decision: Optional[Any] = None
        # Exact per-camera tallies of per-frame post-processing failures, and when each
        # camera was last reported at WARNING. Counts, not a set of "already seen": a
        # camera that fails forever has to stay visible, and the magnitude is the part
        # that says whether it is one bad frame or every frame. All three are bounded by
        # the camera count of one deployment, so none of them needs eviction.
        self._process_failures: Dict[str, int] = {}
        self._none_results: Dict[str, int] = {}
        self._last_process_failure_log: Dict[str, float] = {}

        self._build_backend(
            post_processing_config=post_processing_config,
            app_name=app_name,
            index_to_category=index_to_category,
            target_categories=target_categories,
            redis_config=redis_config,
        )

        # One persistent loop per runner. Bind it to this (worker) thread the
        # same way the workers do, so any asyncio.get_event_loop() inside the
        # processor resolves to our loop.
        self._loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(self._loop)
        except Exception:  # pragma: no cover - defensive (odd thread states)
            logger.debug("PostProcRunner: could not set thread event loop", exc_info=True)
        self._closed = False

    # -- backend selection -------------------------------------------------
    def _build_backend(self, **kwargs: Any) -> None:
        """Decide once, at construction, which implementation serves this app.

        The decision is :func:`~matrice_analytics.engine.routing.route_app`: a manifest that loads
        and names only implemented primitives routes to the engine; everything else — which today
        is every production app — routes to legacy, exactly as before.

        A legacy decision constructs the ``PostProcessor`` here, as this class always has. An
        engine decision constructs no ``PostProcessor`` at all, which is the point: the legacy
        import chain costs ~3,525 modules and ~49 seconds, and a manifest app should pay none of
        it.
        """
        from ..engine.routing import RoutingError
        from .backends import BackendError, LegacyBackend, select_engine_backend

        try:
            engine = select_engine_backend(
                self._app_ref,
                redis_config=kwargs.get("redis_config"),
                app_name=kwargs.get("app_name"),
                post_processing_config=kwargs.get("post_processing_config"),
            )
        except RoutingError as exc:
            # Only reachable under MATRICE_ANALYTICS_FLOW=new, where a failed gate is meant to be
            # loud rather than a silent fallback. `run` still may not raise, so this becomes one
            # error line plus empty results — which is loud in a log and safe in a pipeline.
            self._backend_error = f"routing refused this app under MATRICE_ANALYTICS_FLOW=new: {exc}"
            logger.error("PostProcRunner: %s", self._backend_error)
            return
        except BackendError as exc:
            # A bundle was configured and no candidate loaded. Deliberately *not* a legacy
            # fallback: this app's analytics live in the bundle, so a legacy run would publish
            # zeros that read as a quiet camera. Same shape as above — one error line, empty
            # results, no exception into the worker loop.
            self._backend_error = f"app bundle could not be loaded: {exc}"
            logger.error("PostProcRunner: %s", self._backend_error)
            return

        self._backend = engine if engine is not None else LegacyBackend(**kwargs)

    # -- introspection -----------------------------------------------------
    @property
    def processor(self) -> Any:
        """A handle callers gate on. **Never ``None`` while a backend exists.**

        On the legacy path this is the real :class:`PostProcessor`. On the engine path it is a
        compatibility shim -- an engine app has no ``PostProcessor`` and deliberately never
        constructs one.

        The distinction matters because callers treat this as "is analytics on?". ``workers.py``
        in ml-codebases reads it once and then gates every frame on
        ``analytics_processor is not None``, so a ``None`` here would silently stop analytics for
        good rather than fail. See :class:`~matrice_analytics.runtime.backends._EngineProcessorShim`.
        """
        return getattr(self._backend, "processor", None)

    @property
    def backend(self) -> Any:
        """The chosen backend, or ``None`` when construction failed."""
        return self._backend

    @property
    def engine(self) -> str:
        """``"engine"``, ``"legacy"``, or ``"unavailable"`` when routing refused the app."""
        return getattr(self._backend, "name", "unavailable")

    @property
    def routing_decision(self) -> Any:
        """The :class:`~matrice_analytics.engine.routing.RoutingDecision`, for diagnostics.

        ``None`` on the legacy path -- routing's answer there is simply "no manifest".
        """
        return getattr(self._backend, "decision", None)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """The dedicated event loop owned by this runner."""
        return self._loop

    # -- stream_info -------------------------------------------------------
    build_stream_info = staticmethod(build_stream_info)
    normalize_detections = None  # set below after the static method is defined

    # -- core --------------------------------------------------------------
    async def run_async(
        self,
        *,
        detections: Any,
        camera_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
        input_bytes: Optional[bytes] = None,
        config: Optional[Any] = None,
        source_dims: Optional[Tuple[int, int]] = None,
        frame_dims: Optional[Tuple[int, int]] = None,
        frame_ts: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Async core: build stream_info if needed, await the backend, unwrap.

        Provided for callers that already own an event loop. ``run`` wraps this.
        Never raises for processing failures -- returns a safe empty result.

        ``frame_ts`` is the media timestamp of this frame, in seconds. Optional, and ignored by
        the legacy flow. The engine has no wall-clock fallback by design (**PY-13**), so when it is
        omitted the engine anchors on ``stream_info["stream_time"]`` instead -- which the runner
        always sets, in the one format the engine parses.
        """
        if stream_info is None:
            stream_info = build_stream_info(camera_id, source_dims=source_dims)
        elif source_dims is not None and "stream_resolution" not in stream_info:
            # An explicit source_dims is the caller's most direct statement of the frame size, so
            # honour it even when they built the stream_info themselves.
            width, height = source_dims
            stream_info = {**stream_info, "stream_resolution": {"width": width, "height": height}}

        if self._backend is None:
            return _empty_result()

        if camera_id in self._refused_cameras:
            # This camera's stream_info was already judged unusable and said so once. Its frames are
            # dropped; every OTHER camera on this runner is unaffected -- see `_check_stream`.
            return _empty_result()

        if camera_id in self._deferred_cameras:
            # Refused for a reason that can fix itself -- missing zone geometry, which is a row in
            # a database somebody is about to correct. Drop this camera's frames cheaply, but
            # re-check periodically so the fix takes effect WITHOUT a container restart. A
            # permanent refusal here would put the restart back.
            if (time.monotonic() - self._deferred_cameras[camera_id]) < _DEFERRED_RECHECK_SECONDS:
                return _empty_result()
            del self._deferred_cameras[camera_id]
            self._stream_checked.discard(camera_id)

        if camera_id not in self._stream_checked:
            # PER CAMERA, not once per runner. A worker builds one runner and pushes every camera it
            # serves through it (`yolo_code_base/inference/workers.py:827`, outside the camera loop),
            # so a single flag would validate whichever camera arrived first and exempt all the
            # rest -- which reads as coverage without being it.
            #
            # Only a DECISIVE frame consumes the check -- see `_check_stream`. An inconclusive one
            # leaves the camera unchecked so the next frame is checked instead.
            decisive, ok, retryable = self._check_stream(stream_info, input_bytes, detections)
            if decisive:
                self._stream_checked.add(camera_id)
            if not ok:
                if retryable:
                    self._deferred_cameras[camera_id] = time.monotonic()
                else:
                    self._refused_cameras.add(camera_id)
                return _empty_result()

        try:
            result = await self._backend.process(
                detections=detections,
                camera_id=camera_id,
                stream_info=stream_info,
                input_bytes=input_bytes,
                config=config,
                frame_ts=frame_ts,
            )
        except Exception as exc:
            # WARNING on first occurrence and at most once a minute after that, DEBUG in
            # between, with an exact count either way. At DEBUG for every frame -- what
            # this did until INF-2606 -- a camera could fail on all of them and log
            # nothing at default level, indistinguishable from a camera nobody walked
            # past. Reporting only the FIRST failure, which is what replaced it, has the
            # same end state: a camera failing 30 times a second for a week still leaves
            # one line, dated to startup, and nothing that says it is still happening.
            self._note_process_failure(self._process_failures, camera_id, "raised", exc)
            return _empty_result()

        if result is None:
            # Same treatment as an exception: a backend returning None on every frame
            # produces no detections and, before this, no visible signal either.
            self._note_process_failure(self._none_results, camera_id, "returned None", None)
            return _empty_result()

        return result

    def _check_stream(self, stream_info: Dict[str, Any], input_bytes: Any, detections: Any) -> Tuple[bool, bool, bool]:
        """Validate the backend against the first frame it sees for a camera. Once, not per frame.

        The first *frame*, not the first stream_info, because two of the three things the engine
        needs can be recovered from the frame itself -- the dimensions live in the JPEG header or
        the image array the worker already hands us.

        **A frame with no detections cannot decide the box question** (INF-2606).
        ``_boxes_look_normalised`` returns ``True`` for an empty list -- a ``for`` over nothing --
        so a pipeline started while the scene was quiet used to *pass* this gate on a boxless
        frame, and every later frame carrying a real box was then rejected deep inside
        ``session.process_frame`` and swallowed per-frame. That is the entire "worked when I
        started it, then stopped" symptom: it worked exactly until something was detected.

        So an **inconclusive** frame -- dimensions unresolvable *and* nothing detected -- is not
        allowed to consume the check. It is let through (it carries no box, so nothing can be
        mis-normalised) and the next frame is checked instead. The first frame that can actually
        answer the question either passes or fails loudly.

        Returns:
            ``(decisive, ok, retryable)``. ``decisive`` is whether this frame settled the
            question, i.e. whether the caller should stop re-checking. ``ok`` is whether to
            process this frame. ``retryable`` says the refusal can lift on its own -- missing
            zone geometry is a database row, not a code path, so the camera must be able to come
            back without a restart.
        """
        from .backends import BackendError, require_engine_ready, resolve_source_dims

        if self.engine != "engine":
            return True, True, False

        enriched = self._backend.enrich(stream_info, input_bytes=input_bytes)
        if resolve_source_dims(enriched, input_bytes) is None and not detections:
            logger.debug(
                "PostProcRunner: app %s -- readiness check deferred, this frame has no "
                "detections and no resolvable dimensions so it cannot decide either way",
                self._backend.app_id,
            )
            return False, True, False

        try:
            require_engine_ready(
                enriched,
                self._backend.app_id,
                input_bytes=input_bytes,
                detections=detections,
                manifest=getattr(self._backend, "manifest", None),
                zone_answer=self._zone_answer(enriched),
            )
        except BackendError as exc:
            # Refuse THIS camera, not the backend. Nulling `self._backend` -- what this did until
            # the per-camera change -- disabled analytics for every camera the runner serves, so one
            # camera with missing geometry took the whole worker's post-processing down with it. The
            # caller records the camera in `_refused_cameras` and drops its frames; the others keep
            # running. `_backend_error` still carries the message for introspection.
            self._backend_error = str(exc)
            retryable = bool(getattr(exc, "retryable", False))
            camera_id = str(stream_info.get("camera_id") or "")
            if not retryable:
                logger.error("PostProcRunner: %s", exc)
            else:
                # Decelerating: ERROR once so it cannot be missed, then INFO while it is still
                # being re-checked, then DEBUG. A camera waiting on a zone somebody has not drawn
                # yet must not fill the log for the rest of the deployment.
                seen = self._deferral_reports.get(camera_id, 0)
                self._deferral_reports[camera_id] = seen + 1
                if seen == 0:
                    logger.error("PostProcRunner: %s", exc)
                elif seen < 3:
                    logger.info("PostProcRunner: still waiting -- %s", exc)
                else:
                    logger.debug("PostProcRunner: still waiting -- %s", exc)
            return True, False, retryable
        return True, True, False

    def _zone_answer(self, stream_info: Dict[str, Any]) -> Any:
        """The backend's geometry verdict for this camera, when it has one.

        Only used to explain a refusal, so a backend without a resolver (the legacy one, or a
        stub in a test) is not an error -- it just means the message carries less detail.
        """
        resolver = getattr(self._backend, "_zone_answer_for", None)
        if resolver is None:
            return None
        try:
            return resolver(stream_info)
        except Exception:  # noqa: BLE001 - diagnosing a refusal must not raise a second one
            return None

    def _note_process_failure(
        self,
        counts: Dict[str, int],
        camera_id: str,
        what: str,
        exc: Optional[BaseException],
    ) -> None:
        """Count a per-frame post-processing failure and report it on an interval.

        An interval rather than "every Nth failure": N is frame-rate dependent, so it
        would log almost never at 1 fps and flood at 30. ``AnalyticsPublisher`` chose an
        interval for the same reason -- see its ``_DROP_LOG_INTERVAL_S``.

        The traceback goes out only with the first report per camera; the re-reports
        carry the running count instead, so a camera failing for hours costs one line a
        minute rather than one stack a minute.
        """
        counts[camera_id] = counts.get(camera_id, 0) + 1
        total = counts[camera_id]
        now = time.monotonic()
        last = self._last_process_failure_log.get(camera_id)
        if last is not None and (now - last) < _PROCESS_FAILURE_LOG_INTERVAL_S:
            logger.debug("PostProcRunner: process() %s for cam=%s: %s", what, camera_id, exc)
            return
        self._last_process_failure_log[camera_id] = now
        logger.warning(
            "PostProcRunner: process() %s for cam=%s: %s (%d failure(s) so far for this "
            "camera; further ones are reported at most every %.0fs)",
            what,
            camera_id,
            exc,
            total,
            _PROCESS_FAILURE_LOG_INTERVAL_S,
            # The exception object, not True/False: `exc_info=False` is stored on the
            # record verbatim rather than normalised to None, and None keeps the
            # re-reports genuinely stack-free.
            exc_info=exc if (exc is not None and last is None) else None,
        )

    @property
    def failure_diagnostics(self) -> Dict[str, Any]:
        """Exact per-camera counts of per-frame post-processing failures.

        Separate from the log so monitoring can alert on a rate rather than scrape
        warnings, and so a throttled log never hides the true magnitude.
        """
        return {
            "process_failures": dict(self._process_failures),
            "process_failures_total": sum(self._process_failures.values()),
            "none_results": dict(self._none_results),
            "none_results_total": sum(self._none_results.values()),
        }

    @property
    def zone_diagnostics(self) -> Dict[str, Any]:
        """Zone geometry state and deferrals, plus the per-frame failure tallies.

        The failure counts are mirrored in here because this property is the only
        surface the workers already poll, so surfacing them needs no caller change.
        """
        backend = getattr(self._backend, "zone_diagnostics", None)
        report: Dict[str, Any] = dict(backend) if isinstance(backend, dict) else {}
        report["deferred_cameras"] = sorted(self._deferred_cameras)
        report["refused_cameras"] = sorted(self._refused_cameras)
        report.update(self.failure_diagnostics)
        return report

    def run(
        self,
        *,
        detections: Any,
        camera_id: str,
        stream_info: Optional[Dict[str, Any]] = None,
        input_bytes: Optional[bytes] = None,
        config: Optional[Any] = None,
        source_dims: Optional[Tuple[int, int]] = None,
        frame_dims: Optional[Tuple[int, int]] = None,
        frame_ts: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Sync facade: drive the async processor on this runner's loop.

        Builds ``stream_info`` if not supplied, runs ``process`` to completion on
        the persistent loop, and returns a STABLE dict:
        ``{"result": <ProcessingResult-as-dict>, "agg_summary": <dict-or-None>}``.

        Does not raise on processing failures or a closed runner -- logs and
        returns a safe empty result, matching the workers' fallback tolerance.
        """
        if self._closed:
            logger.warning("PostProcRunner.run called after close(); returning empty result")
            return _empty_result()

        try:
            return self._loop.run_until_complete(
                self.run_async(
                    detections=detections,
                    camera_id=camera_id,
                    stream_info=stream_info,
                    input_bytes=input_bytes,
                    config=config,
                    source_dims=source_dims,
                    frame_dims=frame_dims,
                    frame_ts=frame_ts,
                )
            )
        except Exception as exc:  # pragma: no cover - run_async already guards
            logger.error("PostProcRunner.run failed for cam=%s: %s", camera_id, exc, exc_info=True)
            return _empty_result()

    def close(self) -> None:
        """Close the backend, then stop and close the owned event loop. Idempotent.

        The backend goes first because the engine flushes its open windows here -- without it the
        last partial window of a stream is never published.
        """
        if self._closed:
            return
        self._closed = True
        if self._backend is not None:
            try:
                self._backend.close()
            except Exception:  # pragma: no cover - defensive; close must not raise
                logger.warning("PostProcRunner: backend close failed", exc_info=True)
        try:
            if self._loop.is_running():
                self._loop.stop()
            if not self._loop.is_closed():
                self._loop.close()
        except Exception:  # pragma: no cover - defensive
            logger.debug("PostProcRunner: error closing loop", exc_info=True)

    def __enter__(self) -> "PostProcRunner":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # -- pure helper -------------------------------------------------------
    @staticmethod
    def _box_is_pixel_space(box: Dict[str, Any]) -> bool:
        """True when any corner of ``box`` is outside the unit square, so it needs scaling.

        **All four corners, not just ``xmin``.** Judging from ``xmin`` alone -- what this
        helper did until INF-2606 -- declares a pixel box hugging the left edge
        (``xmin=0.0, xmax=1900``) already-normalized, passes it straight through, and the
        engine's validator then rejects it: ``_to_detection`` raises on anything outside 0-1
        deliberately, because a pixel box silently treated as normalized is a 1920x error
        nobody notices. ``_boxes_look_normalised`` in :mod:`.backends` has always checked all
        four, so the two helpers disagreed -- and the lax one was the one doing the converting.
        """
        for corner in ("xmin", "ymin", "xmax", "ymax"):
            try:
                if float(box.get(corner, 0)) > 1.5:
                    return True
            except (TypeError, ValueError):
                continue
        return False

    @staticmethod
    def _normalize_detections(detections: Any, source_dims: Tuple[int, int]) -> Any:
        """Normalize pixel-space bboxes to 0-1 given ``source_dims=(width,height)``.

        Pure helper mirroring the workers' re-normalize of analytics-emitted
        nested detections. Only scales bboxes that look like pixel coords (any corner
        beyond the unit square -- see :meth:`_box_is_pixel_space`); already-normalized
        boxes are left untouched, so the helper stays idempotent. Handles both
        ``bounding_box`` and ``bbox`` keys. Returns a new list; the input is not mutated.
        """
        if not detections or not isinstance(detections, (list, tuple)):
            return detections
        width, height = source_dims
        if not width or not height:
            return detections

        out: List[Dict[str, Any]] = []
        for det in detections:
            if not isinstance(det, dict):
                out.append(det)
                continue
            new_det = dict(det)
            for key in ("bounding_box", "bbox"):
                bb = new_det.get(key)
                if isinstance(bb, dict) and "xmin" in bb and PostProcRunner._box_is_pixel_space(bb):
                    # ``.get`` rather than ``[...]``: checking all four corners means a box
                    # can now qualify on ``ymax`` alone, so a partial box must not KeyError.
                    new_det[key] = {
                        "xmin": round(float(bb.get("xmin", 0)) / width, 6),
                        "ymin": round(float(bb.get("ymin", 0)) / height, 6),
                        "xmax": round(float(bb.get("xmax", 0)) / width, 6),
                        "ymax": round(float(bb.get("ymax", 0)) / height, 6),
                    }
            out.append(new_det)
        return out


# Expose normalize_detections both as a module function and a static method.
normalize_detections = PostProcRunner._normalize_detections
PostProcRunner.normalize_detections = staticmethod(PostProcRunner._normalize_detections)
