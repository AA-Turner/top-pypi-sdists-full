"""SETTING REJECTIONS — a provider refusing a request because of one of its SETTINGS.

Settings Translation R1 (contract K10, common-docs/projects/settings-translation/
CONTRACTS.md). Before this module every provider 400 became ``invalid_request``:
credit exhaustion, an empty message list, a broken schema and a real settings
mistake all wore one label, and the machine-readable culprit (``param``/``code``)
was thrown away in ``errors._extract_error_body``. A routine keyed on that label
saw about three non-settings rows for every settings row.

Two halves, both pure until ``report_setting_rejection`` files the record:

1. **Recognition** (``recognize``) — called by ``errors._handle_bad_request`` /
   ``_handle_unprocessable``, the two handlers every provider's 400/422 passes
   through, chat AND media. Structured fields first (the provider's ``param`` /
   ``code``), then the provider-specific message shapes in ``RECOGNIZERS`` —
   every row's example is a real message from ``ops.ops_issue_event`` and is a
   test fixture (tests/test_setting_rejection.py). A param that names CONTENT or
   a SCHEMA (messages, input, tools, response_format…) is never a setting, and a
   billing refusal never is either.

2. **The record** (``build_record``) — the K10 payload, assembled from the
   classification plus whatever the caller can see: the wire body that was sent
   (the ambient ExecutionState's captured payload, or the media kwargs attached
   to the exception), the canonical config, the resolved call profile and the
   pre-allocated failure snapshot id. ``failure_report.report_provider_failure``
   (THE one door) files it as ONE ``ops.system_error`` row of kind
   ``PROVIDER_SETTING_REJECTED_KIND`` with ``payload.lifecycle = "new"``.

Never raises into the provider path: every helper degrades to ``None``/empty.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

#: The typed class. ``RetryableError.error_type`` for a settings rejection; the
#: issue key is ``f"{provider}.{SETTING_REJECTION_ERROR_TYPE}"``.
SETTING_REJECTION_ERROR_TYPE = "invalid_setting"

#: ``ops.system_error.kind`` of THE store of record for a settings rejection.
PROVIDER_SETTING_REJECTED_KIND = "provider_setting_rejected"

#: K10 lifecycle, in order. A new record is always ``new``.
LIFECYCLE = ("new", "proposed", "proven", "applied", "verified")

# Attribute a media adapter stamps on its exception with the kwargs it sent
# (media providers do not use ``capture_request_payload``).
_WIRE_ATTR = "_matrx_wire_payload"


# ── recognition ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SettingRejection:
    """What the provider told us about the setting it refused."""

    provider: str  # routing key: groq, openai, google…
    provider_param: str | None  # wire field, e.g. max_completion_tokens; None = opaque
    provider_code: str | None
    provider_type: str | None
    provider_message: str
    provider_limit: Any  # parsed when the provider states one
    shape: str  # above_max | string_too_long | too_many_items | invalid_item | deprecated | unsupported | mode_unsupported | combination | invalid_value | opaque
    recognizer: str  # "structured" or the RECOGNIZERS row id

    @property
    def opaque(self) -> bool:
        return self.provider_param is None

    def as_details(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "provider_param": self.provider_param,
            "provider_code": self.provider_code,
            "provider_type": self.provider_type,
            "provider_message": self.provider_message,
            "provider_limit": self.provider_limit,
            "shape": self.shape,
            "recognizer": self.recognizer,
            "opaque": self.opaque,
        }


@dataclass(frozen=True)
class Recognizer:
    """One provider message shape. ``example`` is the real message it was built from."""

    id: str
    providers: tuple[str, ...]  # where it was observed; matched there first
    pattern: re.Pattern[str]
    shape: str
    example: str
    param: str | None = None  # fixed param when the message names none in a group


def _rx(text: str) -> re.Pattern[str]:
    return re.compile(text, re.IGNORECASE)


# THE RECOGNIZER TABLE. Provider-specific shapes, second after structured
# fields. A new shape goes HERE (with its real message as ``example``, which the
# test suite replays), never into one provider's classifier.
RECOGNIZERS: tuple[Recognizer, ...] = (
    Recognizer(
        id="openai_compat.at_most",
        providers=("groq", "cerebras", "openai", "together", "xai"),
        pattern=_rx(r"`(?P<param>[\w.]+)` must be less than or equal to `?(?P<limit>\d+)`?"),
        shape="above_max",
        example=(
            "`max_completion_tokens` must be less than or equal to `16384`, the maximum value "
            "for `max_completion_tokens` is less than the `context_window` for this model"
        ),
    ),
    Recognizer(
        id="anthropic.deprecated",
        providers=("anthropic",),
        pattern=_rx(r"`(?P<param>[\w.]+)` is deprecated for this model"),
        shape="deprecated",
        example="`temperature` is deprecated for this model.",
    ),
    Recognizer(
        id="anthropic.cannot_both",
        providers=("anthropic",),
        pattern=_rx(r"`(?P<param>[\w.]+)` and `(?P<other>[\w.]+)` cannot both be specified"),
        shape="combination",
        example="`temperature` and `top_p` cannot both be specified for this model.",
    ),
    Recognizer(
        id="together.param_not_supported",
        providers=("together",),
        pattern=_rx(r"Parameter '(?P<param>[\w.]+)' is not supported for the selected model"),
        shape="unsupported",
        example=(
            "Parameter 'steps' is not supported for the selected model configuration. "
            "Please remove this parameter from your request."
        ),
    ),
    Recognizer(
        id="google.param_only_in_mode",
        providers=("google",),
        pattern=_rx(r"(?P<param>[\w.]+) parameter is only supported in (?P<limit>.+?) mode"),
        shape="mode_unsupported",
        example=(
            "generate_audio parameter is only supported in Gemini Enterprise Agent Platform "
            "mode, not in Gemini Developer API mode."
        ),
    ),
    Recognizer(
        id="google.param_not_supported_for",
        providers=("google",),
        pattern=_rx(r"The '(?P<param>[\w.]+)' parameter is not supported for"),
        shape="unsupported",
        example=(
            "The 'system_instruction' parameter is not supported for the "
            "deep-research-preview-04-2026 agent. Please include any specific instructions "
            "in the 'input' prompt instead."
        ),
    ),
    Recognizer(
        id="openai.string_too_long",
        providers=("openai",),
        pattern=_rx(
            r"Invalid '(?P<param>[\w.]+)': string too long\. Expected a string with maximum "
            r"length (?P<limit>\d+)"
        ),
        shape="string_too_long",
        example=(
            "Invalid 'prompt_cache_key': string too long. Expected a string with maximum "
            "length 64, but got a string with length 70 instead."
        ),
    ),
    Recognizer(
        id="openai.unsupported_parameter",
        providers=("openai", "xai", "cerebras", "groq"),
        pattern=_rx(r"Unsupported parameter: '(?P<param>[\w.]+)'"),
        shape="unsupported",
        example="Unsupported parameter: 'max_tokens' is not supported with this model.",
    ),
    Recognizer(
        id="openai.unsupported_value",
        providers=("openai", "xai", "cerebras", "groq"),
        pattern=_rx(r"Unsupported value: '(?P<param>[\w.]+)'"),
        shape="invalid_value",
        example="Unsupported value: 'temperature' does not support 0.2 with this model.",
    ),
    Recognizer(
        id="google.thinking_level_unsupported",
        providers=("google",),
        pattern=_rx(r"Thinking level \w+ is not supported for this model"),
        shape="invalid_value",
        example=(
            "Thinking level MINIMAL is not supported for this model. Please retry with other "
            "thinking level."
        ),
        param="thinking_config.thinking_level",
    ),
    Recognizer(
        id="xai.unsupported_value",
        providers=("xai",),
        pattern=_rx(r"does not support `(?P<param>[\w.]+)` value `"),
        shape="invalid_value",
        example="This model does not support `reasoning_effort` value `none`.",
    ),
    # LIST-valued settings (stop sequences). Every example below is the real
    # message, captured live 2026-10-04 (FIXV1: Groq conversation fdf78037…,
    # Anthropic 555d5547…, the rest from a direct 5/10/16-item probe).
    Recognizer(
        id="groq.max_items",
        providers=("groq",),
        pattern=_rx(r"'(?P<param>[\w.]+)' : maximum number of items is (?P<limit>\d+)"),
        shape="too_many_items",
        example=(
            "'stop' : one of the following must be satisfied[('stop' : value must be a string) "
            "OR ('stop' : maximum number of items is 4)]"
        ),
    ),
    Recognizer(
        id="openai_compat.array_too_long",
        providers=("moonshot", "openai", "together", "xai", "cerebras", "groq"),
        pattern=_rx(
            r"(?:Invalid '(?P<param>[\w.]+)':|request:\s*(?P<bare>[\w.]+)) array too long\. "
            r"Expected an array with maximum length (?P<limit>\d+)"
        ),
        shape="too_many_items",
        example=(
            "Invalid request: stop array too long. Expected an array with maximum length 5, "
            "but got an array with length 10 instead"
        ),
    ),
    Recognizer(
        id="together.max_stop_sequences",
        providers=("together",),
        pattern=_rx(r"(?P<param>[\w.]+): Validation error: maximum (?P<limit>\d+) stop sequences allowed"),
        shape="too_many_items",
        example=(
            'stop: Validation error: maximum 4 stop sequences allowed [{"value": Array '
            '[String("ZQ0X"), String("ZQ1X"), String("ZQ2X"), String("ZQ3X"), String("ZQ4X")]}]'
        ),
    ),
    Recognizer(
        id="xai.max_stop_strings",
        providers=("xai",),
        pattern=_rx(r"Cannot provide more than (?P<limit>\d+) stop strings"),
        shape="too_many_items",
        example="Cannot provide more than 8 stop strings but len(stop) = 10",
        param="stop",
    ),
    # Cerebras answers a list-length refusal as a pydantic validation error with
    # code wrong_api_format and param "validation_error" (live 2026-10-04).
    Recognizer(
        id="cerebras.list_at_most",
        providers=("cerebras",),
        pattern=_rx(r"(?P<param>[\w.]+)\.list\[\w+\]: List should have at most (?P<limit>\d+) items"),
        shape="too_many_items",
        example=(
            "stop.str: Input should be a valid string\nstop.list[str]: List should have at most "
            "4 items after validation, not 5"
        ),
    ),
    Recognizer(
        id="anthropic.stop_sequence_whitespace",
        providers=("anthropic",),
        pattern=_rx(r"(?P<param>[\w.]+): each stop sequence must contain non-whitespace"),
        shape="invalid_item",
        example="stop_sequences: each stop sequence must contain non-whitespace",
    ),
    # Live 2026-10-04 (V2 verifier battery 3g) — each landed as an unrecognised
    # ``provider_request_failed`` with no fingerprint before these rows existed.
    Recognizer(
        id="groq.number_at_most",
        providers=("groq",),
        pattern=_rx(r"'(?P<param>[\w.]+)'\s*:\s*number must be at most (?P<limit>\d+)"),
        shape="above_max",
        example="'temperature' : number must be at most 2",
    ),
    Recognizer(
        id="xai.does_not_support_parameter",
        providers=("xai",),
        pattern=_rx(r"does not support parameter (?P<param>[\w.]+?)\.?(?:\s|\"|$)"),
        shape="unsupported",
        example="Model grok-4.20-0309-reasoning does not support parameter stop.",
    ),
    Recognizer(
        id="google.thinking_budget_range",
        providers=("google",),
        pattern=_rx(r"thinking budget -?\d+ is invalid\. Please choose a value between -?\d+ and (?P<limit>\d+)"),
        shape="above_max",
        example="The thinking budget 64000 is invalid. Please choose a value between 128 and 32768.",
        param="thinking_config.thinking_budget",
    ),
    # Range refusals boundary-probed live 2026-10-04 (NET lane census).
    Recognizer(
        id="cerebras.input_le",
        providers=("cerebras",),
        pattern=_rx(r"(?P<param>[\w.]+): Input should be less than or equal to (?P<limit>\d+)"),
        shape="above_max",
        example="temperature: Input should be less than or equal to 2",
    ),
    Recognizer(
        id="together.must_be_within",
        providers=("together",),
        pattern=_rx(r"(?P<param>[\w.]+) must be within \[-?[\d.]+, (?P<limit>\d+)\]"),
        shape="above_max",
        example="temperature must be within [0, 1], got 2",
    ),
    # Google's opaque 400: no param anywhere. A settings rejection we cannot
    # pin to a field — the record carries ``suspect_params`` instead.
    Recognizer(
        id="google.opaque_invalid_argument",
        providers=("google",),
        pattern=_rx(r"Request contains an invalid argument\."),
        shape="opaque",
        example="Request contains an invalid argument.",
    ),
)

# A ``param`` naming CONTENT or a SCHEMA is never a setting: schema problems,
# message problems and tool problems have their own classes and routines.
_NON_SETTING_PARAM_PREFIXES = (
    "messages",
    "input",
    "contents",
    "prompt",
    "tools",
    "functions",
    "response_format",
    "text.format",
    "output_config.format",
    "json_schema",
    "system",
)
_NON_SETTING_CODES = frozenset(
    {"invalid_json_schema", "wrong_api_format", "context_length_exceeded", "insufficient_quota"}
)

# Cerebras answers setting refusals as pydantic validation errors (code
# wrong_api_format): only these rows, built for those exact messages, may claim one.
_WRONG_API_FORMAT_SETTING_ROWS = frozenset({"cerebras.list_at_most", "cerebras.input_le"})

# Codes that, with a param, say "this setting's value/name was refused".
_CODE_SHAPES = {
    "string_above_max_length": "string_too_long",
    "integer_above_max_value": "above_max",
    "decimal_above_max_value": "above_max",
    "integer_below_min_value": "invalid_value",
    "decimal_below_min_value": "invalid_value",
    "unsupported_parameter": "unsupported",
    "unsupported_value": "invalid_value",
    "unknown_parameter": "unsupported",
    "invalid_value": "invalid_value",
    "array_above_max_length": "too_many_items",
}

_LIMIT_PATTERNS = (
    re.compile(r"less than or equal to `?(\d+)`?", re.IGNORECASE),
    re.compile(r"maximum length (\d+)", re.IGNORECASE),
    re.compile(r"(?:at most|maximum(?: value)?(?: is)?|max(?:imum)?)\s*:?\s*`?(\d+)`?", re.IGNORECASE),
)

_PROVIDER_KEYS = {
    "together ai": "together",
    "ai provider": "generic_openai",
    "hugging face": "huggingface",
    "voyage ai": "voyage",
}


def provider_key(provider: str) -> str:
    """Display name or key → routing key (``"Together AI"`` → ``together``)."""
    lowered = (provider or "").strip().lower()
    return _PROVIDER_KEYS.get(lowered, lowered or "unknown")


def _is_non_setting_param(param: str) -> bool:
    p = param.strip().lower()
    return any(p == pre or p.startswith(pre + ".") or p.startswith(pre + "[") for pre in _NON_SETTING_PARAM_PREFIXES)


def _parse_limit(message: str) -> Any:
    for pattern in _LIMIT_PATTERNS:
        m = pattern.search(message)
        if m:
            try:
                return int(m.group(1))
            except (TypeError, ValueError):
                return m.group(1)
    return None


def _unwrap_google_message(message: str) -> str:
    """Google wraps its JSON error in a string: pull out the inner message."""
    m = re.search(r'"message"\s*:\s*"((?:[^"\\]|\\.)*)"', message)
    return m.group(1) if m else message


def _shape_from_message(message: str, default: str) -> str:
    lowered = message.lower()
    if "array too long" in lowered or "number of items" in lowered or "at most" in lowered and "items" in lowered:
        return "too_many_items"
    if "less than or equal" in lowered or "above max" in lowered:
        return "above_max"
    if "string too long" in lowered:
        return "string_too_long"
    if "deprecated" in lowered:
        return "deprecated"
    if "not supported" in lowered or "unsupported" in lowered or "unknown parameter" in lowered:
        return "unsupported"
    return default


def recognize(provider: str, message: str, body: dict[str, Any] | None) -> SettingRejection | None:
    """Is this bad request a SETTINGS rejection? Structured fields first, then shapes."""
    try:
        return _recognize(provider, message, body or {})
    except Exception:  # noqa: BLE001 — recognition never replaces the classification
        return None


def _recognize(provider: str, message: str, body: dict[str, Any]) -> SettingRejection | None:
    from matrx_ai.providers.errors import is_billing_refusal

    key = provider_key(provider)
    body_message = str(body.get("message") or "")
    text = body_message or message
    if is_billing_refusal(f"{message} {body_message}"):
        return None
    code = body.get("code")
    code = str(code) if code not in (None, "") else None
    ptype = body.get("type")
    ptype = str(ptype) if ptype not in (None, "") else None
    param = body.get("param")
    param = str(param) if param not in (None, "") else None
    if param == "validation_error":  # Cerebras: a category, not a field
        param = None
    if code in _NON_SETTING_CODES:
        # A validation-shaped code can still carry a SETTING refusal (Cerebras
        # list length); only rows built for that exact message may claim it.
        if code != "wrong_api_format":
            return None
        for rec in RECOGNIZERS:
            if rec.id in _WRONG_API_FORMAT_SETTING_ROWS:
                m = rec.pattern.search(text)
                if m:
                    return SettingRejection(
                        provider=key,
                        provider_param=m.group("param"),
                        provider_code=code,
                        provider_type=ptype,
                        provider_message=text,
                        provider_limit=int(m.group("limit")),
                        shape=rec.shape,
                        recognizer=rec.id,
                    )
        return None

    # 1 — STRUCTURED: the provider named the field.
    if param is not None:
        if _is_non_setting_param(param):
            return None
        shape = _CODE_SHAPES.get(code or "", None) or _shape_from_message(text, "invalid_value")
        return SettingRejection(
            provider=key,
            provider_param=param,
            provider_code=code,
            provider_type=ptype,
            provider_message=text,
            provider_limit=_parse_limit(text),
            shape=shape,
            recognizer="structured",
        )

    # 2 — MESSAGE SHAPES: this provider's rows first, then everyone's (Together
    # and Cerebras reach here through the OpenAI classifier).
    candidates = [_unwrap_google_message(text), _unwrap_google_message(message)]
    ordered = sorted(RECOGNIZERS, key=lambda r: 0 if key in r.providers else 1)
    for rec in ordered:
        for candidate in candidates:
            m = rec.pattern.search(candidate)
            if not m:
                continue
            groups = m.groupdict()
            found_param = groups.get("param") or groups.get("bare") or rec.param
            if found_param and _is_non_setting_param(found_param):
                return None
            limit = groups.get("limit")
            if limit is not None and str(limit).isdigit():
                limit = int(limit)
            if limit is None and rec.shape != "opaque":
                limit = _parse_limit(candidate)
            return SettingRejection(
                provider=key,
                provider_param=found_param,
                provider_code=code,
                provider_type=ptype,
                provider_message=candidate,
                provider_limit=limit,
                shape=rec.shape,
                recognizer=rec.id,
            )
    return None


# ── the person's sentence ────────────────────────────────────────────────────

#: The error-state slot budget (common-docs/policies/interface-text-is-layout.md).
USER_MESSAGE_BUDGET = 140


def _setting_label(param: str | None) -> str | None:
    if not param:
        return None
    leaf = param.split(".")[-1].replace("_", " ").strip()
    return leaf or None


def user_message_for(display_name: str | None, rejection: SettingRejection) -> str:
    """What happened + what to do, inside the 140-character error slot.

    Never the provider's raw sentence: that names wire fields and limits the
    person cannot act on; it stays in the record.
    """
    who = display_name or "The AI provider"
    label = _setting_label(rejection.provider_param)
    if label and len(label) <= 32:
        head = f"{who} rejected the {label} setting for this model."
    else:
        head = f"{who} rejected a setting for this model."
    text = f"{head} Reported for a fix; try another model."
    if len(text) > USER_MESSAGE_BUDGET:
        text = f"{head} Reported for a fix."
    return text[:USER_MESSAGE_BUDGET]


# ── the record (K10) ─────────────────────────────────────────────────────────


def attach_wire_payload(exc: BaseException, payload: Any) -> None:
    """Media adapters: remember what was sent, for the K10 ``sent_value``. Never raises."""
    try:
        if getattr(exc, _WIRE_ATTR, None) is None:
            setattr(exc, _WIRE_ATTR, payload)
    except Exception:  # noqa: BLE001
        pass


def attached_wire_payload(exc: BaseException) -> Any:
    return getattr(exc, _WIRE_ATTR, None)


_MISSING = object()


def _as_mapping(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        try:
            out = dump(exclude_none=True)
            return out if isinstance(out, dict) else None
        except Exception:  # noqa: BLE001
            return None
    if hasattr(value, "__dict__") and not isinstance(value, type):
        try:
            return {k: v for k, v in vars(value).items() if not k.startswith("_")}
        except TypeError:
            return None
    return None


def find_wire_value(payload: Any, param: str | None, *, _depth: int = 0) -> Any:
    """The value sent at ``param`` (dotted path, or a leaf anywhere ≤4 levels deep)."""
    if not param or payload is None or _depth > 4:
        return _MISSING
    mapping = _as_mapping(payload)
    if mapping is None:
        return _MISSING
    if "." in param and _depth == 0:
        cur: Any = mapping
        for part in param.split("."):
            m = _as_mapping(cur)
            if m is None or part not in m:
                cur = _MISSING
                break
            cur = m[part]
        if cur is not _MISSING:
            return cur
    leaf = param.split(".")[-1]
    if leaf in mapping:
        return mapping[leaf]
    for key, child in mapping.items():
        if key in ("messages", "contents", "input", "tools", "system"):
            continue
        if isinstance(child, (dict, list)) or _as_mapping(child) is not None:
            if isinstance(child, list):
                continue
            found = find_wire_value(child, leaf, _depth=_depth + 1)
            if found is not _MISSING:
                return found
    return _MISSING


def _json_scalar(value: Any) -> Any:
    """A record-safe copy of a sent value: scalars kept, anything else summarized."""
    if value is _MISSING:
        return None
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value if len(value) <= 200 else f"{value[:200]}…(+{len(value) - 200} chars)"
    if isinstance(value, (list, tuple, dict)):
        try:
            text = json.dumps(value, default=str)
        except Exception:  # noqa: BLE001
            text = str(value)
        return text if len(text) <= 200 else f"<{type(value).__name__} len={len(value)}>"
    return f"<{type(value).__name__}>"


def _emits_natively(rule: Any) -> bool:
    """Can this rule put its key on the wire? A declared drop never does, and
    ``supported: false`` means "not native here" (K6) — neither produced a field
    the provider then refused."""
    return not (getattr(rule, "drop", None) or getattr(rule, "supported", True) is False)


def canonical_key_for(provider_param: str | None, controls: Any) -> str | None:
    """The canonical setting whose control rule produced ``provider_param``.

    A rule that RENAMES onto the field (``provider_key``) outranks a rule whose
    own name merely equals it, and a rule that cannot emit is never the
    producer: on Groq the legacy key ``max_completion_tokens`` is a declared
    drop while ``max_output_tokens`` carries ``provider_key:
    max_completion_tokens`` — the record must name the second (R3 lane, from I2).
    """
    if not provider_param:
        return None
    rules = getattr(controls, "rules", None) or {}
    leaf = provider_param.split(".")[-1]
    renamed: list[str] = []
    same_name: list[str] = []
    for key, rule in rules.items():
        if not _emits_natively(rule):
            continue
        explicit = getattr(rule, "provider_key", None)
        wire = explicit or key
        if wire == provider_param or wire.split(".")[-1] == leaf:
            (renamed if explicit else same_name).append(key)
    if renamed or same_name:
        return (renamed or same_name)[0]
    for name in (provider_param, leaf):
        if name in rules and _emits_natively(rules[name]):
            return name
    return None


def canonical_state(value: Any) -> str:
    """K10 three states: ``unset`` | ``off`` | ``value``."""
    if value is None or value is _MISSING:
        return "unset"
    if value is False or (isinstance(value, str) and value.strip().lower() in {"off", "none", "disabled"}):
        return "off"
    return "value"


def fingerprint(
    *,
    provider: str,
    model_or_profile: str | None,
    provider_param: str | None,
    canonical_key: str | None,
    shape: str,
    message_signature: str | None = None,
) -> str:
    """Stable identity of ONE defect: same model, same field, same refusal → same print.

    ``message_signature`` (the safety net's unrecognised rejections only, which
    name no field) tells two different refusals on one model apart; it is left
    out of the basis when absent so every existing print stays stable.
    """
    parts = [provider, model_or_profile or "", provider_param or "", canonical_key or "", shape]
    if message_signature:
        parts.append(message_signature)
    basis = json.dumps(parts, separators=(",", ":"))
    return hashlib.sha256(basis.encode()).hexdigest()[:32]


# Last PASSING wire shape per (provider, model), in this process. Cheap: top-level
# and one level of nested scalars only, never content. Feeds ``suspect_params``
# for an opaque rejection. Empty after a deploy — the record says so.
_PASSING_MEMORY_MAX = 512
_passing_wire: dict[tuple[str, str], dict[str, Any]] = {}
_CONTENT_KEYS = frozenset({"messages", "contents", "input", "tools", "system", "system_instruction", "prompt"})


def _flat_scalars(payload: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    mapping = _as_mapping(payload)
    if mapping is None:
        return out
    for key, value in mapping.items():
        if key in _CONTENT_KEYS:
            continue
        nested = _as_mapping(value) if not isinstance(value, (str, bytes, list, tuple)) else None
        if nested is not None:
            for sub, sub_value in nested.items():
                if sub in _CONTENT_KEYS or isinstance(sub_value, (dict, list, tuple)):
                    continue
                out[f"{key}.{sub}"] = _json_scalar(sub_value)
        elif not isinstance(value, (list, tuple, bytes)):
            out[key] = _json_scalar(value)
    return out


def remember_passing_wire(provider: str, model: str | None, payload: Any) -> None:
    """Record the wire shape of a call the provider ACCEPTED. Never raises."""
    if not model or payload is None:
        return
    try:
        if len(_passing_wire) >= _PASSING_MEMORY_MAX:
            _passing_wire.clear()
        _passing_wire[(provider_key(provider), str(model))] = _flat_scalars(payload)
    except Exception:  # noqa: BLE001
        pass


def reset_passing_memory() -> None:
    """Forget remembered passing calls. For tests only."""
    _passing_wire.clear()


def suspect_params(provider: str, model: str | None, failed_payload: Any) -> tuple[list[str], str]:
    """Wire keys that differ from the last passing call for the same model.

    Returns (keys, source): source is ``last_passing_in_process`` when compared,
    ``no_passing_call_in_process`` / ``no_wire_payload`` when it could not be —
    an empty list is then announced, never implied to mean "nothing differs".
    """
    if failed_payload is None:
        return [], "no_wire_payload"
    passing = _passing_wire.get((provider_key(provider), str(model or "")))
    if passing is None:
        return [], "no_passing_call_in_process"
    failed = _flat_scalars(failed_payload)
    keys = sorted(k for k in set(failed) | set(passing) if failed.get(k, _MISSING) != passing.get(k, _MISSING))
    return keys, "last_passing_in_process"


#: Wire keys that are the request itself, never a setting: content, tools, the
#: answer contract, identity and transport. Everything else on the wire is a
#: setting a provider may refuse.
_STRUCTURAL_WIRE_KEYS = frozenset(
    {
        *_CONTENT_KEYS,
        "model",
        "stream",
        "stream_options",
        "tool_choice",
        "parallel_tool_calls",
        "response_format",
        "text.format",
        "response_mime_type",
        "response_schema",
        "response_json_schema",
        "user",
        "metadata",
        "store",
        "prompt_cache_key",
        "previous_response_id",
        "safety_identifier",
        "cached_content",
        "system_instruction",
        "tool_config",
    }
)


def setting_keys_sent(wire_payload: Any, canonical: dict[str, Any] | None = None) -> tuple[list[str], str]:
    """Every non-structural SETTING key the failed call carried.

    From the captured wire body when there is one (top level + one nested level,
    content skipped), else the canonical settings of the config. Returns
    ``(keys, source)``; never raises.
    """
    try:
        flat = _flat_scalars(wire_payload) if wire_payload is not None else {}
        mapping = _as_mapping(wire_payload) or {}
        for key, value in mapping.items():  # list settings (stop) are not scalars
            if isinstance(value, (list, tuple)) and key not in _CONTENT_KEYS:
                flat[key] = True
        keys = sorted(
            k
            for k, v in flat.items()
            if v is not None and k not in _STRUCTURAL_WIRE_KEYS and k.split(".")[0] not in _STRUCTURAL_WIRE_KEYS
        )
        if keys:
            return keys, "setting_keys_on_wire"
        keys = sorted(k for k in (canonical or {}) if not k.startswith("_") and k != "response_format")
        return keys, ("canonical_settings" if keys else "no_settings_found")
    except Exception:  # noqa: BLE001
        return [], "no_settings_found"


def _first_present(lookup: Any, *models: Any) -> Any:
    """``lookup(model)`` for the first spelling that answers (None if none does)."""
    for model in models:
        if model:
            found = lookup(model)
            if found is not None:
                return found
    return None


def _producing_adjustment(adjustments: Any, canonical_key: str | None) -> Any:
    """The CONVERSION Adjustment that produced ``canonical_key``'s value — a
    number -> scale bridge or a K7 family conversion (``converted_from`` set).
    A key the caller set directly needs none: the config already has it."""
    if not canonical_key or not adjustments:
        return None
    for adj in adjustments:
        if (
            getattr(adj, "key", None) == canonical_key
            and getattr(adj, "converted_from", None)
            and getattr(adj, "sent_value", None) is not None
        ):
            return adj
    return None


def build_record(
    info: Any,
    *,
    model: str | None = None,
    profile: Any = None,
    config: Any = None,
    wire_payload: Any = None,
    request_snapshot_id: str | None = None,
    modality: str | None = None,
    adjustments: Any = None,
) -> dict[str, Any]:
    """The K10 payload for a classified ``invalid_setting`` failure. Never raises."""
    details = getattr(info, "details", None) or {}
    rej = details.get("setting_rejection") or {}
    provider = str(rej.get("provider") or details.get("provider") or "unknown")
    provider_param = rej.get("provider_param")
    controls = getattr(profile, "controls", None)
    canonical_key = canonical_key_for(provider_param, controls)

    canonical: dict[str, Any] = {}
    if config is not None:
        try:
            from matrx_ai.catalog.canonicalize import canonical_settings_from_config

            canonical = canonical_settings_from_config(config) or {}
        except Exception:  # noqa: BLE001
            canonical = {}
        if canonical_key is None and provider_param:
            leaf = provider_param.split(".")[-1]
            if leaf in canonical:
                canonical_key = leaf
    canonical_value = canonical.get(canonical_key) if canonical_key else None

    # K9 PROVENANCE for the rejected wire key: the Adjustment that produced the
    # value ``canonical_key`` carried into its rule. Since C5 a budget-only
    # config carries no canonical reasoning_effort of its own (the target
    # converts the number), and since C6 a value may arrive CONVERTED from a
    # family sibling — the config alone cannot say what was sent. The
    # Adjustments (passed in, else the last outbound pass for this model in
    # this context) can.
    if adjustments is None:
        try:
            from matrx_ai.providers.outbound_params import last_outbound_adjustments

            # The outbound pass remembers ``config.model`` — a model NAME on a
            # chat turn, a model UUID on a probe — so try every spelling.
            adjustments = _first_present(
                last_outbound_adjustments,
                getattr(profile, "model_name", None),
                model,
                getattr(config, "model", None),
            )
        except Exception:  # noqa: BLE001
            adjustments = None
    converted_from: dict[str, Any] | None = None
    canonical_source = "config" if canonical_key and canonical_key in canonical else None
    produced = _producing_adjustment(adjustments, canonical_key)
    if produced is not None:
        canonical_value = getattr(produced, "sent_value", None)
        canonical_source = f"adjustment:{getattr(produced, 'provenance', 'declared')}"
        source_key = getattr(produced, "converted_from", None)
        if source_key:
            converted_from = {
                "key": source_key,
                "value": _json_scalar(getattr(produced, "canonical_value", None)),
            }

    model_name = getattr(profile, "model_name", None) or model
    profile_id = getattr(profile, "settings_profile_id", None) or getattr(profile, "profile_id", None)

    # WHAT WAS SENT. The captured wire body when the call ran inside an
    # orchestrated turn; otherwise (a probe, a bare dispatch, a media seam
    # without kwargs) the params the outbound pass produced for this call —
    # exactly what the translator merged into the request — and last the
    # producing Adjustment's ``sent_value``.
    sent = find_wire_value(wire_payload, provider_param)
    sent_source: str | None = "wire_payload" if sent is not _MISSING else None
    if sent is _MISSING:
        try:
            from matrx_ai.providers.outbound_params import last_outbound_params

            outbound = _first_present(
                last_outbound_params, model_name, model, getattr(config, "model", None)
            )
            sent = find_wire_value(outbound, provider_param)
            sent_source = "outbound_pass" if sent is not _MISSING else None
        except Exception:  # noqa: BLE001
            sent = _MISSING
    if sent is _MISSING and canonical_key:
        for adj in adjustments or []:
            if getattr(adj, "key", None) == canonical_key and getattr(adj, "sent_value", None) is not None:
                sent, sent_source = adj.sent_value, "adjustment"
                break

    # K9 provenance: the cell that produced the wire value — the compiled
    # controls' CellRef for the key (id AND version, from the K5 view), else a
    # carried Adjustment's ``cell_id``. ``None`` while rules come from the
    # legacy columns (copy mode).
    cell_id = cell_version = None
    ref = (getattr(controls, "cells", None) or {}).get(canonical_key) if canonical_key else None
    if ref is not None:
        cell_id = getattr(ref, "cell_id", None)
        cell_version = getattr(ref, "version", None)
    rule = (getattr(controls, "rules", None) or {}).get(canonical_key) if canonical_key else None
    for source in [*(adjustments or []), rule]:
        if source is None:
            continue
        if getattr(source, "key", canonical_key) not in (canonical_key, None) and source is not rule:
            continue
        cell_id = cell_id or getattr(source, "cell_id", None)
        cell_version = cell_version or getattr(source, "cell_version", None)

    suspects: list[str] = []
    suspect_source = "not_opaque"
    if rej.get("opaque"):
        suspects, suspect_source = suspect_params(provider, model_name, wire_payload)
        if not suspects:
            # No passing call to compare against: EVERY setting the call carried
            # is a suspect (the fixer narrows it), never an empty list.
            suspects, suspect_source = setting_keys_sent(wire_payload, canonical)

    return {
        "provider": provider,
        "offering_id": getattr(profile, "offering_id", None),
        "model_id": getattr(profile, "model_id", None),
        "model_name": model_name,
        "profile_id": profile_id,
        "modality": modality,
        "provider_param": provider_param,
        "provider_code": rej.get("provider_code"),
        "provider_type": rej.get("provider_type"),
        "provider_message": rej.get("provider_message") or getattr(info, "message", None),
        "sent_value": _json_scalar(sent),
        "sent_value_found": sent is not _MISSING,
        "sent_value_source": sent_source,
        "canonical_key": canonical_key,
        "canonical_value": _json_scalar(canonical_value),
        "canonical_state": canonical_state(canonical_value) if canonical_key else None,
        "canonical_source": canonical_source,
        "converted_from": converted_from,
        "provider_limit": rej.get("provider_limit"),
        "request_snapshot_id": request_snapshot_id,
        "cell_id": cell_id,
        "cell_version": cell_version,
        "fingerprint": fingerprint(
            provider=provider,
            model_or_profile=str(profile_id or model_name or ""),
            provider_param=provider_param,
            canonical_key=canonical_key,
            shape=str(rej.get("shape") or ""),
            message_signature=rej.get("message_signature"),
        ),
        "suspect_params": suspects,
        "suspect_params_source": suspect_source,
        "shape": rej.get("shape"),
        "recognizer": rej.get("recognizer"),
        "status_code": getattr(info, "status_code", None),
        "lifecycle": "new",
    }


# ── R2: in-line self-heal (settings-translation PLAN R2) ─────────────────────
#
# A CLASSIFIED settings rejection that names its field is repaired ONCE,
# mechanically, and the call is sent again — the person's request goes through
# (GROUND-TRUTH: "My request should go through"). Three repairs only:
#
#   * a stated / sourced LIMIT       -> clamp to it            (action "clamped")
#   * a value the model does not take -> nearest accepted value (action "mapped")
#   * a parameter the model refuses   -> drop it               (action "dropped")
#   * a refused value, accepted set unknown -> drop it; the model default
#     applies (action "dropped", source "accepted_values_unknown" — ruling)
#
# The repair is applied to the per-call WIRE config (UnifiedAIClient builds a
# shallow copy per dispatch), never to the person's saved config. It is recorded
# as a K9 Adjustment with provenance ``computed`` so the stream warning and the
# K10 record say the same thing. Everything that is not one of those three —
# an opaque rejection, an unknown accepted set, a value that did not come from
# the config — is NOT retried and the record names why. The retry itself lives
# at the shared dispatch seam (``UnifiedAIClient._dispatch_with_billing_net``),
# one attempt kind beside the transient retry.

#: Repairs per provider call. ONE. A second rejection is the person's honest error.
REPAIRS_PER_CALL = 1

#: K10 payload key carrying the R2 outcome.
SELF_HEALED_KEY = "self_healed"

_CLAMP_SHAPES = frozenset({"above_max", "string_too_long", "too_many_items"})
# A LIST item the provider refuses (Anthropic: a whitespace-only stop sequence).
_ITEM_SHAPES = frozenset({"invalid_item"})
_DROP_SHAPES = frozenset({"deprecated", "unsupported", "mode_unsupported", "combination"})
_MAP_SHAPES = frozenset({"invalid_value"})

# Canonical key -> UnifiedConfig attribute, where they differ.
_CONFIG_ATTR = {"quality": "render_quality"}

# Canonical key -> I1 provider fact (ai.provider.provider_models_cache.parameter_facts).
_LIMIT_FACTS = {"max_output_tokens": "output_max", "thinking_budget": "reasoning.budget_max"}
_ACCEPTED_FACTS = {
    "reasoning_effort": "reasoning.efforts",
    "resolution": "media.resolutions",
    "aspect_ratio": "media.aspect_ratios",
    "duration_seconds": "media.durations_seconds",
    "fps": "media.fps",
}

#: Host seam: ``async (profile) -> {fact: value} | None`` — the winning I1 facts
#: for the profile's offering. Registered by the host in ``matrx_ai.configure``.
PARAMETER_FACTS_EXT = "provider_parameter_facts"

_ALLOWED_INTRO = re.compile(
    r"(?:supported values(?: are)?|allowed values(?: are)?|valid values(?: are)?|"
    r"expected one of|must be one of|one of)\s*:?\s*(?P<rest>.+)",
    re.IGNORECASE,
)
_QUOTED = re.compile(r"[\'\"`]([^\'\"`]+)[\'\"`]")

_LABELS = {
    "max_output_tokens": "Output limit",
    "thinking_budget": "Thinking budget",
    "reasoning_effort": "Reasoning effort",
    "top_p": "Top P",
    "top_k": "Top K",
    "duration_seconds": "Duration",
    "aspect_ratio": "Aspect ratio",
    "stop_sequences": "Stop sequences",
}

#: Secondary-text slot budget for the stream warning (interface-text-is-layout).
REPAIR_WARNING_BUDGET = 60


@dataclass(frozen=True)
class SettingRepair:
    """One mechanical repair of the setting a provider refused."""

    canonical_key: str
    config_attr: str
    provider_param: str
    action: str  # clamped | mapped | dropped
    old_value: Any
    new_value: Any
    source: str  # provider_message | provider_facts | allowed_values | shape
    shape: str

    def adjustment(self) -> Any:
        """The K9 Adjustment — provenance ``computed``: the engine decided, no cell did."""
        from matrx_ai.catalog.models import Adjustment

        return Adjustment(
            key=self.canonical_key,
            action=self.action,  # type: ignore[arg-type]
            canonical_value=self.old_value,
            sent_value=self.new_value,
            reason=(
                f"provider rejected {self.provider_param} ({self.shape}); "
                f"repaired from {self.source} and sent once more"
            ),
            expected=True,
            provenance="computed",
        )

    def as_record(self) -> dict[str, Any]:
        return {
            "canonical_key": self.canonical_key,
            "provider_param": self.provider_param,
            "action": self.action,
            "from": _json_scalar(self.old_value),
            "to": _json_scalar(self.new_value),
            "source": self.source,
            "shape": self.shape,
            "adjustment": self.adjustment().model_dump(mode="json"),
        }


@dataclass(frozen=True)
class RepairPlan:
    repair: SettingRepair | None
    reason: str  # "repairable" or why not


def _no(reason: str) -> RepairPlan:
    return RepairPlan(None, reason)


def _coerce(token: str) -> Any:
    t = token.strip()
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    if re.fullmatch(r"-?\d+\.\d+", t):
        return float(t)
    return t


def parse_allowed_values(message: str | None) -> list[Any] | None:
    """Values the provider's own sentence says it accepts, or None."""
    if not message:
        return None
    m = _ALLOWED_INTRO.search(message)
    if not m:
        return None
    rest = m.group("rest")
    quoted = _QUOTED.findall(rest)
    if quoted:
        return [_coerce(q) for q in quoted]
    bracket = re.search(r"\[([^\]]+)\]", rest)
    if bracket:
        return [_coerce(t) for t in bracket.group(1).split(",") if t.strip()]
    return None


