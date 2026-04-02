from typing import Iterable


def join_as_string(values: Iterable[str], delimiter: str = ","):
    return delimiter.join(map(lambda addr: f"'{addr}'", values))
