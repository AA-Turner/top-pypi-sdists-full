"""
Comprehensive tests for sage/reasoning.py

Tests chain-of-thought reasoning, self-reflection, multi-perspective
analysis, and error diagnosis.
"""

import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from sage.reasoning import (
    ReasoningPhase,
    ReasoningStep,
    Hypothesis,
    ProblemAnalysis,
    SubTask,
    ReasoningContext,
    ChainOfThoughtReasoner,
    SelfReflectionEngine,
    MultiPerspectiveAnalyzer,
    ErrorDiagnosis,
)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUM TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestReasoningPhase:
    """Tests for ReasoningPhase enum."""

    def test_all_phases_exist(self):
        """Test all reasoning phases are defined."""
        assert ReasoningPhase.UNDERSTAND is not None
        assert ReasoningPhase.DECOMPOSE is not None
        assert ReasoningPhase.ANALYZE is not None
        assert ReasoningPhase.HYPOTHESIZE is not None
        assert ReasoningPhase.EVALUATE is not None
        assert ReasoningPhase.SYNTHESIZE is not None
        assert ReasoningPhase.VALIDATE is not None
        assert ReasoningPhase.REFLECT is not None

    def test_phases_have_values(self):
        """Test phases have string values."""
        assert ReasoningPhase.UNDERSTAND.value == "understand"
        assert ReasoningPhase.DECOMPOSE.value == "decompose"
        assert ReasoningPhase.ANALYZE.value == "analyze"

    def test_phases_are_unique(self):
        """Test all phases have unique values."""
        values = [p.value for p in ReasoningPhase]
        assert len(values) == len(set(values))


# ═══════════════════════════════════════════════════════════════════════════════
# DATACLASS TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestReasoningStep:
    """Tests for ReasoningStep dataclass."""

    def test_creation(self):
        """Test ReasoningStep creation."""
        step = ReasoningStep(
            phase=ReasoningPhase.UNDERSTAND,
            thought="This is my thought",
            evidence=["evidence1", "evidence2"],
            confidence=0.8,
        )
        assert step.phase == ReasoningPhase.UNDERSTAND
        assert step.thought == "This is my thought"
        assert len(step.evidence) == 2
        assert step.confidence == 0.8
        assert step.timestamp is not None

    def test_defaults(self):
        """Test default values."""
        step = ReasoningStep(
            phase=ReasoningPhase.ANALYZE,
            thought="thought",
        )
        assert step.evidence == []
        assert step.confidence == 0.5
        assert step.timestamp is not None


class TestHypothesis:
    """Tests for Hypothesis dataclass."""

    def test_creation(self):
        """Test Hypothesis creation."""
        hypothesis = Hypothesis(
            id="h1",
            description="Test hypothesis",
            approach="Use TDD approach",
            pros=["fast", "reliable"],
            cons=["complex"],
            confidence=0.7,
            validated=True,
            validation_result="Passed all tests",
        )
        assert hypothesis.id == "h1"
        assert hypothesis.description == "Test hypothesis"
        assert hypothesis.approach == "Use TDD approach"
        assert len(hypothesis.pros) == 2
        assert len(hypothesis.cons) == 1
        assert hypothesis.confidence == 0.7
        assert hypothesis.validated is True
        assert hypothesis.validation_result == "Passed all tests"

    def test_defaults(self):
        """Test default values."""
        hypothesis = Hypothesis(
            id="h2",
            description="desc",
            approach="approach",
        )
        assert hypothesis.pros == []
        assert hypothesis.cons == []
        assert hypothesis.confidence == 0.5
        assert hypothesis.validated is False
        assert hypothesis.validation_result is None


class TestProblemAnalysis:
    """Tests for ProblemAnalysis dataclass."""

    def test_creation(self):
        """Test ProblemAnalysis creation."""
        analysis = ProblemAnalysis(
            original_task="Build a feature",
            goals=["goal1", "goal2"],
            constraints=["constraint1"],
            assumptions=["assumption1"],
            risks=["risk1"],
            inputs=["input1"],
            outputs=["output1"],
            edge_cases=["edge1"],
            dependencies=["dep1"],
            success_criteria=["criterion1"],
        )
        assert analysis.original_task == "Build a feature"
        assert len(analysis.goals) == 2
        assert len(analysis.constraints) == 1

    def test_defaults(self):
        """Test default values."""
        analysis = ProblemAnalysis(original_task="task")
        assert analysis.goals == []
        assert analysis.constraints == []
        assert analysis.assumptions == []
        assert analysis.risks == []


