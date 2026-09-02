"""Questionnaire block data models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class QuestionnaireSection(BaseModel):
    """A section in a questionnaire."""

    model_config = _camel_config

    title: str = ""
    content: str = ""
    items: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []
    code_blocks: list[dict[str, Any]] = []
    json_blocks: list[dict[str, Any]] = []


class QuestionnaireBlockData(BaseModel):
    """Parsed questionnaire data."""

    model_config = _camel_config

    sections: list[QuestionnaireSection] = []
    raw_content: str = ""
