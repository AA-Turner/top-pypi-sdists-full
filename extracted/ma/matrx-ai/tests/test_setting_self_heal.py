"""Settings Translation R2 — a classified settings rejection heals itself ONCE, in-line.

Owner (2026-10-02): "No request should EVER GET an error when you submit one to
the other because the server is supposed to convert it" / "My request should go
through". When a provider refuses a request because of a SETTING it names, the
shared dispatch seam (``UnifiedAIClient._dispatch_with_billing_net``) repairs
that one setting mechanically on the per-call wire config and sends the call
ONCE more; the person gets one short warning and the K10 record still files
(lifecycle ``new``) with ``self_healed`` and the repair.

Breaks named:
* the Groq 32,000-vs-16,384 rejection the owner hit stays an error;
* a retry loops (a second rejection is retried again);
* a non-settings 400 or a billing refusal is retried;
* a rejection after the answer started streaming is retried (the person would
  see the answer twice);
* the record and the stream disagree about what was changed.

Real code: the dispatch seam, the real admission gate, the shared classifier,
the R1 recognizer + record, the client-warning door. Doubles: the vendor wire
(raising each SDK's own exception, with real provider messages from
``ops.ops_issue_event``), ``capture_error`` and the emitter.
``test_planted_*`` proves the guards go red on a looping or over-eager seam.
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
import pytest

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.providers import failure_report, setting_rejection
from matrx_ai.providers import unified_client as uc
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

_REQ = httpx.Request("POST", "https://provider.test/v1/chat/completions")
_GROQ_MODEL = "qwen/qwen3.8-27b"


def _stainless(module: Any, cls: str, status: int, body: dict[str, Any]) -> Exception:
    return getattr(module, cls)(f"Error code: {status} - {body}", response=httpx.Response(status, request=_REQ), body=body)


def _groq_max_completion_tokens() -> Exception:
    """The owner's error, verbatim (request badc0b91…, 2026-10-02 03:48Z)."""
    import groq

    body = {
        "error": {
            "message": (
                "`max_completion_tokens` must be less than or equal to `16384`, the maximum value "
                "for `max_completion_tokens` is less than the `context_window` for this model"
            ),
            "type": "invalid_request_error",
            "param": "max_completion_tokens",
        }
    }
    return _stainless(groq, "BadRequestError", 400, body)


def _anthropic(message: str) -> Exception:
    import anthropic

    return _stainless(
        anthropic,
        "BadRequestError",
        400,
        {"type": "error", "error": {"type": "invalid_request_error", "message": message}},
    )


def _openai(body_error: dict[str, Any], status: int = 400) -> Exception:
    import openai

    return _stainless(openai, "BadRequestError", status, {"error": body_error})


def _gemini_opaque() -> Exception:
    from google.genai.errors import ClientError

    return ClientError(
        400,
        {"error": {"code": 400, "message": "Request contains an invalid argument.", "status": "INVALID_ARGUMENT"}},
    )


class _Emitter:
    """Records warnings; ``streamed`` simulates answer text that reached the person."""

    def __init__(self) -> None:
        self.text = ""
        self.warnings: list[Any] = []

    def get_turn_text(self) -> str:
        return self.text

    async def send_warning(self, payload: Any) -> None:
        self.warnings.append(payload)


@pytest.fixture(autouse=True)
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def capture_error(exc: BaseException, **kwargs: Any) -> None:
        rows.append({"exc": exc, **kwargs})

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_error)
    failure_report.reset_alarm_memory()
    return rows


def _setting_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r["kind"] == setting_rejection.PROVIDER_SETTING_REJECTED_KIND]


def _groq_profile() -> Any:
    return make_profile(
        model_name=_GROQ_MODEL,
        wire_format="groq_chat",
        vendor="groq",
        rules={"max_output_tokens": {"provider_key": "max_completion_tokens"}},
    )


def _anthropic_profile() -> Any:
    return make_profile(
        model_name="claude-opus-5-5",
        wire_format="anthropic_chat",
        vendor="anthropic",
        rules={"temperature": {}, "max_output_tokens": {"provider_key": "max_tokens"}},
    )


def _openai_profile() -> Any:
    return make_profile(
        model_name="gpt-5.5",
        wire_format="openai_chat",
        vendor="openai",
        rules={"reasoning_effort": {"provider_key": "reasoning.effort"}},
        # The canonical scale (ai.setting.canonical_values) the metric measures on.
        value_orders={"reasoning_effort": ["none", "minimal", "low", "medium", "high", "xhigh", "max"]},
    )


