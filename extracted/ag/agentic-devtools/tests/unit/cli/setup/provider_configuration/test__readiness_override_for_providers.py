"""Unit tests for _readiness_override_for_providers."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def _ready(_document: dict) -> tuple[str, str]:
    return ("ready", "ready")


def test__readiness_override_for_providers_handles_skip_policy() -> None:
    assert (
        provider_configuration._readiness_override_for_providers(
            None,
            skip_model_refresh=False,
            provider_types=(None,),
        )
        is None
    )
    assert (
        provider_configuration._readiness_override_for_providers(
            _ready,
            skip_model_refresh=False,
            provider_types=("local_model",),
        )
        is _ready
    )
    assert (
        provider_configuration._readiness_override_for_providers(
            _ready,
            skip_model_refresh=True,
            provider_types=("copilot",),
        )
        is _ready
    )
    assert (
        provider_configuration._readiness_override_for_providers(
            _ready,
            skip_model_refresh=True,
            provider_types=("local_model",),
        )
        is None
    )
