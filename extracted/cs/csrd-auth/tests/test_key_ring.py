"""Tests for KeyRingManager — automatic signing key lifecycle."""

import asyncio
from datetime import UTC, datetime, timedelta

import pytest

from csrd.auth._key_ring import (
    KeyRingManager,
    SigningKey,
    _generate_rsa_keypair,
    _public_pem_to_jwk,
)
from csrd.repository import SQLiteAdapter


@pytest.fixture
async def adapter(tmp_path):
    """Provide a connected SQLite adapter for testing."""
    db_path = tmp_path / "test_keyring.db"
    a = SQLiteAdapter(db_path=str(db_path))
    await a.connect()
    yield a
    await a.close()


@pytest.fixture
async def manager(adapter):
    """Provide an initialized KeyRingManager."""
    mgr = KeyRingManager(
        adapter=adapter,
        key_size=2048,
        rotation_interval=60,
        token_ttl=30,
    )
    await mgr.initialize()
    return mgr


# ── Key generation helpers ───────────────────────────────────────────────


class TestRSAKeypairGeneration:
    def test_generates_pem_bytes(self):
        private_pem, public_pem = _generate_rsa_keypair(2048)
        assert private_pem.startswith(b"-----BEGIN PRIVATE KEY-----")
        assert public_pem.startswith(b"-----BEGIN PUBLIC KEY-----")

    def test_different_calls_produce_different_keys(self):
        priv1, _ = _generate_rsa_keypair(2048)
        priv2, _ = _generate_rsa_keypair(2048)
        assert priv1 != priv2


class TestPublicPemToJwk:
    def test_produces_valid_jwk(self):
        _, public_pem = _generate_rsa_keypair(2048)
        jwk = _public_pem_to_jwk(public_pem, kid="test-key", algorithm="RS256")
        assert jwk["kid"] == "test-key"
        assert jwk["use"] == "sig"
        assert jwk["alg"] == "RS256"
        assert "n" in jwk  # RSA modulus
        assert "e" in jwk  # RSA exponent
        assert jwk["kty"] == "RSA"


# ── SigningKey dataclass ─────────────────────────────────────────────────


class TestSigningKey:
    def test_not_expired(self):
        key = SigningKey(
            kid="k1",
            private_pem=b"",
            public_pem=b"",
            algorithm="RS256",
            created_at=datetime.now(UTC),
            expires_at=datetime.now(UTC) + timedelta(hours=1),
        )
        assert key.is_expired is False

    def test_expired(self):
        key = SigningKey(
            kid="k1",
            private_pem=b"",
            public_pem=b"",
            algorithm="RS256",
            created_at=datetime.now(UTC) - timedelta(hours=2),
            expires_at=datetime.now(UTC) - timedelta(hours=1),
        )
        assert key.is_expired is True


# ── KeyRingManager ───────────────────────────────────────────────────────


class TestKeyRingManagerInit:
    @pytest.mark.asyncio
    async def test_initialize_creates_table_and_first_key(self, adapter):
        mgr = KeyRingManager(adapter=adapter, key_size=2048)
        await mgr.initialize()
        # Should have exactly one key
        rows = await adapter.fetch_all("SELECT * FROM signing_keys")
        assert len(rows) == 1

    @pytest.mark.asyncio
    async def test_initialize_idempotent(self, adapter):
        mgr = KeyRingManager(adapter=adapter, key_size=2048)
        await mgr.initialize()
        await mgr.initialize()
        rows = await adapter.fetch_all("SELECT * FROM signing_keys")
        assert len(rows) == 1

    @pytest.mark.asyncio
    async def test_default_retention_is_interval_plus_ttl(self):
        mgr = KeyRingManager(
            adapter=None,
            rotation_interval=100,
            token_ttl=50,
        )
        assert mgr.retention_period == 150


class TestKeyRingManagerActiveKey:
    @pytest.mark.asyncio
    async def test_returns_kid_and_private_key(self, manager):
        kid, private_key = await manager.active_key()
        assert kid.startswith("key-")
        # Should be an RSA private key object
        assert hasattr(private_key, "sign")

    @pytest.mark.asyncio
    async def test_same_key_on_repeated_calls(self, manager):
        kid1, _ = await manager.active_key()
        kid2, _ = await manager.active_key()
        assert kid1 == kid2


