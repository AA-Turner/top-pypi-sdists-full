from collections.abc import Callable, Iterable
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
    CmdUnwrapper,
)
from fa_purity._core.maybe import (
    Maybe,
)
from fa_purity._core.pure_iter import (
    PureIter,
)
from fa_purity._core.utils import (
    raise_exception,
)

from ._core import (
    Stream,
    unsafe_from_cmd,
)

_T = TypeVar("_T")
_S = TypeVar("_S")


@dataclass(frozen=True)
class StreamFactory:
    @staticmethod
    def from_commands(piter: PureIter[Cmd[_T]]) -> Stream[_T]:
        return unsafe_from_cmd(iter_factory.squash(piter))

    @staticmethod
    def generate(
        get: Callable[[_S], Cmd[_T]],
        extract: Callable[[_T], Maybe[_S]],
        init: _S,
    ) -> Stream[_T]:
        """
        Generate a `Stream` from a command that depends on a previous state.

        - `get` = the command that depends on a previous state
        - `extract` = how to derive the state from the result of the previous command.
            This also determines the stream end when returning empty.
        - `init` = initial state value

        """

        def _iter(unwrapper: CmdUnwrapper) -> Iterable[_T]:
            state: Maybe[_S] = Maybe.some(init)
            while state.map(lambda _: True).value_or(False):
                item = unwrapper.act(
                    get(state.or_else_call(lambda: raise_exception(ValueError("Empty")))),
                )
                yield item
                state = extract(item)

        return unsafe_from_cmd(Cmd.new_cmd(_iter))
