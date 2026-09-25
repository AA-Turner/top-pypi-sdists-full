"""Where the license-plate use case gets its plate text: its own OCR, or the upstream row.

``local`` (the default) is the use case as it has always run: it needs the frame, crops
each plate box and runs the OCR model itself. ``upstream`` is for a chain whose OCR node
already read the plate: each row arrives carrying ``plate_text`` and ``text_confidence``
(the ``text0`` port's legacy rows), so the use case needs no frame and never loads a model.

Upstream reads are not trusted more than local ones. Each goes through the same
``_interpret_ocr_result`` gates (confidence floor, cleaning, minimum length, ``ocr_mode``),
the same stability cache, and ``_update_detections_with_ocr`` exactly as a local read
would, so a rejected read clears the detection's ``plate_text`` the same way.

This lives outside ``license_plate_monitoring.py`` because ``process`` is far past the
complexity cap: the whole switch reaches it through one existing guard line and one call
in ``_analyze_ocr_in_media``.
"""

from __future__ import annotations

import math
import os
import time
from typing import Any, Dict, List, Tuple

OCR_SOURCE_ENV = "MATRICE_LPR_OCR_SOURCE"
OCR_SOURCE_LOCAL = "local"
OCR_SOURCE_UPSTREAM = "upstream"
VALID_OCR_SOURCES = (OCR_SOURCE_LOCAL, OCR_SOURCE_UPSTREAM)

# Both conditions below persist for the life of a deployment, so they are repeated at this
# interval rather than logged once -- an operator reading a log tail hours after startup
# must still see them -- but never per frame.
_WARN_INTERVAL_S = 60.0

_FRAME_REQUIRED_ERROR = "input_bytes (video/image) is required for license plate monitoring"


def resolve_ocr_source(config: Any) -> Tuple[str, str]:
    """``(value, origin)``. The env var wins over the config whenever it is set and non-empty.

    The value is normalised (stripped, lower-cased) but not validated here; callers refuse
    anything outside ``VALID_OCR_SOURCES`` rather than falling back to ``local``.
    """
    env_value = os.environ.get(OCR_SOURCE_ENV, "").strip()
    if env_value:
        return env_value.lower(), f"env {OCR_SOURCE_ENV}"
    configured = getattr(config, "ocr_source", OCR_SOURCE_LOCAL) or OCR_SOURCE_LOCAL
    return str(configured).strip().lower(), "config"


def _invalid_message(value: str) -> str:
    return f"ocr_source '{value}' is invalid; expected one of: {', '.join(VALID_OCR_SOURCES)}"


def validation_errors(config: Any) -> List[str]:
    """The ``validate()`` half of the refusal. ``frame_rejection`` is the half that bites,
    because the processing path does not call ``validate()``."""
    value, _origin = resolve_ocr_source(config)
    return [] if value in VALID_OCR_SOURCES else [_invalid_message(value)]


def is_upstream(config: Any) -> bool:
    return resolve_ocr_source(config)[0] == OCR_SOURCE_UPSTREAM


def _state(use_case: Any) -> Dict[str, Any]:
    # Kept on the instance, not module-global: several use cases can share a process. Built
    # lazily because some tests construct the use case without running ``__init__``.
    state = use_case.__dict__.get("_ocr_source_state")
    if state is None:
        state = {"announced": set(), "warned_at": {}}
        use_case.__dict__["_ocr_source_state"] = state
    return state


def _due(use_case: Any, key: str) -> bool:
    warned_at = _state(use_case)["warned_at"]
    now = time.monotonic()
    if key in warned_at and now - warned_at[key] < _WARN_INTERVAL_S:
        return False
    warned_at[key] = now
    return True


