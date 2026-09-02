"""Stub file for runtime directory."""
from typing import Any, Dict, List, Optional, Tuple

from ..engine.contract.schemas import StreamInfoError
from ..engine.manifest.loader import load_app_bundle
from ..engine.manifest.loader import redact_url
from ..engine.publish import RedisStreamPublisher
from ..engine.routing import RoutingError
from ..engine.routing import resolve_flow_mode, route_app
from ..engine.runtime.session import Session
from ..engine.runtime.stream_info import resolve_stream_info
from ..post_processing.post_processor import PostProcessor
from .app_bundle import AppBundleError, resolve_app_bundle_refs
from .app_bundle import POST_PROCESSING_CONFIGS_PATH
from .app_bundle import _open_session
from .app_bundle import fetch_post_processing_config_by_camera_and_app
from .app_bundle import fetch_post_processing_configs
from .backends import BackendError, LegacyBackend, select_engine_backend
from .backends import BackendError, require_engine_ready, resolve_source_dims
from .backends import _declared_resolution, normalize_zone_config
from .post_proc_runner import _result_as_dict
from .post_proc_runner import _unwrap_agg_summary
from .post_proc_runner import normalize_detections
from .zone_source import ZoneAnswer
from .zone_source import ZoneGeometryResolver
from .zone_source import merge_zone_configs

# Constants
ACTION_DETAILS_PATH: str = ...  # From app_bundle
APPLICATION_VERSION_PATH: str = ...  # From app_bundle
APP_DEPLOYMENT_PATH: str = ...  # From app_bundle
ENV_ACTION_ID: str = ...  # From app_bundle
ENV_ACTION_ID_BARE: str = ...  # From app_bundle
ENV_ALLOW_PUBLISHED_VERSION: str = ...  # From app_bundle
ENV_API_BASE: str = ...  # From app_bundle
ENV_BUNDLE_REF: str = ...  # From app_bundle
ENV_LICENSE_KEY: str = ...  # From app_bundle
ENV_SELF_MINT: str = ...  # From app_bundle
LICENSE_KEY_HEADER: str = ...  # From app_bundle
POST_PROCESSING_CONFIGS_PATH: str = ...  # From app_bundle
POST_PROCESSING_CONFIG_BY_CAMERA_APP_PATH: str = ...  # From app_bundle
USECASE_DOWNLOAD_LICENSE_PATH: str = ...  # From app_bundle
USECASE_DOWNLOAD_PATH: str = ...  # From app_bundle
logger: Any = ...  # From app_bundle
logger: Any = ...  # From backends
logger: Any = ...  # From post_proc_runner
normalize_detections: Any = ...  # From post_proc_runner
LOOKUP_FALLBACK_ENV: str = ...  # From zone_source
MAX_BACKOFF_ENV: str = ...  # From zone_source
REFRESH_SECONDS_ENV: str = ...  # From zone_source
logger: Any = ...  # From zone_source

# Functions
# From app_bundle
def backend_base_url(env: Optional[Any[str, str]] = None) -> str:
    """
    The backend's own address, for a route the session's base URL will not serve.
    
        Deployments set ``MATRICE_BASE_URL`` to a local gateway (``http://localhost``). That gateway
        proxies the route prefixes it knows -- ``/v1/inference/*`` among them, which is why
        ``PostProcessingConfigClient`` has always worked -- and 302s anything else out to the real
        backend. ``matrice_common``'s client has ``follow_redirects=True``, and httpx drops the
        ``Authorization`` header when a redirect crosses origin, so a redirected call arrives
        unauthenticated and be-application answers 404. Observed in production on 0.1.428:
        ``http://localhost/v1/applications/.../usecase/download`` -> 302 -> prod -> 404, while the same
        path with a direct base URL returns 200.
    
        Derived the same way ``matrice_common`` derives its own default, so an on-prem or non-prod
        deployment still lands on its own backend; ``$MATRICE_APP_BUNDLE_API_BASE`` overrides it.
    """
    ...

