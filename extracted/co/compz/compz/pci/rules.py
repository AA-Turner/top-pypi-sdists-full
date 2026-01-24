"""
Basic, language-agnostic PCI-DSS rules for CompZ.

These are heuristic, regex-based checks that work across common source/config
files. They are NOT a substitute for formal PCI audits, but provide practical
signals that can be attested and anchored with CompZ.
"""

import re
from typing import List, Dict

# Forbidden payment data patterns (PCI 3.2)
FORBIDDEN_DATA_PATTERNS = [
    r"\b(cvv|cvc|cid|cav|csc)\b",
    r"\b(pin|pinblock|pin_block)\b",
    r"\b(track_?data|magnetic|mag_stripe)\b",
]

# Private key / seed exposure (PCI 3.5 adapted)
PRIVATE_KEY_PATTERNS = [
    r"\b(private_?key|priv_?key|secret_?key)\b",
    r"\b(seed\s*(phrase|words)\b)",
]

# Weak cryptography patterns (PCI 4.1)
WEAK_CRYPTO_PATTERNS = [
    r"\b(md5|sha-?1|crc32)\b",
    r"\b(rc4|des)(?!\w)\b",
]

# Rate limiting keywords (PCI 12.3.5 heuristic)
RATE_LIMIT_KEYWORDS = [
    "rate_limit", "ratelimit", "throttle", "cooldown", "requests_per",
]

# Transaction limits keywords (PCI 11.3.4 heuristic)
LIMIT_KEYWORDS = [
    "max_amount", "max_transaction", "max_value", "limit", "threshold",
    "MAX_AMOUNT", "MAX_TRANSACTION", "MAX_VALUE",
]


def _any_pattern(content: str, patterns: List[str]) -> bool:
    for p in patterns:
        if re.search(p, content, flags=re.IGNORECASE):
            return True
    return False


def scan_forbidden_data(content: str) -> List[str]:
    hits = []
    for p in FORBIDDEN_DATA_PATTERNS:
        if re.search(p, content, flags=re.IGNORECASE):
            hits.append(p)
    return hits


def scan_private_keys(content: str) -> List[str]:
    hits = []
    for p in PRIVATE_KEY_PATTERNS:
        if re.search(p, content, flags=re.IGNORECASE):
            hits.append(p)
    return hits


def scan_weak_crypto(content: str) -> List[str]:
    hits = []
    for p in WEAK_CRYPTO_PATTERNS:
        if re.search(p, content, flags=re.IGNORECASE):
            hits.append(p)
    return hits


def has_rate_limiting(content: str) -> bool:
    return any(k.lower() in content.lower() for k in RATE_LIMIT_KEYWORDS)


def has_transaction_limits(content: str) -> bool:
    return any(k in content for k in LIMIT_KEYWORDS)


def summarize_matches(matches: List[str]) -> str:
    if not matches:
        return ""
    unique = sorted(set(matches))
    return ", ".join(unique)
