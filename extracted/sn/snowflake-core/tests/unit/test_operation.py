from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor

import pytest

from snowflake.core._operation import PollingOperation, PollingOperations


@pytest.fixture()
def pool():
    pool = ThreadPoolExecutor(max_workers=1)
    yield pool
    pool.shutdown()


def test_return_result(pool):
    f = pool.submit(lambda: 5)
    f2 = PollingOperation(f, lambda num: num * 2)
    assert f2.result() == 10


def test_delegate_throws(pool):
    def throw():
        raise ValueError("Oops")

    f = pool.submit(throw)
    f2 = PollingOperation(f, lambda x: x)
    with pytest.raises(ValueError, match="Oops"):
        f2.result()


def test_fn_throws(pool):
    def throw(_):
        raise ValueError("Oops")

    f = pool.submit(lambda: 5)
    f2 = PollingOperation(f, throw)
    with pytest.raises(ValueError, match="Oops"):
        f2.result()


def test_cancel_when_not_started(pool, event):
    pool.submit(lambda: event.wait())
    f = pool.submit(lambda: event.wait())
    f2 = PollingOperation(f, lambda x: x)
    assert f2.cancel()
    assert f2.cancelled()


def test_cancel_when_already_started(pool, event):
    f = pool.submit(lambda: event.wait())
    f2 = PollingOperation(f, lambda x: x)
    assert not f2.cancel()
    assert not f2.cancelled()


def test_empty(pool):
    f = pool.submit(lambda: 5)
    op = PollingOperations.empty(f)
    assert op.result() is None


def test_identity(pool):
    f = pool.submit(lambda: 5)
    op = PollingOperations.identity(f)
    assert op.result() == 5


def test_iterator(pool):
    f = pool.submit(lambda: [1, 2, 3])
    op = PollingOperations.iterator(f)
    it = op.result()
    assert isinstance(it, Iterator)
    assert list(it) == [1, 2, 3]
