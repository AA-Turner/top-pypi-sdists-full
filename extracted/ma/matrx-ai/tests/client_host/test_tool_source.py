"""Tool-source seam: registry loads through the host source, never the ORM.

Covers:
* an explicit ``configure(tool_source=...)`` seam feeding ``load_from_database``
* the derived ``ServerToolSource`` (server_url + source_app [+ get_jwt])
* seam validation (``ClientHostConfigError`` on a bad tool_source)
* the sync loader path with a source configured
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


class StaticToolSource:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.calls = 0

    async def list_tools(self) -> list[dict[str, Any]]:
        self.calls += 1
        return self.rows


def _row(name: str, **overrides: Any) -> dict[str, Any]:
    row = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": f"{name} description",
        "source_kind": "native",
        "parameters": {"type": "object", "properties": {}},
        "is_active": True,
    }
    row.update(overrides)
    return row


@pytest.fixture
def fresh_registry():
    from matrx_ai.tools.registry import ToolRegistry

    return ToolRegistry()  # NOT the singleton — no global pollution


@pytest.mark.asyncio
async def test_explicit_tool_source_wins_over_orm(fresh_registry):
    source = StaticToolSource([_row("src_tool_a"), _row("src_tool_b")])
    configure_ext(tool_source=source)

    count = await fresh_registry.load_from_database()

    assert source.calls == 1
    assert count == 2
    assert fresh_registry.get("src_tool_a") is not None
    assert fresh_registry.get("src_tool_b") is not None
    assert fresh_registry.loaded


@pytest.mark.asyncio
async def test_tool_source_fetch_failure_degrades_to_zero(fresh_registry):
    class ExplodingSource:
        async def list_tools(self):
            raise RuntimeError("network down")

    configure_ext(tool_source=ExplodingSource())
    count = await fresh_registry.load_from_database()
    assert count == 0
    assert fresh_registry.loaded  # loaded flag still set; registry operational


def test_sync_loader_uses_source_outside_event_loop(fresh_registry):
    source = StaticToolSource([_row("sync_src_tool")])
    configure_ext(tool_source=source)
    count = fresh_registry.load_from_database_sync()
    assert count == 1
    assert fresh_registry.get("sync_src_tool") is not None


def test_derived_server_source_from_server_url_and_source_app():
    from matrx_ai.tools.tool_source import ServerToolSource, get_tool_source

    configure_ext(server_url="https://server.example.com/", source_app="matrx_local")
    source = get_tool_source()
    assert isinstance(source, ServerToolSource)
    assert source.url == "https://server.example.com/ai-tools/app/matrx_local/all"


def test_no_source_when_only_server_url_set():
    from matrx_ai.tools.tool_source import get_tool_source

    configure_ext(server_url="https://server.example.com")
    assert get_tool_source() is None


def test_explicit_source_beats_derived():
    from matrx_ai.tools.tool_source import get_tool_source

    explicit = StaticToolSource([])
    configure_ext(
        tool_source=explicit,
        server_url="https://server.example.com",
        source_app="matrx_local",
    )
    assert get_tool_source() is explicit


def test_server_source_sends_jwt_header():
    from matrx_ai.tools.tool_source import ServerToolSource

    source = ServerToolSource(
        "https://server.example.com", "matrx_local", get_jwt=lambda: "jwt-token-123"
    )
    assert source._headers()["Authorization"] == "Bearer jwt-token-123"

    anon = ServerToolSource("https://server.example.com", "matrx_local")
    assert "Authorization" not in anon._headers()

    # A raising get_jwt degrades to anonymous — never kills the fetch.
    def _boom() -> str:
        raise RuntimeError("token cache empty")

    degraded = ServerToolSource("https://server.example.com", "matrx_local", get_jwt=_boom)
    assert "Authorization" not in degraded._headers()


@pytest.mark.asyncio
async def test_server_source_parses_tools_payload(monkeypatch):
    import httpx

    from matrx_ai.tools.tool_source import ServerToolSource

    rows = [_row("remote_tool")]

    class FakeResponse:
        status_code = 200
        text = ""

        def json(self):
            return {"tools": rows, "count": 1, "executor_name": "matrx-local"}

    class FakeClient:
        def __init__(self, **kwargs: Any) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc: Any) -> None:
            return None

        async def get(self, url: str, headers: dict[str, str] | None = None):
            assert url.endswith("/ai-tools/app/matrx_local/all")
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeClient)
    source = ServerToolSource("https://server.example.com", "matrx_local")
    fetched = await source.list_tools()
    assert fetched == rows
    assert await source.list_bindings() == [
        {"tool_id": rows[0]["id"], "executor_name": "matrx-local"}
    ]
    assert await source.list_executors() == [
        {
            "name": "matrx-local",
            "parent_executor_name": None,
            "is_active": True,
        }
    ]


@pytest.mark.asyncio
async def test_server_source_raises_on_http_error(monkeypatch):
    import httpx

    from matrx_ai.tools.tool_source import ServerToolSource, ToolSourceFetchError

    class FakeResponse:
        status_code = 503
        text = "unavailable"

        def json(self):
            return {}

    class FakeClient:
        def __init__(self, **kwargs: Any) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc: Any) -> None:
            return None

        async def get(self, url: str, headers: dict[str, str] | None = None):
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeClient)
    source = ServerToolSource("https://server.example.com", "matrx_local")
    with pytest.raises(ToolSourceFetchError):
        await source.list_tools()


def test_validate_rejects_bad_tool_source():
    from matrx_ai.client_host.validate import (
        ClientHostConfigError,
        validate_client_host_config,
    )

    with pytest.raises(ClientHostConfigError, match="tool_source"):
        validate_client_host_config(tool_source=object())

    # A conforming source passes.
    validate_client_host_config(tool_source=StaticToolSource([]))
