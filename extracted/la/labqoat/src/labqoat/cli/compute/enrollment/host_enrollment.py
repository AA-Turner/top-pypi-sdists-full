"""Ordered connected-host bootstrap: preflight, enroll, transfer, install and await readiness."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from labqoat.cli.compute.enrollment.agent_image import AgentImage
from labqoat.cli.compute.enrollment.bootstrap_scripts import BootstrapScripts
from labqoat.cli.compute.enrollment.command_result import CommandResult
from labqoat.cli.compute.enrollment.enrollment_error import EnrollmentError
from labqoat.cli.compute.enrollment.host_readiness_waiter import HostReadinessWaiter
from labqoat.cli.compute.enrollment.preflight_report import PreflightReport
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner
from labqoat.cli.compute.enrollment.ssh_target import SshTarget
from labqoat.compute_client import ComputeClient
from labqoat.json_document import JsonDocument


@dataclass
class HostEnrollment:
    """Create the enrollment only after the host qualifies, then install the pinned agent over SSH."""

    runner: ProcessRunner
    client: ComputeClient
    target: SshTarget
    image: AgentImage
    site: str
    waiter: HostReadinessWaiter
    progress: Callable[[str], None]

    def run(self) -> JsonDocument:
        """Perform every step, naming the incomplete enrollment if a later step fails."""
        preflight = self.preflight()
        image_id = self.image.resolve(self.runner)
        self.progress(f"Agent image {self.image.reference} resolved to {image_id}.")
        enrollment = self.client.enroll_host(self.site)
        host_id = str(JsonDocument.expect_dict(enrollment["host"])["id"])
        self.progress(f"Created enrollment {host_id} at site {self.site}.")
        try:
            self.install(JsonDocument.expect_dict(enrollment["agent_settings"]), image_id, bool(preflight.gpus))
            return self.waiter.wait(host_id)
        except EnrollmentError as error:
            raise EnrollmentError(
                f"{error} Enrollment {host_id} is incomplete; fix the cause and re-run, "
                f"or remove it with 'labqoat compute hosts remove {host_id}'."
            ) from error

    def preflight(self) -> PreflightReport:
        """Check the host before Labqoat records anything about it."""
        result = self.remote("Preflight", "sh -s", BootstrapScripts.preflight().encode())
        report = PreflightReport.parse(result.output)
        report.require(self.target.destination)
        self.progress(f"Preflight passed: {report.architecture}, {len(report.gpus)} GPU(s).")
        return report

    def install(self, agent_settings: JsonDocument, image_id: str, gpus: bool) -> None:
        """Load and verify the image, prove GPU access, then configure and start the agent."""
        load = self.target.command(SshTarget.privileged("docker load"))
        self.check("Image transfer", self.runner.pipe(["docker", "save", self.image.reference], load))
        loaded = self.remote("Image verification", BootstrapScripts.image_id(image_id)).output
        if loaded != image_id:
            raise EnrollmentError(f"Host reports image {loaded or 'missing'} instead of {image_id}.")
        self.progress("Agent image loaded and verified on the host.")
        if gpus:
            self.remote("GPU container check", BootstrapScripts.gpu_check(image_id))
        script = BootstrapScripts.install(agent_settings, image_id, gpus)
        self.remote("Agent installation", "sh -s", script.encode())
        self.progress("Agent service installed; waiting for the host to report ready.")

    def remote(self, step: str, command: str, stdin: bytes | None = None) -> CommandResult:
        """Run one privileged remote command and require success."""
        return self.check(step, self.runner.run(self.target.command(SshTarget.privileged(command)), stdin))

    def check(self, step: str, result: CommandResult) -> CommandResult:
        """Convert a failed process into an enrollment error naming the host and step."""
        if not result.ok:
            raise EnrollmentError(f"{step} failed on {self.target.destination}: {result.diagnostic()}")
        return result
