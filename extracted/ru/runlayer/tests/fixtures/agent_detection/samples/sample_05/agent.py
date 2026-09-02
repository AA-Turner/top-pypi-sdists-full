"""Minimal Microsoft AutoGen AgentChat assistant (framework detection corpus)."""

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY", "")
    )
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[get_weather, add],
        system_message="You are a helpful assistant. Use tools when needed.",
    )
    result = await agent.run(task="What's the weather in Paris, and what is 21 + 21?")
    print(result.messages[-1].content)
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
