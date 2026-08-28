"""SafetyProcessor -- SAFETY category processor.

Handles PPE (Personal Protective Equipment) compliance analytics for
apps like PPE Detection on construction sites, warehouses, and
industrial floors.

This processor supports two deployment shapes:

**Two-stage (person detector + PPE on crop):**
  Person bboxes get stable ``track_id``; PPE items inherit the person's id.
  Compliance is evaluated **per person** (``required_ppe`` + ``violation_classes``).

**Single-stage (PPE_Detection.pt on full frame):**
  The model emits PPE / NO-* boxes without separate Person detections.
  When no ``person`` boxes are present, **violation-class detections**
  (``no_hardhat``, ``no_mask``, ``no_safety_vest``) are counted directly —
  matching legacy ``ppe_compliance.py`` behaviour.

1-minute aggregation:
  - ``compliance_pct`` is emitted with ``agg_type=mean`` because the
    design (``ANALYTICS_FLOW_DESIGN.md`` §3.7) mandates per-frame
    averaging — Go sees per-minute totals and cannot recover the
    correct ratio from unique-count sums.
  - Unique counts (``total_persons``, ``violation_count``) come from
    confirmed track IDs accumulated across the window via
    ``self._per_cat_new`` (populated by the base class).
"""
from __future__ import annotations

import logging
from typing import Any

from ..base_processor import BaseMetricProcessor
from ..schemas import MetricEntry, ProcessorAggregationOutput


logger = logging.getLogger(__name__)