async def _run(
    profile: Any,
    config: Any,
    outcomes: list[Any],
    *,
    emitter: _Emitter | None = None,
    stream_on_call: int | None = None,
    request_id: str = "req-r2",
) -> tuple[list[dict[str, Any]], Any]:
    """Dispatch through the REAL seam; the vendor wire is a script of outcomes."""
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    sent: list[dict[str, Any]] = []
    script = list(outcomes)

    async def dispatch() -> Any:
        sent.append(
            {
                "max_output_tokens": getattr(config, "max_output_tokens", None),
                "temperature": getattr(config, "temperature", None),
                "reasoning_effort": getattr(config, "reasoning_effort", None),
                "stop_sequences": getattr(config, "stop_sequences", None),
            }
        )
        if emitter is not None and stream_on_call == len(sent):
            emitter.text += "The quarterly vacancy rate across the portfolio"
        outcome = script.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    token = set_app_context(
        AppContext(emitter=emitter, user_id="user-r2", conversation_id="conv-r2", request_id=request_id)
    )
    try:
        try:
            result: Any = await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=profile, config=config)
        except Exception as exc:  # noqa: BLE001 — returned for the assertion
            result = exc
        await asyncio.sleep(0)  # let the detached warning task run
        await asyncio.sleep(0)
    finally:
        clear_app_context(token)
    return sent, result


_OK = {"answer": "Occupancy held at 96% across the three Harbor View buildings."}


# ── guard helpers (the planted tests drive these red) ────────────────────────


def _assert_at_most_one_repair(sent: list[dict[str, Any]]) -> None:
    assert len(sent) <= 2, f"self-heal looped: {len(sent)} provider calls for one request"


def _assert_not_retried(sent: list[dict[str, Any]]) -> None:
    assert len(sent) == 1, f"a non-repairable failure was retried: {len(sent)} provider calls"


# ── the owner's case ─────────────────────────────────────────────────────────


async def test_groq_output_limit_rejection_heals_once_with_warning_and_record(captured) -> None:
    emitter = _Emitter()
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    sent, result = await _run(_groq_profile(), config, [_groq_max_completion_tokens(), _OK], emitter=emitter)

    assert result is _OK
    assert [c["max_output_tokens"] for c in sent] == [32000, 16384]
    _assert_at_most_one_repair(sent)

    assert len(emitter.warnings) == 1
    warning = emitter.warnings[0]
    assert warning.code == "setting_repaired"
    assert warning.user_message == "Output limit lowered to 16,384 for this model."
    assert len(warning.user_message) <= setting_rejection.REPAIR_WARNING_BUDGET

    rows = _setting_rows(captured)
    assert len(rows) == 1, captured
    payload = rows[0]["payload"]
    assert rows[0]["error_type"] == "groq.invalid_setting"
    assert payload["lifecycle"] == "new"
    assert payload["self_healed"] is True
    assert payload["provider_param"] == "max_completion_tokens"
    assert payload["provider_limit"] == 16384
    assert payload["canonical_key"] == "max_output_tokens"
    assert payload["canonical_value"] == 32000  # what was SENT, not the repaired value
    assert payload["retry"] == {"outcome": "succeeded"}
    repair = payload["repair"]
    assert (repair["action"], repair["from"], repair["to"], repair["source"]) == (
        "clamped",
        32000,
        16384,
        "provider_message",
    )
    # The stream and the record carry the SAME Adjustment (K9, provenance computed).
    assert repair["adjustment"]["provenance"] == "computed"
    assert repair["adjustment"] == warning.metadata["repair"]["adjustment"]
    assert rows[0]["request_id"] == "req-r2"


async def test_deprecated_anthropic_temperature_is_dropped_and_resent(captured) -> None:
    emitter = _Emitter()
    config = UnifiedConfig(model="claude-opus-5-5", messages=[], temperature=0.4)
    sent, result = await _run(
        _anthropic_profile(), config, [_anthropic("`temperature` is deprecated for this model."), _OK], emitter=emitter
    )
    assert result is _OK
    assert [c["temperature"] for c in sent] == [0.4, None]
    assert emitter.warnings[0].user_message == "Temperature left out; this model doesn't accept it."
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["self_healed"] is True and payload["repair"]["action"] == "dropped"


async def test_value_not_accepted_maps_to_the_nearest_stated_value(captured) -> None:
    exc = _openai(
        {
            "message": (
                "Unsupported value: 'reasoning.effort' does not support 'xhigh' with this model. "
                "Supported values are: 'low', 'medium', and 'high'."
            ),
            "type": "invalid_request_error",
            "param": "reasoning.effort",
            "code": "unsupported_value",
        }
    )
    config = UnifiedConfig(model="gpt-5.5", messages=[], reasoning_effort="xhigh")
    sent, result = await _run(_openai_profile(), config, [exc, _OK], emitter=_Emitter())
    assert result is _OK
    assert [c["reasoning_effort"] for c in sent] == ["xhigh", "high"]
    repair = _setting_rows(captured)[0]["payload"]["repair"]
    assert (repair["action"], repair["to"], repair["source"]) == ("mapped", "high", "allowed_values")


