"""Tests for authentication commands."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from runlayer_cli.config import Config
from runlayer_cli.credential_store import KeyringCredentialStore, reset_credential_store
from runlayer_cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def _disable_keyring_store():
    """Default tests to YAML-backed secrets by disabling keyring."""
    reset_credential_store()
    with (
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
        patch("runlayer_cli.commands.auth.get_keyring_store", return_value=None),
    ):
        yield
    reset_credential_store()


def _create_mock_config(
    default_host: str | None = None, hosts: dict | None = None
) -> Config:
    """Create a Config object for testing."""
    config = Config(default_host=default_host, hosts=hosts or {})
    return config


def test_login_requires_host_when_no_config():
    """Test that login fails with clear error when no --host and no config."""
    with patch("runlayer_cli.commands.auth.load_config") as mock_load:
        mock_load.return_value = _create_mock_config()

        result = runner.invoke(app, ["login"])

        assert result.exit_code == 1
        assert (
            "No host configured" in result.output or "provide --host" in result.output
        )


def test_login_uses_host_from_config():
    """Test that login initiates device flow with host from config."""
    mock_authorize_response = MagicMock()
    mock_authorize_response.status_code = 200
    mock_authorize_response.json.return_value = {
        "device_code": "test_device_code",
        "user_code": "TEST-CODE",
        "verification_uri": "https://example.com/device",
        "verification_uri_complete": "https://example.com/device?user_code=TEST-CODE",
        "expires_in": 1,  # Short timeout
        "interval": 1,
    }

    mock_pending_response = MagicMock()
    mock_pending_response.status_code = 202
    mock_pending_response.json.return_value = {"detail": "authorization_pending"}

    with patch("runlayer_cli.commands.auth.load_config") as mock_load:
        with patch("runlayer_cli.commands.auth.httpx.Client") as mock_client_class:
            with patch("runlayer_cli.commands.auth.webbrowser.open"):
                with patch("runlayer_cli.commands.auth.time.sleep"):
                    mock_load.return_value = _create_mock_config(
                        default_host="https://example.com"
                    )

                    mock_client = MagicMock()
                    mock_client.__enter__ = MagicMock(return_value=mock_client)
                    mock_client.__exit__ = MagicMock(return_value=False)
                    mock_client.post.side_effect = [
                        mock_authorize_response,
                        mock_pending_response,
                    ]
                    mock_client_class.return_value = mock_client

                    # Will timeout since auth never completes
                    result = runner.invoke(app, ["login"])

                    # Should have called the device authorize endpoint
                    mock_client.post.assert_called()
                    first_call = mock_client.post.call_args_list[0]
                    assert "/api/v1/cli/device/authorize" in first_call[0][0]


def test_login_displays_user_code():
    """Test that login displays the user code for manual entry."""
    mock_authorize_response = MagicMock()
    mock_authorize_response.status_code = 200
    mock_authorize_response.json.return_value = {
        "device_code": "test_device_code",
        "user_code": "ABCD-1234",
        "verification_uri": "https://example.com/device",
        "verification_uri_complete": "https://example.com/device?user_code=ABCD-1234",
        "expires_in": 1,  # Very short timeout
        "interval": 1,
    }

    mock_pending_response = MagicMock()
    mock_pending_response.status_code = 202
    mock_pending_response.json.return_value = {"detail": "authorization_pending"}

    with patch("runlayer_cli.commands.auth.load_config") as mock_load:
        with patch("runlayer_cli.commands.auth.httpx.Client") as mock_client_class:
            with patch("runlayer_cli.commands.auth.webbrowser.open"):
                with patch("runlayer_cli.commands.auth.time.sleep"):
                    mock_load.return_value = _create_mock_config(
                        default_host="https://example.com"
                    )

                    mock_client = MagicMock()
                    mock_client.__enter__ = MagicMock(return_value=mock_client)
                    mock_client.__exit__ = MagicMock(return_value=False)
                    # First call is authorize, subsequent calls are token polling
                    mock_client.post.side_effect = [
                        mock_authorize_response,
                        mock_pending_response,
                    ]
                    mock_client_class.return_value = mock_client

                    result = runner.invoke(app, ["login"])

                    # Should display the user code
                    assert "ABCD-1234" in result.output


def test_login_success_saves_credentials():
    """Test that successful login saves API key via credential store."""
    mock_authorize_response = MagicMock()
    mock_authorize_response.status_code = 200
    mock_authorize_response.json.return_value = {
        "device_code": "test_device_code",
        "user_code": "ABCD-1234",
        "verification_uri": "https://example.com/device",
        "verification_uri_complete": "https://example.com/device?user_code=ABCD-1234",
        "expires_in": 300,
        "interval": 5,
    }

    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {"api_key": "test_api_key_123"}

    mock_store = MagicMock(spec=KeyringCredentialStore)
    mock_store.set_secret.return_value = True

    with patch("runlayer_cli.commands.auth.load_config") as mock_load:
        with patch("runlayer_cli.commands.auth.save_config") as mock_save:
            with patch("runlayer_cli.commands.auth.httpx.Client") as mock_client_class:
                with patch("runlayer_cli.commands.auth.webbrowser.open"):
                    with patch("runlayer_cli.commands.auth.time.sleep"):
                        with patch(
                            "runlayer_cli.config.get_keyring_store",
                            return_value=mock_store,
                        ):
                            mock_load.return_value = _create_mock_config(
                                default_host="https://example.com"
                            )

                            mock_client = MagicMock()
                            mock_client.__enter__ = MagicMock(return_value=mock_client)
                            mock_client.__exit__ = MagicMock(return_value=False)
                            mock_client.post.side_effect = [
                                mock_authorize_response,
                                mock_token_response,
                            ]
                            mock_client_class.return_value = mock_client

                            result = runner.invoke(app, ["login"])

                            assert result.exit_code == 0
                            assert "Successfully authenticated" in result.output
                            assert "your system's credential store" in result.output

                            mock_save.assert_called_once()
                            saved_config = mock_save.call_args[0][0]
                            assert saved_config.default_host == "https://example.com"
                            assert "secret" not in saved_config.hosts["example.com"]


def test_login_to_second_host_preserves_first_host_credentials():
    """Test that logging into a second host preserves the first host's credentials."""
    mock_authorize_response = MagicMock()
    mock_authorize_response.status_code = 200
    mock_authorize_response.json.return_value = {
        "device_code": "test_device_code",
        "user_code": "ABCD-1234",
        "verification_uri": "https://staging.example.com/device",
        "verification_uri_complete": "https://staging.example.com/device?user_code=ABCD-1234",
        "expires_in": 300,
        "interval": 5,
    }

    mock_token_response = MagicMock()
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {"api_key": "staging_api_key"}

    mock_store = MagicMock(spec=KeyringCredentialStore)
    mock_store.set_secret.return_value = True

    # First host still on file (unmigrated); new login uses credential store for the second host.
    initial_config = _create_mock_config(
        default_host="https://example.com",
        hosts={
            "example.com": {
                "url": "https://example.com",
                "secret": "prod_api_key",
            }
        },
    )

    with patch("runlayer_cli.commands.auth.load_config") as mock_load:
        with patch("runlayer_cli.commands.auth.save_config") as mock_save:
            with patch("runlayer_cli.commands.auth.httpx.Client") as mock_client_class:
                with patch("runlayer_cli.commands.auth.webbrowser.open"):
                    with patch("runlayer_cli.commands.auth.time.sleep"):
                        with patch(
                            "runlayer_cli.config.get_keyring_store",
                            return_value=mock_store,
                        ):
                            mock_load.return_value = initial_config

                            mock_client = MagicMock()
                            mock_client.__enter__ = MagicMock(return_value=mock_client)
                            mock_client.__exit__ = MagicMock(return_value=False)
                            mock_client.post.side_effect = [
                                mock_authorize_response,
                                mock_token_response,
                            ]
                            mock_client_class.return_value = mock_client

                            result = runner.invoke(
                                app,
                                ["login", "--host", "https://staging.example.com"],
                            )

                            assert result.exit_code == 0

                            mock_save.assert_called_once()
                            saved_config = mock_save.call_args[0][0]

                            assert saved_config.hosts["example.com"].get("secret") == (
                                "prod_api_key"
                            )
                            assert "staging.example.com" in saved_config.hosts
                            assert (
                                "secret"
                                not in saved_config.hosts["staging.example.com"]
                            )
                            assert (
                                saved_config.default_host
                                == "https://staging.example.com"
                            )


