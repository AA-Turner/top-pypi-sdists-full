from __future__ import annotations

import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Set, Tuple

from ..state.models import Check, State, Table
from .checks import (
    build_check,
    compiled_sql_check,
    declaring_source_id,
    map_test,
    name_ref,
    non_default_threshold,
    stable_ref,
)
from .manifest import DbtManifest
from .meta import dbt_test_settings, node_settings
from .report import DbtReport, is_configured
from .tables import (
    MONITORING_FLAGS,
    choose_time_column,
    is_monitorable,
    monitoring_flags,
    table_configuration,
    table_labels,
    table_ref,
    turns_monitoring_on,
)


ISO_DURATION = re.compile(
    r"^P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$"
)
OWNER_LABEL_PREFIX = "dbt:"
RELATION_RESOURCE_TYPES = frozenset({"model", "seed", "snapshot", "source"})
# Params dbt controls but may stop setting. Merging keeps the server's copy of every
# other param, so a bound or filter dbt removed has to be cleared explicitly.
RESETTABLE_PARAMS: Dict[str, Tuple[str, ...]] = {
    "ColumnRange": ("high", "low"),
    "JoinLeftAtLeastOne": ("custom_where_sql_right",),
    "MultiColumnUnique": ("column_b", "column_c", "list_of_columns"),
}
# Anomalo counts a table as configured, and licensed, while either monitoring flag is
# on. Unsetting only the cadence, as the generic unconfigure step does, leaves it so.
UNCONFIGURED = {
    "check_cadence_type": None,
    "enable_data_quality": False,
    "enable_observability": False,
}


@dataclass
class CheckSource:
    test_id: str
    kind: str


@dataclass
class DesiredDbtState:
    """What the dbt project says about the tables it sets flags on, before it meets Anomalo.

    Notification channels still hold the values written in dbt; `overlay` resolves
    them against the channels that exist in Anomalo. Monitoring flags the project
    leaves unset are missing from a table's config until `overlay` fills them in.
    """

    owner_label: str
    state: State
    report: DbtReport = field(default_factory=DbtReport)
    # table ref -> check ref -> the dbt test it comes from and how it was mapped
    check_sources: Dict[str, Dict[str, CheckSource]] = field(
        default_factory=lambda: defaultdict(dict)
    )
    # table ref -> for each disabled dbt test, the refs its check may have
    disabled_check_refs: Dict[str, List[List[str]]] = field(
        default_factory=lambda: defaultdict(list)
    )

    @property
    def warehouses(self) -> Set[str]:
        return {ref.rsplit(".", 2)[0] for ref in self.state.tables}


@dataclass
class _CandidateCheck:
    test: Dict[str, Any]
    override_ref: str | None
    check: Check
    kind: str


@dataclass
class _DisabledTest:
    stable: str
    name: str


def owner_label(project_name: str) -> str:
    return f"{OWNER_LABEL_PREFIX}{project_name}"


def build_desired_state(
    manifest: DbtManifest, default_warehouse: str | None
) -> DesiredDbtState:
    desired = DesiredDbtState(owner_label(manifest.project_name), State())
    relatables = {
        unique_id: node
        for unique_id, node in {**manifest.nodes, **manifest.sources}.items()
        if node.get("resource_type") in RELATION_RESOURCE_TYPES
    }
    relation_names = {
        unique_id: node["relation_name"]
        for unique_id, node in relatables.items()
        if node.get("relation_name")
    }
    refs_by_id = _add_tables(desired, manifest, relatables, default_warehouse)
    refs_by_name = {
        relatables[unique_id]["name"]: ref for unique_id, ref in refs_by_id.items()
    }
    enabled_tests, disabled_tests = _tests(manifest)
    candidates: Dict[str, List[_CandidateCheck]] = defaultdict(list)
    for test in enabled_tests:
        candidate = _candidate_check(
            desired, test, refs_by_id, refs_by_name, relation_names
        )
        if candidate:
            table_key, check = candidate
            candidates[table_key].append(check)
    disabled: Dict[str, List[_DisabledTest]] = defaultdict(list)
    for test in disabled_tests:
        settings = dbt_test_settings(test)
        owner = _owning_table(test, settings, refs_by_id, refs_by_name, desired.report)
        if owner is not None:
            disabled[owner].append(
                _DisabledTest(stable_ref(test, settings.get("ref")), name_ref(test))
            )
    for table_key in sorted(candidates.keys() | disabled.keys()):
        table_candidates = candidates.get(table_key, [])
        table_disabled = disabled.get(table_key, [])
        clashing = _clashing_refs(table_candidates, table_disabled)
        if table_candidates:
            desired.state.tables[table_key].checks = _assign_refs(
                table_key, table_candidates, clashing, desired
            )
        desired.disabled_check_refs[table_key] = [
            _disabled_refs(disabled_test, clashing) for disabled_test in table_disabled
        ]
    return desired


