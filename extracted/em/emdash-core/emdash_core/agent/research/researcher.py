"""Researcher agent for executing tool macros and collecting evidence.

The Researcher executes tool macros to gather evidence for research questions.
It produces:
- EvidenceItem list (machine-verifiable)
- Claim list (grounded statements)
- Gap list (explicit unknowns)

Team values enforced:
- V1: Prefer "unknown" over guesses
- V2: All evidence is reproducible (tool calls documented)
- V4: Cost awareness (uses budget limits)
"""

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from rich.console import Console

from ..toolkit import AgentToolkit
from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL
from ...core.config import get_config
from ..events import AgentEventEmitter, NullEmitter
from .state import (
    EvidenceItem,
    Claim,
    Gap,
    ResearchQuestion,
    ResearchPlan,
)
from .macros import (
    MacroExecutor,
    suggest_macros,
    TOOL_MACROS,
)
from ..compaction import LLMCompactor


RESEARCHER_SYSTEM_PROMPT = """You are a research analyst that extracts claims from collected evidence.

CRITICAL RULES:
1. EVERY piece of evidence contains findings - extract them!
2. NEVER say "X results were found but not examined" - READ the evidence details
3. Each claim MUST cite evidence IDs (e.g., "based on E1, E3")
4. Report WHAT was found, not just that something was found

You will receive:
1. A research goal
2. Questions to answer
3. DETAILED evidence with actual entities, names, and content

YOUR JOB - Extract claims from evidence:
1. READ each evidence item carefully - it contains actual names and details
2. MAKE CLAIMS about what the evidence shows (entities, patterns, relationships)
3. If the exact topic wasn't found, claim what WAS found (it's still valuable)
4. Identify GAPS only for questions with truly no relevant evidence

CLAIM FORMAT:
{
  "id": "C1",
  "statement": "The codebase contains a WebScrapeService class that handles web scraping operations",
  "evidence_ids": ["E1", "E3"],
  "confidence": 2,
  "assumptions": []
}

Confidence levels:
- 1: Single source, may have assumptions
- 2: Multiple sources corroborate (requires 2+ evidence_ids)
- 3: Strong evidence, no assumptions

GAP FORMAT (only when evidence truly missing):
{
  "question": "What tests cover the toolkit?",
  "reason": "No test files found in any search results",
  "suggested_tools": ["text_search"]
}

OUTPUT FORMAT (JSON only, no markdown):
{
  "claims": [...],
  "gaps": [...],
  "summary": "Brief summary of key findings"
}

IMPORTANT: Evidence contains ACTUAL entity names and details. Extract them into claims."""


