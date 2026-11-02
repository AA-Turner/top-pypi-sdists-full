from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator
from zoneinfo import ZoneInfo

from ..content_messages import MetaTextContent, MetaImageContent, MetaStickerContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaContactContent, MetaLocationContent, MetaSystemContent, MetaOrderContent, MetaInteractiveContent, MetaButtonContent, MetaReactionContent
from .....utils.types import MessageType
from .value_errors import Error
class MetaReferral(BaseModel):
    # Organic post referrals (source_type="post") omit source_url, and Meta may also
    # send it as null — so it must NOT be required. "" is the canonical "no source url"
    # value used downstream (ChattyReferral.is_default). Making it required previously
    # 422'd every organic-post Click-to-WhatsApp lead.
    source_url: str = ""
    source_id: Optional[str] = Field(default=None)
    source_type: Optional[str] = Field(default=None)
    headline: Optional[str] = Field(default=None)
    body: Optional[str] = Field(default=None)
    media_type: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    video_url: Optional[str] = Field(default=None)
    thumbnail_url: Optional[str] = Field(default=None)
    ctwa_clid: Optional[str] = Field(default=None)

    @field_validator("source_url", mode="before")
    @classmethod
    def _coerce_source_url_none(cls, v: object) -> object:
        # default="" covers an ABSENT key; this covers an explicit null from Meta.
        return "" if v is None else v

class ReferredProduct(BaseModel):
    catalog_id: str
    product_retailer_id: str

class MetaRevoke(BaseModel):
    """Payload of a Meta `type: "revoke"` message — a message the sender DELETED.
    `original_message_id` is the wamid of the message to mark as deleted. Carries no
    content of its own; both the inbound revoke (customer deleted their message) and
    the `smb_message_echoes` revoke (owner deleted from the WhatsApp Business App on a
    coexistence number) share this shape."""
    original_message_id: str

class MetaEditedMessage(BaseModel):
    """The NEW content inside a Meta `type: "edit"` notification. Meta nests a mini
    message object (`{"type": "text", "text": {"body": ...}}`). Only text edits are
    modeled/applied today; other shapes (e.g. media caption edits) parse tolerantly
    (extra keys ignored) and are skipped by the appliers."""
    type: Optional[str] = None
    text: Optional[MetaTextContent] = None


class MetaEdit(BaseModel):
    """Payload of a Meta `type: "edit"` message — the sender EDITED an earlier message.
    `original_message_id` is the wamid of the message whose content must be replaced;
    `message` carries the new content. Shared by the inbound edit and the
    `smb_message_echoes` edit (owner edited from the WhatsApp Business App on a
    coexistence number)."""
    original_message_id: str
    message: Optional[MetaEditedMessage] = None


class MetaContext(BaseModel):
    from_: Optional[str] = Field(default=None, alias="from")
    # BSUID of the sender of the quoted message. Phase 2: a phone-less username-adopter who
    # REPLIES to a message carries `from_user_id` in the context instead of `from` (phone).
    from_user_id: Optional[str] = Field(default=None)
    id: Optional[str] = Field(default=None)
    forwarded: Optional[bool] = Field(default=False)
    referred_product : Optional[ReferredProduct] = Field(default=None)

    @model_validator(mode='after')
    def validate_from_and_id(self):
        # A `from` WITHOUT an `id` is a legitimate Meta shape: a reply to a WhatsApp
        # Status ("estado") arrives as a normal message whose context references only
        # the business number that posted the status (`from`), with no `id` because a
        # status has no regular inbound message id. Rejecting it 500'd the whole
        # webhook. Downstream is safe — `is_response_to_specific_message()` and
        # `ChattyContext.from_meta` both treat `id is None` as "not a reply to a
        # specific message". A referenced message must have a SENDER — but Phase 2 makes
        # that sender identifiable by BSUID (`from_user_id`) when the phone is absent (a
        # phone-less user replying). Reject only when there is an `id` but NEITHER a phone
        # NOR a BSUID (genuinely malformed).
        if self.from_ is None and self.from_user_id is None and self.id is not None:
            raise ValueError("a referenced message needs a sender (from or from_user_id) when an id is provided")
        return self

    def is_possible_status_reply(self) -> bool:
        """HEURISTIC — NOT an exact classification.

        Meta does NOT flag replies to a WhatsApp Status. We can only INFER it from
        the shape of the context: a status reply arrives with ONLY `from` (the number
        that posted the status) and no `id` (a status has no quotable inbound message
        id). We additionally require the absence of the other id-less context markers
        (`referred_product`, `forwarded`) so those known shapes are never misread.

        This remains a guess: Meta could ship a future context that reuses the same
        `{from, no id}` skeleton for something else. Callers should treat a True here
        as "POSSIBLE status reply", never as a certainty — hence the name. The caller
        (api-chatty) further tightens it by checking `from` == our own business number.
        """
        return (
            self.from_ is not None
            and self.id is None
            and self.referred_product is None
            and not self.forwarded
        )


