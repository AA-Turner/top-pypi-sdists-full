"""Auto-generated stub for module: backends."""
from typing import Any, Dict, Optional, Tuple

from ..engine.contract.schemas import StreamInfoError
from ..engine.manifest.loader import load_app_bundle
from ..engine.manifest.loader import redact_url
from ..engine.publish import RedisStreamPublisher
from ..engine.routing import resolve_flow_mode, route_app
from ..engine.runtime.session import Session
from ..engine.runtime.stream_info import resolve_stream_info
from ..post_processing.post_processor import PostProcessor
from .app_bundle import AppBundleError, resolve_app_bundle_refs
from .app_bundle import POST_PROCESSING_CONFIGS_PATH
from .post_proc_runner import _result_as_dict
from .post_proc_runner import _unwrap_agg_summary
from .post_proc_runner import normalize_detections
from .zone_source import ZoneAnswer
from .zone_source import ZoneGeometryResolver
from .zone_source import merge_zone_configs

# Constants
logger: Any

# Functions
def app_bundle_zone_path(deployment_id: Optional[str]) -> str:
    """
    The URL the geometry lookup used, for an error an operator can act on.
    """
    ...
def legacy_shape_agg_summary(agg_summary: Optional[Dict[str, Any]], stream_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Re-key a zone-keyed engine ``agg_summary`` into the legacy frame-keyed shape (PY-5).
    
        The two shapes are a deliberate, documented divergence
        (:class:`~matrice_analytics.engine.contract.schemas.FrameSummaryEntry`), and the engine's is the
        better one -- it is the only form that works for a multi-zone app. But every consumer was built
        against legacy, so this bridges rather than migrates:
    
        ==========================  ==========================  ==================================
        field                       legacy                      engine
        ==========================  ==========================  ==================================
        top-level key               frame number (``"45507"``)  zone (``"global"``, ``"inside"``)
        ``human_text``              on the frame entry          inside ``tracking_stats``
        ``zone_analysis``           on the frame entry          implicit in the zone keys
        ==========================  ==========================  ==================================
    
        So: the per-zone entries collapse into one frame entry, ``human_text`` is lifted back out,
        ``zone_analysis`` is rebuilt from the zone keys (and mirrored inside ``tracking_stats``, which
        is where legacy puts it too), and ``alerts`` / ``incidents`` / ``business_analytics`` are
        merged. Nothing is dropped: the per-zone view survives in full under ``zone_analysis``.
    
        Returns the input unchanged when the bridge is disabled, when there is nothing to convert, or
        when the payload is already frame-keyed -- so it is idempotent and safe to call twice.
    """
    ...
def normalize_zone_config(zone_config: Any) -> Optional[Dict[str, Any]]:
    """
    A ``zone_config`` with every polygon in the unit square, or ``None`` when it declares none.
    
        The engine's geometry takes normalized zones plus a pixel resolution
        (``SceneGeometry.from_zone_config``), and it **raises** on a coordinate outside 0-1 rather than
        coercing it -- so a polygon that cannot be normalized is dropped here, with a warning, instead
        of being handed over to fail the whole stream.
    
        Public because a worker that already holds its camera's geometry should override the API lookup
        rather than duplicate this conversion -- ``yolo_code_base/inference/workers.py`` does exactly
        that. There is one correct normalization and it lives here.
    """
    ...
def require_engine_ready(stream_info: Optional[Dict[str, Any]], app_id: str) -> None:
    """
    Refuse an engine backend that could never produce a usable frame.
    
        Called once, with the first frame the runner sees, because both of these fail the same way on
        every subsequent one. Swallowed per-frame they are indistinguishable from "the camera saw
        nothing"; raised once here they are a single line naming the fix.
    
        Args:
            manifest: The app's manifest, when the caller has it. Only then can this check the third
                failure -- ``zones.required: true`` with no geometry -- which until now escaped the
                gate entirely and surfaced as a ``SessionError`` swallowed on every frame after one
                WARNING. Keyword-only with a default so external callers keep working unchanged.
            zone_answer: The resolver's verdict for this camera, used only to explain the refusal.
    
        Raises:
            BackendError: With :attr:`~BackendError.retryable` set when the condition can resolve
                without a restart -- geometry appearing is the whole reason that flag exists.
    
                An unusable ``stream_info`` is retryable too, since INF-2606. It was not, and the
                runner's ``_refused_cameras`` set "is never cleared", so a camera whose identity
                was momentarily unresolvable -- a ``post_processing_config`` API answering 401,
                an ``application_version`` the platform had not minted yet -- stayed dead for the
                life of the process even after the cause was fixed. Nothing about a missing field
                says it will still be missing a minute later. Dimensions remain non-retryable:
                that verdict is about this frame's own bytes, not about state elsewhere.
    """
    ...
def resolve_source_dims(stream_info: Dict[str, Any], input_bytes: Any = None) -> Optional[Tuple[int, int]]:
    """
    The frame's ``(width, height)``, from whichever of four places actually has it.
    
        No worker in ml-codebases puts a resolution in ``stream_info`` -- the string
        ``stream_resolution`` does not appear in that repo. But both yolo workers hand us the frame
        itself, so the dimensions are in our hands already; they just have to be looked for. Order:
    
        1. ``stream_info["stream_resolution"]`` -- what :func:`build_stream_info` writes for a caller
           that passed ``source_dims``;
        2. ``input_bytes`` as an image array (``ultralytics_worker.py:507`` passes ``bgr_frames[i]``);
        3. ``input_bytes`` as JPEG (``workers.py:1129``).
    
        ``None`` means none of them had it, and the caller decides what that is worth.
    """
    ...
def select_engine_backend(app_ref: Optional[str]) -> Optional['Any']:
    """
    Route once: an :class:`EngineBackend` for a manifest app, ``None`` for the legacy path.
    
        The single place the new-vs-legacy decision is made, because there are **two** entry points into
        this SDK and they must agree. ``PostProcRunner`` is what the ml-codebases workers call;
        ``PostProcessor.process`` is what py_inference's analytics node calls
        (``transport/analytics/pipeline_message_processor.py`` -> ``process_simple`` -> ``process``).
        An app that routes to the engine from one must route to the engine from the other.
    
        ``None`` is the ordinary answer and means "no manifest" -- which today is every production app.
    
        When the deployment names an **app bundle** (see :mod:`.app_bundle`), the candidates are tried in
        order and the first one that routes to the engine wins. If a bundle is configured and *none* of
        them load, that is a :class:`BackendError`, never a quiet legacy decision: a bundle app has no
        legacy use case behind it, so "fall back to legacy" would mean a worker that runs happily and
        publishes nothing -- indistinguishable, downstream, from a camera with nobody in front of it.
    
        Args:
            identity: Anything else the caller holds that may carry ``application_id`` /
                ``application_version`` -- a ``stream_info``, a job-params map.
            bundle_refs: Pre-resolved candidates; ``None`` resolves them here. For tests.
    
        Raises:
            RoutingError: Only under ``MATRICE_ANALYTICS_FLOW=new``, where a failed gate is meant to be
                loud. In ``auto`` a failure is a legacy decision, not an exception.
            BackendError: A bundle was configured and no candidate could be loaded.
    """
    ...
def source_dims_of(stream_info: Dict[str, Any]) -> Optional[Tuple[int, int]]:
    """
    ``(width, height)`` from a stream_info, or ``None`` when it declares no resolution.
    """
    ...

# Classes
class Backend:
    # What :class:`~matrice_analytics.runtime.PostProcRunner` needs from an implementation.

    def close(self: Any) -> None:
        """
        Release whatever the backend holds. Idempotent.
        """
        ...

    async def process(self: Any) -> Optional[Dict[str, Any]]:
        """
        Handle one frame.
        
                Returns the runner's stable ``{"result": ..., "agg_summary": ...}`` dict, or ``None`` when
                there is nothing to report (the runner turns that into its empty result).
        """
        ...

class BackendError:
    # A backend could not be constructed.
    #
    #     Raised at construction, never per frame. The runner turns it into a logged error and a stream
    #     of empty results, because ``PostProcRunner.run`` must not raise — but the operator gets one
    #     loud line saying why every frame is empty, rather than silence.

    def __init__(self: Any, *args: Any) -> None: ...

class EngineBackend:
    # A manifest app, run by :class:`~matrice_analytics.engine.runtime.session.Session`.
    #
    #     One session per camera, because a session is bound to one stream's geometry and window state.
    #     Sessions are built on first sight of a camera and flushed on :meth:`close`, so the final
    #     partial window is published rather than lost.
    #
    #     Unlike the legacy backend this one **publishes for itself**: ``results-agg`` and
    #     ``incident_res`` leave through the injected publisher inside ``Session``. The per-frame S3
    #     payload is returned instead, for the worker to write to its own output topic.

    def __init__(self: Any, loaded: Any) -> None: ...

    name: str

    def app_id(self: Any) -> str: ...

    def close(self: Any) -> None:
        """
        Flush every open window, then release the publisher. Idempotent.
        """
        ...

    def enrich(self: Any, stream_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill the identity fields the engine requires and the worker did not send.
        
                The engine needs five (``StreamInfo``, all required): ``app_id``, ``app_deployment_id``,
                ``application_name``, ``application_key_name``, ``application_version``. No worker in
                ml-codebases sends the last three -- the strings do not appear in that repo at all -- and
                the legacy flow never needed them.
        
                Three of them the SDK knows *better* than the worker could, because they are properties of
                the manifest it has just loaded, and one arrives as a constructor kwarg. So they are
                derived rather than demanded:
        
                =========================  ==========================================================
                ``application_key_name``   ``manifest.app.id`` -- definitional; it *is* the usecase key
                ``application_version``    ``manifest.app.version`` -- definitional
                ``application_name``       the runner's ``app_name``, which ``py_inference`` sets from
                                           ``job_params["application_name"]``
                ``app_deployment_id``      the post-processing config's ``deployment_id``, which
                                           ``py_inference`` injects into it
                =========================  ==========================================================
        
                **Gaps only.** A value the worker supplied always wins -- this never overwrites. And
                ``app_id`` is deliberately absent from the table: nothing the SDK holds is that id, and
                inventing one would put wrong rows in ClickHouse, which is worse than an empty chart. A
                stream without it is refused by :func:`require_engine_ready`.
        
                ``stream_resolution`` is derived too, and it is not cosmetic. ``StreamInfo`` makes the
                resolution **mandatory the moment ``zone_config`` declares a zone**
                (``_resolution_required_when_zoned``), so a camera that ran fine with no polygons is
                refused outright once one is drawn -- which reads downstream as "this app stopped working
                when we added a zone". :meth:`_resolution_gap_fill` says what it may be derived from.
        """
        ...

    def manifest(self: Any) -> Any:
        """
        The parsed ``app.yaml``.
        
                Exposed so the readiness check can ask whether this app *requires* zones, rather than
                reaching through ``_loaded`` from another module.
        """
        ...

    async def process(self: Any) -> Optional[Dict[str, Any]]: ...

    def processor(self: Any) -> Any:
        """
        A compatibility handle for callers that gate on ``runner.processor``.
        
                See :class:`_EngineProcessorShim`. Never ``None``.
        """
        ...

    def sessions(self: Any) -> Dict[str, Any]:
        """
        The live sessions, keyed by camera id. Introspection for tests.
        """
        ...

    def zone_diagnostics(self: Any) -> Dict[str, Any]:
        """
        Per-camera geometry state: what was found, by which key, and why not otherwise.
        
                "Self-diagnosing" should not mean "grep the logs of a container that has already rolled
                them". A camera publishing nothing is the symptom this exists to explain.
        """
        ...

class LegacyBackend:
    # The path every application takes today: one ``PostProcessor``, awaited per frame.
    #
    #     Lifted from ``PostProcRunner`` unchanged, including the lazy import and the ``redis_config``
    #     forwarding. If this class does anything the old runner did not, that is a bug.

    def __init__(self: Any) -> None: ...

    name: str

    def close(self: Any) -> None:
        """
        The legacy processor owns no resource the runner is expected to release.
        """
        ...

    async def process(self: Any) -> Optional[Dict[str, Any]]: ...

    def processor(self: Any) -> Any: ...

