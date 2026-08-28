"""The two implementations behind :class:`~matrice_analytics.runtime.PostProcRunner`.

An application is either a **legacy use case** — one of the ~140 hand-written classes under
``post_processing/usecases/`` — or a **manifest app** the new engine runs from an ``app.yaml``.
Which one it is must not be visible to the worker: it calls ``runner.run(...)`` either way and gets
the same dict back.

This module is that seam. It lives in ``runtime/`` rather than in either implementation because
``runtime/`` is neither side. ``engine/`` may not import ``post_processing`` or ``analytics``
(enforced in a fresh subprocess by ``tests/unit/engine/test_import_isolation.py``), and
``engine/routing.py`` states the intended shape outright: *routing decides whether legacy is used;
it never imports legacy to decide -- the caller does the dispatch.* ``runtime/`` is that caller.

Why the choice is made this high up
-----------------------------------
The obvious hook is ``PostProcessor.process``, which already branches. It is the wrong one: by the
time you reach it you have paid for legacy. A cold ``import matrice_analytics.post_processing``
loads **3,525 modules in ~49 seconds**, pulling torch, sympy, scipy, pandas, torchvision, cv2 and
onnxruntime. Choosing here means a manifest app never imports any of it.

That has a second consequence worth stating plainly, because the current arrangement is the
opposite of it. Today the two flows avoid double-publishing by *starvation*: the newer flow strips
the frame-path ``TrackingStats`` so the legacy publisher finds nothing and stands down — which is
exactly why every be-analytics instant metric evaluates against zero (**PY-2**). Here the backends
are mutually exclusive and :class:`EngineBackend` never constructs a ``PostProcessor``, so the
legacy publisher cannot run at all. Not suppressed. Absent.

Nothing under ``post_processing/`` is modified by any of this. A legacy app takes the same path it
took before this module existed; :class:`LegacyBackend` is that path with a class around it.
"""

from __future__ import annotations

import functools
import logging
import os
from typing import Any, Dict, Final, List, Optional, Protocol, Sequence, Tuple

logger = logging.getLogger(__name__)

__all__ = [
    "Backend",
    "BackendError",
    "EngineBackend",
    "LEGACY_AGG_SHAPE_ENV",
    "LegacyBackend",
    "legacy_shape_agg_summary",
    "normalize_zone_config",
    "require_engine_ready",
    "resolve_source_dims",
    "select_engine_backend",
]


class BackendError(RuntimeError):
    """A backend could not be constructed.

    Raised at construction, never per frame. The runner turns it into a logged error and a stream
    of empty results, because ``PostProcRunner.run`` must not raise — but the operator gets one
    loud line saying why every frame is empty, rather than silence.
    """

    def __init__(self, *args: Any, retryable: bool = False) -> None:
        super().__init__(*args)
        self.retryable = retryable
        """Can this resolve without restarting the container?

        ``False`` for the original cases -- a stream that cannot say how big its frames are, or
        that omits identity the SDK cannot invent, does not start being able to mid-run.

        ``True`` for missing zone geometry, which is a row in a database that somebody is about
        to fix. Refusing that camera permanently would mean the fix requires a restart, which is
        the exact operational cost the retry and TTL exist to remove.
        """


class Backend(Protocol):
    """What :class:`~matrice_analytics.runtime.PostProcRunner` needs from an implementation."""

    #: ``"legacy"`` or ``"engine"`` -- for logs and introspection.
    name: str

    async def process(
        self,
        *,
        detections: Any,
        camera_id: str,
        stream_info: Dict[str, Any],
        input_bytes: Optional[bytes],
        config: Any,
        frame_ts: Optional[float],
    ) -> Optional[Dict[str, Any]]:
        """Handle one frame.

        Returns the runner's stable ``{"result": ..., "agg_summary": ...}`` dict, or ``None`` when
        there is nothing to report (the runner turns that into its empty result).
        """
        ...

    def close(self) -> None:
        """Release whatever the backend holds. Idempotent."""
        ...


# ---------------------------------------------------------------------------
# Legacy
# ---------------------------------------------------------------------------


