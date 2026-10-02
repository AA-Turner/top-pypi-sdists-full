"""The Streamable HTTP import is guarded so the plugin still loads on mistralai<2.8.0.

`mistralai.extra.mcp.streamable_http` only exists on mistralai>=2.8.0, but the
plugin keeps a permissive floor (>=2.0.0). The import is wrapped in try/except so
stdio/SSE users on an older mistralai can still import this module (and the whole
plugin package); a clear ImportError is raised only when a Streamable HTTP config
is actually opened.
"""

import pytest

from mistralai.workflows.plugins.mistralai import mcp
from mistralai.workflows.plugins.mistralai.mcp import MCPStreamableHTTPConfig, collect_tools_streamable_http


@pytest.mark.asyncio
async def test_streamable_http_raises_clear_error_when_client_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    # Simulate mistralai<2.8.0: the optional import failed, so the client symbols are None.
    monkeypatch.setattr(mcp, "MCPClientStreamableHTTP", None)
    monkeypatch.setattr(mcp, "StreamableHTTPServerParams", None)
    monkeypatch.setattr(mcp, "_STREAMABLE_HTTP_IMPORT_ERROR", ImportError("no streamable_http"))

    config = MCPStreamableHTTPConfig(url="http://mcp.test", name="test")
    with pytest.raises(ImportError, match="requires mistralai>=2.8.0"):
        await collect_tools_streamable_http(config)
