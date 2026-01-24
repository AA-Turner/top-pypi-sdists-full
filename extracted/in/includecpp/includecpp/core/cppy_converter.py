"""
CPPY Converter - Python <-> C++ bidirectional code conversion.
Full implementation with struct, class, function, template support.
Maximum stability version with comprehensive error handling.
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field


def _safe_arg(args: List[str], index: int, default: str = '0') -> str:
    """Safely get argument at index, returning default if not available."""
    if args and 0 <= index < len(args):
        return args[index]
    return default


def _safe_get(lst: List[Any], index: int, default: Any = None) -> Any:
    """Safely get element from list at index."""
    if lst and 0 <= index < len(lst):
        return lst[index]
    return default


# v3.3.22: Python reserved keywords - names that need escaping when used as identifiers
PYTHON_KEYWORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield'
}

# v3.4.1: C++ reserved words that need escaping when used as Python identifiers
# These are C++ types/keywords that are valid Python identifiers but confusing
CPP_RESERVED_WORDS = {
    # Primitive types
    'int', 'float', 'double', 'char', 'bool', 'void', 'auto',
    'short', 'long', 'signed', 'unsigned', 'wchar_t',
    # Type modifiers
    'const', 'static', 'virtual', 'volatile', 'mutable', 'extern',
    'register', 'inline', 'explicit', 'constexpr', 'consteval',
    # Access modifiers
    'public', 'private', 'protected',
    # Other keywords
    'template', 'typename', 'namespace', 'using', 'typedef',
    'struct', 'union', 'enum', 'sizeof', 'alignof', 'decltype',
    'new', 'delete', 'operator', 'friend', 'this',
    'throw', 'catch', 'noexcept', 'final', 'override',
}


def _escape_python_keyword(name: str) -> str:
    """Escape Python reserved keywords by adding underscore suffix.

    Example: 'class' -> 'class_', 'def' -> 'def_', 'import' -> 'import_'
    """
    if name in PYTHON_KEYWORDS:
        return name + '_'
    return name


def _escape_cpp_reserved(name: str) -> str:
    """Escape C++ reserved words when used as Python identifiers.

    Example: 'double' -> 'double_', 'int' -> 'int_', 'void' -> 'void_'
    v3.4.1: Prevents C++ type names from being used as Python function/variable names.
    """
    if name in CPP_RESERVED_WORDS:
        return name + '_'
    return name


def _escape_identifier(name: str) -> str:
    """Escape both Python keywords and C++ reserved words.

    Combines both escaping functions for comprehensive identifier safety.
    """
    name = _escape_python_keyword(name)
    name = _escape_cpp_reserved(name)
    return name


# Python type to C++ type mapping
PY_TO_CPP_TYPES = {
    'int': 'int',
    'float': 'double',
    'str': 'std::string',
    'bool': 'bool',
    'bytes': 'std::vector<uint8_t>',
    'bytearray': 'std::vector<uint8_t>',
    'None': 'void',
    'any': 'auto',
    'Any': 'auto',
    'object': 'py::object',
    'list': 'std::vector',
    'List': 'std::vector',
    'dict': 'std::unordered_map',
    'Dict': 'std::unordered_map',
    'set': 'std::unordered_set',
    'Set': 'std::unordered_set',
    'tuple': 'std::tuple',
    'Tuple': 'std::tuple',
    'Optional': 'std::optional',
    'Union': 'std::variant',
    'Callable': 'std::function',
}

# C++ type to Python type mapping
CPP_TO_PY_TYPES = {
    'int': 'int',
    'long': 'int',
    'long long': 'int',
    'short': 'int',
    'unsigned int': 'int',
    'unsigned long': 'int',
    'size_t': 'int',
    'float': 'float',
    'double': 'float',
    'bool': 'bool',
    'char': 'str',
    'std::string': 'str',
    'string': 'str',
    'void': 'None',
    'auto': 'Any',
    'std::vector': 'list',
    'vector': 'list',
    'std::map': 'dict',
    'std::unordered_map': 'dict',
    'map': 'dict',
    'std::set': 'set',
    'std::unordered_set': 'set',
    'set': 'set',
    'std::tuple': 'tuple',
    'tuple': 'tuple',
    'std::optional': 'Optional',
    'optional': 'Optional',
    'std::variant': 'Union',
    'std::function': 'Callable',
    'uint8_t': 'int',
    'int8_t': 'int',
    'uint16_t': 'int',
    'int16_t': 'int',
    'uint32_t': 'int',
    'int32_t': 'int',
    'uint64_t': 'int',
    'int64_t': 'int',
}

# Modules that are fully unconvertible (GUI frameworks, etc.)
UNCONVERTIBLE_MODULES = {
    'tkinter': 'GUI framework - no C++ equivalent',
    'tk': 'tkinter alias - no C++ equivalent',
    'PyQt5': 'GUI framework - use Qt C++ directly',
    'PyQt6': 'GUI framework - use Qt C++ directly',
    'PySide2': 'GUI framework - use Qt C++ directly',
    'PySide6': 'GUI framework - use Qt C++ directly',
    'pygame': 'Game library - no direct C++ equivalent',
    'kivy': 'GUI framework - no C++ equivalent',
    'wx': 'wxPython - use wxWidgets in C++',
    'curses': 'Terminal UI - use ncurses in C++',
    'turtle': 'Graphics - no C++ equivalent',
    'PIL': 'Image library - use OpenCV/stb_image',
    'pillow': 'Image library - use OpenCV/stb_image',
    'matplotlib': 'Plotting library - no direct equivalent',
    'numpy': 'Numerical library - use Eigen/Armadillo',
    'pandas': 'Data analysis - no direct equivalent',
    'scipy': 'Scientific computing - use specialized C++ libs',
    'sklearn': 'Machine learning - use specialized C++ libs',
    'tensorflow': 'ML framework - has C++ API',
    'torch': 'PyTorch - has libtorch C++ API',
    'flask': 'Web framework - no C++ equivalent',
    'django': 'Web framework - no C++ equivalent',
    'requests': 'HTTP library - use libcurl/cpp-httplib',
    'asyncio': 'Async library - use std::async/coroutines',
    'aiohttp': 'Async HTTP - use async C++ libs',
    'socket': 'Network sockets - use C socket API',
    'http': 'HTTP library - use cpp-httplib',
    'urllib': 'URL library - use libcurl',
    'multiprocessing': 'Process-based parallelism - use fork/spawn',
    'subprocess': 'Process execution - use system()/popen()',
    'logging': 'Logging - use spdlog/similar',
    'unittest': 'Testing - use gtest/catch2',
    'pytest': 'Testing - use gtest/catch2',
}

# Modules with partial C++ equivalent mappings
MODULE_CONVERSIONS = {
    # os module
    'os.getcwd': {'cpp': 'std::filesystem::current_path().string()', 'include': '<filesystem>'},
    'os.chdir': {'cpp': 'std::filesystem::current_path', 'include': '<filesystem>', 'pattern': 'std::filesystem::current_path({})'},
    'os.listdir': {'cpp': '_os_listdir', 'include': '<filesystem>'},
    'os.mkdir': {'cpp': 'std::filesystem::create_directory', 'include': '<filesystem>'},
    'os.makedirs': {'cpp': 'std::filesystem::create_directories', 'include': '<filesystem>'},
    'os.remove': {'cpp': 'std::filesystem::remove', 'include': '<filesystem>'},
    'os.rmdir': {'cpp': 'std::filesystem::remove', 'include': '<filesystem>'},
    'os.rename': {'cpp': 'std::filesystem::rename', 'include': '<filesystem>'},
    'os.path.exists': {'cpp': 'std::filesystem::exists', 'include': '<filesystem>'},
    'os.path.isfile': {'cpp': 'std::filesystem::is_regular_file', 'include': '<filesystem>'},
    'os.path.isdir': {'cpp': 'std::filesystem::is_directory', 'include': '<filesystem>'},
    'os.path.join': {'cpp': '_path_join', 'include': '<filesystem>'},
    'os.path.dirname': {'cpp': '_path_dirname', 'include': '<filesystem>'},
    'os.path.basename': {'cpp': '_path_basename', 'include': '<filesystem>'},
    'os.path.splitext': {'cpp': '_path_splitext', 'include': '<filesystem>'},
    'os.path.getsize': {'cpp': 'std::filesystem::file_size', 'include': '<filesystem>'},
    'os.getenv': {'cpp': 'std::getenv', 'include': '<cstdlib>'},
    'os.environ.get': {'cpp': 'std::getenv', 'include': '<cstdlib>'},
    'os.system': {'cpp': 'std::system', 'include': '<cstdlib>'},

    # sys module
    'sys.exit': {'cpp': 'std::exit', 'include': '<cstdlib>'},
    'sys.argv': {'cpp': '_sys_argv', 'include': None, 'note': 'Requires main() args'},
    'sys.platform': {'cpp': '_sys_platform()', 'include': None},

    # time module
    'time.sleep': {'cpp': 'std::this_thread::sleep_for(std::chrono::duration<double>({}))', 'include': '<thread>'},
    'time.time': {'cpp': '_time_now()', 'include': '<chrono>'},
    'time.perf_counter': {'cpp': '_time_perf_counter()', 'include': '<chrono>'},
    'time.monotonic': {'cpp': '_time_monotonic()', 'include': '<chrono>'},

    # threading module
    'threading.Thread': {'cpp': 'std::thread', 'include': '<thread>'},
    'threading.Lock': {'cpp': 'std::mutex', 'include': '<mutex>'},
    'threading.RLock': {'cpp': 'std::recursive_mutex', 'include': '<mutex>'},
    'threading.Event': {'cpp': '_threading_event', 'include': '<condition_variable>'},
    'threading.Semaphore': {'cpp': 'std::counting_semaphore', 'include': '<semaphore>'},
    'threading.Barrier': {'cpp': 'std::barrier', 'include': '<barrier>'},
    'threading.current_thread': {'cpp': 'std::this_thread::get_id', 'include': '<thread>'},

    # json module
    'json.dumps': {'cpp': '/* TODO: json.dumps - use nlohmann/json */', 'include': None},
    'json.loads': {'cpp': '/* TODO: json.loads - use nlohmann/json */', 'include': None},
    'json.load': {'cpp': '/* TODO: json.load - use nlohmann/json */', 'include': None},
    'json.dump': {'cpp': '/* TODO: json.dump - use nlohmann/json */', 'include': None},

    # re module (regex)
    're.match': {'cpp': 'std::regex_match', 'include': '<regex>'},
    're.search': {'cpp': 'std::regex_search', 'include': '<regex>'},
    're.sub': {'cpp': 'std::regex_replace', 'include': '<regex>'},
    're.findall': {'cpp': '_regex_findall', 'include': '<regex>'},
    're.compile': {'cpp': 'std::regex', 'include': '<regex>'},

    # math module
    'math.sqrt': {'cpp': 'std::sqrt', 'include': '<cmath>'},
    'math.pow': {'cpp': 'std::pow', 'include': '<cmath>'},
    'math.sin': {'cpp': 'std::sin', 'include': '<cmath>'},
    'math.cos': {'cpp': 'std::cos', 'include': '<cmath>'},
    'math.tan': {'cpp': 'std::tan', 'include': '<cmath>'},
    'math.log': {'cpp': 'std::log', 'include': '<cmath>'},
    'math.log10': {'cpp': 'std::log10', 'include': '<cmath>'},
    'math.exp': {'cpp': 'std::exp', 'include': '<cmath>'},
    'math.floor': {'cpp': 'std::floor', 'include': '<cmath>'},
    'math.ceil': {'cpp': 'std::ceil', 'include': '<cmath>'},
    'math.fabs': {'cpp': 'std::fabs', 'include': '<cmath>'},
    'math.pi': {'cpp': 'M_PI', 'include': '<cmath>'},
    'math.e': {'cpp': 'M_E', 'include': '<cmath>'},

    # collections module
    'collections.deque': {'cpp': 'std::deque', 'include': '<deque>'},
    'collections.defaultdict': {'cpp': '/* TODO: defaultdict - use std::map with default */', 'include': '<map>'},
    'collections.Counter': {'cpp': '/* TODO: Counter - use std::map<T, int> */', 'include': '<map>'},
    'collections.OrderedDict': {'cpp': 'std::map', 'include': '<map>'},

    # functools module
    'functools.partial': {'cpp': 'std::bind', 'include': '<functional>'},
    'functools.reduce': {'cpp': 'std::accumulate', 'include': '<numeric>'},

    # itertools module
    'itertools.chain': {'cpp': '/* TODO: itertools.chain - manual concatenation */', 'include': None},
    'itertools.zip_longest': {'cpp': '/* TODO: zip_longest - manual implementation */', 'include': None},

    # pathlib module
    'pathlib.Path': {'cpp': 'std::filesystem::path', 'include': '<filesystem>'},
    'Path': {'cpp': 'std::filesystem::path', 'include': '<filesystem>'},

    # typing module (type hints - ignore in conversion)
    'typing.List': {'cpp': 'std::vector', 'include': '<vector>'},
    'typing.Dict': {'cpp': 'std::unordered_map', 'include': '<unordered_map>'},
    'typing.Set': {'cpp': 'std::unordered_set', 'include': '<unordered_set>'},
    'typing.Tuple': {'cpp': 'std::tuple', 'include': '<tuple>'},
    'typing.Optional': {'cpp': 'std::optional', 'include': '<optional>'},
    'typing.Union': {'cpp': 'std::variant', 'include': '<variant>'},
    'typing.Callable': {'cpp': 'std::function', 'include': '<functional>'},
    'typing.Any': {'cpp': 'auto', 'include': None},
}


@dataclass
class FunctionInfo:
    name: str
    return_type: str
    params: List[Tuple[str, str]]
    body: str
    is_method: bool = False
    is_static: bool = False
    is_const: bool = False
    is_virtual: bool = False
    is_property: bool = False
    decorators: List[str] = field(default_factory=list)


@dataclass
class ClassInfo:
    name: str
    bases: List[str]
    methods: List[FunctionInfo]
    fields: List[Tuple[str, str, Optional[str]]]
    is_struct: bool = False
    constructors: List[FunctionInfo] = field(default_factory=list)


@dataclass
class StructInfo:
    name: str
    fields: List[Tuple[str, str]]


class PythonToCppConverter:
    # Common parameter name patterns to infer types
    PARAM_TYPE_HINTS = {
        # Integer-like names
        'n': 'int', 'k': 'int', 'i': 'int', 'j': 'int', 'count': 'int', 'num': 'int',
        'index': 'int', 'idx': 'int', 'size': 'size_t', 'length': 'size_t', 'len': 'size_t',
        'start': 'int', 'end': 'int', 'begin': 'int', 'stop': 'int', 'step': 'int',
        'seed': 'int', 'limit': 'int', 'offset': 'int', 'position': 'int', 'pos': 'int',
        'width': 'int', 'height': 'int', 'depth': 'int', 'x': 'int', 'y': 'int', 'z': 'int',
        'row': 'int', 'col': 'int', 'rows': 'int', 'cols': 'int', 'port': 'int',
        # Float-like names
        'alpha': 'double', 'beta': 'double', 'gamma': 'double', 'delta': 'double',
        'mu': 'double', 'sigma': 'double', 'lambd': 'double', 'lambda_': 'double',
        'rate': 'double', 'ratio': 'double', 'scale': 'double', 'weight': 'double',
        'probability': 'double', 'prob': 'double', 'threshold': 'double',
        'min_val': 'double', 'max_val': 'double',
        'temperature': 'double', 'temp': 'double', 'factor': 'double',
        # Template-matching parameters (for generic functions with T_CONTAINER)
        # These will be T when used with a T_CONTAINER parameter
        'value': 'T_ELEMENT', 'val': 'T_ELEMENT', 'item': 'T_ELEMENT', 'element': 'T_ELEMENT',
        'target': 'T_ELEMENT', 'needle': 'T_ELEMENT', 'search': 'T_ELEMENT',
        # String-like names
        'name': 'std::string', 'text': 'std::string', 'msg': 'std::string', 'message': 'std::string',
        'path': 'std::string', 'filename': 'std::string', 'file': 'std::string', 'dir': 'std::string',
        'url': 'std::string', 'key': 'std::string', 'prefix': 'std::string', 'suffix': 'std::string',
        'pattern': 'std::string', 'format': 'std::string', 'fmt': 'std::string',
        'title': 'std::string', 'label': 'std::string', 'description': 'std::string', 'desc': 'std::string',
        'content': 'std::string', 'data': 'std::string', 'input': 'std::string', 'output': 'std::string',
        's': 'std::string', 'str': 'std::string', 'string': 'std::string', 'line': 'std::string',
        'sep': 'std::string', 'delimiter': 'std::string', 'delim': 'std::string',
        # Boolean-like names
        'flag': 'bool', 'enabled': 'bool', 'disabled': 'bool', 'active': 'bool',
        'is_valid': 'bool', 'is_empty': 'bool', 'success': 'bool', 'ok': 'bool',
        'verbose': 'bool', 'quiet': 'bool', 'force': 'bool', 'recursive': 'bool',
        # Container-like names - use T as template parameter marker
        # These will trigger template generation for the containing function
        'items': 'T_CONTAINER', 'elements': 'T_CONTAINER', 'values': 'T_CONTAINER',
        'list': 'T_CONTAINER', 'lst': 'T_CONTAINER', 'array': 'T_CONTAINER',
        'choices': 'T_CONTAINER', 'options': 'T_CONTAINER',
        'population': 'T_CONTAINER', 'sample': 'T_CONTAINER',
        'weights': 'std::vector<double>',
    }

    # Template parameter markers - functions with these params become templates
    TEMPLATE_MARKER = 'T_CONTAINER'
    TEMPLATE_ELEMENT = 'T_ELEMENT'  # For parameters that match container element type

    def __init__(self):
        self.imports: Set[str] = set()
        self.forward_decls: Set[str] = set()
        self.unconvertible: List[Tuple[str, str, int]] = []  # (item, reason, line)
        self.warnings: List[str] = []
        self.python_imports: Set[str] = set()
        self.seeded_rngs: Dict[str, str] = {}  # var_name -> seed expression
        self.var_types: Dict[str, str] = {}  # Variable name -> C++ type tracking

    def convert(self, source: str, module_name: str) -> Tuple[str, str]:
        """Convert Python source to C++ (.cpp and .h content)."""
        self.imports = set()
        self.forward_decls = set()
        self.unconvertible = []
        self.warnings = []
        self.python_imports = set()
        self.seeded_rngs = {}
        self.var_types = {}

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            raise ValueError(f"Python syntax error: {e}")

        # First pass: detect imports and check for unconvertible modules
        self._analyze_imports(tree)

        classes = []
        functions = []
        global_vars = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(self._convert_class(node))
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                functions.append(self._convert_function(node))
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_type = self._infer_type(node.value)
                        var_value = self._convert_expr(node.value)
                        global_vars.append((target.id, var_type, var_value))
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    var_type = self._convert_type_annotation(node.annotation)
                    var_value = self._convert_expr(node.value) if node.value else None
                    global_vars.append((node.target.id, var_type, var_value))

        header = self._generate_header(module_name, classes, functions, global_vars)
        source_cpp = self._generate_source(module_name, classes, functions, global_vars)

        return source_cpp, header

    def _analyze_imports(self, tree):
        """Analyze imports and detect unconvertible modules."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod_name = alias.name.split('.')[0]
                    self.python_imports.add(mod_name)
                    if mod_name in UNCONVERTIBLE_MODULES:
                        reason = UNCONVERTIBLE_MODULES[mod_name]
                        self.unconvertible.append((mod_name, reason, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    mod_name = node.module.split('.')[0]
                    self.python_imports.add(mod_name)
                    if mod_name in UNCONVERTIBLE_MODULES:
                        reason = UNCONVERTIBLE_MODULES[mod_name]
                        self.unconvertible.append((mod_name, reason, node.lineno))

    def has_unconvertible_code(self) -> bool:
        """Check if there is any unconvertible code."""
        return len(self.unconvertible) > 0

    def get_unconvertible_summary(self) -> str:
        """Get a summary of unconvertible code."""
        if not self.unconvertible:
            return ""
        lines = ["UNCONVERTIBLE CODE DETECTED:"]
        for item, reason, line in self.unconvertible:
            lines.append(f"  Line {line}: {item} - {reason}")
        return '\n'.join(lines)

    def _convert_class(self, node: ast.ClassDef) -> ClassInfo:
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(self._get_attr_name(base))

        methods = []
        constructors = []
        fields = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef) or isinstance(item, ast.AsyncFunctionDef):
                func = self._convert_function(item, is_method=True)
                if func.name == '__init__':
                    func.name = node.name
                    constructors.append(func)
                    for stmt in item.body:
                        if isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                    if target.value.id == 'self':
                                        field_type = self._infer_type(stmt.value)
                                        field_val = self._convert_expr(stmt.value)
                                        fields.append((target.attr, field_type, field_val))
                        elif isinstance(stmt, ast.AnnAssign):
                            if isinstance(stmt.target, ast.Attribute) and isinstance(stmt.target.value, ast.Name):
                                if stmt.target.value.id == 'self':
                                    field_type = self._convert_type_annotation(stmt.annotation)
                                    field_val = self._convert_expr(stmt.value) if stmt.value else None
                                    fields.append((stmt.target.attr, field_type, field_val))
                elif func.name.startswith('__') and func.name.endswith('__'):
                    continue
                else:
                    methods.append(func)
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    field_type = self._convert_type_annotation(item.annotation)
                    field_val = self._convert_expr(item.value) if item.value else None
                    fields.append((item.target.id, field_type, field_val))

        return ClassInfo(
            name=node.name,
            bases=bases,
            methods=methods,
            fields=fields,
            constructors=constructors
        )

    def _infer_param_type(self, param_name: str, func_node) -> str:
        """Infer C++ type from parameter name and usage patterns."""
        # Check direct name hints
        if param_name in self.PARAM_TYPE_HINTS:
            return self.PARAM_TYPE_HINTS[param_name]

        # Check partial matches (e.g., 'file_name' contains 'name')
        param_lower = param_name.lower()
        for hint_name, hint_type in self.PARAM_TYPE_HINTS.items():
            if hint_name in param_lower or param_lower.endswith('_' + hint_name):
                return hint_type

        # Analyze how the parameter is used in the function body
        inferred = self._analyze_param_usage(param_name, func_node)
        if inferred and inferred != 'auto':
            return inferred

        # Default: use auto (will become template)
        return 'auto'

    def _analyze_param_usage(self, param_name: str, func_node) -> str:
        """Analyze how a parameter is used to infer its type."""
        for node in ast.walk(func_node):
            # Check if used in comparison with numeric literal
            if isinstance(node, ast.Compare):
                left = node.left
                if isinstance(left, ast.Name) and left.id == param_name:
                    for comp in node.comparators:
                        if isinstance(comp, ast.Constant):
                            if isinstance(comp.value, int):
                                return 'int'
                            elif isinstance(comp.value, float):
                                return 'double'

            # Check if used in arithmetic operations
            if isinstance(node, ast.BinOp):
                left = node.left
                right = node.right
                if (isinstance(left, ast.Name) and left.id == param_name) or \
                   (isinstance(right, ast.Name) and right.id == param_name):
                    if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)):
                        # Check if other operand hints at type
                        other = right if isinstance(left, ast.Name) and left.id == param_name else left
                        if isinstance(other, ast.Constant):
                            if isinstance(other.value, float):
                                return 'double'
                            elif isinstance(other.value, int):
                                return 'int'

            # Check if used in string operations
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                left = node.left
                right = node.right
                if isinstance(left, ast.Name) and left.id == param_name:
                    if isinstance(right, ast.Constant) and isinstance(right.value, str):
                        return 'std::string'
                if isinstance(right, ast.Name) and right.id == param_name:
                    if isinstance(left, ast.Constant) and isinstance(left.value, str):
                        return 'std::string'

            # Check if used in subscript (likely a container)
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Name) and node.value.id == param_name:
                    return 'auto'  # Container, will become template

            # Check if used in for loop iteration
            if isinstance(node, ast.For):
                if isinstance(node.iter, ast.Name) and node.iter.id == param_name:
                    return 'auto'  # Iterable, will become template

        return 'auto'

    def _convert_function(self, node, is_method: bool = False) -> FunctionInfo:
        decorators = []
        is_static = False
        is_property = False

        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                if dec.id == 'staticmethod':
                    is_static = True
                elif dec.id == 'classmethod':
                    is_static = True
                elif dec.id == 'property':
                    is_property = True
                decorators.append(dec.id)

        params = []
        for arg in node.args.args:
            if arg.arg == 'self' or arg.arg == 'cls':
                continue
            if arg.annotation:
                param_type = self._convert_type_annotation(arg.annotation)
            else:
                # Use smart type inference
                param_type = self._infer_param_type(arg.arg, node)
            params.append((arg.arg, param_type))
            # Track parameter types for use in body conversion
            self.var_types[arg.arg] = param_type

        if node.returns:
            return_type = self._convert_type_annotation(node.returns)
        else:
            return_type = self._infer_return_type(node)

        body = self._convert_body(node.body)

        return FunctionInfo(
            name=node.name,
            return_type=return_type,
            params=params,
            body=body,
            is_method=is_method,
            is_static=is_static,
            is_property=is_property,
            decorators=decorators
        )

    def _convert_type_annotation(self, node) -> str:
        if node is None:
            return 'auto'

        if isinstance(node, ast.Name):
            py_type = node.id
            return PY_TO_CPP_TYPES.get(py_type, py_type)

        elif isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name):
                container = node.value.id
                cpp_container = PY_TO_CPP_TYPES.get(container, container)

                if isinstance(node.slice, ast.Tuple):
                    inner_types = [self._convert_type_annotation(elt) for elt in node.slice.elts]
                    return f"{cpp_container}<{', '.join(inner_types)}>"
                else:
                    inner_type = self._convert_type_annotation(node.slice)
                    return f"{cpp_container}<{inner_type}>"

        elif isinstance(node, ast.Constant):
            if node.value is None:
                return 'void'
            return str(type(node.value).__name__)

        elif isinstance(node, ast.Attribute):
            return self._get_attr_name(node)

        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            left = self._convert_type_annotation(node.left)
            right = self._convert_type_annotation(node.right)
            return f"std::variant<{left}, {right}>"

        return 'auto'

    def _infer_type(self, node) -> str:
        """Infer C++ type from AST node with robust empty container handling."""
        if node is None:
            return 'auto'

        try:
            if isinstance(node, ast.Constant):
                val = node.value
                if isinstance(val, bool):
                    return 'bool'
                elif isinstance(val, int):
                    return 'int'
                elif isinstance(val, float):
                    return 'double'
                elif isinstance(val, str):
                    return 'std::string'
                elif isinstance(val, bytes):
                    return 'std::vector<uint8_t>'
                elif val is None:
                    return 'void'

            elif isinstance(node, ast.List):
                first_elt = _safe_get(node.elts, 0)
                if first_elt is not None:
                    inner = self._infer_type(first_elt)
                    return f'std::vector<{inner}>'
                return 'std::vector<int>'

            elif isinstance(node, ast.Dict):
                first_key = _safe_get(node.keys, 0)
                first_val = _safe_get(node.values, 0)
                if first_key is not None and first_val is not None:
                    key_type = self._infer_type(first_key)
                    val_type = self._infer_type(first_val)
                    return f'std::unordered_map<{key_type}, {val_type}>'
                return 'std::unordered_map<std::string, int>'

            elif isinstance(node, ast.Set):
                first_elt = _safe_get(node.elts, 0)
                if first_elt is not None:
                    inner = self._infer_type(first_elt)
                    return f'std::unordered_set<{inner}>'
                return 'std::unordered_set<int>'

            elif isinstance(node, ast.Tuple):
                if node.elts:
                    types = [self._infer_type(elt) for elt in node.elts]
                    return f'std::tuple<{", ".join(types)}>'
                return 'std::tuple<>'

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name == 'bytearray':
                        return 'std::vector<uint8_t>'
                    if func_name == 'len':
                        return 'size_t'
                    if func_name == 'range':
                        return 'int'  # Range iteration variable
                    if func_name == 'enumerate':
                        return 'auto'  # Tuple of (index, value)
                    return PY_TO_CPP_TYPES.get(func_name, 'auto')

            elif isinstance(node, ast.BinOp):
                left_type = self._infer_type(node.left)
                right_type = self._infer_type(node.right)
                # More precise type checking
                if left_type == 'double' or right_type == 'double':
                    return 'double'
                if left_type == 'std::string' or right_type == 'std::string':
                    return 'std::string'
                return left_type if left_type != 'auto' else right_type

            elif isinstance(node, ast.Compare):
                return 'bool'

            elif isinstance(node, ast.BoolOp):
                return 'bool'

            elif isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.Not):
                    return 'bool'
                return self._infer_type(node.operand)

            elif isinstance(node, ast.Name):
                # Check for common type names
                name = node.id
                if name in PY_TO_CPP_TYPES:
                    return PY_TO_CPP_TYPES[name]
                return 'auto'

            elif isinstance(node, ast.Attribute):
                return 'auto'

            elif isinstance(node, ast.Subscript):
                return 'auto'

            elif isinstance(node, ast.IfExp):
                return self._infer_type(node.body)

            elif isinstance(node, ast.ListComp):
                return f'std::vector<{self._infer_type(node.elt)}>'

            elif isinstance(node, ast.DictComp):
                return f'std::unordered_map<{self._infer_type(node.key)}, {self._infer_type(node.value)}>'

            elif isinstance(node, ast.SetComp):
                return f'std::unordered_set<{self._infer_type(node.elt)}>'

        except Exception:
            pass  # Fall through to 'auto'

        return 'auto'

    def _infer_return_type(self, node) -> str:
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Return) and stmt.value:
                return self._infer_type(stmt.value)
        return 'void'

    def _track_for_loop_var_type(self, var_name: str, iter_node) -> None:
        """Track the type of a for loop variable based on the iterable."""
        iter_type = self._infer_type(iter_node)

        # Extract element type from container types
        if '<' in iter_type and '>' in iter_type:
            element_type = iter_type[iter_type.find('<')+1:iter_type.rfind('>')]
            self.var_types[var_name] = element_type
        elif 'string' in iter_type.lower():
            # Iterating over string gives char
            self.var_types[var_name] = 'char'
        elif isinstance(iter_node, ast.Name):
            # Check if iterable is a known variable
            known_type = self.var_types.get(iter_node.id, '')
            if '<' in known_type and '>' in known_type:
                element_type = known_type[known_type.find('<')+1:known_type.rfind('>')]
                self.var_types[var_name] = element_type
            elif 'string' in known_type.lower():
                self.var_types[var_name] = 'std::string'
            else:
                self.var_types[var_name] = 'auto'
        else:
            self.var_types[var_name] = 'auto'

    def _is_string_expr(self, node, expr: str) -> bool:
        """Check if an expression evaluates to a string type.

        This prevents wrapping string values in std::to_string() in f-strings.
        """
        # Check obvious string indicators in converted expression
        if any(x in expr for x in ['"', '.c_str()', 'std::string', '_str']):
            return True

        # Check if it's a string literal constant
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return True

        # Check if it's a variable we know is a string
        if isinstance(node, ast.Name):
            var_name = node.id
            var_type = self.var_types.get(var_name, '')
            if 'string' in var_type.lower() or var_type == 'std::string':
                return True
            # Check if variable name suggests string type
            if var_name in self.PARAM_TYPE_HINTS:
                if 'string' in self.PARAM_TYPE_HINTS[var_name].lower():
                    return True
            # Common string variable names
            string_names = {'name', 'text', 'msg', 'message', 'path', 'url', 'title',
                           'label', 'description', 'content', 'data', 'line', 's', 'str',
                           'item', 'key', 'value', 'word', 'char', 'prefix', 'suffix',
                           'filename', 'file', 'dir', 'result', 'output', 'input'}
            if var_name.lower() in string_names or any(var_name.lower().endswith('_' + n) for n in string_names):
                return True

        # Check string method calls like .upper(), .strip(), etc.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            string_methods = {'upper', 'lower', 'strip', 'lstrip', 'rstrip', 'title',
                             'capitalize', 'replace', 'format', 'join', 'split',
                             'encode', 'decode', 'center', 'ljust', 'rjust'}
            if node.func.attr in string_methods:
                return True

        # Check attribute access that returns string (like .name, .path)
        if isinstance(node, ast.Attribute):
            string_attrs = {'name', 'path', 'filename', 'text', 'message', 'value'}
            if node.attr in string_attrs:
                return True

        # Check inferred type
        inferred_type = self._infer_type(node)
        if 'string' in inferred_type.lower():
            return True

        return False

    def _convert_body(self, stmts: List, indent: int = 1) -> str:
        lines = []
        ind = '    ' * indent

        for stmt in stmts:
            lines.extend(self._convert_stmt(stmt, indent))

        return '\n'.join(lines)

    def _convert_stmt(self, stmt, indent: int) -> List[str]:
        ind = '    ' * indent
        lines = []

        if isinstance(stmt, ast.Return):
            if stmt.value:
                val = self._convert_expr(stmt.value)
                lines.append(f'{ind}return {val};')
            else:
                lines.append(f'{ind}return;')

        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                # Check for tuple unpacking: a, b = func() or a, b = (1, 2)
                if isinstance(target, ast.Tuple):
                    value_str = self._convert_expr(stmt.value)
                    var_names = [self._convert_expr(elt) for elt in target.elts]
                    # Use C++17 structured bindings
                    lines.append(f'{ind}auto [{", ".join(var_names)}] = {value_str};')
                    continue

                target_str = self._convert_expr(target)
                # Check if this is a seeded random assignment: rng = random.Random(seed)
                if (isinstance(stmt.value, ast.Call) and
                    isinstance(stmt.value.func, ast.Attribute) and
                    isinstance(stmt.value.func.value, ast.Name) and
                    stmt.value.func.value.id == 'random' and
                    stmt.value.func.attr == 'Random' and
                    isinstance(target, ast.Name)):
                    # Track this variable as a seeded RNG
                    seed_expr = self._convert_expr(stmt.value.args[0]) if stmt.value.args else '0'
                    self.seeded_rngs[target.id] = seed_expr
                    self.imports.add('<random>')
                    lines.append(f'{ind}std::mt19937 {target_str}({seed_expr});')
                else:
                    value_str = self._convert_expr(stmt.value)
                    var_type = self._infer_type(stmt.value)
                    if isinstance(target, ast.Name):
                        # Track this variable's type
                        self.var_types[target.id] = var_type
                        lines.append(f'{ind}{var_type} {target_str} = {value_str};')
                    else:
                        lines.append(f'{ind}{target_str} = {value_str};')

        elif isinstance(stmt, ast.AnnAssign):
            target_str = self._convert_expr(stmt.target)
            var_type = self._convert_type_annotation(stmt.annotation)
            # Track annotated variable types
            if isinstance(stmt.target, ast.Name):
                self.var_types[stmt.target.id] = var_type
            if stmt.value:
                value_str = self._convert_expr(stmt.value)
                lines.append(f'{ind}{var_type} {target_str} = {value_str};')
            else:
                lines.append(f'{ind}{var_type} {target_str};')

        elif isinstance(stmt, ast.AugAssign):
            target_str = self._convert_expr(stmt.target)
            value_str = self._convert_expr(stmt.value)
            op = self._convert_binop(stmt.op)
            lines.append(f'{ind}{target_str} {op}= {value_str};')

        elif isinstance(stmt, ast.Expr):
            # Check if this is a docstring (string literal expression) - convert to comment
            if isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                docstring = stmt.value.value.strip()
                if docstring:
                    # Convert to C++ comment (take first line only for brevity)
                    first_line = docstring.split('\n')[0].strip()
                    if first_line:
                        lines.append(f'{ind}// {first_line}')
            else:
                expr_str = self._convert_expr(stmt.value)
                lines.append(f'{ind}{expr_str};')

        elif isinstance(stmt, ast.If):
            test = self._convert_expr(stmt.test)
            lines.append(f'{ind}if ({test}) {{')
            lines.extend(self._convert_stmt_list(stmt.body, indent + 1))
            if stmt.orelse:
                if len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If):
                    lines.append(f'{ind}}} else')
                    lines.extend(self._convert_stmt(stmt.orelse[0], indent))
                else:
                    lines.append(f'{ind}}} else {{')
                    lines.extend(self._convert_stmt_list(stmt.orelse, indent + 1))
                    lines.append(f'{ind}}}')
            else:
                lines.append(f'{ind}}}')

        elif isinstance(stmt, ast.For):
            target = self._convert_expr(stmt.target)
            iter_expr = stmt.iter

            if isinstance(iter_expr, ast.Call) and isinstance(iter_expr.func, ast.Name):
                if iter_expr.func.id == 'range':
                    args = iter_expr.args
                    if len(args) == 1:
                        end = self._convert_expr(args[0])
                        lines.append(f'{ind}for (size_t {target} = 0; {target} < static_cast<size_t>({end}); ++{target}) {{')
                    elif len(args) == 2:
                        start = self._convert_expr(args[0])
                        end = self._convert_expr(args[1])
                        lines.append(f'{ind}for (size_t {target} = {start}; {target} < static_cast<size_t>({end}); ++{target}) {{')
                    elif len(args) == 3:
                        start = self._convert_expr(args[0])
                        end = self._convert_expr(args[1])
                        step = self._convert_expr(args[2])
                        lines.append(f'{ind}for (size_t {target} = {start}; {target} < static_cast<size_t>({end}); {target} += {step}) {{')
                elif iter_expr.func.id == 'enumerate':
                    # Handle enumerate(items, start=N)
                    args = iter_expr.args
                    iterable_node = args[0] if args else None
                    iterable = self._convert_expr(args[0]) if args else 'items'
                    start_idx = '0'
                    # Check for start keyword arg
                    for kw in iter_expr.keywords:
                        if kw.arg == 'start':
                            start_idx = self._convert_expr(kw.value)
                    if len(args) >= 2:
                        start_idx = self._convert_expr(args[1])
                    # Parse target - it's usually a Tuple like (index, item)
                    if isinstance(stmt.target, ast.Tuple) and len(stmt.target.elts) == 2:
                        idx_name = self._convert_expr(stmt.target.elts[0])
                        item_name = self._convert_expr(stmt.target.elts[1])

                        # Track variable types for the loop variables
                        self.var_types[idx_name] = 'size_t'

                        # Infer item type from the iterable
                        if iterable_node:
                            iterable_type = self._infer_type(iterable_node)
                            # Extract element type from container (e.g., std::vector<std::string> -> std::string)
                            if '<' in iterable_type and '>' in iterable_type:
                                element_type = iterable_type[iterable_type.find('<')+1:iterable_type.rfind('>')]
                                self.var_types[item_name] = element_type
                            else:
                                # Check if the iterable is a known variable
                                if isinstance(iterable_node, ast.Name):
                                    var_type = self.var_types.get(iterable_node.id, '')
                                    if 'string' in var_type.lower():
                                        self.var_types[item_name] = 'std::string'
                                    elif var_type == self.TEMPLATE_MARKER or 'std::vector' in var_type:
                                        self.var_types[item_name] = 'auto'
                                    else:
                                        self.var_types[item_name] = 'auto'
                                else:
                                    self.var_types[item_name] = 'auto'
                        else:
                            self.var_types[item_name] = 'auto'

                        lines.append(f'{ind}size_t {idx_name} = {start_idx};')
                        lines.append(f'{ind}for (auto& {item_name} : {iterable}) {{')
                        # Add index increment at end of loop body
                        body_lines = self._convert_stmt_list(stmt.body, indent + 1)
                        body_lines.append(f'{ind}    ++{idx_name};')
                        lines.extend(body_lines)
                        lines.append(f'{ind}}}')
                        return lines
                    else:
                        # Fallback: just iterate
                        iter_str = self._convert_expr(iter_expr)
                        # Track loop variable type from iterable
                        if isinstance(stmt.target, ast.Name):
                            self._track_for_loop_var_type(stmt.target.id, iter_expr)
                        lines.append(f'{ind}for (auto& {target} : {iter_str}) {{')
                else:
                    iter_str = self._convert_expr(iter_expr)
                    # Track loop variable type from iterable
                    if isinstance(stmt.target, ast.Name):
                        self._track_for_loop_var_type(stmt.target.id, iter_expr)
                    lines.append(f'{ind}for (auto& {target} : {iter_str}) {{')
            else:
                iter_str = self._convert_expr(iter_expr)
                # Track loop variable type from iterable
                if isinstance(stmt.target, ast.Name):
                    self._track_for_loop_var_type(stmt.target.id, iter_expr)
                lines.append(f'{ind}for (auto& {target} : {iter_str}) {{')

            lines.extend(self._convert_stmt_list(stmt.body, indent + 1))
            lines.append(f'{ind}}}')

        elif isinstance(stmt, ast.While):
            test = self._convert_expr(stmt.test)
            lines.append(f'{ind}while ({test}) {{')
            lines.extend(self._convert_stmt_list(stmt.body, indent + 1))
            lines.append(f'{ind}}}')

        elif isinstance(stmt, ast.Break):
            lines.append(f'{ind}break;')

        elif isinstance(stmt, ast.Continue):
            lines.append(f'{ind}continue;')

        elif isinstance(stmt, ast.Pass):
            pass

        elif isinstance(stmt, ast.Try):
            lines.append(f'{ind}try {{')
            lines.extend(self._convert_stmt_list(stmt.body, indent + 1))
            lines.append(f'{ind}}}')
            for handler in stmt.handlers:
                exc_type = 'std::exception'
                exc_name = 'e'
                if handler.type:
                    exc_type = self._convert_expr(handler.type)
                if handler.name:
                    exc_name = handler.name
                lines.append(f'{ind}catch (const {exc_type}& {exc_name}) {{')
                lines.extend(self._convert_stmt_list(handler.body, indent + 1))
                lines.append(f'{ind}}}')

        elif isinstance(stmt, ast.Raise):
            if stmt.exc:
                exc = self._convert_exception(stmt.exc)
                lines.append(f'{ind}throw std::runtime_error({exc});')
            else:
                lines.append(f'{ind}throw;')

        elif isinstance(stmt, ast.With):
            for item in stmt.items:
                ctx = self._convert_expr(item.context_expr)
                if item.optional_vars:
                    var = self._convert_expr(item.optional_vars)
                    lines.append(f'{ind}auto {var} = {ctx};')
                else:
                    lines.append(f'{ind}{ctx};')
            lines.extend(self._convert_stmt_list(stmt.body, indent))

        elif isinstance(stmt, ast.FunctionDef):
            func = self._convert_function(stmt)
            lines.append(f'{ind}auto {func.name} = []({self._format_params(func.params)}) -> {func.return_type} {{')
            lines.append(func.body)
            lines.append(f'{ind}}};')

        return lines

    def _convert_exception(self, node) -> str:
        """Convert a Python exception to a C++ exception string."""
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.args:
                    msg = self._convert_expr(node.args[0])
                    return msg
        return '"Unknown error"'

    def _convert_stmt_list(self, stmts: List, indent: int) -> List[str]:
        lines = []
        for stmt in stmts:
            lines.extend(self._convert_stmt(stmt, indent))
        return lines

    def _convert_expr(self, node) -> str:
        """Convert AST expression to C++ with comprehensive error handling."""
        if node is None:
            return ''

        try:
            return self._convert_expr_impl(node)
        except Exception as e:
            line_info = getattr(node, 'lineno', '?')
            self.warnings.append(f"Expression conversion failed at line {line_info}: {type(e).__name__}: {e}")
            return f'/* ERROR at line {line_info}: {type(e).__name__} */'

    def _convert_expr_impl(self, node) -> str:
        """Internal implementation of expression conversion."""
        if isinstance(node, ast.Constant):
            val = node.value
            if isinstance(val, str):
                # Complete string escaping for C++
                escaped = val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t').replace('\0', '\\0').replace('\f', '\\f').replace('\b', '\\b').replace('\a', '\\a').replace('\v', '\\v')
                return f'"{escaped}"'
            elif isinstance(val, bool):
                return 'true' if val else 'false'
            elif val is None:
                return 'nullptr'
            else:
                return str(val)

        elif isinstance(node, ast.Name):
            name = node.id
            if name == 'True':
                return 'true'
            elif name == 'False':
                return 'false'
            elif name == 'None':
                return 'nullptr'
            return name

        elif isinstance(node, ast.Attribute):
            value = self._convert_expr(node.value)
            if value == 'self':
                return f'this->{node.attr}'
            return f'{value}.{node.attr}'

        elif isinstance(node, ast.Subscript):
            # Check if this is random.choices(...)[0] - skip the subscript since we return single element
            if (isinstance(node.value, ast.Call) and
                isinstance(node.value.func, ast.Attribute) and
                isinstance(node.value.func.value, ast.Name) and
                node.value.func.value.id == 'random' and
                node.value.func.attr == 'choices'):
                # Check if subscript is [0] and k=1
                if isinstance(node.slice, ast.Constant) and node.slice.value == 0:
                    # Just return the weighted choice call without subscript
                    return self._convert_expr(node.value)

            value = self._convert_expr(node.value)
            if isinstance(node.slice, ast.Slice):
                lower = self._convert_expr(node.slice.lower) if node.slice.lower else '0'
                upper = self._convert_expr(node.slice.upper) if node.slice.upper else f'{value}.size()'
                return f'std::vector<uint8_t>({value}.begin() + {lower}, {value}.begin() + {upper})'
            else:
                slice_val = self._convert_expr(node.slice)
                return f'{value}[{slice_val}]'

        elif isinstance(node, ast.Call):
            # Handle chained method calls on random.Random(seed)
            if (isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Call) and
                isinstance(node.func.value.func, ast.Attribute)):
                inner_func = node.func.value.func
                if hasattr(inner_func, 'value') and hasattr(inner_func.value, 'id'):
                    if inner_func.value.id == 'random' and inner_func.attr == 'Random':
                        seed_arg = self._convert_expr(node.func.value.args[0]) if node.func.value.args else '0'
                        method = node.func.attr
                        args = [self._convert_expr(arg) for arg in node.args]
                        self.imports.add('<random>')
                        if method == 'randint':
                            # Generate inline seeded randint
                            return f'[&](){{ std::mt19937 rng({seed_arg}); std::uniform_int_distribution<int> dist({_safe_arg(args, 0)}, {_safe_arg(args, 1)}); return dist(rng); }}()'
                        elif method == 'uniform':
                            return f'[&](){{ std::mt19937 rng({seed_arg}); std::uniform_real_distribution<double> dist({_safe_arg(args, 0, "0.0")}, {_safe_arg(args, 1, "1.0")}); return dist(rng); }}()'
                        elif method == 'choice':
                            arg0 = _safe_arg(args, 0, 'std::vector<int>{}')
                            return f'[&](){{ std::mt19937 rng({seed_arg}); std::uniform_int_distribution<size_t> dist(0, {arg0}.size()-1); return {arg0}[dist(rng)]; }}()'

            # Handle method calls on seeded RNG variables: rng.randint(start, end)
            if (isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Name) and
                node.func.value.id in self.seeded_rngs):
                rng_var = node.func.value.id
                method = node.func.attr
                args = [self._convert_expr(arg) for arg in node.args]
                self.imports.add('<random>')
                if method == 'randint':
                    return f'[&](){{ std::uniform_int_distribution<int> dist({_safe_arg(args, 0)}, {_safe_arg(args, 1)}); return dist({rng_var}); }}()'
                elif method == 'uniform':
                    return f'[&](){{ std::uniform_real_distribution<double> dist({_safe_arg(args, 0, "0.0")}, {_safe_arg(args, 1, "1.0")}); return dist({rng_var}); }}()'
                elif method == 'choice':
                    arg0 = _safe_arg(args, 0, 'std::vector<int>{}')
                    return f'[&](){{ std::uniform_int_distribution<size_t> dist(0, {arg0}.size()-1); return {arg0}[dist({rng_var})]; }}()'
                elif method == 'random':
                    return f'[&](){{ std::uniform_real_distribution<double> dist(0.0, 1.0); return dist({rng_var}); }}()'

            func = self._convert_expr(node.func)
            args = [self._convert_expr(arg) for arg in node.args]

            # Check MODULE_CONVERSIONS first for standard library functions
            if func in MODULE_CONVERSIONS:
                conv = MODULE_CONVERSIONS[func]
                cpp = conv['cpp']
                if conv.get('include'):
                    self.imports.add(conv['include'])
                # Check if it's a pattern with {} placeholder
                if '{}' in cpp:
                    return cpp.format(args[0] if args else '')
                elif '(' in cpp:
                    # Already a function call
                    return cpp
                else:
                    # Simple function name replacement
                    return f'{cpp}({", ".join(args)})'

            # Check for unconvertible module calls
            for mod_name in UNCONVERTIBLE_MODULES:
                if func.startswith(f'{mod_name}.'):
                    reason = UNCONVERTIBLE_MODULES[mod_name]
                    self.unconvertible.append((func, reason, getattr(node, 'lineno', 0)))
                    return f'/* UNCONVERTIBLE: {func}({", ".join(args)}) - {reason} */'

            # Builtin functions (with safe argument access)
            if func == 'len':
                return f'{_safe_arg(args, 0, "container")}.size()'
            elif func == 'bytearray':
                if args:
                    return f'std::vector<uint8_t>({_safe_arg(args, 0)}, 0)'
                return 'std::vector<uint8_t>()'
            elif func == 'str':
                return f'std::to_string({_safe_arg(args, 0)})'
            elif func == 'int':
                return f'static_cast<int>({_safe_arg(args, 0)})'
            elif func == 'float':
                return f'static_cast<double>({_safe_arg(args, 0)})'
            elif func == 'print':
                if args:
                    return f'std::cout << {" << \" \" << ".join(args)} << std::endl'
                return 'std::cout << std::endl'
            elif func == 'range':
                return f'/* range({", ".join(args) if args else ""}) */'
            elif func == 'list':
                if args:
                    return f'std::vector({_safe_arg(args, 0)})'
                return 'std::vector<int>{}'
            elif func == 'dict':
                return 'std::unordered_map<std::string, int>{}'
            elif func == 'set':
                if args:
                    return f'std::unordered_set({_safe_arg(args, 0)})'
                return 'std::unordered_set<int>{}'
            elif func == 'abs':
                return f'std::abs({_safe_arg(args, 0)})'
            elif func == 'min':
                self.imports.add('<algorithm>')
                if len(args) == 2:
                    return f'std::min({_safe_arg(args, 0)}, {_safe_arg(args, 1)})'
                elif len(args) == 1:
                    # Single container argument - use min_element
                    arg0 = _safe_arg(args, 0)
                    return f'*std::min_element({arg0}.begin(), {arg0}.end())'
                elif args:
                    return f'std::min({{{", ".join(args)}}})'
                return '0 /* min() requires arguments */'
            elif func == 'max':
                self.imports.add('<algorithm>')
                if len(args) == 2:
                    return f'std::max({_safe_arg(args, 0)}, {_safe_arg(args, 1)})'
                elif len(args) == 1:
                    # Single container argument - use max_element
                    arg0 = _safe_arg(args, 0)
                    return f'*std::max_element({arg0}.begin(), {arg0}.end())'
                elif args:
                    return f'std::max({{{", ".join(args)}}})'
                return '0 /* max() requires arguments */'
            elif func == 'sum':
                self.imports.add('<numeric>')
                arg0 = _safe_arg(args, 0, 'std::vector<int>{}')
                return f'std::accumulate({arg0}.begin(), {arg0}.end(), 0)'
            elif func == 'sorted':
                self.imports.add('<algorithm>')
                arg0 = _safe_arg(args, 0, 'std::vector<int>{}')
                return f'[&](){{ auto tmp = {arg0}; std::sort(tmp.begin(), tmp.end()); return tmp; }}()'
            elif func == 'reversed':
                self.imports.add('<algorithm>')
                arg0 = _safe_arg(args, 0, 'std::vector<int>{}')
                return f'[&](){{ auto tmp = {arg0}; std::reverse(tmp.begin(), tmp.end()); return tmp; }}()'
            elif func.endswith('.append'):
                obj = func.rsplit('.', 1)[0]
                return f'{obj}.push_back({_safe_arg(args, 0)})'
            elif func.endswith('.pop'):
                obj = func.rsplit('.', 1)[0]
                if args:
                    return f'{obj}.erase({obj}.begin() + {_safe_arg(args, 0)})'
                return f'[&](){{ auto tmp = {obj}.back(); {obj}.pop_back(); return tmp; }}()'
            elif func.endswith('.insert'):
                obj = func.rsplit('.', 1)[0]
                return f'{obj}.insert({obj}.begin() + {_safe_arg(args, 0)}, {_safe_arg(args, 1)})'
            elif func.endswith('.remove'):
                obj = func.rsplit('.', 1)[0]
                self.imports.add('<algorithm>')
                return f'{obj}.erase(std::remove({obj}.begin(), {obj}.end(), {_safe_arg(args, 0)}), {obj}.end())'
            elif func.endswith('.clear'):
                obj = func.rsplit('.', 1)[0]
                return f'{obj}.clear()'

            # Python random module conversions (with safe argument access)
            elif func == 'random.randint':
                self.imports.add('<random>')
                return f'_rng_uniform_int({_safe_arg(args, 0)}, {_safe_arg(args, 1)})'
            elif func == 'random.uniform':
                self.imports.add('<random>')
                return f'_rng_uniform_real({_safe_arg(args, 0, "0.0")}, {_safe_arg(args, 1, "1.0")})'
            elif func == 'random.choice':
                self.imports.add('<random>')
                return f'_rng_choice({_safe_arg(args, 0, "std::vector<int>{}")})'
            elif func == 'random.sample':
                self.imports.add('<random>')
                self.imports.add('<algorithm>')
                return f'_rng_sample({_safe_arg(args, 0, "std::vector<int>{}")}, {_safe_arg(args, 1, "1")})'
            elif func == 'random.shuffle':
                self.imports.add('<random>')
                self.imports.add('<algorithm>')
                return f'_rng_shuffle({_safe_arg(args, 0, "std::vector<int>{}")})'
            elif func == 'random.randbytes':
                self.imports.add('<random>')
                return f'_rng_bytes({_safe_arg(args, 0, "1")})'
            elif func == 'random.Random':
                self.imports.add('<random>')
                return f'std::mt19937({_safe_arg(args, 0)})'
            elif func == 'random.gauss' or func == 'random.normalvariate':
                self.imports.add('<random>')
                return f'_rng_normal({_safe_arg(args, 0, "0.0")}, {_safe_arg(args, 1, "1.0")})'
            elif func == 'random.betavariate':
                self.imports.add('<random>')
                return f'_rng_beta({_safe_arg(args, 0, "1.0")}, {_safe_arg(args, 1, "1.0")})'
            elif func == 'random.expovariate':
                self.imports.add('<random>')
                return f'_rng_exponential(1.0 / {_safe_arg(args, 0, "1.0")})'
            elif func == 'random.lognormvariate':
                self.imports.add('<random>')
                return f'_rng_lognormal({_safe_arg(args, 0, "0.0")}, {_safe_arg(args, 1, "1.0")})'
            elif func == 'random.choices':
                self.imports.add('<random>')
                # Handle weighted choices - check both positional and keyword args
                weights_arg = '{}'
                if len(args) > 1:
                    weights_arg = _safe_arg(args, 1, '{}')
                else:
                    # Check keyword arguments for 'weights'
                    for kw in node.keywords:
                        if kw.arg == 'weights':
                            weights_arg = self._convert_expr(kw.value)
                            break
                if args:
                    return f'_rng_weighted_choice({_safe_arg(args, 0)}, {weights_arg})'
                return f'_rng_choice({_safe_arg(args, 0, "std::vector<int>{}")})'
            elif func.startswith('random.'):
                self.imports.add('<random>')
                # Generic random function - mark as needs implementation
                method = func.split('.', 1)[1]
                return f'/* TODO: random.{method} */ 0'

            # tkinter is not convertible - mark as unconvertible
            elif func.startswith('tk.') or func.startswith('tkinter.'):
                return f'/* UNCONVERTIBLE: {func}({", ".join(args)}) - tkinter has no C++ equivalent */'
            elif '.title(' in func or '.pack(' in func or '.mainloop(' in func:
                obj = func.rsplit('.', 1)[0]
                method = func.rsplit('.', 1)[1]
                return f'/* UNCONVERTIBLE: {obj}.{method}() - GUI operation */'

            kwargs = []
            for kw in node.keywords:
                kwargs.append(f'/* {kw.arg}= */{self._convert_expr(kw.value)}')

            all_args = args + kwargs
            return f'{func}({", ".join(all_args)})'

        elif isinstance(node, ast.BinOp):
            left = self._convert_expr(node.left)
            right = self._convert_expr(node.right)
            op = self._convert_binop(node.op)

            if isinstance(node.op, ast.Pow):
                self.imports.add('<cmath>')
                return f'std::pow({left}, {right})'
            elif isinstance(node.op, ast.FloorDiv):
                return f'static_cast<int>({left} / {right})'

            return f'({left} {op} {right})'

        elif isinstance(node, ast.UnaryOp):
            operand = self._convert_expr(node.operand)
            if isinstance(node.op, ast.Not):
                return f'!{operand}'
            elif isinstance(node.op, ast.USub):
                return f'-{operand}'
            elif isinstance(node.op, ast.UAdd):
                return f'+{operand}'
            elif isinstance(node.op, ast.Invert):
                return f'~{operand}'
            return operand

        elif isinstance(node, ast.Compare):
            left = self._convert_expr(node.left)
            parts = [left]
            for i, (op, comp) in enumerate(zip(node.ops, node.comparators)):
                op_str = self._convert_cmpop(op)
                comp_str = self._convert_expr(comp)
                if isinstance(op, ast.In):
                    self.imports.add('<algorithm>')
                    prev = parts[-1] if parts else left
                    return f'std::find({comp_str}.begin(), {comp_str}.end(), {prev}) != {comp_str}.end()'
                elif isinstance(op, ast.NotIn):
                    self.imports.add('<algorithm>')
                    prev = parts[-1] if parts else left
                    return f'std::find({comp_str}.begin(), {comp_str}.end(), {prev}) == {comp_str}.end()'
                parts.append(f'{op_str} {comp_str}')
            return ' '.join(parts)

        elif isinstance(node, ast.BoolOp):
            op = ' && ' if isinstance(node.op, ast.And) else ' || '
            values = [self._convert_expr(v) for v in node.values]
            return f'({op.join(values)})'

        elif isinstance(node, ast.IfExp):
            test = self._convert_expr(node.test)
            body = self._convert_expr(node.body)
            orelse = self._convert_expr(node.orelse)
            return f'({test} ? {body} : {orelse})'

        elif isinstance(node, ast.List):
            elts = [self._convert_expr(e) for e in node.elts]
            if elts:
                inner_type = self._infer_type(node.elts[0])
                return f'std::vector<{inner_type}>{{{", ".join(elts)}}}'
            return 'std::vector<int>{}'

        elif isinstance(node, ast.Dict):
            pairs = []
            for k, v in zip(node.keys, node.values):
                key = self._convert_expr(k)
                val = self._convert_expr(v)
                pairs.append(f'{{{key}, {val}}}')
            if pairs:
                key_type = self._infer_type(node.keys[0]) if node.keys else 'std::string'
                val_type = self._infer_type(node.values[0]) if node.values else 'int'
                return f'std::unordered_map<{key_type}, {val_type}>{{{", ".join(pairs)}}}'
            return 'std::unordered_map<std::string, int>{}'

        elif isinstance(node, ast.Set):
            elts = [self._convert_expr(e) for e in node.elts]
            if elts:
                inner_type = self._infer_type(node.elts[0])
                return f'std::unordered_set<{inner_type}>{{{", ".join(elts)}}}'
            return 'std::unordered_set<int>{}'

        elif isinstance(node, ast.Tuple):
            elts = [self._convert_expr(e) for e in node.elts]
            return f'std::make_tuple({", ".join(elts)})'

        elif isinstance(node, ast.Lambda):
            params = []
            for arg in node.args.args:
                params.append(f'auto {arg.arg}')
            body = self._convert_expr(node.body)
            return f'[&]({", ".join(params)}) {{ return {body}; }}'

        elif isinstance(node, ast.ListComp):
            self.imports.add('<algorithm>')
            elt = self._convert_expr(node.elt)
            gen = _safe_get(node.generators, 0)
            if gen:
                iter_var = self._convert_expr(gen.target)
                iter_src = self._convert_expr(gen.iter)
                cond_check = ''
                if gen.ifs:
                    cond = self._convert_expr(_safe_get(gen.ifs, 0))
                    cond_check = f' if({cond})'
                return f'[&](){{ std::vector<decltype({elt})> result; for(auto& {iter_var} : {iter_src}){cond_check} result.push_back({elt}); return result; }}()'
            return f'std::vector<decltype({elt})>{{}}'

        elif isinstance(node, ast.DictComp):
            # Dict comprehension: {k: v for k, v in items}
            key_expr = self._convert_expr(node.key)
            val_expr = self._convert_expr(node.value)
            gen = _safe_get(node.generators, 0)
            if gen:
                iter_var = self._convert_expr(gen.target)
                iter_src = self._convert_expr(gen.iter)
                cond_check = ''
                if gen.ifs:
                    cond = self._convert_expr(_safe_get(gen.ifs, 0))
                    cond_check = f' if({cond})'
                return f'[&](){{ std::unordered_map<decltype({key_expr}), decltype({val_expr})> result; for(auto& {iter_var} : {iter_src}){cond_check} result[{key_expr}] = {val_expr}; return result; }}()'
            return f'std::unordered_map<decltype({key_expr}), decltype({val_expr})>{{}}'

        elif isinstance(node, ast.SetComp):
            # Set comprehension: {x for x in items}
            elt = self._convert_expr(node.elt)
            gen = _safe_get(node.generators, 0)
            if gen:
                iter_var = self._convert_expr(gen.target)
                iter_src = self._convert_expr(gen.iter)
                cond_check = ''
                if gen.ifs:
                    cond = self._convert_expr(_safe_get(gen.ifs, 0))
                    cond_check = f' if({cond})'
                return f'[&](){{ std::unordered_set<decltype({elt})> result; for(auto& {iter_var} : {iter_src}){cond_check} result.insert({elt}); return result; }}()'
            return f'std::unordered_set<decltype({elt})>{{}}'

        elif isinstance(node, ast.GeneratorExp):
            # Generator expression: (x for x in items) - convert to vector for C++
            elt = self._convert_expr(node.elt)
            gen = _safe_get(node.generators, 0)
            if gen:
                iter_var = self._convert_expr(gen.target)
                iter_src = self._convert_expr(gen.iter)
                cond_check = ''
                if gen.ifs:
                    cond = self._convert_expr(_safe_get(gen.ifs, 0))
                    cond_check = f' if({cond})'
                return f'[&](){{ std::vector<decltype({elt})> result; for(auto& {iter_var} : {iter_src}){cond_check} result.push_back({elt}); return result; }}()'
            return f'std::vector<decltype({elt})>{{}}'

        elif isinstance(node, ast.Slice):
            lower = self._convert_expr(node.lower) if node.lower else '0'
            upper = self._convert_expr(node.upper) if node.upper else ''
            return f'{lower}:{upper}'

        elif isinstance(node, ast.JoinedStr):
            # f-string: convert to std::string concatenation or std::format
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    # Plain string part
                    escaped = str(value.value).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t').replace('\0', '\\0')
                    parts.append(f'"{escaped}"')
                elif isinstance(value, ast.FormattedValue):
                    # {expr} part - convert to std::to_string or direct if already string
                    expr = self._convert_expr(value.value)
                    # Check if it's a string type (no std::to_string needed)
                    is_string_type = self._is_string_expr(value.value, expr)
                    if is_string_type:
                        parts.append(expr)
                    else:
                        parts.append(f'std::to_string({expr})')
                else:
                    parts.append(self._convert_expr(value))
            if not parts:
                return '""'
            return ' + '.join(parts)

        elif isinstance(node, ast.FormattedValue):
            # Standalone formatted value (rare, usually inside JoinedStr)
            return self._convert_expr(node.value)

        # Unknown AST node - add warning and return placeholder
        node_type = type(node).__name__
        line_info = getattr(node, 'lineno', '?')
        self.warnings.append(f"Unsupported AST node '{node_type}' at line {line_info}")
        return f'/* unsupported: {node_type} at line {line_info} */'

    def _convert_binop(self, op) -> str:
        ops = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.FloorDiv: '/',
            ast.Mod: '%',
            ast.Pow: '**',
            ast.LShift: '<<',
            ast.RShift: '>>',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.BitAnd: '&',
            ast.MatMult: '*',
        }
        return ops.get(type(op), '+')

    def _convert_cmpop(self, op) -> str:
        ops = {
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Is: '==',
            ast.IsNot: '!=',
            ast.In: 'in',
            ast.NotIn: 'not in',
        }
        return ops.get(type(op), '==')

    def _get_attr_name(self, node) -> str:
        if isinstance(node, ast.Attribute):
            value = self._get_attr_name(node.value)
            return f'{value}::{node.attr}'
        elif isinstance(node, ast.Name):
            return node.id
        return ''

    def _format_params(self, params: List[Tuple[str, str]]) -> str:
        return ', '.join(f'{ptype} {pname}' for pname, ptype in params)

    def _needs_template(self, params: List[Tuple[str, str]]) -> bool:
        """Check if any parameter requires a template (has T_CONTAINER or T_ELEMENT type)."""
        return any(ptype in (self.TEMPLATE_MARKER, self.TEMPLATE_ELEMENT) for _, ptype in params)

    def _has_container_param(self, params: List[Tuple[str, str]]) -> bool:
        """Check if params include a T_CONTAINER (useful for element type matching)."""
        return any(ptype == self.TEMPLATE_MARKER for _, ptype in params)

    def _get_template_return_type(self, return_type: str, body: str, params: List[Tuple[str, str]]) -> str:
        """Determine the proper return type for a template function."""
        # If return type is already explicit, use it
        if return_type not in ('auto', 'void'):
            return return_type
        if return_type == 'void':
            return 'void'

        # Get container parameter names
        container_params = [pname for pname, ptype in params if ptype == self.TEMPLATE_MARKER]

        # Check if body returns one of the container parameters (e.g., shuffle_list returns items)
        # Look for patterns like "return items" where items is a container param
        for pname in container_params:
            if re.search(rf'\breturn\s+{re.escape(pname)}\b', body):
                return 'std::vector<T>'

        # Default to T for functions that return an element
        return 'T'

    def _generate_explicit_instantiation(self, func_name: str, params: List[Tuple[str, str]],
                                          return_type: str, class_name: str = None,
                                          const: str = '') -> List[str]:
        """Generate explicit template instantiations for common types."""
        lines = ['// Explicit instantiations']

        has_element_param = any(ptype == self.TEMPLATE_ELEMENT for _, ptype in params)

        for cpp_type in ['int', 'double', 'std::string']:
            # Build parameter list for instantiation
            inst_params = []
            for pname, ptype in params:
                if ptype == self.TEMPLATE_MARKER:
                    inst_params.append(f'const std::vector<{cpp_type}>&')
                elif ptype == self.TEMPLATE_ELEMENT:
                    inst_params.append(f'const {cpp_type}&')
                # Skip non-template params in explicit instantiation signature

            params_str = ', '.join(inst_params)

            # Determine return type for instantiation
            if return_type == 'std::vector<T>':
                inst_ret = f'std::vector<{cpp_type}>'
            elif return_type == 'T':
                inst_ret = cpp_type
            else:
                inst_ret = return_type

            if class_name:
                lines.append(f'template {inst_ret} {class_name}::{func_name}<{cpp_type}>({params_str}){const};')
            else:
                lines.append(f'template {inst_ret} {func_name}<{cpp_type}>({params_str});')

        return lines

    def _format_params_with_const_ref(self, params: List[Tuple[str, str]], use_template: bool = False) -> str:
        has_container = self._has_container_param(params)
        result = []
        for pname, ptype in params:
            # Handle template container marker
            if ptype == self.TEMPLATE_MARKER:
                result.append(f'const std::vector<T>& {pname}')
            # Handle template element marker - only becomes T if there's also a container param
            elif ptype == self.TEMPLATE_ELEMENT:
                if has_container:
                    result.append(f'const T& {pname}')
                else:
                    result.append(f'double {pname}')  # Fallback to double if no container context
            elif ptype in ('std::string', 'std::vector', 'std::unordered_map', 'std::unordered_set') or ptype.startswith('std::'):
                result.append(f'const {ptype}& {pname}')
            else:
                result.append(f'{ptype} {pname}')
        return ', '.join(result)

    def _generate_header(self, module_name: str, classes: List[ClassInfo],
                         functions: List[FunctionInfo], global_vars: List) -> str:
        lines = []
        guard = f'{module_name.upper()}_H'

        lines.append(f'#ifndef {guard}')
        lines.append(f'#define {guard}')
        lines.append('')

        std_includes = {'<string>', '<vector>', '<unordered_map>', '<unordered_set>',
                        '<tuple>', '<optional>', '<functional>', '<memory>', '<cstdint>'}
        std_includes.update(self.imports)
        for inc in sorted(std_includes):
            lines.append(f'#include {inc}')
        lines.append('')

        lines.append('namespace includecpp {')
        lines.append('')

        for name, var_type, _ in global_vars:
            lines.append(f'extern {var_type} {name};')

        if global_vars:
            lines.append('')

        for cls in classes:
            if cls.bases:
                bases_str = ', '.join(f'public {b}' for b in cls.bases)
                lines.append(f'class {cls.name} : {bases_str} {{')
            else:
                lines.append(f'class {cls.name} {{')
            lines.append('public:')

            for fname, ftype, fval in cls.fields:
                # 'auto' is invalid for class members - infer from value or use default
                if ftype == 'auto':
                    if fval:
                        # Try to infer from the default value expression
                        if fval.startswith('"') or fval.startswith("'"):
                            ftype = 'std::string'
                        elif fval in ('true', 'false'):
                            ftype = 'bool'
                        elif '.' in fval and fval.replace('.', '').replace('-', '').isdigit():
                            ftype = 'double'
                        elif fval.lstrip('-').isdigit():
                            ftype = 'int'
                        elif fval.startswith('{') or fval.startswith('std::vector'):
                            ftype = 'std::vector<int>'
                        else:
                            ftype = 'int'  # Default fallback
                    else:
                        ftype = 'int'  # Default for uninitialized
                lines.append(f'    {ftype} {fname};')

            if cls.fields:
                lines.append('')

            for ctor in cls.constructors:
                params = self._format_params_with_const_ref(ctor.params)
                lines.append(f'    {cls.name}({params});')

            for method in cls.methods:
                params = self._format_params_with_const_ref(method.params)
                static = 'static ' if method.is_static else ''
                const = ' const' if method.is_const else ''
                # Add template prefix if method uses generic containers
                if self._needs_template(method.params):
                    lines.append(f'    template<typename T>')
                    ret_type = self._get_template_return_type(method.return_type, method.body, method.params)
                    lines.append(f'    {static}{ret_type} {method.name}({params}){const};')
                else:
                    lines.append(f'    {static}{method.return_type} {method.name}({params}){const};')

            lines.append('};')
            lines.append('')

        for func in functions:
            params = self._format_params_with_const_ref(func.params)
            # Add template prefix if function uses generic containers
            if self._needs_template(func.params):
                lines.append('template<typename T>')
                ret_type = self._get_template_return_type(func.return_type, func.body, func.params)
                lines.append(f'{ret_type} {func.name}({params});')
            else:
                lines.append(f'{func.return_type} {func.name}({params});')

        lines.append('')
        lines.append('} // namespace includecpp')
        lines.append('')
        lines.append(f'#endif // {guard}')

        return '\n'.join(lines)

    def _generate_source(self, module_name: str, classes: List[ClassInfo],
                         functions: List[FunctionInfo], global_vars: List) -> str:
        lines = []

        lines.append(f'#include "{module_name}.h"')
        lines.append('#include <iostream>')
        lines.append('#include <cmath>')
        lines.append('#include <stdexcept>')
        lines.append('')
        lines.append('namespace includecpp {')
        lines.append('')

        # Add random helper functions if needed
        if '<random>' in self.imports:
            lines.append('// Random number generation helpers')
            lines.append('static std::mt19937& _get_rng() {')
            lines.append('    static std::random_device rd;')
            lines.append('    static std::mt19937 gen(rd());')
            lines.append('    return gen;')
            lines.append('}')
            lines.append('')
            lines.append('inline int _rng_uniform_int(int a, int b) {')
            lines.append('    std::uniform_int_distribution<int> dist(a, b);')
            lines.append('    return dist(_get_rng());')
            lines.append('}')
            lines.append('')
            lines.append('inline double _rng_uniform_real(double a, double b) {')
            lines.append('    std::uniform_real_distribution<double> dist(a, b);')
            lines.append('    return dist(_get_rng());')
            lines.append('}')
            lines.append('')
            lines.append('template<typename T>')
            lines.append('inline T _rng_choice(const std::vector<T>& choices) {')
            lines.append('    if (choices.empty()) throw std::runtime_error("Cannot choose from empty list");')
            lines.append('    std::uniform_int_distribution<size_t> dist(0, choices.size() - 1);')
            lines.append('    return choices[dist(_get_rng())];')
            lines.append('}')
            lines.append('')
            lines.append('template<typename T>')
            lines.append('inline std::vector<T> _rng_sample(const std::vector<T>& population, size_t k) {')
            lines.append('    if (k > population.size()) throw std::runtime_error("Sample larger than population");')
            lines.append('    std::vector<T> result = population;')
            lines.append('    std::shuffle(result.begin(), result.end(), _get_rng());')
            lines.append('    result.resize(k);')
            lines.append('    return result;')
            lines.append('}')
            lines.append('')
            lines.append('template<typename T>')
            lines.append('inline std::vector<T> _rng_shuffle(std::vector<T> lst) {')
            lines.append('    std::shuffle(lst.begin(), lst.end(), _get_rng());')
            lines.append('    return lst;')
            lines.append('}')
            lines.append('')
            lines.append('inline std::vector<uint8_t> _rng_bytes(size_t n) {')
            lines.append('    std::vector<uint8_t> result(n);')
            lines.append('    std::uniform_int_distribution<int> dist(0, 255);')
            lines.append('    for (size_t i = 0; i < n; ++i) result[i] = static_cast<uint8_t>(dist(_get_rng()));')
            lines.append('    return result;')
            lines.append('}')
            lines.append('')
            lines.append('inline double _rng_normal(double mu, double sigma) {')
            lines.append('    std::normal_distribution<double> dist(mu, sigma);')
            lines.append('    return dist(_get_rng());')
            lines.append('}')
            lines.append('')
            lines.append('inline double _rng_exponential(double lambda) {')
            lines.append('    std::exponential_distribution<double> dist(lambda);')
            lines.append('    return dist(_get_rng());')
            lines.append('}')
            lines.append('')
            lines.append('inline double _rng_lognormal(double mu, double sigma) {')
            lines.append('    std::lognormal_distribution<double> dist(mu, sigma);')
            lines.append('    return dist(_get_rng());')
            lines.append('}')
            lines.append('')
            lines.append('inline double _rng_beta(double alpha, double beta) {')
            lines.append('    // Beta distribution via gamma distributions')
            lines.append('    std::gamma_distribution<double> dist_a(alpha, 1.0);')
            lines.append('    std::gamma_distribution<double> dist_b(beta, 1.0);')
            lines.append('    double x = dist_a(_get_rng());')
            lines.append('    double y = dist_b(_get_rng());')
            lines.append('    return x / (x + y);')
            lines.append('}')
            lines.append('')
            lines.append('template<typename T>')
            lines.append('inline T _rng_weighted_choice(const std::vector<T>& choices, const std::vector<double>& weights) {')
            lines.append('    if (choices.empty()) throw std::runtime_error("Cannot choose from empty list");')
            lines.append('    std::discrete_distribution<size_t> dist(weights.begin(), weights.end());')
            lines.append('    return choices[dist(_get_rng())];')
            lines.append('}')
            lines.append('')

        # Add filesystem helper functions if needed
        if '<filesystem>' in self.imports:
            lines.append('// Filesystem helpers')
            lines.append('inline std::vector<std::string> _os_listdir(const std::string& path) {')
            lines.append('    std::vector<std::string> result;')
            lines.append('    for (const auto& entry : std::filesystem::directory_iterator(path)) {')
            lines.append('        result.push_back(entry.path().filename().string());')
            lines.append('    }')
            lines.append('    return result;')
            lines.append('}')
            lines.append('')
            lines.append('inline std::string _path_join(const std::string& a, const std::string& b) {')
            lines.append('    return (std::filesystem::path(a) / b).string();')
            lines.append('}')
            lines.append('')
            lines.append('inline std::string _path_dirname(const std::string& path) {')
            lines.append('    return std::filesystem::path(path).parent_path().string();')
            lines.append('}')
            lines.append('')
            lines.append('inline std::string _path_basename(const std::string& path) {')
            lines.append('    return std::filesystem::path(path).filename().string();')
            lines.append('}')
            lines.append('')
            lines.append('inline std::pair<std::string, std::string> _path_splitext(const std::string& path) {')
            lines.append('    auto p = std::filesystem::path(path);')
            lines.append('    return {p.stem().string(), p.extension().string()};')
            lines.append('}')
            lines.append('')

        # Add time helper functions if needed
        if '<chrono>' in self.imports:
            lines.append('// Time helpers')
            lines.append('inline double _time_now() {')
            lines.append('    auto now = std::chrono::system_clock::now();')
            lines.append('    auto duration = now.time_since_epoch();')
            lines.append('    return std::chrono::duration<double>(duration).count();')
            lines.append('}')
            lines.append('')
            lines.append('inline double _time_perf_counter() {')
            lines.append('    static auto start = std::chrono::high_resolution_clock::now();')
            lines.append('    auto now = std::chrono::high_resolution_clock::now();')
            lines.append('    return std::chrono::duration<double>(now - start).count();')
            lines.append('}')
            lines.append('')
            lines.append('inline double _time_monotonic() {')
            lines.append('    static auto start = std::chrono::steady_clock::now();')
            lines.append('    auto now = std::chrono::steady_clock::now();')
            lines.append('    return std::chrono::duration<double>(now - start).count();')
            lines.append('}')
            lines.append('')

        # Add sys helpers if needed
        if '_sys_platform' in '\n'.join(lines) or 'sys' in self.python_imports:
            lines.append('// Sys helpers')
            lines.append('inline std::string _sys_platform() {')
            lines.append('#ifdef _WIN32')
            lines.append('    return "win32";')
            lines.append('#elif __APPLE__')
            lines.append('    return "darwin";')
            lines.append('#elif __linux__')
            lines.append('    return "linux";')
            lines.append('#else')
            lines.append('    return "unknown";')
            lines.append('#endif')
            lines.append('}')
            lines.append('')

        # Add regex helpers if needed
        if '<regex>' in self.imports:
            lines.append('// Regex helpers')
            lines.append('inline std::vector<std::string> _regex_findall(const std::string& pattern, const std::string& text) {')
            lines.append('    std::vector<std::string> results;')
            lines.append('    std::regex re(pattern);')
            lines.append('    auto begin = std::sregex_iterator(text.begin(), text.end(), re);')
            lines.append('    auto end = std::sregex_iterator();')
            lines.append('    for (auto it = begin; it != end; ++it) {')
            lines.append('        results.push_back((*it)[0].str());')
            lines.append('    }')
            lines.append('    return results;')
            lines.append('}')
            lines.append('')

        for name, var_type, value in global_vars:
            if value:
                lines.append(f'{var_type} {name} = {value};')
            else:
                lines.append(f'{var_type} {name};')

        if global_vars:
            lines.append('')

        for cls in classes:
            for ctor in cls.constructors:
                params = self._format_params_with_const_ref(ctor.params)
                lines.append(f'{cls.name}::{cls.name}({params}) {{')

                for fname, ftype, fdefault in cls.fields:
                    init_val = None
                    for pname, _ in ctor.params:
                        if pname == fname:
                            init_val = pname
                            break
                    if init_val:
                        lines.append(f'    this->{fname} = {init_val};')
                    elif fdefault:
                        lines.append(f'    this->{fname} = {fdefault};')

                ctor_body_lines = ctor.body.split('\n')
                for line in ctor_body_lines:
                    if 'this->' in line and '=' in line:
                        pass
                    elif line.strip():
                        lines.append(line)

                lines.append('}')
                lines.append('')

            for method in cls.methods:
                params = self._format_params_with_const_ref(method.params)
                const = ' const' if method.is_const else ''
                # Add template prefix if method uses generic containers
                if self._needs_template(method.params):
                    lines.append('template<typename T>')
                    ret_type = self._get_template_return_type(method.return_type, method.body, method.params)
                    lines.append(f'{ret_type} {cls.name}::{method.name}({params}){const} {{')
                else:
                    lines.append(f'{method.return_type} {cls.name}::{method.name}({params}){const} {{')
                lines.append(method.body)
                lines.append('}')
                # Add explicit template instantiations for common types
                if self._needs_template(method.params):
                    ret_type = self._get_template_return_type(method.return_type, method.body, method.params)
                    inst_lines = self._generate_explicit_instantiation(
                        method.name, method.params, ret_type, cls.name, const)
                    lines.extend(inst_lines)
                lines.append('')

        for func in functions:
            params = self._format_params_with_const_ref(func.params)
            # Add template prefix if function uses generic containers
            if self._needs_template(func.params):
                lines.append('template<typename T>')
                ret_type = self._get_template_return_type(func.return_type, func.body, func.params)
                lines.append(f'{ret_type} {func.name}({params}) {{')
            else:
                lines.append(f'{func.return_type} {func.name}({params}) {{')
            lines.append(func.body)
            lines.append('}')
            # Add explicit template instantiations for common types
            if self._needs_template(func.params):
                ret_type = self._get_template_return_type(func.return_type, func.body, func.params)
                inst_lines = self._generate_explicit_instantiation(func.name, func.params, ret_type)
                lines.extend(inst_lines)
            lines.append('')

        lines.append('} // namespace includecpp')

        return '\n'.join(lines)


