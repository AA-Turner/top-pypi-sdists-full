from __future__ import annotations

from collections.abc import Sequence

from ..client import Client
from .save_load.commands import SaveLoad
from .state.filters import TableFilters
from .state.machine import StateMachine


def _split_names(value: str | Sequence[str] | None) -> tuple[str, ...]:
    """Split a comma-separated flag value, dropping blanks.

    Fire passes comma-separated flag values (e.g. ``--schemas a,b``) to the
    method as a tuple, so both forms must be accepted.
    """
    if not value:
        return ()
    if isinstance(value, str):
        value = value.split(",")
    return tuple(name.strip() for name in value if name.strip())


class CLI(Client):
    output_style = "text"

    def save_config(
        self,
        filename: str,
        warehouse_id: int | None = None,
        table_id: int | None = None,
    ) -> None:
        self.output_style = "json"
        SaveLoad(self).save_config(filename, warehouse_id, table_id)

    def load_config(
        self,
        filename: str,
        warehouse_id: int | None = None,
        table_id: int | None = None,
        force: bool = False,
    ) -> None:
        self.output_style = "json"
        SaveLoad(self).load_config(filename, warehouse_id, table_id, force)

    def pull(
        self,
        filename: str,
        *table_refs: str,
        exclude_labels: str | None = None,
        warehouse_id: int | None = None,
        configured_only: bool = False,
        schemas: str | None = None,
        table_labels: str | None = None,
        table_pattern: str | None = None,
    ) -> None:
        self.output_style = "json"
        StateMachine(self).pull(
            filename,
            table_refs,
            _split_names(exclude_labels),
            filters=TableFilters(
                configured_only=configured_only,
                schemas=_split_names(schemas),
                table_labels=_split_names(table_labels),
                table_pattern=table_pattern,
                warehouse_id=warehouse_id,
            ),
        )

    def examine(
        self, table: str, check: str | None = None, format: str = "yaml"
    ) -> None:
        self.output_style = "json"
        StateMachine(self).examine(table, check, format)

    def apply(
        self,
        filename: str,
        dryrun: bool = False,
        noninteractive: bool = False,
    ) -> None:
        self.output_style = "json"
        StateMachine(self).apply(filename, dryrun, noninteractive)

    def destroy(
        self,
        filename: str,
        dryrun: bool = False,
        noninteractive: bool = False,
    ) -> None:
        self.output_style = "json"
        StateMachine(self).apply(filename, dryrun, noninteractive, destroy=True)
