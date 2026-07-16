from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""Routines for working with functions within the disassembled program.

This file also contains routines for working with library signatures (e.g. FLIRT).

Each function consists of function chunks. At least one function chunk must be present in the function definition - the function entry chunk. Other chunks are called function tails. There may be several of them for a function.

A function tail is a continuous range of addresses. It can be used in the definition of one or more functions. One function using the tail is singled out and called the tail owner. This function is considered as 'possessing' the tail. get_func() on a tail address will return the function possessing the tail. You can enumerate the functions using the tail by using func_parent_iterator_t.

Each function chunk in the disassembly is represented as an "range" (a range of addresses, see range.hpp for details) with characteristics.
A function entry must start with an instruction (code) byte.

.. tip::
   The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies
   common tasks and provides better type hints, while remaining fully compatible
   with IDAPython for advanced use cases.

   For function management and analysis, see :mod:`ida_domain.functions`.
"""

class dyn_ea_array:
    @property
    def count(self) -> int: ...
    @property
    def data(self) -> int: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getitem__(self, i: int) -> int:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, _data: int, _count: int) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[int]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __len__(self) -> int:
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
    def __setitem__(self, i: int, v: int) -> None:
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        r"""Return str(self)."""
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

class dyn_range_array:
    @property
    def count(self) -> int: ...
    @property
    def data(self) -> range_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getitem__(self, i: int) -> range_t:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, _data: range_t, _count: int) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[range_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __len__(self) -> int:
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
    def __setitem__(self, i: int, v: range_t) -> None:
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        r"""Return str(self)."""
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

class dyn_regarg_array:
    @property
    def count(self) -> int: ...
    @property
    def data(self) -> regarg_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getitem__(self, i: int) -> regarg_t:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, _data: regarg_t, _count: int) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[regarg_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __len__(self) -> int:
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
    def __setitem__(self, i: int, v: regarg_t) -> None:
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        r"""Return str(self)."""
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

class dyn_regvar_array:
    @property
    def count(self) -> int: ...
    @property
    def data(self) -> regvar_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getitem__(self, i: int) -> regvar_t:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, _data: regvar_t, _count: int) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[regvar_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __len__(self) -> int:
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
    def __setitem__(self, i: int, v: regvar_t) -> None:
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        r"""Return str(self)."""
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

class dyn_stkpnt_array:
    @property
    def count(self) -> int: ...
    @property
    def data(self) -> stkpnt_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getitem__(self, i: int) -> stkpnt_t:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, _data: stkpnt_t, _count: int) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[stkpnt_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __len__(self) -> int:
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
    def __setitem__(self, i: int, v: stkpnt_t) -> None:
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        r"""Return str(self)."""
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

class fchunk_info_t:
    @property
    def end_ea(self) -> ida_idaapi.ea_t: ...
    @property
    def start_ea(self) -> ida_idaapi.ea_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: range_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: range_t) -> bool:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: range_t) -> bool:
        ...
    def __init__(self, start: ida_idaapi.ea_t = 0, end: ida_idaapi.ea_t = 0) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, r: range_t) -> bool:
        ...
    def __lt__(self, r: range_t) -> bool:
        ...
    def __ne__(self, r: range_t) -> bool:
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
    def analyzed_sp(self) -> bool:
        r"""Has SP-analysis been performed?
        
        """
        ...
    def clear(self) -> None:
        r"""Set start_ea, end_ea to 0.
        
        """
        ...
    def compare(self, r: range_t) -> int:
        ...
    @overload
    def contains(self, ea: ida_idaapi.ea_t) -> bool:
        r"""Compare two range_t instances, based on the start_ea.
        
        Is 'ea' in the address range?
        """
        ...
    @overload
    def contains(self, r: range_t) -> bool:
        r"""Is every ea in 'r' also in this range_t?"""
        ...
    def does_return(self) -> bool:
        r"""Does function return?
        
        """
        ...
    def empty(self) -> bool:
        r"""Is the size of the range_t <= 0?
        
        """
        ...
    def extend(self, ea: ida_idaapi.ea_t) -> None:
        r"""Ensure that the range_t includes 'ea'.
        
        """
        ...
    def get_flags(self) -> int:
        r"""Function chunk flags Function flags.
        
        """
        ...
    def intersect(self, r: range_t) -> None:
        r"""Assign the range_t to the intersection between the range_t and 'r'.
        
        """
        ...
    def is_entry(self) -> bool:
        r"""Is this an entry chunk?
        
        """
        ...
    def is_far(self) -> bool:
        r"""Is a far function?
        
        """
        ...
    def is_tail(self) -> bool:
        r"""Is this a tail chunk?
        
        """
        ...
    def is_valid(self) -> bool:
        r"""Is the function chunk info valid?
        
        """
        ...
    def need_prolog_analysis(self) -> bool:
        r"""Needs prolog analysis?
        
        """
        ...
    def overlaps(self, r: range_t) -> bool:
        r"""Is there an ea in 'r' that is also in this range_t?
        
        """
        ...
    def set_flags(self, v: int) -> None:
        ...
    def size(self) -> int:
        r"""Get end_ea - start_ea.
        
        """
        ...

class func_entry_info_t(fchunk_info_t):
    @property
    def end_ea(self) -> ida_idaapi.ea_t: ...
    @property
    def start_ea(self) -> ida_idaapi.ea_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: range_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: range_t) -> bool:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: range_t) -> bool:
        ...
    def __init__(self, start: ida_idaapi.ea_t = 0, end: ida_idaapi.ea_t = 0) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, r: range_t) -> bool:
        ...
    def __lt__(self, r: range_t) -> bool:
        ...
    def __ne__(self, r: range_t) -> bool:
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
    def analyzed_sp(self) -> bool:
        r"""Has SP-analysis been performed?
        
        """
        ...
    def clear(self) -> None:
        r"""Set start_ea, end_ea to 0.
        
        """
        ...
    def compare(self, r: range_t) -> int:
        ...
    @overload
    def contains(self, ea: ida_idaapi.ea_t) -> bool:
        r"""Compare two range_t instances, based on the start_ea.
        
        Is 'ea' in the address range?
        """
        ...
    @overload
    def contains(self, r: range_t) -> bool:
        r"""Is every ea in 'r' also in this range_t?"""
        ...
    def does_return(self) -> bool:
        r"""Does function return?
        
        """
        ...
    def empty(self) -> bool:
        r"""Is the size of the range_t <= 0?
        
        """
        ...
    def extend(self, ea: ida_idaapi.ea_t) -> None:
        r"""Ensure that the range_t includes 'ea'.
        
        """
        ...
    def get_argsize(self) -> int:
        r"""Number of bytes purged from the stack upon returning.
        
        """
        ...
    def get_cmt(self) -> str:
        r"""Function comment (requires GFI_CMT flag).
        
        """
        ...
    def get_cmt_rpt(self) -> str:
        r"""Repeatable function comment (requires GFI_CMT_RPT flag).
        
        """
        ...
    def get_color(self) -> int:
        r"""User defined function color.
        
        """
        ...
    def get_flags(self) -> int:
        r"""Function chunk flags Function flags.
        
        """
        ...
    def get_fpd(self) -> int:
        r"""Frame pointer delta.
        
        """
        ...
    def get_frame_id(self) -> int:
        r"""Netnode id of frame structure.
        
        """
        ...
    def get_frregs(self) -> int:
        r"""Size of saved registers in frame.
        
        """
        ...
    def get_frsize(self) -> int:
        r"""Size of local variables part of frame in bytes.
        
        """
        ...
    def get_name(self) -> str:
        r"""Function name (requires GFI_NAME flag).
        
        """
        ...
    def has(self, gfi_flags: int) -> bool:
        r"""Check if a string field was populated by get_func_entry_info(). 
                
        :param gfi_flags: combination of Flags for get_func_entry_info() flags to check
        :returns: true if all specified fields are available
        """
        ...
    def intersect(self, r: range_t) -> None:
        r"""Assign the range_t to the intersection between the range_t and 'r'.
        
        """
        ...
    def is_entry(self) -> bool:
        r"""Is this an entry chunk?
        
        """
        ...
    def is_far(self) -> bool:
        r"""Is a far function?
        
        """
        ...
    def is_tail(self) -> bool:
        r"""Is this a tail chunk?
        
        """
        ...
    def is_valid(self) -> bool:
        r"""Is the function chunk info valid?
        
        """
        ...
    def need_prolog_analysis(self) -> bool:
        r"""Needs prolog analysis?
        
        """
        ...
    def overlaps(self, r: range_t) -> bool:
        r"""Is there an ea in 'r' that is also in this range_t?
        
        """
        ...
    def set_argsize(self, v: int) -> None:
        ...
    def set_color(self, v: int) -> None:
        ...
    def set_flag(self, v: int, cnd: bool = True) -> None:
        r"""Set or clear function flag Function flags.
        
        """
        ...
    def set_flags(self, v: int) -> None:
        r"""Function flags Function flags.
        
        """
        ...
    def set_fpd(self, v: int) -> None:
        ...
    def set_frregs(self, v: int) -> None:
        ...
    def set_frsize(self, v: int) -> None:
        ...
    def size(self) -> int:
        r"""Get end_ea - start_ea.
        
        """
        ...

class func_item_iterator_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self, **kwargs: Any) -> Any:
        ...
    def __iter__(self) -> Any:
        r"""
        Provide an iterator on code items
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __next__(self, func: testf_t) -> bool:
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
        r"""Return str(self)."""
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
    def addresses(self) -> Any:
        r"""
        Provide an iterator on addresses contained within the function
        
        """
        ...
    def chunk(self) -> range_t:
        ...
    def code_items(self) -> Any:
        r"""
        Provide an iterator on code items contained within the function
        
        """
        ...
    def current(self) -> ida_idaapi.ea_t:
        ...
    def data_items(self) -> Any:
        r"""
        Provide an iterator on data items contained within the function
        
        """
        ...
    def decode_preceding_insn(self, visited: eavec_t, p_farref: bool, out: insn_t) -> bool:
        ...
    def decode_prev_insn(self, out: insn_t) -> bool:
        ...
    def first(self) -> bool:
        ...
    def head_items(self) -> Any:
        r"""
        Provide an iterator on item heads contained within the function
        
        """
        ...
    def last(self) -> bool:
        ...
    def next(self, func: testf_t) -> bool:
        ...
    def next_addr(self) -> bool:
        ...
    def next_code(self) -> bool:
        ...
    def next_data(self) -> bool:
        ...
    def next_head(self) -> bool:
        ...
    def next_not_tail(self) -> bool:
        ...
    def not_tails(self) -> Any:
        r"""
        Provide an iterator on non-tail addresses contained within the function
        
        """
        ...
    def prev(self, func: testf_t) -> bool:
        ...
    def prev_addr(self) -> bool:
        ...
    def prev_code(self) -> bool:
        ...
    def prev_data(self) -> bool:
        ...
    def prev_head(self) -> bool:
        ...
    def prev_not_tail(self) -> bool:
        ...
    def set(self, *args: Any) -> bool:
        r"""Set a function range. if pfn == nullptr then a segment range will be set.
        
        """
        ...
    def set_ea(self, _ea: ida_idaapi.ea_t) -> bool:
        ...
    def set_range(self, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
        r"""Set an arbitrary range.
        
        """
        ...
    def succ(self, func: testf_t) -> bool:
        r"""Similar to next(), but succ() iterates the chunks from low to high addresses, while next() iterates through chunks starting at the function entry chunk 
                
        """
        ...
    def succ_code(self) -> bool:
        ...

class func_parent_iterator_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self, **kwargs: Any) -> Any:
        ...
    def __iter__(self) -> Any:
        r"""
        Provide an iterator on function parents
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __next__(self) -> bool:
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
        r"""Return str(self)."""
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
    def first(self) -> bool:
        ...
    def last(self) -> bool:
        ...
    def next(self) -> bool:
        ...
    def parent(self) -> ida_idaapi.ea_t:
        ...
    def prev(self) -> bool:
        ...
    def reset_fnt(self, _fnt: func_t) -> None:
        ...
    def set(self, _fnt: func_t) -> bool:
        ...

class func_t:
    @property
    def argsize(self) -> int: ...
    @property
    def color(self) -> int: ...
    @property
    def end_ea(self) -> ida_idaapi.ea_t: ...
    @property
    def flags(self) -> int: ...
    @property
    def fpd(self) -> int: ...
    @property
    def frame(self) -> int: ...
    @property
    def frame_object(self) -> Any: ...
    @property
    def frregs(self) -> int: ...
    @property
    def frsize(self) -> int: ...
    @property
    def name(self) -> Any: ...
    @property
    def owner(self) -> ida_idaapi.ea_t: ...
    @property
    def pntqty(self) -> int: ...
    @property
    def points(self) -> stkpnt_t: ...
    @property
    def prototype(self) -> Any: ...
    @property
    def referers(self) -> int: ...
    @property
    def refqty(self) -> int: ...
    @property
    def regargqty(self) -> int: ...
    @property
    def regargs(self) -> regarg_t: ...
    @property
    def regvarqty(self) -> int: ...
    @property
    def regvars(self) -> regvar_t: ...
    @property
    def start_ea(self) -> ida_idaapi.ea_t: ...
    @property
    def tailqty(self) -> int: ...
    @property
    def tails(self) -> range_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: range_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: range_t) -> bool:
        ...
    def __get_points__(self) -> dynamic_wrapped_array_t:
        ...
    def __get_referers__(self) -> dynamic_wrapped_array_t:
        ...
    def __get_regargs__(self) -> dynamic_wrapped_array_t:
        ...
    def __get_regvars__(self) -> dynamic_wrapped_array_t:
        ...
    def __get_tails__(self) -> dynamic_wrapped_array_t:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: range_t) -> bool:
        ...
    def __init__(self, start: ida_idaapi.ea_t = 0, end: ida_idaapi.ea_t = 0, f: int = 0) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Any:
        r"""
        Alias for func_item_iterator_t(self).__iter__()
        
        """
        ...
    def __le__(self, r: range_t) -> bool:
        ...
    def __lt__(self, r: range_t) -> bool:
        ...
    def __ne__(self, r: range_t) -> bool:
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
    def addresses(self) -> Any:
        r"""
        Alias for func_item_iterator_t(self).addresses()
        
        """
        ...
    def analyzed_sp(self) -> bool:
        r"""Has SP-analysis been performed?
        
        """
        ...
    def clear(self) -> None:
        r"""Set start_ea, end_ea to 0.
        
        """
        ...
    def code_items(self) -> Any:
        r"""
        Alias for func_item_iterator_t(self).code_items()
        
        """
        ...
    def compare(self, r: range_t) -> int:
        ...
    @overload
    def contains(self, ea: ida_idaapi.ea_t) -> bool:
        r"""Compare two range_t instances, based on the start_ea.
        
        Is 'ea' in the address range?
        """
        ...
    @overload
    def contains(self, r: range_t) -> bool:
        r"""Is every ea in 'r' also in this range_t?"""
        ...
    def data_items(self) -> Any:
        r"""
        Alias for func_item_iterator_t(self).data_items()
        
        """
        ...
    def does_return(self) -> bool:
        r"""Does function return?
        
        """
        ...
    def empty(self) -> bool:
        r"""Is the size of the range_t <= 0?
        
        """
        ...
    def extend(self, ea: ida_idaapi.ea_t) -> None:
        r"""Ensure that the range_t includes 'ea'.
        
        """
        ...
    def get_frame_object(self) -> Any:
        r"""Retrieve the function frame, in the form of a structure
        where frame offsets that are accessed by the program, as well
        as areas for "saved registers" and "return address", are
        represented by structure members.
        
        If the function has no associated frame, return None
        
        :returns: a ida_typeinf.tinfo_t object representing the frame, or None
        """
        ...
    def get_name(self) -> Any:
        r"""Get the function name
        
        :returns: the function name
        """
        ...
    def get_prototype(self) -> Any:
        r"""Retrieve the function prototype.
        
        Once you have obtained the prototype, you can:
        
        * retrieve the return type through ida_typeinf.tinfo_t.get_rettype()
        * iterate on the arguments using ida_typeinf.tinfo_t.iter_func()
        
        If the function has no associated prototype, return None
        
        :returns: a ida_typeinf.tinfo_t object representing the prototype, or None
        """
        ...
    def head_items(self) -> Any:
        r"""
        Alias for func_item_iterator_t(self).head_items()
        
        """
        ...
    def intersect(self, r: range_t) -> None:
        r"""Assign the range_t to the intersection between the range_t and 'r'.
        
        """
        ...
    def is_far(self) -> bool:
        r"""Is a far function?
        
        """
        ...
    def need_prolog_analysis(self) -> bool:
        r"""Needs prolog analysis?
        
        """
        ...
    def not_tails(self) -> Any:
        r"""
        Alias for func_item_iterator_t(self).not_tails()
        
        """
        ...
    def overlaps(self, r: range_t) -> bool:
        r"""Is there an ea in 'r' that is also in this range_t?
        
        """
        ...
    def size(self) -> int:
        r"""Get end_ea - start_ea.
        
        """
        ...

class func_tail_info_t(fchunk_info_t):
    @property
    def end_ea(self) -> ida_idaapi.ea_t: ...
    @property
    def start_ea(self) -> ida_idaapi.ea_t: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: range_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: range_t) -> bool:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: range_t) -> bool:
        ...
    def __init__(self, start: ida_idaapi.ea_t = 0, end: ida_idaapi.ea_t = 0) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, r: range_t) -> bool:
        ...
    def __lt__(self, r: range_t) -> bool:
        ...
    def __ne__(self, r: range_t) -> bool:
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
    def analyzed_sp(self) -> bool:
        r"""Has SP-analysis been performed?
        
        """
        ...
    def clear(self) -> None:
        r"""Set start_ea, end_ea to 0.
        
        """
        ...
    def compare(self, r: range_t) -> int:
        ...
    @overload
    def contains(self, ea: ida_idaapi.ea_t) -> bool:
        r"""Compare two range_t instances, based on the start_ea.
        
        Is 'ea' in the address range?
        """
        ...
    @overload
    def contains(self, r: range_t) -> bool:
        r"""Is every ea in 'r' also in this range_t?"""
        ...
    def does_return(self) -> bool:
        r"""Does function return?
        
        """
        ...
    def empty(self) -> bool:
        r"""Is the size of the range_t <= 0?
        
        """
        ...
    def extend(self, ea: ida_idaapi.ea_t) -> None:
        r"""Ensure that the range_t includes 'ea'.
        
        """
        ...
    def get_flags(self) -> int:
        r"""Function chunk flags Function flags.
        
        """
        ...
    def get_owner(self) -> ida_idaapi.ea_t:
        r"""Primary owner function start_ea.
        
        """
        ...
    def get_refqty(self) -> int:
        r"""Number of refering functions (for quick checks without iterating).
        
        """
        ...
    def intersect(self, r: range_t) -> None:
        r"""Assign the range_t to the intersection between the range_t and 'r'.
        
        """
        ...
    def is_entry(self) -> bool:
        r"""Is this an entry chunk?
        
        """
        ...
    def is_far(self) -> bool:
        r"""Is a far function?
        
        """
        ...
    def is_tail(self) -> bool:
        r"""Is this a tail chunk?
        
        """
        ...
    def is_valid(self) -> bool:
        r"""Is the function chunk info valid?
        
        """
        ...
    def need_prolog_analysis(self) -> bool:
        r"""Needs prolog analysis?
        
        """
        ...
    def overlaps(self, r: range_t) -> bool:
        r"""Is there an ea in 'r' that is also in this range_t?
        
        """
        ...
    def set_flags(self, v: int) -> None:
        ...
    def size(self) -> int:
        r"""Get end_ea - start_ea.
        
        """
        ...

class func_tail_iterator_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self, **kwargs: Any) -> Any:
        ...
    def __iter__(self) -> Any:
        r"""
        Provide an iterator on function tails
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __next__(self) -> bool:
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
        r"""Return str(self)."""
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
    def chunk(self) -> range_t:
        ...
    def first(self) -> bool:
        ...
    def last(self) -> bool:
        ...
    def main(self) -> bool:
        ...
    def next(self) -> bool:
        ...
    def prev(self) -> bool:
        ...
    def set(self, *args: Any) -> bool:
        ...
    def set_ea(self, ea: ida_idaapi.ea_t) -> bool:
        ...
    def set_range(self, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
        ...

class function_item_iterator_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __next__(self, func: testf_t) -> bool:
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
        r"""Return str(self)."""
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
    def chunk(self, out: range_t) -> None:
        ...
    def current(self) -> ida_idaapi.ea_t:
        ...
    def decode_preceding_insn(self, visited: eavec_t, p_farref: bool, out: insn_t) -> bool:
        ...
    def decode_prev_insn(self, out: insn_t) -> bool:
        ...
    def first(self) -> bool:
        ...
    def last(self) -> bool:
        ...
    def next_addr(self) -> bool:
        ...
    def next_code(self) -> bool:
        ...
    def next_data(self) -> bool:
        ...
    def next_head(self) -> bool:
        ...
    def next_not_tail(self) -> bool:
        ...
    def prev(self, func: testf_t) -> bool:
        ...
    def prev_addr(self) -> bool:
        ...
    def prev_code(self) -> bool:
        ...
    def prev_data(self) -> bool:
        ...
    def prev_head(self) -> bool:
        ...
    def prev_not_tail(self) -> bool:
        ...
    def set(self, *args: Any) -> bool:
        r"""Set a function range. if func_ea == BADADDR then a segment range will be set.
        
        """
        ...
    def set_ea(self, ea: ida_idaapi.ea_t) -> bool:
        ...
    def set_range(self, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
        r"""Set an arbitrary range.
        
        """
        ...
    def succ(self, func: testf_t) -> bool:
        r"""Similar to next(), but succ() iterates the chunks from low to high addresses, while next() iterates through chunks starting at the function entry chunk 
                
        """
        ...
    def succ_code(self) -> bool:
        ...

class function_parent_iterator_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __next__(self) -> bool:
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
        r"""Return str(self)."""
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
    def first(self) -> bool:
        ...
    def last(self) -> bool:
        ...
    def parent(self) -> ida_idaapi.ea_t:
        ...
    def prev(self) -> bool:
        ...
    def set(self, tail_ea: ida_idaapi.ea_t) -> bool:
        ...

class function_tail_iterator_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
        ...
    def __new__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __next__(self) -> bool:
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
        r"""Return str(self)."""
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
    def chunk(self, out: range_t) -> None:
        ...
    def first(self) -> bool:
        ...
    def last(self) -> bool:
        ...
    def main(self) -> bool:
        ...
    def prev(self) -> bool:
        ...
    def set(self, *args: Any) -> bool:
        ...
    def set_ea(self, ea: ida_idaapi.ea_t) -> bool:
        ...
    def set_range(self, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
        ...

class lock_func:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, pfn: func_t) -> Any:
        ...
    def __init_subclass__(self, **kwargs: Any) -> Any:
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
        r"""Return str(self)."""
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

class lock_func_ea:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, ea: ida_idaapi.ea_t) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
        r"""Return str(self)."""
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

class lock_func_with_tails_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, value: Any) -> bool:
        r"""Return self==value."""
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, value: Any) -> bool:
        r"""Return self!=value."""
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
        r"""Return str(self)."""
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

