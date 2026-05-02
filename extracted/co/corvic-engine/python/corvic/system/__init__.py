"""Protocols defining the way corvic interacts with the platform."""

from typing import Final

from corvic.system._dimension_reduction import (
    DimensionReducer,
    TruncateDimensionReducer,
    UmapDimensionReducer,
)
from corvic.system._embedder import (
    EmbedImageContext,
    EmbedImageResult,
    EmbedTextContext,
    EmbedTextResult,
    ImageEmbedder,
    TextEmbedder,
)
from corvic.system._image_embedder import (
    Clip,
    CombinedImageEmbedder,
    RandomImageEmbedder,
    image_from_bytes,
)
from corvic.system._planner import OpGraphPlanner, ValidateFirstExecutor
from corvic.system._text_embedder import RandomTextEmbedder
from corvic.system.client import Client
from corvic.system.in_memory_executor import (
    InMemoryExecutionResult,
    InMemoryExecutor,
    batch_to_proto_struct,  # pyright: ignore[reportDeprecated]
    get_polars_embedding,
    get_polars_embedding_length,
    make_dict_bytes_human_readable,
    make_list_bytes_human_readable,
)
from corvic.system.op_graph_executor import (
    ExecutionContext,
    ExecutionResult,
    OpGraphExecutor,
    TableComputeContext,
    TableComputeResult,
    TableSliceArgs,
)
from corvic.system.staging import StagingDB, VectorSimilarityMetric
from corvic.system.storage import (
    Blob,
    BlobClient,
    Bucket,
    DataKindManager,
    DataMisplacedError,
    StorageManager,
)

DEFAULT_VECTOR_COLUMN_NAMES_TO_SIZES: Final = {
    "2_dim_vector": 2,
    "3_dim_vector": 3,
    "8_dim_vector": 8,
    "16_dim_vector": 16,
    "32_dim_vector": 32,
    "64_dim_vector": 64,
    "128_dim_vector": 128,
}

__all__ = [
    "Blob",
    "BlobClient",
    "Bucket",
    "Client",
    "Clip",
    "DEFAULT_VECTOR_COLUMN_NAMES_TO_SIZES",
    "DataKindManager",
    "DataMisplacedError",
    "DimensionReducer",
    "EmbedTextContext",
    "EmbedTextResult",
    "ExecutionContext",
    "ExecutionResult",
    "EmbedImageContext",
    "EmbedImageResult",
    "ImageEmbedder",
    "InMemoryExecutionResult",
    "InMemoryExecutor",
    "OpGraphExecutor",
    "OpGraphPlanner",
    "RandomImageEmbedder",
    "CombinedImageEmbedder",
    "RandomTextEmbedder",
    "StagingDB",
    "StorageManager",
    "TableComputeContext",
    "TableComputeResult",
    "TableSliceArgs",
    "TextEmbedder",
    "TruncateDimensionReducer",
    "UmapDimensionReducer",
    "ValidateFirstExecutor",
    "VectorSimilarityMetric",
    "batch_to_proto_struct",
    "get_polars_embedding",
    "get_polars_embedding_length",
    "make_dict_bytes_human_readable",
    "make_list_bytes_human_readable",
    "image_from_bytes",
]