async def test_provider_facts_supply_the_limit_the_message_does_not_state(captured, monkeypatch) -> None:
    from matrx_ai import _ext

    async def facts(profile: Any) -> dict[str, Any]:
        assert profile.model_name == "claude-opus-5-5"
        return {"output_max": {"value": 128000, "source": "provider"}}

    monkeypatch.setitem(_ext._registry, setting_rejection.PARAMETER_FACTS_EXT, facts)
    # A structured above-max that states no number: the I1 facts supply it.
    exc = _openai(
        {
            "message": "max_tokens is too large for this model.",
            "type": "invalid_request_error",
            "param": "max_tokens",
            "code": "integer_above_max_value",
        }
    )
    profile = make_profile(
        model_name="claude-opus-5-5",
        wire_format="openai_chat",
        vendor="openai",
        rules={"max_output_tokens": {"provider_key": "max_tokens"}},
    )
    config = UnifiedConfig(model="claude-opus-5-5", messages=[], max_output_tokens=200000)
    sent, result = await _run(profile, config, [exc, _OK], emitter=_Emitter())
    assert result is _OK
    assert [c["max_output_tokens"] for c in sent] == [200000, 128000]
    assert _setting_rows(captured)[0]["payload"]["repair"]["source"] == "provider_facts"


# ── what is NEVER retried ────────────────────────────────────────────────────


async def test_a_non_settings_400_is_not_retried(captured) -> None:
    exc = _anthropic("messages: at least one message is required")
    config = UnifiedConfig(model="claude-opus-5-5", messages=[], temperature=0.4)
    sent, result = await _run(_anthropic_profile(), config, [exc, _OK], emitter=_Emitter())
    assert result is exc
    _assert_not_retried(sent)
    assert _setting_rows(captured) == []


async def test_a_billing_refusal_is_not_retried(captured) -> None:
    exc = _anthropic(
        "Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing "
        "to upgrade or purchase credits."
    )
    config = UnifiedConfig(model="claude-opus-5-5", messages=[], temperature=0.4)
    sent, result = await _run(_anthropic_profile(), config, [exc, _OK], emitter=_Emitter())
    assert result is exc
    _assert_not_retried(sent)
    assert _setting_rows(captured) == []


async def test_a_second_rejection_gets_no_third_attempt_and_the_honest_error(captured) -> None:
    first, second = _groq_max_completion_tokens(), _groq_max_completion_tokens()
    emitter = _Emitter()
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    sent, result = await _run(_groq_profile(), config, [first, second, _OK], emitter=emitter)

    assert result is second  # the person's honest error
    assert len(sent) == 2
    _assert_at_most_one_repair(sent)
    assert emitter.warnings == []  # nothing was healed — no "lowered" claim
    rows = _setting_rows(captured)
    assert len(rows) == 1, rows  # same request + same field: one record
    payload = rows[0]["payload"]
    assert payload["self_healed"] is False
    assert payload["retry"]["outcome"] == "rejected_again"
    assert payload["repair"]["to"] == 16384
    # The executor's second layer must not file again.
    await failure_report.report_provider_failure(second, provider="groq", model=_GROQ_MODEL, request_id="req-r2")
    assert len(_setting_rows(captured)) == 1


async def test_a_rejection_after_output_streamed_is_not_retried_and_the_record_says_so(captured) -> None:
    emitter = _Emitter()
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    exc = _groq_max_completion_tokens()
    sent, result = await _run(_groq_profile(), config, [exc, _OK], emitter=emitter, stream_on_call=1)
    assert result is exc
    _assert_not_retried(sent)
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["self_healed"] is False
    assert payload["not_retried_reason"] == "output_already_streamed"
    assert config.max_output_tokens == 32000  # nothing was changed


async def test_an_opaque_rejection_answers_through_the_safe_minimum(captured) -> None:
    """NET (2026-10-04): an opaque rejection no longer ends the request — the
    safe minimum (optional settings left out) is sent once and answers."""
    exc = _gemini_opaque()
    profile = make_profile(model_name="gemini-3-pro", wire_format="google_chat", vendor="google")
    config = UnifiedConfig(model="gemini-3-pro", messages=[], temperature=0.2)
    sent, result = await _run(profile, config, [exc, _OK], emitter=_Emitter())
    assert result is _OK
    assert [c["temperature"] for c in sent] == [0.2, None]
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["self_healed"] is True and payload["repair"]["action"] == "safe_minimum"