def _fact(facts: dict[str, Any] | None, name: str | None) -> Any:
    if not facts or not name:
        return None
    value = facts.get(name)
    if isinstance(value, dict) and "value" in value:
        value = value["value"]
    return value


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def plan_setting_repair(
    info: Any,
    *,
    profile: Any,
    config: Any,
    facts: dict[str, Any] | None = None,
) -> RepairPlan:
    """Decide the ONE mechanical repair for a classified settings rejection. Pure; never raises."""
    try:
        return _plan(info, profile=profile, config=config, facts=facts)
    except Exception as exc:  # noqa: BLE001 — a planning bug is "not repairable", never a crash
        return _no(f"planner_error:{type(exc).__name__}")


def _plan(info: Any, *, profile: Any, config: Any, facts: dict[str, Any] | None) -> RepairPlan:
    if getattr(info, "error_type", None) != SETTING_REJECTION_ERROR_TYPE:
        return _no("not_a_settings_rejection")
    rej = (getattr(info, "details", None) or {}).get("setting_rejection") or {}
    param = rej.get("provider_param")
    shape = str(rej.get("shape") or "")
    if not param or rej.get("opaque"):
        return _no("opaque_rejection")
    if config is None:
        return _no("no_wire_config")
    key = canonical_key_for(param, getattr(profile, "controls", None))
    if key is None:
        leaf = param.split(".")[-1]
        attr_guess = _CONFIG_ATTR.get(leaf, leaf)
        if hasattr(config, attr_guess):
            key = leaf
    if key is None:
        return _no("no_canonical_key")
    attr = _CONFIG_ATTR.get(key, key)
    if not hasattr(config, attr):
        return _no("not_a_config_setting")
    current = getattr(config, attr)
    if current is None:
        return _no("value_not_from_config")

    def repair(action: str, new: Any, source: str) -> RepairPlan:
        return RepairPlan(
            SettingRepair(
                canonical_key=key,
                config_attr=attr,
                provider_param=param,
                action=action,
                old_value=current,
                new_value=new,
                source=source,
                shape=shape,
            ),
            "repairable",
        )

    if shape in _CLAMP_SHAPES:
        limit, source = rej.get("provider_limit"), "provider_message"
        if not _is_number(limit):
            limit, source = _fact(facts, _LIMIT_FACTS.get(key)), "provider_facts"
        if not _is_number(limit):
            return _no("no_stated_limit")
        if _is_number(current) and current > limit:
            return repair("clamped", int(limit) if isinstance(current, int) else limit, source)
        if isinstance(current, str) and len(current) > int(limit):
            return repair("clamped", current[: int(limit)], source)
        if isinstance(current, list | tuple) and len(current) > int(limit):
            return repair("clamped", list(current)[: int(limit)], source)
        return _no("value_within_stated_limit")

    if shape in _ITEM_SHAPES:
        if not isinstance(current, list | tuple):
            return _no("not_a_list_setting")
        kept = [item for item in current if not (isinstance(item, str) and not item.strip())]
        if not kept:
            return repair("dropped", None, "shape")
        if len(kept) < len(current):
            return repair("clamped", kept, "provider_message")
        # The provider named an item rule we cannot apply mechanically: leave the
        # setting out (the R3 ruling for an unknown accepted set).
        return repair("dropped", None, "accepted_values_unknown")

    if shape in _DROP_SHAPES:
        return repair("dropped", None, "shape")

    if shape in _MAP_SHAPES:
        accepted, source = parse_allowed_values(rej.get("provider_message")), "allowed_values"
        if not accepted:
            fact = _fact(facts, _ACCEPTED_FACTS.get(key))
            accepted = list(fact) if isinstance(fact, list | tuple) else None
            source = "provider_facts"
        if not accepted:
            # Ruling (settings-translation REGISTER, R3 lane): the provider refused
            # the VALUE and neither its message nor the I1 facts say what it takes.
            # Guessing a value is a second rejection waiting to happen; the honest
            # repair is to leave the setting out so the model's own default applies
            # — warned, recorded, and the request goes through.
            return repair("dropped", None, "accepted_values_unknown")
        controls = getattr(profile, "controls", None)
        nearest_fn = getattr(controls, "_nearest_accepted", None)
        if callable(nearest_fn):
            new = nearest_fn(key, current, accepted)
        else:
            from matrx_ai.catalog.equivalence import nearest_accepted

            new = nearest_accepted(key, current, accepted)
        if new is None or new == current:
            return _no("no_nearest_accepted")
        return repair("mapped", new, source)

    return _no(f"shape_not_repairable:{shape or 'unknown'}")


