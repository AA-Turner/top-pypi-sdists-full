"""
CSSL Multi-Language Support Module

Provides language definitions, syntax transformers, and cross-language instance access
for Python, Java, C#, C++, and JavaScript.

Usage:
    @py = libinclude("python")
    cpp = libinclude("c++")

    define my_func() : supports @py {
        # Python syntax here
        for i in range(10):
            print(i)
    }

    class MyClass : extends cpp$BaseClass {
        // C++ style
    }
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re


class SupportedLanguage(Enum):
    """Enumeration of supported programming languages"""
    PYTHON = "python"
    JAVA = "java"
    CSHARP = "c#"
    CPP = "c++"
    JAVASCRIPT = "javascript"


@dataclass
class LanguageSyntax:
    """Defines syntax rules for a programming language"""
    name: str
    statement_terminator: str      # ";" or "\n"
    uses_braces: bool              # True for {}, False for indentation (Python)
    boolean_true: str              # "True", "true"
    boolean_false: str             # "False", "false"
    null_keyword: str              # "None", "null", "nullptr"
    variable_keywords: List[str]   # ["let", "const", "var"] for JS
    function_keywords: List[str]   # ["def"] for Python, ["function"] for JS
    class_keywords: List[str]      # ["class"]
    constructor_name: str          # "__init__" for Python, "constructor" for JS
    print_function: str            # "print", "console.log", "System.out.println"
    comment_single: str            # "#" or "//"
    comment_multi_start: str       # "/*" or '"""'
    comment_multi_end: str         # "*/" or '"""'


@dataclass
class LanguageSupport:
    """
    Language support object returned by libinclude().

    Provides syntax transformation and cross-language instance sharing.
    Now with real runtime bridges for C++, Java, and JavaScript (v4.1.1).
    """
    language: SupportedLanguage
    syntax: LanguageSyntax
    name: str
    _instances: Dict[str, Any] = field(default_factory=dict)
    _transformer: Optional['LanguageTransformer'] = field(default=None, repr=False)
    _bridge: Optional['RuntimeBridge'] = field(default=None, repr=False)

    def _get_bridge(self) -> Optional['RuntimeBridge']:
        """Get the runtime bridge for this language."""
        if self._bridge is not None:
            return self._bridge

        # Lazy-load the appropriate bridge
        if self.language == SupportedLanguage.CPP:
            self._bridge = get_cpp_bridge()
        elif self.language == SupportedLanguage.JAVA:
            self._bridge = get_java_bridge()
        elif self.language == SupportedLanguage.JAVASCRIPT:
            self._bridge = get_js_bridge()

        return self._bridge

    def share(self, name: str, instance: Any) -> None:
        """
        Share an instance for cross-language access.

        Usage in CSSL:
            cpp.share("Engine", myEngine)

        Then accessible via:
            cpp$Engine
        """
        self._instances[name] = instance
        # Also share with the runtime bridge if available
        bridge = self._get_bridge()
        if bridge:
            bridge.share(name, instance)

    def get_instance(self, name: str) -> Any:
        """
        Get a shared instance by name with full bidirectional bridge support.

        v4.1.1: Enhanced to access instances from runtime bridges.

        Usage in CSSL:
            engine = cpp.get("Engine")
            // Or via $ syntax:
            engine = cpp$Engine

        For C++: Also accesses classes from IncludeCPP modules.
        For Java: Accesses instances from JVM via JPype.
        For JavaScript: Accesses instances from Node.js runtime.
        """
        # First check local instances
        if name in self._instances:
            return self._instances[name]

        # Check the runtime bridge
        bridge = self._get_bridge()
        if bridge:
            # Try to get from bridge's shared instances
            instance = bridge.get_instance(name)
            if instance is not None:
                return instance

            # C++ specific: Also check loaded modules for classes
            if self.language == SupportedLanguage.CPP and hasattr(bridge, '_modules'):
                for mod in bridge._modules.values():
                    if hasattr(mod, name):
                        cls_or_instance = getattr(mod, name)
                        # Cache for future access
                        self._instances[name] = cls_or_instance
                        return cls_or_instance

            # Java specific: Try to load class by name
            if self.language == SupportedLanguage.JAVA and hasattr(bridge, 'load_class'):
                try:
                    cls = bridge.load_class(name)
                    if cls is not None:
                        self._instances[name] = cls
                        return cls
                except Exception:
                    pass

            # JavaScript specific: Try to get from JS context
            if self.language == SupportedLanguage.JAVASCRIPT and hasattr(bridge, 'eval'):
                try:
                    result = bridge.eval(f"typeof {name} !== 'undefined' ? {name} : null")
                    if result is not None:
                        self._instances[name] = result
                        return result
                except Exception:
                    pass

        return None

    def has_instance(self, name: str) -> bool:
        """Check if an instance is shared (includes bridge instances)."""
        if name in self._instances:
            return True
        bridge = self._get_bridge()
        if bridge:
            if bridge.get_instance(name) is not None:
                return True
            # For C++, also check modules
            if self.language == SupportedLanguage.CPP and hasattr(bridge, '_modules'):
                for mod in bridge._modules.values():
                    if hasattr(mod, name):
                        return True
        return False

    def list_instances(self) -> List[str]:
        """List all shared instance names (includes bridge instances and C++ classes)."""
        return self.list_available()

    def list_available(self) -> List[str]:
        """
        List all available items accessible via $ syntax.

        v4.1.1: Enhanced to show all accessible items from runtime bridges.

        Returns a list of names that can be used with lang$Name syntax.
        """
        available = set(self._instances.keys())
        bridge = self._get_bridge()
        if bridge:
            # Get from bridge's list_available if it has one
            if hasattr(bridge, 'list_available'):
                try:
                    available.update(bridge.list_available())
                except:
                    pass
            # Also check bridge's _instances directly
            if hasattr(bridge, '_instances'):
                available.update(bridge._instances.keys())
            # For C++, also list module exports
            if self.language == SupportedLanguage.CPP and hasattr(bridge, '_modules'):
                for mod in bridge._modules.values():
                    for attr in dir(mod):
                        if not attr.startswith('_'):
                            available.add(attr)
        return sorted(available)

    def remove_instance(self, name: str) -> bool:
        """Remove a shared instance"""
        if name in self._instances:
            del self._instances[name]
            return True
        return False

    def get_transformer(self) -> 'LanguageTransformer':
        """Get the syntax transformer for this language"""
        if self._transformer is None:
            self._transformer = create_transformer(self)
        return self._transformer

    # === Runtime Bridge Methods (v4.1.1) ===

    def load_module(self, module_name: str) -> Any:
        """Load a module from the target language (C++ only)."""
        bridge = self._get_bridge()
        if bridge and hasattr(bridge, 'load_module'):
            return bridge.load_module(module_name)
        raise NotImplementedError(f"load_module not supported for {self.name}")

    def create(self, class_name: str, *args) -> Any:
        """Create an instance of a class in the target language."""
        bridge = self._get_bridge()
        if bridge and hasattr(bridge, 'create'):
            return bridge.create(class_name, *args)
        raise NotImplementedError(f"create not supported for {self.name}")

    def load_class(self, class_name: str) -> Any:
        """Load a class from the target language (Java only)."""
        bridge = self._get_bridge()
        if bridge and hasattr(bridge, 'load_class'):
            return bridge.load_class(class_name)
        raise NotImplementedError(f"load_class not supported for {self.name}")

    def add_classpath(self, path: str) -> None:
        """Add to classpath (Java only)."""
        bridge = self._get_bridge()
        if bridge and hasattr(bridge, 'add_classpath'):
            bridge.add_classpath(path)
        else:
            raise NotImplementedError(f"add_classpath not supported for {self.name}")

    def eval(self, code: str) -> Any:
        """Evaluate code in the target language (JavaScript only)."""
        bridge = self._get_bridge()
        if bridge and hasattr(bridge, 'eval'):
            return bridge.eval(code)
        raise NotImplementedError(f"eval not supported for {self.name}")

    def call(self, func_name: str, *args) -> Any:
        """Call a function in the target language (JavaScript only)."""
        bridge = self._get_bridge()
        if bridge and hasattr(bridge, 'call'):
            return bridge.call(func_name, *args)
        raise NotImplementedError(f"call not supported for {self.name}")

    def is_available(self) -> bool:
        """Check if the runtime for this language is available."""
        bridge = self._get_bridge()
        if bridge:
            return bridge.is_available()
        return True  # Python/C# don't need external runtimes

    def __getattr__(self, name: str) -> Any:
        """Allow method-like access for convenience"""
        if name == 'get':
            return self.get_instance
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")


