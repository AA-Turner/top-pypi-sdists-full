"""
Completion Provider for the CSSL Language Server.

Provides autocomplete suggestions for CSSL code including:
- Built-in functions and types
- Keywords and modifiers
- Namespace members
- User-defined functions and classes
- Local variables
- Contextual completions based on trigger characters
"""

from typing import List, Optional, Dict, Any
from lsprotocol.types import (
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    InsertTextFormat,
    Position,
    MarkupContent,
    MarkupKind,
)

from ..analysis.document_manager import DocumentAnalysis
from ..utils.symbol_table import SymbolKind
from ..utils.position_utils import get_context_before, get_word_at_position, get_line_text
from ..utils.cssl_registry import get_registry



# Filter operators for [type::operator=value] syntax
FILTER_OPERATORS: List[Dict[str, str]] = [
    {'name': 'gt', 'detail': 'Greater than', 'snippet': 'gt=${1:value}'},
    {'name': 'lt', 'detail': 'Less than', 'snippet': 'lt=${1:value}'},
    {'name': 'ge', 'detail': 'Greater or equal', 'snippet': 'ge=${1:value}'},
    {'name': 'le', 'detail': 'Less or equal', 'snippet': 'le=${1:value}'},
    {'name': 'eq', 'detail': 'Equal to', 'snippet': 'eq=${1:value}'},
    {'name': 'ne', 'detail': 'Not equal to', 'snippet': 'ne=${1:value}'},
    {'name': 'between', 'detail': 'Between two values', 'snippet': 'between=${1:min},${2:max}'},
    {'name': 'contains', 'detail': 'Contains substring', 'snippet': 'contains="${1:text}"'},
    {'name': 'startswith', 'detail': 'Starts with', 'snippet': 'startswith="${1:prefix}"'},
    {'name': 'endswith', 'detail': 'Ends with', 'snippet': 'endswith="${1:suffix}"'},
    {'name': 'like', 'detail': 'Pattern match', 'snippet': 'like="${1:pattern}"'},
    {'name': 'regex', 'detail': 'Regex match', 'snippet': 'regex="${1:pattern}"'},
    {'name': 'in', 'detail': 'In list of values', 'snippet': 'in=[${1:values}]'},
    {'name': 'notin', 'detail': 'Not in list', 'snippet': 'notin=[${1:values}]'},
    {'name': 'null', 'detail': 'Is null', 'snippet': 'null'},
    {'name': 'notnull', 'detail': 'Is not null', 'snippet': 'notnull'},
    {'name': 'empty', 'detail': 'Is empty', 'snippet': 'empty'},
    {'name': 'notempty', 'detail': 'Is not empty', 'snippet': 'notempty'},
]

# Filter type names for [TYPE::operator] syntax
FILTER_TYPES: List[str] = [
    'integer', 'int', 'string', 'str', 'float', 'double', 'bool', 'boolean',
    'date', 'datetime', 'time', 'array', 'list', 'object', 'json', 'any'
]

