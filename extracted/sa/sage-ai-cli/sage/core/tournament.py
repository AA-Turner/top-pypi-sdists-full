"""Item #24 — Multi-model tournament for hard turns."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

__all__ = ["Candidate", "TournamentResult", "tournament"]


@dataclass
class Candidate:
    model: str
    output: str
    error: str | None = None


@dataclass
class TournamentResult:
    winner_model: str
    winner_output: str
    candidates: list[Candidate] = field(default_factory=list)


SendFn = Callable[..., str]
JudgeFn = Callable[[str, list[Candidate]], Candidate]


def tournament(*,
                prompt: str,
                models: list[str],
                send_fn: SendFn,
                judge_fn: JudgeFn,
                system: str = "") -> TournamentResult:
    candidates: list[Candidate] = []
    for model in models:
        try:
            out = send_fn(prompt, model=model, system=system)
            candidates.append(Candidate(model=model, output=out))
        except Exception as exc:
            candidates.append(Candidate(
                model=model, output="", error=str(exc),
            ))

    valid = [c for c in candidates if c.error is None]
    if not valid:
        return TournamentResult(
            winner_model="", winner_output="", candidates=candidates,
        )

    winner = judge_fn(prompt, valid)
    return TournamentResult(
        winner_model=winner.model,
        winner_output=winner.output,
        candidates=candidates,
    )
