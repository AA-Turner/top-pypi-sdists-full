"""Where an app bundle comes from, and in what order to try.

be-application ships an application version's usecase code as a zip: it fetches a GitHub folder at
a pinned commit SHA, re-zips it with the folder's **contents at the archive root**, uploads it to
``application-usecases/<folderKey>/<commitSha>.zip``, and serves a presigned GET at
``/v1/applications/{id}/versions/{version}/usecase/download``. Point ``githubPath`` at an
ml-applications app folder and that zip *is* an engine app bundle -- ``app.yaml``, ``logic.py``, the
three config JSONs -- in exactly the layout ``_locate_manifest_root`` already accepts.

This module answers one question: **given what a worker was handed, where is the bundle?** It does
no I/O and never raises. The answer is an ordered tuple of candidates, and an *empty* tuple is the
ordinary answer -- it means "no bundle reference", which is every app deployed today. That empty
tuple is the backward-compatibility guarantee: with no candidates, ``select_engine_backend`` runs
the same ``route_app`` line it ran before this module existed.

Why an *ordered* list rather than one answer: the four sources have genuinely different failure
modes. An operator's env var should beat platform config. A synced local folder should beat the
network, so an air-gapped box never calls S3. And a presigned URL that arrived in a deployment
config expires after five hours, so when it 403s the right move is to mint a fresh one, not to give
up -- which only works if both are candidates in one list.

The deployed application version is the one thing none of this can invent: be-application assigns
it server-side, so it is unknowable at authoring time. It is read back from the platform -- this
worker's own action record first, then the app-deployment record -- and never guessed from the
application's *published* version, which routinely runs ahead of what a deployment is on.

Standard library only at module scope. ``matrice_common`` is imported lazily inside
:func:`_open_session`, the same way ``PostProcessingConfigClient`` does it, so this module imports
cleanly in an image that has no platform SDK.
"""

from __future__ import annotations

import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

logger = logging.getLogger(__name__)

__all__ = [
    "AppBundleError",
    "BundleRef",
    "backend_base_url",
    "config_get",
    "fetch_action_job_params",
    "fetch_application_published_version",
    "fetch_deployment_app_identity",
    "fetch_deployment_app_version",
    "fetch_post_processing_configs",
    "mint_usecase_download_url",
    "resolve_action_id",
    "resolve_app_bundle_refs",
    "resolve_application_identity",
]

#: Keys a bundle URL may arrive under in ``post_processing_config``, in precedence order.
BUNDLE_URL_KEYS: Tuple[str, ...] = ("app_bundle_url", "usecase_codebase_url", "app_url")
#: ``_idApplication`` is the BE's own ObjectId field -- the sibling of ``_idAppDeployment``, and
#: what a post-processing config document actually carries. py_inference probes it explicitly
#: (``config_resolution.py:resolve_application_id``); omitting it here meant the same document
#: that names the application was read as if it did not.
APPLICATION_ID_KEYS: Tuple[str, ...] = (
    "application_id",
    "applicationId",
    "app_id",
    "appId",
    "_idApplication",
)

#: ``app_version``/``appVersion`` are not new spellings: ``fetch_deployment_app_version`` has
#: always accepted both off the deployment record, and py_inference reads ``app_version`` off the
#: **same** ``post_processing_config`` dict this module is handed
#: (``build_analytics_transport.py:212``). Accepting them only in one of the two readers was an
#: inconsistency, and it cost a wholly unnecessary API round trip -- or, when the deployment record
#: had no version either, a fall back to the published version for a value that was in hand all
#: along.
APPLICATION_VERSION_KEYS: Tuple[str, ...] = (
    "application_version",
    "applicationVersion",
    "app_version",
    "appVersion",
)

APP_DEPLOYMENT_ID_KEYS: Tuple[str, ...] = ("app_deployment_id", "appDeploymentId")

ENV_BUNDLE_REF = "MATRICE_APP_BUNDLE_REF"
ENV_SELF_MINT = "MATRICE_APP_BUNDLE_SELF_MINT"
ENV_ACTION_ID = "MATRICE_ACTION_ID"
ENV_API_BASE = "MATRICE_APP_BUNDLE_API_BASE"
ENV_LICENSE_KEY = "MATRICE_LICENSE_KEY"

#: Kill switch for the published-version fallback (see
#: :func:`fetch_application_published_version`). Default ON, because refusing to resolve
#: leaves the app dead; set to 0/false/no to restore the strict "refuse rather than guess"
#: behaviour fleet-wide without a release.
ENV_ALLOW_PUBLISHED_VERSION = "MATRICE_APP_BUNDLE_ALLOW_PUBLISHED_VERSION"

