from letschatty.models.company.integrations.shopify.company_shopify_integration import ShopifyIntegration
from letschatty.models.company.integrations.tienda_nube.company_tienda_nube_integration import TiendaNubeIntegration
from pydantic import Field, ConfigDict, field_validator, SecretStr, model_validator
from typing import Optional, List, Dict
from datetime import datetime

from letschatty.models.chat.client import QualityScore
from letschatty.models.company.company_messaging_settgins import MessagingSettings
from ..base_models import ChattyAssetModel
from letschatty.models.channels.channel import WhatsAppClientInfo
from letschatty.models.utils.types import StrObjectId

class EmpresaModel(ChattyAssetModel):
    name: str = Field(description="The name of the company")
    frozen_name: str = Field(description="The frozen name of the company", frozen=True)
    industry: Optional[str] = Field(default = "")
    url: Optional[str] = Field(default = "")
    allowed_origins: list[str] = Field(default_factory=lambda: [])
    company_email: Optional[str] = Field(default = "")
    contributor_count: Optional[str] = Field(default = "")
    purpose_of_use_chatty: Optional[List[str]] = Field(default_factory=lambda: [])
    current_wpp_approach: Optional[str] = Field(default = "")
    main_reason_to_use_chatty: Optional[str] = Field(default = "")
    active: Optional[bool] = Field(default = True)
    friendly_aliases: list[str] = Field(description="The friendly aliases of the company used for the enviamewhats.app links", default_factory=lambda: [])
    terms_of_service_agreement: Optional[bool] = Field(default = False)
    display_phone_number: str = Field(description="The display phone number user's write to", default = "33333333333333", alias="display_phone_number")
    phone_number_id: Optional[str] = Field(description="The phone number id of the company", alias="phone_number_id", default = None)
    business_account_id: Optional[str] = Field(description="The WABA - WhatsApp Business Account id of the company", default = None, alias="bussiness_account_id")
    photo_url: str = Field(default = "")
    meta_token: Optional[str] = Field(default = None, alias="meta_token")
    disconnected_at: Optional[datetime] = Field(default=None, alias="disconnected_at", description="UTC timestamp when the WhatsApp connection was lost (e.g. coexistence removed from the WhatsApp app → PARTNER_REMOVED). None while connected; cleared on any (re)connection. When set, the company is treated as NOT connected.")
    slack_channels: Dict[str,Dict[str,str]] = Field(default_factory=lambda:{})
    phone_numbers_for_testing: list[str] = Field(default_factory=lambda: [])
    analytics : Optional[bool] = Field(default = True)
    dataset_id: Optional[str] = Field(default = None, description="To notify events to Meta Conversions API")
    hammer_credentials: Optional[Dict[str,str]] = Field(default = None, description="Only usef for hammer propiedades real state agencies")
    continuous_conversation_template_name: Optional[str] = Field(default = None, description="The name of the continuous conversation template")
    default_follow_up_strategy_id: Optional[StrObjectId] = Field(default = None, description="The id of the default follow up strategy")
    messaging_settings: MessagingSettings = Field(default = MessagingSettings(), description="The messaging settings for the company")
    is_test_group: bool = Field(default = False, description="Mark this company as part of an internal experiment / test cohort (set from the backoffice). Surfaced as a lab badge in company pickers.")
    test_label: Optional[str] = Field(default = None, description="Free-text label naming the experiment/test cohort this company belongs to (shown as the lab badge tooltip).")
    internal_use: bool = Field(default = False, description="Mark this company as an internal / legacy self-made account (set from the backoffice). Suppresses the 'missing contract' prompts across the Empresas UI — it is not a real client.")
    internal_note: Optional[str] = Field(default = None, description="Free-text note for an internal_use company (e.g. why it exists / who owns it).")
    betas: list[str] = Field(default_factory=lambda: [], description="Keys of the beta features enabled for this company (set from the backoffice by a mega admin, e.g. 'flujo_de_atencion'). Empty by default.")
    organization_id: Optional[str] = Field(default = None, description="Opaque group id linking companies that belong together (same business with several numbers, or same owner across businesses). Set from the backoffice. Companies sharing this id are 'the same client / org'.")
    organization_relation: Optional[str] = Field(default = None, description="Why this company is linked to its organization: 'same_company' (misma empresa, otro número), 'same_owner' (mismos dueños, distinta empresa), or 'other'.")
    organization_note: Optional[str] = Field(default = None, description="Free-text detail for the organization link (used when organization_relation is 'other', or extra context).")
    shopify_integration: ShopifyIntegration = Field(default = ShopifyIntegration(), description="The Shopify integration for the company")
    tienda_nube_integration: TiendaNubeIntegration = Field(default = TiendaNubeIntegration(), description="The Tienda Nube integration for the company")

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
                )


    @field_validator("display_phone_number", mode="before")
    def validate_display_phone_number(cls, v):
        if v is None:
            return "33333333333333"
        return v

    @model_validator(mode="before")
    def validate_frozen_name(cls, data: Dict) -> Dict:
        if "frozen_name" not in data:
            data["frozen_name"] = data["name"].replace(" ", "_")
        return data

    @model_validator(mode="before")
    def reconcile_business_account_id_alias(cls, data: Dict) -> Dict:
        """Backward-compat for the historically-misspelled ``bussiness_account_id`` alias.

        Un documento puede traer LAS DOS claves, y no por accidente: los dos serializadores del
        modelo base no coinciden. ``model_dump`` fuerza ``by_alias=True`` (escribe la mal escrita, y
        es la que va a la caché de Redis) mientras que ``model_dump_json`` NO lo fuerza (escribe la
        bien escrita, y es la que persiste a Mongo). Como el guardado usa ``$set``, que nunca borra
        claves ajenas, **Mongo escribe una clave y jamás toca la otra**: la mal escrita queda
        congelada con el valor que tuviera el día que se creó.

        Mientras la WABA no cambia nadie lo nota, porque las dos dicen lo mismo. Cuando la empresa
        reconecta contra otra cuenta de Meta, la nueva se guarda en la bien escrita y se sigue
        leyendo la vieja de la otra: la sincronización de plantillas pide una WABA muerta y Meta
        contesta 400. Medido en producción el 2026-09-14: de 385 empresas, 3 con las dos claves en
        conflicto y en las 2 vivas la bien escrita era la única que respondía en Meta. Cero casos al
        revés — lo esperable, porque la mal escrita no la escribe nadie.

        Por eso la bien escrita GANA siempre que tenga valor, en vez de sólo cuando la otra está
        vacía: es la que el guardado mantiene al día. La mal escrita sólo manda cuando es la única
        que hay (documentos viejos que nunca se volvieron a guardar), que es exactamente su rol de
        compatibilidad. Sin renombrar el campo y sin migración: los documentos partidos se curan al
        leerse.
        """
        if isinstance(data, dict):
            if data.get("business_account_id"):
                data["bussiness_account_id"] = data["business_account_id"]
        return data

    @field_validator("name", mode="before")
    def validate_name(cls, v):
        return v

    @property
    def default_follow_up_strategy_id_value(self) -> StrObjectId:
        if self.default_follow_up_strategy_id is None:
            raise ValueError(f"default_follow_up_strategy_id is not set for company {self.name}")
        return self.default_follow_up_strategy_id

    @property
    def active_continuous_conversation_template_name(self) -> str:
        if not self.continuous_conversation_template_name:
            raise ValueError(f"continuous_conversation_template_name is not set for company {self.name}")
        return self.continuous_conversation_template_name

    @property
    def waba_id_value(self) -> str:
        if self.business_account_id is None:
            raise ValueError(f"business_account_id is not set for company {self.name}")
        return self.business_account_id

    @property
    def phone_number_id_value(self) -> str:
        if self.phone_number_id is None:
            raise ValueError(f"phone_number_id is not set for company {self.name}")
        return self.phone_number_id

    @property
    def meta_token_value(self) -> str:
        if self.meta_token is None:
            raise ValueError(f"meta_token is not set for company {self.name}")
        return self.meta_token


    @property
    def whatsapp_channel(self) -> WhatsAppClientInfo:
        if self.active_for_messaging:
            return WhatsAppClientInfo(
                display_phone_number=self.display_phone_number_value,
                business_phone_number_id=self.phone_number_id_value,
                waba_id=self.waba_id_value,
                access_token=SecretStr(self.meta_token_value),
                dataset_id=self.dataset_id
            )
        else:
            raise ValueError(f"Company {self.name} is not active for messaging")

    @property
    def friendly_alias(self):
        return self.friendly_aliases[0]

    @property
    def display_phone_number_value(self):
        if self.display_phone_number is None:
            raise ValueError(f"display_phone_number is not set for company {self.name}")
        return self.display_phone_number

    @property
    def active_for_messaging(self) -> bool:
        try:
            self.meta_token_value
            self.phone_number_id_value
            self.waba_id_value
            self.display_phone_number_value
            return True
        except ValueError:
            return False

    @property
    def good_quality_score_definition(self) -> str | None:
        return self.messaging_settings.good_quality_score_definition

    @property
    def meta_status(self) -> dict:
        return {
            "meta_token": self.meta_token is not None,
            "phone_number_id": self.phone_number_id,
            "waba_id": self.business_account_id,
            "display_phone_number": self.display_phone_number,
            "active_for_messaging": self.active_for_messaging,
            "disconnected_at": self.disconnected_at.isoformat() if self.disconnected_at else None
        }