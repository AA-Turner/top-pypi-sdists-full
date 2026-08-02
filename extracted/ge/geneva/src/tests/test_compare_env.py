# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for compare_ray_environments diagnostic tool."""

import logging
from collections.abc import Generator
from unittest.mock import patch

import pytest
import ray

from geneva.runners.ray.compare_env import (
    _get_context_runtime_env,
    compare_ray_environments,
    get_comparison_result,
)

_LOG = logging.getLogger(__name__)

pytestmark = pytest.mark.ray


@pytest.fixture(scope="module")
def local_ray_cluster() -> Generator[None, None, None]:
    """Module-scoped fixture that starts Ray once for all tests in this module."""
    ray.shutdown()
    ray.init(ignore_reinit_error=True, logging_level="ERROR")
    yield
    ray.shutdown()


class TestCompareRayEnvironments:
    """Tests for compare_ray_environments using a shared Ray cluster."""

    def test_basic_comparison(self, local_ray_cluster) -> None:
        """Test basic environment comparison with local Ray cluster."""
        # Ray is already initialized by fixture, so default auto_init=False works
        result = compare_ray_environments(include_sys_path=False)

        # Verify result structure
        assert "local" in result
        assert "remote" in result
        assert "env_diffs" in result
        assert "pkg_diffs" in result
        assert "sys_path_diffs" in result

        # Both should be Python 3.x
        assert result["local"]["python"]["version"].startswith("3.")
        assert result["remote"]["python"]["version"].startswith("3.")

        # Should have some common packages
        local_pkgs = result["local"]["packages"]
        remote_pkgs = result["remote"]["packages"]
        assert "ray" in local_pkgs
        assert "ray" in remote_pkgs

        _LOG.info(
            f"Found {len(result['pkg_diffs']['version_mismatch'])} "
            "package version mismatches"
        )
        _LOG.info(
            f"Found {len(result['env_diffs']['diffs'])} "
            "environment variable differences"
        )

    def test_data_only_with_env_prefix(self, local_ray_cluster) -> None:
        """Test get_comparison_result function (data only, no printing)."""
        result = get_comparison_result(env_prefix="PYTHON")

        # Should only have environment variables starting with PYTHON
        env_diffs = result["env_diffs"]
        for key in env_diffs["only_local"]:
            assert key.startswith("PYTHON")
        for key in env_diffs["only_remote"]:
            assert key.startswith("PYTHON")

        _LOG.info(f"Filtered env vars: {len(env_diffs['only_local'])} local-only")

    def test_sys_path_differences(self, local_ray_cluster) -> None:
        """Test that sys.path differences are captured."""
        result = get_comparison_result()

        sys_path_diffs = result["sys_path_diffs"]

        # Should have some paths
        assert sys_path_diffs["local_count"] > 0
        assert sys_path_diffs["remote_count"] > 0
        assert sys_path_diffs["intersection_count"] > 0

        _LOG.info(
            f"sys.path: {sys_path_diffs['local_count']} local, "
            f"{sys_path_diffs['remote_count']} remote, "
            f"{sys_path_diffs['intersection_count']} shared"
        )

        # There should be some differences
        assert (
            len(sys_path_diffs["only_local"]) > 0
            or len(sys_path_diffs["only_remote"]) > 0
        )

    @pytest.mark.parametrize(
        ("show_all", "include_sys_path"),
        [
            (False, True),
            (False, False),
            (True, True),
        ],
    )
    def test_options(
        self, local_ray_cluster, show_all: bool, include_sys_path: bool
    ) -> None:
        """Test compare_ray_environments with different options."""
        result = compare_ray_environments(
            show_all=show_all,
            include_sys_path=include_sys_path,
        )

        # Result should always have sys_path_diffs in the dict
        assert "sys_path_diffs" in result

        _LOG.info(
            f"Tested with show_all={show_all}, include_sys_path={include_sys_path}"
        )

    def test_package_mismatch_format(self, local_ray_cluster) -> None:
        """Test that package version mismatches are properly formatted."""
        result = get_comparison_result()

        pkg_diffs = result["pkg_diffs"]
        version_mismatch = pkg_diffs["version_mismatch"]

        # Each mismatch should be a tuple of (name, local_version, remote_version)
        for item in version_mismatch:
            assert isinstance(item, tuple)
            assert len(item) == 3
            name, local_ver, remote_ver = item
            assert isinstance(name, str)
            assert isinstance(local_ver, str)
            assert isinstance(remote_ver, str)
            assert local_ver != remote_ver
            _LOG.info(f"Version mismatch: {name} local={local_ver} remote={remote_ver}")

        # Verify structure
        assert isinstance(pkg_diffs["only_local"], list)
        assert isinstance(pkg_diffs["only_remote"], list)
        assert isinstance(pkg_diffs["version_mismatch"], list)

    def test_platform_info(self, local_ray_cluster) -> None:
        """Test that platform information is captured correctly."""
        result = get_comparison_result()

        # Check local platform info
        local_platform = result["local"]["platform"]
        assert "system" in local_platform
        assert "release" in local_platform
        assert "machine" in local_platform

        # Check remote platform info
        remote_platform = result["remote"]["platform"]
        assert "system" in remote_platform
        assert "release" in remote_platform
        assert "machine" in remote_platform

        # Should be the same OS (both running locally)
        assert local_platform["system"] == remote_platform["system"]

        _LOG.info(f"Local OS: {local_platform['system']} {local_platform['release']}")
        _LOG.info(
            f"Remote OS: {remote_platform['system']} {remote_platform['release']}"
        )

    def test_runtime_env_passthrough(self, local_ray_cluster) -> None:
        """Test that explicit runtime_env is applied to the remote snapshot."""
        # With an empty runtime_env dict, behavior should be same as default
        result = get_comparison_result(runtime_env={})
        assert "local" in result
        assert "remote" in result

    def test_requires_ray_initialized(self) -> None:
        """Test that RuntimeError is raised when Ray is not initialized."""
        ray.shutdown()
        try:
            with pytest.raises(RuntimeError, match="Ray is not initialized"):
                get_comparison_result()
        finally:
            # Re-init for other tests (though this test runs last due to shutdown)
            ray.init(ignore_reinit_error=True, logging_level="ERROR")


