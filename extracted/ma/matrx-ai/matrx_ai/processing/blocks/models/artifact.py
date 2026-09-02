"""Artifact block data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ArtifactBlockData(BaseModel):
    """
    Parsed data for an artifact block from model output.

    Mirrors the frontend artifact metadata structure:
        <artifact id="artifact_1" type="iframe" title="Revenue Dashboard">
            ...content...
        </artifact>

    The frontend uses this to render canvas artifact cards and persist
    to canvas_items via cx_canvas_upsert RPC.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    artifact_id: str
    artifact_index: int
    artifact_type: str
    title: str
    content: str
