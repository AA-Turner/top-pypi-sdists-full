"""
Instructor auto-instrumentation.

Automatically patches Instructor functions to create traces.
"""

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

_patched_functions: set[str] = set()
_original_functions: dict[str, Any] = {}


def patch_instructor() -> bool:
    """
    Patch Instructor functions for auto-instrumentation.

    This patches:
    - instructor.from_openai() - OpenAI client wrapper
    - instructor.from_anthropic() - Anthropic client wrapper
    - instructor.patch() - Generic client patch

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _patch_from_openai() and success
    success = _patch_from_anthropic() and success
    return _patch_instructor_patch() and success


def unpatch_instructor() -> None:
    """Remove Instructor patches (for testing)."""
    global _patched_functions, _original_functions

    try:
        import instructor

        if "from_openai" in _original_functions:
            instructor.from_openai = _original_functions["from_openai"]

        if "from_anthropic" in _original_functions:
            instructor.from_anthropic = _original_functions["from_anthropic"]

        if "patch" in _original_functions:
            instructor.patch = _original_functions["patch"]

    except ImportError:
        pass

    _patched_functions.clear()
    _original_functions.clear()


def is_instructor_patched() -> bool:
    """Check if Instructor has been patched."""
    return len(_patched_functions) > 0


def _wrap_client_chat_completions_create(original_create, client_type: str):
    """Wrap the create method to add tracing."""

    @functools.wraps(original_create)
    async def traced_create_async(self, *args, **kwargs):
        # Skip if already inside LLM instrumentation (prevents double-tracing
        # when OpenAI client is also auto-instrumented)
        from ...auto_instrument.trace import is_in_llm_instrumentation

        if is_in_llm_instrumentation():
            return await original_create(self, *args, **kwargs)

        from ...client import get_aigie
        from .config import InstructorConfig
        from .handler import InstructorHandler

        aigie = get_aigie()
        config = InstructorConfig.from_env()

        if aigie and aigie._initialized and config.enabled:
            handler = InstructorHandler(
                capture_schemas=config.capture_schemas,
                capture_outputs=config.capture_outputs,
            )
            handler._aigie = aigie

            # Extract relevant info
            messages = kwargs.get("messages", [])
            response_model = kwargs.get("response_model")
            model = kwargs.get("model", "unknown")

            await handler.handle_call_start(messages, response_model, model, **kwargs)

            try:
                result = await original_create(self, *args, **kwargs)

                # Extract usage from response
                usage = None
                if hasattr(result, "_raw_response"):
                    raw = result._raw_response
                    if hasattr(raw, "usage"):
                        usage = {
                            "prompt_tokens": getattr(raw.usage, "prompt_tokens", 0),
                            "completion_tokens": getattr(raw.usage, "completion_tokens", 0),
                        }

                await handler.handle_call_end(result, usage)
                return result

            except Exception as e:
                await handler.handle_call_end(None, error=str(e))
                raise
        else:
            return await original_create(self, *args, **kwargs)

    @functools.wraps(original_create)
    def traced_create_sync(self, *args, **kwargs):
        # For sync calls, we can't use async handlers easily
        # Just pass through for now
        return original_create(self, *args, **kwargs)

    # Return appropriate wrapper based on whether original is async
    import asyncio

    if asyncio.iscoroutinefunction(original_create):
        return traced_create_async
    return traced_create_sync


def _patch_from_openai() -> bool:
    """Patch instructor.from_openai()."""
    try:
        import instructor

        if "from_openai" in _patched_functions:
            return True

        if not hasattr(instructor, "from_openai"):
            logger.debug("instructor.from_openai not found")
            return True

        original_from_openai = instructor.from_openai
        _original_functions["from_openai"] = original_from_openai

        @functools.wraps(original_from_openai)
        def traced_from_openai(client, *args, **kwargs):
            """Traced version of instructor.from_openai()."""
            # Get the patched client from instructor
            patched_client = original_from_openai(client, *args, **kwargs)

            # Store original create method
            if hasattr(patched_client, "chat") and hasattr(patched_client.chat, "completions"):
                original_create = patched_client.chat.completions.create

                # Wrap create method
                patched_client.chat.completions.create = _wrap_client_chat_completions_create(
                    original_create, "openai"
                ).__get__(patched_client.chat.completions)

            return patched_client

        instructor.from_openai = traced_from_openai
        _patched_functions.add("from_openai")

        logger.debug("Patched instructor.from_openai for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("instructor not installed, skipping from_openai patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch instructor.from_openai: {e}")
        return False


def _patch_from_anthropic() -> bool:
    """Patch instructor.from_anthropic()."""
    try:
        import instructor

        if "from_anthropic" in _patched_functions:
            return True

        if not hasattr(instructor, "from_anthropic"):
            logger.debug("instructor.from_anthropic not found")
            return True

        original_from_anthropic = instructor.from_anthropic
        _original_functions["from_anthropic"] = original_from_anthropic

        @functools.wraps(original_from_anthropic)
        def traced_from_anthropic(client, *args, **kwargs):
            """Traced version of instructor.from_anthropic()."""
            patched_client = original_from_anthropic(client, *args, **kwargs)

            # Wrap create method if available
            if hasattr(patched_client, "messages") and hasattr(patched_client.messages, "create"):
                original_create = patched_client.messages.create

                patched_client.messages.create = _wrap_client_chat_completions_create(
                    original_create, "anthropic"
                ).__get__(patched_client.messages)

            return patched_client

        instructor.from_anthropic = traced_from_anthropic
        _patched_functions.add("from_anthropic")

        logger.debug("Patched instructor.from_anthropic for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("instructor not installed, skipping from_anthropic patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch instructor.from_anthropic: {e}")
        return False


def _patch_instructor_patch() -> bool:
    """Patch instructor.patch() function."""
    try:
        import instructor

        if "patch" in _patched_functions:
            return True

        if not hasattr(instructor, "patch"):
            logger.debug("instructor.patch not found")
            return True

        original_patch = instructor.patch
        _original_functions["patch"] = original_patch

        @functools.wraps(original_patch)
        def traced_patch(client, *args, **kwargs):
            """Traced version of instructor.patch()."""
            patched_client = original_patch(client, *args, **kwargs)

            # Try to wrap the create method
            if hasattr(patched_client, "chat") and hasattr(patched_client.chat, "completions"):
                original_create = patched_client.chat.completions.create

                patched_client.chat.completions.create = _wrap_client_chat_completions_create(
                    original_create, "patched"
                ).__get__(patched_client.chat.completions)

            return patched_client

        instructor.patch = traced_patch
        _patched_functions.add("patch")

        logger.debug("Patched instructor.patch for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("instructor not installed, skipping patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch instructor.patch: {e}")
        return False
