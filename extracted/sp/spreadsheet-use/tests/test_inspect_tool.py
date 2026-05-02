from langchain_core.messages import AIMessage, BaseMessage, ToolCall
import pytest
from typing import TypedDict
from univer_use.artifact_aware_tool import ArtifactAwareToolNode
from univer_use.tools import inspect_tool
from dotenv import load_dotenv

# TODO: use the correct path

@pytest.mark.asyncio
async def test_inspect_tool():
    """Test that inspect_tool can be imported and has the expected structure."""
    # load_dotenv(dotenv_path="examples/sheet_edit/.env")

    class InspectState(TypedDict):
        messages: list[BaseMessage]
        conversation_id: str

    tool_call = ToolCall(
        name="inspect_tool",
        args={"requirement": "inspect the workbook", "conversation_id": "default"},
        id="123",
        type="tool_call",
    )

    # state = {
    #     "messages": [
    #         AIMessage("", tool_calls=[tool_call])
    #     ],
    #     "conversation_id": "default"
    # }

    # result = await inspect_tool.ainvoke(tool_call)
