from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class UnitType:
    """
    Alternative to `None`.

    The main issue with `None` is that its type definition is not clear,
    `NoneType` was introduced and removed from typings.
    To patch it, `UnitType` is the type and `UnitType()` or `unit` is the instance.
    """

    def __str__(self) -> str:
        return "unit"

    def __repr__(self) -> str:
        return str(self)


unit: UnitType = UnitType()
