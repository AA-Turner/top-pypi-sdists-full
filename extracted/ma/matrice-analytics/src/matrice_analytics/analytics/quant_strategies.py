"""Pluggable strategies for computing ``incident_quant`` from raw detections.

Each strategy function takes a list of detection dicts and a
:class:`QuantStrategyConfig` and returns ``(incident_quant, event_confidence)``.

``incident_quant`` is a 0-100 percentage used by the severity calculator
to determine the current severity level.  ``event_confidence`` is the raw
max confidence value (0-1) carried through to published events.

To add a new strategy, define a function matching the
``(detections, config) -> (float, float)`` signature and register it in
the ``_STRATEGIES`` dispatch table.
"""
from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from .schemas import QuantStrategyConfig


logger = logging.getLogger(__name__)

QuantFn = Callable[[list[dict[str, Any]], QuantStrategyConfig], tuple[float, float]]


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------


def _max_confidence(
    detections: list[dict[str, Any]],
    _config: QuantStrategyConfig,
) -> tuple[float, float]:
    """``quant = max(confidence) * 100``.

    Suitable for single-class detectors (weapon, fall, etc.) where the
    confidence score directly reflects incident severity.
    """
    max_conf = 0.0
    for det in detections:
        conf = float(det.get("confidence", det.get("score", 0.0)))
        if conf > max_conf:
            max_conf = conf
    return min(100.0, max_conf * 100.0), max_conf


def _area_ratio(
    detections: list[dict[str, Any]],
    config: QuantStrategyConfig,
) -> tuple[float, float]:
    """``quant = (total_bbox_area / threshold_area) * 100``, capped at 100.

    Used by fire/smoke detection where the *extent* of the hazard in the
    frame is more important than any single detection's confidence.
    """
    total_area = 0.0
    max_conf = 0.0
    for det in detections:
        conf = float(det.get("confidence", det.get("score", 0.0)))
        if conf > max_conf:
            max_conf = conf
        bbox = det.get("bounding_box") or det.get("bbox")
        if isinstance(bbox, dict):
            xmin = bbox.get("xmin", bbox.get("x1"))
            ymin = bbox.get("ymin", bbox.get("y1"))
            xmax = bbox.get("xmax", bbox.get("x2"))
            ymax = bbox.get("ymax", bbox.get("y2"))
            if None not in (xmin, ymin, xmax, ymax):
                w = float(xmax) - float(xmin)
                h = float(ymax) - float(ymin)
                if w > 0 and h > 0:
                    total_area += w * h

    if config.threshold_area <= 0:
        return 0.0, max_conf
    return min(100.0, (total_area / config.threshold_area) * 100.0), max_conf


def _count_based(
    detections: list[dict[str, Any]],
    config: QuantStrategyConfig,
) -> tuple[float, float]:
    """``quant = (len(detections) / count_threshold) * 100``, capped at 100.

    Useful for incidents where the *number* of simultaneous detections
    determines severity (e.g. crowd violence, mass loitering).
    """
    max_conf = 0.0
    for det in detections:
        conf = float(det.get("confidence", det.get("score", 0.0)))
        if conf > max_conf:
            max_conf = conf

    threshold = max(1, config.count_threshold)
    quant = min(100.0, (len(detections) / threshold) * 100.0)
    return quant, max_conf


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

_STRATEGIES: dict[str, QuantFn] = {
    "max_confidence": _max_confidence,
    "area_ratio": _area_ratio,
    "count_based": _count_based,
}


def compute_quant(
    detections: list[dict[str, Any]],
    config: QuantStrategyConfig,
) -> tuple[float, float]:
    """Compute ``(incident_quant, event_confidence)`` using the configured strategy.

    Falls back to ``max_confidence`` if the strategy name is not recognised.

    Args:
        detections: Filtered detection dicts for this frame.
        config: Strategy selection and parameters from the YAML manifest.

    Returns:
        ``(incident_quant, event_confidence)`` tuple.
    """
    if not detections:
        return 0.0, 0.0

    fn = _STRATEGIES.get(config.strategy)
    if fn is None:
        logger.warning(
            "Unknown quant strategy '%s', falling back to max_confidence",
            config.strategy,
        )
        fn = _max_confidence

    return fn(detections, config)
