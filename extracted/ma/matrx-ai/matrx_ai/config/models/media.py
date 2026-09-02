"""Pydantic twins for the five media content blocks (Phase 1b.2).

Shadowed, not swapped. Retirement Ledger row 5.

THE FIRST FAMILY THE CORPUS FOUND CLEAN — and that is worth stating plainly,
because three of the four shapes measured before it hid a declared type that was
false. Here nothing is. All 1,109 stored media blocks were measured
(FIELD_TRUTH.md §4c) and:

  * only FOURTEEN distinct keys are ever persisted, against 73 declared field
    slots across the five classes — the stored surface is far narrower than the
    in-memory one, and every unpersisted field is genuinely in-memory
    (resolver state, transcription options, vision hints);
  * every stored key is MONOMORPHIC — one JSON type each, no `text`-style
    surprise;
  * every declared type agrees with what is stored.

Two apparent anomalies were checked and are NOT defects:

  * `size_bytes` is stored but no class declares it — it is the `file_size`
    field under a renamed storage key, and `reconstruct_media_content` reads it
    back with a `size_bytes` → `file_size` fallback.
  * `origin` is stored on 1,030 blocks and no class declares it either — it is
    DERIVED on write (`"matrx" if self.file_id else "external"`) so a reader can
    tell hosted from external without inspecting, and recomputed on every write.
    Nothing to restore.

STORAGE SPELLING ≠ MEMORY SPELLING, deliberately. On the wire a media block is
`{"type": "media", "kind": "image", ...}`; in memory it is
`ImageContent(type="image")`. The `kind` discriminator has no field on any class
— `reconstruct_media_content` dispatches on it and then constructs the right
type. Same boundary as `code_exec` ↔ `code_execution`. The twins model the
IN-MEMORY shape, which is what the dataclasses are.

Because the declared types are verified correct here, these twins are a faithful
transcription rather than a corpus re-derivation — and
`test_media_block_parity.py` asserts field names, order, defaults AND annotations
against the dataclasses, so a transcription slip fails mechanically instead of
surviving into a flip.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

_BLOCK = ConfigDict(extra="forbid", validate_assignment=False, arbitrary_types_allowed=True)


class ImageContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["image", "input_image"] = "image"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None
    mime_type: str | None = None
    media_resolution: str | None = None
    alt: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    width: int | None = None
    height: int | None = None
    vision_class: str | None = None
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None


class AudioContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["audio", "input_audio"] = "audio"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None
    mime_type: str | None = None
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None
    auto_transcribe: bool = False
    transcription_model: str = "stt-default"
    duration_ms: int | None = None
    transcription_language: str | None = None
    transcription_result: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class VideoContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["video", "input_video"] = "video"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None
    mime_type: str | None = None
    video_metadata: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    width: int | None = None
    height: int | None = None
    duration_ms: int | None = None
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None


class DocumentContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["document", "input_document"] = "document"
    url: str | None = None
    base64_data: str | None = None
    file_uri: str | None = None
    file_id: str | None = None
    mime_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    width: int | None = None
    height: int | None = None
    page_count: int | None = None
    resolved_url: str | None = None
    file_size: int | None = None
    owner_id: str | None = None
    is_ours: bool = False
    is_resolved: bool = False
    resolver_error: str | None = None


class YouTubeVideoContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["youtube_video"] = "youtube_video"
    url: str = ""
    video_metadata: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
