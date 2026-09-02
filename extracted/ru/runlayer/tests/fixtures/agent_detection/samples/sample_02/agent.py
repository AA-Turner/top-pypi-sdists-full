"""Minimal LangGraph prebuilt ReAct agent (framework detection corpus)."""

import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    model = ChatOpenAI(model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY", ""))
    agent = create_react_agent(
        model,
        tools=[get_weather, add],
        prompt="You are a helpful assistant. Use tools when needed.",
    )
    result = agent.invoke(
        {"messages": [("user", "What's the weather in Paris, and what is 21 + 21?")]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