def apply_setting_repair(config: Any, repair: SettingRepair) -> bool:
    """Write the repair onto the per-call wire config; prove the canonical pass reads it.

    Returns False (and restores the old value) when the config cannot express the
    repair — e.g. a drop that another field would re-derive. Never raises.
    """
    try:
        setattr(config, repair.config_attr, repair.new_value)
        from matrx_ai.catalog.canonicalize import canonical_settings_from_config

        canonical = canonical_settings_from_config(config)
        if repair.action == "dropped":
            ok = repair.canonical_key not in canonical
        else:
            ok = canonical.get(repair.canonical_key) == repair.new_value
        if not ok:
            setattr(config, repair.config_attr, repair.old_value)
        return ok
    except Exception:  # noqa: BLE001
        try:
            setattr(config, repair.config_attr, repair.old_value)
        except Exception:  # noqa: BLE001
            pass
        return False


def _label(key: str) -> str:
    return _LABELS.get(key) or key.replace("_", " ").capitalize()


def _value_text(value: Any) -> str:
    if _is_number(value) and not isinstance(value, float):
        return f"{value:,}"
    return str(value)


def repair_user_message(repair: SettingRepair) -> str:
    """One label-length sentence (≤ REPAIR_WARNING_BUDGET) for the stream warning."""
    label = _label(repair.canonical_key)
    if repair.action == "clamped" and _is_number(repair.new_value):
        text = f"{label} lowered to {_value_text(repair.new_value)} for this model."
    elif repair.action == "clamped":
        text = f"{label} shortened to fit this model."
    elif repair.action == "mapped":
        text = f"{label} set to {_value_text(repair.new_value)} for this model."
    elif repair.source == "accepted_values_unknown":
        text = f"{label} reset to the model default."
    else:
        text = f"{label} left out; this model doesn't accept it."
    if len(text) > REPAIR_WARNING_BUDGET:
        text = "A setting was adjusted to fit this model."
    return text


