"""Auto-generated stub for module: lpr_ocr_source."""
from typing import Any, Dict, List, Tuple

# Constants
OCR_SOURCE_ENV: str
OCR_SOURCE_LOCAL: str
OCR_SOURCE_UPSTREAM: str
VALID_OCR_SOURCES: Tuple[Any, ...]

# Functions
def build_upstream_ocr_analysis(use_case: Any, data: Any, config: Any) -> List[Dict[str, Any]]:
    """
    ``ocr_analysis`` built from the rows' own ``plate_text``, in detection order.
    
        Mirrors ``_analyze_ocr_in_image``'s record-per-detection contract, minus the crop. A
        smoother-carried row (``_smoothed``) keeps the previous frame's text, so it gets an
        empty record rather than a second vote for a stale read.
    """
    ...
def frame_rejection(use_case: Any, input_bytes: Any, config: Any) -> str | None:
    """
    The error to return for this frame, or ``None`` to process it.
    
        Replaces the ``input_bytes`` guard at the top of ``process``: ``local`` keeps that guard
        and its message and warning unchanged; ``upstream`` needs no frame; anything else is
        refused on every frame, since continuing as ``local`` would hide the misconfiguration.
    """
    ...
def is_upstream(config: Any) -> bool: ...
def resolve_ocr_source(config: Any) -> Tuple[str, str]:
    """
    ``(value, origin)``. The env var wins over the config whenever it is set and non-empty.
    
        The value is normalised (stripped, lower-cased) but not validated here; callers refuse
        anything outside ``VALID_OCR_SOURCES`` rather than falling back to ``local``.
    """
    ...
def validation_errors(config: Any) -> List[str]:
    """
    The ``validate()`` half of the refusal. ``frame_rejection`` is the half that bites,
        because the processing path does not call ``validate()``.
    """
    ...
