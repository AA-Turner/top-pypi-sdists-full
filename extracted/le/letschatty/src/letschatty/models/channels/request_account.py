"""The account a request acts as, whatever its channel (ADR-011 §12, E3).

Common code (use cases, the chat) only needs WHICH account and of WHICH channel: `account_id`, `company_id` and
`channel`. Each channel extends it with what talking to its provider takes (WhatsApp: `AccountContext`, with the
number, the WABA and the token). `ExecutionContext.account` holds one of these.
"""
from pydantic import BaseModel, ConfigDict

from ..utils.types.channel_types import Channel
from ..utils.types.identifier import StrObjectId


class RequestAccount(BaseModel):
    account_id: StrObjectId
    company_id: StrObjectId
    channel: Channel

    model_config = ConfigDict(frozen=True)
