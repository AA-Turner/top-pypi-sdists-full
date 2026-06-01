"""
Configuration for LlamaIndex tracing.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LlamaIndexConfig:
    """Configuration for LlamaIndex tracing behavior.

    Attributes:
        trace_queries: Whether to trace query engine operations
        trace_chat: Whether to trace chat engine operations
        trace_retrieval: Whether to trace retrieval operations
        trace_synthesis: Whether to trace response synthesis
        trace_llm_calls: Whether to trace LLM calls
        trace_embedding: Whether to trace embedding operations
        trace_reranking: Whether to trace reranking operations
        capture_inputs: Whether to capture query/chat inputs
        capture_outputs: Whether to capture response outputs
        capture_nodes: Whether to capture retrieved nodes
        max_content_length: Maximum content length to capture
        max_nodes_captured: Maximum number of nodes to capture
        mask_sensitive_data: Whether to mask potentially sensitive data
        query_timeout: Timeout in seconds for query operations
        retrieval_timeout: Timeout in seconds for retrieval
        llm_timeout: Timeout in seconds for LLM calls
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all transient)
    """

    # Tracing toggles
    trace_queries: bool = True
    trace_chat: bool = True
    trace_retrieval: bool = True
    trace_synthesis: bool = True
    trace_llm_calls: bool = True
    trace_embedding: bool = True
    trace_reranking: bool = True

    # Data capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_nodes: bool = True
    max_content_length: int = 2000
    max_nodes_captured: int = 10

    # Privacy
    mask_sensitive_data: bool = False

    # Span naming
    span_prefix: str = "llamaindex"

    # Timeout settings (in seconds)
    query_timeout: float = 120.0  # 2 minutes for query
    retrieval_timeout: float = 60.0  # 1 minute for retrieval
    llm_timeout: float = 120.0  # 2 minutes for LLM calls

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list[str] = field(default_factory=list)  # Empty = retry all transient

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration."""
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.max_nodes_captured < 1:
            raise ValueError("max_nodes_captured must be at least 1")
        if self.query_timeout <= 0:
            raise ValueError("query_timeout must be positive")
        if self.retrieval_timeout <= 0:
            raise ValueError("retrieval_timeout must be positive")
        if self.llm_timeout <= 0:
            raise ValueError("llm_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
