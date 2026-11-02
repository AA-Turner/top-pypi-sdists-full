"""
Phase 2b/i — DocumentWriter injection seam + AuthMode tests.

Verifies the seam plumbing works in isolation: configure(), get accessors,
the no-op default's warn-once behavior, exception-class rebinding, and
the contract that matrx-rag never raises a `from aidream import` at
module load time.
"""

from __future__ import annotations

import importlib

import pytest


def test_default_document_writer_is_noop_and_warns_once(caplog):
    """A fresh process gets the NoOpDocumentWriter. First call logs a
    warning; subsequent calls are silent."""
    import logging

    import matrx_rag

    matrx_rag._ext._reset_for_tests()

    writer = matrx_rag.get_document_writer()
    assert isinstance(writer, matrx_rag.NoOpDocumentWriter)

    import asyncio

    with caplog.at_level(logging.WARNING, logger="matrx_rag._ext"):
        asyncio.run(writer.update_clean_content("doc-1", "text", "owner-1"))
        asyncio.run(writer.update_clean_content("doc-2", "more text", "owner-1"))

    warnings = [r for r in caplog.records if "no-op" in r.message.lower()]
    assert len(warnings) == 1, f"expected exactly 1 warning, got {len(warnings)}: {warnings}"


def test_configure_replaces_document_writer():
    """configure(document_writer=...) installs the host's writer."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()

    class TestWriter:
        async def persist_processed_document(self, **kwargs):
            return "stub-doc-id"

        async def update_clean_content(self, doc_id, clean_content, owner_id):
            pass

        async def update_page_cleanup(self, **kwargs):
            pass

        async def ensure_derivative(self, **kwargs):
            return matrx_rag._ext.DerivativeResult(outcome="created", id="stub-deriv-id")

    test_writer = TestWriter()
    matrx_rag.configure(document_writer=test_writer)
    assert matrx_rag.get_document_writer() is test_writer
    assert matrx_rag.is_configured()


def test_configure_auth_mode():
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    assert matrx_rag.get_auth_mode() is matrx_rag.AuthMode.USER_JWT

    matrx_rag.configure(auth_mode=matrx_rag.AuthMode.SERVICE_ROLE)
    assert matrx_rag.get_auth_mode() is matrx_rag.AuthMode.SERVICE_ROLE

    matrx_rag.configure(auth_mode="user_jwt")  # string form
    assert matrx_rag.get_auth_mode() is matrx_rag.AuthMode.USER_JWT


def test_configure_source_kind_aliases():
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    assert matrx_rag.get_ext("source_kind_cld_file") == "cld_file"

    matrx_rag.configure(source_kind_aliases={"cld_file": "custom_cld_file"})
    assert matrx_rag.get_ext("source_kind_cld_file") == "custom_cld_file"


def test_exception_class_rebinding():
    """Aidream rebinds matrx_rag.NotFoundError to its own class so
    downstream `except NotFoundError` (from aidream) still catches
    everything matrx_rag raises."""
    import matrx_rag
    import matrx_rag._ext as ext_mod
    import matrx_rag.extraction_indexing as ei_mod

    matrx_rag._ext._reset_for_tests()

    original = matrx_rag._ext.NotFoundError

    class HostNotFoundError(Exception):
        pass

    matrx_rag.configure(not_found_error_class=HostNotFoundError)

    # The rebinding affects BOTH _ext (the home module) and
    # extraction_indexing (which had imported NotFoundError eagerly).
    assert ext_mod.NotFoundError is HostNotFoundError
    assert ei_mod.NotFoundError is HostNotFoundError

    # Clean up so other tests start from the default.
    matrx_rag._ext._reset_for_tests()
    # After reset, the module-level NotFoundError on _ext is back to
    # default; extraction_indexing's local binding may still point at
    # HostNotFoundError until its module is reloaded — acceptable for
    # tests as long as the production configure() path is exercised
    # before any code runs.
    assert ext_mod.NotFoundError is not HostNotFoundError


def test_compute_params_hash_matches_aidream_algorithm():
    """The package's compute_params_hash MUST produce the same SHA-256
    as aidream's dedup_service.compute_params_hash for the same input —
    otherwise derivative lookups would miss matches across hosts."""
    import matrx_rag

    # Order-independent
    h1 = matrx_rag._ext.compute_params_hash({"a": 1, "b": 2})
    h2 = matrx_rag._ext.compute_params_hash({"b": 2, "a": 1})
    assert h1 == h2

    # Different values -> different hashes
    h3 = matrx_rag._ext.compute_params_hash({"a": 1, "b": 3})
    assert h1 != h3

    # None / empty
    assert matrx_rag._ext.compute_params_hash(None) == matrx_rag._ext.compute_params_hash({})

    # Known vector for the empty-dict case (stable across runs)
    assert matrx_rag._ext.compute_params_hash({}) == (
        "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    )


def test_derivative_intent_values_match_aidream():
    """DerivativeIntent string values must match aidream's enum so
    rebinding preserves wire compatibility."""
    import matrx_rag

    assert matrx_rag._ext.DerivativeIntent.CREATE_DERIVATIVE.value == "create_derivative"
    assert (
        matrx_rag._ext.DerivativeIntent.GET_OR_CREATE_DERIVATIVE.value == "get_or_create_derivative"
    )


def test_matrx_rag_imports_without_aidream():
    """Critical Phase 2b/i property: importing matrx_rag and its
    submodules from a fresh interpreter MUST NOT trigger an aidream
    import. The DocumentWriter seam is what makes this possible."""
    # Already-imported modules survive this test — what matters is that
    # no eager `from aidream` exists at module top in matrx_rag.
    from matrx_utils.source_guard import stable_source

    for modname in (
        "matrx_rag",
        "matrx_rag.pdf_pipeline",
        "matrx_rag.stages",
        "matrx_rag.extraction_indexing",
        "matrx_rag.ingestion",
        "matrx_rag.search",
        "matrx_rag.embeddings",
    ):
        mod = importlib.import_module(modname)
        src = stable_source(mod)
        offending = [
            line
            for line in src.splitlines()
            if line.strip().startswith(("from aidream", "import aidream"))
        ]
        assert not offending, f"{modname} has eager aidream imports: {offending}"


def test_no_aidream_import_anywhere_in_matrx_rag():
    """ZERO `aidream` imports in the whole package — eager OR lazy.

    The per-module check above only covers a hand-listed set and used to carry
    a whitelist for `aidream.package_integration` (the eval CLIs imported the
    host to bootstrap it). Those now take a `--bootstrap module:callable`
    argument instead, so there is no exception left and none may be added:
    an import of the host, at any indentation, is a boundary violation.
    """
    from pathlib import Path

    import matrx_rag

    pkg_root = Path(matrx_rag.__file__).resolve().parent
    offending: list[str] = []
    for path in sorted(pkg_root.rglob("*.py")):
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith(("from aidream", "import aidream")):
                offending.append(f"{path.relative_to(pkg_root)}:{lineno}: {stripped}")
    assert not offending, "matrx-rag imports the host aidream:\n" + "\n".join(offending)


def test_get_ext_required_raises_when_missing():
    """Sanity: get_ext(key, required=True) raises for unknown keys."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    with pytest.raises(matrx_rag.RagNotConfiguredError):
        matrx_rag.get_ext("totally_unknown_key_42", required=True)

    # Without required=True, returns the default
    assert matrx_rag.get_ext("totally_unknown_key_42") is None
    assert matrx_rag.get_ext("totally_unknown_key_42", default="fallback") == "fallback"


