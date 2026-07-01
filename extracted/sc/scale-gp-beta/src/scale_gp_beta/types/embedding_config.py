# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .embedding_config_base import EmbeddingConfigBase
from .embedding_config_models_api import EmbeddingConfigModelsAPI

__all__ = ["EmbeddingConfig"]

EmbeddingConfig: TypeAlias = Union[EmbeddingConfigModelsAPI, EmbeddingConfigBase]
