# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

from .text_content_param import TextContentParam

__all__ = ["VectorStoreQueryParams", "RerankConfig"]


class VectorStoreQueryParams(TypedDict, total=False):
    content: Required[TextContentParam]
    """Text content for documents."""

    filter: Dict[str, object]
    """Metadata filter expression"""

    include_vectors: bool
    """Include embedding vectors in response"""

    query_type: Literal["semantic", "lexical", "hybrid"]
    """Query type: semantic, lexical, or hybrid"""

    rerank: bool
    """[Deprecated: use rerank_config] Enable reranking of search results"""

    rerank_config: RerankConfig
    """Reranking configuration.

    Presence enables reranking; omit to disable. Pass an empty object ({}) to enable
    reranking with system defaults.
    """

    rerank_instruction: str
    """[Deprecated: use rerank_config.instruction] Custom instruction for reranker"""

    rerank_model: str
    """[Deprecated: use rerank_config.model] Reranking model to use"""

    rerank_top_n: int
    """[Deprecated: use rerank_config.top_n] Number of results after reranking"""

    top_k: int
    """Number of search results to return"""


class RerankConfig(TypedDict, total=False):
    """Reranking configuration.

    Presence enables reranking; omit to disable. Pass an empty object ({}) to enable reranking with system defaults.
    """

    instruction: str
    """
    Custom instruction for the reranking model (e.g., 'Given a medical question,
    retrieve relevant clinical passages'). Only applies to instruction-following
    rerankers like Qwen3.
    """

    model: str
    """Reranking model to use (uses system default if not specified).

    Supported values depend on the selected provider: Launch cross-encoder names
    (e.g. 'cross-encoder/ms-marco-MiniLM-L-12-v2'), Vertex semantic-ranker names
    (e.g. 'semantic-ranker-default-004') when provider='vertex', or any model id the
    inference proxy serves when provider='proxy'.
    """

    provider: Literal["launch", "vertex", "proxy"]
    """Reranking provider to use.

    When omitted, the deployment default is used ('launch', or 'proxy' on ray-serve
    deployments configured for the OpenAI-compatible inference proxy). Set
    explicitly (e.g. 'vertex') to route to a specific provider on a deployment that
    has more than one configured. Requesting a provider that is not configured on
    the deployment returns a 400.
    """

    top_n: int
    """Number of results to keep after reranking (defaults to top_k)"""

    type: Literal["base"]
    """Reranking configuration type. Currently only 'base' is supported."""
