"""
Google ADK fix adapter — uses native return-value replacement callbacks.

Google ADK's callback system is the most straightforward for modification:
- after_model_callback returns Optional[LlmResponse] — return to REPLACE
- after_tool_callback returns Optional[dict] — return to REPLACE
- Return None to keep original

This adapter provides both:
1. apply_fix() for use from the SDK wrapper layer
2. create_after_model_callback() for native ADK integration
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class GoogleADKFixAdapter:
    """Applies fixes using Google ADK's native return-value replacement.

    ADK callbacks support full replacement: return a new object to replace
    the original, or None to keep it. This is the cleanest modification API.
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
            # Pattern 1: LlmResponse (from after_model_callback)
            # LlmResponse has .content.parts[].text
            if hasattr(context, "content") and hasattr(context.content, "parts"):
                for part in context.content.parts:
                    if hasattr(part, "text"):
                        if fixed_output:
                            part.text = content
                        elif guidance:
                            part.text = f"{part.text}\n\n{content}"
                        return True

            # Pattern 2: Dict (from after_tool_callback)
            if isinstance(context, dict):
                if "result" in context:
                    context["result"] = content
                elif "text" in context:
                    context["text"] = content
                else:
                    context["aigie_fix"] = content
                return True

            # Pattern 3: GenerateContentResponse (legacy)
            if hasattr(context, "candidates"):
                for candidate in context.candidates:
                    cand_content = getattr(candidate, "content", None)
                    if cand_content and hasattr(cand_content, "parts"):
                        for part in cand_content.parts:
                            if hasattr(part, "text"):
                                part.text = content
                                return True
        except Exception as e:
            logger.warning(f"Google ADK fix failed: {e}")
        return False

    @staticmethod
    def create_after_model_callback(fix_fn):
        """Create an after_model_callback for native ADK integration.

        Usage:
            def my_fix(llm_response):
                # Return modified LlmResponse or None
                return modified_response

            agent = LlmAgent(
                after_model_callback=GoogleADKFixAdapter.create_after_model_callback(my_fix)
            )
        """

        def callback(callback_context, llm_response):
            return fix_fn(llm_response)

        return callback


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("google_adk", GoogleADKFixAdapter())
except ImportError:
    pass
