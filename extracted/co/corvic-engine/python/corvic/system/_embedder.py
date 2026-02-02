import dataclasses
from collections.abc import Sequence
from typing import Literal

import polars as pl
from typing_extensions import Protocol

from corvic.result import InternalError, InvalidArgumentError, Ok


@dataclasses.dataclass
class EmbedTextContext:
    """Data to be embedded and arguments to describe how to embed them."""

    inputs: Sequence[str] | pl.Series
    model_name: str
    tokenizer_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: Literal[32, 64]


@dataclasses.dataclass
class EmbedTextResult:
    """The result of running text embedding on an EmbedTextContext."""

    context: EmbedTextContext
    embeddings: pl.Series


class TextEmbedder(Protocol):
    """Use a model to embed text."""

    def embed(
        self, context: EmbedTextContext
    ) -> Ok[EmbedTextResult] | InvalidArgumentError | InternalError: ...


@dataclasses.dataclass
class EmbedImageContext:
    """Data to be embedded and arguments to describe how to embed them."""

    inputs: Sequence[bytes] | pl.Series
    model_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: Literal[32, 64]


@dataclasses.dataclass
class EmbedImageResult:
    """The result of running Image embedding on an EmbedImageContext."""

    context: EmbedImageContext
    embeddings: pl.Series


class ImageEmbedder(Protocol):
    """Use a model to embed text."""

    def embed(
        self, context: EmbedImageContext
    ) -> Ok[EmbedImageResult] | InvalidArgumentError | InternalError: ...
