from __future__ import annotations
from pydantic import Field, ConfigDict, field_validator
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
    creative_mirror_url: Optional[str] = Field(default=None, description="Nuestra copia del creativo en S3. Las URLs del CDN de Meta van firmadas con vencimiento en `oe=` (~7 dias): la que se guarda al crear la fuente muere sola, y el chat se queda sin imagen aunque el anuncio siga vivo. Esta apunta a nuestro bucket y no caduca. La original se conserva al lado para trazabilidad.")

    @field_validator("meta_ad_url", "meta_referral_type", "meta_body",
                     "meta_headline", "meta_media_type", mode="before")
    @classmethod
    def _coerce_none_to_empty(cls, v: object) -> object:
        # Meta sends these Click-to-WhatsApp referral fields as null for ads that
        # lack that element (e.g. image-only ads have no body/headline, some
        # formats have no media_type). ChattyReferral types them Optional, but
        # these PureAd fields are `str`, and pydantic v2 rejects an explicit None
        # for a `str` field even when default="" — the default only applies when
        # the key is ABSENT, not when it's present-but-null. Coerce None -> "" so
        # a legitimate ad with missing text doesn't 500 the webhook.
        return "" if v is None else v

    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"meta_ad_url", "meta_referral_type", "meta_body", "meta_headline", "meta_media_type", "meta_video_url", "meta_image_url", "meta_thumbnail_url"}
    }

    @property
    def default_category(self) -> str:
        return "Anuncios Click to WhatsApp (META)"

    @property
    def type(self) -> SourceType:
        return SourceType.PURE_AD

    def __eq__(self, other: object) -> bool:
        # Type-strict on purpose. `hasattr(other, "ad_id")` used to make this match
        # PureAdUtmSource and GoogleAdUtmSource too, so the SAME ad served through two
        # entry paths looked like a duplicate to SourcesAndTopicsValidator. That is a
        # normal, system-created pair: a Meta ad pointing at the web gets a WhatsApp
        # button bolted on, so web visitors land on a PureAdUtmSource (AD_ID_IN_UTM_PARAMS
        # checker) while button-tappers arrive as a CTWA referral on a PureAd (REFERRAL
        # checker, auto-created by referral_checker.create_not_loaded_pure_ad). They live
        # in different matcher pools and cannot serve each other's traffic. Treating them
        # as duplicates made both permanently uneditable and blocked merging them.
        if not isinstance(other, PureAd):
            return False
        return bool(self.ad_id and other.ad_id and self.ad_id == other.ad_id)

    def __hash__(self) -> int:
        return hash(self.ad_id)