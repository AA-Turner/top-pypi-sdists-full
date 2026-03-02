"""Agent factory for creating different agent types.

This module provides the AgentFactory class for instantiating agents
with appropriate configuration based on use case.
"""

from pathlib import Path
from typing import Optional

from .base import BaseAgent
from .coding import CodingMainAgent
from .coworker import CoworkerAgent
from .open import OpenAgent
from .events import AgentEventEmitter
from .providers.factory import DEFAULT_MODEL


class AgentFactory:
    """Factory for creating agents with appropriate configuration.

    Provides static methods to create different agent types:
    - Coding agents: Full-featured coding assistants
    - Coworker agents: General-purpose assistants without coding

    Example:
        # Create a coding agent
        agent = AgentFactory.create_coding_agent(
            repo_root=Path.cwd(),
        )

        # Create a coworker agent
        agent = AgentFactory.create_coworker_agent(
            personality="creative_collaborator",
            domain_context="You are helping a marketing team.",
        )
    """

    @staticmethod
    def create_coding_agent(
        model: str = DEFAULT_MODEL,
        repo_root: Optional[Path] = None,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = 100,
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        session_id: Optional[str] = None,
        plan_mode: bool = False,
        **kwargs,
    ) -> CodingMainAgent:
        """Create a coding-focused main agent.

        Args:
            model: LLM model to use.
            repo_root: Repository root path. Defaults to cwd.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            enable_thinking: Enable extended thinking.
            session_id: Session ID for plan file isolation.
            plan_mode: Start in plan mode.
            **kwargs: Additional arguments passed to CodingMainAgent.

        Returns:
            Configured CodingMainAgent instance.
        """
        return CodingMainAgent(
            model=model,
            repo_root=repo_root or Path.cwd(),
            emitter=emitter,
            max_iterations=max_iterations,
            verbose=verbose,
            enable_thinking=enable_thinking,
            session_id=session_id,
            plan_mode=plan_mode,
            **kwargs,
        )

    @staticmethod
    def create_coworker_agent(
        model: str = DEFAULT_MODEL,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = 50,
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        session_id: Optional[str] = None,
        personality: str = "helpful_professional",
        domain_context: Optional[str] = None,
        **kwargs,
    ) -> CoworkerAgent:
        """Create a general-purpose coworker agent.

        Args:
            model: LLM model to use.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            enable_thinking: Enable extended thinking.
            session_id: Session ID for isolation.
            personality: Personality style. Options:
                - "helpful_professional": Clear, practical, organized
                - "creative_collaborator": Enthusiastic, creative, ideation-focused
                - "analytical_researcher": Thorough, accurate, evidence-based
                - "friendly_coach": Supportive, encouraging, actionable
                - Or provide a custom personality prompt string.
            domain_context: Optional domain-specific context.
            **kwargs: Additional arguments passed to CoworkerAgent.

        Returns:
            Configured CoworkerAgent instance.
        """
        return CoworkerAgent(
            model=model,
            emitter=emitter,
            max_iterations=max_iterations,
            verbose=verbose,
            enable_thinking=enable_thinking,
            session_id=session_id,
            personality=personality,
            domain_context=domain_context,
            **kwargs,
        )

    @staticmethod
    def create_open_agent(
        model: str = DEFAULT_MODEL,
        repo_root: Optional[Path] = None,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = 100,
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        session_id: Optional[str] = None,
        **kwargs,
    ) -> OpenAgent:
        """Create a self-evolving open personal assistant agent.

        Args:
            model: LLM model to use.
            repo_root: Repository root path. Defaults to cwd.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            enable_thinking: Enable extended thinking.
            session_id: Session ID for isolation.
            **kwargs: Additional arguments passed to OpenAgent.

        Returns:
            Configured OpenAgent instance.
        """
        return OpenAgent(
            model=model,
            repo_root=repo_root or Path.cwd(),
            emitter=emitter,
            max_iterations=max_iterations,
            verbose=verbose,
            enable_thinking=enable_thinking,
            session_id=session_id,
            **kwargs,
        )

    @staticmethod
    def create_agent(
        agent_type: str = "coding",
        **kwargs,
    ) -> BaseAgent:
        """Create an agent by type name.

        Args:
            agent_type: Type of agent ("coding", "coworker", or "open").
            **kwargs: Arguments passed to the specific agent factory method.

        Returns:
            Configured agent instance.

        Raises:
            ValueError: If agent_type is not recognized.
        """
        if agent_type == "coding":
            return AgentFactory.create_coding_agent(**kwargs)
        elif agent_type == "coworker":
            return AgentFactory.create_coworker_agent(**kwargs)
        elif agent_type == "open":
            return AgentFactory.create_open_agent(**kwargs)
        else:
            raise ValueError(
                f"Unknown agent type: {agent_type}. "
                f"Available types: coding, coworker, open"
            )


# Convenience aliases
def create_coding_agent(**kwargs) -> CodingMainAgent:
    """Convenience function to create a coding agent."""
    return AgentFactory.create_coding_agent(**kwargs)


def create_coworker_agent(**kwargs) -> CoworkerAgent:
    """Convenience function to create a coworker agent."""
    return AgentFactory.create_coworker_agent(**kwargs)


def create_open_agent(**kwargs) -> OpenAgent:
    """Convenience function to create an open personal assistant agent."""
    return AgentFactory.create_open_agent(**kwargs)
