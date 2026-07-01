import typing as t
from pathlib import Path

from rich import box
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dreadnode.core.scorer import Scorer
from dreadnode.core.util import get_callable_name, shorten_string

if t.TYPE_CHECKING:
    from dreadnode.core.types import Audio, Image
    from dreadnode.optimization import Study
    from dreadnode.optimization.result import StudyResult
    from dreadnode.optimization.trial import Trial


def _format_image(image: "Image", source_path: str | None = None) -> RenderableType:
    """Format an Image object for console display with clickable path."""
    try:
        pil_img = image.to_pil()
        width, height = pil_img.size
        mode = pil_img.mode
        img_format = getattr(image, "_format", "unknown") or "unknown"

        if not source_path:
            source_metadata = getattr(image, "_source_metadata", {})
            source_path = source_metadata.get("source-path")

        grid = Table.grid(padding=(0, 1))
        grid.add_column()

        if source_path:
            abs_path = str(Path(source_path).resolve())
            grid.add_row(Text(f"file://{abs_path}", style="link file://" + abs_path))

        grid.add_row(Text(f"📷 {width}x{height} {mode} ({img_format})", style="dim"))
    except Exception:
        return Text("📷 [Image]", style="dim")
    else:
        return grid


def _format_audio(audio: "Audio", source_path: str | None = None) -> RenderableType:
    """Format an Audio object for console display with clickable path."""
    try:
        sample_rate = getattr(audio, "_sample_rate", None)
        audio_format = getattr(audio, "_format", None)

        if not source_path:
            audio_data = getattr(audio, "_data", None)
            if isinstance(audio_data, (str, Path)) and Path(audio_data).exists():
                source_path = str(audio_data)

        grid = Table.grid(padding=(0, 1))
        grid.add_column()

        if source_path:
            abs_path = str(Path(source_path).resolve())
            grid.add_row(Text(f"file://{abs_path}", style="link file://" + abs_path))
            if not audio_format:
                audio_format = Path(source_path).suffix.lstrip(".").lower() or "wav"

        info_parts = ["🔊"]
        if sample_rate is not None:
            info_parts.append(f"{sample_rate}Hz")
        if audio_format:
            info_parts.append(f"({audio_format})")
        grid.add_row(Text(" ".join(info_parts), style="dim"))
    except Exception:
        return Text("🔊 [Audio]", style="dim")
    else:
        return grid


def _format_multimodal_input(input_data: dict[str, t.Any]) -> RenderableType:
    """Format a multimodal input dict with proper rendering for each modality."""
    from dreadnode.core.types import Audio, Image

    elements: list[RenderableType] = []

    # Format text prompt (check both "goal" and "prompt" for compatibility)
    text_content = input_data.get("goal") or input_data.get("prompt")
    if text_content:
        prompt_text = shorten_string(str(text_content), max_length=500, separator="\n\n[...]\n\n")
        elements.append(
            Panel(Text(prompt_text), title="📝 Prompt", title_align="left", border_style="blue")
        )

    # Format image if present
    if "image" in input_data and isinstance(input_data["image"], Image):
        image_path = input_data.get("image_path")
        elements.append(
            Panel(
                _format_image(input_data["image"], source_path=image_path),
                title="🖼️ Image",
                title_align="left",
                border_style="green",
            )
        )

    # Format audio if present
    if "audio" in input_data and isinstance(input_data["audio"], Audio):
        audio_path = input_data.get("audio_path")
        elements.append(
            Panel(
                _format_audio(input_data["audio"], source_path=audio_path),
                title="🎵 Audio",
                title_align="left",
                border_style="yellow",
            )
        )

    return Group(*elements) if elements else Text("[No input]", style="dim")


def _is_multimodal_input(input_data: t.Any) -> bool:
    """Check if input contains multimodal content (image/audio)."""
    if not isinstance(input_data, dict):
        return False
    return "image" in input_data or "audio" in input_data


def format_studies(studies: "t.Sequence[Study]") -> RenderableType:
    """
    Takes a list of Study objects and formats them into a concise rich Table.
    """
    table = Table(box=box.ROUNDED)
    table.add_column("Name", style="orange_red1", no_wrap=True)
    table.add_column("Description", min_width=20)
    table.add_column("Objectives", style="cyan")
    table.add_column("Sampler", style="cyan")

    for study in studies:
        objective_names = ", ".join(study.objective_names)
        sampler_name = getattr(study.sampler, "name", type(study.sampler).__name__)
        table.add_row(
            study.name,
            study.description or "-",
            objective_names,
            sampler_name,
        )

    return table


def format_study(study: "Study") -> RenderableType:
    """
    Format a single Study object into a detailed rich Panel.
    """

    details = Table(
        box=box.MINIMAL,
        show_header=False,
        style="orange_red1",
    )
    details.add_column("Property", style="bold dim", justify="right", no_wrap=True)
    details.add_column("Value", style="white")

    details.add_row(Text("Description", justify="right"), study.description or "-")
    details.add_row(Text("Objective", justify="right"), get_callable_name(study.objective))

    sampler_name = getattr(study.sampler, "name", type(study.sampler).__name__)
    details.add_row(Text("Sampler", justify="right"), sampler_name)

    # Format objective directions
    if study.objective_names:
        objectives = " | ".join(
            f"[cyan]{name} :arrow_upper_right:[/]"
            if direction == "maximize"
            else f"[magenta]{name} :arrow_lower_right:[/]"
            for name, direction in zip(study.objective_names, study.directions, strict=True)
        )
        details.add_row(Text("Objectives", justify="right"), objectives)

    if study.constraints:
        constraint_names = ", ".join(
            f"[cyan]{c.name}[/]" for c in Scorer.fit_many(study.constraints)
        )
        details.add_row(Text("Constraints", justify="right"), constraint_names)

    if study.stop_conditions:
        stop_names = ", ".join(f"[yellow]{cond.name}[/]" for cond in study.stop_conditions)
        details.add_row(Text("Stops", justify="right"), stop_names)

    return Panel(
        details,
        title=f"[bold]{study.name}[/]",
        title_align="left",
        border_style="orange_red1",
    )


