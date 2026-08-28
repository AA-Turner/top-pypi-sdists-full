"""Auto-generated stub for module: post_proc_runner."""
from typing import Any, Dict, Optional

from ..engine.routing import RoutingError
from .backends import BackendError, LegacyBackend, select_engine_backend
from .backends import BackendError, require_engine_ready, resolve_source_dims

# Constants
logger: Any
normalize_detections: Any

# Functions
def build_stream_info(camera_id: str) -> Dict[str, Any]:
    """
    Build the canonical ``stream_info`` dict the inference workers construct.
    
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
    ...

# Classes
class PostProcRunner:
    # Single per-frame post-processing entrypoint for an inference worker.
    #
    #     Constructs and holds ONE :class:`PostProcessor` and ONE dedicated asyncio
    #     event loop. Use from a single thread only (see module docstring).

    def __init__(self: Any) -> None: ...

    build_stream_info: Any
    normalize_detections: None

    def backend(self: Any) -> Any:
        """
        The chosen backend, or ``None`` when construction failed.
        """
        ...

    def close(self: Any) -> None:
        """
        Close the backend, then stop and close the owned event loop. Idempotent.
        
                The backend goes first because the engine flushes its open windows here -- without it the
                last partial window of a stream is never published.
        """
        ...

    def engine(self: Any) -> str:
        """
        ``"engine"``, ``"legacy"``, or ``"unavailable"`` when routing refused the app.
        """
        ...

    def failure_diagnostics(self: Any) -> Dict[str, Any]:
        """
        Exact per-camera counts of per-frame post-processing failures.
        
                Separate from the log so monitoring can alert on a rate rather than scrape
                warnings, and so a throttled log never hides the true magnitude.
        """
        ...

    def loop(self: Any) -> Any.Any:
        """
        The dedicated event loop owned by this runner.
        """
        ...

    def processor(self: Any) -> Any:
        """
        A handle callers gate on. **Never ``None`` while a backend exists.**
        
                On the legacy path this is the real :class:`PostProcessor`. On the engine path it is a
                compatibility shim -- an engine app has no ``PostProcessor`` and deliberately never
                constructs one.
        
                The distinction matters because callers treat this as "is analytics on?". ``workers.py``
                in ml-codebases reads it once and then gates every frame on
                ``analytics_processor is not None``, so a ``None`` here would silently stop analytics for
                good rather than fail. See :class:`~matrice_analytics.runtime.backends._EngineProcessorShim`.
        """
        ...

    def routing_decision(self: Any) -> Any:
        """
        The :class:`~matrice_analytics.engine.routing.RoutingDecision`, for diagnostics.
        
                ``None`` on the legacy path -- routing's answer there is simply "no manifest".
        """
        ...

    def run(self: Any) -> Dict[str, Any]:
        """
        Sync facade: drive the async processor on this runner's loop.
        
                Builds ``stream_info`` if not supplied, runs ``process`` to completion on
                the persistent loop, and returns a STABLE dict:
                ``{"result": <ProcessingResult-as-dict>, "agg_summary": <dict-or-None>}``.
        
                Does not raise on processing failures or a closed runner -- logs and
                returns a safe empty result, matching the workers' fallback tolerance.
        """
        ...

    async def run_async(self: Any) -> Dict[str, Any]:
        """
        Async core: build stream_info if needed, await the backend, unwrap.
        
                Provided for callers that already own an event loop. ``run`` wraps this.
                Never raises for processing failures -- returns a safe empty result.
        
                ``frame_ts`` is the media timestamp of this frame, in seconds. Optional, and ignored by
                the legacy flow. The engine has no wall-clock fallback by design (**PY-13**), so when it is
                omitted the engine anchors on ``stream_info["stream_time"]`` instead -- which the runner
                always sets, in the one format the engine parses.
        """
        ...

    def zone_diagnostics(self: Any) -> Dict[str, Any]:
        """
        Zone geometry state and deferrals, plus the per-frame failure tallies.
        
                The failure counts are mirrored in here because this property is the only
                surface the workers already poll, so surfacing them needs no caller change.
        """
        ...

