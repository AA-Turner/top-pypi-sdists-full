# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChunkExtraInfoSchema", "Chunk"]


class Chunk(TypedDict, total=False):
    text: Required[str]

    metadata: Dict[str, object]


class ChunkExtraInfoSchema(TypedDict, total=False):
    chunks: Required[Iterable[Chunk]]

    schema_type: Literal["CHUNKS"]
