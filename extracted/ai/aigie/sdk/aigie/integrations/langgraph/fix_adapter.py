"""
LangGraph fix adapter — modifies graph state via native state updates.

LangGraph uses graph topology as control flow. The native approach is:
1. Post-processing nodes that modify state
2. add_messages reducer handles message updates
3. For create_agent users, LangChain v1.0 middleware applies

This adapter works at the state dict level, modifying messages
using the same patterns LangGraph nodes use internally.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class LangGraphFixAdapter:
    """Applies fixes by modifying LangGraph state messages.

    Works with LangGraph's state dict pattern where state["messages"]
    is a list of message objects. The adapter modifies the last message
    following LangGraph's native state update conventions.
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
            # Pattern 1: Graph state dict with messages list
            if isinstance(context, dict) and "messages" in context:
                messages = context["messages"]
                if messages:
                    last_msg = messages[-1]
                    # AIMessage or BaseMessage with .content
                    if hasattr(last_msg, "content"):
                        if fixed_output:
                            last_msg.content = content
                        elif guidance:
                            last_msg.content = f"{last_msg.content}\n\n{content}"
                        return True
                    # Dict-style message
                    if isinstance(last_msg, dict) and "content" in last_msg:
                        if fixed_output:
                            last_msg["content"] = content
                        elif guidance:
                            last_msg["content"] = f"{last_msg['content']}\n\n{content}"
                        return True

            # Pattern 2: Direct AIMessage/LLMResult (from wrapper layer)
            if hasattr(context, "content") and isinstance(context.content, str):
                if fixed_output:
                    context.content = content
                elif guidance:
                    context.content = f"{context.content}\n\n{content}"
                return True
        except Exception as e:
            logger.warning(f"LangGraph fix failed: {e}")
        return False


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("langgraph", LangGraphFixAdapter())
except ImportError:
    pass
