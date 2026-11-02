"""Phase D — pure value-vs-value matchers (matrx_rag.kg_matching).

Fully unit-testable without a DB or network. Covers:

* exact: phone variants normalize-equal, email case-insensitive, url canonical.
* fuzzy: "John Smith" ~ "J. Smith" above threshold; unrelated below; containment.
* semantic: skipped when no embedder; matches above cosine threshold when one
  is injected.
* threshold boundaries.
"""

from __future__ import annotations

import pytest
from matrx_rag.kg_matching import (
    DEFAULT_FUZZY_THRESHOLD,
    cosine_similarity,
    fuzzy_name_ratio,
    match_values,
    normalize_email,
    normalize_phone,
    normalize_url,
)

# ---------------------------------------------------------------------------
# Normalizers
# ---------------------------------------------------------------------------


def test_normalize_phone_variants_equal():
    assert normalize_phone("(555) 010-0100") == normalize_phone("555-010-0100")
    assert normalize_phone("555.010.0100") == normalize_phone("5550100100")
    # 10-digit NANP gets a +1 prefix.
    assert normalize_phone("5550100100") == "+15550100100"
    # 11-digit leading-1.
    assert normalize_phone("1-555-010-0100") == "+15550100100"


def test_normalize_email_case_insensitive():
    assert normalize_email("  Jane.Doe@Example.COM ") == "jane.doe@example.com"


def test_normalize_url_canonical():
    assert normalize_url("https://Example.com/") == "example.com"
    assert normalize_url("http://www.Example.com") == "example.com"
    assert normalize_url("https://example.com/Path/To") == "example.com/Path/To"


# ---------------------------------------------------------------------------
# exact strategy
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_exact_phone_match():
    m = await match_values("phone", "(555) 010-0100", "string", "555-010-0100")
    assert m is not None
    assert m.match_kind == "exact"
    assert m.confidence == 1.0


@pytest.mark.asyncio
async def test_exact_email_case_insensitive_match():
    m = await match_values("email", "JANE@EXAMPLE.COM", "string", "jane@example.com")
    assert m is not None and m.match_kind == "exact"


@pytest.mark.asyncio
async def test_exact_url_match():
    m = await match_values("url", "https://Example.com/", "string", "example.com")
    assert m is not None and m.match_kind == "exact"


@pytest.mark.asyncio
async def test_exact_phone_mismatch_no_fuzzy_fallthrough():
    # One digit off is a DIFFERENT phone — not a fuzzy hit, no embedder ⇒ None.
    m = await match_values("phone", "555-010-0101", "string", "555-010-0100")
    assert m is None


# ---------------------------------------------------------------------------
# fuzzy strategy
# ---------------------------------------------------------------------------


def test_fuzzy_ratio_containment():
    # "Acme" is a token-subset of "Acme Corp" ⇒ boosted to >= 0.9.
    assert fuzzy_name_ratio("Acme", "Acme Corp") >= 0.9


@pytest.mark.asyncio
async def test_fuzzy_name_match_above_threshold():
    m = await match_values("person", "John Smith", "string", "John Smith")
    assert m is not None and m.match_kind == "fuzzy"
    assert m.confidence >= DEFAULT_FUZZY_THRESHOLD


@pytest.mark.asyncio
async def test_fuzzy_initials_containment():
    # "J Smith" token-subset of "John Smith"? No — "j" not in "john smith" tokens.
    # But "John Smith" vs "John  Smith" (extra space) normalizes equal.
    m = await match_values("person", "John  Smith", "string", "John Smith")
    assert m is not None and m.match_kind == "fuzzy"


@pytest.mark.asyncio
async def test_fuzzy_organization_close():
    m = await match_values("organization", "Acme Corporation", "string", "Acme Corp")
    # Containment boost: "acme corp" tokens... "corp" in "acme corporation"? yes;
    # "acme" in "acme corporation"? yes ⇒ >= 0.9.
    assert m is not None and m.match_kind == "fuzzy"
    assert m.confidence >= DEFAULT_FUZZY_THRESHOLD


@pytest.mark.asyncio
async def test_fuzzy_unrelated_below_threshold():
    m = await match_values("person", "John Smith", "string", "Zara Okonkwo")
    assert m is None


# ---------------------------------------------------------------------------
# semantic strategy
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_semantic_skipped_when_no_embedder():
    # concept is a fuzzy kind, but two unrelated concepts won't pass fuzzy and
    # without an embedder semantic can't run ⇒ None.
    m = await match_values("concept", "quarterly planning", "string", "budget review")
    assert m is None


