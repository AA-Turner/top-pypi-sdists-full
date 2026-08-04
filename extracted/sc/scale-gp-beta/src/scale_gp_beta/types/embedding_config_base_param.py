# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

from .embedding_model_name import EmbeddingModelName

__all__ = ["EmbeddingConfigBaseParam"]


class EmbeddingConfigBaseParam(TypedDict, total=False):
    embedding_model: Required[Union[EmbeddingModelName, str]]
    """The name of the base embedding model to use.

    Either a known base model (EmbeddingModelName) or, in ray-serve deployments with
    NATIVE_OPENAI_EMBEDDING_GATEWAY enabled, any model id served by the
    OpenAI-compatible inference proxy (e.g. 'nomic-embed-text-v1.5'). For fully
    custom deployments, use type 'models_api' with a model_deployment_id.
    """

    type: Literal["base"]
    """The type of the embedding configuration."""
