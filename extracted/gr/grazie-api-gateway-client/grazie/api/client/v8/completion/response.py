from typing import Optional, Union

import attrs

from grazie.api.client._common import StopReason, UnknownMetadataResponse
from grazie.api.client.quota.response import QuotaResponse
from grazie.api.client.v8.completion.prompt import CompletionPrompt


@attrs.define(auto_attribs=True, frozen=True)
class CompletionContentStreamChunk:
    content: str


@attrs.define(auto_attribs=True, frozen=True)
class CompletionFinishMetadataResponse:
    reason: StopReason = StopReason.UNKNOWN
    content: str = ""


@attrs.define(auto_attribs=True, frozen=True)
class CompletionResponse:
    prompt: CompletionPrompt
    content: str
    quota: QuotaResponse
    stop_reason: Optional[str] = None
    unknown_metadata: Optional[UnknownMetadataResponse] = None


CompletionResponseStream = Union[
    CompletionContentStreamChunk,
    CompletionFinishMetadataResponse,
    QuotaResponse,
    UnknownMetadataResponse,
]
