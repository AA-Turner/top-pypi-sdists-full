"""Minimal LangChain tool-using agent (framework detection corpus)."""

import os

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY", ""))
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Use tools when needed."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    tools = [get_weather, add]
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    result = executor.invoke(
        {"input": "What's the weather in Paris, and what is 21 + 21?"}
    )
    print(result["output"])


if __name__ == "__main__":
    main()
