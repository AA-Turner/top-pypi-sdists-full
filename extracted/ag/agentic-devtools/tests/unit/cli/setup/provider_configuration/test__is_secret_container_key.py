"""Unit tests for _is_secret_container_key."""

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("headers", True),
        ("requestHeaders", True),
        ("REQUESTHEADERS", True),
        ("response-header-values", True),
        ("authorization", False),
        ("api_key", False),
        ("model", False),
    ],
)
def test__is_secret_container_key_classifies_header_container_keys(key: str, expected: bool) -> None:
    assert provider_configuration._is_secret_container_key(key) is expected
