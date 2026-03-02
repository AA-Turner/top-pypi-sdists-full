"""System prompts for sub-agent types.

DEPRECATED: This module is deprecated. Import from .prompts instead.

This file re-exports from .prompts.subagents for backwards compatibility.
"""

from .prompts.subagents import SUBAGENT_PROMPTS, get_subagent_prompt

# Backwards compatibility alias
get_system_prompt = get_subagent_prompt

__all__ = ["SUBAGENT_PROMPTS", "get_system_prompt", "get_subagent_prompt"]
