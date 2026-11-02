from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, model_serializer, model_validator
from .filled_data_from_frontend import FilledRecipientParameter
from .header_media import TemplateHeaderKind
from .raw_meta_template import ComponentType, NamedParameter

class NamedParameterForPayload(BaseModel):
    type: str = Field(default="text")
    parameter_name: str
    text: str
    
    @classmethod
    def from_template_parameters(cls, payload_parameters: List[FilledRecipientParameter], template_parameters: List[NamedParameter]) -> List[NamedParameterForPayload]:
        #first validate that the ids of the payload params are in the template params
        param_names = [named_param.param_name for named_param in template_parameters]
        if not all(param.id in param_names for param in payload_parameters):
            raise ValueError(f"The ids of the payload params {[param.id for param in payload_parameters]} are not in the template params {param_names}")
        return [cls(type="text", parameter_name=parameter.id, text=parameter.text) for parameter in payload_parameters]

class PositionalParameterForPayload(BaseModel):
    type: str = Field(default="text")
    text: str
    
    @classmethod
    def from_template_parameters(cls, payload_parameters: List[FilledRecipientParameter], template_parameters: List[str]) -> List[PositionalParameterForPayload]:
        # Create a dict mapping parameter id (position) to parameter text
        param_dict = {int(param.id): param.text for param in payload_parameters}
        #validate that the ids of the payload params are in the template params
        if not all(param_index <= len(template_parameters) for param_index in param_dict):
            raise ValueError(f"Expecting {len(template_parameters)} positional parameters, but got indexes: {param_dict.keys()}")
        param_payloads = []
        for param in param_dict:
            param_payload = cls(type="text", text=param_dict[param])
            param_payloads.append(param_payload)
        return param_payloads

class HeaderMediaParameter(BaseModel):
    """El parámetro de media del componente `header`.

    Meta pide una forma en la que la clave del objeto interno ES el propio tipo:

        {"type": "image",    "image":    {"id": "<media_id>"}}
        {"type": "video",    "video":    {"id": "<media_id>"}}
        {"type": "document", "document": {"id": "<media_id>", "filename": "presupuesto.pdf"}}

    Esa clave dinámica no se puede expresar con campos declarados, de ahí el serializador a medida.
    Al ir por `model_serializer` vale tanto para `model_dump()` como para `model_dump_json()`, que es
    lo que termina viajando en el request.

    Se manda por `id` (archivo ya subido al endpoint `/media` de Meta) y no por `link`, igual que
    cualquier otro mensaje de media de Chatty: así hereda la normalización de video y el manejo de
    errores que ese camino ya tiene.
    """

    type: TemplateHeaderKind
    media_id: str
    filename: Optional[str] = Field(default=None, description="Sólo lo usa Meta en los DOCUMENT")

    @model_serializer
    def serialize_for_meta(self) -> dict:
        media: dict = {"id": self.media_id}
        # El filename sólo tiene sentido en un documento; en imagen o video Meta lo ignora.
        if self.type == TemplateHeaderKind.DOCUMENT and self.filename:
            media["filename"] = self.filename
        return {"type": self.type.value, self.type.value: media}


class ButtonTextParameter(BaseModel):
    """El sufijo dinámico de un botón URL.

    Meta lo pide como un parámetro de texto común; lo que lo vuelve un parámetro DE BOTÓN es el
    `sub_type` y el `index` del componente que lo envuelve, no su propia forma.
    """

    type: str = Field(default="text")
    text: str


class CouponCodeParameter(BaseModel):
    """El código de un botón COPY_CODE. Acá la clave sí es propia del tipo."""

    type: str = Field(default="coupon_code")
    coupon_code: str


class FlowActionParameter(BaseModel):
    """El `flow_token` de un botón de Flow. Meta lo pide envuelto en un parámetro de tipo `action`."""

    type: str = Field(default="action")
    flow_token: str

    @model_serializer
    def serialize_for_meta(self) -> dict:
        return {"type": "action", "action": {"flow_token": self.flow_token}}


