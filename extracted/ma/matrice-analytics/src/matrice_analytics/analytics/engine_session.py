"""Per-camera AnalyticsEngine session — the new-flow runtime, SDK-side.

``PostProcessor`` creates one :class:`AnalyticsEngineSession` per ``stream_key``
(camera) when the deployment's app routes to the new flow (see
:func:`matrice_analytics.analytics.flow.resolve_manifest_for_app`). The session
owns everything the inference pipeline used to do externally:

- build :class:`StreamInfo` from the per-frame ``stream_info`` dict the pipeline
  already passes to ``PostProcessor.process()``;
- map numeric category ids to entity names (the engine wants names);
- run an internal :class:`AdvancedTracker` for stable track ids (the engine has
  no tracker of its own — same arrangement the legacy use-cases use, so the
  pipeline's CCTVTracker stays off);
- drive the :class:`AnalyticsEngine`, drain incident events to ``incident_res``
  and publish 60s aggregations to ``results-agg`` via
  :class:`~matrice_analytics.analytics.redis_publisher.AnalyticsRedisPublisher`;
- return the per-frame ``agg_summary`` for the per-camera output topic.

The returned per-frame ``agg_summary`` deliberately carries no count lists, so
the legacy ``AnalyticsPublisher`` (which the inference pipeline still feeds)
skips it — results-agg comes solely from this session's authoritative
``engine.aggregate()``, with no double-publish.
"""

import logging
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_OBJECT_ID_RE = re.compile(r"^[0-9a-f]{24}$", re.IGNORECASE)
_UNKNOWN_LOCATION_LABELS = frozenset({"Unknown Location", "unknown location"})


_COCO_MARKER_LABELS = frozenset(
    {
        "bus",
        "truck",
        "motorcycle",
        "airplane",
        "boat",
        "train",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
    }
)

# Default COCO-80 names at indices 0–9. The deployment UI overlays these strings
# on custom PPE model indices (same index, wrong label): Hardhat→person, Mask→bicycle,
# NO-Mask→motorcycle, Person→bus, Safety Vest→truck, etc. See
# build_coco_harness_mislabel_lookup() for the reverse map used in post-processing.
_COCO_DEFAULT_CLASS_NAMES: Dict[int, str] = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    4: "airplane",
    5: "bus",
    6: "train",
    7: "truck",
    8: "boat",
    9: "traffic light",
}


def build_coco_harness_mislabel_lookup(
    model_index_to_category: Dict[int, str],
) -> Dict[str, int]:
    """Map wrong COCO string labels back to custom-model class ids.

    The inference harness labels PPE model outputs with COCO names at the same
    numeric index (e.g. class 0 → ``person`` instead of ``Hardhat``,
    class 5 → ``bus`` instead of ``Person``). When ``class_id`` is stripped
    and only the wrong string remains, reverse via the default COCO name at
    each model index.
    """
    lookup: Dict[str, int] = {}
    for model_id, model_label in model_index_to_category.items():
        coco_name = _COCO_DEFAULT_CLASS_NAMES.get(model_id)
        if not coco_name:
            continue
        if coco_name.lower() != str(model_label).strip().lower():
            lookup[coco_name.lower()] = model_id
    return lookup


def looks_like_coco_index_to_category(mapping: Optional[Dict[int, str]]) -> bool:
    """Heuristic: deployment UI often ships a generic COCO map for custom models."""
    if not mapping:
        return False
    if len(mapping) > 20:
        return True
    lowered = {str(v).strip().lower() for v in mapping.values()}
    if lowered & _COCO_MARKER_LABELS:
        return True
    # PPE model class ids that COCO mislabels on the harness overlay path.
    if str(mapping.get(5, "")).lower() == "bus":
        return True
    if str(mapping.get(3, "")).lower() == "motorcycle":
        return True
    if str(mapping.get(7, "")).lower() == "truck":
        return True
    return False


def looks_like_wrong_ppe_index_to_category(mapping: Optional[Dict[int, str]]) -> bool:
    """Detect incomplete or mis-typed PPE maps (e.g. ``{0: 'Person'}`` from the UI)."""
    norm = normalize_index_to_category(mapping)
    if not norm:
        return False
    if looks_like_coco_index_to_category(norm):
        return True
    # PPE class 0 is Hardhat; Person at index 0 is always a bad deployment default.
    if str(norm.get(0, "")).strip().lower() == "person":
        return True
    return False


