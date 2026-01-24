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
from fa_purity._core.coproduct import Coproduct
from fa_purity._core.maybe import (
    Maybe,
)
from fa_purity._core.pure_iter import (
    PureIter,
)
from fa_purity._core.unsafe import (
    Unsafe,
)

_T = TypeVar("_T")
_L = TypeVar("_L")
_R = TypeVar("_R")


@dataclass(frozen=True)
class PureIterTransform:
    """`PureIter` common transforms."""

    @staticmethod
    def chain(
        unchained: PureIter[PureIter[_T]],
    ) -> PureIter[_T]:
        return unchained.bind(lambda x: x)

    @staticmethod
    def consume(p_iter: PureIter[Cmd[None]]) -> Cmd[None]:
        """
        Define the action of consuming (sequentially) the supplied `PureIter`.

        It consumes from the beginning until the end.
        """

        def _action(unwrapper: CmdUnwrapper) -> None:
            for c in p_iter:
                unwrapper.act(c)

        return Cmd.new_cmd(_action)

    @staticmethod
    def filter_opt(items: PureIter[_T | None]) -> PureIter[_T]:
        """Define a `PureIter` from the supplied one, but removing all `None` elements."""
        return Unsafe.pure_iter_from_cmd(Cmd.wrap_impure(lambda: iter_factory.filter_none(items)))

    @classmethod
    def filter_maybe(cls, items: PureIter[Maybe[_T]]) -> PureIter[_T]:
        """Define a `PureIter` from the supplied one, but removing all empty elements."""
        return cls.filter_opt(items.map(lambda x: x.value_or(None)))

    @staticmethod
    def until_right_injection_inclusive(
        items: PureIter[Coproduct[_L, _R]],
    ) -> PureIter[Coproduct[_L, _R]]:
        """
        Define a `PureIter` from the supplied one, but ending at the first right injected object.

        The final right injected object is also returned.
        """
        return Unsafe.pure_iter_from_cmd(
            Cmd.wrap_impure(lambda: iter_factory.until_right_injection_inclusive(items)),
        )

    @staticmethod
    def until_right_injection_exclusive(items: PureIter[Coproduct[_L, _R]]) -> PureIter[_L]:
        """
        Define a `PureIter` from the supplied one, but ending at the first right injected object.

        The final right injected object is NOT returned.
        """
        return Unsafe.pure_iter_from_cmd(
            Cmd.wrap_impure(lambda: iter_factory.until_right_injection_exclusive(items)),
        )

    @classmethod
    def until_none(cls, items: PureIter[_T | None]) -> PureIter[_T]:
        def _to_coproduct(item: _T | None) -> Coproduct[_T, None]:
            if item is None:
                return Coproduct.inr(item)
            return Coproduct.inl(item)

        return cls.until_right_injection_exclusive(items.map(_to_coproduct))

    @classmethod
    def until_empty(cls, items: PureIter[Maybe[_T]]) -> PureIter[_T]:
        return cls.until_none(items.map(lambda m: m.value_or(None)))
