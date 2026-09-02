"""Tests for settings-override argv extraction."""

from __future__ import annotations

import pytest

from runlayer_cli.scan.clients import SettingsOverrideFlag
from runlayer_cli.scan.processes.settings_override import extract_settings_overrides


@pytest.mark.parametrize(
    ("argv", "expected_value"),
    [
        (["claude", "--mcp-config", "/tmp/mcp.json"], "/tmp/mcp.json"),
        (["claude", "--mcp-config=/tmp/mcp.json"], "/tmp/mcp.json"),
    ],
)
def test_extracts_separate_and_equals_values(
    argv: list[str],
    expected_value: str,
) -> None:
    [match] = extract_settings_overrides(
        argv,
        [SettingsOverrideFlag("--mcp-config", mcp_config="file")],
    )

    assert match.flag == "--mcp-config"
    assert match.value == expected_value
    assert match.mcp_config == "file"
    assert match.inline_json is False


def test_preserves_repeated_flags() -> None:
    matches = extract_settings_overrides(
        [
            "claude",
            "--mcp-config",
            "/tmp/first.json",
            "--mcp-config=/tmp/second.json",
        ],
        [SettingsOverrideFlag("--mcp-config", mcp_config="file")],
    )

    assert [match.value for match in matches] == [
        "/tmp/first.json",
        "/tmp/second.json",
    ]


def test_variadic_flag_consumes_values_until_next_flag() -> None:
    matches = extract_settings_overrides(
        [
            "claude",
            "--mcp-config",
            "/tmp/first.json",
            "/tmp/second.json",
            "--settings",
            "/tmp/settings.json",
        ],
        [
            SettingsOverrideFlag(
                "--mcp-config",
                mcp_config="file",
                variadic=True,
            ),
            SettingsOverrideFlag("--settings"),
        ],
    )

    assert [(match.flag, match.value) for match in matches] == [
        ("--mcp-config", "/tmp/first.json"),
        ("--mcp-config", "/tmp/second.json"),
        ("--settings", "/tmp/settings.json"),
    ]


def test_non_variadic_flag_consumes_only_one_value() -> None:
    matches = extract_settings_overrides(
        ["claude", "--settings", "/tmp/first.json", "/tmp/second.json"],
        [SettingsOverrideFlag("--settings")],
    )

    assert [(match.flag, match.value) for match in matches] == [
        ("--settings", "/tmp/first.json"),
    ]


def test_marks_inline_json_without_parsing_it() -> None:
    [match] = extract_settings_overrides(
        ["claude", "--mcp-config", '  {"mcpServers": {}}'],
        [SettingsOverrideFlag("--mcp-config", mcp_config="file")],
    )

    assert match.value == '  {"mcpServers": {}}'
    assert match.inline_json is True


def test_boolean_flag_does_not_consume_next_argument() -> None:
    matches = extract_settings_overrides(
        [
            "claude",
            "--strict-mcp-config",
            "--mcp-config",
            "/tmp/mcp.json",
        ],
        [
            SettingsOverrideFlag("--strict-mcp-config", takes_value=False),
            SettingsOverrideFlag("--mcp-config", mcp_config="file"),
        ],
    )

    assert [(match.flag, match.value) for match in matches] == [
        ("--strict-mcp-config", None),
        ("--mcp-config", "/tmp/mcp.json"),
    ]


@pytest.mark.parametrize(
    "argv",
    [
        ["claude", "--mcp-config"],
        ["claude", "--mcp-config="],
        ["claude", "--mcp-config", "--strict-mcp-config"],
    ],
)
def test_missing_value_is_reported_without_a_path(argv: list[str]) -> None:
    matches = extract_settings_overrides(
        argv,
        [
            SettingsOverrideFlag("--mcp-config", mcp_config="file"),
            SettingsOverrideFlag("--strict-mcp-config", takes_value=False),
        ],
    )

    assert matches[0].flag == "--mcp-config"
    assert matches[0].value is None
    assert matches[0].inline_json is False


def test_ignores_unrecognized_flags() -> None:
    assert (
        extract_settings_overrides(
            ["claude", "--config", "/tmp/config.json"],
            [SettingsOverrideFlag("--settings")],
        )
        == []
    )
