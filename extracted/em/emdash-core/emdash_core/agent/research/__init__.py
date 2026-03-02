"""Deep Research Agent module.

This module provides a multi-agent research system for deep code exploration.

Components:
- PlannerAgent: Creates research plans with prioritized questions
- ResearcherAgent: Executes tool macros and collects evidence
- CriticAgent: Evaluates research quality and team value adherence
- SynthesizerAgent: Generates final reports
- ResearchController: Orchestrates the research loop
- DeepResearchAgent: Main entry point

Team Values Enforced:
- V1: Truth over fluency - prefer "unknown" over guesses
- V2: Evidence-first - all claims must be backed by tool outputs
- V3: Reviewer-first - output includes review checklists
- V4: Cost awareness - minimize tool calls, use budget limits
- V5: Actionable outcomes - end with concrete tasks
- V6: Team alignment - use team vocabulary
"""

from .state import (
    EvidenceItem,
    Claim,
    Gap,
    ResearchQuestion,
    ResearchPlan,
    FollowUpQuestion,
    Contradiction,
    ValuesViolation,
    CritiqueScores,
    Critique,
    IterationResult,
    ResearchState,
)
from .planner import PlannerAgent
from .researcher import ResearcherAgent
from .critic import CriticAgent
from .synthesizer import SynthesizerAgent
from .controller import ResearchController
from .agent import DeepResearchAgent, research
from .macros import (
    ToolMacro,
    MacroStep,
    MacroExecutor,
    get_macro,
    list_macros,
    suggest_macros,
)

__all__ = [
    # State
    "EvidenceItem",
    "Claim",
    "Gap",
    "ResearchQuestion",
    "ResearchPlan",
    "FollowUpQuestion",
    "Contradiction",
    "ValuesViolation",
    "CritiqueScores",
    "Critique",
    "IterationResult",
    "ResearchState",
    # Agents
    "PlannerAgent",
    "ResearcherAgent",
    "CriticAgent",
    "SynthesizerAgent",
    "ResearchController",
    "DeepResearchAgent",
    # Convenience
    "research",
    # Macros
    "ToolMacro",
    "MacroStep",
    "MacroExecutor",
    "get_macro",
    "list_macros",
    "suggest_macros",
]
