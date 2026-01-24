from __future__ import (
    annotations,
)

from collections.abc import Callable
from typing import (
    TypeVar,
)

from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    PureIterFactory,
    Stream,
    StreamFactory,
    StreamTransform,
)

_Page = TypeVar("_Page")
_T = TypeVar("_T")


def cursor_pagination(
    get_page: Callable[[Maybe[_Page]], Cmd[tuple[FrozenList[_T], Maybe[_Page]]]],
) -> Stream[FrozenList[_T]]:
    end_value: tuple[FrozenList[_T], Maybe[_Page]] = (
        (),
        Maybe.empty(),
    )

    def _generator(
        prev: Cmd[tuple[FrozenList[_T], Maybe[_Page]]],
    ) -> Cmd[tuple[FrozenList[_T], Maybe[_Page]]]:
        return prev.bind(
            lambda p_obj: p_obj[1]
            .map(
                lambda p: get_page(Maybe.some(p)),
            )
            .value_or(Cmd.wrap_value(end_value)),
        )

    def _end_filter(
        item: tuple[FrozenList[_T], Maybe[_Page]],
    ) -> Maybe[tuple[FrozenList[_T], Maybe[_Page]]]:
        return Maybe.empty() if item == end_value else Maybe.some(item)

    return (
        StreamFactory.from_commands(
            PureIterFactory.infinite_gen(_generator, get_page(Maybe.empty())),
        )
        .map(lambda t: _end_filter(t))
        .transform(StreamTransform.until_empty)
        .map(lambda t: t[0])
    )
