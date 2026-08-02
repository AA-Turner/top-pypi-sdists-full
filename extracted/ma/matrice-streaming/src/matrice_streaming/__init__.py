"""Module providing __init__ functionality."""

# SCALE-002 RC: resource_tracker semaphore-unlink race fix. Must run BEFORE
# any mp.Queue/Lock is touched. Shared implementation lives in _mp_patch so the
# NVDEC module applies the identical patch without a copy-pasted body.
from matrice_streaming._mp_patch import install_resource_tracker_patch as _matrice_install_rt_patch

_matrice_install_rt_patch()

# SCALE-002: also install sitecustomize.py so the resource_tracker SUBPROCESS
# (a separate Python interpreter started via `python -c "from
# multiprocessing.resource_tracker import main; main(N)"`) ALSO applies the
# patch at its startup. Without this, the subprocess's _CLEANUP_FUNCS is
# unchanged and it still sem_unlinks on hard-kill -> SemLock._rebuild
# FileNotFoundError in the next spawned worker.
import os as _matrice_os

_matrice_sc_path = None
for _matrice_sp in __import__("site").getsitepackages():
    _candidate = _matrice_os.path.join(_matrice_sp, "sitecustomize.py")
    if _matrice_os.path.isdir(_matrice_sp) and _matrice_os.access(_matrice_sp, _matrice_os.W_OK):
        _matrice_sc_path = _candidate
        break
if _matrice_sc_path:
    _matrice_sc_body = '''"""SCALE-002 sitecustomize: resource_tracker semaphore-unlink no-op.
Auto-imported by every Python interpreter at startup. Installed by
matrice_streaming/__init__.py — safe to re-run.
"""
try:
    import multiprocessing.resource_tracker as _rt
    if not getattr(_rt, "_matrice_sem_unlink_patch_installed", False):
        _orig_register = _rt.register
        _orig_unregister = _rt.unregister
        def _safe_register(name, rtype):
            if rtype == "semaphore":
                return
            return _orig_register(name, rtype)
        def _safe_unregister(name, rtype):
            if rtype == "semaphore":
                return
            return _orig_unregister(name, rtype)
        _rt.register = _safe_register
        _rt.unregister = _safe_unregister
        if "semaphore" in getattr(_rt, "_CLEANUP_FUNCS", {}):
            _rt._CLEANUP_FUNCS["semaphore"] = lambda name: None
        _rt._matrice_sem_unlink_patch_installed = True
except Exception:
    pass
'''
    try:
        _existing = ""
        if _matrice_os.path.exists(_matrice_sc_path):
            with open(_matrice_sc_path) as _f:
                _existing = _f.read()
        if "_matrice_sem_unlink_patch_installed" not in _existing:
            # APPEND rather than truncate: a host may already ship a
            # sitecustomize.py (proxy config, coverage hooks, corporate
            # telemetry). Opening in "w" would silently destroy it. Preserve
            # any existing content and add our patch after it.
            with open(_matrice_sc_path, "a") as _f:
                if _existing and not _existing.endswith("\n"):
                    _f.write("\n")
                _f.write(_matrice_sc_body)
    except Exception:  # noqa: BLE001  # nosec B110 - non-fatal best-effort
        pass
del _matrice_os, _matrice_sc_path

import logging  # noqa: E402  — SCALE-002 patch must run before these
import multiprocessing  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402

# Only run dependency checks in the main process, NOT in spawned child processes
# (ProcessPoolExecutor workers). Child processes re-import modules which would
# trigger pip install commands, causing crashes with BrokenProcessPool errors.
_is_main_process = multiprocessing.parent_process() is None


