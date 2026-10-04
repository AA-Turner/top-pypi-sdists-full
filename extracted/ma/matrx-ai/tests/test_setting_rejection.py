"""Settings Translation R1 — a provider's SETTINGS rejection is its own typed class.

Every fixture message below is a real provider message read (SELECT only) from
``ops.ops_issue_event`` on 2026-10-01. Each settings rejection must classify as
``invalid_setting`` with a full K10 record; credit exhaustion, an empty message
list and a schema problem must NOT. ``test_planted_*`` proves the guard goes red
when the recognizer table is wrong.
"""

from __future__ import annotations

import asyncio
import re
from types import SimpleNamespace
from typing import Any

import httpx
import pytest

from matrx_ai.providers import failure_report, setting_rejection
from matrx_ai.providers.errors import classify_provider_error
from matrx_ai.providers.setting_rejection import (
    RECOGNIZERS,
    USER_MESSAGE_BUDGET,
    Recognizer,
    build_record,
    recognize,
)

_REQ = httpx.Request("POST", "https://provider.test/v1/chat/completions")


def _stainless(module: Any, cls: str, status: int, body: dict[str, Any], text: str) -> Exception:
    exc_cls = getattr(module, cls)
    return exc_cls(text, response=httpx.Response(status, request=_REQ), body=body)


def _groq_max_completion_tokens() -> Exception:
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
    return _stainless(groq, "BadRequestError", 400, body, f"Error code: 400 - {body}")


def _anthropic(message: str) -> Exception:
    import anthropic

    body = {"type": "error", "error": {"type": "invalid_request_error", "message": message}}
    return _stainless(anthropic, "BadRequestError", 400, body, f"Error code: 400 - {body}")


def _together_steps() -> Exception:
    import openai

    body = {
        "id": "oyhs8KB-2kFHot-a34f02a12eea72e1-SEA",
        "error": {
            "message": (
                "Parameter 'steps' is not supported for the selected model configuration. "
                "Please remove this parameter from your request."
            ),
            "type": "invalid_request_error",
            "param": None,
            "code": None,
        },
    }
    return _stainless(openai, "BadRequestError", 400, body, f"Error code: 400 - {body}")


def _openai_prompt_cache_key() -> Exception:
    import openai

    body = {
        "error": {
            "message": (
                "Invalid 'prompt_cache_key': string too long. Expected a string with maximum "
                "length 64, but got a string with length 70 instead."
            ),
            "type": "invalid_request_error",
            "param": "prompt_cache_key",
            "code": "string_above_max_length",
        }
    }
    return _stainless(openai, "BadRequestError", 400, body, f"Error code: 400 - {body}")


def _openai_schema() -> Exception:
    import openai

    body = {
        "error": {
            "message": "Invalid schema for response_format 'out': 'additionalProperties' is required to be supplied and to be false.",
            "type": "invalid_request_error",
            "param": "text.format.schema",
            "code": "invalid_json_schema",
        }
    }
    return _stainless(openai, "BadRequestError", 400, body, f"Error code: 400 - {body}")


def _veo_generate_audio() -> Exception:
    # google-genai raises this client-side, before any HTTP call.
    return ValueError(
        "generate_audio parameter is only supported in Gemini Enterprise Agent Platform mode, "
        "not in Gemini Developer API mode."
    )


def _gemini_opaque() -> Exception:
    from google.genai.errors import ClientError

    return ClientError(
        400,
        {"error": {"code": 400, "message": "Request contains an invalid argument.", "status": "INVALID_ARGUMENT"}},
    )


def _gemini_opaque_wrapped() -> Exception:
    # The shape stored in ops_issue_event: the JSON error inside a string.
    from google.genai.errors import ClientError

    inner = '{\n  "error": {\n    "code": 400,\n    "message": "Request contains an invalid argument.",\n    "status": "INVALID_ARGUMENT"\n  }\n}\n'
    return ClientError(400, {"message": inner, "status": "Bad Request"})


def _xai_grpc(code_name: str, details: str) -> Exception:
    # xai_sdk speaks gRPC: a refused request is a grpc.aio.AioRpcError, never an
    # HTTP SDK error. Real text, captured live 2026-10-03 (grok-4.5, effort "none").
    import grpc

    return grpc.aio.AioRpcError(
        code=getattr(grpc.StatusCode, code_name),
        initial_metadata=grpc.aio.Metadata(),
        trailing_metadata=grpc.aio.Metadata(),
        details=details,
        debug_error_string=f"{code_name}:{details}",
    )