# BruteInjector filter types for injection [type::helper=value] syntax
INJECTION_FILTER_TYPES: Dict[str, List[Dict[str, str]]] = {
    'string': [
        {'name': 'where', 'detail': 'Exact match filter', 'snippet': 'where="${1:text}"'},
        {'name': 'contains', 'detail': 'Filter strings containing substring', 'snippet': 'contains="${1:text}"'},
        {'name': 'find', 'detail': 'Find substring (non-exact match)', 'snippet': 'find="${1:text}"'},
        {'name': 'findIndex', 'detail': 'Get position of substring (-1 if not found)', 'snippet': 'findIndex="${1:text}"'},
        {'name': 'not', 'detail': 'Exclude matching strings', 'snippet': 'not="${1:text}"'},
        {'name': 'startsWith', 'detail': 'Filter strings starting with prefix', 'snippet': 'startsWith="${1:prefix}"'},
        {'name': 'endsWith', 'detail': 'Filter strings ending with suffix', 'snippet': 'endsWith="${1:suffix}"'},
        {'name': 'length', 'detail': 'Filter strings of specific length', 'snippet': 'length=${1:n}'},
        {'name': 'cut', 'detail': 'Get part before index/substring', 'snippet': 'cut=${1:2}'},
        {'name': 'cutAfter', 'detail': 'Get part after index/substring', 'snippet': 'cutAfter=${1:2}'},
        {'name': 'slice', 'detail': 'Slice string with start:end', 'snippet': 'slice="${1:0}:${2:5}"'},
        {'name': 'split', 'detail': 'Split string by delimiter', 'snippet': 'split="${1:,}"'},
        {'name': 'replace', 'detail': 'Replace old:new in string', 'snippet': 'replace="${1:old}:${2:new}"'},
        {'name': 'upper', 'detail': 'Convert to uppercase', 'snippet': 'upper'},
        {'name': 'lower', 'detail': 'Convert to lowercase', 'snippet': 'lower'},
        {'name': 'trim', 'detail': 'Trim whitespace', 'snippet': 'trim'},
    ],
    'integer': [
        {'name': 'where', 'detail': 'Filter integers matching value', 'snippet': 'where=${1:value}'},
        {'name': 'gt', 'detail': 'Greater than', 'snippet': 'gt=${1:value}'},
        {'name': 'lt', 'detail': 'Less than', 'snippet': 'lt=${1:value}'},
        {'name': 'gte', 'detail': 'Greater than or equal', 'snippet': 'gte=${1:value}'},
        {'name': 'lte', 'detail': 'Less than or equal', 'snippet': 'lte=${1:value}'},
        {'name': 'not', 'detail': 'Not equal', 'snippet': 'not=${1:value}'},
        {'name': 'range', 'detail': 'Filter integers in range [min, max]', 'snippet': 'range=[${1:0}, ${2:100}]'},
    ],
    'json': [
        {'name': 'key', 'detail': 'Extract values with specific key', 'snippet': 'key="${1:key}"'},
        {'name': 'value', 'detail': 'Filter by value in JSON/dict', 'snippet': 'value="${1:val}"'},
    ],
    'array': [
        {'name': 'index', 'detail': 'Get specific index', 'snippet': 'index=${1:0}'},
        {'name': 'length', 'detail': 'Filter arrays of specific length', 'snippet': 'length=${1:n}'},
        {'name': 'where', 'detail': 'Filter elements matching value', 'snippet': 'where=${1:value}'},
    ],
    'vector': [
        {'name': 'where', 'detail': 'Filter elements matching value', 'snippet': 'where=${1:value}'},
        {'name': 'index', 'detail': 'Get specific index', 'snippet': 'index=${1:0}'},
        {'name': 'length', 'detail': 'Filter vectors of specific length', 'snippet': 'length=${1:n}'},
    ],
    'datastruct': [
        {'name': 'at', 'detail': 'Get element at index', 'snippet': 'at=${1:0}'},
        {'name': 'first', 'detail': 'Get first N elements', 'snippet': 'first=${1:1}'},
        {'name': 'last', 'detail': 'Get last N elements', 'snippet': 'last=${1:1}'},
        {'name': 'size', 'detail': 'Get number of elements', 'snippet': 'size'},
        {'name': 'empty', 'detail': 'Pass only if empty', 'snippet': 'empty'},
        {'name': 'notEmpty', 'detail': 'Pass only if not empty', 'snippet': 'notEmpty'},
        {'name': 'contains', 'detail': 'Pass only if contains value', 'snippet': 'contains="${1:value}"'},
        {'name': 'where', 'detail': 'Filter elements matching value', 'snippet': 'where="${1:value}"'},
        {'name': 'not', 'detail': 'Exclude elements matching value', 'snippet': 'not="${1:value}"'},
        {'name': 'slice', 'detail': 'Slice with start:end', 'snippet': 'slice="${1:0}:${2:5}"'},
        {'name': 'reversed', 'detail': 'Reverse element order', 'snippet': 'reversed'},
        {'name': 'sorted', 'detail': 'Sort elements (asc/desc)', 'snippet': 'sorted="${1:asc}"'},
        {'name': 'unique', 'detail': 'Remove duplicate elements', 'snippet': 'unique'},
        {'name': 'flatten', 'detail': 'Flatten nested lists', 'snippet': 'flatten'},
        {'name': 'count', 'detail': 'Count occurrences of value', 'snippet': 'count="${1:value}"'},
        {'name': 'min', 'detail': 'Get minimum value', 'snippet': 'min'},
        {'name': 'max', 'detail': 'Get maximum value', 'snippet': 'max'},
        {'name': 'sum', 'detail': 'Sum all numeric elements', 'snippet': 'sum'},
        {'name': 'avg', 'detail': 'Average of numeric elements', 'snippet': 'avg'},
        {'name': 'join', 'detail': 'Join elements with separator', 'snippet': 'join="${1:,}"'},
        {'name': 'type', 'detail': 'Filter elements by type name', 'snippet': 'type="${1:int}"'},
        {'name': 'gt', 'detail': 'Filter elements greater than value', 'snippet': 'gt=${1:value}'},
        {'name': 'lt', 'detail': 'Filter elements less than value', 'snippet': 'lt=${1:value}'},
        {'name': 'range', 'detail': 'Filter numeric elements in range', 'snippet': 'range="${1:0}:${2:100}"'},
        {'name': 'map', 'detail': 'Convert all elements to strings', 'snippet': 'map'},
    ],
    'stack': [
        {'name': 'peek', 'detail': 'View top element without removing', 'snippet': 'peek'},
        {'name': 'size', 'detail': 'Get number of elements', 'snippet': 'size'},
        {'name': 'empty', 'detail': 'Pass only if empty', 'snippet': 'empty'},
        {'name': 'notEmpty', 'detail': 'Pass only if not empty', 'snippet': 'notEmpty'},
        {'name': 'contains', 'detail': 'Pass only if contains value', 'snippet': 'contains="${1:value}"'},
        {'name': 'toList', 'detail': 'Convert stack to list', 'snippet': 'toList'},
    ],
    'queue': [
        {'name': 'front', 'detail': 'View front element', 'snippet': 'front'},
        {'name': 'back', 'detail': 'View back element', 'snippet': 'back'},
        {'name': 'size', 'detail': 'Get number of elements', 'snippet': 'size'},
        {'name': 'empty', 'detail': 'Pass only if empty', 'snippet': 'empty'},
        {'name': 'notEmpty', 'detail': 'Pass only if not empty', 'snippet': 'notEmpty'},
        {'name': 'contains', 'detail': 'Pass only if contains value', 'snippet': 'contains="${1:value}"'},
        {'name': 'toList', 'detail': 'Convert queue to list', 'snippet': 'toList'},
    ],
    'map': [
        {'name': 'key', 'detail': 'Get value by key', 'snippet': 'key="${1:key}"'},
        {'name': 'keys', 'detail': 'Get all keys as list', 'snippet': 'keys'},
        {'name': 'values', 'detail': 'Get all values as list', 'snippet': 'values'},
        {'name': 'items', 'detail': 'Get all key-value pairs', 'snippet': 'items'},
        {'name': 'size', 'detail': 'Get number of entries', 'snippet': 'size'},
        {'name': 'hasKey', 'detail': 'Pass only if key exists', 'snippet': 'hasKey="${1:key}"'},
        {'name': 'hasValue', 'detail': 'Pass only if value exists', 'snippet': 'hasValue="${1:val}"'},
        {'name': 'where', 'detail': 'Filter entries by value', 'snippet': 'where="${1:value}"'},
        {'name': 'not', 'detail': 'Exclude entries by value', 'snippet': 'not="${1:value}"'},
        {'name': 'empty', 'detail': 'Pass only if empty', 'snippet': 'empty'},
        {'name': 'notEmpty', 'detail': 'Pass only if not empty', 'snippet': 'notEmpty'},
        {'name': 'merge', 'detail': 'Merge with another dict', 'snippet': 'merge'},
        {'name': 'sorted', 'detail': 'Sort by keys (asc/desc)', 'snippet': 'sorted="${1:asc}"'},
        {'name': 'keyType', 'detail': 'Filter entries by key type', 'snippet': 'keyType="${1:string}"'},
        {'name': 'valueType', 'detail': 'Filter entries by value type', 'snippet': 'valueType="${1:int}"'},
    ],
    'dictionary': [
        {'name': 'key', 'detail': 'Get value by key', 'snippet': 'key="${1:key}"'},
        {'name': 'keys', 'detail': 'Get all keys', 'snippet': 'keys'},
        {'name': 'values', 'detail': 'Get all values', 'snippet': 'values'},
        {'name': 'size', 'detail': 'Get number of entries', 'snippet': 'size'},
        {'name': 'hasKey', 'detail': 'Pass only if key exists', 'snippet': 'hasKey="${1:key}"'},
        {'name': 'where', 'detail': 'Filter entries by value', 'snippet': 'where="${1:value}"'},
    ],
    'set': [
        {'name': 'contains', 'detail': 'Pass only if contains value', 'snippet': 'contains="${1:value}"'},
        {'name': 'size', 'detail': 'Get number of elements', 'snippet': 'size'},
        {'name': 'empty', 'detail': 'Pass only if empty', 'snippet': 'empty'},
        {'name': 'toList', 'detail': 'Convert set to list', 'snippet': 'toList'},
        {'name': 'union', 'detail': 'Union with another set', 'snippet': 'union'},
        {'name': 'intersect', 'detail': 'Intersection with another set', 'snippet': 'intersect'},
        {'name': 'diff', 'detail': 'Difference with another set', 'snippet': 'diff'},
    ],
    'tuple': [
        {'name': 'at', 'detail': 'Get element at index', 'snippet': 'at=${1:0}'},
        {'name': 'first', 'detail': 'Get first element', 'snippet': 'first'},
        {'name': 'last', 'detail': 'Get last element', 'snippet': 'last'},
        {'name': 'size', 'detail': 'Get number of elements', 'snippet': 'size'},
        {'name': 'contains', 'detail': 'Pass only if contains value', 'snippet': 'contains="${1:value}"'},
        {'name': 'toList', 'detail': 'Convert tuple to list', 'snippet': 'toList'},
    ],
    'float': [
        {'name': 'round', 'detail': 'Round to N decimal places', 'snippet': 'round=${1:2}'},
        {'name': 'floor', 'detail': 'Round down to integer', 'snippet': 'floor'},
        {'name': 'ceil', 'detail': 'Round up to integer', 'snippet': 'ceil'},
        {'name': 'abs', 'detail': 'Absolute value', 'snippet': 'abs'},
        {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt'},
        {'name': 'gt', 'detail': 'Greater than', 'snippet': 'gt=${1:value}'},
        {'name': 'lt', 'detail': 'Less than', 'snippet': 'lt=${1:value}'},
        {'name': 'between', 'detail': 'Between min and max', 'snippet': 'between="${1:0.0}:${2:1.0}"'},
        {'name': 'positive', 'detail': 'Pass only if positive', 'snippet': 'positive'},
        {'name': 'negative', 'detail': 'Pass only if negative', 'snippet': 'negative'},
    ],
    'bool': [
        {'name': 'isTrue', 'detail': 'Pass only if true', 'snippet': 'isTrue'},
        {'name': 'isFalse', 'detail': 'Pass only if false', 'snippet': 'isFalse'},
        {'name': 'flip', 'detail': 'Negate the boolean', 'snippet': 'flip'},
        {'name': 'toInt', 'detail': 'Convert to 0 or 1', 'snippet': 'toInt'},
    ],
    'combo': [
        {'name': 'filterdb', 'detail': 'Get filter database from combo', 'snippet': 'filterdb'},
        {'name': 'blocked', 'detail': 'Get blocked items from combo', 'snippet': 'blocked'},
    ],
    'dynamic': [
        {'name': 'content', 'detail': 'Filter by content value', 'snippet': 'content=${1:value}'},
        {'name': 'not', 'detail': 'Exclude elements matching value', 'snippet': 'not=${1:value}'},
        {'name': 'gt', 'detail': 'Greater than', 'snippet': 'gt=${1:value}'},
        {'name': 'lt', 'detail': 'Less than', 'snippet': 'lt=${1:value}'},
        {'name': 'gte', 'detail': 'Greater than or equal', 'snippet': 'gte=${1:value}'},
        {'name': 'lte', 'detail': 'Less than or equal', 'snippet': 'lte=${1:value}'},
        {'name': 'mod', 'detail': 'Modulo filter (item % N == 0)', 'snippet': 'mod=${1:2}'},
        {'name': 'range', 'detail': 'Filter values in min:max range', 'snippet': 'range="${1:0}:${2:100}"'},
        {'name': 'even', 'detail': 'Filter even numbers', 'snippet': 'even'},
        {'name': 'odd', 'detail': 'Filter odd numbers', 'snippet': 'odd'},
        {'name': 'VarName', 'detail': 'Filter by variable value', 'snippet': '${1:VarName}=${2:value}'},
    ],
    'sql': [
        {'name': 'data', 'detail': 'Return only SQL-compatible data', 'snippet': 'data'},
    ],
    'instance': [
        {'name': 'class', 'detail': 'Get classes from object', 'snippet': 'class'},
        {'name': 'method', 'detail': 'Get methods from object', 'snippet': 'method'},
        {'name': 'var', 'detail': 'Get variables from object', 'snippet': 'var'},
        {'name': 'all', 'detail': 'Get all categorized members', 'snippet': 'all'},
        {'name': '"ClassName"', 'detail': 'Get specific class by name', 'snippet': '"${1:ClassName}"'},
    ],
    'name': [
        {'name': '"Name"', 'detail': 'Filter by name (class, dict key, attribute)', 'snippet': '"${1:Name}"'},
    ],
    'iterator': [
        {'name': 'toList', 'detail': 'Convert iterator to list', 'snippet': 'toList'},
        {'name': 'count', 'detail': 'Count elements in iterator', 'snippet': 'count'},
        {'name': 'first', 'detail': 'Get first element', 'snippet': 'first'},
    ],
    'position': [
        {'name': 'begin', 'detail': 'Insert at beginning of container', 'snippet': 'begin'},
        {'name': 'end', 'detail': 'Insert at end of container (default)', 'snippet': 'end'},
        {'name': 'at', 'detail': 'Insert at specific index', 'snippet': 'at=${1:0}'},
    ],
}

class CompletionProvider:
    """
    Provides autocomplete suggestions for CSSL code.

    Supports:
    - Trigger character completions (., ::, ?, @, $, %)
    - Keyword and type completions
    - Builtin function completions
    - User-defined function and class completions
    - Local variable completions
    """

    def __init__(self):
        self._builtin_completions: List[CompletionItem] = []
        self._keyword_completions: List[CompletionItem] = []
        self._type_completions: List[CompletionItem] = []
        self._modifier_completions: List[CompletionItem] = []
        self._injection_completions: List[CompletionItem] = []
        self._document_manager = None
        self._build_static_completions()

    def set_document_manager(self, dm):
        """Set reference to the document manager for cross-document lookups."""
        self._document_manager = dm

    def _build_static_completions(self) -> None:
        """Build completion items from the dynamic CSSLRegistry."""
        registry = get_registry()

        # Builtin functions (dynamically extracted from CSSLBuiltins)
        for name, info in sorted(registry.builtin_functions.items()):
            sig = info.signature or f'{name}()'
            doc = info.doc or f'Built-in function: {name}'

            self._builtin_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Function,
                detail=sig,
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{sig}**\n\n{doc}"
                ),
                insert_text=f"{name}($1)",
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"1_{name}"
            ))

        # Keywords
        for name in sorted(registry.keywords):
            self._keyword_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Keyword,
                detail='keyword',
                documentation=f"CSSL keyword: {name}",
                sort_text=f"2_{name}"
            ))

        # Types (with generic syntax hints)
        for name, info in sorted(registry.builtin_types.items()):
            generic = info.generic_syntax  # e.g. "<T>", "<K, V>"
            display = f"{name}{generic}" if generic else name
            doc = info.doc or f'CSSL type: {display}'

            # Build snippet for generic types
            if generic == '<T>':
                snippet = f"{name}<${{1:int}}>"
            elif generic == '<K, V>':
                snippet = f"{name}<${{1:string}}, ${{2:dynamic}}>"
            elif generic == '<T, size>':
                snippet = f"{name}<${{1:int}}, ${{2:dynamic}}>"
            elif generic == '<"name">':
                snippet = f'{name}<"${{1:name}}">'
            else:
                snippet = name

            self._type_completions.append(CompletionItem(
                label=display,
                kind=CompletionItemKind.Class,
                detail='type',
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{display}**\n\n{doc}"
                ),
                insert_text=snippet,
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"1_{name}"
            ))

        # Modifiers
        for name in sorted(registry.modifiers):
            self._modifier_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Keyword,
                detail='modifier',
                documentation=f"Function modifier: {name}",
                sort_text=f"3_{name}"
            ))

        # GUI classes (from cssl-gui)
        for cssl_name, cls_info in sorted(registry.gui_classes.items()):
            # Only show Cssl-prefixed names (not short aliases) to avoid duplicates
            if not cssl_name.startswith('Cssl'):
                continue
            self._builtin_completions.append(CompletionItem(
                label=cssl_name,
                kind=CompletionItemKind.Class,
                detail=f'GUI widget',
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{cssl_name}**\n\n{cls_info.doc or 'CSSL GUI widget class'}"
                ),
                insert_text=f"{cssl_name}($1)",
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"1_{cssl_name}"
            ))

        # Injection operators
        injection_ops = [
            {'label': '<==', 'detail': 'Injection: overwrite target', 'doc': 'Replace target with source.\n\n`target <== source;`\n- Container: overwrites all elements\n- `target[i] <== value` overwrites index i'},
            {'+<==': '+<==', 'label': '+<==', 'detail': 'Injection: add to target', 'doc': 'Copy & add source to target.\n\n`target +<== source;`\n- Container: appends element\n- `target[i] +<== value` merges into index i'},
            {'label': '-<==', 'detail': 'Injection: remove from target', 'doc': 'Remove matching items from target.\n\n`target -<== source;`\n- Removes elements matching source\n- `target[i] -<== value` removes from index i'},
            {'label': '==>', 'detail': 'Receive: move to target', 'doc': 'Move source to target.\n\n`source ==> target;`\n- `source ==> target[i]` sets index i'},
            {'label': '==>+', 'detail': 'Receive: copy to target', 'doc': 'Copy source and add to target.\n\n`source ==>+ target;`'},
            {'label': '-==>', 'detail': 'Receive: move & clear source', 'doc': 'Move source to target and clear source.\n\n`source -==> target;`'},
            {'label': '<<=', 'detail': 'Infuse: inject code into function', 'doc': 'Replace function body with code block.\n\n`funcName <<= { code };`'},
            {'label': '+<<=', 'detail': 'Infuse: add code to function', 'doc': 'Add code block to function.\n\n`funcName +<<= { code };`'},
            {'label': '-<<=', 'detail': 'Infuse: remove code from function', 'doc': 'Remove injected code from function.\n\n`funcName -<<= { code };`'},
        ]
        for op in injection_ops:
            self._injection_completions.append(CompletionItem(
                label=op['label'],
                kind=CompletionItemKind.Operator,
                detail=op['detail'],
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=op['doc']
                ),
                insert_text=f"{op['label']} ",
                sort_text=f"4_{op['label']}"
            ))

    def get_completions(
        self,
        document: DocumentAnalysis,
        position: Position,
        trigger_character: Optional[str] = None
    ) -> CompletionList:
        """
        Get completions at the given position.

        Args:
            document: The analyzed document
            position: Cursor position
            trigger_character: Character that triggered completion

        Returns:
            CompletionList with relevant completions
        """
        items: List[CompletionItem] = []
        text = document.text
        line = position.line
        column = position.character

        # Get context from trigger character
        context_trigger, context_base = get_context_before(text, line, column)

        # Check if we're inside brackets [] for filter syntax
        in_brackets, filter_type = self._check_bracket_context(text, line, column)

        if in_brackets:
            # Inside filter brackets [type::operator]
            if context_trigger == '::' or trigger_character == ':':
                # Show filter operators
                items.extend(self._get_filter_completions(filter_type))
            else:
                # Show filter types
                items.extend(self._get_filter_completions(None))
            return CompletionList(is_incomplete=False, items=items)

        # Handle specific triggers
        if context_trigger == '::' or trigger_character == ':':
            # Namespace member completion (outside brackets)
            items.extend(self._get_namespace_completions(context_base))

        elif context_trigger == '.' or trigger_character == '.':
            # Member access completion
            items.extend(self._get_member_completions(document, context_base, position))

        elif context_trigger == '->' or trigger_character == '>':
            # Arrow member access (this->prop, instance->method)
            items.extend(self._get_arrow_completions(document, context_base, position))

        elif context_trigger == '?' or trigger_character == '?':
            # Pointer reference - show defined variables
            items.extend(self._get_pointer_completions(document))

        elif context_trigger == '@' or trigger_character == '@':
            # Global reference - show global variables
            items.extend(self._get_global_completions(document))

        elif context_trigger == '$' or trigger_character == '$':
            # Shared reference - show shared variables
            items.extend(self._get_shared_completions(document))

        elif context_trigger == '%' or trigger_character == '%':
            # Snapshot reference - show snapshots
            items.extend(self._get_snapshot_completions(document))

        else:
            # General completions
            items.extend(self._builtin_completions)
            items.extend(self._keyword_completions)
            items.extend(self._type_completions)
            items.extend(self._modifier_completions)
            items.extend(self._injection_completions)
            items.extend(self._get_local_variable_completions(document, position))
            items.extend(self._get_user_function_completions(document))
            items.extend(self._get_user_class_completions(document))
            items.extend(self._get_namespace_triggers())
            # Text-based fallback: extract symbols the semantic analyzer may have missed
            items.extend(self._get_text_based_completions(document))

        # Mark triggered completions as incomplete so VS Code re-requests
        # when context changes (e.g., user deletes the '.' trigger)
        is_triggered = context_trigger is not None or trigger_character is not None
        return CompletionList(is_incomplete=is_triggered, items=items)

    def _get_namespace_completions(self, namespace: Optional[str]) -> List[CompletionItem]:
        """Get completions for namespace members (dynamically from registry)."""
        items: List[CompletionItem] = []
        registry = get_registry()

        if not namespace:
            # Show all known namespaces
            all_ns = set(registry.namespaces.keys()) | set(registry.module_methods.keys())
            for ns_name in sorted(all_ns):
                items.append(CompletionItem(
                    label=ns_name,
                    kind=CompletionItemKind.Module,
                    detail='namespace',
                    documentation=f"CSSL namespace: {ns_name}",
                    insert_text=f"{ns_name}::",
                    sort_text=f"0_{ns_name}"
                ))
            return items

        # Find matching namespace/module methods
        methods = registry.get_namespace_methods(namespace)
        if not methods:
            methods = registry.get_module_methods(namespace)

        for method in methods:
            sig = method.signature or f"{method.name}()"
            doc = method.doc or ''
            items.append(CompletionItem(
                label=method.name,
                kind=CompletionItemKind.Method,
                detail=sig,
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{namespace}::{sig}**\n\n{doc}"
                ),
                insert_text=f"{method.name}($1)",
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"0_{method.name}"
            ))

        return items

    def _get_member_completions(
        self,
        document: DocumentAnalysis,
        base_expression: Optional[str],
        position: Position
    ) -> List[CompletionItem]:
        """Get completions for member access (.) - FULL CONTEXT AWARE.

        Handles:
        - Variable.method() - based on variable type
        - ?pointer.method() - pointer dereference, show target type methods
        - @globalVar.method() - global variable methods
        - %snapshot.method() - snapshot variable methods
        - classInstance.method() - class instance methods AND properties
        """
        items: List[CompletionItem] = []

        if not base_expression:
            return self._get_generic_member_completions()

        # Strip special prefixes and track what kind of reference it is
        var_name = base_expression
        is_pointer = var_name.startswith('?')
        is_global = var_name.startswith('@')
        is_shared = var_name.startswith('$')
        is_snapshot = var_name.startswith('%')

        if is_pointer or is_global or is_shared or is_snapshot:
            var_name = var_name[1:]

        # Try to find the symbol in the document
        symbol = None
        if document.symbol_table:
            symbol = document.symbol_table.get_symbol(var_name)

            # Also search in globals if it's a global reference
            if not symbol and is_global:
                for s in document.symbol_table.get_globals():
                    if s.name == var_name:
                        symbol = s
                        break

        # Determine the type
        inferred_type = None
        class_symbol = None

        if symbol:
            inferred_type = symbol.type_info

            # Check if this is a class instance - find the class definition
            if inferred_type and document.symbol_table:
                # Remove generic parameters for lookup
                base_type = inferred_type.split('<')[0].strip()

                # Check if it's a user-defined class
                for cls in document.symbol_table.get_classes():
                    if cls.name == base_type:
                        class_symbol = cls
                        break

        # If we found a class, show its methods and properties
        if class_symbol and class_symbol.children:
            for name, child in class_symbol.children.items():
                if child.kind == SymbolKind.METHOD or child.kind == SymbolKind.FUNCTION:
                    # Build parameter list for method
                    params = []
                    for p in (child.parameters or []):
                        p_type = p.type_info or ''
                        params.append(f"{p_type} {p.name}" if p_type else p.name)
                    param_str = ', '.join(params)

                    items.append(CompletionItem(
                        label=name,
                        kind=CompletionItemKind.Method,
                        detail=f"({param_str}) -> {child.return_type or 'void'}",
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"**{name}**({param_str})\n\nMethod of class `{class_symbol.name}`"
                        ),
                        insert_text=f"{name}($1)",
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"0_{name}"
                    ))
                elif child.kind == SymbolKind.PROPERTY or child.kind == SymbolKind.VARIABLE:
                    items.append(CompletionItem(
                        label=name,
                        kind=CompletionItemKind.Property,
                        detail=child.type_info or 'dynamic',
                        documentation=f"Property of class `{class_symbol.name}`",
                        sort_text=f"0_{name}"
                    ))

        # If no type found yet from symbol table, try text-based inference
        registry = get_registry()
        if not inferred_type:
            inferred_type = self._infer_type_from_text(document.text, var_name)

        if inferred_type:
            type_lower = inferred_type.lower().split('<')[0].strip()
            methods = registry.get_type_methods_list(type_lower)
            # Also try exact case (for GUI classes like CsslButton)
            if not methods:
                methods = registry.get_type_methods_list(inferred_type.split('<')[0].strip())
            # Also try GUI class info lookup
            if not methods:
                gui_info = registry.get_gui_class_info(inferred_type)
                if gui_info:
                    methods = gui_info.methods

            for method in methods:
                # Don't add duplicates from class methods
                if not any(item.label == method.name for item in items):
                    sig = method.signature or f"{method.name}()"
                    doc = method.doc or ''
                    # Build snippet from params
                    if method.params:
                        param_snippets = [f"${{{i+1}:{p.name}}}" for i, p in enumerate(method.params)]
                        snippet = f"{method.name}({', '.join(param_snippets)})"
                    else:
                        snippet = f"{method.name}()"
                    items.append(CompletionItem(
                        label=method.name,
                        kind=CompletionItemKind.Method,
                        detail=sig,
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"**{sig}**\n\n{doc}"
                        ),
                        insert_text=snippet,
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"1_{method.name}"
                    ))

        # If still no items, try to infer type from expression pattern or text scan
        if not items:
            inferred_type = self._infer_expression_type(document, base_expression)
            # If expression inference failed, scan document text for assignment patterns
            if not inferred_type:
                inferred_type = self._infer_type_from_text(document.text, var_name)
            if inferred_type:
                type_lower = inferred_type.lower()
                methods = registry.get_type_methods_list(type_lower)
                if not methods:
                    methods = registry.get_type_methods_list(inferred_type)
                # Also try GUI class lookup by exact name
                if not methods:
                    gui_info = registry.get_gui_class_info(inferred_type)
                    if gui_info:
                        methods = gui_info.methods
                for method in methods:
                    sig = method.signature or f"{method.name}()"
                    if method.params:
                        param_snippets = [f"${{{i+1}:{p.name}}}" for i, p in enumerate(method.params)]
                        snippet = f"{method.name}({', '.join(param_snippets)})"
                    else:
                        snippet = f"{method.name}()"
                    items.append(CompletionItem(
                        label=method.name,
                        kind=CompletionItemKind.Method,
                        detail=sig,
                        insert_text=snippet,
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"0_{method.name}"
                    ))

        # If still no items, search all open documents for user-defined class
        if not items and inferred_type:
            items = self._get_user_class_member_completions(inferred_type, document)

        # If STILL no items, show generic methods as last resort
        if not items:
            items = self._get_generic_member_completions()

        return items

    def _get_arrow_completions(
        self,
        document: DocumentAnalysis,
        base_expression: Optional[str],
        position: Position
    ) -> List[CompletionItem]:
        """Get completions for arrow access (->) - class properties and methods.

        Handles:
        - this->propName  (current class properties/methods)
        - instance->member (instance member access, same as dot)
        """
        items: List[CompletionItem] = []

        if base_expression == 'this' or not base_expression:
            # this-> : show all properties and methods of the enclosing class
            # Find the class we're inside by scanning for class definition above cursor
            import re
            text = document.text
            lines = text.splitlines()
            # Walk backwards from current line to find the enclosing class
            class_name = None
            brace_depth = 0
            for i in range(position.line, -1, -1):
                line_text = lines[i] if i < len(lines) else ''
                # Count braces on this line (simplified)
                for ch in reversed(line_text):
                    if ch == '}':
                        brace_depth += 1
                    elif ch == '{':
                        brace_depth -= 1
                # If brace_depth goes negative, we found an opening brace
                if brace_depth < 0:
                    # Check if this line or previous has a class definition
                    for j in range(i, max(i - 3, -1), -1):
                        if j >= 0 and j < len(lines):
                            m = re.search(r'\bclass\s+(\w+)', lines[j])
                            if m:
                                class_name = m.group(1)
                                break
                    break

            if class_name:
                # Show class members via member completion
                items = self._get_member_completions(document, class_name, position)
                if not items:
                    # Try text-based extraction
                    items = self._get_user_class_member_completions(class_name, document)

            if not items:
                # Fallback: show all this-> properties found in document text
                seen = set()
                for m in re.finditer(r'this->(\w+)', text):
                    name = m.group(1)
                    if name not in seen:
                        seen.add(name)
                        items.append(CompletionItem(
                            label=name,
                            kind=CompletionItemKind.Property,
                            detail='property',
                            sort_text=f"0_{name}"
                        ))
                # Also show all methods defined in enclosing class
                for m in re.finditer(r'\bdefine\s+(\w+)\s*\(', text):
                    name = m.group(1)
                    if name not in seen:
                        seen.add(name)
                        items.append(CompletionItem(
                            label=name,
                            kind=CompletionItemKind.Method,
                            detail='method',
                            insert_text=f"{name}($1)",
                            insert_text_format=InsertTextFormat.Snippet,
                            sort_text=f"0_{name}"
                        ))
        else:
            # instance->member : treat same as dot access
            items = self._get_member_completions(document, base_expression, position)

        return items

    def _get_user_class_member_completions(
        self,
        class_name: str,
        current_doc: DocumentAnalysis
    ) -> List[CompletionItem]:
        """Search all open documents for a user-defined class and extract its members.

        Uses text-based scanning to find class definitions and their methods/properties.
        Works across files (e.g., class defined in gui.cssl, used in main.cssl).
        """
        import re
        items: List[CompletionItem] = []
        seen_names: set = set()

        # Strip namespace prefix (e.g., cnotes_gui::CNotesGUI -> CNotesGUI)
        base_name = class_name.split('::')[-1].split('<')[0].strip()

        # Collect all document texts to search
        docs_to_search = [current_doc]
        if self._document_manager:
            for doc in self._document_manager.get_all_documents():
                if doc.uri != current_doc.uri:
                    docs_to_search.append(doc)

        for doc in docs_to_search:
            text = doc.text
            if not text:
                continue

            # First try symbol table (faster, more accurate)
            if doc.symbol_table:
                for cls in doc.symbol_table.get_classes():
                    if cls.name == base_name and cls.children:
                        for name, child in cls.children.items():
                            if name in seen_names:
                                continue
                            seen_names.add(name)

                            if child.kind in (SymbolKind.METHOD, SymbolKind.FUNCTION):
                                params = []
                                for p in (child.parameters or []):
                                    p_type = p.type_info or ''
                                    params.append(f"{p_type} {p.name}" if p_type else p.name)
                                param_str = ', '.join(params)
                                items.append(CompletionItem(
                                    label=name,
                                    kind=CompletionItemKind.Method,
                                    detail=f"({param_str}) -> {child.return_type or 'void'}",
                                    documentation=MarkupContent(
                                        kind=MarkupKind.Markdown,
                                        value=f"**{name}**({param_str})\n\nMethod of `{base_name}`"
                                    ),
                                    insert_text=f"{name}($1)",
                                    insert_text_format=InsertTextFormat.Snippet,
                                    sort_text=f"0_{name}"
                                ))
                            elif child.kind in (SymbolKind.PROPERTY, SymbolKind.VARIABLE):
                                items.append(CompletionItem(
                                    label=name,
                                    kind=CompletionItemKind.Property,
                                    detail=child.type_info or 'dynamic',
                                    documentation=f"Property of `{base_name}`",
                                    sort_text=f"0_{name}"
                                ))

                if items:
                    return items  # Found in symbol table, done

            # Fallback: text-based class member extraction
            # Find class block: class ClassName ... { ... }
            class_pattern = re.compile(
                r'\bclass\s+' + re.escape(base_name) + r'\b[^{]*\{',
                re.DOTALL
            )
            match = class_pattern.search(text)
            if not match:
                continue

            # Find the matching closing brace
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

            # Extract methods: define methodName(...)
            for m in re.finditer(r'\bdefine\s+(\w+)\s*\(([^)]*)\)', class_body):
                name = m.group(1)
                params = m.group(2).strip()
                if name not in seen_names:
                    seen_names.add(name)
                    items.append(CompletionItem(
                        label=name,
                        kind=CompletionItemKind.Method,
                        detail=f"({params})" if params else "()",
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"**{name}**({params})\n\nMethod of `{base_name}`"
                        ),
                        insert_text=f"{name}($1)",
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"0_{name}"
                    ))

            # Extract properties: this->propName
            for m in re.finditer(r'this->(\w+)', class_body):
                name = m.group(1)
                if name not in seen_names:
                    seen_names.add(name)
                    # Try to infer property type from assignment
                    prop_type = 'dynamic'
                    type_match = re.search(
                        r'this->' + re.escape(name) + r'\s*=\s*new\s+(?:\w+::)?(\w+)',
                        class_body
                    )
                    if type_match:
                        prop_type = type_match.group(1)
                    items.append(CompletionItem(
                        label=name,
                        kind=CompletionItemKind.Property,
                        detail=prop_type,
                        documentation=f"Property of `{base_name}`",
                        sort_text=f"0_{name}"
                    ))

            if items:
                return items

        return items

    def _get_generic_member_completions(self) -> List[CompletionItem]:
        """Get generic member completions when type is unknown."""
        items: List[CompletionItem] = []
        common_methods = [
            {'name': 'length', 'detail': 'Get length/size', 'snippet': 'length()'},
            {'name': 'size', 'detail': 'Get size', 'snippet': 'size()'},
            {'name': 'toString', 'detail': 'Convert to string', 'snippet': 'toString()'},
            {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt()'},
            {'name': 'toFloat', 'detail': 'Convert to float', 'snippet': 'toFloat()'},
            {'name': 'contains', 'detail': 'Check if contains value', 'snippet': 'contains(${1:item})'},
            {'name': 'get', 'detail': 'Get value', 'snippet': 'get(${1:key})'},
            {'name': 'set', 'detail': 'Set value', 'snippet': 'set(${1:key}, ${2:value})'},
            {'name': 'keys', 'detail': 'Get keys', 'snippet': 'keys()'},
            {'name': 'values', 'detail': 'Get values', 'snippet': 'values()'},
            {'name': 'push', 'detail': 'Add element', 'snippet': 'push(${1:item})'},
            {'name': 'pop', 'detail': 'Remove last element', 'snippet': 'pop()'},
            {'name': 'clear', 'detail': 'Clear all', 'snippet': 'clear()'},
            {'name': 'isEmpty', 'detail': 'Check if empty', 'snippet': 'isEmpty()'},
            {'name': 'indexOf', 'detail': 'Find index', 'snippet': 'indexOf(${1:item})'},
        ]
        for method in common_methods:
            items.append(CompletionItem(
                label=method['name'],
                kind=CompletionItemKind.Method,
                detail=method.get('detail', ''),
                insert_text=method.get('snippet', method['name']),
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"1_{method['name']}"
            ))
        return items

    def _get_filter_completions(self, filter_type: Optional[str]) -> List[CompletionItem]:
        """Get completions for filter operators inside [type::operator=value]."""
        items: List[CompletionItem] = []

        # First show filter types if no type specified
        if not filter_type:
            # Standard query filter types
            for type_name in FILTER_TYPES:
                items.append(CompletionItem(
                    label=type_name,
                    kind=CompletionItemKind.TypeParameter,
                    detail='filter type',
                    documentation=f"Filter by {type_name} type",
                    insert_text=f"{type_name}::",
                    sort_text=f"0_{type_name}"
                ))
            # Injection-specific BruteInjector filter types
            for inj_type in sorted(INJECTION_FILTER_TYPES.keys()):
                if inj_type not in FILTER_TYPES:
                    items.append(CompletionItem(
                        label=inj_type,
                        kind=CompletionItemKind.TypeParameter,
                        detail='injection filter',
                        documentation=f"BruteInjector filter: {inj_type}",
                        insert_text=f"{inj_type}::",
                        sort_text=f"0_{inj_type}"
                    ))
            return items

        # Show BruteInjector-specific helpers for this type first
        inj_helpers = INJECTION_FILTER_TYPES.get(filter_type, [])
        for helper in inj_helpers:
            items.append(CompletionItem(
                label=helper['name'],
                kind=CompletionItemKind.Method,
                detail=helper.get('detail', ''),
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{filter_type}::{helper['name']}**\n\n{helper.get('detail', '')}\n\nUsage: `[{filter_type}::{helper['name']}]`"
                ),
                insert_text=helper.get('snippet', helper['name']),
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"0_{helper['name']}"
            ))

        # Show generic filter operators
        for op in FILTER_OPERATORS:
            items.append(CompletionItem(
                label=op['name'],
                kind=CompletionItemKind.Operator,
                detail=op.get('detail', ''),
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{op['name']}**\n\n{op.get('detail', '')}\n\nUsage: `[{filter_type}::{op['name']}=value]`"
                ),
                insert_text=op.get('snippet', op['name']),
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"1_{op['name']}"
            ))

        return items

    def _get_pointer_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Get completions for pointer references (?)."""
        items: List[CompletionItem] = []

        if document.symbol_table:
            for symbol in document.symbol_table.get_all_symbols_flat():
                if symbol.kind in (SymbolKind.VARIABLE, SymbolKind.PARAMETER):
                    items.append(CompletionItem(
                        label=symbol.name,
                        kind=CompletionItemKind.Variable,
                        detail=f"pointer to {symbol.name}",
                        documentation=f"Create pointer reference to variable '{symbol.name}'",
                        sort_text=f"0_{symbol.name}"
                    ))

        return items

    def _get_global_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Get completions for global references (@)."""
        items: List[CompletionItem] = []

        if document.symbol_table:
            for symbol in document.symbol_table.get_globals():
                items.append(CompletionItem(
                    label=symbol.name,
                    kind=CompletionItemKind.Variable,
                    detail=f"global: {symbol.name}",
                    documentation=f"Global variable '{symbol.name}'",
                    sort_text=f"0_{symbol.name}"
                ))

        return items

    def _get_shared_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Get completions for shared references ($)."""
        items: List[CompletionItem] = []

        if document.symbol_table:
            for symbol in document.symbol_table.get_shared():
                items.append(CompletionItem(
                    label=symbol.name,
                    kind=CompletionItemKind.Variable,
                    detail=f"shared: {symbol.name}",
                    documentation=f"Shared variable '{symbol.name}'",
                    sort_text=f"0_{symbol.name}"
                ))

        return items

    def _get_snapshot_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Get completions for snapshot references (%)."""
        items: List[CompletionItem] = []

        # Find snapshot() calls in the document
        if document.tokens:
            for i, token in enumerate(document.tokens):
                if hasattr(token, 'value') and token.value == 'snapshot':
                    # Look for the next identifier as the snapshot name
                    if i + 2 < len(document.tokens):
                        name_token = document.tokens[i + 2]
                        if hasattr(name_token, 'value') and name_token.value:
                            name = name_token.value
                            if name not in [item.label for item in items]:
                                items.append(CompletionItem(
                                    label=name,
                                    kind=CompletionItemKind.Reference,
                                    detail=f"snapshot: {name}",
                                    documentation=f"Snapshot of variable '{name}'",
                                    sort_text=f"0_{name}"
                                ))

        return items

    def _get_local_variable_completions(
        self,
        document: DocumentAnalysis,
        position: Position
    ) -> List[CompletionItem]:
        """Get completions for local variables."""
        items: List[CompletionItem] = []

        if document.symbol_table:
            for symbol in document.symbol_table.get_all_symbols_flat():
                if symbol.kind in (SymbolKind.VARIABLE, SymbolKind.PARAMETER):
                    # Only show variables defined before current position
                    if symbol.line <= position.line + 1:
                        type_info = symbol.type_info or 'dynamic'
                        items.append(CompletionItem(
                            label=symbol.name,
                            kind=CompletionItemKind.Variable,
                            detail=type_info,
                            documentation=f"Variable: {symbol.name} ({type_info})",
                            sort_text=f"0_{symbol.name}"  # Highest priority
                        ))

        return items

    def _get_user_function_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Get completions for user-defined functions."""
        items: List[CompletionItem] = []

        if document.symbol_table:
            for symbol in document.symbol_table.get_functions():
                if symbol.kind == SymbolKind.FUNCTION:
                    # Build parameter list
                    params = []
                    for i, param in enumerate(symbol.parameters or []):
                        param_type = param.type_info or ''
                        param_str = f"{param_type} {param.name}" if param_type else param.name
                        params.append(param_str)

                    param_list = ', '.join(params)
                    return_type = symbol.return_type or 'void'

                    # Build snippet with parameter placeholders
                    snippet_params = []
                    for i, param in enumerate(symbol.parameters or []):
                        snippet_params.append(f"${{{i+1}:{param.name}}}")
                    snippet = f"{symbol.name}({', '.join(snippet_params)})"

                    items.append(CompletionItem(
                        label=symbol.name,
                        kind=CompletionItemKind.Function,
                        detail=f"({param_list}) -> {return_type}",
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"**{symbol.name}**({param_list}) -> {return_type}\n\nUser-defined function at line {symbol.line}"
                        ),
                        insert_text=snippet,
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"0_{symbol.name}"
                    ))

        return items

    def _get_user_class_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Get completions for user-defined classes."""
        items: List[CompletionItem] = []

        if document.symbol_table:
            for symbol in document.symbol_table.get_classes():
                items.append(CompletionItem(
                    label=symbol.name,
                    kind=CompletionItemKind.Class,
                    detail='class',
                    documentation=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"**class {symbol.name}**\n\nUser-defined class at line {symbol.line}"
                    ),
                    insert_text=f"new {symbol.name}($1)",
                    insert_text_format=InsertTextFormat.Snippet,
                    sort_text=f"0_{symbol.name}"
                ))

        return items

    def _get_namespace_triggers(self) -> List[CompletionItem]:
        """Get namespace completion triggers (ns::)."""
        items: List[CompletionItem] = []
        registry = get_registry()

        all_ns = set(registry.namespaces.keys()) | set(registry.module_methods.keys())
        for ns_name in sorted(all_ns):
            items.append(CompletionItem(
                label=f"{ns_name}::",
                kind=CompletionItemKind.Module,
                detail='namespace',
                documentation=f"Access {ns_name} namespace members",
                insert_text=f"{ns_name}::",
                sort_text=f"1_{ns_name}"
            ))

        return items

    def _get_text_based_completions(self, document: DocumentAnalysis) -> List[CompletionItem]:
        """Extract symbols from document text that the semantic analyzer may have missed.

        Scans for:
        - define funcName() patterns (user-defined functions/methods)
        - this->propName = ... patterns (class properties/instances)
        - varName = new ClassName() patterns (local instances)
        """
        import re
        items: List[CompletionItem] = []
        existing_labels: set = set()

        text = document.text
        if not text:
            return items

        # Collect labels already in symbol table to avoid duplicates
        if document.symbol_table:
            for s in document.symbol_table.get_all_symbols_flat():
                existing_labels.add(s.name)

        # Pattern 1: define funcName(...) — user-defined functions/methods
        for match in re.finditer(r'\bdefine\s+(\w+)\s*\(', text):
            name = match.group(1)
            if name not in existing_labels:
                existing_labels.add(name)
                items.append(CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Function,
                    detail='user function',
                    insert_text=f"{name}($1)",
                    insert_text_format=InsertTextFormat.Snippet,
                    sort_text=f"0_{name}"
                ))

        # Pattern 2: this->propName = new ClassName(...) — class properties
        for match in re.finditer(r'this->(\w+)\s*=\s*new\s+(\w+)', text):
            name = match.group(1)
            type_name = match.group(2)
            if name not in existing_labels:
                existing_labels.add(name)
                items.append(CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Property,
                    detail=type_name,
                    documentation=f"Instance of {type_name}",
                    sort_text=f"0_{name}"
                ))

        # Pattern 3: this->propName = ... (non-new assignments)
        for match in re.finditer(r'this->(\w+)\s*=\s*(?!new\b)', text):
            name = match.group(1)
            if name not in existing_labels:
                existing_labels.add(name)
                items.append(CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Property,
                    detail='property',
                    sort_text=f"0_{name}"
                ))

        # Pattern 4: varName = new ClassName(...) — local instances
        for match in re.finditer(r'\b(\w+)\s*=\s*new\s+(\w+)', text):
            name = match.group(1)
            type_name = match.group(2)
            if name not in existing_labels and name != 'this':
                existing_labels.add(name)
                items.append(CompletionItem(
                    label=name,
                    kind=CompletionItemKind.Variable,
                    detail=type_name,
                    documentation=f"Instance of {type_name}",
                    sort_text=f"0_{name}"
                ))

        return items

    def _infer_expression_type(
        self,
        document: DocumentAnalysis,
        expression: Optional[str]
    ) -> Optional[str]:
        """Try to infer the type of an expression."""
        if not expression:
            return None

        registry = get_registry()

        # Check if it's a direct variable reference
        if document.symbol_table:
            symbol = document.symbol_table.get_symbol(expression)
            if symbol and symbol.type_info:
                return symbol.type_info

        # Check if expression matches known type names
        if expression.lower() in registry.all_type_names:
            return expression.lower()

        # Check if it's a GUI class name
        if expression in registry.all_gui_class_names:
            return expression

        # Check for constructor calls: new ClassName()
        if expression.startswith('new '):
            class_name = expression[4:].strip('() ')
            return class_name

        # Check for namespace prefixes
        if '::' in expression:
            ns, _ = expression.rsplit('::', 1)
            ns_lower = ns.lower()
            if ns_lower in registry.namespaces:
                return ns_lower

        return None

    def _infer_type_from_text(self, text: str, var_name: str) -> Optional[str]:
        """Infer a variable's type by scanning the document text for assignment patterns.

        Handles patterns like:
        - this->VarName = new CsslToolbar(...)
        - VarName = new CsslButton(...)
        - vector<int> VarName
        - instance VarName = new ns::ClassName()
        - this->VarName = this->Other.addMenu(...)  (method return type)
        """
        import re

        if not text or not var_name:
            return None

        registry = get_registry()

        # Pattern 1: this->VarName = new [ns::/ns.]ClassName(...)
        # Pattern 2: VarName = new [ns::/ns.]ClassName(...)
        pattern_new = re.compile(
            r'(?:this->)?' + re.escape(var_name) + r'\s*=\s*new\s+(?:\w+(?:::|\.))?\s*(\w+)',
            re.MULTILINE
        )
        match = pattern_new.search(text)
        if match:
            return match.group(1)

        # Pattern 3: instance VarName = new ns::/ns.ClassName(...)
        pattern_instance = re.compile(
            r'instance\s+' + re.escape(var_name) + r'\s*=\s*new\s+(?:\w+(?:::|\.))?\s*(\w+)',
            re.MULTILINE
        )
        match = pattern_instance.search(text)
        if match:
            return match.group(1)

        # Pattern 4: VarName = something.methodName(...)  (method return type inference)
        # Matches: this->Var = this->Other.method(...) or Var = obj.method(...)
        pattern_method_call = re.compile(
            r'(?:this->)?' + re.escape(var_name) + r'\s*=\s*(?:this->)?(\w+)\.(\w+)\s*\(',
            re.MULTILINE
        )
        match = pattern_method_call.search(text)
        if match:
            obj_name = match.group(1)
            method_name = match.group(2)
            # Infer the type of the object first (recursive, but limited depth)
            obj_type = self._infer_type_from_text(text, obj_name) if obj_name != var_name else None
            if obj_type:
                # Look up the method's return type from the registry
                ret_type = self._get_method_return_type(obj_type, method_name)
                if ret_type:
                    return ret_type

        # Pattern 5: VarName = ns::methodName(...)  (namespace method return type)
        pattern_ns_call = re.compile(
            r'(?:this->)?' + re.escape(var_name) + r'\s*=\s*(\w+)::(\w+)\s*\(',
            re.MULTILINE
        )
        match = pattern_ns_call.search(text)
        if match:
            ns_name = match.group(1)
            method_name = match.group(2)
            ns_methods = registry.get_namespace_methods(ns_name) or registry.get_module_methods(ns_name)
            for m in ns_methods:
                if m.name == method_name and m.return_type:
                    return m.return_type

        # Pattern 6: TypeName VarName  (typed declaration)
        pattern_typed = re.compile(
            r'(\w+(?:<[^>]+>)?)\s+' + re.escape(var_name) + r'\b',
            re.MULTILINE
        )
        match = pattern_typed.search(text)
        if match:
            type_name = match.group(1)
            # Make sure it's actually a type, not a random word
            base_type = type_name.split('<')[0].lower()
            if base_type in registry.all_type_names or type_name in registry.all_gui_class_names:
                return type_name

        return None

    def _get_method_return_type(self, type_name: str, method_name: str) -> Optional[str]:
        """Look up the return type of a method on a given type."""
        registry = get_registry()

        # Check type methods (builtin types like vector, queue, etc.)
        type_lower = type_name.lower().split('<')[0].strip()
        methods = registry.get_type_methods_list(type_lower)
        if not methods:
            methods = registry.get_type_methods_list(type_name.split('<')[0].strip())

        # Check GUI class methods
        if not methods:
            gui_info = registry.get_gui_class_info(type_name)
            if gui_info:
                methods = gui_info.methods

        if methods:
            for m in methods:
                if m.name == method_name and m.return_type:
                    ret = m.return_type
                    # Clean up Python return type annotations
                    ret = ret.strip("'\"")
                    # Remove module prefix if present
                    if '.' in ret:
                        ret = ret.rsplit('.', 1)[-1]
                    return ret

        return None

    def _check_bracket_context(
        self,
        text: str,
        line: int,
        column: int
    ) -> tuple:
        """Check if cursor is inside filter brackets [type::operator].

        Returns:
            tuple: (is_in_brackets, filter_type or None)
        """
        lines = text.splitlines()
        if line >= len(lines):
            return (False, None)

        current_line = lines[line]
        if column > len(current_line):
            column = len(current_line)

        # Get text before cursor on current line
        text_before = current_line[:column]

        # Find last '[' and ']' before cursor
        last_open = text_before.rfind('[')
        last_close = text_before.rfind(']')

        # If we found '[' after the last ']', we're inside brackets
        if last_open > last_close:
            # Extract content inside brackets
            bracket_content = text_before[last_open + 1:]

            # Check if we have a type before ::
            if '::' in bracket_content:
                filter_type = bracket_content.split('::')[0].strip()
                return (True, filter_type)

            # We're after '[' but before '::'
            return (True, None)

        return (False, None)