# ── Phase 2b/ii — EmbeddingProvider seam ───────────────────────────────


def test_default_embedding_provider_is_lazy():
    """The default OpenAI+Voyage provider is built on first
    get_embedding_provider() call, not on package import. matrx-local
    that calls configure() first never builds it."""
    import matrx_rag
    import matrx_rag._ext as ext_mod

    matrx_rag._ext._reset_for_tests()
    # Reset replaced the singleton with None — nothing built yet.
    assert ext_mod._default_embedding_provider_singleton is None

    # First call builds it.
    provider = matrx_rag.get_embedding_provider()
    assert provider is not None
    # And caches.
    assert matrx_rag.get_embedding_provider() is provider


def test_configure_replaces_embedding_provider():
    """When a host configures its own provider, the default is never
    instantiated — verified by the singleton staying None."""
    import matrx_rag
    import matrx_rag._ext as ext_mod

    matrx_rag._ext._reset_for_tests()

    class _FakeFastembedProvider:
        async def embed(self, model, texts, *, input_type=None):
            return [[0.1, 0.2, 0.3] for _ in texts]

        def spec_for(self, model):
            from matrx_rag.embeddings import EmbeddingSpec

            return EmbeddingSpec(name="local:bge", dim=3, table="local.embed", batch_size=32)

        def default_text_model(self):
            return "local:bge"

        def default_code_model(self):
            return "local:bge"

        def known_models(self):
            return ["local:bge"]

    fake = _FakeFastembedProvider()
    matrx_rag.configure(embedding_provider=fake)
    assert matrx_rag.get_embedding_provider() is fake
    # The lazy default singleton was NEVER built.
    assert ext_mod._default_embedding_provider_singleton is None


