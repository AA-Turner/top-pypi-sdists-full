from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence

from ..state.models import Action, CheckAction, TableConfigAction


@dataclass
class TimeColumnChoice:
    column: str | None
    column_type: str | None
    reason: str


@dataclass
class DbtReport:
    """What a dbt-driven apply inferred or skipped, so the plan output can explain itself."""

    time_columns: Dict[str, TimeColumnChoice] = field(default_factory=dict)
    check_counts: Dict[str, int] = field(default_factory=dict)
    singular_tests: List[str] = field(default_factory=list)
    skipped_tests: List[str] = field(default_factory=list)
    ref_collisions: List[str] = field(default_factory=list)
    unmatched_channels: List[str] = field(default_factory=list)
    unconfigured_tables: List[str] = field(default_factory=list)
    missing_tables: List[str] = field(default_factory=list)
    ambiguous_tables: List[str] = field(default_factory=list)
    # table ref -> why the table was left out of the converted file
    skipped_tables: Dict[str, str] = field(default_factory=dict)
    disabled_checks: List[str] = field(default_factory=list)
    reenabled_checks: List[str] = field(default_factory=list)

    def count_check(self, kind: str) -> None:
        self.check_counts[kind] = self.check_counts.get(kind, 0) + 1

    def lines(self) -> List[str]:
        lines = ["Time columns:"]
        for table_ref, choice in sorted(self.time_columns.items()):
            chosen = (
                f"{choice.column} ({choice.column_type})" if choice.column else "none"
            )
            lines.append(f"  {table_ref}: {chosen}, {choice.reason}")
        if self.check_counts:
            counts = ", ".join(
                f"{count} {kind}" for kind, count in sorted(self.check_counts.items())
            )
            lines.append(f"dbt tests mirrored as checks: {counts}")
        lines += _section("Singular tests and their tables:", self.singular_tests)
        lines += _section("Skipped dbt tests:", self.skipped_tests)
        lines += _section(
            "Check refs that fell back to the dbt test name:", self.ref_collisions
        )
        lines += _section(
            "Checks to disable (their dbt tests are disabled):", self.disabled_checks
        )
        lines += _section(
            "Checks to re-enable (their dbt tests are enabled again):",
            self.reenabled_checks,
        )
        lines += _section(
            "Tables to unconfigure (both monitoring flags set to false):",
            self.unconfigured_tables,
        )
        lines += _section(
            "Tables not in Anomalo yet, skipped (refresh the warehouse in Anomalo once"
            " dbt has built them):",
            self.missing_tables,
        )
        lines += _section(
            "Tables matching more than one Anomalo table once case is ignored,"
            " skipped:",
            self.ambiguous_tables,
        )
        lines += _section(
            "Tables skipped because Anomalo hides their checks:",
            [f"{ref}: {reason}" for ref, reason in sorted(self.skipped_tables.items())],
        )
        lines += _section(
            "Notification channels with no match in Anomalo:", self.unmatched_channels
        )
        return lines


def difference_summary(actions: Sequence[Action]) -> str:
    """Counts of how the tables and user checks on the two sides of a comparison differ.

    A converted file is applied without deletion, so there is no deletion count.
    """
    tables = {"change": 0, "configure": 0, "unconfigure": 0}
    checks = {"Create": 0, "Modify": 0}
    for action in actions:
        if isinstance(action, TableConfigAction):
            tables[_table_change(action)] += 1
        elif isinstance(action, CheckAction) and not action.is_system_check:
            checks[action.verb] += 1
    return (
        f"{_count(tables['configure'], 'table')} to configure,"
        f" {tables['change']} to change, {tables['unconfigure']} to unconfigure;"
        f" {_count(checks['Create'], 'check')} to add, {checks['Modify']} to change"
    )


def _table_change(action: TableConfigAction) -> str:
    was_configured = is_configured(action.prev or {})
    will_be_configured = is_configured(action.new or {})
    if will_be_configured and not was_configured:
        return "configure"
    if was_configured and not will_be_configured:
        return "unconfigure"
    return "change"


def is_configured(config: Dict[str, Any]) -> bool:
    # Matches Anomalo's own test for a configured table: either monitoring flag on.
    # A cadence alone counts too, since a new configuration may leave the flags unsent.
    return bool(
        config.get("enable_data_quality")
        or config.get("enable_observability")
        or config.get("check_cadence_type")
    )


def _count(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def _section(title: str, items: List[str]) -> List[str]:
    if not items:
        return []
    return [title, *(f"  {item}" for item in items)]
