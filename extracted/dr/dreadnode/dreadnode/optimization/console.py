import statistics
import typing as t
from collections import deque

from rich import box
from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from dreadnode.optimization.events import (
    BudgetUpdated,
    CandidateAccepted,
    CandidateRejected,
    IterationStart,
    NewBestTrial,
    OptimizationEnd,
    OptimizationError,
    OptimizationEvent,
    OptimizationStart,
    ParetoFrontUpdated,
    StudyEnd,
    StudyEvent,
    TrialComplete,
    TrialFailed,
    TrialPruned,
    TrialStart,
    ValsetEvaluated,
)
from dreadnode.optimization.format import format_study_result, format_trial
from dreadnode.optimization.result import OptimizationResult, StudyResult

if t.TYPE_CHECKING:
    from dreadnode.optimization.api import Optimization
    from dreadnode.optimization.study import Study
    from dreadnode.optimization.trial import Trial


class StudyConsoleAdapter:
    """Consumes a Study's event stream and renders a live progress dashboard."""

    def __init__(
        self, study: "Study[t.Any]", *, console: Console | None = None, max_log_entries: int = 50
    ):
        self.study = study
        self.console = console or Console()

        self._best_trial: Trial | None = None
        self._result: StudyResult | None = None
        self._trials: deque[Trial] = deque(maxlen=max_log_entries)
        self._trial_map: dict[t.Any, Trial] = {}  # Map trial ID to trial object for updates

        self._trials_running = 0
        self._trials_completed = 0
        self._trials_since_best = 0
        self._total_cost = 0
        self._last_error: str | None = None

        self._progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=60),
            TextColumn("{task.completed}/{task.total} Evals"),
            SpinnerColumn("dots"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            expand=True,
        )
        self._progress_task_id: TaskID = self._progress.add_task(
            "[bold]Overall Progress", total=self.study.n_iterations
        )

    def _get_score_progress_indicator(self, trial_score: float) -> tuple[str, str]:
        """Returns (indicator_text, style) based on standard deviations from mean."""
        completed_scores = [
            t.score for t in self._trials if t.status == "finished" and t.score != -float("inf")
        ]

        if len(completed_scores) < 2:
            return "", "dim"

        try:
            mean_score = statistics.mean(completed_scores)
            std_dev = statistics.stdev(completed_scores)
        except statistics.StatisticsError:
            return "", "dim"

        if std_dev == 0:  # All scores are identical
            return "", "dim"

        z_score = (trial_score - mean_score) / std_dev

        # Color coding based on standard deviations
        if z_score >= 2.0:
            style = "green4"
        elif z_score >= 1.0:
            style = "dark_green"
        elif z_score <= -2.0:
            style = "deep_pink4"
        elif z_score <= -1.0:
            style = "dark_red"
        else:
            style = "dim"

        return f"{z_score:+.1f}", style

    def _build_header(self) -> RenderableType:
        grid = Table.grid(expand=True)
        grid.add_column("Best Score", justify="left", ratio=1)
        grid.add_column("Status", justify="right", ratio=2)

        best_score_text = "[dim]-[/dim]"
        if self._best_trial:
            # Get the latest state from the map
            best_trial = self._trial_map.get(self._best_trial.id, self._best_trial)
            best_score_text = f"[bold magenta]{best_trial.score:.5f}[/bold magenta]"

        status_text = Text.from_markup(
            f"Trials: [bold cyan]{self._trials_running}[/] running / [bold green]{self._trials_completed}[/] done | "
            f"Since Best: [bold magenta]{self._trials_since_best}[/] | "
            f"Total Cost: [bold]{self._total_cost}[/]"
        )

        grid.add_row(
            Text.from_markup(f"[b]Best Score:[/b] {best_score_text}"),
            status_text,
        )
        return grid

    def _build_best_trial_panel(self) -> RenderableType:
        if not self._best_trial:
            return Panel(
                Text("No successful trials yet.", style="dim", justify="center"),
                title="[bold magenta]Current Best[/bold magenta]",
                border_style="dim",
            )

        # Get the latest state from the map
        best_trial = self._trial_map.get(self._best_trial.id, self._best_trial)

        return Panel(
            format_trial(best_trial),
            title="[bold magenta]Current Best[/bold magenta]",
            border_style="magenta",
        )

    def _build_trials_panel(self) -> RenderableType:
        table = Table(expand=True, box=box.ROUNDED)
        table.add_column("ID", width=8)
        table.add_column("Status", width=8)
        table.add_column("Step", justify="right", style="dim")
        table.add_column("Score/σ", justify="right")

        for trial_ref in self._trials:
            # Get the latest trial state from the map (in case it was updated)
            trial = self._trial_map.get(trial_ref.id, trial_ref)

            color = {
                "finished": "default",
                "failed": "red",
                "pruned": "yellow",
                "running": "cyan",
            }.get(trial.status, "dim")
            status_text = f"[{color}]{trial.status}[/{color}]"

            if trial.status == "finished":
                indicator, indicator_style = self._get_score_progress_indicator(trial.score)
                score_str = f"[bold]{trial.score:.6f}[/bold] [{indicator_style}]{indicator}[/{indicator_style}]"
            else:
                score_str = "..."

            trial_id = Text(
                str(trial.id)[16:],
                style="bold magenta"
                if self._best_trial and trial.id == self._best_trial.id
                else "dim",
            )

            table.add_row(trial_id, status_text, str(trial.step), score_str)

        return Panel(
            table if self._trials else Text("No trials yet.", style="dim", justify="center"),
            title="[bold]Trials[/bold]",
            border_style="dim",
        )

    def _build_dashboard(self) -> RenderableType:
        layout = Layout()

        layout.split_column(
            Layout(Padding(self._build_header(), 1), size=3),
            Layout(Rule(style="cyan"), size=1),
            Layout(name="body"),
            Layout(Padding(self._progress, 1), size=3),
        )

        if self._last_error:
            layout.add_split(
                Layout(
                    Panel(
                        self._last_error,
                        title="Last Error",
                        title_align="left",
                        border_style="red",
                    ),
                    size=3,
                )
            )

        layout["body"].split_row(
            Layout(self._build_best_trial_panel(), name="left", ratio=3),
            Layout(self._build_trials_panel(), name="right", ratio=2),
        )

        return Layout(
            Panel(
                layout,
                title=Text(self.study.name, justify="center", style="bold cyan"),
                border_style="cyan",
            )
        )

    def _handle_event(self, event: StudyEvent[t.Any]) -> None:
        if isinstance(event, TrialStart):
            self._trials_running += 1
            if event.trial:
                self._trials.appendleft(event.trial)
                self._trial_map[event.trial.id] = event.trial
        elif isinstance(event, TrialComplete | TrialPruned | TrialFailed):
            self._trials_running -= 1
            self._trials_completed += 1
            if isinstance(event, TrialFailed):
                self._last_error = event.error
            # Update the trial in the map with the completed trial from the event
            if event.trial:
                self._trial_map[event.trial.id] = event.trial
        elif isinstance(event, NewBestTrial):
            self._best_trial = event.trial
            # Also update in the trial map
            if event.trial:
                self._trial_map[event.trial.id] = event.trial
        elif isinstance(event, StudyEnd):
            self._result = event.result

        # Update trials_since_best AFTER handling the event to get latest best_trial
        if self._best_trial:
            self._trials_since_best = self._trials_completed - self._best_trial.step

        self._progress.update(self._progress_task_id, completed=self._trials_completed)

    def _is_jupyter(self) -> bool:
        """Check if running in a Jupyter notebook environment."""
        try:
            from IPython import get_ipython

            ipy = get_ipython()
            if ipy is None:
                return False
            # Check for Jupyter kernel
            return "IPKernelApp" in ipy.config or "ZMQInteractiveShell" in type(ipy).__name__
        except Exception:
            return False

    def _display_multimodal_content(self, result: StudyResult[t.Any]) -> None:
        """Display images/audio from best trial in Jupyter notebooks."""
        if not self._is_jupyter():
            return

        if not result.best_trial or not result.best_trial.evaluation_result:
            return

        samples = result.best_trial.evaluation_result.samples
        if not samples:
            return

        sample = samples[0]
        if not hasattr(sample, "input") or not isinstance(sample.input, dict):
            return

        try:
            from IPython.display import Audio as IPAudio
            from IPython.display import display

            # Display image if present
            if "image" in sample.input:
                image = sample.input["image"]
                # Check if it's our Image type with to_pil method
                if hasattr(image, "to_pil"):
                    print("\n📷 Transformed Image (sent to model):")  # noqa: T201
                    display(image.to_pil())

            # Display audio if present
            if "audio" in sample.input:
                audio = sample.input["audio"]
                # Check if it's our Audio type with to_serializable method
                if hasattr(audio, "to_serializable"):
                    print("\n🔊 Transformed Audio (sent to model):")  # noqa: T201
                    audio_bytes, _ = audio.to_serializable()
                    display(IPAudio(audio_bytes, autoplay=False))

        except ImportError:
            pass  # IPython not available

    def _render_final_summary(self, result: StudyResult[t.Any]) -> None:
        """Renders a final, static summary of the study results."""
        self.console.print(
            Rule(f"[bold] {self.study.name}: Optimization Complete [/bold]", style="cyan")
        )
        self.console.print(
            Panel(format_study_result(result), border_style="dim", title="Study Summary")
        )
        self.console.print(
            Panel(
                format_trial(result.best_trial),
                title="[bold magenta]Best Trial[/bold magenta]",
                border_style="magenta",
            )
            if result.best_trial
            else Panel("[yellow]No successful trials were completed.[/yellow]")
        )

        # Auto-display multimodal content in Jupyter
        self._display_multimodal_content(result)

    async def run(self) -> StudyResult:
        with Live(self._build_dashboard(), console=self.console) as live:
            async with self.study.stream() as stream:
                async for event in stream:
                    self._handle_event(event)
                    live.update(self._build_dashboard())
                    live.refresh()  # Force immediate refresh after each event

        if self._result:
            self._render_final_summary(self._result)
            return self._result

        raise RuntimeError("Optimization did not produce a final result.")