# From app_bundle
def config_get(config: Any, keys: Any[str]) -> Optional[str]:
    """
    First non-empty string among ``keys``, from a dict or an attribute-bearing object.
    
        Both shapes are real and this is why the function exists: ``PostProcRunner`` passes the raw
        ``post_processing_config`` dict, while ``PostProcessor`` passes a *parsed* config object. A
        dict-only reader -- which is what ``backends._config_value`` is -- would make the two SDK entry
        points disagree about whether an app has a bundle, and keeping them in agreement is the entire
        reason ``select_engine_backend`` is a single function.
    """
    ...

# From app_bundle
def fetch_action_job_params(action_id: str) -> Dict[str, Any]:
    """
    ``jobParams`` off this worker's action record.
    
        For a ``deploy_add`` action this holds ``application_version`` and ``application_id`` as the
        platform resolved them when it launched the container -- so it is the *deployed* pair, not a
        re-derivation that could disagree.
    """
    ...

# From app_bundle
def fetch_application_published_version(application_id: str) -> Optional[str]:
    """
    The application's **published** version -- deliberately not the deployed one.
    
        This is the mirror image of :func:`fetch_deployment_app_version`, and the thing that
        function documents itself as refusing to be. The same 2026-08-03 live check applies:
        ``INF-M4-Testing`` was deployed on ``v1.8`` while its application's
        ``publishedVersion`` was ``v2.1``. So this value may well not be what a given worker
        runs, and the name says ``published`` for exactly that reason -- a caller that
        forgets which version it is holding is the whole hazard here.
    
        It exists because the alternative is worse. When the config, the caller's identity,
        the action record and the app-deployment record all come back empty -- which is the
        normal case for a ``deploy_postproc_add`` action, whose ``jobParams`` carry no
        version -- refusing to resolve means no bundle, which means the legacy path, which
        for a manifest-only app means ``ConfigValidationError: Unknown use case`` and an app
        that produces nothing at all. A possibly-wrong version's bundle is a worse answer
        than the right one and a better answer than no app.
    
        Returns ``None`` rather than raising, so the caller can fall through to the strict
        refusal message with its diagnostics intact.
    """
    ...

# From app_bundle
def fetch_deployment_app_identity(app_deployment_id: str) -> Tuple[Optional[str], Optional[str]]:
    """
    ``(application_id, application_version)`` an app deployment actually runs.
    
        One call, both halves. The record answers with ``appId`` **and** ``appVersion`` in the same
        payload -- ``{"appName": ..., "appVersion": "v1.8", "appId": "..."}`` -- so reading only the
        version, as this used to, threw away an id that was already on the wire. That mattered: on the
        ``deploy_postproc_add`` path the version is missing *and* the id often is too, and without an id
        there is nothing to ask about, so resolution failed at a point where the answer was in hand.
    
        Deliberately **not** the application's ``publishedVersion``: those diverge in production. A live
        check on 2026-08-03 found ``INF-M4-Testing`` deployed on ``v1.8`` while the application's
        ``publishedVersion`` was ``v2.1`` -- resolving via the latter would have fetched a different
        version's bundle for a running worker. ``None`` here means "unknown", and unknown must stay
        legacy rather than guess. See :func:`fetch_application_published_version` for the last-resort
        route that knowingly relaxes that rule, and only after this one has been tried.
    """
    ...

# From app_bundle
def fetch_deployment_app_version(app_deployment_id: str) -> Optional[str]:
    """
    The version an app deployment actually runs. See :func:`fetch_deployment_app_identity`.
    """
    ...

# From app_bundle
def fetch_post_processing_config_by_camera_and_app(camera_id: str, application_id: str) -> Optional[Dict[str, Any]]:
    """
    One camera's post-processing config for one application, or ``None``.
    
        The fallback for :func:`fetch_post_processing_configs`. Same route group, so the credentials
        that already reach the deployment-scoped call reach this one too -- and the same two-base
        retry, for the same local-gateway reason documented on :func:`backend_base_url`.
    
        This is the key the streaming UI both writes and reads on, so what it returns is by
        construction the polygon the operator can see drawn. Use it when the deployment-scoped query
        came back empty, and say loudly that it was needed: a hit here means the stored
        ``_idAppDeployment`` does not name this deployment, which is a defect upstream that this only
        works around.
    
        Returns ``None`` when the document does not exist -- a real answer, not an error. Raises
        :class:`AppBundleError` only when the call could not be made at all, so a caller can still
        tell "no zones" from "no answer".
    """
    ...

