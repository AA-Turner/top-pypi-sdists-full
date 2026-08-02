"""Unit tests for ``_detect_context_window`` in agno.py.

Guards the model-id → context-window resolution so a misdetect can't
silently regress (PRO-1298 / Mercury: 1M models were detected as 128K
because the substring table was too small, triggering compaction at
~100K and a 25-minute compaction loop).
"""

from __future__ import annotations

import pytest

from xpander_sdk.modules.backend.frameworks.agno import (
    _DEFAULT_UNKNOWN_CONTEXT_WINDOW,
    _MODEL_CONTEXT_WINDOWS_EXACT,
    _detect_context_window,
)


class _M:
    """Minimal stand-in for agno's Model — only ``id`` is read."""

    def __init__(self, model_id: str) -> None:
        self.id = model_id


# Representative model IDs sampled from each tier of the xpander
# platform model catalog (PRO-1298). The expected windows mirror the
# catalog descriptions.
_KNOWN_MODELS = [
    # 10M
    ("meta.llama4-scout-17b-instruct-v1:0", 10_000_000),
    ("meta-llama/llama-4-scout", 10_000_000),
    # 4M
    ("minimax/minimax-01", 4_000_000),
    # 1M
    ("gpt-4.1", 1_047_576),
    ("gpt-4.1-mini", 1_047_576),
    ("global.anthropic.claude-opus-5", 1_000_000),
    ("global.anthropic.claude-opus-4-8", 1_000_000),
    ("global.anthropic.claude-opus-4-7", 1_000_000),
    ("global.anthropic.claude-sonnet-5", 1_000_000),
    ("global.anthropic.claude-sonnet-4-6", 1_000_000),
    # Versioned Bedrock form resolves via substring, not just the exact map.
    ("global.anthropic.claude-sonnet-5-20250930-v1:0", 1_000_000),
    ("claude-opus-5", 1_000_000),
    ("claude-opus-4-8", 1_000_000),
    ("claude-opus-4-7", 1_000_000),
    ("claude-sonnet-5", 1_000_000),
    ("claude-sonnet-4-6", 1_000_000),
    ("gemini-2.5-pro", 1_000_000),
    ("gemini-2.0-flash", 1_000_000),
    ("google/gemini-3-pro-preview", 1_000_000),
    ("amazon.nova-premier-v1:0", 1_000_000),
    ("amazon.nova-2-lite-v1:0", 1_000_000),
    ("meta.llama4-maverick-17b-instruct-v1:0", 1_000_000),
    ("qwen/qwen3-max", 1_000_000),
    ("minimax/minimax-m1", 1_000_000),
    # 400K (GPT-5 family)
    ("gpt-5", 400_000),
    ("gpt-5-mini", 400_000),
    ("gpt-5.5", 400_000),
    ("openai/gpt-5", 400_000),
    ("openai/gpt-5-codex", 400_000),
    # 300K (Nova Pro/Lite)
    ("amazon.nova-pro-v1:0", 300_000),
    ("amazon.nova-lite-v1:0", 300_000),
    # 256K
    ("x-ai/grok-4", 256_000),
    ("moonshotai/Kimi-K2-Instruct", 256_000),
    ("qwen/qwen3-coder", 256_000),
    ("mistral.mistral-large-3-675b-instruct", 256_000),
    # 200K
    ("global.anthropic.claude-opus-4-5-20251101-v1:0", 200_000),
    ("global.anthropic.claude-sonnet-4-5-20250929-v1:0", 200_000),
    ("anthropic.claude-opus-4-1-20250805-v1:0", 200_000),
    ("claude-opus-4-5", 200_000),
    ("claude-sonnet-4-5", 200_000),
    ("anthropic/claude-opus-4.5", 200_000),
    ("anthropic/claude-sonnet-4.5", 200_000),
    ("openai/o1", 200_000),
    ("openai/o3", 200_000),
    # 196K (MiniMax M2.x)
    ("minimax/minimax-m2", 196_000),
    # 128K-131K
    ("gpt-4o", 128_000),
    ("gpt-4o-mini", 128_000),
    ("gpt-4-turbo", 128_000),
    ("meta-llama/Llama-3.3-70B-Instruct", 128_000),
    ("meta.llama3-1-405b-instruct-v1:0", 128_000),
    ("us.deepseek.r1-v1:0", 128_000),
    ("amazon.nova-micro-v1:0", 128_000),
    ("x-ai/grok-3", 131_072),
    # Smaller
    ("mistralai/mistral-7b-instruct", 32_000),
    ("openai/gpt-3.5-turbo", 16_385),
    ("amazon.titan-text-express-v1", 8_000),
]


