import asyncio
import os
from unittest.mock import AsyncMock

import pytest

from arraylake.asyn import (
    asyncio_run,
    get_lock,
    get_loop,
    loop_selector_policy,
    sync,
)


def test_sync() -> None:
    bag = []

    async def add_to_bag(n):
        bag.append(n)

    sync(add_to_bag, 1)
    assert bag == [1]


def test_asyncio_run():
    async def foo():
        return 1

    assert asyncio_run(foo()) == 1


def test_selector_policy() -> None:
    orig_policy = asyncio.get_event_loop_policy()

    with loop_selector_policy():
        new_policy = asyncio.get_event_loop_policy()

        # if on windows policy will be WindowsSelectorEventLoopPolicy
        if os.name == "nt":
            assert isinstance(new_policy, asyncio.WindowsSelectorEventLoopPolicy)
        else:
            # if uvloop is available policy will be uvloop.EventLoopPolicy
            try:
                import uvloop

                assert isinstance(new_policy, uvloop.EventLoopPolicy)
            except ImportError:
                assert orig_policy is asyncio.get_event_loop_policy()

    # confirm that policy was changed back to the original
    assert orig_policy is asyncio.get_event_loop_policy()


def test_get_loop() -> None:
    # test that we only create one loop
    loop = get_loop()
    loop2 = get_loop()
    assert loop is loop2


def test_get_lock() -> None:
    # test that we only create one lock
    lock = get_lock()
    lock2 = get_lock()
    assert lock is lock2
