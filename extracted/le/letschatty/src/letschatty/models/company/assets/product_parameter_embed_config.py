from enum import StrEnum
from pydantic import BaseModel, Field


class ProductParameterEmbedFormat(StrEnum):
    """How a product parameter is stringified into a trigger phrase."""

    KEY_VALUE = "key_value"    # "engine: 1.6 turbo"
    VALUE_ONLY = "value_only"  # "1.6 turbo"


class ProductParameterEmbedEntry(BaseModel):
    """Single allow-list entry: which key to embed and how to format it."""

    key: str = Field(min_length=1, max_length=64)
    format: ProductParameterEmbedFormat = ProductParameterEmbedFormat.KEY_VALUE
    split_by_comma: bool = False


class ProductParameterEmbedConfig(BaseModel):
    """Per-company allow-list controlling which product parameters get embedded.

    Passed into ``Product.embedding_chunks(parameter_config=...)`` so the model
    stays ignorant of where the config is stored.
    """

    entries: list[ProductParameterEmbedEntry] = Field(default_factory=list)
