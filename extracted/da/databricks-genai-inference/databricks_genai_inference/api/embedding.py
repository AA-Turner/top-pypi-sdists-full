"""Embedding API resource.
"""
from typing import List, Optional, Union

from databricks_genai_inference.api.abstract.foundation_model_api_resource import (FoundationModelAPIInput,
                                                                                   FoundationModelAPIResource)
from databricks_genai_inference.api.objects.embedding_object import EmbeddingObject
from databricks_genai_inference.api.util import EmbeddingModel


class EmbeddingAPIInput(FoundationModelAPIInput):
    """
    A class representing the input schema for the Embedding API.

    Attributes:
        input (Union[str, List[str]]): The input text to embed. Can be a string or a list of strings.
        instruction (Optional[str]): The task instruction. If not provided, only the input will be embedded.
        user (Optional[str]): An id representing the user making the request.
    """
    input: Union[str, List[str]]
    instruction: Optional[str] = None
    user: Optional[str] = None


class Embedding(FoundationModelAPIResource):
    """
    A class representing the embedding API resource.
    """
    SUPPORTED_MODEL_LIST = [model.value for model in EmbeddingModel.__members__.values()]
    model_input = EmbeddingAPIInput
    model_output = EmbeddingObject

    @classmethod
    def _get_streaming_response(cls, url, headers, json, timeout):
        raise NotImplementedError("Streaming is not supported for the Embedding API.")

    @classmethod
    async def _aget_streaming_response(cls, url, json, timeout, extra_headers=None):
        raise NotImplementedError("Streaming is not supported for the Embedding API.")
