"""State dataclasses for the Deep Research Agent.

This module defines all data structures used throughout the research process,
including evidence tracking, claims, gaps, and the overall research state.

Team Values Enforcement:
- V1: Truth over fluency - Claims must have evidence_ids
- V2: Evidence-first - EvidenceItem tracks all tool outputs
- V3: Reviewer-first - ResearchPlan includes required sections
- V4: Cost awareness - Budgets tracked in ResearchState
- V5: Actionable outcomes - Gap and ResearchQuestion structures
- V6: Team alignment - Deliverable categories match team workflows
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional, Any


@dataclass
class EvidenceItem:
    """Machine-verifiable evidence from tool execution.

    Every piece of evidence has a unique ID that can be referenced
    in claims. The output_ref points to the raw tool output for
    reproducibility.

    Attributes:
        id: Unique identifier (e.g., "E12")
        tool: Tool name that produced this evidence
        input: Exact arguments passed to the tool
        output_ref: Pointer to raw output (for reproducibility)
        summary: 1-3 line human-readable summary
        entities: File paths, PR IDs, symbols, node IDs found
        timestamp: When the evidence was collected
    """
    id: str
    tool: str
    input: dict
    output_ref: str
    summary: str
    entities: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "tool": self.tool,
            "input": self.input,
            "output_ref": self.output_ref,
            "summary": self.summary,
            "entities": self.entities,
            "timestamp": self.timestamp,
        }


@dataclass
class Claim:
    """A grounded statement backed by evidence.

    Claims are the core output of research. Every claim MUST reference
    at least one evidence ID. This is enforced by __post_init__.

    Confidence levels:
    - 0: Speculation (should be avoided)
    - 1: Single source, may have assumptions
    - 2: Multiple sources corroborate (requires 2+ evidence_ids)
    - 3: Strong evidence, no assumptions

    Attributes:
        id: Unique identifier (e.g., "C7")
        statement: The claim being made
        evidence_ids: References to EvidenceItems (MUST NOT be empty)
        confidence: Discrete confidence level 0-3
        assumptions: Explicit assumptions (caps confidence at 1)
        counterevidence_ids: Evidence that contradicts this claim

    Raises:
        ValueError: If evidence_ids is empty or assumptions conflict with confidence
    """
    id: str
    statement: str
    evidence_ids: list[str]
    confidence: Literal[0, 1, 2, 3]
    assumptions: list[str] = field(default_factory=list)
    counterevidence_ids: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Enforce team value V1: Truth over fluency."""
        if not self.evidence_ids:
            raise ValueError(
                f"Claim {self.id} must have at least one evidence_id. "
                "Team value V1: No claim without evidence."
            )
        if self.assumptions and self.confidence > 1:
            raise ValueError(
                f"Claim {self.id} has assumptions but confidence > 1. "
                "Claims with assumptions cannot exceed confidence 1."
            )
        if self.confidence >= 2 and len(self.evidence_ids) < 2:
            raise ValueError(
                f"Claim {self.id} has confidence >= 2 but only {len(self.evidence_ids)} evidence. "
                "Confidence 2+ requires evidence from 2+ distinct sources."
            )

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "statement": self.statement,
            "evidence_ids": self.evidence_ids,
            "confidence": self.confidence,
            "assumptions": self.assumptions,
            "counterevidence_ids": self.counterevidence_ids,
        }


@dataclass
class Gap:
    """Explicit unknown that couldn't be resolved.

    Gaps are questions that remain unanswered after research.
    They represent honest acknowledgment of limitations (V1: Truth over fluency).

    Attributes:
        question: The unanswered question
        reason: Why this couldn't be answered
        suggested_tools: Tools that might help answer this
    """
    question: str
    reason: str
    suggested_tools: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "question": self.question,
            "reason": self.reason,
            "suggested_tools": self.suggested_tools,
        }


@dataclass
class ResearchQuestion:
    """A question in the research plan.

    Questions are prioritized (P0/P1/P2) and map to team deliverables.
    Each question has success criteria that the Critic evaluates.

    Attributes:
        qid: Unique question identifier (e.g., "Q1")
        question: The research question
        priority: P0 (must answer), P1 (should answer), P2 (nice to have)
        success_criteria: Checkable criteria for completion
        suggested_tools: Tool macros or sequences to use
        deliverable: Team workflow category this maps to
    """
    qid: str
    question: str
    priority: Literal["P0", "P1", "P2"]
    success_criteria: list[str]
    suggested_tools: list[str]
    deliverable: Literal["Design", "Implementation", "Testing", "Review", "Ops"]

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "qid": self.qid,
            "question": self.question,
            "priority": self.priority,
            "success_criteria": self.success_criteria,
            "suggested_tools": self.suggested_tools,
            "deliverable": self.deliverable,
        }


