from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, computed_field

from letschatty.models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation
from .header_media import TemplateHeaderMedia
from ...utils.definitions import Area, AreaOpcionalTolerante
from ...utils.types.identifier import StrObjectId
from zoneinfo import ZoneInfo
from enum import StrEnum
import logging

if TYPE_CHECKING:
    from .required_for_frontend_templates import RequiredTemplateParameter

logger = logging.getLogger("RecipientOfTemplateCampaign")

class TemplateOrigin(StrEnum):
    FROM_CHAT = "from_chat"
    FROM_CAMPAIGN = "from_campaign"
    FROM_WORKFLOW = "from_workflow"
    FROM_CONTINUOUS_CONVERSATION = "from_continuous_conversation"
    FROM_TEMPLATES_MANAGER = "from_templates_manager"
    FROM_SCHEDULED_MESSAGES = "from_scheduled_messages"


class FilledRecipientParameter(BaseModel):
    id: str
    text: str

    @classmethod
    def from_required_template_parameters_and_recipient_dict(cls, required_template_parameters: List[RequiredTemplateParameter], recipient_dict: dict) -> List[FilledRecipientParameter]:
        logger.debug(f"Required template parameters: {required_template_parameters}")
        logger.debug(f"Recipient dict: {recipient_dict}")
        try:
            return [FilledRecipientParameter(id=parameter.id, text=recipient_dict[parameter.id]) for parameter in required_template_parameters]
        except KeyError as e:
            logger.error(f"Error in campaign creation: Missing parameter: {e} in recipient with phone number: {recipient_dict['phone_number']}")
            raise ValueError(f"Error in campaign creation: Missing parameter: {e} in recipient with phone number: {recipient_dict['phone_number']}")

class FilledButtonParameter(BaseModel):
    """El valor que completa un botón al enviar.

    `index` es la POSICIÓN del botón en el array BUTTONS de la plantilla — así lo identifica Meta, no
    por su texto ni por un id. `sub_type` dice qué clase de valor es: `url` (sufijo que se pega al
    final del enlace) o `copy_code` (el cupón que el cliente copia).
    """

    index: int
    sub_type: str
    text: str


class FilledCarouselCard(BaseModel):
    """Los valores de UNA tarjeta del carrusel.

    `index` es la posición de la tarjeta, igual que en los botones: Meta las identifica por ahí. Cada
    tarjeta tiene su propio archivo y sus propias variables — es lo que distingue un carrusel de un
    mensaje con varias imágenes.
    """

    index: int
    header_media: Optional[TemplateHeaderMedia] = None
    parameters: List[FilledRecipientParameter] = Field(default_factory=list)
    button_parameters: List["FilledButtonParameter"] = Field(default_factory=list)


