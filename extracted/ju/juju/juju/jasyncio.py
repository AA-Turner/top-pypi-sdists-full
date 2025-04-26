# Copyright 2023 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.

# A compatibility layer on asyncio that ensures we have all the right
# bindings for the functions we need from asyncio. Reason for this
# layer is the frequent functional changes, additions and deprecations
# in asyncio across the different Python versions.

# Any module that needs to use the asyncio should get the binding from
# this layer.

import logging
import signal
import warnings
from asyncio import (
    ALL_COMPLETED as ALL_COMPLETED,
)
from asyncio import (
    FIRST_COMPLETED as FIRST_COMPLETED,
)

# FIXME: integration tests don't use these, but some are used in this repo
# Use primitives from asyncio within this repo and remove these re-exports
from asyncio import (
    Event as Event,
)
from asyncio import (
    Lock as Lock,
)
from asyncio import (
    Queue as Queue,
)
from asyncio import (
    all_tasks as all_tasks,
)
from asyncio import (
    as_completed as as_completed,
)
from asyncio import (
    create_subprocess_exec as create_subprocess_exec,
)
from asyncio import (
    current_task as current_task,
)
from asyncio import (
    ensure_future as ensure_future,
)
from asyncio import (
    gather as gather,
)
from asyncio import (
    get_event_loop_policy as get_event_loop_policy,
)
from asyncio import (
    get_running_loop as get_running_loop,
)
from asyncio import (
    new_event_loop as new_event_loop,
)
from asyncio import (
    shield as shield,
)
from asyncio import (
    sleep as sleep,
)
from asyncio import (
    subprocess as subprocess,
)
from asyncio import (
    wait,
)
from asyncio import (
    wait_for as wait_for,
)

from juju._jasyncio import (
    SingletonEventLoop as SingletonEventLoop,
)
from juju._jasyncio import (
    create_task_with_handler as create_task_with_handler,
)

warnings.warn(
    "juju.jasyncio module is being deprecated by 3.0, use asyncio or juju._jasyncio instead",
    DeprecationWarning,
    stacklevel=2,
)


ROOT_LOGGER = logging.getLogger()


def run(*steps):
    """Helper to run one or more async functions synchronously, with graceful
    handling of SIGINT / Ctrl-C.

    Returns the return value of the last function.
    """
    if not steps:
        return

    task = None
    run._sigint = False  # function attr to allow setting from closure
    # Use a singleton class to force a single event loop instance
    loop = SingletonEventLoop().loop

    def abort():
        task.cancel()
        run._sigint = True

    added = False
    try:
        loop.add_signal_handler(signal.SIGINT, abort)
        added = True
    except (ValueError, OSError, RuntimeError) as e:
        # add_signal_handler doesn't work in a thread
        if "main thread" not in str(e):
            raise
    try:
        for step in steps:
            task = loop.create_task(step)
            loop.run_until_complete(wait([task]))
            if run._sigint:
                raise KeyboardInterrupt()
            if task.exception():
                raise task.exception()
        return task.result()
    finally:
        if added:
            loop.remove_signal_handler(signal.SIGINT)
