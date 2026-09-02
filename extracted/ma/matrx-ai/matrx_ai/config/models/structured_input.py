"""Pydantic twins for the fourteen structured-input blocks (Phase 1b.2).

Shadowed, not swapped. Retirement Ledger row 6.

WHY FOURTEEN AND NOT SEVEN. The contract closure originally reached only seven
of these, because `UnifiedContent` declared seven and the walk follows
annotations. The union was wrong: `reconstruct_content` returns any of the
fourteen in STRUCTURED_INPUT_TYPE_MAP, including `WorkbookInputContent` for real
stored `input_workbook` blocks. Union fixed, closure corrected 26 → 33, and two
independent layers now reconcile the union against the registry. These are the
seven that were hiding, modelled alongside the seven that were not.

STORED TRAFFIC IS TINY AND THAT IS THE POINT OF SAYING SO: 30 blocks total —
input_notes 12, input_webpage 8, input_table 6, input_task 2, input_workbook 2.
The other nine types have NEVER been persisted. They are modelled anyway because
the deserializer can produce them and the contract must declare what it can
return; but nobody should read a green parity suite here as coverage of
production behaviour, because there is almost no production behaviour to cover.

🚨 FAILURE MODE 9 RESOLVES HERE — `_editable_tools`. The CUTOVER catalogue listed
"private attributes: silently dropped or raises" as a hypothetical. Concretely:
the dataclass declares it `field(default=..., init=False, repr=False,
compare=False)`, so it is a per-subclass CONSTANT, not a constructor parameter.
Pydantic turns a leading-underscore name into a private attribute — which is the
right model — and the catalogue warned that such an attribute is "silently
dropped or raises". Measured: a BARE pydantic model does silently drop it, but
these twins carry `extra="forbid"`, which turns that into a ValidationError. So
BOTH shapes refuse loudly (TypeError vs ValidationError) and the failure mode is
neutralised by a config choice already made for other reasons. `PrivateAttr`
preserves the per-subclass default, and a falsification test drops
`extra="forbid"` to show the silent drop is real and that the config is what
prevents it.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

_BLOCK = ConfigDict(extra="forbid", validate_assignment=False, arbitrary_types_allowed=True)


class StructuredInputBaseModel(BaseModel):
    """The six shared fields. Mirrors `_StructuredInputBase`."""

    model_config = _BLOCK

    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    editable: bool | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    # init=False on the dataclass; a per-subclass constant, never a parameter.
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset())

    def editable_tools(self) -> frozenset[str]:
        """Only an EXPLICIT editable=True injects tools — verbatim from the
        dataclass, including that None and False both inject nothing."""
        return self._editable_tools if self.editable is True else frozenset()


class _RecordReferenceInputModel(StructuredInputBaseModel):
    template: str = "full"


class AgentInputContentModel(_RecordReferenceInputModel):
    type: Literal["input_agent"] = "input_agent"
    agent_ids: list[str] = Field(default_factory=list)


class AgentAppInputContentModel(_RecordReferenceInputModel):
    type: Literal["input_agent_app"] = "input_agent_app"
    agent_app_ids: list[str] = Field(default_factory=list)


class ProjectInputContentModel(_RecordReferenceInputModel):
    type: Literal["input_project"] = "input_project"
    project_ids: list[str] = Field(default_factory=list)
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"data"}))


class TranscriptInputContentModel(_RecordReferenceInputModel):
    type: Literal["input_transcript"] = "input_transcript"
    transcript_ids: list[str] = Field(default_factory=list)
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"data"}))


class TranscriptSessionInputContentModel(_RecordReferenceInputModel):
    type: Literal["input_transcript_session"] = "input_transcript_session"
    transcript_session_ids: list[str] = Field(default_factory=list)


class ContextInputContentModel(StructuredInputBaseModel):
    type: Literal["input_context"] = "input_context"
    context_id: str = ""
    context_name: str = ""
    context_data: dict[str, Any] = Field(default_factory=dict)


class DataInputContentModel(StructuredInputBaseModel):
    type: Literal["input_data"] = "input_data"
    refs: list[dict[str, Any]] = Field(default_factory=list)


class DocumentInputContentModel(StructuredInputBaseModel):
    type: Literal["input_document"] = "input_document"
    document_ids: list[str | dict[str, Any]] = Field(default_factory=list)
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"document"}))


class ListInputContentModel(StructuredInputBaseModel):
    type: Literal["input_list"] = "input_list"
    bookmarks: list[dict[str, Any]] = Field(default_factory=list)
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"picklist"}))


class NotesInputContentModel(StructuredInputBaseModel):
    type: Literal["input_notes"] = "input_notes"
    note_ids: list[str | dict[str, Any]] = Field(default_factory=list)
    template: str = "full"
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"note"}))


class TableInputContentModel(StructuredInputBaseModel):
    type: Literal["input_table"] = "input_table"
    bookmarks: list[dict[str, Any]] = Field(default_factory=list)
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"dataset"}))


class TaskInputContentModel(StructuredInputBaseModel):
    type: Literal["input_task"] = "input_task"
    task_ids: list[str | dict[str, Any]] = Field(default_factory=list)
    template: str = "full"
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"task"}))


class WebpageInputContentModel(StructuredInputBaseModel):
    type: Literal["input_webpage"] = "input_webpage"
    urls: list[str | dict[str, Any]] = Field(default_factory=list)


class WorkbookInputContentModel(StructuredInputBaseModel):
    type: Literal["input_workbook"] = "input_workbook"
    workbook_ids: list[str | dict[str, Any]] = Field(default_factory=list)
    _editable_tools: frozenset[str] = PrivateAttr(default=frozenset({"workbook"}))


# Wire discriminator -> twin, mirroring STRUCTURED_INPUT_TYPE_MAP exactly. The
# reconciliation test asserts the two maps stay in lockstep; a new registered
# input type with no twin fails there rather than silently missing one.
STRUCTURED_INPUT_MODEL_MAP: dict[str, type[StructuredInputBaseModel]] = {
    "input_webpage": WebpageInputContentModel,
    "input_notes": NotesInputContentModel,
    "input_task": TaskInputContentModel,
    "input_table": TableInputContentModel,
    "input_list": ListInputContentModel,
    "input_data": DataInputContentModel,
    "input_context": ContextInputContentModel,
    "input_agent": AgentInputContentModel,
    "input_project": ProjectInputContentModel,
    "input_agent_app": AgentAppInputContentModel,
    "input_transcript": TranscriptInputContentModel,
    "input_transcript_session": TranscriptSessionInputContentModel,
    "input_workbook": WorkbookInputContentModel,
    "input_document": DocumentInputContentModel,
}