class TestSubTask:
    """Tests for SubTask dataclass."""

    def test_creation(self):
        """Test SubTask creation."""
        subtask = SubTask(
            id="st1",
            description="Implement feature",
            type="implementation",
            priority=1,
            complexity=3,
            dependencies=["st0"],
            files_involved=["file1.py"],
            verification_method="run tests",
            status="in_progress",
            result="Partial completion",
        )
        assert subtask.id == "st1"
        assert subtask.description == "Implement feature"
        assert subtask.type == "implementation"
        assert subtask.priority == 1
        assert subtask.complexity == 3
        assert subtask.status == "in_progress"

    def test_defaults(self):
        """Test default values."""
        subtask = SubTask(
            id="st2",
            description="desc",
            type="research",
            priority=2,
            complexity=2,
        )
        assert subtask.dependencies == []
        assert subtask.files_involved == []
        assert subtask.verification_method == ""
        assert subtask.status == "pending"
        assert subtask.result is None


class TestReasoningContext:
    """Tests for ReasoningContext dataclass."""

    def test_creation(self):
        """Test ReasoningContext creation."""
        context = ReasoningContext(
            task="Complete the task",
            analysis=ProblemAnalysis(original_task="task"),
            subtasks=[SubTask(id="st1", description="d", type="t", priority=1, complexity=1)],
            hypotheses=[Hypothesis(id="h1", description="d", approach="a")],
            reasoning_chain=[
                ReasoningStep(phase=ReasoningPhase.UNDERSTAND, thought="t")
            ],
            selected_approach=Hypothesis(id="h1", description="d", approach="a"),
            files_read={"file1.py"},
            files_modified=["file2.py"],
            errors_encountered=["error1"],
            learnings=["learning1"],
        )
        assert context.task == "Complete the task"
        assert context.analysis is not None
        assert len(context.subtasks) == 1
        assert len(context.hypotheses) == 1
        assert len(context.reasoning_chain) == 1

    def test_defaults(self):
        """Test default values."""
        context = ReasoningContext(task="task")
        assert context.analysis is None
        assert context.subtasks == []
        assert context.hypotheses == []
        assert context.reasoning_chain == []
        assert context.selected_approach is None
        assert context.files_read == set()
        assert context.files_modified == []
        assert context.errors_encountered == []
        assert context.learnings == []


