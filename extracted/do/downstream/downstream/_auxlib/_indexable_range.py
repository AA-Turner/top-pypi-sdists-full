import typing


class indexable_range:
    """A sequence of integers supporting random access, slicing, and reversed
    iteration.

    Behaves similarly to built-in range but always returns indexable_range
    on slicing and reversed(), ensuring __getitem__ works consistently.
    """

    start: int
    stop: int
    step: int

    def __init__(
        self: "indexable_range",
        start: int,
        stop: typing.Optional[int] = None,
        step: int = 1,
    ) -> None:
        """Initialize an indexable_range.

        Parameters
        ----------
        start : int
            Start of the sequence, or stop if `stop` is None.
        stop : int, optional
            End of the sequence (exclusive).
        step : int, optional
            Step size between elements.
        """
        if stop is None:
            start, stop = 0, start

        range(start, stop, step)  # validate args

        self.start = start
        self.stop = stop
        self.step = step

    def __eq__(self: "indexable_range", other: object) -> bool:
        return isinstance(other, indexable_range) and (
            (self.start, self.stop, self.step)
            == (other.start, other.stop, other.step)
        )

    def __contains__(self: "indexable_range", value: object) -> bool:
        return value in range(self.start, self.stop, self.step)

    def __len__(self: "indexable_range") -> int:
        """Return the number of elements in the sequence."""
        return len(range(self.start, self.stop, self.step))

    def __getitem__(
        self: "indexable_range", index: typing.Union[int, slice]
    ) -> typing.Union[int, "indexable_range"]:
        """Retrieve an item or sub-range.

        Parameters
        ----------
        index : int or slice

        Returns
        -------
        int or indexable_range
        """
        if isinstance(index, slice):
            # determine new slice parameters
            start_idx, stop_idx, stride = index.indices(len(self))
            try:
                new_start = self[start_idx]
            except IndexError:
                return indexable_range(0)
            new_step = self.step * stride
            try:
                new_stop = self[stop_idx]
            except IndexError:
                new_stop = self.stop

            return indexable_range(new_start, new_stop, new_step)

        # handle negative indices
        if index < 0:
            index += len(self)

        res = self.start + index * self.step
        if not (
            [self.start, self.stop + 1][self.step < 0]
            <= res
            < [self.stop, self.start + 1][self.step < 0]
        ):
            raise IndexError("index out of range")
        return res

    def __iter__(self: "indexable_range") -> typing.Iterator[int]:
        """Iterate over the sequence."""
        yield from range(self.start, self.stop, self.step)

    def __reversed__(self: "indexable_range") -> "indexable_range":
        """Return reversed indexable_range.

        Returns
        -------
        indexable_range
        """
        if len(self) == 0:
            return self
        new_start = self[-1]
        new_step = -self.step
        new_stop = self.start - self.step
        return indexable_range(new_start, new_stop, new_step)

    def __repr__(self: "indexable_range") -> str:
        return f"indexable_range({self.start}, {self.stop}, {self.step})"

    def index(self: "indexable_range", value: int) -> int:
        """Return the index of the first occurrence of value."""
        return range(self.start, self.stop, self.step).index(value)