class OptimizationConsoleAdapter:
    """Simple live console view for Dreadnode optimize_anything runs."""

    def __init__(self, optimization: "Optimization[t.Any]", *, console: Console | None = None):
        self.optimization = optimization
        self.console = console or Console()
        self._backend = "gepa"
        self._dataset_size = 0
        self._valset_size = 0
        self._uses_adapter = False
        self._iteration = 0
        self._accepted = 0
        self._rejected = 0
        self._metric_calls_used = 0
        self._metric_calls_remaining: int | None = None
        self._last_val_score: float | None = None
        self._best_score: float | None = None
        self._frontier_size = 0
        self._error: str | None = None
        self._result: OptimizationResult[t.Any] | None = None

    def _handle_event(self, event: OptimizationEvent[t.Any]) -> None:
        if isinstance(event, OptimizationStart):
            self._backend = event.backend
            self._dataset_size = event.dataset_size
            self._valset_size = event.valset_size
            self._uses_adapter = event.uses_adapter
        elif isinstance(event, IterationStart):
            self._iteration = event.iteration
        elif isinstance(event, CandidateAccepted):
            self._accepted += 1
        elif isinstance(event, CandidateRejected):
            self._rejected += 1
        elif isinstance(event, ValsetEvaluated):
            self._last_val_score = event.average_score
        elif isinstance(event, BudgetUpdated):
            self._metric_calls_used = event.metric_calls_used
            self._metric_calls_remaining = event.metric_calls_remaining
        elif isinstance(event, ParetoFrontUpdated):
            self._frontier_size = event.frontier_size
            if event.iteration is not None:
                self._iteration = event.iteration
            if event.best_score is not None:
                self._best_score = event.best_score
        elif isinstance(event, OptimizationError):
            self._error = event.error
        elif isinstance(event, OptimizationEnd):
            self._result = event.result
            self._best_score = event.best_score
            self._frontier_size = event.frontier_size

    def _build_panel(self) -> RenderableType:
        table = Table.grid(expand=True)
        table.add_column(ratio=1)
        table.add_column(ratio=2)
        table.add_row("Backend", self._backend)
        table.add_row("Trainset", str(self._dataset_size))
        table.add_row("Valset", str(self._valset_size))
        table.add_row("Adapter", "yes" if self._uses_adapter else "no")
        table.add_row("Iteration", str(self._iteration))
        table.add_row(
            "Best Score",
            f"{self._best_score:.5f}" if self._best_score is not None else "-",
        )
        table.add_row(
            "Last Val",
            f"{self._last_val_score:.5f}" if self._last_val_score is not None else "-",
        )
        table.add_row("Frontier", str(self._frontier_size))
        table.add_row("Accepted", str(self._accepted))
        table.add_row("Rejected", str(self._rejected))
        table.add_row("Metric Calls", str(self._metric_calls_used))
        table.add_row(
            "Remaining",
            str(self._metric_calls_remaining) if self._metric_calls_remaining is not None else "-",
        )
        if self._error:
            table.add_row("Error", self._error)
        return Panel(
            table,
            title=f"[bold cyan]{self.optimization.name}[/bold cyan]",
            border_style="cyan",
        )

    async def run(self) -> OptimizationResult[t.Any]:
        with Live(self._build_panel(), console=self.console) as live:
            async with self.optimization.stream() as stream:
                async for event in stream:
                    self._handle_event(event)
                    live.update(self._build_panel())
                    live.refresh()

        if self._result is not None:
            return self._result
        raise RuntimeError("Optimization did not produce a final result.")