def _gemini_thinking_level_minimal() -> Exception:
    # Real text, captured live 2026-10-03 (gemini-flash-latest, thinking_level minimal).
    from google.genai.errors import ClientError

    return ClientError(
        400,
        {
            "error": {
                "code": 400,
                "message": (
                    "Thinking level MINIMAL is not supported for this model. Please retry with "
                    "other thinking level."
                ),
                "status": "INVALID_ARGUMENT",
            }
        },
    )


# (case id, provider, exception factory, expected param, shape, limit)
SETTING_CASES = [
    ("groq.max_completion_tokens", "groq", _groq_max_completion_tokens, "max_completion_tokens", "above_max", 16384),
    ("anthropic.temperature_deprecated", "anthropic", lambda: _anthropic("`temperature` is deprecated for this model."), "temperature", "deprecated", None),
    ("together.steps", "together", _together_steps, "steps", "unsupported", None),
    ("google.veo_generate_audio", "google", _veo_generate_audio, "generate_audio", "mode_unsupported", "Gemini Enterprise Agent Platform"),
    ("openai.prompt_cache_key", "openai", _openai_prompt_cache_key, "prompt_cache_key", "string_too_long", 64),
    ("google.opaque_invalid_argument", "google", _gemini_opaque, None, "opaque", None),
    ("google.opaque_invalid_argument_wrapped", "google", _gemini_opaque_wrapped, None, "opaque", None),
    (
        "google.thinking_level_unsupported",
        "google",
        _gemini_thinking_level_minimal,
        "thinking_config.thinking_level",
        "invalid_value",
        None,
    ),
    (
        "xai.reasoning_effort_value",
        "xai",
        lambda: _xai_grpc(
            "INVALID_ARGUMENT", "This model does not support `reasoning_effort` value `none`."
        ),
        "reasoning_effort",
        "invalid_value",
        None,
    ),
]


def _groq_stop() -> Exception:
    import groq

    body = {"error": {"message": RECOGNIZER_EXAMPLES["groq.max_items"], "type": "invalid_request_error"}}
    return _stainless(groq, "BadRequestError", 400, body, f"Error code: 400 - {body}")


def _openai_compat(message: str, **extra: Any) -> Exception:
    import openai

    body = {"error": {"message": message, "type": "invalid_request_error", **extra}}
    return _stainless(openai, "BadRequestError", 400, body, f"Error code: 400 - {body}")


RECOGNIZER_EXAMPLES = {r.id: r.example for r in RECOGNIZERS}

# FIXV1 (live 2026-10-04): list-valued stop sequences, every provider's real message.
SETTING_CASES += [
    ("groq.stop_max_items", "groq", _groq_stop, "stop", "too_many_items", 4),
    (
        "moonshot.stop_array_too_long",
        "moonshot",
        lambda: _openai_compat(RECOGNIZER_EXAMPLES["openai_compat.array_too_long"]),
        "stop",
        "too_many_items",
        5,
    ),
    (
        "openai.stop_array_above_max_length",
        "openai",
        lambda: _openai_compat(
            "Invalid 'stop': array too long. Expected an array with maximum length 4, but got an "
            "array with length 10 instead.",
            param="stop",
            code="array_above_max_length",
        ),
        "stop",
        "too_many_items",
        4,
    ),
    (
        "together.max_stop_sequences",
        "together",
        lambda: _openai_compat(RECOGNIZER_EXAMPLES["together.max_stop_sequences"]),
        "stop",
        "too_many_items",
        4,
    ),
    (
        "cerebras.stop_list_at_most",
        "cerebras",
        lambda: _openai_compat(
            RECOGNIZER_EXAMPLES["cerebras.list_at_most"], param="validation_error", code="wrong_api_format"
        ),
        "stop",
        "too_many_items",
        4,
    ),
    (
        "anthropic.stop_sequence_whitespace",
        "anthropic",
        lambda: _anthropic("stop_sequences: each stop sequence must contain non-whitespace"),
        "stop_sequences",
        "invalid_item",
        None,
    ),
]