# From app_bundle
def fetch_post_processing_configs(app_deployment_id: str) -> List[Dict[str, Any]]:
    """
    Every camera's post-processing config document for one app deployment.
    
        The engine's zone primitives need the ``zone_config`` inside these documents, and this is the
        only route that serves it. It lives here rather than being read through
        ``PostProcessingConfigClient`` for one reason: that client is inside ``post_processing``, so
        importing it would make a manifest app pay the entire legacy import chain -- the exact cost
        routing at the runner exists to avoid.
    
        ``data`` on this route is a **list**, which is why it does not go through :func:`_rpc_data`
        (that coerces a non-dict ``data`` to ``{}``). The same two-base retry applies, for the same
        reason: a local gateway may not proxy the route.
    
        Returns an empty list when the deployment has no configs. Raises :class:`AppBundleError` when
        the call itself could not be made, so the caller can distinguish "no zones" from "no answer".
    """
    ...

# From app_bundle
def mint_usecase_download_url(application_id: str, application_version: str) -> str:
    """
    Ask be-application for a fresh presigned download URL for this version's bundle.
    
        Minting at load time rather than reading a URL out of config is what makes a restart safe: the
        presigned URLs be-application issues live for five hours, and a deployment's config outlives
        that by design.
    
        ``session`` is injectable so tests never touch the network. Raises :class:`AppBundleError` --
        never returns ``None`` -- so a caller gets a message naming the application, not a ``None`` to
        trip over later.
    """
    ...

# From app_bundle
def resolve_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, if it can be determined locally.
    
        Three sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it,
        then ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read, and the
        only one some py_compute launch paths emitted. Then ``sys.argv``: py_compute launches every
        action container as ``python3 <entrypoint>.py <action_record_id> <port>``, so the id is the
        first argument that looks like an ObjectId. Matching on shape rather than position keeps this
        from mistaking a port or a flag for an id.
    
        A malformed value in either env var falls through rather than erroring, so a truncated id does
        not mask a good one in argv.
    """
    ...

# From app_bundle
def resolve_app_bundle_refs(post_processing_config: Any = None) -> Tuple[Any, ...]:
    """
    Ordered bundle candidates, best first. Empty means "no bundle" -- today's every app.
    
        ``identity`` is any *other* mapping the caller holds that may carry these fields -- a
        ``stream_info``, a job-params map, or the raw ``post_processing_config`` dict when the caller's
        main config is a parsed object that dropped unknown keys. ``post_processing_config`` is
        consulted first, then ``identity``.
    
        Never raises and never does I/O. A malformed value is skipped, not reported: the reference that
        does load is the one that matters, and a candidate list is not the place to fail. The platform
        lookups a mint candidate may need happen inside :meth:`BundleRef.resolve`, never here.
    """
    ...

# From app_bundle
def resolve_application_identity(post_processing_config: Any = None) -> Tuple[Optional[str], Optional[str]]:
    """
    ``(application_id, application_version)`` -- from local data first, then the platform.
    
        Order, cheapest and most local first. **Every step here reports the version this deployment
        actually runs**; the published version is not among them and never resolves through this
        function -- see :func:`fetch_application_published_version` and its call site.
    
        1. whatever the caller already handed us (``post_processing_config``, then ``identity``, which in
           the worker path is ``stream_info``);
        2. this worker's own action record -- ``deploy_add`` jobParams carry both;
        3. the app-deployment record, which answers with the id **and** the version in one call;
        4. the deployment's post-processing config documents -- the same route the zone resolver already
           calls, whose documents carry ``_idApplication``. Last because it is the only step that can
           return several documents, but still a *deployed*-scope answer, so it belongs ahead of any
           published-version guess.
    
        Does I/O only for what is still missing, and returns ``None`` rather than inventing a value.
    """
    ...

# From backends
def app_bundle_zone_path(deployment_id: Optional[str]) -> str:
    """
    The URL the geometry lookup used, for an error an operator can act on.
    """
    ...

# From backends
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

# From backends
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

# From backends
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

# From backends
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

# From backends
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

# From backends
def source_dims_of(stream_info: Dict[str, Any]) -> Optional[Tuple[int, int]]:
    """
    ``(width, height)`` from a stream_info, or ``None`` when it declares no resolution.
    """
    ...

# From post_proc_runner
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

# From zone_source
def merge_zone_configs(api: Optional[Any[str, Any]], supplied: Optional[Any[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Combine the API's geometry with whatever the worker sent, **per field**.
    
        ``enrich`` fills gaps and never overwrites, which is right for identity -- the caller knows
        its own camera name better than the SDK does. It is wrong for geometry, because geometry is
        not identity: it changes after deploy, and the value the worker holds came from the
        deployment-time config blob rather than from the camera.
    
        The concrete failure this prevents: a worker whose ``camera_config`` declares only ``lines``
        suppresses the whole API lookup, so an app needing ``zones`` sees none and refuses -- with a
        ``zone_config`` present on the stream, which makes it look like geometry *was* delivered.
    
        So: each of ``zones`` and ``lines`` is taken from the API when the API declares any, and from
        the caller otherwise. A config declaring neither is treated as absent rather than as an
        authoritative "no geometry", which also closes the empty-dict trap for any producer that
        sends ``{"zones": {}, "lines": {}}``.
    """
    ...

