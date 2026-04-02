from __future__ import annotations

from collections import defaultdict

from ...client import Client
from ...encoder import Encoder
from .models import State, Table, Warehouse


class SaveLoad:
    def __init__(self, client: Client):
        self.client = client

    def _warehouse_ids(
        self, restrict_warehouse_id: int | None = None
    ) -> dict[int, str]:
        warehouse_ids = {
            int(wh["id"]): wh["name"]
            for wh in self.client.list_warehouses()["warehouses"]
        }
        if restrict_warehouse_id:
            restrict_warehouse_id = int(restrict_warehouse_id)
            if restrict_warehouse_id not in warehouse_ids:
                raise Exception(f"Warehouse with ID {restrict_warehouse_id} not found")
            return {restrict_warehouse_id: warehouse_ids[restrict_warehouse_id]}
        return warehouse_ids

    def _table_ids(
        self, restrict_warehouse_id: int, restrict_table_id: int | None = None
    ) -> set[int]:
        table_ids = {
            int(t["table"]["id"])
            for t in self.client.configured_tables(warehouse_id=restrict_warehouse_id)
        }
        if restrict_table_id:
            restrict_table_id = int(restrict_table_id)
            if restrict_table_id not in table_ids:
                raise Exception(
                    f"Table ID {restrict_table_id} not found in warehouse with ID {restrict_warehouse_id}"
                )
            return {restrict_table_id}
        return table_ids

    def _write_table_configuration(
        self,
        warehouse_id: int,
        table_id: int,
        existing_table: Table,
        table: Table,
        force: bool,
    ) -> int:
        if existing_table.configuration == table.configuration:
            return 0
        if not (
            force or table.configuration._may_overwrite(existing_table.configuration)
        ):
            print(
                f"Skipping stale config for table {table.configuration.name}"
                f" (warehouse {warehouse_id}, table {table_id})"
            )
            return 0
        print(
            f"Configuring table {table.configuration.name}"
            f" (warehouse {warehouse_id}, table {table_id})"
        )
        table.configuration.apply(self.client)
        return 1

    def _write_checks(
        self,
        warehouse_id: int,
        table_id: int,
        existing_table: Table,
        table: Table,
        force: bool,
    ) -> int:
        if not table.checks:
            return 0
        checks_count = 0
        for check in table.checks.values():
            if check.id in existing_table.checks:
                if existing_table.checks[check.id] == check:
                    # No changes
                    continue
                if not (force or check._may_overwrite(existing_table.checks[check.id])):
                    print(
                        f"Skipping stale config for check {check.id}"
                        f" in warehouse {warehouse_id} and table {table_id}"
                    )
                    return 0
            check.apply(self.client)
            print(
                f"Loading check {check.id}"
                f" in warehouse {warehouse_id} and table {table_id}"
            )
            checks_count += 1
        return checks_count

    def _load_state_from_api(
        self,
        restrict_warehouse_id: int | None = None,
        restrict_table_id: int | None = None,
    ) -> State:
        state = State()
        warehouses = self._warehouse_ids(restrict_warehouse_id=restrict_warehouse_id)
        for wh_id in warehouses.keys():
            if restrict_warehouse_id and restrict_warehouse_id != wh_id:
                continue
            wh_state = Warehouse(wh_id, name=warehouses[wh_id])
            state.warehouses[wh_state.id] = wh_state
            table_ids = self._table_ids(
                restrict_warehouse_id=wh_id, restrict_table_id=restrict_table_id
            )
            for tbl_id in table_ids:
                if restrict_table_id and restrict_table_id != tbl_id:
                    continue
                table_state = Table.from_api(self.client, wh_id, tbl_id)
                wh_state.tables[table_state.id] = table_state
                print(
                    f"Found table {table_state.configuration.name}"
                    f" (warehouse {wh_id}, table {tbl_id})"
                )
        return state

    def save_config(
        self,
        filename: str,
        warehouse_id: int | None = None,
        table_id: int | None = None,
    ) -> None:
        encoder = Encoder(filename)
        data_by_warehouse_by_table = self._load_state_from_api(
            restrict_warehouse_id=warehouse_id, restrict_table_id=table_id
        ).to_dict()
        encoder.save(data_by_warehouse_by_table)
        tables_count = sum(
            len([tbl_key for tbl_key in wh_value if not tbl_key.startswith("_")])
            for wh_value in data_by_warehouse_by_table.values()
        )
        if tables_count:
            print(f"Saved {tables_count} tables")

    def load_config(
        self,
        filename: str,
        warehouse_id: int | None = None,
        table_id: int | None = None,
        force: bool = False,
    ) -> None:
        encoder = Encoder(filename)
        state = State.from_dict(encoder.load())
        update_counts: defaultdict[str, int] = defaultdict(int)
        for wh in state.warehouses.values():
            for tbl in wh.tables.values():
                existing_table = Table.from_api(self.client, wh.id, tbl.id)
                update_counts["configuration"] += self._write_table_configuration(
                    wh.id, tbl.id, existing_table, tbl, force
                )
                update_counts["quality_checks"] += self._write_checks(
                    wh.id, tbl.id, existing_table, tbl, force
                )
        if update_counts:
            for object_type, count in sorted(update_counts.items()):
                print(f"Table {object_type} changes: {count}")
        else:
            print("No changes to apply")
