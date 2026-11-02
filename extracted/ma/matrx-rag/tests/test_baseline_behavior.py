"""Phase 2c — frozen-behavior baseline.

The Phase 2a–2b/iv refactor moved ~9,400 LOC of RAG code out of
``aidream/services/rag`` into the matrx-rag package and introduced five
injection seams. Each phase ran the existing aidream test suite to
verify no behavior change.

What this suite adds: a **regression net for the package's pure
deterministic transformations** so future commits (including the Phase
2b/iv follow-on call-site migrations) can be diffed against a frozen
expected output.

The functions under test here are intentionally chosen for being:
* Pure (or near-pure with mockable seams) — output is a function of
  input only.
* Algorithm-heavy — chunking strategies, RRF fusion, MMR
  diversification, priority-boosted ranking, payload→text projection.
  Accidental drift in any of these would silently change retrieval
  quality without breaking any existing test.

Non-determinism is monkey-patched out:
* ``uuid.uuid4`` → a counter-based UUID so chunk_id values are stable.
* Env vars touched by ``_priority_boost_*`` are reset to defaults so
  the boost scale is canonical.

What this suite does NOT cover (deferred):
* Full HTTP-route capture-and-replay (Phase 2c was originally scoped to
  capture pre-migration HTTP traffic; we're past that point, so the
  baseline is established at the algorithm layer instead).
* PDF pipeline orchestration end-to-end (covered by aidream's existing
  integration tests via the shim).
"""

from __future__ import annotations

import uuid

import pytest
from matrx_rag.chunking import Chunk, chunk_code, chunk_text
from matrx_rag.extraction_indexing import payload_to_indexable_text
from matrx_rag.search import _apply_priority, _mmr_filter, _rrf_fuse, _token_set

# ---------------------------------------------------------------------------
# Deterministic UUID fixture — chunking allocates chunk_ids via uuid4.
# Patch it to a counter so the baseline IDs are stable across runs.
# ---------------------------------------------------------------------------


@pytest.fixture
def deterministic_uuid(monkeypatch):
    counter = {"n": 0}

    def _fake_uuid4() -> uuid.UUID:
        counter["n"] += 1
        # Construct a v4-ish UUID from a fixed prefix + counter.
        return uuid.UUID(f"00000000-0000-4000-8000-{counter['n']:012x}")

    monkeypatch.setattr(uuid, "uuid4", _fake_uuid4)
    return counter


@pytest.fixture(autouse=True)
def _reset_priority_env(monkeypatch):
    """Clear the (now-defunct) priority-boost env vars for hygiene. They were
    eradicated in favor of code constants (PRIORITY_BOOST_* in search.py); the
    code no longer reads them, but stray values in the dev shell shouldn't even
    appear to matter. The code-constant contract is asserted explicitly in
    test_apply_priority_{enabled,scale}_is_a_code_constant."""
    monkeypatch.delenv("RAG_PRIORITY_BOOST_SCALE", raising=False)
    monkeypatch.delenv("RAG_USE_PRIORITY_BOOST", raising=False)


# ---------------------------------------------------------------------------
# chunk_text — prose hierarchical chunking
# ---------------------------------------------------------------------------


def _chunk_to_baseline(c: Chunk) -> dict:
    """Project a Chunk to the fields we lock in the baseline."""
    return {
        "chunk_id": c.chunk_id,
        "parent_chunk_id": c.parent_chunk_id,
        "chunk_index": c.chunk_index,
        "chunk_kind": c.chunk_kind,
        "content_text": c.content_text,
        "token_count": c.token_count,
        "language": c.language,
        "metadata": c.metadata,
    }


def test_chunk_text_empty_returns_empty(deterministic_uuid):
    assert chunk_text("") == []
    assert chunk_text("   \n\t  ") == []
    assert chunk_text("\n\n") == []


