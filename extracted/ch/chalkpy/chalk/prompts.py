from __future__ import annotations

import json
from typing import TYPE_CHECKING, List, Mapping, Optional, Sequence, Type, Union

import pyarrow as pa

if TYPE_CHECKING:
    from pydantic import BaseModel, Field
else:
    try:
        from pydantic.v1 import BaseModel, Field
    except ImportError:
        from pydantic import BaseModel, Field

from chalk.features.underscore import Underscore, UnderscoreFunction
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_v1


def message(role: str | Underscore, content: str | Underscore):
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
        The contents of the message. It is required for all messages.
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
    >>> from chalk.features import features, DataFrame, _
    >>> @features
    ... class User:
    ...    id: str
    ...    description: str
    ...    estimated_age_response: P.PromptResponse = P.completion(
    ...        model="gpt-3.5-turbo",
    ...        messages=[
    ...            P.message("system", F.jinja("Estimate the age of the user based on the description: {{User.description}}")),
    ...        ],
    ...        max_tokens=100+2*F.length(_.description)
    ...    )
    ...    estimated_age: float = F.json_value(_.estimated_age_response.response, "$.age")
    """
    if isinstance(messages, str) or isinstance(messages, Underscore):
        raise ValueError("Messages should be a list of P.message objects, not a single object.")
    messages_parsed = UnderscoreFunction(
        "array_constructor",
        *messages,
    )
    if output_structure is None:
        output_structure_json = None
    elif isinstance(output_structure, str):
        output_structure_json = output_structure
    elif is_pydantic_v1():
        output_structure_json = output_structure.schema_json()
    else:
        output_structure_json = json.dumps(
            output_structure.model_json_schema()  # pyright: ignore[reportAttributeAccessIssue]
        )

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
    model: str
    messages: List[Message]
    timeout_seconds: Optional[float] = None
    output_structure: Optional[str] = Field(description="Json representation of the output structure", default=None)
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_completion_tokens: Optional[int] = None
    max_tokens: Optional[int] = None
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Mapping[int, float]] = None
    seed: Optional[int] = None
    user: Optional[str] = None
    model_provider: Optional[str] = None
    base_url: Optional[str] = None
    num_retries: Optional[int] = None


class Usage(BaseModel):
    input_tokens: int = Field(description="Number of tokens in the request.")
    output_tokens: int = Field(description="Number of tokens in the response.")
    total_tokens: int = Field(description="Total number of tokens used, equal to input_tokens + output_tokens.")


class RuntimeStats(BaseModel):
    total_latency: float = Field(description="Total time in seconds to generate the response, including any retries.")
    last_try_latency: Optional[float] = Field(
        description="Time in seconds to generate the response in the last successful try."
    )

    total_retries: int = Field(description="Total number of retries.")
    rate_limit_retries: int = Field(description="Number of retries due to rate limiting.")


class PromptResponse(BaseModel):
    response: Optional[str] = Field(
        description="Response from the model. Raw string if no output structure specified, json encoded string otherwise. None if the response was not received or incorrectly formatted."
    )
    prompt: Prompt
    usage: Usage
    runtime_stats: RuntimeStats
