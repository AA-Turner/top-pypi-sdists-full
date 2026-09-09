"""Unit tests for _select_model."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test__select_model_prefers_explicit_existing_and_available_fallbacks() -> None:
    select = provider_configuration._select_model

    assert (
        select(explicit_model="x", existing_model=None, available_models=["x"], defaults=False, interactive=True)[0]
        == "x"
    )
    assert (
        select(explicit_model="bad", existing_model="x", available_models=["x"], defaults=False, interactive=True)[0]
        == "x"
    )
    assert (
        select(explicit_model=None, existing_model=None, available_models=None, defaults=True, interactive=False)[2]
        == "model_unavailable_without_refresh"
    )
    assert (
        select(explicit_model=None, existing_model=None, available_models=["x"], defaults=False, interactive=False)[0]
        == "x"
    )