#: Header the licensed route authorises on. Same name py_compute uses for the one licensed call it
#: already makes (``scaling.py:1086``).
LICENSE_KEY_HEADER = "X-License-Key"

#: Routes. Paths, not URLs: ``matrice_common``'s RPC prepends the gateway base URL and signs the
#: request, so every call here rides the session the container is already authenticated with.
USECASE_DOWNLOAD_PATH = "/v1/applications/{application_id}/versions/{application_version}/usecase/download"

#: The same controller behind a license guard instead of a user-JWT guard
#: (``be-application/cmd/router.go:282-291``, PR #143). This is the one a deployed container can
#: actually use: the JWT route answers 404 unauthenticated and 401 with the container's own token.
USECASE_DOWNLOAD_LICENSE_PATH = (
    "/v1/applications/license/{application_id}/versions/{application_version}/usecase/download"
)

#: The action record that launched this worker. ``jobParams`` on a ``deploy_add`` action carries
#: ``application_version`` *and* ``application_id`` -- the exact pair the download route needs, as
#: the platform itself resolved them at launch. Same route ``matrice.ActionTracker`` uses
#: (``action_tracker.py:297``).
ACTION_DETAILS_PATH = "/v1/actions/action/{action_id}/details"

#: Fallback when the action record has no version (``deploy_postproc_add`` does not carry one):
#: the app-deployment record remembers the version this deployment actually runs.
APP_DEPLOYMENT_PATH = "/v1/inference/get_application_deployment/{app_deployment_id}"

#: Last resort when nothing knows the *deployed* version: the application record, which
#: knows the *published* one. Read :func:`fetch_application_published_version` before
#: using this -- the two are routinely different and the difference matters.
APPLICATION_VERSION_PATH = "/v1/applications/{application_id}"

#: Every camera's post-processing config for one app deployment -- including the ``zone_config`` the
#: engine's zone primitives require. Same route ``PostProcessingConfigClient`` calls
#: (``post_processing_config_client.py:355``), reached from here rather than through that client
#: **because importing it costs the whole legacy chain**: ~3,525 modules and ~49 seconds including
#: torch, which is precisely what routing at the runner exists to avoid, and what
#: ``test_an_engine_backed_runner_imports_no_legacy_module`` enforces.
POST_PROCESSING_CONFIGS_PATH = "/v1/inference/post_processing_configs/by_app_deployment/{app_deployment_id}"

#: The **same document**, found the way the streaming UI finds it: by camera and application.
#:
#: There is exactly one ``post_processing_config`` per ``(camera, application)`` -- every write
#: path in be-inference filters on that pair without upsert, so the document is re-pointed at a
#: new deployment rather than copied. That makes this route and the deployment-scoped one above
#: two keys onto one row, and the field that joins them (``_idAppDeployment``) is written by the
#: streaming UI, which sends the *application* id, and zeroed by be-inference on pipeline
#: teardown. When it is wrong the deployment-scoped query returns an empty envelope and the app
#: sees "this camera has 0 zones" while the operator can see the polygon on screen.
#:
#: Querying this as a fallback is what makes the pipeline agree with the screen. It cannot pick up
#: another deployment's geometry, because there is no other document to pick up.
POST_PROCESSING_CONFIG_BY_CAMERA_APP_PATH = "/v1/inference/post_processing_config"

#: A 24-hex Mongo ObjectId. Used to recognise an action id in ``sys.argv``.
_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$")


class AppBundleError(RuntimeError):
    """A bundle reference exists but could not be turned into something loadable."""


@dataclass(frozen=True)
class BundleRef:
    """One place the bundle might be, and what we can say about it.

    ``trusted`` is about *provenance*, not content: it says this reference came from somewhere
    authenticated (the platform's own API) or from an operator (an env var), rather than from
    author-supplied config. The loader uses it to decide whether a remote ``logic.py`` may be
    executed -- see ``remote_code_allowed`` and finding F9.

    ``speculative`` says whether anyone actually *asserted* that a bundle exists here. An env var,
    a synced folder and a configured URL are assertions: somebody named this bundle, so failing to
    load it must be loud. A minted candidate is not -- it is inferred from the deployment merely
    having an application id, which **every** deployment has. Treating that inference as an assertion
    would make every legacy app in the fleet fail loudly, since the platform answers "no usecase
    uploaded for this version" for all of them.
    """

    reference: Optional[str]
    via: str
    trusted: bool = False
    mint: Optional[Callable[[], str]] = None
    speculative: bool = False

    def resolve(self) -> str:
        """The loadable reference. Any API call happens **here**, not at discovery time.

        Deferring it matters: a worker whose ``$MATRICE_APPS_ROOT`` already holds the app should
        never make a network call to discover a URL it will not use.
        """
        if self.reference:
            return self.reference
        if self.mint is None:  # pragma: no cover - constructed with neither; guarded at build time
            raise AppBundleError(f"Bundle candidate {self.via} has neither a reference nor a way to mint one.")
        minted = self.mint()
        if not isinstance(minted, str) or not minted.strip():
            raise AppBundleError(f"Bundle candidate {self.via} produced no usable download URL.")
        return minted.strip()