@pytest.mark.asyncio
async def test_semantic_match_with_embedder():
    # Identical embedding for any text ⇒ cosine 1.0 ⇒ semantic match.
    # Use a SCOPE-LINKABLE kind (organization) with dissimilar surface forms so
    # the exact/fuzzy paths fall through to the semantic strategy. (concept is
    # rejected at entry by STOP rule 7, so it can't exercise this path.)
    async def embedder(_text: str) -> list[float]:
        return [1.0, 0.0, 0.0]

    m = await match_values("organization", "Globex", "string", "Initech", embedder=embedder)
    assert m is not None and m.match_kind == "semantic"
    assert m.confidence == pytest.approx(1.0)


@pytest.mark.asyncio
async def test_semantic_below_threshold_no_match():
    # Orthogonal vectors ⇒ cosine 0.0 ⇒ below threshold ⇒ None.
    calls = {"n": 0}

    async def embedder(_text: str) -> list[float]:
        calls["n"] += 1
        return [1.0, 0.0] if calls["n"] == 1 else [0.0, 1.0]

    m = await match_values("concept", "alpha", "string", "beta", embedder=embedder)
    assert m is None


@pytest.mark.asyncio
async def test_semantic_only_for_text_slots():
    # A 'number' value_type slot is not free-form prose ⇒ semantic never runs
    # even with an embedder; 'date' entity isn't a fuzzy kind ⇒ None.
    async def embedder(_text: str) -> list[float]:
        return [1.0, 0.0]

    m = await match_values("date", "2026-01-01", "number", "42", embedder=embedder)
    assert m is None


def test_cosine_similarity_basics():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)
    assert cosine_similarity([], [1.0]) == 0.0


# ---------------------------------------------------------------------------
# 2026-06-04: containment-boost noise guard + kind→slot compatibility
# ---------------------------------------------------------------------------


def test_fuzzy_containment_boost_blocked_for_noise_token():
    """`'hospital'` is a known common-noun noise token; containment must NOT
    lift it to 0.9 against `'Mercy Hospital'`."""
    assert fuzzy_name_ratio("hospital", "Mercy Hospital") < 0.9


def test_fuzzy_containment_boost_blocked_for_3char_fragment():
    """3-char single tokens like 'mr' / 'dr' / 'the' are below the floor."""
    assert fuzzy_name_ratio("mr", "Mr Smith") < 0.9
    assert fuzzy_name_ratio("the", "the patient came in") < 0.9


def test_fuzzy_containment_boost_works_for_4char_singletoken_org():
    """Real 4-char single-token org abbreviations (Acme, Sony, Ford) still
    boost — only short fragments and known noise tokens are blocked."""
    assert fuzzy_name_ratio("Acme", "Acme Corp") >= 0.9
    assert fuzzy_name_ratio("Sony", "Sony Pictures") >= 0.9


@pytest.mark.asyncio
async def test_date_entity_does_not_fuzzy_match_string_slot():
    """A date entity must NOT fuzzy/semantic-match a free-form string slot.
    Before the gate, '11/16/2023' was being matched against any string slot
    the user had with that year in it (production e2e Nov-2023). Even with
    a perfect-cosine embedder, the gate blocks the match."""

    async def embedder(_text: str) -> list[float]:
        return [1.0, 0.0, 0.0]

    m = await match_values(
        "date",
        "2023-11-16",
        "string",
        "Notes from 2023-11-16",
        embedder=embedder,
    )
    assert m is None


@pytest.mark.asyncio
async def test_concept_does_not_fuzzy_match() -> None:
    """`concept` is excluded from fuzzy matching entirely — too generic.
    Even identical strings shouldn't fuzzy-match for concept."""
    m = await match_values("concept", "annual budget review", "string", "annual budget review")
    # No embedder ⇒ fuzzy blocked by gate ⇒ None
    assert m is None


@pytest.mark.asyncio
async def test_concept_never_scope_links_even_with_embedder() -> None:
    """STOP rule 7: concepts are NEVER scope-linked. match_values rejects the
    concept kind at entry — even a perfect-cosine embedder cannot produce a
    scope-association match. (Concepts still flow through NER + the entity map
    and stay valid for pure retrieval that calls the semantic strategy
    directly; they just never scope-link through match_values.)"""

    async def embedder(_text: str) -> list[float]:
        return [1.0, 0.0, 0.0]

    m = await match_values(
        "concept",
        "quarterly planning",
        "string",
        "Q4 financial planning",
        embedder=embedder,
    )
    assert m is None
