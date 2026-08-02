# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import queue

import pytest

from geneva.utils.byte_budget_queue import ByteBudgetedQueue


def test_byte_budgeted_queue_fifo_and_unmetered_items() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=10)

    budget_queue.put("first", 4)
    budget_queue.put_unmetered("sentinel")

    first = budget_queue.get()
    sentinel = budget_queue.get()

    assert first.item == "first"
    assert first.size_bytes == 4
    assert sentinel.item == "sentinel"
    assert sentinel.size_bytes == 0

    first.release()
    sentinel.release()


def test_byte_budgeted_queue_holds_budget_until_release() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=10)

    budget_queue.put("oversized", 11)
    lease = budget_queue.get()

    with pytest.raises(queue.Full):
        budget_queue.put("blocked", 1, timeout=0.01)

    lease.release()
    budget_queue.put("blocked", 1, timeout=0.01)

    unblocked = budget_queue.get()
    assert unblocked.item == "blocked"
    unblocked.release()


def test_byte_budgeted_queue_allows_one_item_to_cross_budget() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=10)

    budget_queue.put("first", 6)
    budget_queue.put("second", 6)

    assert budget_queue.outstanding_bytes == 12
    with pytest.raises(queue.Full):
        budget_queue.put("third", 1, timeout=0.01)

    first = budget_queue.get()
    second = budget_queue.get()
    first.release()

    budget_queue.put("third", 1, timeout=0.01)

    second.release()
    third = budget_queue.get()
    assert third.item == "third"
    third.release()


def test_byte_budgeted_queue_unmetered_put_ignores_budget() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=10)

    budget_queue.put("oversized", 11)
    budget_queue.put_unmetered("sentinel")

    oversized = budget_queue.get()
    sentinel = budget_queue.get()

    assert oversized.item == "oversized"
    assert sentinel.item == "sentinel"

    oversized.release()
    sentinel.release()


def test_byte_budgeted_queue_get_timeout_raises_empty() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=10)

    with pytest.raises(queue.Empty):
        budget_queue.get(timeout=0.01)


def test_byte_budgeted_queue_release_is_idempotent() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=10)

    budget_queue.put("item", 11)
    lease = budget_queue.get()

    lease.release()
    lease.release()

    assert budget_queue.outstanding_bytes == 0
    budget_queue.put("next", 1, timeout=0.01)


def test_byte_budgeted_queue_disabled_budget_never_blocks() -> None:
    budget_queue = ByteBudgetedQueue[str](max_bytes=0)

    budget_queue.put("first", 100)
    budget_queue.put("second", 100, timeout=0.01)

    assert budget_queue.outstanding_bytes == 0
    assert budget_queue.get().item == "first"
    assert budget_queue.get().item == "second"
