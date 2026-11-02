"""Digest-pinned agent image resolved to an exact linux/amd64 image ID on this machine."""

from __future__ import annotations

import re
from dataclasses import dataclass

from labqoat.cli.compute.enrollment.enrollment_error import EnrollmentError
from labqoat.cli.compute.enrollment.process_runner import ProcessRunner


@dataclass(frozen=True)
class AgentImage:
    """An immutable image reference that is transferred to hosts without registry access."""

    reference: str

    PINNED = re.compile(r"[a-z0-9][a-z0-9._/:-]*@sha256:[0-9a-f]{64}")
    IDENTIFIER = re.compile(r"sha256:[0-9a-f]{64}")
    PLATFORM = "linux/amd64"

    def __post_init__(self) -> None:
        """Require a digest so every host runs exactly the reviewed image."""
        if self.PINNED.fullmatch(self.reference) is None:
            raise ValueError(f"--agent-image must be pinned by digest (name@sha256:...), not {self.reference!r}")

    def resolve(self, runner: ProcessRunner) -> str:
        """Return the local image ID, pulling the linux/amd64 variant first when needed."""
        platform, identifier = self.inspect(runner)
        if platform != self.PLATFORM:
            pulled = runner.run(["docker", "pull", "--platform", self.PLATFORM, self.reference])
            if not pulled.ok:
                raise EnrollmentError(f"Could not pull {self.reference} locally: {pulled.diagnostic()}")
            platform, identifier = self.inspect(runner)
        if platform != self.PLATFORM or self.IDENTIFIER.fullmatch(identifier) is None:
            raise EnrollmentError(
                f"{self.reference} is {platform or 'unavailable'} locally; {self.PLATFORM} is required"
            )
        return identifier

    def inspect(self, runner: ProcessRunner) -> tuple[str, str]:
        """Read the local platform and ID, or empty values when the image is absent."""
        template = "{{.Os}}/{{.Architecture}} {{.Id}}"
        result = runner.run(["docker", "image", "inspect", "--format", template, self.reference])
        platform, _, identifier = result.output.partition(" ")
        return (platform, identifier) if result.ok else ("", "")
