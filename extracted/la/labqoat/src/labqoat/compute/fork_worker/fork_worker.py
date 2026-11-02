"""A single-threaded, credential-free template never imports authored code or consumes assignment envelopes."""

import os
import signal
import sys
import traceback
from contextlib import suppress
from types import FrameType

from labqoat.compute.prepared_worker.prepared_worker import PreparedWorker
from labqoat.stage_timer import StageTimer
from labqoat.net.transport_trust import TransportTrust


class ForkWorker:
    """Fork a fresh child for each trigger and reap its entire process group before acknowledging completion."""

    @classmethod
    def main(cls) -> None:
        """Load platform modules once, then read only one-byte spawn requests from the shared input pipe."""
        timing = StageTimer.stderr()
        cls.preload()
        TransportTrust.context()
        timing.stage("template.sdk_import")
        output = int(sys.argv[1])
        signal.signal(signal.SIGTERM, cls.stop)
        print("ready", flush=True)
        while trigger := os.read(0, 1):
            if trigger != b"!":
                raise ValueError("Invalid isolated process trigger")
            cls.spawn(output)

    @staticmethod
    def preload() -> None:
        """Import the worker and every public SDK name once, so each forked child starts with them loaded."""
        import labqoat
        from labqoat import compute
        from labqoat.compute.worker.compute_worker import ComputeWorker

        _ = ComputeWorker
        for package in (labqoat, compute):
            for name in package.__all__:
                getattr(package, name)

    @classmethod
    def spawn(cls, output: int) -> None:
        """Keep credentials in the pipe until after the child owns its isolated address space."""
        reader, writer = os.pipe()
        child = os.fork()
        if child == 0:
            os.close(reader)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            os.setsid()
            os.dup2(output, 1)
            os.close(output)
            os.write(writer, b"!")
            os.close(writer)
            cls.invoke()
        else:
            os.close(writer)
            cls.reap(child, reader)

    @staticmethod
    def reap(child: int, reader: int) -> None:
        """Acknowledge only an established child process group, and reap it even during template shutdown."""
        try:
            if os.read(reader, 1) != b"!":
                raise RuntimeError("Isolated child failed to establish its process group")
            print(child, flush=True)
            _, status = os.waitpid(child, 0)
        finally:
            os.close(reader)
            with suppress(ProcessLookupError):
                os.killpg(child, signal.SIGKILL)
            with suppress(ChildProcessError):
                os.waitpid(child, 0)
        print(os.waitstatus_to_exitcode(status), flush=True)

    @staticmethod
    def stop(_signal: int, _frame: FrameType | None) -> None:
        """Unwind the active child owner so physical shutdown cannot orphan an unreaped invocation."""
        raise SystemExit(0)

    @staticmethod
    def invoke() -> None:
        """Run one ordinary worker with fresh credentials, imports and scratch, then exit without returning to the template.

        The exit skips interpreter shutdown: threads and exit handlers that authored code leaves behind, such as an
        inference engine's, would otherwise keep a finished or failed invocation alive. The parent reaps the rest of
        the process group.
        """
        status = 0
        try:
            PreparedWorker.main()
        except BaseException:
            traceback.print_exc()
            status = 1
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            os._exit(status)
