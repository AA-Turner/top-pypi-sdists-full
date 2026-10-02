r"""Contain a simple agent."""

from __future__ import annotations

__all__ = ["AgentChatModel"]

from typing import TYPE_CHECKING, Any

from langchain_core.language_models import BaseChatModel, LanguageModelInput
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import Runnable, RunnableConfig

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator


class AgentChatModel(Runnable[LanguageModelInput | dict[str, Any], dict[str, Any]]):
    r"""Wrap a ``BaseChatModel`` so it exposes the same input/output
    shape as an agent (e.g. ``AgentRunnable`` / ``create_agent``),
    without any tool-calling loop.

    This is useful for dropping a plain chat model into a workflow that's
    built to work with agents: callers can treat this object as if it were
    an agent (accepting the same flexible input shapes and returning the
    same ``{"messages": ...}`` dict shape, with an optional
    ``"structured_response"`` key), while under the hood it's just a
    single call to the wrapped chat model.

    For ``invoke``/``ainvoke``, the input is coerced to a list of
    ``BaseMessage`` objects (optionally prefixed with a system prompt),
    passed to the wrapped model, and the resulting AI message is appended
    to that list. If ``response_format`` is set, the model is queried
    with structured output enabled and a ``"structured_response"`` key
    is added to the result, mirroring ``create_agent``'s behavior.

    Note:
        ``stream``/``astream`` do **not** follow the same
        ``{"messages": ...}`` shape as ``invoke``/``ainvoke``. They
        instead yield the raw ``BaseMessage`` chunks produced by the
        wrapped model's own streaming interface, do not accumulate a
        running message history, and ignore ``response_format``
        entirely (structured output is not supported in streaming
        mode). See the docstrings of those methods for details.

    Accepted input shapes (for all four methods):
        - ``str``: treated as a single human message.
        - ``list[BaseMessage | str]``: used as-is, with any bare strings
          converted to human messages.
        - ``dict`` with a ``"messages"`` key: the value is treated the
          same way as the ``list`` case above (missing key defaults to
          an empty list).

    If a ``system_prompt`` was provided at construction time and the
    resulting message list does not already contain a ``SystemMessage``,
    a ``SystemMessage`` built from ``system_prompt`` is prepended.

    Attributes:
        _model: The chat model to wrap.
        _system_prompt: An optional system prompt to prepend to every
            call, unless the input already contains a system message.
        _response_format: An optional schema (e.g. a Pydantic model, a
            TypedDict, or a JSON schema dict) passed to the wrapped
            model's ``with_structured_output``. When set, ``invoke``/
            ``ainvoke`` additionally return a ``"structured_response"``
            key in the result dict, parsed according to this schema.

    Example:
        ```pycon
        >>> from zenpyre.agents import AgentChatModel
        >>> agent = AgentChatModel(model=my_chat_model)  # doctest: +SKIP
        >>> result = agent.invoke("What is the capital of France?")  # doctest: +SKIP
        >>> result["messages"][-1].content  # doctest: +SKIP
        'The capital of France is Paris.'

        ```
    """

    def __init__(
        self,
        model: BaseChatModel,
        system_prompt: str | None = None,
        response_format: Any | None = None,
    ) -> None:
        r"""Initialize the ``AgentChatModel``.

        Args:
            model: The chat model to wrap. All calls are delegated to
                this model; ``AgentChatModel`` adds no tool-calling loop
                or other agent behavior of its own.
            system_prompt: An optional system prompt. If set, it is
                prepended as a ``SystemMessage`` to the message list on
                every call, unless the input already contains a system
                message. Defaults to ``None`` (no system prompt is
                added).
            response_format: An optional schema describing the desired
                structured output (e.g. a Pydantic ``BaseModel``
                subclass, a ``TypedDict``, or a JSON schema dict), with
                the same semantics as
                ``BaseChatModel.with_structured_output``. When set, the
                wrapped model is queried with structured output enabled
                and the parsed result is exposed under the
                ``"structured_response"`` key of the dict returned by
                ``invoke``/``ainvoke``. Defaults to ``None`` (no
                structured output).
        """
        self._model = model
        self._system_prompt = system_prompt
        self._response_format = response_format

        # Pre-bind the structured-output wrapper once, mirroring how a
        # tool-calling agent pre-binds tools in __init__. include_raw=True
        # gives us back both the raw AIMessage and the parsed object in a
        # single model call.
        self._structured_model = (
            self._model.with_structured_output(self._response_format, include_raw=True)
            if self._response_format is not None
            else None
        )

    def invoke(
        self,
        input: LanguageModelInput | dict[str, Any],  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        r"""Invoke the wrapped chat model once and return an agent-shaped
        result.

        Args:
            input: The input to the model. See the class docstring for
                the accepted shapes (``str``, ``list``, or ``dict`` with
                a ``"messages"`` key).
            config: Optional ``RunnableConfig`` forwarded to the wrapped
                model's ``invoke`` call.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped model's ``invoke`` call.

        Returns:
            A dict with:

            - ``"messages"``: the full list of ``BaseMessage`` objects
              used for the call (including any prepended system prompt),
              with the model's response message appended at the end.
            - ``"structured_response"``: present only if
              ``response_format`` was set at construction time. The
              parsed structured output, as an instance of
              ``response_format``.
        """
        messages = self._coerce_input(input)

        if self._structured_model is not None:
            result = self._structured_model.invoke(messages, config=config, **kwargs)
            ai_message: BaseMessage = result["raw"]
            messages.append(ai_message)
            return {
                "messages": messages,
                "structured_response": result["parsed"],
            }

        ai_message = self._model.invoke(messages, config=config, **kwargs)
        messages.append(ai_message)
        return {"messages": messages}

    async def ainvoke(
        self,
        input: LanguageModelInput | dict[str, Any],  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        r"""Asynchronously invoke the wrapped chat model once and return
        an agent-shaped result.

        This is the async counterpart of :meth:`invoke`; see its
        docstring for details on accepted input shapes and the returned
        dict, including the ``"structured_response"`` key when
        ``response_format`` is set.

        Args:
            input: The input to the model. See the class docstring for
                the accepted shapes (``str``, ``list``, or ``dict`` with
                a ``"messages"`` key).
            config: Optional ``RunnableConfig`` forwarded to the wrapped
                model's ``ainvoke`` call.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped model's ``ainvoke`` call.

        Returns:
            A dict with ``"messages"``, and (if
            ``response_format`` is set) ``"structured_response"``.
        """
        messages = self._coerce_input(input)

        if self._structured_model is not None:
            result = await self._structured_model.ainvoke(messages, config=config, **kwargs)
            ai_message: BaseMessage = result["raw"]
            messages.append(ai_message)
            return {
                "messages": messages,
                "structured_response": result["parsed"],
            }

        ai_message = await self._model.ainvoke(messages, config=config, **kwargs)
        messages.append(ai_message)
        return {"messages": messages}

    # ------------------------------------------------------------------
    # Batch interface
    # ------------------------------------------------------------------

    def batch(
        self,
        inputs: list[LanguageModelInput | dict[str, Any]],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        r"""Invoke the wrapped chat model on a batch of inputs.

        Unlike the default ``Runnable.batch`` (which fans out ``N``
        separate ``invoke`` calls across a thread pool), this pushes the
        batching down to the wrapped model's own ``batch``/
        ``with_structured_output(...).batch`` method, letting providers
        that support genuine server-side batching (or internal
        ``max_concurrency`` tuning) take advantage of it directly.

        Args:
            inputs: A list of inputs, each following the shapes
                described in the class docstring.
            config: Optional ``RunnableConfig`` (or list of one per
                input) forwarded to the wrapped model's ``batch`` call.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped model's ``batch`` call.

        Returns:
            A list of result dicts, one per input, in the same order as
            ``inputs``. Each dict has the same shape as the one returned
            by :meth:`invoke`.
        """
        all_messages = [self._coerce_input(i) for i in inputs]

        if self._structured_model is not None:
            results = self._structured_model.batch(all_messages, config=config, **kwargs)
            output = []
            for messages, result in zip(all_messages, results, strict=True):
                ai_message: BaseMessage = result["raw"]
                messages.append(ai_message)
                output.append(
                    {
                        "messages": messages,
                        "structured_response": result["parsed"],
                    },
                )
            return output

        ai_messages = self._model.batch(all_messages, config=config, **kwargs)
        return [
            {"messages": [*messages, ai_message]}
            for messages, ai_message in zip(all_messages, ai_messages, strict=True)
        ]

    async def abatch(
        self,
        inputs: list[LanguageModelInput | dict[str, Any]],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        r"""Asynchronously invoke the wrapped chat model on a batch of
        inputs.

        This is the async counterpart of :meth:`batch`; see its
        docstring for details.

        Args:
            inputs: A list of inputs, each following the shapes
                described in the class docstring.
            config: Optional ``RunnableConfig`` (or list of one per
                input) forwarded to the wrapped model's ``abatch`` call.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped model's ``abatch`` call.

        Returns:
            A list of result dicts, one per input, in the same order as
            ``inputs``. Each dict has the same shape as the one returned
            by :meth:`ainvoke`.
        """
        all_messages = [self._coerce_input(i) for i in inputs]

        if self._structured_model is not None:
            results = await self._structured_model.abatch(all_messages, config=config, **kwargs)
            output = []
            for messages, result in zip(all_messages, results, strict=True):
                ai_message: BaseMessage = result["raw"]
                messages.append(ai_message)
                output.append(
                    {
                        "messages": messages,
                        "structured_response": result["parsed"],
                    },
                )
            return output

        ai_messages = await self._model.abatch(all_messages, config=config, **kwargs)
        return [
            {"messages": [*messages, ai_message]}
            for messages, ai_message in zip(all_messages, ai_messages, strict=True)
        ]

    # ------------------------------------------------------------------
    # Streaming interface
    # ------------------------------------------------------------------

    def stream(
        self,
        input: LanguageModelInput | dict[str, Any],  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> Iterator[BaseMessage]:
        r"""Stream the wrapped chat model's response chunk by chunk.

        Unlike :meth:`invoke`, this does **not** return the
        ``{"messages": ...}`` agent shape. It is a thin pass-through to
        the wrapped model's own ``stream`` method: the input is coerced
        to a message list (with the system prompt prepended if
        applicable) and each ``BaseMessage`` chunk produced by the model
        is yielded as-is. The running message history is not
        accumulated or returned.

        Note:
            Structured output (``response_format``) is not supported in
            streaming mode: most providers/parsers need the complete
            response before they can validate/parse it against the
            schema, so this always streams the plain, unstructured
            model output regardless of whether ``response_format`` was
            set at construction time.

        Args:
            input: The input to the model. See the class docstring for
                the accepted shapes (``str``, ``list``, or ``dict`` with
                a ``"messages"`` key).
            config: Optional ``RunnableConfig`` forwarded to the wrapped
                model's ``stream`` call.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped model's ``stream`` call.

        Yields:
            Successive ``BaseMessage`` chunks from the wrapped model.
        """
        messages = self._coerce_input(input)
        yield from self._model.stream(messages, config=config, **kwargs)

    async def astream(
        self,
        input: LanguageModelInput | dict[str, Any],  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[BaseMessage]:
        r"""Asynchronously stream the wrapped chat model's response chunk
        by chunk.

        As with :meth:`stream`, this does not return the
        ``{"messages": ...}`` agent shape, does not accumulate message
        history, and ignores ``response_format`` (structured output is
        not supported in streaming mode).

        Args:
            input: The input to the model. See the class docstring for
                the accepted shapes (``str``, ``list``, or ``dict`` with
                a ``"messages"`` key).
            config: Optional ``RunnableConfig`` forwarded to the wrapped
                model's ``astream`` call.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped model's ``astream`` call.

        Yields:
            Successive ``BaseMessage`` chunks from the wrapped model.
        """
        messages = self._coerce_input(input)
        async for chunk in self._model.astream(messages, config=config, **kwargs):
            yield chunk

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _coerce_input(self, input: LanguageModelInput) -> list[BaseMessage]:  # noqa: A002
        r"""Normalize a flexible input into a list of ``BaseMessage``
        objects, prepending the system prompt if applicable.

        Args:
            input: One of:

                - ``str``: wrapped in a single ``HumanMessage``.
                - ``dict``: the value at key ``"messages"`` (defaulting
                  to ``[]`` if absent) is used, with the same coercion
                  rules as the ``list`` case below.
                - ``list``: used as-is, except that any bare ``str``
                  elements are converted to ``HumanMessage`` objects;
                  elements that are already ``BaseMessage`` instances are
                  left untouched.

        Returns:
            A new list of ``BaseMessage`` objects (never the same list
            object as any list passed in, so callers may safely mutate
            the result). If ``self._system_prompt`` is set and the list
            does not already contain a ``SystemMessage``, a
            ``SystemMessage`` built from ``self._system_prompt`` is
            prepended.

        Raises:
            TypeError: If ``input`` is not a ``str``, ``dict``, or
                ``list``.
        """
        if isinstance(input, str):
            messages: list[BaseMessage] = [HumanMessage(content=input)]
        elif isinstance(input, dict):
            messages = list(input.get("messages", []))
            messages = [HumanMessage(content=m) if isinstance(m, str) else m for m in messages]
        elif isinstance(input, list):
            messages = [HumanMessage(content=m) if isinstance(m, str) else m for m in input]
        else:
            msg = f"Unsupported input type for AgentChatModel: {type(input)}"
            raise TypeError(msg)

        if self._system_prompt and not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=self._system_prompt), *messages]

        return messages
