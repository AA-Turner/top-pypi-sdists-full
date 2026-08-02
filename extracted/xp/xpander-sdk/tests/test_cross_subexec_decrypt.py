"""Offloaded context must decrypt across sibling sub-executions of one conversation.

The encryption key is scoped to the conversation root (gateway) execution, so a
blob offloaded in sub-execution A can be retrieved/decrypted from sibling B.
"""
from types import SimpleNamespace

import pytest

from xpander_sdk.core.context_optimizer.encryption import (
    candidate_scope_ids,
    conversation_scope_id,
    derive_key,
    encrypt,
    try_decrypt,
)

_ORG, _AGENT = "org-1", "agent-1"


def _key(scope_id: str) -> bytes:
    return derive_key(_ORG, _AGENT, scope_id)


def _encrypt_for(task, payload: str) -> str:
    return encrypt(payload, _key(conversation_scope_id(task)))


def _decrypt_from(task, blob: str) -> str:
    return try_decrypt(blob, [_key(s) for s in candidate_scope_ids(task)])


def test_sibling_subexecution_can_decrypt():
    payload = '[{"id":"org-02847","name":"Nova Ventures"}]' * 4000
    child_a = SimpleNamespace(id="A", parent_execution="GW")
    child_b = SimpleNamespace(id="B", parent_execution="GW")
    blob = _encrypt_for(child_a, payload)
    assert _decrypt_from(child_b, blob) == payload


def test_same_task_still_decrypts():
    child_a = SimpleNamespace(id="A", parent_execution="GW")
    blob = _encrypt_for(child_a, "hello world payload" * 1000)
    assert _decrypt_from(child_a, blob).startswith("hello world payload")


def test_gateway_offload_decrypts_in_child_and_self():
    gw = SimpleNamespace(id="GW", parent_execution=None)
    child = SimpleNamespace(id="B", parent_execution="GW")
    blob = _encrypt_for(gw, "gateway data" * 1000)
    assert _decrypt_from(child, blob).startswith("gateway data")
    assert _decrypt_from(gw, blob).startswith("gateway data")


def test_scope_ids_order_specific_first():
    assert candidate_scope_ids(SimpleNamespace(id="B", parent_execution="GW")) == ["B", "GW"]
    assert candidate_scope_ids(SimpleNamespace(id="GW", parent_execution=None)) == ["GW"]


def test_try_decrypt_raises_when_no_key_matches():
    blob = encrypt("secret payload" * 500, _key("right"))
    with pytest.raises(Exception):
        try_decrypt(blob, [_key("wrong-1"), _key("wrong-2")])
