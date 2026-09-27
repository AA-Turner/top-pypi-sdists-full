"""WORKFLOW PARITY for code calls — a workflow-held mandate RUNS, it is not refused.

Until 2026-09-26 ``hold_code_call`` refused a workflow Holder ("a code call needs
an AGENT Holder to take its model and instructions from") and wrote a
``mandate_resolution_failed`` row, so binding a workflow to any code-call job
broke the job. Every test below fails on that refusal: ``hold_code_call`` raised
before any funnel was reached.

The adapter is ONE seam (``execute_ai_request``), so these tests drive the real
funnels a site calls — ``llm_to_text``, ``llm_to_pydantic``, the measured twin —
with a provider that FAILS the test if it is ever reached.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

import matrx_ai.mandates as mandates
from matrx_ai.graph_nodes import _strict_json as funnel
from matrx_ai.mandate_workflow_holder import holding_for_metadata
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.console_emitter import ConsoleEmitter


class _Summary(BaseModel):
    title: str
    points: list[str]


@pytest.fixture
def app_context():
    ctx = AppContext(
        emitter=ConsoleEmitter(label="wf-parity-test", debug=False),
        user_id="00000000-0000-4000-8000-000000000001",
        request_id="00000000-0000-4000-8000-000000000002",
        conversation_id="00000000-0000-4000-8000-000000000003",
        store=False,
        debug=False,
        snapshot=False,
    )
    token = set_app_context(ctx)
    try:
        yield ctx
    finally:
        clear_app_context(token)


@pytest.fixture(autouse=True)
def no_provider(monkeypatch):
    """A workflow-held call must never reach a provider."""

    async def _boom(*_a: Any, **_k: Any) -> Any:
        raise AssertionError("a workflow-held call reached the provider loop")

    import matrx_ai.orchestrator.executor as executor

    monkeypatch.setattr(executor, "execute_until_complete", _boom)


@pytest.fixture
def records(monkeypatch):
    captured: list[str] = []

    async def _report(*, mandate_key, consumer, exc):
        captured.append(str(exc))

    monkeypatch.setattr(mandates, "_report_resolution_failure", _report)
    return captured


class _Runner:
    def __init__(self, answer: dict[str, Any]) -> None:
        self.answer = answer
        self.calls: list[dict[str, Any]] = []

    async def __call__(self, supplied, *, correlation_key, stream):
        self.calls.append({"supplied": dict(supplied), "key": correlation_key, "stream": stream})
        return dict(self.answer)


def _install(monkeypatch, runner: _Runner | None, **extra: Any) -> list[Any]:
    finished: list[Any] = []

    async def _complete(result, variables, user_input):
        finished.append(result)

    resolution = mandates.MandateResolution(
        source=None,
        holder_type="workflow",
        workflow_id="wf-1",
        run_workflow=runner,
        complete=_complete,
        **extra,
    )

    async def _resolver(_key: str):
        return resolution

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)
    return finished


_COST = {
    "total_cost_usd": 0.0123,
    "total_input_tokens": 400,
    "total_output_tokens": 90,
    "request_count": 2,
}


async def test_workflow_holder_is_held_not_refused(monkeypatch, records) -> None:
    runner = _Runner({"output": "ok", "run_id": "r1", "cost": {}})
    _install(monkeypatch, runner)

    held = await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hi"})

    assert held.holder_type == "workflow"
    assert held.metadata["mandate_holder"]["holder_type"] == "workflow"
    assert held.metadata["mandate_holder"]["workflow_id"] == "wf-1"
    assert holding_for_metadata(held.metadata) is held.workflow
    assert records == []


async def test_text_funnel_runs_the_workflow_on_the_offered_values(
    monkeypatch, app_context, records
) -> None:
    runner = _Runner({"output": "A two-line summary.", "run_id": "r1", "cost": _COST})
    finished = _install(monkeypatch, runner)
    held = await mandates.hold_code_call(
        "x.y", consumer="t", variables={"text": "the long document"}
    )

    text = await funnel.llm_to_text(
        model=held.pick_model(),
        system=held.system,
        user=held.user_text("Summarize: the long document"),
        metadata=held.metadata,
    )
    await held.finish(text)

    assert text == "A two-line summary."
    assert runner.calls[0]["supplied"] == {"text": "the long document"}
    assert runner.calls[0]["stream"] is True  # the strict-JSON funnel streams
    # held.finish carries completion AND the workflow's measured cost.
    assert finished[0].success is True
    assert finished[0].output == "A two-line summary."
    assert finished[0].usage["total_cost_usd"] == pytest.approx(0.0123)
    assert finished[0].metadata["workflow_run_id"] == "r1"


async def test_structured_answer_validates_and_repair_retry_never_pays_twice(
    monkeypatch, app_context
) -> None:
    runner = _Runner(
        {
            "output": '{"title": "T", "points": ["a", "b"]}',
            "parsed": {"title": "T", "points": ["a", "b"]},
            "run_id": "r2",
            "cost": _COST,
        }
    )
    _install(monkeypatch, runner)
    held = await mandates.hold_code_call("x.y", consumer="t", variables={"text": "doc"})

    value = await mandates.run_held_pydantic(held, output_cls=_Summary, user="doc")

    assert value == _Summary(title="T", points=["a", "b"])
    assert len(runner.calls) == 1


async def test_bad_shape_is_a_warning_the_site_can_see_never_a_refusal(
    monkeypatch, app_context
) -> None:
    runner = _Runner(
        {
            "output": "plain text answer",
            "run_id": "r3",
            "cost": _COST,
            "warnings": ["no deliverable of the workflow settled with this job's kind 'json'"],
        }
    )
    _install(monkeypatch, runner)
    held = await mandates.hold_code_call("x.y", consumer="t", variables={"text": "doc"})

    result = await funnel.llm_to_text_measured(
        model=held.model, system="", user="doc", metadata=held.metadata
    )

    assert result.final_text == "plain text answer"
    facts = result.metadata["workflow_holder"]
    assert facts["run_id"] == "r3"
    assert any("kind 'json'" in w for w in facts["warnings"])
    # Measured callers report the workflow's real spend.
    assert result.usage.cost_usd == pytest.approx(0.0123)
    assert result.usage.input_tokens == 400


async def test_a_composed_user_turn_fills_the_one_unoffered_value(
    monkeypatch, app_context
) -> None:
    runner = _Runner({"output": "claims", "run_id": "r4", "cost": {}})
    _install(
        monkeypatch,
        runner,
        offered_values=(mandates.OfferedValueSpec(name="answer", kind="text"),),
    )
    held = await mandates.hold_code_call("x.y", consumer="t")

    await funnel.llm_to_text(
        model=held.model, system=held.system, user="The answer text.", metadata=held.metadata
    )

    assert runner.calls[0]["supplied"] == {"answer": "The answer text."}


async def test_distinct_inputs_are_distinct_runs(monkeypatch, app_context) -> None:
    runner = _Runner({"output": "x", "run_id": "r5", "cost": {}})
    _install(
        monkeypatch,
        runner,
        offered_values=(mandates.OfferedValueSpec(name="answer", kind="text"),),
    )
    held = await mandates.hold_code_call("x.y", consumer="t")

    for label in ("one", "two"):
        await funnel.llm_to_text(model=held.model, system="", user=label, metadata=held.metadata)

    assert [c["supplied"]["answer"] for c in runner.calls] == ["one", "two"]
    assert runner.calls[0]["key"] != runner.calls[1]["key"]


async def test_no_host_runner_still_refuses_in_words(monkeypatch, records) -> None:
    _install(monkeypatch, None)

    with pytest.raises(mandates.MandateResolutionUnavailable, match="no workflow runner"):
        await mandates.hold_code_call("x.y", consumer="t")
    assert len(records) == 1


async def test_a_workflow_stamp_without_its_holding_never_reaches_a_provider(app_context) -> None:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.orchestrator.executor import execute_ai_request

    orphan = {
        "mandate_key": "x.y",
        "mandate_holder": {"holder_type": "workflow", "held_call_id": "gone"},
    }
    with pytest.raises(mandates.MandateResolutionUnavailable, match="held call that owns it"):
        await execute_ai_request(
            UnifiedConfig.from_dict({"model": "workflow:wf-1", "messages": []}),
            metadata=orphan,
        )


async def test_media_deliverable_arrives_as_a_media_part(monkeypatch, app_context) -> None:
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.config.media_config import AudioContent
    from matrx_ai.orchestrator.executor import execute_ai_request

    runner = _Runner(
        {
            "output": "https://cdn.example/a.wav",
            "parsed": {"file_id": "f-1", "url": "https://cdn.example/a.wav", "mime_type": "audio/wav"},
            "run_id": "r6",
            "cost": {},
        }
    )
    _install(monkeypatch, runner)
    held = await mandates.hold_code_call("audio.x", consumer="t", variables={"text": "hello"})

    completed = await execute_ai_request(
        UnifiedConfig.from_dict({"model": held.model, "messages": [{"role": "user", "content": "hello"}]}),
        metadata=held.metadata,
    )

    parts = completed.final_response.messages[0].content
    audio = [p for p in parts if isinstance(p, AudioContent)]
    assert audio and audio[0].file_id == "f-1" and audio[0].url.endswith("a.wav")
