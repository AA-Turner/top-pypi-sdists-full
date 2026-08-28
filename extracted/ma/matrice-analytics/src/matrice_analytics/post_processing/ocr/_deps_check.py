"""Pre-flight deps check that makes ORT expose a GPU provider when possible.

Runs at OCR-package import time (from ``__init__.py``) so the environment is
repaired *before* :class:`LicensePlateRecognizer` is instantiated. Reuses the
existing ``matrice_common.utils.dependencies_check`` (which serializes pip
across worker processes via a venv-keyed file lock) for the actual install
work; this module adds the GPU-specific repair sequence:

* detect the ``onnxruntime`` + ``onnxruntime-gpu`` dual-install state that
  yields ``['AzureExecutionProvider', 'CPUExecutionProvider']`` (the
  CPU-only wheel clobbers the GPU one at the shared ``onnxruntime/``
  import path), and uninstall plain ``onnxruntime`` so the GPU wheel wins,
* ensure ``onnxruntime-gpu`` is installed,
* re-import onnxruntime and re-check providers.

The function never raises -- it returns the final providers list so callers
can pick ``device='cuda'`` vs ``device='auto'`` based on what's actually
available.
"""

from __future__ import annotations

import importlib
import logging
import os
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import List

_LOGGER = logging.getLogger(__name__)

_GPU_PROVIDERS = ("TensorrtExecutionProvider", "CUDAExecutionProvider")
_CPU_PACKAGE = "onnxruntime"
_GPU_PACKAGE = "onnxruntime-gpu"

_PREFERRED_PROVIDER_ORDER = (
    "TensorrtExecutionProvider",
    "CUDAExecutionProvider",
    "CPUExecutionProvider",
)


def resolve_auto_providers(available, model_name, logger):
    """Pick ORT providers for ``device='auto'`` and warn on CPU fallback.

    Used by :class:`LicensePlateRecognizer` so the auto-mode CPU fallback is
    surfaced as a WARNING (not INFO). Exposed here so it's testable without
    pulling in onnxruntime/fast_plate_ocr at import time.
    """
    providers = [p for p in _PREFERRED_PROVIDER_ORDER if p in available]
    if not providers:
        providers = list(available) if available else ["CPUExecutionProvider"]
    if not any(p in providers for p in _GPU_PROVIDERS):
        logger.warning(
            "device='auto' but no GPU provider in available=%s; falling back to CPU. model_name=%s",
            available,
            model_name,
        )
    return providers


def _is_installed(package: str) -> bool:
    """True if ``package`` resolves to a version via importlib metadata."""
    try:
        version(package)
        return True
    except PackageNotFoundError:
        return False


def _get_providers() -> List[str]:
    """Return current ORT providers, reloading the module to pick up changes."""
    try:
        ort = importlib.import_module("onnxruntime")
        ort = importlib.reload(ort)
        return list(ort.get_available_providers())
    except Exception as exc:  # pragma: no cover - import failure path
        _LOGGER.warning("Could not import onnxruntime to check providers: %s", exc)
        return []


def _has_gpu_provider(providers: List[str]) -> bool:
    return any(p in providers for p in _GPU_PROVIDERS)


