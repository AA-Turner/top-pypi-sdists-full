"""Built-in policies for redacting structured operation data."""

import copy
import re
from collections.abc import Callable, Mapping, Sequence
from typing import Final

from .hooks import OperationDataContext, OperationDataValue

type AttributeMaskCallback = Callable[[str, OperationDataValue], OperationDataValue | None]

DEFAULT_REDACTED_VALUE: Final[str] = "[REDACTED]"

# Keep these policy defaults aligned with mistralai/client-python:
# https://github.com/mistralai/client-python/blob/68172b9acdc6c3095e9fe854c7008d9e9d61211f/src/mistralai/extra/observability/redaction_policies.py
DEFAULT_SENSITIVE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "client.address",
        "db.query.text",
        "db.statement",
        "exception.message",
        "exception.stacktrace",
        "gen_ai.input.messages",
        "gen_ai.output.messages",
        "gen_ai.tool.definitions",
        "gen_ai.tool.call.arguments",
        "gen_ai.tool.call.result",
        "http.request.body",
        "http.request.header.authorization",
        "http.request.header.cookie",
        "http.response.body",
        "http.response.header.set-cookie",
        "http.target",
        "http.url",
        "server.address",
        "url.full",
        "url.path",
        "url.query",
    }
)
DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS: Final[frozenset[str]] = frozenset(
    {
        "api_key",
        "argument",
        "arguments",
        "authorization",
        "body",
        "completion",
        "content",
        "cookie",
        "input",
        "message",
        "messages",
        "output",
        "password",
        "payload",
        "prompt",
        "secret",
        "set_cookie",
        "token",
    }
)
DEFAULT_SAFE_ATTRIBUTE_KEYS: Final[frozenset[str]] = frozenset(
    {
        "agent.trace.public",
        "client.port",
        "error.type",
        "exception.type",
        "gen_ai.agent.id",
        "gen_ai.agent.name",
        "gen_ai.agent.version",
        "gen_ai.conversation.id",
        "gen_ai.data_source.id",
        "gen_ai.memory.record.id",
        "gen_ai.memory.store.id",
        "gen_ai.operation.name",
        "gen_ai.output.type",
        "gen_ai.prompt.name",
        "gen_ai.prompt.version",
        "gen_ai.provider.name",
        "gen_ai.request.max_tokens",
        "gen_ai.request.model",
        "gen_ai.response.finish_reasons",
        "gen_ai.response.id",
        "gen_ai.response.model",
        "gen_ai.token.type",
        "gen_ai.tool.call.id",
        "gen_ai.tool.name",
        "gen_ai.tool.type",
        "http.request.method",
        "http.response.status_code",
        "mistral.connector.id",
        "mistral.conversation.parent.id",
        "mistral.obs.features.judge",
        "mistral.turn.id",
        "mistral.vibe_work.connector.id",
        "network.protocol.name",
        "network.protocol.version",
        "server.port",
        "url.scheme",
    }
)
DEFAULT_TOKEN_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b[sr]k_(?:live|test)_[0-9A-Za-z]{10,}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}\b"),
    re.compile(r"\bsk-proj-[A-Za-z0-9\-_]{20,}\b"),
    re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bmstrl_[0-9A-Za-z]{32}_[0-9A-Za-z]{6}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b"),
    re.compile(r"\bglpat-[A-Za-z0-9\-=_]{20,22}\b"),
    re.compile(r"\bshp(?:at|ca|pa|ss)_[a-fA-F0-9]{32}\b"),
    re.compile(r"\bsq0(?:atp|csp|idp)-[0-9A-Za-z\-_]{22,43}\b"),
    re.compile(r"\bPMAK-[a-zA-Z0-9]{24,59}\b"),
    re.compile(r"\bphc_[a-zA-Z0-9_]{43}\b"),
    re.compile(r"\brubygems_[a-f0-9]{48}\b"),
    re.compile(r"\blin_api_[0-9A-Za-z]{40}\b"),
    re.compile(r"pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]{50,}"),
    re.compile(r"\bsecret_[A-Za-z0-9]{43}\b"),
    re.compile(r"[A-Za-z0-9]{14}\.atlasv1\.[A-Za-z0-9]{60,}"),
    re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b"),
    re.compile(r"\bpk_(?:live|test)_[0-9a-zA-Z]{24}\b"),
    re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/+]{40,}"),
    re.compile(r"https://discord(?:app)?\.com/api/webhooks/[0-9]{17,}/[A-Za-z0-9\-_]{60,}"),
    re.compile(r"https://hooks\.zapier\.com/hooks/catch/[A-Za-z0-9/]{16,}"),
)
EMAIL_PATTERN: Final[re.Pattern[str]] = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
CARD_NUMBER_PATTERN: Final[re.Pattern[str]] = re.compile(r"\b(?:\d[ -]?){13,16}\b")
IPV4_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)
DEFAULT_PII_SECRET_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    *DEFAULT_TOKEN_PATTERNS,
    EMAIL_PATTERN,
    CARD_NUMBER_PATTERN,
    IPV4_PATTERN,
)

_SAFE_KEY_PREFIXES: Final[tuple[str, ...]] = ("gen_ai.usage.",)
_PRIMITIVE_TYPES: Final[tuple[type, ...]] = (str, bool, int, float)


