"""Common transforms utils/module over core types."""

from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from typing import (
    TypeVar,
)

from fa_purity._core.cmd import (
    Cmd,
    CmdUnwrapper,
)
from fa_purity._core.coproduct import Coproduct, CoproductFactory
from fa_purity._core.frozen import (
    FrozenList,
    NewFrozenList,
)
from fa_purity._core.pure_iter import PureIterFactory
from fa_purity._core.result import (
    Result,
    ResultFactory,
)
from fa_purity._core.unit import UnitType

_A = TypeVar("_A")
_B = TypeVar("_B")
_S = TypeVar("_S")
_F = TypeVar("_F")

Mapper = Callable[[Callable[[_A], _B], FrozenList[_A]], FrozenList[_B]]


@dataclass(frozen=True)
class CmdTransform:
    """Transform utils for `Cmd` instances."""

    @staticmethod
    def serial_merge(items: FrozenList[Cmd[_A]]) -> Cmd[FrozenList[_A]]:
        """
        Create a serial execution of commands.

        Create a new command that will execute the supplied commands
        in sequential order when computed.
        """

        def _action(unwrapper: CmdUnwrapper) -> FrozenList[_A]:
            return tuple(map(unwrapper.act, items))

        return Cmd.new_cmd(_action)

    @staticmethod
    def chain_cmd_result(
        cmd_1: Cmd[Result[_S, _F]],
        cmd_2: Callable[[_S], Cmd[Result[_A, _B]]],
    ) -> Cmd[Result[_A, Coproduct[_F, _B]]]:
        """
        Chain two cmd results.

        The resulting command will:
        - execute first command
        - if success: execute cmd_2 with the success value and return the result
        - if failure: return the result of cmd_1
        """
        factory: ResultFactory[_A, Coproduct[_F, _B]] = ResultFactory()
        factory_2: CoproductFactory[_F, _B] = CoproductFactory()
        return cmd_1.bind(
            lambda r: r.to_coproduct().map(
                lambda s: cmd_2(s).map(lambda r: r.alt(factory_2.inr)),
                lambda f: Cmd.wrap_value(factory.failure(factory_2.inl(f))),
            ),
        )

    @staticmethod
    def all_cmds_ok(
        cmd_1: Cmd[Result[UnitType, _F]],
        cmds: NewFrozenList[Cmd[Result[UnitType, _F]]],
    ) -> Cmd[Result[UnitType, _F]]:
        """
        Chain a (non-empty) list of trivial success output commands.

        The resulting command will:
        - execute each command serially until someone returns a failure
        - the commands after the failure will not be executed

        [WARNING] even when a failure is present, all the cmd list is iterated
        """
        return PureIterFactory.from_list(cmds.items).reduce(
            lambda p, c: p.bind(
                lambda r: r.to_coproduct().map(
                    lambda _: c,
                    lambda f: Cmd.wrap_value(Result.failure(f)),
                ),
            ),
            cmd_1,
        )
