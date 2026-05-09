"""Comprehensive tests for sage/core/reasoning_engine.py - 100% coverage target."""

import pytest

from sage.core.reasoning_engine import (
    ActionPlan,
    ActionPlanner,
    AmbiguityResolution,
    AmbiguityResolver,
    Assumption,
    AssumptionTracker,
    CausalAnalysis,
    CausalPrediction,
    CausalReasoner,
    ChainOfThought,
    ChainOfThoughtReasoner,
    CodeAnalysisResult,
    Conclusion,
    ConclusionDrawer,
    CriticalAnalysis,
    CriticalThinker,
    Decision,
    DecisionMaker,
    DeductiveConclusion,
    DeductiveReasoner,
    EvidenceCollection,
    EvidenceCollector,
    EvidenceEvaluation,
    EvidenceItem,
    Experiment,
    ExperimentDesigner,
    FirstPrinciplesAnalysis,
    FirstPrinciplesThinker,
    FullAnalysisResult,
    Hypothesis,
    HypothesisGenerator,
    HypothesisRanker,
    HypothesisTester,
    InductiveGeneralization,
    InductiveReasoner,
    IntegratedSolution,
    MetaAnalysis,
    MetaReasoner,
    PlanStep,
    ProblemDecomposer,
    ReasoningEngine,
    ReasoningVerifier,
    SolutionComposer,
    SubProblem,
    TestPlan,
    ThinkingResult,
    UncertaintyHandler,
    UncertaintyResult,
    Verification,
)


# =============================================================================
# Data Class Tests
# =============================================================================


class TestThinkingResult:
    """Tests for ThinkingResult dataclass."""

    def test_defaults(self):
        """Test default values."""
        result = ThinkingResult()
        assert result.thinking_steps == []
        assert result.conclusion is None
        assert result.depth == 1
        assert result.confidence == 0.0

    def test_with_values(self):
        """Test with provided values."""
        result = ThinkingResult(
            thinking_steps=["Step 1", "Step 2"],
            conclusion="Done",
            depth=3,
            confidence=0.85,
        )
        assert len(result.thinking_steps) == 2
        assert result.conclusion == "Done"
        assert result.depth == 3
        assert result.confidence == 0.85


class TestFirstPrinciplesAnalysis:
    """Tests for FirstPrinciplesAnalysis dataclass."""

    def test_defaults(self):
        """Test default values."""
        analysis = FirstPrinciplesAnalysis()
        assert analysis.fundamental_truths == []
        assert analysis.assumptions_questioned == []
        assert analysis.rebuilt_solution is None


class TestCriticalAnalysis:
    """Tests for CriticalAnalysis dataclass."""

    def test_defaults(self):
        """Test default values."""
        analysis = CriticalAnalysis()
        assert analysis.potential_flaws == []
        assert analysis.logical_validity is None
        assert analysis.reasoning_gaps == []


class TestEvidenceEvaluation:
    """Tests for EvidenceEvaluation dataclass."""

    def test_defaults(self):
        """Test default values."""
        evaluation = EvidenceEvaluation()
        assert evaluation.evidence_strength == 0.0
        assert evaluation.supporting_points == []
        assert evaluation.weaknesses == []


class TestDeductiveConclusion:
    """Tests for DeductiveConclusion dataclass."""

    def test_defaults(self):
        """Test default values."""
        conclusion = DeductiveConclusion(result="Test")
        assert conclusion.result == "Test"
        assert conclusion.valid is True
        assert conclusion.certain is True
        assert conclusion.reasoning == ""


class TestInductiveGeneralization:
    """Tests for InductiveGeneralization dataclass."""

    def test_defaults(self):
        """Test default values."""
        gen = InductiveGeneralization(pattern="Test", confidence=0.8)
        assert gen.pattern == "Test"
        assert gen.confidence == 0.8
        assert gen.supporting_examples == []


class TestCausalAnalysis:
    """Tests for CausalAnalysis dataclass."""

    def test_defaults(self):
        """Test default values."""
        analysis = CausalAnalysis()
        assert analysis.likely_cause is None
        assert analysis.confidence == 0.0
        assert analysis.alternative_causes == []


class TestCausalPrediction:
    """Tests for CausalPrediction dataclass."""

    def test_defaults(self):
        """Test default values."""
        pred = CausalPrediction()
        assert pred.possible_effects == []
        assert pred.confidence == 0.0


class TestMetaAnalysis:
    """Tests for MetaAnalysis dataclass."""

    def test_defaults(self):
        """Test default values."""
        analysis = MetaAnalysis()
        assert analysis.weak_points == []
        assert analysis.improvement_suggestions == []