def repair_warning(repair: SettingRepair, *, provider: str, model: Any) -> Any:
    """The ``warning`` event for the existing client-warning door."""
    from matrx_connect.context.events import WarningPayload

    return WarningPayload(
        code="setting_repaired",
        system_message=(
            f"{provider} rejected {repair.provider_param} ({repair.shape}); sent once more with "
            f"{repair.canonical_key} {repair.action} {repair.old_value!r} -> {repair.new_value!r} "
            f"(source: {repair.source})."
        ),
        user_message=repair_user_message(repair),
        level="low",
        recoverable=True,
        metadata={"model": str(model), "repair": repair.as_record()},
    )


# ── NET: the universal safety net (settings-translation lane NET) ────────────
#
# R1/R2 understand only rejection messages someone already catalogued. Every NEW
# settings rejection (live 2026-10-04: Groq temperature 5, xAI ``stop``, Gemini
# 2.5 Pro thinking budget) landed as ``provider_request_failed`` with no
# fingerprint and no answer. The net closes the class at the shared dispatch
# seam: ANY provider 400/422 on a call that carried settings —
#
#   (a) is filed as a typed ``<provider>.invalid_setting`` candidate (K10, shape
#       ``unrecognized``, recognizer ``safety_net``) with ``suspect_params`` and a
#       fingerprint, so the fixer (R3) sees it;
#   (b) is sent ONCE more pre-stream: the specific repair when a recognizer
#       understood the message (R2), else the SAFE MINIMUM request — every
#       optional sampling / reasoning / list setting the person set is left out;
#       messages, tools, response format, model and output limit stay — with one
#       warning naming what was left out;
#   (c) never loops and never touches billing, auth, content or schema errors.

