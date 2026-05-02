from typing import NotRequired, Literal, TypedDict
from langgraph.prebuilt.chat_agent_executor import AgentState

class Todo(TypedDict):
    """Todo to track."""

    content: str
    status: Literal["pending", "in_progress", "completed"]

class SpreadsheetState(AgentState):
    conversation_id: str
    todos: NotRequired[list[Todo]]
