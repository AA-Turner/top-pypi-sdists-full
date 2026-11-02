from pydantic import Field, field_validator, model_validator
from datetime import datetime, timedelta
from typing import Optional
from ...base_models import CompanyAssetModel
from ...utils.types.identifier import StrObjectId
from ...analytics.sources import Source
from ...analytics.sources.utms.referer_info import RefererInfo
from ...analytics.sources.utms.referer_info import DeviceType
from ...analytics.sources.utms.pixel_attribution import PixelAttribution
from ...analytics.sources.ad_creative import AdCreative
from ...utils.types.source_types import SourceCheckerType
from .inferred_attribution import InferredAttribution

class ContactPoint(CompanyAssetModel):
    account_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "The WhatsApp account (number) this touchpoint happened on: its chat's account, or, when there is no chat "
            "yet (a pixel click, an enviamewhats.app link), the account of the topic that opened the number, or the "
            "company's default account at the moment of the click. Written when the touchpoint is created, stamped on "
            "matching only if missing, never overwritten. A touchpoint is never matched to a chat or a source of "
            "another account. Absent = the default account's (touchpoints from before accounts)."
        ),
    )
    source_checker_method : Optional[SourceCheckerType] = Field(default=None)
    source_id: Optional[StrObjectId] = Field(default=None)
    template_name : Optional[str] = Field(default=None)
    match_timestamp: Optional[datetime] = Field(default=None)
    referer_info: Optional[RefererInfo] = Field(default=None)
    time_from_request_to_match : Optional[timedelta] = Field(default=None)
    topic_id : Optional[StrObjectId] = Field(default=None)
    chat_id : Optional[StrObjectId] = Field(default=None)
    message_id : Optional[str] = Field(default=None)
    ctwa_clid : Optional[str] = Field(default=None)
    fb_clid : Optional[str] = Field(default=None)
    gclid : Optional[str] = Field(default=None)
    # Browser-only Meta cookies: they cannot be derived server-side, so if the
    # pixel didn't capture them here they are gone for good.
    fbc : Optional[str] = Field(default=None)
    fbp : Optional[str] = Field(default=None)
    attribution : Optional[PixelAttribution] = Field(default=None, description="Full chatty_pixel v6+ attribution snapshot")
    ad_creative : Optional[AdCreative] = Field(default=None, description="El creativo que Meta sirvió en ESTE referral, copiado al ingresar. Va acá y no en la fuente porque un mismo `ad_id` sirve varios creativos —anuncios dinámicos, catálogo, carrusel, o el anuncio editado— y en la fuente gana el del primer lead: los demás chats terminan mostrando una imagen y un texto que no son los suyos. Vacío en los touchpoints anteriores a esto y en los que no vienen de un anuncio; ahí la lectura cae al creativo de la fuente, que es lo mejor que hay.")
    client_ip_address : Optional[str] = Field(default=None)
    client_user_agent : Optional[str] = Field(default=None)
    client_external_id : Optional[str] = Field(default=None)
    button_id : Optional[str] = Field(default=None)
    button_name : Optional[str] = Field(default=None)
    device_type : Optional[DeviceType] = Field(default=None)
    inferred_attribution : Optional[InferredAttribution] = Field(default=None)
    new_chat : bool = Field(default=False)
    matched : bool = Field(default=False)
    expired : bool = Field(default=False)

    @field_validator("account_id", mode="before")
    @classmethod
    def _blank_account_is_none(cls, value):
        """`StrObjectId` rejects the empty string."""
        return value or None

    # @model_validator(mode="before")
    # def validate_source_id_or_template_name(cls, data):
    #     if data.get("source_id") is None and data.get("template_name") is None:
    #         raise ValueError("source_id or template_name is required")
    #     return data

    def __lt__(self, other: 'ContactPoint') -> bool:
        """Compare two ContactPoint instances based on their match_timestamp."""
        if self.match_timestamp is None or other.match_timestamp is None:
            return super().__lt__(other)
        return self.match_timestamp < other.match_timestamp

    def __gt__(self, other: 'ContactPoint') -> bool:
        """Compare two ContactPoint instances based on their match_timestamp."""
        if self.match_timestamp is None or other.match_timestamp is None:
            return super().__gt__(other)
        return self.match_timestamp > other.match_timestamp

    @property
    def matched_source_id(self) -> StrObjectId:
        if not self.source_id:
            raise ValueError("Source ID is not set")
        return self.source_id

    @property
    def locked_topic_id(self) -> StrObjectId:
        if not self.topic_id:
            raise ValueError("No topic id found for contact point")
        return self.topic_id