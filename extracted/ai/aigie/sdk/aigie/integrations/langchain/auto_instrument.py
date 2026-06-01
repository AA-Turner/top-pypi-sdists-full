"""
LangChain auto-instrumentation.

Automatically patches LangChain classes to inject Aigie callbacks and create traces.
"""

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()

# LangGraph compiled graph class names — skip in Runnable patch to avoid double-patching
_LANGGRAPH_CLASS_NAMES = frozenset(("CompiledStateGraph", "CompiledGraph", "Pregel"))


from ...auto_instrument._callback_utils import _safe_add_callback  # noqa: F401


def patch_langchain() -> bool:
    """Patch LangChain classes for auto-instrumentation.

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _patch_agent_executor() and success
    success = _patch_create_agent() and success
    success = _patch_chain_base() and success
    success = _patch_runnable() and success
    return _patch_tool_run() and success


def unpatch_langchain() -> None:
    """Remove LangChain patches (for testing)."""
    global _patched_classes
    _patched_classes.clear()


def is_langchain_patched() -> bool:
    """Check if LangChain has been patched."""
    return len(_patched_classes) > 0


def _patch_agent_executor() -> bool:
    """Patch AgentExecutor to auto-inject callbacks."""
    try:
        from langchain.agents import AgentExecutor

        if AgentExecutor in _patched_classes:
            return True
        if getattr(AgentExecutor.ainvoke, "_aigie_patched", False):
            return True  # Already patched by primary

        original_ainvoke = AgentExecutor.ainvoke
        original_invoke = AgentExecutor.invoke

        @functools.wraps(original_ainvoke)
        async def traced_ainvoke(self, inputs: dict[str, Any], config=None, **kwargs) -> Any:
            """Traced version of ainvoke."""
            if config is not None:
                kwargs["config"] = config
            try:
                from ...auto_instrument.trace import clear_current_trace, get_or_create_trace
                from ...callback import AigieCallbackHandler
                from ...client import get_aigie

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    # Get agent name safely
                    agent_name = "agent"
                    agent_class = None
                    if hasattr(self, "agent"):
                        agent = self.agent
                        if hasattr(agent, "name"):
                            agent_name = getattr(agent, "name", "agent")
                        elif hasattr(agent, "__class__"):
                            agent_name = agent.__class__.__name__
                            agent_class = f"{agent.__class__.__module__}.{agent.__class__.__name__}"
                        elif isinstance(agent, dict):
                            agent_name = agent.get("name", "agent")

                    # Extract tool names
                    tool_names = []
                    if hasattr(self, "tools"):
                        tools = getattr(self, "tools", [])
                        if tools:
                            for tool in tools:
                                if hasattr(tool, "name"):
                                    tool_names.append(tool.name)
                                elif isinstance(tool, dict):
                                    tool_names.append(tool.get("name", "unknown_tool"))
                                elif isinstance(tool, str):
                                    tool_names.append(tool)

                    # Extract workflow type from inputs
                    workflow_type = None
                    domain = None
                    if isinstance(inputs, dict):
                        workflow_type = inputs.get("workflow_type")
                        domain = inputs.get("domain")
                        if not workflow_type and "metadata" in inputs:
                            workflow_type = inputs["metadata"].get("workflow_type")
                        if not domain and "metadata" in inputs:
                            domain = inputs["metadata"].get("domain")

                    # Create workflow type identifier
                    workflow_type_id = workflow_type
                    if not workflow_type_id:
                        tool_count = len(tool_names)
                        if tool_count > 0:
                            workflow_type_id = f"{agent_name}_{tool_count}tools"
                        else:
                            workflow_type_id = (
                                agent_name.lower().replace("agent", "").strip() or "agent_workflow"
                            )

                    # Build enriched metadata
                    trace_metadata = {
                        "type": "agent_executor",
                        "inputs": inputs,
                        "agent_type": agent_name,
                        "workflow_type": workflow_type_id,
                    }

                    if agent_class:
                        trace_metadata["agent_class"] = agent_class
                    if tool_names:
                        trace_metadata["tools_used"] = tool_names
                    if workflow_type:
                        trace_metadata["original_workflow_type"] = workflow_type
                    if domain:
                        trace_metadata["domain"] = domain

                    # Clear existing trace context
                    clear_current_trace()

                    # Create descriptive trace name
                    query_snippet = ""
                    if isinstance(inputs, dict):
                        query = inputs.get("input") or inputs.get("messages")
                        if query:
                            if isinstance(query, str):
                                query_snippet = query[:50] + "..." if len(query) > 50 else query
                            elif isinstance(query, list) and query:
                                first_msg = query[0]
                                if hasattr(first_msg, "content"):
                                    query_snippet = (
                                        first_msg.content[:50] + "..."
                                        if len(first_msg.content) > 50
                                        else first_msg.content
                                    )
                                elif isinstance(first_msg, dict):
                                    query_snippet = str(first_msg.get("content", ""))[:50]

                    if workflow_type_id and query_snippet:
                        trace_name = (
                            f"{workflow_type_id.replace('_', ' ').title()}: {query_snippet}"
                        )
                    elif workflow_type_id:
                        trace_name = f"{workflow_type_id.replace('_', ' ').title()} Workflow"
                    elif query_snippet:
                        trace_name = f"{agent_name}: {query_snippet}"
                    else:
                        trace_name = f"Agent: {agent_name}"

                    trace = await get_or_create_trace(name=trace_name, metadata=trace_metadata)

                    callback = AigieCallbackHandler(aigie=aigie, trace=trace)

                    if "config" not in kwargs:
                        kwargs["config"] = {}
                    _safe_add_callback(kwargs["config"], callback)

            except Exception as e:
                logger.warning(f"[AIGIE] LangChain tracing setup failed (non-fatal): {e}")

            return await original_ainvoke(self, inputs, **kwargs)

        @functools.wraps(original_invoke)
        def traced_invoke(self, inputs: dict[str, Any], config=None, **kwargs) -> Any:
            """Traced version of invoke."""
            if config is not None:
                kwargs["config"] = config
            try:
                from ...auto_instrument.trace import clear_current_trace, get_or_create_trace_sync
                from ...callback import AigieCallbackHandler
                from ...client import get_aigie

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    # Get agent name safely
                    agent_name = "agent"
                    agent_class = None
                    if hasattr(self, "agent"):
                        agent = self.agent
                        if hasattr(agent, "name"):
                            agent_name = getattr(agent, "name", "agent")
                        elif hasattr(agent, "__class__"):
                            agent_name = agent.__class__.__name__
                            agent_class = f"{agent.__class__.__module__}.{agent.__class__.__name__}"
                        elif isinstance(agent, dict):
                            agent_name = agent.get("name", "agent")

                    # Extract tool names
                    tool_names = []
                    if hasattr(self, "tools"):
                        tools = getattr(self, "tools", [])
                        if tools:
                            for tool in tools:
                                if hasattr(tool, "name"):
                                    tool_names.append(tool.name)
                                elif isinstance(tool, dict):
                                    tool_names.append(tool.get("name", "unknown_tool"))
                                elif isinstance(tool, str):
                                    tool_names.append(tool)

                    # Extract workflow type
                    workflow_type = None
                    domain = None

                    if "config" in kwargs and isinstance(kwargs["config"], dict):
                        config_metadata = kwargs["config"].get("metadata", {})
                        if isinstance(config_metadata, dict):
                            workflow_type = config_metadata.get(
                                "workflow_type"
                            ) or config_metadata.get("use_case")
                            domain = config_metadata.get("domain")

                    if isinstance(inputs, dict):
                        if not workflow_type:
                            workflow_type = inputs.get("workflow_type")
                        if not domain:
                            domain = inputs.get("domain")
                        if not workflow_type and "metadata" in inputs:
                            workflow_type = inputs["metadata"].get("workflow_type")
                        if not domain and "metadata" in inputs:
                            domain = inputs["metadata"].get("domain")

                    workflow_type_id = workflow_type
                    if not workflow_type_id:
                        tool_count = len(tool_names)
                        if tool_count > 0:
                            workflow_type_id = f"{agent_name}_{tool_count}tools"
                        else:
                            workflow_type_id = (
                                agent_name.lower().replace("agent", "").strip() or "agent_workflow"
                            )

                    trace_metadata = {
                        "type": "agent_executor",
                        "inputs": inputs,
                        "agent_type": agent_name,
                        "workflow_type": workflow_type_id,
                    }

                    if agent_class:
                        trace_metadata["agent_class"] = agent_class
                    if tool_names:
                        trace_metadata["tools_used"] = tool_names
                    if workflow_type:
                        trace_metadata["original_workflow_type"] = workflow_type
                    if domain:
                        trace_metadata["domain"] = domain

                    clear_current_trace()

                    query_snippet = ""
                    if isinstance(inputs, dict):
                        query = inputs.get("input") or inputs.get("messages")
                        if query:
                            if isinstance(query, str):
                                query_snippet = query[:50] + "..." if len(query) > 50 else query
                            elif isinstance(query, list) and query:
                                first_msg = query[0]
                                if hasattr(first_msg, "content"):
                                    query_snippet = (
                                        first_msg.content[:50] + "..."
                                        if len(first_msg.content) > 50
                                        else first_msg.content
                                    )
                                elif isinstance(first_msg, dict):
                                    query_snippet = str(first_msg.get("content", ""))[:50]

                    if workflow_type_id and query_snippet:
                        trace_name = (
                            f"{workflow_type_id.replace('_', ' ').title()}: {query_snippet}"
                        )
                    elif workflow_type_id:
                        trace_name = f"{workflow_type_id.replace('_', ' ').title()} Workflow"
                    elif query_snippet:
                        trace_name = f"{agent_name}: {query_snippet}"
                    else:
                        trace_name = f"Agent: {agent_name}"

                    trace = get_or_create_trace_sync(name=trace_name, metadata=trace_metadata)

                    if trace:
                        callback = AigieCallbackHandler(aigie=aigie, trace=trace)
                        if "config" not in kwargs:
                            kwargs["config"] = {}
                        _safe_add_callback(kwargs["config"], callback)

            except Exception as e:
                logger.warning(f"[AIGIE] LangChain tracing setup failed (non-fatal): {e}")

            return original_invoke(self, inputs, **kwargs)

        traced_ainvoke._aigie_patched = True
        traced_invoke._aigie_patched = True
        AgentExecutor.ainvoke = traced_ainvoke
        AgentExecutor.invoke = traced_invoke
        _patched_classes.add(AgentExecutor)

        logger.debug("Patched AgentExecutor for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("LangChain not installed, skipping AgentExecutor patch")
        return True  # Not an error if LangChain not installed
    except Exception as e:
        logger.warning(f"Failed to patch AgentExecutor: {e}")
        return False


def _patch_create_agent() -> bool:
    """Patch create_agent function to return auto-instrumented agent."""
    try:
        from langchain.agents import create_agent

        if create_agent in _patched_classes:
            return True

        original_create_agent = create_agent

        @functools.wraps(original_create_agent)
        def traced_create_agent(*args, **kwargs):
            """Traced version of create_agent."""
            agent = original_create_agent(*args, **kwargs)

            if hasattr(agent, "ainvoke"):
                original_ainvoke = agent.ainvoke

                async def traced_ainvoke(inputs: dict[str, Any], **kwargs):
                    from ...auto_instrument.trace import get_or_create_trace
                    from ...callback import AigieCallbackHandler
                    from ...client import get_aigie

                    aigie = get_aigie()
                    if aigie and aigie._initialized:
                        trace = await get_or_create_trace(
                            name="LangChain Agent", metadata={"type": "agent", "inputs": inputs}
                        )
                        callback = AigieCallbackHandler(aigie=aigie, trace=trace)

                        if "config" not in kwargs:
                            kwargs["config"] = {}
                        _safe_add_callback(kwargs["config"], callback)

                    return await original_ainvoke(inputs, **kwargs)

                traced_ainvoke._aigie_patched = True
                agent.ainvoke = traced_ainvoke

            return agent

        import langchain.agents

        langchain.agents.create_agent = traced_create_agent
        _patched_classes.add(create_agent)

        logger.debug("Patched create_agent for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch create_agent: {e}")
        return False


def _patch_chain_base() -> bool:
    """Patch Chain base class to auto-instrument all chains."""
    try:
        from langchain_core.chains import Chain

        if Chain in _patched_classes:
            return True
        if getattr(Chain.ainvoke, "_aigie_patched", False):
            return True  # Already patched by primary

        original_ainvoke = Chain.ainvoke
        original_invoke = Chain.invoke

        @functools.wraps(original_ainvoke)
        async def traced_ainvoke(self, inputs: dict[str, Any], config=None, **kwargs) -> Any:
            """Traced version of Chain.ainvoke."""
            if config is not None:
                kwargs["config"] = config
            from ...auto_instrument.trace import clear_current_trace, get_or_create_trace
            from ...callback import AigieCallbackHandler
            from ...client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                chain_name = getattr(self, "name", None)
                if not chain_name:
                    chain_name = type(self).__name__

                chain_class = f"{type(self).__module__}.{type(self).__name__}"

                clear_current_trace()

                if "config" not in kwargs:
                    kwargs["config"] = {}
                if "metadata" not in kwargs["config"]:
                    kwargs["config"]["metadata"] = {}
                kwargs["config"]["metadata"]["chain_class"] = chain_class
                kwargs["config"]["metadata"]["chain_name"] = chain_name

                trace = await get_or_create_trace(
                    name=f"Chain: {chain_name}",
                    metadata={"type": "chain", "chain_class": chain_class, "inputs": inputs},
                )

                callback = AigieCallbackHandler(aigie=aigie, trace=trace)
                _safe_add_callback(kwargs["config"], callback)

            return await original_ainvoke(self, inputs, **kwargs)

        @functools.wraps(original_invoke)
        def traced_invoke(self, inputs: dict[str, Any], config=None, **kwargs) -> Any:
            """Traced version of Chain.invoke."""
            if config is not None:
                kwargs["config"] = config
            from ...auto_instrument.trace import clear_current_trace, get_or_create_trace_sync
            from ...callback import AigieCallbackHandler
            from ...client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                chain_name = getattr(self, "name", None)
                if not chain_name:
                    chain_name = type(self).__name__

                chain_class = f"{type(self).__module__}.{type(self).__name__}"

                clear_current_trace()

                if "config" not in kwargs:
                    kwargs["config"] = {}
                if "metadata" not in kwargs["config"]:
                    kwargs["config"]["metadata"] = {}
                kwargs["config"]["metadata"]["chain_class"] = chain_class
                kwargs["config"]["metadata"]["chain_name"] = chain_name

                trace = get_or_create_trace_sync(
                    name=f"Chain: {chain_name}",
                    metadata={"type": "chain", "chain_class": chain_class, "inputs": inputs},
                )

                if trace:
                    callback = AigieCallbackHandler(aigie=aigie, trace=trace)
                    _safe_add_callback(kwargs["config"], callback)

            return original_invoke(self, inputs, **kwargs)

        traced_ainvoke._aigie_patched = True
        traced_invoke._aigie_patched = True
        Chain.ainvoke = traced_ainvoke
        Chain.invoke = traced_invoke
        _patched_classes.add(Chain)

        logger.debug("Patched Chain base class for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Chain: {e}")
        return False


def _patch_runnable() -> bool:
    """Patch Runnable base class for broader coverage."""
    try:
        from langchain_core.runnables import Runnable

        if Runnable in _patched_classes:
            return True
        if getattr(Runnable.ainvoke, "_aigie_patched", False):
            return True  # Already patched by primary

        original_ainvoke = Runnable.ainvoke
        original_invoke = Runnable.invoke

        @functools.wraps(original_ainvoke)
        async def traced_ainvoke(self, inputs: Any, config=None, **kwargs) -> Any:
            """Traced version of Runnable.ainvoke."""
            if config is not None:
                kwargs["config"] = config
            # Skip if this is a LangGraph compiled graph (already patched by langgraph)
            if type(self).__name__ in _LANGGRAPH_CLASS_NAMES:
                return await original_ainvoke(self, inputs, **kwargs)

            from ...auto_instrument.trace import get_or_create_trace
            from ...callback import AigieCallbackHandler
            from ...client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                runnable_name = getattr(self, "name", type(self).__name__)
                trace = await get_or_create_trace(
                    name=f"Runnable: {runnable_name}",
                    metadata={"type": "runnable", "runnable_class": type(self).__name__},
                )

                callback = AigieCallbackHandler(aigie=aigie, trace=trace)

                if "config" not in kwargs:
                    kwargs["config"] = {}
                _safe_add_callback(kwargs["config"], callback)

            return await original_ainvoke(self, inputs, **kwargs)

        @functools.wraps(original_invoke)
        def traced_invoke(self, inputs: Any, config=None, **kwargs) -> Any:
            """Traced version of Runnable.invoke."""
            if config is not None:
                kwargs["config"] = config
            # Skip if this is a LangGraph compiled graph (already patched by langgraph)
            if type(self).__name__ in _LANGGRAPH_CLASS_NAMES:
                return original_invoke(self, inputs, **kwargs)

            from ...auto_instrument.trace import get_or_create_trace_sync
            from ...callback import AigieCallbackHandler
            from ...client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                runnable_name = getattr(self, "name", type(self).__name__)
                trace = get_or_create_trace_sync(
                    name=f"Runnable: {runnable_name}",
                    metadata={"type": "runnable", "runnable_class": type(self).__name__},
                )

                if trace:
                    callback = AigieCallbackHandler(aigie=aigie, trace=trace)
                    if "config" not in kwargs:
                        kwargs["config"] = {}
                    _safe_add_callback(kwargs["config"], callback)

            return original_invoke(self, inputs, **kwargs)

        traced_ainvoke._aigie_patched = True
        traced_invoke._aigie_patched = True
        Runnable.ainvoke = traced_ainvoke
        Runnable.invoke = traced_invoke
        _patched_classes.add(Runnable)

        logger.debug("Patched Runnable base class for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Runnable: {e}")
        return False


def _patch_tool_run() -> bool:
    """Patch BaseTool._arun/_run to wrap tool execution with remediation.

    The patch is always applied, but the remediation engine and dispatcher
    are resolved lazily at call time (not patch time) because Aigie may not
    be initialized yet when auto-instrumentation runs.
    """
    try:
        from langchain_core.tools import BaseTool as LCBaseTool
    except ImportError:
        return True  # LangChain not installed

    if LCBaseTool in _patched_classes:
        return True
    if getattr(LCBaseTool._arun, "_aigie_patched", False):
        return True  # Already patched by primary

    import asyncio

    original_arun = LCBaseTool._arun
    original_run = LCBaseTool._run

    # Lazy-initialized engine — created on first tool call, not at patch time
    _engine_holder: dict[str, Any] = {}

    def _get_engine():
        """Lazily create remediation engine on first use."""
        if "engine" in _engine_holder:
            return _engine_holder["engine"], _engine_holder.get("config")
        from ...client import get_aigie
        from ...integrations.langchain.config import LangChainConfig

        config = LangChainConfig.from_env()
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
        _engine_holder["dispatcher"] = getattr(aigie, "_intervention_dispatcher", None)
        return engine, config

    @functools.wraps(original_arun)
    async def traced_arun(self, tool_input, **kwargs):
        """Wrapped _arun with remediation."""
        engine, config = _get_engine()
        if not engine:
            return await original_arun(self, tool_input, **kwargs)

        tool_name = getattr(self, "name", "unknown_tool")
        dispatcher = _engine_holder.get("dispatcher")

        # Gateway intervention check
        if dispatcher:
            from ...client import get_aigie

            aigie = get_aigie()
            trace_id = ""
            if aigie:
                from ...auto_instrument.trace import get_current_trace

                t = get_current_trace()
                if t:
                    trace_id = getattr(t, "trace_id", "")
            if trace_id:
                signal = dispatcher.pop_pending(trace_id)
                if signal:
                    if signal.intervention_type == "break_loop":
                        raise RuntimeError(f"[Aigie] {signal.reason}")
                    if signal.intervention_type == "delay":
                        await asyncio.sleep(signal.payload.get("delay_ms", 1000) / 1000.0)
                    elif signal.intervention_type == "inject_correction":
                        corrections = signal.payload.get("corrections", {})
                        if corrections and isinstance(tool_input, dict):
                            tool_input = {**tool_input, **corrections}

        try:
            return await original_arun(self, tool_input, **kwargs)
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
                                    return await original_arun(self, tool_input, **kwargs)

                                applicator.set_retry_executor(_retry_fn)
                                ctx = InterceptionContext(
                                    provider="langchain",
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

    @functools.wraps(original_run)
    def traced_run(self, tool_input, **kwargs):
        """Wrapped _run — sync tools pass through (remediation is async-only)."""
        return original_run(self, tool_input, **kwargs)

    traced_arun._aigie_patched = True
    traced_run._aigie_patched = True
    LCBaseTool._arun = traced_arun
    LCBaseTool._run = traced_run
    _patched_classes.add(LCBaseTool)

    logger.debug("Patched BaseTool._arun/_run for remediation")
    return True
