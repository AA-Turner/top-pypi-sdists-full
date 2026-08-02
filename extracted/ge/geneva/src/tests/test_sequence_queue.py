import logging

import pytest

from geneva.utils.sequence_queue import SequenceQueue


def test_basic_sequence() -> None:
    q = SequenceQueue[str]()
    q.put(0, 1, "first")
    q.put(1, 1, "second")
    q.put(2, 1, "third")

    assert q.pop() == "first"
    assert q.pop() == "second"
    assert q.pop() == "third"
    assert q.pop() is None


def test_out_of_order_insertion() -> None:
    q = SequenceQueue[str]()
    q.put(2, 1, "third")
    q.put(0, 1, "first")
    q.put(1, 1, "second")

    assert q.pop() == "first"
    assert q.pop() == "second"
    assert q.pop() == "third"
    assert q.pop() is None


def test_different_sizes() -> None:
    q = SequenceQueue[str]()
    q.put(1, 2, "second")  # size 2
    q.put(0, 1, "first")  # size 1
    q.put(3, 1, "third")  # size 1

    assert q.next_position() == 0
    assert q.pop() == "first"
    assert q.next_position() == 1
    assert q.pop() == "second"
    assert q.next_position() == 3
    assert q.pop() == "third"
    assert q.next_position() == 4
    assert q.pop() is None


def test_peek() -> None:
    q = SequenceQueue[str]()
    q.put(0, 1, "first")

    assert q.peek() == "first"
    assert q.pop() == "first"
    assert q.peek() is None


def test_empty_queue() -> None:
    q = SequenceQueue[str]()
    assert q.is_empty()
    assert q.pop() is None
    assert q.peek() is None
    assert q.next_position() == 0

    q.put(1, 1, "second")
    assert q.is_empty()
    assert q.pop() is None
    assert q.peek() is None
    assert q.next_position() == 0


def test_gap_in_sequence() -> None:
    q = SequenceQueue[str]()
    q.put(1, 1, "second")
    q.put(0, 1, "first")
    q.put(3, 1, "fourth")

    assert q.pop() == "first"
    assert q.pop() == "second"
    assert q.pop() is None  # Can't pop "fourth" because position 2 is missing
    assert q.next_position() == 2

    q.put(2, 1, "third")
    # Now we can pop "third" AND "fourth"
    assert q.pop() == "third"
    assert q.pop() == "fourth"
    assert q.pop() is None


def test_generic_type() -> None:
    q = SequenceQueue[int]()
    q.put(0, 1, 42)
    assert q.pop() == 42
    assert q.pop() is None


def test_no_wedge_on_overshooting_span() -> None:
    """Guards against the GEN-744 writer-hang wedge.

    If two items are enqueued with the same (too-large) span at different
    positions -- which happens when a recovery task_size splits an existing
    ``_range-START-END`` checkpoint, since the writer derives span from the key
    suffix -- the first overshoots ``next_position`` past the second. The
    second used to be permanently un-poppable: ``is_empty()`` was False (heap
    non-empty) but ``pop()`` returned None (head position < next_position),
    so the writer's ``while not is_empty(): pop()`` loop spun forever.

    Now a partially overlapping item is returned (the consumer trims the
    already-covered prefix) and a fully covered item is dropped, keeping
    ``is_empty()`` and ``pop()`` coherent.
    """
    q = SequenceQueue[str]()
    # Task [0,2): clipped span is 2, but the writer parses span=4 from the key.
    q.put(0, 4, "k@0")
    assert q.pop() == "k@0"
    assert q.next_position() == 4  # overshoot (true span was 2)

    # Task [2,4): same key, span re-parsed as 4 again; position 2 < next_pos 4.
    q.put(2, 4, "k@2")

    # Partial overlap ([2,6) extends past the cursor at 4): still poppable.
    assert not q.is_empty()
    assert q.pop() == "k@2"
    assert q.next_position() == 6
    assert q.is_empty()
    assert q.pop() is None


def test_fully_stale_item_dropped(caplog: pytest.LogCaptureFixture) -> None:
    """An item whose span is entirely behind the cursor contributes nothing."""
    q = SequenceQueue[str]()
    q.put(0, 4, "first")
    assert q.pop() == "first"
    assert q.next_position() == 4

    # Fully covered by the popped span: [2, 4) <= cursor 4.
    q.put(2, 2, "stale")
    with caplog.at_level(logging.WARNING, logger="geneva.utils.sequence_queue"):
        assert q.is_empty()
    # The drop is observable, with enough context to trace the producer.
    assert "position 2 (size 2, next_position 4)" in caplog.text
    assert q.pop() is None
    assert q.peek() is None
    assert q.next_position() == 4  # dropping does not advance the cursor

    # A later in-order item is not blocked by the dropped one.
    q.put(4, 1, "second")
    assert q.pop() == "second"
    assert q.next_position() == 5


def test_duplicate_item_dropped() -> None:
    """The same (position, size) enqueued twice pops once; the dup is reaped."""
    q = SequenceQueue[str]()
    q.put(0, 4, "a")
    q.put(0, 4, "b")
    assert q.pop() in ("a", "b")
    assert q.next_position() == 4
    assert q.is_empty()
    assert q.pop() is None


def test_partial_overlap_resyncs_cursor() -> None:
    """A partially overlapping pop advances the cursor to the item's end."""
    q = SequenceQueue[str]()
    q.put(0, 6, "first")  # covers [0, 6)
    q.put(4, 4, "second")  # covers [4, 8), overlapping [4, 6)
    assert q.pop() == "first"
    assert q.next_position() == 6
    assert q.pop() == "second"
    assert q.next_position() == 8
    assert q.pop() is None


def test_drain_loop_never_spins() -> None:
    """`while not is_empty(): pop()` terminates for any overlapping feed.

    This is the exact consumer shape used by the FragmentWriter drain; the
    GEN-744 wedge made it spin forever.
    """
    q = SequenceQueue[int]()
    # Overlapping, duplicated, and out-of-order spans.
    puts = [(0, 4), (2, 4), (2, 2), (4, 4), (3, 8), (11, 1), (0, 4)]
    for i, (pos, size) in enumerate(puts):
        q.put(pos, size, i)

    popped = 0
    while not q.is_empty():
        assert q.pop() is not None, "is_empty() False must imply a poppable item"
        popped += 1
        assert popped <= len(puts), "drain loop failed to terminate"
    assert q.next_position() == 12
