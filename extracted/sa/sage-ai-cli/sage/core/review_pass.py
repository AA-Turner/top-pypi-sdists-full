"""Per-file principal-engineer review pass.

After a file is generated, run an LLM-driven review against a 10-criteria
rubric. If the score falls below threshold, regenerate the file with the
gaps fed back into the prompt. Loops until score ≥ threshold or
max_review_rounds reached.

The rubric is principal-engineer specific: not just "does the code parse"
but "is the design idiomatic for the framework, are responsibilities
clean, are edge cases handled, are dependencies injected, is naming
clear, are tests meaningful, etc."
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


GenerateFn = Callable[[str], str]


@dataclass
class ReviewResult:
    score: float  # 0.0–10.0
    gaps: list[str]
    notes: str


_REVIEW_PROMPT = """You are a principal engineer reviewing ONE file before merge.

## File path
{path}

## File role
{role}

## File contents
```
{content}
```

## Rubric — score each criterion 0-10

1. Correctness — compiles/parses, no obvious bugs.
2. Idiomatic — uses current API conventions for {framework}.
3. Completeness — every promised responsibility is implemented; no TODO,
   no placeholder strings, no `pass` where logic should be.
4. Error handling — explicit, scoped, never bare `except:`. No silent
   failures.
5. Dependency injection — receives collaborators via __init__ or Depends,
   doesn't reach into globals.
6. Naming — clear, descriptive, follows the project's case conventions.
7. Security — no hardcoded secrets, parameterized queries, no string-built SQL.
8. Tests-friendly — pure functions where possible, side effects isolated
   so the file is reasonable to unit-test.
9. Documentation — module + public function docstrings, one line each.
10. Boundaries — no upward dependencies (models don't import api;
    services don't import FastAPI).

## Output (single JSON line, no prose, no fences)
{{"score": <float 0-10, average of the 10 criteria>, "gaps": ["specific missing thing 1", "..."], "notes": "one-line summary"}}
"""


_REGEN_PROMPT = """A reviewer scored this file {score:.1f}/10. Fix the gaps below.

## File path
{path}

## File role
{role}

## Current (failing) content
```
{content}
```

## Gaps the reviewer flagged
{gap_list}

## Output
Rewrite the file fixing EVERY listed gap. Keep what works. Add what's missing.
Output ONLY the new file contents. No prose, no `<thinking>` tags, no fences.
"""


def _parse_review(raw: str) -> ReviewResult:
    """Tolerant JSON extraction for the review response."""
    if not raw:
        return ReviewResult(score=5.0, notes="(empty review)", gaps=[])
    # Strip code fences and reasoning blocks if any
    raw = raw.strip()
    # Find first JSON object that has a "score" key
    match = re.search(r"\{[^{}]*\"score\"[^{}]*\}", raw, re.DOTALL)
    if not match:
        return ReviewResult(score=5.0, notes="(no JSON in review)", gaps=[])
    try:
        obj = json.loads(match.group(0))
        return ReviewResult(
            score=float(obj.get("score", 5.0)),
            gaps=[str(g) for g in obj.get("gaps", []) if g],
            notes=str(obj.get("notes", "")),
        )
    except (ValueError, TypeError):
        return ReviewResult(score=5.0, notes="(review parse failed)", gaps=[])


def review_file(
    path: Path,
    role: str,
    framework: str,
    generate: GenerateFn,
) -> ReviewResult:
    """Read the file, ask the LLM to review it, parse the JSON response."""
    try:
        content = path.read_text("utf-8", errors="replace")
    except OSError as exc:
        return ReviewResult(score=0.0, notes=f"read failed: {exc}", gaps=[])
    prompt = _REVIEW_PROMPT.format(
        path=path.name, role=role, content=content[:6000], framework=framework
    )
    try:
        raw = generate(prompt)
    except Exception as exc:  # noqa: BLE001 — never crash the build for a review
        return ReviewResult(score=5.0, notes=f"generate failed: {exc}", gaps=[])
    return _parse_review(raw)


def regenerate_for_gaps(
    path: Path,
    role: str,
    score: float,
    gaps: list[str],
    generate: GenerateFn,
    sanitize: Callable[[str], str],
) -> None:
    """Ask the LLM to rewrite the file fixing the gap list."""
    try:
        content = path.read_text("utf-8", errors="replace")
    except OSError:
        return
    if not gaps:
        return
    gap_list = "\n".join(f"- {g}" for g in gaps[:10])
    prompt = _REGEN_PROMPT.format(
        path=path.name,
        role=role,
        score=score,
        content=content[:6000],
        gap_list=gap_list,
    )
    try:
        raw = generate(prompt)
    except Exception:  # noqa: BLE001
        return
    new = sanitize(raw)
    if len(new) >= 20:  # don't replace with empty/near-empty
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")


def review_and_repair(
    path: Path,
    role: str,
    framework: str,
    generate: GenerateFn,
    sanitize: Callable[[str], str],
    *,
    threshold: float = 7.0,
    max_rounds: int = 2,
    log: Callable[[str], None] | None = None,
) -> ReviewResult:
    """Review → regenerate → re-review until score ≥ threshold or rounds exhausted."""
    log = log or (lambda _m: None)
    result = review_file(path, role, framework, generate)
    log(f"  [review] {path.name}: score={result.score:.1f}")
    rounds = 0
    while result.score < threshold and rounds < max_rounds:
        rounds += 1
        log(f"  [review] {path.name}: regenerating (round {rounds}, {len(result.gaps)} gaps)")
        regenerate_for_gaps(path, role, result.score, result.gaps, generate, sanitize)
        result = review_file(path, role, framework, generate)
        log(f"  [review] {path.name}: round {rounds} new score={result.score:.1f}")
    return result


__all__ = ["ReviewResult", "regenerate_for_gaps", "review_and_repair", "review_file"]
