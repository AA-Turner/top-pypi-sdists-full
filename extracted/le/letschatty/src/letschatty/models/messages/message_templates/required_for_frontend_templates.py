from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field
import logging
from letschatty.models.messages.message_templates.raw_meta_template import ParameterFormat
from ..chatty_messages.schema.chatty_context.template_rendering import TemplateRenderedButton

if TYPE_CHECKING:
    from letschatty.models.messages.message_templates.raw_meta_template import NamedParameter
    from letschatty.models.messages.message_templates.raw_meta_template import WhatsappTemplate

logger = logging.getLogger(__name__)

class RequiredTemplateParameter(BaseModel):
    id: str
    example: str

    @classmethod
    def from_whatsapp_template(cls, template : WhatsappTemplate) -> List[RequiredTemplateParameter]:
        # G10: delegate to the null-safe `body_parameters` property (it guards a missing BODY / example)
        # and ALWAYS return a list. The old code fell through to an implicit `None` when parameter_format
        # was Python-None (not the NONE enum), which then failed RequiredTemplateData(parameters=None) with
        # a ValidationError. Any non-NAMED/POSITIONAL format now yields [].
        params = template.body_parameters   # [] when there is no BODY / example (G10)
        if template.parameter_format == ParameterFormat.NAMED:
            return cls.from_named_parameters(params)
        if template.parameter_format == ParameterFormat.POSITIONAL:
            return cls.from_positional_parameters(params)
        return []

    @classmethod
    def from_named_parameters(cls, parameters : List[NamedParameter]) -> List[RequiredTemplateParameter]:
        return [RequiredTemplateParameter(id=parameter.param_name, example=parameter.example) for parameter in parameters]

    @classmethod
    def from_positional_parameters(cls, parameters : List[str]) -> List[RequiredTemplateParameter]:
        return [RequiredTemplateParameter(id=str(index+1), example=parameter) for index, parameter in enumerate(parameters)]

class RequiredButtonParameter(BaseModel):
    """Un botón que necesita que el usuario complete algo.

    `index` es la posición del botón en la plantilla — así lo identifica Meta al enviar. `label` es el
    texto visible del botón, que es lo que la pantalla tiene que mostrarle al agente: el índice es un
    detalle del protocolo, no algo que deba ver.
    """

    index: int
    sub_type: str = Field(description="url · copy_code")
    label: str
    example: Optional[str] = Field(default=None)


class RequiredTemplateData(BaseModel):
    name: str
    text: str
    parameters: List[RequiredTemplateParameter]
    # A5 (ADDITIVE, C2): mobile + web depend on name/text/parameters — these extra fields are optional so
    # old clients ignore them. `category` is the hook for the future category-aware campaign cost estimate
    # (today the estimate is category-blind); `status` lets the picker show a paused/rejected template's state.
    category: Optional[str] = None
    language: Optional[str] = None
    status: Optional[str] = None
    # Encabezado (ADITIVO). Sin esto quien va a enviar no sabe que la plantilla pide un archivo, y el
    # envío falla recién contra Meta. Opcionales para que los clientes viejos (la app móvil) los ignoren.
    header_format: Optional[str] = Field(
        default=None, description="Formato crudo de Meta: TEXT · IMAGE · VIDEO · DOCUMENT · LOCATION")
    requires_header_media: bool = Field(
        default=False, description="True si hay que adjuntar un archivo para poder enviarla")
    header_media_kind: Optional[str] = Field(
        default=None, description="Tipo a usar al adjuntar: image · video · document. Única fuente de verdad del mapeo")
    header_media_available: bool = Field(
        default=False,
        description="True si la plantilla trae su archivo (el que la empresa cargó en Meta). Es el que "
                    "se manda: no se elige ni se reemplaza al enviar.")
    header_text: Optional[str] = Field(
        default=None,
        description="Texto CRUDO del encabezado, con sus {{n}} sin reemplazar — para que la vista "
                    "previa lo interpole igual que el cuerpo. None si el encabezado no es de texto.")
    header_parameters: List[RequiredTemplateParameter] = Field(
        default_factory=list,
        description="Variables del encabezado de TEXTO. Misma forma que `parameters`; vacío si no tiene.")
    button_parameters: List[RequiredButtonParameter] = Field(
        default_factory=list,
        description="Botones que piden un valor al enviar (URL con sufijo, COPY_CODE).")
    header_media_url: Optional[str] = Field(
        default=None,
        description="URL del archivo de la plantilla, para MOSTRARLO en la vista previa. Viene firmada "
                    "por Meta y caduca, pero se renueva en cada sincronización, así que para mostrar "
                    "siempre está fresca. Para enviar NO se usa ésta: api-chatty guarda su propia copia.")
    footer_text: Optional[str] = Field(default=None, description="El pie, para la vista previa.")
    buttons: List[TemplateRenderedButton] = Field(
        default_factory=list,
        description="TODOS los botones, para la vista previa, sin completar (`{{1}}` en el enlace, sin "
                    "código): la pantalla los completa con lo que se escribe. Sale de la misma función "
                    "que guarda el mensaje enviado (`TemplateFactory.render_for_chat`). Los que piden "
                    "un valor siguen en `button_parameters`.")