# (case id, provider, exception factory) — bad requests that are NOT settings.
NON_SETTING_CASES = [
    (
        "anthropic.credit_exhausted",
        "anthropic",
        lambda: _anthropic(
            "Your credit balance is too low to access the Anthropic API. Please go to Plans & "
            "Billing to upgrade or purchase credits."
        ),
    ),
    ("anthropic.empty_messages", "anthropic", lambda: _anthropic("messages: at least one message is required")),
    ("openai.schema", "openai", _openai_schema),
    ("google.plain_invalid_argument", "google", lambda: Exception("400 INVALID_ARGUMENT: Invalid request")),
    (
        "google.mutually_exclusive_inputs",
        "google",
        lambda: ValueError("Source and prompt/image/video are mutually exclusive. Please only use source."),
    ),
]


def _assert_settings_cases(cases: list[tuple]) -> None:
    for case_id, provider, factory, param, shape, limit in cases:
        info = classify_provider_error(provider, factory())
        assert info.error_type == "invalid_setting", f"{case_id}: {info.error_type}"
        rej = info.details["setting_rejection"]
        assert rej["provider"] == provider, case_id
        assert rej["provider_param"] == param, case_id
        assert rej["shape"] == shape, case_id
        assert rej["provider_limit"] == limit, case_id
        assert info.details["provider"] == provider, case_id  # → issue key <provider>.invalid_setting
        assert info.is_retryable is False


def _assert_non_settings_cases(cases: list[tuple]) -> None:
    for case_id, provider, factory in cases:
        info = classify_provider_error(provider, factory())
        assert info.error_type != "invalid_setting", f"{case_id} misclassified as a settings rejection"


@pytest.mark.parametrize("case", SETTING_CASES, ids=[c[0] for c in SETTING_CASES])
def test_real_settings_rejections_classify(case: tuple) -> None:
    _assert_settings_cases([case])


@pytest.mark.parametrize("case", NON_SETTING_CASES, ids=[c[0] for c in NON_SETTING_CASES])
def test_other_bad_requests_are_not_settings(case: tuple) -> None:
    _assert_non_settings_cases([case])


def test_xai_grpc_failures_keep_their_typed_class() -> None:
    """A gRPC status is a typed answer — never laundered into ``unknown_error``."""
    unavailable = classify_provider_error("xai", _xai_grpc("UNAVAILABLE", "upstream connect error"))
    assert unavailable.error_type != "unknown_error"
    assert unavailable.is_retryable is True
    auth = classify_provider_error("xai", _xai_grpc("UNAUTHENTICATED", "Incorrect API key provided"))
    assert auth.error_type != "unknown_error"
    assert auth.is_retryable is False
    plain = classify_provider_error("xai", _xai_grpc("INVALID_ARGUMENT", "messages must not be empty"))
    assert plain.error_type == "invalid_request"


def test_credit_exhaustion_stays_billing() -> None:
    info = classify_provider_error("anthropic", NON_SETTING_CASES[0][2]())
    assert info.error_type == "billing_error"


def test_every_recognizer_row_matches_its_own_real_example() -> None:
    for row in RECOGNIZERS:
        found = recognize(row.providers[0], row.example, {"message": row.example})
        assert found is not None, row.id
        assert found.recognizer == row.id, (row.id, found.recognizer)


def test_person_sees_a_short_honest_sentence_not_the_provider_text() -> None:
    for case_id, provider, factory, *_ in SETTING_CASES:
        info = classify_provider_error(provider, factory())
        assert len(info.user_message) <= USER_MESSAGE_BUDGET, case_id
        raw = info.details["setting_rejection"]["provider_message"]
        assert raw not in info.user_message, case_id
        assert "`" not in info.user_message and "_" not in info.user_message, case_id


# ── the K10 record ───────────────────────────────────────────────────────────


def _profile(provider_key: str = "max_completion_tokens", canonical: str = "max_output_tokens") -> Any:
    rule = SimpleNamespace(provider_key=provider_key, cell_id="cell-7", cell_version=3)
    return SimpleNamespace(
        model_name="qwen/qwen3.8-27b",
        model_id="model-uuid",
        offering_id="offering-uuid",
        controls=SimpleNamespace(rules={canonical: rule}),
    )


