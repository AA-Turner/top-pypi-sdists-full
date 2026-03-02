from copy import deepcopy
import types
import typing

import numpy as np

from .._auxlib._pack_hex import pack_hex
from .._auxlib._unpack_hex import unpack_hex

_DSurfDataItem = typing.TypeVar("_DSurfDataItem")


class Surface(typing.Generic[_DSurfDataItem]):
    """Container orchestrating downstream curation over a fixed-size buffer."""

    __slots__ = ("_storage", "algo", "T")

    algo: types.ModuleType
    _storage: typing.MutableSequence[_DSurfDataItem]
    T: int  # current logical time

    @staticmethod
    def from_hex(
        hex_string: str,
        algo: types.ModuleType,
        *,
        S: int,
        storage_bitoffset: typing.Optional[int] = None,
        storage_bitwidth: int,
        T_bitoffset: int = 0,
        T_bitwidth: int = 32,
    ) -> "Surface":
        """
        Deserialize a Surface object from a hex string representation.

        Hex string representation needs exactly two contiguous parts:
        1. dstream_T (which is the number of ingesgted data items), and
        2. dstream_storage (which holds all the stored data items).

        Data items are deserialized as unsigned integers.

        Data in hex string representation should use big-endian byte order.

        Parameters
        ----------
        hex_string: str
            Hex string to be parsed, which can be uppercase or lowercase.
        algo: module
            Dstream algorithm to use to create the new Surface object.
        storage_bitoffset: int, default T_bitwidth
            Number of bits before the storage.
        storage_bitwidth: int
            Number of bits used for storage.
        T_bitoffset: int, default 0
            Number of bits before dstream_T.
        T_bitwidth: int, default 32
            Number of bits used to store dstream_T.
        S: int
            Number of buffer sites used to store data items.

            Determines how many items are unpacked from storage.

        See Also
        --------
        Surface.to_hex()
            Serialize a Surface object into a hex string.
        """
        if storage_bitoffset is None:
            storage_bitoffset = T_bitwidth

        for arg in (
            "storage_bitoffset",
            "storage_bitwidth",
            "T_bitoffset",
            "T_bitwidth",
        ):
            if locals()[arg] % 4:
                msg = f"Hex-unaligned `{arg}` not yet supported"
                raise NotImplementedError(msg)

        storage_hexoffset = storage_bitoffset // 4
        storage_hexwidth = storage_bitwidth // 4
        storage_hex = hex_string[
            storage_hexoffset : storage_hexoffset + storage_hexwidth
        ]
        storage = unpack_hex(storage_hex, S)

        T_hexoffset = T_bitoffset // 4
        T_hexwidth = T_bitwidth // 4
        T_hex = hex_string[T_hexoffset : T_hexoffset + T_hexwidth]
        T = int(T_hex, base=16)

        return Surface(algo, storage, T)

    def to_hex(
        self: "Surface", *, item_bitwidth: int, T_bitwidth: int = 32
    ) -> str:
        """
        Serialize a Surface object into a hex string representation.

        Serialized data comprises two components:
            1. dstream_T (the number of data items ingested) and
            2. dstream_storage (binary data of data item values).

        The hex layout used is:

            0x...
              ########**************************************************
              ^                                                     ^
              T, length = `T_bitwidth` / 4                          |
                                                                    |
                            storage, length = `item_bitwidth` / 4 * S

        This hex string can be reconstituted by calling `Surface.from_hex()`
        with the following parameters:
            - `T_bitoffset` = 0
            - `T_bitwidth` = `T_bitwidth`
            - `storage_bitoffset` = `storage_bitoffset`
            - `storage_bitwidth` = `self.S * item_bitwidth`

        Parameters
        ----------
        item_bitwidth: int
            Number of storage bits used per data item.
        T_bitwidth: int, default 32
            Number of bits used to store ingested items count (`self.T`).

        See Also
        --------
        Surface.from_hex()
            Deserialize a Surface object from a hex string.
        """
        if T_bitwidth % 4:
            raise NotImplementedError(
                "Hex-unaligned `T_bitwidth` not yet supported"
            )

        if not all(isinstance(x, typing.SupportsInt) for x in self._storage):
            raise NotImplementedError(
                "Non-integer hex serialization not yet implemented"
            )
        if np.asarray(self._storage).min() < 0:
            raise NotImplementedError(
                "Negative integer hex serialization not yet implemented"
            )

        assert self.T >= 0
        if int(self.T).bit_length() > T_bitwidth:
            raise ValueError(
                f"{self.T}= not representable in {T_bitwidth=} bits",
            )
        T_arr = np.asarray(self.T, dtype=np.uint64)
        T_bytes = T_arr.astype(">u8").tobytes()  # big-endian u64
        T_hexwidth = T_bitwidth >> 2
        T_hex = T_bytes.hex()[-T_hexwidth:]

        surface_hex = pack_hex(self._storage, item_bitwidth)

        return T_hex + surface_hex

    def __init__(
        self: "Surface",
        algo: types.ModuleType,
        storage: typing.Union[typing.MutableSequence[_DSurfDataItem], int],
        T: int = 0,
    ) -> None:
        """Initialize a downstream Surface object, which stores hereditary
        stratigraphic annotations using a provided algorithm.

        Parameters
        ----------
        algo: module
            The algorithm used by the surface to determine the placements
            of data items. Should be one of the modules in `downstream.dstream`.
        storage: int or MutableSequence
            The object used to hold any ingested data. If an integer is
            passed in, a list of length `storage` is used. Otherwise, the
            `storage` is used directly. Random access and `__len__` must be
            supported. For example, for efficient storage, a user may pass
            in a NumPy array.
        T: int, default 0
            The initial logical time (i.e. how many items have been ingested)
        """
        self.T = T
        if isinstance(storage, int):
            self._storage = [None] * storage
        else:
            self._storage = storage
        self.algo = algo

    def __repr__(self) -> str:
        return f"Surface(algo={self.algo}, storage={self._storage})"

    def __eq__(self: "Surface", other: typing.Any) -> bool:
        if not isinstance(other, Surface):
            return False
        return (
            self.T == other.T
            and self.algo is other.algo
            and [*self.lookup_zip_items()] == [*other.lookup_zip_items()]
        )

    def __iter__(
        self: "Surface",
    ) -> typing.Iterator[typing.Optional[_DSurfDataItem]]:
        return iter(self._storage)

    def __getitem__(
        self: "Surface", site: int
    ) -> typing.Optional[_DSurfDataItem]:
        return self._storage[site]

    def __deepcopy__(self: "Surface", memo: dict) -> "Surface":
        """Ensure pickle compatibility when algo is a module."""
        new_surf = Surface(self.algo, deepcopy(self._storage, memo))
        new_surf.T = self.T
        return new_surf

    @property
    def S(self: "Surface") -> int:
        return len(self._storage)

    @typing.overload
    def lookup_zip_items(
        self: "Surface",
    ) -> typing.Iterable[typing.Tuple[typing.Optional[int], _DSurfDataItem]]:
        ...

    @typing.overload
    def lookup_zip_items(
        self: "Surface", include_empty: typing.Literal[False]
    ) -> typing.Iterable[typing.Tuple[int, _DSurfDataItem]]:
        ...

    @typing.overload
    def lookup_zip_items(
        self: "Surface", include_empty: bool
    ) -> typing.Iterable[typing.Tuple[typing.Optional[int], _DSurfDataItem]]:
        ...

    def lookup_zip_items(
        self: "Surface", include_empty: bool = True
    ) -> typing.Iterable[typing.Tuple[typing.Optional[int], _DSurfDataItem]]:
        """
        Iterate over ingest times and values of data items in the order they
        appear on the downstream storage, including sites not yet written to.
        """
        res = zip(
            self.lookup(include_empty=True),
            self._storage,
        )
        if not include_empty:
            return ((T, v) for T, v in res if T is not None)
        return res

    def ingest_many(
        self: "Surface",
        n_ingests: int,
        item_getter: typing.Callable[[int], _DSurfDataItem],
        use_relative_time: bool = False,
    ) -> None:
        """Ingest multiple data items.

        Optimizes for the case where large amounts of data is ready to be
        ingested, In such a scenario, we can avoid assigning multiple objects
        to the same site, and simply iterate through sites that would be
        updated after items were ingested.

        Parameters
        ----------
        n_ingests : int
            The number of data to ingest
        item_getter : int -> object
            For a given ingest time within the n_ingests window, should
            return the associated data item.
        use_relative_time : bool, default False
            Use the relative time (i.e. timesteps since current self.T)
            instead of the absolute time as input to `item_getter`
        """

        assert n_ingests >= 0
        if n_ingests == 0:
            return

        assert self.algo.has_ingest_capacity(self.S, self.T + n_ingests - 1)
        for site, (T_1, T_2) in enumerate(
            zip(
                self.lookup(),
                self.algo.lookup_ingest_times(self.S, self.T + n_ingests),
            )
        ):
            if T_1 != T_2 and T_2 is not None:
                self._storage[site] = item_getter(
                    T_2 - self.T if use_relative_time else T_2
                )
        self.T += n_ingests

    def ingest_one(
        self: "Surface", item: _DSurfDataItem
    ) -> typing.Optional[int]:
        """Ingest data item.

        Returns the storage site of the data item, or None if the data item is
        not retained.
        """
        assert self.algo.has_ingest_capacity(self.S, self.T)

        site = self.algo.assign_storage_site(self.S, self.T)
        if site is not None:
            self._storage[site] = item
        self.T += 1
        return site

    @typing.overload
    def lookup(
        self: "Surface",
    ) -> typing.Iterable[typing.Optional[int]]:
        ...

    @typing.overload
    def lookup(
        self: "Surface", include_empty: typing.Literal[False]
    ) -> typing.Iterable[int]:
        ...

    @typing.overload
    def lookup(
        self: "Surface", include_empty: bool
    ) -> typing.Iterable[typing.Optional[int]]:
        ...

    def lookup(
        self: "Surface", include_empty: bool = True
    ) -> typing.Union[
        typing.Iterable[typing.Optional[int]], typing.Iterable[int]
    ]:
        """Iterate over data item ingest times, including null values for
        uninitialized sites."""
        assert len(self._storage) == self.S
        return (
            T
            for T in self.algo.lookup_ingest_times(self.S, self.T)
            if include_empty or T is not None
        )
