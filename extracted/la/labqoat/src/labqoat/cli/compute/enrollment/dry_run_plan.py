"""Human-readable rendering of every command enrollment would run, with secrets withheld."""

from __future__ import annotations

import shlex

from labqoat.cli.compute.enrollment.agent_image import AgentImage
from labqoat.cli.compute.enrollment.bootstrap_scripts import BootstrapScripts
from labqoat.cli.compute.enrollment.ssh_target import SshTarget


class DryRunPlan:
    """Show the remote scripts without contacting the host, Docker or the Labqoat API."""

    IMAGE_ID = "sha256:<local image ID of the agent image>"
    SETTINGS = (
        ("url", "<issued by POST /api/v1/compute/hosts>"),
        ("worker_api_url", "<issued>"),
        ("machine_id", "<issued>"),
        ("environment_id", "<issued>"),
        ("bootstrap", "<withheld one-time secret>"),
    )

    @staticmethod
    def render(target: SshTarget, image: AgentImage, site: str) -> str:
        """Return the ordered steps with their exact local commands and remote scripts."""
        load = shlex.join(target.command(SshTarget.privileged("docker load")))
        script = BootstrapScripts.install(dict(DryRunPlan.SETTINGS), DryRunPlan.IMAGE_ID, False)
        sections = [
            ("1. Preflight", shlex.join(target.command(SshTarget.privileged("sh -s"))), BootstrapScripts.preflight()),
            ("2. Enrollment", f'POST /api/v1/compute/hosts {{"site": "{site}"}}', ""),
            ("3. Image transfer", f"docker save {shlex.quote(image.reference)} | {load}", ""),
            ("4. Image verification", BootstrapScripts.image_id(DryRunPlan.IMAGE_ID), ""),
            ("5. GPU check (only when GPUs are detected)", BootstrapScripts.gpu_check(DryRunPlan.IMAGE_ID), ""),
            ("6. Installation (--gpus all is added when GPUs are detected)", "sh -s", script),
            ("7. Readiness", "GET /api/v1/compute/hosts/<id> until state is ready", ""),
        ]
        return "\n".join(f"# {title}\n{command}\n{body}" for title, command, body in sections)
