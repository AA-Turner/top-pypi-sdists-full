from __future__ import annotations
from pydantic import Field, ConfigDict
from typing import Optional
from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.types.serializer_type import SerializerType
class PureAd(SourceBase):
    ad_id: str
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.REFERRAL)
    meta_ad_url: str = Field(default="")
    meta_referral_type: str = Field(default="")
    meta_body: str = Field(default="")
    meta_headline: str = Field(default="")
    meta_media_type: str = Field(default="")
    meta_video_url: Optional[str] = Field(default=None)
    meta_image_url: Optional[str] = Field(default=None)
    meta_thumbnail_url: Optional[str] = Field(default=None)

    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"meta_ad_url", "meta_referral_type", "meta_body", "meta_headline", "meta_media_type", "meta_video_url", "meta_image_url", "meta_thumbnail_url"}
    }

    @property
    def default_category(self) -> str:
        return "Anuncios Click to WhatsApp (META)"

    @property
    def type(self) -> SourceType:
        return SourceType.PURE_AD

    def __eq__(self, other: PureAd) -> bool:
        if hasattr(other, "ad_id"):
            return self.ad_id == other.ad_id
        return False

    def __hash__(self) -> int:
        return hash(self.ad_id)