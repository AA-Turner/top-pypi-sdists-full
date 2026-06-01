"""
Browser-Use auto-instrumentation.

Automatically patches browser-use classes to inject Aigie tracing.
Similar to langchain auto-instrumentation in aigie/auto_instrument/langchain.py
"""

import functools
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()


def patch_browser_use() -> bool:
    """
    Patch browser-use classes for auto-instrumentation.

    This should be called after aigie.initialize() to enable
    automatic tracing of all browser-use operations.

    Returns:
        True if patching was successful, False otherwise
    """
    success = True
    success = _patch_agent() and success
    success = _patch_llm_base() and success
    return _patch_browser() and success


def _patch_agent() -> bool:
    """Patch browser-use Agent class to auto-inject tracing."""
    try:
        from browser_use import Agent

        if Agent in _patched_classes:
            return True

        original_run = Agent.run
        original_step = Agent.step

        @functools.wraps(original_run)
        async def traced_run(self, *args, **kwargs) -> Any:
            """Traced version of Agent.run."""
            from ...client import get_aigie
            from .handler import BrowserUseHandler

            aigie = get_aigie()
            if aigie and aigie._initialized:
                # Extract task from agent
                task = getattr(self, "task", "Unknown task")
                max_steps = getattr(self, "max_steps", 100)

                # Get LLM info
                llm_info = None
                if hasattr(self, "llm"):
                    llm = self.llm
                    llm_info = {
                        "class": type(llm).__name__,
                        "model": getattr(llm, "model", getattr(llm, "model_name", "unknown")),
                    }

                # Create handler
                handler = BrowserUseHandler(
                    trace_name=f"Browser Task: {task[:50]}..."
                    if len(task) > 50
                    else f"Browser Task: {task}",
                    metadata={
                        "task": task,
                        "max_steps": max_steps,
                        "agent_class": type(self).__name__,
                    },
                )

                # Store handler on agent for step tracking
                self._aigie_handler = handler

                # Start task tracing
                await handler.handle_task_start(
                    task=task,
                    max_steps=max_steps,
                    llm_info=llm_info,
                )

                try:
                    result = await original_run(self, *args, **kwargs)

                    # End task tracing
                    await handler.handle_task_end(
                        success=True,
                        result=result,
                    )

                    return result

                except Exception as e:
                    await handler.handle_task_end(
                        success=False,
                        error=str(e),
                    )
                    raise

            return await original_run(self, *args, **kwargs)

        @functools.wraps(original_step)
        async def traced_step(self, *args, **kwargs) -> Any:
            """Traced version of Agent.step."""
            from ...client import get_aigie

            aigie = get_aigie()
            handler = getattr(self, "_aigie_handler", None)

            if aigie and aigie._initialized and handler:
                # Get step number
                step_number = getattr(self, "_step_count", 0) + 1
                self._step_count = step_number

                # Get browser state if available
                browser_state = None
                if hasattr(self, "browser") and self.browser:
                    try:
                        browser = self.browser
                        browser_state = {
                            "url": getattr(browser, "current_url", None),
                            "title": getattr(browser, "title", None),
                        }
                    except Exception:
                        pass

                # Start step tracing
                await handler.handle_step_start(
                    step_number=step_number,
                    browser_state=browser_state,
                )

                try:
                    result = await original_step(self, *args, **kwargs)

                    # Extract action and reasoning from result
                    action_taken = None
                    reasoning = None
                    is_done = False

                    if result:
                        if hasattr(result, "actions") and result.actions:
                            action_taken = str(result.actions[-1])
                        if hasattr(result, "reasoning"):
                            reasoning = result.reasoning
                        if hasattr(result, "is_done"):
                            is_done = result.is_done
                        elif hasattr(result, "done"):
                            is_done = result.done

                    await handler.handle_step_end(
                        step_number=step_number,
                        action_taken=action_taken,
                        reasoning=reasoning,
                        is_done=is_done,
                    )

                    return result

                except Exception as e:
                    await handler.handle_step_error(
                        step_number=step_number,
                        error=str(e),
                    )
                    raise

            return await original_step(self, *args, **kwargs)

        Agent.run = traced_run
        Agent.step = traced_step
        _patched_classes.add(Agent)

        logger.debug("Patched browser-use Agent for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("browser-use not installed, skipping Agent patching")
        return False
    except Exception as e:
        logger.warning(f"Failed to patch browser-use Agent: {e}")
        return False


def _patch_llm_base() -> bool:
    """Patch browser-use LLM base class for automatic LLM call tracing."""
    try:
        from browser_use.llm import base

        # Check if BaseChatModel exists (it's a Protocol, so we patch implementations)
        if not hasattr(base, "BaseChatModel"):
            return True

        BaseChatModel = base.BaseChatModel

        if BaseChatModel in _patched_classes:
            return True

        # Since BaseChatModel is a Protocol, we need to patch actual implementations
        # Patch common LLM classes
        _patch_llm_implementations()

        _patched_classes.add(BaseChatModel)
        logger.debug("Patched browser-use LLM classes for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("browser-use LLM module not found, skipping LLM patching")
        return False
    except Exception as e:
        logger.warning(f"Failed to patch browser-use LLM: {e}")
        return False


def _patch_llm_implementations() -> None:
    """Patch specific LLM implementations."""
    llm_classes_to_patch = [
        ("browser_use.llm.providers.openai", "ChatOpenAI"),
        ("browser_use.llm.providers.anthropic", "ChatAnthropic"),
        ("browser_use.llm.providers.google", "ChatGoogleGenerativeAI"),
        ("browser_use", "ChatBrowserUse"),
    ]

    for module_path, class_name in llm_classes_to_patch:
        try:
            import importlib

            module = importlib.import_module(module_path)
            cls = getattr(module, class_name, None)

            if cls and cls not in _patched_classes:
                _patch_llm_class(cls)
                _patched_classes.add(cls)
                logger.debug(f"Patched {module_path}.{class_name}")
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"Could not patch {module_path}.{class_name}: {e}")


def _patch_llm_class(cls: Any) -> None:
    """Patch a specific LLM class's ainvoke method."""
    if not hasattr(cls, "ainvoke"):
        return

    original_ainvoke = cls.ainvoke

    @functools.wraps(original_ainvoke)
    async def traced_ainvoke(self, messages, output_format=None, **kwargs) -> Any:
        """Traced version of ainvoke."""
        from ...client import get_aigie
        from .cost_tracking import extract_tokens_from_response, get_browser_use_cost

        aigie = get_aigie()

        # Check if we have a handler from the agent
        handler = None
        if hasattr(self, "_aigie_handler"):
            handler = self._aigie_handler

        if aigie and aigie._initialized:
            # Get model name
            model = getattr(self, "model", getattr(self, "model_name", "unknown"))
            call_id = str(uuid.uuid4())

            # Get parent step from context if available
            parent_step = None

            if handler:
                await handler.handle_llm_start(
                    call_id=call_id,
                    model=model,
                    messages=messages,
                    parent_step=parent_step,
                )

            try:
                result = await original_ainvoke(self, messages, output_format, **kwargs)

                if handler:
                    # Extract tokens
                    tokens = extract_tokens_from_response(result)
                    input_tokens = tokens.get("input_tokens", 0) if tokens else 0
                    output_tokens = tokens.get("output_tokens", 0) if tokens else 0

                    # Calculate cost
                    cost_info = get_browser_use_cost(model, input_tokens, output_tokens)
                    cost = cost_info.get("total_cost", 0.0) if cost_info else 0.0

                    await handler.handle_llm_end(
                        call_id=call_id,
                        output=result,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        cost=cost,
                    )

                return result

            except Exception as e:
                if handler:
                    await handler.handle_llm_error(call_id=call_id, error=str(e))
                raise

        return await original_ainvoke(self, messages, output_format, **kwargs)

    cls.ainvoke = traced_ainvoke


def _patch_browser() -> bool:
    """Patch browser-use Browser class for action tracing."""
    try:
        from browser_use import Browser

        if Browser in _patched_classes:
            return True

        # Patch common browser actions
        action_methods = [
            "click",
            "type",
            "navigate",
            "scroll",
            "wait",
            "screenshot",
            "get_page_content",
            "execute_action",
        ]

        for method_name in action_methods:
            if hasattr(Browser, method_name):
                original_method = getattr(Browser, method_name)
                if callable(original_method):
                    setattr(
                        Browser, method_name, _create_traced_action(method_name, original_method)
                    )

        _patched_classes.add(Browser)
        logger.debug("Patched browser-use Browser for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("browser-use Browser not found, skipping Browser patching")
        return False
    except Exception as e:
        logger.warning(f"Failed to patch browser-use Browser: {e}")
        return False


def _create_traced_action(action_name: str, original_method: Any) -> Any:
    """Create a traced version of a browser action method."""

    @functools.wraps(original_method)
    async def traced_action(self, *args, **kwargs) -> Any:
        """Traced version of browser action."""
        from ...client import get_aigie

        aigie = get_aigie()
        handler = getattr(self, "_aigie_handler", None)

        if aigie and aigie._initialized and handler:
            action_id = str(uuid.uuid4())

            # Build params from args
            params = {"args": [str(a)[:200] for a in args]}
            params.update({k: str(v)[:200] for k, v in kwargs.items()})

            await handler.handle_action_start(
                action_type=action_name,
                action_id=action_id,
                params=params,
            )

            try:
                result = await original_method(self, *args, **kwargs)

                # Capture screenshot for certain actions if enabled
                screenshot_b64 = None
                if action_name in ["click", "type", "navigate", "scroll"]:
                    if hasattr(handler, "capture_screenshots") and handler.capture_screenshots:
                        try:
                            if hasattr(self, "screenshot"):
                                from .utils import compress_screenshot, screenshot_to_base64

                                screenshot_bytes = await self.screenshot()
                                screenshot_bytes = compress_screenshot(screenshot_bytes)
                                screenshot_b64 = screenshot_to_base64(screenshot_bytes)
                        except Exception:
                            pass

                await handler.handle_action_end(
                    action_id=action_id,
                    success=True,
                    result=result,
                    screenshot_b64=screenshot_b64,
                )

                return result

            except Exception as e:
                await handler.handle_action_error(action_id=action_id, error=str(e))
                raise

        return await original_method(self, *args, **kwargs)

    return traced_action


def unpatch_browser_use() -> None:
    """Remove all browser-use patches."""
    global _patched_classes
    _patched_classes.clear()
    logger.debug("Removed all browser-use auto-instrumentation patches")


def is_browser_use_patched() -> bool:
    """Check if browser-use has been patched."""
    return len(_patched_classes) > 0
