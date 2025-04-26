from __future__ import annotations

from enum import Enum
from typing import List

import attrs

from tecton_core import schema
from tecton_core.embeddings import model_artifact_info


class TextEmbeddingModel(str, Enum):
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"
    MXBAI_EMBED_LARGE_v1 = "mixedbread-ai/mxbai-embed-large-v1"
    BGE_LARGE_EN_v1_5 = "BAAI/bge-large-en-v1.5"
    BGE_BASE_EN_v1_5 = "BAAI/bge-base-en-v1.5"
    BGE_SMALL_EN_v1_5 = "BAAI/bge-small-en-v1.5"
    GTE_LARGE = "thenlper/gte-large"
    GTE_BASE = "thenlper/gte-base"
    GTE_GTE_SMALL = "thenlper/gte-small"
    SNOWFLAKE_ARCTIC_EMBED_XS = "Snowflake/snowflake-arctic-embed-xs"
    SNOWFLAKE_ARCTIC_EMBED_S = "Snowflake/snowflake-arctic-embed-s"
    SNOWFLAKE_ARCTIC_EMBED_M = "Snowflake/snowflake-arctic-embed-m"
    SNOWFLAKE_ARCTIC_EMBED_L = "Snowflake/snowflake-arctic-embed-l"
    E5_LARGE_UNSUPERVISED = "intfloat/e5-large-unsupervised"
    E5_BASE_UNSUPERVISED = "intfloat/e5-base-unsupervised"
    E5_SMALL_UNSUPERVISED = "intfloat/e5-small-unsupervised"


class BaseInferenceConfig:
    pass


@attrs.frozen
class TextEmbeddingInferenceConfig(BaseInferenceConfig):
    input_column: str
    output_column: str
    model: TextEmbeddingModel


# TODO(jiadong): Consolidate TextEmbeddingInferenceConfig and this config and migrate pre-trained models to use it.
@attrs.frozen
class CustomModelConfig(BaseInferenceConfig):
    input_columns: List[schema.Column]
    output_column: schema.Column
    model_artifact: model_artifact_info.ModelArtifactInfo
