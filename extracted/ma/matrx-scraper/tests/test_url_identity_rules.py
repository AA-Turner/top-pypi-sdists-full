"""Cross-repo identity guard — the Python half.

Pins :mod:`matrx_scraper.utils.url` against the language-neutral fixture
``matrx_scraper/utils/url-identity-rules.json``. ai-matrx's
``features/marketing/lib/__tests__/page-url.test.ts`` tests its TypeScript twin
against a byte-identical copy of the SAME file, and each suite pins the
fixture's SHA-256 so a one-sided edit reddens the repo that was NOT updated.

Never "fix" a red here by loosening the check — re-sync the two copies.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from matrx_scraper.utils.url import (
    normalize_url,
    page_route_key,
    page_route_match_key,
    url_hash,
)

FIXTURE_PATH = (
    Path(__file__).resolve().parents[1] / "matrx_scraper" / "utils" / "url-identity-rules.json"
)

# SHA-256 of url-identity-rules.json, pinned IDENTICALLY in ai-matrx's
# features/marketing/lib/__tests__/page-url.test.ts. Changing the fixture is a
# four-file change — see the fixture's own `_comment`.
_FIXTURE_SHA256 = "08eec55b9db0313d34bb056dff113fd1b6ceb9111cc69f9c8f7f67dcbcaa082e"

_FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _cases(key: str) -> list[tuple[str, str, str]]:
    return [(case["name"], case["input"], case["expect"]) for case in _FIXTURE[key]]


def test_fixture_is_byte_identical_across_repos() -> None:
    digest = hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest()
    assert digest == _FIXTURE_SHA256, (
        "url-identity-rules.json changed. Copy it verbatim to ai-matrx's "
        "features/marketing/lib/__tests__/url-identity-rules.json and update the "
        "pinned SHA-256 in BOTH suites — a one-sided edit is the exact defect this "
        f"guard exists to catch. New digest: {digest}"
    )


@pytest.mark.parametrize(("name", "raw", "expected"), _cases("normalize_url_cases"))
def test_normalize_url(name: str, raw: str, expected: str) -> None:
    assert normalize_url(raw) == expected, name


@pytest.mark.parametrize(("name", "raw", "expected"), _cases("url_hash_cases"))
def test_url_hash(name: str, raw: str, expected: str) -> None:
    assert url_hash(raw) == expected, name


@pytest.mark.parametrize(("name", "raw", "expected"), _cases("page_route_key_cases"))
def test_page_route_key(name: str, raw: str, expected: str) -> None:
    assert page_route_key(raw) == expected, name


@pytest.mark.parametrize(("name", "raw", "expected"), _cases("page_route_match_key_cases"))
def test_page_route_match_key(name: str, raw: str, expected: str) -> None:
    assert page_route_match_key(raw) == expected, name


def test_page_route_key_is_idempotent() -> None:
    """A route key fed back in must not change — a normalizer that does not
    recognize its own output is how fields get re-wrapped and lost."""
    for _, raw, _ in _cases("page_route_key_cases"):
        once = page_route_key(raw)
        assert page_route_key(once) == once, raw


def test_url_hash_is_derived_from_normalize_url() -> None:
    """The digest must never be computable from a second normalizer."""
    for _, raw, _ in _cases("normalize_url_cases"):
        assert url_hash(raw) == hashlib.sha256(normalize_url(raw).encode("utf-8")).hexdigest()
