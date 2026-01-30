"""
CSSL Syntax Highlighting v4.6.4

Provides syntax highlighting for CSSL code.
Can be used with:
- PyQt5/6 QSyntaxHighlighter
- VSCode/TextMate grammar export
- Terminal ANSI colors
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto
import re


class TokenCategory(Enum):
    """Categories for syntax highlighting"""
    KEYWORD = auto()          # service-init, struct, define, if, while, etc.
    BUILTIN = auto()          # print, len, typeof, etc.
    OPERATOR = auto()         # <==, ==>, ->, <-, +, -, etc.
    STRING = auto()           # "string" or 'string'
    STRING_INTERP = auto()    # <variable> in strings
    F_STRING = auto()         # f"string" or f'string' - v4.6.3
    F_STRING_INTERP = auto()  # {var} in f-strings - v4.6.3
    NUMBER = auto()           # 123, 45.67
    COMMENT = auto()          # # comment or // comment
    MODULE_REF = auto()       # @Module, @VSRAM, @Desktop
    SELF_REF = auto()         # s@StructName, s@Backend.Loop
    GLOBAL_REF = auto()       # r@globalVar
    THIS_REF = auto()         # this->member
    SNAPSHOT_REF = auto()     # %varName - snapshot reference (v4.8.8)
    IDENTIFIER = auto()       # variable names
    PROPERTY = auto()         # service-name:, service-version:
    BOOLEAN = auto()          # True, False, true, false
    NULL = auto()             # null, None
    PACKAGE_KW = auto()       # package, package-includes
    TYPE_LITERAL = auto()     # list, dict
    TYPE_CONTAINER = auto()   # datastruct, vector, stack, etc.
    # v4.1.0: Multi-language support
    SUPPORTS_KW = auto()      # supports keyword (magenta)
    LIBINCLUDE_KW = auto()    # libinclude (yellow/gold)
    LANG_PREFIX = auto()      # Language prefix before $ (cyan): cpp$, py$, java$
    LANG_INSTANCE = auto()    # Instance name after $ (orange): cpp$ClassName
    # v4.6.0: C++ execution control
    NATIVE_KW = auto()        # native keyword (cyan/bright) - forces C++ execution
    # v4.6.5: Python execution control (opposite of native)
    UNATIVE_KW = auto()       # unative keyword (orange) - forces Python execution
    # v4.6.2: Dunder variables
    DUNDER_VAR = auto()       # __name__ style variables (aggressive magenta)
    # Function categories
    FUNCTION_OUTPUT = auto()
    FUNCTION_TYPE = auto()
    FUNCTION_STRING = auto()
    FUNCTION_LIST = auto()
    FUNCTION_DICT = auto()
    FUNCTION_MATH = auto()
    FUNCTION_TIME = auto()
    FUNCTION_FILE = auto()
    FUNCTION_JSON = auto()
    FUNCTION_REGEX = auto()
    FUNCTION_HASH = auto()
    FUNCTION_UTILITY = auto()
    FUNCTION_SYSTEM = auto()
    FUNCTION_NAMESPACE = auto()


@dataclass
class HighlightRule:
    """Rule for syntax highlighting"""
    pattern: str
    category: TokenCategory
    group: int = 0  # Regex group to highlight


# CSSL Keywords - Complete list
KEYWORDS = {
    # Service structure
    'service-init', 'service-run', 'service-include',
    # Definitions
    'struct', 'define', 'main', 'class', 'constr', 'extends', 'overwrites', 'new', 'super', 'enum',
    # Control flow
    'if', 'else', 'elif', 'while', 'for', 'foreach', 'in', 'range',
    'switch', 'case', 'default', 'break', 'continue', 'return',
    # Exception handling
    'try', 'catch', 'finally', 'throw',
    # Logical operators
    'and', 'or', 'not',
    # Async/Event
    'start', 'stop', 'wait_for', 'on_event', 'emit_event', 'await',
    # Package & Import
    'package', 'package-includes', 'exec', 'as', 'global', 'include', 'get', 'payload',
}

# v4.1.0: Multi-language keywords with special highlighting
MULTI_LANG_KEYWORDS = {'supports', 'libinclude'}

# v4.6.0: C++ execution control keyword
NATIVE_KEYWORD = {'native'}  # Forces C++ execution (no Python fallback)
# v4.6.5: Python execution control keyword (opposite of native)
UNATIVE_KEYWORD = {'unative'}  # Forces Python execution (no C++)

# v4.1.0: Language identifiers for cross-language instance access
LANGUAGE_IDS = {'cpp', 'py', 'python', 'java', 'csharp', 'js', 'javascript'}

# Package-related keywords for special highlighting
PACKAGE_KEYWORDS = {'package', 'package-includes'}

# Function modifiers
FUNCTION_MODIFIERS = {
    'undefined', 'open', 'meta', 'super', 'closed', 'private', 'virtual',
    'sqlbased', 'const', 'public', 'static', 'shuffled', 'embedded',
    'secure', 'callable',  # v4.8.8: Constructor modifiers
}

# Type keywords
TYPE_KEYWORDS = {
    'int', 'string', 'float', 'bool', 'void', 'json', 'dynamic', 'list', 'dict', 'map', 'queue',
}

# Container types
TYPE_CONTAINERS = {
    'datastruct', 'dataspace', 'shuffled', 'iterator', 'combo',
    'vector', 'stack', 'array', 'openquote', 'structure', 'bytearrayed',
    # v4.8.4: C++ I/O types
    'fstream', 'ifstream', 'ofstream', 'pipe',
}

# CSSL Built-in Functions - Complete list organized by category
BUILTINS_OUTPUT = {
    'print', 'println', 'printl', 'debug', 'error', 'warn', 'log', 'input', 'encode',
    # v4.8.4: C++ I/O streams
    'cout', 'cin', 'cerr', 'clog', 'endl', 'flush', 'getline',
}

BUILTINS_TYPE = {'typeof', 'isinstance', 'isint', 'isfloat', 'isstr', 'isbool', 'islist', 'isdict', 'isnull', 'isavailable'}

BUILTINS_STRING = {
    'len', 'upper', 'lower', 'trim', 'ltrim', 'rtrim', 'split', 'join', 'replace', 'substr',
    'contains', 'startswith', 'endswith', 'format', 'concat', 'repeat', 'reverse',
    'indexof', 'lastindexof', 'padleft', 'padright', 'sprintf', 'chars', 'ord', 'chr',
    'capitalize', 'title', 'swapcase', 'center', 'zfill', 'isalpha', 'isdigit', 'isalnum', 'isspace',
}

BUILTINS_LIST = {
    'push', 'pop', 'shift', 'unshift', 'slice', 'sort', 'rsort', 'unique', 'flatten',
    'filter', 'map', 'reduce', 'find', 'findindex', 'every', 'some', 'enumerate', 'zip',
    'reversed', 'sorted', 'count', 'first', 'last', 'take', 'drop', 'chunk', 'groupby', 'shuffle', 'sample',
}

BUILTINS_DICT = {'keys', 'values', 'items', 'haskey', 'getkey', 'setkey', 'delkey', 'merge', 'update', 'fromkeys', 'invert', 'pick', 'omit'}

BUILTINS_MATH = {
    'abs', 'min', 'max', 'sum', 'avg', 'round', 'floor', 'ceil', 'pow', 'sqrt', 'mod',
    'random', 'randint', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'exp', 'radians', 'degrees', 'log10',
}

BUILTINS_TIME = {'now', 'timestamp', 'sleep', 'date', 'time', 'datetime', 'strftime', 'delay', 'CurrentTime'}

BUILTINS_FILE = {
    'pathexists', 'isfile', 'isdir', 'basename', 'dirname', 'joinpath', 'splitpath', 'abspath', 'normpath',
    'read', 'readline', 'write', 'writeline', 'readfile', 'writefile', 'appendfile', 'readlines',
    'listdir', 'makedirs', 'removefile', 'removedir', 'copyfile', 'movefile', 'filesize',
    'Listdir', 'ReadFile', 'WriteFile',
}

BUILTINS_JSON = {'tojson', 'fromjson'}

BUILTINS_REGEX = {'match', 'search', 'findall', 'sub'}

BUILTINS_HASH = {'md5', 'sha1', 'sha256'}

BUILTINS_UTILITY = {
    'copy', 'deepcopy', 'assert', 'exit', 'env', 'setenv', 'clear', 'cls', 'color', 'pyimport', 'range',
    # v4.8.4: C++ import and operations
    'cppimport', 'include', 'sizeof', 'memcpy', 'memset', 'pipe', 'contains_fast',
    # C++ stream manipulators
    'setprecision', 'setw', 'setfill', 'fixed', 'scientific',
    # v4.8.8: Snapshot functions
    'snapshot', 'get_snapshot', 'has_snapshot', 'clear_snapshot', 'clear_snapshots', 'list_snapshots', 'restore_snapshot',
}

BUILTINS_SYSTEM = {'createcmd', 'signal', 'appexec', 'initpy', 'initsh', 'wait_for_booted', 'emit', 'cso_root', 'isLinux', 'isWindows', 'isMac'}

# v4.6.5: Color and style functions for f-strings
BUILTINS_COLOR = {
    # Named colors
    'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white', 'black',
    # Bright variants
    'bright_red', 'bright_green', 'bright_blue', 'bright_yellow', 'bright_cyan', 'bright_magenta', 'bright_white',
    # RGB custom color
    'rgb',
    # Background colors
    'bg_red', 'bg_green', 'bg_blue', 'bg_yellow', 'bg_cyan', 'bg_magenta', 'bg_white', 'bg_black', 'bg_rgb',
    # Style functions
    'bold', 'italic', 'cursive', 'underline', 'dim', 'blink', 'reverse', 'strikethrough', 'reset',
}

BUILTINS_CONSTRUCTOR = {
    'datastruct', 'shuffled', 'iterator', 'combo', 'dataspace', 'openquote', 'OpenFind', 'vector', 'array', 'stack',
    # v4.8.4: C++ I/O constructors
    'fstream', 'ifstream', 'ofstream', 'struct',
}

# Namespace functions
NAMESPACE_JSON = {'json::read', 'json::write', 'json::parse', 'json::stringify', 'json::pretty', 'json::keys', 'json::values', 'json::get', 'json::set', 'json::has', 'json::merge'}
NAMESPACE_INSTANCE = {'instance::getMethods', 'instance::getClasses', 'instance::getVars', 'instance::getAll', 'instance::call', 'instance::has', 'instance::type', 'instance::exists'}
NAMESPACE_PYTHON = {'python::pythonize', 'python::wrap', 'python::export', 'python::csslize', 'python::import',
                    'python::param_get', 'python::param_return', 'python::param_count',
                    'python::param_all', 'python::param_has'}
# v4.6.5: Watcher namespace for live Python instance access
NAMESPACE_WATCHER = {'watcher::get', 'watcher::set', 'watcher::list', 'watcher::exists', 'watcher::refresh'}

# Combined builtins for backwards compatibility
BUILTINS = (
    BUILTINS_OUTPUT | BUILTINS_TYPE | BUILTINS_STRING | BUILTINS_LIST | BUILTINS_DICT |
    BUILTINS_MATH | BUILTINS_TIME | BUILTINS_FILE | BUILTINS_JSON | BUILTINS_REGEX |
    BUILTINS_HASH | BUILTINS_UTILITY | BUILTINS_SYSTEM | BUILTINS_CONSTRUCTOR | BUILTINS_COLOR
)


class CSSLSyntaxRules:
    """Collection of syntax highlighting rules for CSSL"""

    @staticmethod
    def get_rules() -> List[HighlightRule]:
        """Get all highlighting rules in priority order"""
        rules = []

        # Comments (highest priority - should match first)
        rules.append(HighlightRule(pattern=r'#[^\n]*', category=TokenCategory.COMMENT))
        rules.append(HighlightRule(pattern=r'//[^\n]*', category=TokenCategory.COMMENT))
        rules.append(HighlightRule(pattern=r'/\*[\s\S]*?\*/', category=TokenCategory.COMMENT))

        # F-strings (must be before regular strings) - v4.6.3
        rules.append(HighlightRule(pattern=r'f"(?:[^"\\]|\\.)*"', category=TokenCategory.F_STRING))
        rules.append(HighlightRule(pattern=r"f'(?:[^'\\]|\\.)*'", category=TokenCategory.F_STRING))

        # F-string interpolation {var} - v4.6.3
        rules.append(HighlightRule(pattern=r'\{[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\}', category=TokenCategory.F_STRING_INTERP))

        # Strings
        rules.append(HighlightRule(pattern=r'"(?:[^"\\]|\\.)*"', category=TokenCategory.STRING))
        rules.append(HighlightRule(pattern=r"'(?:[^'\\]|\\.)*'", category=TokenCategory.STRING))
        rules.append(HighlightRule(pattern=r'`[^`]*`', category=TokenCategory.STRING))  # Raw strings

        # String interpolation <variable> in strings
        rules.append(HighlightRule(pattern=r'<[A-Za-z_][A-Za-z0-9_]*>', category=TokenCategory.STRING_INTERP))

        # Package keywords (special highlighting)
        rules.append(HighlightRule(pattern=r'\b(package|package-includes)\b', category=TokenCategory.PACKAGE_KW))

        # v4.1.0: Multi-language support keywords
        rules.append(HighlightRule(pattern=r'\bsupports\b', category=TokenCategory.SUPPORTS_KW))
        rules.append(HighlightRule(pattern=r'\blibinclude\b', category=TokenCategory.LIBINCLUDE_KW))

        # v4.6.0: 'native' keyword (cyan/bright) - forces C++ execution
        rules.append(HighlightRule(pattern=r'\bnative\b', category=TokenCategory.NATIVE_KW))
        # v4.6.5: 'unative' keyword (orange) - forces Python execution
        rules.append(HighlightRule(pattern=r'\bunative\b', category=TokenCategory.UNATIVE_KW))

        # v4.6.2: Dunder variables (__name__, __this_stat_s__, __s__, etc.)
        rules.append(HighlightRule(pattern=r'\b__[A-Za-z_][A-Za-z0-9_]*__\b', category=TokenCategory.DUNDER_VAR))

        # v4.1.0: Language$Instance patterns (cpp$ClassName, py$Object)
        rules.append(HighlightRule(pattern=r'\b(cpp|py|python|java|csharp|js|javascript)\$', category=TokenCategory.LANG_PREFIX, group=1))
        rules.append(HighlightRule(pattern=r'\b(?:cpp|py|python|java|csharp|js|javascript)\$([A-Za-z_][A-Za-z0-9_]*)', category=TokenCategory.LANG_INSTANCE, group=1))

        # This references
        rules.append(HighlightRule(pattern=r'\bthis->\w+', category=TokenCategory.THIS_REF))
        rules.append(HighlightRule(pattern=r'\bthis\b', category=TokenCategory.THIS_REF))

        # Self-references (s@Name, s@Backend.Loop)
        rules.append(HighlightRule(pattern=r's@[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', category=TokenCategory.SELF_REF))

        # Global references (r@name)
        rules.append(HighlightRule(pattern=r'r@[A-Za-z_][A-Za-z0-9_]*', category=TokenCategory.GLOBAL_REF))

        # v4.8.8: Snapshot references (%name) - access snapshotted values
        rules.append(HighlightRule(pattern=r'%[A-Za-z_][A-Za-z0-9_]*', category=TokenCategory.SNAPSHOT_REF))

        # Module references (@Module, @VSRAM.Read)
        rules.append(HighlightRule(pattern=r'@[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', category=TokenCategory.MODULE_REF))

        # Properties (key: value in service-init)
        rules.append(HighlightRule(
            pattern=r'\b(service-name|service-version|service-author|service-description|execution|executation)\s*:',
            category=TokenCategory.PROPERTY, group=1
        ))

        # Function modifiers
        modifier_pattern = r'\b(' + '|'.join(re.escape(m) for m in FUNCTION_MODIFIERS) + r')\b'
        rules.append(HighlightRule(pattern=modifier_pattern, category=TokenCategory.KEYWORD))

        # Type containers
        container_pattern = r'\b(' + '|'.join(re.escape(t) for t in TYPE_CONTAINERS) + r')\b'
        rules.append(HighlightRule(pattern=container_pattern, category=TokenCategory.TYPE_CONTAINER))

        # Type keywords
        type_pattern = r'\b(' + '|'.join(re.escape(t) for t in TYPE_KEYWORDS) + r')\b'
        rules.append(HighlightRule(pattern=type_pattern, category=TokenCategory.TYPE_LITERAL))

        # Keywords
        keyword_pattern = r'\b(' + '|'.join(re.escape(k) for k in KEYWORDS) + r')\b'
        rules.append(HighlightRule(pattern=keyword_pattern, category=TokenCategory.KEYWORD))

        # Namespace functions
        rules.append(HighlightRule(pattern=r'\bjson::(read|write|parse|stringify|pretty|keys|values|get|set|has|merge)\b', category=TokenCategory.FUNCTION_NAMESPACE))
        rules.append(HighlightRule(pattern=r'\binstance::(getMethods|getClasses|getVars|getAll|call|has|type|exists)\b', category=TokenCategory.FUNCTION_NAMESPACE))
        rules.append(HighlightRule(pattern=r'\bpython::(pythonize|wrap|export|csslize|import|param_get|param_return|param_count|param_all|param_has)\b', category=TokenCategory.FUNCTION_NAMESPACE))

        # Builtin functions by category (require parenthesis)
        def add_builtin_rules(builtins, category):
            pattern = r'\b(' + '|'.join(re.escape(b) for b in builtins) + r')\s*\('
            rules.append(HighlightRule(pattern=pattern, category=category, group=1))

        add_builtin_rules(BUILTINS_OUTPUT, TokenCategory.FUNCTION_OUTPUT)
        add_builtin_rules(BUILTINS_TYPE, TokenCategory.FUNCTION_TYPE)
        add_builtin_rules(BUILTINS_STRING, TokenCategory.FUNCTION_STRING)
        add_builtin_rules(BUILTINS_LIST, TokenCategory.FUNCTION_LIST)
        add_builtin_rules(BUILTINS_DICT, TokenCategory.FUNCTION_DICT)
        add_builtin_rules(BUILTINS_MATH, TokenCategory.FUNCTION_MATH)
        add_builtin_rules(BUILTINS_TIME, TokenCategory.FUNCTION_TIME)
        add_builtin_rules(BUILTINS_FILE, TokenCategory.FUNCTION_FILE)
        add_builtin_rules(BUILTINS_JSON, TokenCategory.FUNCTION_JSON)
        add_builtin_rules(BUILTINS_REGEX, TokenCategory.FUNCTION_REGEX)
        add_builtin_rules(BUILTINS_HASH, TokenCategory.FUNCTION_HASH)
        add_builtin_rules(BUILTINS_UTILITY, TokenCategory.FUNCTION_UTILITY)
        add_builtin_rules(BUILTINS_SYSTEM, TokenCategory.FUNCTION_SYSTEM)
        add_builtin_rules(BUILTINS_CONSTRUCTOR, TokenCategory.BUILTIN)

        # Boolean literals
        rules.append(HighlightRule(pattern=r'\b(True|False|true|false)\b', category=TokenCategory.BOOLEAN))

        # Null literals
        rules.append(HighlightRule(pattern=r'\b(null|None|none|nil)\b', category=TokenCategory.NULL))

        # Numbers
        rules.append(HighlightRule(pattern=r'\b0[xX][0-9a-fA-F]+\b', category=TokenCategory.NUMBER))  # Hex
        rules.append(HighlightRule(pattern=r'\b\d+\.?\d*\b', category=TokenCategory.NUMBER))

        # Special operators
        rules.append(HighlightRule(pattern=r'\+<<=|==>>\+|-<<=|==>>-|<<=|=>>|<==|==>|->', category=TokenCategory.OPERATOR))
        rules.append(HighlightRule(pattern=r'==|!=|<=|>=|<|>', category=TokenCategory.OPERATOR))
        rules.append(HighlightRule(pattern=r'\+\+|--|\+=|-=|\*=|/=|%=', category=TokenCategory.OPERATOR))
        rules.append(HighlightRule(pattern=r'::', category=TokenCategory.OPERATOR))

        return rules


# Default color schemes
class ColorScheme:
    """Color scheme for syntax highlighting"""

    # CSSL Theme (Orange accent, dark background)
    CSSL_THEME = {
        TokenCategory.KEYWORD: '#508cff',           # Blue
        TokenCategory.BUILTIN: '#ff8c00',           # Orange
        TokenCategory.OPERATOR: '#c8c8d2',          # Light gray
        TokenCategory.STRING: '#50c878',            # Green
        TokenCategory.STRING_INTERP: '#f1fa8c',     # Yellow for interpolation
        TokenCategory.F_STRING: '#98c379',          # Bright green for f-strings
        TokenCategory.F_STRING_INTERP: '#e5c07b',   # Gold for {var} in f-strings
        TokenCategory.NUMBER: '#f0c040',            # Yellow
        TokenCategory.COMMENT: '#707080',           # Gray
        TokenCategory.MODULE_REF: '#ff8c00',        # Orange
        TokenCategory.SELF_REF: '#60c8dc',          # Cyan
        TokenCategory.GLOBAL_REF: '#ff79c6',        # Pink
        TokenCategory.THIS_REF: '#bd93f9',          # Purple
        TokenCategory.SNAPSHOT_REF: '#ffd700',      # Gold - for %snapshot refs (v4.8.8)
        TokenCategory.IDENTIFIER: '#f0f0f5',        # White
        TokenCategory.PROPERTY: '#c8a8ff',          # Purple
        TokenCategory.BOOLEAN: '#ff8c00',           # Orange
        TokenCategory.NULL: '#ff6464',              # Red
        TokenCategory.PACKAGE_KW: '#bd93f9',        # Purple for package
        TokenCategory.TYPE_LITERAL: '#8be9fd',      # Cyan for type literals
        TokenCategory.TYPE_CONTAINER: '#50fa7b',    # Green for containers
        # v4.1.0: Multi-language support colors
        TokenCategory.SUPPORTS_KW: '#ff79c6',       # Magenta/Pink for 'supports'
        TokenCategory.LIBINCLUDE_KW: '#f1fa8c',     # Yellow/Gold for 'libinclude'
        TokenCategory.LANG_PREFIX: '#8be9fd',       # Cyan for language prefix (cpp$)
        TokenCategory.LANG_INSTANCE: '#ffb86c',     # Orange for instance name ($ClassName)
        # v4.6.0: C++ execution control
        TokenCategory.NATIVE_KW: '#50fa7b',         # Green for 'native' (C++ forced)
        # v4.6.5: Python execution control
        TokenCategory.UNATIVE_KW: '#ff8c00',        # Orange for 'unative' (Python forced)
        # v4.6.2: Dunder variables
        TokenCategory.DUNDER_VAR: '#ff00ff',        # Aggressive magenta for __name__ vars
        # Function categories
        TokenCategory.FUNCTION_OUTPUT: '#ff8c00',   # Orange
        TokenCategory.FUNCTION_TYPE: '#8be9fd',     # Cyan
        TokenCategory.FUNCTION_STRING: '#50c878',   # Green
        TokenCategory.FUNCTION_LIST: '#ff8c00',     # Orange
        TokenCategory.FUNCTION_DICT: '#ffb86c',     # Light orange
        TokenCategory.FUNCTION_MATH: '#f0c040',     # Yellow
        TokenCategory.FUNCTION_TIME: '#bd93f9',     # Purple
        TokenCategory.FUNCTION_FILE: '#ff79c6',     # Pink
        TokenCategory.FUNCTION_JSON: '#8be9fd',     # Cyan
        TokenCategory.FUNCTION_REGEX: '#50fa7b',    # Green
        TokenCategory.FUNCTION_HASH: '#ff6464',     # Red
        TokenCategory.FUNCTION_UTILITY: '#f0f0f5',  # White
        TokenCategory.FUNCTION_SYSTEM: '#ff8c00',   # Orange
        TokenCategory.FUNCTION_NAMESPACE: '#bd93f9', # Purple
    }

    # Light theme variant
    LIGHT_THEME = {
        TokenCategory.KEYWORD: '#0000ff',           # Blue
        TokenCategory.BUILTIN: '#c65d00',           # Dark orange
        TokenCategory.OPERATOR: '#444444',          # Dark gray
        TokenCategory.STRING: '#008000',            # Green
        TokenCategory.STRING_INTERP: '#b8860b',     # DarkGoldenrod
        TokenCategory.F_STRING: '#2e7d32',          # Dark green for f-strings
        TokenCategory.F_STRING_INTERP: '#bf8c00',   # Dark gold for {var} in f-strings
        TokenCategory.NUMBER: '#a06000',            # Brown
        TokenCategory.COMMENT: '#808080',           # Gray
        TokenCategory.MODULE_REF: '#c65d00',        # Dark orange
        TokenCategory.SELF_REF: '#008b8b',          # Dark cyan
        TokenCategory.GLOBAL_REF: '#d63384',        # Dark pink
        TokenCategory.THIS_REF: '#800080',          # Purple
        TokenCategory.SNAPSHOT_REF: '#b8860b',      # DarkGoldenrod - for %snapshot refs (v4.8.8)
        TokenCategory.IDENTIFIER: '#000000',        # Black
        TokenCategory.PROPERTY: '#800080',          # Purple
        TokenCategory.BOOLEAN: '#c65d00',           # Dark orange
        TokenCategory.NULL: '#ff0000',              # Red
        TokenCategory.PACKAGE_KW: '#8b008b',        # DarkMagenta
        TokenCategory.TYPE_LITERAL: '#008b8b',      # Dark cyan
        TokenCategory.TYPE_CONTAINER: '#198754',    # Green
        # v4.1.0: Multi-language support colors
        TokenCategory.SUPPORTS_KW: '#d63384',       # Dark Magenta
        TokenCategory.LIBINCLUDE_KW: '#b8860b',     # DarkGoldenrod
        TokenCategory.LANG_PREFIX: '#0d6efd',       # Blue
        TokenCategory.LANG_INSTANCE: '#fd7e14',     # Orange
        # v4.6.0: C++ execution control
        TokenCategory.NATIVE_KW: '#198754',         # Green
        # v4.6.5: Python execution control
        TokenCategory.UNATIVE_KW: '#c65d00',        # Dark Orange for 'unative'
        # v4.6.2: Dunder variables
        TokenCategory.DUNDER_VAR: '#c71585',        # MediumVioletRed for __name__ vars
        # Function categories (simplified for light theme)
        TokenCategory.FUNCTION_OUTPUT: '#c65d00',
        TokenCategory.FUNCTION_TYPE: '#008b8b',
        TokenCategory.FUNCTION_STRING: '#008000',
        TokenCategory.FUNCTION_LIST: '#c65d00',
        TokenCategory.FUNCTION_DICT: '#fd7e14',
        TokenCategory.FUNCTION_MATH: '#a06000',
        TokenCategory.FUNCTION_TIME: '#800080',
        TokenCategory.FUNCTION_FILE: '#d63384',
        TokenCategory.FUNCTION_JSON: '#008b8b',
        TokenCategory.FUNCTION_REGEX: '#198754',
        TokenCategory.FUNCTION_HASH: '#ff0000',
        TokenCategory.FUNCTION_UTILITY: '#000000',
        TokenCategory.FUNCTION_SYSTEM: '#c65d00',
        TokenCategory.FUNCTION_NAMESPACE: '#800080',
    }


def highlight_cssl(source: str, scheme: Dict[TokenCategory, str] = None) -> List[Tuple[int, int, str, TokenCategory]]:
    """
    Highlight CSSL source code.

    Args:
        source: CSSL source code
        scheme: Color scheme dict (defaults to CSSL_THEME)

    Returns:
        List of (start, end, color, category) tuples
    """
    if scheme is None:
        scheme = ColorScheme.CSSL_THEME

    highlights = []
    rules = CSSLSyntaxRules.get_rules()

    # Track which positions are already highlighted (for priority)
    highlighted_positions = set()

    for rule in rules:
        try:
            pattern = re.compile(rule.pattern)
            for match in pattern.finditer(source):
                if rule.group > 0 and rule.group <= len(match.groups()):
                    start = match.start(rule.group)
                    end = match.end(rule.group)
                else:
                    start = match.start()
                    end = match.end()

                # Check if position already highlighted
                pos_range = range(start, end)
                if any(p in highlighted_positions for p in pos_range):
                    continue

                # Add highlight
                color = scheme.get(rule.category, '#ffffff')
                highlights.append((start, end, color, rule.category))

                # Mark positions as highlighted
                highlighted_positions.update(pos_range)

        except re.error:
            continue

    # Sort by start position
    highlights.sort(key=lambda h: h[0])

    return highlights


def highlight_cssl_ansi(source: str) -> str:
    """
    Highlight CSSL source with ANSI terminal colors.

    Args:
        source: CSSL source code

    Returns:
        Source with ANSI color codes
    """
    # ANSI color codes
    ANSI_COLORS = {
        TokenCategory.KEYWORD: '\033[94m',          # Blue
        TokenCategory.BUILTIN: '\033[33m',          # Yellow/Orange
        TokenCategory.OPERATOR: '\033[37m',         # White
        TokenCategory.STRING: '\033[92m',           # Green
        TokenCategory.STRING_INTERP: '\033[93m',    # Yellow
        TokenCategory.F_STRING: '\033[92;1m',       # Bright Green for f-strings
        TokenCategory.F_STRING_INTERP: '\033[93;1m',# Bright Yellow for {var}
        TokenCategory.NUMBER: '\033[93m',           # Yellow
        TokenCategory.COMMENT: '\033[90m',          # Gray
        TokenCategory.MODULE_REF: '\033[33m',       # Yellow/Orange
        TokenCategory.SELF_REF: '\033[96m',         # Cyan
        TokenCategory.GLOBAL_REF: '\033[95m',       # Magenta
        TokenCategory.THIS_REF: '\033[95m',         # Magenta
        TokenCategory.IDENTIFIER: '\033[0m',        # Default
        TokenCategory.PROPERTY: '\033[95m',         # Magenta
        TokenCategory.BOOLEAN: '\033[33m',          # Yellow/Orange
        TokenCategory.NULL: '\033[91m',             # Red
        TokenCategory.PACKAGE_KW: '\033[95m',       # Magenta
        TokenCategory.TYPE_LITERAL: '\033[96m',     # Cyan
        TokenCategory.TYPE_CONTAINER: '\033[92m',   # Green
        # v4.1.0: Multi-language support colors
        TokenCategory.SUPPORTS_KW: '\033[95m',      # Magenta
        TokenCategory.LIBINCLUDE_KW: '\033[93m',    # Yellow
        TokenCategory.LANG_PREFIX: '\033[96m',      # Cyan
        TokenCategory.LANG_INSTANCE: '\033[33m',    # Orange/Yellow
        # v4.6.0: C++ execution control
        TokenCategory.NATIVE_KW: '\033[92m',        # Bright Green
        # v4.6.5: Python execution control
        TokenCategory.UNATIVE_KW: '\033[33m',       # Orange (Python forced)
        # v4.6.2: Dunder variables
        TokenCategory.DUNDER_VAR: '\033[95;1m',     # Bright Magenta (bold)
        # Function categories
        TokenCategory.FUNCTION_OUTPUT: '\033[33m',
        TokenCategory.FUNCTION_TYPE: '\033[96m',
        TokenCategory.FUNCTION_STRING: '\033[92m',
        TokenCategory.FUNCTION_LIST: '\033[33m',
        TokenCategory.FUNCTION_DICT: '\033[33m',
        TokenCategory.FUNCTION_MATH: '\033[93m',
        TokenCategory.FUNCTION_TIME: '\033[95m',
        TokenCategory.FUNCTION_FILE: '\033[95m',
        TokenCategory.FUNCTION_JSON: '\033[96m',
        TokenCategory.FUNCTION_REGEX: '\033[92m',
        TokenCategory.FUNCTION_HASH: '\033[91m',
        TokenCategory.FUNCTION_UTILITY: '\033[0m',
        TokenCategory.FUNCTION_SYSTEM: '\033[33m',
        TokenCategory.FUNCTION_NAMESPACE: '\033[95m',
    }
    RESET = '\033[0m'

    highlights = highlight_cssl(source, ColorScheme.CSSL_THEME)

    # Build highlighted string
    result = []
    last_end = 0

    for start, end, color, category in highlights:
        # Add unhighlighted text before this highlight
        if start > last_end:
            result.append(source[last_end:start])

        # Add highlighted text
        ansi_color = ANSI_COLORS.get(category, '')
        result.append(f"{ansi_color}{source[start:end]}{RESET}")
        last_end = end

    # Add remaining text
    if last_end < len(source):
        result.append(source[last_end:])

    return ''.join(result)


# PyQt5/6 Syntax Highlighter
def get_pyqt_highlighter():
    """
    Get a QSyntaxHighlighter class for CSSL.

    Returns:
        CSSLHighlighter class (requires PyQt5 or PyQt6)
    """
    try:
        from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
        from PyQt5.QtCore import QRegularExpression
    except ImportError:
        try:
            from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
            from PyQt6.QtCore import QRegularExpression
        except ImportError:
            return None

    class CSSLHighlighter(QSyntaxHighlighter):
        """Syntax highlighter for CSSL code in Qt editors"""

        def __init__(self, parent=None):
            super().__init__(parent)
            self._rules = []
            self._setup_rules()

        def _setup_rules(self):
            """Setup highlighting rules"""
            scheme = ColorScheme.CSSL_THEME

            for rule in CSSLSyntaxRules.get_rules():
                fmt = QTextCharFormat()
                color = QColor(scheme.get(rule.category, '#ffffff'))
                fmt.setForeground(color)

                # Bold for keywords and builtins
                if rule.category in (TokenCategory.KEYWORD, TokenCategory.BUILTIN):
                    fmt.setFontWeight(QFont.Bold)

                # Italic for comments
                if rule.category == TokenCategory.COMMENT:
                    fmt.setFontItalic(True)

                self._rules.append((QRegularExpression(rule.pattern), fmt, rule.group))

        def highlightBlock(self, text):
            """Apply highlighting to a block of text"""
            for pattern, fmt, group in self._rules:
                match_iterator = pattern.globalMatch(text)
                while match_iterator.hasNext():
                    match = match_iterator.next()
                    if group > 0 and group <= match.lastCapturedIndex():
                        start = match.capturedStart(group)
                        length = match.capturedLength(group)
                    else:
                        start = match.capturedStart()
                        length = match.capturedLength()
                    self.setFormat(start, length, fmt)

    return CSSLHighlighter


# Export for external editors (TextMate/VSCode grammar format)
def export_textmate_grammar() -> dict:
    """
    Export CSSL syntax as TextMate grammar for VSCode.

    Returns:
        Dictionary suitable for JSON export as .tmLanguage.json
    """
    return {
        "scopeName": "source.cssl",
        "name": "CSSL",
        "fileTypes": ["cssl", "service"],
        "patterns": [
            {"name": "comment.line.cssl", "match": "#.*$"},
            {"name": "comment.line.double-slash.cssl", "match": "//.*$"},
            {"name": "comment.block.cssl", "begin": "/\\*", "end": "\\*/"},
            {"name": "string.quoted.double.cssl", "match": '"(?:[^"\\\\]|\\\\.)*"'},
            {"name": "string.quoted.single.cssl", "match": "'(?:[^'\\\\]|\\\\.)*'"},
            {"name": "string.quoted.raw.cssl", "begin": "`", "end": "`"},
            {"name": "keyword.control.supports.cssl", "match": "\\bsupports\\b"},
            {"name": "support.function.libinclude.cssl", "match": "\\blibinclude\\b"},
            {"name": "keyword.control.native.cssl", "match": "\\bnative\\b"},
            {
                "name": "variable.language.lang-instance.cssl",
                "match": "\\b(cpp|py|python|java|csharp|js|javascript)\\$([A-Za-z_][A-Za-z0-9_]*)",
                "captures": {
                    "1": {"name": "entity.name.type.language.cssl"},
                    "2": {"name": "variable.other.instance.cssl"}
                }
            },
            {"name": "variable.language.this.cssl", "match": "\\bthis->\\w+|\\bthis\\b"},
            {"name": "variable.other.self-reference.cssl", "match": "s@[A-Za-z_][A-Za-z0-9_]*(?:\\.[A-Za-z_][A-Za-z0-9_]*)*"},
            {"name": "variable.other.global-reference.cssl", "match": "r@[A-Za-z_][A-Za-z0-9_]*"},
            {"name": "variable.other.snapshot.cssl", "match": "%[A-Za-z_][A-Za-z0-9_]*"},
            {"name": "variable.other.module-reference.cssl", "match": "@[A-Za-z_][A-Za-z0-9_]*(?:\\.[A-Za-z_][A-Za-z0-9_]*)*"},
            {"name": "keyword.other.package.cssl", "match": "\\b(package|package-includes)\\b"},
            {"name": "storage.modifier.cssl", "match": "\\b(undefined|open|meta|super|closed|private|virtual|sqlbased|const|public|static|shuffled|embedded)\\b"},
            {"name": "storage.type.container.cssl", "match": "\\b(datastruct|dataspace|shuffled|iterator|combo|vector|stack|array|openquote|structure|bytearrayed)\\b"},
            {"name": "storage.type.cssl", "match": "\\b(int|string|float|bool|void|json|dynamic|list|dict|map|queue)\\b"},
            {"name": "keyword.control.cssl", "match": "\\b(service-init|service-run|service-include|struct|define|class|constr|if|else|elif|while|for|foreach|in|switch|case|default|break|continue|return|try|catch|finally|throw|await|extends|overwrites|global|as|exec|new|super|enum|main|start|stop|wait_for|on_event|emit_event|include|get|payload)\\b"},
            {"name": "keyword.operator.cssl", "match": "\\b(and|or|not)\\b"},
            {"name": "constant.language.cssl", "match": "\\b(True|False|true|false|null|None|none|nil)\\b"},
            {"name": "constant.numeric.hex.cssl", "match": "\\b0[xX][0-9a-fA-F]+\\b"},
            {"name": "constant.numeric.cssl", "match": "\\b\\d+\\.?\\d*\\b"},
            {"name": "keyword.operator.assignment.cssl", "match": "<==|==>|->|<-|::"},
            {"name": "support.function.namespace.cssl", "match": "\\b(json|instance|python)::\\w+\\b"},
        ]
    }


# Export public API
__all__ = [
    'TokenCategory', 'HighlightRule', 'CSSLSyntaxRules', 'ColorScheme',
    'highlight_cssl', 'highlight_cssl_ansi', 'get_pyqt_highlighter',
    'export_textmate_grammar',
    'KEYWORDS', 'BUILTINS', 'FUNCTION_MODIFIERS', 'TYPE_KEYWORDS', 'TYPE_CONTAINERS',
    'PACKAGE_KEYWORDS', 'MULTI_LANG_KEYWORDS', 'NATIVE_KEYWORD',
    'BUILTINS_OUTPUT', 'BUILTINS_TYPE', 'BUILTINS_STRING', 'BUILTINS_LIST',
    'BUILTINS_DICT', 'BUILTINS_MATH', 'BUILTINS_TIME', 'BUILTINS_FILE',
    'BUILTINS_JSON', 'BUILTINS_REGEX', 'BUILTINS_HASH', 'BUILTINS_UTILITY',
    'BUILTINS_SYSTEM', 'BUILTINS_CONSTRUCTOR',
]
