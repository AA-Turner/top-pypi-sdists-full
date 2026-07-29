"""Output formats for command results: json, yaml and table."""
from enum import Enum
import json
from typing import Any, Optional, Sequence

import click
import tabulate
import yaml

from anyscale.util import AnyscaleJSONEncoder


class OutputFormat(str, Enum):
    """Supported output formats for a command's result."""

    JSON = "json"
    YAML = "yaml"
    TABLE = "table"
    TEXT = "text"

    def render(self, data: Any, columns: Optional[Sequence[str]] = None) -> str:
        """Render a JSON-safe value in this format. TEXT has no structured renderer."""
        plain = _to_plain(data)
        if self is OutputFormat.JSON:
            return json.dumps(plain, indent=4, cls=AnyscaleJSONEncoder, allow_nan=False)
        if self is OutputFormat.YAML:
            return yaml.dump(plain, sort_keys=False).rstrip("\n")
        if self is OutputFormat.TABLE:
            return _render_table(plain, columns)
        raise ValueError(f"{self.value!r} has no structured renderer")


# CLI flags that select an output format, e.g. -o json.
OUTPUT_FLAG = "-o"
OUTPUT_FLAG_LONG = "--output"


def render_output(
    data: Any, output_format: str, table_columns: Optional[Sequence[str]] = None,
) -> str:
    """Render data as a string in output_format (json, yaml or table)."""
    try:
        return OutputFormat(output_format).render(data, table_columns)
    except ValueError as err:
        raise click.ClickException(str(err)) from None


def print_output(
    data: Any, output_format: str, table_columns: Optional[Sequence[str]] = None,
) -> None:
    """Render data in output_format and write it to stdout."""
    click.echo(render_output(data, output_format, table_columns))


def resolve_output_format(output_format: str, json_output: bool = False) -> str:
    """Resolve the effective format from -o and the legacy --json flag.

    TEXT is the default, legacy output of all commands.
    A structured -o value wins over --json, and --json wins over text.
    """
    if output_format != OutputFormat.TEXT.value:
        return output_format
    if json_output:
        return OutputFormat.JSON.value
    return OutputFormat.TEXT.value


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _render_table(data: Any, columns: Optional[Sequence[str]]) -> str:
    rows = data if isinstance(data, list) else [data]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Table output requires a dict or a list of dicts.")
    cols = list(columns) if columns else (list(rows[0]) if rows else [])
    headers = [col.upper() for col in cols]
    body = [[row.get(col) for col in cols] for row in rows]
    return tabulate.tabulate(body, headers=headers, tablefmt="plain", missingval="")


def _to_plain(data: Any) -> Any:
    """Convert model instances (anything with ``to_dict``) into plain dict/list."""
    if callable(getattr(data, "to_dict", None)):
        return _to_plain(data.to_dict())
    if isinstance(data, dict):
        return {key: _to_plain(value) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [_to_plain(item) for item in data]
    return data
