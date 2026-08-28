"""Runtime auto-creation / self-heal of the isolated OCR venv.

On most images the OCR venv is pre-baked at build time and pointed at by
``MATRICE_OCR_PYTHON`` (see ``Dockerfile.inference-pipeline-jetson-thor``). On
images where it is *not* pre-baked but in-process OCR is broken -- notably the
Blackwell PRO 6000 image, where ``onnxruntime`` (CPU) and ``onnxruntime-gpu``
are installed into the same numpy>=2 env so ORT exposes no GPU provider, and
the container runs nonroot so the in-place ``_deps_check`` repair cannot write
to system site-packages -- this module creates the isolated venv at runtime in
a *writable* location, installs the right deps, validates it, and returns the
venv interpreter path. The OCR subprocess client then runs the worker against
it.

This module is **stdlib-only**. It is imported by the parent inference process
(which on these images needs numpy>=2 for cupy) and must therefore NEVER import
``onnxruntime`` or ``fast_plate_ocr`` -- those live only inside the isolated
venv and are exercised through subprocesses (``python -c`` probes and the
worker). :func:`ensure_ocr_venv` never raises; on any failure it returns
``None`` and the caller falls back to in-process CPU OCR.
"""

from __future__ import annotations

import collections
import contextlib
import logging
import os
import platform
import subprocess  # nosec B404 - fixed argv, no shell, used to drive pip/venv
import sys
import threading
from typing import List, Optional

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "cct-s-v1-global-model"
_PRIMARY_VENV_DIR = "/opt/ocr-venv"
_GPU_PLATFORMS = ("gpu", "thor", "orin")
_KNOWN_PLATFORMS = ("gpu", "thor", "orin", "cpu")

# (numpy_pin, ort_pkg, ort_version, extra_index_url, fast_plate_spec). Any field
# may be None. ``fast_plate_spec`` deliberately avoids the ``[onnx-gpu]`` extra
# on GPU rows so it can't pull a CPU ``onnxruntime`` wheel that would shadow the
# GPU one at the shared import path (the exact failure on the Blackwell image).
WheelSpec = collections.namedtuple(
    "WheelSpec",
    "numpy_pin ort_pkg ort_version extra_index_url fast_plate_spec",
)

_WHEEL_SPECS = {
    # x86_64 CUDA GPU (e.g. Blackwell PRO 6000): the x86 onnxruntime-gpu wheel
    # is numpy-2 ABI compatible, so no numpy pin is needed. Isolation alone
    # sidesteps the dual-install clobber in the main env.
    # fast-plate-ocr is PINNED (never left unbounded): an unpinned spec let a
    # surprise 1.1.0 release land via the deploy's pip --upgrade and break OCR.
    # The OCR worker + use-case now handle both upstream run() shapes (the
    # <=1.0.x (texts, confs) tuple and the >=1.1.0 list[PlatePrediction]) via
    # _ocr_ipc.normalize_run_result, so this pin is for reproducibility, not
    # API compatibility -- bump it deliberately after testing.
    "gpu": WheelSpec(None, "onnxruntime-gpu", None, None, "fast-plate-ocr==1.1.0"),
    # Jetson Thor (aarch64/cp312, CUDA 13): prebuilt onnxruntime-gpu is numpy<2.
    # Kept at 1.0.2 (the version validated on that stack); the code tolerates it.
    "thor": WheelSpec(
        "numpy<2",
        "onnxruntime-gpu",
        "==1.24.0",
        "https://pypi.jetson-ai-lab.io/sbsa/cu130/+simple/",
        "fast-plate-ocr==1.0.2",
    ),
    # Jetson Orin (aarch64): jetson onnxruntime-gpu is numpy<2.
    "orin": WheelSpec("numpy<2", "onnxruntime-gpu", None, None, "fast-plate-ocr==1.1.0"),
    # No GPU: CPU onnxruntime; the probe only asserts import, not a GPU provider.
    "cpu": WheelSpec(None, "onnxruntime", None, None, "fast-plate-ocr[onnx]==1.1.0"),
}

# One slow-path bootstrap attempt per target dir per process. Repeated misses
# (e.g. no network) must not re-run pip on every camera/use-case.
_ATTEMPTED: set = set()
_ATTEMPTED_LOCK = threading.Lock()

# The probe runs inside the venv: import the OCR stack and (for GPU platforms)
# require a GPU execution provider. ``sys.argv[1]`` carries the require-gpu flag.
_PROBE_SRC = (
    "import sys\n"
    "try:\n"
    "    import onnxruntime as ort\n"
    "    import fast_plate_ocr  # noqa: F401\n"
    "    provs = list(ort.get_available_providers())\n"
    "except Exception as e:\n"
    "    sys.stderr.write('probe-import-fail: %r\\n' % (e,))\n"
    "    sys.exit(2)\n"
    "require_gpu = (len(sys.argv) > 1 and sys.argv[1] == '1')\n"
    "gpu = [p for p in provs "
    "if p in ('TensorrtExecutionProvider', 'CUDAExecutionProvider')]\n"
    "if require_gpu and not gpu:\n"
    "    sys.stderr.write('probe-no-gpu: %r\\n' % (provs,))\n"
    "    sys.exit(3)\n"
    "sys.exit(0)\n"
)


