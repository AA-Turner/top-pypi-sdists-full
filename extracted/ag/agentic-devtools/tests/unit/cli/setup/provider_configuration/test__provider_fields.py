"""Unit tests for _provider_fields."""

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test__provider_fields_handles_missing_and_fallback_provider_entries() -> None:
    fields = provider_configuration._provider_fields

    assert fields({}) == (None, None, None)
    assert fields({"providers": {"x": {"type": "local_model", "model": " m "}}}) == (
        "x",
        "local_model",
        "m",
    )
    assert fields({"providers": {"copilot_pr_review": {"type": 1, "model": " "}}}) == (
        "copilot_pr_review",
        None,
        None,
    )
