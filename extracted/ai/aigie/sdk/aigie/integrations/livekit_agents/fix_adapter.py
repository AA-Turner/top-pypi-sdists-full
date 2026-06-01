"""
LiveKit Agents fix adapter — uses ChatContext mutation and generate_reply.

LiveKit Agents supports fix injection via:
- Mutating session.chat_ctx (ChatContext) to inject correction messages
- Using session.generate_reply(instructions=...) for forced corrections
"""

import logging
import weakref
from typing import Any

logger = logging.getLogger(__name__)

_pending_corrections: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


class LiveKitAgentsFixAdapter:
    """Applies fixes using LiveKit Agents' native APIs.

    For ChatContext: appends a correction message via context.append().
    For dict context: injects an aigie_correction key.
    For AgentSession: stores a pending correction for generate_reply.
    """

    def apply_fix(self, fix_payload: dict[str, Any], context: Any) -> bool:
        """Apply a fix to the given LiveKit Agents context.

        Args:
            fix_payload: Fix payload containing 'fixed_output' and/or 'guidance'.
            context: The LiveKit Agents context object (ChatContext, dict, or AgentSession).

        Returns:
            True if the fix was applied successfully, False otherwise.
        """
        fixed_output = fix_payload.get("fixed_output")
        guidance = fix_payload.get("guidance")
        content = fixed_output or guidance

        if not context or not content:
            return False

        try:
            # Pattern 1: ChatContext — append correction message
            # ChatContext has .items list and .append() method
            if hasattr(context, "items") and hasattr(context, "append"):
                from livekit.agents.llm import ChatMessage, ChatRole

                correction_msg = ChatMessage(
                    role=ChatRole.SYSTEM,
                    content=f"[Aigie correction]: {content}",
                )
                context.append(message=correction_msg)
                logger.debug("[AIGIE] Applied fix via ChatContext.append()")
                return True
        except ImportError:
            # Fallback if ChatMessage/ChatRole aren't available at expected path
            if hasattr(context, "items") and hasattr(context, "append"):
                try:
                    context.append(
                        role="system",
                        text=f"[Aigie correction]: {content}",
                    )
                    logger.debug("[AIGIE] Applied fix via ChatContext.append() (fallback)")
                    return True
                except Exception as e:
                    logger.warning(f"[AIGIE] ChatContext fallback append failed: {e}")
        except Exception as e:
            logger.warning(f"[AIGIE] ChatContext fix failed: {e}")

        try:
            # Pattern 2: Dict context
            if isinstance(context, dict):
                context["aigie_correction"] = content
                logger.debug("[AIGIE] Applied fix via dict injection")
                return True

            # Pattern 3: AgentSession — store pending correction for generate_reply
            # Cannot call async generate_reply from sync — store for later retrieval
            if hasattr(context, "generate_reply"):
                _pending_corrections[context] = content
                logger.debug("[AIGIE] Stored pending correction on AgentSession")
                return True
        except Exception as e:
            logger.warning(f"[AIGIE] LiveKit Agents fix failed: {e}")

        return False


try:
    from ...realtime.fix_applicator import register_fix_adapter

    register_fix_adapter("livekit_agents", LiveKitAgentsFixAdapter())
except ImportError:
    pass
