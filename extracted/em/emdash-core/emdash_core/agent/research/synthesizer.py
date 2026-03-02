"""Synthesizer agent for generating final research reports.

The Synthesizer produces team-usable final reports that include:
1. Findings (Fact-only) - claims with evidence IDs
2. Evidence Coverage Matrix - questions vs evidence
3. Design/Spec Implications
4. Risks & Unknowns - gaps + impact
5. Recommended Tasks - actionable items
6. Execution-Ready Work Packages - sprint grouping + DoD + acceptance tests
7. Capacity & Sizing - T-shirt sizes and capacity notes
8. Reviewer Checklist - what to verify in PRs
9. Tooling Summary - macros, calls, budgets

Hard rules:
- No claim appears without evidence IDs
- Unknowns must be explicit, not hidden
"""

import json
from typing import Optional

from rich.console import Console

from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL
from ..compaction import LLMCompactor
from .state import (
    ResearchState,
    ResearchPlan,
    IterationResult,
    EvidenceItem,
    Claim,
    Gap,
    Contradiction,
)


SYNTHESIZER_SYSTEM_PROMPT = """You are a research synthesizer that produces team-usable reports.

Your job is to combine research findings into a structured report that helps the team take action.

REQUIRED SECTIONS (in order):

## Findings
- List claims with evidence IDs: "**C7** [E12, E13]: Statement here"
- Group by topic/question
- Only include claims that have evidence

## Evidence Coverage Matrix
- Show which questions are covered by which evidence
- Format as markdown table
- Highlight gaps

## Design/Spec Implications
- What must be true for implementation
- Design constraints discovered
- Patterns to follow

## Risks & Unknowns
- List all gaps
- Impact of unknowns
- How to close gaps

## Recommended Tasks
- Actionable items
- Map each task to evidence
- Include owner placeholders: "**Owner TBD**"

## Execution-Ready Work Packages
- Group Phase 1 tasks into sprints
- Each task includes: T-shirt size (XS/S/M/L/XL), Definition of Done, Acceptance Tests
- Keep dependencies explicit

## Capacity & Sizing
- Roll up T-shirt sizing per sprint
- Note owner gaps and capacity risks

## Reviewer Checklist
- What to verify in PRs
- Critical paths to check
- Tests to ensure

## Tooling Summary
- Macro runs
- Tool calls made
- Budget used

## Planning Artifacts
- Recommend JSON task export to Jira/Linear for execution tracking

CRITICAL RULES:
- Every claim must show evidence IDs
- No ungrounded statements
- Gaps must be explicit
- Use team vocabulary"""


