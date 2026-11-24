"""Saved reply blocks — the typed blocks of one assistant text part (PF-1, CGU-14 blocks v1).

The server's one splitter (``matrx_ai.processing.blocks.blocks_v1``) reads a text part into blocks
that tile its text. The SAME blocks are saved on the ``chat.message`` text part
(``blocks_version`` / ``blocks_of`` / ``blocks``) and streamed (the ``message_blocks`` data event),
so every client draws one representation. Lives here, below matrx-ai, because the stream contract
carries it. Lane: common-docs/systems/chat/projects/chat-ground-up/PF-1-saved-equals-streamed.md.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

BlockType = Literal["markdown", "reasoning", "kind", "data", "artifact", "decision", "protocol"]
KindStatus = Literal["valid", "repaired", "invalid", "unknown_kind", "incomplete", "unchecked"]


class _BlockBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: int = Field(ge=0)
    end: int = Field(ge=0)


class _ClosedBlockBase(_BlockBase):
    # False when the text ended inside the block (a cut-off reply, R5).
    complete: bool = True


class _BodyBlockBase(_ClosedBlockBase):
    # The span between the opening and closing tags.
    body_start: int | None = Field(default=None, ge=0)
    body_end: int | None = Field(default=None, ge=0)


class _TagBlockBase(_BodyBlockBase):
    attributes: dict[str, str] = Field(default_factory=dict)


class BlockCanvasRef(BaseModel):
    """One canvas row made from a region of a block (PF-1 D7): the region's UTF-8 byte span in the part's text,
    its position among the message's canvas regions (``canvas.canvas_items.artifact_index``) and the row's id."""

    model_config = ConfigDict(extra="forbid")

    start: int = Field(ge=0)
    end: int = Field(ge=0)
    artifact_index: int = Field(ge=1)
    artifact_id: str
    canvas_type: str
    version: int = Field(default=1, ge=1)


class _CanvasBlockBase(BaseModel):
    # PF-1 D7: the canvas rows the server's save made from this block. None = the save did not run
    # canvas materialization on it (a client may still materialize the row); [] = it ran and found nothing.
    canvas: list[BlockCanvasRef] | None = None


#: What a region is: the saved ``type`` (code | table) refined by the fence language (P1-CHAT T1 v2.1).
RegionKind = Literal["code", "table", "mermaid", "svg", "html", "math"]


class MarkdownRegion(BaseModel):
    """A fenced code block or GFM table inside a markdown block (PF-1 D9), read by a standard GFM parser
    when the block closes: UTF-8 byte span in the part's text (whole lines, fences included) and, for code,
    the info string's first word."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["code", "table"]
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    language: str | None = None
    # T1 v2.1 STAGED: written only while `platform.debug.blocks_v2_save_enabled` is on (OFF until every
    # installed reader's decoder accepts them). Absent otherwise — never null.
    region_kind: RegionKind | None = None
    display: str | None = None
    complete: bool | None = None


class MarkdownBlock(_BlockBase, _CanvasBlockBase):
    type: Literal["markdown"]
    # PF-1 D9. None = saved before regions were read; [] = read, none found.
    regions: list[MarkdownRegion] | None = None


class ReasoningBlock(_BodyBlockBase):
    type: Literal["reasoning"]
    tag: str
    # T1 v2.1 STAGED: the title the server names for the grounded digest ("Research notes"), written only while
    # `platform.debug.blocks_v2_save_enabled` is on. Absent otherwise — never null.
    label: str | None = None


class SavedDecisionOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: str
    text: str


class SavedDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    prompt: str
    options: list[SavedDecisionOption] = Field(default_factory=list)


class DecisionBlock(_TagBlockBase):
    type: Literal["decision"]
    questions: list[SavedDecision] = Field(default_factory=list)


class ArtifactBlock(_TagBlockBase, _CanvasBlockBase):
    type: Literal["artifact"]
    artifact_id: str | None = None
    version: str | None = None
    artifact_type: str | None = None
    title: str | None = None


class ProtocolBlock(_TagBlockBase):
    type: Literal["protocol"]
    tag: str
    # The registered kind the protocol tag maps to, once one exists.
    kind: str | None = None


class KindBlockItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str | None = None
    kind_version: int | None = None
    status: KindStatus | None = None
    errors: list[str] = Field(default_factory=list)


