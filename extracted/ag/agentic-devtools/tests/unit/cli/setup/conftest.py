"""
Shared fixtures for tests/unit/cli/setup/.

Mocks network-dependent functions to keep unit tests fast and isolated.
"""

import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_setup_network():
    """Mock SSL/cert helpers to avoid real network calls in setup unit tests."""
    # Clear AGDT_NO_VERIFY_SSL so tests are not affected by previous test state.
    original = os.environ.pop("AGDT_NO_VERIFY_SSL", None)
    try:
        with patch("agentic_devtools.cli.cert_utils.get_ssl_verify", return_value=True):
            with patch("agentic_devtools.cli.cert_utils.ensure_ca_bundle", return_value="dummy_ca_bundle"):
                with patch("agentic_devtools.cli.setup.commands._prefetch_certs", return_value=(None, None)):
                    yield
    finally:
        # Restore original env var state.
        os.environ.pop("AGDT_NO_VERIFY_SSL", None)
        if original is not None:
            os.environ["AGDT_NO_VERIFY_SSL"] = original


@pytest.fixture(autouse=True)
def mock_detect_corrupted_artifacts():
    """Mock detect_corrupted_artifacts to avoid scanning real site-packages."""
    with patch(
        "agentic_devtools.cli.setup.script_generators.required_setup.detect_corrupted_artifacts",
        return_value=[],
    ):
        yield


@pytest.fixture(autouse=True)
def no_active_workflow():
    """Default to "no active workflow" so auto-run suppression is deterministic.

    Without this, the developer's (or CI runner's) persisted workflow state
    could suppress auto-run and change the behaviour under test.
    """
    with patch("agentic_devtools.state.get_workflow_state", return_value=None):
        yield
