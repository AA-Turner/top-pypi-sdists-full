"""``schema_proposal`` block data model — an output-schema proposal."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

_camel_config = ConfigDict(populate_by_name=True)


class SchemaProposalBlockData(BaseModel):
    model_config = _camel_config

    name: str
    # ``schema`` shadows a BaseModel attribute, so the wire name is an alias.
    json_schema: dict[str, Any] = Field(alias="schema")
    strict: bool | None = None