class CppToPythonConverter:
    def __init__(self):
        self.indent = '    '
        self._current_class_fields = set()  # Track fields for self. prefix

    def convert(self, source: str, module_name: str) -> str:
        """Convert C++ source to Python."""
        lines = []

        source = self._remove_comments(source)

        # Extract namespace content
        namespace_content = self._extract_namespace_content(source)
        if namespace_content:
            source = namespace_content

        imports_needed = set()
        if 'std::sqrt' in source or 'std::cos' in source or 'std::sin' in source or 'M_PI' in source:
            imports_needed.add('math')
        if 'std::vector' in source or 'std::string' in source:
            imports_needed.add('typing')

        # Add imports
        if 'typing' in imports_needed:
            lines.append('from typing import List, Dict, Set, Tuple, Optional, Any, Callable')
        if 'math' in imports_needed:
            lines.append('import math')
        if imports_needed:
            lines.append('')

        structs = self._parse_structs(source)
        classes = self._parse_classes(source)
        functions = self._parse_functions(source)
        constants = self._parse_constants(source)

        # Add dataclass import if structs exist
        if structs:
            lines.insert(0, 'from dataclasses import dataclass, field')
            if not lines[1].startswith('from typing'):
                lines.insert(1, '')

        for const_name, const_val in constants:
            lines.append(f'{const_name} = {const_val}')

        if constants:
            lines.append('')

        for struct in structs:
            lines.extend(self._generate_struct(struct))
            lines.append('')

        for cls in classes:
            lines.extend(self._generate_class(cls))
            lines.append('')

        for func in functions:
            lines.extend(self._generate_function(func))
            lines.append('')

        return '\n'.join(lines)

    def _remove_comments(self, source: str) -> str:
        source = re.sub(r'//.*$', '', source, flags=re.MULTILINE)
        source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
        return source

    def _extract_namespace_content(self, source: str) -> Optional[str]:
        """Extract content from namespace includecpp { ... }"""
        match = re.search(r'namespace\s+includecpp\s*\{(.*)$', source, re.DOTALL)
        if match:
            content = match.group(1)
            depth = 1
            end_pos = 0
            for i, char in enumerate(content):
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        end_pos = i
                        break
            return content[:end_pos]
        return None

    def _parse_constants(self, source: str) -> List[Tuple[str, str]]:
        """Parse constexpr/const global values."""
        constants = []
        pattern = r'(?:constexpr|const)\s+(\w+)\s+(\w+)\s*=\s*([^;]+);'
        for match in re.finditer(pattern, source):
            # group(1) is type (not used in Python), group(2) is name, group(3) is value
            const_name = match.group(2)
            const_val = self._convert_cpp_expr(match.group(3).strip())
            constants.append((const_name, const_val))
        return constants

    def _parse_functions(self, source: str) -> List[FunctionInfo]:
        functions = []

        # Match function with body
        pattern = r'(?:(?:static|inline|virtual|explicit|constexpr)\s+)*(\w+(?:<[^>]+>)?(?:\s*[*&])?)\s+(\w+)\s*\(([^)]*)\)\s*(?:const)?\s*\{([^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*)\}'

        for match in re.finditer(pattern, source):
            return_type = match.group(1).strip()
            name = match.group(2)
            params_str = match.group(3).strip()
            body = match.group(4)

            if name in ('if', 'while', 'for', 'switch', 'catch'):
                continue

            params = self._parse_params(params_str)
            py_body = self._convert_cpp_body(body)

            functions.append(FunctionInfo(
                name=name,
                return_type=self._convert_cpp_type(return_type),
                params=[(n, self._convert_cpp_type(t)) for n, t in params],
                body=py_body
            ))

        return functions

    def _parse_classes(self, source: str) -> List[ClassInfo]:
        classes = []

        pattern = r'class\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+(\w+))?\s*\{([^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*)\}'

        for match in re.finditer(pattern, source):
            name = match.group(1)
            base = match.group(2)
            body = match.group(3)

            fields = self._parse_class_fields(body)
            field_names = {f[0] for f in fields}  # Extract field names for self. prefix
            methods = self._parse_class_methods(body, name, field_names)
            constructors = self._parse_constructors(body, name, field_names)

            classes.append(ClassInfo(
                name=name,
                bases=[base] if base else [],
                methods=methods,
                fields=fields,
                constructors=constructors
            ))

            # Clear class fields after processing this class
            self._current_class_fields = set()

        return classes

    def _parse_structs(self, source: str) -> List[StructInfo]:
        structs = []

        pattern = r'struct\s+(\w+)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'

        for match in re.finditer(pattern, source):
            name = match.group(1)
            body = match.group(2)

            fields = []
            field_pattern = r'(\w+(?:<[^>]+>)?(?:\s*[*&])?)\s+(\w+)\s*(?:=\s*[^;]+)?;'
            for fm in re.finditer(field_pattern, body):
                field_type = fm.group(1).strip()
                field_name = fm.group(2)
                if field_name not in ('if', 'for', 'while', 'return'):
                    fields.append((field_name, self._convert_cpp_type(field_type)))

            structs.append(StructInfo(name=name, fields=fields))

        return structs

    def _parse_params(self, params_str: str) -> List[Tuple[str, str]]:
        if not params_str.strip():
            return []

        params = []
        depth = 0
        current = ''

        for char in params_str:
            if char == '<':
                depth += 1
            elif char == '>':
                depth -= 1
            elif char == ',' and depth == 0:
                params.append(current.strip())
                current = ''
                continue
            current += char

        if current.strip():
            params.append(current.strip())

        result = []
        for param in params:
            param = param.strip()
            if not param:
                continue

            param = re.sub(r'^const\s+', '', param)
            param = re.sub(r'\s*[&*]+\s*', ' ', param)

            parts = param.rsplit(None, 1)
            if len(parts) == 2:
                ptype, pname = parts
                pname = re.sub(r'=.*$', '', pname).strip()
                result.append((pname, ptype))
            elif len(parts) == 1:
                result.append((parts[0], 'auto'))

        return result

    def _parse_class_fields(self, body: str) -> List[Tuple[str, str, Optional[str]]]:
        fields = []
        all_field_names = set()  # v3.4.1: Track ALL fields for self. prefix

        # v3.4.1: Parse fields from ALL sections (public, private, protected)
        # for self. prefix detection, but only return public fields for dataclass
        sections = re.split(r'(?:public|private|protected)\s*:', body)

        field_pattern = r'(\w+(?:<[^>]+>)?)\s+(\w+)\s*(?:=\s*([^;]+))?\s*;'

        # First pass: collect ALL field names from all sections
        for section in sections:
            for match in re.finditer(field_pattern, section):
                field_type = match.group(1)
                field_name = match.group(2)

                if '(' in field_type or field_type in ('return', 'if', 'for', 'while'):
                    continue

                all_field_names.add(field_name)

        # Store all field names for self. prefix detection
        self._current_class_fields = all_field_names

        # Second pass: return only public fields for the Python class definition
        public_section = sections[1] if len(sections) > 1 else body

        for match in re.finditer(field_pattern, public_section):
            field_type = match.group(1)
            field_name = match.group(2)
            default = match.group(3)

            if '(' in field_type or field_type in ('return', 'if', 'for', 'while'):
                continue

            py_default = self._convert_cpp_expr(default) if default else None
            fields.append((field_name, self._convert_cpp_type(field_type), py_default))

        return fields

    def _parse_class_methods(self, body: str, class_name: str, field_names: set = None) -> List[FunctionInfo]:
        methods = []

        # Set current class fields for self. prefix during body conversion
        if field_names:
            self._current_class_fields = field_names

        pattern = r'(?:(static|virtual)\s+)?(\w+(?:<[^>]+>)?(?:\s*[*&])?)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|;)'

        for match in re.finditer(pattern, body):
            modifier = match.group(1)
            return_type = match.group(2).strip()
            name = match.group(3)
            params_str = match.group(4)
            is_const = match.group(5) is not None
            method_body = match.group(6) or ''

            if name == class_name or name == f'~{class_name}':
                continue

            params = self._parse_params(params_str)
            py_body = self._convert_cpp_body(method_body)

            methods.append(FunctionInfo(
                name=name,
                return_type=self._convert_cpp_type(return_type),
                params=[(n, self._convert_cpp_type(t)) for n, t in params],
                body=py_body,
                is_method=True,
                is_static=(modifier == 'static'),
                is_const=is_const
            ))

        return methods

    def _parse_constructors(self, body: str, class_name: str, field_names: set = None) -> List[FunctionInfo]:
        constructors = []

        # Set current class fields for self. prefix during body conversion
        if field_names:
            self._current_class_fields = field_names

        pattern = rf'{class_name}\s*\(([^)]*)\)\s*(?::\s*[^{{]+)?\s*\{{([^{{}}]*(?:\{{[^{{}}]*\}}[^{{}}]*)*)\}}'

        for match in re.finditer(pattern, body):
            params_str = match.group(1)
            ctor_body = match.group(2)

            params = self._parse_params(params_str)
            py_body = self._convert_cpp_body(ctor_body)

            constructors.append(FunctionInfo(
                name='__init__',
                return_type='None',
                params=[(n, self._convert_cpp_type(t)) for n, t in params],
                body=py_body,
                is_method=True
            ))

        return constructors

    def _convert_cpp_type(self, cpp_type: str) -> str:
        cpp_type = cpp_type.strip()
        cpp_type = re.sub(r'^const\s+', '', cpp_type)
        cpp_type = re.sub(r'\s*[&*]+\s*$', '', cpp_type)
        cpp_type = cpp_type.strip()

        template_match = re.match(r'(\w+(?:::\w+)?)<(.+)>$', cpp_type)
        if template_match:
            container = template_match.group(1)
            inner = template_match.group(2)

            py_container = CPP_TO_PY_TYPES.get(container, container)

            inner_types = self._split_template_args(inner)
            py_inner = [self._convert_cpp_type(t) for t in inner_types]

            if py_container == 'list':
                return f'List[{py_inner[0]}]' if py_inner else 'List'
            elif py_container == 'dict':
                if len(py_inner) >= 2:
                    return f'Dict[{py_inner[0]}, {py_inner[1]}]'
                return 'Dict'
            elif py_container == 'set':
                return f'Set[{py_inner[0]}]' if py_inner else 'Set'
            elif py_container == 'tuple':
                return f'Tuple[{", ".join(py_inner)}]'
            elif py_container == 'Optional':
                return f'Optional[{py_inner[0]}]' if py_inner else 'Optional'

        return CPP_TO_PY_TYPES.get(cpp_type, cpp_type)

    def _split_template_args(self, args: str) -> List[str]:
        result = []
        depth = 0
        current = ''

        for char in args:
            if char == '<':
                depth += 1
                current += char
            elif char == '>':
                depth -= 1
                current += char
            elif char == ',' and depth == 0:
                result.append(current.strip())
                current = ''
            else:
                current += char

        if current.strip():
            result.append(current.strip())

        return result

    def _convert_cpp_body(self, body: str) -> str:
        if not body.strip():
            return 'pass'

        lines = []
        statements = self._split_statements(body)

        for stmt in statements:
            py_line = self._convert_cpp_statement(stmt)
            if py_line:
                lines.append(py_line)

        return '\n'.join(lines) if lines else 'pass'

    def _split_statements(self, body: str) -> List[str]:
        """Split C++ body into statements, handling for loops correctly."""
        statements = []
        current = ''
        depth = 0
        in_for = False
        for_paren_depth = 0

        i = 0
        while i < len(body):
            char = body[i]

            if body[i:i+3] == 'for' and (i == 0 or not body[i-1].isalnum()):
                in_for = True

            if char == '(':
                if in_for and for_paren_depth == 0:
                    for_paren_depth = 1
                elif in_for:
                    for_paren_depth += 1
                depth += 1
            elif char == ')':
                if in_for:
                    for_paren_depth -= 1
                    if for_paren_depth == 0:
                        in_for = False
                depth -= 1
            elif char == '{':
                depth += 1
            elif char == '}':
                depth -= 1

            if char == ';' and depth == 0 and not in_for:
                statements.append(current.strip())
                current = ''
            else:
                current += char

            i += 1

        if current.strip():
            statements.append(current.strip())

        return statements

    def _convert_cpp_statement(self, stmt: str) -> str:
        stmt = stmt.strip()
        if not stmt or stmt == '{' or stmt == '}':
            return ''

        # Handle for loops
        for_match = re.match(r'for\s*\(\s*(?:size_t|int|auto)\s+(\w+)\s*=\s*(\d+)\s*;\s*\1\s*<\s*(.+?)\s*;\s*(?:\+\+\1|\1\s*\+\+|\1\s*\+=\s*\d+)\s*\)\s*\{(.*)\}', stmt, re.DOTALL)
        if for_match:
            var = for_match.group(1)
            start = for_match.group(2)
            end = self._convert_cpp_expr(for_match.group(3))
            body = for_match.group(4)
            body_stmts = self._split_statements(body)
            body_lines = []
            for s in body_stmts:
                converted = self._convert_cpp_statement(s)
                if converted:
                    body_lines.append(f'    {converted}')
            body_str = '\n'.join(body_lines) if body_lines else '    pass'
            if start == '0':
                return f'for {var} in range({end}):\n{body_str}'
            else:
                return f'for {var} in range({start}, {end}):\n{body_str}'

        # Range-based for loop
        range_for_match = re.match(r'for\s*\(\s*(?:const\s+)?(?:auto|[\w:]+)[&*]?\s+(\w+)\s*:\s*(.+?)\s*\)\s*\{(.*)\}', stmt, re.DOTALL)
        if range_for_match:
            var = range_for_match.group(1)
            container = self._convert_cpp_expr(range_for_match.group(2))
            body = range_for_match.group(3)
            body_stmts = self._split_statements(body)
            body_lines = []
            for s in body_stmts:
                converted = self._convert_cpp_statement(s)
                if converted:
                    body_lines.append(f'    {converted}')
            body_str = '\n'.join(body_lines) if body_lines else '    pass'
            return f'for {var} in {container}:\n{body_str}'

        # If statement
        if_match = re.match(r'if\s*\((.+?)\)\s*\{(.*)\}(?:\s*else\s*\{(.*)\})?', stmt, re.DOTALL)
        if if_match:
            cond = self._convert_cpp_expr(if_match.group(1))
            if_body = if_match.group(2)
            else_body = if_match.group(3)
            if_stmts = self._split_statements(if_body)
            if_lines = []
            for s in if_stmts:
                converted = self._convert_cpp_statement(s)
                if converted:
                    if_lines.append(f'    {converted}')
            if_str = '\n'.join(if_lines) if if_lines else '    pass'
            result = f'if {cond}:\n{if_str}'
            if else_body:
                else_stmts = self._split_statements(else_body)
                else_lines = []
                for s in else_stmts:
                    converted = self._convert_cpp_statement(s)
                    if converted:
                        else_lines.append(f'    {converted}')
                else_str = '\n'.join(else_lines) if else_lines else '    pass'
                result += f'\nelse:\n{else_str}'
            return result

        # Single line if with continue/break
        if_single = re.match(r'if\s*\((.+?)\)\s*(continue|break|return[^;]*)', stmt)
        if if_single:
            cond = self._convert_cpp_expr(if_single.group(1))
            action = if_single.group(2).strip()
            if action.startswith('return'):
                ret_val = action[6:].strip()
                if ret_val:
                    return f'if {cond}:\n    return {self._convert_cpp_expr(ret_val)}'
                return f'if {cond}:\n    return'
            return f'if {cond}:\n    {action}'

        if stmt.startswith('return'):
            expr = stmt[6:].strip()
            if not expr:
                return 'return'
            return f'return {self._convert_cpp_expr(expr)}'

        if stmt == 'continue':
            return 'continue'

        if stmt == 'break':
            return 'break'

        # Variable declaration with initialization
        var_match = re.match(r'(?:const\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*=\s*(.+)$', stmt)
        if var_match:
            var_name = var_match.group(2)
            value = self._convert_cpp_expr(var_match.group(3))
            return f'{var_name} = {value}'

        # Variable declaration without initialization
        decl_match = re.match(r'(?:const\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)$', stmt)
        if decl_match:
            var_type = decl_match.group(1)
            var_name = decl_match.group(2)
            if var_name not in ('if', 'for', 'while', 'return'):
                return f'{var_name} = {self._get_default_value(var_type)}'

        # Assignment - v3.3.22: Expanded pattern to capture -> and ::
        assign_match = re.match(r'([a-zA-Z_][\w:>-]*(?:->|\.)?[a-zA-Z_][\w]*(?:\[[^\]]+\])?)\s*=\s*(.+)$', stmt)
        if assign_match:
            target = assign_match.group(1)
            # v3.3.22: Apply full expression conversion to target as well
            target = self._convert_cpp_expr(target)
            value = self._convert_cpp_expr(assign_match.group(2))
            return f'{target} = {value}'

        # Augmented assignment
        aug_match = re.match(r'(\w+(?:\.\w+)*)\s*(\+\+|--|\+=|-=|\*=|/=)', stmt)
        if aug_match:
            # v3.3.22: Apply full expression conversion to target
            target = self._convert_cpp_expr(aug_match.group(1))
            op = aug_match.group(2)
            if op == '++':
                return f'{target} += 1'
            elif op == '--':
                return f'{target} -= 1'
            # Handle += with value
            rest = stmt[aug_match.end():].strip()
            if rest:
                return f'{target} {op} {self._convert_cpp_expr(rest)}'

        return self._convert_cpp_expr(stmt)

    def _get_default_value(self, cpp_type: str) -> str:
        """Get default value for a C++ type in Python."""
        cpp_type = cpp_type.strip()
        if cpp_type in ('int', 'long', 'short', 'size_t'):
            return '0'
        elif cpp_type in ('float', 'double'):
            return '0.0'
        elif cpp_type == 'bool':
            return 'False'
        elif cpp_type in ('std::string', 'string'):
            return "''"
        elif 'vector' in cpp_type:
            return '[]'
        elif 'map' in cpp_type:
            return '{}'
        else:
            return f'{cpp_type}()'

    def _convert_cpp_expr(self, expr: str) -> str:
        if not expr:
            return ''

        expr = expr.strip()

        # Handle C++ patterns
        expr = expr.replace('this->', 'self.')
        expr = expr.replace('->', '.')
        expr = expr.replace('::', '.')
        expr = expr.replace('nullptr', 'None')
        expr = expr.replace('true', 'True')
        expr = expr.replace('false', 'False')
        expr = expr.replace('&&', ' and ')
        expr = expr.replace('||', ' or ')

        # Handle M_PI
        expr = re.sub(r'\bM_PI\b', 'math.pi', expr)

        # Handle std:: functions
        expr = re.sub(r'std::sqrt\(([^)]+)\)', r'math.sqrt(\1)', expr)
        expr = re.sub(r'std::cos\(([^)]+)\)', r'math.cos(\1)', expr)
        expr = re.sub(r'std::sin\(([^)]+)\)', r'math.sin(\1)', expr)
        expr = re.sub(r'std::tan\(([^)]+)\)', r'math.tan(\1)', expr)
        expr = re.sub(r'std::abs\(([^)]+)\)', r'abs(\1)', expr)
        expr = re.sub(r'std::pow\(([^,]+),\s*([^)]+)\)', r'(\1) ** (\2)', expr)
        expr = re.sub(r'std::min\(([^,]+),\s*([^)]+)\)', r'min(\1, \2)', expr)
        expr = re.sub(r'std::max\(([^,]+),\s*([^)]+)\)', r'max(\1, \2)', expr)

        # Handle std::accumulate(container.begin(), container.end(), init) -> sum(container) [+ init]
        # v3.4.1: Also handle accumulate without std:: prefix
        def _accumulate_to_sum(m):
            container = m.group(1)
            init_val = m.group(2).strip()
            if init_val == '0' or init_val == '0.0':
                return f'sum({container})'
            return f'sum({container}) + {init_val}'
        expr = re.sub(r'(?:std::)?accumulate\((\w+)\.begin\(\),\s*\1\.end\(\),\s*([^)]+)\)', _accumulate_to_sum, expr)

        # v3.4.1: Handle std::find, std::count, std::sort with .begin()/.end()
        # std::find(vec.begin(), vec.end(), val) -> val in vec
        expr = re.sub(r'(?:std::)?find\((\w+)\.begin\(\),\s*\1\.end\(\),\s*([^)]+)\)\s*!=\s*\1\.end\(\)', r'\2 in \1', expr)
        # std::count(vec.begin(), vec.end(), val) -> vec.count(val)
        expr = re.sub(r'(?:std::)?count\((\w+)\.begin\(\),\s*\1\.end\(\),\s*([^)]+)\)', r'\1.count(\2)', expr)
        # std::sort(vec.begin(), vec.end()) -> vec.sort()
        expr = re.sub(r'(?:std::)?sort\((\w+)\.begin\(\),\s*\1\.end\(\)\)', r'\1.sort()', expr)
        # std::reverse(vec.begin(), vec.end()) -> vec.reverse()
        expr = re.sub(r'(?:std::)?reverse\((\w+)\.begin\(\),\s*\1\.end\(\)\)', r'\1.reverse()', expr)

        # v3.4.1: Clean up any remaining .begin()/.end() that couldn't be converted
        # container.begin() -> iter(container) for iteration context
        # But typically these are errors - flag as comment if they remain
        expr = re.sub(r'(\w+)\.begin\(\)', r'\1[0]', expr)  # Approximate as first element
        expr = re.sub(r'(\w+)\.end\(\)', r'len(\1)', expr)  # Approximate as length

        # Handle .size() -> len()
        expr = re.sub(r'(\w+)\.size\(\)', r'len(\1)', expr)

        # Handle .push_back -> .append
        expr = re.sub(r'(\w+)\.push_back\(([^)]+)\)', r'\1.append(\2)', expr)

        # Handle .empty() -> len() == 0
        expr = re.sub(r'(\w+)\.empty\(\)', r'len(\1) == 0', expr)

        # Handle static_cast
        expr = re.sub(r'static_cast<\w+>\(([^)]+)\)', r'\1', expr)

        # Handle std::to_string
        expr = re.sub(r'std::to_string\(([^)]+)\)', r'str(\1)', expr)

        # Handle std::stoi/stof
        expr = re.sub(r'std::stoi\(([^)]+)\)', r'int(\1)', expr)
        expr = re.sub(r'std::stof\(([^)]+)\)', r'float(\1)', expr)

        # Handle vector/container literals
        expr = re.sub(r'std::vector<[^>]+>\{([^}]*)\}', r'[\1]', expr)
        expr = re.sub(r'std::unordered_map<[^>]+>\{([^}]*)\}', r'{\1}', expr)
        expr = re.sub(r'std::unordered_set<[^>]+>\{([^}]*)\}', r'{\1}', expr)
        expr = re.sub(r'std::make_tuple\(([^)]*)\)', r'(\1)', expr)

        # Handle cout
        expr = re.sub(r'std::cout\s*<<\s*(.+?)(?:\s*<<\s*std::endl)?', r'print(\1)', expr)

        # Handle string quotes
        expr = re.sub(r'"([^"]*)"', r"'\1'", expr)

        # Clean up remaining std::
        expr = expr.replace('std.', '')

        # Handle negation !
        expr = re.sub(r'!(\w)', r'not \1', expr)

        # v3.3.22: Add self. prefix for class member access (when not already prefixed)
        if self._current_class_fields:
            for field in self._current_class_fields:
                # Match field name that's not already prefixed with self. or another identifier
                # Fixed lookahead to be more permissive - match non-word chars or end
                expr = re.sub(rf'(?<![.\w])(?<!self\.){re.escape(field)}(?=\W|$)', f'self.{field}', expr)

        # v3.4.1: Handle common C++ member naming conventions
        # Convert m_name to self.name when in class context
        if self._current_class_fields:
            # Convert m_xxx to self.xxx
            expr = re.sub(r'(?<![.\w])m_(\w+)(?=\W|$)', r'self.\1', expr)
            # Convert _xxx to self.xxx (leading underscore)
            expr = re.sub(r'(?<![.\w])_(\w+)(?=\W|$)', r'self.\1', expr)
            # v3.4.1: Convert xxx_ to self.xxx_ (trailing underscore - Google style)
            # Only if it's a known field or matches the pattern
            for field in self._current_class_fields:
                if field.endswith('_') and field not in ('self_',):
                    expr = re.sub(rf'(?<![.\w]){re.escape(field)}(?=\W|$)', f'self.{field}', expr)

        return expr

    def _generate_struct(self, struct: StructInfo) -> List[str]:
        lines = ['@dataclass']
        # v3.4.1: Escape Python keywords and C++ reserved words in struct/class names
        struct_name = _escape_identifier(struct.name)
        lines.append(f'class {struct_name}:')

        if not struct.fields:
            lines.append(f'{self.indent}pass')
        else:
            for fname, ftype in struct.fields:
                # v3.4.1: Escape Python keywords and C++ reserved words in field names
                escaped_fname = _escape_identifier(fname)
                lines.append(f'{self.indent}{escaped_fname}: {ftype}')

        return lines

    def _generate_class(self, cls: ClassInfo) -> List[str]:
        lines = []

        # v3.4.1: Escape Python keywords and C++ reserved words in class names
        class_name = _escape_identifier(cls.name)
        if cls.bases:
            lines.append(f'class {class_name}({", ".join(cls.bases)}):')
        else:
            lines.append(f'class {class_name}:')

        if not cls.fields and not cls.methods and not cls.constructors:
            lines.append(f'{self.indent}pass')
            return lines

        for ctor in cls.constructors:
            lines.extend(self._generate_method(ctor, is_init=True))

        for method in cls.methods:
            lines.extend(self._generate_method(method))

        return lines

    def _generate_method(self, method: FunctionInfo, is_init: bool = False) -> List[str]:
        lines = []

        if method.is_static:
            lines.append(f'{self.indent}@staticmethod')

        params = ['self'] if not method.is_static else []
        for pname, ptype in method.params:
            # v3.4.1: Escape Python keywords and C++ reserved words in parameter names
            escaped_pname = _escape_identifier(pname)
            if ptype and ptype != 'Any':
                params.append(f'{escaped_pname}: {ptype}')
            else:
                params.append(escaped_pname)

        ret_type = ''
        if not is_init and method.return_type and method.return_type != 'None':
            ret_type = f' -> {method.return_type}'

        # v3.4.1: Escape Python keywords and C++ reserved words in method names
        method_name = '__init__' if is_init else _escape_identifier(method.name)
        lines.append(f'{self.indent}def {method_name}({", ".join(params)}){ret_type}:')

        body_lines = method.body.split('\n')
        if body_lines and body_lines[0].strip():
            for bl in body_lines:
                lines.append(f'{self.indent}{self.indent}{bl}')
        else:
            lines.append(f'{self.indent}{self.indent}pass')

        return lines

    def _generate_function(self, func: FunctionInfo) -> List[str]:
        lines = []

        params = []
        for pname, ptype in func.params:
            # v3.4.1: Escape Python keywords and C++ reserved words in parameter names
            escaped_pname = _escape_identifier(pname)
            if ptype and ptype != 'Any':
                params.append(f'{escaped_pname}: {ptype}')
            else:
                params.append(escaped_pname)

        ret_type = ''
        if func.return_type and func.return_type != 'None':
            ret_type = f' -> {func.return_type}'

        # v3.4.1: Escape Python keywords and C++ reserved words in function names
        func_name = _escape_identifier(func.name)
        lines.append(f'def {func_name}({", ".join(params)}){ret_type}:')

        body_lines = func.body.split('\n')
        if body_lines and body_lines[0].strip():
            for bl in body_lines:
                lines.append(f'{self.indent}{bl}')
        else:
            lines.append(f'{self.indent}pass')

        return lines