# ═══════════════════════════════════════════════════════════════════════════════
# CHAIN OF THOUGHT REASONER TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestChainOfThoughtReasoner:
    """Tests for ChainOfThoughtReasoner class."""

    @pytest.fixture
    def mock_send_fn(self):
        """Create mock send function."""
        return MagicMock(return_value="OBJECTIVE: Test objective\nREQUIREMENTS:\n- req1\nSUCCESS_CRITERIA:\n- criterion1")

    @pytest.fixture
    def reasoner(self, mock_send_fn, tmp_path):
        """Create reasoner instance."""
        return ChainOfThoughtReasoner(send_fn=mock_send_fn, cwd=tmp_path)

    def test_init(self, reasoner, tmp_path):
        """Test initialization."""
        assert reasoner.send_fn is not None
        assert reasoner.cwd == tmp_path
        assert reasoner.context is None
        assert reasoner._reasoning_cache == {}

    def test_phase_prompts_exist(self):
        """Test all phase prompts are defined."""
        for phase in ReasoningPhase:
            assert phase in ChainOfThoughtReasoner.PHASE_PROMPTS

    def test_reason_quick(self, reasoner):
        """Test quick reasoning mode."""
        context = reasoner.reason("Test task", depth="quick")
        assert context.task == "Test task"
        # Quick mode has 3 phases
        assert len(context.reasoning_chain) == 3

    def test_reason_full(self, reasoner):
        """Test full reasoning mode."""
        context = reasoner.reason("Test task", depth="full")
        assert context.task == "Test task"
        # Full mode has 6 phases
        assert len(context.reasoning_chain) == 6

    def test_execute_phase_no_response(self, tmp_path):
        """Test phase execution with no response."""
        send_fn = MagicMock(return_value=None)
        reasoner = ChainOfThoughtReasoner(send_fn=send_fn, cwd=tmp_path)
        reasoner.context = ReasoningContext(task="test")

        step = reasoner._execute_phase(ReasoningPhase.UNDERSTAND)
        assert step.confidence == 0.0
        assert "no response" in step.thought.lower()

    def test_build_phase_prompt(self, reasoner):
        """Test building phase prompt."""
        reasoner.context = ReasoningContext(task="Test task")
        prompt = reasoner._build_phase_prompt(ReasoningPhase.UNDERSTAND)
        assert "Test task" in prompt

    def test_parse_phase_response_understand(self, reasoner):
        """Test parsing UNDERSTAND phase response."""
        response = """
        OBJECTIVE: Build a REST API
        REQUIREMENTS:
        - Handle HTTP requests
        - Return JSON responses
        SUCCESS_CRITERIA:
        - All endpoints working
        - Tests pass
        """
        parsed = reasoner._parse_phase_response(ReasoningPhase.UNDERSTAND, response)
        assert parsed["objective"] == "Build a REST API"
        assert len(parsed["requirements"]) > 0
        assert len(parsed["success_criteria"]) > 0
        assert parsed["confidence"] == 0.7

    def test_parse_phase_response_decompose(self, reasoner):
        """Test parsing DECOMPOSE phase response."""
        response = """
        SUBTASK_1:
          action: Research existing code
          type: research
        SUBTASK_2:
          action: Implement feature
          type: implementation
        """
        parsed = reasoner._parse_phase_response(ReasoningPhase.DECOMPOSE, response)
        assert len(parsed["subtasks"]) == 2
        assert parsed["subtasks"][0]["type"] == "research"
        assert parsed["confidence"] == 0.8

    def test_parse_phase_response_analyze(self, reasoner):
        """Test parsing ANALYZE phase response."""
        # Use double newlines to separate sections properly
        response = """CONSTRAINTS:
- Memory limit
- Time limit

ASSUMPTIONS:
- Python 3.10+

RISKS:
- Breaking changes

EDGE_CASES:
- Empty input
"""
        parsed = reasoner._parse_phase_response(ReasoningPhase.ANALYZE, response)
        assert len(parsed["constraints"]) == 2
        assert len(parsed["assumptions"]) == 1
        assert len(parsed["risks"]) == 1
        assert len(parsed["edge_cases"]) == 1

    def test_parse_phase_response_hypothesize(self, reasoner):
        """Test parsing HYPOTHESIZE phase response."""
        response = """
        HYPOTHESIS_1:
          approach: Use dependency injection
          pros:
            - Testable
        HYPOTHESIS_2:
          approach: Use singleton pattern
        """
        parsed = reasoner._parse_phase_response(ReasoningPhase.HYPOTHESIZE, response)
        assert len(parsed["hypotheses"]) == 2
        assert parsed["confidence"] == 0.7

    def test_parse_phase_response_evaluate(self, reasoner):
        """Test parsing EVALUATE phase response."""
        response = """
        EVALUATION:
          hypothesis_1: 8
          hypothesis_2: 6
        SELECTED: hypothesis_1
        REASONING: Better testability
        """
        parsed = reasoner._parse_phase_response(ReasoningPhase.EVALUATE, response)
        assert parsed["selected"] == "hypothesis_1"
        assert parsed["reasoning"] == "Better testability"
        assert parsed["confidence"] == 0.8

    def test_parse_phase_response_synthesize(self, reasoner):
        """Test parsing SYNTHESIZE phase response."""
        response = """
        IMPLEMENTATION_PLAN:
          step_1:
            action: Write tests
        """
        parsed = reasoner._parse_phase_response(ReasoningPhase.SYNTHESIZE, response)
        assert parsed["has_plan"] is True
        assert parsed["confidence"] == 0.8

    def test_parse_phase_response_validate(self, reasoner):
        """Test parsing VALIDATE phase response."""
        response = """
        VALIDATION_RESULTS:
          syntax_check: pass
          tests_pass: pass
          edge_cases: fail
          security: pass
        """
        parsed = reasoner._parse_phase_response(ReasoningPhase.VALIDATE, response)
        results = parsed["validation_results"]
        assert results["syntax_check"] is True
        assert results["tests_pass"] is True
        assert results["edge_cases"] is False
        assert results["security"] is True

    def test_update_context_understand(self, reasoner):
        """Test updating context from UNDERSTAND phase."""
        reasoner.context = ReasoningContext(task="test")
        parsed = {"success_criteria": ["criterion1", "criterion2"]}
        reasoner._update_context(ReasoningPhase.UNDERSTAND, parsed)
        assert reasoner.context.analysis is not None
        assert len(reasoner.context.analysis.success_criteria) == 2

    def test_update_context_decompose(self, reasoner):
        """Test updating context from DECOMPOSE phase."""
        reasoner.context = ReasoningContext(task="test")
        parsed = {
            "subtasks": [
                {"id": "st1", "action": "Do thing", "type": "implementation"},
            ]
        }
        reasoner._update_context(ReasoningPhase.DECOMPOSE, parsed)
        assert len(reasoner.context.subtasks) == 1
        assert reasoner.context.subtasks[0].id == "st1"

    def test_update_context_analyze(self, reasoner):
        """Test updating context from ANALYZE phase."""
        reasoner.context = ReasoningContext(task="test")
        parsed = {
            "constraints": ["c1"],
            "assumptions": ["a1"],
            "risks": ["r1"],
            "edge_cases": ["e1"],
        }
        reasoner._update_context(ReasoningPhase.ANALYZE, parsed)
        assert reasoner.context.analysis is not None
        assert reasoner.context.analysis.constraints == ["c1"]

    def test_update_context_hypothesize(self, reasoner):
        """Test updating context from HYPOTHESIZE phase."""
        reasoner.context = ReasoningContext(task="test")
        parsed = {
            "hypotheses": [
                {"id": "h1", "approach": "Test approach"},
            ]
        }
        reasoner._update_context(ReasoningPhase.HYPOTHESIZE, parsed)
        assert len(reasoner.context.hypotheses) == 1

    def test_update_context_evaluate(self, reasoner):
        """Test updating context from EVALUATE phase."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.hypotheses = [
            Hypothesis(id="h1", description="d", approach="a"),
            Hypothesis(id="h2", description="d2", approach="a2"),
        ]
        parsed = {"selected": "h1"}
        reasoner._update_context(ReasoningPhase.EVALUATE, parsed)
        assert reasoner.context.selected_approach is not None
        assert reasoner.context.selected_approach.id == "h1"

    def test_gather_more_context(self, reasoner):
        """Test gathering more context on low confidence."""
        reasoner.context = ReasoningContext(task="test")
        reasoner._gather_more_context(ReasoningPhase.UNDERSTAND)
        # Should have made a call to send_fn for clarification
        assert reasoner.send_fn.call_count >= 1

    def test_get_objective(self, reasoner):
        """Test getting objective from context."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.reasoning_chain = [
            ReasoningStep(
                phase=ReasoningPhase.UNDERSTAND,
                thought="OBJECTIVE: Build API\nMore text",
            )
        ]
        objective = reasoner._get_objective()
        assert objective == "Build API"

    def test_get_objective_fallback(self, reasoner):
        """Test objective fallback to task."""
        reasoner.context = ReasoningContext(task="fallback task")
        objective = reasoner._get_objective()
        assert objective == "fallback task"

    def test_format_subtasks(self, reasoner):
        """Test formatting subtasks."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.subtasks = [
            SubTask(id="st1", description="Do thing", type="impl", priority=1, complexity=2),
        ]
        formatted = reasoner._format_subtasks()
        assert "st1" in formatted
        assert "Do thing" in formatted

    def test_format_subtasks_none(self, reasoner):
        """Test formatting when no subtasks."""
        reasoner.context = ReasoningContext(task="test")
        formatted = reasoner._format_subtasks()
        assert "None" in formatted

    def test_format_analysis(self, reasoner):
        """Test formatting analysis."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.analysis = ProblemAnalysis(
            original_task="test",
            constraints=["c1", "c2"],
            assumptions=["a1"],
            risks=["r1"],
        )
        formatted = reasoner._format_analysis()
        assert "c1" in formatted
        assert "a1" in formatted

    def test_format_hypotheses(self, reasoner):
        """Test formatting hypotheses."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.hypotheses = [
            Hypothesis(id="h1", description="d", approach="Use dependency injection"),
        ]
        formatted = reasoner._format_hypotheses()
        assert "h1" in formatted
        assert "dependency injection" in formatted

    def test_format_success_criteria(self, reasoner):
        """Test formatting success criteria."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.analysis = ProblemAnalysis(
            original_task="test",
            success_criteria=["Tests pass", "No errors"],
        )
        formatted = reasoner._format_success_criteria()
        assert "Tests pass" in formatted

    def test_format_constraints(self, reasoner):
        """Test formatting constraints."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.analysis = ProblemAnalysis(
            original_task="test",
            constraints=["Memory limit", "Time limit"],
        )
        formatted = reasoner._format_constraints()
        assert "Memory limit" in formatted

    def test_format_selected_approach(self, reasoner):
        """Test formatting selected approach."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.selected_approach = Hypothesis(
            id="h1", description="d", approach="TDD approach"
        )
        formatted = reasoner._format_selected_approach()
        assert "TDD approach" in formatted

    def test_format_implementation(self, reasoner):
        """Test formatting implementation."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.files_modified = ["file1.py", "file2.py"]
        formatted = reasoner._format_implementation()
        assert "file1.py" in formatted

    def test_format_outcome(self, reasoner):
        """Test formatting outcome."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.subtasks = [
            SubTask(id="st1", description="d", type="t", priority=1, complexity=1, status="completed"),
            SubTask(id="st2", description="d", type="t", priority=1, complexity=1, status="pending"),
        ]
        formatted = reasoner._format_outcome()
        assert "1/2" in formatted

    def test_format_errors(self, reasoner):
        """Test formatting errors."""
        reasoner.context = ReasoningContext(task="test")
        reasoner.context.errors_encountered = ["Error 1", "Error 2"]
        formatted = reasoner._format_errors()
        assert "Error 1" in formatted

    def test_get_reasoning_summary(self, reasoner):
        """Test getting reasoning summary."""
        reasoner.context = ReasoningContext(task="Build feature")
        reasoner.context.analysis = ProblemAnalysis(
            original_task="task",
            goals=["goal1"],
            constraints=["constraint1"],
            risks=["risk1"],
        )
        reasoner.context.selected_approach = Hypothesis(
            id="h1", description="d", approach="Use TDD"
        )
        reasoner.context.subtasks = [
            SubTask(id="st1", description="Step 1", type="t", priority=1, complexity=1, status="completed"),
        ]
        reasoner.context.reasoning_chain = [
            ReasoningStep(phase=ReasoningPhase.UNDERSTAND, thought="t", confidence=0.8),
        ]

        summary = reasoner.get_reasoning_summary()
        assert "Build feature" in summary
        assert "goal1" in summary
        assert "Use TDD" in summary
        assert "✅" in summary  # Completed status icon
        assert "80.0%" in summary  # Confidence


