from __future__ import annotations

from typing import TYPE_CHECKING, List, Mapping, Optional, Sequence, Type, Union

import pyarrow as pa

if TYPE_CHECKING:
    from pydantic import BaseModel
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel

from chalk.features.underscore import Underscore, UnderscoreFunction
from chalk.utils.pydanticutil.pydantic_compat import get_pydantic_output_structure


def _message_content(
    *,
    type: Optional[str | Underscore] = None,
    text: Optional[str | Underscore] = None,
    image_url: Optional[str | Underscore] = None,
    detail: Optional[str | Underscore] = None,
):
    return UnderscoreFunction(
        "struct_pack",
        ["type", "text", "image_url", "detail"],
        type if type is not None else pa.scalar(None, type=pa.large_string()),
        text if text is not None else pa.scalar(None, type=pa.large_string()),
        image_url if image_url is not None else pa.scalar(None, type=pa.large_string()),
        detail if detail is not None else pa.scalar(None, type=pa.large_string()),
    )


def message(role: str | Underscore, content: str | list[dict[str, str]] | Underscore):
    if isinstance(content, list):
        return UnderscoreFunction(
            "struct_pack",
            ["role", "content"],
            role,
            UnderscoreFunction("array_constructor", *[_message_content(**c) for c in content]),
        )
    return UnderscoreFunction(
        "struct_pack",
        ["role", "content"],
        role,
        content,
    )


def run_prompt(name: str):
    """
    Runs a named prompt. Configure named prompts in the UI.

    Parameters
    ----------
    name
        The name of the prompt to run.

    Examples
    --------
    >>> import chalk.prompts as P
    >>> from chalk.features import features
    >>> @features
    ... class User:
    ...    id: str
    ...    description: P.PromptResponse = P.run_prompt("describe_user")
    """
    return UnderscoreFunction("run_prompt", prompt_name=name)


def completion(
    model: str,
    messages: Sequence[Underscore],
    *,
    timeout_seconds: Optional[float] = None,
    output_structure: Optional[Union[Type[BaseModel], str]] = None,
    temperature: Optional[float | Underscore] = None,
    top_p: Optional[float | Underscore] = None,
    max_completion_tokens: Optional[int | Underscore] = None,
    max_tokens: Optional[int | Underscore] = None,
    stop: Optional[Sequence[str]] = None,
    presence_penalty: Optional[float | Underscore] = None,
    frequency_penalty: Optional[float | Underscore] = None,
    logit_bias: Optional[Mapping[int, float]] = None,
    seed: Optional[int | Underscore] = None,
    user: Optional[str | Underscore] = None,
    model_provider: Optional[str | Underscore] = None,
    base_url: Optional[str | Underscore] = None,
    api_key: Optional[str | Underscore] = None,
    num_retries: Optional[int | Underscore] = None,
):
    """
    Generate LLM model completions from a list of messages.

    Parameters
    ----------
    model
        The name of the model, e.g. "gpt-4o".
    messages
        The list of messages of the type P.Message. Each message in the array contains the following properties: role and content.
        The role of the message's author. Roles can be: system, user, or assistant.
        The contents of the message. It can be a string or a list of objects with the following properties: type and text or image_url.
    timeout_seconds
        The timeout in seconds for completion requests
    output_structure
        The object specifying the format that the model must output. Accepts a Pydantic model or a JSON schema string (see https://docs.pydantic.dev/1.10/usage/schema/).
    temperature
        The sampling temperature to be used, between 0 and 2 inclusive. Higher values like 0.8 produce more random outputs, while lower values like 0.2 make outputs more focused and deterministic.
        Note: This parameter is between 0 and 1 (inclusive) for Anthropic models.
    top_p
        The alternative to sampling with temperature. It instructs the model to consider the results of the tokens with top_p probability. For example, 0.1 means only the tokens comprising the top 10% probability mass are considered.
    max_completion_tokens
        The upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens.
    max_tokens
        The maximum number of tokens to generate in the chat completion.
    stop
        Custom text sequences that will cause the model to stop generating.
    presence_penalty
        It is used to penalize new tokens based on their existence in the text so far.
    frequency_penalty
        It is used to penalize new tokens based on their frequency in the text so far.
    logit_bias
        Used to modify the probability of specific tokens appearing in the completion.
    seed
        If specified, the system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed.
    user
        The unique identifier representing your end-user. This parameter is specific to OpenAI and can help to monitor and detect abuse.
    model_provider
        The model provider.
    base_url
        The URL of the API endpoint where requests are sent.
    api_key
        The API key to use for the completion.
    num_retries
        The number of times to retry the API call if an APIError, TimeoutError or ServiceUnavailableError occurs.

    Examples
    --------
    >>> import chalk.prompts as P
    >>> import chalk.functions as F
    >>> from chalk.features import features, _
    >>> from pydantic import BaseModel
    >>> class EstimatedAge(BaseModel):
    ...     age: float
    ...
    >>> @features
    ... class User:
    ...    id: str
    ...    description: str
    ...    estimated_age_response: P.PromptResponse = P.completion(
    ...        model="gpt-4o",
    ...        messages=[
    ...            P.message(
    ...                "user",
    ...                F.jinja("Estimate the age of the user based on the description: {{User.description}}"),
    ...            ),
    ...        ],
    ...        output_structure=EstimatedAge,
    ...    )
    ...    estimated_age: float = F.json_value(_.estimated_age_response.response, "$.age")
    ...    image_url: str
    ...    image_response: P.MultimodalPromptResponse = P.completion(
    ...        model="gpt-4o",
    ...        messages=[
    ...            P.message(
    ...                "user",
    ...                [
    ...                    {"type": "input_text", "text": "describe this image"},
    ...                    {"type": "input_image", "image_url": _.image_url},
    ...                ],
    ...            ),
    ...        ],
    ...        max_tokens=100+2*F.length(_.description)
    ...    )
    """
    if isinstance(messages, str) or isinstance(messages, Underscore):
        raise ValueError("Messages should be a list of P.message objects, not a single object.")
    messages_parsed = UnderscoreFunction("array_constructor", *messages)
    if output_structure is None:
        output_structure_json = None
    elif isinstance(output_structure, str):
        output_structure_json = output_structure
    else:
        output_structure_json = get_pydantic_output_structure(output_structure)

    return UnderscoreFunction(
        "completion",
        model=model,
        messages=messages_parsed,
        timeout_seconds=timeout_seconds,
        output_structure=output_structure_json,
        temperature=temperature,
        top_p=top_p,
        max_completion_tokens=max_completion_tokens,
        max_tokens=max_tokens,
        stop=stop,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        logit_bias=pa.scalar(list(logit_bias.items()), type=pa.map_(pa.int64(), pa.float64()))
        if logit_bias is not None
        else None,
        seed=seed,
        user=user,
        num_retries=num_retries,
        model_provider=model_provider,
        base_url=base_url,
        api_key=api_key,
    )


