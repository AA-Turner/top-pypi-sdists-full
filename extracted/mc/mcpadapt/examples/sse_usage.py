import subprocess
import time
from textwrap import dedent

from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter

echo_server_sse_script = dedent(
    '''
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("Echo Server")

    @mcp.tool()
    def echo_tool(text: str) -> str:
        """Echo the input text"""
        return f"Echo: {text}"

    mcp.run("sse")
    '''
)

if __name__ == "__main__":
    # we run the sse server in a separate process
    process = subprocess.Popen(
        ["python", "-c", echo_server_sse_script],
    )

    # Give the server a moment to start up
    time.sleep(1)

    with MCPAdapt(
        {"url": "http://127.0.0.1:8000/sse"},
        SmolAgentsAdapter(),  # replace with your agent framework's adapter of choice
    ) as tools:
        # now you can use the tools as you would with any other tool
        print(tools)
        print(tools[0]("hello"))
