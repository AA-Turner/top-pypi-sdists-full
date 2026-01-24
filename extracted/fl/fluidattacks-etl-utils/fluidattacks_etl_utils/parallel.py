from __future__ import (
    annotations,
)

from collections.abc import (
    Iterable,
)
from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
    cast,
)

from fa_purity import (
    Cmd,
    CmdUnwrapper,
    FrozenList,
    PureIter,
    Stream,
    StreamTransform,
    Unsafe,
)
from pathos.pp import ParallelPool  # type: ignore[import-untyped]
from pathos.threading import (  # type: ignore[import-untyped]
    ThreadPool as _RawThreadPool,
)

_T = TypeVar("_T")


@dataclass(frozen=True)  # type: ignore[misc]
class _ThreadPool:  # type: ignore[no-any-unimported]
    pool: _RawThreadPool  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ThreadPool:
    _inner: _ThreadPool

    @staticmethod
    def new(nodes: int) -> Cmd[ThreadPool]:
        return Cmd.wrap_impure(
            lambda: ThreadPool(_ThreadPool(_RawThreadPool(nodes=nodes))),  # type: ignore[misc]
        )

    def in_threads(self, commands: PureIter[Cmd[_T]] | Stream[Cmd[_T]]) -> Stream[_T]:
        def _action(unwrapper: CmdUnwrapper) -> Iterable[_T]:
            def _iter_obj() -> Iterable[Cmd[_T]]:
                if isinstance(commands, PureIter):
                    return commands
                return unwrapper.act(Unsafe.stream_to_iter(commands))

            results: Iterable[_T] = cast(
                "Iterable[_T]",
                self._inner.pool.imap(  # type: ignore[misc]
                    lambda c: unwrapper.act(c),  # type: ignore[misc]
                    _iter_obj(),
                ),
            )
            yield from results

        return Unsafe.stream_from_cmd(Cmd.new_cmd(_action))

    def in_threads_none(self, commands: PureIter[Cmd[None]] | Stream[Cmd[None]]) -> Cmd[None]:
        return StreamTransform.consume(self.in_threads(commands).map(lambda n: Cmd.wrap_value(n)))


def parallel_cmds(cmds: FrozenList[Cmd[_T]], nodes: int | None) -> Cmd[FrozenList[_T]]:
    def _action(unwrapper: CmdUnwrapper) -> FrozenList[_T]:
        pool = ParallelPool(nodes=nodes) if nodes else ParallelPool()  # type: ignore[misc]
        return cast(
            "FrozenList[_T]",
            tuple(pool.map(unwrapper.act, cmds)),  # type: ignore[misc]
        )

    return Cmd.new_cmd(_action)
