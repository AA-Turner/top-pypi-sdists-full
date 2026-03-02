import typing

import numpy as np
import opytional as opyt

from .sticky_algo._sticky_lookup_ingest_times import sticky_lookup_ingest_times
from .sticky_algo._sticky_lookup_ingest_times_batched import (
    sticky_lookup_ingest_times_batched,
)

_maybe_np_T = typing.Union[np.ndarray, int]


class primed_algo:
    """Fills buffer from left-to-right before applying wrapped algorithm.

    Wrapped algorithm may be applied over a subset of buffer space, determined by
    left and right padding values. Useful for applications in hereditary
    stratigraphy, where buffer space is required to be prefilled.

    See Also
    --------
    __init__ : Constructor parameters and validation details.
    """

    _algo: typing.Any
    _pad_offset: int
    _pad_size: int

    def __init__(
        self: "primed_algo",
        *,
        algo: typing.Any,
        lpad: int,
        rpad: int,
    ) -> None:
        """Initialize the primed_algo with wrapped algorithm and buffer padding.

        Left and/or right padded areas are filled in initial left-to-right pass,
        but excluded from further writes by the wrapped algorithm.

        Parameters
        ----------
        algo : Any
            Module or class implementing a dstream algorithm.
        lpad : int
            Number of left pad bits to apply.
        rpad : int
            Number of right pad bits to apply.
        """
        self._algo = algo
        self._pad_offset = lpad
        self._pad_size = lpad + rpad

    def assign_storage_site(
        self: "primed_algo", S: int, T: int
    ) -> typing.Optional[int]:
        """Site selection algorithm for primed curation.

        Parameters
        ----------
        S : int
            Buffer size.
        T : int
            Current logical time. Must be within ingest capacity.

        Returns
        -------
        typing.Optional[int]
            Selected site, if any.

        Raises
        ------
        ValueError
            If insufficient ingest capacity is available.

            See `primed_algo.has_ingest_capacity` for details.
        """
        if T < S:
            return T
        else:
            return opyt.apply_if(
                self._algo.assign_storage_site(
                    S - self._pad_size,
                    T - S,
                ),
                self._pad_offset.__add__,
            )

    def assign_storage_site_batched(
        self: "primed_algo", S: int, T: _maybe_np_T
    ) -> np.ndarray:
        """Site selection algorithm for primed curation.

        Vectorized implementation for bulk calculations. Not yet implemented.

        Parameters
        ----------
        S : int or np.ndarray
            Buffer size.
        T : int or np.ndarray
            Current logical time. Must be within ingest capacity.

        Returns
        -------
        np.ndarray
            Selected site, if any. Otherwise, S.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError(
            "batched site assignment not yet implemented",
        )

    def get_ingest_capacity(
        self: "primed_algo", S: int
    ) -> typing.Optional[int]:
        """How many data item ingestions does this algorithm support?

        Calculated from the ingest capacities of the wrapped algorithm.
        Returns None if the number of supported ingestions is unlimited.

        See Also
        --------
        has_ingest_capacity : Does this algorithm have the capacity to ingest
            `n` data items?
        """
        if S < self._pad_size:
            return 0

        algo_capacity = self._algo.get_ingest_capacity(S - self._pad_size)
        return opyt.apply_if(algo_capacity, int(S).__add__)

    def has_ingest_capacity(self: "primed_algo", S: int, T: int) -> bool:
        """Does this algorithm have the capacity to ingest a data item at
        logical time T?

        Calculated from the ingest capacities of the wrapped algorithm.

        Parameters
        ----------
        S : int
            The number of buffer sites available.
        T : int
            Queried logical time.

        Returns
        -------
        bool

        See Also
        --------
        get_ingest_capacity : How many data item ingestions does this algorithm
            support?
        """
        if S < self._pad_size:
            return False

        return T < S or self._algo.has_ingest_capacity(
            S - self._pad_size, T - S
        )

    def lookup_ingest_times(
        self: "primed_algo", S: int, T: int
    ) -> typing.Iterable[typing.Optional[int]]:
        """Ingest time lookup algorithm for primed curation.

        Parameters
        ----------
        S : int
            Buffer size.
        T : int
            Current logical time.

        Yields
        ------
        typing.Optional[int]
            Ingest time of stored item at buffer sites in index order.
        """
        if T < S:
            yield from sticky_lookup_ingest_times(S, T)
        else:
            for k in range(self._pad_offset):
                yield k

            S_ = S - self._pad_size
            for k, T in enumerate(
                self._algo.lookup_ingest_times(S_, T - S),
                start=self._pad_offset,
            ):
                yield k if T is None else T + S

            for k in range(S - self._pad_size + self._pad_offset, S):
                yield k

    def lookup_ingest_times_eager(
        self: "primed_algo", S: int, T: int
    ) -> typing.List[int]:
        """Ingest time lookup algorithm for primed curation.

        Eager implementation.

        Parameters
        ----------
        S : int
            Buffer size.
        T : int
            Current logical time.

            Must be greater than or equal to S (i.e., all sites filled).

        Returns
        -------
        typing.List[int]
            Ingest time of stored item, if any, at buffer sites in index order.
        """
        if T < S:
            raise ValueError("T < S not supported for eager lookup")
        return list(self.lookup_ingest_times(S, T))

    def lookup_ingest_times_batched(
        self: "primed_algo",
        S: int,
        T: np.ndarray,
        parallel: bool = True,
    ) -> np.ndarray:
        """Ingest time lookup algorithm for primed curation.

        Vectorized implementation for bulk calculations.

        Parameters
        ----------
        S : int
            Buffer size.
        T : np.ndarray
            One-dimensional array of current logical times.

            Must be greater than or equal to S (i.e., all sites filled).
        parallel : bool, default True
            Should numba be applied to parallelize operations?

        Returns
        -------
        np.ndarray
            Ingest time of stored items at buffer sites in index order.

            Two-dimensional array. Each row corresponds to an entry in T.
            Contains S columns, each corresponding to buffer sites.
        """
        assert np.issubdtype(np.asarray(S).dtype, np.integer), S
        assert np.issubdtype(T.dtype, np.integer), T

        if (T < S).any():
            raise ValueError("T < S not supported for batched lookup")

        res = sticky_lookup_ingest_times_batched(S, T, parallel=parallel)

        S_ = S - self._pad_size
        ansatz = S + self._algo.lookup_ingest_times_batched(
            S_, np.maximum(T - S, S_), parallel=parallel
        )
        active_slice = slice(self._pad_offset, self._pad_offset + S_)
        res[:, active_slice] = np.where(
            ansatz >= T[:, None], res[:, active_slice], ansatz
        )
        return res
