"""Unit tests for validate_provider_configuration."""

from typing import Any
from unittest.mock import patch

import agentic_devtools.cli.setup.provider_configuration as provider_configuration
from agentic_devtools.cli.setup.provider_configuration import validate_provider_configuration


def _document(provider_type: str = "copilot", **provider_fields: str) -> dict:
    provider = {"type": provider_type, "model": "model-a", **provider_fields}
    return {
        "providers": {"copilot_pr_review": provider},
        "workflows": {
            "pr_review": {
                "default_provider": "copilot_pr_review",
                "nodes": {"review_files": {"provider": "copilot_pr_review"}},
            }
        },
    }


def test_validate_provider_configuration_covers_required_fields() -> None:
    cases: list[tuple[Any, str]] = [
        (None, "invalid_root"),
        ({}, "providers_missing"),
        ({"providers": []}, "invalid_configuration"),
        ({"providers": {}}, "provider_missing"),
        ({"providers": {"copilot_pr_review": {"type": "openai", "model": "m"}}}, "invalid_configuration"),
        ({"providers": {"copilot_pr_review": {"type": "copilot", "model": ""}}}, "invalid_configuration"),
        (
            {
                **_document(),
                "providers": {
                    "copilot_pr_review": {**_document()["providers"]["copilot_pr_review"], "api_key_env": "KEY"}
                },
            },
            "invalid_configuration",
        ),
        ({**_document(), "workflows": {}}, "workflow_mapping_missing"),
        ({**_document(), "workflows": {"pr_review": {}}}, "default_provider_missing"),
        (
            {**_document(), "workflows": {"pr_review": {"default_provider": "copilot_pr_review", "nodes": {}}}},
            "review_files_mapping_missing",
        ),
    ]
    for document, expected in cases:
        assert validate_provider_configuration(document) == [expected]
    with patch.object(provider_configuration, "validate_config", return_value=[]):
        assert validate_provider_configuration({"providers": {}}) == ["provider_missing"]
        assert validate_provider_configuration({"providers": {"copilot_pr_review": {"type": "openai"}}}) == [
            "provider_type_invalid"
        ]
        assert validate_provider_configuration(
            {"providers": {"copilot_pr_review": {"type": "copilot", "model": ""}}}
        ) == ["model_missing"]
        assert validate_provider_configuration(
            {"providers": {"copilot_pr_review": {"type": "copilot", "model": "m", "api_key_env": "KEY"}}}
        ) == ["copilot_api_key_env_forbidden"]
