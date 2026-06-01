from typing import Literal, cast

ListApiKeysSort = Literal[
    "-created_at",
    "-expires_at",
    "-last_used_at",
    "-name",
    "-status",
    "created_at",
    "expires_at",
    "last_used_at",
    "name",
    "status",
]

LIST_API_KEYS_SORT_VALUES: set[ListApiKeysSort] = {
    "-created_at",
    "-expires_at",
    "-last_used_at",
    "-name",
    "-status",
    "created_at",
    "expires_at",
    "last_used_at",
    "name",
    "status",
}


def check_list_api_keys_sort(value: str) -> ListApiKeysSort:
    if value in LIST_API_KEYS_SORT_VALUES:
        return cast(ListApiKeysSort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_API_KEYS_SORT_VALUES!r}")
