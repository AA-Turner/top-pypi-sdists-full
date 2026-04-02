from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, TypeVar

from ...client import Client


SM = TypeVar("SM", bound="SerializableModel")


def _remove_prefix(s: str, prefix: str):
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


class SerializableModel:
    @classmethod
    def from_dict(cls: type[SM], data: dict[str, Any], id: int | None = None) -> SM:
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class State(SerializableModel):
    warehouses: dict[int, Warehouse] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {f"warehouse_{wh.id}": wh.to_dict() for wh in self.warehouses.values()}

    @classmethod
    def from_dict(cls, data: dict[str, Any], id: int | None = None) -> State:
        warehouses: dict[int, Warehouse] = {}
        for wh_id, wh_data in data.items():
            warehouse_id = int(_remove_prefix(wh_id, "warehouse_"))
            wh = Warehouse.from_dict(wh_data, warehouse_id)
            warehouses[wh.id] = wh
        return cls(warehouses=warehouses)


@dataclass
class Warehouse(SerializableModel):
    id: int
    name: str
    tables: dict[int, Table] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            **{"_metadata": {"name": self.name}},
            **{f"table_{tbl.id}": tbl.to_dict() for tbl in self.tables.values()},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], id: int | None = None) -> Warehouse:
        if not id:
            raise ValueError("id is required")
        data_copy = data.copy()
        metadata = data_copy.pop("_metadata")
        tables: dict[int, Table] = {}
        for tbl_id, tbl_data in data_copy.items():
            table_id = int(_remove_prefix(tbl_id, "table_"))
            tbl = Table.from_dict(tbl_data, table_id)
            tables[tbl.id] = tbl
        return cls(id=id, name=metadata.get("name"), tables=tables)


@dataclass
class Table(SerializableModel):
    id: int
    configuration: TableConfiguration
    checks: dict[int, Check] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        output: dict[str, Any] = {"configuration": self.configuration.to_dict()}
        if self.checks:
            output = {
                **output,
                **{
                    "quality_checks": [
                        self.checks[check_id].to_dict()
                        for check_id in sorted(self.checks.keys())
                    ]
                },
            }
        return output

    @classmethod
    def from_api(cls, client: Client, warehouse_id: int, table_id: int) -> Table:
        return Table(
            table_id,
            configuration=TableConfiguration.from_api_response(
                client.get_table_information(
                    warehouse_id=warehouse_id, table_id=table_id
                )
            ),
            checks={
                c.id: c
                for c in [
                    Check.from_api_response(table_id, c)
                    for c in client.get_checks_for_table(table_id=table_id)["checks"]
                    if c["check_static_id"]
                ]
            },
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any], id: int | None = None) -> Table:
        if not id:
            raise ValueError("id is required")
        checks: dict[int, Check] = {}
        for check_data in data.get("quality_checks") or []:
            check = Check.from_dict(check_data, id)
            checks[check.id] = check
        return cls(
            id=id,
            configuration=TableConfiguration.from_dict(
                data.get("configuration") or {}, id
            ),
            checks=checks,
        )


class ModelWithMetadata(SerializableModel):
    def apply(self, client: Client) -> None:
        raise NotImplementedError

    @classmethod
    def _format_metadata(cls, config: dict[str, Any]) -> Any:
        metadata = {}
        for key in {"created", "created_by", "last_edited_at", "last_edited_by"}:
            if key in config:
                metadata[key] = config.pop(key)
        return metadata

    def _last_edited_at(self) -> datetime | None:
        ts = (getattr(self, "metadata", None) or {}).get("last_edited_at")
        if not ts:
            return None
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _may_overwrite(self, other: ModelWithMetadata) -> bool:
        my_dt = self._last_edited_at()
        other_dt = other._last_edited_at()
        if not my_dt or not other_dt:
            return True
        return my_dt >= other_dt


@dataclass
class TableConfiguration(ModelWithMetadata):
    id: int
    name: str
    config: dict = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def apply(self, client: Client) -> None:
        client.configure_table(table_id=self.id, **self.config)

    @classmethod
    def from_api_response(cls, api_response: dict[str, Any]) -> TableConfiguration:
        config_copy = api_response["config"].copy()
        table_id = config_copy.pop("table_id")
        metadata = cls._format_metadata(config_copy)
        return cls(
            id=table_id,
            name=api_response["full_name"],
            metadata=metadata,
            config=config_copy,
        )

    @classmethod
    def from_dict(
        cls, data: dict[str, Any], table_id: int | None = None
    ) -> TableConfiguration:
        if not table_id:
            raise ValueError("table_id is required")
        data_copy = data.copy()
        metadata = data_copy.pop("_metadata", None) or {}
        return cls(
            id=table_id,
            name=metadata.pop("full_name", None),
            metadata=metadata,
            config=data_copy,
        )

    def to_dict(self) -> dict[str, Any]:
        metadata = {**self.metadata, **{"full_name": self.name}}
        return {**{"_metadata": metadata}, **self.config}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TableConfiguration):
            return False
        return all(
            getattr(self, prop) == getattr(other, prop)
            for prop in {"id", "name", "config"}
        )


@dataclass
class Check(ModelWithMetadata):
    id: int  # static ID
    table_id: int
    check: str
    params: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def apply(self, client: Client) -> None:
        client.create_check(self.table_id, self.check, **self.params)

    @classmethod
    def from_api_response(cls, table_id: int, api_response: dict[str, Any]) -> Check:
        metadata = cls._format_metadata(api_response)
        params = {
            **(api_response["config"].get("params") or {}),
            **{
                "check_static_id": api_response["check_static_id"],
                "notification_channel": api_response[
                    "additional_notification_channel_id"
                ],
                "notification_channels": api_response[
                    "additional_notification_channel_ids"
                ],
            },
        }
        return cls(
            id=api_response["check_static_id"],
            table_id=table_id,
            check=api_response["check_type"],
            params=params,
            metadata=metadata,
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any], table_id: int | None = None) -> Check:
        if not table_id:
            raise ValueError("table_id is required")
        return cls(
            id=data["params"]["check_static_id"],
            table_id=table_id,
            check=data["check"],
            params=data["params"],
            metadata=data["_metadata"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {"_metadata": self.metadata, "check": self.check, "params": self.params}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Check):
            return False
        return all(
            getattr(self, prop) == getattr(other, prop)
            for prop in {"id", "check", "params"}
        )
