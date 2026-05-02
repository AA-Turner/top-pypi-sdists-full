"""Comprehensive tests for sage/core/prompt_system.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch
from dataclasses import dataclass

import pytest


# =============================================================================
# Tests for TaskType Enum
# =============================================================================


class TestTaskType:
    """Tests for TaskType enum."""

    def test_import(self):
        """TaskType can be imported."""
        from sage.core.prompt_system import TaskType
        assert TaskType is not None

    def test_code_generation(self):
        """CODE_GENERATION value."""
        from sage.core.prompt_system import TaskType
        assert TaskType.CODE_GENERATION.value == "code_generation"

    def test_code_review(self):
        """CODE_REVIEW value."""
        from sage.core.prompt_system import TaskType
        assert TaskType.CODE_REVIEW.value == "code_review"

    def test_bug_fix(self):
        """BUG_FIX value."""
        from sage.core.prompt_system import TaskType
        assert TaskType.BUG_FIX.value == "bug_fix"

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.prompt_system import TaskType
        expected = [
            "code_generation", "code_review", "bug_fix", "refactoring",
            "documentation", "testing", "explanation", "architecture",
            "debugging", "general"
        ]
        values = [t.value for t in TaskType]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for PromptStyle Enum
# =============================================================================


class TestPromptStyle:
    """Tests for PromptStyle enum."""

    def test_import(self):
        """PromptStyle can be imported."""
        from sage.core.prompt_system import PromptStyle
        assert PromptStyle is not None

    def test_concise(self):
        """CONCISE value."""
        from sage.core.prompt_system import PromptStyle
        assert PromptStyle.CONCISE.value == "concise"

    def test_detailed(self):
        """DETAILED value."""
        from sage.core.prompt_system import PromptStyle
        assert PromptStyle.DETAILED.value == "detailed"

    def test_all_styles(self):
        """All expected styles exist."""
        from sage.core.prompt_system import PromptStyle
        expected = ["concise", "detailed", "step_by_step", "technical", "beginner"]
        values = [s.value for s in PromptStyle]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for FewShotExample
# =============================================================================


class TestFewShotExample:
    """Tests for FewShotExample dataclass."""

    def test_create(self):
        """Create FewShotExample."""
        from sage.core.prompt_system import FewShotExample, TaskType

        example = FewShotExample(
            id="ex1",
            task_type=TaskType.CODE_GENERATION,
            input_text="Write a hello world function",
            output_text="def hello(): print('Hello, World!')",
        )
        assert example.id == "ex1"
        assert example.task_type == TaskType.CODE_GENERATION

    def test_defaults(self):
        """Default values."""
        from sage.core.prompt_system import FewShotExample, TaskType

        example = FewShotExample(
            id="ex1",
            task_type=TaskType.GENERAL,
            input_text="Input",
            output_text="Output",
        )
        assert example.tags == []
        assert example.language == "python"
        assert example.quality_score == 1.0
        assert example.usage_count == 0

    def test_to_prompt(self):
        """to_prompt formats correctly."""
        from sage.core.prompt_system import FewShotExample, TaskType

        example = FewShotExample(
            id="ex1",
            task_type=TaskType.GENERAL,
            input_text="Question?",
            output_text="Answer!",
        )
        prompt = example.to_prompt()
        assert "User: Question?" in prompt
        assert "Assistant: Answer!" in prompt


# =============================================================================
# Tests for FewShotSelector
# =============================================================================


class TestFewShotSelector:
    """Tests for FewShotSelector class."""

    def test_create_empty(self):
        """Create empty selector."""
        from sage.core.prompt_system import FewShotSelector

        selector = FewShotSelector()
        assert selector.examples == []

    def test_create_with_examples(self):
        """Create with initial examples."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        examples = [
            FewShotExample("e1", TaskType.GENERAL, "in", "out"),
        ]
        selector = FewShotSelector(examples=examples)
        assert len(selector.examples) == 1

    def test_add_example(self):
        """Add example to selector."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        selector = FewShotSelector()
        example = FewShotExample("e1", TaskType.GENERAL, "in", "out")
        selector.add_example(example)

        assert len(selector.examples) == 1

    def test_select_by_task_type(self):
        """Select filters by task type."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        examples = [
            FewShotExample("e1", TaskType.CODE_GENERATION, "gen code", "code"),
            FewShotExample("e2", TaskType.BUG_FIX, "fix bug", "fixed"),
        ]
        selector = FewShotSelector(examples=examples)

        result = selector.select("generate", task_type=TaskType.CODE_GENERATION)
        assert len(result) == 1
        assert result[0].task_type == TaskType.CODE_GENERATION

    def test_select_by_language(self):
        """Select filters by language."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        examples = [
            FewShotExample("e1", TaskType.GENERAL, "python test", "out", language="python"),
            FewShotExample("e2", TaskType.GENERAL, "java test", "out", language="java"),
        ]
        selector = FewShotSelector(examples=examples)

        result = selector.select("test", language="python")
        assert len(result) == 1
        assert result[0].language == "python"

    def test_select_max_examples(self):
        """Select respects max_examples."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        examples = [
            FewShotExample(f"e{i}", TaskType.GENERAL, "test", "out")
            for i in range(10)
        ]
        selector = FewShotSelector(examples=examples)

        result = selector.select("test", max_examples=3)
        assert len(result) == 3

    def test_select_updates_usage_count(self):
        """Select updates usage count."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        example = FewShotExample("e1", TaskType.GENERAL, "test query", "out")
        selector = FewShotSelector(examples=[example])

        selector.select("test query")
        assert example.usage_count == 1

    def test_format_examples_empty(self):
        """Format empty examples."""
        from sage.core.prompt_system import FewShotSelector

        selector = FewShotSelector()
        result = selector.format_examples([])
        assert result == ""

    def test_format_examples(self):
        """Format examples."""
        from sage.core.prompt_system import FewShotSelector, FewShotExample, TaskType

        examples = [
            FewShotExample("e1", TaskType.GENERAL, "Q1", "A1"),
        ]
        selector = FewShotSelector()

        result = selector.format_examples(examples)
        assert "Example 1" in result
        assert "Q1" in result
        assert "A1" in result


# =============================================================================
# Tests for PromptCompressor
# =============================================================================


class TestPromptCompressor:
    """Tests for PromptCompressor class."""

    def test_import(self):
        """PromptCompressor can be imported."""
        from sage.core.prompt_system import PromptCompressor
        assert PromptCompressor is not None

    def test_create(self):
        """Create PromptCompressor."""
        from sage.core.prompt_system import PromptCompressor

        compressor = PromptCompressor()
        assert compressor is not None


# =============================================================================
# Tests for PromptVersion
# =============================================================================


class TestPromptVersion:
    """Tests for PromptVersion dataclass."""

    def test_import(self):
        """PromptVersion can be imported."""
        from sage.core.prompt_system import PromptVersion
        assert PromptVersion is not None


# =============================================================================
# Tests for PromptVersionManager
# =============================================================================


class TestPromptVersionManager:
    """Tests for PromptVersionManager class."""

    def test_import(self):
        """PromptVersionManager can be imported."""
        from sage.core.prompt_system import PromptVersionManager
        assert PromptVersionManager is not None

    def test_create(self):
        """Create PromptVersionManager."""
        from sage.core.prompt_system import PromptVersionManager

        manager = PromptVersionManager()
        assert manager is not None


# =============================================================================
# Tests for PromptGuard
# =============================================================================


class TestPromptGuard:
    """Tests for PromptGuard class."""

    def test_import(self):
        """PromptGuard can be imported."""
        from sage.core.prompt_system import PromptGuard
        assert PromptGuard is not None

    def test_create(self):
        """Create PromptGuard."""
        from sage.core.prompt_system import PromptGuard

        guard = PromptGuard()
        assert guard is not None


# =============================================================================
# Tests for ABTest Classes
# =============================================================================


class TestABTestResult:
    """Tests for ABTestResult dataclass."""

    def test_import(self):
        """ABTestResult can be imported."""
        from sage.core.prompt_system import ABTestResult
        assert ABTestResult is not None


class TestABTest:
    """Tests for ABTest dataclass."""

    def test_import(self):
        """ABTest can be imported."""
        from sage.core.prompt_system import ABTest
        assert ABTest is not None


class TestABTestManager:
    """Tests for ABTestManager class."""

    def test_import(self):
        """ABTestManager can be imported."""
        from sage.core.prompt_system import ABTestManager
        assert ABTestManager is not None

    def test_create(self):
        """Create ABTestManager."""
        from sage.core.prompt_system import ABTestManager

        manager = ABTestManager()
        assert manager is not None


# =============================================================================
# Tests for PromptFeedback Classes
# =============================================================================


class TestPromptFeedback:
    """Tests for PromptFeedback dataclass."""

    def test_import(self):
        """PromptFeedback can be imported."""
        from sage.core.prompt_system import PromptFeedback
        assert PromptFeedback is not None


class TestPromptFeedbackCollector:
    """Tests for PromptFeedbackCollector class."""

    def test_import(self):
        """PromptFeedbackCollector can be imported."""
        from sage.core.prompt_system import PromptFeedbackCollector
        assert PromptFeedbackCollector is not None

    def test_create(self):
        """Create PromptFeedbackCollector."""
        from sage.core.prompt_system import PromptFeedbackCollector

        collector = PromptFeedbackCollector()
        assert collector is not None


# =============================================================================
# Tests for PromptLocalization
# =============================================================================


class TestPromptLocalization:
    """Tests for PromptLocalization class."""

    def test_import(self):
        """PromptLocalization can be imported."""
        from sage.core.prompt_system import PromptLocalization
        assert PromptLocalization is not None

    def test_create(self):
        """Create PromptLocalization."""
        from sage.core.prompt_system import PromptLocalization

        localization = PromptLocalization()
        assert localization is not None


# =============================================================================
# Tests for DynamicPromptBuilder
# =============================================================================


class TestDynamicPromptBuilder:
    """Tests for DynamicPromptBuilder class."""

    def test_import(self):
        """DynamicPromptBuilder can be imported."""
        from sage.core.prompt_system import DynamicPromptBuilder
        assert DynamicPromptBuilder is not None

    def test_create(self):
        """Create DynamicPromptBuilder."""
        from sage.core.prompt_system import DynamicPromptBuilder

        builder = DynamicPromptBuilder()
        assert builder is not None