# ═══════════════════════════════════════════════════════════════════════════════
# SELF REFLECTION ENGINE TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestSelfReflectionEngine:
    """Tests for SelfReflectionEngine class."""

    @pytest.fixture
    def mock_send_fn(self):
        """Create mock send function."""
        return MagicMock(return_value="""
        ISSUES:
        - Missing edge case handling
        - No documentation
        FIXES_NEEDED:
        - Add error handling
        CONFIDENCE: 0.75
        """)

    @pytest.fixture
    def engine(self, mock_send_fn):
        """Create engine instance."""
        return SelfReflectionEngine(send_fn=mock_send_fn)

    def test_init(self, engine):
        """Test initialization."""
        assert engine.send_fn is not None
        assert engine.reflection_history == []

    def test_reflect(self, engine):
        """Test reflection."""
        result = engine.reflect(
            task="Build feature",
            code_files=["file1.py"],
            test_files=["test_file1.py"],
            errors=["Error 1"],
        )
        assert result["success"] is True
        assert len(result["issues"]) > 0
        assert len(result["fixes_needed"]) > 0
        assert result["confidence"] == 0.75

    def test_reflect_no_response(self):
        """Test reflection with no response."""
        send_fn = MagicMock(return_value=None)
        engine = SelfReflectionEngine(send_fn=send_fn)
        result = engine.reflect("task", [], [], [])
        assert result["success"] is False
        assert result["confidence"] == 0.0

    def test_reflect_empty_files(self, engine):
        """Test reflection with empty file lists."""
        result = engine.reflect("task", [], [], [])
        assert result["success"] is True

    def test_reflect_filters_template_issues(self, mock_send_fn):
        """Test that template placeholders are filtered out."""
        mock_send_fn.return_value = """
        ISSUES:
        - [issue 1]
        - Real issue
        FIXES_NEEDED:
        - [fix 1]
        - Real fix
        CONFIDENCE: 0.8
        """
        engine = SelfReflectionEngine(send_fn=mock_send_fn)
        result = engine.reflect("task", [], [], [])
        assert "[issue 1]" not in result["issues"]
        assert "Real issue" in result["issues"]
        assert "[fix 1]" not in result["fixes_needed"]
        assert "Real fix" in result["fixes_needed"]

    def test_reflect_history(self, engine):
        """Test reflection history is updated."""
        engine.reflect("task1", [], [], [])
        engine.reflect("task2", [], [], [])
        assert len(engine.reflection_history) == 2
        assert engine.reflection_history[0]["task"] == "task1"
        assert engine.reflection_history[1]["task"] == "task2"

    def test_needs_improvement_low_confidence(self, engine):
        """Test needs_improvement with low confidence."""
        result = {"confidence": 0.5, "issues": [], "fixes_needed": []}
        assert engine.needs_improvement(result) is True

    def test_needs_improvement_has_issues(self, engine):
        """Test needs_improvement with issues."""
        result = {"confidence": 0.9, "issues": ["issue1"], "fixes_needed": []}
        assert engine.needs_improvement(result) is True

    def test_needs_improvement_has_fixes(self, engine):
        """Test needs_improvement with fixes needed."""
        result = {"confidence": 0.9, "issues": [], "fixes_needed": ["fix1"]}
        assert engine.needs_improvement(result) is True

    def test_needs_improvement_all_good(self, engine):
        """Test needs_improvement when all is good."""
        result = {"confidence": 0.9, "issues": [], "fixes_needed": []}
        assert engine.needs_improvement(result) is False


