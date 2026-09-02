"""Table block data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TableBlockData(BaseModel):
    """Parsed markdown table data — serialized with camelCase keys for client consumption."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    headers: list[str]
    rows: list[list[str]]
    is_complete: bool = False
    raw_markdown: str = Field(default="", description="Raw markdown for rendering flexibility")