class regarg_t:
    @property
    def name(self) -> int: ...
    @property
    def reg(self) -> int: ...
    @property
    def type(self) -> bytes: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: regarg_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: regarg_t) -> bool:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: regarg_t) -> bool:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, r: regarg_t) -> bool:
        ...
    def __lt__(self, r: regarg_t) -> bool:
        ...
    def __ne__(self, r: regarg_t) -> bool:
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
        r"""Return str(self)."""
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
    def compare(self, r: regarg_t) -> int:
        ...
    def deserialize(self, mmdsr: memory_deserializer_t) -> bool:
        ...
    def serialize(self, out: bytevec_t) -> None:
        ...
    def swap(self, r: regarg_t) -> None:
        ...

class regargs_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: regargs_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, value: Any) -> bool:
        r"""Return self>=value."""
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getitem__(self, i: int) -> regarg_t:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[regarg_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __le__(self, value: Any) -> bool:
        r"""Return self<=value."""
        ...
    def __len__(self) -> int:
        ...
    def __lt__(self, value: Any) -> bool:
        r"""Return self<value."""
        ...
    def __ne__(self, r: regargs_t) -> bool:
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
    def __setitem__(self, i: int, v: regarg_t) -> None:
        ...
    def __sizeof__(self) -> Any:
        r"""Size of object in memory, in bytes."""
        ...
    def __str__(self) -> str:
        r"""Return str(self)."""
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
    def add_unique(self, x: regarg_t) -> bool:
        ...
    def append(self, x: regarg_t) -> None:
        ...
    def at(self, _idx: int) -> regarg_t:
        ...
    def back(self) -> Any:
        ...
    def begin(self, *args: Any) -> qvector:
        ...
    def capacity(self) -> int:
        ...
    def clear(self) -> None:
        ...
    def empty(self) -> bool:
        ...
    def end(self, *args: Any) -> qvector:
        ...
    def erase(self, *args: Any) -> qvector:
        ...
    def extend(self, x: regargs_t) -> None:
        ...
    def extract(self) -> regarg_t:
        ...
    def find(self, *args: Any) -> qvector:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def has(self, x: regarg_t) -> bool:
        ...
    def inject(self, s: regarg_t, len: int) -> None:
        ...
    def insert(self, it: regarg_t, x: regarg_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> regarg_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: regargs_t) -> None:
        ...
    def truncate(self) -> None:
        ...

def add_func(*args: Any) -> bool:
    r"""Add a new function. If the function end address is BADADDR, then IDA will try to determine the function bounds by calling find_func_bounds(..., FIND_FUNC_DEFINE). 
            
    :param ea1: start address
    :param ea2: end address
    :returns: success
    """
    ...

def add_func_ex(pfn: func_t) -> bool:
    r"""Add a new function.
    
    :param pfn: ptr to filled function structure
    :returns: success
    """
    ...

def add_func_regarg(func_ea: ida_idaapi.ea_t, reg: int, tif: tinfo_t, name: str) -> None:
    ...

def add_function_ex(fi: func_entry_info_t) -> bool:
    r"""Add a new function using func_entry_info_t. If fi->end_ea is BADADDR, then IDA will try to determine the function bounds by calling find_func_bounds(..., FIND_FUNC_DEFINE). Uses fi->start_ea, fi->end_ea, and fi->get_flags(). On success, `fi` is updated with the resulting function properties. 
            
    :param fi: entry info describing the function to create
    :returns: success
    """
    ...

def add_regarg(pfn: func_t, reg: int, tif: tinfo_t, name: str) -> None:
    ...

def append_func_tail(pfn: func_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
    r"""Append a new tail chunk to the function definition. If the tail already exists, then it will simply be added to the function tail list Otherwise a new tail will be created and its owner will be set to be our function If a new tail cannot be created, then this function will fail. 
            
    :param pfn: pointer to the function
    :param ea1: start of the tail. If a tail already exists at the specified address it must start at 'ea1'
    :param ea2: end of the tail. If a tail already exists at the specified address it must end at 'ea2'. If specified as BADADDR, IDA will determine the end address itself.
    """
    ...

def append_func_tail_ea(func_ea: ida_idaapi.ea_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
    ...

def apply_idasgn_to(signame: str, ea: ida_idaapi.ea_t, is_startup: bool) -> int:
    r"""Apply a signature file to the specified address. 
            
    :param signame: short name of signature file (the file name without path)
    :param ea: address to apply the signature
    :param is_startup: if set, then the signature is treated as a startup one for startup signature ida doesn't rename the first function of the applied module.
    :returns: Library function codes
    """
    ...

def apply_startup_sig(ea: ida_idaapi.ea_t, startup: str) -> bool:
    r"""Apply a startup signature file to the specified address. 
            
    :param ea: address to apply the signature to; usually idainfo::start_ea
    :param startup: the name of the signature file without path and extension
    :returns: true if successfully applied the signature
    """
    ...

def calc_func_size(pfn: func_t) -> int:
    r"""Calculate function size. This function takes into account all fragments of the function. 
            
    :param pfn: ptr to function structure
    """
    ...

def calc_func_size_ea(ea: ida_idaapi.ea_t) -> int:
    ...

def calc_idasgn_state(n: int) -> int:
    r"""Get state of a signature in the list of planned signatures 
            
    :param n: number of signature in the list (0..get_idasgn_qty()-1)
    :returns: state of signature or IDASGN_BADARG
    """
    ...

def calc_thunk_func_target(*args: Any) -> int:
    r"""Calculate target of a thunk function. 
            
    :param pfn: pointer to function (may not be nullptr)
    :returns: the target function or BADADDR
    """
    ...

def calc_thunk_function_target(*args: Any) -> int:
    r"""Calculate thunk function target. 
            
    :param fi: function entry info
    :returns: the target function or BADADDR
    """
    ...

def del_func(ea: ida_idaapi.ea_t) -> bool:
    r"""Delete a function. 
            
    :param ea: any address in the function entry chunk
    :returns: success
    """
    ...

def del_idasgn(n: int) -> int:
    r"""Remove signature from the list of planned signatures. 
            
    :param n: number of signature in the list (0..get_idasgn_qty()-1)
    :returns: IDASGN_OK, IDASGN_BADARG, IDASGN_APPLIED
    """
    ...

def f_any(arg1: int, arg2: Any) -> bool:
    r"""Helper function to accept any address.
    
    """
    ...

def find_func_bounds(nfn: func_t, flags: int) -> int:
    r"""Determine the boundaries of a new function.
    
    :param nfn: structure to fill with information \ nfn->start_ea points to the start address of the new function.
    :param flags: Find function bounds flags
    :returns: Find function bounds result codes
    """
    ...

def find_function_bounds(fi: func_entry_info_t, flags: int) -> int:
    r"""Determine the boundaries of a new function. This function tries to find the start and end addresses of a new function. It calls the module with processor_t::func_bounds in order to fine tune the function boundaries. 
            
    :param fi: entry info to fill with information. \ fi->start_ea points to the start address of the new function.
    :param flags: Find function bounds flags
    :returns: Find function bounds result codes. On success, `fi` is updated with the resulting function properties.
    """
    ...

def free_regarg(v: regarg_t) -> None:
    ...

def func_contains(pfn: func_t, ea: ida_idaapi.ea_t) -> bool:
    ...

def func_does_return(callee: ida_idaapi.ea_t) -> bool:
    r"""Does the function return? To calculate the answer, FUNC_NORET flag and is_noret() are consulted The latter is required for imported functions in the .idata section. Since in .idata we have only function pointers but not functions, we have to introduce a special flag for them. 
            
    """
    ...

def func_parent_iterator_set(fpi: func_parent_iterator_t, pfn: func_t) -> bool:
    ...

def func_t__from_ptrval__(ptrval: int) -> Optional[func_t]:
    ...

def func_tail_iterator_set(fti: func_tail_iterator_t, pfn: func_t, ea: ida_idaapi.ea_t) -> bool:
    ...

def func_tail_iterator_set_ea(fti: func_tail_iterator_t, ea: ida_idaapi.ea_t) -> bool:
    ...

def function_contains(func_ea: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> bool:
    ...

def function_item_iterator_decode_preceding_insn(fii: function_item_iterator_t, visited: eavec_t, p_farref: bool, out: insn_t) -> bool:
    ...

def function_item_iterator_decode_prev_insn(fii: function_item_iterator_t, out: insn_t) -> bool:
    ...

def function_item_iterator_next(fii: function_item_iterator_t, testf: testf_t, ud: Any) -> bool:
    ...

def function_item_iterator_prev(fii: function_item_iterator_t, testf: testf_t, ud: Any) -> bool:
    ...

def function_item_iterator_succ(fii: function_item_iterator_t, testf: testf_t, ud: Any) -> bool:
    ...

def function_parent_iterator_first(fpi: function_parent_iterator_t) -> bool:
    ...

def function_parent_iterator_last(fpi: function_parent_iterator_t) -> bool:
    ...

def function_parent_iterator_next(fpi: function_parent_iterator_t) -> bool:
    ...

def function_parent_iterator_parent(fpi: function_parent_iterator_t) -> ida_idaapi.ea_t:
    ...

def function_parent_iterator_prev(fpi: function_parent_iterator_t) -> bool:
    ...

def function_parent_iterator_set(fpi: function_parent_iterator_t, tail_ea: ida_idaapi.ea_t) -> bool:
    ...

def function_tail_iterator_chunk(out: range_t, fti: function_tail_iterator_t) -> None:
    ...

def function_tail_iterator_first(fti: function_tail_iterator_t) -> bool:
    ...

def function_tail_iterator_last(fti: function_tail_iterator_t) -> bool:
    ...

def function_tail_iterator_main(fti: function_tail_iterator_t) -> bool:
    ...

def function_tail_iterator_next(fti: function_tail_iterator_t) -> bool:
    ...

def function_tail_iterator_prev(fti: function_tail_iterator_t) -> bool:
    ...

def function_tail_iterator_set(fti: function_tail_iterator_t, func_ea: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> bool:
    ...

def function_tail_iterator_set_ea(fti: function_tail_iterator_t, ea: ida_idaapi.ea_t) -> bool:
    ...

def function_tail_iterator_set_range(fti: function_tail_iterator_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
    ...

def get_current_idasgn() -> int:
    r"""Get number of the current signature. 
            
    :returns: 0..n-1
    """
    ...

def get_fchunk(ea: ida_idaapi.ea_t) -> Optional[func_t]:
    r"""Get pointer to function chunk structure by address. 
            
    :param ea: any address in a function chunk
    :returns: ptr to a function chunk or nullptr. This function may return a function entry as well as a function tail.
    """
    ...

def get_fchunk_ea_by_num(n: int) -> ida_idaapi.ea_t:
    ...

def get_fchunk_info(out: fchunk_info_t, ea: ida_idaapi.ea_t) -> bool:
    r"""Get the range of the function chunk (entry or tail) containing 'ea'. 
            
    :param out: pointer to output buffer, may be nullptr
    :param ea: any address in a function chunk
    :returns: true if a chunk was found at ea
    """
    ...

def get_fchunk_num(ea: ida_idaapi.ea_t) -> int:
    r"""Get ordinal number of a function chunk in the global list of function chunks. 
            
    :param ea: any address in the function chunk
    :returns: number of function chunk (0..get_fchunk_qty()-1). -1 means 'no function chunk at the specified address'.
    """
    ...

def get_fchunk_qty() -> int:
    r"""Get total number of function chunks in the program.
    
    """
    ...

def get_fchunk_referer(ea: int, idx: Any) -> Any:
    ...

def get_fchunk_start(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_func(ea: ida_idaapi.ea_t) -> Optional[func_t]:
    r"""Get pointer to function structure by address. 
            
    :param ea: any address in a function
    :returns: ptr to a function or nullptr. This function returns a function entry chunk.
    """
    ...

def get_func_bitness(pfn: func_t) -> int:
    r"""Get function bitness (which is equal to the function segment bitness). pfn==nullptr => returns 0 
            
    :returns: 0: 16
    :returns: 1: 32
    :returns: 2: 64
    """
    ...

def get_func_bitness_ea(ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_bits(pfn: func_t) -> int:
    ...

def get_func_bits_ea(ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_bytes(pfn: func_t) -> int:
    ...

def get_func_bytes_ea(ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_chunknum(pfn: func_t, ea: ida_idaapi.ea_t) -> int:
    r"""Get the containing tail chunk of 'ea'. 
            
    :returns: -1: means 'does not contain ea'
    :returns: 0: means the 'pfn' itself contains ea
    :returns: >0: the number of the containing function tail chunk
    """
    ...

def get_func_chunknum_ea(func_ea: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_cmt(pfn: func_t, repeatable: bool) -> Union[str, None]:
    r"""Get function comment. 
            
    :param pfn: ptr to function structure
    :param repeatable: get repeatable comment?
    :returns: size of comment or -1 In fact this function works with function chunks too.
    """
    ...

def get_func_cmt_ea(ea: ida_idaapi.ea_t, repeatable: bool) -> Union[str, None]:
    ...

def get_func_ea_by_num(n: int) -> ida_idaapi.ea_t:
    ...

def get_func_entry_info(out: func_entry_info_t, ea: ida_idaapi.ea_t, flags: int = 0) -> bool:
    r"""Get function entry info by address. 
            
    :param out: pointer to output buffer, may be nullptr
    :param ea: any address in a function
    :param flags: combination of Flags for get_func_entry_info() flags to control which optional string fields to populate
    :returns: true if a function entry was found at the given address
    """
    ...

def get_func_entry_info_by_num(out: func_entry_info_t, n: int, flags: int = 0) -> bool:
    r"""Get function entry info by ordinal number. 
            
    :param out: pointer to output buffer, may be nullptr
    :param n: number of function, is in range 0..get_func_qty()-1
    :param flags: combination of Flags for get_func_entry_info() flags
    :returns: true if a function with the given number exists
    """
    ...

def get_func_flags(ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_name(ea: ida_idaapi.ea_t) -> Union[str, None]:
    r"""Get function name. 
            
    :param ea: any address in the function
    :returns: length of the function name
    """
    ...

def get_func_num(ea: ida_idaapi.ea_t) -> int:
    r"""Get ordinal number of a function. 
            
    :param ea: any address in the function
    :returns: number of function (0..get_func_qty()-1). -1 means 'no function at the specified address'.
    """
    ...

def get_func_qty() -> int:
    r"""Get total number of functions in the program.
    
    """
    ...

def get_func_ranges(ranges: rangeset_t, pfn: func_t) -> ida_idaapi.ea_t:
    r"""Get function ranges. 
            
    :param ranges: buffer to receive the range info
    :param pfn: ptr to function structure
    :returns: end address of the last function range (BADADDR-error)
    """
    ...

def get_func_ranges_ea(ranges: rangeset_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_func_regarg(out: regarg_t, func_ea: ida_idaapi.ea_t, n: int) -> bool:
    ...

def get_func_regarg_qty(func_ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_regargs(out: regargs_t, func_ea: ida_idaapi.ea_t) -> bool:
    ...

def get_func_start(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_func_tail_info(out: func_tail_info_t, ea: ida_idaapi.ea_t) -> bool:
    r"""Get function tail info by address. 
            
    :param out: pointer to output buffer, may be nullptr
    :param ea: any address in a function tail chunk
    :returns: true if a tail chunk was found at the given address
    """
    ...

def get_func_tail_qty(func_ea: ida_idaapi.ea_t) -> int:
    ...

def get_func_tails(out: rangevec_t, func_ea: ida_idaapi.ea_t) -> bool:
    ...

def get_idasgn_desc(n: Any) -> Any:
    r"""Get information about a signature in the list.
    It returns: (name of signature, names of optional libraries)
    
    See also: get_idasgn_desc_with_matches
    
    :param n: number of signature in the list (0..get_idasgn_qty()-1)
    :returns: None on failure or tuple(signame, optlibs)
    """
    ...

def get_idasgn_desc_with_matches(n: Any) -> Any:
    r"""Get information about a signature in the list.
    It returns: (name of signature, names of optional libraries, number of matches)
    
    :param n: number of signature in the list (0..get_idasgn_qty()-1)
    :returns: None on failure or tuple(signame, optlibs, nmatches)
    """
    ...

def get_idasgn_qty() -> int:
    r"""Get number of signatures in the list of planned and applied signatures. 
            
    :returns: 0..n
    """
    ...

def get_idasgn_title(name: str) -> Union[str, None]:
    r"""Get full description of the signature by its short name. 
            
    :param name: short name of a signature
    :returns: size of signature description or -1
    """
    ...

def get_next_fchunk(ea: ida_idaapi.ea_t) -> Optional[func_t]:
    r"""Get pointer to the next function chunk in the global list. 
            
    :param ea: any address in the program
    :returns: ptr to function chunk or nullptr if next function chunk doesn't exist
    """
    ...

def get_next_fchunk_ea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_next_fchunk_info(out: fchunk_info_t, ea: ida_idaapi.ea_t) -> bool:
    r"""Get the next function chunk after the one containing 'ea'. 
            
    :param out: pointer to output buffer, may be nullptr
    :param ea: any address in the program
    :returns: true if a next chunk was found
    """
    ...

def get_next_func(ea: ida_idaapi.ea_t) -> Optional[func_t]:
    r"""Get pointer to the next function. 
            
    :param ea: any address in the program
    :returns: ptr to function or nullptr if next function doesn't exist
    """
    ...

def get_next_func_addr(pfn: func_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_next_func_ea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_next_function_addr(func_ea: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_prev_fchunk(ea: ida_idaapi.ea_t) -> Optional[func_t]:
    r"""Get pointer to the previous function chunk in the global list. 
            
    :param ea: any address in the program
    :returns: ptr to function chunk or nullptr if previous function chunk doesn't exist
    """
    ...

def get_prev_fchunk_ea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_prev_fchunk_info(out: fchunk_info_t, ea: ida_idaapi.ea_t) -> bool:
    r"""Get the previous function chunk before the one containing 'ea'. 
            
    :param out: pointer to output buffer, may be nullptr
    :param ea: any address in the program
    :returns: true if a previous chunk was found
    """
    ...

def get_prev_func(ea: ida_idaapi.ea_t) -> Optional[func_t]:
    r"""Get pointer to the previous function. 
            
    :param ea: any address in the program
    :returns: ptr to function or nullptr if previous function doesn't exist
    """
    ...

def get_prev_func_addr(pfn: func_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_prev_func_ea(ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_prev_function_addr(func_ea: ida_idaapi.ea_t, ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_tail_owner(tail_ea: ida_idaapi.ea_t) -> ida_idaapi.ea_t:
    ...

def get_tail_referer(tail_ea: ida_idaapi.ea_t, n: int) -> ida_idaapi.ea_t:
    r"""Get a tail chunk referer by index. 
            
    :param tail_ea: any address in a function tail chunk
    :param n: 0-based index
    :returns: referer (function start address), or BADADDR
    """
    ...

def get_tail_referer_qty(tail_ea: ida_idaapi.ea_t) -> int:
    r"""Get the number of referers (parent functions) for a tail chunk. 
            
    :param tail_ea: any address in a function tail chunk
    :returns: number of referers, or 0
    """
    ...

def get_tail_referers(out: eavec_t, tail_ea: ida_idaapi.ea_t) -> bool:
    r"""Get all referers (parent functions) for a tail chunk. 
            
    :param out: output vector of ea_t (function start addresses)
    :param tail_ea: any address in a function tail chunk
    :returns: success
    """
    ...

def getn_fchunk(n: int) -> Optional[func_t]:
    r"""Get pointer to function chunk structure by number. 
            
    :param n: number of function chunk, is in range 0..get_fchunk_qty()-1
    :returns: ptr to a function chunk or nullptr. This function may return a function entry as well as a function tail.
    """
    ...

def getn_func(n: int) -> Optional[func_t]:
    r"""Get pointer to function structure by number. 
            
    :param n: number of function, is in range 0..get_func_qty()-1
    :returns: ptr to a function or nullptr. This function returns a function entry chunk.
    """
    ...

def is_finally_visible_func(*args: Any, **kwargs: Any) -> bool:
    ...

def is_func_entry(pfn: func_t) -> bool:
    r"""Does function describe a function entry chunk?
    
    """
    ...

def is_func_locked(pfn: func_t) -> bool:
    r"""Is the function pointer locked?
    
    """
    ...

def is_func_locked_ea(ea: ida_idaapi.ea_t) -> bool:
    ...

def is_func_tail(pfn: func_t) -> bool:
    r"""Does function describe a function tail chunk?
    
    """
    ...

def is_function_entry(ea: ida_idaapi.ea_t) -> bool:
    ...

def is_function_tail(ea: ida_idaapi.ea_t) -> bool:
    ...

def is_same_fchunk(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
    ...

def is_same_func(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> bool:
    ...

def is_visible_func(*args: Any, **kwargs: Any) -> bool:
    ...

def iterate_func_chunks_ea(fchunk_ea: ida_idaapi.ea_t, visitor: func_chunk_visitor_t, include_parents: bool = False) -> None:
    ...

def lock_func_range(pfn: func_t, lock: bool) -> None:
    r"""Lock function pointer Locked pointers are guaranteed to remain valid until they are unlocked. Ranges with locked pointers cannot be deleted or moved.
    
    """
    ...

def lock_func_range_ea(ea: ida_idaapi.ea_t, lock: bool) -> None:
    ...

def plan_to_apply_idasgn(fname: str) -> int:
    r"""Add a signature file to the list of planned signature files. 
            
    :param fname: file name. should not contain directory part.
    :returns: 0 if failed, otherwise number of planned (and applied) signatures
    """
    ...

def read_regargs(pfn: func_t) -> None:
    ...

def reanalyze_function(*args: Any) -> None:
    r"""Reanalyze a function. This function plans to analyzes all chunks of the given function. Optional parameters (ea1, ea2) may be used to narrow the analyzed range. 
            
    :param pfn: pointer to a function
    :param ea1: start of the range to analyze
    :param ea2: end of range to analyze
    :param analyze_parents: meaningful only if pfn points to a function tail. if true, all tail parents will be reanalyzed. if false, only the given tail will be reanalyzed.
    """
    ...

def reanalyze_function_ea(*args: Any) -> None:
    ...

def reanalyze_noret_flag(ea: ida_idaapi.ea_t) -> bool:
    r"""Plan to reanalyze noret flag. This function does not remove FUNC_NORET if it is already present. It just plans to reanalysis. 
            
    """
    ...

def regarg_t__compare(l: regarg_t, r: regarg_t) -> int:
    ...

def remove_func_tail(pfn: func_t, tail_ea: ida_idaapi.ea_t) -> bool:
    r"""Remove a function tail. If the tail belongs only to one function, it will be completely removed. Otherwise if the function was the tail owner, the first function using this tail becomes the owner of the tail. 
            
    :param pfn: pointer to the function
    :param tail_ea: any address inside the tail to remove
    """
    ...

def remove_func_tail_ea(func_ea: ida_idaapi.ea_t, tail_ea: ida_idaapi.ea_t) -> bool:
    ...

def set_func_cmt(pfn: func_t, cmt: str, repeatable: bool) -> bool:
    r"""Set function comment. This function works with function chunks too. 
            
    :param pfn: ptr to function structure
    :param cmt: comment string, may be multiline (with '
    '). Use empty str ("") to delete comment
    :param repeatable: set repeatable comment?
    """
    ...

def set_func_cmt_ea(ea: ida_idaapi.ea_t, cmt: str, repeatable: bool) -> bool:
    ...

def set_func_end(ea: ida_idaapi.ea_t, newend: ida_idaapi.ea_t) -> bool:
    r"""Move function chunk end address. 
            
    :param ea: any address in the function
    :param newend: new end address of the function
    :returns: success
    """
    ...

def set_func_entry_info(fi: func_entry_info_t) -> bool:
    r"""Update function entry info in the database. You cannot use this function to change the range boundaries. Uses start_ea to identify the function, applies only modified fields. 
            
    :param fi: entry info to update
    :returns: success
    """
    ...

def set_func_flag(ea: ida_idaapi.ea_t, flag: int, on_off: bool = True) -> bool:
    ...

def set_func_flags(ea: ida_idaapi.ea_t, flags: int) -> bool:
    ...

def set_func_name_if_jumpfunc(pfn: func_t, oldname: str) -> int:
    r"""Give a meaningful name to function if it consists of only 'jump' instruction. 
            
    :param pfn: pointer to function (may be nullptr)
    :param oldname: old name of function. if old name was in "j_..." form, then we may discard it and set a new name. if oldname is not known, you may pass nullptr.
    :returns: success
    """
    ...

def set_func_start(ea: ida_idaapi.ea_t, newstart: ida_idaapi.ea_t) -> int:
    r"""Move function chunk start address. 
            
    :param ea: any address in the function
    :param newstart: new end address of the function
    :returns: Function move result codes
    """
    ...

def set_function_name_if_jumpfunc(func_ea: ida_idaapi.ea_t, oldname: str) -> bool:
    ...

def set_noret_insn(insn_ea: ida_idaapi.ea_t, noret: bool) -> bool:
    r"""Signal a non-returning instruction. This function can be used by the processor module to tell the kernel about non-returning instructions (like call exit). The kernel will perform the global function analysis and find out if the function returns at all. This analysis will be done at the first call to func_does_return() 
            
    :returns: true if the instruction 'noret' flag has been changed
    """
    ...

def set_tail_owner(fnt: func_t, new_owner: ida_idaapi.ea_t) -> bool:
    r"""Set a new owner of a function tail. The new owner function must be already referring to the tail (after append_func_tail). 
            
    :param fnt: pointer to the function tail
    :param new_owner: the entry point of the new owner function
    """
    ...

def set_tail_owner_ea(tail_ea: ida_idaapi.ea_t, new_owner: ida_idaapi.ea_t) -> bool:
    ...

def set_visible_func(pfn: func_t, visible: bool) -> None:
    r"""Set visibility of function
    
    """
    ...

def set_visible_func_ea(ea: ida_idaapi.ea_t, visible: bool) -> None:
    ...

def try_to_add_libfunc(ea: ida_idaapi.ea_t) -> int:
    r"""Apply the currently loaded signature file to the specified address. If a library function is found, then create a function and name it accordingly. 
            
    :param ea: any address in the program
    :returns: Library function codes
    """
    ...

def update_func(pfn: func_t) -> bool:
    r"""Update information about a function in the database (func_t). You must not change the function start and end addresses using this function. Use set_func_start() and set_func_end() for it. 
            
    :param pfn: ptr to function structure
    :returns: success
    """
    ...

FIND_FUNC_DEFINE: int  # 1
FIND_FUNC_EXIST: int  # 2
FIND_FUNC_IGNOREFN: int  # 2
FIND_FUNC_KEEPBD: int  # 4
FIND_FUNC_NORMAL: int  # 0
FIND_FUNC_OK: int  # 1
FIND_FUNC_UNDEF: int  # 0
FUNC_BOTTOMBP: int  # 256
FUNC_CATCH: int  # 1048576
FUNC_FAR: int  # 2
FUNC_FRAME: int  # 16
FUNC_FUZZY_SP: int  # 2048
FUNC_HIDDEN: int  # 64
FUNC_LIB: int  # 4
FUNC_LUMINA: int  # 65536
FUNC_NORET: int  # 1
FUNC_NORET_PENDING: int  # 512
FUNC_OUTLINE: int  # 131072
FUNC_PROLOG_OK: int  # 4096
FUNC_PURGED_OK: int  # 16384
FUNC_REANALYZE: int  # 262144
FUNC_SP_READY: int  # 1024
FUNC_STATICDEF: int  # 8
FUNC_TAIL: int  # 32768
FUNC_THUNK: int  # 128
FUNC_UNWIND: int  # 524288
FUNC_USERFAR: int  # 32
GFI_ALL: int  # 7
GFI_CMT: int  # 2
GFI_CMT_RPT: int  # 4
GFI_COMMENTS: int  # 6
GFI_NAME: int  # 1
IDASGN_APPLIED: int  # 2
IDASGN_BADARG: int  # 1
IDASGN_CURRENT: int  # 3
IDASGN_OK: int  # 0
IDASGN_PLANNED: int  # 4
LIBFUNC_DELAY: int  # 2
LIBFUNC_FOUND: int  # 0
LIBFUNC_NONE: int  # 1
MOVE_FUNC_BADSTART: int  # 2
MOVE_FUNC_NOCODE: int  # 1
MOVE_FUNC_NOFUNC: int  # 3
MOVE_FUNC_OK: int  # 0
MOVE_FUNC_REFUSED: int  # 4
SWIG_PYTHON_LEGACY_BOOL: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
ida_idaapi: module
ida_range: module
weakref: module