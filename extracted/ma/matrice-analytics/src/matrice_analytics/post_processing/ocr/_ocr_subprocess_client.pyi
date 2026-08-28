"""Auto-generated stub for module: _ocr_subprocess_client."""
from typing import Any, List, Optional, Tuple

from . import _ocr_ipc
from ._ocr_venv_bootstrap import ensure_ocr_venv

# Constants
logger: Any

# Functions
def get_shared_ocr_client(model_name: str, providers: Optional[Any[str]] = None) -> Any:
    """
    Return a process-wide singleton client keyed by (model, providers).
    
        The plate model is tiny, so all post-processing threads in a worker process
        share one subprocess rather than spawning one per camera/thread.
    """
    ...

# Classes
class OcrSubprocessClient:
    # Manages one long-lived OCR worker subprocess (per parent process).

    def __init__(self: Any, model_name: str = 'cct-s-v1-global-model', providers: Optional[Any[str]] = None, python_exe: Optional[str] = None, ready_timeout: Optional[float] = None, request_timeout: float = 15.0, startup_retry_delays: Any[float] = (1.0, 3.0, 5.0), reinit_cooldown: float = 30.0, startup_budget_s: Optional[float] = None) -> None: ...

    def close(self: Any) -> None: ...

    def is_available(self: Any) -> bool: ...

    def is_permanently_unavailable(self: Any) -> bool:
        """
        True if the GPU OCR path failed for a non-recoverable reason.
        """
        ...

    def run(self: Any, source: Any, return_confidence: bool = True) -> 'Tuple[List[str], Any.Any] | List[str]':
        """
        OCR one image, or a list of crops in one round trip.
        
                Mirrors ``LicensePlateRecognizer.run``. ``source`` is an array-like for a
                single image, or a list/tuple of arrays -- which is sent as one ``run_batch``
                request rather than N separate ones, collapsing N IPC round trips into one.
                Result ``i`` belongs to ``source[i]``.
        
                Raises :class:`OcrSubprocessUnavailable` if the worker dies and cannot
                be recovered. A per-request failure raises a plain ``RuntimeError``
                (the worker stays up).
        """
        ...

    def start(self: Any) -> bool:
        """
        Bring up the worker with retries. Returns True if GPU-ready.
        
                A *permanent* failure (missing onnxruntime / interpreter) sets
                ``_permanently_unavailable`` so we never retry. A *transient* failure
                (model-download 5xx, timeout, network blip) is left recoverable: the
                full retry sequence is rate-limited by ``reinit_cooldown`` so a later
                call -- e.g. once the model is cached -- can bring OCR up without
                stalling every request in between.
        
                The whole sequence -- every attempt and every inter-attempt sleep -- is
                bounded by ``startup_budget_s``, because this runs inline on the frame that
                first needs OCR. Before ANA-21 only each individual attempt was bounded, so
                the frame could wait 4 * ready_timeout + the sleeps.
        """
        ...

class OcrSubprocessUnavailable:
    # Raised when the GPU OCR subprocess cannot serve requests.
    #
    #     Signals the caller to fall back to the in-process CPU OCR path.

    ...
