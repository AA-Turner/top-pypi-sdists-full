"""Unit tests for _managed_copilot_provider."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test__managed_copilot_provider_builds_default_mapping_without_existing_provider() -> None:
    provider = provider_configuration._managed_copilot_provider(None, model="gemini-3.7-flash")

    assert provider == {
        "type": "copilot",
        "model": "gemini-3.7-flash",
    }


def test__managed_copilot_provider_skips_invalid_timeout_and_preserves_existing_key_order() -> None:
    existing_provider = {
        "model": "old-model",
        "timeout_seconds": True,
        "type": "local_model",
        "headers": {"Authorization": "******"},
    }

    provider = provider_configuration._managed_copilot_provider(existing_provider, model="new-model")

    assert provider == {
        "model": "new-model",
        "type": "copilot",
    }
