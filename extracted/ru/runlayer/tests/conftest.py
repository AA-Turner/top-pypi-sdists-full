"""Shared CLI test fixtures."""

from __future__ import annotations

from unittest.mock import patch

import pytest


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
