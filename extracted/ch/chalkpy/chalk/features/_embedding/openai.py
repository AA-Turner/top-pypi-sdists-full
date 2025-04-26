from __future__ import annotations

import functools
from typing import Optional, Sequence, Type

import pyarrow as pa

from chalk.features._embedding.embedding_provider import EmbeddingProvider
from chalk.features._embedding.utils import ModelSpecs, create_fixedsize_with_nulls
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import openai
    import tiktoken
except ImportError:
    openai = None
    tiktoken = None


_MAX_INPUT_TOKENS = 8191
_MAX_BATCH_SIZE = 2048
_MODEL_SPECS = {
    "text-embedding-ada-002": ModelSpecs(
        default_dimensions=1536,
        validate_dimensions=lambda dim: dim == 1536,
        validation_message="Must be 1536.",
        requires_none_input=True,
    ),
    "text-embedding-3-small": ModelSpecs(
        default_dimensions=1536,
        validate_dimensions=lambda dim: 1 <= dim <= 1536,
        validation_message="Must be between 1 and 768 (inclusive).",
    ),
    "text-embedding-3-large": ModelSpecs(
        default_dimensions=3072,
        validate_dimensions=lambda dim: 1 <= dim <= 3072,
        validation_message="Must be between 1 and 3072 (inclusive).",
    ),
}


class OpenAIProvider(EmbeddingProvider):
    def __init__(self, model: str, dimensions: Optional[int] = None) -> None:
        super().__init__()
        if not openai or not tiktoken:
            raise missing_dependency_exception("chalkpy[openai]")
        if model not in _MODEL_SPECS:
            models_str = ", ".join(f"'{model}'" for model in _MODEL_SPECS)
            raise ValueError(f"Unsupported model '{model}' for OpenAI. The supported models are [{models_str}].")
        specs = _MODEL_SPECS[model]
        if dimensions is not None and not specs.validate_dimensions(dimensions):
            raise ValueError(f"Unsupported dimensions '{dimensions}' for model '{model}'. {specs.validation_message}")
        self.model = model
        self.input_dimensions = None if specs.requires_none_input else dimensions
        self.output_dimensions = dimensions if dimensions is not None else specs.default_dimensions

    @functools.cached_property
    def _async_client(self):
        assert openai
        return openai.AsyncOpenAI()

    @functools.cached_property
    def _encoding(self):
        assert tiktoken is not None, "Verified tiktoken is available in init"
        try:
            return tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Use cl100k_base encoding by default
            return tiktoken.get_encoding("cl100k_base")

    def get_provider_name(self) -> str:
        return "openai"

    def get_model_name(self) -> str:
        return self.model

    def validate_input_schema(self, input_schema: Sequence[pa.DataType]) -> str | None:
        if len(input_schema) != 1:
            return f"OpenAI emeddings support only 1 input, but got {len(input_schema)} inputs"
        if input_schema[0] != pa.large_utf8():
            return f"OpenAI embeddings require a large_utf8() feature, but got a feature of type {input_schema[0]}"

    def _truncate_embedding_input(self, inp: str | None) -> str | None:
        if inp is None:
            return None
        if inp == "":
            return None
        input_tokens = self._encoding.encode(inp, allowed_special="all")
        if len(input_tokens) > _MAX_INPUT_TOKENS:
            return self._encoding.decode(input_tokens[:_MAX_INPUT_TOKENS])
        return inp

    def generate_embedding(self, input: pa.Table) -> pa.FixedSizeListArray:
        raise NotImplementedError("use async_generate_embedding instead")

    async def async_generate_embedding(self, input: pa.Table):
        assert openai
        inputs: list[str | None] = [self._truncate_embedding_input(i) for i in input.column(0).to_pylist()]
        # Step over `input` in chunks of MAX_BATCH_SIZE; the max openai array length
        for i in range(0, len(inputs), _MAX_BATCH_SIZE):
            chunked_input = inputs[i : i + _MAX_BATCH_SIZE]
            non_null_chunked_input: list[str] = []
            none_indices: set[int] = set()
            for idx, inp in enumerate(chunked_input):
                if inp is None:
                    none_indices.add(idx)
                else:
                    non_null_chunked_input.append(inp)
            try:
                if len(non_null_chunked_input) > 0:
                    if self.input_dimensions is not None:
                        response = await self._async_client.embeddings.create(
                            input=non_null_chunked_input, model=self.model, dimensions=self.input_dimensions
                        )
                    else:
                        response = await self._async_client.embeddings.create(
                            input=non_null_chunked_input, model=self.model
                        )
                    response_data = response.data
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
                    values_with_nulls.append(response_data[response_position].embedding)
                    response_position += 1
                else:
                    raise ValueError(
                        f"Expected to find an embedding for input at position {idx}, but the response data was exhausted."
                    )
            yield create_fixedsize_with_nulls(values_with_nulls, self.output_dimensions)

    def get_vector_class(self) -> Type[Vector]:
        return Vector[self.output_dimensions]
