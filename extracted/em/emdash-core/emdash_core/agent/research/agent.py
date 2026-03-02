"""Deep Research Agent - main entry point.

Provides a simple interface for deep code research using the
multi-agent research system.
"""

from typing import Optional

from rich.console import Console

from ..events import AgentEventEmitter, NullEmitter
from .controller import ResearchController
from .state import ResearchState


class DeepResearchAgent:
    """High-level interface for deep code research.

    Wraps the ResearchController with a simpler API.

    Example:
        agent = DeepResearchAgent()
        report = agent.research("How does authentication work?")
        print(report)
    """

    def __init__(
        self,
        model_tier: str = "fast",
        verbose: bool = True,
        emitter: Optional[AgentEventEmitter] = None,
    ):
        """Initialize the deep research agent.

        Args:
            model_tier: Model tier (fast, standard, powerful)
            verbose: Whether to print progress
            emitter: Event emitter for unified output
        """
        self.model_tier = model_tier
        self.verbose = verbose
        self.emitter = emitter or NullEmitter(agent_name="DeepResearchAgent")
        self.console = Console()

        self.controller = ResearchController(
            model_tier=model_tier,
            verbose=verbose,
            emitter=self.emitter,
        )

        self._last_state: Optional[ResearchState] = None

    def research(
        self,
        goal: str,
        context: str = "",
        max_iterations: int = 3,
        budgets: Optional[dict] = None,
    ) -> str:
        """Conduct deep research on a topic.

        Args:
            goal: Research goal/question
            context: Additional context
            max_iterations: Maximum research iterations
            budgets: Resource budgets

        Returns:
            Final research report as markdown
        """
        report, state = self.controller.research(
            goal=goal,
            context=context,
            max_iterations=max_iterations,
            budgets=budgets,
        )

        self._last_state = state
        return report

    def get_last_state(self) -> Optional[ResearchState]:
        """Get the state from the last research run.

        Returns:
            ResearchState or None if no research has been run
        """
        return self._last_state

    def get_summary(self) -> str:
        """Get a summary of the last research run.

        Returns:
            Summary string
        """
        if not self._last_state:
            return "No research has been conducted yet."

        state = self._last_state

        lines = [
            f"Research: {state.plan.goal}",
            f"Iterations: {state.iteration}",
            f"Evidence: {len(state.get_all_evidence())}",
            f"Claims: {len(state.get_all_claims())}",
            f"Gaps: {len(state.get_all_gaps())}",
            f"Status: {'Approved' if state.is_approved() else 'In Progress'}",
            f"Budget used: {state.budget_used_percent():.0f}%",
        ]

        return "\n".join(lines)


def research(
    goal: str,
    context: str = "",
    model_tier: str = "fast",
    max_iterations: int = 3,
    verbose: bool = True,
) -> str:
    """Convenience function for quick research.

    Args:
        goal: Research goal/question
        context: Additional context
        model_tier: Model tier to use
        max_iterations: Maximum iterations
        verbose: Whether to print progress

    Returns:
        Research report as markdown

    Example:
        report = research("How does the payment system work?")
    """
    agent = DeepResearchAgent(
        model_tier=model_tier,
        verbose=verbose,
    )
    return agent.research(
        goal=goal,
        context=context,
        max_iterations=max_iterations,
    )