@dataclass
class ResearchPlan:
    """Output of the Planner agent.

    The plan decomposes the research goal into questions aligned with
    how the team works. It includes budgets for cost awareness (V4)
    and required sections for reviewer-first output (V3).

    Attributes:
        goal: The original research goal
        questions: List of prioritized research questions
        max_iterations: Maximum research-critique loops
        budgets: Resource limits {tool_calls, tokens, time_s}
        required_sections: Sections that must appear in final report
        team_values_checklist: Values to check during critique
    """
    goal: str
    questions: list[ResearchQuestion]
    max_iterations: int
    budgets: dict  # {tool_calls: int, tokens: int, time_s: int}
    required_sections: list[str]
    team_values_checklist: list[str]

    def get_p0_questions(self) -> list[ResearchQuestion]:
        """Get all P0 (must answer) questions."""
        return [q for q in self.questions if q.priority == "P0"]

    def get_p1_questions(self) -> list[ResearchQuestion]:
        """Get all P1 (should answer) questions."""
        return [q for q in self.questions if q.priority == "P1"]

    def get_p2_questions(self) -> list[ResearchQuestion]:
        """Get all P2 (nice to have) questions."""
        return [q for q in self.questions if q.priority == "P2"]

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "goal": self.goal,
            "questions": [q.to_dict() for q in self.questions],
            "max_iterations": self.max_iterations,
            "budgets": self.budgets,
            "required_sections": self.required_sections,
            "team_values_checklist": self.team_values_checklist,
        }


@dataclass
class FollowUpQuestion:
    """A follow-up question from the Critic.

    Attributes:
        qid: Optional link to original question
        question: The follow-up question
        why: Reason this follow-up is needed
        suggested_tools: Tools to use for answering
    """
    question: str
    why: str
    suggested_tools: list[str] = field(default_factory=list)
    qid: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "qid": self.qid,
            "question": self.question,
            "why": self.why,
            "suggested_tools": self.suggested_tools,
        }


@dataclass
class Contradiction:
    """A detected contradiction between claims.

    Attributes:
        claim_a: First claim ID
        claim_b: Second claim ID
        note: Explanation of the contradiction
    """
    claim_a: str
    claim_b: str
    note: str

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "claim_a": self.claim_a,
            "claim_b": self.claim_b,
            "note": self.note,
        }


@dataclass
class ValuesViolation:
    """A violation of team values detected by the Critic.

    Attributes:
        value: Which value was violated (V1-V6)
        issue: Description of the violation
        affected_claims: Claims that violate this value
    """
    value: str
    issue: str
    affected_claims: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "value": self.value,
            "issue": self.issue,
            "affected_claims": self.affected_claims,
        }


@dataclass
class CritiqueScores:
    """Scores assigned by the Critic agent.

    Each dimension is scored 1-5:
    - 1: Poor
    - 2: Below expectations
    - 3: Acceptable
    - 4: Good
    - 5: Excellent

    Attributes:
        coverage: Were all questions addressed?
        evidence: Are claims backed by tool results?
        depth: Is analysis thorough or superficial?
        coherence: Do findings connect logically?
        team_alignment: Does output follow team values/workflows?
    """
    coverage: Literal[1, 2, 3, 4, 5]
    evidence: Literal[1, 2, 3, 4, 5]
    depth: Literal[1, 2, 3, 4, 5]
    coherence: Literal[1, 2, 3, 4, 5]
    team_alignment: Literal[1, 2, 3, 4, 5]

    def average(self) -> float:
        """Calculate average score across all dimensions."""
        return (
            self.coverage + self.evidence + self.depth +
            self.coherence + self.team_alignment
        ) / 5.0

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "coverage": self.coverage,
            "evidence": self.evidence,
            "depth": self.depth,
            "coherence": self.coherence,
            "team_alignment": self.team_alignment,
        }


