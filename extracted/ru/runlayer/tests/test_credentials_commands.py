"""Tests for the hidden credentials commands."""

import re
from unittest.mock import MagicMock, patch

import httpx
import pytest
from typer.testing import CliRunner

from runlayer_cli.commands.credentials import app as credentials_app
from runlayer_cli.config import Config
from runlayer_cli.credential_store import KeyringCredentialStore, reset_credential_store
from runlayer_cli.main import app

runner = CliRunner()


def strip_ansi(text: str) -> str:
    return re.compile(r"\x1b\[[0-9;]*m").sub("", text)


@pytest.fixture(autouse=True)
def _disable_keyring():
    reset_credential_store()
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        yield
    reset_credential_store()


def _base_config() -> Config:
    return Config(
        default_host="https://app.runlayer.com",
        hosts={
            "app.runlayer.com": {
                "url": "https://app.runlayer.com",
                "secret": "rl_user_key",
                "org_api_keys": {"mcp-watch": "rl_org_aaaaaa"},
            }
        },
    )


# ── Hidden from root help ────────────────────────────────────────────


def test_credentials_hidden_from_root_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    plain = strip_ansi(result.output)
    for line in plain.splitlines():
        stripped = line.strip()
        if stripped.startswith("credentials"):
            pytest.fail(f"'credentials' command visible in root help: {line}")


def test_credentials_app_is_hidden():
    assert credentials_app.info.hidden is True


# ── add org ──────────────────────────────────────────────────────────


class TestAddOrg:
    def test_saves_org_key(self):
        config = _base_config()
        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config") as mock_save,
        ):
            result = runner.invoke(
                app,
                [
                    "credentials",
                    "add",
                    "org",
                    "security-scan",
                    "--secret",
                    "rl_org_new",
                ],
            )
            assert result.exit_code == 0
            assert "saved" in result.output
            mock_save.assert_called_once()
            saved = mock_save.call_args[0][0]
            assert (
                saved.get_org_api_key("https://app.runlayer.com", "security-scan")
                == "rl_org_new"
            )

    def test_requires_host(self):
        config = Config()
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                ["credentials", "add", "org", "foo", "--secret", "rl_org_x"],
            )
            assert result.exit_code == 1
            assert "No host configured" in result.output

    def test_errors_when_not_persisted(self):
        """aiwatch runtime: save_config no-op (False) means the org key was never
        persisted — must error, not print success."""
        config = _base_config()
        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config", return_value=False),
        ):
            result = runner.invoke(
                app,
                [
                    "credentials",
                    "add",
                    "org",
                    "security-scan",
                    "--secret",
                    "rl_org_new",
                ],
            )
            assert result.exit_code == 1
            assert "could not be persisted" in result.output

    def test_explicit_host(self):
        config = Config()
        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config") as mock_save,
        ):
            result = runner.invoke(
                app,
                [
                    "credentials",
                    "add",
                    "org",
                    "my-key",
                    "--secret",
                    "rl_org_val",
                    "--host",
                    "https://custom.example.com",
                ],
            )
            assert result.exit_code == 0
            mock_save.assert_called_once()
            saved = mock_save.call_args[0][0]
            assert (
                saved.get_org_api_key("https://custom.example.com", "my-key")
                == "rl_org_val"
            )


# ── add user ─────────────────────────────────────────────────────────


