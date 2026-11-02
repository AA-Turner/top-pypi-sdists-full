"""``compute settings set`` reads the current revision and applies one conditional merge patch."""

from __future__ import annotations

import click

from labqoat.cli.compute.settings_patch import SettingsPatch
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument


class SettingsSetCommand(StrictCommand):
    """Change only the selected limits; ``none`` makes an optional limit unbounded."""

    TIMINGS = ("machine_idle_seconds", "worker_idle_seconds", "queue_timeout_seconds")

    def __init__(self) -> None:
        """Declare limit, rate and timing options."""
        super().__init__("set", params=self.options(), help="Change workspace compute limits and idle delays.")

    @staticmethod
    def options() -> list[click.Parameter]:
        """Declare every settable field with its display unit."""
        return [
            click.Option(["--cpu"], type=str, help="Workload CPU limit in CPUs (fractions allowed) or 'none'."),
            click.Option(["--memory-gib", "memory_gib"], type=str, help="Workload memory limit in GiB or 'none'."),
            click.Option(["--gpus"], type=str, help="Total workload GPU devices or 'none'."),
            click.Option(
                ["--gpu-family-limit", "family_limits"],
                multiple=True,
                help="Per-family device ceiling such as nvidia:h100=4; FAMILY=none removes it. Repeatable.",
            ),
            click.Option(
                ["--clear-gpu-family-limits", "clear_family_limits"],
                is_flag=True,
                help="Remove all family ceilings before applying any --gpu-family-limit.",
            ),
            click.Option(["--rate"], type=str, help="Elastic instance-rate ceiling in USD per hour or 'none'."),
            click.Option(["--machine-idle-seconds", "machine_idle_seconds"], type=click.IntRange(min=0)),
            click.Option(["--worker-idle-seconds", "worker_idle_seconds"], type=click.IntRange(min=0)),
            click.Option(["--queue-timeout-seconds", "queue_timeout_seconds"], type=click.IntRange(min=1)),
        ]

    def invoke(self, ctx: click.Context) -> object:
        """Read the revision, build the patch from it and send one conditional update."""
        patch = self.patch(dict(ctx.params))
        client = ContextAccessor.current().compute()
        try:
            current = client.settings()
            ResultWriter().write_dict(client.update_settings(self.build(patch, current), str(current["revision"])))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def build(patch: SettingsPatch, current: JsonDocument) -> JsonDocument:
        """Report invalid flag values as usage errors before any update is sent."""
        try:
            return patch.build(current)
        except ValueError as error:
            ErrorReporter.report_usage(str(error))

    @staticmethod
    def patch(params: dict[str, object]) -> SettingsPatch:
        """Group parsed Click values into one settings patch description."""
        entries = params["family_limits"]
        timings = {name: SettingsSetCommand.seconds(params[name]) for name in SettingsSetCommand.TIMINGS}
        return SettingsPatch(
            cpu=SettingsSetCommand.text(params["cpu"]),
            memory_gib=SettingsSetCommand.text(params["memory_gib"]),
            gpus=SettingsSetCommand.text(params["gpus"]),
            family_limits=tuple(str(entry) for entry in entries) if isinstance(entries, tuple) else (),
            clear_family_limits=bool(params["clear_family_limits"]),
            rate=SettingsSetCommand.text(params["rate"]),
            timings=timings,
        )

    @staticmethod
    def text(value: object) -> str | None:
        """Keep omitted text options distinct from supplied values."""
        return None if value is None else str(value)

    @staticmethod
    def seconds(value: object) -> int | None:
        """Keep omitted timing options distinct from supplied whole seconds."""
        return value if isinstance(value, int) else None
