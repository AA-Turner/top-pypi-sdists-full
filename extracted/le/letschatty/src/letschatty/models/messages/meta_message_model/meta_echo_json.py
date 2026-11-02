from __future__ import annotations
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from .meta_base_notification_json import BaseMetaNotificationJson
from .schema.content_messages import MetaTextContent, MetaImageContent, MetaStickerContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaContactContent, MetaLocationContent, MetaSystemContent, MetaButtonContent
from ...utils.types.message_types import MessageType

if TYPE_CHECKING:
    from .schema.values.value_messages import Message, MetaContext

class MetaEchoJson(BaseMetaNotificationJson):
    """WhatsApp Coexistence — `smb_message_echoes` webhook.

    Mirrors the envelope of an *outbound* message: it describes a message the
    business OWNER sent directly from the WhatsApp Business App on a coexistence
    number. Structurally identical to a MESSAGES notification, except the payload
    lives in `value.message_echoes` and each echo carries the recipient (customer)
    `to` wa_id rather than relying on the inbound `contacts[0].wa_id`.
    """

    @property
    def message(self) -> Message:
        return self.get_value().message_echoes[0]

    def get_wa_id(self) -> str:
        """Meta message id (wamid) of the echoed message."""
        return self.message.id

    def get_created_at(self) -> datetime:
        return self.message.timestamp

    def get_type(self) -> MessageType:
        if self.message.errors is not None:
            self.message.type = MessageType.ERRORS
        return self.message.type

    def get_message_content(self) -> MetaTextContent | MetaImageContent | MetaStickerContent | MetaAudioContent | MetaVideoContent | MetaDocumentContent | List[MetaContactContent] | MetaSystemContent | MetaLocationContent | MetaButtonContent:
        return self.message.get_content()  # type: ignore

    def get_message_content_dict(self) -> dict:
        content = self.get_message_content()
        if content is None:
            return {}
        return dict(content)  # type: ignore

    def get_client_wa_id(self) -> str:
        """The customer (recipient) wa_id the owner messaged from their phone app."""
        if self.message.to is not None:
            return self.message.to
        contacts = self.get_value().contacts
        if contacts and contacts[0].wa_id is not None:
            return contacts[0].wa_id
        raise ValueError(
            "smb_message_echoes payload is missing the recipient wa_id "
            "(neither message_echoes[0].to nor contacts[0].wa_id is present)"
        )

    def get_client_user_id(self) -> Optional[str]:
        """The recipient's BSUID — the stable identity, present even when the phone is not.

        Espejo de `MetaMessageJson.get_client_user_id()` para el camino de los echoes, que
        no lo tenía: un destinatario que adoptó username de WhatsApp no tiene teléfono, así
        que `get_client_wa_id()` LEVANTA y el eco se perdía entero (52 echoes en tres
        empresas del 1 al 10 de septiembre de 2026). Ver api-chatty
        docs/echo-de-coexistence-sin-telefono.md.

        `to_user_id` primero —es el campo propio del echo, el espejo saliente de
        `from_user_id`— y `contacts[0].user_id` como respaldo, que es el mismo lugar del
        que lo lee el camino entrante.
        """
        if self.message.to_user_id is not None:
            return self.message.to_user_id
        contacts = self.get_value().contacts
        if contacts and contacts[0].user_id is not None:
            return contacts[0].user_id
        return None

    def get_context(self) -> Optional[MetaContext]:
        return self.message.context

    def get_revoked_message_id(self) -> Optional[str]:
        """WhatsApp Coexistence `revoke` echo only: the wamid of the message the owner
        DELETED from the WhatsApp Business App (revoke.original_message_id), or None."""
        return self.message.get_revoked_message_id()

    def get_edited_message_id(self) -> Optional[str]:
        """WhatsApp Coexistence `edit` echo only: the wamid of the message the owner
        EDITED from the WhatsApp Business App (edit.original_message_id), or None."""
        return self.message.get_edited_message_id()

    def get_edited_text_body(self) -> Optional[str]:
        """WhatsApp Coexistence `edit` echo only: the NEW text body, or None when the
        edit isn't a plain-text one (not applied today)."""
        return self.message.get_edited_text_body()
