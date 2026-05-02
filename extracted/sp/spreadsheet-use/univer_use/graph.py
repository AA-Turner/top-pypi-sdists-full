
from langgraph.graph import StateGraph, START, END

from univer_use.spreadsheet_act import spreadsheet_agent
from univer_use.state import SpreadsheetState

async def build_graph():
    builder = StateGraph(SpreadsheetState)

    builder.add_node("spreadsheet_act", spreadsheet_agent)
    builder.add_edge(START, "spreadsheet_act")
    builder.add_edge("spreadsheet_act", END)

    return builder.compile()