class TestConfigSecurity:
    """Tests for credential isolation security."""

    def test_credentials_not_leaked_to_different_host(self):
        """Test that credentials for one host are not used for a different host."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "secret_for_runlayer",
                }
            },
        )

        # Should NOT return credentials for a different host
        assert config.get_secret_for_host("https://malicious-server.com") is None
        assert (
            config.get_secret_for_host("http://app.runlayer.com") is None
        )  # Different scheme

    def test_scheme_mismatch_does_not_return_credentials(self):
        """Test that http://host and https://host are treated as different hosts."""
        config = Config(
            default_host="https://localhost:8000",
            hosts={
                "localhost:8000": {
                    "url": "https://localhost:8000",
                    "secret": "https_secret",
                }
            },
        )

        # HTTPS should work
        assert config.get_secret_for_host("https://localhost:8000") == "https_secret"

        # HTTP should NOT return the HTTPS secret (security!)
        assert config.get_secret_for_host("http://localhost:8000") is None

    def test_multiple_hosts_isolated(self):
        """Test that multiple hosts can store credentials independently."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "prod_secret",
                },
                "staging.runlayer.com": {
                    "url": "https://staging.runlayer.com",
                    "secret": "staging_secret",
                },
                "localhost:8000": {
                    "url": "http://localhost:8000",
                    "secret": "local_secret",
                },
            },
        )

        assert config.get_secret_for_host("https://app.runlayer.com") == "prod_secret"
        assert (
            config.get_secret_for_host("https://staging.runlayer.com")
            == "staging_secret"
        )
        assert config.get_secret_for_host("http://localhost:8000") == "local_secret"

        # Cross-host lookups should fail
        assert config.get_secret_for_host("https://other.com") is None

    def test_url_normalization(self):
        """Test that URLs with trailing slashes are normalized."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "my_secret",
                }
            },
        )

        # Both with and without trailing slash should work
        assert config.get_secret_for_host("https://app.runlayer.com") == "my_secret"
        assert config.get_secret_for_host("https://app.runlayer.com/") == "my_secret"

    def test_clear_host_scheme_mismatch_does_not_delete(self):
        """Test that clear_host with wrong scheme doesn't delete credentials.

        Regression test: clear_host should verify stored_url == url before deleting,
        consistent with get_secret_for_host which also validates the URL scheme.
        """
        config = Config(
            default_host="https://localhost:8000",
            hosts={
                "localhost:8000": {
                    "url": "https://localhost:8000",
                    "secret": "https_secret",
                }
            },
        )

        # Try to clear with wrong scheme - should return False and NOT delete
        result = config.clear_host("http://localhost:8000")
        assert result is False

        # Credentials should still exist
        assert config.get_secret_for_host("https://localhost:8000") == "https_secret"
        assert "localhost:8000" in config.hosts

        # Now clear with correct scheme - should work
        result = config.clear_host("https://localhost:8000")
        assert result is True
        assert "localhost:8000" not in config.hosts