async def test_no_person_facing_stream_still_heals(captured) -> None:
    """A headless call (no emitter) has nothing on screen to duplicate: it heals."""
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    sent, result = await _run(_groq_profile(), config, [_groq_max_completion_tokens(), _OK], emitter=None)
    assert result is _OK and len(sent) == 2
    assert _setting_rows(captured)[0]["payload"]["self_healed"] is True


def _effort_refused_without_a_list() -> Exception:
    """A refused VALUE whose message names no accepted set (I1 facts silent too)."""
    return _openai(
        {
            "message": "Unsupported value: 'reasoning.effort' does not support 'xhigh' with this model.",
            "type": "invalid_request_error",
            "param": "reasoning.effort",
            "code": "unsupported_value",
        }
    )


def test_an_unknown_accepted_set_plans_a_drop_to_the_model_default() -> None:
    """Ruling (REGISTER, R3 lane): when a rejected value's accepted set is unknown —
    the provider's message and the I1 facts are both silent — the single retry
    DROPS that setting (the model's default applies) and warns. Never a guess at a
    value, never the person's error."""
    from matrx_ai.providers.errors import classify_provider_error

    info = classify_provider_error("openai", _effort_refused_without_a_list())
    config = UnifiedConfig(model="gpt-5.5", messages=[], reasoning_effort="xhigh")
    plan = setting_rejection.plan_setting_repair(info, profile=_openai_profile(), config=config)
    assert plan.repair is not None, plan.reason
    assert (plan.repair.action, plan.repair.new_value, plan.repair.source) == (
        "dropped",
        None,
        "accepted_values_unknown",
    )


async def test_an_unknown_accepted_set_drops_the_setting_and_the_request_goes_through(captured) -> None:
    emitter = _Emitter()
    config = UnifiedConfig(model="gpt-5.5", messages=[], reasoning_effort="xhigh")
    sent, result = await _run(_openai_profile(), config, [_effort_refused_without_a_list(), _OK], emitter=emitter)

    assert result is _OK
    _assert_unknown_set_heals(sent)
    assert [w.user_message for w in emitter.warnings] == ["Reasoning effort reset to the model default."]
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["self_healed"] is True
    assert (payload["repair"]["action"], payload["repair"]["source"]) == ("dropped", "accepted_values_unknown")


def _assert_unknown_set_heals(sent: list[dict[str, Any]]) -> None:
    assert len(sent) == 2, f"an unknown accepted set was not retried: {len(sent)} provider call(s)"
    assert [c["reasoning_effort"] for c in sent] == ["xhigh", None], sent


# ── the guards can fail ──────────────────────────────────────────────────────


async def test_planted_infinite_retry_turns_the_guard_red(monkeypatch, captured) -> None:
    async def looping(self: Any, exc: BaseException, *, streamed_before: int | None) -> bool:
        self.config.max_output_tokens = int(self.config.max_output_tokens) - 1
        return True  # always "repaired": the budget is ignored

    monkeypatch.setattr(uc._SettingsSelfHeal, "_handle", looping)
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    rejections = [_groq_max_completion_tokens() for _ in range(4)]
    sent, _ = await _run(_groq_profile(), config, [*rejections, _OK], emitter=_Emitter())
    with pytest.raises(AssertionError, match="looped"):
        _assert_at_most_one_repair(sent)


async def test_planted_retry_on_billing_error_turns_the_guard_red(monkeypatch, captured) -> None:
    async def eager(self: Any, exc: BaseException, *, streamed_before: int | None) -> bool:
        if self.repairs_used:
            return False
        self.repairs_used += 1
        return True  # retries ANY failure

    monkeypatch.setattr(uc._SettingsSelfHeal, "_handle", eager)
    exc = _anthropic(
        "Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing "
        "to upgrade or purchase credits."
    )
    config = UnifiedConfig(model="claude-opus-5-5", messages=[], temperature=0.4)
    sent, _ = await _run(_anthropic_profile(), config, [exc, _OK], emitter=_Emitter())
    with pytest.raises(AssertionError, match="retried"):
        _assert_not_retried(sent)


async def test_planted_mid_stream_retry_turns_the_guard_red(monkeypatch, captured) -> None:
    monkeypatch.setattr(uc, "_streamed_text_length", lambda: None)  # blind to the stream
    emitter = _Emitter()
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    sent, _ = await _run(
        _groq_profile(), config, [_groq_max_completion_tokens(), _OK], emitter=emitter, stream_on_call=1
    )
    with pytest.raises(AssertionError, match="retried"):
        _assert_not_retried(sent)


