"""Tests for the webapp server entrypoint."""

import asyncio
import os
from unittest.mock import AsyncMock, Mock

from airbyte_ops_webapp import serve as serve_module


def test_serve_constructs_host_with_installed_fastmcp(monkeypatch) -> None:
    process = Mock(returncode=0)
    monkeypatch.setattr(
        serve_module, "_start_user_server", AsyncMock(return_value=process)
    )
    monkeypatch.setattr(serve_module, "_wait_for_server", AsyncMock(return_value=True))
    monkeypatch.setattr(
        serve_module, "_fetch_app_bridge_bundle", AsyncMock(return_value=("", ""))
    )
    server = Mock(serve=AsyncMock())
    server_factory = Mock(return_value=server)
    monkeypatch.setattr(serve_module.uvicorn, "Server", server_factory)

    asyncio.run(serve_module._serve())

    app = server_factory.call_args.args[0].app
    assert any(route.path == "/oauth/login" for route in app.routes)
    server.serve.assert_awaited_once()


def test_configure_backend_env_defaults_to_stateless(monkeypatch) -> None:
    monkeypatch.delenv(serve_module.STATELESS_HTTP_ENV_VAR, raising=False)

    serve_module._configure_backend_env()

    assert os.environ[serve_module.STATELESS_HTTP_ENV_VAR] == "true"


def test_configure_backend_env_preserves_explicit_false(monkeypatch) -> None:
    monkeypatch.setenv(serve_module.STATELESS_HTTP_ENV_VAR, "false")

    serve_module._configure_backend_env()

    assert os.environ[serve_module.STATELESS_HTTP_ENV_VAR] == "false"
