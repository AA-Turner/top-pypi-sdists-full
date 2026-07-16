from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""Definition of the bitrange_t class."""

class bitrange_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: bitrange_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: bitrange_t) -> bool:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: bitrange_t) -> bool:
        ...
    def __init__(self, bit_ofs: int = 0, size_in_bits: int = 0) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, r: bitrange_t) -> bool:
        ...
    def __lt__(self, r: bitrange_t) -> bool:
        ...
    def __ne__(self, r: bitrange_t) -> bool:
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __reduce_ex__(self, protocol: Any) -> Any:
        r"""Helper for pickle."""
        ...
    def __repr__(self) -> Any:
        ...
    def __setattr__(self, name: Any, value: Any) -> Any:
        r"""Implement setattr(self, name, value)."""
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        ...
    def __subclasshook__(self, object: Any) -> Any:
        r"""Abstract classes can override this to customize issubclass().
        
        This is invoked early on by abc.ABCMeta.__subclasscheck__().
        It should return True, False or NotImplemented.  If it returns
        NotImplemented, the normal algorithm is used.  Otherwise, it
        overrides the normal algorithm (and the outcome is cached).
        
        """
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def apply_mask(self, subrange: bitrange_t) -> bool:
        r"""Apply mask to a bitrange 
                
        :param subrange: range *inside* the main bitrange to keep After this operation the main bitrange will be truncated to have only the bits that are specified by subrange. Example: [off=8,nbits=4], subrange[off=1,nbits=2] => [off=9,nbits=2]
        :returns: success
        """
        ...
    def bitoff(self) -> int:
        r"""Get offset of 1st bit.
        
        """
        ...
    def bitsize(self) -> int:
        r"""Get size of the value in bits.
        
        """
        ...
    def bytesize(self) -> int:
        r"""Size of the value in bytes.
        
        """
        ...
    def compare(self, r: bitrange_t) -> int:
        ...
    def create_union(self, r: bitrange_t) -> None:
        r"""Create union of 2 ranges including the hole between them.
        
        """
        ...
    def empty(self) -> bool:
        r"""Is the bitrange empty?
        
        """
        ...
    def extract(self, src: Any, is_mf: bool) -> bool:
        ...
    def has_common(self, r: bitrange_t) -> bool:
        r"""Does have common bits with another bitrange?
        
        """
        ...
    def init(self, bit_ofs: int, size_in_bits: int) -> None:
        r"""Initialize offset and size to given values.
        
        """
        ...
    def inject(self, dst: Any, src: bytevec_t, is_mf: bool) -> bool:
        ...
    def intersect(self, r: bitrange_t) -> None:
        r"""Intersect two ranges.
        
        """
        ...
    def mask64(self) -> int:
        r"""Convert to mask of 64 bits.
        
        """
        ...
    def reset(self) -> None:
        r"""Make the bitrange empty.
        
        """
        ...
    def shift_down(self, cnt: int) -> None:
        r"""Shift range down (left).
        
        """
        ...
    def shift_up(self, cnt: int) -> None:
        r"""Shift range up (right).
        
        """
        ...
    def sub(self, r: bitrange_t) -> bool:
        r"""Subtract a bitrange.
        
        """
        ...

SWIG_PYTHON_LEGACY_BOOL: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
ida_idaapi: module
weakref: module