"""
Agno fix adapter — uses native hook output mutation.

Agno's hook system supports:
- post_hooks: receive RunOutput with mutable .content field
- tool_hooks: wrap tool execution, can modify return value
- pre_hooks: receive RunInput with mutable .input_content
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class AgnoFixAdapter:
    """Applies fixes using Agno's native hook output mutation.

    For agent responses: mutates RunOutput.content in post_hook.
    For tool results: wraps tool_hook to modify return value.
    For input injection: mutates RunInput.input_content in pre_hook.
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
            # Pattern 1: RunOutput (from post_hook)
            # Has .content (mutable str/list)
            if hasattr(context, "content") and not hasattr(context, "input_content"):
                if fixed_output:
                    context.content = content
                    return True
                if guidance:
                    existing = context.content or ""
                    context.content = f"{existing}\n\n[Aigie: {guidance}]"
                    return True

            # Pattern 2: RunInput (from pre_hook)
            # Has .input_content (mutable)
            if hasattr(context, "input_content"):
                existing = context.input_content or ""
                context.input_content = f"{existing}\n\n[Aigie correction] {content}"
                return True

            # Pattern 3: Tool result dict
            if isinstance(context, dict):
                if "result" in context:
                    context["result"] = content
                else:
                    context["aigie_correction"] = content
                return True

            # Pattern 4: Tool result string — cannot mutate
            if isinstance(context, str):
                return False

        except Exception as e:
            logger.warning(f"Agno fix failed: {e}")
        return False


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("agno", AgnoFixAdapter())
except ImportError:
    pass
