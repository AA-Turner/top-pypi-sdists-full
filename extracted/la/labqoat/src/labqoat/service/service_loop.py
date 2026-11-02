"""An event loop on a thread of its own, running one piece of work until told to stop."""

import asyncio
from collections.abc import Coroutine
from contextlib import suppress
from threading import Thread


class ServiceLoop:
    """Run a coroutine beside synchronous code and cancel it from that code's thread."""

    def __init__(self, name: str, work: Coroutine[object, object, None]) -> None:
        """Start the work at once on a daemon thread, so an abandoned loop never holds a worker open."""
        self._loop = asyncio.new_event_loop()
        self._task = self._loop.create_task(work)
        self._thread = Thread(target=self._run, name=name, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Cancel the work on its own loop and wait until its thread has ended."""
        self._loop.call_soon_threadsafe(self._task.cancel)
        self._thread.join()

    def _run(self) -> None:
        """Drive the loop until the work ends or is cancelled, then release the loop."""
        with suppress(asyncio.CancelledError):
            self._loop.run_until_complete(self._task)
        self._loop.close()
