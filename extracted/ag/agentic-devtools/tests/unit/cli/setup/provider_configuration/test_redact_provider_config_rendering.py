"""Unit tests for redact_provider_config_rendering."""

import yaml

from agentic_devtools.cli.setup.provider_configuration import redact_provider_config_rendering


def test_redact_provider_config_rendering_redacts_secret_like_fields() -> None:
    rendered = yaml.safe_dump(
        {"providers": {"custom": {"api_key": "secret", "auth": "******", "cookie": "session=value", "model": "m"}}}
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "******" not in redacted
    assert "session=value" not in redacted
    assert "<redacted>" in redacted


def test_redact_provider_config_rendering_redacts_separated_key_fields() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "access_key": "secret",
                    "account_key": "secret",
                    "model": "m",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "access_key: <redacted>" in redacted
    assert "account_key: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_compact_uppercase_secret_fields() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"REFRESHTOKEN": "secret", "model": "m"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "REFRESHTOKEN: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_compact_key_secret_fields() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "ACCESSKEY": "secret",
                    "SUBSCRIPTIONKEY": "secret",
                    "GITHUBKEY": "secret",
                    "model": "m",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "ACCESSKEY: <redacted>" in redacted
    assert "GITHUBKEY: <redacted>" in redacted
    assert "SUBSCRIPTIONKEY: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_compact_lowercase_key_secret_fields() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"githubkey": "secret", "webhookkey": "secret", "model": "m"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "githubkey: <redacted>" in redacted
    assert "webhookkey: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_list_entries() -> None:
    rendered = yaml.safe_dump({"items": [{"token": "secret"}]})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted


def test_redact_provider_config_rendering_redacts_header_container_values() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"headers": {"X-Auth": "******", "X-Trace": "trace"}}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "******" not in redacted
    assert "trace" not in redacted
    assert "X-Auth: <redacted>" in redacted
    assert "X-Trace: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_compact_header_container_values() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"REQUESTHEADERS": {"X-Auth": "******", "X-Trace": "trace"}}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "******" not in redacted
    assert "trace" not in redacted
    assert "X-Auth: <redacted>" in redacted
    assert "X-Trace: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_nested_cookie_mapping() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"cookies": {"session_id": "actual-secret"}}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "cookies: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_env_reference_fields() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"max_tokens": 256, "api_key_env": "OPENAI_KEY"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "max_tokens: 256" in redacted
    assert "OPENAI_KEY" not in redacted
    assert "api_key_env: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_unknown_env_suffixed_secret_fields() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"password_env": "actual-secret"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "password_env: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_plural_credential_keys() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "credentials": "actual-secret",
                    "api_keys": "actual-secret",
                    "APIKEYSENV": "OPENAI_KEYS",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "OPENAI_KEYS" not in redacted
    assert "credentials: <redacted>" in redacted
    assert "api_keys: <redacted>" in redacted
    assert "APIKEYSENV: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_password_alias_fields() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "passphrase": "actual-secret",
                    "PassPhrase": "actual-secret",
                    "passwd": "actual-secret",
                    "pwd": "actual-secret",
                    "DBPWD": "actual-secret",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "passphrase: <redacted>" in redacted
    assert "PassPhrase: <redacted>" in redacted
    assert "passwd: <redacted>" in redacted
    assert "pwd: <redacted>" in redacted
    assert "DBPWD: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_connection_string_fields() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "connection_string": "DefaultEndpointsProtocol=https;AccountName=x;AccountKey=secret",
                    "ConnectionString": "Server=tcp:db.example;******",
                    "connectionstring": "Host=db.example;Username=alice;******",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "AccountKey=secret" not in redacted
    assert "******" not in redacted
    assert "connection_string: <redacted>" in redacted
    assert "ConnectionString: <redacted>" in redacted
    assert "connectionstring: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_compact_env_reference_fields() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "APIKEYENV": "actual-secret",
                    "TOKENENV": "OPENAI_TOKEN",
                    "COOKIEENV": "SESSION_ENV",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "OPENAI_TOKEN" not in redacted
    assert "SESSION_ENV" not in redacted
    assert "APIKEYENV: <redacted>" in redacted
    assert "TOKENENV: <redacted>" in redacted
    assert "COOKIEENV: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_compact_key_env_reference_fields() -> None:
    rendered = yaml.safe_dump(
        {"providers": {"custom": {"PATENV": "actual-secret", "ACCESSKEYENV": "CLOUD_KEY", "GITHUBKEYENV": "GH_KEY"}}}
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "CLOUD_KEY" not in redacted
    assert "GH_KEY" not in redacted
    assert "PATENV: <redacted>" in redacted
    assert "ACCESSKEYENV: <redacted>" in redacted
    assert "GITHUBKEYENV: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_non_identifier_env_reference_value() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"api_key_env": "actual-secret"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "api_key_env: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_identifier_shaped_env_reference_value() -> None:
    rendered = yaml.safe_dump({"providers": {"custom": {"api_key_env": "sk_live_SECRET123"}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "sk_live_SECRET123" not in redacted
    assert "api_key_env: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_url_userinfo() -> None:
    endpoint = "https://alice:" + "secret" + "@example.invalid/v1"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "https://******@example.invalid/v1" in redacted


def test_redact_provider_config_rendering_redacts_scheme_relative_url_userinfo() -> None:
    endpoint = "//alice:" + "secret" + "@example.invalid/v1"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "//******@example.invalid/v1" in redacted


def test_redact_provider_config_rendering_redacts_malformed_userinfo_without_slashes() -> None:
    endpoint = "alice:" + "secret" + "@example.invalid/v1"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert endpoint not in redacted
    assert "secret" not in redacted
    assert "endpoint: <redacted>" in redacted


def test_redact_provider_config_rendering_redacts_invalid_scheme_less_userinfo_parse() -> None:
    endpoint = "alice@[bad"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert endpoint not in redacted
    assert "endpoint: <redacted>" in redacted


def test_redact_provider_config_rendering_preserves_at_sign_without_malformed_userinfo() -> None:
    endpoint = "/notes/alice@example.invalid/v1"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert "endpoint: /notes/alice@example.invalid/v1" in redacted


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


def test_redact_provider_config_rendering_redacts_acronym_cased_url_query_credentials() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?APIKey=secret&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "APIKey=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_compact_uppercase_url_query_credentials() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?APIKEY=secret&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "APIKEY=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_compact_suffix_query_credentials() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?GITHUBTOKEN=secret&WEBHOOKSECRET=secret&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "GITHUBTOKEN=%3Credacted%3E" in redacted
    assert "WEBHOOKSECRET=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_plural_query_credentials() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?credentials=secret&api_keys=secret&APIKEYSENV=OPENAI_KEYS&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "OPENAI_KEYS" not in redacted
    assert "credentials=%3Credacted%3E" in redacted
    assert "api_keys=%3Credacted%3E" in redacted
    assert "APIKEYSENV=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_compact_env_suffix_query_values() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": (
                        "https://example.invalid/v1?APIKEYENV=actual-secret&PASSWORDENVVAR=OPENAI_PASSWORD"
                        "&COOKIEENV=SESSION_ENV&region=west"
                    ),
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "OPENAI_PASSWORD" not in redacted
    assert "SESSION_ENV" not in redacted
    assert "APIKEYENV=%3Credacted%3E" in redacted
    assert "PASSWORDENVVAR=%3Credacted%3E" in redacted
    assert "COOKIEENV=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_non_identifier_env_reference_query_value() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?api_key_env=actual-secret&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "actual-secret" not in redacted
    assert "api_key_env=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_scheme_less_secret_query_values() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "example.invalid/v1?api_key=secret&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "secret" not in redacted
    assert "api_key=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_redacts_identifier_env_reference_query_value() -> None:
    rendered = yaml.safe_dump(
        {
            "providers": {
                "custom": {
                    "endpoint": "https://example.invalid/v1?api_key_env=OPENAI_API_KEY&region=west",
                }
            }
        }
    )

    redacted = redact_provider_config_rendering(rendered)

    assert "OPENAI_API_KEY" not in redacted
    assert "api_key_env=%3Credacted%3E" in redacted
    assert "region=west" in redacted


def test_redact_provider_config_rendering_preserves_safe_url_query() -> None:
    endpoint = "https://example.invalid/v1?region=west"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert endpoint in redacted


def test_redact_provider_config_rendering_redacts_malformed_url() -> None:
    endpoint = "https://[?api_key=secret"
    rendered = yaml.safe_dump({"providers": {"custom": {"endpoint": endpoint}}})

    redacted = redact_provider_config_rendering(rendered)

    assert endpoint not in redacted
    assert "secret" not in redacted
    assert "endpoint: <redacted>" in redacted