async def test_planted_refusal_on_an_unknown_set_turns_the_guard_red(monkeypatch, captured) -> None:
    """The pre-ruling planner (refuse when the accepted set is unknown) must fail
    the guard above: the person's request would be an error again."""
    real = setting_rejection._plan

    def refusing(info: Any, **kw: Any) -> Any:
        plan = real(info, **kw)
        if plan.repair is not None and plan.repair.source == "accepted_values_unknown":
            return setting_rejection._no("accepted_values_unknown")
        return plan

    monkeypatch.setattr(setting_rejection, "_plan", refusing)
    # The NET's safe minimum is an independent second layer that would still
    # answer; plant its absence too so this guard judges the planner alone.
    monkeypatch.setattr(setting_rejection, "plan_safe_minimum", lambda *a, **k: None)
    config = UnifiedConfig(model="gpt-5.5", messages=[], reasoning_effort="xhigh")
    sent, result = await _run(_openai_profile(), config, [_effort_refused_without_a_list(), _OK], emitter=_Emitter())
    assert isinstance(result, Exception)
    with pytest.raises(AssertionError, match="not retried"):
        _assert_unknown_set_heals(sent)


# ── I2: a live settings probe must see the provider's own answer ─────────────


async def test_a_probe_call_is_never_healed_and_the_record_says_why(captured) -> None:
    """Settings-translation I2: inside ``settings_self_heal_suppressed`` the same
    Groq rejection that heals above propagates, with ONE provider call and the K10
    record filed ``self_healed: false`` naming the probe — a healed probe would
    read as "accepted" while the cell under test is wrong."""
    from matrx_ai.providers.unified_client import settings_self_heal_suppressed

    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    with settings_self_heal_suppressed("live_probe"):
        sent, result = await _run(_groq_profile(), config, [_groq_max_completion_tokens(), _OK])

    assert isinstance(result, Exception), result
    _assert_not_retried(sent)
    rows = _setting_rows(captured)
    assert len(rows) == 1, captured
    assert rows[0]["payload"]["self_healed"] is False
    assert rows[0]["payload"]["not_retried_reason"] == "live_probe"


async def test_suppression_ends_with_its_block(captured) -> None:
    from matrx_ai.providers.unified_client import settings_self_heal_suppressed

    with settings_self_heal_suppressed("live_probe"):
        pass
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], max_output_tokens=32000)
    sent, result = await _run(_groq_profile(), config, [_groq_max_completion_tokens(), _OK])
    assert result is _OK
    assert len(sent) == 2


# ── list-valued settings: stop sequences (FIXV1, live 2026-10-04) ───────────

_STOPS = [f"END-{i}" for i in range(10)]


def _groq_stop_max_items() -> Exception:
    """Real Groq refusal, conversation fdf78037… (ops.system_error 61f93bac…)."""
    import groq

    body = {
        "error": {
            "message": (
                "'stop' : one of the following must be satisfied[('stop' : value must be a string) "
                "OR ('stop' : maximum number of items is 4)]"
            ),
            "type": "invalid_request_error",
        }
    }
    return _stainless(groq, "BadRequestError", 400, body)


def _groq_stop_profile() -> Any:
    return make_profile(
        model_name=_GROQ_MODEL,
        wire_format="groq_chat",
        vendor="groq",
        rules={"stop_sequences": {"provider_key": "stop"}},
    )


def _anthropic_stop_profile() -> Any:
    return make_profile(
        model_name="claude-haiku-4-5",
        wire_format="anthropic_chat",
        vendor="anthropic",
        rules={"stop_sequences": {}},
    )


async def test_groq_too_many_stop_sequences_heals_to_the_stated_count(captured) -> None:
    emitter = _Emitter()
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], stop_sequences=list(_STOPS))
    sent, result = await _run(_groq_stop_profile(), config, [_groq_stop_max_items(), _OK], emitter=emitter)

    assert result is _OK, result
    assert [c["stop_sequences"] for c in sent] == [_STOPS, _STOPS[:4]]
    assert emitter.warnings[0].user_message == "Stop sequences shortened to fit this model."
    rows = _setting_rows(captured)
    assert len(rows) == 1, captured
    payload = rows[0]["payload"]
    assert rows[0]["error_type"] == "groq.invalid_setting"
    assert payload["fingerprint"], payload
    assert payload["canonical_key"] == "stop_sequences"
    assert payload["provider_limit"] == 4
    assert payload["self_healed"] is True
    assert payload["repair"]["action"] == "clamped"


async def test_anthropic_whitespace_stop_sequence_is_removed_and_resent(captured) -> None:
    emitter = _Emitter()
    config = UnifiedConfig(model="claude-haiku-4-5", messages=[], stop_sequences=["   ", "END"])
    exc = _anthropic("stop_sequences: each stop sequence must contain non-whitespace")
    sent, result = await _run(_anthropic_stop_profile(), config, [exc, _OK], emitter=emitter)

    assert result is _OK, result
    assert [c["stop_sequences"] for c in sent] == [["   ", "END"], ["END"]]
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["fingerprint"] and payload["self_healed"] is True
    assert payload["canonical_key"] == "stop_sequences"


