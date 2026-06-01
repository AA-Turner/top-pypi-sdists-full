"""
Aigie LlamaIndex Integration

Full workflow tracing for LlamaIndex RAG applications with the Aigie SDK.
Traces query engines, chat engines, retrieval, synthesis, and embeddings.

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.llamaindex import patch_llamaindex

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_llamaindex()

    # Now all LlamaIndex operations are automatically traced
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    response = query_engine.query("What is...")  # Automatically traced!

Usage (Manual Callback Handler):
    from aigie.integrations.llamaindex import LlamaIndexHandler

    # Create handler with trace context
    async with aigie.trace("RAG Query") as trace:
        handler = LlamaIndexHandler(trace_name="Document Search")
        handler.set_trace_context(trace)

        await handler.handle_query_start(
            query_id="q1",
            query_str="What is the meaning?",
            query_type="query"
        )

        # ... run query operations ...

        await handler.handle_query_end(query_id="q1", response=result)

Usage (Configuration):
    from aigie.integrations.llamaindex import LlamaIndexConfig, patch_llamaindex

    # Custom configuration
    config = LlamaIndexConfig(
        trace_queries=True,
        trace_retrieval=True,
        trace_synthesis=True,
        capture_nodes=True,
        max_nodes_captured=20,
    )

    # Apply configuration
    patch_llamaindex()
"""

__all__ = [
    # Handler
    "LlamaIndexHandler",
    # Configuration
    "LlamaIndexConfig",
    # Cost tracking
    "LLAMAINDEX_MODEL_PRICING",
    "LLAMAINDEX_EMBEDDING_PRICING",
    "get_llamaindex_cost",
    "get_embedding_cost",
    "extract_tokens_from_response",
    "aggregate_query_costs",
    # Auto-instrumentation
    "patch_llamaindex",
    "unpatch_llamaindex",
    "is_llamaindex_patched",
    # Utilities
    "is_llamaindex_available",
    "get_llamaindex_version",
    "safe_str",
    "extract_node_info",
    "extract_response_info",
    "extract_index_info",
    "format_retrieval_results",
    "get_retrieval_summary",
    "mask_sensitive_content",
    # Retry/Timeout utilities
    "RetryExhaustedError",
    "TimeoutExceededError",
    "QueryError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
    "QueryRetryContext",
]

from typing import TYPE_CHECKING, Any


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "LlamaIndexHandler":
        from .handler import LlamaIndexHandler

        return LlamaIndexHandler

    # Configuration
    if name == "LlamaIndexConfig":
        from .config import LlamaIndexConfig

        return LlamaIndexConfig

    # Cost tracking
    if name == "LLAMAINDEX_MODEL_PRICING":
        from .cost_tracking import LLAMAINDEX_MODEL_PRICING

        return LLAMAINDEX_MODEL_PRICING

    if name == "LLAMAINDEX_EMBEDDING_PRICING":
        from .cost_tracking import LLAMAINDEX_EMBEDDING_PRICING

        return LLAMAINDEX_EMBEDDING_PRICING

    if name == "get_llamaindex_cost":
        from .cost_tracking import get_llamaindex_cost

        return get_llamaindex_cost

    if name == "get_embedding_cost":
        from .cost_tracking import get_embedding_cost

        return get_embedding_cost

    if name == "extract_tokens_from_response":
        from .cost_tracking import extract_tokens_from_response

        return extract_tokens_from_response

    if name == "aggregate_query_costs":
        from .cost_tracking import aggregate_query_costs

        return aggregate_query_costs

    # Auto-instrumentation
    if name == "patch_llamaindex":
        from .auto_instrument import patch_llamaindex

        return patch_llamaindex

    if name == "unpatch_llamaindex":
        from .auto_instrument import unpatch_llamaindex

        return unpatch_llamaindex

    if name == "is_llamaindex_patched":
        from .auto_instrument import is_llamaindex_patched

        return is_llamaindex_patched

    # Utilities
    if name == "is_llamaindex_available":
        from .utils import is_llamaindex_available

        return is_llamaindex_available

    if name == "get_llamaindex_version":
        from .utils import get_llamaindex_version

        return get_llamaindex_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "extract_node_info":
        from .utils import extract_node_info

        return extract_node_info

    if name == "extract_response_info":
        from .utils import extract_response_info

        return extract_response_info

    if name == "extract_index_info":
        from .utils import extract_index_info

        return extract_index_info

    if name == "format_retrieval_results":
        from .utils import format_retrieval_results

        return format_retrieval_results

    if name == "get_retrieval_summary":
        from .utils import get_retrieval_summary

        return get_retrieval_summary

    if name == "mask_sensitive_content":
        from .utils import mask_sensitive_content

        return mask_sensitive_content

    # Retry/Timeout utilities
    if name == "RetryExhaustedError":
        from ..._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError

    if name == "TimeoutExceededError":
        from ..._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError

    if name == "QueryError":
        from ..._legacy_stubs import QueryError

        return QueryError

    if name == "with_timeout":
        from ..._legacy_stubs import with_timeout

        return with_timeout

    if name == "with_retry":
        from ..._legacy_stubs import with_retry

        return with_retry

    if name == "with_timeout_and_retry":
        from ..._legacy_stubs import with_timeout_and_retry

        return with_timeout_and_retry

    if name == "retry_decorator":
        from ..._legacy_stubs import retry_decorator

        return retry_decorator

    if name == "RetryContext":
        from ..._legacy_stubs import RetryContext

        return RetryContext

    if name == "QueryRetryContext":
        from ..._legacy_stubs import QueryRetryContext

        return QueryRetryContext

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_llamaindex_patched,
        patch_llamaindex,
        unpatch_llamaindex,
    )
    from .config import LlamaIndexConfig
    from .cost_tracking import (
        LLAMAINDEX_EMBEDDING_PRICING,
        LLAMAINDEX_MODEL_PRICING,
        aggregate_query_costs,
        extract_tokens_from_response,
        get_embedding_cost,
        get_llamaindex_cost,
    )
    from .handler import LlamaIndexHandler
    from ..._legacy_stubs import (
        QueryError,
        QueryRetryContext,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .utils import (
        extract_index_info,
        extract_node_info,
        extract_response_info,
        format_retrieval_results,
        get_llamaindex_version,
        get_retrieval_summary,
        is_llamaindex_available,
        mask_sensitive_content,
        safe_str,
    )
