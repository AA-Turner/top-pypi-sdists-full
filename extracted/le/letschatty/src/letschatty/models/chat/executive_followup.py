"""
Records a scheduled Executive-Chatty follow-up (customer re-engagement or owner
reminder) as a first-class persisted document.  Each record is stored in its own
collection — NOT inside ``Chat.scheduled_messages[]`` — and is keyed by the owner's
HOME company plus the customer chat that triggered it.  The lifecycle runs from
``pending`` (queued, waiting for the EventBridge ``chatty-exec-fu-*`` schedule to
fire) through ``sent`` or ``cancelled`` and finally to ``done`` once the owner has
acted.
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import Field, field_validator

from letschatty.models.utils.types import StrObjectId
from ..base_models.chatty_asset_model import ChattyAssetModel


class ExecutiveFollowUpKind(StrEnum):
    CUSTOMER_REENGAGEMENT = "customer_reengagement"
    OWNER_REMINDER = "owner_reminder"


class ExecutiveFollowUpStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"
    DONE = "done"


class ExecutiveFollowUp(ChattyAssetModel):
    company_id: StrObjectId = Field(frozen=True, description="HOME company where the customer chat + this record live")
    chat_id: StrObjectId = Field(frozen=True, description="Customer chat in the home company")
    owner_waid: str = Field(description="Owner's WhatsApp id — who to nudge in the assistant company (api-chatty can't derive this; the home company's admin_phones live in cintia-lambdas)")
    kind: ExecutiveFollowUpKind
    fire_at: datetime = Field(description="UTC time the follow-up should fire")
    draft: Optional[str] = Field(default=None, description="Drafted follow-up / reminder message")
    status: ExecutiveFollowUpStatus = Field(default=ExecutiveFollowUpStatus.PENDING)
    schedule_name: Optional[str] = Field(default=None, description="EventBridge schedule name (chatty-exec-fu-...)")

    @field_validator("fire_at", mode="after")
    @classmethod
    def ensure_fire_at_utc(cls, v: datetime) -> datetime:
        """Normalise ``fire_at`` to UTC, mirroring ``TimestampValidationMixin.ensure_utc``.

        A naive datetime is assumed to already be UTC; an aware one is converted.
        Keeps the EventBridge fire-time comparison (``fire_at`` vs a UTC ``now()``)
        correct instead of silently comparing against a naive value.
        """
        return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
