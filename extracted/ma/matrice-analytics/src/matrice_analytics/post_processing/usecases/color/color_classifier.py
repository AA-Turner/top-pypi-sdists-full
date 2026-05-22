"""
Vehicle Color Classifier (CNN) — On Hold

This updated CNN-based vehicle color classification pipeline is currently
not in active use.

NOTE:
Before re-enabling, update the model bucket URL (TODO) to point to the latest
trained checkpoint (.pth) containing the required serialized artifacts:

    - model_state_dict
    - config
    - class_names
    - num_classes
    - model_name

Refer to the standardized checkpoint packaging schema used in recent
training runs.

Current Production Status:
We are continuing with the CLIP-based color classification approach in
usecase `color_detection` (Application: Color Detection) due to its
zero-shot flexibility and robustness across diverse conditions.

The CLIP-based approach is currently augmented with improved crop
preprocessing and an updated color palette.

The CNN pipeline is being retained in the codebase for potential future
use. It remains staged for evaluation, benchmarking, and possible
reintegration pending validation within the updated usecase
`vehicle_color_detection` (Application: Vehicle Color Detection).
"""

import os

try:
    import cv2
except ImportError:
    cv2 = None
import hashlib
import logging
import threading
import time

try:
    import requests
except ImportError:
    requests = None
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

DEFAULT_COLOR_PALETTE: List[str] = [
    "black",
    "white",
    "yellow",
    "gray",
    "red",
    "blue",
    "green",
]

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

DEFAULT_INPUT_SIZE = 224
DEFAULT_MIN_CROP_SIZE = 32
DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "color_classifier")
DEFAULT_MAX_RETRIES = 3
DEFAULT_TIMEOUT = 180
MIN_VALID_FILE_SIZE = 100_000


torch = None
timm = None
ort = None


def _import_torch():
    global torch, timm
    if torch is None:
        try:
            import torch as _torch

            torch = _torch
        except ImportError:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass
    if timm is None:
        try:
            import timm as _timm

            timm = _timm
        except ImportError:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass
    return torch is not None and timm is not None


def _import_onnx():
    global ort
    if ort is None:
        try:
            import onnxruntime as _ort

            ort = _ort
        except ImportError:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass
    return ort is not None


logger = logging.getLogger(__name__)


def _is_url(path: str) -> bool:
    """Check if path is a URL (HTTP/HTTPS/S3)."""
    if path is None:
        return False
    return path.startswith("http://") or path.startswith("https://") or path.startswith("s3://")


def _download_with_retry(
    url: str, max_retries: int = DEFAULT_MAX_RETRIES, timeout: int = DEFAULT_TIMEOUT
) -> Optional[bytes]:
    """
    Download file from URL with retry logic and progress indication.
    Aligned with clip.py pattern.
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Download attempt {attempt + 1}/{max_retries}: {url}")
            response = requests.get(url, stream=True, timeout=(30, timeout))
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            chunks = []
            downloaded = 0

            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    chunks.append(chunk)
                    downloaded += len(chunk)
                    if total_size > 0 and downloaded % (1024 * 1024) == 0:
                        pct = (downloaded / total_size) * 100
                        logger.debug(f"Download progress: {pct:.1f}% ({downloaded // 1024 // 1024}MB)")

            logger.info(f"Download complete: {downloaded // 1024}KB")
            return b"".join(chunks)

        except Exception as e:
            logger.warning(f"Download attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10  # 10s, 20s, 30s backoff
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)

    return None


def _get_cache_path(url: str, cache_dir: str) -> str:
    """
    Generate deterministic cache path from URL.
    Pattern: {cache_dir}/{url_hash[:8]}_{basename}
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]  # noqa: S324  # nosec B324  # nosemgrep: python.lang.security.insecure-hash-algorithms-md5.insecure-hash-algorithm-md5
    basename = os.path.basename(url.split("?")[0])
    return os.path.join(cache_dir, f"{url_hash}_{basename}")


def _is_cached_valid(cache_path: str) -> bool:
    """Check if cached file exists and is valid (size > MIN_VALID_FILE_SIZE)."""
    return os.path.exists(cache_path) and os.path.getsize(cache_path) > MIN_VALID_FILE_SIZE


