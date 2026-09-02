"""``item_presentation`` block data model.

Shape mirrors the live ``content_ir.kind_definition`` schema for the
``item_presentation`` kind: a clickable reference to a platform entity
(agent, note, task, file, ...). ``type`` is the only required field —
the renderer handles unknown types via a neutral fallback.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ItemPresentationBlockData(BaseModel):
    model_config = _camel_config

    type: str
    id: str | None = None
    name: str | None = None
    about: str | None = None
    additional_details: dict[str, Any] | None = Field(default=None)