def test_chunk_text_short_input_fits_in_one_parent(deterministic_uuid):
    """A short prose input under CHILD_SIZE produces ONE parent and no child:
    its only child would duplicate the parent's text (2026-10-11 — the identical
    child was a second row, a second embedding and a double search hit)."""
    text = "Hello world. This is a short test sentence."
    chunks = chunk_text(text, language="en")
    assert len(chunks) == 1

    (parent,) = chunks
    assert parent.parent_chunk_id is None
    assert parent.chunk_index == 0
    assert parent.chunk_kind == "text"
    assert parent.content_text == text
    assert parent.language == "en"
    assert parent.metadata == {"role": "parent", "parent_index": 0}
    assert parent.token_count > 0


def test_chunk_text_long_input_splits_to_multiple_parents(deterministic_uuid):
    """A long input above PARENT_SIZE (1500 tokens) produces multiple
    parents with at least one child each. Parents come before children
    of subsequent parents in flat ordering? No — emits parent then its
    children in sequence per parent block."""
    para = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20
    long_text = "\n\n".join([para] * 50)  # ~comfortably over 1500 tokens

    chunks = chunk_text(long_text, language="en")

    parents = [c for c in chunks if c.parent_chunk_id is None]
    children = [c for c in chunks if c.parent_chunk_id is not None]
    assert len(parents) >= 2, "long input should split into multiple parents"
    assert len(children) >= len(parents), "every parent has >=1 child"

    # Every child references a parent that appears earlier in the flat
    # list (parents-before-children-per-block ordering).
    parent_ids_seen: set[str] = set()
    for c in chunks:
        if c.parent_chunk_id is None:
            parent_ids_seen.add(c.chunk_id)
        else:
            assert c.parent_chunk_id in parent_ids_seen, (
                f"child {c.chunk_id} references unseen parent {c.parent_chunk_id}"
            )

    # chunk_index is dense (0..N-1) and stable.
    for i, c in enumerate(chunks):
        assert c.chunk_index == i

    # Parent metadata's parent_index tracks the parent's ordinal.
    parent_indices = [c.metadata["parent_index"] for c in parents]
    assert parent_indices == list(range(len(parents)))


def test_chunk_text_baseline_three_paragraph_fixture(deterministic_uuid):
    """Three short paragraphs, all fitting in one parent block. The
    exact split is langchain-dependent but the parent/child structure
    is stable."""
    fixture = (
        "The first paragraph introduces the concept.\n\n"
        "The second paragraph develops the idea further.\n\n"
        "The third paragraph offers a concluding thought."
    )
    chunks = chunk_text(fixture)
    # All three fit under PARENT_SIZE so we get one parent.
    parents = [c for c in chunks if c.parent_chunk_id is None]
    assert len(parents) == 1
    parent = parents[0]
    assert parent.content_text == fixture
    # Small enough for one child — which would equal the parent, so none is emitted.
    children = [c for c in chunks if c.parent_chunk_id == parent.chunk_id]
    for ch in children:
        assert ch.content_text in fixture
        assert ch.content_text.strip() != fixture.strip()


# ---------------------------------------------------------------------------
# chunk_code — line-window code chunking
# ---------------------------------------------------------------------------


def test_chunk_code_empty_returns_empty(deterministic_uuid):
    assert chunk_code("") == []
    assert chunk_code("   ") == []


def test_chunk_code_small_file_one_parent_one_child(deterministic_uuid):
    """A small code file (under CODE_CHILD_LINES) emits ONE parent and no child
    (the single child would equal the parent). Note: ``splitlines() + '\\n'.join()``
    strips trailing newlines — locked-in behavior."""
    src = "def hello():\n    return 'world'\n\n\ndef goodbye():\n    return None\n"
    chunks = chunk_code(src, language="python")
    assert len(chunks) == 1

    (parent,) = chunks
    assert parent.chunk_kind == "code_window"
    assert parent.parent_chunk_id is None
    # The chunker rejoins via "\n".join(splitlines()), so a trailing
    # newline on the input is NOT preserved in the chunk text. Baseline.
    assert parent.content_text == src.rstrip("\n")
    assert parent.language == "python"
    assert parent.metadata["role"] == "parent"
    assert parent.metadata["line_start"] == 0
    # line_end equals the number of lines in the parent's content.
    assert parent.metadata["line_end"] == len(src.splitlines())