#: Error classes the net may treat as a settings candidate. Everything else
#: (auth, permission, billing, context length, content filter, not found, rate
#: limits, server errors) has its own class and is never retried by the net.
NET_ERROR_TYPES = frozenset({"invalid_request", "unprocessable_request"})
NET_STATUS_CODES = frozenset({400, 422})
NET_SHAPE = "unrecognized"
NET_RECOGNIZER = "safety_net"

#: A 400 that is about the CONTENT or the SCHEMA, not a setting. Leaving
#: settings out cannot fix these, so the net neither files nor retries them.
_NET_NOT_A_SETTING = _rx(
    r"\b(?:messages?|contents?|prompt|input|image|images|file|files|audio|video|document|pdf|"
    r"tools?|functions?|tool_use|tool_result|function_call|response_format|json_schema|schema|"
    r"context(?:_| )length|context window|too many tokens|token limit|safety|moderation|policy|"
    r"api key|credit|billing|quota|balance)\b"
)

#: UnifiedConfig attribute -> (canonical key, value meaning "not set").
#: The SAFE MINIMUM leaves every one of these out. Kept: model, messages,
#: tools, tool_choice, response_format, max_output_tokens, media knobs.
SAFE_MINIMUM_ATTRS: dict[str, tuple[str, Any]] = {
    "temperature": ("temperature", None),
    "top_p": ("top_p", None),
    "top_k": ("top_k", None),
    "seed": ("seed", None),
    "frequency_penalty": ("frequency_penalty", None),
    "presence_penalty": ("presence_penalty", None),
    "verbosity": ("verbosity", None),
    "stop_sequences": ("stop_sequences", []),
    "reasoning_effort": ("reasoning_effort", None),
    "disable_reasoning": ("reasoning_effort", None),
    "thinking_budget": ("thinking_budget", None),
    "thinking_level": ("thinking_level", None),
    "reasoning_summary": ("reasoning_summary", None),
    "include_thoughts": ("include_thoughts", None),
    "clear_thinking": ("clear_thinking", None),
}

