# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["TokenChunkingStrategyConfigParam"]


class TokenChunkingStrategyConfigParam(TypedDict, total=False):
    strategy: Required[Literal["token"]]

    chunk_overlap: int
    """Number of tokens to overlap between chunks.

    If not specified, an overlap of 0 will be used. Not this if only followed
    approximately.
    """

    max_chunk_size: int
    """Maximum number of tokens in each chunk.

    If not specified, a maximum chunk size of 600 will be used.
    """

    separator: str
    """Character designating breaks in input data.

    Text data will first be split into sections by this separator, then each section
    will be split into chunks of size `chunk_size`.
    """

    target_chunk_size: int
    """Target number of tokens in each chunk.

    If not specified, a target chunk size of 200 will be used.
    """