class Message(BaseModel):
    role: str
    content: str


class Prompt(BaseModel):
    """Chalk Prompts are bundles of a model, a list of messages, and parameters."""

    model: str
    """The name of the model, e.g. "gpt-4o"."""
    messages: List[Message]
    """The list of messages of the type P.Message. Each message in the array contains the following properties: role and content.
    The role of the message's author. Roles can be: system, user, or assistant.
    The contents of the message. It is required for all messages."""
    timeout_seconds: Optional[float] = None
    """The timeout in seconds for completion requests."""
    output_structure: Optional[str] = None
    """The object specifying the format that the model must output. Accepts a Pydantic model or a JSON schema string (see https://docs.pydantic.dev/1.10/usage/schema/)."""
    temperature: Optional[float] = None
    """The sampling temperature to be used, between 0 and 2 inclusive. Higher values like 0.8 produce more random outputs, while lower values like 0.2 make outputs more focused and deterministic.
    Note: This parameter is between 0 and 1 (inclusive) for Anthropic models."""
    top_p: Optional[float] = None
    """The alternative to sampling with temperature. It instructs the model to consider the results of the tokens with top_p probability. For example, 0.1 means only the tokens comprising the top 10% probability mass are considered."""
    max_completion_tokens: Optional[int] = None
    """The upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens."""
    max_tokens: Optional[int] = None
    """The maximum number of tokens to generate in the chat completion."""
    stop: Optional[List[str]] = None
    """Custom text sequences that will cause the model to stop generating."""
    presence_penalty: Optional[float] = None
    """It is used to penalize new tokens based on their existence in the text so far."""
    frequency_penalty: Optional[float] = None
    """It is used to penalize new tokens based on their frequency in the text so far."""
    logit_bias: Optional[Mapping[int, float]] = None
    """Used to modify the probability of specific tokens appearing in the completion."""
    seed: Optional[int] = None
    """If specified, the system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed."""
    user: Optional[str] = None
    """The unique identifier representing your end-user. This parameter is specific to OpenAI and can help to monitor and detect abuse."""
    model_provider: Optional[str] = None
    """The model provider."""
    base_url: Optional[str] = None
    """The URL of the API endpoint where requests are sent."""
    num_retries: Optional[int] = None
    """The number of times to retry the API call if an APIError, TimeoutError or ServiceUnavailableError occurs."""