def detection_class_id_from_detection(det: Dict[str, Any]) -> Optional[int]:
    """Best-effort numeric class id from common inference field names.

    Prefer ``category_id`` / ``cls`` / ``class`` before ``class_id`` — the
    harness often sticks ``class_id`` at 0 while ``category_id`` still carries
    the true model class.
    """
    for key in ("category_id", "cls", "class", "class_id"):
        raw = det.get(key)
        if raw is None:
            continue
        try:
            return int(raw)
        except (TypeError, ValueError):
            continue
    return None


def map_detection_categories(
    detections: List[Dict[str, Any]],
    index_to_category: Optional[Dict[Any, Any]],
    *,
    ppe_coco_fixup: bool = False,
) -> List[Dict[str, Any]]:
    """Map detections to labels from ``index_to_category`` config.

    Shared by new-flow AnalyticsEngineSession and legacy ``ppe_compliance``.

    PPE harness reality (``ppe_coco_fixup=True``):
      - ``class_id`` is often stuck at 0 for every box — do not trust it alone.
      - Category string is the COCO name at the PPE model index:
        person→Hardhat, bicycle→Mask, …, bus→Person, truck→Safety Vest, …
      Priority:
        1. COCO harness strings (primary path)
        2. Keep known PPE labels already on the detection
        3. ``category_id`` / ``cls`` / ``class`` when present and not stuck-only
           via ``class_id`` (prefer those keys over ``class_id``)
        4. Numeric category field
    """
    mapping = normalize_index_to_category(index_to_category)
    if not mapping:
        return detections

    config_values = {str(v).strip() for v in mapping.values()}
    config_values_lower = {v.lower(): v for v in config_values}
    coco_string_fix = build_coco_harness_mislabel_lookup(mapping) if ppe_coco_fixup else {}
    coco_mislabel_strings = set(coco_string_fix.keys())

    for det in detections:
        cat = det.get("category")
        cat_stripped = cat.strip() if isinstance(cat, str) else ""
        cat_lower = cat_stripped.lower()

        # 1) COCO harness overlay names FIRST (class_id is unreliable / stuck at 0).
        #    Match lowercase COCO strings only — title-case "Person" is a real PPE
        #    label and must not be treated as COCO "person" → Hardhat.
        if coco_string_fix and cat_lower in coco_mislabel_strings and cat_stripped not in config_values:
            model_id = coco_string_fix[cat_lower]
            if model_id in mapping:
                det["category"] = mapping[model_id]
                continue

        # 2) Already a PPE config label (e.g. "Person", "Safety Vest") — keep it.
        if cat_stripped in config_values:
            det["category"] = cat_stripped
            continue

        if cat_lower in config_values_lower and cat_lower not in coco_mislabel_strings:
            det["category"] = config_values_lower[cat_lower]
            continue

        # 3) Numeric id — prefer category_id/cls/class over stuck class_id.
        cid = detection_class_id_from_detection(det)
        if cid is not None and cid in mapping:
            # Ignore class_id==0 when category is already a known PPE string handled
            # above; if we reached here, category was unknown so id is best effort.
            det["category"] = mapping[cid]
            continue

        if isinstance(cat, str) and cat.isdigit():
            idx = int(cat)
            if idx in mapping:
                det["category"] = mapping[idx]
                continue
        elif isinstance(cat, int) and cat in mapping:
            det["category"] = mapping[cat]
            continue

    return detections


def normalize_index_to_category(
    mapping: Optional[Dict[Any, Any]],
) -> Dict[int, str]:
    """Coerce ``index_to_category`` keys to ``int`` (JSON uploads use string keys).

    Values are stripped: this is the other ingestion boundary for the deployment's
    ``class_index_map``, and a single trailing space in it (``"gun "``) once made a
    weapon app detect nothing at all, silently, because an unmapped class is ignored
    rather than rejected. See ``post_processing.utils.filter_utils`` for the same guard
    on the other path -- the two must agree or the bug just moves.
    """
    if not mapping:
        return {}
    out: Dict[int, str] = {}
    for key, value in mapping.items():
        try:
            label = str(value).strip()
            if not label:
                continue
            out[int(key)] = label
        except (TypeError, ValueError):
            continue
    return out


def _pick_nonempty_str(*candidates: Any) -> str:
    """Return the first non-empty string candidate."""
    for value in candidates:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def _camera_id_from_topic(topic: Any) -> str:
    """Extract camera id from ``{camera_id}_input_topic`` stream topic names."""
    if not topic or not isinstance(topic, str):
        return ""
    text = topic.strip()
    suffix = "_input_topic"
    if text.endswith(suffix):
        return text[: -len(suffix)].strip()
    return ""


