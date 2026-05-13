from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""Types involved in grouping of item into folders.

The dirtree_t class is used to organize a directory tree on top of any collection that allows for accessing its elements by an id (inode).
No requirements are imposed on the inodes apart from the forbidden value -1 (used to denote a bad inode).
The dirspec_t class is used to specialize the dirtree. It can be used to introduce a directory structure for:
* local types
* structs
* enums
* functions
* names
* etc
"""

class direntry_t:
    BADIDX: int  # 18446744073709551615
    ROOTIDX: int  # 0
    @property
    def idx(self) -> int: ...
    @property
    def isdir(self) -> bool: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: direntry_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: direntry_t) -> bool:
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
    def __lt__(self, r: direntry_t) -> bool:
        ...
    def __ne__(self, r: direntry_t) -> bool:
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
    def valid(self) -> bool:
        ...

class direntry_vec_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: direntry_vec_t) -> bool:
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
    def __getitem__(self, i: int) -> direntry_t:
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
    def __iter__(self) -> Iterator[direntry_t]:
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
    def __ne__(self, r: direntry_vec_t) -> bool:
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
    def __setitem__(self, i: int, v: direntry_t) -> None:
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
    def add_unique(self, x: direntry_t) -> bool:
        ...
    def append(self, x: direntry_t) -> None:
        ...
    def at(self, _idx: int) -> direntry_t:
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
    def extend(self, x: direntry_vec_t) -> None:
        ...
    def extract(self) -> direntry_t:
        ...
    def find(self, *args: Any) -> qvector:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def has(self, x: direntry_t) -> bool:
        ...
    def inject(self, s: direntry_t, len: int) -> None:
        ...
    def insert(self, it: direntry_t, x: direntry_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> direntry_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: direntry_vec_t) -> None:
        ...
    def truncate(self) -> None:
        ...

class dirspec_t:
    DSF_INODE_EA: int  # 1
    DSF_ORDERABLE: int  # 4
    DSF_PRIVRANGE: int  # 2
    DSF_UNQ_NAMES: int  # 8
    @property
    def dsf_flags(self) -> int: ...
    @property
    def id(self) -> str: ...
    @property
    def nodename(self) -> Any: ...
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
    def __init__(self, nm: str = None, f: int = 0) -> Any:
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
    def get_attrs(self, inode: inode_t) -> str:
        ...
    def get_inode(self, dirpath: str, name: str) -> inode_t:
        r"""get the entry inode in the specified directory 
                
        :param dirpath: the absolute directory path with trailing slash
        :param name: the entry name in the directory
        :returns: the entry inode
        """
        ...
    def get_name(self, inode: inode_t, name_flags: int = 0) -> bool:
        r"""get the entry name. for example, the structure name 
                
        :param inode: inode number of the entry
        :param name_flags: how exactly the name should be retrieved. combination of bits for get_...name() methods bits
        :returns: false if the entry does not exist.
        """
        ...
    def has_inode_ea(self) -> bool:
        ...
    def is_orderable(self) -> bool:
        ...
    def rename_inode(self, inode: inode_t, newname: str) -> bool:
        r"""rename the entry 
                
        :returns: success
        """
        ...
    def unique_names(self) -> bool:
        ...
    def unlink_inode(self, inode: inode_t) -> None:
        r"""event: unlinked an inode 
                
        """
        ...

class dirtree_bulk_result_t:
    @property
    def entry(self) -> direntry_t: ...
    @property
    def err(self) -> int: ...
    @property
    def idx(self) -> int: ...
    @property
    def parent(self) -> diridx_t: ...
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

class dirtree_bulk_results_t:
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
    def __getitem__(self, i: int) -> dirtree_bulk_result_t:
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
    def __iter__(self) -> Iterator[dirtree_bulk_result_t]:
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
    def __setitem__(self, i: int, v: dirtree_bulk_result_t) -> None:
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
    def append(self, x: dirtree_bulk_result_t) -> None:
        ...
    def at(self, _idx: int) -> dirtree_bulk_result_t:
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
    def extend(self, x: dirtree_bulk_results_t) -> None:
        ...
    def extract(self) -> dirtree_bulk_result_t:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def inject(self, s: dirtree_bulk_result_t, len: int) -> None:
        ...
    def insert(self, it: dirtree_bulk_result_t, x: dirtree_bulk_result_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> dirtree_bulk_result_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: dirtree_bulk_results_t) -> None:
        ...
    def truncate(self) -> None:
        ...

class dirtree_cursor_t:
    @property
    def parent(self) -> diridx_t: ...
    @property
    def rank(self) -> int: ...
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: dirtree_cursor_t) -> bool:
        ...
    def __format__(self, format_spec: Any) -> str:
        r"""Default object formatter.
        
        Return str(self) if format_spec is empty. Raise TypeError otherwise.
        """
        ...
    def __ge__(self, r: dirtree_cursor_t) -> bool:
        ...
    def __getattribute__(self, name: Any) -> Any:
        r"""Return getattr(self, name)."""
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, r: dirtree_cursor_t) -> bool:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __le__(self, r: dirtree_cursor_t) -> bool:
        ...
    def __lt__(self, r: dirtree_cursor_t) -> bool:
        ...
    def __ne__(self, r: dirtree_cursor_t) -> bool:
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
    def compare(self, r: dirtree_cursor_t) -> int:
        ...
    def is_root_cursor(self) -> bool:
        ...
    def root_cursor(self) -> dirtree_cursor_t:
        ...
    def set_root_cursor(self) -> None:
        ...
    def swap(self, r: dirtree_cursor_t) -> None:
        ...
    def valid(self) -> bool:
        ...

class dirtree_cursor_vec_t:
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: dirtree_cursor_vec_t) -> bool:
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
    def __getitem__(self, i: int) -> dirtree_cursor_t:
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
    def __iter__(self) -> Iterator[dirtree_cursor_t]:
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
    def __ne__(self, r: dirtree_cursor_vec_t) -> bool:
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
    def __setitem__(self, i: int, v: dirtree_cursor_t) -> None:
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
    def add_unique(self, x: dirtree_cursor_t) -> bool:
        ...
    def append(self, x: dirtree_cursor_t) -> None:
        ...
    def at(self, _idx: int) -> dirtree_cursor_t:
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
    def extend(self, x: dirtree_cursor_vec_t) -> None:
        ...
    def extract(self) -> dirtree_cursor_t:
        ...
    def find(self, *args: Any) -> qvector:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def has(self, x: dirtree_cursor_t) -> bool:
        ...
    def inject(self, s: dirtree_cursor_t, len: int) -> None:
        ...
    def insert(self, it: dirtree_cursor_t, x: dirtree_cursor_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> dirtree_cursor_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: dirtree_cursor_vec_t) -> None:
        ...
    def truncate(self) -> None:
        ...

class dirtree_iterator_t:
    @property
    def cursor(self) -> dirtree_cursor_t: ...
    @property
    def pattern(self) -> str: ...
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

class dirtree_selection_t(dirtree_cursor_vec_t):
    def __delattr__(self, name: Any) -> Any:
        r"""Implement delattr(self, name)."""
        ...
    def __dir__(self) -> Any:
        r"""Default dir() implementation."""
        ...
    def __eq__(self, r: dirtree_cursor_vec_t) -> bool:
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
    def __getitem__(self, i: int) -> dirtree_cursor_t:
        ...
    def __getstate__(self) -> Any:
        r"""Helper for pickle."""
        ...
    def __gt__(self, value: Any) -> bool:
        r"""Return self>value."""
        ...
    def __init__(self) -> Any:
        ...
    def __init_subclass__(self) -> Any:
        r"""This method is called when a class is subclassed.
        
        The default implementation does nothing. It may be
        overridden to extend subclasses.
        
        """
        ...
    def __iter__(self) -> Iterator[dirtree_cursor_t]:
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
    def __ne__(self, r: dirtree_cursor_vec_t) -> bool:
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
    def __setitem__(self, i: int, v: dirtree_cursor_t) -> None:
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
    def add_unique(self, x: dirtree_cursor_t) -> bool:
        ...
    def append(self, x: dirtree_cursor_t) -> None:
        ...
    def at(self, _idx: int) -> dirtree_cursor_t:
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
    def extend(self, x: dirtree_cursor_vec_t) -> None:
        ...
    def extract(self) -> dirtree_cursor_t:
        ...
    def find(self, *args: Any) -> qvector:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def has(self, x: dirtree_cursor_t) -> bool:
        ...
    def inject(self, s: dirtree_cursor_t, len: int) -> None:
        ...
    def insert(self, it: dirtree_cursor_t, x: dirtree_cursor_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> dirtree_cursor_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: dirtree_cursor_vec_t) -> None:
        ...
    def truncate(self) -> None:
        ...

class dirtree_t:
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
    def __init__(self, ds: dirspec_t) -> Any:
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
    def bulk_move(self, items: dirtree_cursor_vec_t, dstdir: str, dst_rank: int = -1, moved_items: dirtree_cursor_vec_t = None, errs: dirtree_bulk_results_t = None) -> int:
        r"""Move many items to a directory 
                
        :param items: items to move
        :param dstdir: destination directory. will be created if does not exist.
        :param dst_rank: rank inside the destination directory, where the items should be moved to. example: 0 means to insert to the very beginning of the directory. -1 means to append files to the end of the directory and insert directories after the first existing directory. if the rank is different from -1 and the destination directory has natural ordering and some moved items are files, then the natural ordering will be disabled.
        :param moved_items: buffer for cursors of the successfully moved items
        :param errs: buffer for errors. only errors are reported here, in any order
        :returns: dterr_t error code
        """
        ...
    def bulk_remove(self, items: dirtree_cursor_vec_t, errs: dirtree_bulk_results_t = None) -> int:
        r"""Delete many items 
                
        :param items: items to delete
        :param errs: buffer for errors. only errors are reported here, in any order Directories are deleted recursively, even if they are not empty.
        """
        ...
    def change_rank(self, path: str, rank_delta: int) -> int:
        r"""Change ordering rank of an item. 
                
        :param path: path to the item
        :param rank_delta: the amount of the change. positive numbers mean to move down in the list; negative numbers mean to move up.
        :returns: dterr_t error code
        """
        ...
    def chdir(self, path: str) -> int:
        r"""Change current directory 
                
        :param path: new current directory
        :returns: dterr_t error code
        """
        ...
    def errstr(self, err: int) -> str:
        r"""Get textual representation of the error code.
        
        """
        ...
    def find_entry(self, de: direntry_t) -> dirtree_cursor_t:
        r"""Find the cursor corresponding to an entry of a directory 
                
        :param de: directory entry
        :returns: cursor corresponding to the directory entry
        """
        ...
    def findfirst(self, ff: dirtree_iterator_t, pattern: str) -> bool:
        r"""Start iterating over files in a directory 
                
        :param ff: directory iterator. it will be initialized by the function
        :param pattern: pattern to search for
        :returns: success
        """
        ...
    def findnext(self, ff: dirtree_iterator_t) -> bool:
        r"""Continue iterating over files in a directory 
                
        :param ff: directory iterator
        :returns: success
        """
        ...
    @overload
    def get_abspath(self, cursor: dirtree_cursor_t, name_flags: int = ...) -> str:
        r"""Get absolute path pointed by the cursor 
                
        :returns: path; empty string if error
        """
        ...
    @overload
    def get_abspath(self, relpath: str) -> str:
        r"""Construct an absolute path from the specified relative path. This function verifies the directory part of the specified path. The last component of the specified path is not verified. 
                
        :returns: path. empty path means wrong directory part of RELPATH
        """
        ...
    def get_dir_size(self, diridx: diridx_t) -> int:
        r"""Get dir size 
                
        :param diridx: directory index
        :returns: number of entries under this directory; if error, return -1
        """
        ...
    def get_entry_attrs(self, de: direntry_t) -> str:
        r"""Get entry attributes 
                
        :param de: directory entry
        :returns: name
        """
        ...
    def get_entry_name(self, de: direntry_t, name_flags: int = 0) -> str:
        r"""Get entry name 
                
        :param de: directory entry
        :param name_flags: how exactly the name should be retrieved. combination of bits for get_...name() methods bits
        :returns: name
        """
        ...
    def get_id(self) -> str:
        r"""netnode name
        
        """
        ...
    def get_nodename(self) -> str:
        r"""netnode name
        
        """
        ...
    def get_parent_cursor(self, cursor: dirtree_cursor_t) -> dirtree_cursor_t:
        r"""Get parent cursor. 
                
        :param cursor: a valid ditree cursor
        :returns: cursor's parent
        """
        ...
    def get_rank(self, diridx: diridx_t, de: direntry_t) -> int:
        r"""Get ordering rank of an item. 
                
        :param diridx: index of the parent directory
        :param de: directory entry
        :returns: number in a range of [0..n) where n is the number of entries in the parent directory. -1 if error
        """
        ...
    def getcwd(self) -> str:
        r"""Get current directory 
                
        :returns: the current working directory
        """
        ...
    def is_dir_ordered(self, diridx: diridx_t) -> bool:
        r"""Is dir ordered? 
                
        :returns: true if the dirtree has natural ordering
        """
        ...
    def is_orderable(self) -> bool:
        r"""Is dirtree orderable? 
                
        :returns: true if the dirtree is orderable
        """
        ...
    @overload
    def isdir(self, path: str) -> bool:
        r"""Is a directory? 
                
        :returns: true if the specified path is a directory
        """
        ...
    @overload
    def isdir(self, de: direntry_t) -> bool: ...
    @overload
    def isfile(self, path: str) -> bool:
        r"""Is a file? 
                
        :returns: true if the specified path is a file
        """
        ...
    @overload
    def isfile(self, de: direntry_t) -> bool: ...
    @overload
    def link(self, path: str) -> int:
        r"""Add a file item into a directory. 
                
        :returns: dterr_t error code
        """
        ...
    @overload
    def link(self, inode: inode_t) -> int:
        r"""Add an inode into the current directory 
                
        :returns: dterr_t error code
        """
        ...
    def load(self) -> bool:
        r"""Load the tree structure from the netnode. If dirspec_t::id is empty, the operation will be considered a success. In addition, calling load() more than once will not do anything, and will be considered a success. 
                
        :returns: success
        """
        ...
    def make_cursor(self, path: str) -> dirtree_cursor_t:
        r"""Make cursor from path 
                
        :param path: to analyze
        :returns: directory cursor; if the path is bad, the resolved cursor will be invalid.
        """
        ...
    def mkdir(self, path: str) -> int:
        r"""Create a directory. 
                
        :param path: directory to create
        :returns: dterr_t error code
        """
        ...
    def notify_dirtree(self, added: bool, inode: inode_t) -> None:
        r"""Notify dirtree about a change of an inode. 
                
        :param added: are we adding or deleting an inode?
        :param inode: inode in question
        """
        ...
    def rename(self, _from: str, to: str) -> int:
        r"""Rename a directory entry 
                
        :param to: destination path
        :returns: dterr_t error code
        """
        ...
    def resolve_cursor(self, cursor: dirtree_cursor_t) -> direntry_t:
        r"""Resolve cursor 
                
        :param cursor: to analyze
        :returns: directory entry; if the cursor is bad, the resolved entry will be invalid.
        """
        ...
    def resolve_path(self, path: str) -> direntry_t:
        r"""Resolve path 
                
        :param path: to analyze
        :returns: directory entry
        """
        ...
    def rmdir(self, path: str) -> int:
        r"""Remove a directory. 
                
        :param path: directory to delete
        :returns: dterr_t error code
        """
        ...
    def save(self) -> bool:
        r"""Save the tree structure to the netnode. 
                
        :returns: success
        """
        ...
    def set_id(self, nm: str) -> None:
        ...
    def set_natural_order(self, diridx: diridx_t, enable: bool) -> int:
        r"""Enable/disable natural inode order in a directory. 
                
        :param diridx: directory index
        :param enable: action to do TRUE - enable ordering: re-order existing entries so that all subdirs are at the beginning of the list, file entries are sorted and placed after the subdirs FALSE - disable ordering, no changes to existing entries
        :returns: dterr_t error code
        """
        ...
    def set_nodename(self, nm: str) -> None:
        ...
    def traverse(self, v: dirtree_visitor_t) -> int:
        r"""Traverse dirtree, and be notified at each entry If the the visitor returns anything other than 0, iteration will stop, and that value returned. The tree is traversed using a depth-first algorithm. It is forbidden to modify the dirtree_t during traversal; doing so will result in undefined behavior. 
                
        :param v: the callback
        :returns: 0, or whatever the visitor returned
        """
        ...
    @overload
    def unlink(self, path: str) -> int:
        r"""Remove a file item from a directory. 
                
        :returns: dterr_t error code
        """
        ...
    @overload
    def unlink(self, inode: inode_t) -> int:
        r"""Remove an inode from the current directory 
                
        :returns: dterr_t error code
        """
        ...

class dirtree_visitor_t:
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
    def visit(self, c: dirtree_cursor_t, de: direntry_t) -> int:
        r"""Will be called for each entry in the dirtree_t If something other than 0 is returned, iteration will stop. 
                
        :param c: the current cursor
        :param de: the current entry
        :returns: 0 to keep iterating, or anything else to stop
        """
        ...

def get_std_dirtree(id: dirtree_id_t) -> dirtree_t:
    ...

DIRTREE_BPTS: int  # 5
DIRTREE_END: int  # 7
DIRTREE_FUNCS: int  # 1
DIRTREE_IDAPLACE_BOOKMARKS: int  # 4
DIRTREE_IMPORTS: int  # 3
DIRTREE_LOCAL_TYPES: int  # 0
DIRTREE_LTYPES_BOOKMARKS: int  # 6
DIRTREE_NAMES: int  # 2
DTE_ALREADY_EXISTS: int  # 1
DTE_BAD_PATH: int  # 5
DTE_CANT_RENAME: int  # 6
DTE_LAST: int  # 10
DTE_MAX_DIR: int  # 8
DTE_NOT_DIRECTORY: int  # 3
DTE_NOT_EMPTY: int  # 4
DTE_NOT_FOUND: int  # 2
DTE_NOT_ORDERABLE: int  # 9
DTE_OK: int  # 0
DTE_OWN_CHILD: int  # 7
DTN_DISPLAY_NAME: int  # 1
DTN_FULL_NAME: int  # 0
SWIG_PYTHON_LEGACY_BOOL: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
ida_idaapi: module
weakref: module