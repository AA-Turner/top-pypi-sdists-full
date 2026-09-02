from __future__ import annotations

import hashlib
import re
from collections import Counter
from typing import Any

try:
    from datasketch import MinHash, LeanMinHash

    _MINHASH_AVAILABLE = True
except ImportError:
    _MINHASH_AVAILABLE = False

try:
    from simhash import Simhash

    _SIMHASH_AVAILABLE = True
except ImportError:
    _SIMHASH_AVAILABLE = False

DEFAULT_MINHASH_PERMS = 128
DEFAULT_SHINGLE_SIZE = 3


def compute_minhash_from_text(
    text_content: str,
    shingle_size: int = DEFAULT_SHINGLE_SIZE,
    num_perms: int = DEFAULT_MINHASH_PERMS,
) -> list[int] | None:
    if not _MINHASH_AVAILABLE:
        return None
    parts = text_content.splitlines()
    full_text = " ".join(line.replace("\n", " ") for line in parts)
    words = full_text.split()
    shingles = [" ".join(words[i : i + shingle_size]) for i in range(len(words) - shingle_size + 1)]
    m = MinHash(num_perm=num_perms)
    for shingle in shingles:
        m.update(shingle.encode("utf-8"))
    return LeanMinHash(m).digest().tolist()


def _clean_outline_key(key: str) -> str:
    cleaned = re.sub(r"^H\d+:\s*", "", key)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def compute_simhash(text: str, bits: int = 64) -> int | None:
    if not _SIMHASH_AVAILABLE:
        return None
    features = text.split()
    value = Simhash(features, f=bits).value
    if value >= 2**63:
        value -= 2**64
    return value


def compute_simhash_from_outline(outline: dict) -> int | None:
    if not _SIMHASH_AVAILABLE:
        return None
    text = "\n".join(_clean_outline_key(k) for k in outline.keys())
    return compute_simhash(text)


def compute_hashes(text_content: str, outline: dict | None = None) -> dict:
    result: dict = {}
    minhash = compute_minhash_from_text(text_content)
    if minhash is not None:
        result["minhash"] = minhash
    simhash = compute_simhash(text_content)
    if simhash is not None:
        result["simhash"] = simhash
    if outline:
        outline_simhash = compute_simhash_from_outline(outline)
        if outline_simhash is not None:
            result["outline_simhash"] = outline_simhash
    return result


# --- Persisted content fingerprint (web.snapshot.extracted.fingerprint) ----
#
# STABILITY CONTRACT: these values are persisted on immutable crawl snapshots
# and compared ACROSS crawls and deployments. The implementation is pure
# Python (sha256 + md5) on purpose — no optional dependency whose internal
# feature hashing could drift between library versions. Any change to the
# normalization, shingling, or bit derivation MUST bump
# FINGERPRINT_VERSION, and consumers must only compare equal versions.

FINGERPRINT_VERSION = 1
FINGERPRINT_SHINGLE_SIZE = 3


def compute_text_fingerprint(
    text: str,
    shingle_size: int = FINGERPRINT_SHINGLE_SIZE,
) -> dict[str, Any] | None:
    """Deterministic duplicate-detection fingerprint for one page's text.

    Returns ``{version, exact_sha256, simhash64, shingle_size, token_count}``
    or ``None`` for empty text. ``exact_sha256`` is the hash of the
    whitespace-normalized, lowercased text (exact-duplicate grouping);
    ``simhash64`` is a 64-bit weighted simhash over word shingles encoded as
    a fixed-width lowercase hex string — JSON-safe (a raw 64-bit int loses
    precision in JavaScript) and cheap to compare via XOR popcount.
    """
    normalized = re.sub(r"\s+", " ", text or "").strip().lower()
    if not normalized:
        return None
    tokens = normalized.split()
    if len(tokens) <= shingle_size:
        shingles: list[str] = [normalized]
    else:
        shingles = [
            " ".join(tokens[i : i + shingle_size]) for i in range(len(tokens) - shingle_size + 1)
        ]
    weights = [0] * 64
    for shingle, count in Counter(shingles).items():
        digest = int.from_bytes(hashlib.md5(shingle.encode("utf-8")).digest()[:8], "big")
        for bit in range(64):
            if (digest >> bit) & 1:
                weights[bit] += count
            else:
                weights[bit] -= count
    value = 0
    for bit in range(64):
        if weights[bit] > 0:
            value |= 1 << bit
    return {
        "version": FINGERPRINT_VERSION,
        "exact_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
        "simhash64": f"{value:016x}",
        "shingle_size": shingle_size,
        "token_count": len(tokens),
    }


def simhash64_hamming(hex_a: str, hex_b: str) -> int:
    """Hamming distance between two ``simhash64`` hex fingerprints."""
    return bin(int(hex_a, 16) ^ int(hex_b, 16)).count("1")


def chunk_simhash(simhash_value: int) -> tuple[int, int, int, int]:
    mask = (1 << 16) - 1
    c4 = simhash_value & mask
    c3 = (simhash_value >> 16) & mask
    c2 = (simhash_value >> 32) & mask
    c1 = (simhash_value >> 48) & mask
    return (c1, c2, c3, c4)


def hamming_distance(h1: int, h2: int) -> int:
    xor = (h1 ^ h2) & 0xFFFFFFFFFFFFFFFF
    return bin(xor).count("1")
