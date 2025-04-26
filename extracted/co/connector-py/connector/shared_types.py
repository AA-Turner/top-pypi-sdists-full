import typing as t

RawDataType: t.TypeAlias = dict[
    str,  # url
    dict[str, t.Any] | None,  # response body, can be None with some responses
]
OptionalRawDataType = RawDataType | None


__all__ = ("RawDataType",)