class TestLogout:
    """Tests for logout command."""

    def test_logout_clears_all_credentials(self):
        """Test that logout without --host clears credential store and config."""
        mock_store = MagicMock(spec=KeyringCredentialStore)

        with patch("runlayer_cli.commands.auth.load_config") as mock_load:
            with patch("runlayer_cli.commands.auth.clear_config") as mock_clear:
                with patch(
                    "runlayer_cli.commands.auth.get_keyring_store",
                    return_value=mock_store,
                ):
                    mock_load.return_value = _create_mock_config(
                        default_host="https://example.com",
                        hosts={
                            "example.com": {
                                "url": "https://example.com",
                                "secret": "secret1",
                            }
                        },
                    )

                    result = runner.invoke(app, ["logout"])

                    assert result.exit_code == 0
                    assert "All credentials cleared" in result.output
                    mock_store.delete_all_secrets.assert_called_once()
                    mock_clear.assert_called_once()

    def test_logout_with_host_clears_specific_host(self):
        """Test that logout --host clears only that host's credentials."""
        initial_config = _create_mock_config(
            default_host="https://example.com",
            hosts={
                "example.com": {
                    "url": "https://example.com",
                    "secret": "secret1",
                },
                "staging.example.com": {
                    "url": "https://staging.example.com",
                    "secret": "secret2",
                },
            },
        )

        with patch("runlayer_cli.commands.auth.load_config") as mock_load:
            with patch("runlayer_cli.commands.auth.save_config") as mock_save:
                with patch(
                    "runlayer_cli.config.get_keyring_store",
                    return_value=MagicMock(spec=KeyringCredentialStore),
                ):
                    mock_load.return_value = initial_config

                    result = runner.invoke(
                        app, ["logout", "--host", "https://staging.example.com"]
                    )

                    assert result.exit_code == 0
                    assert (
                        "Credentials cleared for https://staging.example.com"
                        in result.output
                    )

                    mock_save.assert_called_once()
                    saved_config = mock_save.call_args[0][0]
                    assert "example.com" in saved_config.hosts
                    assert "staging.example.com" not in saved_config.hosts

    def test_logout_no_credentials_found(self):
        """Test logout when no credentials are stored."""
        with patch("runlayer_cli.commands.auth.load_config") as mock_load:
            mock_load.return_value = _create_mock_config()

            result = runner.invoke(app, ["logout"])

            assert "No credentials found" in result.output

    def test_logout_host_not_found(self):
        """Test logout --host when that host has no credentials."""
        with patch("runlayer_cli.commands.auth.load_config") as mock_load:
            mock_load.return_value = _create_mock_config(
                default_host="https://example.com",
                hosts={
                    "example.com": {
                        "url": "https://example.com",
                        "secret": "secret1",
                    }
                },
            )

            result = runner.invoke(app, ["logout", "--host", "https://nonexistent.com"])

            assert "No credentials found for https://nonexistent.com" in result.output

    def test_logout_wrong_scheme_does_not_delete_credentials(self):
        """Test that logout with wrong scheme doesn't delete credentials for correct scheme."""
        mock_store = MagicMock(spec=KeyringCredentialStore)

        initial_config = _create_mock_config(
            default_host="https://example.com",
            hosts={
                "example.com": {
                    "url": "https://example.com",
                    "secret": "https_secret",
                }
            },
        )

        with patch("runlayer_cli.commands.auth.load_config") as mock_load:
            with patch("runlayer_cli.commands.auth.save_config") as mock_save:
                with patch(
                    "runlayer_cli.config.get_keyring_store",
                    return_value=mock_store,
                ):
                    mock_load.return_value = initial_config

                    result = runner.invoke(
                        app, ["logout", "--host", "http://example.com"]
                    )

                    assert (
                        "No credentials found for http://example.com" in result.output
                    )
                    mock_save.assert_not_called()
                    # Credential store should NOT have been touched
                    mock_store.delete_secret.assert_not_called()
