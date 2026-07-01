# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TokenChunkingStrategyConfig"]


class TokenChunkingStrategyConfig(BaseModel):
    strategy: Literal["token"]

    chunk_overlap: Optional[int] = None
    """Number of tokens to overlap between chunks.

    If not specified, an overlap of 0 will be used. Not this if only followed
    approximately.
    """

    max_chunk_size: Optional[int] = None
    """Maximum number of tokens in each chunk.

    If not specified, a maximum chunk size of 600 will be used.
    """

    separator: Optional[str] = None
    """Character designating breaks in input data.

    Text data will first be split into sections by this separator, then each section
    will be split into chunks of size `chunk_size`.
    """

    target_chunk_size: Optional[int] = None
    """Target number of tokens in each chunk.

    If not specified, a target chunk size of 200 will be used.
    """
