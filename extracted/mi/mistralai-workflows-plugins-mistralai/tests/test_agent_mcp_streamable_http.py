"""Integration test: a mistralai Agent reaching a local MCP over Streamable HTTP.

Proves that an ``Agent`` configured with ``mcp_clients=[MCPStreamableHTTPConfig(...)]``
and run through ``RemoteSession`` (the way a workflow does) actually gains access
to the MCP's tools and calls one. The ``hello_mcp`` fixture (conftest) spawns a
real local FastMCP server; the Mistral Agents API traffic is recorded via VCR
while the localhost MCP calls run live (``ignore_localhost``). The tool returns a
distinctive, fixed reply, so a passing assertion cannot be a hallucinated
greeting: the marker only exists inside the tool result.

Record the cassette with a live key:
    VCR_RECORD_MODE=all MISTRAL_API_KEY=... uv run pytest \
        tests/test_agent_mcp_streamable_http.py
It then replays offline in CI. Skips if FastMCP is unavailable.
"""

import pytest

pytest.importorskip("mcp.server.fastmcp", reason="FastMCP (mcp server extra) not installed")

from conftest import HelloMcp  # noqa: E402
from mistralai.client import models as mistralai_models  # noqa: E402

from mistralai.workflows.plugins.mistralai import Agent, MCPStreamableHTTPConfig  # noqa: E402
from mistralai.workflows.plugins.mistralai.runner import Runner  # noqa: E402
from mistralai.workflows.plugins.mistralai.session import RemoteSession  # noqa: E402


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_agent_calls_a_streamable_http_mcp_tool(hello_mcp: HelloMcp) -> None:
    """An agent with an MCP client lists + calls the tool and surfaces its reply."""
    agent = Agent(
        model="mistral-medium-latest",
        name="hello-mcp-agent",
        instructions=(
            "You have a tool named `hello`. When asked to greet, call the `hello` "
            "tool and reply with exactly what it returns, verbatim."
        ),
        mcp_clients=[MCPStreamableHTTPConfig(url=hello_mcp.url, name="hello")],
    )

    outputs = await Runner.run(
        agent=agent,
        inputs="Greet me using your tool.",
        session=RemoteSession(raise_on_tool_fail=False),
        max_turns=4,
    )

    text = "\n".join(o.text for o in outputs if isinstance(o, mistralai_models.TextChunk))
    # "mcp-live-ok" only exists inside the tool's reply, so its presence proves the
    # agent actually reached the MCP and called the tool (not a hallucinated hello).
    assert "mcp-live-ok" in text
