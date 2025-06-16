"""An example of using the LangChain adapter to adapt MCP tools to LangChain tools.

This example uses the PubMed API to search for studies.
"""

import os

# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from mcp import StdioServerParameters

from mcpadapt.core import MCPAdapt
from mcpadapt.langchain_adapter import LangChainAdapter
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("ANTHROPIC_API_KEY"):
    raise ValueError(
        "ANTHROPIC_API_KEY is not set create a .env file at the root of the project with ANTHROPIC_API_KEY=<your-api-key>"
    )


def main():
    """Fully synchronous version example. Note that async is preferred (just below).
    As it doesnt rely on the hack with a separate thread running the MCP server.
    """
    with MCPAdapt(
        StdioServerParameters(
            command="uvx",
            args=["--quiet", "pubmedmcp@0.1.3"],
            env={"UV_PYTHON": "3.12", **os.environ},
        ),
        LangChainAdapter(),
    ) as tools:
        # Create the agent
        memory = MemorySaver()

        model = ChatAnthropic(
            model_name="claude-3-5-sonnet-20241022", max_tokens_to_sample=8192
        )
        agent_executor = create_react_agent(model, tools, checkpointer=memory)

        # Use the agent
        config = {"configurable": {"thread_id": "abc123"}}
        for chunk in agent_executor.stream(
            {
                "messages": [
                    HumanMessage(
                        content="Find relevant studies on alcohol hangover and treatment."
                    )
                ]
            },
            config,
        ):
            print(chunk)
            print("----")

        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content="whats the weather where I live?")]},
            config,
        ):
            print(chunk)
            print("----")


async def async_main():
    """Fully asynchronous version example."""
    async with MCPAdapt(
        StdioServerParameters(
            command="uvx",
            args=["--quiet", "pubmedmcp@0.1.3"],
            env={"UV_PYTHON": "3.12", **os.environ},
        ),
        LangChainAdapter(),
    ) as tools:
        # Create the agent
        memory = MemorySaver()

        model = ChatAnthropic(
            model_name="claude-3-5-sonnet-20241022", max_tokens_to_sample=8192
        )
        agent_executor = create_react_agent(model, tools, checkpointer=memory)

        # Use the agent
        config = {"configurable": {"thread_id": "abc123"}}
        async for event in agent_executor.astream(
            {
                "messages": [
                    HumanMessage(
                        content="Find relevant studies on alcohol hangover and treatment."
                    )
                ]
            },
            config,
        ):
            print(event)
            print("----")

        async for event in agent_executor.astream(
            {"messages": [HumanMessage(content="whats the weather where I live?")]},
            config,
        ):
            print(event)
            print("----")


if __name__ == "__main__":
    import asyncio

    # run the sync version
    # main()

    # run the async version
    asyncio.run(async_main())
