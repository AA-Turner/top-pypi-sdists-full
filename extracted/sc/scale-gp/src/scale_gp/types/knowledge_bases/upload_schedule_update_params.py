# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from ..token_chunking_strategy_config_param import TokenChunkingStrategyConfigParam
from ..custom_chunking_strategy_config_param import CustomChunkingStrategyConfigParam
from ..character_chunking_strategy_config_param import CharacterChunkingStrategyConfigParam

__all__ = [
    "UploadScheduleUpdateParams",
    "ChunkingStrategyConfig",
    "ChunkingStrategyConfigPreChunkedStrategyConfig",
    "ChunkingStrategyConfigEnhancedChunkingStrategyConfig",
]


class UploadScheduleUpdateParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    chunking_strategy_config: ChunkingStrategyConfig
    """Only compliant with the .chunks file type"""

    interval: float

    next_run_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]


class ChunkingStrategyConfigPreChunkedStrategyConfig(TypedDict, total=False):
    """Only compliant with the .chunks file type"""

    strategy: Required[Literal["pre_chunked"]]


class ChunkingStrategyConfigEnhancedChunkingStrategyConfig(TypedDict, total=False):
    """Enhanced document parsing and chunking"""

    advanced_options: Dict[str, object]
    """Advanced options for enhanced parsing"""

    chunk_mode: Literal["variable", "section", "page", "page_sections", "block"]
    """Enhanced internal chunking method"""

    experimental_options: Dict[str, object]
    """Experimental options for enhanced parsing"""

    options: Dict[str, object]
    """Options for enhanced parsing"""

    strategy: Literal["enhanced"]

    use_async_parsing: bool


ChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam,
    TokenChunkingStrategyConfigParam,
    CustomChunkingStrategyConfigParam,
    ChunkingStrategyConfigPreChunkedStrategyConfig,
    ChunkingStrategyConfigEnhancedChunkingStrategyConfig,
]