def test_chunk_code_large_file_splits_with_line_metadata(deterministic_uuid):
    """A code file over 250 lines splits into multiple parents; line_start
    and line_end metadata stay consistent."""
    src = "\n".join(f"line_{i:04d}" for i in range(600))
    chunks = chunk_code(src, language="python")

    parents = [c for c in chunks if c.parent_chunk_id is None]
    children = [c for c in chunks if c.parent_chunk_id is not None]

    # 600 lines / 250 parent window = 3 parents (the windows function
    # advances by step=window-overlap=250 with no overlap at parent level).
    assert len(parents) == 3
    assert parents[0].metadata["line_start"] == 0
    assert parents[1].metadata["line_start"] == 250
    assert parents[2].metadata["line_start"] == 500
    assert all(len(children) > 0 for _ in parents)

    # Every child's [line_start, line_end] sits inside its parent's range.
    parents_by_id = {p.chunk_id: p for p in parents}
    for ch in children:
        parent = parents_by_id[ch.parent_chunk_id]
        assert ch.metadata["line_start"] >= parent.metadata["line_start"]
        assert ch.metadata["line_end"] <= parent.metadata["line_end"]


# ---------------------------------------------------------------------------
# _rrf_fuse — reciprocal rank fusion (pure)
# ---------------------------------------------------------------------------


def test_rrf_fuse_empty_inputs():
    assert _rrf_fuse({}, []) == []


def test_rrf_fuse_single_ranking_preserves_order():
    """A single vector ranking with no lexical input produces a fusion
    output where order matches the vector ranking and scores monotonically
    decrease."""
    vector = {"v0": ["a", "b", "c", "d"]}
    out = _rrf_fuse(vector, [])
    ids = [cid for cid, _ in out]
    scores = [s for _, s in out]
    assert ids == ["a", "b", "c", "d"]
    assert scores == sorted(scores, reverse=True)
    # All scores must be > 0 (RRF formula: 1 / (RRF_K + rank), rank >= 1).
    assert all(s > 0 for s in scores)


def test_rrf_fuse_overlap_boosts_intersection():
    """Documents appearing in BOTH the vector and lexical rankings rank
    higher than documents in only one — that's the whole point of RRF."""
    vector = {"v0": ["a", "b", "c", "d"]}
    lexical = ["c", "b", "e", "f"]
    out = _rrf_fuse(vector, lexical)
    # 'b' and 'c' appear in both — they should rank in the top two.
    top_two = {cid for cid, _ in out[:2]}
    assert top_two == {"b", "c"}


def test_rrf_fuse_multi_query_vector_rankings_accumulate():
    """Two vector queries that both return doc 'x' near the top boost
    'x' above any single-query competitor."""
    vector = {
        "q1": ["x", "y", "z"],
        "q2": ["x", "a", "b"],
    }
    out = _rrf_fuse(vector, [])
    assert out[0][0] == "x"


# ---------------------------------------------------------------------------
# _mmr_filter — greedy MMR diversification (pure)
# ---------------------------------------------------------------------------


def test_mmr_filter_keeps_diverse_short_snippets():
    """Snippets with < 8 unique tokens always pass — never filtered by MMR
    (Jaccard on a handful of tokens is noise)."""
    ordered = ["a", "b", "c"]
    rows = {
        "a": {"content_text": "short text one"},
        "b": {"content_text": "different few words"},
        "c": {"content_text": "yet another tiny one"},
    }
    out = _mmr_filter(ordered, rows, threshold=0.5, keep=10)
    assert out == ordered


