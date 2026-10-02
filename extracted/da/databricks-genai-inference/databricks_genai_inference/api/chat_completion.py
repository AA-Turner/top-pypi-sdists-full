"""Chat Completion API resource.
"""
from typing import List, Optional, Union

from databricks_genai_inference.api.abstract.foundation_model_api_resource import (FoundationModelAPIInput,
                                                                                   FoundationModelAPIResource)
from databricks_genai_inference.api.objects.chat_completion_chunk_object import ChatCompletionChunkObject
from databricks_genai_inference.api.objects.chat_completion_object import ChatCompletionObject
from databricks_genai_inference.api.util import ChatCompletionModel


class ChatCompletionAPIInput(FoundationModelAPIInput):
    """
    A class representing the input schema for the Chat Completion API.

    Attributes:
        messages (List[dict]): A list of messages comprising the conversation so far. Each message is a dictionary with the following keys: `role` (str), `content` (str)
        user (Optional[str]): An id representing the user making the request.
        max_tokens (Optional[int]): The maximum number of tokens to generate.
        temperature (Optional[float]): The sampling temperature. Use higher value for more random outputs and lower value for more deterministic outputs. Must be between 0 and 2. Defaults to 1.0.
        top_p (Optional[float]): The probability threshold used for nucleus sampling. Must be between 0 and 1. Defaults to 1.
        top_k (Optional[int]): Defines the number of k most likely tokens to use for top-k-filtering. Set this value to 1 to make outputs deterministic.
        stream (Optional[bool]): If set to True, the API will stream the partial output as it’s generated as message chunks. Defaults to False.
        n (Optional[int]): The number of completion choices to return. Currently, only 1 choice is supported.
    """
    messages: List[dict]
    user: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    stream: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    n: Optional[int] = None


class ChatCompletion(FoundationModelAPIResource):
    """
    A class representing the chat completion API resource.
    """
    SUPPORTED_MODEL_LIST = [model.value for model in ChatCompletionModel.__members__.values()]
    model_input = ChatCompletionAPIInput
    model_output = ChatCompletionObject
    model_streaming_output = ChatCompletionChunkObject

    @classmethod
    def create(cls, **kwargs):
        return super().create(**kwargs)
