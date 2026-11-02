"""Tests for _release_pypi_sync function."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.release.commands import _release_pypi_sync
from agentic_devtools.cli.release.helpers import ReleaseError


class TestReleasePypiSync:
    """Tests for _release_pypi_sync function."""

    @patch("agentic_devtools.cli.release.commands.get_pypi_dry_run", return_value=False)
    @patch("agentic_devtools.cli.release.commands.get_pypi_repository", return_value=None)
    @patch("agentic_devtools.cli.release.commands.get_pypi_version", return_value="1.0.0")
    @patch("agentic_devtools.cli.release.commands.get_pypi_package_name", return_value="my-pkg")
    @patch("agentic_devtools.cli.release.commands.helpers")
    @patch("agentic_devtools.cli.release.commands._run_tests_and_wait", return_value=0)
    def test_full_release_flow(
        self,
        mock_tests,
        mock_helpers,
        mock_pkg,
        mock_ver,
        mock_repo,
        mock_dry,
    ):
        """Should execute full release when not dry-run and version doesn't exist."""
        mock_helpers.pypi_version_exists.return_value = False
        mock_helpers.ReleaseError = ReleaseError

        _release_pypi_sync()

        mock_helpers.pypi_version_exists.assert_called_once_with("my-pkg", "1.0.0", repository="pypi")
        mock_helpers.build_distribution.assert_called_once_with("dist")
        mock_helpers.validate_distribution.assert_called_once_with("dist")
        mock_helpers.upload_distribution.assert_called_once_with("dist", repository="pypi")

    @patch("agentic_devtools.cli.release.commands.get_pypi_dry_run", return_value=True)
    @patch("agentic_devtools.cli.release.commands.get_pypi_repository", return_value=None)
    @patch("agentic_devtools.cli.release.commands.get_pypi_version", return_value="1.0.0")
    @patch("agentic_devtools.cli.release.commands.get_pypi_package_name", return_value="my-pkg")
    @patch("agentic_devtools.cli.release.commands.helpers")
    @patch("agentic_devtools.cli.release.commands._run_tests_and_wait", return_value=0)
    def test_dry_run_skips_upload(
        self,
        mock_tests,
        mock_helpers,
        mock_pkg,
        mock_ver,
        mock_repo,
        mock_dry,
    ):
        """Should skip upload when dry_run is True."""
        mock_helpers.pypi_version_exists.return_value = False
        mock_helpers.ReleaseError = ReleaseError

        _release_pypi_sync()

        mock_helpers.build_distribution.assert_called_once()
        mock_helpers.validate_distribution.assert_called_once()
        mock_helpers.upload_distribution.assert_not_called()

    @patch("agentic_devtools.cli.release.commands.get_pypi_dry_run", return_value=False)
    @patch("agentic_devtools.cli.release.commands.get_pypi_repository", return_value=None)
    @patch("agentic_devtools.cli.release.commands.get_pypi_version", return_value="1.0.0")
    @patch("agentic_devtools.cli.release.commands.get_pypi_package_name", return_value="my-pkg")
    @patch("agentic_devtools.cli.release.commands.helpers")
    def test_raises_when_version_already_exists(
        self,
        mock_helpers,
        mock_pkg,
        mock_ver,
        mock_repo,
        mock_dry,
    ):
        """Should raise ReleaseError when version already published."""
        mock_helpers.pypi_version_exists.return_value = True
        mock_helpers.ReleaseError = ReleaseError

        with pytest.raises(ReleaseError, match="already exists"):
            _release_pypi_sync()

    @patch("agentic_devtools.cli.release.commands.get_pypi_dry_run", return_value=False)
    @patch("agentic_devtools.cli.release.commands.get_pypi_repository", return_value=None)
    @patch("agentic_devtools.cli.release.commands.get_pypi_version", return_value="1.0.0")
    @patch("agentic_devtools.cli.release.commands.get_pypi_package_name", return_value="my-pkg")
    @patch("agentic_devtools.cli.release.commands.helpers")
    @patch("agentic_devtools.cli.release.commands._run_tests_and_wait", return_value=1)
    def test_raises_when_tests_fail(
        self,
        mock_tests,
        mock_helpers,
        mock_pkg,
        mock_ver,
        mock_repo,
        mock_dry,
    ):
        """Should raise ReleaseError when test suite fails."""
        mock_helpers.pypi_version_exists.return_value = False
        mock_helpers.ReleaseError = ReleaseError

        with pytest.raises(ReleaseError, match="Test suite failed"):
            _release_pypi_sync()

    @patch("agentic_devtools.cli.release.commands.get_pypi_dry_run", return_value=False)
    @patch("agentic_devtools.cli.release.commands.get_pypi_repository", return_value="testpypi")
    @patch("agentic_devtools.cli.release.commands.get_pypi_version", return_value="1.0.0")
    @patch("agentic_devtools.cli.release.commands.get_pypi_package_name", return_value="my-pkg")
    @patch("agentic_devtools.cli.release.commands.helpers")
    @patch("agentic_devtools.cli.release.commands._run_tests_and_wait", return_value=0)
    def test_uses_testpypi_repository(
        self,
        mock_tests,
        mock_helpers,
        mock_pkg,
        mock_ver,
        mock_repo,
        mock_dry,
    ):
        """Should pass testpypi repository to upload when configured."""
        mock_helpers.pypi_version_exists.return_value = False
        mock_helpers.ReleaseError = ReleaseError

        _release_pypi_sync()

        mock_helpers.upload_distribution.assert_called_once_with("dist", repository="testpypi")

    def test_exits_when_package_name_missing(self):
        """Should sys.exit(1) when package name is not set."""
        with patch(
            "agentic_devtools.cli.release.commands.get_pypi_package_name",
            return_value=None,
        ):
            with pytest.raises(SystemExit):
                _release_pypi_sync()

    def test_exits_when_version_missing(self):
        """Should sys.exit(1) when version is not set."""
        with patch(
            "agentic_devtools.cli.release.commands.get_pypi_package_name",
            return_value="my-pkg",
        ):
            with patch(
                "agentic_devtools.cli.release.commands.get_pypi_version",
                return_value=None,
            ):
                with pytest.raises(SystemExit):
                    _release_pypi_sync()
