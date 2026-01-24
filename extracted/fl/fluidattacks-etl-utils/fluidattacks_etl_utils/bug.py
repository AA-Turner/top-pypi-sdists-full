from __future__ import (
    annotations,
)

import inspect
import sys
from dataclasses import (
    dataclass,
)
from types import (
    FrameType,
)
from typing import (
    Generic,
    NoReturn,
    TypeVar,
)

from fa_purity import (
    FrozenList,
    Result,
)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


def _frame_location(frame: FrameType | None) -> str:
    if frame is not None:
        return str(inspect.getframeinfo(frame))
    return "?? Unknown ??"


@dataclass
class Bug(Exception, Generic[_T]):
    obj_id: str
    location: str
    parent_error: _T | None
    context: FrozenList[str]

    def explode(self) -> NoReturn:
        sys.tracebacklimit = 0
        raise self

    @staticmethod
    def new(
        name: str,
        location: FrameType | None,
        parent_error: _T | None,
        context: FrozenList[str],
    ) -> Bug[_T]:
        return Bug(
            name,
            _frame_location(location),
            parent_error,
            context,
        )

    @classmethod
    def assume_success(
        cls,
        name: str,
        location: FrameType | None,
        context: FrozenList[str],
        result: Result[_S, _F],
    ) -> _S:
        return (
            result.alt(
                lambda e: Bug.new(
                    name,
                    location,
                    e,
                    context,
                ),
            )
            .alt(lambda e: e.explode())
            .to_union()
        )

    def __str__(self) -> str:
        """Str representation of Bug."""
        return (
            "\n"
            + "-" * 30
            + "\n [Id] "
            + self.obj_id
            + "\n [Location] "
            + self.location
            + "\n [Error] "
            + str(self.parent_error)
            + "\n [Context] "
            + str(self.context)
        )
