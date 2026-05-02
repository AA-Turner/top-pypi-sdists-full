from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator
from zoneinfo import ZoneInfo

from ..content_messages import MetaTextContent, MetaImageContent, MetaStickerContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaContactContent, MetaLocationContent, MetaSystemContent, MetaOrderContent, MetaInteractiveContent, MetaButtonContent, MetaReactionContent
from .....utils.types import MessageType
from .value_errors import Error
class MetaReferral(BaseModel):
    source_url: str
    source_id: Optional[str] = Field(default=None)
    source_type: Optional[str] = Field(default=None)
    headline: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    media_type: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    video_url: Optional[str] = Field(default=None)
    thumbnail_url: Optional[str] = Field(default=None)
    ctwa_clid: Optional[str] = Field(default=None)

class ReferredProduct(BaseModel):
    catalog_id: str
    product_retailer_id: str

class MetaContext(BaseModel):
    from_: Optional[str] = Field(default=None, alias="from")
    id: Optional[str] = Field(default=None)
    forwarded: Optional[bool] = Field(default=False)
    referred_product : Optional[ReferredProduct] = Field(default=None)

    @model_validator(mode='after')
    def validate_from_and_id(self):
        if self.from_ is not None and self.id is None:
            raise ValueError("id is required when from_ is provided")
        if self.from_ is None and self.id is not None:
            raise ValueError("from_ is required when id is provided")
        return self


class Message(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: datetime
    type: MessageType
    context: Optional[MetaContext] = Field(default=None)
    referral: Optional[MetaReferral] = Field(default=None)
    text: Optional[MetaTextContent] = Field(default=None)
    image: Optional[MetaImageContent] = Field(default=None)
    audio: Optional[MetaAudioContent] = Field(default=None)
    document: Optional[MetaDocumentContent] = Field(default=None)
    video: Optional[MetaVideoContent] = Field(default=None)
    sticker: Optional[MetaStickerContent] = Field(default=None)
    location: Optional[MetaLocationContent] = Field(default=None)
    contacts: Optional[List[MetaContactContent]] = Field(default=None)
    system: Optional[MetaSystemContent] = Field(default=None)
    interactive: Optional[MetaInteractiveContent] = Field(default=None)
    order: Optional[MetaOrderContent] = Field(default=None)
    button: Optional[MetaButtonContent] = Field(default=None)
    errors: Optional[List[Error]] = Field(default=None)
    unsupported: Optional[Dict[str, Any]] = Field(default=None)
    reaction: Optional[MetaReactionContent] = Field(default=None)

    @field_serializer('timestamp')
    def serialize_timestamp(self, timestamp: datetime) -> str:
        return timestamp.isoformat()

    @field_validator('timestamp')
    def ensure_utc(cls, v):
        if isinstance(v, str):
            v = datetime.fromtimestamp(int(v))
        if isinstance(v, datetime):
            return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
        raise ValueError('must be a datetime')

    def get_content(self) -> Optional[Union[MetaTextContent, MetaImageContent, MetaStickerContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaContactContent, MetaButtonContent, List[Error], MetaSystemContent, MetaLocationContent]]:
        return getattr(self, self.type.value)

    # Metodos para entender el mensaje en base a context y referral
    def is_response_to_specific_message(self) -> bool:
        """Determina si el mensaje es una respuesta a un mensaje específico anterior"""
        return self.context is not None and self.context.id is not None

    def is_interaction_from_button_or_menu(self) -> bool:
        """Determina si el mensaje proviene de una interacción con un botón o menú"""
        return False
        # return self.context is not None and self.context.interaction_type in ['button_press', 'menu_selection']

    def is_response_to_app_event(self) -> bool:
        """Determina si el mensaje es una respuesta a un evento dentro de una aplicación"""
        return False
        # return self.context is not None and self.context.interaction_type == 'app_event'

    def is_initiated_by_campaign_link(self) -> bool:
        """Determina si el mensaje fue iniciado por un enlace de campaña."""
        return self.referral is not None and self.referral.source_type is not None and 'campaign' in self.referral.source_type

    def is_after_ad_interaction(self) -> bool:
        """Determina si el mensaje fue enviado después de interactuar con un anuncio."""
        return self.referral is not None and self.referral.source_type is not None and 'ad' in self.referral.source_type

    def is_from_web_redirection(self) -> bool:
        """Determina si el mensaje proviene de una redirección web."""
        return self.referral is not None and self.referral.source_type is not None and 'web_redirection' in self.referral.source_type

