"""Structural guard — no ingest entry point may hardcode an embedding model.

Why this test exists (2026-07-07 orphan-chunk incident)
-------------------------------------------------------
The 2026-07 upgrade flipped ``default_text_model()`` from
``openai:text-embedding-3-small`` (1536d, table ``rag.embeddings_oai_3_small_1536``)
to ``voyage:voyage-4-large`` (1024d, table ``rag.embeddings_voyage_4_large_1024``),
and the live SEARCH lane switched to the voyage table. But the PDF ingest path
still carried a *hardcoded* ``embedding_model="openai:text-embedding-3-small"``
default on ``ingest_pdf`` (and ``run_embed`` / ``run_all``). Both callers
(``ingestion._maybe_dispatch_pdf``, ``library.ingest_library_pdf``) relied on
that default, so every cld_file PDF ingested post-deploy wrote its vectors to
the DEAD oai table — 322 chunks silently invisible to the voyage search lane.

The fix, and the invariant this test locks in:

* Every ingest entry point defaults ``embedding_model`` to ``None`` and
  resolves it at call time via ``default_text_model()``. A literal default is
  a latent split-brain waiting for the next model swap.
* ``default_text_model()`` must NOT be the retired oai model — if someone flips
  the default back to a legacy prose model, this fails loudly.

Pure introspection — no DB, no network, no provider calls.
"""

from __future__ import annotations

import inspect

from matrx_rag.embeddings import (
    SPECS,
    default_text_model,
    orm_model_name_for_table,
    spec_for,
)


def test_default_text_model_is_not_the_retired_oai_model():
    """The prose default must be the live corpus model, never the retired oai
    one (its table is slated for drop; new writes there are invisible to search)."""
    model = default_text_model()
    assert model != "openai:text-embedding-3-small", (
        "default_text_model() is the RETIRED oai model — new prose embeddings "
        "would write to the dead rag.embeddings_oai_3_small_1536 table and be "
        "invisible to the voyage search lane. See the 2026-07-07 orphan-chunk "
        "incident."
    )
    # It must be a fully-qualified '<provider>:<model>' identifier.
    assert ":" in model, f"default_text_model() must be provider-qualified, got {model!r}"


def test_no_ingest_entry_point_hardcodes_embedding_model():
    """Every ingest entry point must default ``embedding_model`` to None (defer
    to ``default_text_model()``), never a literal. A hardcoded literal is the
    exact shape of the orphan-chunk bug."""
    from matrx_rag.pdf_pipeline import ingest_pdf
    from matrx_rag.stages import run_all, run_embed

    for fn in (ingest_pdf, run_embed, run_all):
        sig = inspect.signature(fn)
        default = sig.parameters["embedding_model"].default
        assert default is None, (
            f"{fn.__module__}.{fn.__name__} defaults embedding_model to "
            f"{default!r} — it MUST default to None and resolve via "
            f"default_text_model() at call time. A literal default silently "
            f"routes new embeddings to whatever model was hardcoded (the "
            f"orphan-chunk bug class)."
        )


def test_embedding_table_to_orm_model_has_one_source():
    """The table → ORM model mapping lives ONLY on ``EmbeddingSpec.orm_model``.

    ``stages.py`` and ``ingestion.py`` each used to keep their own hand-written
    dict, and drift between them broke ``run_embed`` while ingest self-heal
    still worked (the 2026-07-08 content-processing embed failure). A second
    registry re-opens that failure class — one source, resolved by
    ``orm_model_name_for_table``, makes the drift impossible."""
    import matrx_rag.ingestion as ingestion_mod
    import matrx_rag.search as search_mod
    import matrx_rag.stages as stages_mod

    for mod in (stages_mod, ingestion_mod, search_mod):
        offenders = [
            name
            for name, value in vars(mod).items()
            if isinstance(value, dict)
            and value
            and all(isinstance(k, str) and k.startswith("rag.embeddings_") for k in value)
        ]
        assert not offenders, (
            f"{mod.__name__} re-introduced a local embedding table → model registry "
            f"({offenders}). Declare orm_model on the EmbeddingSpec instead."
        )


def test_default_text_model_table_resolves_to_an_orm_model():
    """The live prose default must resolve to a packaged ORM model — otherwise
    ``run_embed()`` raises before any provider call."""
    import matrx_rag._ext as ext_mod

    ext_mod._reset_for_tests()  # ordering-independent: use the packaged provider
    table = spec_for(default_text_model()).table
    assert orm_model_name_for_table(table) is not None, (
        f"default prose table {table!r} has no orm_model on its EmbeddingSpec"
    )


def test_all_packaged_embedding_specs_declare_an_orm_model():
    """Every table in ``SPECS`` must carry its ORM model name — a new embedding
    table requires models_rag.py plus ``orm_model`` on its spec."""
    import matrx_rag._ext as ext_mod

    ext_mod._reset_for_tests()  # ordering-independent: use the packaged provider
    for spec in SPECS.values():
        assert spec.orm_model, f"{spec.name} table {spec.table!r} declares no orm_model"
        assert orm_model_name_for_table(spec.table) == spec.orm_model, (
            f"{spec.name} table {spec.table!r} does not resolve back to {spec.orm_model!r}"
        )


def test_image_ingest_also_defers_the_model():
    """image_pipeline.ingest_image was already correct (None → default) and is
    the reference pattern; guard it so a future edit can't regress it either."""
    from matrx_rag.image_pipeline import ingest_image

    default = inspect.signature(ingest_image).parameters["embedding_model"].default
    assert default is None, f"ingest_image defaults embedding_model to {default!r}; must be None."
