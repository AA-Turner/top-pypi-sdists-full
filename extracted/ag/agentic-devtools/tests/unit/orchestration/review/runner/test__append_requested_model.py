"""Tests for ``_append_requested_model()``."""

from agentic_devtools.orchestration.review.runner import _append_requested_model


class TestAppendRequestedModel:
    """Covers normalization and deduplication of preflight model lists."""

    def test_ignores_non_string_candidates(self) -> None:
        requested_models = ["gpt-4o"]

        _append_requested_model(requested_models, 42)

        assert requested_models == ["gpt-4o"]

    def test_ignores_blank_and_duplicate_models(self) -> None:
        requested_models = ["gpt-4o"]

        _append_requested_model(requested_models, "  ")
        _append_requested_model(requested_models, "gpt-4o")

        assert requested_models == ["gpt-4o"]

    def test_appends_trimmed_unique_model(self) -> None:
        requested_models = ["gpt-4o"]

        _append_requested_model(requested_models, "  gemini-3.7-flash  ")

        assert requested_models == ["gpt-4o", "gemini-3.7-flash"]
