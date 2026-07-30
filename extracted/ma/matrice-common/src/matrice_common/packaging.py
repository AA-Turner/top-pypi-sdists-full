"""Pip dependency management helpers for the Matrice package.

Split out of ``utils.py``; re-exported from ``matrice_common.utils`` for
backward compatibility.

NOTE: ``dependencies_check`` and ``_install_package`` resolve their
patch-sensitive collaborators (``_is_package_installed``, ``_install_package``,
``subprocess``, ``version``) through the ``matrice_common.utils`` module
namespace. This keeps the historical patch targets
(``matrice_common.utils._is_package_installed`` etc.) effective after the
split, since sibling tests patch on that namespace.
"""

import logging
import os
import subprocess  # noqa: F401  (kept for `matrice_common.utils.subprocess` patch target)
import sys
from importlib.metadata import PackageNotFoundError, version  # noqa: F401
from typing import List, Union


def _utils():
    """Lazily resolve the ``matrice_common.utils`` shim module.

    Used so that test patches against ``matrice_common.utils.<name>`` are
    honored by the functions that now live here.
    """
    import matrice_common.utils as _u

    return _u


# Names this interpreter has already successfully installed — short-circuits
# in-process repeat calls without touching the cross-process lock.
_INSTALLED_THIS_PROCESS: set = set()


def _acquire_install_lock():
    """Acquire an exclusive cross-process file lock for pip install.

    Returns the fd holding the lock, or None if locking is unavailable
    (Windows / no fcntl / lockfile-create failure). Callers must pair a
    non-None return with `_release_install_lock(fd)` in a finally.

    Why: multiple sibling Python interpreters sharing one venv can race
    inside pip's wheel installer when each runs `dependencies_check` at
    import time, corrupting site-packages (.dist-info, .pth). The lock is
    keyed to the venv root (`sys.prefix`) so independent venvs stay
    independent.
    """
    lock_dir = os.path.join(sys.prefix, "var", "lock")
    try:
        os.makedirs(lock_dir, exist_ok=True)
    except OSError:
        lock_dir = os.path.join(os.path.expanduser("~"), ".cache", "matrice")
        try:
            os.makedirs(lock_dir, exist_ok=True)
        except OSError as exc:
            logging.warning(
                "Could not create install lock dir at %s (%s); running pip without cross-process serialization",
                lock_dir,
                exc,
            )
            return None
    lock_path = os.path.join(lock_dir, "matrice_deps.lock")

    try:
        import fcntl  # POSIX-only
    except ImportError:
        logging.debug("fcntl unavailable; running pip install without cross-process lock")
        return None

    fd = None
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
        return fd
    except OSError as exc:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass
        logging.warning(
            "Could not acquire install lock at %s (%s); running pip without cross-process serialization",
            lock_path,
            exc,
        )
        return None


def _release_install_lock(fd):
    """Release a lock acquired by `_acquire_install_lock` and close its fd."""
    if fd is None:
        return
    try:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_UN)
    except (ImportError, OSError):
        pass
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def _is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        _utils().version(package_name.replace("-", "_"))
        return True
    except (ImportError, OSError):
        return False


def _install_package(package_name):
    """Install a package via `pip install --upgrade`, serialized cross-process.

    Holds an exclusive venv-keyed file lock for the duration of the pip
    subprocess so sibling interpreters cannot race inside the wheel
    installer. Re-checks installed state inside the critical section so
    a sibling that just finished installing the same package
    short-circuits this caller.
    """
    if package_name in _INSTALLED_THIS_PROCESS:
        return True
    # Resolve the lock helpers through the matrice_common.utils namespace so
    # test patches against matrice_common.utils._acquire_install_lock /
    # _release_install_lock remain effective after the utils.py split.
    lock_fd = _utils()._acquire_install_lock()
    try:
        if _utils()._is_package_installed(package_name):
            _INSTALLED_THIS_PROCESS.add(package_name)
            return True
        # SECURITY (supply-chain): runtime pip installs pull an unpinned package
        # from whatever index the environment points at and execute its setup
        # hooks in-process. Required dependencies are baked into the service
        # image, so by default we do NOT install at runtime — we warn and report
        # the package as missing. Set MATRICE_ALLOW_RUNTIME_PIP=1 to explicitly
        # opt back into runtime installation (without --upgrade, so an already
        # satisfied pin is never silently bumped).
        if os.environ.get("MATRICE_ALLOW_RUNTIME_PIP", "").lower() not in ("1", "true", "yes"):
            logging.warning(
                "Package %s is not installed and runtime pip install is disabled "
                "(set MATRICE_ALLOW_RUNTIME_PIP=1 to enable). Expected to be provided by the image.",
                package_name,
            )
            return False
        try:
            _utils().subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logging.info("Successfully installed %s", package_name)
            _INSTALLED_THIS_PROCESS.add(package_name)
            return True
        except subprocess.CalledProcessError as exc:
            logging.exception("Failed to install %s: %s", package_name, exc)
            return False
        except Exception as e:
            logging.exception("Unexpected error installing %s: %s", package_name, str(e))
            return False
    finally:
        _utils()._release_install_lock(lock_fd)


def dependencies_check(package_names: Union[List[str], str]) -> bool:
    """Check and (optionally) install required dependencies. NEVER raises.

    Each entry is either a bare package name or a dict declaring a version mode:

      "httpx"
          Install the latest ONLY if the package is entirely missing; if any
          version is already present (e.g. shipped by the Docker image / env),
          leave it untouched.
      {"name": "httpx", "suggested": "0.28.1"}
          Same "install-only-if-missing" behaviour, but install ==0.28.1 when
          absent. Image/env-safe: a version the image already provides is never
          overridden — the suggestion is a fallback for standalone installs.
      {"name": "cryptography", "exact": "48.0.1"}
          Force ==48.0.1 regardless of what is installed (may conflict with a
          system/Debian-managed package — use only when the exact version is
          truly required).

    Any per-entry failure is logged as a warning and swallowed — a missing or
    un-installable dependency must never crash the importing service.
    """
    if not isinstance(package_names, list):
        package_names = [package_names]
    success = True
    for entry in package_names:
        try:
            if isinstance(entry, dict):
                name = entry.get("name")
                exact = entry.get("exact")
                suggested = entry.get("suggested")
            else:
                name, exact, suggested = entry, None, None
            if not name:
                continue

            if exact:
                # Force the exact version regardless of what is installed.
                if not _utils()._install_package(f"{name}=={exact}"):
                    success = False
                continue

            if _utils()._is_package_installed(name):
                # Present at some version — do NOT override (image/env owns it).
                logging.debug("Package %s already present; skipping", name)
                continue

            # Missing: install the suggested version, or the latest if none.
            spec = f"{name}=={suggested}" if suggested else name
            if not _utils()._install_package(spec):
                success = False
        except Exception as exc:  # noqa: BLE001 - dependency check must never raise
            logging.warning(
                "dependencies_check: skipping %r (%s); continuing", entry, exc
            )
            success = False
    return success
