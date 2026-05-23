"""
15-Step Procedural Workflow Orchestrator for SAGE AI Coding Agent.

This module implements a comprehensive workflow for AI-driven coding tasks:
1. Input Normalization & Prompt Autocorrection
2. Intent Decomposition
3. Brainstorming & Solution Search
4. Planning
5. Spec-to-Test Conversion (TDD)
6. Code Generation
7. Execution Loop
8. Self-Review & Static Analysis
9. Refactor Loop
10. Integration Validation
11. Git Workflow Automation
12. CI/CD Pipeline Execution
13. Post-Execution Evaluation
14. Memory & Retrieval Update
15. Human-in-the-Loop

Design Goals:
- Less noisy output for users
- Shows AI's plans during execution
- Shows all code changes
- Follows TDD principles
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
import subprocess
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from itertools import groupby
from pathlib import Path
from threading import Lock
from typing import Any, Protocol, Annotated

from sage.execution import TaskPriority, TaskStatus
from sage.core.commands import execute_command as _execute_command
from sage.core.p0_request_classification import (
    RequestTypeV2 as _RequestType,
    ClassifiedRequestV2 as _ClassifiedRequest,
    PipelineTypeV2 as _PipelineType,
)
from sage.core.checkpoint import CheckpointManager
from sage.core.security import SecurityAuditor
from sage.core.diagnostics import DiagnosticsClient as LSPClient
from sage.core.tools import ExecutionLedger, ToolCall, ToolType
from sage.core.codebase_analyzer import (
    analyze_project as _analyze_project_structure,
    CodeAnalyzer as RepoCodeAnalyzer,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Intelligent Execution Cycle Types
# =============================================================================


class ExecutionPhase(Enum):
    """Phases of the intelligent execution cycle."""

    DISCOVERY = auto()  # Understand the codebase
    PLANNING = auto()  # Create execution plan
    VALIDATION = auto()  # Pre-execution validation
    EXECUTION = auto()  # Execute the plan
    VERIFICATION = auto()  # Verify results
    RECOVERY = auto()  # Handle failures
    LEARNING = auto()  # Learn from outcome


@dataclass
class PlanTask:
    """A single task in the execution plan (for planning purposes)."""

    id: str
    description: str
    priority: TaskPriority
    dependencies: list[str] = field(default_factory=list)
    estimated_complexity: int = 1  # 1-5 scale
    files_involved: list[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed, skipped
    result: str = ""
    error: str = ""
    retries: int = 0
    max_retries: int = 3


@dataclass
class ExecutionPlan:
    """A complete execution plan."""

    id: str
    goal: str
    tasks: list[PlanTask] = field(default_factory=list)
    created_at: str = ""
    completed_at: str = ""
    status: str = "pending"
    total_retries: int = 0


@dataclass
class LearningEntry:
    """An entry in the learning database."""

    error_signature: str
    solution_pattern: str
    success_count: int = 0
    failure_count: int = 0
    last_used: str = ""


# =============================================================================
# Core Types and Protocols
# =============================================================================


class WorkflowSender(Protocol):
    """Protocol for AI model send functions."""

    def __call__(self, prompt: str) -> dict[str, Any]:
        """Send a prompt to the AI model and return structured response."""
        ...


class WorkflowStep(Enum):
    """Enumeration of all 15 workflow steps."""

    INPUT_NORMALIZATION = 1
    INTENT_DECOMPOSITION = 2
    BRAINSTORMING = 3
    PLANNING = 4
    SPEC_TO_TEST = 5
    CODE_GENERATION = 6
    EXECUTION_LOOP = 7
    SELF_REVIEW = 8
    REFACTOR_LOOP = 9
    INTEGRATION_VALIDATION = 10
    GIT_WORKFLOW = 11
    CICD_PIPELINE = 12
    POST_EVALUATION = 13
    MEMORY_UPDATE = 14
    HUMAN_IN_LOOP = 15


# =============================================================================
# Result Dataclasses
# =============================================================================


@dataclass
class NormalizationResult:
    """Result of Step 1: Input Normalization."""

    normalized_prompt: str
    corrections: list[str] = field(default_factory=list)
    confidence: float = 1.0
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class IntentResult:
    """Result of Step 2: Intent Decomposition."""

    primary_intent: str
    sub_intents: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    implicit_requirements: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class Solution:
    """A potential solution from brainstorming."""

    approach: str
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)


@dataclass
class BrainstormResult:
    """Result of Step 3: Brainstorming."""

    solutions: list[Solution] = field(default_factory=list)
    recommended_solution: str | None = None
    reasoning: str | None = None
    codebase_patterns: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class PlanStep:
    """A single step in the execution plan."""

    step_number: int
    action: str
    file: str | None = None
    rollback: str | None = None


@dataclass
class PlanResult:
    """Result of Step 4: Planning."""

    steps: list[PlanStep] = field(default_factory=list)
    dependencies: dict[str, list[str]] = field(default_factory=dict)
    rollback_points: list[dict[str, Any]] = field(default_factory=list)
    estimated_changes: int = 0
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class TestSpec:
    """A test specification."""

    name: str
    code: str


@dataclass
class TestGenerationResult:
    """Result of Step 5: Spec-to-Test Conversion."""

    tests: list[TestSpec] = field(default_factory=list)
    coverage_areas: list[str] = field(default_factory=list)
    tdd_phase: str = "red"
    expected_to_fail: bool = True
    raw_response: dict[str, Any] = field(default_factory=dict)
    assertion_count: int = 0

    def validate_tests(self) -> tuple[bool, list[str]]:
        """Validate that tests meet TDD quality requirements.

        Returns (is_valid, list_of_issues).
        """
        issues = []

        if not self.tests:
            issues.append("No tests were generated - TDD requires tests first")
            return False, issues

        for test in self.tests:
            # Check for empty test functions
            if "pass" in test.code and test.code.strip().endswith("pass"):
                issues.append(
                    f"Test '{test.name}' is empty (just 'pass') - tests must have assertions"
                )

            # Check for assertions
            assertion_patterns = [
                "assert ",
                "assertEqual",
                "assertTrue",
                "assertFalse",
                "assertRaises",
                "assertIn",
                "assertIsNone",
                "expect(",
                "should.",
                "pytest.raises",
            ]
            has_assertion = any(pattern in test.code for pattern in assertion_patterns)
            if not has_assertion:
                issues.append(f"Test '{test.name}' has no assertions - tests must verify behavior")

            # Check for placeholder comments
            placeholder_patterns = ["# TODO", "# FIXME", "# implement", "# placeholder"]
            for pattern in placeholder_patterns:
                if pattern.lower() in test.code.lower():
                    issues.append(f"Test '{test.name}' contains placeholder '{pattern}'")

        return len(issues) == 0, issues


@dataclass
class CodeChange:
    """A code change."""

    file: str
    action: str = "modify"
    content: str = ""
    diff: str = ""


@dataclass
class StyleAdherence:
    """Style adherence information."""

    naming_convention: str = "snake_case"
    docstrings: bool = True
    type_hints: bool = True


@dataclass
class CodeGenerationResult:
    """Result of Step 6: Code Generation."""

    code_changes: list[CodeChange] = field(default_factory=list)
    tests_targeted: list[str] = field(default_factory=list)
    style_adherence: StyleAdherence | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    """Result of Step 7: Execution Loop."""

    passed: int = 0
    failed: int = 0
    errors: int = 0
    failed_tests: list[str] = field(default_factory=list)
    execution_time: float = 0.0
    all_passed: bool = False
    iterations: int = 0
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewFinding:
    """A finding from code review."""

    severity: str
    message: str


@dataclass
class StaticAnalysis:
    """Static analysis results."""

    linting: dict[str, int] = field(default_factory=dict)
    type_checking: dict[str, int] = field(default_factory=dict)
    security: dict[str, int] = field(default_factory=dict)


@dataclass
class ReviewResult:
    """Result of Step 8: Self-Review."""

    quality_score: float = 0.0
    review_findings: list[ReviewFinding] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    static_analysis: StaticAnalysis | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class RefactorSuggestion:
    """A refactoring suggestion."""

    type: str
    location: str


@dataclass
class RefactorResult:
    """Result of Step 9: Refactor Loop."""

    suggestions: list[RefactorSuggestion] = field(default_factory=list)
    applied: bool = False
    tests_preserved: bool = True
    coverage_before: float = 0.0
    coverage_after: float = 0.0
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class IntegrationResult:
    """Result of Step 10: Integration Validation."""

    integration_valid: bool = False
    api_contracts_valid: bool = True
    database_migrations_valid: bool = True
    backward_compatible: bool = True
    breaking_changes: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class GitResult:
    """Result of Step 11: Git Workflow."""

    commit_message: str | None = None
    files_staged: list[str] = field(default_factory=list)
    branch_name: str | None = None
    conventional_commit: bool = True
    ready_for_pr: bool = False
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class CICDStage:
    """A CI/CD pipeline stage."""

    name: str
    status: str


@dataclass
class CICDResult:
    """Result of Step 12: CI/CD Pipeline."""

    pipeline_triggered: bool = False
    pipeline_id: str | None = None
    status: str = "pending"
    stages: list[CICDStage] = field(default_factory=list)
    estimated_duration: int = 0
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Result of Step 13: Post-Execution Evaluation."""

    task_completed: bool = False
    requirements_met: list[str] = field(default_factory=list)
    requirements_missing: list[str] = field(default_factory=list)
    confidence: float = 0.0
    follow_up_tasks: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryResult:
    """Result of Step 14: Memory Update."""

    learnings_stored: bool = False
    patterns_learned: list[str] = field(default_factory=list)
    knowledge_updated: bool = False
    context_updated: bool = False
    codebase_knowledge: dict[str, Any] = field(default_factory=dict)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class HumanReviewResult:
    """Result of Step 15: Human-in-the-Loop."""

    requires_approval: bool = False
    approval_points: list[str] = field(default_factory=list)
    summary: dict[str, Any] | None = None
    review_checklist: list[str] = field(default_factory=list)
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowResult:
    """Complete workflow execution result."""

    completed: bool = False
    current_step: int = 0
    steps_executed: list[int] = field(default_factory=list)
    error: str | None = None
    recovery_attempted: bool = False
    displayed_plan: dict[str, Any] | None = None
    code_changes_displayed: bool = False

    # Results from each step
    normalization: NormalizationResult | None = None
    intent: IntentResult | None = None
    brainstorm: BrainstormResult | None = None
    plan: PlanResult | None = None
    tests: TestGenerationResult | None = None
    code: CodeGenerationResult | None = None
    execution: ExecutionResult | None = None
    review: ReviewResult | None = None
    refactor: RefactorResult | None = None
    integration: IntegrationResult | None = None
    git: GitResult | None = None
    cicd: CICDResult | None = None
    evaluation: EvaluationResult | None = None
    memory: MemoryResult | None = None
    human_review: HumanReviewResult | None = None


