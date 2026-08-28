# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pre-built embedding UDF helpers."""

import abc
import logging
import os
import urllib.parse
import warnings
from functools import cached_property
from typing import Any

import attrs
import pyarrow as pa

from geneva.debug.error_store import Retry
from geneva.transformer import UDF, udf

_LOG = logging.getLogger(__name__)


SENTENCE_TRANSFORMERS_FAMILY = "sentence-transformers"
DEFAULT_SENTENCE_TRANSFORMER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_SENTENCE_TRANSFORMER_COLUMN = "text"

GEMINI_EMBEDDING_FAMILY = "gemini-embedding"
DEFAULT_GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"

# Known Gemini embedding model identifiers (update as new models are released).
KNOWN_GEMINI_EMBEDDING_MODELS: set[str] = {
    "gemini-embedding-001",
}

# Default output dimensions for known Gemini embedding models.
_GEMINI_EMBEDDING_DIMENSIONS: dict[str, int] = {
    "gemini-embedding-001": 3072,
}


def _gemini_retry() -> Retry:
    """Build a Retry for Gemini API errors (lazy import)."""
    from google.genai import errors

    client_error = getattr(errors, "ClientError", Exception)
    server_error = getattr(errors, "ServerError", Exception)

    return Retry(client_error, server_error, max_attempts=7, backoff="exponential")


def _extract_string_inputs(
    values_array: pa.Array,
) -> tuple[list[str], list[int], list[Any]]:
    """Return valid string values and their row indices from ``values_array``."""

    if not pa.types.is_string(values_array.type) and not pa.types.is_large_string(
        values_array.type
    ):
        raise TypeError("embedding UDF input column must contain string data")

    values = values_array.to_pylist()
    valid_indices: list[int] = []
    valid_texts: list[str] = []
    for idx, value in enumerate(values):
        if value is None:
            continue
        if not isinstance(value, str):
            raise TypeError(
                f"embedding UDF expects string inputs, received {type(value).__name__}."
            )
        valid_indices.append(idx)
        valid_texts.append(value)

    return valid_texts, valid_indices, values


# Token counts are estimated from UTF-8 *bytes*, not characters.  BPE runs on
# the byte stream, so UTF-8 already carries most of the cost a non-Latin script
# pays.  Measured against tiktoken, bytes/token spans ~1.4 (base64) to 4.5
# (English), where the same texts span ~0.77 (Japanese on cl100k) to 4.5 by
# character -- so a fixed 4-characters-per-token rule under-counts Japanese by
# more than 5x, and the API rejects the request.
#
# A token always consumes at least one byte, so bytes/token is never below 1
# and ``size / _MIN_BYTES_PER_TOKEN`` is a hard upper bound on the token count.
_MIN_BYTES_PER_TOKEN = 1.0

# Where the estimate starts, before any response has reported a real token
# count.  Set at the natural-language end of the measured range, which is
# tight: English 4.5, Chinese 4.3, Japanese 4.0, Korean 3.8.  Prose in any
# script therefore fits its first request without relying on the recovery
# path.  Denser inputs -- minified JSON at ~2.9 bytes/token, base64 at ~1.4 --
# overshoot once, get split, and calibrate from the halves that succeed.
_INITIAL_BYTES_PER_TOKEN = 4.0


@attrs.define
class _TokenRatio:
    """UTF-8 bytes per token, calibrated from what the API reports.

    Every embeddings response carries the true token count of its request, so
    the ratio is measured rather than guessed -- no tokenizer dependency, and
    no need to provoke a rejection to learn.  Held per model instance, which a
    worker reuses across batches, so the calibration is paid once and then
    applies to every later request.

    Keeps the *smallest* ratio seen rather than the most recent.  A mixed
    column (English rows beside base64 ones) would otherwise swing between a
    generous estimate and a rejected request; converging downward costs some
    request size on the easy rows and never costs a rejection.
    """

    observed: float | None = attrs.field(default=None, init=False)

    @property
    def bytes_per_token(self) -> float:
        """The ratio to size the next request with."""
        if self.observed is None:
            return _INITIAL_BYTES_PER_TOKEN
        return self.observed

    def observe(self, byte_count: int, tokens: int | None) -> None:
        """Record the token count the API reported for ``byte_count`` bytes."""
        if not tokens or tokens <= 0 or byte_count <= 0:
            return
        ratio = max(byte_count / tokens, _MIN_BYTES_PER_TOKEN)
        if self.observed is None or ratio < self.observed:
            self.observed = ratio


