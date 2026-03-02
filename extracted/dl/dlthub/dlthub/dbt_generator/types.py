from typing import Sequence

from dlt.common.typing import TypedDict


class TableReference(TypedDict, total=False):
    columns: Sequence[str]
    referenced_table: str
    referenced_columns: Sequence[str]