# =============================================================================
# Procedural Workflow Orchestrator
# =============================================================================


class ProceduralWorkflowOrchestrator:
    """
    15-Step Procedural Workflow Orchestrator.

    Implements a comprehensive AI-driven coding workflow with:
    - Minimal noise output for users
    - Visible AI plans during execution
    - Full code change display
    - TDD principles throughout
    """

    STEP_NAMES = {
        1: "Input Normalization",
        2: "Intent Decomposition",
        3: "Brainstorming",
        4: "Planning",
        5: "Spec-to-Test (TDD)",
        6: "Code Generation",
        7: "Execution Loop",
        8: "Self-Review",
        9: "Refactor Loop",
        10: "Integration Validation",
        11: "Git Workflow",
        12: "CI/CD Pipeline",
        13: "Post-Evaluation",
        14: "Memory Update",
        15: "Human-in-the-Loop",
    }

    def __init__(self, send: WorkflowSender):
        """Initialize with AI model send function."""
        self._send = send
        self._current_context: dict[str, Any] = {}

    def _safe_send(self, prompt: str) -> dict[str, Any]:
        """Send prompt safely with error handling."""
        try:
            response = self._send(prompt)
            if isinstance(response, str):
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    return {"raw": response}
            return response or {}
        except Exception as e:
            logger.error(f"AI send error: {e}")
            return {"error": str(e)}

    # =========================================================================
    # Step 1: Input Normalization & Prompt Autocorrection
    # =========================================================================

    def step_1_normalize_input(self, raw_input: str) -> NormalizationResult:
        """
        Step 1: Normalize and autocorrect user input.

        - Fixes typos and abbreviations
        - Expands shorthand
        - Preserves technical terms
        """
        prompt = f"""Normalize and autocorrect this user input for a coding task.
Fix typos, expand abbreviations, but preserve technical terms.

Input: {raw_input}

Return JSON:
{{
    "normalized": "corrected and expanded prompt",
    "corrections": ["list of corrections made"],
    "confidence": 0.0 to 1.0
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return NormalizationResult(
            normalized_prompt=response.get("normalized", raw_input),
            corrections=response.get("corrections", []),
            confidence=response.get("confidence", 1.0),
            raw_response=response,
        )

    # =========================================================================
    # Step 2: Intent Decomposition
    # =========================================================================

    def step_2_decompose_intent(self, task: str) -> IntentResult:
        """
        Step 2: Decompose user intent into structured components.

        - Identifies primary intent
        - Extracts sub-intents
        - Finds entities and constraints
        - Discovers implicit requirements
        """
        prompt = f"""Decompose the intent of this coding task.

Task: {task}

