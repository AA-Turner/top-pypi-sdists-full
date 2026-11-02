"""Convert LLM API payloads between OpenAI Chat Completions, Anthropic Messages,
and Open Responses formats.

Supports request conversion, response conversion, and streaming response
conversion (sync and async). Powered by a Rust core for speed.

Quick start::

    import linguafranca as lf

    result = lf.convert_request_json(
        {"model": "gpt-4.1-mini", "messages": [{"role": "user", "content": "hi"}]},
        source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
        target_format=lf.FormatName.ANTHROPIC_MESSAGES,
    )
    print(result.value)       # converted dict
    print(result.warnings)    # lossy-conversion warnings
"""

from .api import (
    AsyncStreamConversion,
    ConversionConfig,
    ConversionResult,
    ConversionWarning,
    FormatName,
    StreamConversion,
    acollect_response_stream,
    acollect_response_stream_json,
    aconvert_response_stream,
    collect_response_stream,
    collect_response_stream_json,
    convert_request,
    convert_request_json,
    convert_response,
    convert_response_json,
    convert_response_stream,
    convert_response_stream_json,
    decompose_response_to_stream,
    decompose_response_to_stream_json,
    to_chat_completions_request,
    to_chat_completions_response,
    to_messages_request,
    to_messages_response,
)
from ._linguafranca import (
    ConversionError,
    InvalidInputError,
    SchemaValidationError,
    UnsupportedConversionError,
)

__all__ = [
    "FormatName",
    "ConversionConfig",
    "ConversionWarning",
    "ConversionResult",
    "StreamConversion",
    "AsyncStreamConversion",
    "ConversionError",
    "InvalidInputError",
    "UnsupportedConversionError",
    "SchemaValidationError",
    "convert_request",
    "convert_response",
    "convert_request_json",
    "convert_response_json",
    "convert_response_stream",
    "convert_response_stream_json",
    "aconvert_response_stream",
    "collect_response_stream",
    "collect_response_stream_json",
    "acollect_response_stream",
    "acollect_response_stream_json",
    "decompose_response_to_stream",
    "decompose_response_to_stream_json",
    "to_messages_request",
    "to_messages_response",
    "to_chat_completions_request",
    "to_chat_completions_response",
]
