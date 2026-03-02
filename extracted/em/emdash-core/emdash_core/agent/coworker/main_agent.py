"""Coworker main agent implementation.

This module provides the CoworkerAgent - a general-purpose assistant
that inherits from BaseAgent WITHOUT coding capabilities.

Focused on:
- Research and information gathering
- Planning and organization
- Brainstorming and ideation
- Collaboration and clarification
"""

from typing import Optional, TYPE_CHECKING

from ..base import BaseAgent
from ..events import AgentEventEmitter
from ..providers.factory import DEFAULT_MODEL
from .toolkit import CoworkerToolkit

if TYPE_CHECKING:
    from ..toolkits.base import BaseToolkit


# Personality templates for different coworker styles
PERSONALITY_PROMPTS = {
    "helpful_professional": """You are a helpful, professional assistant.
- Be clear and concise
- Focus on practical solutions
- Ask clarifying questions when needed
- Organize information logically""",

    "creative_collaborator": """You are a creative, enthusiastic collaborator.
- Think outside the box
- Offer multiple perspectives
- Encourage brainstorming
- Build on ideas constructively""",

    "analytical_researcher": """You are a thorough, analytical researcher.
- Prioritize accuracy and verification
- Cite sources when possible
- Consider multiple viewpoints
- Identify gaps in information""",

    "friendly_coach": """You are a supportive, friendly coach.
- Be encouraging and positive
- Break down complex topics
- Celebrate progress
- Offer actionable advice""",
}


COWORKER_BASE_PROMPT = """You are a helpful AI assistant focused on research, planning, and collaboration.

## Your Capabilities
- Search the web for information
- Save and recall notes during our conversation
- Help plan and organize projects
- Brainstorm ideas and solutions
- Summarize information
- Track tasks and todos
- Execute shell commands (git, npm, etc.)
- Use skills from .emdash/skills/ if available

## Git Access
You have GitHub credentials configured. You CAN clone, push, and pull from GitHub repositories
including private repositories that the user has access to. When asked to clone a repo, just try it -
the credentials will authenticate automatically.

## Your Limitations
- You CANNOT modify files directly (use the coding agent for that)
- You focus on research, planning, and collaboration

## Communication Style
- Be concise and direct
- Use markdown formatting for clarity
- Ask clarifying questions when needed
- Organize your responses logically

{personality}

{domain_context}

{rules_section}

## Available Tools
{tools_section}

## Available Sub-Agents
{subagents_section}

{skills_section}

Use your tools effectively to help the user with their request.
"""


