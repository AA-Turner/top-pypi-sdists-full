"""configure() client-host validation: all errors reported at once."""

from __future__ import annotations

import pytest

from matrx_ai.client_host.validate import (
    ClientHostConfigError,
    validate_client_host_config,
)

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


class _GoodStore:
    async def ensure_conversation_exists(self, *a, **k): ...
    async def create_pending_user_request(self, *a, **k): ...
    async def persist_completed_request(self, *a, **k): ...
    async def log_tool_call_start(self, *a, **k): ...
    async def log_tool_call_update(self, *a, **k): ...
    async def get_conversation_config(self, *a, **k): ...
    async def get_conversation_data(self, *a, **k): ...


class _GoodCatalog:
    async def list_models(self): ...
    async def get_model(self, id_or_name): ...


def test_all_errors_reported_at_once():
    class _BadStore:  # missing everything
        pass

    with pytest.raises(ClientHostConfigError) as excinfo:
        validate_client_host_config(
            conversation_store=_BadStore(),  # protocol violation + no catalog
            get_jwt="not-callable",  # not callable + no server_url
            server_url="",  # empty
            source_app=123,  # not a string
        )
    message = str(excinfo.value)
    assert "conversation_store does not implement" in message
    assert "without model_catalog" in message
    assert "get_jwt must be a zero-argument callable" in message
    assert "server_url must be a non-empty string" in message
    assert "source_app must be a non-empty string" in message


def test_valid_client_host_combination_passes():
    validate_client_host_config(
        conversation_store=_GoodStore(),
        model_catalog=_GoodCatalog(),
        api_key_resolver=lambda name: None,
        get_jwt=lambda: None,
        server_url="https://server.example.com",
        source_app="matrx_local",
    )


def test_seams_are_individually_optional():
    # Key resolver alone is a legitimate configuration.
    validate_client_host_config(api_key_resolver=lambda name: None)
    # Catalog alone is a legitimate configuration.
    validate_client_host_config(model_catalog=_GoodCatalog())


def test_store_without_catalog_is_rejected():
    with pytest.raises(ClientHostConfigError, match="without model_catalog"):
        validate_client_host_config(conversation_store=_GoodStore())


def test_configure_registers_seams(client_host_sandbox):
    import matrx_ai
    from matrx_ai._ext import get_ext
    from matrx_ai.client_host import get_conversation_store

    store = _GoodStore()
    matrx_ai.configure(
        conversation_store=store,
        model_catalog=_GoodCatalog(),
        api_key_resolver=lambda name: None,
        get_jwt=lambda: "jwt-token",
        server_url="https://server.example.com",
        source_app="matrx_local",
    )
    assert get_conversation_store() is store
    assert get_ext("server_url") == "https://server.example.com"
    assert get_ext("source_app") == "matrx_local"
    assert get_ext("get_jwt")() == "jwt-token"


def test_configure_rejects_bad_combo(client_host_sandbox):
    import matrx_ai

    with pytest.raises(ClientHostConfigError):
        matrx_ai.configure(conversation_store=_GoodStore())
