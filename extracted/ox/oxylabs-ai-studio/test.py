

from pydantic_ai import Agent
import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

load_dotenv()
import os
print(os.environ["OXYLABS_USERNAME"])
print(os.environ["OXYLABS_PASSWORD"])

async def main():
    server = MCPServerStdio(  
        'uvx', args=['oxylabs-mcp'], env={
            # "OXYLABS_USERNAME": "",
            # "OXYLABS_PASSWORD": "",
            'OXYLABS_AI_STUDIO_API_KEY': os.getenv('OXYLABS_AI_STUDIO_API_KEY_PROD')
        }
    )
    tools = await server.get_tools({})
    print(tools.keys())
    # agent = Agent(  
    #     'gpt-4.1',
    #     toolsets=[server]
    # )
    # prompt = 'find some lasagne recipes online'
    # prompt = f"get content from oxylabs.io and retrieve pricing if its there."
    # async with agent.iter(prompt) as agent_run:
    #             async for node in agent_run:
    #                 print(node)
if __name__ == '__main__':
    asyncio.run(main())

