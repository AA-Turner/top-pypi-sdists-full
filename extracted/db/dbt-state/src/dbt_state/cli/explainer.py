import fnmatch
import click
import humanize
import json
import typing as t

from pathlib import Path
from dbt.contracts.graph.nodes import NodeType
from dbt_state.config import CloneIncrementalInDev
from dbt_state.decision_logger import (
    NodeInfo,
    NodeLogEntry,
    RunConfigEntry,
    RunStartEntry,
)
from dbt_state.grpc.client import QueryCacheGrpcClient
from query_cache_common.models.shared_models import SubmitSQLResultType
from query_cache_common.models.services import explain_service_models
from query_cache_common.models.services.explain_service_models import (
    ExplainBadge,
    ExplainLine,
    ExplainMarker,
    ExplainMessageEntry,
)

from query_cache_common.utils import format_as_localtime
from rich.console import Console
from rich.tree import Tree

_EXPLAINER_MAX_BATCH_SIZE = 1000


class Explainer:
    def __init__(
        self,
        query_cache_client: QueryCacheGrpcClient,
        file_path: Path,
        verbose: bool,
        node_selector: t.Optional[str] = None,
        console: t.Optional[Console] = None,
    ):
        self._query_cache_client = query_cache_client
        self._file_path = file_path
        self._verbose = verbose
        self._node_selector = node_selector
        self._console = console or Console()

    def explain(self) -> None:
        """Read the log file and print a human-readable explanation of each node's cache decision, fetching server-generated explanation data as needed."""

        execution_decision_ids: t.List[str] = []
        node_log_entries: t.List[NodeLogEntry] = []
        no_decision_entries: t.List[NodeLogEntry] = []
        explanations: t.Dict[str, ExplainMessageEntry] = {}
        run_start_entry: t.Optional[RunStartEntry] = None

        matched = False
        with self._file_path.open() as f:
            for line in f:
                data = json.loads(line)
                entry_type = data.get("entry_type")
                if entry_type == "run_start":
                    run_start_entry = RunStartEntry.from_dict(data)
                elif entry_type == "node":
                    log_entry = NodeLogEntry.from_dict(data)
                    if self._node_selector and not fnmatch.fnmatch(
                        log_entry.node_name, self._node_selector
                    ):
                        continue
                    matched = True
                    if log_entry.execution_decision_id is not None:
                        execution_decision_ids.append(log_entry.execution_decision_id)
                        node_log_entries.append(log_entry)
                    elif log_entry.node_info.is_view:
                        node_log_entries.append(log_entry)
                    else:
                        no_decision_entries.append(log_entry)

        if self._node_selector and not matched:
            self._println(f"No nodes found matching '{self._node_selector}'")

        for i in range(0, len(execution_decision_ids), _EXPLAINER_MAX_BATCH_SIZE):
            batch = execution_decision_ids[i : i + _EXPLAINER_MAX_BATCH_SIZE]
            request = explain_service_models.GetExplainMessagesRequest(execution_decision_ids=batch)

            response = self._query_cache_client.get_explain_messages(request)
            explanations.update(response.by_id)

        if run_start_entry is None:
            raise click.ClickException(
                "Log file does not contain a run start entry — the file may be empty, corrupt, or in an older format."
            )

        self._explain_run_start(run_start_entry)

        for log_entry in node_log_entries:
            explanation = (
                explanations.get(log_entry.execution_decision_id)
                if log_entry.execution_decision_id
                else None
            )
            if log_entry.execution_decision_id and not explanation:
                no_decision_entries.append(log_entry)
            else:
                self._explain_node(run_start_entry.run_config, log_entry, explanation)
        for log_entry in no_decision_entries:
            self._explain_no_decision_node(log_entry)

    def explain_to_str(self) -> str:
        with self._console.capture() as capture:
            self.explain()
        return capture.get()

    def _explain_run_start(self, run_start_entry: RunStartEntry) -> None:
        self._print("Last run: ")

        if self._verbose:
            self._print(format_as_localtime(run_start_entry.start_timestamp_utc))
            self._print(" (")

        self._print(humanize.naturaltime(run_start_entry.start_timestamp_utc))

        if self._verbose:
            self._println(")")
        else:
            self._println()

        if self._verbose:
            self._println()
            tree = Tree(label="Run configuration:")
            cache_config = tree.add("[bold]dbt State:[/bold]")
            run_config = run_start_entry.run_config
            if run_config.org_id:
                cache_config.add(f"[dim]org id:[/dim] {run_config.org_id}")
            cache_config.add(f"[dim]defer to target:[/dim] {run_config.defer_to_target}")
            freshness_tolerance = (
                f"{humanize.naturaldelta(run_config.freshness_tolerance_seconds)} ({run_config.freshness_tolerance_seconds} seconds)"
                if run_config.freshness_tolerance_seconds
                else "disabled"
            )
            cache_config.add(f"[dim]freshness tolerance:[/dim] {freshness_tolerance}")
            cache_config.add(
                f"[dim]tolerate non-determinism:[/dim] {run_config.tolerate_nondeterminism}"
            )
            cache_config.add(
                f"[dim]clone incremental in dev:[/dim] {run_config.clone_incremental_in_dev.value}"
            )
            metadata_cache_ttl = (
                f"{humanize.naturaldelta(run_config.metadata_cache_ttl_seconds)} ({run_config.metadata_cache_ttl_seconds} seconds)"
                if run_config.metadata_cache_ttl_seconds
                else "infinite (cache never expires)"
            )
            cache_config.add(f"[dim]metadata cache ttl:[/dim] {metadata_cache_ttl}")

            if run_config.snowflake_get_view_ddl_override:
                cache_config.add(
                    f"[dim][snowflake] get view ddl override[/dim]: {run_config.snowflake_get_view_ddl_override}"
                )

            dbt_config = tree.add("[bold]dbt:[/bold]")
            dbt_config.add(f"[dim]profile:[/dim] {run_config.profile_name}")
            dbt_config.add(f"[dim]target:[/dim] {run_config.target_name}")
            if run_config.select:
                dbt_config.add(f"[dim]--select:[/dim] {' '.join(run_config.select)}")
            if run_config.exclude:
                dbt_config.add(f"[dim]--exclude:[/dim] {' '.join(run_config.exclude)}")

            self._print(tree)

        self._println()

    def _explain_no_decision_node(self, log_entry: NodeLogEntry) -> None:
        tree = Tree(label=f"[bold]{log_entry.node_name}[/bold]")
        tree.add("explanation unavailable")
        self._print(tree)
        self._println()

    def _explain_node(
        self,
        run_config: RunConfigEntry,
        log_entry: NodeLogEntry,
        explanation: t.Optional[ExplainMessageEntry] = None,
    ) -> None:
        if self._verbose:
            self._explain_node_verbose(run_config, log_entry, explanation)
        else:
            self._explain_node_simple(log_entry, explanation)

        self._println()

    def _explain_node_simple(
        self, log_entry: NodeLogEntry, explanation: t.Optional[ExplainMessageEntry] = None
    ) -> None:
        if log_entry.execution_decision_id and explanation:
            tree = Tree(label=f"[bold]{log_entry.node_name}[/bold]")
            decision_display = _display_decision(
                is_dev_clone=bool(log_entry.node_info.dev_clone),
                decision_label=explanation.decision.label,
            )
            description_display = _short_description(
                node_resource_type=log_entry.node_info.node_resource_type,
                is_dev_clone=bool(log_entry.node_info.dev_clone),
                decision=explanation.decision,
                description=explanation.decision_description,
            )
            tree.add(f"[{decision_display}] {description_display}")
            self._print(tree)
        elif log_entry.node_info.is_view:
            tree = Tree(label=f"[bold]{log_entry.node_name}[/bold]")
            decision_display = _display_decision(
                is_dev_clone=bool(log_entry.node_info.dev_clone), decision_label="Execute"
            )
            tree.add(f"[{decision_display}] views are always executed without checking the cache")
            self._print(tree)

    def _explain_node_verbose(
        self,
        run_config: RunConfigEntry,
        log_entry: NodeLogEntry,
        explanation: t.Optional[ExplainMessageEntry] = None,
    ) -> None:
        if log_entry.execution_decision_id and explanation:
            tree = Tree(label=f"[bold]{log_entry.node_name}[/bold]")

            _decorate_explain_lines(
                run_config=run_config,
                node_info=log_entry.node_info,
                lines=explanation.explain_lines,
            )

            _add_lines_to_tree(tree, explanation.explain_lines)

            self._print(tree)
            decision_display = _display_decision(
                is_dev_clone=bool(log_entry.node_info.dev_clone),
                decision_label=explanation.decision.label,
            )
            description_display = _short_description(
                node_resource_type=log_entry.node_info.node_resource_type,
                is_dev_clone=bool(log_entry.node_info.dev_clone),
                decision=explanation.decision,
                description=explanation.decision_description,
            )
            self._println(f"[bold]decision: [{decision_display}][/bold] {description_display}")
        elif log_entry.node_info.is_view:
            tree = Tree(label=f"[bold]{log_entry.node_name}[/bold]")
            tree.add(f"view ({log_entry.node_info.fqn})")
            self._print(tree)
            decision_display = _display_decision(
                is_dev_clone=bool(log_entry.node_info.dev_clone), decision_label="Execute"
            )
            self._println(
                f"[bold]decision: [{decision_display}][/bold] views are always executed without checking the cache"
            )

    def _print(self, what: t.Optional[t.Any] = None) -> None:
        self._console.print(what or "", end="")

    def _println(self, what: t.Optional[t.Any] = None) -> None:
        self._console.print(what or "")