# ═══════════════════════════════════════════════════════════════════════════════
# MULTI PERSPECTIVE ANALYZER TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestMultiPerspectiveAnalyzer:
    """Tests for MultiPerspectiveAnalyzer class."""

    @pytest.fixture
    def mock_send_fn(self):
        """Create mock send function."""
        return MagicMock(return_value="""
        - Concern 1
        - Concern 2
        - Concern 3
        """)

    @pytest.fixture
    def analyzer(self, mock_send_fn):
        """Create analyzer instance."""
        return MultiPerspectiveAnalyzer(send_fn=mock_send_fn)

    def test_perspectives_exist(self):
        """Test all perspectives are defined."""
        assert len(MultiPerspectiveAnalyzer.PERSPECTIVES) > 0
        perspective_names = [p["name"] for p in MultiPerspectiveAnalyzer.PERSPECTIVES]
        assert "User" in perspective_names
        assert "Security" in perspective_names
        assert "Performance" in perspective_names
        assert "Maintainer" in perspective_names
        assert "Tester" in perspective_names

    def test_init(self, analyzer):
        """Test initialization."""
        assert analyzer.send_fn is not None

    def test_analyze(self, analyzer):
        """Test multi-perspective analysis."""
        results = analyzer.analyze("def foo(): pass", context="Test context")
        # Should have results for each perspective
        assert len(results) == len(MultiPerspectiveAnalyzer.PERSPECTIVES)
        for perspective in MultiPerspectiveAnalyzer.PERSPECTIVES:
            assert perspective["name"] in results

    def test_analyze_extracts_concerns(self, analyzer):
        """Test that concerns are extracted correctly."""
        results = analyzer.analyze("code")
        for perspective, concerns in results.items():
            assert isinstance(concerns, list)
            assert len(concerns) > 0

    def test_get_summary(self, analyzer):
        """Test summary generation."""
        analysis = {
            "User": ["Frustrating UX", "Slow response"],
            "Security": ["SQL injection risk"],
            "Performance": [],  # Empty concerns
        }
        summary = analyzer.get_summary(analysis)
        assert "User" in summary
        assert "Frustrating UX" in summary
        assert "Security" in summary
        # Should limit to top 3 per perspective
        assert "Multi-Perspective Analysis" in summary

    def test_get_summary_empty(self, analyzer):
        """Test summary with no analysis."""
        summary = analyzer.get_summary({})
        assert "No analysis available" in summary

    def test_get_summary_limits_concerns(self, analyzer):
        """Test summary limits concerns to 3 per perspective."""
        analysis = {
            "User": ["concern1", "concern2", "concern3", "concern4", "concern5"],
        }
        summary = analyzer.get_summary(analysis)
        # Should only show first 3
        assert "concern1" in summary
        assert "concern2" in summary
        assert "concern3" in summary
        assert "concern4" not in summary


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR DIAGNOSIS TESTS
# ═══════════════════════════════════════════════════════════════════════════════


