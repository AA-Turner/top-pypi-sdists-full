"""Typed decisions with TypeSafe's System One model (Jev), with ATIF tracing.

Where ``plato.llm`` generates text, System One answers narrow questions about a
state with calibrated, typed answers: a Choice among options you define, a Noul
(probability of yes) or a Score on an ordered rubric. One call answers any
number of questions in ~250 ms.

This is a thin wrapper around TypeSafe's own SDK (``typesafe_sdk``): the
question and answer types are theirs, re-exported here. What it adds is the
Plato conventions ``world.llm`` already has: a ``DecisionConfig`` for world
configs, a ``JEV_API_KEY`` fallback, and one ATIF span per call so decisions
show up in the Chronos trace viewer next to LLM calls.

Usage from a world:

    from plato.decision import Choice, ChoiceAnswer, Noul, NoulAnswer, SystemOneResponse

    class Triage(SystemOneResponse):
        done: NoulAnswer
        outcome: ChoiceAnswer

    decide = self.decision(self.config.jev)
    result = await decide.system_one(
        transcript,
        {
            "done": Noul(instructions="Did the agent finish the task?"),
            "outcome": Choice(
                instructions="How did the run end?",
                criteria={"success": None, "gave_up": None, "crashed": "An error stopped it"},
            ),
        },
        response_model=Triage,
    )
    result.done.noul           # float, P(yes)
    result.outcome.choice      # str, one of the criteria keys
    result.outcome.confidence  # 0..1

Without ``response_model`` you get a ``SystemOneResponse`` with ``.nouls``,
``.choices`` and ``.scores`` dicts keyed by question name.

API contract: https://docs.typesafe.ai/api.md
"""

from __future__ import annotations

import json
import os
import time
from collections.abc import Mapping
from typing import Any, Literal, TypeVar, overload

from pydantic import BaseModel
from typesafe_sdk import (
    AsyncTypeSafeClient,
    Choice,
    ChoiceAnswer,
    JSONContent,
    Noul,
    NoulAnswer,
    Question,
    RetryPolicy,
    Score,
    ScoreAnswer,
    SystemOneResponse,
    TypeSafeError,
)

from plato.otel import get_tracer, record_step_cost
from plato.worlds.config import DecisionConfig

__all__ = [
    "Choice",
    "ChoiceAnswer",
    "DecisionClient",
    "DecisionConfig",
    "Noul",
    "NoulAnswer",
    "Score",
    "ScoreAnswer",
    "SystemOneResponse",
    "TypeSafeError",
]

API_KEY_ENV_VARS = ("JEV_API_KEY", "TYPESAFE_API_KEY")

ResponseT = TypeVar("ResponseT", bound=BaseModel)


class DecisionClient:
    """System One client for worlds. Get one with ``world.decision(config)``.

    ``system_one`` has the same signature as
    ``typesafe_sdk.AsyncTypeSafeClient.system_one``. Each call opens and closes
    its own HTTP client, so there is nothing to clean up afterwards.
    """

    def __init__(
        self,
        config: DecisionConfig | None = None,
        *,
        tracer_name: str = "plato.decision",
        atif_source: Literal["agent", "world"] = "agent",
    ) -> None:
        self._config = config or DecisionConfig()
        self._tracer_name = tracer_name
        self._atif_source = atif_source

    def _client(self) -> AsyncTypeSafeClient:
        api_key = self._config.api_key or next((os.environ[v] for v in API_KEY_ENV_VARS if os.environ.get(v)), None)
        return AsyncTypeSafeClient(
            api_key=api_key,
            model=self._config.model,
            base_url=self._config.api_base or None,
            timeout=self._config.timeout,
            retry=RetryPolicy(max_retries=self._config.max_retries),
        )

    @overload
    async def system_one(
        self,
        state: JSONContent | BaseModel,
        questions: Mapping[str, Question],
        *,
        model: str | None = None,
        response_model: None = None,
    ) -> SystemOneResponse: ...

    @overload
    async def system_one(
        self,
        state: JSONContent | BaseModel,
        questions: Mapping[str, Question],
        *,
        model: str | None = None,
        response_model: type[ResponseT],
    ) -> ResponseT: ...

    async def system_one(
        self,
        state: JSONContent | BaseModel,
        questions: Mapping[str, Question],
        *,
        model: str | None = None,
        response_model: type[ResponseT] | None = None,
    ) -> SystemOneResponse | ResponseT:
        """Answer named questions about ``state`` (text, JSON, or a Pydantic model)."""
        wire_state: JSONContent = state.model_dump(mode="json") if isinstance(state, BaseModel) else state
        wire_questions = {
            name: q.model_dump(mode="json", exclude_none=True) if isinstance(q, BaseModel) else q
            for name, q in questions.items()
        }

        # The ATIF step span wraps the request, so its duration is the real wait and a
        # failed call still leaves a span (with the exception recorded) in the trace.
        from plato.llm import _next_step_id

        step_id = _next_step_id()
        with get_tracer(self._tracer_name).start_as_current_span(f"atif.step.{step_id}") as span:
            span.set_attribute("atif.kind", "llm")
            span.set_attribute("atif.step.id", step_id)
            span.set_attribute("atif.step.source", self._atif_source)
            span.set_attribute("atif.step.model_name", model or self._config.model)
            # The trace viewer renders input from atif.step.input_messages (chat format).
            request = {"state": wire_state, "questions": wire_questions}
            span.set_attribute(
                "atif.step.input_messages",
                json.dumps([{"role": "user", "content": json.dumps(request, indent=2, default=str)}]),
            )

            start = time.monotonic()
            async with self._client() as client:
                if response_model is None:
                    result: SystemOneResponse | ResponseT = await client.system_one(wire_state, questions, model=model)
                else:
                    result = await client.system_one(wire_state, questions, model=model, response_model=response_model)
            span.set_attribute("llm.duration_ms", (time.monotonic() - start) * 1000)

            payload = result.model_dump(mode="json")
            answers = payload.get("answers") or {}
            usage = payload.get("usage") or {}
            model_name = str(payload.get("model") or model or self._config.model)
            input_tokens = int(usage.get("input_tokens") or 0)
            output_tokens = int(usage.get("output_tokens") or 0)
            # TypeSafe bills input tokens only; the response carries no price.
            cost_usd = input_tokens * self._config.input_cost_per_mtok / 1_000_000
            span.set_attribute("atif.step.message", _summarize(answers))
            span.set_attribute("atif.step.model_name", model_name)
            span.set_attribute("atif.step.prompt_tokens", input_tokens)
            span.set_attribute("atif.step.completion_tokens", output_tokens)
            span.set_attribute("atif.step.cost_usd", cost_usd)
            span.set_attribute("decision.answers", json.dumps(answers, default=str))
            record_step_cost(
                cost_usd=cost_usd,
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
                model=model_name,
            )
        return result


def _summarize(answers: Mapping[str, Mapping[str, Any]]) -> str:
    """One line per call for the trace viewer, e.g. ``done: P(yes)=0.93; outcome: success (0.88)``."""
    parts: list[str] = []
    for name, answer in answers.items():
        if "noul" in answer:
            parts.append(f"{name}: P(yes)={float(answer['noul']):.2f}")
        elif "choice" in answer:
            parts.append(f"{name}: {answer['choice']} ({float(answer.get('confidence') or 0):.2f})")
        elif "score" in answer:
            parts.append(f"{name}: score={float(answer['score']):.2f}")
    return "; ".join(parts)