class KindBlock(_ClosedBlockBase, _CanvasBlockBase):
    type: Literal["kind"]
    kind: str | None = None
    kind_version: int | None = None
    array: bool = False
    # The instance as written (or repaired — never the text); keeps its `__kind`.
    value: JsonValue = None
    status: KindStatus = "unchecked"
    errors: list[str] = Field(default_factory=list)
    items: list[KindBlockItem] | None = None


class DataBlock(_ClosedBlockBase):
    type: Literal["data"]
    schema_name: str | None = None
    value: JsonValue = None


SavedBlock = Annotated[
    MarkdownBlock | ReasoningBlock | KindBlock | DataBlock | ArtifactBlock | DecisionBlock | ProtocolBlock,
    Field(discriminator="type"),
]


# ── blocks2: the full server reading of a text part (P1-CHAT T1 v2.1, the saved half of blocks v2) ─────────────
#
# A NEW key beside the unchanged v1 fields (`blocks_version` / `blocks_of` / `blocks`), so an installed reader that
# decodes v1 never meets a field it does not declare: the phones read saved parts by named keys (unknown keys
# ignored) and the web strips undeclared top-level part keys. Written only while
# `platform.debug.blocks_v2_save_enabled` is on. The database drops it when `of` is not md5 of the part's text
# (trigger chat.zz_blocks_are_derived).


class SavedRegion2(BaseModel):
    """A region of a markdown block as the live v2 reader announces it: UTF-8 byte span in the part's text (whole
    lines), what it is (`region_kind`), the drawer (`display`), nesting (`container`) and whether it closed."""

    model_config = ConfigDict(extra="forbid")

    region_kind: RegionKind
    display: str
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    language: str | None = None
    container: list[Literal["list_item", "blockquote"]] | None = None
    # False: the text ended inside it (a fence never closed, a stopped reply's open region).
    complete: bool = True


class MarkdownBlock2(MarkdownBlock):
    regions: list[SavedRegion2] = Field(default_factory=list)  # type: ignore[assignment]
    # False when the text ended inside it: a region left open, or the open block of a stopped reply.
    complete: bool = True


SavedBlock2 = Annotated[
    MarkdownBlock2 | ReasoningBlock | KindBlock | DataBlock | ArtifactBlock | DecisionBlock | ProtocolBlock,
    Field(discriminator="type"),
]


class SavedBlocks2(BaseModel):
    """`blocks2` on a saved text part: the server's whole reading of that part's text — the same object the live
    v2 events build and `message_blocks` carries, so live and saved are one."""

    model_config = ConfigDict(extra="forbid")

    version: Literal[2] = 2
    # md5 of the part's text as stored (Postgres `md5(text)`): blocks2 for other text is dropped by the database.
    of: str = Field(pattern=r"^[0-9a-f]{32}$")
    blocks: list[SavedBlock2]
    # The part's citations (`NormalizedCitation`, answer offsets into this text).
    citations: list[dict[str, JsonValue]] | None = None
    # True on the last text part of a reply the person stopped: its open block and region say `complete: false`.
    stopped: bool | None = None


class SavedTextPartBlocks(BaseModel):
    """One saved text part as the stream announces it: its index in the message, its stored text and blocks."""

    model_config = ConfigDict(extra="forbid")

    index: int = Field(ge=0)
    id: str = ""
    text: str
    blocks_version: int = Field(ge=1)
    blocks_of: str = Field(pattern=r"^[0-9a-f]{32}$")
    blocks: list[SavedBlock]
    # True when a tool call follows this text in the same message: a note between steps, drawn as a
    # progress note, never as the answer (matrx_ai.processing.blocks.interim_text).
    interim: bool = False
    # T1 v2.1 STAGED: the part's citations, sent only while `platform.debug.blocks_v2_save_enabled` is on.
    citations: list[dict[str, JsonValue]] | None = None
    # The part's full server reading (P1-CHAT T1 v2.1), present only while the v2 save knob is on.
    blocks2: SavedBlocks2 | None = None


__all__ = [
    "ArtifactBlock",
    "BlockCanvasRef",
    "BlockType",
    "DataBlock",
    "DecisionBlock",
    "KindBlock",
    "KindBlockItem",
    "KindStatus",
    "MarkdownBlock",
    "MarkdownBlock2",
    "MarkdownRegion",
    "ProtocolBlock",
    "ReasoningBlock",
    "SavedBlock",
    "SavedBlock2",
    "SavedBlocks2",
    "SavedRegion2",
    "SavedDecision",
    "SavedDecisionOption",
    "SavedTextPartBlocks",
]
