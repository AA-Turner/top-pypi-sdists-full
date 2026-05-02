# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .embedding_model_name import EmbeddingModelName

__all__ = ["EmbeddingConfigBase"]


class EmbeddingConfigBase(BaseModel):
    embedding_model: EmbeddingModelName
    """The name of the base embedding model to use.

    To use custom models, change to type 'models'.
    """

    type: Optional[Literal["base"]] = None
    """The type of the embedding configuration."""
