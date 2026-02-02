import asyncio
import os
import platform
import time
from collections.abc import Awaitable, Callable, Generator
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TypeVar

IS_CI = os.environ.get("CI") is not None
IS_OSX = platform.system() == "Darwin"
IS_WINDOWS = platform.system() == "Windows"

T = TypeVar("T")


@contextmanager
def temp_file(content: bytes, suffix: str = "") -> Generator[Path, None, None]:
    """Temp file that works on windows too with subprocesses."""
    tmp = NamedTemporaryFile(suffix=suffix, delete=False)  # noqa: SIM115
    path = Path(tmp.name)
    try:
        tmp.write(content)
        tmp.flush()
        tmp.close()
        yield path
    finally:
        path.unlink()


async def wait_for(fn: Callable[[], Awaitable[T]], success_timeout: timedelta = timedelta(seconds=10)) -> T:
    deadline = time.monotonic() + success_timeout.total_seconds()
    while True:
        try:
            return await fn()
        except Exception as exc:
            if time.monotonic() > deadline:
                print(exc)
                raise
            await asyncio.sleep(0.1)
