"""
LangChain fix adapter — provides utilities for response modification.

LangChain callbacks (BaseCallbackHandler) are READ-ONLY and cannot modify
responses. This adapter provides two integration patterns:

1. RunnableLambda post-processor (works with all LangChain versions)
2. Documentation for v1.0 wrap_model_call middleware

The apply_fix method works at the LLMResult level when called from
the SDK's wrapper layer (which intercepts before LangChain callbacks fire).
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class LangChainFixAdapter:
    """Applies fixes to LangChain LLMResult objects.

    Called from the SDK wrapper layer which intercepts LLM responses
    BEFORE they reach LangChain callbacks. This is the correct
    interception point since callbacks are read-only.

    For v1.0+ users, wrap_model_call middleware is the native approach:
        @wrap_model_call
        def aigie_fix(request, handler):
            response = handler(request)
            # modify response here
            return response
    """

    def apply_fix(self, fix_payload: dict[str, Any], context: Any) -> bool:
        fixed_output = fix_payload.get("fixed_output")
        guidance = fix_payload.get("guidance")

        if not context:
            return False

        try:
            # LLMResult.generations: list[list[Generation]]
            # Each Generation has a mutable .text attribute
            if hasattr(context, "generations") and context.generations:
                for gen_list in context.generations:
                    for gen in gen_list:
                        if hasattr(gen, "text"):
                            if fixed_output:
                                gen.text = fixed_output
                            elif guidance:
                                gen.text = f"{gen.text}\n\n[Aigie: {guidance}]"
                            return True

            # AIMessage (used in chat models) has mutable .content
            if hasattr(context, "content") and isinstance(context.content, str):
                if fixed_output:
                    context.content = fixed_output
                elif guidance:
                    context.content = f"{context.content}\n\n[Aigie: {guidance}]"
                return True
        except Exception as e:
            logger.warning(f"LangChain fix failed: {e}")
        return False

    @staticmethod
    def create_post_processor(fix_fn):
        """Create a RunnableLambda post-processor for LangChain chains.

        Usage:
            from langchain_core.runnables import RunnableLambda

            def my_fix(output):
                # Apply Aigie fix logic
                return modified_output

            chain = prompt | llm | LangChainFixAdapter.create_post_processor(my_fix)
        """
        from langchain_core.runnables import RunnableLambda

        return RunnableLambda(fix_fn)


try:
    from aigie.realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("langchain", LangChainFixAdapter())
except ImportError:
    pass
