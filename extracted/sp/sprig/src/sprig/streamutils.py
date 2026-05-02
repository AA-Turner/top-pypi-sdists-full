import collections
import heapq
import itertools
import operator
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    FrozenSet,
    Generic,
    Hashable,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
)

from typing_extensions import Protocol

from sprig import iterutils

_SENTINEL = object()


class _SupportsSort(Protocol):  # pylint: disable=too-few-public-methods
    def __lt__(self, other):
        ...


_T = TypeVar("_T")
_SortableT = TypeVar("_SortableT", bound=_SupportsSort)
_HashableT = TypeVar("_HashableT", bound=Hashable)
# The time type only really need to support subtraction and comparison but I am not
# sure how to specify that
_TimeT = TypeVar("_TimeT", int, float)


class ManagedMerger(Generic[_T, _HashableT, _SortableT]):
    """Sort a partially sorted iterator

    It must be possible to bucket the iterator into individually sorted iterators.

    A typical use case for this would be sorting incoming TCP messages from several
    sources; Thanks to TCP the messages from each source are guaranteed to be ordered
    and thanks to IP the messages can be bucketed by the source.

    Notice in the example below that
    * the vowels and consonants are each sorted in the input, and
    * the output is sorted without regard for the case of the letter.

    >>> emitted = []
    >>> merger = ManagedMerger(emitted.append)
    >>> merger.register(False)
    >>> merger.register(True)
    >>> for c in "aEbcdifgh": merger.put(c, c.lower() in "aeiou", c.lower())
    >>> merger.close()
    >>> "".join(emitted)
    'abcdEfghi'
    """

    def __init__(
        self,
        callback: Callable[[_T], Any],
    ) -> None:
        self._callback = callback

        self._channels: Dict[_HashableT, Deque[Tuple[_SortableT, _T]]] = {}
        self._blocking: Dict[_HashableT, int] = {}
        self._available: List[
            Tuple[_SortableT, int, _HashableT, Deque[Tuple[_SortableT, _T]]]
        ] = []
        self._tie_breakers = itertools.count()
        self._time: Optional[_SortableT] = None

    def register(self, sender: _HashableT) -> None:
        if sender in self._channels:
            raise ValueError

        self._channels[sender] = collections.deque()
        self._blocking[sender] = next(self._tie_breakers)

    def unregister(self, sender: _HashableT) -> None:
        msgs = self._channels.pop(sender)
        if msgs:
            msgs.append(_SENTINEL)  # type: ignore
        else:
            del self._blocking[sender]
            self._flush()

    def put(self, msg: _T, sender: _HashableT, time: _SortableT) -> None:
        msgs = self._channels[sender]

        if msgs:
            if time < msgs[-1][0]:
                raise ValueError
            msgs.append((time, msg))
        else:
            if self._time is not None and time < self._time:
                raise ValueError
            msgs.append((time, msg))
            tie_breaker = self._blocking.pop(sender)
            heapq.heappush(self._available, (time, tie_breaker, sender, msgs))
            self._flush()

    def _flush(self) -> None:
        while not self._blocking and self._available:
            self._time, tie_breaker, src, msgs = heapq.heappop(self._available)
            _, msg = msgs.popleft()

            self._callback(msg)

            if msgs:
                if msgs[0] is not _SENTINEL:
                    heapq.heappush(
                        self._available,
                        (msgs[0][0], tie_breaker, src, msgs),
                    )
            else:
                self._blocking[src] = tie_breaker

    def close(self) -> None:
        for src in list(self._channels):
            self.unregister(src)


class BucketMerger(Generic[_T, _HashableT, _SortableT]):
    def __init__(
        self,
        sort_key: Callable[[_T], _SortableT],
        bucket_key: Callable[[_T], _HashableT],
        callback: Callable[[_T], Any],
    ) -> None:
        self._get_time = sort_key
        self._get_src = bucket_key
        self._merger: ManagedMerger[_T, _HashableT, _SortableT] = ManagedMerger(
            callback
        )

    def register(self, src: _HashableT) -> None:
        self._merger.register(src)

    def unregister(self, src: _HashableT) -> None:
        self._merger.unregister(src)

    def put(self, msg: _T) -> None:
        time = self._get_time(msg)
        src = self._get_src(msg)
        self._merger.put(msg, src, time)

    def close(self) -> None:
        self._merger.close()


class TimeoutMerger(Generic[_T, _HashableT, _TimeT]):
    """Merge sorted streams of messages

    This class automatically handles the registering of senders joining the cluster and
    the unregistering of senders leaving the clusters using a timeout heuristic; if one
    sender falls behind the leading sender by more than a given duration, then the
    silent sender is presumed to have left.

    Convenient when senders leaving the cluster is a rare occurrence but probably a bad
    fit otherwise.
    """

    def __init__(self, callback: Callable[[_T], Any], timeout: _TimeT) -> None:
        self._merger: ManagedMerger[_T, _HashableT, _TimeT] = ManagedMerger(callback)
        self._timeout: _TimeT = timeout
        self._timeout_ends: Dict[_HashableT, _TimeT] = {}

    def put(self, msg: _T, sender: _HashableT, time: _TimeT) -> None:
        # disable protected-access because I want to try out using `_time` before
        # making it part of the interface.
        # pylint: disable=protected-access
        timeout_end = time + self._timeout
        if sender in self._timeout_ends and timeout_end < self._timeout_ends[sender]:
            raise ValueError("Time must be non-decreasing")

        self._flush(time)
        self._touch(sender, timeout_end=timeout_end)
        if self._merger._time is None or self._merger._time <= time:
            self._merger.put(msg, sender, time)

    def _touch(self, sender: _HashableT, timeout_end: _TimeT) -> None:
        if sender not in self._timeout_ends:
            self._merger.register(sender)
        self._timeout_ends[sender] = timeout_end

    def _flush(self, time: _TimeT) -> None:
        # This has horrible asymptotic runtime but should be reasonably fast in
        # practice for many cases.
        while self._timeout_ends:
            sender, timeout_end = min(
                self._timeout_ends.items(), key=operator.itemgetter(0)
            )
            if time <= timeout_end:
                break
            # Unregistering may release detained messages so we make sure to update
            # `timeout_ends` a.k.a. `senders` first.
            del self._timeout_ends[sender]
            self._merger.unregister(sender)

    @property
    def senders(self) -> FrozenSet[_HashableT]:
        return frozenset(self._timeout_ends)


class _Bucket:
    def __init__(self):
        self._deque = collections.deque()

    def append(self, item):
        self._deque.append(item)

    def __len__(self):
        return len(self._deque)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._deque.popleft()
        except IndexError as e:
            raise StopIteration from e


class SimpleBucketMerger(Generic[_T]):
    """A simpler and less flexible version

    Implemented as warm up, kept for comparison (for now).
    """

    def __init__(
        self,
        sort_key: Callable[[_T], _SupportsSort],
        bucket_key: Callable[[_T], _HashableT],
        bucket_keys: Iterable[_HashableT],
        callback: Callable[[_T], Any],
    ) -> None:
        self._bucket_key = bucket_key
        self._callback = callback
        self._buckets = {k: _Bucket() for k in bucket_keys}
        self._sorted = iterutils.imerge(self._buckets.values(), sort_key)

    def put(self, item: _T) -> None:
        self._buckets[self._bucket_key(item)].append(item)
        while all(self._buckets.values()):
            self._callback(next(self._sorted))

    def close(self) -> None:
        for item in self._sorted:
            self._callback(item)