def _serialize_install(install_fn, *args, **kwargs):
    """Run a pip-install-style callable while holding an exclusive
    advisory file lock on the venv.

    Why: when multiple independent main-process Python interpreters share
    the same venv (e.g. several gateway instances on one host, or a
    subprocess.Popen-launched helper), concurrent calls to
    `dependencies_check` can race inside pip's resolver / wheel installer
    and corrupt the site-packages tree (half-written .dist-info, partial
    .pth files, BrokenProcessPool downstream). The `_is_main_process`
    gate only protects against mp-children; it does NOT protect against
    sibling interpreters — those all see `parent_process() is None`.

    Implementation: an exclusive `fcntl.flock` on a lockfile keyed to
    `sys.prefix` (the active venv root). Linux/macOS only — Windows
    falls back to no-op (which is consistent with the rest of the GPU
    streaming stack being Linux-only).
    """
    lock_dir = os.path.join(sys.prefix, "var", "lock")
    try:
        os.makedirs(lock_dir, exist_ok=True)
    except OSError:
        # /usr venvs may be read-only; fall back to a per-user dir.
        lock_dir = os.path.join(os.path.expanduser("~"), ".cache", "matrice_streaming")
        os.makedirs(lock_dir, exist_ok=True)
    lock_path = os.path.join(lock_dir, "matrice_streaming_deps.lock")

    try:
        import fcntl  # POSIX-only
    except ImportError:
        # Windows / no-fcntl platform — best-effort, no cross-process serialization.
        logging.getLogger(__name__).debug("fcntl unavailable; running dependencies_check without cross-process lock")
        return install_fn(*args, **kwargs)

    fd = None
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
    except OSError as exc:
        if fd is not None:
            os.close(fd)
        logging.getLogger(__name__).warning(
            "Could not acquire dependencies install lock at %s (%s); running without cross-process serialization",
            lock_path,
            exc,
        )
        return install_fn(*args, **kwargs)

    try:
        return install_fn(*args, **kwargs)
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


# SECURITY (supply-chain): installing packages at import time resolves to
# whatever version is newest on the index at that moment, giving a compromised
# or typosquatted upstream an execution path with no version gate. These
# packages are pre-installed in the baked runtime image, so the runtime
# bootstrap is DISABLED by default and only runs when the operator explicitly
# opts in with MATRICE_STREAMING_INSTALL_DEPS=1 (e.g. bare dev checkouts).
_install_deps_at_import = os.environ.get("MATRICE_STREAMING_INSTALL_DEPS") == "1"

if _is_main_process and _install_deps_at_import:
    try:
        from matrice_common.utils import dependencies_check
    except ImportError:
        dependencies_check = None  # type: ignore[assignment]

    if dependencies_check is not None:
        # Pin versions to APPROVED_DEPS where audited so behaviour is
        # reproducible across environments. Packages without an approved
        # pin are left unpinned and tracked separately.
        base = [
            "httpx==0.28.1",
            "fastapi",
            "uvicorn",
            "pillow==9.5.0",
            "confluent_kafka[snappy]",
            "aiokafka",
            "aiohttp==3.13.4",
            "filterpy",
            "scipy",
            "scikit-learn",
            "matplotlib==3.9.4",
            "scikit-image",
            "python-snappy",
            "pyyaml==6.0.3",
            "imagehash",
            "psutil",
        ]

        # Install base dependencies under the cross-process lock.
        _serialize_install(dependencies_check, base)

        try:
            import cv2  # noqa: F401
        except ImportError:
            # Always pull opencv-python-headless on ImportError. The full
            # opencv-python wheel needs system X11 libs (libxcb.so.1, etc.)
            # that aren't present in the CI runner image (or in most
            # server-side deploys), so importing cv2 fails at runtime even
            # when opencv-python's metadata shows installed. The headless
            # variant has the same API surface minus the GUI bits and no
            # system-lib deps.
            _serialize_install(dependencies_check, ["opencv-python-headless"])


# Lazily expose LocalDecoder at the top level (`from matrice_streaming import
# LocalDecoder`) without importing it at package load — it requires cupy /
# PyNvVideoCodec, which are absent on CPU-only hosts where the gateway still
# needs to import. PEP 562 module __getattr__ defers the import to first access.
def __getattr__(name):  # noqa: D401
    if name == "LocalDecoder":
        from .local_decoder import LocalDecoder

        return LocalDecoder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
