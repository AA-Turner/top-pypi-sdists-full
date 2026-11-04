from __future__ import annotations

from typing import Any, Dict, List

from ..state.errors import StateMachineError
from .meta import META_PREFIX
from .report import TimeColumnChoice


DEFAULT_FULL_SCAN_RUN_AT = "PT6H"
MONITORING_FLAGS = ("enable_data_quality", "enable_observability")
# Ephemeral models compile into the models that use them and never exist as tables.
UNMONITORABLE_MATERIALIZATIONS = frozenset({"ephemeral"})


class MissingWarehouse(StateMachineError):
    def __init__(self, node: Dict[str, Any]) -> None:
        self.location = node.get("original_file_path") or node.get("unique_id", "")
        self.node_name = node.get("name", "")

    def __str__(self) -> str:
        return (
            f"{self.location} ({self.node_name}): no Anomalo warehouse; pass"
            f" --warehouse or set {META_PREFIX}warehouse"
        )


class UnknownTimeColumnType(StateMachineError):
    def __init__(self, node: Dict[str, Any], column: str) -> None:
        self.location = node.get("original_file_path") or node.get("unique_id", "")
        self.node_name = node.get("name", "")
        self.column = column

    def __str__(self) -> str:
        return (
            f"{self.location} ({self.node_name}): can't tell whether time column"
            f" {self.column} holds dates or timestamps; set"
            f" {META_PREFIX}time_column_type, declare the column's data_type, or put"
            " the dbt catalog.json next to the manifest"
        )


def is_monitorable(node: Dict[str, Any], settings: Dict[str, Any]) -> bool:
    """Whether a model or source sets a monitoring flag and can be monitored.

    A flag set to false counts: it is how a project turns a table off. A table that
    sets neither is left as Anomalo has it, like a table missing from a YAML file.
    """
    if node.get("resource_type") not in ("model", "source"):
        return False
    config = node.get("config") or {}
    if config.get("enabled") is False:
        return False
    if config.get("materialized") in UNMONITORABLE_MATERIALIZATIONS:
        return False
    return bool(monitoring_flags(settings))


def monitoring_flags(settings: Dict[str, Any]) -> Dict[str, bool]:
    """The monitoring flags the project sets, as Anomalo configuration fields."""
    return {flag: settings[flag] for flag in MONITORING_FLAGS if flag in settings}


def turns_monitoring_on(settings: Dict[str, Any]) -> bool:
    return any(monitoring_flags(settings).values())


def table_ref(
    node: Dict[str, Any], settings: Dict[str, Any], default_warehouse: str | None
) -> str:
    warehouse = settings.get("warehouse") or default_warehouse
    if not warehouse:
        raise MissingWarehouse(node)
    name = node.get("alias") or node.get("identifier") or node["name"]
    return f"{warehouse}.{node['schema']}.{name}"


def choose_time_column(
    node: Dict[str, Any], settings: Dict[str, Any], column_types: Dict[str, str]
) -> TimeColumnChoice:
    """The column that tells Anomalo which rows are new, from explicit dbt signals only.

    Column names are never guessed from: a misread load column made static tables
    look stale. A table without a signal is scanned in full.
    """
    config = node.get("config") or {}
    if "time_column" in settings:
        column = settings["time_column"]
        if column is None:
            return TimeColumnChoice(
                None, None, f"{META_PREFIX}time_column is null: full table scan"
            )
        return _choice(
            node, settings, column_types, column, f"{META_PREFIX}time_column"
        )
    if config.get("event_time"):
        return _choice(
            node, settings, column_types, config["event_time"], "dbt event_time"
        )
    partition_by = config.get("partition_by") or {}
    if partition_by.get("field") and partition_by.get("data_type") != "int64":
        return _choice(
            node, settings, column_types, partition_by["field"], "dbt partition_by"
        )
    loaded_at = node.get("loaded_at_field") or config.get("loaded_at_field")
    if loaded_at:
        return _choice(
            node, settings, column_types, loaded_at, "source loaded_at_field"
        )
    return TimeColumnChoice(None, None, "no time column declared: full table scan")


def table_configuration(
    node: Dict[str, Any], settings: Dict[str, Any], time_column: TimeColumnChoice
) -> Dict[str, Any]:
    configuration: Dict[str, Any] = {
        "definition": " ".join((node.get("description") or "").split()) or None,
        # Only a flag the project sets; `overlay` fills an unset one from Anomalo.
        **monitoring_flags(settings),
    }
    if time_column.column:
        return {
            **configuration,
            "check_cadence_run_at_duration": None,
            "check_cadence_type": "automatic",
            "scope_of_data_to_check": "latest_day",
            "time_column_type": time_column.column_type,
            "time_columns": [time_column.column],
        }
    return {
        **configuration,
        "check_cadence_run_at_duration": settings.get(
            "run_at", DEFAULT_FULL_SCAN_RUN_AT
        ),
        "check_cadence_type": "scheduled",
        "scope_of_data_to_check": "full_table_scan",
        "time_column_type": None,
        "time_columns": [],
    }


def table_labels(node: Dict[str, Any], owner_label: str) -> List[str]:
    config = node.get("config") or {}
    labels = [owner_label, *(node.get("tags") or [])]
    labels += [f"{key}:{value}" for key, value in (config.get("labels") or {}).items()]
    return list(dict.fromkeys(labels))


def _choice(
    node: Dict[str, Any],
    settings: Dict[str, Any],
    column_types: Dict[str, str],
    column: str,
    reason: str,
) -> TimeColumnChoice:
    column_type = settings.get("time_column_type") or _detected_type(
        node, column_types, column
    )
    if not column_type:
        raise UnknownTimeColumnType(node, column)
    return TimeColumnChoice(column, column_type, reason)


def _detected_type(
    node: Dict[str, Any], column_types: Dict[str, str], column: str
) -> str | None:
    declared = ((node.get("columns") or {}).get(column) or {}).get("data_type")
    partition_by = (node.get("config") or {}).get("partition_by") or {}
    partition_type = (
        partition_by.get("data_type") if partition_by.get("field") == column else None
    )
    for warehouse_type in (column_types.get(column.lower()), declared, partition_type):
        anomalo_type = _anomalo_time_type(warehouse_type or "")
        if anomalo_type:
            return anomalo_type
    return None


def _anomalo_time_type(warehouse_type: str) -> str | None:
    normalized = warehouse_type.strip().upper()
    if normalized == "DATE":
        return "date"
    if "TIMESTAMP" in normalized or "DATETIME" in normalized:
        return "timestamp"
    return None