class TestKeyRingManagerRotation:
    @pytest.mark.asyncio
    async def test_no_rotation_when_key_is_fresh(self, manager):
        rotated = await manager.rotate_if_needed()
        assert rotated is False

    @pytest.mark.asyncio
    async def test_rotation_when_key_is_old(self, adapter):
        mgr = KeyRingManager(
            adapter=adapter,
            key_size=2048,
            rotation_interval=1,  # 1 second
            token_ttl=30,
        )
        await mgr.initialize()

        kid_before, _ = await mgr.active_key()

        # Wait for key to age past rotation interval
        await asyncio.sleep(1.1)

        rotated = await mgr.rotate_if_needed()
        assert rotated is True

        kid_after, _ = await mgr.active_key()
        assert kid_before != kid_after

    @pytest.mark.asyncio
    async def test_both_keys_in_jwks_after_rotation(self, adapter):
        mgr = KeyRingManager(
            adapter=adapter,
            key_size=2048,
            rotation_interval=1,
            token_ttl=30,
        )
        await mgr.initialize()
        kid_before, _ = await mgr.active_key()

        await asyncio.sleep(1.1)
        await mgr.rotate_if_needed()
        kid_after, _ = await mgr.active_key()

        jwks = await mgr.jwks_dict()
        kids_in_jwks = {k["kid"] for k in jwks["keys"]}
        assert kid_before in kids_in_jwks
        assert kid_after in kids_in_jwks


class TestKeyRingManagerJWKS:
    @pytest.mark.asyncio
    async def test_jwks_has_one_key_initially(self, manager):
        jwks = await manager.jwks_dict()
        assert len(jwks["keys"]) == 1
        key = jwks["keys"][0]
        assert key["use"] == "sig"
        assert key["alg"] == "RS256"
        assert "kid" in key

    @pytest.mark.asyncio
    async def test_jwks_excludes_expired_keys(self, adapter):
        mgr = KeyRingManager(
            adapter=adapter,
            key_size=2048,
            rotation_interval=1,
            retention_period=2,
            token_ttl=1,
        )
        await mgr.initialize()

        # Force-expire the first key by updating expires_at
        await adapter.execute(
            "UPDATE signing_keys SET expires_at = :exp",
            {"exp": (datetime.now(UTC) - timedelta(seconds=1)).isoformat()},
        )

        jwks = await mgr.jwks_dict()
        assert len(jwks["keys"]) == 0


class TestKeyRingManagerCleanup:
    @pytest.mark.asyncio
    async def test_cleanup_removes_expired_keys(self, adapter):
        mgr = KeyRingManager(
            adapter=adapter,
            key_size=2048,
            rotation_interval=60,
            token_ttl=30,
        )
        await mgr.initialize()

        # Force-expire the key
        await adapter.execute(
            "UPDATE signing_keys SET expires_at = :exp",
            {"exp": (datetime.now(UTC) - timedelta(seconds=1)).isoformat()},
        )

        removed = await mgr.cleanup_expired()
        assert removed == 1

        rows = await adapter.fetch_all("SELECT * FROM signing_keys")
        assert len(rows) == 0

    @pytest.mark.asyncio
    async def test_cleanup_keeps_active_keys(self, manager):
        removed = await manager.cleanup_expired()
        assert removed == 0

        rows = await manager.adapter.fetch_all("SELECT * FROM signing_keys")
        assert len(rows) == 1


class TestKeyRingManagerSignAndVerify:
    """Integration test: sign a token with KeyRingManager, verify with public key."""

    @pytest.mark.asyncio
    async def test_sign_and_verify_round_trip(self, manager):
        import jwt as pyjwt

        kid, private_key = await manager.active_key()

        # Sign a token
        token = pyjwt.encode(
            {"sub": "test-user", "authorities": ["ADMIN"]},
            private_key,
            algorithm="RS256",
            headers={"kid": kid},
        )

        # Get the public key from JWKS
        jwks = await manager.jwks_dict()
        jwk_data = jwks["keys"][0]

        # Verify the token using the public key from JWKS
        from jwt.algorithms import RSAAlgorithm

        public_key = RSAAlgorithm.from_jwk(jwk_data)
        payload = pyjwt.decode(token, public_key, algorithms=["RS256"])
        assert payload["sub"] == "test-user"
        assert payload["authorities"] == ["ADMIN"]
