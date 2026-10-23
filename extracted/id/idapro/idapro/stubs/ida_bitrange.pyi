from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""Definition of the bitrange_t class."""

class bitrange_t:
    def __eq__(self, r: bitrange_t) -> bool:
        ...
    def __ge__(self, r: bitrange_t) -> bool:
        ...
    def __gt__(self, r: bitrange_t) -> bool:
        ...
    def __init__(self, bit_ofs: int = 0, size_in_bits: int = 0) -> Any:
        ...
    def __le__(self, r: bitrange_t) -> bool:
        ...
    def __lt__(self, r: bitrange_t) -> bool:
        ...
    def __ne__(self, r: bitrange_t) -> bool:
        ...
    def __repr__(self) -> Any:
        ...
    def __str__(self) -> str:
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