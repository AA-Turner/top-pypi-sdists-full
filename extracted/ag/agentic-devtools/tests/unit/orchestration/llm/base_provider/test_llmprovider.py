"""Tests for abstract LLMProvider interface."""

import pytest

from agentic_devtools.orchestration.llm.base_provider import LLMProvider


class TestLLMProvider:
    """Tests for LLMProvider ABC."""

    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError, match="abstract"):
            LLMProvider()  # type: ignore[abstract]

    def test_enforces_complete_signature(self):
        assert hasattr(LLMProvider, "complete")
        assert hasattr(LLMProvider, "complete_structured")
        assert hasattr(LLMProvider, "stream")

    def test_concrete_subclass_must_implement_all(self):
        class IncompleteProvider(LLMProvider):
            pass

        with pytest.raises(TypeError):
            IncompleteProvider()  # type: ignore[abstract]
