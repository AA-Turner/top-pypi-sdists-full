"""Module providing __init__ functionality."""

import logging
import multiprocessing
import os
import platform
import sys

# Configure package-level loggers
logging.getLogger("kafka").setLevel(logging.INFO)
logging.getLogger("confluent_kafka").setLevel(logging.INFO)

# Create logger for this module
logger = logging.getLogger(__name__)

# Only run dependency checks in the main process, NOT in spawned child
# processes (mp workers re-import modules; rerunning pip installs from
# children racks up BrokenProcessPool errors and corrupts site-packages).
# Cross-process serialization between sibling main-process interpreters is
# handled inside `dependencies_check` itself (`matrice_common.utils`).
_is_main_process = multiprocessing.parent_process() is None

# ``matrice_common`` is an internal Matrice.ai wheel (not published to public
# PyPI). It is present in every real deployment/CI environment where this
# package actually runs, but a bare ``pip install matrice_inference`` in a
# clean, PyPI-only venv (e.g. the install-smoke gate) will not have it. Guard
# the import so ``import matrice_inference`` degrades gracefully instead of
# hard-crashing at module load: the runtime dependency bootstrap below is
# simply skipped when the helper is unavailable.
try:
    from matrice_common.utils import dependencies_check

    _HAS_MATRICE_COMMON = True
except ImportError:
    _HAS_MATRICE_COMMON = False

    def dependencies_check(*_args, **_kwargs):  # type: ignore[misc]
        """Fallback no-op when matrice_common is unavailable (import-only envs)."""
        return False

    logger.warning(
        "matrice_common is unavailable; skipping runtime dependency bootstrap. "
        "This is expected in a pure-PyPI import-smoke environment but must NOT "
        "occur in a real deployment."
    )

base = [
    "httpx",
    "fastapi",
    "uvicorn",
    "pillow",
    "confluent_kafka[snappy]",
    "aiokafka",
    "aiohttp",
    "filterpy",
    "scipy",
    "scikit-learn",
    "matplotlib",
    "scikit-image",
    "python-snappy",
    "pyyaml",
    "imagehash",
    "Pillow",
    "transformers",
]

# Package name to import name mapping for common packages
_IMPORT_NAMES = {
    "pillow": "PIL",
    "Pillow": "PIL",
    "scikit-learn": "sklearn",
    "scikit-image": "skimage",
    "python-snappy": "snappy",
    "pyyaml": "yaml",
    "opencv-python": "cv2",
    "opencv-python-headless": "cv2",
    "confluent_kafka[snappy]": "confluent_kafka",
    "fast-plate-ocr[onnx-gpu]": "fast_plate_ocr",
    "fast-plate-ocr[onnx]": "fast_plate_ocr",
    "fast-plate-ocr": "fast_plate_ocr",
    "onnxruntime-gpu": "onnxruntime",
}


def _install_and_verify(pkg: str, import_name: str):
    """Install a package expression and return True if the import succeeds."""
    try:
        if pkg == "onnxruntime-gpu":
            pkg = "onnxruntime"
        __import__(import_name)
        return True
    except ImportError:
        if dependencies_check([pkg]):
            try:
                __import__(import_name)
                return True
            except ImportError:
                return False
        return False


# Runtime gating for optional OCR bootstrap (default OFF), and never on Jetson
_ENABLE_OCR_BOOTSTRAP = os.getenv("MATRICE_ENABLE_OCR_BOOTSTRAP", "0")
_IS_JETSON = platform.machine().lower() in ("aarch64", "arm64")

# Log deployment environment information
logger.info("*******************************Deployment ENV Info**********************************")
logger.info(f"ENABLE_JETSON_PIP_SETTINGS: {_ENABLE_OCR_BOOTSTRAP}")
logger.info(f"IS_JETSON_ARCH?: {_IS_JETSON}")
logger.info("*************************************************************************************")

if _HAS_MATRICE_COMMON and _is_main_process and not int(_ENABLE_OCR_BOOTSTRAP) and not _IS_JETSON:
    dependencies_check(base)

    # Always pull opencv-python-headless. The full opencv-python wheel
    # needs system X11 libs (libxcb.so.1, libsm6, libxext6, libxrender1)
    # that aren't present in aiforeveryone/cicd-runner:v1 (or in most
    # server-side deploys), so importing cv2 fails at runtime even when
    # opencv-python's metadata shows installed. The headless variant has
    # the same API surface minus the GUI bits and no system-lib deps.
    dependencies_check(["opencv-python-headless"])

    # Attempt GPU-specific dependencies first
    _gpu_ok = _install_and_verify("onnxruntime-gpu", "onnxruntime") and _install_and_verify(
        "fast-plate-ocr[onnx-gpu]", "fast_plate_ocr"
    )

    if not _gpu_ok:
        # Fallback to CPU variants
        _cpu_ok = _install_and_verify("onnxruntime", "onnxruntime") and _install_and_verify(
            "fast-plate-ocr[onnx]", "fast_plate_ocr"
        )
        if not _cpu_ok:
            # Last-chance fallback without extras tag (PyPI sometimes lacks them)
            _install_and_verify("fast-plate-ocr", "fast_plate_ocr")

# matrice_deps = ["matrice_common", "matrice_analytics", "matrice"]

# dependencies_check(matrice_deps)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# The public server API pulls in the internal Matrice.ai wheels
# (``matrice_common``, ``matrice_analytics``) transitively. In a real
# deployment/CI environment these are always installed and the names below bind
# normally. In a pure-PyPI import-smoke environment they are absent; rather than
# hard-crash ``import matrice_inference``, expose the public names as ``None``
# and log a clear warning. Any actual USE of these APIs without the internal
# deps still raises a clear error at call time.
try:
    from server.inference_interface import InferenceInterface
    from server.proxy_interface import MatriceProxyInterface
    from server.server import MatriceDeployServer
    from server.server import MatriceDeployServer as MatriceDeploy  # Keep this for backwards compatibility
except ImportError as _api_import_error:
    if _HAS_MATRICE_COMMON:
        # Internal deps are present but the server API still failed to import —
        # that's a genuine error, not the import-smoke case. Re-raise.
        raise
    logger.warning(
        "matrice_inference public server API is unavailable because internal "
        "dependencies are missing (%s). Package imported in degraded mode "
        "(import-smoke only); the server API is not usable here.",
        _api_import_error,
    )
    InferenceInterface = None  # type: ignore[assignment,misc]
    MatriceProxyInterface = None  # type: ignore[assignment,misc]
    MatriceDeployServer = None  # type: ignore[assignment,misc]
    MatriceDeploy = None  # type: ignore[assignment,misc]

__all__ = [
    "InferenceInterface",
    "MatriceDeploy",
    "MatriceDeployServer",
    "MatriceProxyInterface",
]
