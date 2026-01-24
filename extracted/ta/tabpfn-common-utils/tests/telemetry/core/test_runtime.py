from __future__ import annotations

import os
import pytest
import sys
from unittest.mock import patch

from tabpfn_common_utils.telemetry.core.runtime import (
    _is_ci,
    _is_ipy,
    _is_jupyter_kernel,
    _is_tty,
    get_execution_context,
)


class TestRuntimeDetection:
    """Test runtime environment detection."""

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.module = "tabpfn_common_utils.telemetry.core.runtime"

    def test_get_runtime_ci_environment(self) -> None:
        """Test that CI environments are detected correctly."""
        with patch(f"{self.module}._is_ci", return_value=True):
            runtime = get_execution_context()
            assert runtime.ci is True
            assert runtime.interactive is False
            assert runtime.kernel is None

    def test_get_runtime_interactive_ipython(self) -> None:
        """Test that IPython environments are detected as interactive."""
        with (
            patch(f"{self.module}._is_ci", return_value=False),
            patch(f"{self.module}._is_ipy", return_value=True),
        ):
            runtime = get_execution_context()
            assert runtime.interactive is True
            assert runtime.ci is False

    def test_get_runtime_interactive_jupyter(self) -> None:
        """Test that Jupyter environments are detected as interactive."""
        with (
            patch(f"{self.module}._is_ci", return_value=False),
            patch(f"{self.module}._is_ipy", return_value=False),
            patch(f"{self.module}._is_jupyter_kernel", return_value=True),
        ):
            runtime = get_execution_context()
            assert runtime.interactive is True
            assert runtime.ci is False

    def test_get_runtime_default_noninteractive(self) -> None:
        """Test that default environment is noninteractive."""
        with (
            patch(f"{self.module}._is_ci", return_value=False),
            patch(f"{self.module}._is_ipy", return_value=False),
            patch(f"{self.module}._is_jupyter_kernel", return_value=False),
        ):
            runtime = get_execution_context()
            assert runtime.interactive is False
            assert runtime.ci is False


class TestIPythonCheck:
    """Test IPython environment detection."""

    def test_is_ipy_returns_bool(self) -> None:
        """Test that _is_ipy always returns a boolean."""
        result = _is_ipy()
        assert isinstance(result, bool)

    def test_is_ipy_handles_import_error(self) -> None:
        """Test that _is_ipy handles import errors gracefully."""
        # Since IPython is not installed, this should return False
        result = _is_ipy()
        assert result is False


class TestJupyterKernelCheck:
    """Test Jupyter kernel detection."""

    def test_is_jupyter_kernel_with_ipykernel(self) -> None:
        """Test Jupyter detection with ipykernel in sys.modules."""
        with patch.dict(sys.modules, {"ipykernel": object()}):
            assert _is_jupyter_kernel() is True

    def test_is_jupyter_kernel_with_jupyter_env_vars(self) -> None:
        """Test Jupyter detection with Jupyter environment variables."""
        with patch.dict(os.environ, {"JPY_PARENT_PID": "12345"}):
            assert _is_jupyter_kernel() is True

    def test_is_jupyter_kernel_with_colab(self) -> None:
        """Test Jupyter detection with Colab environment."""
        with patch.dict(os.environ, {"COLAB_RELEASE_TAG": "r20231201"}):
            assert _is_jupyter_kernel() is True

    def test_is_jupyter_kernel_no_indicators(self) -> None:
        """Test Jupyter detection with no indicators."""
        with (
            patch.dict(sys.modules, {}, clear=True),
            patch.dict(os.environ, {}, clear=True),
        ):
            assert _is_jupyter_kernel() is False


class TestCICheck:
    """Test CI environment detection."""

    def test_is_ci_github_actions(self) -> None:
        """Test CI detection with GitHub Actions."""
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
            assert _is_ci() is True

    def test_is_ci_gitlab_ci(self) -> None:
        """Test CI detection with GitLab CI."""
        with patch.dict(os.environ, {"GITLAB_CI": "true"}):
            assert _is_ci() is True

    def test_is_ci_jenkins(self) -> None:
        """Test CI detection with Jenkins."""
        with patch.dict(os.environ, {"JENKINS_URL": "http://jenkins.example.com"}):
            assert _is_ci() is True

    def test_is_ci_travis(self) -> None:
        """Test CI detection with Travis CI."""
        with patch.dict(os.environ, {"TRAVIS": "true"}):
            assert _is_ci() is True

    def test_is_ci_circleci(self) -> None:
        """Test CI detection with CircleCI."""
        with patch.dict(os.environ, {"CIRCLECI": "true"}):
            assert _is_ci() is True

    def test_is_ci_azure_devops(self) -> None:
        """Test CI detection with Azure DevOps."""
        with patch.dict(os.environ, {"TF_BUILD": "true"}):
            assert _is_ci() is True

    def test_is_ci_aws_codebuild(self) -> None:
        """Test CI detection with AWS CodeBuild."""
        with patch.dict(os.environ, {"CODEBUILD_BUILD_ID": "build-123"}):
            assert _is_ci() is True

    def test_is_ci_google_cloud_build(self) -> None:
        """Test CI detection with Google Cloud Build."""
        with patch.dict(os.environ, {"BUILD_ID": "build-123"}):
            assert _is_ci() is True

    def test_is_ci_no_indicators(self) -> None:
        """Test CI detection with no CI indicators."""
        with patch.dict(os.environ, {}, clear=True):
            assert _is_ci() is False

    def test_is_ci_returns_bool(self) -> None:
        """Test that _is_ci always returns a boolean."""
        result = _is_ci()
        assert isinstance(result, bool)


class TestTTYCheck:
    """Test TTY detection."""

    def test_is_tty_with_tty(self) -> None:
        """Test TTY detection when stdin/stdout are TTY."""
        with (
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stdout.isatty", return_value=True),
        ):
            assert _is_tty() is True

    def test_is_tty_without_tty(self) -> None:
        """Test TTY detection when stdin/stdout are not TTY."""
        with (
            patch("sys.stdin.isatty", return_value=False),
            patch("sys.stdout.isatty", return_value=False),
        ):
            assert _is_tty() is False

    def test_is_tty_mixed_tty(self) -> None:
        """Test TTY detection with mixed TTY status."""
        with (
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stdout.isatty", return_value=False),
        ):
            assert _is_tty() is False

    def test_is_tty_exception(self) -> None:
        """Test TTY detection with exception."""
        with patch("sys.stdin.isatty", side_effect=OSError):
            assert _is_tty() is False
