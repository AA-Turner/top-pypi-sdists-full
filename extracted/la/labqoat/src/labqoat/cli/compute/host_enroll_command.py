"""``compute hosts enroll`` bootstraps a connected machine over verified SSH."""

from __future__ import annotations

import click

from labqoat.cli.compute.enrollment.agent_image import AgentImage
from labqoat.cli.compute.enrollment.dry_run_plan import DryRunPlan
from labqoat.cli.compute.enrollment.host_enrollment import HostEnrollment
from labqoat.cli.compute.enrollment.host_readiness_waiter import HostReadinessWaiter
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.compute.enrollment.ssh_target import SshTarget
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument


class HostEnrollCommand(StrictCommand):
    """Qualify, enroll and start the agent on an existing machine reachable by SSH."""

    def __init__(self) -> None:
        """Declare the destination, site, pinned image and SSH controls."""
        params: list[click.Parameter] = [
            click.Argument(["destination"], type=str, required=True),
            click.Option(["--site"], type=str, required=True, help="Existing-machine site to enroll into."),
            click.Option(["--agent-image", "agent_image"], type=str, required=True, help="Agent image name@sha256:..."),
            click.Option(["--ssh-option", "ssh_options"], multiple=True, help="Extra ssh -o KEY=VALUE; repeatable."),
            click.Option(
                ["--wait-seconds", "wait_seconds"], type=click.IntRange(min=1), default=120, show_default=True
            ),
            click.Option(["--dry-run", "dry_run"], is_flag=True, help="Print the commands and scripts only."),
        ]
        super().__init__("enroll", params=params, help="Enroll an existing machine over SSH (user@host).")

    def invoke(self, ctx: click.Context) -> object:
        """Validate inputs, then print the plan or perform the enrollment."""
        try:
            target = SshTarget(str(ctx.params["destination"]), tuple(ctx.params["ssh_options"]))
            image = AgentImage(str(ctx.params["agent_image"]))
        except ValueError as error:
            ErrorReporter.report_usage(str(error))
        if ctx.params["dry_run"]:
            click.echo(DryRunPlan.render(target, image, str(ctx.params["site"])))
            return None
        client = ContextAccessor.current().compute()
        try:
            waiter = HostReadinessWaiter(client, timeout_seconds=float(ctx.params["wait_seconds"]))
            enrollment = HostEnrollment(
                ProcessRunner(), client, target, image, str(ctx.params["site"]), waiter, HostEnrollCommand.progress
            )
            host = enrollment.run()
            HostEnrollCommand.progress(HostEnrollCommand.summary(host))
            ResultWriter().write_dict(host)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def progress(message: str) -> None:
        """Report progress on stderr so stdout stays a single result document."""
        click.echo(message, err=True)

    @staticmethod
    def summary(host: JsonDocument) -> str:
        """Describe the derived share and the GPU devices the host reported."""
        return f"Host {host.get('id')} is ready. Share: {host.get('share')}. GPU devices: {host.get('gpu_devices')}."
