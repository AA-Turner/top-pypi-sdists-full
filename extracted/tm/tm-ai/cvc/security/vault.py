"""
cvc.security.vault — AES-GCM encrypted vault for the soul's data at rest.

Threat model: an attacker gains local filesystem access (laptop stolen,
backup stolen, malware). Without the passphrase, every encrypted blob is
opaque. With it, the owner decrypts transparently.

Crypto:
  - Key derivation : scrypt(passphrase, salt) — stdlib, no extra deps
  - Symmetric      : AES-256-GCM (authenticated encryption)
  - Per-blob nonce : 96-bit random
  - Header format  : magic(4) + version(1) + salt(16) + nonce(12) + ct(N) + tag(16)

The vault is locked by default. Reading requires unlock() with the passphrase.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b"CVCV"
VERSION = 1
SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32  # AES-256
SCRYPT_N = 2 ** 14  # ~16 MiB cost — sane default for desktop, tune up for prod
SCRYPT_R = 8
SCRYPT_P = 1


class VaultLocked(RuntimeError):
    """Raised when an operation requires unlock() first."""


@dataclass
class VaultUnlocked:
    """A handle returned by SoulVault.unlock() — holds the derived key."""

    key: bytes
    path: Path

    def encrypt(self, plaintext: bytes, *, aad: bytes = b"") -> bytes:
        """Encrypt + authenticate. Returns the framed ciphertext."""
        nonce = secrets.token_bytes(NONCE_LEN)
        aesgcm = AESGCM(self.key)
        ct = aesgcm.encrypt(nonce, plaintext, aad or None)
        return MAGIC + struct.pack("B", VERSION) + nonce + ct

    def decrypt(self, framed: bytes, *, aad: bytes = b"") -> bytes:
        """Decrypt + verify. Raises on tampering or wrong key."""
        if framed[:4] != MAGIC:
            raise ValueError("not a vault frame (bad magic)")
        version = framed[4]
        if version != VERSION:
            raise ValueError(f"unsupported vault version: {version}")
        nonce = framed[5 : 5 + NONCE_LEN]
        ct = framed[5 + NONCE_LEN :]
        aesgcm = AESGCM(self.key)
        return aesgcm.decrypt(nonce, ct, aad or None)


class SoulVault:
    """
    Manages the soul's encrypted storage.

    Usage:
        vault = SoulVault(Path("~/.cvc/vault").expanduser())
        unlocked = vault.unlock("correct horse battery staple")
        ciphertext = unlocked.encrypt(b"my soul")
        plaintext = unlocked.decrypt(ciphertext)

    File layout:
        vault_dir/
            meta.json      — {kdf_params, salt_b64, fingerprint, created_at}
            blobs/         — opaque *.cvcv files (encrypted)
    """

    def __init__(self, vault_dir: Path) -> None:
        self.vault_dir = Path(vault_dir)
        self.blobs_dir = self.vault_dir / "blobs"
        self.meta_path = self.vault_dir / "meta.json"
        self._unlocked: VaultUnlocked | None = None

    # ── state ──────────────────────────────────────────────────────────

    @property
    def is_initialized(self) -> bool:
        return self.meta_path.exists()

    @property
    def is_unlocked(self) -> bool:
        return self._unlocked is not None

    def status(self) -> dict[str, Any]:
        return {
            "initialized": self.is_initialized,
            "unlocked": self.is_unlocked,
            "blobs": len(list(self.blobs_dir.glob("*.cvcv"))) if self.blobs_dir.exists() else 0,
            "vault_dir": str(self.vault_dir),
            "kdf": "scrypt",
            "kdf_params": {"N": SCRYPT_N, "r": SCRYPT_R, "p": SCRYPT_P},
            "cipher": "AES-256-GCM",
        }

    # ── init / unlock / lock ──────────────────────────────────────────

    def initialize(self, passphrase: str) -> VaultUnlocked:
        """Create a fresh vault. Idempotent on existing meta."""
        if not passphrase or len(passphrase) < 8:
            raise ValueError("passphrase must be at least 8 characters")

        salt = secrets.token_bytes(SALT_LEN)
        key = self._derive_key(passphrase, salt)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.blobs_dir.mkdir(parents=True, exist_ok=True)

        fingerprint = hashlib.sha256(key).hexdigest()[:16]
        import json, time

        if not self.meta_path.exists():
            self.meta_path.write_text(
                json.dumps(
                    {
                        "version": VERSION,
                        "kdf": "scrypt",
                        "kdf_params": {"N": SCRYPT_N, "r": SCRYPT_R, "p": SCRYPT_P},
                        "salt_b64": salt.hex(),
                        "fingerprint": fingerprint,
                        "created_at": time.time(),
                    }
                ),
                encoding="utf-8",
            )
        self._unlocked = VaultUnlocked(key=key, path=self.vault_dir)
        return self._unlocked

    def unlock(self, passphrase: str) -> VaultUnlocked:
        """Open an existing vault. Verifies the passphrase via fingerprint."""
        import json

        if not self.meta_path.exists():
            raise VaultLocked("vault not initialized — call initialize() first")

        meta = json.loads(self.meta_path.read_text(encoding="utf-8"))
        salt = bytes.fromhex(meta["salt_b64"])
        params = meta.get("kdf_params", {})
        key = self._derive_key(
            passphrase,
            salt,
            n=params.get("N", SCRYPT_N),
            r=params.get("r", SCRYPT_R),
            p=params.get("p", SCRYPT_P),
        )
        fp = hashlib.sha256(key).hexdigest()[:16]
        if fp != meta.get("fingerprint"):
            raise VaultLocked("wrong passphrase")
        self._unlocked = VaultUnlocked(key=key, path=self.vault_dir)
        return self._unlocked

    def lock(self) -> None:
        """Zero the key and require unlock() again."""
        if self._unlocked is not None:
            # best-effort zero (CPython may keep copies; this is the standard mitigation)
            self._unlocked.key = b"\x00" * KEY_LEN
        self._unlocked = None

    # ── blob operations ────────────────────────────────────────────────

    def require(self) -> VaultUnlocked:
        if not self._unlocked:
            raise VaultLocked("soul vault is locked — call unlock() first")
        return self._unlocked

    def write_blob(self, name: str, plaintext: bytes) -> Path:
        """Encrypt `plaintext` and write to blobs/<name>.cvcv."""
        u = self.require()
        self.blobs_dir.mkdir(parents=True, exist_ok=True)
        path = self.blobs_dir / f"{name}.cvcv"
        path.write_bytes(u.encrypt(plaintext, aad=name.encode("utf-8")))
        return path

    def read_blob(self, name: str) -> bytes:
        u = self.require()
        path = self.blobs_dir / f"{name}.cvcv"
        return u.decrypt(path.read_bytes(), aad=name.encode("utf-8"))

    def list_blobs(self) -> list[str]:
        if not self.blobs_dir.exists():
            return []
        return sorted(p.stem for p in self.blobs_dir.glob("*.cvcv"))

    # ── internals ──────────────────────────────────────────────────────

    @staticmethod
    def _derive_key(
        passphrase: str,
        salt: bytes,
        *,
        n: int = SCRYPT_N,
        r: int = SCRYPT_R,
        p: int = SCRYPT_P,
    ) -> bytes:
        return hashlib.scrypt(
            passphrase.encode("utf-8"),
            salt=salt,
            n=n,
            r=r,
            p=p,
            dklen=KEY_LEN,
        )