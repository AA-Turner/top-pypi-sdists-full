"""Tests for sage.reasoning module."""

import pytest

from sage.reasoning import (
    ChainOfThoughtReasoner,
    ErrorDiagnosis,
    Hypothesis,
    ProblemAnalysis,
    ReasoningContext,
    ReasoningPhase,
    ReasoningStep,
    SubTask,
)


class TestReasoningPhase:
    """Test ReasoningPhase enum."""

    def test_all_phases_exist(self):
        """Test that all expected phases exist."""
        assert ReasoningPhase.UNDERSTAND is not None
        assert ReasoningPhase.DECOMPOSE is not None
        assert ReasoningPhase.ANALYZE is not None
        assert ReasoningPhase.HYPOTHESIZE is not None
        assert ReasoningPhase.EVALUATE is not None
        assert ReasoningPhase.SYNTHESIZE is not None
        assert ReasoningPhase.VALIDATE is not None
        assert ReasoningPhase.REFLECT is not None

    def test_phase_values(self):
        """Test that phases have string values."""
        assert ReasoningPhase.UNDERSTAND.value == "understand"
        assert ReasoningPhase.DECOMPOSE.value == "decompose"


class TestReasoningStep:
    """Test ReasoningStep dataclass."""

    def test_create_step(self):
        """Test creating a reasoning step."""
        step = ReasoningStep(
            phase=ReasoningPhase.UNDERSTAND,
            thought="This is a test task",
            evidence=["evidence1", "evidence2"],
            confidence=0.8,
        )
        assert step.phase == ReasoningPhase.UNDERSTAND
        assert step.thought == "This is a test task"
        assert len(step.evidence) == 2
        assert step.confidence == 0.8
        assert step.timestamp is not None

    def test_default_values(self):
        """Test default values for reasoning step."""
        step = ReasoningStep(
            phase=ReasoningPhase.ANALYZE,
            thought="Test",
        )
        assert step.evidence == []
        assert step.confidence == 0.5


class TestHypothesis:
    """Test Hypothesis dataclass."""

    def test_create_hypothesis(self):
        """Test creating a hypothesis."""
        hyp = Hypothesis(
            id="h1",
            description="Test hypothesis",
            approach="Use TDD approach",
            pros=["Fast", "Reliable"],
            cons=["Complex"],
            confidence=0.75,
        )
        assert hyp.id == "h1"
        assert hyp.description == "Test hypothesis"
        assert len(hyp.pros) == 2
        assert len(hyp.cons) == 1
        assert hyp.confidence == 0.75
        assert hyp.validated is False

    def test_validation_state(self):
        """Test hypothesis validation."""
        hyp = Hypothesis(
            id="h1",
            description="Test",
            approach="Test approach",
            validated=True,
            validation_result="Passed all tests",
        )
        assert hyp.validated is True
        assert hyp.validation_result == "Passed all tests"


class TestProblemAnalysis:
    """Test ProblemAnalysis dataclass."""

    def test_create_analysis(self):
        """Test creating a problem analysis."""
        analysis = ProblemAnalysis(
            original_task="Implement feature X",
            goals=["Goal 1", "Goal 2"],
            constraints=["Constraint 1"],
            risks=["Risk 1"],
        )
        assert analysis.original_task == "Implement feature X"
        assert len(analysis.goals) == 2
        assert len(analysis.constraints) == 1
        assert len(analysis.risks) == 1

    def test_default_lists(self):
        """Test that lists are empty by default."""
        analysis = ProblemAnalysis(original_task="Task")
        assert analysis.goals == []
        assert analysis.constraints == []
        assert analysis.assumptions == []
        assert analysis.risks == []
        assert analysis.inputs == []
        assert analysis.outputs == []
        assert analysis.edge_cases == []
        assert analysis.dependencies == []
        assert analysis.success_criteria == []


class TestSubTask:
    """Test SubTask dataclass."""

    def test_create_subtask(self):
        """Test creating a subtask."""
        task = SubTask(
            id="st1",
            description="Implement function X",
            type="implementation",
            priority=1,
            complexity=3,
            dependencies=["st0"],
            files_involved=["src/module.py"],
        )
        assert task.id == "st1"
        assert task.type == "implementation"
        assert task.priority == 1
        assert task.complexity == 3
        assert task.status == "pending"

    def test_subtask_status(self):
        """Test subtask status transitions."""
        task = SubTask(
            id="st1",
            description="Test",
            type="testing",
            priority=2,
            complexity=2,
            status="in_progress",
        )
        assert task.status == "in_progress"


class TestReasoningContext:
    """Test ReasoningContext dataclass."""

    def test_create_context(self):
        """Test creating a reasoning context."""
        ctx = ReasoningContext(task="Build a REST API")
        assert ctx.task == "Build a REST API"
        assert ctx.analysis is None
        assert ctx.subtasks == []
        assert ctx.hypotheses == []
        assert ctx.reasoning_chain == []

    def test_context_with_data(self):
        """Test context with populated data."""
        analysis = ProblemAnalysis(original_task="Task")
        step = ReasoningStep(phase=ReasoningPhase.UNDERSTAND, thought="Test")

        ctx = ReasoningContext(
            task="Test task",
            analysis=analysis,
            reasoning_chain=[step],
            files_read={"file1.py", "file2.py"},
        )
        assert ctx.analysis is not None
        assert len(ctx.reasoning_chain) == 1
        assert len(ctx.files_read) == 2


class TestChainOfThoughtReasoner:
    """Test ChainOfThoughtReasoner class."""

    def test_phase_prompts_class_attribute(self):
        """Test that phase prompts are defined as class attribute."""
        assert hasattr(ChainOfThoughtReasoner, "PHASE_PROMPTS")
        assert isinstance(ChainOfThoughtReasoner.PHASE_PROMPTS, dict)

    def test_all_phases_have_prompts(self):
        """Test that all phases have prompts defined."""
        for phase in ReasoningPhase:
            assert phase in ChainOfThoughtReasoner.PHASE_PROMPTS

    def test_prompts_contain_placeholders(self):
        """Test that prompts contain expected placeholders."""
        understand_prompt = ChainOfThoughtReasoner.PHASE_PROMPTS[ReasoningPhase.UNDERSTAND]
        assert "{task}" in understand_prompt


class TestErrorDiagnosis:
    """Test ErrorDiagnosis class."""

    def test_diagnosis_class_exists(self):
        """Test ErrorDiagnosis class is importable."""
        assert ErrorDiagnosis is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
