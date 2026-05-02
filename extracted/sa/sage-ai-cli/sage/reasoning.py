"""Advanced Reasoning Engine for SAGE.

This module provides sophisticated reasoning capabilities including:
- Chain-of-thought reasoning
- Structured problem decomposition
- Self-reflection and validation
- Multi-perspective analysis
- Hypothesis testing
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ReasoningPhase(Enum):
    """Phases of the reasoning process."""

    UNDERSTAND = "understand"  # Comprehend the problem
    DECOMPOSE = "decompose"  # Break into sub-problems
    ANALYZE = "analyze"  # Examine constraints and requirements
    HYPOTHESIZE = "hypothesize"  # Form potential solutions
    EVALUATE = "evaluate"  # Assess solutions
    SYNTHESIZE = "synthesize"  # Combine into final approach
    VALIDATE = "validate"  # Verify correctness
    REFLECT = "reflect"  # Learn from the process


@dataclass
class ReasoningStep:
    """A single step in the reasoning chain."""

    phase: ReasoningPhase
    thought: str
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.5
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Hypothesis:
    """A hypothesis about the solution."""

    id: str
    description: str
    approach: str
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    confidence: float = 0.5
    validated: bool = False
    validation_result: str | None = None


@dataclass
class ProblemAnalysis:
    """Structured analysis of a problem."""

    original_task: str
    goals: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    edge_cases: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)


@dataclass
class SubTask:
    """A decomposed sub-task."""

    id: str
    description: str
    type: str  # research, implementation, testing, validation
    priority: int  # 1-5, 1 being highest
    complexity: int  # 1-5
    dependencies: list[str] = field(default_factory=list)
    files_involved: list[str] = field(default_factory=list)
    verification_method: str = ""
    status: str = "pending"  # pending, in_progress, completed, blocked
    result: str | None = None


@dataclass
class ReasoningContext:
    """Full context for reasoning about a task."""

    task: str
    analysis: ProblemAnalysis | None = None
    subtasks: list[SubTask] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    reasoning_chain: list[ReasoningStep] = field(default_factory=list)
    selected_approach: Hypothesis | None = None
    files_read: set[str] = field(default_factory=set)
    files_modified: list[str] = field(default_factory=list)
    errors_encountered: list[str] = field(default_factory=list)
    learnings: list[str] = field(default_factory=list)


class ChainOfThoughtReasoner:
    """Implements chain-of-thought reasoning for complex problem solving."""

    # Prompt templates for each reasoning phase
    PHASE_PROMPTS = {
        ReasoningPhase.UNDERSTAND: """
## Task Understanding Phase
Analyze this task deeply:

**Task:** {task}

Think through:
1. What is the core objective? State it in one sentence.
2. What domain knowledge is required?
3. What are the explicit requirements?
4. What are the implicit requirements?
5. What would success look like?

Format your understanding as:
OBJECTIVE: [one sentence core goal]
REQUIREMENTS:
- [explicit requirement 1]
- [implicit requirement 1]
SUCCESS_CRITERIA:
- [criterion 1]
""",
        ReasoningPhase.DECOMPOSE: """
## Problem Decomposition Phase

Break down this task into atomic, verifiable sub-tasks:

**Task:** {task}
**Objective:** {objective}

For each sub-task, specify:
1. What needs to be done (action)
2. What type it is (research/implementation/testing/validation)
3. What it depends on
4. How to verify completion

Format as:
SUBTASK_1:
  action: [what to do]
  type: [research|implementation|testing|validation]
  depends_on: [subtask IDs or "none"]
  verify: [how to check completion]
""",
        ReasoningPhase.ANALYZE: """
## Deep Analysis Phase

Analyze the constraints and requirements:

**Task:** {task}
**Sub-tasks:** {subtasks}

Identify:
1. CONSTRAINTS: What limitations exist?
2. ASSUMPTIONS: What are we taking for granted?
3. RISKS: What could go wrong?
4. EDGE_CASES: What unusual inputs/states exist?
5. DEPENDENCIES: What external factors matter?

Format as:
CONSTRAINTS:
- [constraint 1]
ASSUMPTIONS:
- [assumption 1] (confidence: high/medium/low)
RISKS:
- [risk 1] (severity: high/medium/low, mitigation: [strategy])
EDGE_CASES:
- [edge case 1]
""",
        ReasoningPhase.HYPOTHESIZE: """
