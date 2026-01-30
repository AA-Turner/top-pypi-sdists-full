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
from ..analysis.semantic_analyzer import CSSL_KEYWORDS, CSSL_TYPES, CSSL_BUILTINS, CSSL_MODIFIERS
from ..utils.symbol_table import SymbolKind
from ..utils.position_utils import get_context_before, get_word_at_position, get_line_text


# Namespace members for :: completions
NAMESPACE_MEMBERS: Dict[str, List[Dict[str, str]]] = {
    'json': [
        {'name': 'read', 'detail': 'Read JSON from file', 'snippet': 'read(${1:filename})'},
        {'name': 'write', 'detail': 'Write JSON to file', 'snippet': 'write(${1:filename}, ${2:data})'},
        {'name': 'parse', 'detail': 'Parse JSON string', 'snippet': 'parse(${1:jsonString})'},
        {'name': 'stringify', 'detail': 'Convert to JSON string', 'snippet': 'stringify(${1:data})'},
        {'name': 'pretty', 'detail': 'Pretty print JSON', 'snippet': 'pretty(${1:data})'},
        {'name': 'keys', 'detail': 'Get keys from JSON object', 'snippet': 'keys(${1:obj})'},
        {'name': 'values', 'detail': 'Get values from JSON object', 'snippet': 'values(${1:obj})'},
        {'name': 'get', 'detail': 'Get value by key path', 'snippet': 'get(${1:obj}, ${2:path})'},
        {'name': 'set', 'detail': 'Set value at key path', 'snippet': 'set(${1:obj}, ${2:path}, ${3:value})'},
        {'name': 'has', 'detail': 'Check if key exists', 'snippet': 'has(${1:obj}, ${2:key})'},
        {'name': 'merge', 'detail': 'Merge JSON objects', 'snippet': 'merge(${1:obj1}, ${2:obj2})'},
    ],
    'instance': [
        {'name': 'getMethods', 'detail': 'Get all instance methods', 'snippet': 'getMethods()'},
        {'name': 'getClasses', 'detail': 'Get all defined classes', 'snippet': 'getClasses()'},
        {'name': 'getVars', 'detail': 'Get all variables', 'snippet': 'getVars()'},
        {'name': 'getAll', 'detail': 'Get all symbols', 'snippet': 'getAll()'},
        {'name': 'call', 'detail': 'Call method by name', 'snippet': 'call(${1:methodName}, ${2:args})'},
        {'name': 'has', 'detail': 'Check if symbol exists', 'snippet': 'has(${1:name})'},
        {'name': 'type', 'detail': 'Get type of symbol', 'snippet': 'type(${1:name})'},
        {'name': 'exists', 'detail': 'Check if instance exists', 'snippet': 'exists(${1:name})'},
        {'name': 'delete', 'detail': 'Delete instance', 'snippet': 'delete(${1:name})'},
    ],
    'python': [
        {'name': 'pythonize', 'detail': 'Convert CSSL to Python object', 'snippet': 'pythonize(${1:value})'},
        {'name': 'wrap', 'detail': 'Wrap Python object for CSSL', 'snippet': 'wrap(${1:pyobj})'},
        {'name': 'export', 'detail': 'Export to Python module', 'snippet': 'export(${1:name}, ${2:value})'},
        {'name': 'csslize', 'detail': 'Convert Python to CSSL', 'snippet': 'csslize(${1:pyobj})'},
        {'name': 'import', 'detail': 'Import Python module', 'snippet': 'import(${1:module})'},
        {'name': 'parameter_get', 'detail': 'Get Python parameter', 'snippet': 'parameter_get(${1:name})'},
        {'name': 'parameter_return', 'detail': 'Return parameter to Python', 'snippet': 'parameter_return(${1:name}, ${2:value})'},
    ],
    'string': [
        {'name': 'where', 'detail': 'Find position of substring', 'snippet': 'where(${1:str}, ${2:substr})'},
        {'name': 'contains', 'detail': 'Check if contains substring', 'snippet': 'contains(${1:str}, ${2:substr})'},
        {'name': 'not', 'detail': 'Negate string check', 'snippet': 'not(${1:str}, ${2:condition})'},
        {'name': 'startsWith', 'detail': 'Check if starts with', 'snippet': 'startsWith(${1:str}, ${2:prefix})'},
        {'name': 'endsWith', 'detail': 'Check if ends with', 'snippet': 'endsWith(${1:str}, ${2:suffix})'},
        {'name': 'length', 'detail': 'Get string length', 'snippet': 'length(${1:str})'},
        {'name': 'cut', 'detail': 'Cut string before position', 'snippet': 'cut(${1:str}, ${2:pos})'},
        {'name': 'cutAfter', 'detail': 'Cut string after position', 'snippet': 'cutAfter(${1:str}, ${2:pos})'},
        {'name': 'value', 'detail': 'Get string value', 'snippet': 'value(${1:str})'},
    ],
    'sql': [
        {'name': 'connect', 'detail': 'Connect to database', 'snippet': 'connect(${1:connString})'},
        {'name': 'load', 'detail': 'Load data from table', 'snippet': 'load(${1:table})'},
        {'name': 'save', 'detail': 'Save data to table', 'snippet': 'save(${1:table}, ${2:data})'},
        {'name': 'update', 'detail': 'Update table data', 'snippet': 'update(${1:table}, ${2:data}, ${3:where})'},
        {'name': 'sync', 'detail': 'Synchronize with database', 'snippet': 'sync(${1:table})'},
        {'name': 'Structured', 'detail': 'Create structured query', 'snippet': 'Structured(${1:query})'},
        {'name': 'table', 'detail': 'Get table reference', 'snippet': 'table(${1:name})'},
        {'name': 'data', 'detail': 'Access table data', 'snippet': 'data(${1:table})'},
    ],
    'filter': [
        {'name': 'register', 'detail': 'Register a filter', 'snippet': 'register(${1:name}, ${2:func})'},
        {'name': 'unregister', 'detail': 'Unregister a filter', 'snippet': 'unregister(${1:name})'},
        {'name': 'list', 'detail': 'List all filters', 'snippet': 'list()'},
        {'name': 'exists', 'detail': 'Check if filter exists', 'snippet': 'exists(${1:name})'},
    ],
    'combo': [
        {'name': 'filterdb', 'detail': 'Filter database combo', 'snippet': 'filterdb(${1:filter})'},
        {'name': 'blocked', 'detail': 'Get blocked items', 'snippet': 'blocked()'},
        {'name': 'like', 'detail': 'Pattern match combo', 'snippet': 'like(${1:pattern})'},
    ],
    'async': [
        {'name': 'run', 'detail': 'Run async task', 'snippet': 'run(${1:func})'},
        {'name': 'wait', 'detail': 'Wait for async result', 'snippet': 'wait(${1:task})'},
        {'name': 'cancel', 'detail': 'Cancel async task', 'snippet': 'cancel(${1:task})'},
        {'name': 'parallel', 'detail': 'Run tasks in parallel', 'snippet': 'parallel([${1:tasks}])'},
    ],
    'math': [
        {'name': 'abs', 'detail': 'Absolute value', 'snippet': 'abs(${1:x})'},
        {'name': 'floor', 'detail': 'Floor value', 'snippet': 'floor(${1:x})'},
        {'name': 'ceil', 'detail': 'Ceiling value', 'snippet': 'ceil(${1:x})'},
        {'name': 'round', 'detail': 'Round value', 'snippet': 'round(${1:x})'},
        {'name': 'sqrt', 'detail': 'Square root', 'snippet': 'sqrt(${1:x})'},
        {'name': 'pow', 'detail': 'Power function', 'snippet': 'pow(${1:base}, ${2:exp})'},
        {'name': 'sin', 'detail': 'Sine function', 'snippet': 'sin(${1:x})'},
        {'name': 'cos', 'detail': 'Cosine function', 'snippet': 'cos(${1:x})'},
        {'name': 'tan', 'detail': 'Tangent function', 'snippet': 'tan(${1:x})'},
        {'name': 'log', 'detail': 'Natural logarithm', 'snippet': 'log(${1:x})'},
        {'name': 'exp', 'detail': 'Exponential function', 'snippet': 'exp(${1:x})'},
        {'name': 'random', 'detail': 'Random float 0-1', 'snippet': 'random()'},
        {'name': 'randint', 'detail': 'Random integer', 'snippet': 'randint(${1:min}, ${2:max})'},
    ],
    'file': [
        {'name': 'read', 'detail': 'Read file contents', 'snippet': 'read(${1:path})'},
        {'name': 'write', 'detail': 'Write to file', 'snippet': 'write(${1:path}, ${2:content})'},
        {'name': 'append', 'detail': 'Append to file', 'snippet': 'append(${1:path}, ${2:content})'},
        {'name': 'exists', 'detail': 'Check if file exists', 'snippet': 'exists(${1:path})'},
        {'name': 'delete', 'detail': 'Delete file', 'snippet': 'delete(${1:path})'},
        {'name': 'copy', 'detail': 'Copy file', 'snippet': 'copy(${1:src}, ${2:dest})'},
        {'name': 'move', 'detail': 'Move file', 'snippet': 'move(${1:src}, ${2:dest})'},
        {'name': 'list', 'detail': 'List directory contents', 'snippet': 'list(${1:dir})'},
    ],
    'fmt': [
        {'name': 'red', 'detail': 'Red colored text', 'snippet': 'red(${1:text})'},
        {'name': 'green', 'detail': 'Green colored text', 'snippet': 'green(${1:text})'},
        {'name': 'blue', 'detail': 'Blue colored text', 'snippet': 'blue(${1:text})'},
        {'name': 'yellow', 'detail': 'Yellow colored text', 'snippet': 'yellow(${1:text})'},
        {'name': 'cyan', 'detail': 'Cyan colored text', 'snippet': 'cyan(${1:text})'},
        {'name': 'magenta', 'detail': 'Magenta colored text', 'snippet': 'magenta(${1:text})'},
        {'name': 'white', 'detail': 'White colored text', 'snippet': 'white(${1:text})'},
        {'name': 'black', 'detail': 'Black colored text', 'snippet': 'black(${1:text})'},
        {'name': 'bold', 'detail': 'Bold text', 'snippet': 'bold(${1:text})'},
        {'name': 'italic', 'detail': 'Italic text', 'snippet': 'italic(${1:text})'},
        {'name': 'underline', 'detail': 'Underlined text', 'snippet': 'underline(${1:text})'},
        {'name': 'reset', 'detail': 'Reset formatting', 'snippet': 'reset()'},
        {'name': 'color', 'detail': 'Custom color', 'snippet': 'color(${1:text}, ${2:colorCode})'},
        {'name': 'bg', 'detail': 'Background color', 'snippet': 'bg(${1:text}, ${2:colorCode})'},
        {'name': 'bright', 'detail': 'Bright/bold color', 'snippet': 'bright(${1:text})'},
    ],
    'std': [
        {'name': 'InitializeSTD', 'detail': 'Initialize standard library', 'snippet': 'InitializeSTD()'},
        {'name': 'MakeTest', 'detail': 'Create test function', 'snippet': 'MakeTest()'},
        {'name': 'Version', 'detail': 'Get std library version', 'snippet': 'Version()'},
        {'name': 'Help', 'detail': 'Show help', 'snippet': 'Help(${1:topic})'},
        {'name': 'Debug', 'detail': 'Debug mode', 'snippet': 'Debug(${1:enabled})'},
    ],
    'watcher': [
        {'name': 'get', 'detail': 'Get watcher value', 'snippet': 'get(${1:name})'},
        {'name': 'set', 'detail': 'Set watcher value', 'snippet': 'set(${1:name}, ${2:value})'},
        {'name': 'list', 'detail': 'List all watchers', 'snippet': 'list()'},
        {'name': 'exists', 'detail': 'Check if watcher exists', 'snippet': 'exists(${1:name})'},
        {'name': 'refresh', 'detail': 'Refresh watcher', 'snippet': 'refresh(${1:name})'},
    ],
    'reflect': [
        {'name': 'getMethods', 'detail': 'Get all methods of object', 'snippet': 'getMethods(${1:obj})'},
        {'name': 'getProperties', 'detail': 'Get all properties of object', 'snippet': 'getProperties(${1:obj})'},
        {'name': 'getType', 'detail': 'Get type information', 'snippet': 'getType(${1:obj})'},
        {'name': 'getParent', 'detail': 'Get parent class', 'snippet': 'getParent(${1:obj})'},
        {'name': 'getModifiers', 'detail': 'Get access modifiers', 'snippet': 'getModifiers(${1:obj})'},
        {'name': 'getAnnotations', 'detail': 'Get annotations/decorators', 'snippet': 'getAnnotations(${1:obj})'},
        {'name': 'invoke', 'detail': 'Invoke method by name', 'snippet': 'invoke(${1:obj}, ${2:methodName}, ${3:args})'},
        {'name': 'create', 'detail': 'Create instance by type name', 'snippet': 'create(${1:typeName}, ${2:args})'},
        {'name': 'getField', 'detail': 'Get field value by name', 'snippet': 'getField(${1:obj}, ${2:fieldName})'},
        {'name': 'setField', 'detail': 'Set field value by name', 'snippet': 'setField(${1:obj}, ${2:fieldName}, ${3:value})'},
        {'name': 'getConstructors', 'detail': 'Get constructors of class', 'snippet': 'getConstructors(${1:cls})'},
        {'name': 'isInstance', 'detail': 'Check if object is instance of type', 'snippet': 'isInstance(${1:obj}, ${2:type})'},
        {'name': 'getInterfaces', 'detail': 'Get implemented interfaces', 'snippet': 'getInterfaces(${1:obj})'},
        {'name': 'getSource', 'detail': 'Get source code of function', 'snippet': 'getSource(${1:func})'},
        {'name': 'getSignature', 'detail': 'Get function signature', 'snippet': 'getSignature(${1:func})'},
    ],
    'resolve': [
        {'name': 'byName', 'detail': 'Resolve symbol by name', 'snippet': 'byName(${1:name})'},
        {'name': 'byPath', 'detail': 'Resolve by dot-separated path', 'snippet': 'byPath(${1:path})'},
        {'name': 'inScope', 'detail': 'Resolve in specific scope', 'snippet': 'inScope(${1:name}, ${2:scope})'},
        {'name': 'lazy', 'detail': 'Create lazy resolver', 'snippet': 'lazy(${1:name})'},
        {'name': 'tryResolve', 'detail': 'Try to resolve, return null if not found', 'snippet': 'tryResolve(${1:name})'},
        {'name': 'exists', 'detail': 'Check if symbol can be resolved', 'snippet': 'exists(${1:name})'},
        {'name': 'type', 'detail': 'Resolve type by name', 'snippet': 'type(${1:typeName})'},
        {'name': 'function', 'detail': 'Resolve function by name', 'snippet': 'function(${1:funcName})'},
        {'name': 'class', 'detail': 'Resolve class by name', 'snippet': 'class(${1:className})'},
    ],
}

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

