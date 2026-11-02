"""What a sandbox host keeps about one of a sandbox's processes."""

from dataclasses import dataclass
from datetime import datetime

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_process_state import SandboxProcessState


@dataclass(frozen=True)
class SandboxProcessInfo:
    """A process's identifier, command, state and when it started and ended.

    The entrypoint's identifier is ``main``; ``Sandbox.process`` opens any process by its identifier to read
    its output, wait for it or kill it. An ended process is listed until its host retires its record, about ten
    minutes after it exited.
    """

    id: str
    argv: tuple[str, ...]
    state: SandboxProcessState
    started_at: datetime
    ended_at: datetime | None

    @property
    def running(self) -> bool:
        """Report whether the process has yet to exit."""
        return self.state.running

    @property
    def exit_code(self) -> int | None:
        """Return the exit code once the process has exited."""
        return self.state.exit_code

    @staticmethod
    def decode(document: JsonDocument) -> "SandboxProcessInfo":
        """Read one process of a host's listing."""
        ended_at = JsonDocument.expect_optional_scalar(document["ended_at"], str)
        return SandboxProcessInfo(
            JsonDocument.expect_scalar(document["id"], str),
            tuple(JsonDocument.expect_scalar(part, str) for part in JsonDocument.expect_list(document["argv"])),
            SandboxProcessState.decode(document),
            datetime.fromisoformat(JsonDocument.expect_scalar(document["started_at"], str)),
            None if ended_at is None else datetime.fromisoformat(ended_at),
        )

    @staticmethod
    def listed(document: JsonDocument) -> "tuple[SandboxProcessInfo, ...]":
        """Read a host's listing of a sandbox's processes, in the order they started."""
        processes = JsonDocument.expect_list(document["processes"])
        return tuple(SandboxProcessInfo.decode(JsonDocument.expect_dict(process)) for process in processes)
