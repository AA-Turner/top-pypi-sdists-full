"""Unit tests for _is_secret_key."""

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("api_key", True),
        ("accessToken", True),
        ("GITHUBTOKEN", True),
        ("AUTHTOKEN", True),
        ("WEBHOOKSECRET", True),
        ("APIKEY", True),
        ("client-secret", True),
        ("credential", True),
        ("credentials", True),
        ("Authorization", True),
        ("auth", True),
        ("cookie", True),
        ("cookies", True),
        ("passphrase", True),
        ("PassPhrase", True),
        ("passwd", True),
        ("pwd", True),
        ("DBPWD", True),
        ("private_key", True),
        ("api_keys", True),
        ("access_key", True),
        ("account_key", True),
        ("ACCESSKEY", True),
        ("SUBSCRIPTIONKEY", True),
        ("SECRETKEY", True),
        ("GITHUBKEY", True),
        ("WEBHOOKKEY", True),
        ("connection_string", True),
        ("ConnectionString", True),
        ("connectionstring", True),
        ("githubkey", True),
        ("webhookkey", True),
        ("PATENV", True),
        ("ACCESSKEYENV", True),
        ("GITHUBKEYENV", True),
        ("APIKEYSENV", True),
        ("CREDENTIALSENV", True),
        ("key", True),
        ("pat", True),
        ("sig", True),
        ("signature", True),
        ("api_key_env", False),
        ("token_environment_variable", False),
        ("max_tokens", False),
        ("model", False),
    ],
)
def test__is_secret_key_classifies_secret_like_keys(key: str, expected: bool) -> None:
    assert provider_configuration._is_secret_key(key) is expected