def _ensure_file_local(
    path_or_url: str,
    cache_dir: str = DEFAULT_CACHE_DIR,
    max_retries: int = DEFAULT_MAX_RETRIES,
    timeout: int = DEFAULT_TIMEOUT,
) -> Optional[str]:
    """
    Ensure file is available locally. Downloads from URL if needed.

    Returns:
        Local file path, or None if unavailable
    """
    if path_or_url is None:
        return None

    # Case 1: Local path
    if not _is_url(path_or_url):
        if os.path.exists(path_or_url):
            logger.info(f"Using local file: {path_or_url}")
            return path_or_url
        logger.warning(f"Local file not found: {path_or_url}")
        return None

    # Case 2: URL - check cache first
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = _get_cache_path(path_or_url, cache_dir)

    if _is_cached_valid(cache_path):
        logger.info(f"Using cached file: {cache_path}")
        return cache_path

    # Case 3: Download from URL
    logger.info(f"Downloading from URL: {path_or_url}")
    model_bytes = _download_with_retry(path_or_url, max_retries, timeout)

    if model_bytes is None:
        logger.error(f"Failed to download: {path_or_url}")
        return None

    # Save to cache
    try:
        with open(cache_path, "wb") as f:
            f.write(model_bytes)
        logger.info(f"Cached to: {cache_path}")
        return cache_path
    except Exception as e:
        logger.error(f"Failed to cache file: {e}")
        return None


def preprocess_crop(crop: np.ndarray, input_size: int = DEFAULT_INPUT_SIZE) -> np.ndarray:
    """Preprocess single crop: resize, normalize, transpose to NCHW."""
    img = cv2.resize(crop, (input_size, input_size), interpolation=cv2.INTER_LINEAR)
    img = img.astype(np.float32) / 255.0
    img = (img - IMAGENET_MEAN) / IMAGENET_STD
    img = np.transpose(img, (2, 0, 1))  # HWC → CHW
    return img.astype(np.float32)


@dataclass
class ColorCacheEntry:
    color: str
    confidence: float
    last_frame: int


class ColorCache:
    """Track-ID based LRU cache for color predictions."""

    def __init__(self, max_size: int = 1000, update_interval: int = 5):
        self.max_size = max_size
        self.update_interval = update_interval
        self._cache: Dict[int, ColorCacheEntry] = {}
        self._order: List[int] = []

    def should_classify(self, track_id: int, frame: int) -> bool:
        if track_id not in self._cache:
            return True
        return (frame - self._cache[track_id].last_frame) >= self.update_interval

    def get(self, track_id: int) -> Optional[ColorCacheEntry]:
        return self._cache.get(track_id)

    def set(self, track_id: int, color: str, confidence: float, frame: int):
        if track_id in self._cache:
            self._cache[track_id] = ColorCacheEntry(color, confidence, frame)
            if track_id in self._order:
                self._order.remove(track_id)
        else:
            if len(self._cache) >= self.max_size:
                oldest = self._order.pop(0)
                del self._cache[oldest]
            self._cache[track_id] = ColorCacheEntry(color, confidence, frame)
        self._order.append(track_id)


