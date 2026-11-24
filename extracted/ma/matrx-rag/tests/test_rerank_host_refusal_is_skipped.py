"""A host reranker that REFUSES on policy (a caller refusal — e.g. a compliance mode with no
agreement with the reranker's vendor) is not a provider failure: the search keeps the fused
order, reports ``rerank_status="skipped"`` with the host's sentence, and files no incident."""

from __future__ import annotations

from matrx_rag import search
from matrx_utils.source_guard import stable_source


def test_caller_refusal_is_skipped_not_failed():
    src = stable_source(search)
    refusal = src.index('getattr(exc, "is_caller_refusal", False)')
    skipped = src.index('rerank_status = "skipped"', refusal)
    failed = src.index('rerank_status = "failed"', refusal)
    incident = src.index('kind="rag_rerank_provider_failed"', refusal)
    # The refusal branch decides first; the incident is filed only on the failure branch.
    assert refusal < skipped < failed < incident


def test_skipped_is_a_documented_status():
    src = stable_source(search.SearchResponse)
    assert '"skipped"' in src
