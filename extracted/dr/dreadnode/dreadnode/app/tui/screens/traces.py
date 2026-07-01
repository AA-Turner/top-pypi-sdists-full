"""Traces Browser screen -- browse and inspect OpenTelemetry traces."""

from __future__ import annotations

import asyncio
import typing as t
from datetime import datetime

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static, Tree

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import (
    BRAND,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    PURPLE,
    SUCCESS,
    TEAL,
    WARNING,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.widgets.tree import TreeNode

    from dreadnode.app.api.client import ApiClient

# -- Status dot helper -------------------------------------------------------

_STATUS_DOT: dict[str, str] = {
    "completed": f"[{SUCCESS}]\u25cf[/]",
    "failed": f"[{ERROR}]\u25cf[/]",
    "pending": f"[{WARNING}]\u25cf[/]",
}


def _status_dot(status: str) -> str:
    return _STATUS_DOT.get(status, f"[{FG_SUBTLE}]\u25cf[/]")


# -- Span colour by type ----------------------------------------------------

_SPAN_TYPE_COLOUR: dict[str, str] = {
    "llm": PURPLE,
    "generation": PURPLE,
    "chat": PURPLE,
    "tool": TEAL,
    "agent": INFO,
}


def _span_colour(span_type: str) -> str:
    lower = span_type.lower()
    for key, colour in _SPAN_TYPE_COLOUR.items():
        if key in lower:
            return colour
    return BRAND


# -- Duration formatting -----------------------------------------------------


def _fmt_duration(ns: float) -> str:
    """Format nanoseconds into a human-readable duration."""
    ms = ns / 1_000_000
    if ms < 1000:
        return f"{int(ms)}ms"
    seconds = ms / 1000
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}m{secs:.0f}s"


def _fmt_timestamp(ts: str | datetime) -> str:
    """Format an ISO timestamp for display."""
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return ts[:19]
    else:
        dt = ts
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# -- Duration bar helper ----------------------------------------------------


def _duration_bar(span_ms: float, total_ms: float, max_width: int = 20) -> str:
    """Build a proportional bar string."""
    if total_ms <= 0:
        return ""
    ratio = min(span_ms / total_ms, 1.0)
    filled = max(1, int(ratio * max_width))
    return "\u2592" * filled


# ============================================================================
# TracesScreen
# ============================================================================


