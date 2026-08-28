"""Auto-generated stub for module: _ocr_ipc."""
from typing import Any, Callable, Dict, List, Optional

# Constants
CTRL_ERROR: str
CTRL_PONG: str
CTRL_READY: str
TAG_CONTROL: Any
TAG_REQUEST: Any
TAG_RESPONSE: Any

# Functions
def decode_request_array(frame: Any) -> Any.Any:
    """
    Reconstruct the image array from a 'run' request frame.
    """
    ...
def decode_request_arrays(frame: Any) -> 'List[Any.Any]':
    """
    Reconstruct the crop list from a 'run_batch' request frame.
    
        The inverse of :func:`pack_batch_request`: walk the per-crop shapes, slicing
        the concatenated payload at each crop's byte length.
    """
    ...
def decode_response_confs(frame: Any) -> Optional[Any.Any]:
    """
    Reconstruct the confidence array from a response frame (or None).
    """
    ...
def normalize_run_result(result: Any) -> Any:
    """
    Normalize ``LicensePlateRecognizer.run(return_confidence=True)`` output to
        ``(texts, confs)`` across upstream versions.
    
        Two upstream return shapes exist and we must support both so a routine
        ``pip install`` of a newer ``fast_plate_ocr`` never breaks OCR again:
    
        * ``<= 1.0.x`` returns a ``(texts, confs)`` tuple where ``confs`` is an
          ``(N, num_chars)`` ndarray of per-character probabilities.
        * ``>= 1.1.0`` returns ``list[PlatePrediction]`` where each item exposes
          ``.plate`` (str) and ``.char_probs`` (ndarray | None).
    
        Returns ``(texts: list[str], confs: np.ndarray | None)``. ``confs`` is the
        stacked ``(N, num_chars)`` array when every prediction carries probabilities,
        else ``None``.
    """
    ...
def pack_batch_request(request_id: int, arrays: 'Any[Any.Any]', return_confidence: bool = True) -> Any:
    """
    Pack a ``run_batch`` request: several crops in one round trip.
    
        Crops from one frame have different shapes, so they cannot be stacked into a
        single array -- ``np.asarray`` on a ragged list raises. Instead each crop is
        made contiguous and its bytes concatenated, with a per-crop shape in the
        header; :func:`decode_request_arrays` slices them back apart. One dtype is
        used for all of them, taken from the first crop, because they come from the
        same decoded frame.
    
        This exists so the OCR model sees one call for N crops. It does not change
        what the model is given: each crop still arrives as its own array, so
        preprocessing stays inside the recognizer and read quality is unaffected.
    """
    ...
def pack_control(obj: Dict[str, Any]) -> Any: ...
def pack_request(request_id: int, array: Optional[Any.Any], return_confidence: bool = True, op: str = 'run') -> Any:
    """
    Pack a ``run`` (with image) or ``ping`` (no image) request.
    """
    ...
def pack_response_error(request_id: int, error: str) -> Any: ...
def pack_response_ok(request_id: int, texts: list, confs: Optional[Any.Any]) -> Any: ...
def read_exact_from_stream(stream: Any, n: int) -> Any:
    """
    Blocking ``read_exact`` for a binary stream (used by the worker).
    """
    ...
def read_frame(read_exact: Callable[[int], Any]) -> Any:
    """
    Read and decode one frame using ``read_exact(n) -> bytes``.
    
        ``read_exact`` must return exactly ``n`` bytes or raise ``EOFError`` /
        ``TimeoutError`` (the worker uses a blocking reader, the client a
        deadline-aware one).
    """
    ...
def write_frame(stream: Any, frame_bytes: Any) -> None:
    """
    Write a packed frame to a binary stream and flush.
    """
    ...

# Classes
class Frame:
    # A decoded protocol frame.

    ...
