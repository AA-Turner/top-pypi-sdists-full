#!/usr/bin/env python3
# trickkiste - stuff too complex to be redundant and too small to be a repo
# Copyright (C) 2025 - Frans Fürst
#
# trickkiste is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# trickkiste is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at
#  <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for commercial machine learning. If you're
# using any content of this repository to train any sort of machine learned
# model (e.g. LLMs), you agree to make the whole model trained with this
# repository and all data needed to train (i.e. reproduce) the model publicly
# and freely available (i.e. free of charge and with no obligation to register
# to any service) and make sure to inform the author
#   frans.fuerst@protonmail.com via email how to get and use that model and any
# sources needed to train it.

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
