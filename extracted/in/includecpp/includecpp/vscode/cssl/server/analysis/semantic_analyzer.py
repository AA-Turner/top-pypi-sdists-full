"""
Semantic Analyzer for the CSSL Language Server.

Extracts symbols, tracks variable usage, and builds the symbol table
from CSSL AST nodes.
"""

from typing import Dict, List, Any, Optional, Set

from ..utils.symbol_table import SymbolTable, Symbol, SymbolKind
from ..utils.cssl_registry import get_registry

# CSSL Keywords that should not be flagged as undefined
CSSL_KEYWORDS = {
    'if', 'else', 'elif', 'while', 'for', 'foreach', 'in', 'range',
    'switch', 'case', 'default', 'break', 'continue', 'return',
    'try', 'catch', 'finally', 'throw', 'except', 'always',
    'class', 'struct', 'enum', 'interface', 'namespace',
    'define', 'void', 'constr', 'cleanup', 'new', 'this', 'super', 'init',
    'extends', 'overwrites', 'service-init', 'service-run',
    'service-include', 'main', 'package', 'exec', 'as', 'global',
    'include', 'get', 'payload', 'convert', 'and', 'or', 'not',
    'start', 'stop', 'wait_for', 'on_event', 'emit_event', 'await',
    'async', 'yield', 'generator', 'future',
    'true', 'false', 'True', 'False', 'null', 'None',
}

# CSSL Builtin Types
CSSL_TYPES = {
    'int', 'string', 'float', 'bool', 'void', 'json', 'dynamic', 'auto',
    'long', 'double', 'bit', 'byte', 'address', 'ptr', 'pointer',
    'array', 'vector', 'stack', 'list', 'dictionary', 'dict', 'map',
    'datastruct', 'dataspace', 'shuffled', 'iterator', 'combo',
    'openquote', 'tuple', 'set', 'queue', 'instance',
}

# CSSL Builtin Functions
CSSL_BUILTINS = {
    'print', 'printl', 'println', 'input', 'read', 'readline', 'write', 'writeline',
    'len', 'type', 'toInt', 'toFloat', 'toString', 'toBool', 'typeof',
    'memory', 'address', 'reflect', 'resolve', 'destroy',
    'exit', 'sleep', 'range', 'isavailable',
    'OpenFind', 'cast', 'share', 'shared', 'include', 'includecpp',
    'snapshot', 'get_snapshot', 'has_snapshot', 'clear_snapshot',
    'clear_snapshots', 'list_snapshots', 'restore_snapshot',
    'random', 'randint', 'round', 'abs', 'ceil', 'floor', 'sqrt', 'pow', 'min', 'max', 'sum',
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'exp',
    'upper', 'lower', 'trim', 'split', 'join', 'replace', 'substr',
    'contains', 'startswith', 'endswith', 'format', 'concat',
    'push', 'pop', 'shift', 'unshift', 'slice', 'sort', 'rsort',
    'unique', 'flatten', 'filter', 'map', 'reduce', 'find', 'findindex',
    'every', 'some', 'keys', 'values', 'items', 'haskey', 'getkey', 'setkey', 'delkey', 'merge',
    'now', 'timestamp', 'date', 'time', 'datetime', 'strftime',
    'tojson', 'fromjson', 'debug', 'error', 'warn', 'log',
    'readfile', 'writefile', 'appendfile', 'readlines', 'listdir',
    'makedirs', 'removefile', 'removedir', 'copyfile', 'movefile',
    'filesize', 'pathexists', 'isfile', 'isdir', 'basename', 'dirname',
    'joinpath', 'splitpath', 'abspath',
    'isinstance', 'isint', 'isfloat', 'isstr', 'isbool', 'islist', 'isdict', 'isnull',
    'copy', 'deepcopy', 'pyimport',
    # Reflection/Introspection
    'getattr', 'setattr', 'hasattr', 'delattr', 'dir', 'vars', 'locals', 'globals',
    'callable', 'classof', 'nameof', 'sizeof', 'alignof',
}

