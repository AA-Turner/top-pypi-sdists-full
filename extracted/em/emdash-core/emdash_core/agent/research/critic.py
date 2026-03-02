"""Critic agent for evaluating research quality.

The Critic evaluates research completeness AND team value adherence.
It enforces hard rules and provides feedback for improvement.
"""

import json
from typing import Optional

from rich.console import Console

from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL
from .state import (
    ResearchPlan,
    EvidenceItem,
    Claim,
    Gap,
    Critique,
    CritiqueScores,
    FollowUpQuestion,
    Contradiction,
    ValuesViolation,
)


CRITIC_SYSTEM_PROMPT = """You are a research critic that evaluates research quality and team value adherence.

Your job is to:
1. Score research across 5 dimensions (1-5 each)
2. Identify issues that must be fixed
3. Suggest follow-up questions
4. Detect contradictions
5. Check team value compliance

SCORING DIMENSIONS (1-5):
- coverage: Were all P0/P1 questions addressed?
- evidence: Are claims backed by tool results?
- depth: Is analysis thorough or superficial?
- coherence: Do findings connect logically?
- team_alignment: Does output follow team values?

DECISION RULES:
- APPROVE: All P0 met, evidence >= 3, team_alignment >= 4
- CONTINUE: Progress made, but gaps remain
- REJECT: Values violated (ungrounded claims, missing evidence)
- ESCALATE: Need more powerful model/budget

TEAM VALUES TO CHECK:
- V1: All claims have evidence IDs
- V2: Evidence is reproducible (tool calls documented)
- V3: Output includes reviewer checklist
- V4: Budget respected
- V5: Report ends with actionable tasks
- V6: Uses team vocabulary

OUTPUT FORMAT (JSON only):
{
  "decision": "APPROVE|CONTINUE|REJECT|ESCALATE",
  "scores": {
    "coverage": 1-5,
    "evidence": 1-5,
    "depth": 1-5,
    "coherence": 1-5,
    "team_alignment": 1-5
  },
  "must_fix": ["blocking issue 1", ...],
  "follow_up_questions": [
    {"question": "...", "why": "...", "suggested_tools": [...]}
  ],
  "risky_claims": ["C1", "C3"],
  "contradictions": [
    {"claim_a": "C1", "claim_b": "C2", "note": "..."}
  ],
  "values_violations": [
    {"value": "V1", "issue": "...", "affected_claims": ["C1"]}
  ]
}

Be strict. Evidence quality matters more than quantity."""


class CriticAgent:
    """Evaluates research quality and team value adherence.

    The Critic provides objective feedback on research progress
    and enforces hard rules about evidence and values.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
    ):
        """Initialize the critic agent.

        Args:
            model: LLM model to use
            verbose: Whether to print progress
        """
        self.provider = get_provider(model)
        self.model = model
        self.verbose = verbose
        self.console = Console()

    def evaluate(
        self,
        plan: ResearchPlan,
        evidence: list[EvidenceItem],
        claims: list[Claim],
        gaps: list[Gap],
        iteration: int,
        budget_used_percent: float,
    ) -> Critique:
        """Evaluate research progress.

        Args:
            plan: Research plan
            evidence: Evidence collected
            claims: Claims proposed
            gaps: Gaps identified
            iteration: Current iteration number
            budget_used_percent: Percentage of budget used

        Returns:
            Critique with scores and feedback
        """
        if self.verbose:
            self.console.print(f"[cyan]Evaluating iteration {iteration + 1}...[/cyan]")

        # Try LLM-based evaluation
        try:
            critique = self._llm_evaluate(
                plan, evidence, claims, gaps, iteration, budget_used_percent
            )
            if critique:
                if self.verbose:
                    self.console.print(
                        f"[{'green' if critique.decision == 'APPROVE' else 'yellow'}]"
                        f"Decision: {critique.decision} "
                        f"(avg score: {critique.scores.average():.1f})"
                        f"[/{'green' if critique.decision == 'APPROVE' else 'yellow'}]"
                    )
                return critique
        except Exception as e:
            if self.verbose:
                self.console.print(f"[yellow]LLM evaluation failed: {e}[/yellow]")

        # Fallback to heuristic evaluation
        return self._heuristic_evaluate(
            plan, evidence, claims, gaps, iteration, budget_used_percent
        )

    def _llm_evaluate(
        self,
        plan: ResearchPlan,
        evidence: list[EvidenceItem],
        claims: list[Claim],
        gaps: list[Gap],
        iteration: int,
        budget_used_percent: float,
    ) -> Optional[Critique]:
        """Evaluate using LLM.

        Args:
            plan: Research plan
            evidence: Evidence collected
            claims: Claims proposed
            gaps: Gaps identified
            iteration: Current iteration
            budget_used_percent: Budget usage

        Returns:
            Critique or None on failure
        """
        # Format input for LLM
        questions_text = "\n".join([
            f"- [{q.priority}] {q.qid}: {q.question}"
            for q in plan.questions
        ])

        evidence_text = "\n".join([
            f"- {e.id}: {e.tool} -> {e.summary}"
            for e in evidence
        ]) or "No evidence"

        claims_text = "\n".join([
            f"- {c.id} (conf={c.confidence}, evidence={c.evidence_ids}): {c.statement}"
            for c in claims
        ]) or "No claims"

        gaps_text = "\n".join([
            f"- {g.question}: {g.reason}"
            for g in gaps
        ]) or "No gaps"

        user_message = f"""Evaluate this research progress.

