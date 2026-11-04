from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Dict, List

from ..dbt.driver import adopt_anomalo_table_refs, build_desired_state, overlay
from ..dbt.manifest import read_dbt_manifest
from .api import APIDriver
from .errors import InvalidFile, UnknownConfigFormat
from .filters import TableFilters
from .models import State, Table


@dataclass
class Conversion:
    """A source file as Anomalo configuration, plus what the conversion inferred."""

    state: State
    report: List[str] = field(default_factory=list)


def convert(
    config_format: str | None,
    filename: str,
    api_state: Callable[[], APIDriver],
    warehouse: str | None = None,
) -> Conversion:
    """`filename`, read as `config_format`, as Anomalo configuration.

    `api_state` builds the read-only view of the organization a format needs; only
    formats that read the organization call it.
    """
    if config_format not in CONVERTERS:
        raise UnknownConfigFormat(config_format, sorted(CONVERTERS))
    return CONVERTERS[config_format](filename, api_state, warehouse)


def _convert_dbt(
    filename: str, api_state: Callable[[], APIDriver], warehouse: str | None
) -> Conversion:
    """The tables a dbt project sets monitoring flags on, as Anomalo has them plus dbt.

    `anomalo apply` sends each table's configuration as a full replace, so a table is
    written with its whole current configuration and dbt's settings merged on top.
    Applying the result then changes only what the project states.
    """
    manifest = read_dbt_manifest(filename)
    if manifest is None:
        raise InvalidFile(filename, "not a dbt manifest.json")
    desired = build_desired_state(manifest, warehouse)
    api = api_state()
    warehouses = sorted(desired.warehouses | ({warehouse} if warehouse else set()))
    known_refs: set[str] = set()
    for warehouse_name in warehouses:
        known_refs |= api.pull_table_refs(
            TableFilters(warehouse_id=api.warehouse_id(warehouse_name))
        )
    adopt_anomalo_table_refs(desired, known_refs)
    check_ids = {}
    for table_ref in sorted(desired.state.tables):
        api.load_table(table_ref)
        api.load_non_system_checks(table_ref)
        api.load_system_checks(table_ref)
        check_ids[table_ref] = api.check_ids(table_ref)
    merged = overlay(api.state, desired, api.notification_channels, check_ids)
    tables: Dict[str, Table] = defaultdict(Table)
    for table_ref in sorted(desired.state.tables):
        # A table overlay skipped is one it cannot convert safely; leave it out
        # rather than write a configuration the project did not ask for.
        if table_ref in desired.report.skipped_tables:
            continue
        tables[table_ref] = merged.tables[table_ref]
    return Conversion(State(tables=tables), desired.report.lines())


CONVERTERS: Dict[
    str, Callable[[str, Callable[[], APIDriver], str | None], Conversion]
] = {
    "dbt": _convert_dbt,
}