def test_mmr_filter_drops_near_duplicate_long_snippets():
    """Long snippets with high token-overlap are filtered out by MMR.
    Use 8+ unique tokens of length >= 3 so MMR engages."""
    long_a = "alpha beta gamma delta epsilon zeta eta theta"
    long_b = "alpha beta gamma delta epsilon zeta eta theta"  # identical
    long_c = "lambda mu nu omicron pi rho sigma tau"  # disjoint vocab
    ordered = ["a", "b", "c"]
    rows = {
        "a": {"content_text": long_a},
        "b": {"content_text": long_b},
        "c": {"content_text": long_c},
    }
    out = _mmr_filter(ordered, rows, threshold=0.5, keep=10)
    # 'a' is kept; 'b' is dropped (Jaccard == 1.0 with 'a'); 'c' is
    # kept (Jaccard == 0 with 'a').
    assert out == ["a", "c"]


def test_mmr_filter_respects_keep_cap():
    """MMR stops at ``keep`` retained candidates regardless of how many
    remain."""
    ordered = [str(i) for i in range(10)]
    rows = {
        str(i): {"content_text": f"unique_word_{i} more_distinct_text_{i} payload"}
        for i in range(10)
    }
    out = _mmr_filter(ordered, rows, threshold=0.5, keep=3)
    assert out == ["0", "1", "2"]


def test_mmr_filter_missing_row_is_skipped():
    """Candidates with no matching row are silently skipped."""
    ordered = ["a", "missing", "b"]
    rows = {
        "a": {"content_text": "first"},
        "b": {"content_text": "second"},
    }
    out = _mmr_filter(ordered, rows, threshold=0.5, keep=10)
    assert out == ["a", "b"]


# 8-token snippets (past the < 8 bypass) sharing 5 tokens → Jaccard 5/11 ≈ 0.45.
# That sits between the same-source-variant bar (0.45) and the diversity bar
# (0.72), which is exactly the cross-granularity-duplicate band.
_MMR_A = "alpha beta gamma delta epsilon zeta eta theta"
_MMR_B = "alpha beta gamma delta epsilon omega psi chi"  # shares 5/8 with A → ~0.45


def test_mmr_filter_dedupes_same_source_cross_granularity():
    """A `child` chunk and the `chunked_fine` window of the SAME page (same
    source, different granularity, ~0.45 Jaccard) collapse to one — even though
    that overlap is below the cross-source diversity threshold."""
    rows = {
        "a": {"content_text": _MMR_A, "source_id": "src-1", "chunk_kind": "child"},
        "b": {
            "content_text": _MMR_B,
            "source_id": "src-1",
            "chunk_kind": "chunked_fine",
        },
    }
    out = _mmr_filter(["a", "b"], rows, threshold=0.72, keep=10)
    assert out == ["a"]


def test_mmr_filter_keeps_distinct_same_source_same_granularity():
    """Two DISTINCT sections of the same document at the SAME granularity that
    happen to share ~0.45 vocabulary are KEPT — the tighter bar is reserved for
    cross-granularity variants, so dense docs aren't over-collapsed (the P3
    guard)."""
    rows = {
        "a": {"content_text": _MMR_A, "source_id": "src-1", "chunk_kind": "child"},
        "b": {"content_text": _MMR_B, "source_id": "src-1", "chunk_kind": "child"},
    }
    out = _mmr_filter(["a", "b"], rows, threshold=0.72, keep=10)
    assert out == ["a", "b"]


def test_mmr_filter_keeps_moderate_overlap_across_sources():
    """The same ~0.45-Jaccard pair from DIFFERENT sources is kept — the cross-
    source diversity bar (0.72) is unchanged, so distinct documents that share
    vocabulary survive."""
    rows = {
        "a": {"content_text": _MMR_A, "source_id": "src-1", "chunk_kind": "child"},
        "b": {
            "content_text": _MMR_B,
            "source_id": "src-2",
            "chunk_kind": "chunked_fine",
        },
    }
    out = _mmr_filter(["a", "b"], rows, threshold=0.72, keep=10)
    assert out == ["a", "b"]


# ---------------------------------------------------------------------------
# _token_set — lowercase tokenizer for MMR
# ---------------------------------------------------------------------------