def convert_python_to_cpp(source: str, module_name: str) -> Tuple[str, str]:
    """Convert Python to C++. Returns (cpp_content, header_content)."""
    converter = PythonToCppConverter()
    return converter.convert(source, module_name)


def convert_cpp_to_python(source: str, module_name: str) -> str:
    """Convert C++ to Python. Returns python content."""
    converter = CppToPythonConverter()
    return converter.convert(source, module_name)


# ============================================================================
# AI-Assisted Conversion System
# ============================================================================

# Comprehensive rulebase for AI-assisted code conversion
AI_CONVERSION_RULEBASE = {
    'python_to_cpp': {
        # Type mapping rules
        'types': {
            'int': {'cpp': 'int', 'notes': 'Direct mapping'},
            'float': {'cpp': 'double', 'notes': 'Python float is 64-bit'},
            'str': {'cpp': 'std::string', 'notes': 'Requires <string>'},
            'bool': {'cpp': 'bool', 'notes': 'Direct mapping'},
            'bytes': {'cpp': 'std::vector<uint8_t>', 'notes': 'Raw bytes'},
            'bytearray': {'cpp': 'std::vector<uint8_t>', 'notes': 'Mutable bytes'},
            'list': {'cpp': 'std::vector<T>', 'notes': 'Requires element type'},
            'dict': {'cpp': 'std::unordered_map<K,V>', 'notes': 'Hash map'},
            'set': {'cpp': 'std::unordered_set<T>', 'notes': 'Hash set'},
            'tuple': {'cpp': 'std::tuple<...>', 'notes': 'Fixed-size'},
            'None': {'cpp': 'void', 'notes': 'Return type'},
            'Any': {'cpp': 'auto', 'notes': 'Type deduction'},
            'Optional': {'cpp': 'std::optional<T>', 'notes': 'Requires <optional>'},
            'Union': {'cpp': 'std::variant<...>', 'notes': 'Requires <variant>'},
            'Callable': {'cpp': 'std::function<R(Args...)>', 'notes': 'Requires <functional>'},
        },
        # Built-in function mappings
        'builtins': {
            'len': {'cpp': '.size()', 'pattern': 'len({x})', 'to': '{x}.size()'},
            'print': {'cpp': 'std::cout', 'notes': 'Requires <iostream>'},
            'range': {'cpp': 'for loop', 'notes': 'Convert to C-style for'},
            'str': {'cpp': 'std::to_string', 'notes': 'Numeric conversion'},
            'int': {'cpp': 'static_cast<int>', 'notes': 'Type cast'},
            'float': {'cpp': 'static_cast<double>', 'notes': 'Type cast'},
            'abs': {'cpp': 'std::abs', 'notes': 'Requires <cmath>'},
            'min': {'cpp': 'std::min', 'notes': 'Requires <algorithm>'},
            'max': {'cpp': 'std::max', 'notes': 'Requires <algorithm>'},
            'sum': {'cpp': 'std::accumulate', 'notes': 'Requires <numeric>'},
            'sorted': {'cpp': 'std::sort', 'notes': 'In-place, use copy'},
            'reversed': {'cpp': 'std::reverse', 'notes': 'In-place, use copy'},
            'enumerate': {'cpp': 'index loop', 'notes': 'Manual index tracking'},
            'zip': {'cpp': 'parallel iteration', 'notes': 'Manual or ranges::zip'},
            'map': {'cpp': 'std::transform', 'notes': 'Requires <algorithm>'},
            'filter': {'cpp': 'std::copy_if', 'notes': 'Requires <algorithm>'},
            'any': {'cpp': 'std::any_of', 'notes': 'Requires <algorithm>'},
            'all': {'cpp': 'std::all_of', 'notes': 'Requires <algorithm>'},
            'isinstance': {'cpp': 'dynamic_cast', 'notes': 'Runtime type check'},
            'type': {'cpp': 'typeid', 'notes': 'Requires <typeinfo>'},
            'id': {'cpp': '&', 'notes': 'Address as identity'},
            'hash': {'cpp': 'std::hash', 'notes': 'Requires <functional>'},
            'open': {'cpp': 'std::fstream', 'notes': 'Requires <fstream>'},
            'input': {'cpp': 'std::cin', 'notes': 'Requires <iostream>'},
        },
        # Python-unique patterns that need workarounds
        'workarounds': {
            'list_comprehension': {
                'pattern': '[expr for x in iterable]',
                'cpp': 'Lambda IIFE with loop',
                'example': '[&]() { std::vector<T> r; for(auto& x : iterable) r.push_back(expr); return r; }()',
            },
            'dict_comprehension': {
                'pattern': '{k: v for ...}',
                'cpp': 'Lambda IIFE with loop',
                'notes': 'Similar to list comprehension',
            },
            'generator': {
                'pattern': 'yield x',
                'cpp': 'Iterator class or callback',
                'notes': 'No direct equivalent, use custom iterator',
            },
            'async_await': {
                'pattern': 'async def / await',
                'cpp': 'std::future/std::async or coroutines (C++20)',
                'notes': 'Requires threading support',
            },
            'decorators': {
                'pattern': '@decorator',
                'cpp': 'Wrapper function or template',
                'notes': 'Manual wrapping required',
            },
            'context_manager': {
                'pattern': 'with ... as x:',
                'cpp': 'RAII class',
                'notes': 'Use constructor/destructor pattern',
            },
            'multiple_inheritance': {
                'pattern': 'class A(B, C)',
                'cpp': 'Multiple inheritance',
                'notes': 'Virtual inheritance may be needed',
            },
            'duck_typing': {
                'pattern': 'Dynamic attribute access',
                'cpp': 'Templates or concepts (C++20)',
                'notes': 'Use template constraints',
            },
            'slice_assignment': {
                'pattern': 'a[1:3] = [x, y]',
                'cpp': 'Vector operations',
                'notes': 'Use erase + insert',
            },
            'unpacking': {
                'pattern': 'a, b = func()',
                'cpp': 'structured bindings (C++17)',
                'notes': 'auto [a, b] = func();',
            },
        },
        # Method mappings for common types
        'methods': {
            'list.append': {'cpp': 'push_back', 'notes': 'Same semantics'},
            'list.extend': {'cpp': 'insert(end, begin, end)', 'notes': 'Range insert'},
            'list.insert': {'cpp': 'insert(begin+i, val)', 'notes': 'Index insert'},
            'list.remove': {'cpp': 'erase(remove(...), end())', 'notes': 'Erase-remove idiom'},
            'list.pop': {'cpp': 'back() + pop_back()', 'notes': 'Two operations'},
            'list.clear': {'cpp': 'clear()', 'notes': 'Same name'},
            'list.index': {'cpp': 'find + distance', 'notes': 'No direct method'},
            'list.count': {'cpp': 'std::count', 'notes': 'Requires <algorithm>'},
            'list.sort': {'cpp': 'std::sort', 'notes': 'Requires <algorithm>'},
            'list.reverse': {'cpp': 'std::reverse', 'notes': 'Requires <algorithm>'},
            'str.split': {'cpp': 'Manual or stringstream', 'notes': 'No direct method'},
            'str.join': {'cpp': 'Loop with append', 'notes': 'No direct method'},
            'str.strip': {'cpp': 'Manual trim', 'notes': 'No direct method'},
            'str.replace': {'cpp': 'Manual or regex_replace', 'notes': 'Requires loop'},
            'str.find': {'cpp': 'find()', 'notes': 'Returns size_t'},
            'str.startswith': {'cpp': 'substr(0, n) == prefix', 'notes': 'Manual check'},
            'str.endswith': {'cpp': 'substr(len-n) == suffix', 'notes': 'Manual check'},
            'str.upper': {'cpp': 'std::transform with toupper', 'notes': 'Requires <cctype>'},
            'str.lower': {'cpp': 'std::transform with tolower', 'notes': 'Requires <cctype>'},
            'str.format': {'cpp': 'std::format (C++20) or sprintf', 'notes': 'Format string'},
            'dict.keys': {'cpp': 'Loop or ranges', 'notes': 'No direct method'},
            'dict.values': {'cpp': 'Loop or ranges', 'notes': 'No direct method'},
            'dict.items': {'cpp': 'Loop over pairs', 'notes': 'Iterate map directly'},
            'dict.get': {'cpp': 'find + check', 'notes': 'Manual default handling'},
            'dict.update': {'cpp': 'insert or merge', 'notes': 'Loop or ranges'},
            'set.add': {'cpp': 'insert', 'notes': 'Same semantics'},
            'set.remove': {'cpp': 'erase', 'notes': 'Same semantics'},
            'set.union': {'cpp': 'set_union', 'notes': 'Requires <algorithm>'},
            'set.intersection': {'cpp': 'set_intersection', 'notes': 'Requires <algorithm>'},
        },
    },
    'cpp_to_python': {
        # Type mapping rules
        'types': {
            'int': {'python': 'int', 'notes': 'Direct mapping'},
            'long': {'python': 'int', 'notes': 'Python int is arbitrary precision'},
            'long long': {'python': 'int', 'notes': 'Python int is arbitrary precision'},
            'short': {'python': 'int', 'notes': 'Python int is arbitrary precision'},
            'unsigned': {'python': 'int', 'notes': 'Python handles large numbers'},
            'size_t': {'python': 'int', 'notes': 'Python int is arbitrary precision'},
            'float': {'python': 'float', 'notes': 'Direct mapping'},
            'double': {'python': 'float', 'notes': 'Python float is 64-bit'},
            'bool': {'python': 'bool', 'notes': 'Direct mapping'},
            'char': {'python': 'str', 'notes': 'Single character'},
            'std::string': {'python': 'str', 'notes': 'Direct mapping'},
            'string': {'python': 'str', 'notes': 'Direct mapping'},
            'void': {'python': 'None', 'notes': 'Return type'},
            'auto': {'python': 'Any', 'notes': 'Type deduction'},
            'std::vector': {'python': 'List', 'notes': 'Requires typing'},
            'vector': {'python': 'List', 'notes': 'Requires typing'},
            'std::array': {'python': 'List', 'notes': 'Fixed-size to dynamic'},
            'std::map': {'python': 'Dict', 'notes': 'Ordered dict'},
            'std::unordered_map': {'python': 'Dict', 'notes': 'Hash map'},
            'std::set': {'python': 'Set', 'notes': 'Ordered set'},
            'std::unordered_set': {'python': 'Set', 'notes': 'Hash set'},
            'std::tuple': {'python': 'Tuple', 'notes': 'Direct mapping'},
            'std::optional': {'python': 'Optional', 'notes': 'Requires typing'},
            'std::variant': {'python': 'Union', 'notes': 'Requires typing'},
            'std::function': {'python': 'Callable', 'notes': 'Requires typing'},
            'std::shared_ptr': {'python': 'object', 'notes': 'Python handles GC'},
            'std::unique_ptr': {'python': 'object', 'notes': 'Python handles GC'},
        },
        # C++ patterns to Python
        'patterns': {
            'for_index': {
                'cpp': 'for (size_t i = 0; i < n; ++i)',
                'python': 'for i in range(n)',
            },
            'for_range': {
                'cpp': 'for (auto& x : container)',
                'python': 'for x in container',
            },
            'nullptr': {
                'cpp': 'nullptr',
                'python': 'None',
            },
            'true_false': {
                'cpp': 'true/false',
                'python': 'True/False',
            },
            'this_pointer': {
                'cpp': 'this->member',
                'python': 'self.member',
            },
            'scope_resolution': {
                'cpp': 'Class::method',
                'python': 'Class.method',
            },
            'stream_io': {
                'cpp': 'std::cout << x',
                'python': 'print(x)',
            },
            'lambda': {
                'cpp': '[&](auto x) { return x; }',
                'python': 'lambda x: x',
            },
        },
        # C++ unique features that need workarounds
        'workarounds': {
            'templates': {
                'pattern': 'template<typename T>',
                'python': 'Generic[T] or Any',
                'notes': 'Use typing.Generic for type hints',
            },
            'pointers': {
                'pattern': 'T* ptr',
                'python': 'Reference semantics (native)',
                'notes': 'Python uses references by default',
            },
            'references': {
                'pattern': 'T& ref',
                'python': 'Reference semantics (native)',
                'notes': 'Python uses references by default',
            },
            'const': {
                'pattern': 'const T&',
                'python': 'No direct equivalent',
                'notes': 'Use conventions or @property',
            },
            'operator_overload': {
                'pattern': 'operator+',
                'python': '__add__',
                'notes': 'Magic methods',
            },
            'destructor': {
                'pattern': '~ClassName()',
                'python': '__del__',
                'notes': 'Not guaranteed to be called',
            },
            'move_semantics': {
                'pattern': 'std::move(x)',
                'python': 'No equivalent (GC handles)',
                'notes': 'Python uses reference counting',
            },
            'raii': {
                'pattern': 'Resource acquisition',
                'python': 'Context manager (with)',
                'notes': 'Use __enter__/__exit__',
            },
            'preprocessor': {
                'pattern': '#define, #ifdef',
                'python': 'No equivalent',
                'notes': 'Use constants or conditionals',
            },
        },
    },
    # Common includes needed for converted code
    'cpp_includes': {
        'string': '<string>',
        'vector': '<vector>',
        'map': '<unordered_map>',
        'set': '<unordered_set>',
        'optional': '<optional>',
        'variant': '<variant>',
        'functional': '<functional>',
        'algorithm': '<algorithm>',
        'numeric': '<numeric>',
        'cmath': '<cmath>',
        'iostream': '<iostream>',
        'fstream': '<fstream>',
        'sstream': '<sstream>',
        'memory': '<memory>',
        'tuple': '<tuple>',
        'stdexcept': '<stdexcept>',
    },
}

