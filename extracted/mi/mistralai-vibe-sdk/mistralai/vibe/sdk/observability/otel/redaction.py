"""Vibe-specific configuration for Mistral SDK OpenTelemetry redaction."""

import re
from collections.abc import Iterable, Sequence

from mistralai.extra.observability import (
    DEFAULT_REDACTED_VALUE,
    DEFAULT_SAFE_ATTRIBUTE_KEYS,
    DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
    DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
    DEFAULT_TOKEN_PATTERNS,
    AttributeRedactionPolicy,
)

VIBE_SAFE_ATTRIBUTE_KEYS = frozenset(
    {
        "vibe.sdk.agent_name",
        "vibe.sdk.callback_id",
        "vibe.sdk.callback_name",
        "vibe.sdk.conversation_id",
        "vibe.sdk.current_context_tokens",
        "vibe.sdk.duration_ms",
        "vibe.sdk.history_length",
        "vibe.sdk.message_task_id",
        "vibe.sdk.message_type",
        "vibe.sdk.model",
        "vibe.sdk.outcome",
        "vibe.sdk.patch_count",
        "vibe.sdk.path_length",
        "vibe.sdk.priority",
        "vibe.sdk.provider",
        "vibe.sdk.reason",
        "vibe.sdk.request_kind",
        "vibe.sdk.result_status",
        "vibe.sdk.run_mode",
        "vibe.sdk.session_id",
        "vibe.sdk.status",
        "vibe.sdk.task_id",
        "vibe.sdk.threshold",
    }
)


class VibeAttributeRedactionPolicy(AttributeRedactionPolicy):
    """Mistral SDK attribute redaction policy preconfigured for Vibe SDK spans."""

    def __init__(
        self,
        *,
        additional_safe_keys: Iterable[str] = (),
        sensitive_keys: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
        sensitive_fragments: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
        token_patterns: Sequence[re.Pattern[str]] = DEFAULT_TOKEN_PATTERNS,
        redact_non_primitive: bool = True,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
        emit_redaction_metadata: bool = True,
    ) -> None:
        additional_safe_key_set = frozenset(key.lower() for key in additional_safe_keys)
        super().__init__(
            sensitive_keys=sensitive_keys,
            safe_keys=(
                DEFAULT_SAFE_ATTRIBUTE_KEYS | VIBE_SAFE_ATTRIBUTE_KEYS | additional_safe_key_set
            ),
            sensitive_fragments=sensitive_fragments,
            token_patterns=token_patterns,
            redact_non_primitive=redact_non_primitive,
            redacted_value=redacted_value,
            emit_redaction_metadata=emit_redaction_metadata,
        )