class TestChainOfThought:
    """Tests for ChainOfThought dataclass."""

    def test_defaults(self):
        """Test default values."""
        chain = ChainOfThought()
        assert chain.steps == []
        assert chain.final_answer is None


class TestVerification:
    """Tests for Verification dataclass."""

    def test_defaults(self):
        """Test default values."""
        verification = Verification()
        assert verification.is_valid is True
        assert verification.confidence == 1.0
        assert verification.issues == []


class TestUncertaintyResult:
    """Tests for UncertaintyResult dataclass."""

    def test_defaults(self):
        """Test default values."""
        result = UncertaintyResult()
        assert result.confidence == 0.0
        assert result.confidence_interval is None


class TestAmbiguityResolution:
    """Tests for AmbiguityResolution dataclass."""

    def test_defaults(self):
        """Test default values."""
        resolution = AmbiguityResolution()
        assert resolution.clarified_meaning is None
        assert resolution.assumptions_made is None


class TestAssumption:
    """Tests for Assumption dataclass."""

    def test_defaults(self):
        """Test default values."""
        assumption = Assumption(text="Test assumption")
        assert assumption.text == "Test assumption"
        assert assumption.category == "general"
        assert assumption.confidence == 0.5


class TestDecision:
    """Tests for Decision dataclass."""

    def test_defaults(self):
        """Test default values."""
        decision = Decision()
        assert decision.chosen is None
        assert decision.reasoning is None
        assert decision.alternatives_considered == []


class TestHypothesis:
    """Tests for Hypothesis dataclass."""

    def test_defaults(self):
        """Test default values."""
        hypothesis = Hypothesis(description="Test hypothesis")
        assert hypothesis.description == "Test hypothesis"
        assert hypothesis.confidence == 0.5
        assert hypothesis.evidence == []
        assert hypothesis.type == "general"


class TestTestPlan:
    """Tests for TestPlan dataclass."""

    def test_defaults(self):
        """Test default values."""
        plan = TestPlan()
        assert plan.steps == []
        assert plan.expected_result is None
        assert plan.success_criteria is None


class TestExperiment:
    """Tests for Experiment dataclass."""

    def test_defaults(self):
        """Test default values."""
        experiment = Experiment()
        assert experiment.control_group is None
        assert experiment.test_group is None
        assert experiment.success_criteria is None
        assert experiment.variables == []


class TestEvidenceItem:
    """Tests for EvidenceItem dataclass."""

    def test_defaults(self):
        """Test default values."""
        item = EvidenceItem(content="Test", source="Source")
        assert item.content == "Test"
        assert item.source == "Source"
        assert item.strength == 0.5


class TestEvidenceCollection:
    """Tests for EvidenceCollection dataclass."""

    def test_defaults(self):
        """Test default values."""
        collection = EvidenceCollection()
        assert collection.items == []


class TestConclusion:
    """Tests for Conclusion dataclass."""

    def test_defaults(self):
        """Test default values."""
        conclusion = Conclusion(statement="Test", confidence=0.9)
        assert conclusion.statement == "Test"
        assert conclusion.confidence == 0.9
        assert conclusion.supporting_evidence == []


class TestPlanStep:
    """Tests for PlanStep dataclass."""

    def test_defaults(self):
        """Test default values."""
        step = PlanStep(action="Do something")
        assert step.action == "Do something"
        assert step.dependencies == []
        assert step.description == ""


class TestActionPlan:
    """Tests for ActionPlan dataclass."""

    def test_defaults(self):
        """Test default values."""
        plan = ActionPlan()
        assert plan.steps == []
        assert plan.approach == "default"
        assert plan.estimated_complexity == "medium"


class TestSubProblem:
    """Tests for SubProblem dataclass."""

    def test_defaults(self):
        """Test default values."""
        sub = SubProblem(name="Test")
        assert sub.name == "Test"
        assert sub.description == ""
        assert sub.parent == ""
        assert sub.complexity == "medium"


class TestIntegratedSolution:
    """Tests for IntegratedSolution dataclass."""

    def test_defaults(self):
        """Test default values."""
        solution = IntegratedSolution(integrated_solution="Test")
        assert solution.integrated_solution == "Test"
        assert solution.integration_points == []


class TestFullAnalysisResult:
    """Tests for FullAnalysisResult dataclass."""

    def test_defaults(self):
        """Test default values."""
        result = FullAnalysisResult()
        assert result.hypotheses is None
        assert result.reasoning_chain is None
        assert result.conclusion is None
        assert result.confidence == 0.0


