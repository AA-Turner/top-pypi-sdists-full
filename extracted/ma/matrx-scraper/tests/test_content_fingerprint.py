"""Content fingerprint contract — capture-time duplicate detection evidence.

The fingerprint is persisted on immutable `web.snapshot.extracted.fingerprint`
and compared ACROSS crawls, so determinism and version discipline are the
contract, not implementation details.
"""

from __future__ import annotations

from matrx_scraper.parser.hashing import (
    FINGERPRINT_VERSION,
    compute_text_fingerprint,
    simhash64_hamming,
)
from matrx_scraper.seo_audit import audit_html

ARTICLE = (
    "Recycling electronics responsibly protects the environment and keeps "
    "hazardous materials out of landfills. Our certified facility processes "
    "laptops, servers, and mobile devices with full data destruction. "
) * 12


def test_fingerprint_shape_and_determinism():
    a = compute_text_fingerprint(ARTICLE)
    b = compute_text_fingerprint(ARTICLE)
    assert a == b
    assert a["version"] == FINGERPRINT_VERSION
    assert len(a["exact_sha256"]) == 64
    assert len(a["simhash64"]) == 16
    int(a["simhash64"], 16)  # valid fixed-width hex
    assert a["shingle_size"] == 3
    assert a["token_count"] == len(ARTICLE.split())


def test_whitespace_and_case_normalization():
    a = compute_text_fingerprint("Hello   World\n\tfoo bar")
    b = compute_text_fingerprint("hello world foo bar")
    assert a is not None and b is not None
    assert a["exact_sha256"] == b["exact_sha256"]
    assert a["simhash64"] == b["simhash64"]


def test_empty_text_returns_none():
    assert compute_text_fingerprint("") is None
    assert compute_text_fingerprint("   \n\t ") is None


def test_near_duplicates_are_close_and_distinct_pages_are_far():
    base = compute_text_fingerprint(ARTICLE)
    near = compute_text_fingerprint(ARTICLE + " Serving the greater Sacramento region since 2003.")
    far = compute_text_fingerprint(
        "A completely different page about workflow orchestration, database "
        "migrations, and structured content rendering in a multi-agent "
        "platform with streaming pipelines. " * 12
    )
    assert base is not None and near is not None and far is not None
    assert base["exact_sha256"] != near["exact_sha256"]
    near_distance = simhash64_hamming(base["simhash64"], near["simhash64"])
    far_distance = simhash64_hamming(base["simhash64"], far["simhash64"])
    # 90% similarity == hamming <= 6 of 64 bits (the frontend default).
    assert near_distance <= 6
    assert far_distance > 6


def test_short_text_still_fingerprints():
    tiny = compute_text_fingerprint("one two")
    assert tiny is not None
    assert tiny["token_count"] == 2


def test_audit_html_carries_fingerprint_over_visible_text():
    html = f"<html><body><main><p>{ARTICLE}</p></main></body></html>"
    audit = audit_html(html, "https://example.com/")
    assert audit.content_fingerprint is not None
    assert audit.text_hash == audit.content_fingerprint["exact_sha256"]
    # Same text through the raw helper must agree — the audit adds nothing.
    direct = compute_text_fingerprint(ARTICLE)
    assert direct is not None
    assert audit.content_fingerprint["simhash64"] == direct["simhash64"]


def test_audit_empty_page_has_no_fingerprint():
    audit = audit_html("<html><body></body></html>", "https://example.com/")
    assert audit.content_fingerprint is None
    assert audit.text_hash is None
