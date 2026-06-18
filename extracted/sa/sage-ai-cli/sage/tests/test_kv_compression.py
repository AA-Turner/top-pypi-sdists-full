"""Unit and integration tests for kv_compression.py."""

from __future__ import annotations

import zlib
import pytest

from sage.core.kv_compression import compress_kv, decompress_kv


# ==========================================
# UNIT TESTS
# ==========================================

def test_kv_compression_empty_payload():
    """Verify compression and decompression works for empty payloads."""
    payload = b""
    compressed = compress_kv(payload)
    assert isinstance(compressed, bytes)
    assert len(compressed) > 0  # zlib headers
    
    decompressed = decompress_kv(compressed)
    assert decompressed == payload


def test_kv_compression_round_trip():
    """Verify round-trip data integrity for various string structures."""
    payloads = [
        b"hello world",
        b"a" * 1000,
        b"random bytes: \x00\x01\x02\xff\xfe\xfd",
        bytes(range(256))
    ]
    for payload in payloads:
        compressed = compress_kv(payload)
        decompressed = decompress_kv(compressed)
        assert decompressed == payload


def test_kv_compression_ratio_for_highly_repetitive():
    """Verify highly repetitive payload compresses significantly."""
    payload = b"test_data_sequence_12345! " * 500  # 13,000 bytes
    compressed = compress_kv(payload)
    assert len(compressed) < len(payload) / 10  # should compress very well


def test_kv_decompression_failure_on_invalid_data():
    """Verify that decompressing invalid data raises a zlib error."""
    with pytest.raises(zlib.error):
        decompress_kv(b"invalid compressed payload")


# ==========================================
# INTEGRATION TESTS
# ==========================================

class MockKVCacheStore:
    """Mock KV Cache store that manages prompt prefixes and compresses inactive layers."""
    def __init__(self):
        self._store: dict[str, bytes] = {}

    def save_cache(self, prefix_id: str, raw_kv_tensor: bytes):
        # In real settings, kv_tensors can be extremely large, compressing saves RAM/disk
        compressed_kv = compress_kv(raw_kv_tensor)
        self._store[prefix_id] = compressed_kv

    def load_cache(self, prefix_id: str) -> bytes:
        if prefix_id not in self._store:
            raise KeyError(prefix_id)
        compressed_kv = self._store[prefix_id]
        return decompress_kv(compressed_kv)


def test_integration_kv_cache_storage_flow():
    """Integration test simulating storing and loading KV-tensors using the cache store."""
    store = MockKVCacheStore()
    
    # Simulate KV cache activation layers
    layer_1_kv = b"layer_1_weights_and_attention_keys_" * 100
    layer_2_kv = b"layer_2_weights_and_attention_keys_" * 100
    
    # Store them
    store.save_cache("prompt_prefix_1", layer_1_kv)
    store.save_cache("prompt_prefix_2", layer_2_kv)
    
    # Verify they were saved in compressed form
    assert len(store._store["prompt_prefix_1"]) < len(layer_1_kv)
    assert len(store._store["prompt_prefix_2"]) < len(layer_2_kv)

    # Load and check data integrity
    loaded_1 = store.load_cache("prompt_prefix_1")
    loaded_2 = store.load_cache("prompt_prefix_2")
    
    assert loaded_1 == layer_1_kv
    assert loaded_2 == layer_2_kv

    # Attempt to load missing prefix
    with pytest.raises(KeyError):
        store.load_cache("prompt_prefix_3")
