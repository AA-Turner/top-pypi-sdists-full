"""Shared CLI test fixtures."""

from __future__ import annotations

import os

_NULL_KEYRING_BACKEND = "keyring.backends.null.Keyring"

# Set before any test dependency can initialize the OS backend.
os.environ["PYTHON_KEYRING_BACKEND"] = _NULL_KEYRING_BACKEND

import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402
from unittest.mock import patch  # noqa: E402

import keyring  # noqa: E402
import keyring.backends.null  # noqa: E402
import pytest  # noqa: E402

from runlayer_cli.credential_store import reset_credential_store  # noqa: E402
from runlayer_cli.hook_install.browser_extension import (  # noqa: E402
    _SKIP_NO_EXTENSION_ID,
    BrowserExtensionResult,
)
from runlayer_cli.runtime import reset_aiwatch_runtime  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _force_null_keyring():
    """Replace any initialized in-process keyring backend."""
    keyring.set_keyring(keyring.backends.null.Keyring())


@pytest.fixture(scope="session", autouse=True)
def _guard_subprocess_keyring():
    """Guard child processes that supply their own environment."""
    original_init = subprocess.Popen.__init__

    def guarded_init(self, *args, **kwargs):
        if "env" in kwargs and kwargs["env"] is not None:
            guarded_env = dict(kwargs["env"])
            guarded_env.setdefault("PYTHON_KEYRING_BACKEND", _NULL_KEYRING_BACKEND)
            kwargs["env"] = guarded_env
        elif len(args) > 10 and args[10] is not None:
            guarded_env = dict(args[10])
            guarded_env.setdefault("PYTHON_KEYRING_BACKEND", _NULL_KEYRING_BACKEND)
            args = (*args[:10], guarded_env, *args[11:])
        return original_init(self, *args, **kwargs)

    with patch.object(subprocess.Popen, "__init__", new=guarded_init):
        yield


@pytest.fixture(autouse=True)
def isolated_scan_run_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Path:
    """Point the scan run lock at a per-test dir.

    run_lock binds get_runlayer_dir at import time, so ~/.runlayer isolation
    that patches runlayer_cli.paths (or overrides HOME) never reaches it:
    every in-process ``scan`` invocation flocks the machine's real
    ``~/.runlayer/aiwatch-scan.lock``. Concurrent lock holders — xdist e2e
    workers, or a real AI Watch scan on the host — then make the losing scan
    exit 0 with only ``scan_skipped_lock_busy`` logged, failing output
    assertions. Regression tests: ``tests/e2e/scan/test_scan_lock_isolation.py``.
    """
    lock_dir = tmp_path / ".runlayer-scan-lock"
    monkeypatch.setattr(
        "runlayer_cli.scan.run_lock.get_runlayer_dir", lambda: lock_dir
    )
    return lock_dir


@pytest.fixture(autouse=True)
def _reset_aiwatch_runtime():
    """Clear the aiwatch runtime flag around every test.

    ``runtime.mark_aiwatch_runtime`` sets a process-global flag at the aiwatch
    entrypoints. Any test that drives ``aiwatch.main`` / ``hook.__main__.main``
    in-process would otherwise leak the flag into later tests and flip
    ``config.load_config``/``save_config`` behavior.
    """
    reset_aiwatch_runtime()
    yield
    reset_aiwatch_runtime()


@pytest.fixture(autouse=True)
def _default_managed_config():
    """Default the command-module managed config to empty for determinism.

    ``aiwatch setup hooks`` / ``aiwatch bootstrap`` read MDM-managed settings
    via ``mdm_config.read_managed_config()`` at the OS level (macOS Managed
    Preferences / Windows registry). On a developer's own machine those can be
    populated (e.g. a real scan-only profile with ``Enforcement=false`` +
    ``Sessions=false`` and an ``OrgApiKey``), which would otherwise flip command
    behavior (scan-only hook removal, enroll-skip) and make tests non-deterministic.

    Tests that exercise specific managed-config behavior override this by
    patching the same name inside the test body.
    """
    with (
        patch(
            "runlayer_cli.commands.bootstrap.read_managed_config",
            return_value={},
        ),
        patch(
            "runlayer_cli.commands.aiwatch_setup.read_managed_config",
            return_value={},
        ),
        patch(
            "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
            return_value=False,
        ),
        patch(
            "runlayer_cli.hook_install.credential_gate.read_managed_config",
            return_value={},
        ),
        patch("runlayer_cli.mdm_config.read_backend_config", return_value=None),
    ):
        yield


@pytest.fixture(autouse=True)
def _disable_keyring():
    """Route credential reads/writes away from the real OS keychain.

    ``Config.get_secret_for_host`` — reached by the credential gate that
    ``aiwatch setup hooks`` / ``aiwatch bootstrap`` run — calls
    ``get_keyring_store()``. On a developer's own Mac that opens the real login
    keychain, which can raise a GUI auth prompt (or hang / hand back a stale
    item), so command tests block or flake locally. Default every test to the
    ``None`` (YAML-fallback) store; the handful of tests that assert keyring
    behavior override with their own ``runlayer_cli.config.get_keyring_store``
    patch. ``config`` is the sole consumer of the helper, so patching it there
    covers all command paths. Reset the cached probe around each test so real-
    keyring state from a prior test can't leak in.
    """
    reset_credential_store()
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        yield
    reset_credential_store()


def _noop_install_browser_extension(_managed, **_kwargs) -> BrowserExtensionResult:
    # Silent skip: _SKIP_NO_EXTENSION_ID is the one reason the install step never
    # reports (should_report_browser_extension_skip), so callers print nothing.
    return BrowserExtensionResult(written=False, skipped_reason=_SKIP_NO_EXTENSION_ID)


def _noop_check_browser_extension(_managed, **_kwargs) -> tuple[bool, str | None]:
    return True, None


@pytest.fixture(autouse=True)
def _isolate_browser_extension():
    """Keep the Chrome-policy reconcile off the real /Library/Managed Preferences.

    In MDM scope ``aiwatch setup hooks install`` / ``aiwatch bootstrap`` call
    ``install_browser_extension`` with the default root-owned managed-prefs dir.
    On a dev Mac that already carries a Runlayer Chrome policy the reconcile
    tries to rewrite ``/Library/Managed Preferences/com.google.Chrome.plist``
    and fails with EACCES (not root), so any MDM-scope command test that doesn't
    stub the step errors out locally. Default it to a silent no-op; the browser-
    extension tests override with their own patch of the same names. Unit tests
    call the ``browser_extension`` module directly with injected tmp dirs, so
    they are unaffected.
    """
    with (
        patch(
            "runlayer_cli.commands.aiwatch_setup.install_browser_extension",
            new=_noop_install_browser_extension,
        ),
        patch(
            "runlayer_cli.commands.aiwatch_setup.check_browser_extension",
            new=_noop_check_browser_extension,
        ),
        patch(
            "runlayer_cli.commands.bootstrap.install_browser_extension",
            new=_noop_install_browser_extension,
        ),
        patch(
            "runlayer_cli.commands.bootstrap.check_browser_extension",
            new=_noop_check_browser_extension,
        ),
    ):
        yield
