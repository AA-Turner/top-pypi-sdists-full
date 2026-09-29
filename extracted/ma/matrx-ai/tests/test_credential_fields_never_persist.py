"""Credential-shaped fields never reach a durable row; ordinary fields always do.

2026-09-26: 653 chat.user_request rows held metadata.active_sandbox.access_token
(a live sandbox bearer token) because the run context's metadata is persisted
wholesale at the end of every turn.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

import pytest

from matrx_ai.utils.credential_fields import is_credential_field, without_credential_fields


@pytest.mark.parametrize(
    "name",
    ["access_token", "accessToken", "refresh_token", "api_key", "apiKey", "x-api-key",
     "Authorization", "client_secret", "password", "session_cookie", "credentials",
     "bearer", "private_key"],
)
def test_credential_names_are_caught(name: str) -> None:
    assert is_credential_field(name)


@pytest.mark.parametrize(
    "name",
    ["mandate_key", "setting_key", "signature", "max_output_tokens", "total_tokens",
     "input_tokens", "token_count", "token_type", "token_expires", "keywords",
     "sandbox_id", "base_url", "jwt_claims", "auth_type", "response_id"],
)
def test_ordinary_names_are_kept(name: str) -> None:
    assert not is_credential_field(name)


def test_a_real_turn_record_loses_only_the_token() -> None:
    metadata = {
        "mandate_key": "ai.model_config_sync",
        "active_sandbox": {
            "sandbox_id": "sbx-7ddc2eb0c364",
            "base_url": "http://sandbox-orchestrator.internal.matrxserver.com:8000/sandboxes/sbx-7ddc2eb0c364",
            "root_path": "/home/agent",
            "target_kind": "sandbox",
            "access_token": "eyJhbGciOiJIUzI1NiJ9.sandbox.sig",
        },
        "usage_by_model": {"claude-opus-5-5": {"input_tokens": 93081, "output_tokens": 0}},
    }

    kept = without_credential_fields(metadata)

    assert "access_token" not in kept["active_sandbox"]
    assert kept["active_sandbox"]["sandbox_id"] == "sbx-7ddc2eb0c364"
    assert kept["mandate_key"] == "ai.model_config_sync"
    assert kept["usage_by_model"]["claude-opus-5-5"]["input_tokens"] == 93081
    assert metadata["active_sandbox"]["access_token"], "the live run keeps its token"


def test_both_durable_request_writes_filter_their_metadata() -> None:

    from matrx_ai.db import persistence

    source = stable_source(persistence)
    assert source.count("without_credential_fields(") >= 2


def test_ownership_markers_and_cursors_survive() -> None:
    kept = without_credential_fields(
        {
            "run_claim_token": "conversation_recovery:acdd41f4-c1e1-4787-9d7c-0b4b6f7a2e11",
            "next_page_token": "page-3",
            "secret_names": ["ANTHROPIC_API_KEY"],
            "cookie_consent": True,
            "credential_login": {"verdict": "matched", "password": "hunter2-live"},
            "session_blob_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcm1hbiJ9.c2lnbmF0dXJlc2ln",
        }
    )

    assert kept["run_claim_token"].startswith("conversation_recovery:")
    assert kept["next_page_token"] == "page-3"
    assert kept["secret_names"] == ["ANTHROPIC_API_KEY"]
    assert kept["cookie_consent"] is True
    assert kept["credential_login"] == {"verdict": "matched"}
    assert "session_blob_token" not in kept