def _next_chunk_end(
    sizes: list[int],
    start: int,
    *,
    max_inputs: int,
    max_tokens: int,
    bytes_per_token: float,
) -> int:
    """End index of the largest ``sizes[start:end]`` that fits one request.

    ``sizes`` are UTF-8 byte lengths.  The chunk closes when adding the next
    input would exceed *max_inputs* or the estimated *max_tokens*.  An input
    whose own estimate exceeds the budget is returned alone: splitting cannot
    make one text smaller, so the API decides.
    """
    per_token = max(bytes_per_token, _MIN_BYTES_PER_TOKEN)
    tokens = 0.0
    end = start
    while end < len(sizes) and end - start < max_inputs:
        estimate = sizes[end] / per_token + 1
        if end > start and tokens + estimate > max_tokens:
            break
        tokens += estimate
        end += 1
    return end


def _normalize_embeddings(embeddings: list[list[float]]) -> list[list[float]]:
    """L2-normalise ``embeddings``, leaving zero vectors untouched."""
    import numpy as np

    arr = np.array(embeddings)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms = np.where(norms > 0, norms, 1)
    return (arr / norms).tolist()


def _resolve_device(num_gpus: float) -> str | None:
    if num_gpus <= 0:
        return None

    try:
        import torch
    except ImportError:
        _LOG.warning("torch not available; falling back to CPU for embeddings")
        return None

    if torch.cuda.is_available():
        _LOG.debug("CUDA is available; using GPU for embeddings")
        return "cuda"

    _LOG.debug("GPU requested but CUDA is not available; using CPU")
    return None


@attrs.define
class _EmbeddingModel(abc.ABC):
    """
    Base class interface for implementing pre-baked embedding models.
    All model families are required to only implement:
    * _build_model - load and return the model instance
    * _get_dimension - return the model's embedding dimension
    * embed_array - embed a string Array, returning a ListArray of float32

    The base class handles lazy model loading, dimension caching, and output type.

    Parameters
    ----------
    model_name:
        The model being used for embedding. It can be a name of a model
        to be loaded from HuggingFace Hub, a local path or in case of
        API-based models, it can be an endpoint URL or model ID.
    column:
        Name of the column that will be embedded.
    normalize:
        Whether to L2-normalise the generated embeddings.
    num_gpus:
        GPU allocation requested for the UDF. Values ``>= 0``
        positive values will request CUDA based execution.
    """

    model_name: str = attrs.field(kw_only=True)
    column: str = attrs.field(kw_only=True)
    normalize: bool = attrs.field(kw_only=True)
    num_gpus: float = attrs.field(
        default=0.0, kw_only=True, validator=attrs.validators.ge(0)
    )

    _device: str | None = attrs.field(init=False, default=None)

    @abc.abstractmethod
    def _build_model(self) -> Any:
        """
        Return the model instance for the embedding backend. This
        method is called by UDF worker to lazily load the model.
        This can be used for one-time setup of the model instance, or
        client in case of API-based models (e.g. OpenAI, Gemini).
        """

    @abc.abstractmethod
    def _get_dimension(self) -> int:
        """
        Return the embedding dimension for the model.
        Embedding dimension must be a positive integer. It is the
        length of the embedding vector returned by the model for each input.
        """

    @abc.abstractmethod
    def embed_array(self, values: pa.Array) -> pa.Array:
        """
        Embed the ``values`` string array and return a fixed-size list array of
        floats. It should handle missing inputs gracefully. For example::

            ["hello", None, "world"] -> [[0.1, 0.2], None, [0.3, 0.4]]
        """

    def embed(self, batch: pa.RecordBatch) -> pa.Array:
        """Deprecated RecordBatch entry point, kept for payload compatibility.

        Embedding UDFs became Array UDFs so a backfill projects only the text
        column instead of the whole row. That changed the model call contract,
        and the contract is a persistence boundary: ``EmbeddingUDF.__call__``
        is cloudpickled *by value*, while the model class is resolved *by
        reference* from the installed module. A UDF pickled before the change
        therefore keeps calling ``embed(batch)`` against a newer module, so
        this has to keep working. New code calls :meth:`embed_array`.

        Deliberately not warning per call: this is the path an old payload
        takes on every batch, and a warning there is noise the caller cannot
        act on. Remove once no stored payload predates the Array UDFs.
        """
        index = batch.schema.get_field_index(self.column)
        if index == -1:
            raise ValueError(f"Column '{self.column}' not found in RecordBatch")
        return self.embed_array(batch.column(index))

    @cached_property
    def model(self) -> Any:
        """Lazily load and cache the model instance."""
        return self._build_model()

    @cached_property
    def dimension(self) -> int:
        """Lazily get and cache the model's embedding dimension."""
        dimension = self._get_dimension()
        if dimension <= 0:
            raise ValueError("embedding dimension must be a positive integer")
        return dimension

    def output_type(self) -> pa.DataType:
        return pa.list_(pa.float32(), self.dimension)

    def __getstate__(self) -> dict[str, Any]:
        """
        only serialize attributes excluding internal state or cached properties
        """
        return attrs.asdict(
            self,
            # include only the attributes that are part of __init__
            filter=lambda attribute, value: attribute.init,
        )

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(**state)


