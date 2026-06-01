"""
CrewAI fix adapter — uses native hooks for response modification.

CrewAI's hooks system supports:
- after_llm_call: return modified response string to REPLACE
- before_llm_call: modify messages list (mutable) to inject context
- after_tool_call: return modified result string to REPLACE
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CrewAIFixAdapter:
    """Applies fixes using CrewAI's native hook response modification.

    For LLM responses: returns modified string from after_llm_call hook.
    For tool results: returns modified string from after_tool_call hook.
    For pre-LLM injection: mutates messages list in before_llm_call hook.
    """

    def apply_fix(self, fix_payload: dict[str, Any], context: Any) -> bool:
        fixed_output = fix_payload.get("fixed_output")
        guidance = fix_payload.get("guidance")

        if not context:
            return False

        content = fixed_output or (f"[Aigie: {guidance}]" if guidance else None)
        if not content:
            return False

        try:
            # Pattern 1: LLMCallHookContext (from after_llm_call)
            # Has .response (str), .messages (list), .agent, .task
            if hasattr(context, "response") and hasattr(context, "messages"):
                if fixed_output:
                    # Replace the LLM response — hook return value replaces
                    context._aigie_replacement = content
                    return True
                if guidance:
                    # Inject guidance into messages for next iteration
                    context.messages.append(
                        {
                            "role": "system",
                            "content": f"[Aigie correction] {guidance}",
                        }
                    )
                    return True

            # Pattern 2: ToolCallHookContext (from after_tool_call)
            # Has .tool_result (str), .tool_name, .tool_input
            if hasattr(context, "tool_result") and hasattr(context, "tool_name"):
                context._aigie_replacement = content
                return True

            # Pattern 3: Messages list (from before_llm_call)
            if isinstance(context, list):
                context.append(
                    {
                        "role": "system",
                        "content": f"[Aigie correction] {content}",
                    }
                )
                return True

            # Pattern 4: Dict context (generic)
            if isinstance(context, dict):
                context["aigie_correction"] = content
                return True

        except Exception as e:
            logger.warning(f"CrewAI fix failed: {e}")
        return False


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("crewai", CrewAIFixAdapter())
except ImportError:
    pass
