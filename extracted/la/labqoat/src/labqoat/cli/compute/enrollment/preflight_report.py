"""Parsed connected-host preflight facts and the requirements enrollment enforces."""

from __future__ import annotations

from dataclasses import dataclass

from labqoat.cli.compute.enrollment.enrollment_error import EnrollmentError


@dataclass(frozen=True)
class PreflightReport:
    """Architecture, what the sandbox runtime needs from the host, detected GPUs and their container toolkit."""

    architecture: str
    ready: frozenset[str]
    gpus: tuple[str, ...]

    REQUIRED = (
        ("docker=ok", "'docker info' failed; install Docker and allow root access to it"),
        ("cgroup=v2", "control groups are not the unified hierarchy; workloads need cgroup v2"),
        (
            "containerd=ok",
            "containerd's socket, its 'ctr' client and /var/lib/containerd were not all found; Docker's own "
            "containerd provides them",
        ),
        ("fetch=ok", "'curl' and 'zstd' are needed to install the sandbox runtime"),
    )

    @classmethod
    def parse(cls, output: str) -> PreflightReport:
        """Read the key=value lines printed by the preflight script."""
        lines = [line.strip() for line in output.splitlines()]
        architecture = next((line.partition("=")[2] for line in lines if line.startswith("arch=")), "unknown")
        gpus = tuple(line.partition("=")[2] for line in lines if line.startswith("gpu="))
        return cls(architecture, frozenset(lines), gpus)

    def problems(self) -> list[str]:
        """List every unmet requirement so the administrator can fix them together."""
        problems = [message for fact, message in self.REQUIRED if fact not in self.ready]
        if self.architecture != "x86_64":
            problems.insert(0, f"architecture is {self.architecture}; the agent image requires x86_64")
        if self.gpus and "nvidia_toolkit=yes" not in self.ready:
            problems.append(f"{len(self.gpus)} GPU(s) found but the NVIDIA container toolkit is not set up for Docker")
        return problems

    def require(self, destination: str) -> None:
        """Stop before any enrollment is created when the host cannot run the agent."""
        problems = self.problems()
        if problems:
            raise EnrollmentError(f"Preflight failed on {destination}: " + "; ".join(problems))