# ---------------------------------------------------------------------------
# Path / platform resolution
# ---------------------------------------------------------------------------
def _is_creatable(path: str) -> bool:
    """True if ``path`` can be created: its first existing ancestor is writable."""
    p = os.path.abspath(path)
    while True:
        if os.path.exists(p):
            return os.access(p, os.W_OK)
        parent = os.path.dirname(p)
        if parent == p:
            return False
        p = parent


def _resolve_venv_dir() -> str:
    """Pick the venv directory: env override, else first writable candidate.

    Falls back to a ``$HOME`` path so a non-root container (no write to ``/opt``)
    still gets a usable location.
    """
    override = os.environ.get("MATRICE_OCR_VENV")
    if override:
        return override
    candidates = [
        _PRIMARY_VENV_DIR,
        os.path.join(os.path.expanduser("~"), ".matrice", "ocr-venv"),
        "/usr/src/workspace/.matrice-ocr-venv",
    ]
    for cand in candidates:
        if _is_creatable(cand):
            return cand
    # Nothing writable found; return the HOME candidate so creation surfaces a
    # clear error rather than silently using a read-only /opt.
    return candidates[1]


def _venv_python(venv_dir: str) -> str:
    return os.path.join(venv_dir, "bin", "python3")


def _detect_platform() -> str:
    """Resolve to one of gpu/thor/orin/cpu.

    Honors ``MATRICE_PLATFORM`` first; otherwise infers from CPU arch and CUDA
    presence (aarch64 -> orin; x86_64 -> gpu if a CUDA toolkit dir exists, else
    cpu).
    """
    env_val = os.environ.get("MATRICE_PLATFORM", "").strip().lower()
    if env_val in _KNOWN_PLATFORMS:
        return env_val

    machine = platform.machine().lower()
    if machine in ("aarch64", "arm64"):
        # Thor is identified by MATRICE_PLATFORM (handled above); default the
        # bare aarch64 case to the Orin jetson wheel family.
        return "orin"
    if os.path.isdir("/usr/local/cuda"):
        return "gpu"
    return "cpu"


def _wheel_spec(platform_key: str) -> WheelSpec:
    return _WHEEL_SPECS.get(platform_key, _WHEEL_SPECS["cpu"])


# ---------------------------------------------------------------------------
# Subprocess helpers (pip / venv / probe)
# ---------------------------------------------------------------------------
def _base_python() -> str:
    """Interpreter used to build the venv. Override via ``MATRICE_OCR_BASE_PYTHON``."""
    return os.environ.get("MATRICE_OCR_BASE_PYTHON") or sys.executable or "python3"


def _child_env() -> dict:
    """Env for venv subprocesses: route the hub cache at ``MATRICE_OCR_HOME``."""
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    ocr_home = os.environ.get("MATRICE_OCR_HOME")
    if ocr_home:
        env["HOME"] = ocr_home
    return env


