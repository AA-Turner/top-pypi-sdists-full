"""ECDSA keypair generation for identity-service client credentials.

Produces credentials in the same on-the-wire format as the identity-service's
helper scripts: a fresh ECDSA P-384 private key (PKCS#8 PEM) bundled with a
`clientId` and `keyId` as `{"clientId": ..., "keyId": ..., "key": ...}`.
"""

from __future__ import annotations

import base64
import json
import os
import secrets
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

_DEFAULT_CLIENT_ID_PREFIX = "client"
_DEFAULT_KEY_ID_PREFIX = "key"
# 4 bytes → 8 hex chars
_RANDOM_SUFFIX_BYTES = 4


class GeneratedClientCredentials(BaseModel):
    """An ECDSA P-384 keypair plus identifiers for an identity-service client."""

    client_id: str
    key_id: str
    # secret: keep the PEM private key out of repr/str/logs (exclude=True only
    # covers model_dump, not __repr__).
    private_key_pem: str = Field(repr=False)
    public_key_pem: str

    def to_credentials_dict(self) -> dict[str, str]:
        """Return the dict shape identity-service consumes.

        The public key is intentionally omitted because it can be re-derived
        from the included data.
        """
        return {
            "clientId": self.client_id,
            "keyId": self.key_id,
            "key": self.private_key_pem,
        }

    def to_identity_service_secret(self) -> str:
        """Return the base64-encoded JSON credentials blob.

        This is the inline form `Configuration.identity_service_secret` expects.
        """
        blob = json.dumps(self.to_credentials_dict()).encode("utf-8")
        return base64.b64encode(blob).decode("ascii")

    def write_credentials_json(self, path: str | Path) -> None:
        """Write `to_credentials_dict` as compact JSON to `path`.

        Creates the file with mode `0o600` as appropriate for a private key.
        If `path` already exists, the mode argument to `os.open` is ignored on
        POSIX, so re-tighten the mode via `fchmod` before writing.
        """
        payload = json.dumps(self.to_credentials_dict()).encode("utf-8")
        fd = os.open(
            os.fspath(path),
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            0o600,
        )
        try:
            if hasattr(os, "fchmod"):
                os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(payload)
        except BaseException:
            try:
                os.close(fd)
            except OSError:
                pass
            raise

    @classmethod
    def from_credentials_dict(cls, data: dict[str, str]) -> "GeneratedClientCredentials":
        """Build credentials from the `{clientId, keyId, key}` dict shape.

        The inverse of `to_credentials_dict`. `key` must be a PEM-encoded ECDSA
        P-384 (secp384r1) private key; the public key is re-derived from it.

        :raises ValueError: if a field is missing or the PEM key is unparseable.
        :raises TypeError: if the key is not an ECDSA P-384 private key.
        """
        # Lazy import; see generate_client_keypair for the rationale.
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives.serialization import load_pem_private_key

        try:
            client_id = data["clientId"]
            key_id = data["keyId"]
            private_pem = data["key"]
        except (KeyError, TypeError) as e:
            raise ValueError(
                "credentials must contain 'clientId', 'keyId', and 'key'"
            ) from e

        try:
            private_key = load_pem_private_key(private_pem.encode(), password=None)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"credentials 'key' is not a valid PEM private key: {e}"
            ) from e
        if not isinstance(private_key, ec.EllipticCurvePrivateKey) or not isinstance(
            private_key.curve, ec.SECP384R1
        ):
            raise TypeError(
                "credentials 'key' must be an ECDSA P-384 (secp384r1) private key"
            )

        public_pem = (
            private_key.public_key()
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode("ascii")
        )
        return cls(
            client_id=client_id,
            key_id=key_id,
            private_key_pem=private_pem,
            public_key_pem=public_pem,
        )

    @classmethod
    def read_credentials_json(cls, path: str | Path) -> "GeneratedClientCredentials":
        """Load credentials from a `{clientId, keyId, key}` JSON file.

        The inverse of `write_credentials_json`.

        :raises ValueError: if the file is unreadable/malformed or a field is
                            missing or carries an unparseable PEM key.
        :raises TypeError: if the key is not an ECDSA P-384 private key.
        """
        try:
            data = json.loads(Path(path).read_text())
        except OSError as e:
            raise ValueError(f"cannot read credentials file at {path}: {e}") from e
        except UnicodeDecodeError as e:
            raise ValueError(f"credentials file at {path} is not valid UTF-8: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"credentials file at {path} is not valid JSON: {e}") from e
        return cls.from_credentials_dict(data)


class _CredentialsResult(BaseModel):
    """Base for results that carry a generated keypair plus credential helpers.

    Holds the `credentials` (excluded from serialization so the private key
    never lands in logs or on the wire) and the persistence helpers that delegate
    to it. Shared by the PAT-exchange and key-registration result types, whose
    `credentials` are always present, so these helpers work for every result.
    """

    # Excluded from serialization (exclude) AND from repr so the private key
    # inside `credentials` never leaks via model_dump, repr/str, or logs.
    credentials: GeneratedClientCredentials = Field(exclude=True, repr=False)

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )

    def write_credentials_json(self, path: Any) -> None:
        """Write the Identity Service `{clientId, keyId, key}` credentials JSON to `path`."""
        self.credentials.write_credentials_json(path)

    def to_identity_service_secret(self) -> str:
        """Return a base64-encoded JSON credentials blob."""
        return self.credentials.to_identity_service_secret()


def generate_client_keypair(
    client_id: str | None = None,
    key_id: str | None = None,
    *,
    client_id_prefix: str = _DEFAULT_CLIENT_ID_PREFIX,
    key_id_prefix: str = _DEFAULT_KEY_ID_PREFIX,
) -> GeneratedClientCredentials:
    """Generate a fresh ECDSA P-384 keypair and bundle it with identifiers.

    The generated key is built to the standards and format established by the
    identity-service's existing helper scripts:

    * ECDSA on the NIST P-384 curve
    * Private key PEM-encoded as PKCS#8 (`-----BEGIN PRIVATE KEY-----`)
    * Public key PEM-encoded as SubjectPublicKeyInfo (`-----BEGIN PUBLIC KEY-----`)

    If `client_id` or `key_id` is omitted, a random value of the form
    `"<prefix>-<8 hex chars>"` is generated.
    """
    # Lazy import: cryptography's PyO3 Rust extension cannot be initialized in
    # more than one (sub)interpreter per process (pyca/cryptography#9016,
    # PyO3/pyo3#3451). pytest-cov's tracer setup creates a subinterpreter
    # during conftest load, which makes any cryptography import reachable from
    # `import istari` fatal under coverage. Deferring the import
    # to call time keeps the package import path off cryptography entirely.
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec

    private_key = ec.generate_private_key(ec.SECP384R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")

    resolved_client_id = client_id or f"{client_id_prefix}-{secrets.token_hex(_RANDOM_SUFFIX_BYTES)}"
    resolved_key_id = key_id or f"{key_id_prefix}-{secrets.token_hex(_RANDOM_SUFFIX_BYTES)}"

    return GeneratedClientCredentials(
        client_id=resolved_client_id,
        key_id=resolved_key_id,
        private_key_pem=private_pem,
        public_key_pem=public_pem,
    )