async def test_anthropic_only_whitespace_stop_sequences_are_left_out(captured) -> None:
    config = UnifiedConfig(model="claude-haiku-4-5", messages=[], stop_sequences=["   "])
    exc = _anthropic("stop_sequences: each stop sequence must contain non-whitespace")
    sent, result = await _run(_anthropic_stop_profile(), config, [exc, _OK], emitter=_Emitter())

    assert result is _OK, result
    assert sent[0]["stop_sequences"] == ["   "]
    assert not sent[1]["stop_sequences"]


# ── NET: the universal safety net (settings-translation lane NET, 2026-10-04) ─
#
# Breaks named: a settings rejection nobody catalogued returns no answer and
# lands untyped (`provider_request_failed`, no fingerprint) — the three live
# cases from the V2 verifier (Groq temperature 5, xAI `stop`, Gemini 2.5 Pro
# budget) and any NEW one. The net must answer through the safe minimum, file
# a typed fingerprinted record with suspects, never loop, and never touch
# billing / auth / content / schema errors.


class _GrpcInvalidArgument(Exception):
    """xai_sdk's refusal shape: a gRPC RpcError (code() / details())."""

    class _Code:
        name = "INVALID_ARGUMENT"

    def __init__(self, details: str) -> None:
        super().__init__(details)
        self._details = details

    def code(self) -> Any:
        return self._Code()

    def details(self) -> str:
        return self._details


def _groq_unrecognised(message: str) -> Exception:
    import groq

    return _stainless(groq, "BadRequestError", 400, {"error": {"message": message, "type": "invalid_request_error"}})


def _gemini_400(message: str) -> Exception:
    from google.genai.errors import ClientError

    return ClientError(400, {"error": {"code": 400, "message": message, "status": "INVALID_ARGUMENT"}})


def _rich_groq_config() -> Any:
    return UnifiedConfig(
        model=_GROQ_MODEL,
        messages=[],
        temperature=0.7,
        top_p=0.9,
        stop_sequences=["END"],
        reasoning_effort="high",
        max_output_tokens=4000,
    )


def _assert_answer_warning_record(result: Any, emitter: _Emitter, captured: list[dict[str, Any]]) -> dict[str, Any]:
    assert result is _OK, f"no answer: {result!r}"
    assert len(emitter.warnings) == 1, emitter.warnings
    assert emitter.warnings[0].code == "setting_repaired"
    assert len(emitter.warnings[0].user_message) <= setting_rejection.REPAIR_WARNING_BUDGET
    rows = _setting_rows(captured)
    assert len(rows) == 1, captured
    payload = rows[0]["payload"]
    assert rows[0]["error_type"].endswith(".invalid_setting")
    assert payload["self_healed"] is True
    assert isinstance(payload["fingerprint"], str) and len(payload["fingerprint"]) == 32
    return payload


async def test_live_groq_temperature_5_answers(captured) -> None:
    """Live 5b6be2fb / a492b11f: "'temperature' : number must be at most 2"."""
    emitter = _Emitter()
    config = UnifiedConfig(model=_GROQ_MODEL, messages=[], temperature=5)
    profile = make_profile(model_name=_GROQ_MODEL, wire_format="groq_chat", vendor="groq", rules={"temperature": {}})
    sent, result = await _run(
        profile, config, [_groq_unrecognised("'temperature' : number must be at most 2"), _OK], emitter=emitter
    )
    payload = _assert_answer_warning_record(result, emitter, captured)
    assert [c["temperature"] for c in sent] == [5, 2]
    assert payload["repair"]["action"] == "clamped" and payload["provider_param"] == "temperature"


async def test_live_xai_stop_on_reasoning_model_answers(captured) -> None:
    """Live b7a467eb / acf62bb1: xAI refuses `stop` on grok-4.20-0309-reasoning."""
    emitter = _Emitter()
    model = "grok-4.20-0309-reasoning"
    config = UnifiedConfig(model=model, messages=[], stop_sequences=["zz"])
    profile = make_profile(model_name=model, wire_format="xai_chat", vendor="xai", rules={"stop_sequences": {"provider_key": "stop"}})
    exc = _GrpcInvalidArgument(f"Model {model} does not support parameter stop.")
    sent, result = await _run(profile, config, [exc, _OK], emitter=emitter)
    payload = _assert_answer_warning_record(result, emitter, captured)
    assert sent[1]["stop_sequences"] in (None, [])
    assert payload["provider"] == "xai"


