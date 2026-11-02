"""``compute hosts share`` sets the resources Labqoat may use on a connected machine."""

from __future__ import annotations

import click

from labqoat.cli.compute.settings_patch import SettingsPatch
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue


class HostShareCommand(StrictCommand):
    """Merge-patch the CPU, memory, disk and exact GPU devices reserved for Labqoat workloads."""

    def __init__(self) -> None:
        """Declare the host selector and share options."""
        params: list[click.Parameter] = [
            click.Argument(["host_id"], type=str, required=True),
            click.Option(["--cpu"], type=str, help="CPUs Labqoat may use (fractions allowed)."),
            click.Option(["--memory-gib", "memory_gib"], type=str, help="Memory Labqoat may use, in GiB."),
            click.Option(["--disk-gib", "disk_gib"], type=str, help="Container disk Labqoat may reserve, in GiB."),
            click.Option(
                ["--gpu", "gpu_device_ids"], multiple=True, help="GPU device UUID Labqoat may use; repeatable."
            ),
            click.Option(["--no-gpus", "no_gpus"], is_flag=True, help="Give Labqoat no GPU devices on this host."),
        ]
        super().__init__("share", params=params, help="Change the resource share of a connected host.")

    def invoke(self, ctx: click.Context) -> object:
        """Validate the requested share, then send it."""
        share = self.share(ctx.params)
        client = ContextAccessor.current().compute()
        try:
            ResultWriter().write_dict(client.update_host_share(str(ctx.params["host_id"]), share))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def share(params: dict[str, object]) -> JsonDocument:
        """Convert display units and reject contradictory or empty selections as usage errors."""
        share = HostShareCommand.quantities(params)
        devices = params["gpu_device_ids"]
        selected: list[JsonValue] = [str(device) for device in devices] if isinstance(devices, tuple) else []
        if selected and params["no_gpus"]:
            ErrorReporter.report_usage("--gpu and --no-gpus are mutually exclusive.")
        if selected or params["no_gpus"]:
            share["gpu_device_ids"] = selected
        if not share:
            ErrorReporter.report_usage("Select --cpu, --memory-gib, --disk-gib, --gpu or --no-gpus.")
        return share

    @staticmethod
    def quantities(params: dict[str, object]) -> JsonDocument:
        """Convert CPUs to millicores and GiB to MiB; a share is always a finite quantity."""
        share = JsonDocument()
        quantities = (
            ("cpu", "cpu_millicores", 1000),
            ("memory_gib", "memory_mb", 1024),
            ("disk_gib", "ephemeral_storage_mb", 1024),
        )
        for name, field, scale in quantities:
            value = params[name]
            if value is None:
                continue
            flag = "--" + name.replace("_", "-")
            try:
                amount = SettingsPatch.scaled(str(value), scale, flag)
            except ValueError as error:
                ErrorReporter.report_usage(str(error))
            if amount is None:
                ErrorReporter.report_usage(f"{flag} must be a number for a host share.")
            share[field] = amount
        return share
