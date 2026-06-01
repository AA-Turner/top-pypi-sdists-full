"""Tests for org-api-key CLI commands and Config org key methods."""

from unittest.mock import MagicMock, patch

import pytest
import typer
from click.exceptions import Exit
from typer.testing import CliRunner

from runlayer_cli.config import Config, resolve_credentials
from runlayer_cli.credential_store import KeyringCredentialStore, reset_credential_store
from runlayer_cli.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def _disable_keyring_store():
    """Default tests to YAML-backed secrets by disabling keyring."""
    reset_credential_store()
    with patch("runlayer_cli.config.get_keyring_store", return_value=None):
        yield
    reset_credential_store()


def _config_with_org_keys() -> Config:
    return Config(
        default_host="https://app.runlayer.com",
        hosts={
            "app.runlayer.com": {
                "url": "https://app.runlayer.com",
                "secret": "rl_user_key",
                "org_api_keys": {
                    "mcp-watch": "rl_org_aaaaaa",
                    "security": "rl_org_bbbbbb",
                },
            }
        },
    )


# ── Config model unit tests ──────────────────────────────────────────


class TestConfigOrgApiKeys:
    def test_get_org_api_key(self):
        config = _config_with_org_keys()
        assert (
            config.get_org_api_key("https://app.runlayer.com", "mcp-watch")
            == "rl_org_aaaaaa"
        )

    def test_get_org_api_key_missing_name(self):
        config = _config_with_org_keys()
        assert config.get_org_api_key("https://app.runlayer.com", "nonexistent") is None

    def test_get_org_api_key_missing_host(self):
        config = _config_with_org_keys()
        assert config.get_org_api_key("https://other.com", "mcp-watch") is None

    def test_get_org_api_key_no_org_keys_section(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                }
            },
        )
        assert config.get_org_api_key("https://app.runlayer.com", "any") is None

    def test_set_org_api_key_existing_host(self):
        config = _config_with_org_keys()
        config.set_org_api_key("https://app.runlayer.com", "new-key", "rl_org_cccccc")
        assert (
            config.get_org_api_key("https://app.runlayer.com", "new-key")
            == "rl_org_cccccc"
        )
        # existing keys preserved
        assert (
            config.get_org_api_key("https://app.runlayer.com", "mcp-watch")
            == "rl_org_aaaaaa"
        )

    def test_set_org_api_key_creates_host_entry(self):
        config = Config()
        config.set_org_api_key("https://new.host.com", "scan", "rl_org_dddddd")
        assert config.get_org_api_key("https://new.host.com", "scan") == "rl_org_dddddd"

    def test_set_org_api_key_scheme_mismatch_rejects(self):
        """set with http:// when config stores https:// must not silently write
        into the wrong host entry, making the key invisible to get/remove/list."""
        config = _config_with_org_keys()
        with pytest.raises(ValueError, match="scheme mismatch"):
            config.set_org_api_key(
                "http://app.runlayer.com", "bad-key", "rl_org_zzzzzz"
            )
        # Original https keys unaffected
        assert (
            config.get_org_api_key("https://app.runlayer.com", "mcp-watch")
            == "rl_org_aaaaaa"
        )

    def test_remove_org_api_key(self):
        config = _config_with_org_keys()
        assert (
            config.remove_org_api_key("https://app.runlayer.com", "mcp-watch") is True
        )
        assert config.get_org_api_key("https://app.runlayer.com", "mcp-watch") is None
        # other key still there
        assert (
            config.get_org_api_key("https://app.runlayer.com", "security")
            == "rl_org_bbbbbb"
        )

    def test_remove_org_api_key_not_found(self):
        config = _config_with_org_keys()
        assert config.remove_org_api_key("https://app.runlayer.com", "nope") is False

    def test_remove_last_org_api_key_cleans_section(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user",
                    "org_api_keys": {"only": "rl_org_only"},
                }
            },
        )
        config.remove_org_api_key("https://app.runlayer.com", "only")
        assert "org_api_keys" not in config.hosts["app.runlayer.com"]

    def test_list_org_api_keys(self):
        config = _config_with_org_keys()
        keys = config.list_org_api_keys("https://app.runlayer.com")
        assert set(keys.keys()) == {"mcp-watch", "security"}
        # values are truncated prefixes
        for prefix in keys.values():
            assert prefix.endswith("...")

    def test_list_org_api_keys_empty(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user",
                }
            },
        )
        assert config.list_org_api_keys("https://app.runlayer.com") == {}

    def test_set_host_credentials_preserves_org_keys(self):
        mock_store = MagicMock(spec=KeyringCredentialStore)
        mock_store.set_secret.return_value = True
        mock_store.get_secret.return_value = "rl_new_user_key"

        with patch("runlayer_cli.config.get_keyring_store", return_value=mock_store):
            config = _config_with_org_keys()
            config.set_host_credentials("https://app.runlayer.com", "rl_new_user_key")
            assert (
                config.get_secret_for_host("https://app.runlayer.com")
                == "rl_new_user_key"
            )
            assert (
                config.get_org_api_key("https://app.runlayer.com", "mcp-watch")
                == "rl_org_aaaaaa"
            )

    def test_to_dict_includes_org_api_keys(self):
        config = _config_with_org_keys()
        d = config.to_dict()
        host_data = d["hosts"]["app.runlayer.com"]
        assert host_data["org_api_keys"]["mcp-watch"] == "rl_org_aaaaaa"


