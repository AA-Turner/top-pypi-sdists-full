from __future__ import (
    annotations,
)

import sys
from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    NoReturn,
    TypeVar,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Cmd(Generic[_A]):
    """
    Impure commands type.

    Equivalent to haskell IO type.
    This type handles impure commands without executing them.
    """

    _value: Callable[[], _A]  # not a pure function!

    @staticmethod
    def wrap_impure(value: Callable[[], _A]) -> Cmd[_A]:
        """Build a `Cmd` from an impure procedure."""
        return Cmd(value)

    @staticmethod
    def wrap_value(value: _A) -> Cmd[_A]:
        """Build a `Cmd` from a value."""
        return Cmd(lambda: value)

    @staticmethod
    def new_cmd(action: Callable[[CmdUnwrapper], _A]) -> Cmd[_A]:
        """Build a `Cmd` from an action context i.e. `Cmd` can be executed in the context."""
        return Cmd(lambda: action(_unwrapper))

    def map(self, function: Callable[[_A], _B]) -> Cmd[_B]:
        """
        Apply a function to a `Cmd`.

        Outputs a new procedure that when computed will:
        - execute the command
        - apply the supplied function to the result
        """
        return Cmd(lambda: function(self._value()))

    def bind(self, function: Callable[[_A], Cmd[_B]]) -> Cmd[_B]:
        """
        Chain a command with the current one.

        Outputs a new procedure that when computed will:
        - execute the current command
        - apply the supplied function to the result
        - execute the resulting command
        """
        return Cmd(lambda: function(self._value()).execute(_Private()))

    def apply(self, wrapped: Cmd[Callable[[_A], _B]]) -> Cmd[_B]:
        return wrapped.bind(lambda f: self.map(f))

    def compute(self) -> NoReturn:
        """
        Execute the command.

        - this should be the last thing the program will do
        """
        self._value()
        sys.exit(0)

    def execute(self, _: _Private) -> _A:
        """Private-method. Do not call this method, only for authorized functions."""
        return self._value()

    def __add__(self, other: Cmd[_B]) -> Cmd[_B]:
        return self.bind(lambda _: other)

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({id(self._value)})"


@dataclass(frozen=True)
class CmdUnwrapper:
    """
    Object that allows cmd execution.

    Instances can not be created by the user by design.
    Only through the `Cmd.new_cmd` the user can use an
    instance of this type.
    """

    # Do not build any public constructors or instances
    # This obj is only accessible in the action context through the `new_cmd` builder
    _inner: _Private = field(repr=False, hash=False, compare=False)

    def act(self, action: Cmd[_A]) -> _A:
        """
        [WARNING] Not a pure function.

        This method is more safe than `unsafe_unwrap` since it
        wraps the result into another `Cmd`, but is possible to
        use it incorrectly in places where a pure function is
        expected e.g. `PureIter.map` and cause unexpected bugs.
        """
        return action.execute(_Private())


_unwrapper = CmdUnwrapper(_Private())


def unsafe_unwrap(action: Cmd[_A]) -> _A:
    return action.execute(_Private())