class TestCodeAnalysisResult:
    """Tests for CodeAnalysisResult dataclass."""

    def test_defaults(self):
        """Test default values."""
        result = CodeAnalysisResult()
        assert result.issues == []
        assert result.suggestions is None
        assert result.reasoning == ""


# =============================================================================
# ReasoningEngine Tests
# =============================================================================


class TestReasoningEngine:
    """Tests for ReasoningEngine class."""

    def test_init(self):
        """Test initialization."""
        engine = ReasoningEngine()
        assert engine.thinking_depth == 1
        assert engine.deep_thinking_enabled is False
        assert engine._chain_reasoner is not None
        assert engine._hypothesis_generator is not None

    def test_enable_deep_thinking(self):
        """Test enabling deep thinking."""
        engine = ReasoningEngine()
        engine.enable_deep_thinking(depth=5)
        assert engine.thinking_depth == 5
        assert engine.deep_thinking_enabled is True

    def test_think_shallow(self):
        """Test shallow thinking."""
        engine = ReasoningEngine()
        result = engine.think("How to fix this bug?", depth=1)

        assert result.depth == 1
        assert len(result.thinking_steps) <= 3
        assert result.conclusion is not None
        assert 0 < result.confidence <= 1

    def test_think_deep(self):
        """Test deep thinking."""
        engine = ReasoningEngine()
        result = engine.think("Complex architecture problem", depth=3)

        assert result.depth == 3
        assert len(result.thinking_steps) > 3
        assert result.conclusion is not None

    def test_think_uses_default_depth(self):
        """Test thinking uses default depth."""
        engine = ReasoningEngine()
        engine.enable_deep_thinking(depth=4)
        result = engine.think("Test problem")

        assert result.depth == 4

    def test_think_confidence_calculation(self):
        """Test confidence is calculated correctly."""
        engine = ReasoningEngine()
        result = engine.think("Problem", depth=5)
        assert result.confidence <= 0.95

    def test_evaluate_thinking_quality(self):
        """Test evaluating thinking quality."""
        engine = ReasoningEngine()
        thinking = ThinkingResult(
            thinking_steps=["Step 1", "Step 2", "Step 3", "Step 4"],
            depth=2,
        )
        quality = engine.evaluate_thinking_quality(thinking)

        assert "coherence" in quality
        assert "completeness" in quality
        assert "correctness" in quality
        assert all(0 <= v <= 1 for v in quality.values())

    def test_analyze(self):
        """Test full analysis."""
        engine = ReasoningEngine()
        result = engine.analyze("Application performance issues")

        assert isinstance(result, FullAnalysisResult)
        assert result.hypotheses is not None
        assert result.reasoning_chain is not None
        assert result.conclusion is not None
        assert result.confidence > 0

    def test_analyze_no_hypotheses(self):
        """Test analysis when no hypotheses generated."""
        engine = ReasoningEngine()
        # Empty problem generates default hypotheses
        result = engine.analyze("")

        assert result.conclusion is not None

    def test_analyze_code_with_n_plus_1(self):
        """Test analyzing code with N+1 query pattern."""
        engine = ReasoningEngine()
        code = """
        for item in items:
            data = db.fetch(item.id)
            results.append(data)
        """
        result = engine.analyze_code(code, "performance issue")

        assert len(result.issues) > 0
        assert any("N+1" in issue for issue in result.issues)

    def test_analyze_code_with_inefficient_loop(self):
        """Test analyzing code with inefficient loop."""
        engine = ReasoningEngine()
        code = """
        for key in keys:
            value = cache.get(key)
        """
        result = engine.analyze_code(code, "slow operation")

        assert len(result.issues) > 0
        assert len(result.suggestions) > 0

    def test_analyze_code_no_issues(self):
        """Test analyzing clean code."""
        engine = ReasoningEngine()
        code = "x = 1 + 2"
        result = engine.analyze_code(code, "check code")

        assert any("No obvious" in issue for issue in result.issues)


# =============================================================================
# FirstPrinciplesThinker Tests
# =============================================================================


class TestFirstPrinciplesThinker:
    """Tests for FirstPrinciplesThinker class."""

    def test_analyze(self):
        """Test first principles analysis."""
        thinker = FirstPrinciplesThinker()
        result = thinker.analyze("Build a caching system")

        assert len(result.fundamental_truths) > 0
        assert len(result.assumptions_questioned) > 0
        assert result.rebuilt_solution is not None


# =============================================================================
# CriticalThinker Tests
# =============================================================================


