from __future__ import annotations

import os
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import unified_diff
from textwrap import indent
from typing import Any, Dict, List, Optional, TypeVar

import yaml
from dataclasses_json import (
    DataClassJsonMixin,
    config,
)
from dataclasses_json.core import Json


SM = TypeVar("SM", bound="StateModel")


always_exclude = lambda _: True


class StateModel(DataClassJsonMixin):
    pass


@dataclass
class Table(StateModel):
    config: Dict[str, Any] = field(
        default_factory=dict, metadata=config(field_name="configuration")
    )
    checks: Dict[str, Check] = field(default_factory=dict)
    system_checks: Dict[str, Check] = field(default_factory=dict)
    labels: Optional[List[str]] = None
    notification_channels: Optional[List[str]] = None


@dataclass
class Check(StateModel):
    check_type: str = field(metadata=config(field_name="check"))
    params: Dict[str, Any] = field(default_factory=dict)
    labels: Optional[List[str]] = None
    notification_channels: Optional[List[str]] = None


@dataclass
class State(StateModel):
    tables: Dict[str, Table] = field(
        default_factory=lambda: defaultdict(Table),
        metadata=config(field_name="AnomaloTables"),
    )

    @classmethod
    def _remove_unused_table_properties(cls, kvs: Dict[str, Json]) -> Dict[str, Json]:
        # Remove empty tables and unused configuration / checks properties from tables
        if isinstance(kvs, dict) and "AnomaloTables" in kvs:
            kvs["AnomaloTables"] = {
                table_ref: {
                    table_data_key: table_data_value
                    for table_data_key, table_data_value in table_data.items()
                    if table_data_value
                }
                for table_ref, table_data in kvs["AnomaloTables"].items()
                if table_data and any(table_data.values())
            }
        return kvs

    @classmethod
    def _normalize_check_cadence_types(cls, kvs: Dict[str, Json]) -> Dict[str, Json]:
        """Normalize check_cadence_type values from old names to new API names."""
        # Mapping from old/internal names to new API names
        cadence_type_map = {
            "data_freshness_gated": "automatic",
            "daily": "scheduled",
            "observability": "observability",
        }

        if isinstance(kvs, dict) and "AnomaloTables" in kvs:
            for table_data in kvs["AnomaloTables"].values():
                if isinstance(table_data, dict) and "configuration" in table_data:
                    config = table_data["configuration"]
                    if isinstance(config, dict) and "check_cadence_type" in config:
                        old_value = config["check_cadence_type"]
                        if old_value in cadence_type_map:
                            config["check_cadence_type"] = cadence_type_map[old_value]
        return kvs

    @classmethod
    def from_dict(cls, kvs: Json, *args: Any, **kwargs: Any) -> State:
        new_state = super().from_dict(
            cls._normalize_check_cadence_types(
                cls._remove_unused_table_properties(kvs)
            ),
            *args,
            **kwargs,
        )
        # dataclasses_json can't construct a defaultdict using type() since defaultdict
        # requires an argument. Instead, replace the parsed dict with a defaultdict.
        new_state.tables = defaultdict(Table, new_state.tables.items())
        return new_state

    def to_dict(self, *args: Any, **kwargs: Any) -> Dict[str, Json]:
        return self._remove_unused_table_properties(super().to_dict(*args, **kwargs))


@dataclass
class Action:
    prev: Dict[str, Any] | StateModel | List[str] | None = None
    new: Dict[str, Any] | StateModel | List[str] | None = None

    def __str__(self) -> str:
        raise NotImplementedError

    def diff(self, format: str = "yaml") -> str | None:
        if self.prev == self.new:
            return None

        def _repr(obj: Dict[str, Any] | StateModel) -> str:
            flat = obj.to_dict() if isinstance(obj, StateModel) else obj
            return indent(yaml.safe_dump(flat), prefix="    ") if flat else ""

        diff = unified_diff(
            _repr(self.prev).splitlines(), _repr(self.new).splitlines(), lineterm=""
        )

        diff = [line for line in diff if not line.startswith(("+++", "---"))]
        return indent(os.linesep.join(diff), prefix="  |  ")

    @property
    def verb(self) -> str:
        if self.new:
            return "Modify" if self.prev else "Create"
        if self.prev:
            return "Destroy"
        return "N/A"


@dataclass
class TableConfigAction(Action):
    prev: Dict[str, Any] | None = None
    new: Dict[str, Any] | None = None
    table_ref: str | None = None

    def __str__(self) -> str:
        return f"{self.verb} {self.table_ref} configuration"

    def diff(self, format: str = "yaml") -> str | None:
        if self.prev == self.new:
            return None
        if format == "shacl" and self.table_ref:
            from .shacl_file import ShaclFileDriver

            driver = ShaclFileDriver(validate_shacl=False)

            def _repr(config: Dict[str, Any] | None) -> str:
                return indent(
                    driver.serialize_table_config(self.table_ref, config),
                    prefix="    ",
                )

        else:

            def _repr(config: Dict[str, Any] | None) -> str:  # type: ignore[misc]
                return indent(yaml.safe_dump(config), prefix="    ") if config else ""

        diff = unified_diff(
            _repr(self.prev).splitlines(), _repr(self.new).splitlines(), lineterm=""
        )
        diff = [line for line in diff if not line.startswith(("+++", "---"))]
        return indent(os.linesep.join(diff), prefix="  |  ")


@dataclass
class CheckAction(Action):
    prev: Check | None = None
    new: Check | None = None
    table_ref: str | None = None
    check_ref: str | None = None
    # System checks are created by the server when a table is configured. They can
    # only be modified, never created or destroyed, so they take a different apply
    # path. Ids cannot stand in for this flag: they are unresolvable at plan time
    # for a table that is configured during the same apply, which is the case that
    # matters. Every check-scoped action carries it so both the dependency graph
    # and the executor can tell the two variants of one ref apart.
    is_system_check: bool = False

    def __str__(self) -> str:
        return f"{self.verb} {self.check_ref} on {self.table_ref}"

    def diff(self, format: str = "yaml") -> str | None:
        if self.prev == self.new:
            return None
        if format == "shacl" and self.table_ref and self.check_ref:
            from .shacl_file import ShaclFileDriver

            driver = ShaclFileDriver(validate_shacl=False)

            def _repr(check: Check | None) -> str:
                return indent(
                    driver.serialize_check(
                        self.table_ref,
                        self.check_ref,
                        check,
                        system_check=self.is_system_check,
                    ),
                    prefix="    ",
                )

        else:

            def _repr(check: Check | None) -> str:  # type: ignore[misc]
                flat = check.to_dict() if check else None
                return indent(yaml.safe_dump(flat), prefix="    ") if flat else ""

        diff = unified_diff(
            _repr(self.prev).splitlines(), _repr(self.new).splitlines(), lineterm=""
        )
        diff = [line for line in diff if not line.startswith(("+++", "---"))]
        return indent(os.linesep.join(diff), prefix="  |  ")


@dataclass
class LabelAction(Action):
    prev: List[str] | None = None
    new: List[str] | None = None
    table_ref: str | None = None
    check_ref: str | None = None
    is_system_check: bool = False

    def __str__(self) -> str:
        return f"{self.verb} labels on {self.check_ref or self.table_ref}"


@dataclass
class NotificationChannelAction(Action):
    prev: List[str] | None = None
    new: List[str] | None = None
    table_ref: str | None = None
    check_ref: str | None = None
    is_system_check: bool = False

    def __str__(self) -> str:
        return (
            f"{self.verb} notification channels on {self.check_ref or self.table_ref}"
        )
