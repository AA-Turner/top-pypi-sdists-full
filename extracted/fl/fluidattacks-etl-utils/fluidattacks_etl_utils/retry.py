import logging
from collections.abc import Callable
from time import (
    sleep,
)
from typing import (
    TypeVar,
)

from fa_purity import (
    Cmd,
    PureIterFactory,
    Result,
    StreamFactory,
    UnitType,
    Unsafe,
)

from fluidattacks_etl_utils.typing import none_to_unit

LOG = logging.getLogger(__name__)
_S = TypeVar("_S")
_F = TypeVar("_F")


class MaxRetriesReached(Exception):
    pass


def retry_cmd(
    cmd: Cmd[Result[_S, _F]],
    next_cmd: Callable[[int, Result[_S, _F]], Cmd[Result[_S, _F]]],
    max_retries: int,
) -> Cmd[Result[_S, MaxRetriesReached]]:
    cmds = PureIterFactory.from_range(range(max_retries + 1)).map(
        lambda i: cmd.bind(
            lambda r: next_cmd(i + 1, r) if i + 1 <= max_retries else Cmd.wrap_value(r),
        ),
    )
    return (
        StreamFactory.from_commands(cmds)
        .find_first(lambda x: x.map(lambda _: True).alt(lambda _: False).to_union())
        .map(
            lambda x: x.map(
                lambda r: r.alt(
                    lambda _: Unsafe.raise_exception(
                        ValueError("first found item should be a success"),
                    ),
                ).to_union(),
            )
            .to_result()
            .alt(lambda _: MaxRetriesReached(max_retries)),
        )
    )


def cmd_if_fail_2(
    result: Result[_S, _F],
    cmd: Callable[[_F], Cmd[UnitType]],
) -> Cmd[Result[_S, _F]]:
    def _cmd(err: _F) -> Cmd[Result[_S, _F]]:
        fail: Result[_S, _F] = Result.failure(err)
        return cmd(err).map(lambda _: fail)

    return result.map(lambda _: Cmd.wrap_value(result)).alt(_cmd).to_union()


def cmd_if_fail(
    result: Result[_S, _F],
    cmd: Cmd[None],
) -> Cmd[Result[_S, _F]]:
    return cmd_if_fail_2(result, lambda _: cmd.map(none_to_unit))


def sleep_cmd(delay: float) -> Cmd[None]:
    return Cmd.wrap_impure(lambda: sleep(delay))


def sleep_cmd_2(delay: float) -> Cmd[UnitType]:
    return sleep_cmd(delay).map(none_to_unit)
