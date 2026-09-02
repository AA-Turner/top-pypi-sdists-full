"""Tests for orchestration key embedding and extraction."""

from __future__ import annotations

from agentic_devtools.adapters.orchestration_key import (
    embed_orchestration_key,
    extract_orchestration_key,
)


class TestEmbedOrchestrationKey:
    """Verify orchestration key embedding."""

    def test_embed_into_empty_body(self):
        key = "a" * 64
        result = embed_orchestration_key("", key)
        assert result == f"<!-- agdt-orch-key:{'a' * 64} -->"

    def test_embed_appends_to_body(self):
        key = "b" * 64
        result = embed_orchestration_key("Hello world", key)
        assert result == f"Hello world\n\n<!-- agdt-orch-key:{'b' * 64} -->"

    def test_embed_with_trailing_newline(self):
        key = "c" * 64
        result = embed_orchestration_key("Hello\n", key)
        assert result == f"Hello\n\n<!-- agdt-orch-key:{'c' * 64} -->"

    def test_embed_replaces_different_key(self):
        key_old = "a" * 64
        key_new = "b" * 64
        body = f"Content\n\n<!-- agdt-orch-key:{key_old} -->"
        result = embed_orchestration_key(body, key_new)
        assert f"agdt-orch-key:{key_new}" in result
        assert key_old not in result

    def test_embed_idempotent_same_key(self):
        key = "d" * 64
        body = f"Content\n\n<!-- agdt-orch-key:{key} -->"
        result = embed_orchestration_key(body, key)
        assert result == body

    def test_embed_normalizes_uppercase_key_and_marker(self):
        key = "ABCD" * 16
        body = f"Content\n\n<!-- agdt-orch-key:{key} -->"
        result = embed_orchestration_key(body, key)
        assert result == f"Content\n\n<!-- agdt-orch-key:{key.lower()} -->"


class TestExtractOrchestrationKey:
    """Verify orchestration key extraction."""

    def test_extract_from_body(self):
        key = "e" * 64
        body = f"Some content\n\n<!-- agdt-orch-key:{key} -->"
        assert extract_orchestration_key(body) == key

    def test_extract_returns_none_when_missing(self):
        assert extract_orchestration_key("No key here") is None

    def test_extract_returns_none_for_empty(self):
        assert extract_orchestration_key("") is None

    def test_extract_with_surrounding_content(self):
        key = "f" * 64
        body = f"Before\n<!-- agdt-orch-key:{key} -->\nAfter"
        assert extract_orchestration_key(body) == key

    def test_extract_uppercase_marker_normalizes_to_lowercase(self):
        key = "ABCD" * 16
        body = f"Before\n<!-- agdt-orch-key:{key} -->\nAfter"
        assert extract_orchestration_key(body) == key.lower()