class LegacyBackend:
    """The path every application takes today: one ``PostProcessor``, awaited per frame.

    Lifted from ``PostProcRunner`` unchanged, including the lazy import and the ``redis_config``
    forwarding. If this class does anything the old runner did not, that is a bug.
    """

    name = "legacy"

    def __init__(
        self,
        *,
        post_processing_config: Optional[Any] = None,
        app_name: Optional[str] = None,
        index_to_category: Optional[Dict[int, str]] = None,
        target_categories: Optional[List[str]] = None,
        redis_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Lazy so that importing this module -- or constructing an engine-backed runner --
        # never drags in the post_processor chain.
        from ..post_processing.post_processor import PostProcessor

        # redis_config reaches the analytics publisher, which otherwise falls back to the
        # environment (and, with nothing set, to localhost). The caller has already resolved the
        # real host/Sentinel topology, so forwarding it here is what closes that seam.
        self._processor = PostProcessor(
            post_processing_config=post_processing_config,
            app_name=app_name,
            index_to_category=index_to_category,
            target_categories=target_categories,
            redis_config=redis_config,
        )

    @property
    def processor(self) -> Any:
        return self._processor

    async def process(
        self,
        *,
        detections: Any,
        camera_id: str,
        stream_info: Dict[str, Any],
        input_bytes: Optional[bytes],
        config: Any,
        frame_ts: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        # `frame_ts` is accepted for interface parity and deliberately ignored: the legacy flow
        # takes its cadence from wall-clock inside the bridge (PY-13), and threading a frame
        # timestamp in here would change behaviour for every existing app.
        result = await self._processor.process(
            data=detections,
            config=config if config is not None else {},
            stream_key=camera_id,
            stream_info=stream_info,
            input_bytes=input_bytes,
        )
        if result is None:
            return None
        return {"result": _result_as_dict(result), "agg_summary": _unwrap_agg_summary(result)}

    def close(self) -> None:
        """The legacy processor owns no resource the runner is expected to release."""


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


class _EngineProcessorShim:
    """What ``runner.processor`` returns on the engine path.

    Not cosmetic. ``ml-codebases/yolo_code_base/inference/workers.py`` reads ``runner.processor``
    once at ``:789`` and then gates **every frame** on it::

        analytics_processor = runner.processor                        # :789
        _apply_tracking = enable_tracking and (analytics_processor is None)   # :821
        if enable_pp and analytics_processor is not None:             # :1024
            ...runner.run(...)                                        # :1147

    Returning ``None`` there is not an error -- it is worse. The gate at ``:1024`` closes
    permanently, ``run`` is never called, ``agg_summary`` stays ``{}`` on every frame, and the
    worker's own tracker silently switches back on. Nothing is logged after startup.

    So the engine path returns this instead: truthy, and carrying the one attribute the worker
    actually touches. ``workers.py:1097`` guards with
    ``hasattr(p, '_use_case_cache') and p._use_case_cache``, so an empty mapping makes the
    LPR ``set_bgr_frame`` block skip cleanly rather than raise.
    """

    #: Empty on purpose: a manifest app has no legacy use-case instances to hand raw frames to.
    _use_case_cache: Dict[str, Any] = {}

    def __init__(self, app_id: str) -> None:
        self.app_id = app_id

    def __repr__(self) -> str:
        return f"<engine backend for {self.app_id!r}; not a PostProcessor>"


class EngineBackend:
    """A manifest app, run by :class:`~matrice_analytics.engine.runtime.session.Session`.

    One session per camera, because a session is bound to one stream's geometry and window state.
    Sessions are built on first sight of a camera and flushed on :meth:`close`, so the final
    partial window is published rather than lost.

    Unlike the legacy backend this one **publishes for itself**: ``results-agg`` and
    ``incident_res`` leave through the injected publisher inside ``Session``. The per-frame S3
    payload is returned instead, for the worker to write to its own output topic.
    """

    name = "engine"

    def __init__(
        self,
        loaded: Any,
        *,
        redis_config: Optional[Dict[str, Any]] = None,
        app_name: Optional[str] = None,
        post_processing_config: Any = None,
    ) -> None:
        from ..engine.publish import RedisStreamPublisher

        self._loaded = loaded
        self._app_name = app_name
        self._config = post_processing_config
        self._publisher = RedisStreamPublisher(redis_config)
        self._sessions: Dict[str, Any] = {}
        self._closed = False
        self._shim = _EngineProcessorShim(loaded.manifest.app.id)
        # Zone geometry. Owned by `runtime/zone_source.py` rather than inlined here, because
        # "this camera has no zones" and "nobody answered" are different answers and only one of
        # them should be cached forever -- see that module's docstring.
        from .zone_source import ZoneGeometryResolver

        self._zones = ZoneGeometryResolver(loaded.manifest.app.id)
        # The resolution the operator drew the polygons against, kept out of band because
        # `normalize_zone_config` deliberately drops it: `ZoneConfig` declares only `zones` and
        # `lines`, and that function's output shape is consumed by a separately-shipped repo
        # (`ml-codebases/yolo_code_base/inference/workers.py`). It is the last-resort source for
        # `stream_resolution` -- see `_resolution_gap_fill`.
        self._drawn_resolution_by_camera: Dict[str, Tuple[int, int]] = {}
        # Which geometry each live session was built from. A Session derives seven structures
        # from its SceneGeometry at construction and exposes no setter, so a redrawn polygon is
        # a rebuild, not a mutation -- see `_session`.
        self._session_fingerprints: Dict[str, str] = {}

    @property
    def app_id(self) -> str:
        return self._loaded.manifest.app.id

    @property
    def manifest(self) -> Any:
        """The parsed ``app.yaml``.

        Exposed so the readiness check can ask whether this app *requires* zones, rather than
        reaching through ``_loaded`` from another module.
        """
        return self._loaded.manifest

    @property
    def processor(self) -> Any:
        """A compatibility handle for callers that gate on ``runner.processor``.

        See :class:`_EngineProcessorShim`. Never ``None``.
        """
        return self._shim

    @property
    def sessions(self) -> Dict[str, Any]:
        """The live sessions, keyed by camera id. Introspection for tests."""
        return dict(self._sessions)

    def enrich(self, stream_info: Dict[str, Any], *, input_bytes: Any = None) -> Dict[str, Any]:
        """Fill the identity fields the engine requires and the worker did not send.

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
        app = self._loaded.manifest.app
        # Resolved before the table, not inside it: the resolution gap-fill needs to know whether
        # geometry ends up declared, and relying on dict-literal evaluation order to express that
        # is the kind of implicit coupling that survives one refactor and not two.
        zone_config = self._zone_config_for(stream_info)
        zoned = bool((zone_config or {}).get("zones") or _has_identity(stream_info, "zone_config"))
        derived = {
            "application_key_name": app.id,
            "application_version": app.version,
            "application_name": _display_name(self._app_name) or app.name,
            "app_deployment_id": _config_value(self._config, "deployment_id"),
            # py_inference deletes `camera_info` outright, taking `camera_name` with it, and
            # `StreamInfo.from_raw` refuses a stream without one -- so this gap-fill is what buys
            # an engine session at all, not a display choice. It is deliberately *not* the wire
            # value: `AggregationResult` and `IncidentMessage` both blank a name that equals the
            # id (FROZEN-8), so the ObjectID stops at the emit boundary. The real name arrives
            # separately, from `PostProcessor._enrich_stream_info_camera_metadata`, and wins here
            # because this table only fills gaps.
            "camera_name": stream_info.get("camera_id"),
            # The zone geometry the app's own primitives require. No worker in ml-codebases sends
            # it -- the string `zone_config` does not appear in that repo at all -- and a zone app
            # without it does not degrade, it refuses: `Session.from_loaded_app` raises
            # `SessionError` ("this camera has 0 zones") and every frame comes back empty. The
            # legacy use cases resolve it from the same API internally (`dwell_detection.py:383`,
            # `post_processor.py:714`), which is why only the engine path was affected.
            "zone_config": zone_config,
            # Required once geometry exists, and derivable from the frame we were handed. Last in
            # the table because `_resolution_gap_fill` reads `zoned`, resolved above.
            "stream_resolution": self._resolution_gap_fill(stream_info, input_bytes, zoned=zoned),
        }

        enriched = dict(stream_info)
        filled = []
        for key, value in derived.items():
            if value and not _has_identity(stream_info, key):
                enriched[key] = value
                filled.append(key)

        # `zone_config` is the one key where caller-wins is wrong. Caller-wins is right for
        # identity -- the worker knows its own camera better than the SDK does -- but geometry is
        # not identity: it changes after deploy, and the value a worker holds came from the
        # deployment-time config blob rather than from the camera. A blob declaring only `lines`
        # would otherwise suppress the whole API lookup, so an app needing `zones` sees none and
        # refuses, with a `zone_config` present on the stream making it look delivered.
        supplied_zone_config = _first_zone_config(stream_info)
        if supplied_zone_config is not None and zone_config is not None:
            from .zone_source import merge_zone_configs

            merged = merge_zone_configs(zone_config, supplied_zone_config)
            if merged is not None and merged != supplied_zone_config:
                enriched["zone_config"] = merged
                filled.append("zone_config(merged)")

        if filled:
            logger.debug(
                "engine backend: app %s -- derived stream_info field(s) the worker did not send: %s",
                self.app_id,
                ", ".join(filled),
            )
        return enriched

    def _resolution_gap_fill(
        self, stream_info: Dict[str, Any], input_bytes: Any, *, zoned: bool
    ) -> Optional[Dict[str, int]]:
        """``{"width": w, "height": h}`` the caller did not send, or ``None``.

        Two sources, in order, and the second one is deliberately narrow.

        1. :func:`resolve_source_dims` -- the frame itself, via its JPEG SOF marker or an ndarray
           shape. **Measured**, so it is correct for every consumer, and it is already computed on
           this path: ``_boxes_to_unit_square`` normalizes boxes with exactly this number and then
           throws it away. Writing it back is the whole fix.
        2. The resolution the polygons were drawn against, only when geometry is declared and only
           when nothing in the pipeline needs *true* pixels.

        Why source 2 is safe for zone membership and nothing else: polygons go unit -> pixel with
        ``stream.resolution`` (``SceneGeometry.from_zone_config``) and a detection's reference
        point goes unit -> pixel with the **same** ``stream.resolution``
        (``detection_reference_point``), so point-in-polygon is invariant under any positive
        scale -- the number cancels. ``keypoint_pose``, ``segmentation_area`` and
        ``velocity_state`` do not have that property: they report distances, areas and speeds in
        pixels, so a drawing resolution that differs from the frame's silently rescales a real
        measurement. Those three opt the source out entirely rather than warn.

        What this deliberately does **not** do is invent a resolution. ``py_inference`` returns
        ``None`` from ``_analytics_source_dims`` on purpose when the coordinate space is the model
        grid or the frame shape was defaulted rather than measured, arguing that a loud refusal
        beats a wrong resolution (INF-2606). Neither source here overrides that: source 1 is
        measured from the frame, and source 2 needs geometry to exist before it applies.
        """
        if source_dims_of(stream_info) is not None:
            return None

        dims = resolve_source_dims(stream_info, input_bytes)
        if dims is not None:
            return {"width": dims[0], "height": dims[1]}

        if not zoned:
            return None
        camera_id = str(stream_info.get("camera_id") or "")
        drawn = self._drawn_resolution_by_camera.get(camera_id)
        if drawn is None or self._needs_true_pixels():
            return None

        logger.warning(
            "engine backend: app %s camera %s -- this frame carries no resolution, so zone "
            "geometry will be scaled against the resolution the polygons were drawn at (%dx%d). "
            "Zone membership is unaffected (polygons and detections scale by the same number), "
            "but pass source_dims= to run() if any absolute-pixel figure is ever added to this "
            "app.",
            self.app_id,
            camera_id,
            drawn[0],
            drawn[1],
        )
        return {"width": drawn[0], "height": drawn[1]}

    def _needs_true_pixels(self) -> bool:
        """Does any stage in this manifest report a figure in real pixels?

        ``keypoint_pose``, ``segmentation_area`` and ``velocity_state`` call
        ``FrameContext.require_resolution`` and turn it into a distance, an area or a speed. For
        those a substituted resolution is not a harmless scale factor, it is a wrong measurement.
        """
        return any(
            getattr(stage, "PRIMITIVE", "") in _ABSOLUTE_PIXEL_PRIMITIVES for stage in self._loaded.manifest.pipeline
        )

    # -- zone geometry -----------------------------------------------------
    def _zone_answer_for(self, stream_info: Dict[str, Any]) -> Any:
        """What is known about this camera's geometry right now.

        Delegates to :class:`~matrice_analytics.runtime.zone_source.ZoneGeometryResolver`, which
        distinguishes "this camera has no zones" from "nobody answered" and retries only the
        second. Called from :meth:`enrich`, so it runs per frame and must be cheap: the resolver
        does nothing at all between refresh intervals.
        """
        from .zone_source import ZoneAnswer

        camera_id = str(stream_info.get("camera_id") or "")
        if not camera_id:
            return ZoneAnswer()

        deployment_id = _stream_value(
            stream_info, "app_deployment_id", "appDeploymentId", "deployment_id", "deploymentId"
        ) or _config_value(self._config, "deployment_id")
        application_id = _stream_value(stream_info, "app_id", "appId", "application_id", "applicationId")

        answer = self._zones.answer_for(
            camera_id,
            str(deployment_id) if deployment_id else None,
            str(application_id) if application_id else None,
        )
        if answer.drawn_resolution is not None:
            self._drawn_resolution_by_camera[camera_id] = answer.drawn_resolution
        return answer

    def _zone_config_for(self, stream_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """This camera's ``zone_config``, normalized to 0-1, or ``None``.

        Kept as the name :meth:`enrich` and the tests use; the resolution itself moved to
        :meth:`_zone_answer_for`.
        """
        return self._zone_answer_for(stream_info).zone_config

    @property
    def zone_diagnostics(self) -> Dict[str, Any]:
        """Per-camera geometry state: what was found, by which key, and why not otherwise.

        "Self-diagnosing" should not mean "grep the logs of a container that has already rolled
        them". A camera publishing nothing is the symptom this exists to explain.
        """
        return self._zones.diagnostics()

    def _session(self, camera_id: str, stream_info: Dict[str, Any]) -> Any:
        from ..engine.runtime.session import Session

        session = self._sessions.get(camera_id)
        fingerprint = _geometry_fingerprint(stream_info)
        if session is not None and self._session_fingerprints.get(camera_id) != fingerprint:
            # The polygons changed under a live session. `Session` derives `_zoned`,
            # `_zone_polygons`, `_reference_point`, `_emission_zones`, `_pipelines`, `_rules` and
            # `_window` from its `SceneGeometry` at construction and exposes no setter, so
            # swapping the geometry alone would leave seven structures describing the old zones.
            # Rebuild, and flush first so the counts up to the change are published rather than
            # dropped. State is deliberately NOT carried: it is scoped by zone name, and handing
            # the old zone's dwell to a redrawn polygon would attribute time nobody spent there.
            logger.info(
                "engine backend: app %s camera %s -- zone geometry changed; flushing the open "
                "window and rebuilding the session",
                self.app_id,
                camera_id,
            )
            try:
                session.flush()
            except Exception as exc:  # noqa: BLE001 - a failed flush must not block the rebuild
                logger.warning(
                    "engine backend: app %s camera %s -- flush before rebuild failed: %s",
                    self.app_id,
                    camera_id,
                    exc,
                )
            session = None
            self._sessions.pop(camera_id, None)

        if session is None:
            session = Session.from_loaded_app(
                self._loaded,
                stream_info,
                publisher=self._publisher,
            )
            self._sessions[camera_id] = session
            self._session_fingerprints[camera_id] = fingerprint
            logger.info(
                "engine backend: app %s camera %s -- session started (%d stage(s), zones %s)",
                self.app_id,
                camera_id,
                len(session.stage_names),
                ", ".join(session.emission_zones),
            )
        return session

    async def process(
        self,
        *,
        detections: Any,
        camera_id: str,
        stream_info: Dict[str, Any],
        input_bytes: Optional[bytes] = None,
        config: Any = None,
        frame_ts: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        # `config` is accepted for interface parity. A manifest app takes its configuration from
        # app.yaml, resolved once at routing time; a per-frame override has no meaning here and is
        # ignored rather than half-honoured. `input_bytes` is not inert -- it is one of the places
        # the frame's dimensions can be recovered from (see `resolve_source_dims`).
        enriched = self.enrich(stream_info, input_bytes=input_bytes)
        session = self._session(camera_id, enriched)

        # All three media anchors are per-frame. The session is cached per camera, so anything
        # not passed here stays at the value the first frame happened to carry -- which for
        # `rtp_number` meant every alert on the camera resolved to the same thumbnail.
        outcome = session.process_frame(
            _boxes_to_unit_square(detections, enriched, input_bytes),
            frame_ts=frame_ts,
            frame_id=enriched.get("frame_id") or None,
            stream_time=enriched.get("stream_time") or None,
            rtp_number=_anchor_str(enriched.get("rtp_number")),
        )

        payload = outcome.payload()
        agg_summary = payload.get("agg_summary") if payload else None
        # The engine keys `agg_summary` by ZONE and legacy keys it by FRAME NUMBER (PY-5). Consumers
        # were built against the legacy shape, so bridge it here -- one place, so all four callers
        # (both yolo workers, fr, and py_inference's analytics node) see one shape instead of three
        # worker copies drifting apart.
        return {
            "result": _outcome_as_result(outcome, self._loaded.manifest, payload),
            "agg_summary": legacy_shape_agg_summary(agg_summary, enriched),
        }

    def close(self) -> None:
        """Flush every open window, then release the publisher. Idempotent."""
        if self._closed:
            return
        self._closed = True
        for camera_id, session in self._sessions.items():
            try:
                session.flush()
            except Exception:  # pragma: no cover - defensive; close must not raise
                logger.warning(
                    "engine backend: flush failed for app %s camera %s",
                    self.app_id,
                    camera_id,
                    exc_info=True,
                )
        try:
            self._publisher.close()
        except Exception:  # pragma: no cover - defensive
            logger.debug("engine backend: publisher close failed", exc_info=True)


# ---------------------------------------------------------------------------
# Zone geometry
# ---------------------------------------------------------------------------


def _anchor_str(value: Any) -> Optional[str]:
    """A media anchor as the string the wire declares, or ``None`` for "absent".

    ``rtp_number`` reaches us as an ``int`` from some workers and a ``str`` from others
    (``engine/contract/schemas.py`` says so where it coerces on the parse path). That parse
    path does not run here: the per-frame value goes to ``Session.process_frame``, which puts
    it on the model with ``model_copy(update=...)`` -- and ``model_copy`` does **not**
    validate. An int would therefore travel all the way to the wire as an int and fail
    contract Section 1 rule 7 at the conformance check. Coerce once, here.

    ``0`` is the "not an RTSP source" sentinel every producer already maps to ``""``
    (``post_proc_runner.py``, ``workers.py``), so it is absent rather than an anchor.
    """
    if value is None or value == "" or value == 0:
        return None
    return str(value)


def _stream_value(stream_info: Dict[str, Any], *aliases: str) -> Optional[str]:
    """The first non-empty value under any of ``aliases``, at the root or in ``camera_info``."""
    containers = (stream_info, stream_info.get("camera_info"), stream_info.get("input_settings"))
    for container in containers:
        if not isinstance(container, dict):
            continue
        for alias in aliases:
            value = container.get(alias)
            if value:
                return str(value)
    return None


def _iter_config_documents(configs: Any) -> List[Dict[str, Any]]:
    """Flatten what the config API returns into a flat list of documents.

    The endpoint's element type is not uniform -- an element is either a document or a list of
    them -- so this flattens one level rather than assuming either shape.
    """
    documents: List[Dict[str, Any]] = []
    if not isinstance(configs, (list, tuple)):
        configs = [configs]
    for item in configs:
        if isinstance(item, dict):
            documents.append(item)
        elif isinstance(item, (list, tuple)):
            documents.extend(entry for entry in item if isinstance(entry, dict))
    return documents


def _as_points(raw: Any) -> Optional[List[Tuple[float, float]]]:
    """``raw`` as a list of ``(x, y)`` pairs, whichever of the two shapes it arrived in.

    ``ZoneConfig.lines`` is typed ``list[float] | list[list[float]]`` -- a line may be the flat
    ``[x, y]`` form, not only ``[[x1,y1],[x2,y2]]`` -- so a converter that assumes list-of-points
    would silently drop every line-based app (footfall, line_crossing). ``None`` means the value is
    not coordinates at all.
    """
    if not isinstance(raw, (list, tuple)) or not raw:
        return None
    if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in raw):
        if len(raw) < 2 or len(raw) % 2:
            return None
        return [(float(raw[i]), float(raw[i + 1])) for i in range(0, len(raw), 2)]

    points: List[Tuple[float, float]] = []
    for point in raw:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            return None
        try:
            points.append((float(point[0]), float(point[1])))
        except (TypeError, ValueError):
            return None
    return points or None


_ABSOLUTE_PIXEL_PRIMITIVES: Final[frozenset] = frozenset({"keypoint_pose", "segmentation_area", "velocity_state"})
"""Stages that turn ``FrameContext.require_resolution`` into a reported figure.

Zone membership is scale-invariant, so a substituted resolution cannot change it. A distance, an
area or a speed is not: for these three the number *is* the answer, and a resolution derived from
anywhere but the frame would be a wrong measurement rather than a harmless scale.
"""


def _geometry_fingerprint(stream_info: Dict[str, Any]) -> str:
    """Stable identity of the geometry a session was built from.

    Sorted by name, because the config arrives as JSON and a re-fetch that returned the same
    polygons in a different key order must not read as a redraw and rebuild the session.
    """
    config = _first_zone_config(stream_info) or {}
    parts = []
    for field_name in ("zones", "lines"):
        shapes = config.get(field_name) or {}
        if isinstance(shapes, dict):
            for name in sorted(shapes):
                parts.append(f"{field_name}:{name}:{shapes[name]}")
    return "|".join(parts) or "-"


def _first_zone_config(stream_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """The ``zone_config`` the caller supplied, under any spelling, or ``None``."""
    containers = (stream_info, stream_info.get("camera_info"), stream_info.get("input_settings"))
    for container in containers:
        if not isinstance(container, dict):
            continue
        for alias in ("zone_config", "zoneConfig"):
            value = container.get(alias)
            if isinstance(value, dict) and value:
                return value
    return None


def _declared_resolution(zone_config: Any) -> Optional[Tuple[int, int]]:
    """``(width, height)`` a raw ``zone_config`` declares, or ``None``.

    Read off the **raw** document, before :func:`normalize_zone_config` drops it: ``ZoneConfig``
    declares only ``zones`` and ``lines``, and that function's output shape is consumed by
    ``ml-codebases/yolo_code_base/inference/workers.py`` from a repo that ships separately -- so
    the resolution travels out of band rather than by widening a published contract.
    """
    if not isinstance(zone_config, dict):
        return None
    resolution = zone_config.get("resolution")
    if not isinstance(resolution, dict):
        return None
    try:
        width, height = int(resolution.get("width") or 0), int(resolution.get("height") or 0)
    except (TypeError, ValueError):
        return None
    return (width, height) if width > 0 and height > 0 else None


def _clamp_unit(value: float) -> float:
    """``value`` inside ``[0, 1]``.

    ``ZoneConfig`` validates to 0-1 with only a 1e-6 tolerance and **raises** outside it, taking
    the whole stream down. A polygon drawn flush to the frame edge routinely lands a pixel over
    (``1051`` against a width of ``1050`` -> ``1.00095``), and refusing a camera over one pixel of
    rounding is worse than snapping it to the edge it was clearly drawn on.
    """
    return 0.0 if value < 0.0 else (1.0 if value > 1.0 else value)


def _normalize_points(raw: Any, width: float, height: float) -> Optional[List[List[float]]]:
    """``raw`` in the unit square, or ``None`` when it cannot be expressed there.

    Scaled **only** when a coordinate is outside 0-1, per polygon -- the same test
    ``PostProcessingConfigClient._is_normalized_points`` makes. This is why the module does not
    simply divide by the resolution: the API returns polygons in **either** space, so the
    unconditional divide the hand-patched containers used collapses an already-normalized zone into
    a dot near the origin.
    """
    points = _as_points(raw)
    if points is None:
        return None
    if all(0.0 <= x <= 1.0 and 0.0 <= y <= 1.0 for x, y in points):
        return [[x, y] for x, y in points]
    if width <= 0 or height <= 0:
        return None
    return [[_clamp_unit(x / width), _clamp_unit(y / height)] for x, y in points]


def normalize_zone_config(zone_config: Any) -> Optional[Dict[str, Any]]:
    """A ``zone_config`` with every polygon in the unit square, or ``None`` when it declares none.

    The engine's geometry takes normalized zones plus a pixel resolution
    (``SceneGeometry.from_zone_config``), and it **raises** on a coordinate outside 0-1 rather than
    coercing it -- so a polygon that cannot be normalized is dropped here, with a warning, instead
    of being handed over to fail the whole stream.

    Public because a worker that already holds its camera's geometry should override the API lookup
    rather than duplicate this conversion -- ``yolo_code_base/inference/workers.py`` does exactly
    that. There is one correct normalization and it lives here.
    """
    if not isinstance(zone_config, dict):
        return None
    resolution = zone_config.get("resolution")
    resolution = resolution if isinstance(resolution, dict) else {}
    try:
        width = float(resolution.get("width") or 0)
        height = float(resolution.get("height") or 0)
    except (TypeError, ValueError):
        width = height = 0.0

    out: Dict[str, Any] = {}
    for field in ("zones", "lines"):
        source = zone_config.get(field)
        if not isinstance(source, dict):
            continue
        converted: Dict[str, Any] = {}
        for name, points in source.items():
            polygon = _normalize_points(points, width, height)
            if polygon is None:
                logger.warning(
                    "engine backend: dropping %s %r -- its coordinates are outside the unit "
                    "square and the zone_config declares no usable resolution to scale by "
                    "(resolution=%r)",
                    field[:-1],
                    name,
                    resolution or None,
                )
                continue
            converted[str(name)] = polygon
        if converted:
            out[field] = converted

    if not out:
        return None
    out.setdefault("zones", {})
    out.setdefault("lines", {})
    return out


# ---------------------------------------------------------------------------
# agg_summary shape bridge (PY-5)
# ---------------------------------------------------------------------------

LEGACY_AGG_SHAPE_ENV: Final[str] = "MATRICE_LEGACY_AGG_SUMMARY_SHAPE"
"""Off switch for :func:`legacy_shape_agg_summary`. **Default on.**

Read on every call rather than at import, deliberately: that makes ``docker restart`` with
``MATRICE_LEGACY_AGG_SUMMARY_SHAPE=0`` a complete rollback of the shape change, with no rebuild and
no redeploy. Accepts ``0`` / ``false`` / ``no`` / ``off`` (case-insensitive) to disable.
"""

#: The per-category count lists on a ``tracking_stats``. ``current_counts`` is deliberately absent
#: -- it is recomputed from the merged detections instead. See :func:`_merge_tracking_stats`.
_SUMMED_COUNT_KEYS: Final[Tuple[str, ...]] = (
    "current_new_counts",
    "total_counts",
    "total_current_counts",
)


def _legacy_shape_enabled() -> bool:
    raw = str(os.environ.get(LEGACY_AGG_SHAPE_ENV, "") or "").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def _frame_key(stream_info: Dict[str, Any]) -> str:
    """The legacy ``agg_summary`` key: this frame's number, as a string.

    Legacy use cases key on ``str(frame_number)`` (e.g. ``people_counting.py:674``). The number is
    in ``input_settings.start_frame``, which every worker builder sets; ``frame_id`` carries it as a
    trailing ``_<n>`` when it does not. ``"current_frame"`` is the last resort -- one of the four
    keys PY-5 records consumers already coping with, so it is a shape they have seen.
    """
    settings = stream_info.get("input_settings")
    if isinstance(settings, dict):
        for key in ("start_frame", "end_frame"):
            value = settings.get(key)
            if isinstance(value, int):
                return str(value)
            try:
                if value is not None and str(value).strip():
                    return str(int(str(value).strip()))
            except (TypeError, ValueError):
                pass

    tail = str(stream_info.get("frame_id") or "").rsplit("_", 1)[-1]
    if tail.isdigit():
        return tail
    return "current_frame"


def _detection_key(detection: Any) -> Any:
    """An identity for a detection, for dedupe when merging zones.

    ``track_id`` when the app tracks, else the bbox corners plus the category. Needed because
    ``overlap: all_match`` (``primitives/geometry.py`` ``OverlapPolicy``) counts one detection in
    **every** zone containing it, so zone entries are not always a partition of the frame.
    """
    if not isinstance(detection, dict):
        return id(detection)
    track_id = detection.get("track_id")
    if track_id is not None:
        return ("track", track_id)
    box = detection.get("bounding_box")
    corners = tuple(box.get(c) for c in ("xmin", "ymin", "xmax", "ymax")) if isinstance(box, dict) else ()
    return ("box", corners, detection.get("category"))


def _sum_counts(count_lists: List[Any]) -> List[Dict[str, Any]]:
    """Sum ``[{"category": c, "count": n}, ...]`` lists per category, order preserved."""
    totals: Dict[str, int] = {}
    for counts in count_lists:
        if not isinstance(counts, (list, tuple)):
            continue
        for item in counts:
            if not isinstance(item, dict):
                continue
            category = str(item.get("category", ""))
            try:
                totals[category] = totals.get(category, 0) + int(item.get("count", 0) or 0)
            except (TypeError, ValueError):
                continue
    return [{"category": category, "count": count} for category, count in totals.items()]


def _counts_from_detections(detections: List[Any]) -> List[Dict[str, Any]]:
    """Per-category counts of ``detections``, order of first appearance preserved."""
    totals: Dict[str, int] = {}
    for detection in detections:
        if not isinstance(detection, dict):
            continue
        category = str(detection.get("category", ""))
        totals[category] = totals.get(category, 0) + 1
    return [{"category": category, "count": count} for category, count in totals.items()]


def _merge_tracking_stats(entries: Sequence[Tuple[str, Dict[str, Any]]]) -> Dict[str, Any]:
    """One frame-level ``tracking_stats`` from the per-zone ones.

    ``detections`` are concatenated and **deduped** by :func:`_detection_key`, and
    ``current_counts`` is then recomputed from that deduped list rather than summed. This is the
    one field that has to be derived rather than added: be-analytics resolves its ``total_count``
    and ``category_total_count`` instant metrics from ``current_counts`` (**BE-16**), and under
    ``overlap: all_match`` a sum would count one person standing in two zones twice.

    The cumulative lists (``total_counts`` and friends) *are* summed, because a frame's detections
    cannot reconstruct a running total. Under ``all_match`` those inherit the engine's own
    documented ``sum(per_zone) >= occupancy`` behaviour -- the bridge does not invent a number the
    engine was not already publishing.
    """
    merged: Dict[str, Any] = {}
    seen: set = set()
    detections: List[Any] = []
    human_texts: List[str] = []

    for _zone, stats in entries:
        for detection in stats.get("detections") or []:
            key = _detection_key(detection)
            if key in seen:
                continue
            seen.add(key)
            detections.append(detection)
        text = str(stats.get("human_text") or "").strip()
        if text and text not in human_texts:
            human_texts.append(text)
        # Timestamps are frame-level and identical across zones; first non-empty wins.
        for key in ("input_timestamp", "reset_timestamp"):
            if not merged.get(key) and stats.get(key):
                merged[key] = stats[key]

    merged["detections"] = detections
    merged["current_counts"] = _counts_from_detections(detections)
    for key in _SUMMED_COUNT_KEYS:
        merged[key] = _sum_counts([stats.get(key) for _zone, stats in entries])
    if human_texts:
        merged["human_text"] = "; ".join(human_texts)
    return merged


def legacy_shape_agg_summary(
    agg_summary: Optional[Dict[str, Any]],
    stream_info: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Re-key a zone-keyed engine ``agg_summary`` into the legacy frame-keyed shape (PY-5).

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
    if not agg_summary or not isinstance(agg_summary, dict) or not _legacy_shape_enabled():
        return agg_summary

    # Already legacy-shaped: every key is a frame number. Converting again would nest a frame
    # inside a frame, so a double call must be a no-op.
    if all(str(key).isdigit() for key in agg_summary):
        return agg_summary

    entries: List[Tuple[str, Dict[str, Any]]] = [
        (str(zone), entry) for zone, entry in agg_summary.items() if isinstance(entry, dict)
    ]
    if not entries:
        return agg_summary

    zone_analysis: Dict[str, Any] = {}
    alerts: List[Any] = []
    incidents: Dict[str, Any] = {}
    business_analytics: Dict[str, Any] = {}
    tracking_entries: List[Tuple[str, Dict[str, Any]]] = []

    for zone, entry in entries:
        stats = entry.get("tracking_stats")
        stats = stats if isinstance(stats, dict) else {}
        tracking_entries.append((zone, stats))

        # The per-zone view, preserved. Legacy's `zone_analysis` is per-zone counts, and the
        # `__global__` spelling is what a zoneless legacy app uses (`people_counting.py:465`).
        zone_analysis[zone] = {
            "current_counts": stats.get("current_counts") or [],
            "total_counts": stats.get("total_counts") or [],
            "human_text": stats.get("human_text") or "",
        }

        for alert in entry.get("alerts") or []:
            alerts.append(alert)
        for source, target in (
            (entry.get("incidents"), incidents),
            (entry.get("business_analytics"), business_analytics),
        ):
            if isinstance(source, dict):
                for key, value in source.items():
                    # First non-empty wins: a later zone must not blank a populated field.
                    if key not in target or not target[key]:
                        target[key] = value

    tracking_stats = _merge_tracking_stats(tracking_entries)
    human_text = tracking_stats.pop("human_text", "")
    tracking_stats["zone_analysis"] = zone_analysis

    return {
        _frame_key(stream_info): {
            "incidents": incidents,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "zone_analysis": zone_analysis,
            "human_text": human_text,
        }
    }


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def source_dims_of(stream_info: Dict[str, Any]) -> Optional[Tuple[int, int]]:
    """``(width, height)`` from a stream_info, or ``None`` when it declares no resolution."""
    resolution = stream_info.get("stream_resolution")
    if not isinstance(resolution, dict):
        return None
    width, height = resolution.get("width"), resolution.get("height")
    if not width or not height:
        return None
    try:
        return int(width), int(height)
    except (TypeError, ValueError):
        return None


def select_engine_backend(
    app_ref: Optional[str],
    *,
    redis_config: Optional[Dict[str, Any]] = None,
    app_name: Optional[str] = None,
    post_processing_config: Any = None,
    identity: Optional[Dict[str, Any]] = None,
    bundle_refs: Optional[Sequence[Any]] = None,
) -> Optional["EngineBackend"]:
    """Route once: an :class:`EngineBackend` for a manifest app, ``None`` for the legacy path.

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
    from ..engine.manifest.loader import redact_url
    from ..engine.routing import resolve_flow_mode, route_app
    from .app_bundle import AppBundleError, resolve_app_bundle_refs

    if resolve_flow_mode() == "old":
        # The off switch has to stay unconditional. A bundle reference is a statement about where
        # the app lives, not a request to override an operator who has turned the engine off.
        candidates: Tuple[Any, ...] = ()
    elif bundle_refs is None:
        candidates = resolve_app_bundle_refs(post_processing_config, app_name=app_name, identity=identity)
    else:
        candidates = tuple(bundle_refs)

    if not candidates:
        # No bundle reference: the line this function has always run, unchanged.
        decision = route_app(app_ref)
    else:
        decision = None
        failures: List[str] = []
        for candidate in candidates:
            try:
                reference = candidate.resolve()
                loader = _bundle_loader(trusted=bool(getattr(candidate, "trusted", False)))
                attempt = route_app(reference, loader=loader)
            except AppBundleError as exc:
                failures.append(f"{candidate.via}: {exc}")
                continue
            except Exception as exc:  # noqa: BLE001 - every loader error is a candidate failure
                failures.append(f"{candidate.via}: {type(exc).__name__}: {exc}")
                continue
            if attempt.use_new_engine:
                logger.info("analytics routing: app bundle via %s -> engine", candidate.via)
                decision = attempt
                break
            failures.append(f"{candidate.via} -> {redact_url(reference)}: {attempt.reason}")

        if decision is None:
            listed = "\n".join(f"  - {line}" for line in failures)
            asserted = [c for c in candidates if not getattr(c, "speculative", False)]
            if not asserted:
                # Every candidate was *inferred* from identity the deployment happened to carry --
                # nobody said this app has a bundle. It may simply mean the application version has
                # none, which is the legacy answer, so this must not raise: that would take down
                # every legacy app in the fleet the day be-inference starts forwarding the version.
                #
                # But it is a WARNING, not an INFO. An app whose manifest exists and whose operator
                # expects the engine looks *identical* here to an app that has no bundle at all, and
                # the consequences of the two differ completely: the engine app quietly runs on the
                # legacy path with configuration authored for the manifest, which is how a
                # `TypeError: DwellConfig.__init__() got an unexpected keyword argument 'method'`
                # reaches a legacy dataclass at all. The candidate list below names every reference
                # tried and why each failed; a 401/403/404 on the download route usually means
                # `MATRICE_LICENSE_KEY` is not set in this container, which py_compute forwards only
                # when the manager's own environment has it (`action_instance.py:731`).
                logger.warning(
                    "analytics routing: no app bundle loaded for this version, so this app is "
                    "running on the LEGACY path. If it was expected to run on the analytics engine, "
                    "one of the candidates below is the reason -- a 401/403/404 on the download "
                    "route usually means MATRICE_LICENSE_KEY is missing from this container.\n%s",
                    listed,
                )
                decision = route_app(app_ref)
            else:
                raise BackendError(
                    f"An app bundle was configured for this deployment but none of the "
                    f"{len(candidates)} reference(s) could be loaded, so this app would publish "
                    f"nothing. Refusing to fall back to the legacy path -- a legacy run for an app "
                    f"that has no legacy use case emits plausible zeros, and a plausible zero is "
                    f"indistinguishable from a quiet camera.\n{listed}\n"
                    f"Set $MATRICE_APPS_ROOT to a synced app folder to run offline, or "
                    f"$MATRICE_ANALYTICS_FLOW=old to choose the legacy path deliberately."
                )

    if not decision.use_new_engine:
        # INFO, at the same level as the engine decision below. At DEBUG -- what this was until
        # INF-2606 -- only half of a binary choice was observable in production, so a backend flip
        # across a restart with an unchanged config could not be explained from the logs at all.
        # `decision.reason` is always populated and always names the specific cause.
        logger.info("analytics routing: app %r -> legacy (%s)", app_ref, decision.reason)
        return None

    logger.info("analytics routing: app %r -> engine (%s)", app_ref, decision.reason)
    backend = EngineBackend(
        decision.loaded,
        redis_config=redis_config,
        app_name=app_name,
        post_processing_config=post_processing_config,
    )
    backend.decision = decision
    return backend


def _bundle_loader(*, trusted: bool) -> Any:
    """The loader ``route_app`` should use for a bundle candidate.

    A trusted candidate came from the platform API or an operator's env var, so a remote
    ``logic.py`` may be executed; an untrusted one is author-supplied config and gets the
    loader's default trusted-host check (finding F9).
    """
    from ..engine.manifest.loader import load_app_bundle

    if not trusted:
        return load_app_bundle
    return functools.partial(load_app_bundle, allow_remote_code=True)


def _has_identity(stream_info: Dict[str, Any], key: str) -> bool:
    """Did the caller already supply this field, under any spelling the engine searches?"""
    aliases = {
        "camera_name": ("camera_name", "cameraName", "name"),
        "app_id": ("app_id", "appId", "application_id", "applicationId"),
        "app_deployment_id": ("app_deployment_id", "appDeploymentId", "deployment_id", "deploymentId"),
        "application_name": ("application_name", "applicationName"),
        "application_key_name": ("application_key_name", "applicationKeyName"),
        "application_version": ("application_version", "applicationVersion"),
        "zone_config": ("zone_config", "zoneConfig"),
        # The three spellings `stream_info.FIELD_ALIASES` searches for the resolution. Without
        # this entry the gap-fill below would overwrite a resolution the caller *did* send under
        # a non-canonical name, which is the one thing `enrich` promises never to do.
        "stream_resolution": ("stream_resolution", "streamResolution", "resolution"),
    }.get(key, (key,))
    containers = (stream_info, stream_info.get("camera_info"), stream_info.get("input_settings"))
    return any(isinstance(container, dict) and container.get(alias) for container in containers for alias in aliases)


def _display_name(app_name: Optional[str]) -> Optional[str]:
    """The runner's ``app_name`` when it is a name, not a reference.

    ``app_name`` is overloaded: ``py_inference`` passes the real
    ``job_params["application_name"]``, but :func:`route_app` also accepts a folder path or a zip
    URL there, and a filesystem path in ``application_name`` would land in ClickHouse as the
    application's name. When it looks like a reference, ``manifest.app.name`` is used instead --
    which is the same value, authored in ``app.yaml``.
    """
    text = (app_name or "").strip()
    if not text or "/" in text or "\\" in text or text.endswith(".zip") or "://" in text:
        return None
    return text


def _config_value(config: Any, key: str) -> Optional[str]:
    """Read a key out of whatever shape ``post_processing_config`` arrived in."""
    if isinstance(config, dict):
        value = config.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _jpeg_dims(data: bytes) -> Optional[Tuple[int, int]]:
    """``(width, height)`` from a JPEG's SOF marker, or ``None``.

    ``workers.py:1129`` hands the runner ``jpeg_buf.tobytes()``, so the frame's real dimensions are
    already in the bytes we were given -- there is no need to ask the worker for them. Walking the
    marker chain is a dozen lines and no dependency; decoding the image would cost a JPEG decode
    per frame for two integers.
    """
    if data[:2] != b"\xff\xd8":
        return None
    index, end = 2, len(data)
    while index + 9 < end:
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        # SOF0..SOF15, excluding the DHT/JPG/DAC markers that share the range.
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height = int.from_bytes(data[index + 5 : index + 7], "big")
            width = int.from_bytes(data[index + 7 : index + 9], "big")
            return (width, height) if width and height else None
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            index += 2
            continue
        index += 2 + int.from_bytes(data[index + 2 : index + 4], "big")
    return None


def _array_dims(frame: Any) -> Optional[Tuple[int, int]]:
    """``(width, height)`` from an HWC image array. ``ultralytics_worker.py:507`` passes one."""
    shape = getattr(frame, "shape", None)
    if not isinstance(shape, tuple) or len(shape) < 2:
        return None
    height, width = shape[0], shape[1]
    if not isinstance(height, int) or not isinstance(width, int) or not (height and width):
        return None
    return width, height


def _boxes_look_normalised(detections: Any) -> bool:
    """True when nothing in this frame is outside the unit square, so no conversion is needed."""
    if not isinstance(detections, (list, tuple)):
        return False
    for detection in detections:
        if not isinstance(detection, dict):
            continue
        for key in ("bounding_box", "bbox"):
            box = detection.get(key)
            if not isinstance(box, dict):
                continue
            for corner in ("xmin", "ymin", "xmax", "ymax"):
                try:
                    if float(box.get(corner, 0)) > 1.5:
                        return False
                except (TypeError, ValueError):
                    return False
    return True


def resolve_source_dims(
    stream_info: Dict[str, Any],
    input_bytes: Any = None,
) -> Optional[Tuple[int, int]]:
    """The frame's ``(width, height)``, from whichever of four places actually has it.

    No worker in ml-codebases puts a resolution in ``stream_info`` -- the string
    ``stream_resolution`` does not appear in that repo. But both yolo workers hand us the frame
    itself, so the dimensions are in our hands already; they just have to be looked for. Order:

    1. ``stream_info["stream_resolution"]`` -- what :func:`build_stream_info` writes for a caller
       that passed ``source_dims``;
    2. ``input_bytes`` as an image array (``ultralytics_worker.py:507`` passes ``bgr_frames[i]``);
    3. ``input_bytes`` as JPEG (``workers.py:1129``).

    ``None`` means none of them had it, and the caller decides what that is worth.
    """
    return (
        source_dims_of(stream_info)
        or _array_dims(input_bytes)
        or (_jpeg_dims(input_bytes) if isinstance(input_bytes, (bytes, bytearray)) else None)
    )


def _boxes_to_unit_square(detections: Any, stream_info: Dict[str, Any], input_bytes: Any = None) -> Any:
    """Put boxes in the unit square, which is the only space the engine accepts.

    The runner's contract with its callers is SOURCE-PIXEL detections (module docstring, "bbox
    contract"). The engine's contract is the opposite and it is strict: a box outside 0-1 **raises**
    rather than being coerced, deliberately, because a pixel box silently treated as normalized is
    a 1920x error nobody notices (``engine/runtime/session.py`` ``_to_detection``).

    The conversion happens here, using the runner's own pure helper -- itself idempotent, so a
    producer that already sends normalized boxes is untouched.
    """
    dims = resolve_source_dims(stream_info, input_bytes)
    if dims is None:
        return detections
    from .post_proc_runner import normalize_detections

    return normalize_detections(detections, dims)


def require_engine_ready(
    stream_info: Optional[Dict[str, Any]],
    app_id: str,
    *,
    input_bytes: Any = None,
    detections: Any = None,
    manifest: Any = None,
    zone_answer: Any = None,
) -> None:
    """Refuse an engine backend that could never produce a usable frame.

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
    if stream_info is None:
        return

    if resolve_source_dims(stream_info, input_bytes) is None and not _boxes_look_normalised(detections):
        raise BackendError(
            f"app {app_id!r} routes to the analytics engine, but this frame's dimensions cannot be "
            f"determined and its boxes are not already in the unit square. The engine requires "
            f"normalized boxes and the runner is documented to receive source pixels, so nothing "
            f"can be converted. Looked in: stream_info['stream_resolution'], and input_bytes as an "
            f"image array or JPEG. Fix by passing source_dims= to run(), or building stream_info "
            f"with source_dims set."
        )

    # The engine's own resolver produces a far better message than anything reconstructed here --
    # it names every missing field and every spelling it searched for.
    from ..engine.contract.schemas import StreamInfoError
    from ..engine.runtime.stream_info import resolve_stream_info

    try:
        resolve_stream_info(stream_info)
    except StreamInfoError as exc:
        raise BackendError(
            f"app {app_id!r} routes to the analytics engine, but this stream_info is not usable "
            f"by it. The legacy flow tolerates these absences; the engine does not, because they "
            f"become the results-agg envelope and a fabricated default would land in ClickHouse "
            f"as real identity. The SDK already derives everything it legitimately can -- what is "
            f"listed below is what only the caller knows.\n{exc}"
            f"\nThis camera is DEFERRED, not refused -- the runner re-tests it periodically, "
            f"so a field that appears late (a config API that was down, an identity the "
            f"platform had not resolved yet) takes effect without a container restart.",
            retryable=True,
        ) from exc

    _require_geometry(stream_info, app_id, manifest=manifest, zone_answer=zone_answer)


def _require_geometry(stream_info: Dict[str, Any], app_id: str, *, manifest: Any, zone_answer: Any) -> None:
    """Refuse -- retryably -- a ``zones.required: true`` app whose camera has no geometry.

    This is the failure the readiness gate used to miss entirely. ``Session.__init__`` raises
    ``SessionError`` for it, and because the session is only cached on success the construction
    re-ran and re-raised on **every frame**, logged WARNING once and DEBUG forever, and returned
    an empty result indistinguishable from a camera nobody walked past.

    Retryable because the fix is a database write, not a code change: the moment the pointer is
    corrected -- or the operator draws the zone -- the resolver's next refresh finds it, and the
    camera must come back **without a container restart**. A permanent refusal here would make
    the whole retry/TTL design pointless.
    """
    zones_spec = getattr(manifest, "zones", None) if manifest is not None else None
    if zones_spec is None or not getattr(zones_spec, "required", False):
        return

    config = _first_zone_config(stream_info) or {}
    if config.get("zones"):
        return

    detail = getattr(zone_answer, "reason", "") or "no geometry was returned for this camera"
    pointer = getattr(zone_answer, "stored_pointer", None)
    deployment = _stream_value(stream_info, "app_deployment_id", "appDeploymentId", "deployment_id", "deploymentId")
    raise BackendError(
        f"app {app_id!r} declares zones.required: true, and camera "
        f"{stream_info.get('camera_id')!r} has no zone geometry, so it can only ever publish "
        f"empty frames. Looked it up by app deployment {deployment!r} at "
        f"{app_bundle_zone_path(deployment)}"
        + (f" (the stored _idAppDeployment is {pointer!r})" if pointer else "")
        + f". {detail}. Draw a zone for this camera, or correct the stored _idAppDeployment -- "
        "note that re-saving the zone from the UI does NOT repair it, because the update route "
        "writes only postProcessing. This camera will start on its own once the geometry "
        "resolves; nothing needs restarting.",
        retryable=True,
    )


def app_bundle_zone_path(deployment_id: Optional[str]) -> str:
    """The URL the geometry lookup used, for an error an operator can act on."""
    from .app_bundle import POST_PROCESSING_CONFIGS_PATH

    return POST_PROCESSING_CONFIGS_PATH.format(app_deployment_id=deployment_id or "<unknown>")


def _outcome_as_result(outcome: Any, manifest: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
    """A ``ProcessingResult``-shaped view of a :class:`FrameOutcome`.

    The runner promises callers a ``"result"`` that reads like a legacy ``ProcessingResult``. Only
    the fields that carry meaning for a manifest app are filled; inventing values for the rest
    (``processing_time``, ``insights``) would make the two backends look more alike than they are.
    """
    return {
        "status": "success",
        "usecase": manifest.app.id,
        "category": manifest.app.category,
        "data": payload,
        "metrics": dict(outcome.metric_values),
        "warnings": [],
        "timestamp": outcome.frame_ts,
    }


def _unwrap_agg_summary(result: Any) -> Optional[Dict[str, Any]]:
    """Re-exported from the runner so the legacy backend keeps its exact unwrap behaviour."""
    from .post_proc_runner import _unwrap_agg_summary as unwrap

    return unwrap(result)


def _result_as_dict(result: Any) -> Dict[str, Any]:
    """Re-exported from the runner so the legacy backend keeps its exact result shape."""
    from .post_proc_runner import _result_as_dict as as_dict

    return as_dict(result)
