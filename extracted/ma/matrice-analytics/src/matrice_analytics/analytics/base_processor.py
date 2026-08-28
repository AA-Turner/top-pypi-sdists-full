"""Base classes for the category-processor analytics framework.

BaseMetricProcessor is the abstract base for all 6 category processors
(VOLUME, INCIDENT, ZONE, QUALITY, IDENTITY, SPECIAL). It provides:
  - Per-frame processing with a template method pattern
  - 1-minute aggregation with configurable agg_type per metric
  - Track-ID counting with configurable consecutive-frame confirmation
  - Backward-compatible agg_summary output alongside new metrics[] format
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from .schemas import (
    BoundingBox,
    DetectionEntry,
    MetricEntry,
    ProcessorAggregationOutput,
    ProcessorFrameOutput,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# BaseMetricProcessor
# ---------------------------------------------------------------------------


class BaseMetricProcessor(ABC):
    """Abstract base for all category processors.

    Subclasses must implement ``_compute_frame_metrics()`` and optionally
    override ``_compute_category_metrics()`` for aggregation-time extras.
    """

    def __init__(self, category: str, manifest_config: dict[str, Any]) -> None:
        """Initialize the processor with a category name and manifest config.

        Args:
            category: The analytics category string (e.g. "VOLUME", "INCIDENT").
            manifest_config: Full parsed manifest dict from the YAML config file.
        """
        self.category = category
        self.manifest_config = manifest_config
        self.logger = logging.getLogger(f"{__name__}.{category}")

        # Build reverse lookup from entity_mapping dict:
        #   {entity: class_or_list} → {detection_class: entity}
        entity_mapping: dict[str, Any] = manifest_config.get("entity_mapping", {})
        if not entity_mapping:
            self.logger.warning(
                "No entity_mapping defined for category '%s' — all detections will pass through unfiltered",
                category,
            )
        # Case-insensitive lookup: upstream may send "Dent" while manifest uses "dent".
        # Keys are also stripped, because the labels on the other side of this lookup come
        # from a deployment config that has shipped a trailing space before now.
        self._class_to_entity: dict[str, str] = {}
        for entity, classes in entity_mapping.items():
            canonical = str(entity).strip()
            self._class_to_entity[canonical] = canonical
            self._class_to_entity[canonical.lower()] = canonical
            for cls in [classes] if isinstance(classes, str) else classes:
                alias = str(cls).strip()
                self._class_to_entity[alias] = canonical
                self._class_to_entity[alias.lower()] = canonical
        self.target_categories: list[str] = list(entity_mapping.keys())
        # Labels already reported as unmapped; see _resolve_entity_name.
        self._unmapped_entity_warned: set[str] = set()

        # Frame buffer for 1-minute aggregation
        self._frame_buffer: list[ProcessorFrameOutput] = []
        self._frame_count: int = 0

        # Track-ID confirmation: require N consecutive frames before counting
        self._min_consecutive_frames: int = max(3, int(manifest_config.get("min_consecutive_frames", 1)))
        self._track_consecutive_counts: dict[Any, int] = {}
        self._confirmed_track_ids: set[Any] = set()

        # Per-category tracking (mirrors production people_counting format)
        self._per_cat_confirmed: dict[str, set[Any]] = {}
        self._per_cat_new: dict[str, set[Any]] = {}
        self._current_detection_counts: dict[str, int] = {}

        # Running totals for sum-type metrics (entry_count, exit_count, etc.)
        # so that frame-level business_analytics shows cumulative values.
        self._cumulative_sum_metrics: dict[str, float] = {}

        # Timing
        self._last_agg_time: float | None = None
        self._reset_timestamp: str = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    def _metric_category(self, mc: dict[str, Any]) -> str:
        """Resolve the analytics category for a manifest metric entry (uppercase)."""
        return str(mc.get("category") or self.category).strip().upper()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_frame(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str = "",
    ) -> ProcessorFrameOutput:
        """Process a single frame of detections.

        Template method:
          1. ``_pre_process``  — filter to target categories
          2. ``_update_track_counts`` — update track-ID sets
          3. ``_compute_frame_metrics`` — subclass hook (returns metrics)
          4. Build ``ProcessorFrameOutput`` with business_analytics, human_text, etc.

        The engine is responsible for assembling the final ``FrameResult``
        envelope from outputs of all processors.
        """
        filtered = self._pre_process(detections)
        self._update_track_counts(filtered)

        metrics = self._compute_frame_metrics(filtered, frame_ts, frame_id)

        business_analytics: dict[str, Any] = {}
        for m in metrics:
            if m.agg_type == "sum":
                self._cumulative_sum_metrics[m.key] = self._cumulative_sum_metrics.get(m.key, 0.0) + m.data
                business_analytics[m.key] = self._cumulative_sum_metrics[m.key]
            else:
                business_analytics[m.key] = m.data

        human_text = self._build_human_text(filtered, business_analytics)
        detection_entries = self._build_detection_entries(filtered)

        output = ProcessorFrameOutput(
            metrics=metrics,
            business_analytics=business_analytics,
            human_text=human_text,
            detections=detection_entries,
            alerts=[],
            frame_ts=frame_ts,
            frame_id=frame_id,
        )

        self._frame_buffer.append(output)
        self._frame_count += 1

        if self._last_agg_time is None:
            self._last_agg_time = frame_ts

        return output

    def aggregate_1min(self) -> ProcessorAggregationOutput:
        """Aggregate buffered frames into metrics and optional VOLUME ``tracking_stats``.

        Returns a processor chunk; ``AnalyticsEngine.aggregate`` merges chunks
        into the full publisher-shaped ``AggregationResult``.
        """
        aggregated_metrics = self._aggregate_metrics(self._frame_buffer)

        tracking_stats: dict[str, Any] = self._build_tracking_stats() if self.category.upper() == "VOLUME" else {}

        result = ProcessorAggregationOutput(
            metrics=aggregated_metrics,
            tracking_stats=tracking_stats,
        )

        self._reset_buffers()

        return result

    def reset(self) -> None:
        """Full reset — clears all state including cumulative track IDs."""
        self._frame_buffer.clear()
        self._frame_count = 0
        self._track_consecutive_counts.clear()
        self._confirmed_track_ids.clear()
        self._per_cat_confirmed.clear()
        self._per_cat_new.clear()
        self._current_detection_counts.clear()
        self._cumulative_sum_metrics.clear()
        self._last_agg_time = None
        self._reset_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _pre_process(self, detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter detections to mapped classes and normalise category to entity name.

        Confidence filtering is done upstream. Raw detection classes are rewritten
        to their semantic entity names so all downstream code is model-agnostic.
        """
        if not self._class_to_entity:
            return detections
        result = []
        for det in detections:
            raw_class = det.get("category", "")
            entity = self._resolve_entity_name(raw_class)
            result.append({**det, "category": entity})
        return result

    def _resolve_entity_name(self, raw_class: Any) -> str:
        """Map a detection class label to the manifest canonical entity name.

        Labels are stripped as well as lower-cased. All three lookups below used to be
        case-insensitive but whitespace-sensitive, so a deployment ``class_index_map``
        carrying ``"gun "`` missed every one of them, warned, and returned ``"gun "`` --
        which then matched nothing downstream either.
        """
        if raw_class is None or raw_class == "":
            return ""
        label = str(raw_class).strip()
        if not label:
            return ""
        needle = label.lower()
        entity = self._class_to_entity.get(label)
        if entity is None:
            entity = self._class_to_entity.get(needle)
        if entity is None:
            # Case-insensitive match against model display labels (Person→person).
            for model_label, mapped_entity in self._class_to_entity.items():
                if str(model_label).strip().lower() == needle:
                    entity = mapped_entity
                    break
        if entity is None:
            # Once per label, not once per detection per frame: an unmapped class recurs
            # on every frame it appears in, and this used to be the log's loudest noise.
            if needle not in self._unmapped_entity_warned:
                self._unmapped_entity_warned.add(needle)
                self.logger.warning(
                    "No entity mapping for class '%s' — using class name as entity. The "
                    "manifest maps %s; a class that matches none of them is ignored by "
                    "every downstream filter.",
                    raw_class,
                    sorted(str(k) for k in self._class_to_entity),
                )
            return label
        return entity

    def _update_track_counts(self, detections: list[dict[str, Any]]) -> None:
        """Update track-ID sets from pre-tracked detections.

        A track ID is only promoted to "confirmed" once it has appeared in
        at least ``_min_consecutive_frames`` consecutive frames, filtering
        out flickering / noisy detections.  Short dropouts are tolerated
        via a soft-decay counter: a one-frame miss decrements the counter
        by 1 instead of resetting it to 0, so a brief occlusion does not
        force the track to re-qualify from scratch.

        Each track ID is reported as "new" exactly once — the frame in
        which its counter first reaches ``_min_consecutive_frames``.

        Mirrors the confirmed-track logic from the production
        ``PeopleCountingUseCase._update_tracking_state``.
        """
        raw_ids: set[Any] = set()
        per_cat_raw: dict[str, set[Any]] = {cat: set() for cat in self.target_categories}
        detection_counts: dict[str, int] = {}

        for det in detections:
            cat = det.get("category", "")
            detection_counts[cat] = detection_counts.get(cat, 0) + 1
            tid = det.get("track_id")
            if tid is not None:
                raw_ids.add(tid)
                if cat in per_cat_raw:
                    per_cat_raw[cat].add(tid)

        self._current_detection_counts = detection_counts

        min_hits = self._min_consecutive_frames
        next_counts: dict[Any, int] = {}

        # Increment consecutive counts for IDs present this frame (capped)
        for tid in raw_ids:
            next_counts[tid] = min(min_hits, self._track_consecutive_counts.get(tid, 0) + 1)

        # Soft decay for IDs not seen this frame
        for tid, prev in self._track_consecutive_counts.items():
            if tid in raw_ids:
                continue
            decayed = max(0, prev - 1)
            if decayed > 0:
                next_counts[tid] = decayed

        self._track_consecutive_counts = next_counts

        # Promote newly confirmed IDs into the permanent confirmed set
        newly_confirmed: set[Any] = set()
        for tid, count in next_counts.items():
            if count >= min_hits and tid not in self._confirmed_track_ids:
                self._confirmed_track_ids.add(tid)
                newly_confirmed.add(tid)

        # Per-category sets (for production-format tracking_stats output)
        self._per_cat_new = {cat: set() for cat in self.target_categories}
        for cat, ids in per_cat_raw.items():
            for tid in ids:
                if tid in newly_confirmed:
                    self._per_cat_new[cat].add(tid)

        for cat, ids in per_cat_raw.items():
            confirmed_in_cat = ids & self._confirmed_track_ids
            if confirmed_in_cat:
                self._per_cat_confirmed.setdefault(cat, set()).update(confirmed_in_cat)

    def _build_detection_entries(self, detections: list[dict[str, Any]]) -> list[DetectionEntry]:
        """Convert raw detection dicts to DetectionEntry models."""
        entries: list[DetectionEntry] = []
        for det in detections:
            bbox_raw = det.get("bounding_box", det.get("bbox", {}))
            if isinstance(bbox_raw, dict):
                bbox = BoundingBox(
                    xmin=float(bbox_raw.get("xmin", bbox_raw.get("x1", 0.0))),
                    ymin=float(bbox_raw.get("ymin", bbox_raw.get("y1", 0.0))),
                    xmax=float(bbox_raw.get("xmax", bbox_raw.get("x2", 0.0))),
                    ymax=float(bbox_raw.get("ymax", bbox_raw.get("y2", 0.0))),
                )
            else:
                bbox = BoundingBox()
            entries.append(DetectionEntry(category=det.get("category", ""), bounding_box=bbox))
        return entries

    def _build_human_text(self, detections: list[dict[str, Any]], business_analytics: dict[str, Any]) -> str:
        """Build human-readable summary text. Override in subclass for custom text."""
        count = len(detections)
        default_cat = self.target_categories[0] if self.target_categories else "object"
        return f"{count} {default_cat} detected in monitored area"

    @abstractmethod
    def _compute_frame_metrics(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str,
    ) -> list[MetricEntry]:
        """Compute category-specific per-frame metrics.

        Subclasses must implement this. The detections are already filtered
        to target categories and have track_id assigned.

        Returns:
            List of :class:`MetricEntry` for this frame.
        """
        ...

    def _aggregate_metrics(self, frame_results: list[ProcessorFrameOutput]) -> list[dict[str, Any]]:
        """Aggregate per-frame MetricEntry lists by key and agg_type."""
        values_by_key: dict[str, list[float]] = defaultdict(list)
        agg_type_by_key: dict[str, str] = {}
        category_by_key: dict[str, str] = {}
        zone_by_key: dict[str, str] = {}

        for fr in frame_results:
            for m in fr.metrics:
                values_by_key[m.key].append(m.data)
                agg_type_by_key[m.key] = m.agg_type
                category_by_key[m.key] = m.category
                zone_by_key[m.key] = m.zone

        aggregated: list[dict[str, Any]] = []
        for key, values in values_by_key.items():
            agg_type = agg_type_by_key[key]
            category = category_by_key[key]
            zone = zone_by_key[key]
            if agg_type == "sum":
                result_value = sum(values)
            elif agg_type == "max":
                result_value = max(values) if values else 0
            elif agg_type == "min":
                result_value = min(values) if values else 0
            elif agg_type == "avg":
                result_value = sum(values) / len(values) if values else 0
            elif agg_type == "last":
                result_value = values[-1] if values else 0
            else:
                self.logger.warning("Unknown agg_type '%s' for key '%s', using sum", agg_type, key)
                result_value = sum(values)

            aggregated.append(
                {
                    "key": key,
                    "data": result_value,
                    "agg_type": agg_type,
                    "category": category,
                    "zone": zone,
                }
            )

        return aggregated

    def _build_tracking_stats(self) -> dict[str, Any]:
        """Build aggregation-level tracking_stats with count arrays."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        total_counts = [
            {"category": cat, "count": len(ids)} for cat, ids in self._per_cat_confirmed.items() if len(ids) > 0
        ]
        current_counts = [{"category": cat, "count": count} for cat, count in self._current_detection_counts.items()]
        current_new_counts = [{"category": cat, "count": len(ids)} for cat, ids in self._per_cat_new.items()]

        return {
            "input_timestamp": now,
            "current_counts": current_counts,
            "current_new_counts": current_new_counts,
            "total_counts": total_counts,
            "total_current_counts": current_counts,
        }

    def _reset_buffers(self) -> None:
        """Reset per-window buffers. Does NOT reset cumulative track IDs."""
        self._frame_buffer.clear()
        self._last_agg_time = None
