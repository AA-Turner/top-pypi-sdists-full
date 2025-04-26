# Copyright 2023 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.

from __future__ import annotations

import asyncio
import functools
import logging
from asyncio import CancelledError, Task
from typing import Any, Coroutine

import websockets

ROOT_LOGGER = logging.getLogger()


def create_task_with_handler(
    coro: Coroutine[Any, Any, Any], task_name: str, logger: logging.Logger = ROOT_LOGGER
) -> Task[Any]:
    """Wrapper around "asyncio.create_task" to make sure the task
    exceptions are handled properly.

    asyncio loop event_handler is only called on task exceptions when
    the Task object is cleared from memory. But the GC doesn't clear
    the Task if we keep a reference for it (e.g. _pinger_task in
    connection.py) until the very end.

    This makes sure the exceptions are retrieved and properly
    handled/logged whenever the Task is destroyed.
    """

    def _task_result_exp_handler(
        task: Task[Any], task_name: str = task_name, logger: logging.Logger = logger
    ):
        try:
            task.result()
        except CancelledError:
            pass
        except websockets.exceptions.ConnectionClosed:
            return
        except Exception as e:
            # This really is an arbitrary exception we need to catch
            #
            # No need to re-raise, though, because after this point
            # the only thing that can catch this is asyncio loop base
            # event_handler, which won't do anything but yell 'Task
            # exception was never retrieved' anyways.
            logger.exception("Task %s raised an exception: %s" % (task_name, e))

    task = asyncio.create_task(coro)
    task.add_done_callback(
        functools.partial(_task_result_exp_handler, task_name=task_name, logger=logger)
    )
    return task


class SingletonEventLoop:
    """Single instance containing an event loop to be reused."""

    loop: asyncio.AbstractEventLoop
    instance: SingletonEventLoop

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
            cls.instance.loop = asyncio.new_event_loop()

        return cls.instance