def format_study_result(result: "StudyResult") -> RenderableType:
    """
    Format a StudyResult into a rich Table.
    """
    table = Table.grid(padding=(0, 2))
    table.add_column("Metric", style="dim")
    table.add_column("Value")
    table.add_row("Stop Reason:", f"[bold]{result.stop_reason}[/bold]")
    table.add_row("Explanation:", result.stop_explanation or "-")
    if (num_failed_trials := len(result.failed_trials)) > 0:
        table.add_row("Failed Trials:", f"[red]{num_failed_trials}[/red]")
    if (num_pruned_trials := len(result.pruned_trials)) > 0:
        table.add_row("Pruned Trials:", f"[yellow]{num_pruned_trials}[/yellow]")
    if (num_pending_trials := len(result.pending_trials)) > 0:
        table.add_row("Pending Trials:", f"[dim]{num_pending_trials}[/dim]")
    table.add_row("Total Trials:", str(len(result.trials)))

    return table


def format_trial(trial: "Trial[t.Any]") -> RenderableType:
    """
    Format a Trial object into a rich Table.
    """
    table = Table.grid(padding=(0, 2))
    table.add_column("Name")
    table.add_column("Score", justify="right", min_width=10)
    for name, value in trial.scores.items():
        table.add_row(
            name,
            f"[bold magenta]{value:.6f}[/bold magenta]",
        )

    for name, value in trial.all_scores.items():
        if name not in trial.scores:
            table.add_row(f"[dim]{name}[/dim]", f"[dim]{value:.6f}[/dim]")

    # Main content grid
    candidate_str = shorten_string(str(trial.candidate), max_length=500, separator="\n\n[...]\n\n")

    # Try to get transformed input and output from evaluation_result samples
    transformed_input_data: dict[str, t.Any] | None = None
    output_str = ""
    has_multimodal = False

    if (
        hasattr(trial, "evaluation_result")
        and trial.evaluation_result
        and trial.evaluation_result.samples
    ):
        first_sample = trial.evaluation_result.samples[0]

        # Get transformed input (what was actually sent to target)
        if (
            hasattr(first_sample, "input")
            and first_sample.input is not None
            and _is_multimodal_input(first_sample.input)
        ):
            has_multimodal = True
            transformed_input_data = first_sample.input

        # Get output
        if hasattr(first_sample, "output") and first_sample.output is not None:
            output_str = shorten_string(
                str(first_sample.output), max_length=500, separator="\n\n[...]\n\n"
            )

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Panel(table, title="Scores", title_align="left"))

    if has_multimodal and transformed_input_data:
        # Use multimodal formatter for rich display
        grid.add_row(
            Panel(
                _format_multimodal_input(transformed_input_data),
                title="Input (Multimodal)",
                title_align="left",
                border_style="cyan",
            )
        )
    else:
        # Standard text display
        grid.add_row(
            Panel(
                Text(candidate_str, style="dim"),
                title="Candidate",
                title_align="left",
            )
        )

    if output_str:
        import re

        tool_calls_display = None
        display_output = output_str

        # Check for tool calls markers (support both old and new format)
        tool_match = re.search(
            r"=== TOOL CALLS (?:MADE|EXECUTED) ===\n(.*?)===+",
            output_str,
            re.DOTALL,
        )
        if tool_match:
            tool_calls_display = tool_match.group(1).strip()
            display_output = re.sub(
                r"=== TOOL CALLS (?:MADE|EXECUTED) ===\n.*?===+\n*",
                "",
                output_str,
                flags=re.DOTALL,
            ).strip()
        elif "=== NO TOOL CALLS ===" in output_str:
            tool_calls_display = "[dim]None[/dim]"
            display_output = output_str.replace("=== NO TOOL CALLS ===", "").strip()

        # Add Tool Calls panel if present
        if tool_calls_display:
            grid.add_row(
                Panel(
                    Text.from_markup(tool_calls_display)
                    if "[" in tool_calls_display
                    else Text(tool_calls_display, style="bold cyan"),
                    title="🔧 Tool Calls",
                    title_align="left",
                    border_style="red" if tool_calls_display != "[dim]None[/dim]" else "dim",
                )
            )

        # Add Output panel with cleaned output
        if display_output:
            grid.add_row(
                Panel(Text(display_output, style="dim"), title="Output", title_align="left")
            )
    else:
        pass  # No output to display

    # Show evaluation result summary if available
    if trial.evaluation_result and trial.evaluation_result.samples:
        result_str = f"Samples: {len(trial.evaluation_result.samples)}, Pass rate: {trial.evaluation_result.pass_rate:.1%}"
        grid.add_row(Panel(Text(result_str, style="dim"), title="Evaluation", title_align="left"))

    return grid
