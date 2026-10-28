"""Native crypto for content tokens and envelope encryption.

Hand-written drop-in for the pieces of ``istari_digital_core`` the client used:
salted-SHA-384 content tokens and RSA+AES envelope encryption. Pure Python via
``cryptography`` (already a client dependency) so there is no compiled Rust core.
FIPS is provided by Istari's custom-built ``cryptography`` at install time, not by
this code: see ``FIPS.md`` and ``fips_check``.

The wire format and digest are a byte-for-byte contract shared with the backend
(``fileservice2/credential/agentcrypto.py``) and the agent decryptor. Do not change
them without updating those and the golden vectors in both repos.

Token digest::

    sha = SHA384(content ‖ salt.encode("utf-8"))   # salt appended last, lowercase hex

Envelope wire format (big-endian)::

    u16(len(enc_key)) | enc_key | nonce[12] | aes_ciphertext+gcm_tag[16]
"""

from __future__ import annotations

import hashlib
import hmac
import os
import uuid
from typing import NamedTuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_NONCE_LENGTH = 12  # 96-bit GCM nonce, per NIST SP 800-38D
_KEY_LENGTH_PREFIX = 2  # bytes of the big-endian u16 holding len(enc_key)
_MIN_RSA_BITS = 2048
_OAEP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)


def _digest(data: bytes, salt: str) -> str:
    """Return the lowercase-hex SHA-384 of ``data`` with ``salt`` appended last."""
    h = hashlib.sha384()
    h.update(data)
    h.update(salt.encode("utf-8"))
    return h.hexdigest()


class Token(NamedTuple):
    """A content token: the salted SHA-384 digest and the salt that produced it."""

    sha: str
    salt: str

    @classmethod
    def from_bytes(cls, data: bytes, salt: str | None = None) -> Token:
        """Hash ``data`` with ``salt`` (random UUID4 hex if omitted)."""
        if salt is None:
            salt = (
                uuid.uuid4().hex
            )  # 32 lowercase hex, no dashes (Rust Uuid::as_simple)
        return cls(sha=_digest(data, salt), salt=salt)

    @classmethod
    def compare_token(cls, sha: str, salt: str, data: bytes) -> None:
        """Raise ``ValueError`` if ``data`` does not hash to ``sha`` under ``salt``."""
        if not hmac.compare_digest(_digest(data, salt), sha):
            raise ValueError("Token mismatch")


class Hasher:
    """Incrementally hash content, appending the UTF-8 salt only at finalization."""

    def __init__(self, salt: str | None = None) -> None:
        """Start a SHA-384 digest with an explicit or randomly generated salt."""
        self.salt = uuid.uuid4().hex if salt is None else salt
        self._hash = hashlib.sha384()

    def update(self, data: bytes | bytearray | memoryview) -> None:
        """Add the next content chunk without retaining its buffer."""
        self._hash.update(data)

    def finalize(self) -> Token:
        """Return the salted token without changing the accumulated content digest."""
        digest = self._hash.copy()
        digest.update(self.salt.encode("utf-8"))
        return Token(sha=digest.hexdigest(), salt=self.salt)


class VerifyingHasher:
    """Incrementally verify content against an expected salted SHA-384 token."""

    def __init__(self, sha: str, salt: str) -> None:
        """Start verification using the expected digest and salt."""
        self._sha = sha
        self._hasher = Hasher(salt)

    def update(self, data: bytes | bytearray | memoryview) -> None:
        """Add the next content chunk without retaining its buffer."""
        self._hasher.update(data)

    def finalize(self) -> None:
        """Raise ``ValueError`` if the accumulated content does not match."""
        if not hmac.compare_digest(self._hasher.finalize().sha, self._sha):
            raise ValueError("Token mismatch")


def compare_hash(sha: str, salt: str, data: bytes) -> bool:
    """Return whether ``data`` hashes to ``sha`` under ``salt``."""
    return hmac.compare_digest(_digest(data, salt), sha)


def encrypt(public_key_pem: bytes, plaintext: bytes) -> bytes:
    """Envelope-encrypt ``plaintext`` to an RSA public key (PKCS#1 or SPKI PEM).

    AES-256-GCM over the payload, RSA-OAEP-SHA256 wrapping the per-message AES key.
    All FIPS-approved primitives. Returns the wire format documented above.

    :raises TypeError: if the PEM is not an RSA public key.
    :raises ValueError: if the key is under 2048 bits, or the wrapped key overflows the u16 prefix.
    """
    public_key = serialization.load_pem_public_key(public_key_pem)
    if not isinstance(public_key, RSAPublicKey):
        raise TypeError("Provided public key is not an RSA public key")
    if public_key.key_size < _MIN_RSA_BITS:
        raise ValueError(
            f"RSA key too small: {public_key.key_size} < {_MIN_RSA_BITS} bits"
        )

    aes_key = os.urandom(32)
    nonce = os.urandom(_NONCE_LENGTH)
    encryptor = Cipher(algorithms.AES(aes_key), modes.GCM(nonce)).encryptor()
    aes_ciphertext = encryptor.update(plaintext) + encryptor.finalize() + encryptor.tag

    enc_key = public_key.encrypt(aes_key, _OAEP)
    if len(enc_key) >= 2 ** (8 * _KEY_LENGTH_PREFIX):
        raise ValueError("Encrypted session key is unexpectedly large")

    return (
        len(enc_key).to_bytes(_KEY_LENGTH_PREFIX, "big")
        + enc_key
        + nonce
        + aes_ciphertext
    )