class TestCriticalThinker:
    """Tests for CriticalThinker class."""

    def test_analyze_weak_argument(self):
        """Test analyzing weak argument."""
        thinker = CriticalThinker()
        result = thinker.analyze("This is fast because it's written in C")

        assert len(result.potential_flaws) > 0
        # Weak causal link detected
        assert any("causal" in flaw.lower() for flaw in result.potential_flaws)

    def test_analyze_unsupported_claim(self):
        """Test analyzing unsupported performance claim."""
        thinker = CriticalThinker()
        result = thinker.analyze("This is the best solution - it's very fast")

        assert len(result.potential_flaws) > 0
        assert any("evidence" in flaw.lower() for flaw in result.potential_flaws)

    def test_analyze_valid_argument(self):
        """Test analyzing valid argument."""
        thinker = CriticalThinker()
        result = thinker.analyze(
            "This is fast because we optimized the algorithm significantly and reduced complexity"
        )

        # Should not have weak causal link flaw
        assert result.logical_validity is not None

    def test_analyze_no_obvious_flaws(self):
        """Test analyzing argument with no obvious flaws."""
        thinker = CriticalThinker()
        result = thinker.analyze("The data is stored in a dictionary")

        assert len(result.potential_flaws) > 0  # Will have "requires additional evidence"

    def test_evaluate_evidence_supporting(self):
        """Test evaluating supporting evidence."""
        thinker = CriticalThinker()
        result = thinker.evaluate_evidence(
            "Database queries are slow",
            ["Query execution time is 500ms", "DB profiler shows bottleneck"],
        )

        assert result.evidence_strength > 0
        assert len(result.supporting_points) > 0

    def test_evaluate_evidence_weak(self):
        """Test evaluating weak evidence."""
        thinker = CriticalThinker()
        result = thinker.evaluate_evidence(
            "Memory usage is high", ["The server has 32GB RAM", "CPU utilization is normal"]
        )

        # Evidence doesn't directly relate
        assert len(result.weaknesses) > 0


# =============================================================================
# DeductiveReasoner Tests
# =============================================================================


class TestDeductiveReasoner:
    """Tests for DeductiveReasoner class."""

    def test_deduce_insufficient_premises(self):
        """Test deduction with insufficient premises."""
        reasoner = DeductiveReasoner()
        result = reasoner.deduce(["Single premise"])

        assert result.result == "Insufficient premises"
        assert result.valid is False

    def test_deduce_syllogism(self):
        """Test classic syllogism."""
        reasoner = DeductiveReasoner()
        result = reasoner.deduce(
            ["All programmers should have good debugging skills", "Alice is a programmer (Alice)"]
        )

        assert result.valid is True
        assert result.certain is True

    def test_deduce_with_have(self):
        """Test deduction with 'have' pattern."""
        reasoner = DeductiveReasoner()
        result = reasoner.deduce(
            ["All cats have whiskers", "Fluffy is a cat"]
        )

        assert result.valid is True
        assert "must have" in result.result.lower()

    def test_deduce_generic(self):
        """Test generic deduction."""
        reasoner = DeductiveReasoner()
        result = reasoner.deduce(["All dogs bark", "Rex is a dog"])

        assert result.valid is True

    def test_deduce_existential_quantifier(self):
        """Test deduction with existential quantifier."""
        reasoner = DeductiveReasoner()
        result = reasoner.deduce(
            ["Some animals are fast", "Cheetahs are animals"]
        )

        assert result.valid is True
        assert result.certain is False

    def test_deduce_no_universal(self):
        """Test deduction without universal quantifier."""
        reasoner = DeductiveReasoner()
        result = reasoner.deduce(["The sky is blue", "Water reflects the sky"])

        assert result.valid is True
        assert result.certain is False


# =============================================================================
# InductiveReasoner Tests
# =============================================================================


class TestInductiveReasoner:
    """Tests for InductiveReasoner class."""

    def test_induce_find_pattern(self):
        """Test finding patterns in observations."""
        reasoner = InductiveReasoner()
        result = reasoner.induce(
            [
                "Authentication failed with invalid token",
                "Authentication failed with expired token",
                "Authentication failed with missing token",
            ]
        )

        assert "authentication" in result.pattern.lower() or "token" in result.pattern.lower()
        assert result.confidence > 0

    def test_induce_empty_observations(self):
        """Test induction with empty observations."""
        reasoner = InductiveReasoner()
        result = reasoner.induce([])

        assert "issue" in result.pattern.lower()
        assert result.confidence == 0.5

    def test_induce_no_common_words(self):
        """Test induction with no meaningful common words."""
        reasoner = InductiveReasoner()
        result = reasoner.induce(["a b c", "d e f"])

        assert "issue" in result.pattern.lower()


