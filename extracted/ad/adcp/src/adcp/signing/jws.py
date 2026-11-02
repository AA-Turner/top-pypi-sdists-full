"""Minimal JWS parse + verify for AdCP revocation lists.

The AdCP governance profile uses JSON Web Signature (RFC 7515) to sign
revocation-list documents published at
``{origin}/.well-known/governance-revocations.json``. The list MAY be
serialized in compact form (``header.payload.signature``) or JWS general
JSON serialization (an object with ``payload`` and ``signatures[]``).
Both carry the same three fields after decoding.

This module intentionally does not pull in ``pyjwt`` / ``authlib``. AdCP
has a narrow allowed-alg set (``EdDSA``, ``ES256``) and we already own
the underlying crypto primitives for RFC 9421, so a ~120-line parser
over the existing ``verify_signature`` is both leaner and auditable.

The signature base for compact JWS is::

    ASCII(BASE64URL(protected_header)) || "." || ASCII(BASE64URL(payload))

— exactly what ``verify_signature`` expects, given the JWS-to-RFC-9421
algorithm mapping below.
"""

from __future__ import annotations

import binascii
import json
from typing import Any

from adcp.signing.crypto import (
    ALG_ED25519,
    ALG_ES256,
    b64url_decode,
    public_key_from_jwk,
    verify_signature,
)
from adcp.signing.jwks import AsyncJwksResolver, JwksResolver

# JWS uses RFC 7518 algorithm names; RFC 9421 uses the IANA HTTP Signature
# names. We convert at the JWS boundary so the rest of the module speaks
# the internal alg vocabulary already used by our crypto primitives.
JWS_ALG_TO_INTERNAL: dict[str, str] = {
    "EdDSA": ALG_ED25519,
    "ES256": ALG_ES256,
}
ALLOWED_JWS_ALGS: frozenset[str] = frozenset(JWS_ALG_TO_INTERNAL.keys())


class JwsError(Exception):
    """Base class for JWS parse/verify failures."""


class JwsMalformedError(JwsError):
    """JWS document is syntactically invalid or uses a disallowed shape."""


class JwsUnknownKeyError(JwsError):
    """The JWS header ``kid`` is not present in the configured JWKS."""


class JwsSignatureInvalidError(JwsError):
    """The JWS signature did not verify against the resolved key."""


def _decode_protected_header(b64_header: str) -> dict[str, Any]:
    try:
        raw = b64url_decode(b64_header)
    except (ValueError, binascii.Error) as exc:
        raise JwsMalformedError(f"protected header is not valid base64url: {exc}") from exc
    try:
        header = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise JwsMalformedError(f"protected header is not valid JSON: {exc}") from exc
    if not isinstance(header, dict):
        raise JwsMalformedError("protected header is not a JSON object")
    return header


def parse_compact_jws(token: str) -> tuple[str, str, bytes]:
    """Split a compact JWS into ``(b64_header, b64_payload, signature bytes)``.

    Returns the header and payload as the ORIGINAL base64url substrings —
    not decoded and re-encoded — so the verifier uses the exact bytes that
    the signer hashed. This matters because ``urlsafe_b64decode`` is
    lenient (accepts ``+``/``/`` and padding); round-tripping through it
    can produce different bytes than the wire form.
    """
    if not isinstance(token, str):
        raise JwsMalformedError("compact JWS must be a string")
    parts = token.split(".")
    if len(parts) != 3:
        raise JwsMalformedError(
            f"compact JWS must have exactly 3 dot-separated segments, got {len(parts)}"
        )
    b64_header, b64_payload, b64_signature = parts
    if not b64_header or not b64_payload or not b64_signature:
        raise JwsMalformedError("compact JWS has an empty segment")
    try:
        signature = b64url_decode(b64_signature)
    except (ValueError, binascii.Error) as exc:
        raise JwsMalformedError(f"compact JWS signature is not valid base64url: {exc}") from exc
    return b64_header, b64_payload, signature