class LanguageTransformer:
    """
    Base class for transforming language-specific syntax to CSSL.

    Each language has a specific transformer that handles its unique syntax.
    """

    def __init__(self, lang_support: LanguageSupport):
        self.lang = lang_support
        self.syntax = lang_support.syntax

    def transform_source(self, source: str) -> str:
        """Transform source code from target language to CSSL"""
        raise NotImplementedError("Subclasses must implement transform_source")

    def _common_replacements(self, stmt: str) -> str:
        """Apply common replacements across all languages"""
        return stmt


class PythonTransformer(LanguageTransformer):
    """
    Transforms Python syntax to CSSL.

    Handles:
    - Indentation-based blocks -> brace-based blocks
    - def -> define
    - print() -> printl()
    - self. -> this->
    - None -> null
    - Python-style for loops -> CSSL for loops
    """

    def transform_source(self, source: str) -> str:
        lines = source.split('\n')
        result = []
        indent_stack = [0]  # Stack of indentation levels

        for i, line in enumerate(lines):
            stripped = line.lstrip()

            # Handle empty lines and comments
            if not stripped:
                continue
            if stripped.startswith('#'):
                # Convert Python comment to CSSL comment
                result.append('// ' + stripped[1:].lstrip())
                continue

            current_indent = len(line) - len(stripped)

            # Handle dedent - close blocks
            while len(indent_stack) > 1 and current_indent < indent_stack[-1]:
                indent_stack.pop()
                result.append(' ' * indent_stack[-1] + '}')

            # Transform the statement
            transformed = self._transform_statement(stripped)

            # Check if line opens a new block (ends with :)
            if stripped.rstrip().endswith(':'):
                # Remove trailing colon, add opening brace
                transformed = transformed.rstrip(':').rstrip() + ' {'
                # Get next line's indentation
                next_indent = self._get_next_indent(lines, i)
                if next_indent > current_indent:
                    indent_stack.append(next_indent)
            elif not transformed.endswith(('{', '}', ';')):
                # Add semicolon if not a block statement
                transformed += ';'

            result.append(' ' * current_indent + transformed)

        # Close remaining open blocks
        while len(indent_stack) > 1:
            indent_stack.pop()
            result.append(' ' * indent_stack[-1] + '}')

        return '\n'.join(result)

    def _transform_statement(self, stmt: str) -> str:
        """Transform a single Python statement to CSSL"""

        # def func(args): -> define func(args)
        # Handles: def func(self, param: type = default) -> ReturnType:
        if stmt.startswith('def '):
            # Match function with optional return type annotation
            match = re.match(r'def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*\w+)?\s*:', stmt)
            if match:
                func_name = match.group(1)
                params = match.group(2)
                # Strip type annotations from parameters
                params = self._strip_type_annotations(params)
                # Remove 'self' parameter (first param in methods)
                params = self._strip_self_param(params)
                return f"define {func_name}({params})"

        # class ClassName(Parent): -> class ClassName : extends Parent
        if stmt.startswith('class '):
            match = re.match(r'class\s+(\w+)(?:\s*\((.*?)\))?\s*:', stmt)
            if match:
                class_name = match.group(1)
                parent = match.group(2)
                if parent and parent.strip():
                    return f"class {class_name} : extends {parent}"
                return f"class {class_name}"

        # if condition: -> if (condition)
        if stmt.startswith('if '):
            match = re.match(r'if\s+(.+?):', stmt)
            if match:
                condition = match.group(1)
                return f"if ({condition})"

        # elif condition: -> elif (condition)
        if stmt.startswith('elif '):
            match = re.match(r'elif\s+(.+?):', stmt)
            if match:
                condition = match.group(1)
                return f"elif ({condition})"

        # else: -> else
        if stmt.strip() == 'else:':
            return 'else'

        # while condition: -> while (condition)
        if stmt.startswith('while '):
            match = re.match(r'while\s+(.+?):', stmt)
            if match:
                condition = match.group(1)
                return f"while ({condition})"

        # for i in range(n): -> for (i in range(0, n))
        # for i in iterable: -> for (i in iterable)
        if stmt.startswith('for '):
            match = re.match(r'for\s+(\w+)\s+in\s+(.+?):', stmt)
            if match:
                var = match.group(1)
                iterable = match.group(2)
                # Handle range with single argument
                range_match = re.match(r'range\s*\(\s*(\d+)\s*\)', iterable)
                if range_match:
                    return f"for ({var} in range(0, {range_match.group(1)}))"
                return f"for ({var} in {iterable})"

        # try: -> try
        if stmt.strip() == 'try:':
            return 'try'

        # except Exception as e: -> catch (e)
        if stmt.startswith('except'):
            match = re.match(r'except\s*(?:\w+\s+)?(?:as\s+(\w+))?\s*:', stmt)
            if match:
                var = match.group(1) or 'e'
                return f"catch ({var})"

        # finally: -> finally
        if stmt.strip() == 'finally:':
            return 'finally'

        # return value -> return value
        # (no change needed, just ensure semicolon is added)

        # Common replacements
        stmt = self._apply_replacements(stmt)

        return stmt

    def _apply_replacements(self, stmt: str) -> str:
        """Apply common Python to CSSL replacements"""
        # print() -> printl()
        stmt = re.sub(r'\bprint\s*\(', 'printl(', stmt)

        # self. -> this->
        stmt = stmt.replace('self.', 'this->')

        # None -> null
        stmt = re.sub(r'\bNone\b', 'null', stmt)

        # True/False stay the same (CSSL supports both cases)

        # v4.2.0: Transform compound assignment operators (CSSL doesn't have +=, -=, etc.)
        # var -= expr -> var = var - expr
        # var += expr -> var = var + expr
        # var *= expr -> var = var * expr
        # var /= expr -> var = var / expr
        # Handles: this->health -= damage, x += 1, etc.
        compound_ops = [
            (r'(\S+)\s*-=\s*(.+)', r'\1 = \1 - \2'),   # -= to = -
            (r'(\S+)\s*\+=\s*(.+)', r'\1 = \1 + \2'),  # += to = +
            (r'(\S+)\s*\*=\s*(.+)', r'\1 = \1 * \2'),  # *= to = *
            (r'(\S+)\s*/=\s*(.+)', r'\1 = \1 / \2'),   # /= to = /
        ]
        for pattern, replacement in compound_ops:
            stmt = re.sub(pattern, replacement, stmt)

        # __init__ -> constructor handling would be done at class level

        return stmt

    def _get_next_indent(self, lines: List[str], current_idx: int) -> int:
        """Get indentation of next non-empty, non-comment line"""
        for i in range(current_idx + 1, len(lines)):
            line = lines[i]
            stripped = line.lstrip()
            if stripped and not stripped.startswith('#'):
                return len(line) - len(stripped)
        return 0

    def _strip_type_annotations(self, params: str) -> str:
        """Strip Python type annotations from parameter list.

        Examples:
            'self, x: int, y: str = "default"' -> 'self, x, y = "default"'
            'a: List[int], b: Dict[str, int]' -> 'a, b'
        """
        if not params.strip():
            return params

        result = []
        # Split by comma, but be careful with nested brackets
        depth = 0
        current = []
        for char in params + ',':
            if char in '([{':
                depth += 1
                current.append(char)
            elif char in ')]}':
                depth -= 1
                current.append(char)
            elif char == ',' and depth == 0:
                param = ''.join(current).strip()
                if param:
                    # Strip type annotation: "name: type = default" -> "name = default"
                    # or "name: type" -> "name"
                    colon_match = re.match(r'^(\w+)\s*:', param)
                    if colon_match:
                        param_name = colon_match.group(1)
                        # Check for default value after type annotation
                        default_match = re.search(r'=\s*(.+)$', param)
                        if default_match:
                            param = f"{param_name} = {default_match.group(1)}"
                        else:
                            param = param_name
                    result.append(param)
                current = []
            else:
                current.append(char)

        return ', '.join(result)

    def _strip_self_param(self, params: str) -> str:
        """Remove 'self' parameter from method parameters.

        Examples:
            'self, x, y' -> 'x, y'
            'self' -> ''
            'x, y' -> 'x, y'
        """
        if not params.strip():
            return params

        parts = [p.strip() for p in params.split(',')]
        if parts and parts[0] == 'self':
            parts = parts[1:]
        return ', '.join(parts)


