from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Echo")


@mcp.tool()
def echo(message: str) -> str:
    """Echo back the provided message"""
    return f"Echo: {message}"


if __name__ == "__main__":
    mcp.run()
