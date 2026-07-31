import math
import time

import jwt
import pytest
from pydantic import SecretStr

from mistralai.workflows.core.auth import (
    FileTokenProvider,
    StaticTokenProvider,
    get_token_provider,
)
from mistralai.workflows.core.config.config import config
from mistralai.workflows.exceptions import WorkflowError

# HS256 requires a key >= 32 bytes; the signature is never verified in these
# tests, but a short key triggers jwt's InsecureKeyLengthWarning.
_SIGNING_KEY = "test-signing-key-not-verified-but-long-enough"


def _make_jwt(exp: float) -> str:
    return jwt.encode({"exp": exp}, key=_SIGNING_KEY, algorithm="HS256")


@pytest.fixture
def restore_common_auth_config():
    original_key = config.common.mistral_api_key
    original_path = config.common.mistral_sa_token_path
    yield
    config.common.mistral_api_key = original_key
    config.common.mistral_sa_token_path = original_path


class TestStaticTokenProvider:
    def test_get_token_returns_wrapped_value(self):
        provider = StaticTokenProvider("secret-key")
        assert provider.get_token() == "secret-key"

    def test_get_token_with_max_age_never_expires(self):
        provider = StaticTokenProvider("secret-key")
        token, max_age = provider.get_token_with_max_age()
        assert token == "secret-key"
        assert math.isinf(max_age)


class TestFileTokenProvider:
    def test_reads_and_strips_token(self, tmp_path):
        token_file = tmp_path / "token"
        token = _make_jwt(time.time() + 3600)
        token_file.write_text(f"  {token}\n")
        provider = FileTokenProvider(token_file)
        assert provider.get_token() == token

    def test_missing_file_raises_workflow_error(self, tmp_path):
        provider = FileTokenProvider(tmp_path / "does-not-exist")
        with pytest.raises(WorkflowError):
            provider.get_token()

    def test_empty_file_raises_workflow_error(self, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text("   \n")
        provider = FileTokenProvider(token_file)
        with pytest.raises(WorkflowError):
            provider.get_token()

    def test_non_jwt_token_raises_workflow_error(self, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text("not-a-jwt")
        provider = FileTokenProvider(token_file)
        with pytest.raises(WorkflowError):
            provider.get_token()

    def test_jwt_without_exp_raises_workflow_error(self, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text(jwt.encode({"sub": "worker"}, key=_SIGNING_KEY, algorithm="HS256"))
        provider = FileTokenProvider(token_file)
        with pytest.raises(WorkflowError):
            provider.get_token()

    def test_jwt_is_cached_until_near_expiry(self, tmp_path):
        token_file = tmp_path / "token"
        jwt = _make_jwt(time.time() + 3600)
        token_file.write_text(jwt)
        provider = FileTokenProvider(token_file)
        assert provider.get_token() == jwt
        token_file.write_text(_make_jwt(time.time() + 7200))
        # Still within validity window: cached value is returned, file not re-read.
        assert provider.get_token() == jwt

    def test_jwt_re_read_when_within_refresh_margin(self, tmp_path):
        token_file = tmp_path / "token"
        near_expiry = _make_jwt(time.time() + 10)
        token_file.write_text(near_expiry)
        provider = FileTokenProvider(token_file, refresh_margin_seconds=30.0)
        assert provider.get_token() == near_expiry
        rotated = _make_jwt(time.time() + 3600)
        token_file.write_text(rotated)
        assert provider.get_token() == rotated

    def test_max_age_for_jwt_reflects_time_to_expiry(self, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text(_make_jwt(time.time() + 3600))
        provider = FileTokenProvider(token_file, refresh_margin_seconds=30.0)
        _, max_age = provider.get_token_with_max_age()
        assert 3600 - 30 - 5 < max_age <= 3600 - 30


class TestFactory:
    def test_get_token_provider_prefers_sa_token_path(self, restore_common_auth_config, tmp_path):
        token_file = tmp_path / "token"
        sa_token = _make_jwt(time.time() + 3600)
        token_file.write_text(sa_token)
        config.common.mistral_sa_token_path = str(token_file)
        config.common.mistral_api_key = SecretStr("api-key")

        provider = get_token_provider()

        assert isinstance(provider, FileTokenProvider)
        assert provider.get_token() == sa_token

    def test_get_token_provider_falls_back_to_api_key(self, restore_common_auth_config):
        config.common.mistral_sa_token_path = None
        config.common.mistral_api_key = SecretStr("api-key")

        provider = get_token_provider()

        assert isinstance(provider, StaticTokenProvider)
        assert provider.get_token() == "api-key"

    def test_get_token_provider_returns_none_when_unconfigured(self, restore_common_auth_config):
        config.common.mistral_sa_token_path = None
        config.common.mistral_api_key = None

        assert get_token_provider() is None

    def test_explicit_str_key_wins(self, restore_common_auth_config, tmp_path):
        token_file = tmp_path / "token"
        token_file.write_text("sa-token")
        config.common.mistral_sa_token_path = str(token_file)
        config.common.mistral_api_key = SecretStr("config-key")

        provider = get_token_provider("explicit-key")

        assert isinstance(provider, StaticTokenProvider)
        assert provider.get_token() == "explicit-key"

    def test_explicit_secretstr_key_wins(self, restore_common_auth_config):
        config.common.mistral_api_key = SecretStr("config-key")

        provider = get_token_provider(SecretStr("explicit-key"))

        assert isinstance(provider, StaticTokenProvider)
        assert provider.get_token() == "explicit-key"
