# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel
from .tool_source import ToolSource
from .tool_metadata import ToolMetadata

__all__ = ["Tool"]


class Tool(BaseModel):
    source: ToolSource

    tool: ToolMetadata
    """
    Tool metadata follows the
    [MCP Tool definition](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#tool)
    and the
    [WebMCP RegisteredTool definition](https://webmachinelearning.github.io/webmcp/#dictdef-registeredtool).
    outputSchema is optional for page and custom tools.
    """

    tool_ref: str
    """Opaque reference for invoking this exact live registration.

    It becomes invalid when its document or browser process is replaced.
    """