# AI prompt for conversion assistance
AI_CONVERSION_PROMPT = '''You are an expert code converter for Python <-> C++ translation.

RULEBASE (follow strictly):
{rulebase}

CONVERSION MODE: {mode}
SOURCE CODE:
```{source_lang}
{source_code}
```

TASK: Convert the code {direction}. Process section by section.

RULES:
1. Preserve ALL functionality exactly
2. Use type hints in Python, proper types in C++
3. For Python->C++: ALL code MUST be in namespace includecpp {{ }}
4. For unique features without direct equivalent, provide workaround with WORKAROUND comment
5. Report any API changes at the end

OUTPUT FORMAT:
For each section (class, function, struct):

SECTION: <name>
ANALYSIS: <brief analysis of conversion needs>
WORKAROUNDS: <list any workarounds needed, or "None">
```{target_lang}
<converted code>
```

After all sections:

API_CHANGES:
- <list any changes to function signatures, removed features, etc.>
- If no changes: "None - API preserved"

WARNINGS:
- <list any potential issues or limitations>

Convert now:'''


class AIConversionAssistant:
    """AI-assisted code conversion helper."""

    def __init__(self):
        self.workarounds_used = []
        self.api_changes = []
        self.warnings = []

    def prepare_prompt(self, source: str, mode: str) -> str:
        """Prepare AI prompt with rulebase and source."""
        if mode == 'py_to_cpp':
            rules = AI_CONVERSION_RULEBASE['python_to_cpp']
            direction = 'from Python to C++'
            source_lang = 'python'
            target_lang = 'cpp'
        else:
            rules = AI_CONVERSION_RULEBASE['cpp_to_python']
            direction = 'from C++ to Python'
            source_lang = 'cpp'
            target_lang = 'python'

        # Format rulebase for prompt
        rulebase_str = self._format_rulebase(rules)

        return AI_CONVERSION_PROMPT.format(
            rulebase=rulebase_str,
            mode=mode.upper(),
            source_code=source,
            direction=direction,
            source_lang=source_lang,
            target_lang=target_lang
        )

    def _format_rulebase(self, rules: dict) -> str:
        """Format rulebase as readable text for AI."""
        lines = []

        if 'types' in rules:
            lines.append("TYPE MAPPINGS:")
            for py_type, info in list(rules['types'].items())[:15]:
                target = info.get('cpp') or info.get('python')
                lines.append(f"  {py_type} -> {target}")

        if 'builtins' in rules:
            lines.append("\nBUILTIN FUNCTIONS:")
            for func, info in list(rules['builtins'].items())[:10]:
                lines.append(f"  {func}() -> {info['cpp']} ({info.get('notes', '')})")

        if 'workarounds' in rules:
            lines.append("\nPATTERNS NEEDING WORKAROUNDS:")
            for name, info in list(rules['workarounds'].items())[:8]:
                lines.append(f"  {name}: {info['pattern']} -> {info.get('cpp') or info.get('python')}")

        if 'methods' in rules:
            lines.append("\nMETHOD MAPPINGS:")
            for method, info in list(rules['methods'].items())[:10]:
                lines.append(f"  {method} -> {info['cpp']}")

        return '\n'.join(lines)

    def analyze_source(self, source: str, mode: str) -> dict:
        """Analyze source code for conversion complexity."""
        result = {
            'sections': [],
            'workarounds_needed': [],
            'complexity': 'simple',
            'estimated_changes': 0,
        }

        if mode == 'py_to_cpp':
            result = self._analyze_python(source)
        else:
            result = self._analyze_cpp(source)

        return result

    def _analyze_python(self, source: str) -> dict:
        """Analyze Python source for conversion needs."""
        import ast
        result = {
            'sections': [],
            'workarounds_needed': [],
            'complexity': 'simple',
            'estimated_changes': 0,
        }

        try:
            tree = ast.parse(source)
        except SyntaxError:
            result['complexity'] = 'error'
            return result

        workarounds = AI_CONVERSION_RULEBASE['python_to_cpp']['workarounds']

        for node in ast.walk(tree):
            # Check for patterns needing workarounds
            if isinstance(node, ast.ListComp):
                result['workarounds_needed'].append({
                    'type': 'list_comprehension',
                    'line': node.lineno,
                    'suggestion': workarounds['list_comprehension']['cpp'],
                })
            elif isinstance(node, ast.DictComp):
                result['workarounds_needed'].append({
                    'type': 'dict_comprehension',
                    'line': node.lineno,
                    'suggestion': workarounds['dict_comprehension']['cpp'],
                })
            elif isinstance(node, ast.Yield) or isinstance(node, ast.YieldFrom):
                result['workarounds_needed'].append({
                    'type': 'generator',
                    'line': node.lineno,
                    'suggestion': workarounds['generator']['cpp'],
                })
            elif isinstance(node, ast.AsyncFunctionDef):
                result['workarounds_needed'].append({
                    'type': 'async_await',
                    'line': node.lineno,
                    'suggestion': workarounds['async_await']['cpp'],
                })
            elif isinstance(node, ast.With):
                result['workarounds_needed'].append({
                    'type': 'context_manager',
                    'line': node.lineno,
                    'suggestion': workarounds['context_manager']['cpp'],
                })

        # Extract sections
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                result['sections'].append({
                    'type': 'class',
                    'name': node.name,
                    'line': node.lineno,
                    'methods': len([n for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]),
                })
            elif isinstance(node, ast.FunctionDef):
                result['sections'].append({
                    'type': 'function',
                    'name': node.name,
                    'line': node.lineno,
                })

        # Determine complexity
        if len(result['workarounds_needed']) > 5:
            result['complexity'] = 'complex'
        elif len(result['workarounds_needed']) > 0:
            result['complexity'] = 'moderate'

        result['estimated_changes'] = len(result['workarounds_needed'])
        return result

    def _analyze_cpp(self, source: str) -> dict:
        """Analyze C++ source for conversion needs."""
        result = {
            'sections': [],
            'workarounds_needed': [],
            'complexity': 'simple',
            'estimated_changes': 0,
        }

        workarounds = AI_CONVERSION_RULEBASE['cpp_to_python']['workarounds']

        # Check for templates
        if re.search(r'template\s*<', source):
            result['workarounds_needed'].append({
                'type': 'templates',
                'suggestion': workarounds['templates']['python'],
            })

        # Check for pointers
        if re.search(r'\w+\s*\*\s*\w+', source):
            result['workarounds_needed'].append({
                'type': 'pointers',
                'suggestion': workarounds['pointers']['python'],
            })

        # Check for operator overloads
        if re.search(r'operator\s*[+\-*/=<>!&|^~\[\]]+', source):
            result['workarounds_needed'].append({
                'type': 'operator_overload',
                'suggestion': workarounds['operator_overload']['python'],
            })

        # Check for destructors
        if re.search(r'~\w+\s*\(', source):
            result['workarounds_needed'].append({
                'type': 'destructor',
                'suggestion': workarounds['destructor']['python'],
            })

        # Check for move semantics
        if 'std::move' in source:
            result['workarounds_needed'].append({
                'type': 'move_semantics',
                'suggestion': workarounds['move_semantics']['python'],
            })

        # Check for preprocessor
        if re.search(r'#\s*(define|ifdef|ifndef|endif)', source):
            result['workarounds_needed'].append({
                'type': 'preprocessor',
                'suggestion': workarounds['preprocessor']['python'],
            })

        # Extract sections (classes, structs, functions)
        for match in re.finditer(r'class\s+(\w+)', source):
            result['sections'].append({'type': 'class', 'name': match.group(1)})

        for match in re.finditer(r'struct\s+(\w+)', source):
            result['sections'].append({'type': 'struct', 'name': match.group(1)})

        # Functions outside classes
        func_pattern = r'(?:^|\n)\s*(?:static\s+|inline\s+|virtual\s+)*(\w+(?:<[^>]+>)?(?:\s*[*&])?)\s+(\w+)\s*\([^)]*\)\s*(?:const)?\s*\{'
        for match in re.finditer(func_pattern, source):
            name = match.group(2)
            if name not in ('if', 'while', 'for', 'switch'):
                result['sections'].append({'type': 'function', 'name': name})

        # Determine complexity
        if len(result['workarounds_needed']) > 3:
            result['complexity'] = 'complex'
        elif len(result['workarounds_needed']) > 0:
            result['complexity'] = 'moderate'

        result['estimated_changes'] = len(result['workarounds_needed'])
        return result

    def parse_ai_response(self, response: str) -> dict:
        """Parse AI conversion response."""
        result = {
            'sections': [],
            'api_changes': [],
            'warnings': [],
            'full_code': '',
        }

        # Extract sections
        section_pattern = r'SECTION:\s*(\w+)\s*\nANALYSIS:\s*([^\n]+)\s*\nWORKAROUNDS:\s*([^\n]+)\s*\n```\w*\n(.*?)```'
        for match in re.finditer(section_pattern, response, re.DOTALL):
            result['sections'].append({
                'name': match.group(1),
                'analysis': match.group(2),
                'workarounds': match.group(3),
                'code': match.group(4).strip(),
            })

        # Extract API changes
        api_match = re.search(r'API_CHANGES:\s*(.*?)(?=WARNINGS:|$)', response, re.DOTALL)
        if api_match:
            changes_text = api_match.group(1).strip()
            if 'None' not in changes_text:
                for line in changes_text.split('\n'):
                    line = line.strip().lstrip('-').strip()
                    if line:
                        result['api_changes'].append(line)

        # Extract warnings
        warn_match = re.search(r'WARNINGS:\s*(.*?)$', response, re.DOTALL)
        if warn_match:
            for line in warn_match.group(1).strip().split('\n'):
                line = line.strip().lstrip('-').strip()
                if line:
                    result['warnings'].append(line)

        # Combine code sections
        if result['sections']:
            result['full_code'] = '\n\n'.join(s['code'] for s in result['sections'])

        return result


def get_ai_assistant() -> AIConversionAssistant:
    """Get AI conversion assistant instance."""
    return AIConversionAssistant()


def get_conversion_rulebase() -> dict:
    """Get the full conversion rulebase."""
    return AI_CONVERSION_RULEBASE
