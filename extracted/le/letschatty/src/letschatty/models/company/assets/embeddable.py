"""Embedding-chunks contract for assets.

Assets that can drive retrieval (contexts, products, tags, fast-answers, etc.)
implement ``embedding_chunks()`` to emit the text pieces we want embedded and
matched against an incoming chat query.

Each chunk is ``{"name": "<prefix>_<field>", "phrase": "<text>"}`` so a single
asset can expose multiple independent embedding surfaces (e.g. a product's
name vs. its description). Return an empty list when the asset has nothing
embeddable — downstream consumers (asset-embedding-worker) treat that as
"skip, no system triggers for this asset".

Keep this file dependency-light: import only stdlib and pydantic. Models that
import this must remain importable in the worker's runtime.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class EmbeddableAsset(Protocol):
    """Asset whose text content can be chunked for embedding."""

    def embedding_chunks(self) -> list[dict[str, str]]: ...


def build_chunks(prefix: str, fields: dict[str, Any]) -> list[dict[str, str]]:
    """Build ``[{name, phrase}]`` chunks, skipping empty/whitespace-only values.

    Args:
        prefix: Chunk-name prefix (e.g. ``"product"``, ``"context"``). Final
            chunk name becomes ``f"{prefix}_{field_key}"``.
        fields: Mapping of field-key → raw value. Non-string values are
            stringified; ``None`` / empty / whitespace values are dropped.
    """
    chunks: list[dict[str, str]] = []
    for key, value in fields.items():
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        chunks.append({"name": f"{prefix}_{key}", "phrase": text})
    return chunks