def frame_rejection(use_case: Any, input_bytes: Any, config: Any) -> str | None:
    """The error to return for this frame, or ``None`` to process it.

    Replaces the ``input_bytes`` guard at the top of ``process``: ``local`` keeps that guard
    and its message and warning unchanged; ``upstream`` needs no frame; anything else is
    refused on every frame, since continuing as ``local`` would hide the misconfiguration.
    """
    value, origin = resolve_ocr_source(config)
    if value not in VALID_OCR_SOURCES:
        message = _invalid_message(value)
        if _due(use_case, "invalid"):
            use_case.logger.error(
                "[LPR] %s (from %s) -- every frame is rejected until it is fixed", message, origin
            )
        return message
    if value == OCR_SOURCE_UPSTREAM:
        # Once per origin, at WARNING: the deploy containers run this logger at WARNING, so
        # an INFO line would never show that the switch took effect.
        announced = _state(use_case)["announced"]
        if origin not in announced:
            announced.add(origin)
            use_case.logger.warning(
                "[LPR] ocr_source=upstream (from %s); the local OCR model will not be loaded",
                origin,
            )
        return None
    if input_bytes is None or (hasattr(input_bytes, "__len__") and len(input_bytes) == 0):
        use_case._warn_no_frame_pixels(input_bytes)
        return _FRAME_REQUIRED_ERROR
    return None


def _new_record(detection: Dict[str, Any], index: int, cached: bool) -> Dict[str, Any]:
    """The record ``_analyze_ocr_in_image`` builds per detection, before any read lands."""
    return {
        "frame_id": "0",
        "timestamp": 0.0,
        "category": detection.get("category", ""),
        "confidence": round(detection.get("confidence", 0.0), 3),
        "plate_text": None,
        "bbox": detection.get("bounding_box", detection.get("bbox")),
        "detection_id": detection.get("id", f"det_{index}"),
        "track_id": detection.get("track_id"),
        "ocr_confidence": 0.0,
        "reject_reason": None,
        "raw_text": "",
        "ocr_ms": 0.0,
        "ocr_cached": cached,
    }


def _gate_upstream_read(use_case: Any, detection: Dict[str, Any]) -> Dict[str, Any]:
    """Run one upstream read through the local gates.

    ``_interpret_ocr_result`` averages per-character confidences over the non-pad positions
    of ``raw_text``. Handing it the pad-stripped text and the one scalar the row carries
    makes that average exactly ``text_confidence``. A non-finite confidence is treated as
    0.0: ``NaN < threshold`` is False, so it would otherwise pass the floor.
    """
    text = str(detection.get("plate_text") or "")
    confidence = float(detection.get("text_confidence") or 0.0)
    if not math.isfinite(confidence):
        confidence = 0.0
    result = use_case._interpret_ocr_result(text.replace("_", ""), [confidence])
    result["raw_text"] = text
    return result


def build_upstream_ocr_analysis(use_case: Any, data: Any, config: Any) -> List[Dict[str, Any]]:
    """``ocr_analysis`` built from the rows' own ``plate_text``, in detection order.

    Mirrors ``_analyze_ocr_in_image``'s record-per-detection contract, minus the crop. A
    smoother-carried row (``_smoothed``) keeps the previous frame's text, so it gets an
    empty record rather than a second vote for a stale read.
    """
    ocr_analysis: List[Dict[str, Any]] = []
    rows = missing = 0
    for detection in use_case._get_frame_detections(data, "0"):
        if detection.get("confidence", 1.0) < config.confidence_threshold:
            continue
        if not detection.get("bounding_box", detection.get("bbox")):
            continue
        if detection.get("_smoothed"):
            ocr_analysis.append(_new_record(detection, len(ocr_analysis), cached=False))
            continue
        rows += 1
        has_text = "plate_text" in detection
        missing += 0 if has_text else 1
        cached_result = use_case._cached_stable_ocr_result(detection.get("track_id"))
        record = _new_record(detection, len(ocr_analysis), cached=cached_result is not None)
        ocr_analysis.append(record)
        if cached_result is not None:
            use_case._apply_ocr_to_record(record, cached_result, 0.0, 0, 0, cached=True)
        elif has_text:
            read = _gate_upstream_read(use_case, detection)
            use_case._apply_ocr_to_record(record, read, 0.0, 0, 0, cached=False)
    if missing and _due(use_case, "missing_text"):
        use_case.logger.warning(
            "[LPR] ocr_source=upstream but %d of %d rows carry no plate_text; "
            "check that the PP's upstream_port is text0",
            missing,
            rows,
        )
    return ocr_analysis
