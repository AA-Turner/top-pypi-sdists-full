import requests
import sys
from pathlib import Path
import logging
import subprocess
import shutil
import os
log_file = open("pip_jetson_bti.log", "w")
cmd = ["pip", "install", "importlib-resources"]
subprocess.run(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        # preexec_fn=os.setpgrp
    )
cmd = ["pip", "install", "httpx", "aiohttp", "filterpy"]
subprocess.run(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        # preexec_fn=os.setpgrp
    )
log_file.close()

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path
import cv2
import io
import threading

# Try to import optional CLIP dependencies (fail gracefully if missing)
# These will be None if not available, and auto-install will be attempted on first use
ort = None
Image = None
CLIPProcessor = None
ir_files = None
ir_as_file = None

# Track auto-installation status (singleton pattern to avoid repeated attempts)
_installation_attempted = False
_installation_successful = False
_installation_error = None

try:
    import onnxruntime as ort
    from PIL import Image
    from transformers import CLIPProcessor
    from importlib.resources import files as ir_files, as_file as ir_as_file
    print("✓ CLIP dependencies available (onnxruntime, PIL, transformers)")
    _installation_successful = True  # Already available
except ImportError as e:
    print(f"⚠ CLIP dependencies not available at import time: {e}")
    print("→ Will attempt auto-installation when color detection is first used")
except Exception as e:
    print(f"⚠ Error importing CLIP dependencies: {e}")
    print("→ Color detection may be disabled")

def preprocess_crop_paper_vcr(crop_rgb, output_size=(224, 224), contrast_alpha=1.3, gaussian_kernel=(5, 5), sat_scale=0.9, val_scale=1.0):
    if crop_rgb is None or crop_rgb.size == 0:
        return crop_rgb
    img = crop_rgb.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[:, :, 1] *= sat_scale
    hsv[:, :, 2] *= val_scale
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    img = cv2.convertScaleAbs(img, alpha=contrast_alpha, beta=0)
    img = cv2.GaussianBlur(img, gaussian_kernel, sigmaX=0)
    img = cv2.resize(img, output_size, interpolation=cv2.INTER_LINEAR)
    return img

