"""IdentityProcessor -- IDENTITY category processor.

Handles identity-recognition analytics for apps like License Plate
Recognition (LPR) and Face Recognition (FR).

The processor is **recognizer-agnostic**: the upstream pipeline is
expected to attach an identity string (``plate_text`` for LPR,
``face_id`` for FR) to each detection, along with optional
``identity_confidence``.  The processor then classifies each detection
into matched / unknown / blacklisted and emits per-frame and
per-window metrics matching the production ``results-agg`` Redis
stream contract.

Per-frame metrics (from ``_compute_frame_metrics``):

- **total_identifications** : plate/face detections in this frame.
- **matched_count**         : detections whose identity is on the
                              whitelist (or simply known).
- **unknown_count**         : detections without a recognized identity.
- **blacklist_matches**     : detections matching the blacklist.
- **match_confidence_avg**  : mean OCR/recognition confidence this frame.

1-minute aggregation (override of ``aggregate_1min``):

- window-level unique-track-ID counts for each classification bucket
  (so flickering plates don't inflate totals).
- match_confidence_avg is averaged across the window's confirmed
  detections.

YAML manifest ``identity`` section:

.. code-block:: yaml

    identity:
      identity_field: plate_text          # or face_id
      confidence_field: identity_confidence
      whitelist: []                        # plates/faces known & allowed
      blacklist: []                        # plates/faces flagged
      metrics:
        - {key: total_identifications, agg_type: sum}
        - {key: matched_count,         agg_type: sum}
        - {key: unknown_count,         agg_type: sum}
        - {key: blacklist_matches,     agg_type: sum}
        - {key: match_confidence_avg,  agg_type: avg}

If ``whitelist`` is empty, "matched" = "has any recognized identity".
"""
from __future__ import annotations

import logging
from typing import Any

from ..base_processor import BaseMetricProcessor, MetricEntry
from ..schemas import ProcessorAggregationOutput


logger = logging.getLogger(__name__)


