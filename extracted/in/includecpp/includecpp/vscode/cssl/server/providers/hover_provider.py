"""
Hover Provider for the CSSL Language Server.

Provides hover information (documentation) for CSSL code elements including:
- Built-in functions and types
- Keywords and modifiers
- User-defined functions and classes
- Local variables
- Namespace members
"""

import logging
from typing import Optional
from lsprotocol.types import (
    Hover,
    MarkupContent,
    MarkupKind,
    Position,
    Range,
)

from ..analysis.document_manager import DocumentAnalysis
from ..analysis.semantic_analyzer import CSSL_KEYWORDS, CSSL_TYPES, CSSL_BUILTINS, CSSL_MODIFIERS
from ..utils.symbol_table import SymbolKind, Symbol
from ..utils.position_utils import get_word_at_position

logger = logging.getLogger('cssl-lsp.hover')


# Comprehensive builtin function documentation
BUILTIN_DOCS = {
    # I/O Functions
    'print': {
        'signature': 'print(value, ...)',
        'doc': 'Print values to standard output without adding a newline at the end.',
        'params': [('value', 'dynamic', 'Value(s) to print')],
        'returns': 'void',
        'example': 'print("Hello, ");  // Output: Hello, '
    },
    'printl': {
        'signature': 'printl(value, ...)',
        'doc': 'Print values to standard output with a newline at the end.',
        'params': [('value', 'dynamic', 'Value(s) to print')],
        'returns': 'void',
        'example': 'printl("Hello!");  // Output: Hello!\\n'
    },
    'println': {
        'signature': 'println(value, ...)',
        'doc': 'Print values to standard output with a newline at the end.',
        'params': [('value', 'dynamic', 'Value(s) to print')],
        'returns': 'void',
        'example': 'println("Hello!");  // Output: Hello!\\n'
    },
    'input': {
        'signature': 'input(prompt?)',
        'doc': 'Read a line of input from the user. Optionally display a prompt first.',
        'params': [('prompt', 'string', 'Optional prompt to display')],
        'returns': 'string',
        'example': 'string name = input("Enter name: ");'
    },
    'read': {
        'signature': 'read()',
        'doc': 'Read input from standard input.',
        'params': [],
        'returns': 'string',
        'example': 'string data = read();'
    },
    'readline': {
        'signature': 'readline()',
        'doc': 'Read a single line from standard input.',
        'params': [],
        'returns': 'string',
        'example': 'string line = readline();'
    },
    'write': {
        'signature': 'write(value)',
        'doc': 'Write value to standard output.',
        'params': [('value', 'dynamic', 'Value to write')],
        'returns': 'void',
        'example': 'write("data");'
    },
    'writeline': {
        'signature': 'writeline(value)',
        'doc': 'Write value to standard output with a newline.',
        'params': [('value', 'dynamic', 'Value to write')],
        'returns': 'void',
        'example': 'writeline("data");'
    },

    # Type Functions
    'len': {
        'signature': 'len(collection)',
        'doc': 'Get the length or size of a collection (array, string, dict, etc.).',
        'params': [('collection', 'dynamic', 'Collection to measure')],
        'returns': 'int',
        'example': 'int size = len(myArray);'
    },
    'type': {
        'signature': 'type(value)',
        'doc': 'Get the type name of a value as a string.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'string',
        'example': 'string t = type(42);  // "int"'
    },
    'typeof': {
        'signature': 'typeof(value)',
        'doc': 'Get the type of a value.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'string',
        'example': 'string t = typeof(myVar);'
    },
    'toInt': {
        'signature': 'toInt(value)',
        'doc': 'Convert a value to an integer.',
        'params': [('value', 'dynamic', 'Value to convert')],
        'returns': 'int',
        'example': 'int n = toInt("42");  // 42'
    },
    'toFloat': {
        'signature': 'toFloat(value)',
        'doc': 'Convert a value to a floating-point number.',
        'params': [('value', 'dynamic', 'Value to convert')],
        'returns': 'float',
        'example': 'float f = toFloat("3.14");  // 3.14'
    },
    'toString': {
        'signature': 'toString(value)',
        'doc': 'Convert a value to its string representation.',
        'params': [('value', 'dynamic', 'Value to convert')],
        'returns': 'string',
        'example': 'string s = toString(42);  // "42"'
    },
    'toBool': {
        'signature': 'toBool(value)',
        'doc': 'Convert a value to a boolean.',
        'params': [('value', 'dynamic', 'Value to convert')],
        'returns': 'bool',
        'example': 'bool b = toBool(1);  // true'
    },

    # Memory Functions
    'memory': {
        'signature': 'memory()',
        'doc': 'Get information about current memory usage.',
        'params': [],
        'returns': 'dict',
        'example': 'json mem = memory();'
    },
    'address': {
        'signature': 'address(var)',
        'doc': 'Get the memory address of a variable.',
        'params': [('var', 'dynamic', 'Variable to get address of')],
        'returns': 'address',
        'example': 'address addr = address(myVar);'
    },
    'reflect': {
        'signature': 'reflect(obj)',
        'doc': 'Get comprehensive reflection information about an object including methods, properties, type info, and metadata.',
        'params': [('obj', 'dynamic', 'Object to reflect')],
        'returns': 'dict',
        'example': '''json info = reflect(myClass);
// Returns: {
//   "type": "class",
//   "name": "MyClass",
//   "methods": ["method1", "method2"],
//   "properties": ["prop1", "prop2"],
//   "parent": "BaseClass",
//   "modifiers": ["public"],
//   "line": 10
// }'''
    },
    'resolve': {
        'signature': 'resolve(name, context?)',
        'doc': 'Resolve a symbol by name at runtime. Returns the value/reference of the named symbol in the current or specified context.',
        'params': [
            ('name', 'string', 'Name of the symbol to resolve'),
            ('context', 'dynamic', 'Optional context/scope to search in')
        ],
        'returns': 'dynamic',
        'example': '''// Resolve variable by name
dynamic val = resolve("myVariable");

// Resolve in specific context
dynamic method = resolve("methodName", myObject);

// Dynamic function call
resolve("funcName")();'''
    },
    'getattr': {
        'signature': 'getattr(obj, name, default?)',
        'doc': 'Get an attribute from an object by name. Returns default if not found.',
        'params': [
            ('obj', 'dynamic', 'Object to get attribute from'),
            ('name', 'string', 'Attribute name'),
            ('default', 'dynamic', 'Default value if not found')
        ],
        'returns': 'dynamic',
        'example': 'dynamic value = getattr(obj, "property", null);'
    },
    'setattr': {
        'signature': 'setattr(obj, name, value)',
        'doc': 'Set an attribute on an object by name.',
        'params': [
            ('obj', 'dynamic', 'Object to set attribute on'),
            ('name', 'string', 'Attribute name'),
            ('value', 'dynamic', 'Value to set')
        ],
        'returns': 'void',
        'example': 'setattr(obj, "property", 42);'
    },
    'hasattr': {
        'signature': 'hasattr(obj, name)',
        'doc': 'Check if an object has an attribute with the given name.',
        'params': [
            ('obj', 'dynamic', 'Object to check'),
            ('name', 'string', 'Attribute name')
        ],
        'returns': 'bool',
        'example': 'if (hasattr(obj, "method")) { obj.method(); }'
    },
    'delattr': {
        'signature': 'delattr(obj, name)',
        'doc': 'Delete an attribute from an object by name.',
        'params': [
            ('obj', 'dynamic', 'Object to delete attribute from'),
            ('name', 'string', 'Attribute name')
        ],
        'returns': 'void',
        'example': 'delattr(obj, "tempProperty");'
    },
    'dir': {
        'signature': 'dir(obj?)',
        'doc': 'Get a list of all attributes and methods of an object. Without argument, returns names in current scope.',
        'params': [('obj', 'dynamic', 'Optional object to inspect')],
        'returns': 'array<string>',
        'example': 'array attrs = dir(myObject);'
    },
    'vars': {
        'signature': 'vars(obj?)',
        'doc': 'Get the __dict__ attribute of an object, or local variables if no argument.',
        'params': [('obj', 'dynamic', 'Optional object')],
        'returns': 'dict',
        'example': 'json localVars = vars();'
    },
    'locals': {
        'signature': 'locals()',
        'doc': 'Get a dictionary of all local variables in the current scope.',
        'params': [],
        'returns': 'dict',
        'example': 'json local = locals();'
    },
    'globals': {
        'signature': 'globals()',
        'doc': 'Get a dictionary of all global variables.',
        'params': [],
        'returns': 'dict',
        'example': 'json global = globals();'
    },
    'callable': {
        'signature': 'callable(obj)',
        'doc': 'Check if an object is callable (function, method, or has __call__).',
        'params': [('obj', 'dynamic', 'Object to check')],
        'returns': 'bool',
        'example': 'if (callable(obj)) { obj(); }'
    },
    'classof': {
        'signature': 'classof(obj)',
        'doc': 'Get the class/type of an object.',
        'params': [('obj', 'dynamic', 'Object to get class of')],
        'returns': 'class',
        'example': 'auto cls = classof(myInstance);'
    },
    'nameof': {
        'signature': 'nameof(symbol)',
        'doc': 'Get the name of a symbol as a string (compile-time).',
        'params': [('symbol', 'dynamic', 'Symbol to get name of')],
        'returns': 'string',
        'example': 'string name = nameof(myVariable);  // "myVariable"'
    },
    'sizeof': {
        'signature': 'sizeof(obj)',
        'doc': 'Get the size in bytes of an object or type.',
        'params': [('obj', 'dynamic', 'Object or type to measure')],
        'returns': 'int',
        'example': 'int bytes = sizeof(myStruct);'
    },
    'alignof': {
        'signature': 'alignof(type)',
        'doc': 'Get the alignment requirement in bytes of a type.',
        'params': [('type', 'type', 'Type to get alignment of')],
        'returns': 'int',
        'example': 'int align = alignof(int);'
    },
    'destroy': {
        'signature': 'destroy(var)',
        'doc': 'Explicitly destroy a variable and free its memory.',
        'params': [('var', 'dynamic', 'Variable to destroy')],
        'returns': 'void',
        'example': 'destroy(tempData);'
    },

    # Control Functions
    'exit': {
        'signature': 'exit(code?)',
        'doc': 'Exit the program with an optional exit code.',
        'params': [('code', 'int', 'Exit code (default: 0)')],
        'returns': 'void',
        'example': 'exit(0);  // Normal exit'
    },
    'sleep': {
        'signature': 'sleep(ms)',
        'doc': 'Pause execution for the specified number of milliseconds.',
        'params': [('ms', 'int', 'Milliseconds to sleep')],
        'returns': 'void',
        'example': 'sleep(1000);  // Sleep 1 second'
    },
    'range': {
        'signature': 'range(start, end, step?)',
        'doc': 'Generate a range of numbers from start to end (exclusive).',
        'params': [
            ('start', 'int', 'Start value (inclusive)'),
            ('end', 'int', 'End value (exclusive)'),
            ('step', 'int', 'Step increment (default: 1)')
        ],
        'returns': 'iterator',
        'example': 'foreach (i in range(0, 10)) { }'
    },
    'isavailable': {
        'signature': 'isavailable(name)',
        'doc': 'Check if a named resource or variable is available.',
        'params': [('name', 'string', 'Name to check')],
        'returns': 'bool',
        'example': 'if (isavailable("myService")) { }'
    },

    # Utility Functions
    'OpenFind': {
        'signature': 'OpenFind(pattern)',
        'doc': 'Open a find dialog with the specified pattern.',
        'params': [('pattern', 'string', 'Search pattern')],
        'returns': 'dynamic',
        'example': 'OpenFind("*.txt");'
    },
    'cast': {
        'signature': 'cast(value, type)',
        'doc': 'Cast a value to the specified type.',
        'params': [
            ('value', 'dynamic', 'Value to cast'),
            ('type', 'string', 'Target type name')
        ],
        'returns': 'dynamic',
        'example': 'int n = cast(myFloat, "int");'
    },
    'share': {
        'signature': 'share(name, value)',
        'doc': 'Share a variable across modules/contexts.',
        'params': [
            ('name', 'string', 'Shared variable name'),
            ('value', 'dynamic', 'Value to share')
        ],
        'returns': 'void',
        'example': 'share("config", myConfig);'
    },
    'shared': {
        'signature': 'shared(name)',
        'doc': 'Access a shared variable by name.',
        'params': [('name', 'string', 'Shared variable name')],
        'returns': 'dynamic',
        'example': 'json config = shared("config");'
    },
    'include': {
        'signature': 'include(path)',
        'doc': 'Include and execute a CSSL file.',
        'params': [('path', 'string', 'Path to CSSL file')],
        'returns': 'void',
        'example': 'include("utils.cssl");'
    },
    'includecpp': {
        'signature': 'includecpp(path)',
        'doc': 'Include a C++ file for native functionality.',
        'params': [('path', 'string', 'Path to C++ file')],
        'returns': 'void',
        'example': 'includecpp("native.cpp");'
    },

    # Snapshot Functions
    'snapshot': {
        'signature': 'snapshot(name)',
        'doc': 'Create a snapshot of a variable\'s current state.',
        'params': [('name', 'string', 'Variable name to snapshot')],
        'returns': 'void',
        'example': 'snapshot(myData);  // Access later with %myData'
    },
    'get_snapshot': {
        'signature': 'get_snapshot(name)',
        'doc': 'Get the value from a named snapshot.',
        'params': [('name', 'string', 'Snapshot name')],
        'returns': 'dynamic',
        'example': 'json old = get_snapshot("myData");'
    },
    'has_snapshot': {
        'signature': 'has_snapshot(name)',
        'doc': 'Check if a snapshot with the given name exists.',
        'params': [('name', 'string', 'Snapshot name')],
        'returns': 'bool',
        'example': 'if (has_snapshot("myData")) { }'
    },
    'clear_snapshot': {
        'signature': 'clear_snapshot(name)',
        'doc': 'Clear a specific snapshot.',
        'params': [('name', 'string', 'Snapshot name')],
        'returns': 'void',
        'example': 'clear_snapshot("myData");'
    },
    'clear_snapshots': {
        'signature': 'clear_snapshots()',
        'doc': 'Clear all snapshots.',
        'params': [],
        'returns': 'void',
        'example': 'clear_snapshots();'
    },
    'list_snapshots': {
        'signature': 'list_snapshots()',
        'doc': 'Get a list of all snapshot names.',
        'params': [],
        'returns': 'array<string>',
        'example': 'array names = list_snapshots();'
    },
    'restore_snapshot': {
        'signature': 'restore_snapshot(name)',
        'doc': 'Restore a variable to its snapshot state.',
        'params': [('name', 'string', 'Snapshot name')],
        'returns': 'void',
        'example': 'restore_snapshot("myData");'
    },

    # Math Functions
    'random': {
        'signature': 'random()',
        'doc': 'Generate a random floating-point number between 0 and 1.',
        'params': [],
        'returns': 'float',
        'example': 'float r = random();  // 0.0 to 1.0'
    },
    'randint': {
        'signature': 'randint(min, max)',
        'doc': 'Generate a random integer between min and max (inclusive).',
        'params': [
            ('min', 'int', 'Minimum value'),
            ('max', 'int', 'Maximum value')
        ],
        'returns': 'int',
        'example': 'int dice = randint(1, 6);'
    },
    'round': {
        'signature': 'round(value, decimals?)',
        'doc': 'Round a number to the specified number of decimal places.',
        'params': [
            ('value', 'float', 'Value to round'),
            ('decimals', 'int', 'Decimal places (default: 0)')
        ],
        'returns': 'float',
        'example': 'float r = round(3.14159, 2);  // 3.14'
    },
    'abs': {
        'signature': 'abs(value)',
        'doc': 'Get the absolute value of a number.',
        'params': [('value', 'float', 'Number')],
        'returns': 'float',
        'example': 'int a = abs(-5);  // 5'
    },
    'ceil': {
        'signature': 'ceil(value)',
        'doc': 'Round a number up to the nearest integer.',
        'params': [('value', 'float', 'Value to round')],
        'returns': 'int',
        'example': 'int c = ceil(3.2);  // 4'
    },
    'floor': {
        'signature': 'floor(value)',
        'doc': 'Round a number down to the nearest integer.',
        'params': [('value', 'float', 'Value to round')],
        'returns': 'int',
        'example': 'int f = floor(3.8);  // 3'
    },
    'sqrt': {
        'signature': 'sqrt(value)',
        'doc': 'Calculate the square root of a number.',
        'params': [('value', 'float', 'Number')],
        'returns': 'float',
        'example': 'float s = sqrt(16);  // 4.0'
    },
    'pow': {
        'signature': 'pow(base, exponent)',
        'doc': 'Raise a number to a power.',
        'params': [
            ('base', 'float', 'Base number'),
            ('exponent', 'float', 'Exponent')
        ],
        'returns': 'float',
        'example': 'float p = pow(2, 8);  // 256.0'
    },
    'min': {
        'signature': 'min(a, b, ...)',
        'doc': 'Get the minimum value from the arguments.',
        'params': [('values', 'dynamic', 'Values to compare')],
        'returns': 'dynamic',
        'example': 'int m = min(5, 3, 8);  // 3'
    },
    'max': {
        'signature': 'max(a, b, ...)',
        'doc': 'Get the maximum value from the arguments.',
        'params': [('values', 'dynamic', 'Values to compare')],
        'returns': 'dynamic',
        'example': 'int m = max(5, 3, 8);  // 8'
    },
    'sum': {
        'signature': 'sum(collection)',
        'doc': 'Sum all values in a collection.',
        'params': [('collection', 'array', 'Collection to sum')],
        'returns': 'dynamic',
        'example': 'int total = sum([1, 2, 3]);  // 6'
    },
    'sin': {
        'signature': 'sin(x)',
        'doc': 'Calculate the sine of an angle (in radians).',
        'params': [('x', 'float', 'Angle in radians')],
        'returns': 'float',
        'example': 'float s = sin(3.14159);'
    },
    'cos': {
        'signature': 'cos(x)',
        'doc': 'Calculate the cosine of an angle (in radians).',
        'params': [('x', 'float', 'Angle in radians')],
        'returns': 'float',
        'example': 'float c = cos(0);  // 1.0'
    },
    'tan': {
        'signature': 'tan(x)',
        'doc': 'Calculate the tangent of an angle (in radians).',
        'params': [('x', 'float', 'Angle in radians')],
        'returns': 'float',
        'example': 'float t = tan(0.785);'
    },
    'asin': {
        'signature': 'asin(x)',
        'doc': 'Calculate the arc sine (inverse sine) of a value.',
        'params': [('x', 'float', 'Value (-1 to 1)')],
        'returns': 'float',
        'example': 'float a = asin(0.5);'
    },
    'acos': {
        'signature': 'acos(x)',
        'doc': 'Calculate the arc cosine (inverse cosine) of a value.',
        'params': [('x', 'float', 'Value (-1 to 1)')],
        'returns': 'float',
        'example': 'float a = acos(0.5);'
    },
    'atan': {
        'signature': 'atan(x)',
        'doc': 'Calculate the arc tangent (inverse tangent) of a value.',
        'params': [('x', 'float', 'Value')],
        'returns': 'float',
        'example': 'float a = atan(1);'
    },
    'log': {
        'signature': 'log(x)',
        'doc': 'Calculate the natural logarithm (ln) of a value.',
        'params': [('x', 'float', 'Value (> 0)')],
        'returns': 'float',
        'example': 'float l = log(2.718);  // ~1.0'
    },
    'exp': {
        'signature': 'exp(x)',
        'doc': 'Calculate e raised to the power of x.',
        'params': [('x', 'float', 'Exponent')],
        'returns': 'float',
        'example': 'float e = exp(1);  // ~2.718'
    },

    # String Functions
    'upper': {
        'signature': 'upper(str)',
        'doc': 'Convert a string to uppercase.',
        'params': [('str', 'string', 'String to convert')],
        'returns': 'string',
        'example': 'string s = upper("hello");  // "HELLO"'
    },
    'lower': {
        'signature': 'lower(str)',
        'doc': 'Convert a string to lowercase.',
        'params': [('str', 'string', 'String to convert')],
        'returns': 'string',
        'example': 'string s = lower("HELLO");  // "hello"'
    },
    'trim': {
        'signature': 'trim(str)',
        'doc': 'Remove leading and trailing whitespace from a string.',
        'params': [('str', 'string', 'String to trim')],
        'returns': 'string',
        'example': 'string s = trim("  hello  ");  // "hello"'
    },
    'split': {
        'signature': 'split(str, delimiter)',
        'doc': 'Split a string into an array using a delimiter.',
        'params': [
            ('str', 'string', 'String to split'),
            ('delimiter', 'string', 'Delimiter to split on')
        ],
        'returns': 'array<string>',
        'example': 'array parts = split("a,b,c", ",");  // ["a", "b", "c"]'
    },
    'join': {
        'signature': 'join(arr, delimiter)',
        'doc': 'Join array elements into a string with a delimiter.',
        'params': [
            ('arr', 'array', 'Array to join'),
            ('delimiter', 'string', 'Delimiter between elements')
        ],
        'returns': 'string',
        'example': 'string s = join(["a", "b"], ",");  // "a,b"'
    },
    'replace': {
        'signature': 'replace(str, old, new)',
        'doc': 'Replace all occurrences of a substring.',
        'params': [
            ('str', 'string', 'Original string'),
            ('old', 'string', 'Substring to replace'),
            ('new', 'string', 'Replacement string')
        ],
        'returns': 'string',
        'example': 'string s = replace("hello", "l", "L");  // "heLLo"'
    },
    'substr': {
        'signature': 'substr(str, start, length?)',
        'doc': 'Extract a substring from a string.',
        'params': [
            ('str', 'string', 'Original string'),
            ('start', 'int', 'Start index'),
            ('length', 'int', 'Optional length')
        ],
        'returns': 'string',
        'example': 'string s = substr("hello", 1, 3);  // "ell"'
    },
    'contains': {
        'signature': 'contains(collection, item)',
        'doc': 'Check if a collection contains an item.',
        'params': [
            ('collection', 'dynamic', 'Collection to search'),
            ('item', 'dynamic', 'Item to find')
        ],
        'returns': 'bool',
        'example': 'bool has = contains("hello", "ell");  // true'
    },
    'startswith': {
        'signature': 'startswith(str, prefix)',
        'doc': 'Check if a string starts with a prefix.',
        'params': [
            ('str', 'string', 'String to check'),
            ('prefix', 'string', 'Prefix to look for')
        ],
        'returns': 'bool',
        'example': 'bool b = startswith("hello", "he");  // true'
    },
    'endswith': {
        'signature': 'endswith(str, suffix)',
        'doc': 'Check if a string ends with a suffix.',
        'params': [
            ('str', 'string', 'String to check'),
            ('suffix', 'string', 'Suffix to look for')
        ],
        'returns': 'bool',
        'example': 'bool b = endswith("hello", "lo");  // true'
    },
    'format': {
        'signature': 'format(template, ...args)',
        'doc': 'Format a string with indexed placeholders. Use this for expression interpolation instead of `{expr}` in strings.',
        'params': [
            ('template', 'string', 'Template string with {0}, {1}, etc.'),
            ('args', 'dynamic', 'Values to insert at placeholders')
        ],
        'returns': 'string',
        'example': '''// Basic formatting
string s = format("Hello {0}!", "World");

// Expression interpolation (use this instead of {func()} in strings)
string info = format("Object: {0}", reflect(myObj));
string calc = format("Result: {0}", someFunc(x, y));'''
    },
    'concat': {
        'signature': 'concat(a, b, ...)',
        'doc': 'Concatenate multiple strings or values.',
        'params': [('values', 'dynamic', 'Values to concatenate')],
        'returns': 'string',
        'example': 'string s = concat("Hello", " ", "World");'
    },

    # Array Functions
    'push': {
        'signature': 'push(arr, item)',
        'doc': 'Add an item to the end of an array.',
        'params': [
            ('arr', 'array', 'Array to modify'),
            ('item', 'dynamic', 'Item to add')
        ],
        'returns': 'void',
        'example': 'push(myArray, "new item");'
    },
    'pop': {
        'signature': 'pop(arr)',
        'doc': 'Remove and return the last item from an array.',
        'params': [('arr', 'array', 'Array to modify')],
        'returns': 'dynamic',
        'example': 'dynamic last = pop(myArray);'
    },
    'shift': {
        'signature': 'shift(arr)',
        'doc': 'Remove and return the first item from an array.',
        'params': [('arr', 'array', 'Array to modify')],
        'returns': 'dynamic',
        'example': 'dynamic first = shift(myArray);'
    },
    'unshift': {
        'signature': 'unshift(arr, item)',
        'doc': 'Add an item to the beginning of an array.',
        'params': [
            ('arr', 'array', 'Array to modify'),
            ('item', 'dynamic', 'Item to add')
        ],
        'returns': 'void',
        'example': 'unshift(myArray, "first item");'
    },
    'slice': {
        'signature': 'slice(arr, start, end?)',
        'doc': 'Extract a portion of an array.',
        'params': [
            ('arr', 'array', 'Array to slice'),
            ('start', 'int', 'Start index'),
            ('end', 'int', 'End index (exclusive)')
        ],
        'returns': 'array',
        'example': 'array part = slice(arr, 1, 3);'
    },
    'sort': {
        'signature': 'sort(arr)',
        'doc': 'Sort an array in ascending order.',
        'params': [('arr', 'array', 'Array to sort')],
        'returns': 'array',
        'example': 'array sorted = sort([3, 1, 2]);  // [1, 2, 3]'
    },
    'rsort': {
        'signature': 'rsort(arr)',
        'doc': 'Sort an array in descending order.',
        'params': [('arr', 'array', 'Array to sort')],
        'returns': 'array',
        'example': 'array sorted = rsort([1, 3, 2]);  // [3, 2, 1]'
    },
    'unique': {
        'signature': 'unique(arr)',
        'doc': 'Get unique elements from an array.',
        'params': [('arr', 'array', 'Array to filter')],
        'returns': 'array',
        'example': 'array u = unique([1, 2, 2, 3]);  // [1, 2, 3]'
    },
    'flatten': {
        'signature': 'flatten(arr)',
        'doc': 'Flatten a nested array into a single level.',
        'params': [('arr', 'array', 'Nested array')],
        'returns': 'array',
        'example': 'array f = flatten([[1, 2], [3, 4]]);  // [1, 2, 3, 4]'
    },
    'filter': {
        'signature': 'filter(arr, predicate)',
        'doc': 'Filter array elements that match a predicate.',
        'params': [
            ('arr', 'array', 'Array to filter'),
            ('predicate', 'function', 'Filter function')
        ],
        'returns': 'array',
        'example': 'array evens = filter(arr, x -> x % 2 == 0);'
    },
    'map': {
        'signature': 'map(arr, func)',
        'doc': 'Transform each element in an array.',
        'params': [
            ('arr', 'array', 'Array to map'),
            ('func', 'function', 'Transform function')
        ],
        'returns': 'array',
        'example': 'array doubled = map(arr, x -> x * 2);'
    },
    'reduce': {
        'signature': 'reduce(arr, func, initial)',
        'doc': 'Reduce an array to a single value.',
        'params': [
            ('arr', 'array', 'Array to reduce'),
            ('func', 'function', 'Reducer function (acc, val) -> acc'),
            ('initial', 'dynamic', 'Initial accumulator value')
        ],
        'returns': 'dynamic',
        'example': 'int sum = reduce(arr, (a, b) -> a + b, 0);'
    },
    'find': {
        'signature': 'find(arr, predicate)',
        'doc': 'Find the first element matching a predicate.',
        'params': [
            ('arr', 'array', 'Array to search'),
            ('predicate', 'function', 'Match function')
        ],
        'returns': 'dynamic',
        'example': 'dynamic found = find(arr, x -> x > 10);'
    },
    'findindex': {
        'signature': 'findindex(arr, predicate)',
        'doc': 'Find the index of the first matching element.',
        'params': [
            ('arr', 'array', 'Array to search'),
            ('predicate', 'function', 'Match function')
        ],
        'returns': 'int',
        'example': 'int idx = findindex(arr, x -> x > 10);'
    },
    'every': {
        'signature': 'every(arr, predicate)',
        'doc': 'Check if all elements match a predicate.',
        'params': [
            ('arr', 'array', 'Array to check'),
            ('predicate', 'function', 'Test function')
        ],
        'returns': 'bool',
        'example': 'bool allPositive = every(arr, x -> x > 0);'
    },
    'some': {
        'signature': 'some(arr, predicate)',
        'doc': 'Check if any element matches a predicate.',
        'params': [
            ('arr', 'array', 'Array to check'),
            ('predicate', 'function', 'Test function')
        ],
        'returns': 'bool',
        'example': 'bool hasNegative = some(arr, x -> x < 0);'
    },

    # Dictionary Functions
    'keys': {
        'signature': 'keys(obj)',
        'doc': 'Get all keys from an object or dictionary.',
        'params': [('obj', 'dict', 'Object to get keys from')],
        'returns': 'array<string>',
        'example': 'array k = keys(myDict);'
    },
    'values': {
        'signature': 'values(obj)',
        'doc': 'Get all values from an object or dictionary.',
        'params': [('obj', 'dict', 'Object to get values from')],
        'returns': 'array',
        'example': 'array v = values(myDict);'
    },
    'items': {
        'signature': 'items(obj)',
        'doc': 'Get all key-value pairs as an array of tuples.',
        'params': [('obj', 'dict', 'Object to iterate')],
        'returns': 'array<tuple>',
        'example': 'foreach ((k, v) in items(obj)) { }'
    },
    'haskey': {
        'signature': 'haskey(obj, key)',
        'doc': 'Check if an object has a specific key.',
        'params': [
            ('obj', 'dict', 'Object to check'),
            ('key', 'string', 'Key to look for')
        ],
        'returns': 'bool',
        'example': 'bool has = haskey(obj, "name");'
    },
    'getkey': {
        'signature': 'getkey(obj, key)',
        'doc': 'Get a value by key from an object.',
        'params': [
            ('obj', 'dict', 'Object to access'),
            ('key', 'string', 'Key to get')
        ],
        'returns': 'dynamic',
        'example': 'dynamic val = getkey(obj, "name");'
    },
    'setkey': {
        'signature': 'setkey(obj, key, value)',
        'doc': 'Set a key-value pair in an object.',
        'params': [
            ('obj', 'dict', 'Object to modify'),
            ('key', 'string', 'Key to set'),
            ('value', 'dynamic', 'Value to assign')
        ],
        'returns': 'void',
        'example': 'setkey(obj, "name", "John");'
    },
    'delkey': {
        'signature': 'delkey(obj, key)',
        'doc': 'Delete a key from an object.',
        'params': [
            ('obj', 'dict', 'Object to modify'),
            ('key', 'string', 'Key to delete')
        ],
        'returns': 'void',
        'example': 'delkey(obj, "temp");'
    },
    'merge': {
        'signature': 'merge(obj1, obj2)',
        'doc': 'Merge two objects into a new object.',
        'params': [
            ('obj1', 'dict', 'First object'),
            ('obj2', 'dict', 'Second object (overwrites)')
        ],
        'returns': 'dict',
        'example': 'json merged = merge(defaults, overrides);'
    },

    # Date/Time Functions
    'now': {
        'signature': 'now()',
        'doc': 'Get the current timestamp.',
        'params': [],
        'returns': 'int',
        'example': 'int ts = now();'
    },
    'timestamp': {
        'signature': 'timestamp()',
        'doc': 'Get the current Unix timestamp in seconds.',
        'params': [],
        'returns': 'int',
        'example': 'int unix = timestamp();'
    },
    'date': {
        'signature': 'date(format?)',
        'doc': 'Get the current date as a formatted string.',
        'params': [('format', 'string', 'Date format (default: YYYY-MM-DD)')],
        'returns': 'string',
        'example': 'string d = date();  // "2024-01-15"'
    },
    'time': {
        'signature': 'time(format?)',
        'doc': 'Get the current time as a formatted string.',
        'params': [('format', 'string', 'Time format (default: HH:MM:SS)')],
        'returns': 'string',
        'example': 'string t = time();  // "14:30:45"'
    },
    'datetime': {
        'signature': 'datetime(format?)',
        'doc': 'Get the current date and time as a formatted string.',
        'params': [('format', 'string', 'Datetime format')],
        'returns': 'string',
        'example': 'string dt = datetime();'
    },
    'strftime': {
        'signature': 'strftime(format, timestamp?)',
        'doc': 'Format a timestamp using strftime format codes.',
        'params': [
            ('format', 'string', 'Format string'),
            ('timestamp', 'int', 'Unix timestamp (default: now)')
        ],
        'returns': 'string',
        'example': 'string s = strftime("%Y-%m-%d", ts);'
    },

    # JSON Functions
    'tojson': {
        'signature': 'tojson(value)',
        'doc': 'Convert a value to a JSON string.',
        'params': [('value', 'dynamic', 'Value to serialize')],
        'returns': 'string',
        'example': 'string j = tojson(myData);'
    },
    'fromjson': {
        'signature': 'fromjson(str)',
        'doc': 'Parse a JSON string into a CSSL value.',
        'params': [('str', 'string', 'JSON string')],
        'returns': 'dynamic',
        'example': 'json data = fromjson(jsonStr);'
    },

    # Logging Functions
    'debug': {
        'signature': 'debug(msg)',
        'doc': 'Log a debug message.',
        'params': [('msg', 'string', 'Message to log')],
        'returns': 'void',
        'example': 'debug("Variable x = " + x);'
    },
    'error': {
        'signature': 'error(msg)',
        'doc': 'Log an error message.',
        'params': [('msg', 'string', 'Error message')],
        'returns': 'void',
        'example': 'error("Failed to connect!");'
    },
    'warn': {
        'signature': 'warn(msg)',
        'doc': 'Log a warning message.',
        'params': [('msg', 'string', 'Warning message')],
        'returns': 'void',
        'example': 'warn("Deprecated function used");'
    },

    # File Functions
    'readfile': {
        'signature': 'readfile(path)',
        'doc': 'Read the entire contents of a file.',
        'params': [('path', 'string', 'Path to file')],
        'returns': 'string',
        'example': 'string content = readfile("data.txt");'
    },
    'writefile': {
        'signature': 'writefile(path, content)',
        'doc': 'Write content to a file (overwrites if exists).',
        'params': [
            ('path', 'string', 'Path to file'),
            ('content', 'string', 'Content to write')
        ],
        'returns': 'void',
        'example': 'writefile("output.txt", data);'
    },
    'appendfile': {
        'signature': 'appendfile(path, content)',
        'doc': 'Append content to a file.',
        'params': [
            ('path', 'string', 'Path to file'),
            ('content', 'string', 'Content to append')
        ],
        'returns': 'void',
        'example': 'appendfile("log.txt", line);'
    },
    'readlines': {
        'signature': 'readlines(path)',
        'doc': 'Read a file as an array of lines.',
        'params': [('path', 'string', 'Path to file')],
        'returns': 'array<string>',
        'example': 'array lines = readlines("data.txt");'
    },
    'listdir': {
        'signature': 'listdir(path)',
        'doc': 'List contents of a directory.',
        'params': [('path', 'string', 'Directory path')],
        'returns': 'array<string>',
        'example': 'array files = listdir("./data");'
    },
    'makedirs': {
        'signature': 'makedirs(path)',
        'doc': 'Create a directory and all parent directories.',
        'params': [('path', 'string', 'Directory path')],
        'returns': 'void',
        'example': 'makedirs("./data/cache");'
    },
    'removefile': {
        'signature': 'removefile(path)',
        'doc': 'Delete a file.',
        'params': [('path', 'string', 'Path to file')],
        'returns': 'void',
        'example': 'removefile("temp.txt");'
    },
    'removedir': {
        'signature': 'removedir(path)',
        'doc': 'Delete a directory.',
        'params': [('path', 'string', 'Directory path')],
        'returns': 'void',
        'example': 'removedir("./temp");'
    },
    'copyfile': {
        'signature': 'copyfile(src, dest)',
        'doc': 'Copy a file to a new location.',
        'params': [
            ('src', 'string', 'Source path'),
            ('dest', 'string', 'Destination path')
        ],
        'returns': 'void',
        'example': 'copyfile("data.txt", "backup.txt");'
    },
    'movefile': {
        'signature': 'movefile(src, dest)',
        'doc': 'Move a file to a new location.',
        'params': [
            ('src', 'string', 'Source path'),
            ('dest', 'string', 'Destination path')
        ],
        'returns': 'void',
        'example': 'movefile("temp.txt", "archive/temp.txt");'
    },
    'filesize': {
        'signature': 'filesize(path)',
        'doc': 'Get the size of a file in bytes.',
        'params': [('path', 'string', 'Path to file')],
        'returns': 'int',
        'example': 'int size = filesize("data.bin");'
    },
    'pathexists': {
        'signature': 'pathexists(path)',
        'doc': 'Check if a path exists.',
        'params': [('path', 'string', 'Path to check')],
        'returns': 'bool',
        'example': 'if (pathexists("config.cssl")) { }'
    },
    'isfile': {
        'signature': 'isfile(path)',
        'doc': 'Check if a path is a file.',
        'params': [('path', 'string', 'Path to check')],
        'returns': 'bool',
        'example': 'if (isfile(path)) { }'
    },
    'isdir': {
        'signature': 'isdir(path)',
        'doc': 'Check if a path is a directory.',
        'params': [('path', 'string', 'Path to check')],
        'returns': 'bool',
        'example': 'if (isdir(path)) { }'
    },
    'basename': {
        'signature': 'basename(path)',
        'doc': 'Get the base name (file name) from a path.',
        'params': [('path', 'string', 'Full path')],
        'returns': 'string',
        'example': 'string name = basename("/path/to/file.txt");  // "file.txt"'
    },
    'dirname': {
        'signature': 'dirname(path)',
        'doc': 'Get the directory name from a path.',
        'params': [('path', 'string', 'Full path')],
        'returns': 'string',
        'example': 'string dir = dirname("/path/to/file.txt");  // "/path/to"'
    },
    'joinpath': {
        'signature': 'joinpath(a, b, ...)',
        'doc': 'Join path components with the correct separator.',
        'params': [('parts', 'string', 'Path parts to join')],
        'returns': 'string',
        'example': 'string p = joinpath("dir", "subdir", "file.txt");'
    },
    'splitpath': {
        'signature': 'splitpath(path)',
        'doc': 'Split a path into its components.',
        'params': [('path', 'string', 'Path to split')],
        'returns': 'array<string>',
        'example': 'array parts = splitpath("/path/to/file");'
    },
    'abspath': {
        'signature': 'abspath(path)',
        'doc': 'Get the absolute path.',
        'params': [('path', 'string', 'Relative or absolute path')],
        'returns': 'string',
        'example': 'string abs = abspath("./data");'
    },

    # Type Check Functions
    'isinstance': {
        'signature': 'isinstance(obj, type)',
        'doc': 'Check if an object is an instance of a type.',
        'params': [
            ('obj', 'dynamic', 'Object to check'),
            ('type', 'string', 'Type name')
        ],
        'returns': 'bool',
        'example': 'if (isinstance(x, "MyClass")) { }'
    },
    'isint': {
        'signature': 'isint(value)',
        'doc': 'Check if a value is an integer.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (isint(x)) { }'
    },
    'isfloat': {
        'signature': 'isfloat(value)',
        'doc': 'Check if a value is a float.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (isfloat(x)) { }'
    },
    'isstr': {
        'signature': 'isstr(value)',
        'doc': 'Check if a value is a string.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (isstr(x)) { }'
    },
    'isbool': {
        'signature': 'isbool(value)',
        'doc': 'Check if a value is a boolean.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (isbool(x)) { }'
    },
    'islist': {
        'signature': 'islist(value)',
        'doc': 'Check if a value is a list/array.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (islist(x)) { }'
    },
    'isdict': {
        'signature': 'isdict(value)',
        'doc': 'Check if a value is a dictionary.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (isdict(x)) { }'
    },
    'isnull': {
        'signature': 'isnull(value)',
        'doc': 'Check if a value is null.',
        'params': [('value', 'dynamic', 'Value to check')],
        'returns': 'bool',
        'example': 'if (isnull(x)) { }'
    },

    # Copy Functions
    'copy': {
        'signature': 'copy(value)',
        'doc': 'Create a shallow copy of a value.',
        'params': [('value', 'dynamic', 'Value to copy')],
        'returns': 'dynamic',
        'example': 'array copy = copy(original);'
    },
    'deepcopy': {
        'signature': 'deepcopy(value)',
        'doc': 'Create a deep copy of a value (including nested structures).',
        'params': [('value', 'dynamic', 'Value to copy')],
        'returns': 'dynamic',
        'example': 'json copy = deepcopy(nested);'
    },

    # Python Integration
    'pyimport': {
        'signature': 'pyimport(module)',
        'doc': 'Import a Python module for use in CSSL.',
        'params': [('module', 'string', 'Python module name')],
        'returns': 'dynamic',
        'example': 'dynamic np = pyimport("numpy");'
    },
}

