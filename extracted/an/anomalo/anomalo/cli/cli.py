from __future__ import annotations

from ..client import Client
from .save_load.commands import SaveLoad
from .state.machine import StateMachine


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

    def pull(self, filename: str, *table_refs: str) -> None:
        self.output_style = "json"
        StateMachine(self).pull(filename, table_refs)

    def examine(self, table: str, check: str | None = None) -> None:
        self.output_style = "json"
        StateMachine(self).examine(table, check)

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
