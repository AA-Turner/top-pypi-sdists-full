# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ModelParameters"]


class ModelParameters(BaseModel):
    frequency_penalty: Optional[float] = None
    """Penalize tokens based on how much they have already appeared in the text.

    Positive values encourage the model to generate new tokens and negative values
    encourage the model to repeat tokens. Available for models from LLM Engine, and
    OpenAI
    """

    max_tokens: Optional[int] = None
    """The maximum number of tokens to generate in the completion.

    The token count of your prompt plus max_tokens cannot exceed the model's context
    length. If not, specified, max_tokens will be determined based on the model
    used: | Model API family | Model API default | EGP applied default | | --- | ---
    | --- | | OpenAI Completions |
    [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
    | `context window - prompt size` | | OpenAI Chat Completions |
    [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
    | `context window - prompt size` | | LLM Engine |
    [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
    parameter is required | `100` | | Anthropic Claude 2 |
    [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
    parameter is required | `10000` |
    """

    presence_penalty: Optional[float] = None
    """Penalize tokens based on if they have already appeared in the text.

    Positive values encourage the model to generate new tokens and negative values
    encourage the model to repeat tokens. Available for models from LLM Engine, and
    OpenAI.
    """

    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None
    """The effort level for the model to reason. Available for models from OpenAI."""

    stop_sequences: Optional[List[str]] = None
    """List of up to 4 sequences where the API will stop generating further tokens.

    The returned text will not contain the stop sequence.
    """

    temperature: Optional[float] = None
    """What sampling temperature to use, between [0, 1].

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic. Setting temperature=0.0 will
    enable fully deterministic (greedy) sampling. Temperature is ignored for OpenAI
    reasoning models.
    """

    top_k: Optional[int] = FieldInfo(alias="topK", default=None)
    """Sample from the k most likely next tokens at each step.

    Lower k focuses on higher probability tokens. Available for models from
    Anthropic, Google, and LLM Engine.
    """

    top_p: Optional[float] = FieldInfo(alias="topP", default=None)
    """The cumulative probability cutoff for token selection.

    Lower values mean sampling from a smaller, more top-weighted nucleus. Available
    for models from Anthropic, Google, Mistral, LLM Engine, and OpenAI.
    """
