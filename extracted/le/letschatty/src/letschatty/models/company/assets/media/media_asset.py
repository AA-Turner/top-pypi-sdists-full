"""Catalog row for the curated media library.

Only deliberately-saved files get a row (library uploads and promoted files).
Conversation-send uploads and received WhatsApp media stay S3-only — their URL
lives inline on the message. See api-chatty docs/image-asset-management.md.
"""
from datetime import datetime
from enum import StrEnum
from typing import Any, ClassVar, Optional

from pydantic import Field

from ....base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from .file import MediaFile, MediaType


class MediaOrigin(StrEnum):
    UPLOADED = "uploaded"   # an agent uploaded it (library upload or promoted conversation-send)
    RECEIVED = "received"   # a customer sent it; promoted into the library keeping provenance
    SYSTEM = "system"       # reserved (logos, avatars)
    # La imagen/video/documento que la empresa cargó en una PLANTILLA de Meta. La bajamos de su CDN una
    # sola vez y la guardamos acá para no depender de una URL que caduca. No es un archivo del usuario:
    # se excluye de la galería, igual que SYSTEM. Origen propio (y no SYSTEM) para poder encontrarlas y
    # refrescarlas cuando la plantilla cambie de imagen.
    TEMPLATE = "template"


class MetaCompatStatus(StrEnum):
    """Whether this asset is known to satisfy Meta's media constraints.

    Only videos are ever normalized, so this stays None for every other type — and
    for every row written before the normalizer shipped. None means "not checked",
    NOT "incompatible": the send path re-probes anything that isn't OK.
    """
    OK = "ok"                  # probed and compliant (either natively or after normalization)
    OPTIMIZING = "optimizing"  # handed off to the video-normalizer lambda; not sendable yet
    FAILED = "failed"          # normalization could not produce a compliant file


class MediaAssetPreview(ChattyAssetPreview):
    type: MediaType
    url: str
    mime_type: str
    origin: MediaOrigin
    is_starred: bool = False
    width: Optional[int] = None
    height: Optional[int] = None
    # The picker needs this to grey out a video that is still being normalized.
    meta_compat: Optional["MetaCompatStatus"] = None

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {
            "type": 1,
            "url": 1,
            "mime_type": 1,
            "origin": 1,
            "is_starred": 1,
            "width": 1,
            "height": 1,
            "meta_compat": 1,
        }

    @classmethod
    def from_asset(cls, asset: "MediaAsset") -> "MediaAssetPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            type=asset.type,
            url=asset.url,
            mime_type=asset.mime_type,
            origin=asset.origin,
            is_starred=asset.is_starred,
            width=asset.width,
            height=asset.height,
            meta_compat=asset.meta_compat,
        )


class MediaAsset(CompanyAssetModel):
    preview_class: ClassVar[type[MediaAssetPreview]] = MediaAssetPreview

    # storage
    s3_key: str
    url: str
    type: MediaType
    mime_type: str
    size_bytes: int = Field(ge=0, default=0)
    sha256: Optional[str] = Field(default=None, description="Metadata only — NOT unique, no dedup")

    # presentation
    name: str
    filename: Optional[str] = Field(default=None, description="Original filename (documents)")
    folder: Optional[str] = Field(default=None, description="None means the root/'All' folder")
    tags: list[str] = Field(default_factory=list)
    is_starred: bool = False

    # media specifics
    width: Optional[int] = None
    height: Optional[int] = None
    duration_ms: Optional[int] = None

    # Meta compatibility — videos only (see MetaCompatStatus). None on every other
    # type and on every row predating the normalizer.
    meta_compat: Optional[MetaCompatStatus] = None
    meta_compat_started_at: Optional[datetime] = Field(
        default=None,
        description=(
            "When OPTIMIZING was stamped. The lambda can die without ever calling back, "
            "so readers treat a row stuck here past the lambda timeout as FAILED rather "
            "than waiting forever."
        ),
    )

    # provenance
    origin: MediaOrigin = MediaOrigin.UPLOADED
    uploaded_by: Optional[str] = Field(default=None, description="user_id of uploader/promoter; None for seeded rows")
    source_chat_id: Optional[str] = Field(default=None, description="Set when origin=RECEIVED (save-to-library)")
    source_message_id: Optional[str] = Field(default=None, description="Set when origin=RECEIVED")
    source_url: Optional[str] = Field(default=None, description="Original URL before the library copy")
    seeded_from: Optional[str] = Field(default=None, description='"starred" | "fast_answer" | "folder" | None')

    # usage (cached sort hint — source of truth is messages carrying media_asset_id)
    use_count: int = 0
    last_used_at: Optional[datetime] = None

    @staticmethod
    def media_type_from_mime(mime_type: str) -> MediaType:
        return MediaFile._get_media_type(mime_type)

    @staticmethod
    def normalize_folder(folder: Optional[str]) -> Optional[str]:
        """The S3 layout uses 'All'/'' as the catch-all root — the catalog stores None for it."""
        if not folder:
            return None
        if folder.strip().lower() in ("", "all"):
            return None
        return folder.strip()
