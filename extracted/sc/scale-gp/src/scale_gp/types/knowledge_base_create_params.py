# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "KnowledgeBaseCreateParams",
    "EmbeddingConfig",
    "EmbeddingConfigEmbeddingConfigModelsAPI",
    "EmbeddingConfigEmbeddingConfigBase",
    "KBIndexConfiguration",
]


class KnowledgeBaseCreateParams(TypedDict, total=False):
    embedding_config: Required[EmbeddingConfig]
    """The configuration of the embedding"""

    knowledge_base_name: Required[str]
    """A unique name for the knowledge base"""

    account_id: str
    """Account to create knowledge base in.

    If you have access to more than one account, you must specify an account_id
    """

    kb_index_configuration: KBIndexConfiguration
    """
    Configuration for metadata schema in the knowledge base, including field
    definitions and index settings
    """

    metadata: Dict[str, object]
    """Metadata associated with the knowledge base"""


class EmbeddingConfigEmbeddingConfigModelsAPI(TypedDict, total=False):
    model_deployment_id: Required[str]
    """The ID of the deployment of the created model in the Models API V3."""

    type: Required[Literal["models_api"]]
    """The type of the embedding configuration."""


class EmbeddingConfigEmbeddingConfigBase(TypedDict, total=False):
    embedding_model: Required[
        Literal[
            "sentence-transformers/all-MiniLM-L12-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/multi-qa-distilbert-cos-v1",
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            "openai/text-embedding-ada-002",
            "openai/text-embedding-3-small",
            "openai/text-embedding-3-large",
            "embed-english-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-v3.0",
            "gemini/text-embedding-005",
            "gemini/text-multilingual-embedding-002",
            "gemini/gemini-embedding-001",
        ]
    ]
    """The name of the base embedding model to use.

    To use custom models, change to type 'models'.
    """

    type: Literal["base"]
    """The type of the embedding configuration."""


EmbeddingConfig: TypeAlias = Union[EmbeddingConfigEmbeddingConfigModelsAPI, EmbeddingConfigEmbeddingConfigBase]


class KBIndexConfiguration(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """
    Configuration for metadata schema in the knowledge base, including field definitions and index settings
    """

    fields: Required[Dict[str, object]]
    """Schema defining metadata fields for the knowledge base.

    Each field can have properties: type (string, int32, int64, double, boolean,
    complex), filterable (bool), searchable (bool). Complex types can have nested
    'fields' with the same structure.
    """

    max_index_size: int
    """Maximum size (in bytes) for the index. If not provided, uses the default."""