class RegexRedactionPolicy:
    """Redact known PII and secret patterns while preserving value structure."""

    def __init__(
        self,
        patterns: Sequence[re.Pattern[str]] = DEFAULT_PII_SECRET_PATTERNS,
        *,
        safe_keys: frozenset[str] = DEFAULT_SAFE_ATTRIBUTE_KEYS,
        safe_key_patterns: Sequence[re.Pattern[str]] = DEFAULT_TOKEN_PATTERNS,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
    ) -> None:
        """Configure compiled patterns, safe keys and their replacement value."""
        self._patterns = tuple(patterns)
        self._safe_keys = safe_keys
        self._safe_key_patterns = tuple(safe_key_patterns)
        self._redacted_value = redacted_value

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue:
        """Redact every matching string leaf in a structured telemetry value."""
        normalized_key = context.field.lower()
        if normalized_key in self._safe_keys or normalized_key.startswith(_SAFE_KEY_PREFIXES):
            return _redact_value(value, self._safe_key_patterns, self._redacted_value)
        return _redact_value(value, self._patterns, self._redacted_value)


class AttributeRedactionPolicy:
    """Redact sensitive fields wholesale and scan retained values for tokens."""

    def __init__(
        self,
        *,
        sensitive_keys: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_KEYS,
        safe_keys: frozenset[str] = DEFAULT_SAFE_ATTRIBUTE_KEYS,
        sensitive_fragments: frozenset[str] = DEFAULT_SENSITIVE_ATTRIBUTE_FRAGMENTS,
        token_patterns: Sequence[re.Pattern[str]] = DEFAULT_TOKEN_PATTERNS,
        redact_non_primitive: bool = True,
        redacted_value: str = DEFAULT_REDACTED_VALUE,
    ) -> None:
        """Configure key classification and fallback token scanning."""
        self._sensitive_keys = sensitive_keys
        self._safe_keys = safe_keys
        self._sensitive_fragments = sensitive_fragments
        self._token_patterns = tuple(token_patterns)
        self._redact_non_primitive = redact_non_primitive
        self._redacted_value = redacted_value

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue:
        """Apply key-oriented redaction to one operation field."""
        if value is None:
            return None
        if context.field == "span.name":
            return value
        if context.field == "status.description":
            return self._redacted_value
        if self._should_redact(context.field, value):
            return self._redacted_value
        return _redact_value(value, self._token_patterns, self._redacted_value)

    def _should_redact(self, key: str, value: object) -> bool:
        normalized_key = key.lower()
        if normalized_key in self._safe_keys or normalized_key.startswith(_SAFE_KEY_PREFIXES):
            return False
        if normalized_key in self._sensitive_keys or self._has_sensitive_fragment(normalized_key):
            return True
        return self._redact_non_primitive and not isinstance(value, _PRIMITIVE_TYPES)

    def _has_sensitive_fragment(self, normalized_key: str) -> bool:
        normalized_path = normalized_key.replace("-", "_").replace(".", "_")
        # Deliberately match substrings conservatively; exact safe keys take
        # precedence in _should_redact for useful metadata such as token type.
        return any(fragment in normalized_path for fragment in self._sensitive_fragments)


class CallbackRedactionPolicy:
    """Adapt a per-field masking callback to the operation transformer API.

    With ``recursive=True``, the callback receives each leaf of structured values,
    such as the text of every message, with the field name as key. Returning
    ``None`` drops that leaf only.
    """

    def __init__(self, mask_function: AttributeMaskCallback, *, recursive: bool = False) -> None:
        """Configure the callback invoked for each operation field or leaf."""
        self._mask_function = mask_function
        self._recursive = recursive

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: OperationDataContext,
    ) -> OperationDataValue | None:
        """Return the callback result for this operation field."""
        if context.field == "span.name":
            return value
        if self._recursive:
            return _map_leaves(value, lambda leaf: self._mask_function(context.field, leaf))
        # The value may be the caller's own object: a callback that edits it in place must not change it.
        return self._mask_function(context.field, copy.deepcopy(value))


def _redact_value(
    value: OperationDataValue,
    patterns: Sequence[re.Pattern[str]],
    redacted_value: str,
) -> OperationDataValue:
    def redact_leaf(leaf: OperationDataValue) -> OperationDataValue:
        if not isinstance(leaf, str):
            return leaf
        for pattern in patterns:
            leaf = pattern.sub(redacted_value, leaf)
        return leaf

    return _map_leaves(value, redact_leaf)


def _map_leaves(
    value: OperationDataValue,
    leaf_function: Callable[[OperationDataValue], OperationDataValue | None],
) -> OperationDataValue | None:
    """Apply ``leaf_function`` to every leaf, dropping the leaves it maps to ``None``.

    Leaves that were already ``None`` are kept.
    """
    if isinstance(value, bytes):
        value = value.decode(errors="replace")
    if isinstance(value, Mapping):
        return {
            key: mapped
            for key, item in value.items()
            if (mapped := _map_leaves(item, leaf_function)) is not None or item is None
        }
    if isinstance(value, Sequence) and not isinstance(value, str):
        items = [mapped for item in value if (mapped := _map_leaves(item, leaf_function)) is not None or item is None]
        return tuple(items) if isinstance(value, tuple) else items
    return leaf_function(value)
