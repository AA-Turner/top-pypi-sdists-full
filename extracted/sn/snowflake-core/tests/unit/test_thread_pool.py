from concurrent.futures import ThreadPoolExecutor

import pytest

import snowflake.core._thread_pool as thread_pool

from snowflake.core._thread_pool import get_thread_pool


@pytest.fixture(autouse=True)
def reset_pool():
    thread_pool.THREAD_POOL.reset()


def test_default_thread_pool_size():
    pool = get_thread_pool()
    assert pool._max_workers == ThreadPoolExecutor()._max_workers


def test_custom_thread_pool_size():
    pool = get_thread_pool(10)
    assert pool._max_workers == 10


def test_init_once():
    get_thread_pool(10)
    pool = get_thread_pool(20)
    assert pool._max_workers == 10