def _probe_health(py_exe: str, require_gpu: bool, timeout: float = 120.0) -> bool:
    """Run the in-venv import/provider probe. Returns True iff it exits 0."""
    if not os.path.exists(py_exe):
        return False
    try:
        proc = subprocess.run(  # nosec B603 - fixed argv, no shell
            [py_exe, "-c", _PROBE_SRC, "1" if require_gpu else "0"],
            env=_child_env(),
            capture_output=True,
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        logger.warning("OCR venv health probe error: %s", exc)
        return False
    if proc.returncode != 0:
        logger.info(
            "OCR venv health probe failed (rc=%s): %s",
            proc.returncode,
            proc.stderr.decode(errors="replace").strip()[:300],
        )
        return False
    return True


def _pip_install(py_exe: str, args: List[str], timeout: Optional[float] = None) -> None:
    """``pip install --no-cache-dir <args>`` with the image's PIP_CONSTRAINT cleared.

    Clearing ``PIP_CONSTRAINT`` keeps the parent image's numpy pin (e.g.
    ``numpy==2.1.3``) from leaking into the isolated venv. Raises on failure.
    """
    env = _child_env()
    env["PIP_CONSTRAINT"] = ""
    subprocess.run(  # nosec B603 - fixed argv, no shell
        [py_exe, "-m", "pip", "install", "--no-cache-dir", *args],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def _create_venv(venv_dir: str, timeout: Optional[float] = None) -> None:
    """Create a fresh venv (no system-site-packages) and upgrade its installer.

    No ``--system-site-packages``: the parent env's broken/CPU onnxruntime must
    NOT leak in. Raises on failure.
    """
    subprocess.run(  # nosec B603 - fixed argv, no shell
        [_base_python(), "-m", "venv", venv_dir],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    _pip_install(_venv_python(venv_dir), ["--upgrade", "pip", "setuptools", "wheel"], timeout)


def _install_deps(py_exe: str, spec: WheelSpec, timeout: Optional[float] = None) -> None:
    """Install numpy/opencv, onnxruntime, and fast-plate-ocr per ``spec``."""
    np_pkgs: List[str] = []
    if spec.numpy_pin:
        np_pkgs.append(spec.numpy_pin)
    np_pkgs.append("opencv-python-headless>=4.9")
    _pip_install(py_exe, np_pkgs, timeout)

    ort_args = [spec.ort_pkg + (spec.ort_version or "")]
    if spec.extra_index_url:
        ort_args += ["--extra-index-url", spec.extra_index_url]
    _pip_install(py_exe, ort_args, timeout)

    _pip_install(py_exe, [spec.fast_plate_spec], timeout)


def _predownload_model(py_exe: str, model_name: str, timeout: Optional[float] = None) -> None:
    """Best-effort: warm the fast_plate_ocr hub cache so the worker hits no network."""
    src = f"from fast_plate_ocr.inference.hub import download_model; download_model(model_name={model_name!r})"
    try:
        subprocess.run(  # nosec B603 - fixed argv, no shell
            [py_exe, "-c", src],
            check=False,
            env=_child_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        logger.warning("OCR model pre-download skipped (%s); worker will fetch it", exc)


@contextlib.contextmanager
def _venv_lock(venv_dir: str):
    """Serialize venv creation across worker processes via an flock on a sibling file.

    Keyed to the *target* venv dir (not ``sys.prefix``). Degrades to a no-op if
    ``fcntl`` is unavailable or the lock file can't be created.
    """
    try:
        import fcntl
    except Exception:  # pragma: no cover - non-posix
        yield
        return

    lock_path = venv_dir.rstrip("/") + ".lock"
    fh = None
    try:
        os.makedirs(os.path.dirname(lock_path) or ".", exist_ok=True)
        fh = open(lock_path, "w")  # noqa: SIM115 - released in finally
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
    except OSError as exc:
        logger.warning("OCR venv lock unavailable (%s); proceeding without it", exc)
        if fh is not None:
            fh.close()
        fh = None
    try:
        yield
    finally:
        if fh is not None:
            try:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            except Exception:  # pragma: no cover - best effort
                pass
            fh.close()


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def ensure_ocr_venv(model_name: str = _DEFAULT_MODEL, timeout: float = 1800.0) -> Optional[str]:
    """Return a healthy isolated-OCR-venv python, creating/repairing it if needed.

    Fast path (no lock): an existing venv that passes the health probe is
    returned immediately. Slow path: acquire a cross-process lock, re-probe (a
    sibling may have just built it), then create the venv and install deps.
    Never raises -- returns ``None`` on any failure so the caller falls back to
    in-process OCR.
    """
    try:
        venv_dir = _resolve_venv_dir()
        py_exe = _venv_python(venv_dir)
        platform_key = _detect_platform()
        require_gpu = platform_key in _GPU_PLATFORMS

        if os.path.exists(py_exe) and _probe_health(py_exe, require_gpu):
            logger.info("OCR venv healthy at %s (platform=%s)", py_exe, platform_key)
            return py_exe

        with _ATTEMPTED_LOCK:
            if venv_dir in _ATTEMPTED:
                logger.info(
                    "OCR venv bootstrap already attempted for %s this process; not retrying.",
                    venv_dir,
                )
                return None
            _ATTEMPTED.add(venv_dir)

        spec = _wheel_spec(platform_key)
        with _venv_lock(venv_dir):
            # A sibling worker may have built it while we waited on the lock.
            if os.path.exists(py_exe) and _probe_health(py_exe, require_gpu):
                logger.info("OCR venv became healthy under lock: %s", py_exe)
                return py_exe
            logger.warning(
                "Bootstrapping OCR venv at %s (platform=%s, ort=%s%s)",
                venv_dir,
                platform_key,
                spec.ort_pkg,
                spec.ort_version or "",
            )
            if not os.path.exists(py_exe):
                _create_venv(venv_dir, timeout)
            _install_deps(py_exe, spec, timeout)
            _predownload_model(py_exe, model_name, timeout)

        if os.path.exists(py_exe) and _probe_health(py_exe, require_gpu):
            logger.info("OCR venv bootstrap succeeded: %s", py_exe)
            return py_exe
        logger.error(
            "OCR venv bootstrap completed but health probe still failing at %s; falling back to in-process OCR.",
            py_exe,
        )
        return None
    except Exception as exc:  # noqa: BLE001 - never propagate to the pipeline
        logger.warning("ensure_ocr_venv error (%s); falling back to in-process OCR.", exc)
        return None
