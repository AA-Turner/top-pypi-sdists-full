"""
OpenAI Agents SDK fix adapter — uses message injection for corrections.

The OpenAI Agents SDK does not support direct response replacement.
Fixes are applied by injecting corrective messages into the agent's
input items for the next turn, or by modifying tool results.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OpenAIAgentsFixAdapter:
    """Applies fixes using OpenAI Agents SDK's message/tool mechanisms.

    For tool results: directly modifies the tool output string.
    For model responses: injects a system-level correction message
    into the input items for the next model call.
    """

    def apply_fix(self, fix_payload: dict[str, Any], context: Any) -> bool:
        fixed_output = fix_payload.get("fixed_output")
        guidance = fix_payload.get("guidance")

        if not context:
            return False

        correction = guidance or (
            f"Previous output needs correction: {fixed_output}" if fixed_output else None
        )
        if not correction:
            return False

        try:
            # Pattern 1: Tool result string — replace directly
            if isinstance(context, str):
                # Cannot mutate strings; caller must use return value
                return False

            # Pattern 2: RunHooks context — inject into input_items
            # on_llm_start receives (context, agent, system_prompt, input_items)
            # input_items is a mutable list we can append to
            if isinstance(context, list):
                context.append(
                    {
                        "role": "developer",
                        "content": f"[Aigie correction] {correction}",
                    }
                )
                return True

            # Pattern 3: Dict context (generic) — add correction key
            if isinstance(context, dict):
                context["aigie_correction"] = correction
                return True

            # Pattern 4: RunResult — cannot modify after completion
            if hasattr(context, "final_output"):
                # RunResult is immutable after run completes
                return False

        except Exception as e:
            logger.warning(f"OpenAI Agents fix failed: {e}")
        return False


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("openai_agents", OpenAIAgentsFixAdapter())
except ImportError:
    pass
