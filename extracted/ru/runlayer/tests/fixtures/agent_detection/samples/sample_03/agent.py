"""Minimal LlamaIndex FunctionAgent (framework detection corpus)."""

import asyncio
import os

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI


def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


async def main() -> None:
    llm = OpenAI(model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY", ""))
    agent = FunctionAgent(
        tools=[
            FunctionTool.from_defaults(get_weather),
            FunctionTool.from_defaults(add),
        ],
        llm=llm,
        system_prompt="You are a helpful assistant. Use tools when needed.",
    )
    response = await agent.run("What's the weather in Paris, and what is 21 + 21?")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
