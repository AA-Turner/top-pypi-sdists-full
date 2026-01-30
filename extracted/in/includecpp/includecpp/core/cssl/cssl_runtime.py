"""
CSSL Runtime Environment
Executes CSSL scripts by interpreting the AST
"""

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union

from .cssl_parser import ASTNode, parse_cssl, parse_cssl_program, CSSLSyntaxError
from .cssl_events import CSSLEventManager, EventType, EventData, get_event_manager
from .cssl_builtins import CSSLBuiltins
from .cssl_modules import get_module_registry, get_standard_module
from .cssl_types import (
    Parameter, DataStruct, Shuffled, Iterator, Combo,
    Stack, Vector, Array, DataSpace, OpenQuote, List, Dictionary, Map,
    Queue,  # v4.7: Thread-safe queue
    CSSLClass, CSSLInstance, ByteArrayed,
    CSSLNamespace,  # v4.8: Custom namespace support
    Bit, Byte, Address,  # v4.9.0: Binary types and address pointer
    CSSLFuture, CSSLGenerator, CSSLAsyncFunction, AsyncModule  # v4.9.3: Async support
)


# Global custom filter registry
# Structure: { "type::helper": callback_function }
# Callback signature: (source, filter_value, runtime) -> Any
_custom_filters: Dict[str, Callable[[Any, Any, Any], Any]] = {}


def register_filter(filter_type: str, helper: str, callback: Callable[[Any, Any, Any], Any]) -> None:
    """Register a custom filter.

    Args:
        filter_type: The filter type (e.g., "mytype")
        helper: The helper name (e.g., "where", "index", or "*" for catch-all)
        callback: Function(source, filter_value, runtime) -> filtered_result

    Usage in CSSL:
        result <==[mytype::where="value"] source;

    Usage from Python:
        from includecpp.core.cssl.cssl_runtime import register_filter
        register_filter("mytype", "where", lambda src, val, rt: ...)
    """
    key = f"{filter_type}::{helper}"
    _custom_filters[key] = callback


def unregister_filter(filter_type: str, helper: str) -> bool:
    """Unregister a custom filter."""
    key = f"{filter_type}::{helper}"
    if key in _custom_filters:
        del _custom_filters[key]
        return True
    return False


def get_custom_filters() -> Dict[str, Callable]:
    """Get all registered custom filters."""
    return _custom_filters.copy()


class CSSLRuntimeError(Exception):
    """Runtime error during CSSL execution with detailed context"""
    def __init__(self, message: str, line: int = 0, context: str = None, hint: str = None):
        self.line = line
        self.context = context
        self.hint = hint

        # Build detailed error message
        error_parts = []

        # Main error message (no "Error:" prefix - CLI handles that)
        if line:
            error_parts.append(f"Line {line}: {message}")
        else:
            error_parts.append(message)

        # Add context if available
        if context:
            error_parts.append(f"  Context: {context}")

        # Add hint if available
        if hint:
            error_parts.append(f"  Hint: {hint}")

        super().__init__("\n".join(error_parts))


# Common error hints for better user experience
ERROR_HINTS = {
    'undefined_variable': "Did you forget to declare the variable? Use 'string x = ...' or 'int x = ...'",
    'undefined_function': "Check function name spelling. Functions are case-sensitive.",
    'type_mismatch': "Try using explicit type conversion: toInt(), toFloat(), toString()",
    'null_reference': "Variable is null. Check if it was properly initialized.",
    'index_out_of_bounds': "Array index must be >= 0 and < array.length()",
    'division_by_zero': "Cannot divide by zero. Add a check: if (divisor != 0) { ... }",
    'invalid_operation': "This operation is not supported for this type.",
    'missing_semicolon': "Statement might be missing a semicolon (;)",
    'missing_brace': "Check for matching opening and closing braces { }",
}


def _find_similar_names(name: str, candidates: list, max_distance: int = 2) -> list:
    """Find similar names for 'did you mean' suggestions using Levenshtein distance."""
    if not candidates:
        return []

    def levenshtein(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        if len(s2) == 0:
            return len(s1)
        prev_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1.lower() != c2.lower())
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        return prev_row[-1]

    similar = []
    name_lower = name.lower()
    for candidate in candidates:
        if candidate.startswith('_'):
            continue
        dist = levenshtein(name, candidate)
        # Also check case-insensitive exact match
        if name_lower == candidate.lower() and name != candidate:
            similar.insert(0, candidate)  # Exact case mismatch goes first
        elif dist <= max_distance:
            similar.append(candidate)

    return similar[:3]  # Return top 3 suggestions


def _get_available_classes(scope: 'Scope', global_scope: 'Scope', promoted_globals: dict) -> list:
    """Get list of all available class names."""
    classes = []
    # Check current scope chain
    current = scope
    while current:
        for name, val in current.variables.items():
            if isinstance(val, CSSLClass) and name not in classes:
                classes.append(name)
        current = current.parent
    # Check global scope
    for name, val in global_scope.variables.items():
        if isinstance(val, CSSLClass) and name not in classes:
            classes.append(name)
    # Check promoted globals
    for name, val in promoted_globals.items():
        if isinstance(val, CSSLClass) and name not in classes:
            classes.append(name)
    return classes


def _get_available_functions(scope: 'Scope', global_scope: 'Scope', builtins) -> list:
    """Get list of all available function names."""
    functions = []
    # Check current scope chain
    current = scope
    while current:
        for name, val in current.variables.items():
            if callable(val) or (isinstance(val, ASTNode) and val.type == 'function'):
                if name not in functions:
                    functions.append(name)
        current = current.parent
    # Check global scope
    for name, val in global_scope.variables.items():
        if callable(val) or (isinstance(val, ASTNode) and val.type == 'function'):
            if name not in functions:
                functions.append(name)
    # Check builtins
    if builtins:
        for name in dir(builtins):
            if name.startswith('builtin_'):
                func_name = name[8:]  # Remove 'builtin_' prefix
                if func_name not in functions:
                    functions.append(func_name)
    return functions


class CSSLBreak(Exception):
    """Break statement"""
    pass


class CSSLContinue(Exception):
    """Continue statement"""
    pass


class CSSLReturn(Exception):
    """Return statement"""
    def __init__(self, value: Any = None):
        self.value = value
        super().__init__()


class CSSLYield(Exception):
    """Yield statement - v4.9.3: Generator yield that pauses execution."""
    def __init__(self, value: Any = None):
        self.value = value
        super().__init__()


class CSSLThrow(Exception):
    """Throw statement - v4.5.1: User-thrown exceptions that propagate to catch blocks
    v4.8: Extended to support Python exception types via raise statement.
    """
    def __init__(self, message: Any = None, underlying_exception: Exception = None):
        self.message = message
        self.underlying_exception = underlying_exception
        self.exception_type = type(underlying_exception).__name__ if underlying_exception else 'Error'
        super().__init__(str(message) if message else "")


class SuperProxy:
    """v4.8.8: Proxy for super->method() calls in child classes.

    Provides access to parent class methods from within a child class method.

    Usage in CSSL:
        class Parent {
            define greet() { println("Hello from Parent"); }
        }
        class Child extends Parent {
            define greet() {
                super->greet();  // Calls Parent.greet()
                println("Hello from Child");
            }
        }
    """
    def __init__(self, instance: 'CSSLInstance', parent_class: 'CSSLClass', runtime: 'CSSLRuntime'):
        self._instance = instance
        self._parent_class = parent_class
        self._runtime = runtime

    def get_method(self, name: str):
        """Get a method from the parent class."""
        if self._parent_class is None:
            return None

        # Check parent class methods (methods is a dict with name -> AST node)
        if hasattr(self._parent_class, 'methods') and isinstance(self._parent_class.methods, dict):
            if name in self._parent_class.methods:
                return self._parent_class.methods[name]

        # Check if parent has its own parent (grandparent) - recursive lookup
        if hasattr(self._parent_class, 'parent') and self._parent_class.parent:
            grandparent_proxy = SuperProxy(self._instance, self._parent_class.parent, self._runtime)
            return grandparent_proxy.get_method(name)

        return None

    def get_member(self, name: str):
        """Get a member variable from parent class defaults."""
        if self._parent_class is None:
            return None

        # Check parent class member defaults (members is a dict with name -> type/default)
        if hasattr(self._parent_class, 'members') and isinstance(self._parent_class.members, dict):
            if name in self._parent_class.members:
                member_info = self._parent_class.members[name]
                if isinstance(member_info, dict) and 'default' in member_info:
                    return self._runtime._evaluate(member_info['default'])
                return member_info

        return None


@dataclass
class Scope:
    """Variable scope"""
    variables: Dict[str, Any] = field(default_factory=dict)
    parent: Optional['Scope'] = None

    def get(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name: str, value: Any):
        self.variables[name] = value

    def update(self, name: str, value: Any) -> bool:
        if name in self.variables:
            self.variables[name] = value
            return True
        if self.parent:
            return self.parent.update(name, value)
        return False

    def has(self, name: str) -> bool:
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


@dataclass
class ServiceDefinition:
    """Parsed service definition

    v4.8.6: Added __getattr__ and get() for accessing exported functions/structs/classes.
    This allows include() modules to be used like: mod.myFunc() or mod.get('myFunc')
    """
    name: str = ""
    version: str = "1.0"
    author: str = ""
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    autostart: bool = False
    priority: int = 0
    structs: Dict[str, ASTNode] = field(default_factory=dict)
    functions: Dict[str, ASTNode] = field(default_factory=dict)
    classes: Dict[str, Any] = field(default_factory=dict)  # v4.8.6: Class definitions
    enums: Dict[str, Any] = field(default_factory=dict)    # v4.8.6: Enum definitions
    namespaces: Dict[str, Any] = field(default_factory=dict)  # v4.8.6: Namespace definitions
    event_handlers: Dict[str, List[ASTNode]] = field(default_factory=dict)
    _runtime: Any = field(default=None, repr=False)  # Reference to runtime for calling functions

    def get(self, name: str, default: Any = None) -> Any:
        """Get an exported function, struct, class, enum, or namespace by name."""
        if name in self.functions:
            return self.functions[name]
        if name in self.classes:
            return self.classes[name]
        if name in self.structs:
            return self.structs[name]
        if name in self.enums:
            return self.enums[name]
        if name in self.namespaces:
            return self.namespaces[name]
        return default

    def __getattr__(self, name: str) -> Any:
        """Allow direct attribute access to functions, classes, structs, etc.

        Usage: mod.myFunc (returns the function AST node)
               mod.MyClass (returns the class definition)
        """
        # Avoid infinite recursion with dataclass fields
        if name.startswith('_') or name in ('name', 'version', 'author', 'description',
                                             'dependencies', 'autostart', 'priority',
                                             'structs', 'functions', 'classes', 'enums',
                                             'namespaces', 'event_handlers'):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        # Check classes first (most common case after functions)
        if hasattr(self, 'classes') and name in self.classes:
            return self.classes[name]
        # Check functions
        if hasattr(self, 'functions') and name in self.functions:
            return self.functions[name]
        # Check structs
        if hasattr(self, 'structs') and name in self.structs:
            return self.structs[name]
        # Check enums
        if hasattr(self, 'enums') and name in self.enums:
            return self.enums[name]
        # Check namespaces
        if hasattr(self, 'namespaces') and name in self.namespaces:
            return self.namespaces[name]

        raise AttributeError(f"Module '{self.name}' has no export '{name}'")