# =============================================================================
# CausalReasoner Tests
# =============================================================================


class TestCausalReasoner:
    """Tests for CausalReasoner class."""

    def test_find_cause_recent_change(self):
        """Test finding cause with recent change."""
        reasoner = CausalReasoner()
        result = reasoner.find_cause(
            "Application crashes", ["New dependency added yesterday", "Server unchanged", "Code unchanged"]
        )

        assert result.likely_cause is not None
        assert "New dependency" in result.likely_cause
        assert result.confidence > 0.5

    def test_find_cause_no_recent_changes(self):
        """Test finding cause without recent changes."""
        reasoner = CausalReasoner()
        result = reasoner.find_cause("Performance degradation", ["Config same", "Code stable"])

        assert "Unknown" in result.likely_cause
        assert result.confidence < 0.5

    def test_predict_effect_validation_removal(self):
        """Test predicting effects of removing validation."""
        reasoner = CausalReasoner()
        result = reasoner.predict_effect("Remove input validation", {})

        assert len(result.possible_effects) > 0
        assert any("security" in e.lower() for e in result.possible_effects)

    def test_predict_effect_delete(self):
        """Test predicting effects of delete operation."""
        reasoner = CausalReasoner()
        result = reasoner.predict_effect("Delete user records", {})

        assert len(result.possible_effects) > 0
        assert any("data loss" in e.lower() for e in result.possible_effects)

    def test_predict_effect_unknown(self):
        """Test predicting effects of unknown action."""
        reasoner = CausalReasoner()
        result = reasoner.predict_effect("Do something", {})

        assert len(result.possible_effects) > 0


# =============================================================================
# MetaReasoner Tests
# =============================================================================


class TestMetaReasoner:
    """Tests for MetaReasoner class."""

    def test_analyze_with_weak_points(self):
        """Test analyzing trace with weak points."""
        reasoner = MetaReasoner()
        result = reasoner.analyze(
            [
                {"step": "Analysis", "confidence": 0.9},
                {"step": "Hypothesis", "confidence": 0.3},
                {"step": "Conclusion", "confidence": 0.8},
            ]
        )

        assert len(result.weak_points) > 0
        assert any("Hypothesis" in wp for wp in result.weak_points)
        assert len(result.improvement_suggestions) > 0

    def test_analyze_no_weak_points(self):
        """Test analyzing trace with no weak points."""
        reasoner = MetaReasoner()
        result = reasoner.analyze([{"step": "Analysis", "confidence": 0.9}])

        assert "No critical weaknesses" in result.weak_points[0]


# =============================================================================
# ChainOfThoughtReasoner Tests
# =============================================================================


class TestChainOfThoughtReasoner:
    """Tests for ChainOfThoughtReasoner class."""

    def test_reason_bug_problem(self):
        """Test reasoning about a bug."""
        reasoner = ChainOfThoughtReasoner()
        result = reasoner.reason("Bug in the application")

        assert len(result.steps) > 0
        assert result.final_answer is not None
        assert any("error" in step.lower() for step in result.steps)

    def test_reason_loop_modification_bug(self):
        """Test reasoning about loop modification bug."""
        reasoner = ChainOfThoughtReasoner()
        result = reasoner.reason("Bug: items removed from list during for loop range")

        assert "modifying collection during iteration" in result.final_answer.lower()

    def test_reason_general_problem(self):
        """Test reasoning about general problem."""
        reasoner = ChainOfThoughtReasoner()
        result = reasoner.reason("How to design API endpoints")

        assert len(result.steps) > 0
        assert "recommended action" in result.final_answer.lower()


# =============================================================================
# ReasoningVerifier Tests
# =============================================================================


class TestReasoningVerifier:
    """Tests for ReasoningVerifier class."""

    def test_verify_valid_python_reasoning(self):
        """Test verifying valid Python reasoning."""
        verifier = ReasoningVerifier()
        result = verifier.verify(
            {"premise": "Function has no return statement", "conclusion": "Returns None"}
        )

        assert result.is_valid is True
        assert result.confidence > 0.9

    def test_verify_invalid_test_reasoning(self):
        """Test verifying invalid test reasoning."""
        verifier = ReasoningVerifier()
        result = verifier.verify(
            {"premise": "All test passed", "conclusion": "There are no bugs"}
        )

        assert result.is_valid is False
        assert len(result.issues) > 0
        assert any("tests" in issue.lower() or "bugs" in issue.lower() for issue in result.issues)

    def test_verify_unknown_pattern(self):
        """Test verifying unknown reasoning pattern."""
        verifier = ReasoningVerifier()
        result = verifier.verify({"premise": "Some condition", "conclusion": "Some result"})

        assert result.confidence == 0.6


