"""Text Completion API resource.
"""
from typing import List, Optional, Union

from databricks_genai_inference.api.abstract.foundation_model_api_resource import (FoundationModelAPIInput,
                                                                                   FoundationModelAPIResource)
from databricks_genai_inference.api.objects.completion_chunk_object import CompletionChunkObject
from databricks_genai_inference.api.objects.completion_object import CompletionObject
from databricks_genai_inference.api.util import CompletionModel


class CompletionAPIInput(FoundationModelAPIInput):
    """
    A class representing the input parameters for the completion API.

    Attributes:
        prompt (Union[str, List[str]]): The prompt(s) to generate completions. Can be a string or a list of strings.
        user (Optional[str]): An id representing the user making the request.
        max_tokens (Optional[int]): The maximum number of tokens to generate.
        temperature (Optional[float]): The sampling temperature. Use higher value for more random outputs and lower value for more deterministic outputs. Must be between 0 and 2. Defaults to 1.0.
        top_p (Optional[float]): The probability threshold used for nucleus sampling. Must be between 0 and 1. Defaults to 1.
        top_k (Optional[int]): Defines the number of k most likely tokens to use for top-k-filtering. Set this value to 1 to make outputs deterministic.
        stream (Optional[bool]): If set to True, the API will stream the partial output as it’s generated as message chunks. Defaults to False.
        n (Optional[int]): The number of completion choices to return. Currently, only 1 choice is supported.
        suffix (Optional[str]): A string that is appended to the end of every completion. Defaults to an empty string.
        echo (Optional[bool]): If set to True, the API will echo the prompt in the completion. Defaults to False.
        error_behavior (Optional[str]): Error behavior when timeouts or context-length-exceeded errors happen. Two options: “truncate” (return as many tokens as possible) and “error” (return an error). Defaults to "error".
        stop (Optional[Union[str, List[str]]]): API will stop generating further tokens when any one of the sequences in stop are encountered.
        use_raw_prompt (Optional[bool]): If set to True, API will skip prompt template and use the raw prompt. Defaults to False.
    """
    prompt: Union[str, List[str]]
    user: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    stream: Optional[bool] = None
    n: Optional[int] = None
    suffix: Optional[str] = None
    echo: Optional[bool] = None
    error_behavior: Optional[str] = None
    stop: Optional[Union[str, List[str]]] = None
    use_raw_prompt: Optional[bool] = None


class Completion(FoundationModelAPIResource):
    """
    A class representing the text completion API resource.
    """

    SUPPORTED_MODEL_LIST = [model.value for model in CompletionModel.__members__.values()]
    model_input = CompletionAPIInput
    model_output = CompletionObject
    model_streaming_output = CompletionChunkObject