def adopt_anomalo_table_refs(
    desired: DesiredDbtState, known_refs: Iterable[str]
) -> None:
    """Respell desired tables as Anomalo spells them, and drop the ones it doesn't have.

    Warehouses differ in how they case identifiers (Snowflake upper-cases unquoted
    names, dbt usually writes them lowercase), so tables match case-insensitively. An
    exact match wins, and a name that only matches several tables once case is ignored
    is left out: a warehouse can hold `wh.s.fact` and `wh.s.FACT` side by side, and
    guessing between them could monitor the wrong table. Two desired tables that would
    land on one Anomalo table keep only an exact name match for it. A table dbt built
    since Anomalo last refreshed the warehouse is reported and skipped rather than
    failing the run, so CI keeps converting everything else.
    """
    known = set(known_refs)
    by_lowercase: Dict[str, List[str]] = defaultdict(list)
    for known_ref in sorted(known):
        by_lowercase[known_ref.lower()].append(known_ref)
    resolved = {
        ref: _matched_ref(ref, known, by_lowercase) for ref in desired.state.tables
    }
    winners = _claimed_refs(resolved, desired.report)
    tables: Dict[str, Table] = defaultdict(Table)
    check_sources: Dict[str, Dict[str, CheckSource]] = defaultdict(dict)
    disabled_refs: Dict[str, List[List[str]]] = defaultdict(list)
    for ref, table in desired.state.tables.items():
        anomalo_ref = resolved[ref]
        if anomalo_ref is None:
            candidates = by_lowercase.get(ref.lower())
            if candidates:
                desired.report.ambiguous_tables.append(
                    f"{ref}: matches {', '.join(candidates)}"
                )
            else:
                desired.report.missing_tables.append(ref)
            desired.report.time_columns.pop(ref, None)
            continue
        if winners.get(anomalo_ref) != ref:
            desired.report.time_columns.pop(ref, None)
            continue
        tables[anomalo_ref] = table
        if ref in desired.check_sources:
            check_sources[anomalo_ref] = desired.check_sources[ref]
        if ref in desired.disabled_check_refs:
            disabled_refs[anomalo_ref] = desired.disabled_check_refs[ref]
        if ref in desired.report.time_columns:
            desired.report.time_columns[anomalo_ref] = desired.report.time_columns.pop(
                ref
            )
    desired.state.tables = tables
    desired.check_sources = check_sources
    desired.disabled_check_refs = disabled_refs


def _claimed_refs(resolved: Dict[str, str | None], report: DbtReport) -> Dict[str, str]:
    """The desired ref that keeps each Anomalo ref, reporting the ones that lose it.

    Two dbt tables can resolve to one Anomalo table when one name matches it exactly
    and the other only once case is ignored. Only the exact name keeps it; without an
    exact name neither does, since nothing says which table Anomalo's name means.
    """
    claims: Dict[str, List[str]] = defaultdict(list)
    for ref, anomalo_ref in resolved.items():
        if anomalo_ref is not None:
            claims[anomalo_ref].append(ref)
    winners: Dict[str, str] = {}
    for anomalo_ref, refs in claims.items():
        exact = [ref for ref in refs if ref == anomalo_ref]
        if len(refs) == 1:
            winners[anomalo_ref] = refs[0]
            continue
        if len(exact) == 1:
            winners[anomalo_ref] = exact[0]
            for ref in refs:
                if ref != exact[0]:
                    report.ambiguous_tables.append(
                        f"{ref}: only matches {anomalo_ref} when case is ignored, and"
                        f" {exact[0]} names it exactly"
                    )
            continue
        for ref in refs:
            others = ", ".join(other for other in refs if other != ref)
            report.ambiguous_tables.append(
                f"{ref}: only matches {anomalo_ref} when case is ignored, as do"
                f" {others}"
            )
    return winners