def test_groq_record_carries_the_full_k10_payload() -> None:
    info = classify_provider_error("groq", _groq_max_completion_tokens())
    config = SimpleNamespace(max_output_tokens=32000)
    record = build_record(
        info,
        model="qwen/qwen3.8-27b",
        profile=_profile(),
        config=config,
        wire_payload={"model": "qwen/qwen3.8-27b", "max_completion_tokens": 32000, "messages": []},
        request_snapshot_id="snap-1",
        modality="text",
    )
    assert record["provider"] == "groq"
    assert record["provider_param"] == "max_completion_tokens"
    assert record["provider_limit"] == 16384
    assert record["sent_value"] == 32000 and record["sent_value_found"] is True
    assert record["canonical_key"] == "max_output_tokens"
    assert record["canonical_value"] == 32000
    assert record["canonical_state"] == "value"
    assert record["request_snapshot_id"] == "snap-1"
    assert (record["cell_id"], record["cell_version"]) == ("cell-7", 3)
    assert record["offering_id"] == "offering-uuid" and record["model_id"] == "model-uuid"
    assert record["modality"] == "text"
    assert record["lifecycle"] == "new"
    assert re.fullmatch(r"[0-9a-f]{32}", record["fingerprint"])
    for key in (
        "provider", "offering_id", "model_id", "model_name", "profile_id", "modality",
        "provider_param", "provider_code", "provider_message", "sent_value", "canonical_key",
        "canonical_value", "canonical_state", "provider_limit", "request_snapshot_id",
        "cell_id", "cell_version", "fingerprint", "suspect_params",
    ):
        assert key in record, key


@pytest.mark.parametrize("case", SETTING_CASES, ids=[c[0] for c in SETTING_CASES])
def test_every_case_builds_a_record(case: tuple) -> None:
    case_id, provider, factory, param, _shape, limit = case
    info = classify_provider_error(provider, factory())
    wire: Any = None
    if param:  # the wire as a provider SDK receives it: a dotted param is nested
        wire = "sent"
        for part in reversed(param.split(".")):
            wire = {part: wire}
    record = build_record(info, model="m", wire_payload=wire)
    assert record["provider_param"] == param
    assert record["provider_limit"] == limit
    assert record["lifecycle"] == "new"
    if param:
        assert record["sent_value"] == "sent"


def test_fingerprint_is_stable_and_separates_defects() -> None:
    a = build_record(classify_provider_error("groq", _groq_max_completion_tokens()), model="m1")
    b = build_record(classify_provider_error("groq", _groq_max_completion_tokens()), model="m1")
    c = build_record(classify_provider_error("groq", _groq_max_completion_tokens()), model="m2")
    assert a["fingerprint"] == b["fingerprint"] != c["fingerprint"]


def test_sent_value_found_in_nested_media_kwargs() -> None:
    info = classify_provider_error("google", _veo_generate_audio())
    kwargs = {"model": "veo", "config": SimpleNamespace(generate_audio=True, duration_seconds=8)}
    record = build_record(info, model="veo-3.1-generate-preview", wire_payload=kwargs, modality="video")
    assert record["sent_value"] is True
    assert record["canonical_state"] is None  # no canonical key derivable without a profile


def test_opaque_rejection_names_suspects_against_last_passing_call() -> None:
    setting_rejection.reset_passing_memory()
    info = classify_provider_error("google", _gemini_opaque())
    no_memory = build_record(info, model="gemini-3.8-flash", wire_payload={"temperature": 0.2})
    # NET: no passing call to compare against → EVERY setting on the wire is a
    # suspect (never an empty list the fixer cannot act on).
    assert no_memory["suspect_params"] == ["temperature"]
    assert no_memory["suspect_params_source"] == "setting_keys_on_wire"

    setting_rejection.remember_passing_wire(
        "google", "gemini-3.8-flash", {"contents": ["x"], "config": {"temperature": 0.2, "top_k": 40}}
    )
    record = build_record(
        info,
        model="gemini-3.8-flash",
        wire_payload={"contents": ["y"], "config": {"temperature": 0.2, "top_k": 40, "media_resolution": "ultra"}},
    )
    assert record["suspect_params"] == ["config.media_resolution"]
    assert record["suspect_params_source"] == "last_passing_in_process"
    setting_rejection.reset_passing_memory()


# ── the one store of record ──────────────────────────────────────────────────


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def fake_capture(exc: BaseException, *, kind: str, **fields: Any) -> None:
        rows.append({"kind": kind, **fields})

    import matrx_connect.streaming.error_capture as ec

    monkeypatch.setattr(ec, "capture_error", fake_capture)
    failure_report.reset_alarm_memory()
    yield rows
    failure_report.reset_alarm_memory()