class SynthesizerAgent:
    """Generates final report with required sections.

    The Synthesizer transforms raw research data into a
    structured, team-usable report.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
    ):
        """Initialize the synthesizer agent.

        Args:
            model: LLM model to use
            verbose: Whether to print progress
        """
        self.provider = get_provider(model)
        self.model = model
        self.verbose = verbose
        self.console = Console()
        self.compactor = LLMCompactor(self.provider)

    def write(
        self,
        plan: ResearchPlan,
        history: list[IterationResult],
    ) -> str:
        """Generate final report from research state.

        Args:
            plan: Research plan
            history: All iteration results

        Returns:
            Markdown report string
        """
        if self.verbose:
            self.console.print("[cyan]Synthesizing final report...[/cyan]")

        # Gather all data
        all_evidence = []
        all_claims = []
        all_gaps = []
        all_contradictions = []

        for result in history:
            all_evidence.extend(result.evidence)
            all_claims.extend(result.claims)
            all_gaps.extend(result.gaps)
            all_contradictions.extend(result.critique.contradictions)

        # Try LLM-based synthesis
        try:
            report = self._llm_synthesize(plan, all_evidence, all_claims, all_gaps, all_contradictions, history)
            if report and len(report) > 500:
                if self.verbose:
                    self.console.print("[green]Report synthesized[/green]")
                return report
        except Exception as e:
            if self.verbose:
                self.console.print(f"[yellow]LLM synthesis failed: {e}. Using template.[/yellow]")

        # Fallback to template-based synthesis
        return self._template_synthesize(plan, all_evidence, all_claims, all_gaps, all_contradictions, history)

    def _llm_synthesize(
        self,
        plan: ResearchPlan,
        evidence: list[EvidenceItem],
        claims: list[Claim],
        gaps: list[Gap],
        contradictions: list[Contradiction],
        history: list[IterationResult],
    ) -> Optional[str]:
        """Synthesize using LLM.

        Args:
            plan: Research plan
            evidence: All evidence
            claims: All claims
            gaps: All gaps
            contradictions: All contradictions
            history: Iteration history

        Returns:
            Report string or None
        """
        # Build context for LLM
        claims_text = "\n".join([
            f"- {c.id} (conf={c.confidence}, evidence={c.evidence_ids}): {c.statement}"
            for c in claims
        ]) or "No claims"

        evidence_text = "\n".join([
            f"- {e.id}: {e.tool} -> {e.summary}"
            for e in evidence[:30]  # Limit
        ]) or "No evidence"

        gaps_text = "\n".join([
            f"- {g.question} (reason: {g.reason})"
            for g in gaps
        ]) or "No gaps"

        contradictions_text = "\n".join([
            f"- {c.claim_a} vs {c.claim_b}: {c.note}"
            for c in contradictions
        ]) or "No contradictions"

        questions_text = "\n".join([
            f"- [{q.priority}] {q.qid}: {q.question}"
            for q in plan.questions
        ])

        # Calculate stats
        total_tool_calls = len(evidence)
        iterations = len(history)

        payload = {
            "questions": questions_text,
            "claims": claims_text,
            "evidence": evidence_text,
            "gaps": gaps_text,
            "contradictions": contradictions_text,
        }
        compacted = self.compactor.compact_payload(payload, plan.goal)
        questions_text = compacted.get("questions", questions_text)
        claims_text = compacted.get("claims", claims_text)
        evidence_text = compacted.get("evidence", evidence_text)
        gaps_text = compacted.get("gaps", gaps_text)
        contradictions_text = compacted.get("contradictions", contradictions_text)

        user_message = f"""Synthesize a research report from this data.

RESEARCH GOAL: {plan.goal}

QUESTIONS INVESTIGATED:
{questions_text}

CLAIMS (with evidence):
{claims_text}

EVIDENCE COLLECTED:
{evidence_text}

GAPS (unanswered):
{gaps_text}

CONTRADICTIONS:
{contradictions_text}

STATS:
- Iterations: {iterations}
- Tool calls: {total_tool_calls}
- Claims: {len(claims)}
- Gaps: {len(gaps)}

