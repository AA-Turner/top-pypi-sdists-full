import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

from aigie import Aigie


async def run_single_trace():
    """Run a single traced query with proper resource management.

    Creates a fresh Aigie instance for each run, ensuring complete cleanup
    between iterations. This pattern supports millions of runs without
    state corruption or memory leaks.
    """
    # Create fresh instance for this run
    aigie = Aigie(
        aigie_url="https://app.aigie.io/staging/api",
        aigie_token="kytte_lic_enterprise_jKZzsLKJuClFI-1Q9imPMkhFWMhj04Ik",
        log_level="WARNING",  # Silent by default (only errors shown)
    )

    try:
        # Initialize Aigie - all Claude SDK calls are now traced!
        await aigie.initialize()

        options = ClaudeAgentOptions(system_prompt="You are a helpful assistant.", model="haiku")

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt="What is quantum computing?")

            async for msg in client.receive_response():
                if hasattr(msg, "content"):
                    for block in msg.content:
                        if hasattr(block, "text"):
                            print(block.text)
    finally:
        # CRITICAL: Always close to reset global state
        # This prevents _global_aigie corruption that crashes after ~30 runs
        await aigie.close()


async def main():
    """Main entry point - run single or multiple traces."""
    # For single run (testing):
    await run_single_trace()

    # For stress testing millions of runs, use:
    # for i in range(1000000):
    #     await run_single_trace()
    #     if (i + 1) % 100 == 0:
    #         print(f"Completed {i + 1} runs")


if __name__ == "__main__":
    asyncio.run(main())
