"""The canonical `capabilities` vocabulary and the write-path guard.

Regression cover for 2026-09-12: the model-sync agent inserted gpt-6-astra,
claude-fable-5-1 and two gpt-image rows carrying provider-documentation
spellings, which resolved to capabilities being silently OFF.
"""

from __future__ import annotations

import pytest

from matrx_ai.providers.capability_vocabulary import (
    FEATURE_ALIASES,
    FEATURE_KEYS,
    normalize_capabilities,
)
from matrx_ai.providers.resolved_capabilities import (
    StructuredOutputMode,
    _structured_mode,
    resolve_model_capabilities,
)
from matrx_ai.tools.implementations.database import _guard_vocabulary


class _Model:
    def __init__(self, name, capabilities):
        self.name = name
        self.capabilities = capabilities


# ── the exact payloads that landed on 2026-09-12 ──────────────────────────

GPT_6_ASTRA = {
    "input": ["text", "image"],
    "output": ["text"],
    "features": [
        "function_calling",
        "structured_outputs",
        "streaming",
        "vision",
        "web_search",
        "file_search",
        "code_interpreter",
        "computer_use",
        "prompt_caching",
        "reasoning",
    ],
    "interaction": "turn",
    "multilingual": True,
}

CLAUDE_FABLE = {
    "input": ["image", "text"],
    "output": ["text"],
    "features": [
        "function_calling",
        "json_mode",
        "structured_output",
        "thinking",
        "vision",
        "pdf_input",
        "citations",
        "code_execution",
        "context_management",
        "batch",
        "prompt_caching",
    ],
    "interaction": "turn",
}


def test_provider_spellings_are_normalized_not_dropped():
    result = normalize_capabilities(GPT_6_ASTRA, label="gpt-6-astra")
    assert result.ok, result.rejections
    features = result.value["features"]
    assert "structured_output" in features
    assert "thinking" in features
    assert "code_execution" in features
    # the provider spellings never survive into the column
    assert "structured_outputs" not in features
    assert "reasoning" not in features
    assert "code_interpreter" not in features
    # and every correction is announced, never applied silently
    assert len(result.corrections) == 3


def test_pdf_input_is_relocated_to_the_document_input_modality():
    result = normalize_capabilities(CLAUDE_FABLE, label="claude-fable-5-1")
    assert result.ok, result.rejections
    assert "pdf_input" not in result.value["features"]
    assert "document" in result.value["input"]
    assert "batch_api" in result.value["features"]
    # a genuinely new capability keeps its own word
    assert "context_management" in result.value["features"]


def test_unknown_value_is_rejected_with_the_fix_named():
    result = normalize_capabilities(
        {"input": ["text"], "output": ["text"], "features": ["telepathy"]}, label="m"
    )
    assert not result.ok
    message = result.rejection_message()
    assert "telepathy" in message
    assert "capability_vocabulary.py" in message


@pytest.mark.parametrize("bad", [None, [], "features", 7])
def test_pre_canonical_shapes_are_rejected(bad):
    assert not normalize_capabilities(bad).ok


def test_unknown_top_level_key_is_rejected():
    assert not normalize_capabilities({"input": ["text"], "text_input": True}).ok


@pytest.mark.parametrize(
    ("label", "capabilities"),
    [
        (
            "scalar feature alias",
            {"input": ["text"], "output": ["text"], "features": "structured_outputs"},
        ),
        (
            "null feature collection",
            {"input": ["text"], "output": ["text"], "features": None},
        ),
        (
            "null input collection",
            {"input": None, "output": ["text"], "features": []},
        ),
        (
            "nested feature object",
            {
                "input": ["text"],
                "output": ["text"],
                "features": {"structured_outputs": True},
            },
        ),
        (
            "nested input object",
            {"input": {"modalities": ["pdf"]}, "output": ["text"], "features": []},
        ),
        (
            "mixed invalid members",
            {
                "input": ["text", {"kind": "pdf"}, 7],
                "output": ["text"],
                "features": ["structured_output", {"name": "batch"}],
            },
        ),
    ],
)
def test_malformed_capability_collections_are_rejected_not_erased(label, capabilities):
    """The write guard must never make malformed nested data look accepted."""
    result = normalize_capabilities(capabilities, label=label)

    assert not result.ok
    assert result.rejections

    rows = [{"name": label, "capabilities": capabilities}]
    error, corrections = _guard_vocabulary("ai", "model_definition", rows)

    assert error
    assert not corrections
    # A rejected payload is left intact rather than quietly half-normalized.
    assert rows[0]["capabilities"] is capabilities


