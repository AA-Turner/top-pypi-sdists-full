"""Config env/header redaction tests."""

from __future__ import annotations

import pytest

from runlayer_cli.scan.config_redact import (
    BENIGN_ENV_KEYS,
    redact_config_mapping,
)


@pytest.mark.parametrize(
    "value",
    [
        "${env:GITHUB_TOKEN}",
        "{env:GITHUB_TOKEN}",
        "${GITHUB_TOKEN}",
        "Bearer ${GITHUB_TOKEN}",
        "Basic ${USERNAME}:${PASSWORD}",
    ],
)
def test_placeholder_values_are_preserved(value: str) -> None:
    assert redact_config_mapping({"AUTH": value}) == {"AUTH": value}


def test_literal_value_is_replaced_with_length_marker() -> None:
    value = "ghp_example_literal_secret"

    assert redact_config_mapping({"GITHUB_TOKEN": value}) == {
        "GITHUB_TOKEN": f"<redacted:len={len(value)}>"
    }


def test_literal_prefix_next_to_placeholder_is_not_treated_as_scaffolding() -> None:
    value = "literal-secret-${TOKEN}"

    assert redact_config_mapping({"TOKEN": value}) == {
        "TOKEN": f"<redacted:len={len(value)}>"
    }


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("PORT", "8080"),
        ("HOST", "127.0.0.1"),
        ("NODE_ENV", "production"),
        ("LOG_LEVEL", "debug"),
        ("DEBUG", "true"),
        ("TZ", "UTC"),
    ],
)
def test_known_benign_env_literals_are_preserved(key: str, value: str) -> None:
    assert redact_config_mapping(
        {key: value},
        allowed_literal_keys=BENIGN_ENV_KEYS,
    ) == {key: value}


def test_env_allowlist_is_not_implicitly_applied_to_headers() -> None:
    value = "internal.example.com"

    assert redact_config_mapping({"Host": value}) == {
        "Host": f"<redacted:len={len(value)}>"
    }


def test_non_mapping_values_pass_through() -> None:
    assert redact_config_mapping(None) is None
