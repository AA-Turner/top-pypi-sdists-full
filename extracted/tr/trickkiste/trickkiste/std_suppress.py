#!/usr/bin/env python
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

"""Runs a process but suppress output if it returns successfully before a given amount of time"""

import signal
import sys
from asyncio import (
    Queue,
    StreamReader,
    create_subprocess_exec,
    gather,
    run,
    wait_for,
)
from asyncio import TimeoutError as AsyncTimeoutError
from asyncio.subprocess import PIPE, Process
from collections.abc import Sequence
from contextlib import suppress
from typing import TextIO

LineQueue = Queue[None | tuple[TextIO, bytes]]


async def print_after(
    timeout: float,
    abort: Queue[bool],
    buffer: LineQueue,
) -> None:
    """Wait for a given time or until aborted - print buffer contents if appropriate"""
    with suppress(AsyncTimeoutError):
        if await wait_for(abort.get(), timeout):
            return
    while elem := await buffer.get():
        out_file, line = elem
        out_file.write(line.decode(errors="replace"))


async def buffer_stream(
    stream: StreamReader, buffer: LineQueue, out_file: TextIO
) -> None:
    """Records a given stream to a buffer line by line along with the source"""
    while line := await stream.readline():
        await buffer.put((out_file, line))
    await buffer.put(None)


async def wait_and_notify(process: Process, abort: Queue[bool]) -> None:
    """Just waits for @process to finish and notify the result"""
    await process.wait()
    await abort.put(process.returncode == 0)


async def run_quiet_and_verbose(timeout: float, cmd: Sequence[str]) -> None:
    """Run a command and start printing it's output only after a given timeout"""
    buffer: LineQueue = Queue()
    abort: Queue[bool] = Queue()

    process = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)

    assert process.stdout
    assert process.stderr

    signal.signal(signal.SIGINT, lambda _sig, _frame: 0)

    await gather(
        print_after(float(timeout), abort, buffer),
        buffer_stream(process.stdout, buffer, sys.stdout),
        buffer_stream(process.stderr, buffer, sys.stderr),
        wait_and_notify(process, abort),
    )
    raise SystemExit(process.returncode)


def main() -> None:
    """Just the entrypoint for run_quiet_and_verbose()"""
    timeout, *cmd = sys.argv[1:]
    run(run_quiet_and_verbose(float(timeout), cmd))


if __name__ == "__main__":
    main()