# CSSL Function Modifiers
CSSL_MODIFIERS = {
    'undefined', 'open', 'closed', 'private', 'virtual', 'meta', 'super',
    'sqlbased', 'protected', 'limited', 'const', 'static', 'final',
    'abstract', 'readonly', 'native', 'unative', 'embedded', 'public',
    'global', 'shuffled', 'bytearrayed',
}


class SemanticAnalyzer:
    """
    Analyzes CSSL AST to extract semantic information.

    Builds a symbol table with all declarations, tracks variable usage,
    and identifies potential issues.
    """

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = self.symbol_table
        self.usages: Set[str] = set()
        self._load_builtins()

    def _load_builtins(self):
        """Load builtin functions and types into the root symbol table."""
        registry = get_registry()

        # Add builtin functions with real signatures from the runtime
        for name, info in registry.builtin_functions.items():
            self.symbol_table.add_symbol(Symbol(
                name=name,
                kind=SymbolKind.BUILTIN_FUNCTION,
                documentation=info.doc or f"Built-in function: {name}()",
                return_type=info.return_type or '',
            ))

        # Add builtin types
        for name, info in registry.builtin_types.items():
            generic = info.generic_syntax
            display = f"{name}{generic}" if generic else name
            self.symbol_table.add_symbol(Symbol(
                name=name,
                kind=SymbolKind.BUILTIN_TYPE,
                documentation=info.doc or f"Built-in type: {display}"
            ))

        # Add GUI class names (so they're recognized as valid identifiers)
        for cssl_name, cls_info in registry.gui_classes.items():
            if cssl_name.startswith('Cssl'):
                self.symbol_table.add_symbol(Symbol(
                    name=cssl_name,
                    kind=SymbolKind.BUILTIN_TYPE,
                    documentation=cls_info.doc or f"GUI widget: {cssl_name}"
                ))

        # Fallback: ensure all names from static sets are present
        # (in case registry failed to load some)
        for name in CSSL_BUILTINS:
            if not self.symbol_table.get_symbol(name):
                self.symbol_table.add_symbol(Symbol(
                    name=name,
                    kind=SymbolKind.BUILTIN_FUNCTION,
                    documentation=f"Built-in function: {name}()"
                ))
        for name in CSSL_TYPES:
            if not self.symbol_table.get_symbol(name):
                self.symbol_table.add_symbol(Symbol(
                    name=name,
                    kind=SymbolKind.BUILTIN_TYPE,
                    documentation=f"Built-in type: {name}"
                ))

    def analyze(self, ast: Any, tokens: List[Any] = None) -> SymbolTable:
        """
        Analyze the AST and build a symbol table.

        Args:
            ast: The root AST node
            tokens: Optional list of tokens for usage tracking

        Returns:
            The completed symbol table
        """
        if ast is None:
            return self.symbol_table

        # Walk the AST to collect declarations
        self._visit_node(ast)

        # Track usages from tokens
        if tokens:
            self._track_usages(tokens)

        return self.symbol_table

    def _visit_node(self, node: Any) -> None:
        """Visit an AST node and dispatch to the appropriate handler."""
        if node is None:
            return

        if not hasattr(node, 'type'):
            return

        # Dispatch based on node type
        handler_name = f'_visit_{node.type.replace("-", "_")}'
        handler = getattr(self, handler_name, None)

        if handler:
            handler(node)
        else:
            # Visit children for unknown node types
            self._visit_children(node)

    def _visit_children(self, node: Any) -> None:
        """Visit all children of a node."""
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                self._visit_node(child)

    def _visit_program(self, node: Any) -> None:
        """Visit program root node."""
        self._visit_children(node)

    def _visit_service(self, node: Any) -> None:
        """Visit service node."""
        self._visit_children(node)

    def _visit_function(self, node: Any) -> None:
        """Extract function definition."""
        info = node.value if hasattr(node, 'value') else {}

        if isinstance(info, dict):
            name = info.get('name', '')
            params = info.get('params', [])
            return_type = info.get('return_type')
            modifiers = info.get('modifiers', [])
        else:
            name = str(info)
            params = []
            return_type = None
            modifiers = []

        # Create parameter symbols
        param_symbols = []
        for p in params:
            if isinstance(p, dict):
                param_symbols.append(Symbol(
                    name=p.get('name', ''),
                    kind=SymbolKind.PARAMETER,
                    type_info=p.get('type'),
                    modifiers=['const'] if p.get('const') else []
                ))
            elif isinstance(p, str):
                param_symbols.append(Symbol(
                    name=p,
                    kind=SymbolKind.PARAMETER
                ))

        # Add function to current scope
        func_symbol = Symbol(
            name=name,
            kind=SymbolKind.FUNCTION,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1),
            return_type=return_type,
            parameters=param_symbols,
            modifiers=modifiers if isinstance(modifiers, list) else [modifiers]
        )
        self.current_scope.add_symbol(func_symbol)

        # Create child scope for function body
        func_scope = self.current_scope.create_child_scope(name)
        old_scope = self.current_scope
        self.current_scope = func_scope

        # Add parameters to function scope
        for param in param_symbols:
            func_scope.add_symbol(param)

        # Visit function body
        self._visit_children(node)

        self.current_scope = old_scope

    def _visit_constructor(self, node: Any) -> None:
        """Extract constructor/destructor definition."""
        info = node.value if hasattr(node, 'value') else {}

        if isinstance(info, dict):
            name = info.get('name', '')
            params = info.get('params', [])
            is_destructor = info.get('is_destructor', False)
        else:
            name = str(info)
            params = []
            is_destructor = False

        display_name = f"~{name}" if is_destructor else name

        param_symbols = []
        for p in params:
            if isinstance(p, dict):
                param_symbols.append(Symbol(
                    name=p.get('name', ''),
                    kind=SymbolKind.PARAMETER,
                    type_info=p.get('type'),
                ))
            elif isinstance(p, str):
                param_symbols.append(Symbol(
                    name=p,
                    kind=SymbolKind.PARAMETER,
                ))

        constr_symbol = Symbol(
            name=display_name,
            kind=SymbolKind.METHOD,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1),
            parameters=param_symbols,
            return_type=None,
        )
        self.current_scope.add_symbol(constr_symbol)
        self._visit_children(node)

    def _visit_class(self, node: Any) -> None:
        """Extract class definition."""
        info = node.value if hasattr(node, 'value') else {}

        if isinstance(info, dict):
            name = info.get('name', '')
        else:
            name = str(info)

        class_symbol = Symbol(
            name=name,
            kind=SymbolKind.CLASS,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1)
        )
        self.current_scope.add_symbol(class_symbol)

        # Create child scope for class body
        class_scope = self.current_scope.create_child_scope(name)
        old_scope = self.current_scope
        self.current_scope = class_scope

        self._visit_children(node)

        # Copy children to class symbol
        class_symbol.children = dict(class_scope.symbols)
        self.current_scope = old_scope

    def _visit_struct(self, node: Any) -> None:
        """Extract struct definition."""
        info = node.value if hasattr(node, 'value') else {}
        name = info.get('name', '') if isinstance(info, dict) else str(info)

        struct_symbol = Symbol(
            name=name,
            kind=SymbolKind.STRUCT,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1)
        )
        self.current_scope.add_symbol(struct_symbol)
        self._visit_children(node)

    def _visit_namespace(self, node: Any) -> None:
        """Extract namespace definition."""
        info = node.value if hasattr(node, 'value') else {}
        name = info.get('name', '') if isinstance(info, dict) else str(info)

        ns_symbol = Symbol(
            name=name,
            kind=SymbolKind.NAMESPACE,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1)
        )
        self.current_scope.add_symbol(ns_symbol)

        # Create namespace scope
        ns_scope = self.current_scope.create_child_scope(name)
        old_scope = self.current_scope
        self.current_scope = ns_scope

        self._visit_children(node)

        self.current_scope = old_scope

    def _visit_enum(self, node: Any) -> None:
        """Extract enum definition."""
        info = node.value if hasattr(node, 'value') else {}
        name = info.get('name', '') if isinstance(info, dict) else str(info)

        enum_symbol = Symbol(
            name=name,
            kind=SymbolKind.ENUM,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1)
        )
        self.current_scope.add_symbol(enum_symbol)

    def _visit_typed_declaration(self, node: Any) -> None:
        """Extract typed variable declaration."""
        info = node.value if hasattr(node, 'value') else {}

        if isinstance(info, dict):
            name = info.get('name', '')
            type_name = info.get('type', 'dynamic')
            element_type = info.get('element_type')

            full_type = type_name
            if element_type:
                full_type = f"{type_name}<{element_type}>"

            var_symbol = Symbol(
                name=name,
                kind=SymbolKind.VARIABLE,
                type_info=full_type,
                line=getattr(node, 'line', 1),
                column=getattr(node, 'column', 1)
            )
            self.current_scope.add_symbol(var_symbol)

        self._visit_children(node)

    def _visit_assignment(self, node: Any) -> None:
        """Extract variable from assignment if not already declared."""
        info = node.value if hasattr(node, 'value') else {}

        if isinstance(info, dict):
            name = info.get('name') or info.get('target')

            # Handle ASTNode targets
            if hasattr(name, 'type') and hasattr(name, 'value'):
                if name.type == 'identifier':
                    name = name.value
                else:
                    name = None

            if name and isinstance(name, str):
                # Only add if not already in scope
                if not self.current_scope.has_symbol(name):
                    var_symbol = Symbol(
                        name=name,
                        kind=SymbolKind.VARIABLE,
                        type_info='dynamic',
                        line=getattr(node, 'line', 1),
                        column=getattr(node, 'column', 1)
                    )
                    self.current_scope.add_symbol(var_symbol)

        self._visit_children(node)

    def _visit_for(self, node: Any) -> None:
        """Extract loop variable from for (var in ...) loops."""
        info = node.value if hasattr(node, 'value') else {}
        if isinstance(info, dict):
            var_name = info.get('var')
            if var_name and isinstance(var_name, str):
                if not self.current_scope.has_symbol(var_name):
                    self.current_scope.add_symbol(Symbol(
                        name=var_name,
                        kind=SymbolKind.VARIABLE,
                        type_info='dynamic',
                        line=getattr(node, 'line', 1),
                        column=getattr(node, 'column', 1)
                    ))
        self._visit_children(node)

    def _visit_foreach(self, node: Any) -> None:
        """Extract loop variable from foreach loops."""
        info = node.value if hasattr(node, 'value') else {}
        if isinstance(info, dict):
            var_name = info.get('var') or info.get('variable')
            if var_name and isinstance(var_name, str):
                if not self.current_scope.has_symbol(var_name):
                    self.current_scope.add_symbol(Symbol(
                        name=var_name,
                        kind=SymbolKind.VARIABLE,
                        type_info='dynamic',
                        line=getattr(node, 'line', 1),
                        column=getattr(node, 'column', 1)
                    ))
        self._visit_children(node)

    def _visit_global_declaration(self, node: Any) -> None:
        """Extract global variable declaration."""
        info = node.value if hasattr(node, 'value') else {}
        name = info.get('name', '') if isinstance(info, dict) else str(info)

        global_symbol = Symbol(
            name=name,
            kind=SymbolKind.GLOBAL,
            line=getattr(node, 'line', 1),
            column=getattr(node, 'column', 1)
        )
        self.symbol_table.add_symbol(global_symbol)

    def _track_usages(self, tokens: List[Any]) -> None:
        """Track variable usages from tokens."""
        for token in tokens:
            if hasattr(token, 'type') and hasattr(token, 'value'):
                type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)

                if type_name == 'IDENTIFIER':
                    name = token.value
                    self.usages.add(name)
                    self.symbol_table.mark_symbol_used(name)

    def is_defined(self, name: str) -> bool:
        """Check if a name is defined (variable, function, builtin, keyword)."""
        if name in CSSL_KEYWORDS:
            return True
        if name in CSSL_TYPES:
            return True
        if name in CSSL_BUILTINS:
            return True
        if name in CSSL_MODIFIERS:
            return True
        return self.symbol_table.has_symbol(name)

    def get_defined_names(self) -> Set[str]:
        """Get all defined names."""
        names = set(CSSL_KEYWORDS)
        names.update(CSSL_TYPES)
        names.update(CSSL_BUILTINS)
        names.update(CSSL_MODIFIERS)

        for symbol in self.symbol_table.get_all_symbols_flat():
            names.add(symbol.name)

        return names
