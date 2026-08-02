"""
xpander_sdk.decorators.on_task

This module provides the `@on_task` decorator, which allows developers to define
task execution functions that integrate with xpander.ai's event system.

The decorator ensures that the registered function:
- Accepts a single parameter named `task` of type `Task`
- Returns the modified `Task` after processing (regular handler)
- Or yields `TaskUpdateEvent` instances (streaming handler)
- The handler type is auto-detected: no extra parameters needed

Execution Notes:
- The task executor automatically handles status transitions (e.g., success or failure).
- You must set `task.result = ...` to assign your output (regular handlers).
- If an exception is raised in the function, the task will be marked as failed.
- You do not need to manually manage status or lifecycle hooks.

HTTP Server:
- A mini HTTP server is always started on port 59321 alongside the SSE listener.
- POST /invoke accepts a Task JSON body (authenticated via x-api-key header).
- For regular handlers: returns the Task as JSON.
- For streaming handlers: streams TaskUpdateEvent SSE lines.

Example usage:
--------------
Regular handler (returns Task):
>>> @on_task
... async def handle_agent_task(task: Task):
...     backend = Backend(task.configuration)
...     agno_args = await backend.aget_args(
...         agent_id=task.agent_id,
...         agent_version=task.agent_version,
...         task=task
...     )
...     agno_agent = Agent(**agno_args)
...     result = await agno_agent.arun(message=task.to_message())
...     task.result = result.content
...     return task

Streaming handler (yields TaskUpdateEvent):
>>> @on_task
... async def handle_streaming_task(task: Task):
...     from xpander_sdk import TaskUpdateEvent, TaskUpdateEventType
...     async for chunk in some_streaming_source(task):
...         yield TaskUpdateEvent(
...             type=TaskUpdateEventType.Chunk,
...             task_id=task.id,
...             organization_id=task.organization_id,
...             time=datetime.now(timezone.utc),
...             data=chunk,
...         )
"""

import asyncio
import argparse
import json
import sys
from functools import wraps
from inspect import isasyncgenfunction, iscoroutinefunction, signature
from typing import Optional, Callable

from loguru import logger

from xpander_sdk.models.configuration import Configuration
from xpander_sdk.models.events import TaskUpdateEventType
from xpander_sdk.modules.events.events_module import Events
from xpander_sdk.modules.tasks.models.task import LocalTaskTest, AgentExecutionInput
from xpander_sdk.models.shared import OutputFormat
from xpander_sdk.modules.tasks.sub_modules.task import Task, TaskUpdateEvent


