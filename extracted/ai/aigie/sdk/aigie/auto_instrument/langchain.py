"""
LangChain auto-instrumentation.

Automatically patches LangChain classes to inject Aigie callbacks and create traces.
"""

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

from aigie.auto_instrument._callback_utils import _safe_add_callback  # noqa: F401

_patched_classes = set()
_callback_manager_patched = False


def patch_langchain() -> None:
    """Patch LangChain classes for auto-instrumentation."""
    # Patch BaseCallbackManager to auto-inject our callback (like Traceloop does)
    _patch_callback_manager()
    _patch_agent_executor()
    _patch_create_agent()


def _patch_callback_manager() -> None:
    """Patch BaseCallbackManager.__init__ to auto-inject AigieCallbackHandler.

    This ensures our callback handler is present in all LangChain/LangGraph operations,
    which allows proper tracing hierarchy and prevents duplicate traces.
    """
    global _callback_manager_patched
    if _callback_manager_patched:
        return

    try:
        from langchain_core.callbacks import BaseCallbackManager

        from aigie.callback import AigieCallbackHandler
        from aigie.client import get_aigie

        original_init = BaseCallbackManager.__init__

        @functools.wraps(original_init)
        def patched_init(self, *args, **kwargs):
            """Patched __init__ that auto-injects AigieCallbackHandler."""
            original_init(self, *args, **kwargs)

            # Skip injection when we're already in a callback-traced context
            # (LangGraph auto-instrument already injected our handler)
            from aigie.auto_instrument.trace import is_in_callback_context

            if is_in_callback_context():
                return

            # Check if we already have an AigieCallbackHandler
            aigie = get_aigie()
            if aigie and aigie._initialized:
                has_aigie_handler = False
                for handler in self.inheritable_handlers:
                    if isinstance(handler, AigieCallbackHandler):
                        has_aigie_handler = True
                        break

                if not has_aigie_handler:
                    # Get current trace from context
                    from aigie.auto_instrument.trace import get_current_trace

                    trace = get_current_trace()

                    if trace:
                        # Create and add AigieCallbackHandler
                        callback = AigieCallbackHandler(aigie=aigie, trace=trace)
                        self.add_handler(callback, inherit=True)
                        logger.debug(
                            f"Auto-injected AigieCallbackHandler into BaseCallbackManager for trace {trace.id}"
                        )

        BaseCallbackManager.__init__ = patched_init
        _callback_manager_patched = True
        logger.debug("Patched BaseCallbackManager.__init__ for auto-injection")

    except ImportError:
        pass  # LangChain not installed
    except Exception as e:
        logger.warning(f"Failed to patch BaseCallbackManager: {e}")


