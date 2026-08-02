r"""Provide a structured-output Runnable built from a chat model, with a
JSON-parsing fallback for models that don't reliably support native
structured output."""

from __future__ import annotations

__all__ = ["StructuredOutputError", "structured_output_runnable"]

import functools
import logging
from typing import TYPE_CHECKING, Any, Literal, TypeVar, overload

from langchain_core.runnables import Runnable, RunnableLambda

from zenpyre.utils.json_to_structured import (
    JsonStructuredOutputParseError,
    parse_json_to_structured,
)

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel, LanguageModelInput
    from pydantic import BaseModel

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T", bound="BaseModel")


class StructuredOutputError(RuntimeError):
    """Raised when the underlying LLM output cannot be parsed into the
    requested ``output_type``, even after the JSON-parsing fallback.

    Only raised when ``include_raw=False`` (the default) -- see
    :func:`structured_output_runnable`.
    """


@overload
def structured_output_runnable(
    chat_model: BaseChatModel,
    output_type: type[T],
    *,
    include_raw: Literal[False] = False,
) -> Runnable[LanguageModelInput, T]: ...  # pragma: no cover


@overload
def structured_output_runnable(
    chat_model: BaseChatModel,
    output_type: type[T],
    *,
    include_raw: Literal[True],
) -> Runnable[LanguageModelInput, dict[str, Any]]: ...  # pragma: no cover


def structured_output_runnable(
    chat_model: BaseChatModel,
    output_type: type[T],
    *,
    include_raw: bool = False,
) -> Runnable[LanguageModelInput, T] | Runnable[LanguageModelInput, dict[str, Any]]:
    r"""Build a Runnable that returns validated, structured output, with
    a JSON-parsing fallback.

    This composes ``chat_model.with_structured_output(output_type,
    include_raw=True)`` -- itself a
    :class:`~langchain_core.runnables.Runnable` returning
    ``{"raw": AIMessage, "parsed": T | None, "parsing_error":
    Exception | None}`` -- with a small unwrapping step piped after it
    via ``|``.

    If the chat model's native structured-output parsing fails (e.g.
    the model didn't emit a proper tool call, which is common with
    small or local models), the unwrap step falls back to manually
    parsing the raw message content as JSON, without making a second
    LLM call.

    ``include_raw`` controls both the output shape *and* the failure
    behavior, mirroring ``with_structured_output``'s own contract:

    * ``include_raw=False`` (default): invoking returns ``T``
      directly. If both native parsing and the JSON fallback fail,
      this raises :class:`StructuredOutputError`.
    * ``include_raw=True``: invoking returns a dict with the same
      ``"raw"``/``"parsed"``/``"parsing_error"`` keys as
      ``with_structured_output(..., include_raw=True)``, plus a
      ``"used_fallback": bool`` key. This mode never raises on parse
      failure, matching the underlying method's own fail-open
      contract: ``"parsed"`` is populated whenever native parsing *or*
      the JSON fallback succeeds, and ``"parsing_error"`` is only set
      if both fail.

    Because the result is a plain ``|``-composed
    :class:`~langchain_core.runnables.RunnableSequence`, it already
    implements ``invoke``, ``ainvoke``, ``batch``, ``abatch``,
    ``stream``, ``astream``, and config propagation -- nothing here
    reimplements the ``Runnable`` interface. ``batch``/``abatch`` in
    particular delegate to each step's own batch implementation (so
    the chat model's native batching is preserved), and correctly
    skip re-processing items that already failed when
    ``return_exceptions=True``.

    Args:
        chat_model: The chat model to wrap.
        output_type: The type (e.g. a Pydantic model) that the LLM
            output should be parsed into.
        include_raw: If ``False`` (default), invoking returns
            ``output_type`` directly and raises
            :class:`StructuredOutputError` on total parse failure. If
            ``True``, invoking returns a
            ``{"raw", "parsed", "parsing_error", "used_fallback"}``
            dict and never raises on parse failure.

    Returns:
        A ``Runnable[LanguageModelInput, T]`` if ``include_raw=False``,
        or a ``Runnable[LanguageModelInput, dict[str, Any]]`` if
        ``include_raw=True``.

    Example:
        ```pycon
        >>> from pydantic import BaseModel
        >>> class Answer(BaseModel):
        ...     value: int
        ...
        >>> chain = structured_output_runnable(chat_model, Answer)  # doctest: +SKIP
        >>> chain.invoke("What is 2+2?")  # doctest: +SKIP
        Answer(value=4)

        ```
    """
    structured = chat_model.with_structured_output(output_type, include_raw=True)
    unwrap = RunnableLambda(
        functools.partial(_unwrap, output_type=output_type, include_raw=include_raw)
    ).with_config(run_name="unwrap_structured_output")
    return structured | unwrap


def _unwrap(
    result: dict[str, Any], *, output_type: type[T], include_raw: bool
) -> T | dict[str, Any]:
    """Extract (or assemble) the unwrapped structured-output result.

    If the underlying chat model already parsed the output
    successfully, that parsed value is used directly. If parsing
    failed, this falls back to manually parsing the raw message
    content as JSON via
    :func:`~zenpyre.utils.json_to_structured.parse_json_to_structured`.

    Args:
        result: The dict returned by the underlying LLM when
            ``include_raw=True``, containing ``"raw"``, ``"parsed"``,
            and ``"parsing_error"`` keys.
        output_type: The type to parse the fallback JSON content into.
        include_raw: Controls both the return shape and the failure
            behavior -- see :func:`structured_output_runnable`'s
            docstring for the full contract.

    Returns:
        If ``include_raw`` is ``False``: the parsed ``output_type``
        instance. If ``include_raw`` is ``True``: a dict with
        ``"raw"``, ``"parsed"``, ``"parsing_error"``, and
        ``"used_fallback"`` keys.

    Raises:
        StructuredOutputError: If ``include_raw`` is ``False`` and
            both native parsing and the JSON fallback fail.
    """
    if result["parsing_error"] is None and result["parsed"] is not None:
        if include_raw:
            return {**result, "used_fallback": False}
        return result["parsed"]

    raw_content = _as_text(result["raw"].content)
    try:
        parsed = parse_json_to_structured(raw_content, output_type)
    except JsonStructuredOutputParseError as e:
        native_error = result["parsing_error"]
        msg = (
            f"Failed to parse LLM output into {output_type.__name__}: "
            f"{native_error!r}. Fallback manual JSON parsing also failed: {e}"
        )
        if include_raw:
            return {**result, "parsing_error": StructuredOutputError(msg), "used_fallback": False}
        raise StructuredOutputError(msg) from e

    if include_raw:
        return {**result, "parsed": parsed, "parsing_error": None, "used_fallback": True}
    return parsed


def _as_text(content: str | list[Any]) -> str:
    """Normalize an ``AIMessage.content`` value into a plain string.

    ``content`` is usually a plain ``str``, but some providers return
    a list of content blocks instead (e.g. for multimodal or certain
    tool-calling response formats). In that case, this concatenates
    the text of any string or ``{"type": "text", ...}`` blocks,
    ignoring non-text blocks (e.g. images), so the JSON fallback
    parser always receives a string.

    Args:
        content: The raw ``content`` value from an ``AIMessage``.

    Returns:
        The text content as a single string.
    """
    if isinstance(content, str):
        return content
    parts = [
        block if isinstance(block, str) else block.get("text", "")
        for block in content
        if isinstance(block, str) or block.get("type") == "text"
    ]
    return "".join(parts)
