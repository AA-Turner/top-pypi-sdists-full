"""QualityProcessor -- QUALITY category processor.

Handles defect-detection analytics: defect count, total inspected,
and defect rate.

Supports apps like: Bottle Defect Detection, Weld Defect Detection,
PCB Inspection, Concrete Crack Detection, Car Damage Detection, etc.

The per-frame output and 1-minute aggregation output are structured to
match the production ``results-agg`` Redis stream contract so that
downstream consumers (Go tracker, ClickHouse, UI) see identical JSON.

Design note: ``defect_rate`` in the 1-min aggregation is computed as
**unique defects / unique inspected** in that window, not as an average
of per-frame rates.  The backend receives per-window rates and can
further aggregate to 1hr/2hr/etc. windows without re-deriving.

Unique counts are derived from the base class's track-ID confirmation
state (``_per_cat_new``), so flickering / unconfirmed detections are
automatically excluded.
"""
from __future__ import annotations

import logging
from typing import Any

from ..base_processor import BaseMetricProcessor, MetricEntry
from ..schemas import ProcessorAggregationOutput


logger = logging.getLogger(__name__)


class QualityProcessor(BaseMetricProcessor):
    """QUALITY category processor for defect-detection analytics.

    Per-frame metrics (from ``_compute_frame_metrics``):

    - **defect_count**: number of defect-class detections in this frame.
    - **total_inspected**: number of inspection-class detections in this
      frame (e.g. bottles currently visible).
    - **defect_rate**: ``defect_count / total_inspected`` for this frame.

    1-minute aggregation (from ``aggregate_1min``, overridden):

    - **defect_count**: unique defect track IDs confirmed in the 60s window.
    - **total_inspected**: unique inspection-class track IDs confirmed in
      the 60s window.
    - **defect_rate**: ``unique_defects / unique_inspected`` (window-level).

    The YAML manifest's ``quality.metrics`` section controls which keys
    are emitted.  ``quality.inspection_classes`` and
    ``quality.defect_classes`` configure which entity names count as
    inspected items vs defects.
    """

    # Entity names counted as "defects" for defect_count / defect_rate.
    # Populated from ``quality.defect_classes`` in the manifest;
    # defaults to all entity-mapped classes.
    _defect_classes: set[str]

    # Entity names counted as "items being inspected" for total_inspected.
    # Populated from ``quality.inspection_classes`` in the manifest.
    # When ``None``, total_inspected falls back to counting all detections
    # (useful for single-class defect-only models).
    _inspection_classes: set[str] | None

    def __init__(
        self,
        category: str,
        manifest_config: dict[str, Any],
        zone_id: str = "",
    ) -> None:
        """Initialise QualityProcessor.

        Args:
            category: Passed by the engine; always overridden to ``"QUALITY"``.
            manifest_config: Full parsed manifest dict from the YAML config.
            zone_id: Optional zone name when running per-zone analytics.
                Empty string means global (no zone).
        """
        super().__init__(category="QUALITY", manifest_config=manifest_config)
        self._zone_id: str = zone_id

        quality_section = manifest_config.get("quality", {}) or {}

        # Metrics declared in the manifest (same pattern as VolumeProcessor)
        raw_metrics = quality_section.get("metrics") or []
        self._metrics_config: list[dict[str, str]] = [
            m for m in raw_metrics if isinstance(m, dict) and "key" in m
        ]
        if not self._metrics_config:
            self._metrics_config = [
                {"key": "defect_count", "agg_type": "sum"},
                {"key": "total_inspected", "agg_type": "sum"},
                {"key": "defect_rate", "agg_type": "avg"},
            ]

        # Which entity names are "defects"?
        defect_classes_raw = quality_section.get("defect_classes")
        if defect_classes_raw and isinstance(defect_classes_raw, list):
            self._defect_classes = set(defect_classes_raw)
        else:
            self._defect_classes = set(self.target_categories)

        # Which entity names are "items being inspected"?
        inspection_classes_raw = quality_section.get("inspection_classes")
        if inspection_classes_raw and isinstance(inspection_classes_raw, list):
            self._inspection_classes = set(inspection_classes_raw)
        else:
            self._inspection_classes = None

        # Per-window unique track IDs, sourced from ``_per_cat_new`` (which
        # the base class's ``_update_track_counts`` populates with IDs that
        # were newly confirmed this frame).  Accumulated across the window
        # so ``aggregate_1min`` can emit window-level unique counts.
        self._window_defect_ids: set[Any] = set()
        self._window_inspection_ids: set[Any] = set()
        # Peak per-frame counts when track confirmation yields no uniques.
        self._window_peak_inspected: int = 0
        self._window_peak_defect: int = 0

    # ------------------------------------------------------------------
    # Core per-frame computation
    # ------------------------------------------------------------------

    def _compute_frame_metrics(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str,
    ) -> list[MetricEntry]:
        """Compute per-frame QUALITY metrics.

        Detections are already filtered to entity-mapped classes and
        normalised by ``_pre_process``.  The base class has also already
        called ``_update_track_counts``, so ``self._per_cat_new`` reflects
        the IDs newly confirmed on this frame.

        Returns:
            List of ``MetricEntry`` for the keys declared in
            ``quality.metrics``.
        """
        # ── Per-frame raw counts ───────────────────────────────────────
        if self._inspection_classes is not None:
            total_inspected = sum(
                1 for det in detections
                if det.get("category", "") in self._inspection_classes
            )
        else:
            total_inspected = len(detections)

        defect_count = sum(
            1 for det in detections
            if det.get("category", "") in self._defect_classes
        )

        defect_rate = (
            defect_count / total_inspected if total_inspected > 0 else 0.0
        )

        self._window_peak_inspected = max(self._window_peak_inspected, total_inspected)
        self._window_peak_defect = max(self._window_peak_defect, defect_count)

        # ── Accumulate window-level unique IDs from confirmed tracks ───
        # ``_per_cat_new`` holds IDs that were newly confirmed this frame,
        # keyed by entity name.  Union them into the window sets so the
        # 1-min aggregation can report unique counts.
        for cat in self._defect_classes:
            self._window_defect_ids.update(self._per_cat_new.get(cat, set()))

        if self._inspection_classes is not None:
            for cat in self._inspection_classes:
                self._window_inspection_ids.update(
                    self._per_cat_new.get(cat, set())
                )
        else:
            # Fallback: treat every target category as an "inspected" item.
            for cat in self.target_categories:
                self._window_inspection_ids.update(
                    self._per_cat_new.get(cat, set())
                )

        # ── Build MetricEntry list driven by manifest config ───────────
        computed: dict[str, float] = {
            "defect_count": float(defect_count),
            "total_inspected": float(total_inspected),
            "defect_rate": defect_rate,
        }

        metrics: list[MetricEntry] = []
        for mc in self._metrics_config:
            key = mc["key"]
            value = computed.get(key)
            if value is not None:
                metrics.append(
                    MetricEntry(
                        key=key,
                        data=value,
                        agg_type=mc.get("agg_type", "sum"),
                        category=self._metric_category(mc),
                        zone=self._zone_id,
                    )
                )

        return metrics

    # ------------------------------------------------------------------
    # Aggregation override -- window-level defect_rate
    # ------------------------------------------------------------------

    def aggregate_1min(self) -> ProcessorAggregationOutput:
        """Aggregate buffered frames into window-level QUALITY metrics.

        Overrides the base class's default averaging behaviour because
        ``defect_rate`` must be computed on window-level uniques, not as
        a mean of per-frame rates.

        Emits:
            - ``defect_count``    = unique defect track IDs confirmed in window.
            - ``total_inspected`` = unique inspection-class track IDs confirmed in window.
            - ``defect_rate``     = unique_defects / unique_inspected.

        QUALITY processors do not emit ``tracking_stats``; only VOLUME does.
        """
        unique_defects = len(self._window_defect_ids)
        unique_inspected = len(self._window_inspection_ids)
        if unique_inspected == 0 and self._window_peak_inspected > 0:
            unique_inspected = self._window_peak_inspected
        if unique_defects == 0 and self._window_peak_defect > 0:
            unique_defects = self._window_peak_defect

        window_defect_rate = (
            unique_defects / unique_inspected if unique_inspected > 0 else 0.0
        )

        window_values: dict[str, float] = {
            "defect_count": float(unique_defects),
            "total_inspected": float(unique_inspected),
            "defect_rate": window_defect_rate,
        }

        aggregated_metrics: list[dict[str, Any]] = []
        for mc in self._metrics_config:
            key = mc["key"]
            if key in window_values:
                aggregated_metrics.append(
                    {
                        "key": key,
                        "data": window_values[key],
                        "agg_type": mc.get("agg_type", "sum"),
                        "category": self._metric_category(mc),
                        "zone": self._zone_id,
                    }
                )

        result = ProcessorAggregationOutput(
            metrics=aggregated_metrics,
            tracking_stats={},
        )

        self._reset_buffers()
        return result

    # ------------------------------------------------------------------
    # Human-readable text
    # ------------------------------------------------------------------

    def _build_human_text(
        self,
        detections: list[dict[str, Any]],
        business_analytics: dict[str, Any],
    ) -> str:
        """Build per-frame human text for defect detection."""
        if self._inspection_classes is not None:
            total = sum(
                1 for d in detections
                if d.get("category", "") in self._inspection_classes
            )
        else:
            total = len(detections)

        defects = sum(
            1 for d in detections
            if d.get("category", "") in self._defect_classes
        )
        rate_pct = (defects / total * 100) if total > 0 else 0.0

        zone_prefix = f"Zone {self._zone_id} — " if self._zone_id and self._zone_id != "global" else ""
        lines = [
            f"{zone_prefix}CURRENT FRAME:",
            f"\t- Defects detected: {defects}",
            f"\t- Total inspected: {total}",
            f"\t- Defect rate: {rate_pct:.1f}%",
            "",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Overrides -- reset accumulators
    # ------------------------------------------------------------------

    def _reset_buffers(self) -> None:
        """Reset per-window buffers including QUALITY accumulators."""
        super()._reset_buffers()
        self._window_defect_ids.clear()
        self._window_inspection_ids.clear()
        self._window_peak_inspected = 0
        self._window_peak_defect = 0

    def reset(self) -> None:
        """Full reset including QUALITY-specific state."""
        super().reset()
        self._window_defect_ids.clear()
        self._window_inspection_ids.clear()
        self._window_peak_inspected = 0
        self._window_peak_defect = 0
