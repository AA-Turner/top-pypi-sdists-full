# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Manifest and runtime environment tests for direct Ray connect mode.

These tests validate that manifests and runtime environments work correctly
when connecting to a pre-existing Ray cluster via direct network access.
"""

import logging

import pytest
import ray

import geneva

_LOG = logging.getLogger(__name__)


@pytest.mark.timeout(900)
def test_direct_connect_manifest_isolation(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Verify runtime environment isolation with direct connect."""
    # Verify Ray is initialized with correct environment
    assert ray.is_initialized(), "Ray should be initialized"

    # Test that packaged dependencies are available on workers
    @ray.remote
    def check_imports() -> tuple[str | None, str]:
        import pyarrow

        return geneva.__version__, pyarrow.__version__

    geneva_ver, pyarrow_ver = ray.get(check_imports.remote())
    _LOG.info(f"Worker environment: geneva={geneva_ver}, pyarrow={pyarrow_ver}")

    assert geneva_ver is not None, "geneva should be importable on workers"
    assert pyarrow_ver is not None, "pyarrow should be importable on workers"


@pytest.mark.timeout(900)
def test_direct_connect_env_vars(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Verify environment variables propagate to workers."""
    import os

    @ray.remote
    def get_env_var(key: str) -> str | None:
        return os.getenv(key)

    # Check Ray-specific env vars we set in direct_connect_context
    log_to_driver = ray.get(get_env_var.remote("RAY_LOG_TO_DRIVER"))
    assert log_to_driver == "1", "RAY_LOG_TO_DRIVER should be set to '1'"


@pytest.mark.timeout(900)
def test_direct_connect_get_imported(
    geneva_test_bucket: str,
    direct_connect_context: None,
) -> None:
    """Test that get_imported works with direct connect."""
    from geneva.runners.ray.pipeline import get_imported

    pkgs = ray.get(get_imported.remote())
    for pkg, ver in sorted(pkgs.items()):
        _LOG.info(f"{pkg}=={ver}")

    # Verify essential packages are available
    assert "geneva" in pkgs, "geneva should be importable"
    assert "pyarrow" in pkgs, "pyarrow should be importable"
