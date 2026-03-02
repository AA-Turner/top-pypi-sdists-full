"""Module providing __init__ functionality."""

import os
import sys
import platform
import logging
import fcntl

logging.getLogger("kafka").setLevel(logging.INFO)
logging.getLogger("confluent_kafka").setLevel(logging.INFO)

from matrice_common.utils import dependencies_check

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
    "transformers"
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


def _is_package_installed(pkg: str) -> bool:
    """Check if a package is already importable."""
    # Get the import name for this package
    import_name = _IMPORT_NAMES.get(pkg, pkg.split('[')[0].replace('-', '_'))
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False


def _safe_dependencies_check(packages: list) -> bool:
    """Install dependencies with file locking to prevent race conditions.

    Uses file-based locking to ensure only one process installs packages at a time.
    Checks if packages are already installed before attempting installation.
    """
    lock_file = "/tmp/matrice_deps_install.lock"

    # First, quick check if all packages are already installed (no lock needed)
    packages_to_install = [pkg for pkg in packages if not _is_package_installed(pkg)]
    if not packages_to_install:
        return True

    try:
        # Acquire lock for installation
        with open(lock_file, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                # Double-check after acquiring lock (another process may have installed)
                packages_to_install = [pkg for pkg in packages if not _is_package_installed(pkg)]
                if not packages_to_install:
                    return True

                # Actually install the missing packages
                return dependencies_check(packages_to_install)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        # Fallback to direct call if locking fails (e.g., permission issues)
        logging.getLogger(__name__).warning(f"Lock acquisition failed, falling back to direct install: {e}")
        return dependencies_check(packages)


# Helper to attempt installation and verify importability
def _install_and_verify(pkg: str, import_name: str):
    """Install a package expression and return True if the import succeeds."""
    try:
        if pkg == 'onnxruntime-gpu':
            pkg = 'onnxruntime'
        __import__(import_name)
        return True
    except ImportError:
        if _safe_dependencies_check([pkg]):
            try:
                __import__(import_name)
                return True
            except ImportError:
                return False
        return False


# Runtime gating for optional OCR bootstrap (default OFF), and never on Jetson
_ENABLE_OCR_BOOTSTRAP = os.getenv("MATRICE_ENABLE_OCR_BOOTSTRAP", "0")
_IS_JETSON = (platform.machine().lower() in ("aarch64", "arm64"))

print("*******************************Deployment ENV Info**********************************")
print(f"ENABLE_JETSON_PIP_SETTINGS: {_ENABLE_OCR_BOOTSTRAP}") #0 if OFF, 1 if ON, this will be set to 1 in jetson byom codebase.
print(f"IS_JETSON_ARCH?: {_IS_JETSON}") #True if Jetson, False otherwise
print("*************************************************************************************")

if not int(_ENABLE_OCR_BOOTSTRAP) and not _IS_JETSON:
    # Install base dependencies first (with file locking)
    _safe_dependencies_check(base)

    if not _safe_dependencies_check(["opencv-python"]):
        _safe_dependencies_check(["opencv-python-headless"])

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
from server.server import MatriceDeployServer  # noqa: E402
from server.server import MatriceDeployServer as MatriceDeploy  # noqa: E402 # Keep this for backwards compatibility
from server.inference_interface import InferenceInterface  # noqa: E402
from server.proxy_interface import MatriceProxyInterface  # noqa: E402

__all__ = [
    "MatriceDeploy",
    "MatriceDeployServer",
    "InferenceInterface",
    "MatriceProxyInterface",
]