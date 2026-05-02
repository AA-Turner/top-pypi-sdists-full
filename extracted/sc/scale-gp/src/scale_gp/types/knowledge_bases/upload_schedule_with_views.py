# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..knowledge_base_data_source import KnowledgeBaseDataSource
from ..token_chunking_strategy_config import TokenChunkingStrategyConfig
from ..custom_chunking_strategy_config import CustomChunkingStrategyConfig
from ..character_chunking_strategy_config import CharacterChunkingStrategyConfig

__all__ = [
    "UploadScheduleWithViews",
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


class UploadScheduleWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    chunking_strategy_config: ChunkingStrategyConfig
    """Only compliant with the .chunks file type"""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    interval: float

    knowledge_base_data_source_id: str

    knowledge_base_id: str

    status: Literal["HEALTHY", "UNHEALTHY", "ERROR", "PAUSED"]

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    knowledge_base_data_source: Optional[KnowledgeBaseDataSource] = None

    next_run_at: Optional[datetime] = None

    status_reason: Optional[str] = None