async def test_live_gemini_budget_range_answers(captured) -> None:
    """Live da318b6f / 3e8f93b6: the budget is clamped to Google's stated ceiling."""
    emitter = _Emitter()
    config = UnifiedConfig(model="gemini-2.5-pro", messages=[], thinking_budget=64000)
    profile = make_profile(model_name="gemini-2.5-pro", wire_format="google_chat", vendor="google")
    exc = _gemini_400("The thinking budget 64000 is invalid. Please choose a value between 128 and 32768.")
    sent, result = await _run(profile, config, [exc, _OK], emitter=emitter)
    payload = _assert_answer_warning_record(result, emitter, captured)
    assert config.thinking_budget == 32768
    assert payload["repair"]["to"] == 32768


async def test_a_planted_unknown_400_answers_through_the_safe_minimum(captured) -> None:
    emitter = _Emitter()
    config = _rich_groq_config()
    exc = _groq_unrecognised("`frobnication_window` is not compatible with nucleus settings on this deployment")
    sent, result = await _run(_groq_profile(), config, [exc, _OK], emitter=emitter)
    payload = _assert_answer_warning_record(result, emitter, captured)
    assert len(sent) == 2
    assert sent[1] == {"max_output_tokens": 4000, "temperature": None, "reasoning_effort": None, "stop_sequences": []}
    assert payload["recognizer"] == "safety_net" and payload["shape"] == "unrecognized"
    assert payload["repair"]["action"] == "safe_minimum"
    assert set(payload["repair"]["canonical_keys"]) == {"temperature", "top_p", "stop_sequences", "reasoning_effort"}
    assert payload["suspect_params"], "the fixer needs suspects"
    assert emitter.warnings[0].user_message.startswith(("4 settings left out", "Left out:"))


async def test_safe_minimum_failing_too_is_the_honest_error_and_no_third_call(captured) -> None:
    first = _groq_unrecognised("`frobnication_window` is not compatible with nucleus settings on this deployment")
    second = _groq_unrecognised("the deployment is in maintenance; try later")
    sent, result = await _run(_groq_profile(), _rich_groq_config(), [first, second, _OK], emitter=_Emitter())
    assert result is second
    _assert_at_most_one_repair(sent)
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["self_healed"] is False and payload["retry"]["kind"] == "safe_minimum"


async def test_an_unknown_400_after_streaming_is_typed_but_not_retried(captured) -> None:
    emitter = _Emitter()
    exc = _groq_unrecognised("`frobnication_window` is not compatible with nucleus settings on this deployment")
    sent, result = await _run(_groq_profile(), _rich_groq_config(), [exc, _OK], emitter=emitter, stream_on_call=1)
    assert result is exc
    _assert_not_retried(sent)
    payload = _setting_rows(captured)[0]["payload"]
    assert payload["not_retried_reason"] == "output_already_streamed"
    assert payload["fingerprint"]


@pytest.mark.parametrize(
    "exc_factory",
    [
        pytest.param(lambda: _anthropic("messages: at least one message is required"), id="content"),
        pytest.param(
            lambda: _openai({"message": "Invalid schema for response_format 'x'", "type": "invalid_request_error", "param": "response_format"}),
            id="schema",
        ),
        pytest.param(
            lambda: _openai({"message": "Your input image may contain content that is not allowed by our safety system.", "type": "invalid_request_error"}),
            id="safety",
        ),
        pytest.param(
            lambda: _anthropic("Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits."),
            id="billing",
        ),
        pytest.param(
            lambda: _stainless(__import__("openai"), "AuthenticationError", 401, {"error": {"message": "Incorrect API key provided", "type": "invalid_request_error"}}),
            id="auth",
        ),
    ],
)
async def test_the_net_never_retries_non_settings_errors(exc_factory, captured) -> None:
    exc = exc_factory()
    config = UnifiedConfig(model="claude-opus-5-5", messages=[], temperature=0.4, top_p=0.9)
    sent, result = await _run(_anthropic_profile(), config, [exc, _OK], emitter=_Emitter())
    assert result is exc
    _assert_not_retried(sent)
    assert _setting_rows(captured) == []


def test_unrecognised_prints_tell_two_refusals_apart_and_stay_stable() -> None:
    from matrx_ai.providers.errors import classify_provider_error

    def print_of(message: str) -> str:
        info = setting_rejection.net_candidate(classify_provider_error("groq", _groq_unrecognised(message)))
        assert info is not None
        return setting_rejection.build_record(info, model=_GROQ_MODEL, wire_payload={"temperature": 0.7})["fingerprint"]

    a = print_of("`frobnication_window` is not compatible with nucleus 3")
    assert a == print_of("`frobnication_window` is not compatible with nucleus 7")  # numbers blanked
    assert a != print_of("`glimmer` is out of band for this deployment")


