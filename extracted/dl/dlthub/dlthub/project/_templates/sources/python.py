"""The Python Source Template is a good starting point for implementing a python based source."""

from typing import Iterator

import random

import dlt

from dlt.sources import DltResource, TDataItems

names = ["tom", "jerry", "bob", "alice", "john", "jane", "jim", "jill", "jack", "jenny"]


def create_example_python_list(row_count: int) -> Iterator[TDataItems]:
    for i in range(row_count):
        yield {"id": row_count, "name": random.choice(names), "age": random.randint(18, 65)}


@dlt.source
def source(row_count: int = dlt.config.value, some_secret: int = dlt.secrets.value) -> DltResource:
    """Example arrow source"""

    # if no row count is provided or row_count is 0, use default value
    if not row_count:
        row_count = 100

    @dlt.resource(
        primary_key="id",
    )
    def items() -> Iterator[TDataItems]:
        yield from create_example_python_list(row_count)

    return items
