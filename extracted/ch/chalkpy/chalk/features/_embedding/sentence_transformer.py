from __future__ import annotations

import asyncio
import functools
from typing import TYPE_CHECKING, Optional, Sequence, Type

import pyarrow as pa

from chalk.features._embedding.embedding_provider import EmbeddingProvider
from chalk.features._embedding.utils import ModelSpecs, create_fixedsize_with_nulls
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer
else:
    SentenceTransformer = None


_MAX_BATCH_SIZE = 2048
_DEFAULT_TASK_TYPE = "SEMANTIC_SIMILARITY"
_MODEL_SPECS = {
    "all-MiniLM-L6-v2": ModelSpecs(
        default_dimensions=384,
        validate_dimensions=lambda dim: dim == 384,
        validation_message="Must be 384.",
    ),
}


class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self, model: str, dimensions: Optional[int] = None) -> None:
        super().__init__()

        try:
            global SentenceTransformer
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise missing_dependency_exception("chalkpy[sentence-transformers]")

        if model not in _MODEL_SPECS:
            supported_models_str = ", ".join(f"'{model}'" for model in _MODEL_SPECS)
            raise ValueError(
                f"Unsupported model '{model}' for SentenceTransformer. The supported models are [{supported_models_str}]."
            )
        specs = _MODEL_SPECS[model]
        if dimensions is not None and not specs.validate_dimensions(dimensions):
            raise ValueError(f"Unsupported dimensions '{dimensions}' for model '{model}'. {specs.validation_message}")
        self.model = model
        self.dimensions = dimensions if dimensions is not None else specs.default_dimensions

    @functools.cached_property
    def _model(self):
        assert SentenceTransformer
        return SentenceTransformer(self.model)

    def get_provider_name(self) -> str:
        return "sentence-transformers"

    def get_model_name(self) -> str:
        return self.model

    def validate_input_schema(self, input_schema: Sequence[pa.DataType]) -> str | None:
        if len(input_schema) != 1:
            return f"SentenceTransformer emeddings support only 1 input, but got {len(input_schema)} inputs"
        if input_schema[0] != pa.large_utf8():
            return f"SentenceTransformer embeddings require a large_utf8() feature, but got a feature of type {input_schema[0]}"

    def generate_embedding(self, input: pa.Table) -> pa.FixedSizeListArray:
        raise NotImplementedError("use async_generate_embedding instead")

    async def async_generate_embedding(self, input: pa.Table):
        assert SentenceTransformer
        inputs: list[str | None] = input.column(0).to_pylist()

        for i in range(0, len(inputs), _MAX_BATCH_SIZE):
            chunked_input = inputs[i : i + _MAX_BATCH_SIZE]
            non_null_chunked_input: list[str] = []
            none_indices: set[int] = set()
            for idx, inp in enumerate(chunked_input):
                if inp is None or inp == "":
                    none_indices.add(idx)
                else:
                    non_null_chunked_input.append(inp)
            try:
                if len(non_null_chunked_input) > 0:
                    response = await asyncio.get_event_loop().run_in_executor(
                        None, lambda: list(self._model.encode(non_null_chunked_input, batch_size=_MAX_BATCH_SIZE))
                    )
                else:
                    response = []
            except Exception as e:
                try:
                    distinct_types = {type(e) for e in inputs}
                except Exception:
                    distinct_types = None
                raise ValueError(
                    f"Failed to generate embeddings for inputs of length {len(inputs)}. "
                    + f"Found distinct types {distinct_types}. Error: {e}"
                ) from e

            values_with_nulls: list[Sequence[float] | None] = []
            response_position = 0
            for idx in range(len(chunked_input)):
                if idx in none_indices:
                    values_with_nulls.append(None)
                elif response_position < len(response):
                    values_with_nulls.append(response[response_position])
                    response_position += 1
                else:
                    raise ValueError(
                        f"Expected to find an embedding for input at position {idx}, but the response data was exhausted."
                    )
            yield create_fixedsize_with_nulls(response, self.dimensions)

    def get_vector_class(self) -> Type[Vector]:
        return Vector[self.dimensions]
