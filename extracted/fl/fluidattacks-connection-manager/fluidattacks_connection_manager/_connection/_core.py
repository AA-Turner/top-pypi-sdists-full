from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from fa_purity import Result, ResultE
from fluidattacks_etl_utils.typing import Callable, TypeVar

_T = TypeVar("_T")


def _handle_value_error(process: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(process())
    except ValueError as e:
        return Result.failure(e)


class Databases(Enum):
    OBSERVES = "OBSERVES"

    @staticmethod
    def from_raw(raw: str) -> ResultE[Databases]:
        return _handle_value_error(lambda: Databases(raw))


class Warehouses(Enum):
    GENERIC_COMPUTE = "GENERIC_COMPUTE"

    @staticmethod
    def from_raw(raw: str) -> ResultE[Warehouses]:
        return _handle_value_error(lambda: Warehouses(raw))


class Roles(Enum):
    SORTS = "SORTS"
    ETL_UPLOADER = "ETL_UPLOADER"
    INTEGRATES = "INTEGRATES"
    MIGRATION_UPLOADER = "MIGRATION_UPLOADER"

    @staticmethod
    def from_raw(raw: str) -> ResultE[Roles]:
        return _handle_value_error(lambda: Roles(raw))


@dataclass
class SetupException(Exception):  # noqa: N818
    exception: Exception


@dataclass(frozen=True)
class ConnectionConf:
    warehouse: Warehouses
    role: Roles
    database: Databases
