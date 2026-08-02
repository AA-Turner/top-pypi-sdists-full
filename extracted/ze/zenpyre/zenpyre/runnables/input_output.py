r"""Provide a runnable wrapper that pairs a runnable's input with its
output."""

from __future__ import annotations

__all__ = ["InputOutputRunnable"]

from typing import Any, Generic

from langchain_core.runnables import Runnable, RunnableConfig

from zenpyre.runnables.utils import Input, InputOutputPair, Output


class InputOutputRunnable(Runnable[Input, InputOutputPair[Input, Output]], Generic[Input, Output]):
    r"""Wrap a runnable so invoking it returns an
    :class:`InputOutputPair` of its input and output, instead of just
    the output.

    This is useful whenever downstream code needs to know which input
    produced a given output -- e.g. logging, evaluation harnesses, or
    building a dataset of (input, output) examples -- without having to
    thread the input through the wrapped runnable itself or zip inputs
    and outputs back together by hand afterwards.

    ``.batch()``/``.abatch()`` delegate to the wrapped runnable's own
    batch/abatch implementation (rather than falling back to the
    default per-item ``invoke`` loop that :class:`Runnable` provides),
    so any batching optimizations the inner runnable implements (e.g.
    batched LLM calls) are preserved. When ``return_exceptions=True``
    and a given input's call fails, the corresponding entry in the
    returned list is the raw exception, not an :class:`InputOutputPair`
    -- exactly as :meth:`Runnable.batch` behaves for the wrapped
    runnable itself.

    Args:
        runnable: The runnable to wrap.

    Example:
        ```pycon
        >>> from langchain_core.runnables import RunnableLambda
        >>> from zenpyre.runnables import InputOutputRunnable
        >>> inner = RunnableLambda(lambda x: x.upper())
        >>> wrapped = InputOutputRunnable(inner)
        >>> result = wrapped.invoke("hello")
        >>> result.input
        'hello'
        >>> result.output
        'HELLO'
        >>> [pair.output for pair in wrapped.batch(["a", "b"])]
        ['A', 'B']

        ```
    """

    def __init__(self, runnable: Runnable[Input, Output]) -> None:
        self._runnable = runnable

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self._runnable!r})"

    def invoke(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> InputOutputPair[Input, Output]:
        output = self._runnable.invoke(input, config=config, **kwargs)
        return InputOutputPair(input=input, output=output)

    async def ainvoke(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> InputOutputPair[Input, Output]:
        output = await self._runnable.ainvoke(input, config=config, **kwargs)
        return InputOutputPair(input=input, output=output)

    def batch(
        self,
        inputs: list[Input],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Any | None,
    ) -> list[InputOutputPair[Input, Output] | BaseException]:
        outputs = self._runnable.batch(
            inputs, config=config, return_exceptions=return_exceptions, **kwargs
        )
        return [
            (
                output
                if return_exceptions and isinstance(output, BaseException)
                else InputOutputPair(input=inp, output=output)
            )
            for inp, output in zip(inputs, outputs, strict=True)
        ]

    async def abatch(
        self,
        inputs: list[Input],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Any | None,
    ) -> list[InputOutputPair[Input, Output] | BaseException]:
        outputs = await self._runnable.abatch(
            inputs, config=config, return_exceptions=return_exceptions, **kwargs
        )
        return [
            (
                output
                if return_exceptions and isinstance(output, BaseException)
                else InputOutputPair(input=inp, output=output)
            )
            for inp, output in zip(inputs, outputs, strict=True)
        ]
