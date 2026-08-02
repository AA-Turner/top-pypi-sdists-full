# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pre-built OpenAI embedding and generative-AI UDF helpers."""

import base64
import os
import warnings
from functools import cached_property
from typing import Any

import attrs
import pyarrow as pa

from geneva.debug.error_store import Retry
from geneva.transformer import UDF, udf
from geneva.udfs.text.embeddings import (
    _build_embedding_udf,
    _EmbeddingModel,
    _extract_string_inputs,
)

# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------


def _openai_retry() -> Retry:
    """Build a Retry for OpenAI API errors (lazy import)."""
    import openai

    return Retry(
        openai.RateLimitError,
        openai.APITimeoutError,
        openai.APIConnectionError,
        openai.InternalServerError,
        max_attempts=7,
        backoff="exponential",
    )


# ---------------------------------------------------------------------------
# Embedding UDF
# ---------------------------------------------------------------------------

OPENAI_EMBEDDING_FAMILY = "openai-embedding"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

KNOWN_OPENAI_EMBEDDING_MODELS: set[str] = {
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
}

# Default output dimensions for known OpenAI embedding models.
_OPENAI_EMBEDDING_DIMENSIONS: dict[str, int] = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}


@attrs.define
class _OpenAIEmbeddingModel(_EmbeddingModel):
    """OpenAI API-based embedding model.

    Carries its API key through serialization so that remote workers
    can use it without cluster-level ``env_vars`` configuration.

    Parameters
    ----------
    api_key:
        The OpenAI API key.  Hidden from ``repr`` to avoid leaking secrets.
    output_dimensionality:
        Optional reduced output dimensionality.  When set, the API returns
        truncated embeddings (only supported by ``text-embedding-3-*``
        models).
    """

    api_key: str = attrs.field(repr=False, kw_only=True)
    output_dimensionality: int | None = attrs.field(default=None, kw_only=True)

    def _build_model(self) -> Any:
        """Lazily create a per-instance OpenAI client on the worker."""
        import openai

        return openai.OpenAI(api_key=self.api_key)

    def _get_dimension(self) -> int:
        if self.output_dimensionality is not None:
            return self.output_dimensionality
        dim = _OPENAI_EMBEDDING_DIMENSIONS.get(self.model_name)
        if dim is not None:
            return dim
        # Unknown model — make a single probe call to discover the dimension.
        result = self.model.embeddings.create(
            input=["dimension probe"],
            model=self.model_name,
        )
        return len(result.data[0].embedding)

    def embed(self, batch: pa.RecordBatch) -> pa.Array:
        valid_texts, valid_indices, values = _extract_string_inputs(batch, self.column)

        outputs: list[list[float] | None] = [None] * len(values)
        if valid_texts:
            kwargs: dict[str, Any] = {
                "input": valid_texts,
                "model": self.model_name,
            }
            if self.output_dimensionality is not None:
                kwargs["dimensions"] = self.output_dimensionality
            result = self.model.embeddings.create(**kwargs)
            embeddings: list[list[float]] = [d.embedding for d in result.data]

            if self.normalize:
                import numpy as np

                arr = np.array(embeddings)
                norms = np.linalg.norm(arr, axis=1, keepdims=True)
                norms = np.where(norms > 0, norms, 1)
                embeddings = (arr / norms).tolist()

            for idx, vector in zip(valid_indices, embeddings, strict=False):
                outputs[idx] = vector

        return pa.array(outputs, type=self.output_type())


