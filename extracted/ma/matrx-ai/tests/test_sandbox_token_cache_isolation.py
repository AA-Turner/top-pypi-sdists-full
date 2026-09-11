"""A re-minted sandbox token belongs to ONE actor, ONE run, ONE exact target.

``_sandbox_proxy`` caches a token re-minted after a 401/403 so the rest of the
loop reuses it. The cache key is the isolation boundary: a key coarser than
(user, request/execution, target_kind, base_url, sandbox_id) serves one
principal's credential to another. The minter is the only external dependency
(host orchestrator); it mints a DISTINCT token per (sandbox, caller) so a
cross-served token is observable by value.
"""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import AsyncMock

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import set_app_context, try_get_app_context

from matrx_ai import _ext
from matrx_ai.tools import _sandbox_proxy as proxy


class _Minter:
    """Mints ``fresh:<sandbox_id>:<user>:<request>`` — distinct per identity."""

    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    async def __call__(self, *, sandbox_id: str, base_url: str) -> str:
        self.calls.append({"sandbox_id": sandbox_id, "base_url": base_url})
        ctx = try_get_app_context()
        return f"fresh:{sandbox_id}:{ctx.user_id}:{ctx.request_id or ctx.execution_id}"


@pytest.fixture
def minter(monkeypatch: pytest.MonkeyPatch) -> _Minter:
    m = _Minter()
    monkeypatch.setattr(_ext, "get_sandbox_token_minter", lambda: m)
    return m


def _binding(**overrides: str) -> proxy.SandboxBinding:
    base = proxy.SandboxBinding(
        sandbox_id="sbx-a",
        base_url="https://trusted.invalid/sandboxes/sbx-a",
        access_token="client-token-a",
        root_path="/home/agent",
    )
    return replace(base, **overrides)


def _token(binding: proxy.SandboxBinding) -> str:
    return proxy._headers(binding)["X-Sandbox-Access-Token"]


OWNER = AppContext(emitter=AsyncMock(), user_id="owner", request_id="request-owner")


async def test_reminted_token_is_reused_by_the_same_actor_run_and_target(minter: _Minter) -> None:
    # Breaks caught: the cache never consulted, or the client token preferred
    # over the renewal (the loop would 401 on every call after expiry).
    set_app_context(OWNER)
    binding = _binding()

    assert await proxy._remint_token(binding) == "fresh:sbx-a:owner:request-owner"
    assert minter.calls == [
        {"sandbox_id": "sbx-a", "base_url": "https://trusted.invalid/sandboxes/sbx-a"}
    ]
    assert _token(binding) == "fresh:sbx-a:owner:request-owner"


@pytest.mark.parametrize(
    "crossing",
    ["other_actor", "other_request", "other_route", "other_sandbox", "local_machine"],
)
async def test_reminted_token_never_crosses_an_isolation_boundary(
    minter: _Minter, crossing: str
) -> None:
    set_app_context(OWNER)
    await proxy._remint_token(_binding())

    other = _binding(access_token="client-token-b")
    if crossing == "other_actor":
        set_app_context(OWNER.with_overrides(user_id="stranger"))
    elif crossing == "other_request":
        set_app_context(OWNER.with_overrides(request_id="unrelated-request"))
    elif crossing == "other_route":
        other = replace(other, base_url="https://attacker.invalid")
    elif crossing == "other_sandbox":
        # Same orchestrator route, different box: the sandbox id alone separates them.
        other = replace(other, sandbox_id="sbx-b")
    else:
        other = replace(other, target_kind="local_machine")

    assert _token(other) == "client-token-b"


async def test_two_actors_on_one_sandbox_each_keep_their_own_renewal(minter: _Minter) -> None:
    # Break caught: a key missing the actor — the second renewal overwrites the
    # first, and the owner's next call rides the stranger's credential.
    binding = _binding()
    stranger = OWNER.with_overrides(user_id="stranger", request_id="request-stranger")

    set_app_context(OWNER)
    await proxy._remint_token(binding)
    set_app_context(stranger)
    await proxy._remint_token(binding)

    assert _token(binding) == "fresh:sbx-a:stranger:request-stranger"
    set_app_context(OWNER)
    assert _token(binding) == "fresh:sbx-a:owner:request-owner"


@pytest.mark.parametrize(
    "ctx",
    [
        pytest.param(AppContext(emitter=AsyncMock(), user_id="owner"), id="no_request_or_execution"),
        pytest.param(AppContext(emitter=AsyncMock(), user_id="", request_id="r-1"), id="no_actor"),
    ],
)
async def test_renewal_without_a_full_identity_is_never_cached(minter: _Minter, ctx: AppContext) -> None:
    # Break caught: caching under a partial key — every request-less context of
    # a user (or every anonymous caller of a request) would share one credential.
    set_app_context(ctx)
    binding = _binding()

    fresh = await proxy._remint_token(binding)

    assert fresh is not None and fresh.startswith("fresh:sbx-a:")
    assert _token(binding) == "client-token-a"


async def test_local_machine_never_requests_orchestrator_token(minter: _Minter) -> None:
    set_app_context(AppContext(emitter=AsyncMock(), user_id="owner", request_id="local-request"))
    binding = proxy.SandboxBinding(
        sandbox_id="sbx-cloud-shaped",
        base_url="https://local-proxy.invalid",
        access_token="desktop-jwt",
        root_path="C:\\Users\\owner",
        target_kind="local_machine",
    )
    assert await proxy._remint_token(binding) is None
    assert minter.calls == []