def test_token_set_strips_punctuation_and_lowercases():
    """_token_set strips ONLY the chars in its strip-set ('.,;:()[]{}\"`)
    from each word's edges, then lowercases. Embedded chars (like '!')
    and mid-word punctuation are NOT stripped. Locked-in behavior."""
    # Use punctuation that IS in the strip set: ',', '(', ')'.
    assert _token_set("Hello, (World) Greeting") == {"hello", "world", "greeting"}


def test_token_set_does_not_strip_unlisted_punctuation():
    """'!' is not in the strip-set; it survives on the token edge."""
    out = _token_set("World! Hello")
    assert "world!" in out
    assert "hello" in out


def test_token_set_drops_short_tokens():
    """Tokens shorter than 3 chars are dropped."""
    # "is" and "an" are dropped (< 3 chars); "the" and "test" survive.
    assert _token_set("Is an the test") == {"the", "test"}


def test_token_set_deduplicates():
    """Repeated tokens collapse to one (it's a set)."""
    assert _token_set("foo Foo FOO bar") == {"foo", "bar"}


# ---------------------------------------------------------------------------
# _apply_priority — boosted ranking score (pure)
# ---------------------------------------------------------------------------


def test_apply_priority_zero_is_identity():
    """priority=0 returns score unchanged. This is the no-op path that
    makes priority-boost safe to leave on by default."""
    assert _apply_priority(0.85, 0) == 0.85
    assert _apply_priority(0.0, 0) == 0.0


def test_apply_priority_positive_boosts():
    """Default scale is 0.05 — priority=10 produces a 1.5x multiplier."""
    boosted = _apply_priority(1.0, 10)
    assert boosted == pytest.approx(1.5)


def test_apply_priority_negative_demotes():
    """Negative priority shrinks the score."""
    demoted = _apply_priority(1.0, -10)
    assert demoted == pytest.approx(0.5)


def test_apply_priority_enabled_is_a_code_constant(monkeypatch):
    """The priority boost is a CODE constant (PRIORITY_BOOST_ENABLED), not an
    env var. The old RAG_USE_PRIORITY_BOOST override was eradicated (silent-
    env-var policy): setting it must have ZERO effect — the boost stays on."""
    from matrx_rag import search as search_mod

    assert search_mod.PRIORITY_BOOST_ENABLED is True
    monkeypatch.setenv("RAG_USE_PRIORITY_BOOST", "false")
    # Env var is ignored — priority still boosts.
    assert _apply_priority(0.7, 50) != 0.7
    assert search_mod._priority_boost_enabled() is True


def test_apply_priority_scale_is_a_code_constant(monkeypatch):
    """The boost scale is a CODE constant (PRIORITY_BOOST_SCALE_DEFAULT = 0.05),
    not an env var. The old RAG_PRIORITY_BOOST_SCALE override was eradicated:
    setting it must have ZERO effect — the scale stays 0.05 (10 → 1.5x)."""
    from matrx_rag import search as search_mod

    assert search_mod.PRIORITY_BOOST_SCALE_DEFAULT == 0.05
    monkeypatch.setenv("RAG_PRIORITY_BOOST_SCALE", "0.10")
    # Env var is ignored — scale stays the code default (0.05).
    assert _apply_priority(1.0, 10) == pytest.approx(1.5)
    assert search_mod._priority_boost_scale() == 0.05


# ---------------------------------------------------------------------------
# payload_to_indexable_text — extraction payload → embeddable string
# ---------------------------------------------------------------------------


def test_payload_to_text_dict_with_keys():
    payload = {"title": "Invoice 42", "total": 1234.56, "currency": "USD"}
    out = payload_to_indexable_text(payload)
    assert out == "title: Invoice 42\ntotal: 1234.56\ncurrency: USD"


def test_payload_to_text_list_numbers_items():
    payload = ["first", "second", "third"]
    out = payload_to_indexable_text(payload)
    assert out == "1. first\n2. second\n3. third"


def test_payload_to_text_scalar_passes_through():
    assert payload_to_indexable_text("hello") == "hello"
    assert payload_to_indexable_text(42) == "42"
    assert payload_to_indexable_text(True) == "True"


