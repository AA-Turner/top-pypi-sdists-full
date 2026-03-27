"""Tests for services/db_auth.py — argon2 passphrase hashing."""

from __future__ import annotations

import pytest


class TestArgon2Unavailable:
    """Tests for the fallback paths when argon2-cffi is not installed."""

    def test_hash_passphrase_raises_when_argon2_unavailable(self) -> None:
        import anteroom.services.db_auth as mod

        original = mod._HAS_ARGON2
        mod._HAS_ARGON2 = False
        try:
            with pytest.raises(RuntimeError, match="argon2-cffi is required"):
                mod.hash_passphrase("test-passphrase")
        finally:
            mod._HAS_ARGON2 = original

    def test_verify_passphrase_raises_when_argon2_unavailable(self) -> None:
        import anteroom.services.db_auth as mod

        original = mod._HAS_ARGON2
        mod._HAS_ARGON2 = False
        try:
            with pytest.raises(RuntimeError, match="argon2-cffi is required"):
                mod.verify_passphrase("test", "$argon2id$v=19$m=65536,t=3,p=4$abc$xyz")
        finally:
            mod._HAS_ARGON2 = original

    def test_needs_rehash_returns_false_when_argon2_unavailable(self) -> None:
        import anteroom.services.db_auth as mod

        original = mod._HAS_ARGON2
        mod._HAS_ARGON2 = False
        try:
            assert mod.needs_rehash("$argon2id$v=19$m=65536,t=3,p=4$abc$xyz") is False
        finally:
            mod._HAS_ARGON2 = original


class TestArgon2Available:
    """Tests for happy-path when argon2-cffi is available."""

    def test_hash_and_verify_roundtrip(self) -> None:
        from anteroom.services.db_auth import hash_passphrase, verify_passphrase

        hashed = hash_passphrase("my-secret-passphrase")
        assert hashed.startswith("$argon2")
        assert verify_passphrase("my-secret-passphrase", hashed) is True

    def test_verify_wrong_passphrase(self) -> None:
        from anteroom.services.db_auth import hash_passphrase, verify_passphrase

        hashed = hash_passphrase("correct-password")
        assert verify_passphrase("wrong-password", hashed) is False
