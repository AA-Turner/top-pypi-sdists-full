# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V1, ConfigDict
from .._models import BaseModel
from .knowledge_base_data_source import KnowledgeBaseDataSource

__all__ = [
    "KnowledgeBase",
    "EmbeddingConfig",
    "EmbeddingConfigEmbeddingConfigModelsAPI",
    "EmbeddingConfigEmbeddingConfigBase",
    "ArtifactsStatus",
    "Connection",
]


class EmbeddingConfigEmbeddingConfigModelsAPI(BaseModel):
    model_deployment_id: str
    """The ID of the deployment of the created model in the Models API V3."""

    type: Literal["models_api"]
    """The type of the embedding configuration."""

    if not PYDANTIC_V1:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())


class EmbeddingConfigEmbeddingConfigBase(BaseModel):
    embedding_model: Literal[
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
    """The name of the base embedding model to use.

    To use custom models, change to type 'models'.
    """

    type: Optional[Literal["base"]] = None
    """The type of the embedding configuration."""


EmbeddingConfig: TypeAlias = Union[EmbeddingConfigEmbeddingConfigModelsAPI, EmbeddingConfigEmbeddingConfigBase]


class ArtifactsStatus(BaseModel):
    """
    Number of artifacts in each of the various states, such as completed and failed for this knowledge base. This includes all data sources.
    """

    artifacts_chunking: int
    """Number of artifacts in the chunking state"""

    artifacts_completed: int
    """Number of artifacts uploaded successfully."""

    artifacts_embedding: int
    """Number of artifacts in the embedding state"""

    artifacts_failed: int
    """Number of artifacts that failed while being processed."""

    artifacts_pending: int
    """Previously: Number of artifacts awaiting upload.

    Note that this status will be deprecated soon and should show 0
    """

    artifacts_uploading: int
    """Number of artifacts with upload in progress."""


class Connection(BaseModel):
    knowledge_base_data_source: KnowledgeBaseDataSource
    """The knowledge base data source entity."""

    last_uploaded_at: datetime
    """The date and time when the last upload for the data source was initiated."""

    deletion_status: Optional[Literal["DELETING", "FAILED"]] = None
    """The status of the deletion job for this data source connection, if any."""


class KnowledgeBase(BaseModel):
    created_at: str
    """The timestamp at which the knowledge base was created"""

    embedding_config: EmbeddingConfig
    """The embedding configuration"""

    knowledge_base_id: str
    """The unique ID of the knowledge base"""

    knowledge_base_name: str
    """The name of the knowledge base"""

    vector_store_id: str
    """(Legacy) The unique ID of the underlying vector store.

    This is to allow for backwards compatibility with the V1 Vector Store APIs. This
    will be removed in the near future.
    """

    artifact_count: Optional[int] = None
    """The total number of artifacts in the knowledge base.

    Only returned with the `view=ArtifactCount` query parameter.
    """

    artifacts_status: Optional[ArtifactsStatus] = None
    """
    Number of artifacts in each of the various states, such as completed and failed
    for this knowledge base. This includes all data sources.
    """

    cluster_status: Optional[str] = None
    """Whether the knowledge base has been clustered."""

    connections: Optional[List[Connection]] = None
    """The data source connections associated with the knowledge base.

    Only returned with the `view=Connections` query parameter.
    """

    created_by_user_id: Optional[str] = None
    """The user ID of the user who created the knowledge base."""

    metadata: Optional[Dict[str, object]] = None
    """Metadata associated with the knowledge base"""

    updated_at: Optional[str] = None
    """The timestamp at which the knowledge base was last updated"""