# ── CLI command tests ────────────────────────────────────────────────


class TestOrgApiKeyAddCommand:
    def test_add_saves_key(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user",
                }
            },
        )
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            with patch("runlayer_cli.commands.org_api_key.save_config") as mock_save:
                result = runner.invoke(
                    app,
                    ["org-api-key", "add", "my-key", "--secret", "rl_org_test123"],
                )
                assert result.exit_code == 0
                assert "saved" in result.output
                mock_save.assert_called_once()
                saved = mock_save.call_args[0][0]
                assert (
                    saved.get_org_api_key("https://app.runlayer.com", "my-key")
                    == "rl_org_test123"
                )

    def test_add_requires_host(self):
        config = Config()
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                ["org-api-key", "add", "my-key", "--secret", "rl_org_x"],
            )
            assert result.exit_code == 1
            assert "No host configured" in result.output

    def test_add_scheme_mismatch_errors(self):
        config = _config_with_org_keys()
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            result = runner.invoke(
                app,
                [
                    "org-api-key",
                    "add",
                    "bad",
                    "--secret",
                    "rl_org_x",
                    "--host",
                    "http://app.runlayer.com",
                ],
            )
            assert result.exit_code == 1
            assert "scheme mismatch" in result.output.lower()


class TestOrgApiKeyRemoveCommand:
    def test_remove_existing(self):
        config = _config_with_org_keys()
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            with patch("runlayer_cli.commands.org_api_key.save_config") as mock_save:
                result = runner.invoke(app, ["org-api-key", "remove", "mcp-watch"])
                assert result.exit_code == 0
                assert "removed" in result.output
                mock_save.assert_called_once()

    def test_remove_nonexistent(self):
        config = _config_with_org_keys()
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            result = runner.invoke(app, ["org-api-key", "remove", "nope"])
            assert result.exit_code == 0
            assert "No org API key 'nope'" in result.output


class TestOrgApiKeyListCommand:
    def test_list_shows_keys(self):
        config = _config_with_org_keys()
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            result = runner.invoke(app, ["org-api-key", "list"])
            assert result.exit_code == 0
            assert "mcp-watch" in result.output
            assert "security" in result.output

    def test_list_uses_global_host_flag(self):
        """Global --host flag should override config.default_host."""
        config = Config(
            default_host="https://default.runlayer.com",
            hosts={
                "default.runlayer.com": {
                    "url": "https://default.runlayer.com",
                    "secret": "rl_user",
                },
                "custom.runlayer.com": {
                    "url": "https://custom.runlayer.com",
                    "secret": "rl_user2",
                    "org_api_keys": {"custom-key": "rl_org_custom"},
                },
            },
        )
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            result = runner.invoke(
                app, ["--host", "https://custom.runlayer.com", "org-api-key", "list"]
            )
            assert result.exit_code == 0
            assert "custom-key" in result.output
            assert "custom.runlayer.com" in result.output

    def test_list_empty(self):
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user",
                }
            },
        )
        with patch(
            "runlayer_cli.commands.org_api_key.load_config", return_value=config
        ):
            result = runner.invoke(app, ["org-api-key", "list"])
            assert result.exit_code == 0
            assert "No org API keys" in result.output


