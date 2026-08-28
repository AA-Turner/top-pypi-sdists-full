"""Auto-generated stub for module: app_bundle."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
ACTION_DETAILS_PATH: str
APPLICATION_VERSION_PATH: str
APP_DEPLOYMENT_PATH: str
ENV_ACTION_ID: str
ENV_ALLOW_PUBLISHED_VERSION: str
ENV_API_BASE: str
ENV_BUNDLE_REF: str
ENV_LICENSE_KEY: str
ENV_SELF_MINT: str
LICENSE_KEY_HEADER: str
POST_PROCESSING_CONFIGS_PATH: str
POST_PROCESSING_CONFIG_BY_CAMERA_APP_PATH: str
USECASE_DOWNLOAD_LICENSE_PATH: str
USECASE_DOWNLOAD_PATH: str
logger: Any

# Functions
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
def fetch_action_job_params(action_id: str) -> Dict[str, Any]:
    """
    ``jobParams`` off this worker's action record.
    
        For a ``deploy_add`` action this holds ``application_version`` and ``application_id`` as the
        platform resolved them when it launched the container -- so it is the *deployed* pair, not a
        re-derivation that could disagree.
    """
    ...
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
def fetch_deployment_app_version(app_deployment_id: str) -> Optional[str]:
    """
    The version an app deployment actually runs. See :func:`fetch_deployment_app_identity`.
    """
    ...
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
def resolve_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, if it can be determined locally.
    
        Two sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it. Then
        ``sys.argv``: py_compute launches every action container as
        ``python3 <entrypoint>.py <action_record_id> <port>`` (``action_instance.py:2660``, ``:2703``),
        so the id is the first argument that looks like an ObjectId. Matching on shape rather than
        position keeps this from mistaking a port or a flag for an id.
    """
    ...
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

# Classes
class AppBundleError:
    # A bundle reference exists but could not be turned into something loadable.

    ...
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

