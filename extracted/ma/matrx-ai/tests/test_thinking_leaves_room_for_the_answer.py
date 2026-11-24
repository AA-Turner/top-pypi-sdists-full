"""THINKING NEVER TAKES THE ANSWER'S ROOM — the send boundary's answer reserve, per provider family.

Live 2026-11-04 (Claude Haiku 5.5, output limit 1,500, effort low): requests 9d19883a and
ca6660d2 spent 1,247 and 1,467 of their 1,500 tokens thinking and the person got a cut-off
story. Every thinking model counts its thinking inside the output limit, so the boundary now
keeps ``agents.output_room.answer_reserve_share`` (starting 0.5) of the authored limit for the
answer: a numeric thinking cap is lowered where the provider takes one, otherwise the limit is
raised by the reserve, within the model's real maximum.

Forcing: every case runs the REAL ``prepare_for_send`` over the REAL catalog translation
(``CompiledControlsMap.outbound`` with the live offering cells, verbatim from
``ai.offering_rules_compiled`` 2026-11-04); only the profile lookup and the context window are
replaced. On the pre-fix boundary nothing touched the limit, so every "raised"/"capped" case
fails (the Haiku 5.5 case goes out at 1,500 — exactly the live failure).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog import resolve as catalog_resolve
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.config import context_preflight
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.knobs import configure_package_knobs
from matrx_ai.providers.outbound_params import preview_outbound_params

CONVERSATION_ID = "conv-answer-room"
REQUEST_ID = "9d19883a-0000-4000-8000-000000000001"
ORDER = {"reasoning_effort": ["auto", "none", "minimal", "low", "medium", "high", "xhigh", "max"]}

_CONSUMES = ["thinking_budget", "thinking_level", "include_thoughts", "reasoning_summary", "clear_thinking"]

# Live cells, verbatim shape (ai.offering_rules_compiled, 2026-11-04).
OFFERINGS: dict[str, dict[str, Any]] = {
    "claude-haiku-5-5": {
        "max": 128_000,
        "rules": {
            "max_output_tokens": {"provider_key": "max_tokens"},
            "reasoning_effort": {
                "off": {"send": {"type": "disabled"}},
                "processor": "anthropic_thinking",
                "provider_key": "thinking",
                "processor_config": {
                    "mode": "adaptive", "order": 100, "consumes": _CONSUMES,
                    "thinks_by_default": True, "default_max_tokens": 128000,
                },
            },
            "thinking_budget": {"supported": False},
        },
    },
    "claude-haiku-4-5-20251001": {
        "max": 64_000,
        "rules": {
            "max_output_tokens": {"provider_key": "max_tokens"},
            "reasoning_effort": {
                "off": {"send": {"type": "disabled"}},
                "processor": "anthropic_thinking",
                "provider_key": "thinking",
                "processor_config": {
                    "mode": "budget", "order": 100, "consumes": _CONSUMES, "default_max_tokens": 32768,
                },
            },
        },
    },
    "gemini-2.5-flash": {
        "max": 50_000,
        "rules": {
            "max_output_tokens": {"clamp": {"min": 16}, "provider_key": "max_output_tokens"},
            "reasoning_effort": {
                "off": {"send": 0},
                "processor": "google_thinking",
                "provider_key": "thinking_config.thinking_budget",
                "processor_config": {
                    "mode": "legacy", "order": 100, "consumes": _CONSUMES, "max_thinking_budget": 24576,
                },
            },
        },
    },
    "gemini-3.8-flash": {
        "max": 128_000,
        "rules": {
            "max_output_tokens": {"clamp": {"min": 16}, "provider_key": "max_output_tokens"},
            "reasoning_effort": {
                "default": "medium",
                "processor": "google_thinking",
                "ui_values": ["auto", "none", "low", "medium", "high"],
                "processor_config": {"mode": "gemini_3", "family": "flash", "consumes": _CONSUMES},
            },
        },
    },
    "gpt-5.5": {
        "max": 128_000,
        "rules": {
            "max_output_tokens": {"clamp": {"min": 16}, "provider_key": "max_output_tokens"},
            "reasoning_effort": {
                "off": {"send": "none"},
                "accepts": ["none", "low", "medium", "high", "xhigh"],
                "to_default": ["auto"],
                "on_unmapped": "nearest",
                "provider_key": "reasoning.effort",
            },
            "thinking_budget": {"supported": False},
        },
    },
    "openai/gpt-oss-120b@cerebras": {
        "max": 40_960,
        "rules": {
            "max_output_tokens": {"clamp": {"max": 40960}, "provider_key": "max_completion_tokens"},
            "reasoning_effort": {
                "off": {"floor": True},
                "value_map": {"low": "low", "auto": None, "high": "high", "none": None,
                              "xhigh": "high", "medium": "medium", "minimal": "low"},
                "provider_key": "reasoning_effort",
            },
        },
    },
    "zai-org/GLM-5.2": {
        "max": 131_072,
        "rules": {
            "max_output_tokens": {"provider_key": "max_tokens"},
            "reasoning_effort": {
                "off": {"send": "false"},
                "accepts": ["high", "max"],
                "processor": "together_reasoning",
                "to_default": ["auto"],
                "on_unmapped": "nearest",
                "provider_key": "chat_template_kwargs.thinking",
            },
        },
    },
    "plain-chat-model": {
        "max": 32_000,
        "rules": {"max_output_tokens": {"provider_key": "max_tokens"}},
    },
}


def _controls(model: str) -> CompiledControlsMap:
    spec = OFFERINGS[model]
    rules = {k: ControlRule.model_validate(v) for k, v in spec["rules"].items()}
    return CompiledControlsMap(rules=rules, value_orders=ORDER, output_maximum=spec["max"])


def _config(model: str, *, limit: int = 1500, effort: str | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        model=model,
        matrx_model_name=model,
        messages=[{"role": "user", "content": "Write a 150-word story ending in THE END."}],
        system_instruction="You are a storyteller.",
        tools=[],
        prompt_cache_key=None,
        max_output_tokens=limit,
        reasoning_effort=effort,
        thinking_budget=None,
        thinking_level=None,
        response_format=None,
    )


async def _send(config: SimpleNamespace) -> Any:
    return await prepare_for_send(
        config, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=1
    )


@pytest.fixture(autouse=True)
def _catalog(monkeypatch):
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    configure_package_knobs(None)  # standalone: the knob answers its mirror (0.5)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)

    async def _profile(model: str, **_kw: Any) -> Any:
        return SimpleNamespace(model_name=model, offering_id="", controls=_controls(model))

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)
    yield
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


def _wire(config: SimpleNamespace) -> dict[str, Any]:
    return preview_outbound_params(config, _controls(config.model))


def _sent(prep: Any, config: SimpleNamespace) -> SimpleNamespace:
    """What went on the wire: the raise rides ``prep.wire_config``, never the stored config."""
    return prep.wire_config if prep.wire_config is not None else config


# ── Anthropic ────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_haiku_5_5_adaptive_thinking_gets_the_reserve_added_to_its_limit() -> None:
    """The live failure: adaptive thinking has no budget, so the limit carries the reserve."""
    config = _config("claude-haiku-5-5")
    assert _wire(config)["thinking"]["type"] == "adaptive"
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 2250
    assert _sent(prep, config).thinking_budget is None  # Haiku 5.5 rejects budget_tokens; none is sent
    assert "answer_reserve" in prep.steps
    assert _wire(_sent(prep, config))["max_tokens"] == 2250


@pytest.mark.asyncio
async def test_haiku_4_5_budget_thinking_is_capped_to_leave_the_reserve() -> None:
    """Budget mode takes a number: effort high (8,192) at a limit of 8,000 is capped to 4,000."""
    config = _config("claude-haiku-4-5-20251001", limit=8000, effort="high")
    prep = await _send(config)
    wire = _wire(_sent(prep, config))
    assert wire["max_tokens"] == 8000
    assert wire["thinking"] == {"type": "enabled", "budget_tokens": 4000}


@pytest.mark.asyncio
async def test_haiku_4_5_below_the_budget_floor_raises_the_limit_instead() -> None:
    """At 1,500 the cap would be 750 < Anthropic's 1,024 floor: floor budget, limit 1,024 + 750."""
    config = _config("claude-haiku-4-5-20251001", limit=1500, effort="low")
    prep = await _send(config)
    wire = _wire(_sent(prep, config))
    assert wire["thinking"] == {"type": "enabled", "budget_tokens": 1024}
    assert wire["max_tokens"] == 1774
    assert wire["max_tokens"] - wire["thinking"]["budget_tokens"] >= 750


