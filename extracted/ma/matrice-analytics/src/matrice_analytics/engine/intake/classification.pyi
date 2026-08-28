"""Auto-generated stub for module: classification."""
from typing import Any

# Functions
def whole_frame_detections(raw: Any) -> list[dict[str, Any]]:
    """
    Normalize one frame's whole-frame/whole-clip classification output to detection dicts.
    
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
    ...