class JavaScriptTransformer(LanguageTransformer):
    """
    Transforms JavaScript syntax to CSSL.

    Handles:
    - let/const/var -> dynamic
    - function name() -> define name()
    - console.log() -> printl()
    - null/undefined -> null
    - Arrow functions (basic support)
    """

    def transform_source(self, source: str) -> str:
        lines = source.split('\n')
        result = []

        for line in lines:
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                continue

            # Convert comments
            if stripped.startswith('//'):
                result.append(stripped)
                continue

            # Transform the line
            transformed = self._transform_line(stripped)
            result.append(transformed)

        return '\n'.join(result)

    def _transform_line(self, line: str) -> str:
        """Transform a single JavaScript line to CSSL"""

        # function name(args) { -> define name(args) {
        match = re.match(r'function\s+(\w+)\s*\((.*?)\)\s*\{?', line)
        if match:
            func_name = match.group(1)
            params = match.group(2)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            return f"define {func_name}({params}){suffix}"

        # const/let/var name = value; -> dynamic name = value;
        match = re.match(r'(const|let|var)\s+(\w+)\s*=\s*(.+)', line)
        if match:
            var_name = match.group(2)
            value = match.group(3)
            return f"dynamic {var_name} = {value}"

        # const/let/var name; -> dynamic name;
        match = re.match(r'(const|let|var)\s+(\w+)\s*;', line)
        if match:
            var_name = match.group(2)
            return f"dynamic {var_name};"

        # class Name { or class Name extends Parent {
        match = re.match(r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{?', line)
        if match:
            class_name = match.group(1)
            parent = match.group(2)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            if parent:
                return f"class {class_name} : extends {parent}{suffix}"
            return f"class {class_name}{suffix}"

        # constructor(args) { -> constr ClassName(args) {
        if line.strip().startswith('constructor'):
            match = re.match(r'constructor\s*\((.*?)\)\s*\{?', line)
            if match:
                params = match.group(1)
                suffix = ' {' if line.rstrip().endswith('{') else ''
                return f"constr __init__({params}){suffix}"

        # Common replacements
        line = self._apply_replacements(line)

        return line

    def _apply_replacements(self, line: str) -> str:
        """Apply common JavaScript to CSSL replacements"""
        # console.log() -> printl()
        line = re.sub(r'console\.log\s*\(', 'printl(', line)

        # console.error() -> error()
        line = re.sub(r'console\.error\s*\(', 'error(', line)

        # console.warn() -> warn()
        line = re.sub(r'console\.warn\s*\(', 'warn(', line)

        # true/false -> True/False
        line = re.sub(r'\btrue\b', 'True', line)
        line = re.sub(r'\bfalse\b', 'False', line)

        # undefined -> null
        line = re.sub(r'\bundefined\b', 'null', line)

        # this. stays as this. (CSSL uses this-> but also supports this.)

        return line


class JavaTransformer(LanguageTransformer):
    """
    Transforms Java syntax to CSSL.

    Handles:
    - System.out.println() -> printl()
    - true/false -> True/False
    - String -> string (optional lowercase)
    """

    def transform_source(self, source: str) -> str:
        lines = source.split('\n')
        result = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith('//'):
                result.append(stripped)
                continue

            transformed = self._transform_line(stripped)
            result.append(transformed)

        return '\n'.join(result)

    def _transform_line(self, line: str) -> str:
        """Transform a single Java line to CSSL"""

        # public/private/protected static void main(String[] args)
        # -> define main(args)
        match = re.match(r'(?:public|private|protected)?\s*(?:static)?\s*(?:void|int|String|boolean|float|double)\s+(\w+)\s*\((.*?)\)\s*\{?', line)
        if match:
            func_name = match.group(1)
            params = match.group(2)
            # Simplify Java params: String[] args -> args
            params = re.sub(r'\w+(?:\[\])?\s+(\w+)', r'\1', params)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            return f"define {func_name}({params}){suffix}"

        # class Name extends Parent implements Interface {
        match = re.match(r'(?:public\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+\w+(?:,\s*\w+)*)?\s*\{?', line)
        if match:
            class_name = match.group(1)
            parent = match.group(2)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            if parent:
                return f"class {class_name} : extends {parent}{suffix}"
            return f"class {class_name}{suffix}"

        # Common replacements
        line = self._apply_replacements(line)

        return line

    def _apply_replacements(self, line: str) -> str:
        """Apply common Java to CSSL replacements"""
        # System.out.println() -> printl()
        line = re.sub(r'System\.out\.println\s*\(', 'printl(', line)
        line = re.sub(r'System\.out\.print\s*\(', 'print(', line)

        # true/false -> True/False
        line = re.sub(r'\btrue\b', 'True', line)
        line = re.sub(r'\bfalse\b', 'False', line)

        # String -> string (CSSL convention)
        line = re.sub(r'\bString\b', 'string', line)

        return line


class CSharpTransformer(LanguageTransformer):
    """
    Transforms C# syntax to CSSL.

    Handles:
    - Console.WriteLine() -> printl()
    - true/false -> True/False
    - var -> dynamic
    """

    def transform_source(self, source: str) -> str:
        lines = source.split('\n')
        result = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith('//'):
                result.append(stripped)
                continue

            transformed = self._transform_line(stripped)
            result.append(transformed)

        return '\n'.join(result)

    def _transform_line(self, line: str) -> str:
        """Transform a single C# line to CSSL"""

        # public/private void MethodName(params) {
        match = re.match(r'(?:public|private|protected|internal)?\s*(?:static)?\s*(?:async)?\s*(?:void|int|string|bool|float|double|var|dynamic|\w+)\s+(\w+)\s*\((.*?)\)\s*\{?', line)
        if match and not line.strip().startswith('class'):
            func_name = match.group(1)
            params = match.group(2)
            # Simplify C# params: string name -> name
            params = re.sub(r'\w+\s+(\w+)', r'\1', params)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            return f"define {func_name}({params}){suffix}"

        # class Name : Parent {
        match = re.match(r'(?:public\s+)?(?:partial\s+)?class\s+(\w+)(?:\s*:\s*(\w+))?\s*\{?', line)
        if match:
            class_name = match.group(1)
            parent = match.group(2)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            if parent:
                return f"class {class_name} : extends {parent}{suffix}"
            return f"class {class_name}{suffix}"

        # var name = value; -> dynamic name = value;
        match = re.match(r'var\s+(\w+)\s*=\s*(.+)', line)
        if match:
            var_name = match.group(1)
            value = match.group(2)
            return f"dynamic {var_name} = {value}"

        # Common replacements
        line = self._apply_replacements(line)

        return line

    def _apply_replacements(self, line: str) -> str:
        """Apply common C# to CSSL replacements"""
        # Console.WriteLine() -> printl()
        line = re.sub(r'Console\.WriteLine\s*\(', 'printl(', line)
        line = re.sub(r'Console\.Write\s*\(', 'print(', line)

        # true/false -> True/False
        line = re.sub(r'\btrue\b', 'True', line)
        line = re.sub(r'\bfalse\b', 'False', line)

        return line


class CppTransformer(LanguageTransformer):
    """
    Transforms C++ syntax to CSSL.

    Handles:
    - std::cout << x << std::endl; -> printl(x);
    - nullptr -> null
    - auto -> dynamic
    - true/false -> True/False
    """

    def transform_source(self, source: str) -> str:
        lines = source.split('\n')
        result = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith('//'):
                result.append(stripped)
                continue

            transformed = self._transform_line(stripped)
            result.append(transformed)

        return '\n'.join(result)

    def _transform_line(self, line: str) -> str:
        """Transform a single C++ line to CSSL"""

        # void/int/etc functionName(params) {
        match = re.match(r'(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:void|int|string|bool|float|double|auto|\w+)\s+(\w+)\s*\((.*?)\)\s*(?:const)?\s*(?:override)?\s*\{?', line)
        if match and not any(kw in line for kw in ['class ', 'struct ', 'namespace ']):
            func_name = match.group(1)
            params = match.group(2)
            # Simplify C++ params: const std::string& name -> name
            params = re.sub(r'(?:const\s+)?(?:std::)?(?:\w+)(?:&|\*)?\s+(\w+)', r'\1', params)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            return f"define {func_name}({params}){suffix}"

        # class Name : public Parent {
        match = re.match(r'class\s+(\w+)(?:\s*:\s*(?:public|protected|private)\s+(\w+))?\s*\{?', line)
        if match:
            class_name = match.group(1)
            parent = match.group(2)
            suffix = ' {' if line.rstrip().endswith('{') else ''
            if parent:
                return f"class {class_name} : extends {parent}{suffix}"
            return f"class {class_name}{suffix}"

        # auto name = value; -> dynamic name = value;
        match = re.match(r'auto\s+(\w+)\s*=\s*(.+)', line)
        if match:
            var_name = match.group(1)
            value = match.group(2)
            return f"dynamic {var_name} = {value}"

        # Common replacements
        line = self._apply_replacements(line)

        return line

    def _apply_replacements(self, line: str) -> str:
        """Apply common C++ to CSSL replacements"""
        # std::cout << x << std::endl; -> printl(x);
        match = re.match(r'std::cout\s*<<\s*(.*?)\s*<<\s*std::endl\s*;', line)
        if match:
            content = match.group(1)
            return f'printl({content});'

        match = re.match(r'std::cout\s*<<\s*(.*?)\s*;', line)
        if match:
            content = match.group(1)
            return f'print({content});'

        # true/false -> True/False
        line = re.sub(r'\btrue\b', 'True', line)
        line = re.sub(r'\bfalse\b', 'False', line)

        # nullptr -> null
        line = re.sub(r'\bnullptr\b', 'null', line)

        # auto -> dynamic (for standalone declarations)
        line = re.sub(r'\bauto\b', 'dynamic', line)

        return line


# =============================================================================
# CROSS-LANGUAGE RUNTIME BRIDGES (v4.1.1)
# =============================================================================

class RuntimeBridge:
    """
    Base class for cross-language runtime bridges.

    v4.1.1: Provides bidirectional instance sharing and access between
    CSSL and target languages (C++, Java, JavaScript).
    """

    def __init__(self):
        self._instances: Dict[str, Any] = {}
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize the runtime bridge. Returns True if successful."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Check if this runtime is available on the system."""
        raise NotImplementedError

    def share(self, name: str, instance: Any) -> None:
        """Share an instance for cross-language access."""
        self._instances[name] = instance

    def get_instance(self, name: str) -> Any:
        """Get a shared instance by name."""
        return self._instances.get(name)

    def has_instance(self, name: str) -> bool:
        """Check if an instance exists."""
        return name in self._instances

    def list_available(self) -> List[str]:
        """List all available instances and classes."""
        return sorted(self._instances.keys())

    def call_method(self, instance: Any, method: str, *args) -> Any:
        """Call a method on a foreign language object."""
        raise NotImplementedError

    def get_field(self, instance: Any, field: str) -> Any:
        """Get a field value from a foreign language object."""
        raise NotImplementedError

    def set_field(self, instance: Any, field: str, value: Any) -> None:
        """Set a field value on a foreign language object."""
        raise NotImplementedError


class CppRuntimeBridge(RuntimeBridge):
    """
    C++ Runtime Bridge using IncludeCPP's pybind11 modules.

    Accesses C++ classes and objects via the generated Python bindings.
    v4.1.1: Full bidirectional support with automatic module discovery.

    Usage in CSSL:
        cpp = libinclude("c++");

        // List available C++ classes/modules
        printl(cpp.list_available());

        // Access a C++ module built with IncludeCPP
        cpp.load_module("mymodule");

        // Create C++ instance
        obj = cpp.create("MyClass", 10, 20);
        cpp.share("MyInstance", obj);

        // Access via $ syntax
        instance = cpp$MyInstance;

        // Direct class access (if module is loaded)
        MyClass = cpp$MyClass;
        obj2 = new MyClass(5, 10);
    """

    def __init__(self):
        super().__init__()
        self._modules: Dict[str, Any] = {}
        self._api = None
        self._class_cache: Dict[str, Any] = {}  # Cache class lookups

    def initialize(self) -> bool:
        """Initialize by connecting to IncludeCPP's CppApi."""
        if self._initialized:
            return True
        try:
            from ...cpp_api import CppApi
            self._api = CppApi()
            self._initialized = True
            # Auto-load all registered modules
            for name in self._api.registry.keys():
                try:
                    module = self._api.include(name)
                    self._modules[name] = module
                    # Cache all classes from the module
                    self._cache_module_classes(name, module)
                except Exception:
                    pass  # Module might not be built yet
            return True
        except Exception as e:
            # CppApi not available, but bridge still works for sharing
            self._initialized = True
            return True

    def _cache_module_classes(self, module_name: str, module: Any) -> None:
        """Cache all classes and functions from a module for quick access."""
        for attr_name in dir(module):
            if not attr_name.startswith('_'):
                attr = getattr(module, attr_name, None)
                if attr is not None:
                    self._class_cache[attr_name] = attr

    def is_available(self) -> bool:
        """C++ is always available via pybind11."""
        return True

    def load_module(self, module_name: str) -> Any:
        """Load a C++ module built with IncludeCPP."""
        if not self._initialized:
            self.initialize()

        # Check if already loaded
        if module_name in self._modules:
            return self._modules[module_name]

        if self._api and module_name in self._api.registry:
            module = self._api.include(module_name)
            self._modules[module_name] = module
            self._cache_module_classes(module_name, module)
            return module

        # Try to import as a regular Python module (for external pybind11 modules)
        try:
            import importlib
            module = importlib.import_module(module_name)
            self._modules[module_name] = module
            self._cache_module_classes(module_name, module)
            return module
        except ImportError:
            pass

        return None

    def get_class(self, class_name: str) -> Any:
        """Get a C++ class by name (from any loaded module)."""
        if not self._initialized:
            self.initialize()

        # Check cache first
        if class_name in self._class_cache:
            return self._class_cache[class_name]

        # Search through modules
        for mod in self._modules.values():
            if hasattr(mod, class_name):
                cls = getattr(mod, class_name)
                self._class_cache[class_name] = cls
                return cls

        return None

    def create(self, class_name: str, *args, module: str = None) -> Any:
        """Create an instance of a C++ class."""
        if not self._initialized:
            self.initialize()

        # Try cache first
        if class_name in self._class_cache:
            return self._class_cache[class_name](*args)

        # Search through loaded modules for the class
        for mod_name, mod in self._modules.items():
            if module and mod_name != module:
                continue
            if hasattr(mod, class_name):
                cls = getattr(mod, class_name)
                self._class_cache[class_name] = cls
                return cls(*args)

        raise ValueError(f"C++ class '{class_name}' not found. Available: {self.list_available()}")

    def get_instance(self, name: str) -> Any:
        """Get a shared instance OR a class by name."""
        # First check shared instances
        instance = self._instances.get(name)
        if instance is not None:
            return instance

        # Then check class cache
        if name in self._class_cache:
            return self._class_cache[name]

        # Finally search modules
        for mod in self._modules.values():
            if hasattr(mod, name):
                attr = getattr(mod, name)
                self._class_cache[name] = attr
                return attr

        return None

    def list_available(self) -> List[str]:
        """List all available C++ classes, functions, and shared instances."""
        if not self._initialized:
            self.initialize()

        available = set()

        # Add shared instances
        available.update(self._instances.keys())

        # Add cached classes
        available.update(self._class_cache.keys())

        # Add module exports
        for mod in self._modules.values():
            for attr in dir(mod):
                if not attr.startswith('_'):
                    available.add(attr)

        return sorted(available)

    def list_modules(self) -> List[str]:
        """List all loaded C++ module names."""
        if not self._initialized:
            self.initialize()
        return list(self._modules.keys())

    def call_method(self, instance: Any, method: str, *args) -> Any:
        """Call a method on a C++ object."""
        if hasattr(instance, method):
            return getattr(instance, method)(*args)
        raise AttributeError(f"C++ object has no method '{method}'")

    def get_field(self, instance: Any, field: str) -> Any:
        """Get a field from a C++ object."""
        return getattr(instance, field)

    def set_field(self, instance: Any, field: str, value: Any) -> None:
        """Set a field on a C++ object."""
        setattr(instance, field, value)


class JavaRuntimeBridge(RuntimeBridge):
    """
    Java Runtime Bridge using JPype.

    Connects to JVM and allows access to Java classes and objects.
    v4.1.1: Full bidirectional support with class caching.

    Requirements:
        pip install jpype1

    Usage in CSSL:
        java = libinclude("java");

        // Add JAR to classpath BEFORE first use
        java.add_classpath("/path/to/mylib.jar");

        // Load a Java class
        MyClass = java.load_class("com.example.MyClass");

        // Create instance
        obj = java.create("com.example.MyClass", 10, "hello");
        java.share("MyService", obj);

        // Access via $ syntax
        service = java$MyService;

        // List what's available
        printl(java.list_available());
    """

    def __init__(self):
        super().__init__()
        self._jpype = None
        self._jvm_started = False
        self._classpaths: List[str] = []
        self._loaded_classes: Dict[str, Any] = {}  # Cache loaded classes

    def initialize(self) -> bool:
        """Initialize JPype and start JVM if not already running."""
        if self._initialized:
            return True
        try:
            import jpype
            import jpype.imports
            self._jpype = jpype

            if not jpype.isJVMStarted():
                # Build classpath from all added paths
                import os
                sep = ";" if os.name == 'nt' else ":"
                classpath = sep.join(self._classpaths) if self._classpaths else None
                jpype.startJVM(classpath=classpath)
                self._jvm_started = True

            self._initialized = True
            return True
        except ImportError:
            # JPype not installed
            self._initialized = True  # Mark as initialized but limited
            return False
        except Exception as e:
            self._initialized = True
            return False

    def is_available(self) -> bool:
        """Check if JPype is installed."""
        try:
            import jpype
            return True
        except ImportError:
            return False

    def add_classpath(self, path: str) -> None:
        """Add a JAR or directory to the classpath (must be called before first use)."""
        import os
        # Normalize path for current OS
        path = os.path.abspath(path)
        if path not in self._classpaths:
            self._classpaths.append(path)

    def load_class(self, class_name: str) -> Any:
        """Load a Java class by fully qualified name."""
        if not self._initialized:
            self.initialize()
        if not self._jpype:
            raise RuntimeError("JPype not available. Install with: pip install jpype1")

        # Check cache
        if class_name in self._loaded_classes:
            return self._loaded_classes[class_name]

        # Load the Java class
        try:
            cls = self._jpype.JClass(class_name)
            self._loaded_classes[class_name] = cls
            # Also cache by simple name
            simple_name = class_name.rsplit('.', 1)[-1]
            self._loaded_classes[simple_name] = cls
            return cls
        except Exception as e:
            raise RuntimeError(f"Failed to load Java class '{class_name}': {e}")

    def create(self, class_name: str, *args) -> Any:
        """Create an instance of a Java class."""
        cls = self.load_class(class_name)
        return cls(*args)

    def get_instance(self, name: str) -> Any:
        """Get a shared instance OR a loaded class by name."""
        # First check shared instances
        if name in self._instances:
            return self._instances[name]
        # Then check loaded classes (by simple name)
        if name in self._loaded_classes:
            return self._loaded_classes[name]
        return None

    def list_available(self) -> List[str]:
        """List all available Java classes and shared instances."""
        available = set()
        available.update(self._instances.keys())
        # Add loaded classes (simple names only for readability)
        for name in self._loaded_classes.keys():
            if '.' not in name:  # Only simple names
                available.add(name)
        return sorted(available)

    def list_classpaths(self) -> List[str]:
        """List all added classpaths."""
        return list(self._classpaths)

    def call_method(self, instance: Any, method: str, *args) -> Any:
        """Call a method on a Java object."""
        return getattr(instance, method)(*args)

    def get_field(self, instance: Any, field: str) -> Any:
        """Get a field from a Java object."""
        return getattr(instance, field)

    def set_field(self, instance: Any, field: str, value: Any) -> None:
        """Set a field on a Java object."""
        setattr(instance, field, value)

    def call_static(self, class_name: str, method: str, *args) -> Any:
        """Call a static method on a Java class."""
        cls = self.load_class(class_name)
        return getattr(cls, method)(*args)

    def shutdown(self) -> None:
        """Shutdown the JVM (only if we started it)."""
        if self._jvm_started and self._jpype and self._jpype.isJVMStarted():
            self._jpype.shutdownJVM()
            self._jvm_started = False


class JavaScriptRuntimeBridge(RuntimeBridge):
    """
    JavaScript Runtime Bridge using Node.js subprocess.

    Runs JavaScript code via Node.js and communicates via JSON IPC.
    v4.1.1: Full bidirectional support with persistent JS context.

    Requirements:
        Node.js must be installed and in PATH

    Usage in CSSL:
        js = libinclude("javascript");

        // Execute JavaScript code
        result = js.eval("2 + 2");

        // Define a function in JS context
        js.eval('''
            function greet(name) {
                return "Hello, " + name + "!";
            }
        ''');

        // Call it
        result = js.call("greet", "World");

        // Store value in JS context for $ access
        js.set("myValue", 42);

        // Access via $ syntax
        value = js$myValue;

        // List what's available
        printl(js.list_available());
    """

    def __init__(self):
        super().__init__()
        self._process = None
        self._node_path = "node"
        self._js_context_vars: List[str] = []  # Track defined variables/functions

    def initialize(self) -> bool:
        """Start Node.js subprocess if not already running."""
        if self._initialized:
            return True
        try:
            import subprocess
            import json

            # Check if Node.js is available
            result = subprocess.run([self._node_path, "--version"],
                                   capture_output=True, text=True,
                                   timeout=5)
            if result.returncode != 0:
                self._initialized = True
                return False

            # Start persistent Node.js process with IPC
            self._process = subprocess.Popen(
                [self._node_path, "-e", self._get_ipc_server_code()],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            self._initialized = True
            return True
        except Exception as e:
            self._initialized = True
            return False

    def _get_ipc_server_code(self) -> str:
        """Get the Node.js IPC server code."""
        return '''
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });

// Global context for storing variables accessible via $
const __cssl_context = {};

rl.on('line', (line) => {
    try {
        const cmd = JSON.parse(line);
        let result;

        if (cmd.type === 'eval') {
            result = eval(cmd.code);
        } else if (cmd.type === 'call') {
            const fn = eval(cmd.func);
            result = fn(...(cmd.args || []));
        } else if (cmd.type === 'get') {
            // First check context, then global
            result = __cssl_context[cmd.name] !== undefined
                ? __cssl_context[cmd.name]
                : (typeof global[cmd.name] !== 'undefined' ? global[cmd.name] : null);
        } else if (cmd.type === 'set') {
            __cssl_context[cmd.name] = cmd.value;
            global[cmd.name] = cmd.value;
            result = true;
        } else if (cmd.type === 'has') {
            result = cmd.name in __cssl_context || typeof global[cmd.name] !== 'undefined';
        } else if (cmd.type === 'list') {
            result = Object.keys(__cssl_context);
        } else if (cmd.type === 'define') {
            // Define a function that can be called later
            eval(cmd.code);
            if (cmd.name) {
                __cssl_context[cmd.name] = eval(cmd.name);
            }
            result = true;
        }

        console.log(JSON.stringify({success: true, result: result}));
    } catch (e) {
        console.log(JSON.stringify({success: false, error: e.message}));
    }
});
'''

    def is_available(self) -> bool:
        """Check if Node.js is available."""
        try:
            import subprocess
            result = subprocess.run([self._node_path, "--version"],
                                   capture_output=True, text=True,
                                   timeout=5)
            return result.returncode == 0
        except:
            return False

    def eval(self, code: str) -> Any:
        """Evaluate JavaScript code and return the result."""
        return self._send_command({"type": "eval", "code": code})

    def call(self, func_name: str, *args) -> Any:
        """Call a JavaScript function."""
        return self._send_command({"type": "call", "func": func_name, "args": list(args)})

    def set(self, name: str, value: Any) -> None:
        """Set a variable in the JS context for $ access."""
        self._send_command({"type": "set", "name": name, "value": value})
        self._js_context_vars.append(name)
        # Also store locally for Python-side access
        self._instances[name] = value

    def get(self, name: str) -> Any:
        """Get a variable from the JS context."""
        return self._send_command({"type": "get", "name": name})

    def define(self, name: str, code: str) -> None:
        """Define a function or class in the JS context."""
        self._send_command({"type": "define", "name": name, "code": code})
        self._js_context_vars.append(name)

    def get_instance(self, name: str) -> Any:
        """Get a shared instance from local cache or JS context."""
        # First check local Python instances
        if name in self._instances:
            return self._instances[name]

        # Then try to get from JS context
        try:
            has_it = self._send_command({"type": "has", "name": name})
            if has_it:
                result = self._send_command({"type": "get", "name": name})
                if result is not None:
                    self._instances[name] = result  # Cache it
                    return result
        except:
            pass

        return None

    def list_available(self) -> List[str]:
        """List all available variables in JS context and local instances."""
        available = set(self._instances.keys())
        available.update(self._js_context_vars)

        # Also get from JS context
        try:
            js_vars = self._send_command({"type": "list"})
            if js_vars:
                available.update(js_vars)
        except:
            pass

        return sorted(available)

    def _send_command(self, cmd: dict) -> Any:
        """Send a command to Node.js and get the result."""
        if not self._initialized:
            self.initialize()
        if not self._process:
            raise RuntimeError("Node.js not available. Make sure Node.js is installed and in PATH.")

        import json

        try:
            self._process.stdin.write(json.dumps(cmd) + "\n")
            self._process.stdin.flush()

            response_line = self._process.stdout.readline()
            if not response_line:
                raise RuntimeError("No response from Node.js process")

            response = json.loads(response_line)

            if response.get("success"):
                return response.get("result")
            else:
                raise RuntimeError(f"JavaScript error: {response.get('error')}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response from Node.js: {e}")

    def call_method(self, instance: Any, method: str, *args) -> Any:
        """For JS objects stored locally, call method."""
        if hasattr(instance, method):
            return getattr(instance, method)(*args)
        # For remote JS objects, use eval
        raise NotImplementedError("Remote JS method calls not yet supported")

    def get_field(self, instance: Any, field: str) -> Any:
        return getattr(instance, field, None)

    def set_field(self, instance: Any, field: str, value: Any) -> None:
        setattr(instance, field, value)

    def require(self, module_name: str) -> Any:
        """Require a Node.js module and return it."""
        return self.eval(f"require('{module_name}')")

    def shutdown(self) -> None:
        """Shutdown the Node.js process."""
        if self._process:
            try:
                self._process.terminate()
                self._process.wait(timeout=2)
            except:
                self._process.kill()
            self._process = None
            self._initialized = False


# Global bridge instances
_cpp_bridge: Optional[CppRuntimeBridge] = None
_java_bridge: Optional[JavaRuntimeBridge] = None
_js_bridge: Optional[JavaScriptRuntimeBridge] = None


def get_cpp_bridge() -> CppRuntimeBridge:
    """Get the global C++ runtime bridge."""
    global _cpp_bridge
    if _cpp_bridge is None:
        _cpp_bridge = CppRuntimeBridge()
        _cpp_bridge.initialize()
    return _cpp_bridge


def get_java_bridge() -> JavaRuntimeBridge:
    """Get the global Java runtime bridge."""
    global _java_bridge
    if _java_bridge is None:
        _java_bridge = JavaRuntimeBridge()
    return _java_bridge


def get_js_bridge() -> JavaScriptRuntimeBridge:
    """Get the global JavaScript runtime bridge."""
    global _js_bridge
    if _js_bridge is None:
        _js_bridge = JavaScriptRuntimeBridge()
    return _js_bridge


# Language Registry
LANGUAGE_DEFINITIONS: Dict[str, LanguageSupport] = {}


def register_language(lang_id: str, lang_support: LanguageSupport) -> None:
    """Register a language definition"""
    LANGUAGE_DEFINITIONS[lang_id.lower()] = lang_support


def get_language(lang_id: str) -> Optional[LanguageSupport]:
    """Get a language definition by ID"""
    return LANGUAGE_DEFINITIONS.get(lang_id.lower())


def list_languages() -> List[str]:
    """List all registered language IDs"""
    return list(LANGUAGE_DEFINITIONS.keys())


def create_transformer(lang_support: LanguageSupport) -> LanguageTransformer:
    """Create the appropriate transformer for a language"""
    if lang_support.language == SupportedLanguage.PYTHON:
        return PythonTransformer(lang_support)
    elif lang_support.language == SupportedLanguage.JAVASCRIPT:
        return JavaScriptTransformer(lang_support)
    elif lang_support.language == SupportedLanguage.JAVA:
        return JavaTransformer(lang_support)
    elif lang_support.language == SupportedLanguage.CSHARP:
        return CSharpTransformer(lang_support)
    elif lang_support.language == SupportedLanguage.CPP:
        return CppTransformer(lang_support)
    else:
        return LanguageTransformer(lang_support)


def _init_languages() -> None:
    """Initialize all built-in language definitions"""

    # Python
    python_syntax = LanguageSyntax(
        name="Python",
        statement_terminator="\n",
        uses_braces=False,
        boolean_true="True",
        boolean_false="False",
        null_keyword="None",
        variable_keywords=[],
        function_keywords=["def"],
        class_keywords=["class"],
        constructor_name="__init__",
        print_function="print",
        comment_single="#",
        comment_multi_start='"""',
        comment_multi_end='"""'
    )
    python_support = LanguageSupport(
        language=SupportedLanguage.PYTHON,
        syntax=python_syntax,
        name="Python"
    )
    register_language("python", python_support)
    register_language("py", python_support)

    # Java
    java_syntax = LanguageSyntax(
        name="Java",
        statement_terminator=";",
        uses_braces=True,
        boolean_true="true",
        boolean_false="false",
        null_keyword="null",
        variable_keywords=["int", "String", "boolean", "float", "double", "var"],
        function_keywords=["public", "private", "protected", "static", "void"],
        class_keywords=["class", "interface", "enum"],
        constructor_name="<classname>",
        print_function="System.out.println",
        comment_single="//",
        comment_multi_start="/*",
        comment_multi_end="*/"
    )
    java_support = LanguageSupport(
        language=SupportedLanguage.JAVA,
        syntax=java_syntax,
        name="Java"
    )
    register_language("java", java_support)

    # C#
    csharp_syntax = LanguageSyntax(
        name="C#",
        statement_terminator=";",
        uses_braces=True,
        boolean_true="true",
        boolean_false="false",
        null_keyword="null",
        variable_keywords=["int", "string", "bool", "float", "double", "var", "dynamic"],
        function_keywords=["public", "private", "protected", "static", "void", "async"],
        class_keywords=["class", "interface", "struct", "enum"],
        constructor_name="<classname>",
        print_function="Console.WriteLine",
        comment_single="//",
        comment_multi_start="/*",
        comment_multi_end="*/"
    )
    csharp_support = LanguageSupport(
        language=SupportedLanguage.CSHARP,
        syntax=csharp_syntax,
        name="C#"
    )
    register_language("c#", csharp_support)
    register_language("csharp", csharp_support)

    # C++
    cpp_syntax = LanguageSyntax(
        name="C++",
        statement_terminator=";",
        uses_braces=True,
        boolean_true="true",
        boolean_false="false",
        null_keyword="nullptr",
        variable_keywords=["int", "string", "bool", "float", "double", "auto", "const"],
        function_keywords=["void", "int", "string", "bool", "float", "double", "auto"],
        class_keywords=["class", "struct"],
        constructor_name="<classname>",
        print_function="std::cout",
        comment_single="//",
        comment_multi_start="/*",
        comment_multi_end="*/"
    )
    cpp_support = LanguageSupport(
        language=SupportedLanguage.CPP,
        syntax=cpp_syntax,
        name="C++"
    )
    register_language("c++", cpp_support)
    register_language("cpp", cpp_support)

    # JavaScript
    js_syntax = LanguageSyntax(
        name="JavaScript",
        statement_terminator=";",
        uses_braces=True,
        boolean_true="true",
        boolean_false="false",
        null_keyword="null",
        variable_keywords=["let", "const", "var"],
        function_keywords=["function", "async"],
        class_keywords=["class"],
        constructor_name="constructor",
        print_function="console.log",
        comment_single="//",
        comment_multi_start="/*",
        comment_multi_end="*/"
    )
    js_support = LanguageSupport(
        language=SupportedLanguage.JAVASCRIPT,
        syntax=js_syntax,
        name="JavaScript"
    )
    register_language("javascript", js_support)
    register_language("js", js_support)


# Initialize languages on module load
_init_languages()


# Export public API
__all__ = [
    'SupportedLanguage',
    'LanguageSyntax',
    'LanguageSupport',
    'LanguageTransformer',
    'PythonTransformer',
    'JavaScriptTransformer',
    'JavaTransformer',
    'CSharpTransformer',
    'CppTransformer',
    'register_language',
    'get_language',
    'list_languages',
    'create_transformer',
    'LANGUAGE_DEFINITIONS',
]