# =============================================================================
# UncertaintyHandler Tests
# =============================================================================


class TestUncertaintyHandler:
    """Tests for UncertaintyHandler class."""

    def test_quantify_with_evidence(self):
        """Test quantifying with evidence."""
        handler = UncertaintyHandler()
        result = handler.quantify("The issue is a memory leak", ["Log shows memory growth", "Profile confirms"])

        assert result.confidence > 0.5
        assert result.confidence_interval is not None
        assert result.confidence_interval[0] < result.confidence_interval[1]

    def test_quantify_with_hedging(self):
        """Test quantifying with hedging language."""
        handler = UncertaintyHandler()
        result = handler.quantify("This might be the cause", ["Some evidence"])

        # Hedging should reduce confidence
        assert result.confidence < 0.9

    def test_quantify_max_confidence(self):
        """Test confidence capped at 0.9."""
        handler = UncertaintyHandler()
        result = handler.quantify("Definite conclusion", ["e1", "e2", "e3", "e4", "e5"])

        assert result.confidence <= 0.9


# =============================================================================
# AmbiguityResolver Tests
# =============================================================================


class TestAmbiguityResolver:
    """Tests for AmbiguityResolver class."""

    def test_resolve_with_function_context(self):
        """Test resolving with function context."""
        resolver = AmbiguityResolver()
        result = resolver.resolve("Fix the function", {"current_file": "main.py"})

        assert "main.py" in result.clarified_meaning
        assert len(result.assumptions_made) > 0

    def test_resolve_with_error_line(self):
        """Test resolving with error line context."""
        resolver = AmbiguityResolver()
        result = resolver.resolve("Check this line", {"error_line": 42})

        assert "42" in result.clarified_meaning

    def test_resolve_no_context(self):
        """Test resolving without context."""
        resolver = AmbiguityResolver()
        result = resolver.resolve("Do something", {})

        assert "default interpretation" in result.assumptions_made[0].lower()


# =============================================================================
# AssumptionTracker Tests
# =============================================================================


class TestAssumptionTracker:
    """Tests for AssumptionTracker class."""

    def test_add_and_get_assumptions(self):
        """Test adding and retrieving assumptions."""
        tracker = AssumptionTracker()
        tracker.add_assumption("Server is running", "environment")
        tracker.add_assumption("Database is accessible", "environment")

        assumptions = tracker.get_all()
        assert len(assumptions) == 2

    def test_has_assumption(self):
        """Test checking for assumption."""
        tracker = AssumptionTracker()
        tracker.add_assumption("Python version is 3.9")

        assert tracker.has_assumption("python") is True
        assert tracker.has_assumption("java") is False

    def test_clear_assumptions(self):
        """Test clearing assumptions."""
        tracker = AssumptionTracker()
        tracker.add_assumption("Test")
        tracker.clear()

        assert len(tracker.get_all()) == 0


# =============================================================================
# DecisionMaker Tests
# =============================================================================


class TestDecisionMaker:
    """Tests for DecisionMaker class."""

    def test_decide_no_options(self):
        """Test deciding with no options."""
        maker = DecisionMaker()
        result = maker.decide([])

        assert result.chosen is None
        assert "No options" in result.reasoning

    def test_decide_single_criterion(self):
        """Test deciding with single criterion."""
        maker = DecisionMaker()
        result = maker.decide(
            [
                {"name": "Option A", "benefit": 8},
                {"name": "Option B", "benefit": 5},
                {"name": "Option C", "benefit": 9},
            ],
            criteria=["benefit"],
        )

        assert result.chosen["name"] == "Option C"
        assert len(result.alternatives_considered) == 2

    def test_decide_with_risk(self):
        """Test deciding with risk criterion (inverted)."""
        maker = DecisionMaker()
        result = maker.decide(
            [
                {"name": "Low Risk", "benefit": 5, "risk": 2},
                {"name": "High Risk", "benefit": 5, "risk": 8},
            ],
            criteria=["benefit", "risk"],
        )

        # Low risk should be preferred (risk is inverted)
        assert result.chosen["name"] == "Low Risk"


# =============================================================================
# HypothesisGenerator Tests
# =============================================================================


