from enum import Enum
from typing import Optional

import attrs

from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.quota.response import Quota, QuotaCredit
from grazie.api.client.utils import typ_or_none


@attrs.define(auto_attribs=True)
class LLMChatEventV5:
    type: str
    content: str
    name: Optional[str] = None


class LLMChatEventTypeV6(str, Enum):
    Content = "Content"
    FunctionCall = "FunctionCall"
    QuotaMetadata = "QuotaMetadata"


@attrs.define(auto_attribs=True)
class LLMChatEvent:
    type: LLMChatEventTypeV6 = attrs.field(
        converter=LLMChatEventTypeV6  # pyright: ignore [reportGeneralTypeIssues]
    )
    content: str = ""
    name: Optional[str] = None
    updated: Optional[Quota] = typ_or_none(Quota)
    spent: Optional[QuotaCredit] = typ_or_none(QuotaCredit)


@attrs.define(auto_attribs=True, frozen=True)
class ChatResponse:
    prompt: ChatPrompt
    content: str
    function_call: Optional[str] = None
    updated: Optional[Quota] = None
    spent: Optional[QuotaCredit] = None


@attrs.define(auto_attribs=True, frozen=True)
class ChatResponseStream:
    chunk: str
    function_call: Optional[str] = None
    updated: Optional[Quota] = None
    spent: Optional[QuotaCredit] = None
