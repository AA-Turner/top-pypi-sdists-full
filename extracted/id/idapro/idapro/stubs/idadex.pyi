from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

class Dex:
    ACCESS_FLAGS: dict
    DEBINFO_LINEINFO: int  # 1
    DEXCMN_DEBINFO: int  # 68
    DEXCMN_DEBSTR: int  # 66
    DEXCMN_METHOD_ID: int  # 77
    DEXCMN_STRING_ID: int  # 83
    DEXCMN_TRY_IDS: int  # 89
    DEXCMN_TRY_TYPES: int  # 69
    DEXVAR_CLASS_TIDS: int  # 75
    DEXVAR_FIELD: int  # 70
    DEXVAR_METHOD: int  # 77
    DEXVAR_METH_STR: int  # 78
    DEXVAR_METH_STRO: int  # 79
    DEXVAR_OLD_STRIDS: int  # 83
    DEXVAR_OLD_TYPIDS: int  # 84
    DEXVAR_OLD_TYPRENS: int  # 118
    DEXVAR_OLD_TYPSTR: int  # 85
    DEXVAR_OLD_TYPSTRO: int  # 86
    DEXVAR_STRING_EAS: int  # 115
    DEXVAR_TRYLIST: int  # 89
    HASHVAL_DEXVERSION: str  # dex_version
    HASHVAL_MAGIC: str  # version
    HASHVAL_OPTIMIZED: str  # optimized
    META_BASEADDRS: int  # 1
    META_XTRNADDRS: int  # 2
    PRIMITVE_TYPES: dict
    def __init__(self) -> Any:
        ...
    @staticmethod
    def access_string(flags: Any) -> Any:
        ...
    @staticmethod
    def as_string(s: Any) -> Any:
        ...
    @staticmethod
    def decorate_java_typename(desc: Any) -> Any:
        ...
    def get_call_method_name(self, method: Any) -> Any:
        ...
    def get_dexnum(self, from_ea: Any) -> Any:
        ...
    def get_field(self, from_ea: Any, field_idx: Any) -> Any:
        ...
    def get_field_name(self, from_ea: Any, field_idx: Any) -> Any:
        ...
    def get_full_field_name(self, field_idx: Any, field: Any, field_name: Any) -> Any:
        ...
    def get_full_method_name(self, method: Any) -> Any:
        ...
    @staticmethod
    def get_full_type_name(longname: Any) -> Any:
        ...
    def get_method(self, from_ea: Any, method_idx: Any) -> Any:
        ...
    def get_method_idx(self, ea: Any) -> Any:
        ...
    def get_method_name(self, from_ea: Any, method_idx: Any) -> Any:
        ...
    def get_nn_var(self, from_ea: Any) -> Any:
        ...
    def get_parameter_name(self, from_ea: Any, idx: Any) -> Any:
        ...
    def get_short_field_name(self, field_idx: Any, field: Any, field_name: Any) -> Any:
        ...
    def get_short_method_name(self, method: Any) -> Any:
        ...
    @staticmethod
    def get_short_type_name(longname: Any) -> Any:
        ...
    def get_string(self, from_ea: Any, string_idx: Any) -> Any:
        ...
    @staticmethod
    def get_string_by_index(node: Any, idx: Any, tag: Any) -> Any:
        ...
    def get_string_ea(self, from_ea: Any, string_idx: Any) -> Any:
        ...
    def get_type_string(self, from_ea: Any, type_idx: Any) -> Any:
        ...
    @staticmethod
    def is_wide_type(typechar: Any) -> Any:
        ...

class char:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class dex_field:
    IS_LOCAL: int  # 1
    access_flags: CField  # <Field type=c_ulong, ofs=24, size=4>
    ctype: CField  # <Field type=c_ulong, ofs=0, size=4>
    flags: CField  # <Field type=c_ulong, ofs=40, size=4>
    maddr: CField  # <Field type=c_ulonglong, ofs=16, size=8>
    name: CField  # <Field type=c_ulong, ofs=4, size=4>
    reserved: CField  # <Field type=c_ulong, ofs=44, size=4>
    saddr: CField  # <Field type=c_ulonglong, ofs=32, size=8>
    type: CField  # <Field type=c_ulong, ofs=8, size=4>
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def is_local(self) -> Any:
        ...

class dex_field_t:
    IS_LOCAL: int  # 1
    access_flags: CField  # <Field type=c_ulong, ofs=24, size=4>
    ctype: CField  # <Field type=c_ulong, ofs=0, size=4>
    flags: CField  # <Field type=c_ulong, ofs=40, size=4>
    maddr: CField  # <Field type=c_ulonglong, ofs=16, size=8>
    name: CField  # <Field type=c_ulong, ofs=4, size=4>
    reserved: CField  # <Field type=c_ulong, ofs=44, size=4>
    saddr: CField  # <Field type=c_ulonglong, ofs=32, size=8>
    type: CField  # <Field type=c_ulong, ofs=8, size=4>
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def is_local(self) -> Any:
        ...