class ColorClassifier:
    """
    CNN-based color classifier for vehicle color detection.

    Model Loading Priority:
        1. PyTorch checkpoint (.pt/.pth) - preferred
        2. ONNX model (.onnx) - fallback

    Source Priority:
        1. URL (HTTP/S3) → download to ~/.cache/color_classifier/ → load
        2. Local path → load directly

    Supports:
        - PyTorch checkpoint with timm models (ConvNeXt, EfficientNet, etc.)
        - ONNX model with optional external weights (.onnx.data)
        - Automatic CUDA/CPU device selection
        - Track-ID based caching with frame-skip
    """

    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        onnx_path: Optional[str] = None,
        onnx_data_path: Optional[str] = None,
        color_palette: Optional[List[str]] = None,
        input_size: int = DEFAULT_INPUT_SIZE,
        min_crop_size: int = DEFAULT_MIN_CROP_SIZE,
        return_probabilities: bool = False,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        """
        Initialize color classifier.

        Args:
            checkpoint_path: Path or URL to PyTorch checkpoint (.pt/.pth)
            onnx_path: Path or URL to ONNX model (.onnx)
            onnx_data_path: Path or URL to ONNX external weights (.onnx.data)
            color_palette: List of color labels (default: 7 classes)
            input_size: Input image size (default: 224)
            min_crop_size: Minimum crop dimension to process (default: 32)
            return_probabilities: Include full probability dict in output
            cache_dir: Directory for caching downloaded models
        """
        self.color_palette = color_palette or DEFAULT_COLOR_PALETTE.copy()
        self.num_classes = len(self.color_palette)
        self.input_size = input_size
        self.min_crop_size = min_crop_size
        self.return_probabilities = return_probabilities
        self.cache_dir = cache_dir

        self._lock = threading.Lock()
        self._disabled = False
        self._disable_reason: Optional[str] = None
        self._init_logged = False

        # Model state
        self._use_onnx = False
        self._use_pytorch = False
        self._model = None
        self._onnx_session = None
        self._device = None
        self._model_info: Dict[str, Any] = {}

        initialized = False

        # Priority 1: PyTorch checkpoint
        if checkpoint_path and not initialized:
            initialized = self._try_init_pytorch(checkpoint_path)

        # Priority 2: ONNX model
        if onnx_path and not initialized:
            initialized = self._try_init_onnx(onnx_path, onnx_data_path)

        if not initialized:
            self._disable(f"No valid model available. checkpoint_path={checkpoint_path}, onnx_path={onnx_path}")

        self._log_init_status()

    def _disable(self, reason: str):
        """Disable classifier with reason (logged once)."""
        self._disabled = True
        self._disable_reason = reason

    def _log_init_status(self):
        """Log initialization status once."""
        if self._init_logged:
            return
        self._init_logged = True

        if self._disabled:
            logger.error(f"ColorClassifier DISABLED: {self._disable_reason}")
        else:
            mode = "PyTorch" if self._use_pytorch else "ONNX"
            logger.info(
                f"ColorClassifier initialized: mode={mode}, classes={self.num_classes}, palette={self.color_palette}"
            )
            if self._model_info:
                logger.info(f"Model info: {self._model_info}")

    def _try_init_pytorch(self, checkpoint_path: str) -> bool:
        """
        Attempt to initialize PyTorch model.

        Returns:
            True if successful, False otherwise
        """
        if not _import_torch():
            logger.warning("PyTorch/timm not available, skipping PyTorch initialization")
            return False

        local_path = _ensure_file_local(checkpoint_path, self.cache_dir)
        if local_path is None:
            logger.warning(f"PyTorch checkpoint unavailable: {checkpoint_path}")
            return False

        try:
            logger.info(f"Loading PyTorch checkpoint: {local_path}")

            ckpt = torch.load(local_path, map_location="cpu", weights_only=False)  # nosec B614

            # NOTE : Store essential info in config
            config = ckpt.get("config", {})
            model_name = config.get("model_name", "convnext_small.in12k_ft_in1k")

            if "model_state_dict" in ckpt:
                state_dict = ckpt["model_state_dict"]
            elif "state_dict" in ckpt:
                state_dict = ckpt["state_dict"]
            else:
                state_dict = ckpt

            detected_num_classes = None
            for key, value in state_dict.items():
                if any(
                    x in key
                    for x in [
                        "head.fc.weight",
                        "classifier.weight",
                        "head.weight",
                        "fc.weight",
                    ]
                ):
                    detected_num_classes = value.shape[0]
                    logger.info(f"Detected num_classes from checkpoint: {detected_num_classes}")
                    break

            # Update class configuration
            if "class_names" in ckpt:
                self.color_palette = ckpt["class_names"]
                self.num_classes = len(self.color_palette)
                logger.info(f"Loaded class_names from checkpoint: {self.color_palette}")
            elif detected_num_classes is not None:
                if detected_num_classes != self.num_classes:
                    logger.warning(
                        f"Checkpoint num_classes ({detected_num_classes}) differs from "
                        f"palette size ({self.num_classes}). Using checkpoint value."
                    )
                    self.num_classes = detected_num_classes
                    # Extend or truncate palette if needed
                    if len(self.color_palette) < self.num_classes:
                        for i in range(len(self.color_palette), self.num_classes):
                            self.color_palette.append(f"color_{i}")
                    elif len(self.color_palette) > self.num_classes:
                        self.color_palette = self.color_palette[: self.num_classes]
            else:
                logger.warning(f"Could not detect num_classes from checkpoint. Using palette size: {self.num_classes}")

            # Create model
            logger.info(f"Creating timm model: {model_name} with {self.num_classes} classes")
            self._model = timm.create_model(model_name, pretrained=False, num_classes=self.num_classes)

            # Load weights
            self._model.load_state_dict(state_dict, strict=False)

            # Setup device
            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self._model.to(self._device)
            self._model.eval()

            self._use_pytorch = True
            self._model_info = {
                "model_name": model_name,
                "device": str(self._device),
                "source": checkpoint_path,
                "local_path": local_path,
                "epoch": ckpt.get("epoch", "N/A"),
                "val_acc": ckpt.get("val_acc", "N/A"),
            }

            logger.info(f"PyTorch model loaded successfully on {self._device}")
            return True

        except Exception as e:
            logger.warning(f"PyTorch initialization failed: {e}")
            return False

    def _try_init_onnx(self, onnx_path: str, onnx_data_path: Optional[str] = None) -> bool:
        """
        Attempt to initialize ONNX model.

        Args:
            onnx_path: Path or URL to .onnx file
            onnx_data_path: Optional path or URL to .onnx.data file (external weights)

        Returns:
            True if successful, False otherwise
        """
        if not _import_onnx():
            logger.warning("ONNX Runtime not available, skipping ONNX initialization")
            return False

        local_onnx = _ensure_file_local(onnx_path, self.cache_dir)
        if local_onnx is None:
            logger.warning(f"ONNX model unavailable: {onnx_path}")
            return False

        if onnx_data_path:
            local_data = _ensure_file_local(onnx_data_path, self.cache_dir)
            if local_data is None:
                logger.warning(f"ONNX data file unavailable: {onnx_data_path}")
            else:
                onnx_dir = os.path.dirname(local_onnx)
                expected_data_path = os.path.join(onnx_dir, os.path.basename(local_data))
                if local_data != expected_data_path and not os.path.exists(expected_data_path):
                    try:
                        import shutil

                        shutil.copy2(local_data, expected_data_path)
                        logger.info(f"Copied ONNX data to: {expected_data_path}")
                    except Exception as e:
                        logger.warning(f"Failed to copy ONNX data file: {e}")

        try:
            logger.info(f"Loading ONNX model: {local_onnx}")

            providers = ort.get_available_providers()
            logger.info(f"Available ONNX providers: {providers}")

            use_providers = (
                ["CUDAExecutionProvider", "CPUExecutionProvider"]
                if "CUDAExecutionProvider" in providers
                else ["CPUExecutionProvider"]
            )

            # Session options
            sess_options = ort.SessionOptions()
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            sess_options.intra_op_num_threads = 1
            sess_options.inter_op_num_threads = 1

            self._onnx_session = ort.InferenceSession(local_onnx, sess_options=sess_options, providers=use_providers)

            self._onnx_input_name = self._onnx_session.get_inputs()[0].name
            self._use_onnx = True

            output_info = self._onnx_session.get_outputs()[0]
            if hasattr(output_info, "shape") and output_info.shape:
                detected_classes = output_info.shape[-1]
                if isinstance(detected_classes, int) and detected_classes != self.num_classes:
                    logger.warning(
                        f"ONNX output classes ({detected_classes}) differs from "
                        f"palette size ({self.num_classes}). Adjusting palette."
                    )
                    self.num_classes = detected_classes
                    if len(self.color_palette) < self.num_classes:
                        for i in range(len(self.color_palette), self.num_classes):
                            self.color_palette.append(f"color_{i}")
                    elif len(self.color_palette) > self.num_classes:
                        self.color_palette = self.color_palette[: self.num_classes]

            self._model_info = {
                "source": onnx_path,
                "local_path": local_onnx,
                "providers": self._onnx_session.get_providers(),
            }

            logger.info(f"ONNX model loaded, providers: {self._onnx_session.get_providers()}")
            return True

        except Exception as e:
            logger.warning(f"ONNX initialization failed: {e}")
            return False

    @property
    def is_available(self) -> bool:
        """Check if classifier is ready for inference."""
        return not self._disabled

    def classify(
        self,
        detections: List[Dict],
        input_bytes: bytes,
        frame_number: int = 0,
        cache: Optional[ColorCache] = None,
    ) -> Dict[int, Dict[str, Any]]:
        """
        Classify colors for detections in a frame.

        Args:
            detections: List of detection dicts with 'track_id' and 'bounding_box'
            input_bytes: JPEG/PNG encoded frame bytes
            frame_number: Current frame number (for cache logic)
            cache: Optional ColorCache instance

        Returns:
            Dict mapping track_id → {"color": str, "confidence": float}
        """
        if self._disabled:
            return {}

        with self._lock:
            results = {}
            needs_inference = []

            for det in detections:
                tid = det.get("track_id")
                if tid is None:
                    continue

                if cache and not cache.should_classify(tid, frame_number):
                    entry = cache.get(tid)
                    if entry:
                        results[tid] = {
                            "color": entry.color,
                            "confidence": entry.confidence,
                        }
                        continue

                needs_inference.append(det)

            if not needs_inference:
                return results

            try:
                frame = cv2.imdecode(np.frombuffer(input_bytes, np.uint8), cv2.IMREAD_COLOR)
                if frame is None:
                    logger.warning("Failed to decode frame")
                    return results
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                logger.warning(f"Frame decode error: {e}")
                return results

            for det in needs_inference:
                tid = det["track_id"]
                bbox = det.get("bounding_box", det.get("bbox"))

                crop = self._extract_crop(frame_rgb, bbox)
                if crop is None:
                    results[tid] = {"color": "unknown", "confidence": 0.0}
                    continue

                color, conf, probs = self._infer_single(crop)

                result = {"color": color, "confidence": conf}
                if self.return_probabilities and probs is not None:
                    result["probabilities"] = probs

                results[tid] = result

                if cache:
                    cache.set(tid, color, conf, frame_number)

            return results

    def _extract_crop(self, frame: np.ndarray, bbox: Any) -> Optional[np.ndarray]:
        """Extract and validate crop from frame."""
        try:
            if isinstance(bbox, dict):
                x1 = int(bbox.get("xmin", bbox.get("x1", 0)))
                y1 = int(bbox.get("ymin", bbox.get("y1", 0)))
                x2 = int(bbox.get("xmax", bbox.get("x2", 0)))
                y2 = int(bbox.get("ymax", bbox.get("y2", 0)))
            elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                x1, y1, x2, y2 = map(int, bbox[:4])
            else:
                return None

            h, w = frame.shape[:2]
            x1, x2 = max(0, x1), min(w, x2)
            y1, y2 = max(0, y1), min(h, y2)

            if (x2 - x1) < self.min_crop_size or (y2 - y1) < self.min_crop_size:
                return None

            return frame[y1:y2, x1:x2]
        except Exception:
            return None

    def _infer_single(self, crop: np.ndarray) -> Tuple[str, float, Optional[Dict[str, float]]]:
        """Run inference on single crop. Returns (color, confidence, probabilities)."""
        try:
            processed = preprocess_crop(crop, self.input_size)
            batch = np.expand_dims(processed, axis=0)

            if self._use_onnx:
                logits = self._onnx_session.run(None, {self._onnx_input_name: batch})[0]
                exp_logits = np.exp(logits - logits.max(axis=1, keepdims=True))
                probs = (exp_logits / exp_logits.sum(axis=1, keepdims=True))[0]
            else:
                with torch.no_grad():
                    tensor = torch.from_numpy(batch).to(self._device)
                    logits = self._model(tensor)
                    probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

            best_idx = int(np.argmax(probs))
            color = self.color_palette[best_idx] if best_idx < len(self.color_palette) else "unknown"
            conf = float(probs[best_idx])

            prob_dict = None
            if self.return_probabilities:
                prob_dict = {
                    self.color_palette[i]: round(float(probs[i]), 4)
                    for i in range(min(len(self.color_palette), len(probs)))
                }

            return color, round(conf, 4), prob_dict

        except Exception as e:
            logger.debug(f"Inference error: {e}")
            return "unknown", 0.0, None

    def classify_crops(self, crops: List[np.ndarray]) -> List[Dict]:
        """
        Batch classification API (ClipProcessor compatible).

        Args:
            crops: List of RGB numpy arrays

        Returns:
            List of {"color": str, "confidence": float, "all_colors": [...]}
        """
        if self._disabled or not crops:
            return []

        with self._lock:
            results = []
            for crop in crops:
                if crop is None or crop.size == 0:
                    results.append({"color": "unknown", "confidence": 0.0, "all_colors": []})
                    continue

                color, conf, probs = self._infer_single(crop)

                all_colors = []
                if probs:
                    sorted_items = sorted(probs.items(), key=lambda x: x[1], reverse=True)
                    all_colors = [
                        {"rank": i + 1, "color": c, "probability": round(p, 4)}
                        for i, (c, p) in enumerate(sorted_items[:5])
                    ]

                results.append({"color": color, "confidence": conf, "all_colors": all_colors})

            return results
