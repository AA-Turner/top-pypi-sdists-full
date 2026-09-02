"""Math problem block data models — matches features/math/types.ts in the React app."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class MathProblemStatement(BaseModel):
    model_config = _camel_config

    text: str = ""
    equation: str = ""
    instruction: str = ""


class MathSolutionStep(BaseModel):
    model_config = _camel_config

    title: str = ""
    equation: str = ""
    explanation: str | None = None
    simplified: str | None = None


class MathSolution(BaseModel):
    model_config = _camel_config

    task: str = ""
    transition_text: str | None = None
    solution_answer: str = ""
    steps: list[MathSolutionStep] = Field(default_factory=list)


class MathProblemInner(BaseModel):
    """Matches the math_problem DB schema shape that MathProblemBlock.tsx expects."""

    model_config = _camel_config

    title: str = ""
    course_name: str = ""
    topic_name: str = ""
    module_name: str = ""
    description: str | None = None
    intro_text: str | None = None
    final_statement: str | None = None
    problem_statement: MathProblemStatement = Field(default_factory=MathProblemStatement)
    solutions: list[MathSolution] = Field(default_factory=list)


class MathProblemBlockData(BaseModel):
    """
    Top-level data shape sent in block.data.

    BlockRenderer.tsx and MathProblemBlock.tsx both read problemData.math_problem
    (snake_case key), so we must preserve that exact key — NOT convert it to
    mathProblem via the camelCase generator.  The explicit alias overrides it.
    """

    model_config = _camel_config

    math_problem: MathProblemInner = Field(alias="math_problem")