GOAL: {plan.goal}

QUESTIONS:
{questions_text}

EVIDENCE COLLECTED:
{evidence_text}

CLAIMS MADE:
{claims_text}

GAPS IDENTIFIED:
{gaps_text}

STATS:
- Iteration: {iteration + 1}/{plan.max_iterations}
- Budget used: {budget_used_percent:.0f}%
- Evidence count: {len(evidence)}
- Claims count: {len(claims)}
- Gaps count: {len(gaps)}

TEAM VALUES CHECKLIST:
{chr(10).join(plan.team_values_checklist)}

Evaluate and return JSON only."""

        messages = [{"role": "user", "content": user_message}]
        response = self.provider.chat(messages, system=CRITIC_SYSTEM_PROMPT)
        content = response.content or ""

        # Parse JSON
        try:
            json_str = content
            if "```" in content:
                start = content.find("```")
                end = content.find("```", start + 3)
                if end > start:
                    json_str = content[start + 3:end]
                    if json_str.startswith("json"):
                        json_str = json_str[4:]

            data = json.loads(json_str.strip())

            scores = CritiqueScores(
                coverage=max(1, min(5, data["scores"].get("coverage", 3))),
                evidence=max(1, min(5, data["scores"].get("evidence", 3))),
                depth=max(1, min(5, data["scores"].get("depth", 3))),
                coherence=max(1, min(5, data["scores"].get("coherence", 3))),
                team_alignment=max(1, min(5, data["scores"].get("team_alignment", 3))),
            )

            # Parse follow-up questions
            follow_ups = []
            for q in data.get("follow_up_questions", []):
                follow_ups.append(FollowUpQuestion(
                    question=q.get("question", ""),
                    why=q.get("why", ""),
                    suggested_tools=q.get("suggested_tools", []),
                ))

            # Parse contradictions
            contradictions = []
            for c in data.get("contradictions", []):
                contradictions.append(Contradiction(
                    claim_a=c.get("claim_a", ""),
                    claim_b=c.get("claim_b", ""),
                    note=c.get("note", ""),
                ))

            # Parse values violations
            violations = []
            for v in data.get("values_violations", []):
                violations.append(ValuesViolation(
                    value=v.get("value", ""),
                    issue=v.get("issue", ""),
                    affected_claims=v.get("affected_claims", []),
                ))

            # Validate decision against scores
            decision = data.get("decision", "CONTINUE")
            if decision == "APPROVE":
                if scores.evidence < 3:
                    decision = "CONTINUE"
                if scores.team_alignment < 4:
                    decision = "CONTINUE"

            return Critique(
                decision=decision,
                scores=scores,
                must_fix=data.get("must_fix", []),
                follow_up_questions=follow_ups,
                risky_claims=data.get("risky_claims", []),
                contradictions=contradictions,
                values_violations=violations,
            )

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            if self.verbose:
                self.console.print(f"[yellow]Failed to parse critique: {e}[/yellow]")
            return None

    def _heuristic_evaluate(
        self,
        plan: ResearchPlan,
        evidence: list[EvidenceItem],
        claims: list[Claim],
        gaps: list[Gap],
        iteration: int,
        budget_used_percent: float,
    ) -> Critique:
        """Evaluate using heuristics.

        Fallback method when LLM evaluation fails.

        Args:
            plan: Research plan
            evidence: Evidence collected
            claims: Claims proposed
            gaps: Gaps identified
            iteration: Current iteration
            budget_used_percent: Budget usage

        Returns:
            Critique
        """
        # Calculate coverage score
        p0_questions = plan.get_p0_questions()
        p0_answered = 0
        for q in p0_questions:
            # Check if any claim relates to this question
            q_keywords = set(q.question.lower().split())
            for claim in claims:
                c_keywords = set(claim.statement.lower().split())
                if len(q_keywords & c_keywords) >= 2:
                    p0_answered += 1
                    break

        coverage = min(5, max(1, int(5 * p0_answered / max(len(p0_questions), 1))))

        # Calculate evidence score
        if not evidence:
            evidence_score = 1
        elif len(evidence) < 3:
            evidence_score = 2
        elif len(evidence) < 10:
            evidence_score = 3
        else:
            evidence_score = 4

        # Boost if claims have good evidence
        high_conf_claims = [c for c in claims if c.confidence >= 2]
        if len(high_conf_claims) > len(claims) / 2:
            evidence_score = min(5, evidence_score + 1)

        # Calculate depth score
        if not claims:
            depth = 1
        elif len(claims) < 3:
            depth = 2
        elif len(claims) < 8:
            depth = 3
        else:
            depth = 4

        # Coherence score
        coherence = 3  # Default to acceptable
        if len(gaps) > len(claims):
            coherence = 2  # Too many gaps

        # Team alignment score
        team_alignment = 4  # Default to good

        # Check for ungrounded claims (V1 violation)
        ungrounded = [c for c in claims if len(c.evidence_ids) == 0]
        if ungrounded:
            team_alignment = 2

        scores = CritiqueScores(
            coverage=coverage,
            evidence=evidence_score,
            depth=depth,
            coherence=coherence,
            team_alignment=team_alignment,
        )

        # Determine decision
        must_fix = []
        follow_ups = []

        if coverage >= 4 and evidence_score >= 3 and team_alignment >= 4:
            decision = "APPROVE"
        elif iteration >= plan.max_iterations - 1:
            decision = "APPROVE"  # Out of iterations
            must_fix.append("Max iterations reached")
        elif budget_used_percent > 90:
            decision = "APPROVE"  # Out of budget
            must_fix.append("Budget nearly exhausted")
        elif not evidence and iteration > 0:
            decision = "ESCALATE"
            must_fix.append("No evidence collected despite attempts")
        else:
            decision = "CONTINUE"

            # Generate follow-up questions
            for q in p0_questions:
                answered = False
                for claim in claims:
                    c_keywords = set(claim.statement.lower().split())
                    q_keywords = set(q.question.lower().split())
                    if len(q_keywords & c_keywords) >= 2:
                        answered = True
                        break

                if not answered:
                    follow_ups.append(FollowUpQuestion(
                        question=q.question,
                        why="P0 question not yet answered",
                        suggested_tools=q.suggested_tools,
                        qid=q.qid,
                    ))

        return Critique(
            decision=decision,
            scores=scores,
            must_fix=must_fix,
            follow_up_questions=follow_ups[:3],
            risky_claims=[],
            contradictions=[],
            values_violations=[],
        )
