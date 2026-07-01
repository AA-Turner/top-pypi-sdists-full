"""Evaluations Dashboard screen -- view evaluation jobs with progress."""

from __future__ import annotations

import asyncio
import typing as t
from datetime import UTC, datetime

from textual import events, on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static, Tree

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import (
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    SUCCESS,
    WARNING,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.timer import Timer

    from dreadnode.app.api.client import ApiClient

try:
    from textual_plot import PlotWidget

    _HAS_PLOT = True
except ImportError:
    _HAS_PLOT = False

# -- Status dot helper -------------------------------------------------------

_STATUS_DOT: dict[str, str] = {
    "completed": f"[{SUCCESS}]\u25cf[/]",
    "running": f"[{WARNING}]\u25cf[/]",
    "claiming": f"[{WARNING}]\u25cf[/]",
    "provisioning": f"[{WARNING}]\u25cf[/]",
    "agent_running": f"[{WARNING}]\u25cf[/]",
    "failed": f"[{ERROR}]\u25cf[/]",
    "cancelled": f"[{ERROR}]\u25cf[/]",
    "timed_out": f"[{ERROR}]\u25cf[/]",
    "pending": f"[{INFO}]\u25cf[/]",
    "queued": f"[{INFO}]\u25cf[/]",
}


def _status_dot(status: str) -> str:
    return _STATUS_DOT.get(status, f"[{FG_SUBTLE}]\u25cf[/]")


# -- Formatting helpers ------------------------------------------------------


def _fmt_timestamp(ts: str | datetime | None) -> str:
    """Format an ISO timestamp for display."""
    if ts is None:
        return "-"
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return ts[:19]
    else:
        dt = ts
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _fmt_duration(start: str | datetime | None, end: str | datetime | None) -> str:
    """Format the duration between two timestamps."""
    if start is None:
        return "-"

    def _parse(ts: str | datetime) -> datetime | None:
        if isinstance(ts, datetime):
            return ts
        try:
            return datetime.fromisoformat(ts)
        except ValueError:
            return None

    dt_start = _parse(start)
    if dt_start is None:
        return "-"

    if end is not None:
        dt_end = _parse(end)
    else:
        dt_end = datetime.now(tz=UTC)

    if dt_end is None:
        return "-"

    if dt_start.tzinfo is None:
        dt_start = dt_start.replace(tzinfo=UTC)
    if dt_end.tzinfo is None:
        dt_end = dt_end.replace(tzinfo=UTC)

    delta_secs = int((dt_end - dt_start).total_seconds())
    if delta_secs < 0:
        return "-"
    if delta_secs < 60:
        return f"{delta_secs}s"
    mins = delta_secs // 60
    secs = delta_secs % 60
    if mins < 60:
        return f"{mins}m{secs:02d}s"
    hours = mins // 60
    remaining_mins = mins % 60
    return f"{hours}h{remaining_mins:02d}m"


def _fmt_progress(counts: dict[str, t.Any]) -> str:
    """Build a progress string like '45/100' from item counts."""
    finished = (
        int(counts.get("passed", 0))
        + int(counts.get("failed", 0))
        + int(counts.get("timed_out", 0))
        + int(counts.get("cancelled", 0))
        + int(counts.get("infra_error", 0))
    )
    total = finished + (
        int(counts.get("queued", 0))
        + int(counts.get("claiming", 0))
        + int(counts.get("provisioning", 0))
        + int(counts.get("agent_running", 0))
        + int(counts.get("agent_finished", 0))
        + int(counts.get("verifying", 0))
    )
    if total == 0:
        return "-"
    return f"{finished}/{total}"


def _fmt_pass_rate(counts: dict[str, t.Any]) -> str:
    """Calculate and format pass rate from item counts."""
    passed = int(counts.get("passed", 0))
    failed = int(counts.get("failed", 0))
    total_decided = passed + failed
    if total_decided == 0:
        return "-"
    rate = passed / total_decided * 100
    return f"{rate:.0f}%"


def _progress_bar(counts: dict[str, t.Any], width: int = 20) -> str:
    """Build a text progress bar from item counts."""
    passed = int(counts.get("passed", 0))
    failed = int(counts.get("failed", 0))
    timed_out = int(counts.get("timed_out", 0))
    infra_error = int(counts.get("infra_error", 0))
    cancelled = int(counts.get("cancelled", 0))
    in_progress = (
        int(counts.get("queued", 0))
        + int(counts.get("claiming", 0))
        + int(counts.get("provisioning", 0))
        + int(counts.get("agent_running", 0))
        + int(counts.get("agent_finished", 0))
        + int(counts.get("verifying", 0))
    )
    total = passed + failed + timed_out + infra_error + cancelled + in_progress
    if total == 0:
        return f"[{FG_SUBTLE}]{'░' * width}[/]"

    def _fill(count: int) -> int:
        return max(1, int(count / total * width)) if count > 0 else 0

    bar = ""
    remaining = width

    for count, colour, char in [
        (passed, SUCCESS, "█"),
        (failed, ERROR, "█"),
        (timed_out, WARNING, "█"),
        (infra_error, ERROR, "▓"),
        (cancelled, FG_SUBTLE, "▓"),
    ]:
        if count > 0:
            filled = min(_fill(count), remaining)
            bar += f"[{colour}]{char * filled}[/]"
            remaining -= filled

    if in_progress > 0 and remaining > 0:
        filled = min(_fill(in_progress), remaining)
        bar += f"[{INFO}]{'░' * filled}[/]"
        remaining -= filled

    if remaining > 0:
        bar += f"[{FG_SUBTLE}]{'░' * remaining}[/]"

    return bar


# ============================================================================
# EvaluationsScreen
# ============================================================================


class EvaluationsScreen(DreadnodeScreen):
    """View evaluation jobs with progress and details."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("r", "refresh_evaluations", "Refresh", show=True),
        Binding("c", "cancel_evaluation", "Cancel", show=True),
        Binding("t", "retry_evaluation", "Retry", show=True),
    ]

    def __init__(
        self,
        api: ApiClient,
        org: str,
        workspace: str,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._org = org
        self._workspace = workspace

        # Data
        self._evaluations: list[dict[str, t.Any]] = []
        self._refresh_timer: Timer | None = None

    # ------------------------------------------------------------------ compose

    _SUBTITLE = f"\n[{FG_FAINTEST}] Run and monitor capability evaluations[/]"

    def compose_content(self) -> ComposeResult:
        yield Static(
            f"[bold {FG}] Evaluations[/]{self._SUBTITLE}",
            id="eval-title",
        )
        with Horizontal(id="eval-body"):
            with Vertical(id="eval-left"):
                yield DataTable(id="eval-table")
                yield Static("", id="eval-progress-bar")
            with Vertical(id="eval-right"):
                yield Tree("Detail", id="eval-detail")
                if _HAS_PLOT:
                    yield PlotWidget(id="eval-chart")

    # ------------------------------------------------------------------ mount

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#eval-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("", "Name", "Progress", "Pass Rate", "Duration", "Created")

        self._load_evaluations()
        self._start_refresh_timer()

    def on_unmount(self) -> None:
        self._stop_refresh_timer()

    def on_screen_suspend(self, _event: events.ScreenSuspend) -> None:
        self._stop_refresh_timer()

    def on_screen_resume(self, _event: events.ScreenResume) -> None:
        self._load_evaluations()
        self._start_refresh_timer()

    def _start_refresh_timer(self) -> None:
        if self._refresh_timer is None:
            self._refresh_timer = self.set_interval(5.0, self._load_evaluations)

    def _stop_refresh_timer(self) -> None:
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    # ------------------------------------------------------------------ actions

    def action_go_back(self) -> None:
        self._stop_refresh_timer()
        self.dismiss()

    def action_cursor_down(self) -> None:
        table = self.query_one("#eval-table", DataTable)
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        table = self.query_one("#eval-table", DataTable)
        table.action_cursor_up()

    def action_refresh_evaluations(self) -> None:
        self._load_evaluations()

    def action_cancel_evaluation(self) -> None:
        eval_id = self._selected_evaluation_id()
        if eval_id:
            self._do_cancel(eval_id)

    def action_retry_evaluation(self) -> None:
        eval_id = self._selected_evaluation_id()
        if eval_id:
            self._do_retry(eval_id)

    # ------------------------------------------------------------------ helpers

    def _selected_evaluation_id(self) -> str | None:
        """Return the evaluation ID of the currently highlighted row."""
        table = self.query_one("#eval-table", DataTable)
        if table.cursor_row is None:
            return None
        try:
            row_key = table.coordinate_to_cell_key((table.cursor_row, 0)).row_key
            return str(row_key.value) if row_key else None
        except Exception:
            return None

    def _selected_evaluation(self) -> dict[str, t.Any] | None:
        """Return the full evaluation dict for the currently highlighted row."""
        eval_id = self._selected_evaluation_id()
        if eval_id is None:
            return None
        for ev in self._evaluations:
            if str(ev.get("id", "")) == eval_id:
                return ev
        return None

    def _flash_title(self, message: str = "", colour: str = FG_MUTED) -> None:
        title = self.query_one("#eval-title", Static)
        suffix = f"  [{colour}]{message}[/]" if message else ""
        title.update(f"[bold {FG}] Evaluations[/]{suffix}{self._SUBTITLE}")

    # ------------------------------------------------------------------ data loading

    @work(exclusive=True, group="evaluations")
    async def _load_evaluations(self) -> None:
        """Fetch evaluation jobs from the platform API."""
        if not self.is_mounted:
            return
        table = self.query_one("#eval-table", DataTable)
        table.clear()

        self._flash_title("\u2026", FG_FAINTEST)

        try:
            data = await asyncio.to_thread(
                self._api.list_evaluation_jobs,
                self._org,
                self._workspace,
                page=1,
                page_size=50,
            )
            self._evaluations = data.get("items", [])
        except Exception as exc:
            self._flash_title(f"Error: {exc}", ERROR)
            return

        if not self.is_mounted:
            return

        if not self._evaluations:
            self._flash_title()
            self._clear_detail()
            self._update_progress_bar(None)
            return

        for ev in self._evaluations:
            job_status = ev.get("job_status", "unknown")
            name = ev.get("name", "unnamed")
            counts = ev.get("item_counts", {})
            progress = _fmt_progress(counts)
            pass_rate = _fmt_pass_rate(counts)
            duration = _fmt_duration(
                ev.get("started_at") or ev.get("queued_at"),
                ev.get("completed_at"),
            )
            created = _fmt_timestamp(ev.get("queued_at"))

            table.add_row(
                _status_dot(job_status),
                name,
                progress,
                pass_rate,
                duration,
                created,
                key=str(ev.get("id", "")),
            )

        total = data.get("total", len(self._evaluations))
        self._flash_title(str(total))

        if self._evaluations:
            self._show_evaluation_detail(self._evaluations[0])
            self._update_progress_bar(self._evaluations[0])
            self._update_chart()

    # ------------------------------------------------------------------ events

    @on(DataTable.RowHighlighted, "#eval-table")
    def _on_evaluation_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        eval_id = str(event.row_key.value)
        for ev in self._evaluations:
            if str(ev.get("id", "")) == eval_id:
                self._show_evaluation_detail(ev)
                self._update_progress_bar(ev)
                break

    # ------------------------------------------------------------------ detail panel

    def _clear_detail(self) -> None:
        detail = self.query_one("#eval-detail", Tree)
        detail.clear()
        detail.root.set_label("[dim]No evaluation selected[/]")

    def _show_evaluation_detail(self, ev: dict[str, t.Any]) -> None:
        """Populate the right-hand detail tree with evaluation info."""
        detail = self.query_one("#eval-detail", Tree)
        detail.clear()

        name = ev.get("name", "unnamed")
        detail.root.set_label(f"[bold]Eval: {name}[/]")

        job_status = ev.get("job_status", "unknown")
        status_colour = {
            "completed": SUCCESS,
            "running": WARNING,
            "failed": ERROR,
            "cancelled": ERROR,
            "timed_out": ERROR,
            "pending": INFO,
            "queued": INFO,
        }.get(job_status, FG_SUBTLE)

        # Basic info
        info_node = detail.root.add("Info", expand=True)
        info_node.add_leaf(f"ID: [{FG_SUBTLE}]{ev.get('id', 'n/a')}[/]")
        info_node.add_leaf(f"Status: [{status_colour}]{job_status}[/]")
        info_node.add_leaf(f"Kind: [{FG_SUBTLE}]{ev.get('kind', 'n/a')}[/]")
        info_node.add_leaf(f"Model: [{FG_SUBTLE}]{ev.get('model') or 'default'}[/]")
        info_node.add_leaf(f"Agent Type: [{FG_SUBTLE}]{ev.get('agent_type') or 'n/a'}[/]")

        # Concurrency
        config_node = detail.root.add("Config", expand=True)
        config_node.add_leaf(
            f"Concurrency: [{FG}]{ev.get('requested_concurrency', '?')}"
            f" (eff: {ev.get('effective_concurrency', '?')})[/]"
        )
        config_node.add_leaf(f"Dataset Size: [{FG}]{ev.get('dataset_size', 0)}[/]")
        if ev.get("task_timeout_sec"):
            config_node.add_leaf(f"Timeout: [{FG}]{ev['task_timeout_sec']}s[/]")
        config_node.add_leaf(f"Cleanup: [{FG_SUBTLE}]{ev.get('cleanup_policy', 'n/a')}[/]")

        # Item counts
        counts = ev.get("item_counts", {})
        if counts:
            counts_node = detail.root.add("Item Counts", expand=True)
            for field_name in [
                "queued",
                "claiming",
                "provisioning",
                "agent_running",
                "agent_finished",
                "verifying",
                "passed",
                "failed",
                "timed_out",
                "cancelled",
                "infra_error",
            ]:
                count = int(counts.get(field_name, 0))
                if count > 0:
                    field_colour = {
                        "passed": SUCCESS,
                        "failed": ERROR,
                        "timed_out": WARNING,
                        "infra_error": ERROR,
                        "cancelled": FG_SUBTLE,
                    }.get(field_name, INFO)
                    counts_node.add_leaf(f"{field_name}: [{field_colour}]{count}[/]")

        # Runtime costs
        costs = ev.get("runtime_costs", {})
        if costs:
            cost_node = detail.root.add("Costs", expand=True)
            cost_node.add_leaf(f"Sandboxes: [{FG}]{costs.get('sandbox_count', 0)}[/]")
            cost_node.add_leaf(f"Billed: [{FG}]{costs.get('billed_credits', 0)}[/]")
            cost_node.add_leaf(f"Running: [{FG}]{costs.get('running_credits', 0)}[/]")
            cost_node.add_leaf(f"Est. Total: [{FG}]{costs.get('estimated_total_credits', 0)}[/]")

        # Timing
        timing_node = detail.root.add("Timing", expand=True)
        timing_node.add_leaf(f"Queued: [{FG_SUBTLE}]{_fmt_timestamp(ev.get('queued_at'))}[/]")
        timing_node.add_leaf(f"Started: [{FG_SUBTLE}]{_fmt_timestamp(ev.get('started_at'))}[/]")
        timing_node.add_leaf(f"Completed: [{FG_SUBTLE}]{_fmt_timestamp(ev.get('completed_at'))}[/]")

        # Error
        error = ev.get("error_summary")
        if error:
            detail.root.add_leaf(f"[{ERROR}]Error: {error}[/]")

        # Run ID
        run_id = ev.get("run_id")
        if run_id:
            detail.root.add_leaf(f"Run ID: [{FG_SUBTLE}]{run_id}[/]")

        detail.root.expand()

    # ------------------------------------------------------------------ progress bar

    def _update_progress_bar(self, ev: dict[str, t.Any] | None) -> None:
        """Update the progress bar widget for the selected evaluation."""
        bar_widget = self.query_one("#eval-progress-bar", Static)
        if ev is None:
            bar_widget.update("")
            return

        counts = ev.get("item_counts", {})
        bar = _progress_bar(counts, width=40)
        progress = _fmt_progress(counts)
        pass_rate = _fmt_pass_rate(counts)

        bar_widget.update(f" {bar} [{FG}]{progress}[/] [{FG_SUBTLE}]pass: {pass_rate}[/]")

    # ------------------------------------------------------------------ chart

    def _update_chart(self) -> None:
        """Show pass/fail distribution as a bar chart."""
        if not _HAS_PLOT:
            return
        try:
            chart = self.query_one("#eval-chart", PlotWidget)
        except Exception:
            return
        chart.clear()
        if not self._evaluations:
            return

        names: list[str] = []
        pass_rates: list[float] = []
        for ev in self._evaluations[:15]:
            name = ev.get("name", "?")
            if len(name) > 15:
                name = name[:12] + "..."
            names.append(name)

            counts = ev.get("item_counts", {})
            passed = int(counts.get("passed", 0))
            failed = int(counts.get("failed", 0))
            total = passed + failed
            pass_rates.append(passed / total * 100 if total > 0 else 0)

        if not pass_rates:
            return

        x = list(range(len(pass_rates)))
        chart.plt.bar(x=x, y=pass_rates)
        chart.plt.title = "Pass Rate (%)"

    # ------------------------------------------------------------------ evaluation actions

    @work(exclusive=True, group="eval-action")
    async def _do_cancel(self, eval_id: str) -> None:
        self.notify(f"Cancelling {eval_id[:8]}...", title="Evaluations", severity="warning")
        try:
            await asyncio.to_thread(
                self._api.cancel_evaluation,
                self._org,
                self._workspace,
                eval_id,
            )
            self.notify("Evaluation cancelled", title="Evaluations", severity="information")
        except Exception as exc:
            self.notify(f"Cancel failed: {exc}", title="Evaluations", severity="error")
        self._load_evaluations()

    @work(exclusive=True, group="eval-action")
    async def _do_retry(self, eval_id: str) -> None:
        self.notify(
            f"Retrying failed items {eval_id[:8]}...",
            title="Evaluations",
            severity="information",
        )
        try:
            await asyncio.to_thread(
                self._api.retry_failed_evaluation,
                self._org,
                self._workspace,
                eval_id,
            )
            self.notify("Retrying failed items", title="Evaluations", severity="information")
        except Exception as exc:
            self.notify(f"Retry failed: {exc}", title="Evaluations", severity="error")
        self._load_evaluations()
