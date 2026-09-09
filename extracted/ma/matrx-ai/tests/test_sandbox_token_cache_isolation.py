from dataclasses import replace
from unittest.mock import AsyncMock

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import set_app_context
from matrx_ai.tools import _sandbox_proxy as proxy


@pytest.mark.asyncio
@pytest.mark.parametrize("mutation", ["actor", "route", "local_machine", "request"])
async def test_renewed_token_never_crosses_execution_authority(monkeypatch, mutation):
    from matrx_ai import _ext

    monkeypatch.setattr(
        _ext, "get_sandbox_token_minter", lambda: AsyncMock(return_value="fresh-owner-token")
    )
    owner = AppContext(emitter=AsyncMock(), user_id="owner", request_id="request-owner")
    set_app_context(owner)
    binding = proxy.SandboxBinding(
        sandbox_id="sbx-cache-proof",
        base_url="https://trusted.invalid/sandboxes/sbx-cache-proof",
        access_token="original-owner-token",
        root_path="/home/agent",
    )
    assert await proxy._remint_token(binding) == "fresh-owner-token"
    assert proxy._headers(binding)["X-Sandbox-Access-Token"] == "fresh-owner-token"
    other = replace(binding, access_token="other-binding-token")
    if mutation == "actor":
        set_app_context(owner.with_overrides(user_id="stranger"))
    elif mutation == "request":
        set_app_context(owner.with_overrides(request_id="unrelated-request"))
    elif mutation == "route":
        other = replace(other, base_url="https://attacker.invalid")
    else:
        other = replace(other, target_kind="local_machine")
    assert proxy._headers(other)["X-Sandbox-Access-Token"] == "other-binding-token"


@pytest.mark.asyncio
async def test_local_machine_never_requests_orchestrator_token(monkeypatch):
    from matrx_ai import _ext

    minter = AsyncMock(return_value="cloud-only-token")
    monkeypatch.setattr(_ext, "get_sandbox_token_minter", lambda: minter)
    set_app_context(AppContext(emitter=AsyncMock(), user_id="owner", request_id="local-request"))
    binding = proxy.SandboxBinding(
        sandbox_id="sbx-cloud-shaped",
        base_url="https://local-proxy.invalid",
        access_token="desktop-jwt",
        root_path="C:\\Users\\owner",
        target_kind="local_machine",
    )
    assert await proxy._remint_token(binding) is None
    minter.assert_not_awaited()
