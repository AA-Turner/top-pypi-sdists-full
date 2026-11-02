from __future__ import annotations
from pydantic import Field, field_validator
from typing import Optional
from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.types.serializer_type import SerializerType


class MetaPostSource(SourceBase):
    """Organic Facebook/Instagram POST Click-to-WhatsApp referral (referral.source_type == "post").

    Distinct from PureAd (paid ads): a post carries a `post_id` and a permalink, and we
    preserve the post media (video/image/thumbnail) so the frontend source-detail view can
    render it. Matched/deduped by `post_id` (= referral.source_id).

    NOTE: we deliberately use `meta_referral_type` (the real field name). PureAd's factory
    historically wrote a non-existent `meta_source_type` key that got dropped — do not repeat.
    """
    post_id: str
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.REFERRAL)
    post_permalink: str = Field(default="")      # referral.source_url — "view original post" link
    meta_referral_type: str = Field(default="")  # referral.source_type, e.g. "post"
    headline: str = Field(default="")
    body: str = Field(default="")
    media_type: str = Field(default="")          # "video" | "image" | ""
    video_url: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    thumbnail_url: Optional[str] = Field(default=None)
    creative_mirror_url: Optional[str] = Field(default=None, description="Nuestra copia del creativo en S3. Las URLs del CDN de Meta van firmadas con vencimiento en `oe=` (~7 dias): la que se guarda al crear la fuente muere sola, y el chat se queda sin imagen aunque el anuncio siga vivo. Esta apunta a nuestro bucket y no caduca. La original se conserva al lado para trazabilidad.")

    @field_validator("post_permalink", "meta_referral_type", "headline", "body", "media_type", mode="before")
    @classmethod
    def _coerce_none_to_empty(cls, v: object) -> object:
        # Meta sends absent referral fields as null; these are `str`, and pydantic v2
        # rejects an explicit None even with default="". Coerce so a post with no
        # body/headline/media doesn't break parsing.
        return "" if v is None else v

    # Keep the list/preview light; the detail (FRONTEND) serializer still exposes these,
    # which is how the frontend renders the post media + permalink.
    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {
            "post_permalink", "meta_referral_type", "headline", "body",
            "media_type", "video_url", "image_url", "thumbnail_url",
        }
    }

    @property
    def default_category(self) -> str:
        return "Posteos Click to WhatsApp (META)"

    @property
    def type(self) -> SourceType:
        return SourceType.META_POST

    def __eq__(self, other: object) -> bool:
        if hasattr(other, "post_id"):
            return self.post_id == other.post_id  # type: ignore[attr-defined]
        return False

    def __hash__(self) -> int:
        return hash(self.post_id)
