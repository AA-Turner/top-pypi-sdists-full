"""Vault CredentialResolver seam: stable-reference resolution via host injection.

Unified Credential Vault Phase 5 — matrx-ai consumes stable
``{item_id, field_key}`` / ``field_id`` refs through the host-injected
``credential_resolver`` (matrx_connect.credentials.CredentialResolver) and
never imports the host or the battery.
"""

from __future__ import annotations

import pytest

from matrx_ai._ext import configure_ext
from matrx_ai.providers.keys import (
    ApiKeyNotFoundError,
    get_credential_resolver,
    resolve_credential_field,
)
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.credentials import (
    CredentialRequest,
    CredentialResolution,
    CredentialResolutionError,
)
from matrx_connect.emitters import SilentEmitter

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


class _FakeResolver:
    def __init__(self) -> None:
        self.requests: list[CredentialRequest] = []

    async def resolve(self, request: CredentialRequest) -> CredentialResolution:
        self.requests.append(request)
        if request.ref.item_id == "denied":
            raise CredentialResolutionError("credential item denied not found")
        return CredentialResolution(output="value", value="sk-vault-123")


def _with_actor():
    return set_app_context(AppContext(emitter=SilentEmitter(), user_id="u-actor"))


def test_get_credential_resolver_none_by_default():
    configure_ext(credential_resolver=None)
    assert get_credential_resolver() is None


def test_get_credential_resolver_rejects_non_resolver():
    configure_ext(credential_resolver="not-a-resolver")
    with pytest.raises(TypeError):
        get_credential_resolver()


@pytest.mark.asyncio
async def test_resolves_stable_ref_with_attribution():
    fake = _FakeResolver()
    configure_ext(credential_resolver=fake)
    token = _with_actor()
    try:
        value = await resolve_credential_field(
            item_id="item-1",
            field_key="api_key",
            purpose="anthropic provider call",
            invocation_id="run-9",
        )
    finally:
        clear_app_context(token)
    assert value == "sk-vault-123"
    (request,) = fake.requests
    assert request.actor_user_id == "u-actor"
    assert request.ref.item_id == "item-1"
    assert request.ref.field_key == "api_key"
    assert request.consumer == "agent"
    assert request.purpose == "anthropic provider call"
    assert request.invocation_id == "run-9"
    assert request.output == "value"


@pytest.mark.asyncio
async def test_denied_returns_none_or_raises_when_required():
    fake = _FakeResolver()
    configure_ext(credential_resolver=fake)
    token = _with_actor()
    try:
        assert (
            await resolve_credential_field(
                item_id="denied", field_key="api_key", purpose="t"
            )
            is None
        )
        with pytest.raises(ApiKeyNotFoundError):
            await resolve_credential_field(
                item_id="denied", field_key="api_key", purpose="t", required=True
            )
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_missing_resolver_or_actor_is_loud_when_required():
    configure_ext(credential_resolver=None)
    with pytest.raises(ApiKeyNotFoundError):
        await resolve_credential_field(
            item_id="i", field_key="k", purpose="t", required=True
        )
    # Resolver present but no ambient actor:
    configure_ext(credential_resolver=_FakeResolver())
    with pytest.raises(ApiKeyNotFoundError):
        await resolve_credential_field(
            item_id="i", field_key="k", purpose="t", required=True
        )