def openai_embedding_udf(
    column: str = "text",
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    output_dimensionality: int | None = None,
    normalize: bool = False,
    api_key_env: str = "OPENAI_API_KEY",
    version: str | None = None,
    dimension: int | None = None,
) -> UDF:
    """Return an OpenAI embedding UDF with the API key captured at call time.

    The API key is read from ``os.environ[api_key_env]`` at call time and
    serialized with the UDF.  On remote workers the key is available without
    cluster-level ``env_vars`` configuration.

    Parameters
    ----------
    column:
        Name of the input column containing text to embed.
        Defaults to ``"text"``.
    model:
        OpenAI embedding model identifier
        (default ``text-embedding-3-small``).
    output_dimensionality:
        Optional reduced output dimensionality.  When specified the API
        returns truncated embeddings (only supported by
        ``text-embedding-3-*`` models).  If *None*, the model's full
        dimensionality is used.
    normalize:
        Whether to L2-normalise the embeddings.  Defaults to ``False``
        because OpenAI embedding models return pre-normalized vectors.
    api_key_env:
        Environment variable that holds the API key
        (default ``OPENAI_API_KEY``).
    version:
        Explicit version string for the UDF so that key rotation does not
        change the UDF hash and trigger a re-backfill.
    dimension:
        Optional pre-specified embedding dimension.  If *None* (default),
        the dimension is looked up from a built-in table of known models
        (or determined from *output_dimensionality* if set).  If provided,
        model loading is deferred until UDF execution.

    Returns
    -------
    UDF
        A UDF instance ready to be registered with a Geneva dataset.

    Notes
    -----
    Requires the ``openai`` package::

        pip install 'geneva[udf-text-openai]'

    Examples
    --------
    Embed text documents:

    >>> udf = openai_embedding_udf(column="body")
    >>> table.add_columns({"embedding": udf})

    Use a reduced dimensionality:

    >>> udf = openai_embedding_udf(
    ...     column="body",
    ...     output_dimensionality=256,
    ... )
    """
    if model not in KNOWN_OPENAI_EMBEDDING_MODELS:
        warnings.warn(
            f"Unknown OpenAI embedding model {model!r}. Known models: "
            f"{sorted(KNOWN_OPENAI_EMBEDDING_MODELS)}. The model will still "
            f"be used, but may not be valid.",
            stacklevel=2,
        )

    api_key = os.environ[api_key_env]

    # Resolve dimension for lazy mode when possible.
    if dimension is None and output_dimensionality is not None:
        dimension = output_dimensionality
    elif dimension is None:
        dimension = _OPENAI_EMBEDDING_DIMENSIONS.get(model)

    embedding_model = _OpenAIEmbeddingModel(
        model_name=model,
        column=column,
        normalize=normalize,
        api_key=api_key,
        output_dimensionality=output_dimensionality,
    )

    udf_name = f"{OPENAI_EMBEDDING_FAMILY}:{model}"
    return _build_embedding_udf(
        model=embedding_model,
        udf_name=udf_name,
        num_gpus=0.0,
        dimension=dimension,
        on_error=[_openai_retry()],
        version=version,
    )


# ---------------------------------------------------------------------------
# Generative (Chat Completions) UDF
# ---------------------------------------------------------------------------

# Known OpenAI chat model identifiers (update as new models are released).
# Source: https://platform.openai.com/docs/models
KNOWN_OPENAI_MODELS: set[str] = {
    # GPT-4o (retiring from ChatGPT Feb 2026, still available in API)
    "gpt-4o",
    "gpt-4o-mini",
    # GPT-4.1
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    # GPT-5
    "gpt-5-mini",
    "gpt-5-nano",
    # GPT-5.1
    "gpt-5.1",
    # GPT-5.2 (current flagship)
    "gpt-5.2",
    "gpt-5.2-pro",
    # o-series reasoning
    "o1",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
}


