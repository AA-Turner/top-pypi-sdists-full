"""Minimal PydanticAI agent with tools (framework detection corpus)."""

from pydantic_ai import Agent

agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="You are a helpful assistant. Use tools when needed.",
)


@agent.tool_plain
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's 72F and sunny in {city}."


@agent.tool_plain
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def main() -> None:
    result = agent.run_sync("What's the weather in Paris, and what is 21 + 21?")
    print(result.output)


if __name__ == "__main__":
    main()