class HistoryContext(BaseModel):
    """Per-message context carried only by WhatsApp Coexistence `history` backfill
    messages. `from_me` is Meta's authoritative direction flag (`True` =
    business-sent/outgoing, `False` = customer/incoming) — more reliable than
    comparing `from` to the business `display_phone_number`. `status` is the
    historical delivery status (e.g. "read", "delivered"). Both default to None
    so this model is harmless on normal (non-history) messages, which never set it."""
    status: Optional[str] = Field(default=None)
    from_me: Optional[bool] = Field(default=None)


class Message(BaseModel):
    # `from` (sender phone) is OPTIONAL: a WhatsApp username-adopter whose phone is out of
    # the 30-day window arrives with only `from_user_id` (BSUID) and no `from`. Keeping this
    # required made pydantic reject the whole webhook (422 → the customer message is dropped).
    # The stable identity is the contact's `user_id` (BSUID); resolve the chat by BSUID when
    # `from` is absent (see MetaMessageJson.get_client_user_id / empresa.receive_message_from_meta).
    from_: Optional[str] = Field(default=None, alias="from")
    to: Optional[str] = Field(default=None, description="WhatsApp Coexistence echoes only: the recipient (customer) wa_id of the message the business owner sent from the WhatsApp Business App")
    # El BSUID del REMITENTE, a nivel mensaje. En el tráfico en vivo la identidad del
    # cliente se lee de `contacts[0].user_id`, así que este campo nunca hizo falta —
    # pero el backfill de `history` NO trae `contacts`, y en su forma plana el BSUID
    # viaja únicamente acá. Sin declararlo, pydantic lo descartaba y un cliente sin
    # teléfono quedaba sin ninguna identidad derivable: su mensaje se salteaba como
    # "saliente sin `to`". Misma lección que `to_user_id` (0.4.537), del otro lado.
    from_user_id: Optional[str] = Field(default=None, description="BSUID del remitente cuando NO tiene teléfono (username-adopter). Única fuente de identidad en la forma PLANA del backfill de history, que no trae `contacts`.")
    # El espejo saliente de `from_user_id`: cuando el DESTINATARIO del echo es un contacto
    # que adoptó username de WhatsApp, no tiene teléfono y Meta manda `to_user_id` (BSUID)
    # en vez de `to`. Sin declararlo, pydantic descartaba el campo y el eco quedaba sin
    # identidad — la respuesta que el dueño escribió desde la app del teléfono no
    # encontraba chat. Ver api-chatty docs/echo-de-coexistence-sin-telefono.md.
    to_user_id: Optional[str] = Field(default=None, description="WhatsApp Coexistence echoes only: BSUID del destinatario cuando NO tiene teléfono (username-adopter). Espejo saliente de `from_user_id`.")
    group_id: Optional[str] = Field(default=None, description="WhatsApp Groups API: presente cuando el mensaje ocurrió DENTRO de un grupo. `from`/contacts traen al PARTICIPANTE — el chat destino se resuelve por este campo, nunca por el contacto (spec 2026-08-29 §5.3)")
    id: str
    timestamp: datetime
    type: MessageType
    history_context: Optional[HistoryContext] = Field(default=None, description="WhatsApp Coexistence history backfill only: {status, from_me}; from_me is Meta's authoritative direction flag. None on normal live messages/echoes.")
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
    revoke: Optional[MetaRevoke] = Field(default=None, description="Meta `type: revoke` only: the deleted message reference {original_message_id}. None on all normal messages.")
    edit: Optional[MetaEdit] = Field(default=None, description="Meta `type: edit` only: {original_message_id, message} — the reference to the edited message plus its NEW content. None on all normal messages.")

    def get_revoked_message_id(self) -> Optional[str]:
        """The wamid of the message this revoke deletes, or None if this is not a
        revoke / carries no reference. Used to locate and tombstone the original."""
        return self.revoke.original_message_id if self.revoke is not None else None

    def get_edited_message_id(self) -> Optional[str]:
        """The wamid of the message this edit replaces, or None if this is not an
        edit / carries no reference. Used to locate the original message."""
        return self.edit.original_message_id if self.edit is not None else None

    def get_edited_text_body(self) -> Optional[str]:
        """The NEW text body carried by a `type: edit` notification, or None when this
        is not an edit or the edit isn't a plain-text one (e.g. a media caption edit —
        not applied today). Callers must treat None as \"nothing to apply\"."""
        if self.edit is None or self.edit.message is None or self.edit.message.text is None:
            return None
        return self.edit.message.text.body

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

    @field_validator('type', mode='before')
    @classmethod
    def coerce_unknown_type(cls, v):
        """Tolerate message types Meta hasn't taught us (e.g. `call`, or any
        type added over a ~6-month WhatsApp Coexistence history backfill) by mapping
        unrecognized values to MessageType.UNKNOWN.

        WHY this is load-bearing for history import: a `history` webhook packs MANY
        messages into ONE envelope (value.messages[] / value.history[].threads[].messages[]),
        which pydantic validates atomically. With a strict MessageType, a single message
        of a novel type raises ValidationError for the WHOLE envelope, silently dropping
        the entire chunk of otherwise-valid history — and the receiver's per-message
        try/except runs AFTER the envelope parse, so it can't isolate the bad message.
        Coercing to UNKNOWN lets the chunk survive: the live path routes UNKNOWN to the
        unsupported-message notifier (which never calls get_content()), and the history
        factory renders it as a `[unknown]` text placeholder. Known values pass through
        untouched (StrEnum members compare equal to their string value)."""
        if isinstance(v, str) and v not in MessageType.values():
            return MessageType.UNKNOWN
        return v

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