@attrs.define
class _OpenAIModel:
    """Stateful callable that carries its OpenAI API key through serialization.

    The API key is captured at definition time and serialized with the object
    so that remote workers can use it without cluster-level ``env_vars``
    configuration.

    Parameters
    ----------
    api_key:
        The OpenAI API key.  Hidden from ``repr`` to avoid leaking secrets.
    prompt:
        Instruction sent to OpenAI alongside each row's value.
    model_name:
        OpenAI model identifier passed to ``chat.completions.create``.
    mime_type:
        MIME type for binary columns (e.g. ``image/jpeg``).
        Required when the input column contains binary data.
    """

    api_key: str = attrs.field(repr=False)
    prompt: str = attrs.field()
    model_name: str = attrs.field(default="gpt-5-mini")
    mime_type: str | None = attrs.field(default=None)

    @cached_property
    def client(self) -> Any:
        """Lazily initialise the OpenAI client on the worker."""
        import openai

        return openai.OpenAI(api_key=self.api_key)

    def _build_content(self, value: Any) -> list[dict[str, Any]]:
        """Build the OpenAI messages payload for a single row value."""
        if isinstance(value, (bytes, bytearray)):
            mime_type = self.mime_type
            if mime_type is None:
                raise ValueError(
                    "mime_type is required for binary columns. "
                    "Pass mime_type to openai_udf() "
                    "(e.g. mime_type='image/jpeg')."
                )
            b64 = base64.b64encode(bytes(value)).decode("ascii")
            data_uri = f"data:{mime_type};base64,{b64}"
            return [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": data_uri},
                        },
                        {"type": "text", "text": self.prompt},
                    ],
                }
            ]
        return [{"role": "user", "content": f"{self.prompt}\n\n{value}"}]

    def generate(self, value: Any) -> str | None:
        """Call OpenAI for a single value.  Returns *None* for null inputs."""
        if value is None:
            return None
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self._build_content(value),
        )
        return response.choices[0].message.content

    def __getstate__(self) -> dict[str, Any]:
        """Serialize only init attrs, excluding cached client."""
        return attrs.asdict(
            self,
            filter=lambda attribute, _: attribute.init,
        )

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(**state)


def openai_udf(
    column: str,
    prompt: str,
    model: str = "gpt-5-mini",
    mime_type: str | None = None,
    api_key_env: str = "OPENAI_API_KEY",
    version: str | None = None,
) -> UDF:
    """Return an OpenAI Chat Completions UDF with the API key captured at call time.

    The API key is read from ``os.environ[api_key_env]`` at call time and
    serialized with the UDF.  On remote workers the key is available without
    cluster-level ``env_vars`` configuration.

    Supports both text and binary (e.g. image) columns.  For text columns
    the prompt is prepended to each value.  For binary columns the raw bytes
    are sent as a base64 ``image_url`` content part alongside the prompt.
    The column type is detected at runtime from the Arrow array; pass
    ``mime_type`` when the column contains binary data.

    Parameters
    ----------
    column:
        Name of the input column.
    prompt:
        Instruction sent to OpenAI alongside each row's value.
    model:
        OpenAI model identifier (default ``gpt-5-mini``).
    mime_type:
        MIME type for binary columns.  Required when the input column
        contains binary data; ignored for text columns.

        Supported types:

        * **Image** — ``image/jpeg``, ``image/png``, ``image/webp``,
          ``image/gif``
          (`docs <https://platform.openai.com/docs/guides/images-vision>`_)
    api_key_env:
        Environment variable that holds the API key
        (default ``OPENAI_API_KEY``).
    version:
        Explicit version string for the UDF so that key rotation does not
        change the UDF hash and trigger a re-backfill.

    Returns
    -------
    UDF
        A UDF instance ready to be registered with a Geneva dataset.

    Notes
    -----
    Requires the ``openai`` package::

        pip install 'geneva[udf-text-openai]'

    Examples
    --------
    Caption images with a one-sentence description:

    >>> udf = openai_udf(
    ...     column="image",
    ...     prompt="Provide a 1 sentence description of the scene",
    ...     mime_type="image/jpeg",
    ... )
    >>> table.add_columns({"caption": udf})

    Summarise text documents:

    >>> udf = openai_udf(
    ...     column="body",
    ...     prompt="Summarise this document in 3 bullet points",
    ... )
    """
    if model not in KNOWN_OPENAI_MODELS:
        warnings.warn(
            f"Unknown OpenAI model {model!r}. Known models: "
            f"{sorted(KNOWN_OPENAI_MODELS)}. The model will still be used, "
            f"but may not be valid.",
            stacklevel=2,
        )

    api_key = os.environ[api_key_env]
    openai_model = _OpenAIModel(
        api_key=api_key, prompt=prompt, model_name=model, mime_type=mime_type
    )

    @udf(
        name=f"openai:{model}",
        data_type=pa.string(),
        version=version,
        input_columns=[column],
        on_error=[_openai_retry()],
    )
    class OpenAIUDF:
        def __init__(self) -> None:
            self._model = openai_model

        def __call__(self, value) -> str | None:  # noqa: ANN001
            return self._model.generate(value)

    return OpenAIUDF()  # type: ignore
