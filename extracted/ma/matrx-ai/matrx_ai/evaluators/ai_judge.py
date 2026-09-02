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
- Default model is the latest Claude Opus.
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

from matrx_ai.graph_nodes._strict_json import StrictJsonError, llm_messages_to_pydantic
from matrx_ai.providers.keys import resolve_api_key

# The catalog resolves ROUTES, not dated snapshots: the pinned
# "claude-opus-4-5-20250929" was retired out from under this constant and
# every AIJudge call died with matrx_catalog_error ("unknown model") — a
# failure that reads as "the thing under test is broken". Keep this on a
# live route name, the same one the workflow nodes use.
DEFAULT_MODEL = "claude-opus-4-7"
"""Latest Claude Opus snapshot. Override for cost tuning (e.g. Sonnet)."""


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
        model: str = DEFAULT_MODEL,
        web_access: bool = True,
        api_key: str | None = None,
        max_iterations: int = 4,
        max_tokens: int = 4096,
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
        api_key = self._api_key or resolve_api_key("ANTHROPIC_API_KEY")
        if not api_key:
            raise JudgeError(
                "ANTHROPIC_API_KEY not set and no api_key passed. "
                "AIJudge cannot run without an API key."
            )

        output_str = _format_output(actual_output)
        system_prompt = _build_system_prompt(self.web_access)
        user_message = _build_user_message(rubric, output_str, context)
        try:
            return await llm_messages_to_pydantic(
                model=self.model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                output_cls=JudgeVerdict,
                max_tokens=self.max_tokens,
                internal_web_search=self.web_access,
                api_keys={"ANTHROPIC_API_KEY": api_key},
                system_run=True,
                store=True,
                metadata={
                    "source_app": "matrx-ai",
                    "source_feature": "ai_judge",
                    "judge_max_iterations_legacy": self.max_iterations,
                },
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


def _build_system_prompt(web_access: bool) -> str:
    web_clause = (
        " You may use web_search to verify facts when the rubric demands "
        "accuracy against current information; use it sparingly."
        if web_access
        else ""
    )
    return (
        "You are an impartial test evaluator. You read a rubric and an "
        "output, then return a strict pass/fail verdict.\n\n"
        "Rules:\n"
        "1. Be rigorous. False positives undermine the test suite.\n"
        "2. Cite specific evidence from the output (or its absence) in the "
        "evidence list.\n"
        "3. Prefer verdict='fail' with low confidence over verdict='pass' "
        "with reservations.\n"
        "4. confidence reflects your certainty in the verdict, not the "
        "output's quality.\n"
        f"5. Always return the required structured verdict.{web_clause}"
    )


def _build_user_message(rubric: str, output: str, context: dict[str, Any] | None) -> str:
    ctx_block = ""
    if context:
        ctx_block = f"\n\n## Context\n```json\n{json.dumps(context, indent=2, default=str)}\n```"
    return (
        f"## Rubric\n{rubric}\n\n"
        f"## Actual Output\n```\n{output}\n```"
        f"{ctx_block}\n\n"
        "Evaluate whether the output satisfies the rubric, then call "
        "submit_verdict with your final assessment."
    )
