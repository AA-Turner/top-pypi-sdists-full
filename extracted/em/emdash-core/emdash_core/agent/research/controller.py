"""Research controller for orchestrating the research loop.

The Controller manages the research cycle:
1. Plan -> questions
2. Research -> evidence, claims
3. Critique -> decision
4. If not approved, back to 2 or adjust plan
5. Synthesize final report
"""

from typing import Optional

from rich.console import Console

from ..events import AgentEventEmitter, NullEmitter
from ..providers.models import ModelRegistry
from .state import (
    ResearchState,
    IterationResult,
)
from .planner import PlannerAgent
from .researcher import ResearcherAgent
from .critic import CriticAgent
from .synthesizer import SynthesizerAgent


# Model tiers for escalation
def _get_config_model_tiers() -> dict[str, str]:
    """Build model tiers from registry config."""
    registry = ModelRegistry.get()
    fallback = registry.default_model
    if not fallback:
        raise ValueError("No default_model configured in model registry.")

    fast = registry.fast_model or fallback
    standard = fallback
    powerful = registry.vision_model or standard

    return {
        "fast": fast,
        "standard": standard,
        "powerful": powerful,
    }


class ResearchController:
    """Orchestrates the multi-agent research loop.

    The Controller coordinates:
    - PlannerAgent: Creates research plan
    - ResearcherAgent: Executes tools, collects evidence
    - CriticAgent: Evaluates progress
    - SynthesizerAgent: Writes final report

    It handles model tier escalation and budget management.
    """

    def __init__(
        self,
        model_tier: str = "fast",
        verbose: bool = True,
        emitter: Optional[AgentEventEmitter] = None,
    ):
        """Initialize the research controller.

        Args:
            model_tier: Initial model tier (fast, standard, powerful)
            verbose: Whether to print progress
            emitter: Event emitter for unified output
        """
        self.model_tier = model_tier
        self.verbose = verbose
        self.console = Console()
        self.emitter = emitter or NullEmitter(agent_name="ResearchController")
        self._model_tiers = _get_config_model_tiers()

        # Initialize agents with current model tier
        model = self._model_tiers.get(model_tier, self._model_tiers["fast"])
        self.planner = PlannerAgent(model=model, verbose=verbose)
        self.researcher = ResearcherAgent(model=model, verbose=verbose, emitter=self.emitter)
        self.critic = CriticAgent(model=model, verbose=verbose)
        self.synthesizer = SynthesizerAgent(model=model, verbose=verbose)

    def research(
        self,
        goal: str,
        context: str = "",
        max_iterations: int = 3,
        budgets: Optional[dict] = None,
    ) -> tuple[str, ResearchState]:
        """Execute the full research loop.

        Args:
            goal: Research goal
            context: Additional context
            max_iterations: Maximum iterations
            budgets: Resource budgets

        Returns:
            Tuple of (final_report, research_state)
        """
        if self.verbose:
            self.console.print(f"\n[bold cyan]Starting research: {goal}[/bold cyan]\n")

        # Phase 1: Planning
        plan = self.planner.create_plan(
            goal=goal,
            context=context,
            max_iterations=max_iterations,
            budgets=budgets,
        )

        # Initialize state
        state = ResearchState(plan=plan)

        # Phase 2: Research Loop
        while state.iteration < plan.max_iterations:
            if self.verbose:
                self.console.print(f"\n[cyan]--- Iteration {state.iteration + 1} ---[/cyan]")

            # Get questions for this iteration
            questions = self._get_questions_for_iteration(state)
            if not questions:
                if self.verbose:
                    self.console.print("[yellow]No more questions to investigate[/yellow]")
                break

            # Run research
            evidence, updated_context = self.researcher.run_macros(
                questions=questions,
                context=state.context,
                budget=state.remaining_budget,
            )

            # Update context
            state.context.update(updated_context)

            # Update budget
            state.remaining_budget["tool_calls"] = max(
                0,
                state.remaining_budget.get("tool_calls", 0) - len(evidence)
            )

            # Generate claims
            all_prior_claims = state.get_all_claims()
            claims = self.researcher.propose_claims(
                goal=plan.goal,
                questions=questions,
                evidence=evidence,
                prior_claims=all_prior_claims,
            )

            # Identify gaps
            gaps = self.researcher.identify_gaps(plan, claims, evidence)

            # Critique
            critique = self.critic.evaluate(
                plan=plan,
                evidence=evidence,
                claims=claims,
                gaps=gaps,
                iteration=state.iteration,
                budget_used_percent=state.budget_used_percent(),
            )

            # Record iteration
            result = IterationResult(
                iteration=state.iteration,
                evidence=evidence,
                claims=claims,
                gaps=gaps,
                critique=critique,
                model_tier=self.model_tier,
            )
            state.history.append(result)
            state.iteration += 1

            # Check decision
            if critique.decision == "APPROVE":
                if self.verbose:
                    self.console.print("[green]Research APPROVED[/green]")
                break

            elif critique.decision == "ESCALATE":
                if self._escalate_model():
                    if self.verbose:
                        self.console.print(f"[yellow]Escalated to {self.model_tier}[/yellow]")
                else:
                    if self.verbose:
                        self.console.print("[yellow]Cannot escalate further[/yellow]")
                    break

            elif critique.decision == "REJECT":
                if self.verbose:
                    self.console.print("[red]Research REJECTED[/red]")
                    for issue in critique.must_fix:
                        self.console.print(f"  - {issue}")
                # Try to fix in next iteration

            # Add follow-up questions to queue
            for followup in critique.follow_up_questions:
                if followup.qid and followup.qid not in state.answered_questions:
                    if followup.qid not in state.question_queue:
                        state.question_queue.insert(0, followup.qid)

        # Phase 3: Synthesis
        report = self.synthesizer.write(plan, state.history)

        return report, state

    def _get_questions_for_iteration(
        self,
        state: ResearchState,
    ) -> list:
        """Get questions to investigate in this iteration.

        Prioritizes P0, then P1, then follow-ups from Critic.

        Args:
            state: Current research state

        Returns:
            List of ResearchQuestion objects
        """
        questions = []

        # Take from queue
        qids_to_process = state.question_queue[:3]  # Up to 3 at a time

        for qid in qids_to_process:
            question = state.get_question_by_qid(qid)
            if question and qid not in state.answered_questions:
                questions.append(question)
                state.answered_questions.add(qid)

        # Remove processed from queue
        for qid in qids_to_process:
            if qid in state.question_queue:
                state.question_queue.remove(qid)

        return questions

    def _escalate_model(self) -> bool:
        """Escalate to a more powerful model tier.

        Returns:
            True if escalation was possible
        """
        tiers = ["fast", "standard", "powerful"]
        current_idx = tiers.index(self.model_tier) if self.model_tier in tiers else 0

        if current_idx >= len(tiers) - 1:
            return False

        self.model_tier = tiers[current_idx + 1]
        model = self._model_tiers[self.model_tier]

        # Reinitialize agents with new model
        self.planner = PlannerAgent(model=model, verbose=self.verbose)
        self.researcher = ResearcherAgent(
            model=model, verbose=self.verbose, emitter=self.emitter
        )
        self.critic = CriticAgent(model=model, verbose=self.verbose)
        self.synthesizer = SynthesizerAgent(model=model, verbose=self.verbose)

        return True
