"""Threading lock object purity patch."""

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from threading import (
    Lock as _Lock,
)
from typing import (
    TypeVar,
)

from fa_purity._core.cmd import (
    Cmd,
    CmdUnwrapper,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class ThreadLock:
    """Lock object for controlling concurrent access."""

    _inner: _Lock

    @staticmethod
    def new() -> Cmd[ThreadLock]:
        """Create a new `ThreadLock`."""
        return Cmd.wrap_impure(lambda: ThreadLock(_Lock()))

    def execute_with_lock(self, cmd: Cmd[_T]) -> Cmd[_T]:
        """
        Execute a cmd in a context lock.

        Create a command that will:
        - acquire the lock
        - execute the command
        - release the lock
        """

        def _action(unwrapper: CmdUnwrapper) -> _T:
            with self._inner:
                return unwrapper.act(cmd)

        return Cmd.new_cmd(_action)

    @property
    def acquire(self) -> Cmd[None]:
        """Command to acquire the lock. It will wait until the lock is acquired."""
        return Cmd.wrap_impure(lambda: self._inner.acquire()).map(lambda _: None)

    @property
    def try_acquire(self) -> Cmd[bool]:
        """Command to try acquiring the lock. Returns False if not acquired."""
        return Cmd.wrap_impure(lambda: self._inner.acquire(False))

    @property
    def release(self) -> Cmd[None]:
        """Command to release the lock."""
        return Cmd.wrap_impure(lambda: self._inner.release()).map(lambda _: None)

    @property
    def locked(self) -> Cmd[bool]:
        """Command to get the status of the lock."""
        return Cmd.wrap_impure(lambda: self._inner.locked())
