# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EmbeddingConfigModelsAPI"]


class EmbeddingConfigModelsAPI(BaseModel):
    deployment_id: str = FieldInfo(alias="model_deployment_id")
    """The ID of the deployment of the created model in the Models API V3."""

    type: Literal["models_api"]
    """The type of the embedding configuration."""