class SafetyProcessor(BaseMetricProcessor):
    """SAFETY category processor for PPE compliance analytics.

    Per-frame metrics (``_compute_frame_metrics``):

    - **total_persons**: number of person detections in this frame.
    - **compliant_count**: persons wearing all ``required_ppe`` items.
    - **violation_count**: persons missing any required PPE (or with
      a direct violation-class detection).
    - **compliance_pct**: ``compliant_count / total_persons * 100`` for
      the current frame (0.0 when no persons).
    - **<item>_count**: one entry per configured PPE item (e.g.
      ``hardhat_count``, ``vest_count``).

    1-minute aggregation (``aggregate_1min`` override):

    - ``total_persons``      = unique person track IDs confirmed in window.
    - ``violation_count``    = unique violator track IDs in window.
    - ``compliance_pct``     = mean of per-frame compliance_pct values.
    - ``<item>_count``       = unique track IDs per PPE item in window.

    YAML manifest (``safety:`` section) drives:

    - ``person_classes``:     entity names counted as persons.
    - ``ppe_classes``:        entity names recognised as PPE items.
    - ``required_ppe``:       subset of ``ppe_classes`` that MUST be worn.
    - ``violation_classes``:  entity names that directly indicate a
                              violation (model-emitted ``NO-*`` labels).
    - ``metrics``:            which metric keys to emit (same shape as
                              other processors).
    """

    # Populated from the manifest ``safety:`` block.
    _person_classes: set[str]
    _ppe_classes: set[str]
    _required_ppe: set[str]
    _violation_classes: set[str]

    def __init__(
        self,
        category: str,
        manifest_config: dict[str, Any],
        zone_id: str = "",
    ) -> None:
        """Initialise SafetyProcessor.

        Args:
            category: Passed by the engine; always overridden to ``"SAFETY"``.
            manifest_config: Full parsed manifest dict.
            zone_id: Optional zone name when running per-zone analytics.
                Empty string means global (no zone).
        """
        super().__init__(category="SAFETY", manifest_config=manifest_config)
        self._zone_id: str = zone_id

        safety_section = manifest_config.get("safety", {}) or {}

        # ---- class sets ------------------------------------------------
        self._person_classes = set(safety_section.get("person_classes") or ["person"])
        self._ppe_classes = set(safety_section.get("ppe_classes") or [])
        self._required_ppe = set(safety_section.get("required_ppe") or [])
        self._violation_classes = set(safety_section.get("violation_classes") or [])

        # Fall back to all ppe_classes being required when not explicitly set
        if not self._required_ppe and self._ppe_classes:
            self._required_ppe = set(self._ppe_classes)

        # ---- metrics to emit -------------------------------------------
        raw_metrics = safety_section.get("metrics") or []
        self._metrics_config: list[dict[str, str]] = [
            m for m in raw_metrics if isinstance(m, dict) and "key" in m
        ]
        if not self._metrics_config:
            # sensible default set
            default_keys: list[dict[str, str]] = [
                {"key": "total_persons", "agg_type": "sum"},
                {"key": "compliant_count", "agg_type": "sum"},
                {"key": "violation_count", "agg_type": "sum"},
                {"key": "compliance_pct", "agg_type": "mean"},
            ]
            for ppe_item in sorted(self._ppe_classes):
                default_keys.append(
                    {"key": f"{self._sanitize_key(ppe_item)}_count", "agg_type": "sum"}
                )
            self._metrics_config = default_keys

        # ---- window-level accumulators ---------------------------------
        # Unique person / violator IDs confirmed during the window.
        self._window_person_ids: set[Any] = set()
        self._window_violator_ids: set[Any] = set()
        # Unique IDs per PPE item across the window.
        self._window_ppe_ids: dict[str, set[Any]] = {
            item: set() for item in self._ppe_classes
        }
        # Per-frame compliance values for window-level mean.
        self._per_frame_compliance: list[float] = []

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize_key(label: str) -> str:
        """Convert an entity label like ``"Safety Vest"`` to ``"safety_vest"``.

        Used to build metric keys (``safety_vest_count``) from PPE entity
        names.  Also accepts already-snake entity names unchanged.
        """
        return label.strip().lower().replace(" ", "_").replace("-", "_")

    # ------------------------------------------------------------------
    # Core per-frame computation
    # ------------------------------------------------------------------

    @staticmethod
    def _count_direct_violations(
        violation_dets: list[dict[str, Any]],
        *,
        exclude_track_ids: set[Any] | None = None,
    ) -> tuple[int, set[Any]]:
        """Count violation-class boxes not already scored via a person track.

        Single-stage PPE models emit ``no_*`` labels without Person boxes.
        Unique ``track_id`` values count once; untracked boxes count individually
        (same as legacy ``ppe_compliance`` violation counting).
        """
        exclude = exclude_track_ids or set()
        seen: set[Any] = set()
        untracked = 0
        for det in violation_dets:
            tid = det.get("track_id")
            if tid is not None:
                if tid in exclude or tid in seen:
                    continue
                seen.add(tid)
            else:
                untracked += 1
        return len(seen) + untracked, seen

    def _compute_frame_metrics(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str,
    ) -> list[MetricEntry]:
        """Compute per-frame SAFETY metrics.

        ``detections`` are already entity-mapped and tracked.  Each PPE
        detection is expected to carry the ``track_id`` of the person
        it belongs to (upstream harness assigns this during dedupe).
        """
        # ── Partition detections by role ────────────────────────────
        persons = [
            d for d in detections if d.get("category", "") in self._person_classes
        ]
        ppe_dets = [d for d in detections if d.get("category", "") in self._ppe_classes]
        violation_dets = [
            d for d in detections if d.get("category", "") in self._violation_classes
        ]

        total_persons = len(persons)

        # Which track_ids wear which PPE items this frame?
        ppe_items_by_person: dict[Any, set[str]] = {}
        for det in ppe_dets:
            tid = det.get("track_id")
            if tid is None:
                continue
            ppe_items_by_person.setdefault(tid, set()).add(det.get("category", ""))

        # Track_ids flagged by direct violation-class detections.
        direct_violator_ids: set[Any] = set()
        for det in violation_dets:
            tid = det.get("track_id")
            if tid is not None:
                direct_violator_ids.add(tid)

        person_tids = {
            p.get("track_id") for p in persons if p.get("track_id") is not None
        }

        # ── Per-person compliance check ─────────────────────────────
        compliant_count = 0
        violation_count = 0
        frame_violator_ids: set[Any] = set()

        for person in persons:
            tid = person.get("track_id")
            if tid is None:
                # Un-tracked person: cannot evaluate compliance reliably
                # → treat as violator to be safe (conservative default).
                violation_count += 1
                continue

            if tid in direct_violator_ids:
                violation_count += 1
                frame_violator_ids.add(tid)
                continue

            worn = ppe_items_by_person.get(tid, set())
            if self._required_ppe and self._required_ppe.issubset(worn):
                compliant_count += 1
            else:
                violation_count += 1
                frame_violator_ids.add(tid)

        # Single-stage PPE: no Person boxes — count NO-* detections directly.
        if total_persons == 0:
            direct_count, direct_ids = self._count_direct_violations(violation_dets)
            violation_count = direct_count
            frame_violator_ids = direct_ids
        else:
            orphan_count, orphan_ids = self._count_direct_violations(
                violation_dets, exclude_track_ids=person_tids,
            )
            violation_count += orphan_count
            frame_violator_ids |= orphan_ids

        compliance_pct = (
            (compliant_count / total_persons * 100.0) if total_persons > 0 else 0.0
        )
        self._per_frame_compliance.append(compliance_pct)

        # ── Per-PPE-item counts (after dedupe upstream, so just count) ──
        ppe_counts: dict[str, int] = {item: 0 for item in self._ppe_classes}
        for det in ppe_dets:
            cat = det.get("category", "")
            if cat in ppe_counts:
                ppe_counts[cat] += 1

        # ── Accumulate window-level unique IDs from confirmed tracks ──
        for cat in self._person_classes:
            self._window_person_ids.update(self._per_cat_new.get(cat, set()))

        # Violators: frame flags + confirmed violation-class track IDs (window).
        self._window_violator_ids.update(frame_violator_ids)
        for vclass in self._violation_classes:
            self._window_violator_ids.update(self._per_cat_new.get(vclass, set()))

        for item in self._ppe_classes:
            self._window_ppe_ids.setdefault(item, set()).update(
                self._per_cat_new.get(item, set())
            )

        # ── Build MetricEntry list driven by manifest config ────────
        computed: dict[str, float] = {
            "total_persons": float(total_persons),
            "compliant_count": float(compliant_count),
            "violation_count": float(violation_count),
            "compliance_pct": float(compliance_pct),
        }
        for item, cnt in ppe_counts.items():
            computed[f"{self._sanitize_key(item)}_count"] = float(cnt)

        metrics: list[MetricEntry] = []
        for mc in self._metrics_config:
            key = mc["key"]
            value = computed.get(key)
            if value is None:
                continue
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
    # Aggregation override -- window-level uniques + compliance mean
    # ------------------------------------------------------------------

    def aggregate_1min(self) -> ProcessorAggregationOutput:
        """Aggregate buffered frames into window-level SAFETY metrics.

        Window semantics (design doc §3.7):
          - ``compliance_pct``  — mean of per-frame values.
          - ``total_persons``   — unique confirmed person track IDs.
          - ``violation_count`` — unique confirmed violator track IDs.
          - ``<item>_count``    — unique confirmed track IDs per PPE item.
          - ``compliant_count`` — ``total_persons - violation_count``
                                  (conservative window-level derivation).

        SAFETY does not emit ``tracking_stats`` (only VOLUME does).
        """
        unique_persons = len(self._window_person_ids)
        unique_violators = len(self._window_violator_ids)
        if unique_persons > 0:
            unique_compliant = max(0, unique_persons - unique_violators)
        else:
            unique_compliant = 0

        if self._per_frame_compliance:
            window_compliance_pct = sum(self._per_frame_compliance) / len(
                self._per_frame_compliance
            )
        else:
            window_compliance_pct = 0.0

        window_values: dict[str, float] = {
            "total_persons": float(unique_persons),
            "compliant_count": float(unique_compliant),
            "violation_count": float(unique_violators),
            "compliance_pct": float(window_compliance_pct),
        }
        for item, ids in self._window_ppe_ids.items():
            window_values[f"{self._sanitize_key(item)}_count"] = float(len(ids))

        aggregated_metrics: list[dict[str, Any]] = []
        for mc in self._metrics_config:
            key = mc["key"]
            if key in window_values:
                aggregated_metrics.append(
                    {
                        "key": key,
                        "data": window_values[key],
                        "agg_type": mc.get(
                            "agg_type", "mean" if key == "compliance_pct" else "sum"
                        ),
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
        """Build per-frame human text for PPE compliance."""
        total = sum(
            1 for d in detections if d.get("category", "") in self._person_classes
        )
        compliant = int(business_analytics.get("compliant_count", 0))
        violations = int(business_analytics.get("violation_count", 0))
        pct = float(business_analytics.get("compliance_pct", 0.0))

        zone_prefix = f"Zone {self._zone_id} — " if self._zone_id and self._zone_id != "global" else ""
        lines = [
            f"{zone_prefix}CURRENT FRAME:",
            f"\t- Persons detected: {total}",
            f"\t- Compliant: {compliant}",
            f"\t- Violations: {violations}",
            f"\t- Compliance: {pct:.1f}%",
            "",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Overrides -- reset accumulators
    # ------------------------------------------------------------------

    def _reset_buffers(self) -> None:
        """Reset per-window buffers including SAFETY accumulators."""
        super()._reset_buffers()
        self._window_person_ids.clear()
        self._window_violator_ids.clear()
        for ids in self._window_ppe_ids.values():
            ids.clear()
        self._per_frame_compliance.clear()

    def reset(self) -> None:
        """Full reset including SAFETY-specific state."""
        super().reset()
        self._window_person_ids.clear()
        self._window_violator_ids.clear()
        for ids in self._window_ppe_ids.values():
            ids.clear()
        self._per_frame_compliance.clear()
