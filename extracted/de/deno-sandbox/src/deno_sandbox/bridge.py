import asyncio
import threading
from typing import Any, Coroutine, TypeVar

T = TypeVar("T")


class AsyncBridge:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    def run(self, coro: Coroutine[Any, Any, T]) -> T:
        if not asyncio.iscoroutine(coro):
            raise TypeError("Must pass a coroutine")

        # Submit the coroutine to the loop in the other thread
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

    def stop(self) -> None:
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
