import attrs

from grazie.api.client.completion.prompt import CompletionPrompt


@attrs.define(auto_attribs=True)
class LLMCompleteEventV3:
    current: str


@attrs.define(auto_attribs=True, frozen=True)
class CompletionResponse:
    prompt: CompletionPrompt
    completion: str


@attrs.define(auto_attribs=True, frozen=True)
class CompletionResponseStream:
    chunk: str
