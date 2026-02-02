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
from .semantic_analyzer import SemanticAnalyzer
from ..utils.cssl_registry import get_registry
from ..utils.symbol_table import SymbolKind


def _safe_pos(line: int, character: int) -> Position:
    """Create a Position with clamped non-negative values."""
    return Position(line=max(0, line), character=max(0, character))


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
                    start=_safe_pos(line, col),
                    end=_safe_pos(line, col + token_len)
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

                # Skip if this is a named parameter (followed by = but not ==)
                if self._is_named_parameter(tokens, i):
                    continue

                # Skip if this is a namespace prefix (followed by ::)
                if self._is_namespace_prefix(tokens, i):
                    continue

                seen_warnings.add(name)
                line = token.line - 1
                col = token.column - 1

                diagnostics.append(Diagnostic(
                    range=Range(
                        start=_safe_pos(line, col),
                        end=_safe_pos(line, col + len(name))
                    ),
                    message=f"Variable '{name}' is not defined",
                    severity=DiagnosticSeverity.Warning,
                    source='cssl',
                    code='W001'
                ))

        return diagnostics

    def _collect_names_from_tokens(self, tokens: List[Any]) -> Set[str]:
        """Collect variable names from typed declarations, global/instance declarations, and include statements."""
        registry = get_registry()
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

            # Check for payload("path", "name") - the second string arg is a namespace variable
            if type_name == 'IDENTIFIER' and value == 'payload':
                string_args = []
                for j in range(i + 1, min(i + 12, len(tokens))):
                    nt = tokens[j]
                    if not hasattr(nt, 'type'):
                        continue
                    nt_type = nt.type.name if hasattr(nt.type, 'name') else ''
                    if nt_type == 'STRING':
                        string_args.append(str(nt.value).strip('"\''))
                    elif nt_type in ('SEMICOLON', 'NEWLINE') or str(nt.value) == ')':
                        break
                # Second string argument is the namespace name
                if len(string_args) >= 2:
                    names.add(string_args[1])

            # Check for class/constr parameter lists: class Name(paramA, type paramB, ...) / constr Name(paramA, ...)
            # All identifiers inside these parens are parameter names
            if type_name in ('IDENTIFIER', 'KEYWORD') and value.lower() in ('class', 'constr'):
                # Find opening paren after class/constr name
                paren_depth = 0
                found_paren = False
                for j in range(i + 1, min(i + 50, len(tokens))):
                    nt = tokens[j]
                    if not hasattr(nt, 'type'):
                        continue
                    nt_type = nt.type.name if hasattr(nt.type, 'name') else ''
                    nt_value = str(nt.value) if hasattr(nt, 'value') else ''
                    if nt_type == 'PAREN_START' or nt_value == '(':
                        paren_depth += 1
                        found_paren = True
                    elif nt_type == 'PAREN_END' or nt_value == ')':
                        paren_depth -= 1
                        if paren_depth <= 0:
                            break
                    elif found_paren and paren_depth > 0 and nt_type == 'IDENTIFIER':
                        names.add(str(nt.value))
                    elif nt_type in ('BRACE_START', 'SEMICOLON', 'NEWLINE') and not found_paren:
                        break  # No parens found before body

            # Check for ptr/instance parameter declarations: ptr VarName, instance VarName (in class/constr signatures)
            if type_name in ('IDENTIFIER', 'KEYWORD') and value.lower() in ('ptr', 'instance'):
                for j in range(i + 1, min(i + 4, len(tokens))):
                    nt = tokens[j]
                    if not hasattr(nt, 'type') or not hasattr(nt, 'value'):
                        continue
                    nt_type = nt.type.name if hasattr(nt.type, 'name') else ''
                    if nt_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                        continue
                    if nt_type == 'IDENTIFIER':
                        names.add(str(nt.value))
                    break

            # Check for global/instance/shared declarations: global VarName = ...
            if type_name in ('IDENTIFIER', 'KEYWORD') and value.lower() in ('global', 'instance', 'shared', 'const'):
                # Find the next IDENTIFIER token (skip whitespace, type annotations, etc.)
                for j in range(i + 1, min(i + 8, len(tokens))):
                    nt = tokens[j]
                    if not hasattr(nt, 'type') or not hasattr(nt, 'value'):
                        continue
                    nt_type = nt.type.name if hasattr(nt.type, 'name') else ''
                    nt_value = str(nt.value)
                    if nt_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                        continue
                    if nt_type == 'IDENTIFIER':
                        # Skip if this is a type name (e.g., global vector<dynamic> name)
                        if nt_value.lower() in registry.all_type_names:
                            continue
                        names.add(nt_value)
                        break
                    # Skip type tokens and angle brackets for generics
                    if nt_type in ('TYPE', 'BUILTIN_TYPE', 'LT', 'GT', 'LESS_THAN', 'GREATER_THAN',
                                   'COMMA', 'ANGLE_OPEN', 'ANGLE_CLOSE'):
                        continue
                    break

            # Check for typed declarations: TYPE NAME = ...
            # Look for pattern: type identifier (where type is a known CSSL type)
            if type_name == 'IDENTIFIER' and value.lower() in registry.all_type_names:
                # Find the next IDENTIFIER after the type (skip angle brackets for generics like vector<int>)
                for j in range(i + 1, min(i + 10, len(tokens))):
                    nt = tokens[j]
                    if not hasattr(nt, 'type') or not hasattr(nt, 'value'):
                        continue
                    nt_type = nt.type.name if hasattr(nt.type, 'name') else ''
                    nt_value = str(nt.value)
                    if nt_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                        continue
                    if nt_type == 'IDENTIFIER':
                        # Make sure it's not another type name
                        if nt_value.lower() not in registry.all_type_names:
                            names.add(nt_value)
                        break
                    # Skip angle brackets and their contents for generics like vector<dynamic>
                    if nt_type in ('LT', 'GT', 'LESS_THAN', 'GREATER_THAN', 'COMMA',
                                   'ANGLE_OPEN', 'ANGLE_CLOSE', 'TYPE', 'BUILTIN_TYPE'):
                        continue
                    # Also skip identifier inside angle brackets (it's the generic type param)
                    if nt_value in ('<', '>', ','):
                        continue
                    break

            # Also check for TYPE keyword tokens
            if type_name in ('TYPE', 'BUILTIN_TYPE', 'KEYWORD') and value.lower() in registry.all_type_names:
                for j in range(i + 1, min(i + 10, len(tokens))):
                    nt = tokens[j]
                    if not hasattr(nt, 'type') or not hasattr(nt, 'value'):
                        continue
                    nt_type = nt.type.name if hasattr(nt.type, 'name') else ''
                    nt_value = str(nt.value)
                    if nt_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                        continue
                    if nt_type == 'IDENTIFIER':
                        if nt_value.lower() not in registry.all_type_names:
                            names.add(nt_value)
                        break
                    if nt_type in ('LT', 'GT', 'LESS_THAN', 'GREATER_THAN', 'COMMA',
                                   'ANGLE_OPEN', 'ANGLE_CLOSE', 'TYPE', 'BUILTIN_TYPE'):
                        continue
                    if nt_value in ('<', '>', ','):
                        continue
                    break

            # Check for receive operator targets: ... ==> identifier
            # e.g. MeinSpeicher -==> "CNotes" ==> s;
            # The ==> operator creates/assigns to the target variable
            if type_name == 'IDENTIFIER' and i >= 2:
                for j in range(i - 1, max(0, i - 4), -1):
                    pt = tokens[j]
                    if not hasattr(pt, 'type') or not hasattr(pt, 'value'):
                        continue
                    pt_type = pt.type.name if hasattr(pt.type, 'name') else ''
                    pt_value = str(pt.value)
                    if pt_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                        continue
                    # Found ==> or ==>+ or -==> before this identifier
                    if pt_value in ('==>', '==>+', '-==>') or pt_type in (
                        'RECEIVE', 'RECEIVE_COPY', 'MOVE_RECEIVE',
                        'EXTRACT', 'EXTRACT_COPY', 'MOVE_EXTRACT'
                    ):
                        names.add(value)
                    break

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
        registry = get_registry()
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
                if prev_value in registry.modifiers:
                    continue
                break

        return False

    def _is_type_annotation(self, tokens: List[Any], index: int) -> bool:
        """Check if token looks like a type being used as annotation."""
        registry = get_registry()
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
            if value[0].isupper() or value in registry.all_type_names:
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
        """Check if token is a constructor/destructor name.

        Handles:
        - constr init()          — constructor
        - constr ~init()         — destructor (cleanup)
        - ~init()                — destructor shorthand
        - cleanup init()         — cleanup/destructor
        """
        registry = get_registry()
        if index < 1:
            return False

        # Check previous tokens for 'constr', '~', or 'cleanup' keyword
        for i in range(index - 1, max(0, index - 5), -1):
            prev_token = tokens[i]
            if hasattr(prev_token, 'type') and hasattr(prev_token, 'value'):
                prev_type = prev_token.type.name if hasattr(prev_token.type, 'name') else ''
                prev_value = str(prev_token.value)
                prev_value_lower = prev_value.lower()

                # Found constr or cleanup keyword
                if prev_value_lower in ('constr', 'cleanup'):
                    return True
                # Found ~ (tilde) for destructor syntax
                if prev_value == '~' or prev_type in ('TILDE', 'BITWISE_NOT', 'DESTRUCTOR'):
                    return True
                # Skip whitespace and modifiers
                if prev_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
                    continue
                if prev_value_lower in registry.modifiers:
                    continue
                # Found something else, stop
                break

        return False

    def _is_named_parameter(self, tokens: List[Any], index: int) -> bool:
        """Check if token is a named parameter (followed by = but not ==)."""
        if index + 1 >= len(tokens):
            return False

        next_token = tokens[index + 1]
        if not hasattr(next_token, 'value'):
            return False

        next_value = str(next_token.value)

        # Check for = but not ==
        if next_value == '=':
            # Make sure it's not == (check the token after)
            if index + 2 < len(tokens):
                next_next = tokens[index + 2]
                if hasattr(next_next, 'value') and str(next_next.value) == '=':
                    return False  # This is == comparison, not named param
            return True

        # Also handle ASSIGN token types
        if hasattr(next_token, 'type'):
            next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''
            if next_type in ('ASSIGN', 'EQUALS') and next_value != '==':
                return True

        return False

    def _is_namespace_prefix(self, tokens: List[Any], index: int) -> bool:
        """Check if token is a namespace prefix (followed by ::)."""
        if index + 1 >= len(tokens):
            return False

        # Check next tokens for :: pattern
        for i in range(index + 1, min(index + 3, len(tokens))):
            next_token = tokens[i]
            if hasattr(next_token, 'type'):
                next_type = next_token.type.name if hasattr(next_token.type, 'name') else ''
                next_value = str(next_token.value) if hasattr(next_token, 'value') else ''

                # Found :: operator
                if next_type in ('DOUBLE_COLON', 'COLON_COLON', 'NAMESPACE_SEP') or next_value == '::':
                    return True
                # Skip whitespace
                if next_type in ('WHITESPACE', 'NEWLINE', 'INDENT'):
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
                            start=_safe_pos(line, col),
                            end=_safe_pos(line, col + len(value))
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
                            start=_safe_pos(line, col),
                            end=_safe_pos(line, col + len(value))
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
                            start=_safe_pos(line, col),
                            end=_safe_pos(line, col + len(value))
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
                            start=_safe_pos(line, col),
                            end=_safe_pos(line, col + len(value))
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
                                start=_safe_pos(line, col),
                                end=_safe_pos(line, col + len(name))
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
                    var_name = info.get('name', '')

                    if expected_type and value:
                        actual_type = self._infer_type(value)

                        if actual_type and not self._types_compatible(expected_type, actual_type):
                            line = getattr(node, 'line', 0) - 1
                            col = getattr(node, 'column', 0) - 1

                            # Skip if line info is missing/default (would show on wrong line)
                            if line < 0:
                                continue

                            # Try to find exact position from tokens for better accuracy
                            if var_name and document.tokens:
                                for tok in document.tokens:
                                    if (hasattr(tok, 'value') and str(tok.value) == var_name
                                            and hasattr(tok, 'line') and tok.line > 0):
                                        line = tok.line - 1
                                        col = tok.column - 1 if hasattr(tok, 'column') else 0
                                        break

                            diagnostics.append(Diagnostic(
                                range=Range(
                                    start=_safe_pos(line, col),
                                    end=_safe_pos(line, col + 20)
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
                                    start=_safe_pos(line, col),
                                    end=_safe_pos(line, col + 15)
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
                                    start=_safe_pos(line, col),
                                    end=_safe_pos(line, col + len(method) + 5)
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
                                        start=_safe_pos(line, col),
                                        end=_safe_pos(line, col + 10)
                                    ),
                                    message="Division by zero",
                                    severity=DiagnosticSeverity.Error,
                                    source='cssl',
                                    code='E005'
                                ))

        return diagnostics

    def _invalid_namespace_access_diagnostics(self, document: DocumentAnalysis) -> List[Diagnostic]:
        """E006: Invalid namespace member access."""
        registry = get_registry()
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

                        ns_methods = registry.get_namespace_methods(ns)
                        if ns_methods:
                            method_names = {m.name for m in ns_methods}
                            if member not in method_names:
                                line = token.line - 1
                                col = prev_prev_token.column - 1

                                diagnostics.append(Diagnostic(
                                    range=Range(
                                        start=_safe_pos(line, col),
                                        end=_safe_pos(line, col + len(ns) + 2 + len(member))
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
                                start=_safe_pos(line, col),
                                end=_safe_pos(line, col + len(name) + 7)
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
                                start=_safe_pos(line, col),
                                end=_safe_pos(line, col + len(name) + 6)
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
                        start=_safe_pos(symbol.line - 1, symbol.column - 1),
                        end=_safe_pos(symbol.line - 1, symbol.column - 1 + len(symbol.name))
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
                                    start=_safe_pos(line, col),
                                    end=_safe_pos(line, col + 10)
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
        import re
        registry = get_registry()
        names = registry.get_all_known_names()

        # Add all known namespace names (fmt, std, json, math, etc.)
        names.update(registry.namespaces.keys())
        names.update(registry.module_methods.keys())

        for symbol in document.symbol_table.get_all_symbols_flat():
            names.add(symbol.name)

        # Text-based fallback: scan for common declaration patterns
        # the parser/symbol table may have missed (e.g., when parser times out)
        text = document.source if hasattr(document, 'source') else ''
        if text:
            # global/instance/shared/const declarations
            for m in re.finditer(r'\b(?:global|instance|shared|const)\s+(\w+)', text):
                names.add(m.group(1))
            # Typed declarations: type<generic> varName (handles vector<dynamic> name)
            for m in re.finditer(
                r'\b(?:int|string|float|double|bool|dynamic|dict|json|list|array|'
                r'vector|queue|stack|map|set|tuple|iterator)\s*(?:<[^>]*>)?\s+(\w+)', text):
                names.add(m.group(1))
            # define funcName
            for m in re.finditer(r'\bdefine\s+(\w+)', text):
                names.add(m.group(1))
            # class ClassName
            for m in re.finditer(r'\bclass\s+(\w+)', text):
                names.add(m.group(1))
            # Receive operator targets: ==> varName or ==>+ varName
            for m in re.finditer(r'={2,3}>[\+]?\s+(\w+)', text):
                names.add(m.group(1))

        return names

    def _collect_global_names(self, document: DocumentAnalysis) -> Set[str]:
        """Collect global variable names."""
        import re
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

        # Text-based fallback for when parser times out
        text = document.source if hasattr(document, 'source') else ''
        if text:
            for m in re.finditer(r'\bglobal\s+(\w+)', text):
                names.add(m.group(1))

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
        registry = get_registry()
        return registry.is_known_name(name)

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
        registry = get_registry()
        type_lower = type_name.lower()

        # Strip generic parameters
        if '<' in type_lower:
            type_lower = type_lower.split('<')[0]

        methods = registry.get_type_methods_list(type_lower)
        if methods:
            return any(m.name == method for m in methods)

        # Default: allow any method on unknown types
        return True
