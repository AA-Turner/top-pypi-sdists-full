"""RunResult envelope parsing, extra-field round-trip, and unwrap (SPEC 3.3)."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from getanyapi import AnyAPIError, BareRunResult, NotFoundError, RunResult, unwrap
from getanyapi.types import OutputFound, OutputNotFound


def test_found_envelope_parses_with_alias_and_extra() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": True, "data": {"a": 1, "_extra": "x"}},
            "provider": "AnyAPI",
            "costUsd": 0.5,
            "items": 3,
            "replayed": False,
            "hint": "trimmed",
            "topExtra": "kept",
        }
    )
    assert isinstance(result.output, OutputFound)
    assert result.output.found is True
    assert result.output.data == {"a": 1, "_extra": "x"}
    assert result.cost_usd == 0.5
    assert result.items == 3
    assert result.hint == "trimmed"
    assert result.provider == "AnyAPI"
    # Unknown top-level keys round-trip via model_extra (open root).
    assert result.model_extra == {"topExtra": "kept"}


def test_not_found_envelope() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": False, "data": None},
            "provider": "AnyAPI",
            "costUsd": 0.0,
            "items": 0,
            "replayed": False,
        }
    )
    assert isinstance(result.output, OutputNotFound)
    assert result.output.found is False
    assert result.output.data is None
    assert result.items == 0
    assert result.hint is None


def test_not_found_envelope_carries_its_reason() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": False, "data": None, "reason": "suspended"},
            "provider": "AnyAPI",
            "costUsd": 0.0,
            "items": 0,
            "replayed": False,
        }
    )
    assert isinstance(result.output, OutputNotFound)
    assert result.output.reason == "suspended"


def test_unwrap_returns_data_when_found() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": True, "data": {"x": 1}},
            "provider": "AnyAPI",
            "costUsd": 0.1,
            "items": 1,
            "replayed": False,
        }
    )
    assert unwrap(result) == {"x": 1}


def test_unwrap_raises_not_found() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": False, "data": None},
            "provider": "AnyAPI",
            "costUsd": 0.0,
            "items": 0,
            "replayed": False,
        }
    )
    with pytest.raises(NotFoundError) as exc:
        unwrap(result)
    assert "no matching result was found" in str(exc.value)
    assert exc.value.status == 404


def test_replay_metadata_parses_with_aliases() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": True, "data": {"x": 1}},
            "provider": "AnyAPI",
            "costUsd": 0.1,
            "items": 1,
            "replayed": True,
            "resultId": "res_abc",
            "jqError": "jq: compile error",
        }
    )
    assert result.replayed is True
    assert result.result_id == "res_abc"
    assert result.jq_error == "jq: compile error"
    # The wire shape round-trips unchanged.
    dumped = result.model_dump(by_alias=True)
    assert dumped["replayed"] is True
    assert dumped["resultId"] == "res_abc"
    assert dumped["jqError"] == "jq: compile error"


def test_fresh_run_defaults_the_optional_replay_metadata() -> None:
    result = RunResult[dict[str, Any]].model_validate(
        {
            "output": {"found": True, "data": {"x": 1}},
            "provider": "AnyAPI",
            "costUsd": 0.1,
            "items": 1,
            "replayed": False,
        }
    )
    assert result.replayed is False
    assert result.result_id is None
    assert result.jq_error is None


def test_unwrap_raises_when_replayed_output_was_not_retained() -> None:
    # An idempotent replay can outlive its stored payload (24h TTL, or a payload over
    # the size cap): the metadata is intact and `output` is legally null.
    # model_construct bypasses validation to build exactly that wire state.
    result: RunResult[dict[str, Any]] = RunResult[dict[str, Any]].model_construct(
        output=None,
        provider="AnyAPI",
        cost_usd=0.001,
        items=3,
        replayed=True,
    )
    with pytest.raises(AnyAPIError) as exc:
        unwrap(result)
    message = str(exc.value)
    assert "was not retained" in message
    assert "idempotent replay" in message
    assert "without the idempotency key" in message
    # Not an empty upstream result: a ResultNotFoundError handler must not swallow it.
    assert not isinstance(exc.value, NotFoundError)


def test_unwrap_raises_on_a_bare_replay_without_a_retained_output() -> None:
    result: BareRunResult[Any] = BareRunResult[Any].model_construct(
        output=None,
        provider="AnyAPI",
        cost_usd=0.001,
        items=3,
        replayed=True,
    )
    with pytest.raises(AnyAPIError) as exc:
        unwrap(result)
    assert "was not retained" in str(exc.value)
    assert not isinstance(exc.value, NotFoundError)


@pytest.mark.parametrize("model", [RunResult, BareRunResult])
def test_parsing_a_null_output_raises_the_not_retained_error(model: Any) -> None:
    # The gateway sends `output` on every success envelope, but a replay can outlive its
    # stored payload, so `{"output": null, ...}` is a legal body. Neither declared output
    # type admits None, so the guard must fire BEFORE pydantic reports a shape mismatch:
    # a raw ValidationError never mentions idempotency.
    with pytest.raises(AnyAPIError) as exc:
        model[dict[str, Any]].model_validate(
            {
                "output": None,
                "provider": "AnyAPI",
                "costUsd": 0.001,
                "items": 3,
                "replayed": True,
            }
        )
    message = str(exc.value)
    assert "was not retained" in message
    assert "idempotent replay" in message
    assert "without the idempotency key" in message
    assert exc.value.status == 200
    assert not isinstance(exc.value, NotFoundError)


@pytest.mark.parametrize("model", [RunResult, BareRunResult])
def test_parsing_an_absent_output_raises_the_not_retained_error(model: Any) -> None:
    # SPEC 2.3 treats a missing `output` exactly like a null one, in both languages.
    with pytest.raises(AnyAPIError) as exc:
        model[dict[str, Any]].model_validate(
            {"provider": "AnyAPI", "costUsd": 0.001, "items": 3, "replayed": True}
        )
    assert "was not retained" in str(exc.value)


@pytest.mark.parametrize("model", [RunResult, BareRunResult])
def test_items_is_required_on_both_envelopes(model: Any) -> None:
    # `items` carries no omitempty on the gateway struct, so a body without it is
    # malformed rather than an "input-priced SKU" signal.
    with pytest.raises(ValidationError) as exc:
        model[dict[str, Any]].model_validate(
            {
                "output": {"found": True, "data": {"x": 1}},
                "provider": "AnyAPI",
                "costUsd": 0.1,
                "replayed": False,
            }
        )
    assert "items" in str(exc.value)