# --- WhatsApp Coexistence: history backfill + state-sync sub-models -----------
# Defined after Message so HistoryThread.messages can reference it directly.

class HistoryChunkMetadata(BaseModel):
    """Per-chunk metadata for a WhatsApp Coexistence `history` webhook entry.

    The history sync arrives in ordered chunks; `phase` distinguishes the
    initial backfill phases and `progress` is a 0-100 completion percentage.

    Real Meta payloads send `phase` as an INTEGER (e.g. 1); pydantic also coerces
    numeric strings, so this stays backward-compatible with the earlier guess."""
    phase: Optional[int] = Field(default=None)
    chunk_order: Optional[int] = Field(default=None)
    progress: Optional[float] = Field(default=None)


class HistoryThreadContext(BaseModel):
    """The identity block Meta attaches to a history thread.

    `wa_id` is the customer's phone number. A contact who identifies with a
    WhatsApp **username** instead of a phone number has NO `wa_id` here and no
    top-level `thread.id` either — only the opaque `user_id` (the BSUID, e.g.
    `CO.1472426137994571`) and the `username`. Declared so the thread key can
    fall back to `context.wa_id`, and so the BSUID/username survive the parse
    for whoever resolves a phoneless identity later. Unknown keys Meta adds
    (e.g. `logical_id`) are ignored, as everywhere else in this schema."""
    wa_id: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)


class HistoryThread(BaseModel):
    """One customer conversation thread inside a history chunk: `id` is the
    customer wa_id and `messages` are that thread's historical messages, each
    reusing the standard `Message` value model.

    ⚠️ `id` is OPTIONAL, and that is load-bearing. Meta omits it for a customer
    who has no phone number (a WhatsApp username account) — identity then lives
    only in `context`. While `id` was required, ONE such thread raised
    ValidationError for the WHOLE envelope, and since a chunk packs hundreds of
    threads into one webhook, every valid thread beside it died too. Measured in
    prod 2026-09-17: 128 phoneless threads voided a 737-thread / 947-message
    chunk, and across five companies ~40.000 historical messages were dropped
    this way. The receiver ACKs a ValidationError with 422, so Meta never
    redelivers — the loss is permanent. `iter_threads()` is what decides a
    thread without a usable key is skipped alone, not with its neighbours."""
    id: Optional[str] = Field(default=None)
    context: Optional[HistoryThreadContext] = Field(default=None)
    messages: List[Message] = Field(default_factory=list)


class HistoryEntry(BaseModel):
    """A single `value.history[]` entry: a chunk of threads plus its metadata."""
    metadata: Optional[HistoryChunkMetadata] = Field(default=None)
    threads: List[HistoryThread] = Field(default_factory=list)


class StateSyncContact(BaseModel):
    """The contact card carried by a `smb_app_state_sync` contact entry."""
    full_name: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)


class StateSyncEntry(BaseModel):
    """A single `value.state_sync[]` entry from the `smb_app_state_sync` webhook.
    Only `type == "contact"` entries carry a `contact`; other types (e.g. chat
    state) are tolerated and ignored by the contact accessor."""
    type: Optional[str] = Field(default=None)
    action: Optional[str] = Field(default=None)
    contact: Optional[StateSyncContact] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