class dex_method:
    HAS_CODE: int  # 2
    IS_LINKED: int  # 4
    IS_LOCAL: int  # 1
    MAX_PROTO_PARAMS: int  # 32
    NO_PROTO: int  # 8
    PACK_V1: int  # 128
    def __init__(self) -> Any:
        ...
    def callable_ea(self) -> Any:
        r"""the address that stands for this method: its code when we know
        it, else its IMPORTS entry
        """
        ...
    def has_code(self) -> Any:
        ...
    def has_proto(self) -> Any:
        r"""do nparams and proto_params describe the prototype? when they do
        not, the shorty still gives the parameter count and the rough
        kinds; only the type ids are out of reach
        """
        ...
    def is_linked(self) -> Any:
        r"""the body is declared elsewhere -- by a superclass, by another file
        of the multidex set, or both -- and startAddr names it there
        """
        ...
    def is_local(self) -> Any:
        ...
    def owns_body(self) -> Any:
        r"""does this record own the body it names, rather than point at one
        declared elsewhere? enumerating the bodies of a file means keeping
        only these: a linked reference carries its definition's address,
        so counting it too would list the same function once per file
        that refers to it
        """
        ...
    @staticmethod
    def unpack(buf: Any) -> Any:
        r"""parse a DEXVAR_METHOD record, in either of the two forms.
        returns None if buf is neither
        """
        ...

class dex_method_t:
    HAS_CODE: int  # 2
    IS_LINKED: int  # 4
    IS_LOCAL: int  # 1
    MAX_PROTO_PARAMS: int  # 32
    NO_PROTO: int  # 8
    PACK_V1: int  # 128
    def __init__(self) -> Any:
        ...
    def callable_ea(self) -> Any:
        r"""the address that stands for this method: its code when we know
        it, else its IMPORTS entry
        """
        ...
    def has_code(self) -> Any:
        ...
    def has_proto(self) -> Any:
        r"""do nparams and proto_params describe the prototype? when they do
        not, the shorty still gives the parameter count and the rough
        kinds; only the type ids are out of reach
        """
        ...
    def is_linked(self) -> Any:
        r"""the body is declared elsewhere -- by a superclass, by another file
        of the multidex set, or both -- and startAddr names it there
        """
        ...
    def is_local(self) -> Any:
        ...
    def owns_body(self) -> Any:
        r"""does this record own the body it names, rather than point at one
        declared elsewhere? enumerating the bodies of a file means keeping
        only these: a linked reference carries its definition's address,
        so counting it too would list the same function once per file
        that refers to it
        """
        ...
    @staticmethod
    def unpack(buf: Any) -> Any:
        r"""parse a DEXVAR_METHOD record, in either of the two forms.
        returns None if buf is neither
        """
        ...

class dex_method_v11:
    access_flags: CField  # <Field type=c_ulong, ofs=164, size=4>
    catch_handler_data: CField  # <Field type=c_ulonglong, ofs=192, size=8>
    cname: CField  # <Field type=c_ulong, ofs=16, size=4>
    defaddr: CField  # <Field type=c_ulonglong, ofs=8, size=8>
    endAddr: CField  # <Field type=c_ulonglong, ofs=176, size=8>
    flags: CField  # <Field type=c_ulong, ofs=0, size=4>
    id: CField  # <Field type=c_ulong, ofs=20, size=4>
    impaddr: CField  # <Field type=c_ulonglong, ofs=200, size=8>
    nparams: CField  # <Field type=c_ushort, ofs=32, size=2>
    proto_idx: CField  # <Field type=c_ushort, ofs=208, size=2>
    proto_params: CField  # <Field type=c_ulong_Array_32, ofs=36, size=128>
    proto_ret: CField  # <Field type=c_ulong, ofs=24, size=4>
    proto_shorty: CField  # <Field type=c_ulong, ofs=28, size=4>
    reg_out: CField  # <Field type=c_ushort, ofs=188, size=2>
    reg_params: CField  # <Field type=c_ushort, ofs=186, size=2>
    reg_total: CField  # <Field type=c_ushort, ofs=184, size=2>
    startAddr: CField  # <Field type=c_ulonglong, ofs=168, size=8>
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class ea_t:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class longname_director_t:
    node: CField  # <Field type=c_ulonglong, ofs=1, size=8>
    zero: CField  # <Field type=c_ubyte, ofs=0, size=1>
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class uint16:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class uint32:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class uint64:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class uint8:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

class ushort:
    value: getset_descriptor
    def __bool__(self) -> bool:
        r"""True if self else False"""
        ...
    def __buffer__(self, flags: Any) -> Any:
        r"""Return a buffer object that exposes the underlying memory of the object."""
        ...
    def __ctype_be__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctype_le__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __ctypes_from_outparam__(self) -> Any:
        ...
    def __hash__(self) -> int:
        r"""Return hash(self)."""
        ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        r"""Initialize self.  See help(type(self)) for accurate signature."""
        ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        r"""Create and return a new object.  See help(type) for accurate signature."""
        ...
    def __reduce__(self) -> Any:
        ...
    def __repr__(self) -> str:
        r"""Return repr(self)."""
        ...
    def __setstate__(self, *args: Any, **kwargs: Any) -> Any:
        ...

def get_dw(buf: Any, off: Any) -> Any:
    ...

def get_struct(str_: Any, off: Any, struct: Any) -> Any:
    ...

def to_uint32(v: Any) -> Any:
    ...

def unpack_db(buf: Any, off: Any) -> Any:
    ...

def unpack_dd(buf: Any, off: Any) -> Any:
    ...

def unpack_dq(buf: Any, off: Any) -> Any:
    ...

def unpack_dw(buf: Any, off: Any) -> Any:
    ...

def unpack_ea(buf: Any, off: Any) -> Any:
    ...

def unpack_eavec(buf: Any, base_ea: Any) -> Any:
    ...

ctypes: module
ida_bytes: module
ida_idaapi: module
ida_segment: module
ida_typeinf: module
idaapi: module
idc: _module_wrapper_t
print_function: _Feature
sys: module  # <module 'sys' (built-in)>