def _decorate_explain_lines(
    run_config: RunConfigEntry, node_info: NodeInfo, lines: list[ExplainLine]
) -> None:
    if run_config.target_name != run_config.defer_to_target:
        _apply_target_name_to_table_exists(target_name=run_config.target_name, lines=lines)

    if node_info.dev_clone:
        _apply_dev_clone_modifications(
            clone_incremental_in_dev=run_config.clone_incremental_in_dev,
            source_table_fqn=node_info.dev_clone.source_table_fqn,
            lines=lines,
        )

    if node_info.deferrals:
        _apply_deferral_modifications(
            deferrals=node_info.deferrals,
            defer_to_target=run_config.defer_to_target,
            lines=lines,
        )

    if (
        node_info.is_incremental_or_snapshot
        and node_info.node_resource_type == NodeType.Model.value
    ):
        _apply_full_refresh_modifications(is_full_refresh=node_info.is_full_refresh, lines=lines)


def _apply_target_name_to_table_exists(target_name: str, lines: list[ExplainLine]) -> None:
    for line in lines:
        if line.text.startswith("table analysis"):
            for ta_line in line.children:
                if ta_line.badge == ExplainBadge.TARGET_TABLE_EXISTS:
                    ta_line.text = ta_line.text + f" in '{target_name}'"


