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

    def pull(
        self, filename: str, *table_refs: str, exclude_labels: str | None = None
    ) -> None:
        self.output_style = "json"
        labels_to_exclude: list[str] = []
        if exclude_labels:
            labels_to_exclude = [
                label.strip() for label in exclude_labels.split(",") if label.strip()
            ]
        StateMachine(self).pull(filename, table_refs, labels_to_exclude)

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
