# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

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
    "KBIndexConfiguration",
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


class KBIndexConfiguration(BaseModel):
    """
    The effective metadata schema enforced on this knowledge base's underlying index, including system defaults (`page`, `artifact_uri_public`, `artifact_name`). Populated for Azure AI Search backends; `null` for schemaless backends (OpenSearch, Vertex AI). Only returned when the caller opts in via `view=IndexConfiguration` on both the GET and list endpoints.
    """

    fields: Dict[str, object]
    """Schema defining metadata fields for the knowledge base.

    Each field can have properties: type (string, int32, int64, double, boolean,
    complex), filterable (bool), searchable (bool). Complex types can have nested
    'fields' with the same structure.
    """

    max_index_size: Optional[int] = None
    """Maximum size (in bytes) for the index. If not provided, uses the default."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


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

    index_backend: Optional[Literal["AzureSearch", "OpenSearch", "Redis", "VertexAISearch"]] = None
    """The underlying search backend powering this knowledge base."""

    kb_index_configuration: Optional[KBIndexConfiguration] = None
    """
    The effective metadata schema enforced on this knowledge base's underlying
    index, including system defaults (`page`, `artifact_uri_public`,
    `artifact_name`). Populated for Azure AI Search backends; `null` for schemaless
    backends (OpenSearch, Vertex AI). Only returned when the caller opts in via
    `view=IndexConfiguration` on both the GET and list endpoints.
    """

    metadata: Optional[Dict[str, object]] = None
    """Metadata associated with the knowledge base"""

    updated_at: Optional[str] = None
    """The timestamp at which the knowledge base was last updated"""
