"""
A simple example demonstrating how to trace an OpenAI Agent run.

To run this example:
1. Install the necessary packages:
   pip install openai-agents
2. Fill in your SGP `api_key` and `account_id`.
3. Run the script from your terminal
"""
import os
import asyncio

try:
    from agents import Agent, Runner, function_tool, set_trace_processors  # type: ignore
except ImportError as e:
    raise ImportError("Please install the required packages: pip install openai-agents") from e

import scale_gp_beta.lib.tracing as tracing
from scale_gp_beta import SGPClient
from scale_gp_beta.lib.tracing.integrations import OpenAITracingSGPProcessor


@function_tool  # type: ignore
def get_current_weather(city: str) -> str:
    if "san francisco" in city.lower():
        return "The weather in San Francisco is foggy."
    return f"The weather in {city} is sunny."


async def main() -> None:
    weather_agent = Agent(  # type: ignore
        name="Weather Agent",
        instructions="You are a helpful assistant that can provide weather information.",
        model="gpt-4-turbo",
        tools=[get_current_weather],
    )

    result = await Runner.run(weather_agent, "What's the weather like in San Francisco?")  # type: ignore
    print("Final Output:", result.final_output)  # type: ignore


if __name__ == "__main__":
    api_key = "XXX"
    account_id = "XXX"
    os.environ["OPENAI_API_KEY"] = "XXX"

    tracing.init(SGPClient(api_key=api_key, account_id=account_id), disabled=False)

    sgp_processor = OpenAITracingSGPProcessor()
    set_trace_processors([sgp_processor])
    asyncio.run(main())
