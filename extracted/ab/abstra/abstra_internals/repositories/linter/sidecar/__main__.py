"""Linter sidecar entrypoint:

    python -m abstra_internals.repositories.linter.sidecar <root_path>

Spawned by the editor process (see client.py). stdout is the protocol channel
and stderr is inherited for logs. The process exits by itself on stdin EOF —
that covers a dead parent, a SIGKILLed parent and the parent's os.execv
(non-inheritable fds close on exec), so no orphan is ever left behind.
"""

import os
import sys


def main() -> int:
    # FD hygiene FIRST, before any rule-stack import can print: duplicate
    # fd 1 as the exclusive protocol channel, then point fd 1 at stderr so
    # rule prints AND subprocesses spawned by fixes (pip install writes to
    # fd 1!) can never corrupt the framing.
    protocol_fd = os.dup(1)
    os.dup2(2, 1)
    protocol_writer = os.fdopen(protocol_fd, "wb")
    protocol_reader = sys.stdin.buffer
    try:
        # fd 1 now points at stderr (usually a pipe ⇒ block-buffered); rule
        # prints must not die unflushed in the buffer when os._exit() runs.
        sys.stdout.reconfigure(line_buffering=True)  # type: ignore[union-attr]
    except Exception:
        pass

    if len(sys.argv) < 2:
        sys.stderr.write(
            "usage: python -m abstra_internals.repositories.linter.sidecar "
            "<root_path>\n"
        )
        return 2

    from abstra_internals.settings import Settings

    Settings.set_root_path(sys.argv[1])

    if hasattr(os, "nice"):
        # Lint work yields CPU to the editor's serving threads inside the
        # same cgroup; POSIX only.
        try:
            os.nice(10)
        except OSError:
            pass

    from abstra_internals.environment import EDITOR_MODE
    from abstra_internals.logger import AbstraLogger

    AbstraLogger.init("local" if EDITOR_MODE == "local" else "cloud")

    from abstra_internals.controllers.language_server import (
        set_diagnostics_provider,
    )
    from abstra_internals.repositories.linter.repository import (
        LocalLinterRepository,
    )
    from abstra_internals.repositories.linter.rules import rules
    from abstra_internals.repositories.linter.sidecar.server import (
        SidecarLinterServer,
    )

    repository = LocalLinterRepository(serial=True)
    server = SidecarLinterServer(
        repository=repository,
        registry=rules,
        reader=protocol_reader,
        writer=protocol_writer,
    )
    # TypeCheckingRule reaches the EDITOR's pyrefly via reverse RPC instead
    # of spawning a second pyrefly in this process (option B, PR1).
    set_diagnostics_provider(server.request_diagnostics)

    server.serve()
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        import traceback

        traceback.print_exc(file=sys.stderr)
        exit_code = 1
    # os._exit: worker/daemon threads must not block the shutdown the parent
    # is relying on (EOF ⇒ child gone) — but flush text buffers first, since
    # os._exit skips them.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.flush()
        except Exception:
            pass
    os._exit(exit_code)
