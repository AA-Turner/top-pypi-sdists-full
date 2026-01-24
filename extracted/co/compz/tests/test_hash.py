"""
Tests for SHA-256 hashing with known reference vectors.
"""
import pytest
from compz.hash import hash_compliance, create_memo, parse_memo


def test_hash_known_vector():
    """Test SHA-256 hash against a known reference vector."""
    # Simple canonical JSON string
    canonical_json = '{"a":1,"b":2}'
    
    # Expected SHA-256 hash of this exact string
    expected_hash = "0x43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777"
    
    result = hash_compliance(canonical_json)
    
    assert result == expected_hash, f"Hash mismatch: got {result}, expected {expected_hash}"


def test_hash_empty_string():
    """Test hashing empty string."""
    result = hash_compliance("")
    
    # SHA-256 of empty string
    expected = "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    
    assert result == expected


def test_hash_deterministic():
    """Test that same input always produces same hash."""
    input_str = '{"test":"data","num":123}'
    
    hash1 = hash_compliance(input_str)
    hash2 = hash_compliance(input_str)
    
    assert hash1 == hash2, "Hash should be deterministic"


def test_create_memo_format():
    """Test memo creation follows CompZ format."""
    test_hash = "0xabc123def456"
    memo = create_memo(test_hash)
    
    assert memo.startswith("compz:v1:"), "Memo should start with version prefix"
    assert test_hash in memo, "Memo should contain the hash"


def test_parse_memo_roundtrip():
    """Test memo creation and parsing roundtrip."""
    original_hash = "0x1234567890abcdef"
    memo = create_memo(original_hash)
    parsed = parse_memo(memo)
    
    assert parsed['hash'] == original_hash, "Parsed hash should match original"
    assert parsed['version'] == 'v1', "Version should be v1"