def parse_general_json_jws(doc: dict[str, Any]) -> tuple[str, str, bytes]:
    """Extract the first signature from a JWS general JSON serialization.

    Returns ``(b64_header, b64_payload, signature_bytes)``. AdCP revocation
    lists are signed by a single operator key, so we only honor the first
    entry in ``signatures[]``. A list with multiple signatures is malformed
    for this profile.
    """
    if not isinstance(doc, dict):
        raise JwsMalformedError("JWS general JSON document must be an object")
    if "payload" not in doc or "signatures" not in doc:
        raise JwsMalformedError("JWS general JSON document must have 'payload' and 'signatures'")
    signatures = doc["signatures"]
    if not isinstance(signatures, list) or len(signatures) == 0:
        raise JwsMalformedError("JWS general JSON 'signatures' must be a non-empty array")
    if len(signatures) > 1:
        raise JwsMalformedError(
            "JWS general JSON 'signatures' with multiple entries is not supported for "
            "this profile"
        )
    entry = signatures[0]
    if not isinstance(entry, dict):
        raise JwsMalformedError("JWS signature entry must be an object")
    b64_header = entry.get("protected")
    b64_signature = entry.get("signature")
    b64_payload = doc["payload"]
    if not isinstance(b64_header, str) or not isinstance(b64_signature, str):
        raise JwsMalformedError("JWS signature entry missing 'protected' or 'signature'")
    if not isinstance(b64_payload, str):
        raise JwsMalformedError("JWS 'payload' must be a base64url string")
    try:
        signature = b64url_decode(b64_signature)
    except (ValueError, binascii.Error) as exc:
        raise JwsMalformedError(f"JWS signature is not valid base64url: {exc}") from exc
    return b64_header, b64_payload, signature


def _validate_header(
    b64_protected: str,
    *,
    expected_typ: str,
    allowed_algs: frozenset[str],
) -> tuple[str, str]:
    """Parse + validate the protected header; return ``(internal_alg, kid)``.

    Shared by sync and async verify paths — everything here is pure CPU.
    """
    header = _decode_protected_header(b64_protected)

    alg = header.get("alg")
    if not isinstance(alg, str) or alg == "none" or alg not in allowed_algs:
        raise JwsMalformedError(
            f"JWS alg {alg!r} not allowed; permitted values: {sorted(allowed_algs)}"
        )
    internal_alg = JWS_ALG_TO_INTERNAL[alg]

    typ = header.get("typ")
    if typ != expected_typ:
        raise JwsMalformedError(
            f"JWS typ {typ!r} does not match expected {expected_typ!r}"
        )

    crit = header.get("crit")
    if crit is not None and (not isinstance(crit, list) or len(crit) > 0):
        raise JwsMalformedError("JWS 'crit' header is not supported for this profile")

    kid = header.get("kid")
    if not isinstance(kid, str) or not kid:
        raise JwsMalformedError("JWS protected header must include a non-empty 'kid'")

    return internal_alg, kid


