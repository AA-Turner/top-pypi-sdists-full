"""Whether a sandbox process still runs, and how it ended."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class SandboxProcessState:
    """A running process has no exit code; an ended one has one, and says whether its timeout killed it."""

    exit_code: int | None
    timed_out: bool = False

    @property
    def running(self) -> bool:
        """Report whether the process has yet to exit."""
        return self.exit_code is None

    @staticmethod
    def decode(document: JsonDocument) -> "SandboxProcessState":
        """Read the host's process document, whose state and exit code must agree."""
        state = JsonDocument.expect_scalar(document["state"], str)
        exit_code = JsonDocument.expect_optional_scalar(document["exit_code"], int)
        if (state, exit_code is None) not in (("running", True), ("exited", False)):
            raise ValueError(f"a process that is {state!r} cannot have exit code {exit_code!r}")
        return SandboxProcessState(exit_code, JsonDocument.expect_scalar(document["timed_out"], bool))
