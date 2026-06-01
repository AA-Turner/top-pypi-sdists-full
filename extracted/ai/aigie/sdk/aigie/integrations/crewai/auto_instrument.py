"""
CrewAI auto-instrumentation.

Automatically patches CrewAI classes to create traces and inject handlers.
Also registers native CrewAI hooks for LLM and tool call tracing,
and supports gateway intervention (break_loop, inject_correction, delay).
"""

import functools
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()


def _register_hooks() -> bool:
    """Register Aigie hooks using CrewAI's native hooks system.

    CrewAI hooks (v0.80+) provide:
    - before_llm_call: receives LLMCallHookContext with .messages, .agent, .task, .crew
    - after_llm_call: receives LLMCallHookContext with .response added
    - before_tool_call: receives ToolCallHookContext with .tool_name, .tool_input, .agent
    - after_tool_call: receives ToolCallHookContext with .tool_result added

    Returns:
        True if hooks registered (or CrewAI hooks not available — not an error)
    """
    try:
        from crewai.hooks import (
            register_after_llm_call_hook,
            register_after_tool_call_hook,
            register_before_llm_call_hook,
            register_before_tool_call_hook,
        )
    except ImportError:
        logger.debug("CrewAI hooks not available (older version), skipping hook registration")
        return True

    if "hooks" in _patched_classes:
        return True

    def _aigie_before_llm_call(context):
        """Capture LLM call start and check gateway intervention."""
        try:
            from ...client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return None

            import time

            context._aigie_start_time = time.monotonic()

            # Gateway intervention
            if hasattr(aigie, "_intervention_dispatcher"):
                dispatcher = getattr(aigie, "_intervention_dispatcher", None)
                if dispatcher:
                    crew = getattr(context, "crew", None)
                    handler = getattr(crew, "_aigie_handler", None) if crew else None
                    if handler and hasattr(handler, "trace_id") and handler.trace_id:
                        signal = dispatcher.pop_pending(handler.trace_id)
                        if signal:
                            if signal.intervention_type == "delay":
                                delay_ms = signal.payload.get("delay_ms", 1000)
                                time.sleep(delay_ms / 1000.0)
                            elif signal.intervention_type == "inject_correction":
                                corrections = signal.payload.get("corrections", {})
                                if corrections and hasattr(context, "messages"):
                                    context.messages.append(
                                        {
                                            "role": "system",
                                            "content": f"[Aigie correction] {corrections}",
                                        }
                                    )
                            elif signal.intervention_type == "break_loop":
                                return False  # Block execution

            return None
        except Exception as e:
            logger.debug(f"[AIGIE] Error in before_llm_call hook: {e}")
            return None

    def _aigie_after_llm_call(context):
        """Capture LLM call end with response."""
        try:
            from ...client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return

            crew = getattr(context, "crew", None)
            handler = getattr(crew, "_aigie_handler", None) if crew else None
            if handler and hasattr(handler, "handle_llm_end"):
                import asyncio

                agent_role = (
                    getattr(context.agent, "role", "unknown") if context.agent else "unknown"
                )
                response = getattr(context, "response", None)
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(
                        handler.handle_llm_end(
                            agent_role=agent_role,
                            response=str(response)[:2000] if response else None,
                        )
                    )
                except RuntimeError:
                    pass  # No running loop — best effort in sync context

            return
        except Exception as e:
            logger.debug(f"[AIGIE] Error in after_llm_call hook: {e}")
            return

    def _aigie_before_tool_call(context):
        """Capture tool call start."""
        try:
            from ...client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return

            tool_name = getattr(context, "tool_name", "unknown")
            logger.debug(f"[AIGIE] CrewAI tool call start: {tool_name}")
            return
        except Exception as e:
            logger.debug(f"[AIGIE] Error in before_tool_call hook: {e}")
            return

    def _aigie_after_tool_call(context):
        """Capture tool call end with result."""
        try:
            from ...client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return

            crew = getattr(context, "crew", None)
            handler = getattr(crew, "_aigie_handler", None) if crew else None
            if handler and hasattr(handler, "handle_tool_end"):
                import asyncio

                tool_name = getattr(context, "tool_name", "unknown")
                tool_result = getattr(context, "tool_result", None)
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(
                        handler.handle_tool_end(
                            tool_name=tool_name,
                            result=str(tool_result)[:1000] if tool_result else None,
                        )
                    )
                except RuntimeError:
                    pass

            return
        except Exception as e:
            logger.debug(f"[AIGIE] Error in after_tool_call hook: {e}")
            return

    try:
        register_before_llm_call_hook(_aigie_before_llm_call)
        register_after_llm_call_hook(_aigie_after_llm_call)
        register_before_tool_call_hook(_aigie_before_tool_call)
        register_after_tool_call_hook(_aigie_after_tool_call)
        _patched_classes.add("hooks")
        logger.debug("[AIGIE] CrewAI hooks registered for LLM and tool tracing")
    except Exception as e:
        logger.debug(f"[AIGIE] Failed to register CrewAI hooks: {e}")

    return True


