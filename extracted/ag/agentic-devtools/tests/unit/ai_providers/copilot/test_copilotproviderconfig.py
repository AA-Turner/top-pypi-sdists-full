from dataclasses import replace
from typing import Any, cast

import pytest

from agentic_devtools.ai_providers import CopilotProviderConfig, ModelDiscovery, ModelRecord


class FakeTransport:
    def request(self, method, url, *, headers, json_body, timeout):
        raise AssertionError("should not be called")  # pragma: no cover


class FakeDiscovery(ModelDiscovery):
    def _discover_models(self) -> list[ModelRecord]:
        return []  # pragma: no cover


def _config(transport=None) -> CopilotProviderConfig:
    return CopilotProviderConfig(
        owner="octo",
        repo="demo",
        base_url="https://api.github.com",
        api_version="2026-03-10",
        timeout_seconds=3.5,
        transport=transport or FakeTransport(),
        model_discovery=FakeDiscovery(),
        auth_header_factory=lambda: {"Authorization": "******"},
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("owner", ""),
        ("owner", "../owner"),
        ("repo", "repo/name"),
        ("base_url", ""),
        ("base_url", "http://api.github.com"),
        ("base_url", "https://api.github.com/v1"),
        ("base_url", "https://api.github.com?x=1"),
        ("base_url", "https://api.github.com:notaport"),
        ("base_url", "https://api.github.com:0"),
        ("base_url", "https://api.github.com:70000"),
        ("base_url", "https://@api.github.com"),
        ("base_url", "https://api github.com"),
        ("base_url", "https:///"),
        ("base_url", "******api.github.com"),
        ("base_url", r"https://api.github.com\evil"),
        ("base_url", "https://api..github.com"),
        ("base_url", "https://api.-github.com"),
        ("base_url", "https://api.github-.com"),
        ("base_url", f"https://{'a' * 64}.{'b' * 64}.{'c' * 64}.{'d' * 62}.com"),
        ("api_version", "2022-11-28"),
        ("timeout_seconds", 0),
        ("timeout_seconds", float("nan")),
    ],
)
def test_config_rejects_malformed_values(field: str, value: object) -> None:
    with pytest.raises(ValueError):
        replace(_config(), **cast(Any, {field: value}))


@pytest.mark.parametrize(
    "field",
    ["transport", "model_discovery", "auth_header_factory"],
)
def test_config_requires_explicit_dependencies(field: str) -> None:
    with pytest.raises(ValueError):
        replace(_config(), **cast(Any, {field: object()}))