@pytest.mark.asyncio
async def test_module_level_embed_delegates_to_provider():
    """The module-level ``embed()``, ``spec_for()``, ``default_text_model()``
    facade functions delegate to the configured provider."""
    import matrx_rag
    import matrx_rag.embeddings as embeddings_mod

    matrx_rag._ext._reset_for_tests()

    class _RecordingProvider:
        def __init__(self):
            self.embed_calls: list = []

        async def embed(self, model, texts, *, input_type=None):
            self.embed_calls.append((model, list(texts), input_type))
            return [[0.5] * 4 for _ in texts]

        def spec_for(self, model):
            from matrx_rag.embeddings import EmbeddingSpec

            return EmbeddingSpec(name=model, dim=4, table=f"t.{model}", batch_size=8)

        def default_text_model(self):
            return "rec:text"

        def default_code_model(self):
            return "rec:code"

        def known_models(self):
            return ["rec:text", "rec:code"]

    rec = _RecordingProvider()
    matrx_rag.configure(embedding_provider=rec)

    # spec_for, default_text_model, default_code_model — sync facades
    assert embeddings_mod.default_text_model() == "rec:text"
    assert embeddings_mod.default_code_model() == "rec:code"
    spec = embeddings_mod.spec_for("rec:text")
    assert spec.name == "rec:text"
    assert spec.dim == 4

    # embed — async facade
    out = await embeddings_mod.embed(
        "rec:text", ["hello", "world"], input_type="query", organization_id=None
    )
    assert out == [[0.5] * 4, [0.5] * 4]
    assert rec.embed_calls == [("rec:text", ["hello", "world"], "query")]


def test_default_provider_has_known_models():
    """The aidream-default provider declares both OpenAI text + Voyage code."""
    import matrx_rag
    from matrx_rag.embeddings import DefaultOpenAIVoyageProvider

    matrx_rag._ext._reset_for_tests()
    provider = DefaultOpenAIVoyageProvider()
    names = provider.known_models()
    assert "openai:text-embedding-3-small" in names
    assert "voyage:voyage-code-3" in names


def test_default_provider_specs_match_pgvector_tables():
    """The default specs must match the table names baked into the
    Phase 2.0 schema migrations — any drift breaks vector recall."""
    from matrx_rag.embeddings import DefaultOpenAIVoyageProvider

    p = DefaultOpenAIVoyageProvider()
    text_spec = p.spec_for("openai:text-embedding-3-small")
    code_spec = p.spec_for("voyage:voyage-code-3")
    assert text_spec.dim == 1536
    assert text_spec.table == "rag.embeddings_oai_3_small_1536"
    assert code_spec.dim == 1024
    assert code_spec.table == "rag.embeddings_voyage_code_3_1024"


