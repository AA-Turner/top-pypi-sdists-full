# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["EmbeddingConfigModelsAPIParam"]


class EmbeddingConfigModelsAPIParam(TypedDict, total=False):
    model_deployment_id: Required[str]
    """The ID of the deployment of the created model in the Models API V3."""

    type: Required[Literal["models_api"]]
    """The type of the embedding configuration."""
