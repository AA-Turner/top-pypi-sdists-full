"""Everything needed to talk to Meta as one account, for one request.

A `RequestAccount` of the WhatsApp channel (ADR-011 §12, E3): common code reads only `account_id`, `company_id`
and `channel`; what talks to Meta reads the rest.

Immutable and passed explicitly: the in-memory company object is shared by concurrent requests
for different numbers, so the account can never be one of its attributes. Every sender takes
an `AccountContext` and builds its Graph client from it; nothing that sends reads the company.
"""

from typing import Optional

from pydantic import ConfigDict, Field, SecretStr, field_validator

from ..channels.channel import WhatsAppClientInfo
from ..channels.request_account import RequestAccount
from ..utils.types.channel_types import Channel


class AccountContext(RequestAccount):
    #: Always WhatsApp. Typed as `Channel` (not a `Literal`) so a dumped account comes back: `"whatsapp"` as text
    #: validates, any other channel is refused.
    channel: Channel = Channel.WHATSAPP
    account_name: str
    phone_number_id: str
    display_phone_number: str
    waba_id: str
    portfolio_id: Optional[str] = None
    dataset_id: Optional[str] = None
    is_default: bool = False
    #: False when the webhook arrived on a number the account no longer uses (the 5A case).
    via_current_number: bool = True
    token: SecretStr = Field(repr=False)

    model_config = ConfigDict(frozen=True)

    @field_validator("channel")
    @classmethod
    def _only_whatsapp(cls, channel: Channel) -> Channel:
        if channel is not Channel.WHATSAPP:
            raise ValueError(f"an AccountContext is a WhatsApp account, not {channel.value}")
        return channel

    @property
    def channel_id(self) -> str:
        """The legacy `Chat.channel_id` value. letschatty <= 0.5.x requires it on every chat."""
        return f"whatsapp_{self.phone_number_id}"

    def client_info(self) -> WhatsAppClientInfo:
        """The only factory of the Graph client for this account."""
        return WhatsAppClientInfo(
            display_phone_number=self.display_phone_number,
            business_phone_number_id=self.phone_number_id,
            access_token=self.token,
            waba_id=self.waba_id,
            dataset_id=self.dataset_id,
        )
