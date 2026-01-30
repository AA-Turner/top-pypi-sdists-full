"""
Diagnostic Provider for the CSSL Language Server.

Generates all diagnostic messages including syntax errors, undefined variables,
type mismatches, invalid pointer references, and other code issues.
"""

from typing import List, Set, Dict, Any, Optional
from dataclasses import dataclass

from lsprotocol.types import (
    Diagnostic, DiagnosticSeverity, Position, Range
)

from .document_manager import DocumentAnalysis
from .semantic_analyzer import (
    SemanticAnalyzer, CSSL_KEYWORDS, CSSL_TYPES, CSSL_BUILTINS, CSSL_MODIFIERS
)
from ..utils.symbol_table import SymbolKind


# Known namespaces and their members
# Note: User-defined namespaces from include() are dynamically allowed
KNOWN_NAMESPACES = {
    'json': ['read', 'write', 'parse', 'stringify', 'pretty', 'keys', 'values', 'get', 'set', 'has', 'merge', 'key', 'value'],
    'instance': ['getMethods', 'getClasses', 'getVars', 'getAll', 'call', 'has', 'type', 'exists', 'delete'],
    'python': ['pythonize', 'wrap', 'export', 'csslize', 'import', 'parameter_get', 'parameter_return', 'param_get', 'param_return'],
    'string': ['where', 'contains', 'not', 'startsWith', 'endsWith', 'length', 'lenght', 'cut', 'cutAfter', 'value'],
    'sql': ['connect', 'load', 'save', 'update', 'sync', 'Structured', 'table', 'data', 'data__list', 'db'],
    'filter': ['register', 'unregister', 'list', 'exists'],
    'combo': ['filterdb', 'blocked', 'like'],
    'async': ['run', 'wait', 'cancel', 'parallel'],
    'watcher': ['get', 'set', 'list', 'exists', 'refresh'],
    # Standard library namespaces
    'fmt': ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white', 'black', 'bold', 'italic', 'underline', 'reset', 'color', 'bg', 'bright'],
    'std': [],  # Standard library - allow any member (checked dynamically)
    'math': ['sin', 'cos', 'tan', 'sqrt', 'pow', 'abs', 'ceil', 'floor', 'round', 'log', 'exp', 'pi', 'e', 'random', 'randint'],
    'io': ['read', 'write', 'open', 'close', 'readline', 'writeline', 'flush', 'seek', 'tell', 'eof'],
    'sys': ['exit', 'args', 'env', 'platform', 'version', 'path'],
    'os': ['getcwd', 'chdir', 'listdir', 'mkdir', 'rmdir', 'remove', 'rename', 'exists', 'isfile', 'isdir'],
    'time': ['now', 'sleep', 'timestamp', 'format', 'parse', 'delta'],
    'net': ['get', 'post', 'request', 'socket', 'connect', 'listen', 'accept', 'send', 'recv'],
    # Reflection/Introspection namespaces
    'reflect': ['getMethods', 'getProperties', 'getType', 'getParent', 'getModifiers', 'getAnnotations',
                'invoke', 'create', 'getField', 'setField', 'getConstructors', 'isInstance',
                'getInterfaces', 'getSource', 'getSignature'],
    'resolve': ['byName', 'byPath', 'inScope', 'lazy', 'tryResolve', 'exists', 'type', 'function', 'class'],
}

