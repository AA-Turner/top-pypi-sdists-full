from typing import Required, Union, TypedDict


class LlmProxyCost(TypedDict, total=False):
    """ llm_proxy_cost. """

    timestamp: Required[str]
    """
    ISO 8601 UTC timestamp of the LLM call

    Required property
    """

    org_id: Required[int]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    feature: Required[str]
    """
    Seer feature that initiated the call (e.g. autofix, issue_detection)

    Required property
    """

    model: Required[str]
    """
    LLM model name (e.g. claude-sonnet-4-6)

    Required property
    """

    region: str
    """ Vertex region or 'global' """

    call_type: str
    """ LLM call type (e.g. chat.completion, embedding) """

    prompt_tokens: Required[int]
    """ Required property """

    completion_tokens: Required[int]
    """ Required property """

    cache_read_tokens: int
    cache_write_tokens: int
    total_cost_usd: Required[Union[int, float]]
    """
    Corrected total cost in USD (includes regional/long-context adjustments)

    Required property
    """

    input_cost_usd: Union[int, float]
    output_cost_usd: Union[int, float]
    cache_read_cost_usd: Union[int, float]
    cache_write_cost_usd: Union[int, float]
    litellm_cost_usd: Union[int, float]
    """ Original uncorrected cost from LiteLLM """

    is_long_context: int
    """ 1 if input exceeded 200K token threshold, 0 otherwise """

    is_regional: int
    """ 1 if Claude model on non-global Vertex region, 0 otherwise """

    response_time_ms: Union[int, float]
    litellm_call_id: str
