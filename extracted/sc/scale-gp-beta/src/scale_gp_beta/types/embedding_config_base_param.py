# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .embedding_model_name import EmbeddingModelName

__all__ = ["EmbeddingConfigBaseParam"]


class EmbeddingConfigBaseParam(TypedDict, total=False):
    embedding_model: Required[EmbeddingModelName]
    """The name of the base embedding model to use.

    To use custom models, change to type 'models'.
    """

    type: Literal["base"]
    """The type of the embedding configuration."""
