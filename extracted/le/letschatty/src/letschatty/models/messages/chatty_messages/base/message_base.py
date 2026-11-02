from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Dict, Any, Optional, TYPE_CHECKING
import json
from ....utils.types.serializer_type import SerializerType
from ....utils.types.message_types import MessageType
from bson import ObjectId
from ....utils import MessageType, Status, MessageSubtype
from ....utils.types.message_status_types import is_meta_message_id
from ..schema import ChattyContent, ChattyContext, ChattyReferral
from ...meta_message_model.schema.values.value_statuses import ErrorDetail
from ...meta_message_model.schema.values.motivos_de_no_entrega import NoEntrega
from letschatty.models.utils import StrObjectId
import logging
from letschatty.models.utils.custom_exceptions import ImpossibleError

logger = logging.getLogger(__name__)

class Message(BaseModel):
    created_at: datetime
    updated_at: datetime
    type: MessageType
    content: ChattyContent
    status: Status
    is_incoming_message: bool
    id: str = Field(default_factory=lambda: str(ObjectId()),description="Unique identifier for the message. In case it's a central notification or a message request (still not confirmed by external API) we'll use an object id as default. Also known as wamid form Meta")
    sent_by: Optional[str] = Field(description="Email of the agent who sent the message. If it's incoming, it'll be None")
    starred: bool = Field(default=False)
    revoked: bool = Field(default=False, description="True once the sender DELETED this message (inbound `revoke`, or an owner `smb_message_echoes` revoke on a coexistence number). Content is kept; the frontend shows a 'message deleted' legend. Orthogonal to `status`.")
    subtype: MessageSubtype = Field(default_factory=lambda: MessageSubtype.NONE)
    referral: ChattyReferral = Field(default_factory=lambda: ChattyReferral.default())
    played_at: Optional[datetime] = Field(default=None, description="Voice notes only: the UTC time the recipient first PLAYED the audio (Meta `played` status). None for non-audio or not-yet-played. Additive/optional and ORTHOGONAL to `status` — `played` is not a delivery status, so it never touches the status ladder.")
    context: ChattyContext = Field(default_factory=lambda: ChattyContext.default())
    error_details: Optional[ErrorDetail] = Field(default=None, description="Lo que dijo Meta cuando no lo entregó (status `failed`: código, título, detalle). Se guarda con el estado (`ChatMessagesCollection.update_status`); sin esto, el resultado de una campaña no sabe POR QUÉ no llegó.")
    no_entrega: Optional[NoEntrega] = Field(default=None, description="Por qué no se entregó, en castellano y con el motivo agrupado (tope de marketing, sin WhatsApp, …). Derivado de `error_details`, guardado junto a él.")

    @property
    def is_cc_related(self) -> bool:
        return self.context.continuous_conversation_id is not None

    @property
    def sent_by_outgoing_id(self) -> StrObjectId:
        if self.is_incoming_message:
            raise ValueError("sent_by_outgoing_id is not available for incoming messages")
        if self.sent_by is None:
            raise ValueError("sent_by is required for outgoing messages")
        return self.sent_by

    @property
    def sent_by_incoming(self) -> bool:
        return self.is_incoming_message

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Message):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Message):
            return False
        return self.created_at > other.created_at

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Message):
            return False
        return self.created_at < other.created_at

    @property
    def is_template_message(self) -> bool:
        return self.subtype == MessageSubtype.TEMPLATE

    @property
    def is_incoming(self) -> bool:
        return self.is_incoming_message

    @property
    def is_outgoing(self) -> bool:
        return not self.is_incoming_message and self.type != MessageType.CENTRAL

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Dump the message to a dictionary, with the option to convert datetimes to a specific timezone.
        """
        timezone = kwargs.pop('timezone', None)
        kwargs.pop('serializer', None)
        data = super().model_dump(*args, **kwargs)
        if timezone:
            try:
                tz = ZoneInfo(timezone)
                data['created_at'] = self.created_at.astimezone(tz).isoformat()
                data['updated_at'] = self.updated_at.astimezone(tz).isoformat()
            except ZoneInfoNotFoundError:
                raise ValueError(f"Invalid timezone: {timezone}")
        return data

    class ConfigDict:
        validate_assignment = True

    @model_validator(mode='after')
    def validate_sent_by_for_outgoing(self) -> "Message":
        """Outgoing messages require a sent_by (the agent's email), EXCEPT WhatsApp
        Coexistence echoes and imported history: those are outgoing messages the
        business owner sent from the WhatsApp Business App (live echo or one-time
        history import), so they have no Chatty agent author and are allowed to keep
        sent_by=None. The relaxation is scoped strictly to COEXISTENCE_ECHO and
        COEXISTENCE_IMPORT.

        Incoming: sent_by se limpia SIEMPRE (el autor de un entrante 1:1 es el cliente,
        no hay nada que guardar y un valor espurio legado se normaliza) — EXCEPTO los
        mensajes de grupo (subtype GROUP), donde sent_by ES el waid del participante
        que escribio y tiene que sobrevivir el round-trip por Mongo. La limpieza vivia
        en un before-field-validator que no podia ver `subtype` (se parsea despues de
        sent_by) y borraba el autor del grupo en CADA lectura — misma clase de bug que
        el round-trip de `starred`."""
        if self.is_incoming_message:
            if self.subtype != MessageSubtype.GROUP and self.sent_by is not None:
                self.sent_by = None
            return self
        if not self.sent_by:
            if self.subtype in (MessageSubtype.COEXISTENCE_ECHO, MessageSubtype.COEXISTENCE_IMPORT):
                return self
            raise ValueError("sent_by is required for outgoing messages")
        return self

    @field_validator('status', mode='before')
    def validate_status(cls, v: Optional[str], info: ValidationInfo) -> Status:
        """Status should be validated always, both instantiation and assignment"""
        if isinstance(v, str):
            return Status(v)
        return v

    @field_validator('subtype', mode='before')
    def validate_subtype(cls, v: Optional[str], info: ValidationInfo) -> MessageSubtype:
        """Degrade an unknown subtype instead of rejecting the whole message.

        api-chatty writes subtypes that a pinned letschatty may not know yet.
        Because the message is nested inside the chat, a rejected subtype makes
        `ChatFactory.from_json` raise, which makes `ChatRepository.find_by_id`
        fail hard — so a single new string takes the entire chat down, and with
        it every CINTIA execution on that chat. It surfaced with
        `history_unshared_content` (the "Meta no comparte archivos" placeholders
        on coexistence imports): 10% of a real company's chats became
        unreadable, silently.

        Being strict here buys nothing — nothing branches on an unknown subtype
        anyway — and costs the whole conversation. So: log it and fall back to
        NONE, which is what the field already means for "nothing special about
        this message".
        """
        if v is None or v == "":
            return MessageSubtype.NONE
        if isinstance(v, MessageSubtype):
            return v
        try:
            return MessageSubtype(v)
        except ValueError:
            logger.warning(
                "unknown_message_subtype",
                extra={"subtype": str(v)[:64], "message_id": (info.data or {}).get("id")},
            )
            return MessageSubtype.NONE

    @field_validator('referral', mode='before')
    def validate_referral(cls, v: Optional[Dict], info: ValidationInfo) -> ChattyReferral:
        """If there's no referral, we'll use the referral default."""
        if v is None or v == {}:
            return ChattyReferral.default()
        return v

    @field_validator('context', mode='before')
    def validate_context(cls, v: Optional[Dict], info: ValidationInfo) -> ChattyContext:
        """If there's no context, we'll use the context default."""
        if v is None or v == {}:
            return ChattyContext.default()
        return v

    @field_validator('context', mode='after')
    def validate_context_based_on_subtype(cls, v: ChattyContext, info: ValidationInfo) -> ChattyContext:
        """We'll validate the context based on the subtype.
        And if there's no context, we'll use the context default."""
        subtype = info.data.get('subtype')
        if subtype == MessageSubtype.TEMPLATE:
            if v.template_name is None:
                raise ValueError("template_name is required for template messages")
        elif subtype == MessageSubtype.CHATTY_FAST_ANSWER:
            if v.response_id is None:
                raise ValueError("response_id is required for chatty_response messages")
        return v

    @field_validator('created_at', 'updated_at')
    def ensure_utc(cls, v):
        if isinstance(v, datetime):
            v = v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
            if v > datetime.now(ZoneInfo("UTC")):
                v = datetime.now(ZoneInfo("UTC"))
                logger.warning(f"Message created at {v} is in the future, setting it to now")
                # raise ImpossibleError(f"Message created at {v} is in the future")
            return v
        raise ValueError('must be a datetime')

    def update_status(self, new_status: Status, status_datetime: datetime) -> bool:
        """Aplica el estado sólo si avanza (ver `Status.supersedes`). Devuelve si lo aplicó."""
        if new_status == Status.PLAYED:
            # PLAYED is a voice-note webhook receipt, NOT a delivery status. It must never
            # overwrite the delivery ladder (sent→delivered→read) — the receiver records it
            # via mark_played() → played_at. See docs/played-voice-note-status.md.
            raise ValueError("Status.PLAYED is a voice-note receipt, not a delivery status; use mark_played()")
        if new_status not in Status:
            raise ValueError(f"Invalid status: {new_status}")
        if not new_status.supersedes(self.status, confirmed_by_meta=is_meta_message_id(self.id)):
            return False
        self.status = new_status
        self.updated_at = status_datetime
        return True

    def mark_as_read(self):
        self.status = Status.READ
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_starred(self):
        self.starred = True
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_unstarred(self):
        self.starred = False
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_revoked(self):
        """Tombstone this message: it was DELETED by the sender (an inbound `revoke`
        from the customer, or a `smb_message_echoes` revoke when the owner deleted it
        from the WhatsApp Business App). Content is preserved in the DB; the frontend
        renders a "message deleted" legend off this flag. Orthogonal to delivery
        `status` — a delivered/read message can still be revoked afterwards."""
        self.revoked = True
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_edited(self, new_body: str, edited_at: datetime):
        """Apply a sender-side EDIT (Meta `type: edit` — inbound or coexistence echo):
        replace the text body and stamp context.edited_at so the frontend renders the
        'editado' legend. The caller guards that this is a TEXT message — captions and
        other content shapes are not applied today. Orthogonal to delivery `status`."""
        self.content.body = new_body
        self.context.edited_at = edited_at
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_failed(self):
        self.status = Status.FAILED
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_sent(self):
        self.status = Status.SENT
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_as_delivered(self):
        self.status = Status.DELIVERED
        self.updated_at = datetime.now(ZoneInfo("UTC"))

    def mark_played(self, played_datetime: datetime):
        """Record that a VOICE NOTE was played by the recipient (Meta `played` status).
        Set-once (Meta reports the FIRST play), idempotent on re-delivery. NEVER touches
        `status` — played is a separate audio-only signal, not a delivery status."""
        if self.played_at is None:
            self.played_at = played_datetime

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        """Since we currently don't support all messages types in the frontend, we need to convert the message to a text message."""
        from .. import ContactMessage, ReactionMessage, ButtonMessage, LocationMessage

        dump = json.loads(super().model_dump_json())
        return dump