async def test_planted_net_removed_turns_the_guard_red(monkeypatch, captured) -> None:
    """Without the net an unknown 400 is the person's error again — the guard sees it."""
    monkeypatch.setattr(setting_rejection, "net_candidate", lambda info: None)
    exc = _groq_unrecognised("`frobnication_window` is not compatible with nucleus settings on this deployment")
    sent, result = await _run(_groq_profile(), _rich_groq_config(), [exc, _OK], emitter=_Emitter())
    with pytest.raises(AssertionError, match="no answer"):
        _assert_answer_warning_record(result, _Emitter(), captured)


async def test_planted_safe_minimum_loop_turns_the_guard_red(monkeypatch, captured) -> None:
    """A seam that forgot the safe minimum was spent would call again and again."""
    real = uc._SettingsSelfHeal._handle

    async def forgetful(self: Any, exc: BaseException, *, streamed_before: int | None) -> bool:
        self.safe_min = None
        self.repairs_used = 0
        self.config.temperature = 0.7  # something to leave out again
        return await real(self, exc, streamed_before=streamed_before)

    monkeypatch.setattr(uc._SettingsSelfHeal, "_handle", forgetful)
    rej = lambda: _groq_unrecognised("`frobnication_window` is not compatible with nucleus settings")  # noqa: E731
    sent, _ = await _run(_groq_profile(), _rich_groq_config(), [rej(), rej(), rej(), _OK], emitter=_Emitter())
    with pytest.raises(AssertionError, match="looped"):
        _assert_at_most_one_repair(sent)


async def test_cerebras_validation_range_refusal_heals(captured) -> None:
    """Live 2026-10-04 probe: Cerebras answers a range refusal as code wrong_api_format."""
    import cerebras.cloud.sdk as cerebras_sdk

    body = {
        "message": "temperature: Input should be less than or equal to 2",
        "type": "invalid_request_error",
        "param": "validation_error",
        "code": "wrong_api_format",
    }
    exc = _stainless(cerebras_sdk, "BadRequestError", 400, body)
    profile = make_profile(model_name="gpt-oss-120b", wire_format="cerebras_chat", vendor="cerebras", rules={"temperature": {}})
    config = UnifiedConfig(model="gpt-oss-120b", messages=[], temperature=3)
    sent, result = await _run(profile, config, [exc, _OK], emitter=_Emitter())
    assert result is _OK
    assert [c["temperature"] for c in sent] == [3, 2]


async def test_together_model_range_refusal_heals(captured) -> None:
    """Live 2026-10-04 probe: Kimi-K3 on Together takes temperature in [0, 1]."""
    import together

    body = {"error": {"type": "Bad Request", "code": "invalid_temperature", "message": "temperature must be within [0, 1], got 2", "param": None}}
    exc = _stainless(together, "BadRequestError", 400, body)
    profile = make_profile(model_name="moonshotai/Kimi-K3", wire_format="together_chat", vendor="together", rules={"temperature": {}})
    config = UnifiedConfig(model="moonshotai/Kimi-K3", messages=[], temperature=2)
    sent, result = await _run(profile, config, [exc, _OK], emitter=_Emitter())
    assert result is _OK
    assert [c["temperature"] for c in sent] == [2, 1]


# ── R-b: an EMPTY 200 on a settings-bearing call (FUZZ-2, 2026-10-04) ──────────


def _response(text: str) -> Any:
    from types import SimpleNamespace

    from matrx_ai.config.unified_config import TextContent

    return SimpleNamespace(messages=[SimpleNamespace(content=[TextContent(text=text)])])


async def test_an_empty_200_with_settings_is_recorded_and_sent_once_more_at_the_safe_minimum(captured) -> None:
    config = UnifiedConfig(model="grok-4.3", messages=[], temperature=2.0, max_output_tokens=50)
    sent, result = await _run(_groq_profile(), config, [_response(""), _response("ok")])
    assert len(sent) == 2, sent
    assert sent[0]["temperature"] == 2.0 and sent[1]["temperature"] is None
    assert result.messages[0].content[0].text == "ok"
    rows = _setting_rows(captured)
    assert len(rows) == 1, captured
    assert "no visible output" in str(rows[0]["exc"])


async def test_an_empty_200_retried_empty_again_gets_no_third_call(captured) -> None:
    config = UnifiedConfig(model="grok-4.3", messages=[], temperature=2.0)
    sent, result = await _run(_groq_profile(), config, [_response(" "), _response("")])
    assert len(sent) == 2, sent
    assert len(_setting_rows(captured)) == 1


async def test_an_empty_200_without_settings_is_not_retried(captured) -> None:
    config = UnifiedConfig(model="grok-4.3", messages=[])
    sent, _ = await _run(_groq_profile(), config, [_response("")])
    _assert_not_retried(sent)
