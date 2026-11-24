"""Our SimHash reproduces the retired ``simhash`` package bit for bit.

Page fingerprints are persisted and compared across crawls (near-duplicate detection reads
``simhash64`` hamming distance), so the 2026-10-30 replacement of the ``simhash`` package
(last release 2022) must not move a single bit. These golden values were produced by
``simhash.Simhash(text.split(), f=...)`` 2.1.2 itself before it was removed; the
in-house version also matched it on 915 randomized cases at 32/64/128 bits.
"""

from __future__ import annotations

import pytest

from matrx_scraper.parser.hashing import _simhash_value, compute_simhash

GOLDEN = [
    ("", 0, 0),
    ("hello", 13362634815750784402, 269993362),
    ("The quick brown fox jumps over the lazy dog", 3279227056236043070, 818715454),
    ("price price price shipping returns price", 6601398920714463940, 3117755076),
    ("héllo naïve café 日本語 テスト", 15783236208992926546, 2065382226),
    (
        "Acme Widgets Inc sells industrial widgets gaskets and valves to manufacturers across "
        "North America since 1984 with same day shipping",
        6059941939656720736,
        1354432864,
    ),
]


@pytest.mark.parametrize(("text", "v64", "v32"), GOLDEN, ids=[g[0][:16] or "empty" for g in GOLDEN])
def test_values_match_the_retired_package(text: str, v64: int, v32: int) -> None:
    assert _simhash_value(text.split(), 64) == v64
    assert _simhash_value(text.split(), 32) == v32


def test_compute_simhash_keeps_its_signed_64_bit_storage_form() -> None:
    text, v64, _ = GOLDEN[1]
    assert compute_simhash(text) == (v64 - 2**64 if v64 >= 2**63 else v64)


def test_a_page_with_an_outline_keeps_every_hash() -> None:
    """The 2026-10-30 retirement left ``compute_simhash_from_outline`` reading the deleted
    ``_SIMHASH_AVAILABLE`` flag: every page WITH an outline raised NameError, which
    ``ParserOrchestrator._compute_hashes`` swallowed into ``{}``, so the page lost all three hashes."""
    from matrx_scraper.parser.hashing import compute_hashes, compute_simhash_from_outline

    outline = {"H1: Acme Widgets": [], "H2: Shipping & returns": []}
    assert compute_simhash_from_outline(outline) == compute_simhash("Acme Widgets\nShipping returns")
    hashes = compute_hashes("Acme Widgets sells industrial widgets", outline)
    assert hashes["simhash"] == compute_simhash("Acme Widgets sells industrial widgets")
    assert hashes["outline_simhash"] == compute_simhash_from_outline(outline)
