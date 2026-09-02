"""Diagram block data models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Position(BaseModel):
    """2D position for a node."""

    x: float
    y: float


class DiagramNode(BaseModel):
    """A single node in a diagram."""

    model_config = _camel_config

    id: str
    label: str
    type: str | None = None
    node_type: str = "default"
    description: str | None = None
    details: str | None = None
    position: Position | None = None


class DiagramEdge(BaseModel):
    """A single edge connecting two nodes."""

    model_config = _camel_config

    id: str
    source: str
    target: str
    label: str | None = None
    type: str = "default"
    color: str | None = None
    dashed: bool = False
    stroke_width: float = 2


class DiagramLayout(BaseModel):
    """Layout configuration."""

    direction: Literal["TB", "LR", "BT", "RL"] = "TB"
    spacing: float = 100


class DiagramBlockData(BaseModel):
    """Parsed diagram data."""

    title: str
    description: str | None = None
    type: Literal["flowchart", "mindmap", "orgchart", "network", "system", "process"] = "flowchart"
    # When the LLM emitted a type OUTSIDE the literal set, `type` is degraded
    # to "flowchart" and the original string is preserved here (zero data
    # loss). Unknown to the diagram_spec kind schema, so it travels in the
    # envelope's residue channel rather than root.value. Excluded from dumps
    # when unset so ordinary diagrams keep their established payload shape.
    requested_type: str | None = Field(default=None, exclude_if=lambda v: v is None)
    nodes: list[DiagramNode] = []
    edges: list[DiagramEdge] = []
    layout: DiagramLayout = DiagramLayout()
