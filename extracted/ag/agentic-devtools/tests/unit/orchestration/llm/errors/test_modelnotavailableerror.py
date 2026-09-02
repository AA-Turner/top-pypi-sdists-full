"""Tests for ModelNotAvailableError."""

from agentic_devtools.orchestration.llm.errors import LLMError, ModelNotAvailableError


class TestModelNotAvailableError:
    """Tests for ModelNotAvailableError."""

    def test_attributes_and_default_message(self):
        err = ModelNotAvailableError(provider_type="copilot", model="missing")

        assert "not available" in str(err)
        assert err.provider_type == "copilot"
        assert err.model == "missing"

    def test_is_llm_error(self):
        assert issubclass(ModelNotAvailableError, LLMError)
