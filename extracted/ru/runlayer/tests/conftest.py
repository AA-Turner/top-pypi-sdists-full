"""Shared CLI test fixtures."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from runlayer_cli.runtime import reset_aiwatch_runtime


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
    behavior (scan-only no-op, enroll-skip) and make tests non-deterministic.

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
            "runlayer_cli.hook_install.credential_gate.read_managed_config",
            return_value={},
        ),
    ):
        yield
