"""Quiz block data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class QuizQuestion(BaseModel):
    """A single multiple-choice question."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: int
    question: str
    options: list[str]
    correct_answer: int = Field(description="Index into options")
    explanation: str


class QuizBlockData(BaseModel):
    """Parsed quiz data — serialized with camelCase keys for client consumption."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    quiz_title: str
    category: str | None = None
    multiple_choice: list[QuizQuestion]