class ResearcherAgent:
    """Executes tool macros, collects evidence, proposes claims.

    The Researcher is the "hands" of the research process. It:
    1. Runs appropriate tool macros for each question
    2. Collects evidence with unique IDs
    3. Proposes claims grounded in evidence
    4. Identifies gaps where evidence is missing
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
        emitter: Optional[AgentEventEmitter] = None,
    ):
        """Initialize the researcher agent.

        Args:
            model: LLM model to use for claim generation
            verbose: Whether to print progress
            emitter: Event emitter for unified message stream
        """
        self.provider = get_provider(model)
        self.model = model
        self.verbose = verbose
        self.console = Console()
        self.toolkit = AgentToolkit(enable_session=True)
        self.macro_executor = MacroExecutor(self.toolkit)
        self.claim_counter = 0
        self.emitter = emitter or NullEmitter(agent_name="ResearcherAgent")
        self.compactor = LLMCompactor(self.provider)

        # Check if GitHub MCP is available
        config = get_config()
        self._mcp_available = config.mcp.is_available

    def run_macros(
        self,
        questions: list[ResearchQuestion],
        context: dict,
        budget: dict,
        parallel: bool = True,
        max_workers: int = 3,
    ) -> tuple[list[EvidenceItem], dict]:
        """Execute appropriate macros for questions.

        Args:
            questions: Research questions to investigate
            context: Prior context from previous iterations
            budget: Remaining budget {tool_calls, tokens, time_s}
            parallel: Whether to run questions in parallel (default True)
            max_workers: Max parallel workers (default 3)

        Returns:
            Tuple of (evidence_items, updated_context)
        """
        all_evidence: list[EvidenceItem] = []
        updated_context = dict(context)
        budget_remaining = budget.get("tool_calls", 50)

        # Step 1: Bootstrap search (sequential - establishes shared context)
        if not updated_context.get("last_search_results") and questions:
            # Use first question's topic for bootstrap
            first_topic = self._extract_topic(questions[0].question)
            evidence, ctx_updates, budget_remaining = self._bootstrap_search(
                topic=first_topic,
                budget_remaining=budget_remaining,
            )
            all_evidence.extend(evidence)
            updated_context.update(ctx_updates)

        if budget_remaining <= 0:
            if self.verbose:
                self.console.print("[yellow]Budget exhausted after bootstrap[/yellow]")
            return all_evidence, updated_context

        # Step 2: Run macro execution for each question
        if parallel and len(questions) > 1:
            # Parallel execution
            evidence, ctx = self._run_questions_parallel(
                questions=questions,
                context=updated_context,
                budget_remaining=budget_remaining,
                max_workers=max_workers,
            )
            all_evidence.extend(evidence)
            updated_context.update(ctx)
        else:
            # Sequential execution (for single question or when parallel=False)
            for question in questions:
                if budget_remaining <= 0:
                    if self.verbose:
                        self.console.print("[yellow]Budget exhausted[/yellow]")
                    break

                evidence, ctx, budget_remaining = self._run_single_question(
                    question=question,
                    context=updated_context,
                    budget_remaining=budget_remaining,
                )
                all_evidence.extend(evidence)
                updated_context.update(ctx)

        return all_evidence, updated_context

    def _run_single_question(
        self,
        question: ResearchQuestion,
        context: dict,
        budget_remaining: int,
    ) -> tuple[list[EvidenceItem], dict, int]:
        """Run macros for a single question.

        Args:
            question: Research question to investigate
            context: Current context
            budget_remaining: Remaining budget

        Returns:
            Tuple of (evidence, context_updates, remaining_budget)
        """
        evidence: list[EvidenceItem] = []
        ctx_updates: dict = {}

        if self.verbose:
            self.console.print(f"[dim]Investigating: {question.question}[/dim]")

        topic = self._extract_topic(question.question)

        if budget_remaining > 0 and context.get("last_search_results"):
            macros_to_run = question.suggested_tools or suggest_macros(
                question.question,
                include_github=self._mcp_available
            )

            for macro_name in macros_to_run:
                if budget_remaining <= 0:
                    break

                if macro_name not in TOOL_MACROS:
                    continue

                params = {"topic": topic, "symbol": topic}

                if "last_search_top" in context:
                    top_result = context["last_search_top"]
                    params["identifier"] = top_result.get("qualified_name", topic)

                try:
                    ev, ctx = self.macro_executor.execute_macro(
                        macro_name=macro_name,
                        params=params,
                        budget_remaining=budget_remaining,
                        prior_context=context,
                    )

                    evidence.extend(ev)
                    ctx_updates.update(ctx)
                    budget_remaining -= len(ev)

                    if self.verbose:
                        self.console.print(f"  [green]{macro_name}: {len(ev)} evidence[/green]")

                except Exception as e:
                    if self.verbose:
                        self.console.print(f"  [red]{macro_name}: {e}[/red]")

        return evidence, ctx_updates, budget_remaining

    def _run_questions_parallel(
        self,
        questions: list[ResearchQuestion],
        context: dict,
        budget_remaining: int,
        max_workers: int = 3,
    ) -> tuple[list[EvidenceItem], dict]:
        """Run multiple questions in parallel using thread pool.

        Args:
            questions: Research questions to investigate
            context: Shared context from bootstrap
            budget_remaining: Total remaining budget
            max_workers: Max parallel workers

        Returns:
            Tuple of (all_evidence, merged_context)
        """
        all_evidence: list[EvidenceItem] = []
        merged_context: dict = {}

        # Distribute budget among questions (with some buffer)
        budget_per_question = max(5, budget_remaining // len(questions))

        if self.verbose:
            self.console.print(
                f"[dim]Running {len(questions)} questions in parallel "
                f"({max_workers} workers, {budget_per_question} budget each)[/dim]"
            )

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all questions
            future_to_question = {
                executor.submit(
                    self._run_single_question,
                    question=q,
                    context=context,
                    budget_remaining=budget_per_question,
                ): q
                for q in questions
            }

            # Collect results as they complete
            for future in as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    evidence, ctx_updates, _ = future.result()
                    all_evidence.extend(evidence)
                    merged_context.update(ctx_updates)
                except Exception as e:
                    if self.verbose:
                        self.console.print(
                            f"[red]Question failed: {question.question[:50]}... - {e}[/red]"
                        )

        return all_evidence, merged_context

    def _bootstrap_search(
        self,
        topic: str,
        budget_remaining: int,
    ) -> tuple[list[EvidenceItem], dict, int]:
        """Bootstrap context with direct search calls.

        Args:
            topic: The topic to search for
            budget_remaining: Remaining tool call budget

        Returns:
            Tuple of (evidence, context_updates, remaining_budget)
        """
        evidence: list[EvidenceItem] = []
        context: dict = {}

        # Try semantic search
        try:
            result = self.toolkit.execute(
                "semantic_search",
                query=topic,
                limit=10,
                min_score=0.3,
            )
            budget_remaining -= 1

            if result.success and result.data.get("results"):
                self.macro_executor.evidence_counter += 1
                ev = EvidenceItem(
                    id=f"E{self.macro_executor.evidence_counter}",
                    tool="semantic_search",
                    input={"query": topic, "limit": 10},
                    output_ref=f"result_{self.macro_executor.evidence_counter}",
                    summary=f"Search for '{topic}': {len(result.data['results'])} results",
                    entities=[r.get("qualified_name", "") for r in result.data["results"][:5]],
                )
                evidence.append(ev)

                context["last_search_results"] = result.data["results"]
                context["last_search_top"] = result.data["results"][0]

                if self.verbose:
                    self.console.print(f"  [green]search: {len(result.data['results'])} results[/green]")

        except Exception as e:
            if self.verbose:
                self.console.print(f"  [dim]search failed: {e}[/dim]")

        return evidence, context, budget_remaining

    def propose_claims(
        self,
        goal: str,
        questions: list[ResearchQuestion],
        evidence: list[EvidenceItem],
        prior_claims: list[Claim] = None,
    ) -> list[Claim]:
        """Generate claims grounded in evidence.

        Args:
            goal: Research goal
            questions: Questions being answered
            evidence: Evidence collected
            prior_claims: Claims from previous iterations

        Returns:
            List of new Claims
        """
        if not evidence:
            return []

        # Build evidence summary for LLM
        evidence_text = "\n".join([
            f"[{e.id}] {e.tool}: {e.summary}"
            for e in evidence
        ])

        questions_text = "\n".join([
            f"- [{q.priority}] {q.question}"
            for q in questions
        ])

        prior_text = ""
        if prior_claims:
            prior_text = "\nPRIOR CLAIMS:\n" + "\n".join([
                f"- {c.statement}" for c in prior_claims
            ])

        user_message = f"""Extract claims from evidence.

