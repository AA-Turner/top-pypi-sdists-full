"""uniseg database lookup interface. """

from uniseg.db_lookups import columns, index1, index2, shift, values


def get_handle(table_name: str) -> int:
    return columns.index(table_name)


def get_value(h_table: int, key: int, /) -> str:
    index = index1[key >> shift]
    ivalue = index2[(index << shift) + (key & ((1 << shift) - 1))]
    return values[ivalue][h_table]