class IdentityProcessor(BaseMetricProcessor):
    """IDENTITY category processor for LPR / FR analytics."""

    def __init__(
        self,
        category: str,
        manifest_config: dict[str, Any],
        zone_id: str = "",
    ) -> None:
        """Initialise IdentityProcessor.

        Args:
            category: Passed by the engine; always overridden to ``"IDENTITY"``.
            manifest_config: Full parsed manifest dict from the YAML config.
            zone_id: Optional zone name when running per-zone analytics.
                Empty string means global (no zone).
        """
        super().__init__(category="IDENTITY", manifest_config=manifest_config)
        self._zone_id: str = zone_id

        identity_section = manifest_config.get("identity", {}) or {}

        # Which detection field carries the recognized identity string?
        # For LPR this is "plate_text"; for FR it's "face_id".
        self._identity_field: str = str(
            identity_section.get("identity_field", "plate_text")
        )
        self._confidence_field: str = str(
            identity_section.get("confidence_field", "identity_confidence")
        )

        # Whitelist / blacklist (case-insensitive match on stripped string).
        def _norm_list(raw: Any) -> set[str]:
            if not raw or not isinstance(raw, list):
                return set()
            return {str(x).strip().upper() for x in raw if str(x).strip()}

        self._whitelist: set[str] = _norm_list(identity_section.get("whitelist"))
        self._blacklist: set[str] = _norm_list(identity_section.get("blacklist"))

        # Metrics declared in the manifest
        raw_metrics = identity_section.get("metrics") or []
        self._metrics_config: list[dict[str, str]] = [
            m for m in raw_metrics if isinstance(m, dict) and "key" in m
        ]
        if not self._metrics_config:
            self._metrics_config = [
                {"key": "total_identifications", "agg_type": "sum"},
                {"key": "matched_count", "agg_type": "sum"},
                {"key": "unknown_count", "agg_type": "sum"},
                {"key": "blacklist_matches", "agg_type": "sum"},
                {"key": "match_confidence_avg", "agg_type": "avg"},
            ]

        # Window-level state: track-ID → best-seen classification bucket
        # so a plate that fluctuates between "unknown" and "matched" as OCR
        # stabilizes is counted once (as matched).
        self._window_total_ids: set[Any] = set()
        self._window_matched_ids: set[Any] = set()
        self._window_unknown_ids: set[Any] = set()
        self._window_blacklist_ids: set[Any] = set()
        self._window_confidences: list[float] = []
        # Unique identity strings seen this window, per bucket.
        self._window_matched_texts: set[str] = set()
        self._window_blacklist_texts: set[str] = set()

    # ------------------------------------------------------------------
    # Classification helper
    # ------------------------------------------------------------------

    def _classify(self, text: str | None) -> str:
        """Return one of ``matched`` | ``unknown`` | ``blacklist``.

        - blacklist wins if the identity matches the blacklist.
        - matched if identity is non-empty AND (whitelist is empty OR in list).
        - unknown otherwise.
        """
        if not text:
            return "unknown"
        norm = str(text).strip().upper()
        if not norm:
            return "unknown"
        if norm in self._blacklist:
            return "blacklist"
        if self._whitelist:
            return "matched" if norm in self._whitelist else "unknown"
        # No whitelist configured: any recognized identity counts as matched.
        return "matched"

    # ------------------------------------------------------------------
    # Core per-frame computation
    # ------------------------------------------------------------------

    def _compute_frame_metrics(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str,
    ) -> list[MetricEntry]:
        """Compute per-frame IDENTITY metrics."""
        total = len(detections)
        matched = 0
        unknown = 0
        blacklist = 0
        confidences: list[float] = []

        for det in detections:
            text = det.get(self._identity_field)
            bucket = self._classify(text)
            if bucket == "matched":
                matched += 1
            elif bucket == "blacklist":
                blacklist += 1
            else:
                unknown += 1

            conf = det.get(self._confidence_field)
            if isinstance(conf, (int, float)):
                confidences.append(float(conf))

            # Window-level unique-track bookkeeping
            tid = det.get("track_id")
            if tid is not None:
                self._window_total_ids.add(tid)
                if bucket == "matched":
                    self._window_matched_ids.add(tid)
                    self._window_matched_ids.discard  # no-op, clarity
                    if text:
                        self._window_matched_texts.add(str(text).strip().upper())
                elif bucket == "blacklist":
                    self._window_blacklist_ids.add(tid)
                    if text:
                        self._window_blacklist_texts.add(str(text).strip().upper())
                else:
                    # Only count as unknown if not already promoted to matched/
                    # blacklist in an earlier frame of this window.
                    if (
                        tid not in self._window_matched_ids
                        and tid not in self._window_blacklist_ids
                    ):
                        self._window_unknown_ids.add(tid)

        # If a track id was previously unknown but is now matched/blacklist,
        # remove it from the unknown bucket (promotion as OCR stabilises).
        self._window_unknown_ids -= self._window_matched_ids
        self._window_unknown_ids -= self._window_blacklist_ids

        if confidences:
            self._window_confidences.extend(confidences)

        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        computed: dict[str, float] = {
            "total_identifications": float(total),
            "matched_count": float(matched),
            "unknown_count": float(unknown),
            "blacklist_matches": float(blacklist),
            "match_confidence_avg": avg_conf,
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
    # Aggregation override -- window-level unique counts
    # ------------------------------------------------------------------

    def aggregate_1min(self) -> ProcessorAggregationOutput:
        """Aggregate buffered frames into window-level IDENTITY metrics.

        Emits window-unique counts based on confirmed track IDs rather
        than summed frame counts, so the same plate visible for 100
        frames counts as 1 identification.
        """
        total_unique = len(self._window_total_ids)
        matched_unique = len(self._window_matched_ids)
        blacklist_unique = len(self._window_blacklist_ids)
        unknown_unique = len(self._window_unknown_ids)

        window_avg_conf = (
            sum(self._window_confidences) / len(self._window_confidences)
            if self._window_confidences
            else 0.0
        )

        window_values: dict[str, float] = {
            "total_identifications": float(total_unique),
            "matched_count": float(matched_unique),
            "unknown_count": float(unknown_unique),
            "blacklist_matches": float(blacklist_unique),
            "match_confidence_avg": window_avg_conf,
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

        # Emit the set of recognised plate/face strings seen this window
        # as a side-channel so UI/backend can surface them.
        tracking_stats: dict[str, Any] = {
            "matched_identities": sorted(self._window_matched_texts),
            "blacklist_identities": sorted(self._window_blacklist_texts),
        }

        result = ProcessorAggregationOutput(
            metrics=aggregated_metrics,
            tracking_stats=tracking_stats,
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
        total = len(detections)
        matched = 0
        unknown = 0
        blacklist = 0
        for det in detections:
            bucket = self._classify(det.get(self._identity_field))
            if bucket == "matched":
                matched += 1
            elif bucket == "blacklist":
                blacklist += 1
            else:
                unknown += 1

        zone_prefix = (
            f"Zone {self._zone_id} — "
            if self._zone_id and self._zone_id != "global"
            else ""
        )
        lines = [
            f"{zone_prefix}CURRENT FRAME:",
            f"\t- Total identifications: {total}",
            f"\t- Matched: {matched}",
            f"\t- Unknown: {unknown}",
            f"\t- Blacklist matches: {blacklist}",
            "",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Overrides -- reset accumulators
    # ------------------------------------------------------------------

    def _reset_buffers(self) -> None:
        super()._reset_buffers()
        self._window_total_ids.clear()
        self._window_matched_ids.clear()
        self._window_unknown_ids.clear()
        self._window_blacklist_ids.clear()
        self._window_confidences.clear()
        self._window_matched_texts.clear()
        self._window_blacklist_texts.clear()

    def reset(self) -> None:
        super().reset()
        self._window_total_ids.clear()
        self._window_matched_ids.clear()
        self._window_unknown_ids.clear()
        self._window_blacklist_ids.clear()
        self._window_confidences.clear()
        self._window_matched_texts.clear()
        self._window_blacklist_texts.clear()
