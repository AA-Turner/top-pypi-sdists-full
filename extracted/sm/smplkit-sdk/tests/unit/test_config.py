"""Tests for SDK configuration resolution."""

from __future__ import annotations

import pytest

from smplkit import Error
from smplkit._config import _parse_bool, resolve_config


class TestResolveConfigDefaults:
    """Step 1: SDK hardcoded defaults."""

    def test_defaults_applied(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_BASE_DOMAIN", raising=False)
        monkeypatch.delenv("SMPLKIT_SCHEME", raising=False)
        monkeypatch.delenv("SMPLKIT_DEBUG", raising=False)
        monkeypatch.delenv("SMPLKIT_TELEMETRY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        cfg = resolve_config(
            api_key="sk_api_test",
            environment="test",
            service="svc",
            _home_dir=tmp_path,
        )
        assert cfg.base_domain == "smplkit.com"
        assert cfg.scheme == "https"
        assert cfg.debug is False
        assert cfg.telemetry is True


class TestResolveConfigFile:
    """Step 2: Configuration file."""

    def test_default_profile(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_file\nenvironment = production\nservice = my-svc\n")
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_api_file"
        assert cfg.environment == "production"
        assert cfg.service == "my-svc"

    def test_common_section_inherited(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text(
            "[common]\nenvironment = production\nservice = my-app\n\n[default]\napi_key = sk_api_default\n"
        )
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.environment == "production"
        assert cfg.service == "my-app"
        assert cfg.api_key == "sk_api_default"

    def test_profile_overrides_common(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text(
            "[common]\n"
            "environment = production\n"
            "service = my-app\n"
            "\n"
            "[local]\n"
            "api_key = sk_api_local\n"
            "environment = development\n"
            "base_domain = localhost\n"
            "scheme = http\n"
        )
        cfg = resolve_config(profile="local", _home_dir=tmp_path)
        assert cfg.environment == "development"
        assert cfg.service == "my-app"  # inherited from [common]
        assert cfg.api_key == "sk_api_local"
        assert cfg.base_domain == "localhost"
        assert cfg.scheme == "http"

    def test_profile_via_env_var(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.setenv("SMPLKIT_PROFILE", "staging")
        config = tmp_path / ".smplkit"
        config.write_text("[common]\nservice = my-app\n\n[staging]\napi_key = sk_api_staging\nenvironment = staging\n")
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_api_staging"
        assert cfg.environment == "staging"

    def test_constructor_profile_overrides_env(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.setenv("SMPLKIT_PROFILE", "staging")
        config = tmp_path / ".smplkit"
        config.write_text(
            "[common]\n"
            "service = my-app\n"
            "\n"
            "[staging]\n"
            "api_key = sk_api_staging\n"
            "environment = staging\n"
            "\n"
            "[local]\n"
            "api_key = sk_api_local\n"
            "environment = development\n"
        )
        cfg = resolve_config(profile="local", _home_dir=tmp_path)
        assert cfg.api_key == "sk_api_local"
        assert cfg.environment == "development"

    def test_missing_profile_raises_error(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_default\n\n[staging]\napi_key = sk_api_staging\n")
        with pytest.raises(Error, match="Profile \\[nonexistent\\] not found"):
            resolve_config(
                profile="nonexistent",
                environment="test",
                service="svc",
                _home_dir=tmp_path,
            )

    def test_malformed_file_silently_skipped(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        # Write binary garbage that configparser cannot parse
        config.write_bytes(b"\x80\x81\x82\x00\xff")
        cfg = resolve_config(
            api_key="sk_api_explicit",
            environment="test",
            service="svc",
            _home_dir=tmp_path,
        )
        assert cfg.api_key == "sk_api_explicit"

    def test_default_profile_missing_with_other_profiles(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        # File has [local] and [staging] but no [default] section
        config.write_text(
            "[local]\n"
            "api_key = sk_api_local\n"
            "environment = development\n"
            "service = svc\n"
            "\n"
            "[staging]\n"
            "api_key = sk_api_staging\n"
            "environment = staging\n"
            "service = svc\n"
        )
        # Should proceed silently — not raise an error
        cfg = resolve_config(
            api_key="sk_api_explicit",
            environment="test",
            service="svc",
            _home_dir=tmp_path,
        )
        assert cfg.api_key == "sk_api_explicit"

    def test_missing_file_silently_skipped(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        # No .smplkit file in tmp_path
        cfg = resolve_config(
            api_key="sk_api_explicit",
            environment="test",
            service="svc",
            _home_dir=tmp_path,
        )
        assert cfg.api_key == "sk_api_explicit"

    def test_empty_value_in_file_treated_as_unset(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = \nenvironment = production\nservice = svc\n")
        # api_key is empty in file, should still be unset
        with pytest.raises(Error, match="No API key provided"):
            resolve_config(_home_dir=tmp_path)

    def test_semicolon_comments(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text(
            "; this is a comment\n"
            "[default]\n"
            "; another comment\n"
            "api_key = sk_api_semicolon\n"
            "environment = test\n"
            "service = svc\n"
        )
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_api_semicolon"

    def test_hash_comments(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text(
            "# this is a comment\n"
            "[default]\n"
            "# another comment\n"
            "api_key = sk_api_hash\n"
            "environment = test\n"
            "service = svc\n"
        )
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_api_hash"

    def test_boolean_from_file(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_DEBUG", raising=False)
        monkeypatch.delenv("SMPLKIT_TELEMETRY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text(
            "[default]\napi_key = sk_api_test\nenvironment = test\nservice = svc\ndebug = true\ntelemetry = no\n"
        )
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.debug is True
        assert cfg.telemetry is False


class TestResolveConfigEnvVars:
    """Step 3: Environment variables."""

    def test_env_vars_override_file(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_file\nenvironment = production\nservice = file-svc\n")
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_api_env")
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "staging")
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_api_env"
        assert cfg.environment == "staging"
        assert cfg.service == "file-svc"  # not overridden by env

    def test_empty_env_var_treated_as_unset(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setenv("SMPLKIT_API_KEY", "")
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_file\nenvironment = test\nservice = svc\n")
        cfg = resolve_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_api_file"

    def test_boolean_from_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("SMPLKIT_DEBUG", "1")
        monkeypatch.setenv("SMPLKIT_TELEMETRY", "no")
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        cfg = resolve_config(
            api_key="sk_api_test",
            environment="test",
            service="svc",
            _home_dir=tmp_path,
        )
        assert cfg.debug is True
        assert cfg.telemetry is False

    def test_base_domain_and_scheme_from_env(self, monkeypatch, tmp_path):
        monkeypatch.setenv("SMPLKIT_BASE_DOMAIN", "localhost")
        monkeypatch.setenv("SMPLKIT_SCHEME", "http")
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        cfg = resolve_config(
            api_key="sk_api_test",
            environment="test",
            service="svc",
            _home_dir=tmp_path,
        )
        assert cfg.base_domain == "localhost"
        assert cfg.scheme == "http"


class TestResolveConfigConstructorArgs:
    """Step 4: Constructor arguments override everything."""

    def test_constructor_overrides_all(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_api_env")
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "env-env")
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_file\nenvironment = file-env\nservice = file-svc\n")
        cfg = resolve_config(
            api_key="sk_api_explicit",
            environment="explicit-env",
            service="explicit-svc",
            base_domain="custom.example.com",
            scheme="http",
            debug=True,
            telemetry=False,
            _home_dir=tmp_path,
        )
        assert cfg.api_key == "sk_api_explicit"
        assert cfg.environment == "explicit-env"
        assert cfg.service == "explicit-svc"
        assert cfg.base_domain == "custom.example.com"
        assert cfg.scheme == "http"
        assert cfg.debug is True
        assert cfg.telemetry is False

    def test_explicit_false_overrides_file_true(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_DEBUG", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_test\nenvironment = test\nservice = svc\ndebug = true\n")
        cfg = resolve_config(debug=False, _home_dir=tmp_path)
        assert cfg.debug is False


class TestResolveConfigPrecedence:
    """Full precedence chain: constructor > env > file > defaults."""

    def test_full_precedence(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text(
            "[common]\n"
            "environment = common-env\n"
            "service = common-svc\n"
            "\n"
            "[default]\n"
            "api_key = sk_api_file\n"
            "environment = file-env\n"
        )
        monkeypatch.setenv("SMPLKIT_ENVIRONMENT", "env-env")
        cfg = resolve_config(
            environment="constructor-env",
            _home_dir=tmp_path,
        )
        # constructor > env > file > common
        assert cfg.environment == "constructor-env"
        assert cfg.service == "common-svc"  # from [common], not overridden
        assert cfg.api_key == "sk_api_file"


class TestResolveConfigErrors:
    """Error cases."""

    def test_missing_api_key(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No API key provided"):
            resolve_config(
                environment="test",
                service="svc",
                _home_dir=tmp_path,
            )

    def test_missing_environment(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No environment provided"):
            resolve_config(
                api_key="sk_api_test",
                service="svc",
                _home_dir=tmp_path,
            )

    def test_missing_service(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No service provided"):
            resolve_config(
                api_key="sk_api_test",
                environment="test",
                _home_dir=tmp_path,
            )

    def test_error_message_mentions_profile(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[local]\nenvironment = dev\nservice = svc\n")
        with pytest.raises(Error, match=r"\[local\]"):
            resolve_config(
                profile="local",
                _home_dir=tmp_path,
            )

    def test_invalid_boolean_raises_error(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        config = tmp_path / ".smplkit"
        config.write_text("[default]\napi_key = sk_api_test\nenvironment = test\nservice = svc\ndebug = maybe\n")
        with pytest.raises(Error, match="Invalid boolean value"):
            resolve_config(_home_dir=tmp_path)

    def test_invalid_boolean_env_raises_error(self, monkeypatch, tmp_path):
        monkeypatch.setenv("SMPLKIT_DEBUG", "maybe")
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="Invalid boolean value"):
            resolve_config(
                api_key="sk_api_test",
                environment="test",
                service="svc",
                _home_dir=tmp_path,
            )


class TestParseBool:
    """Boolean parsing helper."""

    @pytest.mark.parametrize("value", ["true", "True", "TRUE", "1", "yes", "Yes", "YES"])
    def test_truthy(self, value):
        assert _parse_bool(value, "test") is True

    @pytest.mark.parametrize("value", ["false", "False", "FALSE", "0", "no", "No", "NO"])
    def test_falsy(self, value):
        assert _parse_bool(value, "test") is False

    def test_invalid(self):
        with pytest.raises(Error, match="Invalid boolean"):
            _parse_bool("maybe", "test")

    def test_whitespace_stripped(self):
        assert _parse_bool("  true  ", "test") is True