def _stream_config_dict(stream_info: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve deployment ``stream_config`` from common stream_info shapes."""
    for src in (stream_info, stream_info.get("input_settings") or {}):
        if not isinstance(src, dict):
            continue
        sc = src.get("stream_config")
        if isinstance(sc, dict):
            return sc
    return {}


def _looks_like_object_id(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    return bool(text and _OBJECT_ID_RE.match(text))


def resolve_camera_fields_from_stream_info(
    stream_info: Optional[Dict[str, Any]],
) -> Dict[str, str]:
    """Resolve camera identity fields from the per-frame ``stream_info`` dict.

    Mirrors legacy ``AnalyticsPublisher`` / ``INCIDENT_MANAGER`` lookup paths
    so ``results-agg`` gets the human-readable ``camera_name``, not a duplicate
    of ``camera_id`` when the name lives under ``stream_config`` or nested
    ``input_streams``.
    """
    si = stream_info or {}
    camera_info = si.get("camera_info") if isinstance(si.get("camera_info"), dict) else {}
    input_settings = si.get("input_settings") if isinstance(si.get("input_settings"), dict) else {}
    input_stream = input_settings.get("input_stream") if isinstance(input_settings.get("input_stream"), dict) else {}
    input_camera_info = input_stream.get("camera_info") if isinstance(input_stream.get("camera_info"), dict) else {}

    input_streams = si.get("input_streams") or []
    if input_streams and isinstance(input_streams[0], dict):
        inner = input_streams[0].get("input_stream", input_streams[0])
        if isinstance(inner, dict):
            nested_cam = inner.get("camera_info")
            if isinstance(nested_cam, dict) and nested_cam:
                input_camera_info = nested_cam

    stream_config = _stream_config_dict(si)
    topic_camera_id = _camera_id_from_topic(si.get("topic"))

    camera_id = _pick_nonempty_str(
        si.get("camera_id"),
        si.get("cameraId"),
        camera_info.get("camera_id"),
        camera_info.get("cameraId"),
        input_camera_info.get("camera_id"),
        input_camera_info.get("cameraId"),
        input_settings.get("camera_id"),
        input_settings.get("cameraId"),
        stream_config.get("camera_id"),
        stream_config.get("cameraId"),
        topic_camera_id,
    )

    camera_name = _pick_nonempty_str(
        stream_config.get("camera_name"),
        stream_config.get("cameraName"),
        stream_config.get("name"),
        camera_info.get("camera_name"),
        camera_info.get("cameraName"),
        camera_info.get("name"),
        input_camera_info.get("camera_name"),
        input_camera_info.get("cameraName"),
        input_camera_info.get("name"),
        si.get("camera_name"),
        si.get("cameraName"),
        si.get("name"),
        input_settings.get("camera_name"),
        input_settings.get("cameraName"),
    )

    camera_group = _pick_nonempty_str(
        stream_config.get("camera_group"),
        camera_info.get("camera_group"),
        input_camera_info.get("camera_group"),
        si.get("camera_group"),
        "default",
    )

    location = _pick_nonempty_str(
        stream_config.get("location"),
        stream_config.get("locationName"),
        camera_info.get("location"),
        camera_info.get("locationName"),
        input_camera_info.get("location"),
        input_camera_info.get("locationName"),
        si.get("location"),
        si.get("locationName"),
    )

    location_id = _pick_nonempty_str(
        stream_config.get("location_id"),
        stream_config.get("locationId"),
        si.get("location_id"),
        si.get("locationId"),
        camera_info.get("location_id"),
        camera_info.get("locationId"),
        input_camera_info.get("location_id"),
        input_camera_info.get("locationId"),
    )

    if location in _UNKNOWN_LOCATION_LABELS:
        location = ""

    from ..post_processing.utils.post_processing_config_client import (
        is_null_object_id,
        normalize_location_id,
    )

    if not location_id and _looks_like_object_id(location) and not is_null_object_id(location):
        location_id = location
        location = ""
    elif _looks_like_object_id(location):
        if not location_id and not is_null_object_id(location):
            location_id = location
        location = ""

    location_id = normalize_location_id(location_id)

    if camera_name and camera_id and camera_name == camera_id:
        camera_name = ""

    if camera_group and camera_id and camera_group == camera_id:
        camera_group = "default"

    return {
        "camera_id": camera_id,
        "camera_name": camera_name,
        "camera_group": camera_group,
        "location": location,
        "location_id": location_id,
    }


def resolve_location_for_publish(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """Resolve ``locationId`` and display ``location`` for Redis / results-agg envelopes.

    Mirrors the field lookup paths used for incidents (``camera_info``, ``stream_config``,
    enriched top-level ``stream_info``). Null Mongo ObjectIds are blanked; missing names
    fall back to ``Unknown Location``.
    """
    si = stream_info or {}
    cam_fields = resolve_camera_fields_from_stream_info(si)
    location_id = cam_fields.get("location_id") or ""
    location = cam_fields.get("location") or str(si.get("location") or "").strip()
    if not location:
        location = "Unknown Location"
    return {"location_id": location_id, "locationId": location_id, "location": location}


def _utc_now_iso_z() -> str:
    # timezone.utc (NOT datetime.UTC): datetime.UTC is 3.11+ and this SDK
    # targets 3.8+. Do not let a linter rewrite this to datetime.UTC.
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")  # noqa: UP017


def _utc_now_stream_time() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")  # noqa: UP017


def _empty_tracking_stats_fallback(input_timestamp: str) -> Dict[str, Any]:
    """Harness-compatible skeleton when no zone produced tracking stats."""
    return {
        "global": {
            "input_timestamp": input_timestamp,
            "current_counts": [],
            "current_new_counts": [],
            "total_counts": [],
            "total_current_counts": [],
        }
    }


class AnalyticsEngineSession:
    """One camera's AnalyticsEngine + tracker + publishing wiring."""

    def __init__(
        self,
        manifest_name: str,
        app_name: Optional[str],
        index_to_category: Optional[Dict[int, str]],
        publisher: Any,
        logger_: Optional[logging.Logger] = None,
    ):
        # Imported here so PostProcessor can lazily route only when the new
        # analytics subpackage is present (old installs stay on legacy).
        from .engine import AnalyticsEngine

        self._engine_cls = AnalyticsEngine
        self.manifest_name = manifest_name
        self.app_name = app_name or ""
        self.index_to_category = index_to_category or {}
        self.publisher = publisher
        self.logger = logger_ or logger

        self._engine: Any = None
        self._engine_failed = False
        self._tracker: Any = None
        self._tracker_seam: Any = None

    # ------------------------------------------------------------------
    # Detection prep
    # ------------------------------------------------------------------

    def _map_categories(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map detections to labels from ``index_to_category`` config."""
        mapping = normalize_index_to_category(self.index_to_category)
        if not mapping:
            if self.manifest_name in ("ppe_compliance", "ppe_compliance_new", "ppe_detection_new"):
                self.logger.warning(
                    "PPE new-flow: index_to_category is empty — detections will keep raw model/harness labels"
                )
            return detections

        ppe_fixup = self.manifest_name in (
            "ppe_compliance",
            "ppe_compliance_new",
            "ppe_detection_new",
        )
        return map_detection_categories(
            detections,
            mapping,
            ppe_coco_fixup=ppe_fixup,
        )

    def _get_tracker(self, stream_key: str) -> Any:
        if self._tracker is not None:
            return self._tracker
        try:
            from ..post_processing.Trackers.integration import ConfigDrivenTracker, TrackerProfile

            # F10b S8: the shared seam (consolidation-plan.md §9.3 Step 8) -- NEW_FLOW's base
            # kwargs (0.4/0.05/0.3/0.8, track_buffer=600, max_time_lost=1200, frame_rate=25)
            # are this exact call site's literal config, so no overrides are needed.
            # namespace=True is load-bearing (F18 flow): tracker_namespace() reads
            # stream_info["stream_key"] and applies the SAME str(hash(x) % 1000000) formula
            # this call used inline before, so passing stream_key through stream_info
            # reproduces the identical namespace value byte-for-byte.
            if self._tracker_seam is None:
                self._tracker_seam = ConfigDrivenTracker()
            self._tracker = self._tracker_seam.get_shared_tracker(
                stream_info={"stream_key": stream_key},
                profile=TrackerProfile.NEW_FLOW,
                namespace=True,
            )
        except Exception as e:
            self.logger.warning("AnalyticsEngineSession: tracker unavailable (%s); feeding detections untracked", e)
            self._tracker = False  # sentinel: don't retry
        return self._tracker

    # ------------------------------------------------------------------
    # Engine lifecycle
    # ------------------------------------------------------------------

    def _build_stream_info(self, stream_info: Dict[str, Any]) -> Dict[str, Any]:
        si = stream_info or {}
        inp = si.get("input_settings", {}) or {}
        cam_fields = resolve_camera_fields_from_stream_info(si)
        return {
            "camera_id": cam_fields["camera_id"],
            "camera_name": cam_fields["camera_name"],
            "camera_group": cam_fields["camera_group"],
            "location": cam_fields["location"],
            "location_id": cam_fields["location_id"],
            "original_fps": float(inp.get("original_fps", 30.0) or 30.0),
            "app_deployment_id": si.get("app_deployment_id", "") or "",
            "app_id": si.get("application_id", si.get("app_id", "")) or "",
            "application_name": self.app_name,
            # No geometry for eligible apps -> default resolution.
            "resolution": [0, 0],
        }

    def _sync_stream_context(self, engine: Any, stream_info: Dict[str, Any]) -> None:
        """Refresh camera/app identity on the engine each frame."""
        built = self._build_stream_info(stream_info)
        loc = resolve_location_for_publish(stream_info)
        si = engine._stream_info
        if built.get("camera_id"):
            si.camera_id = built["camera_id"]
        if built.get("camera_name"):
            si.camera_name = built["camera_name"]
        if built.get("camera_group"):
            si.camera_group = built["camera_group"]
        si.location = loc["location"]
        si.location_id = loc["location_id"]
        if built.get("app_deployment_id"):
            si.app_deployment_id = built["app_deployment_id"]
        if built.get("app_id"):
            si.app_id = built["app_id"]

    def _get_engine(self, stream_info: Dict[str, Any]) -> Any:
        if self._engine_failed:
            return None
        if self._engine is None:
            try:
                self._engine = self._engine_cls(self.manifest_name, stream_info=self._build_stream_info(stream_info))
                self.logger.info(
                    "AnalyticsEngine session created (manifest=%s, app=%s)", self.manifest_name, self.app_name
                )
            except Exception as e:
                self._engine_failed = True
                self.logger.error(
                    "AnalyticsEngine init failed (manifest=%s): %s — analytics disabled for this stream",
                    self.manifest_name,
                    e,
                )
                return None
        return self._engine

    # ------------------------------------------------------------------
    # Per-frame entry point
    # ------------------------------------------------------------------

    def process(
        self,
        detections: List[Dict[str, Any]],
        stream_info: Optional[Dict[str, Any]],
        stream_key: str = "",
    ) -> Dict[str, Any]:
        """Run one frame; return the per-frame zone-keyed agg_summary (or {})."""
        try:
            stream_info = stream_info or {}
            engine = self._get_engine(stream_info)
            if engine is None:
                return {}

            detections = self._map_categories(list(detections or []))
            tracker = self._get_tracker(stream_key)
            if tracker:
                try:
                    detections = tracker.update(detections)
                except Exception as e:
                    self.logger.debug("AnalyticsEngineSession tracking error: %s", e)

            rtp_number = str(stream_info.get("rtp_number") or "")
            stream_time = stream_info.get("stream_time") or _utc_now_stream_time()
            self._sync_stream_context(engine, stream_info)
            engine._stream_info.rtp_number = rtp_number
            engine._stream_info.stream_time = stream_time

            frame_ts = time.time()
            frame_id = str(stream_info.get("frame_id") or "")
            frame_result = engine.process_frame(detections, frame_ts, frame_id)
            agg_summary = ((frame_result.get("result") or {}).get("value") or {}).get("agg_summary", {})

            self._publish_incidents(engine)
            self._maybe_publish_aggregation(engine, frame_ts, rtp_number)
            return agg_summary or {}
        except Exception as e:
            self.logger.debug("AnalyticsEngineSession.process error: %s", e)
            return {}

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    def _publish_incidents(self, engine: Any) -> None:
        camera_id = engine._stream_info.camera_id
        for payload in engine.drain_incident_events():
            # The engine's incident lifecycle keys by det["_camera_id"] and
            # falls back to "default_camera"; force the authoritative camera id
            # at the envelope top level.
            payload["camera_id"] = camera_id
            self.publisher.publish_incident(camera_id, payload)

    def _maybe_publish_aggregation(self, engine: Any, frame_ts: float, rtp_number: str) -> None:
        if not engine.should_aggregate(frame_ts):
            return
        payload = engine.aggregate().model_dump()
        input_timestamp = _utc_now_iso_z()
        payload["input_timestamp"] = input_timestamp
        payload["rtp_number"] = rtp_number
        if not payload.get("tracking_stats"):
            payload["tracking_stats"] = _empty_tracking_stats_fallback(input_timestamp)
        self.publisher.publish_aggregation(engine._stream_info.camera_id, payload)
