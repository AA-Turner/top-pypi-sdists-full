# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pre-built Gemini generative-AI UDF helper."""

import os
import warnings
from functools import cached_property
from typing import Any

import attrs
import pyarrow as pa

from geneva.debug.error_store import Retry
from geneva.transformer import UDF, udf


def _gemini_retry() -> Retry:
    """Build a Retry for Gemini API errors (lazy import)."""
    from google.genai import errors

    client_error = getattr(errors, "ClientError", Exception)
    server_error = getattr(errors, "ServerError", Exception)

    return Retry(client_error, server_error, max_attempts=7, backoff="exponential")


# Known Gemini model identifiers (update as new models are released).
KNOWN_GEMINI_MODELS: set[str] = {
    # Gemini 3 (preview)
    "gemini-3-pro-preview",
    "gemini-3-pro-image-preview",
    "gemini-3-flash-preview",
    # Gemini 2.5 (stable)
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-image",
    # Gemini 2.5 (preview)
    "gemini-2.5-pro-preview-tts",
    "gemini-2.5-flash-preview-tts",
}


@attrs.define
class _GeminiModel:
    """Stateful callable that carries its Gemini API key through serialization.

    The API key is captured at definition time and serialized with the object
    so that remote workers can use it without cluster-level ``env_vars``
    configuration.

    Parameters
    ----------
    api_key:
        The Gemini API key. Hidden from ``repr`` to avoid leaking secrets.
    prompt:
        Instruction sent to Gemini alongside each row's value.
    model_name:
        Gemini model identifier passed to ``GenerativeModel``.
    mime_type:
        MIME type for binary columns (e.g. ``image/jpeg``).
        Required when the input column contains binary data.
    """

    api_key: str = attrs.field(repr=False)
    prompt: str = attrs.field()
    model_name: str = attrs.field(default="gemini-2.5-flash")
    mime_type: str | None = attrs.field(default=None)

    @cached_property
    def client(self) -> Any:
        """Lazily initialise the Gemini client on the worker."""
        import google.genai as genai

        return genai.Client(api_key=self.api_key)

    def _build_content(self, value: Any) -> Any:
        """Build the Gemini content payload for a single row value."""
        if isinstance(value, (bytes, bytearray)):
            from google.genai import types

            mime_type = self.mime_type
            if mime_type is None:
                raise ValueError(
                    "mime_type is required for binary columns. "
                    "Pass mime_type to gemini_udf() (e.g. mime_type='image/jpeg')."
                )
            return [
                types.Part.from_bytes(data=bytes(value), mime_type=mime_type),
                self.prompt,
            ]
        return f"{self.prompt}\n\n{value}"

    def generate(self, value: Any) -> str | None:
        """Call Gemini for a single value. Returns *None* for null inputs."""
        if value is None:
            return None
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=self._build_content(value),
        )
        return response.text

    def __getstate__(self) -> dict[str, Any]:
        """Serialize only init attrs, excluding cached client."""
        return attrs.asdict(
            self,
            filter=lambda attribute, _: attribute.init,
        )

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(**state)


def gemini_udf(
    column: str,
    prompt: str,
    model: str = "gemini-2.5-flash",
    mime_type: str | None = None,
    api_key_env: str = "GEMINI_API_KEY",
    version: str | None = None,
) -> UDF:
    """Return a Gemini UDF with the API key captured from the local environment.

    The API key is read from ``os.environ[api_key_env]`` at call time and
    serialized with the UDF.  On remote workers the key is available without
    cluster-level ``env_vars`` configuration.

    Supports both text and binary (e.g. image) columns.  For text columns
    the prompt is prepended to each value.  For binary columns the raw bytes
    are sent as inline data with the given ``mime_type`` alongside the prompt.
    The column type is detected at runtime from the Arrow array; pass
    ``mime_type`` when the column contains binary data.

    Parameters
    ----------
    column:
        Name of the input column.
    prompt:
        Instruction sent to Gemini alongside each row's value.
    model:
        Gemini model identifier (default ``gemini-2.5-flash``).
    mime_type:
        MIME type for binary columns.  Required when the input column
        contains binary data; ignored for text columns.

        Supported types:

        * **Image** — ``image/jpeg``, ``image/png``, ``image/webp``,
          ``image/heic``, ``image/heif``
          (`docs <https://ai.google.dev/gemini-api/docs/vision>`_)
        * **Audio** — ``audio/wav``, ``audio/mp3``, ``audio/aac``,
          ``audio/flac``, ``audio/aiff``, ``audio/ogg``
          (`docs <https://ai.google.dev/gemini-api/docs/audio>`_)
        * **Video** — ``video/mp4``, ``video/mpeg``, ``video/webm``,
          ``video/mov``, ``video/avi``, ``video/x-flv``, ``video/wmv``,
          ``video/mpg``, ``video/3gpp``
          (`docs <https://ai.google.dev/gemini-api/docs/video-understanding>`_)
        * **Document** — ``application/pdf``, ``text/plain``

        Note: inline data is limited to 20 MB per request.
    api_key_env:
        Environment variable that holds the API key (default ``GEMINI_API_KEY``).
    version:
        Explicit version string for the UDF so that key rotation does not
        change the UDF hash and trigger a re-backfill.

    Returns
    -------
    UDF
        A UDF instance ready to be registered with a Geneva dataset.

    Notes
    -----
    Requires the ``google-genai`` package::

        pip install 'geneva[udf-text-gemini]'

    Examples
    --------
    Caption images with a one-sentence description:

    >>> udf = gemini_udf(
    ...     column="image",
    ...     prompt="Provide a 1 sentence description of the scene",
    ...     mime_type="image/jpeg",
    ... )
    >>> table.add_columns({"caption": udf})

    Summarise text documents:

    >>> udf = gemini_udf(
    ...     column="body",
    ...     prompt="Summarise this document in 3 bullet points",
    ... )
    """
    if model not in KNOWN_GEMINI_MODELS:
        warnings.warn(
            f"Unknown Gemini model {model!r}. Known models: "
            f"{sorted(KNOWN_GEMINI_MODELS)}. The model will still be used, "
            f"but may not be valid.",
            stacklevel=2,
        )

    api_key = os.environ[api_key_env]
    gemini_model = _GeminiModel(
        api_key=api_key, prompt=prompt, model_name=model, mime_type=mime_type
    )

    @udf(
        name=f"gemini:{model}",
        data_type=pa.string(),
        version=version,
        input_columns=[column],
        on_error=[_gemini_retry()],
    )
    class GeminiUDF:
        def __init__(self) -> None:
            self._model = gemini_model

        def __call__(self, value) -> str | None:
            return self._model.generate(value)

    return GeminiUDF()  # type: ignore
