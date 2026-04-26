"""Model-aware context threshold derivation."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MODEL_CONTEXT_WINDOW = 128_000
DEFAULT_MAX_OUTPUT_TOKENS = 4_096
DEFAULT_CONTEXT_WARN_TOKENS = 80_000
DEFAULT_CONTEXT_AUTO_COMPACT_TOKENS = 100_000
DEFAULT_SUMMARY_TRIGGER_TOKEN_COUNT = 90_000

DEFAULT_CONTEXT_WARN_BUFFER_TOKENS = (
    DEFAULT_MODEL_CONTEXT_WINDOW - DEFAULT_MAX_OUTPUT_TOKENS - DEFAULT_CONTEXT_WARN_TOKENS
)
DEFAULT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS = (
    DEFAULT_MODEL_CONTEXT_WINDOW - DEFAULT_MAX_OUTPUT_TOKENS - DEFAULT_CONTEXT_AUTO_COMPACT_TOKENS
)
DEFAULT_SUMMARY_TRIGGER_BUFFER_TOKENS = (
    DEFAULT_MODEL_CONTEXT_WINDOW - DEFAULT_MAX_OUTPUT_TOKENS - DEFAULT_SUMMARY_TRIGGER_TOKEN_COUNT
)

MIN_MODEL_CONTEXT_WINDOW = 1_000
MAX_MODEL_CONTEXT_WINDOW = 2_000_000
MIN_CLI_CONTEXT_THRESHOLD = 1_000
MAX_CLI_CONTEXT_THRESHOLD = 1_000_000
MIN_SUMMARY_TRIGGER_TOKEN_COUNT = 5_000
MAX_SUMMARY_TRIGGER_TOKEN_COUNT = 500_000

_WARN_FLOOR_RATIO = 0.625
_SUMMARY_FLOOR_RATIO = 0.70
_AUTO_COMPACT_FLOOR_RATIO = 0.78


@dataclass(frozen=True)
class ContextThresholdConfig:
    """Inputs used to resolve active context thresholds."""

    model_context_window: int = DEFAULT_MODEL_CONTEXT_WINDOW
    reserved_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    warn_buffer_tokens: int = DEFAULT_CONTEXT_WARN_BUFFER_TOKENS
    auto_compact_buffer_tokens: int = DEFAULT_CONTEXT_AUTO_COMPACT_BUFFER_TOKENS
    summary_trigger_buffer_tokens: int = DEFAULT_SUMMARY_TRIGGER_BUFFER_TOKENS
    explicit_warn_tokens: int | None = None
    explicit_auto_compact_tokens: int | None = None
    explicit_summary_trigger_token_count: int | None = None


@dataclass(frozen=True)
class ContextThresholds:
    """Resolved context thresholds used by CLI, web, and shared agent loop."""

    model_context_window: int
    reserved_output_tokens: int
    effective_context_window: int
    context_warn_tokens: int
    context_auto_compact_tokens: int
    summary_trigger_token_count: int


def _clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _derived_threshold(
    *,
    effective_window: int,
    buffer_tokens: int,
    floor_ratio: float,
    minimum: int,
    maximum: int,
) -> int:
    buffered = effective_window - max(0, buffer_tokens)
    ratio_floor = int(effective_window * floor_ratio)
    return _clamp(max(buffered, ratio_floor), minimum, min(maximum, effective_window))


def derive_context_thresholds(config: ContextThresholdConfig) -> ContextThresholds:
    """Resolve context thresholds from model window, output reserve, buffers, and overrides."""

    model_window = _clamp(config.model_context_window, MIN_MODEL_CONTEXT_WINDOW, MAX_MODEL_CONTEXT_WINDOW)
    reserved = _clamp(config.reserved_output_tokens, 0, model_window - MIN_MODEL_CONTEXT_WINDOW)
    effective_window = max(MIN_MODEL_CONTEXT_WINDOW, model_window - reserved)

    warn = (
        _clamp(config.explicit_warn_tokens, MIN_CLI_CONTEXT_THRESHOLD, MAX_CLI_CONTEXT_THRESHOLD)
        if config.explicit_warn_tokens is not None
        else _derived_threshold(
            effective_window=effective_window,
            buffer_tokens=config.warn_buffer_tokens,
            floor_ratio=_WARN_FLOOR_RATIO,
            minimum=MIN_CLI_CONTEXT_THRESHOLD,
            maximum=MAX_CLI_CONTEXT_THRESHOLD,
        )
    )
    auto = (
        _clamp(config.explicit_auto_compact_tokens, MIN_CLI_CONTEXT_THRESHOLD, MAX_CLI_CONTEXT_THRESHOLD)
        if config.explicit_auto_compact_tokens is not None
        else _derived_threshold(
            effective_window=effective_window,
            buffer_tokens=config.auto_compact_buffer_tokens,
            floor_ratio=_AUTO_COMPACT_FLOOR_RATIO,
            minimum=MIN_CLI_CONTEXT_THRESHOLD,
            maximum=MAX_CLI_CONTEXT_THRESHOLD,
        )
    )
    summary = (
        _clamp(
            config.explicit_summary_trigger_token_count,
            MIN_SUMMARY_TRIGGER_TOKEN_COUNT,
            MAX_SUMMARY_TRIGGER_TOKEN_COUNT,
        )
        if config.explicit_summary_trigger_token_count is not None
        else _derived_threshold(
            effective_window=effective_window,
            buffer_tokens=config.summary_trigger_buffer_tokens,
            floor_ratio=_SUMMARY_FLOOR_RATIO,
            minimum=MIN_SUMMARY_TRIGGER_TOKEN_COUNT,
            maximum=MAX_SUMMARY_TRIGGER_TOKEN_COUNT,
        )
    )

    if config.explicit_warn_tokens is None and config.explicit_auto_compact_tokens is None and warn >= auto:
        warn = max(MIN_CLI_CONTEXT_THRESHOLD, auto - 1)
    if config.explicit_summary_trigger_token_count is None:
        if config.explicit_warn_tokens is None:
            summary = max(summary, min(warn + 1, effective_window))
        if config.explicit_auto_compact_tokens is None:
            summary = min(summary, max(auto - 1, MIN_SUMMARY_TRIGGER_TOKEN_COUNT))

    return ContextThresholds(
        model_context_window=model_window,
        reserved_output_tokens=reserved,
        effective_context_window=effective_window,
        context_warn_tokens=warn,
        context_auto_compact_tokens=auto,
        summary_trigger_token_count=summary,
    )
