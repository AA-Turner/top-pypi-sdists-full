"""ai.judge.resolve — picks among gathered arms, names holes, writes the ledger, refuses unbound.

Only the provider boundary (the strict-JSON funnel) and the ledger's host model
are doubled; the node body, the mandate hold and ``record_verdict`` run for real.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.types.context import ChannelView, NodeExecutionContext
from matrx_graph.types.result import Failure, Success
from pydantic import BaseModel

from matrx_ai.code_call_mandate_keys import ARM_RESOLVER_MANDATE
from matrx_ai.graph_nodes.resolve_action import (
    ArmResolverError,
    GatheredHole,
    ResolveArmsInput,
    lay_out_arms,
    resolve_arms,
)
from matrx_ai.testing.holders import install_inline_holders

RUN_ID = "0b6c1f7e-3a1d-4c55-9a8e-6f1f2b9d7c01"
ORG_ID = "5dc930e9-bd65-44a1-8369-af773f6e1a5b"
USER_ID = "7d0f8a3e-1b2c-4d5e-8f90-a1b2c3d4e5f6"


class _Emitter:
    def __getattr__(self, _name: str) -> Any:
        async def _noop(*_a: Any, **_k: Any) -> None:
            return None

        return _noop


def _ctx() -> NodeExecutionContext:
    from matrx_connect.context.app_context import AppContext

    return NodeExecutionContext(
        app=AppContext(
            emitter=_Emitter(),
            user_id=USER_ID,
            is_authenticated=True,
            conversation_id="c",
            request_id="r",
            organization_id=ORG_ID,
        ),
        run_id=RUN_ID,
        thread_id=RUN_ID,
        node_id="n_resolve",
        step=3,
        attempt=1,
        channels=ChannelView(_values={}, _pending_writes=[]),
        checkpointer=None,
    )


class _FakeLedger:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def create(self, **row: Any) -> Any:
        self.rows.append(row)

        class _Row:
            id = "11111111-2222-3333-4444-555555555555"

        return _Row()


@pytest.fixture
def ledger(monkeypatch) -> _FakeLedger:
    fake = _FakeLedger()
    monkeypatch.setattr("matrx_ai.evaluators.ledger._model", lambda: fake)
    return fake


def _bind_holder(monkeypatch) -> None:
    install_inline_holders(
        monkeypatch,
        {
            ARM_RESOLVER_MANDATE: {
                "model": "holder-model",
                "messages": [
                    {"role": "system", "content": "You resolve arms."},
                    {"role": "user", "content": "Job: {{job}}\nArms: {{arms}}"},
                ],
                "variables": [
                    {"name": "job", "defaultValue": ""},
                    {"name": "arms", "defaultValue": ""},
                ],
            }
        },
    )


def _answer(monkeypatch, payload: dict[str, Any], captured: dict[str, Any] | None = None) -> None:
    async def fake(*, output_cls: type[BaseModel], **kwargs: Any) -> BaseModel:
        if captured is not None:
            captured.update(kwargs)
        return output_cls.model_validate(payload)

    monkeypatch.setattr("matrx_ai.graph_nodes._strict_json.llm_to_pydantic", fake)


def _three_arms(**extra: Any) -> ResolveArmsInput:
    return ResolveArmsInput(
        job="Write a one-line brand tagline for a dental clinic.",
        criteria=["memorable", "names the benefit"],
        arms=["Smile brighter.", "Teeth: handled.", "Your smile, our craft."],
        arm_labels=["chain: researcher→writer", "chain: writer only", "multi-job agent"],
        **extra,
    )


async def test_picks_a_winner_from_three_arms_and_writes_the_ledger(monkeypatch, ledger):
    _bind_holder(monkeypatch)
    captured: dict[str, Any] = {}
    _answer(
        monkeypatch,
        {
            "verdict": "pick",
            "winner_arm_index": 2,
            "reasons": ["Names the craft benefit", "Most memorable"],
            "confidence": 0.8,
            "arm_assessments": [
                {"arm_index": 0, "rank": 2},
                {"arm_index": 1, "rank": 3},
                {"arm_index": 2, "rank": 1},
            ],
        },
        captured,
    )

    result = await resolve_arms(_ctx(), _three_arms())

    assert isinstance(result, Success)
    out = result.result
    assert out.verdict == "pick"
    assert out.winner_arm_index == 2
    assert out.winner_label == "multi-job agent"
    assert out.winner_result == "Your smile, our craft."
    assert [a.arm_index for a in out.arm_assessments] == [2, 0, 1]
    assert out.ledger_id == "11111111-2222-3333-4444-555555555555"
    # The judge ran on the mandate Holder's model and authored user turn.
    assert captured["model"] == "holder-model"
    assert "Your smile, our craft." in captured["user"]

    (row,) = ledger.rows
    assert row["judge_key"] == ARM_RESOLVER_MANDATE
    assert row["mode"] == "comparative"
    assert row["verdict"] == "pick"
    assert row["subject_ref_type"] == "workflow_run"
    assert row["subject_ref_id"] == RUN_ID
    assert row["organization_id"] == ORG_ID
    assert row["created_by"] == USER_ID
    assert row["invocation"]["workflow_run_id"] == RUN_ID
    assert row["invocation"]["node_id"] == "n_resolve"
    winners = [c for c in row["candidate_refs"] if c.get("winner")]
    assert [c["arm_index"] for c in winners] == [2]


async def test_a_hole_is_named_and_never_shifts_the_arms(monkeypatch, ledger):
    _bind_holder(monkeypatch)
    captured: dict[str, Any] = {}
    _answer(
        monkeypatch,
        {"verdict": "pick", "winner_arm_index": 2, "reasons": ["Only strong one"], "confidence": 0.6},
        captured,
    )
    # Arm 1 failed: gather compacted the values and reported the hole.
    inputs = ResolveArmsInput(
        job="Tagline",
        arms=["Smile brighter.", "Your smile, our craft."],
        item_indexes=[0, 2],
        holes=[GatheredHole(item_index=1, status="skipped")],
        expected=3,
        arm_labels=["A", "B", "C"],
    )

    result = await resolve_arms(_ctx(), inputs)

    out = result.result
    assert out.winner_label == "C"
    assert out.winner_result == "Your smile, our craft."
    assert [(m.arm_index, m.label, m.status) for m in out.missing_arms] == [(1, "B", "skipped")]
    assert out.arm_count == 3 and out.judged_count == 2
    refs = ledger.rows[0]["candidate_refs"]
    assert [(r["arm_index"], r["present"]) for r in refs] == [(0, True), (1, False), (2, True)]


def test_an_arm_missing_without_a_hole_is_still_named():
    present, missing, count = lay_out_arms(
        ResolveArmsInput(job="j", arms=["x"], item_indexes=[0], expected=2)
    )
    assert count == 2
    assert [a["arm_index"] for a in present] == [0]
    assert [(m.arm_index, m.status) for m in missing] == [(1, "missing")]


async def test_refuses_clearly_when_the_mandate_is_unbound(monkeypatch, ledger):
    install_inline_holders(monkeypatch, {})  # resolver knows no Holder for the key

    async def must_not_run(**_kw: Any) -> Any:
        raise AssertionError("an unbound judge must never reach a model")

    monkeypatch.setattr("matrx_ai.graph_nodes._strict_json.llm_to_pydantic", must_not_run)

    result = await resolve_arms(_ctx(), _three_arms())

    assert isinstance(result, Failure)
    assert result.error.code == "judge_unbound"
    assert ARM_RESOLVER_MANDATE in result.error.message
    assert ledger.rows == []


async def test_a_pick_of_an_arm_it_was_not_shown_raises(monkeypatch, ledger):
    _bind_holder(monkeypatch)
    _answer(
        monkeypatch,
        {"verdict": "pick", "winner_arm_index": 1, "reasons": ["x"], "confidence": 0.5},
    )
    inputs = ResolveArmsInput(
        job="j", arms=["a", "c"], item_indexes=[0, 2], holes=[GatheredHole(item_index=1)]
    )
    with pytest.raises(ArmResolverError, match="not one of the arms"):
        await resolve_arms(_ctx(), inputs)
    assert ledger.rows == []


async def test_merge_returns_the_merged_result_in_the_arms_form(monkeypatch, ledger):
    _bind_holder(monkeypatch)
    _answer(
        monkeypatch,
        {
            "verdict": "merge",
            "reasons": ["A has the name, B has the benefit"],
            "confidence": 0.7,
            "merged_result": '{"tagline": "Bright smiles, crafted."}',
        },
    )
    inputs = ResolveArmsInput(job="j", arms=[{"tagline": "a"}, {"tagline": "b"}])

    out = (await resolve_arms(_ctx(), inputs)).result

    assert out.verdict == "merge"
    assert out.winner_arm_index is None
    assert out.merged_result == {"tagline": "Bright smiles, crafted."}
    assert ledger.rows[0]["verdict"] == "merge"


async def test_no_arms_answers_none_without_a_paid_call(monkeypatch, ledger):
    async def must_not_run(**_kw: Any) -> Any:
        raise AssertionError("nothing to judge must not call a model")

    monkeypatch.setattr("matrx_ai.graph_nodes._strict_json.llm_to_pydantic", must_not_run)
    inputs = ResolveArmsInput(
        job="j", holes=[GatheredHole(item_index=0), GatheredHole(item_index=1)], expected=2
    )

    out = (await resolve_arms(_ctx(), inputs)).result

    assert out.verdict == "none"
    assert len(out.missing_arms) == 2