# ── Credential resolution with --org-api-key ─────────────────────────


class TestOrgApiKeyResolution:
    def test_global_org_api_key_flag_resolves(self):
        """--org-api-key on root command resolves named key."""
        config = _config_with_org_keys()
        with patch("runlayer_cli.config.load_config", return_value=config):
            from runlayer_cli.config import resolve_credentials
            import typer

            # Simulate context chain: main sets org_api_key_name
            ctx = typer.Context(typer.main.get_command(app))
            ctx.ensure_object(dict)
            ctx.obj["org_api_key_name"] = "mcp-watch"
            ctx.obj["secret"] = None
            ctx.obj["host"] = None

            creds = resolve_credentials(ctx, require_auth=False)
            assert creds["secret"] == "rl_org_aaaaaa"
            assert creds["host"] == "https://app.runlayer.com"

    def test_secret_flag_takes_priority_over_org_api_key(self):
        """--secret overrides --org-api-key."""
        config = _config_with_org_keys()
        with patch("runlayer_cli.config.load_config", return_value=config):
            from runlayer_cli.config import resolve_credentials
            import typer

            ctx = typer.Context(typer.main.get_command(app))
            ctx.ensure_object(dict)
            ctx.obj["secret"] = "rl_direct_secret"
            ctx.obj["org_api_key_name"] = "mcp-watch"
            ctx.obj["host"] = None

            creds = resolve_credentials(ctx, require_auth=False)
            assert creds["secret"] == "rl_direct_secret"

    def test_org_key_as_default_secret_triggers_login(self):
        """rl_org_ stored as host secret triggers device auth flow."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_org_managed_key",
                }
            },
        )
        # After login, config returns a user key
        config_after = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key_from_login",
                }
            },
        )
        with patch(
            "runlayer_cli.config.load_config", side_effect=[config, config_after]
        ):
            with patch("runlayer_cli.commands.auth.login") as mock_login:
                from runlayer_cli.config import resolve_credentials
                import typer

                ctx = typer.Context(typer.main.get_command(app))
                ctx.ensure_object(dict)
                ctx.obj["secret"] = None
                ctx.obj["org_api_key_name"] = None
                ctx.obj["host"] = None

                creds = resolve_credentials(ctx, require_auth=True)
                mock_login.assert_called_once_with(host="https://app.runlayer.com")
                assert creds["secret"] == "rl_user_key_from_login"

    def test_org_key_as_default_secret_no_auth_returns_as_is(self):
        """require_auth=False with rl_org_ secret returns it without login."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_org_managed_key",
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            from runlayer_cli.config import resolve_credentials
            import typer

            ctx = typer.Context(typer.main.get_command(app))
            ctx.ensure_object(dict)
            ctx.obj["secret"] = None
            ctx.obj["org_api_key_name"] = None
            ctx.obj["host"] = None

            creds = resolve_credentials(ctx, require_auth=False)
            assert creds["secret"] == "rl_org_managed_key"

    def test_org_key_as_default_secret_allow_org_key_skips_login(self):
        """allow_org_key=True with rl_org_ secret returns it without login (scan use case)."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_org_managed_key",
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            from runlayer_cli.config import resolve_credentials
            import typer

            ctx = typer.Context(typer.main.get_command(app))
            ctx.ensure_object(dict)
            ctx.obj["secret"] = None
            ctx.obj["org_api_key_name"] = None
            ctx.obj["host"] = None

            creds = resolve_credentials(ctx, require_auth=True, allow_org_key=True)
            assert creds["secret"] == "rl_org_managed_key"

    def test_cli_secret_flag_with_org_prefix_skips_login(self):
        """Explicit --secret rl_org_... does NOT trigger login."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            from runlayer_cli.config import resolve_credentials
            import typer

            ctx = typer.Context(typer.main.get_command(app))
            ctx.ensure_object(dict)
            ctx.obj["secret"] = "rl_org_explicit"
            ctx.obj["org_api_key_name"] = None
            ctx.obj["host"] = None

            creds = resolve_credentials(ctx, require_auth=True)
            assert creds["secret"] == "rl_org_explicit"

    def test_org_api_key_not_found_exits(self):
        """--org-api-key with unknown name exits with error."""
        config = _config_with_org_keys()
        with patch("runlayer_cli.config.load_config", return_value=config):
            from runlayer_cli.config import resolve_credentials
            import typer
            import pytest
            from click.exceptions import Exit

            ctx = typer.Context(typer.main.get_command(app))
            ctx.ensure_object(dict)
            ctx.obj["secret"] = None
            ctx.obj["org_api_key_name"] = "nonexistent"
            ctx.obj["host"] = None

            with pytest.raises(Exit):
                resolve_credentials(ctx, require_auth=False)


