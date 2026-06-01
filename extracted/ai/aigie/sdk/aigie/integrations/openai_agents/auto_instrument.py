"""
OpenAI Agents SDK auto-instrumentation.

Automatically patches OpenAI Agents SDK classes to create traces.
Also patches tool execution with retry executor support for auto-fix remediation.
Provides RunHooks-based lifecycle tracing and gateway intervention support.
"""

import functools
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()

try:
    from agents import RunHooks as _RunHooksBase
except ImportError:
    _RunHooksBase = object  # type: ignore[assignment,misc]


class AigieRunHooks(_RunHooksBase):
    """RunHooks implementation for richer LLM-level tracing.

    Automatically injected into Runner.run() calls to capture
    agent lifecycle events (agent start/end, LLM start/end,
    tool start/end, handoffs) via the OpenAI Agents SDK RunHooks
    interface.
    """

    def __init__(self) -> None:
        self._handler: Any = None
        self._spans: dict[str, str] = {}

    def _get_handler(self) -> Any:
        """Lazily initialize the handler on first use."""
        if self._handler is None:
            try:
                from ...client import get_aigie

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    from .handler import OpenAIAgentsHandler

                    self._handler = OpenAIAgentsHandler(
                        trace_name="OpenAI Agents Run",
                        metadata={"source": "run_hooks"},
                    )
                    self._handler._aigie = aigie
            except Exception as e:
                logger.debug(f"Failed to initialize RunHooks handler: {e}")
        return self._handler

    async def on_agent_start(self, context: Any, agent: Any) -> None:
        """Called before agent execution begins."""
        try:
            handler = self._get_handler()
            if handler:
                agent_name = getattr(agent, "name", "unknown")
                span_id = await handler.handle_agent_start(
                    agent_name=agent_name,
                    model=getattr(agent, "model", None),
                    tools=[getattr(t, "name", str(t)) for t in getattr(agent, "tools", [])],
                    handoffs=[getattr(h, "name", str(h)) for h in getattr(agent, "handoffs", [])],
                )
                self._spans[f"agent:{agent_name}"] = span_id
        except Exception as e:
            logger.debug(f"RunHooks on_agent_start error: {e}")

    async def on_agent_end(self, context: Any, agent: Any, output: Any) -> None:
        """Called when agent produces final output."""
        try:
            handler = self._get_handler()
            if handler:
                agent_name = getattr(agent, "name", "unknown")
                span_id = self._spans.pop(f"agent:{agent_name}", None)
                if span_id:
                    await handler.handle_agent_end(
                        agent_id=span_id,
                        output=output,
                    )
        except Exception as e:
            logger.debug(f"RunHooks on_agent_end error: {e}")

    async def on_llm_start(
        self,
        context: Any,
        agent: Any,
        system_prompt: Any,
        input_items: Any,
    ) -> None:
        """Called before each LLM call."""
        try:
            handler = self._get_handler()
            if handler:
                agent_name = getattr(agent, "name", "unknown")
                model = getattr(agent, "model", None) or "unknown"

                # Build messages from system_prompt + input_items
                messages = []
                if system_prompt:
                    messages.append(
                        {
                            "role": "system",
                            "content": str(system_prompt)[:500],
                        }
                    )
                if input_items:
                    for item in input_items if isinstance(input_items, list) else [input_items]:
                        messages.append(
                            {
                                "role": "user",
                                "content": str(item)[:500],
                            }
                        )

                span_id = await handler.handle_generation_start(
                    model=model,
                    messages=messages,
                )
                self._spans[f"llm:{agent_name}"] = span_id
        except Exception as e:
            logger.debug(f"RunHooks on_llm_start error: {e}")

    async def on_llm_end(self, context: Any, agent: Any, response: Any) -> None:
        """Called after each LLM call completes."""
        try:
            handler = self._get_handler()
            if handler:
                agent_name = getattr(agent, "name", "unknown")
                span_id = self._spans.pop(f"llm:{agent_name}", None)
                if span_id:
                    # Extract token usage if available
                    usage = getattr(response, "usage", None)
                    input_tokens = getattr(usage, "input_tokens", 0) if usage else 0
                    output_tokens = getattr(usage, "output_tokens", 0) if usage else 0

                    await handler.handle_generation_end(
                        gen_id=span_id,
                        response=str(response)[:2000] if response else None,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                    )
        except Exception as e:
            logger.debug(f"RunHooks on_llm_end error: {e}")

    async def on_tool_start(self, context: Any, agent: Any, tool: Any) -> None:
        """Called before tool invocation."""
        try:
            handler = self._get_handler()
            if handler:
                tool_name = getattr(tool, "name", str(tool))
                span_id = await handler.handle_tool_start(
                    tool_name=tool_name,
                )
                self._spans[f"tool:{tool_name}"] = span_id
        except Exception as e:
            logger.debug(f"RunHooks on_tool_start error: {e}")

    async def on_tool_end(self, context: Any, agent: Any, tool: Any, result: Any) -> None:
        """Called after tool invocation completes."""
        try:
            handler = self._get_handler()
            if handler:
                tool_name = getattr(tool, "name", str(tool))
                span_id = self._spans.pop(f"tool:{tool_name}", None)
                if span_id:
                    await handler.handle_tool_end(
                        tool_id=span_id,
                        result=result,
                    )
        except Exception as e:
            logger.debug(f"RunHooks on_tool_end error: {e}")

    async def on_handoff(self, context: Any, from_agent: Any, to_agent: Any) -> None:
        """Called when an agent handoff occurs."""
        try:
            handler = self._get_handler()
            if handler:
                from_name = getattr(from_agent, "name", "unknown")
                to_name = getattr(to_agent, "name", "unknown")
                span_id = await handler.handle_handoff_start(
                    source_agent=from_name,
                    target_agent=to_name,
                )
                # Handoffs are instant events, close immediately
                if span_id:
                    await handler.handle_handoff_end(
                        handoff_id=span_id,
                        success=True,
                    )
        except Exception as e:
            logger.debug(f"RunHooks on_handoff error: {e}")


