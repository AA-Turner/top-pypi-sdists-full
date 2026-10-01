"""The MCP server's version and user agent; it ships in ``dlthub-client`` beside the SDK."""

# Current package
from dlthub_sdk.version import __version__

USER_AGENT = f"dlthub-mcp/{__version__}"
