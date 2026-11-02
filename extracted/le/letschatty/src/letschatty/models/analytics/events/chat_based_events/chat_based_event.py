from pydantic import BaseModel, Field, field_validator
from ....utils.types.identifier import StrObjectId
from typing import Any, ClassVar, Dict, Optional
from .chat_context import ChatContext
from ....utils.types.executor_types import ExecutorType
from ....company.assets.users.agent_chats_snapshot import AgentChatsSnapshot
from ....company.company_chats_snapshot import CompanyChatsSnapshot
from ..base import EventData
import json

class CustomerEventData(EventData):
    company_phone_number_id: str
    company_waba_id: str
    account_id: Optional[StrObjectId] = Field(default=None, description="The WhatsApp account of the chat (multi-account). Analytics stay per company; this is an extra dimension")
    chat_id: Optional[StrObjectId] = Field(default=None)
    client_phone_number : Optional[str] = Field(default=None)
    client_email : Optional[str] = Field(default=None)
    client_country : Optional[str] = Field(default=None)
    client_name : Optional[str] = Field(default=None)
    ctwa_clid : Optional[str] = Field(default=None)
    fb_clid : Optional[str] = Field(default=None)
    gclid : Optional[str] = Field(default=None)
    fbc : Optional[str] = Field(default=None, description="Meta _fbc cookie captured by chatty_pixel; already in Meta's fb.<idx>.<ms>.<fbclid> format")
    fbp : Optional[str] = Field(default=None, description="Meta _fbp browser id cookie captured by chatty_pixel")
    client_ip_address : Optional[str] = Field(default=None)
    client_user_agent : Optional[str] = Field(default=None)
    client_external_id : Optional[str] = Field(default=None)
    #: Los campos LIBRES del lead (formularios de WhatsApp Flows, la IA, la API).
    #: Las claves las define cada empresa en su propio formulario: no hay dos
    #: iguales y cambian cuando el cliente cambia el form. Viaja el diccionario
    #: COMPLETO —no el delta— así analytics resuelve la fila con "el último gana"
    #: y no necesita reconstruir el estado sumando eventos.
    lead_form_data : Dict[str, Any] = Field(default_factory=dict)
    executor_type: ExecutorType
    executor_id: StrObjectId
    chat_context: Optional[ChatContext] = Field(default=None)
    agent_snapshot: Optional[AgentChatsSnapshot] = Field(default=None)
    company_snapshot: Optional[CompanyChatsSnapshot] = Field(default=None)

    #: Topes del diccionario libre. Es texto que escribe el cliente final, así que
    #: nada acota su tamaño del lado de Chatty: un formulario con un campo de texto
    #: largo puede generar un evento enorme. Acá ya pasó —un payload sobredimensionado
    #: de history disparó una tormenta falsa en la SQS— así que el corte va en el
    #: borde del evento y no río abajo. Se trunca en vez de descartar: un valor
    #: cortado sigue sirviendo para ver y segmentar; perder el campo entero, no.
    MAX_CLAVES: ClassVar[int] = 50
    MAX_LARGO_CLAVE: ClassVar[int] = 100
    MAX_LARGO_VALOR: ClassVar[int] = 500

    @field_validator("lead_form_data", mode="before")
    @classmethod
    def _acotar_lead_form_data(cls, v: Any) -> Dict[str, Any]:
        if not isinstance(v, dict):
            return {}
        out: Dict[str, Any] = {}
        for k, val in list(v.items())[: cls.MAX_CLAVES]:
            clave = str(k)[: cls.MAX_LARGO_CLAVE]
            if val is None:
                continue
            texto = val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str)
            out[clave] = texto[: cls.MAX_LARGO_VALOR]
        return out

    @property
    def message_group_id(self) -> str:
        return f"chat-{self.chat_id}"