class TracesScreen(DreadnodeScreen):
    """Two-mode traces browser: list view and waterfall drill-down."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("r", "refresh_traces", "Refresh", show=True),
    ]

    def __init__(
        self,
        api: ApiClient,
        org: str,
        workspace: str,
        project: str,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._org = org
        self._workspace = workspace
        self._project = project

        # Data
        self._traces: list[dict[str, t.Any]] = []
        self._spans: list[dict[str, t.Any]] = []
        self._selected_trace_id: str | None = None

        # Mode: "list" or "waterfall"
        self._mode: t.Literal["list", "waterfall"] = "list"

    # ------------------------------------------------------------------ compose

    _SUBTITLE = f"\n[{FG_FAINTEST}] Inspect OpenTelemetry traces and spans[/]"

    def compose_content(self) -> ComposeResult:
        yield Static(
            f"[bold {FG}] Traces[/]{self._SUBTITLE}",
            id="traces-title",
        )
        with Horizontal(id="traces-body"):
            with Vertical(id="traces-left"):
                yield DataTable(id="traces-table")
                yield Tree("Spans", id="span-tree")
            with Vertical(id="traces-right"):
                yield Tree("Detail", id="detail-tree")

    # ------------------------------------------------------------------ mount

    def on_mount(self) -> None:
        super().on_mount()
        # Configure DataTable
        table = self.query_one("#traces-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("", "Name", "Type", "Duration", "Timestamp")

        # Span tree starts hidden
        self.query_one("#span-tree", Tree).display = False

        self._load_traces()

    # ------------------------------------------------------------------ actions

    def action_go_back(self) -> None:
        if self._mode == "waterfall":
            self._switch_to_list_mode()
        else:
            self.dismiss()

    def action_cursor_down(self) -> None:
        if self._mode == "list":
            table = self.query_one("#traces-table", DataTable)
            table.action_cursor_down()
        else:
            tree = self.query_one("#span-tree", Tree)
            tree.action_cursor_down()

    def action_cursor_up(self) -> None:
        if self._mode == "list":
            table = self.query_one("#traces-table", DataTable)
            table.action_cursor_up()
        else:
            tree = self.query_one("#span-tree", Tree)
            tree.action_cursor_up()

    def action_refresh_traces(self) -> None:
        if self._mode == "list":
            self._load_traces()

    # ------------------------------------------------------------------ list mode

    @work(exclusive=True, group="traces")
    async def _load_traces(self) -> None:
        """Fetch traces from the platform API."""
        if not self.is_mounted:
            return
        table = self.query_one("#traces-table", DataTable)
        table.clear()

        title = self.query_one("#traces-title", Static)
        title.update(f"[bold {FG}] Traces[/]  [{FG_FAINTEST}]\u2026[/]{self._SUBTITLE}")

        try:
            data = await asyncio.to_thread(
                self._api.list_traces,
                self._org,
                self._workspace,
                self._project,
                page=1,
                page_size=50,
            )
            self._traces = data.get("traces", [])
        except Exception as exc:
            if self.is_mounted:
                title.update(f"[bold {FG}] Traces[/]  [{ERROR}]{exc}[/]{self._SUBTITLE}")
            return

        if not self.is_mounted:
            return

        if not self._traces:
            title.update(f"[bold {FG}] Traces[/]{self._SUBTITLE}")
            return

        for trace in self._traces:
            status = trace.get("status", "pending")
            name = trace.get("name", "unknown")
            span_type = trace.get("type", "span")
            duration = _fmt_duration(trace.get("duration", 0))
            timestamp = _fmt_timestamp(trace.get("timestamp", ""))
            table.add_row(
                _status_dot(status),
                name,
                span_type,
                duration,
                timestamp,
                key=trace.get("trace_id", ""),
            )

        total = data.get("total", len(self._traces))
        title.update(f"[bold {FG}] Traces[/]  [{FG_MUTED}]{total}[/]{self._SUBTITLE}")

        # Show detail for first trace
        if self._traces:
            self._show_trace_summary(self._traces[0])

    # ------------------------------------------------------------------ events

    @on(DataTable.RowHighlighted, "#traces-table")
    def _on_trace_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        trace_id = str(event.row_key.value)
        for trace in self._traces:
            if trace.get("trace_id") == trace_id:
                self._show_trace_summary(trace)
                break

    @on(DataTable.RowSelected, "#traces-table")
    def _on_trace_selected(self, event: DataTable.RowSelected) -> None:
        if event.row_key is None:
            return
        trace_id = str(event.row_key.value)
        self._selected_trace_id = trace_id
        self._switch_to_waterfall_mode(trace_id)

    @on(Tree.NodeHighlighted, "#span-tree")
    def _on_span_highlighted(self, event: Tree.NodeHighlighted) -> None:
        span_data = event.node.data
        if isinstance(span_data, dict):
            self._show_span_detail(span_data)

    # ------------------------------------------------------------------ trace summary

    def _show_trace_summary(self, trace: dict[str, t.Any]) -> None:
        """Populate the right-hand detail tree with trace summary info."""
        detail = self.query_one("#detail-tree", Tree)
        detail.clear()
        detail.root.set_label(f"[bold]Trace: {trace.get('name', 'unknown')}[/]")

        status = trace.get("status", "pending")
        status_colour = {
            "completed": SUCCESS,
            "failed": ERROR,
            "pending": WARNING,
        }.get(status, FG_SUBTLE)

        # Basic info
        info_node = detail.root.add("Info", expand=True)
        info_node.add_leaf(f"Trace ID: [{FG_SUBTLE}]{trace.get('trace_id', 'n/a')}[/]")
        info_node.add_leaf(f"Span ID: [{FG_SUBTLE}]{trace.get('span_id', 'n/a')}[/]")
        info_node.add_leaf(f"Status: [{status_colour}]{status}[/]")
        info_node.add_leaf(f"Type: [{FG_SUBTLE}]{trace.get('type', 'span')}[/]")
        info_node.add_leaf(f"Duration: [{FG}]{_fmt_duration(trace.get('duration', 0))}[/]")
        info_node.add_leaf(
            f"Timestamp: [{FG_SUBTLE}]{_fmt_timestamp(trace.get('timestamp', ''))}[/]"
        )

        if trace.get("task_id"):
            info_node.add_leaf(f"Task ID: [{FG_SUBTLE}]{trace['task_id']}[/]")

        # Tags
        tags = trace.get("tags", [])
        if tags:
            tags_node = detail.root.add("Tags", expand=True)
            for tag in sorted(tags):
                tags_node.add_leaf(f"[{TEAL}]{tag}[/]")

        # Params
        params = trace.get("params", {})
        if params:
            params_node = detail.root.add("Params", expand=True)
            for key in sorted(params):
                value = params[key]
                params_node.add_leaf(f"{key}: [{FG_SUBTLE}]{value}[/]")

        # Metrics
        metrics = trace.get("metrics", {})
        if metrics:
            metrics_node = detail.root.add("Metrics", expand=True)
            for key in sorted(metrics):
                metric_list = metrics[key]
                if isinstance(metric_list, list) and metric_list:
                    last_val = metric_list[-1]
                    if isinstance(last_val, dict):
                        val = last_val.get("value", "n/a")
                    else:
                        val = last_val
                    metrics_node.add_leaf(f"{key}: [{INFO}]{val}[/]")

        # Exception
        exc = trace.get("exception")
        if exc and isinstance(exc, dict):
            exc_node = detail.root.add(f"[{ERROR}]Exception[/]", expand=True)
            exc_node.add_leaf(f"Type: [{ERROR}]{exc.get('type', 'unknown')}[/]")
            exc_node.add_leaf(f"Message: [{ERROR}]{exc.get('message', '')}[/]")

        detail.root.expand()

    # ------------------------------------------------------------------ waterfall mode

    def _switch_to_waterfall_mode(self, trace_id: str) -> None:
        """Switch from list mode to waterfall mode for a specific trace."""
        self._mode = "waterfall"

        # Hide table, show span tree
        self.query_one("#traces-table", DataTable).display = False
        span_tree = self.query_one("#span-tree", Tree)
        span_tree.display = True
        span_tree.focus()

        # Adjust layout: 33/66 for waterfall
        self.query_one("#traces-left").styles.width = "1fr"
        self.query_one("#traces-right").styles.width = "2fr"

        title = self.query_one("#traces-title", Static)
        title.update(
            f"[bold {FG}] Waterfall[/]  [{FG_MUTED}]{trace_id[:12]}[/] [{FG_FAINTEST}]\u2026[/]{self._SUBTITLE}"
        )

        self._load_spans(trace_id)

    def _switch_to_list_mode(self) -> None:
        """Switch back from waterfall to list mode."""
        self._mode = "list"

        # Show table, hide span tree
        self.query_one("#traces-table", DataTable).display = True
        table = self.query_one("#traces-table", DataTable)
        table.focus()
        self.query_one("#span-tree", Tree).display = False

        # Restore layout: 60/40 for list
        self.query_one("#traces-left").styles.width = "3fr"
        self.query_one("#traces-right").styles.width = "2fr"

        total = len(self._traces)
        title = self.query_one("#traces-title", Static)
        title.update(f"[bold {FG}] Traces[/]  [{FG_MUTED}]{total}[/]{self._SUBTITLE}")

        # Re-show summary of currently highlighted trace
        if self._traces:
            self._show_trace_summary(self._traces[0])

    @work(exclusive=True, group="traces")
    async def _load_spans(self, trace_id: str) -> None:
        """Fetch spans for a trace and build the waterfall tree."""
        try:
            result = await asyncio.to_thread(
                self._api.get_trace_spans,
                self._org,
                self._workspace,
                self._project,
                trace_id,
                limit=500,
            )
            rows = result.get("data", [])
            meta = result.get("meta", [])
        except Exception as exc:
            title = self.query_one("#traces-title", Static)
            title.update(f"[bold {FG}] Waterfall[/]  [{ERROR}]{exc}[/]{self._SUBTITLE}")
            return

        # Parse span data from ClickHouse columnar response
        self._spans = self._parse_span_rows(rows, meta)

        title = self.query_one("#traces-title", Static)
        title.update(
            f"[bold {FG}] Waterfall[/]  [{FG_MUTED}]{trace_id[:12]} \u00b7 {len(self._spans)} spans[/]{self._SUBTITLE}"
        )

        self._build_span_tree()

        # Show detail for root span if available
        if self._spans:
            self._show_span_detail(self._spans[0])

    def _parse_span_rows(
        self,
        rows: list[dict[str, t.Any] | list[t.Any]],
        meta: list[dict[str, str]],
    ) -> list[dict[str, t.Any]]:
        """Convert ClickHouse response to list of span dicts."""
        if not rows:
            return []
        # JSON format returns rows as dicts already
        if isinstance(rows[0], dict):
            return t.cast("list[dict[str, t.Any]]", rows)
        # Columnar format returns rows as arrays
        if not meta:
            return []
        col_names = [m.get("name", f"col_{i}") for i, m in enumerate(meta)]
        return [dict(zip(col_names, row, strict=False)) for row in rows]

    def _build_span_tree(self) -> None:
        """Build the hierarchical span tree from flat span list."""
        tree = self.query_one("#span-tree", Tree)
        tree.clear()

        if not self._spans:
            tree.root.set_label("[dim]No spans[/]")
            return

        # Compute total duration for proportional bars
        total_ms = max(
            (s.get("Duration", 0) for s in self._spans),
            default=1,
        )
        # Ensure it's numeric
        if not isinstance(total_ms, (int, float)):
            total_ms = 1

        # Build parent-child index
        spans_by_id: dict[str, dict[str, t.Any]] = {}
        children: dict[str, list[str]] = {}
        root_spans: list[str] = []

        for span in self._spans:
            sid = str(span.get("SpanId", ""))
            parent = str(span.get("ParentSpanId", ""))
            spans_by_id[sid] = span
            if not parent or parent == sid or parent == "0" * len(parent):
                root_spans.append(sid)
            else:
                children.setdefault(parent, []).append(sid)

        # If no root spans found, treat all as root
        if not root_spans:
            root_spans = [str(s.get("SpanId", "")) for s in self._spans]

        tree.root.set_label(f"[bold {BRAND}]Trace Spans[/]")

        def _add_span_node(parent_node: TreeNode, span_id: str, depth: int = 0) -> None:
            span = spans_by_id.get(span_id)
            if span is None:
                return

            name = str(span.get("SpanName", "unknown"))
            duration = span.get("Duration", 0)
            if not isinstance(duration, (int, float)):
                duration = 0
            span_kind = str(span.get("SpanKind", ""))

            # Detect span type from name/attributes for colouring
            span_type = _detect_span_type(span)
            colour = _span_colour(span_type)

            bar = _duration_bar(duration, total_ms)
            dur_str = _fmt_duration(duration)
            kind_label = f" [{FG_SUBTLE}]({span_kind})[/]" if span_kind else ""
            label = f"[{colour}]{name}[/]{kind_label} [{FG_SUBTLE}]{dur_str}[/] [{colour}]{bar}[/]"

            child_ids = children.get(span_id, [])
            if child_ids:
                node = parent_node.add(label, data=span, expand=True)
                for child_id in child_ids:
                    _add_span_node(node, child_id, depth + 1)
            else:
                parent_node.add_leaf(label, data=span)

        for root_id in root_spans:
            _add_span_node(tree.root, root_id)

        tree.root.expand()

    # ------------------------------------------------------------------ span detail

    def _show_span_detail(self, span: dict[str, t.Any]) -> None:
        """Populate the right-hand detail tree with span attributes."""
        detail = self.query_one("#detail-tree", Tree)
        detail.clear()

        name = str(span.get("SpanName", "unknown"))
        detail.root.set_label(f"[bold]Span: {name}[/]")

        # IDs
        ids_node = detail.root.add("Identifiers", expand=True)
        ids_node.add_leaf(f"Span ID: [{FG_SUBTLE}]{span.get('SpanId', 'n/a')}[/]")
        ids_node.add_leaf(f"Parent Span ID: [{FG_SUBTLE}]{span.get('ParentSpanId', 'n/a')}[/]")
        ids_node.add_leaf(f"Trace ID: [{FG_SUBTLE}]{span.get('TraceId', 'n/a')}[/]")

        # Status
        status_code = str(span.get("StatusCode", ""))
        if "ERROR" in status_code.upper() or status_code == "2":
            status_label = f"[{ERROR}]Error[/]"
        elif "OK" in status_code.upper() or status_code == "1":
            status_label = f"[{SUCCESS}]OK[/]"
        else:
            status_label = f"[{WARNING}]{status_code or 'Unset'}[/]"

        timing_node = detail.root.add("Timing", expand=True)
        timing_node.add_leaf(f"Status: {status_label}")

        timestamp = span.get("Timestamp", "")
        if timestamp:
            timing_node.add_leaf(f"Start: [{FG_SUBTLE}]{_fmt_timestamp(timestamp)}[/]")

        duration = span.get("Duration", 0)
        if isinstance(duration, (int, float)):
            timing_node.add_leaf(f"Duration: [{FG}]{_fmt_duration(duration)}[/]")

        span_kind = span.get("SpanKind", "")
        if span_kind:
            timing_node.add_leaf(f"Kind: [{FG_SUBTLE}]{span_kind}[/]")

        service = span.get("ServiceName", "")
        if service:
            timing_node.add_leaf(f"Service: [{FG_SUBTLE}]{service}[/]")

        # Span Attributes
        attrs = span.get("SpanAttributes", {})
        if isinstance(attrs, dict) and attrs:
            attrs_node = detail.root.add("Attributes", expand=True)
            for key in sorted(attrs):
                value = attrs[key]
                # Truncate very long values
                val_str = str(value)
                if len(val_str) > 200:
                    val_str = val_str[:200] + "..."
                attrs_node.add_leaf(f"{key}: [{FG_SUBTLE}]{val_str}[/]")

        # Resource Attributes
        res_attrs = span.get("ResourceAttributes", {})
        if isinstance(res_attrs, dict) and res_attrs:
            res_node = detail.root.add("Resource", expand=False)
            for key in sorted(res_attrs):
                value = res_attrs[key]
                val_str = str(value)
                if len(val_str) > 200:
                    val_str = val_str[:200] + "..."
                res_node.add_leaf(f"{key}: [{FG_SUBTLE}]{val_str}[/]")

        # Events
        events = span.get("Events.Name", [])
        event_timestamps = span.get("Events.Timestamp", [])
        event_attrs = span.get("Events.Attributes", [])
        if events and isinstance(events, list) and any(events):
            events_node = detail.root.add("Events", expand=True)
            for i, event_name in enumerate(events):
                if not event_name:
                    continue
                ts = event_timestamps[i] if i < len(event_timestamps) else ""
                ts_str = f" [{FG_SUBTLE}]{_fmt_timestamp(ts)}[/]" if ts else ""
                ev_node = events_node.add(f"[{TEAL}]{event_name}[/]{ts_str}")
                if i < len(event_attrs) and isinstance(event_attrs[i], dict):
                    for ek, ev in sorted(event_attrs[i].items()):
                        ev_str = str(ev)
                        if len(ev_str) > 200:
                            ev_str = ev_str[:200] + "..."
                        ev_node.add_leaf(f"{ek}: [{FG_SUBTLE}]{ev_str}[/]")

        # Status message
        status_msg = span.get("StatusMessage", "")
        if status_msg:
            detail.root.add_leaf(f"Status Message: [{ERROR}]{status_msg}[/]")

        detail.root.expand()


# -- Span type detection helper -----------------------------------------------


def _detect_span_type(span: dict[str, t.Any]) -> str:
    """Heuristic to detect the type of a span for colour coding."""
    name = str(span.get("SpanName", "")).lower()
    attrs = span.get("SpanAttributes", {})
    if not isinstance(attrs, dict):
        attrs = {}

    # Check for LLM/generation spans
    if any(k in name for k in ("llm", "generation", "chat", "completion", "inference")):
        return "llm"
    if any(k.startswith(("gen_ai.", "llm.")) for k in attrs):
        return "llm"

    # Check for tool spans
    if any(k in name for k in ("tool", "function_call", "tool_call")):
        return "tool"
    if any(k.startswith("tool.") for k in attrs):
        return "tool"

    # Check for agent spans
    if any(k in name for k in ("agent", "step", "react")):
        return "agent"

    return "generic"
