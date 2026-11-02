from __future__ import annotations
from pydantic import ConfigDict, Field, field_validator, model_validator
from typing import Any, List, ClassVar, Optional
from ....messages.chatty_messages import MessageDraft
from ....base_models.chatty_asset_model import CompanyAssetModel, ChattyAssetPreview
from ....messages.chatty_messages.schema import ChattyContext
from ....utils.types.message_types import MessageSubtype
from ....utils.types.serializer_type import SerializerType
from ..account_scope import applies_to_account, normalize_account_ids
from ..embeddable import build_chunks


class FastAnswerPreview(ChattyAssetPreview):
    """The 5 generic preview fields plus the account scope: the composer lists previews, and the API
    filters them by the account of the chat."""
    # Plain strings on purpose: a stored value that is not an ObjectId must not make the whole
    # fast answer (or its preview, which `get_preview_docs` would skip) unreadable.
    account_ids: List[str] = Field(default_factory=list)

    @field_validator("account_ids", mode="before")
    @classmethod
    def _normalize_account_ids(cls, value: Any) -> List[str]:
        return normalize_account_ids(value)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"account_ids": 1}

    @classmethod
    def from_asset(cls, asset: "ChattyFastAnswer") -> "FastAnswerPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            account_ids=asset.account_ids,
        )


class ChattyFastAnswer(CompanyAssetModel):
    name: str
    messages: List[MessageDraft]
    account_ids: List[str] = Field(
        default_factory=list,
        description=(
            "Which WhatsApp accounts (numbers) the fast answer is limited to. Empty = every account, "
            "the ones connected later included."
        ),
    )
    preview_class: ClassVar[type[ChattyAssetPreview]] = FastAnswerPreview

    @field_validator("account_ids", mode="before")
    @classmethod
    def _normalize_account_ids(cls, value: Any) -> List[str]:
        return normalize_account_ids(value)

    def applies_to(self, account_id: Optional[str], default_account_id: Optional[str] = None) -> bool:
        """Can it be used in a chat of that account? Empty scope = yes. A chat without account is the
        default account's; if it cannot be resolved, only unscoped fast answers apply."""
        return applies_to_account(self.account_ids, account_id, default_account_id)

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