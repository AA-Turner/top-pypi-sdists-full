from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Optional, Sequence, Type

import pyarrow as pa

from chalk.features._embedding.embedding_provider import EmbeddingProvider
from chalk.features._embedding.utils import ModelSpecs, create_fixedsize_with_nulls
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
else:
    TextEmbeddingInput = None
    TextEmbeddingModel = None


_MAX_BATCH_SIZE = 5
_DEFAULT_TASK_TYPE = "SEMANTIC_SIMILARITY"
_MODEL_SPECS = {
    "text-embedding-004": ModelSpecs(
        default_dimensions=768,
        validate_dimensions=lambda dim: 1 <= dim <= 768,
        validation_message="Must be between 1 and 768 (inclusive).",
    ),
    "text-embedding-005": ModelSpecs(
        default_dimensions=768,
        validate_dimensions=lambda dim: 1 <= dim <= 768,
        validation_message="Must be between 1 and 768 (inclusive).",
    ),
    "text-multilingual-embedding-002": ModelSpecs(
        default_dimensions=768,
        validate_dimensions=lambda dim: 1 <= dim <= 768,
        validation_message="Must be between 1 and 768 (inclusive).",
    ),
}


class VertexAIProvider(EmbeddingProvider):
    def __init__(self, model: str, dimensions: Optional[int] = None) -> None:
        super().__init__()

        try:
            global TextEmbeddingInput, TextEmbeddingModel
            from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
        except ImportError:
            raise missing_dependency_exception("chalkpy[vertexai]")

        if model not in _MODEL_SPECS:
            supported_models_str = ", ".join(f"'{model}'" for model in _MODEL_SPECS)
            raise ValueError(
                f"Unsupported model '{model}' for VertexAI. The supported models are [{supported_models_str}]."
            )
        specs = _MODEL_SPECS[model]
        if dimensions is not None and not specs.validate_dimensions(dimensions):
            raise ValueError(f"Unsupported dimensions '{dimensions}' for model '{model}'. {specs.validation_message}")
        self.model = model
        self.dimensions = dimensions if dimensions is not None else specs.default_dimensions

    @functools.cached_property
    def _model(self):
        assert TextEmbeddingModel
        return TextEmbeddingModel.from_pretrained(self.model)

    def get_provider_name(self) -> str:
        return "vertexai"

    def get_model_name(self) -> str:
        return self.model

    def validate_input_schema(self, input_schema: Sequence[pa.DataType]) -> str | None:
        if len(input_schema) != 1:
            return f"VertexAI emeddings support only 1 input, but got {len(input_schema)} inputs"
        if input_schema[0] != pa.large_utf8():
            return f"VertexAI embeddings require a large_utf8() feature, but got a feature of type {input_schema[0]}"

    def generate_embedding(self, input: pa.Table) -> pa.FixedSizeListArray:
        raise NotImplementedError("use async_generate_embedding instead")

    async def async_generate_embedding(self, input: pa.Table):
        assert TextEmbeddingInput
        inputs: list[str | None] = input.column(0).to_pylist()
        # Step over `input` in chunks of MAX_BATCH_SIZE; the max vertexai array length
        for i in range(0, len(inputs), _MAX_BATCH_SIZE):
            chunked_input = inputs[i : i + _MAX_BATCH_SIZE]
            non_null_chunked_input: list[str | TextEmbeddingInput] = []
            none_indices: set[int] = set()
            for idx, inp in enumerate(chunked_input):
                if inp is None or inp == "":
                    none_indices.add(idx)
                else:
                    non_null_chunked_input.append(TextEmbeddingInput(inp, _DEFAULT_TASK_TYPE))
            try:
                if len(non_null_chunked_input) > 0:
                    response_data = await self._model.get_embeddings_async(
                        non_null_chunked_input, output_dimensionality=self.dimensions, auto_truncate=True
                    )
                else:
                    response_data = []
            except Exception as e:
                try:
                    distinct_types = {type(e) for e in chunked_input}
                except Exception:
                    distinct_types = None
                raise ValueError(
                    f"Failed to generate embeddings for inputs of length {len(chunked_input)}. "
                    + f"Found distinct types {distinct_types}. Error: {e}"
                ) from e
            values_with_nulls: list[Sequence[float] | None] = []
            response_position = 0
            for idx in range(len(chunked_input)):
                if idx in none_indices:
                    values_with_nulls.append(None)
                elif response_position < len(response_data):
                    values_with_nulls.append(response_data[response_position].values)
                    response_position += 1
                else:
                    raise ValueError(
                        f"Expected to find an embedding for input at position {idx}, but the response data was exhausted."
                    )
            yield create_fixedsize_with_nulls(values_with_nulls, self.dimensions)

    def get_vector_class(self) -> Type[Vector]:
        return Vector[self.dimensions]
