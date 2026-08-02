"""XOR stream cipher: linear rewrite stays byte-identical to the reference."""

import hashlib
import os

import pytest

from xpander_sdk.core.context_optimizer import encryption as enc


def _reference_xor(data: bytes, key: bytes) -> bytes:
    """The original O(n^2) implementation, kept here as the byte-identity oracle."""
    key_stream = b""
    counter = 0
    while len(key_stream) < len(data):
        key_stream += hashlib.sha256(key + counter.to_bytes(4, "big")).digest()
        counter += 1
    return bytes(a ^ b for a, b in zip(data, key_stream[: len(data)]))


KEY = hashlib.sha256(b"org_agent_task").digest()


@pytest.mark.parametrize("size", [0, 1, 31, 32, 33, 1000, 1 << 20])
def test_xor_stream_byte_identical_to_reference(size: int) -> None:
    """The linear _xor_stream produces the exact bytes of the reference impl."""
    data = os.urandom(size)
    assert enc._xor_stream(data, KEY) == _reference_xor(data, KEY)


@pytest.mark.parametrize("text", ["", "hi", "unicode: café ☕", "x" * 100_000])
def test_encrypt_decrypt_roundtrip(text: str) -> None:
    """encrypt then decrypt returns the original string (incl. multibyte)."""
    ct = enc.encrypt(text, KEY)
    assert enc.decrypt(ct, KEY) == text


def test_derive_key_stable() -> None:
    """Key derivation is deterministic and varies with the identifiers."""
    assert enc.derive_key("o", "a", "t") == enc.derive_key("o", "a", "t")
    assert enc.derive_key("o", "a", "t") != enc.derive_key("o", "a", "t2")


@pytest.mark.asyncio
async def test_aencrypt_matches_sync_small_and_large() -> None:
    """aencrypt equals encrypt on both sides of the thread-offload byte gate."""
    for text in ["small", "y" * 300_000]:  # 300K crosses the to_thread offload gate
        assert await enc.aencrypt(text, KEY) == enc.encrypt(text, KEY)


@pytest.mark.asyncio
async def test_aencrypt_offloads_on_multibyte_byte_size() -> None:
    """A short-in-chars but large-in-bytes payload still roundtrips (gate uses bytes)."""
    text = "☕" * 100_000  # ~100k chars but ~300k UTF-8 bytes
    assert enc.decrypt(await enc.aencrypt(text, KEY), KEY) == text


def test_try_decrypt_picks_the_working_key() -> None:
    """try_decrypt returns the plaintext for the first valid key, raises if none work."""
    right = enc.derive_key("o", "a", "task")
    wrong = enc.derive_key("o", "a", "other")
    ct = enc.encrypt("payload", right)
    assert enc.try_decrypt(ct, [wrong, right]) == "payload"
    with pytest.raises(Exception):
        enc.try_decrypt(ct, [wrong])