# Type methods - all methods available on built-in types
TYPE_METHODS = {
    'datastruct': ['add', 'push', 'pop', 'get', 'set', 'remove', 'clear', 'content', 'len', 'at', 'filter', 'map', 'size', 'isEmpty', 'contains', 'begin', 'end'],
    'vector': ['push', 'push_back', 'pop', 'pop_back', 'at', 'set', 'size', 'empty', 'clear', 'insert', 'erase', 'front', 'back', 'contains', 'indexOf'],
    'stack': ['push', 'pop', 'peek', 'size', 'empty', 'clear', 'isEmpty', 'contains'],
    'queue': ['push', 'pop', 'peek', 'front', 'back', 'size', 'empty', 'clear', 'isEmpty', 'isFull'],
    'string': ['length', 'len', 'upper', 'lower', 'trim', 'split', 'replace', 'contains', 'startswith', 'endswith', 'substr', 'at', 'indexOf', 'charAt', 'concat', 'format'],
    'list': ['append', 'extend', 'insert', 'remove', 'pop', 'clear', 'index', 'count', 'sort', 'reverse', 'push', 'len', 'size'],
    'dict': ['keys', 'values', 'items', 'get', 'set', 'has', 'remove', 'clear', 'update', 'pop'],
    'map': ['insert', 'find', 'erase', 'contains', 'count', 'size', 'empty', 'at', 'keys', 'values', 'items', 'get', 'clear'],
    'array': ['push', 'pop', 'at', 'set', 'size', 'len', 'slice', 'concat', 'join', 'map', 'filter', 'reduce', 'sort', 'reverse', 'indexOf'],
    'iterator': ['next', 'has_next', 'reset', 'current', 'to_list'],
    'shuffled': ['add', 'get', 'at', 'size', 'isEmpty', 'clear'],
    # Pointer/memory types
    'ptr': ['get_address', 'set_address', 'get_value', 'set_value', 'deref', 'ref', 'is_null', 'is_valid', 'offset', 'copy', 'free'],
    'pointer': ['get_address', 'set_address', 'get_value', 'set_value', 'deref', 'ref', 'is_null', 'is_valid', 'offset', 'copy', 'free'],
    'address': ['get', 'set', 'offset', 'to_ptr', 'to_int', 'is_valid', 'copy'],
    # Numeric types
    'byte': ['to_int', 'to_bits', 'to_hex', 'to_string', 'set', 'get', 'flip', 'and', 'or', 'xor', 'not'],
    'bit': ['set', 'get', 'flip', 'to_int', 'to_bool', 'and', 'or', 'xor', 'not'],
    'int': ['to_string', 'to_float', 'to_hex', 'to_bin', 'abs', 'sign'],
    'float': ['to_string', 'to_int', 'round', 'ceil', 'floor', 'abs', 'sign'],
    # JSON type
    'json': ['parse', 'stringify', 'pretty', 'keys', 'values', 'get', 'set', 'has', 'remove', 'merge', 'clone'],
}


