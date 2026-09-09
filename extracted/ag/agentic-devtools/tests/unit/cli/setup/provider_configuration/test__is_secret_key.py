"""Unit tests for _is_secret_key."""

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("api_key", True),
        ("accessToken", True),
        ("client-secret", True),
        ("credential", True),
        ("Authorization", True),
        ("private_key", True),
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