class TestImplicitOrgKeyResolution:
    """Tests for implicit_org_key_label / interactive_login_on_missing kwargs."""

    def _make_ctx(self, *, secret=None, org_api_key_name=None, host=None):
        ctx = typer.Context(typer.main.get_command(app))
        ctx.ensure_object(dict)
        ctx.obj["secret"] = secret
        ctx.obj["org_api_key_name"] = org_api_key_name
        ctx.obj["host"] = host
        return ctx

    def test_implicit_org_key_preferred_over_user_secret(self):
        """When both ai_watch_mdm org key and user secret exist, org key wins."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                    "org_api_keys": {"ai_watch_mdm": "rl_org_mdm_key"},
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
            )
            assert creds["secret"] == "rl_org_mdm_key"

    def test_implicit_org_key_only_no_user_secret(self):
        """Only ai_watch_mdm org key stored, no user secret — returns org key."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "org_api_keys": {"ai_watch_mdm": "rl_org_mdm_key"},
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
            )
            assert creds["secret"] == "rl_org_mdm_key"

    def test_falls_back_to_user_secret_when_no_implicit_org_key(self):
        """No ai_watch_mdm key stored, user secret present — returns user secret."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
            )
            assert creds["secret"] == "rl_user_key"

    def test_no_login_when_interactive_disabled(self):
        """interactive_login_on_missing=False exits instead of calling login."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.commands.auth.login") as mock_login,
        ):
            with pytest.raises(Exit):
                resolve_credentials(
                    self._make_ctx(),
                    require_auth=True,
                    allow_org_key=True,
                    implicit_org_key_label="ai_watch_mdm",
                    interactive_login_on_missing=False,
                )
            mock_login.assert_not_called()

    def test_interactive_login_passes_no_ca_bundle_when_called_programmatically(self):
        """Programmatic login must not pass Typer's OptionInfo default as ca_bundle."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch(
                "runlayer_cli.commands.auth.set_ca_bundle_path",
                side_effect=Exit(1),
            ) as mock_set_ca_bundle_path,
        ):
            with pytest.raises(Exit):
                resolve_credentials(self._make_ctx(), require_auth=True)

            mock_set_ca_bundle_path.assert_called_once_with(None)

    def test_default_resolve_does_not_auto_discover_org_key(self):
        """Without implicit_org_key_label, ai_watch_mdm org key is NOT used."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "org_api_keys": {"ai_watch_mdm": "rl_org_mdm_key"},
                }
            },
        )
        config_after = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_from_login",
                }
            },
        )
        with (
            patch(
                "runlayer_cli.config.load_config",
                side_effect=[config, config_after],
            ),
            patch("runlayer_cli.commands.auth.login"),
        ):
            creds = resolve_credentials(
                self._make_ctx(), require_auth=True, allow_org_key=False
            )
            assert creds["secret"] == "rl_user_from_login"

    def test_explicit_org_api_key_name_takes_priority(self):
        """Explicit --org-api-key still takes priority over implicit label."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_key",
                    "org_api_keys": {
                        "ai_watch_mdm": "rl_org_mdm_key",
                        "other": "rl_org_other",
                    },
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            creds = resolve_credentials(
                self._make_ctx(org_api_key_name="other"),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
            )
            assert creds["secret"] == "rl_org_other"

    def test_cli_secret_takes_priority_over_implicit_org_key(self):
        """--secret always wins, even when implicit org key is configured."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "org_api_keys": {"ai_watch_mdm": "rl_org_mdm_key"},
                }
            },
        )
        with patch("runlayer_cli.config.load_config", return_value=config):
            creds = resolve_credentials(
                self._make_ctx(secret="rl_explicit"),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
            )
            assert creds["secret"] == "rl_explicit"