@pytest.mark.asyncio
async def test_claude_with_thinking_off_is_left_alone() -> None:
    config = _config("claude-haiku-4-5-20251001", effort="none")
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 1500


# ── Google ───────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_gemini_2_5_thinking_budget_is_capped() -> None:
    config = _config("gemini-2.5-flash", limit=1500, effort="low")
    assert _wire(config)["thinking_config"]["thinking_budget"] == 1024
    prep = await _send(config)
    wire = _wire(_sent(prep, config))
    assert _sent(prep, config).max_output_tokens == 1500
    assert wire["thinking_config"]["thinking_budget"] == 750


@pytest.mark.asyncio
async def test_gemini_3_thinking_level_has_no_cap_so_the_limit_is_raised() -> None:
    config = _config("gemini-3.8-flash")
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 2250


# ── OpenAI and OpenAI-compatible ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_openai_reasoning_effort_raises_the_limit() -> None:
    config = _config("gpt-5.5", effort="medium")
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 2250


@pytest.mark.asyncio
async def test_openai_reasoning_none_is_left_alone() -> None:
    config = _config("gpt-5.5", effort="none")
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 1500


@pytest.mark.asyncio
async def test_cerebras_gpt_oss_always_reasons_so_the_limit_is_raised() -> None:
    config = _config("openai/gpt-oss-120b@cerebras")
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 2250


