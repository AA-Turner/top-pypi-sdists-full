"""Whole-frame / whole-clip classifiers -- the one raw shape ``Session`` cannot take directly.

Normative context: ``ml-applications/guidelines/FIELD_REFERENCE.md`` §5 and §10 assume every
detection carries a bounding box (contract Section 4, boxes normalized 0-1).
:func:`~matrice_analytics.engine.runtime.session._to_detection` enforces that at intake --
``"detection carries no bounding box"`` is a :class:`~matrice_analytics.engine.runtime.session.
SessionError`, not a warning -- because a box-less detection is silently mis-handled everywhere
downstream (``incident_quantise._total_area``, the overlay renderer, MPR1 storage).

A whole-frame classifier (X3D-style action/event classification: "accident" vs "normal", and by
the same shape "fall" vs "not falling", "drowsy" vs "alert", ...) has no box at all -- the model
looks at the whole frame or a short clip and returns one label for it.  Its wire shape, proven in
production by ``post_processing/usecases/accident_detection.py``, is a dict of ``TypedOutput``-like
entries::

    {
        "classification0": {
            "type": "classification",
            "data": {
                "predictions": [{"class_id": 0, "category": "class_0", "confidence": 0.68}, ...],
                "top_prediction": {"class_id": 0, "category": "class_0", "confidence": 0.68},
            },
        },
    }

Only ``top_prediction`` matters (``predictions``/top-k are not consulted, matching the legacy
normalizer); ``top_prediction.category`` is frequently a generic placeholder (``"class_0"``), so
``class_id`` is what should resolve to a real label -- via ``model.index_to_category``, the same
mechanism every other app already uses for an index-only producer (``Session._EntityMapper``).

**What this module does, and no more**: turn that payload into the flat ``category`` /
``class_id`` / ``confidence`` / ``bounding_box`` dicts :func:`~matrice_analytics.engine.runtime.
session._to_detection` already reads (``_CATEGORY_KEYS``, ``_INDEX_KEYS``, ``_CONFIDENCE_KEYS``,
``_BOX_KEYS``) -- with the box synthesised as the full frame, ``[0, 0, 1, 1]``, since a whole-frame
classifier has nothing else to report. Everything after that boundary -- entity remap, ``detect``,
``track``, ``incident_quantise``, ``state_machine`` -- is then unmodified, ordinary, config-only
pipeline: from the manifest's point of view this is just another bounding-box app whose box happens
to always be the full frame. No primitive in ``engine/primitives`` needs to know this producer
exists.

**Why a full-frame box, and why it is safe to hand to ``track``.**  ``incident_quantise.area_ratio``
would read a whole-frame box as "the hazard fills 100% of the frame" every time, which is wrong for
a classifier -- so an app built on this normalizer should quantise by ``max_confidence`` or
``count_based``, never ``area_ratio`` (see the app's own manifest for the reasoning; this module has
no opinion on strategy). A **stationary, identical** box tracks trivially under every method in
``TrackConfig.method`` (IoU-based association is *easiest* on a non-moving target, not hardest), so
composing ``track`` + ``unique_count`` on top of this normalizer is a supported way to turn "this
frame classified positive" into "how many separate positive *episodes*" -- one continuous track per
unbroken run of positive frames, a new track id after a gap longer than ``track.max_time_lost``.

**Where this runs.**  Nothing in :mod:`matrice_analytics.engine` reads raw model output (``09``
architecture note, session.py's own docstring: "Nothing here imports post_processing"). This
function is the boundary piece a deployment's worker calls *before*
:meth:`~matrice_analytics.engine.runtime.session.Session.process_frame`::

    detections = whole_frame_detections(raw_model_output)
    outcome = session.process_frame(detections, frame_ts=...)

It is deliberately not a registered ``@register`` primitive: primitives run *after* intake, over
already-boxed :class:`~matrice_analytics.engine.primitives.base.PipelineDetection` objects, and by
the time a primitive would see this producer's output the box already has to exist. This is the
one thing that has to happen first.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final

__all__ = ["whole_frame_detections"]

#: The synthetic box every whole-frame classification gets. Normalized 0-1, per contract Section 4
#: -- the whole frame, because a classifier that saw the whole frame has nothing narrower to report.
_FULL_FRAME_BOX: Final[dict[str, float]] = {"xmin": 0.0, "ymin": 0.0, "xmax": 1.0, "ymax": 1.0}


def whole_frame_detections(raw: Any) -> list[dict[str, Any]]:
    """Normalize one frame's whole-frame/whole-clip classification output to detection dicts.

    Accepts, in order of what is tried:

    * a mapping of named ``TypedOutput``-like entries (``{"classification0": {...}, ...}``) --
      the real production shape, one entry per model head;
    * a single such entry;
    * a plain list of entries;
    * a flattened ``{"label": ..., "confidence": ...}`` (or ``"category"``/``"score"``) shape,
      for callers that already unwrapped the model's own envelope.

    Each entry's payload is read off a ``"data"`` key (or a ``.data`` attribute, for callers that
    hand in an object rather than a dict) and only ``top_prediction`` is consulted -- the full
    ``predictions`` / top-k list is not, matching the proven behaviour of
    ``post_processing/usecases/accident_detection.py._normalize_x3d_results`` this module ports.

    Args:
        raw: This frame's raw classification output, in any of the shapes above.

    Returns:
        Zero or one detection dict per entry found, each shaped
        ``{"category": str, "class_id": int | None, "confidence": float, "bounding_box": {...}}``
        -- exactly the spellings :func:`~matrice_analytics.engine.runtime.session._to_detection`
        already reads, with a synthetic full-frame box. Never fabricates an entry for a payload
        with no usable label: an empty list is the correct reading of "nothing classified this
        frame", the same as a quiet frame from any bounding-box producer.
    """
    return [detection for detection in (_extract(entry) for entry in _entries(raw)) if detection is not None]


def _entries(raw: Any) -> Sequence[Any]:
    """Split ``raw`` into individual classification entries, whatever shape it arrived in."""
    if raw is None:
        return ()
    if isinstance(raw, Mapping):
        # A single flattened {"label"/"category": ..., "confidence": ...} entry is itself the
        # entry, not a dict of entries to iterate -- and so is a single {"data": {...}} envelope.
        if "label" in raw or "category" in raw or isinstance(raw.get("data"), Mapping):
            return (raw,)
        return tuple(raw.values())
    if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
        return tuple(raw)
    return (raw,)


def _extract(entry: Any) -> dict[str, Any] | None:
    """One entry -> one detection dict, or ``None`` when it carries no usable label."""
    payload: Any = entry.data if hasattr(entry, "data") else entry
    if isinstance(payload, Mapping) and isinstance(payload.get("data"), Mapping):
        payload = payload["data"]
    if not isinstance(payload, Mapping):
        return None

    class_id: int | None = None
    category: str | None = None
    confidence: float = 0.0

    top_prediction = payload.get("top_prediction")
    if isinstance(top_prediction, Mapping):
        raw_id = top_prediction.get("class_id")
        if isinstance(raw_id, int) and not isinstance(raw_id, bool):
            class_id = raw_id
        else:
            # No class_id to resolve a real label from index_to_category, so the
            # placeholder is all there is -- use it rather than return nothing.
            raw_category = top_prediction.get("category")
            if isinstance(raw_category, str) and raw_category.strip():
                category = raw_category.strip()
        confidence = _as_float(top_prediction.get("confidence"))
    else:
        # Flattened fallback: {"label"/"category": ..., "confidence"/"score": ...}.
        raw_category = payload.get("label", payload.get("category"))
        if isinstance(raw_category, str) and raw_category.strip():
            category = raw_category.strip()
        raw_id = payload.get("class_id")
        if isinstance(raw_id, int) and not isinstance(raw_id, bool):
            class_id = raw_id
        confidence = _as_float(payload.get("confidence", payload.get("score")))

    if class_id is None and category is None:
        return None

    return {
        "category": category or "",
        "class_id": class_id,
        "confidence": confidence,
        "bounding_box": dict(_FULL_FRAME_BOX),
    }


def _as_float(value: Any) -> float:
    """Read a confidence-shaped value as a float, treating anything unusable as ``0.0``."""
    if isinstance(value, bool):
        return float(int(value))
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0
