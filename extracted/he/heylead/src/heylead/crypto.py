"""AES-256-GCM encryption for LinkedIn cookie storage."""

from __future__ import annotations

import hashlib
import logging
import os
import platform
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from . import config

logger = logging.getLogger(__name__)

# Key derivation: SHA-256 of (hostname + username + static salt)
# This ties the encrypted cookie to this specific machine + user.
_SALT = b"heylead-cookie-encryption-v1"


def _derive_key() -> bytes:
    """Derive a 256-bit key from machine identity."""
    identity = f"{platform.node()}:{os.getlogin()}".encode()
    return hashlib.sha256(_SALT + identity).digest()


def encrypt_cookie(cookie: str) -> None:
    """Encrypt and store a LinkedIn cookie."""
    config.ensure_dirs()
    path = config.cookie_path()

    key = _derive_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce for GCM
    ciphertext = aesgcm.encrypt(nonce, cookie.encode("utf-8"), None)

    # Store as: nonce (12 bytes) + ciphertext
    with open(path, "wb") as f:
        f.write(nonce + ciphertext)

    logger.info("LinkedIn cookie encrypted and stored")


def decrypt_cookie() -> str | None:
    """Load and decrypt the stored LinkedIn cookie. Returns None if missing or corrupt."""
    path = config.cookie_path()
    if not path.exists():
        return None

    try:
        with open(path, "rb") as f:
            data = f.read()

        if len(data) < 13:  # 12-byte nonce + at least 1 byte
            logger.warning("Cookie file too small, likely corrupt")
            return None

        nonce = data[:12]
        ciphertext = data[12:]

        key = _derive_key()
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")

    except Exception as e:
        logger.warning(f"Failed to decrypt cookie: {e}")
        return None


def delete_cookie() -> None:
    """Remove stored cookie."""
    path = config.cookie_path()
    if path.exists():
        path.unlink()
        logger.info("LinkedIn cookie deleted")
