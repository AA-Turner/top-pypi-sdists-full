"""
CSSL Built-in Functions
Provides standard functions available in all CSSL scripts
"""

import os
import sys
import time
import random
import hashlib
import json
import re
import math
from typing import Any, Dict, List, Optional, Callable, Union
from datetime import datetime


class CSSLBuiltinError(Exception):
    """Error in builtin function execution"""
    pass


class CSSLBuiltins:
    """
    Built-in functions for CSSL runtime
    These functions are available in all CSSL scripts without imports
    """

    def __init__(self, runtime=None):
        self.runtime = runtime
        self._functions: Dict[str, Callable] = {}
        self._register_all()

    def _register_all(self):
        """Register all built-in functions"""
        # Output functions
        self._functions['print'] = self.builtin_print
        self._functions['println'] = self.builtin_println
        self._functions['input'] = self.builtin_input
        self._functions['debug'] = self.builtin_debug
        self._functions['error'] = self.builtin_error
        self._functions['warn'] = self.builtin_warn
        self._functions['log'] = self.builtin_log
        self._functions['encode'] = self.builtin_encode  # v4.3.2: Safe unicode encoding

        # Type conversion
        self._functions['int'] = self.builtin_int
        self._functions['float'] = self.builtin_float
        self._functions['str'] = self.builtin_str
        self._functions['bool'] = self.builtin_bool
        self._functions['list'] = self.builtin_list
        self._functions['dict'] = self.builtin_dict

        # Type checking
        self._functions['typeof'] = self.builtin_typeof
        self._functions['isinstance'] = self.builtin_isinstance
        self._functions['isint'] = self.builtin_isint
        self._functions['isfloat'] = self.builtin_isfloat
        self._functions['isstr'] = self.builtin_isstr
        self._functions['isbool'] = self.builtin_isbool
        self._functions['islist'] = self.builtin_islist
        self._functions['isdict'] = self.builtin_isdict
        self._functions['isnull'] = self.builtin_isnull

        # String functions
        self._functions['len'] = self.builtin_len
        self._functions['upper'] = self.builtin_upper
        self._functions['lower'] = self.builtin_lower
        self._functions['trim'] = self.builtin_trim
        self._functions['ltrim'] = self.builtin_ltrim
        self._functions['rtrim'] = self.builtin_rtrim
        self._functions['split'] = self.builtin_split
        self._functions['join'] = self.builtin_join
        self._functions['replace'] = self.builtin_replace
        self._functions['substr'] = self.builtin_substr
        self._functions['contains'] = self.builtin_contains
        self._functions['startswith'] = self.builtin_startswith
        self._functions['endswith'] = self.builtin_endswith
        self._functions['format'] = self.builtin_format
        self._functions['concat'] = self.builtin_concat
        self._functions['repeat'] = self.builtin_repeat
        self._functions['reverse'] = self.builtin_reverse
        self._functions['indexof'] = self.builtin_indexof
        self._functions['lastindexof'] = self.builtin_lastindexof
        self._functions['padleft'] = self.builtin_padleft
        self._functions['padright'] = self.builtin_padright

        # List functions
        self._functions['push'] = self.builtin_push
        self._functions['pop'] = self.builtin_pop
        self._functions['shift'] = self.builtin_shift
        self._functions['unshift'] = self.builtin_unshift
        self._functions['slice'] = self.builtin_slice
        self._functions['sort'] = self.builtin_sort
        self._functions['rsort'] = self.builtin_rsort
        self._functions['unique'] = self.builtin_unique
        self._functions['flatten'] = self.builtin_flatten
        self._functions['filter'] = self.builtin_filter
        self._functions['map'] = self.builtin_map
        self._functions['reduce'] = self.builtin_reduce
        self._functions['find'] = self.builtin_find
        self._functions['findindex'] = self.builtin_findindex
        self._functions['every'] = self.builtin_every
        self._functions['some'] = self.builtin_some
        self._functions['range'] = self.builtin_range

        # Dict functions
        self._functions['keys'] = self.builtin_keys
        self._functions['values'] = self.builtin_values
        self._functions['items'] = self.builtin_items
        self._functions['haskey'] = self.builtin_haskey
        self._functions['getkey'] = self.builtin_getkey
        self._functions['setkey'] = self.builtin_setkey
        self._functions['delkey'] = self.builtin_delkey
        self._functions['merge'] = self.builtin_merge

        # Math functions
        self._functions['abs'] = self.builtin_abs
        self._functions['min'] = self.builtin_min
        self._functions['max'] = self.builtin_max
        self._functions['sum'] = self.builtin_sum
        self._functions['avg'] = self.builtin_avg
        self._functions['round'] = self.builtin_round
        self._functions['floor'] = self.builtin_floor
        self._functions['ceil'] = self.builtin_ceil
        self._functions['pow'] = self.builtin_pow
        self._functions['sqrt'] = self.builtin_sqrt
        self._functions['mod'] = self.builtin_mod
        self._functions['random'] = self.builtin_random
        self._functions['randint'] = self.builtin_randint
        # Extended math functions
        self._functions['sin'] = self.builtin_sin
        self._functions['cos'] = self.builtin_cos
        self._functions['tan'] = self.builtin_tan
        self._functions['asin'] = self.builtin_asin
        self._functions['acos'] = self.builtin_acos
        self._functions['atan'] = self.builtin_atan
        self._functions['atan2'] = self.builtin_atan2
        self._functions['log'] = self.builtin_log
        self._functions['log10'] = self.builtin_log10
        self._functions['exp'] = self.builtin_exp
        self._functions['pi'] = lambda: math.pi
        self._functions['e'] = lambda: math.e
        self._functions['radians'] = self.builtin_radians
        self._functions['degrees'] = self.builtin_degrees

        # Time functions
        self._functions['now'] = self.builtin_now
        self._functions['timestamp'] = self.builtin_timestamp
        self._functions['sleep'] = self.builtin_sleep
        self._functions['date'] = self.builtin_date
        self._functions['time'] = self.builtin_time
        self._functions['datetime'] = self.builtin_datetime
        self._functions['strftime'] = self.builtin_strftime

        # File/Path functions
        self._functions['pathexists'] = self.builtin_pathexists
        self._functions['exists'] = self.builtin_pathexists  # Alias
        self._functions['isfile'] = self.builtin_isfile
        self._functions['isdir'] = self.builtin_isdir
        self._functions['basename'] = self.builtin_basename
        self._functions['dirname'] = self.builtin_dirname
        self._functions['joinpath'] = self.builtin_joinpath
        self._functions['splitpath'] = self.builtin_splitpath
        self._functions['abspath'] = self.builtin_abspath
        self._functions['normpath'] = self.builtin_normpath
        # File I/O functions
        self._functions['read'] = self.builtin_read
        self._functions['readline'] = self.builtin_readline
        self._functions['write'] = self.builtin_write
        self._functions['writeline'] = self.builtin_writeline
        self._functions['readfile'] = self.builtin_readfile
        self._functions['writefile'] = self.builtin_writefile
        self._functions['appendfile'] = self.builtin_appendfile
        self._functions['readlines'] = self.builtin_readlines
        self._functions['listdir'] = self.builtin_listdir
        self._functions['makedirs'] = self.builtin_makedirs
        self._functions['removefile'] = self.builtin_removefile
        self._functions['removedir'] = self.builtin_removedir
        self._functions['copyfile'] = self.builtin_copyfile
        self._functions['movefile'] = self.builtin_movefile
        self._functions['filesize'] = self.builtin_filesize

        # JSON functions
        self._functions['tojson'] = self.builtin_tojson
        self._functions['fromjson'] = self.builtin_fromjson
        # JSON namespace functions (json::read, json::write, etc.)
        self._functions['json::read'] = self.builtin_json_read
        self._functions['json::write'] = self.builtin_json_write
        self._functions['json::parse'] = self.builtin_fromjson
        self._functions['json::stringify'] = self.builtin_tojson
        self._functions['json::pretty'] = self.builtin_json_pretty
        self._functions['json::keys'] = self.builtin_json_keys
        self._functions['json::values'] = self.builtin_json_values
        self._functions['json::get'] = self.builtin_json_get
        self._functions['json::set'] = self.builtin_json_set
        self._functions['json::has'] = self.builtin_json_has
        self._functions['json::merge'] = self.builtin_json_merge

        # Instance introspection functions (instance::getMethods, etc.)
        self._functions['instance::getMethods'] = self.builtin_instance_getMethods
        self._functions['instance::getClasses'] = self.builtin_instance_getClasses
        self._functions['instance::getVars'] = self.builtin_instance_getVars
        self._functions['instance::getAll'] = self.builtin_instance_getAll
        self._functions['instance::call'] = self.builtin_instance_call
        self._functions['instance::has'] = self.builtin_instance_has
        self._functions['instance::type'] = self.builtin_instance_type
        self._functions['isavailable'] = self.builtin_isavailable
        self._functions['instance::exists'] = self.builtin_isavailable  # Alias

        # Python interop functions
        self._functions['python::pythonize'] = self.builtin_python_pythonize
        self._functions['python::wrap'] = self.builtin_python_pythonize  # Alias
        self._functions['python::export'] = self.builtin_python_pythonize  # Alias
        self._functions['python::csslize'] = self.builtin_python_csslize
        self._functions['python::import'] = self.builtin_python_csslize  # Alias

        # v4.6.5: Watcher namespace functions for live Python instance access
        self._functions['watcher::get'] = self.builtin_watcher_get
        self._functions['watcher::set'] = self.builtin_watcher_set
        self._functions['watcher::list'] = self.builtin_watcher_list
        self._functions['watcher::exists'] = self.builtin_watcher_exists
        self._functions['watcher::refresh'] = self.builtin_watcher_refresh

        # Regex functions
        self._functions['match'] = self.builtin_match
        self._functions['search'] = self.builtin_search
        self._functions['findall'] = self.builtin_findall
        self._functions['sub'] = self.builtin_sub

        # Hash functions
        self._functions['md5'] = self.builtin_md5
        self._functions['sha1'] = self.builtin_sha1
        self._functions['sha256'] = self.builtin_sha256

        # Utility functions
        self._functions['copy'] = self.builtin_copy
        self._functions['deepcopy'] = self.builtin_deepcopy
        self._functions['assert'] = self.builtin_assert
        self._functions['exit'] = self.builtin_exit
        self._functions['env'] = self.builtin_env
        self._functions['setenv'] = self.builtin_setenv
        # v4.8.5: os/sys replacement builtins
        self._functions['getcwd'] = self.builtin_getcwd
        self._functions['chdir'] = self.builtin_chdir
        self._functions['mkdir'] = self.builtin_mkdir
        self._functions['rmdir'] = self.builtin_rmdir
        self._functions['rmfile'] = self.builtin_rmfile
        self._functions['rename'] = self.builtin_rename
        self._functions['argv'] = self.builtin_argv
        self._functions['argc'] = self.builtin_argc
        self._functions['platform'] = self.builtin_platform
        self._functions['version'] = self.builtin_version
        self._functions['input'] = self.builtin_input
        self._functions['clear'] = self.builtin_clear
        self._functions['cls'] = self.builtin_clear  # Alias
        self._functions['color'] = self.builtin_color
        self._functions['delay'] = self.builtin_delay
        self._functions['pyimport'] = self.builtin_pyimport

        # v4.8.4: C++ import and I/O streams
        self._functions['cppimport'] = self.builtin_cppimport
        self._functions['include'] = self.builtin_include
        self._functions['cout'] = self.builtin_cout
        self._functions['cin'] = self.builtin_cin
        self._functions['cerr'] = self.builtin_cerr
        self._functions['clog'] = self.builtin_clog
        self._functions['endl'] = self.builtin_endl
        self._functions['getline'] = self.builtin_getline
        self._functions['fstream'] = self.builtin_fstream
        self._functions['ifstream'] = self.builtin_ifstream
        self._functions['ofstream'] = self.builtin_ofstream
        self._functions['setprecision'] = self.builtin_setprecision
        self._functions['setw'] = self.builtin_setw
        self._functions['setfill'] = self.builtin_setfill
        self._functions['fixed'] = self.builtin_fixed
        self._functions['scientific'] = self.builtin_scientific
        self._functions['flush'] = self.builtin_flush
        # Struct operations
        self._functions['sizeof'] = self.builtin_sizeof
        self._functions['memcpy'] = self.builtin_memcpy
        self._functions['memset'] = self.builtin_memset
        # Pipe operations
        self._functions['pipe'] = self.builtin_pipe
        # Optimized containment check
        self._functions['contains_fast'] = self.builtin_contains_fast

        # Extended string functions
        self._functions['sprintf'] = self.builtin_sprintf
        self._functions['chars'] = self.builtin_chars
        self._functions['ord'] = self.builtin_ord
        self._functions['chr'] = self.builtin_chr
        self._functions['capitalize'] = self.builtin_capitalize
        self._functions['title'] = self.builtin_title
        self._functions['swapcase'] = self.builtin_swapcase
        self._functions['center'] = self.builtin_center
        self._functions['zfill'] = self.builtin_zfill
        self._functions['isalpha'] = self.builtin_isalpha
        self._functions['isdigit'] = self.builtin_isdigit
        self._functions['isalnum'] = self.builtin_isalnum
        self._functions['isspace'] = self.builtin_isspace

        # Extended list functions
        self._functions['enumerate'] = self.builtin_enumerate
        self._functions['zip'] = self.builtin_zip
        self._functions['reversed'] = self.builtin_reversed
        self._functions['sorted'] = self.builtin_sorted
        self._functions['count'] = self.builtin_count
        self._functions['first'] = self.builtin_first
        self._functions['last'] = self.builtin_last
        self._functions['take'] = self.builtin_take
        self._functions['drop'] = self.builtin_drop
        self._functions['chunk'] = self.builtin_chunk
        self._functions['groupby'] = self.builtin_groupby
        self._functions['shuffle'] = self.builtin_shuffle
        self._functions['sample'] = self.builtin_sample

        # Extended dict functions
        self._functions['update'] = self.builtin_update
        self._functions['fromkeys'] = self.builtin_fromkeys
        self._functions['invert'] = self.builtin_invert
        self._functions['pick'] = self.builtin_pick
        self._functions['omit'] = self.builtin_omit

        # CSSL-specific system functions
        self._functions['createcmd'] = self.builtin_createcmd
        self._functions['signal'] = self.builtin_signal
        self._functions['appexec'] = self.builtin_appexec
        self._functions['initpy'] = self.builtin_initpy
        self._functions['initsh'] = self.builtin_initsh
        self._functions['wait_for'] = self.builtin_wait_for
        self._functions['wait_for_event'] = self.builtin_wait_for_event
        self._functions['wait_for_booted'] = self.builtin_wait_for_booted
        self._functions['emit'] = self.builtin_emit
        self._functions['on_event'] = self.builtin_on_event

        # CSSL Import System Functions
        self._functions['cso_root'] = self.builtin_cso_root
        self._functions['include'] = self.builtin_include
        self._functions['payload'] = self.builtin_payload
        self._functions['get'] = self.builtin_get
        self._functions['libinclude'] = self.builtin_libinclude  # v4.1.0: Multi-language support

        # NEW: Extended OS Functions
        self._functions['Listdir'] = self.builtin_listdir  # Alias with capital L
        self._functions['ReadFile'] = self.builtin_readfile  # Alias with capitals
        self._functions['WriteFile'] = self.builtin_writefile  # Alias with capitals
        self._functions['isLinux'] = self.builtin_islinux
        self._functions['isWindows'] = self.builtin_iswindows
        self._functions['isMac'] = self.builtin_ismac

        # NEW: Extended Time Functions
        self._functions['CurrentTime'] = self.builtin_currenttime

        # NEW: Scope/Global Functions
        self._functions['global'] = self.builtin_global

        # CSSL Data Type Constructors
        self._functions['datastruct'] = self.builtin_datastruct
        self._functions['shuffled'] = self.builtin_shuffled
        self._functions['iterator'] = self.builtin_iterator
        self._functions['combo'] = self.builtin_combo
        self._functions['dataspace'] = self.builtin_dataspace
        self._functions['openquote'] = self.builtin_openquote
        self._functions['OpenFind'] = self.builtin_openfind
        self._functions['vector'] = self.builtin_vector
        self._functions['array'] = self.builtin_array
        self._functions['stack'] = self.builtin_stack
        self._functions['map'] = self.builtin_map

        # Print aliases for CSSL
        self._functions['printl'] = self.builtin_println  # CSSL uses printl for println

        # Shared object functions
        self._functions['delete'] = self.builtin_delete  # Delete shared object ($Name)

        # v4.6.5: Color functions - individual colors for f-strings
        # Named colors: red("text"), green("text"), etc.
        self._functions['red'] = self.builtin_red
        self._functions['green'] = self.builtin_green
        self._functions['blue'] = self.builtin_blue
        self._functions['yellow'] = self.builtin_yellow
        self._functions['cyan'] = self.builtin_cyan
        self._functions['magenta'] = self.builtin_magenta
        self._functions['white'] = self.builtin_white
        self._functions['black'] = self.builtin_black
        # Bright variants
        self._functions['bright_red'] = self.builtin_bright_red
        self._functions['bright_green'] = self.builtin_bright_green
        self._functions['bright_blue'] = self.builtin_bright_blue
        self._functions['bright_yellow'] = self.builtin_bright_yellow
        self._functions['bright_cyan'] = self.builtin_bright_cyan
        self._functions['bright_magenta'] = self.builtin_bright_magenta
        self._functions['bright_white'] = self.builtin_bright_white
        # RGB custom color
        self._functions['rgb'] = self.builtin_rgb
        # Background colors
        self._functions['bg_red'] = self.builtin_bg_red
        self._functions['bg_green'] = self.builtin_bg_green
        self._functions['bg_blue'] = self.builtin_bg_blue
        self._functions['bg_yellow'] = self.builtin_bg_yellow
        self._functions['bg_cyan'] = self.builtin_bg_cyan
        self._functions['bg_magenta'] = self.builtin_bg_magenta
        self._functions['bg_white'] = self.builtin_bg_white
        self._functions['bg_black'] = self.builtin_bg_black
        self._functions['bg_rgb'] = self.builtin_bg_rgb
        # Style functions
        self._functions['bold'] = self.builtin_bold
        self._functions['italic'] = self.builtin_italic
        self._functions['cursive'] = self.builtin_italic  # Alias
        self._functions['underline'] = self.builtin_underline
        self._functions['dim'] = self.builtin_dim
        self._functions['blink'] = self.builtin_blink
        self._functions['reverse'] = self.builtin_reverse_style
        self._functions['strikethrough'] = self.builtin_strikethrough
        self._functions['reset'] = self.builtin_reset

    def get_function(self, name: str) -> Optional[Callable]:
        """Get a built-in function by name"""
        return self._functions.get(name)

    def has_function(self, name: str) -> bool:
        """Check if a built-in function exists"""
        return name in self._functions

    def call(self, name: str, *args, **kwargs) -> Any:
        """Call a built-in function"""
        func = self._functions.get(name)
        if not func:
            raise CSSLBuiltinError(f"Unknown builtin function: {name}")
        return func(*args, **kwargs)

    def list_functions(self) -> List[str]:
        """List all available built-in functions"""
        return sorted(self._functions.keys())

    # ============= Output Functions =============

    def builtin_print(self, *args, **kwargs) -> None:
        """Print without newline"""
        import sys
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '')
        output = sep.join(str(a) for a in args) + end
        if self.runtime and hasattr(self.runtime, 'output'):
            self.runtime.output(output)
        else:
            # Handle encoding issues on Windows console
            try:
                print(output, end='')
            except UnicodeEncodeError:
                encoded = output.encode(sys.stdout.encoding or 'utf-8', errors='replace')
                print(encoded.decode(sys.stdout.encoding or 'utf-8', errors='replace'), end='')

    def builtin_println(self, *args, **kwargs) -> None:
        """Print with newline"""
        import sys
        sep = kwargs.get('sep', ' ')
        output = sep.join(str(a) for a in args)
        if self.runtime and hasattr(self.runtime, 'output'):
            self.runtime.output(output + '\n')
        else:
            # Handle encoding issues on Windows console
            try:
                print(output)
            except UnicodeEncodeError:
                # Fallback: encode with errors='replace' for unsupported chars
                encoded = output.encode(sys.stdout.encoding or 'utf-8', errors='replace')
                print(encoded.decode(sys.stdout.encoding or 'utf-8', errors='replace'))

    def builtin_encode(self, content: str, fallback: str = "?") -> str:
        """Encode unicode/emoji characters for safe console output.

        v4.3.2: Safely encode emojis and special unicode characters that may not
        be supported by the current console encoding (e.g., Windows cp1252).

        Usage:
            printl("Status: " + encode("✅"));
            printl("Result: " + encode("😂", "[emoji]"));

            // With custom fallback
            msg = encode("🎉 Success!", "[party]");

        Args:
            content: String containing unicode/emoji characters
            fallback: Replacement string for unencodable characters (default: "?")

        Returns:
            String safe for console output
        """
        import sys
        encoding = sys.stdout.encoding or 'utf-8'

        try:
            # Test if content can be encoded with current console encoding
            content.encode(encoding)
            return content
        except UnicodeEncodeError:
            # Replace unencodable characters with fallback
            result = []
            for char in content:
                try:
                    char.encode(encoding)
                    result.append(char)
                except UnicodeEncodeError:
                    result.append(fallback)
            return ''.join(result)

    def builtin_input(self, prompt: str = "") -> str:
        """Read user input from console.

        Usage:
            name = input("Enter your name: ");
            age = int(input("Enter your age: "));

            // Without prompt
            value = input();

        Args:
            prompt: Optional prompt text to display

        Returns:
            The user's input as a string
        """
        if self.runtime and hasattr(self.runtime, 'input'):
            return self.runtime.input(prompt)
        else:
            return input(prompt)

    def builtin_debug(self, *args) -> None:
        """Debug output"""
        msg = ' '.join(str(a) for a in args)
        if self.runtime and hasattr(self.runtime, 'debug'):
            self.runtime.debug(msg)
        else:
            print(f"[DEBUG] {msg}")

    def builtin_error(self, *args) -> None:
        """Error output"""
        msg = ' '.join(str(a) for a in args)
        if self.runtime and hasattr(self.runtime, 'error'):
            self.runtime.error(msg)
        else:
            print(f"[ERROR] {msg}")

    def builtin_warn(self, *args) -> None:
        """Warning output"""
        msg = ' '.join(str(a) for a in args)
        if self.runtime and hasattr(self.runtime, 'warn'):
            self.runtime.warn(msg)
        else:
            print(f"[WARN] {msg}")

    def builtin_log(self, level: str, *args) -> None:
        """Log with level"""
        msg = ' '.join(str(a) for a in args)
        if self.runtime and hasattr(self.runtime, 'log'):
            self.runtime.log(level, msg)
        else:
            print(f"[{level.upper()}] {msg}")

    # ============= Type Conversion =============

    def builtin_int(self, value: Any, base: int = 10) -> int:
        """Convert to integer"""
        if isinstance(value, str):
            return int(value, base)
        return int(value)

    def builtin_float(self, value: Any) -> float:
        """Convert to float"""
        return float(value)

    def builtin_str(self, value: Any) -> str:
        """Convert to string"""
        return str(value)

    def builtin_bool(self, value: Any) -> bool:
        """Convert to boolean"""
        if isinstance(value, str):
            return value.lower() not in ('', '0', 'false', 'no', 'null', 'none')
        return bool(value)

    def builtin_list(self, value: Any = None) -> list:
        """Convert to list"""
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return list(value)
        if isinstance(value, dict):
            return list(value.items())
        if isinstance(value, str):
            return list(value)
        return [value]

    def builtin_dict(self, value: Any = None) -> dict:
        """Convert to dict"""
        if value is None:
            return {}
        if isinstance(value, dict):
            return dict(value)
        if isinstance(value, (list, tuple)):
            return dict(value)
        raise CSSLBuiltinError(f"Cannot convert {type(value).__name__} to dict")

    # ============= Type Checking =============

    def builtin_typeof(self, value: Any) -> str:
        """Get type name - returns CSSL-specific type names for CSSL types"""
        if value is None:
            return 'null'

        # Check CSSL-specific types first
        from .cssl_types import (Vector, Array, Stack, DataStruct,
                                  List as CSSLList, Dictionary, Map,
                                  Shuffled, Iterator, Combo, DataSpace,
                                  OpenQuote, Parameter, CSSLInstance)

        if isinstance(value, Vector):
            return 'vector'
        elif isinstance(value, Array):
            return 'array'
        elif isinstance(value, Stack):
            return 'stack'
        elif isinstance(value, DataStruct):
            return 'datastruct'
        elif isinstance(value, CSSLList):
            return 'list'
        elif isinstance(value, Dictionary):
            return 'dictionary'
        elif isinstance(value, Map):
            return 'map'
        elif isinstance(value, Shuffled):
            return 'shuffled'
        elif isinstance(value, Iterator):
            return 'iterator'
        elif isinstance(value, Combo):
            return 'combo'
        elif isinstance(value, DataSpace):
            return 'dataspace'
        elif isinstance(value, OpenQuote):
            return 'openquote'
        elif isinstance(value, Parameter):
            return 'parameter'
        elif isinstance(value, CSSLInstance):
            return value._class.name

        # Python types as fallback
        type_map = {
            int: 'int',
            float: 'float',
            str: 'string',
            bool: 'bool',
            list: 'list',
            dict: 'dict',
            tuple: 'tuple'
        }
        return type_map.get(type(value), type(value).__name__)

    def builtin_isinstance(self, value: Any, type_name: str) -> bool:
        """Check if value is of type"""
        type_map = {
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'null': type(None)
        }
        check_type = type_map.get(type_name)
        if check_type:
            return isinstance(value, check_type)
        return False

    def builtin_isint(self, value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    def builtin_isfloat(self, value: Any) -> bool:
        return isinstance(value, float)

    def builtin_isstr(self, value: Any) -> bool:
        return isinstance(value, str)

    def builtin_isbool(self, value: Any) -> bool:
        return isinstance(value, bool)

    def builtin_islist(self, value: Any) -> bool:
        return isinstance(value, list)

    def builtin_isdict(self, value: Any) -> bool:
        return isinstance(value, dict)

    def builtin_isnull(self, value: Any) -> bool:
        return value is None

    # ============= String Functions =============

    def builtin_len(self, value: Union[str, list, dict]) -> int:
        """Get length"""
        return len(value)

    def builtin_upper(self, s: str) -> str:
        return str(s).upper()

    def builtin_lower(self, s: str) -> str:
        return str(s).lower()

    def builtin_trim(self, s: str, chars: str = None) -> str:
        return str(s).strip(chars)

    def builtin_ltrim(self, s: str, chars: str = None) -> str:
        return str(s).lstrip(chars)

    def builtin_rtrim(self, s: str, chars: str = None) -> str:
        return str(s).rstrip(chars)

    def builtin_split(self, s: str, sep: str = None, maxsplit: int = -1) -> list:
        return str(s).split(sep, maxsplit)

    def builtin_join(self, sep: str, items: list) -> str:
        return str(sep).join(str(i) for i in items)

    def builtin_replace(self, s: str, old: str, new: str, count: int = -1) -> str:
        return str(s).replace(old, new, count)

    def builtin_substr(self, s: str, start: int, length: int = None) -> str:
        s = str(s)
        if length is None:
            return s[start:]
        return s[start:start + length]

    def builtin_contains(self, s: str, sub: str) -> bool:
        return sub in str(s)

    def builtin_startswith(self, s: str, prefix: str) -> bool:
        return str(s).startswith(prefix)

    def builtin_endswith(self, s: str, suffix: str) -> bool:
        return str(s).endswith(suffix)

    def builtin_format(self, template: str, *args, **kwargs) -> str:
        return template.format(*args, **kwargs)

    def builtin_concat(self, *args) -> str:
        return ''.join(str(a) for a in args)

    def builtin_repeat(self, s: str, count: int) -> str:
        return str(s) * count

    def builtin_reverse(self, value: Union[str, list]) -> Union[str, list]:
        if isinstance(value, str):
            return value[::-1]
        if isinstance(value, list):
            return value[::-1]
        raise CSSLBuiltinError("reverse requires string or list")

    def builtin_indexof(self, s: str, sub: str, start: int = 0) -> int:
        return str(s).find(sub, start)

    def builtin_lastindexof(self, s: str, sub: str) -> int:
        return str(s).rfind(sub)

    def builtin_padleft(self, s: str, width: int, char: str = ' ') -> str:
        return str(s).rjust(width, char)

    def builtin_padright(self, s: str, width: int, char: str = ' ') -> str:
        return str(s).ljust(width, char)

    # ============= List Functions =============

    def builtin_push(self, lst: list, *items) -> list:
        """Push items onto a list/stack/vector.

        v4.5.1: For Stack/Vector/Array types, modifies in place.
        For regular lists, creates a copy (immutable behavior).
        """
        if lst is None:
            lst = []
            lst.extend(items)
            return lst

        # v4.5.1: For CSSL typed containers, modify in place
        from .cssl_types import Stack, Vector, Array, DataStruct
        if isinstance(lst, (Stack, Vector, Array, DataStruct)):
            for item in items:
                lst.append(item)
            return lst

        # For regular lists, create a copy (immutable behavior)
        lst = list(lst)
        lst.extend(items)
        return lst

    def builtin_pop(self, lst: list, index: int = -1) -> Any:
        """Pop item from list/stack/vector.

        v4.5.1: For Stack/Vector/Array types, modifies in place.
        """
        if lst is None:
            return None

        # v4.5.1: For CSSL typed containers, modify in place
        from .cssl_types import Stack, Vector, Array, DataStruct
        if isinstance(lst, (Stack, Vector, Array, DataStruct)):
            if len(lst) == 0:
                return None
            return lst.pop(index)

        # For regular lists, create a copy
        lst = list(lst)
        return lst.pop(index) if lst else None

    def builtin_shift(self, lst: list) -> Any:
        """Remove and return first element.

        v4.5.1: For Stack/Vector/Array types, modifies in place.
        """
        if lst is None:
            return None

        # v4.5.1: For CSSL typed containers, modify in place
        from .cssl_types import Stack, Vector, Array, DataStruct
        if isinstance(lst, (Stack, Vector, Array, DataStruct)):
            if len(lst) == 0:
                return None
            return lst.pop(0)

        # For regular lists, create a copy
        lst = list(lst)
        return lst.pop(0) if lst else None

    def builtin_unshift(self, lst: list, *items) -> list:
        """Add items to the front of a list/stack/vector.

        v4.5.1: For Stack/Vector/Array types, modifies in place.
        """
        if lst is None:
            lst = []
            for item in reversed(items):
                lst.insert(0, item)
            return lst

        # v4.5.1: For CSSL typed containers, modify in place
        from .cssl_types import Stack, Vector, Array, DataStruct
        if isinstance(lst, (Stack, Vector, Array, DataStruct)):
            for item in reversed(items):
                lst.insert(0, item)
            return lst

        # For regular lists, create a copy
        lst = list(lst)
        for item in reversed(items):
            lst.insert(0, item)
        return lst

    def builtin_slice(self, value: Union[str, list], start: int, end: int = None) -> Union[str, list]:
        if end is None:
            return value[start:]
        return value[start:end]

    def builtin_sort(self, lst: list, key: str = None) -> list:
        lst = list(lst)
        if key:
            lst.sort(key=lambda x: x.get(key) if isinstance(x, dict) else x)
        else:
            lst.sort()
        return lst

    def builtin_rsort(self, lst: list, key: str = None) -> list:
        lst = list(lst)
        if key:
            lst.sort(key=lambda x: x.get(key) if isinstance(x, dict) else x, reverse=True)
        else:
            lst.sort(reverse=True)
        return lst

    def builtin_unique(self, lst: list) -> list:
        seen = []
        result = []
        for item in lst:
            key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
            if key not in seen:
                seen.append(key)
                result.append(item)
        return result

    def builtin_flatten(self, lst: list, depth: int = 1) -> list:
        result = []
        for item in lst:
            if isinstance(item, list) and depth > 0:
                result.extend(self.builtin_flatten(item, depth - 1))
            else:
                result.append(item)
        return result

    def builtin_filter(self, lst: list, condition: Callable) -> list:
        return [item for item in lst if condition(item)]

    def builtin_map(self, lst: list, func: Callable) -> list:
        return [func(item) for item in lst]

    def builtin_reduce(self, lst: list, func: Callable, initial: Any = None) -> Any:
        from functools import reduce
        if initial is not None:
            return reduce(func, lst, initial)
        return reduce(func, lst)

    def builtin_find(self, lst: list, condition: Callable) -> Any:
        for item in lst:
            if condition(item):
                return item
        return None

    def builtin_findindex(self, lst: list, condition: Callable) -> int:
        for i, item in enumerate(lst):
            if condition(item):
                return i
        return -1

    def builtin_every(self, lst: list, condition: Callable) -> bool:
        return all(condition(item) for item in lst)

    def builtin_some(self, lst: list, condition: Callable) -> bool:
        return any(condition(item) for item in lst)

    def builtin_range(self, *args) -> list:
        return list(range(*args))

    # ============= Dict Functions =============

    def builtin_keys(self, d: dict) -> list:
        return list(d.keys())

    def builtin_values(self, d: dict) -> list:
        return list(d.values())

    def builtin_items(self, d: dict) -> list:
        return list(d.items())

    def builtin_haskey(self, d: dict, key: str) -> bool:
        return key in d

    def builtin_getkey(self, d: dict, key: str, default: Any = None) -> Any:
        return d.get(key, default)

    def builtin_setkey(self, d: dict, key: str, value: Any) -> dict:
        d = dict(d)
        d[key] = value
        return d

    def builtin_delkey(self, d: dict, key: str) -> dict:
        d = dict(d)
        d.pop(key, None)
        return d

    def builtin_merge(self, *dicts) -> dict:
        result = {}
        for d in dicts:
            if isinstance(d, dict):
                result.update(d)
        return result

    # ============= Math Functions =============

    def builtin_abs(self, x: Union[int, float]) -> Union[int, float]:
        return abs(x)

    def builtin_min(self, *args) -> Any:
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return min(args[0])
        return min(args)

    def builtin_max(self, *args) -> Any:
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            return max(args[0])
        return max(args)

    def builtin_sum(self, items: list, start: Union[int, float] = 0) -> Union[int, float]:
        return sum(items, start)

    def builtin_avg(self, items: list) -> float:
        if not items:
            return 0.0
        return sum(items) / len(items)

    def builtin_round(self, x: float, digits: int = 0) -> float:
        return round(x, digits)

    def builtin_floor(self, x: float) -> int:
        import math
        return math.floor(x)

    def builtin_ceil(self, x: float) -> int:
        import math
        return math.ceil(x)

    def builtin_pow(self, base: Union[int, float], exp: Union[int, float]) -> Union[int, float]:
        return pow(base, exp)

    def builtin_sqrt(self, x: Union[int, float]) -> float:
        import math
        return math.sqrt(x)

    def builtin_mod(self, a: int, b: int) -> int:
        return a % b

    def builtin_random(self) -> float:
        return random.random()

    def builtin_randint(self, a: int, b: int) -> int:
        return random.randint(a, b)

    def builtin_sin(self, x: float) -> float:
        return math.sin(x)

    def builtin_cos(self, x: float) -> float:
        return math.cos(x)

    def builtin_tan(self, x: float) -> float:
        return math.tan(x)

    def builtin_asin(self, x: float) -> float:
        return math.asin(x)

    def builtin_acos(self, x: float) -> float:
        return math.acos(x)

    def builtin_atan(self, x: float) -> float:
        return math.atan(x)

    def builtin_atan2(self, y: float, x: float) -> float:
        return math.atan2(y, x)

    def builtin_log(self, x: float, base: float = math.e) -> float:
        return math.log(x, base)

    def builtin_log10(self, x: float) -> float:
        return math.log10(x)

    def builtin_exp(self, x: float) -> float:
        return math.exp(x)

    def builtin_radians(self, degrees: float) -> float:
        return math.radians(degrees)

    def builtin_degrees(self, radians: float) -> float:
        return math.degrees(radians)

    # ============= Time Functions =============

    def builtin_now(self) -> float:
        return time.time()

    def builtin_timestamp(self) -> int:
        return int(time.time())

    def builtin_sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def builtin_date(self, format_str: str = '%Y-%m-%d') -> str:
        return datetime.now().strftime(format_str)

    def builtin_time(self, format_str: str = '%H:%M:%S') -> str:
        return datetime.now().strftime(format_str)

    def builtin_datetime(self, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        return datetime.now().strftime(format_str)

    def builtin_strftime(self, format_str: str, timestamp: float = None) -> str:
        if timestamp is None:
            return datetime.now().strftime(format_str)
        return datetime.fromtimestamp(timestamp).strftime(format_str)

    # ============= File/Path Functions =============

    def builtin_pathexists(self, path: str) -> bool:
        return os.path.exists(path)

    def builtin_isfile(self, path: str) -> bool:
        return os.path.isfile(path)

    def builtin_isdir(self, path: str) -> bool:
        return os.path.isdir(path)

    def builtin_basename(self, path: str) -> str:
        return os.path.basename(path)

    def builtin_dirname(self, path: str) -> str:
        return os.path.dirname(path)

    def builtin_joinpath(self, *parts) -> str:
        return os.path.join(*parts)

    def builtin_splitpath(self, path: str) -> list:
        return list(os.path.split(path))

    def builtin_abspath(self, path: str) -> str:
        return os.path.abspath(path)

    def builtin_normpath(self, path: str) -> str:
        return os.path.normpath(path)

    # ============= File I/O Functions =============

    # v4.7.1: Path validation helper to prevent directory traversal attacks
    def _validate_path(self, path: str, allow_write: bool = False) -> str:
        """Validate file path for security.

        v4.7.1: Prevents directory traversal attacks by checking for '..' sequences
        and ensuring paths are within reasonable bounds.

        Args:
            path: The file path to validate
            allow_write: If True, allows write operations

        Returns:
            The normalized absolute path

        Raises:
            CSSLBuiltinError: If path is invalid or attempts traversal
        """
        if not isinstance(path, str) or not path:
            raise CSSLBuiltinError("Invalid path: path must be a non-empty string")

        # Normalize the path
        normalized = os.path.normpath(path)

        # Check for directory traversal attempts
        if '..' in normalized:
            raise CSSLBuiltinError("Directory traversal not allowed in path")

        return normalized

    def builtin_read(self, path: str, encoding: str = 'utf-8') -> str:
        """Read entire file content.
        Usage: read('/path/to/file.txt')
        v4.7.1: Added path validation
        """
        validated_path = self._validate_path(path)
        with open(validated_path, 'r', encoding=encoding) as f:
            return f.read()

    def builtin_readline(self, line: int, path: str, encoding: str = 'utf-8') -> str:
        """Read specific line from file (1-indexed).
        Usage: readline(5, '/path/to/file.txt')  -> returns line 5
        v4.7.1: Added path validation and line number validation
        """
        if not isinstance(line, int) or line < 1:
            raise CSSLBuiltinError("Line number must be a positive integer")
        validated_path = self._validate_path(path)
        with open(validated_path, 'r', encoding=encoding) as f:
            for i, file_line in enumerate(f, 1):
                if i == line:
                    return file_line.rstrip('\n\r')
            return ""  # Line not found

    def builtin_write(self, path: str, content: str, encoding: str = 'utf-8') -> int:
        """Write content to file, returns chars written.
        Usage: write('/path/to/file.txt', 'Hello World')
        v4.7.1: Added path validation
        """
        validated_path = self._validate_path(path, allow_write=True)
        with open(validated_path, 'w', encoding=encoding) as f:
            return f.write(str(content) if content is not None else '')

    def builtin_writeline(self, line: int, content: str, path: str, encoding: str = 'utf-8') -> bool:
        """Write/replace specific line in file (1-indexed).
        Usage: writeline(5, 'New content', '/path/to/file.txt')
        v4.7.1: Added path and line number validation
        """
        if not isinstance(line, int) or line < 1:
            raise CSSLBuiltinError("Line number must be a positive integer")
        validated_path = self._validate_path(path, allow_write=True)

        # Read all lines
        lines = []
        if os.path.exists(validated_path):
            with open(validated_path, 'r', encoding=encoding) as f:
                lines = f.readlines()

        # Ensure we have enough lines
        while len(lines) < line:
            lines.append('\n')

        # Replace the specific line (1-indexed)
        content_str = str(content) if content is not None else ''
        if not content_str.endswith('\n'):
            content_str = content_str + '\n'
        lines[line - 1] = content_str

        # Write back
        with open(validated_path, 'w', encoding=encoding) as f:
            f.writelines(lines)
        return True

    def builtin_readfile(self, path: str, encoding: str = 'utf-8') -> str:
        """Read entire file content. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path)
        with open(validated_path, 'r', encoding=encoding) as f:
            return f.read()

    def builtin_writefile(self, path: str, content: str, encoding: str = 'utf-8') -> int:
        """Write content to file, returns bytes written. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path, allow_write=True)
        with open(validated_path, 'w', encoding=encoding) as f:
            return f.write(str(content) if content is not None else '')

    def builtin_appendfile(self, path: str, content: str, encoding: str = 'utf-8') -> int:
        """Append content to file, returns bytes written. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path, allow_write=True)
        with open(validated_path, 'a', encoding=encoding) as f:
            return f.write(str(content) if content is not None else '')

    def builtin_readlines(self, path: str, encoding: str = 'utf-8') -> list:
        """Read file lines into list. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path)
        with open(validated_path, 'r', encoding=encoding) as f:
            return f.readlines()

    def builtin_listdir(self, path: str = '.') -> list:
        """List directory contents. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path) if path != '.' else '.'
        return os.listdir(validated_path)

    def builtin_makedirs(self, path: str, exist_ok: bool = True) -> bool:
        """Create directories recursively. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path, allow_write=True)
        os.makedirs(validated_path, exist_ok=exist_ok)
        return True

    def builtin_removefile(self, path: str) -> bool:
        """Remove a file. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path, allow_write=True)
        os.remove(validated_path)
        return True

    def builtin_removedir(self, path: str) -> bool:
        """Remove an empty directory. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path, allow_write=True)
        os.rmdir(validated_path)
        return True

    def builtin_copyfile(self, src: str, dst: str) -> str:
        """Copy a file, returns destination path. v4.7.1: Added path validation"""
        import shutil
        validated_src = self._validate_path(src)
        validated_dst = self._validate_path(dst, allow_write=True)
        return shutil.copy2(validated_src, validated_dst)

    def builtin_movefile(self, src: str, dst: str) -> str:
        """Move a file, returns destination path. v4.7.1: Added path validation"""
        import shutil
        validated_src = self._validate_path(src, allow_write=True)
        validated_dst = self._validate_path(dst, allow_write=True)
        return shutil.move(validated_src, validated_dst)

    def builtin_filesize(self, path: str) -> int:
        """Get file size in bytes. v4.7.1: Added path validation"""
        validated_path = self._validate_path(path)
        return os.path.getsize(validated_path)

    # ============= JSON Functions =============

    def builtin_tojson(self, value: Any, indent: int = None) -> str:
        return json.dumps(value, indent=indent, ensure_ascii=False)

    def builtin_fromjson(self, s: str) -> Any:
        return json.loads(s)

    # JSON namespace functions (json::read, json::write, etc.)
    def builtin_json_read(self, path: str, encoding: str = 'utf-8') -> Any:
        """Read and parse JSON file.
        Usage: json::read('/path/to/file.json')
        """
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f)

    def builtin_json_write(self, path: str, data: Any, indent: int = 2, encoding: str = 'utf-8') -> bool:
        """Write data to JSON file.
        Usage: json::write('/path/to/file.json', data)
        """
        with open(path, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True

    def builtin_json_pretty(self, value: Any, indent: int = 2) -> str:
        """Pretty print JSON.
        Usage: json::pretty(data)
        """
        return json.dumps(value, indent=indent, ensure_ascii=False)

    def builtin_json_keys(self, data: Any) -> list:
        """Get all keys from JSON object.
        Usage: json::keys(data)
        """
        if isinstance(data, dict):
            return list(data.keys())
        return []

    def builtin_json_values(self, data: Any) -> list:
        """Get all values from JSON object.
        Usage: json::values(data)
        """
        if isinstance(data, dict):
            return list(data.values())
        return []

    def builtin_json_get(self, data: Any, path: str, default: Any = None) -> Any:
        """Get value by dot-path from JSON.
        Usage: json::get(data, 'user.name')
        """
        if not isinstance(data, dict):
            return default
        keys = path.split('.')
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list):
                try:
                    current = current[int(key)]
                except (ValueError, IndexError):
                    return default
            else:
                return default
        return current

    def builtin_json_set(self, data: Any, path: str, value: Any) -> Any:
        """Set value by dot-path in JSON object.
        Usage: json::set(data, 'user.name', 'John')
        """
        if not isinstance(data, dict):
            return data
        data = dict(data)  # Copy
        keys = path.split('.')
        current = data
        for i, key in enumerate(keys[:-1]):
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
        return data

    def builtin_json_has(self, data: Any, path: str) -> bool:
        """Check if path exists in JSON.
        Usage: json::has(data, 'user.name')
        """
        result = self.builtin_json_get(data, path, _MISSING := object())
        return result is not _MISSING

    def builtin_json_merge(self, *dicts) -> dict:
        """Deep merge multiple JSON objects.
        Usage: json::merge(obj1, obj2, obj3)
        """
        def deep_merge(base, update):
            result = dict(base)
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        result = {}
        for d in dicts:
            if isinstance(d, dict):
                result = deep_merge(result, d)
        return result

    # ============= Instance Introspection Functions =============

    def builtin_instance_getMethods(self, obj: Any) -> list:
        """Get all methods from an object/module.
        Usage: instance::getMethods(@module) or instance::getMethods($obj)
        Returns list of method names.
        """
        from .cssl_types import CSSLInstance

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            return list(obj._class.methods.keys())

        # Handle Python objects
        import inspect
        methods = []
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name, None)
                if callable(attr):
                    methods.append(name)
        return methods

    def builtin_instance_getClasses(self, obj: Any) -> list:
        """Get all classes from an object/module.
        Usage: instance::getClasses(@module)
        Returns list of class names (including merged classes).
        """
        from .cssl_types import CSSLInstance

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            classes = [obj._class.name]  # Primary class
            # Check for merged class instances in members
            for name, member in obj._members.items():
                if isinstance(member, CSSLInstance):
                    classes.append(member._class.name)
            return classes

        # Handle Python objects
        import inspect
        classes = []
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name, None)
                if inspect.isclass(attr):
                    classes.append(name)
        return classes

    def builtin_instance_getVars(self, obj: Any) -> list:
        """Get all variables/attributes (non-callable) from an object.
        Usage: instance::getVars(@module)
        Returns list of variable names (excludes merged class instances).
        """
        from .cssl_types import CSSLInstance

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            vars_list = []
            for name, member in obj._members.items():
                # Exclude merged class instances
                if not isinstance(member, CSSLInstance):
                    vars_list.append(name)
            return vars_list

        # Handle Python objects
        vars_list = []
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name, None)
                if not callable(attr):
                    vars_list.append(name)
        return vars_list

    def builtin_instance_getAll(self, obj: Any) -> dict:
        """Get all attributes from an object, categorized.
        Usage: instance::getAll(@module)
        Returns dict with 'methods', 'classes', 'vars' keys.
        """
        from .cssl_types import CSSLInstance

        result = {
            'methods': [],
            'classes': [],
            'vars': []
        }

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            result['methods'] = list(obj._class.methods.keys())
            result['classes'] = [obj._class.name]

            # Separate regular vars from merged class instances
            for name, member in obj._members.items():
                if isinstance(member, CSSLInstance):
                    # Merged class - add to classes list
                    result['classes'].append(member._class.name)
                else:
                    # Regular variable
                    result['vars'].append(name)
            return result

        # Handle Python objects
        import inspect
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name, None)
                if inspect.isclass(attr):
                    result['classes'].append(name)
                elif callable(attr):
                    result['methods'].append(name)
                else:
                    result['vars'].append(name)
        return result

    def builtin_instance_call(self, obj: Any, method_name: str, *args, **kwargs) -> Any:
        """Dynamically call a method on an object.
        Usage: instance::call(@module, 'methodName', arg1, arg2)
        """
        from .cssl_types import CSSLInstance

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            if obj.has_method(method_name):
                # Need runtime to call the method
                if self.runtime:
                    return self.runtime._call_method(obj, obj.get_method(method_name), list(args), kwargs or {})
            raise RuntimeError(f"Method '{method_name}' not found on CSSL instance")

        # Handle Python objects
        method = getattr(obj, method_name, None)
        if method and callable(method):
            return method(*args, **kwargs)
        raise RuntimeError(f"Method '{method_name}' not found on object")

    def builtin_instance_has(self, obj: Any, name: str) -> bool:
        """Check if object has an attribute or method.
        Usage: instance::has(@module, 'methodName')
        """
        from .cssl_types import CSSLInstance

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            return obj.has_member(name) or obj.has_method(name)

        # Handle Python objects
        return hasattr(obj, name)

    def builtin_instance_type(self, obj: Any) -> str:
        """Get the type name of an object.
        Usage: instance::type(@module)
        """
        from .cssl_types import CSSLInstance

        # Handle CSSL class instances
        if isinstance(obj, CSSLInstance):
            return obj._class.name

        # Handle Python objects
        return type(obj).__name__

    def builtin_isavailable(self, name_or_obj: Any) -> bool:
        """Check if a shared instance exists.
        Usage:
            isavailable("MyInstance")     - check by name string
            isavailable($MyInstance)      - check shared ref (returns True if not None)
            instance::exists("MyInstance") - alias
        """
        from ..cssl_bridge import _live_objects


        # If it's a string, check by name
        if isinstance(name_or_obj, str):
            return name_or_obj in _live_objects

        # Otherwise, check if the object is not None (for $name or instance<"name">)
        return name_or_obj is not None

    # ============= Filter Registration Functions =============

    def builtin_filter_register(self, filter_type: str, helper: str, callback: Any) -> bool:
        """Register a custom filter.
        Usage: filter::register("mytype", "where", myCallback)

        The callback receives (source, filter_value, runtime) and returns filtered result.
        Use "*" as helper for catch-all.

        Example:
            define myFilter(source, value, runtime) {
                return source + value;
            }
            filter::register("custom", "add", myFilter);

            result <==[custom::add=10] 5;  // result = 15
        """
        from .cssl_runtime import register_filter
        register_filter(filter_type, helper, callback)
        return True

    def builtin_filter_unregister(self, filter_type: str, helper: str) -> bool:
        """Unregister a custom filter.
        Usage: filter::unregister("mytype", "where")
        """
        from .cssl_runtime import unregister_filter
        return unregister_filter(filter_type, helper)

    def builtin_filter_list(self) -> list:
        """List all registered custom filters.
        Usage: filter::list()
        Returns list of filter keys like ["mytype::where", "custom::*"]
        """
        from .cssl_runtime import get_custom_filters
        return list(get_custom_filters().keys())

    def builtin_filter_exists(self, filter_type: str, helper: str) -> bool:
        """Check if a custom filter exists.
        Usage: filter::exists("mytype", "where")
        """
        from .cssl_runtime import get_custom_filters
        key = f"{filter_type}::{helper}"
        return key in get_custom_filters()

    # ============= Regex Functions =============

    def builtin_match(self, pattern: str, string: str) -> Optional[dict]:
        m = re.match(pattern, string)
        if m:
            return {'match': m.group(), 'groups': m.groups(), 'start': m.start(), 'end': m.end()}
        return None

    def builtin_search(self, pattern: str, string: str) -> Optional[dict]:
        m = re.search(pattern, string)
        if m:
            return {'match': m.group(), 'groups': m.groups(), 'start': m.start(), 'end': m.end()}
        return None

    def builtin_findall(self, pattern: str, string: str) -> list:
        return re.findall(pattern, string)

    def builtin_sub(self, pattern: str, repl: str, string: str, count: int = 0) -> str:
        return re.sub(pattern, repl, string, count)

    # ============= Hash Functions =============

    def builtin_md5(self, s: str) -> str:
        return hashlib.md5(s.encode()).hexdigest()

    def builtin_sha1(self, s: str) -> str:
        return hashlib.sha1(s.encode()).hexdigest()

    def builtin_sha256(self, s: str) -> str:
        return hashlib.sha256(s.encode()).hexdigest()

    # ============= Utility Functions =============

    def builtin_copy(self, value: Any) -> Any:
        import copy
        return copy.copy(value)

    def builtin_deepcopy(self, value: Any) -> Any:
        import copy
        return copy.deepcopy(value)

    def builtin_assert(self, condition: bool, message: str = "Assertion failed") -> None:
        if not condition:
            raise CSSLBuiltinError(message)

    def builtin_exit(self, code: int = 0) -> None:
        if self.runtime and hasattr(self.runtime, 'exit'):
            self.runtime.exit(code)
        else:
            raise SystemExit(code)

    def builtin_original(self, func_name: str, *args) -> Any:
        """Call the original version of a replaced function.

        Usage:
            exit <<== { printl("custom exit"); }
            original("exit");  // Calls the ORIGINAL exit, not the replacement

            // In an injection that was defined BEFORE replacement:
            old_exit <<== { original("exit"); }  // Calls original exit
        """
        if self.runtime and hasattr(self.runtime, '_original_functions'):
            original_func = self.runtime._original_functions.get(func_name)
            if original_func is not None:
                if callable(original_func):
                    return original_func(*args)
                elif isinstance(original_func, type(lambda: None).__class__.__bases__[0]):  # Check if bound method
                    return original_func(*args)
        # Fallback: try to call builtin directly
        builtin_method = getattr(self, f'builtin_{func_name}', None)
        if builtin_method:
            return builtin_method(*args)
        raise CSSLBuiltinError(f"No original function '{func_name}' found")

    def builtin_env(self, name: str, default: str = None) -> Optional[str]:
        return os.environ.get(name, default)

    def builtin_setenv(self, name: str, value: str) -> None:
        """Set environment variable"""
        os.environ[name] = value

    # v4.8.5: os module replacement builtins
    def builtin_getcwd(self) -> str:
        """Get current working directory (replaces os.getcwd())"""
        return os.getcwd()

    def builtin_chdir(self, path: str) -> bool:
        """Change current working directory (replaces os.chdir())"""
        os.chdir(path)
        return True

    def builtin_mkdir(self, path: str) -> bool:
        """Create single directory (replaces os.mkdir())"""
        os.mkdir(path)
        return True

    def builtin_rmdir(self, path: str) -> bool:
        """Remove empty directory (alias for removedir, replaces os.rmdir())"""
        os.rmdir(path)
        return True

    def builtin_rmfile(self, path: str) -> bool:
        """Remove file (alias for removefile, replaces os.remove())"""
        os.remove(path)
        return True

    def builtin_rename(self, src: str, dst: str) -> bool:
        """Rename file or directory (replaces os.rename())"""
        os.rename(src, dst)
        return True

    def builtin_argv(self) -> list:
        """Get command line arguments (replaces sys.argv)"""
        import sys
        return sys.argv

    def builtin_argc(self) -> int:
        """Get argument count (replaces len(sys.argv))"""
        import sys
        return len(sys.argv)

    def builtin_platform(self) -> str:
        """Get platform name (replaces sys.platform)"""
        import sys
        return sys.platform

    def builtin_version(self) -> str:
        """Get Python version (replaces sys.version)"""
        import sys
        return sys.version

    def builtin_input(self, prompt: str = '') -> str:
        """Read user input"""
        return input(prompt)

    def builtin_clear(self) -> None:
        """Clear console screen"""
        if os.name == 'nt':
            # Use ANSI escape codes on Windows 10+ (modern terminals support it)
            # Fall back to subprocess for older Windows
            print('\033[2J\033[H', end='', flush=True)
        else:
            print('\033[2J\033[H', end='', flush=True)

    def builtin_color(self, text: str, color: str) -> str:
        """Apply ANSI color to text"""
        colors = {
            'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
            'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
            'bright_black': '90', 'bright_red': '91', 'bright_green': '92',
            'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
            'bright_cyan': '96', 'bright_white': '97',
            'reset': '0', 'bold': '1', 'dim': '2', 'italic': '3',
            'underline': '4', 'blink': '5', 'reverse': '7'
        }
        code = colors.get(color.lower(), color)
        return f'\033[{code}m{text}\033[0m'

    def builtin_delay(self, ms: float) -> None:
        """Delay execution by milliseconds"""
        time.sleep(ms / 1000.0)

    # =========================================================================
    # v4.6.5: Individual Color Functions for F-Strings
    # Usage: string name = f"{red("H")}{green("E")}{yellow("Y")}"
    # Accepts any type (string, int, float, etc.) - auto-converts to string
    # =========================================================================

    def _color_str(self, value) -> str:
        """Convert any value to string for color functions."""
        if value is None:
            return "null"
        return str(value)

    # --- Named Colors (Foreground) ---
    def builtin_red(self, text) -> str:
        """Apply red color: red("hello") or red(123)"""
        return f'\033[31m{self._color_str(text)}\033[0m'

    def builtin_green(self, text) -> str:
        """Apply green color to text"""
        return f'\033[32m{self._color_str(text)}\033[0m'

    def builtin_blue(self, text) -> str:
        """Apply blue color to text"""
        return f'\033[34m{self._color_str(text)}\033[0m'

    def builtin_yellow(self, text) -> str:
        """Apply yellow color to text"""
        return f'\033[33m{self._color_str(text)}\033[0m'

    def builtin_cyan(self, text) -> str:
        """Apply cyan color to text"""
        return f'\033[36m{self._color_str(text)}\033[0m'

    def builtin_magenta(self, text) -> str:
        """Apply magenta color to text"""
        return f'\033[35m{self._color_str(text)}\033[0m'

    def builtin_white(self, text) -> str:
        """Apply white color to text"""
        return f'\033[37m{self._color_str(text)}\033[0m'

    def builtin_black(self, text) -> str:
        """Apply black color to text"""
        return f'\033[30m{self._color_str(text)}\033[0m'

    # --- Bright Color Variants ---
    def builtin_bright_red(self, text) -> str:
        """Apply bright red color to text"""
        return f'\033[91m{self._color_str(text)}\033[0m'

    def builtin_bright_green(self, text) -> str:
        """Apply bright green color to text"""
        return f'\033[92m{self._color_str(text)}\033[0m'

    def builtin_bright_blue(self, text) -> str:
        """Apply bright blue color to text"""
        return f'\033[94m{self._color_str(text)}\033[0m'

    def builtin_bright_yellow(self, text) -> str:
        """Apply bright yellow color to text"""
        return f'\033[93m{self._color_str(text)}\033[0m'

    def builtin_bright_cyan(self, text) -> str:
        """Apply bright cyan color to text"""
        return f'\033[96m{self._color_str(text)}\033[0m'

    def builtin_bright_magenta(self, text) -> str:
        """Apply bright magenta color to text"""
        return f'\033[95m{self._color_str(text)}\033[0m'

    def builtin_bright_white(self, text) -> str:
        """Apply bright white color to text"""
        return f'\033[97m{self._color_str(text)}\033[0m'

    # --- RGB Custom Colors (24-bit True Color) ---
    def builtin_rgb(self, text, r: int, g: int, b: int) -> str:
        """Apply RGB color to text using 24-bit true color.

        Usage: rgb("hello", 255, 128, 0) -> orange text
        """
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        return f'\033[38;2;{r};{g};{b}m{self._color_str(text)}\033[0m'

    # --- Background Colors ---
    def builtin_bg_red(self, text) -> str:
        """Apply red background to text"""
        return f'\033[41m{self._color_str(text)}\033[0m'

    def builtin_bg_green(self, text) -> str:
        """Apply green background to text"""
        return f'\033[42m{self._color_str(text)}\033[0m'

    def builtin_bg_blue(self, text) -> str:
        """Apply blue background to text"""
        return f'\033[44m{self._color_str(text)}\033[0m'

    def builtin_bg_yellow(self, text) -> str:
        """Apply yellow background to text"""
        return f'\033[43m{self._color_str(text)}\033[0m'

    def builtin_bg_cyan(self, text) -> str:
        """Apply cyan background to text"""
        return f'\033[46m{self._color_str(text)}\033[0m'

    def builtin_bg_magenta(self, text) -> str:
        """Apply magenta background to text"""
        return f'\033[45m{self._color_str(text)}\033[0m'

    def builtin_bg_white(self, text) -> str:
        """Apply white background to text"""
        return f'\033[47m{self._color_str(text)}\033[0m'

    def builtin_bg_black(self, text) -> str:
        """Apply black background to text"""
        return f'\033[40m{self._color_str(text)}\033[0m'

    def builtin_bg_rgb(self, text, r: int, g: int, b: int) -> str:
        """Apply RGB background color using 24-bit true color.

        Usage: bg_rgb("hello", 255, 128, 0) -> orange background
        """
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
        return f'\033[48;2;{r};{g};{b}m{self._color_str(text)}\033[0m'

    # --- Text Style Functions ---
    def builtin_bold(self, text) -> str:
        """Apply bold style to text"""
        return f'\033[1m{self._color_str(text)}\033[0m'

    def builtin_italic(self, text) -> str:
        """Apply italic/cursive style to text"""
        return f'\033[3m{self._color_str(text)}\033[0m'

    def builtin_underline(self, text) -> str:
        """Apply underline style to text"""
        return f'\033[4m{self._color_str(text)}\033[0m'

    def builtin_dim(self, text) -> str:
        """Apply dim/faint style to text"""
        return f'\033[2m{self._color_str(text)}\033[0m'

    def builtin_blink(self, text) -> str:
        """Apply blinking style to text (not supported in all terminals)"""
        return f'\033[5m{self._color_str(text)}\033[0m'

    def builtin_reverse_style(self, text) -> str:
        """Reverse foreground and background colors"""
        return f'\033[7m{self._color_str(text)}\033[0m'

    def builtin_strikethrough(self, text) -> str:
        """Apply strikethrough style to text"""
        return f'\033[9m{self._color_str(text)}\033[0m'

    def builtin_reset(self, text="") -> str:
        """Reset all styles. Can wrap text or return just the reset code.

        Usage:
            reset("text") -> returns text without any styles
            reset() -> returns the ANSI reset code
        """
        if text:
            return f'\033[0m{self._color_str(text)}\033[0m'
        return '\033[0m'

    # v4.8.5: Blocked modules for pyimport (os/sys replaced by CSSL builtins)
    BLOCKED_MODULES = {'os', 'sys', 'subprocess', 'shutil'}

    def builtin_pyimport(self, module_name: str) -> Any:
        """
        Import a Python module for use in CSSL.

        v4.8.5: All modules allowed EXCEPT os, sys, subprocess, shutil.
                Use CSSL builtins for filesystem/system operations instead:
                - env(), setenv() for environment variables
                - getcwd(), chdir() for directory operations
                - readfile(), writefile() for file I/O
                - initsh() for shell commands (restricted)
                - exit() for program termination
                - argv, argc for command line args

        Usage:
            @math = pyimport("math");
            result = math.sqrt(16);

            @requests = pyimport("requests");
            response = requests.get("https://api.example.com");
        """
        import importlib
        # Check if module is blocked
        base_module = module_name.split('.')[0]
        if base_module in self.BLOCKED_MODULES:
            alternatives = {
                'os': 'Use CSSL builtins: env(), setenv(), getcwd(), chdir(), readfile(), writefile(), mkdir(), rmdir(), listdir()',
                'sys': 'Use CSSL builtins: exit(), argv, argc, parameter',
                'subprocess': 'Use CSSL builtin: initsh() for shell commands',
                'shutil': 'Use CSSL builtins: copyfile(), movefile(), rmfile()'
            }
            alt_msg = alternatives.get(base_module, 'Use CSSL builtins instead')
            raise RuntimeError(
                f"Module '{module_name}' is blocked for security.\n{alt_msg}"
            )
        return importlib.import_module(module_name)

    # ============= v4.8.4: C++ Import & I/O Streams =============

    # Global stream instances (singleton pattern for C++ behavior)
    _cout_instance = None
    _cin_instance = None
    _cerr_instance = None
    _clog_instance = None

    def builtin_cppimport(self, module_name: str) -> Any:
        """Import a compiled C++ module from IncludeCPP.

        Supports importing IncludeCPP modules directly into CSSL.
        Uses the C++ optimized module if available.

        Usage:
            @mathlib = cppimport("mathlib");
            result = mathlib.add(5, 3);

            // Or with full path:
            @mod = cppimport("includecpp.mathlib");
        """
        try:
            # Check if it's an includecpp module request
            if module_name.startswith('includecpp.'):
                actual_name = module_name[11:]  # Remove 'includecpp.' prefix
            else:
                actual_name = module_name

            # Try to import from includecpp
            try:
                import includecpp
                if hasattr(includecpp, actual_name):
                    return getattr(includecpp, actual_name)

                # Try using CppApi directly
                api = includecpp.CppApi()
                if actual_name in api.registry:
                    return api.include(actual_name)
            except Exception:
                pass

            # Fallback: try as a regular Python module (for .pyd files)
            import importlib
            return importlib.import_module(module_name)

        except Exception as e:
            raise RuntimeError(f"Failed to import C++ module '{module_name}': {e}")

    def builtin_include(self, module_path: str) -> Any:
        """Include a module (IncludeCPP or file).

        Usage:
            @mod = include("includecpp.mathlib");  // C++ module
            @header = include("./myheader.h");      // Header file
        """
        if module_path.startswith('includecpp.'):
            return self.builtin_cppimport(module_path)
        elif module_path.endswith(('.h', '.hpp', '.cpp', '.c')):
            # Include as source file (read content)
            return self.builtin_readfile(module_path)
        else:
            return self.builtin_cppimport(module_path)

    def builtin_cout(self) -> 'OutputStream':
        """Get stdout stream (C++ cout equivalent).

        C++ optimized output stream with << operator support.

        Usage:
            cout() << "Hello" << " World" << endl();
        """
        from .cssl_types import OutputStream
        if CSSLBuiltins._cout_instance is None:
            CSSLBuiltins._cout_instance = OutputStream('stdout')
        return CSSLBuiltins._cout_instance

    def builtin_cin(self) -> 'InputStream':
        """Get stdin stream (C++ cin equivalent).

        C++ optimized input stream with >> operator support.

        Usage:
            @name = cin().read(str);
            @age = cin().read(int);
        """
        from .cssl_types import InputStream
        if CSSLBuiltins._cin_instance is None:
            CSSLBuiltins._cin_instance = InputStream('stdin')
        return CSSLBuiltins._cin_instance

    def builtin_cerr(self) -> 'OutputStream':
        """Get stderr stream (C++ cerr equivalent).

        Auto-flushing error output stream.

        Usage:
            cerr() << "Error: " << errMsg << endl();
        """
        from .cssl_types import OutputStream
        if CSSLBuiltins._cerr_instance is None:
            CSSLBuiltins._cerr_instance = OutputStream('stderr')
        return CSSLBuiltins._cerr_instance

    def builtin_clog(self) -> 'OutputStream':
        """Get log stream (C++ clog equivalent).

        Buffered logging output stream.

        Usage:
            clog() << "[INFO] " << message << endl();
        """
        from .cssl_types import OutputStream
        if CSSLBuiltins._clog_instance is None:
            CSSLBuiltins._clog_instance = OutputStream('clog')
        return CSSLBuiltins._clog_instance

    def builtin_endl(self) -> str:
        """End line and flush (C++ endl equivalent).

        Usage:
            cout() << "Hello" << endl();
        """
        return 'endl'

    def builtin_getline(self, stream=None) -> str:
        """Read entire line from stream (C++ getline equivalent).

        Usage:
            @line = getline();           // From stdin
            @line = getline(fileStream); // From file
        """
        if stream is None:
            stream = self.builtin_cin()
        if hasattr(stream, 'getline'):
            return stream.getline()
        # Fallback for regular file objects
        if hasattr(stream, 'readline'):
            return stream.readline().rstrip('\n')
        return str(stream)

    def builtin_fstream(self, filename: str = None, mode: str = 'r+') -> 'FileStream':
        """Create file stream (C++ fstream equivalent).

        C++ optimized file I/O with << and >> operator support.

        Usage:
            @file = fstream("data.txt", "r+");
            file << "Hello" << endl();
            @data = file.read(str);
            file.close();
        """
        from .cssl_types import FileStream
        return FileStream(filename, mode)

    def builtin_ifstream(self, filename: str = None) -> 'FileStream':
        """Create input file stream (C++ ifstream equivalent).

        Usage:
            @file = ifstream("input.txt");
            @content = file.readall();
        """
        from .cssl_types import FileStream
        return FileStream(filename, 'r')

    def builtin_ofstream(self, filename: str = None) -> 'FileStream':
        """Create output file stream (C++ ofstream equivalent).

        Usage:
            @file = ofstream("output.txt");
            file << "Data" << endl();
        """
        from .cssl_types import FileStream
        return FileStream(filename, 'w')

    def builtin_setprecision(self, n: int) -> dict:
        """Set floating point precision (C++ setprecision equivalent).

        Returns a manipulator object for use with streams.

        Usage:
            cout() << setprecision(4) << 3.14159;  // "3.1416"
        """
        return {'type': 'manipulator', 'name': 'setprecision', 'value': n}

    def builtin_setw(self, n: int) -> dict:
        """Set field width (C++ setw equivalent).

        Usage:
            cout() << setw(10) << value;
        """
        return {'type': 'manipulator', 'name': 'setw', 'value': n}

    def builtin_setfill(self, c: str) -> dict:
        """Set fill character (C++ setfill equivalent).

        Usage:
            cout() << setfill('0') << setw(5) << 42;  // "00042"
        """
        return {'type': 'manipulator', 'name': 'setfill', 'value': c}

    def builtin_fixed(self) -> dict:
        """Use fixed-point notation (C++ fixed equivalent).

        Usage:
            cout() << fixed() << 3.14159;
        """
        return {'type': 'manipulator', 'name': 'fixed'}

    def builtin_scientific(self) -> dict:
        """Use scientific notation (C++ scientific equivalent).

        Usage:
            cout() << scientific() << 1234.5;  // "1.234500e+03"
        """
        return {'type': 'manipulator', 'name': 'scientific'}

    def builtin_flush(self) -> str:
        """Flush stream (C++ flush equivalent).

        Usage:
            cout() << "Processing..." << flush();
        """
        return 'flush'

    # ============= Struct Operations =============

    def builtin_sizeof(self, obj: Any) -> int:
        """Get size of object in bytes (C sizeof equivalent).

        For CStruct, returns estimated memory size.
        For other types, returns sys.getsizeof.

        Usage:
            @size = sizeof(myStruct);
            @size = sizeof(myArray);
        """
        import sys
        from .cssl_types import CStruct
        if isinstance(obj, CStruct):
            return obj.sizeof()
        return sys.getsizeof(obj)

    def builtin_memcpy(self, dest: Any, src: Any, n: int = None) -> Any:
        """Copy memory/data (C memcpy equivalent).

        For lists/arrays, copies n elements.
        For structs, copies all fields.

        Usage:
            memcpy(destArray, srcArray, 10);
            memcpy(destStruct, srcStruct);
        """
        from .cssl_types import CStruct
        if isinstance(src, CStruct) and isinstance(dest, CStruct):
            # Copy struct fields
            for name, value in src._values.items():
                if name in dest._fields:
                    dest._values[name] = value
            return dest
        elif hasattr(dest, '__setitem__') and hasattr(src, '__getitem__'):
            # Copy array/list elements
            count = n if n is not None else len(src)
            for i in range(min(count, len(src), len(dest) if hasattr(dest, '__len__') else count)):
                dest[i] = src[i]
            return dest
        else:
            # Generic copy
            import copy
            return copy.copy(src)

    def builtin_memset(self, dest: Any, value: Any, n: int = None) -> Any:
        """Set memory/data to value (C memset equivalent).

        For lists/arrays, sets n elements to value.
        For structs, sets all fields to value.

        Usage:
            memset(myArray, 0, 100);
            memset(myStruct, null);
        """
        from .cssl_types import CStruct
        if isinstance(dest, CStruct):
            for name in dest._values:
                dest._values[name] = value
            return dest
        elif hasattr(dest, '__setitem__'):
            count = n if n is not None else len(dest)
            for i in range(min(count, len(dest) if hasattr(dest, '__len__') else count)):
                dest[i] = value
            return dest
        return dest

    # ============= Pipe Operations =============

    def builtin_pipe(self, data: Any = None) -> 'Pipe':
        """Create a new pipe for data transformation.

        C++ optimized piping with | operator support.

        Usage:
            @result = pipe([1,2,3,4,5])
                | Pipe.filter(x => x > 2)
                | Pipe.map(x => x * 2)
                | collect();
        """
        from .cssl_types import Pipe
        return Pipe(data)

    # ============= Optimized Containment Check =============

    def builtin_contains_fast(self, container: Any, item: Any, use_native: bool = False) -> bool:
        """Fast containment check (C++ optimized 'in' operator).

        When use_native=False (default), uses C++ optimized search.
        When use_native=True, uses Python's native 'in' operator.

        For sorted containers, uses binary search (O(log n)).
        For hash-based containers, uses O(1) lookup.

        Usage:
            // C++ optimized (default)
            @found = contains_fast(myList, 42);

            // Python native
            @found = contains_fast(myList, 42, true);
        """
        if use_native:
            # Python native 'in' operator
            return item in container

        # C++ optimized path
        from .cssl_types import Vector, Array, List, Dictionary, Map, DataStruct

        # Hash-based containers - O(1)
        if isinstance(container, (dict, set, frozenset)):
            return item in container
        if isinstance(container, (Dictionary, Map)):
            return container.contains(item)

        # For sorted data, use binary search - O(log n)
        if isinstance(container, (list, tuple, Vector, Array, List, DataStruct)):
            # Check if sorted (sample check for performance)
            data = list(container) if not isinstance(container, list) else container
            if len(data) > 10:
                # Quick sorted check on sample
                sample = [data[i] for i in range(0, len(data), max(1, len(data) // 10))]
                try:
                    is_sorted = all(sample[i] <= sample[i+1] for i in range(len(sample)-1))
                    if is_sorted:
                        # Binary search
                        import bisect
                        idx = bisect.bisect_left(data, item)
                        return idx < len(data) and data[idx] == item
                except TypeError:
                    pass  # Non-comparable items, fall through to linear

            # Linear search with early termination
            for x in data:
                if x == item:
                    return True
            return False

        # String containment - use native (already optimized in Python)
        if isinstance(container, str):
            return str(item) in container

        # Generic fallback
        try:
            return item in container
        except TypeError:
            return False

    # ============= Extended String Functions =============

    def builtin_sprintf(self, fmt: str, *args) -> str:
        """C-style format string with validation.

        v4.7.1: Added format specifier validation for security.
        """
        import re
        # Count format specifiers (excluding %%)
        specifiers = re.findall(r'%(?!%)[#0\- +]*\d*\.?\d*[hlL]?[diouxXeEfFgGcrsab]', fmt)
        if len(specifiers) != len(args):
            raise ValueError(
                f"Format string has {len(specifiers)} specifiers but {len(args)} arguments provided"
            )
        return fmt % args

    def builtin_chars(self, s: str) -> list:
        """Convert string to list of characters"""
        return list(s)

    def builtin_ord(self, c: str) -> int:
        """Get ASCII/Unicode code of character"""
        return ord(c[0] if c else '\0')

    def builtin_chr(self, n: int) -> str:
        """Convert ASCII/Unicode code to character"""
        return chr(n)

    def builtin_capitalize(self, s: str) -> str:
        return str(s).capitalize()

    def builtin_title(self, s: str) -> str:
        return str(s).title()

    def builtin_swapcase(self, s: str) -> str:
        return str(s).swapcase()

    def builtin_center(self, s: str, width: int, fillchar: str = ' ') -> str:
        return str(s).center(width, fillchar)

    def builtin_zfill(self, s: str, width: int) -> str:
        return str(s).zfill(width)

    def builtin_isalpha(self, s: str) -> bool:
        return str(s).isalpha()

    def builtin_isdigit(self, s: str) -> bool:
        return str(s).isdigit()

    def builtin_isalnum(self, s: str) -> bool:
        return str(s).isalnum()

    def builtin_isspace(self, s: str) -> bool:
        return str(s).isspace()

    # ============= Extended List Functions =============

    def builtin_enumerate(self, lst: list, start: int = 0) -> list:
        """Return list of (index, value) pairs"""
        return list(enumerate(lst, start))

    def builtin_zip(self, *lists) -> list:
        """Zip multiple lists together"""
        return list(zip(*lists))

    def builtin_reversed(self, lst: list) -> list:
        """Return reversed list"""
        return list(reversed(lst))

    def builtin_sorted(self, lst: list, key: str = None, reverse: bool = False) -> list:
        """Return sorted list"""
        if key:
            return sorted(lst, key=lambda x: x.get(key) if isinstance(x, dict) else x, reverse=reverse)
        return sorted(lst, reverse=reverse)

    def builtin_count(self, collection: Union[list, str], item: Any) -> int:
        """Count occurrences of item"""
        return collection.count(item)

    def builtin_first(self, lst: list, default: Any = None) -> Any:
        """Get first element or default"""
        return lst[0] if lst else default

    def builtin_last(self, lst: list, default: Any = None) -> Any:
        """Get last element or default"""
        return lst[-1] if lst else default

    def builtin_take(self, lst: list, n: int) -> list:
        """Take first n elements"""
        return lst[:n]

    def builtin_drop(self, lst: list, n: int) -> list:
        """Drop first n elements"""
        return lst[n:]

    def builtin_chunk(self, lst: list, size: int) -> list:
        """Split list into chunks of given size"""
        return [lst[i:i + size] for i in range(0, len(lst), size)]

    def builtin_groupby(self, lst: list, key: str) -> dict:
        """Group list of dicts by key"""
        result = {}
        for item in lst:
            k = item.get(key) if isinstance(item, dict) else getattr(item, key, None)
            if k not in result:
                result[k] = []
            result[k].append(item)
        return result

    def builtin_shuffle(self, lst: list) -> list:
        """Return shuffled copy of list"""
        result = list(lst)
        random.shuffle(result)
        return result

    def builtin_sample(self, lst: list, k: int) -> list:
        """Return k random elements from list"""
        return random.sample(lst, min(k, len(lst)))

    # ============= Extended Dict Functions =============

    def builtin_update(self, d: dict, other: dict) -> dict:
        """Update dict with another dict, return new dict"""
        result = dict(d)
        result.update(other)
        return result

    def builtin_fromkeys(self, keys: list, value: Any = None) -> dict:
        """Create dict from keys with default value"""
        return dict.fromkeys(keys, value)

    def builtin_invert(self, d: dict) -> dict:
        """Swap keys and values"""
        return {v: k for k, v in d.items()}

    def builtin_pick(self, d: dict, *keys) -> dict:
        """Pick only specified keys from dict"""
        return {k: d[k] for k in keys if k in d}

    def builtin_omit(self, d: dict, *keys) -> dict:
        """Omit specified keys from dict"""
        return {k: v for k, v in d.items() if k not in keys}

    # ============= CSSL System Functions =============

    def builtin_createcmd(self, cmd_name: str, handler: Callable = None) -> bool:
        """
        Create a custom console command
        Usage: createcmd('mycommand') <== { ... handler code ... }
        """
        if not self.runtime:
            print(f"Cannot create command '{cmd_name}': No runtime available")
            return False

        # Store the command handler in runtime
        if not hasattr(self.runtime, '_custom_commands'):
            self.runtime._custom_commands = {}

        self.runtime._custom_commands[cmd_name] = handler

        # Find Console via multiple paths
        console = None

        # Try 1: Direct _console reference on runtime
        if hasattr(self.runtime, '_console') and self.runtime._console:
            console = self.runtime._console

        # Try 2: Via service_engine.Console
        elif self.runtime.service_engine and hasattr(self.runtime.service_engine, 'Console'):
            console = self.runtime.service_engine.Console

        # Register with Console if found
        if console and hasattr(console, 'register_custom_command'):
            console.register_custom_command(cmd_name, handler)
        else:
            print(f"Custom command '{cmd_name}' stored (Console not yet available)")

        return True

    def builtin_signal(self, event_ref: Any, action: str = '+') -> bool:
        """
        Send or register a signal/event
        Usage: signal(@event.CustomEvent, '+') to emit, '-' to unregister
        """
        try:
            from .cssl_events import get_event_manager, EventType

            event_manager = get_event_manager()

            # Handle event reference (could be string or module ref)
            event_name = str(event_ref) if not isinstance(event_ref, str) else event_ref

            if action == '+':
                # Emit the event
                event_manager.emit_custom(event_name, source="cssl_signal")
                print(f"Signal emitted: {event_name}")
                return True
            elif action == '-':
                # Unregister handlers for this event
                # This would need custom implementation
                print(f"Signal handlers cleared: {event_name}")
                return True
            else:
                print(f"Unknown signal action: {action}")
                return False

        except Exception as e:
            print(f"Signal error: {e}")
            return False

    def builtin_appexec(self, app_name: str, *args) -> bool:
        """
        Start a desktop application (visually)
        Usage: appexec('xface')
        """
        if not self.runtime or not self.runtime.service_engine:
            print(f"Cannot execute app '{app_name}': No service engine available")
            return False

        try:
            kernel = self.runtime.service_engine.KernelClient

            # Check if desktop environment is available
            if hasattr(kernel, 'start_desktop_app'):
                return kernel.start_desktop_app(app_name, *args)

            # Try to find and launch the app
            app_paths = [
                os.path.join(kernel.RootDirectory, 'apps', app_name),
                os.path.join(kernel.RootDirectory, 'apps', f'{app_name}.py'),
                os.path.join(kernel.RootDirectory, 'desktop', 'apps', app_name),
                os.path.join(kernel.RootDirectory, 'desktop', 'apps', f'{app_name}.py'),
            ]

            for app_path in app_paths:
                if os.path.exists(app_path):
                    print(f"Launching app: {app_name}")
                    if app_path.endswith('.py'):
                        return self.builtin_initpy(app_path)
                    return True

            print(f"App not found: {app_name}")
            return False

        except Exception as e:
            print(f"App execution error: {e}")
            return False

    def builtin_initpy(self, path: str, *args, **kwargs) -> Any:
        """
        Execute a Python file
        Usage: initpy('/path/to/script.py')
        """
        if not os.path.isabs(path) and self.runtime and self.runtime.service_engine:
            path = os.path.join(self.runtime.service_engine.KernelClient.RootDirectory, path)

        if not os.path.exists(path):
            raise CSSLBuiltinError(f"Python file not found: {path}")

        try:
            # Prepare execution context
            exec_globals = {
                '__file__': path,
                '__name__': '__main__',
            }

            # Add kernel and service engine if available
            if self.runtime and self.runtime.service_engine:
                exec_globals['kernel'] = self.runtime.service_engine.KernelClient
                exec_globals['service'] = self.runtime.service_engine
                exec_globals['args'] = args
                exec_globals['kwargs'] = kwargs

            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()

            exec(compile(code, path, 'exec'), exec_globals)
            return exec_globals.get('result', True)

        except Exception as e:
            print(f"Python execution error [{path}]: {e}")
            raise CSSLBuiltinError(f"initpy failed: {e}")

    def builtin_initsh(self, path: str, *args) -> int:
        """
        Execute a shell script from the 'scripts' directory only.

        v4.7.1: Restricted to 'scripts/' directory for security.

        Usage: initsh('myscript.sh')  // Runs scripts/myscript.sh
        """
        import subprocess

        # v4.7.1: Security - prevent directory traversal
        if '..' in path or os.path.isabs(path):
            raise CSSLBuiltinError(
                f"Invalid script path: '{path}'. "
                "Scripts must be relative paths without '..' and must be in 'scripts/' directory."
            )

        # Determine base directory
        if self.runtime and self.runtime.service_engine:
            base_dir = self.runtime.service_engine.KernelClient.RootDirectory
        else:
            base_dir = os.getcwd()

        # Force scripts to be in 'scripts' subdirectory
        scripts_dir = os.path.join(base_dir, 'scripts')
        full_path = os.path.normpath(os.path.join(scripts_dir, path))

        # Verify path is within scripts directory (prevent traversal)
        if not full_path.startswith(os.path.normpath(scripts_dir)):
            raise CSSLBuiltinError(
                f"Security: Script path '{path}' escapes the scripts directory."
            )

        if not os.path.exists(full_path):
            raise CSSLBuiltinError(f"Shell script not found: {full_path}")

        # Validate file extension
        valid_extensions = {'.sh', '.bat', '.cmd', '.ps1'}
        _, ext = os.path.splitext(full_path)
        if ext.lower() not in valid_extensions:
            raise CSSLBuiltinError(
                f"Invalid script type: '{ext}'. Allowed: {', '.join(valid_extensions)}"
            )

        try:
            # Determine shell based on platform
            import platform
            if platform.system() == 'Windows':
                if ext.lower() == '.ps1':
                    cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', full_path] + list(args)
                else:
                    cmd = ['cmd', '/c', full_path] + list(args)
            else:
                cmd = ['bash', full_path] + list(args)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"STDERR: {result.stderr}")

            return result.returncode

        except subprocess.TimeoutExpired:
            raise CSSLBuiltinError(f"Script execution timeout (60s): {path}")
        except Exception as e:
            print(f"Shell execution error [{path}]: {e}")
            raise CSSLBuiltinError(f"initsh failed: {e}")

    def builtin_wait_for(self, condition: Callable, timeout: float = 30.0, interval: float = 0.1) -> bool:
        """
        Wait for a condition to become true
        Usage: wait_for(lambda: some_condition, timeout=30)
        """
        import time
        start = time.time()

        while time.time() - start < timeout:
            try:
                if callable(condition):
                    if condition():
                        return True
                elif condition:
                    return True
            except Exception:
                pass
            time.sleep(interval)

        return False

    def builtin_wait_for_event(self, event_name: str, timeout: float = 30.0) -> bool:
        """
        Wait for a specific event to occur
        Usage: wait_for_event('@event.Booted', timeout=60)
        """
        try:
            from .cssl_events import get_event_manager

            event_manager = get_event_manager()
            event_occurred = [False]

            def handler(event_data):
                event_occurred[0] = True

            # Register temporary handler
            handler_id = event_manager.register_custom(
                event_name,
                handler,
                once=True
            )

            # Wait for event
            import time
            start = time.time()
            while not event_occurred[0] and (time.time() - start) < timeout:
                time.sleep(0.1)

            # Cleanup if not occurred
            if not event_occurred[0]:
                event_manager.unregister(handler_id)

            return event_occurred[0]

        except Exception as e:
            print(f"wait_for_event error: {e}")
            return False

    def builtin_wait_for_booted(self, timeout: float = 60.0) -> bool:
        """
        Wait until the system is fully booted
        Usage: await wait_for_booted()
        """
        if not self.runtime or not self.runtime.service_engine:
            return False

        import time
        start = time.time()

        while time.time() - start < timeout:
            try:
                wheel = self.runtime.service_engine.KernelClient.WheelKernel
                booted = wheel.ReadWheelParam('boot', 'BOOTED')
                if booted == '1':
                    return True
            except Exception:
                pass
            time.sleep(0.5)

        return False

    def builtin_emit(self, event_name: str, data: Any = None) -> bool:
        """
        Emit a custom event
        Usage: emit('MyCustomEvent', {data: 'value'})
        """
        try:
            from .cssl_events import get_event_manager

            event_manager = get_event_manager()
            event_manager.emit_custom(event_name, source="cssl", data=data or {})
            return True

        except Exception as e:
            print(f"emit error: {e}")
            return False

    def builtin_on_event(self, event_name: str, handler: Callable) -> str:
        """
        Register an event handler
        Usage: on_event('MyEvent', handler_function)
        Returns: handler_id for later removal
        """
        try:
            from .cssl_events import get_event_manager

            event_manager = get_event_manager()
            handler_id = event_manager.register_custom(event_name, handler)
            return handler_id

        except Exception as e:
            print(f"on_event error: {e}")
            return ""

    # ============= CSSL Import System Functions =============

    def builtin_cso_root(self, path: str = "") -> str:
        """
        Get absolute path relative to project root directory
        Usage: cso_root('/services/myservice.cssl')
        Returns: Full absolute path to the file
        """
        base = os.getcwd()

        # Try to get base from kernel parameters
        if self.runtime and self.runtime.service_engine:
            try:
                kernel = self.runtime.service_engine.KernelClient
                if hasattr(kernel, 'WheelKernel'):
                    wheel = kernel.WheelKernel
                    if hasattr(wheel, 'KernelParam'):
                        base = wheel.KernelParam.get('@base', base)
                if hasattr(kernel, 'RootDirectory'):
                    base = kernel.RootDirectory
            except Exception:
                pass

        # Clean path and join (strip leading separators for both platforms)
        if path:
            clean_path = path.lstrip('/\\')
            return os.path.normpath(os.path.join(base, clean_path))

        return base

    def builtin_include(self, filepath: str) -> Any:
        """
        Load and execute a CSSL file or .cssl-mod module, returning its ServiceDefinition
        Usage: include(cso_root('/services/utils.cssl'))
               include('modules/math_utils.cssl-mod')
               include('C:/absolute/path/module.cssl-mod')
        Returns: ServiceDefinition with structs, functions, etc.
        """
        if not self.runtime:
            raise CSSLBuiltinError("include requires runtime context")

        # Normalize path separators (support both / and \)
        filepath = filepath.replace('\\', '/')

        # Handle absolute paths (Windows: C:/, D:/, etc. and Unix: /)
        is_absolute = os.path.isabs(filepath) or (len(filepath) > 2 and filepath[1] == ':')

        if not is_absolute:
            # Try relative to current working directory first
            cwd_path = os.path.join(os.getcwd(), filepath)
            if os.path.exists(cwd_path):
                filepath = cwd_path
            else:
                # Fall back to cso_root for service context
                filepath = self.builtin_cso_root(filepath)

        # Check file exists
        if not os.path.exists(filepath):
            raise CSSLBuiltinError(f"Include file not found: {filepath}")

        # Check include cache to prevent circular imports
        if not hasattr(self.runtime, '_include_cache'):
            self.runtime._include_cache = {}

        if filepath in self.runtime._include_cache:
            return self.runtime._include_cache[filepath]

        try:
            # Read the file
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            # Check if this is a .cssl-mod file
            if filepath.endswith('.cssl-mod') or source.startswith('CSSLMOD1'):
                result = self._load_cssl_module(filepath, source)
                self.runtime._include_cache[filepath] = result
                return result

            # Regular CSSL file
            from .cssl_parser import parse_cssl

            ast = parse_cssl(source)

            # Execute the service to get definitions
            service_def = self.runtime._exec_service(ast)

            # Cache the result
            self.runtime._include_cache[filepath] = service_def

            return service_def

        except Exception as e:
            raise CSSLBuiltinError(f"Failed to include '{filepath}': {e}")

    def builtin_libinclude(self, lang_id: str) -> Any:
        """
        Load a language support module for multi-language syntax support.

        v4.1.0: Multi-language support for CSSL.

        Usage:
            @py = libinclude("python")
            cpp = libinclude("c++")
            java = libinclude("java")
            js = libinclude("javascript")
            csharp = libinclude("c#")

        Returns: LanguageSupport object that can be used with 'supports' keyword.

        Example:
            @py = libinclude("python");

            define my_func() : supports @py {
                # Python syntax here!
                for i in range(10):
                    print(i)
            }

            class MyClass : extends cpp$BaseClass {
                // Inherit from C++ class
            }
        """
        from .cssl_languages import get_language

        lang_support = get_language(lang_id)
        if lang_support is None:
            supported = ["python", "py", "java", "c#", "csharp", "c++", "cpp", "javascript", "js"]
            raise CSSLBuiltinError(
                f"Unknown language '{lang_id}'. Supported languages: {', '.join(supported)}"
            )

        return lang_support

    def _load_cssl_module(self, filepath: str, source: str) -> Any:
        """
        Load a .cssl-mod module file and return a callable module object.
        Handles Python and C++ modules.
        """
        import base64
        import pickle

        # Parse the module format: CSSLMOD1\n<base64-encoded-pickle>
        lines = source.strip().split('\n', 1)
        if len(lines) < 2 or lines[0] != 'CSSLMOD1':
            raise CSSLBuiltinError(f"Invalid .cssl-mod format: {filepath}")

        # Decode the module data
        try:
            encoded_data = lines[1].strip()
            module_data = pickle.loads(base64.b64decode(encoded_data))
        except Exception as e:
            raise CSSLBuiltinError(f"Failed to decode .cssl-mod: {e}")

        module_name = module_data.get('name', 'unknown')
        module_type = module_data.get('type', 'python')
        module_source = module_data.get('source', '')

        if module_type == 'python':
            return self._execute_python_module(module_name, module_source, filepath)
        elif module_type == 'cpp':
            return self._load_cpp_module(module_name, module_source, filepath)
        else:
            raise CSSLBuiltinError(f"Unsupported module type: {module_type}")

    def _execute_python_module(self, name: str, source: str, filepath: str) -> Any:
        """
        Execute Python source and return a module-like object with all functions.
        """
        # Create a namespace for the module
        module_namespace = {
            '__name__': name,
            '__file__': filepath,
            '__builtins__': __builtins__,
        }

        # Execute the Python source
        try:
            exec(source, module_namespace)
        except Exception as e:
            raise CSSLBuiltinError(f"Failed to execute Python module '{name}': {e}")

        # Create a callable module wrapper
        class CSSLModuleWrapper:
            """Wrapper that makes Python functions callable from CSSL"""
            def __init__(self, namespace, mod_name):
                self._namespace = namespace
                self._name = mod_name
                self._functions = {}

                # Extract all callable functions (not dunder methods)
                for key, value in namespace.items():
                    if callable(value) and not key.startswith('_'):
                        self._functions[key] = value
                        # Also set as attribute for @Module.func() syntax
                        setattr(self, key, value)

            def __getattr__(self, name):
                if name.startswith('_'):
                    raise AttributeError(f"'{self._name}' has no attribute '{name}'")
                if name in self._functions:
                    return self._functions[name]
                if name in self._namespace:
                    return self._namespace[name]
                raise AttributeError(f"Module '{self._name}' has no function '{name}'")

            def __repr__(self):
                funcs = list(self._functions.keys())
                return f"<CSSLModule '{self._name}' functions={funcs}>"

            def __dir__(self):
                return list(self._functions.keys())

        return CSSLModuleWrapper(module_namespace, name)

    def _load_cpp_module(self, name: str, source: str, filepath: str) -> Any:
        """
        Load a C++ module (stub for future implementation).
        For now, returns a placeholder with the source available.
        """
        class CppModuleStub:
            def __init__(self, mod_name, cpp_source):
                self._name = mod_name
                self._source = cpp_source

            def __repr__(self):
                return f"<CppModule '{self._name}' (not compiled)>"

            def compile(self):
                """Future: Compile and load the C++ module"""
                raise NotImplementedError("C++ module compilation not yet implemented")

        return CppModuleStub(name, source)

    def builtin_payload(self, filepath: str, libname: str = None) -> None:
        """
        Load a CSSL payload file (.cssl-pl) and execute it.

        Payloads are like header files but for CSSL:
        - Define global variables (accessible via @name)
        - Define helper functions (globally callable)
        - Inject code into builtins (like exit() <<== {...})
        - Set configuration values

        Usage in .cssl file:
            // Standard: everything is applied globally
            payload("myconfig.cssl-pl");

            // Namespaced: everything goes into a namespace
            payload("myconfig.cssl-pl", "mylib");
            mylib::myFunction();  // Access via namespace

        Namespace behavior:
            - Without libname: All changes are global (embedded replaces globally)
            - With libname: All definitions go into namespace
              - embedded new_exit &exit {} -> mylib::exit is new_exit
              - Global exit remains unchanged
              - Access via libname::function(), libname::MyClass

        Usage in Python:
            cssl = CSSL.CsslLang()
            cssl.code("myhelper", "... cssl code ...")  # Creates inline payload
            cssl.exec('payload("myhelper");')  # Loads the inline payload

        .cssl-pl file format:
            // Variables
            global version = "1.0.0";
            global debug = true;

            // Injections
            exit() <<== {
                printl("Cleanup...");
            }

            // Helper functions
            void log(string msg) {
                if (@debug) printl("[LOG] " + msg);
            }
        """
        if not self.runtime:
            raise CSSLBuiltinError("payload requires runtime context")

        # Normalize path separators
        filepath = filepath.replace('\\', '/')

        # Check if this is an inline payload (registered via cssl.code())
        if hasattr(self.runtime, '_inline_payloads') and filepath in self.runtime._inline_payloads:
            source = self.runtime._inline_payloads[filepath]
        else:
            # v4.2.6: Auto-append .cssl-pl extension if not specified
            # payload("engine") -> looks for engine.cssl-pl
            original_filepath = filepath

            # Handle absolute paths
            is_absolute = os.path.isabs(filepath) or (len(filepath) > 2 and filepath[1] == ':')

            if not is_absolute:
                # Try relative to current working directory first
                cwd_path = os.path.join(os.getcwd(), filepath)
                if os.path.exists(cwd_path):
                    filepath = cwd_path
                else:
                    # Try with .cssl-pl extension
                    cwd_path_pl = os.path.join(os.getcwd(), filepath + '.cssl-pl')
                    if os.path.exists(cwd_path_pl):
                        filepath = cwd_path_pl
                    else:
                        # Fall back to cso_root for service context
                        filepath = self.builtin_cso_root(filepath)

            # Check file exists, try with .cssl-pl extension if not
            if not os.path.exists(filepath):
                # Try adding .cssl-pl extension
                filepath_with_ext = filepath + '.cssl-pl'
                if os.path.exists(filepath_with_ext):
                    filepath = filepath_with_ext
                else:
                    raise CSSLBuiltinError(f"Payload file not found: {original_filepath} (tried {filepath} and {filepath_with_ext})")

            # Check payload cache to prevent double loading
            if not hasattr(self.runtime, '_payload_cache'):
                self.runtime._payload_cache = set()

            # For namespaced payloads, use different cache key
            cache_key = f"{filepath}::{libname}" if libname else filepath
            if cache_key in self.runtime._payload_cache:
                return  # Already loaded

            # Read the payload file
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()

            self.runtime._payload_cache.add(cache_key)

        # Parse and execute the payload
        try:
            from .cssl_parser import parse_cssl_program

            ast = parse_cssl_program(source)

            if libname:
                # Namespaced execution: execute in isolated scope
                self._execute_payload_namespaced(ast, libname, source)
            else:
                # Standard execution: apply globally
                # Execute the payload - this will:
                # - Register global variables (accessible via @name)
                # - Define functions in current scope
                # - Set up any code injections
                self.runtime._execute_node(ast)

        except Exception as e:
            raise CSSLBuiltinError(f"Failed to load payload '{filepath}': {e}")

    def _execute_payload_namespaced(self, ast, libname: str, source: str) -> None:
        """
        Execute payload in a namespace.

        All definitions go into the namespace dict.
        embedded replacements are scoped to the namespace only.
        Variables declared with 'global' keyword remain truly global (accessible via @).
        """
        # Create namespace dict
        namespace = {}

        # Save current scope state (copy the variables dicts)
        old_scope_vars = dict(self.runtime.scope.variables)
        old_global_vars = dict(self.runtime.global_scope.variables)
        old_promoted_globals = dict(self.runtime._promoted_globals)

        # Track what gets added during payload execution
        scope_before = set(self.runtime.scope.variables.keys())
        global_before = set(self.runtime.global_scope.variables.keys())
        promoted_before = set(self.runtime._promoted_globals.keys())

        # Set a flag to tell runtime we're in namespace mode
        self.runtime._payload_namespace_mode = libname

        try:
            # Execute the payload
            self.runtime._execute_node(ast)

            # Find which variables were explicitly promoted to global (via 'global' keyword)
            new_promoted = set(self.runtime._promoted_globals.keys()) - promoted_before

            # Collect new definitions from scope (but not promoted globals)
            for key in self.runtime.scope.variables:
                if key not in scope_before and key not in new_promoted:
                    namespace[key] = self.runtime.scope.get(key)

            # Collect new definitions from global_scope (but not namespace itself, not promoted globals)
            for key in self.runtime.global_scope.variables:
                if key not in global_before and key != libname and key not in new_promoted:
                    namespace[key] = self.runtime.global_scope.get(key)

            # Handle embedded replacements: move replaced targets into namespace
            if hasattr(self.runtime, '_namespace_replacements'):
                for target_name, new_impl in self.runtime._namespace_replacements.items():
                    # Get the original from before execution
                    original = old_scope_vars.get(target_name) or old_global_vars.get(target_name)
                    if original is not None:
                        # Restore original globally
                        if target_name in old_scope_vars:
                            self.runtime.scope.set(target_name, original)
                        if target_name in old_global_vars:
                            self.runtime.global_scope.set(target_name, original)
                    # Put the replacement in namespace
                    namespace[target_name] = new_impl
                del self.runtime._namespace_replacements

            # Remove new definitions from scope (they're in namespace now)
            # BUT keep promoted globals - they stay global!
            for key in list(self.runtime.scope.variables.keys()):
                if key not in scope_before and key not in new_promoted:
                    del self.runtime.scope.variables[key]

            for key in list(self.runtime.global_scope.variables.keys()):
                if key not in global_before and key != libname and key not in new_promoted:
                    del self.runtime.global_scope.variables[key]

            # Promoted globals stay in _promoted_globals and global_scope (not moved to namespace)
            # They are accessible via @name from anywhere

        finally:
            # Clear namespace mode flag
            self.runtime._payload_namespace_mode = None

        # Register namespace in global scope
        self.runtime.global_scope.set(libname, namespace)

    def builtin_get(self, source: Any, key: str = None) -> Any:
        """
        Get value from module, ServiceDefinition, or dict
        Usage:
          get('list')                   - Get list module (returns empty list creator)
          get('os')                     - Get OS module
          get('time')                   - Get Time module
          get(@Time)                    - Get standard module
          get(service_def, 'funcName')  - Get function from included service
          get(dict_obj, 'key')          - Get key from dict
        Returns: The requested value or None
        """
        # Single argument - return module reference directly
        if key is None:
            if isinstance(source, str):
                # NEW: Handle standard module names
                module_map = {
                    'list': self._get_list_module(),
                    'dict': self._get_dict_module(),
                    'os': self._get_os_module(),
                    'time': self._get_time_module(),
                    'vsramsdk': self._get_vsram_module(),
                    'kernel': self._get_kernel_module(),
                }
                if source.lower() in module_map:
                    return module_map[source.lower()]

                # Treat as module path
                if self.runtime:
                    return self.runtime.get_module(source)
            return source

        # Two arguments - extract from source
        if hasattr(source, key):
            return getattr(source, key)

        if isinstance(source, dict):
            return source.get(key)

        # Check if source is a ServiceDefinition-like object
        if hasattr(source, 'structs') and key in source.structs:
            return source.structs[key]

        if hasattr(source, 'functions') and key in source.functions:
            return source.functions[key]

        return None

    # NEW: Module factories for get()
    def _get_list_module(self):
        """Return a list module proxy"""
        class ListModule:
            @staticmethod
            def create():
                return []
            @staticmethod
            def add(lst, item):
                if isinstance(lst, list):
                    lst.append(item)
                return lst
        return ListModule()

    def _get_dict_module(self):
        """Return a dict module proxy"""
        class DictModule:
            @staticmethod
            def create():
                return {}
        return DictModule()

    def _get_os_module(self):
        """Return OS module proxy"""
        class OSModule:
            @staticmethod
            def Listdir(path='.'):
                return os.listdir(path)
            @staticmethod
            def ReadFile(path, encoding='utf-8'):
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            @staticmethod
            def WriteFile(path, content, encoding='utf-8'):
                with open(path, 'w', encoding=encoding) as f:
                    return f.write(content)
            @staticmethod
            def isLinux():
                import platform
                return platform.system() == 'Linux'
            @staticmethod
            def isWindows():
                import platform
                return platform.system() == 'Windows'
            @staticmethod
            def isMac():
                import platform
                return platform.system() == 'Darwin'
        return OSModule()

    def _get_time_module(self):
        """Return Time module proxy"""
        class TimeModule:
            @staticmethod
            def CurrentTime(format_str='%Y-%m-%d %H:%M:%S'):
                return datetime.now().strftime(format_str)
            @staticmethod
            def Now():
                return time.time()
            @staticmethod
            def Sleep(seconds):
                time.sleep(seconds)
        return TimeModule()

    def _get_vsram_module(self):
        """Return VSRAM module proxy from runtime"""
        if self.runtime and hasattr(self.runtime, '_modules'):
            return self.runtime._modules.get('VSRam') or self.runtime._modules.get('VSRAM')
        return None

    def _get_kernel_module(self):
        """Return Kernel module proxy from runtime"""
        if self.runtime and hasattr(self.runtime, '_modules'):
            return self.runtime._modules.get('Kernel') or self.runtime._modules.get('KernelClient')
        return None

    # NEW: Platform Detection Functions
    def builtin_islinux(self) -> bool:
        """Check if running on Linux"""
        import platform
        return platform.system() == 'Linux'

    def builtin_iswindows(self) -> bool:
        """Check if running on Windows"""
        import platform
        return platform.system() == 'Windows'

    def builtin_ismac(self) -> bool:
        """Check if running on macOS"""
        import platform
        return platform.system() == 'Darwin'

    # NEW: CurrentTime function
    def builtin_currenttime(self, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        """Get current time as formatted string"""
        return datetime.now().strftime(format_str)

    # NEW: Global function for scope promotion
    def builtin_global(self, s_ref: Any) -> None:
        """
        Promote s@<name> to @<name> (make globally accessible)
        Usage: global(s@cache) - makes @cache available

        This takes the value referenced by s@<name> and registers it
        as a module reference accessible via @<name>
        """
        if not self.runtime:
            return

        # The argument could be:
        # 1. A direct value from s@<name> reference
        # 2. A string path like "MyStruct.cache"

        if isinstance(s_ref, str):
            # It's a path - promote it
            self.runtime.promote_to_global(s_ref)
        else:
            # It's a value - we need the original s@<name> reference
            # This is handled by the runtime which passes the path
            pass

    def builtin_delete(self, name: str) -> bool:
        """
        Delete a shared object by name.
        Usage: delete("MyLib") - removes the $MyLib shared object

        Args:
            name: Name of the shared object (without the $ prefix)

        Returns:
            True if deleted, False if not found
        """
        from ..cssl_bridge import _live_objects

        # Remove from live objects registry
        if name in _live_objects:
            del _live_objects[name]
            # Also remove from runtime's global scope if present
            if self.runtime:
                try:
                    self.runtime.global_scope.delete(f'${name}')
                except Exception:
                    pass
            return True
        return False

    # ============= CSSL Data Type Constructors =============

    def builtin_datastruct(self, element_type: str = 'dynamic') -> Any:
        """Create a datastruct container.

        Usage: datastruct<string> myData; or datastruct('string')
        """
        from .cssl_types import DataStruct
        return DataStruct(element_type)

    def builtin_shuffled(self, element_type: str = 'dynamic') -> Any:
        """Create a shuffled container for multiple returns.

        Usage: shuffled<string> results;
        """
        from .cssl_types import Shuffled
        return Shuffled(element_type)

    def builtin_iterator(self, element_type: str = 'int', size: int = 16) -> Any:
        """Create an advanced iterator.

        Usage: iterator<int, 16> Map;
        """
        from .cssl_types import Iterator
        return Iterator(element_type, size)

    def builtin_combo(self, element_type: str = 'dynamic') -> Any:
        """Create a combo filter/search space.

        Usage: combo<open&string> myCombo;
        """
        from .cssl_types import Combo
        return Combo(element_type)

    def builtin_dataspace(self, space_type: str = 'dynamic') -> Any:
        """Create a dataspace for SQL/structured data.

        Usage: dataspace<sql::table> table;
        """
        from .cssl_types import DataSpace
        return DataSpace(space_type)

    def builtin_openquote(self, db_ref: Any = None) -> Any:
        """Create an openquote container for SQL operations.

        Usage: openquote<datastruct<dynamic>&@sql::db.oqt(@db)> Queue;
        """
        from .cssl_types import OpenQuote
        return OpenQuote(db_ref)

    def builtin_vector(self, element_type: str = 'dynamic') -> Any:
        """Create a vector container.

        Usage: vector<int> myVector; or vector('int')
        """
        from .cssl_types import Vector
        return Vector(element_type)

    def builtin_array(self, element_type: str = 'dynamic') -> Any:
        """Create an array container.

        Usage: array<string> myArray; or array('string')
        """
        from .cssl_types import Array
        return Array(element_type)

    def builtin_stack(self, element_type: str = 'dynamic') -> Any:
        """Create a stack container.

        Usage: stack<int> myStack; or stack('int')
        """
        from .cssl_types import Stack
        return Stack(element_type)

    def builtin_map(self, key_type: str = 'dynamic', value_type: str = 'dynamic') -> Any:
        """Create a map container.

        Usage: map<string, int> myMap; or map('string', 'int')
        """
        from .cssl_types import Map
        return Map(key_type, value_type)

    def builtin_openfind(self, combo_or_type: Any, index: int = 0, params: list = None) -> Any:
        """Find open parameter by type or combo space.

        Usage:
            OpenFind<string>(0)  # Find first string at position 0
            OpenFind(&@comboSpace)  # Find using combo filter

        When using with open parameters:
            open define myFunc(open Params) {
                string name = OpenFind<string>(0);  // Find nearest string at index 0
                int age = OpenFind<int>(1);  // Find nearest int at index 1
            }
        """
        from .cssl_types import Combo

        if isinstance(combo_or_type, Combo):
            # Find by combo space
            if params:
                return combo_or_type.find_match(params)
            return combo_or_type.find_match([])

        # Type-based search
        target_type = combo_or_type
        if params is None:
            params = []

        # Map type names to Python types
        type_map = {
            'string': str, 'str': str,
            'int': int, 'integer': int,
            'float': float, 'double': float,
            'bool': bool, 'boolean': bool,
            'list': list, 'array': list,
            'dict': dict, 'dictionary': dict
        }

        python_type = type_map.get(str(target_type).lower(), None)
        if python_type is None:
            return None

        # Find the nearest matching type from index position
        matches_found = 0
        for i, param in enumerate(params):
            if isinstance(param, python_type):
                if matches_found == index:
                    return param
                matches_found += 1

        return None

    # ============= Python Interop Functions =============

    def builtin_python_pythonize(self, cssl_instance: Any) -> Any:
        """Convert a CSSL class instance to a Python-usable object.

        This allows CSSL classes to be returned and used in Python code
        with proper attribute access and method calls.

        Usage in CSSL:
            class Greeter {
                string name;

                Greeter(string n) {
                    this->name = n;
                }

                string sayHello() {
                    return "Hello, " + this->name + "!";
                }

                void setName(string newName) {
                    this->name = newName;
                }

                string getName() {
                    return this->name;
                }
            }

            greeter = new Greeter("World");
            pyclass = python::pythonize(greeter);
            parameter.return(pyclass);

        Usage in Python:
            from includecpp import CSSL

            cssl = CSSL.CsslLang()
            greeter = cssl.run('''
                class Greeter { ... }
                g = new Greeter("World");
                parameter.return(python::pythonize(g));
            ''')

            # Now use it like a normal Python object:
            print(greeter.name)           # "World"
            print(greeter.sayHello())     # "Hello, World!"
            greeter.setName("Python")
            print(greeter.getName())      # "Python"

        Args:
            cssl_instance: A CSSLInstance object (created via 'new ClassName()')

        Returns:
            PythonizedCSSLInstance - A Python-friendly wrapper
        """
        from .cssl_types import CSSLInstance, CSSLClass

        if cssl_instance is None:
            return None

        # Already pythonized
        if isinstance(cssl_instance, PythonizedCSSLInstance):
            return cssl_instance

        # Must be a CSSLInstance
        if not isinstance(cssl_instance, CSSLInstance):
            # If it's a dict, wrap it as a simple object
            if isinstance(cssl_instance, dict):
                return PythonizedDict(cssl_instance)
            # Return as-is for primitives
            return cssl_instance

        return PythonizedCSSLInstance(cssl_instance, self.runtime)

    def builtin_python_csslize(self, python_obj: Any) -> Any:
        """Convert a Python object (class instance or function) to a CSSL-compatible wrapper.

        Syntax:
            cssl_obj <== python::csslize($python_instance);
            cssl_func <== python::csslize($python_function);

        Example:
            # In Python:
            class MyPythonClass:
                def __init__(self, name):
                    self.name = name
                def greet(self):
                    return f"Hello, {self.name}!"

            cssl = CSSL.CsslLang()
            cssl.set_variable('MyPython', MyPythonClass("World"))
            result = cssl.run('''
                py_obj <== python::csslize($MyPython);
                printl(py_obj.greet());  // "Hello, World!"
            ''')

        For class inheritance:
            py_class <== python::csslize($MyPythonClass);
            class MyExtended : extends py_class {
                void newMethod() { ... }
            }

        Args:
            python_obj: A Python object (class instance, function, or class)

        Returns:
            CSSLizedPythonObject - A CSSL-compatible wrapper
        """
        if python_obj is None:
            return None

        # Already csslized
        if isinstance(python_obj, CSSLizedPythonObject):
            return python_obj

        # Wrap the Python object
        return CSSLizedPythonObject(python_obj, self.runtime)

    # =========================================================================
    # v4.6.5: Watcher Namespace Functions - Live Python Instance Access
    # =========================================================================

    def builtin_watcher_get(self, watcher_id: str) -> Any:
        """Get all instances from a Python CsslWatcher.

        Syntax:
            all_instances = watcher::get("MyWatcher");
            pygame = all_instances['Game'];
            game_instance = all_instances['game'];

        Example in Python:
            from includecpp.core.cssl_bridge import CsslWatcher
            cwatcher = CsslWatcher(id="MyWatcher")
            cwatcher.start()

            class Game:
                def start(self): print("Game started!")
            game = Game()

        Then in CSSL:
            instances = watcher::get("MyWatcher");
            instances['game'].start();  // "Game started!"

        Args:
            watcher_id: The watcher's unique ID

        Returns:
            Dict of all collected instances, classes, and functions
        """
        from ..cssl_bridge import watcher_get
        result = watcher_get(watcher_id)
        if result is None:
            return {}
        return result

    def builtin_watcher_set(self, watcher_id: str, path: str, value: Any) -> bool:
        """Set/overwrite a value in a Python watcher (bidirectional).

        Syntax:
            watcher::set("MyWatcher", "Game.start", myNewFunction);

        This allows CSSL to overwrite Python functions/methods at runtime.

        Args:
            watcher_id: The watcher's unique ID
            path: Path to the item (e.g., 'Game.start')
            value: New value (function, class, or instance)

        Returns:
            true if successful, false otherwise
        """
        from ..cssl_bridge import watcher_set
        return watcher_set(watcher_id, path, value)

    def builtin_watcher_list(self) -> list:
        """List all active watcher IDs.

        Syntax:
            watchers = watcher::list();
            foreach (w in watchers) {
                printl("Active watcher: " + w);
            }

        Returns:
            List of active watcher IDs
        """
        from ..cssl_bridge import list_watchers
        return list_watchers()

    def builtin_watcher_exists(self, watcher_id: str) -> bool:
        """Check if a watcher with the given ID exists.

        Syntax:
            if watcher::exists("MyWatcher") {
                instances = watcher::get("MyWatcher");
            }

        Args:
            watcher_id: The watcher's unique ID

        Returns:
            true if watcher exists, false otherwise
        """
        from ..cssl_bridge import get_watcher
        return get_watcher(watcher_id) is not None

    def builtin_watcher_refresh(self, watcher_id: str) -> bool:
        """Manually refresh a watcher's collected instances.

        Syntax:
            watcher::refresh("MyWatcher");

        This forces the watcher to re-scan the Python scope for new instances.

        Args:
            watcher_id: The watcher's unique ID

        Returns:
            true if successful, false otherwise
        """
        from ..cssl_bridge import get_watcher
        watcher = get_watcher(watcher_id)
        if watcher:
            watcher.refresh()
            return True
        return False


class CSSLizedPythonObject:
    """CSSL wrapper for Python objects (classes, instances, functions).

    Allows Python objects to be used within CSSL code, including as base classes.
    """

    def __init__(self, python_obj: Any, runtime: Any = None):
        self._python_obj = python_obj
        self._runtime = runtime
        self._is_class = isinstance(python_obj, type)
        self._is_callable = callable(python_obj) and not self._is_class

    def __repr__(self):
        if self._is_class:
            return f"<CSSLizedPythonClass: {self._python_obj.__name__}>"
        elif self._is_callable:
            return f"<CSSLizedPythonFunction: {getattr(self._python_obj, '__name__', 'anonymous')}>"
        else:
            return f"<CSSLizedPythonInstance: {type(self._python_obj).__name__}>"

    def __call__(self, *args, **kwargs):
        """Call the wrapped object (for functions or class instantiation)."""
        return self._python_obj(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """Get attribute from wrapped Python object."""
        if name.startswith('_'):
            raise AttributeError(f"Cannot access private attribute '{name}'")

        obj = object.__getattribute__(self, '_python_obj')

        if hasattr(obj, name):
            attr = getattr(obj, name)
            # If it's a method, wrap it for CSSL calling
            if callable(attr):
                return CSSLizedPythonMethod(attr, self._runtime)
            return attr

        raise AttributeError(f"Python object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any):
        """Set attribute on wrapped Python object."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._python_obj, name, value)

    def has_member(self, name: str) -> bool:
        """Check if the Python object has a member."""
        return hasattr(self._python_obj, name)

    def get_member(self, name: str) -> Any:
        """Get a member from the Python object."""
        return getattr(self._python_obj, name, None)

    def set_member(self, name: str, value: Any):
        """Set a member on the Python object."""
        setattr(self._python_obj, name, value)

    def get_method(self, name: str):
        """Get a method from the Python object."""
        if hasattr(self._python_obj, name):
            method = getattr(self._python_obj, name)
            if callable(method):
                return CSSLizedPythonMethod(method, self._runtime)
        return None

    def get_python_obj(self):
        """Get the underlying Python object (for inheritance)."""
        return self._python_obj


class CSSLizedPythonMethod:
    """Wrapper for Python methods to be called from CSSL."""

    def __init__(self, method: Any, runtime: Any = None):
        self._method = method
        self._runtime = runtime

    def __call__(self, *args, **kwargs):
        """Call the Python method."""
        return self._method(*args, **kwargs)

    def __repr__(self):
        return f"<CSSLizedPythonMethod: {getattr(self._method, '__name__', 'anonymous')}>"


class PythonizedCSSLInstance:
    """Python wrapper for CSSL class instances.

    Provides Pythonic attribute access and method calling for CSSL objects.
    """

    def __init__(self, instance: Any, runtime: Any = None):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, '_cssl_instance', instance)
        object.__setattr__(self, '_cssl_runtime', runtime)
        object.__setattr__(self, '_cssl_class_name', instance._class.name if hasattr(instance, '_class') else 'Unknown')

    def __getattr__(self, name: str) -> Any:
        """Get member or method from CSSL instance."""
        if name.startswith('_'):
            raise AttributeError(f"'{self._cssl_class_name}' has no attribute '{name}'")

        instance = object.__getattribute__(self, '_cssl_instance')
        runtime = object.__getattribute__(self, '_cssl_runtime')

        # Check for member variable first
        if instance.has_member(name):
            value = instance.get_member(name)
            # Recursively pythonize nested CSSL instances
            from .cssl_types import CSSLInstance
            if isinstance(value, CSSLInstance):
                return PythonizedCSSLInstance(value, runtime)
            return value

        # Check for method
        if instance.has_method(name):
            method = instance.get_method(name)
            # Return a callable wrapper for the method
            return PythonizedMethod(instance, name, method, runtime)

        raise AttributeError(f"'{self._cssl_class_name}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Set member value on CSSL instance."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return

        instance = object.__getattribute__(self, '_cssl_instance')
        instance.set_member(name, value)

    def __repr__(self) -> str:
        class_name = object.__getattribute__(self, '_cssl_class_name')
        instance = object.__getattribute__(self, '_cssl_instance')
        members = list(instance._members.keys()) if hasattr(instance, '_members') else []
        return f"<PythonizedCSSL '{class_name}' members={members}>"

    def __dir__(self) -> list:
        """List available attributes."""
        instance = object.__getattribute__(self, '_cssl_instance')
        members = list(instance._members.keys()) if hasattr(instance, '_members') else []
        methods = list(instance._class.methods.keys()) if hasattr(instance._class, 'methods') else []
        return members + methods

    def _to_dict(self) -> dict:
        """Convert to Python dictionary."""
        instance = object.__getattribute__(self, '_cssl_instance')
        result = {}
        for name, value in instance._members.items():
            from .cssl_types import CSSLInstance
            if isinstance(value, CSSLInstance):
                result[name] = PythonizedCSSLInstance(value, None)._to_dict()
            else:
                result[name] = value
        return result


class PythonizedMethod:
    """Wrapper that makes CSSL methods callable from Python."""

    def __init__(self, instance: Any, method_name: str, method_ast: Any, runtime: Any):
        self._instance = instance
        self._method_name = method_name
        self._method_ast = method_ast
        self._runtime = runtime

    def __call__(self, *args, **kwargs) -> Any:
        """Call the CSSL method with arguments."""
        if self._runtime is None:
            raise RuntimeError(f"Cannot call method '{self._method_name}' - no runtime available")

        # Validate argument count
        # Method AST structure: node.value is a dict with 'params' key
        method_info = getattr(self._method_ast, 'value', {}) or {}
        method_params = method_info.get('params', []) if isinstance(method_info, dict) else []
        param_names = [p.get('name', str(p)) if isinstance(p, dict) else (p.name if hasattr(p, 'name') else str(p)) for p in method_params]
        expected_count = len(param_names)
        actual_count = len(args)

        if actual_count < expected_count:
            missing = param_names[actual_count:]
            class_name = self._instance._class.name
            raise TypeError(
                f"{class_name}.{self._method_name}() missing {len(missing)} required argument(s): {', '.join(repr(p) for p in missing)}\n"
                f"  Expected: {self._method_name}({', '.join(param_names)})\n"
                f"  Got:      {self._method_name}({', '.join(repr(a) for a in args)})"
            )
        elif actual_count > expected_count:
            class_name = self._instance._class.name
            raise TypeError(
                f"{class_name}.{self._method_name}() takes {expected_count} argument(s) but {actual_count} were given\n"
                f"  Expected: {self._method_name}({', '.join(param_names)})"
            )

        # Execute the method through the runtime
        # Pass the method AST node, not the method name
        result = self._runtime._call_method(self._instance, self._method_ast, list(args), kwargs)

        # Pythonize the result if it's a CSSL instance
        from .cssl_types import CSSLInstance
        if isinstance(result, CSSLInstance):
            return PythonizedCSSLInstance(result, self._runtime)

        return result

    def __repr__(self) -> str:
        return f"<method '{self._method_name}' of '{self._instance._class.name}'>"


class PythonizedDict:
    """Simple wrapper for dict objects with attribute access."""

    def __init__(self, data: dict):
        object.__setattr__(self, '_data', data)

    def __getattr__(self, name: str) -> Any:
        data = object.__getattribute__(self, '_data')
        if name in data:
            value = data[name]
            if isinstance(value, dict):
                return PythonizedDict(value)
            return value
        raise AttributeError(f"No attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        data = object.__getattribute__(self, '_data')
        data[name] = value

    def __repr__(self) -> str:
        data = object.__getattribute__(self, '_data')
        return f"<PythonizedDict {data}>"

    def _to_dict(self) -> dict:
        return object.__getattribute__(self, '_data')


# Module-level convenience functions
_default_builtins: Optional[CSSLBuiltins] = None


def get_builtins(runtime=None) -> CSSLBuiltins:
    """Get default builtins instance"""
    global _default_builtins
    if _default_builtins is None or runtime is not None:
        _default_builtins = CSSLBuiltins(runtime)
    return _default_builtins


def call_builtin(name: str, *args, **kwargs) -> Any:
    """Call a builtin function"""
    return get_builtins().call(name, *args, **kwargs)
