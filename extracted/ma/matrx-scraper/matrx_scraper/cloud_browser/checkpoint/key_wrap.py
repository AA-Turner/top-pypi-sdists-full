"""Key-wrap providers — the ONE seam that keeps the engine identical under AWS KMS
and under a local KMS stand-in (S3 §9).

The engine never branches on ``production``. It calls a :class:`KeyWrapProvider`,
records ``wrap_alg`` + ``kms_key_id`` in the manifest, and everything else (archive,
GCM, AAD, hashes, verification, restore, fallback) is byte-identical in both modes.

Three guards keep the local provider out of production (S3 §9.3):
1. construction refusal outside local/test;
2. a loud self-identifying warning on every wrap;
3. restore refusal (R9) of any ``local-dev-*`` wrap on a real deployment.

Selection is by explicit host injection — ``configure_checkpoint_key_wrapping`` —
matching the package rule that a package accepts host objects rather than reading
the host's environment. With nothing injected the engine builds a
:class:`KmsKeyWrapProvider` and fails LOUD if it is unconfigured.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Protocol, runtime_checkable

from .constants import (
    CHECKPOINT_KMS_KEY_ENV,
    KEY_VERSION,
    WRAP_ALG_KMS,
    WRAP_ALG_LOCAL_DEV,
)
from .errors import (
    CheckpointError,
    CheckpointKmsNotConfiguredError,
    LocalDevProviderRefusedError,
)

logger = logging.getLogger(__name__)


@runtime_checkable
class KeyWrapProvider(Protocol):
    """Wrap / unwrap a symmetric DEK, binding an encryption context.

    ``wrap`` returns ``(wrapped_blob, key_id_or_None)``. ``unwrap`` must reproduce
    the exact plaintext DEK and must REFUSE when the passed context differs from the
    one bound at wrap time (KMS enforces this natively; the local provider emulates it).
    """

    wrap_alg: str

    def wrap(self, dek: bytes, context: dict[str, str]) -> tuple[bytes, str | None]: ...

    def unwrap(self, wrapped: bytes, context: dict[str, str]) -> bytes: ...


def _validate_context(context: dict[str, str]) -> None:
    if set(context.keys()) != {"profile_id", "key_version", "purpose"}:
        raise CheckpointError(
            f"encryption context must have exactly keys "
            f"{{profile_id, key_version, purpose}}, got {sorted(context)}",
            code="wrap_context_mismatch",
        )
    if context["key_version"] != KEY_VERSION:
        raise CheckpointError(
            f"key_version must be {KEY_VERSION!r}, got {context['key_version']!r}",
            code="wrap_context_mismatch",
        )
    for k, v in context.items():
        if not isinstance(v, str):
            raise CheckpointError(
                f"encryption-context value for {k!r} must be a string (KMS requires it)",
                code="wrap_context_mismatch",
            )


class LocalDevKeyWrapProvider:
    """Local KMS stand-in — wraps the DEK with the platform's ONE symmetric primitive
    (the secrets battery Fernet), never a second key or a second Fernet instance.

    Fernet carries no AAD, so the encryption-context binding is reproduced by
    prefixing the canonical context JSON inside the wrapped plaintext and rejecting
    an unwrap whose embedded context differs — so a wrong-context unwrap fails here
    exactly as KMS would.
    """

    wrap_alg = WRAP_ALG_LOCAL_DEV

    def __init__(self, *, allow_outside_local: bool = False) -> None:
        # Guard 1 — construction refusal. Host identity, not a flag (S3 §9.3).
        if not allow_outside_local:
            try:
                from matrx_utils import get_runtime_env

                env = get_runtime_env()
                if not (env.is_local or env.is_test):
                    raise LocalDevProviderRefusedError(
                        "LocalDevKeyWrapProvider may only be constructed on a local "
                        f"or test host; runtime stage is {env.stage!r}. A real "
                        "deployment MUST use KmsKeyWrapProvider."
                    )
            except LocalDevProviderRefusedError:
                raise
            except Exception:  # matrx_utils unavailable in a truly bare venv
                logger.warning(
                    "[checkpoint] runtime env unavailable; allowing "
                    "LocalDevKeyWrapProvider only because allow_outside_local was "
                    "not requested and no host identity could be read."
                )

    def _fernet_pair(self):
        from matrx_orm.secrets_battery.crypto import decrypt_bytes, encrypt_bytes

        return encrypt_bytes, decrypt_bytes

    def wrap(self, dek: bytes, context: dict[str, str]) -> tuple[bytes, str | None]:
        _validate_context(context)
        encrypt_bytes, _ = self._fernet_pair()
        ctx_bytes = json.dumps(context, sort_keys=True, separators=(",", ":")).encode()
        # length-prefixed context || dek, then Fernet over the whole thing
        framed = len(ctx_bytes).to_bytes(4, "big") + ctx_bytes + dek
        # Guard 2 — loud self-identifying banner on every wrap (S3 §9.3).
        logger.warning(
            "[checkpoint] LOCAL-DEV key wrap in use (%s) for profile_id=%s — this "
            "checkpoint is NOT a production checkpoint and any real deployment will "
            "refuse to restore it.",
            self.wrap_alg,
            context.get("profile_id"),
        )
        return encrypt_bytes(framed), None

    def unwrap(self, wrapped: bytes, context: dict[str, str]) -> bytes:
        _validate_context(context)
        _, decrypt_bytes = self._fernet_pair()
        framed = decrypt_bytes(wrapped)
        clen = int.from_bytes(framed[:4], "big")
        embedded = framed[4 : 4 + clen]
        dek = framed[4 + clen :]
        want = json.dumps(context, sort_keys=True, separators=(",", ":")).encode()
        if embedded != want:
            raise CheckpointError(
                "local-dev unwrap context mismatch (embedded context differs from "
                "the context passed to unwrap)",
                code="wrap_context_mismatch",
            )
        return dek


class KmsKeyWrapProvider:
    """AWS KMS symmetric wrap/unwrap of the DEK with encryption context (S3 §3.2).

    Uses ``kms.Encrypt`` on a locally generated DEK (not ``GenerateDataKey``) so the
    engine's one code path is identical to the local provider — see the design note
    in the S3 contract. Loud when unconfigured; never a silent fallback.
    """

    wrap_alg = WRAP_ALG_KMS

    def __init__(self, *, key_id: str | None = None, kms_client: object | None = None) -> None:
        resolved = key_id or os.environ.get(CHECKPOINT_KMS_KEY_ENV)
        if not resolved:
            raise CheckpointKmsNotConfiguredError(
                "checkpoint KMS key is not configured — set the env var "
                f"{CHECKPOINT_KMS_KEY_ENV} to a symmetric ENCRYPT_DECRYPT KMS key "
                "id/ARN/alias, or inject a LocalDevKeyWrapProvider for local dev. "
                "This is a VALUE, never a toggle, and there is NO silent local fallback."
            )
        self.key_id = resolved
        self._client = kms_client

    def _kms(self) -> object:
        if self._client is None:
            # Reuse the platform's boto3 client factory when present.
            try:
                from matrx_files.cloud_sync.boto import (  # type: ignore
                    get_boto3_service_client,
                )

                self._client = get_boto3_service_client("kms")
            except Exception:
                import boto3  # type: ignore

                self._client = boto3.client("kms")
        return self._client

    def wrap(self, dek: bytes, context: dict[str, str]) -> tuple[bytes, str | None]:
        _validate_context(context)
        resp = self._kms().encrypt(  # type: ignore[attr-defined]
            KeyId=self.key_id, Plaintext=dek, EncryptionContext=context
        )
        return resp["CiphertextBlob"], self.key_id

    def unwrap(self, wrapped: bytes, context: dict[str, str]) -> bytes:
        _validate_context(context)
        try:
            resp = self._kms().decrypt(  # type: ignore[attr-defined]
                CiphertextBlob=wrapped, EncryptionContext=context, KeyId=self.key_id
            )
        except Exception as exc:  # KMS refusal, wrong context, wrong key
            raise CheckpointError(
                f"KMS could not unwrap the DEK: {exc}", code="dek_unwrap_failed"
            ) from exc
        return resp["Plaintext"]


# ── Host injection registry ──────────────────────────────────────────────
_PROVIDER: KeyWrapProvider | None = None


def configure_checkpoint_key_wrapping(provider: KeyWrapProvider) -> None:
    """Inject the key-wrap provider (host wiring). Overrides the default resolver."""
    global _PROVIDER
    _PROVIDER = provider


def reset_checkpoint_key_wrapping_for_tests() -> None:
    global _PROVIDER
    _PROVIDER = None


def get_key_wrap_provider() -> KeyWrapProvider:
    """The active provider. With nothing injected, the safe default is KMS, which
    fails LOUD if unconfigured — never a silent local fallback."""
    if _PROVIDER is not None:
        return _PROVIDER
    return KmsKeyWrapProvider()