# Keyword documentation
KEYWORD_DOCS = {
    'if': 'Conditional statement. Executes block if condition is true.\n\nSyntax: `if (condition) { ... }`',
    'else': 'Alternative branch for `if` statement.\n\nSyntax: `if (...) { } else { ... }`',
    'elif': 'Else-if branch for chained conditions.\n\nSyntax: `if (...) { } elif (...) { } else { }`',
    'while': 'Loop that repeats while condition is true.\n\nSyntax: `while (condition) { ... }`',
    'for': 'Classic C-style for loop.\n\nSyntax: `for (init; condition; update) { ... }`',
    'foreach': 'Iterate over elements in a collection.\n\nSyntax: `foreach (item in collection) { ... }`',
    'in': 'Used with `foreach` for iteration or membership testing.',
    'range': 'Generate a sequence of numbers.\n\nSyntax: `range(start, end, step?)`',
    'switch': 'Multi-way branch statement.\n\nSyntax: `switch (value) { case x: ... }`',
    'case': 'Label for a switch case.\n\nSyntax: `case value: ...`',
    'default': 'Default case in switch statement.',
    'break': 'Exit the current loop or switch statement.',
    'continue': 'Skip to the next iteration of a loop.',
    'return': 'Return a value from a function.\n\nSyntax: `return value;`',
    'try': 'Begin a try-catch block for exception handling.\n\nSyntax: `try { ... } catch (e) { ... }`',
    'catch': 'Handle an exception from a try block.',
    'finally': 'Block that always executes after try/catch.',
    'throw': 'Throw an exception.\n\nSyntax: `throw "Error message";`',
    'except': 'Alternative to catch for exception handling.',
    'always': 'Block that always executes (like finally).',
    'class': 'Define a new class.\n\nSyntax: `class ClassName { ... }`',
    'struct': 'Define a new struct (value type).\n\nSyntax: `struct StructName { ... }`',
    'enum': 'Define an enumeration.\n\nSyntax: `enum EnumName { A, B, C }`',
    'interface': 'Define an interface.\n\nSyntax: `interface IName { ... }`',
    'namespace': 'Define a namespace for grouping.\n\nSyntax: `namespace Name { ... }`',
    'define': 'Define a function.\n\nSyntax: `define funcName(params) { ... }`',
    'void': 'Indicates no return value.',
    'constr': 'Define a constructor for a class.\n\nSyntax: `constr(params) { ... }`',
    'new': 'Create a new instance of a class.\n\nSyntax: `new ClassName(args)`',
    'this': 'Reference to the current object instance.',
    'super': 'Reference to the parent class.',
    'extends': 'Inherit from a parent class.\n\nSyntax: `class Child extends Parent { }`',
    'overwrites': 'Override a parent method.\n\nSyntax: `overwrites define method() { }`',
    'service-init': 'Service initialization block. Runs once on startup.',
    'service-run': 'Service run block. Main service loop.',
    'service-include': 'Include additional service files.',
    'main': 'Main entry point of the program.',
    'package': 'Declare the package name.',
    'exec': 'Execute a string as code.',
    'as': 'Type alias or import alias.',
    'global': 'Declare a global variable.\n\nSyntax: `global varName = value;`',
    'include': 'Include a CSSL file.\n\nSyntax: `include "path.cssl";`',
    'get': 'Property getter definition.',
    'payload': 'Access service payload data.',
    'convert': 'Type conversion operation.',
    'and': 'Logical AND operator.',
    'or': 'Logical OR operator.',
    'not': 'Logical NOT operator.',
    'start': 'Start a service or process.',
    'stop': 'Stop a service or process.',
    'wait_for': 'Wait for a condition or event.',
    'on_event': 'Define an event handler.\n\nSyntax: `on_event "eventName" { ... }`',
    'emit_event': 'Emit an event.\n\nSyntax: `emit_event("eventName", data);`',
    'await': 'Await an async operation.',
    'async': 'Mark function as asynchronous.\n\nSyntax: `async define func() { }`',
    'yield': 'Yield a value from a generator.\n\nSyntax: `yield value;`',
    'generator': 'Define a generator function.\n\nSyntax: `generator define func() { yield ...; }`',
    'future': 'Future/promise type for async operations.',
    'true': 'Boolean true value.',
    'false': 'Boolean false value.',
    'null': 'Null/none value.',
    'True': 'Boolean true (Python-style alias).',
    'False': 'Boolean false (Python-style alias).',
    'None': 'Null value (Python-style alias).',
}