class TestErrorDiagnosis:
    """Tests for ErrorDiagnosis class."""

    @pytest.fixture
    def diagnosis(self):
        """Create diagnosis instance."""
        return ErrorDiagnosis()

    def test_error_patterns_exist(self):
        """Test error patterns are defined."""
        assert len(ErrorDiagnosis.ERROR_PATTERNS) > 0
        expected_types = [
            "import_error", "attribute_error", "type_error",
            "syntax_error", "name_error", "assertion_error",
            "key_error", "file_not_found"
        ]
        for error_type in expected_types:
            assert error_type in ErrorDiagnosis.ERROR_PATTERNS

    def test_init(self, diagnosis):
        """Test initialization."""
        assert diagnosis.diagnosis_cache == {}

    def test_diagnose_import_error(self, diagnosis):
        """Test diagnosing ImportError."""
        result = diagnosis.diagnose("ImportError: No module named 'foo'")
        assert result["error_type"] == "import_error"
        assert result["confidence"] == 0.8
        assert len(result["suggested_fixes"]) > 0
        assert result["missing_module"] == "foo"

    def test_diagnose_attribute_error(self, diagnosis):
        """Test diagnosing AttributeError."""
        result = diagnosis.diagnose("AttributeError: 'str' object has no attribute 'foo'")
        assert result["error_type"] == "attribute_error"
        assert result["confidence"] == 0.8

    def test_diagnose_type_error(self, diagnosis):
        """Test diagnosing TypeError."""
        result = diagnosis.diagnose("TypeError: expected str, got int")
        assert result["error_type"] == "type_error"
        assert result["confidence"] == 0.8

    def test_diagnose_syntax_error(self, diagnosis):
        """Test diagnosing SyntaxError."""
        result = diagnosis.diagnose("SyntaxError: invalid syntax at line 10")
        assert result["error_type"] == "syntax_error"
        assert result["confidence"] == 0.8
        assert result["line_number"] == 10

    def test_diagnose_name_error(self, diagnosis):
        """Test diagnosing NameError."""
        result = diagnosis.diagnose("NameError: name 'undefined_var' is not defined")
        assert result["error_type"] == "name_error"
        assert result["undefined_name"] == "undefined_var"

    def test_diagnose_assertion_error(self, diagnosis):
        """Test diagnosing AssertionError."""
        result = diagnosis.diagnose("AssertionError: assert x == y failed")
        assert result["error_type"] == "assertion_error"

    def test_diagnose_key_error(self, diagnosis):
        """Test diagnosing KeyError."""
        result = diagnosis.diagnose("KeyError: 'missing_key'")
        assert result["error_type"] == "key_error"

    def test_diagnose_file_not_found(self, diagnosis):
        """Test diagnosing FileNotFoundError."""
        result = diagnosis.diagnose("FileNotFoundError: No such file '/path/to/file'")
        assert result["error_type"] == "file_not_found"

    def test_diagnose_unknown_error(self, diagnosis):
        """Test diagnosing unknown error."""
        result = diagnosis.diagnose("SomeRandomError: mysterious failure")
        assert result["error_type"] == "unknown"
        assert result["confidence"] == 0.3

    def test_diagnose_extracts_line_number(self, diagnosis):
        """Test line number extraction."""
        result = diagnosis.diagnose("Error at line 42")
        assert result["line_number"] == 42

    def test_diagnose_extracts_file(self, diagnosis):
        """Test file extraction."""
        result = diagnosis.diagnose('File "/path/to/module.py", line 10')
        assert result["file"] == "/path/to/module.py"

    def test_diagnose_caching(self, diagnosis):
        """Test diagnosis caching."""
        error = "ImportError: No module named 'test'"
        result1 = diagnosis.diagnose(error)
        result2 = diagnosis.diagnose(error)
        # Should return cached result
        assert result1 == result2
        assert len(diagnosis.diagnosis_cache) == 1

    def test_format_diagnosis(self, diagnosis):
        """Test formatting diagnosis."""
        diag = {
            "error_type": "import_error",
            "diagnosis": "Missing import",
            "line_number": 10,
            "file": "module.py",
            "missing_module": "foo",
            "suggested_fixes": ["Check import path", "Install module"],
            "confidence": 0.8,
        }
        formatted = diagnosis.format_diagnosis(diag)
        assert "import_error" in formatted
        assert "Missing import" in formatted
        assert "Line:" in formatted
        assert "10" in formatted
        assert "module.py" in formatted
        assert "foo" in formatted
        assert "Check import path" in formatted
        assert "80%" in formatted

    def test_format_diagnosis_minimal(self, diagnosis):
        """Test formatting minimal diagnosis."""
        diag = {
            "error_type": "unknown",
            "diagnosis": "Unknown error",
            "suggested_fixes": ["Review error"],
            "confidence": 0.3,
        }
        formatted = diagnosis.format_diagnosis(diag)
        assert "unknown" in formatted
        assert "30%" in formatted


