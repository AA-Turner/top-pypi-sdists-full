from __future__ import annotations

import typing
from typing import Protocol, Sequence, Type

import pyarrow as pa

from chalk.features._vector import Vector


class EmbeddingProvider(Protocol):
    def get_provider_name(self) -> str:
        """Get the name for the embedding provider (i.e. OpenAI)"""
        ...

    def get_model_name(self) -> str:
        """Get the name of the embedding model"""
        ...

    def validate_input_schema(self, input_schema: Sequence[pa.DataType]) -> str | None:
        """Validate that this embedding provider can accept this input schema. It should return None if successful, or a string
        of an error message if the schema is not supported. The inputs table to future `generate_embedding` calls will have columns
        in the same order as this input_schema"""
        ...

    def generate_embedding(self, input: pa.Table) -> pa.FixedSizeListArray:
        """Generate embeddings from the input table. The input table will contain all string columns.
        The embedding implementation should have a well defined order for which column index is for the the feature that will be embedded, and which
        additional columns are for metadata (such as the prompt, with instructor)"""
        ...

    def async_generate_embedding(self, input: pa.Table) -> typing.AsyncGenerator[pa.FixedSizeListArray, None]:
        """Generate embeddings from the input table. The input table will contain all string columns.
        The embedding implementation should have a well defined order for which column index is for the the feature that will be embedded, and which
        additional columns are for metadata (such as the prompt, with instructor)"""
        ...

    def get_vector_class(self) -> Type[Vector]:
        """Get the expected output class, with the vector dimensions and dtype"""
        ...