@dataclass
class Critique:
    """Output of the Critic agent.

    The Critic evaluates research completeness AND team value adherence.

    Decision meanings:
    - APPROVE: All P0 criteria met, scores pass thresholds
    - CONTINUE: Progress made, follow-ups needed
    - REJECT: Values violated, must fix issues
    - ESCALATE: Need more powerful model/budget

    Hard rules enforced:
    - evidence < 3 -> APPROVE forbidden
    - team_alignment < 4 -> APPROVE forbidden
    - All P0 questions must meet success criteria for APPROVE
    - Any contradiction must be resolved or listed

    Attributes:
        decision: The Critic's decision
        scores: Scores across all dimensions
        must_fix: Blocking issues that must be fixed
        follow_up_questions: Questions to investigate next
        risky_claims: Claims that need more evidence
        contradictions: Detected contradictions between claims
        values_violations: Team value violations found
    """
    decision: Literal["APPROVE", "CONTINUE", "REJECT", "ESCALATE"]
    scores: CritiqueScores
    must_fix: list[str] = field(default_factory=list)
    follow_up_questions: list[FollowUpQuestion] = field(default_factory=list)
    risky_claims: list[str] = field(default_factory=list)
    contradictions: list[Contradiction] = field(default_factory=list)
    values_violations: list[ValuesViolation] = field(default_factory=list)

    def __post_init__(self):
        """Enforce hard approval rules."""
        if self.decision == "APPROVE":
            if self.scores.evidence < 3:
                raise ValueError(
                    "Cannot APPROVE with evidence score < 3. "
                    "Team value V2: Evidence-first."
                )
            if self.scores.team_alignment < 4:
                raise ValueError(
                    "Cannot APPROVE with team_alignment score < 4. "
                    "Team value V6: Team alignment."
                )

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "decision": self.decision,
            "scores": self.scores.to_dict(),
            "must_fix": self.must_fix,
            "follow_up_questions": [q.to_dict() for q in self.follow_up_questions],
            "risky_claims": self.risky_claims,
            "contradictions": [c.to_dict() for c in self.contradictions],
            "values_violations": [v.to_dict() for v in self.values_violations],
        }


@dataclass
class IterationResult:
    """Record of one research iteration.

    Captures all outputs from a single research-critique cycle
    for history tracking and final synthesis.

    Attributes:
        iteration: Iteration number (0-indexed)
        evidence: Evidence collected in this iteration
        claims: Claims proposed in this iteration
        gaps: Gaps identified in this iteration
        critique: Critic's evaluation
        model_tier: Model tier used for this iteration
    """
    iteration: int
    evidence: list[EvidenceItem]
    claims: list[Claim]
    gaps: list[Gap]
    critique: Critique
    model_tier: str = "fast"

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "iteration": self.iteration,
            "evidence": [e.to_dict() for e in self.evidence],
            "claims": [c.to_dict() for c in self.claims],
            "gaps": [g.to_dict() for g in self.gaps],
            "critique": self.critique.to_dict(),
            "model_tier": self.model_tier,
        }


@dataclass
class ResearchState:
    """Full state of the research process.

    Tracks everything needed for the multi-loop research cycle,
    including history, budgets, and model tiers.

    Attributes:
        plan: The research plan from the Planner
        history: Results from all iterations
        context: Shared context updated each iteration
        iteration: Current iteration number
        remaining_budget: Remaining resource budgets
        current_model_tier: Current model tier (fast/standard/powerful)
        question_queue: Questions still to be answered
        answered_questions: Questions that have been answered
    """
    plan: ResearchPlan
    history: list[IterationResult] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    iteration: int = 0
    remaining_budget: dict = field(default_factory=dict)
    current_model_tier: Literal["fast", "standard", "powerful"] = "fast"
    question_queue: list[str] = field(default_factory=list)  # qids
    answered_questions: set[str] = field(default_factory=set)  # qids

    def __post_init__(self):
        """Initialize remaining budget from plan."""
        if not self.remaining_budget and self.plan:
            self.remaining_budget = dict(self.plan.budgets)
        if not self.question_queue and self.plan:
            # Initialize queue with P0 first, then P1, then P2
            self.question_queue = [
                q.qid for q in self.plan.get_p0_questions()
            ] + [
                q.qid for q in self.plan.get_p1_questions()
            ] + [
                q.qid for q in self.plan.get_p2_questions()
            ]

    def get_all_evidence(self) -> list[EvidenceItem]:
        """Get all evidence from all iterations."""
        evidence = []
        for result in self.history:
            evidence.extend(result.evidence)
        return evidence

    def get_all_claims(self) -> list[Claim]:
        """Get all claims from all iterations."""
        claims = []
        for result in self.history:
            claims.extend(result.claims)
        return claims

    def get_all_gaps(self) -> list[Gap]:
        """Get all gaps from all iterations."""
        gaps = []
        for result in self.history:
            gaps.extend(result.gaps)
        return gaps

    def get_question_by_qid(self, qid: str) -> Optional[ResearchQuestion]:
        """Get a question by its ID."""
        for q in self.plan.questions:
            if q.qid == qid:
                return q
        return None

    def is_approved(self) -> bool:
        """Check if research has been approved."""
        if not self.history:
            return False
        return self.history[-1].critique.decision == "APPROVE"

    def budget_used_percent(self) -> float:
        """Calculate percentage of tool call budget used."""
        total = self.plan.budgets.get("tool_calls", 100)
        remaining = self.remaining_budget.get("tool_calls", total)
        return ((total - remaining) / total) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "plan": self.plan.to_dict(),
            "history": [h.to_dict() for h in self.history],
            "context": self.context,
            "iteration": self.iteration,
            "remaining_budget": self.remaining_budget,
            "current_model_tier": self.current_model_tier,
            "question_queue": self.question_queue,
            "answered_questions": list(self.answered_questions),
        }
