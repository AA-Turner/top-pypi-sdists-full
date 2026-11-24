"""The One Source contract's ``SourceSet`` inside matrx-ai.

A chat turn hands its attachments over as ONE ``source_set``; the stored message
keeps it as a ``source_set`` part (``matrx_ai.db.message_parts.SourceSetPart``)
so read-back and edit-resend can show and resend it.

This module is the ONE definition of the One Source models: the host
(``aidream/services/conversation_context/resource_context.py``) imports them from
here rather than keeping a copy. Parity with the host's wire behaviour is pinned by
``aidream/services/conversation_context/tests/test_source_set_part_twin.py``.
Contract: ``common-docs/systems/knowledge/projects/unified-source-input/CONTRACT.md``.

Resolution (text + media) is the HOST's job: matrx-ai calls the injected
``source_set_resolver`` seam (``matrx_ai._ext.get_source_set_resolver``).
"""

from __future__ import annotations

from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    field_validator,
    model_validator,
)

RESOURCE_REF_KIND = "resource_ref"
SOURCE_SET_KIND = "source_set"
#: The plain key naming a caller-intent envelope (amendment A6) — never ``__kind``.
ENVELOPE_KEY = "envelope"
_ENVELOPE_IN = AliasChoices(ENVELOPE_KEY, "__kind", "kind")
DEFAULT_PROMOTION_CHARS = 5_000
MAX_PROMOTION_CHARS = 10_000
#: Ref kinds whose ``resource_id`` is a provider's own id, not a platform UUID (P0a).
NON_UUID_RESOURCE_TYPES = frozenset({"google_file", "connector_resource"})
_DELIVERIES = ("direct", "context")