def _pip_uninstall(package: str) -> bool:
    """Run ``pip uninstall -y <package>``. Returns True on success."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", package],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _LOGGER.info("Uninstalled %s", package)
        return True
    except (subprocess.CalledProcessError, OSError) as exc:
        _LOGGER.warning("Failed to uninstall %s: %s", package, exc)
        return False


def _pip_force_reinstall(package: str) -> bool:
    """Run ``pip install --force-reinstall --no-deps <package>``. Returns True on success.

    ``--no-deps`` keeps the existing numpy/transitive versions intact so we
    don't trigger the cascading-reinstall problem that started this whole
    mess.
    """
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--force-reinstall",
                "--no-deps",
                package,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _LOGGER.info("Force-reinstalled %s", package)
        return True
    except (subprocess.CalledProcessError, OSError) as exc:
        _LOGGER.warning("Failed to force-reinstall %s: %s", package, exc)
        return False


def ensure_onnxruntime_gpu_available() -> List[str]:
    """Best-effort: make sure ORT exposes a GPU provider. Returns providers list.

    Never raises. Safe to call multiple times -- early-returns when a GPU
    provider is already visible.

    Defense-in-depth: the canonical repair runs at Python ``site``-init via
    ``_matrice_ort_bootstrap`` (installed by the ``.pth`` shipped with
    py_analytics). This function still runs at OCR package import time so
    we recover gracefully if the ``.pth`` was bypassed (e.g. ``python -S``
    or an environment where py_analytics is on ``PYTHONPATH`` but wasn't
    pip-installed).
    """
    try:
        # If the .pth bootstrap already ran AND ORT now shows a GPU
        # provider, this is a millisecond-fast no-op path.
        try:
            import _matrice_ort_bootstrap as _bootstrap

            bootstrap_done = getattr(_bootstrap, "_ORT_BOOTSTRAP_DONE", False)
        except ImportError:
            bootstrap_done = False
        if bootstrap_done:
            providers = _get_providers()
            if _has_gpu_provider(providers):
                _LOGGER.info(
                    "ORT GPU provider already visible (site .pth bootstrap ran): %s",
                    providers,
                )
                return providers
            _LOGGER.warning(
                "Site .pth bootstrap completed but ORT still %s; falling through to in-package repair.",
                providers,
            )
        return _ensure_inner()
    except Exception as exc:  # pragma: no cover - defensive
        _LOGGER.warning("ensure_onnxruntime_gpu_available unexpected error: %s", exc)
        return []


def _ensure_inner() -> List[str]:
    providers = _get_providers()
    if _has_gpu_provider(providers):
        _LOGGER.info("ORT already has GPU provider: %s", providers)
        return providers

    cpu_installed = _is_installed(_CPU_PACKAGE)
    gpu_installed = _is_installed(_GPU_PACKAGE)
    repaired = False

    # State 1: both installed -> the CPU wheel clobbered the GPU wheel's shared
    # libs at the same import path. Uninstall the CPU package and reinstall
    # onnxruntime-gpu with --force-reinstall so any shared-lib files removed
    # by the uninstall are restored.
    if cpu_installed and gpu_installed:
        _LOGGER.warning(
            "Detected both '%s' and '%s' installed; removing CPU package and "
            "reinstalling GPU package so GPU providers become visible.",
            _CPU_PACKAGE,
            _GPU_PACKAGE,
        )
        if _pip_uninstall(_CPU_PACKAGE):
            _pip_force_reinstall(_GPU_PACKAGE)
            repaired = True

    # State 2: onnxruntime-gpu not installed -> install via the shared helper
    # (which uses the matrice_common cross-process install lock).
    if not _is_installed(_GPU_PACKAGE):
        try:
            from matrice_common.utils import dependencies_check

            dependencies_check(_GPU_PACKAGE)
            repaired = True
        except Exception as exc:
            _LOGGER.warning(
                "matrice_common.dependencies_check('%s') failed: %s",
                _GPU_PACKAGE,
                exc,
            )
        # If plain onnxruntime is still around after the install, remove it
        # and force-reinstall the GPU wheel one more time.
        if _is_installed(_CPU_PACKAGE) and _is_installed(_GPU_PACKAGE):
            _pip_uninstall(_CPU_PACKAGE)
            _pip_force_reinstall(_GPU_PACKAGE)

    providers = _get_providers()
    if _has_gpu_provider(providers):
        _LOGGER.info("ORT GPU providers visible after repair: %s", providers)
        return providers

    # In-process providers cache may be stale (Python can't unload the already-
    # loaded onnxruntime C extension via importlib.reload), so the repair only
    # takes effect at the next process restart. Log a clear notice so ops know
    # the disk state is fixed even if this process keeps running on CPU.
    if repaired:
        _LOGGER.warning(
            "Pip-level repair completed but in-process ORT providers still %s; "
            "the fix will take effect after the next process restart.",
            providers,
        )
    else:
        _LOGGER.warning(
            "ORT still has no GPU provider after repair attempt. "
            "providers=%s onnxruntime_installed=%s onnxruntime_gpu_installed=%s "
            "LD_LIBRARY_PATH=%r cuda_lib_dir_exists=%s",
            providers,
            _is_installed(_CPU_PACKAGE),
            _is_installed(_GPU_PACKAGE),
            os.environ.get("LD_LIBRARY_PATH", ""),
            os.path.isdir("/usr/local/cuda/lib64"),
        )
    return providers


_CACHED_ORT_PROVIDERS = None


def get_ort_providers() -> List[str]:
    """Cached available-ORT-provider list (runs the GPU repair pre-flight once).

    Replaces the old module-level ``fast_plate_ocr_py38.ORT_PROVIDERS`` constant:
    callers use it to filter their preferred provider order down to what ORT can
    actually bind. Computed lazily and memoized so the repair runs at most once
    per process.
    """
    global _CACHED_ORT_PROVIDERS
    if _CACHED_ORT_PROVIDERS is None:
        _CACHED_ORT_PROVIDERS = ensure_onnxruntime_gpu_available()
    return _CACHED_ORT_PROVIDERS