@attrs.define
class _SentenceTransformersModel(_EmbeddingModel):
    trust_remote_code: bool = attrs.field(default=False, kw_only=True)

    def _build_model(self) -> Any:
        self._device = _resolve_device(self.num_gpus)
        model = self._load_model(self.model_name, self._device, self.trust_remote_code)
        return model

    def _get_dimension(self) -> int:
        dimension = self.model.get_sentence_embedding_dimension()
        return int(dimension)

    def embed_array(self, values_array: pa.Array) -> pa.Array:
        model = self.model
        valid_texts, valid_indices, values = _extract_string_inputs(values_array)

        outputs: list[list[float] | None] = [None] * len(values)
        if valid_texts:
            embeddings = model.encode(
                valid_texts,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize,
            )
            vectors = embeddings.tolist()
            for idx, vector in zip(valid_indices, vectors, strict=False):
                outputs[idx] = vector

        return pa.array(outputs, type=self.output_type())

    @staticmethod
    def _load_model(
        model_name: str, device: str | None, trust_remote_code: bool
    ) -> Any:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required; install via "
                "`pip install sentence-transformers`"
            ) from exc

        return SentenceTransformer(
            model_name, device=device, trust_remote_code=trust_remote_code
        )


def _build_embedding_udf(
    model: _EmbeddingModel,
    udf_name: str,
    num_gpus: float,
    dimension: int | None = None,
    on_error: list[Any] | None = None,
    version: str | None = None,
) -> UDF:
    """
    Build an embedding UDF from a model.

    Parameters
    ----------
    model:
        The embedding model instance
    udf_name:
        Name for the UDF
    num_gpus:
        GPU allocation for the UDF
    dimension:
        Optional pre-specified embedding dimension. If None, will eagerly
        load the model to determine dimension. If provided, model loading
        is deferred until UDF execution.
    on_error:
        Optional error handling configuration passed to the ``@udf`` decorator.
    version:
        Optional explicit version string passed to the ``@udf`` decorator.
    """
    if dimension is None:
        # Eager mode: load model now to get dimension
        dimension = model.dimension
        data_type = model.output_type()
    else:
        # Lazy mode: use provided dimension, defer model loading
        data_type = pa.list_(pa.float32(), dimension)

    @udf(
        name=udf_name,
        data_type=data_type,
        num_gpus=num_gpus,
        on_error=on_error,
        version=version,
        # Array UDF over the single text column: the scanner projects to just
        # this column instead of reading (and discarding) the whole row.
        input_columns=[model.column],
    )
    class EmbeddingUDF:
        def __init__(self) -> None:
            self._model = model
            self.dimension = dimension

        def __call__(self, values: pa.Array) -> pa.Array:
            # Both halves of the compatibility story. This function is
            # cloudpickled by value, so it travels with the payload, while
            # ``self._model``'s class comes from whatever module the runtime
            # has installed. Against an older module there is no
            # ``embed_array``, so hand it the RecordBatch its contract expects
            # -- one column, which is all this UDF reads anyway.
            embed_array = getattr(self._model, "embed_array", None)
            if embed_array is None:
                return self._model.embed(
                    pa.RecordBatch.from_arrays([values], [self._model.column])
                )
            return embed_array(values)

    return EmbeddingUDF()  # type: ignore


