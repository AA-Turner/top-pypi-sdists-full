"""Unit tests for _normalize_secret_key."""

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("apiKey", "api_key"),
        ("APIKey", "api_key"),
        ("APIKEY", "api_key"),
        ("APIKEYENV", "api_key_env"),
        ("GITHUBKEYENV", "github_key_env"),
        ("APIKEYSENV", "api_keys_env"),
        ("API_KEYENVVAR", "api_key_env_var"),
        ("CONNECTIONSTRINGENV", "connectionstring_env"),
        ("CREDENTIALSENV", "credentials_env"),
        ("COOKIEENV", "cookie_env"),
        ("TOKENENV", "token_env"),
        ("WEBHOOKSECRETENV", "webhook_secret_env"),
        ("PASSWORDENVVAR", "password_env_var"),
        ("PassPhrase", "password"),
        ("PASSWDENV", "password_env"),
        ("PWDENV", "password_env"),
        ("ENV", "env"),
        ("FOOENV", "fooenv"),
        ("REFRESHTOKEN", "refresh_token"),
        ("token-environment-variable", "token_environment_variable"),
        ("Authorization", "authorization"),
        (123, "123"),
    ],
)
def test__normalize_secret_key_normalizes_mixed_key_shapes(key: object, expected: str) -> None:
    assert provider_configuration._normalize_secret_key(key) == expected
