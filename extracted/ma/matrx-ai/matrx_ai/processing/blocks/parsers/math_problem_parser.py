"""Math problem parser.

Accepts both snake_case and camelCase field names from the LLM, and maps
the LLM output into the shape MathProblemBlock.tsx expects.

Expected LLM JSON shape (flexible — LLMs vary widely):
    {
        "math_problem": {
            "title": "string",
            "problem": "string",          # maps → problem_statement.text
            "equation": "string",         # optional → problem_statement.equation
            "instruction": "string",      # optional → problem_statement.instruction
            "answer": "string",           # maps → solutions[0].solution_answer
            "steps": [...],               # maps → solutions[0].steps
            "explanation": "string",      # maps → solutions[0].task description
            "difficulty": "string",       # → module_name fallback
            "topic": "string",            # → topic_name
            "course": "string",           # optional → course_name
            "solutions": [                # full structured form if provided
                {
                    "task": "string",
                    "solution_answer" | "solutionAnswer": "string",
                    "steps": [
                        {"title": ..., "equation": ..., "explanation": ...}
                    ]
                }
            ]
        }
    }
"""

from __future__ import annotations

import json
import re
from typing import Any

from matrx_ai.processing.blocks.models.math_problem import (
    MathProblemBlockData,
    MathProblemInner,
    MathProblemStatement,
    MathSolution,
    MathSolutionStep,
)
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json

_CODE_BLOCK_RE = re.compile(r'```(?:json)?\s*([\s\S]*?)\s*```')


def _get(d: dict, *keys: str, default=None):
    for k in keys:
        if k in d:
            return d[k]
    return default


def parse_math_problem(content: str) -> MathProblemBlockData | None:
    """
    Parse math problem JSON into MathProblemBlockData.

    Returns None if the content is not parseable or missing the required problem.
    """
    try:
        json_content = content.strip()
        m = _CODE_BLOCK_RE.search(json_content)
        if m:
            json_content = m.group(1).strip()
        parsed = loads_block_json(json_content)
    except (json.JSONDecodeError, ValueError):
        return None

    if not isinstance(parsed, dict):
        return None

    # Accept {"math_problem": {...}} wrapper or the inner dict directly
    if "math_problem" in parsed and isinstance(parsed["math_problem"], dict):
        inner_raw = parsed["math_problem"]
    else:
        inner_raw = parsed

    problem_text = _get(inner_raw, "problem", "problem_statement", default="")
    if isinstance(problem_text, dict):
        # Already a problem_statement object
        stmt = MathProblemStatement(
            text=problem_text.get("text", ""),
            equation=problem_text.get("equation", ""),
            instruction=problem_text.get("instruction", ""),
        )
    else:
        stmt = MathProblemStatement(
            text=str(problem_text) if problem_text else "",
            equation=_get(inner_raw, "equation", default="") or "",
            instruction=_get(inner_raw, "instruction", default="") or "",
        )

    if not stmt.text:
        return None

    # Build solutions
    solutions_raw = _get(inner_raw, "solutions")
    if isinstance(solutions_raw, list) and solutions_raw:
        solutions = [_parse_solution(s) for s in solutions_raw if isinstance(s, dict)]
    else:
        # Flatten: single solution from answer + steps fields
        steps_raw = _get(inner_raw, "steps", default=[])
        steps = _parse_steps_list(steps_raw)
        answer = _get(inner_raw, "answer", "solution_answer", "solutionAnswer", default="") or ""
        explanation = _get(inner_raw, "explanation", default="") or ""
        solutions = [MathSolution(
            task=explanation or "Solution",
            solution_answer=str(answer),
            steps=steps,
        )]

    inner = MathProblemInner(
        title=_get(inner_raw, "title", default="") or "",
        course_name=_get(inner_raw, "course", "course_name", "courseName", default="") or "",
        topic_name=_get(inner_raw, "topic", "topic_name", "topicName", default="") or "",
        module_name=_get(inner_raw, "difficulty", "module_name", "moduleName", default="") or "",
        description=_get(inner_raw, "description", default=None),
        intro_text=_get(inner_raw, "intro_text", "introText", default=None),
        final_statement=_get(inner_raw, "final_statement", "finalStatement", default=None),
        problem_statement=stmt,
        solutions=solutions,
    )
    return MathProblemBlockData(math_problem=inner)


def _parse_solution(raw: dict) -> MathSolution:
    steps_raw = _get(raw, "steps", default=[])
    steps = _parse_steps_list(steps_raw)
    return MathSolution(
        task=_get(raw, "task", default="") or "",
        transition_text=_get(raw, "transition_text", "transitionText", default=None),
        solution_answer=str(_get(raw, "solution_answer", "solutionAnswer", "answer", default="") or ""),
        steps=steps,
    )


def _parse_steps_list(steps_raw: Any) -> list[MathSolutionStep]:
    if not isinstance(steps_raw, list):
        return []
    result: list[MathSolutionStep] = []
    for item in steps_raw:
        if isinstance(item, str):
            result.append(MathSolutionStep(title=item))
        elif isinstance(item, dict):
            result.append(MathSolutionStep(
                title=_get(item, "title", "description", "step", default="") or "",
                equation=_get(item, "equation", "expression", default="") or "",
                explanation=_get(item, "explanation", default=None),
                simplified=_get(item, "simplified", default=None),
            ))
    return result
