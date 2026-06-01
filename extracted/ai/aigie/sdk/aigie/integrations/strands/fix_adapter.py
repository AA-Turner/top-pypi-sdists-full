"""
Strands fix adapter — uses native hook event system.

Strands AfterToolCallEvent.result is writable (supported API).
AfterModelCallEvent supports retry_model=True to discard and retry.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class StrandsFixAdapter:
    """Applies fixes using Strands' native event mutation API.

    For tool results: directly mutates event.result (writable field).
    For model responses: sets event.retry_model = True to force re-invocation,
    or injects guidance into the next tool result.
    """

    def apply_fix(self, fix_payload: dict[str, Any], context: Any) -> bool:
        fixed_output = fix_payload.get("fixed_output")
        guidance = fix_payload.get("guidance")

        if not context:
            return False

        try:
            # AfterToolCallEvent — mutate result directly (native API)
            if hasattr(context, "result") and isinstance(context.result, dict):
                content = context.result.get("content", [])
                if fixed_output:
                    # Replace tool result content
                    context.result = {
                        "role": context.result.get("role", "tool"),
                        "content": [{"text": fixed_output}],
                    }
                    return True
                if guidance:
                    # Append guidance to existing content
                    if isinstance(content, list):
                        content.append({"text": f"\n[Aigie: {guidance}]"})
                    return True

            # AfterModelCallEvent — request retry (native API)
            if hasattr(context, "retry_model") and (fixed_output or guidance):
                context.retry_model = True
                return True
        except Exception as e:
            logger.warning(f"Strands fix failed: {e}")
        return False


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("strands", StrandsFixAdapter())
except ImportError:
    pass