class FilledTemplateData(BaseModel):
    template_name: str
    #: Multi-account: the account that sends. Stored by campaigns and scheduled messages when they
    #: are created; without it, the account of `chat_id`, and otherwise the company's default.
    account_id: Optional[StrObjectId] = None
    #: The chat the template is sent from (the chat's account sends it).
    chat_id: Optional[StrObjectId] = None
    fast_answer_id: Optional[StrObjectId] = None
    area: AreaOpcionalTolerante
    assign_to_agent: Optional[StrObjectId] = Field(default=None)
    phone_number: str | None = None
    # BSUID del destinatario. Los contactos que adoptaron username de WhatsApp
    # llegan sin telefono y solo se los puede identificar por aca. Ver
    # `recipient_identity`: el telefono manda cuando existe (Meta le da
    # precedencia), y el BSUID es el fallback.
    user_id: str | None = None
    new_contact_name: str | None = None
    parameters: List[FilledRecipientParameter] = Field(default_factory=list)
    # Archivo del encabezado, cuando la plantilla lo lleva. Meta lo trata como un parámetro más: el que
    # se subió al crear la plantilla es sólo el ejemplo de la aprobación, así que cada envío trae el suyo.
    # En una campaña es uno solo para todos los destinatarios; en un chat, el que elige el agente.
    header_media: Optional[TemplateHeaderMedia] = Field(default=None)
    header_parameters: List[FilledRecipientParameter] = Field(
        default_factory=list,
        description="Valores de las variables del encabezado de TEXTO. Misma forma que `parameters`.")
    carousel_cards: List[FilledCarouselCard] = Field(
        default_factory=list, description="Los valores de cada tarjeta del carrusel, si la plantilla lo lleva.")
    offer_expiration_ms: Optional[int] = Field(
        default=None, description="Vencimiento de la oferta por tiempo limitado, en ms desde época.")
    flow_token: Optional[str] = Field(
        default=None, description="Ata la respuesta de un Flow a ESTE envío. Sin él no se sabe de quién es.")
    otp_code: Optional[str] = Field(
        default=None, description="El código de una plantilla de autenticación. Viaja al cuerpo Y al botón.")
    button_parameters: List[FilledButtonParameter] = Field(
        default_factory=list,
        description="Valores de los botones que llevan parámetro (URL con sufijo, COPY_CODE).")
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    # Removal automations — asset IDs to REMOVE from the chat on send (mirror of
    # tags/products/flow, which add).
    tags_to_remove: List[StrObjectId] = Field(default_factory=list)
    products_to_remove: List[StrObjectId] = Field(default_factory=list)
    flows_to_remove: List[StrObjectId] = Field(default_factory=list)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = Field(default=None)
    description: str | None = None
    #: «Envío forzado»: sale aunque el chat lo tenga otra persona o la plantilla ya se haya mandado.
    forced_send: bool = False
    #: Sólo para un programado: «Enviar aunque el usuario escriba» (no queda en espera si el cliente
    #: escribe antes). Es `ScheduledMessages.forced_send`, otra cosa que `forced_send`. Sin informar
    #: (un cliente viejo), vale lo mismo que `forced_send`, como antes de separarlos.
    enviar_aunque_escriba: Optional[bool] = None
    lenguage: str | None = None
    campaign_name: str | None = None
    campaign_id: StrObjectId | None = None
    body: str | None = None
    origin : TemplateOrigin
    scheduled_at : Optional[datetime] = None
    scheduled_messages_id : Optional[StrObjectId] = None
    continuous_conversation_id : Optional[StrObjectId] = None
    target_funnel_id : Optional[StrObjectId] = None
    target_stage_id : Optional[StrObjectId] = None

    @property
    def recipient_name(self) -> str:
        if self.new_contact_name:
            return self.new_contact_name
        # Antes usaba recipient_phone_number, que EXPLOTA sin telefono — y un
        # contacto por username no tiene. Para mostrar alcanza cualquier identidad.
        return self.recipient_identity

    @property
    def recipient_phone_number(self) -> str:
        if not self.phone_number:
            raise ValueError("Template data does not have a phone number, can't be used as recipient")
        return self.phone_number

    @property
    def recipient_identity(self) -> str:
        """Identidad para mandar: telefono si hay, si no el BSUID.

        Como Client.get_identity() pero SIN el fallback a group_id: los templates a
        grupos van por otro payload (recipient_type "group") y no por este campo.
        Meta le da precedencia al telefono, asi que cuando existe se usa ese y el
        payload sale idéntico a como salia antes.
        """
        identity = self.phone_number or self.user_id
        if not identity:
            raise ValueError(
                "Template data no tiene ni telefono ni BSUID, no se puede usar como destinatario"
            )
        return identity

    @property
    def is_phone_less(self) -> bool:
        """True cuando solo hay BSUID — el envio tiene que ir por `recipient`."""
        return not self.phone_number and bool(self.user_id)

    @property
    def completed_body(self) -> str:
        if not self.body:
            raise ValueError("Body is empty")
        return self.body

    @model_validator(mode='before')
    def assign_to_agent_if_area_is_with_agent(cls, data: dict) -> dict:
        if not data.get("area") == Area.WITH_AGENT:
            data["assign_to_agent"] = None
        return data

    @model_validator(mode='after') #type: ignore
    def validate_template_data(self) -> dict:

        if self.area == Area.WITH_AGENT and not self.assign_to_agent:
            # TEMPORARY FIX FOR AGENT ASSIGNMENT: IF IT'S NOT SPECIFIED, ASSIGN TO THE AGENT EMAIL
            raise ValueError("Agent assignment must be specified for WITH AGENT area")

        # Hace falta UNA identidad, no necesariamente el telefono: un contacto que
        # adopto username de WhatsApp llega solo con BSUID y aun asi es un
        # destinatario valido (Meta acepta templates via `recipient`). Exigir
        # telefono aca hacia imposible construir el dato para esos contactos.
        if not self.phone_number and not self.user_id:
            logger.warning("Se necesita telefono o BSUID para identificar al destinatario")
            raise ValueError("Se necesita telefono o BSUID para identificar al destinatario")

        # Solo si HAY telefono: el str() incondicional convertia None en el string
        # "None", que antes no importaba porque el telefono era obligatorio, y
        # ahora se colaria como destinatario de un contacto sin telefono.
        if self.phone_number is not None:
            self.phone_number = str(self.phone_number)

        if not self.new_contact_name:
            self.new_contact_name = self.recipient_identity

        return self #type: ignore

    @model_validator(mode='after')
    def validate_scheduled_at(self):
        # Skip validation if this is an existing scheduled message being loaded from DB.
        # scheduled_messages_id is set when the ScheduledMessages model saves to DB,
        # or origin is FROM_SCHEDULED_MESSAGES (set by ScheduledMessages validator).
        if self.scheduled_messages_id or self.origin == TemplateOrigin.FROM_SCHEDULED_MESSAGES:
            return self
        if self.scheduled_at and self.scheduled_at < datetime.now(ZoneInfo("UTC")):
            raise ValueError("Scheduled at must be in the future")
        return self
