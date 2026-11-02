"""LLM provider abstraction for the LangGraph orchestration engine.

Public API for the LLM provider package. Provides configurable provider
instantiation, structured output, streaming, deterministic test mode,
retry handling, token counting, usage tracking, cost estimation, and logging.
"""

from agentic_devtools.orchestration.llm.base_provider import LLMProvider
from agentic_devtools.orchestration.llm.call_logger import CallLogger, LogLevel, log_llm_call
from agentic_devtools.orchestration.llm.config import (
    LLMConfigSnapshot,
    load_config,
    resolve_node_config,
)
from agentic_devtools.orchestration.llm.config_schema import CONFIG_SCHEMA, validate_config
from agentic_devtools.orchestration.llm.cost_estimator import CostEstimator, PricingTable, estimate_cost
from agentic_devtools.orchestration.llm.errors import (
    AuthenticationError,
    ContextWindowOverflowError,
    DuplicateNodeMappingError,
    FixtureVersionMismatchError,
    LLMError,
    ModelNotAvailableError,
    NoFixtureFoundError,
    ProviderNotConfiguredError,
    RateLimitExhaustedError,
    RetryExhaustedError,
    StreamInterruptedError,
    StructuredOutputValidationError,
)
from agentic_devtools.orchestration.llm.factory import ProviderFactory, get_provider
from agentic_devtools.orchestration.llm.retry import RetryConfig, RetryHandler, execute_with_retry
from agentic_devtools.orchestration.llm.token_counter import (
    TokenCounter,
    TruncationStrategy,
    check_context_window,
    count_tokens,
)
from agentic_devtools.orchestration.llm.types import (
    LLMMessage,
    LLMResponse,
    ModelConfig,
    NodeConfig,
    ProviderConfig,
    ProviderType,
    StreamChunk,
    TokenUsage,
)
from agentic_devtools.orchestration.llm.usage_tracker import AggregateUsage, UsageTracker

__all__ = [
    # Base
    "LLMProvider",
    # Types
    "LLMMessage",
    "LLMResponse",
    "ModelConfig",
    "NodeConfig",
    "ProviderConfig",
    "ProviderType",
    "StreamChunk",
    "TokenUsage",
    # Errors
    "AuthenticationError",
    "ContextWindowOverflowError",
    "DuplicateNodeMappingError",
    "FixtureVersionMismatchError",
    "LLMError",
    "ModelNotAvailableError",
    "NoFixtureFoundError",
    "ProviderNotConfiguredError",
    "RateLimitExhaustedError",
    "RetryExhaustedError",
    "StreamInterruptedError",
    "StructuredOutputValidationError",
    # Config
    "CONFIG_SCHEMA",
    "LLMConfigSnapshot",
    "load_config",
    "resolve_node_config",
    "validate_config",
    # Factory
    "ProviderFactory",
    "get_provider",
    # Retry
    "RetryConfig",
    "RetryHandler",
    "execute_with_retry",
    # Token counting
    "TokenCounter",
    "TruncationStrategy",
    "check_context_window",
    "count_tokens",
    # Usage tracking
    "AggregateUsage",
    "UsageTracker",
    # Cost estimation
    "CostEstimator",
    "PricingTable",
    "estimate_cost",
    # Call logging
    "CallLogger",
    "LogLevel",
    "log_llm_call",
]
