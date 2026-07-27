"""MoE-style routing across small specialists.

Stretches `core/agent_pipeline.py` from a fixed 4-phase pipeline into a
generic specialist-router: any number of named specialists, each backed
by a different (typically smaller) model, with a planner that decides
which specialists to consult and in what order.

Why MoE-style: a 3B planner + 7B coder + 3B reviewer = 13B of activated
parameters per turn, but only the relevant 7-8B is loaded at once if you
swap models (or you keep all three resident on a 32GB box for parallelism).
This routinely beats a single 14B generalist on agent-style tasks.

This is intentionally model-agnostic: you supply the routing function and
the specialists; this module orchestrates them.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "Specialist",
    "MoEResult",
    "MoEPipeline",
]

SendFn = Callable[..., str]


@dataclass
class Specialist:
    name: str
    model: str
    system_prompt: str
    description: str = ""


@dataclass
class SpecialistOutput:
    specialist: str
    model: str
    output: str
    duration_s: float
    error: str | None = None


@dataclass
class MoEResult:
    plan: list[str]
    outputs: list[SpecialistOutput]
    final: str
    total_duration_s: float
    success: bool
    routing_reason: str = ""


class MoEPipeline:
    """Plan → consult selected specialists → synthesize.

    Args:
        send_fn:      (prompt, *, model, system) -> str
        planner:      Specialist that decides which other specialists to call
        specialists:  registry of name → Specialist
        max_specialists: cap on how many specialists the planner can pick
    """

    def __init__(
        self,
        send_fn: SendFn,
        planner: Specialist,
        specialists: dict[str, Specialist],
        max_specialists: int = 3,
    ):
        self.send_fn = send_fn
        self.planner = planner
        self.specialists = specialists
        self.max_specialists = max_specialists

    def _ask_planner(self, user_request: str) -> tuple[list[str], str]:
        """Ask the planner which specialists to call. Returns (names, reasoning)."""
        roster = "\n".join(
            f"  - {s.name}: {s.description}" for s in self.specialists.values()
        )
        prompt = (
            f"USER REQUEST:\n{user_request}\n\n"
            f"AVAILABLE SPECIALISTS:\n{roster}\n\n"
            "Reply with a single line: a comma-separated list of "
            f"specialist names to consult (max {self.max_specialists}), "
            "in the order you want them called. No commentary."
        )
        try:
            reply = self.send_fn(prompt, model=self.planner.model,
                                 system=self.planner.system_prompt)
        except Exception as exc:
            return ([], f"planner error: {exc}")
        names = [n.strip() for n in reply.split(",") if n.strip() in self.specialists]
        return (names[: self.max_specialists], reply.strip())

    def _consult(self, spec: Specialist, user_request: str,
                 prior_outputs: list[SpecialistOutput]) -> SpecialistOutput:
        ctx = "\n".join(f"## {o.specialist}\n{o.output}" for o in prior_outputs if o.error is None)
        prompt = f"USER REQUEST:\n{user_request}"
        if ctx:
            prompt += f"\n\n## PRIOR SPECIALISTS\n{ctx}"
        t0 = time.time()
        try:
            out = self.send_fn(prompt, model=spec.model, system=spec.system_prompt)
            return SpecialistOutput(spec.name, spec.model, out, time.time() - t0)
        except Exception as exc:
            return SpecialistOutput(spec.name, spec.model, "", time.time() - t0, error=str(exc))

    def _synthesize(self, user_request: str, outputs: list[SpecialistOutput]) -> str:
        """Last call: planner aggregates specialist outputs into a final answer."""
        body = "\n\n".join(
            f"### {o.specialist} ({o.model})\n{o.output}"
            for o in outputs if o.error is None
        )
        prompt = (
            f"USER REQUEST:\n{user_request}\n\n"
            f"SPECIALIST OUTPUTS:\n{body}\n\n"
            "Synthesize a single coherent final answer for the user."
        )
        try:
            return self.send_fn(prompt, model=self.planner.model,
                                system=self.planner.system_prompt)
        except Exception as exc:
            return f"[synthesis failed: {exc}]"

    def run(self, user_request: str) -> MoEResult:
        t0 = time.time()
        plan, reasoning = self._ask_planner(user_request)
        if not plan:
            return MoEResult(
                plan=[], outputs=[], final="", total_duration_s=time.time() - t0,
                success=False, routing_reason=reasoning or "no specialists selected",
            )
        outputs: list[SpecialistOutput] = []
        for name in plan:
            spec = self.specialists[name]
            outputs.append(self._consult(spec, user_request, outputs))
        final = self._synthesize(user_request, outputs)
        success = any(o.error is None for o in outputs)
        return MoEResult(
            plan=plan, outputs=outputs, final=final,
            total_duration_s=time.time() - t0,
            success=success, routing_reason=reasoning,
        )