def test_door_files_one_record_per_rejection(captured: list[dict[str, Any]]) -> None:
    exc = _groq_max_completion_tokens()

    async def run() -> None:
        # dispatch seam, then the orchestrator's second layer: one row.
        await failure_report.report_provider_failure(
            exc,
            provider="groq",
            model="qwen/qwen3.8-27b",
            setting_context={"profile": _profile()},
            request_id="r1",
        )
        await failure_report.report_provider_failure(exc, provider="groq", model="qwen/qwen3.8-27b", request_id="r1")
        # A second exception for the SAME request and defect: still one row.
        await failure_report.report_provider_failure(
            _groq_max_completion_tokens(), provider="groq", model="qwen/qwen3.8-27b", request_id="r1"
        )

    asyncio.run(run())
    setting_rows = [r for r in captured if r["kind"] == "provider_setting_rejected"]
    assert len(setting_rows) == 1, captured
    row = setting_rows[0]
    assert row["error_type"] == "groq.invalid_setting"
    assert row["payload"]["lifecycle"] == "new"
    assert row["payload"]["provider_param"] == "max_completion_tokens"
    assert row["payload"]["canonical_key"] == "max_output_tokens"


def test_dispatch_seam_passes_profile_and_modality(captured: list[dict[str, Any]]) -> None:
    asyncio.run(
        failure_report.report_dispatch_failure(
            _groq_max_completion_tokens(),
            provider="groq",
            model="qwen/qwen3.8-27b",
            profile=_profile(),
            config=SimpleNamespace(max_output_tokens=32000),
            modality="text",
        )
    )
    rows = [r for r in captured if r["kind"] == "provider_setting_rejected"]
    assert len(rows) == 1
    assert rows[0]["payload"]["offering_id"] == "offering-uuid"
    assert rows[0]["payload"]["modality"] == "text"
    assert rows[0]["payload"]["canonical_value"] == 32000


def test_non_setting_failure_files_no_setting_record(captured: list[dict[str, Any]]) -> None:
    asyncio.run(
        failure_report.report_provider_failure(
            _anthropic("messages: at least one message is required"), provider="anthropic"
        )
    )
    assert not [r for r in captured if r["kind"] == "provider_setting_rejected"]


def test_orchestrator_writes_no_generic_row_for_a_settings_rejection(captured: list[dict[str, Any]]) -> None:
    from matrx_ai.orchestrator import executor

    exc = _groq_max_completion_tokens()
    info = classify_provider_error("groq", exc)
    request = SimpleNamespace(
        request_id="r9", conversation_id=None, config=SimpleNamespace(model="qwen/qwen3.8-27b", max_output_tokens=32000)
    )
    asyncio.run(
        executor._capture_terminal_provider_failure(
            exc,
            exec_ctx=SimpleNamespace(user_id=None, request_id="r9", conversation_id=None),
            current_request=request,
            error_info=info,
            provider="groq",
            iteration=0,
            retry_attempt=0,
        )
    )
    kinds = [r["kind"] for r in captured]
    assert kinds == ["provider_setting_rejected"], kinds
    assert captured[0]["payload"]["provider_param"] == "max_completion_tokens"
    assert captured[0]["request_id"] == "r9"


# ── the guard can fail ───────────────────────────────────────────────────────


def test_planted_greedy_recognizer_turns_the_guard_red(monkeypatch: pytest.MonkeyPatch) -> None:
    """A recognizer row that also swallows 'empty messages' must fail the negative guard."""
    greedy = Recognizer(
        id="planted.greedy",
        providers=("anthropic",),
        pattern=re.compile(r"(?P<param>messages|credit)"),
        shape="unsupported",
        example="messages",
        param=None,
    )
    # The planted row names a content param, which the non-setting filter refuses;
    # plant the filter's removal too so the mis-classification really reaches it.
    monkeypatch.setattr(setting_rejection, "RECOGNIZERS", (greedy, *RECOGNIZERS))
    monkeypatch.setattr(setting_rejection, "_NON_SETTING_PARAM_PREFIXES", ())
    with pytest.raises(AssertionError, match="misclassified"):
        _assert_non_settings_cases(NON_SETTING_CASES)


def test_planted_missing_row_turns_the_guard_red(monkeypatch: pytest.MonkeyPatch) -> None:
    """Dropping the Anthropic 'deprecated' row must fail the positive guard."""
    monkeypatch.setattr(
        setting_rejection,
        "RECOGNIZERS",
        tuple(r for r in RECOGNIZERS if r.id != "anthropic.deprecated"),
    )
    with pytest.raises(AssertionError):
        _assert_settings_cases(SETTING_CASES)