class TestMDMManagedOrgKeyFallback:
    """Tests for MDM-managed plist/registry fallback in resolve_credentials."""

    def _make_ctx(self, *, secret=None, org_api_key_name=None, host=None):
        ctx = typer.Context(typer.main.get_command(app))
        ctx.ensure_object(dict)
        ctx.obj["secret"] = secret
        ctx.obj["org_api_key_name"] = org_api_key_name
        ctx.obj["host"] = host
        return ctx

    def test_mdm_managed_org_key_used_when_config_yaml_missing(self):
        """ENG-2842 repro: config.yaml has no org key, MDM plist does.

        The MDM wrapper runs `runlayer scan --org-api-key ai_watch_mdm`.
        If `credentials add org` didn't persist, config.yaml is empty
        but the plist still has the key — should fall back to it.
        """
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(org_api_key_name="ai_watch_mdm"),
                require_auth=True,
                allow_org_key=True,
            )
            assert creds["secret"] == "rl_org_mdm_plist"

    def test_mdm_managed_org_key_used_via_implicit_label(self):
        """implicit_org_key_label path also falls back to MDM-managed key."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
                interactive_login_on_missing=False,
            )
            assert creds["secret"] == "rl_org_mdm_plist"

    def test_mdm_managed_org_key_skipped_when_host_mismatch(self):
        """MDM-managed key for a different host is NOT used."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        managed = {
            "host": "https://other.example.com",
            "org_api_key": "rl_org_wrong_host",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            with pytest.raises(Exit):
                resolve_credentials(
                    self._make_ctx(org_api_key_name="ai_watch_mdm"),
                    require_auth=True,
                    allow_org_key=True,
                    interactive_login_on_missing=False,
                )

    def test_config_yaml_org_key_preferred_over_mdm_managed(self):
        """config.yaml org key wins over MDM-managed — explicit > implicit."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "org_api_keys": {"ai_watch_mdm": "rl_org_from_yaml"},
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_from_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(org_api_key_name="ai_watch_mdm"),
                require_auth=True,
                allow_org_key=True,
            )
            assert creds["secret"] == "rl_org_from_yaml"

    def test_mdm_managed_org_key_beats_user_secret(self):
        """MDM org key should win over a stale user secret (wrong-tenant guard)."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                    "secret": "rl_user_stale",
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
                interactive_login_on_missing=False,
            )
            assert creds["secret"] == "rl_org_mdm_plist"

    def test_unknown_org_key_label_does_not_fall_back_to_mdm(self):
        """ENG-2842: unknown --org-api-key label must NOT silently use MDM key.

        A typo or non-MDM label should error out, not authenticate with the
        ai_watch_mdm key from MDM-managed config.
        """
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            with pytest.raises(Exit):
                resolve_credentials(
                    self._make_ctx(org_api_key_name="ai_watch_typo"),
                    require_auth=True,
                    allow_org_key=True,
                    interactive_login_on_missing=False,
                )

    def test_unknown_implicit_label_does_not_fall_back_to_mdm(self):
        """Defensive: implicit label other than ai_watch_mdm must not use MDM key."""
        config = Config(
            default_host="https://app.runlayer.com",
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            with pytest.raises(Exit):
                resolve_credentials(
                    self._make_ctx(),
                    require_auth=True,
                    allow_org_key=True,
                    implicit_org_key_label="some_other_label",
                    interactive_login_on_missing=False,
                )

    def test_single_host_fallback_with_mdm_org_key(self):
        """No --host, no default_host, but one host in config → uses that host.

        After `credentials add org ai_watch_mdm --host $H`, config.yaml has one
        host entry but no default_host. Should infer the host + fall back to MDM
        plist for the org key.
        """
        config = Config(
            default_host=None,
            hosts={
                "app.runlayer.com": {
                    "url": "https://app.runlayer.com",
                }
            },
        )
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
                interactive_login_on_missing=False,
            )
            assert creds["host"] == "https://app.runlayer.com"
            assert creds["secret"] == "rl_org_mdm_plist"

    def test_mdm_managed_host_used_when_config_yaml_empty(self):
        """ENG-2842 repro: config.yaml entirely empty, MDM provides host+key.

        Fresh MDM-deployed device: no `runlayer login`, no `credentials add`,
        so config.yaml has no default_host and no hosts entries. The MDM
        plist/registry is the sole source of truth for host AND org key.
        Must not exit with "No host configured".
        """
        config = Config(default_host=None, hosts={})
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(org_api_key_name="ai_watch_mdm"),
                require_auth=True,
                allow_org_key=True,
                interactive_login_on_missing=False,
            )
            assert creds["host"] == "https://app.runlayer.com"
            assert creds["secret"] == "rl_org_mdm_plist"

    def test_mdm_managed_host_used_when_config_yaml_empty_implicit_label(self):
        """Same as above via implicit_org_key_label (scan's default path)."""
        config = Config(default_host=None, hosts={})
        managed = {
            "host": "https://app.runlayer.com",
            "org_api_key": "rl_org_mdm_plist",
        }
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            creds = resolve_credentials(
                self._make_ctx(),
                require_auth=True,
                allow_org_key=True,
                implicit_org_key_label="ai_watch_mdm",
                interactive_login_on_missing=False,
            )
            assert creds["host"] == "https://app.runlayer.com"
            assert creds["secret"] == "rl_org_mdm_plist"

    def test_mdm_managed_org_key_not_leaked_when_managed_host_missing(self):
        """Managed plist with org_api_key but no host must NOT authorize any host.

        Without a managed host we can't prove the key is intended for the
        effective host (which may come from --host). Sending the key would
        leak it to a user-controlled tenant.
        """
        config = Config(
            default_host="https://attacker.example.com",
            hosts={
                "attacker.example.com": {
                    "url": "https://attacker.example.com",
                }
            },
        )
        managed = {"org_api_key": "rl_org_mdm_plist"}
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            with pytest.raises(Exit):
                resolve_credentials(
                    self._make_ctx(org_api_key_name="ai_watch_mdm"),
                    require_auth=True,
                    allow_org_key=True,
                    interactive_login_on_missing=False,
                )

    def test_mdm_managed_org_key_not_leaked_via_implicit_label_when_host_missing(
        self,
    ):
        """implicit_org_key_label path also refuses to use MDM key without managed host."""
        config = Config(
            default_host="https://attacker.example.com",
            hosts={
                "attacker.example.com": {
                    "url": "https://attacker.example.com",
                }
            },
        )
        managed = {"org_api_key": "rl_org_mdm_plist"}
        with (
            patch("runlayer_cli.config.load_config", return_value=config),
            patch("runlayer_cli.config.read_managed_config", return_value=managed),
        ):
            with pytest.raises(Exit):
                resolve_credentials(
                    self._make_ctx(),
                    require_auth=True,
                    allow_org_key=True,
                    implicit_org_key_label="ai_watch_mdm",
                    interactive_login_on_missing=False,
                )
