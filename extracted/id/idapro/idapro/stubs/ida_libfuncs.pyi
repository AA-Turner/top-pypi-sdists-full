from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

class idasgn_header_t:
    @property
    def apptype(self) -> int: ...
    @apptype.setter
    def apptype(self, value: int) -> None: ...
    @property
    def ctype_crc(self) -> int: ...
    @ctype_crc.setter
    def ctype_crc(self, value: int) -> None: ...
    @property
    def ctype_crc_3v(self) -> int: ...
    @ctype_crc_3v.setter
    def ctype_crc_3v(self, value: int) -> None: ...
    @property
    def ctype_crc_alt(self) -> int: ...
    @ctype_crc_alt.setter
    def ctype_crc_alt(self, value: int) -> None: ...
    @property
    def ctype_name(self) -> Any: ...
    @ctype_name.setter
    def ctype_name(self, value: Any) -> None: ...
    @property
    def file_formats(self) -> int: ...
    @file_formats.setter
    def file_formats(self, value: int) -> None: ...
    @property
    def flags(self) -> int: ...
    @flags.setter
    def flags(self, value: int) -> None: ...
    @property
    def libname_length(self) -> int: ...
    @libname_length.setter
    def libname_length(self, value: int) -> None: ...
    @property
    def magic(self) -> Any: ...
    @magic.setter
    def magic(self, value: Any) -> None: ...
    @property
    def number_of_modules(self) -> int: ...
    @number_of_modules.setter
    def number_of_modules(self, value: int) -> None: ...
    @property
    def number_of_modules_v5(self) -> int: ...
    @number_of_modules_v5.setter
    def number_of_modules_v5(self, value: int) -> None: ...
    @property
    def ostype(self) -> int: ...
    @ostype.setter
    def ostype(self, value: int) -> None: ...
    @property
    def pattern_length(self) -> int: ...
    @pattern_length.setter
    def pattern_length(self, value: int) -> None: ...
    @property
    def processor_id(self) -> int: ...
    @processor_id.setter
    def processor_id(self, value: int) -> None: ...
    @property
    def version(self) -> int: ...
    @version.setter
    def version(self, value: int) -> None: ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...

def get_idasgn_header_by_short_name(out_header: idasgn_header_t, name: str) -> Union[str, None]:
    r"""Get idasgn header by a short signature name. 
            
    :param out_header: buffer for the signature file header
    :param name: short name of a signature
    :returns: true in case of success
    """
    ...

def get_idasgn_path_by_short_name(name: str) -> Union[str, None]:
    r"""Get idasgn full path by a short signature name. 
            
    :param name: short name of a signature
    :returns: true in case of success
    """
    ...

APPT_16BIT: int  # 128
APPT_1THREAD: int  # 32
APPT_32BIT: int  # 256
APPT_64BIT: int  # 512
APPT_CONSOLE: int  # 1
APPT_DRIVER: int  # 16
APPT_GRAPHIC: int  # 2
APPT_LIBRARY: int  # 8
APPT_MTHREAD: int  # 64
APPT_PROGRAM: int  # 4
FLIRT_TC_GLIBC: int  # 3
FLIRT_TC_MINGW: int  # 2
FLIRT_TC_MSVC: int  # 1
FLIRT_TC_NONE: int  # 0
FLIRT_TC_USER: int  # 128
LS_CTYPE: int  # 2
LS_CTYPE2: int  # 4
LS_CTYPE_3V: int  # 32
LS_CTYPE_ALT: int  # 8
LS_STARTUP: int  # 1
LS_ZIP: int  # 16
LS_ZSTD: int  # 64
OSTYPE_MSDOS: int  # 1
OSTYPE_NETW: int  # 8
OSTYPE_OS2: int  # 4
OSTYPE_OTHER: int  # 32
OSTYPE_UNIX: int  # 16
OSTYPE_WIN: int  # 2
SIGN_HEADER_MAGIC: str  # IDASGN
SIGN_HEADER_VERSION: int  # 10
SWIG_PYTHON_LEGACY_BOOL: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
ida_idaapi: module
weakref: module