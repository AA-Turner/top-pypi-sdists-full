from __future__ import (
    annotations,
)

import logging
import subprocess
from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from subprocess import (
    Popen,
)
from typing import (
    IO,
    Generic,
    TypeVar,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Maybe,
    PureIterFactory,
    Result,
    ResultFactory,
)

LOG = logging.getLogger(__name__)
_A = TypeVar("_A", bytes, str)


class StdValues(Enum):
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL


class Stdout(Enum):
    STDOUT = subprocess.STDOUT


@dataclass(frozen=True)
class Subprocess(Generic[_A]):
    args: FrozenList[str]
    stdin: StdValues | IO[_A] | None
    stdout: StdValues | IO[_A] | None
    stderr: StdValues | Stdout | IO[_A] | None
    env: FrozenDict[str, str]


def _normalize(
    item: StdValues | Stdout | IO[_A] | None,
) -> int | IO[_A] | None:
    if isinstance(item, StdValues):
        return item.value
    if isinstance(item, Stdout):
        return item.value
    return item


@dataclass(frozen=True)
class RunningSubprocess(Generic[_A]):
    _process: Popen[_A]
    stdin: IO[_A] | None
    stdout: IO[_A] | None
    stderr: IO[_A] | None

    @staticmethod
    def run_bin_mode(item: Subprocess[bytes]) -> Cmd[RunningSubprocess[bytes]]:
        def _action() -> RunningSubprocess[bytes]:
            process = Popen(  # noqa: S603
                # Should be refactored
                item.args,
                stdin=_normalize(item.stdin),
                stdout=_normalize(item.stdout),
                stderr=_normalize(item.stderr),
                env=dict(item.env),
            )
            return RunningSubprocess(process, process.stdin, process.stdout, process.stderr)

        return Cmd.wrap_impure(_action)

    @staticmethod
    def run_universal_newlines(
        item: Subprocess[str],
    ) -> Cmd[RunningSubprocess[str]]:
        def _action() -> RunningSubprocess[str]:
            process = Popen(  # noqa: S603
                # Should be refactored
                item.args,
                stdin=_normalize(item.stdin),
                stdout=_normalize(item.stdout),
                stderr=_normalize(item.stderr),
                universal_newlines=True,
                env=dict(item.env),
            )
            return RunningSubprocess(process, process.stdin, process.stdout, process.stderr)

        return Cmd.wrap_impure(_action)

    def poll(self) -> Cmd[int | None]:
        return Cmd.wrap_impure(self._process.poll)

    def wait(self, timeout: float | None) -> Cmd[int]:
        return Cmd.wrap_impure(lambda: self._process.wait(timeout))

    def wait_result(self, timeout: float | None) -> Cmd[Result[None, Exception]]:
        factory: ResultFactory[None, Exception] = ResultFactory()
        return self.wait(timeout).map(
            lambda c: factory.success(None)
            if c == 0
            else factory.failure(Exception(f"Process ended with return code: {c} i.e. {self}")),
        )


def pipe(
    run: Callable[[Subprocess[_A]], Cmd[RunningSubprocess[_A]]],
    cmds: FrozenList[Subprocess[_A]],
) -> Maybe[Cmd[RunningSubprocess[_A]]]:
    """
    Commands that will be piped.

    i.e. `cmd_1 | cmd_2 | cmd_3 ...`.
    """

    def _chain(
        previous: Cmd[RunningSubprocess[_A]] | None,
        current: Subprocess[_A],
    ) -> Cmd[RunningSubprocess[_A]]:
        if previous is None:
            return run(
                Subprocess(
                    current.args,
                    None,
                    StdValues.PIPE,
                    current.stderr,
                    current.env,
                ),
            )
        return previous.map(
            lambda r: Subprocess(
                current.args,
                r.stdout,
                StdValues.PIPE,
                current.stderr,
                current.env,
            ),
        ).bind(run)

    result = PureIterFactory.from_list(cmds).reduce(_chain, None)
    return Maybe.from_optional(result)