## Solution Hypothesis Phase

Generate multiple potential solutions:

**Task:** {task}
**Analysis:** {analysis}

For each hypothesis:
1. Describe the approach clearly
2. List advantages (pros)
3. List disadvantages (cons)
4. Estimate complexity (1-5)
5. Estimate confidence (0-1)

Format as:
HYPOTHESIS_1:
  approach: [description of approach]
  pros:
    - [advantage 1]
  cons:
    - [disadvantage 1]
  complexity: [1-5]
  confidence: [0.0-1.0]
""",
        ReasoningPhase.EVALUATE: """
## Solution Evaluation Phase

Evaluate each hypothesis against criteria:

**Hypotheses:** {hypotheses}
**Success Criteria:** {criteria}
**Constraints:** {constraints}

For each hypothesis, assess:
1. Does it meet all success criteria?
2. Does it respect all constraints?
3. How does it handle edge cases?
4. What is the implementation risk?
5. What is the maintenance burden?

Rank hypotheses and select the best one:
EVALUATION:
  hypothesis_1: [score 1-10, reasoning]
  hypothesis_2: [score 1-10, reasoning]
SELECTED: [hypothesis_id]
REASONING: [why this is the best choice]
""",
        ReasoningPhase.SYNTHESIZE: """
## Solution Synthesis Phase

Create the implementation plan:

**Selected Approach:** {approach}
**Sub-tasks:** {subtasks}

Produce a step-by-step implementation plan:
1. What files need to be created/modified?
2. What is the order of operations?
3. What tests should be written first (TDD)?
4. What validation checks are needed?

Format as:
IMPLEMENTATION_PLAN:
  step_1:
    action: [specific action]
    files: [file paths]
    tests_first: [test file if applicable]
    validation: [how to verify]
""",
        ReasoningPhase.VALIDATE: """
## Validation Phase

Verify the solution is correct:

**Implementation:** {implementation}
**Success Criteria:** {criteria}

Check:
1. Does the code compile/parse without errors?
2. Do all tests pass?
3. Are all edge cases handled?
4. Are there any security concerns?
5. Is the code maintainable?

Format as:
VALIDATION_RESULTS:
  syntax_check: [pass/fail]
  tests_pass: [pass/fail]
  edge_cases: [pass/fail]
  security: [pass/fail]
  maintainability: [pass/fail]
ISSUES:
  - [issue 1]
FIXES_NEEDED:
  - [fix 1]
""",
        ReasoningPhase.REFLECT: """
## Reflection Phase

Learn from this task:

**Task:** {task}
**Outcome:** {outcome}
**Errors Encountered:** {errors}

Reflect on:
1. What worked well?
2. What could be improved?
3. What patterns should be remembered?
4. What mistakes should be avoided?

Format as:
LEARNINGS:
  successes:
    - [what worked]
  improvements:
    - [what to do better]
  patterns:
    - [pattern to remember]
  anti_patterns:
    - [mistake to avoid]