GOAL: {goal}

QUESTIONS:
{questions_text}

EVIDENCE:
{evidence_text}
{prior_text}

Return JSON with claims and gaps."""

        messages = [{"role": "user", "content": user_message}]
        response = self.provider.chat(messages, system=RESEARCHER_SYSTEM_PROMPT)

        return self._parse_claims(response.content or "", evidence)

    def _parse_claims(
        self,
        content: str,
        evidence: list[EvidenceItem],
    ) -> list[Claim]:
        """Parse claims from LLM response."""
        claims = []
        evidence_ids = {e.id for e in evidence}

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

            for c in data.get("claims", []):
                claim_evidence = c.get("evidence_ids", [])
                valid_evidence = [eid for eid in claim_evidence if eid in evidence_ids]

                if not valid_evidence:
                    continue

                self.claim_counter += 1

                confidence = c.get("confidence", 1)
                assumptions = c.get("assumptions", [])

                if confidence >= 2 and len(valid_evidence) < 2:
                    confidence = 1
                if assumptions and confidence > 1:
                    confidence = 1

                try:
                    claim = Claim(
                        id=c.get("id", f"C{self.claim_counter}"),
                        statement=c["statement"],
                        evidence_ids=valid_evidence,
                        confidence=confidence,
                        assumptions=assumptions,
                    )
                    claims.append(claim)
                except ValueError:
                    pass

        except (json.JSONDecodeError, KeyError, TypeError):
            pass

        return claims

    def identify_gaps(
        self,
        plan: ResearchPlan,
        claims: list[Claim],
        evidence: list[EvidenceItem],
    ) -> list[Gap]:
        """Identify questions that couldn't be answered."""
        gaps = []

        for question in plan.questions:
            if question.priority == "P2":
                continue

            # Check if any claim addresses this question
            question_addressed = False
            question_lower = question.question.lower()

            for claim in claims:
                claim_lower = claim.statement.lower()
                keywords = self._extract_keywords(question_lower)

                if any(kw in claim_lower for kw in keywords):
                    question_addressed = True
                    break

            if not question_addressed:
                gaps.append(Gap(
                    question=question.question,
                    reason="No relevant claims found",
                    suggested_tools=question.suggested_tools or ["semantic_search"],
                ))

        return gaps

    def _extract_topic(self, question: str) -> str:
        """Extract the main topic from a question."""
        topic = question.lower()
        patterns = [
            "what is the feature/behavior of ",
            "where is ",
            "what depends on ",
            "who owns or touches ",
            "what's risky about ",
            "what tests/ci validate ",
            "what should a reviewer check for ",
            "how does ",
            "what is ",
        ]

        for pattern in patterns:
            if topic.startswith(pattern):
                topic = topic[len(pattern):]
                break

        return topic.rstrip("?!.").strip() or question

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract keywords from text for matching."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be",
            "to", "of", "in", "for", "on", "with", "at", "by",
            "what", "where", "who", "how", "why", "when",
        }

        words = text.lower().split()
        return [w.strip("?!.,") for w in words if w not in stopwords and len(w) > 2]
