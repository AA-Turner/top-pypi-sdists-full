from typing import Annotated, Any
from pydantic import BaseModel, Field
import os
import json
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool as create_tool, InjectedToolCallId
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.types import Command

from univer_use.artifact_aware_tool import ArtifactAwareToolNode
from univer_use.prompts.template import get_rendered_template
from univer_use.model import load_chat_model
from univer_use.state import Todo
from univer_use.prompts.prompts import (
    WRITE_TODOS_TOOL_DESCRIPTION,
    INSPECT_TOOL_DESCRIPTION,
    PIPELINE_DESCRIPTION,
)


def univer_mcp_config(univer_session_id: str, univer_api_key: str = ""):

    return {
        "transport": "streamable_http",
        "url": f"https://mcp.univer.ai/mcp/?univer_session_id={univer_session_id}",
        "headers": {
            "Authorization": f"Bearer {univer_api_key or os.getenv('UNIVER_API_KEY')}"
        },
    }


async def _load_univer_tools(
    univer_session_id: str
) -> list[BaseTool]:
    """Return provided tools, or attempt to load MCP tools for Univer.

    Tries to import fastmcp's LangChain client loader if tools are not supplied.
    If unavailable, raises a clear error directing the caller to pass tools in.
    """

    connection = univer_mcp_config(univer_session_id)
    maybe_tools = load_mcp_tools(session=None, connection=connection)  # type: ignore
    # Support async or sync loader transparently
    if hasattr(maybe_tools, "__await__"):
        return await maybe_tools  # type: ignore
    return maybe_tools  # type: ignore


# deprecated
@create_tool(description=INSPECT_TOOL_DESCRIPTION)
async def inspect_tool(
    requirement: Annotated[str, "The requirement to inspect"],
    conversation_id: Annotated[str, InjectedState("conversation_id")],
    config: RunnableConfig,
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    tools = await _load_univer_tools(conversation_id)

    inspect_tool_names = ["get_activity_status", "get_lint_errors", "preview_formula_distribution", "get_sheets", "scroll_and_screenshot"]
    inspect_tools = [tool for tool in tools if tool.name in inspect_tool_names]

    tool_node = ArtifactAwareToolNode(inspect_tools)
    model = load_chat_model("anthropic/claude-sonnet-4")

    inspect_system_prompt = await get_rendered_template("inspect_agent_system_prompt")

    inspect_agent = create_react_agent(
        name="inspect_spreadsheet",
        model=model,
        tools=tool_node,
        prompt=inspect_system_prompt,
    )

    result = await inspect_agent.ainvoke({"requirement": requirement}, config)

    content = result.content

    return Command(
        update={
            "messages": [ToolMessage(content=content, tool_call_id=tool_call_id)]
        }
    )


@create_tool(description=WRITE_TODOS_TOOL_DESCRIPTION)
def write_todos(
    todos: list[Todo], tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(f"Updated todo list to {todos}", tool_call_id=tool_call_id)
            ],
        }
    )


class SingleToolCall(BaseModel):
    tool_name: str = Field(description="The name of the tool to execute")
    args: dict[str, Any] = Field(description="The arguments to the tool")


@create_tool(description=PIPELINE_DESCRIPTION)
async def pipeline(
    tool_calls: list[SingleToolCall],
    conversation_id: Annotated[str, InjectedState("conversation_id")],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    mcp_conn = univer_mcp_config(conversation_id)
    tools = await load_mcp_tools(session=None, connection=mcp_conn)  # type: ignore
    tools_by_name = {}
    for tool in tools:
        if not isinstance(tool, BaseTool):
            tool = create_tool(tool)
        tools_by_name[tool.name] = tool

    response = []
    forbidden_tools = ["pipeline", "write_todos", "get_activity_status", "scroll_and_screenshot", "get_range_data", "preview_formula_distribution"]
    for i, tool_call in enumerate(tool_calls):
        tool_name = tool_call.tool_name
        if tool_name not in tools_by_name:
            result = f"ERROR: Tool {tool_name} not found"
        elif tool_name in forbidden_tools:
            result = f"ERROR: Tool {tool_name} is not allowed to be used in pipeline"
        else:
            try:
                tool = tools_by_name[tool_name]
                result = await tool.ainvoke(tool_call.args)
                response.append(
                    {
                        "tool_name": f"{i}_{tool_name}",
                        "result": result,
                    }
                )
            except Exception as e:
                result = f"ERROR: {e}"

        response.append(
            {
                "tool_name": f"{i}_{tool_name}",
                "result": result,
            }
        )

    return Command(
        update={
            "messages": [
                ToolMessage(
                    f"Executed pipeline of tools.\n{json.dumps(response, indent=2)}",
                    tool_call_id=tool_call_id,
                )
            ],
        }
    )