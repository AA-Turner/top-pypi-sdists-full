"""Tests for derive_operation_id_fallback in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

import hashlib

from agentic_devtools.cli.speckit.phase0.identifiers import (
    canonicalize_json,
    derive_operation_id_fallback,
)


class TestDeriveOperationIdFallback:
    """Tests for the derive_operation_id_fallback function."""

    def test_matches_expected_digest(self) -> None:
        payload = {"b": 2, "a": 1}
        expected_digest = hashlib.sha256(canonicalize_json(payload)).hexdigest()
        assert derive_operation_id_fallback(payload) == f"gh-event-fallback:{expected_digest}"

    def test_is_deterministic_regardless_of_key_order(self) -> None:
        first = derive_operation_id_fallback({"a": 1, "b": 2})
        second = derive_operation_id_fallback({"b": 2, "a": 1})
        assert first == second

    def test_lowercase_hex_digest(self) -> None:
        result = derive_operation_id_fallback({"x": 1})
        digest = result.split(":", 1)[1]
        assert digest == digest.lower()
        assert len(digest) == 64

    def test_different_payloads_produce_different_ids(self) -> None:
        assert derive_operation_id_fallback({"a": 1}) != derive_operation_id_fallback({"a": 2})
