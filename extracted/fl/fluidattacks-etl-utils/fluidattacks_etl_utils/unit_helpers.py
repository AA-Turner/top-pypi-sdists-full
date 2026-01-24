from typing import (
    TypeVar,
)

from fa_purity import Result, UnitType, unit

_F = TypeVar("_F")


def none_to_unit(_: None) -> UnitType:
    return unit


def unit_to_none(_: UnitType) -> None:
    return None


def none_result_to_unit(result: Result[None, _F]) -> Result[UnitType, _F]:
    return result.map(none_to_unit)
