"""
AutoGen/AG2 auto-instrumentation.

Automatically patches AutoGen classes to create traces and inject handlers.
"""

import functools
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()


def patch_autogen() -> bool:
    """Patch AutoGen classes for auto-instrumentation.

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _patch_conversable_agent() and success
    success = _patch_group_chat_manager() and success
    return _patch_user_proxy_agent() and success


def unpatch_autogen() -> None:
    """Remove AutoGen patches (for testing)."""
    global _patched_classes
    _patched_classes.clear()


def is_autogen_patched() -> bool:
    """Check if AutoGen has been patched."""
    return len(_patched_classes) > 0


def _patch_conversable_agent() -> bool:
    """Patch ConversableAgent.initiate_chat() and a_initiate_chat() methods."""
    try:
        # Try ag2 first (newer package name)
        try:
            from ag2 import ConversableAgent
        except ImportError:
            # Fall back to autogen
            from autogen import ConversableAgent

        if ConversableAgent in _patched_classes:
            return True

        original_initiate_chat = ConversableAgent.initiate_chat
        original_a_initiate_chat = getattr(ConversableAgent, "a_initiate_chat", None)

        @functools.wraps(original_initiate_chat)
        def traced_initiate_chat(
            self,
            recipient,
            clear_history: bool = True,
            silent: bool = False,
            cache=None,
            max_turns: int | None = None,
            **kwargs,
        ):
            """Traced version of ConversableAgent.initiate_chat()."""
            import asyncio

            from ...client import get_aigie
            from .handler import AutoGenHandler

            aigie = get_aigie()
            if aigie and aigie._initialized:
                handler = AutoGenHandler(
                    trace_name=f"Conversation: {self.name} -> {getattr(recipient, 'name', 'unknown')}",
                    metadata={"max_turns": max_turns},
                )
                handler._aigie = aigie

                initiator_name = getattr(self, "name", "unknown")
                recipient_name = getattr(recipient, "name", "unknown")
                initial_message = kwargs.get("message", "")

                # Run async handler in sync context
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        import concurrent.futures

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                handler.handle_conversation_start(
                                    initiator=initiator_name,
                                    recipient=recipient_name,
                                    message=str(initial_message)[:500] if initial_message else None,
                                    max_turns=max_turns,
                                    conversation_type="two_agent",
                                ),
                            )
                            future.result(timeout=5)
                    else:
                        loop.run_until_complete(
                            handler.handle_conversation_start(
                                initiator=initiator_name,
                                recipient=recipient_name,
                                message=str(initial_message)[:500] if initial_message else None,
                                max_turns=max_turns,
                                conversation_type="two_agent",
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting conversation trace: {e}")

                # Store handler on agents for access
                self._aigie_handler = handler
                if hasattr(recipient, "__dict__"):
                    recipient._aigie_handler = handler

                try:
                    result = original_initiate_chat(
                        self, recipient, clear_history, silent, cache, max_turns, **kwargs
                    )

                    # Handle completion
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_conversation_end(success=True, result=result),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_conversation_end(success=True, result=result)
                            )
                    except Exception as e:
                        logger.debug(f"Error ending conversation trace: {e}")

                    return result

                except Exception as e:
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_conversation_end(success=False, error=str(e)),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_conversation_end(success=False, error=str(e))
                            )
                    except Exception:
                        pass
                    raise

            return original_initiate_chat(
                self, recipient, clear_history, silent, cache, max_turns, **kwargs
            )

        if original_a_initiate_chat:

            @functools.wraps(original_a_initiate_chat)
            async def traced_a_initiate_chat(
                self,
                recipient,
                clear_history: bool = True,
                silent: bool = False,
                cache=None,
                max_turns: int | None = None,
                **kwargs,
            ):
                """Traced version of ConversableAgent.a_initiate_chat()."""
                from ...client import get_aigie
                from .handler import AutoGenHandler

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    handler = AutoGenHandler(
                        trace_name=f"Conversation: {self.name} -> {getattr(recipient, 'name', 'unknown')}",
                        metadata={"max_turns": max_turns},
                    )
                    handler._aigie = aigie

                    initiator_name = getattr(self, "name", "unknown")
                    recipient_name = getattr(recipient, "name", "unknown")
                    initial_message = kwargs.get("message", "")

                    await handler.handle_conversation_start(
                        initiator=initiator_name,
                        recipient=recipient_name,
                        message=str(initial_message)[:500] if initial_message else None,
                        max_turns=max_turns,
                        conversation_type="two_agent",
                    )

                    self._aigie_handler = handler
                    if hasattr(recipient, "__dict__"):
                        recipient._aigie_handler = handler

                    try:
                        result = await original_a_initiate_chat(
                            self, recipient, clear_history, silent, cache, max_turns, **kwargs
                        )
                        await handler.handle_conversation_end(success=True, result=result)
                        return result
                    except Exception as e:
                        await handler.handle_conversation_end(success=False, error=str(e))
                        raise

                return await original_a_initiate_chat(
                    self, recipient, clear_history, silent, cache, max_turns, **kwargs
                )

            ConversableAgent.a_initiate_chat = traced_a_initiate_chat

        ConversableAgent.initiate_chat = traced_initiate_chat
        _patched_classes.add(ConversableAgent)

        logger.debug("Patched ConversableAgent for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("AutoGen/AG2 not installed, skipping ConversableAgent patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch ConversableAgent: {e}")
        return False


def _patch_group_chat_manager() -> bool:
    """Patch GroupChatManager for group chat tracing."""
    try:
        # Try ag2 first
        try:
            from ag2 import GroupChatManager
        except ImportError:
            from autogen import GroupChatManager

        if GroupChatManager in _patched_classes:
            return True

        original_init = GroupChatManager.__init__

        @functools.wraps(original_init)
        def traced_init(self, groupchat, *args, **kwargs):
            """Traced version of GroupChatManager.__init__."""
            result = original_init(self, groupchat, *args, **kwargs)

            # Store groupchat info for tracing
            self._aigie_groupchat = groupchat
            if hasattr(groupchat, "agents"):
                self._aigie_agent_names = [getattr(a, "name", "unknown") for a in groupchat.agents]

            return result

        GroupChatManager.__init__ = traced_init
        _patched_classes.add(GroupChatManager)

        logger.debug("Patched GroupChatManager for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("AutoGen/AG2 GroupChatManager not found, skipping patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch GroupChatManager: {e}")
        return False


def _patch_user_proxy_agent() -> bool:
    """Patch UserProxyAgent for code execution tracing."""
    try:
        # Try ag2 first
        try:
            from ag2 import UserProxyAgent
        except ImportError:
            from autogen import UserProxyAgent

        if UserProxyAgent in _patched_classes:
            return True

        # Check if execute_code_blocks exists
        if not hasattr(UserProxyAgent, "execute_code_blocks"):
            logger.debug("UserProxyAgent.execute_code_blocks not found, skipping")
            return True

        original_execute = UserProxyAgent.execute_code_blocks

        @functools.wraps(original_execute)
        def traced_execute_code_blocks(self, code_blocks):
            """Traced version of execute_code_blocks."""
            import asyncio

            from ...client import get_aigie

            aigie = get_aigie()
            handler = getattr(self, "_aigie_handler", None)

            if aigie and aigie._initialized and handler:
                for _i, (lang, code) in enumerate(code_blocks):
                    exec_id = str(uuid.uuid4())

                    try:
                        loop = asyncio.get_event_loop()
                        if not loop.is_running():
                            loop.run_until_complete(
                                handler.handle_code_execution_start(
                                    exec_id=exec_id,
                                    language=lang,
                                    code=code[:2000],
                                    agent_name=getattr(self, "name", "unknown"),
                                )
                            )
                    except Exception as e:
                        logger.debug(f"Error starting code execution trace: {e}")

            # Execute the code
            result = original_execute(self, code_blocks)

            # Trace completion
            if aigie and aigie._initialized and handler:
                exit_code = result[0] if isinstance(result, tuple) else 0
                output = result[1] if isinstance(result, tuple) and len(result) > 1 else str(result)

                for _i, (lang, code) in enumerate(code_blocks):
                    try:
                        loop = asyncio.get_event_loop()
                        if not loop.is_running():
                            loop.run_until_complete(
                                handler.handle_code_execution_end(
                                    exec_id=exec_id,
                                    exit_code=exit_code,
                                    output=output[:1000] if output else None,
                                )
                            )
                    except Exception as e:
                        logger.debug(f"Error ending code execution trace: {e}")

            return result

        UserProxyAgent.execute_code_blocks = traced_execute_code_blocks
        _patched_classes.add(UserProxyAgent)

        logger.debug("Patched UserProxyAgent for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("AutoGen/AG2 UserProxyAgent not found, skipping patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch UserProxyAgent: {e}")
        return False
