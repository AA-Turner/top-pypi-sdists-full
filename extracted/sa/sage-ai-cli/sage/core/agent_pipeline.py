"""Planner → Coder → Reviewer → Validator pipeline.

The premise: small models do better when they specialize. Instead of asking
qwen3-coder-next to plan, code, review, and validate in a single thought,
we route each phase to the best-fit model and let cheap models handle
cheap work:

  Planner    — fast small model (gemma2:2b, llama3.2:3b) — decompose the task
  Coder      — strong coder (qwen3-coder-next, deepseek-coder) — write each step
  Reviewer   — reasoning model (qwq, deepseek-r1) or Coder again — find bugs
  Validator  — programmatic — runs tests/typecheck, returns pass/fail

This sits on top of the existing SwarmOrchestrator (core/swarm.py) for
parallel execution and dependency tracking — it's not a replacement, it's
a curated four-phase recipe.

Send-fn signature is intentionally narrow so any caller (typer command,
test, REPL) can drive it: `send(prompt: str, *, model: str, system: str) -> str`.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

__all__ = ["PhaseResult", "PipelineResult", "AgentPipeline", "SendFn"]

SendFn = Callable[..., str]   # (prompt, *, model, system) -> str


@dataclass
class PhaseResult:
    name: str
    model: str
    output: str
    duration_s: float
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass
class PipelineResult:
    plan: PhaseResult
    code: PhaseResult
    review: PhaseResult
    validate: PhaseResult | None = None
    total_duration_s: float = 0.0
    success: bool = False

    @property
    def models_used(self) -> set[str]:
        models = {self.plan.model, self.code.model, self.review.model}
        if self.validate:
            models.add(self.validate.model)
        return models


_PLANNER_SYS = (
    "You are the PLANNER. Decompose the user's task into 3-7 concrete, "
    "ordered steps. Each step is one self-contained subtask the Coder will "
    "implement. Output a numbered list — no commentary, no code."
)

_CODER_SYS = (
    "You are the CODER. The Planner gave you ordered steps and the user's "
    "original request. Implement them using the SAGE protocol "
    "(FILE: / READ: / RUN: / SEARCH:). Stay concrete; do not re-plan. "
    "Output COMPLETE file contents in FILE: blocks."
)

_REVIEWER_SYS = (
    "You are the REVIEWER. You will be shown the original task and the "
    "Coder's output. Find concrete bugs, security issues, missing error "
    "handling, and incorrect assumptions. Be specific (file:line). "
    "If the code is correct, say so in one sentence."
)


class AgentPipeline:
    """Drive a 4-phase pipeline given a `send` function.

    The caller provides:
      - send_fn: how to talk to a model (handles streaming, retries, etc.)
      - planner_model / coder_model / reviewer_model: model ids
      - validate_fn: optional callable that runs tests/typecheck and returns
        (success: bool, message: str). Skipped if None.
    """

    def __init__(
        self,
        send_fn: SendFn,
        *,
        planner_model: str,
        coder_model: str,
        reviewer_model: str | None = None,
        validate_fn: Callable[[str], tuple[bool, str]] | None = None,
    ):
        self.send_fn = send_fn
        self.planner_model = planner_model
        self.coder_model = coder_model
        # Reviewer defaults to coder model if no reasoning model is configured.
        self.reviewer_model = reviewer_model or coder_model
        self.validate_fn = validate_fn

    def _phase(self, name: str, model: str, prompt: str, system: str) -> PhaseResult:
        t0 = time.time()
        try:
            out = self.send_fn(prompt, model=model, system=system)
            return PhaseResult(name=name, model=model, output=out, duration_s=time.time() - t0)
        except Exception as exc:
            return PhaseResult(
                name=name, model=model, output="", duration_s=time.time() - t0,
                error=f"{type(exc).__name__}: {exc}",
            )

    def run(self, user_request: str, *, project_context: str = "") -> PipelineResult:
        t0 = time.time()
        ctx_block = f"\n\n## PROJECT CONTEXT\n{project_context}\n" if project_context else ""

        plan = self._phase(
            "plan", self.planner_model,
            prompt=f"USER REQUEST:\n{user_request}{ctx_block}",
            system=_PLANNER_SYS,
        )
        if not plan.ok:
            return PipelineResult(plan=plan, code=plan, review=plan,
                                  total_duration_s=time.time() - t0, success=False)

        code = self._phase(
            "code", self.coder_model,
            prompt=(
                f"ORIGINAL REQUEST:\n{user_request}{ctx_block}\n\n"
                f"PLAN (from Planner):\n{plan.output}\n\n"
                "Implement each step in order."
            ),
            system=_CODER_SYS,
        )
        if not code.ok:
            return PipelineResult(plan=plan, code=code, review=code,
                                  total_duration_s=time.time() - t0, success=False)

        review = self._phase(
            "review", self.reviewer_model,
            prompt=(
                f"ORIGINAL REQUEST:\n{user_request}{ctx_block}\n\n"
                f"CODER OUTPUT:\n{code.output}\n\n"
                "Find concrete issues (file:line). One sentence if it looks correct."
            ),
            system=_REVIEWER_SYS,
        )

        validate: PhaseResult | None = None
        success = review.ok
        if self.validate_fn:
            t1 = time.time()
            try:
                ok, msg = self.validate_fn(code.output)
                validate = PhaseResult(
                    name="validate", model="programmatic", output=msg,
                    duration_s=time.time() - t1,
                    error=None if ok else "validation failed",
                )
                success = success and ok
            except Exception as exc:
                validate = PhaseResult(
                    name="validate", model="programmatic", output="",
                    duration_s=time.time() - t1, error=str(exc),
                )
                success = False

        return PipelineResult(
            plan=plan, code=code, review=review, validate=validate,
            total_duration_s=time.time() - t0, success=success,
        )
