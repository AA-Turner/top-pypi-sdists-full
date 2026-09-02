from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from matrx_ai.coding_sessions import BridgeAction, BridgeRequest


def test_observe_hook_allows_bridge_minted_conversation_and_missing_stable_id() -> None:
    request = BridgeRequest.model_validate(
        {
            "action": "observe_hook",
            "provider": "claude_code",
            "provider_session_id": "claude-session",
            "hook_event": {
                "name": "Stop",
                "payload": {"last_assistant_message": "done"},
            },
        }
    )

    assert request.action is BridgeAction.OBSERVE_HOOK
    assert request.conversation is None
    assert request.hook_event is not None
    assert request.hook_event.stable_event_id is None


def test_append_native_requires_managed_origin_runtime_and_conversation() -> None:
    with pytest.raises(ValidationError, match="conversation is required"):
        BridgeRequest.model_validate(
            {
                "action": "append_native",
                "provider": "claude_code",
                "provider_session_id": "native-session",
                "origin": "matrx_local",
                "writer_runtime_id": "local-1",
                "entries": [{"entry_id": "e1", "kind": "user", "payload": {}}],
            }
        )

    request = BridgeRequest.model_validate(
        {
            "action": "append_native",
            "provider": "claude_code",
            "provider_session_id": "native-session",
            "origin": "matrx_sandbox",
            "writer_runtime_id": "sandbox-1",
            "conversation": {
                "conversation_id": str(uuid4()),
                "is_new": True,
                "store": True,
            },
            "entries": [
                {
                    "entry_id": "e1",
                    "source_sequence": 0,
                    "kind": "user",
                    "payload": {"message": "hello"},
                }
            ],
        }
    )

    assert request.writer_runtime_id == "sandbox-1"

    with pytest.raises(ValidationError, match="Input should be True"):
        BridgeRequest.model_validate(
            {
                "action": "append_native",
                "provider": "claude_code",
                "provider_session_id": "native-session",
                "origin": "matrx_local",
                "writer_runtime_id": "local-1",
                "conversation": {
                    "conversation_id": str(uuid4()),
                    "is_new": True,
                    "store": False,
                },
                "entries": [
                    {
                        "entry_id": "e1",
                        "source_sequence": 0,
                        "kind": "user",
                        "payload": {},
                    }
                ],
            }
        )


def test_contract_rejects_unknown_fields_and_noncanonical_hash() -> None:
    with pytest.raises(ValidationError):
        BridgeRequest.model_validate(
            {
                "action": "health",
                "provider": "claude_code",
                "surprise": True,
            }
        )


def test_local_claude_source_metadata_is_bounded_and_identity_free() -> None:
    payload = {
        "action": "append_native",
        "provider": "claude_code",
        "provider_session_id": "native-session",
        "provider_project_key": "project-a",
        "origin": "matrx_local",
        "writer_runtime_id": "local-import",
        "conversation": {
            "conversation_id": str(uuid4()),
            "is_new": True,
            "store": True,
        },
        "entries": [
            {
                "entry_id": "e1",
                "source_sequence": 0,
                "kind": "user",
                "payload": {"message": "hello"},
            }
        ],
        "source_metadata": {
            "source_kind": "claude_local_jsonl",
            "provider_native_session_id": str(uuid4()),
            "provider_account_key": "a" * 64,
            "importer_version": "matrx-local/1",
            "client_version": "2.1.228",
            "transcript_sha256": "b" * 64,
            "transcript_bytes": 12,
            "transcript_entry_count": 1,
            "transcript_mtime_ns": 1,
            "source_complete": True,
        },
    }
    request = BridgeRequest.model_validate(payload)
    assert request.source_metadata is not None
    assert request.source_metadata.provider_account_key == "a" * 64

    project_key = payload.pop("provider_project_key")
    with pytest.raises(ValidationError, match="provider_project_key is required"):
        BridgeRequest.model_validate(payload)
    payload["provider_project_key"] = project_key

    payload["source_metadata"]["email"] = "private@example.com"
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        BridgeRequest.model_validate(payload)