def _apply_dev_clone_modifications(
    clone_incremental_in_dev: CloneIncrementalInDev,
    source_table_fqn: str,
    lines: list[ExplainLine],
) -> None:
    for line in lines:
        if line.text.startswith("table analysis"):
            if clone_incremental_in_dev == CloneIncrementalInDev.IF_TABLE_MISSING:
                line.children.insert(
                    0,
                    ExplainLine(text="the model table did not exist", marker=ExplainMarker.INFO),
                )
            for ta_line in line.children:
                if ta_line.badge == ExplainBadge.TARGET_TABLE_EXISTS:
                    ta_line.text = f"we cloned from {source_table_fqn} to create it"
                    ta_line.marker = ExplainMarker.SUCCESS
                    ta_line.badge = None

        if line.text.startswith("query analysis"):
            for qa_line in line.children:
                if qa_line.badge == ExplainBadge.NODE_QUERY_CHANGED:
                    qa_line.text = f"{qa_line.text} (vs the one the clone was based on)"


def _apply_deferral_modifications(
    deferrals: t.Dict[str, str], defer_to_target: str, lines: list[ExplainLine]
) -> None:
    has_query_analysis = False
    deferral_lines = ExplainLine(
        text=f"the following relations were resolved to their '{defer_to_target}' counterparts:",
        children=(
            [ExplainLine(text=f"{name} -> {target_fqn}") for name, target_fqn in deferrals.items()]
        ),
        marker=ExplainMarker.INFO,
    )
    for line in lines:
        if line.text.startswith("query analysis"):
            has_query_analysis = True
            line.children.insert(0, deferral_lines)
    if not has_query_analysis:
        query_analysis_line = ExplainLine(text="query analysis", children=[deferral_lines])
        if not lines:
            lines.insert(0, query_analysis_line)
        elif "table analysis" in lines[0].text:
            lines.insert(1, query_analysis_line)
        else:
            lines.insert(0, query_analysis_line)