def on_task(
    _func: Optional[Callable] = None,
    *,
    configuration: Optional[Configuration] = None,
    test_task: Optional[LocalTaskTest] = None,
):
    """
    Decorator to register a handler as an event-driven task executor.

    The decorated function will be executed when the task is triggered through
    xpander.ai's event system and/or via the HTTP ``/invoke`` endpoint.

    **Handler types (auto-detected):**

    - **Regular handler** (async/sync function that returns ``Task``):
      Works with both the SSE event listener and ``POST /invoke``.
    - **Streaming handler** (async generator that yields ``TaskUpdateEvent``):
      Works via ``POST /invoke`` only – events are streamed back as SSE lines.

    A mini HTTP server on port 59321 is always started alongside the SSE
    listener (for regular handlers) or on its own (for streaming handlers).

    Args:
        _func (Optional[Callable]):
            The function to decorate (for direct usage like ``@on_task``).
        configuration (Optional[Configuration]):
            An optional configuration object used to initialize the Events module.
        test_task (Optional[LocalTaskTest]):
            Optional simulated task used for local development or testing.

    Raises:
        TypeError: If the decorated function does not accept a ``task`` parameter.
        TypeError: If ``test_task`` is provided but is not a ``LocalTaskTest``.
        TypeError: If the input ``task`` is not an instance of ``Task``.
        TypeError: If the return value is not an instance of ``Task`` (regular handler).
        TypeError: If a yielded value is not a ``TaskUpdateEvent`` (streaming handler).
    """

    def decorator(func: Callable) -> Callable:
        sig = signature(func)

        if "task" not in sig.parameters:
            raise TypeError(f"Function '{func.__name__}' must have a 'task' parameter.")

        is_streaming_handler = isasyncgenfunction(func)

        # ------------------------------------------------------------------ #
        # Build the appropriate wrapper                                       #
        # ------------------------------------------------------------------ #

        if is_streaming_handler:
            # Streaming wrapper – for /invoke (yields TaskUpdateEvent)
            @wraps(func)
            async def streaming_wrapper(*args, **kwargs):
                async for event in func(*args, **kwargs):
                    if not isinstance(event, TaskUpdateEvent):
                        raise TypeError(
                            f"Streaming handler must yield TaskUpdateEvent instances, "
                            f"got {type(event).__name__}"
                        )
                    yield event

            # Adapter for Events.register() – consumes the generator, returns Task
            @wraps(func)
            async def events_adapter(*args, **kwargs):
                task_value = kwargs.get("task") or args[0]
                async for event in func(*args, **kwargs):
                    if isinstance(event, TaskUpdateEvent):
                        if event.type == TaskUpdateEventType.TaskFinished:
                            if isinstance(event.data, Task):
                                if not event.data.configuration:
                                    event.data.configuration = task_value.configuration
                                task_value = event.data
                            elif isinstance(event.data, dict):
                                task_value = Task(
                                    **{
                                        **event.data,
                                        "configuration": task_value.configuration,
                                    }
                                )
                            elif isinstance(event.data, str):
                                task_value.result = event.data
                return task_value

            wrapped = streaming_wrapper
            events_handler = events_adapter
        else:
            # Regular handler – returns Task
            param_names = list(sig.parameters)

            def get_task_from_call(args, kwargs) -> Task:
                if "task" in kwargs:
                    task_value = kwargs["task"]
                else:
                    task_index = param_names.index("task")
                    task_value = args[task_index] if len(args) > task_index else None
                if not isinstance(task_value, Task):
                    raise TypeError(
                        f"'task' must be an instance of Task, got {type(task_value).__name__}"
                    )
                return task_value

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                get_task_from_call(args, kwargs)
                result = await func(*args, **kwargs)
                if not isinstance(result, Task):
                    raise TypeError(
                        f"Function '{func.__name__}' must return an instance of Task, got {type(result).__name__}"
                    )
                return result

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                get_task_from_call(args, kwargs)
                result = func(*args, **kwargs)
                if not isinstance(result, Task):
                    raise TypeError(
                        f"Function '{func.__name__}' must return an instance of Task, got {type(result).__name__}"
                    )
                return result

            wrapped = async_wrapper if iscoroutinefunction(func) else sync_wrapper
            events_handler = wrapped

        # ------------------------------------------------------------------ #
        # Start the /invoke HTTP server in a background daemon thread         #
        # ------------------------------------------------------------------ #
        from xpander_sdk.modules.events.streaming_server import (
            run_streaming_server_in_background,
        )

        run_streaming_server_in_background(
            handler=wrapped,
            configuration=configuration,
            is_streaming_handler=is_streaming_handler,
        )

        # ------------------------------------------------------------------ #
        # Register with Events SSE listener (both handler types)              #
        # ------------------------------------------------------------------ #

        # Initialize effective_test_task with the passed parameter
        effective_test_task = test_task

        if effective_test_task and not isinstance(effective_test_task, LocalTaskTest):
            raise TypeError(
                f"'test_task' must be an instance of LocalTaskTest, got {type(effective_test_task).__name__}"
            )

        # Check for direct invocation with --invoke and --prompt arguments
        if any("--invoke" in arg for arg in sys.argv):
            # Parse command line arguments
            parser = argparse.ArgumentParser(description="Run task handler locally")
            parser.add_argument(
                "--invoke", action="store_true", help="Invoke the task handler directly"
            )
            parser.add_argument(
                "--prompt",
                type=str,
                required="--invoke" in sys.argv,
                help="Input text for the task",
            )
            parser.add_argument(
                "--output_format",
                type=str,
                choices=["json", "markdown", "text"],
                help="Output format (json, markdown, text)",
            )
            parser.add_argument(
                "--output_schema",
                type=str,
                help="JSON schema as a string for output validation",
            )

            # Parse only known args to avoid conflicts with other args that might be present
            args, _ = parser.parse_known_args()

            if args.invoke:
                # Create a LocalTaskTest instance from command line arguments (like existing test_task logic)
                output_format_map = {
                    "json": OutputFormat.Json,
                    "markdown": OutputFormat.Markdown,
                    "text": OutputFormat.Text,
                }

                # Parse output schema if provided
                output_schema = None
                if args.output_schema:
                    try:
                        output_schema = json.loads(args.output_schema)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing output_schema JSON: {e}")
                        sys.exit(1)

                # Create LocalTaskTest (same as existing test_task functionality)
                # Only include output_format and output_schema if explicitly provided
                task_kwargs = {"input": AgentExecutionInput(text=args.prompt)}

                if args.output_format:
                    task_kwargs["output_format"] = output_format_map.get(
                        args.output_format.lower()
                    )

                if output_schema is not None:
                    task_kwargs["output_schema"] = output_schema

                cli_test_task = LocalTaskTest(**task_kwargs)
                # Override effective_test_task with CLI-provided one
                effective_test_task = cli_test_task
                print(f"Running task handler directly with prompt: {args.prompt}")
                if output_schema:
                    print(f"Using output schema: {output_schema}")

        events_module = Events(configuration=configuration)
        events_module.register(on_task=events_handler, test_task=effective_test_task)

        return wrapped

    if _func and callable(_func):
        return decorator(_func)

    return decorator
