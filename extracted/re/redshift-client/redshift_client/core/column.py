from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)

from redshift_client.core.data_type.core import (
    DataType,
)
from redshift_client.core.id_objs import (
    ColumnId,
)
from redshift_client.sql_client import (
    DbPrimitive,
)


@dataclass(frozen=True)
class Column:
    data_type: DataType
    nullable: bool
    default: DbPrimitive


@dataclass(frozen=True)
class ColumnObj:
    id_obj: ColumnId
    column: Column


__all__ = [
    "ColumnId",
]