# Classes
# From app_bundle
class AppBundleError:
    # A bundle reference exists but could not be turned into something loadable.

    ...

# From app_bundle
class BundleRef:
    # One place the bundle might be, and what we can say about it.
    #
    #     ``trusted`` is about *provenance*, not content: it says this reference came from somewhere
    #     authenticated (the platform's own API) or from an operator (an env var), rather than from
    #     author-supplied config. The loader uses it to decide whether a remote ``logic.py`` may be
    #     executed -- see ``remote_code_allowed`` and finding F9.
    #
    #     ``speculative`` says whether anyone actually *asserted* that a bundle exists here. An env var,
    #     a synced folder and a configured URL are assertions: somebody named this bundle, so failing to
    #     load it must be loud. A minted candidate is not -- it is inferred from the deployment merely
    #     having an application id, which **every** deployment has. Treating that inference as an assertion
    #     would make every legacy app in the fleet fail loudly, since the platform answers "no usecase
    #     uploaded for this version" for all of them.

    def resolve(self: Any) -> str:
        """
        The loadable reference. Any API call happens **here**, not at discovery time.
        
                Deferring it matters: a worker whose ``$MATRICE_APPS_ROOT`` already holds the app should
                never make a network call to discover a URL it will not use.
        """
        ...


# From backends
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


# From backends
class BackendError:
    # A backend could not be constructed.
    #
    #     Raised at construction, never per frame. The runner turns it into a logged error and a stream
    #     of empty results, because ``PostProcRunner.run`` must not raise — but the operator gets one
    #     loud line saying why every frame is empty, rather than silence.

    def __init__(self: Any, *args: Any) -> None: ...


# From backends
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


# From backends
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


# From post_proc_runner
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


# From zone_source
class ZoneAnswer:
    # What is known about one camera's geometry, and how confident we are of it.

    def fingerprint(self: Any) -> str:
        """
        Stable identity of this geometry, for deciding whether a Session must be rebuilt.
        
                Sorted, because a dict built from a JSON response has whatever key order the server sent
                and a re-fetch that reordered it must not read as a redraw.
        """
        ...

    def has_zones(self: Any) -> bool: ...


# From zone_source
class ZoneGeometryResolver:
    # Resolves and re-resolves zone geometry for every camera in one app deployment.
    #
    #     One instance per :class:`~matrice_analytics.runtime.backends.EngineBackend`. Holds one
    #     platform session for its whole life rather than opening one per fetch: with a TTL the fetch
    #     recurs, and ``fetch_post_processing_configs`` opens a fresh session every call otherwise.

    def __init__(self: Any, app_id: str) -> None: ...

    def answer_for(self: Any, camera_id: str, deployment_id: Optional[str], application_id: Optional[str]) -> Any:
        """
        This camera's geometry, refetching when the previous answer is due for a re-check.
        """
        ...

    def diagnostics(self: Any) -> Dict[str, Any]:
        """
        Per-camera geometry state, for an operator asking "why is this camera empty?".
        """
        ...

    def fallback_enabled(self: Any) -> bool: ...

    def max_backoff(self: Any) -> float: ...

    def refresh_seconds(self: Any) -> float: ...


from . import app_bundle, backends, post_proc_runner, zone_source