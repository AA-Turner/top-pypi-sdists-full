from __future__ import annotations

import copy
import os
from collections import defaultdict
from dataclasses import MISSING, dataclass, field, fields
from difflib import unified_diff
from textwrap import indent
from typing import Any, Dict, List, Optional

import yaml


class StateModel:
    """Base for the models written to and read from state files.

    Subclasses convert to and from the plain dicts that are dumped to YAML. The
    dict keys differ from some attribute names (`config` is `configuration`,
    `check_type` is `check`, `tables` is `AnomaloTables`). Unknown keys are
    ignored when reading, missing keys take the field default (a missing `check` is a KeyError), and
    None values are kept as None.
    """

    def to_dict(self, encode_json: bool = False) -> Dict[str, Any]:
        raise NotImplementedError


def _missing(cls: type, name: str, key: str) -> Any:
    """The value a field gets when its key is absent from the input dict."""
    for f in fields(cls):
        if f.name == name:
            if f.default_factory is not MISSING:
                return f.default_factory()
            if f.default is not MISSING:
                return f.default
    raise KeyError(key)


def _get(cls: type, kvs: Dict[str, Any], key: str, name: str) -> Any:
    return copy.deepcopy(kvs[key]) if key in kvs else _missing(cls, name, key)


def _copy_list(value: Optional[List[str]]) -> Optional[List[str]]:
    return list(value) if value is not None else None


def _models_to_dicts(models: Optional[Dict[str, Check]]) -> Optional[Dict[str, Any]]:
    if models is None:
        return None
    return {
        ref: model.to_dict() if isinstance(model, StateModel) else model
        for ref, model in models.items()
    }


def _dicts_to_checks(data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Check]]:
    if data is None:
        return None
    return {
        ref: Check.from_dict(value) if isinstance(value, dict) else value
        for ref, value in data.items()
    }


@dataclass
class Table(StateModel):
    config: Dict[str, Any] = field(default_factory=dict)
    checks: Dict[str, Check] = field(default_factory=dict)
    system_checks: Dict[str, Check] = field(default_factory=dict)
    labels: Optional[List[str]] = None
    notification_channels: Optional[List[str]] = None

    def to_dict(self, encode_json: bool = False) -> Dict[str, Any]:
        return {
            "configuration": copy.deepcopy(self.config),
            "checks": _models_to_dicts(self.checks),
            "system_checks": _models_to_dicts(self.system_checks),
            "labels": _copy_list(self.labels),
            "notification_channels": _copy_list(self.notification_channels),
        }

    @classmethod
    def from_dict(cls, kvs: Dict[str, Any]) -> Table:
        return cls(
            config=_get(cls, kvs, "configuration", "config"),
            checks=_dicts_to_checks(_get(cls, kvs, "checks", "checks")),  # type: ignore[arg-type]
            system_checks=_dicts_to_checks(  # type: ignore[arg-type]
                _get(cls, kvs, "system_checks", "system_checks")
            ),
            labels=_get(cls, kvs, "labels", "labels"),
            notification_channels=_get(
                cls, kvs, "notification_channels", "notification_channels"
            ),
        )


@dataclass
class Check(StateModel):
    check_type: str
    params: Dict[str, Any] = field(default_factory=dict)
    labels: Optional[List[str]] = None
    notification_channels: Optional[List[str]] = None

    def to_dict(self, encode_json: bool = False) -> Dict[str, Any]:
        return {
            "check": self.check_type,
            "params": copy.deepcopy(self.params),
            "labels": _copy_list(self.labels),
            "notification_channels": _copy_list(self.notification_channels),
        }

    @classmethod
    def from_dict(cls, kvs: Dict[str, Any]) -> Check:
        return cls(
            check_type=_get(cls, kvs, "check", "check_type"),
            params=_get(cls, kvs, "params", "params"),
            labels=_get(cls, kvs, "labels", "labels"),
            notification_channels=_get(
                cls, kvs, "notification_channels", "notification_channels"
            ),
        )


@dataclass
class State(StateModel):
    tables: Dict[str, Table] = field(default_factory=lambda: defaultdict(Table))

    @classmethod
    def _remove_unused_table_properties(cls, kvs: Dict[str, Any]) -> Dict[str, Any]:
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
    def _normalize_check_cadence_types(cls, kvs: Dict[str, Any]) -> Dict[str, Any]:
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
    def from_dict(cls, kvs: Dict[str, Any]) -> State:
        kvs = cls._normalize_check_cadence_types(
            cls._remove_unused_table_properties(kvs)
        )
        tables = kvs.get("AnomaloTables")
        # Loaders index `state.tables[table_ref]` for tables that don't exist yet,
        # so `tables` is always a defaultdict.
        return cls(
            tables=defaultdict(
                Table,
                {
                    ref: Table.from_dict(value) if isinstance(value, dict) else value
                    for ref, value in (tables or {}).items()
                },
            )
        )

    def to_dict(self, encode_json: bool = False) -> Dict[str, Any]:
        return self._remove_unused_table_properties(
            {
                "AnomaloTables": {
                    ref: table.to_dict() if isinstance(table, StateModel) else table
                    for ref, table in self.tables.items()
                }
            }
        )


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
