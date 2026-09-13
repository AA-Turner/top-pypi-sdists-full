"""Unit tests for _provider_details."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test__provider_details_normalizes_provider_metadata() -> None:
    details = provider_configuration._provider_details(
        "custom",
        {"type": "local_model", "model": " llama3 "},
    )

    assert details == ("custom", "local_model", "llama3")


def test__provider_details_handles_missing_mapping() -> None:
    assert provider_configuration._provider_details(None, None) == (None, None, None)
