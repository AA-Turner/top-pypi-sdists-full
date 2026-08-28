"""Stub file for post_processing.ocr directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from . import _ocr_ipc
from ._ocr_venv_bootstrap import ensure_ocr_venv

# Constants
CTRL_ERROR: str = ...  # From _ocr_ipc
CTRL_PONG: str = ...  # From _ocr_ipc
CTRL_READY: str = ...  # From _ocr_ipc
TAG_CONTROL: Any = ...  # From _ocr_ipc
TAG_REQUEST: Any = ...  # From _ocr_ipc
TAG_RESPONSE: Any = ...  # From _ocr_ipc
logger: Any = ...  # From _ocr_subprocess_client
WheelSpec: Any = ...  # From _ocr_venv_bootstrap
logger: Any = ...  # From _ocr_venv_bootstrap

# Functions
# From _deps_check
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

# From _deps_check
def get_ort_providers() -> List[str]:
    """
    Cached available-ORT-provider list (runs the GPU repair pre-flight once).
    
        Replaces the old module-level ``fast_plate_ocr_py38.ORT_PROVIDERS`` constant:
        callers use it to filter their preferred provider order down to what ORT can
        actually bind. Computed lazily and memoized so the repair runs at most once
        per process.
    """
    ...

# From _deps_check
def resolve_auto_providers(available: Any, model_name: Any, logger: Any) -> Any:
    """
    Pick ORT providers for ``device='auto'`` and warn on CPU fallback.
    
        Used by :class:`LicensePlateRecognizer` so the auto-mode CPU fallback is
        surfaced as a WARNING (not INFO). Exposed here so it's testable without
        pulling in onnxruntime/fast_plate_ocr at import time.
    """
    ...

# From _ocr_ipc
def decode_request_array(frame: Any) -> Any.Any:
    """
    Reconstruct the image array from a 'run' request frame.
    """
    ...

# From _ocr_ipc
def decode_request_arrays(frame: Any) -> 'List[Any.Any]':
    """
    Reconstruct the crop list from a 'run_batch' request frame.
    
        The inverse of :func:`pack_batch_request`: walk the per-crop shapes, slicing
        the concatenated payload at each crop's byte length.
    """
    ...

# From _ocr_ipc
def decode_response_confs(frame: Any) -> Optional[Any.Any]:
    """
    Reconstruct the confidence array from a response frame (or None).
    """
    ...

# From _ocr_ipc
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

# From _ocr_ipc
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

# From _ocr_ipc
def pack_control(obj: Dict[str, Any]) -> Any: ...

# From _ocr_ipc
def pack_request(request_id: int, array: Optional[Any.Any], return_confidence: bool = True, op: str = 'run') -> Any:
    """
    Pack a ``run`` (with image) or ``ping`` (no image) request.
    """
    ...

# From _ocr_ipc
def pack_response_error(request_id: int, error: str) -> Any: ...

# From _ocr_ipc
def pack_response_ok(request_id: int, texts: list, confs: Optional[Any.Any]) -> Any: ...

# From _ocr_ipc
def read_exact_from_stream(stream: Any, n: int) -> Any:
    """
    Blocking ``read_exact`` for a binary stream (used by the worker).
    """
    ...

# From _ocr_ipc
def read_frame(read_exact: Callable[[int], Any]) -> Any:
    """
    Read and decode one frame using ``read_exact(n) -> bytes``.
    
        ``read_exact`` must return exactly ``n`` bytes or raise ``EOFError`` /
        ``TimeoutError`` (the worker uses a blocking reader, the client a
        deadline-aware one).
    """
    ...

# From _ocr_ipc
def write_frame(stream: Any, frame_bytes: Any) -> None:
    """
    Write a packed frame to a binary stream and flush.
    """
    ...

# From _ocr_subprocess_client
def get_shared_ocr_client(model_name: str, providers: Optional[Any[str]] = None) -> Any:
    """
    Return a process-wide singleton client keyed by (model, providers).
    
        The plate model is tiny, so all post-processing threads in a worker process
        share one subprocess rather than spawning one per camera/thread.
    """
    ...

# From _ocr_subprocess_worker
def main(argv: Any = None) -> int: ...

# From _ocr_venv_bootstrap
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

# Classes
# From _ocr_ipc
class Frame:
    # A decoded protocol frame.

    ...

# From _ocr_subprocess_client
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


# From _ocr_subprocess_client
class OcrSubprocessUnavailable:
    # Raised when the GPU OCR subprocess cannot serve requests.
    #
    #     Signals the caller to fall back to the in-process CPU OCR path.

    ...

# From easyocr_extractor
class EasyOCRExtractor:
    def __init__(self: Any, lang: Any = ['en', 'hi', 'ar'], gpu: Any = False, model_storage_directory: Any = None, download_enabled: Any = True, detector: Any = True, recognizer: Any = True, verbose: Any = False) -> None:
        """
        Initializes the EasyOCR text extractor with optimized parameters.
        
        Args:
            lang (str or list): Language(s) to be used by EasyOCR. Default is ['en', 'hi', 'ar'].
            gpu (bool): Enable GPU acceleration if available. Default is True.
            model_storage_directory (str): Custom path to store models. Default is None.
            download_enabled (bool): Allow downloading models if not found. Default is True.
            detector (bool): Load text detection model. Default is True.
            recognizer (bool): Load text recognition model. Default is True.
            verbose (bool): Enable verbose output (e.g., progress bars). Default is False.
        """
        ...

    def detect_text_regions(self: Any, image_np: Any, min_size: Any = 10, text_threshold: Any = 0.7, low_text: Any = 0.4, link_threshold: Any = 0.4, canvas_size: Any = 2560, mag_ratio: Any = 1.0, slope_ths: Any = 0.1, ycenter_ths: Any = 0.5, height_ths: Any = 0.5, width_ths: Any = 0.5, add_margin: Any = 0.1, optimal_num_chars: Any = None) -> Any:
        """
        Detects text regions in the image without performing recognition.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            min_size (int): Filter text boxes smaller than this pixel size.
            text_threshold (float): Text confidence threshold.
            low_text (float): Text low-bound score.
            link_threshold (float): Link confidence threshold.
            canvas_size (int): Maximum image size before resizing.
            mag_ratio (float): Image magnification ratio.
            slope_ths (float): Maximum slope for merging boxes.
            ycenter_ths (float): Maximum y-center shift for merging boxes.
            height_ths (float): Maximum height difference for merging boxes.
            width_ths (float): Maximum width for horizontal merging.
            add_margin (float): Margin to add around text boxes.
            optimal_num_chars (int): Prioritize boxes with this estimated character count.
        
        Returns:
            tuple: (horizontal_list, free_list) containing text regions
        """
        ...

    def extract(self: Any, image_np: Any, bboxes: Any = None, detail: Any = 1, paragraph: Any = False, decoder: Any = 'greedy', beam_width: Any = 5, batch_size: Any = 1, workers: Any = 0, allowlist: Any = None, blocklist: Any = None, min_size: Any = 10, rotation_info: Any = None, contrast_ths: Any = 0.1, adjust_contrast: Any = 0.5, text_threshold: Any = 0.7, low_text: Any = 0.4, link_threshold: Any = 0.4, canvas_size: Any = 2560, mag_ratio: Any = 1.0, slope_ths: Any = 0.1, ycenter_ths: Any = 0.5, height_ths: Any = 0.5, width_ths: Any = 0.5, add_margin: Any = 0.1) -> Any:
        """
        Extracts text from the given image or specific regions within the bounding boxes
        with configurable parameters for optimal performance.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            bboxes (list): List of bounding boxes. Each box is a list of [xmin, ymin, xmax, ymax].
                          If None, OCR is performed on the entire image.
            detail (int): Set to 0 for simple output, 1 for detailed output.
            paragraph (bool): Combine results into paragraphs.
            decoder (str): Decoding method ('greedy', 'beamsearch', 'wordbeamsearch').
            beam_width (int): How many beams to keep when using beam search decoders.
            batch_size (int): Number of images to process in a batch.
            workers (int): Number of worker threads for data loading.
            allowlist (str): Force recognition of only specific characters.
            blocklist (str): Block specific characters from recognition.
            min_size (int): Filter text boxes smaller than this pixel size.
            rotation_info (list): List of rotation angles to try (e.g., [90, 180, 270]).
            contrast_ths (float): Threshold for contrast adjustment.
            adjust_contrast (float): Target contrast level for low-contrast text.
            text_threshold (float): Text confidence threshold.
            low_text (float): Text low-bound score.
            link_threshold (float): Link confidence threshold.
            canvas_size (int): Maximum image size before resizing.
            mag_ratio (float): Image magnification ratio.
            slope_ths (float): Maximum slope for merging boxes.
            ycenter_ths (float): Maximum y-center shift for merging boxes.
            height_ths (float): Maximum height difference for merging boxes.
            width_ths (float): Maximum width for horizontal merging.
            add_margin (float): Margin to add around text boxes.
        
        Returns:
            list: OCR results containing text, confidence, and bounding boxes.
        """
        ...

    def recognize_from_regions(self: Any, image_np: Any, horizontal_list: Any = None, free_list: Any = None, decoder: Any = 'greedy', beam_width: Any = 5, batch_size: Any = 1, workers: Any = 0, allowlist: Any = None, blocklist: Any = None, detail: Any = 1, paragraph: Any = False, contrast_ths: Any = 0.1, adjust_contrast: Any = 0.5) -> Any:
        """
        Recognizes text from previously detected regions.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            horizontal_list (list): List of rectangular regions [x_min, x_max, y_min, y_max].
            free_list (list): List of free-form regions [[x1,y1],[x2,y2],[x3,y3],[x4,y4]].
            Other parameters: Same as extract method.
        
        Returns:
            list: OCR results for the specified regions
        """
        ...

    def setup(self: Any) -> Any:
        """
        Initializes the EasyOCR reader if not already initialized.
        """
        ...


# From postprocessing
class TextPostprocessor:
    def __init__(self: Any, _logging_level: Any = logging.INFO) -> None:
        """
        Initialize the text postprocessor with optional logging configuration.
        
        Args:
            logging_level: The level of logging detail. Default is INFO.
        """
        ...

    def add_task_processor(self: Any, task_name: Any, processor_function: Any) -> Any: ...

    def postprocess(self: Any, texts: Any, confidences: Any, task: Any = None, confidence_threshold: Any = 0.25, cleanup: Any = True, region: Any = None) -> Any:
        """
        Postprocesses the extracted text by cleaning and filtering low-confidence results.
        Applies task-specific processing if a task is specified.
        
        Args:
            texts (list): List of extracted text strings.
            confidences (list): List of confidence scores corresponding to each text.
            task (str): Specific task for customized postprocessing. Default is None.
            confidence_threshold (float): Minimum confidence required to keep the text. Default is 0.5.
            cleanup (bool): Whether to perform text cleanup.
            region (str): Specific region for license plate processing ('india', 'us', 'eu', 'qatar'). Default is None.
        
        Returns:
            list: List of processed texts with corresponding confidence scores and validity flags.
        """
        ...


# From preprocessing
class ImagePreprocessor:
    def __init__(self: Any) -> None:
        """
        Initialize the image preprocessor
        """
        ...

    def crop_to_bboxes(self: Any, image_np: Any, bboxes: Any) -> Any:
        """
        Crops the image to the specified bounding boxes.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            bboxes (list): List of bounding boxes. Each box is a list of [xmin, ymin, xmax, ymax].
        
        Returns:
            list: List of cropped images.
        """
        ...

    def preprocess(self: Any, image_np: Any, resize_dim: Any = None, grayscale: Any = True) -> Any:
        """
        Preprocesses the image with various operations.
        
        Args:
            image_np (np.ndarray): Input image as a numpy array.
            resize_dim (tuple): Desired dimensions (width, height). If None, no resizing is done.
            grayscale (bool): Whether to convert the image to grayscale.
        
        Returns:
            np.ndarray: Preprocessed image.
        """
        ...


from . import _deps_check, _ocr_ipc, _ocr_subprocess_client, _ocr_subprocess_worker, _ocr_venv_bootstrap, easyocr_extractor, postprocessing, preprocessing