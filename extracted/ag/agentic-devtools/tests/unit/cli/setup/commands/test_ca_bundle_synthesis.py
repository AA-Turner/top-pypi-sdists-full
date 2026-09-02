"""Tests for CA-bundle DependencyStatus synthesis in setup_check_cmd."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup import commands


class TestCaBundleSynthesis:
    """setup_check_cmd synthesizes CA-bundle DependencyStatus."""

    def test_ca_bundle_missing_results_in_exit_2(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """When CA bundle file is missing, setup_check_cmd exits with code 2."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        empty_home = tmp_path / "empty_home"
        empty_home.mkdir()
        # No .agdt/certs/ directory exists.

        with (
            patch("pathlib.Path.home", return_value=empty_home),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_ca_bundle_empty_results_in_exit_2(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """When CA bundle file exists but is empty (0 bytes), exits with code 2."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_home = tmp_path / "home"
        bundle = fake_home / ".agdt" / "certs" / "unified-ca-bundle.pem"
        bundle.parent.mkdir(parents=True)
        bundle.write_text("")  # Empty file.

        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_ca_bundle_oserror_treated_as_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """When stat() raises OSError (not FileNotFoundError), treated as missing."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_home = tmp_path / "home"
        fake_home.mkdir()

        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch("pathlib.Path.stat", side_effect=OSError("permission denied")),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_ca_bundle_directory_treated_as_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """A directory at the CA bundle path does not count as a valid found bundle."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_home = tmp_path / "home"
        bundle_dir = fake_home / ".agdt" / "certs" / "unified-ca-bundle.pem"
        bundle_dir.mkdir(parents=True)

        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_ca_bundle_non_pem_content_treated_as_missing(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """A non-empty bundle with no cert blocks is treated as missing."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_home = tmp_path / "home"
        bundle = fake_home / ".agdt" / "certs" / "unified-ca-bundle.pem"
        bundle.parent.mkdir(parents=True)
        bundle.write_text("not a pem bundle")

        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2

    def test_ca_bundle_with_certificate_content_is_found(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """A non-empty bundle containing at least one cert block is treated as found."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_home = tmp_path / "home"
        bundle = fake_home / ".agdt" / "certs" / "unified-ca-bundle.pem"
        bundle.parent.mkdir(parents=True)
        bundle.write_text("-----BEGIN CERTIFICATE-----\nabc\n-----END CERTIFICATE-----\n")

        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            commands.setup_check_cmd()

    def test_ca_bundle_read_error_treated_as_missing(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """A read failure when validating bundle content is treated as missing."""
        monkeypatch.setattr(sys, "argv", ["agdt-setup-check"])
        fake_home = tmp_path / "home"
        bundle = fake_home / ".agdt" / "certs" / "unified-ca-bundle.pem"
        bundle.parent.mkdir(parents=True)
        bundle.write_text("-----BEGIN CERTIFICATE-----\nabc\n-----END CERTIFICATE-----\n")

        with (
            patch("pathlib.Path.home", return_value=fake_home),
            patch("pathlib.Path.read_text", side_effect=OSError("read failed")),
            patch.object(commands, "check_all_dependencies", return_value=[]),
        ):
            with pytest.raises(SystemExit) as exc_info:
                commands.setup_check_cmd()
        assert exc_info.value.code == 2
