"""Comprehensive tests for sage/core/model_selector.py - Model selection."""

import pytest
from dataclasses import dataclass

from sage.core.model_selector import (
    TaskType,
    TaskAnalysis,
    ModelSelector,
    auto_select_model,
)
from sage.providers.base import ModelInfo


# =============================================================================
# Helper function to create ModelInfo
# =============================================================================


def make_model(model_id: str, name: str = "", local: bool = False) -> ModelInfo:
    """Create a ModelInfo for testing."""
    return ModelInfo(
        id=model_id,
        provider="test",
        name=name or model_id,
        local=local,
    )


# =============================================================================
# Tests for TaskType enum
# =============================================================================


class TestTaskType:
    """Tests for TaskType enum."""

    def test_coding(self):
        """CODING is defined."""
        assert TaskType.CODING is not None

    def test_reasoning(self):
        """REASONING is defined."""
        assert TaskType.REASONING is not None

    def test_chat(self):
        """CHAT is defined."""
        assert TaskType.CHAT is not None

    def test_vision(self):
        """VISION is defined."""
        assert TaskType.VISION is not None

    def test_embedding(self):
        """EMBEDDING is defined."""
        assert TaskType.EMBEDDING is not None

    def test_summarization(self):
        """SUMMARIZATION is defined."""
        assert TaskType.SUMMARIZATION is not None

    def test_translation(self):
        """TRANSLATION is defined."""
        assert TaskType.TRANSLATION is not None

    def test_analysis(self):
        """ANALYSIS is defined."""
        assert TaskType.ANALYSIS is not None

    def test_creative(self):
        """CREATIVE is defined."""
        assert TaskType.CREATIVE is not None


# =============================================================================
# Tests for TaskAnalysis dataclass
# =============================================================================


class TestTaskAnalysis:
    """Tests for TaskAnalysis dataclass."""

    def test_create(self):
        """Create TaskAnalysis."""
        analysis = TaskAnalysis(
            task_type=TaskType.CODING,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=True,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        assert analysis.task_type == TaskType.CODING
        assert analysis.complexity == 0.5
        assert analysis.requires_large_context is False
        assert analysis.requires_code_execution is True
        assert analysis.requires_vision is False
        assert analysis.estimated_tokens == 100
        assert analysis.confidence == 0.8


# =============================================================================
# Tests for ModelSelector class constants
# =============================================================================


class TestModelSelectorConstants:
    """Tests for ModelSelector constants."""

    def test_coding_patterns(self):
        """CODING_PATTERNS contains patterns."""
        assert len(ModelSelector.CODING_PATTERNS) > 0
        assert any("code" in p for p in ModelSelector.CODING_PATTERNS)

    def test_reasoning_patterns(self):
        """REASONING_PATTERNS contains patterns."""
        assert len(ModelSelector.REASONING_PATTERNS) > 0
        assert any("solve" in p for p in ModelSelector.REASONING_PATTERNS)

    def test_vision_patterns(self):
        """VISION_PATTERNS contains patterns."""
        assert len(ModelSelector.VISION_PATTERNS) > 0
        assert any("image" in p for p in ModelSelector.VISION_PATTERNS)

    def test_creative_patterns(self):
        """CREATIVE_PATTERNS contains patterns."""
        assert len(ModelSelector.CREATIVE_PATTERNS) > 0
        assert any("write" in p for p in ModelSelector.CREATIVE_PATTERNS)

    def test_model_capabilities(self):
        """MODEL_CAPABILITIES contains mappings."""
        assert len(ModelSelector.MODEL_CAPABILITIES) > 0


# =============================================================================
# Tests for ModelSelector initialization
# =============================================================================


class TestModelSelectorInit:
    """Tests for ModelSelector initialization."""

    def test_default_init(self):
        """Initialize with defaults."""
        selector = ModelSelector()
        assert selector.available_models == []
        assert len(selector._compiled_patterns) == 4

    def test_with_models(self):
        """Initialize with models."""
        models = [make_model("model1"), make_model("model2")]
        selector = ModelSelector(available_models=models)
        assert len(selector.available_models) == 2


# =============================================================================
# Tests for analyze_task method
# =============================================================================


class TestAnalyzeTask:
    """Tests for analyze_task method."""

    def test_detect_coding_task(self):
        """Detect coding task from prompt."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Write a Python function to sort a list")
        assert analysis.task_type == TaskType.CODING

    def test_detect_coding_from_code_block(self):
        """Detect coding from code block."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Fix this code:\n```python\ndef foo():\n```")
        assert analysis.task_type == TaskType.CODING

    def test_detect_reasoning_task(self):
        """Detect reasoning task from prompt."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Solve this math equation: 2x + 5 = 15")
        assert analysis.task_type == TaskType.REASONING

    def test_detect_vision_task(self):
        """Detect vision task from prompt."""
        selector = ModelSelector()
        analysis = selector.analyze_task("What's in this image.png?")
        assert analysis.task_type == TaskType.VISION

    def test_detect_creative_task(self):
        """Detect creative task from prompt."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Write a creative story about dragons")
        assert analysis.task_type == TaskType.CREATIVE

    def test_default_chat_task(self):
        """Default to chat for general prompts."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Hello, how are you?")
        assert analysis.task_type == TaskType.CHAT

    def test_complexity_short_prompt(self):
        """Low complexity for short prompts."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Hi")
        assert analysis.complexity < 0.1

    def test_complexity_long_prompt(self):
        """Higher complexity for long prompts."""
        selector = ModelSelector()
        long_prompt = " ".join(["word"] * 300)
        analysis = selector.analyze_task(long_prompt)
        assert analysis.complexity > 0.5

    def test_requires_large_context(self):
        """Detect large context requirements."""
        selector = ModelSelector()
        large_context = "x" * 15000
        analysis = selector.analyze_task("Query", large_context)
        assert analysis.requires_large_context is True

    def test_no_large_context_small(self):
        """No large context for small inputs."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Small query")
        assert analysis.requires_large_context is False

    def test_requires_code_execution(self):
        """Detect code execution requirements."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Run this code and execute it")
        assert analysis.requires_code_execution is True

    def test_requires_vision(self):
        """Detect vision requirements."""
        selector = ModelSelector()
        analysis = selector.analyze_task("Analyze this screenshot")
        assert analysis.requires_vision is True

    def test_estimated_tokens(self):
        """Estimate tokens from prompt length."""
        selector = ModelSelector()
        prompt = "a" * 400  # 400 chars = ~100 tokens
        analysis = selector.analyze_task(prompt)
        assert analysis.estimated_tokens == 100

    def test_confidence_increases_with_matches(self):
        """Confidence increases with more pattern matches."""
        selector = ModelSelector()
        analysis1 = selector.analyze_task("code")
        analysis2 = selector.analyze_task("code function class method python")
        assert analysis2.confidence >= analysis1.confidence


