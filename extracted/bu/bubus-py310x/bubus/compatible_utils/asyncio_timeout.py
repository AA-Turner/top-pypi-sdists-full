from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def async_timeout(timeout: float):
    task = asyncio.current_task()
    loop = asyncio.get_event_loop()
    if task is None:
        raise RuntimeError("async_timeout must be used within a running asyncio Task")
    handle = loop.call_later(timeout, task.cancel)
    try:
        yield
    except asyncio.CancelledError:
        raise asyncio.TimeoutError(f"Operation exceeded {timeout} seconds")
    finally:
        handle.cancel()