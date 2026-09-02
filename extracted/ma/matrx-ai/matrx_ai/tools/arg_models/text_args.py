from typing import Literal

from pydantic import BaseModel, Field


class TextAnalyzeArgs(BaseModel):
    text: str
    analysis_type: Literal["entities", "keywords", "language", "summary"] = "summary"


class RegexExtractArgs(BaseModel):
    text: str
    pattern: str
    group: int = Field(default=0, ge=0)
    find_all: bool = True