def normalize_uuid(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        return str(UUID(value.strip()))
    except (ValueError, AttributeError):
        return None


class ResourcePromotion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    representation: str
    max_chars: int = Field(default=DEFAULT_PROMOTION_CHARS, ge=1, le=MAX_PROMOTION_CHARS)

    @field_validator("representation")
    @classmethod
    def _normalise_representation(cls, value: str) -> str:
        value = value.strip().lower()
        if not value:
            raise ValueError("representation must not be empty")
        if len(value) > 64:
            raise ValueError("representation must be at most 64 characters")
        return value


class _SourcePartBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ColumnPart(_SourcePartBase):
    scope: Literal["column"]
    column: str = Field(min_length=1)


class RowPart(_SourcePartBase):
    scope: Literal["row"]
    row_id: str = Field(min_length=1)


class CellPart(_SourcePartBase):
    scope: Literal["cell"]
    row_id: str = Field(min_length=1)
    column: str = Field(min_length=1)


class SchemaPart(_SourcePartBase):
    scope: Literal["schema"]


class GroupPart(_SourcePartBase):
    scope: Literal["group"]
    group: str = Field(min_length=1)


class ItemPart(_SourcePartBase):
    scope: Literal["item"]
    item_id: str = Field(min_length=1)


class PagePart(_SourcePartBase):
    scope: Literal["page"]
    page: int = Field(ge=1)


class SheetPart(_SourcePartBase):
    scope: Literal["sheet"]
    sheet: str = Field(min_length=1)


class ContextCellPart(_SourcePartBase):
    scope: Literal["context_cell"]
    scope_id: str = Field(min_length=1)


SourcePart = Annotated[
    ColumnPart
    | RowPart
    | CellPart
    | SchemaPart
    | GroupPart
    | ItemPart
    | PagePart
    | SheetPart
    | ContextCellPart,
    Field(discriminator="scope"),
]


class SourceRef(BaseModel):
    """The pointer — the ``resource_ref`` envelope (v1 + P0a)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    kind: Literal["resource_ref"] = Field(
        default=RESOURCE_REF_KIND,
        validation_alias=_ENVELOPE_IN,
        serialization_alias=ENVELOPE_KEY,
    )
    resource_type: str = Field(min_length=1, max_length=64)
    resource_id: str
    representation: str | None = None
    include_segments: list[str] | None = None
    delivery: Literal["direct", "context"] | None = None
    max_chars: int | None = Field(default=None, ge=1)
    promote: ResourcePromotion | list[ResourcePromotion] | None = None
    exclude: list[str] | None = None
    label: str | None = Field(default=None, max_length=500)
    overlay: dict[str, JsonValue] | None = None
    part: SourcePart | None = None
    editable: bool | None = None
    keep_fresh: bool | None = None
    optional_context: bool | None = None
    template: Literal["full", "compact", "minimal"] | None = None
    persistence: Literal["durable", "turn"] | None = None

    @model_validator(mode="after")
    def _id_shape(self) -> SourceRef:
        if self.resource_type in NON_UUID_RESOURCE_TYPES:
            ident = self.resource_id.strip()
            if not ident or len(ident) > 512:
                raise ValueError("resource_id must be a non-empty provider id")
            self.resource_id = ident
            return self
        normal = normalize_uuid(self.resource_id)
        if normal is None:
            raise ValueError("resource_id must be a UUID")
        self.resource_id = normal
        return self

    @field_validator("resource_type", "representation")
    @classmethod
    def _token(cls, value: str | None) -> str | None:
        if value is None:
            return None
        token = value.strip().lower()
        return token or None

    @field_validator("include_segments", mode="before")
    @classmethod
    def _choices_segments(cls, value: Any) -> list[str] | None:
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError("include_segments must be a list of Segment ids")
        ids = [str(item).strip() for item in value if str(item).strip()]
        return list(dict.fromkeys(ids))

    @field_validator("delivery", mode="before")
    @classmethod
    def _choices_delivery(cls, value: Any) -> str | None:
        if value is None or value in _DELIVERIES:
            return value
        raise ValueError(f"delivery must be one of {', '.join(_DELIVERIES)}")

    @field_validator("max_chars", mode="before")
    @classmethod
    def _choices_max_chars(cls, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, int | float) or value < 1:
            raise ValueError("max_chars must be a whole number of at least 1")
        return int(value)


class SourceSet(BaseModel):
    """The one payload that carries a person's chosen Sources."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    kind: Literal["source_set"] = Field(
        default=SOURCE_SET_KIND,
        validation_alias=_ENVELOPE_IN,
        serialization_alias=ENVELOPE_KEY,
    )
    version: Literal[1] = 1
    sources: list[SourceRef] = Field(default_factory=list)
    topic: str | None = None
    grounding: Literal["whole", "selected", "retrieve"] = "whole"
    retrieve_query: str | None = None
    target_model_id: str | None = None

    def is_empty(self) -> bool:
        return not self.sources and not (self.topic or "").strip()


def dump_source_set(source_set: SourceSet) -> dict[str, Any]:
    """The stored / wire form: ``envelope`` key, no unset ``None`` noise."""
    return source_set.model_dump(mode="json", by_alias=True, exclude_none=True)


class SourceSetResolution(BaseModel):
    """What the host's ``source_set_resolver`` returns for one set.

    ``text`` is the grounded text the model reads. ``media`` are user media part
    dicts (``{"type": "media", "kind": "image" | "document" | …, "file_id": …}``)
    the model receives as real media beside the text. ``dropped`` names every
    Source the host could not deliver, with its reason — never silently skipped.
    """

    model_config = ConfigDict(extra="forbid")

    text: str = ""
    media: list[dict[str, JsonValue]] = Field(default_factory=list)
    dropped: list[dict[str, JsonValue]] = Field(default_factory=list)


__all__ = [
    "ENVELOPE_KEY",
    "NON_UUID_RESOURCE_TYPES",
    "SOURCE_SET_KIND",
    "SourcePart",
    "SourceRef",
    "SourceSet",
    "SourceSetResolution",
    "dump_source_set",
]
