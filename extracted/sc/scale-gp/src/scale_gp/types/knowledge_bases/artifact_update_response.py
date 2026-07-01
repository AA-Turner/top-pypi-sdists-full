# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..token_chunking_strategy_config import TokenChunkingStrategyConfig
from ..custom_chunking_strategy_config import CustomChunkingStrategyConfig
from ..character_chunking_strategy_config import CharacterChunkingStrategyConfig

__all__ = [
    "ArtifactUpdateResponse",
    "ChunkingStrategyConfig",
    "ChunkingStrategyConfigPreChunkedStrategyConfig",
    "ChunkingStrategyConfigEnhancedChunkingStrategyConfig",
]


class ChunkingStrategyConfigPreChunkedStrategyConfig(BaseModel):
    """Only compliant with the .chunks file type"""

    strategy: Literal["pre_chunked"]


class ChunkingStrategyConfigEnhancedChunkingStrategyConfig(BaseModel):
    """Enhanced document parsing and chunking"""

    advanced_options: Optional[Dict[str, object]] = None
    """Advanced options for enhanced parsing"""

    chunk_mode: Optional[Literal["variable", "section", "page", "page_sections", "block"]] = None
    """Enhanced internal chunking method"""

    experimental_options: Optional[Dict[str, object]] = None
    """Experimental options for enhanced parsing"""

    options: Optional[Dict[str, object]] = None
    """Options for enhanced parsing"""

    strategy: Optional[Literal["enhanced"]] = None

    use_async_parsing: Optional[bool] = None


ChunkingStrategyConfig: TypeAlias = Annotated[
    Union[
        CharacterChunkingStrategyConfig,
        TokenChunkingStrategyConfig,
        CustomChunkingStrategyConfig,
        ChunkingStrategyConfigPreChunkedStrategyConfig,
        ChunkingStrategyConfigEnhancedChunkingStrategyConfig,
    ],
    PropertyInfo(discriminator="strategy"),
]


class ArtifactUpdateResponse(BaseModel):
    artifact_name: str

    artifact_uri: str

    created_at: Union[str, datetime]

    knowledge_base_id: str

    source: Literal[
        "S3",
        "SharePoint",
        "SharePointPage",
        "LocalFile",
        "LocalChunks",
        "GoogleDrive",
        "AzureBlobStorage",
        "GoogleCloudStorage",
        "Confluence",
        "Slack",
        "Snowflake",
        "Databricks",
        "SQLDatabase",
        "MongoDB",
    ]

    status: Literal["Pending", "Chunking", "Uploading", "Completed", "Failed", "Deleting", "Canceled", "Embedding"]

    updated_at: Union[str, datetime]

    artifact_id: Optional[str] = None

    artifact_uri_public: Optional[str] = None

    checkpoint: Optional[
        Literal["Pending", "Chunking", "Uploading", "Completed", "Failed", "Deleting", "Canceled", "Embedding"]
    ] = None

    chunking_strategy_config: Optional[ChunkingStrategyConfig] = None
    """Only compliant with the .chunks file type"""

    content_modification_identifier: Optional[str] = None

    deleted_at: Union[str, datetime, None] = None

    status_reason: Optional[str] = None

    tags: Optional[Dict[str, object]] = None