def test_account_identity_fields_are_consistent_and_display_safe() -> None:
    metadata = {
        "source_kind": "claude_local_jsonl",
        "provider_native_session_id": str(uuid4()),
        "provider_account_key": "a" * 64,
        "provider_account_key_version": 2,
        "provider_account_fingerprint": "a" * 12,
        "provider_account_label": "a***n@t***.com",
        "importer_version": "matrx-local/1",
        "transcript_sha256": "b" * 64,
        "transcript_bytes": 12,
        "transcript_entry_count": 1,
        "transcript_mtime_ns": 1,
        "source_complete": True,
    }
    base = {
        "action": "append_native",
        "provider": "claude_code",
        "provider_session_id": "native-session",
        "provider_project_key": "project-a",
        "origin": "matrx_local",
        "writer_runtime_id": "local-import",
        "conversation": {"conversation_id": str(uuid4()), "is_new": True, "store": True},
        "entries": [
            {"entry_id": "e1", "source_sequence": 0, "kind": "user", "payload": {}}
        ],
        "source_metadata": metadata,
    }
    request = BridgeRequest.model_validate(base)
    assert request.source_metadata is not None
    assert request.source_metadata.provider_account_key_version == 2
    assert request.source_metadata.provider_account_fingerprint == "a" * 12
    assert request.source_metadata.provider_account_label == "a***n@t***.com"

    with pytest.raises(ValidationError, match="first 12 hex chars"):
        BridgeRequest.model_validate(
            {**base, "source_metadata": {**metadata, "provider_account_fingerprint": "b" * 12}}
        )
    with pytest.raises(ValidationError, match="requires provider_account_key"):
        BridgeRequest.model_validate(
            {
                **base,
                "source_metadata": {
                    key: value
                    for key, value in metadata.items()
                    if key not in {"provider_account_key", "provider_account_label"}
                },
            }
        )


def test_account_identity_object_is_observe_hook_only() -> None:
    identity = {
        "provider_account_key": "a" * 64,
        "provider_account_key_version": 2,
        "provider_account_label": "a***n@t***.com",
    }
    request = BridgeRequest.model_validate(
        {
            "action": "observe_hook",
            "provider": "claude_code",
            "provider_session_id": "claude-session",
            "hook_event": {"name": "UserPromptSubmit", "payload": {"prompt": "hi"}},
            "account_identity": identity,
        }
    )
    assert request.account_identity is not None
    assert request.account_identity.provider_account_key_version == 2

    with pytest.raises(ValidationError, match="only valid for observe_hook"):
        BridgeRequest.model_validate(
            {
                "action": "append_native",
                "provider": "claude_code",
                "provider_session_id": "native-session",
                "origin": "matrx_sandbox",
                "writer_runtime_id": "sandbox-1",
                "conversation": {
                    "conversation_id": str(uuid4()),
                    "is_new": True,
                    "store": True,
                },
                "entries": [
                    {"entry_id": "e1", "source_sequence": 0, "kind": "user", "payload": {}}
                ],
                "account_identity": identity,
            }
        )

    with pytest.raises(ValidationError, match="first 12 hex chars"):
        BridgeRequest.model_validate(
            {
                "action": "observe_hook",
                "provider": "claude_code",
                "provider_session_id": "claude-session",
                "hook_event": {"name": "UserPromptSubmit", "payload": {"prompt": "hi"}},
                "account_identity": {**identity, "provider_account_fingerprint": "f" * 12},
            }
        )


def test_source_metadata_is_rejected_outside_local_claude_import() -> None:
    payload = {
        "action": "append_native",
        "provider": "codex",
        "provider_session_id": "native-session",
        "provider_project_key": "project-a",
        "origin": "matrx_local",
        "writer_runtime_id": "local-import",
        "conversation": {
            "conversation_id": str(uuid4()),
            "is_new": True,
            "store": True,
        },
        "entries": [
            {
                "entry_id": "e1",
                "source_sequence": 0,
                "kind": "user",
                "payload": {},
            }
        ],
        "source_metadata": {
            "source_kind": "claude_local_jsonl",
            "provider_native_session_id": str(uuid4()),
            "importer_version": "matrx-local/1",
            "transcript_sha256": "b" * 64,
            "transcript_bytes": 0,
            "transcript_entry_count": 1,
            "transcript_mtime_ns": 1,
            "source_complete": True,
        },
    }
    with pytest.raises(ValidationError, match="Matrx Local Claude imports"):
        BridgeRequest.model_validate(payload)

    with pytest.raises(ValidationError, match="string_pattern_mismatch"):
        BridgeRequest.model_validate(
            {
                "action": "append_native",
                "provider": "claude_code",
                "provider_session_id": "native-session",
                "origin": "matrx_local",
                "writer_runtime_id": "local-1",
                "conversation": {
                    "conversation_id": str(uuid4()),
                    "is_new": True,
                },
                "entries": [
                    {
                        "entry_id": "e1",
                        "kind": "user",
                        "payload_sha256": "ABC",
                        "payload": {},
                    }
                ],
            }
        )
