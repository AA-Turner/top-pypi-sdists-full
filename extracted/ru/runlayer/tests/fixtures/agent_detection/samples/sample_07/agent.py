"""Minimal OpenAI Agents SDK agent (framework detection corpus)."""

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


@function_tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Use tools when needed.",
        tools=[get_weather, add],
    )
    result = Runner.run_sync(agent, "What's the weather in Paris, and what is 21 + 21?")
    print(result.final_output)


if __name__ == "__main__":
    main()
