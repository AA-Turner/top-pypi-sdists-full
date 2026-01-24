#!/usr/bin/env python3

"""Example for fancy logging"""

# ruff: noqa: T201 print

import asyncio
import time

from trickkiste.misc import async_retry, asyncify, awatch_duration


@async_retry(exceptions=RuntimeError, tries=3, delay=1)
@awatch_duration(warn_timeout=0.5)
@asyncify
def fancy_synchronous_function1(arg: list[int]) -> str:
    """A synchronous function with distict arguments"""
    arg[0] += 1
    if arg[0] < 3:
        raise RuntimeError("too small")
    time.sleep(1)
    return str(arg[0])


@async_retry
@awatch_duration
async def fancy_synchronous_function2(arg: str) -> None:
    """An async function with distict arguments"""
    await asyncio.sleep(2)
    print(f"hallo {arg}")


async def main() -> None:
    """Runs this"""
    print(await fancy_synchronous_function1([0]))
    task1: asyncio.Task[str] = asyncio.create_task(
        fancy_synchronous_function1([0])
    )
    print(await task1)
    await fancy_synchronous_function2("world")
    task2: asyncio.Task[None] = asyncio.create_task(
        fancy_synchronous_function2("world")
    )
    await task2


if __name__ == "__main__":
    asyncio.run(main())