def _matched_ref(
    ref: str, known: Set[str], by_lowercase: Dict[str, List[str]]
) -> str | None:
    """The one Anomalo ref `ref` names, or None when none does or several might."""
    if ref in known:
        return ref
    candidates = by_lowercase.get(ref.lower(), [])
    return candidates[0] if len(candidates) == 1 else None


def overlay(
    actual: State,
    desired: DesiredDbtState,
    channels: List[Dict[str, Any]],
    check_ids: Dict[str, Dict[str, int]],
) -> State:
    """Anomalo's state with what the dbt project states written over it.

    Like a native YAML apply, only what the project states changes: a table that
    sets no monitoring flag is left alone, a flag it leaves unset keeps Anomalo's
    value (off on a table not configured yet), and no check is ever removed. A dbt
    test removed from the project leaves its check as it is; one disabled in dbt
    disables its check, by adding its id to the table's disabled checks.

    A table whose Data Quality ends up off keeps its checks as they are. Anomalo stops
    listing them, and deleting one would cut it off from its run history; kept, they
    resume with it when Data Quality is back on. That hidden state is also why a table
    turning Data Quality on with a disabled test is left out of the conversion: its
    check cannot be found to disable, so enabling Data Quality would let the check run
    again. `skipped_tables` carries the reason for the report.

    `check_ids` maps each table's check refs to Anomalo check ids.
    """
    result = deepcopy(actual)
    for ref, wanted in sorted(desired.state.tables.items()):
        target = result.tables[ref]
        was_configured = is_configured(target.config)
        was_data_quality_on = bool(target.config.get("enable_data_quality"))
        # A table with no stored configuration has never had a check created on it,
        # so nothing of its can be hidden.
        had_config = bool(target.config)
        flags = {
            flag: wanted.config[flag]
            if flag in wanted.config
            else (target.config.get(flag) if was_configured else False)
            for flag in MONITORING_FLAGS
        }
        if not any(flags.values()):
            if was_configured:
                target.config = {**target.config, **UNCONFIGURED}
                desired.report.unconfigured_tables.append(ref)
            continue
        disabled_refs = desired.disabled_check_refs.get(ref, [])
        if (
            flags["enable_data_quality"]
            and had_config
            and not was_data_quality_on
            and _has_unresolved_disabled(disabled_refs, check_ids.get(ref, {}))
        ):
            # The check for a disabled test can only be turned off by id, and Anomalo
            # stops listing a table's checks while its Data Quality is off. Enabling it
            # here would let a check the project disabled start running again.
            desired.report.skipped_tables[ref] = (
                "Data Quality is off, so its checks are hidden and a disabled dbt test"
                " cannot be matched to its check; turn Data Quality on, then run"
                " convert_config again"
            )
            continue
        target.config = _merged_config(target.config, {**wanted.config, **flags})
        target.labels = _union(target.labels, wanted.labels)
        if wanted.notification_channels is not None:
            target.notification_channels = _resolved_channels(
                wanted.notification_channels,
                target.notification_channels,
                channels,
                ref,
                desired.report,
            )
        sources = desired.check_sources.get(ref, {})
        if not flags["enable_data_quality"]:
            desired.report.skipped_tests += [
                f"{sources[check_ref].test_id}: Data Quality is off for {ref}; its"
                " checks are kept but don't run, and this test isn't synced"
                for check_ref in sorted(wanted.checks)
            ]
            continue
        for check_ref, check in sorted(wanted.checks.items()):
            target.checks[check_ref] = _merged_check(
                target.checks.get(check_ref), check, channels, ref, desired.report
            )
            desired.report.count_check(sources[check_ref].kind)
        _sync_disabled_checks(
            target,
            ref,
            wanted.checks,
            desired.disabled_check_refs.get(ref, []),
            check_ids.get(ref, {}),
            desired.report,
        )
    return result


