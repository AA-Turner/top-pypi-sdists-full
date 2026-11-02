"""Pure value-vs-value matchers for KG entity → scope-item slot association.

Phase D of the Knowledge-Graph plan. This module is **pure**: it compares a KG
entity value against a scope-item slot value and returns a typed :class:`Match`
(or ``None``). It performs NO database reads and imports nothing from aidream —
the Package Independence Rule.

.. deprecated:: 2026-06-12
   The aidream consumer (``auto_ingest/suggestions.py``, the value×value
   matching loop) was deleted when files/notes moved fully onto the agent
   orchestrator (``orchestrate_for_source`` → ``ner_document_orienter``: one
   LLM call over the full scope tree, no value×value matrix, no embeddings).
   These pure matchers now have no host consumer. They are kept as a tested,
   standalone matrx-rag export for potential reuse; if none reappears, remove
   them in a matrx-rag-scoped cleanup. **Do not wire this back into the hot
   path** — the value-matching loop is the exact design the orchestrator
   replaced (and the one that risked the per-entity embedding blow-up).

Three strategies, tried in order of decreasing confidence:

* **exact** — normalize both sides by entity kind (phone → digits/E.164-ish,
  email → strip+lower, url → strip scheme/trailing-slash/lower-host), then ``==``.
  Confidence 1.0.
* **fuzzy** — normalized Levenshtein ratio over names/addresses/organizations.
  Default threshold 0.85. Confidence = the ratio.
* **semantic** — cosine over two embedding vectors for free-form text slots.
  The embedder is INJECTED (``embedder`` kwarg). Default threshold 0.78.
  Confidence = the cosine. With no embedder configured, semantic is skipped
  (returns ``None``) — exact + fuzzy still run.

Everything here is synchronous and dependency-free EXCEPT the optional
``embedder`` callable (which the caller may pass as async). ``match_values`` is
async only so it can ``await`` the injected embedder; the exact/fuzzy paths
never touch it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Awaitable, Callable, Literal

MatchKind = Literal["exact", "fuzzy", "semantic"]

# STOP RULE 7 (common-docs/projects/knowledge-system/vision/02_KNOWLEDGE_ARCHITECTURE.md §7 / common-docs/projects/knowledge-system/vision/03_KNOWLEDGE_MODULE.md §3):
# CONCEPTS are thematic ideas ("back pain", "negligence") tagged for semantic
# retrieval. They are NEVER scope-linked. Only ENTITIES (named things with
# identity — "John Smith", "Case 2024-CV-001") may produce scope-association
# matches. Enforced here by _SCOPE_LINKABLE_KINDS: every call to match_values
# for a concept kind returns None immediately, regardless of strategy.
_SCOPE_LINKABLE_KINDS: frozenset[str] = frozenset(
    {"person", "organization", "address", "phone", "email", "url", "date"}
)

# The entity kinds the matchers recognize. Mirrors matrx_rag.ner.NER_KINDS.
# Kinds with a canonical normal form go through the exact path first.
_EXACT_KINDS: frozenset[str] = frozenset({"phone", "email", "url"})
# Kinds where a fuzzy name comparison is meaningful.
# NOTE: 'concept' is intentionally excluded — concepts are not scope-linkable
# (STOP rule 7). They still flow through NER and the entity map; they just
# never produce scope-association matches.
_FUZZY_KINDS: frozenset[str] = frozenset(
    {"person", "organization", "address"}
)

DEFAULT_FUZZY_THRESHOLD = 0.85
DEFAULT_SEMANTIC_THRESHOLD = 0.78

# Slot value_type values that carry free-form text the semantic path can embed.
# (ctx_context_items.value_type enum: string|number|boolean|object|array|
#  document|reference — only 'string' is free-form prose we'd embed.)
_SEMANTIC_SLOT_TYPES: frozenset[str] = frozenset({"string", "text"})

# Per-kind compatibility maps — which ctx_context_items.value_type values a
# given entity kind is ALLOWED to fuzzy/semantic-match. These gates exist
# because in production we saw `'11/16/2023'` fuzzy-matched to free-form
# string slots and bare `'hospital'` fuzzy-matched to slots containing
# 'hospital' (Mercy Hospital, Hospital Notes, …).
#
# Two separate maps because the right answer differs:
#   * fuzzy is name-similarity-based — too risky for bare common words; and
#     meaningless for `date` against a free-form `string`.
#   * semantic is embedding-cosine — good for free-form prose; `date` stays
#     strict: a date entity should only ever match a date-typed slot.
#
# NOTE: 'concept' entries are kept below for documentation purposes only —
# match_values() rejects concept kind at entry (STOP rule 7 guard via
# _SCOPE_LINKABLE_KINDS) before these maps are consulted for scope-linking.
# Concepts remain valid for pure RETRIEVAL contexts that call the semantic
# strategies directly without going through match_values().
#
# A `None` value means "any slot type" (back-compat for unknown kinds).
_FUZZY_KIND_TO_SLOT_TYPES: dict[str, frozenset[str]] = {
    "person": frozenset({"string", "text", "reference"}),
    "organization": frozenset({"string", "text", "reference"}),
    "address": frozenset({"string", "text"}),
    "phone": frozenset({"string", "text", "phone"}),
    "email": frozenset({"string", "text", "email"}),
    "url": frozenset({"string", "text", "url"}),
    "date": frozenset({"date", "datetime"}),
    "concept": frozenset(),  # never fuzzy-match — too generic
}

_SEMANTIC_KIND_TO_SLOT_TYPES: dict[str, frozenset[str]] = {
    "person": frozenset({"string", "text", "reference"}),
    "organization": frozenset({"string", "text", "reference"}),
    "address": frozenset({"string", "text"}),
    "phone": frozenset({"string", "text", "phone"}),
    "email": frozenset({"string", "text", "email"}),
    "url": frozenset({"string", "text", "url"}),
    "date": frozenset({"date", "datetime"}),  # still strict — a date is a date
    "concept": frozenset({"string", "text"}),  # the legitimate semantic case
}


def _kind_fuzzy_compatible(entity_kind: str, slot_value_type: str) -> bool:
    allowed = _FUZZY_KIND_TO_SLOT_TYPES.get(entity_kind)
    if allowed is None:
        return True
    return slot_value_type in allowed


def _kind_semantic_compatible(entity_kind: str, slot_value_type: str) -> bool:
    allowed = _SEMANTIC_KIND_TO_SLOT_TYPES.get(entity_kind)
    if allowed is None:
        return True
    return slot_value_type in allowed


# A small denylist of bare common words that, even after canonicalisation,
# should never be the basis for a fuzzy match. These are the words GLiNER
# routinely mis-tags as entities; canonicalize_ner_entity drops them at
# extraction time, but if anything slips through (LLM finisher accepting
# them, an older row in the DB), the matcher refuses to lift them to 0.9
# via the containment boost.
_FUZZY_NOISE_TOKENS: frozenset[str] = frozenset({
    "hospital", "clinic", "patient", "paciente", "doctor", "doctora",
    "providence", "center", "centro", "office", "company", "department",
})

# An async OR sync callable: text -> embedding vector (list[float]).
Embedder = Callable[[str], "Awaitable[list[float]] | list[float]"]


@dataclass(frozen=True)
class Match:
    """A positive match between an entity value and a slot value."""

    match_kind: MatchKind
    confidence: float


# ---------------------------------------------------------------------------
# Normalizers (pure)
# ---------------------------------------------------------------------------


def normalize_email(value: str) -> str:
    """Strip surrounding whitespace + lowercase. Email is case-insensitive in
    practice for the domain (and, for our matching purposes, the local part)."""
    return value.strip().lower()


def normalize_url(value: str) -> str:
    """Canonicalize a URL for equality: drop the scheme, lowercase the host,
    strip a single trailing slash. Deliberately conservative — we only want
    ``https://Example.com/`` to equal ``example.com``, not aggressive path
    rewriting that could merge distinct resources."""
    v = value.strip()
    for scheme in ("https://", "http://", "ftp://"):
        if v.lower().startswith(scheme):
            v = v[len(scheme) :]
            break
    if v.lower().startswith("www."):
        v = v[4:]
    v = v.rstrip("/")
    # Lowercase only the host portion (before the first '/'), preserve path case.
    if "/" in v:
        host, _, rest = v.partition("/")
        return f"{host.lower()}/{rest}"
    return v.lower()


def normalize_phone(value: str) -> str:
    """Digits-only normalization with a light country-code heuristic.

    We don't depend on the ``phonenumbers`` package (not a matrx-rag dep), so
    this is a pragmatic best-effort: keep digits (and a leading ``+``); if the
    result is a 10-digit NANP number, prefix ``+1``; if 11 digits starting with
    ``1``, prefix ``+``. Anything else is returned as ``+<digits>`` when it had a
    leading ``+``, else just the digits. NOTE: this is a heuristic, not a true
    E.164 parser — adequate for matching ``(555) 010-0100`` ⇔ ``555-010-0100``
    within one locale; international edge cases may not normalize identically.
    """
    raw = value.strip()
    had_plus = raw.startswith("+")
    digits = "".join(ch for ch in raw if ch.isdigit())
    if not digits:
        return ""
    if not had_plus:
        if len(digits) == 10:
            return "+1" + digits
        if len(digits) == 11 and digits.startswith("1"):
            return "+" + digits
        return digits
    return "+" + digits


def _normalize_for_kind(kind: str, value: str) -> str:
    if kind == "email":
        return normalize_email(value)
    if kind == "url":
        return normalize_url(value)
    if kind == "phone":
        return normalize_phone(value)
    return value.strip()


def _normalize_name(value: str) -> str:
    """Lowercase + collapse internal whitespace + drop a small set of name
    punctuation (periods after initials, commas). Used by the fuzzy path so
    ``J. Smith`` and ``J Smith`` compare cleanly."""
    cleaned = value.strip().lower().replace(".", " ").replace(",", " ")
    return " ".join(cleaned.split())


# ---------------------------------------------------------------------------
# Fuzzy: pure-python normalized Levenshtein ratio (no external deps)
# ---------------------------------------------------------------------------


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    # Two-row dynamic programming — O(len(a) * len(b)) time, O(len(b)) space.
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr[j] = min(
                prev[j] + 1,        # deletion
                curr[j - 1] + 1,    # insertion
                prev[j - 1] + cost,  # substitution
            )
        prev = curr
    return prev[-1]


def levenshtein_ratio(a: str, b: str) -> float:
    """Similarity in [0.0, 1.0]: ``1 - distance / max(len)``. 1.0 == identical."""
    if not a and not b:
        return 1.0
    longest = max(len(a), len(b))
    if longest == 0:
        return 1.0
    return 1.0 - (_levenshtein(a, b) / longest)


def fuzzy_name_ratio(entity_value: str, slot_value: str) -> float:
    """Normalized-name fuzzy ratio. Also rewards a containment match (one name
    being a prefix/substring of the other — ``Acme Corp`` ⊂ ``Acme Corporation``)
    so an abbreviated entity still matches its fuller slot value.

    Containment boost is GATED (2026-06-04) to avoid lifting single common
    words to 0.9:

      * the shorter side must be ≥2 tokens OR ≥4 characters (so 3-char
        fragments like 'mr', 'dr', 'the' don't get boosted)
      * neither side may be a known common-noun noise token

    Without the gate, a `'hospital'` entity (single short common word)
    cleared the 0.85 fuzzy threshold against any slot containing the word
    `'hospital'` ('Mercy Hospital', 'Hospital Notes', etc.) and produced
    junk suggestions in production. The noise-token denylist is the
    primary defense; the length floor is a backstop for noise we haven't
    enumerated.
    """
    a = _normalize_name(entity_value)
    b = _normalize_name(slot_value)
    if not a or not b:
        return 0.0
    base = levenshtein_ratio(a, b)
    short, long = (a, b) if len(a) <= len(b) else (b, a)
    short_tokens = short.split()
    if not short_tokens:
        return base
    # Containment-boost eligibility: substantial-enough surface on both sides
    # AND not a known noise token. A short fragment / common word stays at
    # its raw Levenshtein ratio.
    short_eligible = (len(short_tokens) >= 2) or (len(short) >= 4)
    short_noisy = short in _FUZZY_NOISE_TOKENS
    long_noisy = long in _FUZZY_NOISE_TOKENS
    if short_eligible and not (short_noisy or long_noisy):
        if all(tok in long for tok in short_tokens):
            base = max(base, 0.9)
    return base


# ---------------------------------------------------------------------------
# Semantic: cosine over injected embeddings
# ---------------------------------------------------------------------------


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(x * y for x, y in zip(v1, v2))
    n1 = math.sqrt(sum(x * x for x in v1))
    n2 = math.sqrt(sum(y * y for y in v2))
    if n1 == 0.0 or n2 == 0.0:
        return 0.0
    return dot / (n1 * n2)


async def _embed(embedder: Embedder, text: str) -> list[float]:
    out = embedder(text)
    if hasattr(out, "__await__"):
        return await out  # type: ignore[no-any-return]
    return out  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# The single entry point
# ---------------------------------------------------------------------------


async def match_values(
    entity_kind: str,
    entity_value: str,
    slot_value_type: str,
    slot_value: str,
    *,
    embedder: Embedder | None = None,
    fuzzy_threshold: float = DEFAULT_FUZZY_THRESHOLD,
    semantic_threshold: float = DEFAULT_SEMANTIC_THRESHOLD,
) -> Match | None:
    """Compare one entity value to one slot value. Returns the best :class:`Match`
    or ``None`` if nothing clears its threshold.

    Strategy order:
      1. exact (phone/email/url) — normalized equality, confidence 1.0.
      2. fuzzy (person/organization/address) — Levenshtein ratio ≥
         ``fuzzy_threshold``.
      3. semantic (free-form string slots, any kind) — cosine ≥
         ``semantic_threshold``; requires an ``embedder``. Skipped when no
         embedder is provided.

    Pure: no DB, no aidream imports. Never raises for a normal "no match" — it
    returns ``None``.

    STOP RULE 7 (common-docs/projects/knowledge-system/vision/02_KNOWLEDGE_ARCHITECTURE.md §7): concepts are NEVER scope-linked.
    A concept entity kind returns ``None`` immediately — concepts are
    thematic ideas used for semantic retrieval, not named scope-linkable
    entities. This is a hard structural rule, not a threshold gate.

    Kind→slot-type compatibility (2026-06-04): some entity kinds are
    forbidden from matching certain slot types. A ``date`` entity won't
    fuzzy/semantic-match a free-form ``string`` slot anymore. This kills a
    whole class of nonsense suggestions (every note containing '11/16/2023'
    showing up as a date-slot suggestion in production). The gate doesn't
    affect explicit slot types — a date entity still matches a date slot.
    """
    if not entity_value or not slot_value:
        return None

    # STOP RULE 7: only scope-linkable kinds (named entities with identity) may
    # produce scope-association matches. Concepts ("back pain", "negligence")
    # are thematic ideas used for semantic retrieval — they must NEVER be
    # scope-linked. Any kind absent from _SCOPE_LINKABLE_KINDS is rejected here
    # before any strategy runs, so no fuzzy/semantic path can bypass the rule.
    if entity_kind not in _SCOPE_LINKABLE_KINDS:
        return None

    ev = entity_value.strip()
    sv = slot_value.strip()

    # ── 1. exact ────────────────────────────────────────────────────────────
    if entity_kind in _EXACT_KINDS:
        if _normalize_for_kind(entity_kind, ev) == _normalize_for_kind(entity_kind, sv):
            return Match(match_kind="exact", confidence=1.0)
        # Phone/email/url that don't normalize-equal don't fall through to
        # fuzzy (a one-digit-off phone is a DIFFERENT phone, not a fuzzy hit).
        # They MAY still match semantically if the slot is free-form text and an
        # embedder is available — fall through to the semantic block.

    # ── 2. fuzzy ────────────────────────────────────────────────────────────
    if entity_kind in _FUZZY_KINDS and _kind_fuzzy_compatible(entity_kind, slot_value_type):
        ratio = fuzzy_name_ratio(ev, sv)
        if ratio >= fuzzy_threshold:
            return Match(match_kind="fuzzy", confidence=round(ratio, 4))

    # ── 3. semantic ─────────────────────────────────────────────────────────
    if (
        embedder is not None
        and slot_value_type in _SEMANTIC_SLOT_TYPES
        and _kind_semantic_compatible(entity_kind, slot_value_type)
    ):
        try:
            e_vec = await _embed(embedder, ev)
            s_vec = await _embed(embedder, sv)
        except Exception:
            # Embedder failure is a "no semantic signal", not an error that
            # should kill the whole match attempt. Exact/fuzzy already ran.
            return None
        cos = cosine_similarity(e_vec, s_vec)
        if cos >= semantic_threshold:
            return Match(match_kind="semantic", confidence=round(cos, 4))

    return None


__all__ = [
    "Match",
    "MatchKind",
    "Embedder",
    "match_values",
    "normalize_email",
    "normalize_url",
    "normalize_phone",
    "levenshtein_ratio",
    "fuzzy_name_ratio",
    "cosine_similarity",
    "DEFAULT_FUZZY_THRESHOLD",
    "DEFAULT_SEMANTIC_THRESHOLD",
]
