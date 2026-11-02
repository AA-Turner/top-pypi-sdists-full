"""Validated presentation policy shared by foreground execution and explicit observers."""

from dataclasses import dataclass
from collections.abc import Mapping

import click
import json

from labqoat.cli.output.cli_failure import CliFailure
from labqoat.cli.console.metric_cadence import MetricCadence


@dataclass(frozen=True)
class ConsoleOptions:
    """Keep verbosity independent of source selection and build visibility."""

    level: str = "progress"
    sources: tuple[str, ...] = ()
    build_output: str = "auto"
    timestamps: str = "off"
    silent: bool = False
    json: bool = False
    grep: str = ""
    every: str = "auto"
    metrics: tuple[str, ...] = ()

    @classmethod
    def current(cls, values: Mapping[str, object]) -> "ConsoleOptions":
        """Honor local JSON flags and the existing global output mode."""
        raw = str(values.get("source") or "")
        sources = tuple(part.strip() for part in raw.split(",") if part.strip())
        known = {"system", "build", "stdout", "stderr", "logging", "metric", "app", "milestone", "progress"}
        if set(sources) - known:
            raise click.UsageError("Unknown --source; choose system, build, stdout, stderr, logging, metric, or app.")
        mode = CliFailure.output_mode(click.get_current_context(silent=True))
        return cls(
            str(values.get("level", "progress")),
            sources,
            str(values.get("build_output", "auto")),
            str(values.get("timestamps", "off")),
            bool(values.get("silent")),
            bool(values.get("json")) or mode != "human",
            str(values.get("grep") or ""),
            str(values.get("every") or "auto"),
            tuple(part.strip() for part in str(values.get("metrics") or "").split(",") if part.strip()),
        )

    def delivered_builds(self) -> str | None:
        """Name the build output the service may withhold because this console would discard it."""
        if self.build_output == "none":
            return "none"
        if self.build_output == "full" or "build" in self.sources:
            return None
        return "unfinished"

    @staticmethod
    def selection(values: Mapping[str, object]) -> dict[str, object]:
        """Encode repeated paths without making commas or slashes ambiguous in child keys."""
        result: dict[str, object] = {}
        if values.get("depth") is not None:
            result["depth"] = values["depth"]
        paths = values.get("run")
        if paths:
            result["run"] = paths if isinstance(paths, str) else json.dumps(paths, separators=(",", ":"))
        return result

    @staticmethod
    def cadence(_ctx: click.Context, _param: click.Parameter, value: str) -> str:
        """Reject malformed metric cadence during parsing, before accepting remote work."""
        try:
            MetricCadence(value)
        except ValueError as error:
            raise click.BadParameter(str(error)) from error
        return value

    @staticmethod
    def parameters(level: str = "progress") -> list[click.Parameter]:
        """Expose stable explicit controls without changing stream delivery."""
        return [
            click.Option(
                ["--every"],
                default="auto",
                callback=ConsoleOptions.cadence,
                help="Training metric spacing in steps or time, such as 500 or 2m.",
            ),
            click.Option(["--metrics"], help="Comma-separated metric names or glob patterns."),
            click.Option(["--depth"], type=click.IntRange(0, 64), help="Maximum child depth; zero selects this run."),
            click.Option(
                ["--run"],
                multiple=True,
                help="Select descendant UUIDs or operation-key paths; repeatable, supports * and ? wildcards.",
            ),
            click.Option(
                ["--level"], type=click.Choice(["debug", "info", "progress", "warning", "error"]), default=level
            ),
            click.Option(["--source"], help="Comma-separated sources; app means stdout, stderr, logging."),
            click.Option(
                ["--build-output"], type=click.Choice(["auto", "full", "errors-only", "none"]), default="auto"
            ),
            click.Option(
                ["-t", "--timestamps"],
                type=click.Choice(["off", "rel", "abs"]),
                default="off",
                flag_value="rel",
                is_flag=False,
            ),
            click.Option(["--json"], is_flag=True, help="Write compact JSON records to stdout."),
        ]
