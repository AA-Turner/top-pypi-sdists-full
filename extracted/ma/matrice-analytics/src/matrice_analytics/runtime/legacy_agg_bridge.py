"""agg_summary shape bridge (PY-5), split out of runtime/backends.py.

Moved here verbatim (INC-2026-146 file-size cap) -- fully self-contained: nothing outside
this module reads its private helpers, only :func:`legacy_shape_agg_summary` and
:data:`LEGACY_AGG_SHAPE_ENV` are re-exported from ``backends.py`` for the existing public
import path (``from matrice_analytics.runtime.backends import legacy_shape_agg_summary``).
"""

from __future__ import annotations

import os
from typing import Any, Dict, Final, List, Optional, Sequence, Tuple

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
    corners = (
        tuple(box.get(c) for c in ("xmin", "ymin", "xmax", "ymax")) if isinstance(box, dict) else ()
    )
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