class LimitedTimeOfferParameter(BaseModel):
    """Cuándo vence la oferta. Meta lo quiere en milisegundos desde época."""

    type: str = Field(default="limited_time_offer")
    expiration_time_ms: int

    @model_serializer
    def serialize_for_meta(self) -> dict:
        return {"type": "limited_time_offer",
                "limited_time_offer": {"expiration_time_ms": self.expiration_time_ms}}


class ComponentForPayload(BaseModel):
    """Un componente del payload de envío.

    `type` es `str` y no `ComponentType` a propósito: los nombres de CREACIÓN y los de ENVÍO no
    coinciden. Al crear, el componente de botones se llama `BUTTONS` (uno solo, con la lista adentro);
    al enviar, cada botón con parámetros es su propio componente `button`, identificado por su
    posición. Forzar el enum obligaría a inventarle miembros al vocabulario de creación.

    Los armadores existentes siguen pasando `ComponentType.HEADER` / `ComponentType.BODY`, que son
    StrEnum: serializan igual que siempre, así que el payload de una plantilla de texto no cambia ni
    un byte.
    """

    type: str
    # Sólo los componentes de botón los usan. `exclude_none` los deja afuera del resto del payload.
    sub_type: Optional[str] = Field(default=None, description="quick_reply · url · copy_code · flow")
    index: Optional[str] = Field(default=None, description="Posición del botón en el array BUTTONS")
    cards: Optional[list] = Field(default=None, description="Sólo el carrusel: una entrada por tarjeta")
    parameters: List[
        NamedParameterForPayload
        | PositionalParameterForPayload
        | HeaderMediaParameter
        | ButtonTextParameter
        | CouponCodeParameter
        | FlowActionParameter
        | LimitedTimeOfferParameter
    ]

    @model_serializer
    def serialize_for_meta(self) -> dict:
        # A mano en vez de `exclude_none` porque el serializador de los parámetros ya es a medida
        # (HeaderMediaParameter) y hay que respetarlo.
        payload: dict = {"type": str(self.type)}
        if self.sub_type is not None:
            payload["sub_type"] = self.sub_type
        if self.index is not None:
            payload["index"] = self.index
        if self.cards is not None:
            # El carrusel no lleva `parameters`: sus valores viven dentro de cada tarjeta.
            payload["cards"] = self.cards
            return payload
        payload["parameters"] = [p.model_dump() for p in self.parameters]
        return payload

class TemplateComponentForPayload(BaseModel):
    name: str
    language: dict 
    components: List[ComponentForPayload]

class TemplateRequestPayload(BaseModel):
    """Payload de /messages para un template.

    Destinatario por TELEFONO via `to`, o — contactos que adoptaron username de
    WhatsApp, que llegan sin telefono — por BSUID via `recipient`. Meta acepta
    templates a BSUID de cualquier categoria salvo los auth de one-tap, zero-tap y
    copy-code, que exigen telefono; ese caso se corta aguas arriba.
    Ref: developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids/

    Mismo contrato que `WhatsAppPayload` de api-chatty para mensajes libres: si
    van los dos, Meta le da precedencia a `to`, asi que se manda EXACTAMENTE uno.
    `model_dump(exclude_none=True)` descarta el que no se usa, de modo que el
    payload de un envio por telefono queda byte a byte igual que antes.
    """

    messaging_product: str = Field(default="whatsapp")
    recipient_type: str = Field(default="individual")
    to: Optional[str] = None
    recipient: Optional[str] = None
    type: str = Field(default="template")
    template: TemplateComponentForPayload

    @model_validator(mode="after")
    def exactly_one_recipient(self) -> "TemplateRequestPayload":
        if bool(self.to) == bool(self.recipient):
            raise ValueError(
                "TemplateRequestPayload requiere exactamente uno de `to` (telefono) o `recipient` (BSUID)"
            )
        return self

    def model_dump_json(self, **kwargs) -> str:  # type: ignore[override]
        """Meta rechaza `to: null`; el campo que no se usa no debe viajar."""
        kwargs.setdefault("exclude_none", True)
        return super().model_dump_json(**kwargs)

    def model_dump(self, **kwargs):  # type: ignore[override]
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)
