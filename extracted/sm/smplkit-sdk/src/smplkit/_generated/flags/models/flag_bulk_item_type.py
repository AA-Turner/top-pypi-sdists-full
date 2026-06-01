from typing import Literal, cast

FlagBulkItemType = Literal["BOOLEAN", "JSON", "NUMERIC", "STRING"]

FLAG_BULK_ITEM_TYPE_VALUES: set[FlagBulkItemType] = {
    "BOOLEAN",
    "JSON",
    "NUMERIC",
    "STRING",
}


def check_flag_bulk_item_type(value: str) -> FlagBulkItemType:
    if value in FLAG_BULK_ITEM_TYPE_VALUES:
        return cast(FlagBulkItemType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {FLAG_BULK_ITEM_TYPE_VALUES!r}")