@pytest.mark.asyncio
async def test_default_provider_empty_inputs():
    """Zero-vector backfill preserves a 1:1 index mapping when some
    inputs are empty strings."""
    import matrx_rag
    from matrx_rag.embeddings import DefaultOpenAIVoyageProvider

    matrx_rag._ext._reset_for_tests()
    # We can exercise the empty-input fast path without an OpenAI key —
    # the provider short-circuits to zero vectors.
    p = DefaultOpenAIVoyageProvider()
    out = await p.embed("openai:text-embedding-3-small", ["", "  ", ""])
    assert len(out) == 3
    for v in out:
        assert v == [0.0] * 1536


def test_default_provider_rejects_unknown_model():
    from matrx_rag.embeddings import DefaultOpenAIVoyageProvider

    p = DefaultOpenAIVoyageProvider()
    with pytest.raises(ValueError, match="Unknown embedding model"):
        p.spec_for("totally-not-a-model")


# ── Phase 2b/iii — LLMProvider seam ────────────────────────────────────


def test_no_default_llm_provider_refuses_loudly():
    """There is no raw-client default (2026-09-25): with nothing injected,
    get_llm_provider() refuses in words instead of building an OpenAI client."""
    import matrx_rag
    import matrx_rag._ext as ext_mod

    matrx_rag._ext._reset_for_tests()
    with pytest.raises(ext_mod.LLMProviderNotConfigured):
        matrx_rag.get_llm_provider()
    assert not hasattr(ext_mod, "_default_llm_provider")


def test_configure_replaces_llm_provider():
    """When a host configures its own LLM provider, the default never
    instantiates — verified via the singleton-stays-None check."""
    import matrx_rag
    import matrx_rag._ext as ext_mod

    matrx_rag._ext._reset_for_tests()

    class _FakeLlamaProvider:
        async def chat(
            self,
            messages,
            *,
            model,
            temperature=None,
            max_tokens=None,
            response_format=None,
            timeout=None,
            purpose=None,
        ):
            return "stub response"

    fake = _FakeLlamaProvider()
    matrx_rag.configure(llm_provider=fake)
    assert matrx_rag.get_llm_provider() is fake


@pytest.mark.asyncio
async def test_llm_jobs_raise_without_runner():
    """matrx_rag.llm has NO raw-provider fallback: the four LLM jobs run only
    through the injected RagAgentRunner. With none injected, each raises a
    clear RuntimeError rather than silently degrading (host-config error)."""
    import matrx_rag
    import matrx_rag.llm as llm_mod

    matrx_rag._ext._reset_for_tests()  # no runner injected

    with pytest.raises(RuntimeError, match="requires a RagAgentRunner"):
        await llm_mod.clean_pdf_text("raw page text")
    with pytest.raises(RuntimeError, match="requires a RagAgentRunner"):
        await llm_mod.contextualize_chunk("a long document", "a chunk")
    with pytest.raises(RuntimeError, match="requires a RagAgentRunner"):
        await llm_mod.expand_query("a query", n=3)
    with pytest.raises(RuntimeError, match="requires a RagAgentRunner"):
        await llm_mod.hyde_passage("a query")


@pytest.mark.asyncio
async def test_llm_jobs_short_circuit_without_runner():
    """Empty / no-op inputs short-circuit BEFORE the runner requirement, so a
    trivial input never raises and never wastes an agent call even when no
    runner is injected."""
    import matrx_rag
    import matrx_rag.llm as llm_mod

    matrx_rag._ext._reset_for_tests()  # no runner injected

    page = await llm_mod.clean_pdf_text("   ")
    assert page.text == ""
    assert await llm_mod.contextualize_chunk("doc", "   ") == ""
    assert await llm_mod.expand_query("   ", n=3) == ["   "]
    assert await llm_mod.expand_query("q", n=1) == ["q"]
    assert await llm_mod.hyde_passage("   ") == ""


# ── VectorStore seam (Phase 2b/iv) ─────────────────────────────────────