""",
    }

    def __init__(self, send_fn: Callable[[str], str | None], cwd: Path):
        self.send_fn = send_fn
        self.cwd = cwd
        self.context: ReasoningContext | None = None
        self._reasoning_cache: dict[str, Any] = {}

    def reason(self, task: str, depth: str = "full") -> ReasoningContext:
        """Execute the full reasoning chain for a task.

        Args:
            task: The task to reason about
            depth: "quick" for fast analysis, "full" for complete reasoning

        Returns:
            ReasoningContext with the full reasoning chain
        """
        self.context = ReasoningContext(task=task)

        if depth == "quick":
            phases = [
                ReasoningPhase.UNDERSTAND,
                ReasoningPhase.DECOMPOSE,
                ReasoningPhase.SYNTHESIZE,
            ]
        else:
            phases = [
                ReasoningPhase.UNDERSTAND,
                ReasoningPhase.DECOMPOSE,
                ReasoningPhase.ANALYZE,
                ReasoningPhase.HYPOTHESIZE,
                ReasoningPhase.EVALUATE,
                ReasoningPhase.SYNTHESIZE,
            ]

        for phase in phases:
            step = self._execute_phase(phase)
            self.context.reasoning_chain.append(step)

            if step.confidence < 0.3:
                # Low confidence - need more information
                self._gather_more_context(phase)

        return self.context

    def _execute_phase(self, phase: ReasoningPhase) -> ReasoningStep:
        """Execute a single reasoning phase."""
        prompt = self._build_phase_prompt(phase)
        response = self.send_fn(prompt)

        if not response:
            return ReasoningStep(
                phase=phase,
                thought="Phase failed - no response from model",
                confidence=0.0,
            )

        # Parse the response and extract structured information
        parsed = self._parse_phase_response(phase, response)

        # Update context based on phase
        self._update_context(phase, parsed)

        return ReasoningStep(
            phase=phase,
            thought=response,
            evidence=parsed.get("evidence", []),
            confidence=parsed.get("confidence", 0.5),
        )

    def _build_phase_prompt(self, phase: ReasoningPhase) -> str:
        """Build the prompt for a reasoning phase."""
        template = self.PHASE_PROMPTS[phase]

        # Gather context for template substitution
        context = {
            "task": self.context.task if self.context else "",
            "objective": self._get_objective(),
            "subtasks": self._format_subtasks(),
            "analysis": self._format_analysis(),
            "hypotheses": self._format_hypotheses(),
            "criteria": self._format_success_criteria(),
            "constraints": self._format_constraints(),
            "approach": self._format_selected_approach(),
            "implementation": self._format_implementation(),
            "outcome": self._format_outcome(),
            "errors": self._format_errors(),
        }

        return template.format(**context)

    def _parse_phase_response(self, phase: ReasoningPhase, response: str) -> dict[str, Any]:
        """Parse the response from a reasoning phase."""
        parsed: dict[str, Any] = {"raw": response, "evidence": [], "confidence": 0.5}

        if phase == ReasoningPhase.UNDERSTAND:
            # Extract objective
            if match := re.search(r"OBJECTIVE:\s*(.+?)(?:\n|$)", response):
                parsed["objective"] = match.group(1).strip()
                parsed["confidence"] = 0.7

            # Extract requirements
            requirements = re.findall(r"^\s*-\s*(.+)$", response, re.MULTILINE)
            parsed["requirements"] = requirements

            # Extract success criteria
            if "SUCCESS_CRITERIA" in response:
                criteria_section = response.split("SUCCESS_CRITERIA")[1]
                criteria = re.findall(r"^\s*-\s*(.+)$", criteria_section, re.MULTILINE)
                parsed["success_criteria"] = criteria

        elif phase == ReasoningPhase.DECOMPOSE:
            # Extract subtasks
            subtasks = []
            for match in re.finditer(
                r"SUBTASK_(\d+):\s*\n\s*action:\s*(.+?)\n\s*type:\s*(\w+)", response, re.DOTALL
            ):
                subtasks.append(
                    {
                        "id": f"subtask_{match.group(1)}",
                        "action": match.group(2).strip(),
                        "type": match.group(3).strip(),
                    }
                )
            parsed["subtasks"] = subtasks
            parsed["confidence"] = 0.8 if subtasks else 0.3

        elif phase == ReasoningPhase.ANALYZE:
            # Extract constraints, assumptions, risks, edge cases
            for key in ["CONSTRAINTS", "ASSUMPTIONS", "RISKS", "EDGE_CASES"]:
                if key in response:
                    section = response.split(key)[1].split("\n\n", maxsplit=1)[0]
                    items = re.findall(r"^\s*-\s*(.+)$", section, re.MULTILINE)
                    parsed[key.lower()] = items
            parsed["confidence"] = 0.7

        elif phase == ReasoningPhase.HYPOTHESIZE:
            # Extract hypotheses
            hypotheses = []
            for match in re.finditer(
                r"HYPOTHESIS_(\d+):\s*\n\s*approach:\s*(.+?)(?:\n\s*pros:|$)", response, re.DOTALL
            ):
                hypotheses.append(
                    {
                        "id": f"hypothesis_{match.group(1)}",
                        "approach": match.group(2).strip(),
                    }
                )
            parsed["hypotheses"] = hypotheses
            parsed["confidence"] = 0.7 if hypotheses else 0.4

        elif phase == ReasoningPhase.EVALUATE:
            # Extract selected hypothesis
            if match := re.search(r"SELECTED:\s*(\w+)", response):
                parsed["selected"] = match.group(1)
                parsed["confidence"] = 0.8
            if match := re.search(r"REASONING:\s*(.+?)(?:\n\n|$)", response, re.DOTALL):
                parsed["reasoning"] = match.group(1).strip()

        elif phase == ReasoningPhase.SYNTHESIZE:
            # Extract implementation plan
            if "IMPLEMENTATION_PLAN" in response:
                parsed["has_plan"] = True
                parsed["confidence"] = 0.8
            else:
                parsed["confidence"] = 0.4

        elif phase == ReasoningPhase.VALIDATE:
            # Extract validation results
            results = {}
            for check in ["syntax_check", "tests_pass", "edge_cases", "security"]:
                if match := re.search(rf"{check}:\s*(pass|fail)", response, re.IGNORECASE):
                    results[check] = match.group(1).lower() == "pass"
            parsed["validation_results"] = results
            parsed["confidence"] = 0.9 if results else 0.5

        return parsed

    def _update_context(self, phase: ReasoningPhase, parsed: dict[str, Any]) -> None:
        """Update the reasoning context based on parsed phase output."""
        if not self.context:
            return

        if phase == ReasoningPhase.UNDERSTAND:
            if "success_criteria" in parsed:
                if not self.context.analysis:
                    self.context.analysis = ProblemAnalysis(original_task=self.context.task)
                self.context.analysis.success_criteria = parsed["success_criteria"]

        elif phase == ReasoningPhase.DECOMPOSE:
            for st_data in parsed.get("subtasks", []):
                subtask = SubTask(
                    id=st_data["id"],
                    description=st_data["action"],
                    type=st_data.get("type", "implementation"),
                    priority=2,
                    complexity=3,
                )
                self.context.subtasks.append(subtask)

        elif phase == ReasoningPhase.ANALYZE:
            if not self.context.analysis:
                self.context.analysis = ProblemAnalysis(original_task=self.context.task)
            self.context.analysis.constraints = parsed.get("constraints", [])
            self.context.analysis.assumptions = parsed.get("assumptions", [])
            self.context.analysis.risks = parsed.get("risks", [])
            self.context.analysis.edge_cases = parsed.get("edge_cases", [])

        elif phase == ReasoningPhase.HYPOTHESIZE:
            for h_data in parsed.get("hypotheses", []):
                hypothesis = Hypothesis(
                    id=h_data["id"],
                    description=h_data.get("approach", ""),
                    approach=h_data.get("approach", ""),
                )
                self.context.hypotheses.append(hypothesis)

        elif phase == ReasoningPhase.EVALUATE:
            selected_id = parsed.get("selected")
            if selected_id:
                for h in self.context.hypotheses:
                    if h.id == selected_id or selected_id in h.id:
                        self.context.selected_approach = h
                        break

    def _gather_more_context(self, phase: ReasoningPhase) -> None:
        """Gather more context when confidence is low."""
        if phase == ReasoningPhase.UNDERSTAND:
            # Ask for clarification
            clarify_prompt = (
                "I need more clarity on this task. Please help me understand:\n"
                "1. What specific problem are we solving?\n"
                "2. What are the key requirements?\n"
                "3. What constraints should I be aware of?"
            )
            response = self.send_fn(clarify_prompt)
            if response and self.context:
                self.context.reasoning_chain.append(
                    ReasoningStep(
                        phase=ReasoningPhase.UNDERSTAND,
                        thought=f"Clarification: {response}",
                        confidence=0.6,
                    )
                )

    def _get_objective(self) -> str:
        """Get the objective from the reasoning chain."""
        if not self.context:
            return ""
        for step in self.context.reasoning_chain:
            if step.phase == ReasoningPhase.UNDERSTAND:
                if match := re.search(r"OBJECTIVE:\s*(.+?)(?:\n|$)", step.thought):
                    return match.group(1).strip()
        return self.context.task

    def _format_subtasks(self) -> str:
        """Format subtasks for prompt."""
        if not self.context or not self.context.subtasks:
            return "None defined yet"
        return "\n".join(
            f"- {st.id}: {st.description} (type: {st.type})" for st in self.context.subtasks
        )

    def _format_analysis(self) -> str:
        """Format analysis for prompt."""
        if not self.context or not self.context.analysis:
            return "Not yet analyzed"
        a = self.context.analysis
        parts = []
        if a.constraints:
            parts.append(f"Constraints: {', '.join(a.constraints)}")
        if a.assumptions:
            parts.append(f"Assumptions: {', '.join(a.assumptions)}")
        if a.risks:
            parts.append(f"Risks: {', '.join(a.risks)}")
        return "\n".join(parts) if parts else "No detailed analysis"

    def _format_hypotheses(self) -> str:
        """Format hypotheses for prompt."""
        if not self.context or not self.context.hypotheses:
            return "None generated yet"
        return "\n".join(f"- {h.id}: {h.approach[:100]}..." for h in self.context.hypotheses)

    def _format_success_criteria(self) -> str:
        """Format success criteria for prompt."""
        if not self.context or not self.context.analysis:
            return "Not defined"
        return (
            "\n".join(f"- {c}" for c in self.context.analysis.success_criteria)
            if self.context.analysis.success_criteria
            else "Not defined"
        )

    def _format_constraints(self) -> str:
        """Format constraints for prompt."""
        if not self.context or not self.context.analysis:
            return "None identified"
        return (
            "\n".join(f"- {c}" for c in self.context.analysis.constraints)
            if self.context.analysis.constraints
            else "None identified"
        )

    def _format_selected_approach(self) -> str:
        """Format selected approach for prompt."""
        if not self.context or not self.context.selected_approach:
            return "None selected yet"
        return self.context.selected_approach.approach

    def _format_implementation(self) -> str:
        """Format implementation summary for prompt."""
        if not self.context:
            return "No implementation yet"
        if self.context.files_modified:
            return f"Modified files: {', '.join(self.context.files_modified)}"
        return "No files modified yet"

    def _format_outcome(self) -> str:
        """Format outcome for prompt."""
        if not self.context:
            return "Unknown"
        completed = sum(1 for st in self.context.subtasks if st.status == "completed")
        total = len(self.context.subtasks)
        return f"{completed}/{total} subtasks completed"

    def _format_errors(self) -> str:
        """Format errors for prompt."""
        if not self.context or not self.context.errors_encountered:
            return "None"
        return "\n".join(f"- {e}" for e in self.context.errors_encountered)

    def get_reasoning_summary(self) -> str:
        """Get a human-readable summary of the reasoning process."""
        if not self.context:
            return "No reasoning context available"

        lines = ["## Reasoning Summary\n"]

        # Task
        lines.append(f"**Task:** {self.context.task}\n")

        # Analysis
        if self.context.analysis:
            a = self.context.analysis
            if a.goals:
                lines.append(f"**Goals:** {', '.join(a.goals)}")
            if a.constraints:
                lines.append(f"**Constraints:** {', '.join(a.constraints)}")
            if a.risks:
                lines.append(f"**Risks:** {', '.join(a.risks)}")

        # Selected approach
        if self.context.selected_approach:
            lines.append(f"\n**Selected Approach:** {self.context.selected_approach.approach}")

        # Subtasks
        if self.context.subtasks:
            lines.append("\n**Execution Plan:**")
            for st in self.context.subtasks:
                status_icon = {
                    "pending": "⏳",
                    "in_progress": "🔄",
                    "completed": "✅",
                    "blocked": "🚫",
                }.get(st.status, "?")
                lines.append(f"  {status_icon} {st.description}")

        # Reasoning chain confidence
        if self.context.reasoning_chain:
            avg_confidence = sum(s.confidence for s in self.context.reasoning_chain) / len(
                self.context.reasoning_chain
            )
            lines.append(f"\n**Overall Confidence:** {avg_confidence:.1%}")

        return "\n".join(lines)


class SelfReflectionEngine:
    """Implements self-reflection and validation for code quality."""

    REFLECTION_PROMPT = """