def resolve_notify(
    values: List[str], channels: List[Dict[str, Any]]
) -> Tuple[List[str], List[str]]:
    """Match notification values from dbt to existing Anomalo channel refs.

    Accepts a channel ref, a numeric id, or a friendly "<type>:<name>" such as
    "Slack:#alerts", matched on the channel type and the channel name in its
    config or description.
    """
    resolved, unmatched = [], []
    for value in values:
        channel = _find_channel(value, channels)
        if channel is None:
            unmatched.append(value)
        else:
            resolved.append(channel.get("ref") or str(channel["id"]))
    return list(dict.fromkeys(resolved)), unmatched


def _add_tables(
    desired: DesiredDbtState,
    manifest: DbtManifest,
    relatables: Dict[str, Dict[str, Any]],
    default_warehouse: str | None,
) -> Dict[str, str]:
    refs_by_id: Dict[str, str] = {}
    for unique_id, node in sorted(relatables.items()):
        settings = node_settings(node)
        if not is_monitorable(node, settings):
            continue
        ref = table_ref(node, settings, default_warehouse)
        refs_by_id[unique_id] = ref
        table = desired.state.tables[ref]
        if not turns_monitoring_on(settings):
            # Only turning the table off: nothing else about it is the project's to set.
            table.config = monitoring_flags(settings)
            continue
        time_column = choose_time_column(
            node, settings, manifest.column_types.get(unique_id, {})
        )
        table.config = table_configuration(node, settings, time_column)
        table.labels = table_labels(node, desired.owner_label)
        if "notify" in settings:
            table.notification_channels = list(settings["notify"])
        desired.report.time_columns[ref] = time_column
    return refs_by_id