# ═══════════════════════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════════════════════


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_task_reasoning(self, tmp_path):
        """Test reasoning with empty task."""
        send_fn = MagicMock(return_value="OBJECTIVE: None\n")
        reasoner = ChainOfThoughtReasoner(send_fn=send_fn, cwd=tmp_path)
        context = reasoner.reason("", depth="quick")
        assert context.task == ""

    def test_reasoning_with_unicode(self, tmp_path):
        """Test reasoning with unicode characters."""
        send_fn = MagicMock(return_value="OBJECTIVE: 测试\n")
        reasoner = ChainOfThoughtReasoner(send_fn=send_fn, cwd=tmp_path)
        context = reasoner.reason("实现功能", depth="quick")
        assert context.task == "实现功能"

    def test_diagnosis_with_multiline_error(self):
        """Test diagnosis with multiline error."""
        diagnosis = ErrorDiagnosis()
        error = """
        Traceback (most recent call last):
          File "test.py", line 10, in <module>
            foo()
        NameError: name 'bar' is not defined
        """
        result = diagnosis.diagnose(error)
        assert result["error_type"] == "name_error"
        assert result["undefined_name"] == "bar"

    def test_reflection_with_special_characters(self):
        """Test reflection with special characters in task."""
        send_fn = MagicMock(return_value="CONFIDENCE: 0.9\n")
        engine = SelfReflectionEngine(send_fn=send_fn)
        result = engine.reflect("Task with $pecial @#% characters", [], [], [])
        assert result["success"] is True
