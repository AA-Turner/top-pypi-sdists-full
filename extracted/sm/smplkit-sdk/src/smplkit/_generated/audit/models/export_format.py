from typing import Literal, cast

ExportFormat = Literal["CSV", "JSONL"]

EXPORT_FORMAT_VALUES: set[ExportFormat] = {
    "CSV",
    "JSONL",
}


def check_export_format(value: str) -> ExportFormat:
    if value in EXPORT_FORMAT_VALUES:
        return cast(ExportFormat, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EXPORT_FORMAT_VALUES!r}")