@pytest.mark.asyncio
async def test_together_reasoning_on_raises_and_off_is_left_alone() -> None:
    on = _config("zai-org/GLM-5.2", effort="high")
    prep = await _send(on)
    assert _sent(prep, on).max_output_tokens == 2250
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    off = _config("zai-org/GLM-5.2", effort="none")
    prep = await _send(off)
    assert _sent(prep, off).max_output_tokens == 1500


# ── Every family ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_model_without_reasoning_keeps_its_authored_limit() -> None:
    config = _config("plain-chat-model")
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 1500
    assert "answer_reserve" not in prep.steps


@pytest.mark.asyncio
async def test_the_raise_never_passes_the_models_real_maximum() -> None:
    config = _config("claude-haiku-5-5", limit=100_000)
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 128_000


@pytest.mark.asyncio
async def test_later_rounds_start_from_the_authored_limit_and_a_reasoning_off_retry_gets_it_back() -> None:
    config = _config("claude-haiku-5-5")
    prep = await _send(config)
    prep = await _send(config)
    assert _sent(prep, config).max_output_tokens == 2250  # not 3,375: the second round re-judges from 1,500
    # EMPTY-REPLY's last resort turns reasoning off (``_turn_reasoning_off_for_retry``) for ONE send,
    # on the wire copy (CGU-10 IMG6 #1): no reserve on that call, and the stored effort is untouched.
    prep = await prepare_for_send(
        config, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=3,
        one_call={"reasoning_effort": "none", "thinking_budget": None, "thinking_level": None},
    )
    assert _sent(prep, config).max_output_tokens == 1500
    assert _sent(prep, config).reasoning_effort == "none"
    assert config.reasoning_effort is None and config.max_output_tokens == 1500


@pytest.mark.asyncio
async def test_the_reserve_follows_the_knob(monkeypatch) -> None:
    configure_package_knobs(lambda feature, key: 0.25 if (feature, key) == ("agents.output_room", "answer_reserve_share") else None)
    try:
        config = _config("claude-haiku-5-5")
        prep = await _send(config)
        assert _sent(prep, config).max_output_tokens == 1875
    finally:
        configure_package_knobs(None)


class _RecordingEmitter:
    def __init__(self) -> None:
        self.warnings: list[Any] = []

    async def send_warning(self, payload: Any) -> None:
        self.warnings.append(payload)


@pytest.mark.asyncio
async def test_the_change_is_announced_to_the_caller(monkeypatch) -> None:
    import asyncio

    import matrx_connect

    rec = _RecordingEmitter()
    monkeypatch.setattr(matrx_connect, "get_app_context", lambda: SimpleNamespace(emitter=rec))
    config = _config("claude-haiku-5-5")
    await _send(config)
    for _ in range(5):
        await asyncio.sleep(0)
    codes = [(w.code, w.metadata.get("adjusted")) for w in rec.warnings]
    assert ("setting_adjusted", [{"key": "max_output_tokens", "requested": 1500, "sent": 2250}]) in codes


@pytest.mark.asyncio
async def test_the_reserve_is_announced_once_per_request_not_every_round(monkeypatch) -> None:
    """CGU-10 IMG6 F9 (plant N2 survived): a tool loop's later rounds re-apply the reserve but the
    person and the settings record hear about it ONCE per request."""
    import asyncio

    import matrx_connect

    from matrx_ai.config import send_boundary

    rec = _RecordingEmitter()
    recorded: list[Any] = []
    monkeypatch.setattr(matrx_connect, "get_app_context", lambda: SimpleNamespace(emitter=rec))
    monkeypatch.setattr(send_boundary, "_record_answer_reserve", lambda **kw: recorded.append(kw))
    config = _config("claude-haiku-5-5")
    for iteration in (1, 2, 3, 4):
        prep = await prepare_for_send(
            config, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID, iteration=iteration
        )
        assert _sent(prep, config).max_output_tokens == 2250  # every round still sends the reserve
    for _ in range(5):
        await asyncio.sleep(0)
    reserve_warnings = [
        w for w in rec.warnings if any(a.get("key") == "max_output_tokens" for a in (w.metadata.get("adjusted") or []))
    ]
    assert len(reserve_warnings) == 1
    assert len(recorded) == 1
