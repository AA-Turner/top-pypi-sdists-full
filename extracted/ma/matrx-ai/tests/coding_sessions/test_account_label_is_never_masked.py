"""THE GUARD: a masked provider account label never gets through the bridge door.

WHY THIS FILE EXISTS. Arman ruled on 2026-09-07 that a Claude account name is
not a secret, and the masking code was deleted from every producer that day
(``matrx-local`` ``claude_probe.account_label``, the plugin hook
``account_identity.account_label``). On 2026-09-17 he opened AI Matrx and still
saw his own email as ``a***@…``: 923 ``chat.coding_session`` rows written before
the deletion still carried the masked string, and every reader shows what the
row holds. Deleting a producer is not closing a class — nothing at the door
refused the shape, so any future producer, importer, replay or hand-written
envelope could put it back.

WHAT IT PROVES. ``provider_account_label`` reaches the platform through exactly
two wire carriers, :class:`BridgeAccountIdentity` (the ``observe_hook``
envelope) and :class:`BridgeSourceMetadata` (the Matrx Local import envelope).
Both annotate the field with the ONE ``AccountLabel`` type, so the refusal is a
single door. Each test below plants a real masked value observed in production
and proves the envelope is refused as a typed ``ValidationError``, then proves
the same envelope with the account's own identity is accepted — red on the
mask, green on the truth.

FALSIFIABILITY. ``test_the_guard_can_fail`` calls the validator directly on the
masked strings and on the clean ones, so a future edit that neuters
``refuse_masked_account_label`` into a pass-through fails here by name rather
than silently disarming every other test in this file.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from matrx_ai.coding_sessions.models import (
    AccountLabel,
    BridgeAccountIdentity,
    BridgeRequest,
    BridgeSourceMetadata,
    refuse_masked_account_label,
)

# Exactly the strings production held on 2026-09-17, plus the org-id form.
MASKED_LABELS = (
    "a***n@a***.com",  # arman@allgreenrecycling.com — 306 rows, what Arman saw
    "a***n@t***.com",  # arman@titaniumsuccess.com — 152 rows
    "i***o@a***.com",  # info@aimatrx.com — 447 rows
    "a***i@v***.com",  # armani@vasaro.com — 1 row
    "a***6@g***.com",  # the one account with no unmasked sibling — 5 rows
    "***@***.com",
    "org:9f8e***-****-****",
)

CLEAN_LABELS = (
    "arman@allgreenrecycling.com",
    "arman@titaniumsuccess.com",
    "info@aimatrx.com",
    "armani@vasaro.com",
    "admin@admin.com",
    "org:0e2f4a1c-6b7d-4c3e-9a11-8d5f2b6c7e90",
)


def _identity_payload(label: str) -> dict[str, object]:
    return {
        "provider_account_key": "a" * 64,
        "provider_account_key_version": 2,
        "provider_account_fingerprint": "a" * 12,
        "provider_account_label": label,
    }


def _source_metadata_payload(label: str) -> dict[str, object]:
    return {
        "source_kind": "claude_local_jsonl",
        "provider_native_session_id": str(uuid4()),
        "provider_account_key": "a" * 64,
        "provider_account_key_version": 2,
        "provider_account_fingerprint": "a" * 12,
        "provider_account_label": label,
        "importer_version": "matrx-local/1",
        "transcript_sha256": "b" * 64,
        "transcript_bytes": 12,
        "transcript_entry_count": 1,
        "transcript_mtime_ns": 1,
        "source_complete": True,
    }


def _observe_hook_request(label: str) -> dict[str, object]:
    return {
        "action": "observe_hook",
        "provider": "claude_code",
        "provider_session_id": "claude-session",
        "origin": "independent_hook",
        "hook_event": {"name": "UserPromptSubmit", "payload": {"prompt": "hi"}},
        "account_identity": _identity_payload(label),
    }


def _append_native_request(label: str) -> dict[str, object]:
    return {
        "action": "append_native",
        "provider": "claude_code",
        "provider_session_id": "native-session",
        "provider_project_key": "project-a",
        "origin": "matrx_local",
        "writer_runtime_id": "local-import",
        "conversation": {"conversation_id": str(uuid4()), "is_new": True, "store": True},
        "entries": [{"entry_id": "e1", "source_sequence": 0, "kind": "user", "payload": {}}],
        "source_metadata": _source_metadata_payload(label),
    }


def test_the_guard_can_fail() -> None:
    """The validator itself refuses every mask and passes every real label."""

    for label in MASKED_LABELS:
        with pytest.raises(ValueError, match="never a mask"):
            refuse_masked_account_label(label)
    for label in CLEAN_LABELS:
        assert refuse_masked_account_label(label) == label
    assert AccountLabel is not None


@pytest.mark.parametrize("label", MASKED_LABELS)
def test_account_identity_carrier_refuses_a_masked_label(label: str) -> None:
    with pytest.raises(ValidationError, match="never a mask"):
        BridgeAccountIdentity.model_validate(_identity_payload(label))


@pytest.mark.parametrize("label", CLEAN_LABELS)
def test_account_identity_carrier_accepts_the_accounts_own_identity(label: str) -> None:
    identity = BridgeAccountIdentity.model_validate(_identity_payload(label))
    assert identity.provider_account_label == label


@pytest.mark.parametrize("label", MASKED_LABELS)
def test_source_metadata_carrier_refuses_a_masked_label(label: str) -> None:
    with pytest.raises(ValidationError, match="never a mask"):
        BridgeSourceMetadata.model_validate(_source_metadata_payload(label))


@pytest.mark.parametrize("label", CLEAN_LABELS)
def test_source_metadata_carrier_accepts_the_accounts_own_identity(label: str) -> None:
    metadata = BridgeSourceMetadata.model_validate(_source_metadata_payload(label))
    assert metadata.provider_account_label == label


def test_the_whole_observe_hook_envelope_is_refused() -> None:
    """The refusal is reached through the real request model, not just the field."""

    with pytest.raises(ValidationError, match="never a mask"):
        BridgeRequest.model_validate(_observe_hook_request("a***n@a***.com"))
    request = BridgeRequest.model_validate(_observe_hook_request("arman@allgreenrecycling.com"))
    assert request.account_identity is not None
    assert request.account_identity.provider_account_label == "arman@allgreenrecycling.com"


def test_the_whole_append_native_envelope_is_refused() -> None:
    with pytest.raises(ValidationError, match="never a mask"):
        BridgeRequest.model_validate(_append_native_request("a***n@t***.com"))
    request = BridgeRequest.model_validate(_append_native_request("arman@titaniumsuccess.com"))
    assert request.source_metadata is not None
    assert request.source_metadata.provider_account_label == "arman@titaniumsuccess.com"


def test_every_wire_carrier_of_the_label_is_covered_by_this_guard() -> None:
    """A third carrier added later must be added here, or this census fails.

    The refusal is only a class-closing guard while the two models below are
    the complete set of bridge fields named ``provider_account_label``. This
    test reads the live model registry rather than a hand-kept list, so a new
    carrier declared without the ``AccountLabel`` annotation is named out loud.
    """

    from matrx_ai.coding_sessions import models as models_module

    carriers = {
        name: model
        for name, model in vars(models_module).items()
        if isinstance(model, type)
        and issubclass(model, BridgeAccountIdentity.__mro__[1])
        and "provider_account_label" in getattr(model, "model_fields", {})
    }
    assert set(carriers) == {"BridgeAccountIdentity", "BridgeSourceMetadata"}, (
        "a new carrier of provider_account_label appeared: annotate it with "
        f"AccountLabel and add it to this guard — found {sorted(carriers)}"
    )
    for name, model in carriers.items():
        with pytest.raises(ValidationError, match="never a mask"):
            model.model_validate(
                _identity_payload("a***n@a***.com")
                if name == "BridgeAccountIdentity"
                else _source_metadata_payload("a***n@a***.com")
            )