# Type methods for . completions
TYPE_METHODS: Dict[str, List[Dict[str, str]]] = {
    'string': [
        {'name': 'length', 'detail': 'Get string length', 'snippet': 'length()'},
        {'name': 'upper', 'detail': 'Convert to uppercase', 'snippet': 'upper()'},
        {'name': 'lower', 'detail': 'Convert to lowercase', 'snippet': 'lower()'},
        {'name': 'trim', 'detail': 'Trim whitespace', 'snippet': 'trim()'},
        {'name': 'split', 'detail': 'Split string', 'snippet': 'split(${1:delimiter})'},
        {'name': 'replace', 'detail': 'Replace substring', 'snippet': 'replace(${1:old}, ${2:new})'},
        {'name': 'contains', 'detail': 'Check contains', 'snippet': 'contains(${1:substr})'},
        {'name': 'startswith', 'detail': 'Check starts with', 'snippet': 'startswith(${1:prefix})'},
        {'name': 'endswith', 'detail': 'Check ends with', 'snippet': 'endswith(${1:suffix})'},
        {'name': 'substr', 'detail': 'Get substring', 'snippet': 'substr(${1:start}, ${2:end})'},
        {'name': 'indexOf', 'detail': 'Find index of substring', 'snippet': 'indexOf(${1:substr})'},
        {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt()'},
        {'name': 'toFloat', 'detail': 'Convert to float', 'snippet': 'toFloat()'},
        {'name': 'format', 'detail': 'Format string', 'snippet': 'format(${1:args})'},
    ],
    'array': [
        {'name': 'length', 'detail': 'Get array length', 'snippet': 'length()'},
        {'name': 'push', 'detail': 'Add element to end', 'snippet': 'push(${1:item})'},
        {'name': 'pop', 'detail': 'Remove last element', 'snippet': 'pop()'},
        {'name': 'shift', 'detail': 'Remove first element', 'snippet': 'shift()'},
        {'name': 'unshift', 'detail': 'Add to beginning', 'snippet': 'unshift(${1:item})'},
        {'name': 'slice', 'detail': 'Get array slice', 'snippet': 'slice(${1:start}, ${2:end})'},
        {'name': 'join', 'detail': 'Join elements', 'snippet': 'join(${1:delimiter})'},
        {'name': 'sort', 'detail': 'Sort array', 'snippet': 'sort()'},
        {'name': 'rsort', 'detail': 'Reverse sort', 'snippet': 'rsort()'},
        {'name': 'reverse', 'detail': 'Reverse array', 'snippet': 'reverse()'},
        {'name': 'contains', 'detail': 'Check if contains', 'snippet': 'contains(${1:item})'},
        {'name': 'indexOf', 'detail': 'Find index of item', 'snippet': 'indexOf(${1:item})'},
        {'name': 'filter', 'detail': 'Filter elements', 'snippet': 'filter(${1:predicate})'},
        {'name': 'map', 'detail': 'Map elements', 'snippet': 'map(${1:func})'},
        {'name': 'reduce', 'detail': 'Reduce array', 'snippet': 'reduce(${1:func}, ${2:initial})'},
        {'name': 'find', 'detail': 'Find element', 'snippet': 'find(${1:predicate})'},
        {'name': 'every', 'detail': 'Check all match', 'snippet': 'every(${1:predicate})'},
        {'name': 'some', 'detail': 'Check any match', 'snippet': 'some(${1:predicate})'},
        {'name': 'flatten', 'detail': 'Flatten nested arrays', 'snippet': 'flatten()'},
        {'name': 'unique', 'detail': 'Get unique elements', 'snippet': 'unique()'},
    ],
    'list': [
        {'name': 'length', 'detail': 'Get list length', 'snippet': 'length()'},
        {'name': 'add', 'detail': 'Add element', 'snippet': 'add(${1:item})'},
        {'name': 'remove', 'detail': 'Remove element', 'snippet': 'remove(${1:item})'},
        {'name': 'get', 'detail': 'Get element at index', 'snippet': 'get(${1:index})'},
        {'name': 'set', 'detail': 'Set element at index', 'snippet': 'set(${1:index}, ${2:value})'},
        {'name': 'clear', 'detail': 'Clear all elements', 'snippet': 'clear()'},
        {'name': 'contains', 'detail': 'Check if contains', 'snippet': 'contains(${1:item})'},
        {'name': 'toArray', 'detail': 'Convert to array', 'snippet': 'toArray()'},
    ],
    'dict': [
        {'name': 'keys', 'detail': 'Get all keys', 'snippet': 'keys()'},
        {'name': 'values', 'detail': 'Get all values', 'snippet': 'values()'},
        {'name': 'items', 'detail': 'Get key-value pairs', 'snippet': 'items()'},
        {'name': 'get', 'detail': 'Get value by key', 'snippet': 'get(${1:key})'},
        {'name': 'set', 'detail': 'Set key-value pair', 'snippet': 'set(${1:key}, ${2:value})'},
        {'name': 'has', 'detail': 'Check if key exists', 'snippet': 'has(${1:key})'},
        {'name': 'delete', 'detail': 'Delete key', 'snippet': 'delete(${1:key})'},
        {'name': 'clear', 'detail': 'Clear all pairs', 'snippet': 'clear()'},
        {'name': 'merge', 'detail': 'Merge with another dict', 'snippet': 'merge(${1:other})'},
        {'name': 'length', 'detail': 'Get number of keys', 'snippet': 'length()'},
    ],
    'dictionary': [
        {'name': 'keys', 'detail': 'Get all keys', 'snippet': 'keys()'},
        {'name': 'values', 'detail': 'Get all values', 'snippet': 'values()'},
        {'name': 'items', 'detail': 'Get key-value pairs', 'snippet': 'items()'},
        {'name': 'get', 'detail': 'Get value by key', 'snippet': 'get(${1:key})'},
        {'name': 'set', 'detail': 'Set key-value pair', 'snippet': 'set(${1:key}, ${2:value})'},
        {'name': 'has', 'detail': 'Check if key exists', 'snippet': 'has(${1:key})'},
        {'name': 'delete', 'detail': 'Delete key', 'snippet': 'delete(${1:key})'},
    ],
    'json': [
        {'name': 'stringify', 'detail': 'Convert to JSON string', 'snippet': 'stringify()'},
        {'name': 'keys', 'detail': 'Get all keys', 'snippet': 'keys()'},
        {'name': 'values', 'detail': 'Get all values', 'snippet': 'values()'},
        {'name': 'get', 'detail': 'Get value by path', 'snippet': 'get(${1:path})'},
        {'name': 'set', 'detail': 'Set value at path', 'snippet': 'set(${1:path}, ${2:value})'},
        {'name': 'has', 'detail': 'Check path exists', 'snippet': 'has(${1:path})'},
    ],
    'iterator': [
        {'name': 'next', 'detail': 'Get next element', 'snippet': 'next()'},
        {'name': 'hasNext', 'detail': 'Check if has next', 'snippet': 'hasNext()'},
        {'name': 'reset', 'detail': 'Reset iterator', 'snippet': 'reset()'},
        {'name': 'current', 'detail': 'Get current element', 'snippet': 'current()'},
        {'name': 'toArray', 'detail': 'Convert to array', 'snippet': 'toArray()'},
    ],
    'generator': [
        {'name': 'next', 'detail': 'Get next yielded value', 'snippet': 'next()'},
        {'name': 'send', 'detail': 'Send value to generator', 'snippet': 'send(${1:value})'},
        {'name': 'hasNext', 'detail': 'Check if has more', 'snippet': 'hasNext()'},
        {'name': 'toArray', 'detail': 'Collect all values', 'snippet': 'toArray()'},
        {'name': 'close', 'detail': 'Close generator', 'snippet': 'close()'},
    ],
    'future': [
        {'name': 'get', 'detail': 'Get result (blocking)', 'snippet': 'get()'},
        {'name': 'isDone', 'detail': 'Check if complete', 'snippet': 'isDone()'},
        {'name': 'cancel', 'detail': 'Cancel execution', 'snippet': 'cancel()'},
        {'name': 'then', 'detail': 'Chain callback', 'snippet': 'then(${1:callback})'},
        {'name': 'catch', 'detail': 'Handle error', 'snippet': 'catch(${1:handler})'},
    ],
    'stack': [
        {'name': 'push', 'detail': 'Push element', 'snippet': 'push(${1:item})'},
        {'name': 'pop', 'detail': 'Pop element', 'snippet': 'pop()'},
        {'name': 'peek', 'detail': 'Peek top element', 'snippet': 'peek()'},
        {'name': 'isEmpty', 'detail': 'Check if empty', 'snippet': 'isEmpty()'},
        {'name': 'size', 'detail': 'Get stack size', 'snippet': 'size()'},
        {'name': 'clear', 'detail': 'Clear stack', 'snippet': 'clear()'},
    ],
    'queue': [
        {'name': 'enqueue', 'detail': 'Add to queue', 'snippet': 'enqueue(${1:item})'},
        {'name': 'dequeue', 'detail': 'Remove from queue', 'snippet': 'dequeue()'},
        {'name': 'peek', 'detail': 'Peek front element', 'snippet': 'peek()'},
        {'name': 'isEmpty', 'detail': 'Check if empty', 'snippet': 'isEmpty()'},
        {'name': 'size', 'detail': 'Get queue size', 'snippet': 'size()'},
        {'name': 'clear', 'detail': 'Clear queue', 'snippet': 'clear()'},
    ],
    'set': [
        {'name': 'add', 'detail': 'Add element', 'snippet': 'add(${1:item})'},
        {'name': 'remove', 'detail': 'Remove element', 'snippet': 'remove(${1:item})'},
        {'name': 'has', 'detail': 'Check if contains', 'snippet': 'has(${1:item})'},
        {'name': 'size', 'detail': 'Get set size', 'snippet': 'size()'},
        {'name': 'clear', 'detail': 'Clear set', 'snippet': 'clear()'},
        {'name': 'union', 'detail': 'Union with another set', 'snippet': 'union(${1:other})'},
        {'name': 'intersection', 'detail': 'Intersection with set', 'snippet': 'intersection(${1:other})'},
        {'name': 'difference', 'detail': 'Difference from set', 'snippet': 'difference(${1:other})'},
        {'name': 'toArray', 'detail': 'Convert to array', 'snippet': 'toArray()'},
    ],
    'tuple': [
        {'name': 'get', 'detail': 'Get element at index', 'snippet': 'get(${1:index})'},
        {'name': 'length', 'detail': 'Get tuple length', 'snippet': 'length()'},
        {'name': 'toArray', 'detail': 'Convert to array', 'snippet': 'toArray()'},
    ],
    'int': [
        {'name': 'toString', 'detail': 'Convert to string', 'snippet': 'toString()'},
        {'name': 'toFloat', 'detail': 'Convert to float', 'snippet': 'toFloat()'},
        {'name': 'abs', 'detail': 'Absolute value', 'snippet': 'abs()'},
    ],
    'float': [
        {'name': 'toString', 'detail': 'Convert to string', 'snippet': 'toString()'},
        {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt()'},
        {'name': 'round', 'detail': 'Round value', 'snippet': 'round()'},
        {'name': 'floor', 'detail': 'Floor value', 'snippet': 'floor()'},
        {'name': 'ceil', 'detail': 'Ceiling value', 'snippet': 'ceil()'},
        {'name': 'abs', 'detail': 'Absolute value', 'snippet': 'abs()'},
    ],
    'datastruct': [
        {'name': 'add', 'detail': 'Add element', 'snippet': 'add(${1:item})'},
        {'name': 'push', 'detail': 'Push element', 'snippet': 'push(${1:item})'},
        {'name': 'pop', 'detail': 'Pop element', 'snippet': 'pop()'},
        {'name': 'get', 'detail': 'Get element', 'snippet': 'get(${1:index})'},
        {'name': 'set', 'detail': 'Set element', 'snippet': 'set(${1:index}, ${2:value})'},
        {'name': 'remove', 'detail': 'Remove element', 'snippet': 'remove(${1:index})'},
        {'name': 'clear', 'detail': 'Clear all elements', 'snippet': 'clear()'},
        {'name': 'content', 'detail': 'Get all content', 'snippet': 'content()'},
        {'name': 'len', 'detail': 'Get length', 'snippet': 'len()'},
        {'name': 'size', 'detail': 'Get size', 'snippet': 'size()'},
        {'name': 'at', 'detail': 'Get element at index', 'snippet': 'at(${1:index})'},
        {'name': 'filter', 'detail': 'Filter elements', 'snippet': 'filter(${1:predicate})'},
        {'name': 'map', 'detail': 'Map elements', 'snippet': 'map(${1:func})'},
        {'name': 'isEmpty', 'detail': 'Check if empty', 'snippet': 'isEmpty()'},
        {'name': 'contains', 'detail': 'Check if contains', 'snippet': 'contains(${1:item})'},
        {'name': 'begin', 'detail': 'Get begin iterator', 'snippet': 'begin()'},
        {'name': 'end', 'detail': 'Get end iterator', 'snippet': 'end()'},
    ],
    'vector': [
        {'name': 'push', 'detail': 'Push element', 'snippet': 'push(${1:item})'},
        {'name': 'push_back', 'detail': 'Push to back', 'snippet': 'push_back(${1:item})'},
        {'name': 'pop', 'detail': 'Pop element', 'snippet': 'pop()'},
        {'name': 'pop_back', 'detail': 'Pop from back', 'snippet': 'pop_back()'},
        {'name': 'at', 'detail': 'Get element at index', 'snippet': 'at(${1:index})'},
        {'name': 'set', 'detail': 'Set element', 'snippet': 'set(${1:index}, ${2:value})'},
        {'name': 'size', 'detail': 'Get size', 'snippet': 'size()'},
        {'name': 'empty', 'detail': 'Check if empty', 'snippet': 'empty()'},
        {'name': 'clear', 'detail': 'Clear all elements', 'snippet': 'clear()'},
        {'name': 'insert', 'detail': 'Insert at position', 'snippet': 'insert(${1:pos}, ${2:item})'},
        {'name': 'erase', 'detail': 'Erase at position', 'snippet': 'erase(${1:pos})'},
        {'name': 'front', 'detail': 'Get first element', 'snippet': 'front()'},
        {'name': 'back', 'detail': 'Get last element', 'snippet': 'back()'},
        {'name': 'contains', 'detail': 'Check if contains', 'snippet': 'contains(${1:item})'},
        {'name': 'indexOf', 'detail': 'Find index of item', 'snippet': 'indexOf(${1:item})'},
    ],
    'byte': [
        {'name': 'switch', 'detail': 'Toggle byte value', 'snippet': 'switch(${1:bitPosition})'},
        {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt()'},
        {'name': 'toString', 'detail': 'Convert to string', 'snippet': 'toString()'},
        {'name': 'toBinary', 'detail': 'Convert to binary string', 'snippet': 'toBinary()'},
        {'name': 'toHex', 'detail': 'Convert to hex string', 'snippet': 'toHex()'},
    ],
    'bit': [
        {'name': 'switch', 'detail': 'Toggle bit value', 'snippet': 'switch(${1:position})'},
        {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt()'},
        {'name': 'toString', 'detail': 'Convert to string', 'snippet': 'toString()'},
        {'name': 'set', 'detail': 'Set bit to 1', 'snippet': 'set()'},
        {'name': 'clear', 'detail': 'Set bit to 0', 'snippet': 'clear()'},
        {'name': 'flip', 'detail': 'Flip bit value', 'snippet': 'flip()'},
    ],
    'ptr': [
        {'name': 'get_address', 'detail': 'Get memory address of pointer target', 'snippet': 'get_address()'},
        {'name': 'set_address', 'detail': 'Set pointer to address', 'snippet': 'set_address(${1:addr})'},
        {'name': 'get_value', 'detail': 'Get value at pointer', 'snippet': 'get_value()'},
        {'name': 'set_value', 'detail': 'Set value at pointer', 'snippet': 'set_value(${1:value})'},
        {'name': 'deref', 'detail': 'Dereference pointer', 'snippet': 'deref()'},
        {'name': 'ref', 'detail': 'Get reference', 'snippet': 'ref()'},
        {'name': 'isNull', 'detail': 'Check if null pointer', 'snippet': 'isNull()'},
        {'name': 'is_null', 'detail': 'Check if null pointer', 'snippet': 'is_null()'},
        {'name': 'is_valid', 'detail': 'Check if pointer is valid', 'snippet': 'is_valid()'},
        {'name': 'is_address', 'detail': 'Check if pointer holds a valid address', 'snippet': 'is_address()'},
        {'name': 'offset', 'detail': 'Add offset to pointer', 'snippet': 'offset(${1:bytes})'},
        {'name': 'copy', 'detail': 'Copy pointer', 'snippet': 'copy()'},
        {'name': 'free', 'detail': 'Free memory at pointer', 'snippet': 'free()'},
        {'name': 'address', 'detail': 'Get address', 'snippet': 'address()'},
        {'name': 'set', 'detail': 'Set pointer target', 'snippet': 'set(${1:target})'},
    ],
    'pointer': [
        {'name': 'get_address', 'detail': 'Get memory address of pointer target', 'snippet': 'get_address()'},
        {'name': 'set_address', 'detail': 'Set pointer to address', 'snippet': 'set_address(${1:addr})'},
        {'name': 'get_value', 'detail': 'Get value at pointer', 'snippet': 'get_value()'},
        {'name': 'set_value', 'detail': 'Set value at pointer', 'snippet': 'set_value(${1:value})'},
        {'name': 'deref', 'detail': 'Dereference pointer', 'snippet': 'deref()'},
        {'name': 'ref', 'detail': 'Get reference', 'snippet': 'ref()'},
        {'name': 'isNull', 'detail': 'Check if null pointer', 'snippet': 'isNull()'},
        {'name': 'is_null', 'detail': 'Check if null pointer', 'snippet': 'is_null()'},
        {'name': 'is_valid', 'detail': 'Check if pointer is valid', 'snippet': 'is_valid()'},
        {'name': 'is_address', 'detail': 'Check if pointer holds a valid address', 'snippet': 'is_address()'},
        {'name': 'offset', 'detail': 'Add offset to pointer', 'snippet': 'offset(${1:bytes})'},
        {'name': 'copy', 'detail': 'Copy pointer', 'snippet': 'copy()'},
        {'name': 'free', 'detail': 'Free memory at pointer', 'snippet': 'free()'},
    ],
    'address': [
        {'name': 'get', 'detail': 'Get value at address', 'snippet': 'get()'},
        {'name': 'set', 'detail': 'Set value at address', 'snippet': 'set(${1:value})'},
        {'name': 'deref', 'detail': 'Dereference address', 'snippet': 'deref()'},
        {'name': 'offset', 'detail': 'Add offset to address', 'snippet': 'offset(${1:bytes})'},
        {'name': 'to_ptr', 'detail': 'Convert to pointer', 'snippet': 'to_ptr()'},
        {'name': 'isNull', 'detail': 'Check if null', 'snippet': 'isNull()'},
        {'name': 'is_valid', 'detail': 'Check if address is valid', 'snippet': 'is_valid()'},
        {'name': 'toInt', 'detail': 'Convert to integer', 'snippet': 'toInt()'},
        {'name': 'toString', 'detail': 'Convert to hex string', 'snippet': 'toString()'},
        {'name': 'copy', 'detail': 'Copy address', 'snippet': 'copy()'},
    ],
}

# Builtin function documentation
BUILTIN_DOCS: Dict[str, Dict[str, str]] = {
    'print': {'signature': 'print(value, ...)', 'doc': 'Print values to stdout without newline'},
    'printl': {'signature': 'printl(value, ...)', 'doc': 'Print values to stdout with newline'},
    'println': {'signature': 'println(value, ...)', 'doc': 'Print values to stdout with newline'},
    'input': {'signature': 'input(prompt?)', 'doc': 'Read line from stdin'},
    'read': {'signature': 'read()', 'doc': 'Read input'},
    'readline': {'signature': 'readline()', 'doc': 'Read a line from stdin'},
    'write': {'signature': 'write(value)', 'doc': 'Write value to output'},
    'writeline': {'signature': 'writeline(value)', 'doc': 'Write value with newline'},
    'len': {'signature': 'len(collection)', 'doc': 'Get length of collection'},
    'type': {'signature': 'type(value)', 'doc': 'Get type name of value'},
    'toInt': {'signature': 'toInt(value)', 'doc': 'Convert value to integer'},
    'toFloat': {'signature': 'toFloat(value)', 'doc': 'Convert value to float'},
    'toString': {'signature': 'toString(value)', 'doc': 'Convert value to string'},
    'toBool': {'signature': 'toBool(value)', 'doc': 'Convert value to boolean'},
    'typeof': {'signature': 'typeof(value)', 'doc': 'Get type of value'},
    'memory': {'signature': 'memory()', 'doc': 'Get memory usage info'},
    'address': {'signature': 'address(var)', 'doc': 'Get memory address of variable'},
    'reflect': {'signature': 'reflect(obj)', 'doc': 'Get comprehensive reflection info (methods, properties, type, metadata)'},
    'resolve': {'signature': 'resolve(name, context?)', 'doc': 'Resolve symbol by name at runtime'},
    'getattr': {'signature': 'getattr(obj, name, default?)', 'doc': 'Get attribute from object by name'},
    'setattr': {'signature': 'setattr(obj, name, value)', 'doc': 'Set attribute on object by name'},
    'hasattr': {'signature': 'hasattr(obj, name)', 'doc': 'Check if object has attribute'},
    'delattr': {'signature': 'delattr(obj, name)', 'doc': 'Delete attribute from object'},
    'dir': {'signature': 'dir(obj?)', 'doc': 'List all attributes/methods of object'},
    'vars': {'signature': 'vars(obj?)', 'doc': 'Get variables dict from object/scope'},
    'locals': {'signature': 'locals()', 'doc': 'Get dict of local variables'},
    'globals': {'signature': 'globals()', 'doc': 'Get dict of global variables'},
    'callable': {'signature': 'callable(obj)', 'doc': 'Check if object is callable'},
    'classof': {'signature': 'classof(obj)', 'doc': 'Get class/type of object'},
    'nameof': {'signature': 'nameof(symbol)', 'doc': 'Get name of symbol as string'},
    'sizeof': {'signature': 'sizeof(obj)', 'doc': 'Get size in bytes of object/type'},
    'alignof': {'signature': 'alignof(type)', 'doc': 'Get alignment requirement of type'},
    'destroy': {'signature': 'destroy(var)', 'doc': 'Destroy variable and free memory'},
    'exit': {'signature': 'exit(code?)', 'doc': 'Exit program with optional code'},
    'sleep': {'signature': 'sleep(ms)', 'doc': 'Sleep for milliseconds'},
    'range': {'signature': 'range(start, end, step?)', 'doc': 'Generate range of numbers'},
    'isavailable': {'signature': 'isavailable(name)', 'doc': 'Check if name is available'},
    'OpenFind': {'signature': 'OpenFind(pattern)', 'doc': 'Open find dialog'},
    'cast': {'signature': 'cast(value, type)', 'doc': 'Cast value to type'},
    'share': {'signature': 'share(name, value)', 'doc': 'Share variable across modules'},
    'shared': {'signature': 'shared(name)', 'doc': 'Access shared variable'},
    'include': {'signature': 'include(path)', 'doc': 'Include CSSL file'},
    'includecpp': {'signature': 'includecpp(path)', 'doc': 'Include C++ file'},
    'snapshot': {'signature': 'snapshot(name)', 'doc': 'Create snapshot of variable'},
    'get_snapshot': {'signature': 'get_snapshot(name)', 'doc': 'Get snapshot value'},
    'has_snapshot': {'signature': 'has_snapshot(name)', 'doc': 'Check if snapshot exists'},
    'clear_snapshot': {'signature': 'clear_snapshot(name)', 'doc': 'Clear single snapshot'},
    'clear_snapshots': {'signature': 'clear_snapshots()', 'doc': 'Clear all snapshots'},
    'list_snapshots': {'signature': 'list_snapshots()', 'doc': 'List all snapshot names'},
    'restore_snapshot': {'signature': 'restore_snapshot(name)', 'doc': 'Restore variable from snapshot'},
    'random': {'signature': 'random()', 'doc': 'Generate random float 0-1'},
    'randint': {'signature': 'randint(min, max)', 'doc': 'Generate random integer'},
    'round': {'signature': 'round(value, decimals?)', 'doc': 'Round to decimals'},
    'abs': {'signature': 'abs(value)', 'doc': 'Absolute value'},
    'ceil': {'signature': 'ceil(value)', 'doc': 'Ceiling function'},
    'floor': {'signature': 'floor(value)', 'doc': 'Floor function'},
    'sqrt': {'signature': 'sqrt(value)', 'doc': 'Square root'},
    'pow': {'signature': 'pow(base, exp)', 'doc': 'Power function'},
    'min': {'signature': 'min(a, b, ...)', 'doc': 'Minimum value'},
    'max': {'signature': 'max(a, b, ...)', 'doc': 'Maximum value'},
    'sum': {'signature': 'sum(collection)', 'doc': 'Sum of collection'},
    'sin': {'signature': 'sin(x)', 'doc': 'Sine function'},
    'cos': {'signature': 'cos(x)', 'doc': 'Cosine function'},
    'tan': {'signature': 'tan(x)', 'doc': 'Tangent function'},
    'asin': {'signature': 'asin(x)', 'doc': 'Arc sine'},
    'acos': {'signature': 'acos(x)', 'doc': 'Arc cosine'},
    'atan': {'signature': 'atan(x)', 'doc': 'Arc tangent'},
    'log': {'signature': 'log(x)', 'doc': 'Natural logarithm'},
    'exp': {'signature': 'exp(x)', 'doc': 'Exponential function'},
    'upper': {'signature': 'upper(str)', 'doc': 'Convert to uppercase'},
    'lower': {'signature': 'lower(str)', 'doc': 'Convert to lowercase'},
    'trim': {'signature': 'trim(str)', 'doc': 'Trim whitespace'},
    'split': {'signature': 'split(str, delimiter)', 'doc': 'Split string'},
    'join': {'signature': 'join(arr, delimiter)', 'doc': 'Join array elements'},
    'replace': {'signature': 'replace(str, old, new)', 'doc': 'Replace substring'},
    'substr': {'signature': 'substr(str, start, len?)', 'doc': 'Get substring'},
    'contains': {'signature': 'contains(collection, item)', 'doc': 'Check if contains'},
    'startswith': {'signature': 'startswith(str, prefix)', 'doc': 'Check starts with'},
    'endswith': {'signature': 'endswith(str, suffix)', 'doc': 'Check ends with'},
    'format': {'signature': 'format(template, ...args)', 'doc': 'Format string'},
    'concat': {'signature': 'concat(a, b, ...)', 'doc': 'Concatenate values'},
    'push': {'signature': 'push(arr, item)', 'doc': 'Add item to array'},
    'pop': {'signature': 'pop(arr)', 'doc': 'Remove last item'},
    'shift': {'signature': 'shift(arr)', 'doc': 'Remove first item'},
    'unshift': {'signature': 'unshift(arr, item)', 'doc': 'Add to beginning'},
    'slice': {'signature': 'slice(arr, start, end?)', 'doc': 'Get array slice'},
    'sort': {'signature': 'sort(arr)', 'doc': 'Sort array ascending'},
    'rsort': {'signature': 'rsort(arr)', 'doc': 'Sort array descending'},
    'unique': {'signature': 'unique(arr)', 'doc': 'Get unique elements'},
    'flatten': {'signature': 'flatten(arr)', 'doc': 'Flatten nested arrays'},
    'filter': {'signature': 'filter(arr, predicate)', 'doc': 'Filter elements'},
    'map': {'signature': 'map(arr, func)', 'doc': 'Map elements'},
    'reduce': {'signature': 'reduce(arr, func, initial)', 'doc': 'Reduce array'},
    'find': {'signature': 'find(arr, predicate)', 'doc': 'Find element'},
    'findindex': {'signature': 'findindex(arr, predicate)', 'doc': 'Find element index'},
    'every': {'signature': 'every(arr, predicate)', 'doc': 'Check all match'},
    'some': {'signature': 'some(arr, predicate)', 'doc': 'Check any match'},
    'keys': {'signature': 'keys(obj)', 'doc': 'Get object keys'},
    'values': {'signature': 'values(obj)', 'doc': 'Get object values'},
    'items': {'signature': 'items(obj)', 'doc': 'Get key-value pairs'},
    'haskey': {'signature': 'haskey(obj, key)', 'doc': 'Check if key exists'},
    'getkey': {'signature': 'getkey(obj, key)', 'doc': 'Get value by key'},
    'setkey': {'signature': 'setkey(obj, key, value)', 'doc': 'Set key-value pair'},
    'delkey': {'signature': 'delkey(obj, key)', 'doc': 'Delete key'},
    'merge': {'signature': 'merge(obj1, obj2)', 'doc': 'Merge objects'},
    'now': {'signature': 'now()', 'doc': 'Get current timestamp'},
    'timestamp': {'signature': 'timestamp()', 'doc': 'Get Unix timestamp'},
    'date': {'signature': 'date(format?)', 'doc': 'Get formatted date'},
    'time': {'signature': 'time(format?)', 'doc': 'Get formatted time'},
    'datetime': {'signature': 'datetime(format?)', 'doc': 'Get formatted datetime'},
    'strftime': {'signature': 'strftime(format, timestamp?)', 'doc': 'Format timestamp'},
    'tojson': {'signature': 'tojson(value)', 'doc': 'Convert to JSON string'},
    'fromjson': {'signature': 'fromjson(str)', 'doc': 'Parse JSON string'},
    'debug': {'signature': 'debug(msg)', 'doc': 'Log debug message'},
    'error': {'signature': 'error(msg)', 'doc': 'Log error message'},
    'warn': {'signature': 'warn(msg)', 'doc': 'Log warning message'},
    'readfile': {'signature': 'readfile(path)', 'doc': 'Read entire file'},
    'writefile': {'signature': 'writefile(path, content)', 'doc': 'Write to file'},
    'appendfile': {'signature': 'appendfile(path, content)', 'doc': 'Append to file'},
    'readlines': {'signature': 'readlines(path)', 'doc': 'Read file lines'},
    'listdir': {'signature': 'listdir(path)', 'doc': 'List directory contents'},
    'makedirs': {'signature': 'makedirs(path)', 'doc': 'Create directories'},
    'removefile': {'signature': 'removefile(path)', 'doc': 'Remove file'},
    'removedir': {'signature': 'removedir(path)', 'doc': 'Remove directory'},
    'copyfile': {'signature': 'copyfile(src, dest)', 'doc': 'Copy file'},
    'movefile': {'signature': 'movefile(src, dest)', 'doc': 'Move file'},
    'filesize': {'signature': 'filesize(path)', 'doc': 'Get file size'},
    'pathexists': {'signature': 'pathexists(path)', 'doc': 'Check path exists'},
    'isfile': {'signature': 'isfile(path)', 'doc': 'Check if is file'},
    'isdir': {'signature': 'isdir(path)', 'doc': 'Check if is directory'},
    'basename': {'signature': 'basename(path)', 'doc': 'Get base name'},
    'dirname': {'signature': 'dirname(path)', 'doc': 'Get directory name'},
    'joinpath': {'signature': 'joinpath(a, b, ...)', 'doc': 'Join path parts'},
    'splitpath': {'signature': 'splitpath(path)', 'doc': 'Split path'},
    'abspath': {'signature': 'abspath(path)', 'doc': 'Get absolute path'},
    'isinstance': {'signature': 'isinstance(obj, type)', 'doc': 'Check instance type'},
    'isint': {'signature': 'isint(value)', 'doc': 'Check if integer'},
    'isfloat': {'signature': 'isfloat(value)', 'doc': 'Check if float'},
    'isstr': {'signature': 'isstr(value)', 'doc': 'Check if string'},
    'isbool': {'signature': 'isbool(value)', 'doc': 'Check if boolean'},
    'islist': {'signature': 'islist(value)', 'doc': 'Check if list'},
    'isdict': {'signature': 'isdict(value)', 'doc': 'Check if dictionary'},
    'isnull': {'signature': 'isnull(value)', 'doc': 'Check if null'},
    'copy': {'signature': 'copy(value)', 'doc': 'Shallow copy'},
    'deepcopy': {'signature': 'deepcopy(value)', 'doc': 'Deep copy'},
    'pyimport': {'signature': 'pyimport(module)', 'doc': 'Import Python module'},
}

# Keyword documentation
KEYWORD_DOCS: Dict[str, str] = {
    'if': 'Conditional execution',
    'else': 'Alternative branch for if',
    'elif': 'Else-if branch',
    'while': 'While loop - repeats while condition is true',
    'for': 'For loop - classic C-style loop',
    'foreach': 'Foreach loop - iterate over collection',
    'in': 'Membership test or iteration keyword',
    'range': 'Generate numeric range',
    'switch': 'Switch statement for multiple conditions',
    'case': 'Case label in switch',
    'default': 'Default case in switch',
    'break': 'Exit loop or switch',
    'continue': 'Skip to next iteration',
    'return': 'Return from function',
    'try': 'Begin try-catch block',
    'catch': 'Handle exception',
    'finally': 'Always execute block',
    'throw': 'Throw exception',
    'except': 'Exception handler',
    'always': 'Always execute (like finally)',
    'class': 'Define a class',
    'struct': 'Define a struct',
    'enum': 'Define an enumeration',
    'interface': 'Define an interface',
    'namespace': 'Define a namespace',
    'define': 'Define a function',
    'void': 'No return value',
    'constr': 'Constructor function',
    'new': 'Create new instance',
    'this': 'Reference to current instance',
    'super': 'Reference to parent class',
    'extends': 'Inherit from class',
    'overwrites': 'Override parent method',
    'service-init': 'Service initialization block',
    'service-run': 'Service run block',
    'service-include': 'Include in service',
    'main': 'Main function entry point',
    'package': 'Package declaration',
    'exec': 'Execute code',
    'as': 'Type alias or import alias',
    'global': 'Global variable declaration',
    'include': 'Include CSSL file',
    'get': 'Property getter',
    'payload': 'Data payload',
    'convert': 'Type conversion',
    'and': 'Logical AND',
    'or': 'Logical OR',
    'not': 'Logical NOT',
    'start': 'Start service/process',
    'stop': 'Stop service/process',
    'wait_for': 'Wait for condition',
    'on_event': 'Event handler',
    'emit_event': 'Emit event',
    'await': 'Await async operation',
    'async': 'Async function modifier',
    'yield': 'Yield from generator',
    'generator': 'Generator function',
    'future': 'Future/promise type',
    'true': 'Boolean true',
    'false': 'Boolean false',
    'null': 'Null value',
}

# Type documentation
TYPE_DOCS: Dict[str, str] = {
    'int': 'Integer number type',
    'string': 'String type for text',
    'float': 'Floating-point number',
    'bool': 'Boolean (true/false)',
    'void': 'No value type',
    'json': 'JSON data structure',
    'dynamic': 'Dynamic type (any)',
    'auto': 'Auto-inferred type',
    'long': 'Long integer',
    'double': 'Double precision float',
    'bit': 'Single bit',
    'byte': 'Single byte',
    'address': 'Memory address',
    'ptr': 'Pointer type',
    'pointer': 'Pointer type',
    'array': 'Array collection',
    'vector': 'Dynamic array',
    'stack': 'LIFO stack',
    'list': 'Linked list',
    'dictionary': 'Key-value dictionary',
    'dict': 'Key-value dictionary',
    'map': 'Key-value map',
    'datastruct': 'Custom data structure',
    'dataspace': 'Data space container',
    'shuffled': 'Shuffled collection',
    'iterator': 'Iterator type',
    'combo': 'Combination type',
    'openquote': 'Open quote type',
    'tuple': 'Immutable tuple',
    'set': 'Unique element set',
    'queue': 'FIFO queue',
    'instance': 'Object instance',
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
        self._build_static_completions()

    def _build_static_completions(self) -> None:
        """Build completion items for static entries (builtins, keywords, etc.)."""
        # Builtin functions
        for name in sorted(CSSL_BUILTINS):
            doc_info = BUILTIN_DOCS.get(name, {})
            signature = doc_info.get('signature', f'{name}()')
            doc = doc_info.get('doc', f'Built-in function: {name}')

            self._builtin_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Function,
                detail=signature,
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{signature}**\n\n{doc}"
                ),
                insert_text=f"{name}($1)",
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"1_{name}"  # Higher priority
            ))

        # Keywords
        for name in sorted(CSSL_KEYWORDS):
            doc = KEYWORD_DOCS.get(name, f'CSSL keyword: {name}')

            self._keyword_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Keyword,
                detail='keyword',
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{name}**\n\n{doc}"
                ),
                sort_text=f"2_{name}"
            ))

        # Types
        for name in sorted(CSSL_TYPES):
            doc = TYPE_DOCS.get(name, f'CSSL type: {name}')

            self._type_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Class,
                detail='type',
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{name}**\n\n{doc}"
                ),
                sort_text=f"1_{name}"  # Same priority as builtins
            ))

        # Modifiers
        for name in sorted(CSSL_MODIFIERS):
            self._modifier_completions.append(CompletionItem(
                label=name,
                kind=CompletionItemKind.Keyword,
                detail='modifier',
                documentation=f"Function modifier: {name}",
                sort_text=f"3_{name}"
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
            items.extend(self._get_local_variable_completions(document, position))
            items.extend(self._get_user_function_completions(document))
            items.extend(self._get_user_class_completions(document))
            items.extend(self._get_namespace_triggers())

        return CompletionList(is_incomplete=False, items=items)

    def _get_namespace_completions(self, namespace: Optional[str]) -> List[CompletionItem]:
        """Get completions for namespace members."""
        items: List[CompletionItem] = []

        if not namespace:
            # Show all known namespaces
            for ns_name in sorted(NAMESPACE_MEMBERS.keys()):
                items.append(CompletionItem(
                    label=ns_name,
                    kind=CompletionItemKind.Module,
                    detail='namespace',
                    documentation=f"CSSL namespace: {ns_name}",
                    insert_text=f"{ns_name}::",
                    sort_text=f"0_{ns_name}"
                ))
            return items

        # Find matching namespace (case-insensitive)
        ns_lower = namespace.lower()
        members = NAMESPACE_MEMBERS.get(ns_lower, [])

        for member in members:
            items.append(CompletionItem(
                label=member['name'],
                kind=CompletionItemKind.Method,
                detail=member.get('detail', ''),
                documentation=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{namespace}::{member['name']}**\n\n{member.get('detail', '')}"
                ),
                insert_text=member.get('snippet', member['name']),
                insert_text_format=InsertTextFormat.Snippet,
                sort_text=f"0_{member['name']}"
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

        # If it's a built-in type, show type methods
        if inferred_type:
            type_lower = inferred_type.lower().split('<')[0].strip()
            methods = TYPE_METHODS.get(type_lower, [])

            for method in methods:
                # Don't add duplicates from class methods
                if not any(item.label == method['name'] for item in items):
                    items.append(CompletionItem(
                        label=method['name'],
                        kind=CompletionItemKind.Method,
                        detail=method.get('detail', ''),
                        documentation=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"**{method['name']}**\n\n{method.get('detail', '')}"
                        ),
                        insert_text=method.get('snippet', method['name']),
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"1_{method['name']}"  # Lower priority than class methods
                    ))

        # If still no items, try to infer type from expression pattern
        if not items:
            inferred_type = self._infer_expression_type(document, base_expression)
            if inferred_type:
                type_lower = inferred_type.lower()
                methods = TYPE_METHODS.get(type_lower, [])
                for method in methods:
                    items.append(CompletionItem(
                        label=method['name'],
                        kind=CompletionItemKind.Method,
                        detail=method.get('detail', ''),
                        insert_text=method.get('snippet', method['name']),
                        insert_text_format=InsertTextFormat.Snippet,
                        sort_text=f"0_{method['name']}"
                    ))

        # If STILL no items, show generic methods
        if not items:
            common_methods = [
                {'name': 'length', 'detail': 'Get length/size'},
                {'name': 'toString', 'detail': 'Convert to string'},
                {'name': 'toInt', 'detail': 'Convert to integer'},
                {'name': 'toFloat', 'detail': 'Convert to float'},
                {'name': 'contains', 'detail': 'Check if contains value'},
                {'name': 'get', 'detail': 'Get value'},
                {'name': 'set', 'detail': 'Set value'},
                {'name': 'keys', 'detail': 'Get keys'},
                {'name': 'values', 'detail': 'Get values'},
            ]
            for method in common_methods:
                items.append(CompletionItem(
                    label=method['name'],
                    kind=CompletionItemKind.Method,
                    detail=method.get('detail', ''),
                    sort_text=f"1_{method['name']}"
                ))

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
            for type_name in FILTER_TYPES:
                items.append(CompletionItem(
                    label=type_name,
                    kind=CompletionItemKind.TypeParameter,
                    detail='filter type',
                    documentation=f"Filter by {type_name} type",
                    insert_text=f"{type_name}::",
                    sort_text=f"0_{type_name}"
                ))
            return items

        # Show filter operators for the type
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
                sort_text=f"0_{op['name']}"
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

        for ns_name in sorted(NAMESPACE_MEMBERS.keys()):
            items.append(CompletionItem(
                label=f"{ns_name}::",
                kind=CompletionItemKind.Module,
                detail='namespace',
                documentation=f"Access {ns_name} namespace members",
                insert_text=f"{ns_name}::",
                sort_text=f"1_{ns_name}"
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

        # Check if it's a direct variable reference
        if document.symbol_table:
            symbol = document.symbol_table.get_symbol(expression)
            if symbol and symbol.type_info:
                return symbol.type_info

        # Check if expression matches known type names
        if expression.lower() in CSSL_TYPES:
            return expression.lower()

        # Check for constructor calls: new ClassName()
        if expression.startswith('new '):
            class_name = expression[4:].strip('() ')
            return class_name

        # Check for namespace prefixes
        if '::' in expression:
            ns, _ = expression.rsplit('::', 1)
            ns_lower = ns.lower()
            if ns_lower in NAMESPACE_MEMBERS:
                # Return the namespace name as type hint
                return ns_lower

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