# Type documentation
TYPE_DOCS = {
    'int': 'Integer number type. Whole numbers without decimals.\n\nExample: `int x = 42;`',
    'string': '''String type for text. Enclosed in double or single quotes.

**String Interpolation (NO `f` prefix needed!):**
CSSL strings automatically support variable interpolation with `{var}` or `<var>` syntax:

```cssl
string name = "World";
printl("Hello {name}!");    // Output: Hello World!
printl("Hello <name>!");    // Output: Hello World! (legacy)
```

**Important:** Only simple variable names work - NOT expressions or function calls:
- ✅ `"{myVar}"` - works
- ❌ `"{func(x)}"` - prints literal string (use concatenation instead)

For expressions, use concatenation:
```cssl
printl("Result: " + toString(reflect(obj)));
```

Example: `string s = "Hello";`''',
    'float': 'Floating-point number. Numbers with decimals.\n\nExample: `float f = 3.14;`',
    'bool': 'Boolean type. Either `true` or `false`.\n\nExample: `bool flag = true;`',
    'void': 'No value type. Used for functions that return nothing.',
    'json': 'JSON data structure. Key-value pairs.\n\nExample: `json data = {"key": "value"};`',
    'dynamic': 'Dynamic type that can hold any value.\n\nExample: `dynamic x = "can be anything";`',
    'auto': 'Auto-inferred type. Compiler determines the type.\n\nExample: `auto x = 42;  // int`',
    'long': 'Long integer for larger numbers.',
    'double': 'Double precision floating-point.',
    'bit': 'Single bit (0 or 1).',
    'byte': 'Single byte (0-255).',
    'address': 'Memory address type.',
    'ptr': 'Pointer type. References another variable.\n\nUsage: `?varName` for pointer reference.\n\n**Methods:**\n- `get_address()` - Get memory address\n- `set_address(addr)` - Set pointer to address\n- `get_value()` - Get value at pointer\n- `set_value(val)` - Set value at pointer\n- `deref()` - Dereference pointer\n- `is_null()` - Check if null\n- `is_valid()` - Check if valid\n- `offset(n)` - Add offset\n- `free()` - Free memory',
    'pointer': 'Pointer type (alias for ptr).\n\n**Methods:**\n- `get_address()` - Get memory address\n- `set_address(addr)` - Set pointer to address\n- `get_value()` - Get value at pointer\n- `deref()` - Dereference pointer\n- `is_null()` - Check if null',
    'array': 'Dynamic array collection.\n\nExample: `array<int> nums = [1, 2, 3];`',
    'vector': 'Dynamic array (alias for array).',
    'stack': 'LIFO (Last In, First Out) stack data structure.',
    'list': 'Linked list data structure.',
    'dictionary': 'Key-value dictionary.\n\nExample: `dictionary<string, int> ages;`',
    'dict': 'Key-value dictionary (alias).',
    'map': 'Key-value map (alias for dictionary).',
    'datastruct': 'Custom data structure.',
    'dataspace': 'Data space container for large datasets.',
    'shuffled': 'Shuffled/randomized collection.',
    'iterator': 'Iterator for traversing collections.',
    'combo': 'Combination type for complex data.',
    'openquote': 'Open quote type for special string handling.',
    'tuple': 'Immutable tuple type.\n\nExample: `tuple<int, string> pair = (1, "one");`',
    'set': 'Set type with unique elements.\n\nExample: `set<int> nums = {1, 2, 3};`',
    'queue': 'FIFO (First In, First Out) queue data structure.',
    'instance': 'Object instance type.',
}