class CoworkerAgent(BaseAgent):
    """General-purpose coworker agent without coding capabilities.

    Focuses on:
    - Web research and information gathering
    - Note-taking and memory
    - Task planning and organization
    - Brainstorming and ideation
    - Collaboration and clarification

    Example:
        agent = CoworkerAgent(
            personality="creative_collaborator",
            domain_context="You are helping a marketing team.",
        )
        response = agent.run("Research our competitors' recent campaigns")
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = 50,
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        session_id: Optional[str] = None,
        personality: str = "helpful_professional",
        domain_context: Optional[str] = None,
    ):
        """Initialize the coworker agent.

        Args:
            model: LLM model to use.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            enable_thinking: Enable extended thinking.
            session_id: Session ID for isolation.
            personality: Personality style (helpful_professional, creative_collaborator,
                        analytical_researcher, friendly_coach, or custom prompt).
            domain_context: Optional domain-specific context to inject into prompt.
        """
        self._personality = personality
        self._domain_context = domain_context

        super().__init__(
            model=model,
            emitter=emitter,
            max_iterations=max_iterations,
            verbose=verbose,
            enable_thinking=enable_thinking,
            session_id=session_id,
        )

    def _get_toolkit(self) -> "BaseToolkit":
        """Return the CoworkerToolkit."""
        return CoworkerToolkit()

    def _build_system_prompt(self) -> str:
        """Build the coworker-focused system prompt.

        Includes:
        - Personality prompt
        - Domain context (if provided)
        - Rules from .emdash/rules/ (shared with coding agent)
        - Tools list
        - Sub-agents list
        - Skills list (if any loaded)
        """
        # Get personality prompt
        if self._personality in PERSONALITY_PROMPTS:
            personality_text = PERSONALITY_PROMPTS[self._personality]
        else:
            # Treat as custom personality prompt
            personality_text = self._personality

        # Build domain context
        domain_text = ""
        if self._domain_context:
            domain_text = f"## Domain Context\n{self._domain_context}"

        # Build rules section (shared with coding agent via BaseToolkit)
        rules_text = ""
        rules_content = self.toolkit.load_rules()
        if rules_content:
            rules_text = f"## Project Rules\n{rules_content}"

        # Build tools section
        tools_lines = []
        for tool in self.toolkit._tools.values():
            tools_lines.append(f"- **{tool.name}**: {tool.description}")
        tools_section = "\n".join(tools_lines)

        # Build sub-agents section
        subagents = self._get_available_subagents()
        subagents_lines = []
        for name, desc in subagents.items():
            subagents_lines.append(f"- **{name}**: {desc}")
        subagents_section = "\n".join(subagents_lines) or "None available"

        # Build skills section (if skills are loaded)
        skills_text = ""
        from ..skills import SkillRegistry
        registry = SkillRegistry.get_instance()
        all_skills = registry.get_all_skills()
        if all_skills:
            skills_lines = ["## Available Skills", "Use the `skill` tool to load detailed instructions for these tasks:"]
            for name, skill in all_skills.items():
                description = skill.description if skill.description else "No description"
                skills_lines.append(f"- **{name}**: {description}")
            skills_text = "\n".join(skills_lines)

        return COWORKER_BASE_PROMPT.format(
            personality=personality_text,
            domain_context=domain_text,
            rules_section=rules_text,
            tools_section=tools_section,
            subagents_section=subagents_section,
            skills_section=skills_text,
        )

    def _get_available_subagents(self) -> dict[str, str]:
        """Return available coworker sub-agents.

        These sub-agents are registered in TOOLKIT_REGISTRY and have
        corresponding prompts in SUBAGENT_PROMPTS.
        """
        return {
            "Researcher": "Web research specialist - searches web, fetches URLs, organizes findings with notes",
            "GeneralPlanner": "Project planning - breaks down goals, creates tasks, organizes work (NOT code)",
        }

    @property
    def name(self) -> str:
        """Return the display name for this agent."""
        return "Emdash Coworker"

    @property
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        return "coworker"

    # -------------------------------------------------------------------------
    # Coworker-specific methods
    # -------------------------------------------------------------------------

    def get_notes(self) -> list[dict]:
        """Get all notes saved during this session.

        Returns:
            List of note dictionaries
        """
        if isinstance(self.toolkit, CoworkerToolkit):
            return self.toolkit.get_notes()
        return []

    def get_todos(self) -> list[dict]:
        """Get all todos from this session.

        Returns:
            List of todo dictionaries
        """
        if isinstance(self.toolkit, CoworkerToolkit):
            return self.toolkit.get_todos()
        return []

    def summarize_session(self) -> str:
        """Get a summary of the current session.

        Returns:
            String summarizing notes, todos, and conversation topics
        """
        notes = self.get_notes()
        todos = self.get_todos()

        summary_parts = [f"## Session Summary"]

        if notes:
            summary_parts.append(f"\n### Notes ({len(notes)})")
            for note in notes:
                summary_parts.append(f"- **{note['title']}**: {note['content'][:100]}...")

        if todos:
            pending = [t for t in todos if t['status'] == 'pending']
            in_progress = [t for t in todos if t['status'] == 'in_progress']
            completed = [t for t in todos if t['status'] == 'completed']

            summary_parts.append(f"\n### Todos ({len(todos)})")
            if completed:
                summary_parts.append(f"  Completed: {len(completed)}")
            if in_progress:
                summary_parts.append(f"  In Progress: {len(in_progress)}")
            if pending:
                summary_parts.append(f"  Pending: {len(pending)}")

        if not notes and not todos:
            summary_parts.append("\nNo notes or todos in this session yet.")

        return "\n".join(summary_parts)

    @property
    def personality(self) -> str:
        """Get the current personality setting."""
        return self._personality

    @property
    def domain_context(self) -> Optional[str]:
        """Get the domain context."""
        return self._domain_context
