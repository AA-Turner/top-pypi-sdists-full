from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

from fa_purity._core import (
    iter_factory,
)
from fa_purity._core.cmd import (
    Cmd,
)
from fa_purity._core.maybe import (
    Maybe,
)
from fa_purity._core.pure_iter import (
    PureIter,
)
from fa_purity._core.stream import (
    Stream,
    StreamFactory,
)
from fa_purity._core.unsafe import (
    Unsafe,
)

_T = TypeVar("_T")


def _chain_1(
    unchained: Stream[PureIter[_T]],
) -> Stream[_T]:
    return unchained.map(
        lambda p: p.map(lambda x: Cmd.wrap_impure(lambda: x)).transform(
            lambda x: StreamFactory.from_commands(x),
        ),
    ).bind(lambda x: x)


def _chain_2(
    unchained: PureIter[Stream[_T]],
) -> Stream[_T]:
    return (
        unchained.map(lambda s: Cmd.wrap_impure(lambda: s))
        .transform(lambda x: StreamFactory.from_commands(x))
        .bind(lambda x: x)
    )


@dataclass(frozen=True)
class StreamTransform:
    @staticmethod
    def chain(
        unchained: Stream[PureIter[_T]] | PureIter[Stream[_T]],
    ) -> Stream[_T]:
        if isinstance(unchained, Stream):
            return _chain_1(unchained)
        return _chain_2(unchained)

    @staticmethod
    def squash(stm: Stream[Cmd[_T]]) -> Stream[_T]:
        return Unsafe.stream_from_cmd(Unsafe.stream_to_iter(stm).bind(iter_factory.squash))

    @staticmethod
    def consume(stm: Stream[Cmd[None]]) -> Cmd[None]:
        return Cmd.wrap_impure(
            lambda: iter_factory.deque(
                iter(Unsafe.compute(a) for a in Unsafe.compute(Unsafe.stream_to_iter(stm))),
            ),
        )

    @staticmethod
    def filter_opt(stm: Stream[_T | None]) -> Stream[_T]:
        return Unsafe.stream_from_cmd(Unsafe.stream_to_iter(stm).map(iter_factory.filter_none))

    @classmethod
    def filter_maybe(cls, stm: Stream[Maybe[_T]]) -> Stream[_T]:
        return cls.filter_opt(stm.map(lambda x: x.value_or(None)))

    @staticmethod
    def until_none(stm: Stream[_T | None]) -> Stream[_T]:
        return Unsafe.stream_from_cmd(Unsafe.stream_to_iter(stm).map(iter_factory.until_none))

    @classmethod
    def until_empty(cls, stm: Stream[Maybe[_T]]) -> Stream[_T]:
        return cls.until_none(stm.map(lambda m: m.value_or(None)))