class TestAddUser:
    def test_saves_user_key_to_config(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config") as mock_save,
        ):
            result = runner.invoke(
                app,
                ["credentials", "add", "user", "--secret", "rl_user_new"],
            )
            assert result.exit_code == 0
            assert "saved" in result.output
            assert "config file" in result.output
            mock_save.assert_called_once()

    def test_user_errors_when_not_persisted(self):
        """aiwatch runtime: keychain write failed (keyring disabled) and
        save_config no-op (False) — user key not persisted, must error."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config", return_value=False),
        ):
            result = runner.invoke(
                app,
                ["credentials", "add", "user", "--secret", "rl_user_new"],
            )
            assert result.exit_code == 1
            assert "could not be persisted" in result.output

    def test_saves_user_key_to_keyring(self):
        mock_store = MagicMock(spec=KeyringCredentialStore)
        mock_store.set_secret.return_value = True
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        with (
            patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config"),
        ):
            result = runner.invoke(
                app,
                ["credentials", "add", "user", "--secret", "rl_user_new"],
            )
            assert result.exit_code == 0
            assert "credential store" in result.output


# ── enroll ───────────────────────────────────────────────────────────


class TestEnroll:
    def test_success(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"api_key": "rl_enrolled_key"}

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response

        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch("runlayer_cli.config.save_config") as mock_save,
            patch(
                "runlayer_cli.cli_persistence.write_enrollment_marker"
            ) as mock_marker,
            patch(
                "runlayer_cli.enrollment.httpx.Client",
                return_value=mock_client,
            ),
        ):
            result = runner.invoke(
                app,
                [
                    "credentials",
                    "enroll",
                    "rl_enroll_testkey",
                    "--username",
                    "alice",
                    "--device-name",
                    "macbook",
                ],
            )
            assert result.exit_code == 0
            assert "Enrollment successful" in result.output
            mock_save.assert_called_once()
            mock_marker.assert_called_once_with("https://app.runlayer.com")
            call_args = mock_client.post.call_args
            assert "/api/v1/mdm/enroll" in call_args[0][0]
            body = call_args[1]["json"]
            assert body["username"] == "alice"
            assert body["device_name"] == "macbook"

    def test_http_error(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Invalid enrollment key"}

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response

        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch(
                "runlayer_cli.enrollment.httpx.Client",
                return_value=mock_client,
            ),
        ):
            result = runner.invoke(app, ["credentials", "enroll", "rl_enroll_bad"])
            assert result.exit_code == 1
            assert "401" in result.output
            assert "Invalid enrollment key" in result.output

    def test_network_error(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.side_effect = httpx.ConnectError("Connection refused")

        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch(
                "runlayer_cli.enrollment.httpx.Client",
                return_value=mock_client,
            ),
        ):
            result = runner.invoke(app, ["credentials", "enroll", "rl_enroll_test"])
            assert result.exit_code == 2
            assert "Failed to connect" in result.output

    def test_missing_api_key_in_response(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"other": "data"}

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response

        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch(
                "runlayer_cli.enrollment.httpx.Client",
                return_value=mock_client,
            ),
        ):
            result = runner.invoke(app, ["credentials", "enroll", "rl_enroll_test"])
            assert result.exit_code == 1
            assert "did not contain api_key" in result.output

    @pytest.mark.parametrize("body", [None, [1, 2], 42, "string"])
    def test_non_dict_json_response(self, body):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {"url": "https://app.runlayer.com"},
            },
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = body

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response

        with (
            patch("runlayer_cli.commands.credentials.load_config", return_value=config),
            patch(
                "runlayer_cli.enrollment.httpx.Client",
                return_value=mock_client,
            ),
        ):
            result = runner.invoke(app, ["credentials", "enroll", "rl_enroll_test"])
            assert result.exit_code == 1
            assert "did not contain api_key" in result.output


# ── check ────────────────────────────────────────────────────────────


class TestCheck:
    def test_both_present(self):
        config = _base_config()
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                ["credentials", "check", "--org-api-key", "mcp-watch"],
            )
            assert result.exit_code == 0
            assert "user: ok" in result.output
            assert "org (mcp-watch): ok" in result.output

    def test_user_missing(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "org_api_keys": {"mcp-watch": "rl_org_aaaaaa"},
                }
            },
        )
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                ["credentials", "check", "--org-api-key", "mcp-watch"],
            )
            assert result.exit_code == 1
            assert "user: missing" in result.output
            assert "org (mcp-watch): ok" in result.output

    def test_org_missing(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                }
            },
        )
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                ["credentials", "check", "--org-api-key", "mcp-watch"],
            )
            assert result.exit_code == 1
            assert "user: ok" in result.output
            assert "org (mcp-watch): missing" in result.output

    def test_skip_org_check(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                }
            },
        )
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                ["credentials", "check", "--skip-org-check"],
            )
            assert result.exit_code == 0
            assert "user: ok" in result.output
            assert "org" not in result.output

    def test_skip_user_check(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "org_api_keys": {"mcp-watch": "rl_org_aaaaaa"},
                }
            },
        )
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                [
                    "credentials",
                    "check",
                    "--skip-user-check",
                    "--org-api-key",
                    "mcp-watch",
                ],
            )
            assert result.exit_code == 0
            assert "user" not in result.output
            assert "org (mcp-watch): ok" in result.output

    def test_org_check_requires_label(self):
        config = _base_config()
        with patch(
            "runlayer_cli.commands.credentials.load_config", return_value=config
        ):
            result = runner.invoke(app, ["credentials", "check"])
            assert result.exit_code == 1
            assert "--org-api-key is required" in result.output