class MultimodalMessage(BaseModel):
    role: str
    content: List[Mapping[str, str]]


class MultimodalPrompt(BaseModel):
    """Chalk Prompts are bundles of a model, a list of messages, and parameters."""

    model: str
    """The name of the model, e.g. "gpt-4o"."""
    messages: List[MultimodalMessage]
    """The list of messages of the type P.Message. Each message in the array contains the following properties: role and content.
    The role of the message's author. Roles can be: system, user, or assistant.
    The contents of the message. It is a list of objects with the following properties: type and text or image_url."""
    timeout_seconds: Optional[float] = None
    """The timeout in seconds for completion requests."""
    output_structure: Optional[str] = None
    """The object specifying the format that the model must output. Accepts a Pydantic model or a JSON schema string (see https://docs.pydantic.dev/1.10/usage/schema/)."""
    temperature: Optional[float] = None
    """The sampling temperature to be used, between 0 and 2 inclusive. Higher values like 0.8 produce more random outputs, while lower values like 0.2 make outputs more focused and deterministic.
    Note: This parameter is between 0 and 1 (inclusive) for Anthropic models."""
    top_p: Optional[float] = None
    """The alternative to sampling with temperature. It instructs the model to consider the results of the tokens with top_p probability. For example, 0.1 means only the tokens comprising the top 10% probability mass are considered."""
    max_completion_tokens: Optional[int] = None
    """The upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens."""
    max_tokens: Optional[int] = None
    """The maximum number of tokens to generate in the chat completion."""
    stop: Optional[List[str]] = None
    """Custom text sequences that will cause the model to stop generating."""
    presence_penalty: Optional[float] = None
    """It is used to penalize new tokens based on their existence in the text so far."""
    frequency_penalty: Optional[float] = None
    """It is used to penalize new tokens based on their frequency in the text so far."""
    logit_bias: Optional[Mapping[int, float]] = None
    """Used to modify the probability of specific tokens appearing in the completion."""
    seed: Optional[int] = None
    """If specified, the system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed."""
    user: Optional[str] = None
    """The unique identifier representing your end-user. This parameter is specific to OpenAI and can help to monitor and detect abuse."""
    model_provider: Optional[str] = None
    """The model provider."""
    base_url: Optional[str] = None
    """The URL of the API endpoint where requests are sent."""
    num_retries: Optional[int] = None
    """The number of times to retry the API call if an APIError, TimeoutError or ServiceUnavailableError occurs."""


class Usage(BaseModel):
    """Usage statistics for the response."""

    input_tokens: int
    """Number of tokens in the request."""
    output_tokens: int
    """Number of tokens in the response."""
    total_tokens: int
    """Total number of tokens used, equal to input_tokens + output_tokens."""


class RuntimeStats(BaseModel):
    """Runtime statistics for the response."""

    total_latency: float
    """Total time in seconds to generate the response, including any retries."""
    last_try_latency: Optional[float]
    """Time in seconds to generate the response in the last successful try."""
    total_retries: int
    """Total number of retries."""
    rate_limit_retries: int
    """Number of retries due to rate limiting."""


class PromptResponse(BaseModel):
    """Response from the model."""

    response: Optional[str]
    """Response from the model. Raw string if no output structure specified, json encoded string otherwise. None if the response was not received or incorrectly formatted."""
    prompt: Prompt
    """Prompt used to generate the response."""
    usage: Usage
    """Usage statistics for the response."""
    runtime_stats: RuntimeStats
    """Runtime statistics for the response."""


class MultimodalPromptResponse(BaseModel):
    """Response from the model."""

    response: Optional[str]
    """Response from the model. Raw string if no output structure specified, json encoded string otherwise. None if the response was not received or incorrectly formatted."""
    prompt: MultimodalPrompt
    """Prompt used to generate the response."""
    usage: Usage
    """Usage statistics for the response."""
    runtime_stats: RuntimeStats
    """Runtime statistics for the response."""
