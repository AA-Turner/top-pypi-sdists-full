"""A person's chats (``cx_message`` chunks, D-3 2026-11-19) are recalled ONLY when the caller asks.

Every ordinary search — an agent's RAG tool, a data store, the Knowledge search's passages lane —
passes no ``include_private_kinds``; the host's chat lane sets it after its private-class decision.
Red if the default ever widens back to "every kind" or an explicit list can smuggle the kind in.
"""

from __future__ import annotations

from matrx_rag.search import CHUNK_KINDS, PRIVATE_CHUNK_KINDS, effective_source_kinds


def test_no_kinds_named_means_every_kind_but_chats():
    kinds = effective_source_kinds(None, include_private_kinds=False)
    assert kinds is not None
    assert set(kinds) == set(CHUNK_KINDS) - PRIVATE_CHUNK_KINDS
    assert "cx_message" not in kinds


def test_an_explicit_list_cannot_name_chats_without_permission():
    assert effective_source_kinds(["cx_message"], include_private_kinds=False) == []
    assert effective_source_kinds(["note", "cx_message"], include_private_kinds=False) == ["note"]


def test_the_chat_lane_gets_chats_when_it_asks():
    assert effective_source_kinds(["cx_message"], include_private_kinds=True) == ["cx_message"]
    assert effective_source_kinds(None, include_private_kinds=True) is None
