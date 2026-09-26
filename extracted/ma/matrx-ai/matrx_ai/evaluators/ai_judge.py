"""``AIJudge`` — strict-JSON AI-as-judge evaluator for the test suite.

Why this exists
---------------
Tests for AI workflows can't rely on string assertions — model outputs are
non-deterministic by nature. Mocking the LLM defeats the purpose; the test
no longer proves the engine works. The right primitive is an *impartial,
top-tier judge model* that reads the actual output and votes pass/fail.

Design
------
- Uses the canonical matrx-ai execution funnel so routing, retries, usage,
  provider-tool charges, and durable cost capture are identical to product calls.
- HELD BY A MANDATE (``proof_runs.judge``, 2026-09-25). The judge's model,
  instructions and web access are the mandate Holder's — the "Proof Run Judge"
  agent, seeded with this file's former prompt verbatim — so improving the
  judge is an agent edit through the mandate console, never a code change.
  An explicit ``model=`` / ``web_access=`` is a run-scope override.
- Strict-JSON output is enforced with the funnel's provider-native structured
  output contract and validated again as :class:`JudgeVerdict`.
- Optional web access via Anthropic's server-side ``web_search`` tool —
  enable for rubrics that require fact-checking against current information.
- Pydantic validation catches any schema drift and raises :class:`JudgeError`.

Anti-patterns to avoid
----------------------
- Calling a provider SDK directly. All paid calls go through the funnel.
- Asking the judge to score on a 0-100 scale. Pass/fail is enforceable;
  fine-grained scores are noise. Use ``confidence`` for nuance.
- Calling :meth:`AIJudge.judge` from inside a tight loop. It's an LLM
  call — assume seconds of latency and real cost per invocation.
"""

from __future__ import annotations

import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

#: The mandate that holds every AIJudge call (declared in aidream
#: ``services/proof_runs/judge.py``).
from matrx_ai.code_call_mandate_keys import AI_JUDGE_MANDATE  # noqa: E402
from matrx_ai.graph_nodes._strict_json import StrictJsonError
from matrx_ai.mandates import MandateResolutionUnavailable, hold_code_call, run_held_pydantic
from matrx_ai.providers.keys import resolve_api_key


class JudgeVerdict(BaseModel):
    """Strict-JSON verdict returned by an :class:`AIJudge`.

    Round-trips losslessly via ``model_validate_json(strict=True)`` — any
    deviation in the model's output raises :class:`JudgeError`.
    """

    model_config = ConfigDict(extra="forbid")

    verdict: Literal["pass", "fail"]
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="The judge's certainty in the verdict, 0.0-1.0.",
    )
    reasoning: str = Field(
        min_length=1,
        description="One paragraph explaining the verdict.",
    )
    evidence: list[str] = Field(
        default_factory=list,
        description=(
            "Quotes or specific observations from the actual output that support the verdict."
        ),
    )
    failure_modes: list[str] = Field(
        default_factory=list,
        description=(
            "When verdict='fail', the categories of failure observed. Empty when verdict='pass'."
        ),
    )


class JudgeError(Exception):
    """Raised when the judge cannot produce a valid verdict."""


class AIJudge:
    """Strict-JSON evaluator for AI workflow / agent output.

    Typical use::

        judge = AIJudge()
        verdict = await judge.judge(
            rubric="The output should be a non-empty study summary...",
            actual_output=workflow_result.final_text,
        )
        assert verdict.verdict == "pass", verdict.reasoning

    The judge does **not** see the test code. It only sees the rubric and
    the output. This isolation prevents the judge from rationalizing a
    pass that the test would have caught.
    """

    def __init__(
        self,
        model: str | None = None,
        web_access: bool | None = None,
        api_key: str | None = None,
        max_iterations: int = 4,
        max_tokens: int | None = None,
    ) -> None:
        self.model = model
        self.web_access = web_access
        self._api_key = api_key
        self.max_iterations = max_iterations
        self.max_tokens = max_tokens

    async def judge(
        self,
        rubric: str,
        actual_output: Any,
        context: dict[str, Any] | None = None,
    ) -> JudgeVerdict:
        """Return a verdict on whether ``actual_output`` satisfies ``rubric``.

        ``actual_output`` may be a string, dict, list, or Pydantic model —
        it is JSON-serialized for the prompt.

        The caller must have an ambient ``AppContext`` so the judge's cost can
        be attributed to the same user request. Raises :class:`JudgeError` for
        missing credentials/context or invalid structured output.
        """
        output_str = _format_output(actual_output)
        # Web access is the caller's explicit choice when set; otherwise the
        # Holder decides. Resolved BEFORE the Holder renders, because its
        # instructions say whether this judgment may search.
        try:
            held = await hold_code_call(
                AI_JUDGE_MANDATE,
                consumer="matrx_ai.evaluators.AIJudge",
                variables={
                    "rubric": rubric,
                    "actual_output": output_str,
                    "context": json.dumps(context, indent=2, default=str) if context else "",
                    **(
                        {"web_search": "allowed" if self.web_access else "not allowed"}
                        if self.web_access is not None
                        else {}
                    ),
                },
                metadata={
                    "source_app": "matrx-ai",
                    "source_feature": "ai_judge",
                    "judge_max_iterations_legacy": self.max_iterations,
                },
            )
        except MandateResolutionUnavailable as exc:
            raise JudgeError(f"AIJudge could not resolve its mandate: {exc}") from exc
        web_access = (
            self.web_access
            if self.web_access is not None
            else bool(getattr(held.config, "internal_web_search", False))
        )
        api_key = self._api_key or resolve_api_key("ANTHROPIC_API_KEY")
        try:
            return await run_held_pydantic(
                held,
                messages=held.turns,
                output_cls=JudgeVerdict,
                model=self.model,
                max_tokens=self.max_tokens,
                unset_max_tokens=4096,
                internal_web_search=web_access,
                api_keys={"ANTHROPIC_API_KEY": api_key} if api_key else None,
                system_run=True,
                store=True,
            )
        except (StrictJsonError, RuntimeError) as exc:
            raise JudgeError(f"AIJudge failed through the execution funnel: {exc}") from exc


def _format_output(actual_output: Any) -> str:
    if isinstance(actual_output, str):
        return actual_output
    if isinstance(actual_output, BaseModel):
        return actual_output.model_dump_json(indent=2)
    try:
        return json.dumps(actual_output, indent=2, default=str)
    except (TypeError, ValueError):
        return str(actual_output)


