"""Streaming AES-256-GCM over the archive bytes, binding the manifest header as AAD
(S3 §3.1, §5.2 V3).

The whole profile is never held in memory: encrypt reads the plaintext archive in
8 MiB chunks and writes ciphertext to a temp file, hashing the ciphertext as it is
produced; decrypt streams the ciphertext back and verifies the GCM tag on finalize.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .constants import ARCHIVE_CHUNK_BYTES, DEK_BYTES, GCM_NONCE_BYTES
from .errors import CaptureError, VerificationError


@dataclass(frozen=True)
class EncryptResult:
    path: Path
    content_hash: str  # sha256 of the ciphertext, lowercase hex
    byte_count: int
    tag: bytes  # 16-byte GCM tag


def encrypt_archive(
    plaintext_path: Path, dest_path: Path, dek: bytes, nonce: bytes, aad: bytes
) -> EncryptResult:
    if len(dek) != DEK_BYTES:
        raise CaptureError(f"DEK must be {DEK_BYTES} bytes", code="encrypt_failed")
    if len(nonce) != GCM_NONCE_BYTES:
        raise CaptureError(f"nonce must be {GCM_NONCE_BYTES} bytes", code="encrypt_failed")

    hasher = hashlib.sha256()
    total = 0
    encryptor = Cipher(algorithms.AES(dek), modes.GCM(nonce)).encryptor()
    encryptor.authenticate_additional_data(aad)

    fd = os.open(dest_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "wb") as out, open(plaintext_path, "rb") as src:
            while True:
                block = src.read(ARCHIVE_CHUNK_BYTES)
                if not block:
                    break
                ct = encryptor.update(block)
                if ct:
                    hasher.update(ct)
                    total += len(ct)
                    out.write(ct)
            final = encryptor.finalize()
            if final:
                hasher.update(final)
                total += len(final)
                out.write(final)
    except Exception as exc:
        dest_path.unlink(missing_ok=True)
        raise CaptureError(f"encrypt failed: {exc}", code="encrypt_failed") from exc

    return EncryptResult(
        path=dest_path,
        content_hash=hasher.hexdigest(),
        byte_count=total,
        tag=encryptor.tag,
    )


def decrypt_stream_to_file(
    ciphertext: BinaryIO,
    dest_path: Path,
    dek: bytes,
    nonce: bytes,
    aad: bytes,
    tag: bytes,
) -> tuple[str, int]:
    """Stream-decrypt ``ciphertext`` into ``dest_path``; verify the GCM tag on finalize.

    Returns ``(plaintext_hash, plaintext_byte_count)``. Raises ``auth_tag_invalid``
    when the tag does not authenticate — a tampered ciphertext, wrong AAD (a lied
    manifest header), or wrong key all land here.
    """
    hasher = hashlib.sha256()
    total = 0
    decryptor = Cipher(algorithms.AES(dek), modes.GCM(nonce, tag)).decryptor()
    decryptor.authenticate_additional_data(aad)

    fd = os.open(dest_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "wb") as out:
            while True:
                block = ciphertext.read(ARCHIVE_CHUNK_BYTES)
                if not block:
                    break
                pt = decryptor.update(block)
                if pt:
                    hasher.update(pt)
                    total += len(pt)
                    out.write(pt)
            final = decryptor.finalize()  # raises InvalidTag on a bad tag/AAD
            if final:
                hasher.update(final)
                total += len(final)
                out.write(final)
    except Exception as exc:
        dest_path.unlink(missing_ok=True)
        raise VerificationError(
            f"GCM tag did not authenticate: {exc}", code="auth_tag_invalid"
        ) from exc

    return hasher.hexdigest(), total


def zeroize(buf: bytearray) -> None:
    """Best-effort overwrite of secret key material held in a bytearray."""
    for i in range(len(buf)):
        buf[i] = 0
