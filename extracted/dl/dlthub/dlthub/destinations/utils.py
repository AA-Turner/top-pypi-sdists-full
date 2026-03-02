from dlt.common.schema.typing import TTableSchema
from dlt.common.schema.utils import get_dedup_sort_tuple


def get_dedup_sort_order_by_sql(table_schema: TTableSchema) -> str:
    dedup_sort = get_dedup_sort_tuple(table_schema)
    if dedup_sort is None:
        return "(SELECT NULL)"
    else:
        return f"{dedup_sort[0]} {dedup_sort[1].upper()}"