def config_get(config: Any, keys: Sequence[str]) -> Optional[str]:
    """First non-empty string among ``keys``, from a dict or an attribute-bearing object.

    Both shapes are real and this is why the function exists: ``PostProcRunner`` passes the raw
    ``post_processing_config`` dict, while ``PostProcessor`` passes a *parsed* config object. A
    dict-only reader -- which is what ``backends._config_value`` is -- would make the two SDK entry
    points disagree about whether an app has a bundle, and keeping them in agreement is the entire
    reason ``select_engine_backend`` is a single function.
    """
    for key in keys:
        value = config.get(key) if isinstance(config, dict) else getattr(config, key, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def resolve_app_bundle_refs(
    post_processing_config: Any = None,
    *,
    app_name: Optional[str] = None,
    identity: Optional[Mapping[str, Any]] = None,
    env: Optional[Mapping[str, str]] = None,
    argv: Optional[Sequence[str]] = None,
    session: Any = None,
    minter: Optional[Callable[[str, str], str]] = None,
    action_params_fetcher: Optional[Callable[[str], Mapping[str, Any]]] = None,
    deployment_version_fetcher: Optional[Callable[[str], Optional[str]]] = None,
) -> Tuple[BundleRef, ...]:
    """Ordered bundle candidates, best first. Empty means "no bundle" -- today's every app.

    ``identity`` is any *other* mapping the caller holds that may carry these fields -- a
    ``stream_info``, a job-params map, or the raw ``post_processing_config`` dict when the caller's
    main config is a parsed object that dropped unknown keys. ``post_processing_config`` is
    consulted first, then ``identity``.

    Never raises and never does I/O. A malformed value is skipped, not reported: the reference that
    does load is the one that matters, and a candidate list is not the place to fail. The platform
    lookups a mint candidate may need happen inside :meth:`BundleRef.resolve`, never here.
    """
    environ = os.environ if env is None else env
    extra: Any = identity or {}
    candidates: list[BundleRef] = []

    explicit = (environ.get(ENV_BUNDLE_REF) or "").strip()
    if explicit:
        candidates.append(BundleRef(reference=explicit, via=f"${ENV_BUNDLE_REF}", trusted=True))

    usecase = (
        config_get(post_processing_config, ("usecase",))
        or config_get(extra, ("usecase",))
        or (app_name or "").strip()
        or None
    )
    local = _local_app_folder(usecase, environ)
    if local is not None:
        candidates.append(BundleRef(reference=local, via=f"$MATRICE_APPS_ROOT/{usecase}", trusted=True))

    url = config_get(post_processing_config, BUNDLE_URL_KEYS) or config_get(extra, BUNDLE_URL_KEYS)
    if url:
        # Author-supplied config: loadable, but not vouched for. A URL here also expires -- see the
        # mint candidate below, which is what recovers a 403 five hours into a deployment.
        candidates.append(BundleRef(reference=url, via="post_processing_config bundle url"))

    if (environ.get(ENV_SELF_MINT) or "").strip() not in {"0", "false", "no"}:
        have_locally = bool(
            config_get(post_processing_config, APPLICATION_ID_KEYS) or config_get(extra, APPLICATION_ID_KEYS)
        )
        can_look_up = bool(
            resolve_action_id(env=environ, argv=argv)
            or config_get(post_processing_config, APP_DEPLOYMENT_ID_KEYS)
            or config_get(extra, APP_DEPLOYMENT_ID_KEYS)
        )
        if have_locally or can_look_up:
            # The session has to reach the minter too, not just the identity lookups -- otherwise it
            # resolves the version over the caller's session and then tries to open a second one from
            # env credentials to mint the URL.
            call = minter or (
                lambda app_id, app_ver: mint_usecase_download_url(app_id, app_ver, session=session, env=environ)
            )

            def _mint_via_platform() -> str:
                # Resolution happens HERE, not at discovery: an app already present under
                # $MATRICE_APPS_ROOT must never cost an API round trip. `identity` in the worker
                # path is `stream_info`, which is where the yolo worker puts both ids
                # (workers.py:1072-1073).
                app_id, app_ver = resolve_application_identity(
                    post_processing_config,
                    identity=extra,
                    env=environ,
                    argv=argv,
                    session=session,
                    action_params_fetcher=action_params_fetcher,
                    deployment_version_fetcher=deployment_version_fetcher,
                )
                if app_id and not app_ver and _published_version_allowed(environ):
                    # Last resort. Deliberately NOT a fourth source inside
                    # `resolve_application_identity`: that function is public and its
                    # documented contract is the *deployed* version, so widening it would
                    # silently re-point every future caller at something weaker.
                    #
                    # Why fall back at all, given `fetch_deployment_app_version` documents
                    # a refusal to do exactly this: refusing leaves no bundle, which means
                    # the legacy path, which for a manifest-only app means
                    # `ConfigValidationError: Unknown use case` and an app that produces
                    # nothing whatsoever. That was the live state of X-Ray Detection. A
                    # possibly-wrong version's bundle is a worse answer than the right one
                    # and a better answer than no app -- but it IS a guess, so it is
                    # logged at WARNING every time and can be switched off fleet-wide.
                    app_ver = fetch_application_published_version(app_id, session=session, env=environ)
                    if app_ver:
                        logger.warning(
                            "app bundle: no record knows which version application %s is deployed "
                            "on, so falling back to its PUBLISHED version %r. That is routinely "
                            "ahead of what a deployment runs, so this may load a different "
                            "version's bundle; the alternative is no bundle at all, which for a "
                            "manifest-only app means the legacy path and no output. Set $%s=0 to "
                            "restore the strict refusal.",
                            app_id,
                            app_ver,
                            ENV_ALLOW_PUBLISHED_VERSION,
                        )
                if not app_id or not app_ver:
                    raise AppBundleError(
                        f"Could not determine the deployed application version "
                        f"(application_id={app_id!r}, application_version={app_ver!r}). Tried the "
                        f"config, the caller's identity, this worker's action record, the "
                        f"app-deployment record and the application's published version."
                    )
                return call(app_id, app_ver)

            candidates.append(
                BundleRef(
                    reference=None,
                    # Names both routes, because the mint closure may take either and
                    # `backends.py` logs this string as the explanation of what happened.
                    # A `via` that named only the strict route would be a lie in the one
                    # log line a future investigator reads first.
                    via=(
                        "usecase-download API (identity from action/deployment record, else the "
                        "application's PUBLISHED version -- which is not verified as the version "
                        "this deployment runs)"
                    ),
                    trusted=True,
                    mint=_mint_via_platform,
                    speculative=True,
                )
            )

    return tuple(candidates)


def _published_version_allowed(environ: Mapping[str, str]) -> bool:
    """Whether the published-version fallback may be used. Default yes."""
    raw = (environ.get(ENV_ALLOW_PUBLISHED_VERSION) or "").strip().lower()
    return raw not in {"0", "false", "no"}


def _local_app_folder(usecase: Optional[str], environ: Mapping[str, str]) -> Optional[str]:
    """The app's folder under ``$MATRICE_APPS_ROOT``, if it is really there. Else ``None``.

    Only ``$MATRICE_APPS_ROOT`` counts as a local hit. ``$MATRICE_APPS_URL`` resolves to a URL,
    which belongs later in the order -- the whole point of putting the root first is that a box
    holding the app on disk never makes a network call for it.

    Two layouts are accepted: ``<root>/<usecase>`` and ``<root>/<usecase>-v<X.Y>``. The second is
    the ml-applications leaf-folder convention, which exists because be-application keys its S3
    object on the *last* segment of githubPath, so a bare ``v1.6`` leaf would collide across apps.
    An ambiguous glob (two versions of one app synced side by side) is skipped rather than guessed:
    picking one silently is how a box ends up running a version nobody chose.

    The env is read from ``environ`` rather than via the loader's ``resolve_ref``, which consults
    ``os.environ`` directly and so cannot be told about an injected mapping.
    """
    root = (environ.get("MATRICE_APPS_ROOT") or "").strip()
    if not usecase or not root:
        return None

    base = Path(root).expanduser()
    exact = base / usecase
    if (exact / "app.yaml").is_file():
        return str(exact)

    versioned = sorted(candidate for candidate in base.glob(f"{usecase}-v*") if (candidate / "app.yaml").is_file())
    if len(versioned) == 1:
        return str(versioned[0])
    if versioned:
        logger.warning(
            "app bundle: $MATRICE_APPS_ROOT holds %d folders for %r (%s); not guessing which one "
            "to run -- name one with $%s",
            len(versioned),
            usecase,
            ", ".join(path.name for path in versioned),
            ENV_BUNDLE_REF,
        )
    return None


def resolve_action_id(env: Optional[Mapping[str, str]] = None, argv: Optional[Sequence[str]] = None) -> Optional[str]:
    """The action record id for this worker, if it can be determined locally.

    Two sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it. Then
    ``sys.argv``: py_compute launches every action container as
    ``python3 <entrypoint>.py <action_record_id> <port>`` (``action_instance.py:2660``, ``:2703``),
    so the id is the first argument that looks like an ObjectId. Matching on shape rather than
    position keeps this from mistaking a port or a flag for an id.
    """
    environ = os.environ if env is None else env
    explicit = (environ.get(ENV_ACTION_ID) or "").strip()
    if _OBJECT_ID_RE.match(explicit.lower()):
        return explicit.lower()

    for arg in list(argv if argv is not None else sys.argv)[1:]:
        candidate = str(arg).strip().lower()
        if _OBJECT_ID_RE.match(candidate):
            return candidate
    return None


def _rpc(session: Any) -> Any:
    """The authenticated RPC off a session, or a named error.

    ``session.rpc`` is the same handle ``PostProcessingConfigClient`` uses, already signed with the
    container's access keys -- nothing here builds its own auth.
    """
    try:
        return session.rpc
    except Exception as exc:  # pragma: no cover - a session whose rpc property raises
        raise AppBundleError(f"Session has no usable RPC handle: {exc}") from exc


def backend_base_url(env: Optional[Mapping[str, str]] = None) -> str:
    """The backend's own address, for a route the session's base URL will not serve.

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
    environ = os.environ if env is None else env
    explicit = (environ.get(ENV_API_BASE) or "").strip()
    if explicit:
        return explicit.rstrip("/")
    stage = ((environ.get("ENV") or "").strip() or "prod").lower()
    return f"https://{stage}.backend.app.matrice.ai"


def _rpc_data(
    session: Any,
    path: str,
    *,
    what: str,
    env: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """GET ``path`` on the authenticated session and return ``data`` as a dict.

    Tries the session's own base URL first -- where the gateway does proxy the route, that is one
    call and the right one. Only if that fails does it retry against
    :func:`backend_base_url`, because the most likely reason for the first failure is a
    cross-origin redirect that stripped the auth header rather than anything wrong with the request.
    """
    attempts: list[str] = []
    for base in (None, backend_base_url(env)):
        try:
            rpc = _rpc(session)
            response = rpc.get(path) if base is None else rpc.get(path, base_url=base)
        except AppBundleError as exc:
            # Recorded rather than re-raised so the final message still names the path. A session
            # with no usable rpc fails the same way twice, which is fine -- the cause is in the list.
            attempts.append(f"{base or 'session base url'}: {exc}")
            continue
        except Exception as exc:
            attempts.append(f"{base or 'session base url'}: {type(exc).__name__}: {exc}")
            continue

        if isinstance(response, dict) and response.get("success"):
            if base is not None:
                logger.info(
                    "app bundle: %s served from %s -- the session's base URL did not serve it (%s)",
                    path,
                    base,
                    attempts[0] if attempts else "no detail",
                )
            data = response.get("data")
            return data if isinstance(data, dict) else {}
        attempts.append(f"{base or 'session base url'}: {_describe(response)}")

    raise AppBundleError(
        f"GET {path} did not succeed while resolving {what}. Tried: " + "; ".join(attempts) + ". "
        "A 404 here usually means the request lost its Authorization header on a redirect out of "
        "the local gateway; a 401/403 means the container's credentials are not accepted on this "
        "route. Set $MATRICE_APP_BUNDLE_API_BASE to the backend that should serve it."
    )


def _describe(response: Any) -> str:
    """Say something useful about a failed response, including one that is not ours at all.

    ``message`` is absent whenever the body did not come from the platform -- an edge proxy
    returning its own error page, for instance. Reporting ``None`` in that case sends whoever reads
    the log hunting for a bug in the API call rather than in the network path, so name the shape.
    """
    if not isinstance(response, dict):
        return f"non-dict response {type(response).__name__}: {str(response)[:120]}"
    for key in ("message", "detail", "title", "error_name"):
        value = response.get(key)
        if isinstance(value, str) and value.strip():
            return f"{key}={value.strip()[:160]!r}"
    return f"no message; response keys were {sorted(response)[:12]}"


def fetch_action_job_params(action_id: str, *, session: Any = None) -> Dict[str, Any]:
    """``jobParams`` off this worker's action record.

    For a ``deploy_add`` action this holds ``application_version`` and ``application_id`` as the
    platform resolved them when it launched the container -- so it is the *deployed* pair, not a
    re-derivation that could disagree.
    """
    session = session if session is not None else _open_session(f"action {action_id}")
    data = _rpc_data(session, ACTION_DETAILS_PATH.format(action_id=action_id), what="action jobParams")
    params = data.get("jobParams")
    return params if isinstance(params, dict) else {}


def fetch_deployment_app_identity(
    app_deployment_id: str,
    *,
    session: Any = None,
) -> Tuple[Optional[str], Optional[str]]:
    """``(application_id, application_version)`` an app deployment actually runs.

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
    session = session if session is not None else _open_session(f"deployment {app_deployment_id}")
    data = _rpc_data(
        session,
        APP_DEPLOYMENT_PATH.format(app_deployment_id=app_deployment_id),
        what="deployment appVersion",
    )
    return _first_str(data, APPLICATION_ID_KEYS), _first_str(data, ("appVersion", "applicationVersion", "app_version"))


def fetch_deployment_app_version(app_deployment_id: str, *, session: Any = None) -> Optional[str]:
    """The version an app deployment actually runs. See :func:`fetch_deployment_app_identity`."""
    return fetch_deployment_app_identity(app_deployment_id, session=session)[1]


def _first_str(data: Mapping[str, Any], keys: Sequence[str]) -> Optional[str]:
    """The first non-blank string among ``keys``, unwrapping ``{"$oid": ...}`` encodings."""
    for key in keys:
        value = data.get(key)
        if isinstance(value, dict):  # some encoders emit {"$oid": "..."}
            value = value.get("$oid")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def fetch_application_published_version(
    application_id: str,
    *,
    session: Any = None,
    env: Optional[Mapping[str, str]] = None,
) -> Optional[str]:
    """The application's **published** version -- deliberately not the deployed one.

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
    try:
        session = session if session is not None else _open_session(f"application {application_id}")
        data = _rpc_data(
            session,
            APPLICATION_VERSION_PATH.format(application_id=application_id),
            what="application publishedVersion",
            env=env,
        )
    except AppBundleError as exc:
        logger.debug("app bundle: application %s gave no published version (%s)", application_id, exc)
        return None
    for key in ("publishedVersion", "latestVersion", "currentVersion", "version"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def fetch_post_processing_configs(
    app_deployment_id: str,
    *,
    session: Any = None,
    env: Optional[Mapping[str, str]] = None,
) -> List[Dict[str, Any]]:
    """Every camera's post-processing config document for one app deployment.

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
    session = session if session is not None else _open_session(f"deployment {app_deployment_id}")
    path = POST_PROCESSING_CONFIGS_PATH.format(app_deployment_id=app_deployment_id)

    attempts: list[str] = []
    for base in (None, backend_base_url(env)):
        try:
            rpc = _rpc(session)
            response = rpc.get(path) if base is None else rpc.get(path, base_url=base)
        except AppBundleError as exc:
            attempts.append(f"{base or 'session base url'}: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 - every transport error is one failed attempt
            attempts.append(f"{base or 'session base url'}: {type(exc).__name__}: {exc}")
            continue

        if isinstance(response, dict) and response.get("success"):
            data = response.get("data")
            if isinstance(data, list):
                return [entry for entry in data if isinstance(entry, (dict, list))]
            return [data] if isinstance(data, dict) else []
        attempts.append(f"{base or 'session base url'}: {_describe(response)}")

    raise AppBundleError(
        f"GET {path} did not succeed while resolving zone geometry. Tried: "
        + "; ".join(attempts)
        + ". Without it a zone-based app has no geometry and every frame comes back empty, so the "
        "caller must supply zone_config on its stream_info instead."
    )


def fetch_post_processing_config_by_camera_and_app(
    camera_id: str,
    application_id: str,
    *,
    session: Any = None,
    env: Optional[Mapping[str, str]] = None,
) -> Optional[Dict[str, Any]]:
    """One camera's post-processing config for one application, or ``None``.

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
    session = session if session is not None else _open_session(f"camera {camera_id}")
    path = POST_PROCESSING_CONFIG_BY_CAMERA_APP_PATH
    params = {"cameraId": camera_id, "applicationId": application_id}

    attempts: list[str] = []
    for base in (None, backend_base_url(env)):
        try:
            rpc = _rpc(session)
            response = rpc.get(path, params=params) if base is None else rpc.get(path, params=params, base_url=base)
        except AppBundleError as exc:
            attempts.append(f"{base or 'session base url'}: {exc}")
            continue
        except Exception as exc:  # noqa: BLE001 - every transport error is one failed attempt
            attempts.append(f"{base or 'session base url'}: {type(exc).__name__}: {exc}")
            continue

        if isinstance(response, dict) and response.get("success"):
            data = response.get("data")
            return data if isinstance(data, dict) else None
        # A 404 here is the document not existing, which is an answer. Only keep looking when the
        # call itself failed.
        attempts.append(f"{base or 'session base url'}: {_describe(response)}")

    raise AppBundleError(
        f"GET {path}?cameraId={camera_id}&applicationId={application_id} did not succeed while "
        "resolving zone geometry by camera and application. Tried: " + "; ".join(attempts)
    )


def _open_session(what: str) -> Any:
    """A ``matrice_common`` session from the container's own credentials.

    Imported lazily, exactly as ``PostProcessingConfigClient.__init__`` does, so this module stays
    importable in an image with no platform SDK.
    """
    access_key = os.getenv("MATRICE_ACCESS_KEY_ID", "")
    secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
    if not access_key or not secret_key:
        raise AppBundleError(
            f"Cannot resolve {what}: MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY are not set in this process."
        )
    try:
        from matrice_common.session import Session
    except Exception as exc:
        raise AppBundleError(f"Cannot resolve {what}: matrice_common is not importable ({exc}).") from exc
    try:
        return Session(
            access_key=access_key,
            secret_key=secret_key,
            account_number=os.getenv("MATRICE_ACCOUNT_NUMBER", "") or "",
        )
    except Exception as exc:
        raise AppBundleError(f"Could not open a Matrice session to resolve {what}: {exc}") from exc


def resolve_application_identity(
    post_processing_config: Any = None,
    *,
    identity: Optional[Mapping[str, Any]] = None,
    env: Optional[Mapping[str, str]] = None,
    argv: Optional[Sequence[str]] = None,
    session: Any = None,
    action_params_fetcher: Optional[Callable[[str], Mapping[str, Any]]] = None,
    deployment_version_fetcher: Optional[Callable[[str], Optional[str]]] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """``(application_id, application_version)`` -- from local data first, then the platform.

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
    extra: Any = identity or {}

    application_id = config_get(post_processing_config, APPLICATION_ID_KEYS) or config_get(extra, APPLICATION_ID_KEYS)
    application_version = config_get(post_processing_config, APPLICATION_VERSION_KEYS) or config_get(
        extra, APPLICATION_VERSION_KEYS
    )
    if application_id and application_version:
        return application_id, application_version

    action_id = resolve_action_id(env=env, argv=argv)
    if action_id:
        fetch = action_params_fetcher or (lambda a: fetch_action_job_params(a, session=session))
        try:
            params = fetch(action_id) or {}
        except AppBundleError as exc:
            logger.debug("app bundle: action %s gave no jobParams (%s)", action_id, exc)
            params = {}
        application_id = application_id or config_get(params, APPLICATION_ID_KEYS)
        application_version = application_version or config_get(params, APPLICATION_VERSION_KEYS)
        if application_id and application_version:
            return application_id, application_version

    deployment_id = config_get(post_processing_config, APP_DEPLOYMENT_ID_KEYS) or config_get(
        extra, APP_DEPLOYMENT_ID_KEYS
    )
    if deployment_id and not (application_id and application_version):
        try:
            if deployment_version_fetcher is not None:
                # An injected fetcher answers for the version only -- that is its published
                # signature, and widening it would break every existing caller.
                application_version = application_version or deployment_version_fetcher(deployment_id)
            else:
                found_id, found_version = fetch_deployment_app_identity(deployment_id, session=session)
                application_id = application_id or found_id
                application_version = application_version or found_version
        except AppBundleError as exc:
            logger.debug("app bundle: deployment %s gave no appVersion (%s)", deployment_id, exc)
        if application_id and application_version:
            return application_id, application_version

    if deployment_id and not (application_id and application_version):
        # The post-processing config documents. Reached only when everything above came back
        # empty, and worth the call because it is still the *deployed* answer: these documents
        # are per-camera deployment config, and they carry `_idApplication`. Trying this before
        # the published version is the difference between the right version and a plausible one.
        try:
            documents = fetch_post_processing_configs(deployment_id, session=session, env=env)
        except AppBundleError as exc:
            logger.debug("app bundle: deployment %s served no post-processing configs (%s)", deployment_id, exc)
            documents = []
        for document in documents:
            if not isinstance(document, Mapping):
                continue
            application_id = application_id or _first_str(document, APPLICATION_ID_KEYS)
            application_version = application_version or _first_str(document, APPLICATION_VERSION_KEYS)
            if application_id and application_version:
                break
        if application_id or application_version:
            logger.info(
                "app bundle: resolved application identity from the deployment's post-processing "
                "config documents (application_id=%r, application_version=%r) -- the deployed "
                "answer, after the action and app-deployment records had none.",
                application_id,
                application_version,
            )

    return application_id, application_version


def _mint_via_license(
    application_id: str,
    application_version: str,
    *,
    session: Any,
    env: Optional[Mapping[str, str]],
    what: str,
) -> Optional[str]:
    """The download URL off the licensed route, or ``None`` when there is no license key.

    Mirrors the one licensed call py_compute already makes
    (``scaling.py:1048-1090`` ``_fetch_docker_credentials_via_license``) in all three respects that
    matter: the ``X-License-Key`` header from ``$MATRICE_LICENSE_KEY``, an explicit **cloud** base
    URL, and ``send_request`` rather than ``get`` -- ``rpc.get`` takes no ``headers``.

    The cloud base URL is not an optimisation. py_compute's docstring is explicit that
    ``MATRICE_BASE_URL`` points at the local nginx on on-prem boxes and *"the local backend does not
    serve the licensed route -- only the cloud backend does"*, so this must never go through the
    session's own base URL.

    ``None`` means "not attempted", so the caller falls through to the JWT route -- which is still
    the right path in a context where that token is accepted.
    """
    environ = os.environ if env is None else env
    license_key = (environ.get(ENV_LICENSE_KEY) or "").strip()
    if not license_key:
        return None

    path = USECASE_DOWNLOAD_LICENSE_PATH.format(application_id=application_id, application_version=application_version)
    base = backend_base_url(env)
    try:
        response = _rpc(session).send_request(
            "GET",
            path=path,
            headers={LICENSE_KEY_HEADER: license_key},
            base_url=base,
        )
    except AppBundleError:
        raise
    except Exception as exc:
        raise AppBundleError(f"GET {base}{path} failed while resolving {what}: {exc}") from exc

    data = response.get("data") if isinstance(response, dict) else None
    if isinstance(response, dict) and response.get("success") and isinstance(data, dict):
        url = data.get("downloadUrl") or data.get("download_url")
        if isinstance(url, str) and url.strip():
            logger.info("app bundle: %s resolved from the licensed route at %s", what, base)
            return url.strip()

    raise AppBundleError(
        f"GET {base}{path} did not succeed while resolving {what}: {_describe(response)}. A 400 here "
        f"means the version has no usecase bundle attached, which is the ordinary legacy case; a 401 "
        f"means ${ENV_LICENSE_KEY} was rejected."
    )


def mint_usecase_download_url(
    application_id: str,
    application_version: str,
    *,
    session: Any = None,
    env: Optional[Mapping[str, str]] = None,
) -> str:
    """Ask be-application for a fresh presigned download URL for this version's bundle.

    Minting at load time rather than reading a URL out of config is what makes a restart safe: the
    presigned URLs be-application issues live for five hours, and a deployment's config outlives
    that by design.

    ``session`` is injectable so tests never touch the network. Raises :class:`AppBundleError` --
    never returns ``None`` -- so a caller gets a message naming the application, not a ``None`` to
    trip over later.
    """
    session = (
        session
        if session is not None
        else _open_session(f"the bundle URL for application {application_id} version {application_version}")
    )

    what = f"the bundle URL for application {application_id} version {application_version}"

    # The licensed route first when a license key is present. That is the one a deployed container
    # can actually use: the user-JWT route answers 404 unauthenticated (auth lost on the gateway's
    # cross-origin redirect) and 401 with the container's own token. Same controller, different
    # guard -- be-application PR #143.
    licensed = _mint_via_license(application_id, application_version, session=session, env=env, what=what)
    if licensed is not None:
        return licensed

    path = USECASE_DOWNLOAD_PATH.format(application_id=application_id, application_version=application_version)
    # Through _rpc_data, not session.rpc.get directly: this route lives on be-application, which the
    # local gateway does not proxy, so it needs the same direct-base-url retry the identity lookups
    # get. 0.1.429 shipped that retry for the lookups only and left this call on the plain handle,
    # which is why it kept 404ing in production while the identity resolved fine.
    try:
        data = _rpc_data(
            session,
            path,
            what=what,
            env=env,
        )
    except AppBundleError as exc:
        # The commonest failure by far is "this version has no bundle", which is not a fault at all.
        # Say so, so nobody reads a routine legacy app as a broken one.
        raise AppBundleError(
            f"{exc} A 400 on this route means the version has no usecase bundle attached, which is "
            f"the ordinary legacy case."
        ) from exc

    url = data.get("downloadUrl") or data.get("download_url")
    if not isinstance(url, str) or not url.strip():
        raise AppBundleError(
            f"GET {path} succeeded but returned no downloadUrl: {data!r}. A 400 on this route means "
            f"the version has no usecase bundle attached, which is the ordinary legacy case."
        )
    return url.strip()
