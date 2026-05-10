"""Verifier / self-consistency loop.

Idea: a small model gets significantly smarter on coding tasks if you
sample N candidate solutions, then ask a critic (same or different model)
to pick the best one. This is well-documented in the LLM literature
(Chen et al. 2022, Madaan et al. 2023, etc.).

Sage's loop is intentionally simple:
  1. Generate N candidates with temperature spread (0.0, 0.4, 0.8)
  2. If a programmatic validator was supplied (e.g., runs tests), prefer
     candidates that pass
  3. Otherwise, ask a critic to score each on (correctness, clarity,
     completeness) and pick the highest

Cost: N× generation. Use sparingly — wrap only the final implementation
phase, not exploratory turns. The agent_pipeline integration plugs this
in as the Coder phase when `n_samples > 1`.
"""

from __future__ import annotations

import statistics
from collections.abc import Callable
from dataclasses import dataclass, field

__all__ = [
    "Candidate",
    "VerifierResult",
    "best_of_n",
]


@dataclass
class Candidate:
    output: str
    temperature: float
    score: float = 0.0
    notes: str = ""
    valid: bool = True


@dataclass
class VerifierResult:
    winner: Candidate
    all_candidates: list[Candidate] = field(default_factory=list)
    used_validator: bool = False
    used_critic: bool = False


def _critic_prompt(task: str, candidates: list[Candidate]) -> str:
    parts = [
        "You are a critical code reviewer. Score each candidate solution to "
        "the task below on a scale of 1-10 considering correctness, clarity, "
        "and completeness. Reply ONLY with one line per candidate in the "
        "exact form: '<index>: <score> <one-sentence-reason>'.",
        "",
        f"TASK:\n{task}",
        "",
        "CANDIDATES:",
    ]
    for i, c in enumerate(candidates):
        parts.append(f"\n=== CANDIDATE {i} ===\n{c.output}")
    return "\n".join(parts)


def _parse_critic_scores(reply: str, n: int) -> list[float]:
    scores = [0.0] * n
    for line in reply.splitlines():
        line = line.strip()
        if not line:
            continue
        # "0: 8 ..." or "0: 8.5 - "
        try:
            idx_str, rest = line.split(":", 1)
            idx = int(idx_str.strip())
            tokens = rest.strip().split()
            if not tokens:
                continue
            score = float(tokens[0])
            if 0 <= idx < n:
                scores[idx] = score
        except (ValueError, IndexError):
            continue
    return scores


def best_of_n(
    *,
    task: str,
    generator: Callable[[float], str],         # (temperature) -> output
    n_samples: int = 3,
    validator: Callable[[str], tuple[bool, str]] | None = None,
    critic: Callable[[str], str] | None = None,  # (prompt) -> reply
    temperatures: list[float] | None = None,
) -> VerifierResult:
    """Sample N candidates, score them, return the best.

    Args:
        task: the original task description (for the critic prompt)
        generator: callable that produces an output given a temperature
        n_samples: how many candidates to draw
        validator: optional programmatic check; if provided, valid candidates
                   beat invalid ones regardless of critic score
        critic: optional reviewer model callable; if absent, picks the most
                "agreed-upon" candidate by lexical overlap (cheap fallback)
    """
    if n_samples < 1:
        n_samples = 1
    temps = temperatures or _spread_temperatures(n_samples)
    candidates: list[Candidate] = []
    for t in temps[:n_samples]:
        try:
            out = generator(t)
        except Exception as exc:
            out = ""
        candidates.append(Candidate(output=out, temperature=t))

    # ── Validator pass (cheap; deterministic)
    used_validator = False
    if validator is not None:
        used_validator = True
        for c in candidates:
            try:
                ok, msg = validator(c.output)
            except Exception as exc:
                ok, msg = False, f"validator error: {exc}"
            c.valid = ok
            c.notes = msg

    valid_pool = [c for c in candidates if c.valid] or candidates

    # ── Critic pass (expensive; one model call)
    used_critic = False
    if critic is not None and len(valid_pool) > 1:
        used_critic = True
        try:
            reply = critic(_critic_prompt(task, valid_pool))
            scores = _parse_critic_scores(reply, n=len(valid_pool))
            for c, s in zip(valid_pool, scores):
                c.score = s
        except Exception:
            pass  # Fall through to lexical fallback

    # ── Decide winner
    if used_critic and any(c.score > 0 for c in valid_pool):
        winner = max(valid_pool, key=lambda c: c.score)
    elif used_validator:
        # Among valid, pick the longest non-trivial output (proxy for completeness)
        winner = max(valid_pool, key=lambda c: len(c.output))
    else:
        # Self-consistency fallback: count how many candidates produced
        # outputs with shared content lines
        winner = _consistency_winner(valid_pool)

    return VerifierResult(
        winner=winner, all_candidates=candidates,
        used_validator=used_validator, used_critic=used_critic,
    )


def _spread_temperatures(n: int) -> list[float]:
    if n <= 1:
        return [0.2]
    if n == 2:
        return [0.2, 0.7]
    if n == 3:
        return [0.0, 0.4, 0.8]
    # Spread linearly across [0, 0.9]
    return [round(i * 0.9 / (n - 1), 2) for i in range(n)]


def _consistency_winner(pool: list[Candidate]) -> Candidate:
    """Fallback: pick the candidate whose lines appear most across siblings."""
    if not pool:
        return Candidate(output="", temperature=0.0)
    line_sets = [set(c.output.splitlines()) for c in pool]
    best_idx = 0
    best_overlap = -1
    for i, lines in enumerate(line_sets):
        overlap = sum(len(lines & other) for j, other in enumerate(line_sets) if j != i)
        if overlap > best_overlap:
            best_overlap = overlap
            best_idx = i
    return pool[best_idx]
