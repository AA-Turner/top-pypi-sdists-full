# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["CompletionResponse", "Choice", "ChoiceLogprobs", "ChoiceLogprobsContent", "ChoiceLogprobsContentTopLogprob"]


class ChoiceLogprobsContentTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None


class ChoiceLogprobsContent(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[ChoiceLogprobsContentTopLogprob]

    bytes: Optional[List[int]] = None


class ChoiceLogprobs(BaseModel):
    content: Optional[List[ChoiceLogprobsContent]] = None


class Choice(BaseModel):
    index: int

    logprobs: Optional[ChoiceLogprobs] = None


class CompletionResponse(BaseModel):
    completions: List[List[object]]

    choices: Optional[List[Choice]] = None

    finish_reason: Optional[str] = None

    prompt_tokens: Optional[int] = None

    response_tokens: Optional[int] = None
