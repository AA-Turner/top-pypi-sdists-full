"""Minimal Google ADK agent (framework detection corpus)."""

import asyncio

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types


def get_weather(city: str) -> dict:
    """Get the current weather for a city."""
    return {"status": "success", "report": f"It's 72F and sunny in {city}."}


def add(a: int, b: int) -> dict:
    """Add two integers."""
    return {"status": "success", "result": a + b}


root_agent = Agent(
    name="assistant",
    model="gemini-2.0-flash",
    description="A helpful assistant.",
    instruction="You are a helpful assistant. Use tools when needed.",
    tools=[get_weather, add],
)


async def main() -> None:
    runner = InMemoryRunner(agent=root_agent, app_name="corpus")
    session = await runner.session_service.create_session(
        app_name="corpus", user_id="user"
    )
    content = types.Content(
        role="user",
        parts=[types.Part(text="What's the weather in Paris, and what is 21 + 21?")],
    )
    async for event in runner.run_async(
        user_id="user", session_id=session.id, new_message=content
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
