# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

from .embedding_model_name import EmbeddingModelName
from .embedding_config_param import EmbeddingConfigParam

__all__ = ["VectorStoreCreateParams"]


class VectorStoreCreateParams(TypedDict, total=False):
    name: Required[str]
    """A unique name for the vector store within the account"""

    dimensions: int
    """Dimension size of embedding vectors.

    Required when neither 'embedding_config' nor 'embedding_model' is set.
    Automatically derived when an embedding model is provided.
    """

    embedding_config: EmbeddingConfigParam
    """The embedding configuration.

    Either 'base' type with an embedding_model, or 'models_api' type with a
    model_deployment_id for custom models.
    """

    embedding_model: EmbeddingModelName
    """The base embedding model to use.

    Shorthand for embedding_config with type 'base'. Provide either embedding_config
    or embedding_model, not both.
    """

    indexed_metadata_fields: Dict[str, Literal["string", "number", "boolean"]]
    """Dictionary mapping metadata field names to their types for efficient filtering.

    Only STRING, NUMBER, and BOOLEAN types can be indexed.
    """