def _apply_full_refresh_modifications(is_full_refresh: bool, lines: list[ExplainLine]) -> None:
    for line in lines:
        if line.text.startswith("query analysis"):
            for qa_line in line.children:
                if qa_line.badge == ExplainBadge.NODE_QUERY_CHANGED:
                    if is_full_refresh:
                        qa_line.children.append(
                            ExplainLine(
                                text="the query has been rendered in full mode (is_incremental=False)"
                            )
                        )
                    else:
                        qa_line.children.append(
                            ExplainLine(
                                text="the query has been rendered in incremental mode (is_incremental=True)"
                            )
                        )


def _add_lines_to_tree(tree: Tree, lines: list[ExplainLine]) -> None:
    for line in lines:
        child = tree.add(_format_line(line))
        if line.children:
            _add_lines_to_tree(child, line.children)


def _display_decision(is_dev_clone: bool, decision_label: str) -> str:
    colors = {
        SubmitSQLResultType.SKIP_EXECUTION.label: "green",
        SubmitSQLResultType.READY_TO_EXECUTE.label: "yellow",
        SubmitSQLResultType.READY_TO_CLONE.label: "cyan",
        SubmitSQLResultType.UNKNOWN.label: "dim",
    }

    color = colors[decision_label]

    if is_dev_clone:
        decision_label = f"{SubmitSQLResultType.READY_TO_CLONE.label}; {decision_label}"

    return f"[{color}]{decision_label}[/{color}]"


def _short_description(
    node_resource_type: str, is_dev_clone: bool, decision: SubmitSQLResultType, description: str
) -> str:
    if is_dev_clone:
        if node_resource_type == NodeType.Model.value:
            if decision == SubmitSQLResultType.READY_TO_EXECUTE:
                return "incremental model base data was cloned; model was executed against clone because either the query changed or the upstream data was out of date"
            if decision == SubmitSQLResultType.SKIP_EXECUTION:
                return "incremental model was cloned from a fresh source in the compile phase, resulting in a no-op in the execute phase"
        elif node_resource_type == NodeType.Snapshot.value:
            if decision == SubmitSQLResultType.READY_TO_EXECUTE:
                return "snapshot base data was cloned; snapshot was executed against clone because either the query changed or the upstream data was out of date"
            if decision == SubmitSQLResultType.SKIP_EXECUTION:
                return "snapshot was cloned from a fresh source in the compile phase, resulting in a no-op in the execute phase"
    return description


def _format_line(line: ExplainLine) -> str:
    if line.badge:
        if line.badge == ExplainBadge.FRESH:
            line.text = f"[[green]fresh[/green]] {line.text}"
        elif line.badge == ExplainBadge.WITHIN_TOLERANCE:
            line.text = f"[[yellow]within tolerance[/yellow]] {line.text}"
        elif line.badge == ExplainBadge.OUTDATED:
            line.text = f"[[red]outdated[/red]] {line.text}"
        elif line.badge == ExplainBadge.UPSTREAM_QUERY_UNCHANGED:
            line.text = f"[green]{line.text}[/green]"
        elif line.badge == ExplainBadge.UPSTREAM_QUERY_CHANGED:
            line.text = f"[red]{line.text}[/red]"

    if line.marker:
        if line.marker == ExplainMarker.SUCCESS:
            line.text = f"[green]✓[/green] {line.text}"
        elif line.marker == ExplainMarker.FAIL:
            line.text = f"[red]✗[/red] {line.text}"
        elif line.marker == ExplainMarker.INFO:
            line.text = f"[blue]-[/blue] {line.text}"
    return line.text