# Modifier documentation
MODIFIER_DOCS = {
    'undefined': 'Mark as undefined/uninitialized.',
    'open': 'Open modifier for extensibility.',
    'closed': 'Closed/sealed - cannot be extended.',
    'private': 'Private access - only accessible within the class.',
    'virtual': 'Virtual method - can be overridden.',
    'meta': 'Meta programming modifier.',
    'super': 'Reference to parent class.',
    'sqlbased': 'SQL-backed data structure.',
    'protected': 'Protected access - accessible in class and subclasses.',
    'limited': 'Limited access modifier.',
    'const': 'Constant - cannot be modified.\n\nExample: `const int MAX = 100;`',
    'static': 'Static - belongs to class, not instance.\n\nExample: `static int count = 0;`',
    'final': 'Final - cannot be overridden or modified.',
    'abstract': 'Abstract - must be implemented by subclass.',
    'readonly': 'Read-only - can only be set once.',
    'native': 'Native implementation (C++).',
    'unative': 'User-defined native implementation.',
    'embedded': 'Embedded code block.',
    'public': 'Public access - accessible everywhere.',
    'global': 'Global scope variable.',
    'shuffled': 'Shuffled/randomized modifier.',
    'bytearrayed': 'Stored as byte array.',
}


class HoverProvider:
    """
    Provides hover information for CSSL code elements.

    Shows documentation on hover for:
    - Built-in functions
    - Keywords
    - Types
    - Modifiers
    - User-defined symbols
    """

    def __init__(self):
        pass

    def get_hover(
        self,
        document: DocumentAnalysis,
        position: Position
    ) -> Optional[Hover]:
        """
        Get hover information at the given position.

        Args:
            document: The analyzed document
            position: Cursor position

        Returns:
            Hover with documentation, or None if no hover available
        """
        try:
            if document is None:
                logger.warning("Hover called with None document")
                return None

            text = document.text
            if not text:
                logger.debug("Document has no text")
                return None

            line = position.line
            column = position.character

            logger.debug(f"Getting hover at line {line}, column {column}")

            # Get the word at position
            word_info = get_word_at_position(text, line, column)

            if not word_info:
                logger.debug(f"No word found at position {line}:{column}")
                return None

            word, start_col, end_col = word_info
            logger.debug(f"Found word: '{word}' at {start_col}-{end_col}")

            # Check for special prefixes
            if word.startswith('?'):
                return self._hover_pointer_reference(document, word[1:], line, start_col, end_col)
            elif word.startswith('@'):
                return self._hover_global_reference(document, word[1:], line, start_col, end_col)
            elif word.startswith('$'):
                return self._hover_shared_reference(document, word[1:], line, start_col, end_col)
            elif word.startswith('%'):
                return self._hover_snapshot_reference(document, word[1:], line, start_col, end_col)

            # Create range for the word
            word_range = Range(
                start=Position(line=line, character=start_col),
                end=Position(line=line, character=end_col)
            )

            # Check builtins first
            if word in BUILTIN_DOCS:
                return self._format_builtin_hover(word, word_range)

            # Check keywords
            if word in KEYWORD_DOCS:
                return self._format_keyword_hover(word, word_range)

            # Check types
            if word in TYPE_DOCS:
                return self._format_type_hover(word, word_range)

            # Check modifiers
            if word in MODIFIER_DOCS:
                return self._format_modifier_hover(word, word_range)

            # Check user-defined symbols
            if document.symbol_table:
                symbol = document.symbol_table.get_symbol(word)
                if symbol:
                    return self._format_symbol_hover(symbol, word_range)

            logger.debug(f"No hover info for '{word}'")
            return None

        except Exception as e:
            logger.error(f"Error in get_hover: {e}", exc_info=True)
            return None

    def _format_builtin_hover(self, name: str, range: Range) -> Hover:
        """Format hover for a builtin function."""
        info = BUILTIN_DOCS.get(name, {})
        signature = info.get('signature', f'{name}()')
        doc = info.get('doc', f'Built-in function: {name}')
        returns = info.get('returns', 'dynamic')
        example = info.get('example', '')
        params = info.get('params', [])

        # Build markdown content
        lines = [
            f"```cssl",
            f"{signature} -> {returns}",
            f"```",
            "",
            doc,
        ]

        if params:
            lines.append("")
            lines.append("**Parameters:**")
            for param_name, param_type, param_doc in params:
                lines.append(f"- `{param_name}` ({param_type}): {param_doc}")

        if example:
            lines.append("")
            lines.append("**Example:**")
            lines.append(f"```cssl")
            lines.append(example)
            lines.append(f"```")

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value="\n".join(lines)
            ),
            range=range
        )

    def _format_keyword_hover(self, name: str, range: Range) -> Hover:
        """Format hover for a keyword."""
        doc = KEYWORD_DOCS.get(name, f'CSSL keyword: {name}')

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**{name}** (keyword)\n\n{doc}"
            ),
            range=range
        )

    def _format_type_hover(self, name: str, range: Range) -> Hover:
        """Format hover for a type."""
        doc = TYPE_DOCS.get(name, f'CSSL type: {name}')

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**{name}** (type)\n\n{doc}"
            ),
            range=range
        )

    def _format_modifier_hover(self, name: str, range: Range) -> Hover:
        """Format hover for a modifier."""
        doc = MODIFIER_DOCS.get(name, f'Function modifier: {name}')

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**{name}** (modifier)\n\n{doc}"
            ),
            range=range
        )

    def _format_symbol_hover(self, symbol: Symbol, range: Range) -> Hover:
        """Format hover for a user-defined symbol."""
        kind_name = symbol.kind.name.lower()

        if symbol.kind == SymbolKind.FUNCTION:
            # Build function signature
            params = []
            for p in symbol.parameters or []:
                if p.type_info:
                    params.append(f"{p.type_info} {p.name}")
                else:
                    params.append(p.name)
            param_str = ", ".join(params)
            return_type = symbol.return_type or "void"

            modifiers = " ".join(symbol.modifiers) + " " if symbol.modifiers else ""

            lines = [
                f"```cssl",
                f"{modifiers}define {symbol.name}({param_str}) -> {return_type}",
                f"```",
                "",
                f"User-defined function at line {symbol.line}"
            ]

            if symbol.documentation:
                lines.append("")
                lines.append(symbol.documentation)

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value="\n".join(lines)
                ),
                range=range
            )

        elif symbol.kind == SymbolKind.CLASS:
            lines = [
                f"```cssl",
                f"class {symbol.name}",
                f"```",
                "",
                f"User-defined class at line {symbol.line}"
            ]

            # Show class members if available
            if symbol.children:
                lines.append("")
                lines.append("**Members:**")
                for name, child in symbol.children.items():
                    if child.kind == SymbolKind.METHOD:
                        lines.append(f"- `{name}()` (method)")
                    elif child.kind == SymbolKind.PROPERTY:
                        lines.append(f"- `{name}` (property)")
                    else:
                        lines.append(f"- `{name}`")

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value="\n".join(lines)
                ),
                range=range
            )

        elif symbol.kind in (SymbolKind.VARIABLE, SymbolKind.PARAMETER):
            type_info = symbol.type_info or "dynamic"

            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"```cssl\n{type_info} {symbol.name}\n```\n\n{kind_name.capitalize()} defined at line {symbol.line}"
                ),
                range=range
            )

        elif symbol.kind == SymbolKind.GLOBAL:
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"```cssl\nglobal {symbol.name}\n```\n\nGlobal variable defined at line {symbol.line}"
                ),
                range=range
            )

        elif symbol.kind == SymbolKind.SHARED:
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"```cssl\nshared {symbol.name}\n```\n\nShared variable"
                ),
                range=range
            )

        else:
            return Hover(
                contents=MarkupContent(
                    kind=MarkupKind.Markdown,
                    value=f"**{symbol.name}** ({kind_name})\n\nDefined at line {symbol.line}"
                ),
                range=range
            )

    def _hover_pointer_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for pointer reference (?var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        # Try to find the referenced variable
        if document.symbol_table:
            symbol = document.symbol_table.get_symbol(var_name)
            if symbol:
                type_info = symbol.type_info or "dynamic"
                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"**Pointer Reference**\n\n```cssl\n?{var_name}  // pointer to {type_info} {var_name}\n```\n\nReferences variable `{var_name}` defined at line {symbol.line}"
                    ),
                    range=word_range
                )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Pointer Reference**\n\n`?{var_name}` - pointer to variable `{var_name}`\n\n⚠️ Variable `{var_name}` not found"
            ),
            range=word_range
        )

    def _hover_global_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for global reference (@var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Global Reference**\n\n`@{var_name}` - reference to global variable `{var_name}`"
            ),
            range=word_range
        )

    def _hover_shared_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for shared reference ($var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Shared Reference**\n\n`${var_name}` - reference to shared variable `{var_name}`\n\nShared variables are accessible across modules."
            ),
            range=word_range
        )

    def _hover_snapshot_reference(
        self,
        document: DocumentAnalysis,
        var_name: str,
        line: int,
        start_col: int,
        end_col: int
    ) -> Hover:
        """Format hover for snapshot reference (%var)."""
        word_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=end_col)
        )

        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=f"**Snapshot Reference**\n\n`%{var_name}` - reference to snapshot of `{var_name}`\n\nAccess the value from when `snapshot({var_name})` was called."
            ),
            range=word_range
        )