def test_payload_to_text_empty_returns_empty_sentinel():
    """Empty payloads use the 'EMPTY' sentinel so the chunk isn't dropped
    by downstream emptiness checks. Locks the contract added in 2b/i."""
    assert payload_to_indexable_text({}) == "EMPTY"
    assert payload_to_indexable_text([]) == "EMPTY"
    assert payload_to_indexable_text(None) == "EMPTY"


def test_payload_to_text_page_prefixes():
    payload = {"text": "body"}
    out = payload_to_indexable_text(payload, canonical_page=3, source_pages=[3, 4, 5])
    lines = out.split("\n")
    assert lines[0] == "PAGE: 3"
    assert lines[1] == "SOURCE_PAGES: 3, 4, 5"
    assert lines[2] == "text: body"


def test_payload_to_text_nested_object_is_json_encoded():
    """Nested structures are JSON-serialized — preserves order via
    ensure_ascii=False and default=str for arbitrary types."""
    payload = {"meta": {"agent": "doc_extractor", "version": 2}}
    out = payload_to_indexable_text(payload)
    assert out == 'meta: {"agent": "doc_extractor", "version": 2}'


def test_payload_to_text_long_value_truncated_with_marker():
    """Field values over _VALUE_LIMIT (4000 chars) get truncated with a
    sentinel marker so a runaway nested blob doesn't blow up the chunk."""
    long_value = "x" * 5000
    payload = {"big": long_value}
    out = payload_to_indexable_text(payload)
    assert out.endswith("… [truncated]")
    # The keep is _VALUE_LIMIT chars + the truncation marker.
    assert len(out) < 5000 + 100


# ---------------------------------------------------------------------------
# Shim parity — aidream.services.rag.* submodules must expose every
# call-site symbol the host's ~60 import sites depend on.
#
# The submodule shims are where the real risk lives: each one is a
# separate file with its own ``__getattr__`` that proxies to a
# ``matrx_rag.X`` module. If a submodule shim is missing, accidentally
# renamed, or proxies to the wrong target, aidream's call sites break
# even though the top-level ``aidream.services.rag`` shim resolves
# fine.
#
# This test pins a representative cross-section of the actual call-site
# import shapes — chunking, search, extraction, embeddings, ingestion,
# pdf_pipeline, llm, db, library — against the matrx_rag counterparts.
# A missing shim file or a renamed package function fails here.
# ---------------------------------------------------------------------------


# (shim attribute path, matrx_rag attribute path) — locks the
# submodule-level proxy resolution to the package module.
_SHIM_CALL_SITE_SYMBOLS: list[tuple[str, str]] = [
    # chunking — every aidream call site uses these three names
    ("aidream.services.rag.chunking:chunk_text", "matrx_rag.chunking:chunk_text"),
    ("aidream.services.rag.chunking:chunk_code", "matrx_rag.chunking:chunk_code"),
    ("aidream.services.rag.chunking:Chunk", "matrx_rag.chunking:Chunk"),
    # search — fusion + diversification + the public entry point
    ("aidream.services.rag.search:search", "matrx_rag.search:search"),
    ("aidream.services.rag.search:_rrf_fuse", "matrx_rag.search:_rrf_fuse"),
    ("aidream.services.rag.search:_mmr_filter", "matrx_rag.search:_mmr_filter"),
    ("aidream.services.rag.search:_apply_priority", "matrx_rag.search:_apply_priority"),
    ("aidream.services.rag.search:SearchHit", "matrx_rag.search:SearchHit"),
    ("aidream.services.rag.search:SearchResponse", "matrx_rag.search:SearchResponse"),
    # extraction_indexing — payload mapping + helpers
    (
        "aidream.services.rag.extraction_indexing:payload_to_indexable_text",
        "matrx_rag.extraction_indexing:payload_to_indexable_text",
    ),
    # embeddings — facade functions called from ingestion + search
    ("aidream.services.rag.embeddings:embed", "matrx_rag.embeddings:embed"),
    ("aidream.services.rag.embeddings:spec_for", "matrx_rag.embeddings:spec_for"),
    (
        "aidream.services.rag.embeddings:default_text_model",
        "matrx_rag.embeddings:default_text_model",
    ),
    (
        "aidream.services.rag.embeddings:default_code_model",
        "matrx_rag.embeddings:default_code_model",
    ),
    ("aidream.services.rag.embeddings:SPECS", "matrx_rag.embeddings:SPECS"),
    # ingestion — top-level entry + write
    ("aidream.services.rag.ingestion:ingest_source", "matrx_rag.ingestion:ingest_source"),
    ("aidream.services.rag.ingestion:upsert_chunks", "matrx_rag.ingestion:upsert_chunks"),
    # llm — the four LLM-backed functions in the package
    (
        "aidream.services.rag.llm:contextualize_chunk",
        "matrx_rag.llm:contextualize_chunk",
    ),
    ("aidream.services.rag.llm:expand_query", "matrx_rag.llm:expand_query"),
    ("aidream.services.rag.llm:hyde_passage", "matrx_rag.llm:hyde_passage"),
    ("aidream.services.rag.llm:clean_pdf_text", "matrx_rag.llm:clean_pdf_text"),
    # db — the pool accessor
    # sources — the ResolvedSource dataclass used across the package
    ("aidream.services.rag.sources:ResolvedSource", "matrx_rag.sources:ResolvedSource"),
]


