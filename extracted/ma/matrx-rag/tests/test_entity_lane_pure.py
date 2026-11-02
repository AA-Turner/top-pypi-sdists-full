"""Unit tests for the entity-aware search pure helpers — NO DB.

Locks the E1 entity-lane plumbing in matrx_rag/search.py: query tokenization,
scope-id validation (fail-closed), and the static scope-alias VALUES builder
(which is interpolated into SQL, so it MUST contain only safe literals).
"""
from __future__ import annotations

from matrx_rag.search import (
    _ENTITY_MAX_TERMS,
    _ENTITY_MIN_TERM_LEN,
    _SCOPE_ENTITY_TYPE_ALIASES,
    _tokenize_query,
    _validate_scope_ids,
)


class TestTokenizeQuery:
    def test_drops_short_tokens(self):
        tokens, _ = _tokenize_query("a in the cat")
        assert all(len(t) >= _ENTITY_MIN_TERM_LEN for t in tokens)
        assert "cat" in tokens
        assert "a" not in tokens and "in" not in tokens

    def test_lowercases_and_dedupes_preserving_order(self):
        tokens, _ = _tokenize_query("Smith smith SMITH Jones")
        assert tokens == ["smith", "jones"]

    def test_caps_at_max_terms(self):
        q = " ".join(f"term{i}" for i in range(50))
        tokens, _ = _tokenize_query(q)
        assert len(tokens) <= _ENTITY_MAX_TERMS

    def test_phrase_is_full_lowercased_query(self):
        _, phrase = _tokenize_query("  Back Pain Diagnosis  ")
        assert phrase == "back pain diagnosis"

    def test_empty_query(self):
        tokens, phrase = _tokenize_query("")
        assert tokens == []
        assert phrase == ""

    def test_punctuation_split(self):
        tokens, _ = _tokenize_query("case-2024,client.ava")
        assert "2024" in tokens and "client" in tokens and "ava" in tokens


class TestValidateScopeIds:
    _UUID = "3e790542-fdaf-40b2-8bf3-658bf94fe67f"

    def test_none_passthrough(self):
        assert _validate_scope_ids(None) is None

    def test_keeps_valid_uuids(self):
        out = _validate_scope_ids([self._UUID])
        assert out == [self._UUID]

    def test_drops_non_uuids(self):
        out = _validate_scope_ids([self._UUID, "not-a-uuid", "'; DROP TABLE--"])
        assert out == [self._UUID]

    def test_all_invalid_returns_empty_list_not_none(self):
        # An empty list (not None) is the fail-closed signal: caller passed
        # scope_ids but none survived → search must return nothing, not widen.
        out = _validate_scope_ids(["garbage", "also-bad"])
        assert out == []


class TestScopeAliases:
    def test_cx_message_deliberately_unmapped(self):
        # cx_message scope-linking needs a conversation_id join (deferred);
        # it must NOT be in the alias map or scope-filtered cx_message chunks
        # would silently drop.
        assert "cx_message" not in _SCOPE_ENTITY_TYPE_ALIASES

    def test_every_chunk_kind_pairs_with_its_own_token(self):
        # Derived pairing: a chunk kind IS its entity token, so a scope edge
        # carrying the kind always reaches its chunks (web kinds were dropped by
        # the old hand list, 2026-09-26).
        from matrx_rag.search import CHUNK_SOURCE_KINDS

        for kind in CHUNK_SOURCE_KINDS - {"cx_message"}:
            assert kind in _SCOPE_ENTITY_TYPE_ALIASES[kind], kind

    def test_legacy_spellings_survive(self):
        assert {"file", "files", "user_files"} <= set(_SCOPE_ENTITY_TYPE_ALIASES["cld_file"])
        assert "notes" in _SCOPE_ENTITY_TYPE_ALIASES["note"]
        assert "scraped" in _SCOPE_ENTITY_TYPE_ALIASES["scrape_parsed_page"]
