"""CredentialResolver protocol contract tests (Unified Credential Vault, Phase 5)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_connect.credentials import (
    CredentialRef,
    CredentialRequest,
    CredentialResolution,
    CredentialResolver,
)


def test_ref_field_id_form() -> None:
    ref = CredentialRef(field_id="f-1")
    assert not ref.is_item_level


def test_ref_item_field_key_form() -> None:
    ref = CredentialRef(item_id="i-1", field_key="api_key")
    assert not ref.is_item_level


def test_ref_item_level_form() -> None:
    assert CredentialRef(item_id="i-1").is_item_level


def test_ref_rejects_mixed_forms() -> None:
    with pytest.raises(ValidationError):
        CredentialRef(field_id="f-1", item_id="i-1")


def test_ref_rejects_empty() -> None:
    with pytest.raises(ValidationError):
        CredentialRef()


def test_ref_rejects_key_only() -> None:
    # A mutable env-key string is deliberately not representable.
    with pytest.raises(ValidationError):
        CredentialRef(field_key="api_key")


def test_request_value_requires_field_ref() -> None:
    with pytest.raises(ValidationError):
        CredentialRequest(
            actor_user_id="u1",
            ref=CredentialRef(item_id="i-1"),
            consumer="agent",
            purpose="provider call",
            output="value",
        )


def test_request_env_map_requires_item_ref() -> None:
    with pytest.raises(ValidationError):
        CredentialRequest(
            actor_user_id="u1",
            ref=CredentialRef(field_id="f-1"),
            consumer="sandbox",
            purpose="sandbox env",
            output="env_map",
        )


def test_resolution_payload_must_match_output() -> None:
    with pytest.raises(ValidationError):
        CredentialResolution(output="value", env_map={"A": "b"})
    with pytest.raises(ValidationError):
        CredentialResolution(output="value")
    ok = CredentialResolution(output="value", value="s")
    assert ok.value == "s"


@pytest.mark.asyncio
async def test_protocol_is_runtime_checkable() -> None:
    class Impl:
        async def resolve(self, request: CredentialRequest) -> CredentialResolution:
            return CredentialResolution(output="value", value="x")

    impl = Impl()
    assert isinstance(impl, CredentialResolver)
    request = CredentialRequest(
        actor_user_id="u1",
        ref=CredentialRef(item_id="i-1", field_key="api_key"),
        consumer="agent",
        purpose="test",
        invocation_id="inv-1",
    )
    result = await impl.resolve(request)
    assert result.value == "x"
