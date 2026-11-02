from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from ....meta_message_model.schema.values.value_messages import MetaContext
from .template_rendering import TemplateRendering

class ChattyContext(BaseModel):
    message_id: Optional[str] = Field(default="")
    template_name: Optional[str] = Field(default=None)
    meta_template_id: Optional[str] = Field(default=None, description="Meta's stable template id (WhatsappTemplate.id). Stamped alongside template_name so a sent message keeps a durable pointer to the exact template object even if the name is reused after a delete+recreate. Sending is by name; this is for traceability and rides the message.sent event via context.")
    campaign_id: Optional[str] = Field(default=None)
    response_id: Optional[str] = Field(default=None)
    chain_of_thought_id: Optional[str] = Field(default=None)
    cintia_id: Optional[str] = Field(default=None)
    workflow_id: Optional[str] = Field(default=None, description="Id of the copilot workflow/automation that produced this message, when sent by a copilot automation")
    forwarded: Optional[bool] = Field(default=False)
    continuous_conversation_id: Optional[str] = Field(default=None)
    scheduled_messages_id: Optional[str] = Field(default=None)
    contact_point_id: Optional[str] = Field(default=None, description="Id of the contact point this central notification is about. The notification body names the source ('TouchPoint de la fuente X agregado…'), which freezes at write time and starts lying the moment the touchpoint is reattributed. With the pointer the client can render the CURRENT source instead of the frozen text, and the body stays as the fallback for clients that don't resolve it.")
    template_rendering: Optional[TemplateRendering] = Field(default=None, description="Encabezado de texto, pie y botones de una plantilla enviada, congelados al enviarla (ver template_rendering.py). El cuerpo ya está en content. None = no es plantilla, o es un mensaje anterior a este campo.")
    edited_at: Optional[datetime] = Field(default=None, description="UTC time the SENDER edited this message on WhatsApp (Meta `type: edit` notification — inbound or coexistence echo). None = never edited. content.body already holds the NEW text; the frontend renders an 'editado' legend off this field, like WhatsApp does. Lives on context (not the message top level) so it rides the ChattyMessageJson/JsonMessageFactory context dict passthrough and round-trips the DB with no whitelist edits (the `starred` lesson).")
    received_on_previous_number: Optional[bool] = Field(default=None, description="Multi-account (5A): an INCOMING message that arrived on a number its account no longer uses. It lands in the same chat but does not open the 24 h window: the reply goes out from the current number, where the window is still closed. None = arrived on the current number.")

    def model_dump(self, *args, **kwargs):
        kwargs['exclude_unset'] = True
        return super().model_dump(*args, **kwargs)

    @classmethod
    def from_meta(cls, meta_context: MetaContext | None) -> ChattyContext:
        if meta_context is None:
            return cls.default()
        return cls(message_id=meta_context.id, forwarded=meta_context.forwarded)

    @classmethod
    def default(cls) -> ChattyContext:
        return cls()