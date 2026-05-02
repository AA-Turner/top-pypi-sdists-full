from langgraph.graph.state import RunnableConfig
from langgraph.prebuilt import create_react_agent

from univer_use.model import load_chat_model
from univer_use.prompts.template import get_rendered_template
from univer_use.tools import write_todos, pipeline
from univer_use.state import SpreadsheetState
from univer_use.tools import _load_univer_tools
from univer_use.artifact_aware_tool import ArtifactAwareToolNode

async def spreadsheet_agent(
    state: SpreadsheetState, config: RunnableConfig
):

    conversation_id = state.get("conversation_id", "default")
    all_univer_tools = await _load_univer_tools(conversation_id)

    built_in_tools = [
        write_todos,
        pipeline,
    ]

    exclude_univer_tools = []

    univer_tools = [tool for tool in all_univer_tools if tool.name not in exclude_univer_tools]

    model = load_chat_model("anthropic/claude-sonnet-4")

    all_agent_tools = [
        *built_in_tools,
        *univer_tools,
    ]

    # Turn the list of tools into a ToolNode
    tool_node = ArtifactAwareToolNode(all_agent_tools)

    spreadsheet_system_prompt = await get_rendered_template("spreadsheet_act_sysetm_prompt")

    agent = create_react_agent(
        name="spreadsheet_act",
        model=model,
        tools=tool_node,
        prompt=spreadsheet_system_prompt,
        state_schema=SpreadsheetState,
    )

    config["recursion_limit"] = 100  # Higher limit for complex app building tasks

    resp = await agent.ainvoke(state, config)

    return resp