from typing import TypedDict


class Parameters(TypedDict):
    query: dict[str, str | list[str]]
    path: dict[str, str]
