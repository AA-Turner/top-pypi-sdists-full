"""A customer's sentence never names a model, a provider or a model id (Arman, 2026-11-18).

2026-11-16 a free-plan customer read "gemini-2.5-pro-preview-tts needs a paid plan". The rule, for every sentence the
server builds for a person (``user_message``, a caller-refusal exception's message):

* it is FIXED TEXT of ours, never a model, provider, ``{exc}``, tool id or HTTP status interpolated in;
* the raw detail rides the developer fields (``RetryableError.message`` / ``details``, the log).

THE LISTS live once, in ``matrx_ai.providers.customer_words``. This file:

* STATIC - walks every ``user_message=`` in the package and fails on a forbidden interpolation or a forbidden word;
* DYNAMIC - sends representative provider errors (every provider, every status class, raw text that names a model
  and a provider) through the real classifiers and every caller-refusal gate, and reads what a person would read;
* SELF-TEST - the detector flags a leaking sentence (the red proof; no tracked source is ever broken to show it).
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

import matrx_ai
from matrx_ai.providers import errors as provider_errors
from matrx_ai.providers.customer_words import PROVIDER_WORDS, names_a_model_or_provider

PACKAGE = Path(matrx_ai.__file__).resolve().parent
LEAK_MODEL = "gemini-2.5-pro-preview-tts"
LEAK_RAW = f"The model {LEAK_MODEL} failed on OpenAI Anthropic Google Groq Moonshot xAI with key sk-abcdef123456"

#: Interpolated names that carry a model, a provider, raw exception text or an internal id into a sentence.
FORBIDDEN_INTERPOLATIONS = {
    "provider", "model", "model_name", "model_id", "model_label", "api_class", "exc", "e", "err", "error",
    "error_str", "detail", "status_code", "tool_id", "table", "vendor", "display",
}

#: ``user_message=`` sites in the package that interpolate one of the names above ON PURPOSE. Each carries why.
STATIC_ALLOWLIST: dict[tuple[str, str], str] = {}


# ── self-test: the detector can fail ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "leak",
    [
        f"{LEAK_MODEL} needs a paid plan.",
        "OpenAI refused this request: the platform's OpenAI account is out of credit.",
        "Together AI rate limit reached.",
        "The selected Anthropic model has been retired.",
        "Moonshot could not complete this request.",
        "gpt-4o can't answer a chat message.",
        "o3-mini is no longer offered.",
        "An unexpected Google error occurred: quota",
    ],
)
def test_the_detector_flags_a_leaking_sentence(leak: str) -> None:
    assert names_a_model_or_provider(leak), leak


@pytest.mark.parametrize(
    "clean",
    [
        "Something went wrong on our side. We have been notified and are fixing it.",
        "This needs a paid plan. Upgrade to use it. Not run.",
        "The service is busy right now.",
        "This model is no longer offered. Pick another model and try again.",
    ],
)
def test_the_detector_passes_a_clean_sentence(clean: str) -> None:
    assert names_a_model_or_provider(clean) is None


def test_a_static_scan_fails_on_a_leaking_template() -> None:
    tree = ast.parse('x = Info(user_message=f"{provider} rejected the request: {detail}")')
    assert _leaks_in(tree, "inline"), "the static scan must flag a provider/detail interpolation"
    assert not _leaks_in(ast.parse('x = Info(user_message="Something went wrong.")'), "inline")


# ── static: every user_message template ─────────────────────────────────────────────────────────────────────────


def _names_in(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)} | {
        n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)
    }


def _literal_text(node: ast.AST) -> str:
    return " ".join(
        part.value for part in ast.walk(node) if isinstance(part, ast.Constant) and isinstance(part.value, str)
    )


def _leaks_in(tree: ast.AST, where: str) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "user_message":
            value = node.value
            if isinstance(value, ast.Name | ast.Attribute | ast.Call | ast.Subscript):
                continue  # a passed-through value is checked where it is built
            interpolated = {
                n for fv in ast.walk(value) if isinstance(fv, ast.FormattedValue) for n in _names_in(fv.value)
            }
            bad = sorted(interpolated & FORBIDDEN_INTERPOLATIONS)
            if bad:
                found.append(f"{where}:{node.value.lineno}: interpolates {bad}")
            word = names_a_model_or_provider(_literal_text(value))
            if word:
                found.append(f"{where}:{node.value.lineno}: names {word!r}")
    return found


def test_no_user_message_template_in_the_package_names_a_model_or_provider() -> None:
    problems: list[str] = []
    for path in sorted(PACKAGE.rglob("*.py")):
        rel = str(path.relative_to(PACKAGE))
        if "/tests/" in str(path) or rel.startswith("providers/customer_words"):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        problems += [p for p in _leaks_in(tree, rel) if (rel, p.split(":")[1]) not in STATIC_ALLOWLIST]
    assert not problems, "customer sentences must be fixed text of ours:\n" + "\n".join(problems)


def _caller_refusal_classes() -> list[tuple[str, ast.ClassDef]]:
    out: list[tuple[str, ast.ClassDef]] = []
    for path in sorted((PACKAGE / "providers").rglob("*.py")) + [PACKAGE / "catalog" / "lifecycle.py"]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and any(
                isinstance(s, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "is_caller_refusal" for t in s.targets)
                for s in node.body
            ):
                out.append((f"{path.relative_to(PACKAGE)}::{node.name}", node))
    return out


def test_every_caller_refusal_sentence_is_fixed_text() -> None:
    """``self.message`` / ``self.user_message`` of a caller-refusal exception: no model/provider/raw interpolation."""
    problems: list[str] = []
    classes = _caller_refusal_classes()
    assert classes, "no caller-refusal class found: the scan is broken"
    for label, cls in classes:
        for node in ast.walk(cls):
            if not isinstance(node, ast.Assign):
                continue
            targets = [t for t in node.targets if isinstance(t, ast.Attribute) and t.attr in {"message", "user_message"}]
            if not targets:
                continue
            interpolated = {
                n for fv in ast.walk(node.value) if isinstance(fv, ast.FormattedValue) for n in _names_in(fv.value)
            }
            bad = sorted(interpolated & (FORBIDDEN_INTERPOLATIONS | {"mandate_key", "model_name"}))
            word = names_a_model_or_provider(_literal_text(node.value))
            if bad or word:
                problems.append(f"{label}:{node.lineno}: interpolates {bad} / names {word!r}")
    assert not problems, "\n".join(problems)


# ── dynamic: the real classifiers ───────────────────────────────────────────────────────────────────────────────


class _WireError(Exception):
    def __init__(self, message: str, status_code: int | None = None, body: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body or {"error": {"type": "x", "message": message}}


PROVIDERS = [
    "openai", "anthropic", "google", "groq", "xai", "together", "cerebras", "moonshot", "elevenlabs",
    "generic_openai", "replicate", "cohere", "huggingface", "fastino", "cartesia", "voyage", "unknown",
]
STATUSES = [None, 400, 401, 402, 403, 404, 408, 409, 413, 422, 425, 429, 451, 500, 502, 503, 504]
RAW_TEXTS = [
    LEAK_RAW,
    f"{LEAK_MODEL} does not match the expected schema (json_validate_failed)",
    "Tool choice is none, but model called a tool",
    f"You exceeded your current quota, no credits remaining for {LEAK_MODEL}",
    f"Your credit balance is too low to access the Anthropic API ({LEAK_MODEL})",
    f"model {LEAK_MODEL} is overloaded",
    f"context length exceeded for {LEAK_MODEL}",
    "voice_not_found",
    f"account is suspended ({LEAK_MODEL})",
]


def test_every_provider_error_translation_speaks_in_fixed_text() -> None:
    problems: list[str] = []
    seen = 0
    for provider in PROVIDERS:
        for status in STATUSES:
            for raw in RAW_TEXTS:
                try:
                    info = provider_errors.classify_provider_error(provider, _WireError(raw, status))
                except Exception:  # noqa: BLE001 - a classifier that raises is not this test's finding
                    continue
                seen += 1
                for field in (info.user_message, info.retrying_message):
                    word = names_a_model_or_provider(field)
                    if word:
                        problems.append(f"{provider}/{status}/{raw[:30]!r}: {field!r} names {word!r}")
    assert seen > 500, f"the matrix barely ran ({seen})"
    assert not problems, "\n".join(sorted(set(problems))[:25])


@pytest.mark.parametrize("provider", ["OpenAI", "Anthropic", "Google", "Groq", "Moonshot", "Together AI", "xAI"])
def test_every_handler_speaks_in_fixed_text(provider: str) -> None:
    infos = [
        provider_errors._handle_auth_error(provider, LEAK_RAW, 401),
        provider_errors._handle_permission_error(provider, LEAK_RAW, 403),
        provider_errors._handle_bad_request(provider, LEAK_RAW, {"message": LEAK_RAW}),
        provider_errors._handle_not_found(provider, LEAK_RAW),
        provider_errors._handle_not_found(provider, "model_archived " + LEAK_RAW),
        provider_errors._handle_request_too_large(provider, LEAK_RAW),
        provider_errors._handle_billing_error(provider, LEAK_RAW, 402),
        provider_errors._handle_unprocessable(provider, LEAK_RAW, {"message": LEAK_RAW}),
        provider_errors._handle_conflict(provider, LEAK_RAW),
        provider_errors._handle_rate_limit(provider, LEAK_RAW, 5.0),
        provider_errors._handle_server_error(provider, LEAK_RAW, 500),
        provider_errors._handle_overloaded(provider, LEAK_RAW, 529),
        provider_errors._handle_timeout(provider, LEAK_RAW),
        provider_errors._handle_connection_error(provider, LEAK_RAW),
        provider_errors._handle_incomplete_response(provider, LEAK_RAW),
        provider_errors._handle_content_filter(provider, LEAK_RAW),
        provider_errors._handle_context_length_exceeded(provider, LEAK_RAW),
        provider_errors._handle_schema_violation(provider, LEAK_RAW),
        provider_errors._handle_unoffered_tool_call(provider, LEAK_RAW),
        provider_errors._classify_unbranched_status(provider, 451, LEAK_RAW),
        provider_errors._classify_unbranched_status(provider, 425, LEAK_RAW),
        provider_errors._fallback_classify(LEAK_RAW, provider),
        provider_errors.classify_internal_error(AttributeError(LEAK_RAW), provider),
    ]
    for info in infos:
        assert info is not None
        for field in (info.user_message, info.retrying_message):
            assert names_a_model_or_provider(field) is None, (info.error_type, field)
        # the developer detail is kept: nothing was thrown away to make the sentence clean
        assert info.message or info.details, info.error_type


def test_a_provider_or_account_fault_reads_as_ours() -> None:
    for info in (
        provider_errors._handle_billing_error("OpenAI", "no credits remaining", 429),
        provider_errors._handle_auth_error("Anthropic", "invalid x-api-key", 401),
        provider_errors._handle_server_error("Google", "boom", 500),
    ):
        assert info.user_message == provider_errors.OUR_SIDE_MESSAGE
    billing = provider_errors._handle_billing_error("OpenAI", "account is suspended", 402)
    assert billing.details["account_condition"] == "is suspended"  # the operator still learns what happened
    assert "suspended" in billing.message


# ── dynamic: the caller-refusal gates ───────────────────────────────────────────────────────────────────────────


def test_every_caller_refusal_gate_speaks_in_fixed_text() -> None:
    from matrx_ai.providers.baa_gate import BaaRefusedError
    from matrx_ai.providers.free_tier_models import FreeTierModelRefusedError
    from matrx_ai.providers.model_channel_gate import ModelNotForChatError
    from matrx_ai.providers.model_tier_gate import TopTierModelRefusedError
    from matrx_ai.providers.readiness_gate import ReadinessRefusedError
    from matrx_ai.providers.usage_gate import UsageLimitReachedError
    from matrx_ai.speech.compile import SpeechScriptRefusal

    refusals: list[Any] = [
        FreeTierModelRefusedError(model_name=LEAK_MODEL, tier="free", user_id="u"),
        FreeTierModelRefusedError(model_name=LEAK_MODEL, tier="guest", user_id="u"),
        TopTierModelRefusedError(model_name=LEAK_MODEL, model_id=LEAK_MODEL, user_id="u"),
        ModelNotForChatError(model_name=LEAK_MODEL, channel="realtime", wire_format="x"),
        BaaRefusedError("This model", "openai"),
        ReadinessRefusedError(
            mandate_key="seo.keyword_gap", summary="A required input is missing",
            missing=[{"label": "Website", "fill_url": "https://x/y"}],
        ),
        UsageLimitReachedError({"plan_key": "free"}),
        UsageLimitReachedError({"plan_key": "guest"}),
    ]
    for refusal in refusals:
        info = refusal.error_info
        assert names_a_model_or_provider(info.user_message) is None, (type(refusal).__name__, info.user_message)
        assert "seo.keyword_gap" not in info.user_message
    speech = provider_errors.classify_internal_error(
        SpeechScriptRefusal(f"{LEAK_MODEL} ElevenLabs", user_message="Merge speakers."), "elevenlabs"
    )
    assert speech is not None and speech.user_message == "Merge speakers."
    bare = provider_errors.classify_internal_error(SpeechScriptRefusal(f"{LEAK_MODEL} ElevenLabs"), "elevenlabs")
    assert bare is not None and names_a_model_or_provider(bare.user_message) is None


def test_the_provider_word_list_covers_the_routing_table() -> None:
    lowered = {w.lower() for w in PROVIDER_WORDS}
    for key, display in provider_errors._PROVIDER_DISPLAY_NAMES.items():
        assert key in lowered and display.lower() in lowered
