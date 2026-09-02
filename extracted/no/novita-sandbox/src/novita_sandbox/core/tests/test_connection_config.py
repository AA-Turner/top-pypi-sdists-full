import pytest

from novita_sandbox.core.connection_config import (
    ConnectionConfig,
    DEFAULT_NOVITA_DOMAIN,
    LEGACY_REQUEST_TIMEOUT,
    is_legacy_domain,
)
from novita_sandbox.core.volume.volume_sync import Volume

LEGACY_DOMAINS = [
    "sandbox.novita.ai",
    "us-01.sandbox.novita.ai",
    "us-ga-01.sandbox.novita.ai",
    "us-ga-1.sandbox.novita.ai",
    "sandbox-dev.novita.ai",
    "us-01.sandbox-dev.novita.ai",
    "us-ga-01.sandbox-dev.novita.ai",
    "us-ca-1.sandbox-dev.novita.ai",
]


def test_connection_config_defaults_to_supported_alpha_domain(monkeypatch):
    monkeypatch.delenv("NOVITA_DOMAIN", raising=False)

    config = ConnectionConfig()

    assert config.domain == DEFAULT_NOVITA_DOMAIN
    assert config.api_url == f"https://api.{DEFAULT_NOVITA_DOMAIN}"


def test_is_legacy_domain_requires_non_empty_domain():
    with pytest.raises(ValueError, match="domain cannot be empty"):
        is_legacy_domain("")


def test_is_legacy_domain_detects_legacy_domains():
    for domain in LEGACY_DOMAINS:
        assert is_legacy_domain(domain) is True
    assert is_legacy_domain(DEFAULT_NOVITA_DOMAIN) is False


@pytest.mark.parametrize("domain", LEGACY_DOMAINS)
def test_connection_config_accepts_legacy_option_domain(domain):
    config = ConnectionConfig(domain=domain)

    assert config.domain == domain
    assert config.is_legacy_domain is True


@pytest.mark.parametrize("domain", LEGACY_DOMAINS)
def test_connection_config_uses_legacy_request_timeout_for_legacy_domain(domain):
    config = ConnectionConfig(domain=domain)

    assert config.request_timeout == LEGACY_REQUEST_TIMEOUT


def test_connection_config_explicit_request_timeout_overrides_legacy_default():
    config = ConnectionConfig(domain="sandbox.novita.ai", request_timeout=120)

    assert config.request_timeout == 120


def test_connection_config_rejects_unsupported_env_domain(monkeypatch):
    monkeypatch.setenv("NOVITA_DOMAIN", "us-ga-1.sandbox.novita.ai")

    config = ConnectionConfig()

    assert config.domain == "us-ga-1.sandbox.novita.ai"
    assert config.is_legacy_domain is True


def test_connection_config_rejects_unsupported_api_params_domain():
    config = ConnectionConfig()

    params = config.get_api_params(domain="sandbox.novita.ai")

    assert params["domain"] == "sandbox.novita.ai"


def test_volume_accepts_legacy_constructor_domain():
    volume = Volume("volume-id", "volume-name", "token", domain="sandbox.novita.ai")

    assert volume.volume_id == "volume-id"