def patch_openai_agents() -> bool:
    """Patch OpenAI Agents SDK classes for auto-instrumentation.

    This adds the Aigie tracing processor to the SDK's tracing system.
    It's additive - it doesn't replace existing tracing.

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _add_aigie_processor() and success
    success = _patch_runner() and success
    success = _patch_agent() and success
    success = _patch_tool_execution() and success
    return _patch_run_hooks() and success


def unpatch_openai_agents() -> None:
    """Remove OpenAI Agents SDK patches (for testing)."""
    global _patched_classes
    _patched_classes.clear()


def is_openai_agents_patched() -> bool:
    """Check if OpenAI Agents SDK has been patched."""
    return len(_patched_classes) > 0


def _add_aigie_processor() -> bool:
    """Add Aigie tracing processor to the SDK.

    Returns:
        True if successful
    """
    try:
        # Try to import the SDK
        try:
            from agents import add_trace_processor
        except ImportError:
            try:
                from openai_agents import add_trace_processor
            except ImportError:
                logger.debug("OpenAI Agents SDK not installed")
                return False

        # Check if already added
        if "aigie_processor" in _patched_classes:
            return True

        # Create and add processor
        from .processor import AigieTracingProcessor

        processor = AigieTracingProcessor()

        try:
            add_trace_processor(processor)
            _patched_classes.add("aigie_processor")
            logger.debug("Added Aigie tracing processor to OpenAI Agents SDK")
        except Exception as e:
            logger.debug(f"Could not add trace processor: {e}")
            # Continue anyway - the processor can be added manually

        return True

    except Exception as e:
        logger.warning(f"Failed to add Aigie processor: {e}")
        return False


def _patch_runner() -> bool:
    """Patch Runner.run() and Runner.run_sync() methods.

    Returns:
        True if successful
    """
    try:
        # Try different import paths
        Runner = None
        try:
            from agents import Runner
        except ImportError:
            try:
                from openai_agents import Runner
            except ImportError:
                logger.debug("OpenAI Agents SDK Runner not found")
                return True

        if Runner in _patched_classes:
            return True

        original_run = getattr(Runner, "run", None)
        original_run_sync = getattr(Runner, "run_sync", None)

        if original_run:

            @functools.wraps(original_run)
            async def traced_run(agent, input_data, *args, **kwargs):
                """Traced version of Runner.run()."""
                from ...client import get_aigie
                from .handler import OpenAIAgentsHandler

                # Inject AigieRunHooks if no hooks provided
                if kwargs.get("hooks") is None:
                    try:
                        kwargs["hooks"] = AigieRunHooks()
                    except Exception as e:
                        logger.debug(f"Could not inject AigieRunHooks: {e}")

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    handler = OpenAIAgentsHandler(
                        trace_name=f"Agent: {getattr(agent, 'name', 'unknown')}",
                        metadata={"agent_type": type(agent).__name__},
                    )
                    handler._aigie = aigie

                    workflow_id = await handler.handle_workflow_start(
                        workflow_name=getattr(agent, "name", "agent_workflow"),
                        input_data=input_data,
                    )

                    try:
                        result = await original_run(agent, input_data, *args, **kwargs)

                        await handler.handle_workflow_end(
                            workflow_id=workflow_id,
                            output=result,
                        )

                        return result

                    except Exception as e:
                        await handler.handle_workflow_end(
                            workflow_id=workflow_id,
                            error=str(e),
                        )
                        raise

                return await original_run(agent, input_data, *args, **kwargs)

            Runner.run = staticmethod(traced_run)

        if original_run_sync:

            @functools.wraps(original_run_sync)
            def traced_run_sync(agent, input_data, *args, **kwargs):
                """Traced version of Runner.run_sync()."""
                import asyncio

                from ...client import get_aigie
                from .handler import OpenAIAgentsHandler

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    handler = OpenAIAgentsHandler(
                        trace_name=f"Agent: {getattr(agent, 'name', 'unknown')}",
                        metadata={"agent_type": type(agent).__name__},
                    )
                    handler._aigie = aigie

                    # Run async handler in sync context
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_workflow_start(
                                        workflow_name=getattr(agent, "name", "agent_workflow"),
                                        input_data=input_data,
                                    ),
                                )
                                workflow_id = future.result(timeout=5)
                        else:
                            workflow_id = loop.run_until_complete(
                                handler.handle_workflow_start(
                                    workflow_name=getattr(agent, "name", "agent_workflow"),
                                    input_data=input_data,
                                )
                            )
                    except Exception as e:
                        logger.debug(f"Error starting workflow trace: {e}")
                        return original_run_sync(agent, input_data, *args, **kwargs)

                    try:
                        result = original_run_sync(agent, input_data, *args, **kwargs)

                        try:
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                import concurrent.futures

                                with concurrent.futures.ThreadPoolExecutor() as executor:
                                    future = executor.submit(
                                        asyncio.run,
                                        handler.handle_workflow_end(
                                            workflow_id=workflow_id,
                                            output=result,
                                        ),
                                    )
                                    future.result(timeout=5)
                            else:
                                loop.run_until_complete(
                                    handler.handle_workflow_end(
                                        workflow_id=workflow_id,
                                        output=result,
                                    )
                                )
                        except Exception as e:
                            logger.debug(f"Error ending workflow trace: {e}")

                        return result

                    except Exception as e:
                        try:
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                import concurrent.futures

                                with concurrent.futures.ThreadPoolExecutor() as executor:
                                    future = executor.submit(
                                        asyncio.run,
                                        handler.handle_workflow_end(
                                            workflow_id=workflow_id,
                                            error=str(e),
                                        ),
                                    )
                                    future.result(timeout=5)
                            else:
                                loop.run_until_complete(
                                    handler.handle_workflow_end(
                                        workflow_id=workflow_id,
                                        error=str(e),
                                    )
                                )
                        except Exception:
                            pass
                        raise

                return original_run_sync(agent, input_data, *args, **kwargs)

            Runner.run_sync = staticmethod(traced_run_sync)

        _patched_classes.add(Runner)
        logger.debug("Patched Runner for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("OpenAI Agents SDK not installed, skipping Runner patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Runner: {e}")
        return False


def _patch_agent() -> bool:
    """Patch Agent class for additional instrumentation.

    Returns:
        True if successful
    """
    try:
        # Try different import paths
        Agent = None
        try:
            from agents import Agent
        except ImportError:
            try:
                from openai_agents import Agent
            except ImportError:
                logger.debug("OpenAI Agents SDK Agent not found")
                return True

        if Agent in _patched_classes:
            return True

        # Store original __init__
        original_init = Agent.__init__

        @functools.wraps(original_init)
        def traced_init(self, *args, **kwargs):
            """Traced version of Agent.__init__()."""
            original_init(self, *args, **kwargs)

            # Store agent info for tracing
            self._aigie_agent_id = str(uuid.uuid4())
            self._aigie_metadata = {
                "name": getattr(self, "name", "unknown"),
                "model": getattr(self, "model", None),
                "tools": [getattr(t, "name", str(t)) for t in getattr(self, "tools", [])],
                "handoffs": [getattr(h, "name", str(h)) for h in getattr(self, "handoffs", [])],
            }

        Agent.__init__ = traced_init
        _patched_classes.add(Agent)

        logger.debug("Patched Agent for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("OpenAI Agents SDK not installed, skipping Agent patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Agent: {e}")
        return False


def _patch_tool_execution() -> bool:
    """Patch OpenAI Agents SDK tool execution with remediation and retry executor.

    Wraps FunctionTool.on_invoke_tool (or equivalent) to add AutoFixApplicator
    with a retry executor, following the same pattern as the LangChain
    integration's _patch_tool_run.

    The patch is always applied, but the remediation engine and config
    are resolved lazily at call time (not patch time) because Aigie may
    not be initialized yet when auto-instrumentation runs.

    Returns:
        True if patching was successful
    """
    try:
        # Try to find the FunctionTool class
        FunctionTool = None
        try:
            from agents import FunctionTool
        except ImportError:
            try:
                from openai_agents import FunctionTool
            except ImportError:
                logger.debug(
                    "OpenAI Agents SDK FunctionTool not found, skipping tool remediation patch"
                )
                return True

        if FunctionTool in _patched_classes:
            return True

        # Find the async invocation method
        original_invoke = getattr(FunctionTool, "on_invoke_tool", None)
        if original_invoke is None:
            original_invoke = getattr(FunctionTool, "invoke", None)
        if original_invoke is None:
            logger.debug(
                "[AIGIE] OpenAI Agents FunctionTool has no on_invoke_tool/invoke method, skipping"
            )
            return True

        invoke_method_name = (
            "on_invoke_tool" if hasattr(FunctionTool, "on_invoke_tool") else "invoke"
        )

        if getattr(original_invoke, "_aigie_patched", False):
            return True  # Already patched

        # Lazy-initialized engine holder
        _engine_holder: dict[str, Any] = {}

        def _get_engine():
            """Lazily create remediation engine on first use."""
            if "engine" in _engine_holder:
                return _engine_holder["engine"], _engine_holder.get("config")
            from ...client import get_aigie
            from .config import OpenAIAgentsConfig

            config = OpenAIAgentsConfig()
            if not (config.enable_realtime_remediation and config.remediation_mode == "autonomous"):
                _engine_holder["engine"] = None
                _engine_holder["config"] = config
                return None, config
            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return None, config
            api_url = getattr(aigie, "api_url", None) or getattr(aigie, "_api_url", None)
            if not api_url:
                _engine_holder["engine"] = None
                _engine_holder["config"] = config
                return None, config
            from ...realtime.remediation_engine import RemediationEngine

            api_key = getattr(aigie, "_api_key", None) or getattr(aigie, "api_key", None)
            engine = RemediationEngine(
                api_url=api_url,
                api_key=api_key or "",
                query_timeout=getattr(config, "remediation_query_timeout", 2.0),
            )
            _engine_holder["engine"] = engine
            _engine_holder["config"] = config
            return engine, config

        @functools.wraps(original_invoke)
        async def traced_invoke(self, *args, **kwargs):
            """Wrapped tool invocation with remediation, gateway intervention, and retry executor."""
            # Check pending gateway intervention before executing
            try:
                from ...client import get_aigie

                aigie_inst = get_aigie()
                if aigie_inst and hasattr(aigie_inst, "_intervention_dispatcher"):
                    dispatcher = getattr(aigie_inst, "_intervention_dispatcher", None)
                    if dispatcher:
                        trace_id = getattr(self, "_aigie_trace_id", None)
                        if trace_id:
                            signal = dispatcher.pop_pending(trace_id)
                            if signal:
                                if signal.intervention_type == "delay":
                                    import asyncio

                                    delay_ms = signal.payload.get("delay_ms", 1000)
                                    await asyncio.sleep(delay_ms / 1000.0)
                                elif signal.intervention_type == "inject_correction":
                                    corrections = signal.payload.get("corrections", {})
                                    if corrections:
                                        kwargs = {**kwargs, **corrections}
                                elif signal.intervention_type == "break_loop":
                                    raise RuntimeError(f"[Aigie] {signal.reason}")
            except RuntimeError:
                raise
            except Exception as e:
                logger.debug(f"Gateway intervention check failed: {e}")

            engine, config = _get_engine()
            if not engine:
                return await original_invoke(self, *args, **kwargs)

            tool_name = getattr(self, "name", "unknown_tool")

            try:
                return await original_invoke(self, *args, **kwargs)
            except Exception as e:
                try:
                    rem = await engine.evaluate(
                        str(e),
                        tool_name,
                        "",
                        "",
                        mode=config.remediation_mode,
                    )
                    if rem and config.remediation_mode == "autonomous":
                        applied_programmatic = False
                        if rem.action_type:
                            try:
                                fix_action = engine.to_fix_action(rem)
                                if fix_action:
                                    from ...interceptor.protocols import InterceptionContext
                                    from ...realtime.auto_fix import AutoFixApplicator

                                    applicator = AutoFixApplicator()

                                    async def _retry_fn(**kw2):
                                        return await original_invoke(self, *args, **kwargs)

                                    applicator.set_retry_executor(_retry_fn)
                                    ctx = InterceptionContext(
                                        provider="openai_agents",
                                        model="",
                                        messages=[],
                                        response_content=str(e),
                                    )
                                    fix_result = await applicator.apply_fixes(ctx, [fix_action])
                                    if fix_result.success:
                                        applied_programmatic = True
                                        engine.mark_applied(rem)
                                        if fix_result.modified_response is not None:
                                            return fix_result.modified_response
                            except Exception as fix_err:
                                logger.debug(f"[AIGIE] Programmatic fix failed: {fix_err}")

                        if not applied_programmatic and rem.guidance_text:
                            engine.mark_applied(rem)
                            raise type(e)(f"{e}\n\n{rem.guidance_text}") from e
                except type(e):
                    raise
                except Exception:
                    pass
                raise

        traced_invoke._aigie_patched = True
        setattr(FunctionTool, invoke_method_name, traced_invoke)
        _patched_classes.add(FunctionTool)

        logger.debug(
            "[AIGIE] Patched OpenAI Agents FunctionTool for remediation with retry executor"
        )
        return True

    except ImportError:
        logger.debug("OpenAI Agents SDK not installed, skipping tool remediation patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch FunctionTool for remediation: {e}")
        return False


def _patch_run_hooks() -> bool:
    """Register AigieRunHooks availability for RunHooks-based tracing.

    The actual injection happens in the patched Runner.run() (traced_run),
    which sets AigieRunHooks as the default hooks when none are provided.
    This function validates that the RunHooks base class exists in the SDK
    so we know our AigieRunHooks will be compatible.

    Returns:
        True if RunHooks support is available or SDK not installed
    """
    try:
        # Verify RunHooks base class exists in the SDK
        try:
            from agents import RunHooks
        except ImportError:
            try:
                from openai_agents import RunHooks
            except ImportError:
                logger.debug(
                    "OpenAI Agents SDK RunHooks not found, "
                    "AigieRunHooks injection will rely on duck typing"
                )
                # Still return True -- AigieRunHooks uses duck typing
                # and will work even without the base class
                return True

        if "aigie_run_hooks" in _patched_classes:
            return True

        _patched_classes.add("aigie_run_hooks")
        logger.debug("AigieRunHooks registered for OpenAI Agents SDK")
        return True

    except Exception as e:
        logger.warning(f"Failed to register AigieRunHooks: {e}")
        return False