def _resolve(path: str):
    """Resolve 'a.b.c:name' to ``a.b.c.name`` via import + getattr."""
    import importlib

    module_path, attr = path.split(":")
    mod = importlib.import_module(module_path)
    return getattr(mod, attr)


@pytest.mark.parametrize("shim_path,pkg_path", _SHIM_CALL_SITE_SYMBOLS)
def test_shim_submodule_resolves_to_package(shim_path, pkg_path):
    """Every shim-submodule attribute aidream's call sites depend on
    must resolve to the EXACT same object on matrx_rag. Identity check
    catches accidental shim drift (renamed function in matrx_rag without
    updating the shim, or vice versa)."""
    shim_obj = _resolve(shim_path)
    pkg_obj = _resolve(pkg_path)
    assert shim_obj is pkg_obj, (
        f"shim {shim_path} ({shim_obj!r}) is not package {pkg_path} ({pkg_obj!r})"
    )


def test_shim_top_level_re_exports_every_public_matrx_rag_name():
    """The top-level aidream.services.rag shim's PEP-562 __getattr__
    must resolve every name in matrx_rag.__all__. This is a weaker check
    than the submodule parametrize above (the top-level shim is a single
    passthrough), but it catches __all__ drift."""
    import matrx_rag

    import aidream.services.rag as shim

    for name in matrx_rag.__all__:
        # Will raise AttributeError if matrx_rag.__all__ lists a name
        # that doesn't actually exist on matrx_rag — that's the failure
        # mode this test detects.
        resolved = getattr(shim, name)
        expected = getattr(matrx_rag, name)
        assert resolved is expected, (
            f"shim.{name} ({resolved!r}) is not matrx_rag.{name} ({expected!r})"
        )


# ---------------------------------------------------------------------------
# _rerank_is_confident — Cohere confidence floor (pure)
# ---------------------------------------------------------------------------


def test_rerank_confident_when_any_score_clears_floor():
    from matrx_rag.search import _rerank_is_confident

    assert _rerank_is_confident({"a": 0.9, "b": 0.05}) is True
    assert _rerank_is_confident({"a": 0.25}) is True  # floor is inclusive


def test_rerank_not_confident_when_all_scores_low():
    """The observed failure mode: every candidate in the window scores ~0.10
    (query matched nothing well) — Cohere's ordering of uniformly-bad
    candidates is noise, so the fused RRF order must win."""
    from matrx_rag.search import _rerank_is_confident

    assert _rerank_is_confident({"a": 0.10, "b": 0.07, "c": 0.05}) is False
    assert _rerank_is_confident({}) is False
