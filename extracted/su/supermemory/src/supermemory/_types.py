"""The 3.x `NOT_GIVEN` sentinel: "option not supplied", distinct from an explicit `None`."""

from __future__ import annotations

from typing import Literal


class NotGiven:
    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()
not_given = NOT_GIVEN

__all__ = ["NOT_GIVEN", "NotGiven", "not_given"]