def patch_crewai() -> bool:
    """Patch CrewAI classes for auto-instrumentation.

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _register_hooks() and success  # Native hooks first
    success = _patch_crew() and success
    success = _patch_agent() and success
    return _patch_task() and success


def unpatch_crewai() -> None:
    """Remove CrewAI patches (for testing)."""
    global _patched_classes
    _patched_classes.clear()


def is_crewai_patched() -> bool:
    """Check if CrewAI has been patched."""
    return len(_patched_classes) > 0


def _patch_crew() -> bool:
    """Patch Crew.kickoff() and kickoff_async() methods."""
    try:
        from crewai import Crew

        if Crew in _patched_classes:
            return True

        original_kickoff = Crew.kickoff
        original_kickoff_async = getattr(Crew, "kickoff_async", None)
        getattr(Crew, "kickoff_for_each", None)

        @functools.wraps(original_kickoff)
        def traced_kickoff(self, inputs: dict[str, Any] | None = None):
            """Traced version of Crew.kickoff()."""
            import asyncio

            from ...client import get_aigie
            from .handler import CrewAIHandler

            aigie = get_aigie()
            if aigie and aigie._initialized:
                handler = CrewAIHandler(
                    trace_name=f"Crew: {getattr(self, 'name', 'unnamed')}",
                    metadata={"inputs": inputs if isinstance(inputs, dict) else {}},
                )
                handler._aigie = aigie

                # Extract crew info
                agents_info = _extract_agents_info(self)
                tasks_info = _extract_tasks_info(self)
                process_type = getattr(self, "process", "sequential")
                if hasattr(process_type, "value"):
                    process_type = process_type.value

                # Run async handler in sync context
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Create task for running event loop
                        import concurrent.futures

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                handler.handle_crew_start(
                                    crew_name=getattr(self, "name", "unnamed"),
                                    agents=agents_info,
                                    tasks=tasks_info,
                                    process_type=str(process_type),
                                    verbose=getattr(self, "verbose", False),
                                ),
                            )
                            future.result(timeout=5)
                    else:
                        loop.run_until_complete(
                            handler.handle_crew_start(
                                crew_name=getattr(self, "name", "unnamed"),
                                agents=agents_info,
                                tasks=tasks_info,
                                process_type=str(process_type),
                                verbose=getattr(self, "verbose", False),
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting crew trace: {e}")

                # Store handler on crew for access in callbacks
                self._aigie_handler = handler

                try:
                    result = original_kickoff(self, inputs)

                    # Handle completion
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_crew_end(success=True, result=result),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_crew_end(success=True, result=result)
                            )
                    except Exception as e:
                        logger.debug(f"Error ending crew trace: {e}")

                    return result

                except Exception as e:
                    # Handle error
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_crew_end(success=False, error=str(e)),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_crew_end(success=False, error=str(e))
                            )
                    except Exception:
                        pass
                    raise

            return original_kickoff(self, inputs)

        if original_kickoff_async:

            @functools.wraps(original_kickoff_async)
            async def traced_kickoff_async(self, inputs: dict[str, Any] | None = None):
                """Traced version of Crew.kickoff_async()."""
                from ...client import get_aigie
                from .handler import CrewAIHandler

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    handler = CrewAIHandler(
                        trace_name=f"Crew: {getattr(self, 'name', 'unnamed')}",
                        metadata={"inputs": inputs if isinstance(inputs, dict) else {}},
                    )
                    handler._aigie = aigie

                    # Extract crew info
                    agents_info = _extract_agents_info(self)
                    tasks_info = _extract_tasks_info(self)
                    process_type = getattr(self, "process", "sequential")
                    if hasattr(process_type, "value"):
                        process_type = process_type.value

                    await handler.handle_crew_start(
                        crew_name=getattr(self, "name", "unnamed"),
                        agents=agents_info,
                        tasks=tasks_info,
                        process_type=str(process_type),
                        verbose=getattr(self, "verbose", False),
                    )

                    self._aigie_handler = handler

                    try:
                        result = await original_kickoff_async(self, inputs)
                        await handler.handle_crew_end(success=True, result=result)
                        return result
                    except Exception as e:
                        await handler.handle_crew_end(success=False, error=str(e))
                        raise

                return await original_kickoff_async(self, inputs)

            Crew.kickoff_async = traced_kickoff_async

        Crew.kickoff = traced_kickoff
        _patched_classes.add(Crew)

        logger.debug("Patched Crew for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("CrewAI not installed, skipping Crew patch")
        return True  # Not an error if CrewAI not installed
    except Exception as e:
        logger.warning(f"Failed to patch Crew: {e}")
        return False


def _patch_agent() -> bool:
    """Patch Agent to capture step callbacks."""
    try:
        from crewai import Agent

        if Agent in _patched_classes:
            return True

        original_init = Agent.__init__

        @functools.wraps(original_init)
        def traced_init(self, *args, **kwargs):
            """Traced version of Agent.__init__."""
            # Inject step callback
            original_step_callback = kwargs.get("step_callback")

            def aigie_step_callback(step_output):
                """Callback to trace agent steps."""
                try:
                    crew = getattr(self, "_crew", None)
                    if crew and hasattr(crew, "_aigie_handler"):
                        handler = crew._aigie_handler
                        step_id = str(uuid.uuid4())

                        # Extract step info
                        thought = getattr(step_output, "thought", None) or getattr(
                            step_output, "text", None
                        )
                        action = getattr(step_output, "tool", None)
                        action_input = getattr(step_output, "tool_input", None)
                        observation = getattr(step_output, "result", None) or getattr(
                            step_output, "observation", None
                        )

                        # Run async in sync context
                        import asyncio

                        try:
                            loop = asyncio.get_event_loop()
                            if not loop.is_running():
                                loop.run_until_complete(
                                    handler.handle_agent_step_start(
                                        step_id=step_id,
                                        agent_role=getattr(self, "role", "unknown"),
                                        step_number=handler.total_steps + 1,
                                    )
                                )
                                loop.run_until_complete(
                                    handler.handle_agent_step_end(
                                        step_id=step_id,
                                        thought=str(thought) if thought else None,
                                        action=str(action) if action else None,
                                        action_input=action_input,
                                        observation=str(observation) if observation else None,
                                    )
                                )
                        except Exception as e:
                            logger.debug(f"Error in step callback: {e}")

                except Exception as e:
                    logger.debug(f"Error in aigie step callback: {e}")

                # Call original callback if exists
                if original_step_callback:
                    original_step_callback(step_output)

            kwargs["step_callback"] = aigie_step_callback

            return original_init(self, *args, **kwargs)

        Agent.__init__ = traced_init
        _patched_classes.add(Agent)

        logger.debug("Patched Agent for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("CrewAI not installed, skipping Agent patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Agent: {e}")
        return False


def _patch_task() -> bool:
    """Patch Task.execute() to trace task execution."""
    try:
        from crewai import Task

        if Task in _patched_classes:
            return True

        # Check if execute method exists (may vary by version)
        if not hasattr(Task, "execute"):
            logger.debug("Task.execute not found, skipping Task patch")
            return True

        original_execute = Task.execute

        @functools.wraps(original_execute)
        def traced_execute(self, *args, **kwargs):
            """Traced version of Task.execute()."""
            import asyncio

            from ...client import get_aigie

            aigie = get_aigie()

            # Try to get handler from crew context
            handler = None
            context = kwargs.get("context")
            if context and hasattr(context, "_aigie_handler"):
                handler = context._aigie_handler

            if aigie and aigie._initialized and handler:
                task_id = str(uuid.uuid4())
                agent = getattr(self, "agent", None)
                agent_role = getattr(agent, "role", "unknown") if agent else "unknown"

                try:
                    loop = asyncio.get_event_loop()
                    if not loop.is_running():
                        loop.run_until_complete(
                            handler.handle_task_start(
                                task_id=task_id,
                                description=getattr(self, "description", "")[:500],
                                agent_role=agent_role,
                                expected_output=getattr(self, "expected_output", None),
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting task trace: {e}")

                try:
                    result = original_execute(self, *args, **kwargs)

                    try:
                        loop = asyncio.get_event_loop()
                        if not loop.is_running():
                            output = str(result) if result else None
                            loop.run_until_complete(
                                handler.handle_task_end(task_id=task_id, output=output)
                            )
                    except Exception as e:
                        logger.debug(f"Error ending task trace: {e}")

                    return result

                except Exception as e:
                    try:
                        loop = asyncio.get_event_loop()
                        if not loop.is_running():
                            loop.run_until_complete(
                                handler.handle_task_error(task_id=task_id, error=str(e))
                            )
                    except Exception:
                        pass
                    raise

            return original_execute(self, *args, **kwargs)

        Task.execute = traced_execute
        _patched_classes.add(Task)

        logger.debug("Patched Task for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("CrewAI not installed, skipping Task patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Task: {e}")
        return False


def _extract_agents_info(crew) -> list:
    """Extract agent information from a crew."""
    agents_info = []
    agents = getattr(crew, "agents", []) or []
    for agent in agents:
        agent_info = {
            "role": getattr(agent, "role", "unknown"),
            "goal": getattr(agent, "goal", "")[:200] if getattr(agent, "goal", None) else None,
            "backstory": getattr(agent, "backstory", "")[:200]
            if getattr(agent, "backstory", None)
            else None,
            "allow_delegation": getattr(agent, "allow_delegation", False),
        }

        # Extract tools
        tools = getattr(agent, "tools", []) or []
        if tools:
            agent_info["tools"] = [getattr(t, "name", str(t)[:50]) for t in tools[:10]]

        # Extract LLM info
        llm = getattr(agent, "llm", None)
        if llm:
            agent_info["llm"] = getattr(llm, "model_name", None) or getattr(llm, "model", "unknown")

        agents_info.append(agent_info)

    return agents_info


def _extract_tasks_info(crew) -> list:
    """Extract task information from a crew."""
    tasks_info = []
    tasks = getattr(crew, "tasks", []) or []
    for task in tasks:
        task_info = {
            "description": getattr(task, "description", "")[:200]
            if getattr(task, "description", None)
            else None,
            "expected_output": getattr(task, "expected_output", "")[:200]
            if getattr(task, "expected_output", None)
            else None,
        }

        # Get assigned agent
        agent = getattr(task, "agent", None)
        if agent:
            task_info["agent_role"] = getattr(agent, "role", "unknown")

        tasks_info.append(task_info)

    return tasks_info
