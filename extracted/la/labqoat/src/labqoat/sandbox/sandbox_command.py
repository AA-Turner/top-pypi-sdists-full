"""A command as a sandbox host starts it."""

import math
from collections.abc import Sequence
from typing import ClassVar

from labqoat.json_document import JsonValue
from labqoat.sandbox.sandbox_exec_options import SandboxExecOptions
from labqoat.sandbox.stream_type import StreamType


class SandboxCommand:
    """Translate ``exec`` arguments into the host's process document and the streams that come back."""

    STDIN: ClassVar[dict[StreamType, JsonValue]] = {StreamType.PIPE: None, StreamType.DEVNULL: False}
    STDOUT: ClassVar[dict[StreamType, JsonValue]] = {StreamType.PIPE: None, StreamType.DEVNULL: "null"}
    STDERR: ClassVar[dict[StreamType, JsonValue]] = {
        StreamType.PIPE: None,
        StreamType.STDOUT: "stdout",
        StreamType.DEVNULL: "null",
    }

    @classmethod
    def document(cls, process_id: str, argv: Sequence[str], options: SandboxExecOptions) -> dict[str, JsonValue]:
        """Describe the process by its identifier and arguments and only what differs from the defaults.

        A list passed as one argument would become a single program name, so arguments must all be strings.
        """
        if not argv or not all(isinstance(argument, str) for argument in argv):
            raise TypeError("exec takes the command's arguments one by one: exec('python3', '-c', 'print(1)')")
        env, user, timeout = options.get("env"), options.get("user"), options.get("timeout")
        optional: dict[str, JsonValue] = {
            "cwd": options.get("workdir"),
            "env": None if env is None else dict(env),
            "user": None if user is None else str(user),
            "timeout_ms": None if timeout is None else math.ceil(timeout * 1000),
            "stdin": cls._wired("stdin", cls.STDIN, options.get("stdin", StreamType.PIPE)),
            "stdout": cls._wired("stdout", cls.STDOUT, options.get("stdout", StreamType.PIPE)),
            "stderr": cls._wired("stderr", cls.STDERR, options.get("stderr", StreamType.PIPE)),
        }
        return {
            "id": process_id,
            "argv": list(argv),
            **{key: value for key, value in optional.items() if value is not None},
        }

    @staticmethod
    def streams(options: SandboxExecOptions) -> tuple[str | None, str | None]:
        """Name the outputs the caller reads back: only piped ones are kept for reading."""
        piped = StreamType.PIPE
        stdout = "stdout" if options.get("stdout", piped) is piped else None
        return stdout, "stderr" if options.get("stderr", piped) is piped else None

    @staticmethod
    def piped(options: SandboxExecOptions) -> bool:
        """Report whether the caller writes the process's standard input."""
        return options.get("stdin", StreamType.PIPE) is StreamType.PIPE

    @staticmethod
    def _wired(stream: str, choices: dict[StreamType, JsonValue], chosen: StreamType) -> JsonValue:
        """Return how the host names a stream's destination, refusing one the stream cannot have."""
        if chosen not in choices:
            raise ValueError(f"{stream} cannot be {chosen}; only stderr may join stdout")
        return choices[chosen]