Generate a complete research report with all required sections.
Start with "# Research Report: [topic]"
"""

        messages = [
            {"role": "user", "content": user_message},
        ]

        response = self.provider.chat(messages, system=SYNTHESIZER_SYSTEM_PROMPT)
        return response.content

    def _template_synthesize(
        self,
        plan: ResearchPlan,
        evidence: list[EvidenceItem],
        claims: list[Claim],
        gaps: list[Gap],
        contradictions: list[Contradiction],
        history: list[IterationResult],
    ) -> str:
        """Synthesize using template.

        Fallback method for structured report generation.
        """
        sections = []

        # Title
        sections.append(f"# Research Report: {plan.goal}\n")

        # Summary
        sections.append("## Executive Summary\n")
        sections.append(f"This report summarizes research into: **{plan.goal}**\n")
        sections.append(f"- **{len(claims)}** claims established")
        sections.append(f"- **{len(evidence)}** evidence items collected")
        sections.append(f"- **{len(gaps)}** gaps identified")
        sections.append(f"- **{len(history)}** research iterations\n")

        # Findings
        sections.append("## Findings\n")
        sections.append(self._format_findings(claims))

        # Evidence Coverage Matrix
        sections.append("## Evidence Coverage Matrix\n")
        sections.append(self._build_coverage_matrix(plan, claims, evidence))

        # Design/Spec Implications
        sections.append("## Design/Spec Implications\n")
        sections.append(self._format_implications(claims))

        # Risks & Unknowns
        sections.append("## Risks & Unknowns\n")
        sections.append(self._format_risks(gaps, contradictions))

        # Recommended Tasks
        sections.append("## Recommended Tasks\n")
        sections.append(self._format_tasks(claims, gaps))

        # Execution-Ready Work Packages
        sections.append("## Execution-Ready Work Packages\n")
        sections.append(
            "### Sprint 1 (Phase 1)\n"
            "- Task: [Owner TBD] (Size: M)\n"
            "  - Definition of Done: Documented artifacts delivered\n"
            "  - Acceptance Tests: Evidence-backed review checklist complete\n\n"
            "### Sprint 2 (Phase 1)\n"
            "- Task: [Owner TBD] (Size: M)\n"
            "  - Definition of Done: Dependencies mapped\n"
            "  - Acceptance Tests: Dependency graph reviewed\n\n"
            "### Sprint 3 (Phase 1)\n"
            "- Task: [Owner TBD] (Size: S)\n"
            "  - Definition of Done: Test inventory documented\n"
            "  - Acceptance Tests: Coverage gaps recorded\n"
        )

        # Capacity & Sizing
        sections.append("## Capacity & Sizing\n")
        sections.append(
            "- Sprint 1: M\n"
            "- Sprint 2: M\n"
            "- Sprint 3: S\n"
            "- Owners: TBD (capacity risk until ownership assigned)\n"
        )

        # Reviewer Checklist
        sections.append("## Reviewer Checklist\n")
        sections.append(self._format_checklist(claims, evidence))

        # Tooling Summary
        sections.append("## Tooling Summary\n")
        sections.append(self._format_tooling(evidence, history, plan))

        # Planning Artifacts
        sections.append("## Planning Artifacts\n")
        sections.append("- Export tasks as JSON for Jira/Linear indexing\n")

        return "\n".join(sections)

    def _format_findings(self, claims: list[Claim]) -> str:
        """Format claims as findings."""
        if not claims:
            return "_No findings established._\n"

        lines = []

        # Group by confidence
        high_conf = [c for c in claims if c.confidence >= 2]
        low_conf = [c for c in claims if c.confidence < 2]

        if high_conf:
            lines.append("### High Confidence\n")
            for claim in high_conf:
                evidence_str = ", ".join(claim.evidence_ids)
                lines.append(f"- **{claim.id}** [{evidence_str}]: {claim.statement}")
            lines.append("")

        if low_conf:
            lines.append("### Lower Confidence\n")
            for claim in low_conf:
                evidence_str = ", ".join(claim.evidence_ids)
                assumptions_str = ""
                if claim.assumptions:
                    assumptions_str = f" _(Assumptions: {', '.join(claim.assumptions)})_"
                lines.append(f"- **{claim.id}** [{evidence_str}]: {claim.statement}{assumptions_str}")
            lines.append("")

        return "\n".join(lines)

    def _build_coverage_matrix(
        self,
        plan: ResearchPlan,
        claims: list[Claim],
        evidence: list[EvidenceItem],
    ) -> str:
        """Build evidence coverage matrix."""
        lines = []

        # Header
        lines.append("| Question | Priority | Evidence | Claims | Status |")
        lines.append("|----------|----------|----------|--------|--------|")

        for question in plan.questions:
            # Find related claims and evidence
            q_keywords = set(question.question.lower().split())

            related_claims = []
            related_evidence = set()

            for claim in claims:
                c_keywords = set(claim.statement.lower().split())
                if len(q_keywords & c_keywords) >= 2:
                    related_claims.append(claim.id)
                    related_evidence.update(claim.evidence_ids)

            # Status
            if related_claims:
                if any(c.confidence >= 2 for c in claims if c.id in related_claims):
                    status = "Answered"
                else:
                    status = "Partial"
            else:
                status = "Gap"

            evidence_str = ", ".join(list(related_evidence)[:3])
            if len(related_evidence) > 3:
                evidence_str += "..."

            claims_str = ", ".join(related_claims[:3])
            if len(related_claims) > 3:
                claims_str += "..."

            lines.append(
                f"| {question.question[:40]}... | {question.priority} | "
                f"{evidence_str or '-'} | {claims_str or '-'} | {status} |"
            )

        lines.append("")
        return "\n".join(lines)

    def _format_implications(self, claims: list[Claim]) -> str:
        """Format design/spec implications."""
        if not claims:
            return "_No implications identified._\n"

        lines = []

        # Extract implications from high-confidence claims
        high_conf = [c for c in claims if c.confidence >= 2]

        if high_conf:
            lines.append("Based on the research findings:\n")
            for i, claim in enumerate(high_conf[:10], 1):
                lines.append(f"{i}. {claim.statement} (from {', '.join(claim.evidence_ids)})")
            lines.append("")
        else:
            lines.append("_Limited high-confidence findings. More research needed._\n")

        return "\n".join(lines)

    def _format_risks(
        self,
        gaps: list[Gap],
        contradictions: list[Contradiction],
    ) -> str:
        """Format risks and unknowns."""
        lines = []

        if gaps:
            lines.append("### Unanswered Questions\n")
            for gap in gaps:
                tools_str = ", ".join(gap.suggested_tools) if gap.suggested_tools else "manual investigation"
                lines.append(f"- **{gap.question}**")
                lines.append(f"  - Reason: {gap.reason}")
                lines.append(f"  - Suggested: {tools_str}")
            lines.append("")

        if contradictions:
            lines.append("### Contradictions (Unresolved)\n")
            for c in contradictions:
                lines.append(f"- **{c.claim_a}** vs **{c.claim_b}**: {c.note}")
            lines.append("")

        if not gaps and not contradictions:
            lines.append("_No significant risks or unknowns identified._\n")

        return "\n".join(lines)

    def _format_tasks(
        self,
        claims: list[Claim],
        gaps: list[Gap],
    ) -> str:
        """Format recommended tasks."""
        lines = []
        task_num = 1

        # Tasks from high-confidence findings
        high_conf = [c for c in claims if c.confidence >= 2]
        if high_conf:
            lines.append("### Based on Findings\n")
            for claim in high_conf[:5]:
                lines.append(f"{task_num}. Implement based on {claim.id}: {claim.statement[:60]}...")
                lines.append(f"   - **Owner**: TBD")
                lines.append(f"   - **Evidence**: {', '.join(claim.evidence_ids)}")
                task_num += 1
            lines.append("")

        # Tasks from gaps
        if gaps:
            lines.append("### To Close Gaps\n")
            for gap in gaps[:5]:
                lines.append(f"{task_num}. Investigate: {gap.question}")
                lines.append(f"   - **Owner**: TBD")
                lines.append(f"   - **Tools**: {', '.join(gap.suggested_tools)}")
                task_num += 1
            lines.append("")

        if not high_conf and not gaps:
            lines.append("_No specific tasks recommended. More research needed._\n")

        return "\n".join(lines)

    def _format_checklist(
        self,
        claims: list[Claim],
        evidence: list[EvidenceItem],
    ) -> str:
        """Format reviewer checklist."""
        lines = []

        # Extract file paths from evidence
        files = set()
        for e in evidence:
            for entity in e.entities:
                if "/" in entity or entity.endswith(".py") or entity.endswith(".ts"):
                    files.add(entity)

        if files:
            lines.append("### Files to Review\n")
            for f in list(files)[:15]:
                lines.append(f"- [ ] `{f}`")
            lines.append("")

        # Checklist items from claims
        if claims:
            lines.append("### Verification Points\n")
            for claim in claims[:10]:
                lines.append(f"- [ ] Verify: {claim.statement[:60]}... ({claim.id})")
            lines.append("")

        # General checklist
        lines.append("### General Checks\n")
        lines.append("- [ ] Tests pass")
        lines.append("- [ ] No regressions in affected areas")
        lines.append("- [ ] Documentation updated if needed")
        lines.append("- [ ] Code follows project patterns")
        lines.append("")

        return "\n".join(lines)

    def _format_tooling(
        self,
        evidence: list[EvidenceItem],
        history: list[IterationResult],
        plan: ResearchPlan,
    ) -> str:
        """Format tooling summary."""
        lines = []

        # Tool usage stats
        tool_counts: dict[str, int] = {}
        for e in evidence:
            tool_counts[e.tool] = tool_counts.get(e.tool, 0) + 1

        lines.append("### Tool Usage\n")
        lines.append("| Tool | Calls |")
        lines.append("|------|-------|")
        for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {tool} | {count} |")
        lines.append("")

        # Iteration summary
        lines.append("### Iteration History\n")
        for result in history:
            decision = result.critique.decision
            lines.append(
                f"- Iteration {result.iteration + 1}: "
                f"{len(result.evidence)} evidence, {len(result.claims)} claims -> {decision}"
            )
        lines.append("")

        # Budget summary
        lines.append("### Budget\n")
        total_calls = len(evidence)
        budget = plan.budgets.get("tool_calls", 50)
        lines.append(f"- Tool calls: {total_calls}/{budget} ({total_calls/budget*100:.0f}%)")
        lines.append(f"- Iterations: {len(history)}/{plan.max_iterations}")
        lines.append("")

        return "\n".join(lines)
