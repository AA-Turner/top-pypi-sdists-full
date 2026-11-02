from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from pydantic import model_validator
from .meta_base_notification_json import BaseMetaNotificationJson
from .schema.content_messages import MetaTextContent, MetaImageContent, MetaStickerContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaContactContent, MetaLocationContent, MetaSystemContent, MetaButtonContent
from ...utils.types.message_types import MessageType

if TYPE_CHECKING:
    from .schema.values.value_messages import Message, MetaContext, MetaReferral
    from .meta_base_notification_json import Contact

class MetaMessageJson(BaseMetaNotificationJson):

    @model_validator(mode='after')
    def require_identity_in_contacts(self) -> 'MetaMessageJson':
        # A contact must carry SOME identity. Historically that was the phone (`wa_id`);
        # since the WhatsApp username rollout a contact may arrive with ONLY a BSUID
        # (`user_id`) and no phone (out-of-window username-adopter). Accept BSUID-only;
        # reject only a contact with NEITHER a phone nor a BSUID (genuinely malformed).
        contacts = self.get_value().contacts
        if contacts and contacts[0].wa_id is None and contacts[0].user_id is None:
            raise ValueError(
                "contacts[0] has neither wa_id nor user_id for an incoming message — "
                "genuinely malformed payload"
            )
        return self

    @property
    def message(self) -> Message:
        return self.get_value().messages[0]

    def get_wa_id(self) -> str:
        return self.message.id

    def get_created_at(self) -> datetime:
        return self.message.timestamp

    def get_referral(self) -> Optional[MetaReferral]:
        return self.message.referral

    def get_type(self) -> MessageType:
        if self.message.errors is not None:
            self.message.type = MessageType.ERRORS
        return self.message.type

    def get_message_content(self) -> MetaTextContent | MetaImageContent | MetaStickerContent | MetaAudioContent | MetaVideoContent | MetaDocumentContent | List[MetaContactContent] | MetaSystemContent | MetaLocationContent | MetaButtonContent:
        return self.message.get_content() # type: ignore

    def get_message_content_dict(self) -> dict:
        content = self.get_message_content()
        if content is None:
            return {}  # Retorna un diccionario vacío si el contenido es None
        return dict(content) # type: ignore

    def get_client(self) -> Contact:
        return self.get_value().contacts[0]

    def get_client_wa_id(self) -> Optional[str]:
        # May be None now: a username-adopter out of the 30-day window arrives with only a
        # BSUID. Callers must fall back to get_client_user_id() and never assume a phone.
        return self.get_client().get_wa_id()

    def get_client_user_id(self) -> Optional[str]:
        """The contact's BSUID — the stable identity, present even when the phone is absent."""
        return self.get_client().get_user_id()

    def get_group_id(self) -> Optional[str]:
        """WhatsApp Groups API: el group id cuando el mensaje ocurrió dentro de un grupo,
        None en un 1:1. ES el discriminador de ruteo — un mensaje con group_id JAMÁS debe
        resolverse al chat 1:1 del participante (contacts[0])."""
        return self.message.group_id

    def get_context(self) -> Optional[MetaContext]:
        return self.message.context

    def get_revoked_message_id(self) -> Optional[str]:
        """Inbound `revoke` only: the wamid of the message the customer DELETED from
        their WhatsApp (revoke.original_message_id), or None for a normal message."""
        return self.message.get_revoked_message_id()

    def get_edited_message_id(self) -> Optional[str]:
        """Inbound `edit` only: the wamid of the message the customer EDITED on
        their WhatsApp (edit.original_message_id), or None for a normal message."""
        return self.message.get_edited_message_id()

    def get_edited_text_body(self) -> Optional[str]:
        """Inbound `edit` only: the NEW text body, or None when the edit isn't a
        plain-text one (not applied today)."""
        return self.message.get_edited_text_body()