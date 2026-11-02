"""Tests for orchestration key generation (FR-005)."""

from __future__ import annotations

import hashlib

import pytest

from agentic_devtools.adapters.orchestration_key import generate_orchestration_key


class TestGenerateOrchestrationKey:
    """Verify orchestration key generation with NUL-separated SHA-256 algorithm."""

    def test_produces_64_char_hex(self):
        key = generate_orchestration_key("create_issue", "feature-1")
        assert len(key) == 64
        assert all(c in "0123456789abcdef" for c in key)

    def test_deterministic(self):
        key1 = generate_orchestration_key("create_issue", "feature-1")
        key2 = generate_orchestration_key("create_issue", "feature-1")
        assert key1 == key2

    def test_different_refs_produce_different_keys(self):
        key1 = generate_orchestration_key("create_issue", "feature-1")
        key2 = generate_orchestration_key("create_issue", "feature-2")
        assert key1 != key2

    def test_different_operation_types_produce_different_keys(self):
        key1 = generate_orchestration_key("create_issue", "ref-1")
        key2 = generate_orchestration_key("link_subissue", "ref-1")
        assert key1 != key2

    def test_multi_ref(self):
        key = generate_orchestration_key("link_subissue", "parent-ref", "child-ref")
        assert len(key) == 64
        assert all(c in "0123456789abcdef" for c in key)

    def test_multi_ref_order_matters(self):
        key1 = generate_orchestration_key("link_subissue", "parent-ref", "child-ref")
        key2 = generate_orchestration_key("link_subissue", "child-ref", "parent-ref")
        assert key1 != key2

    def test_empty_ref_is_allowed(self):
        key = generate_orchestration_key("create_issue", "")
        assert len(key) == 64

    def test_known_value_regression(self):
        """Verify exact hash matches SHA-256 of NUL-separated input."""
        expected = hashlib.sha256(b"create_issue\x00feature-1").hexdigest()
        actual = generate_orchestration_key("create_issue", "feature-1")
        assert actual == expected

    def test_nul_in_operation_type_raises(self):
        with pytest.raises(ValueError, match="operation_type must not contain NUL bytes"):
            generate_orchestration_key("create\x00issue", "ref")

    def test_nul_in_ref_raises(self):
        with pytest.raises(ValueError, match="refs must not contain NUL bytes"):
            generate_orchestration_key("create_issue", "ref\x00bad")

    def test_empty_operation_type_raises(self):
        with pytest.raises(ValueError, match="operation_type must be a non-empty string"):
            generate_orchestration_key("", "ref")

    def test_whitespace_only_operation_type_raises(self):
        with pytest.raises(ValueError, match="operation_type must be a non-empty string"):
            generate_orchestration_key("   ", "ref")

    def test_non_string_operation_type_raises(self):
        """Non-string operation_type raises ValueError with type name in message."""
        with pytest.raises(ValueError, match="operation_type must be a string, got NoneType"):
            generate_orchestration_key(None, "ref")  # type: ignore[arg-type]

    def test_non_string_ref_raises(self):
        """Non-string ref raises ValueError with type name in message."""
        with pytest.raises(ValueError, match="each ref must be a string, got int"):
            generate_orchestration_key("create_issue", 42)  # type: ignore[arg-type]

    def test_no_refs_produces_valid_key(self):
        key = generate_orchestration_key("create_issue")
        assert len(key) == 64

    def test_distinctness_same_source_multi_target_blocked_by(self):
        """SC-003: multi-target add_blocked_by produces distinct keys."""
        key1 = generate_orchestration_key("add_blocked_by", "issue-A", "blocker-B")
        key2 = generate_orchestration_key("add_blocked_by", "issue-A", "blocker-C")
        assert key1 != key2

    def test_zero_collisions_500_inputs(self):
        """SC-003: zero collisions across 500+ distinct input tuples."""
        keys = set()
        for i in range(500):
            key = generate_orchestration_key("create_issue", f"node-{i}")
            keys.add(key)
        assert len(keys) == 500
