"""Automatic signing key lifecycle management for JWT issuance.

``KeyRingManager`` generates, rotates, and serves RSA (or EC) signing
keys.  Keys are stored in a database table and exposed via a JWKS
endpoint.  Consumers discover keys automatically using the existing
``JWKSKeyProvider``.
"""

import logging
import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)


def _generate_rsa_keypair(key_size: int = 2048) -> tuple[bytes, bytes]:
    """Generate an RSA keypair and return (private_pem, public_pem)."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def _public_pem_to_jwk(public_pem: bytes, kid: str, algorithm: str) -> dict[str, str]:
    """Convert a PEM-encoded public key to a JWK dict."""
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from jwt.algorithms import RSAAlgorithm

    public_key = load_pem_public_key(public_pem)
    jwk: dict[str, Any] = RSAAlgorithm.to_jwk(public_key, as_dict=True)  # type: ignore[call-overload]
    jwk["kid"] = kid
    jwk["use"] = "sig"
    jwk["alg"] = algorithm
    return jwk


def _load_private_key(private_pem: bytes) -> Any:
    """Load a PEM-encoded private key for signing."""
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    return load_pem_private_key(private_pem, password=None)


_CREATE_TABLE_SQL = """\
CREATE TABLE IF NOT EXISTS signing_keys (
    kid         VARCHAR(255) PRIMARY KEY,
    private_key TEXT NOT NULL,
    public_key  TEXT NOT NULL,
    algorithm   VARCHAR(32) NOT NULL DEFAULT 'RS256',
    created_at  TEXT NOT NULL,
    expires_at  TEXT NOT NULL
)"""

_DROP_TABLE_SQL = "DROP TABLE IF EXISTS signing_keys"

#: Migration-compatible schema definitions for use with ``csrd.migration``.
#: The generated auth service template should include this in its migrations
#: list so the schema is tracked alongside user/credential tables::
#:
#:     from csrd.migration import Migration
#:     from csrd.auth import SIGNING_KEYS_MIGRATION
#:
#:     migrations = [
#:         SIGNING_KEYS_MIGRATION,
#:         Migration(version="002", description="users table", up=..., down=...),
#:     ]
SIGNING_KEYS_MIGRATION_UP = _CREATE_TABLE_SQL.replace("IF NOT EXISTS ", "")
SIGNING_KEYS_MIGRATION_DOWN = _DROP_TABLE_SQL


@dataclass
class SigningKey:
    """In-memory representation of a signing key from the key ring."""

    kid: str
    private_pem: bytes
    public_pem: bytes
    algorithm: str
    created_at: datetime
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        return datetime.now(UTC) >= self.expires_at


@dataclass
class KeyRingManager:
    """Manages RSA signing key lifecycle: generation, rotation, JWKS.

    Parameters
    ----------
    adapter:
        A connected database adapter (any ``DBProtocol`` implementation).
        The adapter must support ``execute``, ``fetch_one``, and
        ``fetch_all``.
    algorithm:
        JWT signing algorithm. Default ``RS256``.
    key_size:
        RSA key size in bits. Default ``2048``.
    rotation_interval:
        Seconds between key rotations. Default ``86400`` (24 hours).
    retention_period:
        Seconds to keep old keys in JWKS after rotation. Must be >=
        ``rotation_interval + token_ttl``.  When *None*, defaults to
        ``rotation_interval + token_ttl``.
    token_ttl:
        Token lifetime in seconds, used to compute default retention.
        Default ``3600`` (1 hour).
    """

    adapter: Any
    algorithm: str = "RS256"
    key_size: int = 2048
    rotation_interval: int = 86400
    retention_period: int | None = None
    token_ttl: int = 3600

    _initialized: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.retention_period is None:
            self.retention_period = self.rotation_interval + self.token_ttl

    @property
    def _effective_retention(self) -> int:
        return self.retention_period or (self.rotation_interval + self.token_ttl)

    async def initialize(self) -> None:
        """Create the signing_keys table and generate the first key if empty.

        Safe to call multiple times — uses ``CREATE TABLE IF NOT EXISTS``.
        """
        await self.adapter.execute(_CREATE_TABLE_SQL)
        self._initialized = True

        active = await self._fetch_active_key()
        if active is None:
            logger.info("No signing keys found — generating initial key")
            await self._generate_and_store()

    async def active_key(self) -> tuple[str, Any]:
        """Return ``(kid, private_key_object)`` for the current signing key.

        The active key is the most recently created non-expired key.
        """
        key = await self._fetch_active_key()
        if key is None:
            logger.warning("No active signing key — generating emergency key")
            key = await self._generate_and_store()
        return key.kid, _load_private_key(key.private_pem)

    async def rotate_if_needed(self) -> bool:
        """Generate a new key if the active key exceeds the rotation interval.

        Returns ``True`` if a new key was generated.
        """
        key = await self._fetch_active_key()
        if key is None:
            await self._generate_and_store()
            return True

        age = (datetime.now(UTC) - key.created_at).total_seconds()
        if age >= self.rotation_interval:
            logger.info(
                "Active key %s is %.0fs old (interval=%ds) — rotating",
                key.kid,
                age,
                self.rotation_interval,
            )
            await self._generate_and_store()
            return True

        return False

    async def jwks_dict(self) -> dict[str, list[dict[str, str]]]:
        """Return a JWKS payload containing all non-expired public keys.

        This response is suitable for serving at
        ``/.well-known/jwks.json``.
        """
        keys = await self._fetch_all_active_keys()
        jwk_list = [_public_pem_to_jwk(k.public_pem, k.kid, k.algorithm) for k in keys]
        return {"keys": jwk_list}

    async def cleanup_expired(self) -> int:
        """Remove keys that have passed their retention period.

        Returns the number of keys removed.
        """
        now_iso = datetime.now(UTC).isoformat()
        count: int = await self.adapter.execute(
            "DELETE FROM signing_keys WHERE expires_at < :now",
            {"now": now_iso},
        )
        if count > 0:
            logger.info("Cleaned up %d expired signing key(s)", count)
        return count

    async def _generate_and_store(self) -> SigningKey:
        """Generate a new keypair and persist it."""
        kid = f"key-{uuid.uuid4().hex[:12]}"
        private_pem, public_pem = _generate_rsa_keypair(self.key_size)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._effective_retention)

        await self.adapter.execute(
            "INSERT INTO signing_keys (kid, private_key, public_key, algorithm, created_at, expires_at) "
            "VALUES (:kid, :private_key, :public_key, :algorithm, :created_at, :expires_at)",
            {
                "kid": kid,
                "private_key": private_pem.decode(),
                "public_key": public_pem.decode(),
                "algorithm": self.algorithm,
                "created_at": now.isoformat(),
                "expires_at": expires_at.isoformat(),
            },
        )

        key = SigningKey(
            kid=kid,
            private_pem=private_pem,
            public_pem=public_pem,
            algorithm=self.algorithm,
            created_at=now,
            expires_at=expires_at,
        )
        logger.info("Generated new signing key: kid=%s, expires=%s", kid, expires_at.isoformat())
        return key

    async def _fetch_active_key(self) -> SigningKey | None:
        """Fetch the most recently created non-expired key."""
        now_iso = datetime.now(UTC).isoformat()
        row = await self.adapter.fetch_one(
            "SELECT kid, private_key, public_key, algorithm, created_at, expires_at "
            "FROM signing_keys "
            "WHERE expires_at >= :now "
            "ORDER BY created_at DESC "
            "LIMIT 1",
            {"now": now_iso},
        )
        return self._row_to_key(row) if row else None

    async def _fetch_all_active_keys(self) -> list[SigningKey]:
        """Fetch all non-expired keys, newest first."""
        now_iso = datetime.now(UTC).isoformat()
        rows: Sequence[dict[str, Any]] = await self.adapter.fetch_all(
            "SELECT kid, private_key, public_key, algorithm, created_at, expires_at "
            "FROM signing_keys "
            "WHERE expires_at >= :now "
            "ORDER BY created_at DESC",
            {"now": now_iso},
        )
        return [self._row_to_key(row) for row in rows if row]

    @staticmethod
    def _row_to_key(row: dict[str, Any]) -> SigningKey:
        """Convert a database row to a ``SigningKey``."""
        return SigningKey(
            kid=str(row["kid"]),
            private_pem=str(row["private_key"]).encode(),
            public_pem=str(row["public_key"]).encode(),
            algorithm=str(row["algorithm"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            expires_at=datetime.fromisoformat(str(row["expires_at"])),
        )
