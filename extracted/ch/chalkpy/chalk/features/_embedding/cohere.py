from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence, Type

import numpy as np
import pyarrow as pa

from chalk.features._embedding.embedding_provider import EmbeddingProvider
from chalk.features._embedding.utils import ModelSpecs
from chalk.features._vector import Vector
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import cohere
else:
    cohere = None

_MODEL_SPECS = {
    "embed-english-v3.0": ModelSpecs(
        default_dimensions=1024,
        validate_dimensions=lambda dim: dim == 1024,
        validation_message="Must be 1024.",
        requires_none_input=True,
    ),
    "embed-multilingual-v3.0": ModelSpecs(
        default_dimensions=1024,
        validate_dimensions=lambda dim: dim == 1024,
        validation_message="Must be 1024.",
        requires_none_input=True,
    ),
    "embed-english-light-v3.0": ModelSpecs(
        default_dimensions=384,
        validate_dimensions=lambda dim: dim == 384,
        validation_message="Must be 384.",
        requires_none_input=True,
    ),
    "embed-multilingual-light-v3.0": ModelSpecs(
        default_dimensions=384,
        validate_dimensions=lambda dim: dim == 384,
        validation_message="Must be 384.",
        requires_none_input=True,
    ),
}


class CohereProvider(EmbeddingProvider):
    def __init__(self, model: str, dimensions: Optional[int] = None) -> None:
        super().__init__()
        try:
            global cohere
            import cohere
        except ImportError:
            raise missing_dependency_exception("chalkpy[cohere]")

        if model not in _MODEL_SPECS:
            supported_models_str = ", ".join(f"'{model}'" for model in _MODEL_SPECS)
            raise ValueError(
                f"Unsupported model '{model}' for Cohere. The supported models are [{supported_models_str}]."
            )
        specs = _MODEL_SPECS[model]
        if dimensions is not None and not specs.validate_dimensions(dimensions):
            raise ValueError(f"Unsupported dimensions '{dimensions}' for model '{model}'. {specs.validation_message}")
        self.model = model
        self.dimensions = dimensions if dimensions is not None else specs.default_dimensions

    def get_provider_name(self) -> str:
        return "Cohere"

    def get_model_name(self) -> str:
        return self.model

    def validate_input_schema(self, input_schema: Sequence[pa.DataType]) -> str | None:
        # Cohere requires two columns -- the data and the input type
        # For now not validating but will do so later
        return

    async def async_generate_embedding(self, input: pa.Table):
        co = cohere.AsyncClient()
        text_input: list[str] = input.column(0).to_pylist()
        response = await co.embed(texts=text_input, model=self.model, input_type="search_document")
        vectors = np.array(
            response.embeddings, dtype=np.dtype(self.get_vector_class().precision.replace("fp", "float"))
        )
        yield pa.FixedSizeListArray.from_arrays(vectors.reshape(-1), self.dimensions)

    def generate_embedding(self, input: pa.Table) -> pa.FixedSizeListArray:
        co = cohere.Client()
        text_input: list[str] = input.column(0).to_pylist()
        response = co.embed(texts=text_input, model=self.model, input_type="search_document")
        vectors = np.array(
            response.embeddings, dtype=np.dtype(self.get_vector_class().precision.replace("fp", "float"))
        )
        return pa.FixedSizeListArray.from_arrays(vectors.reshape(-1), self.dimensions)

    def get_vector_class(self) -> Type[Vector]:
        return Vector[self.dimensions]
