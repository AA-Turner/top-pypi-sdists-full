from enum import Enum
from typing import List, Optional, Union

import attrs

from grazie.api.client._common import StopReason, UnknownMetadataResponse
from grazie.api.client.quota.response import QuotaResponse
from grazie.api.client.v8.chat.prompt import ChatPrompt


class LLMChatEventType(str, Enum):
    Content = "Content"
    QuotaMetadata = "QuotaMetadata"


@attrs.define(auto_attribs=True, frozen=True)
class ChatContentStreamChunk:
    content: str
    choiceIndex: Optional[int] = None


@attrs.define(auto_attribs=True, frozen=True)
class ChatToolCallStreamChunk:
    choiceIndex: Optional[int] = None
    parallelToolIndex: Optional[int] = None
    id: Optional[str] = None
    name: Optional[str] = None
    content: str = ""


@attrs.define(auto_attribs=True, frozen=True)
class ChatFinishMetadataResponse:
    reason: StopReason = StopReason.UNKNOWN
    choiceIndex: Optional[int] = None
    content: str = ""


@attrs.define(auto_attribs=True, frozen=True)
class ChatToolResponse:
    content: str
    parallelToolIndex: Optional[int] = None
    id: Optional[str] = None
    name: Optional[str] = None


@attrs.define(auto_attribs=True, frozen=True)
class ChatSingleResponse:
    stop_reason: Optional[str] = None
    content: Optional[str] = None
    tool_calls: List[ChatToolResponse] = []


@attrs.define(auto_attribs=True, frozen=True)
class ChatResponse:
    prompt: ChatPrompt
    responses: List[ChatSingleResponse]
    quota: QuotaResponse
    unknown_metadata: Optional[UnknownMetadataResponse] = None

    @property
    def content(self) -> str:
        """
        Aggregate texts from all responses.
        """
        texts: List[str] = []
        for r in self.responses:
            texts.append(r.content) if r.content else None
            texts.extend(tool.content for tool in r.tool_calls) if r.tool_calls else None
        return "\n".join(texts)


ChatResponseStream = Union[
    ChatContentStreamChunk,
    ChatToolCallStreamChunk,
    QuotaResponse,
    ChatFinishMetadataResponse,
    UnknownMetadataResponse,
]

IndexableStreamChunk = Union[
    ChatContentStreamChunk, ChatToolCallStreamChunk, ChatFinishMetadataResponse
]
