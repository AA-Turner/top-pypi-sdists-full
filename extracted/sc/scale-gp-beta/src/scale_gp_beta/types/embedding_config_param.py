# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .embedding_config_base_param import EmbeddingConfigBaseParam
from .embedding_config_models_api_param import EmbeddingConfigModelsAPIParam

__all__ = ["EmbeddingConfigParam"]

EmbeddingConfigParam: TypeAlias = Union[EmbeddingConfigModelsAPIParam, EmbeddingConfigBaseParam]
