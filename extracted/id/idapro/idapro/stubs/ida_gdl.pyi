from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""Low level graph drawing operations.

.. tip::
   The `IDA Domain API <https://ida-domain.docs.hex-rays.com/>`_ simplifies
   common tasks and provides better type hints, while remaining fully compatible
   with IDAPython for advanced use cases.

   For graph operations, see :mod:`ida_domain.functions`.
"""

class BasicBlock:
    r"""Basic block class. It is returned by the Flowchart class"""
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
    def __init__(self, id: Any, bb: Any, fc: Any) -> Any:
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
    def __repr__(self) -> str:
        r"""Return repr(self)."""
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
    def preds(self) -> Any:
        r"""
        Iterates the predecessors list
        
        """
        ...
    def succs(self) -> Any:
        r"""
        Iterates the successors list
        
        """
        ...

class FlowChart:
    r"""
    Flowchart class used to determine basic blocks.
    Check ex_gdl_qflow_chart.py for sample usage.
    
    """
    @property
    def size(self) -> Any: ...
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
    def __getitem__(self, index: Any) -> Any:
        r"""
        Returns a basic block
        
        :returns: BasicBlock
        
        """
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
    def __init__(self, f: Any = None, bounds: Any = None, flags: Any = 0) -> Any:
        r"""
        Constructor
        :param f: A func_t type, use get_func(ea) to get a reference
        :param bounds: A tuple of the form (start, end). Used if "f" is None
        :param flags: one of the FC_xxxx flags.
        
        """
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Any:
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
    def __repr__(self) -> str:
        r"""Return repr(self)."""
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
    def refresh(self) -> Any:
        r"""Refreshes the flow chart"""
        ...

class cancellable_graph_t(gdl_graph_t):
    @property
    def cancelled(self) -> bool: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __disown__(self) -> Any:
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
    def __init__(self) -> Any:
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
    def begin(self) -> Any:
        ...
    def edge(self, node: int, i: int, ispred: bool) -> int:
        ...
    def empty(self) -> bool:
        ...
    def end(self) -> Any:
        ...
    def entry(self) -> int:
        ...
    def exists(self, node: int) -> bool:
        ...
    def exit(self) -> int:
        ...
    def front(self) -> int:
        ...
    def get_edge_color(self, i: int, j: int) -> int:
        ...
    def get_node_color(self, n: int) -> int:
        ...
    def get_node_label(self, n: int) -> int:
        ...
    def nedge(self, node: int, ispred: bool) -> int:
        ...
    def node_qty(self) -> int:
        ...
    def npred(self, node: int) -> int:
        ...
    def nsucc(self, node: int) -> int:
        ...
    def pred(self, node: int, i: int) -> int:
        ...
    def print_edge(self, fp: Any, i: int, j: int) -> bool:
        ...
    def print_graph_attributes(self, fp: Any) -> None:
        ...
    def print_node(self, fp: Any, n: int) -> bool:
        ...
    def print_node_attributes(self, fp: Any, n: int) -> None:
        ...
    def size(self) -> int:
        ...
    def succ(self, node: int, i: int) -> int:
        ...

class edge_t:
    @property
    def dst(self) -> int: ...
    @property
    def src(self) -> int: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, y: edge_t) -> bool:
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
    def __init__(self, x: int = 0, y: int = 0) -> Any:
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
    def __lt__(self, y: edge_t) -> bool:
        ...
    def __ne__(self, y: edge_t) -> bool:
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

class edgevec_t:
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
    def __init__(self) -> Any:
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

class gdl_graph_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __disown__(self) -> Any:
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
    def __init__(self) -> Any:
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
    def begin(self) -> Any:
        ...
    def edge(self, node: int, i: int, ispred: bool) -> int:
        ...
    def empty(self) -> bool:
        ...
    def end(self) -> Any:
        ...
    def entry(self) -> int:
        ...
    def exists(self, node: int) -> bool:
        ...
    def exit(self) -> int:
        ...
    def front(self) -> int:
        ...
    def get_edge_color(self, i: int, j: int) -> int:
        ...
    def get_node_color(self, n: int) -> int:
        ...
    def get_node_label(self, n: int) -> int:
        ...
    def nedge(self, node: int, ispred: bool) -> int:
        ...
    def node_qty(self) -> int:
        ...
    def npred(self, node: int) -> int:
        ...
    def nsucc(self, node: int) -> int:
        ...
    def pred(self, node: int, i: int) -> int:
        ...
    def print_edge(self, fp: Any, i: int, j: int) -> bool:
        ...
    def print_graph_attributes(self, fp: Any) -> None:
        ...
    def print_node(self, fp: Any, n: int) -> bool:
        ...
    def print_node_attributes(self, fp: Any, n: int) -> None:
        ...
    def size(self) -> int:
        ...
    def succ(self, node: int, i: int) -> int:
        ...

class node_iterator:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, n: Any) -> bool:
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
    def __init__(self, _g: gdl_graph_t, n: int) -> Any:
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
    def __ne__(self, n: Any) -> bool:
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
    def __ref__(self) -> int:
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

class node_ordering_t:
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
    def __init__(self) -> Any:
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
    def clear(self) -> None:
        ...
    def clr(self, _node: int) -> bool:
        ...
    def node(self, _order: int) -> int:
        ...
    def order(self, _node: int) -> int:
        ...
    def resize(self, n: int) -> None:
        ...
    def set(self, _node: int, num: int) -> None:
        ...
    def size(self) -> int:
        ...

class qbasic_block_t:
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
    def __init__(self) -> Any:
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
    def empty(self) -> bool:
        r"""Is the size of the range_t <= 0?
        
        """
        ...
    def extend(self, ea: ida_idaapi.ea_t) -> None:
        r"""Ensure that the range_t includes 'ea'.
        
        """
        ...
    def intersect(self, r: range_t) -> None:
        r"""Assign the range_t to the intersection between the range_t and 'r'.
        
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

