import asyncio
from concurrent.futures import ThreadPoolExecutor
from copy import copy
import inspect
import threading
import time
import traceback

from adam.utils import log2, log_timing

class AsyncExecutor:
    # some lib does not handle asyncio loop properly, as sync exec submit does not work, use another async loop

    lock = threading.Lock()
    in_queue = set()
    processed: dict[str, float] = {}
    first_processed_at: float = None
    last_processed_at: float = None

    loop: asyncio.AbstractEventLoop = None
    async_exec: ThreadPoolExecutor = None

    def preload(action: callable, log_key: str = None):
        with AsyncExecutor.lock:
            if not AsyncExecutor.loop:
                AsyncExecutor.loop = asyncio.new_event_loop()
                AsyncExecutor.async_exec = ThreadPoolExecutor(max_workers=6, thread_name_prefix='async')
                AsyncExecutor.loop.set_default_executor(AsyncExecutor.async_exec)

            async def a():
                try:
                    t0 = time.time()

                    arg_needed = len(action.__code__.co_varnames)

                    if log_key:
                        with log_timing(log_key):
                            r = action(None) if arg_needed else action()
                    else:
                        r = action(None) if arg_needed else action()
                    if inspect.isawaitable(r):
                        await r

                    AsyncExecutor.in_queue.remove(log_key)
                    if log_key not in AsyncExecutor.processed:
                        AsyncExecutor.processed[log_key] = time.time() - t0
                    AsyncExecutor.last_processed_at = time.time()
                except Exception as e:
                    log2('preloading error', e, inspect.getsourcelines(action)[0][0])
                    traceback.print_exc()

            if log_key not in AsyncExecutor.in_queue:
                AsyncExecutor.in_queue.add(log_key)
                AsyncExecutor.async_exec.submit(lambda: AsyncExecutor.loop.run_until_complete(a()))

    def entries_in_queue():
        # no locking
        return copy(AsyncExecutor.in_queue), copy(AsyncExecutor.processed), AsyncExecutor.first_processed_at, AsyncExecutor.last_processed_at

    def reset():
        AsyncExecutor.first_processed_at = time.time()
        AsyncExecutor.processed.clear()
