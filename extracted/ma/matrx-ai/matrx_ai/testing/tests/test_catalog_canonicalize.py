"""Pure-unit tests for matrx_ai.catalog.canonicalize — no DB."""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.catalog.canonicalize import canonical_settings_from_config


def _cfg(**kwargs) -> SimpleNamespace:
    return SimpleNamespace(**kwargs)


class TestCanonicalizeReasoning:
    def test_disable_reasoning_true_wins(self):
        out = canonical_settings_from_config(
            _cfg(disable_reasoning=True, reasoning_effort="high", thinking_budget=5000)
        )
        assert out["reasoning_effort"] == "none"

    def test_explicit_effort_wins_over_budget(self):
        out = canonical_settings_from_config(_cfg(reasoning_effort="low", thinking_budget=50_000))
        assert out["reasoning_effort"] == "low"

    def test_disable_reasoning_false_defaults_medium(self):
        # Mirrors ThinkingConfig.from_settings: "reasoning ON, no level picked".
        out = canonical_settings_from_config(_cfg(disable_reasoning=False))
        assert out["reasoning_effort"] == "medium"

    def test_thinking_budget_tiers(self):
        # Transcribed from ThinkingConfig.to_openai_reasoning.
        for budget, effort in [
            (0, "none"),
            (1, "low"),
            (1999, "low"),
            (2000, "medium"),
            (9999, "medium"),
            (10_000, "high"),
            (19_999, "high"),
            (20_000, "xhigh"),
            (100_000, "xhigh"),
        ]:
            out = canonical_settings_from_config(_cfg(thinking_budget=budget))
            assert out["reasoning_effort"] == effort, f"budget={budget}"
            assert out["thinking_budget"] == budget  # raw budget rides along

    def test_budget_passthrough_with_explicit_effort(self):
        out = canonical_settings_from_config(_cfg(reasoning_effort="high", thinking_budget=4096))
        assert out == {"reasoning_effort": "high", "thinking_budget": 4096}


class TestCanonicalizeGeneral:
    def test_all_none_produces_empty(self):
        assert canonical_settings_from_config(_cfg()) == {}
        assert (
            canonical_settings_from_config(
                _cfg(
                    reasoning_effort=None,
                    reasoning_summary=None,
                    temperature=None,
                    top_p=None,
                    top_k=None,
                    max_output_tokens=None,
                    seed=None,
                    stop_sequences=[],
                    response_format=None,
                    thinking_budget=None,
                    disable_reasoning=None,
                )
            )
            == {}
        )

    def test_only_set_keys_included(self):
        out = canonical_settings_from_config(
            _cfg(temperature=0.7, max_output_tokens=1000, reasoning_summary="detailed")
        )
        assert out == {
            "temperature": 0.7,
            "max_output_tokens": 1000,
            "reasoning_summary": "detailed",
        }

    def test_scalar_passthrough(self):
        out = canonical_settings_from_config(
            _cfg(
                top_p=0.9,
                top_k=40,
                seed=42,
                stop_sequences=["END"],
                response_format={"type": "json_object"},
            )
        )
        assert out == {
            "top_p": 0.9,
            "top_k": 40,
            "seed": 42,
            "stop_sequences": ["END"],
            "response_format": {"type": "json_object"},
        }

    def test_temperature_zero_is_kept(self):
        assert canonical_settings_from_config(_cfg(temperature=0.0)) == {"temperature": 0.0}