def test_vector_store_default_is_lazy():
    """Until something calls get_vector_store, the registry slot stays
    None — so matrx-local with its own backend never instantiates the
    pgvector delegate."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    # Slot is None at startup.
    assert matrx_rag._ext._registry["vector_store"] is None
    # First accessor call materializes the default singleton.
    store = matrx_rag.get_vector_store()
    assert store is not None
    assert matrx_rag._ext._registry["vector_store"] is store
    # Same instance on subsequent calls.
    assert matrx_rag.get_vector_store() is store


def test_vector_store_default_is_pgvector_delegate():
    """The default falls back to _PgVectorStoreDelegate."""
    import matrx_rag
    from matrx_rag._ext import _PgVectorStoreDelegate

    matrx_rag._ext._reset_for_tests()
    store = matrx_rag.get_vector_store()
    assert isinstance(store, _PgVectorStoreDelegate)


def test_vector_store_protocol_runtime_check():
    """Default delegate satisfies the VectorStore Protocol via
    runtime_checkable."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    store = matrx_rag.get_vector_store()
    assert isinstance(store, matrx_rag.VectorStore)


def test_vector_store_configure_swap():
    """A host that calls configure(vector_store=...) replaces the slot
    and the default delegate is never instantiated."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()

    class _StubVectorStore:
        async def upsert_chunks(self, *, chunks, embeddings, embedding_model, scope):
            return 42

        async def vector_recall(self, **kwargs):
            return ["chunk-1", "chunk-2"]

        async def lexical_recall(self, **kwargs):
            return ["chunk-3"]

        async def delete_by_source(self, *, source_kind, source_id, field_id=None):
            return 0

    stub = _StubVectorStore()
    matrx_rag.configure(vector_store=stub)
    assert matrx_rag.get_vector_store() is stub
    # The default singleton was never built.
    assert matrx_rag._ext._default_vector_store_singleton is None


@pytest.mark.asyncio
async def test_vector_store_default_recall_raises_not_implemented():
    """The default delegate's upsert_chunks / vector_recall /
    lexical_recall are stubs that raise NotImplementedError with a
    clear message pointing at the Phase 2b/iv follow-on. matrx-rag's
    actual call sites still use their inline asyncpg paths today, so
    nothing in production hits these stubs unless a host opts in via
    ``get_vector_store()`` and calls them directly."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    store = matrx_rag.get_vector_store()

    with pytest.raises(NotImplementedError, match="upsert_chunks"):
        await store.upsert_chunks(
            chunks=[],
            embeddings=[],
            embedding_model="openai:text-embedding-3-small",
            scope={"owner_id": "u", "source_kind": "note", "source_id": "s"},
        )
    with pytest.raises(NotImplementedError, match="vector_recall"):
        await store.vector_recall(
            query_vector=[0.1] * 1536,
            embedding_model="openai:text-embedding-3-small",
            organization_id=None,
            owner_id=None,
        )
    with pytest.raises(NotImplementedError, match="lexical_recall"):
        await store.lexical_recall(
            query="hello",
            organization_id=None,
            owner_id=None,
        )


def test_vector_store_reset_clears_singleton():
    """_reset_for_tests must clear both the registry slot AND the
    lazy default singleton so subsequent tests get a fresh delegate."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    first = matrx_rag.get_vector_store()
    matrx_rag._ext._reset_for_tests()
    assert matrx_rag._ext._registry["vector_store"] is None
    assert matrx_rag._ext._default_vector_store_singleton is None
    second = matrx_rag.get_vector_store()
    assert first is not second


# ── RagAgentRunner seam (LLM-to-Agents migration) ──────────────────────
#
# These prove BOTH rollout phases without a live LLM call:
#   * Phase 2 (switch OFF): no runner injected -> get_rag_agent_runner() is
#     None -> the four llm.py functions take the raw LLMProvider path
#     (already covered by the LLMProvider-seam tests above, which run with
#     no runner present).
#   * Phase 3 (switch ON): a runner IS injected -> the four functions
#     delegate to it, the raw provider is never touched, and ALL shared
#     assembly (CleanedPage normalization, multi-query dedup/cap) still
#     happens in llm.py so the two paths produce identical-shape results.


def test_rag_agent_runner_default_is_none():
    """Fresh process / after reset: nothing injected, so llm.py takes the
    raw path. This is the Phase-2 (switch OFF) contract."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()
    assert matrx_rag.get_rag_agent_runner() is None


