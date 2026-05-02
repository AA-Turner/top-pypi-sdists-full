from __future__ import annotations
from pydantic import ConfigDict, model_validator
from typing import List, ClassVar
from ....messages.chatty_messages import MessageDraft
from ....base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from ....messages.chatty_messages.schema import ChattyContext
from ....utils.types.message_types import MessageSubtype
from ....utils.types.serializer_type import SerializerType
from ..embeddable import build_chunks

class ChattyFastAnswer(CompanyAssetModel):
    name: str
    messages: List[MessageDraft]
    preview_class: ClassVar[type[ChattyAssetPreview]] = ChattyAssetPreview

    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"messages"}
    }

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True
                )

    @model_validator(mode='after')
    def set_context_and_subtype_on_messages(self):
        for message in self.messages:
            message.context = ChattyContext(response_id=self.id)
            message.subtype = MessageSubtype.CHATTY_FAST_ANSWER
        return self

    def embedding_chunks(self) -> list[dict[str, str]]:
        """Name + inherited description + visible body/caption of each message.

        Real production fast-answers frequently have no description and rely on
        name + messages, so we don't gate on description.
        """
        parts: list[str] = []
        for msg in self.messages or []:
            try:
                body = str(msg.content.get_body_or_caption() or "").strip()
            except Exception:
                body = ""
            if body:
                parts.append(body)
        return build_chunks(
            "fast_answer",
            {
                "name": self.name,
                "description": self.description,
                "messages": "\n".join(parts),
            },
        )