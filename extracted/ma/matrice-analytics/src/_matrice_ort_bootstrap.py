"""ORT pip-repair bootstrap that runs at Python ``site``-init time.

Triggered by ``matrice_analytics_ort_bootstrap.pth`` installed at the
site-packages root. Because this module is a **top-level** module (not
inside the ``matrice_analytics`` package), importing it does NOT trigger
``matrice_analytics/__init__.py`` -- which is critical, since that
package's eager submodule imports include ``onnxruntime``.

What this module does, in order:

1. Read ``importlib.metadata.version("onnxruntime")`` and
   ``version("onnxruntime-gpu")`` to detect the dual-install state baked
   into ``aiforeveryone/inference-pipeline:h100-trt10``. No
   ``import onnxruntime`` -- so the broken CPU-only shared libs never
   get loaded into the process.
2. If dual-installed, ``pip uninstall -y onnxruntime`` then
   ``pip install --force-reinstall --no-deps onnxruntime-gpu``.
3. Set ``_ORT_BOOTSTRAP_DONE`` / ``_ORT_BOOTSTRAP_REPAIRED`` sentinels
   for downstream code to consult.
4. Catch every exception at the outermost level -- a broken bootstrap
   must not break Python startup.

After this returns control, the FIRST ``import onnxruntime`` in the
process (typically at
``ml-codebases/yolo_code_base/inference/config.py:91``) sees the freshly
repaired install and exposes ``TensorrtExecutionProvider`` +
``CUDAExecutionProvider``.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version

_LOGGER = logging.getLogger(__name__)

_CPU_PACKAGE = "onnxruntime"
_GPU_PACKAGE = "onnxruntime-gpu"

# Re-entry guard env var. We set this before any pip subprocess we spawn
# and bail at the very top of the bootstrap if it's already set. Without
# this, the bootstrap fork-bombs itself: .pth runs bootstrap -> bootstrap
# spawns `python -m pip uninstall` -> that subprocess is a fresh python ->
# its site-init runs the .pth -> bootstrap runs again -> spawns another
# pip -> infinite recursion.
_REENTRY_ENV = "_MATRICE_ORT_BOOTSTRAP_ACTIVE"

# Sentinels (read by post_processing.ocr._deps_check
# for short-circuit logic).
_ORT_BOOTSTRAP_DONE: bool = False
_ORT_BOOTSTRAP_REPAIRED: bool = False


def _is_installed(package: str) -> bool:
    try:
        version(package)
        return True
    except PackageNotFoundError:
        return False


def _subprocess_env() -> dict:
    """Build env for pip subprocesses with the re-entry guard set."""
    env = os.environ.copy()
    env[_REENTRY_ENV] = "1"
    return env


def _pip_uninstall(package: str) -> bool:
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", package],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=_subprocess_env(),
        )
        _LOGGER.info("ORT bootstrap: uninstalled %s", package)
        return True
    except (subprocess.CalledProcessError, OSError) as exc:
        _LOGGER.warning("ORT bootstrap: failed to uninstall %s: %s", package, exc)
        return False


def _pip_force_reinstall(package: str) -> bool:
    """``pip install --force-reinstall --no-deps`` (no transitive churn)."""
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
            env=_subprocess_env(),
        )
        _LOGGER.info("ORT bootstrap: force-reinstalled %s", package)
        return True
    except (subprocess.CalledProcessError, OSError) as exc:
        _LOGGER.warning("ORT bootstrap: failed to force-reinstall %s: %s", package, exc)
        return False


def _repair_dual_install() -> bool:
    """If both onnxruntime and onnxruntime-gpu are installed, fix it.

    Returns True if a repair was performed, False if nothing was needed.
    Never raises.
    """
    if not (_is_installed(_CPU_PACKAGE) and _is_installed(_GPU_PACKAGE)):
        return False

    _LOGGER.warning(
        "ORT bootstrap: both '%s' and '%s' installed; the CPU wheel clobbers "
        "the GPU wheel's shared libs. Uninstalling CPU package and "
        "force-reinstalling GPU package so the first 'import onnxruntime' "
        "in this process exposes TensorrtExecutionProvider + "
        "CUDAExecutionProvider.",
        _CPU_PACKAGE,
        _GPU_PACKAGE,
    )
    _pip_uninstall(_CPU_PACKAGE)
    _pip_force_reinstall(_GPU_PACKAGE)
    return True


def _should_skip() -> bool:
    """Return True if this Python invocation is itself a pip subprocess.

    The .pth runs the bootstrap at site-init on EVERY Python invocation,
    including the ``python -m pip uninstall`` / ``python -m pip install``
    subprocesses spawned by the bootstrap itself. Without a guard, that
    fork-bombs (bootstrap -> pip subprocess -> .pth -> bootstrap -> ...).

    Two signals are enough:
      * ``_MATRICE_ORT_BOOTSTRAP_ACTIVE`` env var set by our own helpers
        before they spawn pip -- the subprocess inherits it.
      * ``sys.argv`` looking like a pip invocation (defensive: covers any
        path where our env var wasn't propagated, e.g. ``pip`` running
        without going through subprocess.run from us).
    """
    if os.environ.get(_REENTRY_ENV) == "1":
        return True
    argv0 = (sys.argv[0] or "").lower()
    if "pip" in argv0:
        return True
    if len(sys.argv) > 1 and any("pip" in str(a).lower() for a in sys.argv[:3]):
        return True
    return False


def _run_bootstrap() -> None:
    """Entry called at .pth-import time. Never raises."""
    global _ORT_BOOTSTRAP_DONE, _ORT_BOOTSTRAP_REPAIRED
    if _should_skip():
        # Inside a pip subprocess; the parent bootstrap is doing the work.
        _ORT_BOOTSTRAP_DONE = True
        return
    try:
        _ORT_BOOTSTRAP_REPAIRED = _repair_dual_install()
    except Exception as exc:  # pragma: no cover - last-resort guard
        _LOGGER.warning("ORT bootstrap failed (continuing): %s", exc)
    finally:
        _ORT_BOOTSTRAP_DONE = True


_run_bootstrap()