SAFE_MINIMUM_SOURCE = "safe_minimum"


def _message_signature(message: str) -> str:
    """The refusal's wording with numbers and quoted values blanked, for the print."""
    text = _unwrap_google_message(message or "")
    text = re.sub(r"\d+(?:\.\d+)?", "#", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text[:120]


def net_candidate(info: Any) -> Any:
    """An UNRECOGNISED 400/422 → a typed ``invalid_setting`` candidate, else None.

    Pure; never raises. Returns a new ``RetryableError`` (the original is left
    as it is) whose ``details["setting_rejection"]`` is an opaque rejection with
    shape ``unrecognized`` — so the K10 record, the dedupe and the fixer treat
    it like any other settings rejection.
    """
    try:
        from matrx_ai.providers.errors import RetryableError, is_billing_refusal

        if info is None or getattr(info, "error_type", None) not in NET_ERROR_TYPES:
            return None
        if getattr(info, "status_code", None) not in NET_STATUS_CODES:
            return None
        details = dict(getattr(info, "details", None) or {})
        message = str(details.get("message") or getattr(info, "message", "") or "")
        full = f"{getattr(info, 'message', '')} {message}"
        if is_billing_refusal(full):
            return None
        param = details.get("param")
        if param not in (None, "") and _is_non_setting_param(str(param)):
            return None
        code = details.get("code")
        if code not in (None, "") and str(code) in _NON_SETTING_CODES:
            return None
        inner = _unwrap_google_message(message or str(getattr(info, "message", "")))
        if _NET_NOT_A_SETTING.search(inner):
            return None
        provider = provider_key(str(details.get("provider") or ""))
        rejection = SettingRejection(
            provider=provider,
            provider_param=None,
            provider_code=str(code) if code not in (None, "") else None,
            provider_type=str(details.get("type")) if details.get("type") else None,
            provider_message=inner[:2000],
            provider_limit=None,
            shape=NET_SHAPE,
            recognizer=NET_RECOGNIZER,
        )
        rej = rejection.as_details()
        rej["message_signature"] = _message_signature(inner)
        return RetryableError(
            error_type=SETTING_REJECTION_ERROR_TYPE,
            message=getattr(info, "message", "") or inner,
            status_code=getattr(info, "status_code", None),
            is_retryable=False,
            user_message=getattr(info, "user_message", "") or inner,
            details={**details, "provider": provider, "setting_rejection": rej},
        )
    except Exception:  # noqa: BLE001
        return None


@dataclass(frozen=True)
class SafeMinimum:
    """The safe-minimum retry: every optional setting the person set, left out."""

    dropped: tuple[tuple[str, Any], ...]  # (config attr, value as sent)
    provider_message: str

    @property
    def canonical_keys(self) -> list[str]:
        seen: list[str] = []
        for attr, _ in self.dropped:
            key = SAFE_MINIMUM_ATTRS[attr][0]
            if key not in seen:
                seen.append(key)
        return seen

    def adjustments(self) -> list[Any]:
        from matrx_ai.catalog.models import Adjustment

        return [
            Adjustment(
                key=SAFE_MINIMUM_ATTRS[attr][0],
                action="dropped",
                canonical_value=_json_scalar(old),
                sent_value=None,
                reason="provider refused the request (unrecognised settings rejection); sent once more without it",
                expected=True,
                provenance="computed",
            )
            for attr, old in self.dropped
        ]

    def as_record(self) -> dict[str, Any]:
        return {
            "action": "safe_minimum",
            "source": SAFE_MINIMUM_SOURCE,
            "dropped": {attr: _json_scalar(old) for attr, old in self.dropped},
            "canonical_keys": self.canonical_keys,
            "adjustments": [a.model_dump(mode="json") for a in self.adjustments()],
        }


def plan_safe_minimum(config: Any, *, provider_message: str = "") -> SafeMinimum | None:
    """Which optional settings the config carries (None = nothing to leave out)."""
    if config is None:
        return None
    dropped: list[tuple[str, Any]] = []
    for attr, (_, unset) in SAFE_MINIMUM_ATTRS.items():
        if not hasattr(config, attr):
            continue
        value = getattr(config, attr)
        if value is None or value == unset or (isinstance(value, (list, tuple)) and not value):
            continue
        dropped.append((attr, value))
    if not dropped:
        return None
    return SafeMinimum(tuple(dropped), provider_message)


def apply_safe_minimum(config: Any, plan: SafeMinimum) -> bool:
    """Leave every planned setting out of the per-call wire config. Never raises."""
    try:
        for attr, _ in plan.dropped:
            setattr(config, attr, SAFE_MINIMUM_ATTRS[attr][1])
        return True
    except Exception:  # noqa: BLE001
        try:
            for attr, old in plan.dropped:
                setattr(config, attr, old)
        except Exception:  # noqa: BLE001
            pass
        return False


def config_as_sent_before_safe_minimum(config: Any, plan: SafeMinimum) -> Any:
    from copy import copy

    sent = copy(config)
    for attr, old in plan.dropped:
        try:
            setattr(sent, attr, old)
        except Exception:  # noqa: BLE001
            pass
    return sent


def safe_minimum_user_message(plan: SafeMinimum) -> str:
    """One label-length sentence (≤ REPAIR_WARNING_BUDGET) naming what was left out."""
    labels = [_label(k) for k in plan.canonical_keys]
    if len(labels) == 1:
        text = f"{labels[0]} left out; this model refused it."
    else:
        text = f"Left out: {', '.join(labels)}."
    if len(text) > REPAIR_WARNING_BUDGET:
        text = f"{len(labels)} settings left out; this model refused them."
    return text


def safe_minimum_warning(plan: SafeMinimum, *, provider: str, model: Any) -> Any:
    from matrx_connect.context.events import WarningPayload

    return WarningPayload(
        code="setting_repaired",
        system_message=(
            f"{provider} refused the request ({plan.provider_message[:200]}); sent once more with "
            f"only the safe minimum — left out: {', '.join(plan.canonical_keys)}."
        ),
        user_message=safe_minimum_user_message(plan),
        level="low",
        recoverable=True,
        metadata={"model": str(model), "repair": plan.as_record()},
    )


async def load_parameter_facts(profile: Any) -> dict[str, Any] | None:
    """The I1 facts for this offering through the host seam, or None. Never raises."""
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext(PARAMETER_FACTS_EXT):
            return None
        lookup = get_ext(PARAMETER_FACTS_EXT)
        facts = await lookup(profile)
        return facts if isinstance(facts, dict) else None
    except Exception:  # noqa: BLE001
        return None


__all__ = [
    "NET_ERROR_TYPES",
    "NET_SHAPE",
    "SAFE_MINIMUM_ATTRS",
    "SafeMinimum",
    "apply_safe_minimum",
    "net_candidate",
    "plan_safe_minimum",
    "safe_minimum_warning",
    "setting_keys_sent",
    "LIFECYCLE",
    "PARAMETER_FACTS_EXT",
    "REPAIRS_PER_CALL",
    "RepairPlan",
    "SELF_HEALED_KEY",
    "SettingRepair",
    "apply_setting_repair",
    "load_parameter_facts",
    "parse_allowed_values",
    "plan_setting_repair",
    "repair_user_message",
    "repair_warning",
    "PROVIDER_SETTING_REJECTED_KIND",
    "RECOGNIZERS",
    "SETTING_REJECTION_ERROR_TYPE",
    "SettingRejection",
    "attach_wire_payload",
    "attached_wire_payload",
    "build_record",
    "canonical_key_for",
    "find_wire_value",
    "fingerprint",
    "recognize",
    "remember_passing_wire",
    "suspect_params",
    "user_message_for",
]