class qflow_chart_t(cancellable_graph_t, gdl_graph_t):
    @property
    def bounds(self) -> range_t: ...
    @property
    def cancelled(self) -> bool: ...
    @property
    def flags(self) -> int: ...
    @property
    def nproper(self) -> int: ...
    @property
    def pfn(self) -> func_t: ...
    @property
    def title(self) -> str: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __disown__(self) -> Any:
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
    def __getitem__(self, n: int) -> qbasic_block_t:
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
    def append_to_flowchart(self, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t) -> None:
        ...
    def begin(self) -> Any:
        ...
    def calc_block_type(self, blknum: int) -> fc_block_type_t:
        ...
    @overload
    def create(self, _title: str, _pfn: func_t, _ea1: ida_idaapi.ea_t, _ea2: ida_idaapi.ea_t, _flags: int) -> None: ...
    @overload
    def create(self, _title: str, ranges: rangevec_t, _flags: int) -> None: ...
    def edge(self, node: int, i: int, ispred: bool) -> int:
        ...
    def empty(self) -> bool:
        ...
    def end(self) -> Any:
        ...
    def entry(self) -> int:
        ...
    def exists(self, node: int) -> bool:
        ...
    def exit(self) -> int:
        ...
    def front(self) -> int:
        ...
    def get_edge_color(self, i: int, j: int) -> int:
        ...
    def get_node_color(self, n: int) -> int:
        ...
    def get_node_label(self, *args: Any) -> int:
        ...
    def is_noret_block(self, blknum: int) -> bool:
        ...
    def is_ret_block(self, blknum: int) -> bool:
        ...
    def nedge(self, node: int, ispred: bool) -> int:
        ...
    def node_qty(self) -> int:
        ...
    def npred(self, node: int) -> int:
        ...
    def nsucc(self, node: int) -> int:
        ...
    def pred(self, node: int, i: int) -> int:
        ...
    def print_edge(self, fp: Any, i: int, j: int) -> bool:
        ...
    def print_graph_attributes(self, fp: Any) -> None:
        ...
    def print_names(self) -> bool:
        ...
    def print_node(self, fp: Any, n: int) -> bool:
        ...
    def print_node_attributes(self, fp: Any, n: int) -> None:
        ...
    def refresh(self) -> None:
        ...
    def size(self) -> int:
        ...
    def succ(self, node: int, i: int) -> int:
        ...