# Supported pre-baked embedding UDFs


def sentence_transformer_udf(
    model: str = DEFAULT_SENTENCE_TRANSFORMER_MODEL,
    column: str = DEFAULT_SENTENCE_TRANSFORMER_COLUMN,
    normalize: bool = True,
    num_gpus: float = 0.0,
    trust_remote_code: bool = False,
    dimension: int | None = None,
) -> UDF:
    """
    Return a stateful sentence-transformers embedding UDF.

    Parameters
    ----------
    model:
        The model being used for embedding. by default, it uses
        ``sentence-transformers/all-MiniLM-L6-v2`` from HuggingFace Hub.
    column:
        Name of the column that will be embedded. By default, it uses ``text``.
    normalize:
        Whether to L2-normalise the generated embeddings. Defaults to ``True``.
    num_gpus:
        Fractional GPU allocation requested for the UDF. Values ``>= 0``
        Be default, keeps execution on CPU; positive values request CUDA.
    trust_remote_code:
        Whether to trust remote code when loading the model. Defaults to ``False``
        as recommended by sentence-transformers.
    dimension:
        Optional pre-specified embedding dimension. If None (default), will eagerly
        load the model to determine dimension. If provided, model loading is deferred
        until UDF execution. Use this for lazy loading when the model is not available
        at UDF definition time (e.g., in manifest upload scripts).

    Returns
    -------
    UDF
        A UDF instance that can be registered with a Geneva dataset.
    """

    embedding_model = _SentenceTransformersModel(
        model_name=model,
        column=column,
        normalize=normalize,
        num_gpus=num_gpus,
        trust_remote_code=trust_remote_code,
    )
    model_name_sanitized = urllib.parse.quote_plus(model)
    udf_name = f"{SENTENCE_TRANSFORMERS_FAMILY}:{model_name_sanitized}"
    return _build_embedding_udf(
        model=embedding_model,
        udf_name=udf_name,
        num_gpus=num_gpus,
        dimension=dimension,
    )


# ---------------------------------------------------------------------------
# Gemini embedding UDF
# ---------------------------------------------------------------------------


