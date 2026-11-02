"""What a command started in a sandbox may set besides its arguments."""

from collections.abc import Mapping
from typing import TypedDict

from labqoat.sandbox.stream_type import StreamType


class SandboxExecOptions(TypedDict, total=False):
    """Keyword arguments of ``Sandbox.exec``, every one optional.

    ``workdir`` is the absolute directory the command starts in and ``env`` adds variables to the sandbox's.
    ``user`` is a numeric ``uid`` or ``uid:gid``; the command runs as root without it. A command still running
    ``timeout`` seconds after it started is killed with everything it started; without one it may run as
    long as the sandbox. ``stdin``, ``stdout`` and ``stderr`` say where each stream goes, ``StreamType.PIPE``
    by default; only ``stderr`` may be ``StreamType.STDOUT``.
    """

    workdir: str | None
    env: Mapping[str, str] | None
    user: str | int | None
    timeout: float | None
    stdin: StreamType
    stdout: StreamType
    stderr: StreamType