def test_missing_capability_collections_remain_a_valid_sparse_shape():
    """Missing sections default to empty; explicit null is rejected above."""
    result = normalize_capabilities({"interaction": "turn"})

    assert result.ok
    assert result.value["input"] == []
    assert result.value["output"] == []
    assert result.value["features"] == []


def test_rejected_batch_is_not_partially_canonicalized():
    alias_row = {"name": "alias", "capabilities": dict(GPT_6_ASTRA)}
    malformed = {"name": "bad", "capabilities": {"features": None}}
    original_alias_features = alias_row["capabilities"]["features"]
    original_malformed = malformed["capabilities"]

    error, corrections = _guard_vocabulary("ai", "model_definition", [alias_row, malformed])

    assert error
    assert corrections == []
    assert alias_row["capabilities"]["features"] is original_alias_features
    assert "structured_outputs" in alias_row["capabilities"]["features"]
    assert malformed["capabilities"] is original_malformed


def test_aliases_only_ever_point_at_canonical_terms():
    for spelling, canonical in FEATURE_ALIASES.items():
        assert canonical in FEATURE_KEYS, f"{spelling} -> {canonical} is not canonical"
        assert spelling not in FEATURE_KEYS, f"{spelling} is both a term and an alias"


# ── the damage the drift actually caused ──────────────────────────────────


def test_the_stored_drift_turned_schema_output_off():
    """THE failure, both halves.

    First half proves the defect is real and not hypothetical: the stored
    feature set, read literally the way the resolver read it before
    2026-09-12, yields TEXT — schema-mode structured output OFF on a model
    whose row declares it. Second half proves the repair.
    """
    assert _structured_mode(frozenset(GPT_6_ASTRA["features"])) is StructuredOutputMode.TEXT

    raw = resolve_model_capabilities(_Model("gpt-6-astra", GPT_6_ASTRA))
    # the read path now normalizes the legacy spelling instead of resolving
    # around it (while screaming), so schema mode is honoured
    assert raw.structured_output_mode is StructuredOutputMode.SCHEMA
    assert "code_execution" in raw.native_capabilities


def test_canonical_row_resolves_identically():
    canonical = normalize_capabilities(GPT_6_ASTRA).value
    assert resolve_model_capabilities(
        _Model("gpt-6-astra", canonical)
    ) == resolve_model_capabilities(_Model("gpt-6-astra", GPT_6_ASTRA))


def test_single_and_agent_interaction_survive_resolution():
    """9 live rows declared these; the resolver used to coerce them to 'turn'."""
    for mode in ("single", "agent"):
        caps = resolve_model_capabilities(
            _Model("m", {"input": ["text"], "output": ["image"], "interaction": mode})
        )
        assert caps.interaction == mode


# ── the write choke point ─────────────────────────────────────────────────


def test_write_guard_refuses_an_unknown_capability_value():
    rows = [{"name": "m", "capabilities": {"input": ["text"], "features": ["telepathy"]}}]
    error, corrections = _guard_vocabulary("ai", "model_definition", rows)
    assert error and "telepathy" in error
    # the payload is NOT quietly half-written
    assert rows[0]["capabilities"]["features"] == ["telepathy"]


def test_write_guard_canonicalizes_and_reports_provider_spellings():
    rows = [{"name": "gpt-6-astra", "capabilities": dict(GPT_6_ASTRA)}]
    error, corrections = _guard_vocabulary("ai", "model_definition", rows)
    assert error is None
    assert "structured_output" in rows[0]["capabilities"]["features"]
    assert corrections, "a silent correction is the same bug as a silent drop"


def test_write_guard_ignores_tables_it_does_not_own():
    rows = [{"capabilities": "anything at all"}]
    assert _guard_vocabulary("chat", "message", rows) == (None, [])
