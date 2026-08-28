"""Auto-generated stub for module: _ocr_venv_bootstrap."""
from typing import Any, Optional

# Constants
WheelSpec: Any
logger: Any

# Functions
def ensure_ocr_venv(model_name: str = _DEFAULT_MODEL, timeout: float = 1800.0) -> Optional[str]:
    """
    Return a healthy isolated-OCR-venv python, creating/repairing it if needed.
    
        Fast path (no lock): an existing venv that passes the health probe is
        returned immediately. Slow path: acquire a cross-process lock, re-probe (a
        sibling may have just built it), then create the venv and install deps.
        Never raises -- returns ``None`` on any failure so the caller falls back to
        in-process OCR.
    """
    ...
