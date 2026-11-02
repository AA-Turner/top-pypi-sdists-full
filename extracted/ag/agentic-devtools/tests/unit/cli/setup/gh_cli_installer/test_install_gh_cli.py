"""Tests for install_gh_cli."""

from unittest.mock import patch

import requests

from agentic_devtools.cli.setup import gh_cli_installer


def _make_release(version: str = "v2.65.0") -> dict:
    return {
        "tag_name": version,
        "assets": [
            {
                "name": "gh_2.65.0_linux_amd64.tar.gz",
                "browser_download_url": "https://github.com/dl/gh.tar.gz",
            }
        ],
    }


class TestInstallGhCli:
    """Tests for install_gh_cli."""

    def test_skips_when_already_up_to_date(self, capsys):
        """Prints up-to-date message and returns True when version matches."""
        release = _make_release("v2.65.0")
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value="/usr/bin/gh"):
            with patch.object(gh_cli_installer, "get_installed_version", return_value="v2.65.0"):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    result = gh_cli_installer.install_gh_cli()
        assert result is True
        assert "up-to-date" in capsys.readouterr().out

    def test_returns_false_on_release_fetch_error(self, capsys):
        """Returns False when release info cannot be fetched."""
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value=None):
            with patch.object(gh_cli_installer, "get_installed_version", return_value=None):
                with patch.object(
                    gh_cli_installer,
                    "get_latest_release_info",
                    side_effect=requests.ConnectionError("no network"),
                ):
                    result = gh_cli_installer.install_gh_cli()
        assert result is False
        assert "Failed to fetch" in capsys.readouterr().err

    def test_returns_false_on_unsupported_platform(self, capsys):
        """Returns False when no asset matches the platform."""
        release = {"tag_name": "v2.65.0", "assets": []}
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value=None):
            with patch.object(gh_cli_installer, "get_installed_version", return_value=None):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    with patch.object(
                        gh_cli_installer,
                        "detect_platform_asset",
                        side_effect=RuntimeError("No asset"),
                    ):
                        result = gh_cli_installer.install_gh_cli()
        assert result is False

    def test_returns_false_when_no_download_url(self, capsys):
        """Returns False when the asset has no browser_download_url."""
        release = {
            "tag_name": "v2.65.0",
            "assets": [{"name": "gh_2.65.0_linux_amd64.tar.gz"}],
        }
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value=None):
            with patch.object(gh_cli_installer, "get_installed_version", return_value=None):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    with patch.object(
                        gh_cli_installer,
                        "detect_platform_asset",
                        return_value="gh_2.65.0_linux_amd64.tar.gz",
                    ):
                        result = gh_cli_installer.install_gh_cli()
        assert result is False

    def test_force_reinstall_ignores_version_match(self, capsys):
        """With force=True, reinstalls even when already up-to-date."""
        release = _make_release("v2.65.0")
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value="/usr/bin/gh"):
            with patch.object(gh_cli_installer, "get_installed_version", return_value="v2.65.0"):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    with patch.object(
                        gh_cli_installer,
                        "detect_platform_asset",
                        return_value="gh_2.65.0_linux_amd64.tar.gz",
                    ):
                        with patch.object(gh_cli_installer, "download_and_install", return_value=True) as mock_dl:
                            result = gh_cli_installer.install_gh_cli(force=True)
        assert result is True
        mock_dl.assert_called_once()

    def test_successful_install_prints_paths(self, capsys):
        """Prints download and install messages on success."""
        release = _make_release("v2.65.0")
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value=None):
            with patch.object(gh_cli_installer, "get_installed_version", return_value=None):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    with patch.object(
                        gh_cli_installer,
                        "detect_platform_asset",
                        return_value="gh_2.65.0_linux_amd64.tar.gz",
                    ):
                        with patch.object(gh_cli_installer, "download_and_install", return_value=True):
                            result = gh_cli_installer.install_gh_cli()
        assert result is True
        out = capsys.readouterr().out
        assert "Downloaded gh" in out
        assert "Installed to" in out

    def test_returns_false_when_download_fails(self, capsys):
        """Returns False when download_and_install returns False."""
        release = _make_release("v2.65.0")
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value=None):
            with patch.object(gh_cli_installer, "get_installed_version", return_value=None):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    with patch.object(
                        gh_cli_installer,
                        "detect_platform_asset",
                        return_value="gh_2.65.0_linux_amd64.tar.gz",
                    ):
                        with patch.object(gh_cli_installer, "download_and_install", return_value=False):
                            result = gh_cli_installer.install_gh_cli()
        assert result is False

    def test_dry_run_returns_true_without_network(self, capsys):
        """dry_run=True returns True immediately without fetching releases."""
        with patch.object(gh_cli_installer, "get_latest_release_info") as mock_fetch:
            result = gh_cli_installer.install_gh_cli(dry_run=True)
        assert result is True
        mock_fetch.assert_not_called()
        assert "would install GitHub CLI" in capsys.readouterr().out

    def test_dry_run_returns_true_without_other_lookups(self):
        """dry_run=True exits before version and binary discovery."""
        with patch.object(gh_cli_installer, "get_gh_cli_binary") as mock_binary:
            with patch.object(gh_cli_installer, "get_installed_version") as mock_version:
                assert gh_cli_installer.install_gh_cli(dry_run=True) is True
        mock_binary.assert_not_called()
        mock_version.assert_not_called()

    def test_platform_label_uses_arm64_alias(self):
        """_get_platform_label normalizes aarch64 to arm64."""
        with patch.object(gh_cli_installer.platform, "system", return_value="Linux"):
            with patch.object(gh_cli_installer.platform, "machine", return_value="aarch64"):
                assert gh_cli_installer._get_platform_label() == "linux-arm64"

    def test_platform_label_defaults_to_amd64(self):
        """_get_platform_label maps non-arm architectures to amd64."""
        with patch.object(gh_cli_installer.platform, "system", return_value="Darwin"):
            with patch.object(gh_cli_installer.platform, "machine", return_value="x86_64"):
                assert gh_cli_installer._get_platform_label() == "darwin-amd64"

    def test_returns_false_when_asset_not_in_list(self, capsys):
        """Returns False when detected asset name has no matching entry in assets list."""
        release = {
            "tag_name": "v2.65.0",
            "assets": [
                {"name": "other-asset", "browser_download_url": "https://example.com/other"},
                {"name": "another-asset", "browser_download_url": "https://example.com/another"},
            ],
        }
        with patch.object(gh_cli_installer, "get_gh_cli_binary", return_value=None):
            with patch.object(gh_cli_installer, "get_installed_version", return_value=None):
                with patch.object(gh_cli_installer, "get_latest_release_info", return_value=release):
                    with patch.object(
                        gh_cli_installer,
                        "detect_platform_asset",
                        return_value="gh_2.65.0_linux_amd64.tar.gz",
                    ):
                        result = gh_cli_installer.install_gh_cli()
        assert result is False
        assert "No download URL" in capsys.readouterr().err