class DiagnosticProvider:
    """
    Provides diagnostics for CSSL documents.

    Generates errors (red), warnings (yellow), and information (blue)
    messages for various code issues.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the diagnostic provider.

        Args:
            config: Optional configuration dictionary with settings like:
                - diagnostics.enabled
                - diagnostics.undefinedVariables
                - diagnostics.unusedVariables
                - diagnostics.invalidPointers
        """
        self.config = config or {}

    def get_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """
        Generate all diagnostics for a document.

        Args:
            document: The analyzed document

        Returns:
            List of LSP Diagnostic objects
        """
        if not self.config.get('diagnostics.enabled', True):
            return []

        diagnostics = []

        # E001: Syntax errors (RED)
        diagnostics.extend(self._syntax_error_diagnostics(document))

        # Only proceed if document has tokens
        if not document.tokens:
            return diagnostics

        # Collect defined names for validation
        defined_names = self._collect_defined_names(document)
        global_names = self._collect_global_names(document)
        shared_names = self._collect_shared_names(document)
        snapshot_names = self._collect_snapshot_names(document)
        function_defs = self._collect_function_definitions(document)

        # W001: Undefined variables (YELLOW)
        if self.config.get('diagnostics.undefinedVariables', True):
            diagnostics.extend(self._undefined_variable_diagnostics(document, defined_names))

        # W002: Invalid pointer references (YELLOW)
        if self.config.get('diagnostics.invalidPointers', True):
            diagnostics.extend(self._invalid_pointer_diagnostics(document, defined_names))

        # W003: Invalid global references (YELLOW)
        diagnostics.extend(self._invalid_global_ref_diagnostics(document, global_names))

        # W004: Invalid shared references (YELLOW)
        diagnostics.extend(self._invalid_shared_ref_diagnostics(document, shared_names))

        # W005: Invalid snapshot references (YELLOW)
        diagnostics.extend(self._invalid_snapshot_ref_diagnostics(document, snapshot_names))

        # W006: Function called before definition (YELLOW)
        diagnostics.extend(self._function_order_diagnostics(document, function_defs))

        # E002-E004: Type and operation errors (RED) - only if AST is available
        if document.ast:
            diagnostics.extend(self._type_mismatch_diagnostics(document))
            diagnostics.extend(self._invalid_operation_diagnostics(document))

        # E005: Division by zero (RED)
        diagnostics.extend(self._division_by_zero_diagnostics(document))

        # E006: Invalid namespace access (RED)
        diagnostics.extend(self._invalid_namespace_access_diagnostics(document))

        # E007-E008: Duplicate definitions (RED)
        diagnostics.extend(self._duplicate_definition_diagnostics(document))

        # I001: Unused variables (INFO)
        if self.config.get('diagnostics.unusedVariables', True):
            diagnostics.extend(self._unused_variable_diagnostics(document))

        # I002: Unreachable code (INFO)
        if document.ast:
            diagnostics.extend(self._unreachable_code_diagnostics(document))

        return diagnostics

    def _syntax_error_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E001: Syntax errors from parser."""
        diagnostics = []

        for error in document.syntax_errors:
            line = max(0, error.line - 1)
            col = max(0, error.column - 1)
            token_len = len(error.token) if error.token else 1

            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=line, character=col),
                    end=Position(line=line, character=col + token_len)
                ),
                message=error.message,
                severity=DiagnosticSeverity.Error,
                source='cssl',
                code='E001'
            ))

        return diagnostics

    def _undefined_variable_diagnostics(self, document: DocumentAnalysis, defined_names: Set[str]) -> List[Diagnostic]:
        """W001: Undefined variable warnings."""
        diagnostics = []
        seen_warnings = set()

        # Build a list of tokens for context checking
        tokens = document.tokens

        # Also collect names from include() calls and typed declarations from tokens
        extra_names = self._collect_names_from_tokens(tokens)
        all_defined = defined_names | extra_names

        for i, token in enumerate(tokens):
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)

            if type_name == 'IDENTIFIER':
                name = token.value

                # Skip if already warned
                if name in seen_warnings:
                    continue

                # Skip builtins, keywords, types
                if self._is_builtin_or_keyword(name):
                    continue

                # Skip if defined
                if name in all_defined:
                    continue

                # Skip if this is a namespace member (preceded by ::)
                if self._is_namespace_member(tokens, i):
                    continue

                # Skip if this is a function/class definition name
                if self._is_definition_name(tokens, i):
                    continue

                # Skip if this looks like a type annotation (followed by identifier)
                if self._is_type_annotation(tokens, i):
                    continue

                # Skip if this is part of filter syntax [type::operator=value]
                if self._is_filter_syntax(tokens, i):
                    continue

                # Skip if this is a method call (preceded by . or ->)
                if self._is_method_call(tokens, i):
                    continue

                # Skip if this is a member access (preceded by -> or this->)
                if self._is_member_access(tokens, i):
                    continue

                # Skip if this is a constructor name (preceded by constr)
                if self._is_constructor_name(tokens, i):
                    continue

                seen_warnings.add(name)
                line = token.line - 1
                col = token.column - 1

                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=line, character=col),
                        end=Position(line=line, character=col + len(name))
                    ),
                    message=f"Variable '{name}' is not defined",
                    severity=DiagnosticSeverity.Warning,
                    source='cssl',
                    code='W001'
                ))

        return diagnostics

    def _collect_names_from_tokens(self, tokens: List[Any]) -> Set[str]:
        """Collect variable names from typed declarations and include statements in tokens."""
        names = set()

        for i, token in enumerate(tokens):
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)
            value = str(token.value)

            # Check for include("name") - adds the name as a namespace
            if type_name == 'IDENTIFIER' and value == 'include':
                # Look for the string argument
                for j in range(i + 1, min(i + 5, len(tokens))):
                    next_token = tokens[j]
                    if hasattr(next_token, 'type'):
                        next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''
                        if next_type == 'STRING':
                            # Extract string value without quotes
                            str_val = str(next_token.value).strip('"\'')
                            names.add(str_val)
                            break

            # Check for typed declarations: TYPE NAME = ...
            # Look for pattern: type identifier (where type is in CSSL_TYPES)
            if type_name == 'IDENTIFIER' and value.lower() in {t.lower() for t in CSSL_TYPES}:
                # Check if next token is an identifier (the variable name)
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if hasattr(next_token, 'type'):
                        next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''
                        if next_type == 'IDENTIFIER':
                            names.add(str(next_token.value))

            # Also check for TYPE keyword tokens
            if type_name in ('TYPE', 'BUILTIN_TYPE', 'KEYWORD') and value.lower() in {t.lower() for t in CSSL_TYPES}:
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if hasattr(next_token, 'type'):
                        next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''
                        if next_type == 'IDENTIFIER':
                            names.add(str(next_token.value))

        return names

    def _is_namespace_member(self, tokens: List[Any], index: int) -> bool:
        """Check if token at index is a namespace member (preceded by ::)."""
        if index < 2:
            return False

        # Check previous tokens for :: pattern
        for i in range(index - 1, max(0, index - 3), -1):
            prev_token = tokens[i]
            if hasattr(prev_token, 'type'):
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_value = str(prev_token.value) if hasattr(prev_token, 'value') else ''

                # Found :: operator
                if prev_type in ('DOUBLE_COLON', 'COLON_COLON', 'NAMESPACE_SEP') or prev_value == '::':
                    return True
                # Skip whitespace
                if prev_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                    continue
                # Found something else, stop
                break

        return False

    def _is_definition_name(self, tokens: List[Any], index: int) -> bool:
        """Check if token is a function/class definition name."""
        if index < 1:
            return False

        # Check previous tokens for define, class, struct, etc.
        for i in range(index - 1, max(0, index - 3), -1):
            prev_token = tokens[i]
            if hasattr(prev_token, 'type') and hasattr(prev_token, 'value'):
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_value = str(prev_token.value).lower()

                if prev_type == 'KEYWORD' or prev_type == 'IDENTIFIER':
                    if prev_value in ('define', 'class', 'struct', 'enum', 'interface', 'namespace'):
                        return True

                # Skip whitespace/modifiers
                if prev_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                    continue
                if prev_value in CSSL_MODIFIERS:
                    continue
                break

        return False

    def _is_type_annotation(self, tokens: List[Any], index: int) -> bool:
        """Check if token looks like a type being used as annotation."""
        if index + 1 >= len(tokens):
            return False

        token = tokens[index]
        next_token = tokens[index + 1]

        if not hasattr(token, 'value') or not hasattr(next_token, 'type'):
            return False

        # Check if current token looks like a type and next is identifier
        value = str(token.value).lower()
        next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''

        # If this looks like a type followed by an identifier, it's probably a declaration
        if next_type == 'IDENTIFIER':
            # Check if it could be a type (starts with capital or is known type-like)
            if value[0].isupper() or value in {t.lower() for t in CSSL_TYPES}:
                return True

        return False

    def _is_filter_syntax(self, tokens: List[Any], index: int) -> bool:
        """Check if token is part of filter syntax [type::operator=value].

        Filter syntax examples:
        - [integer::gt=5]
        - [string::contains="test"]
        - [float::between=1,10]
        """
        if index < 1:
            return False

        token = tokens[index]
        token_value = str(token.value).lower() if hasattr(token, 'value') else ''

        # Check if this is a type name followed by :: (filter type)
        # Look for pattern: [ type ::
        for i in range(index - 1, max(0, index - 5), -1):
            prev_token = tokens[i]
            if not hasattr(prev_token, 'value'):
                continue

            prev_value = str(prev_token.value)

            # If we find an opening bracket before this token, it's filter syntax
            if prev_value == '[':
                return True

            # If we find a closing bracket or other structure, stop
            if prev_value in (']', ';', '{', '}', '(', ')'):
                break

        # Also check if this token is followed by :: inside brackets (it's a type filter)
        if index + 1 < len(tokens):
            next_token = tokens[index + 1]
            next_value = str(next_token.value) if hasattr(next_token, 'value') else ''
            next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''

            if next_value == '::' or next_type in ('DOUBLE_COLON', 'COLON_COLON', 'NAMESPACE_SEP'):
                # Check if we're inside brackets
                bracket_depth = 0
                for i in range(index - 1, -1, -1):
                    prev_token = tokens[i]
                    prev_value = str(prev_token.value) if hasattr(prev_token, 'value') else ''
                    if prev_value == '[':
                        bracket_depth -= 1
                    elif prev_value == ']':
                        bracket_depth += 1
                    if bracket_depth < 0:
                        return True  # Found unmatched [ before us

        # Check if this is a filter operator (gt, lt, eq, ne, etc.)
        filter_operators = {'gt', 'lt', 'ge', 'le', 'eq', 'ne', 'between', 'contains',
                           'startswith', 'endswith', 'like', 'not', 'in', 'notin',
                           'null', 'notnull', 'empty', 'notempty', 'regex', 'match'}
        if token_value in filter_operators:
            # Check if preceded by ::
            for i in range(index - 1, max(0, index - 3), -1):
                prev_token = tokens[i]
                prev_value = str(prev_token.value) if hasattr(prev_token, 'value') else ''
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''

                if prev_value == '::' or prev_type in ('DOUBLE_COLON', 'COLON_COLON', 'NAMESPACE_SEP'):
                    return True

        return False

    def _is_method_call(self, tokens: List[Any], index: int) -> bool:
        """Check if token at index is a method call (preceded by . or ->)."""
        if index < 1:
            return False

        # Check previous tokens for . (dot) or -> (arrow) pattern
        for i in range(index - 1, max(0, index - 3), -1):
            prev_token = tokens[i]
            if hasattr(prev_token, 'type'):
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_value = str(prev_token.value) if hasattr(prev_token, 'value') else ''

                # Found . (dot) or -> (arrow) operator - this is a method/member call
                if prev_type in ('DOT', 'MEMBER_ACCESS', 'ARROW', 'POINTER_ACCESS') or prev_value in ('.', '->'):
                    return True
                # Skip whitespace
                if prev_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                    continue
                # Found something else, stop
                break

        return False

    def _is_member_access(self, tokens: List[Any], index: int) -> bool:
        """Check if token at index is a member access (preceded by -> or this->)."""
        if index < 1:
            return False

        # Check previous tokens for -> pattern or this keyword
        for i in range(index - 1, max(0, index - 5), -1):
            prev_token = tokens[i]
            if hasattr(prev_token, 'type'):
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_value = str(prev_token.value) if hasattr(prev_token, 'value') else ''

                # Found -> (arrow) operator
                if prev_type in ('ARROW', 'POINTER_ACCESS') or prev_value == '->':
                    return True
                # Found > which could be part of ->
                if prev_value == '>':
                    # Check if previous is -
                    if i > 0:
                        prev_prev = tokens[i - 1]
                        if hasattr(prev_prev, 'value') and str(prev_prev.value) == '-':
                            return True
                # Skip whitespace
                if prev_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                    continue
                # Found something else, stop
                break

        return False

    def _is_constructor_name(self, tokens: List[Any], index: int) -> bool:
        """Check if token is a constructor name (preceded by constr keyword)."""
        if index < 1:
            return False

        # Check previous tokens for 'constr' keyword
        for i in range(index - 1, max(0, index - 3), -1):
            prev_token = tokens[i]
            if hasattr(prev_token, 'type') and hasattr(prev_token, 'value'):
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_value = str(prev_token.value).lower()

                # Found constr keyword
                if prev_value == 'constr':
                    return True
                # Skip whitespace and modifiers
                if prev_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                    continue
                if prev_value in CSSL_MODIFIERS:
                    continue
                # Found something else, stop
                break

        return False

    def _invalid_pointer_diagnostics(self, document: DocumentAnalysis, defined_names: Set[str]) -> List[Diagnostic]:
        """W002: Pointer references to undefined variables."""
        diagnostics = []

        for token in document.tokens:
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)
            value = str(token.value)

            # Check for pointer reference pattern
            if type_name in ('POINTER_REF', 'QUESTION') or value.startswith('?'):
                var_name = value[1:] if value.startswith('?') else value

                if var_name and var_name not in defined_names:
                    line = token.line - 1
                    col = token.column - 1

                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=line, character=col),
                            end=Position(line=line, character=col + len(value))
                        ),
                        message=f"Pointer reference '?{var_name}' targets undefined variable '{var_name}'",
                        severity=DiagnosticSeverity.Warning,
                        source='cssl',
                        code='W002'
                    ))

        return diagnostics

    def _invalid_global_ref_diagnostics(self, document: DocumentAnalysis, global_names: Set[str]) -> List[Diagnostic]:
        """W003: Global references to undefined globals."""
        diagnostics = []

        for token in document.tokens:
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)
            value = str(token.value)

            if type_name in ('GLOBAL_REF', 'AT') or (value.startswith('@') and not value.startswith('@async')):
                var_name = value[1:] if value.startswith('@') else value

                # Skip module references (start with uppercase)
                if var_name and var_name[0].isupper():
                    continue

                if var_name and var_name not in global_names:
                    line = token.line - 1
                    col = token.column - 1

                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=line, character=col),
                            end=Position(line=line, character=col + len(value))
                        ),
                        message=f"Global reference '@{var_name}' targets undefined global '{var_name}'",
                        severity=DiagnosticSeverity.Warning,
                        source='cssl',
                        code='W003'
                    ))

        return diagnostics

    def _invalid_shared_ref_diagnostics(self, document: DocumentAnalysis, shared_names: Set[str]) -> List[Diagnostic]:
        """W004: Shared references to undefined shared variables."""
        diagnostics = []

        for token in document.tokens:
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)
            value = str(token.value)

            if type_name in ('SHARED_REF', 'DOLLAR') or value.startswith('$'):
                var_name = value[1:] if value.startswith('$') else value

                if var_name and var_name not in shared_names:
                    line = token.line - 1
                    col = token.column - 1

                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=line, character=col),
                            end=Position(line=line, character=col + len(value))
                        ),
                        message=f"Shared reference '${var_name}' targets undefined shared variable",
                        severity=DiagnosticSeverity.Warning,
                        source='cssl',
                        code='W004'
                    ))

        return diagnostics

    def _invalid_snapshot_ref_diagnostics(self, document: DocumentAnalysis, snapshot_names: Set[str]) -> List[Diagnostic]:
        """W005: Snapshot references to non-existent snapshots."""
        diagnostics = []

        for token in document.tokens:
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)
            value = str(token.value)

            if type_name in ('SNAPSHOT_REF', 'PERCENT') or value.startswith('%'):
                var_name = value[1:] if value.startswith('%') else value

                if var_name and var_name not in snapshot_names:
                    line = token.line - 1
                    col = token.column - 1

                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=line, character=col),
                            end=Position(line=line, character=col + len(value))
                        ),
                        message=f"Snapshot '%{var_name}' was never created with snapshot()",
                        severity=DiagnosticSeverity.Warning,
                        source='cssl',
                        code='W005'
                    ))

        return diagnostics

    def _function_order_diagnostics(self, document: DocumentAnalysis, function_defs: Dict[str, int]) -> List[Diagnostic]:
        """W006: Function called before definition."""
        diagnostics = []
        seen = set()

        for token in document.tokens:
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)

            if type_name == 'IDENTIFIER':
                name = token.value

                if name in function_defs and name not in seen:
                    if token.line < function_defs[name]:
                        seen.add(name)
                        line = token.line - 1
                        col = token.column - 1

                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=line, character=col),
                                end=Position(line=line, character=col + len(name))
                            ),
                            message=f"Function '{name}' called before definition (defined at line {function_defs[name]})",
                            severity=DiagnosticSeverity.Warning,
                            source='cssl',
                            code='W006'
                        ))

        return diagnostics

    def _type_mismatch_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E002: Type mismatch errors."""
        diagnostics = []

        for node in self._walk_ast(document.ast):
            if node.type == 'typed_declaration':
                info = node.value if hasattr(node, 'value') else {}

                if isinstance(info, dict):
                    expected_type = info.get('type')
                    value = info.get('value')

                    if expected_type and value:
                        actual_type = self._infer_type(value)

                        if actual_type and not self._types_compatible(expected_type, actual_type):
                            line = getattr(node, 'line', 1) - 1
                            col = getattr(node, 'column', 1) - 1

                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=Position(line=line, character=col),
                                    end=Position(line=line, character=col + 20)
                                ),
                                message=f"Type mismatch: expected '{expected_type}', got '{actual_type}'",
                                severity=DiagnosticSeverity.Error,
                                source='cssl',
                                code='E002'
                            ))

        return diagnostics

    def _invalid_operation_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E003-E004: Invalid operation errors."""
        diagnostics = []

        for node in self._walk_ast(document.ast):
            if node.type == 'binary_op':
                info = node.value if hasattr(node, 'value') else {}

                if isinstance(info, dict):
                    op = info.get('operator')
                    left = info.get('left')
                    right = info.get('right')

                    if op == '+':
                        left_type = self._infer_type(left)
                        right_type = self._infer_type(right)

                        if left_type == 'string' and right_type in ('int', 'float'):
                            line = getattr(node, 'line', 1) - 1
                            col = getattr(node, 'column', 1) - 1

                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=Position(line=line, character=col),
                                    end=Position(line=line, character=col + 15)
                                ),
                                message=f"Cannot concatenate string with {right_type} - use str() conversion",
                                severity=DiagnosticSeverity.Error,
                                source='cssl',
                                code='E003'
                            ))

            elif node.type == 'method_call':
                info = node.value if hasattr(node, 'value') else {}

                if isinstance(info, dict):
                    obj = info.get('object')
                    method = info.get('method')

                    if obj and method:
                        obj_type = self._infer_type(obj)

                        if obj_type and not self._type_has_method(obj_type, method):
                            line = getattr(node, 'line', 1) - 1
                            col = getattr(node, 'column', 1) - 1

                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=Position(line=line, character=col),
                                    end=Position(line=line, character=col + len(method) + 5)
                                ),
                                message=f"Type '{obj_type}' has no method '{method}'",
                                severity=DiagnosticSeverity.Error,
                                source='cssl',
                                code='E004'
                            ))

        return diagnostics

    def _division_by_zero_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E005: Division by zero errors."""
        diagnostics = []

        if not document.ast:
            return diagnostics

        for node in self._walk_ast(document.ast):
            if node.type == 'binary_op':
                info = node.value if hasattr(node, 'value') else {}

                if isinstance(info, dict):
                    op = info.get('operator')
                    right = info.get('right')

                    if op in ('/', '%') and right:
                        if hasattr(right, 'type') and right.type == 'number':
                            if right.value == 0:
                                line = getattr(node, 'line', 1) - 1
                                col = getattr(node, 'column', 1) - 1

                                diagnostics.append(Diagnostic(
                                    range=Range(
                                        start=Position(line=line, character=col),
                                        end=Position(line=line, character=col + 10)
                                    ),
                                    message="Division by zero",
                                    severity=DiagnosticSeverity.Error,
                                    source='cssl',
                                    code='E005'
                                ))

        return diagnostics

    def _invalid_namespace_access_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E006: Invalid namespace member access."""
        diagnostics = []

        # Look for namespace::member patterns in tokens
        prev_token = None
        prev_prev_token = None

        for token in document.tokens:
            if not hasattr(token, 'type') or not hasattr(token, 'value'):
                prev_prev_token = prev_token
                prev_token = token
                continue

            type_name = token.type.name if hasattr(token.type, 'name') else str(token.type)

            # Check for pattern: namespace :: member
            if prev_token and prev_prev_token:
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_prev_type = prev_prev_token.type.name if hasattr(prev_prev_token.type, 'name') else ''

                if prev_type in ('DOUBLE_COLON', 'COLON_COLON', 'NAMESPACE_SEP'):
                    if prev_prev_type == 'IDENTIFIER':
                        ns = prev_prev_token.value.lower()
                        member = token.value

                        if ns in KNOWN_NAMESPACES:
                            if member not in KNOWN_NAMESPACES[ns]:
                                line = token.line - 1
                                col = prev_prev_token.column - 1

                                diagnostics.append(Diagnostic(
                                    range=Range(
                                        start=Position(line=line, character=col),
                                        end=Position(line=line, character=col + len(ns) + 2 + len(member))
                                    ),
                                    message=f"Namespace '{ns}' has no member '{member}'",
                                    severity=DiagnosticSeverity.Error,
                                    source='cssl',
                                    code='E006'
                                ))

            prev_prev_token = prev_token
            prev_token = token

        return diagnostics

    def _duplicate_definition_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E007-E008: Duplicate function/class definitions."""
        diagnostics = []

        if not document.ast:
            return diagnostics

        seen_functions: Dict[str, int] = {}
        seen_classes: Dict[str, int] = {}

        for node in self._walk_ast(document.ast):
            if node.type == 'function':
                info = node.value if hasattr(node, 'value') else {}
                name = info.get('name', '') if isinstance(info, dict) else str(info)

                if name:
                    if name in seen_functions:
                        line = getattr(node, 'line', 1) - 1
                        col = getattr(node, 'column', 1) - 1

                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=line, character=col),
                                end=Position(line=line, character=col + len(name) + 7)
                            ),
                            message=f"Function '{name}' already defined at line {seen_functions[name]}",
                            severity=DiagnosticSeverity.Error,
                            source='cssl',
                            code='E007'
                        ))
                    else:
                        seen_functions[name] = getattr(node, 'line', 1)

            elif node.type == 'class':
                info = node.value if hasattr(node, 'value') else {}
                name = info.get('name', '') if isinstance(info, dict) else str(info)

                if name:
                    if name in seen_classes:
                        line = getattr(node, 'line', 1) - 1
                        col = getattr(node, 'column', 1) - 1

                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=line, character=col),
                                end=Position(line=line, character=col + len(name) + 6)
                            ),
                            message=f"Class '{name}' already defined at line {seen_classes[name]}",
                            severity=DiagnosticSeverity.Error,
                            source='cssl',
                            code='E008'
                        ))
                    else:
                        seen_classes[name] = getattr(node, 'line', 1)

        return diagnostics

    def _unused_variable_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """I001: Unused variable information."""
        diagnostics = []

        unused = document.symbol_table.get_unused_symbols()

        for symbol in unused:
            if symbol.line > 0:
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(line=symbol.line - 1, character=symbol.column - 1),
                        end=Position(line=symbol.line - 1, character=symbol.column - 1 + len(symbol.name))
                    ),
                    message=f"Variable '{symbol.name}' is declared but never used",
                    severity=DiagnosticSeverity.Information,
                    source='cssl',
                    code='I001'
                ))

        return diagnostics

    def _unreachable_code_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """I002: Unreachable code information."""
        diagnostics = []

        for node in self._walk_ast(document.ast):
            if node.type in ('function', 'while', 'for', 'foreach'):
                if hasattr(node, 'children') and node.children:
                    found_exit = False

                    for child in node.children:
                        if found_exit and hasattr(child, 'line'):
                            line = child.line - 1
                            col = getattr(child, 'column', 1) - 1

                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=Position(line=line, character=col),
                                    end=Position(line=line, character=col + 10)
                                ),
                                message="Unreachable code after return/break/continue",
                                severity=DiagnosticSeverity.Information,
                                source='cssl',
                                code='I002'
                            ))
                            break

                        if hasattr(child, 'type') and child.type in ('return', 'break', 'continue'):
                            found_exit = True

        return diagnostics

    # Helper methods

    def _collect_defined_names(self, document: DocumentAnalysis) -> Set[str]:
        """Collect all defined names from the document."""
        names = set(CSSL_KEYWORDS)
        names.update(CSSL_TYPES)
        names.update(CSSL_BUILTINS)
        names.update(CSSL_MODIFIERS)

        for symbol in document.symbol_table.get_all_symbols_flat():
            names.add(symbol.name)

        return names

    def _collect_global_names(self, document: DocumentAnalysis) -> Set[str]:
        """Collect global variable names."""
        names = set()

        for symbol in document.symbol_table.get_globals():
            names.add(symbol.name)

        # Also check for explicit global declarations in AST
        if document.ast:
            for node in self._walk_ast(document.ast):
                if node.type in ('global_declaration', 'global'):
                    info = node.value if hasattr(node, 'value') else {}
                    name = info.get('name', '') if isinstance(info, dict) else str(info)
                    if name:
                        names.add(name)

        return names

    def _collect_shared_names(self, document: DocumentAnalysis) -> Set[str]:
        """Collect shared variable names."""
        names = set()

        for symbol in document.symbol_table.get_shared():
            names.add(symbol.name)

        return names

    def _collect_snapshot_names(self, document: DocumentAnalysis) -> Set[str]:
        """Collect snapshot names from snapshot() calls."""
        names = set()

        # Look for snapshot() function calls in tokens/AST
        if document.ast:
            for node in self._walk_ast(document.ast):
                if node.type == 'function_call':
                    info = node.value if hasattr(node, 'value') else {}
                    func_name = info.get('name', '') if isinstance(info, dict) else ''

                    if func_name == 'snapshot':
                        args = info.get('args', []) if isinstance(info, dict) else []
                        if args and len(args) > 0:
                            first_arg = args[0]
                            if isinstance(first_arg, str):
                                names.add(first_arg)
                            elif hasattr(first_arg, 'value'):
                                names.add(str(first_arg.value))

        return names

    def _collect_function_definitions(self, document: DocumentAnalysis) -> Dict[str, int]:
        """Collect function names and their definition lines."""
        funcs = {}

        if document.ast:
            for node in self._walk_ast(document.ast):
                if node.type == 'function':
                    info = node.value if hasattr(node, 'value') else {}
                    name = info.get('name', '') if isinstance(info, dict) else str(info)
                    if name:
                        funcs[name] = getattr(node, 'line', 1)

        return funcs

    def _is_builtin_or_keyword(self, name: str) -> bool:
        """Check if a name is a builtin or keyword."""
        return (
            name in CSSL_KEYWORDS or
            name in CSSL_TYPES or
            name in CSSL_BUILTINS or
            name in CSSL_MODIFIERS
        )

    def _walk_ast(self, node: Any) -> List[Any]:
        """Walk AST and yield all nodes."""
        if node is None:
            return []

        nodes = [node]

        if hasattr(node, 'children') and node.children:
            for child in node.children:
                nodes.extend(self._walk_ast(child))

        # Also check value for nested nodes
        if hasattr(node, 'value') and node.value:
            if hasattr(node.value, 'type'):
                nodes.extend(self._walk_ast(node.value))
            elif isinstance(node.value, dict):
                for v in node.value.values():
                    if hasattr(v, 'type'):
                        nodes.extend(self._walk_ast(v))

        return nodes

    def _infer_type(self, node: Any) -> Optional[str]:
        """Infer the type of an expression node."""
        if node is None:
            return None

        if not hasattr(node, 'type'):
            if isinstance(node, (int, float)):
                return 'float' if isinstance(node, float) else 'int'
            elif isinstance(node, str):
                return 'string'
            elif isinstance(node, bool):
                return 'bool'
            return None

        if node.type == 'number':
            return 'float' if isinstance(node.value, float) else 'int'
        elif node.type == 'string':
            return 'string'
        elif node.type in ('boolean', 'bool'):
            return 'bool'
        elif node.type in ('null', 'none'):
            return 'null'
        elif node.type in ('array', 'list_literal'):
            return 'list'
        elif node.type in ('object', 'dict_literal'):
            return 'dict'

        return None

    def _types_compatible(self, expected: str, actual: str) -> bool:
        """Check if types are compatible."""
        if expected == 'dynamic' or actual == 'dynamic':
            return True
        if expected == actual:
            return True
        # Numeric compatibility
        if expected in ('int', 'float', 'double', 'long') and actual in ('int', 'float', 'double', 'long'):
            return True
        return False

    def _type_has_method(self, type_name: str, method: str) -> bool:
        """Check if a type has a specific method."""
        type_lower = type_name.lower()

        # Strip generic parameters
        if '<' in type_lower:
            type_lower = type_lower.split('<')[0]

        if type_lower in TYPE_METHODS:
            return method in TYPE_METHODS[type_lower]

        # Default: allow any method on unknown types
        return True
