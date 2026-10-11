"""A mandated judge that gets no parsed answer says WHY — never a parse-shaped mask.

2026-10-11: every mandate-candidate review ended "Review didn't run" with
``JudgeError: mandated agent returned no parsed output``. The run had never reached a
model: the protected-account gate refused it (``success=False``, ``error_kind=execution``,
``error="Not run: …"``). The judge threw that reason away and reported a parse failure, so
the owner chased the agent's output schema. These tests drive the real
``Judge._run_mandated`` with a runner returning each real no-verdict shape and require the
JudgeError to carry the run's own reason.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from matrx_ai.agents.executor import AgentRunResult
from matrx_ai.evaluators import Judge, JudgeError, JudgeSubject
from matrx_ai.evaluators.judge import JudgeContract


class _Inputs(BaseModel):
    question: str
    rubric_name: str | None = None
    rubric: str | None = None
    verdict_values: list[str]
    subject_label: str
    subject_content: str
    subject_metrics: dict[str, Any] | None = None
    reference_label: str | None = None
    reference_content: str | None = None
    reference_metrics: dict[str, Any] | None = None
    context: dict[str, Any] | None = None


class _JudgeAgent:
    Inputs = _Inputs
    mandate_key = "tests.judge"


_CONTRACT = JudgeContract(
    key="tests.comparative",
    question="Is the candidate better?",
    mode="comparative",
    subject_kind="text",
    verdict_values=("better", "same", "worse"),
    rubric_name="r",
    rubric="Prefer the correct answer.",
    mandate="tests.judge",
)


async def _judge_with(result: AgentRunResult) -> str:
    async def _runner(_cls: Any, **_kw: Any) -> AgentRunResult:
        return result

    judge = Judge(_CONTRACT, agent_cls=_JudgeAgent, mandate_runner=_runner)  # type: ignore[arg-type]
    with pytest.raises(JudgeError) as caught:
        await judge._run_mandated(
            JudgeSubject(label="candidate", content="a"),
            JudgeSubject(label="live", content="b"),
            context=None,
            user_id="u",
        )
    return str(caught.value)


@pytest.mark.asyncio
async def test_a_refused_run_names_its_refusal() -> None:
    message = await _judge_with(
        AgentRunResult(
            success=False,
            error_kind="execution",
            error="Not run: this system run would run as, and bill, a protected account",
        )
    )
    assert "Not run: this system run would run as, and bill, a protected account" in message
    assert "execution" in message
    assert "did not succeed" in message


@pytest.mark.asyncio
async def test_an_unparseable_answer_names_the_parse_error() -> None:
    message = await _judge_with(
        AgentRunResult(success=True, output="not json", parse_error="Expecting value: line 1")
    )
    assert "did not parse" in message and "Expecting value: line 1" in message


@pytest.mark.asyncio
async def test_an_empty_answer_says_so() -> None:
    message = await _judge_with(AgentRunResult(success=True, output=""))
    assert "returned no answer text" in message
