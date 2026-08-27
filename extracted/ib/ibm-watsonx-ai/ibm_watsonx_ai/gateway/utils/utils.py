#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2026.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import logging

from ibm_watsonx_ai.gateway import Gateway
from ibm_watsonx_ai.utils import get_from_json
from ibm_watsonx_ai.wml_client_error import WMLClientError

logger = logging.getLogger(__name__)


def get_max_input_tokens(
    gateway: Gateway, model_id: str, max_completion_tokens: int = 1024
) -> int:
    """Get maximum number of tokens allowed as input for a given model.

    :param gateway: initialized Model Gateway instance
    :type gateway: Gateway

    :param model_id: unique model ID
    :type model_id: str

    :param max_completion_tokens: the maximum number of tokens that can be generated in the chat completion, defaults to 1024
    :type max_completion_tokens: int, optional

    :return: the maximum number of tokens allowed as input for a given model
    :rtype: int
    """
    model_details = gateway.models.get_details(model_id=model_id)
    model_context_window = get_from_json(model_details, ["metadata", "context_window"])

    if model_context_window is None:
        error_msg = (
            f"Maximum input tokens for the model id `{model_id}` cannot be calculated"
        )
        reason_msg = "The `context_window` cannot be found in the model metadata"
        raise WMLClientError(error_msg=error_msg, reason=reason_msg)

    return model_context_window - max_completion_tokens


def build_chat_params(
    kwargs: dict,
    temperature: float | None,
    max_completion_tokens: int | None,
    max_tokens: int | None,
    top_p: float | None,
    n: int | None,
    stop: dict | None,
    frequency_penalty: float | None,
    presence_penalty: float | None,
    logprobs: bool | None,
    top_logprobs: int | None,
    logit_bias: dict | None,
    seed: int | None,
    reasoning_effort: dict | None,
    tools: list | None,
    tool_choice: dict | None,
    parallel_tool_calls: bool | None,
    function_call: dict | None,
    functions: dict | None,
    response_format: dict | None,
    modalities: list | None,
    audio: dict | None,
    stream_options: dict | None,
    store: bool | None,
    metadata: dict | None,
    user: str | None,
    service_tier: dict | None,
    prediction: dict | None,
    router: dict | None,
    cache: dict | None,
) -> dict:
    return {
        k: v
        for k, v in {
            **kwargs,
            "temperature": temperature,
            "max_completion_tokens": max_completion_tokens,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "n": n,
            "stop": stop,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
            "logit_bias": logit_bias,
            "seed": seed,
            "reasoning_effort": reasoning_effort,
            "tools": tools,
            "tool_choice": tool_choice,
            "parallel_tool_calls": parallel_tool_calls,
            "function_call": function_call,
            "functions": functions,
            "response_format": response_format,
            "modalities": modalities,
            "audio": audio,
            "stream_options": stream_options,
            "store": store,
            "metadata": metadata,
            "user": user,
            "service_tier": service_tier,
            "prediction": prediction,
            "router": router,
            "cache": cache,
        }.items()
        if v is not None
    }


def build_generate_params(
    kwargs: dict,
    temperature: float | None,
    max_tokens: int | None,
    top_p: float | None,
    n: int | None,
    stop: list | None,
    frequency_penalty: float | None,
    presence_penalty: float | None,
    logprobs: int | None,
    logit_bias: dict | None,
    seed: int | None,
    echo: bool | None,
    suffix: str | None,
    stream_options: dict | None,
    metadata: dict | None,
    user: str | None,
    router: dict | None,
    best_of: int | None = None,
    cache: dict | None = None,
) -> dict:
    return {
        k: v
        for k, v in {
            **kwargs,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "n": n,
            "best_of": best_of,
            "stop": stop,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "logprobs": logprobs,
            "logit_bias": logit_bias,
            "seed": seed,
            "echo": echo,
            "suffix": suffix,
            "stream_options": stream_options,
            "metadata": metadata,
            "user": user,
            "router": router,
            "cache": cache,
        }.items()
        if v is not None
    }
