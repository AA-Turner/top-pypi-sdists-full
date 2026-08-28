from __future__ import annotations

import copy
import logging
import numbers
import os
import re
import threading
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from .hazard_zone_entry import PostProcessingConfigClient

logger = logging.getLogger(__name__)

# Post-processing output class ids (not YOLO model classes; detector still uses COCO person=0).
TAILGATING_OUTPUT_CLASS_IDS = {
    "person": 0,
    "tailgating_person": 1,
}

# Incident manager accepts: none, info, low, medium, significant, critical.
TAILGATING_SEVERITY = "critical"

_GEOMETRY_RETRY_INTERVAL = (
    30  # Seconds between background retry attempts when API fails
)

from ..core.base import (  # noqa: E402
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig, ZoneConfig  # noqa: E402
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides  # noqa: E402
from ..utils import (  # noqa: E402
    ByteTrackWrapper,
    SORTTracker,
    filter_by_confidence,
    get_bbox_bottom25_center,
    match_results_structure,
)
from ..utils.geometry_utils import (  # noqa: E402
    calculate_iou,
    get_bbox_bottom_center,
    point_in_polygon,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory  # noqa: E402
from ..utils.tailgating_utils import (  # noqa: E402
    AccessEventManager,
    AccessPointState,
    CrossingRecord,
    analyze_passage,
    build_side_zone_map,
    detect_crossing,
)


def _post_processing_config_client_cls() -> Any:
    """Late import: ``hazard_zone_entry`` is heavy; only load when API zones are used."""
    from .hazard_zone_entry import PostProcessingConfigClient

    return PostProcessingConfigClient


def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Fold AI-style payloads into ``postProcessing`` (same contract as overcrowding).

    Matrice UI / exports may place ``zone_config`` under a top-level camera id key;
    this merges those into ``postProcessing`` without overwriting existing keys.
    """
    if not isinstance(doc, dict):
        return doc

    reserved = {
        "_id",
        "_idCamera",
        "_idApplication",
        "_idAppDeployment",
        "postProcessing",
        "postprocessing",
        "createdAt",
        "updatedAt",
        "created_at",
        "updated_at",
    }
    lifted: Dict[str, Any] = {}
    for k, v in doc.items():
        if k in reserved or not isinstance(v, dict):
            continue
        zc = v.get("zone_config")
        if not isinstance(zc, dict):
            continue
        if zc.get("zones") or zc.get("lines") is not None:
            lifted[k] = v
    if not lifted:
        return doc

    out = copy.deepcopy(doc)
    post = dict(out.get("postProcessing") or {})
    for k, v in lifted.items():
        if k not in post:
            post[k] = v
    out["postProcessing"] = post
    return out


def _parse_geometry_points(points: Any) -> List[List[float]]:
    """Parse zone/line points as stored in config (pixel coordinates)."""
    if not isinstance(points, list) or not points:
        return []
    out: List[List[float]] = []
    for pt in points:
        if isinstance(pt, (list, tuple)) and len(pt) >= 2:
            try:
                out.append([float(pt[0]), float(pt[1])])
            except (TypeError, ValueError):
                continue
    return out


def _parse_polygon_map(raw: Any) -> Dict[str, List[List[float]]]:
    """Coerce a ``name -> polygon`` mapping to numeric point lists (no coord conversion)."""
    out: Dict[str, List[List[float]]] = {}
    if not isinstance(raw, dict):
        return out
    for key, val in raw.items():
        if isinstance(val, list):
            pts = _parse_geometry_points(val)
            if pts:
                out[str(key)] = pts
    return out


def _parse_line_map(raw: Any) -> Dict[str, List[List[float]]]:
    """Coerce an ``access_line_id -> [p1, p2]`` mapping to numeric two-point lines."""
    out: Dict[str, List[List[float]]] = {}
    if isinstance(raw, dict):
        items = raw.items()
    elif isinstance(raw, list):
        # Allow a bare list of lines; synthesize stable ids line_0, line_1, ...
        items = ((f"line_{i}", v) for i, v in enumerate(raw))
    else:
        return out
    for key, val in items:
        pts = _parse_geometry_points(val)
        if len(pts) >= 2:
            out[str(key)] = [pts[0], pts[-1]]
    return out


def _geometry_coord_max(points: Any) -> float:
    """Largest absolute coordinate magnitude across polygon / line points."""
    if not isinstance(points, list):
        return 0.0
    peak = 0.0
    for pt in points:
        if not isinstance(pt, (list, tuple)) or len(pt) < 2:
            continue
        try:
            peak = max(peak, abs(float(pt[0])), abs(float(pt[1])))
        except (TypeError, ValueError):
            continue
    return peak


def _stream_dimensions_for_geometry(
    stream_info: Optional[Dict[str, Any]],
) -> Tuple[Optional[int], Optional[int]]:
    """Best-effort (width, height) for denormalizing detection bboxes to pixel space."""
    if not isinstance(stream_info, dict):
        return None, None

    res = stream_info.get("stream_resolution") or {}
    if isinstance(res, dict):
        w, h = res.get("width"), res.get("height")
        if w and h:
            return int(w), int(h)

    inp = stream_info.get("input_settings") or {}
    if isinstance(inp, dict):
        sr = inp.get("stream_resolution")
        if isinstance(sr, (list, tuple)) and len(sr) >= 2:
            return int(sr[0]), int(sr[1])
        w, h = inp.get("width"), inp.get("height")
        if w and h:
            return int(w), int(h)

    meta = stream_info.get("metadata") or {}
    if isinstance(meta, dict):
        isize = meta.get("input_size")
        if isinstance(isize, str) and "x" in isize.lower():
            parts = isize.lower().split("x", 1)
            if len(parts) == 2:
                try:
                    return int(parts[0]), int(parts[1])
                except ValueError:
                    pass

    return None, None


def _bbox_coord_max(bbox: Any) -> float:
    """Largest absolute bbox coordinate (detect normalized 0-1 vs pixel boxes)."""
    if not isinstance(bbox, dict):
        return 0.0
    keys = ("xmin", "ymin", "xmax", "ymax", "x1", "y1", "x2", "y2")
    peak = 0.0
    for key in keys:
        if key in bbox:
            try:
                peak = max(peak, abs(float(bbox[key])))
            except (TypeError, ValueError):
                continue
    return peak


def _foot_point_for_geometry(
    bbox: Dict[str, Any],
    stream_info: Optional[Dict[str, Any]],
    *,
    bottom25: bool = False,
) -> Tuple[float, float]:
    """Foot point in the same coordinate space as config zones (pixels when zones are pixels)."""
    foot = (
        get_bbox_bottom25_center(bbox)
        if bottom25
        else get_bbox_bottom_center(bbox)
    )
    if _bbox_coord_max(bbox) > 1.5:
        return foot
    width, height = _stream_dimensions_for_geometry(stream_info)
    if not width or not height:
        return foot
    return (foot[0] * width, foot[1] * height)


def _enrich_stream_info_from_prediction(
    data: Any,
    stream_info: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Merge prediction-envelope fields into *stream_info* for geometry and stream ids."""
    out = dict(stream_info) if isinstance(stream_info, dict) else {}
    if not isinstance(data, dict):
        return out
    for key in ("frame_id", "camera_id", "app_deployment_id", "metadata"):
        val = data.get(key)
        if val is not None and key not in out:
            out[key] = val
    return out


def _coerce_numeric_track_id(track_id: Any) -> Any:
    """Normalize numeric string track ids (prod sends ``\"11\"``) to ``int``."""
    if track_id is None or isinstance(track_id, bool):
        return track_id
    try:
        return int(track_id)
    except (TypeError, ValueError):
        return track_id


def _normalize_detection_track_ids(detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Coerce numeric-string ``track_id`` values in place for stable runtime keys."""
    for det in detections:
        if not isinstance(det, dict):
            continue
        raw = det.get("track_id")
        if raw is not None:
            det["track_id"] = _coerce_numeric_track_id(raw)
    return detections


def _tailgating_geometry_from_ui_pixels(
    zone_config_raw: Dict[str, Any],
    width: int,
    height: int,
) -> Optional[Tuple[Dict[str, List[List[float]]], Dict[str, List[List[float]]]]]:
    """Parse the new (denormalized, pixel) ``zone_config`` into ``(zones, access_lines)``.

    Expected shape (door-agnostic):
        ``zones``: exactly two polygons (e.g. ``{"zone_1": [...], "zone_2": [...]}``)
        ``lines``: one or more access lines (``{"<line_id>": [p1, p2], ...}``)
    Returns ``None`` when the shape does not satisfy the contract.
    """
    if not isinstance(zone_config_raw, dict) or width <= 0 or height <= 0:
        return None

    zones = _parse_polygon_map(zone_config_raw.get("zones"))
    lines = _parse_line_map(zone_config_raw.get("lines"))

    # Keep only valid polygons (>= 3 points) and require exactly two.
    zones = {k: v for k, v in zones.items() if len(v) >= 3}
    if len(zones) != 2 or not lines:
        return None

    return zones, lines


_UNTRACKED_TRACK_ID_RE = re.compile(r"^untracked_", re.IGNORECASE)


def _is_ephemeral_track_id(track_id: Any) -> bool:
    """True when upstream ids are missing or change every frame (e.g. ``untracked_110_0``)."""
    if track_id is None:
        return True
    if isinstance(track_id, str):
        s = track_id.strip()
        if not s or _UNTRACKED_TRACK_ID_RE.match(s):
            return True
    return False


def _track_id_usable(track_id: Any) -> bool:
    """True when ``track_id`` can drive crossing / incident state (mirrors loitering guards)."""
    if track_id is None or isinstance(track_id, bool):
        return False
    try:
        return int(track_id) >= 0
    except (TypeError, ValueError):
        return not _is_ephemeral_track_id(track_id)


def _resolve_frame_id(stream_info: Optional[Dict[str, Any]]) -> int:
    """Best-effort monotonic frame index for crossing memory and IoU tracking."""
    if not stream_info:
        return 0
    for key in ("frame_number", "frame_index", "frame_idx"):
        val = stream_info.get(key)
        if val is not None:
            try:
                return int(val)
            except (TypeError, ValueError):
                pass
    fid = stream_info.get("frame_id")
    if isinstance(fid, str):
        tail = re.search(r"_(\d+)$", fid)
        if tail:
            try:
                return int(tail.group(1))
            except ValueError:
                pass
    return 0


def _extract_detections_from_data(data: Any) -> List[Dict[str, Any]]:
    """Accept list detections or full prediction envelopes with a ``detections`` key."""
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    if isinstance(data, dict):
        dets = data.get("detections")
        if isinstance(dets, list):
            return [d for d in dets if isinstance(d, dict)]
    return []


def _stabilize_ephemeral_track_ids(
    detections: List[Dict[str, Any]],
    runtime: Dict[str, Any],
    frame_id: int,
    *,
    iou_threshold: float = 0.25,
    max_gap_frames: int = 90,
) -> List[Dict[str, Any]]:
    """Assign stable internal ids when production sends ``untracked_*`` or no ``track_id``."""
    if not detections:
        return detections
    if not any(_is_ephemeral_track_id(d.get("track_id")) for d in detections):
        return detections

    registry: Dict[Any, Dict[str, Any]] = runtime.setdefault("track_registry", {})
    next_id = int(runtime.setdefault("next_track_id", 1))
    stabilized: List[Dict[str, Any]] = []
    assigned_this_frame: set[Any] = set()

    for det in detections:
        out = dict(det)
        raw_tid = out.get("track_id")
        if not _is_ephemeral_track_id(raw_tid):
            stabilized.append(out)
            continue

        bbox = out.get("bounding_box") or out.get("bbox")
        best_cid: Any = None
        best_iou = 0.0
        if isinstance(bbox, dict):
            for cid, info in registry.items():
                if cid in assigned_this_frame:
                    continue
                last_f = int(info.get("last_frame", -1))
                if frame_id - last_f > max_gap_frames:
                    continue
                prev_bbox = info.get("last_bbox")
                if not isinstance(prev_bbox, dict):
                    continue
                iou = calculate_iou(bbox, prev_bbox)
                if iou >= iou_threshold and iou > best_iou:
                    best_iou = iou
                    best_cid = cid

        if best_cid is None:
            best_cid = next_id
            next_id += 1

        assigned_this_frame.add(best_cid)
        registry[best_cid] = {
            "last_bbox": bbox,
            "last_frame": frame_id,
        }
        out["track_id"] = best_cid
        stabilized.append(out)

    runtime["next_track_id"] = next_id
    for cid in list(registry.keys()):
        last_f = int(registry[cid].get("last_frame", -1))
        if frame_id - last_f > max_gap_frames:
            registry.pop(cid, None)

    return stabilized


def _detection_matches_target_categories(
    detection: Dict[str, Any],
    target_categories: List[str],
) -> bool:
    """Match loitering category filter; treat missing category as person when configured."""
    cat = detection.get("category")
    if cat is None:
        return "person" in target_categories
    return cat in target_categories


def _normalize_track_id_for_label(track_id: Any) -> Any:
    """Normalize tracker id for set membership (``int`` for numpy/Python integers)."""
    if track_id is None:
        return None
    if isinstance(track_id, bool):
        return track_id
    if isinstance(track_id, numbers.Integral):
        return int(track_id)
    return track_id


@dataclass
class _PassageHit:
    """A completed crossing analysis for one ``(access_line, direction)`` this frame.

    ``ep_key`` is the episode key ``f"{access_line_id}::{direction}"`` used to key
    incident episodes and alert state. ``secured_zone`` / ``buffer_zone`` are the
    dynamic zone names for this passage (destination = secured, origin = buffer);
    either may be ``None`` for a degenerate side->zone map.

    ``event_id`` is the UUID of the underlying ``AccessEvent`` (one authorization
    window). It is the churn-robust identity for a tailgating passage: it is stable
    across track-ID reissue *within* an event and unique *between* events, so it is
    used to count each passage exactly once for the volume metrics.
    """

    ep_key: str
    access_line_id: str
    direction: str
    secured_zone: Optional[str]
    buffer_zone: Optional[str]
    analysis: Any
    event_id: str = ""


def _direction_labels(
    side_map: Optional[Dict[int, str]],
    direction_sign: int,
) -> Tuple[str, Optional[str], Optional[str]]:
    """Map a crossing direction sign to ``(direction_key, secured_zone, buffer_zone)``.

    With a valid side->zone map the destination zone (the one entered) is the
    secured zone and the origin zone is the buffer. For a degenerate map (line does
    not separate the zones) the direction is labelled by raw side and zone names are
    ``None``.
    """
    if side_map:
        secured = side_map.get(direction_sign)
        buffer_ = side_map.get(-direction_sign)
        if secured is not None:
            return f"to_{secured}", secured, buffer_
    side_name = "pos" if direction_sign > 0 else "neg"
    return f"to_side_{side_name}", None, None


def _suspect_track_ids_from_analyses(analyses: List[_PassageHit]) -> set[Any]:
    """Union of ``suspected_tailgaters`` track ids across all passages this frame."""
    ids: set[Any] = set()
    for hit in analyses:
        suspects = getattr(hit.analysis, "suspected_tailgaters", None) or []
        for tid in suspects:
            n = _normalize_track_id_for_label(tid)
            if n is not None:
                ids.add(n)
    return ids


def _normalize_suspect_id_set(raw_ids: Any) -> set[Any]:
    """Normalize a collection of suspect track ids for set membership."""
    out: set[Any] = set()
    if not raw_ids:
        return out
    for tid in raw_ids:
        n = _normalize_track_id_for_label(tid)
        if n is not None:
            out.add(n)
    return out


def _track_ids_in_detections(detections: List[Any]) -> set[Any]:
    """Normalized ``track_id`` values present in the current frame detections."""
    return _normalize_suspect_id_set(
        det.get("track_id") for det in detections if isinstance(det, dict)
    )


def _register_active_incidents(
    active_incidents: Dict[str, Dict[str, Any]],
    analyses: List[_PassageHit],
    frame_id: int,
) -> None:
    """Open or extend a per-(access_line, direction) incident episode for suspects."""
    for hit in analyses:
        new_ids = _normalize_suspect_id_set(getattr(hit.analysis, "suspected_tailgaters", None))
        if not new_ids:
            continue

        ep_key = hit.ep_key
        rec = active_incidents.get(ep_key)
        if rec is None:
            rec = {
                "incident_id": f"tailgating_{hit.access_line_id}_{hit.direction}_{frame_id}",
                "opened_frame": frame_id,
                "access_line_id": hit.access_line_id,
                "direction": hit.direction,
                "secured_zone": hit.secured_zone,
                "buffer_zone": hit.buffer_zone,
                "suspected_tailgaters": set(),
                "confidence": float(getattr(hit.analysis, "confidence", 0.0) or 0.0),
                "severity": TAILGATING_SEVERITY,
            }
            active_incidents[ep_key] = rec
            logger.info(
                "tailgating incident opened line=%s direction=%s incident_id=%s suspects=%s frame=%s",
                hit.access_line_id,
                hit.direction,
                rec["incident_id"],
                sorted(new_ids, key=str),
                frame_id,
            )
        else:
            added = new_ids - rec["suspected_tailgaters"]
            if added:
                logger.info(
                    "tailgating incident extended line=%s direction=%s incident_id=%s added=%s frame=%s",
                    hit.access_line_id,
                    hit.direction,
                    rec["incident_id"],
                    sorted(added, key=str),
                    frame_id,
                )

        rec["suspected_tailgaters"].update(new_ids)
        analysis_conf = float(getattr(hit.analysis, "confidence", 0.0) or 0.0)
        if analysis_conf > rec.get("confidence", 0.0):
            rec["confidence"] = analysis_conf
        rec["severity"] = TAILGATING_SEVERITY


def _sync_active_incidents_with_detections(
    active_incidents: Dict[str, Dict[str, Any]],
    current_track_ids: set[Any],
) -> Tuple[List[Tuple[str, Dict[str, Any], set[Any]]], List[Tuple[str, Dict[str, Any]]]]:
    """Drop episodes with no live suspects.

    Returns ``(live, closed)``: ``live`` is the visible-suspect set per active
    episode key; ``closed`` is the list of episodes that just ended this frame (so
    a closing incident with a real end_time can be emitted for them).
    """
    live: List[Tuple[str, Dict[str, Any], set[Any]]] = []
    closed: List[Tuple[str, Dict[str, Any]]] = []
    for ep_key in list(active_incidents.keys()):
        rec = active_incidents[ep_key]
        visible = rec["suspected_tailgaters"] & current_track_ids
        if not visible:
            logger.info(
                "tailgating incident cleared episode=%s incident_id=%s "
                "(no suspect track_ids in live detections)",
                ep_key,
                rec["incident_id"],
            )
            closed.append((ep_key, dict(rec)))
            del active_incidents[ep_key]
            continue
        live.append((ep_key, rec, visible))
    return live, closed


def _visible_suspect_track_ids_from_live(
    live_incidents: List[Tuple[str, Dict[str, Any], set[Any]]],
) -> set[Any]:
    """Union of suspect track ids visible in the current frame across active incidents."""
    visible: set[Any] = set()
    for _ep_key, _rec, ep_visible in live_incidents:
        visible |= ep_visible
    return visible


def _detection_foot_in_polygon(
    detection: Dict[str, Any],
    polygon: List[List[float]],
    stream_info: Optional[Dict[str, Any]] = None,
) -> bool:
    """True when detection foot point is inside *polygon* (same foot rule as zone counting)."""
    if not isinstance(polygon, list) or len(polygon) < 3:
        return False
    bbox = detection.get("bounding_box") or detection.get("bbox")
    if not isinstance(bbox, dict):
        return False
    poly = _parse_geometry_points(polygon)
    if len(poly) < 3:
        return False
    foot = _foot_point_for_geometry(bbox, stream_info, bottom25=False)
    return point_in_polygon(foot, [(float(p[0]), float(p[1])) for p in poly])


def _build_zone_analysis_for_frame(
    clean_detections: List[Dict[str, Any]],
    config: "TailgatingConfig",
    runtime: Dict[str, Any],
    live_incidents: List[Tuple[str, Dict[str, Any], set[Any]]],
    stream_info: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Occupancy of the two shared zones + a per-access-line incident block.

    The two zones are global (not per door). Each access line reports its active
    incident(s) and, for any active episode, the dynamic ``secured_zone`` /
    ``buffer_zone`` mapping for that passage. Does not affect crossing logic.
    """
    all_tailgating = _visible_suspect_track_ids_from_live(live_incidents)

    zone_out: Dict[str, Any] = {}
    for zone_name, poly in (config.zones or {}).items():
        poly = _parse_geometry_points(poly)
        if len(poly) < 3:
            continue

        current_tracks: set[Any] = set()
        counts_by_category: Counter = Counter()
        for det in clean_detections:
            if not _detection_foot_in_polygon(det, poly, stream_info):
                continue
            counts_by_category[det.get("category", "person")] += 1
            tid = _normalize_track_id_for_label(det.get("track_id"))
            if tid is not None:
                current_tracks.add(tid)

        zone_out[zone_name] = {
            "current_count": len(current_tracks),
            "current_track_ids": sorted(current_tracks, key=str),
            "tailgating_track_ids": sorted(current_tracks & all_tailgating, key=str),
            "counts_by_category": dict(counts_by_category),
            "zone_coords": config.zones.get(zone_name),
        }

    # Per-access-line incident / event view.
    events: Dict[Tuple[str, str], Any] = runtime.get("events") or {}
    lines_active_event: set[str] = {
        line_id for (line_id, _direction), ev in events.items() if ev is not None
    }

    line_out: Dict[str, Any] = {}
    for line_id, line in (config.access_lines or {}).items():
        incidents_here = [
            {
                "incident_id": rec.get("incident_id"),
                "direction": rec.get("direction"),
                "from_zone": rec.get("buffer_zone"),
                "to_zone": rec.get("secured_zone"),
                "secured_zone": rec.get("secured_zone"),
                "buffer_zone": rec.get("buffer_zone"),
                "visible_tailgaters": sorted(visible, key=str),
            }
            for _ep_key, rec, visible in live_incidents
            if rec.get("access_line_id") == line_id
        ]
        line_out[line_id] = {
            "access_line_coords": line,
            "active_incident": bool(incidents_here),
            "active_event": line_id in lines_active_event,
            "incidents": incidents_here,
        }

    return {"zones": zone_out, "access_lines": line_out}


# ============================================================
# CONFIG
# ============================================================


class TailgatingConfig(BaseConfig):
    """Tailgating post-processing configuration (door-agnostic, bidirectional).

    **Geometry** is **two shared zones** plus **one or more access lines**:

    - ``zones``: exactly **two** polygons (e.g. ``{"zone_1": [...], "zone_2": [...]}``).
      They are shared by every access line. For any single passage the
      *destination* zone is treated as the secured zone and the *origin* zone as
      the access/buffer zone — the roles flip with direction.
    - ``access_lines``: a mapping ``{access_line_id: [p1, p2]}`` with at least one
      entry. Each access line is an independent access point (door / turnstile)
      with its own per-direction tailgating state.

    Both may also be supplied via ``extra_params`` (``extra_params["zones"]`` /
    ``extra_params["access_lines"]``); top-level values win on duplicate keys.

    **Bidirectional detection**: a crossing is detected in either direction. The
    detector anchors on the last *clear* side of a line and fires when the foot
    reaches the opposite clear side, so an arbitrary gap between the zone polygons
    and the line (where the foot is momentarily inside neither zone) does not break
    detection. Tailgating windows are keyed by ``(access_line_id, direction)`` so
    opposite-direction passages never interfere.

    **Matrice UI / API geometry**: When ``stream_info`` is present and
    ``PostProcessingConfigClient`` can reach the deployment post-processing config,
    geometry is merged on the first frame. The camera ``zone_config`` (after
    denormalization) must contain ``zones`` (two polygons) and ``lines`` (one or
    more two-point lines). For local / bench runs set
    ``stream_info["skip_tailgating_api_zones"]`` to true to skip API resolution.

    **Output labeling**: ``tracking_stats.detections`` use
    ``category: "tailgating_person"`` (``class_id: 1``) for any detection whose
    ``track_id`` is a suspect from an active incident still present in live
    detections; others remain ``"person"`` (``class_id: 0``).

    **Incidents / alerts**: keyed by ``(access_line_id, direction)``. An incident
    opens immediately on the crossing frame whose passage analysis flags
    suspect(s) and persists while any suspect ``track_id`` remains visible. Alerts
    fire on the crossing frame for new suspects (per-line alert cooldown).

    **Internal tracking** (same contract as ``loitering_detection``): when
    ``enable_tracking`` is True, a per-stream SORT (default) or ByteTrack wrapper
    assigns stable integer ``track_id`` values before crossing logic runs.

    **Per-line tuning** via ``zone_params`` (``{access_line_id: {...overrides}}``):
    ``allowed_persons_per_event``, ``access_window_sec``, ``silence_timeout_sec``,
    ``cooldown_sec``, ``max_follow_time_delta_sec``. Absent keys fall back to the
    global defaults.
    """

    EXTRA_PARAM_KEYS = frozenset(
        {
            "access_window_sec",
            "silence_timeout_sec",
            "cooldown_sec",
            "allowed_persons_per_event",
            "max_follow_time_delta_sec",
            "zones",
            "access_lines",
            "zone_config",
            "zone_params",
            "min_motion_magnitude",
            "side_margin",
            "line_endpoint_padding",
            "cross_memory_frames",
            "tracking_method",
            "tracking_max_age",
            "tracking_min_hits",
            "tracking_iou_threshold",
            "bytetrack_track_thresh",
            "bytetrack_match_thresh",
        }
    )

    def _line_param(self, line_id: Any, key: str, default: Any) -> Any:
        """Return a per-access-line override from ``zone_params`` or the global default.

        Lookup: ``zone_params[line_id][key]`` -> ``default`` (the global config
        value). This is how "default to normal params when nothing is given" works.
        """
        params = (getattr(self, "zone_params", None) or {}).get(str(line_id))
        if isinstance(params, dict) and key in params:
            return params[key]
        return default

    @staticmethod
    def normalize_zone_polygons(raw: Any) -> Dict[str, List[List[float]]]:
        """Coerce shared zones to ``{name: polygon}`` from a dict or a ``ZoneConfig``."""
        if isinstance(raw, ZoneConfig):
            raw = raw.zones
        return _parse_polygon_map(raw)

    @staticmethod
    def normalize_access_lines(raw: Any) -> Dict[str, List[List[float]]]:
        """Coerce access lines to ``{access_line_id: [p1, p2]}``."""
        return _parse_line_map(raw)

    @staticmethod
    def zones_lines_from_zone_config(
        zone_config: Any,
    ) -> Tuple[Dict[str, List[List[float]]], Dict[str, List[List[float]]]]:
        """Split a Matrice/UI ``zone_config`` into ``(zones, access_lines)``.

        Expected shape: ``{"zones": {zone_name: polygon, ...},
        "lines": {line_name: [p1, p2], ...}}`` (pixel coordinates).
        """
        if not isinstance(zone_config, dict):
            return {}, {}
        return (
            TailgatingConfig.normalize_zone_polygons(zone_config.get("zones")),
            TailgatingConfig.normalize_access_lines(zone_config.get("lines")),
        )

    def __init__(
        self,
        usecase: str = "tailgating_detection",  # Registry / pipeline id; must be "tailgating_detection".
        category: str = "security",  # Post-processor category (e.g. security) for registration and routing.
        confidence_threshold: float = 0.5,  # Min detection confidence; frames are filtered before crossing logic.
        target_categories: Optional[
            List[str]
        ] = None,  # Intended object classes (e.g. ["person"]).
        zones: Optional[
            Dict[str, List[List[float]]]
        ] = None,  # Exactly two shared polygons; may also be set via extra_params["zones"] (merged).
        access_lines: Optional[
            Dict[str, List[List[float]]]
        ] = None,  # access_line_id -> [p1, p2]; may also be set via extra_params["access_lines"] (merged).
        zone_config: Optional[
            Dict[str, Any]
        ] = None,  # Matrice/UI shape: {"zones": {name: polygon}, "lines": {name: [p1,p2]}}. Geometry source; explicit zones/access_lines override per key.
        zone_params: Optional[
            Dict[str, Dict[str, Any]]
        ] = None,  # Per-access-line tuning overrides keyed by access_line_id.
        access_window_sec: float = 5.0,  # Seconds after the first crossing in an access event; hard cap on the window.
        silence_timeout_sec: float = 2.0,  # Seconds with no new crossings after the last one; closes the event when elapsed.
        cooldown_sec: float = 4.0,  # Seconds after closing an event before a new event can open on that (line, direction).
        allowed_persons_per_event: int = 1,  # Authorized headcount per passage window; extras within the window → suspected tailgaters.
        max_follow_time_delta_sec: float = 3.0,  # Max seconds between consecutive crossings to treat a follower as tailgating (analyze_passage).
        min_motion_magnitude: float = 2.0,  # Min anchor->foot traversal (pixels) to accept a crossing.
        side_margin: float = 5.0,  # Abs signed distance (pixels) past which a foot counts as on a clear side; the gap band is |d| < side_margin.
        line_endpoint_padding: float = 0.0,  # Optionally extend the access-line segment (pixels) beyond each endpoint for attribution.
        cross_memory_frames: int = 0,  # Drop stale per-track foot/side state after this many frames without the track (0 = disable).
        tracking_method: str = "sort",  # Internal tracker when enable_tracking: "sort" (default) or "bytetrack".
        tracking_max_age: int = 30,  # SORT/ByteTrack max frames to keep lost tracks (also ByteTrack buffer).
        tracking_min_hits: int = 2,  # SORT min consecutive matches before confirming a track.
        tracking_iou_threshold: float = 0.25,  # SORT detection-to-track IoU match threshold.
        bytetrack_track_thresh: float = 0.25,  # ByteTrack high-confidence detection threshold.
        bytetrack_match_thresh: float = 0.80,  # ByteTrack association match threshold.
        alert_config: Optional[
            AlertConfig
        ] = None,  # Alert channels; validated when present.
        **kwargs,  # Forwarded to BaseConfig: enable_tracking, enable_analytics, extra_params (prod tuning blob), etc.
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)

        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["person"]

        self.access_window_sec = access_window_sec
        self.silence_timeout_sec = silence_timeout_sec
        self.cooldown_sec = cooldown_sec

        self.allowed_persons_per_event = allowed_persons_per_event
        self.max_follow_time_delta_sec = max_follow_time_delta_sec

        self.min_motion_magnitude = min_motion_magnitude
        self.side_margin = side_margin
        self.line_endpoint_padding = line_endpoint_padding
        self.cross_memory_frames = cross_memory_frames

        self.tracking_method = str(tracking_method).lower().strip()
        self.tracking_max_age = int(tracking_max_age)
        self.tracking_min_hits = int(tracking_min_hits)
        self.tracking_iou_threshold = float(tracking_iou_threshold)
        self.bytetrack_track_thresh = float(bytetrack_track_thresh)
        self.bytetrack_match_thresh = float(bytetrack_match_thresh)

        self.alert_config = alert_config

        ep = dict(self.extra_params or {})

        # Geometry sources, lowest -> highest precedence (later overrides per key):
        #   extra_params["zone_config"] -> top-level zone_config
        #   -> extra_params["zones"/"access_lines"] -> top-level zones/access_lines
        # zone_config is the Matrice/UI shape ({"zones": {...}, "lines": {...}});
        # explicit zones/access_lines still work and win on duplicate keys.
        zcz_extra, zcl_extra = TailgatingConfig.zones_lines_from_zone_config(ep.pop("zone_config", None))
        zcz_top, zcl_top = TailgatingConfig.zones_lines_from_zone_config(zone_config)
        zones_merged = {
            **zcz_extra,
            **zcz_top,
            **TailgatingConfig.normalize_zone_polygons(ep.pop("zones", None)),
            **TailgatingConfig.normalize_zone_polygons(zones),
        }
        lines_merged = {
            **zcl_extra,
            **zcl_top,
            **TailgatingConfig.normalize_access_lines(ep.pop("access_lines", None)),
            **TailgatingConfig.normalize_access_lines(access_lines),
        }
        self.zones: Dict[str, List[List[float]]] = zones_merged
        self.access_lines: Dict[str, List[List[float]]] = lines_merged

        zp_extra = ep.pop("zone_params", None)
        merged_zp: Dict[str, Dict[str, Any]] = {}
        for src in (zp_extra, zone_params):
            if isinstance(src, dict):
                for k, v in src.items():
                    if isinstance(v, dict):
                        merged_zp[str(k)] = dict(v)
        self.zone_params: Dict[str, Dict[str, Any]] = merged_zp

        def _pop_float(key: str, attr: str) -> None:
            if key not in ep:
                return
            setattr(self, attr, float(ep.pop(key)))

        _pop_float("access_window_sec", "access_window_sec")
        _pop_float("silence_timeout_sec", "silence_timeout_sec")
        _pop_float("cooldown_sec", "cooldown_sec")
        _pop_float("max_follow_time_delta_sec", "max_follow_time_delta_sec")

        if "allowed_persons_per_event" in ep:
            self.allowed_persons_per_event = int(ep.pop("allowed_persons_per_event"))

        if "min_motion_magnitude" in ep:
            self.min_motion_magnitude = float(ep.pop("min_motion_magnitude"))

        if "side_margin" in ep:
            self.side_margin = float(ep.pop("side_margin"))

        if "line_endpoint_padding" in ep:
            self.line_endpoint_padding = float(ep.pop("line_endpoint_padding"))

        if "cross_memory_frames" in ep:
            self.cross_memory_frames = int(ep.pop("cross_memory_frames"))

        if "tracking_method" in ep:
            self.tracking_method = str(ep.pop("tracking_method")).lower().strip()

        if "tracking_max_age" in ep:
            self.tracking_max_age = int(ep.pop("tracking_max_age"))

        if "tracking_min_hits" in ep:
            self.tracking_min_hits = int(ep.pop("tracking_min_hits"))

        if "tracking_iou_threshold" in ep:
            self.tracking_iou_threshold = float(ep.pop("tracking_iou_threshold"))

        if "bytetrack_track_thresh" in ep:
            self.bytetrack_track_thresh = float(ep.pop("bytetrack_track_thresh"))

        if "bytetrack_match_thresh" in ep:
            self.bytetrack_match_thresh = float(ep.pop("bytetrack_match_thresh"))

        for k in list(ep.keys()):
            if k in TailgatingConfig.EXTRA_PARAM_KEYS:
                ep.pop(k, None)

        self.extra_params = ep

    # --------------------------------------------------------

    @staticmethod
    def _validate_point(label: str, pt: Any) -> None:
        if not isinstance(pt, (list, tuple)) or len(pt) != 2:
            raise ValueError(f"{label} point must be a sequence of two numbers")
        if not all(isinstance(c, numbers.Real) for c in pt):
            raise ValueError(f"{label} coordinates must be numbers")

    def validate(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0 and 1")

        if not isinstance(self.zones, dict) or len(self.zones) != 2:
            raise ValueError(
                "Exactly two shared zones are required: set them under "
                "'zone_config' (zone_config={'zones': {'zone_1': [...], "
                "'zone_2': [...]}, 'lines': {...}}) or via top-level 'zones' / "
                "extra_params['zones']"
            )
        for zone_name, poly in self.zones.items():
            if not isinstance(poly, (list, tuple)) or len(poly) < 3:
                raise ValueError(f"zone '{zone_name}' must be a polygon with at least 3 points")
            for i, pt in enumerate(poly):
                TailgatingConfig._validate_point(f"zone '{zone_name}' point {i}", pt)

        if not isinstance(self.access_lines, dict) or not self.access_lines:
            raise ValueError(
                "At least one access line is required: set them under "
                "zone_config['lines'] ({line_id: [p1, p2]}) or via top-level "
                "'access_lines' / extra_params['access_lines']"
            )
        for line_id, line in self.access_lines.items():
            if not isinstance(line, (list, tuple)) or len(line) != 2:
                raise ValueError(f"access_line '{line_id}' must be exactly two points [p1, p2]")
            TailgatingConfig._validate_point(f"access_line '{line_id}'", line[0])
            TailgatingConfig._validate_point(f"access_line '{line_id}'", line[1])

        if self.access_window_sec <= 0:
            raise ValueError("access_window_sec must be positive")

        if self.silence_timeout_sec <= 0:
            raise ValueError("silence_timeout_sec must be positive")

        if self.cooldown_sec <= 0:
            raise ValueError("cooldown_sec must be positive")

        if self.max_follow_time_delta_sec <= 0:
            raise ValueError("max_follow_time_delta_sec must be positive")

        if self.allowed_persons_per_event < 1:
            raise ValueError("allowed_persons_per_event must be at least 1")

        if self.min_motion_magnitude < 0:
            raise ValueError("min_motion_magnitude must be non-negative")

        if self.side_margin < 0:
            raise ValueError("side_margin must be non-negative")

        if self.line_endpoint_padding < 0:
            raise ValueError("line_endpoint_padding must be non-negative")

        if self.cross_memory_frames < 0:
            raise ValueError("cross_memory_frames must be non-negative")

        if self.tracking_max_age < 1:
            raise ValueError("tracking_max_age must be at least 1")

        if self.tracking_min_hits < 1:
            raise ValueError("tracking_min_hits must be at least 1")

        if not 0.0 <= self.tracking_iou_threshold <= 1.0:
            raise ValueError("tracking_iou_threshold must be between 0 and 1")

        if self.tracking_method not in ("sort", "bytetrack"):
            raise ValueError("tracking_method must be 'sort' or 'bytetrack'")

        if self.alert_config:
            alert_errors = self.alert_config.validate()
            if alert_errors:
                raise ValueError("; ".join(alert_errors))


# ============================================================
# USE CASE
# ============================================================


class TailgatingDetectionUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("tailgating_detection")

        self.event_manager = AccessEventManager()
        self.category = "security"

        # Runtime state isolated per stream
        self._runtime: Dict[str, Dict[str, Any]] = {}
        self._streams_warned_tracker_fallback: set = set()

        self._config_client: Optional[PostProcessingConfigClient] = None
        self._resolved_geometry_cache: Optional[TailgatingConfig] = None
        self._geometry_thread: Optional[threading.Thread] = None
        self._zone_resolution_attempted: bool = False

        self._incident_manager_initialized: bool = False
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._tracking_start_time = None
        self.start_timer = None

    # ------------------------------------------------------------------
    # Matrice UI / post-processing API zone geometry (same flow as overcrowding)
    # ------------------------------------------------------------------

    def set_config_client(self, client: Optional[PostProcessingConfigClient]) -> None:
        """Set client used to resolve zone/line geometry from deployment post-processing config."""
        self._config_client = client

    def _api_zone_retry_is_worthwhile(self, stream_info: Dict[str, Any]) -> bool:
        """True when credentials exist and stream_info yields deployment + camera ids."""
        try:
            client = self._config_client or stream_info.get("config_client")
            if not client:
                PPC = _post_processing_config_client_cls()
                client = PPC(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    return False
                self._config_client = client
            ids = client.get_stream_identifiers(stream_info)
            return bool(ids.get("app_deployment_id") and ids.get("camera_id"))
        except Exception:
            return False

    def _start_geometry_resolver(
        self,
        config: TailgatingConfig,
        stream_info: Dict[str, Any],
    ) -> None:
        if self._geometry_thread is not None:
            return

        def _resolver() -> None:
            while True:
                try:
                    result = self._resolve_geometry_from_api(config, stream_info)
                    if result is not None:
                        self._resolved_geometry_cache = result
                        self.logger.info(
                            "TailgatingDetection: zone/line geometry resolved from API "
                            "(background thread)"
                        )
                        return
                    self.logger.info(
                        "TailgatingDetection: API geometry returned None, retrying in %ds",
                        _GEOMETRY_RETRY_INTERVAL,
                    )
                except Exception as exc:
                    self.logger.warning(
                        "TailgatingDetection: background geometry resolve error: %s",
                        exc,
                    )
                time.sleep(_GEOMETRY_RETRY_INTERVAL)

        t = threading.Thread(
            target=_resolver,
            daemon=True,
            name="tailgating-zone-geometry-resolver",
        )
        self._geometry_thread = t
        t.start()
        self.logger.info(
            "TailgatingDetection: started background zone/line geometry resolver thread"
        )

    def _resolve_geometry_from_api(
        self,
        config: TailgatingConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[TailgatingConfig]:
        """Merge ``access_line`` / ``secured_zone`` (and optional buffer) from Matrice API.

        ``PostProcessingConfigClient`` returns pixel coordinates from the Matrice API;
        tailgating uses those pixel values directly (same as intrusion_detection).

        Client resolution order:
        ``set_config_client()`` → ``stream_info["config_client"]`` → env credentials.
        """
        client = self._config_client or (
            stream_info.get("config_client") if stream_info else None
        )
        if not client and stream_info:
            try:
                PPC = _post_processing_config_client_cls()
                client = PPC(logger=self.logger)
                if getattr(client, "_session", None) is None:
                    self.logger.info(
                        "TailgatingDetection: _resolve_geometry_from_api skipped "
                        "(no config_client; set MATRICE_ACCESS_KEY_ID, "
                        "MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER "
                        "or call set_config_client() for API zone resolution)"
                    )
                    return None
                self._config_client = client
            except Exception as e:
                self.logger.warning(
                    "TailgatingDetection: could not create config client from env: %s",
                    e,
                )
                return None

        if not stream_info:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api skipped (no stream_info)"
            )
            return None
        if not client:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api skipped (no config_client)"
            )
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        self.logger.info(
            "TailgatingDetection: _resolve_geometry_from_api app_deployment_id=%s camera_id=%s",
            app_deployment_id or "(empty)",
            camera_id or "(empty)",
        )

        if not app_deployment_id or not camera_id:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(missing app_deployment_id or camera_id)"
            )
            return None

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(
            app_deployment_id
        )
        if err or not configs:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(by_app_deployment err=%r, configs=%s)",
                err,
                len(configs) if configs else 0,
            )
            return None

        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(no postProcessing entry for camera_id=%s)",
                camera_id,
            )
            return None

        doc = lift_ai_camera_zones_into_post_processing(filtered[0])
        width, height = client.get_resolution(camera_id)
        if width is None or height is None:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(get_resolution width=%r height=%r for camera_id=%s)",
                width,
                height,
                camera_id,
            )
            return None

        doc_px = client.denormalize_config(doc, width, height)
        post = doc_px.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) if isinstance(post, dict) else None
        if not isinstance(cam_cfg, dict):
            return None

        zone_config_raw = cam_cfg.get("zone_config") or {}
        if not isinstance(zone_config_raw, dict):
            return None

        parsed = _tailgating_geometry_from_ui_pixels(
            zone_config_raw, int(width), int(height)
        )
        if parsed is None:
            self.logger.info(
                "TailgatingDetection: _resolve_geometry_from_api returning None "
                "(zone_config needs exactly two zones + >=1 line for camera_id=%s)",
                camera_id,
            )
            return None

        zones_px, lines_px = parsed
        merged = copy.copy(config)
        merged.zones = dict(zones_px)
        merged.access_lines = dict(lines_px)

        # Per-access-line tuning overrides live as a sibling of "zones"/"lines" inside
        # the camera "zone_config" as {access_line_id: {...}}. Hoist them onto the
        # config keyed by access_line_id. Absent -> global defaults apply.
        zone_params_raw = zone_config_raw.get("zone_params")
        if isinstance(zone_params_raw, dict) and zone_params_raw:
            merged.zone_params = dict(getattr(config, "zone_params", {}) or {})
            for k, v in zone_params_raw.items():
                if isinstance(v, dict):
                    merged.zone_params[str(k)] = dict(v)
            self.logger.info(
                "TailgatingDetection: merged API zone_params for access lines: %s",
                sorted(merged.zone_params.keys()),
            )

        self.logger.info(
            "TailgatingDetection: merged API geometry zones=%s access_lines=%s",
            sorted(merged.zones.keys()),
            sorted(merged.access_lines.keys()),
        )
        return merged

    def draw_config_zones_on_frame(
        self,
        frame: Any,
        config: TailgatingConfig,
        *,
        zone_colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]] = (
            (0, 255, 0),
            (0, 255, 255),
        ),
        access_line_color: Tuple[int, int, int] = (0, 0, 255),
        line_thickness: int = 2,
        poly_thickness: int = 2,
    ) -> None:
        """Draw the two shared zones and every access line on *frame* in place.

        *frame* is BGR; geometry points may be pixel or normalized (auto-detected).
        Requires ``opencv-python`` and ``numpy``.
        """
        import cv2
        import numpy as np

        h, w = int(frame.shape[0]), int(frame.shape[1])

        def _to_pix(pt: Any) -> Tuple[int, int]:
            if _geometry_coord_max([pt]) > 1.5:
                return int(pt[0]), int(pt[1])
            return int(pt[0] * w), int(pt[1] * h)

        for idx, (_zone_name, poly) in enumerate(sorted((config.zones or {}).items())):
            if not poly:
                continue
            pts = np.array([[_to_pix(p)[0], _to_pix(p)[1]] for p in poly], dtype=np.int32)
            cv2.polylines(frame, [pts], True, zone_colors[idx % len(zone_colors)], poly_thickness)

        for _line_id, line in (config.access_lines or {}).items():
            if line and len(line) >= 2:
                cv2.line(
                    frame,
                    _to_pix(line[0]),
                    _to_pix(line[-1]),
                    access_line_color,
                    max(1, line_thickness),
                )

    # ========================================================
    # TEMPLATE
    # ========================================================

    def create_default_config(self, **overrides):
        defaults = {
            "usecase": self.name,
            "category": "security",
            "confidence_threshold": 0.5,
        }
        defaults.update(overrides)
        return TailgatingConfig(**defaults)

    # --------------------------------------------------------
    # Internal tracking (SORT / ByteTrack — same path as loitering)
    # --------------------------------------------------------

    @staticmethod
    def _resolve_stream_fps(stream_info: Optional[Dict[str, Any]]) -> float:
        fps = 30.0
        if stream_info:
            try:
                fps_val = stream_info.get("input_settings", {}).get("original_fps")
                if fps_val and float(fps_val) > 1e-6:
                    fps = float(fps_val)
            except Exception:
                pass
        return fps

    def _init_stream_tracker(
        self,
        runtime: Dict[str, Any],
        config: TailgatingConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> None:
        """Create a per-stream tracker once (SORT default, ByteTrack optional)."""
        if runtime.get("tracker") is not None:
            return

        method = str(getattr(config, "tracking_method", "sort")).lower().strip()

        # F10b S9 (consolidation-plan.md Step 9): route the legacy SORT/ByteTrack
        # default onto the AdvancedTracker seam. MATRICE_LEGACY_SORT=1 keeps the
        # pre-migration path alive for one release (kill-switch, plan §7). A
        # fresh ConfigDrivenTracker() per stream's own `runtime` dict, matching
        # the existing per-stream SORTTracker/ByteTrackWrapper instantiation.
        if method in ("sort", "bytetrack") and os.environ.get("MATRICE_LEGACY_SORT") != "1":
            runtime["tracker"] = ConfigDrivenTracker().get_shared_tracker(
                profile=TrackerProfile.DEFAULT,
                **legacy_sort_tracker_overrides(config, method),
            )
            runtime["tracker_method"] = method
            return

        if method == "sort":
            runtime["tracker"] = SORTTracker(
                iou_threshold=float(config.tracking_iou_threshold),
                max_age=int(config.tracking_max_age),
                min_hits=int(config.tracking_min_hits),
            )
            runtime["tracker_method"] = "sort"
            return

        if method == "bytetrack":
            try:
                runtime["tracker"] = ByteTrackWrapper(
                    fps=self._resolve_stream_fps(stream_info),
                    track_thresh=float(config.bytetrack_track_thresh),
                    match_thresh=float(config.bytetrack_match_thresh),
                    track_buffer=int(config.tracking_max_age),
                )
                runtime["tracker_method"] = "bytetrack"
            except ImportError as exc:
                logger.warning(
                    "tailgating_detection: ByteTrack unavailable (%s); falling back to SORT",
                    exc,
                )
                runtime["tracker"] = SORTTracker(
                    iou_threshold=float(config.tracking_iou_threshold),
                    max_age=int(config.tracking_max_age),
                    min_hits=int(config.tracking_min_hits),
                )
                runtime["tracker_method"] = "sort"
            return

        logger.warning(
            "tailgating_detection: unknown tracking_method=%r; internal tracker disabled",
            method,
        )
        runtime["tracker"] = None

    def _apply_internal_tracking(
        self,
        detections: List[Dict[str, Any]],
        config: TailgatingConfig,
        stream_info: Optional[Dict[str, Any]],
        runtime: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Run SORT/ByteTrack when ``enable_tracking`` is True (loitering-compatible)."""
        if not config.enable_tracking or not detections:
            return detections

        self._init_stream_tracker(runtime, config, stream_info)
        tracker = runtime.get("tracker")
        if tracker is None:
            return detections

        try:
            if isinstance(tracker, ByteTrackWrapper):
                return tracker.update(detections, stream_info=stream_info)
            return tracker.update(detections)
        except Exception:
            logger.exception("tailgating_detection: internal tracker update failed")
            return detections

    def _ensure_stable_track_ids(
        self,
        detections: List[Dict[str, Any]],
        config: TailgatingConfig,
        stream_info: Optional[Dict[str, Any]],
        runtime: Dict[str, Any],
        frame_id: int,
    ) -> List[Dict[str, Any]]:
        """Internal SORT/ByteTrack when needed; keep stable upstream ids in prod."""
        if not config.enable_tracking or not detections:
            return _normalize_detection_track_ids(detections)

        # Production inference often already provides stable ids ("11", "37", …).
        if all(not _is_ephemeral_track_id(d.get("track_id")) for d in detections):
            return _normalize_detection_track_ids(detections)

        tracked = self._apply_internal_tracking(detections, config, stream_info, runtime)
        needs_fallback = any(not _track_id_usable(d.get("track_id")) for d in tracked)
        if not needs_fallback:
            return _normalize_detection_track_ids(tracked)

        sid = self._get_stream_id(stream_info)
        if sid not in self._streams_warned_tracker_fallback:
            self._streams_warned_tracker_fallback.add(sid)
            logger.warning(
                "tailgating_detection: internal tracker did not yield stable track_id; "
                "using IoU fallback (stream=%s)",
                sid,
            )

        gap = max(1, int(config.cross_memory_frames or config.tracking_max_age))
        return _normalize_detection_track_ids(
            _stabilize_ephemeral_track_ids(tracked, runtime, frame_id, max_gap_frames=gap)
        )

    def _line_geometry(
        self,
        line_id: str,
        line: List[List[float]],
        config: TailgatingConfig,
        runtime: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Per-line geometry: endpoints + side->zone map (computed once, cached).

        ``side_map`` is ``{1: zone_on_positive_side, -1: zone_on_negative_side}`` or
        ``None`` when the line does not cleanly separate the two zones (direction is
        still detected, but zone names are unavailable for labelling).
        """
        cache: Dict[str, Dict[str, Any]] = runtime.setdefault("line_geometry", {})
        if line_id not in cache:
            p1, p2 = line[0], line[1]
            side_map = build_side_zone_map(p1, p2, config.zones or {})
            cache[line_id] = {"p1": p1, "p2": p2, "side_map": side_map}
        return cache[line_id]

    # ------------------------------------------------------------------ #
    # Incident Manager                                                    #
    # ------------------------------------------------------------------ #

    def _initialize_incident_manager_once(self, config: TailgatingConfig) -> None:
        """Initialize incident manager once (first ``process()`` after config is valid)."""
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(
                "[INCIDENT_MANAGER] Starting incident manager initialization for tailgating detection..."
            )
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(
                    "[INCIDENT_MANAGER] Incident manager initialized successfully for tailgating detection"
                )
            else:
                self.logger.warning(
                    "[INCIDENT_MANAGER] Incident manager not available, incidents won't be published"
                )
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Incident manager initialization failed: {e}",
                exc_info=True,
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> None:
        """Send incident to incident manager for level tracking and publishing.

        Sets ``incident_published_via_manager`` on the context so the legacy
        analytics bridge does not double-publish the same incident to
        ``incident_res``.
        """
        if context is not None:
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        if not self._incident_manager:
            self.logger.debug("[INCIDENT_MANAGER] No incident manager available, skipping")
            return
        camera_id = ""
        if stream_info:
            camera_info = stream_info.get("camera_info", {}) or {}
            camera_id = camera_info.get("camera_id", "") or camera_info.get("cameraId", "")
            if not camera_id:
                camera_id = stream_info.get("camera_id", "") or stream_info.get("cameraId", "")
            if not camera_id:
                topic = stream_info.get("topic", "")
                if topic:
                    if topic.endswith("_input_topic"):
                        camera_id = topic[: -len("_input_topic")]
                    elif topic.endswith("_input-topic"):
                        camera_id = topic[: -len("_input-topic")]
                    elif "_input_topic" in topic:
                        camera_id = topic.split("_input_topic")[0]
                    elif "_input-topic" in topic:
                        camera_id = topic.split("_input-topic")[0]
        if not camera_id:
            camera_id = "default_camera"
        try:
            published = self._incident_manager.process_incident(
                camera_id=camera_id,
                incident_data=incident,
                stream_info=stream_info,
            )
            if published:
                self.logger.info(f"[INCIDENT_MANAGER] Incident published for camera: {camera_id}")
        except Exception as e:
            self.logger.error(
                f"[INCIDENT_MANAGER] Error sending incident to manager: {e}",
                exc_info=True,
            )

    # ========================================================

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:
        if not isinstance(config, TailgatingConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category="security",
                context=context,
            )

        si_dict: Dict[str, Any] = (
            dict(stream_info) if isinstance(stream_info, dict) else {}
        )

        si_dict = _enrich_stream_info_from_prediction(data, si_dict)

        skip_api = bool(
            (getattr(config, "extra_params", None) or {}).get(
                "skip_tailgating_api_zones"
            )
        )
        if skip_api:
            si_dict["skip_tailgating_api_zones"] = True

        if not self._zone_resolution_attempted:
            self._zone_resolution_attempted = True
            if si_dict.get("skip_tailgating_api_zones"):
                self.logger.info(
                    "TailgatingDetection: skipping API zone/line geometry "
                    "(skip_tailgating_api_zones in stream_info)"
                )
            elif si_dict:
                self.logger.info(
                    "TailgatingDetection: attempting zone/line geometry resolution from API "
                    "(first frame, blocking)"
                )
                try:
                    resolved = self._resolve_geometry_from_api(config, si_dict)
                    if resolved is not None:
                        self._resolved_geometry_cache = resolved
                        self.logger.info(
                            "TailgatingDetection: zone/line geometry resolved from API and cached"
                        )
                    elif self._api_zone_retry_is_worthwhile(si_dict):
                        self.logger.warning(
                            "TailgatingDetection: API returned no zone/line geometry on first "
                            "attempt; starting background retry thread (every %ds). "
                            "Using zones from user config until resolved.",
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, si_dict)
                    else:
                        self.logger.info(
                            "TailgatingDetection: not starting API geometry background retry "
                            "(stream_info did not yield both app_deployment_id and camera_id; "
                            "using zones from user config)"
                        )
                except Exception as exc:
                    if self._api_zone_retry_is_worthwhile(si_dict):
                        self.logger.warning(
                            "TailgatingDetection: zone/line geometry resolution raised on first "
                            "attempt (%s); starting background retry thread (every %ds). "
                            "Using zones from user config until resolved.",
                            exc,
                            _GEOMETRY_RETRY_INTERVAL,
                        )
                        self._start_geometry_resolver(config, si_dict)
                    else:
                        self.logger.warning(
                            "TailgatingDetection: zone/line geometry resolution failed (%s); "
                            "not starting background retry (stream_info lacks "
                            "app_deployment_id or camera_id, or Matrice session unavailable)",
                            exc,
                        )
            else:
                self.logger.info(
                    "TailgatingDetection: no stream_info on first frame; "
                    "using zones from user config"
                )

        effective_config = (
            self._resolved_geometry_cache
            if self._resolved_geometry_cache is not None
            else config
        )

        self._initialize_incident_manager_once(effective_config)

        try:
            effective_config.validate()
        except ValueError as exc:
            ctx = context or ProcessingContext()
            ctx.mark_completed()
            return self.create_error_result(
                str(exc),
                usecase=self.name,
                category="security",
                context=ctx,
            )

        if si_dict and si_dict.get("visualization_frame") is not None:
            try:
                self.draw_config_zones_on_frame(
                    si_dict["visualization_frame"],
                    effective_config,
                )
            except ImportError:
                logger.debug(
                    "tailgating visualization skipped: opencv and/or numpy not installed",
                )
            except Exception as e:
                logger.warning("tailgating zone visualization failed: %s", e)

        context = context or ProcessingContext()
        context.input_format = match_results_structure(data)

        stream_id = self._get_stream_id(si_dict)

        runtime = self._runtime.setdefault(
            stream_id,
            {
                "line_geometry": {},          # line_id -> {p1, p2, side_map}
                "track_side": {},             # (line_id, track_id) -> {last_side, last_side_pt}
                "events": {},                 # (line_id, direction) -> AccessPointState
                "crossing_latch": {},         # (line_id, track_id) -> frame_id
                "alert_state": {},            # ep_key -> {last_alert_ts, alerted_track_ids}
                "entity_last_frame": {},      # (line_id, track_id) -> frame_id
                "active_incidents": {},       # ep_key -> incident record
                "tailgating_event_ids": set(),  # session-cumulative AccessEvent UUIDs w/ a tailgater (VOLUME)
            },
        )

        detections = _extract_detections_from_data(data)
        if not detections and isinstance(data, list):
            detections = [d for d in data if isinstance(d, dict)]

        frame_id = _resolve_frame_id(si_dict if isinstance(si_dict, dict) else None)

        frame_output = self._process_frame(
            frame_id=frame_id,
            detections=detections,
            config=effective_config,
            stream_info=si_dict,
            runtime=runtime,
        )

        self._send_incident_to_manager(frame_output.get("incidents") or {}, si_dict, context=context)

        # String frame keys only (matches BaseProcessor.create_agg_summary / protobuf).
        agg_summary = {str(frame_id): frame_output}

        context.mark_completed()

        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category="security",
            context=context,
        )

    # ========================================================
    # FRAME PROCESSING
    # ========================================================

    def _process_frame(
        self,
        frame_id,
        detections,
        config,
        stream_info,
        runtime,
    ):
        detections = filter_by_confidence(
            detections,
            config.confidence_threshold,
        )

        target_cats = getattr(config, "target_categories", None) or ["person"]
        detections = [
            d for d in detections if _detection_matches_target_categories(d, target_cats)
        ]

        detections = self._ensure_stable_track_ids(
            detections,
            config,
            stream_info,
            runtime,
            frame_id,
        )

        raw_ts = stream_info.get("video_ts") if stream_info and "video_ts" in stream_info else time.time()
        # Monotonic clock guard: a looped video restarts video_ts to ~0 at each
        # loop boundary. A backward jump would corrupt the access-event state
        # machine (cooldown_until_ts / access_window / follow-time deltas all go
        # negative). Bridge the gap with a per-stream offset so ``now_ts`` never
        # regresses; the event machine then sees a continuous timeline across loops.
        prev_raw = runtime.get("_last_raw_ts")
        ts_offset = runtime.get("_ts_offset", 0.0)
        if prev_raw is not None and raw_ts < prev_raw - 1.0:
            ts_offset += (prev_raw - raw_ts)
            runtime["_ts_offset"] = ts_offset
        runtime["_last_raw_ts"] = raw_ts
        now_ts = raw_ts + ts_offset

        analyses: List[_PassageHit] = []

        events: Dict[Tuple[str, str], AccessPointState] = runtime.setdefault("events", {})
        track_side: Dict[Tuple[str, Any], Dict[str, Any]] = runtime.setdefault("track_side", {})
        crossing_latch: Dict[Tuple[str, Any], Any] = runtime.setdefault("crossing_latch", {})
        entity_last_frame: Dict[Tuple[str, Any], Any] = runtime.setdefault("entity_last_frame", {})

        # Foot point per usable track (geometry-independent; computed once per frame).
        foot_by_track: Dict[Any, Tuple[float, float]] = {}
        for det in detections:
            track_id = det.get("track_id")
            if not _track_id_usable(track_id):
                continue
            foot_by_track[track_id] = _foot_point_for_geometry(
                det["bounding_box"],
                stream_info if isinstance(stream_info, dict) else None,
                bottom25=False,
            )

        for line_id, line in config.access_lines.items():
            geom = self._line_geometry(line_id, line, config, runtime)
            line_p1, line_p2 = geom["p1"], geom["p2"]
            side_map = geom["side_map"]

            for track_id, foot in foot_by_track.items():
                ts_key = (line_id, track_id)
                side_state = track_side.setdefault(
                    ts_key, {"last_side": None, "last_side_pt": None}
                )
                entity_last_frame[ts_key] = frame_id

                crossed, direction_sign = detect_crossing(
                    side_state,
                    foot,
                    line_p1,
                    line_p2,
                    side_margin=config.side_margin,
                    min_motion_magnitude=config.min_motion_magnitude,
                    endpoint_padding=config.line_endpoint_padding,
                )
                if not crossed or direction_sign is None:
                    continue

                # One crossing per (line, track) per frame.
                if crossing_latch.get(ts_key) == frame_id:
                    continue
                crossing_latch[ts_key] = frame_id

                dir_key, secured_zone, buffer_zone = _direction_labels(
                    side_map, direction_sign
                )
                ev_key = (line_id, dir_key)
                state = events.get(ev_key)
                if state is None:
                    state = AccessPointState(access_line_id=line_id, direction=dir_key)
                    events[ev_key] = state

                self._handle_crossing(
                    state,
                    CrossingRecord(track_id=track_id, timestamp=now_ts),
                    config,
                    now_ts,
                )
                state.last_activity_ts = now_ts

                analysis = self._analyze_active_event_passage(state, config)
                if analysis and analysis.suspected_tailgaters:
                    active_event = state.active_event
                    analyses.append(
                        _PassageHit(
                            ep_key=f"{line_id}::{dir_key}",
                            access_line_id=line_id,
                            direction=dir_key,
                            secured_zone=secured_zone,
                            buffer_zone=buffer_zone,
                            analysis=analysis,
                            event_id=active_event.event_id if active_event else "",
                        )
                    )

        # Close any open events whose window/silence has expired. When an event
        # closes, drop its alert dedup so a genuinely new event on the same
        # (line, direction) later re-alerts, even while a merged incident persists.
        for (l_id, d_key), state in list(events.items()):
            if self._finalize_event_if_needed(state, config, now_ts) is not None:
                runtime.get("alert_state", {}).pop(f"{l_id}::{d_key}", None)

        cm = config.cross_memory_frames
        if cm > 0:
            for key in list(entity_last_frame.keys()):
                if frame_id - entity_last_frame.get(key, -1) > cm:
                    track_side.pop(key, None)
                    crossing_latch.pop(key, None)
                    entity_last_frame.pop(key, None)

        # Per-(line, direction) episodes drive the granular zone_analysis view.
        active_incidents = runtime.setdefault("active_incidents", {})
        _register_active_incidents(active_incidents, analyses, frame_id)

        current_track_ids = _track_ids_in_detections(detections)
        live_incidents, _closed_incidents = _sync_active_incidents_with_detections(
            active_incidents,
            current_track_ids,
        )

        # Single merged stream-level incident: concurrent per-(line, direction)
        # episodes are folded into one persistent incident so none are dropped from
        # the top-level field / incident manager. It stays active until every
        # accumulated suspect has left the frame; from_zone/to_zone reflect the most
        # recent contributing event. (merged_visible == union of live episode visibles.)
        incident, suspect_track_ids = self._update_merged_incident(
            runtime, analyses, current_track_ids, stream_info, frame_id
        )

        alerts = self._generate_alerts(
            analyses,
            frame_id,
            stream_info,
            config,
            runtime,
        )

        # -----------------------------
        # CLEAN DETECTIONS (remove np)
        # -----------------------------
        clean_detections: List[Dict[str, Any]] = []

        for det in detections:
            bbox = det.get("bounding_box", {})
            clean_bbox = {k: float(v) for k, v in bbox.items()}
            tid_raw = det.get("track_id")
            tid_norm = _normalize_track_id_for_label(tid_raw)
            category = (
                "tailgating_person"
                if tid_norm is not None and tid_norm in suspect_track_ids
                else "person"
            )
            clean_detections.append(
                self.create_detection_object(
                    category,
                    clean_bbox,
                    track_id=tid_raw,
                )
                | {"class_id": TAILGATING_OUTPUT_CLASS_IDS.get(category, 0)}
            )

        # -----------------------------
        # COUNTS (aligned with clean_detections categories)
        # -----------------------------
        cat_counts = Counter(d.get("category", "person") for d in clean_detections)
        total_counts = [
            self.create_count_object(cat, cat_counts[cat])
            for cat in ("person", "tailgating_person")
            if cat_counts[cat] > 0
        ]
        if not total_counts:
            total_counts = [self.create_count_object("person", 0)]
        current_counts = list(total_counts)

        n_tailgaters = cat_counts.get("tailgating_person", 0)
        person_count = len(clean_detections)

        # -----------------------------
        # HUMAN TEXT
        # -----------------------------
        if n_tailgaters:
            tracking_text = (
                f"CURRENT FRAME:\n\t- People Detected: {person_count}\n"
                f"\t- tailgating_person: {n_tailgaters}"
            )
        else:
            tracking_text = f"CURRENT FRAME:\n\t- People Detected: {person_count}"

        # -----------------------------
        # CREATE TRACKING STATS
        # -----------------------------
        tracking_stats = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=clean_detections,
            human_text=tracking_text,
            camera_info=self.get_camera_info_from_stream(stream_info),
        )
        tracking_stats["target_categories"] = list(target_cats)
        tracking_stats["current_new_counts"] = [
            {"category": cat, "count": 0} for cat in target_cats
        ]
        tracking_stats["total_current_counts"] = current_counts

        # ------------------------------------------------------------------ #
        # VOLUME analytics block (consumed by legacy_analytics_bridge).       #
        # Compact snapshot read directly by the bridge; the five keys match   #
        # tailgating-detection-metrics.json exactly.                          #
        #   people_in_frame       = all people detected now (person +          #
        #                           tailgating_person).                        #
        #   active_tailgaters     = suspected tailgaters visible now            #
        #                           (instantaneous; aggType last).             #
        #   tailgating_events     = NEW tailgating passages started this frame  #
        #                           (bridge sums over window; aggType sum).     #
        #   unique_tailgaters     = cumulative distinct tailgating passages     #
        #                           this session (aggType last).                #
        #   tailgating_percentage = tailgating_person / people_in_frame * 100. #
        #                                                                      #
        # tailgating_events / unique_tailgaters are counted per AccessEvent    #
        # (event_id), NOT per crossing-frame or per track id. This is robust   #
        # to (a) a lingering / re-crossing suspect that used to re-fire an      #
        # event every frame, and (b) track-ID churn on looped video that used  #
        # to grow the unique set without bound. Each authorization window with #
        # a tailgater counts exactly once.                                     #
        # ------------------------------------------------------------------ #
        counted_events = runtime.setdefault("tailgating_event_ids", set())
        new_events_this_frame = 0
        for hit in analyses:
            eid = getattr(hit, "event_id", "") or ""
            if eid and eid not in counted_events:
                counted_events.add(eid)
                new_events_this_frame += 1
        tracking_stats["tailgating_analytics"] = {
            "people_in_frame": int(person_count),
            "active_tailgaters": int(n_tailgaters),
            "tailgating_events": int(new_events_this_frame),
            "unique_tailgaters": int(len(counted_events)),
            "tailgating_percentage": (
                round(n_tailgaters / person_count * 100.0, 2) if person_count > 0 else 0.0
            ),
        }

        business_analytics = self.create_business_analytics(
            analysis_name="tailgating",
            statistics={
                "access_lines_monitored": len(config.access_lines),
                "zones_monitored": len(config.zones),
                "tailgating_events": len(analyses),
                "active_tailgating_incidents": len(live_incidents),
                "tailgating_person_count": n_tailgaters,
            },
            human_text=(
                f"Active tailgating incidents: {len(live_incidents)} "
                f"(new events this frame: {len(analyses)})"
            ),
            camera_info=self.get_camera_info_from_stream(stream_info),
        )

        if live_incidents:
            visible_total = len(suspect_track_ids)
            human_text = (
                f"Application: tailgating_detection\n"
                f"Active tailgating incident(s): {len(live_incidents)} "
                f"({visible_total} suspect(s) in frame)"
            )
        elif analyses:
            total = sum(len(h.analysis.suspected_tailgaters) for h in analyses)
            human_text = (
                f"Application: tailgating_detection\n"
                f"Tailgating detected: {total} unauthorized follower(s)"
            )
        else:
            human_text = "Application: tailgating_detection\nNo tailgating events detected"

        zone_analysis = _build_zone_analysis_for_frame(
            clean_detections,
            config,
            runtime,
            live_incidents,
            stream_info if isinstance(stream_info, dict) else None,
        )

        return {
            "incidents": incident,
            "tracking_stats": tracking_stats,
            "business_analytics": business_analytics,
            "alerts": alerts,
            "zone_analysis": zone_analysis,
            "human_text": human_text,
        }

    # ========================================================
    # INCIDENTS & ALERTS
    # ========================================================

    def _update_merged_incident(
        self,
        runtime: Dict[str, Any],
        analyses: List[_PassageHit],
        current_track_ids: set[Any],
        stream_info,
        frame_id: Any,
    ) -> Tuple[Dict[str, Any], set[Any]]:
        """Maintain one merged stream-level incident across all lines/directions.

        New tailgating events this frame are folded into the active merged incident
        (accumulating suspects; ``from_zone``/``to_zone``/``direction`` follow the
        latest event), opening one if none is active. The incident persists while any
        accumulated suspect is still visible and closes the frame none remain.

        Returns ``(incident_payload, visible_suspects)``. ``visible_suspects`` is the
        merged incident's suspects present this frame (used to relabel detections).
        """
        merged = runtime.get("merged_incident")

        for hit in analyses:
            new_ids = _normalize_suspect_id_set(getattr(hit.analysis, "suspected_tailgaters", None))
            if not new_ids:
                continue
            if merged is None:
                merged = {
                    "incident_id": f"tailgating_{hit.access_line_id}_{hit.direction}_{frame_id}",
                    "opened_frame": frame_id,
                    "suspects": set(),
                    "lines_involved": set(),
                    "confidence": 0.0,
                }
                logger.info(
                    "tailgating merged incident opened incident_id=%s frame=%s",
                    merged["incident_id"],
                    frame_id,
                )
            before = set(merged["suspects"])
            merged["suspects"] |= new_ids
            merged["lines_involved"].add(hit.access_line_id)
            # from/to (and the security-named aliases) reflect the latest event.
            merged["access_line_id"] = hit.access_line_id
            merged["direction"] = hit.direction
            merged["from_zone"] = hit.buffer_zone
            merged["to_zone"] = hit.secured_zone
            merged["secured_zone"] = hit.secured_zone
            merged["buffer_zone"] = hit.buffer_zone
            merged["confidence"] = max(
                float(merged.get("confidence", 0.0)),
                float(getattr(hit.analysis, "confidence", 0.0) or 0.0),
            )
            merged["last_event_frame"] = frame_id
            if merged["suspects"] != before:
                logger.info(
                    "tailgating merged incident updated incident_id=%s latest=%s %s->%s suspects=%s frame=%s",
                    merged["incident_id"],
                    hit.access_line_id,
                    hit.buffer_zone,
                    hit.secured_zone,
                    sorted(merged["suspects"], key=str),
                    frame_id,
                )

        closed_merged = None
        merged_visible: set[Any] = set()
        if merged is not None:
            merged_visible = merged["suspects"] & current_track_ids
            if not merged_visible:
                closed_merged = merged
                merged = None
                logger.info(
                    "tailgating merged incident cleared incident_id=%s frame=%s",
                    closed_merged["incident_id"],
                    frame_id,
                )
        runtime["merged_incident"] = merged

        if merged is not None:
            incident = self._build_merged_incident_payload(
                merged, merged_visible, stream_info, frame_id, closing=False
            )
        elif closed_merged is not None:
            incident = self._build_merged_incident_payload(
                closed_merged, set(), stream_info, frame_id, closing=True
            )
        else:
            incident = {}
        return incident, merged_visible

    def _build_merged_incident_payload(
        self,
        merged: Dict[str, Any],
        visible: set[Any],
        stream_info,
        frame_id: Any,
        *,
        closing: bool,
    ) -> Dict[str, Any]:
        """Render the merged incident dict (active: end_time=''; closing: real end_time)."""
        visible_list = sorted(visible, key=str)
        episode_list = sorted(merged.get("suspects", set()), key=str)
        access_line_id = merged.get("access_line_id")
        direction = merged.get("direction")
        start_timestamp = self._get_start_timestamp_str(stream_info)

        if closing:
            end_timestamp = self._get_current_timestamp_str(
                stream_info,
                frame_id=str(frame_id) if frame_id is not None else None,
            )
            human_text = (
                f"Tailgating cleared (latest {access_line_id} {direction}): {episode_list}"
            )
        else:
            end_timestamp = ""
            human_text = (
                f"Tailgating active (latest {access_line_id} {direction}): {visible_list}"
            )

        incident = self.create_incident(
            incident_id=merged["incident_id"],
            incident_type="tailgating",
            severity_level=TAILGATING_SEVERITY,
            human_text=human_text,
            camera_info=self.get_camera_info_from_stream(stream_info),
            start_time=start_timestamp,
            end_time=end_timestamp,
        )
        # create_incident replaces an empty end_time with start; force "" while active.
        incident["end_time"] = end_timestamp
        incident["access_line_id"] = access_line_id
        incident["direction"] = direction
        # Pure motion direction (latest event): from_zone (origin) -> to_zone (destination).
        incident["from_zone"] = merged.get("from_zone")
        incident["to_zone"] = merged.get("to_zone")
        incident["secured_zone"] = merged.get("secured_zone")
        incident["buffer_zone"] = merged.get("buffer_zone")
        incident["lines_involved"] = sorted(merged.get("lines_involved", set()))
        incident["suspected_tailgaters"] = [] if closing else visible_list
        incident["all_suspected_tailgaters"] = episode_list
        incident["confidence"] = merged.get("confidence", 0.0)
        incident["opened_frame"] = merged.get("opened_frame")
        incident["persistent"] = not closing

        return incident

    # --------------------------------------------------------

    def _generate_alerts(self, analyses: List[_PassageHit], frame_id, stream_info, config, runtime):
        alerts = []

        now_ts = stream_info.get("video_ts") if stream_info and "video_ts" in stream_info else time.time()

        alert_state = runtime.setdefault("alert_state", {})

        for hit in analyses:
            analysis = hit.analysis
            if not analysis.suspected_tailgaters:
                continue

            # Per-(access_line, direction) alert state.
            state = alert_state.setdefault(
                hit.ep_key, {"last_alert_ts": 0.0, "alerted_track_ids": set()}
            )

            tailgaters = analysis.suspected_tailgaters
            new_tailgaters = [tid for tid in tailgaters if tid not in state["alerted_track_ids"]]
            if not new_tailgaters:
                continue

            # Cooldown between successive alerts (not measured from t=0).
            last_alert_ts = state["last_alert_ts"]
            cooldown_ok = (
                last_alert_ts == 0.0
                or (now_ts - last_alert_ts)
                >= config._line_param(hit.access_line_id, "cooldown_sec", config.cooldown_sec)
            )
            if not cooldown_ok:
                continue

            alert_id = f"tailgating_{hit.access_line_id}_{hit.direction}_{frame_id}"
            alert = self.create_alert_object(
                alert_type="tailgating",
                alert_id=alert_id,
                incident_category="security",
                threshold_value=float(len(tailgaters)),
                ascending=True,
                settings={
                    "access_line_id": hit.access_line_id,
                    "direction": hit.direction,
                    "from_zone": hit.buffer_zone,
                    "to_zone": hit.secured_zone,
                    "secured_zone": hit.secured_zone,
                    "buffer_zone": hit.buffer_zone,
                    "tailgaters": tailgaters,
                    "new_tailgaters": new_tailgaters,
                    "confidence": analysis.confidence,
                },
            )
            alert["severity_level"] = TAILGATING_SEVERITY
            alert["event_type"] = "tailgating_detection"

            alerts.append(alert)

            state["last_alert_ts"] = now_ts
            state["alerted_track_ids"].update(tailgaters)

        return alerts

    # --------------------------------------------------------

    def _generate_summary(self, analyses: List[_PassageHit]):
        if not analyses:
            return "No tailgating events detected"

        total = sum(len(h.analysis.suspected_tailgaters) for h in analyses)
        return f"Tailgating detected: {total} unauthorized follower(s)"

    # ========================================================
    # EVENT MANAGEMENT (per access_line + direction)
    # ========================================================

    def _analyze_active_event_passage(self, state: AccessPointState, config):
        """Run tailgating analysis on the open access event (after a new crossing)."""
        event = state.active_event
        if not event or not event.crossings:
            return None
        return analyze_passage(
            event.crossings,
            config._line_param(
                state.access_line_id, "allowed_persons_per_event", config.allowed_persons_per_event
            ),
            config._line_param(
                state.access_line_id, "max_follow_time_delta_sec", config.max_follow_time_delta_sec
            ),
        )

    def _handle_crossing(self, state: AccessPointState, crossing, config, now_ts):
        if state.active_event is None:
            # Respect the post-close cooldown for this (line, direction).
            if not self.event_manager.can_open(state, now_ts):
                return
            self.event_manager.open_event(
                state,
                config._line_param(state.access_line_id, "access_window_sec", config.access_window_sec),
                now_ts,
            )

        if not state.active_event:
            return

        self.event_manager.add_crossing(state.active_event, crossing)

    # --------------------------------------------------------

    def _finalize_event_if_needed(self, state: AccessPointState, config, now_ts):
        """Close the access event when silence/access window expires (lifecycle only)."""
        event = state.active_event
        if not event:
            return None

        if not self.event_manager.should_close(
            event,
            state,
            now_ts,
            config._line_param(state.access_line_id, "silence_timeout_sec", config.silence_timeout_sec),
        ):
            return None

        return self.event_manager.close_event(
            state,
            config._line_param(state.access_line_id, "cooldown_sec", config.cooldown_sec),
            now_ts,
        )

    # ========================================================
    # STREAM ISOLATION
    # ========================================================

    def _get_stream_id(self, stream_info):
        if not stream_info:
            return "default_stream"

        camera = self.get_camera_info_from_stream(stream_info)
        return camera.get("camera_id", "default_stream")

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        if not isinstance(timestamp, str):
            return str(timestamp)

        timestamp_clean = timestamp.replace(" UTC", "").strip()
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        try:
            if timestamp_clean.count("-") >= 2:
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception as e:
            import logging

            logging.getLogger(__name__).warning(
                "Failed to normalize timestamp '%s': %s",
                timestamp_clean,
                e,
            )

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision=False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Get formatted current timestamp (aligned with intrusion/hazard; never returns literal 'NA')."""
        _ = (frame_id,)
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                candidate = stream_info.get("input_settings", {}).get("stream_time", "NA")
                if not candidate or candidate == "NA":
                    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                return self._format_timestamp(candidate)
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            candidate = stream_info.get("input_settings", {}).get("stream_time", "NA")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                        return self._format_timestamp_for_stream(timestamp)
                    except Exception:
                        return self._format_timestamp_for_stream(time.time())
                return self._format_timestamp_for_stream(time.time())
            return self._format_timestamp(candidate)

        stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
        if stream_time_str:
            try:
                timestamp_str = stream_time_str.replace(" UTC", "")
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                return self._format_timestamp_for_stream(timestamp)
            except Exception:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        if not stream_info:
            return "00:00:00"

        if precision:
            if self.start_timer is None:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except Exception:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime("%Y:%m:%d %H:%M:%S")