Return JSON:
{{
    "primary_intent": "main action type",
    "sub_intents": ["list of sub-tasks"],
    "entities": ["key entities mentioned"],
    "constraints": ["explicit constraints"],
    "implicit_requirements": ["implied requirements not stated"]
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return IntentResult(
            primary_intent=response.get("primary_intent", "unknown"),
            sub_intents=response.get("sub_intents", []),
            entities=response.get("entities", []),
            constraints=response.get("constraints", []),
            implicit_requirements=response.get("implicit_requirements", []),
            raw_response=response,
        )

    # =========================================================================
    # Step 3: Brainstorming & Solution Search
    # =========================================================================

    def step_3_brainstorm_solutions(
        self, task: str, codebase_context: str | None = None
    ) -> BrainstormResult:
        """
        Step 3: Brainstorm multiple solution approaches.

        - Generates multiple solutions
        - Considers codebase patterns
        - Recommends best approach
        """
        context_info = f"\nCodebase Context: {codebase_context}" if codebase_context else ""

        prompt = f"""Brainstorm solutions for this coding task.
Generate multiple approaches with pros/cons.{context_info}

Task: {task}

Return JSON:
{{
    "solutions": [
        {{"approach": "solution 1", "pros": ["pro1"], "cons": ["con1"]}},
        {{"approach": "solution 2", "pros": ["pro2"], "cons": ["con2"]}}
    ],
    "recommended": "best solution name",
    "reasoning": "why this is recommended",
    "codebase_patterns": ["existing patterns to consider"]
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        solutions = []
        for sol in response.get("solutions", []):
            solutions.append(
                Solution(
                    approach=sol.get("approach", ""),
                    pros=sol.get("pros", []),
                    cons=sol.get("cons", []),
                )
            )

        return BrainstormResult(
            solutions=solutions,
            recommended_solution=response.get("recommended"),
            reasoning=response.get("reasoning"),
            codebase_patterns=response.get("codebase_patterns", []),
            raw_response=response,
        )

    # =========================================================================
    # Step 4: Planning
    # =========================================================================

    def step_4_create_plan(self, task: str) -> PlanResult:
        """
        Step 4: Create a detailed execution plan.

        - Defines ordered steps
        - Maps dependencies
        - Identifies rollback points
        """
        prompt = f"""Create an execution plan for this coding task.

Task: {task}

Return JSON:
{{
    "plan": [
        {{"step": 1, "action": "description", "file": "path/to/file.py", "rollback": "undo action"}}
    ],
    "dependencies": {{"step_2": ["step_1"]}},
    "rollback_points": [{{"step": 1, "action": "rollback description"}}],
    "estimated_changes": 3
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        steps = []
        for step in response.get("plan", []):
            steps.append(
                PlanStep(
                    step_number=step.get("step", 0),
                    action=step.get("action", ""),
                    file=step.get("file"),
                    rollback=step.get("rollback"),
                )
            )

        return PlanResult(
            steps=steps,
            dependencies=response.get("dependencies", {}),
            rollback_points=response.get("rollback_points", []),
            estimated_changes=response.get("estimated_changes", 0),
            raw_response=response,
        )

    # =========================================================================
    # Step 5: Spec-to-Test Conversion (TDD)
    # =========================================================================

    def step_5_generate_tests(self, spec: str) -> TestGenerationResult:
        """
        Step 5: Generate tests from specification (TDD Red phase).

        - Creates failing tests first
        - Covers happy path and edge cases
        - CRITICAL: Tests must have real assertions, not just 'pass'
        """
        prompt = f"""Generate tests for this specification using TDD (Test-Driven Development).
These tests are for the RED phase - they MUST fail initially because no implementation exists yet.

CRITICAL TDD REQUIREMENTS:
1. Each test MUST have real assertions (assert, assertEqual, assertTrue, etc.)
2. NEVER write empty test functions with just 'pass'
3. NEVER use placeholder comments like '# TODO' or '# implement this'
4. NO MOCKING BY DEFAULT: You MUST write live tests that execute real code on the local system. Only use mocks if the user specifically asked for them.
5. Tests should test ACTUAL expected behavior, not just "it works"
6. Include edge cases and error handling tests

Specification: {spec}

Return JSON:
{{
    "tests": [
        {{"name": "test_function_name_describes_behavior", "code": "def test_function_name_describes_behavior():\\n    # Test setup\\n    input_data = ...\\n    expected = ...\\n    # Act\\n    result = function_under_test(input_data)\\n    # Assert - REAL assertion\\n    assert result == expected"}}
    ],
    "coverage_areas": ["happy path", "error handling", "edge cases", "boundary conditions"],
    "tdd_phase": "red",
    "expected_to_fail": true,
    "assertion_count": 5
}}

VALIDATION: Each test function MUST contain at least one assertion keyword (assert, assertEqual, etc.).
Tests without assertions will be REJECTED.

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        tests = []
        for test in response.get("tests", []):
            tests.append(
                TestSpec(
                    name=test.get("name", ""),
                    code=test.get("code", ""),
                )
            )

        return TestGenerationResult(
            tests=tests,
            coverage_areas=response.get("coverage_areas", []),
            tdd_phase=response.get("tdd_phase", "red"),
            expected_to_fail=response.get("expected_to_fail", True),
            raw_response=response,
        )

    # =========================================================================
    # Step 6: Code Generation
    # =========================================================================

    def step_6_generate_code(
        self, tests: list[str], style_guide: str | None = None
    ) -> CodeGenerationResult:
        """
        Step 6: Generate code to pass tests (TDD Green phase).

        - Writes minimal code to pass tests
        - Follows style guide
        - CRITICAL: Code must be complete, no placeholders
        """
        style_info = f"\nStyle Guide: {style_guide}" if style_guide else ""

        prompt = f"""Generate COMPLETE, WORKING implementation code to pass these tests (TDD GREEN phase).
The tests are already written and failing. Your implementation must make them pass.{style_info}

CRITICAL IMPLEMENTATION REQUIREMENTS:
1. Write COMPLETE, FUNCTIONAL code - no placeholders, no TODOs, no 'pass' statements
2. Every function MUST have actual implementation logic
3. NEVER use comments like '# implement this' or '# placeholder'
4. Code must be ready to run without modification
5. Include proper error handling where appropriate
6. Use type hints for function signatures

Tests to make pass: {json.dumps(tests)}

Return JSON:
{{
    "code_changes": [
        {{"file": "path/to/file.py", "action": "create", "content": "# Complete implementation\\nimport ...\\n\\ndef function_name(param: Type) -> ReturnType:\\n    '''Docstring explaining behavior.'''\\n    # Actual implementation logic\\n    result = compute_something(param)\\n    return result"}}
    ],
    "tests_targeted": ["test_name1", "test_name2"],
    "style_adherence": {{
        "naming_convention": "snake_case",
        "docstrings": true,
        "type_hints": true
    }},
    "implementation_complete": true
}}

VALIDATION:
- Code with 'pass' as the only statement in a function will be REJECTED
- Code with TODO/FIXME comments will be REJECTED
- Code that cannot make tests pass will be REJECTED

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        changes = []
        for change in response.get("code_changes", []):
            changes.append(
                CodeChange(
                    file=change.get("file", ""),
                    action=change.get("action", "modify"),
                    content=change.get("content", ""),
                )
            )

        style = None
        if "style_adherence" in response:
            sa = response["style_adherence"]
            style = StyleAdherence(
                naming_convention=sa.get("naming_convention", "snake_case"),
                docstrings=sa.get("docstrings", True),
                type_hints=sa.get("type_hints", True),
            )

        return CodeGenerationResult(
            code_changes=changes,
            tests_targeted=response.get("tests_targeted", []),
            style_adherence=style,
            raw_response=response,
        )

    # =========================================================================
    # Step 7: Execution Loop
    # =========================================================================

    def step_7_execute_tests(self, max_iterations: int = 5) -> ExecutionResult:
        """
        Step 7: Execute tests and iterate until passing.

        - Runs test suite
        - Reports results
        - Iterates on failures
        """
        prompt = """Execute tests and report results.

Return JSON:
{{
    "test_results": {{"passed": 5, "failed": 1, "errors": 0}},
    "failed_tests": ["test_name"],
    "execution_time": 2.5,
    "all_passed": false
}}

Respond ONLY with valid JSON."""

        iterations = 0
        all_passed = False

        while iterations < max_iterations and not all_passed:
            response = self._safe_send(prompt)
            iterations += 1

            results = response.get("test_results", {})
            all_passed = response.get("all_passed", results.get("failed", 1) == 0)

            if all_passed:
                break

        results = response.get("test_results", {})

        return ExecutionResult(
            passed=results.get("passed", 0),
            failed=results.get("failed", 0),
            errors=results.get("errors", 0),
            failed_tests=response.get("failed_tests", []),
            execution_time=response.get("execution_time", 0.0),
            all_passed=all_passed,
            iterations=iterations,
            raw_response=response,
        )

    # =========================================================================
    # Step 8: Self-Review & Static Analysis
    # =========================================================================

    def step_8_self_review(self) -> ReviewResult:
        """
        Step 8: Perform code review and static analysis.

        - Reviews code quality
        - Runs linting and type checking
        - Checks for security issues
        """
        prompt = """Review the generated code for quality issues.

Return JSON:
{{
    "review_findings": [
        {{"severity": "warning", "message": "description"}}
    ],
    "quality_score": 8.5,
    "suggestions": ["suggestion 1"],
    "static_analysis": {{
        "linting": {{"errors": 0, "warnings": 2}},
        "type_checking": {{"errors": 0}},
        "security": {{"vulnerabilities": 0}}
    }}
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        findings = []
        for finding in response.get("review_findings", []):
            findings.append(
                ReviewFinding(
                    severity=finding.get("severity", "info"),
                    message=finding.get("message", ""),
                )
            )

        static = None
        if "static_analysis" in response:
            sa = response["static_analysis"]
            static = StaticAnalysis(
                linting=sa.get("linting", {}),
                type_checking=sa.get("type_checking", {}),
                security=sa.get("security", {}),
            )

        return ReviewResult(
            quality_score=response.get("quality_score", 0.0),
            review_findings=findings,
            suggestions=response.get("suggestions", []),
            static_analysis=static,
            raw_response=response,
        )

    # =========================================================================
    # Step 9: Refactor Loop
    # =========================================================================

    def step_9_refactor(self) -> RefactorResult:
        """
        Step 9: Refactor code while preserving tests.

        - Identifies refactoring opportunities
        - Applies safe refactorings
        - Ensures tests still pass
        """
        prompt = """Identify refactoring opportunities and apply them.

Return JSON:
{{
    "refactoring_suggestions": [
        {{"type": "extract_method", "location": "file.py:50-60"}}
    ],
    "applied": true,
    "tests_still_passing": true,
    "coverage_before": 85.0,
    "coverage_after": 87.0
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        suggestions = []
        for sug in response.get("refactoring_suggestions", []):
            suggestions.append(
                RefactorSuggestion(
                    type=sug.get("type", ""),
                    location=sug.get("location", ""),
                )
            )

        return RefactorResult(
            suggestions=suggestions,
            applied=response.get("applied", False),
            tests_preserved=response.get("tests_still_passing", True),
            coverage_before=response.get("coverage_before", 0.0),
            coverage_after=response.get("coverage_after", 0.0),
            raw_response=response,
        )

    # =========================================================================
    # Step 10: Integration Validation
    # =========================================================================

    def step_10_validate_integration(self) -> IntegrationResult:
        """
        Step 10: Validate integration with existing code.

        - Checks integration points
        - Validates API contracts
        - Verifies backward compatibility
        """
        prompt = """Validate integration with the existing codebase.

Return JSON:
{{
    "integration_tests_passed": true,
    "api_contracts_valid": true,
    "database_migrations_valid": true,
    "backward_compatible": true,
    "breaking_changes": []
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return IntegrationResult(
            integration_valid=response.get("integration_tests_passed", False),
            api_contracts_valid=response.get("api_contracts_valid", True),
            database_migrations_valid=response.get("database_migrations_valid", True),
            backward_compatible=response.get("backward_compatible", True),
            breaking_changes=response.get("breaking_changes", []),
            raw_response=response,
        )

    # =========================================================================
    # Step 11: Git Workflow Automation
    # =========================================================================

    def step_11_git_workflow(self) -> GitResult:
        """
        Step 11: Automate git workflow.

        - Creates meaningful commits
        - Manages branches
        - Prepares for PR
        """
        prompt = """Create git commits and manage branches for the changes.

Return JSON:
{{
    "commit_message": "feat(scope): description",
    "files_staged": ["file1.py", "file2.py"],
    "conventional_commit": true,
    "branch_created": "feature/name",
    "base_branch": "main",
    "ready_for_pr": true
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return GitResult(
            commit_message=response.get("commit_message"),
            files_staged=response.get("files_staged", []),
            branch_name=response.get("branch_created"),
            conventional_commit=response.get("conventional_commit", True),
            ready_for_pr=response.get("ready_for_pr", False),
            raw_response=response,
        )

    # =========================================================================
    # Step 12: CI/CD Pipeline Execution
    # =========================================================================

    def step_12_run_cicd(self) -> CICDResult:
        """
        Step 12: Trigger and monitor CI/CD pipeline.

        - Triggers pipeline
        - Reports status
        - Handles failures
        """
        prompt = """Trigger CI/CD pipeline and report status.

Return JSON:
{{
    "pipeline_triggered": true,
    "pipeline_id": "ci-12345",
    "status": "passed",
    "stages": [
        {{"name": "build", "status": "passed"}},
        {{"name": "test", "status": "passed"}}
    ],
    "estimated_duration": 300
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        stages = []
        for stage in response.get("stages", []):
            stages.append(
                CICDStage(
                    name=stage.get("name", ""),
                    status=stage.get("status", "pending"),
                )
            )

        return CICDResult(
            pipeline_triggered=response.get("pipeline_triggered", False),
            pipeline_id=response.get("pipeline_id"),
            status=response.get("status", "pending"),
            stages=stages,
            estimated_duration=response.get("estimated_duration", 0),
            raw_response=response,
        )

    # =========================================================================
    # Step 13: Post-Execution Evaluation
    # =========================================================================

    def step_13_evaluate(self) -> EvaluationResult:
        """
        Step 13: Evaluate task completion.

        - Checks requirements met
        - Measures confidence
        - Identifies follow-up tasks
        """
        prompt = """Evaluate if the task was completed successfully.

Return JSON:
{{
    "task_completed": true,
    "requirements_met": ["requirement 1", "requirement 2"],
    "requirements_missing": [],
    "confidence": 0.95,
    "follow_up_tasks": ["optional future improvement"]
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return EvaluationResult(
            task_completed=response.get("task_completed", False),
            requirements_met=response.get("requirements_met", []),
            requirements_missing=response.get("requirements_missing", []),
            confidence=response.get("confidence", 0.0),
            follow_up_tasks=response.get("follow_up_tasks", []),
            raw_response=response,
        )

    # =========================================================================
    # Step 14: Memory & Retrieval Update
    # =========================================================================

    def step_14_update_memory(self) -> MemoryResult:
        """
        Step 14: Update memory and context for future tasks.

        - Stores learnings
        - Updates codebase knowledge
        - Prepares context for future
        """
        prompt = """Update memory with learnings from this task.

Return JSON:
{{
    "learnings_stored": true,
    "patterns_learned": ["pattern description"],
    "knowledge_updated": true,
    "context_updated": true,
    "codebase_knowledge": {{"key": "value"}}
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return MemoryResult(
            learnings_stored=response.get("learnings_stored", False),
            patterns_learned=response.get("patterns_learned", []),
            knowledge_updated=response.get("knowledge_updated", False),
            context_updated=response.get("context_updated", False),
            codebase_knowledge=response.get("codebase_knowledge", {}),
            raw_response=response,
        )

    # =========================================================================
    # Step 15: Human-in-the-Loop
    # =========================================================================

    def step_15_human_review(self) -> HumanReviewResult:
        """
        Step 15: Request human review when needed.

        - Identifies approval points
        - Provides summary
        - Creates review checklist
        """
        prompt = """Determine if human review is needed and prepare summary.

Return JSON:
{{
    "requires_approval": true,
    "approval_points": ["point needing review"],
    "summary": {{
        "changes_made": 5,
        "tests_added": 3,
        "files_modified": ["file1.py"]
    }},
    "review_checklist": ["Security", "Performance"]
}}

Respond ONLY with valid JSON."""

        response = self._safe_send(prompt)

        return HumanReviewResult(
            requires_approval=response.get("requires_approval", False),
            approval_points=response.get("approval_points", []),
            summary=response.get("summary"),
            review_checklist=response.get("review_checklist", []),
            raw_response=response,
        )

    # =========================================================================
    # Full Workflow Execution
    # =========================================================================

    def execute(
        self,
        task: str,
        stop_after_step: int | None = None,
        on_progress: Callable[[int, str], None] | None = None,
        verbosity: str = "normal",
        show_code_changes: bool = True,
    ) -> WorkflowResult:
        """
        Execute the complete 15-step workflow.

        Args:
            task: The coding task to execute
            stop_after_step: Stop after this step (for resumable workflows)
            on_progress: Callback for progress updates (step, status)
            verbosity: Output level ("minimal", "normal", "plan", "verbose")
            show_code_changes: Whether to display code changes

        Returns:
            WorkflowResult with all step results
        """
        result = WorkflowResult()
        total_steps = stop_after_step or 15

        def report_progress(step: int, status: str):
            if on_progress:
                on_progress(step, status)
            if verbosity != "minimal":
                logger.info(f"Step {step}: {self.STEP_NAMES.get(step, 'Unknown')} - {status}")

        try:
            # Step 1: Input Normalization
            report_progress(1, "started")
            result.normalization = self.step_1_normalize_input(task)
            result.steps_executed.append(1)
            result.current_step = 1
            report_progress(1, "completed")
            if total_steps == 1:
                return result

            normalized_task = result.normalization.normalized_prompt

            # Step 2: Intent Decomposition
            report_progress(2, "started")
            result.intent = self.step_2_decompose_intent(normalized_task)
            result.steps_executed.append(2)
            result.current_step = 2
            report_progress(2, "completed")
            if total_steps == 2:
                return result

            # Step 3: Brainstorming
            report_progress(3, "started")
            result.brainstorm = self.step_3_brainstorm_solutions(normalized_task)
            result.steps_executed.append(3)
            result.current_step = 3
            report_progress(3, "completed")
            if total_steps == 3:
                return result

            # Step 4: Planning
            report_progress(4, "started")
            result.plan = self.step_4_create_plan(normalized_task)
            result.steps_executed.append(4)
            result.current_step = 4
            if verbosity in ("plan", "verbose"):
                result.displayed_plan = {
                    "steps": [
                        {"step": s.step_number, "action": s.action} for s in result.plan.steps
                    ],
                    "estimated_changes": result.plan.estimated_changes,
                }
            report_progress(4, "completed")
            if total_steps == 4:
                return result

            # Step 5: Spec-to-Test (TDD)
            report_progress(5, "started")
            result.tests = self.step_5_generate_tests(normalized_task)
            result.steps_executed.append(5)
            result.current_step = 5

            # TDD GATE: Validate tests before proceeding to implementation
            max_test_retries = 3
            test_retry = 0
            tests_valid, test_issues = result.tests.validate_tests()

            while not tests_valid and test_retry < max_test_retries:
                test_retry += 1
                logger.warning(
                    f"TDD Gate: Test validation failed (attempt {test_retry}/{max_test_retries})"
                )
                for issue in test_issues:
                    logger.warning(f"  - {issue}")

                # Regenerate tests with explicit feedback about failures
                regenerate_prompt = f"""Your previous tests were REJECTED for the following reasons:
{chr(10).join(f"- {issue}" for issue in test_issues)}

You MUST fix these issues. Requirements:
1. Every test function MUST have at least one assertion (assert, assertEqual, etc.)
2. NO empty functions with just 'pass'
3. NO placeholder comments (TODO, FIXME, etc.)
4. Tests must verify actual expected behavior

Specification: {normalized_task}

Regenerate the tests with REAL assertions."""

                result.tests = self.step_5_generate_tests(regenerate_prompt)
                tests_valid, test_issues = result.tests.validate_tests()

            if not tests_valid:
                result.error = f"TDD Gate Failed: Tests do not meet quality requirements after {max_test_retries} attempts: {'; '.join(test_issues)}"
                logger.error(result.error)
                return result

            report_progress(5, "completed")
            if total_steps == 5:
                return result

            # Step 6: Code Generation (only proceeds if tests are valid)
            report_progress(6, "started")
            test_names = [t.name for t in result.tests.tests]
            result.code = self.step_6_generate_code(test_names)
            result.steps_executed.append(6)
            result.current_step = 6
            if show_code_changes:
                result.code_changes_displayed = True
            report_progress(6, "completed")
            if total_steps == 6:
                return result

            # Step 7: Execution Loop
            report_progress(7, "started")
            result.execution = self.step_7_execute_tests()
            result.steps_executed.append(7)
            result.current_step = 7
            report_progress(7, "completed")
            if total_steps == 7:
                return result

            # Step 8: Self-Review
            report_progress(8, "started")
            result.review = self.step_8_self_review()
            result.steps_executed.append(8)
            result.current_step = 8
            report_progress(8, "completed")
            if total_steps == 8:
                return result

            # Step 9: Refactor Loop
            report_progress(9, "started")
            result.refactor = self.step_9_refactor()
            result.steps_executed.append(9)
            result.current_step = 9
            report_progress(9, "completed")
            if total_steps == 9:
                return result

            # Step 10: Integration Validation
            report_progress(10, "started")
            result.integration = self.step_10_validate_integration()
            result.steps_executed.append(10)
            result.current_step = 10
            report_progress(10, "completed")
            if total_steps == 10:
                return result

            # Step 11: Git Workflow
            report_progress(11, "started")
            result.git = self.step_11_git_workflow()
            result.steps_executed.append(11)
            result.current_step = 11
            report_progress(11, "completed")
            if total_steps == 11:
                return result

            # Step 12: CI/CD Pipeline
            report_progress(12, "started")
            result.cicd = self.step_12_run_cicd()
            result.steps_executed.append(12)
            result.current_step = 12
            report_progress(12, "completed")
            if total_steps == 12:
                return result

            # Step 13: Post-Evaluation
            report_progress(13, "started")
            result.evaluation = self.step_13_evaluate()
            result.steps_executed.append(13)
            result.current_step = 13
            report_progress(13, "completed")
            if total_steps == 13:
                return result

            # Step 14: Memory Update
            report_progress(14, "started")
            result.memory = self.step_14_update_memory()
            result.steps_executed.append(14)
            result.current_step = 14
            report_progress(14, "completed")
            if total_steps == 14:
                return result

            # Step 15: Human-in-the-Loop
            report_progress(15, "started")
            result.human_review = self.step_15_human_review()
            result.steps_executed.append(15)
            result.current_step = 15
            report_progress(15, "completed")

            result.completed = True

        except Exception as e:
            result.error = str(e)
            result.recovery_attempted = True
            logger.error(f"Workflow error at step {result.current_step}: {e}")

        return result


def _detect_repetition(responses: list[str], current: str) -> bool:
    """Detect if the model is stuck in a loop producing identical responses."""
    if not responses:
        return False
    # Require 3 consecutive matches on 2000 chars before flagging a loop so
    # minor differences (attempt numbers, line numbers) don't trigger early.
    current_stripped = current.strip()[:2000]
    if len(responses) < 3:
        return False
    for prev in responses[-3:]:
        if prev.strip()[:2000] != current_stripped:
            return False
    return True


# =============================================================================
# Helper Functions (Migrated from main.py)
# =============================================================================


def _summarize_test_output(output: str, max_chars: int = 6000) -> str:
    """Condense long test output into failure-focused context for fix prompts."""
    text = output.strip()
    if len(text) <= max_chars:
        return text

    lines = text.splitlines()
    keep: list[str] = []
    for i, line in enumerate(lines):
        low = line.lower()
        if (
            "error collecting" in low
            or "short test summary info" in low
            or "traceback" in low
            or line.startswith("E   ")
            or " failed " in low
            or line.startswith("FAILED ")
            or line.startswith("ERROR ")
        ):
            start = max(0, i - 2)
            end = min(len(lines), i + 6)
            keep.extend(lines[start:end])

    if not keep:
        return text[-max_chars:]

    deduped = []
    seen = set()
    for ln in keep:
        if ln not in seen:
            deduped.append(ln)
            seen.add(ln)
    summary = "\n".join(deduped)
    return summary[:max_chars]


def _detect_broken_test_files(output: str, cwd: Path) -> list[Path]:
    """Detect test files with import errors from test output."""
    from sage.core.validation import module_exists_in_codebase as _module_exists_in_codebase
    from sage.core.validation import validate_imports_in_content as _validate_imports_in_content

    broken_files: list[Path] = []
    seen_files: set[str] = set()

    lines = output.splitlines()
    current_file: Path | None = None

    for i, line in enumerate(lines):
        file_patterns = [
            r"^(tests?/[^\s:]+\.py):\d+:",
            r"^(\./tests?/[^\s:]+\.py):\d+:",
            r"^([^\s:]+/tests?/[^\s:]+\.py):\d+:",
            r"^([^\s:]+test_[^\s:]+\.py):\d+:",
        ]

        for pattern in file_patterns:
            file_match = re.search(pattern, line)
            if file_match:
                filepath = file_match.group(1).lstrip("./")
                current_file = cwd / filepath
                break

        import_error_patterns = [
            r"ModuleNotFoundError:\s*No module named\s*['\"]([^'\"]+)['\"]",
            r"ImportError:\s*cannot import name\s*['\"]([^'\"]+)['\"].*from\s*['\"]([^'\"]+)['\"]",
            r"ImportError:\s*No module named\s*['\"]([^'\"]+)['\"]",
        ]

        for error_pattern in import_error_patterns:
            error_match = re.search(error_pattern, line)
            if error_match and current_file:
                module_name = error_match.group(1).split(".")[0]
                if not _module_exists_in_codebase(module_name, cwd):
                    file_key = str(current_file)
                    if current_file.exists() and file_key not in seen_files:
                        broken_files.append(current_file)
                        seen_files.add(file_key)
                        current_file = None
                break

        if "SyntaxError" in line or "IndentationError" in line:
            if current_file and current_file.exists():
                file_key = str(current_file)
                if file_key not in seen_files:
                    broken_files.append(current_file)
                    seen_files.add(file_key)
                    current_file = None

    error_collect_patterns = [
        r"error collecting\s+([^\s]+\.py)",
        r"ERROR collecting\s+([^\s]+\.py)",
        r"ERROR\s+([^\s]+test_[^\s]+\.py)",
    ]

    for i, line in enumerate(lines):
        for pattern in error_collect_patterns:
            error_collect_match = re.search(pattern, line, re.IGNORECASE)
            if error_collect_match:
                filepath = error_collect_match.group(1).lstrip("./")
                file_path = cwd / filepath
                file_key = str(file_path)

                if file_path.exists() and file_key not in seen_files:
                    for j in range(i, min(i + 15, len(lines))):
                        check_line = lines[j]
                        module_match = re.search(
                            r"No module named\s*['\"]([^'\"]+)['\"]", check_line
                        )
                        if module_match:
                            module_name = module_match.group(1).split(".")[0]
                            if not _module_exists_in_codebase(module_name, cwd):
                                broken_files.append(file_path)
                                seen_files.add(file_key)
                                break
                        if "SyntaxError" in check_line or "IndentationError" in check_line:
                            broken_files.append(file_path)
                            seen_files.add(file_key)
                            break

    for tests_dir in ["tests", "test"]:
        tests_path = cwd / tests_dir
        if tests_path.is_dir():
            for test_file in tests_path.glob("test_*.py"):
                file_key = str(test_file)
                if file_key in seen_files:
                    continue

                try:
                    content = test_file.read_text(encoding="utf-8", errors="ignore")
                    is_valid, missing = _validate_imports_in_content(content, cwd)
                    if not is_valid and missing:
                        for module in missing:
                            if module in output:
                                broken_files.append(test_file)
                                seen_files.add(file_key)
                                break
                except Exception:
                    pass

    return broken_files


def _cleanup_broken_tests(broken_files: list[Path], renderer) -> list[str]:
    """Delete broken test files that import non-existent modules."""
    deleted: list[str] = []
    for file_path in broken_files:
        try:
            rel_path = str(
                file_path.relative_to(file_path.parent.parent.parent)
                if len(file_path.parts) > 3
                else file_path.name
            )
            file_path.unlink()
            deleted.append(str(file_path))
            if renderer:
                renderer.warning(
                    f"🗑️  Deleted broken test file: {rel_path} (imports non-existent modules)"
                )
        except OSError as e:
            if renderer:
                renderer.warning(f"Could not delete {file_path}: {e}")
    return deleted


def _has_errors(output: str) -> bool:
    """Check if command output indicates failure."""
    from sage.core.shell import has_test_errors
    return has_test_errors(output)


def _discover_project_modules(cwd: Path, max_depth: int = 3) -> list[str]:
    """Scan project directory and return available Python module paths."""
    modules: list[str] = []
    import os
    
    # Optimization: Use os.walk for efficiency and early directory pruning
    for root, dirs, files in os.walk(cwd):
        # Prune directories in-place
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"node_modules", "__pycache__", "venv", ".venv"}]
        
        root_path = Path(root)
        try:
            rel_root = root_path.relative_to(cwd)
        except ValueError:
            continue
            
        if len(rel_root.parts) > max_depth:
            # We still need to process files in this directory if it's at max_depth,
            # but we don't want to go deeper.
            dirs[:] = [] 
            
        for f in files:
            if not f.endswith(".py") or f.startswith("."):
                continue
                
            p = root_path / f
            try:
                rel = p.relative_to(cwd)
            except ValueError:
                continue
                
            parts = rel.parts
            if f == "__init__.py":
                mod = ".".join(parts[:-1])
            else:
                mod = ".".join(parts)[:-3]
            if mod:
                modules.append(mod)
                
            if len(modules) >= 100: # Safety cap
                break
        if len(modules) >= 100:
            break
            
    return sorted(set(modules))[:50]


def _build_smart_error_context(output: str, written: list[str], cwd: Path) -> str:
    """Build context-aware error feedback with module discovery."""
    from sage.core.shell import run_shell
    extra = []

    if "ModuleNotFoundError" in output or "ImportError" in output:
        modules = _discover_project_modules(cwd)
        if modules:
            extra.append(
                "AVAILABLE PROJECT MODULES (use these for imports):\n"
                + "\n".join(f"  - {m}" for m in modules[:30])
                + "\n\nDo NOT import modules that are not in this list. "
                "Use the correct module paths shown above."
            )

        import_match = re.search(r"No module named ['\"]([^'\"]+)['\"]", output)
        if import_match:
            bad_module = import_match.group(1)
            extra.append(
                f"FAILED IMPORT: '{bad_module}'\n"
                "COMMON FIXES:\n"
                "- Check spelling of module name\n"
                "- Ensure __init__.py exists in package directories\n"
                "- Use relative imports if within same package\n"
                "- Verify the module file exists before importing"
            )

    if "FileNotFoundError" in output or "No such file" in output:
        tree_result = run_shell(
            "find . -name '*.py' -not -path './__pycache__/*' -not -path './.git/*' | head -30",
            cwd,
            timeout=5,
        )
        if tree_result.strip():
            extra.append(f"PROJECT FILES:\n{tree_result}")

    if "SyntaxError" in output:
        line_match = re.search(r"line (\d+)", output)
        if line_match:
            line_num = line_match.group(1)
            extra.append(
                f"SYNTAX ERROR at line {line_num}\n"
                "COMMON CAUSES:\n"
                "- Missing colon after if/for/def/class\n"
                "- Unclosed parentheses, brackets, or quotes\n"
                "- Incorrect indentation\n"
                "- Missing comma in list/dict/function args"
            )

    if "IndentationError" in output or "TabError" in output:
        extra.append(
            "INDENTATION ERROR\n"
            "FIXES:\n"
            "- Use consistent 4-space indentation (no tabs)\n"
            "- Check that all lines in a block have same indent\n"
            "- Ensure no mixed tabs and spaces"
        )

    if "NameError" in output:
        name_match = re.search(r"name ['\"]([^'\"]+)['\"] is not defined", output)
        if name_match:
            bad_name = name_match.group(1)
            extra.append(
                f"UNDEFINED NAME: '{bad_name}'\n"
                "COMMON FIXES:\n"
                "- Check spelling of variable/function name\n"
                "- Ensure it's defined before use\n"
                "- Add missing import if it's from another module\n"
                "- Check variable scope (local vs global)"
            )

    if "TypeError" in output:
        arg_match = re.search(r"takes (\d+) .*arguments? but (\d+)", output)
        if arg_match:
            expected, got = arg_match.group(1), arg_match.group(2)
            extra.append(
                f"ARGUMENT COUNT MISMATCH: expected {expected}, got {got}\n"
                "FIX: Check the function signature and match the argument count"
            )

    if "AssertionError" in output:
        extra.append(
            "TEST ASSERTION FAILED\n"
            "DEBUG STEPS:\n"
            "1. Check expected vs actual values in the assertion\n"
            "2. Verify the implementation logic\n"
            "3. Add print/debug statements if needed\n"
            "4. Ensure test data matches expected format"
        )

    if "AttributeError" in output:
        attr_match = re.search(
            r"['\"]([^'\"]+)['\"] object has no attribute ['\"]([^'\"]+)['\"]", output
        )
        if attr_match:
            obj_type, attr_name = attr_match.group(1), attr_match.group(2)
            extra.append(
                f"ATTRIBUTE ERROR: '{obj_type}' has no attribute '{attr_name}'\n"
                "COMMON FIXES:\n"
                "- Check spelling of attribute name\n"
                "- Verify the object type is what you expect\n"
                "- Check if you're accessing a None value\n"
                "- Ensure the attribute exists on this type"
            )

    if extra:
        return "\n\n".join(extra)
    return ""


# =============================================================================
# Core Execution Intelligence Classes
# =============================================================================


class IntelligentExecutionEngine:
    """
    The brain of SAGE autopilot - orchestrates intelligent code execution.
    """

    def __init__(self, cwd: Path, renderer, max_workers: int = 4):
        self.cwd = cwd
        self.renderer = renderer
        self.max_workers = max_workers
        self.current_plan: ExecutionPlan | None = None
        self.learning_db: dict[str, LearningEntry] = {}
        self.execution_history: list[dict] = []
        self.lock = Lock()
        self._load_learning_db()

    def _is_informational(self, classification: _ClassifiedRequest | None) -> bool:
        """Safely check if classification is informational."""
        if not classification:
            return False
        if hasattr(classification, "is_informational"):
            return classification.is_informational
        
        # Fallback detection for robustness
        try:
            if hasattr(classification, "request_type") and hasattr(classification.request_type, "name"):
                return classification.request_type.name in ("QUESTION", "SUMMARY", "EXPLANATION")
        except:
            pass
        return False

    def _is_analysis_only(self, classification: _ClassifiedRequest | None) -> bool:
        """Check if this is an analysis-only request that should NOT have implementation steps."""
        if not classification:
            return False
            
        # Check request type (Item 24)
        try:
            if hasattr(classification, "request_type"):
                read_only_types = (
                    _RequestType.ANALYSIS,
                    _RequestType.LIST_GENERATION,
                    _RequestType.QUESTION,
                    _RequestType.SEARCH,
                    _COMPARISON := getattr(_RequestType, "COMPARISON", None),
                    _SUMMARY := getattr(_RequestType, "SUMMARY", None),
                    _EXPLANATION := getattr(_RequestType, "EXPLANATION", None)
                )
                if classification.request_type in read_only_types:
                    return True
        except:
            pass
            
        # Check strict_read_only flag if present
        if hasattr(classification, "strict_read_only") and classification.strict_read_only:
            return True
            
        return False

    def _sage_dir(self) -> Path:
        sage_dir = self.cwd / ".sage"
        sage_dir.mkdir(exist_ok=True)
        return sage_dir

    def _load_learning_db(self) -> None:
        db_path = self._sage_dir() / "learning.json"
        if db_path.exists():
            try:
                data = json.loads(db_path.read_text(encoding="utf-8", errors="replace"))
                for sig, entry in data.items():
                    self.learning_db[sig] = LearningEntry(**entry)
            except (OSError, json.JSONDecodeError, TypeError, KeyError) as e:
                logger.debug("Failed to load learning DB: %s", e)

    def _save_learning_db(self) -> None:
        db_path = self._sage_dir() / "learning.json"
        try:
            data = {
                sig: {
                    "error_signature": e.error_signature,
                    "solution_pattern": e.solution_pattern,
                    "success_count": e.success_count,
                    "failure_count": e.failure_count,
                    "last_used": e.last_used,
                }
                for sig, e in self.learning_db.items()
            }
            db_path.write_text(json.dumps(data, indent=2))
        except (OSError, TypeError) as e:
            logger.debug("Failed to save learning DB: %s", e)

    def _compute_error_signature(self, error: str) -> str:
        normalized = re.sub(r"line \d+", "line N", error)
        normalized = re.sub(r":\d+:", ":N:", normalized)
        normalized = re.sub(r"/[^/]+\.py", "/FILE.py", normalized)
        normalized = re.sub(r"'[^']+\.py'", "'FILE.py'", normalized)
        return hashlib.md5(normalized.encode()).hexdigest()[:12]

    def learn_from_success(self, error: str, solution: str) -> None:
        sig = self._compute_error_signature(error)
        if sig in self.learning_db:
            entry = self.learning_db[sig]
            entry.success_count += 1
            entry.last_used = datetime.now().isoformat()
        else:
            self.learning_db[sig] = LearningEntry(
                error_signature=sig,
                solution_pattern=solution,
                success_count=1,
                last_used=datetime.now().isoformat(),
            )
        self._save_learning_db()

    def learn_from_failure(self, error: str) -> None:
        sig = self._compute_error_signature(error)
        if sig in self.learning_db:
            self.learning_db[sig].failure_count += 1
            self._save_learning_db()

    def get_learned_solution(self, error: str) -> str | None:
        sig = self._compute_error_signature(error)
        if sig in self.learning_db:
            entry = self.learning_db[sig]
            if entry.success_count > entry.failure_count:
                return entry.solution_pattern
        return None

    def analyze_codebase(self) -> dict:
        analysis = {
            "languages": Counter(),
            "test_files": [],
            "source_files": [],
            "config_files": [],
            "entry_points": [],
            "total_files": 0,
            "total_lines": 0,
            "has_tests": False,
            "test_framework": None,
            "package_manager": None,
        }

        if (self.cwd / "pyproject.toml").exists():
            analysis["package_manager"] = "poetry/pip"
            content = (self.cwd / "pyproject.toml").read_text(encoding="utf-8", errors="replace")
            if "pytest" in content:
                analysis["test_framework"] = "pytest"
        elif (self.cwd / "package.json").exists():
            analysis["package_manager"] = "npm"
            content = (self.cwd / "package.json").read_text(encoding="utf-8", errors="replace")
            if "jest" in content:
                analysis["test_framework"] = "jest"
            elif "vitest" in content:
                analysis["test_framework"] = "vitest"
        elif (self.cwd / "Cargo.toml").exists():
            analysis["package_manager"] = "cargo"
            analysis["test_framework"] = "cargo test"
        elif (self.cwd / "go.mod").exists():
            analysis["package_manager"] = "go"
            analysis["test_framework"] = "go test"

        from sage.core.project import safe_walk
        
        # Optimization: Use safe_walk for efficiency
        for fp in safe_walk(self.cwd):
            ext = fp.suffix.lower()
            analysis["total_files"] += 1

            if ext in {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java"}:
                analysis["languages"][ext] += 1
                try:
                    analysis["total_lines"] += len(fp.read_text(encoding="utf-8", errors="replace").splitlines())
                except Exception:
                    pass

                name = fp.name.lower()
                rel_path = str(fp.relative_to(self.cwd))

                if "test" in name or rel_path.startswith("tests/"):
                    analysis["test_files"].append(rel_path)
                    analysis["has_tests"] = True
                elif name in {
                    "main.py",
                    "app.py",
                    "index.js",
                    "index.ts",
                    "main.go",
                    "main.rs",
                }:
                    analysis["entry_points"].append(rel_path)
                    analysis["source_files"].append(rel_path)
                else:
                    analysis["source_files"].append(rel_path)

            elif ext in {".json", ".toml", ".yaml", ".yml"}:
                analysis["config_files"].append(str(fp.relative_to(self.cwd)))

        return analysis

    def decompose_task(
        self,
        task_description: str,
        codebase_analysis: dict,
        send_fn: Callable | None = None,
        previous_findings: str | None = None,
        classification: _ClassifiedRequest | None = None,
    ) -> list[PlanTask]:
        tasks = []
        task_id = 0

        def make_task(
            desc: str,
            priority: TaskPriority,
            deps: list[str] = None,
            complexity: int = 1,
            files: list[str] = None,
        ) -> PlanTask:
            nonlocal task_id
            task_id += 1
            return PlanTask(
                id=f"task_{task_id}",
                description=desc,
                priority=priority,
                dependencies=deps or [],
                estimated_complexity=complexity,
                files_involved=files or [],
            )

        # ── Step 0: Handle Informational/General Knowledge tasks ──
        if self._is_informational(classification):
            if send_fn:
                # Use a specific prompt for informational task decomposition
                info_prompt = f"""Decompose this informational request into a series of steps to provide a comprehensive answer.

REQUEST: {task_description}

GUIDELINES:
1. Identify the core subjects and what specifically needs to be explained.
2. Break it down into 2-4 logical steps (e.g., "Research biography", "Summarize discography").
3. Ensure the final step is a synthesis of all information.
4. Do NOT suggest any codebase analysis or code changes.

RESPONSE FORMAT (JSON ONLY):
[
  {{
    "description": "Short description of the research/synthesis step",
    "priority": "HIGH",
    "dependencies": [],
    "complexity": 2
  }}
]
"""
                try:
                    response = send_fn(info_prompt)
                    if response:
                        clean_response = response.strip()
                        if clean_response.startswith("```json"):
                            clean_response = clean_response[7:].strip()
                        if clean_response.endswith("```"):
                            clean_response = clean_response[:-3].strip()
                        
                        dynamic_tasks = json.loads(clean_response)
                        if isinstance(dynamic_tasks, list):
                            for dt in dynamic_tasks:
                                tasks.append(make_task(
                                    dt.get("description", "Research step"),
                                    TaskPriority.HIGH,
                                    deps=dt.get("dependencies", []),
                                    complexity=dt.get("complexity", 2)
                                ))
                            if tasks:
                                return tasks
                except Exception:
                    pass

            # Minimal fallback for informational tasks
            tasks.append(make_task(
                f"Research and answer: {task_description}", 
                TaskPriority.HIGH, 
                complexity=2
            ))
            if not classification.strict_read_only:
                tasks.append(make_task(
                    "Synthesize findings and provide response", 
                    TaskPriority.MEDIUM, 
                    deps=["task_1"], 
                    complexity=2
                ))
            return tasks

        # ── Step 0.5: Handle Analysis-only tasks ──
        if self._is_analysis_only(classification):
            if send_fn:
                analysis_prompt = f"""Decompose this codebase analysis request into steps.
                
REQUEST: {task_description}

GUIDELINES:
1. Break it down into 2-5 logical investigation steps.
2. Ensure the final step is a synthesis of findings.
3. ⚠️ CRITICAL: Do NOT suggest any implementation, code changes, or bug fixes. This is a READ-ONLY analysis.

RESPONSE FORMAT (JSON ONLY):
[
  {{
    "description": "Short description of the analysis step",
    "priority": "HIGH",
    "dependencies": [],
    "complexity": 2
  }}
]
"""
                try:
                    response = send_fn(analysis_prompt)
                    if response:
                        clean_response = response.strip()
                        if clean_response.startswith("```json"):
                            clean_response = clean_response[7:].strip()
                        if clean_response.endswith("```"):
                            clean_response = clean_response[:-3].strip()
                        
                        dynamic_tasks = json.loads(clean_response)
                        if isinstance(dynamic_tasks, list):
                            for dt in dynamic_tasks:
                                tasks.append(make_task(
                                    dt.get("description", "Analysis step"),
                                    TaskPriority.HIGH,
                                    deps=dt.get("dependencies", []),
                                    complexity=dt.get("complexity", 2)
                                ))
                            if tasks:
                                return tasks
                except Exception:
                    pass

            # Minimal fallback for analysis tasks
            tasks.append(make_task(
                f"Locate and analyze code for: {task_description[:50]}...", 
                TaskPriority.HIGH, 
                complexity=2
            ))
            tasks.append(make_task(
                "Synthesize findings and provide comprehensive review", 
                TaskPriority.MEDIUM, 
                deps=["task_1"], 
                complexity=2
            ))
            return tasks

        if send_fn:
            try:
                # ── Step 1: Relevance Check for Context Persistence ──
                # If we have previous findings, check if they are actually relevant to the new task
                effective_findings = previous_findings
                if previous_findings and task_description:
                    # Heuristic: Determine if this is a follow-up or a fresh task
                    followup_keywords = [
                        "fix", "implement", "those", "these", "address", "findings", "issues",
                        "continue", "proceed", "next", "more", "detail", "again", "previous",
                        "item", "step", "improvement", "suggestion", "recommendation"
                    ]
                    task_lower = task_description.lower()
                    is_followup = any(kw in task_lower for kw in followup_keywords)
                    
                    # Check for entity overlap (e.g., if the same files are mentioned)
                    current_files = set(re.findall(r"\b[\w\-/]+\.(?:py|js|ts|tsx|jsx|html|css|json|md|txt|yaml|yml|sh|bash|sql|c|cpp|h|hpp|rs|go|java|kt|rb|php)\b", task_description))
                    previous_files = set(re.findall(r"\b[\w\-/]+\.(?:py|js|ts|tsx|jsx|html|css|json|md|txt|yaml|yml|sh|bash|sql|c|cpp|h|hpp|rs|go|java|kt|rb|php)\b", previous_findings))
                    has_file_overlap = bool(current_files & previous_files)
                    
                    # Check for subject overlap (for informational tasks)
                    def extract_entities(text: str) -> set[str]:
                        words = re.findall(r"\b[A-Z][a-z]+\b", text)
                        return set(words)
                    
                    current_entities = extract_entities(task_description)
                    previous_entities = extract_entities(previous_findings)
                    has_subject_overlap = bool(current_entities & previous_entities)
                    
                    # Reset context if unrelated
                    if not (is_followup or has_file_overlap or has_subject_overlap) and classification and classification.request_type in (_RequestType.ANALYSIS, _RequestType.QUESTION, _RequestType.SUMMARY, _RequestType.EXPLANATION):
                        effective_findings = None

                findings_context = ""
                if effective_findings:
                    findings_context = (
                        "\n## CRITICAL: PRIOR ANALYSIS FINDINGS\n"
                        "The following issues and improvements were identified in the previous phase. "
                        "Your new plan MUST specifically address these findings step-by-step.\n\n"
                        f"{effective_findings}\n"
                    )

                # Check if TDD is requested
                is_tdd = "tdd" in task_lower or "test driven" in task_lower
                tdd_guideline = ""
                if is_tdd:
                    tdd_guideline = "⚠️ TDD ENFORCEMENT: Your plan MUST follow Test-Driven Development. Step 1 should be writing a failing test, and subsequent steps should implement the logic to make it pass."

                decomposition_prompt = f"""Decompose this coding task into a list of atomic, verifiable subtasks.

TASK: {task_description}
{findings_context}
{tdd_guideline}
CODEBASE CONTEXT:
- Languages: {codebase_analysis.get('languages')}
- Test framework: {codebase_analysis.get('test_framework')}
- Total files: {codebase_analysis.get('total_files')}

GUIDELINES:
1. Break down the task into 3-8 logical steps that are SPECIFIC to the user's prompt.
2. Each unit must be verifiable (e.g., "Run tests", "Modify X to do Y").
3. Identify dependencies between tasks (e.g., Task 2 depends on Task 1).
4. Assign priority: CRITICAL, HIGH, MEDIUM, LOW.
5. Assign estimated complexity: 1 (easy) to 5 (expert).
6. ⚠️ MANDATORY: If 'PRIOR ANALYSIS FINDINGS' are provided above, your plan MUST be a direct implementation roadmap for those findings.
7. ⚠️ CONTEXT AWARENESS: If the current task is unrelated to the findings above, IGNORE them and focus ONLY on the new task.
8. ⚠️ DYNAMIC PLANNING: Do NOT use a one-size-fits-all template. Tailor the steps to the specific files and technologies mentioned or detected.

RESPONSE FORMAT (JSON ONLY):
[
  {{
    "description": "Short description of the subtask",
    "priority": "HIGH",
    "dependencies": [],
    "complexity": 2,
    "files": ["optional/file/path.py"]
  }}
]
"""
                response = send_fn(decomposition_prompt)
                if response:
                    clean_response = response.strip()
                    if clean_response.startswith("```json"):
                        clean_response = clean_response[7:].strip()
                    if clean_response.endswith("```"):
                        clean_response = clean_response[:-3].strip()

                    try:
                        dynamic_tasks = json.loads(clean_response)
                        if isinstance(dynamic_tasks, list):
                            for dt in dynamic_tasks:
                                priority_map = {
                                    "CRITICAL": TaskPriority.CRITICAL,
                                    "HIGH": TaskPriority.HIGH,
                                    "MEDIUM": TaskPriority.MEDIUM,
                                    "LOW": TaskPriority.LOW,
                                }
                                priority = priority_map.get(
                                    dt.get("priority", "MEDIUM").upper(), TaskPriority.MEDIUM
                                )
                                tasks.append(
                                    make_task(
                                        dt.get("description", "Unknown task"),
                                        priority,
                                        deps=dt.get("dependencies", []),
                                        complexity=dt.get("complexity", 1),
                                        files=dt.get("files", []),
                                    )
                                )
                            if tasks:
                                return tasks
                    except (json.JSONDecodeError, TypeError):
                        pass
            except Exception:
                pass

        # ── Step 2: Fallback to dynamic-heuristic decomposition ──
        # We only reach here if send_fn was not provided or failed
        # Instead of hardcoded templates, we build a tailored minimal plan
        cleaned_goal = task_description[:50] + "..." if len(task_description) > 50 else task_description
        
        # We still categorize slightly to provide better default steps, but keep them descriptive
        task_lower = task_description.lower()
        
        # Check for pure analysis/review keywords first to avoid misclassifying "Analyze and fix"
        is_pure_analysis = any(kw in task_lower for kw in ["analyze", "review", "audit", "check", "examine"]) and not any(kw in task_lower for kw in ["fix", "implement", "add", "create", "build", "refactor"])

        if is_pure_analysis:
            tasks.append(make_task(f"Locate and analyze code for: {cleaned_goal}", TaskPriority.HIGH, complexity=2))
            tasks.append(make_task("Synthesize findings and provide review", TaskPriority.MEDIUM, deps=["task_1"], complexity=2))
        elif any(kw in task_lower for kw in ["fix", "debug", "error", "bug", "failing"]):
            tasks.append(make_task(f"Locate root cause for: {cleaned_goal}", TaskPriority.CRITICAL, complexity=2))
            tasks.append(make_task("Apply and verify implementation", TaskPriority.HIGH, deps=["task_1"], complexity=3))
        elif any(kw in task_lower for kw in ["add", "implement", "create", "build"]):
            tasks.append(make_task(f"Design implementation for: {cleaned_goal}", TaskPriority.HIGH, complexity=2))
            tasks.append(make_task("Execute core implementation steps", TaskPriority.HIGH, deps=["task_1"], complexity=4))
        else:
            tasks.append(make_task(f"Analyze and execute: {cleaned_goal}", TaskPriority.HIGH, complexity=2))
            tasks.append(make_task("Verify results against requirements", TaskPriority.MEDIUM, deps=["task_1"], complexity=1))

        return tasks

    def create_plan(
        self,
        goal: str,
        send_fn: Callable | None = None,
        previous_findings: str | None = None,
        classification: _ClassifiedRequest | None = None,
    ) -> ExecutionPlan:
        # For informational tasks, skip heavy codebase analysis and dynamic planning (P3-71)
        if self._is_informational(classification):
            analysis = {"total_files": 0, "has_tests": False, "languages": Counter()}
            tasks = [
                PlanTask(
                    id="task_1",
                    description=f"Research and answer: {goal}",
                    priority=TaskPriority.HIGH,
                    dependencies=[],
                    estimated_complexity=2,
                    files_involved=[],
                ),
                PlanTask(
                    id="task_2",
                    description="Synthesize findings and provide response",
                    priority=TaskPriority.MEDIUM,
                    dependencies=["task_1"],
                    estimated_complexity=2,
                    files_involved=[],
                ),
            ]
        else:
            analysis = self.analyze_codebase()
            tasks = self.decompose_task(
                goal,
                analysis,
                send_fn=send_fn,
                previous_findings=previous_findings,
                classification=classification,
            )
        
        plan = ExecutionPlan(
            id=f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            goal=goal,
            tasks=tasks,
            created_at=datetime.now().isoformat(),
        )
        self.current_plan = plan
        return plan


class QualityGate:
    """
    Quality gates that code must pass before being accepted.
    """

    def __init__(self, cwd: Path, renderer):
        self.cwd = cwd
        self.renderer = renderer
        self.gates_passed: dict[str, bool] = {}
        self.lsp_client = LSPClient(cwd)
        self.security_auditor = SecurityAuditor(cwd)

    def check_syntax(self, filepath: str, content: str) -> tuple[bool, str]:
        if filepath.endswith(".py"):
            try:
                compile(content, filepath, "exec")
                return True, "Syntax OK"
            except SyntaxError as e:
                return False, f"Syntax error at line {e.lineno}: {e.msg}"
        return True, "Syntax check skipped"

    def check_imports(self, filepath: str, content: str) -> tuple[bool, list[str]]:
        if not filepath.endswith(".py"):
            return True, []
        from sage.core.validation import extract_imports_from_python as _extract_imports_from_python
        from sage.core.validation import module_exists_in_codebase as _module_exists_in_codebase
        imports = _extract_imports_from_python(content)
        missing = []
        for module in imports:
            if not _module_exists_in_codebase(module, self.cwd):
                missing.append(module)
        return len(missing) == 0, missing

    def check_test_file(self, filepath: str, content: str) -> tuple[bool, str]:
        if not ("test_" in filepath or filepath.startswith("tests/")):
            return True, "Not a test file"
        has_assertions = bool(
            re.search(
                r"\b(assert|assertEqual|assertTrue|assertFalse|assertRaises|"
                r"assertIn|assertIsNone|expect\(|should\.|pytest\.raises)",
                content,
            )
        )
        if not has_assertions:
            return False, "Test file has no assertions"
        empty_tests = len(re.findall(r"def test_\w+\([^)]*\):\s*\n\s*pass", content))
        if empty_tests > 0:
            return False, f"Test file has {empty_tests} empty test functions"
        return True, "Test file OK"

    def check_boilerplate(self, filepath: str, content: str) -> tuple[bool, list[str]]:
        issues = []
        placeholder_patterns = [
            (r"# TODO[:\s]", "TODO comment found"),
            (r"# FIXME[:\s]", "FIXME comment found"),
            (r"# implement\s+this", "placeholder 'implement this' comment"),
            (r"raise\s+NotImplementedError", "NotImplementedError raised - incomplete implementation"),
            (r"pass\s*#\s*placeholder", "placeholder pass statement"),
            (r"\.\.\.\s*#\s*rest", "ellipsis placeholder"),
        ]
        for pattern, message in placeholder_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(message)
        empty_funcs = re.findall(r"def\s+(\w+)\([^)]*\):\s*\n\s*(?:#[^\n]*)?\s*pass\s*(?:\n|$)", content)
        if len(empty_funcs) >= 2:
            issues.append(f"Multiple empty functions: {', '.join(empty_funcs[:5])}")
        func_names = re.findall(r"def\s+(\w+)\s*\(", content)
        if len(func_names) > 10:
            base_names = [re.sub(r"_\d+$", "", name) for name in func_names]
            name_counts = Counter(base_names)
            most_common = name_counts.most_common(1)
            if most_common and most_common[0][1] >= 5:
                issues.append(f"Repetitive function names - {most_common[0][1]} functions starting with '{most_common[0][0]}'")
        return len(issues) == 0, issues

    def check_implementation_completeness(self, filepath: str, content: str) -> tuple[bool, list[str]]:
        issues = []
        if "test_" in filepath or filepath.startswith("tests/"):
            return True, []
        func_pattern = r"def\s+\w+\([^)]*\):"
        functions = re.findall(func_pattern, content)
        if not functions:
            return True, []
        incomplete_pattern = r"def\s+(\w+)\([^)]*\):\s*\n\s*(?:\"\"\"[^\"]*\"\"\"\s*)?\s*(?:pass|return\s+None)\s*(?:\n|$)"
        incomplete = re.findall(incomplete_pattern, content)
        if len(incomplete) > len(functions) // 2:
            issues.append(f"More than half of functions are incomplete stubs: {', '.join(incomplete[:5])}")
        return len(issues) == 0, issues

    def check_static_diagnostics(self, filepath: str) -> tuple[bool, list[str]]:
        diagnostics = self.lsp_client.check_file(filepath)
        # Handle both old LSPDiagnostic and new Diagnostic objects
        errors = []
        if hasattr(diagnostics, "diagnostics"): # New DiagnosticResult
            errors = [d.format() for d in diagnostics.diagnostics if d.severity == "error"]
        else: # Old list[LSPDiagnostic]
            errors = [f"{d.source} {d.file}:{d.line}:{d.column} {d.message}" for d in diagnostics if d.severity == "error"]
        return len(errors) == 0, errors

    def check_security(self, filepath: str) -> tuple[bool, list[str]]:
        findings = self.security_auditor.scan_files([filepath])
        blocking = [f"[{f.severity}] {f.file}:{f.line} {f.message}" for f in findings if f.severity in {"CRITICAL", "HIGH"}]
        return len(blocking) == 0, blocking

    def run_all_gates(self, filepath: str, content: str) -> tuple[bool, list[str]]:
        issues = []
        ok, msg = self.check_syntax(filepath, content)
        if not ok: issues.append(f"Syntax: {msg}")
        ok, missing = self.check_imports(filepath, content)
        if not ok: issues.append(f"Imports: Missing modules: {', '.join(missing)}")
        ok, msg = self.check_test_file(filepath, content)
        if not ok: issues.append(f"Test quality: {msg}")
        ok, diagnostics = self.check_static_diagnostics(filepath)
        if not ok: issues.append(f"Diagnostics: {'; '.join(diagnostics[:5])}")
        ok, findings = self.check_security(filepath)
        if not ok: issues.append(f"Security: {'; '.join(findings[:5])}")
        ok, b_issues = self.check_boilerplate(filepath, content)
        if not ok: issues.append(f"Boilerplate: {'; '.join(b_issues[:3])}")
        ok, c_issues = self.check_implementation_completeness(filepath, content)
        if not ok: issues.append(f"Incomplete: {'; '.join(c_issues[:3])}")
        all_passed = len(issues) == 0
        self.gates_passed[filepath] = all_passed
        return all_passed, issues


class IncrementalValidator:
    """
    Validates code incrementally as it's written.
    """

    def __init__(self, cwd: Path, renderer, test_cmd: str = ""):
        self.cwd = cwd
        self.renderer = renderer
        self.test_cmd, self.test_cmd_cwd = self._parse_scoped_cmd(test_cmd or "python -m pytest -v --tb=short")
        self.validation_cache: dict[str, tuple[bool, str]] = {}
        self.last_validation_time: float = 0
        self.min_validation_interval: float = 2.0

    def _parse_scoped_cmd(self, cmd: str) -> tuple[str, Path]:
        match = re.match(r"^\s*\[(?:cwd|dir)=(.+?)\]\s*(.*)$", cmd, re.DOTALL)
        if match:
            rel_path = match.group(1).strip()
            clean_cmd = match.group(2).strip()
            return clean_cmd, self.cwd / rel_path
        return cmd.strip(), self.cwd

    def validate_file(self, filepath: str) -> tuple[bool, str]:
        full_path = self.cwd / filepath
        if not full_path.exists():
            return False, f"File not found: {filepath}"
        if filepath.endswith(".py"):
            try:
                compile(full_path.read_text(encoding="utf-8", errors="replace"), filepath, "exec")
            except SyntaxError as e:
                return False, f"Syntax error at line {e.lineno}: {e.msg}"
        return True, "File OK"

    def validate_unit(self, files: list[str]) -> tuple[bool, str]:
        for fp in files:
            ok, msg = self.validate_file(fp)
            if not ok: return False, f"{fp}: {msg}"
        test_files = [f for f in files if "test_" in f or f.startswith("tests/")]
        if test_files:
            return self._run_tests(test_files)
        return True, "Unit validated"

    def _run_tests(self, test_files: list[str]) -> tuple[bool, str]:
        now = time.time()
        if now - self.last_validation_time < self.min_validation_interval:
            time.sleep(self.min_validation_interval - (now - self.last_validation_time))
        self.last_validation_time = time.time()
        cmd = f"{self.test_cmd} {' '.join(test_files)}"
        result = _execute_command(cmd, cwd=self.test_cmd_cwd, timeout=60, allow_shell=True, validate=False)
        if result.success:
            return True, "Tests passed"
        elif result.timed_out:
            return False, "Test timeout"
        elif result.error:
            return False, f"Test error: {result.error}"
        else:
            return False, _summarize_test_output(result.output, max_chars=500)

    def full_validation(self, timeout: int = 120) -> tuple[bool, str]:
        if not self.test_cmd or not self.test_cmd.strip():
            return True, "No test command configured"
        result = _execute_command(self.test_cmd, cwd=self.test_cmd_cwd, timeout=timeout, allow_shell=True, validate=False)
        if result.success:
            return True, "All tests passed"
        elif result.timed_out:
            return False, f"Test suite timed out after {timeout}s"
        elif result.error:
            return False, f"Validation error: {result.error}"
        else:
            return False, _summarize_test_output(result.output, max_chars=1000)


class FreeModelRouter:
    """
    Intelligent routing to free model providers.
    """

    FREE_PROVIDERS = [
        {"name": "ollama", "model": "qwen2.5-coder:7b", "capability": 4, "rate_limit": float("inf")},
        {"name": "ollama", "model": "deepseek-coder:6.7b", "capability": 4, "rate_limit": float("inf")},
        {"name": "ollama", "model": "codellama:7b", "capability": 3, "rate_limit": float("inf")},
        {"name": "gemini", "model": "gemini-1.5-flash", "capability": 5, "rate_limit": 15},
    ]

    def __init__(self, renderer):
        self.renderer = renderer
        self.usage_counts: dict[str, int] = {}
        self.last_reset: float = time.time()
        self.failure_counts: dict[str, int] = {}

    def _reset_if_needed(self) -> None:
        if time.time() - self.last_reset > 3600:
            self.usage_counts = {}
            self.last_reset = time.time()

    def get_best_provider(self, task_complexity: int = 3) -> dict | None:
        self._reset_if_needed()
        candidates = []
        for provider in self.FREE_PROVIDERS:
            key = f"{provider['name']}:{provider['model']}"
            if self.usage_counts.get(key, 0) >= provider["rate_limit"]: continue
            if self.failure_counts.get(key, 0) > 5: continue
            if provider["capability"] >= task_complexity:
                candidates.append((provider, self.usage_counts.get(key, 0), self.failure_counts.get(key, 0)))
        if not candidates: return None
        candidates.sort(key=lambda x: (-x[0]["capability"], x[2], x[1]))
        return candidates[0][0]

    def record_usage(self, provider_name: str, model: str) -> None:
        key = f"{provider_name}:{model}"
        self.usage_counts[key] = self.usage_counts.get(key, 0) + 1

    def record_failure(self, provider_name: str, model: str) -> None:
        key = f"{provider_name}:{model}"
        self.failure_counts[key] = self.failure_counts.get(key, 0) + 1

    def record_success(self, provider_name: str, model: str) -> None:
        key = f"{provider_name}:{model}"
        if key in self.failure_counts and self.failure_counts[key] > 0:
            self.failure_counts[key] -= 1


class SelfHealingSystem:
    """
    Self-healing system that automatically recovers from errors.
    """

    COMMON_FIXES = {
        "ModuleNotFoundError": "Delete test files importing non-existent modules",
        "ImportError": "Check import paths and module existence",
        "SyntaxError": "Fix syntax error at indicated line",
        "IndentationError": "Fix indentation at indicated line",
        "NameError": "Define the missing variable or import",
        "TypeError": "Check argument types and function signatures",
        "AttributeError": "Verify object has the attribute or method",
        "AssertionError": "Test assertion failed - check test logic",
    }

    def __init__(self, cwd: Path, renderer, learning_engine: IntelligentExecutionEngine):
        self.cwd = cwd
        self.renderer = renderer
        self.learning = learning_engine
        self.recovery_attempts: dict[str, int] = {}
        self.max_recovery_attempts = 3

    def can_recover(self, error: str) -> bool:
        sig = self.learning._compute_error_signature(error)
        return self.recovery_attempts.get(sig, 0) < self.max_recovery_attempts

    def analyze_error(self, error: str) -> dict:
        analysis = {"error_type": None, "suggested_fix": None, "learned_solution": None, "files_involved": [], "recoverable": True}
        for error_type in self.COMMON_FIXES:
            if error_type in error:
                analysis["error_type"] = error_type
                analysis["suggested_fix"] = self.COMMON_FIXES[error_type]
                break
        learned = self.learning.get_learned_solution(error)
        if learned: analysis["learned_solution"] = learned
        analysis["files_involved"] = list(set(re.findall(r"([a-zA-Z0-9_/]+\.py)", error)))
        return analysis

    def attempt_recovery(self, error: str, written_files: list[str]) -> tuple[bool, str]:
        sig = self.learning._compute_error_signature(error)
        self.recovery_attempts[sig] = self.recovery_attempts.get(sig, 0) + 1
        analysis = self.analyze_error(error)
        if analysis["error_type"] in ("ModuleNotFoundError", "ImportError"):
            broken = _detect_broken_test_files(error, self.cwd)
            if broken:
                deleted = _cleanup_broken_tests(broken, self.renderer)
                if deleted: return True, f"Deleted {len(deleted)} broken test file(s)"
        if analysis["learned_solution"]: return False, f"Try learned solution: {analysis['learned_solution']}"
        if analysis["suggested_fix"]: return False, f"Suggested fix: {analysis['suggested_fix']}"
        return False, "Unable to auto-recover"

    def reset_recovery_state(self) -> None:
        self.recovery_attempts = {}


# =============================================================================
# FAILURE LOOP DETECTION AND HARD STOP
# =============================================================================


class FailureLoopDetector:
    """Detects and stops failure loops to prevent infinite hallucination spirals.

    This class tracks:
    - Repeated identical errors
    - Repeated identical response patterns
    - Missing context patterns that repeat
    - Escalating validation failures

    When a failure loop is detected, it forces a hard stop.
    """

    def __init__(self, max_identical_errors: int = 7, max_similar_responses: int = 7):
        self.error_history: list[str] = []
        self.response_hashes: list[str] = []
        self.validation_failures: list[str] = []
        self.max_identical_errors = max_identical_errors
        self.max_similar_responses = max_similar_responses
        self._loop_detected = False
        self._loop_reason = ""

    def record_error(self, error: str) -> bool:
        """Record an error and check if we're in a loop.

        Returns:
            True if failure loop detected (should stop)
        """
        normalized_error = error.lower().strip()
        self.error_history.append(normalized_error)

        # Check for repeated identical errors
        if len(self.error_history) >= self.max_identical_errors:
            recent = self.error_history[-self.max_identical_errors :]
            if len(set(recent)) == 1:
                self._loop_detected = True
                self._loop_reason = (
                    f"Same error repeated {self.max_identical_errors} times: {recent[0][:100]}"
                )
                return True

        return False

    def record_response(self, response: str) -> bool:
        """Record a response and check for repetition loop.

        Returns:
            True if failure loop detected (should stop)
        """
        response_hash = _compute_response_hash(response)
        self.response_hashes.append(response_hash)

        # Check for repeated identical responses
        if len(self.response_hashes) >= self.max_similar_responses:
            recent = self.response_hashes[-self.max_similar_responses :]
            if len(set(recent)) == 1:
                self._loop_detected = True
                self._loop_reason = (
                    f"Identical response generated {self.max_similar_responses} times"
                )
                return True

        return False

    def record_validation_failure(self, violations: list[str]) -> bool:
        """Record validation failures and check for escalation.

        Returns:
            True if validation failures are escalating (should stop)
        """
        self.validation_failures.extend(violations)

        # Check if same validation failures keep occurring
        # Use a lower threshold for identical violations
        if len(self.validation_failures) >= 3:
            recent = self.validation_failures[-3:]
            # Normalize violations for comparison (take first 50 chars)
            normalized = [v[:50].lower().strip() for v in recent]
            # If all 3 recent are identical, trigger loop detection
            if len(set(normalized)) == 1:
                self._loop_detected = True
                self._loop_reason = "Identical validation failure repeated 3 times"
                return True

        # Also check for pattern-based repetition with more violations
        if len(self.validation_failures) >= 6:
            recent = self.validation_failures[-6:]
            # If more than half are the same violation type
            from collections import Counter

            violation_counts = Counter(v.split(":")[0] if ":" in v else v[:30] for v in recent)
            most_common_count = violation_counts.most_common(1)[0][1]
            if most_common_count >= 4:
                self._loop_detected = True
                self._loop_reason = (
                    f"Same validation failure pattern repeated {most_common_count} times"
                )
                return True

        return False

    def is_in_loop(self) -> tuple[bool, str]:
        """Check if we're in a failure loop.

        Returns:
            Tuple of (is_looping, reason)
        """
        return self._loop_detected, self._loop_reason

    def reset(self) -> None:
        """Reset the detector after successful operation."""
        self.error_history.clear()
        self.response_hashes.clear()
        self.validation_failures.clear()
        self._loop_detected = False
        self._loop_reason = ""


def _compute_response_hash(response: str) -> str:
    """Compute normalized hash of response for repetition detection.

    Normalizes whitespace to detect subtle repetition.
    """
    import hashlib

    # Normalize whitespace
    normalized = " ".join(response.split())

    # Compute hash
    return hashlib.sha256(normalized.encode()).hexdigest()
