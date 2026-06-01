import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

from aigie import Aigie

# Initialize Aigie with verbose logging for debugging
# Set log_level="INFO" to see what's happening internally
aigie = Aigie(
    aigie_url="https://app.aigie.io/staging/api",
    aigie_token="kytte_lic_enterprise_jKZzsLKJuClFI-1Q9imPMkhFWMhj04Ik",
    log_level="INFO",  # Show INFO logs for debugging/troubleshooting
)


async def main():
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

    await aigie.close()


asyncio.run(main())