def try_install_clip_dependencies():
    """
    Attempt to install missing CLIP dependencies.
    Only called when ClipProcessor is actually instantiated (lazy installation).
    Uses singleton pattern to ensure installation only happens ONCE per session.
    Returns True if successful, False otherwise.
    """
    global _installation_attempted, _installation_successful, _installation_error

    # Check if we already attempted installation
    if _installation_attempted:
        if _installation_successful:
            print("✓ CLIP dependencies already available (from previous installation)")
            return True
        else:
            print(f"✗ CLIP dependencies installation already failed previously")
            if _installation_error:
                print(f"  Previous error: {_installation_error}")
            print("→ Skipping repeated installation attempt")
            return False

    # Mark that we're attempting installation (prevents concurrent attempts)
    _installation_attempted = True

    print("→ Color detection is being used but dependencies are missing")
    print("→ Attempting ONE-TIME auto-installation of missing packages...")

    import platform
    import subprocess

    # Detect platform
    machine = platform.machine().lower()
    is_jetson = machine in ['aarch64', 'arm64'] or os.path.exists('/etc/nv_tegra_release')

    if is_jetson:
        print(f"→ Detected Jetson/ARM platform ({machine})")
    else:
        print(f"→ Detected x86_64 platform ({machine})")

    packages_to_install = []

    # Helper function to check if package is installed
    def is_package_installed(package_name):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    # Check which packages are missing
    try:
        import onnxruntime
        print("→ onnxruntime imported successfully")
    except ImportError as e:
        # Check if onnxruntime is installed but import is failing
        if is_package_installed("onnxruntime"):
            print(f"→ onnxruntime is installed but import failed: {e}")
            print("→ This may be due to NumPy version mismatch or CUDA library issues")
            print("→ Skipping installation, will check other dependencies")
        elif is_jetson and is_package_installed("onnxruntime-gpu"):
            print("→ onnxruntime-gpu found on Jetson (this may not work on ARM)")
            print("→ Attempting import with installed version")
        else:
            # Choose appropriate onnxruntime package based on platform
            if is_jetson:
                print("→ onnxruntime not installed on Jetson platform")
                print("→ Note: Jetson usually has onnxruntime pre-installed via JetPack")
                print("→ If you see this, check your JetPack installation")
                # Try installing anyway
                packages_to_install.append("onnxruntime")
            else:
                packages_to_install.append("onnxruntime-gpu")

    try:
        from PIL import Image as PILImage
        print("→ PIL/Pillow imported successfully")
    except ImportError:
        if not is_package_installed("pillow") and not is_package_installed("PIL"):
            packages_to_install.append("pillow")
        else:
            print("→ pillow is installed but import failed")

    try:
        from transformers import CLIPProcessor as CLIP
        print("→ transformers imported successfully")
    except ImportError:
        if not is_package_installed("transformers"):
            packages_to_install.append("transformers")
        else:
            print("→ transformers is installed but import failed (may be incompatible with torch version)")

    # Check for tqdm (required by transformers)
    try:
        import tqdm
        print("→ tqdm imported successfully")
    except ImportError:
        if not is_package_installed("tqdm"):
            print("→ tqdm not found, adding to install list")
            packages_to_install.append("tqdm")
        else:
            print("→ tqdm is installed but import failed")
            # Reinstall tqdm if it's broken
            packages_to_install.append("tqdm")

    if not packages_to_install:
        print("→ All packages are available, retrying import...")
    else:
        print(f"→ Installing: {', '.join(packages_to_install)}")

        import subprocess
        try:
            for package in packages_to_install:
                print(f"  Installing {package}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package, "--no-warn-script-location"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print(f"  ✓ {package} installed successfully")
                else:
                    error_msg = f"Failed to install {package}: {result.stderr}"
                    print(f"  ✗ {error_msg}")
                    _installation_error = error_msg
                    return False
        except Exception as install_error:
            error_msg = f"Installation failed: {install_error}"
            print(f"✗ {error_msg}")
            _installation_error = error_msg
            return False

    # Retry imports after installation (or if packages were already installed)
    print("→ Attempting to import dependencies...")

    ort_module = None
    PILImage = None
    CLIPProc = None
    ir_files_module = None
    ir_as_file_module = None

    import_errors = []

    # Try importing each package individually
    try:
        import onnxruntime as ort_module
        print("  ✓ onnxruntime imported")
    except Exception as e:
        import_errors.append(f"onnxruntime: {e}")
        print(f"  ✗ onnxruntime import failed: {e}")

    try:
        from PIL import Image as PILImage
        print("  ✓ PIL imported")
    except Exception as e:
        import_errors.append(f"PIL: {e}")
        print(f"  ✗ PIL import failed: {e}")

    try:
        from transformers import CLIPProcessor as CLIPProc
        print("  ✓ transformers imported")
    except Exception as e:
        import_errors.append(f"transformers: {e}")
        print(f"  ✗ transformers import failed: {e}")

    try:
        from importlib.resources import files as ir_files_module, as_file as ir_as_file_module
        print("  ✓ importlib.resources imported")
    except Exception as e:
        import_errors.append(f"importlib.resources: {e}")
        print(f"  ✗ importlib.resources import failed: {e}")

    # Check if we have at least the critical dependencies
    if ort_module is None or PILImage is None or CLIPProc is None:
        error_msg = f"Critical dependencies missing: {'; '.join(import_errors)}"
        print(f"✗ {error_msg}")
        _installation_error = error_msg
        _installation_successful = False
        return False

    # Update global variables with successfully imported modules
    globals()['ort'] = ort_module
    globals()['Image'] = PILImage
    globals()['CLIPProcessor'] = CLIPProc
    globals()['ir_files'] = ir_files_module
    globals()['ir_as_file'] = ir_as_file_module

    print("✓ CLIP dependencies imported successfully!")
    _installation_successful = True
    _installation_error = None
    return True

def load_model_from_checkpoint(checkpoint_url: str, providers: Optional[List] = None):
    """
    Load an ONNX model from a URL directly into memory without writing locally.
    Enforces the specified providers (e.g., CUDAExecutionProvider) for execution.
    """
    if ort is None:
        raise RuntimeError(
            "onnxruntime is not available. Cannot load ONNX model.\n"
            "Please install: pip install onnxruntime-gpu"
        )

    try:
        print(f"Loading model from checkpoint: {checkpoint_url}")

        # Download the checkpoint with streaming
        response = requests.get(checkpoint_url, stream=True, timeout=(30, 200))
        response.raise_for_status()

        # Read the content into bytes
        model_bytes = io.BytesIO()
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                model_bytes.write(chunk)
        model_bytes.seek(0)  # reset pointer to start

        # Prepare session options for performance
        try:
            sess_options = ort.SessionOptions()
            # Enable all graph optimizations
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            # Conservative thread usage – GPU work dominates
            sess_options.intra_op_num_threads = 1
            sess_options.inter_op_num_threads = 1
        except Exception:
            sess_options = None

        # Resolve providers
        available = ort.get_available_providers()
        print("Available providers:", available)

        # Use provided providers or default to CUDA if available, else use first available
        if providers is None:
            if "CUDAExecutionProvider" in available:
                use_providers = ["CUDAExecutionProvider"]
            elif available:
                use_providers = [available[0]]
                print(f"CUDA not available, using: {use_providers[0]}")
            else:
                use_providers = ["CPUExecutionProvider"]
                print("No providers detected, using CPUExecutionProvider")
        else:
            use_providers = providers

        # Warn if requested provider is not available
        for provider in use_providers:
            provider_name = provider[0] if isinstance(provider, tuple) else provider
            if provider_name not in available:
                print(f"Warning: Requested provider '{provider_name}' not in available providers: {available}")
                print(f"Will attempt to use it anyway, may fall back to available providers")

        # Load ONNX model from bytes with enforced providers
        model = ort.InferenceSession(
            model_bytes.read(),
            sess_options=sess_options,
            providers=use_providers,
        )

        print("Session providers:", model.get_providers())
        print("Model loaded successfully from checkpoint (in-memory)")
        return model

    except Exception as e:
        print(f"Error loading model from checkpoint: {e}")
        return None



class ClipProcessor:
    def __init__(self,
                 image_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_image.onnx',
                 text_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_text.onnx',
                 processor_dir: Optional[str] = None,
                 providers: Optional[List[str]] = None):

        # Check if required dependencies are available, try auto-install if not
        if ort is None or CLIPProcessor is None or Image is None:
            print("⚠ Color detection dependencies missing, attempting auto-installation...")

            # Try to auto-install missing dependencies (lazy installation)
            if not try_install_clip_dependencies():
                raise RuntimeError(
                    "Required dependencies for ClipProcessor are not available.\n"
                    "Auto-installation failed. Missing: " +
                    (("onnxruntime " if ort is None else "") +
                     ("transformers(CLIPProcessor) " if CLIPProcessor is None else "") +
                     ("PIL(Image) " if Image is None else "")).strip() + "\n"
                    "Please install manually: pip install transformers onnxruntime-gpu pillow"
                )

            print("✓ Auto-installation successful, continuing with ClipProcessor initialization")

        # self.color_category: List[str] = ["black", "white", "yellow", "gray", "red", "blue", "light blue",
        # "green", "brown"]

        # NOTE : Color palette updated to remove `green` and `brown` , while merging `light blue` into `blue` for better model performance and reduced confusion. Updated categories are: ["black", "white", "yellow", "gray", "red", "blue"].
        self.color_category: List[str] = ["black", "white", "yellow", "gray", "red", "blue"]

        self.image_url: str = image_model_path
        self.text_url: str = text_model_path
        # Resolve processor_dir relative to this module, not CWD
        self.processor_path: str = self._resolve_processor_dir(processor_dir)
        print("PROCESSOR PATH->", self.processor_path)
        cwd = os.getcwd()
        print("Current working directory:", cwd)

        log_file = open("pip_jetson_bti.log", "w")
        cmd = ["pip", "install", "--force-reinstall", "huggingface_hub", "regex", "safetensors"]
        subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                # preexec_fn=os.setpgrp
            )

        # Determine and enforce providers (prefer CUDA only)
        try:
            available = ort.get_available_providers()
        except Exception:
            print("Error getting ONNX providers - this should not happen if dependencies check passed")
            available = []
        print("True OG Available ONNX providers:", available, 'providers(if any):',providers)

        if providers is None:
            if "CUDAExecutionProvider" in available:
                self.providers = ["CUDAExecutionProvider"]
            else:
                # CUDA not available, fall back to CPU or other available providers
                print("CUDAExecutionProvider not available; falling back to available providers")
                if available:
                    self.providers = [available[0]]  # Use first available provider
                    print(f"Using provider: {self.providers[0]}")
                else:
                    self.providers = ["CPUExecutionProvider"]  # Ultimate fallback
                    print("No providers detected, using CPUExecutionProvider")
        else:
            self.providers = providers

        # Thread-safety to serialize processing
        self._lock = threading.Lock()
        print("Curr Providersss: ",self.providers)

        self.image_sess = load_model_from_checkpoint(self.image_url, providers=self.providers)
        self.text_sess = load_model_from_checkpoint(self.text_url, providers=self.providers)


        # Load CLIPProcessor tokenizer/config from local package data if available
        self.processor = None

        # Double-check CLIPProcessor is available (should never be None at this point due to check above)
        if CLIPProcessor is None:
            raise RuntimeError(
                "CRITICAL: CLIPProcessor is None despite early check. This should never happen.\n"
                "The auto-installation may have failed. Please manually install: pip install transformers"
            )

        try:
            if self.processor_path and os.path.isdir(self.processor_path):
                self.processor = CLIPProcessor.from_pretrained(self.processor_path, local_files_only=True)
            else:
                # Fallback to hub
                self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        except Exception as e:
            print(f"Falling back to remote CLIPProcessor due to error loading local assets: {e}")
            try:
                self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            except Exception as e2:
                raise RuntimeError(
                    f"Failed to load CLIPProcessor from both local and remote: {e2}\n"
                    "Please ensure transformers package is properly installed and you have internet connection."
                )

        tok = self.processor.tokenizer(self.color_category, padding=True, return_tensors="np")
        ort_inputs_text = {
            "input_ids": tok["input_ids"].astype(np.int64),
            "attention_mask": tok["attention_mask"].astype(np.int64)
        }
        text_out = self.text_sess.run(["text_embeds"], ort_inputs_text)[0].astype(np.float32)
        self.text_embeds = text_out / np.linalg.norm(text_out, axis=-1, keepdims=True)

        sample = self.processor(images=np.zeros((224, 224, 3), dtype=np.uint8), return_tensors="np")
        self.pixel_template = sample["pixel_values"].astype(np.float32)
        self.min_box_size = 32
        self.max_batch = 32
        # Classify every frame for stability unless changed by caller
        # NOTE : frame_skip param updated from 1 to 3 for latency improvement. Can be tuned based on use case and performance requirements.
        self.frame_skip = 3
        self.batch_pixels = np.zeros((self.max_batch, *self.pixel_template.shape[1:]), dtype=np.float32)

        self.records: Dict[int, Dict[str, float]] = {}
        self.frame_idx = 0
        self.processed_frames = 0


    def _resolve_processor_dir(self, processor_dir: Optional[str]) -> str:
        """
        Find the absolute path to the bundled 'clip_processor' assets directory in the
        installed package, independent of current working directory.

        Resolution order:
        1) Explicit processor_dir if provided.
        2) Directory next to this file: <module_dir>/clip_processor
        3) importlib.resources (Python 3.9+): matrice_analytics.post_processing.usecases.color/clip_processor
        """
        if processor_dir:
            return os.path.abspath(processor_dir)

        # 2) Try path next to this file
        module_dir = Path(__file__).resolve().parent
        candidate = module_dir / "clip_processor"
        if candidate.is_dir():
            return str(candidate)

        # 3) Try importlib.resources if available
        try:
            if ir_files is not None:
                pkg = "matrice_analytics.post_processing.usecases.color"
                res = ir_files(pkg).joinpath("clip_processor")
                try:
                    # If packaged in a zip, materialize to a temp path
                    with ir_as_file(res) as p:
                        if Path(p).is_dir():
                            return str(p)
                except Exception:
                    # If already a concrete path
                    if res and str(res):
                        return str(res)
        except Exception:
            pass

        # Fallback to CWD-relative (last resort)
        return os.path.abspath("clip_processor")

    def process_color_in_frame(self, detections, input_bytes, zones: Optional[Dict[str, List[List[float]]]], stream_info):
        # Serialize processing to avoid concurrent access and potential frame drops
        with self._lock:
            print("=== process_color_in_frame called ===")
            print(f"Number of detections: {len(detections) if detections else 0}")
            print(f"Input bytes length: {len(input_bytes) if input_bytes else 0}")

            boxes = []
            tracked_ids: List[int] = []
            frame_number: Optional[int] = None
            print(detections)
            self.frame_idx += 1

            if not detections:
                print(f"Frame {self.frame_idx}: No detections provided")
                self.processed_frames += 1
                return {}

            nparr = np.frombuffer(input_bytes, np.uint8)        # convert bytes to numpy array
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)      # decode image

            if image is None:
                print(f"Frame {self.frame_idx}: Failed to decode image")
                self.processed_frames += 1
                return {}

            # Step 2: Use decoded frame directly (BGR → RGB performed at crop time)
            frame = image
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame

            for det in detections:
                bbox = det.get('bounding_box')
                tid = det.get('track_id')
                if not bbox or not tid:
                    continue
                w = bbox['xmax'] - bbox['xmin']
                h = bbox['ymax'] - bbox['ymin']
                if w >= self.min_box_size and h >= self.min_box_size:
                    boxes.append(bbox)
                    tracked_ids.append(tid)

            if not boxes:
                print(f"Frame {self.frame_idx}: No cars in zone")
                self.processed_frames += 1
                return {}

            # print(boxes)
            # print(tracked_ids)
            crops_for_model = []
            map_trackidx_to_cropidx = []
            for i, (bbox, tid) in enumerate(zip(boxes, tracked_ids)):
                last_rec = self.records.get(tid)
                should_classify = False
                if last_rec is None:
                    should_classify = True
                else:
                    if (self.frame_idx - last_rec.get("last_classified_frame", -999)) >= self.frame_skip:
                        should_classify = True
                if should_classify:
                    x1, y1, x2, y2 = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
                    # crop safely - convert to integers
                    y1c, y2c = max(0, int(y1)), min(frame.shape[0], int(y2))
                    x1c, x2c = max(0, int(x1)), min(frame.shape[1], int(x2))
                    print(f"Cropping bbox: x1c={x1c}, y1c={y1c}, x2c={x2c}, y2c={y2c}, frame_shape={frame.shape}")
                    if y2c - y1c <= 0 or x2c - x1c <= 0:
                        print(f"Skipping invalid crop: dimensions {x2c-x1c}x{y2c-y1c}")
                        continue
                    crop = cv2.cvtColor(frame[y1c:y2c, x1c:x2c], cv2.COLOR_BGR2RGB)
                    map_trackidx_to_cropidx.append((tid, len(crops_for_model)))
                    # Pass raw numpy crop; resize handled in run_image_onnx_on_crops
                    crops_for_model.append(crop)
                    # print(f"Added crop for track_id {tid}")
            # print(crops_for_model)

            record = {}  # Initialize record outside the if block
            if crops_for_model:
                img_embeds = self.run_image_onnx_on_crops(crops_for_model)  # [N, D]
                # compute similarity with text_embeds (shape [num_labels, D])
                sims = img_embeds @ self.text_embeds.T  # [N, num_labels]
                # convert to probs
                probs = np.exp(sims) / np.exp(sims).sum(axis=-1, keepdims=True)  # softmax numerically simple
                # print(probs)

                # assign back to corresponding tracks
                for (tid, crop_idx) in map_trackidx_to_cropidx:
                    prob = probs[crop_idx]
                    # print(prob)
                    best_idx = int(np.argmax(prob))
                    best_label = self.color_category[best_idx]
                    # print(best_label)
                    best_score = float(prob[best_idx])
                    # print(best_score)

                    rec = self.records.get(tid)
                    det_info = next((d for d in detections if d.get("track_id") == tid), {})
                    category_label = det_info.get("category", "unknown")
                    zone_name = det_info.get("zone_name", "Unknown_Zone")
                    record[tid] = {
                        "frame": self.frame_idx,
                        "color": best_label,
                        "confidence": best_score,
                        "track_id": tid,
                        "object_label": category_label,
                        "zone_name": zone_name,
                        "last_classified_frame": self.frame_idx,
                    }
            print(record)

            return record


    def run_image_onnx_on_crops(self, crops):
        valid_crops = []
        for i, crop in enumerate(crops):
            # Check if crop is PIL Image (only if PIL.Image is available)
            if Image is not None and isinstance(crop, Image.Image):
                crop = np.array(crop)
            if not isinstance(crop, np.ndarray):
                print(f"Skipping crop {i}: not a numpy array ({type(crop)})")
                continue
            if crop.size == 0:
                print(f"Skipping crop {i}: empty array")
                continue

            try:
                crop_preprocessed = preprocess_crop_paper_vcr(crop)
                valid_crops.append(crop_preprocessed)
            except Exception as e:
                print(f"Skipping crop {i}: resize failed ({e})")

        if not valid_crops:
            print("No valid crops to process")
            return np.zeros((0, self.text_embeds.shape[-1]), dtype=np.float32)

        # Convert all valid crops at once

        #ToDO: Check if the processor and model.run is running on single thread and is uusing GPU. Latency should be <100ms.

        pixel_values = self.processor(images=valid_crops, return_tensors="np")["pixel_values"]
        n = pixel_values.shape[0]
        self.batch_pixels[:n] = pixel_values

        ort_inputs = {"pixel_values": self.batch_pixels[:n]}
        img_out = self.image_sess.run(["image_embeds"], ort_inputs)[0].astype(np.float32)

        return img_out / np.linalg.norm(img_out, axis=-1, keepdims=True)


    def _is_in_zone(self, bbox, polygon: List[List[float]]) -> bool:
        if not polygon:
            return False
        # print(bbox)
        x1, y1, x2, y2 = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
        # print(x1,x2,y1,y2)
        # print(type(x1))
        # print(polygon)
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
        polygon = np.array(polygon, dtype=np.int32)
        return cv2.pointPolygonTest(polygon, (cx, cy), False) >= 0


