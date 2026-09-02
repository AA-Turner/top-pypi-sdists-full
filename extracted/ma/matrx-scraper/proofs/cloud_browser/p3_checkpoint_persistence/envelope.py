"""P3 envelope encryption — PLAN.md "Secure profile storage / Encryption design".

PHASE-0 PROOF HARNESS. NOT SHIPPED CODE.

    #############################################################
    #  THE KMS WRAPPER HERE IS A LOCAL STAND-IN, NOT AWS KMS.   #
    #  This machine has no aws cli and no KMS access.           #
    #  `LocalKmsSubstitute` keeps the AWS KMS interface exactly  #
    #  (generate_data_key / decrypt, both taking an encryption   #
    #  context) so WS-3 can swap in boto3 KMS by replacing ONE   #
    #  class. It provides NO KMS security properties: the master #
    #  key sits in a local file, so there is no HSM, no key      #
    #  policy, no CloudTrail, and no cryptographic erasure by    #
    #  key deletion.                                             #
    #############################################################

What is faithful to PLAN.md:

- random 256-bit DEK per checkpoint;
- AES-256-GCM with a fresh 96-bit nonce over a CLOSED profile archive;
- the KMS encryption context ({profile_id, key_version, purpose} — non-secret only)
  is bound as AES-GCM Additional Authenticated Data on BOTH the DEK wrap and the
  payload, so a wrong context cannot decrypt;
- a manifest recording nonce, wrapped DEK, content hash, byte count, format version
  and Chromium version; never the plaintext DEK;
- verification (hash + byte count) before a restore is accepted — fail closed.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
from dataclasses import dataclass, asdict
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

FORMAT_VERSION = "p3-profile-checkpoint/1"
NONCE_BYTES = 12
DEK_BYTES = 32


def b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode()


def unb64(s: str) -> bytes:
    return base64.b64decode(s)


def context_aad(encryption_context: dict[str, str]) -> bytes:
    """Canonical bytes for an encryption context, exactly as AWS KMS treats it:
    a sorted, non-secret key/value map bound as AAD."""
    return json.dumps(encryption_context, sort_keys=True, separators=(",", ":")).encode()


class KmsUnavailable(Exception):
    pass


class InvalidCiphertext(Exception):
    """Raised where AWS KMS would raise InvalidCiphertextException — which is also
    what KMS raises on a wrong encryption context."""


class LocalKmsSubstitute:
    """KMS-SHAPED STAND-IN. Interface parity with boto3 kms only.

    Real replacement for WS-3:
        kms.generate_data_key(KeyId=..., KeySpec='AES_256', EncryptionContext=ctx)
        kms.decrypt(CiphertextBlob=..., EncryptionContext=ctx)
    """

    IS_REAL_KMS = False

    def __init__(self, master_key_path: Path):
        self.master_key_path = Path(master_key_path)
        if not self.master_key_path.exists():
            self.master_key_path.parent.mkdir(parents=True, exist_ok=True)
            self.master_key_path.write_bytes(secrets.token_bytes(32))
            os.chmod(self.master_key_path, 0o600)
        self._master = self.master_key_path.read_bytes()
        if len(self._master) != 32:
            raise KmsUnavailable("stand-in master key is not 32 bytes")

    def generate_data_key(self, key_id: str, encryption_context: dict[str, str]):
        """-> (plaintext_dek, wrapped_dek). Mirrors KMS GenerateDataKey."""
        dek = secrets.token_bytes(DEK_BYTES)
        nonce = secrets.token_bytes(NONCE_BYTES)
        aad = context_aad({**encryption_context, "__kms_key_id": key_id})
        blob = nonce + AESGCM(self._master).encrypt(nonce, dek, aad)
        return dek, blob

    def decrypt(self, wrapped_dek: bytes, encryption_context: dict[str, str], key_id: str):
        """-> plaintext_dek. Mirrors KMS Decrypt; raises on a wrong context."""
        aad = context_aad({**encryption_context, "__kms_key_id": key_id})
        nonce, ct = wrapped_dek[:NONCE_BYTES], wrapped_dek[NONCE_BYTES:]
        try:
            return AESGCM(self._master).decrypt(nonce, ct, aad)
        except Exception as exc:  # cryptography raises InvalidTag
            raise InvalidCiphertext(
                f"DEK unwrap failed (wrong encryption context, wrong key, or tampered "
                f"wrapped key): {type(exc).__name__}"
            ) from exc


@dataclass
class CheckpointManifest:
    format_version: str
    profile_id: str
    key_version: str
    purpose: str
    kms_key_id: str
    kms_is_real: bool
    encryption_context: dict
    nonce_b64: str
    wrapped_dek_b64: str
    content_sha256: str  # sha256 of the PLAINTEXT archive
    ciphertext_sha256: str  # sha256 of the stored object
    plaintext_bytes: int
    ciphertext_bytes: int
    chromium_version: str
    created_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


class CheckpointVerificationError(Exception):
    """Fail-closed marker. A restore that raises this MUST NOT yield a profile dir."""


def encrypt_checkpoint(
    plaintext_path: Path,
    out_path: Path,
    kms: LocalKmsSubstitute,
    kms_key_id: str,
    profile_id: str,
    key_version: str,
    purpose: str,
    chromium_version: str,
    created_at: str,
) -> CheckpointManifest:
    plaintext = Path(plaintext_path).read_bytes()
    ctx = {"profile_id": profile_id, "key_version": key_version, "purpose": purpose}
    dek, wrapped = kms.generate_data_key(kms_key_id, ctx)
    nonce = secrets.token_bytes(NONCE_BYTES)
    ct = AESGCM(dek).encrypt(nonce, plaintext, context_aad(ctx))
    del dek  # plaintext DEK is never persisted
    Path(out_path).write_bytes(ct)
    return CheckpointManifest(
        format_version=FORMAT_VERSION,
        profile_id=profile_id,
        key_version=key_version,
        purpose=purpose,
        kms_key_id=kms_key_id,
        kms_is_real=kms.IS_REAL_KMS,
        encryption_context=ctx,
        nonce_b64=b64(nonce),
        wrapped_dek_b64=b64(wrapped),
        content_sha256=hashlib.sha256(plaintext).hexdigest(),
        ciphertext_sha256=hashlib.sha256(ct).hexdigest(),
        plaintext_bytes=len(plaintext),
        ciphertext_bytes=len(ct),
        chromium_version=chromium_version,
        created_at=created_at,
    )


def decrypt_checkpoint(
    ciphertext_path: Path,
    manifest: CheckpointManifest,
    out_path: Path,
    kms: LocalKmsSubstitute,
    override_context: dict | None = None,
) -> int:
    """Fail-closed restore. Every failure raises BEFORE out_path is written."""
    ct = Path(ciphertext_path).read_bytes()

    if len(ct) != manifest.ciphertext_bytes:
        raise CheckpointVerificationError(
            f"ciphertext byte count mismatch: stored={len(ct)} "
            f"manifest={manifest.ciphertext_bytes} (truncated or padded object)"
        )
    got_ct_hash = hashlib.sha256(ct).hexdigest()
    if got_ct_hash != manifest.ciphertext_sha256:
        raise CheckpointVerificationError(
            f"ciphertext sha256 mismatch: stored={got_ct_hash} "
            f"manifest={manifest.ciphertext_sha256} (object tampered in transit/at rest)"
        )

    ctx = override_context if override_context is not None else manifest.encryption_context
    dek = kms.decrypt(unb64(manifest.wrapped_dek_b64), ctx, manifest.kms_key_id)
    try:
        pt = AESGCM(dek).decrypt(unb64(manifest.nonce_b64), ct, context_aad(ctx))
    except Exception as exc:
        raise CheckpointVerificationError(
            f"AES-256-GCM authentication failed: {type(exc).__name__} "
            f"(ciphertext tampered, nonce wrong, or encryption context mismatched)"
        ) from exc
    finally:
        del dek

    got = hashlib.sha256(pt).hexdigest()
    if got != manifest.content_sha256:
        raise CheckpointVerificationError(
            f"plaintext content sha256 mismatch: got={got} "
            f"manifest={manifest.content_sha256} (manifest does not describe this object)"
        )
    if len(pt) != manifest.plaintext_bytes:
        raise CheckpointVerificationError(
            f"plaintext byte count mismatch: got={len(pt)} manifest={manifest.plaintext_bytes}"
        )
    Path(out_path).write_bytes(pt)
    return len(pt)
