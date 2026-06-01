from typing import Literal, cast

ListEventsFormatType0 = Literal["CSV", "JSONL"]

LIST_EVENTS_FORMAT_TYPE_0_VALUES: set[ListEventsFormatType0] = {
    "CSV",
    "JSONL",
}


def check_list_events_format_type_0(value: str) -> ListEventsFormatType0:
    if value in LIST_EVENTS_FORMAT_TYPE_0_VALUES:
        return cast(ListEventsFormatType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LIST_EVENTS_FORMAT_TYPE_0_VALUES!r}")