@pytest.mark.parametrize("model_id,expected", _KNOWN_MODELS)
def test_known_model_resolves_to_documented_window(
    model_id: str, expected: int
) -> None:
    assert _detect_context_window(_M(model_id)) == expected


def test_unknown_model_defaults_to_conservative_window() -> None:
    # An unmapped model id falls back to a conservative window so it can't
    # be told it has more context than it does (over-budgeting an unmapped
    # small-window model is what caused the non-frontier overflow + spin).
    assert (
        _detect_context_window(_M("totally-made-up-2099-model"))
        == _DEFAULT_UNKNOWN_CONTEXT_WINDOW
    )
    assert _DEFAULT_UNKNOWN_CONTEXT_WINDOW < 200_000


def test_empty_model_id_defaults_to_conservative_window() -> None:
    assert _detect_context_window(_M("")) == _DEFAULT_UNKNOWN_CONTEXT_WINDOW


def test_substring_fallback_for_unmapped_1m_variant() -> None:
    # Variants we don't enumerate explicitly should still resolve via
    # substring fallback. ``claude-opus-4-7-1m`` is not in the exact map
    # but ``-1m`` substring should win before the generic ``claude``.
    assert _detect_context_window(_M("claude-opus-4-7-1m")) == 1_000_000


def test_substring_fallback_for_bracketed_1m_suffix() -> None:
    assert _detect_context_window(_M("claude-opus-4-7[1m]")) == 1_000_000


def test_case_insensitive_exact_match() -> None:
    # Nebius uses mixed-case ids — confirm case-insensitive lookup
    # finds the entry even when the catalog stored it differently.
    expected = _MODEL_CONTEXT_WINDOWS_EXACT.get("meta-llama/Meta-Llama-3.1-8B-Instruct")
    assert expected is not None
    detected = _detect_context_window(_M("META-LLAMA/META-LLAMA-3.1-8B-INSTRUCT"))
    assert detected == expected


def test_gpt5_does_not_match_gpt5_image_variants_to_legacy_window() -> None:
    # Regression guard: ``gpt-5`` substring must not catch ``gpt-5-image``
    # at a wrong tier (both are GPT-5 family, both 400K).
    assert _detect_context_window(_M("openai/gpt-5-image")) == 400_000
    assert _detect_context_window(_M("openai/gpt-5-image-mini")) == 400_000


def test_1m_takes_precedence_over_generic_claude() -> None:
    # Without the ``-1m`` / ``[1m]`` substring entries, this id would
    # match ``claude`` first and fall to 200K — that was the Mercury bug.
    assert _detect_context_window(_M("anthropic/claude-foo-1m")) == 1_000_000


def test_bedrock_dot_form_llama4_substring_fallback() -> None:
    # Future Bedrock SKUs in the ``meta.llama4-*`` family (dot-form, no
    # hyphen between ``llama`` and ``4``) must resolve to the right
    # tier even if the EXACT map doesn't list them.
    assert _detect_context_window(_M("meta.llama4-scout-future-sku")) == 10_000_000
    assert _detect_context_window(_M("meta.llama4-maverick-future-sku")) == 1_000_000


def test_unknown_model_warning_dedup_set_records_id() -> None:
    # The unknown-model warning must dedup per process — flooding the log
    # on tight loops over the same unmapped id is a pre-existing PR
    # complaint (PR #511 review). The dedup mechanism is the
    # module-level set; assert it records the id and survives repeat
    # calls without growing.
    from xpander_sdk.modules.backend.frameworks.agno import (
        _LOGGED_UNKNOWN_MODEL_IDS,
    )

    unique_id = "deduped-warning-probe-model-x"
    _LOGGED_UNKNOWN_MODEL_IDS.discard(unique_id)
    _detect_context_window(_M(unique_id))
    assert unique_id in _LOGGED_UNKNOWN_MODEL_IDS
    before = len(_LOGGED_UNKNOWN_MODEL_IDS)
    _detect_context_window(_M(unique_id))
    _detect_context_window(_M(unique_id))
    assert len(_LOGGED_UNKNOWN_MODEL_IDS) == before
