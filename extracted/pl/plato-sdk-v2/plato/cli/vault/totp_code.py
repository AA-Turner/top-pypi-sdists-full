"""RFC 6238 TOTP codes, stdlib only (python-sdk has no pyotp dependency).

The same arithmetic as ``worlds/login/src/login_world/get_otp.py:_totp`` (which
runs on its own on the agent VM, so it cannot be imported here), plus SHA256 and
SHA512 for the RFC test vectors, a seed check and an ``otpauth://`` URI parser.
No function here logs or prints a seed or a code.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import re
import struct
import time
import urllib.parse
from collections.abc import Callable

from pydantic import SecretStr

from plato.cli.vault.client import VaultConsoleError
from plato.cli.vault.totp_models import TotpAlgorithm, TotpParams

# A seed shorter than this many bytes is not a real authenticator seed (RFC 4226
# asks for 128 bits; 80 bits is the floor that vendors use).
MIN_SEED_BYTES = 10
_HASHES = {
    TotpAlgorithm.sha1: hashlib.sha1,
    TotpAlgorithm.sha256: hashlib.sha256,
    TotpAlgorithm.sha512: hashlib.sha512,
}
_SEED_STRIP = re.compile(r"[\s-]+")


class BadSeed(VaultConsoleError):
    """The seed is not base32 or is too short. The text never quotes the seed."""


def normalize_seed(seed: str) -> str:
    """Upper case, no spaces, no dashes, no ``=`` padding: the form the vault keeps."""
    return _SEED_STRIP.sub("", seed).upper().rstrip("=")


def seed_bytes(seed: str) -> bytes:
    """The key bytes of a base32 seed. Raises :class:`BadSeed` (no seed text in it)."""
    clean = normalize_seed(seed)
    try:
        key = base64.b32decode(clean + "=" * (-len(clean) % 8))
    except (binascii.Error, ValueError):
        raise BadSeed(f"the key is not base32 ({len(clean)} characters)") from None
    if len(key) < MIN_SEED_BYTES:
        raise BadSeed(f"the key is too short ({len(key)} bytes; at least {MIN_SEED_BYTES})")
    return key


def hotp(key: bytes, counter: int, digits: int = 6, algorithm: TotpAlgorithm = TotpAlgorithm.sha1) -> str:
    """RFC 4226 HOTP with dynamic truncation."""
    digest = hmac.new(key, struct.pack(">Q", counter), _HASHES[algorithm]).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF) % (10**digits)
    return str(code).zfill(digits)


def totp(
    seed: str | SecretStr | bytes,
    at: float | None = None,
    *,
    digits: int = 6,
    period_s: int = 30,
    algorithm: TotpAlgorithm = TotpAlgorithm.sha1,
) -> str:
    """The RFC 6238 code for ``seed`` (base32 text, or raw key bytes) at epoch ``at``."""
    if isinstance(seed, SecretStr):
        seed = seed.get_secret_value()
    key = seed if isinstance(seed, bytes) else seed_bytes(seed)
    now = time.time() if at is None else at
    return hotp(key, int(now) // period_s, digits, algorithm)


def seconds_left(at: float, period_s: int = 30) -> int:
    """Seconds until the code at ``at`` stops being the current one."""
    return period_s - int(at) % period_s


def fresh_code(
    seed: SecretStr,
    params: TotpParams,
    *,
    min_left_s: int,
    clock: Callable[[], float] = time.time,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[str, int]:
    """The current code and its seconds left. When fewer than ``min_left_s`` are left,
    wait for the next period first, so a code is not typed just as it expires."""
    now = clock()
    left = seconds_left(now, params.period_s)
    if left < min_left_s:
        sleep(left + 0.5)
        now = clock()
        left = seconds_left(now, params.period_s)
    code = totp(seed, now, digits=params.digits, period_s=params.period_s, algorithm=params.algorithm)
    return code, left


def parse_otpauth(uri: str, default: TotpParams) -> tuple[str, TotpParams]:
    """``(seed, params)`` from an ``otpauth://totp/...`` URI (Google Authenticator key
    URI format). Missing parameters take ``default``'s. Errors never quote the URI."""
    parsed = urllib.parse.urlparse(uri.strip())
    if parsed.scheme.lower() != "otpauth" or parsed.netloc.lower() != "totp":
        raise BadSeed("the otpauth URI is not a TOTP URI")
    query = {k.lower(): v for k, v in urllib.parse.parse_qsl(parsed.query)}
    secret = query.get("secret")
    if not secret:
        raise BadSeed("the otpauth URI has no secret")
    try:
        digits = int(query.get("digits", default.digits))
        period = int(query.get("period", default.period_s))
    except ValueError:
        raise BadSeed("the otpauth URI has a digits or period that is not a number") from None
    raw_alg = query.get("algorithm", default.algorithm.value).upper()
    try:
        algorithm = TotpAlgorithm(raw_alg)
    except ValueError:
        raise BadSeed(f"the otpauth URI names an unknown algorithm ({len(raw_alg)} characters)") from None
    label = urllib.parse.unquote(parsed.path.lstrip("/"))
    issuer = query.get("issuer") or (label.split(":", 1)[0] if ":" in label else None)
    return normalize_seed(secret), TotpParams(digits=digits, period_s=period, algorithm=algorithm, issuer=issuer)
