"""Auto-generated stub for module: _deps_check."""
from typing import Any, List

# Functions
def ensure_onnxruntime_gpu_available() -> List[str]:
    """
    Best-effort: make sure ORT exposes a GPU provider. Returns providers list.
    
        Never raises. Safe to call multiple times -- early-returns when a GPU
        provider is already visible.
    
        Defense-in-depth: the canonical repair runs at Python ``site``-init via
        ``_matrice_ort_bootstrap`` (installed by the ``.pth`` shipped with
        py_analytics). This function still runs at OCR package import time so
        we recover gracefully if the ``.pth`` was bypassed (e.g. ``python -S``
        or an environment where py_analytics is on ``PYTHONPATH`` but wasn't
        pip-installed).
    """
    ...
def get_ort_providers() -> List[str]:
    """
    Cached available-ORT-provider list (runs the GPU repair pre-flight once).
    
        Replaces the old module-level ``fast_plate_ocr_py38.ORT_PROVIDERS`` constant:
        callers use it to filter their preferred provider order down to what ORT can
        actually bind. Computed lazily and memoized so the repair runs at most once
        per process.
    """
    ...
def resolve_auto_providers(available: Any, model_name: Any, logger: Any) -> Any:
    """
    Pick ORT providers for ``device='auto'`` and warn on CPU fallback.
    
        Used by :class:`LicensePlateRecognizer` so the auto-mode CPU fallback is
        surfaced as a WARNING (not INFO). Exposed here so it's testable without
        pulling in onnxruntime/fast_plate_ocr at import time.
    """
    ...
