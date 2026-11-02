"""Tests for orchestration key normalization."""

from __future__ import annotations

import hashlib
from typing import cast

import pytest

from agentic_devtools.adapters.orchestration_key import normalize_orchestration_key


class TestNormalizeOrchestrationKey:
    """Verify caller keys are represented by the canonical SHA-256 marker value."""

    def test_preserves_lowercase_sha256_key(self) -> None:
        key = "a" * 64
        assert normalize_orchestration_key(key) == key

    def test_normalizes_uppercase_sha256_key(self) -> None:
        assert normalize_orchestration_key("ABCD" * 16) == ("abcd" * 16)

    def test_hashes_arbitrary_key(self) -> None:
        key = "customer-path"
        assert normalize_orchestration_key(key) == hashlib.sha256(key.encode("utf-8")).hexdigest()

    @pytest.mark.parametrize("key", ["", None])
    def test_rejects_empty_or_non_string_key(self, key: str | None) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            normalize_orchestration_key(cast(str, key))