## Self-Reflection Check

Review your work critically:

**Task:** {task}
**Code Written:** {code_summary}
**Tests Written:** {test_summary}
**Errors Seen:** {errors}

Ask yourself:
1. Does this solution actually solve the problem?
2. Are there any obvious bugs I missed?
3. Did I handle all edge cases?
4. Is the code clean and maintainable?
5. Are the tests comprehensive?
6. Did I follow TDD properly?

Be brutally honest. List any issues found:
ISSUES:
- [issue 1]
FIXES_NEEDED:
- [fix 1]
CONFIDENCE: [0-1]
"""

    def __init__(self, send_fn: Callable[[str], str | None]):
        self.send_fn = send_fn
        self.reflection_history: list[dict] = []

    def reflect(
        self,
        task: str,
        code_files: list[str],
        test_files: list[str],
        errors: list[str],
    ) -> dict[str, Any]:
        """Perform self-reflection on completed work."""
        prompt = self.REFLECTION_PROMPT.format(
            task=task,
            code_summary=", ".join(code_files) if code_files else "None",
            test_summary=", ".join(test_files) if test_files else "None",
            errors="\n".join(f"- {e}" for e in errors) if errors else "None",
        )

        response = self.send_fn(prompt)
        if not response:
            return {"success": False, "issues": [], "confidence": 0.0}

        # Parse reflection response
        result: dict[str, Any] = {
            "success": True,
            "issues": [],
            "fixes_needed": [],
            "confidence": 0.5,
            "raw_response": response,
        }

        # Extract issues
        if "ISSUES:" in response:
            issues_section = response.split("ISSUES:")[1].split("\n\n")[0]
            issues = re.findall(r"^\s*-\s*(.+)$", issues_section, re.MULTILINE)
            result["issues"] = [i for i in issues if i.strip() and i.strip() != "[issue 1]"]

        # Extract fixes needed
        if "FIXES_NEEDED:" in response:
            fixes_section = response.split("FIXES_NEEDED:")[1].split("\n\n")[0]
            fixes = re.findall(r"^\s*-\s*(.+)$", fixes_section, re.MULTILINE)
            result["fixes_needed"] = [f for f in fixes if f.strip() and f.strip() != "[fix 1]"]

        # Extract confidence
        if match := re.search(r"CONFIDENCE:\s*([\d.]+)", response):
            try:
                result["confidence"] = float(match.group(1))
            except ValueError:
                pass

        self.reflection_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "result": result,
            }
        )

        return result

    def needs_improvement(self, reflection_result: dict[str, Any]) -> bool:
        """Check if the reflection indicates improvements are needed."""
        if reflection_result.get("confidence", 1.0) < 0.7:
            return True
        if reflection_result.get("issues"):
            return True
        if reflection_result.get("fixes_needed"):
            return True
        return False


class MultiPerspectiveAnalyzer:
    """Analyzes problems from multiple perspectives for robust solutions."""

    PERSPECTIVES = [
        {
            "name": "User",
            "prompt": "As a user of this code, what would frustrate me? What would delight me?",
        },
        {
            "name": "Security",
            "prompt": "As a security auditor, what vulnerabilities exist? What attack vectors?",
        },
        {
            "name": "Performance",
            "prompt": "As a performance engineer, what bottlenecks exist? What could scale poorly?",
        },
        {
            "name": "Maintainer",
            "prompt": "As a future maintainer, what would confuse me? What lacks documentation?",
        },
        {
            "name": "Tester",
            "prompt": "As a QA engineer, what edge cases exist? What's hard to test?",
        },
    ]

    def __init__(self, send_fn: Callable[[str], str | None]):
        self.send_fn = send_fn

    def analyze(self, code: str, context: str = "") -> dict[str, list[str]]:
        """Analyze code from multiple perspectives."""
        results: dict[str, list[str]] = {}

        for perspective in self.PERSPECTIVES:
            prompt = (
                f"## {perspective['name']} Perspective Analysis\n\n"
                f"{perspective['prompt']}\n\n"
                f"**Context:** {context}\n\n"
                f"**Code:**\n```\n{code[:2000]}\n```\n\n"
                f"List concerns (one per line, prefix with -):"
            )

            response = self.send_fn(prompt)
            if response:
                concerns = re.findall(r"^\s*-\s*(.+)$", response, re.MULTILINE)
                results[perspective["name"]] = concerns

        return results

    def get_summary(self, analysis: dict[str, list[str]]) -> str:
        """Get a summary of multi-perspective analysis."""
        if not analysis:
            return "No analysis available"

        lines = ["## Multi-Perspective Analysis\n"]
        for perspective, concerns in analysis.items():
            if concerns:
                lines.append(f"\n**{perspective}:**")
                for concern in concerns[:3]:  # Top 3 per perspective
                    lines.append(f"  - {concern}")

        return "\n".join(lines)


class ErrorDiagnosis:
    """Intelligent error diagnosis and fix suggestion."""

    ERROR_PATTERNS = {
        "import_error": {
            "pattern": r"ImportError|ModuleNotFoundError|No module named",
            "diagnosis": "Missing import or incorrect module path",
            "fixes": [
                "Check if the module exists in the codebase",
                "Verify the import path matches the file structure",
                "Check if __init__.py exists for package imports",
                "Install missing dependencies with pip/npm",
            ],
        },
        "attribute_error": {
            "pattern": r"AttributeError|has no attribute",
            "diagnosis": "Object doesn't have the expected attribute",
            "fixes": [
                "Check spelling of the attribute name",
                "Verify the object type is correct",
                "Check if the attribute was renamed or removed",
                "Look for typos in variable names",
            ],
        },
        "type_error": {
            "pattern": r"TypeError|expected .* got",
            "diagnosis": "Wrong type passed to function or operation",
            "fixes": [
                "Check function signature and expected types",
                "Verify argument order is correct",
                "Add type conversion if needed",
                "Check for None values",
            ],
        },
        "syntax_error": {
            "pattern": r"SyntaxError|invalid syntax",
            "diagnosis": "Code has syntax errors",
            "fixes": [
                "Check for missing colons, brackets, or quotes",
                "Verify indentation is consistent",
                "Look at the line before the error",
                "Check for unclosed strings or brackets",
            ],
        },
        "name_error": {
            "pattern": r"NameError|is not defined",
            "diagnosis": "Variable or function not defined",
            "fixes": [
                "Check if the name is spelled correctly",
                "Verify the variable is defined before use",
                "Check import statements",
                "Look for scope issues",
            ],
        },
        "assertion_error": {
            "pattern": r"AssertionError|assert.*failed",
            "diagnosis": "Test assertion failed",
            "fixes": [
                "Check expected vs actual values",
                "Verify test logic is correct",
                "Review the code being tested",
                "Check for off-by-one errors",
            ],
        },
        "key_error": {
            "pattern": r"KeyError",
            "diagnosis": "Dictionary key doesn't exist",
            "fixes": [
                "Use .get() with default value",
                "Check if key exists before access",
                "Verify key spelling",
                "Print available keys for debugging",
            ],
        },
        "file_not_found": {
            "pattern": r"FileNotFoundError|No such file",
            "diagnosis": "File or directory doesn't exist",
            "fixes": [
                "Check file path is correct",
                "Use absolute paths or verify working directory",
                "Create the file/directory if it should exist",
                "Check for typos in the path",
            ],
        },
    }

    def __init__(self):
        self.diagnosis_cache: dict[str, dict] = {}

    def diagnose(self, error: str) -> dict[str, Any]:
        """Diagnose an error and suggest fixes."""
        # Check cache
        error_hash = hashlib.md5(error.encode()).hexdigest()[:12]
        if error_hash in self.diagnosis_cache:
            return self.diagnosis_cache[error_hash]

        result: dict[str, Any] = {
            "error_type": "unknown",
            "diagnosis": "Unknown error",
            "suggested_fixes": ["Review the error message carefully"],
            "confidence": 0.3,
        }

        for error_type, pattern_info in self.ERROR_PATTERNS.items():
            if re.search(pattern_info["pattern"], error, re.IGNORECASE):
                result = {
                    "error_type": error_type,
                    "diagnosis": pattern_info["diagnosis"],
                    "suggested_fixes": pattern_info["fixes"],
                    "confidence": 0.8,
                }
                break

        # Extract specific details from error
        if match := re.search(r"line (\d+)", error):
            result["line_number"] = int(match.group(1))
        if match := re.search(r"File [\"'](.+?)[\"']", error):
            result["file"] = match.group(1)
        if match := re.search(r"'(\w+)' is not defined", error):
            result["undefined_name"] = match.group(1)
        if match := re.search(r"No module named '([^']+)'", error):
            result["missing_module"] = match.group(1)

        self.diagnosis_cache[error_hash] = result
        return result

    def format_diagnosis(self, diagnosis: dict[str, Any]) -> str:
        """Format diagnosis for display."""
        lines = [
            f"🔍 **Error Type:** {diagnosis['error_type']}",
            f"📋 **Diagnosis:** {diagnosis['diagnosis']}",
        ]

        if "line_number" in diagnosis:
            lines.append(f"📍 **Line:** {diagnosis['line_number']}")
        if "file" in diagnosis:
            lines.append(f"📁 **File:** {diagnosis['file']}")
        if "missing_module" in diagnosis:
            lines.append(f"📦 **Missing Module:** {diagnosis['missing_module']}")

        lines.append("\n**Suggested Fixes:**")
        for fix in diagnosis["suggested_fixes"]:
            lines.append(f"  - {fix}")

        lines.append(f"\n**Confidence:** {diagnosis['confidence']:.0%}")

        return "\n".join(lines)
