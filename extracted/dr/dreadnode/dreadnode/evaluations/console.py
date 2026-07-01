from collections import deque
from datetime import datetime

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text

from dreadnode.evaluations.evaluation import Evaluation
from dreadnode.evaluations.events import (
    EvalEnd,
    EvalEvent,
    EvalSample,
    EvalStart,
)
from dreadnode.evaluations.format import format_eval_result
from dreadnode.evaluations.result import EvalResult


class EvalConsoleAdapter:
    """Consumes an Eval's event stream and renders a live progress dashboard."""

    def __init__(
        self,
        eval: Evaluation,
        *,
        console: Console | None = None,
        max_events_to_show: int = 10,
    ):
        self.eval = eval
        self.console = console or Console()
        self.final_result: EvalResult | None = None
        self.max_events_to_show = max_events_to_show
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            "•",
            TimeRemainingColumn(),
            expand=True,
        )
        self._event_log: deque[str] = deque(maxlen=max_events_to_show)
        self._task_id: TaskID | None = None
        self._total_samples = 0
        self._passed_count = 0
        self._failed_count = 0
        self._error_count = 0

    def _build_summary_table(self) -> Table:
        success_rate = (
            f"{self._passed_count / self._total_samples:.1%}" if self._total_samples > 0 else "N/A"
        )
        table = Table.grid(expand=True)
        table.add_column("Statistic", style="dim")
        table.add_column("Value")
        table.add_row("Pass Rate:", success_rate)
        table.add_row("Samples:", str(self._total_samples))
        table.add_row("  Passed:", f"[green]{self._passed_count}[/green]")
        table.add_row("  Failed:", f"[yellow]{self._failed_count}[/yellow]")
        table.add_row("  Errors:", f"[red]{self._error_count}[/red]")
        return table

    def _build_dashboard(self) -> Panel:
        events_panel = Panel(
            "\n".join(self._event_log),
            title="[dim]Events[/dim]",
            border_style="dim",
        )
        stats_panel = Panel(
            self._build_summary_table(),
            title="[dim]Summary[/dim]",
            border_style="dim",
        )

        layout = Layout()

        layout.split_column(
            Layout(Padding(self._progress, (1, 0, 0, 0)), name="progress", size=4),
            Layout(name="bottom"),
        )

        layout["bottom"].split_row(
            Layout(events_panel, ratio=2),
            Layout(stats_panel, ratio=1),
        )

        eval_name = (
            self.eval.name or self.eval.task
            if isinstance(self.eval.task, str)
            else self.eval.task.name
        )

        return Panel(
            layout,
            title=Text(f"Evaluating '{eval_name}'", justify="center", style="bold"),
            border_style="cyan",
            height=self.max_events_to_show + 10,
        )

    def _log_event(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")  # noqa: DTZ005 - local time for console display
        self._event_log.append(f"[dim]{timestamp}[/dim] {message}")

    def _handle_event(self, event: EvalEvent) -> None:
        """Update state based on incoming event."""
        if isinstance(event, EvalStart):
            self._log_event("Evaluation started.")
            self._task_id = self._progress.add_task(
                "[bold]Progress", total=event.dataset_size * event.iterations
            )
        elif isinstance(event, EvalSample):
            self._total_samples += 1
            if event.error:
                self._error_count += 1
                self._log_event(f"[red]ERROR[/red] {event.error[:80]}")
            elif event.passed is False:
                self._failed_count += 1
            else:
                self._passed_count += 1
            if self._task_id is not None:
                self._progress.update(self._task_id, advance=1)
        elif isinstance(event, EvalEnd):
            self._progress.stop()
            self._log_event(
                f"[bold]Evaluation complete: {event.result.stop_reason if event.result else 'unknown'}[/bold]"
            )
            self.final_result = event.result

    async def run(self) -> EvalResult:
        """Run the evaluation and render the console interface."""
        with Live(self._build_dashboard(), console=self.console) as live:
            async with self.eval.stream() as stream:
                async for event in stream:
                    self._handle_event(event)
                    live.update(self._build_dashboard(), refresh=True)

        if self.final_result:
            self.console.print(format_eval_result(self.final_result))
            return self.final_result

        raise RuntimeError("Evaluation did not produce a final result.")