@attrs.define
class _GeminiEmbeddingModel(_EmbeddingModel):
    """Gemini API-based embedding model.

    Carries its API key through serialization so that remote workers
    can use it without cluster-level ``env_vars`` configuration.

    Parameters
    ----------
    api_key:
        The Gemini API key.  Hidden from ``repr`` to avoid leaking secrets.
    task_type:
        Optional task-type hint (e.g. ``RETRIEVAL_DOCUMENT``).
    output_dimensionality:
        Optional reduced output dimensionality (Matryoshka Representation
        Learning).  When set, the API returns truncated embeddings.
    """

    api_key: str = attrs.field(repr=False, kw_only=True)
    task_type: str | None = attrs.field(default=None, kw_only=True)
    output_dimensionality: int | None = attrs.field(default=None, kw_only=True)

    def _build_model(self) -> Any:
        """Lazily create a per-instance Gemini client on the worker."""
        import google.genai as genai

        return genai.Client(api_key=self.api_key)

    def _get_dimension(self) -> int:
        if self.output_dimensionality is not None:
            return self.output_dimensionality
        dim = _GEMINI_EMBEDDING_DIMENSIONS.get(self.model_name)
        if dim is not None:
            return dim
        # Unknown model — make a single probe call to discover the dimension.
        result = self.model.models.embed_content(
            model=self.model_name,
            contents="dimension probe",
        )
        return len(result.embeddings[0].values)

    def embed_array(self, values_array: pa.Array) -> pa.Array:
        from google.genai import types

        valid_texts, valid_indices, values = _extract_string_inputs(values_array)

        outputs: list[list[float] | None] = [None] * len(values)
        if valid_texts:
            config = types.EmbedContentConfig(
                task_type=self.task_type,
                output_dimensionality=self.output_dimensionality,
            )
            result = self.model.models.embed_content(
                model=self.model_name,
                contents=valid_texts,
                config=config,
            )
            embeddings: list[list[float]] = [e.values for e in result.embeddings]

            if self.normalize:
                embeddings = _normalize_embeddings(embeddings)

            for idx, vector in zip(valid_indices, embeddings, strict=False):
                outputs[idx] = vector

        return pa.array(outputs, type=self.output_type())


def gemini_embedding_udf(
    column: str = "text",
    model: str = DEFAULT_GEMINI_EMBEDDING_MODEL,
    task_type: str | None = None,
    output_dimensionality: int | None = None,
    normalize: bool = False,
    api_key_env: str = "GEMINI_API_KEY",
    version: str | None = None,
    dimension: int | None = None,
) -> UDF:
    """Return a Gemini embedding UDF with the API key captured at call time.

    The API key is read from ``os.environ[api_key_env]`` at call time and
    serialized with the UDF.  On remote workers the key is available without
    cluster-level ``env_vars`` configuration.

    Parameters
    ----------
    column:
        Name of the input column containing text to embed.
        Defaults to ``"text"``.
    model:
        Gemini embedding model identifier (default ``gemini-embedding-001``).
    task_type:
        Optional task-type hint for the embedding model.  One of
        ``RETRIEVAL_QUERY``, ``RETRIEVAL_DOCUMENT``, ``SEMANTIC_SIMILARITY``,
        ``CLASSIFICATION``, ``CLUSTERING``, ``QUESTION_ANSWERING``,
        ``FACT_VERIFICATION``.  If *None*, the API default is used.
    output_dimensionality:
        Optional reduced output dimensionality.  When specified the API
        returns truncated embeddings (Matryoshka Representation Learning).
        If *None*, the model's full dimensionality is used (768 for
        ``gemini-embedding-001``).
    normalize:
        Whether to L2-normalise the embeddings.  Defaults to ``False``
        because Gemini embedding models return pre-normalized vectors.
    api_key_env:
        Environment variable that holds the API key (default ``GEMINI_API_KEY``).
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
    """
    if model not in KNOWN_GEMINI_EMBEDDING_MODELS:
        warnings.warn(
            f"Unknown Gemini embedding model {model!r}. Known models: "
            f"{sorted(KNOWN_GEMINI_EMBEDDING_MODELS)}. The model will still "
            f"be used, but may not be valid.",
            stacklevel=2,
        )

    api_key = os.environ[api_key_env]

    # Resolve dimension for lazy mode when possible.
    if dimension is None and output_dimensionality is not None:
        dimension = output_dimensionality
    elif dimension is None:
        dimension = _GEMINI_EMBEDDING_DIMENSIONS.get(model)

    embedding_model = _GeminiEmbeddingModel(
        model_name=model,
        column=column,
        normalize=normalize,
        api_key=api_key,
        task_type=task_type,
        output_dimensionality=output_dimensionality,
    )

    udf_name = f"{GEMINI_EMBEDDING_FAMILY}:{model}"
    return _build_embedding_udf(
        model=embedding_model,
        udf_name=udf_name,
        num_gpus=0.0,
        dimension=dimension,
        on_error=[_gemini_retry()],
        version=version,
    )
