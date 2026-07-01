# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CharacterChunkingStrategyConfig"]


class CharacterChunkingStrategyConfig(BaseModel):
    strategy: Literal["character"]

    chunk_overlap: Optional[int] = None
    """Number of characters to overlap between chunks.

    If not specified, an overlap of 200 will be used. For example if the chunk size
    is 3 and the overlap size is 1, and the text to chunk is 'abcde', the chunks
    will be 'abc', 'cde'.
    """

    chunk_size: Optional[int] = None
    """Maximum number of characters in each chunk.

    If not specified, a chunk size of 1000 will be used.
    """

    separator: Optional[str] = None
    """Character designating breaks in input data.

    Text data will first be split into sections by this separator, then each section
    will be split into chunks of size `chunk_size`.
    """
