"""Unit tests for _provider_check_remediation."""

from types import SimpleNamespace

from agentic_devtools.cli.setup import commands


def test__provider_check_remediation_returns_reason_specific_guidance() -> None:
    assert "gh auth login" in commands._provider_check_remediation(SimpleNamespace(reason="authentication_unavailable"))
    assert "pick a supported model" in commands._provider_check_remediation(SimpleNamespace(reason="model_unavailable"))
    assert "create `.agdt/config/llm-providers.yml`" in commands._provider_check_remediation(
        SimpleNamespace(reason="missing_file")
    )
    assert "set the environment variable referenced" in commands._provider_check_remediation(
        SimpleNamespace(reason="credential_missing")
    )


def test__provider_check_remediation_returns_edit_or_regenerate_guidance_for_config_errors() -> None:
    message = commands._provider_check_remediation(SimpleNamespace(reason="review_files_mapping_missing"))

    assert "edit `.agdt/config/llm-providers.yml`" in message
    assert "run `agdt-setup --reconfigure`" in message


def test__provider_check_remediation_returns_default_guidance_for_unknown_reason() -> None:
    message = commands._provider_check_remediation(SimpleNamespace(reason="unknown_reason"))

    assert message == "run `agdt-setup --reconfigure` after completing the prerequisite."