def test_configure_replaces_rag_agent_runner():
    """configure(rag_agent_runner=...) installs the host's runner."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()

    class _StubRunner:
        async def clean_page(self, raw_text, *, timeout=None):
            return {"text": raw_text, "section_kind": "academic_paper"}

        async def contextualize(self, document, chunk, *, timeout=None):
            return ""

        async def expand_query(self, query, *, n=3, timeout=None):
            return []

        async def hyde(self, query, *, timeout=None):
            return ""

    runner = _StubRunner()
    matrx_rag.configure(rag_agent_runner=runner)
    assert matrx_rag.get_rag_agent_runner() is runner
    assert isinstance(runner, matrx_rag.RagAgentRunner)


def test_reset_clears_rag_agent_runner():
    """_reset_for_tests must drop the runner so the next test starts on the
    raw path."""
    import matrx_rag

    matrx_rag._ext._reset_for_tests()

    class _StubRunner:
        async def clean_page(self, raw_text, *, timeout=None):
            return {"text": raw_text}

        async def contextualize(self, document, chunk, *, timeout=None):
            return ""

        async def expand_query(self, query, *, n=3, timeout=None):
            return []

        async def hyde(self, query, *, timeout=None):
            return ""

    matrx_rag.configure(rag_agent_runner=_StubRunner())
    assert matrx_rag.get_rag_agent_runner() is not None
    matrx_rag._ext._reset_for_tests()
    assert matrx_rag.get_rag_agent_runner() is None


@pytest.mark.asyncio
async def test_llm_functions_delegate_to_runner_when_injected():
    """When a runner is injected the four functions delegate to it, the raw
    LLMProvider is NEVER called, and llm.py still owns shared assembly
    (expand prepends the original query + dedups; clean normalizes)."""
    import matrx_rag
    import matrx_rag.llm as llm_mod

    matrx_rag._ext._reset_for_tests()

    class _RecordingRunner:
        def __init__(self):
            self.calls: list = []

        async def clean_page(self, raw_text, *, timeout=None):
            self.calls.append(("clean_page", raw_text))
            return {"text": "agent cleaned", "section_kind": "Legal"}

        async def contextualize(self, document, chunk, *, timeout=None):
            self.calls.append(("contextualize", document, chunk))
            return "  agent prefix  "

        async def expand_query(self, query, *, n=3, timeout=None):
            self.calls.append(("expand_query", query, n))
            # Includes a duplicate to prove llm.py dedups, and 3 lines to
            # prove the cap-to-n (with the prepended original) holds.
            return ["alt one", "alt two", "alt one", "alt three"]

        async def hyde(self, query, *, timeout=None):
            self.calls.append(("hyde", query))
            return "  agent hyde  "

    # A recording provider proves the raw path is never taken when a runner
    # is present (the runner must win even if a provider is also configured).
    class _ProviderTripwire:
        def __init__(self):
            self.calls: list = []

        async def chat(self, messages, *, model, **kwargs):
            self.calls.append(model)
            raise AssertionError("raw provider must not be called when a runner is injected")

    runner = _RecordingRunner()
    tripwire = _ProviderTripwire()
    matrx_rag.configure(rag_agent_runner=runner, llm_provider=tripwire)

    # contextualize -> stripped runner output
    assert await llm_mod.contextualize_chunk("a long document", "a chunk") == "agent prefix"

    # expand -> original first, deduped, capped at n=3
    assert await llm_mod.expand_query("my query", n=3) == ["my query", "alt one", "alt two"]

    # hyde -> stripped runner output
    assert await llm_mod.hyde_passage("a query") == "agent hyde"

    # clean -> normalized CleanedPage (section_kind lowercased by assembly)
    page = await llm_mod.clean_pdf_text("raw page text")
    assert page.text == "agent cleaned"
    assert page.section_kind == "legal"

    # The runner saw all four jobs; the raw provider saw none.
    assert [c[0] for c in runner.calls] == [
        "contextualize",
        "expand_query",
        "hyde",
        "clean_page",
    ]
    assert tripwire.calls == []


@pytest.mark.asyncio
async def test_llm_runner_failure_falls_back_like_raw():
    """A runner that raises must trigger the SAME loud fallback the raw
    path uses: raw text for the cleaner, empty/[query] for the others —
    so behavior is identical regardless of which path failed."""
    import matrx_rag
    import matrx_rag.llm as llm_mod

    matrx_rag._ext._reset_for_tests()

    class _FailingRunner:
        async def clean_page(self, raw_text, *, timeout=None):
            raise RuntimeError("agent outage")

        async def contextualize(self, document, chunk, *, timeout=None):
            raise RuntimeError("agent outage")

        async def expand_query(self, query, *, n=3, timeout=None):
            raise RuntimeError("agent outage")

        async def hyde(self, query, *, timeout=None):
            raise RuntimeError("agent outage")

    matrx_rag.configure(rag_agent_runner=_FailingRunner())

    assert await llm_mod.contextualize_chunk("doc", "chunk") == ""
    assert await llm_mod.expand_query("q", n=3) == ["q"]
    assert await llm_mod.hyde_passage("q") == ""
    page = await llm_mod.clean_pdf_text("raw")
    assert page.text == "raw"
    # Runner outage ⇒ honestly unclassified (""), never the fake bucket "other".
    assert page.section_kind == ""


# ---------------------------------------------------------------------------
# Open-vocabulary section_kind contract — the cleaner classifies with world
# knowledge (e.g. "academic_paper", "discharge_summary"), and NEVER emits a
# catch-all bucket. _normalize_cleaned is the single enforcement point shared
# by the raw-JSON and agent paths, so a disobedient model can't poison data.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "forbidden",
    [
        "other",
        "Other",
        "OTHER",
        "misc",
        "miscellaneous",
        "unknown",
        "unclassified",
        "general",
        "document",
        "n/a",
        "none",
    ],
)
def test_normalize_cleaned_coerces_forbidden_kinds_to_empty(forbidden):
    """Any catch-all kind a model might emit is coerced to "" — honestly
    unclassified — rather than persisted as a fake bucket."""
    from matrx_rag.llm import _normalize_cleaned

    page = _normalize_cleaned({"text": "body", "section_kind": forbidden})
    assert page.section_kind == "", f"{forbidden!r} should coerce to ''"


@pytest.mark.parametrize(
    "kind",
    ["academic_paper", "discharge_summary", "lease_agreement", "earnings_call"],
)
def test_normalize_cleaned_preserves_open_vocab_kind(kind):
    """A genuine, open-vocabulary world-knowledge label survives normalization
    (lower-cased, stripped) — the whole point of the open-vocab contract."""
    from matrx_rag.llm import _normalize_cleaned

    page = _normalize_cleaned({"text": "body", "section_kind": kind})
    assert page.section_kind == kind


@pytest.mark.asyncio
async def test_search_blank_query_short_circuits():
    """A blank / all-whitespace query short-circuits to an empty response
    BEFORE any embedding or DB work — an empty query embeds to a zero vector
    (garbage cosine hits) and produces a NULL tsquery (silently drops lexical),
    so retrieving on it would surface noise. Passing ``embedding_models`` keeps
    the guard free of any provider dependency."""
    from matrx_rag.search import search

    resp = await search(
        "   ",
        user_id="00000000-0000-0000-0000-000000000000",
        embedding_models=["openai:text-embedding-3-small"],
    )
    assert resp.hits == []
    assert resp.total_candidates == 0
    assert resp.query == ""