def _patch_agent_executor() -> None:
    """Patch AgentExecutor to auto-inject callbacks."""
    try:
        try:
            from langchain.agents import AgentExecutor
        except ImportError:
            # LangChain 1.x moved AgentExecutor to langchain_classic.agents.
            from langchain_classic.agents import AgentExecutor

        if AgentExecutor in _patched_classes:
            return
        if getattr(AgentExecutor.ainvoke, "_aigie_patched", False):
            return

        original_ainvoke = AgentExecutor.ainvoke
        original_invoke = AgentExecutor.invoke

        @functools.wraps(original_ainvoke)
        async def traced_ainvoke(self, inputs: dict[str, Any], config=None, **kwargs) -> Any:
            """Traced version of ainvoke."""
            if config is not None:
                kwargs["config"] = config
            from aigie.auto_instrument.trace import get_or_create_trace
            from aigie.callback import AigieCallbackHandler
            from aigie.client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                # Get agent name safely
                agent_name = "agent"
                agent_class = None
                if hasattr(self, "agent"):
                    agent = self.agent
                    # Try to get name from various possible attributes
                    if hasattr(agent, "name"):
                        agent_name = getattr(agent, "name", "agent")
                    elif hasattr(agent, "__class__"):
                        agent_name = agent.__class__.__name__
                        agent_class = f"{agent.__class__.__module__}.{agent.__class__.__name__}"
                    elif isinstance(agent, dict):
                        agent_name = agent.get("name", "agent")

                # Extract tool names from AgentExecutor
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

                # Extract workflow type from inputs or metadata
                workflow_type = None
                domain = None
                if isinstance(inputs, dict):
                    workflow_type = inputs.get("workflow_type")
                    domain = inputs.get("domain")
                    # Also check nested structures
                    if not workflow_type and "metadata" in inputs:
                        workflow_type = inputs["metadata"].get("workflow_type")
                    if not domain and "metadata" in inputs:
                        domain = inputs["metadata"].get("domain")

                # Create workflow type identifier
                workflow_type_id = workflow_type
                if not workflow_type_id:
                    # Generate from agent + tools
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
                    trace_metadata["workflow_type"] = workflow_type
                    trace_metadata["original_workflow_type"] = workflow_type
                if domain:
                    trace_metadata["domain"] = domain

                # Clear any existing trace context to ensure each workflow gets its own trace
                from aigie.auto_instrument.trace import clear_current_trace

                clear_current_trace()

                # Create descriptive trace name with workflow context
                # Extract query from inputs for better trace naming
                query_snippet = ""
                if isinstance(inputs, dict):
                    query = inputs.get("input") or inputs.get("messages")
                    if query:
                        if isinstance(query, str):
                            query_snippet = query[:50] + "..." if len(query) > 50 else query
                        elif isinstance(query, list) and query:
                            # Extract from message list
                            first_msg = query[0]
                            if hasattr(first_msg, "content"):
                                query_snippet = (
                                    first_msg.content[:50] + "..."
                                    if len(first_msg.content) > 50
                                    else first_msg.content
                                )
                            elif isinstance(first_msg, dict):
                                query_snippet = str(first_msg.get("content", ""))[:50]

                # Build trace name with workflow type and query context
                if workflow_type_id and query_snippet:
                    trace_name = f"{workflow_type_id.replace('_', ' ').title()}: {query_snippet}"
                elif workflow_type_id:
                    trace_name = f"{workflow_type_id.replace('_', ' ').title()} Workflow"
                elif query_snippet:
                    trace_name = f"{agent_name}: {query_snippet}"
                else:
                    trace_name = f"Agent: {agent_name}"

                # Create new trace for this workflow (don't reuse existing)
                trace = await get_or_create_trace(name=trace_name, metadata=trace_metadata)

                # Create callback handler
                callback = AigieCallbackHandler(aigie=aigie, trace=trace)

                # Inject callback into config
                if "config" not in kwargs:
                    kwargs["config"] = {}
                _safe_add_callback(kwargs["config"], callback)

            from aigie.auto_instrument.trace import set_callback_context

            set_callback_context(True)
            try:
                return await original_ainvoke(self, inputs, **kwargs)
            finally:
                set_callback_context(False)

        @functools.wraps(original_invoke)
        def traced_invoke(self, inputs: dict[str, Any], config=None, **kwargs) -> Any:
            """Traced version of invoke."""
            if config is not None:
                kwargs["config"] = config
            from aigie.auto_instrument.trace import get_or_create_trace_sync
            from aigie.callback import AigieCallbackHandler
            from aigie.client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                # Get agent name safely
                agent_name = "agent"
                agent_class = None
                if hasattr(self, "agent"):
                    agent = self.agent
                    # Try to get name from various possible attributes
                    if hasattr(agent, "name"):
                        agent_name = getattr(agent, "name", "agent")
                    elif hasattr(agent, "__class__"):
                        agent_name = agent.__class__.__name__
                        agent_class = f"{agent.__class__.__module__}.{agent.__class__.__name__}"
                    elif isinstance(agent, dict):
                        agent_name = agent.get("name", "agent")

                # Extract tool names from AgentExecutor
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

                # Extract workflow type from inputs, kwargs config metadata, or inputs metadata
                workflow_type = None
                domain = None

                # Check kwargs config metadata first (passed from app code)
                if "config" in kwargs and isinstance(kwargs["config"], dict):
                    config_metadata = kwargs["config"].get("metadata", {})
                    if isinstance(config_metadata, dict):
                        workflow_type = config_metadata.get("workflow_type") or config_metadata.get(
                            "use_case"
                        )
                        domain = config_metadata.get("domain")

                # Fallback to inputs
                if isinstance(inputs, dict):
                    if not workflow_type:
                        workflow_type = inputs.get("workflow_type")
                    if not domain:
                        domain = inputs.get("domain")
                    # Also check nested structures
                    if not workflow_type and "metadata" in inputs:
                        workflow_type = inputs["metadata"].get("workflow_type")
                    if not domain and "metadata" in inputs:
                        domain = inputs["metadata"].get("domain")

                # Create workflow type identifier
                workflow_type_id = workflow_type
                if not workflow_type_id:
                    # Generate from agent + tools
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
                    trace_metadata["workflow_type"] = workflow_type
                    trace_metadata["original_workflow_type"] = workflow_type
                if domain:
                    trace_metadata["domain"] = domain

                # Clear any existing trace context to ensure each workflow gets its own trace
                from aigie.auto_instrument.trace import clear_current_trace

                clear_current_trace()

                # Create descriptive trace name with workflow context
                # Extract query from inputs for better trace naming
                query_snippet = ""
                if isinstance(inputs, dict):
                    query = inputs.get("input") or inputs.get("messages")
                    if query:
                        if isinstance(query, str):
                            query_snippet = query[:50] + "..." if len(query) > 50 else query
                        elif isinstance(query, list) and query:
                            # Extract from message list
                            first_msg = query[0]
                            if hasattr(first_msg, "content"):
                                query_snippet = (
                                    first_msg.content[:50] + "..."
                                    if len(first_msg.content) > 50
                                    else first_msg.content
                                )
                            elif isinstance(first_msg, dict):
                                query_snippet = str(first_msg.get("content", ""))[:50]

                # Build trace name with workflow type and query context
                if workflow_type_id and query_snippet:
                    trace_name = f"{workflow_type_id.replace('_', ' ').title()}: {query_snippet}"
                elif workflow_type_id:
                    trace_name = f"{workflow_type_id.replace('_', ' ').title()} Workflow"
                elif query_snippet:
                    trace_name = f"{agent_name}: {query_snippet}"
                else:
                    trace_name = f"Agent: {agent_name}"

                # Use sync version for sync invoke
                trace = get_or_create_trace_sync(name=trace_name, metadata=trace_metadata)

                if trace:
                    callback = AigieCallbackHandler(aigie=aigie, trace=trace)
                    if "config" not in kwargs:
                        kwargs["config"] = {}
                    _safe_add_callback(kwargs["config"], callback)

            from aigie.auto_instrument.trace import set_callback_context

            set_callback_context(True)
            try:
                return original_invoke(self, inputs, **kwargs)
            finally:
                set_callback_context(False)

        traced_ainvoke._aigie_patched = True
        traced_invoke._aigie_patched = True
        AgentExecutor.ainvoke = traced_ainvoke
        AgentExecutor.invoke = traced_invoke
        _patched_classes.add(AgentExecutor)

        logger.debug("Patched AgentExecutor for auto-instrumentation")

    except ImportError:
        pass  # LangChain not installed
    except Exception as e:
        logger.warning(f"Failed to patch AgentExecutor: {e}")


def _patch_create_agent() -> None:
    """Patch create_agent function to return auto-instrumented agent."""
    try:
        try:
            from langchain.agents import create_agent
        except ImportError:
            # LangChain 1.x moved create_agent to langchain_classic.agents.
            from langchain_classic.agents import create_agent

        if create_agent in _patched_classes:
            return

        original_create_agent = create_agent

        @functools.wraps(original_create_agent)
        def traced_create_agent(*args, **kwargs):
            """Traced version of create_agent."""
            agent = original_create_agent(*args, **kwargs)

            # Patch the agent's invoke methods
            if hasattr(agent, "ainvoke"):
                original_ainvoke = agent.ainvoke

                async def traced_ainvoke(inputs: dict[str, Any], **kwargs):
                    from aigie.auto_instrument.trace import get_or_create_trace
                    from aigie.callback import AigieCallbackHandler
                    from aigie.client import get_aigie

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

        # Replace the function
        import langchain.agents

        langchain.agents.create_agent = traced_create_agent
        _patched_classes.add(create_agent)

        logger.debug("Patched create_agent for auto-instrumentation")

    except ImportError:
        pass  # LangChain not installed
    except Exception as e:
        logger.warning(f"Failed to patch create_agent: {e}")
