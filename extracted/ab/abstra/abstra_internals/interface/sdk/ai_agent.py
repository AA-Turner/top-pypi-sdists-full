from typing import Any, Callable, Dict, List, Optional, Union

from abstra_internals.agents.tools.base import AgentTools
from abstra_internals.contracts_generated import (
    CloudApiCliAgentsPostRequestBodyStartToolsItem,
)
from abstra_internals.controllers.sdk.sdk_ai import Prompt
from abstra_internals.controllers.sdk.sdk_context import SDKContextStore
from abstra_internals.interface.sdk.ai import to_list
from abstra_internals.utils.json_schema import get_function_json_schema


def _callable_to_tool_item(
    func: Callable,
) -> CloudApiCliAgentsPostRequestBodyStartToolsItem:
    return CloudApiCliAgentsPostRequestBodyStartToolsItem(
        function_name=func.__name__,
        description=func.__doc__.strip() if func.__doc__ else f"Tool: {func.__name__}",
        parameters=get_function_json_schema(func),
    )


def _collect_tools(
    tools: List[Any],
) -> tuple[
    List[CloudApiCliAgentsPostRequestBodyStartToolsItem],
    Dict[str, Callable],
]:
    tool_items: List[CloudApiCliAgentsPostRequestBodyStartToolsItem] = []
    tool_callables: Dict[str, Callable] = {}
    seen: set = set()

    for tool in tools:
        if isinstance(tool, AgentTools):
            for method_name in tool.__tools__():
                method = getattr(tool, method_name)
                item = _callable_to_tool_item(method)
                if item.function_name in seen:
                    raise ValueError(f"Duplicate tool name: '{item.function_name}'.")
                seen.add(item.function_name)
                tool_items.append(item)
                tool_callables[item.function_name] = method
        elif callable(tool):
            item = _callable_to_tool_item(tool)
            if item.function_name in seen:
                raise ValueError(f"Duplicate tool name: '{item.function_name}'.")
            seen.add(item.function_name)
            tool_items.append(item)
            tool_callables[item.function_name] = tool
        else:
            raise TypeError(
                f"Invalid tool: {type(tool).__name__}. "
                f"Must have a __tools__() method or be callable."
            )

    return tool_items, tool_callables


def run_agent(
    prompt: Union[Prompt, List[Prompt]],
    tools: Optional[List[Union[Callable, AgentTools]]] = None,
    max_steps: int = 30,
) -> Dict[str, Any]:
    """
    Run an autonomous AI agent loop. The agent reasons about the prompt, decides which tools to call, executes them, and continues until it produces a final answer or hits `max_steps`.

    Use this from any regular Python stage (Tasklet, Job, Hook, or Form logic) when the task requires multi-step reasoning, tool use, or autonomous decision-making. For single-shot completions, use `prompt` instead.

    Args:
        prompt (str): Instruction(s) for the agent. A single string, a list of strings, or a list mixing strings, files (Path), and images. Files and images are forwarded to the LLM as multimodal input.
        tools (Optional): Tools the agent may call. Each item is either a plain Python function (its name, type hints and docstring become the tool spec) or an `AgentTools` subclass instance (e.g. `BrowserTools`, `TablesTools`, `FilesTools`, `ConnectorsTools`). Defaults to None (no tools).
        max_steps (int): Maximum number of reasoning/tool-use iterations before the agent is forced to stop. Defaults to 30.

    Returns:
        The agent's final response as a dict with the agent output payload.
    """
    resolved_tools = tools if tools is not None else []
    tool_items, tool_callables = _collect_tools(resolved_tools)
    prompt_list = to_list(prompt)
    context = SDKContextStore.get_by_thread()

    response = context.ai_sdk.run_agent(
        prompts=prompt_list,
        tool_callables=tool_callables if tool_callables else None,
        tool_items=tool_items if tool_items else None,
        max_steps=max_steps,
    )

    return response.get("data", response)
