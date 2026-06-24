"""Linter sidecar entrypoint:

    python -m abstra_internals.repositories.linter.sidecar <root_path>

Spawned by the editor process (see client.py). stdout is the protocol channel
and stderr is inherited for logs. The process exits by itself on stdin EOF —
that covers a dead parent, a SIGKILLed parent and the parent's os.execv
(non-inheritable fds close on exec), so no orphan is ever left behind.

This process owns its OWN pyrefly (the language_server _lsp singleton spawns it
lazily for TypeCheckingRule). os._exit() skips atexit, so the graceful shutdown
path would orphan that pyrefly — _kill_own_pyrefly() tears it down explicitly.
"""

import os
import sys


def main() -> int:
    # FD hygiene FIRST, before any rule-stack import can print: duplicate
    # fd 1 as the exclusive protocol channel, then point fd 1 at stderr so
    # rule prints AND subprocesses spawned by fixes (pip install writes to
    # fd 1!) can never corrupt the framing.
    protocol_fd = os.dup(1)
    if sys.platform == "win32":
        # Inherited pipe stdio comes up in the MS C runtime's TEXT mode (O_TEXT)
        # by default, which translates \n<->\r\n on every read/write. That
        # silently corrupts the binary Content-Length framing (protocol.py): a
        # side blocks forever on byte counts the translation shifted, the child
        # stays alive but mute, and the editor's request only fails on its full
        # timeout. Force both protocol fds to binary. No-op off Windows.
        import msvcrt

        msvcrt.setmode(protocol_fd, os.O_BINARY)  # child -> editor (responses)
        msvcrt.setmode(0, os.O_BINARY)  # editor -> child (stdin requests)
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
    # TypeCheckingRule resolves diagnostics from THIS process's own pyrefly,
    # spawned lazily by the language_server _lsp singleton on the first call.
    # No diagnostics provider is installed, so get_diagnostics() uses the local
    # pyrefly directly instead of an IPC round-trip to the editor.

    server.serve()
    return 0


def _kill_own_pyrefly() -> None:
    """Kill this process's pyrefly child before os._exit().

    The sidecar owns its pyrefly (the language_server _lsp singleton spawns it
    for TypeCheckingRule). os._exit() skips atexit, so PyreflyLSP's atexit kill
    never runs on the graceful shutdown path (shutdown RPC / stdin EOF) — without
    this, the pyrefly would orphan. The parent's ungraceful kill path (SIGKILL of
    the whole process group) already covers a crash."""
    try:
        from abstra_internals.controllers import language_server

        proc = getattr(language_server._lsp, "_process", None)
        if proc is not None and proc.poll() is None:
            proc.kill()
    except Exception:
        pass


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        import traceback

        traceback.print_exc(file=sys.stderr)
        exit_code = 1
    # os._exit: worker/daemon threads must not block the shutdown the parent
    # is relying on (EOF ⇒ child gone) — but kill the owned pyrefly and flush
    # text buffers first, since os._exit skips atexit and the buffers.
    _kill_own_pyrefly()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.flush()
        except Exception:
            pass
    os._exit(exit_code)
