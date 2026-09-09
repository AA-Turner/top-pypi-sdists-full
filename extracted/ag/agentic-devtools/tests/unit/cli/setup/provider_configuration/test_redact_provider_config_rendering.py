"""Unit tests for redact_provider_config_rendering."""

import yaml

from agentic_devtools.cli.setup.provider_configuration import redact_provider_config_rendering


def test_redact_provider_config_rendering_redacts_secret_like_fields() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"api_key": "secret", "model": "m"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "<redacted>" in redacted


def test_redact_provider_config_rendering_redacts_list_entries() -> None:
    rendered = yaml.safe_dump({"items": [{"token": "secret"}]})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted


def test_redact_provider_config_rendering_keeps_non_secret_and_env_reference_fields() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"max_tokens": 256, "api_key_env": "OPENAI_KEY"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "max_tokens: 256" in redacted
    assert "api_key_env: OPENAI_KEY" in redacted


def test_redact_provider_config_rendering_redacts_url_userinfo() -> None:
    endpoint = "https://alice:" + "secret" + "@example.invalid/v1"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "https://******@example.invalid/v1" in redacted


def test_redact_provider_config_rendering_redacts_url_credentials() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?api_key=secret&region=west#secret",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "api_key=%3Credacted%3E" in redacted
    assert "region=west" in redacted
    assert "#<redacted>" in redacted


def test_redact_provider_config_rendering_redacts_signed_url_query_credentials() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": (
                        "https://example.invalid/v1?sig=secret&signature=secret&pat=secret&key=secret&region=west"
                    ),
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "sig=%3Credacted%3E" in redacted
    assert "signature=%3Credacted%3E" in redacted
    assert "pat=%3Credacted%3E" in redacted
    assert "key=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_preserves_safe_url_query() -> None:
    endpoint = "https://example.invalid/v1?region=west"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert endpoint in redacted


def test_redact_provider_config_rendering_redacts_malformed_url() -> None:
    endpoint = "http://alice:" + "secret" + "@["
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert endpoint not in redacted
    assert "<redacted>" in redacted
