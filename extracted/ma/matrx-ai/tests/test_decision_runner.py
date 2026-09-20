from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from matrx_ai.decisions import DecisionRequest, execute_decision
from matrx_ai.decisions.runner import DecisionAdmissionError
from matrx_ai.providers.typesafe import SystemOneResult


def _profile(*, interaction: str = "decision", wire_format: str = "typesafe_systemone"):
    return SimpleNamespace(
        wire_format=wire_format,
        capabilities=SimpleNamespace(interaction=interaction),
        byok_secret_key=None,
        provider_model_id="jev-1.13.0",
        base_url="https://api.typesafe.ai",
        model_name="jev-1.13.0",
        vendor="typesafe",
        offering_id="offering-1",
        resolution_route="pinned",
    )


@pytest.mark.asyncio
async def test_invalid_native_schema_refuses_before_catalog_or_transport():
    called = False

    async def resolver(*_args, **_kwargs):
        nonlocal called
        called = True
        return _profile()

    with pytest.raises(ValidationError):
        await execute_decision(
            DecisionRequest(model="jev-1.13.0", state="x", questions={}),
            profile_resolver=resolver,
        )
    assert called is False


@pytest.mark.asyncio
async def test_nondecision_profile_refuses_before_transport():
    called = False

    async def resolver(*_args, **_kwargs):
        return _profile(interaction="turn")

    async def caller(*_args, **_kwargs):
        nonlocal called
        called = True
        raise AssertionError("transport must not run")

    with pytest.raises(DecisionAdmissionError):
        await execute_decision(
            DecisionRequest(
                model="jev-1.13.0",
                state="x",
                questions={"is_safe": {"type": "noul", "instructions": "Is it safe?"}},
            ),
            profile_resolver=resolver,
            caller=caller,
        )
    assert called is False


@pytest.mark.asyncio
async def test_direct_consumer_uses_provider_model_without_http(monkeypatch):
    from matrx_ai.decisions import runner

    monkeypatch.setattr(runner, "ensure_pricing_lookup", lambda: _priced())
    monkeypatch.setattr(runner.TokenUsage, "calculate_catalog_cost", lambda *_args: 0.01)
    monkeypatch.setattr(runner, "admit_provider_call", _admission)
    captured = {}

    async def resolver(*_args, **_kwargs):
        return _profile()

    async def caller(request, **kwargs):
        captured["request"] = request
        captured["kwargs"] = kwargs
        return SystemOneResult.model_validate(
            {
                "model": "jev-1.13.0",
                "answers": {"is_safe": {"type": "noul", "noul": 0.2}},
                "usage": {"input_tokens": 3, "output_tokens": 2},
                "request_id": "provider-1",
            }
        )

    result = await execute_decision(
        DecisionRequest(
            model="jev-latest",
            state={"item": "x"},
            questions={"is_safe": {"type": "noul", "instructions": "Is it safe?"}},
        ),
        offering_id="offering-1",
        profile_resolver=resolver,
        caller=caller,
    )
    assert captured["request"].model == "jev-1.13.0"
    assert captured["kwargs"]["base_url"] == "https://api.typesafe.ai"
    assert result.request_id == "provider-1"
    assert result.usage.total_tokens == 5
    assert result.answers["is_safe"].noul == 0.2
    assert result.model_dump()["answers"]["is_safe"] == {"type": "noul", "noul": 0.2}


@pytest.mark.asyncio
async def test_pricing_failure_after_paid_response_retains_usage(monkeypatch):
    from matrx_ai.decisions import runner
    from matrx_ai.providers.errors import get_billed_usage

    monkeypatch.setattr(runner, "ensure_pricing_lookup", lambda: _priced())
    monkeypatch.setattr(runner.TokenUsage, "calculate_catalog_cost", lambda *_args: None)
    monkeypatch.setattr(runner, "admit_provider_call", _admission)

    async def resolver(*_args, **_kwargs):
        return _profile()

    async def caller(*_args, **_kwargs):
        return SystemOneResult.model_validate({
            "model": "jev-1.13.0", "answers": {"safe": {"type": "noul", "noul": 0.2}},
            "usage": {"input_tokens": 30, "output_tokens": 2}, "request_id": "paid-response",
        })

    with pytest.raises(DecisionAdmissionError) as caught:
        await execute_decision(
            DecisionRequest(model="jev-1.13.0", state="x", questions={"safe": {"type": "noul", "instructions": "Safe?"}}),
            profile_resolver=resolver, caller=caller,
        )
    billed = get_billed_usage(caught.value)
    assert billed is not None
    assert (billed.input_tokens, billed.output_tokens, billed.offering_id) == (30, 2, "offering-1")


async def _priced():
    return {"offering-1": object()}


class _Admission:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


def _admission(_profile):
    return _Admission()