class TestHypothesisGenerator:
    """Tests for HypothesisGenerator class."""

    def test_generate_intermittent_issue(self):
        """Test generating hypotheses for intermittent issue."""
        generator = HypothesisGenerator()
        result = generator.generate("Intermittent test failures")

        assert len(result) > 0
        assert any("race condition" in h.description.lower() for h in result)

    def test_generate_failure(self):
        """Test generating hypotheses for failure."""
        generator = HypothesisGenerator()
        result = generator.generate("Build fail sometimes")

        assert any("environment" in h.description.lower() for h in result)

    def test_generate_slow_issue(self):
        """Test generating hypotheses for slow performance."""
        generator = HypothesisGenerator()
        result = generator.generate("Application is slow")

        assert any("performance" in h.description.lower() for h in result)

    def test_generate_default(self):
        """Test generating default hypotheses."""
        generator = HypothesisGenerator()
        result = generator.generate("Some issue")

        assert len(result) > 0

    def test_generate_for_bug_null(self):
        """Test generating hypotheses for null bug."""
        generator = HypothesisGenerator()
        result = generator.generate_for_bug({"description": "NullPointerException"})

        assert any("null" in h.description.lower() or "none" in h.description.lower() for h in result)

    def test_generate_for_bug_timeout(self):
        """Test generating hypotheses for timeout bug."""
        generator = HypothesisGenerator()
        result = generator.generate_for_bug({"description": "Request timeout"})

        assert any("timeout" in h.description.lower() for h in result)

    def test_generate_for_bug_generic(self):
        """Test generating hypotheses for generic bug."""
        generator = HypothesisGenerator()
        result = generator.generate_for_bug({"description": "Application error"})

        assert len(result) > 0


# =============================================================================
# HypothesisRanker Tests
# =============================================================================


class TestHypothesisRanker:
    """Tests for HypothesisRanker class."""

    def test_rank(self):
        """Test ranking hypotheses."""
        ranker = HypothesisRanker()
        hypotheses = [
            {"description": "H1", "evidence_count": 3},
            {"description": "H2", "evidence_count": 5},
            {"description": "H3", "evidence_count": 1},
        ]
        result = ranker.rank(hypotheses)

        assert result[0]["description"] == "H2"
        assert result[-1]["description"] == "H3"


# =============================================================================
# HypothesisTester Tests
# =============================================================================


class TestHypothesisTester:
    """Tests for HypothesisTester class."""

    def test_design_test_cache(self):
        """Test designing test for cache hypothesis."""
        tester = HypothesisTester()
        result = tester.design_test({"description": "Cache invalidation issue"})

        assert len(result.steps) > 0
        assert any("cache" in step.lower() for step in result.steps)

    def test_design_test_memory(self):
        """Test designing test for memory hypothesis."""
        tester = HypothesisTester()
        result = tester.design_test({"description": "Memory leak"})

        assert len(result.steps) > 0
        assert any("memory" in step.lower() for step in result.steps)

    def test_design_test_generic(self):
        """Test designing test for generic hypothesis."""
        tester = HypothesisTester()
        result = tester.design_test({"description": "Unknown issue"})

        assert len(result.steps) > 0
        assert result.success_criteria is not None


# =============================================================================
# ExperimentDesigner Tests
# =============================================================================


class TestExperimentDesigner:
    """Tests for ExperimentDesigner class."""

    def test_design_index_experiment(self):
        """Test designing index performance experiment."""
        designer = ExperimentDesigner()
        result = designer.design("Database index improves query performance")

        assert result.control_group is not None
        assert result.test_group is not None
        assert "20%" in result.success_criteria

    def test_design_generic_experiment(self):
        """Test designing generic experiment."""
        designer = ExperimentDesigner()
        result = designer.design("Some hypothesis")

        assert result.control_group is not None


# =============================================================================
# EvidenceCollector Tests
# =============================================================================


class TestEvidenceCollector:
    """Tests for EvidenceCollector class."""

    def test_collect(self):
        """Test collecting evidence."""
        collector = EvidenceCollector()
        result = collector.collect("Memory leak hypothesis", ["logs", "profiler", "metrics"])

        assert len(result.items) == 3
        assert all(item.strength == 0.6 for item in result.items)


# =============================================================================
# ConclusionDrawer Tests
# =============================================================================


class TestConclusionDrawer:
    """Tests for ConclusionDrawer class."""

    def test_draw_with_theme(self):
        """Test drawing conclusion with clear theme."""
        drawer = ConclusionDrawer()
        result = drawer.draw(
            [
                {"content": "Memory usage increasing over time"},
                {"content": "Memory not released after requests"},
            ]
        )

        assert "memory" in result.statement.lower()
        assert result.confidence > 0

    def test_draw_no_theme(self):
        """Test drawing inconclusive conclusion."""
        drawer = ConclusionDrawer()
        result = drawer.draw([{"content": "Some unrelated data"}])

        assert "inconclusive" in result.statement.lower()


