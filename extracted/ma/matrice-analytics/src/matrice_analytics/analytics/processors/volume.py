"""VolumeProcessor — VOLUME category processor.

Handles counting-based analytics: entry/exit counts, current occupancy,
peak count, unique count, and turnover rate.

Supports two counting modes:
  - **Simple** (default): new track_id = entry, no exit logic.
  - **Geometry-based**: uses ``ABLineCounter`` / ``PolygonCounter`` for real
    entry/exit counting when a ``zone_config`` is provided via
    ``set_zone_config()``.

Covers apps like: People Counting, Vehicle Monitoring, Footfall,
Pedestrian Detection, Shelf Inventory, etc.

The per-frame output and 1-minute aggregation output are structured to
match the production ``PeopleCountingUseCase`` / ``AnalyticsPublisher``
contract so that downstream consumers (UI, DB, Redis) see identical JSON.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import numpy as np

from ..base_processor import BaseMetricProcessor, MetricEntry
from ..geometry import create_counter_from_zone_config, denormalize_zone_config


logger = logging.getLogger(__name__)


class VolumeProcessor(BaseMetricProcessor):
    """VOLUME category processor for counting-based analytics.

    Computes per-frame metrics (entry_count, exit_count, current_occupancy)
    and aggregation-time metrics (peak_count, unique_count, turnover_rate).

    When geometry (zone_config) is set via ``set_zone_config()``, entry/exit
    counts are derived from line-crossing or polygon-based counters. Otherwise,
    falls back to simple track-ID counting.

    Window-level aggregation mirrors ``AnalyticsPublisher`` semantics:

    - **current_counts** = SUM of per-frame ``current_new_counts``
      (new arrivals in the 1-min window).
    - **total_current_counts** = previous window's last-frame occupancy
      + accumulated new arrivals (0 carry on first window).
    - **total_counts** = cumulative unique since last full reset.
    """

    def __init__(
        self,
        category: str,
        manifest_config: dict[str, Any],
        zone_id: str = "",
    ) -> None:
        """Initialize VolumeProcessor, ignoring ``category`` in favour of "VOLUME".

        Args:
            category: Passed by the engine; always overridden to ``"VOLUME"``.
            manifest_config: Full parsed manifest dict from the YAML config file.
            zone_id: Optional zone name when running per-zone analytics.
                Empty string means global (no zone).
        """
        super().__init__(category="VOLUME", manifest_config=manifest_config)
        self._zone_id: str = zone_id

        # Parse metrics config from manifest (volume.metrics section)
        volume_section = manifest_config.get("volume", {}) or {}
        raw_metrics = volume_section.get("metrics") or []
        self._metrics_config: list[dict[str, str]] = [
            m for m in raw_metrics if isinstance(m, dict) and "key" in m
        ]

        # Per-frame accumulators for aggregation
        self._frame_occupancies: list[int] = []
        self._frame_entry_counts: list[int] = []

        # Geometry-based counting (None = fallback to simple track-ID counting)
        self._counter: Any | None = None
        self._counter_method: str | None = None
        self._zone_config_raw: dict[str, Any] | None = None

        # Window-level aggregation accumulators (match analytics_publisher)
        # Accumulated new arrivals: SUM of current_new_counts across all frames
        self._window_new_counts_sum: dict[str, int] = {}
        # Last-frame in-frame occupancy this window (carried to next on publish)
        self._last_frame_current: dict[str, int] = {}
        # Previous window last-frame occupancy (0 until first publish)
        self._prev_window_last_frame_current: dict[str, int] = {}

    # ------------------------------------------------------------------
    # Geometry configuration
    # ------------------------------------------------------------------

    def set_zone_config(
        self,
        zone_config: dict[str, Any],
        width: int,
        height: int,
        method: str = "abline",
        in_direction: str = "A_to_B",
        use_foot_center: bool = False,
    ) -> None:
        """Set geometry and create a counting counter for entry/exit analytics.

        After calling this, ``_compute_frame_metrics`` will use the geometry
        counter instead of simple track-ID counting.

        Args:
            zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized
                (0-1) coordinates, matching the Matrice post-processing API format.
            width: Frame width in pixels (for denormalization).
            height: Frame height in pixels (for denormalization).
            method: ``"abline"`` (two-line trap zone) or ``"polygon"``
                (double-polygon hysteresis).
            in_direction: For abline method -- ``"A_to_B"`` or ``"B_to_A"``.
            use_foot_center: Use bottom-center of bbox instead of center.
        """
        self._zone_config_raw = zone_config
        zone_config_px = denormalize_zone_config(zone_config, width, height)
        self._counter = create_counter_from_zone_config(
            zone_config_px,
            method=method,
            in_direction=in_direction,
            use_foot_center=use_foot_center,
        )
        self._counter_method = method
        self.logger.info(
            "VolumeProcessor: zone_config set (method=%s, resolution=%dx%d)",
            method,
            width,
            height,
        )

    def remove_zone_config(self) -> None:
        """Remove geometry config and revert to simple track-ID counting."""
        self._counter = None
        self._counter_method = None
        self._zone_config_raw = None
        self.logger.info("VolumeProcessor: zone_config removed, reverting to simple counting")

    @property
    def has_geometry(self) -> bool:
        """Whether a geometry counter is active."""
        return self._counter is not None

    # ------------------------------------------------------------------
    # Core per-frame computation
    # ------------------------------------------------------------------

    def _compute_frame_metrics(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str,
    ) -> list[MetricEntry]:
        """Compute VOLUME metrics for a single frame.

        When a geometry counter is active, uses it for entry/exit.
        Otherwise falls back to simple track-ID counting with raw
        detection count for occupancy (matching production behaviour).
        """
        if self._counter is not None:
            entry_count, exit_count, current_occupancy = self._compute_with_counter(detections)
        else:
            current_occupancy = len(detections)
            entry_count = sum(len(ids) for ids in self._per_cat_new.values())
            exit_count = 0

        self._frame_occupancies.append(current_occupancy)
        self._frame_entry_counts.append(entry_count)

        # Latest in-frame occupancy this window (for next-window carry).
        self._last_frame_current = dict(self._current_detection_counts)

        for cat, ids in self._per_cat_new.items():
            new_count = len(ids)
            if new_count > 0:
                self._window_new_counts_sum[cat] = self._window_new_counts_sum.get(cat, 0) + new_count

        metrics: list[MetricEntry] = []
        if self._metrics_config:
            computed = {
                "entry_count": float(entry_count),
                "exit_count": float(exit_count),
                "current_occupancy": float(current_occupancy),
            }
            for mc in self._metrics_config:
                key = mc["key"]
                if key in computed:
                    metrics.append(
                        MetricEntry(
                            key=key,
                            data=computed[key],
                            agg_type=mc.get("agg_type", "sum"),
                            category=self._metric_category(mc),
                            zone=self._zone_id,
                        )
                    )

        return metrics

    def _compute_with_counter(self, detections: list[dict[str, Any]]) -> tuple[int, int, int]:
        """Run the geometry counter on this frame's detections.

        Returns:
            Tuple of (entry_count, exit_count, current_occupancy).
        """
        boxes, track_ids = self._extract_boxes_and_ids(detections)
        self._counter.update(boxes, track_ids)
        return (
            self._counter.new_in,
            self._counter.new_out,
            self._counter.present_count,
        )

    # ------------------------------------------------------------------
    # Aggregation-time category metrics
    # ------------------------------------------------------------------


    # ------------------------------------------------------------------
    # Aggregation output — match AnalyticsPublisher format
    # ------------------------------------------------------------------

    def _build_tracking_stats(self) -> dict[str, Any]:
        """Build aggregated tracking_stats matching analytics_publisher output.

        Output mapping (mirrors ``AnalyticsPublisher._build_analytics_message``):

        - ``current_counts``  = accumulated ``current_new`` (new arrivals in window)
        - ``current_new_counts`` = per-category new counts from the latest frame
        - ``total_current_counts`` = prev window last-frame occupancy + new arrivals
        - ``total_counts``    = cumulative unique since reset
        """
        now_ts = datetime.now(timezone.utc)
        input_timestamp = now_ts.strftime("%Y-%m-%dT%H:%M:%SZ")

        current_counts: list[dict[str, Any]] = [
            {"category": cat, "count": count} for cat, count in self._window_new_counts_sum.items()
        ]
        if not current_counts:
            current_counts = [{"category": cat, "count": 0} for cat in self.target_categories]

        current_new_counts: list[dict[str, Any]] = [
            {"category": cat, "count": len(ids)} for cat, ids in self._per_cat_new.items()
        ]
        if not current_new_counts:
            current_new_counts = [{"category": cat, "count": 0} for cat in self.target_categories]

        all_cats = (
            set(self._prev_window_last_frame_current.keys())
            | set(self._window_new_counts_sum.keys())
            | set(self.target_categories)
        )
        total_current_counts: list[dict[str, Any]] = []
        for cat in sorted(all_cats):
            prev_last = self._prev_window_last_frame_current.get(cat, 0)
            new_arrivals = self._window_new_counts_sum.get(cat, 0)
            total_current_counts.append({"category": cat, "count": prev_last + new_arrivals})

        total_counts: list[dict[str, Any]] = [
            {"category": cat, "count": len(ids)} for cat, ids in self._per_cat_confirmed.items() if len(ids) > 0
        ]

        return {
            "input_timestamp": input_timestamp,
            "current_counts": current_counts,
            "current_new_counts": current_new_counts,
            "total_counts": total_counts,
            "total_current_counts": total_current_counts,
        }

    # ------------------------------------------------------------------
    # Human-readable text — match production PeopleCountingUseCase
    # ------------------------------------------------------------------

    def _build_human_text(self, detections: list[dict[str, Any]], business_analytics: dict[str, Any]) -> str:
        """Build per-frame human text matching production people_counting format."""
        default_cat = self.target_categories[0] if self.target_categories else "object"
        display_name = default_cat.title()
        count = self._current_detection_counts.get(default_cat, len(detections))
        new_count = len(self._per_cat_new.get(default_cat, set()))

        zone_prefix = f"Zone {self._zone_id} — " if self._zone_id else ""
        lines = [
            f"{zone_prefix}CURRENT FRAME:",
            f"\t- Total {display_name} in Frame: {count}",
            f"\t- New {display_name} (just entered): {new_count}",
            "",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------------

    def _reset_buffers(self) -> None:
        """Reset per-window buffers including VOLUME accumulators."""
        super()._reset_buffers()
        # Carry last-frame occupancy into the next window before clearing.
        self._prev_window_last_frame_current = dict(self._last_frame_current)
        self._frame_occupancies.clear()
        self._frame_entry_counts.clear()
        self._window_new_counts_sum.clear()
        self._last_frame_current = {}

    def reset(self) -> None:
        """Full reset including VOLUME-specific state."""
        super().reset()
        self._frame_occupancies.clear()
        self._frame_entry_counts.clear()
        self._window_new_counts_sum.clear()
        self._last_frame_current = {}
        self._prev_window_last_frame_current = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_boxes_and_ids(
        detections: list[dict[str, Any]],
    ) -> tuple[np.ndarray, np.ndarray]:
        """Extract bounding boxes and track IDs from detection dicts.

        Args:
            detections: List of detection dicts, each with ``bounding_box``
                (or ``bbox``) and ``track_id``.

        Returns:
            Tuple of ``(boxes, track_ids)`` as numpy arrays. ``boxes`` has
            shape ``(N, 4)`` in ``[x1, y1, x2, y2]`` format; ``track_ids``
            has shape ``(N,)``.
        """
        boxes_list: list[list[float]] = []
        ids_list: list[int] = []

        for idx, det in enumerate(detections):
            raw_bbox = det.get("bounding_box", det.get("bbox"))
            xyxy = _bbox_to_xyxy(raw_bbox)
            if xyxy is None:
                continue
            track_id = det.get("track_id")
            if track_id is None:
                track_id = idx
            else:
                try:
                    track_id = int(track_id)
                except (ValueError, TypeError):
                    track_id = hash(track_id) % (10**9)
            boxes_list.append([float(v) for v in xyxy])
            ids_list.append(track_id)

        if not boxes_list:
            return np.empty((0, 4), dtype=np.float64), np.empty((0,), dtype=np.int64)

        return (
            np.array(boxes_list, dtype=np.float64),
            np.array(ids_list, dtype=np.int64),
        )


def _bbox_to_xyxy(bbox: Any) -> list[float] | None:
    """Convert a bounding-box (dict or list) to ``[x1, y1, x2, y2]``."""
    if isinstance(bbox, list):
        return bbox[:4] if len(bbox) >= 4 else None
    if isinstance(bbox, dict):
        if "x1" in bbox:
            return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
        if "xmin" in bbox:
            return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
        vals = list(bbox.values())
        return vals[:4] if len(vals) >= 4 else None
    return None
