import numbers
import typing

import numpy as np

from .._auxlib._jit import jit
from .._auxlib._jit_prange import jit_prange
from .._auxlib._pick_batched_chunk_size import pick_batched_chunk_size

_maybe_np_T = typing.Union[np.ndarray, int]


@jit(cache=True, nogil=True, nopython=True, parallel=True)
def _hybrid_remap_and_assign(
    res: np.ndarray,
    Tbar: np.ndarray,
    num_chunks: int,
    begin_chunk: int,
    span_chunk_length: int,
    span_offset: int,
    chunk_size: int = pick_batched_chunk_size(),
) -> None:
    """JIT-compiled remap of sub-algo results into hybrid output array."""
    num_rows = res.shape[0]
    span_length = Tbar.shape[1]
    num_chunks_ = np.int64(num_chunks)
    begin_chunk_ = np.int64(begin_chunk)
    span_chunk_length_ = np.int64(span_chunk_length)
    num_row_chunks = (num_rows + chunk_size - 1) // chunk_size
    for row_chunk in jit_prange(num_row_chunks):
        row_begin = row_chunk * chunk_size
        row_end = min(row_begin + chunk_size, num_rows)
        for i in range(row_begin, row_end):
            for j in range(span_length):
                v = np.int64(Tbar[i, j])
                res[i, span_offset + j] = np.uint64(
                    begin_chunk_
                    + (v // span_chunk_length_) * num_chunks_
                    + v % span_chunk_length_
                )


class hybrid_algo:
    """Composes dstream stream curation algorithms into a single hybrid
    algorithm.

    Buffer space is partitioned between algorithms, with algorithms taking
    turns ingesting data in a round-robin fashion. At an implementation level,
    buffer space is broken into a number of even chunks, based on the maximum
    fencepost value provided.

    See Also
    --------
    __init__ : Constructor parameters and validation details.
    """

    _algos: typing.List[typing.Any]
    _fenceposts: typing.List[int]
    _chunk_algo_indices: typing.List[int]

    def __init__(
        self: "hybrid_algo",
        *layout: typing.List,
    ) -> None:
        """
        Initialize the hybrid_algo with fencepost values and algorithms.

        Fencepost values partition buffer chunks between algorithms.

        Parameters
        ----------
        *layout : list
            Sequence of fencepost values and algorithms in an alternating
            pattern, as [fencepost0, algo0, fencepost1, algo2, ..., fencepostn].

            Fencepost values must be strinctly increasing integers. The first
            fencepost value must be zero.

            Algorithms must be dstream algo modules, or implement a compatible
            interface.

        Raises
        ------
        ValueError
            If fencepost values are not integers or not in increasing order,
            or if no algorithms/fenceposts are provided.

        Examples
        --------
        >>> from downstream.dstream import hybrid_algo
        >>> from downstream.dstream import stretched_algo, steady_algo
        >>> algo = hybrid_algo(0, stretched_algo, 1, steady_algo, 3)
        """
        self._algos = list(layout[1::2])
        self._fenceposts = list(layout[::2])
        if not all(
            isinstance(val, numbers.Integral) for val in self._fenceposts
        ):
            raise ValueError("Fencepost values must be integers")

        self.__name__ = (
            ".".join(self.__class__.__name__.split(".")[:-1])
            + "hybrid_"
            + "_".join(
                str(x)
                if isinstance(x, int)
                else x.__name__.split(".")[-1].removesuffix("_algo")
                for x in layout
            )
            + "_algo"
        )
        self._chunk_algo_indices = [
            index
            for index, __ in enumerate(self._algos)
            for __ in range(*self._fenceposts[index : index + 2])
        ]

        if not self._algos:
            raise ValueError("At least one algorithm required")
        if not len(self._fenceposts) >= 2:
            raise ValueError("At least two fenceposts required")
        if not all(val >= i for i, val in enumerate(self._fenceposts)):
            raise ValueError("Fenceposts must be in increasing order")

    def _get_num_chunks(self: "hybrid_algo") -> int:
        """Get the total number of chunks inferred from initialized fenceposts.

        Returns
        -------
        int
            The number of chunks, determined by the last fencepost values.
        """
        return self._fenceposts[-1]

    def _get_algo_index(self: "hybrid_algo", T: _maybe_np_T) -> _maybe_np_T:
        """Determine which algorithm should process a given time step.

        Parameters
        ----------
        T : int or ndarray
            The time step(s) to determine the responsible algorithm index.

        Returns
        -------
        int or ndarray
            The algorithm index (or indices) responsible for T.
        """
        leftover = T % self._get_num_chunks()
        return self._chunk_algo_indices[leftover]

    def _get_adj_T(
        self: "hybrid_algo", T: _maybe_np_T, index: _maybe_np_T
    ) -> _maybe_np_T:
        """How many time steps have been processed by the `index`th
        sub-algorithm?

        Parameters
        ----------
        T : int or ndarray
            The total number of time steps processed.
        index : int or ndarray
            The sub-algorithm index.

        Returns
        -------
        int or ndarray
        """
        begin_chunk = self._fenceposts[index]
        end_chunk = self._fenceposts[index + 1]
        span_chunk_length = end_chunk - begin_chunk
        num_chunks = self._get_num_chunks()

        assert np.asarray(T + num_chunks - end_chunk >= 0).all()  # T_ref
        if num_chunks.bit_count() == 1:  # power of two optimization
            num_whole_rounds = T >> (num_chunks.bit_length() - 1)
        else:
            num_whole_rounds = T // num_chunks
        partial_chunks = (
            np.clip(
                T % num_chunks, begin_chunk, span_chunk_length + begin_chunk
            )
            - begin_chunk
        )

        return num_whole_rounds * span_chunk_length + partial_chunks

    def _get_span_scale(self: "hybrid_algo", S: int) -> _maybe_np_T:
        """How many buffer sites does each chunk contain?

        Parameters
        ----------
        S : int
            The total buffer size.

        Returns
        -------
        int
        """
        num_chunks = self._get_num_chunks()
        if not S % num_chunks == 0:
            raise ValueError("chunks must evenly divide buffer size S")
        if num_chunks > S:
            raise ValueError("chunks must contain at least one buffer site")
        return S // num_chunks

    def _get_span_length(
        self: "hybrid_algo", S: int, index: _maybe_np_T
    ) -> _maybe_np_T:
        """How many buffer sites are assigned to the `index`th sub-algorithm?

        Parameters
        ----------
        S : int
            The total buffer size.
        index : int or np.ndarray
            The sub-algorithm index.

        Returns
        -------
        int or np.ndarray
        """
        span_scale = self._get_span_scale(S)
        begin_chunk = self._fenceposts[index]
        end_chunk = self._fenceposts[index + 1]
        return span_scale * (end_chunk - begin_chunk)

    def _get_span_offset(
        self: "hybrid_algo", S: int, index: _maybe_np_T
    ) -> _maybe_np_T:
        """What is the starting buffer offset for the `index`th sub-algorithm?

        Parameters
        ----------
        S : int
            The total buffer size.
        index : int or np.ndarray
            The sub-algorithm index.

        Returns
        -------
        int or np.ndarray
        """
        span_scale = self._get_span_scale(S)
        begin_chunk = self._fenceposts[index]
        return span_scale * begin_chunk

    def assign_storage_site(
        self: "hybrid_algo", S: int, T: int
    ) -> typing.Optional[int]:
        """Site selection algorithm for hybrid curation.

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

            See `hybrid_algo.has_ingest_capacity` for details.
        """
        index = self._get_algo_index(T)
        algo = self._algos[index]

        span_length = self._get_span_length(S, index)
        T_adj = self._get_adj_T(T, index)
        span_site = algo.assign_storage_site(span_length, int(T_adj))

        span_offset = self._get_span_offset(S, index)
        return span_offset + span_site if span_site is not None else None

    def assign_storage_site_batched(
        self: "hybrid_algo", S: int, T: _maybe_np_T
    ) -> np.ndarray:
        """Site selection algorithm for hybrid curation.

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
        self: "hybrid_algo", S: int
    ) -> typing.Optional[int]:
        """How many data item ingestions does this algorithm support?

        Calculated from the ingest capacities of the sub-algorithms. Returns
        None if the number of supported ingestions is unlimited.

        See Also
        --------
        has_ingest_capacity : Does this algorithm have the capacity to ingest
            `n` data items?
        """
        num_chunks = self._get_num_chunks()
        if S < num_chunks:
            return 0

        span_lengths = (
            self._get_span_length(S, i) for i, __ in enumerate(self._algos)
        )
        ingest_capacities = (
            algo.get_ingest_capacity(span_length)
            for span_length, algo in zip(span_lengths, self._algos)
        )
        return min(
            (
                capacity * num_chunks + self._fenceposts[i]
                for i, capacity in enumerate(ingest_capacities)
                if capacity is not None
            ),
            default=None,
        )

    def has_ingest_capacity(self: "hybrid_algo", S: int, T: int) -> bool:
        """Does this algorithm have the capacity to ingest a data item at
        logical time T?

        Calculated from the ingest capacities of the sub-algorithms.

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
        num_chunks = self._get_num_chunks()
        if S < num_chunks or S % num_chunks != 0:
            return False

        for T_ in range(max(0, T - num_chunks + 1), T + 1):
            index = self._get_algo_index(T_)
            if not self._algos[index].has_ingest_capacity(
                self._get_span_length(S, index),
                self._get_adj_T(T_, index),
            ):
                return False
        return True

    def lookup_ingest_times(
        self: "hybrid_algo", S: int, T: int
    ) -> typing.Iterable[typing.Optional[int]]:
        """Ingest time lookup algorithm for hybrid curation.

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
        for index, algo in enumerate(self._algos):
            adj_T = self._get_adj_T(T, index)
            span_length = self._get_span_length(S, index)

            num_chunks = self._get_num_chunks()
            begin_chunk = self._fenceposts[index]
            end_chunk = self._fenceposts[index + 1]
            span_chunk_length = end_chunk - begin_chunk

            for Tbar in algo.lookup_ingest_times(span_length, adj_T):
                if Tbar is not None:
                    yield begin_chunk + (
                        (Tbar // span_chunk_length) * num_chunks
                        + Tbar % span_chunk_length
                    )
                else:
                    yield None

    def lookup_ingest_times_eager(
        self: "hybrid_algo", S: int, T: int
    ) -> typing.List[int]:
        """Ingest time lookup algorithm for hybrid curation.

        Eager implementation.

        Parameters
        ----------
        S : int
            Buffer size.
        T : int
            Current logical time.

        Returns
        -------
        typing.List[int]
            Ingest time of stored item, if any, at buffer sites in index order.
        """
        if T < S:
            raise ValueError("T < S not supported for eager lookup")
        return list(self.lookup_ingest_times(S, T))

    def lookup_ingest_times_batched(
        self: "hybrid_algo",
        S: int,
        T: np.ndarray,
        parallel: bool = True,
    ) -> np.ndarray:
        """Ingest time lookup algorithm for hybrid curation.

        Vectorized implementation for bulk calculations.

        Parameters
        ----------
        S : int
            Buffer size.
        T : np.ndarray
            One-dimensional array of current logical times.
        parallel : bool, default True
            Should numba be applied to parallelize operations?

        Returns
        -------
        np.ndarray
            Ingest time of stored items at buffer sites in index order.

            Two-dimensional array. Each row corresponds to an entry in T.
            Contains S columns, each corresponding to buffer sites.
        """
        res = np.empty((T.size, S), dtype=np.uint64)
        for index, algo in enumerate(self._algos):
            adj_T = self._get_adj_T(T, index)
            span_length = self._get_span_length(S, index)
            Tbar = algo.lookup_ingest_times_batched(
                span_length,
                adj_T,
                parallel=parallel,
            )
            num_chunks = self._get_num_chunks()
            begin_chunk = self._fenceposts[index]
            end_chunk = self._fenceposts[index + 1]
            span_chunk_length = end_chunk - begin_chunk
            span_offset = self._get_span_offset(S, index)

            if parallel:
                _hybrid_remap_and_assign(
                    res,
                    Tbar,
                    num_chunks,
                    begin_chunk,
                    span_chunk_length,
                    span_offset,
                )
            else:
                subres = (
                    begin_chunk
                    + (Tbar // span_chunk_length) * num_chunks
                    + Tbar % span_chunk_length
                )
                res[:, span_offset : span_offset + span_length] = subres

        return res
