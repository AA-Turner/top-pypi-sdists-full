"""verify a minisign signature (and its signed version) exactly as minisign-verify 0.3.0 checks it."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass
from pathlib import Path
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import same_version
#: prbe-ai/desktop `src-tauri/tauri.conf.json`, `plugins.updater.pubkey`,
#: verbatim: base64 of the minisign public key file ("untrusted comment:
#: minisign public key: AF847825AFE96A41" and the key). The app verifies every
#: update against it; so does this. A new key there is a new constant here.
PUBKEY = (
    "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6IEFGODQ3ODI1QUZFOTZBNDEKUldSQmF1bXZKWGlFcno5ajlV"
    "SW1rWk1aUE83ejNxL3lubVY2MmQ0L1N2K0tiWTZZaFJPMnRDdUQK"
)
#: `plugins.updater.requireSignedVersion` there: a signature must name the
#: version it was made for (its trusted comment's `version:`).
REQUIRE_SIGNED_VERSION = True


# -- minisign, as minisign-verify 0.3.0 and tauri-plugin-updater 2.14.0 check it --


@dataclass(frozen=True)
class PublicKey:
    key_id: bytes  # 8 bytes
    key: bytes  # 32 bytes, Ed25519


@dataclass(frozen=True)
class Signature:
    algorithm: bytes  # b"Ed" (the data itself) or b"ED" (its BLAKE2b-512)
    key_id: bytes
    signature: bytes  # 64 bytes, over the data or its hash
    trusted_comment: str  # after "trusted comment: "
    global_signature: bytes  # 64 bytes, over signature + trusted comment

    @property
    def prehashed(self) -> bool:
        return self.algorithm == b"ED"


def _b64(text: str) -> bytes:
    try:
        return base64.b64decode(text, validate=True)
    except (ValueError, TypeError) as exc:
        raise InstallError("not valid base64") from exc


def _lines(text: str) -> list[str]:
    # Rust's `str::lines`: split at "\n", one trailing "\r" dropped from each.
    out = text.split("\n")
    if out and out[-1] == "":
        out.pop()
    return [line[:-1] if line.endswith("\r") else line for line in out]


def _text(blob: bytes, what: str) -> str:
    try:
        return blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InstallError(f"the {what} is not UTF-8") from exc


def parse_public_key(encoded: str) -> PublicKey:
    """tauri.conf.json's `pubkey`: base64 of a minisign key file, whose second
    line is base64 of `Ed` + key id (8) + key (32)."""
    lines = _lines(_text(_b64(encoded), "public key"))
    if len(lines) < 2:
        raise InstallError("the public key has no key line")
    raw = _b64(lines[1])
    if len(raw) != 42 or raw[:2] not in (b"Ed", b"ED"):
        raise InstallError("the public key is not a minisign Ed25519 key")
    return PublicKey(key_id=raw[2:10], key=raw[10:42])


def parse_signature(encoded: str) -> Signature:
    """A manifest entry's `signature`: base64 of a minisign `.sig` file (an
    untrusted comment, the signature line, the trusted comment, the global
    signature line)."""
    lines = _lines(_text(_b64(encoded), "signature"))
    if len(lines) < 4:
        raise InstallError("the signature is not a minisign signature")
    raw = _b64(lines[1])
    if len(raw) != 74:
        raise InstallError("the signature line has the wrong length")
    trusted = lines[2]
    if not trusted.startswith("trusted comment: "):
        raise InstallError("the signature has no trusted comment")
    global_signature = _b64(lines[3])
    if len(global_signature) != 64:
        raise InstallError("the global signature has the wrong length")
    if raw[:2] not in (b"Ed", b"ED"):
        raise InstallError("the signature algorithm is not supported")
    return Signature(
        algorithm=raw[:2],
        key_id=raw[2:10],
        signature=raw[10:74],
        trusted_comment=trusted[len("trusted comment: "):],
        global_signature=global_signature,
    )


def _ed25519_verify(key: bytes, signature: bytes, message: bytes) -> bool:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError as exc:  # pinned in pyproject.toml; a broken env fails closed
        raise InstallError("this Probe install cannot check signatures (no `cryptography`)") from exc
    try:
        Ed25519PublicKey.from_public_bytes(key).verify(signature, message)
    except (InvalidSignature, ValueError):
        return False
    return True


def signed_version(trusted_comment: str) -> str | None:
    """The `version:` field of Tauri's trusted comment (tab-separated `key:value`)."""
    for field in trusted_comment.split("\t"):
        if field.startswith("version:"):
            return field[len("version:"):]
    return None


def verify(
    message: bytes,
    sig: Signature,
    key: PublicKey,
    announced_version: str,
    *,
    prehashed_digest: bytes | None = None,
    require_signed_version: bool = REQUIRE_SIGNED_VERSION,
) -> None:
    """Raise InstallError unless `sig` is `key`'s signature of `message` (or,
    for `ED`, of its BLAKE2b-512 `prehashed_digest`) and names
    `announced_version`. minisign-verify's `verify(.., allow_legacy=true)`,
    then the updater's `verify_signed_version`: the trusted comment is read
    only after the global signature proves it."""
    if sig.key_id != key.key_id:
        raise InstallError("the signature was made with a different key than the app's")
    if sig.prehashed:
        signed = prehashed_digest if prehashed_digest is not None else hashlib.blake2b(message, digest_size=64).digest()
    else:
        signed = message
    if not _ed25519_verify(key.key, sig.signature, signed):
        raise InstallError("the signature does not verify")
    if not _ed25519_verify(key.key, sig.global_signature, sig.signature + sig.trusted_comment.encode("utf-8")):
        raise InstallError("the signature's trusted comment does not verify")
    version = signed_version(sig.trusted_comment)
    if version is None:
        if require_signed_version:
            raise InstallError("the signature names no version")
        return
    if not same_version(version, announced_version):
        raise InstallError(f"the signature is for {version}, not the announced {announced_version}")


def verify_file(path: Path, sig: Signature, key: PublicKey, announced_version: str) -> None:
    """`verify` of a file: hashed in chunks for `ED`, read whole for `Ed`."""
    if sig.prehashed:
        digest = hashlib.blake2b(digest_size=64)
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        verify(b"", sig, key, announced_version, prehashed_digest=digest.digest())
    else:
        verify(path.read_bytes(), sig, key, announced_version)
