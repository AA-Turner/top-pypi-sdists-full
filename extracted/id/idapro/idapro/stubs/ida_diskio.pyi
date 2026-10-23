from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""File I/O functions for IDA.

You should not use standard C file I/O functions in modules. Use functions from this header, pro.h and fpro.h instead.
This file also declares a call_system() function.

"""

class choose_ioport_parser_t:
    def __disown__(self) -> Any:
        ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def parse(self, param: str, line: str) -> bool:
        r""":returns: true: and fill PARAM with a displayed string
        :returns: false: and empty PARAM to skip the current device
        :returns: false: and fill PARAM with an error message
        """
        ...

class file_enumerator_t:
    def __disown__(self) -> Any:
        ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def visit_file(self, file: str) -> int:
        ...

class generic_linput_t:
    @property
    def blocksize(self) -> int: ...
    @blocksize.setter
    def blocksize(self, value: int) -> None: ...
    @property
    def filesize(self) -> int: ...
    @filesize.setter
    def filesize(self, value: int) -> None: ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def read(self, off: qoff64_t, buffer: Any, nbytes: int) -> int:
        ...

class ioports_fallback_t:
    def __disown__(self) -> Any:
        ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def handle(self, ports: ioports_t, line: str) -> Union[str, None]:
        r""":param ports: i/o port definitions
        :param line: input line to parse
        :returns: success or fills ERRBUF with an error message
        """
        ...

def choose_ioport_device2(_device: str, file: str, parse_params: choose_ioport_parser_t) -> bool:
    ...

def close_linput(li: linput_t) -> None:
    ...

def create_bytearray_linput(s: str) -> linput_t:
    ...

def create_generic_linput(gl: generic_linput_t) -> linput_t:
    ...

def create_memory_linput(start: ida_idaapi.ea_t, size: int) -> linput_t:
    ...

def enumerate_files(path: Any, fname: Any, callback: Any) -> Any:
    r"""Enumerate files in the specified directory while the callback returns 0.
    
    :param path: directory to enumerate files in
    :param fname: mask of file names to enumerate
    :param callback: a callable object that takes the filename as
                     its first argument and it returns 0 to continue
                     enumeration or non-zero to stop enumeration.
    :returns: tuple(code, fname) : If the callback returns non-zero, or None in case of script errors
    """
    ...

def fopenA(file: str) -> Any:
    ...

def fopenM(file: str) -> Any:
    ...

def fopenRB(file: str) -> Any:
    ...

def fopenRT(file: str) -> Any:
    ...

def fopenWB(file: str) -> Any:
    ...

def fopenWT(file: str) -> Any:
    ...

def get_ida_subdirs(subdir: str, flags: int = 0) -> qstrvec_t:
    r"""Get list of directories in which to find a specific IDA resource (see IDA subdirectories). The order of the resulting list is as follows: 
         [$IDAUSR/subdir (0..N entries)]
         [$IDAUSR/extensions/<pack>/subdir (0..N entries)]
         the directory in $IDASGN, $IDAIDS, $IDAIDC or $IDATIL, for the matching subdir
         $IDADIR/subdir
         [$IDADIR/extensions/<pack>/subdir (0..N entries)]
    
    
            
    :param subdir: name of the resource to list (can be nullptr)
    :param flags: Subdirectory modification flags bits
    :returns: number of directories appended to 'dirs'
    """
    ...

def get_linput_type(li: linput_t) -> linput_type_t:
    ...

def get_special_folder(csidl: int) -> Union[str, None]:
    r"""Get a folder location by CSIDL (see Common CSIDLs). Path should be of at least MAX_PATH size 
            
    """
    ...

def get_user_idadir() -> str:
    r"""Get user ida related directory. 
    if $IDAUSR is defined:
       - the first element in $IDAUSR
    else
       - default user directory ($HOME/.idapro or %APPDATA%Hex-Rays/IDA Pro)
    
    
       
    """
    ...

def getsysfile(filename: str, subdir: str) -> Union[str, None]:
    r"""Search for IDA system file. This function searches for a file in the directories returned by get_ida_subdirs() and returns the first match. For plugins, loaders and processor modules, the file can also be the entry point of an extension installed as a directory with a manifest. Each root is searched in order: first the file in the root, then the entry points of the extensions in the root. The entry point is found by its file name, without regard to case. The other files in the extension directory are not found. 
            
    :param filename: name of file to search
    :param subdir: if specified, the file is looked for in the specified subdirectory of the ida directory first (see IDA subdirectories)
    :returns: nullptr if not found, otherwise a pointer to full file name.
    """
    ...

def idadir(subdir: str) -> str:
    r"""Get IDA directory (if subdir==nullptr) or the specified subdirectory (see IDA subdirectories) 
            
    """
    ...

def open_linput(file: str, remote: bool) -> linput_t:
    ...

def qlgetz(li: linput_t, fpos: int) -> Union[str, None]:
    ...

def read_ioports(ports: ioports_t, device: str, file: str, callback: ioports_fallback_t = None) -> int:
    ...

CFG_SUBDIR: str  # cfg
CSIDL_APPDATA: int  # 26
CSIDL_LOCAL_APPDATA: int  # 28
CSIDL_PERSONAL: int  # 5
CSIDL_PROFILE: int  # 40
CSIDL_PROGRAM_FILES: int  # 38
CSIDL_PROGRAM_FILESX86: int  # 42
CSIDL_PROGRAM_FILES_COMMON: int  # 43
IDA_SUBDIR_IDADIR_FIRST: int  # 2
IDA_SUBDIR_IDP: int  # 1
IDA_SUBDIR_ONLY_EXISTING: int  # 4
IDC_SUBDIR: str  # idc
IDP_SUBDIR: str  # procs
IDS_SUBDIR: str  # ids
LDR_SUBDIR: str  # loaders
LINPUT_GENERIC: int  # 4
LINPUT_LOCAL: int  # 1
LINPUT_NONE: int  # 0
LINPUT_PROCMEM: int  # 3
LINPUT_RFILE: int  # 2
LOC_CLOSE: int  # 0
LOC_KEEP: int  # 2
LOC_UNMAKE: int  # 1
PLG_SUBDIR: str  # plugins
SIG_SUBDIR: str  # sig
SWIG_PYTHON_LEGACY_BOOL: int  # 1
THM_SUBDIR: str  # themes
TIL_SUBDIR: str  # til
VAULT_CACHE_FNAME: str  # .vault_cache
VAULT_CACHE_SUBDIR: str  # .vault
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
ida_idaapi: module
weakref: module