def _tests(
    manifest: DbtManifest,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """The project's enabled data tests, and the ones turned off with `enabled: false`."""
    enabled, disabled = [], list(manifest.disabled_tests)
    for _, node in sorted(manifest.nodes.items()):
        if node.get("resource_type") != "test":
            continue
        if (node.get("config") or {}).get("enabled", True) is False:
            disabled.append(node)
        else:
            enabled.append(node)
    return enabled, disabled


def _candidate_check(
    desired: DesiredDbtState,
    test: Dict[str, Any],
    refs_by_id: Dict[str, str],
    refs_by_name: Dict[str, str],
    relation_names: Dict[str, str],
) -> Tuple[str, _CandidateCheck] | None:
    settings = dbt_test_settings(test)
    owner = _owning_table(test, settings, refs_by_id, refs_by_name, desired.report)
    if owner is None:
        return None
    mapped = None if non_default_threshold(test) else map_test(test, relation_names)
    kind = "native"
    if mapped is None:
        mapped, kind = compiled_sql_check(test), "compiled SQL"
    if mapped is None:
        desired.report.skipped_tests.append(
            f"{test['unique_id']}: no native Anomalo check, and the manifest has no"
            " compiled SQL for it (run dbt compile, not dbt parse)"
        )
        return None
    table_config = desired.state.tables[owner].config
    is_time_based = settings.get("scope") == "latest_day" and bool(
        table_config.get("time_columns")
    )
    if settings.get("scope") == "latest_day" and not is_time_based:
        desired.report.skipped_tests.append(
            f"{test['unique_id']}: anomalo_scope latest_day ignored because {owner}"
            " has no time column; it checks the whole table"
        )
    check_type, specific = mapped
    check = build_check(
        test,
        check_type,
        specific,
        owner_label=desired.owner_label,
        priority=settings.get("priority"),
        is_time_based=is_time_based,
    )
    if "notify" in settings:
        check.notification_channels = list(settings["notify"])
    if not test.get("test_metadata"):
        desired.report.singular_tests.append(f"{test['unique_id']} -> {owner}")
    return owner, _CandidateCheck(test, settings.get("ref"), check, kind)


def _owning_table(
    test: Dict[str, Any],
    settings: Dict[str, Any],
    refs_by_id: Dict[str, str],
    refs_by_name: Dict[str, str],
    report: DbtReport,
) -> str | None:
    """The opted-in table a test's check belongs on, or None to leave the test out."""
    if settings.get("table"):
        owner = refs_by_name.get(settings["table"])
        if owner is None:
            report.skipped_tests.append(
                f"{test['unique_id']}: anomalo_table {settings['table']!r} is not an"
                " opted-in model or source"
            )
        return owner
    if test.get("attached_node"):
        return refs_by_id.get(test["attached_node"])
    source_id = declaring_source_id(test)
    if source_id:
        return refs_by_id.get(source_id)
    # A singular test attaches to nothing and can reference several models, so it goes
    # on the first opted-in one it refs.
    dependencies = (test.get("depends_on") or {}).get("nodes") or []
    return next(
        (refs_by_id[node_id] for node_id in dependencies if node_id in refs_by_id), None
    )


def _clashing_refs(
    candidates: List[_CandidateCheck], disabled: List[_DisabledTest]
) -> Set[str]:
    """Stable refs that more than one test on the table shares.

    Disabled tests count. Their checks exist on the server, so a stable ref two
    tests share must not move to the one that is currently enabled.
    """
    refs = [
        stable_ref(candidate.test, candidate.override_ref) for candidate in candidates
    ]
    refs += [disabled_test.stable for disabled_test in disabled]
    return {ref for ref in refs if refs.count(ref) > 1}


def _disabled_refs(disabled: _DisabledTest, clashing: Set[str]) -> List[str]:
    """The refs the disabled test's check may have, best candidate first.

    A stable ref shared with another test never names this test's check: both fell
    back to their dbt names when their checks were created.
    """
    refs = (
        [disabled.name]
        if disabled.stable in clashing
        else [disabled.stable, disabled.name]
    )
    return list(dict.fromkeys(refs))


def _assign_refs(
    table_key: str,
    candidates: List[_CandidateCheck],
    clashing: Set[str],
    desired: DesiredDbtState,
) -> Dict[str, Check]:
    """Give each check its stable ref, falling back to the dbt test name on a clash."""
    checks: Dict[str, Check] = {}
    for candidate in candidates:
        stable_check_ref = stable_ref(candidate.test, candidate.override_ref)
        ref = stable_check_ref
        if ref in clashing:
            ref = name_ref(candidate.test)
            desired.report.ref_collisions.append(
                f"{table_key}: {stable_check_ref} -> {ref}"
            )
        checks[ref] = candidate.check
        desired.check_sources[table_key][ref] = CheckSource(
            candidate.test["unique_id"], candidate.kind
        )
    return checks


def _has_unresolved_disabled(
    disabled_refs: List[List[str]], check_ids: Dict[str, int]
) -> bool:
    """Whether a disabled test has no check among the ones Anomalo lists."""
    return any(not any(ref in check_ids for ref in refs) for refs in disabled_refs)


def _sync_disabled_checks(
    target: Table,
    table_key: str,
    enabled_refs: Iterable[str],
    disabled_refs: List[List[str]],
    check_ids: Dict[str, int],
    report: DbtReport,
) -> None:
    """Disable the checks of dbt tests disabled in dbt, and re-enable enabled ones.

    Anomalo disables a check by listing its id in the table's
    `disabled_quality_check_ids`, as its own enable toggle does. Only checks the
    project maps to are added or removed, so a check disabled by hand stays disabled.
    """
    current = list(target.config.get("disabled_quality_check_ids") or [])
    to_disable: List[int] = []
    for refs in disabled_refs:
        ref = next((ref for ref in refs if ref in check_ids), None)
        if ref is None or check_ids[ref] in current + to_disable:
            continue
        to_disable.append(check_ids[ref])
        report.disabled_checks.append(f"{table_key}: {ref}")
    to_enable = set()
    for ref in sorted(enabled_refs):
        if check_ids.get(ref) in current:
            to_enable.add(check_ids[ref])
            report.reenabled_checks.append(f"{table_key}: {ref}")
    if to_disable or to_enable:
        target.config["disabled_quality_check_ids"] = [
            *(check_id for check_id in current if check_id not in to_enable),
            *to_disable,
        ]


def _merged_config(current: Dict[str, Any], wanted: Dict[str, Any]) -> Dict[str, Any]:
    """dbt's table settings on top of Anomalo's, keeping Anomalo's spelling of equal values.

    The server reads some values back in another form (an empty `time_columns` as
    null, `PT6H` as `P0DT06H00M00S`, and `enable_observability: true` as null on a
    table that can't run Table Observability); keeping its form is what lets a
    second apply find nothing to change.
    """
    merged = dict(current)
    for key, value in wanted.items():
        if not _same_setting(current.get(key), value):
            merged[key] = value
    if (
        "enable_observability" in current
        and current["enable_observability"] is None
        and wanted.get("enable_observability") is True
    ):
        merged["enable_observability"] = None
    # A table with only Table Observability on reads back with the deprecated
    # `observability` cadence in place of the scheduled one it stores.
    if (
        current.get("check_cadence_type") == "observability"
        and wanted.get("check_cadence_type") == "scheduled"
        and wanted.get("enable_observability")
        and not wanted.get("enable_data_quality")
    ):
        merged["check_cadence_type"] = "observability"
    return merged


def _same_setting(current: Any, wanted: Any) -> bool:
    if current == wanted:
        return True
    if isinstance(wanted, list) and not wanted:
        return current is None
    if isinstance(current, str) and isinstance(wanted, str):
        current_seconds = _duration_seconds(current)
        return current_seconds is not None and current_seconds == _duration_seconds(
            wanted
        )
    return False


def _duration_seconds(value: str) -> int | None:
    match = ISO_DURATION.match(value)
    if not match or value in ("P", "PT"):
        return None
    days, hours, minutes, seconds = (
        int(match.group(name) or 0) for name in ("days", "hours", "minutes", "seconds")
    )
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def _merged_check(
    previous: Check | None,
    wanted: Check,
    channels: List[Dict[str, Any]],
    table_key: str,
    report: DbtReport,
) -> Check:
    """dbt's check on top of the server's copy, keeping the defaults the server filled in."""
    is_same_type = previous is not None and previous.check_type == wanted.check_type
    params = (
        {**previous.params, **wanted.params} if is_same_type else dict(wanted.params)
    )
    if is_same_type:
        for name in RESETTABLE_PARAMS.get(wanted.check_type, ()):
            if name not in wanted.params and params.get(name) is not None:
                params[name] = None
    notification_channels = previous.notification_channels if previous else None
    if wanted.notification_channels is not None:
        notification_channels = _resolved_channels(
            wanted.notification_channels,
            notification_channels,
            channels,
            table_key,
            report,
        )
    return Check(
        check_type=wanted.check_type,
        params=params,
        labels=_union(previous.labels if previous else None, wanted.labels),
        notification_channels=notification_channels,
    )


def _resolved_channels(
    values: List[str],
    current: List[str] | None,
    channels: List[Dict[str, Any]],
    table_key: str,
    report: DbtReport,
) -> List[str] | None:
    resolved, unmatched = resolve_notify(values, channels)
    report.unmatched_channels += [f"{table_key}: {value}" for value in unmatched]
    # When nothing matched, keep the channels already set rather than clearing them.
    if unmatched and not resolved:
        return current
    return resolved


def _find_channel(value: str, channels: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for channel in channels:
        if value in (channel.get("ref"), str(channel.get("id"))):
            return channel
    if ":" not in value:
        return None
    channel_type, name = (part.strip() for part in value.split(":", 1))
    wanted = {name.lower(), name.lstrip("#").lower()}
    for channel in channels:
        if str(channel.get("channel_type", "")).lower() != channel_type.lower():
            continue
        if wanted & _channel_names(channel):
            return channel
    return None


def _channel_names(channel: Dict[str, Any]) -> Set[str]:
    config = channel.get("config") or {}
    names = {
        str(value).strip().lower()
        for key, value in config.items()
        if "channel" in key.lower() and isinstance(value, str)
    }
    names |= {name.lstrip("#") for name in names}
    names.add(str(channel.get("description") or "").strip().lower())
    return names


def _union(current: List[str] | None, additions: List[str] | None) -> List[str] | None:
    if current is None and additions is None:
        return None
    return list(dict.fromkeys([*(current or []), *(additions or [])]))
