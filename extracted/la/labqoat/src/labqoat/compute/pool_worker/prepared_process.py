"""One credential-free template amortizes SDK imports while every invocation retains its own OS process."""

import asyncio
import json
import os
import signal
import sys
from contextlib import suppress
from dataclasses import dataclass, field


@dataclass
class PreparedProcess:
    """Own a private template protocol and never release a slot before its authored process group is reaped."""

    process: asyncio.subprocess.Process | None = field(default=None, init=False)
    _child: int | None = field(default=None, init=False)
    _warming: asyncio.Task[None] | None = field(default=None, init=False)

    def warm(self) -> None:
        """Start the template now, so its imports overlap whatever the supervisor does before the first input."""
        if self.process is None and self._warming is None:
            self._warming = asyncio.ensure_future(self._start())

    async def prepare(self) -> None:
        """Wait until the template is ready, starting it unless ``warm`` already did; failure closes it."""
        self.warm()
        warming = self._warming
        if warming is None:
            return
        try:
            await warming
        except BaseException:
            await self.close()
            raise
        self._warming = None

    async def _start(self) -> None:
        """Preload platform imports with no credentials and preserve the original output stream only for children."""
        output = os.dup(1)
        try:
            await self._spawn(output)
            if await self._line() != b"ready\n":
                raise RuntimeError("Isolated process template did not become ready")
        except BaseException:
            await self.close()
            raise
        finally:
            os.close(output)

    async def _spawn(self, output: int) -> None:
        """Retain process ownership even if cancellation arrives before subprocess creation completes."""
        pending = asyncio.create_task(
            asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "labqoat.compute.fork_worker",
                str(output),
                env={key: value for key, value in os.environ.items() if not key.startswith("LABQOAT_")},
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                pass_fds=(output,),
                limit=128,
                start_new_session=True,
            )
        )
        try:
            self.process = await asyncio.shield(pending)
        except asyncio.CancelledError:
            self.process = await pending
            raise

    async def execute(self, environment: dict[str, str], *, refill: bool = False) -> int:
        """Fork before installing the assignment and retain the template only within an explicitly owned session."""
        await self.prepare()
        pending = asyncio.create_task(self._begin(environment))
        try:
            self._child = await asyncio.shield(pending)
            return int(await self._line())
        except asyncio.CancelledError:
            try:
                self._child = await pending
            finally:
                await self.close()
            raise
        except BaseException:
            await self.close()
            raise
        finally:
            self._reap_child()
            if not refill:
                await self.close()

    async def _begin(self, environment: dict[str, str]) -> int:
        """The template consumes only the trigger; the fresh child alone reads the bounded assignment."""
        process = self.process
        if process is None or process.stdin is None:
            raise RuntimeError("Prepared worker has no assignment channel")
        document = json.dumps(environment, separators=(",", ":")).encode() + b"\n"
        if len(document) > 1_048_576:
            raise ValueError("Prepared assignment exceeds its framing limit")
        process.stdin.write(b"!" + document)
        await process.stdin.drain()
        child = int(await self._line())
        if child <= 1:
            raise RuntimeError("Isolated process template returned an invalid child")
        return child

    async def _line(self) -> bytes:
        """Control acknowledgements cannot be mixed with authored stdout or stderr."""
        if self.process is None or self.process.stdout is None:
            raise RuntimeError("Prepared worker has no control channel")
        line = await self.process.stdout.readline()
        if not line.endswith(b"\n"):
            raise RuntimeError("Isolated process template disconnected")
        return line

    async def close(self) -> None:
        """Reap the active invocation before terminating its template on every owning-worker exit."""
        warming, self._warming = self._warming, None
        if warming is not None and warming is not asyncio.current_task():
            warming.cancel()
            await asyncio.gather(warming, return_exceptions=True)
        self._reap_child()
        process, self.process = self.process, None
        if process is not None:
            with suppress(ProcessLookupError):
                process.terminate()
            await process.wait()
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)

    def _reap_child(self) -> None:
        """A completed or cancelled child cannot leave descendants running into the next invocation."""
        child, self._child = self._child, None
        if child is not None:
            with suppress(ProcessLookupError):
                os.killpg(child, signal.SIGKILL)
