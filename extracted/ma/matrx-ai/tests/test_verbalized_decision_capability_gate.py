"""A text model's decision run is gated by a field that EXISTS.

THE BREAK THIS CATCHES: `UnifiedAIClient._execute_dispatch` decides whether a
non-decision model may be asked decision questions. Until 2026-09-20 it asked
for three attribute names `ResolvedModelCapabilities` has never had —
`supports_structured_output`, `supports_json_schema`, `supports_json_mode` —
each through `getattr(..., False)`. The expression was therefore ALWAYS False,
so `prepare_verbalized_decision` refused EVERY text model by name:

    The message asks decision questions, but 'claude-sonnet-5' does not
    support structured output ...

about a model whose catalog row declares `structured_output`. A fallback ladder
over guessed attribute names cannot fail loudly. The one real field is
`structured_output_mode`.

The forcing input is the REAL live capability row of each model (swept from
ai.model_definition, 2026-09-20), so the test moves the day the catalog does.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.providers.resolved_capabilities import (
    ResolvedModelCapabilities,
    StructuredOutputMode,
    resolve_model_capabilities,
)

# The three names the broken ladder guessed at.
_GUESSED_NAMES = (
    "supports_structured_output",
    "supports_json_schema",
    "supports_json_mode",
)

# Live rows, verbatim. Sonnet declares structured_output; Jev is the decision
# holder and declares no features at all — two OPPOSITE answers, so a constant
# cannot satisfy both.
_SONNET = {
    "input": ["text", "image"],
    "output": ["text"],
    "features": [
        "computer_use",
        "function_calling",
        "json_mode",
        "prompt_caching",
        "structured_output",
        "thinking",
        "vision",
        "web_search",
    ],
    "interaction": "turn",
    "multilingual": True,
}
_JSON_ONLY = {**_SONNET, "features": ["json_mode"]}
_PLAIN = {**_SONNET, "features": []}


def _caps(row: dict, name: str) -> ResolvedModelCapabilities:
    return resolve_model_capabilities(
        SimpleNamespace(name=name, capabilities=dict(row))
    )


@pytest.mark.parametrize(
    ("row", "name", "may_be_asked"),
    [
        (_SONNET, "claude-sonnet-5", True),
        # json_mode promises well-formed JSON of NO particular shape, which is
        # the prose-nobody-can-score the decision contract exists to stop.
        (_JSON_ONLY, "some-json-mode-model", False),
        (_PLAIN, "some-plain-model", False),
    ],
)
def test_the_gate_reads_the_field_the_catalog_actually_fills(row, name, may_be_asked):
    caps = _caps(row, name)
    # This is the expression the client evaluates.
    assert (caps.structured_output_mode is StructuredOutputMode.SCHEMA) is may_be_asked


def test_the_guessed_attribute_names_do_not_exist_and_must_never_be_asked_for():
    caps = _caps(_SONNET, "claude-sonnet-5")
    for guessed in _GUESSED_NAMES:
        assert not hasattr(caps, guessed), (
            f"{guessed!r} now exists on ResolvedModelCapabilities. Either it is "
            "real and every reader should use it, or the ladder is back — "
            "decide deliberately, do not let getattr default it to False."
        )


def test_the_client_no_longer_gates_the_decision_overlay_on_a_missing_attribute():
    import inspect

    from matrx_ai.providers import unified_client

    source = inspect.getsource(unified_client.UnifiedAIClient._execute_dispatch)
    _head, _, tail = source.partition("prepare_verbalized_decision(")
    assert tail, "the verbalized overlay call moved — re-point this guard"
    call = tail.split("supports_structured_output=", 1)[1][:300]
    for guessed in _GUESSED_NAMES:
        assert guessed not in call, (
            f"the decision overlay is gated on {guessed!r} again — that "
            "attribute does not exist, so the gate is always False and every "
            "text model is refused a decision it can answer."
        )
    assert "structured_output_mode" in call
