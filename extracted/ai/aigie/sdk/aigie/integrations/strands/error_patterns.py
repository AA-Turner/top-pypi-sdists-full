"""Regex patterns used by ErrorDetector to classify error text.

``(regex, error_type, severity, is_transient)``; patterns are intentionally
specific to avoid matching benign content.
"""

from __future__ import annotations

from .error_types import ErrorSeverity, ErrorType

ERROR_PATTERNS: list[tuple[str, ErrorType, ErrorSeverity, bool]] = [
    # Rate limiting - specific error messages
    (
        r"rate.?limit(?:ed|ing)?|http.?429|too many requests|quota exceeded|throttl(?:ed|ing)",
        ErrorType.RATE_LIMIT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:server|api|service)\s+(?:is\s+)?(?:overloaded|busy)|capacity\s+exceeded",
        ErrorType.RATE_LIMIT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Timeout - specific error messages
    (
        r"(?:request|connection|operation)\s+(?:timed?.?out|timeout)",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"deadline\s+exceeded|read.?timeout|write.?timeout|connect.?timeout",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Network - specific error indicators
    (
        r"connection\s+(?:refused|reset|failed|error)|socket\s+error",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:network|dns)\s+(?:error|failure|unreachable)",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"ssl.?(?:error|handshake|certificate)|tls.?(?:error|handshake)",
        ErrorType.NETWORK,
        ErrorSeverity.HIGH,
        True,
    ),
    # Concurrency - specific tool error
    (
        r"tool.?use.?concurrency|concurrent.?(?:request|limit)|parallel.?limit",
        ErrorType.CONCURRENCY,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Server errors - HTTP status codes with context
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?(?:500|502|503|504)(?:\s|:|$)",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"internal\s+server\s+error|server\s+error|service\s+unavailable",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Authentication - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?401(?:\s|:|$)|unauthorized",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"(?:invalid|expired|missing)\s+(?:api.?key|token|credentials)",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    # Permission - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?403(?:\s|:|$)|forbidden",
        ErrorType.PERMISSION,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"permission\s+denied|access\s+denied|not\s+(?:allowed|authorized)",
        ErrorType.PERMISSION,
        ErrorSeverity.HIGH,
        False,
    ),
    # Not found - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?404(?:\s|:|$)",
        ErrorType.NOT_FOUND,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:resource|file|path)\s+not\s+found|does\s+not\s+exist|no\s+such\s+file",
        ErrorType.NOT_FOUND,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Validation - specific error messages
    (
        r"(?:http\s*)?(?:status\s*)?(?:code\s*)?400(?:\s|:|$)|bad\s+request",
        ErrorType.VALIDATION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:invalid|malformed)\s+(?:request|input|parameter|argument)",
        ErrorType.VALIDATION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"missing\s+required\s+(?:field|parameter)|required\s+field\s+missing",
        ErrorType.VALIDATION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Context length - specific model errors
    (
        r"context.?length\s+exceeded|max.?tokens?\s+exceeded|token\s+limit",
        ErrorType.CONTEXT_LENGTH,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:input|prompt|message)\s+too\s+long", ErrorType.CONTEXT_LENGTH, ErrorSeverity.HIGH, False),
    # Strands-specific: agent loop hits max_tokens limit
    (
        r"unrecoverable\s+state\s+due\s+to\s+max_tokens",
        ErrorType.CONTEXT_LENGTH,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"MaxTokensReachedException", ErrorType.CONTEXT_LENGTH, ErrorSeverity.MEDIUM, False),
    # Model errors - specific model-related errors
    (
        r"model\s+(?:error|failed|unavailable|not\s+found)",
        ErrorType.MODEL_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    # Quota exceeded
    (r"resource.?exhausted|resourceexhausted", ErrorType.QUOTA_EXCEEDED, ErrorSeverity.HIGH, True),
    (r"quota.*exceeded|exceeded.*quota", ErrorType.QUOTA_EXCEEDED, ErrorSeverity.HIGH, False),
    # Safety / Content filtering
    (
        r"safety.?(?:filter|block|rating)|content.?blocked",
        ErrorType.SAFETY_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"harmful.?content|blocked.?(?:due|by).?safety",
        ErrorType.SAFETY_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"finish.?reason.*safety|safety.*finish.?reason",
        ErrorType.SAFETY_FILTER,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"blocked_reason|candidatesblockedreason",
        ErrorType.CONTENT_BLOCKED,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Agent errors
    (r"agent\s+(?:error|failed|exception)", ErrorType.AGENT_ERROR, ErrorSeverity.HIGH, False),
    (
        r"(?:infinite|endless)\s+loop|loop\s+detected",
        ErrorType.AGENT_LOOP,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"max.?(?:iterations?|turns?|steps?)\s+(?:reached|exceeded)",
        ErrorType.AGENT_LOOP,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Tool errors - specific tool execution errors
    (
        r"tool\s+(?:execution|call)\s+(?:error|failed)",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"command\s+(?:execution\s+)?failed|execution\s+error",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:unknown|unsupported|invalid)\s+tool",
        ErrorType.TOOL_NOT_FOUND,
        ErrorSeverity.HIGH,
        False,
    ),
    # Python exceptions - common runtime errors
    (
        r"name\s+['\"]?\w+['\"]?\s+is\s+not\s+defined",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"(?:NameError|TypeError|ValueError|KeyError|IndexError|AttributeError):\s*",
        ErrorType.TOOL_EXECUTION,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"SyntaxError:\s*", ErrorType.VALIDATION, ErrorSeverity.MEDIUM, False),
    (r"ImportError|ModuleNotFoundError", ErrorType.TOOL_EXECUTION, ErrorSeverity.MEDIUM, False),
    (r"\[EXIT\s*CODE\]:\s*[1-9]\d*", ErrorType.TOOL_EXECUTION, ErrorSeverity.MEDIUM, False),
    # API errors - generic API failure patterns
    (r"api\s+(?:error|failure|unavailable)", ErrorType.API_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"api\s+call\s+failed|api\s+request\s+failed",
        ErrorType.API_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"failed\s+to\s+(?:fetch|get|retrieve|connect)",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
]