def _verify_signature_and_decode_payload(
    *,
    b64_protected: str,
    b64_payload: str,
    signature: bytes,
    jwk: dict[str, Any],
    internal_alg: str,
    kid: str,
) -> dict[str, Any]:
    """Run the cryptographic verify + decode the payload as JSON.

    Signing input uses the ORIGINAL base64url strings — don't decode-
    then-re-encode, since ``urlsafe_b64decode`` is lenient and a
    round-trip can produce different bytes than the wire form.
    """
    signing_input = (b64_protected + "." + b64_payload).encode("ascii")

    public_key = public_key_from_jwk(jwk)
    if not verify_signature(
        alg=internal_alg,
        public_key=public_key,
        signature_base=signing_input,
        signature=signature,
    ):
        raise JwsSignatureInvalidError(f"signature did not verify for kid {kid!r}")

    try:
        payload_bytes = b64url_decode(b64_payload)
    except (ValueError, binascii.Error) as exc:
        raise JwsMalformedError(f"JWS payload is not valid base64url: {exc}") from exc
    try:
        decoded_payload = json.loads(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise JwsMalformedError(f"JWS payload is not valid JSON: {exc}") from exc
    if not isinstance(decoded_payload, dict):
        raise JwsMalformedError("JWS payload is not a JSON object")
    return decoded_payload


def verify_detached_jws(
    *,
    b64_protected: str,
    b64_payload: str,
    signature: bytes,
    jwks_resolver: JwksResolver,
    expected_typ: str,
    allowed_algs: frozenset[str] = ALLOWED_JWS_ALGS,
) -> dict[str, Any]:
    """Verify a parsed JWS and return the decoded payload JSON.

    Performs, in order:
    1. Decode + parse the protected header.
    2. Reject if ``alg`` is absent, is ``none``, or not in ``allowed_algs``.
    3. Reject if ``typ`` is not exactly ``expected_typ`` (byte equality, no
       normalization — matches the AdCP spec).
    4. Resolve ``kid`` via ``jwks_resolver``; reject unknown.
    5. Verify the detached signature against the original b64 strings.
    6. Decode the payload as JSON and return it.

    Any failure raises a :class:`JwsError` subclass. The caller maps these
    to transport-error codes (e.g. ``request_signature_revocation_stale``).
    """
    internal_alg, kid = _validate_header(
        b64_protected, expected_typ=expected_typ, allowed_algs=allowed_algs
    )
    jwk = jwks_resolver(kid)
    if jwk is None:
        raise JwsUnknownKeyError(f"no JWK for kid {kid!r}")
    return _verify_signature_and_decode_payload(
        b64_protected=b64_protected,
        b64_payload=b64_payload,
        signature=signature,
        jwk=jwk,
        internal_alg=internal_alg,
        kid=kid,
    )


async def averify_detached_jws(
    *,
    b64_protected: str,
    b64_payload: str,
    signature: bytes,
    jwks_resolver: AsyncJwksResolver,
    expected_typ: str,
    allowed_algs: frozenset[str] = ALLOWED_JWS_ALGS,
) -> dict[str, Any]:
    """Async variant of :func:`verify_detached_jws`.

    Awaits an :class:`AsyncJwksResolver` on the ``kid`` lookup; all
    other work is pure CPU and runs inline.
    """
    internal_alg, kid = _validate_header(
        b64_protected, expected_typ=expected_typ, allowed_algs=allowed_algs
    )
    jwk = await jwks_resolver(kid)
    if jwk is None:
        raise JwsUnknownKeyError(f"no JWK for kid {kid!r}")
    return _verify_signature_and_decode_payload(
        b64_protected=b64_protected,
        b64_payload=b64_payload,
        signature=signature,
        jwk=jwk,
        internal_alg=internal_alg,
        kid=kid,
    )


def verify_jws_document(
    doc: str | dict[str, Any],
    *,
    jwks_resolver: JwksResolver,
    expected_typ: str,
    allowed_algs: frozenset[str] = ALLOWED_JWS_ALGS,
) -> dict[str, Any]:
    """Parse a JWS (compact string or general-JSON dict) and verify in one call.

    Dispatches to the right parser based on the input shape, then calls
    :func:`verify_detached_jws`. Returns the verified payload dict.
    """
    if isinstance(doc, str):
        b64_header, b64_payload, signature = parse_compact_jws(doc)
    elif isinstance(doc, dict):
        b64_header, b64_payload, signature = parse_general_json_jws(doc)
    else:
        raise JwsMalformedError(
            "JWS document must be a compact string or JSON general-serialization object"
        )
    return verify_detached_jws(
        b64_protected=b64_header,
        b64_payload=b64_payload,
        signature=signature,
        jwks_resolver=jwks_resolver,
        expected_typ=expected_typ,
        allowed_algs=allowed_algs,
    )


async def averify_jws_document(
    doc: str | dict[str, Any],
    *,
    jwks_resolver: AsyncJwksResolver,
    expected_typ: str,
    allowed_algs: frozenset[str] = ALLOWED_JWS_ALGS,
) -> dict[str, Any]:
    """Async variant of :func:`verify_jws_document`.

    Accepts an :class:`AsyncJwksResolver`; parsing and signature verify
    are pure CPU and run inline.
    """
    if isinstance(doc, str):
        b64_header, b64_payload, signature = parse_compact_jws(doc)
    elif isinstance(doc, dict):
        b64_header, b64_payload, signature = parse_general_json_jws(doc)
    else:
        raise JwsMalformedError(
            "JWS document must be a compact string or JSON general-serialization object"
        )
    return await averify_detached_jws(
        b64_protected=b64_header,
        b64_payload=b64_payload,
        signature=signature,
        jwks_resolver=jwks_resolver,
        expected_typ=expected_typ,
        allowed_algs=allowed_algs,
    )


__all__ = [
    "ALLOWED_JWS_ALGS",
    "AsyncJwksResolver",
    "JWS_ALG_TO_INTERNAL",
    "JwksResolver",
    "JwsError",
    "JwsMalformedError",
    "JwsSignatureInvalidError",
    "JwsUnknownKeyError",
    "averify_detached_jws",
    "averify_jws_document",
    "parse_compact_jws",
    "parse_general_json_jws",
    "verify_detached_jws",
    "verify_jws_document",
]
