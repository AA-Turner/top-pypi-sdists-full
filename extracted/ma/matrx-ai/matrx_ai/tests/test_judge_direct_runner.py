"""Lane 2E: the independent ``direct`` judge runner and its public surface.

``Judge(contract, runner="direct")`` is the sanctioned way to judge WITHOUT the agent-under-test's
plumbing: the Holder authors the text, ONE strict-JSON call returns the verdict, and the subject is
proven inside the text sent before a cent is spent. These pin what a host used to hand-roll by
importing privates. No DB, no LLM."""

from __future__ import annotations

import hashlib

import pytest

import matrx_ai.evaluators as ev
from matrx_ai.evaluators import (
    Judge,
    JudgeContract,
    JudgeContractError,
    JudgeError,
    JudgeSubject,
    JudgeUnfed,
)

REPLY = 'The "Kessler" crew arrives Tuesday.\nBring the 4 inch drain tile.'
RUBRIC = "Judge only the facts the case lists; ignore tone, length and formatting entirely, always."


def _rubric_contract(**kw) -> JudgeContract:
    base = {
        "key": "t.direct", "question": "Does it satisfy the facts?", "mode": "rubric",
        "subject_kind": "reply", "verdict_values": ("holds", "fails"),
        "rubric_name": "t.v1", "rubric": RUBRIC,
    }
    return JudgeContract(**{**base, **kw})


class _Held:
    system = "You are a strict fact judge."
    metadata: dict = {}

    def __init__(self, user: str) -> None:
        self._user = user
        self.finished: list = []

    def authored_user(self) -> str:
        return self._user

    def pick_model(self, explicit=None):
        return explicit or "m"

    def pin_for(self, *_a, **_k):
        return {}

    def pick_max_tokens(self, explicit=None, *, unset):
        return explicit or unset

    def pick_temperature(self, explicit=None):
        return explicit

    async def finish(self, output, **kw):
        self.finished.append((output, kw))


@pytest.fixture
def wired(monkeypatch):
    import matrx_ai.evaluators.ledger as ledger
    import matrx_ai.graph_nodes._strict_json as funnel
    import matrx_ai.mandates as mandates
    from matrx_ai.graph_nodes._strict_json import MeasuredStrictJson, StrictJsonUsage

    seen: dict = {"funnel": [], "user": None, "agent_plumbing": 0, "hold_meta": None}

    async def never(*_a, **_k):
        seen["agent_plumbing"] += 1
        raise AssertionError("the direct judge went through the agent plumbing")

    monkeypatch.setattr(mandates, "run_held_pydantic", never)
    monkeypatch.setattr("matrx_ai.mandates._send_pydantic", never)

    async def hold(key, **kwargs):
        seen["key"] = key
        seen["hold_meta"] = kwargs["metadata"]
        offer = kwargs["variables"]["subject_content"]
        user = seen["user"] if seen["user"] is not None else f"Judge:\n{offer}"
        held = _Held(user)
        seen["held"] = held
        return held

    async def measured(**kwargs):
        seen["funnel"].append(kwargs)
        out = kwargs["output_cls"](verdict="holds", confidence=0.9, reasoning="stated", evidence=[])
        return MeasuredStrictJson(value=out, usage=StrictJsonUsage(cost_usd=0.002), calls=1, duration_ms=5)

    async def record(**kwargs):
        seen["ledger"] = kwargs
        return "ledger-1"

    monkeypatch.setattr(mandates, "hold_code_call", hold)
    monkeypatch.setattr(funnel, "llm_to_pydantic_measured", measured)
    monkeypatch.setattr(ledger, "record_verdict", record)
    return seen


async def test_direct_makes_one_funnel_call_and_labels_the_ledger_row(wired):
    out = await Judge(_rubric_contract(), runner="direct").score(
        JudgeSubject(label="reply", content=REPLY), organization_id="o", user_id="u"
    )
    assert out.verdict == "holds"
    assert len(wired["funnel"]) == 1 and wired["agent_plumbing"] == 0
    assert wired["funnel"][0]["system_run"] is True and REPLY in wired["funnel"][0]["user"]
    assert out.invocation["runner"] == "direct", "the ledger shows which path ran"
    assert wired["ledger"]["invocation"]["runner"] == "direct" and out.ledger_id == "ledger-1"
    assert out.invocation["cost_usd"] == 0.002 and out.invocation["calls"] == 1


async def test_outcome_carries_sent_text_and_the_reply_hash(wired):
    out = await Judge(_rubric_contract(), runner="direct").score(JudgeSubject(label="reply", content=REPLY))
    assert out.reply_sha256 == hashlib.sha256(REPLY.encode()).hexdigest()
    assert out.invocation["reply_sha256"] == out.reply_sha256
    assert out.sent_text is not None and REPLY in out.sent_text and "strict fact judge" in out.sent_text


async def test_a_subject_that_did_not_arrive_is_unfed_before_any_model_call(wired):
    """Break caught: a trimmed subject got a confident verdict on the wrong text."""
    wired["user"] = "Judge:\nThe \"Kessler\" crew arrives Tuesday."  # first line only
    with pytest.raises(JudgeUnfed) as exc:
        await Judge(_rubric_contract(), runner="direct").score(JudgeSubject(label="reply", content=REPLY))
    assert wired["funnel"] == [], "nothing is paid for on the wrong text"
    assert exc.value.reply_sha256 == hashlib.sha256(REPLY.encode()).hexdigest()
    assert exc.value.sent_text and "strict fact judge" in exc.value.sent_text
    assert "ledger" not in wired


def test_judge_unfed_is_public_and_a_judge_error():
    assert ev.JudgeUnfed is JudgeUnfed and issubclass(JudgeUnfed, JudgeError)


def test_the_integrity_helpers_are_public():
    assert ev.reply_in_input(REPLY, '{"c": "The \\"Kessler\\" crew arrives Tuesday.\\nBring the 4 inch drain tile."}')
    assert not ev.reply_in_input("", "x")
    assert ev.missing_from_input(REPLY, ["Tuesday"], "nothing here")[0].startswith("reply sha256:")
    assert ev.reply_sha256("a") == hashlib.sha256(b"a").hexdigest()


async def test_host_metadata_merges_over_the_package_default(wired):
    await Judge(_rubric_contract(), runner="direct", metadata={"source_feature": "agent_tests_judge"}).score(
        JudgeSubject(label="reply", content=REPLY)
    )
    assert wired["hold_meta"]["source_feature"] == "agent_tests_judge"
    assert wired["funnel"][0]["metadata"]["source_feature"] == "agent_tests_judge"


def test_mandated_runner_needs_an_agent_class_and_mandate():
    with pytest.raises(JudgeContractError, match="runner='mandated'"):
        Judge(_rubric_contract(), runner="mandated")


def test_default_runner_keeps_the_old_implicit_choice():
    assert Judge(_rubric_contract())._runner == "funnel"
    assert Judge(_rubric_contract(mandate="m.x"), agent_cls=object)._runner == "mandated"


def test_public_rubric_isolation_door():
    assert ev.assert_rubric_isolation is not None
    with pytest.raises(JudgeContractError):
        ev.assert_rubric_isolation(_rubric_contract(), JudgeSubject(label="s", content=RUBRIC))
