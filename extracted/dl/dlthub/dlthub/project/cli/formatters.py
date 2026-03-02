"""Utility functions for outputting from cli commands."""

from typing import List

from dlt._workspace.cli import echo as fmt


def print_entity_list(entity_name: str, entity_list: List[str], note: str = "") -> None:
    if not entity_list:
        fmt.echo(
            f"No {entity_name}s found in project. Run the `dlt {entity_name} add` "
            + "command to add one."
        )
    else:
        fmt.echo(f"Found {len(entity_list)} {entity_name}(s) in project:")
        for entity in entity_list:
            fmt.echo(" * %s" % entity)

    if note:
        fmt.echo(note)
