"""Where a camera's zone geometry comes from, and what to do when it is not there yet.

Resolving geometry used to be four lines inside ``EngineBackend``: one call per
``app_deployment_id``, the result cached per camera, and ``None`` cached just as firmly as a
real answer. Every one of those choices turned a transient or upstream problem into a permanent
one, and the failure is silent -- a zone app with no geometry does not degrade, it refuses, and
every frame comes back empty for the life of the process.

Three things this module changes, all of them consequences of one idea: **"no geometry" is not a
single answer.**

``none_declared``
    The deployment answered and this camera genuinely has no polygons. Cache it; re-check
    occasionally, because an operator draws zones on a running pipeline all the time.

``unknown``
    Nobody answered -- the call raised, the credentials are missing, the deployment returned
    nothing at all. This is the one the old code could not express: it wrote ``None``, which
    reads as ``none_declared`` forever after. Retry it, with backoff.

``resolved``
    Real geometry. Still re-checked on a TTL, because a polygon can be redrawn, and the session
    that was built from the old one has to be rebuilt.

The second idea is that the deployment-scoped lookup is not the only key onto the row. See
:func:`~matrice_analytics.runtime.app_bundle.fetch_post_processing_config_by_camera_and_app`
and :attr:`ZoneAnswer.stored_pointer`.

Nothing here imports ``post_processing`` or ``engine`` at module scope: ``app_bundle`` is
imported lazily inside the fetchers so that ``tests/unit/engine/test_import_isolation.py`` keeps
passing and a manifest app never pays the legacy import chain.
"""

from __future__ import annotations

import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Mapping, Optional, Tuple

logger = logging.getLogger(__name__)

__all__ = [
    "REFRESH_SECONDS_ENV",
    "MAX_BACKOFF_ENV",
    "LOOKUP_FALLBACK_ENV",
    "ZoneAnswer",
    "ZoneGeometryResolver",
    "merge_zone_configs",
]

REFRESH_SECONDS_ENV = "MATRICE_ZONE_REFRESH_SECONDS"
"""How often a settled answer is re-checked, in seconds. Default 300.

**``0`` disables refreshing entirely** and reproduces the pre-existing behaviour exactly: one
lookup per deployment for the life of the process, the answer cached forever. That is the
rollback lever, and it is read per call rather than at import for the same reason
``LEGACY_AGG_SHAPE_ENV`` is -- ``docker restart`` with the variable set is a complete rollback,
with no rebuild and no redeploy.
"""

MAX_BACKOFF_ENV = "MATRICE_ZONE_REFRESH_MAX_BACKOFF"
"""Ceiling on the retry backoff for an ``unknown`` answer, in seconds. Default 60."""

LOOKUP_FALLBACK_ENV = "MATRICE_ZONE_LOOKUP_FALLBACK"
"""Off switch for the ``(camera, application)`` fallback lookup. **Default on.**

Set to ``0`` / ``false`` / ``no`` / ``off`` to query only the deployment-scoped route, which is
the strict reading of the contract. With the fallback off, a camera whose stored
``_idAppDeployment`` is wrong stays dark until the upstream write path is fixed.
"""

_DEFAULT_REFRESH_SECONDS = 300.0
_DEFAULT_MAX_BACKOFF = 60.0
_FIRST_BACKOFF = 2.0

#: A 24-hex Mongo ObjectId, and the all-zero one be-inference writes on pipeline teardown.
_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$")
_NIL_OBJECT_ID = "0" * 24

_RESOLVED = "resolved"
_NONE_DECLARED = "none_declared"
_UNKNOWN = "unknown"


