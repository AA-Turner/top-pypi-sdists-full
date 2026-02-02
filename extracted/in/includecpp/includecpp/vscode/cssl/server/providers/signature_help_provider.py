"""
Signature Help Provider for the CSSL Language Server.

Shows parameter hints when the user types inside function/method calls.
Supports:
- Built-in functions (from dynamic registry)
- User-defined functions (from symbol table)
- Class methods (builtin type methods, GUI class methods, user class methods)
- Namespace methods (ns::method)
- Constructor calls (new ClassName)
"""

import re
import logging
from typing import Optional, List, Tuple

from lsprotocol.types import (
    SignatureHelp,
    SignatureInformation,
    ParameterInformation,
    MarkupContent,
    MarkupKind,
    Position,
)

from ..analysis.document_manager import DocumentAnalysis, DocumentManager
from ..utils.symbol_table import SymbolKind
from ..utils.cssl_registry import get_registry, FunctionInfo, MethodInfo

logger = logging.getLogger('cssl-lsp.signature_help')


class SignatureHelpProvider:
    """Provides signature help (parameter hints) for function and method calls."""

    def __init__(self):
        self._document_manager: Optional[DocumentManager] = None

    def set_document_manager(self, dm: DocumentManager) -> None:
        self._document_manager = dm

    def get_signature_help(
        self,
        document: DocumentAnalysis,
        position: Position,
        trigger_character: Optional[str] = None,
    ) -> Optional[SignatureHelp]:
        """Get signature help at the given position.

        Args:
            document: The analyzed document
            position: Cursor position
            trigger_character: Character that triggered signature help

        Returns:
            SignatureHelp or None
        """
        text = document.text
        if not text:
            return None

        line = position.line
        column = position.character

        # Find the function call context at cursor position
        call_info = self._find_call_context(text, line, column)
        if not call_info:
            return None

        func_name, obj_expr, ns_name, active_param = call_info

        # Look up the function/method signature
        signatures = self._resolve_signatures(
            document, func_name, obj_expr, ns_name
        )
        if not signatures:
            return None

        return SignatureHelp(
            signatures=signatures,
            active_signature=0,
            active_parameter=active_param,
        )

    def _find_call_context(
        self, text: str, line: int, column: int
    ) -> Optional[Tuple[str, Optional[str], Optional[str], int]]:
        """Find the function call surrounding the cursor.

        Walks backwards from cursor to find the matching '(' and extract:
        - function name
        - object expression (for obj.method() or this->method())
        - namespace (for ns::func())
        - active parameter index (counting commas)

        Returns:
            (func_name, obj_expr, ns_name, active_param) or None
        """
        lines = text.splitlines()
        if line >= len(lines):
            return None

        line_text = lines[line]
        if column > len(line_text):
            column = len(line_text)

        # Walk backwards from cursor to find the opening '('
        # We need to handle nested parens
        paren_depth = 0
        comma_count = 0
        pos = column - 1  # Start at char before cursor

        # First search on current line
        found_open = False
        open_col = -1

        while pos >= 0:
            ch = line_text[pos]
            if ch == ')':
                paren_depth += 1
            elif ch == '(':
                if paren_depth > 0:
                    paren_depth -= 1
                else:
                    # Found our opening paren
                    found_open = True
                    open_col = pos
                    break
            elif ch == ',' and paren_depth == 0:
                comma_count += 1
            # Skip string literals
            elif ch == '"':
                pos -= 1
                while pos >= 0 and line_text[pos] != '"':
                    if pos > 0 and line_text[pos - 1] == '\\':
                        pos -= 1
                    pos -= 1
            elif ch == "'":
                pos -= 1
                while pos >= 0 and line_text[pos] != "'":
                    pos -= 1
            pos -= 1

        if not found_open:
            # Try searching previous lines (up to 5 lines back for multiline calls)
            for search_line in range(line - 1, max(line - 6, -1), -1):
                if search_line < 0 or search_line >= len(lines):
                    continue
                prev_text = lines[search_line]
                pos = len(prev_text) - 1
                while pos >= 0:
                    ch = prev_text[pos]
                    if ch == ')':
                        paren_depth += 1
                    elif ch == '(':
                        if paren_depth > 0:
                            paren_depth -= 1
                        else:
                            found_open = True
                            open_col = pos
                            line_text = prev_text
                            line = search_line
                            break
                    elif ch == ',' and paren_depth == 0:
                        comma_count += 1
                    pos -= 1
                if found_open:
                    break

        if not found_open:
            return None

        # Now extract the function/method name before the '('
        # Get text before the opening paren on that line
        before_paren = line_text[:open_col].rstrip()
        if not before_paren:
            return None

        # Pattern: this->methodName(
        m = re.search(r'this->(\w+)\s*$', before_paren)
        if m:
            return (m.group(1), 'this', None, comma_count)

        # Pattern: obj.methodName(
        m = re.search(r'(\w+)\.(\w+)\s*$', before_paren)
        if m:
            return (m.group(2), m.group(1), None, comma_count)

        # Pattern: ?ptr.methodName( or @global.methodName(
        m = re.search(r'([?@$%]\w+)\.(\w+)\s*$', before_paren)
        if m:
            return (m.group(2), m.group(1), None, comma_count)

        # Pattern: ns::funcName(
        m = re.search(r'(\w+)::(\w+)\s*$', before_paren)
        if m:
            return (m.group(2), None, m.group(1), comma_count)

        # Pattern: new ClassName(
        m = re.search(r'\bnew\s+(?:\w+::)?(\w+)\s*$', before_paren)
        if m:
            return (m.group(1), None, '__constructor__', comma_count)

        # Pattern: plain funcName(
        m = re.search(r'(\w+)\s*$', before_paren)
        if m:
            return (m.group(1), None, None, comma_count)

        return None

    def _resolve_signatures(
        self,
        document: DocumentAnalysis,
        func_name: str,
        obj_expr: Optional[str],
        ns_name: Optional[str],
    ) -> List[SignatureInformation]:
        """Resolve the function/method to its signature(s).

        Searches in order:
        1. Namespace methods (ns::func)
        2. Constructor calls (new Class)
        3. Object method calls (obj.method, this->method)
        4. Builtin functions
        5. User-defined functions (symbol table)
        6. Cross-document user functions/methods
        """
        registry = get_registry()

        # 1. Namespace method
        if ns_name and ns_name != '__constructor__':
            methods = registry.get_namespace_methods(ns_name)
            if not methods:
                methods = registry.get_module_methods(ns_name)
            for m in methods:
                if m.name == func_name:
                    return [self._method_info_to_signature(m, prefix=f"{ns_name}::")]

        # 2. Constructor
        if ns_name == '__constructor__':
            gui_info = registry.get_gui_class_info(func_name)
            if gui_info:
                return [self._build_constructor_signature(func_name, gui_info.constructor_params)]
            # Check user-defined classes
            sigs = self._resolve_user_class_constructor(document, func_name)
            if sigs:
                return sigs
            # Fallback: just show class name
            return [SignatureInformation(
                label=f"{func_name}()",
                documentation=f"Constructor for {func_name}",
                parameters=[],
            )]

        # 3. Object method call
        if obj_expr:
            sigs = self._resolve_method_on_object(document, obj_expr, func_name)
            if sigs:
                return sigs

        # 4. Builtin function
        info = registry.get_function_info(func_name)
        if info:
            return [self._function_info_to_signature(info)]

        # 5. User-defined function from current document symbol table
        if document.symbol_table:
            for sym in document.symbol_table.get_functions():
                if sym.name == func_name:
                    return [self._symbol_to_signature(sym)]
            # Also check methods inside classes
            for cls in document.symbol_table.get_classes():
                if cls.children:
                    child = cls.children.get(func_name)
                    if child and child.kind in (SymbolKind.METHOD, SymbolKind.FUNCTION):
                        return [self._symbol_to_signature(child, class_name=cls.name)]

        # 6. Cross-document lookup
        sigs = self._resolve_cross_document(func_name, document)
        if sigs:
            return sigs

        # 7. Text-based fallback: scan for define funcName(params)
        sigs = self._resolve_from_text(document, func_name)
        if sigs:
            return sigs

        return []

    def _resolve_method_on_object(
        self,
        document: DocumentAnalysis,
        obj_expr: str,
        method_name: str,
    ) -> List[SignatureInformation]:
        """Resolve a method call on an object expression."""
        registry = get_registry()

        # Handle this-> by finding enclosing class
        if obj_expr == 'this':
            return self._resolve_this_method(document, method_name)

        # Strip prefixes
        var_name = obj_expr
        if var_name and var_name[0] in '?@$%':
            var_name = var_name[1:]

        # Try to infer the type of the object
        inferred_type = None

        # From symbol table
        if document.symbol_table:
            sym = document.symbol_table.get_symbol(var_name)
            if sym and sym.type_info:
                inferred_type = sym.type_info

        # From text-based inference
        if not inferred_type:
            inferred_type = self._infer_type_from_text(document.text, var_name)

        if inferred_type:
            base_type = inferred_type.split('<')[0].strip()

            # Check builtin type methods
            methods = registry.get_type_methods_list(base_type.lower())
            if not methods:
                methods = registry.get_type_methods_list(base_type)

            # Check GUI class methods
            if not methods:
                gui_info = registry.get_gui_class_info(base_type)
                if gui_info:
                    methods = gui_info.methods

            if methods:
                for m in methods:
                    if m.name == method_name:
                        return [self._method_info_to_signature(
                            m, prefix=f"{inferred_type}."
                        )]

            # Check user-defined class methods
            sigs = self._resolve_user_class_method(document, base_type, method_name)
            if sigs:
                return sigs

        return []

    def _resolve_this_method(
        self, document: DocumentAnalysis, method_name: str
    ) -> List[SignatureInformation]:
        """Resolve a this->method() call by finding the enclosing class."""
        # Try symbol table first
        if document.symbol_table:
            for cls in document.symbol_table.get_classes():
                if cls.children:
                    child = cls.children.get(method_name)
                    if child and child.kind in (SymbolKind.METHOD, SymbolKind.FUNCTION):
                        return [self._symbol_to_signature(child, class_name=cls.name)]

        # Text-based fallback
        sigs = self._resolve_from_text(document, method_name)
        return sigs

    def _resolve_user_class_method(
        self,
        document: DocumentAnalysis,
        class_name: str,
        method_name: str,
    ) -> List[SignatureInformation]:
        """Find a method on a user-defined class, across all open documents."""
        docs_to_search = [document]
        if self._document_manager:
            for doc in self._document_manager.get_all_documents():
                if doc.uri != document.uri:
                    docs_to_search.append(doc)

        for doc in docs_to_search:
            # Symbol table lookup
            if doc.symbol_table:
                for cls in doc.symbol_table.get_classes():
                    if cls.name == class_name and cls.children:
                        child = cls.children.get(method_name)
                        if child and child.kind in (SymbolKind.METHOD, SymbolKind.FUNCTION):
                            return [self._symbol_to_signature(child, class_name=class_name)]

            # Text-based fallback: find class block and extract method
            text = doc.text
            if not text:
                continue

            class_pattern = re.compile(
                r'\bclass\s+' + re.escape(class_name) + r'\b[^{]*\{',
                re.DOTALL,
            )
            match = class_pattern.search(text)
            if not match:
                continue

            start = match.end()
            brace_depth = 1
            pos = start
            while pos < len(text) and brace_depth > 0:
                if text[pos] == '{':
                    brace_depth += 1
                elif text[pos] == '}':
                    brace_depth -= 1
                pos += 1
            class_body = text[start:pos - 1] if brace_depth == 0 else text[start:]

            m = re.search(
                r'\bdefine\s+' + re.escape(method_name) + r'\s*\(([^)]*)\)',
                class_body,
            )
            if m:
                params_str = m.group(1).strip()
                return [self._build_signature_from_text(
                    method_name, params_str, class_name=class_name
                )]

        return []

    def _resolve_user_class_constructor(
        self, document: DocumentAnalysis, class_name: str
    ) -> List[SignatureInformation]:
        """Find constructor params for a user-defined class."""
        docs_to_search = [document]
        if self._document_manager:
            for doc in self._document_manager.get_all_documents():
                if doc.uri != document.uri:
                    docs_to_search.append(doc)

        for doc in docs_to_search:
            # Symbol table
            if doc.symbol_table:
                for cls in doc.symbol_table.get_classes():
                    if cls.name == class_name and cls.children:
                        constr = cls.children.get('constr') or cls.children.get(class_name)
                        if constr and constr.kind in (SymbolKind.CONSTRUCTOR, SymbolKind.METHOD, SymbolKind.FUNCTION):
                            return [self._symbol_to_signature(constr, class_name=class_name, is_constructor=True)]

            # Text-based: find constr(...) inside class block
            text = doc.text
            if not text:
                continue

            class_pattern = re.compile(
                r'\bclass\s+' + re.escape(class_name) + r'\b[^{]*\{',
                re.DOTALL,
            )
            match = class_pattern.search(text)
            if not match:
                continue

            start = match.end()
            brace_depth = 1
            pos = start
            while pos < len(text) and brace_depth > 0:
                if text[pos] == '{':
                    brace_depth += 1
                elif text[pos] == '}':
                    brace_depth -= 1
                pos += 1
            class_body = text[start:pos - 1] if brace_depth == 0 else text[start:]

            m = re.search(r'\bconstr\s*\(([^)]*)\)', class_body)
            if m:
                params_str = m.group(1).strip()
                return [self._build_signature_from_text(
                    class_name, params_str, is_constructor=True
                )]

        return []

    def _resolve_cross_document(
        self, func_name: str, current_doc: DocumentAnalysis
    ) -> List[SignatureInformation]:
        """Search all open documents for a function definition."""
        if not self._document_manager:
            return []

        for doc in self._document_manager.get_all_documents():
            if doc.uri == current_doc.uri:
                continue

            # Symbol table
            if doc.symbol_table:
                for sym in doc.symbol_table.get_functions():
                    if sym.name == func_name:
                        return [self._symbol_to_signature(sym)]

            # Text-based
            sigs = self._resolve_from_text(doc, func_name)
            if sigs:
                return sigs

        return []

    def _resolve_from_text(
        self, document: DocumentAnalysis, func_name: str
    ) -> List[SignatureInformation]:
        """Scan document text for define funcName(params) pattern."""
        text = document.text
        if not text:
            return []

        pattern = re.compile(
            r'\bdefine\s+' + re.escape(func_name) + r'\s*\(([^)]*)\)'
        )
        match = pattern.search(text)
        if match:
            params_str = match.group(1).strip()
            return [self._build_signature_from_text(func_name, params_str)]

        return []

    # ------------------------------------------------------------------
    # Signature building helpers
    # ------------------------------------------------------------------

    def _function_info_to_signature(self, info: FunctionInfo) -> SignatureInformation:
        """Convert a FunctionInfo from registry to SignatureInformation."""
        params = []
        param_labels = []
        for p in info.params:
            label = p.name
            if p.type_hint:
                label = f"{p.type_hint} {p.name}"
            if p.default:
                label += f"={p.default}"
            param_labels.append(label)
            doc = p.doc or (f"Type: {p.type_hint}" if p.type_hint else "")
            params.append(ParameterInformation(
                label=label,
                documentation=doc if doc else None,
            ))

        sig_label = f"{info.name}({', '.join(param_labels)})"
        if info.return_type:
            sig_label += f" -> {info.return_type}"

        return SignatureInformation(
            label=sig_label,
            documentation=MarkupContent(
                kind=MarkupKind.Markdown,
                value=info.doc or f"Built-in function `{info.name}`",
            ) if info.doc else f"Built-in function: {info.name}",
            parameters=params,
        )

    def _method_info_to_signature(
        self, info: MethodInfo, prefix: str = ""
    ) -> SignatureInformation:
        """Convert a MethodInfo from registry to SignatureInformation."""
        params = []
        param_labels = []
        for p in info.params:
            label = p.name
            if p.type_hint:
                label = f"{p.type_hint} {p.name}"
            if p.default:
                label += f"={p.default}"
            param_labels.append(label)
            doc = p.doc or (f"Type: {p.type_hint}" if p.type_hint else "")
            params.append(ParameterInformation(
                label=label,
                documentation=doc if doc else None,
            ))

        sig_label = f"{prefix}{info.name}({', '.join(param_labels)})"
        if info.return_type:
            ret = info.return_type.strip("'\"")
            if '.' in ret:
                ret = ret.rsplit('.', 1)[-1]
            sig_label += f" -> {ret}"

        return SignatureInformation(
            label=sig_label,
            documentation=MarkupContent(
                kind=MarkupKind.Markdown,
                value=info.doc or f"Method `{info.name}`",
            ) if info.doc else None,
            parameters=params,
        )

    def _symbol_to_signature(
        self,
        sym,
        class_name: Optional[str] = None,
        is_constructor: bool = False,
    ) -> SignatureInformation:
        """Convert a Symbol from the symbol table to SignatureInformation."""
        params = []
        param_labels = []
        for p in (sym.parameters or []):
            label = p.name
            if p.type_info:
                label = f"{p.type_info} {p.name}"
            param_labels.append(label)
            params.append(ParameterInformation(
                label=label,
                documentation=f"Type: {p.type_info}" if p.type_info else None,
            ))

        display_name = sym.name
        if is_constructor and class_name:
            display_name = f"new {class_name}"
        elif class_name:
            display_name = f"{class_name}.{sym.name}"

        sig_label = f"{display_name}({', '.join(param_labels)})"
        ret = sym.return_type
        if ret and not is_constructor:
            sig_label += f" -> {ret}"

        doc = sym.documentation or ""
        if not doc:
            if is_constructor:
                doc = f"Constructor for class `{class_name}`"
            elif class_name:
                doc = f"Method of class `{class_name}`"
            else:
                doc = f"User-defined function `{sym.name}`"

        return SignatureInformation(
            label=sig_label,
            documentation=MarkupContent(
                kind=MarkupKind.Markdown,
                value=doc,
            ),
            parameters=params,
        )

    def _build_constructor_signature(
        self, class_name: str, params_list
    ) -> SignatureInformation:
        """Build a constructor signature from ParamInfo list."""
        params = []
        param_labels = []
        for p in (params_list or []):
            label = p.name
            if p.type_hint:
                label = f"{p.type_hint} {p.name}"
            if p.default:
                label += f"={p.default}"
            param_labels.append(label)
            params.append(ParameterInformation(
                label=label,
                documentation=f"Type: {p.type_hint}" if p.type_hint else None,
            ))

        sig_label = f"new {class_name}({', '.join(param_labels)})"
        return SignatureInformation(
            label=sig_label,
            documentation=f"Constructor for `{class_name}`",
            parameters=params,
        )

    def _build_signature_from_text(
        self,
        func_name: str,
        params_str: str,
        class_name: Optional[str] = None,
        is_constructor: bool = False,
    ) -> SignatureInformation:
        """Build a signature from a raw parameter string extracted from text."""
        params = []
        param_labels = []

        if params_str:
            for part in params_str.split(','):
                part = part.strip()
                if not part:
                    continue
                # Parse "type name" or just "name"
                tokens = part.split()
                if len(tokens) >= 2:
                    label = f"{tokens[0]} {tokens[1]}"
                    param_labels.append(label)
                    params.append(ParameterInformation(
                        label=label,
                        documentation=f"Type: {tokens[0]}",
                    ))
                else:
                    param_labels.append(part)
                    params.append(ParameterInformation(
                        label=part,
                        documentation=None,
                    ))

        display_name = func_name
        if is_constructor and class_name:
            display_name = f"new {class_name}"
        elif class_name:
            display_name = f"{class_name}.{func_name}"

        sig_label = f"{display_name}({', '.join(param_labels)})"

        doc = ""
        if is_constructor:
            doc = f"Constructor for class `{class_name or func_name}`"
        elif class_name:
            doc = f"Method of class `{class_name}`"
        else:
            doc = f"User-defined function `{func_name}`"

        return SignatureInformation(
            label=sig_label,
            documentation=MarkupContent(
                kind=MarkupKind.Markdown,
                value=doc,
            ),
            parameters=params,
        )

    # ------------------------------------------------------------------
    # Type inference (reuses patterns from completion_provider)
    # ------------------------------------------------------------------

    def _infer_type_from_text(self, text: str, var_name: str) -> Optional[str]:
        """Infer a variable's type by scanning document text."""
        if not text or not var_name:
            return None

        registry = get_registry()

        # Pattern 1: this->VarName = new [ns::]ClassName(...)
        # Pattern 2: VarName = new [ns::]ClassName(...)
        pattern_new = re.compile(
            r'(?:this->)?' + re.escape(var_name) + r'\s*=\s*new\s+(?:\w+::)?(\w+)',
            re.MULTILINE,
        )
        match = pattern_new.search(text)
        if match:
            return match.group(1)

        # Pattern 3: instance VarName = new ns::ClassName(...)
        pattern_instance = re.compile(
            r'instance\s+' + re.escape(var_name) + r'\s*=\s*new\s+(?:\w+::)?(\w+)',
            re.MULTILINE,
        )
        match = pattern_instance.search(text)
        if match:
            return match.group(1)

        # Pattern 4: VarName = obj.method(...) (method return type)
        pattern_method_call = re.compile(
            r'(?:this->)?' + re.escape(var_name) + r'\s*=\s*(?:this->)?(\w+)\.(\w+)\s*\(',
            re.MULTILINE,
        )
        match = pattern_method_call.search(text)
        if match:
            obj_name = match.group(1)
            method_name = match.group(2)
            if obj_name != var_name:
                obj_type = self._infer_type_from_text(text, obj_name)
                if obj_type:
                    ret_type = self._get_method_return_type(obj_type, method_name)
                    if ret_type:
                        return ret_type

        # Pattern 5: TypeName VarName (typed declaration)
        pattern_typed = re.compile(
            r'(\w+(?:<[^>]+>)?)\s+' + re.escape(var_name) + r'\b',
            re.MULTILINE,
        )
        match = pattern_typed.search(text)
        if match:
            type_name = match.group(1)
            base_type = type_name.split('<')[0].lower()
            if base_type in registry.all_type_names or type_name in registry.all_gui_class_names:
                return type_name

        return None

    def _get_method_return_type(self, type_name: str, method_name: str) -> Optional[str]:
        """Look up the return type of a method on a type."""
        registry = get_registry()

        type_lower = type_name.lower().split('<')[0].strip()
        methods = registry.get_type_methods_list(type_lower)
        if not methods:
            methods = registry.get_type_methods_list(type_name.split('<')[0].strip())
        if not methods:
            gui_info = registry.get_gui_class_info(type_name)
            if gui_info:
                methods = gui_info.methods

        if methods:
            for m in methods:
                if m.name == method_name and m.return_type:
                    ret = m.return_type.strip("'\"")
                    if '.' in ret:
                        ret = ret.rsplit('.', 1)[-1]
                    return ret
        return None
