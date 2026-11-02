"""Redaction policies for ``agents.Agent(redaction=...)``."""

import temporalio.workflow

from mistralai.agents import _silence

# Direct submodule imports bypass the parent package's lazy `__getattr__`, so apply the same
# Temporal passthrough and log quieting here, as `mistralai.agents.pattern` does.
with temporalio.workflow.unsafe.imports_passed_through():
    _silence.presilence()
    try:
        from mistralai.vibe_agents.sdk.quiet import quiet_local_sdk_logs

        quiet_local_sdk_logs()
        from mistralai.observability.otel import (
            CARD_NUMBER_PATTERN,
            DEFAULT_PII_SECRET_PATTERNS,
            DEFAULT_REDACTED_VALUE,
            DEFAULT_SAFE_ATTRIBUTE_KEYS,
            DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
            DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
            DEFAULT_TOKEN_PATTERNS,
            EMAIL_PATTERN,
            IPV4_PATTERN,
            AttributeMaskCallback,
            AttributeRedactionPolicy,
            CallbackRedactionPolicy,
            RegexRedactionPolicy,
        )
        from mistralai.vibe_agents.sdk.authoring.redaction import Redaction, RedactionPolicy
    finally:
        _silence.restore_runtime_warning_levels()

__all__ = [
    "CARD_NUMBER_PATTERN",
    "DEFAULT_PII_SECRET_PATTERNS",
    "DEFAULT_REDACTED_VALUE",
    "DEFAULT_SAFE_ATTRIBUTE_KEYS",
    "DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS",
    "DEFAULT_SENSITIVE_ATTRIBUTE_KEYS",
    "DEFAULT_TOKEN_PATTERNS",
    "EMAIL_PATTERN",
    "IPV4_PATTERN",
    "AttributeMaskCallback",
    "AttributeRedactionPolicy",
    "CallbackRedactionPolicy",
    "Redaction",
    "RedactionPolicy",
    "RegexRedactionPolicy",
]