def _env_float(name: str, default: float, env: Optional[Mapping[str, str]] = None) -> float:
    raw = (env or os.environ).get(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        value = float(raw)
    except (TypeError, ValueError):
        logger.warning(
            "zone geometry: %s=%r is not a number; using the default of %s", name, raw, default
        )
        return default
    return value if value >= 0 else default


def _env_flag(name: str, default: bool, env: Optional[Mapping[str, str]] = None) -> bool:
    raw = (env or os.environ).get(name)
    if raw is None or not str(raw).strip():
        return default
    return str(raw).strip().lower() not in {"0", "false", "no", "off"}


@dataclass(frozen=True)
class ZoneAnswer:
    """What is known about one camera's geometry, and how confident we are of it."""

    zone_config: Optional[Dict[str, Any]] = None
    """Normalized 0-1 geometry, or ``None``. ``None`` with ``state == 'resolved'`` means the
    camera really has no polygons; ``None`` with ``state == 'unknown'`` means nobody answered."""

    drawn_resolution: Optional[Tuple[int, int]] = None
    """``(width, height)`` the polygons were drawn against, read off the raw document before
    ``normalize_zone_config`` drops it. The last-resort source for ``stream_resolution``."""

    state: str = _UNKNOWN
    """``resolved`` | ``none_declared`` | ``unknown``. See the module docstring."""

    provenance: str = ""
    """``by_app_deployment`` | ``camera+application`` | ``none``. Which key found it."""

    stored_pointer: Optional[str] = None
    """The ``_idAppDeployment`` actually on the document, when the fallback saw one. Diagnostic
    only -- it is what names the upstream defect."""

    reason: str = ""
    """One sentence, suitable for putting verbatim into an operator-facing error."""

    @property
    def has_zones(self) -> bool:
        return bool((self.zone_config or {}).get("zones"))

    @property
    def fingerprint(self) -> str:
        """Stable identity of this geometry, for deciding whether a Session must be rebuilt.

        Sorted, because a dict built from a JSON response has whatever key order the server sent
        and a re-fetch that reordered it must not read as a redraw.
        """
        config = self.zone_config or {}
        parts = []
        for field_name in ("zones", "lines"):
            shapes = config.get(field_name) or {}
            for name in sorted(shapes):
                parts.append(f"{field_name}:{name}:{shapes[name]}")
        return "|".join(parts) or "-"


@dataclass
class _DeploymentAttempt:
    """When this deployment was last asked, and how it went."""

    outcome: str = _UNKNOWN
    attempts: int = 0
    last_attempt: float = 0.0


class ZoneGeometryResolver:
    """Resolves and re-resolves zone geometry for every camera in one app deployment.

    One instance per :class:`~matrice_analytics.runtime.backends.EngineBackend`. Holds one
    platform session for its whole life rather than opening one per fetch: with a TTL the fetch
    recurs, and ``fetch_post_processing_configs`` opens a fresh session every call otherwise.
    """

    def __init__(
        self,
        app_id: str,
        *,
        clock: Callable[[], float] = time.monotonic,
        env: Optional[Mapping[str, str]] = None,
        fetch_by_deployment: Optional[Callable[..., Any]] = None,
        fetch_by_camera_app: Optional[Callable[..., Any]] = None,
    ) -> None:
        self._app_id = app_id
        self._clock = clock
        self._env = env
        self._fetch_by_deployment = fetch_by_deployment
        self._fetch_by_camera_app = fetch_by_camera_app
        self._answers: Dict[str, ZoneAnswer] = {}
        self._deployments: Dict[str, _DeploymentAttempt] = {}
        #: Fallback-lookup budget, per camera. See :meth:`_camera_due`.
        self._cameras: Dict[str, _DeploymentAttempt] = {}
        self._session: Any = None
        self._pointer_reported: set = set()

    # -- configuration -----------------------------------------------------

    @property
    def refresh_seconds(self) -> float:
        return _env_float(REFRESH_SECONDS_ENV, _DEFAULT_REFRESH_SECONDS, self._env)

    @property
    def max_backoff(self) -> float:
        return _env_float(MAX_BACKOFF_ENV, _DEFAULT_MAX_BACKOFF, self._env)

    @property
    def fallback_enabled(self) -> bool:
        return _env_flag(LOOKUP_FALLBACK_ENV, True, self._env)

    # -- the question the backend asks -------------------------------------

    def answer_for(
        self, camera_id: str, deployment_id: Optional[str], application_id: Optional[str]
    ) -> ZoneAnswer:
        """This camera's geometry, refetching when the previous answer is due for a re-check."""
        if not camera_id:
            return ZoneAnswer(state=_UNKNOWN, reason="the frame carries no camera id")
        if not deployment_id:
            # Not retryable: identity does not arrive late. The old code logged this per camera
            # and cached None, which was right -- it is the only "no geometry" that is permanent.
            return ZoneAnswer(
                state=_NONE_DECLARED,
                provenance="none",
                reason=(
                    "this stream carries no app_deployment_id, so zone geometry cannot be looked "
                    "up at all"
                ),
            )

        if self._due(deployment_id):
            self._refresh(deployment_id)

        answer = self._answers.get(camera_id)
        # The fallback is rate-limited on its own budget, not on the deployment's. Without this
        # a camera that genuinely has no zones sits at `none_declared` forever -- never
        # `resolved` -- so the condition below would be true on EVERY frame, and `enrich` runs
        # per frame: one HTTP call per frame per camera, 25 a second on a 25fps stream.
        if (answer is None or answer.state != _RESOLVED) and self._camera_due(camera_id):
            fallback = self._try_camera_app(camera_id, application_id, deployment_id)
            if fallback is not None:
                self._answers[camera_id] = fallback
                return fallback

        if answer is None:
            attempt = self._deployments.get(deployment_id)
            state = attempt.outcome if attempt else _UNKNOWN
            answer = ZoneAnswer(
                state=_NONE_DECLARED if state == _NONE_DECLARED else _UNKNOWN,
                provenance="by_app_deployment",
                reason=(
                    f"deployment {deployment_id} returned no post-processing config naming this "
                    "camera"
                ),
            )
            self._answers[camera_id] = answer
        return answer

    def _camera_due(self, camera_id: str) -> bool:
        """Is the ``(camera, application)`` fallback due for this camera?

        Its own budget, on the same backoff-then-TTL shape as the deployment lookup. The
        fallback answers a *different* question from the deployment one -- "is there a row the
        UI can see that we cannot?" -- so it needs its own clock; sharing the deployment's would
        either spend a call per frame or skip the fallback entirely on the frames that matter.
        """
        if not self.fallback_enabled:
            return False
        attempt = self._cameras.get(camera_id)
        if attempt is None:
            return True
        refresh = self.refresh_seconds
        if attempt.outcome == _UNKNOWN:
            wait = min(_FIRST_BACKOFF * (2 ** max(0, attempt.attempts - 1)), self.max_backoff)
        elif refresh <= 0:
            return False
        else:
            wait = refresh
        return (self._clock() - attempt.last_attempt) >= wait

    def _due(self, deployment_id: str) -> bool:
        """Is this deployment due to be asked again?"""
        attempt = self._deployments.get(deployment_id)
        if attempt is None:
            return True

        refresh = self.refresh_seconds
        if attempt.outcome == _UNKNOWN:
            # Backoff, not the TTL: an unanswered call is a different thing from a settled one,
            # and hammering a dead endpoint every frame is what the single-shot cache was
            # avoiding in the first place.
            wait = min(_FIRST_BACKOFF * (2 ** max(0, attempt.attempts - 1)), self.max_backoff)
        elif refresh <= 0:
            return False  # MATRICE_ZONE_REFRESH_SECONDS=0 -- ask once, ever.
        else:
            wait = refresh
        return (self._clock() - attempt.last_attempt) >= wait

    # -- the two lookups ---------------------------------------------------

    def _refresh(self, deployment_id: str) -> None:
        """Ask the deployment-scoped route and fold every camera it names into the cache."""
        attempt = self._deployments.setdefault(deployment_id, _DeploymentAttempt())
        attempt.attempts += 1
        attempt.last_attempt = self._clock()

        try:
            configs = self._call_by_deployment(deployment_id)
        except Exception as exc:  # noqa: BLE001 - a failed lookup must not kill the frame loop
            attempt.outcome = _UNKNOWN
            logger.warning(
                "zone geometry: app %s -- lookup failed for deployment %s (attempt %d, will "
                "retry): %s",
                self._app_id,
                deployment_id,
                attempt.attempts,
                exc,
            )
            return

        found = []
        for document in configs:
            if not isinstance(document, dict):
                continue
            pointer = _pointer_of(document)
            per_camera = document.get("postProcessing")
            if not isinstance(per_camera, dict):
                continue
            for camera_id, camera_config in per_camera.items():
                answer = _answer_from_camera_config(
                    camera_config, provenance="by_app_deployment", stored_pointer=pointer
                )
                if answer is None:
                    continue
                self._answers[str(camera_id)] = answer
                found.append(
                    f"{camera_id}({len((answer.zone_config or {}).get('zones') or {})}z/"
                    f"{len((answer.zone_config or {}).get('lines') or {})}l)"
                )

        attempt.outcome = _RESOLVED if found else _NONE_DECLARED
        if found:
            logger.info(
                "zone geometry: app %s -- deployment %s resolved: %s",
                self._app_id,
                deployment_id,
                ", ".join(found),
            )
        else:
            logger.info(
                "zone geometry: app %s -- deployment %s declares no zones or lines on any camera",
                self._app_id,
                deployment_id,
            )

    def _try_camera_app(
        self, camera_id: str, application_id: Optional[str], deployment_id: str
    ) -> Optional[ZoneAnswer]:
        """The fallback: find the row the streaming UI reads, and say why that was necessary."""
        if not self.fallback_enabled or not application_id:
            return None
        if not _OBJECT_ID_RE.match(str(application_id).lower()):
            # Not spending a call on something that cannot be a Mongo id.
            return None

        attempt = self._cameras.setdefault(camera_id, _DeploymentAttempt())
        attempt.attempts += 1
        attempt.last_attempt = self._clock()

        try:
            document = self._call_by_camera_app(camera_id, str(application_id))
        except Exception as exc:  # noqa: BLE001
            attempt.outcome = _UNKNOWN
            logger.debug(
                "zone geometry: app %s camera %s -- fallback lookup failed: %s",
                self._app_id,
                camera_id,
                exc,
            )
            return None
        if not isinstance(document, dict):
            attempt.outcome = _NONE_DECLARED
            return None
        attempt.outcome = _RESOLVED

        per_camera = document.get("postProcessing")
        camera_config = per_camera.get(camera_id) if isinstance(per_camera, dict) else None
        pointer = _pointer_of(document)
        answer = _answer_from_camera_config(
            camera_config, provenance="camera+application", stored_pointer=pointer
        )
        if answer is None:
            return None

        self._report_pointer(camera_id, pointer, deployment_id, application_id)
        return answer

    def _report_pointer(
        self,
        camera_id: str,
        pointer: Optional[str],
        deployment_id: str,
        application_id: Optional[str],
    ) -> None:
        """One ERROR per camera naming which upstream defect produced the bad pointer.

        Loud, and once: the geometry is being used, so the app works -- but it works because of a
        workaround, and a workaround nobody can see is a workaround that becomes permanent.
        """
        if camera_id in self._pointer_reported:
            return
        self._pointer_reported.add(camera_id)

        if pointer == _NIL_OBJECT_ID:
            cause = (
                "it is all zeros, which be-inference writes when a pipeline is torn down "
                "(post_processing_config_mongo.go, ResetAppDeploymentBatch) -- the geometry "
                "outlived the deployment that stamped it"
            )
        elif pointer and application_id and pointer.lower() == str(application_id).lower():
            cause = (
                "it is the APPLICATION id, which the streaming UI sends verbatim when a zone is "
                "saved (fe-streaming assign-application-form.tsx) -- it was never a deployment id"
            )
        elif pointer:
            cause = f"it names app deployment {pointer}, and this container is {deployment_id}"
        else:
            cause = "the document carries no _idAppDeployment at all"

        logger.error(
            "zone geometry: app %s camera %s -- this camera's zones were found by (camera, "
            "application) after the deployment-scoped lookup returned nothing, because the "
            "stored _idAppDeployment does not name this deployment: %s. The geometry IS being "
            "used, so the app will run -- but re-saving the zone from the UI cannot repair the "
            "pointer (the update route only writes postProcessing), so fix it upstream or set "
            "_idAppDeployment to %s directly. Set %s=0 to refuse instead of working around it.",
            self._app_id,
            camera_id,
            cause,
            deployment_id,
            LOOKUP_FALLBACK_ENV,
        )

    # -- transport (lazy, so `engine/` import isolation holds) --------------

    def _call_by_deployment(self, deployment_id: str) -> Any:
        if self._fetch_by_deployment is not None:
            return self._fetch_by_deployment(deployment_id)
        from .app_bundle import fetch_post_processing_configs

        return fetch_post_processing_configs(deployment_id, session=self._platform_session())

    def _call_by_camera_app(self, camera_id: str, application_id: str) -> Any:
        if self._fetch_by_camera_app is not None:
            return self._fetch_by_camera_app(camera_id, application_id)
        from .app_bundle import fetch_post_processing_config_by_camera_and_app

        return fetch_post_processing_config_by_camera_and_app(
            camera_id, application_id, session=self._platform_session()
        )

    def _platform_session(self) -> Any:
        """One session for the resolver's life. ``None`` lets the fetcher open its own.

        Without this each refresh would open a fresh ``matrice_common`` session, which was
        acceptable when the fetch happened once and is not when it happens on a TTL.
        """
        if self._session is None:
            from .app_bundle import _open_session

            try:
                self._session = _open_session(f"app {self._app_id} zone geometry")
            except Exception as exc:  # noqa: BLE001 - no credentials is an `unknown`, not a crash
                logger.debug("zone geometry: app %s -- no platform session: %s", self._app_id, exc)
                raise
        return self._session

    # -- introspection -----------------------------------------------------

    def diagnostics(self) -> Dict[str, Any]:
        """Per-camera geometry state, for an operator asking "why is this camera empty?"."""
        return {
            "app_id": self._app_id,
            "refresh_seconds": self.refresh_seconds,
            "fallback_enabled": self.fallback_enabled,
            "deployments": {
                deployment: {
                    "outcome": attempt.outcome,
                    "attempts": attempt.attempts,
                }
                for deployment, attempt in self._deployments.items()
            },
            "cameras": {
                camera: {
                    "state": answer.state,
                    "provenance": answer.provenance,
                    "stored_pointer": answer.stored_pointer,
                    "zones": sorted((answer.zone_config or {}).get("zones") or {}),
                    "lines": sorted((answer.zone_config or {}).get("lines") or {}),
                    "reason": answer.reason,
                }
                for camera, answer in self._answers.items()
            },
        }


def _pointer_of(document: Mapping[str, Any]) -> Optional[str]:
    """The ``_idAppDeployment`` on a config document, in any spelling, as a plain string."""
    for key in ("_idAppDeployment", "idAppDeployment", "appDeploymentId", "app_deployment_id"):
        value = document.get(key)
        if isinstance(value, str) and value:
            return value
        if isinstance(value, dict):  # some encoders emit {"$oid": "..."}
            oid = value.get("$oid")
            if isinstance(oid, str) and oid:
                return oid
    return None


def _answer_from_camera_config(
    camera_config: Any, *, provenance: str, stored_pointer: Optional[str]
) -> Optional[ZoneAnswer]:
    """A :class:`ZoneAnswer` from one camera's slice of a config document, or ``None``."""
    if not isinstance(camera_config, dict):
        return None
    from .backends import _declared_resolution, normalize_zone_config

    raw = camera_config.get("zone_config")
    normalized = normalize_zone_config(raw)
    if normalized is None:
        return None
    return ZoneAnswer(
        zone_config=normalized,
        drawn_resolution=_declared_resolution(raw),
        state=_RESOLVED,
        provenance=provenance,
        stored_pointer=stored_pointer,
        reason="",
    )


def merge_zone_configs(
    api: Optional[Mapping[str, Any]], supplied: Optional[Mapping[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Combine the API's geometry with whatever the worker sent, **per field**.

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
    api_zones = dict((api or {}).get("zones") or {})
    api_lines = dict((api or {}).get("lines") or {})
    supplied_zones = dict((supplied or {}).get("zones") or {})
    supplied_lines = dict((supplied or {}).get("lines") or {})

    zones = api_zones or supplied_zones
    lines = api_lines or supplied_lines
    if not zones and not lines:
        return None

    if api_zones and supplied_zones and set(api_zones) != set(supplied_zones):
        logger.info(
            "zone geometry: the caller supplied zones %s and the platform holds %s for this "
            "camera; using the platform's, which is what the operator drew",
            sorted(supplied_zones),
            sorted(api_zones),
        )
    return {"zones": zones, "lines": lines}
