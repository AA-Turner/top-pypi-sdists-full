"""Unit tests for _validate_provider_mapping."""

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


@pytest.mark.parametrize(
    ("provider", "reason"),
    [
        (None, "provider_missing"),
        ({"type": "unsupported", "model": "m"}, "provider_type_invalid"),
        ({"type": "copilot"}, "model_missing"),
        ({"type": "copilot", "model": "m", "api_key_env": "SECRET"}, "copilot_api_key_env_forbidden"),
        ({"type": "openai_direct", "model": "m"}, "credential_reference_missing"),
        ({"type": "local_model", "model": "m", "endpoint": " "}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "bad"}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "http://example.invalid:bad"}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "http://:8080"}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "http://alice@example.invalid:8080"}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "https://@example.invalid:8080"}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "https://exa mple.invalid:8443"}, "endpoint_invalid"),
        ({"type": "local_model", "model": "m", "endpoint": "https://example.invalid "}, "endpoint_invalid"),
    ],
)
def test__validate_provider_mapping_reports_expected_error(provider: dict | None, reason: str) -> None:
    assert provider_configuration._validate_provider_mapping(provider) == reason


def test__validate_provider_mapping_accepts_ready_provider(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")

    assert (
        provider_configuration._validate_provider_mapping(
            {"type": "openai_direct", "model": "m", "api_key_env": "OPENAI_KEY"}
        )
        is None
    )


def test__validate_provider_mapping_allows_local_model_without_explicit_endpoint() -> None:
    assert provider_configuration._validate_provider_mapping({"type": "local_model", "model": "m"}) is None


def test__validate_provider_mapping_accepts_valid_explicit_local_model_endpoint() -> None:
    assert (
        provider_configuration._validate_provider_mapping(
            {"type": "local_model", "model": "m", "endpoint": "http://example.invalid:8080"}
        )
        is None
    )


def test__validate_provider_mapping_rejects_local_model_endpoint_with_password() -> None:
    endpoint = "https://alice:" + "pwd" + "@example.invalid:8080"
    assert (
        provider_configuration._validate_provider_mapping({"type": "local_model", "model": "m", "endpoint": endpoint})
        == "endpoint_invalid"
    )


def test__validate_provider_mapping_requires_endpoint_for_azure_openai(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")
    assert (
        provider_configuration._validate_provider_mapping(
            {"type": "azure_openai", "model": "m", "api_key_env": "OPENAI_KEY"}
        )
        == "endpoint_missing"
    )


def test__validate_provider_mapping_rejects_malformed_azure_openai_endpoint(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")
    assert (
        provider_configuration._validate_provider_mapping(
            {"type": "azure_openai", "model": "m", "api_key_env": "OPENAI_KEY", "endpoint": "http://:8080"}
        )
        == "endpoint_invalid"
    )


def test__validate_provider_mapping_rejects_azure_openai_endpoint_with_embedded_credentials(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")
    assert (
        provider_configuration._validate_provider_mapping(
            {
                "type": "azure_openai",
                "model": "m",
                "api_key_env": "OPENAI_KEY",
                "endpoint": "https://alice@example.invalid:8443",
            }
        )
        == "endpoint_invalid"
    )


def test__validate_provider_mapping_rejects_azure_openai_endpoint_with_whitespace_in_authority(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")
    assert (
        provider_configuration._validate_provider_mapping(
            {
                "type": "azure_openai",
                "model": "m",
                "api_key_env": "OPENAI_KEY",
                "endpoint": "https://exa mple.invalid:8443",
            }
        )
        == "endpoint_invalid"
    )


def test__validate_provider_mapping_rejects_hostname_with_whitespace_after_parsing(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")

    class _ParsedEndpoint:
        scheme = "https"
        netloc = "example.invalid:8443"
        hostname = "example .invalid"
        port = 8443

    monkeypatch.setattr(provider_configuration, "urlparse", lambda _value: _ParsedEndpoint())

    assert (
        provider_configuration._validate_provider_mapping(
            {
                "type": "azure_openai",
                "model": "m",
                "api_key_env": "OPENAI_KEY",
                "endpoint": "https://example.invalid:8443",
            }
        )
        == "endpoint_invalid"
    )


def test__validate_provider_mapping_accepts_valid_azure_openai_endpoint(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_KEY", "present")
    assert (
        provider_configuration._validate_provider_mapping(
            {
                "type": "azure_openai",
                "model": "m",
                "api_key_env": "OPENAI_KEY",
                "endpoint": "https://example.invalid:8443",
            }
        )
        is None
    )