def test_seam_reads_the_running_turn(captured: list[dict[str, Any]]) -> None:
    """Inside an orchestrated turn the seam links the snapshot and reads the sent wire value."""
    from matrx_ai.orchestrator.execution_state import (
        ExecutionState,
        clear_execution_state,
        set_execution_state,
    )

    state = ExecutionState()
    state.snapshot_payload = {"model": "qwen/qwen3.8-27b", "max_completion_tokens": 32000, "messages": []}
    state.failure_snapshot_id = "11111111-2222-3333-4444-555555555555"
    state.current_request = SimpleNamespace(config=SimpleNamespace(max_output_tokens=32000))
    token = set_execution_state(state)
    try:
        asyncio.run(
            failure_report.report_dispatch_failure(
                _groq_max_completion_tokens(),
                provider="groq",
                model="qwen/qwen3.8-27b",
                profile=_profile(),
                modality="text",
            )
        )
    finally:
        clear_execution_state(token)
    rows = [r for r in captured if r["kind"] == "provider_setting_rejected"]
    assert len(rows) == 1
    payload = rows[0]["payload"]
    assert payload["request_snapshot_id"] == "11111111-2222-3333-4444-555555555555"
    assert payload["sent_value"] == 32000
    assert payload["canonical_value"] == 32000 and payload["canonical_state"] == "value"
    assert payload["provider_limit"] == 16384


# ── R1 gaps (settings-translation R3 lane) ───────────────────────────────────
#
# Found by the I2 probe on the clone: probe- and dispatch-filed records carried
# no sent_value and no cell, and named the DECLARED-DROP legacy key
# ``max_completion_tokens`` as the canonical key (its identity name equals the
# wire field), so the record's fingerprint disagreed with the probe's and no
# cell could be found for it.


def _groq_cells_profile() -> Any:
    from matrx_ai.catalog.models import CellRef
    from matrx_ai.testing.profile_factory import make_profile

    profile = make_profile(
        model_name="qwen/qwen3.8-27b",
        wire_format="groq_chat",
        vendor="groq",
        rules={
            # The clone's real pair for this Groq offering, in the order compiled.
            "max_completion_tokens": {"drop": True, "why": "legacy alias of max_output_tokens"},
            "max_output_tokens": {"provider_key": "max_completion_tokens", "clamp": {"max": 32000}},
        },
    )
    cells = {
        "max_output_tokens": CellRef(cell_id="f18d5da2-cell", layer="offering", state="proposed", version=5),
    }
    return profile.model_copy(update={"controls": profile.controls.model_copy(update={"cells": cells})})


def test_a_declared_drop_never_claims_the_wire_field_it_shares_a_name_with() -> None:
    from matrx_ai.providers.setting_rejection import canonical_key_for

    assert canonical_key_for("max_completion_tokens", _groq_cells_profile().controls) == "max_output_tokens"


def test_a_call_outside_an_orchestrated_turn_still_records_what_it_sent_and_which_cell() -> None:
    """No ExecutionState (a probe, a bare dispatch): the wire value comes from the
    outbound pass that produced it, the cell and version from the K9 provenance."""
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.providers.outbound_params import resolve_outbound_params

    profile = _groq_cells_profile()
    config = UnifiedConfig(model="qwen/qwen3.8-27b", messages=[], max_output_tokens=32000)
    sent = resolve_outbound_params(config, profile.controls)
    assert sent["max_completion_tokens"] == 32000

    info = classify_provider_error("groq", _groq_max_completion_tokens())
    record = build_record(info, model="qwen/qwen3.8-27b", profile=profile, config=config, wire_payload=None)
    assert record["canonical_key"] == "max_output_tokens"
    assert (record["sent_value"], record["sent_value_found"]) == (32000, True)
    assert record["sent_value_source"] == "outbound_pass"
    assert (record["cell_id"], record["cell_version"]) == ("f18d5da2-cell", 5)


def test_the_probe_and_the_record_agree_on_the_fingerprint() -> None:
    from matrx_ai.providers.setting_rejection import canonical_key_for, fingerprint

    profile = _groq_cells_profile()
    info = classify_provider_error("groq", _groq_max_completion_tokens())
    record = build_record(info, model="qwen/qwen3.8-27b", profile=profile)
    probe_print = fingerprint(  # live_probe.send_probe's own formula
        provider="groq",
        model_or_profile="qwen/qwen3.8-27b",
        provider_param="max_completion_tokens",
        canonical_key=canonical_key_for("max_completion_tokens", profile.controls) or "max_output_tokens",
        shape="above_max",
    )
    assert record["fingerprint"] == probe_print