# =============================================================================
# ActionPlanner Tests
# =============================================================================


class TestActionPlanner:
    """Tests for ActionPlanner class."""

    def test_plan_auth_feature(self):
        """Test planning authentication feature."""
        planner = ActionPlanner()
        result = planner.plan("Implement user authentication")

        assert len(result.steps) > 0
        assert any("auth" in step.action.lower() for step in result.steps)

    def test_plan_deployment(self):
        """Test planning deployment."""
        planner = ActionPlanner()
        result = planner.plan("Deploy new feature")

        assert len(result.steps) > 0
        assert any("deploy" in step.action.lower() for step in result.steps)

    def test_plan_fix(self):
        """Test planning fix."""
        planner = ActionPlanner()
        result = planner.plan("Fix performance issues")

        assert len(result.steps) > 0
        assert any("profile" in step.action.lower() for step in result.steps)

    def test_plan_generic(self):
        """Test planning generic task."""
        planner = ActionPlanner()
        result = planner.plan("Build something")

        assert len(result.steps) > 0
        assert result.approach == "systematic"

    def test_generate_alternatives(self):
        """Test generating alternative plans."""
        planner = ActionPlanner()
        result = planner.generate_alternatives("Fix bug", num_alternatives=3)

        assert len(result) == 3
        approaches = [p.approach for p in result]
        assert "fast_track" in approaches
        assert "thorough" in approaches

    def test_generate_fewer_alternatives(self):
        """Test generating fewer alternatives."""
        planner = ActionPlanner()
        result = planner.generate_alternatives("Fix bug", num_alternatives=2)

        assert len(result) == 2


# =============================================================================
# ProblemDecomposer Tests
# =============================================================================


class TestProblemDecomposer:
    """Tests for ProblemDecomposer class."""

    def test_decompose_with_keywords(self):
        """Test decomposing problem with keywords."""
        decomposer = ProblemDecomposer()
        result = decomposer.decompose("Build API with auth and rate limiting")

        assert len(result) > 0
        names = [p.name for p in result]
        assert "Authentication" in names
        assert "Rate Limiting" in names

    def test_decompose_generic(self):
        """Test decomposing generic problem."""
        decomposer = ProblemDecomposer()
        result = decomposer.decompose("Do something")

        assert len(result) >= 2
        # Should use generic decomposition
        names = [p.name for p in result]
        assert "Analysis" in names or "Design" in names

    def test_identify_subproblems_database(self):
        """Test identifying database subproblems."""
        decomposer = ProblemDecomposer()
        result = decomposer.identify_subproblems("Optimize database queries")

        assert len(result) > 0
        names = [p.name for p in result]
        assert any("Query" in name or "Index" in name for name in names)

    def test_identify_subproblems_performance(self):
        """Test identifying performance subproblems."""
        decomposer = ProblemDecomposer()
        result = decomposer.identify_subproblems("Fix performance issues")

        names = [p.name for p in result]
        assert any("Profiling" in name or "Hotspot" in name for name in names)

    def test_identify_subproblems_generic(self):
        """Test identifying generic subproblems."""
        decomposer = ProblemDecomposer()
        result = decomposer.identify_subproblems("Fix something")

        assert len(result) > 0


# =============================================================================
# SolutionComposer Tests
# =============================================================================


class TestSolutionComposer:
    """Tests for SolutionComposer class."""

    def test_compose_with_auth_and_rate_limit(self):
        """Test composing with auth and rate limiting."""
        composer = SolutionComposer()
        result = composer.compose(
            [
                {"problem": "Auth", "solution": "Use JWT tokens"},
                {"problem": "Rate limit", "solution": "Use Redis counters"},
            ]
        )

        assert "Auth" in result.integrated_solution
        assert len(result.integration_points) > 0
        assert any("before" in ip.lower() for ip in result.integration_points)

    def test_compose_with_logging(self):
        """Test composing with logging component."""
        composer = SolutionComposer()
        result = composer.compose(
            [
                {"problem": "Log", "solution": "Use structured logging"},
                {"problem": "API", "solution": "RESTful endpoints"},
            ]
        )

        assert any("log" in ip.lower() for ip in result.integration_points)

    def test_compose_generic(self):
        """Test composing generic solutions."""
        composer = SolutionComposer()
        result = composer.compose(
            [
                {"problem": "Feature A", "solution": "Solution A"},
                {"problem": "Feature B", "solution": "Solution B"},
            ]
        )

        assert "modularly" in result.integration_points[0].lower()
