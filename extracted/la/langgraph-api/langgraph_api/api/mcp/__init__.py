"""Implement MCP endpoint for Streamable HTTP protocol.

The current version of the RFC can be found here:

https://github.com/modelcontextprotocol/specification/blob/0f4924b07447073cbe1e29fbe64e42d379b52b04/docs/specification/draft/basic/transports.md#streamable-http

Tools specification:

https://github.com/modelcontextprotocol/specification/blob/0f4924b07447073cbe1e29fbe64e42d379b52b04/docs/specification/draft/server/tools.md

Message format:

https://github.com/modelcontextprotocol/specification/blob/0f4924b07447073cbe1e29fbe64e42d379b52b04/docs/specification/draft/basic/messages.md

Error handling with tools:

https://github.com/modelcontextprotocol/specification/blob/0f4924b07447073cbe1e29fbe64e42d379b52b04/docs/specification/draft/server/tools.md#error-handling

Streamable HTTP is a protocol that allows for the use of HTTP as transport.

The protocol supports both stateless and stateful interactions, and allows
the server to respond via either Application/JSON or text/event-stream.

LangGraph's implementation is currently stateless and only uses Application/JSON.

1. Adding stateful sessions: A stateful session would in theory allow agents used
as tools to remember past interactions. We likely do not want to map a session
to a thread ID as a single session may involve more than one tool call.
We would need to map a session to a collection of threads.

2. text/event-stream (SSE): Should be simple to add we'd want to make sure
we know what information we want to stream; e.g., progress notifications or
custom notifications.

In addition, the server could support resumability by allowing clients to specify
a Last-Event-ID in the request headers.
"""

from langgraph_api.api.mcp._routes import mcp_routes

__all__ = ["mcp_routes"]
