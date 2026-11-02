"""Class-level tests for ``PipelineValidationError`` (T047a)."""

from __future__ import annotations

from agentic_devtools.cli.jira.creation_pipeline import PipelineValidationError


class TestPipelineValidationError:
    def test_message_maps_to_str(self):
        err = PipelineValidationError("bad input")
        assert str(err) == "bad input"
        assert err.message == "bad input"

    def test_cause_defaults_to_none(self):
        err = PipelineValidationError("bad input")
        assert err.cause is None

    def test_cause_is_stored_when_provided(self):
        original = ValueError("root cause")
        err = PipelineValidationError("wrapped", cause=original)
        assert err.cause is original
        assert err.message == "wrapped"
        assert str(err) == "wrapped"

    def test_is_exception_subclass(self):
        assert issubclass(PipelineValidationError, Exception)

    def test_can_be_raised_and_caught(self):
        try:
            raise PipelineValidationError("boom")
        except PipelineValidationError as caught:
            assert caught.message == "boom"
        else:  # pragma: no cover - defensive
            raise AssertionError("not raised")
