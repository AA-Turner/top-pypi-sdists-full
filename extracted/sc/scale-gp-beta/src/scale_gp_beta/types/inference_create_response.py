# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .inference_response import InferenceResponse
from .inference_response_chunk import InferenceResponseChunk

__all__ = ["InferenceCreateResponse"]

InferenceCreateResponse: TypeAlias = Union[InferenceResponse, InferenceResponseChunk]