class TestGetContextRuntimeEnv:
    """Tests for _get_context_runtime_env helper."""

    def test_no_context_returns_none(self) -> None:
        """Returns None when no Geneva context is active."""
        with patch("geneva._context.get_current_context", return_value=None):
            assert _get_context_runtime_env() is None

    def test_context_without_manifest_returns_none(self) -> None:
        """Returns None when context has no manifest."""
        mock_ctx = type("MockCtx", (), {"manifest": None})()
        with patch(
            "geneva._context.get_current_context",
            return_value=mock_ctx,
        ):
            assert _get_context_runtime_env() is None

    def test_manifest_with_pip(self) -> None:
        """Builds runtime_env with pip from manifest."""
        from geneva.manifest.mgr import GenevaManifest

        manifest = GenevaManifest(name="test", pip=["emoji==2.14.1"])
        mock_ctx = type("MockCtx", (), {"manifest": manifest})()
        with patch(
            "geneva._context.get_current_context",
            return_value=mock_ctx,
        ):
            result = _get_context_runtime_env()
            assert result == {"pip": ["emoji==2.14.1"]}

    def test_manifest_with_requirements_path(self, tmp_path) -> None:
        """Prefers requirements_path over pip list."""
        from geneva.manifest.mgr import GenevaManifest

        req_file = tmp_path / "requirements.txt"
        req_file.write_text("emoji==2.14.1\n")

        manifest = GenevaManifest(
            name="test",
            pip=["emoji==2.14.1"],
            requirements_path=str(req_file),
        )
        mock_ctx = type("MockCtx", (), {"manifest": manifest})()
        with patch(
            "geneva._context.get_current_context",
            return_value=mock_ctx,
        ):
            result = _get_context_runtime_env()
            assert result == {"pip": str(req_file)}

    def test_manifest_with_conda(self) -> None:
        """Builds runtime_env with conda from manifest."""
        from geneva.manifest.mgr import GenevaManifest

        conda_cfg = {"dependencies": ["pip", {"pip": ["numpy"]}]}
        manifest = GenevaManifest(name="test", conda=conda_cfg)
        mock_ctx = type("MockCtx", (), {"manifest": manifest})()
        with patch(
            "geneva._context.get_current_context",
            return_value=mock_ctx,
        ):
            result = _get_context_runtime_env()
            assert result == {"conda": conda_cfg}

    def test_manifest_with_no_deps_returns_none(self) -> None:
        """Returns None when manifest has no pip or conda."""
        from geneva.manifest.mgr import GenevaManifest

        manifest = GenevaManifest(name="test")
        mock_ctx = type("MockCtx", (), {"manifest": manifest})()
        with patch(
            "geneva._context.get_current_context",
            return_value=mock_ctx,
        ):
            assert _get_context_runtime_env() is None