def display_gdl(fname: str) -> int:
    r"""Display GDL file by calling wingraph32. The exact name of the grapher is taken from the configuration file and set up by setup_graph_subsystem(). The path should point to a temporary file: when wingraph32 succeeds showing the graph, the input file will be deleted. 
            
    :returns: error code from os, 0 if ok
    """
    ...

def gen_complex_call_chart(filename: str, wait: str, title: str, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, flags: int, recursion_depth: int = -1) -> bool:
    r"""Build and display a complex xref graph. 
            
    :param filename: output file name. the file extension is not used. maybe nullptr.
    :param wait: message to display during graph building
    :param title: graph title
    :param ea1: address range
    :param ea2: address range
    :param flags: combination of Call chart building flags and Flow graph building flags. if none of CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH is specified, the function will return false.
    :param recursion_depth: optional limit of recursion
    :returns: success. if fails, a warning message is displayed on the screen
    """
    ...

def gen_flow_graph(filename: str, title: str, pfn: func_t, ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, gflags: int) -> bool:
    r"""Build and display a flow graph. 
            
    :param filename: output file name. the file extension is not used. maybe nullptr.
    :param title: graph title
    :param pfn: function to graph
    :param ea1: if pfn == nullptr, then the address range
    :param ea2: if pfn == nullptr, then the address range
    :param gflags: combination of Flow graph building flags. if none of CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH is specified, the function will return false
    :returns: success. if fails, a warning message is displayed on the screen
    """
    ...

def gen_gdl(g: gdl_graph_t, fname: str) -> None:
    r"""Create GDL file for graph.
    
    """
    ...

def gen_simple_call_chart(filename: str, wait: str, title: str, gflags: int) -> bool:
    r"""Build and display a simple function call graph. 
            
    :param filename: output file name. the file extension is not used. maybe nullptr.
    :param wait: message to display during graph building
    :param title: graph title
    :param gflags: combination of CHART_NOLIBFUNCS and Flow graph building flags. if none of CHART_GEN_DOT, CHART_GEN_GDL, CHART_WINGRAPH is specified, the function will return false.
    :returns: success. if fails, a warning message is displayed on the screen
    """
    ...

def is_noret_block(btype: fc_block_type_t) -> bool:
    r"""Does this block never return?
    
    """
    ...

def is_ret_block(btype: fc_block_type_t) -> bool:
    r"""Does this block return?
    
    """
    ...

CHART_FOLLOW_DIRECTION: int  # 8
CHART_GEN_DOT: int  # 8192
CHART_GEN_GDL: int  # 16384
CHART_IGNORE_DATA_BSS: int  # 32
CHART_IGNORE_LIB_FROM: int  # 128
CHART_IGNORE_LIB_TO: int  # 64
CHART_IGNORE_XTRN: int  # 16
CHART_NOLIBFUNCS: int  # 1024
CHART_PRINT_COMMENTS: int  # 256
CHART_PRINT_DOTS: int  # 512
CHART_PRINT_NAMES: int  # 4096
CHART_RECURSIVE: int  # 4
CHART_REFERENCED: int  # 2
CHART_REFERENCING: int  # 1
CHART_WINGRAPH: int  # 32768
EDGE_BACK: int  # 3
EDGE_CROSS: int  # 4
EDGE_FORWARD: int  # 2
EDGE_NONE: int  # 0
EDGE_SUBGRAPH: int  # 5
EDGE_TREE: int  # 1
FC_APPND: int  # 8
FC_CALL_ENDS: int  # 32
FC_CHKBREAK: int  # 16
FC_NOEXT: int  # 2
FC_NOPREDS: int  # 64
FC_OUTLINES: int  # 128
FC_PREDS: int  # 0
FC_PRINT: int  # 1
FC_RESERVED: int  # 4
SWIG_PYTHON_LEGACY_BOOL: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
fcb_cndret: int  # 3
fcb_enoret: int  # 5
fcb_error: int  # 7
fcb_extern: int  # 6
fcb_indjump: int  # 1
fcb_noret: int  # 4
fcb_normal: int  # 0
fcb_ret: int  # 2
ida_idaapi: module
ida_range: module
types: module
weakref: module