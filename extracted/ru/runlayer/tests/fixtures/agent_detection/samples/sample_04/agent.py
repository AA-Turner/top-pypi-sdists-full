"""Minimal CrewAI agent with tools (framework detection corpus)."""

from crewai import Agent, Crew, Task
from crewai.tools import tool


@tool("get_weather")
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


@tool("add")
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    assistant = Agent(
        role="Assistant",
        goal="Help the user, using tools when needed.",
        backstory="You are a helpful assistant. Use tools when needed.",
        tools=[get_weather, add],
        verbose=True,
    )
    task = Task(
        description="What's the weather in Paris, and what is 21 + 21?",
        expected_output="A helpful answer that uses the tools.",
        agent=assistant,
    )
    crew = Crew(agents=[assistant], tasks=[task])
    result = crew.kickoff()
    print(result)


if __name__ == "__main__":
    main()