# =============================================================================
# Tests for get_model_score method
# =============================================================================


class TestGetModelScore:
    """Tests for get_model_score method."""

    def test_coding_model_for_coding_task(self):
        """Coding model scores high for coding tasks."""
        selector = ModelSelector()
        model = make_model("deepseek-coder-7b")
        task = TaskAnalysis(
            task_type=TaskType.CODING,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        score = selector.get_model_score(model, task)
        assert score >= 0.8

    def test_reasoning_model_for_reasoning_task(self):
        """Reasoning model scores high for reasoning tasks."""
        selector = ModelSelector()
        model = make_model("qwq-32b")
        task = TaskAnalysis(
            task_type=TaskType.REASONING,
            complexity=0.7,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        score = selector.get_model_score(model, task)
        assert score >= 0.8

    def test_vision_model_for_vision_task(self):
        """Vision model scores high for vision tasks."""
        selector = ModelSelector()
        model = make_model("llava-7b")
        task = TaskAnalysis(
            task_type=TaskType.VISION,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=True,
            estimated_tokens=100,
            confidence=0.8,
        )
        score = selector.get_model_score(model, task)
        assert score >= 0.8

    def test_non_vision_penalized_for_vision(self):
        """Non-vision model penalized for vision tasks."""
        selector = ModelSelector()
        model = make_model("llama-7b")
        task = TaskAnalysis(
            task_type=TaskType.VISION,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=True,
            estimated_tokens=100,
            confidence=0.8,
        )
        score = selector.get_model_score(model, task)
        assert score < 0.5

    def test_large_model_bonus_for_complex(self):
        """Large models get bonus for complex tasks."""
        selector = ModelSelector()
        model = make_model("llama-70b")
        task = TaskAnalysis(
            task_type=TaskType.REASONING,
            complexity=0.8,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        score = selector.get_model_score(model, task)
        assert score >= 0.9


# =============================================================================
# Tests for select method
# =============================================================================


class TestSelect:
    """Tests for select method."""

    def test_no_models_returns_none(self):
        """Returns None when no models available."""
        selector = ModelSelector()
        model, task = selector.select("Test prompt")
        assert model is None

    def test_selects_best_model(self):
        """Selects best model for task."""
        models = [
            make_model("llama-7b"),
            make_model("deepseek-coder-7b"),
        ]
        selector = ModelSelector(available_models=models)
        model, task = selector.select("Write a Python function")
        assert model is not None
        assert "coder" in model.id

    def test_prefer_fast_small_models(self):
        """Prefers small models when prefer_fast=True."""
        models = [
            make_model("llama-general"),  # No size pattern - base score
            make_model("llama-3b-mini"),  # Small model gets +0.3 bonus
        ]
        selector = ModelSelector(available_models=models)
        model, task = selector.select("Hello", prefer_fast=True)
        assert model is not None
        assert "mini" in model.id or "3b" in model.id

    def test_prefer_local(self):
        """Prefers local models when prefer_local=True."""
        models = [
            make_model("gemini:gemini-2.0-flash"),
            make_model("llama_cpp:llama-7b"),
        ]
        selector = ModelSelector(available_models=models)
        model, task = selector.select("Hello", prefer_local=True)
        assert model is not None
        assert "llama_cpp" in model.id

    def test_returns_task_analysis(self):
        """Returns task analysis with selection."""
        models = [make_model("llama-7b")]
        selector = ModelSelector(available_models=models)
        model, task = selector.select("Write code to sort a list")
        assert task is not None
        assert isinstance(task, TaskAnalysis)


# =============================================================================
# Tests for get_recommendations method
# =============================================================================


class TestGetRecommendations:
    """Tests for get_recommendations method."""

    def test_no_models_returns_empty(self):
        """Returns empty list when no models."""
        selector = ModelSelector()
        task = TaskAnalysis(
            task_type=TaskType.CHAT,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        recs = selector.get_recommendations(task)
        assert recs == []

    def test_returns_limited_recommendations(self):
        """Returns limited number of recommendations."""
        models = [make_model(f"model-{i}") for i in range(10)]
        selector = ModelSelector(available_models=models)
        task = TaskAnalysis(
            task_type=TaskType.CHAT,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        recs = selector.get_recommendations(task, limit=3)
        assert len(recs) <= 3

    def test_recommendations_have_explanations(self):
        """Recommendations include explanations."""
        models = [make_model("deepseek-coder-7b")]
        selector = ModelSelector(available_models=models)
        task = TaskAnalysis(
            task_type=TaskType.CODING,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        recs = selector.get_recommendations(task)
        assert len(recs) == 1
        model, score, explanation = recs[0]
        assert "code" in explanation.lower()

    def test_sorted_by_score(self):
        """Recommendations sorted by score descending."""
        models = [
            make_model("llama-7b"),
            make_model("deepseek-coder-7b"),
        ]
        selector = ModelSelector(available_models=models)
        task = TaskAnalysis(
            task_type=TaskType.CODING,
            complexity=0.5,
            requires_large_context=False,
            requires_code_execution=False,
            requires_vision=False,
            estimated_tokens=100,
            confidence=0.8,
        )
        recs = selector.get_recommendations(task)
        scores = [r[1] for r in recs]
        assert scores == sorted(scores, reverse=True)


# =============================================================================
# Tests for auto_select_model function
# =============================================================================


class TestAutoSelectModel:
    """Tests for auto_select_model function."""

    def test_returns_model_id(self):
        """Returns model ID string."""
        models = [make_model("llama-7b")]
        result = auto_select_model("Hello", models)
        assert result == "llama-7b"

    def test_returns_none_no_models(self):
        """Returns None when no models available."""
        result = auto_select_model("Hello", [])
        assert result is None

    def test_with_context(self):
        """Works with context parameter."""
        models = [make_model("llama-7b")]
        result = auto_select_model("Test", models, context="Additional context")
        assert result == "llama-7b"


# =============================================================================
# Integration tests
# =============================================================================


class TestModelSelectorIntegration:
    """Integration tests for ModelSelector."""

    def test_full_selection_workflow(self):
        """Full model selection workflow."""
        models = [
            make_model("llama-7b"),
            make_model("deepseek-coder-7b"),
            make_model("qwq-32b"),
            make_model("llava-7b-vision"),
        ]
        selector = ModelSelector(available_models=models)

        # Test coding task
        model, task = selector.select("Write a Python class to handle HTTP requests")
        assert task.task_type == TaskType.CODING
        assert "coder" in model.id

        # Test reasoning task
        model, task = selector.select("Solve the equation 2x + 3 = 15 step by step")
        assert task.task_type == TaskType.REASONING

        # Test vision task
        model, task = selector.select("What's in this image.png file?")
        assert task.task_type == TaskType.VISION
        assert "vision" in model.id or "llava" in model.id

    def test_recommendations_for_different_tasks(self):
        """Get recommendations for different task types."""
        models = [
            make_model("llama-7b"),
            make_model("deepseek-coder-7b"),
            make_model("llama-70b"),
        ]
        selector = ModelSelector(available_models=models)

        # Coding task
        task = selector.analyze_task("Implement a sorting algorithm")
        recs = selector.get_recommendations(task)
        assert len(recs) == 3
        # Best should be coder
        assert "coder" in recs[0][0].id

        # Complex reasoning
        task = selector.analyze_task("Solve complex mathematical proof " * 50)
        recs = selector.get_recommendations(task)
        # Large model should score well for complex task
        large_model_scores = [r[1] for r in recs if "70b" in r[0].id]
        assert len(large_model_scores) > 0

    def test_pattern_matching_case_insensitive(self):
        """Pattern matching is case insensitive."""
        selector = ModelSelector()
        
        # Should detect coding regardless of case
        analysis1 = selector.analyze_task("Write a PYTHON function")
        analysis2 = selector.analyze_task("Write a python function")
        assert analysis1.task_type == analysis2.task_type