class CSSLRuntime:
    """
    CSSL Script Runtime
    Interprets and executes CSSL Abstract Syntax Trees
    """

    def __init__(self, service_engine=None, output_callback: Callable[[str, str], None] = None):
        self.service_engine = service_engine
        self.scope = Scope()
        self.global_scope = self.scope
        self.builtins = CSSLBuiltins(self)
        self.event_manager = get_event_manager()
        self.output_buffer: List[str] = []
        self.services: Dict[str, ServiceDefinition] = {}
        self._modules: Dict[str, Any] = {}
        self._global_structs: Dict[str, Any] = {}  # Global structs for s@<name> references
        self._function_injections: Dict[str, List[tuple]] = {}  # List of (code_block, captured_values_dict)
        self._function_replaced: Dict[str, bool] = {}  # NEW: Track replaced functions (<<==)
        self._original_functions: Dict[str, Any] = {}  # Store originals before replacement
        self._hook_executing: set = set()  # v4.9.2: Track currently executing hooks to prevent recursion
        self._hook_locals: dict = {}  # v4.9.2: Local variables from hooked function for local:: access
        self._injection_captures: Dict[str, Dict[str, Any]] = {}  # Captured %vars per injection
        self._current_captured_values: Dict[str, Any] = {}  # Current captured values during injection execution
        self._promoted_globals: Dict[str, Any] = {}  # NEW: Variables promoted via global()
        self._current_instance: Optional[CSSLInstance] = None  # Current class instance for this-> access
        self._var_meta: Dict[str, Dict[str, bool]] = {}  # v4.9.4: Track local/static/freezed modifiers
        self._running = False
        self._exit_code = 0
        self._output_callback = output_callback  # Callback for console output (text, level)
        self._source_lines: List[str] = []  # Store source code lines for error reporting
        self._current_file: str = "<code>"  # Current file being executed

        self._setup_modules()
        self._setup_builtins()

    def output(self, text: str, level: str = 'normal') -> None:
        """Output text, using callback if available, otherwise print."""
        if self._output_callback:
            self._output_callback(text, level)
        else:
            print(text, end='')
        self.output_buffer.append(text)

    def debug(self, text: str) -> None:
        """Debug output."""
        self.output(f"[DEBUG] {text}\n", 'debug')

    def error(self, text: str) -> None:
        """Error output."""
        self.output(f"[ERROR] {text}\n", 'error')

    def warn(self, text: str) -> None:
        """Warning output."""
        self.output(f"[WARN] {text}\n", 'warning')

    def _setup_modules(self):
        """Setup module references for @KernelClient, @VSRAM, etc."""
        if self.service_engine:
            self._modules['KernelClient'] = self.service_engine.KernelClient
            self._modules['Kernel'] = self.service_engine.KernelClient

            if hasattr(self.service_engine.KernelClient, 'VSRam'):
                self._modules['VSRAM'] = self.service_engine.KernelClient.VSRam
                self._modules['VSRam'] = self.service_engine.KernelClient.VSRam

            if hasattr(self.service_engine.KernelClient, 'WheelKernel'):
                self._modules['Wheel'] = self.service_engine.KernelClient.WheelKernel
                self._modules['WheelKernel'] = self.service_engine.KernelClient.WheelKernel

            if hasattr(self.service_engine.KernelClient, 'CSnI'):
                self._modules['Network'] = self.service_engine.KernelClient.CSnI
                self._modules['CSnI'] = self.service_engine.KernelClient.CSnI

            if hasattr(self.service_engine, 'ServiceOperation'):
                self._modules['Service'] = self.service_engine.ServiceOperation
                self._modules['ServiceOperation'] = self.service_engine.ServiceOperation

            self._modules['ServiceEngine'] = self.service_engine
            self._modules['Boot'] = self.service_engine

        self._modules['event'] = self.event_manager
        self._modules['Events'] = self.event_manager

        # Register CSSL Standard Modules
        module_registry = get_module_registry()
        for module_name in module_registry.list_modules():
            module = module_registry.get_module(module_name)
            if module:
                module.runtime = self
                self._modules[module_name] = module

    def _setup_builtins(self):
        """Register built-in functions in global scope"""
        for name in self.builtins.list_functions():
            self.global_scope.set(name, self.builtins.get_function(name))

        # v4.8.5: Setup C++ style stream variables (not functions)
        # This enables: cout << "Hello" << endl;  (without parentheses)
        from .cssl_types import OutputStream, InputStream
        self.global_scope.set('cout', OutputStream('stdout'))
        self.global_scope.set('cerr', OutputStream('stderr'))
        self.global_scope.set('clog', OutputStream('clog'))
        self.global_scope.set('cin', InputStream('stdin'))
        self.global_scope.set('endl', '\n')  # endl as newline marker

    def get_module(self, path: str) -> Any:
        """Get a module by path like 'KernelClient.VSRam'"""
        parts = path.split('.')
        obj = self._modules.get(parts[0])

        if obj is None:
            return None

        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return None

        return obj

    def register_global_struct(self, name: str, struct_data: Any):
        """Register a struct as globally accessible via s@<name>"""
        self._global_structs[name] = struct_data

    def get_global_struct(self, path: str) -> Any:
        """Get a global struct by path like 'Backend.Loop.timer'"""
        parts = path.split('.')
        obj = self._global_structs.get(parts[0])

        if obj is None:
            return None

        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return None

        return obj

    def _format_error(self, line: int, message: str, hint: str = None) -> CSSLRuntimeError:
        """Format a detailed error with source context"""
        error_parts = []

        # Main error header (no "Error:" prefix - CLI handles that)
        if line and line > 0:
            error_parts.append(f"Line {line} in {self._current_file}:")
        else:
            error_parts.append(f"In {self._current_file}:")

        # Extract message without existing line info
        clean_msg = message
        if "at line" in clean_msg.lower():
            # Remove redundant line info from message
            clean_msg = clean_msg.split(":", 1)[-1].strip() if ":" in clean_msg else clean_msg

        error_parts.append(f"  {clean_msg}")

        # Show source context (3 lines before and after)
        if self._source_lines and line and line > 0:
            error_parts.append("")
            start = max(0, line - 3)
            end = min(len(self._source_lines), line + 2)

            for i in range(start, end):
                line_num = i + 1
                source_line = self._source_lines[i] if i < len(self._source_lines) else ""
                marker = ">>>" if line_num == line else "   "
                error_parts.append(f"  {marker} {line_num:4d} | {source_line}")

        # Add hint
        if hint:
            error_parts.append("")
            error_parts.append(f"  Hint: {hint}")

        return CSSLRuntimeError("\n".join(error_parts), line)

    def _get_source_line(self, line: int) -> str:
        """Get source line by number (1-indexed)"""
        if self._source_lines and 0 < line <= len(self._source_lines):
            return self._source_lines[line - 1]
        return ""

    def _get_empty_value_for_type(self, value: Any) -> Any:
        """v4.8.6: Get an empty value of the same type for move operations.

        Used by -<== operator to clear source after move without destroying it.
        Returns empty container for containers, None for primitives.
        """
        from .cssl_types import Stack, Vector, Array, DataStruct, List, Dictionary, Map, Queue

        if isinstance(value, Stack):
            return Stack(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, Vector):
            return Vector(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, Array):
            return Array(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, DataStruct):
            return DataStruct(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, List):
            return List(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, Dictionary):
            return Dictionary(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, Map):
            return Map(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, Queue):
            return Queue(getattr(value, '_element_type', 'dynamic'))
        elif isinstance(value, list):
            return []
        elif isinstance(value, dict):
            return {}
        elif isinstance(value, str):
            return ""
        else:
            # For other types (int, float, objects), return None
            return None

    def execute(self, source: str) -> Any:
        """Execute CSSL service source code"""
        self._source_lines = source.splitlines()
        try:
            ast = parse_cssl(source)
            return self._execute_node(ast)
        except CSSLSyntaxError as e:
            raise self._format_error(e.line, str(e))
        except SyntaxError as e:
            raise CSSLRuntimeError(f"Syntax error: {e}")

    def execute_program(self, source: str) -> Any:
        """Execute standalone CSSL program (no service wrapper)"""
        self._source_lines = source.splitlines()
        try:
            ast = parse_cssl_program(source)
            return self._exec_program(ast)
        except CSSLSyntaxError as e:
            raise self._format_error(e.line, str(e))
        except SyntaxError as e:
            raise CSSLRuntimeError(f"Syntax error: {e}")

    def execute_ast(self, ast: ASTNode) -> Any:
        """Execute a pre-parsed AST"""
        return self._execute_node(ast)

    def execute_file(self, filepath: str) -> Any:
        """Execute a CSSL file (auto-detects service vs program format)"""
        import os
        self._current_file = os.path.basename(filepath)
        # v4.8.8: Track full path for relative payload resolution
        self._current_file_path = os.path.abspath(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        # Auto-detect: if file starts with service-init, use service parser
        # Otherwise use program parser (supports class, struct, define at top level)
        stripped = source.lstrip()
        if stripped.startswith('service-init') or stripped.startswith('service-run') or stripped.startswith('service-include'):
            return self.execute(source)
        else:
            return self.execute_program(source)

    def execute_program_file(self, filepath: str) -> Any:
        """Execute a standalone CSSL program file"""
        import os
        self._current_file = os.path.basename(filepath)
        # v4.8.8: Track full path for relative payload resolution
        self._current_file_path = os.path.abspath(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.execute_program(source)

    def _execute_node(self, node: ASTNode) -> Any:
        """Execute an AST node"""
        if node is None:
            return None
        method_name = f'_exec_{node.type.replace("-", "_")}'
        method = getattr(self, method_name, None)

        if method:
            return method(node)
        else:
            raise CSSLRuntimeError(f"Unknown node type: {node.type}", node.line)

    def _exec_service(self, node: ASTNode) -> ServiceDefinition:
        """Execute service root node"""
        service = ServiceDefinition()

        for child in node.children:
            if child.type == 'service-init':
                self._exec_service_init(child, service)
            elif child.type == 'service-include':
                self._exec_service_include(child, service)
            elif child.type == 'service-run':
                self._exec_service_run(child, service)
            # NEW: package block support
            elif child.type == 'package':
                self._exec_package(child, service)
            # NEW: package-includes block support
            elif child.type == 'package-includes':
                self._exec_package_includes(child, service)
            # NEW: struct at top level
            elif child.type == 'struct':
                struct_info = child.value
                if isinstance(struct_info, dict):
                    struct_name = struct_info.get('name', '')
                else:
                    struct_name = struct_info
                service.structs[struct_name] = child
                self._exec_struct(child)
            # NEW: define at top level
            elif child.type == 'function':
                func_info = child.value
                func_name = func_info.get('name')
                service.functions[func_name] = child
                self.scope.set(func_name, child)
            # v4.8.6: class at top level
            elif child.type == 'class':
                class_info = child.value
                class_name = class_info.get('name') if isinstance(class_info, dict) else class_info
                # Execute class definition to register it
                class_def = self._exec_class(child)
                if class_def:
                    service.classes[class_name] = class_def
            # v4.8.6: enum at top level
            elif child.type == 'enum':
                enum_info = child.value
                enum_name = enum_info.get('name') if isinstance(enum_info, dict) else enum_info
                enum_def = self._exec_enum(child)
                if enum_def:
                    service.enums[enum_name] = enum_def
            # v4.8.6: namespace at top level
            elif child.type == 'namespace':
                ns_info = child.value
                ns_name = ns_info.get('name') if isinstance(ns_info, dict) else ns_info
                ns_def = self._exec_namespace(child)
                if ns_def:
                    service.namespaces[ns_name] = ns_def

        return service

    def _exec_program(self, node: ASTNode) -> Any:
        """Execute standalone program (no service wrapper)

        A program can contain:
        - struct definitions
        - function definitions (define)
        - top-level statements (assignments, function calls, control flow)
        """
        result = None
        self._running = True  # Start running

        for child in node.children:
            # Check if exit() was called
            if not self._running:
                break

            if child.type == 'struct':
                self._exec_struct(child)
            elif child.type == 'class':
                self._exec_class(child)
            elif child.type == 'enum':
                self._exec_enum(child)
            elif child.type == 'namespace':
                self._exec_namespace(child)
            elif child.type == 'bytearrayed':
                self._exec_bytearrayed(child)
            elif child.type == 'function':
                self._exec_function(child)
            elif child.type == 'global_assignment':
                # Handle global variable declaration: global Name = value
                result = self._exec_global_assignment(child)
            elif child.type == 'typed_declaration':
                # Handle typed variable declaration: type<T> varName = value;
                result = self._exec_typed_declaration(child)
            elif child.type == 'instance_declaration':
                # Handle instance declaration: instance<"name"> varName;
                result = self._exec_instance_declaration(child)
            elif child.type == 'super_func':
                # Super-function for .cssl-pl payload files (#$run, #$exec, #$printl)
                result = self._exec_super_func(child)
            elif child.type in ('assignment', 'expression', 'inject', 'receive', 'flow',
                               'if', 'while', 'for', 'c_for', 'foreach', 'switch', 'try'):
                result = self._execute_node(child)
            elif child.type == 'call':
                result = self._eval_call(child)
            else:
                # Try to execute as statement
                try:
                    result = self._execute_node(child)
                except CSSLRuntimeError:
                    pass  # Ignore unknown nodes in program mode

        # Look for and execute main() if defined (only if still running)
        if self._running:
            main_func = self.scope.get('main')
            if main_func and isinstance(main_func, ASTNode) and main_func.type == 'function':
                try:
                    result = self._call_function(main_func, [])
                except CSSLReturn as ret:
                    result = ret.value

        return result

    def _exec_service_init(self, node: ASTNode, service: ServiceDefinition):
        """Execute service-init block"""
        # Property aliases mapping
        key_aliases = {
            'service-name': 'name',
            'service-version': 'version',
            'service-author': 'author',
            'service-description': 'description',
            'executation': 'execution',
            'execution': 'execution',
        }

        for child in node.children:
            if child.type == 'property' and child.value:
                key = child.value.get('key')
                value = child.value.get('value')

                # Apply alias mapping
                key = key_aliases.get(key, key)

                if key == 'name':
                    service.name = value
                elif key == 'version':
                    service.version = value
                elif key == 'author':
                    service.author = value
                elif key == 'description':
                    service.description = value
                elif key == 'dependencies':
                    if isinstance(value, list):
                        service.dependencies = value
                    elif isinstance(value, str):
                        service.dependencies = [value]
                elif key == 'autostart':
                    service.autostart = bool(value)
                elif key == 'priority':
                    service.priority = int(value)
                elif key == 'execution':
                    # Handle execution type
                    if value == 'Persistent':
                        service.autostart = True
                    elif value == 'Only-Once':
                        service.autostart = False

    def _exec_service_include(self, node: ASTNode, service: ServiceDefinition):
        """Execute service-include block for importing modules and files"""
        for child in node.children:
            if child.type == 'expression':
                # Evaluate the expression which may be:
                # - @ModuleName (standard module reference)
                # - include(cso_root('/path/to/file.cssl'))
                # - Variable assignment
                result = self._evaluate(child.value)

                # If result is a module, register it
                if result is not None:
                    # Check if it's a call result (like include())
                    if hasattr(result, 'name') and result.name:
                        # It's a ServiceDefinition from include()
                        # Merge its functions and structs into current service
                        if hasattr(result, 'functions'):
                            for fname, fnode in result.functions.items():
                                service.functions[fname] = fnode
                                self.scope.set(fname, fnode)
                        if hasattr(result, 'structs'):
                            for sname, snode in result.structs.items():
                                service.structs[sname] = snode

            elif child.type == 'assignment' or child.type == 'injection':
                # Handle: utils <== include(cso_root('/services/utils.cssl'));
                info = child.value
                name = info.get('name') or info.get('target')
                if isinstance(name, ASTNode):
                    name = name.value if name.type == 'identifier' else str(name)
                source = info.get('source') or info.get('value')
                value = self._evaluate(source)
                self.scope.set(name, value)

            elif child.type == 'call':
                # Direct function call like include(...)
                self._eval_call(child)

            elif child.type == 'module_ref':
                # @ModuleName reference - just evaluate to register
                self._evaluate(child)

    def _exec_service_run(self, node: ASTNode, service: ServiceDefinition):
        """Execute service-run block"""
        for child in node.children:
            if child.type == 'struct':
                # Handle new dict format: {'name': name, 'global': is_global}
                struct_info = child.value
                if isinstance(struct_info, dict):
                    struct_name = struct_info.get('name', '')
                else:
                    struct_name = struct_info
                service.structs[struct_name] = child
                self._exec_struct(child)
            elif child.type == 'function':
                func_info = child.value
                func_name = func_info.get('name')
                service.functions[func_name] = child
                self.scope.set(func_name, child)

    def _exec_package(self, node: ASTNode, service: ServiceDefinition):
        """Execute package {} block for service metadata - NEW

        Syntax:
        package {
            service = "ServiceName";
            exec = @Start();
            version = "1.0.0";
            description = "Beschreibung";
        }
        """
        exec_func = None

        for child in node.children:
            if child.type == 'package_property' and child.value:
                key = child.value.get('key')
                value_node = child.value.get('value')

                # Evaluate the value
                value = self._evaluate(value_node)

                if key == 'service':
                    service.name = value
                elif key == 'version':
                    service.version = value
                elif key == 'description':
                    service.description = value
                elif key == 'author':
                    service.author = value
                elif key == 'exec':
                    # Store exec function for later execution
                    exec_func = value_node

        # Store exec function reference for later
        if exec_func:
            service.functions['__exec__'] = exec_func

    def _exec_package_includes(self, node: ASTNode, service: ServiceDefinition):
        """Execute package-includes {} block for imports - NEW

        Syntax:
        package-includes {
            @Lists = get('list');
            @OS = get('os');
            @Time = get('time');
            @VSRam = get('vsramsdk');
        }
        """
        for child in node.children:
            if child.type == 'assignment':
                info = child.value
                target = info.get('target')
                value_node = info.get('value')

                # Evaluate the value (e.g., get('list'))
                value = self._evaluate(value_node)

                # Get target name
                if isinstance(target, ASTNode):
                    if target.type == 'module_ref':
                        # @ModuleName = get(...)
                        module_name = target.value
                        self._modules[module_name] = value
                    elif target.type == 'identifier':
                        # varName = get(...)
                        self.scope.set(target.value, value)
                elif isinstance(target, str):
                    self.scope.set(target, value)

            elif child.type == 'expression':
                # Evaluate expression statements
                self._evaluate(child.value)

            elif child.type == 'inject':
                # Handle: @Module <== get(...);
                target = child.value.get('target')
                source = self._evaluate(child.value.get('source'))

                if isinstance(target, ASTNode) and target.type == 'module_ref':
                    self._modules[target.value] = source
                elif isinstance(target, ASTNode) and target.type == 'identifier':
                    self.scope.set(target.value, source)

    def _exec_struct(self, node: ASTNode) -> Dict[str, Any]:
        """Execute struct block"""
        struct_data = {}

        # Get struct name and global flag
        struct_info = node.value
        if isinstance(struct_info, dict):
            struct_name = struct_info.get('name', '')
            is_global = struct_info.get('global', False)
        else:
            # Backwards compatibility: value is just the name
            struct_name = struct_info
            is_global = False

        for child in node.children:
            if child.type == 'injection':
                info = child.value
                name = info.get('name')
                source = info.get('source')
                value = self._evaluate(source)
                struct_data[name] = value
                self.scope.set(name, value)

            elif child.type == 'assignment':
                info = child.value
                name = info.get('name')
                value = self._evaluate(info.get('value'))
                struct_data[name] = value
                self.scope.set(name, value)

            elif child.type == 'function':
                func_info = child.value
                func_name = func_info.get('name')
                struct_data[func_name] = child
                self.scope.set(func_name, child)

            elif child.type == 'expression':
                # Execute expression statements like print()
                self._evaluate(child.value)

            elif child.type == 'call':
                # Direct function calls
                self._eval_call(child)

            else:
                # Try to execute other statement types
                try:
                    self._execute_node(child)
                except Exception:
                    pass

        # Register as global struct if decorated with (@)
        if is_global and struct_name:
            self.register_global_struct(struct_name, struct_data)

        return struct_data

    def _exec_enum(self, node: ASTNode) -> Dict[str, Any]:
        """Execute enum declaration - registers enum values in scope.

        Creates a dictionary-like enum object accessible via EnumName::VALUE syntax.

        Example:
            enum Colors { RED, GREEN, BLUE }
            Colors::RED  // returns 0
            Colors::GREEN  // returns 1

        v4.3.2: Support for embedded enum modification:
            embedded __NewEnum &OldEnum { ... }       // Replace OldEnum
            embedded __NewEnum &OldEnum ++ { ... }    // Add to OldEnum
            embedded __NewEnum &OldEnum -- { ... }    // Remove from OldEnum
        """
        enum_info = node.value
        enum_name = enum_info.get('name')
        members = enum_info.get('members', [])
        is_embedded = enum_info.get('is_embedded', False)
        replace_target = enum_info.get('replace_target')
        mode = enum_info.get('mode', 'replace')

        # Create enum object as a dict-like object with members
        new_values = {}
        for member in members:
            member_name = member['name']
            member_value = member['value']
            # Evaluate if value is an ASTNode
            if isinstance(member_value, ASTNode):
                member_value = self._evaluate(member_value)
            new_values[member_name] = member_value

        # v4.3.2: Handle embedded modification
        if is_embedded and replace_target:
            target_name = replace_target.lstrip('@') if replace_target.startswith('@') else replace_target

            if mode == 'add':
                # Get existing enum and add new values
                existing = self.scope.get(target_name) or self.global_scope.get(target_name) or {}
                if isinstance(existing, dict):
                    # For add mode, auto-increment from highest existing int value
                    max_val = -1
                    for v in existing.values():
                        if isinstance(v, int) and v > max_val:
                            max_val = v
                    # Update new values that don't have explicit values
                    for name, val in new_values.items():
                        if isinstance(val, int) and val <= max_val:
                            max_val += 1
                            new_values[name] = max_val
                    enum_obj = {**existing, **new_values}
                else:
                    enum_obj = new_values
            elif mode == 'remove':
                # Get existing enum and remove specified keys
                existing = self.scope.get(target_name) or self.global_scope.get(target_name) or {}
                if isinstance(existing, dict):
                    enum_obj = {k: v for k, v in existing.items() if k not in new_values}
                else:
                    enum_obj = {}
            else:
                # Replace mode - just use new values
                enum_obj = new_values

            self.scope.set(target_name, enum_obj)
            self.global_scope.set(target_name, enum_obj)
            if replace_target.startswith('@'):
                self._promoted_globals[target_name] = enum_obj
        else:
            # Regular enum - just register it
            enum_obj = new_values
            self.scope.set(enum_name, enum_obj)
            self.global_scope.set(enum_name, enum_obj)

        return enum_obj

    def _exec_bytearrayed(self, node: ASTNode) -> 'ByteArrayed':
        """Execute bytearrayed declaration - function-to-byte mapping with pattern matching.

        Creates a ByteArrayed object that:
        - Maps function references to byte positions (0x0, 0x1, etc.)
        - Executes functions "invisibly" when called to get return values
        - Matches case patterns based on return values
        - Supports indexing: MyBytes["0x0"] or MyBytes[0]

        Example:
            bytearrayed MyBytes {
                &func1;           // 0x0
                &func2;           // 0x1
                case {0, 1} {     // func1=0, func2=1
                    printl("Match!");
                }
            }
            MyBytes();            // Execute pattern matching
            x = MyBytes["0x0"];   // Get value at position 0
        """
        info = node.value
        name = info.get('name')
        func_refs = info.get('func_refs', [])
        cases = info.get('cases', [])
        default_block = info.get('default')

        # Create ByteArrayed object
        bytearrayed_obj = ByteArrayed(
            name=name,
            func_refs=func_refs,
            cases=cases,
            default_block=default_block,
            runtime=self
        )

        # Register in scope
        self.scope.set(name, bytearrayed_obj)
        self.global_scope.set(name, bytearrayed_obj)

        return bytearrayed_obj

    def _execute_bytearrayed_function(self, func_node: ASTNode) -> Any:
        """Execute a function with bytearrayed modifier (v4.7).

        Bytearrayed functions call &FuncRef() to get a value, then match
        against case patterns to determine which body to execute.

        Syntax:
            bytearrayed define Localize() {
                case "en": &GetLang() {
                    return "Hello";
                }
                case "de": &GetLang() {
                    return "Hallo";
                }
                default: {
                    return "Unknown";
                }
            }
        """
        case_blocks = []
        default_node = None
        func_ref_stmts = []  # v4.8.8: Collect &func; statements before case/default

        # Collect case/default blocks and func_ref statements
        for child in func_node.children:
            if not self._running:
                break
            if child.type == 'case':
                case_blocks.append(child)
            elif child.type == 'default':
                default_node = child
            elif child.type == 'func_ref':
                # v4.8.8: Collect func_ref statements (&n; &b(100);)
                func_ref_stmts.append(child)
            elif child.type == 'expression' and hasattr(child, 'value'):
                # Check if expression is a func_ref (ampersand expression)
                expr_val = child.value
                if hasattr(expr_val, 'type') and expr_val.type == 'func_ref':
                    func_ref_stmts.append(expr_val)

        # v4.8.8: Execute all func_ref statements and collect results
        collected_results = []
        for ref_stmt in func_ref_stmts:
            ref_info = ref_stmt.value if hasattr(ref_stmt, 'value') else ref_stmt
            if isinstance(ref_info, dict):
                func_name = ref_info.get('name')
                func_args = ref_info.get('args', [])
            else:
                func_name = str(ref_info)
                func_args = []

            eval_args = [self._evaluate(a) for a in func_args] if func_args else []

            # Call the function
            try:
                result = None
                func_def = self.scope.get(func_name) or self.global_scope.get(func_name)
                if func_def and hasattr(func_def, 'type') and func_def.type == 'function':
                    result = self._call_function(func_def, eval_args)
                elif callable(func_def):
                    result = func_def(*eval_args)
            except Exception as e:
                result = None

            collected_results.append(result)

        # Process each case block
        for case_node in case_blocks:
            case_value = case_node.value
            if not isinstance(case_value, dict):
                continue

            patterns = case_value.get('patterns', [])
            func_refs = case_value.get('func_refs', [])
            body = case_value.get('body', [])
            is_except = case_value.get('except', False)  # v4.9.4: Inverted matching for except blocks

            # v4.8.8: If we have collected results from &func; statements,
            # match patterns against those results (tuple pattern matching)
            if collected_results and not func_refs:
                # Match collected_results against patterns
                all_match = True
                if isinstance(patterns, list) and len(patterns) == 1 and isinstance(patterns[0], tuple):
                    # Tuple pattern: case {0, 0}: -> patterns = [(0, 0)]
                    expected = list(patterns[0])
                    if len(expected) == len(collected_results):
                        for i, (exp, got) in enumerate(zip(expected, collected_results)):
                            if exp != got:
                                all_match = False
                                break
                    else:
                        all_match = False
                elif len(patterns) == len(collected_results):
                    # Comma-separated patterns: case 0, 0: -> patterns = [0, 0]
                    for i, (exp, got) in enumerate(zip(patterns, collected_results)):
                        if exp != got:
                            all_match = False
                            break
                else:
                    all_match = False
            else:
                # Original behavior: execute func_refs from case and match
                all_match = True
                for i, func_ref in enumerate(func_refs):
                    func_name = func_ref.get('name')
                    func_args = func_ref.get('args', [])
                    eval_args = [self._evaluate(a) for a in func_args]

                    try:
                        result = None
                        if self._current_instance and hasattr(self._current_instance, 'get_method'):
                            method = self._current_instance.get_method(func_name)
                            if method:
                                result = self._call_method(self._current_instance, method, eval_args)
                            else:
                                func_def = self.scope.get(func_name) or self.global_scope.get(func_name)
                                if func_def and hasattr(func_def, 'type') and func_def.type == 'function':
                                    result = self._call_function(func_def, eval_args)
                                elif callable(func_def):
                                    result = func_def(*eval_args)
                        else:
                            func_def = self.scope.get(func_name) or self.global_scope.get(func_name)
                            if func_def and hasattr(func_def, 'type') and func_def.type == 'function':
                                result = self._call_function(func_def, eval_args)
                            elif callable(func_def):
                                result = func_def(*eval_args)
                    except Exception as e:
                        result = None

                    if i < len(patterns):
                        pattern = patterns[i]
                        if result != pattern:
                            all_match = False
                            break

            # v4.9.4: For except blocks, invert the match logic
            should_execute = (not all_match) if is_except else all_match

            if should_execute:
                # Execute the case body
                for stmt in body:
                    try:
                        self._execute_node(stmt)
                    except CSSLReturn as ret:
                        return ret.value
                return None

        # No case matched - execute default
        if default_node and isinstance(default_node.value, dict):
            body = default_node.value.get('body', [])
            for stmt in body:
                try:
                    self._execute_node(stmt)
                except CSSLReturn as ret:
                    return ret.value

        return None

    def _match_bytearrayed_pattern(self, pattern: Any, values: List[Any]) -> bool:
        """Match a pattern against collected bytearrayed values.

        Patterns can be:
        - List/tuple: [10, 7] matches if values[0]==10 and values[1]==7
        - Dict with values: evaluates expressions
        - Single value: matches first collected value
        - Wildcard '_': matches any value
        """
        if pattern is None:
            return False

        # Convert pattern to list if needed
        if isinstance(pattern, (list, tuple)):
            pattern_list = list(pattern)
        elif isinstance(pattern, dict):
            # Dict patterns - extract values
            pattern_list = list(pattern.values())
        else:
            pattern_list = [pattern]

        # Match each pattern element against collected values
        for i, pat_val in enumerate(pattern_list):
            if i >= len(values):
                return False

            # Wildcard matches anything
            if pat_val == '_' or pat_val is None:
                continue

            # Exact match
            if values[i] != pat_val:
                return False

        return True

    def _exec_class(self, node: ASTNode) -> CSSLClass:
        """Execute class definition - registers class in scope.

        Parses class members and methods, creating a CSSLClass object
        that can be instantiated with 'new'.
        Supports inheritance via 'extends' keyword and method overwriting via 'overwrites'.

        Classes are local by default. Use 'global class' or 'class @Name' for global classes.
        """
        class_info = node.value
        class_name = class_info.get('name')
        is_global = class_info.get('is_global', False)
        extends_class_name = class_info.get('extends')
        extends_is_python = class_info.get('extends_is_python', False)
        overwrites_class_name = class_info.get('overwrites')
        overwrites_is_python = class_info.get('overwrites_is_python', False)
        uses_memory = class_info.get('uses_memory')  # v4.9.0

        # v4.9.0: Handle ': uses memory(address)' - deferred execution binding
        # Class constructor is hooked to the host's execution
        if uses_memory:
            host_obj = self._evaluate(uses_memory)
            # Convert to hashable key - use name for functions, id() for others
            if isinstance(host_obj, ASTNode):
                host_key = host_obj.value.get('name') if isinstance(host_obj.value, dict) else str(id(host_obj))
            elif isinstance(host_obj, str):
                host_key = host_obj
            else:
                host_key = str(id(host_obj))
            if not hasattr(self, '_memory_hooks'):
                self._memory_hooks = {}
            if host_key not in self._memory_hooks:
                self._memory_hooks[host_key] = []
            self._memory_hooks[host_key].append(('class', node))
            # Continue to register the class normally so it can be referenced
            # Hooks execute when the host is called

        # Resolve parent class if extends is specified
        parent_class = None
        if extends_class_name:
            if extends_is_python:
                # extends $PythonObject - look up in shared objects
                from ..cssl_bridge import _live_objects, SharedObjectProxy
                if extends_class_name in _live_objects:
                    parent_class = _live_objects[extends_class_name]
                    # Unwrap SharedObjectProxy if needed
                    if isinstance(parent_class, SharedObjectProxy):
                        parent_class = parent_class._obj
                else:
                    # Also check scope with $ prefix
                    parent_class = self.global_scope.get(f'${extends_class_name}')
            else:
                # Try to resolve from scope (could be CSSL class or variable holding Python object)
                parent_class = self.scope.get(extends_class_name)
                if parent_class is None:
                    parent_class = self.global_scope.get(extends_class_name)

            if parent_class is None:
                # Build detailed error for extends
                available_classes = _get_available_classes(self.scope, self.global_scope, self._promoted_globals)
                similar = _find_similar_names(extends_class_name, available_classes)

                if similar:
                    hint = f"Did you mean: {', '.join(similar)}?"
                elif extends_is_python:
                    hint = f"Python object '${extends_class_name}' not found. Use share() to share Python objects first."
                else:
                    hint = f"Define class '{extends_class_name}' before this class, or use 'extends $PyObject' for Python objects"

                raise self._format_error(
                    node.line,
                    f"Cannot extend unknown class '{extends_class_name}'",
                    hint
                )

            # Auto-wrap Python objects for inheritance
            from .cssl_builtins import CSSLizedPythonObject
            if not isinstance(parent_class, (CSSLClass, CSSLizedPythonObject)):
                # Wrap raw Python object
                parent_class = CSSLizedPythonObject(parent_class, self)

        members = {}  # Member variable defaults/types
        methods = {}  # Method AST nodes
        constructors = []  # List of constructors (multiple allowed with constr keyword)
        constructor = None  # Primary constructor (backward compatibility)

        # Get class parameters and extends args
        class_params = class_info.get('class_params', [])
        extends_args = class_info.get('extends_args', [])

        # v4.2.0: Handle 'supports' language transformation for raw_body
        supports_language = class_info.get('supports_language')
        raw_body = class_info.get('raw_body')

        if raw_body and supports_language:
            # Transform raw body from target language to CSSL and parse
            transformed_children = self._transform_and_parse_class_body(
                raw_body, supports_language, class_name
            )
            # Add transformed children to node's children
            node.children = transformed_children

        destructors = []  # v4.8.8: Store destructors (constr ~Name())

        for child in node.children:
            if child.type == 'constructor':
                # v4.8.8: Check if this is a destructor (~Name)
                if child.value.get('is_destructor'):
                    destructors.append(child)
                else:
                    # New-style constructor from 'constr' keyword
                    constructors.append(child)

            elif child.type == 'function':
                # This is a method or old-style constructor
                func_info = child.value
                method_name = func_info.get('name')

                if func_info.get('is_constructor') or method_name == class_name or method_name == '__init__':
                    constructor = child
                else:
                    methods[method_name] = child

            elif child.type == 'typed_declaration':
                # This is a member variable
                decl = child.value
                member_name = decl.get('name')
                member_type = decl.get('type')
                member_value = decl.get('value')

                # Store member info with type and optional default
                members[member_name] = {
                    'type': member_type,
                    'default': self._evaluate(member_value) if member_value else None
                }

        # Create class definition object
        class_def = CSSLClass(
            name=class_name,
            members=members,
            methods=methods,
            constructor=constructor,
            parent=parent_class
        )
        # Store additional constructor info
        class_def.constructors = constructors  # Multiple constructors from 'constr' keyword
        class_def.destructors = destructors    # v4.8.8: Destructors (constr ~Name())
        class_def.class_params = class_params  # Class-level constructor parameters
        class_def.extends_args = extends_args  # Arguments to pass to parent constructor

        # Register class in scope (local by default, global if marked)
        self.scope.set(class_name, class_def)
        if is_global:
            self.global_scope.set(class_name, class_def)
            self._promoted_globals[class_name] = class_def

        # v4.2.5: Handle &target replacement for classes
        # embedded class MyClass &$Target { } - immediate replacement
        # class MyClass &$Target { } - deferred until instantiation
        append_ref_class = class_info.get('append_ref_class')
        is_embedded = class_info.get('is_embedded', False)
        if append_ref_class and is_embedded:
            append_ref_member = class_info.get('append_ref_member')
            self._overwrite_class_target(append_ref_class, append_ref_member, class_def)
            class_def._target_applied = True
        elif append_ref_class:
            # Store reference info for deferred replacement
            class_def._pending_target = {
                'append_ref_class': append_ref_class,
                'append_ref_member': class_info.get('append_ref_member')
            }

        # Handle class overwrites - replace methods in target class
        if overwrites_class_name:
            self._apply_class_overwrites(
                class_def, overwrites_class_name, overwrites_is_python
            )

        return class_def

    def _apply_class_overwrites(self, new_class: CSSLClass, target_name: str, is_python: bool):
        """Apply method overwrites from new_class to target class/object.

        When a class has 'overwrites' specified, all methods defined in new_class
        will replace the corresponding methods in the target.
        """
        from .cssl_builtins import CSSLizedPythonObject

        # Resolve target
        target = None
        if is_python:
            from ..cssl_bridge import _live_objects
            if target_name in _live_objects:
                target = _live_objects[target_name]
        else:
            target = self.scope.get(target_name)
            if target is None:
                target = self.global_scope.get(target_name)

        if target is None:
            return  # Target not found, silently skip

        # Get methods to overwrite
        methods_to_overwrite = new_class.methods

        if is_python and hasattr(target, '__class__'):
            # Python object - overwrite methods on the object/class
            for method_name, method_node in methods_to_overwrite.items():
                # Create a Python-callable wrapper for the CSSL method
                wrapper = self._create_method_wrapper(method_node, target)
                # Set on the object
                try:
                    setattr(target, method_name, wrapper)
                except AttributeError:
                    # Try setting on class instead
                    try:
                        setattr(target.__class__, method_name, wrapper)
                    except (AttributeError, TypeError):
                        pass  # Can't set attribute on immutable type
        elif isinstance(target, CSSLClass):
            # CSSL class - directly replace methods
            for method_name, method_node in methods_to_overwrite.items():
                target.methods[method_name] = method_node
        elif isinstance(target, CSSLizedPythonObject):
            # CSSLized Python object - get underlying object and overwrite
            py_obj = target.get_python_obj()
            for method_name, method_node in methods_to_overwrite.items():
                wrapper = self._create_method_wrapper(method_node, py_obj)
                try:
                    setattr(py_obj, method_name, wrapper)
                except AttributeError:
                    try:
                        setattr(py_obj.__class__, method_name, wrapper)
                    except (AttributeError, TypeError):
                        pass  # Can't set attribute on immutable type

    def _create_method_wrapper(self, method_node: ASTNode, instance: Any):
        """Create a Python-callable wrapper for a CSSL method that works with an instance."""
        def wrapper(*args, **kwargs):
            # Set up instance context for this->
            old_instance = self._current_instance
            # Create a fake CSSLInstance-like wrapper if needed
            self._current_instance = instance
            try:
                return self._call_function(method_node, list(args), kwargs)
            finally:
                self._current_instance = old_instance
        return wrapper

    def _exec_namespace(self, node: ASTNode) -> 'CSSLNamespace':
        """Execute namespace definition - registers namespace in scope.

        Namespaces group functions, classes, and nested namespaces together,
        accessible via the :: operator (e.g., mylib::myFunc()).

        Syntax:
            namespace mylib {
                void myFunc() { ... }
                class MyClass { ... }
                namespace nested { ... }
            }

        Access: mylib::myFunc(), mylib::MyClass, mylib::nested::innerFunc()
        """
        ns_name = node.value.get('name') if isinstance(node.value, dict) else node.value

        # Create namespace object
        namespace = CSSLNamespace(ns_name)

        # Process namespace members
        for child in node.children:
            if child.type == 'function':
                # Register function in namespace
                func_info = child.value
                func_name = func_info.get('name')
                namespace.functions[func_name] = child
            elif child.type == 'class':
                # Register class in namespace
                class_info = child.value
                class_name = class_info.get('name')
                cssl_class = self._exec_class(child)
                namespace.classes[class_name] = cssl_class
            elif child.type == 'enum':
                # Register enum in namespace
                enum_info = child.value
                enum_name = enum_info.get('name')
                self._exec_enum(child)
                namespace.enums[enum_name] = self.scope.get(enum_name)
            elif child.type == 'struct':
                # Register struct in namespace
                struct_info = child.value
                if isinstance(struct_info, dict):
                    struct_name = struct_info.get('name', '')
                else:
                    struct_name = struct_info
                namespace.structs[struct_name] = child
            elif child.type == 'namespace':
                # Nested namespace
                nested_ns = self._exec_namespace(child)
                namespace.namespaces[nested_ns.name] = nested_ns

        # Register namespace in both local and global scope for :: access
        self.scope.set(ns_name, namespace)
        self.global_scope.set(ns_name, namespace)

        return namespace

    def _transform_and_parse_class_body(self, raw_body: str, language: str, class_name: str) -> list:
        """Transform source code from another language to CSSL and parse as class body.

        v4.2.0: Used for 'supports <lang>' in class definitions.

        Args:
            raw_body: Raw source code in the target language
            language: Language identifier (py, python, cpp, c++, js, javascript, etc.)
            class_name: Name of the class (for constructor recognition)

        Returns:
            List of parsed AST nodes representing methods, constructors, and members
        """
        import textwrap
        from .cssl_languages import get_language
        from .cssl_parser import parse_cssl_program, ASTNode

        # Normalize language ID
        lang_id = language.lstrip('@').lower()

        # Get language support and transformer
        lang_support = get_language(lang_id)
        if lang_support is None:
            raise CSSLRuntimeError(f"Unknown language '{lang_id}' in 'supports' clause")

        # Dedent the raw body to normalize indentation
        # This fixes the issue where code inside CSSL {} has relative indentation
        dedented_body = textwrap.dedent(raw_body)

        # Transform the raw body to CSSL syntax
        transformer = lang_support.get_transformer()
        transformed_source = transformer.transform_source(dedented_body)

        # Wrap in a dummy class for parsing
        wrapper_source = f"class _TempClass {{\n{transformed_source}\n}}"

        try:
            ast = parse_cssl_program(wrapper_source)
        except Exception as e:
            raise CSSLRuntimeError(
                f"Failed to parse transformed '{lang_id}' code: {e}\n"
                f"Dedented:\n{dedented_body}\n"
                f"Transformed:\n{transformed_source}"
            )

        # Extract children from the parsed temp class
        children = []
        for top_level in ast.children:
            if top_level.type == 'class':
                for child in top_level.children:
                    # Mark constructor if method name matches class_name or is __init__
                    if child.type == 'function':
                        func_info = child.value
                        method_name = func_info.get('name')
                        if method_name == class_name or method_name == '__init__':
                            child.value['is_constructor'] = True
                    children.append(child)
                break

        return children

    def _transform_and_parse_function_body(self, raw_body: str, language: str) -> list:
        """Transform source code from another language to CSSL and parse as function body.

        v4.2.0: Used for 'supports <lang>' in function definitions.

        Args:
            raw_body: Raw source code in the target language
            language: Language identifier (py, python, cpp, c++, js, javascript, etc.)

        Returns:
            List of parsed AST nodes representing statements in the function body
        """
        import textwrap
        from .cssl_languages import get_language
        from .cssl_parser import parse_cssl_program

        # Normalize language ID
        lang_id = language.lstrip('@').lower()

        # Get language support and transformer
        lang_support = get_language(lang_id)
        if lang_support is None:
            raise CSSLRuntimeError(f"Unknown language '{lang_id}' in 'supports' clause")

        # Dedent the raw body to normalize indentation
        dedented_body = textwrap.dedent(raw_body)

        # Transform the raw body to CSSL syntax
        transformer = lang_support.get_transformer()
        transformed_source = transformer.transform_source(dedented_body)

        # Wrap in a dummy function for parsing
        wrapper_source = f"define _TempFunc() {{\n{transformed_source}\n}}"

        try:
            ast = parse_cssl_program(wrapper_source)
        except Exception as e:
            raise CSSLRuntimeError(
                f"Failed to parse transformed '{lang_id}' code: {e}\n"
                f"Dedented:\n{dedented_body}\n"
                f"Transformed:\n{transformed_source}"
            )

        # Extract children from the parsed temp function
        children = []
        for top_level in ast.children:
            if top_level.type == 'function':
                children = top_level.children
                break

        return children

    def _exec_function(self, node: ASTNode) -> Any:
        """Execute function definition - registers it and handles extends/overwrites.

        Syntax:
            define func() { ... }                           - Local function
            global define func() { ... }                    - Global function
            define @func() { ... }                          - Global function (alternative)
            define func : extends otherFunc() { ... }       - Inherit local vars
            define func : overwrites otherFunc() { ... }    - Replace otherFunc
        """
        func_info = node.value
        func_name = func_info.get('name')
        is_global = func_info.get('is_global', False)
        extends_func = func_info.get('extends')
        extends_is_python = func_info.get('extends_is_python', False)
        overwrites_func = func_info.get('overwrites')
        overwrites_is_python = func_info.get('overwrites_is_python', False)
        uses_memory = func_info.get('uses_memory')  # v4.9.0

        # v4.9.0: Handle ': uses memory(address)' - deferred execution binding
        # Function is not executed immediately but deferred until the host is called
        # Calling this function directly is a no-op - it only triggers when the host is called
        if uses_memory:
            # Evaluate the address expression (can be function ref, address string, etc.)
            host_obj = self._evaluate(uses_memory)

            # Resolve the actual target function to get its name for hook lookup
            host_key = None
            from .cssl_types import Address
            if isinstance(host_obj, Address):
                # Address type - reflect to get the original object
                reflected = host_obj.reflect()
                if isinstance(reflected, ASTNode) and reflected.type == 'function':
                    host_key = reflected.value.get('name')
                elif reflected is not None:
                    host_key = str(id(reflected))
            elif isinstance(host_obj, ASTNode):
                # Direct function reference
                host_key = host_obj.value.get('name') if isinstance(host_obj.value, dict) else str(id(host_obj))
            elif isinstance(host_obj, str):
                host_key = host_obj  # Address string like "0x..."
            else:
                host_key = str(id(host_obj))

            if host_key:
                # Store the function as a memory hook
                if not hasattr(self, '_memory_hooks'):
                    self._memory_hooks = {}  # key -> list of hooked functions
                if host_key not in self._memory_hooks:
                    self._memory_hooks[host_key] = []
                self._memory_hooks[host_key].append(node)

            # Mark function as a hook (calling it directly is a no-op)
            node.value['_is_memory_hook'] = True
            # Register the function by name for reference
            self.scope.set(func_name, node)
            if is_global:
                self.global_scope.set(func_name, node)
            return None

        # Get append/overwrite reference info (&Class::method syntax)
        append_mode = func_info.get('append_mode', False)
        append_ref_class = func_info.get('append_ref_class')
        append_ref_member = func_info.get('append_ref_member')

        # Store function extends info for runtime use
        if extends_func:
            node.value['_extends_resolved'] = self._resolve_function_target(
                extends_func, extends_is_python
            )

        # Handle &Class::method syntax
        # Without ++ = full replacement
        # With ++ = append (run original first, then new code)
        # v4.2.5: Only do immediate replacement if is_embedded=True
        #         For regular 'define', replacement is deferred until function is called
        is_embedded = func_info.get('is_embedded', False)
        if append_ref_class and is_embedded:
            if append_mode:
                # Append mode: wrap original to run original + new
                self._append_to_target(append_ref_class, append_ref_member, node)
            else:
                # Full replacement
                self._overwrite_target(append_ref_class, append_ref_member, node)
            # Mark as already applied so we don't apply again on call
            node.value['_target_applied'] = True

        # Handle overwrites keyword - replace the target function
        if overwrites_func:
            target = self._resolve_function_target(overwrites_func, overwrites_is_python)
            if target is not None:
                # Store original for reference
                node.value['_overwrites_original'] = target
                # Replace the target function with this one
                if overwrites_is_python:
                    from ..cssl_bridge import _live_objects
                    if overwrites_func in _live_objects:
                        # Create a wrapper that calls the CSSL function
                        _live_objects[overwrites_func] = self._create_python_wrapper(node)
                else:
                    # Replace in CSSL scope
                    self.scope.set(overwrites_func, node)
                    self.global_scope.set(overwrites_func, node)

        # v4.9.3: Check for async modifier - wrap function in CSSLAsyncFunction
        modifiers = func_info.get('modifiers', [])
        if 'async' in modifiers:
            # Create async wrapper that returns a Future when called
            async_func = CSSLAsyncFunction(func_name, node, self)
            self.scope.set(func_name, async_func)
            if is_global:
                self.global_scope.set(func_name, async_func)
                self._promoted_globals[func_name] = async_func
            return None

        # v4.9.3: Check if function is a generator (contains yield statements)
        # Return type 'generator' or body contains yield
        return_type = func_info.get('return_type', '')
        if return_type == 'generator' or self._contains_yield(node):
            # Mark as generator function - will create CSSLGenerator on call
            node.value['_is_generator'] = True

        # Register the function (local by default, global if marked)
        self.scope.set(func_name, node)
        if is_global:
            self.global_scope.set(func_name, node)
            self._promoted_globals[func_name] = node
        return None

    def _contains_yield(self, node: ASTNode) -> bool:
        """Check if a function node contains yield statements."""
        if node is None:
            return False

        def _search_yield(n):
            if n is None:
                return False
            if hasattr(n, 'type') and n.type in ('yield', 'yield_expr'):
                return True
            if hasattr(n, 'children'):
                for child in n.children:
                    if _search_yield(child):
                        return True
            if hasattr(n, 'value'):
                # Check if value is an ASTNode (nested structure)
                if isinstance(n.value, dict):
                    for v in n.value.values():
                        if isinstance(v, ASTNode) and _search_yield(v):
                            return True
                        if isinstance(v, list):
                            for item in v:
                                if isinstance(item, ASTNode) and _search_yield(item):
                                    return True
            return False

        # Search in function body (children)
        for child in node.children:
            if _search_yield(child):
                return True
        return False

    def _resolve_function_target(self, name: str, is_python: bool) -> Any:
        """Resolve a function target for extends/overwrites."""
        if is_python:
            from ..cssl_bridge import _live_objects
            if name in _live_objects:
                return _live_objects[name]
            return self.global_scope.get(f'${name}')
        else:
            target = self.scope.get(name)
            if target is None:
                target = self.global_scope.get(name)
            return target

    def _create_python_wrapper(self, func_node: ASTNode):
        """Create a Python-callable wrapper for a CSSL function."""
        def wrapper(*args, **kwargs):
            return self._call_function(func_node, list(args), kwargs)
        return wrapper

    def _create_python_method_wrapper(self, func_node: ASTNode, python_obj):
        """Create a Python-callable wrapper that passes python_obj as 'this'.

        v4.3.0: Used when replacing Python object methods with CSSL functions.
        The wrapper ensures 'this->' in CSSL refers to the Python object.
        """
        runtime = self
        _captured_obj = python_obj

        def wrapper(*args, **kwargs):
            # Save current instance context
            old_instance = runtime._current_instance
            old_this = runtime.scope.get('this')
            try:
                # Set Python object as current instance for this-> access
                runtime._current_instance = _captured_obj
                runtime.scope.set('this', _captured_obj)
                return runtime._call_function(func_node, list(args), kwargs)
            finally:
                # Restore previous context
                runtime._current_instance = old_instance
                if old_this is not None:
                    runtime.scope.set('this', old_this)
                elif 'this' in runtime.scope.variables:
                    del runtime.scope.variables['this']

        return wrapper

    def _create_generator(self, func_node: ASTNode, args: List[Any], kwargs: Dict[str, Any] = None) -> CSSLGenerator:
        """Create a CSSLGenerator for a generator function - v4.9.3

        Generator functions are functions that contain yield statements.
        When called, they return a CSSLGenerator object that can be iterated.

        Example CSSL:
            generator<int> define Range(int n) {
                int i = 0;
                while (i < n) {
                    yield i;
                    i = i + 1;
                }
            }

            gen = Range(5);
            while (gen.has_next()) {
                printl(gen.next());
            }
        """
        func_info = func_node.value
        params = func_info.get('params', [])
        kwargs = kwargs or {}
        func_name = func_info.get('name', 'anonymous')

        # Set up scope with parameters first (before creating generator)
        old_scope = self.scope
        gen_scope = Scope(parent=self.scope)

        # Bind parameters
        for i, param in enumerate(params):
            if isinstance(param, dict):
                param_name = param['name']
                param_default = param.get('default')
            else:
                param_name = param
                param_default = None

            # Get value from kwargs, args, or default
            if param_name in kwargs:
                value = kwargs[param_name]
            elif i < len(args):
                value = args[i]
            elif param_default is not None:
                self.scope = gen_scope
                value = self._evaluate(param_default)
                self.scope = old_scope
            else:
                value = None

            gen_scope.set(param_name, value)

        # Generator execution using a Python generator with proper state management
        runtime = self
        # Shared container for sent values - accessible to both Python generator and CSSL
        sent_container = {'value': None}

        def cssl_generator_func():
            # Execute generator body, properly managing scope around each yield
            for child in func_node.children:
                if not runtime._running:
                    return

                # Save caller's scope before entering generator scope
                caller_scope = runtime.scope
                runtime.scope = gen_scope

                try:
                    if child.type == 'yield':
                        # Direct yield node
                        value = runtime._evaluate(child.value) if child.value else None
                        runtime.scope = caller_scope  # Restore before yield
                        sent_container['value'] = yield value  # Capture sent value!
                        runtime.scope = gen_scope
                        gen_scope.set('__sent__', sent_container['value'])
                    elif child.type == 'assignment' and _is_yield_assignment(child):
                        # Handle: received = yield value
                        yield_node = child.value.get('value')
                        if yield_node and yield_node.type in ('yield', 'yield_expr'):
                            yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                            runtime.scope = caller_scope
                            sent_container['value'] = yield yield_val  # Capture sent value!
                            runtime.scope = gen_scope
                            # Assign sent value to the target variable
                            target_name = _get_target_name(child.value.get('target'))
                            if target_name:
                                gen_scope.set(target_name, sent_container['value'])
                    elif child.type == 'while':
                        # While loop - handle yield inside
                        for val in _execute_generator_while(child, sent_container):
                            runtime.scope = caller_scope
                            sent_container['value'] = yield val
                            runtime.scope = gen_scope
                            gen_scope.set('__sent__', sent_container['value'])
                    elif child.type in ('for', 'c_for'):
                        for val in _execute_generator_for(child, sent_container):
                            runtime.scope = caller_scope
                            sent_container['value'] = yield val
                            runtime.scope = gen_scope
                            gen_scope.set('__sent__', sent_container['value'])
                    elif child.type == 'foreach':
                        for val in _execute_generator_foreach(child, sent_container):
                            runtime.scope = caller_scope
                            sent_container['value'] = yield val
                            runtime.scope = gen_scope
                            gen_scope.set('__sent__', sent_container['value'])
                    elif child.type == 'if':
                        for val in _execute_generator_if(child, sent_container):
                            runtime.scope = caller_scope
                            sent_container['value'] = yield val
                            runtime.scope = gen_scope
                            gen_scope.set('__sent__', sent_container['value'])
                    elif child.type == 'return':
                        runtime.scope = caller_scope
                        return
                    else:
                        # Regular statement
                        try:
                            runtime._execute_node(child)
                        except CSSLYield as y:
                            runtime.scope = caller_scope
                            sent_container['value'] = yield y.value
                            runtime.scope = gen_scope
                            gen_scope.set('__sent__', sent_container['value'])
                        except CSSLReturn:
                            runtime.scope = caller_scope
                            return
                finally:
                    runtime.scope = caller_scope

        def _is_yield_assignment(node):
            """Check if node is an assignment with yield on RHS."""
            if node.type != 'assignment':
                return False
            val = node.value.get('value')
            return val and hasattr(val, 'type') and val.type in ('yield', 'yield_expr')

        def _get_target_name(target):
            """Extract variable name from assignment target ASTNode."""
            if isinstance(target, str):
                return target
            if hasattr(target, 'type'):
                if target.type == 'identifier':
                    return target.value
            return None

        def _execute_generator_while(node, sent_container):
            while runtime._running:
                # Always restore gen_scope at start of each iteration (may have been changed by yield)
                runtime.scope = gen_scope
                if not runtime._evaluate(node.value.get('condition')):
                    break
                try:
                    for child in node.children:
                        runtime.scope = gen_scope  # Ensure gen_scope for all operations
                        if child.type == 'yield':
                            value = runtime._evaluate(child.value) if child.value else None
                            yield value
                        elif child.type == 'assignment' and _is_yield_assignment(child):
                            # Handle: received = yield value inside while
                            yield_node = child.value.get('value')
                            if yield_node and yield_node.type in ('yield', 'yield_expr'):
                                yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                                yield yield_val
                                # After yield, sent_container has the sent value
                                target_name = _get_target_name(child.value.get('target'))
                                if target_name:
                                    gen_scope.set(target_name, sent_container['value'])
                        else:
                            try:
                                runtime._execute_node(child)
                            except CSSLYield as y:
                                yield y.value
                            except CSSLReturn:
                                return
                except CSSLBreak:
                    break
                except CSSLContinue:
                    continue

        def _execute_generator_for(node, sent_container):
            if node.type == 'c_for':
                init = node.value.get('init')
                condition = node.value.get('condition')
                update = node.value.get('update')

                runtime.scope = gen_scope
                if init:
                    runtime._execute_node(init)

                while runtime._running:
                    # Restore gen_scope at start of each iteration
                    runtime.scope = gen_scope
                    if condition is not None and not runtime._evaluate(condition):
                        break
                    try:
                        for child in node.children:
                            runtime.scope = gen_scope
                            if child.type == 'yield':
                                value = runtime._evaluate(child.value) if child.value else None
                                yield value
                            elif child.type == 'assignment' and _is_yield_assignment(child):
                                yield_node = child.value.get('value')
                                if yield_node and yield_node.type in ('yield', 'yield_expr'):
                                    yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                                    yield yield_val
                                    target = child.value.get('target')
                                    if target:
                                        gen_scope.set(target, sent_container['value'])
                            else:
                                try:
                                    runtime._execute_node(child)
                                except CSSLYield as y:
                                    yield y.value
                                except CSSLReturn:
                                    return
                    except CSSLBreak:
                        break
                    except CSSLContinue:
                        pass

                    runtime.scope = gen_scope
                    if update:
                        runtime._evaluate(update)
            else:
                runtime.scope = gen_scope
                var_name = node.value.get('var')
                start = int(runtime._evaluate(node.value.get('start')))
                end = int(runtime._evaluate(node.value.get('end')))
                step_node = node.value.get('step')
                step = int(runtime._evaluate(step_node)) if step_node else 1

                for i in range(start, end, step):
                    if not runtime._running:
                        break
                    runtime.scope = gen_scope  # Restore at start of each iteration
                    gen_scope.set(var_name, i)
                    try:
                        for child in node.children:
                            runtime.scope = gen_scope
                            if child.type == 'yield':
                                value = runtime._evaluate(child.value) if child.value else None
                                yield value
                            elif child.type == 'assignment' and _is_yield_assignment(child):
                                yield_node = child.value.get('value')
                                if yield_node and yield_node.type in ('yield', 'yield_expr'):
                                    yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                                    yield yield_val
                                    target = child.value.get('target')
                                    if target:
                                        gen_scope.set(target, sent_container['value'])
                            else:
                                try:
                                    runtime._execute_node(child)
                                except CSSLYield as y:
                                    yield y.value
                                except CSSLReturn:
                                    return
                    except CSSLBreak:
                        break
                    except CSSLContinue:
                        continue

        def _execute_generator_foreach(node, sent_container):
            runtime.scope = gen_scope
            var_name = node.value.get('var')
            iterable = runtime._evaluate(node.value.get('iterable'))

            if hasattr(iterable, '__iter__'):
                for item in iterable:
                    if not runtime._running:
                        break
                    runtime.scope = gen_scope  # Restore at start of each iteration
                    gen_scope.set(var_name, item)
                    try:
                        for child in node.children:
                            runtime.scope = gen_scope
                            if child.type == 'yield':
                                value = runtime._evaluate(child.value) if child.value else None
                                yield value
                            elif child.type == 'assignment' and _is_yield_assignment(child):
                                yield_node = child.value.get('value')
                                if yield_node and yield_node.type in ('yield', 'yield_expr'):
                                    yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                                    yield yield_val
                                    target = child.value.get('target')
                                    if target:
                                        gen_scope.set(target, sent_container['value'])
                            else:
                                try:
                                    runtime._execute_node(child)
                                except CSSLYield as y:
                                    yield y.value
                                except CSSLReturn:
                                    return
                    except CSSLBreak:
                        break
                    except CSSLContinue:
                        continue

        def _execute_generator_if(node, sent_container):
            runtime.scope = gen_scope
            condition = runtime._evaluate(node.value.get('condition'))
            if condition:
                for child in node.children:
                    runtime.scope = gen_scope
                    if child.type == 'yield':
                        value = runtime._evaluate(child.value) if child.value else None
                        yield value
                    elif child.type == 'assignment' and _is_yield_assignment(child):
                        yield_node = child.value.get('value')
                        if yield_node and yield_node.type in ('yield', 'yield_expr'):
                            yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                            yield yield_val
                            target = child.value.get('target')
                            if target:
                                gen_scope.set(target, sent_container['value'])
                    else:
                        try:
                            runtime._execute_node(child)
                        except CSSLYield as y:
                            yield y.value
                        except CSSLReturn:
                            return
            else:
                else_branch = node.value.get('else_branch')
                if else_branch:
                    branches = else_branch if isinstance(else_branch, list) else [else_branch]
                    for child in branches:
                        runtime.scope = gen_scope
                        if hasattr(child, 'type') and child.type == 'yield':
                            value = runtime._evaluate(child.value) if child.value else None
                            yield value
                        elif hasattr(child, 'type') and child.type == 'assignment' and _is_yield_assignment(child):
                            yield_node = child.value.get('value')
                            if yield_node and yield_node.type in ('yield', 'yield_expr'):
                                yield_val = runtime._evaluate(yield_node.value) if yield_node.value else None
                                yield yield_val
                                target_name = _get_target_name(child.value.get('target'))
                                if target_name:
                                    gen_scope.set(target_name, sent_container['value'])
                        elif hasattr(child, 'type'):
                            try:
                                runtime._execute_node(child)
                            except CSSLYield as y:
                                yield y.value
                            except CSSLReturn:
                                return

        return CSSLGenerator(func_name, cssl_generator_func())

    def _overwrite_target(self, ref_class: str, ref_member: str, replacement_node: ASTNode):
        """Overwrite a class method or function with the replacement.

        Handles:
        - &ClassName::method - Overwrite method in CSSL class
        - &$PyObject.method - Overwrite method in Python shared object
        - &functionName - Overwrite standalone function

        v4.2.6: In namespace mode (_payload_namespace_mode), track replacements
        instead of applying globally. The namespace handler will scope them.

        v4.5.1: Respects 'private' modifier - private functions/methods cannot be overwritten.
        """
        from ..cssl_bridge import _live_objects, SharedObjectProxy

        # v4.5.1: Check if target has 'private' modifier - prevent overwrite
        if not ref_class.startswith('$'):
            target_func = self.scope.get(ref_class) or self.global_scope.get(ref_class)
            if target_func is not None:
                # Check for function with private modifier
                if hasattr(target_func, 'value') and isinstance(target_func.value, dict):
                    modifiers = target_func.value.get('modifiers', [])
                    if 'private' in modifiers:
                        raise CSSLRuntimeError(
                            f"Cannot overwrite private function '{ref_class}' - "
                            f"private functions are protected from embedded replacements"
                        )
                # Check for class with private method
                if ref_member and isinstance(target_func, CSSLClass):
                    method = target_func.methods.get(ref_member) if hasattr(target_func, 'methods') else None
                    if method and hasattr(method, 'value') and isinstance(method.value, dict):
                        modifiers = method.value.get('modifiers', [])
                        if 'private' in modifiers:
                            raise CSSLRuntimeError(
                                f"Cannot overwrite private method '{ref_class}::{ref_member}' - "
                                f"private methods are protected from embedded replacements"
                            )

        # v4.2.6: Check for namespace mode
        namespace_mode = getattr(self, '_payload_namespace_mode', None)
        if namespace_mode and ref_member is None and not ref_class.startswith('$'):
            # Standalone function replacement in namespace mode
            # Track it for the namespace handler
            if not hasattr(self, '_namespace_replacements'):
                self._namespace_replacements = {}
            self._namespace_replacements[ref_class] = replacement_node
            # Still register the function normally (namespace handler will move it)
            self.scope.set(ref_class, replacement_node)
            self.global_scope.set(ref_class, replacement_node)
            return

        # Handle Python shared objects
        if ref_class.startswith('$'):
            var_name = ref_class[1:]
            ref_obj = _live_objects.get(var_name)
            if ref_obj is None:
                ref_obj = self.scope.get(var_name) or self.global_scope.get(var_name)

            if ref_obj is None:
                return

            # Unwrap SharedObjectProxy
            if isinstance(ref_obj, SharedObjectProxy):
                ref_obj = ref_obj._obj

            # Overwrite Python object method
            if ref_member and hasattr(ref_obj, ref_member):
                # v4.3.0: Create wrapper that passes Python object as 'this' context
                wrapper = self._create_python_method_wrapper(replacement_node, ref_obj)
                try:
                    setattr(ref_obj, ref_member, wrapper)
                except (AttributeError, TypeError):
                    pass  # Can't overwrite (immutable or builtin)
            return

        # Handle CSSL class method overwrite
        target_class = self.scope.get(ref_class) or self.global_scope.get(ref_class)

        # v4.9.2: Handle &builtinName syntax (stored as __builtins__::builtinName)
        if ref_class == '__builtins__' and ref_member:
            # Treat as standalone builtin function overwrite
            ref_class = ref_member
            ref_member = None
            target_class = self.scope.get(ref_class) or self.global_scope.get(ref_class)

        # v4.2.3: Handle standalone function reference (&functionName) including builtins
        if ref_member is None:
            # Check if this is a builtin function
            is_builtin = hasattr(self, 'builtins') and self.builtins.has_function(ref_class)

            # Check if target_class is NOT a CSSLClass (it's either a function/builtin or None)
            is_cssl_class = isinstance(target_class, CSSLClass)
            # v4.2.5: Also check if target is a CSSL function (ASTNode with type 'function')
            is_cssl_function = (hasattr(target_class, 'type') and target_class.type == 'function')

            if is_builtin or (target_class is None) or (not is_cssl_class and callable(target_class)) or is_cssl_function:
                # v4.2.3: CRITICAL - Store original BEFORE overwriting for %name captures
                # This ensures %exit() refers to the ORIGINAL exit, not the replacement
                if ref_class not in self._original_functions:
                    if is_builtin:
                        # Store the original builtin from _functions dict
                        # (handles aliases like printl -> builtin_println)
                        original_builtin = self.builtins._functions.get(ref_class)
                        if original_builtin is not None:
                            self._original_functions[ref_class] = original_builtin
                    elif is_cssl_function:
                        # v4.2.5: Store original CSSL function (ASTNode)
                        self._original_functions[ref_class] = target_class
                    elif target_class is not None and callable(target_class):
                        # Store the original function/callable
                        self._original_functions[ref_class] = target_class

                # &functionName - overwrite the function/builtin
                self.scope.set(ref_class, replacement_node)
                self.global_scope.set(ref_class, replacement_node)

                # Also overwrite in builtins dict if it's a builtin
                if is_builtin:
                    # Create wrapper that calls CSSL function instead of builtin
                    def make_wrapper(node, runtime):
                        def wrapper(*args, **kwargs):
                            return runtime._call_function(node, list(args), kwargs)
                        return wrapper
                    self.builtins._functions[ref_class] = make_wrapper(replacement_node, self)
                return

        if target_class is None:
            return

        if isinstance(target_class, CSSLClass) and ref_member:
            # Overwrite method in the class
            if hasattr(target_class, 'methods') and isinstance(target_class.methods, dict):
                target_class.methods[ref_member] = replacement_node
            # Also check members list
            if hasattr(target_class, 'members'):
                for i, member in enumerate(target_class.members):
                    if member.type in ('function', 'FUNCTION') and member.value.get('name') == ref_member:
                        target_class.members[i] = replacement_node
                        break

    def _append_to_target(self, ref_class: str, ref_member: str, append_node: ASTNode):
        """Append new code to an existing class method or function.

        Creates a wrapper that runs original first, then the appended code.
        Handles:
        - &ClassName::method ++ - Append to method in CSSL class
        - &$PyObject.method ++ - Append to method in Python shared object
        - &functionName ++ - Append to standalone function

        v4.5.1: Respects 'private' modifier - private functions/methods cannot be appended to.
        """
        from ..cssl_bridge import _live_objects, SharedObjectProxy

        # v4.5.1: Check if target has 'private' modifier - prevent append
        if not ref_class.startswith('$'):
            target_func = self.scope.get(ref_class) or self.global_scope.get(ref_class)
            if target_func is not None:
                # Check for function with private modifier
                if hasattr(target_func, 'value') and isinstance(target_func.value, dict):
                    modifiers = target_func.value.get('modifiers', [])
                    if 'private' in modifiers:
                        raise CSSLRuntimeError(
                            f"Cannot append to private function '{ref_class}' - "
                            f"private functions are protected from embedded modifications"
                        )
                # Check for class with private method
                if ref_member and isinstance(target_func, CSSLClass):
                    method = target_func.methods.get(ref_member) if hasattr(target_func, 'methods') else None
                    if method and hasattr(method, 'value') and isinstance(method.value, dict):
                        modifiers = method.value.get('modifiers', [])
                        if 'private' in modifiers:
                            raise CSSLRuntimeError(
                                f"Cannot append to private method '{ref_class}::{ref_member}' - "
                                f"private methods are protected from embedded modifications"
                            )

        # Handle Python shared objects
        if ref_class.startswith('$'):
            var_name = ref_class[1:]
            ref_obj = _live_objects.get(var_name)
            if ref_obj is None:
                ref_obj = self.scope.get(var_name) or self.global_scope.get(var_name)

            if ref_obj is None:
                return

            if isinstance(ref_obj, SharedObjectProxy):
                ref_obj = ref_obj._obj

            # Create wrapper that calls original + new
            if ref_member and hasattr(ref_obj, ref_member):
                original_method = getattr(ref_obj, ref_member)
                runtime = self
                # Store the original method before wrapping
                _saved_original = original_method
                def appended_wrapper(*args, **kwargs):
                    # Run original first (use saved reference to avoid recursion)
                    result = None
                    if callable(_saved_original):
                        try:
                            result = _saved_original(*args, **kwargs)
                        except Exception:
                            pass  # Continue to appended code even if original fails
                    # Then run appended code - disable append_mode to prevent recursion
                    append_node.value['append_mode'] = False
                    try:
                        return runtime._call_function(append_node, list(args), kwargs)
                    finally:
                        append_node.value['append_mode'] = True
                try:
                    setattr(ref_obj, ref_member, appended_wrapper)
                except (AttributeError, TypeError):
                    pass
            return

        # Handle CSSL class method append
        target_class = self.scope.get(ref_class) or self.global_scope.get(ref_class)

        # v4.9.2: Handle &builtinName ++ syntax (stored as __builtins__::builtinName)
        is_builtin_hook = False
        if ref_class == '__builtins__' and ref_member:
            # Treat as standalone builtin function append
            ref_class = ref_member
            ref_member = None
            is_builtin_hook = True
            # For builtin hooks, force standalone path (don't use target_class lookup)
            target_class = None
        # v4.9.2: Also check if ref_class is a direct builtin name (not via __builtins__)
        # This handles cases like &address ++ where address is a builtin
        elif ref_member is None and hasattr(self, 'builtins') and self.builtins.has_function(ref_class):
            is_builtin_hook = True
            # Force standalone path for builtin hooks
            target_class = None

        if target_class is None or is_builtin_hook:
            # Standalone function append (or builtin hook)
            if ref_member is None:
                # v4.9.2: For builtin hooks, get from builtins._functions directly
                if is_builtin_hook and hasattr(self, 'builtins') and self.builtins.has_function(ref_class):
                    original_func = self.builtins._functions.get(ref_class)
                    # Store original before we overwrite
                    if original_func and ref_class not in self._original_functions:
                        self._original_functions[ref_class] = original_func
                else:
                    original_func = self.scope.get(ref_class) or self.global_scope.get(ref_class)
                    # For non-builtin, check _original_functions as fallback
                    if original_func is None:
                        if hasattr(self, '_original_functions'):
                            original_func = self._original_functions.get(ref_class)
                        if original_func is None and hasattr(self, 'builtins') and self.builtins.has_function(ref_class):
                            original_func = self.builtins._functions.get(ref_class)
                            if original_func and ref_class not in self._original_functions:
                                self._original_functions[ref_class] = original_func

                if original_func:
                    # Store original in append_node so it can run first
                    append_node.value['_original_func'] = original_func
                self.scope.set(ref_class, append_node)
                self.global_scope.set(ref_class, append_node)

                # v4.9.2: Also update builtins._functions for builtin hooks
                # For builtin hooks, DON'T store in scope - only use the wrapper in builtins._functions
                # This ensures all calls go through the wrapper which has proper re-entry protection
                if hasattr(self, 'builtins') and self.builtins.has_function(ref_class):
                    # Remove from scope so all lookups go through builtins
                    self.scope.set(ref_class, None)
                    self.global_scope.set(ref_class, None)
                    # v4.9.2: Also clear from _promoted_globals since @var=builtin stores there too
                    if ref_class in self._promoted_globals:
                        del self._promoted_globals[ref_class]

                    def make_wrapper(node, runtime, builtin_name, orig_func):
                        def wrapper(*args, **kwargs):
                            # v4.9.2: Prevent infinite recursion - if hook is already executing,
                            # call the original builtin directly instead of the hook
                            if builtin_name in runtime._hook_executing:
                                # Already in hook, call original directly
                                if callable(orig_func):
                                    return orig_func(*args, **kwargs)
                                return None
                            # Mark hook as executing
                            runtime._hook_executing.add(builtin_name)
                            try:
                                # v4.9.2: Append mode - run ORIGINAL first, capture result
                                original_result = None
                                if callable(orig_func):
                                    try:
                                        original_result = orig_func(*args, **kwargs)
                                    except Exception:
                                        pass  # Continue to hook even if original fails
                                # Store original result so hook can access it via %<name>_result or _result
                                runtime._original_functions[f'{builtin_name}_result'] = original_result
                                # Also set _result in scope for easy access inside hook
                                runtime.scope.set('_result', original_result)
                                # v4.9.2: Populate _hook_locals with args for local:: access
                                old_hook_locals = runtime._hook_locals
                                runtime._hook_locals = {'_result': original_result, '_args': args, '_kwargs': kwargs}
                                # Add numbered args (local::0, local::1, etc.)
                                for i, arg in enumerate(args):
                                    runtime._hook_locals[str(i)] = arg
                                # Run hook body with same args
                                hook_result = runtime._call_function(node, list(args), kwargs)
                                # Restore previous hook locals
                                runtime._hook_locals = old_hook_locals
                                # Clean up _result
                                runtime.scope.set('_result', None)
                                # Return original result unless hook explicitly returned something
                                if hook_result is not None:
                                    return hook_result
                                return original_result
                            finally:
                                runtime._hook_executing.discard(builtin_name)
                                # Clean up result
                                runtime._original_functions.pop(f'{builtin_name}_result', None)
                        return wrapper
                    self.builtins._functions[ref_class] = make_wrapper(append_node, self, ref_class, original_func)
                    return  # Don't store in scope for builtin hooks
            return

        if isinstance(target_class, CSSLClass) and ref_member:
            # Find original method
            original_method = None
            if hasattr(target_class, 'methods') and isinstance(target_class.methods, dict):
                original_method = target_class.methods.get(ref_member)

            if original_method is None and hasattr(target_class, 'members'):
                for member in target_class.members:
                    if member.type in ('function', 'FUNCTION') and member.value.get('name') == ref_member:
                        original_method = member
                        break

            # Store original in append_node for runtime execution
            if original_method:
                append_node.value['_original_method'] = original_method

            # Replace with append_node (which will call original first via _call_function)
            if hasattr(target_class, 'methods') and isinstance(target_class.methods, dict):
                target_class.methods[ref_member] = append_node
            if hasattr(target_class, 'members'):
                for i, member in enumerate(target_class.members):
                    if member.type in ('function', 'FUNCTION') and member.value.get('name') == ref_member:
                        target_class.members[i] = append_node
                        break

    def _overwrite_class_target(self, ref_class: str, ref_member: str, replacement_class: 'CSSLClass'):
        """Overwrite a target class with the replacement class.

        v4.2.5: Used by 'embedded class' with &target syntax.
        Handles:
        - &ClassName - Overwrite CSSL class
        - &$PyObject - Overwrite Python shared object

        v4.2.6: In namespace mode, track replacements instead of applying globally.
        """
        from ..cssl_bridge import _live_objects, SharedObjectProxy

        # v4.2.6: Check for namespace mode
        namespace_mode = getattr(self, '_payload_namespace_mode', None)
        if namespace_mode and not ref_class.startswith('$') and not ref_class.startswith('@'):
            # Class replacement in namespace mode
            # Track it for the namespace handler
            if not hasattr(self, '_namespace_replacements'):
                self._namespace_replacements = {}
            self._namespace_replacements[ref_class] = replacement_class
            # Still register the class normally (namespace handler will move it)
            self.scope.set(ref_class, replacement_class)
            self.global_scope.set(ref_class, replacement_class)
            return

        # Handle Python shared objects
        if ref_class.startswith('$'):
            var_name = ref_class[1:]
            # Replace the shared object with the new class
            _live_objects[var_name] = replacement_class
            self.scope.set(var_name, replacement_class)
            self.global_scope.set(var_name, replacement_class)
            return

        # Handle @ prefix (global reference)
        if ref_class.startswith('@'):
            var_name = ref_class[1:]
            self.global_scope.set(var_name, replacement_class)
            self._promoted_globals[var_name] = replacement_class
            return

        # Handle regular class reference
        target_class = self.scope.get(ref_class)
        if target_class is None:
            target_class = self.global_scope.get(ref_class)

        # Replace the class definition
        self.scope.set(ref_class, replacement_class)
        self.global_scope.set(ref_class, replacement_class)
        if ref_class in self._promoted_globals:
            self._promoted_globals[ref_class] = replacement_class

    def _exec_typed_declaration(self, node: ASTNode) -> Any:
        """Execute typed variable declaration: type<T> varName = value;

        Creates appropriate type instances for stack, vector, datastruct, etc.

        The * prefix indicates a non-nullable variable (can never be None/null).
        Example: vector<dynamic> *MyVector - can never contain None values.
        """
        decl = node.value
        type_name = decl.get('type')
        element_type = decl.get('element_type', 'dynamic')
        var_name = decl.get('name')
        value_node = decl.get('value')
        non_null = decl.get('non_null', False)

        # Create the appropriate type instance
        if type_name == 'stack':
            instance = Stack(element_type)
        elif type_name == 'vector':
            instance = Vector(element_type)
        elif type_name == 'datastruct':
            instance = DataStruct(element_type)
        elif type_name == 'shuffled':
            instance = Shuffled(element_type)
        elif type_name == 'iterator':
            instance = Iterator(element_type)
        elif type_name == 'combo':
            instance = Combo(element_type)
        elif type_name == 'dataspace':
            instance = DataSpace(element_type)
        elif type_name == 'openquote':
            instance = OpenQuote()
        elif type_name in ('int', 'integer'):
            instance = 0 if value_node is None else self._evaluate(value_node)
        elif type_name in ('string', 'str'):
            instance = "" if value_node is None else self._evaluate(value_node)
        elif type_name in ('float', 'double'):
            instance = 0.0 if value_node is None else self._evaluate(value_node)
        elif type_name == 'bool':
            instance = False if value_node is None else self._evaluate(value_node)
        elif type_name == 'dynamic':
            instance = None if value_node is None else self._evaluate(value_node)
        elif type_name == 'json':
            instance = {} if value_node is None else self._evaluate(value_node)
        elif type_name == 'array':
            instance = Array(element_type)
        elif type_name == 'list':
            instance = List(element_type)
        elif type_name in ('dictionary', 'dict'):
            instance = Dictionary(element_type)
        elif type_name == 'map':
            instance = Map(element_type)
        elif type_name == 'queue':
            # v4.7: Queue with optional size from element_type (queue<type, size>)
            queue_size = decl.get('size', 'dynamic')
            instance = Queue(element_type, queue_size)
        elif type_name == 'bit':
            # v4.9.0: Single bit value (0 or 1)
            from .cssl_types import Bit
            if value_node is None:
                instance = Bit(0)
            else:
                val = self._evaluate(value_node)
                if isinstance(val, Bit):
                    # Already a Bit object (e.g., from .copy())
                    instance = val
                elif isinstance(val, int) and val in (0, 1):
                    instance = Bit(val)
                else:
                    raise CSSLRuntimeError(f"Bit must be 0 or 1, got {val}", node.line)
        elif type_name == 'byte':
            # v4.9.0: Byte value (x^y notation where x=0/1, y=0-255)
            from .cssl_types import Byte
            if value_node is None:
                instance = Byte(0, 0)
            else:
                val = self._evaluate(value_node)
                if isinstance(val, Byte):
                    instance = val
                elif isinstance(val, tuple) and len(val) == 2:
                    # Tuple from byte literal parsing (base, weight)
                    instance = Byte(val[0], val[1])
                elif isinstance(val, int):
                    # Plain int - store as 1^val
                    instance = Byte(1, val % 256)
                else:
                    raise CSSLRuntimeError(f"Invalid byte value: {val}", node.line)
        elif type_name in ('address', 'ptr', 'pointer'):
            # v4.9.0: Memory address/pointer type
            # v4.9.3: Added 'ptr' and 'pointer' as aliases for 'address'
            from .cssl_types import Address
            if value_node is None:
                instance = Address()  # Null address
            else:
                val = self._evaluate(value_node)
                if isinstance(val, Address):
                    # Already an Address object
                    instance = val
                elif isinstance(val, str):
                    # Address string from memory().get("address")
                    instance = Address(val)
                else:
                    # Create address from object
                    instance = Address(obj=val)
        else:
            # Default: evaluate the value or set to None
            instance = self._evaluate(value_node) if value_node else None

        # If there's an explicit value, use it instead
        # v4.8.7: Removed 'array' from exclusion - arrays should also get init values
        # v4.8.8: Added 'instance' to exclusion - instance type already evaluates value above
        # v4.9.0: Added 'bit', 'byte', 'address' to exclusion - they already handle values above
        # v4.9.2: Added 'ptr', 'pointer' to exclusion - they already evaluate value above
        if value_node and type_name not in ('int', 'integer', 'string', 'str', 'float', 'double', 'bool', 'dynamic', 'json', 'instance', 'bit', 'byte', 'address', 'ptr', 'pointer'):
            # For container types, the value might be initialization data
            init_value = self._evaluate(value_node)
            if isinstance(init_value, (list, tuple)):
                # For non-null containers, filter out None values
                if non_null:
                    init_value = [v for v in init_value if v is not None]
                instance.extend(init_value)
            elif isinstance(init_value, dict):
                # v4.8.7: Handle dict initialization: dict d = {"key": "value"}
                if hasattr(instance, 'update'):
                    instance.update(init_value)
                elif hasattr(instance, '__setitem__'):
                    for k, v in init_value.items():
                        instance[k] = v
            elif init_value is not None:
                if hasattr(instance, 'append'):
                    instance.append(init_value)

        # Non-null enforcement: container types get wrapped to filter None on operations
        if non_null:
            # Mark the instance as non-null for runtime checks
            if hasattr(instance, '_non_null'):
                instance._non_null = True
            # Track non-null variables for assignment enforcement
            if not hasattr(self, '_non_null_vars'):
                self._non_null_vars = set()
            self._non_null_vars.add(var_name)

            # Ensure initial value is not None for non-null variables
            if instance is None:
                raise CSSLRuntimeError(
                    f"Non-null variable '*{var_name}' cannot be initialized to None",
                    node.line,
                    hint="Use a default value or remove the * prefix"
                )

        # Check for global modifier
        modifiers = decl.get('modifiers', [])
        is_global = 'global' in modifiers

        # v4.9.4: Check for local/static/freezed modifiers
        is_local = decl.get('is_local', False)
        is_static = decl.get('is_static', False)
        is_freezed = decl.get('is_freezed', False)

        # v4.9.4: Track variable metadata for local/static/freezed enforcement
        if is_local or is_static or is_freezed:
            self._var_meta[var_name] = {'is_local': is_local, 'is_static': is_static, 'is_freezed': is_freezed}

        # v4.9.2: Check for this->member declaration
        is_this_member = decl.get('is_this_member', False)

        # Store in appropriate location
        if is_this_member:
            # this->member declaration - store on current instance
            if self._current_instance is None:
                raise CSSLRuntimeError("'this' used outside of class method context", node.line)
            if hasattr(self._current_instance, 'set_member'):
                self._current_instance.set_member(var_name, instance)
            else:
                setattr(self._current_instance, var_name, instance)
        else:
            # Normal variable - store in scope
            self.scope.set(var_name, instance)

        # If global, also store in promoted_globals and global_scope
        if is_global:
            self._promoted_globals[var_name] = instance
            self.global_scope.set(var_name, instance)

        return instance

    def _exec_instance_declaration(self, node: ASTNode) -> Any:
        """Execute instance declaration: instance<"name"> varName;

        Gets or creates a universal shared instance by name.
        Universal instances are accessible from CSSL, Python, and C++.

        Usage:
            instance<"myContainer"> container;  // Creates or gets instance
            container.member = "value";         // Set member
            container +<<== { void func() {} }  // Inject methods
        """
        from .cssl_types import UniversalInstance

        decl = node.value
        instance_name = decl.get('instance_name')
        var_name = decl.get('name')
        value_node = decl.get('value')

        # Get existing or create new universal instance
        instance = UniversalInstance.get_or_create(instance_name)

        # If value is provided, set it as initial content
        if value_node:
            initial_value = self._evaluate(value_node)
            # If it's a dict, set all keys as members
            if isinstance(initial_value, dict):
                for key, val in initial_value.items():
                    instance.set_member(key, val)
            else:
                instance.set_member('value', initial_value)

        # Store in scope and global scope for access
        self.scope.set(var_name, instance)
        self.global_scope.set(f'${instance_name}', instance)

        return instance

    def _exec_super_func(self, node: ASTNode) -> Any:
        """Execute super-function for .cssl-pl payload files.

        Super-functions are pre-execution hooks that run when payload() loads a file.

        Supported super-functions:
            #$run(funcName)        - Call a function defined in the payload
            #$exec(expression)     - Execute an expression immediately
            #$printl(message)      - Print a message during load

        Example .cssl-pl file:
            void initDatabase() {
                printl("DB initialized");
            }

            #$run(initDatabase);       // Calls initDatabase when payload loads
            #$printl("Payload loaded"); // Prints during load
        """
        super_info = node.value
        super_name = super_info.get('name', '')  # e.g., "#$run", "#$exec", "#$printl"
        args = super_info.get('args', [])

        # Extract the function name part (after #$)
        if super_name.startswith('#$'):
            func_type = super_name[2:]  # "run", "exec", "printl"
        else:
            func_type = super_name

        if func_type == 'run':
            # #$run(funcName) - Call a function by name
            if args:
                func_ref = args[0]
                if isinstance(func_ref, ASTNode):
                    if func_ref.type == 'identifier':
                        func_name = func_ref.value
                    elif func_ref.type == 'call':
                        # Direct call like #$run(setup())
                        return self._eval_call(func_ref)
                    else:
                        func_name = self._evaluate(func_ref)
                else:
                    func_name = str(func_ref)

                # Look up and call the function
                func_node = self.scope.get(func_name)
                if func_node and isinstance(func_node, ASTNode) and func_node.type == 'function':
                    return self._call_function(func_node, [])
                else:
                    raise CSSLRuntimeError(f"#$run: Function '{func_name}' not found", node.line)

        elif func_type == 'exec':
            # #$exec(expression) - Execute an expression
            if args:
                return self._evaluate(args[0])

        elif func_type == 'printl':
            # #$printl(message) - Print a message
            if args:
                msg = self._evaluate(args[0])
                print(str(msg))
                self.output_buffer.append(str(msg))
                return None

        elif func_type == 'print':
            # #$print(message) - Print without newline
            if args:
                msg = self._evaluate(args[0])
                print(str(msg), end='')
                self.output_buffer.append(str(msg))
                return None

        else:
            raise CSSLRuntimeError(f"Unknown super-function: {super_name}", node.line)

        return None

    def _exec_global_assignment(self, node: ASTNode) -> Any:
        """Execute global variable assignment: global Name = value

        Stores the value in _promoted_globals so it can be accessed via @Name
        """
        inner = node.value  # The wrapped assignment/expression node

        if inner is None:
            return None

        # Handle assignment node: global Name = value
        if inner.type == 'assignment':
            target = inner.value.get('target')
            value = self._evaluate(inner.value.get('value'))

            # Get variable name from target
            if isinstance(target, ASTNode):
                if target.type == 'identifier':
                    var_name = target.value
                elif target.type == 'global_ref':
                    # r@Name = value
                    var_name = target.value
                else:
                    var_name = str(target.value) if hasattr(target, 'value') else str(target)
            elif isinstance(target, str):
                var_name = target
            else:
                var_name = str(target)

            # Store in promoted globals for @Name access
            self._promoted_globals[var_name] = value
            # Also store in global scope for regular access
            self.global_scope.set(var_name, value)
            return value

        # Handle expression that results in assignment
        elif inner.type == 'expression':
            result = self._evaluate(inner.value)
            return result

        # Handle typed declaration: global datastruct<int> data;
        elif inner.type == 'typed_declaration':
            # Add global modifier to the declaration
            if isinstance(inner.value, dict):
                inner.value['modifiers'] = inner.value.get('modifiers', []) + ['global']
            result = self._exec_typed_declaration(inner)
            return result

        # Fallback: execute normally
        return self._execute_node(inner)

    def _call_function(self, func_node: ASTNode, args: List[Any], kwargs: Dict[str, Any] = None, _is_hook_trigger: bool = False) -> Any:
        """Call a function node with arguments (positional and named)

        Args:
            func_node: The function AST node
            args: List of positional arguments
            kwargs: Dict of named arguments (param_name -> value)
            _is_hook_trigger: Internal flag - True when called as a hook trigger

        Supports:
            define func : extends otherFunc() { ... } - Inherit local vars from otherFunc
        """
        func_info = func_node.value
        params = func_info.get('params', [])
        modifiers = func_info.get('modifiers', [])
        kwargs = kwargs or {}

        # v4.9.3: If this is a generator function, return a CSSLGenerator instead of executing
        if func_info.get('_is_generator'):
            return self._create_generator(func_node, args, kwargs)

        # v4.9.0: If this is a memory hook function and it's being called directly
        # (not as a hook trigger), skip execution - it's just a hook registration
        if func_info.get('_is_memory_hook') and not _is_hook_trigger:
            return None  # Silent no-op for direct calls to hook functions

        # v4.9.0: Execute memory-hooked functions first
        # Functions with ': uses memory(address)' are executed when their host is called
        if hasattr(self, '_memory_hooks'):
            # Look up by function name (how hooks are stored)
            func_name = func_info.get('name', '')
            if func_name in self._memory_hooks:
                for hooked_item in self._memory_hooks[func_name]:
                    try:
                        # hooked_item can be ASTNode or ('class', ASTNode) tuple
                        if isinstance(hooked_item, tuple) and hooked_item[0] == 'class':
                            # Class hook - instantiate the class
                            pass  # Class instantiation happens separately
                        elif isinstance(hooked_item, ASTNode) and hooked_item.type == 'function':
                            # Call with _is_hook_trigger=True so hook body executes
                            self._call_function(hooked_item, args, kwargs, _is_hook_trigger=True)
                    except Exception:
                        pass  # Continue with host even if hook fails

        # v4.2.5: Deferred &target replacement for non-embedded functions
        # If function has &target and hasn't been applied yet, apply now on first call
        append_ref_class = func_info.get('append_ref_class')
        if append_ref_class and not func_info.get('_target_applied', False):
            append_mode = func_info.get('append_mode', False)
            append_ref_member = func_info.get('append_ref_member')
            if append_mode:
                self._append_to_target(append_ref_class, append_ref_member, func_node)
            else:
                self._overwrite_target(append_ref_class, append_ref_member, func_node)
            func_node.value['_target_applied'] = True

        # Check for undefined modifier - suppress errors if present
        is_undefined = 'undefined' in modifiers

        # Create new scope
        new_scope = Scope(parent=self.scope)

        # Handle function extends - inherit local vars from extended function
        extends_resolved = func_info.get('_extends_resolved')
        if extends_resolved:
            if callable(extends_resolved):
                # Python function - call it first to populate any state
                try:
                    extends_resolved(*args, **kwargs)
                except Exception:
                    pass  # Extended function failed - continue anyway
            elif hasattr(extends_resolved, 'value'):
                # CSSL function - execute it in a temporary scope to get local vars
                old_scope = self.scope
                temp_scope = Scope(parent=self.scope)
                self.scope = temp_scope
                try:
                    # Execute extended function body to populate local vars
                    for child in extends_resolved.children:
                        if not self._running:
                            break
                        self._execute_node(child)
                except CSSLReturn:
                    # Parent returned - that's fine, we just want the local vars
                    pass
                except Exception:
                    pass  # Extended function failed - still copy local vars
                finally:
                    # ALWAYS copy local vars (even if parent returned)
                    for name, value in temp_scope.variables.items():
                        new_scope.set(name, value)
                    self.scope = old_scope

        # Bind parameters - handle both positional and named arguments
        for i, param in enumerate(params):
            # Extract param name, type, and default from dict format: {'name': 'a', 'type': 'int', 'default': ...}
            if isinstance(param, dict):
                param_name = param['name']
                param_type = param.get('type', '')
                param_default = param.get('default')  # v4.2.0: Default value AST node
            else:
                param_name = param
                param_type = ''
                param_default = None

            # Check if this is an 'open' parameter - receives all args as a list
            # The parser sets param['open'] = True for 'open' keyword
            is_open_param = (isinstance(param, dict) and param.get('open', False)) or param_name == 'Params'
            if is_open_param:
                # 'open Params' receives all arguments as a list
                # Check for non_null flag: open *Params filters out None values
                is_non_null = isinstance(param, dict) and param.get('non_null', False)
                args_list = list(args)
                if is_non_null:
                    args_list = [a for a in args_list if a is not None]
                    # Also filter kwargs
                    kwargs = {k: v for k, v in kwargs.items() if v is not None}
                new_scope.set(param_name, args_list)
                new_scope.set('Params', args_list)  # Also set 'Params' for OpenFind
                new_scope.set('_OpenKwargs', kwargs)  # Store kwargs for OpenFind<type, "name">
            elif param_name in kwargs:
                # Named argument takes priority
                new_scope.set(param_name, kwargs[param_name])
            elif i < len(args):
                # Positional argument
                new_scope.set(param_name, args[i])
            elif param_default is not None:
                # v4.2.0: Use default value if no argument provided
                default_value = self._evaluate(param_default)
                new_scope.set(param_name, default_value)
            else:
                new_scope.set(param_name, None)

        # Execute body
        old_scope = self.scope
        self.scope = new_scope

        try:
            # Handle append mode (++) - execute referenced function first
            # v4.9.2: Skip for builtin hooks - the wrapper handles original execution
            append_mode = func_info.get('append_mode', False)
            append_ref_class = func_info.get('append_ref_class')
            append_ref_member = func_info.get('append_ref_member')

            # v4.9.2: Don't execute original for builtin hooks - wrapper already does that
            is_builtin_hook = append_ref_class == '__builtins__'
            if append_mode and append_ref_class and not is_builtin_hook:
                self._execute_append_reference(
                    None, append_ref_class, append_ref_member,
                    args, kwargs, {}, is_constructor=False
                )

            # v4.7: Handle bytearrayed function modifier
            if 'bytearrayed' in modifiers:
                return self._execute_bytearrayed_function(func_node)

            # v4.2.0: Handle raw_body with supports_language (multi-language support)
            raw_body = func_info.get('raw_body')
            supports_language = func_info.get('supports_language')

            if raw_body and supports_language:
                # Transform and parse the raw body from the target language
                body_children = self._transform_and_parse_function_body(raw_body, supports_language)
                # v4.9.4: undefined/super modifiers - catch errors per-statement and continue
                is_error_tolerant = is_undefined or 'super' in modifiers
                for child in body_children:
                    if not self._running:
                        break
                    if is_error_tolerant:
                        try:
                            self._execute_node(child)
                        except CSSLReturn:
                            raise  # Let return statements through
                        except Exception:
                            pass  # Swallow error and continue to next statement
                    else:
                        self._execute_node(child)
            else:
                # Normal CSSL function body
                # v4.9.4: undefined/super modifiers - catch errors per-statement and continue
                is_error_tolerant = is_undefined or 'super' in modifiers
                for child in func_node.children:
                    # Check if exit() was called
                    if not self._running:
                        break
                    if is_error_tolerant:
                        try:
                            self._execute_node(child)
                        except CSSLReturn:
                            raise  # Let return statements through
                        except Exception:
                            pass  # Swallow error and continue to next statement
                    else:
                        self._execute_node(child)
        except CSSLReturn as ret:
            return_value = ret.value

            # Check exclude_type: *[type] - must NOT return excluded type
            exclude_type = func_info.get('exclude_type')
            if exclude_type and isinstance(exclude_type, str):
                type_map = {
                    'string': str, 'int': int, 'float': float, 'bool': bool,
                    'null': type(None), 'none': type(None),
                    'list': list, 'array': list, 'dict': dict, 'json': dict,
                }
                excluded_py_type = type_map.get(exclude_type.lower())
                # For shuffled returns (tuples), check each element
                if isinstance(return_value, tuple):
                    for val in return_value:
                        if excluded_py_type and isinstance(val, excluded_py_type):
                            raise CSSLRuntimeError(f"Type exclusion: function must NOT return '{exclude_type}' values")
                elif excluded_py_type and isinstance(return_value, excluded_py_type):
                    raise CSSLRuntimeError(f"Type exclusion: function must NOT return '{exclude_type}'")

            # Enforce return type for typed functions (like C++)
            # Typed functions MUST return the declared type
            # Exception: 'meta' modifier allows any return type
            enforce_return_type = func_info.get('enforce_return_type', False)
            return_type = func_info.get('return_type')

            if enforce_return_type and return_type and return_type != 'void':
                # Type mapping from CSSL types to Python types
                type_validate_map = {
                    'string': str, 'int': int, 'float': (int, float), 'bool': bool,
                    'list': list, 'array': list, 'dict': dict, 'json': dict,
                    'dynamic': object,  # Any type
                    'void': type(None),
                }

                # Generic container types - accept lists/tuples
                container_types = {
                    'vector', 'stack', 'datastruct', 'dataspace',
                    'shuffled', 'iterator', 'combo', 'openquote', 'map'
                }

                if return_type in container_types:
                    # Container types accept list, tuple, dict depending on type
                    if return_type == 'map':
                        expected = dict
                    elif return_type == 'shuffled':
                        expected = (list, tuple)
                    else:
                        expected = (list, tuple, object)

                    if not isinstance(return_value, expected):
                        func_name = func_info.get('name', 'unknown')
                        actual_type = type(return_value).__name__
                        raise CSSLRuntimeError(
                            f"Type error in '{func_name}': declared return type '{return_type}' "
                            f"but returned '{actual_type}'. Typed functions must return declared type."
                        )
                elif return_type in type_validate_map:
                    expected = type_validate_map[return_type]
                    if expected != object and return_value is not None:
                        if not isinstance(return_value, expected):
                            func_name = func_info.get('name', 'unknown')
                            actual_type = type(return_value).__name__
                            raise CSSLRuntimeError(
                                f"Type error in '{func_name}': declared return type '{return_type}' "
                                f"but returned '{actual_type}'. Typed functions must return declared type."
                            )

            # Check non_null: function must return a value (not None)
            non_null = func_info.get('non_null', False)
            if non_null and return_value is None:
                func_name = func_info.get('name', 'unknown')
                raise CSSLRuntimeError(f"Non-null function '{func_name}' returned null/None")

            return return_value
        except Exception as e:
            # If undefined modifier, suppress all errors
            if is_undefined:
                return None
            raise
        finally:
            self.scope = old_scope

        return None

    def _exec_if(self, node: ASTNode) -> Any:
        """Execute if statement"""
        condition = self._evaluate(node.value.get('condition'))

        if condition:
            for child in node.children:
                if child.type == 'then':
                    for stmt in child.children:
                        self._execute_node(stmt)
                    return None

        # Execute else block
        for child in node.children:
            if child.type == 'else':
                for stmt in child.children:
                    self._execute_node(stmt)
                return None

        return None

    def _exec_while(self, node: ASTNode) -> Any:
        """Execute while loop"""
        while self._running and self._evaluate(node.value.get('condition')):
            try:
                for child in node.children:
                    if not self._running:
                        break
                    self._execute_node(child)
            except CSSLBreak:
                break
            except CSSLContinue:
                continue

        return None

    def _exec_for(self, node: ASTNode) -> Any:
        """Execute Python-style for loop: for (i in range(start, end, step)) { }"""
        var_name = node.value.get('var')
        start = int(self._evaluate(node.value.get('start')))
        end = int(self._evaluate(node.value.get('end')))

        # Optional step parameter (default is 1)
        step_node = node.value.get('step')
        step = int(self._evaluate(step_node)) if step_node else 1

        for i in range(start, end, step):
            if not self._running:
                break
            self.scope.set(var_name, i)
            try:
                for child in node.children:
                    if not self._running:
                        break
                    self._execute_node(child)
            except CSSLBreak:
                break
            except CSSLContinue:
                continue

        return None

    def _exec_c_for(self, node: ASTNode) -> Any:
        """Execute C-style for loop: for (init; condition; update) { }

        Supports:
        - for (int i = 0; i < n; i++) { }
        - for (int i = 0; i < n; i = i + 1) { }
        - for (i = 0; i < n; i += 1) { }
        - for (; condition; ) { }  (infinite loop with condition)
        """
        init = node.value.get('init')
        condition = node.value.get('condition')
        update = node.value.get('update')

        # Execute init statement
        if init:
            var_name = init.value.get('var')
            init_value = self._evaluate(init.value.get('value'))
            self.scope.set(var_name, init_value)
        else:
            var_name = None

        # Main loop
        while self._running:
            # Check condition
            if condition:
                cond_result = self._evaluate(condition)
                if not cond_result:
                    break
            # If no condition, this would be infinite - we still need a way to break

            # Execute body
            try:
                for child in node.children:
                    if not self._running:
                        break
                    self._execute_node(child)
            except CSSLBreak:
                break
            except CSSLContinue:
                pass  # Continue to update, then next iteration

            # Execute update
            if update:
                self._exec_c_for_update(update)

        return None

    def _exec_c_for_update(self, update: 'ASTNode') -> None:
        """Execute the update part of a C-style for loop."""
        var_name = update.value.get('var')
        op = update.value.get('op')
        value_node = update.value.get('value')

        current = self.scope.get(var_name) or 0

        if op == 'increment':
            self.scope.set(var_name, current + 1)
        elif op == 'decrement':
            self.scope.set(var_name, current - 1)
        elif op == 'add':
            add_value = self._evaluate(value_node)
            self.scope.set(var_name, current + add_value)
        elif op == 'subtract':
            sub_value = self._evaluate(value_node)
            self.scope.set(var_name, current - sub_value)
        elif op == 'assign':
            new_value = self._evaluate(value_node)
            self.scope.set(var_name, new_value)

    def _exec_foreach(self, node: ASTNode) -> Any:
        """Execute foreach loop"""
        var_name = node.value.get('var')
        iterable = self._evaluate(node.value.get('iterable'))

        if iterable is None:
            return None

        for item in iterable:
            if not self._running:
                break
            self.scope.set(var_name, item)
            try:
                for child in node.children:
                    if not self._running:
                        break
                    self._execute_node(child)
            except CSSLBreak:
                break
            except CSSLContinue:
                continue

        return None

    def _exec_switch(self, node: ASTNode) -> Any:
        """Execute switch statement"""
        value = self._evaluate(node.value.get('value'))
        matched = False

        for child in node.children:
            if child.type == 'case':
                case_value = self._evaluate(child.value.get('value'))
                if value == case_value:
                    matched = True
                    try:
                        for stmt in child.children:
                            self._execute_node(stmt)
                    except CSSLBreak:
                        return None
            elif child.type == 'default' and not matched:
                try:
                    for stmt in child.children:
                        self._execute_node(stmt)
                except CSSLBreak:
                    return None

        return None

    def _exec_param_switch(self, node: ASTNode) -> Any:
        """Execute param switch statement for open parameters.

        v4.2.5: Switch on which parameters were provided.

        Syntax:
            switch(Params) {
                case name:              // if 'name' param exists
                case name & age:        // if both exist
                case name & not age:    // if 'name' exists but 'age' doesn't
                except name:            // if 'name' does NOT exist
                default:                // fallback
                always:                 // always runs after match
                finally:                // cleanup, always runs
            }
        """
        params_name = node.value.get('params')
        # v4.3.2: Use the actual variable from switch(Variable), not just _OpenKwargs
        # This allows switch(Input) where Input is the open parameter
        if params_name == 'Params':
            open_kwargs = self.scope.get('_OpenKwargs') or {}
        else:
            # Try to get kwargs from the named variable
            open_kwargs = self.scope.get(params_name)
            if open_kwargs is None:
                open_kwargs = self.scope.get('_OpenKwargs') or {}
            elif not isinstance(open_kwargs, dict):
                # If it's not a dict, try _OpenKwargs as fallback
                open_kwargs = self.scope.get('_OpenKwargs') or {}

        matched = False
        always_node = None
        finally_node = None
        default_node = None

        # First pass: find always, finally, default nodes
        for child in node.children:
            if child.type == 'param_always':
                always_node = child
            elif child.type == 'param_finally':
                finally_node = child
            elif child.type == 'param_default':
                default_node = child

        try:
            # Execute matching cases
            for child in node.children:
                if child.type == 'param_case':
                    condition = child.value.get('condition')
                    if self._eval_param_condition(condition, open_kwargs):
                        matched = True
                        try:
                            for stmt in child.children:
                                self._execute_node(stmt)
                        except CSSLBreak:
                            break

            # Execute default if no match
            if not matched and default_node:
                try:
                    for stmt in default_node.children:
                        self._execute_node(stmt)
                except CSSLBreak:
                    pass

            # Execute always block (runs after a match, before finally)
            if matched and always_node:
                try:
                    for stmt in always_node.children:
                        self._execute_node(stmt)
                except CSSLBreak:
                    pass

        finally:
            # Execute finally block (always runs, even on break/exception)
            if finally_node:
                for stmt in finally_node.children:
                    self._execute_node(stmt)

        return None

    def _eval_param_condition(self, condition: dict, kwargs: dict) -> bool:
        """Evaluate a param switch condition.

        Condition types:
            {'type': 'exists', 'param': 'name'}  -> 'name' in kwargs OR variable 'name' is truthy
            {'type': 'not', 'param': 'name'}     -> 'name' not in kwargs AND variable 'name' is falsy
            {'type': 'and', 'left': {...}, 'right': {...}} -> left AND right
            {'type': 'or', 'left': {...}, 'right': {...}}  -> left OR right

        v4.3.2: Added 'or' type for || operator support.
        v4.3.2: Enhanced to check both kwargs AND scope variables (from OpenFind).
                This allows positional args found via OpenFind<type>(index) to work
                with param_switch conditions like 'case text & !error:'.
        """
        cond_type = condition.get('type')

        if cond_type == 'exists':
            param = condition.get('param')
            # Check kwargs first
            if param in kwargs:
                return True
            # Also check if a variable with this name exists in scope and is truthy
            # This allows OpenFind results to work with param_switch
            var_value = self.scope.get(param)
            if var_value is not None and var_value != '' and var_value != 0 and var_value != False:
                # Make sure it's not a builtin function
                if not callable(var_value):
                    return True
            return False

        elif cond_type == 'not':
            param = condition.get('param')
            # Check kwargs first
            if param in kwargs:
                return False
            # Also check if variable is truthy (then it's "provided")
            var_value = self.scope.get(param)
            if var_value is not None and var_value != '' and var_value != 0 and var_value != False:
                if not callable(var_value):
                    return False  # Variable has value, so it IS provided
            return True  # Not in kwargs and variable is null/empty

        elif cond_type == 'and':
            left = self._eval_param_condition(condition.get('left'), kwargs)
            right = self._eval_param_condition(condition.get('right'), kwargs)
            return left and right

        elif cond_type == 'or':
            left = self._eval_param_condition(condition.get('left'), kwargs)
            right = self._eval_param_condition(condition.get('right'), kwargs)
            return left or right

        return False

    def _exec_return(self, node: ASTNode) -> Any:
        """Execute return statement.

        Supports multiple return values for shuffled functions:
            return a, b, c;  // Returns tuple (a, b, c)
        """
        if node.value is None:
            raise CSSLReturn(None)

        # Check if this is a multiple return value
        if isinstance(node.value, dict) and node.value.get('multiple'):
            values = [self._evaluate(v) for v in node.value.get('values', [])]
            raise CSSLReturn(tuple(values))

        value = self._evaluate(node.value)
        raise CSSLReturn(value)

    def _exec_yield(self, node: ASTNode) -> Any:
        """Execute yield statement - v4.9.3

        Yields a value from a generator function, pausing execution.
        The function resumes from here when next() is called on the generator.

        Syntax:
            yield value;     // Yield a value and pause
            yield;           // Yield None and pause

        Example:
            generator<int> define Range(int n) {
                int i = 0;
                while (i < n) {
                    yield i;
                    i = i + 1;
                }
            }
        """
        if node.value is None:
            raise CSSLYield(None)

        value = self._evaluate(node.value)
        raise CSSLYield(value)

    def _exec_await(self, node: ASTNode) -> Any:
        """Execute await expression - v4.9.3

        Awaits a Future or async function result, blocking until complete.

        Syntax:
            await future;              // Wait for future to complete
            await asyncFunc();         // Wait for async function
            result = await future;     // Capture result

        Example:
            async define FetchData() {
                return http::get("url");
            }
            data = await FetchData();
        """
        value = self._evaluate(node.value)

        # If it's a CSSLFuture, wait for it
        if isinstance(value, CSSLFuture):
            # Block until the future completes
            import time
            while value.state in (CSSLFuture.PENDING, CSSLFuture.RUNNING):
                time.sleep(0.001)  # Small sleep to avoid busy-waiting
            if value.state == CSSLFuture.FAILED:
                raise CSSLRuntimeError(f"Awaited future failed: {value._exception}")
            if value.state == CSSLFuture.CANCELLED:
                raise CSSLRuntimeError("Awaited future was cancelled")
            return value.result()

        # If it's an async function wrapper, execute it
        if isinstance(value, CSSLAsyncFunction):
            future = value.start()
            # Wait for completion
            import time
            while future.state in (CSSLFuture.PENDING, CSSLFuture.RUNNING):
                time.sleep(0.001)
            if future.state == CSSLFuture.FAILED:
                raise CSSLRuntimeError(f"Async function failed: {future._exception}")
            return future.result()

        # If it's a generator, exhaust it and return last value
        if isinstance(value, CSSLGenerator):
            result = None
            while value.has_next():
                result = value.next()
            return result

        # For regular values, just return them
        return value

    def _exec_break(self, node: ASTNode) -> Any:
        """Execute break statement"""
        raise CSSLBreak()

    def _exec_continue(self, node: ASTNode) -> Any:
        """Execute continue statement"""
        raise CSSLContinue()

    def _exec_throw(self, node: ASTNode) -> Any:
        """Execute throw statement - v4.5.1

        Throws a CSSLThrow exception that propagates to the nearest catch block.

        Syntax:
            throw "Error message";
            throw errorVar;
            throw;  // re-throw current exception
        """
        if node.value is None:
            # throw; - re-throw current exception (should be in a catch block)
            raise CSSLThrow("Re-thrown exception")

        message = self._evaluate(node.value)
        raise CSSLThrow(message)

    def _exec_raise(self, node: ASTNode) -> Any:
        """Execute raise statement - v4.8 (Python-style exceptions)

        Raises a Python-style exception that propagates to the nearest catch block.

        Syntax:
            raise;                          # Re-raise current exception
            raise "Error message";          # Simple error message
            raise ValueError("message");    # Python exception type
            raise CustomError("msg", 123);  # Custom exception with args
        """
        value = node.value

        # Handle re-raise (raise;)
        if value is None or (isinstance(value, dict) and value.get('type') is None):
            raise CSSLThrow("Re-raised exception")

        # Map of Python exception types
        EXCEPTION_MAP = {
            'ValueError': ValueError,
            'TypeError': TypeError,
            'KeyError': KeyError,
            'IndexError': IndexError,
            'AttributeError': AttributeError,
            'RuntimeError': RuntimeError,
            'IOError': IOError,
            'OSError': OSError,
            'FileNotFoundError': FileNotFoundError,
            'NameError': NameError,
            'ZeroDivisionError': ZeroDivisionError,
            'OverflowError': OverflowError,
            'StopIteration': StopIteration,
            'AssertionError': AssertionError,
            'NotImplementedError': NotImplementedError,
            'PermissionError': PermissionError,
            'TimeoutError': TimeoutError,
            'ConnectionError': ConnectionError,
            'ImportError': ImportError,
            'ModuleNotFoundError': ModuleNotFoundError,
            'RecursionError': RecursionError,
            # Generic fallback
            'Error': Exception,
            'Exception': Exception,
        }

        if isinstance(value, dict):
            exc_type_name = value.get('type', 'Error')
            args = value.get('args', [])
            message = value.get('message')

            # Evaluate args if present
            if args:
                evaluated_args = [self._evaluate(arg) for arg in args]
                message_str = evaluated_args[0] if evaluated_args else "Error"
            elif message:
                message_str = self._evaluate(message)
            else:
                message_str = f"{exc_type_name}: Unknown error"

            # Get the exception class
            exc_class = EXCEPTION_MAP.get(exc_type_name, Exception)

            # Raise the Python exception
            # Wrap in CSSLThrow so it can be caught by CSSL try/catch
            raise CSSLThrow(f"{exc_type_name}: {message_str}", exc_class(message_str))
        else:
            # Simple message
            message = self._evaluate(value)
            raise CSSLThrow(str(message))

    def _exec_constructor(self, node: ASTNode) -> Any:
        """Execute constructor node - only called when encountered directly.

        Normally constructors are executed through _call_constructor in _eval_new.
        This handles cases where a constructor node is executed in other contexts.
        """
        # Constructor nodes should be handled during class instantiation
        # If we reach here, it's in a context where the constructor is stored but not executed
        return None

    def _exec_super_call(self, node: ASTNode) -> Any:
        """Execute super() call to invoke parent constructor or method.

        Syntax:
            super()              - Call parent constructor with no args
            super(arg1, arg2)    - Call parent constructor with args
            super::method()      - Call specific parent method
            super::method(args)  - Call specific parent method with args
        """
        if self._current_instance is None:
            raise CSSLRuntimeError(
                "super() called outside of class context",
                node.line if hasattr(node, 'line') else 0,
                hint="super() can only be used inside class constructors and methods"
            )

        instance = self._current_instance

        # Try to get parent from instance first, then from class definition
        parent = getattr(instance, '_parent_class', None)
        if parent is None and hasattr(instance, '_class') and instance._class:
            parent = getattr(instance._class, 'parent', None)

        if parent is None:
            raise CSSLRuntimeError(
                "super() called but class has no parent",
                node.line if hasattr(node, 'line') else 0,
                hint="super() requires the class to extend another class"
            )

        method_name = node.value.get('method')
        args = [self._evaluate(arg) for arg in node.value.get('args', [])]

        from .cssl_builtins import CSSLizedPythonObject

        if method_name:
            # super::method() - call specific parent method
            if isinstance(parent, CSSLClass):
                method = parent.methods.get(method_name)
                if method:
                    return self._call_method(instance, method, args, {})
                else:
                    raise CSSLRuntimeError(
                        f"Parent class has no method '{method_name}'",
                        node.line if hasattr(node, 'line') else 0
                    )
            elif isinstance(parent, CSSLizedPythonObject):
                py_obj = parent.get_python_obj()
                if hasattr(py_obj, method_name):
                    method = getattr(py_obj, method_name)
                    return method(*args)
                else:
                    raise CSSLRuntimeError(
                        f"Parent Python object has no method '{method_name}'",
                        node.line if hasattr(node, 'line') else 0
                    )
            elif hasattr(parent, method_name):
                method = getattr(parent, method_name)
                return method(*args)
        else:
            # super() - call parent constructor
            self._call_parent_constructor(instance, args)
            instance._parent_constructor_called = True

        return None

    def _exec_try(self, node: ASTNode) -> Any:
        """Execute try/catch/finally block"""
        try:
            for child in node.children:
                if child.type == 'try-block':
                    for stmt in child.children:
                        self._execute_node(stmt)
        except CSSLThrow as e:
            # v4.5.1: Handle user-thrown exceptions from throw statement
            for child in node.children:
                if child.type == 'catch-block':
                    error_var = child.value.get('error_var') if child.value else None
                    if error_var:
                        # Store the thrown message in the error variable
                        self.scope.set(error_var, e.message if e.message else str(e))
                    for stmt in child.children:
                        self._execute_node(stmt)
                    break  # Only execute first matching catch block
            else:
                # No catch block found - re-raise for outer try-catch
                raise
        except CSSLRuntimeError as e:
            for child in node.children:
                if child.type == 'catch-block':
                    error_var = child.value.get('error_var') if child.value else None
                    if error_var:
                        self.scope.set(error_var, str(e))
                    for stmt in child.children:
                        self._execute_node(stmt)
                    break
            else:
                raise  # Re-raise if no catch block
        except Exception as e:
            # v4.2.6: Also catch Python exceptions
            for child in node.children:
                if child.type == 'catch-block':
                    error_var = child.value.get('error_var') if child.value else None
                    if error_var:
                        self.scope.set(error_var, str(e))
                    for stmt in child.children:
                        self._execute_node(stmt)
                    break
            else:
                raise  # Re-raise if no catch block
        finally:
            # v4.2.6: Execute finally block if present
            for child in node.children:
                if child.type == 'finally-block':
                    for stmt in child.children:
                        self._execute_node(stmt)

        return None

    def _exec_supports_block(self, node: ASTNode) -> Any:
        """Execute standalone supports block for multi-language syntax.

        v4.2.0: Allows 'supports' to be used anywhere, not just in class/function.

        Syntax:
            supports py {
                for i in range(10):
                    print(i)
            }

            supports cpp {
                int x = 42;
                std::cout << x << std::endl;
            }
        """
        block_info = node.value
        language = block_info.get('language')
        raw_source = block_info.get('raw_source')

        # If we have raw_source, transform and execute
        if raw_source and language:
            import textwrap
            from .cssl_languages import get_language
            from .cssl_parser import parse_cssl_program

            # Normalize language ID
            lang_id = language.lstrip('@').lower()

            # Get language support and transformer
            lang_support = get_language(lang_id)
            if lang_support is None:
                raise CSSLRuntimeError(f"Unknown language '{lang_id}' in 'supports' block")

            # Dedent the raw source to normalize indentation
            dedented_source = textwrap.dedent(raw_source)

            # Transform the raw source to CSSL
            transformer = lang_support.get_transformer()
            transformed_source = transformer.transform_source(dedented_source)

            # Parse the transformed CSSL
            try:
                ast = parse_cssl_program(transformed_source)
            except Exception as e:
                raise CSSLRuntimeError(
                    f"Failed to parse transformed '{lang_id}' code in supports block: {e}\n"
                    f"Dedented:\n{dedented_source}\n"
                    f"Transformed:\n{transformed_source}"
                )

            # Execute the transformed AST
            result = None
            for child in ast.children:
                result = self._execute_node(child)

            return result

        # Fallback: execute already-parsed children (CSSL syntax)
        result = None
        for child in node.children:
            result = self._execute_node(child)

        return result

    def _exec_createcmd_inject(self, node: ASTNode) -> Any:
        """Execute createcmd injection: createcmd('cmd') <== { action }"""
        command_call = node.value.get('command_call')
        action_block = node.value.get('action')

        # Get command name from the createcmd call arguments
        args = command_call.value.get('args', [])
        if args:
            command_name = self._evaluate(args[0])
        else:
            raise CSSLRuntimeError("createcmd requires a command name argument")

        # Create the command handler function
        def command_handler(*cmd_args):
            # Create a scope for the command execution
            cmd_scope = Scope(parent=self.scope)

            # Set cmd_args in scope
            cmd_scope.set('args', list(cmd_args))
            cmd_scope.set('argc', len(cmd_args))

            old_scope = self.scope
            self.scope = cmd_scope

            try:
                # Execute action block statements
                for child in action_block.children:
                    if child.type == 'function':
                        # If there's a define action { } inside, call it
                        func_name = child.value.get('name')
                        if func_name == 'action':
                            return self._call_function(child, list(cmd_args))
                    else:
                        self._execute_node(child)
            except CSSLReturn as ret:
                return ret.value
            finally:
                self.scope = old_scope

            return None

        # Register the command using the builtin
        self.builtins.builtin_createcmd(command_name, command_handler)

        return command_name

    def _apply_injection_filter(self, source: Any, filter_info) -> Any:
        """Apply injection filter(s) to extract specific data from source.

        Supports both single filter dict and list of filter dicts for chained filters.
        Example: [dynamic::content=10][dynamic::content=100] applies both filters.

        All BruteInjector Helpers:
        - string::where=VALUE - Filter strings containing VALUE
        - string::length=LENGTH - Filter strings of specific length
        - integer::where=VALUE - Filter integers matching VALUE
        - json::key=KEY - Extract values with specific key from JSON/dict
        - json::value=VALUE - Filter by value in JSON/dict
        - array::index=INDEX - Get specific index from array
        - array::length=LENGTH - Filter arrays of specific length
        - vector::where=VALUE - Filter vectors containing VALUE
        - vector::index=INDEX - Get specific index from vector
        - vector::length=LENGTH - Filter vectors of specific length
        - combo::filterdb - Get filter database from combo
        - combo::blocked - Get blocked items from combo
        - dynamic::VarName=VALUE - Filter by dynamic variable value
        - sql::data - Return only SQL-compatible data
        - instance::class - Get classes from object
        - instance::method - Get methods from object
        - instance::var - Get variables from object
        - instance::all - Get all categorized (methods, classes, vars)
        - instance::"ClassName" - Get specific class by name
        - name::"Name" - Filter by name (class, dict key, attribute)
        """
        if not filter_info:
            return source

        # Handle list of filters (chained filters)
        if isinstance(filter_info, list):
            result = source
            for single_filter in filter_info:
                result = self._apply_single_filter(result, single_filter)
            return result

        # Single filter (dict)
        return self._apply_single_filter(source, filter_info)

    def _apply_single_filter(self, source: Any, filter_info: dict) -> Any:
        """Apply a single injection filter to extract specific data from source."""
        if not filter_info:
            return source

        result = source

        for filter_key, filter_value in filter_info.items():
            if '::' in filter_key:
                filter_type, helper = filter_key.split('::', 1)
                filter_val = self._evaluate(filter_value) if isinstance(filter_value, ASTNode) else filter_value

                # === CHECK CUSTOM FILTERS FIRST ===
                custom_key = f"{filter_type}::{helper}"
                if custom_key in _custom_filters:
                    result = _custom_filters[custom_key](result, filter_val, self)
                    continue

                # Check for catch-all custom filter (type::*)
                catchall_key = f"{filter_type}::*"
                if catchall_key in _custom_filters:
                    result = _custom_filters[catchall_key](result, filter_val, self)
                    continue

                # === STRING HELPERS ===
                if filter_type == 'string':
                    if helper == 'where':
                        # Exact match
                        if isinstance(result, str):
                            result = result if result == filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, str) and item == filter_val]
                    elif helper == 'contains':
                        # Contains substring
                        if isinstance(result, str):
                            result = result if filter_val in result else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, str) and filter_val in item]
                    elif helper == 'not':
                        # Exclude matching
                        if isinstance(result, str):
                            result = result if result != filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if not (isinstance(item, str) and item == filter_val)]
                    elif helper == 'startsWith':
                        if isinstance(result, str):
                            result = result if result.startswith(filter_val) else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, str) and item.startswith(filter_val)]
                    elif helper == 'endsWith':
                        if isinstance(result, str):
                            result = result if result.endswith(filter_val) else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, str) and item.endswith(filter_val)]
                    elif helper in ('length', 'lenght'):  # Support common typo
                        if isinstance(result, str):
                            result = result if len(result) == filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, str) and len(item) == filter_val]
                    elif helper == 'cut':
                        # Cut string - returns the part BEFORE the index/substring
                        # x = <==[string::cut=2] "20:200-1"  -->  x = "20"
                        # x = <==[string::cut="1.0"] "1.0.0"  -->  x = "" (before "1.0")
                        if isinstance(result, str):
                            if isinstance(filter_val, str):
                                # Cut at substring position
                                idx = result.find(filter_val)
                                result = result[:idx] if idx >= 0 else result
                            else:
                                # Cut at integer index
                                idx = int(filter_val)
                                result = result[:idx] if 0 <= idx <= len(result) else result
                        elif isinstance(result, list):
                            def cut_item(item):
                                if not isinstance(item, str):
                                    return item
                                if isinstance(filter_val, str):
                                    idx = item.find(filter_val)
                                    return item[:idx] if idx >= 0 else item
                                return item[:int(filter_val)]
                            result = [cut_item(item) for item in result]
                    elif helper == 'cutAfter':
                        # Get the part AFTER the index/substring
                        # x = <==[string::cutAfter=2] "20:200-1"  -->  x = ":200-1"
                        # x = <==[string::cutAfter="1.0"] "1.0.0"  -->  x = ".0" (after "1.0")
                        if isinstance(result, str):
                            if isinstance(filter_val, str):
                                # Cut after substring
                                idx = result.find(filter_val)
                                result = result[idx + len(filter_val):] if idx >= 0 else result
                            else:
                                # Cut after integer index
                                idx = int(filter_val)
                                result = result[idx:] if 0 <= idx <= len(result) else result
                        elif isinstance(result, list):
                            def cut_after_item(item):
                                if not isinstance(item, str):
                                    return item
                                if isinstance(filter_val, str):
                                    idx = item.find(filter_val)
                                    return item[idx + len(filter_val):] if idx >= 0 else item
                                return item[int(filter_val):]
                            result = [cut_after_item(item) for item in result]
                    elif helper == 'slice':
                        # Slice string with start:end format (e.g., "2:5")
                        if isinstance(result, str) and isinstance(filter_val, str) and ':' in filter_val:
                            parts = filter_val.split(':')
                            start = int(parts[0]) if parts[0] else 0
                            end = int(parts[1]) if parts[1] else len(result)
                            result = result[start:end]
                    elif helper == 'split':
                        # Split string by delimiter
                        if isinstance(result, str):
                            result = result.split(str(filter_val))
                    elif helper == 'replace':
                        # Replace in string (format: "old:new")
                        if isinstance(result, str) and isinstance(filter_val, str) and ':' in filter_val:
                            parts = filter_val.split(':', 1)
                            if len(parts) == 2:
                                result = result.replace(parts[0], parts[1])
                    elif helper == 'upper':
                        if isinstance(result, str):
                            result = result.upper()
                    elif helper == 'lower':
                        if isinstance(result, str):
                            result = result.lower()
                    elif helper == 'trim':
                        if isinstance(result, str):
                            result = result.strip()

                # === INTEGER HELPERS ===
                elif filter_type == 'integer':
                    if helper == 'where':
                        if isinstance(result, int):
                            result = result if result == filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, int) and item == filter_val]
                    # v4.8.8: Integer comparison filters
                    elif helper == 'gt':  # Greater than
                        if isinstance(result, int):
                            result = result if result > filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, int) and item > filter_val]
                    elif helper == 'lt':  # Less than
                        if isinstance(result, int):
                            result = result if result < filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, int) and item < filter_val]
                    elif helper == 'gte' or helper == 'ge':  # Greater than or equal
                        if isinstance(result, int):
                            result = result if result >= filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, int) and item >= filter_val]
                    elif helper == 'lte' or helper == 'le':  # Less than or equal
                        if isinstance(result, int):
                            result = result if result <= filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, int) and item <= filter_val]
                    elif helper == 'not':  # Not equal
                        if isinstance(result, int):
                            result = result if result != filter_val else None
                        elif isinstance(result, list):
                            result = [item for item in result if isinstance(item, int) and item != filter_val]
                    elif helper == 'range':  # Range filter [min, max]
                        if isinstance(filter_val, (list, tuple)) and len(filter_val) == 2:
                            min_val, max_val = filter_val
                            if isinstance(result, int):
                                result = result if min_val <= result <= max_val else None
                            elif isinstance(result, list):
                                result = [item for item in result if isinstance(item, int) and min_val <= item <= max_val]

                # === JSON HELPERS ===
                elif filter_type == 'json':
                    if helper == 'key':
                        if isinstance(result, dict):
                            result = result.get(filter_val)
                        elif isinstance(result, list):
                            result = [item.get(filter_val) for item in result if isinstance(item, dict) and filter_val in item]
                    elif helper == 'value':
                        if isinstance(result, dict):
                            # Find key(s) with matching value
                            matches = [k for k, v in result.items() if v == filter_val]
                            result = matches[0] if len(matches) == 1 else matches
                        elif isinstance(result, list):
                            result = [item for item in result if (isinstance(item, dict) and filter_val in item.values())]

                # === ARRAY HELPERS ===
                elif filter_type == 'array':
                    if helper == 'index':
                        if isinstance(result, (list, tuple)):
                            idx = int(filter_val) if not isinstance(filter_val, int) else filter_val
                            if 0 <= idx < len(result):
                                result = result[idx]
                            else:
                                result = None
                    elif helper in ('length', 'lenght'):  # Support common typo
                        if isinstance(result, (list, tuple)):
                            result = result if len(result) == filter_val else []
                    elif helper == 'where':
                        if isinstance(result, list):
                            result = [item for item in result if item == filter_val]

                # === VECTOR HELPERS ===
                elif filter_type == 'vector':
                    if helper == 'index':
                        if isinstance(result, (list, tuple)):
                            idx = int(filter_val) if not isinstance(filter_val, int) else filter_val
                            if 0 <= idx < len(result):
                                result = result[idx]
                            else:
                                result = None
                    elif helper in ('length', 'lenght'):  # Support common typo
                        if isinstance(result, (list, tuple)):
                            result = result if len(result) == filter_val else []
                    elif helper == 'where':
                        if isinstance(result, list):
                            result = [item for item in result if item == filter_val]

                # === COMBO HELPERS ===
                elif filter_type == 'combo':
                    if helper == 'filterdb':
                        if hasattr(result, '_filterdb'):
                            result = result._filterdb
                        elif hasattr(result, 'filterdb'):
                            result = result.filterdb
                    elif helper == 'blocked':
                        if hasattr(result, '_blocked'):
                            result = result._blocked
                        elif hasattr(result, 'blocked'):
                            result = result.blocked

                # === DYNAMIC HELPERS ===
                elif filter_type == 'dynamic':
                    if helper == 'content':
                        # dynamic::content=VALUE - General content filter for any type
                        # Filters elements where content equals VALUE
                        if isinstance(result, (list, tuple)):
                            # Filter list/tuple elements by content value
                            result = [item for item in result if item == filter_val]
                        elif isinstance(result, dict):
                            # Filter dict by values matching filter_val
                            result = {k: v for k, v in result.items() if v == filter_val}
                        elif result == filter_val:
                            pass  # Keep result if it matches
                        else:
                            result = None
                    elif helper == 'not':
                        # dynamic::not=VALUE - Exclude elements equal to VALUE
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if item != filter_val]
                        elif isinstance(result, dict):
                            result = {k: v for k, v in result.items() if v != filter_val}
                        elif result != filter_val:
                            pass  # Keep result if it doesn't match
                        else:
                            result = None
                    elif helper == 'gt':
                        # dynamic::gt=VALUE - Greater than
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if item > filter_val]
                        elif result > filter_val:
                            pass
                        else:
                            result = None
                    elif helper == 'lt':
                        # dynamic::lt=VALUE - Less than
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if item < filter_val]
                        elif result < filter_val:
                            pass
                        else:
                            result = None
                    elif helper == 'gte':
                        # dynamic::gte=VALUE - Greater than or equal
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if item >= filter_val]
                        elif result >= filter_val:
                            pass
                        else:
                            result = None
                    elif helper == 'lte':
                        # dynamic::lte=VALUE - Less than or equal
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if item <= filter_val]
                        elif result <= filter_val:
                            pass
                        else:
                            result = None
                    elif helper == 'mod':
                        # dynamic::mod=VALUE - Modulo filter (item % VALUE == 0)
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if isinstance(item, (int, float)) and item % filter_val == 0]
                        elif isinstance(result, (int, float)) and result % filter_val == 0:
                            pass
                        else:
                            result = None
                    elif helper == 'range':
                        # dynamic::range="min:max" - Filter values in range
                        if isinstance(filter_val, str) and ':' in filter_val:
                            parts = filter_val.split(':')
                            min_val = int(parts[0]) if parts[0] else None
                            max_val = int(parts[1]) if parts[1] else None
                            if isinstance(result, (list, tuple)):
                                def in_range(x):
                                    if min_val is not None and x < min_val:
                                        return False
                                    if max_val is not None and x > max_val:
                                        return False
                                    return True
                                result = [item for item in result if in_range(item)]
                            elif isinstance(result, (int, float)):
                                if min_val is not None and result < min_val:
                                    result = None
                                elif max_val is not None and result > max_val:
                                    result = None
                    elif helper == 'even':
                        # dynamic::even - Filter even numbers
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if isinstance(item, int) and item % 2 == 0]
                        elif isinstance(result, int) and result % 2 == 0:
                            pass
                        else:
                            result = None
                    elif helper == 'odd':
                        # dynamic::odd - Filter odd numbers
                        if isinstance(result, (list, tuple)):
                            result = [item for item in result if isinstance(item, int) and item % 2 != 0]
                        elif isinstance(result, int) and result % 2 != 0:
                            pass
                        else:
                            result = None
                    else:
                        # dynamic::VarName=VALUE - Match if variable equals value
                        var_name = helper
                        var_value = self.scope.get(var_name)
                        if var_value == filter_val:
                            pass  # Keep result
                        else:
                            result = None

                # === SQL HELPERS ===
                elif filter_type == 'sql':
                    if helper == 'data':
                        # Return only SQL-compatible data types
                        if isinstance(result, (int, str, bool, float, list, dict)):
                            pass  # Keep result
                        else:
                            result = str(result)  # Convert to string

                # === INSTANCE HELPERS ===
                # Works on CSSLInstance, Python objects, dicts, modules
                elif filter_type == 'instance':
                    from .cssl_types import CSSLInstance
                    import inspect

                    if isinstance(result, CSSLInstance):
                        # Filter CSSL instances
                        if helper in ('class', 'classes'):
                            classes = {}
                            for name, member in result._members.items():
                                if isinstance(member, CSSLInstance):
                                    classes[name] = member
                            result = classes if classes else None
                        elif helper in ('method', 'methods'):
                            result = dict(result._class.methods)
                        elif helper in ('var', 'vars', 'variable', 'variables'):
                            vars_dict = {}
                            for name, member in result._members.items():
                                if not isinstance(member, CSSLInstance):
                                    vars_dict[name] = member
                            result = vars_dict
                        elif helper in ('all',):
                            result = {
                                'methods': list(result._class.methods.keys()),
                                'classes': [result._class.name] + [m._class.name for m in result._members.values() if isinstance(m, CSSLInstance)],
                                'vars': [n for n, m in result._members.items() if not isinstance(m, CSSLInstance)]
                            }
                        else:
                            # Filter by class name
                            class_name = filter_val if filter_val else helper
                            found = None
                            if result._class.name == class_name:
                                found = result
                            else:
                                for name, member in result._members.items():
                                    if isinstance(member, CSSLInstance) and member._class.name == class_name:
                                        found = member
                                        break
                            result = found
                    elif isinstance(result, dict):
                        # Filter dicts
                        if helper in ('class', 'classes'):
                            result = {k: v for k, v in result.items() if inspect.isclass(v)}
                        elif helper in ('method', 'methods', 'func', 'function', 'functions'):
                            result = {k: v for k, v in result.items() if callable(v)}
                        elif helper in ('var', 'vars', 'variable', 'variables'):
                            result = {k: v for k, v in result.items() if not callable(v) and not inspect.isclass(v)}
                        else:
                            # Get by key
                            key_name = filter_val if filter_val else helper
                            result = result.get(key_name)
                    elif hasattr(result, '__dict__') or hasattr(result, '__class__'):
                        # Filter Python objects/modules
                        if helper in ('class', 'classes'):
                            classes = {}
                            for name in dir(result):
                                if not name.startswith('_'):
                                    attr = getattr(result, name, None)
                                    if inspect.isclass(attr):
                                        classes[name] = attr
                            result = classes if classes else None
                        elif helper in ('method', 'methods', 'func', 'function', 'functions'):
                            methods = {}
                            for name in dir(result):
                                if not name.startswith('_'):
                                    attr = getattr(result, name, None)
                                    if callable(attr):
                                        methods[name] = attr
                            result = methods if methods else None
                        elif helper in ('var', 'vars', 'variable', 'variables'):
                            vars_dict = {}
                            for name in dir(result):
                                if not name.startswith('_'):
                                    attr = getattr(result, name, None)
                                    if not callable(attr) and not inspect.isclass(attr):
                                        vars_dict[name] = attr
                            result = vars_dict if vars_dict else None
                        elif helper in ('all',):
                            all_info = {'methods': [], 'classes': [], 'vars': []}
                            for name in dir(result):
                                if not name.startswith('_'):
                                    attr = getattr(result, name, None)
                                    if inspect.isclass(attr):
                                        all_info['classes'].append(name)
                                    elif callable(attr):
                                        all_info['methods'].append(name)
                                    else:
                                        all_info['vars'].append(name)
                            result = all_info
                        else:
                            # Get attribute by name
                            attr_name = filter_val if filter_val else helper
                            result = getattr(result, attr_name, None)

                # === NAME HELPERS ===
                # General name filter for any object type
                elif filter_type == 'name':
                    from .cssl_types import CSSLInstance
                    target_name = filter_val if filter_val else helper

                    if isinstance(result, CSSLInstance):
                        if result._class.name == target_name:
                            pass  # Keep result
                        else:
                            found = None
                            for name, member in result._members.items():
                                if isinstance(member, CSSLInstance) and member._class.name == target_name:
                                    found = member
                                    break
                            result = found
                    elif isinstance(result, dict):
                        result = result.get(target_name)
                    elif isinstance(result, list):
                        result = [item for item in result if str(item) == target_name or (hasattr(item, 'name') and item.name == target_name)]
                    elif hasattr(result, target_name):
                        result = getattr(result, target_name)
                    elif hasattr(result, '__class__') and result.__class__.__name__ == target_name:
                        pass  # Keep result if class name matches
                    else:
                        result = None

        return result

    def _exec_inject(self, node: ASTNode) -> Any:
        """Execute inject operation (<==, +<==, -<==)

        Modes:
        - replace: target <== source (replace target with source)
        - add: target +<== source (copy & add to target)
        - remove: target -<== source (remove items in source from target) [v4.9.2]
        """
        target = node.value.get('target')
        source_node = node.value.get('source')
        mode = node.value.get('mode', 'replace')
        filter_info = node.value.get('filter')

        # Check if target is a function call (for permanent injection)
        if isinstance(target, ASTNode) and target.type == 'call':
            callee = target.value.get('callee')
            if isinstance(callee, ASTNode) and callee.type == 'identifier':
                func_name = callee.value
                self.register_function_injection(func_name, source_node)
                return None

        # Check if source is an action_block with %<name> captures
        # If so, capture values NOW and evaluate the block with those captures
        if isinstance(source_node, ASTNode) and source_node.type == 'action_block':
            # Scan for %<name> captured references and capture their current values
            captured_values = self._scan_and_capture_refs(source_node)
            old_captured = self._current_captured_values.copy()
            self._current_captured_values = captured_values
            try:
                # Execute the action block and get the last expression's value
                source = self._evaluate_action_block(source_node)
            finally:
                self._current_captured_values = old_captured
        else:
            # Evaluate source normally
            source = self._evaluate(source_node)

        # Apply filter if present
        if filter_info:
            source = self._apply_injection_filter(source, filter_info)

        # Get current target value for add/move/replace modes (needed for UniversalInstance handling)
        current_value = None
        try:
            current_value = self._evaluate(target)
        except Exception:
            # Target might not exist yet, that's okay for add mode
            current_value = None

        # Determine final value based on mode
        if mode == 'replace':
            from .cssl_types import CSSLInstance, UniversalInstance, CSSLClass
            # Special handling for UniversalInstance targets - inject instead of replace
            if isinstance(current_value, UniversalInstance):
                if isinstance(source, CSSLClass):
                    current_value.set_member(source.name, source)
                    final_value = current_value
                elif isinstance(source, ASTNode) and source.type == 'function':
                    func_info = source.value
                    func_name = func_info.get('name') if isinstance(func_info, dict) else None
                    if func_name:
                        current_value.set_method(func_name, source, self)
                    final_value = current_value
                elif isinstance(source, CSSLInstance):
                    current_value.set_member(source._class.name, source)
                    final_value = current_value
                else:
                    # For other types, store as member with source type name
                    final_value = source
            else:
                final_value = source
        elif mode == 'add':
            # Copy & add - preserve target and add source
            from .cssl_types import CSSLInstance, UniversalInstance, CSSLClass

            # Special handling for UniversalInstance + CSSLClass
            if isinstance(current_value, UniversalInstance) and isinstance(source, CSSLClass):
                # Inject class definition into universal instance
                current_value.set_member(source.name, source)
                final_value = current_value
            # Special handling for UniversalInstance + Function (AST node)
            elif isinstance(current_value, UniversalInstance) and isinstance(source, ASTNode) and source.type == 'function':
                # Inject function as a method into universal instance
                func_info = source.value
                func_name = func_info.get('name') if isinstance(func_info, dict) else None
                if func_name:
                    current_value.set_method(func_name, source, self)
                final_value = current_value
            # Special handling for UniversalInstance + CSSLInstance
            elif isinstance(current_value, UniversalInstance) and isinstance(source, CSSLInstance):
                class_name = source._class.name
                current_value.set_member(class_name, source)
                final_value = current_value
            # Special handling for CSSLInstance - merge classes
            elif isinstance(current_value, CSSLInstance) and isinstance(source, CSSLInstance):
                # Add the new class instance as a member with class name as key
                class_name = source._class.name
                current_value._members[class_name] = source
                final_value = current_value
            elif isinstance(current_value, list):
                if isinstance(source, list):
                    final_value = current_value + source
                else:
                    final_value = current_value + [source]
            elif isinstance(current_value, dict) and isinstance(source, dict):
                final_value = {**current_value, **source}
            elif isinstance(current_value, str) and isinstance(source, str):
                final_value = current_value + source
            # Handle CSSL container types (DataStruct, Vector, Stack, etc.)
            elif hasattr(current_value, 'append') or hasattr(current_value, 'push') or hasattr(current_value, 'add') or hasattr(current_value, 'update'):
                # v4.9.2: Special handling for dict source into containers with update method
                if isinstance(source, dict) and hasattr(current_value, 'update'):
                    current_value.update(source)
                elif isinstance(source, dict) and hasattr(current_value, '__setitem__'):
                    # DataStruct, Map, etc. - merge dict key-value pairs
                    for k, v in source.items():
                        current_value[k] = v
                elif hasattr(current_value, 'append'):
                    current_value.append(source)
                elif hasattr(current_value, 'push'):
                    current_value.push(source)
                elif hasattr(current_value, 'add'):
                    current_value.add(source)
                final_value = current_value
            elif current_value is None:
                # v4.9.2: Handle None target - wrap source appropriately
                if isinstance(source, dict):
                    final_value = source  # Keep dict as-is
                elif isinstance(source, list):
                    final_value = source
                else:
                    final_value = source  # Keep single value as-is
            else:
                final_value = [current_value, source]
        elif mode == 'move':
            # v4.9.2: Changed semantics - remove items from target (not move from source)
            # target -<== source → remove items in source from target
            if isinstance(current_value, list):
                if isinstance(source, list):
                    # Remove all items in source from current_value
                    final_value = [item for item in current_value if item not in source]
                else:
                    # Remove single item
                    final_value = [item for item in current_value if item != source]
            elif isinstance(current_value, dict) and isinstance(source, (list, tuple)):
                # Remove keys from dict
                final_value = {k: v for k, v in current_value.items() if k not in source}
            elif isinstance(current_value, dict) and isinstance(source, dict):
                # Remove keys that exist in source dict
                final_value = {k: v for k, v in current_value.items() if k not in source}
            elif hasattr(current_value, 'remove') or hasattr(current_value, '__delitem__'):
                # CSSL container types
                if isinstance(source, (list, tuple)):
                    for item in source:
                        if hasattr(current_value, 'remove'):
                            try:
                                current_value.remove(item)
                            except (ValueError, KeyError):
                                pass
                elif hasattr(current_value, 'remove'):
                    try:
                        current_value.remove(source)
                    except (ValueError, KeyError):
                        pass
                final_value = current_value
            else:
                # Fallback - just return source (old behavior)
                final_value = source
        else:
            final_value = source

        # Set the target
        if target.type == 'identifier':
            self.scope.set(target.value, final_value)
        elif target.type == 'module_ref':
            self._set_module_value(target.value, final_value)
        elif target.type == 'shared_ref':
            # $Name <== value - create/update shared object
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            name = target.value
            _live_objects[name] = final_value
            self.global_scope.set(f'${name}', SharedObjectProxy(name, final_value))
        elif target.type == 'member_access':
            self._set_member(target, final_value)
        elif target.type == 'this_access':
            # v4.9.2: this->member <== value
            if self._current_instance is None:
                raise CSSLRuntimeError("'this' used outside of class method context")
            member = target.value.get('member')
            if hasattr(self._current_instance, 'set_member'):
                self._current_instance.set_member(member, final_value)
            else:
                setattr(self._current_instance, member, final_value)
        elif target.type == 'call':
            callee = target.value.get('callee')
            if isinstance(callee, ASTNode) and callee.type == 'member_access':
                obj = self._evaluate(callee.value.get('object'))
                method_name = callee.value.get('member')
                if method_name == 'add' and isinstance(obj, list):
                    obj.append(final_value)
                    return final_value

        return final_value

    def _exec_receive(self, node: ASTNode) -> Any:
        """Execute receive operation (==>, ==>+, -==>)

        Modes:
        - replace: source ==> target (move source to target, replace)
        - add: source ==>+ target (copy source to target, add)
        - move: source -==> target (move from source, remove)
        """
        source_node = node.value.get('source')
        target = node.value.get('target')
        mode = node.value.get('mode', 'replace')
        filter_info = node.value.get('filter')

        # Evaluate source
        source = self._evaluate(source_node)

        # Apply filter if present
        if filter_info:
            source = self._apply_injection_filter(source, filter_info)

        # Get current target value for add mode
        current_value = None
        if mode == 'add':
            current_value = self._evaluate(target)

        # Determine final value based on mode
        if mode == 'replace':
            final_value = source
        elif mode == 'add':
            if isinstance(current_value, list):
                if isinstance(source, list):
                    final_value = current_value + source
                else:
                    final_value = current_value + [source]
            elif isinstance(current_value, dict) and isinstance(source, dict):
                final_value = {**current_value, **source}
            elif isinstance(current_value, str) and isinstance(source, str):
                final_value = current_value + source
            # v4.9.2: Handle CSSL container types
            elif hasattr(current_value, 'append') or hasattr(current_value, 'push') or hasattr(current_value, 'add') or hasattr(current_value, 'update'):
                if isinstance(source, dict) and hasattr(current_value, 'update'):
                    current_value.update(source)
                elif isinstance(source, dict) and hasattr(current_value, '__setitem__'):
                    for k, v in source.items():
                        current_value[k] = v
                elif hasattr(current_value, 'append'):
                    current_value.append(source)
                elif hasattr(current_value, 'push'):
                    current_value.push(source)
                elif hasattr(current_value, 'add'):
                    current_value.add(source)
                final_value = current_value
            elif current_value is None:
                # v4.9.2: Keep source type when target is None
                if isinstance(source, dict):
                    final_value = source
                elif isinstance(source, list):
                    final_value = source
                else:
                    final_value = source
            else:
                final_value = [current_value, source]
        elif mode == 'move':
            final_value = source
            # Remove filtered elements from source (not clear entirely)
            if isinstance(source_node, ASTNode):
                if filter_info:
                    # Get original source value
                    original_source = self._evaluate(source_node)
                    if isinstance(original_source, list) and isinstance(final_value, list):
                        # Remove filtered items from original list
                        remaining = [item for item in original_source if item not in final_value]
                        if source_node.type == 'identifier':
                            self.scope.set(source_node.value, remaining)
                        elif source_node.type == 'module_ref':
                            self._set_module_value(source_node.value, remaining)
                        elif source_node.type == 'member_access':
                            self._set_member(source_node, remaining)
                    else:
                        # Single value filter - set source to None
                        if source_node.type == 'identifier':
                            self.scope.set(source_node.value, None)
                        elif source_node.type == 'module_ref':
                            self._set_module_value(source_node.value, None)
                        elif source_node.type == 'member_access':
                            self._set_member(source_node, None)
                else:
                    # No filter - clear entire source
                    if source_node.type == 'identifier':
                        self.scope.set(source_node.value, None)
                    elif source_node.type == 'module_ref':
                        self._set_module_value(source_node.value, None)
                    elif source_node.type == 'member_access':
                        self._set_member(source_node, None)
        else:
            final_value = source

        # Set the target
        if target.type == 'identifier':
            self.scope.set(target.value, final_value)
        elif target.type == 'module_ref':
            self._set_module_value(target.value, final_value)
        elif target.type == 'shared_ref':
            # value ==> $Name - create/update shared object
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            name = target.value
            _live_objects[name] = final_value
            self.global_scope.set(f'${name}', SharedObjectProxy(name, final_value))
        elif target.type == 'instance_ref':
            # value ==> instance<"name"> - create/update shared object
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            name = target.value
            _live_objects[name] = final_value
            self.global_scope.set(f'${name}', SharedObjectProxy(name, final_value))
        elif target.type == 'member_access':
            self._set_member(target, final_value)
        elif target.type == 'this_access':
            # v4.9.2: source ==> this->member
            if self._current_instance is None:
                raise CSSLRuntimeError("'this' used outside of class method context")
            member = target.value.get('member')
            if hasattr(self._current_instance, 'set_member'):
                self._current_instance.set_member(member, final_value)
            else:
                setattr(self._current_instance, member, final_value)
        elif target.type == 'typed_declaration':
            # Handle typed target: source ==> datastruct<dynamic> Output
            var_name = target.value.get('name')
            type_name = target.value.get('type_name')
            element_type = target.value.get('element_type', 'dynamic')

            # Create appropriate container with final_value
            from .cssl_types import (create_datastruct, create_vector, create_array,
                                      create_stack, create_list, create_dictionary, create_map)

            container = None
            if type_name == 'datastruct':
                container = create_datastruct(element_type)
            elif type_name == 'vector':
                container = create_vector(element_type)
            elif type_name == 'array':
                container = create_array(element_type)
            elif type_name == 'stack':
                container = create_stack(element_type)
            elif type_name == 'list':
                container = create_list(element_type)
            elif type_name == 'dictionary':
                container = create_dictionary()
            elif type_name == 'map':
                container = create_map()

            if container is not None:
                # Add final_value to container
                if isinstance(final_value, (list, tuple)):
                    container.extend(final_value)
                elif final_value is not None:
                    container.append(final_value)
                self.scope.set(var_name, container)
            else:
                # Unknown type, just set the value directly
                self.scope.set(var_name, final_value)

        return final_value

    def _exec_infuse(self, node: ASTNode) -> Any:
        """Execute code infusion (<<==, +<<==, -<<==)

        Modes:
        - replace: func <<== { code } - REPLACES function body (original won't execute)
        - add: func +<<== { code } - ADDS code to function (both execute)
        - remove: func -<<== { code } - REMOVES matching code from function

        Also supports instance injection:
        - instance +<<== { void method() { ... } } - ADDS methods to UniversalInstance

        Also supports expression form: func <<== %exit() (wraps in action_block)
        """
        from .cssl_types import UniversalInstance

        target = node.value.get('target')
        code_block = node.value.get('code')
        source_expr = node.value.get('source')  # For expression form: func <<== expr
        mode = node.value.get('mode', 'replace')  # Default is REPLACE for <<==

        # If source expression is provided instead of code block, wrap it
        if code_block is None and source_expr is not None:
            # Wrap in expression node so _execute_node can handle it
            expr_node = ASTNode('expression', value=source_expr)
            code_block = ASTNode('action_block', children=[expr_node])

        # Check if target is a UniversalInstance
        target_value = None
        if isinstance(target, ASTNode) and target.type == 'identifier':
            target_value = self.scope.get(target.value)
            if target_value is None:
                target_value = self.global_scope.get(target.value)

        # Handle UniversalInstance injection
        if isinstance(target_value, UniversalInstance):
            return self._inject_into_instance(target_value, code_block, mode)

        # Get function name from target
        func_name = None
        if isinstance(target, ASTNode):
            if target.type == 'identifier':
                func_name = target.value
            elif target.type == 'call':
                callee = target.value.get('callee')
                if isinstance(callee, ASTNode) and callee.type == 'identifier':
                    func_name = callee.value

        if not func_name or code_block is None:
            return None

        # v4.8.6: Check if target is actually a function or if it's just a variable
        # If it's a variable (not a function), fall back to value assignment with capture
        existing_func = self.scope.get(func_name)
        if existing_func is None:
            existing_func = self.global_scope.get(func_name)
        is_function = (isinstance(existing_func, ASTNode) and existing_func.type == 'function') or callable(existing_func)

        if not is_function and target.type == 'identifier':
            # Target is a variable, not a function - do value capture assignment instead
            # This handles: savedVersion <<== { %version; }
            captured_values = self._scan_and_capture_refs(code_block)
            old_captured = self._current_captured_values.copy()
            self._current_captured_values = captured_values
            try:
                value = self._evaluate_action_block(code_block)
            finally:
                self._current_captured_values = old_captured
            self.scope.set(func_name, value)
            return value

        if mode == 'add':
            # +<<== : Add code to function (both injection + original execute)
            self.register_function_injection(func_name, code_block)
            self._function_replaced[func_name] = False  # Don't replace, just add
        elif mode == 'replace':
            # <<== : Replace function body (only injection executes, original skipped)
            # Save original function BEFORE replacing (for original() access)
            if func_name not in self._original_functions:
                # Try to find original in scope or builtins
                original = self.scope.get(func_name)
                if original is None:
                    original = getattr(self.builtins, f'builtin_{func_name}', None)
                if original is not None:
                    self._original_functions[func_name] = original
            # Capture %<name> references at registration time
            captured_values = self._scan_and_capture_refs(code_block)
            self._function_injections[func_name] = [(code_block, captured_values)]
            self._function_replaced[func_name] = True  # Mark as replaced
        elif mode == 'remove':
            # -<<== or -<<==[n] : Remove matching code from function body
            remove_index = node.value.get('index')

            if func_name in self._function_injections:
                if remove_index is not None:
                    # Indexed removal: -<<==[n] removes only the nth injection
                    if 0 <= remove_index < len(self._function_injections[func_name]):
                        self._function_injections[func_name].pop(remove_index)
                else:
                    # No index: -<<== removes all injections
                    self._function_injections[func_name] = []
            self._function_replaced[func_name] = False

        return None

    def _inject_into_instance(self, instance: Any, code_block: Any, mode: str) -> Any:
        """Inject code/methods into a UniversalInstance.

        Usage:
            instance<"myContainer"> container;
            container +<<== {
                void sayHello() { printl("Hello!"); }
                int value = 42;
            }
        """
        from .cssl_types import UniversalInstance

        if not isinstance(instance, UniversalInstance):
            return None

        if code_block is None:
            return None

        # Store the raw injection
        instance.add_injection(code_block)

        # Parse the code block for function definitions and variable declarations
        if isinstance(code_block, ASTNode):
            children = code_block.children if hasattr(code_block, 'children') else []

            for child in children:
                if isinstance(child, ASTNode):
                    if child.type == 'function':
                        # Extract function name and store the AST node
                        func_info = child.value
                        func_name = func_info.get('name') if isinstance(func_info, dict) else None
                        if func_name:
                            instance.set_method(func_name, child, self)
                    elif child.type == 'var_declaration':
                        # Extract variable and value
                        var_info = child.value
                        if isinstance(var_info, dict):
                            var_name = var_info.get('name')
                            value_node = var_info.get('value')
                            if var_name:
                                value = self._evaluate(value_node) if value_node else None
                                instance.set_member(var_name, value)
                    elif child.type == 'typed_var_declaration':
                        # Typed variable declaration
                        var_info = child.value
                        if isinstance(var_info, dict):
                            var_name = var_info.get('name')
                            value_node = var_info.get('value')
                            if var_name:
                                value = self._evaluate(value_node) if value_node else None
                                instance.set_member(var_name, value)

        return instance

    def _exec_infuse_right(self, node: ASTNode) -> Any:
        """Execute right-side code infusion (==>>)"""
        source = node.value.get('source')
        target = node.value.get('target')
        mode = node.value.get('mode', 'replace')

        # Similar to infuse but direction is reversed
        func_name = None
        if isinstance(target, ASTNode):
            if target.type == 'identifier':
                func_name = target.value
            elif target.type == 'call':
                callee = target.value.get('callee')
                if isinstance(callee, ASTNode) and callee.type == 'identifier':
                    func_name = callee.value

        if func_name and isinstance(source, ASTNode):
            self.register_function_injection(func_name, source)

        return None

    def _exec_flow(self, node: ASTNode) -> Any:
        """Execute flow operation (-> or <-)"""
        source = self._evaluate(node.value.get('source'))
        target = node.value.get('target')

        # Flow sends data to a target (could be function call or variable)
        if target.type == 'call':
            callee = self._evaluate(target.value.get('callee'))
            args = [source] + [self._evaluate(a) for a in target.value.get('args', [])]

            if callable(callee):
                return callee(*args)
            elif isinstance(callee, ASTNode) and callee.type == 'function':
                return self._call_function(callee, args)
        elif target.type == 'identifier':
            self.scope.set(target.value, source)
        elif target.type == 'module_ref':
            self._set_module_value(target.value, source)
        elif target.type == 'shared_ref':
            # $Name <== value - create/update shared object
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            name = target.value
            _live_objects[name] = source
            self.global_scope.set(f'${name}', SharedObjectProxy(name, source))
        elif target.type == 'member_access':
            self._set_member(target, source)

        return source

    def _exec_assignment(self, node: ASTNode) -> Any:
        """Execute assignment"""
        target = node.value.get('target')

        # v4.9.4: Check if target variable is freezed (immutable) - return null if so
        if isinstance(target, ASTNode) and target.type == 'identifier':
            var_name = target.value
            if var_name in self._var_meta and self._var_meta[var_name].get('is_freezed', False):
                return None  # Cannot reassign freezed variable

        value = self._evaluate(node.value.get('value'))

        if isinstance(target, ASTNode):
            if target.type == 'identifier':
                # Check if we're in a class method and this is a class member
                # If so, set the member instead of creating a local variable
                if self._current_instance is not None and self._current_instance.has_member(target.value):
                    self._current_instance.set_member(target.value, value)
                else:
                    self.scope.set(target.value, value)
            elif target.type == 'global_ref':
                # r@Name = value - store in promoted globals
                self._promoted_globals[target.value] = value
                self.global_scope.set(target.value, value)
            elif target.type == 'shared_ref':
                # $Name = value - create/update shared object
                from ..cssl_bridge import _live_objects, SharedObjectProxy
                name = target.value
                _live_objects[name] = value
                self.global_scope.set(f'${name}', SharedObjectProxy(name, value))
            elif target.type == 'captured_ref':
                # v4.8.9: %name = value - assign to snapshot directly
                # This allows: %xyz = othervar, %xyz = "hello", %xyz = (int number = 200)
                name = target.value
                self.builtins._snapshots[name] = value
            elif target.type == 'pointer_ref':
                # v4.9.0: ?name = value - create pointer to value
                # The pointer stores an address to the object
                name = target.value
                from .cssl_types import Address
                addr = Address(obj=value)
                self.scope.set(f'?{name}', addr)
            elif target.type == 'module_ref':
                # @Name = value - store in promoted globals (like global keyword)
                self._promoted_globals[target.value] = value
                self.global_scope.set(target.value, value)
            elif target.type == 'member_access':
                self._set_member(target, value)
            elif target.type == 'index_access':
                self._set_index(target, value)
            elif target.type == 'this_access':
                # this->member = value
                if self._current_instance is None:
                    raise CSSLRuntimeError("'this' used outside of class method context")
                member = target.value.get('member')
                instance = self._current_instance
                # Check if instance is a CSSL instance or a plain Python object
                if hasattr(instance, 'set_member'):
                    instance.set_member(member, value)
                else:
                    # Plain Python object - use setattr
                    setattr(instance, member, value)
        elif isinstance(target, str):
            # v4.9.4: Check if string target is freezed - return null if so
            if target in self._var_meta and self._var_meta[target].get('is_freezed', False):
                return None
            self.scope.set(target, value)

        return value

    def _exec_tuple_assignment(self, node: ASTNode) -> Any:
        """Execute tuple unpacking assignment: a, b, c = shuffled_func()

        Used with shuffled functions that return multiple values.
        """
        targets = node.value.get('targets', [])
        value = self._evaluate(node.value.get('value'))

        # Convert value to list if it's a tuple or iterable
        if isinstance(value, (list, tuple)):
            values = list(value)
        elif hasattr(value, '__iter__') and not isinstance(value, (str, dict)):
            values = list(value)
        else:
            # Single value - assign to first target only
            values = [value]

        # Assign values to targets
        for i, target in enumerate(targets):
            if i < len(values):
                var_name = target.value if isinstance(target, ASTNode) else target
                self.scope.set(var_name, values[i])
            else:
                # More targets than values - set to None
                var_name = target.value if isinstance(target, ASTNode) else target
                self.scope.set(var_name, None)

        # Assignment statements don't produce a visible result
        return None

    def _exec_expression(self, node: ASTNode) -> Any:
        """Execute expression statement"""
        return self._evaluate(node.value)

    def _exec_type_instantiation(self, node: ASTNode) -> Any:
        """Execute type instantiation as statement (e.g., vector<int>)"""
        return self._evaluate(node)

    def _exec_then(self, node: ASTNode) -> Any:
        """Execute then block"""
        for child in node.children:
            self._execute_node(child)
        return None

    def _exec_else(self, node: ASTNode) -> Any:
        """Execute else block"""
        for child in node.children:
            self._execute_node(child)
        return None

    def _exec_try_block(self, node: ASTNode) -> Any:
        """Execute try block"""
        for child in node.children:
            self._execute_node(child)
        return None

    def _exec_catch_block(self, node: ASTNode) -> Any:
        """Execute catch block"""
        for child in node.children:
            self._execute_node(child)
        return None

    def _evaluate(self, node: Any) -> Any:
        """Evaluate an expression node to get its value"""
        if node is None:
            return None

        if not isinstance(node, ASTNode):
            return node

        if node.type == 'literal':
            value = node.value
            # Handle dict-format literals from parser: {'type': 'int', 'value': 0}
            if isinstance(value, dict) and 'value' in value:
                value = value['value']
            # String interpolation - replace {var} or <var> with scope values
            if isinstance(value, str):
                has_fstring = '{' in value and '}' in value
                has_legacy = '<' in value and '>' in value
                if has_fstring or has_legacy:
                    value = self._interpolate_string(value)
            return value

        # NEW: Type literals (list, dict) - create empty instances
        if node.type == 'type_literal':
            type_name = node.value
            if type_name == 'list':
                return []
            elif type_name == 'dict':
                return {}
            return None

        # v4.9.0: Byte literal (x^y notation)
        if node.type == 'byte_literal':
            from .cssl_types import Byte
            base = node.value.get('base')
            weight = node.value.get('weight')
            return Byte(base, weight)

        # v4.8.9: Typed expression (type name = value) - creates variable and returns value
        # Used for snapshot assignment: %xyz = (int number = 200)
        if node.type == 'typed_expression':
            var_type = node.value.get('type')
            var_name = node.value.get('name')
            var_value = self._evaluate(node.value.get('value'))
            # Create the typed variable in current scope
            self.scope.set(var_name, var_value)
            # Return the value so it can be used in assignment
            return var_value

        if node.type == 'identifier':
            name = node.value

            # Handle enum/namespace access: Colors::RED, MyNamespace::func
            if '::' in name:
                parts = name.split('::', 1)
                container_name = parts[0]
                member_name = parts[1]

                # Look up the container (enum, class, namespace, or module)
                container = self.scope.get(container_name)
                if container is None:
                    container = self.global_scope.get(container_name)
                if container is None:
                    container = self._promoted_globals.get(container_name)
                # v4.8: Also check modules for :: access (fmt::green, etc.)
                if container is None:
                    container = self.get_module(container_name)

                if container is not None:
                    # v4.8: Handle CSSLNamespace - supports arbitrarily deep nested access
                    if isinstance(container, CSSLNamespace):
                        # Handle nested :: access (e.g., ns::inner::deep::func)
                        current = container
                        remaining = member_name
                        while '::' in remaining and isinstance(current, CSSLNamespace):
                            parts = remaining.split('::', 1)
                            current = current.get(parts[0])
                            remaining = parts[1]
                            if current is None:
                                break
                        # Final lookup
                        if isinstance(current, CSSLNamespace):
                            return current.get(remaining)
                        return current if current is not None else None
                    # If it's a dict-like object (enum or namespace), get the member
                    elif isinstance(container, dict):
                        return container.get(member_name)
                    # If it's an object with the member as an attribute
                    elif hasattr(container, member_name):
                        return getattr(container, member_name)

                # v4.3.2: Check if full name exists as builtin function (json::write, string::cut, etc.)
                if self.builtins.has_function(name):
                    return self.builtins.get_function(name)

                # Fall through to normal lookup if container not found
                return None

            # v4.9.2: When inside a hook execution, return original builtin to prevent recursion
            # This must be checked BEFORE scope lookup since the hook is stored in scope
            if name in self._hook_executing and name in self._original_functions:
                return self._original_functions[name]

            value = self.scope.get(name)
            # Check if it's a class member in current instance context
            # This allows accessing members without 'this->' inside methods
            if value is None and self._current_instance is not None:
                if self._current_instance.has_member(name):
                    value = self._current_instance.get_member(name)
                elif self._current_instance.has_method(name):
                    # Return bound method
                    method_node = self._current_instance.get_method(name)
                    instance = self._current_instance
                    value = lambda *args, **kwargs: self._call_method(instance, method_node, list(args), kwargs)
            # Fallback to global scope
            if value is None:
                value = self.global_scope.get(name)
            # Fallback to promoted globals (from 'global' keyword)
            if value is None:
                value = self._promoted_globals.get(name)
            # Fallback to builtins
            if value is None and self.builtins.has_function(name):
                return self.builtins.get_function(name)
            return value

        if node.type == 'module_ref':
            # User-defined globals have priority over SDK modules
            # Check promoted globals first, then global scope, then SDK modules
            value = self._promoted_globals.get(node.value)
            if value is None:
                value = self.global_scope.get(node.value)
            if value is None:
                value = self.get_module(node.value)  # SDK modules as fallback
            return value

        if node.type == 'self_ref':
            # s@<name> reference to global struct
            return self.get_global_struct(node.value)

        if node.type == 'global_ref':
            # r@<name> global variable reference
            # v4.9.4: Check if variable is marked as 'local' - return null if so
            var_name = node.value
            if var_name in self._var_meta and self._var_meta[var_name].get('is_local', False):
                return None  # local variables cannot be accessed via @
            # Check promoted globals first, then global scope
            value = self._promoted_globals.get(var_name)
            if value is None:
                value = self.global_scope.get(var_name)
            return value

        if node.type == 'shared_ref':
            # $<name> shared object reference
            # Returns the SharedObjectProxy for live access
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            name = node.value
            if name in _live_objects:
                return SharedObjectProxy(name, _live_objects[name])
            # Check if stored in runtime's scope as $name
            scoped_val = self.global_scope.get(f'${name}')
            if scoped_val is not None:
                return scoped_val
            # List available shared objects for helpful error
            available_shared = list(_live_objects.keys())
            similar = _find_similar_names(name, available_shared)
            if similar:
                hint = f"Did you mean: ${', $'.join(similar)}?"
            elif available_shared:
                hint = f"Available shared objects: ${', $'.join(available_shared[:5])}"
            else:
                hint = "Use share(name, object) from Python to share objects first."

            raise self._format_error(
                node.line if hasattr(node, 'line') else 0,
                f"Shared object '${name}' not found",
                hint
            )

        if node.type == 'captured_ref':
            # %<name> captured reference - use value captured at infusion registration time
            # Priority: The % prefix means "get the ORIGINAL value before any replacement"
            name = node.value

            # v4.9.4: Check if variable is marked as 'static' - return null if so
            if name in self._var_meta and self._var_meta[name].get('is_static', False):
                return None  # static variables cannot be snapshotted/captured

            # 1. First check captured values from current injection context
            if name in self._current_captured_values:
                captured_value = self._current_captured_values[name]
                if captured_value is not None:
                    return captured_value

            # 2. v4.2.3: Check _original_functions FIRST - this is the pre-replacement value
            #    This ensures %exit() refers to the ORIGINAL exit when using &exit
            value = self._original_functions.get(name)
            if value is not None:
                return value

            # 3. v4.8.8: Check snapshots - %name accesses snapshotted values (BEFORE scope!)
            #    This ensures snapshot(var); var = "new"; %var returns the OLD value
            if hasattr(self.builtins, '_snapshots') and name in self.builtins._snapshots:
                return self.builtins._snapshots[name]

            # 4. v4.9.2: Only fall back to scope if we're in an injection context
            #    (i.e., _current_captured_values is populated). For direct %name usage
            #    outside injections, return null if no snapshot exists.
            if self._current_captured_values:
                # We're in an injection context - fall back to scope/builtins
                value = self.scope.get(name)
                if value is None:
                    value = self.global_scope.get(name)
                if value is None:
                    # For critical builtins like 'exit', create direct wrapper
                    if name == 'exit':
                        runtime = self
                        value = lambda code=0, rt=runtime: rt.exit(code)
                    else:
                        value = getattr(self.builtins, f'builtin_{name}', None)
                if value is not None:
                    return value

                # Build helpful error for captured reference in injection context
                hint = f"Variable '{name}' must exist when the infusion is registered, or be snapshotted with snapshot({name}). Check that '%{name}' is defined before use."
                raise self._format_error(
                    node.line if hasattr(node, 'line') else 0,
                    f"Captured reference '%{name}' not found (no snapshot or captured value)",
                    hint
                )
            else:
                # v4.9.2: Direct %name usage outside injection - no snapshot exists, return null
                return None

        # v4.9.2: Local reference - local::<name> accesses hooked function's local variables/params
        if node.type == 'local_ref':
            name = node.value
            # Access the hook's local context (set by hook wrapper)
            if hasattr(self, '_hook_locals') and self._hook_locals:
                if name in self._hook_locals:
                    return self._hook_locals[name]
            # Also check _result which is set automatically for append hooks
            if name == 'result' or name == '_result':
                result = self.scope.get('_result')
                if result is not None:
                    return result
            # Fall back to current scope
            value = self.scope.get(name)
            if value is not None:
                return value
            return None

        # v4.9.2: Local assignment - local::<name> = value
        if node.type == 'local_assign':
            name = node.value.get('name')
            value_node = node.value.get('value')
            value = self._evaluate(value_node)
            # Set in hook locals if available, otherwise scope
            if hasattr(self, '_hook_locals') and self._hook_locals is not None:
                self._hook_locals[name] = value
            else:
                self.scope.set(name, value)
            return value

        # v4.9.2: Local injection - local::func -<<== {...} or local::func +<<== {...}
        if node.type == 'local_injection':
            local_name = node.value.get('local_name')
            mode = node.value.get('mode')  # 'remove', 'add', 'replace'
            filters = node.value.get('filters', [])
            code_block = node.value.get('code')
            # This modifies the local function at runtime - advanced feature
            # For now, just store the injection intent
            if not hasattr(self, '_local_injections'):
                self._local_injections = {}
            self._local_injections[local_name] = {
                'mode': mode,
                'filters': filters,
                'code': code_block
            }
            return None

        # v4.9.0: Pointer reference - ?name can either:
        # 1. Dereference an existing pointer named ?name
        # 2. Create an Address to a variable named 'name' (v4.9.2)
        if node.type == 'pointer_ref':
            name = node.value
            # First check if ?name exists as a pointer in scope
            addr = self.scope.get(f'?{name}')
            if addr is None:
                addr = self.global_scope.get(f'?{name}')

            if addr is not None:
                # Dereference the existing pointer
                if isinstance(addr, Address):
                    return addr.reflect()
                # If it's a direct object (simple pointer), return it
                return addr

            # v4.9.2: No pointer exists - check if 'name' is a variable
            # If so, create an Address pointing to it (like &name in C)
            # v4.9.3: If the variable IS an Address, dereference it instead
            var_value = self.scope.get(name)
            if var_value is None:
                var_value = self.global_scope.get(name)

            if var_value is not None:
                # v4.9.3: If var is already an Address, dereference it
                if isinstance(var_value, Address):
                    return var_value.reflect()
                # Otherwise create an Address to this variable
                return Address(obj=var_value)

            # Neither pointer nor variable exists
            raise self._format_error(
                node.line if hasattr(node, 'line') else 0,
                f"Cannot resolve '?{name}': no pointer '?{name}' or variable '{name}' found",
                f"Either create a pointer: ?{name} = someObject, or declare variable: {name} = value"
            )

        # v4.9.4: Pointer-snapshot reference ?%name - get address of snapshotted value
        if node.type == 'pointer_snapshot_ref':
            from .cssl_types import Address as SnapshotAddress
            name = node.value
            # Get the snapshot value
            snapshot_value = self.builtins._snapshots.get(name)
            if snapshot_value is None:
                raise self._format_error(
                    node.line if hasattr(node, 'line') else 0,
                    f"Snapshot '%{name}' does not exist",
                    f"Create a snapshot first with: snapshot({name})"
                )
            # Return an Address pointing to the snapshot value
            return SnapshotAddress(obj=snapshot_value)

        if node.type == 'instance_ref':
            # instance<"name"> - get shared instance by name
            # Works like $name but with explicit syntax
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            name = node.value
            if name in _live_objects:
                return SharedObjectProxy(name, _live_objects[name])
            # Check if stored in runtime's scope
            scoped_val = self.global_scope.get(f'${name}')
            if scoped_val is not None:
                return scoped_val
            # Return None if instance doesn't exist (can be created via ==>)
            return None

        # v4.1.0/v4.1.1: Cross-language instance reference: cpp$ClassName, py$Object
        # Enhanced bidirectional access with real runtime bridges
        if node.type == 'lang_instance_ref':
            ref = node.value  # {'lang': 'cpp', 'instance': 'ClassName'}
            lang_id = ref['lang']
            instance_name = ref['instance']

            # First, try to get the language support object from scope
            lang_support = self.scope.get(lang_id)
            if lang_support is None:
                lang_support = self.global_scope.get(lang_id)

            # If not found in scope, try to get from modules
            if lang_support is None:
                lang_support = self._modules.get(lang_id)

            # If still not found, try getting default language support
            if lang_support is None:
                from .cssl_languages import get_language
                lang_support = get_language(lang_id)

            if lang_support is not None:
                # v4.1.1: Check if it's a LanguageSupport object with get_instance method
                if hasattr(lang_support, 'get_instance'):
                    instance = lang_support.get_instance(instance_name)
                    if instance is not None:
                        return instance

                # v4.1.1: For C++, also try to get class from loaded modules directly
                if hasattr(lang_support, '_get_bridge'):
                    bridge = lang_support._get_bridge()
                    if bridge is not None:
                        # Try to get from bridge's instances
                        bridge_instance = bridge.get_instance(instance_name)
                        if bridge_instance is not None:
                            return bridge_instance

                        # For C++: Try to access class from IncludeCPP modules
                        if hasattr(bridge, '_modules'):
                            for mod in bridge._modules.values():
                                if hasattr(mod, instance_name):
                                    cls_or_instance = getattr(mod, instance_name)
                                    # Cache it for future access
                                    lang_support._instances[instance_name] = cls_or_instance
                                    return cls_or_instance

                # Check _instances dict directly as fallback
                if hasattr(lang_support, '_instances'):
                    if instance_name in lang_support._instances:
                        return lang_support._instances[instance_name]

            # Build helpful error message based on language
            if lang_id in ('cpp', 'c++'):
                hint = (f"For C++ access:\n"
                       f"  1. Build your module with 'includecpp build'\n"
                       f"  2. Use cpp.share(\"{instance_name}\", instance) to register\n"
                       f"  3. Or access a class directly: obj = new cpp${instance_name}()")
            elif lang_id in ('java',):
                hint = (f"For Java access:\n"
                       f"  1. Install JPype: pip install jpype1\n"
                       f"  2. Add classpath: java.add_classpath(\"path/to/jar\")\n"
                       f"  3. Load class: MyClass = java.load_class(\"com.example.{instance_name}\")\n"
                       f"  4. Share instance: java.share(\"{instance_name}\", instance)")
            elif lang_id in ('js', 'javascript'):
                hint = (f"For JavaScript access:\n"
                       f"  1. Make sure Node.js is installed\n"
                       f"  2. Define in JS: js.eval(\"function {instance_name}() {{...}}\")\n"
                       f"  3. Share result: js.share(\"{instance_name}\", result)")
            else:
                hint = f"Use '{lang_id}.share(\"{instance_name}\", instance)' to register the instance first."

            raise self._format_error(
                node.line if hasattr(node, 'line') else 0,
                f"Cross-language instance '{lang_id}${instance_name}' not found",
                hint
            )

        if node.type == 'new':
            # Create new instance of a class: new ClassName(args)
            return self._eval_new(node)

        if node.type == 'this_access':
            # this->member access
            return self._eval_this_access(node)

        if node.type == 'type_instantiation':
            # Create new instance of a type: stack<string>, vector<int>, map<K,V>, etc.
            type_name = node.value.get('type')
            element_type = node.value.get('element_type', 'dynamic')
            value_type = node.value.get('value_type')  # For map<K, V>
            init_values = node.value.get('init_values')  # For inline init: map<K,V>{...}

            # Helper to populate container with init values
            def _populate_container(container, init_vals):
                if init_vals and isinstance(init_vals, list):
                    for val_node in init_vals:
                        val = self._evaluate(val_node) if isinstance(val_node, ASTNode) else val_node
                        if hasattr(container, 'push'):
                            container.push(val)
                        elif hasattr(container, 'add'):
                            container.add(val)
                        elif hasattr(container, 'append'):
                            container.append(val)
                return container

            if type_name == 'stack':
                s = Stack(element_type)
                return _populate_container(s, init_values)
            elif type_name == 'vector':
                v = Vector(element_type)
                return _populate_container(v, init_values)
            elif type_name == 'datastruct':
                d = DataStruct(element_type)
                return _populate_container(d, init_values)
            elif type_name == 'shuffled':
                return Shuffled(element_type)
            elif type_name == 'iterator':
                return Iterator(element_type)
            elif type_name == 'combo':
                return Combo(element_type)
            elif type_name == 'dataspace':
                return DataSpace(element_type)
            elif type_name == 'openquote':
                return OpenQuote()
            elif type_name == 'array':
                a = Array(element_type)
                return _populate_container(a, init_values)
            elif type_name == 'list':
                l = List(element_type)
                return _populate_container(l, init_values)
            elif type_name in ('dictionary', 'dict'):
                return Dictionary(element_type)
            elif type_name == 'map':
                # Create Map with key_type and value_type
                m = Map(element_type, value_type or 'dynamic')
                # If inline initialization provided, populate the map
                if init_values:
                    for key, value_node in init_values.items():
                        value = self._evaluate(value_node)
                        m.insert(key, value)
                return m
            elif type_name == 'queue':
                # v4.7: Create Queue with element_type and size
                queue_size = node.value.get('queue_size', 'dynamic')
                q = Queue(element_type, queue_size)
                return _populate_container(q, init_values)
            else:
                return None

        if node.type == 'binary':
            return self._eval_binary(node)

        if node.type == 'unary':
            return self._eval_unary(node)

        # v4.9.3: await expression
        if node.type == 'await':
            return self._exec_await(node)

        # v4.9.3: yield expression (for use in assignments like: received = yield value)
        if node.type == 'yield_expr':
            value = self._evaluate(node.value) if node.value else None
            raise CSSLYield(value)

        # Increment: ++i or i++
        if node.type == 'increment':
            return self._eval_increment(node)

        # Decrement: --i or i--
        if node.type == 'decrement':
            return self._eval_decrement(node)

        if node.type == 'non_null_assert':
            # *$var, *@module, *identifier - safe access, returns 0 if null
            # v4.9.3: Changed from error to safe default (0) for null values
            operand = node.value.get('operand')
            value = self._evaluate(operand)
            if value is None:
                # Return 0 as safe default instead of throwing error
                return 0
            return value

        if node.type == 'non_null_assert_fallback':
            # v4.9.4: *[fallback]variable - returns fallback if variable is null
            # Supports:
            #   *[3]x                              - returns 3 if x is null
            #   *[vector<int> = {0, 2}]x           - returns vector if x is null
            #   *[reflect(%NULLPTR)]x             - returns function result if x is null
            operand = node.value.get('operand')
            fallback_node = node.value.get('fallback')

            # First evaluate the operand
            value = self._evaluate(operand)

            # If not null, return the value
            if value is not None:
                return value

            # Value is null, evaluate and return the fallback
            if fallback_node.type == 'typed_fallback':
                # Handle typed fallback: vector<int> = {0, 2}
                type_name = fallback_node.value.get('type')
                element_type = fallback_node.value.get('element_type')
                init_value = self._evaluate(fallback_node.value.get('init'))

                # Create typed container if needed
                if type_name in ('vector', 'list', 'array'):
                    return list(init_value) if init_value else []
                elif type_name in ('queue', 'stack'):
                    from collections import deque
                    return deque(init_value) if init_value else deque()
                elif type_name in ('set',):
                    return set(init_value) if init_value else set()
                elif type_name in ('dict', 'map', 'json'):
                    return dict(init_value) if init_value else {}
                elif type_name == 'datastruct':
                    # Return as-is for datastruct
                    return init_value
                else:
                    # For other types, just return the init value
                    return init_value
            else:
                # Simple fallback expression
                return self._evaluate(fallback_node)

        if node.type == 'conditional_assert':
            # v4.9.4: [condition]*[fallback]variable - conditional pattern matching
            # Examples:
            #   [null]*[{0}]x              - if x is null, return {0}
            #   [int 2]*[string "2"]x      - if x is int 2, return "2"
            #   [vector<int>]*[{1,2}]x     - if x matches type, use fallback
            condition_node = node.value.get('condition')
            fallback_node = node.value.get('fallback')
            operand = node.value.get('operand')

            # First evaluate the operand
            value = self._evaluate(operand)

            # Check if condition matches
            condition_matches = self._check_condition_pattern(condition_node, value)

            if condition_matches:
                # Condition matched, return fallback
                return self._evaluate_fallback(fallback_node)
            else:
                # Condition didn't match, return original value
                return value

        if node.type == 'type_exclude_assert':
            # *[type]expr - assert value is NOT of excluded type
            exclude_type = node.value.get('exclude_type')
            operand = node.value.get('operand')
            value = self._evaluate(operand)

            # Map CSSL types to Python types
            type_map = {
                'string': str,
                'int': int,
                'float': float,
                'bool': bool,
                'null': type(None),
                'none': type(None),
                'list': list,
                'array': list,
                'dict': dict,
                'json': dict,
            }

            excluded_py_type = type_map.get(exclude_type.lower() if isinstance(exclude_type, str) else exclude_type)
            if excluded_py_type and isinstance(value, excluded_py_type):
                raise self._format_error(
                    node.line if hasattr(node, 'line') else 0,
                    f"Type exclusion assertion failed: value is of excluded type '{exclude_type}'",
                    f"The expression was marked *[{exclude_type}] meaning it must NOT return {exclude_type}, but it did."
                )
            return value

        if node.type == 'call':
            return self._eval_call(node)

        if node.type == 'typed_call':
            # Handle OpenFind<type>(args) style calls
            return self._eval_typed_call(node)

        if node.type == 'member_access':
            return self._eval_member_access(node)

        if node.type == 'index_access':
            return self._eval_index_access(node)

        if node.type == 'array':
            return [self._evaluate(elem) for elem in node.value]

        # v4.9.2: Tuple literals (0, 10) or (a, b, c)
        if node.type == 'tuple':
            return tuple(self._evaluate(elem) for elem in node.value)

        if node.type == 'object':
            return {k: self._evaluate(v) for k, v in node.value.items()}

        if node.type == 'reference':
            # &variable - return a reference object wrapping the actual value
            inner = node.value
            if isinstance(inner, ASTNode):
                if inner.type == 'identifier':
                    # Return a reference wrapper with the variable name
                    return {'__ref__': True, 'name': inner.value, 'value': self.scope.get(inner.value)}
                elif inner.type == 'module_ref':
                    return {'__ref__': True, 'name': inner.value, 'value': self.get_module(inner.value)}
            return {'__ref__': True, 'value': self._evaluate(inner)}

        # Handle action_block - execute and return last expression value
        if node.type == 'action_block':
            return self._evaluate_action_block(node)

        return None

    def _evaluate_action_block(self, node: ASTNode) -> Any:
        """Evaluate an action block and return the last expression's value.

        Used for: v <== { %version; } - captures %version at this moment

        Returns the value of the last expression in the block.
        If the block contains a captured_ref (%name), that's what gets returned.
        """
        last_value = None
        for child in node.children:
            if child.type == 'captured_ref':
                # Direct captured reference - return its value
                last_value = self._evaluate(child)
            elif child.type == 'expression':
                # Expression statement - evaluate and keep value
                last_value = self._evaluate(child.value if hasattr(child, 'value') else child)
            elif child.type == 'identifier':
                # Just an identifier - evaluate it
                last_value = self._evaluate(child)
            elif child.type in ('call', 'member_access', 'binary', 'unary'):
                # Expression types
                last_value = self._evaluate(child)
            else:
                # Execute other statements
                result = self._execute_node(child)
                if result is not None:
                    last_value = result
        return last_value

    def _eval_binary(self, node: ASTNode) -> Any:
        """Evaluate binary operation with auto-casting support"""
        op = node.value.get('op')
        left = self._evaluate(node.value.get('left'))
        right = self._evaluate(node.value.get('right'))

        # === AUTO-CAST FOR STRING OPERATIONS ===
        if op == '+':
            # String concatenation with auto-cast
            if isinstance(left, str) or isinstance(right, str):
                return str(left if left is not None else '') + str(right if right is not None else '')
            # List concatenation
            if isinstance(left, list) and isinstance(right, list):
                result = type(left)(left._element_type) if hasattr(left, '_element_type') else []
                if hasattr(result, 'extend'):
                    result.extend(left)
                    result.extend(right)
                else:
                    result = list(left) + list(right)
                return result
            # Numeric addition
            return (left or 0) + (right or 0)

        if op == '-':
            return self._to_number(left) - self._to_number(right)

        if op == '*':
            # String repeat: "abc" * 3 = "abcabcabc"
            if isinstance(left, str) and isinstance(right, (int, float)):
                return left * int(right)
            if isinstance(right, str) and isinstance(left, (int, float)):
                return right * int(left)
            return self._to_number(left) * self._to_number(right)

        if op == '/':
            r = self._to_number(right)
            if r == 0:
                raise CSSLRuntimeError("Division by zero")
            return self._to_number(left) / r

        if op == '//':
            r = self._to_number(right)
            if r == 0:
                raise CSSLRuntimeError("Integer division by zero")
            return self._to_number(left) // r

        if op == '%':
            r = self._to_number(right)
            if r == 0:
                raise CSSLRuntimeError("Modulo by zero")
            return self._to_number(left) % r

        if op == '**':
            return self._to_number(left) ** self._to_number(right)

        # === COMPARISON OPERATIONS ===
        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            return self._compare(left, right) < 0
        if op == '>':
            return self._compare(left, right) > 0
        if op == '<=':
            return self._compare(left, right) <= 0
        if op == '>=':
            return self._compare(left, right) >= 0

        # === LOGICAL OPERATIONS ===
        if op == 'and' or op == '&&':
            return left and right
        if op == 'or' or op == '||':
            return left or right

        # === BITWISE OPERATIONS (or stream/pipe operations) ===
        if op == '&':
            return int(left or 0) & int(right or 0)
        if op == '|':
            # v4.8.4: Pipe operator support
            from .cssl_types import Pipe, OutputStream, InputStream, FileStream
            if isinstance(left, Pipe):
                if callable(right):
                    return left | right
                return Pipe(left._data)
            # If right is a Pipe transform function
            if callable(right) and hasattr(right, '__name__') and 'pipe' in str(type(right)):
                return Pipe(left) | right
            # Bitwise OR for integers
            return int(left or 0) | int(right or 0)
        if op == '^':
            return int(left or 0) ^ int(right or 0)
        if op == '<<':
            # v4.8.4: Stream output operator support
            from .cssl_types import OutputStream, FileStream
            if isinstance(left, (OutputStream, FileStream)):
                # Handle manipulators
                if isinstance(right, dict) and right.get('type') == 'manipulator':
                    name = right.get('name')
                    value = right.get('value')
                    if name == 'setprecision':
                        left.setprecision(value)
                    elif name == 'setw':
                        left.setw(value)
                    elif name == 'setfill':
                        left.setfill(value)
                    elif name == 'fixed':
                        left.fixed()
                    elif name == 'scientific':
                        left.scientific()
                    return left
                # Stream output
                return left.write(right)
            # Bitwise left shift for integers
            return int(left or 0) << int(right or 0)
        if op == '>>':
            # v4.8.4: Stream input operator support
            from .cssl_types import InputStream, FileStream
            if isinstance(left, (InputStream, FileStream)):
                # Read from stream into target type
                if isinstance(right, type):
                    return left.read(right)
                return left.read(str)
            # Bitwise right shift for integers
            return int(left or 0) >> int(right or 0)

        # === IN OPERATOR (v4.8.4: C++ optimized with unative fallback) ===
        if op == 'in':
            if right is None:
                return False
            # Check if unative mode is requested (use Python's native 'in')
            use_native = node.value.get('unative', False)
            if use_native:
                return left in right
            # C++ optimized containment check
            return self._contains_fast(right, left)

        # === NOT IN OPERATOR ===
        if op == 'not in' or op == '!in' or op == 'notin':
            if right is None:
                return True
            use_native = node.value.get('unative', False)
            if use_native:
                return left not in right
            return not self._contains_fast(right, left)

        return None

    def _to_number(self, value: Any) -> Union[int, float]:
        """Convert value to number with auto-casting"""
        if value is None:
            return 0
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return 0
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except ValueError:
                return 0
        if isinstance(value, bool):
            return 1 if value else 0
        if isinstance(value, (list, tuple)):
            return len(value)
        return 0

    def _compare(self, left: Any, right: Any) -> int:
        """Compare two values with auto-casting, returns -1, 0, or 1"""
        # Handle None
        if left is None and right is None:
            return 0
        if left is None:
            return -1
        if right is None:
            return 1

        # Both strings - compare as strings
        if isinstance(left, str) and isinstance(right, str):
            if left < right:
                return -1
            elif left > right:
                return 1
            return 0

        # Both numbers - compare as numbers
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if left < right:
                return -1
            elif left > right:
                return 1
            return 0

        # Mixed types - try to convert to numbers
        try:
            l = self._to_number(left)
            r = self._to_number(right)
            if l < r:
                return -1
            elif l > r:
                return 1
            return 0
        except (ValueError, TypeError):
            # Fallback to string comparison
            l_str = str(left)
            r_str = str(right)
            if l_str < r_str:
                return -1
            elif l_str > r_str:
                return 1
            return 0

    def _contains_fast(self, container: Any, item: Any) -> bool:
        """C++ optimized containment check (v4.8.4).

        Uses optimized algorithms based on container type:
        - Hash-based (dict, set): O(1) lookup
        - Sorted data: Binary search O(log n)
        - Linear: O(n) with early termination
        """
        from .cssl_types import Vector, Array, List, Dictionary, Map, DataStruct

        # Hash-based containers - O(1)
        if isinstance(container, (dict, set, frozenset)):
            return item in container
        if isinstance(container, (Dictionary, Map)):
            if hasattr(container, 'contains'):
                return container.contains(item)
            return item in container

        # For list-like containers, check if sorted and use binary search
        if isinstance(container, (list, tuple, Vector, Array, List, DataStruct)):
            data = list(container) if not isinstance(container, list) else container

            # For larger collections, check if sorted and use binary search
            if len(data) > 10:
                # Quick sorted check on sample
                sample_size = min(10, len(data))
                step = max(1, len(data) // sample_size)
                sample = [data[i] for i in range(0, len(data), step)][:sample_size]

                try:
                    is_sorted = all(sample[i] <= sample[i+1] for i in range(len(sample)-1))
                    if is_sorted:
                        # Binary search for sorted data
                        import bisect
                        idx = bisect.bisect_left(data, item)
                        return idx < len(data) and data[idx] == item
                except (TypeError, AttributeError):
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

    def _eval_unary(self, node: ASTNode) -> Any:
        """Evaluate unary operation"""
        op = node.value.get('op')
        operand = self._evaluate(node.value.get('operand'))

        if op == 'not':
            return not operand
        if op == '-':
            return -operand

        return None

    def _eval_increment(self, node: ASTNode) -> Any:
        """Evaluate increment operation (++i or i++)"""
        op_type = node.value.get('op')  # 'prefix' or 'postfix'
        operand = node.value.get('operand')

        # Get variable name
        var_name = None
        if isinstance(operand, ASTNode):
            if operand.type == 'identifier':
                var_name = operand.value
            elif operand.type == 'shared_ref':
                # Handle $var++
                var_name = operand.value
                current = self.shared_vars.get(var_name, 0)
                if op_type == 'prefix':
                    self.shared_vars[var_name] = current + 1
                    return current + 1
                else:  # postfix
                    self.shared_vars[var_name] = current + 1
                    return current

        if var_name:
            current = self.scope.get(var_name, 0)
            if op_type == 'prefix':
                # ++i: increment then return
                self.scope.set(var_name, current + 1)
                return current + 1
            else:
                # i++: return then increment
                self.scope.set(var_name, current + 1)
                return current

        return None

    def _eval_decrement(self, node: ASTNode) -> Any:
        """Evaluate decrement operation (--i or i--)"""
        op_type = node.value.get('op')  # 'prefix' or 'postfix'
        operand = node.value.get('operand')

        # Get variable name
        var_name = None
        if isinstance(operand, ASTNode):
            if operand.type == 'identifier':
                var_name = operand.value
            elif operand.type == 'shared_ref':
                # Handle $var--
                var_name = operand.value
                current = self.shared_vars.get(var_name, 0)
                if op_type == 'prefix':
                    self.shared_vars[var_name] = current - 1
                    return current - 1
                else:  # postfix
                    self.shared_vars[var_name] = current - 1
                    return current

        if var_name:
            current = self.scope.get(var_name, 0)
            if op_type == 'prefix':
                # --i: decrement then return
                self.scope.set(var_name, current - 1)
                return current - 1
            else:
                # i--: return then decrement
                self.scope.set(var_name, current - 1)
                return current

        return None

    def _check_condition_pattern(self, condition_node: ASTNode, value: Any) -> bool:
        """Check if a value matches a condition pattern.

        v4.9.4: Used by [condition]*[fallback] syntax.
        """
        if condition_node.type == 'condition_null':
            # [null]*[fallback] - matches if value is None
            return value is None

        elif condition_node.type == 'condition_type':
            # [vector<int>]*[fallback] - matches if value is of type
            type_name = condition_node.value.get('type')
            return self._value_matches_type(value, type_name)

        elif condition_node.type == 'condition_type_value':
            # [int 2]*[fallback] - matches if value is int AND equals 2
            type_name = condition_node.value.get('type')
            match_value = self._evaluate(condition_node.value.get('match_value'))

            if not self._value_matches_type(value, type_name):
                return False
            return value == match_value

        elif condition_node.type == 'condition_typed_pattern':
            # [vector<int> = {1,2}]*[fallback] - matches exact pattern
            type_name = condition_node.value.get('type')
            pattern_value = self._evaluate(condition_node.value.get('pattern'))

            if not self._value_matches_type(value, type_name):
                return False
            return value == pattern_value

        else:
            # Generic expression condition - evaluate and compare
            condition_value = self._evaluate(condition_node)
            return value == condition_value

    def _value_matches_type(self, value: Any, type_name: str) -> bool:
        """Check if a value matches a CSSL type name."""
        type_map = {
            'int': (int,),
            'float': (float, int),
            'string': (str,),
            'bool': (bool,),
            'list': (list,),
            'array': (list,),
            'vector': (list,),
            'dict': (dict,),
            'map': (dict,),
            'json': (dict,),
            'null': (type(None),),
            'none': (type(None),),
        }

        py_types = type_map.get(type_name.lower())
        if py_types:
            return isinstance(value, py_types)

        # For unknown types, check class name
        if hasattr(value, '__class__'):
            return value.__class__.__name__.lower() == type_name.lower()

        return False

    def _evaluate_fallback(self, fallback_node: ASTNode) -> Any:
        """Evaluate a fallback value node."""
        if fallback_node.type == 'typed_fallback':
            # Handle typed fallback: vector<int> = {0, 2}
            type_name = fallback_node.value.get('type')
            init_value = self._evaluate(fallback_node.value.get('init'))

            # Create typed container if needed
            if type_name in ('vector', 'list', 'array'):
                return list(init_value) if init_value else []
            elif type_name in ('queue', 'stack'):
                from collections import deque
                return deque(init_value) if init_value else deque()
            elif type_name in ('set',):
                return set(init_value) if init_value else set()
            elif type_name in ('dict', 'map', 'json'):
                return dict(init_value) if init_value else {}
            else:
                return init_value
        else:
            # Simple fallback expression
            return self._evaluate(fallback_node)

    def _eval_call(self, node: ASTNode) -> Any:
        """Evaluate function call with optional named arguments"""
        callee_node = node.value.get('callee')
        args = [self._evaluate(a) for a in node.value.get('args', [])]

        # Evaluate named arguments (kwargs)
        kwargs_raw = node.value.get('kwargs', {})
        kwargs = {k: self._evaluate(v) for k, v in kwargs_raw.items()} if kwargs_raw else {}

        # v4.9.3: Handle ?FuncName() - call function and handle pointer result
        if isinstance(callee_node, ASTNode) and callee_node.type == 'pointer_ref':
            from .cssl_types import Address
            func_name = callee_node.value
            # Check if this is a function (not a variable)
            func = self.scope.get(func_name) or self.global_scope.get(func_name)
            if func is None:
                func = self.builtins.get(func_name)

            # If it's a function, call it
            if callable(func) or (isinstance(func, ASTNode) and func.type == 'function'):
                if callable(func):
                    result = func(*args, **kwargs) if kwargs else func(*args)
                else:
                    result = self._call_function(func, args, kwargs)
                # If result is already an Address, dereference it
                if isinstance(result, Address):
                    return result.reflect()
                # Otherwise return pointer to the result
                return Address(obj=result)

        # Get function name for injection check FIRST (before evaluating callee)
        func_name = None
        if isinstance(callee_node, ASTNode):
            if callee_node.type == 'identifier':
                func_name = callee_node.value
            elif callee_node.type == 'member_access':
                func_name = callee_node.value.get('member')

        # Check if function has injections
        has_injections = func_name and func_name in self._function_injections
        is_replaced = func_name and self._function_replaced.get(func_name, False)

        # If function is FULLY REPLACED (<<==), run injection and skip original
        # This allows creating new functions via infusion: new_func <<== { ... }
        if is_replaced:
            self._execute_function_injections(func_name)
            return None  # Injection ran, don't try to find original

        # Now evaluate the callee (only if not replaced)
        callee = self._evaluate(callee_node)

        # Execute added injections (+<<==) before original
        if has_injections and not is_replaced:
            self._execute_function_injections(func_name)

        # Execute original function
        if callable(callee):
            if kwargs:
                return callee(*args, **kwargs)
            return callee(*args)

        if isinstance(callee, ASTNode) and callee.type == 'function':
            return self._call_function(callee, args, kwargs)

        # Extract callee name for error messages
        if isinstance(callee_node, ASTNode) and hasattr(callee_node, 'value'):
            val = callee_node.value
            if isinstance(val, str):
                callee_name = val
            elif isinstance(val, dict):
                # For member access nodes like obj.method, get the member name
                if 'member' in val:
                    obj_node = val.get('object')
                    member = val.get('member')
                    obj_name = obj_node.value if isinstance(obj_node, ASTNode) else str(obj_node)
                    callee_name = f"{obj_name}.{member}"
                # For call nodes, try to get the callee name
                elif 'callee' in val:
                    callee_val = val.get('callee')
                    if isinstance(callee_val, ASTNode):
                        callee_name = callee_val.value if isinstance(callee_val.value, str) else str(callee_val.value)
                    else:
                        callee_name = str(callee_val)
                elif 'name' in val:
                    callee_name = str(val.get('name'))
                else:
                    callee_name = str(val)
            else:
                callee_name = str(val)
        else:
            callee_name = str(callee_node)

        # Build detailed error with suggestions
        available_funcs = _get_available_functions(self.scope, self.global_scope, self.builtins)
        similar = _find_similar_names(callee_name, available_funcs)

        if callee is None:
            # Function not found at all
            if similar:
                hint = f"Did you mean: {', '.join(similar)}?"
            else:
                hint = f"Function '{callee_name}' is not defined. Define it with: define {callee_name}() {{ }}"
            raise self._format_error(
                node.line,
                f"Function '{callee_name}' not found",
                hint
            )
        else:
            # Found something but it's not callable
            if similar:
                hint = f"'{callee_name}' is a {type(callee).__name__}, not a function. Did you mean: {', '.join(similar)}?"
            else:
                hint = f"'{callee_name}' is a {type(callee).__name__}. Functions must be defined with 'define' keyword."
            raise self._format_error(
                node.line,
                f"Cannot call '{callee_name}' - it is not a function",
                hint
            )

    def _eval_typed_call(self, node: ASTNode) -> Any:
        """Evaluate typed function call like OpenFind<string>(0) or OpenFind<dynamic, "name">"""
        name = node.value.get('name')
        type_param = node.value.get('type_param', 'dynamic')
        param_name = node.value.get('param_name')  # For OpenFind<type, "name">
        args = [self._evaluate(a) for a in node.value.get('args', [])]

        # Handle OpenFind<type>(index) or OpenFind<type, "name">
        if name == 'OpenFind':
            # OpenFind searches for a value of the specified type
            # from the open parameters in scope
            open_params = self.scope.get('Params') or []
            open_kwargs = self.scope.get('_OpenKwargs') or {}

            # Type mapping for type checking
            type_map = {
                'string': str, 'str': str,
                'int': int, 'integer': int,
                'float': float, 'double': float,
                'bool': bool, 'boolean': bool,
                'list': list, 'array': list,
                'dict': dict, 'json': dict,
                'dynamic': None,  # Accept any type
            }
            target_type = type_map.get(type_param.lower())

            # If param_name is specified, search by name in kwargs
            # OpenFind<dynamic, "tasks"> -> searches for MyFunc(tasks="value")
            if param_name:
                if param_name in open_kwargs:
                    value = open_kwargs[param_name]
                    # Type check if not dynamic
                    if target_type is None or isinstance(value, target_type):
                        return value
                return None

            # Otherwise, search by index in positional args
            index = args[0] if args else 0

            if isinstance(open_params, (list, tuple)):
                # Find first matching type starting from index
                for i in range(index, len(open_params)):
                    if target_type is None or isinstance(open_params[i], target_type):
                        return open_params[i]
                # Also search before index
                for i in range(0, min(index, len(open_params))):
                    if target_type is None or isinstance(open_params[i], target_type):
                        return open_params[i]

            return None

        # v4.9.2: Handle cast<type>(value) - type casting
        if name == 'cast':
            if not args:
                raise CSSLRuntimeError(
                    "cast<type>(value) requires a value argument",
                    node.line,
                    hint="Usage: cast<int>(3.14) or cast<string>(42)"
                )
            value = args[0]
            target_type = type_param.lower()

            try:
                if target_type in ('int', 'integer'):
                    return int(value)
                elif target_type in ('float', 'double'):
                    return float(value)
                elif target_type in ('string', 'str'):
                    return str(value)
                elif target_type in ('bool', 'boolean'):
                    if isinstance(value, str):
                        return value.lower() not in ('', '0', 'false', 'no', 'null', 'none')
                    return bool(value)
                elif target_type in ('list', 'array'):
                    if isinstance(value, (list, tuple)):
                        return list(value)
                    return [value]
                elif target_type in ('dict', 'json'):
                    if isinstance(value, dict):
                        return value
                    return {'value': value}
                elif target_type == 'dynamic':
                    return value  # No conversion
                else:
                    raise CSSLRuntimeError(
                        f"Unknown cast type: {target_type}",
                        node.line,
                        hint="Supported types: int, float, string, bool, list, dict, dynamic"
                    )
            except (ValueError, TypeError) as e:
                raise CSSLRuntimeError(
                    f"Cannot cast {type(value).__name__} to {target_type}: {e}",
                    node.line
                )

        # Fallback: call as regular function with type hint
        func = self.builtins.get_function(name)
        if func and callable(func):
            return func(type_param, *args)

        raise CSSLRuntimeError(
            f"Unknown typed function: {name}<{type_param}>",
            node.line,
            context=f"Available typed functions: OpenFind<type>, cast<type>",
            hint="Use cast<int>(value), cast<string>(value), etc."
        )

    def _eval_new(self, node: ASTNode) -> CSSLInstance:
        """Evaluate 'new ClassName(args)' or 'new @ClassName(args)' or 'new Namespace::ClassName(args)' expression.

        Creates a new instance of a CSSL class and calls its constructor.
        Supports multiple constructors (constr keyword), class parameters,
        and automatic parent constructor calling.

        With '@' prefix (new @ClassName), looks only in global scope.
        With Namespace:: prefix, looks in the namespace dict first.
        """
        class_name = node.value.get('class')
        namespace = node.value.get('namespace')  # v4.2.6: Namespace::ClassName support
        is_global_ref = node.value.get('is_global_ref', False)
        args = [self._evaluate(arg) for arg in node.value.get('args', [])]
        kwargs = {k: self._evaluate(v) for k, v in node.value.get('kwargs', {}).items()}

        class_def = None

        # v4.2.6: Handle Namespace::ClassName lookup
        if namespace:
            # Look up namespace first
            ns_obj = self.scope.get(namespace)
            if ns_obj is None:
                ns_obj = self.global_scope.get(namespace)
            # v4.8: Handle CSSLNamespace objects
            if isinstance(ns_obj, CSSLNamespace):
                class_def = ns_obj.classes.get(class_name)
            elif isinstance(ns_obj, dict) and class_name in ns_obj:
                class_def = ns_obj[class_name]

        # Get class definition from scope (if not found in namespace)
        if class_def is None:
            if is_global_ref:
                # With @ prefix, only look in global scope
                class_def = self._promoted_globals.get(class_name)
                if class_def is None:
                    class_def = self.global_scope.get(class_name)
            else:
                # Normal lookup: local scope first, then global
                class_def = self.scope.get(class_name)
                if class_def is None:
                    class_def = self.global_scope.get(class_name)

        if class_def is None:
            # Build detailed error with suggestions
            source_line = self._get_source_line(node.line)
            available_classes = _get_available_classes(self.scope, self.global_scope, self._promoted_globals)
            similar = _find_similar_names(class_name, available_classes)

            # Check if class exists in global scope (user forgot @)
            global_class = self._promoted_globals.get(class_name) or self.global_scope.get(class_name)
            if global_class and isinstance(global_class, CSSLClass) and not is_global_ref:
                hint = f"Class '{class_name}' exists in global scope. Use: new @{class_name}()"
            elif similar:
                hint = f"Did you mean: {', '.join(similar)}?"
            elif available_classes:
                hint = f"Available classes: {', '.join(available_classes[:5])}"
            else:
                hint = "Define the class before instantiation, or use 'global class' / 'class @Name' for global classes"

            context = f"in expression: {source_line.strip()}" if source_line else None
            raise self._format_error(
                node.line,
                f"Class '{class_name}' not found",
                hint
            )

        # If we got a variable that holds a class reference, use that class
        if not isinstance(class_def, CSSLClass):
            # Check if it's a variable holding a class (dynamic class instantiation)
            if hasattr(class_def, '__class__') and isinstance(class_def, CSSLClass):
                pass  # Already a CSSLClass, continue
            elif isinstance(class_def, dict) and 'class_def' in class_def:
                # Injected class reference from +<== operator
                class_def = class_def['class_def']
            elif isinstance(class_def, type):
                # v4.9.6: Support Python classes with 'new' keyword
                # This allows: new CsslWidget("title", 400, 300)
                try:
                    return class_def(*args, **kwargs)
                except Exception as e:
                    raise CSSLRuntimeError(
                        f"Failed to instantiate Python class '{class_name}': {e}",
                        node.line
                    )
            else:
                # Not a class - show error
                raise CSSLRuntimeError(
                    f"'{class_name}' is not a class",
                    node.line,
                    hint=f"'{class_name}' is of type {type(class_def).__name__}"
                )

        if not isinstance(class_def, CSSLClass):
            raise CSSLRuntimeError(
                f"'{class_name}' is not a class",
                node.line,
                hint=f"'{class_name}' is of type {type(class_def).__name__}"
            )

        # v4.2.5: Deferred &target replacement for non-embedded classes
        # Apply on first instantiation if pending
        if hasattr(class_def, '_pending_target') and class_def._pending_target:
            pending = class_def._pending_target
            self._overwrite_class_target(
                pending['append_ref_class'],
                pending.get('append_ref_member'),
                class_def
            )
            class_def._target_applied = True
            class_def._pending_target = None  # Clear pending

        # Create new instance
        instance = CSSLInstance(class_def)

        # Store parent class reference for super() calls
        instance._parent_class = class_def.parent
        instance._parent_constructor_called = False

        # Get class params and extends args
        class_params = getattr(class_def, 'class_params', [])
        extends_args = getattr(class_def, 'extends_args', [])
        constructors = getattr(class_def, 'constructors', [])

        # Bind class_params to instance scope (they receive values from constructor args)
        # These are the implicit constructor parameters defined in class declaration
        # v4.9.4: Also check kwargs for named class params like: new Engine(debug=true)
        param_values = {}
        for i, param in enumerate(class_params):
            param_name = param.get('name') if isinstance(param, dict) else param
            if i < len(args):
                param_values[param_name] = args[i]
            elif param_name in kwargs:
                param_values[param_name] = kwargs[param_name]
            else:
                param_values[param_name] = None

        # Call parent constructor with extends_args if parent exists and args specified
        if class_def.parent and extends_args:
            evaluated_extends_args = [self._evaluate(arg) for arg in extends_args]
            self._call_parent_constructor(instance, evaluated_extends_args)
            instance._parent_constructor_called = True

        # v4.8.8: Separate constructors by modifier type
        regular_constructors = []
        secure_constructors = []
        callable_constructors = []

        for constr in constructors:
            constr_info = constr.value
            if constr_info.get('is_secure'):
                secure_constructors.append(constr)
            elif constr_info.get('is_callable'):
                callable_constructors.append(constr)
            else:
                regular_constructors.append(constr)

        # Store callable constructors on instance for manual invocation
        instance._callable_constructors = callable_constructors
        instance._secure_constructors = secure_constructors

        # Execute regular constructors (not callable, not secure)
        # Wrap in try/except to call secure constructors on exception
        try:
            for constr in regular_constructors:
                self._call_constructor(instance, constr, args, kwargs, param_values)

            # Call primary constructor (old-style) if defined
            if class_def.constructor:
                self._call_method(instance, class_def.constructor, args, kwargs)
        except Exception as e:
            # v4.8.8: Call all secure constructors on exception
            for secure_constr in secure_constructors:
                try:
                    self._call_constructor(instance, secure_constr, args, kwargs, param_values)
                except:
                    pass  # Secure constructor failed, continue with others
            raise  # Re-raise the original exception

        return instance

    def _call_parent_constructor(self, instance: CSSLInstance, args: list, kwargs: dict = None):
        """Call the parent class constructor on an instance.

        Used for automatic parent constructor calling and super() calls.
        """
        kwargs = kwargs or {}
        parent = instance._parent_class

        if parent is None:
            return

        from .cssl_builtins import CSSLizedPythonObject

        if isinstance(parent, CSSLClass):
            # CSSL parent class
            if parent.constructor:
                self._call_method(instance, parent.constructor, args, kwargs)
            # Also call parent's constr constructors
            for constr in getattr(parent, 'constructors', []):
                self._call_constructor(instance, constr, args, kwargs, {})
        elif isinstance(parent, CSSLizedPythonObject):
            # Python parent - call __init__ if it's a class
            py_obj = parent.get_python_obj()
            if isinstance(py_obj, type):
                # It's a class - we need to initialize it
                try:
                    py_obj.__init__(instance, *args, **kwargs)
                except TypeError:
                    pass  # Initialization might not be needed
        elif isinstance(parent, type):
            # Raw Python class
            try:
                parent.__init__(instance, *args, **kwargs)
            except TypeError:
                pass

    def _execute_append_reference(self, instance: CSSLInstance, ref_class: str, ref_member: str,
                                   args: list, kwargs: dict, param_values: dict, is_constructor: bool = True):
        """Execute referenced parent constructor/method for append mode (++).

        Resolves the class/instance reference and executes the specified member.
        Supports:
        - Static class references: &ClassName::member
        - Dynamic instance references: &$instanceVar::member
        - Direct function references: &FunctionName (for define functions)

        Args:
            instance: Current class instance (can be None for standalone functions)
            ref_class: Referenced class name, $instanceVar, or function name
            ref_member: Member name (constructor name, 'constructors', or method name) - can be None
            args: Arguments to pass
            kwargs: Keyword arguments to pass
            param_values: Parameter values from class params
            is_constructor: True if looking for constructor, False for method
        """
        from .cssl_builtins import CSSLizedPythonObject

        # v4.9.2: Handle &builtinName ++ syntax (stored as __builtins__::builtinName)
        if ref_class == '__builtins__' and ref_member:
            ref_class = ref_member
            ref_member = None

        # Handle direct function reference: &FunctionName ++ (no ::member part)
        if ref_member is None and not is_constructor:
            # ref_class is actually a function name
            func_name = ref_class
            if func_name.startswith('$'):
                func_name = func_name[1:]

            # v4.9.2: For builtin hooks, check _original_functions FIRST to avoid infinite recursion
            # When &builtin ++ is used, scope contains the wrapper, but we want the original
            func = None
            if hasattr(self, '_original_functions'):
                func = self._original_functions.get(func_name)

            # If not an overwritten builtin, check scope
            if func is None:
                func = self.scope.get(func_name) or self.global_scope.get(func_name)

            # v4.9.2: Check in builtins._functions if still not found (for non-overwritten builtins)
            if func is None and hasattr(self, 'builtins') and hasattr(self.builtins, '_functions'):
                func = self.builtins._functions.get(func_name)

            if func is not None:
                if isinstance(func, ASTNode) and func.type in ('function', 'FUNCTION'):
                    # Execute the referenced function
                    if instance:
                        self._call_method(instance, func, args, kwargs)
                    else:
                        self._call_function(func, args, kwargs)
                elif callable(func):
                    # It's a callable (Python function or lambda)
                    func(*args, **kwargs)
            return

        # Resolve the class/instance reference
        if ref_class.startswith('$'):
            # Dynamic instance reference: &$instanceVar::member or &$PyObject.method
            var_name = ref_class[1:]

            # First check in _live_objects for Python shared objects
            from ..cssl_bridge import _live_objects, SharedObjectProxy
            ref_obj = _live_objects.get(var_name)
            if ref_obj is None:
                ref_obj = self.scope.get(var_name) or self.global_scope.get(var_name)

            if ref_obj is None:
                return  # Instance not found, skip silently

            # Handle Python shared objects
            if isinstance(ref_obj, SharedObjectProxy):
                ref_obj = ref_obj._obj

            # If it's a Python object (not CSSL), call the method directly
            if not isinstance(ref_obj, (CSSLInstance, CSSLClass)):
                if ref_member and hasattr(ref_obj, ref_member):
                    method = getattr(ref_obj, ref_member)
                    if callable(method):
                        try:
                            method(*args, **kwargs)
                        except TypeError:
                            # Try without args
                            method()
                return

            if isinstance(ref_obj, CSSLInstance):
                # Get the class definition from the instance
                target_class = ref_obj.class_def
            elif isinstance(ref_obj, CSSLClass):
                target_class = ref_obj
            else:
                return  # Not a valid reference
        else:
            # Static class reference: &ClassName::member
            target_class = self.scope.get(ref_class) or self.global_scope.get(ref_class)

        if target_class is None:
            return  # Class not found, skip silently

        # Handle different target types
        if isinstance(target_class, CSSLInstance):
            # Referenced an instance variable directly
            target_class = target_class.class_def

        if not isinstance(target_class, CSSLClass):
            return  # Not a CSSL class

        # Find and execute the referenced member
        if is_constructor:
            # Looking for a constructor
            if ref_member == 'constructors' or ref_member is None:
                # Execute all constructors from the referenced class
                for constr in getattr(target_class, 'constructors', []):
                    self._call_constructor(instance, constr, args, kwargs, param_values)
            else:
                # Execute specific constructor by name
                for constr in getattr(target_class, 'constructors', []):
                    if constr.value.get('name') == ref_member:
                        self._call_constructor(instance, constr, args, kwargs, param_values)
                        break
        else:
            # Looking for a method (define function)
            if ref_member:
                # Find method in class
                for member in getattr(target_class, 'members', []):
                    if member.type in ('function', 'FUNCTION') and member.value.get('name') == ref_member:
                        self._call_method(instance, member, args, kwargs)
                        break
                # Also check in methods dict if available
                methods = getattr(target_class, 'methods', {})
                if ref_member in methods:
                    method_node = methods[ref_member]
                    self._call_method(instance, method_node, args, kwargs)

    def _call_constructor(self, instance: CSSLInstance, constr_node: ASTNode,
                          args: list, kwargs: dict, param_values: dict):
        """Call a constructor defined with 'constr' keyword.

        Handles constructor extends/overwrites and sets up the instance scope.
        Supports append mode (++) for keeping parent code and adding new code.
        """
        constr_info = constr_node.value
        constr_params = constr_info.get('params', [])
        extends_class = constr_info.get('extends_class')
        extends_method = constr_info.get('extends_method')

        # Append mode: ++ operator for keeping parent code + adding new
        append_mode = constr_info.get('append_mode', False)
        append_ref_class = constr_info.get('append_ref_class')  # &ClassName or &$instanceVar
        append_ref_member = constr_info.get('append_ref_member')  # ::constructorName or ::methodName

        # Save previous instance context
        prev_instance = self._current_instance
        self._current_instance = instance

        # Create new scope for constructor
        new_scope = Scope(parent=self.scope)

        # Bind param_values (from class params) to constructor scope
        for name, value in param_values.items():
            new_scope.set(name, value)

        # Bind constructor parameters
        for i, param in enumerate(constr_params):
            param_name = param.get('name') if isinstance(param, dict) else param
            if i < len(args):
                new_scope.set(param_name, args[i])
            elif param_name in kwargs:
                new_scope.set(param_name, kwargs[param_name])
            else:
                new_scope.set(param_name, None)

        # If constructor extends another constructor, inherit its local vars
        if extends_class and extends_method:
            parent_class = self.scope.get(extends_class) or self.global_scope.get(extends_class)
            if parent_class and isinstance(parent_class, CSSLClass):
                for constr in getattr(parent_class, 'constructors', []):
                    if constr.value.get('name') == extends_method:
                        # Execute parent constructor first to get local vars
                        self._call_constructor(instance, constr, args, kwargs, param_values)
                        break

        # Handle append mode (++) - execute referenced parent member first
        if append_mode and append_ref_class:
            self._execute_append_reference(
                instance, append_ref_class, append_ref_member,
                args, kwargs, param_values, is_constructor=True
            )

        # Execute constructor body
        prev_scope = self.scope
        self.scope = new_scope

        # v4.8.8: Set 'this' and 'super' in constructor scope
        new_scope.set('this', instance)
        parent_class = getattr(instance, '_parent_class', None)
        if parent_class is None and hasattr(instance, '_class'):
            parent_class = getattr(instance._class, 'parent', None)
        if parent_class:
            new_scope.set('super', SuperProxy(instance, parent_class, self))

        try:
            for stmt in constr_node.children:
                self._execute_node(stmt)
        finally:
            self.scope = prev_scope
            self._current_instance = prev_instance

    def _call_destructor(self, instance: CSSLInstance, destr_node: ASTNode):
        """v4.8.8: Call a destructor on an instance.

        Destructors are defined with constr ~Name() { } syntax.
        They are called by delete(instance) or delete(instance, "Name").

        Args:
            instance: The CSSLInstance to clean up
            destr_node: The destructor AST node
        """
        # Save previous instance context
        prev_instance = self._current_instance
        self._current_instance = instance

        # Create new scope for destructor
        new_scope = Scope(parent=self.scope)
        prev_scope = self.scope
        self.scope = new_scope

        # v4.8.8: Set 'this' and 'super' in destructor scope
        new_scope.set('this', instance)
        parent_class = getattr(instance, '_parent_class', None)
        if parent_class is None and hasattr(instance, '_class'):
            parent_class = getattr(instance._class, 'parent', None)
        if parent_class:
            new_scope.set('super', SuperProxy(instance, parent_class, self))

        try:
            # Execute destructor body
            for child in destr_node.children:
                self._execute_node(child)
        finally:
            self.scope = prev_scope
            self._current_instance = prev_instance

    def _eval_this_access(self, node: ASTNode) -> Any:
        """Evaluate 'this->member' access.

        Returns the value of a member from the current class instance.
        """
        if self._current_instance is None:
            raise CSSLRuntimeError(
                "'this' used outside of class method context",
                node.line if hasattr(node, 'line') else 0,
                hint="'this->' can only be used inside class methods"
            )

        member = node.value.get('member')

        # Check if it's a chained access (this->a->b)
        if 'object' in node.value:
            # First evaluate the object part
            obj = self._evaluate(node.value.get('object'))
            if obj is None:
                return None
            if hasattr(obj, member):
                return getattr(obj, member)
            if isinstance(obj, dict):
                return obj.get(member)
            return None

        # Direct this->member access
        instance = self._current_instance

        # Check if instance is a CSSL instance or a plain Python object
        is_cssl_instance = hasattr(instance, 'has_member') and hasattr(instance, 'has_method')

        if is_cssl_instance:
            # CSSL instance - use CSSL methods
            if instance.has_member(member):
                return instance.get_member(member)

            # Check if it's a method
            if instance.has_method(member):
                # Return a callable that will invoke the method with instance context
                method_node = instance.get_method(member)
                # Check if this is an inherited Python method
                if isinstance(method_node, tuple) and method_node[0] == 'python_method':
                    python_method = method_node[1]
                    return lambda *args, **kwargs: python_method(*args, **kwargs)
                return lambda *args, **kwargs: self._call_method(instance, method_node, list(args), kwargs)
        else:
            # Plain Python object - use standard attribute access
            if hasattr(instance, member):
                return getattr(instance, member)
            # Also check __dict__ for dynamic attributes
            if hasattr(instance, '__dict__') and member in instance.__dict__:
                return instance.__dict__[member]

        # Build helpful error with available members
        if is_cssl_instance:
            class_name = instance._class.name
            available_members = list(instance._members.keys()) if hasattr(instance, '_members') else []
            available_methods = list(instance._methods.keys()) if hasattr(instance, '_methods') else []
        else:
            class_name = type(instance).__name__
            available_members = [k for k in dir(instance) if not k.startswith('_')]
            available_methods = []
        all_available = available_members + available_methods
        similar = _find_similar_names(member, all_available)

        if similar:
            hint = f"Did you mean: {', '.join(similar)}?"
        elif all_available:
            hint = f"Available: {', '.join(all_available[:5])}"
        else:
            hint = f"Class '{class_name}' has no accessible members. Check class definition."

        raise self._format_error(
            node.line if hasattr(node, 'line') else 0,
            f"'{class_name}' has no member or method '{member}'",
            hint
        )

    def _call_method(self, instance: CSSLInstance, method_node: ASTNode, args: list, kwargs: dict = None) -> Any:
        """Call a method on an instance with 'this' context.

        Sets up the instance as the current 'this' context and executes the method.
        Supports append mode (++) for keeping parent code and adding new code.
        """
        kwargs = kwargs or {}
        func_info = method_node.value
        params = func_info.get('params', [])
        modifiers = func_info.get('modifiers', [])

        # Append mode: ++ operator for keeping parent code + adding new
        append_mode = func_info.get('append_mode', False)
        append_ref_class = func_info.get('append_ref_class')  # &ClassName or &$instanceVar
        append_ref_member = func_info.get('append_ref_member')  # ::methodName

        # Check for undefined modifier
        is_undefined = 'undefined' in modifiers

        # v4.7: Handle bytearrayed modifier for methods
        if 'bytearrayed' in modifiers:
            # Set up instance context for the bytearrayed execution
            old_instance = self._current_instance
            self._current_instance = instance
            try:
                return self._execute_bytearrayed_function(method_node)
            finally:
                self._current_instance = old_instance

        # Create new scope for method
        new_scope = Scope(parent=self.scope)

        # Bind parameters
        for i, param in enumerate(params):
            param_name = param['name'] if isinstance(param, dict) else param

            if param_name in kwargs:
                new_scope.set(param_name, kwargs[param_name])
            elif i < len(args):
                new_scope.set(param_name, args[i])
            else:
                new_scope.set(param_name, None)

        # Save current state
        old_scope = self.scope
        old_instance = self._current_instance

        # Set up method context
        self.scope = new_scope
        self._current_instance = instance
        # v4.7: Set 'this' in scope for this.member access
        new_scope.set('this', instance)
        # v4.8.8: Set 'super' for parent method access
        parent_class = getattr(instance, '_parent_class', None)
        if parent_class is None and hasattr(instance, '_class'):
            parent_class = getattr(instance._class, 'parent', None)
        if parent_class:
            new_scope.set('super', SuperProxy(instance, parent_class, self))

        original_return = None
        try:
            # Handle append mode via _append_to_target (stored original)
            original_method = func_info.get('_original_method')
            if original_method:
                # Execute original method first - capture return for fallback
                try:
                    original_return = self._call_method(instance, original_method, args, kwargs)
                except CSSLReturn as ret:
                    original_return = ret.value

            # Handle append mode (++) - execute referenced parent method first
            elif append_mode and append_ref_class:
                self._execute_append_reference(
                    instance, append_ref_class, append_ref_member,
                    args, kwargs, {}, is_constructor=False
                )

            for child in method_node.children:
                if not self._running:
                    break
                self._execute_node(child)
        except CSSLReturn as ret:
            return ret.value
        except Exception as e:
            if is_undefined:
                return None
            raise
        finally:
            # Restore previous state
            self.scope = old_scope
            self._current_instance = old_instance

        # If no return in appended code, use original's return
        return original_return

    def _call_method_with_super(self, instance: CSSLInstance, method_node: ASTNode,
                                 args: list, kwargs: dict, super_parent_class) -> Any:
        """v4.8.8: Call a method with a specific super context.

        Used when calling parent methods via super->method() to ensure the super
        inside the parent method points to the grandparent, not the instance's parent.

        Args:
            instance: The CSSLInstance to use as 'this'
            method_node: The method AST node to execute
            args: Method arguments
            kwargs: Keyword arguments
            super_parent_class: The class to use for 'super' (typically grandparent)
        """
        kwargs = kwargs or {}
        func_info = method_node.value
        params = func_info.get('params', [])
        modifiers = func_info.get('modifiers', [])

        # Check for undefined modifier
        is_undefined = 'undefined' in modifiers

        # Create new scope for method
        new_scope = Scope(parent=self.scope)

        # Bind parameters
        for i, param in enumerate(params):
            param_name = param['name'] if isinstance(param, dict) else param
            if param_name in kwargs:
                new_scope.set(param_name, kwargs[param_name])
            elif i < len(args):
                new_scope.set(param_name, args[i])
            else:
                new_scope.set(param_name, None)

        # Save current state
        old_scope = self.scope
        old_instance = self._current_instance

        # Set up method context
        self.scope = new_scope
        self._current_instance = instance
        # Set 'this' in scope for this.member access
        new_scope.set('this', instance)
        # Set 'super' with the specified parent class (typically grandparent)
        if super_parent_class:
            new_scope.set('super', SuperProxy(instance, super_parent_class, self))

        try:
            for child in method_node.children:
                if not self._running:
                    break
                self._execute_node(child)
        except CSSLReturn as ret:
            return ret.value
        except Exception as e:
            if is_undefined:
                return None
            raise
        finally:
            # Restore previous state
            self.scope = old_scope
            self._current_instance = old_instance

        return None

    # v4.7.1: Attribute blacklist for security - prevents access to dangerous Python attributes
    ATTR_BLACKLIST = frozenset({
        '__class__', '__dict__', '__bases__', '__mro__', '__subclasses__',
        '__import__', '__builtins__', '__globals__', '__locals__',
        '__code__', '__call__', '__delattr__', '__setattr__', '__getattribute__',
        '__reduce__', '__reduce_ex__', '__init_subclass__', '__new__',
        '__module__', '__qualname__', '__annotations__', '__slots__',
        '__weakref__', '__func__', '__self__', '__wrapped__',
    })

    def _eval_member_access(self, node: ASTNode) -> Any:
        """Evaluate member access"""
        obj = self._evaluate(node.value.get('object'))
        member = node.value.get('member')

        # v4.9.3: Special handling for null checks - null.is_null() returns true
        if obj is None:
            if member == 'is_null':
                return lambda: True
            return None

        # v4.7.1: Security - block access to dangerous Python attributes
        if member in self.ATTR_BLACKLIST:
            raise CSSLRuntimeError(
                f"Access to '{member}' is not allowed for security reasons."
            )
        if member.startswith('__') and member.endswith('__'):
            raise CSSLRuntimeError(
                f"Access to dunder attributes ('{member}') is not allowed."
            )

        # Special handling for Parameter.return() -> Parameter.return_()
        # since 'return' is a Python keyword
        if isinstance(obj, Parameter) and member == 'return':
            member = 'return_'

        # === ServiceDefinition (from include()) ===
        if isinstance(obj, ServiceDefinition):
            # v4.8.6: Check classes first (for new MyClass() pattern)
            if member in obj.classes:
                return obj.classes[member]
            # Check functions
            if member in obj.functions:
                func_node = obj.functions[member]
                return lambda *args, **kwargs: self._call_function(func_node, list(args), kwargs)
            # Check structs
            if member in obj.structs:
                return obj.structs[member]
            # v4.8.6: Check enums
            if member in obj.enums:
                return obj.enums[member]
            # v4.8.6: Check namespaces
            if member in obj.namespaces:
                return obj.namespaces[member]
            # Check regular attributes
            if hasattr(obj, member):
                return getattr(obj, member)
            # Build helpful error
            available = (list(obj.classes.keys()) + list(obj.functions.keys()) +
                        list(obj.structs.keys()) + list(obj.enums.keys()) +
                        list(obj.namespaces.keys()))
            similar = _find_similar_names(member, available)
            if similar:
                hint = f"Did you mean: {', '.join(similar)}?"
            elif available:
                hint = f"Available: {', '.join(available[:10])}"
            else:
                hint = "No exports defined in this module."
            raise self._format_error(
                node.line if hasattr(node, 'line') else 0,
                f"Module has no export '{member}'",
                hint
            )

        # === CSSL CLASS INSTANCE METHODS ===
        if isinstance(obj, CSSLInstance):
            # Check for member variable
            if obj.has_member(member):
                return obj.get_member(member)
            # Check for method
            if obj.has_method(member):
                method_node = obj.get_method(member)
                # Check if this is an inherited Python method
                if isinstance(method_node, tuple) and method_node[0] == 'python_method':
                    python_method = method_node[1]
                    return lambda *args, **kwargs: python_method(*args, **kwargs)
                return lambda *args, **kwargs: self._call_method(obj, method_node, list(args), kwargs)
            # Build helpful error with available members
            class_name = obj._class.name
            available_members = list(obj._members.keys()) if hasattr(obj, '_members') else []
            available_methods = list(obj._methods.keys()) if hasattr(obj, '_methods') else []
            all_available = available_members + available_methods
            similar = _find_similar_names(member, all_available)

            if similar:
                hint = f"Did you mean: {', '.join(similar)}?"
            elif all_available:
                hint = f"Available: {', '.join(all_available[:5])}"
            else:
                hint = f"Class '{class_name}' has no accessible members."

            raise self._format_error(
                node.line,
                f"'{class_name}' has no member or method '{member}'",
                hint
            )

        # === v4.8.8: SUPER PROXY - Parent class method access ===
        if isinstance(obj, SuperProxy):
            # Get method from parent class
            method_node = obj.get_method(member)
            if method_node:
                # Return a callable that invokes the parent method with correct super context
                # Key: super inside the parent method should point to grandparent!
                parent_of_parent = getattr(obj._parent_class, 'parent', None)

                def call_parent_method(*args, **kwargs):
                    return self._call_method_with_super(
                        obj._instance, method_node, list(args), kwargs,
                        parent_of_parent  # Pass grandparent as the super context
                    )
                return call_parent_method

            # Check for member
            member_val = obj.get_member(member)
            if member_val is not None:
                return member_val

            # Error: no such method in parent
            parent_name = obj._parent_class.name if obj._parent_class else "parent"
            raise self._format_error(
                node.line if hasattr(node, 'line') else 0,
                f"Parent class '{parent_name}' has no method '{member}'",
                "Check that the parent class defines this method."
            )

        # === UNIVERSAL INSTANCE METHODS ===
        from .cssl_types import UniversalInstance
        if isinstance(obj, UniversalInstance):
            # Check for member variable
            if obj.has_member(member):
                return obj.get_member(member)
            # Check for method
            if obj.has_method(member):
                method_node = obj.get_method(member)
                # Create a callable that executes the method in context
                def instance_method_caller(*args, **kwargs):
                    # Set 'this' to refer to the instance
                    old_this = self.scope.get('this')
                    self.scope.set('this', obj)
                    try:
                        return self._call_function(method_node, list(args))
                    finally:
                        if old_this is not None:
                            self.scope.set('this', old_this)
                        else:
                            self.scope.remove('this') if hasattr(self.scope, 'remove') else None
                return instance_method_caller
            # Build helpful error with available members
            instance_name = obj.name
            available_members = list(obj.get_all_members().keys())
            available_methods = list(obj.get_all_methods().keys())
            all_available = available_members + available_methods
            similar = _find_similar_names(member, all_available)

            if similar:
                hint = f"Did you mean: {', '.join(similar)}?"
            elif all_available:
                hint = f"Available: {', '.join(all_available[:5])}"
            else:
                hint = f"Instance '{instance_name}' has no accessible members."

            raise self._format_error(
                node.line,
                f"Instance '{instance_name}' has no member or method '{member}'",
                hint
            )

        # === STRING METHODS ===
        if isinstance(obj, str):
            string_methods = self._get_string_method(obj, member)
            if string_methods is not None:
                return string_methods

        # === LIST/ARRAY METHODS for plain lists ===
        # Exclude DataStruct and other custom containers - they have their own methods
        from .cssl_types import DataStruct, List, Dictionary, Queue, Bit, Byte, Address
        if isinstance(obj, list) and not isinstance(obj, (Stack, Vector, Array, DataStruct, List)):
            list_methods = self._get_list_method(obj, member)
            if list_methods is not None:
                return list_methods

        # === CSSL CONTAINER TYPES (Stack, Vector, Array, Map, Queue, etc.) ===
        # v4.8.7: Explicit handling for CSSL container methods to ensure they're found
        # v4.9.0: Added Bit and Byte types
        if isinstance(obj, (Stack, Vector, Array, DataStruct, List, Dictionary, Map, Queue, Bit, Byte, Address)):
            # Try to get the method directly from the object
            method = getattr(obj, member, None)
            if method is not None:
                return method
            # Also check the class for methods (handles inheritance)
            for cls in type(obj).__mro__:
                if hasattr(cls, member):
                    method = getattr(obj, member)
                    if method is not None:
                        return method

        if hasattr(obj, member):
            return getattr(obj, member)

        if isinstance(obj, dict):
            return obj.get(member)

        return None

    def _get_string_method(self, s: str, method: str) -> Any:
        """Get string method implementation for CSSL.

        Provides C++/Java/JS style string methods that Python doesn't have.
        """
        # === C++/Java/JS STRING METHODS ===
        if method == 'contains':
            return lambda substr: substr in s
        elif method == 'indexOf':
            return lambda substr, start=0: s.find(substr, start)
        elif method == 'lastIndexOf':
            return lambda substr: s.rfind(substr)
        elif method == 'charAt':
            return lambda index: s[index] if 0 <= index < len(s) else ''
        elif method == 'charCodeAt':
            return lambda index: ord(s[index]) if 0 <= index < len(s) else -1
        elif method == 'substring':
            return lambda start, end=None: s[start:end] if end else s[start:]
        elif method == 'substr':
            return lambda start, length=None: s[start:start+length] if length else s[start:]
        elif method == 'slice':
            return lambda start, end=None: s[start:end] if end else s[start:]

        # === TRIM METHODS ===
        elif method == 'trim':
            return lambda: s.strip()
        elif method == 'trimStart' or method == 'trimLeft' or method == 'ltrim':
            return lambda: s.lstrip()
        elif method == 'trimEnd' or method == 'trimRight' or method == 'rtrim':
            return lambda: s.rstrip()

        # === CASE METHODS ===
        elif method in ('toUpperCase', 'toUpper', 'upper'):
            return lambda: s.upper()
        elif method in ('toLowerCase', 'toLower', 'lower'):
            return lambda: s.lower()
        elif method == 'capitalize':
            return lambda: s.capitalize()
        elif method == 'title':
            return lambda: s.title()
        elif method == 'swapcase':
            return lambda: s.swapcase()

        # === REPLACE METHODS ===
        elif method == 'replaceAll':
            return lambda old, new: s.replace(old, new)
        elif method == 'replaceFirst':
            return lambda old, new: s.replace(old, new, 1)

        # === CHECK METHODS ===
        elif method == 'isEmpty':
            return lambda: len(s) == 0
        elif method == 'isBlank':
            return lambda: len(s.strip()) == 0
        elif method == 'isDigit' or method == 'isNumeric':
            return lambda: s.isdigit()
        elif method == 'isAlpha':
            return lambda: s.isalpha()
        elif method == 'isAlphaNumeric' or method == 'isAlnum':
            return lambda: s.isalnum()
        elif method == 'isSpace' or method == 'isWhitespace':
            return lambda: s.isspace()
        elif method == 'isUpper':
            return lambda: s.isupper()
        elif method == 'isLower':
            return lambda: s.islower()

        # === STARTS/ENDS WITH ===
        elif method == 'startsWith' or method == 'startswith':
            return lambda prefix: s.startswith(prefix)
        elif method == 'endsWith' or method == 'endswith':
            return lambda suffix: s.endswith(suffix)

        # === LENGTH/SIZE ===
        elif method == 'length' or method == 'size':
            return lambda: len(s)

        # === SPLIT/JOIN ===
        elif method == 'toArray':
            return lambda sep=None: list(s.split(sep) if sep else list(s))
        elif method == 'lines':
            return lambda: s.splitlines()
        elif method == 'words':
            return lambda: s.split()

        # === PADDING ===
        elif method == 'padStart' or method == 'padLeft' or method == 'lpad':
            return lambda width, char=' ': s.rjust(width, char[0] if char else ' ')
        elif method == 'padEnd' or method == 'padRight' or method == 'rpad':
            return lambda width, char=' ': s.ljust(width, char[0] if char else ' ')
        elif method == 'center':
            return lambda width, char=' ': s.center(width, char[0] if char else ' ')
        elif method == 'zfill':
            return lambda width: s.zfill(width)

        # === REPEAT ===
        elif method == 'repeat':
            return lambda n: s * n

        # === REVERSE ===
        elif method == 'reverse':
            return lambda: s[::-1]

        # === FORMAT ===
        elif method == 'format':
            return lambda *args, **kwargs: s.format(*args, **kwargs)

        # === ENCODING ===
        elif method == 'encode':
            return lambda encoding='utf-8': s.encode(encoding)
        elif method == 'bytes':
            return lambda encoding='utf-8': list(s.encode(encoding))

        # === NUMERIC CONVERSION ===
        elif method == 'toInt' or method == 'toInteger':
            return lambda base=10: int(s, base) if s.lstrip('-').isdigit() else 0
        elif method == 'toFloat' or method == 'toDouble':
            def _to_float():
                try:
                    return float(s)
                except (ValueError, TypeError):
                    return 0.0
            return _to_float
        elif method == 'toBool':
            return lambda: s.lower() in ('true', '1', 'yes', 'on')

        # === C++ ITERATOR STYLE ===
        elif method == 'begin':
            return lambda: 0
        elif method == 'end':
            return lambda: len(s)

        # Return None if not a string method
        return None

    def _get_list_method(self, lst: list, method: str) -> Any:
        """Get list method implementation for plain Python lists in CSSL."""
        if method == 'contains':
            return lambda item: item in lst
        elif method == 'indexOf':
            def index_of(item):
                try:
                    return lst.index(item)
                except ValueError:
                    return -1
            return index_of
        elif method == 'lastIndexOf':
            def last_index_of(item):
                for i in range(len(lst) - 1, -1, -1):
                    if lst[i] == item:
                        return i
                return -1
            return last_index_of
        elif method == 'length' or method == 'size':
            return lambda: len(lst)
        elif method == 'isEmpty':
            return lambda: len(lst) == 0
        elif method == 'first':
            return lambda: lst[0] if lst else None
        elif method == 'last':
            return lambda: lst[-1] if lst else None
        elif method == 'at':
            return lambda i: lst[i] if 0 <= i < len(lst) else None
        elif method == 'slice':
            return lambda start, end=None: lst[start:end] if end else lst[start:]
        elif method == 'join':
            return lambda sep=',': sep.join(str(x) for x in lst)
        elif method == 'find':
            def find_item(val):
                for item in lst:
                    if item == val:
                        return item
                return None
            return find_item
        elif method == 'push':
            def push_item(item):
                lst.append(item)
                return lst
            return push_item
        elif method == 'push_back':
            def push_back_item(item):
                lst.append(item)
                return lst
            return push_back_item
        elif method == 'toArray':
            return lambda: list(lst)
        elif method == 'content':
            return lambda: list(lst)
        # === C++ ITERATOR STYLE ===
        elif method == 'begin':
            return lambda: 0
        elif method == 'end':
            return lambda: len(lst)

        return None

    def _eval_index_access(self, node: ASTNode) -> Any:
        """Evaluate index access"""
        obj = self._evaluate(node.value.get('object'))
        index = self._evaluate(node.value.get('index'))

        if obj is None:
            raise CSSLRuntimeError(f"Cannot index into None/null value")

        try:
            return obj[index]
        except IndexError:
            # v4.2.6: Throw error instead of returning None
            length = len(obj) if hasattr(obj, '__len__') else 'unknown'
            raise CSSLRuntimeError(f"Index {index} out of bounds (length: {length})")
        except KeyError:
            # v4.2.6: Throw error for missing dict keys
            raise CSSLRuntimeError(f"Key '{index}' not found in dictionary")
        except TypeError as e:
            raise CSSLRuntimeError(f"Cannot index: {e}")

    def _set_member(self, node: ASTNode, value: Any):
        """Set member value"""
        obj = self._evaluate(node.value.get('object'))
        member = node.value.get('member')

        if obj is None:
            return

        # Check for CSSLInstance - use set_member method
        if isinstance(obj, CSSLInstance):
            obj.set_member(member, value)
            return

        # Check for UniversalInstance - use set_member method
        from .cssl_types import UniversalInstance
        if isinstance(obj, UniversalInstance):
            obj.set_member(member, value)
            return

        # Check for SharedObjectProxy - directly access underlying object
        # This is more robust than relying on the proxy's __setattr__
        if hasattr(obj, '_direct_object') and hasattr(obj, '_name'):
            # This is a SharedObjectProxy - get the real object directly
            real_obj = object.__getattribute__(obj, '_direct_object')
            if real_obj is None:
                # Fallback to _live_objects registry
                name = object.__getattribute__(obj, '_name')
                from ..cssl_bridge import _live_objects
                real_obj = _live_objects.get(name)
            if real_obj is not None:
                setattr(real_obj, member, value)
                return

        if hasattr(obj, member):
            setattr(obj, member, value)
        elif isinstance(obj, dict):
            obj[member] = value
        else:
            # Try setattr anyway for objects that support dynamic attributes
            try:
                setattr(obj, member, value)
            except (AttributeError, TypeError):
                pass

    def _set_index(self, node: ASTNode, value: Any):
        """Set index value"""
        obj = self._evaluate(node.value.get('object'))
        index = self._evaluate(node.value.get('index'))

        if obj is not None:
            try:
                obj[index] = value
            except (IndexError, KeyError, TypeError):
                pass

    def _set_module_value(self, path: str, value: Any):
        """Set a value on a module path or promoted global"""
        parts = path.split('.')
        if len(parts) < 2:
            # Single name (no dots) - set in promoted_globals and global_scope
            self._promoted_globals[path] = value
            self.global_scope.set(path, value)
            return

        obj = self._modules.get(parts[0])
        # Also check promoted_globals for the base object
        if obj is None:
            obj = self._promoted_globals.get(parts[0])
        if obj is None:
            obj = self.global_scope.get(parts[0])
        if obj is None:
            return

        for part in parts[1:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict):
                obj = obj.get(part)
            else:
                return

        final_attr = parts[-1]
        if hasattr(obj, final_attr):
            setattr(obj, final_attr, value)
        elif isinstance(obj, dict):
            obj[final_attr] = value

    # String interpolation (supports both <var> and {var} syntax)
    def _interpolate_string(self, string: str) -> str:
        """Replace {variable} and <variable> placeholders with values from scope.

        Both syntaxes are supported (variables only, not expressions):
            "Hello {name}!"   -> "Hello John!"  (f-string style)
            "Hello <name>!"   -> "Hello John!"  (legacy CSSL style)

        Examples:
            string name = "Alice";
            int age = 30;
            printl("Hello {name}, you are {age} years old!");
            printl("Hello <name>, you are <age> years old!");

        Note: Only simple variable names are supported, not expressions.
        Use string concatenation for complex expressions.
        """
        import re

        def replacer(match):
            var_name = match.group(1)
            # Try scope first
            value = self.scope.get(var_name)
            # Try promoted globals
            if value is None:
                value = self._promoted_globals.get(var_name)
            # Try modules
            if value is None:
                value = self._modules.get(var_name)
            # Try global scope
            if value is None:
                value = self.global_scope.get(var_name)
            # Return string representation or empty string if None
            return str(value) if value is not None else ''

        # Support both {var} and <var> syntax - simple variable names only
        # Pattern: {identifier} or <identifier>
        patterns = [
            r'\{([A-Za-z_][A-Za-z0-9_]*)\}',  # {name} f-string style
            r'<([A-Za-z_][A-Za-z0-9_]*)>',     # <name> legacy CSSL style
        ]

        result = string
        for pattern in patterns:
            result = re.sub(pattern, replacer, result)
        return result

    # NEW: Promote variable to global scope via global()
    def promote_to_global(self, s_ref_name: str):
        """Promote s@<name> to @<name> (make globally accessible) - NEW

        Example: global(s@cache) makes @cache available
        """
        # Extract the base name from s@<path>
        parts = s_ref_name.split('.')
        base_name = parts[0]

        # Get the value from global structs
        value = self.get_global_struct(s_ref_name)

        if value is not None:
            # Register as module reference
            self._modules[base_name] = value
            # Also store in promoted globals for string interpolation
            self._promoted_globals[base_name] = value

    # NEW: Scan for captured_ref nodes and capture their current values
    def _scan_and_capture_refs(self, node: ASTNode) -> Dict[str, Any]:
        """Scan AST for %<name> captured references and capture their current values.

        This is called at infusion registration time to capture values.
        Example: old_exit <<== { %exit(); } captures 'exit' at definition time.
        """
        captured = {}

        def scan_node(n):
            if not isinstance(n, ASTNode):
                return

            # Found a captured_ref - capture its current value
            if n.type == 'captured_ref':
                name = n.value
                if name not in captured:
                    # Try to find value - check multiple sources
                    value = None

                    # 1. Check _original_functions first (for functions that were JUST replaced)
                    if value is None:
                        value = self._original_functions.get(name)

                    # 2. Check scope
                    if value is None:
                        value = self.scope.get(name)

                    # 3. Check global_scope
                    if value is None:
                        value = self.global_scope.get(name)

                    # 4. Check builtins (most common case for exit, print, etc.)
                    if value is None:
                        # For critical builtins like 'exit', create a direct wrapper
                        # that captures the runtime reference to ensure correct behavior
                        if name == 'exit':
                            runtime = self  # Capture runtime in closure
                            value = lambda code=0, rt=runtime: rt.exit(code)
                        else:
                            value = getattr(self.builtins, f'builtin_{name}', None)

                    # 5. Check if there's a user-defined function in scope
                    if value is None:
                        # Look for function definitions
                        func_def = self.global_scope.get(f'__func_{name}')
                        if func_def is not None:
                            value = func_def

                    # Only capture if we found something
                    if value is not None:
                        captured[name] = value

            # Check call node's callee
            if n.type == 'call':
                callee = n.value.get('callee')
                if callee:
                    scan_node(callee)
                for arg in n.value.get('args', []):
                    scan_node(arg)

            # Recurse into children
            if hasattr(n, 'children') and n.children:
                for child in n.children:
                    scan_node(child)

            # Check value dict for nested nodes
            if hasattr(n, 'value') and isinstance(n.value, dict):
                for key, val in n.value.items():
                    if isinstance(val, ASTNode):
                        scan_node(val)
                    elif isinstance(val, list):
                        for item in val:
                            if isinstance(item, ASTNode):
                                scan_node(item)

        scan_node(node)
        return captured

    # NEW: Register permanent function injection
    def register_function_injection(self, func_name: str, code_block: ASTNode):
        """Register code to be permanently injected into a function - NEW

        Example: exit() <== { println("Cleanup..."); }
        Makes every call to exit() also execute the injected code

        Captures %<name> references at registration time.
        """
        # Scan for %<name> captured references and capture their current values
        captured_values = self._scan_and_capture_refs(code_block)

        if func_name not in self._function_injections:
            self._function_injections[func_name] = []
        self._function_injections[func_name].append((code_block, captured_values))

    # NEW: Execute injected code for a function
    def _execute_function_injections(self, func_name: str):
        """Execute all injected code blocks for a function - NEW

        Includes protection against recursive execution to prevent doubled output.
        Uses captured values for %<name> references.
        """
        # Prevent recursive injection execution (fixes doubled output bug)
        if getattr(self, '_injection_executing', False):
            return

        if func_name in self._function_injections:
            self._injection_executing = True
            old_captured = self._current_captured_values.copy()
            try:
                for injection in self._function_injections[func_name]:
                    # Handle both tuple format (code_block, captured_values) and legacy ASTNode format
                    if isinstance(injection, tuple):
                        code_block, captured_values = injection
                        self._current_captured_values = captured_values
                    else:
                        code_block = injection
                        self._current_captured_values = {}

                    if isinstance(code_block, ASTNode):
                        if code_block.type == 'action_block':
                            for child in code_block.children:
                                # Check if exit() was called
                                if not self._running:
                                    break
                                self._execute_node(child)
                        else:
                            self._execute_node(code_block)
            finally:
                self._injection_executing = False
                self._current_captured_values = old_captured

    # Output functions for builtins
    def set_output_callback(self, callback: Callable[[str, str], None]):
        """Set output callback for console integration"""
        self._output_callback = callback

    def _emit_output(self, text: str, level: str = 'normal'):
        """Emit output through callback or print"""
        import sys
        if self._output_callback:
            self._output_callback(text, level)
        else:
            # Handle encoding issues on Windows console
            try:
                print(text, end='')
            except UnicodeEncodeError:
                # Fallback: encode with errors='replace' for unsupported chars
                encoded = text.encode(sys.stdout.encoding or 'utf-8', errors='replace')
                print(encoded.decode(sys.stdout.encoding or 'utf-8', errors='replace'), end='')

    def output(self, text: str):
        """Output text"""
        self.output_buffer.append(text)
        self._emit_output(text, 'normal')

    def debug(self, message: str):
        """Debug output"""
        text = f"[DEBUG] {message}\n"
        self._emit_output(text, 'debug')

    def error(self, message: str):
        """Error output"""
        text = f"[ERROR] {message}\n"
        self._emit_output(text, 'error')

    def warn(self, message: str):
        """Warning output"""
        text = f"[WARN] {message}\n"
        self._emit_output(text, 'warning')

    def log(self, level: str, message: str):
        """Log with level"""
        level_map = {'debug': 'debug', 'info': 'normal', 'warn': 'warning', 'warning': 'warning', 'error': 'error'}
        output_level = level_map.get(level.lower(), 'normal')
        text = f"[{level.upper()}] {message}\n"
        self._emit_output(text, output_level)

    def exit(self, code: int = 0):
        """Exit runtime"""
        self._exit_code = code
        self._running = False

    def get_output(self) -> str:
        """Get buffered output"""
        return ''.join(self.output_buffer)

    def clear_output(self):
        """Clear output buffer"""
        self.output_buffer.clear()


class CSSLServiceRunner:
    """
    Runs CSSL services with event integration
    """

    def __init__(self, runtime: CSSLRuntime):
        self.runtime = runtime
        self.running_services: Dict[str, ServiceDefinition] = {}
        self.event_manager = get_event_manager()

    def load_service(self, source: str) -> ServiceDefinition:
        """Load and parse a CSSL service"""
        ast = parse_cssl(source)
        service = self.runtime._exec_service(ast)
        return service

    def load_service_file(self, filepath: str) -> ServiceDefinition:
        """Load a service from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.load_service(source)

    def start_service(self, service: ServiceDefinition) -> bool:
        """Start a loaded service"""
        if service.name in self.running_services:
            return False

        self.running_services[service.name] = service

        try:
            # Execute Initialization struct first if exists
            if 'Initialization' in service.structs:
                init_struct = service.structs['Initialization']
                self.runtime._exec_struct(init_struct)
            elif 'Init' in service.structs:
                init_struct = service.structs['Init']
                self.runtime._exec_struct(init_struct)

            # Execute main function if exists
            if 'main' in service.functions:
                main_func = service.functions['main']
                self.runtime._call_function(main_func, [])
            else:
                # Try to find a main-like function
                for func_name in ['Main', 'run', 'Run', 'start', 'Start']:
                    if func_name in service.functions:
                        self.runtime._call_function(service.functions[func_name], [])
                        break

        except CSSLReturn:
            pass  # Normal return from main
        except CSSLRuntimeError as e:
            # Runtime error with line number
            self.runtime.error(f"Service '{service.name}' Fehler (Zeile {e.line}): {e}")
            return False
        except Exception as e:
            # Try to extract line info
            line_info = ""
            if hasattr(e, 'line') and e.line:
                line_info = f" (Zeile {e.line})"
            self.runtime.error(f"Service '{service.name}' Fehler{line_info}: {e}")
            return False

        return True

    def stop_service(self, service_name: str) -> bool:
        """Stop a running service"""
        if service_name not in self.running_services:
            return False

        service = self.running_services[service_name]

        # Execute cleanup if exists
        if 'cleanup' in service.functions:
            cleanup_func = service.functions['cleanup']
            self.runtime._call_function(cleanup_func, [])

        del self.running_services[service_name]
        return True

    def get_running_services(self) -> List[str]:
        """Get list of running service names"""
        return list(self.running_services.keys())


# C++ interpreter cache
_cpp_interpreter = None


def _get_cpp_interpreter():
    """Get or create C++ interpreter instance."""
    global _cpp_interpreter
    if _cpp_interpreter is not None:
        return _cpp_interpreter

    try:
        from . import _CPP_AVAILABLE, _cpp_module
        if _CPP_AVAILABLE and _cpp_module and hasattr(_cpp_module, 'Interpreter'):
            _cpp_interpreter = _cpp_module.Interpreter()
            return _cpp_interpreter
    except Exception:
        pass
    return None


def run_cssl(source: str, service_engine=None, force_python: bool = False) -> Any:
    """Run CSSL source code.

    Uses C++ interpreter for maximum performance when available.
    Falls back to Python interpreter for unsupported features.

    Args:
        source: CSSL source code
        service_engine: Optional service engine for external integrations
        force_python: Force Python interpreter (for debugging)

    Returns:
        Execution result
    """
    # v4.8.8: Python-only builtins that require subprocess/import magic
    # These don't work in C++ interpreter and must use Python
    # v4.9.2: Added address/reflect/memory for pointer system, hooks syntax
    PYTHON_ONLY_FEATURES = ['includecpp(', 'snapshot(', '%', 'address(', 'reflect(', 'memory(', ' &', '&$', 'destroy(', 'execute(']

    # Check if source uses Python-only features
    needs_python = any(feat in source for feat in PYTHON_ONLY_FEATURES)

    # Try C++ interpreter first (10-20x faster)
    if not force_python and not needs_python:
        cpp_interp = _get_cpp_interpreter()
        if cpp_interp:
            try:
                return cpp_interp.run_string(source)
            except Exception as e:
                # C++ doesn't support this feature, fall back to Python
                # v4.8.5: Extended fallback triggers for advanced CSSL syntax
                error_msg = str(e).lower()
                fallback_triggers = [
                    'unsupported', 'not implemented', 'unexpected', 'expected',
                    'syntax error', 'unknown identifier', 'undefined', 'not defined'
                ]
                should_fallback = any(trigger in error_msg for trigger in fallback_triggers)
                if should_fallback:
                    pass  # Fall through to Python
                else:
                    # Re-raise actual errors
                    raise CSSLRuntimeError(str(e))

    # Python fallback (full feature support)
    runtime = CSSLRuntime(service_engine)
    return runtime.execute(source)


def run_cssl_file(filepath: str, service_engine=None, force_python: bool = False) -> Any:
    """Run a CSSL file.

    Uses C++ interpreter for maximum performance when available.
    """
    # v4.8.8: Python-only builtins that require subprocess/import magic
    # v4.9.2: Added address/reflect/memory for pointer system, hooks syntax
    PYTHON_ONLY_FEATURES = ['includecpp(', 'snapshot(', '%', 'address(', 'reflect(', 'memory(', ' &', '&$', 'destroy(', 'execute(']

    # Check file content for Python-only features
    needs_python = False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            needs_python = any(feat in source for feat in PYTHON_ONLY_FEATURES)
    except Exception:
        pass  # If we can't read, let the runtime handle it

    # Try C++ interpreter first
    if not force_python and not needs_python:
        cpp_interp = _get_cpp_interpreter()
        if cpp_interp:
            try:
                return cpp_interp.run(filepath)
            except Exception as e:
                # v4.8.5: Extended fallback triggers
                error_msg = str(e).lower()
                fallback_triggers = [
                    'unsupported', 'not implemented', 'unexpected', 'expected',
                    'syntax error', 'unknown identifier', 'undefined', 'not defined'
                ]
                should_fallback = any(trigger in error_msg for trigger in fallback_triggers)
                if should_fallback:
                    pass  # Fall through to Python
                else:
                    raise CSSLRuntimeError(str(e))

    # Python fallback
    runtime = CSSLRuntime(service_engine)
    return runtime.execute_file(filepath)
