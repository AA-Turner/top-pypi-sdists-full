"""The information specs (one-graph CONTRACTS §2.2). None of them executes."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.node_spec import EmptyInput, EmptyOutput, NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult

_ALL_GRAPHS = ("*",)
_FACES = ("detailed", "map", "essentials", "figure")
_REFERENCE_GRAPHS = ("workflow", "orchestra", "org_chart", "topical_map", "map", "board")


class InformationNeverRuns(RuntimeError):
    """An information node was invoked. The engine takes them out of the graph first."""


class _InfoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NoteConfig(_InfoConfig):
    text: str = Field(default="", description="The note, in markdown.")
    color: str = Field(default="yellow", description="The sticky note's color name.")


class FrameConfig(_InfoConfig):
    title: str = Field(default="", description="The frame's title.")
    color: str = Field(default="gray", description="The frame's color name.")


class MediaConfig(_InfoConfig):
    file_id: str = Field(default="", description="The file's id (a MediaRef file id, never a URL).")
    caption: str = Field(default="", description="Optional caption under the image or file card.")


class KindConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"x-contract-dynamic": "holds any registered kind value, whatever its kind is"},
    )

    value: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Any registered kind value, its __kind marker kept; drawn by that kind's component.",
    )


class RecordConfig(_InfoConfig):
    entity_type: str = Field(default="", description="The record's entity type token.")
    id: str = Field(default="", description="The record's id.")


class AgentRefConfig(_InfoConfig):
    agent_id: str = Field(default="", description="The agent this card points at.")


class WorkflowRefConfig(_InfoConfig):
    workflow_id: str = Field(default="", description="The workflow this card points at.")


class PositionRefConfig(_InfoConfig):
    position_id: str = Field(default="", description="The org-chart position this card points at.")


class TopicRefConfig(_InfoConfig):
    topic_id: str = Field(default="", description="The topical-map topic this card points at.")


def _spec(node_type: str, display_name: str, description: str, icon: str, config: type[BaseModel],
          *, allowed_graphs: tuple[str, ...] = _ALL_GRAPHS, looks: tuple[str, ...] = _FACES) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.INFO,
        display_name=display_name,
        description=description,
        input_schema=EmptyInput,
        output_schema=EmptyOutput,
        config_schema=config,
        handles=(),
        determinism=ActionTier.PURE,
        icon=icon,
        executes=False,
        looks=looks,
        allowed_graphs=allowed_graphs,
    )


class _InfoExecutor:
    """Registered so the type resolves in the palette and registry; never called."""

    spec: ClassVar[NodeSpec]

    async def execute(self, ctx: NodeExecutionContext, inputs: EmptyInput, config: Any) -> NodeResult[EmptyOutput]:
        _ = ctx, inputs, config
        raise InformationNeverRuns(f"{self.spec.node_type} is an information node and never runs")


class InfoNoteExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.note", "Sticky note", "A note on the canvas. Never runs; the workflow ignores it.", "sticky-note", NoteConfig)


class InfoFrameExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.frame", "Frame", "A titled frame around other nodes (they sit in it by parentId). Never runs.", "square-dashed", FrameConfig)


class InfoMediaExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.media", "Image or file", "An image or file card from the file library. Never runs.", "image", MediaConfig,
        looks=("detailed", "map", "essentials"))


class InfoKindExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.kind", "Shown value", "Any registered kind value, drawn by that kind's own component. Never runs.", "shapes", KindConfig,
        looks=("detailed", "map", "essentials"))


class InfoRecordExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.record", "Record", "A card for any record (a peek that opens it). Never runs.", "database", RecordConfig,
        looks=("detailed", "map", "essentials"))


class InfoAgentExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.agent", "Agent card", "A card that points at an agent. Never runs.", "bot", AgentRefConfig,
        allowed_graphs=_REFERENCE_GRAPHS, looks=("detailed", "map", "essentials"))


class InfoWorkflowExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.workflow", "Workflow card", "A card that points at a workflow. Never runs.", "workflow", WorkflowRefConfig,
        allowed_graphs=_REFERENCE_GRAPHS, looks=("detailed", "map", "essentials"))


class InfoPositionExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.position", "Position card", "A card that points at an org-chart position. Never runs.", "user-round", PositionRefConfig,
        allowed_graphs=_REFERENCE_GRAPHS, looks=("detailed", "map", "essentials"))


class InfoTopicExecutor(_InfoExecutor):
    spec: ClassVar[NodeSpec] = _spec(
        "info.topic", "Topic card", "A card that points at a topical-map topic. Never runs.", "tag", TopicRefConfig,
        allowed_graphs=_REFERENCE_GRAPHS, looks=("detailed", "map", "essentials"))


INFO_EXECUTORS: tuple[type[_InfoExecutor], ...] = (
    InfoNoteExecutor, InfoFrameExecutor, InfoMediaExecutor, InfoKindExecutor, InfoRecordExecutor,
    InfoAgentExecutor, InfoWorkflowExecutor, InfoPositionExecutor, InfoTopicExecutor,
)
