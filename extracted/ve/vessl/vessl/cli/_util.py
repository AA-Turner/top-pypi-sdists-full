from datetime import datetime
from typing import Any, Callable, Dict, List, Union

import click
from tabulate import tabulate
from terminaltables import AsciiTable

from openapi_client.models import StorageFile
from vessl.util.fmt import format_key, format_data, format_size, format_bool

UNDEFINED = click.style("undefined", fg="red")


def print_table(objects: List[Any], keys: List[str], data_func: Callable, **kwargs) -> None:
    table_data = [[format_key(x) for x in keys]]
    table_data.extend(data_func(x) for x in objects)

    table = AsciiTable(table_data)
    table.inner_column_border = kwargs.get("inner_column_border", False)
    table.inner_heading_row_border = kwargs.get("inner_heading_row_border", False)
    table.inner_footing_row_border = kwargs.get("inner_footing_row_border", False)
    table.outer_border = kwargs.get("outer_border", False)

    print(table.table)

def print_table_tabulate(objects: List[dict]) -> None:
    print(tabulate(objects, headers="keys", tablefmt="grid"))


def print_data(data: Dict[str, Any]) -> None:
    lines = format_data(data, 0)
    print("\n".join(lines))


def print_logs(logs: List[Any]):
    timezone = datetime.now().astimezone().tzinfo
    for log in logs:
        ts = datetime.fromtimestamp(log.timestamp, tz=timezone).strftime("%H:%M:%S.%f")
        message = log.message.replace("\\r", "\n").replace("\\n", "\n")
        for x in message.split("\n"):
            print(f"[{ts}] {x}")


def truncate_datetime(value: datetime) -> Union[str, datetime]:
    if not value:
        return UNDEFINED
    return value.replace(microsecond=0)


def print_volume_files(
    files: List[StorageFile],
    keys: List[str] = None,
    data_func: Callable = None,
    **kwargs,
) -> None:
    """Print volume files

    Separately defined as a util function because it is used often across many files.
    TODO: Support recursive. Add Sort? Parse paths?
    """

    if keys is None:
        keys = ["Path", "Dir", "Size"]

    if data_func is None:
        data_func = lambda x: [
            x.path,
            format_bool(x.is_dir),
            format_size(x.size) if not x.is_dir else "-",
        ]

    print_table(files, keys, data_func)


