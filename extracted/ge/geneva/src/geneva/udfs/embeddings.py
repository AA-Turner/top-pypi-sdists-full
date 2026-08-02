# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Compatibility shim for ``geneva.udfs.embeddings``."""

from geneva.udfs.text.embeddings import (
    DEFAULT_GEMINI_EMBEDDING_MODEL,
    DEFAULT_SENTENCE_TRANSFORMER_COLUMN,
    DEFAULT_SENTENCE_TRANSFORMER_MODEL,
    GEMINI_EMBEDDING_FAMILY,
    KNOWN_GEMINI_EMBEDDING_MODELS,
    SENTENCE_TRANSFORMERS_FAMILY,
    _build_embedding_udf,
    _EmbeddingModel,
    _extract_string_inputs,
    _gemini_retry,
    _GeminiEmbeddingModel,
    _resolve_device,
    _SentenceTransformersModel,
    gemini_embedding_udf,
    sentence_transformer_udf,
)

__all__ = [
    "DEFAULT_GEMINI_EMBEDDING_MODEL",
    "DEFAULT_SENTENCE_TRANSFORMER_COLUMN",
    "DEFAULT_SENTENCE_TRANSFORMER_MODEL",
    "GEMINI_EMBEDDING_FAMILY",
    "KNOWN_GEMINI_EMBEDDING_MODELS",
    "SENTENCE_TRANSFORMERS_FAMILY",
    "gemini_embedding_udf",
    "sentence_transformer_udf",
    "_GeminiEmbeddingModel",
    "_EmbeddingModel",
    "_SentenceTransformersModel",
    "_build_embedding_udf",
    "_extract_string_inputs",
    "_gemini_retry",
    "_resolve_device",
]
