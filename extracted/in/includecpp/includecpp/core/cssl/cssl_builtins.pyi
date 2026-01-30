"""
CSSL Built-in Functions - Complete Type Stubs & Documentation
==============================================================

This file provides comprehensive type hints and documentation for all CSSL
built-in functions, data types, and container types. All are available in
CSSL scripts without imports.

Total: 200+ functions + 9 container classes + 10 data types across 20 categories.

Categories:
    - Output Functions (7)
    - Type Conversion (6)
    - Type Checking (9)
    - String Operations (30)
    - Array/List Operations (25)
    - Dictionary Operations (15)
    - Math Functions (28)
    - Date/Time Functions (8)
    - File System Functions (23)
    - JSON Functions (12) - json:: namespace
    - Instance Introspection (9) - instance:: namespace
    - Regex Functions (4)
    - Hash Functions (3)
    - System/Control Functions (18)
    - Platform Detection (3)
    - Container Classes (9) - stack<T>, vector<T>, array<T>, map<K,V>, etc.
    - Function Keywords (10)
    - Classes & OOP
    - Data Types (10) - int, float, string, bool, dynamic, var, list, dict, void, null
    - Special Syntax Reference

Container Types with Methods (use lowercase names for quick lookup):
    - stack: stack<T> - LIFO with push(), pop(), peek(), etc.
    - vector: vector<T> - Dynamic array with at(), front(), back(), etc.
    - array: array<T> - Standard array with similar methods
    - map: map<K,V> - Ordered key-value with insert(), find(), erase(), etc.
    - datastruct: datastruct<T> - Universal container for BruteInjection
    - iterator: iterator<T> - Programmable with insert(), fill(), at()
    - shuffled: shuffled<T> - Multi-value returns
    - combo: combo<T> - Filter/search space
    - dataspace: dataspace<T> - SQL-like data storage

Type "vector." to see all available methods with documentation.

Data Types (use type aliases for quick lookup):
    - int_t: int - whole numbers
    - float_t: float - decimal numbers
    - string_t: string - text with interpolation
    - bool_t: bool - true/false values
    - dynamic_t: dynamic - any type (auto-typed)
    - var_t: var - type inference
    - list_t: list - ordered collection
    - dict_t: dict - key-value pairs
    - void_t: void - no return value
    - null_t: null/None - absence of value

Type "int_t" or "DataTypes." to see data type documentation.

Usage from Python:
    from includecpp import CSSL

    CSSL.run('''
        stack<string> names;
        names.push("Alice");
        names.push("Bob");
        printl(names.pop());  // "Bob"
    ''')
"""

from typing import Any, List, Dict, Optional, Callable, Union, Tuple, TypeVar

T = TypeVar('T')

# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def print(*args: Any, sep: str = " ", end: str = "") -> None:
    """Print values without trailing newline.

    Outputs text to the console without automatically adding a newline at the end.
    Multiple arguments are joined with the separator.

    Args:
        *args: Values to print (any type, automatically converted to string)
        sep: Separator between values (default: single space)
        end: String appended after output (default: empty string)

    Example:
        print("Loading");
        print(".");
        print(".");
        printl("Done!");
        // Output: Loading...Done!

        print("A", "B", "C", sep="-");
        // Output: A-B-C
    """
    ...

def printl(*args: Any, sep: str = " ") -> None:
    """Print values with trailing newline (primary CSSL output function).

    The most commonly used output function in CSSL. Prints values followed
    by a newline character. Automatically converts all types to strings.

    Args:
        *args: Values to print (any type)
        sep: Separator between multiple values (default: space)

    Example:
        printl("Hello World");
        // Output: Hello World

        string name = "Alice";
        int age = 30;
        printl("Name:", name, "Age:", age);
        // Output: Name: Alice Age: 30

        // String concatenation also works:
        printl("Value: " + 42);  // Auto-conversion
        // Output: Value: 42
    """
    ...

def println(*args: Any, sep: str = " ") -> None:
    """Alias for printl(). Print values with newline."""
    ...

def debug(*args: Any) -> None:
    """Print debug information with [DEBUG] prefix.

    Useful for development and troubleshooting. Output is prefixed
    with [DEBUG] to distinguish from regular output.

    Args:
        *args: Debug values to display

    Example:
        int x = 42;
        debug("Variable x =", x);
        // Output: [DEBUG] Variable x = 42

        debug("Entering function processData()");
        debug("items.length =", len(items));
    """
    ...

def error(*args: Any) -> None:
    """Print error message with [ERROR] prefix.

    Used for reporting errors. Output is prefixed with [ERROR].
    Does NOT throw an exception - just prints the message.

    Args:
        *args: Error message components

    Example:
        error("File not found:", path);
        // Output: [ERROR] File not found: /path/to/file.txt

        if (!pathexists(file)) {
            error("Cannot read file:", file);
        }
    """
    ...

def warn(*args: Any) -> None:
    """Print warning message with [WARN] prefix.

    Used for non-critical issues that should be noted.
    Output is prefixed with [WARN].

    Args:
        *args: Warning message components

    Example:
        warn("Configuration file missing, using defaults");
        // Output: [WARN] Configuration file missing, using defaults
    """
    ...

def log(level: str, *args: Any) -> None:
    """Print message with custom log level prefix.

    Args:
        level: Log level string (e.g., "INFO", "TRACE", "VERBOSE")
        *args: Message components

    Example:
        log("INFO", "Server started on port", 8080);
        // Output: [INFO] Server started on port 8080
    """
    ...

# =============================================================================
# TYPE CONVERSION FUNCTIONS
# =============================================================================

def int(value: Any, base: int = 10) -> int:
    """Convert value to integer.

    Converts strings, floats, or booleans to integer representation.
    For strings, optionally specify the numeric base.

    Args:
        value: Value to convert (string, float, bool)
        base: Numeric base for string conversion (default: 10)

    Returns:
        Integer representation of the value

    Example:
        int("42");        // 42
        int(3.14);        // 3 (truncated, not rounded)
        int(3.9);         // 3
        int(true);        // 1
        int(false);       // 0
        int("ff", 16);    // 255 (hexadecimal)
        int("1010", 2);   // 10 (binary)
    """
    ...

def float(value: Any) -> float:
    """Convert value to floating-point number.

    Args:
        value: Value to convert (string, int, bool)

    Returns:
        Float representation of the value

    Example:
        float("3.14");    // 3.14
        float(42);        // 42.0
        float("1e-5");    // 0.00001 (scientific notation)
        float(true);      // 1.0
    """
    ...

def str(value: Any) -> str:
    """Convert value to string representation.

    Args:
        value: Any value to convert

    Returns:
        String representation

    Example:
        str(42);          // "42"
        str(3.14);        // "3.14"
        str(true);        // "True"
        str([1, 2, 3]);   // "[1, 2, 3]"
    """
    ...

def bool(value: Any) -> bool:
    """Convert value to boolean.

    Conversion rules:
    - Empty string "", "0", "false", "no", "null", "none" -> false
    - Any other non-empty string -> true
    - 0 -> false, any other number -> true
    - Empty list/dict -> false, non-empty -> true
    - null/None -> false

    Args:
        value: Value to convert

    Returns:
        Boolean representation

    Example:
        bool(1);          // true
        bool(0);          // false
        bool("");         // false
        bool("text");     // true
        bool("false");    // false (special case)
        bool([]);         // false
        bool([1, 2]);     // true
    """
    ...

def list(value: Any = None) -> List[Any]:
    """Convert value to list or create empty list.

    Args:
        value: Optional value to convert (string splits to chars,
               dict converts to list of tuples)

    Returns:
        List representation

    Example:
        list();               // []
        list("abc");          // ["a", "b", "c"]
        list((1, 2, 3));      // [1, 2, 3]
        list({"a": 1});       // [("a", 1)]
    """
    ...

def dict(value: Any = None) -> Dict[str, Any]:
    """Convert value to dictionary or create empty dict.

    Args:
        value: Optional value to convert (list of tuples)

    Returns:
        Dictionary representation

    Example:
        dict();                       // {}
        dict([("a", 1), ("b", 2)]);  // {"a": 1, "b": 2}
    """
    ...

# =============================================================================
# TYPE CHECKING FUNCTIONS
# =============================================================================

def typeof(value: Any) -> str:
    """Get the type name of a value as string.

    Args:
        value: Value to check

    Returns:
        Type name: "int", "float", "str", "bool", "list", "dict", "null"

    Example:
        typeof(42);           // "int"
        typeof(3.14);         // "float"
        typeof("hello");      // "str"
        typeof(true);         // "bool"
        typeof([1, 2, 3]);    // "list"
        typeof({"a": 1});     // "dict"
        typeof(null);         // "null"
    """
    ...

def memory(value: Any) -> dict:
    """Get memory/introspection info about a value (v4.8.9).

    Args:
        value: Any CSSL value (variable, function, class instance, etc.)

    Returns:
        Dictionary with keys:
            - address: Memory address as hex string
            - type: Type name string
            - repr: Python repr() string
            - value: Actual value for simple types
            - methods: List of method names
            - attributes: Dict of non-callable attributes
            - class_name: For CSSL instances, the class name
            - members: For CSSL instances, dict of member values

    Example:
        data = memory(myClass);
        printl(data.get("address"));    // "0x7f..."
        printl(data.get("type"));       // "MyClass"
        printl(data.get("methods"));    // ["method1", "method2"]

        // Copy the info
        info = memory(func).copy();

        // Get specific field
        addr = memory(obj).get("address");
    """
    ...


def address(value: Any) -> 'CSSLAddress':
    """Get memory address of an object as an Address type (v4.9.0).

    Shortcut for memory(obj).get("address") that returns an Address object
    which can be used with reflect() to get the object back.

    Args:
        value: Any CSSL value

    Returns:
        Address object pointing to the value

    Example:
        string text = "Hello";
        address addr = address(text);

        // Later, in another function:
        obj = addr.reflect();
        printl(obj);  // "Hello"

        // Or use the builtin
        obj = reflect(addr);
    """
    ...


def reflect(addr: Any) -> Any:
    """Reflect an address to get the original object (v4.9.0).

    Takes an Address object or address string and returns the object at that address.

    Args:
        addr: Address object or address string (hex)

    Returns:
        The object at that address, or None if not found

    Example:
        string text = "Hello";
        address addr = address(text);

        // Reflect to get object back
        obj = reflect(addr);
        printl(obj);  // "Hello"

        // Also works with address strings from memory()
        data = memory(text);
        obj = reflect(data.get("address"));
    """
    ...


def destroy(target: Any) -> bool:
    """Destroy an object and free its memory (v4.9.2).

    Clears the contents of containers, removes objects from the address registry,
    and helps garbage collection by nullifying references.

    Args:
        target: Object to destroy (can be Address, container, or any object)

    Returns:
        True if destruction was successful, False otherwise

    Example:
        list data = [1, 2, 3, 4, 5];
        printl(len(data));  // 5
        destroy(data);
        printl(len(data));  // 0

        // Works with addresses
        ptr addr = address(someVar);
        destroy(addr);  // Removes from address registry
    """
    ...


def execute(code: str, context: dict = None) -> Any:
    """Execute CSSL code string inline (v4.9.2).

    Parses and executes CSSL code from a string. Useful for dynamic code
    execution, metaprogramming, and runtime code generation.

    Args:
        code: CSSL code string to execute
        context: Optional dict of variables to inject into scope

    Returns:
        The result of the last expression or explicit return value.
        Returns dict with 'error' key if execution fails.

    Example:
        // Simple execution
        execute("x = 5; y = x * 2;");
        printl(y);  // 10

        // Get return value
        result = execute("return 5 + 3;");
        printl(result);  // 8

        // With context
        execute("printl(greeting + name);", {"greeting": "Hello, ", "name": "World"});
    """
    ...


def isinstance(value: Any, type_name: str) -> bool:
    """Check if value is instance of specified type.

    Args:
        value: Value to check
        type_name: Type name string ("int", "float", "str", "bool",
                   "list", "dict", "null")

    Returns:
        True if value matches the type

    Example:
        isinstance(42, "int");           // true
        isinstance("hello", "str");      // true
        isinstance([1, 2], "list");      // true
        isinstance(null, "null");        // true
    """
    ...

def isint(value: Any) -> bool:
    """Check if value is an integer.

    Note: Returns false for booleans even though bool is subclass of int.

    Example:
        isint(42);       // true
        isint(3.14);     // false
        isint("42");     // false
        isint(true);     // false
    """
    ...

def isfloat(value: Any) -> bool:
    """Check if value is a floating-point number.

    Example:
        isfloat(3.14);   // true
        isfloat(42);     // false
        isfloat(42.0);   // true
    """
    ...

def isstr(value: Any) -> bool:
    """Check if value is a string.

    Example:
        isstr("hello");  // true
        isstr(42);       // false
        isstr("");       // true
    """
    ...

def isbool(value: Any) -> bool:
    """Check if value is a boolean.

    Example:
        isbool(true);    // true
        isbool(false);   // true
        isbool(1);       // false
        isbool("true");  // false
    """
    ...

def islist(value: Any) -> bool:
    """Check if value is a list/array.

    Example:
        islist([1, 2, 3]);   // true
        islist("abc");       // false
        islist([]);          // true
    """
    ...

def isdict(value: Any) -> bool:
    """Check if value is a dictionary.

    Example:
        isdict({"a": 1});    // true
        isdict([]);          // false
    """
    ...

def isnull(value: Any) -> bool:
    """Check if value is null/None.

    Example:
        isnull(null);        // true
        isnull(None);        // true
        isnull("");          // false
        isnull(0);           // false
    """
    ...

# =============================================================================
# STRING OPERATIONS
# =============================================================================

def len(value: Union[str, List, Dict]) -> int:
    """Get length of string, list, or dictionary.

    Args:
        value: String (returns character count), list (element count),
               or dictionary (key count)

    Returns:
        Number of items

    Example:
        len("hello");         // 5
        len([1, 2, 3]);       // 3
        len({"a": 1, "b": 2}); // 2
        len("");              // 0
    """
    ...

def upper(s: str) -> str:
    """Convert string to uppercase.

    Example:
        upper("hello");       // "HELLO"
        upper("Hello World"); // "HELLO WORLD"
    """
    ...

def lower(s: str) -> str:
    """Convert string to lowercase.

    Example:
        lower("HELLO");       // "hello"
        lower("Hello World"); // "hello world"
    """
    ...

def trim(s: str, chars: str = None) -> str:
    """Remove whitespace (or specified chars) from both ends.

    Args:
        s: String to trim
        chars: Optional specific characters to remove

    Example:
        trim("  hello  ");         // "hello"
        trim("...hello...", "."); // "hello"
        trim("\\n\\thello\\n");    // "hello"
    """
    ...

def ltrim(s: str, chars: str = None) -> str:
    """Remove whitespace (or specified chars) from left side only.

    Example:
        ltrim("  hello  ");   // "hello  "
    """
    ...

def rtrim(s: str, chars: str = None) -> str:
    """Remove whitespace (or specified chars) from right side only.

    Example:
        rtrim("  hello  ");   // "  hello"
    """
    ...

def split(s: str, delimiter: str = None, maxsplit: int = -1) -> List[str]:
    """Split string into list by delimiter.

    Args:
        s: String to split
        delimiter: Split character/string (default: whitespace)
        maxsplit: Maximum number of splits (-1 for unlimited)

    Returns:
        List of substrings

    Example:
        split("a,b,c", ",");          // ["a", "b", "c"]
        split("hello world");          // ["hello", "world"]
        split("a-b-c-d", "-", 2);     // ["a", "b", "c-d"]
    """
    ...

def join(delimiter: str, items: List[str]) -> str:
    """Join list elements into string with delimiter.

    Args:
        delimiter: String to place between elements
        items: List of strings to join

    Returns:
        Joined string

    Example:
        join("-", ["a", "b", "c"]);   // "a-b-c"
        join(", ", ["Alice", "Bob"]); // "Alice, Bob"
        join("", ["H", "i"]);         // "Hi"
    """
    ...

def replace(s: str, old: str, new: str, count: int = -1) -> str:
    """Replace occurrences of substring.

    Args:
        s: Original string
        old: Substring to find
        new: Replacement string
        count: Max replacements (-1 for all)

    Example:
        replace("hello", "l", "x");       // "hexxo"
        replace("aaa", "a", "b", 2);      // "bba"
    """
    ...

def substr(s: str, start: int, length: int = None) -> str:
    """Extract substring by start position and length.

    Args:
        s: Original string
        start: Start index (0-based)
        length: Number of characters (optional, defaults to end)

    Example:
        substr("hello", 1, 3);    // "ell"
        substr("hello", 2);       // "llo"
        substr("hello", 0, 1);    // "h"
    """
    ...

def contains(s: str, substring: str) -> bool:
    """Check if string contains substring.

    Example:
        contains("hello world", "world");  // true
        contains("hello", "xyz");          // false
        contains("", "");                  // true
    """
    ...

def startswith(s: str, prefix: str) -> bool:
    """Check if string starts with prefix.

    Example:
        startswith("hello", "he");     // true
        startswith("hello", "lo");     // false
    """
    ...

def endswith(s: str, suffix: str) -> bool:
    """Check if string ends with suffix.

    Example:
        endswith("hello", "lo");       // true
        endswith("hello.txt", ".txt"); // true
    """
    ...

def format(template: str, *args: Any) -> str:
    """Format string with {} placeholders.

    Args:
        template: String with {} placeholders
        *args: Values to insert (in order)

    Example:
        format("Hello, {}!", "World");           // "Hello, World!"
        format("{} + {} = {}", 2, 3, 5);         // "2 + 3 = 5"
    """
    ...

def concat(*strings: str) -> str:
    """Concatenate multiple strings efficiently.

    More efficient than repeated + for many strings.

    Example:
        concat("a", "b", "c");     // "abc"
        concat("Hello", " ", "World"); // "Hello World"
    """
    ...

def repeat(s: str, count: int) -> str:
    """Repeat string n times.

    Example:
        repeat("ab", 3);          // "ababab"
        repeat("-", 10);          // "----------"
    """
    ...

def reverse(s: str) -> str:
    """Reverse string character order.

    Example:
        reverse("hello");         // "olleh"
        reverse("12345");         // "54321"
    """
    ...

def indexof(s: str, substring: str, start: int = 0) -> int:
    """Find first occurrence of substring.

    Args:
        s: String to search in
        substring: Substring to find
        start: Starting position for search (default: 0)

    Returns:
        Index of first occurrence, -1 if not found

    Example:
        indexof("hello", "l");        // 2
        indexof("hello", "l", 3);     // 3
        indexof("hello", "xyz");      // -1
    """
    ...

def lastindexof(s: str, substring: str) -> int:
    """Find last occurrence of substring.

    Returns:
        Index of last occurrence, -1 if not found

    Example:
        lastindexof("hello", "l");    // 3
        lastindexof("abcabc", "bc");  // 4
    """
    ...

def padleft(s: str, width: int, char: str = " ") -> str:
    """Pad string on left to specified width.

    Args:
        s: Original string
        width: Target width
        char: Padding character (default: space)

    Example:
        padleft("42", 5, "0");     // "00042"
        padleft("hi", 6);         // "    hi"
    """
    ...

def padright(s: str, width: int, char: str = " ") -> str:
    """Pad string on right to specified width.

    Example:
        padright("42", 5, "0");    // "42000"
        padright("hi", 6);        // "hi    "
    """
    ...

def capitalize(s: str) -> str:
    """Capitalize first character of string.

    Example:
        capitalize("hello");      // "Hello"
        capitalize("hELLO");      // "Hello"
    """
    ...

def title(s: str) -> str:
    """Capitalize first character of each word.

    Example:
        title("hello world");     // "Hello World"
        title("the quick fox");   // "The Quick Fox"
    """
    ...

def swapcase(s: str) -> str:
    """Swap uppercase and lowercase characters.

    Example:
        swapcase("Hello");        // "hELLO"
        swapcase("PyThOn");       // "pYtHoN"
    """
    ...

def center(s: str, width: int, fillchar: str = " ") -> str:
    """Center string within specified width.

    Example:
        center("hi", 10);         // "    hi    "
        center("hi", 10, "-");    // "----hi----"
    """
    ...

def zfill(s: str, width: int) -> str:
    """Pad numeric string with leading zeros.

    Example:
        zfill("42", 5);           // "00042"
        zfill("-42", 5);          // "-0042"
    """
    ...

def chars(s: str) -> List[str]:
    """Convert string to list of characters.

    Example:
        chars("hello");           // ["h", "e", "l", "l", "o"]
    """
    ...

def ord(c: str) -> int:
    """Get ASCII/Unicode code point of character.

    Example:
        ord("A");                 // 65
        ord("a");                 // 97
        ord("0");                 // 48
    """
    ...

def chr(n: int) -> str:
    """Convert ASCII/Unicode code point to character.

    Example:
        chr(65);                  // "A"
        chr(97);                  // "a"
        chr(8364);                // "€"
    """
    ...

def isalpha(s: str) -> bool:
    """Check if string contains only alphabetic characters."""
    ...

def isdigit(s: str) -> bool:
    """Check if string contains only digits."""
    ...

def isalnum(s: str) -> bool:
    """Check if string contains only alphanumeric characters."""
    ...

def isspace(s: str) -> bool:
    """Check if string contains only whitespace."""
    ...

def sprintf(fmt: str, *args: Any) -> str:
    """C-style format string with % placeholders.

    Example:
        sprintf("%s: %d", "Count", 42);   // "Count: 42"
        sprintf("%.2f", 3.14159);         // "3.14"
    """
    ...

# =============================================================================
# ARRAY/LIST OPERATIONS
# =============================================================================

def push(arr: List[Any], *values: Any) -> List[Any]:
    """Add one or more elements to end of array.

    Args:
        arr: Target array
        *values: Values to add

    Returns:
        Modified array

    Example:
        stack<int> nums = [1, 2];
        nums = push(nums, 3);        // [1, 2, 3]
        nums = push(nums, 4, 5);     // [1, 2, 3, 4, 5]
    """
    ...

def pop(arr: List[Any], index: int = -1) -> Any:
    """Remove and return element at index (default: last).

    Args:
        arr: Source array (modified in place)
        index: Index to remove (default: -1 for last element)

    Returns:
        Removed element

    Example:
        stack<int> nums = [1, 2, 3];
        int last = pop(nums);        // 3, nums is now [1, 2]
        int first = pop(nums, 0);    // 1, nums is now [2]
    """
    ...

def shift(arr: List[Any]) -> Any:
    """Remove and return first element.

    Example:
        stack<string> names = ["Alice", "Bob"];
        string first = shift(names);  // "Alice", names is ["Bob"]
    """
    ...

def unshift(arr: List[Any], *values: Any) -> List[Any]:
    """Add elements to beginning of array.

    Example:
        stack<int> nums = [3, 4];
        nums = unshift(nums, 1, 2);   // [1, 2, 3, 4]
    """
    ...

def slice(arr: List[Any], start: int, end: int = None) -> List[Any]:
    """Extract portion of array (does not modify original).

    Args:
        arr: Source array
        start: Start index (inclusive)
        end: End index (exclusive, optional)

    Returns:
        New array with extracted elements

    Example:
        slice([1, 2, 3, 4, 5], 1, 4);  // [2, 3, 4]
        slice([1, 2, 3, 4, 5], 2);     // [3, 4, 5]
        slice([1, 2, 3, 4, 5], -2);    // [4, 5]
    """
    ...

def sort(arr: List[Any], key: str = None) -> List[Any]:
    """Sort array in ascending order.

    Args:
        arr: Array to sort
        key: Optional key name for sorting dicts/objects

    Returns:
        Sorted array

    Example:
        sort([3, 1, 2]);              // [1, 2, 3]
        sort(["c", "a", "b"]);        // ["a", "b", "c"]

        // Sort objects by key
        stack<json> users = [{"name": "Bob"}, {"name": "Alice"}];
        sort(users, "name");          // [{name: "Alice"}, {name: "Bob"}]
    """
    ...

def rsort(arr: List[Any], key: str = None) -> List[Any]:
    """Sort array in descending order.

    Example:
        rsort([1, 3, 2]);             // [3, 2, 1]
    """
    ...

def unique(arr: List[Any]) -> List[Any]:
    """Remove duplicate elements (preserves first occurrence order).

    Example:
        unique([1, 2, 2, 3, 1]);      // [1, 2, 3]
        unique(["a", "b", "a"]);      // ["a", "b"]
    """
    ...

def flatten(arr: List[Any], depth: int = 1) -> List[Any]:
    """Flatten nested arrays to specified depth.

    Args:
        arr: Nested array
        depth: How many levels to flatten (default: 1)

    Example:
        flatten([[1, 2], [3, 4]]);           // [1, 2, 3, 4]
        flatten([[[1]], [[2]]]);             // [[1], [2]]
        flatten([[[1]], [[2]]], 2);          // [1, 2]
    """
    ...

def filter(arr: List[Any], predicate: Callable[[Any], bool]) -> List[Any]:
    """Filter array by predicate function.

    Note: In CSSL, use inline conditions or lambda-like syntax.

    Args:
        arr: Source array
        predicate: Function returning true for elements to keep

    Returns:
        Filtered array (only elements where predicate returned true)
    """
    ...

def map(arr: List[Any], func: Callable[[Any], Any]) -> List[Any]:
    """Apply transformation function to each element.

    Args:
        arr: Source array
        func: Transformation function

    Returns:
        Array of transformed elements
    """
    ...

def reduce(arr: List[Any], func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
    """Reduce array to single value using accumulator function.

    Args:
        arr: Source array
        func: Reducer (accumulator, current) -> result
        initial: Starting accumulator value

    Returns:
        Final accumulated value
    """
    ...

def find(arr: List[Any], predicate: Callable[[Any], bool]) -> Optional[Any]:
    """Find first element matching predicate.

    Returns:
        First matching element or null if none found
    """
    ...

def findindex(arr: List[Any], predicate: Callable[[Any], bool]) -> int:
    """Find index of first element matching predicate.

    Returns:
        Index of first match, -1 if not found
    """
    ...

def every(arr: List[Any], predicate: Callable[[Any], bool]) -> bool:
    """Check if ALL elements satisfy predicate.

    Returns:
        True if predicate returns true for all elements
    """
    ...

def some(arr: List[Any], predicate: Callable[[Any], bool]) -> bool:
    """Check if ANY element satisfies predicate.

    Returns:
        True if predicate returns true for at least one element
    """
    ...

def range(start_or_stop: int, stop: int = None, step: int = 1) -> List[int]:
    """Generate list of integers in range.

    Args:
        start_or_stop: If only arg, this is stop (start=0). Otherwise start.
        stop: End value (exclusive)
        step: Increment between values (default: 1)

    Returns:
        List of integers

    Example:
        range(5);               // [0, 1, 2, 3, 4]
        range(1, 5);            // [1, 2, 3, 4]
        range(0, 10, 2);        // [0, 2, 4, 6, 8]
        range(10, 0, -1);       // [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    """
    ...

def enumerate(arr: List[Any], start: int = 0) -> List[Tuple[int, Any]]:
    """Return list of (index, value) pairs.

    Args:
        arr: Array to enumerate
        start: Starting index number (default: 0)

    Example:
        enumerate(["a", "b", "c"]);      // [(0, "a"), (1, "b"), (2, "c")]
        enumerate(["a", "b"], 1);        // [(1, "a"), (2, "b")]
    """
    ...

def zip(*arrays: List[Any]) -> List[Tuple[Any, ...]]:
    """Combine multiple arrays into array of tuples.

    Example:
        zip([1, 2], ["a", "b"]);         // [(1, "a"), (2, "b")]
    """
    ...

def reversed(arr: List[Any]) -> List[Any]:
    """Return reversed copy of array.

    Example:
        reversed([1, 2, 3]);              // [3, 2, 1]
    """
    ...

def count(collection: Union[List, str], item: Any) -> int:
    """Count occurrences of item in list or string.

    Example:
        count([1, 2, 2, 3, 2], 2);        // 3
        count("hello", "l");              // 2
    """
    ...

def first(arr: List[Any], default: Any = None) -> Any:
    """Get first element or default if empty.

    Example:
        first([1, 2, 3]);                 // 1
        first([], "none");                // "none"
    """
    ...

def last(arr: List[Any], default: Any = None) -> Any:
    """Get last element or default if empty.

    Example:
        last([1, 2, 3]);                  // 3
        last([], "none");                 // "none"
    """
    ...

def take(arr: List[Any], n: int) -> List[Any]:
    """Take first n elements.

    Example:
        take([1, 2, 3, 4, 5], 3);         // [1, 2, 3]
    """
    ...

def drop(arr: List[Any], n: int) -> List[Any]:
    """Drop first n elements, return rest.

    Example:
        drop([1, 2, 3, 4, 5], 2);         // [3, 4, 5]
    """
    ...

def chunk(arr: List[Any], size: int) -> List[List[Any]]:
    """Split array into chunks of specified size.

    Example:
        chunk([1, 2, 3, 4, 5], 2);        // [[1, 2], [3, 4], [5]]
    """
    ...

def shuffle(arr: List[Any]) -> List[Any]:
    """Return randomly shuffled copy of array.

    Example:
        shuffle([1, 2, 3, 4]);            // [3, 1, 4, 2] (random)
    """
    ...

def sample(arr: List[Any], k: int) -> List[Any]:
    """Return k random elements from array (without replacement).

    Example:
        sample([1, 2, 3, 4, 5], 3);       // [2, 5, 1] (random 3 elements)
    """
    ...

# =============================================================================
# DICTIONARY OPERATIONS
# =============================================================================

def keys(d: Dict[str, Any]) -> List[str]:
    """Get all keys from dictionary.

    Example:
        keys({"a": 1, "b": 2});           // ["a", "b"]
    """
    ...

def values(d: Dict[str, Any]) -> List[Any]:
    """Get all values from dictionary.

    Example:
        values({"a": 1, "b": 2});          // [1, 2]
    """
    ...

def items(d: Dict[str, Any]) -> List[Tuple[str, Any]]:
    """Get all key-value pairs as list of tuples.

    Example:
        items({"a": 1, "b": 2});           // [("a", 1), ("b", 2)]
    """
    ...

def haskey(d: Dict[str, Any], key: str) -> bool:
    """Check if dictionary has key.

    Example:
        haskey({"a": 1}, "a");             // true
        haskey({"a": 1}, "b");             // false
    """
    ...

def getkey(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Get value by key with optional default.

    Args:
        d: Dictionary
        key: Key to look up
        default: Value to return if key not found

    Example:
        getkey({"a": 1}, "a", 0);          // 1
        getkey({"a": 1}, "b", 0);          // 0
        getkey({"a": 1}, "b");             // null
    """
    ...

def setkey(d: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    """Set key-value pair in dictionary (returns modified copy).

    Example:
        json obj = {"a": 1};
        obj = setkey(obj, "b", 2);        // {"a": 1, "b": 2}
    """
    ...

def delkey(d: Dict[str, Any], key: str) -> Dict[str, Any]:
    """Delete key from dictionary (returns modified copy).

    Example:
        json obj = {"a": 1, "b": 2};
        obj = delkey(obj, "a");           // {"b": 2}
    """
    ...

def merge(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries (later values override).

    Example:
        merge({"a": 1}, {"b": 2}, {"a": 3});  // {"a": 3, "b": 2}
    """
    ...

def update(d: Dict[str, Any], other: Dict[str, Any]) -> Dict[str, Any]:
    """Update dictionary with another (returns new dict).

    Example:
        update({"a": 1}, {"b": 2});        // {"a": 1, "b": 2}
    """
    ...

def fromkeys(keys: List[str], value: Any = None) -> Dict[str, Any]:
    """Create dictionary from list of keys with default value.

    Example:
        fromkeys(["a", "b", "c"], 0);      // {"a": 0, "b": 0, "c": 0}
    """
    ...

def invert(d: Dict[str, Any]) -> Dict[Any, str]:
    """Swap keys and values (values must be hashable).

    Example:
        invert({"a": 1, "b": 2});          // {1: "a", 2: "b"}
    """
    ...

def pick(d: Dict[str, Any], *keys: str) -> Dict[str, Any]:
    """Pick only specified keys from dictionary.

    Example:
        pick({"a": 1, "b": 2, "c": 3}, "a", "c");  // {"a": 1, "c": 3}
    """
    ...

def omit(d: Dict[str, Any], *keys: str) -> Dict[str, Any]:
    """Omit specified keys from dictionary.

    Example:
        omit({"a": 1, "b": 2, "c": 3}, "b");       // {"a": 1, "c": 3}
    """
    ...

def groupby(arr: List[Any], key: str) -> Dict[Any, List[Any]]:
    """Group list of dicts/objects by key value.

    Example:
        stack<json> users = [
            {"name": "Alice", "role": "admin"},
            {"name": "Bob", "role": "user"},
            {"name": "Carol", "role": "admin"}
        ];
        groupby(users, "role");
        // {"admin": [{Alice}, {Carol}], "user": [{Bob}]}
    """
    ...

# =============================================================================
# MATH FUNCTIONS
# =============================================================================

def abs(x: Union[int, float]) -> Union[int, float]:
    """Absolute value.

    Example:
        abs(-5);          // 5
        abs(3.14);        // 3.14
        abs(-3.14);       // 3.14
    """
    ...

def min(*values: Union[int, float, List]) -> Union[int, float]:
    """Minimum value from arguments or list.

    Example:
        min(3, 1, 2);             // 1
        min([3, 1, 2]);           // 1
    """
    ...

def max(*values: Union[int, float, List]) -> Union[int, float]:
    """Maximum value from arguments or list.

    Example:
        max(3, 1, 2);             // 3
        max([3, 1, 2]);           // 3
    """
    ...

def sum(arr: List[Union[int, float]], start: Union[int, float] = 0) -> Union[int, float]:
    """Sum of list elements.

    Args:
        arr: List of numbers
        start: Starting value to add to sum (default: 0)

    Example:
        sum([1, 2, 3, 4]);        // 10
        sum([1, 2, 3], 10);       // 16
    """
    ...

def avg(arr: List[Union[int, float]]) -> float:
    """Average (mean) of list elements.

    Example:
        avg([1, 2, 3, 4, 5]);     // 3.0
        avg([10, 20]);            // 15.0
    """
    ...

def round(x: float, decimals: int = 0) -> float:
    """Round to specified decimal places.

    Example:
        round(3.14159, 2);        // 3.14
        round(3.5);               // 4.0
        round(2.5);               // 2.0 (banker's rounding)
    """
    ...

def floor(x: float) -> int:
    """Round down to nearest integer.

    Example:
        floor(3.9);               // 3
        floor(3.1);               // 3
        floor(-3.1);              // -4
    """
    ...

def ceil(x: float) -> int:
    """Round up to nearest integer.

    Example:
        ceil(3.1);                // 4
        ceil(3.9);                // 4
        ceil(-3.9);               // -3
    """
    ...

def pow(base: float, exponent: float) -> float:
    """Raise base to power.

    Example:
        pow(2, 3);                // 8.0
        pow(9, 0.5);              // 3.0 (square root)
        pow(2, -1);               // 0.5
    """
    ...

def sqrt(x: float) -> float:
    """Square root.

    Example:
        sqrt(16);                 // 4.0
        sqrt(2);                  // 1.41421...
    """
    ...

def mod(a: int, b: int) -> int:
    """Modulo (remainder after division).

    Example:
        mod(7, 3);                // 1
        mod(10, 5);               // 0
    """
    ...

def random() -> float:
    """Random float between 0.0 (inclusive) and 1.0 (exclusive).

    Example:
        float r = random();       // 0.0 <= r < 1.0
    """
    ...

def randint(min_val: int, max_val: int) -> int:
    """Random integer in inclusive range [min, max].

    Example:
        randint(1, 6);            // 1, 2, 3, 4, 5, or 6
        randint(0, 100);          // 0 to 100 inclusive
    """
    ...

def sin(x: float) -> float:
    """Sine (argument in radians).

    Example:
        sin(0);                   // 0.0
        sin(pi() / 2);            // 1.0
    """
    ...

def cos(x: float) -> float:
    """Cosine (argument in radians).

    Example:
        cos(0);                   // 1.0
        cos(pi());                // -1.0
    """
    ...

def tan(x: float) -> float:
    """Tangent (argument in radians)."""
    ...

def asin(x: float) -> float:
    """Arc sine (result in radians)."""
    ...

def acos(x: float) -> float:
    """Arc cosine (result in radians)."""
    ...

def atan(x: float) -> float:
    """Arc tangent (result in radians)."""
    ...

def atan2(y: float, x: float) -> float:
    """Two-argument arc tangent (result in radians).

    Returns angle from positive x-axis to point (x, y).
    """
    ...

def log(x: float, base: float = None) -> float:
    """Logarithm. Natural log if base not specified.

    Example:
        log(e());                 // 1.0 (natural log)
        log(100, 10);             // 2.0 (log base 10)
        log(8, 2);                // 3.0 (log base 2)
    """
    ...

def log10(x: float) -> float:
    """Base-10 logarithm.

    Example:
        log10(100);               // 2.0
        log10(1000);              // 3.0
    """
    ...

def exp(x: float) -> float:
    """Exponential function (e^x).

    Example:
        exp(1);                   // 2.71828...
        exp(0);                   // 1.0
    """
    ...

def pi() -> float:
    """Mathematical constant pi (3.14159265358979...).

    Example:
        float circumference = 2 * pi() * radius;
    """
    ...

def e() -> float:
    """Mathematical constant e (2.71828182845904...).

    Example:
        float growth = e() ** rate;
    """
    ...

def radians(degrees: float) -> float:
    """Convert degrees to radians.

    Example:
        radians(180);             // 3.14159... (pi)
        radians(90);              // 1.5708... (pi/2)
    """
    ...

def degrees(radians: float) -> float:
    """Convert radians to degrees.

    Example:
        degrees(pi());            // 180.0
        degrees(pi() / 2);        // 90.0
    """
    ...

# =============================================================================
# DATE/TIME FUNCTIONS
# =============================================================================

def now() -> float:
    """Current timestamp as float (seconds since Unix epoch).

    Example:
        float ts = now();         // 1703956800.123456
    """
    ...

def timestamp() -> int:
    """Current timestamp as integer (seconds since Unix epoch).

    Example:
        int ts = timestamp();     // 1703956800
    """
    ...

def sleep(seconds: float) -> None:
    """Pause execution for specified seconds.

    Args:
        seconds: Duration to sleep (can be fractional)

    Example:
        sleep(1.5);               // Wait 1.5 seconds
        sleep(0.1);               // Wait 100 milliseconds
    """
    ...

def delay(ms: float) -> None:
    """Pause execution for specified milliseconds.

    Example:
        delay(500);               // Wait 500 milliseconds
        delay(1000);              // Wait 1 second
    """
    ...

def date(format: str = "%Y-%m-%d") -> str:
    """Current date as formatted string.

    Args:
        format: strftime format string

    Common format codes:
        %Y - 4-digit year
        %m - 2-digit month
        %d - 2-digit day
        %H - Hour (24-hour)
        %M - Minute
        %S - Second

    Example:
        date();                   // "2025-12-30"
        date("%d/%m/%Y");         // "30/12/2025"
        date("%Y%m%d");           // "20251230"
    """
    ...

def time(format: str = "%H:%M:%S") -> str:
    """Current time as formatted string.

    Example:
        time();                   // "14:30:45"
        time("%H:%M");            // "14:30"
        time("%I:%M %p");         // "02:30 PM"
    """
    ...

def datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Current date and time as formatted string.

    Example:
        datetime();               // "2025-12-30 14:30:45"
    """
    ...

def strftime(format: str, timestamp: float = None) -> str:
    """Format timestamp as string.

    Args:
        format: strftime format string
        timestamp: Unix timestamp (default: current time)

    Example:
        strftime("%Y-%m-%d", 0);  // "1970-01-01"
    """
    ...

# =============================================================================
# FILE SYSTEM FUNCTIONS
# =============================================================================

def read(path: str, encoding: str = "utf-8") -> str:
    """Read entire file content as string.

    Args:
        path: File path (absolute or relative)
        encoding: Character encoding (default: utf-8)

    Returns:
        File content as string

    Example:
        string content = read("config.txt");
        string data = read("/path/to/file.txt");
    """
    ...

def readline(line: int, path: str) -> str:
    """Read specific line from file (1-indexed).

    Args:
        line: Line number (1-based, first line is 1)
        path: File path

    Returns:
        Content of that line (without newline)

    Example:
        string line5 = readline(5, "file.txt");
        string first = readline(1, "config.ini");
    """
    ...

def write(path: str, content: str) -> int:
    """Write content to file (overwrites existing).

    Args:
        path: File path
        content: Content to write

    Returns:
        Number of characters written

    Example:
        write("output.txt", "Hello World");
        write("data.json", json::stringify(myData));
    """
    ...

def writeline(line: int, content: str, path: str) -> bool:
    """Write/replace specific line in file (1-indexed).

    Creates lines if file is shorter than specified line number.

    Args:
        line: Line number (1-based)
        content: New content for that line
        path: File path

    Returns:
        Success status

    Example:
        writeline(3, "New third line", "file.txt");
    """
    ...

def appendfile(path: str, content: str) -> int:
    """Append content to end of file.

    Returns:
        Number of characters written

    Example:
        appendfile("log.txt", "New log entry\\n");
    """
    ...

def readlines(path: str) -> List[str]:
    """Read all lines from file as list.

    Returns:
        List of lines (including newline characters)

    Example:
        stack<string> lines = readlines("file.txt");
        foreach (line in lines) {
            printl(trim(line));
        }
    """
    ...

def pathexists(path: str) -> bool:
    """Check if path exists (file or directory).

    Example:
        if (pathexists("config.json")) {
            json config = json::read("config.json");
        }
    """
    ...

def isfile(path: str) -> bool:
    """Check if path is a file (not directory).

    Example:
        if (isfile("data.txt")) {
            string content = read("data.txt");
        }
    """
    ...

def isdir(path: str) -> bool:
    """Check if path is a directory.

    Example:
        if (isdir("output")) {
            // Directory exists
        } else {
            makedirs("output");
        }
    """
    ...

def listdir(path: str = ".") -> List[str]:
    """List directory contents (file and folder names).

    Args:
        path: Directory path (default: current directory)

    Returns:
        List of file/folder names (not full paths)

    Example:
        stack<string> files = listdir("./data");
        foreach (f in files) {
            printl(f);
        }
    """
    ...

def makedirs(path: str) -> bool:
    """Create directory and all parent directories.

    Does not raise error if directory already exists.

    Example:
        makedirs("output/reports/2025");
    """
    ...

def removefile(path: str) -> bool:
    """Delete a file.

    Example:
        removefile("temp.txt");
    """
    ...

def removedir(path: str) -> bool:
    """Delete an empty directory.

    Note: Directory must be empty. Use with caution.

    Example:
        removedir("empty_folder");
    """
    ...

def copyfile(src: str, dst: str) -> str:
    """Copy file from source to destination.

    Returns:
        Destination path

    Example:
        copyfile("original.txt", "backup.txt");
    """
    ...

def movefile(src: str, dst: str) -> str:
    """Move or rename file.

    Returns:
        Destination path

    Example:
        movefile("old_name.txt", "new_name.txt");
        movefile("file.txt", "archive/file.txt");
    """
    ...

def filesize(path: str) -> int:
    """Get file size in bytes.

    Example:
        int size = filesize("large_file.zip");
        printl("Size: " + size + " bytes");
    """
    ...

def basename(path: str) -> str:
    """Get filename from path.

    Example:
        basename("/path/to/file.txt");    // "file.txt"
        basename("C:\\Users\\file.txt"); // "file.txt"
    """
    ...

def dirname(path: str) -> str:
    """Get directory from path.

    Example:
        dirname("/path/to/file.txt");     // "/path/to"
    """
    ...

def joinpath(*parts: str) -> str:
    """Join path components with correct separator.

    Example:
        joinpath("/path", "to", "file.txt");  // "/path/to/file.txt"
        joinpath("data", "output.csv");       // "data/output.csv"
    """
    ...

def abspath(path: str) -> str:
    """Get absolute path from relative path.

    Example:
        abspath("./file.txt");    // "/current/working/dir/file.txt"
    """
    ...

def normpath(path: str) -> str:
    """Normalize path (resolve .. and ., fix separators).

    Example:
        normpath("/path/to/../file.txt");  // "/path/file.txt"
    """
    ...

def splitpath(path: str) -> List[str]:
    """Split path into [directory, filename].

    Example:
        splitpath("/path/to/file.txt");   // ["/path/to", "file.txt"]
    """
    ...

# =============================================================================
# JSON FUNCTIONS (json:: namespace)
# =============================================================================

def json_read(path: str) -> Any:
    """Read and parse JSON file.

    Usage in CSSL: json::read("/path/to/file.json")

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON data (dict, list, or primitive)

    Example:
        json config = json::read("config.json");
        printl(config.name);
        printl(config.settings.theme);
    """
    ...

def json_write(path: str, data: Any, indent: int = 2) -> bool:
    """Write data to JSON file with formatting.

    Usage in CSSL: json::write("/path/to/file.json", data)

    Args:
        path: Output file path
        data: Data to serialize (dict, list, primitives)
        indent: Indentation spaces (default: 2)

    Returns:
        Success status

    Example:
        json data = {"name": "Alice", "age": 30};
        json::write("user.json", data);
    """
    ...

def json_parse(s: str) -> Any:
    """Parse JSON string to object.

    Usage in CSSL: json::parse('{"key": "value"}')

    Example:
        string jsonStr = '{"name": "Bob", "active": true}';
        json obj = json::parse(jsonStr);
        printl(obj.name);    // "Bob"
    """
    ...

def json_stringify(data: Any) -> str:
    """Convert object to JSON string (compact).

    Usage in CSSL: json::stringify(data)

    Example:
        json obj = {"a": 1, "b": [1, 2, 3]};
        string s = json::stringify(obj);
        // '{"a":1,"b":[1,2,3]}'
    """
    ...

def json_pretty(data: Any, indent: int = 2) -> str:
    """Convert object to formatted JSON string.

    Usage in CSSL: json::pretty(data)

    Example:
        string formatted = json::pretty(config);
        printl(formatted);
    """
    ...

def json_get(data: Any, path: str, default: Any = None) -> Any:
    """Get value by dot-path from nested structure.

    Usage in CSSL: json::get(data, "user.profile.name")

    Supports array indexing with numeric path segments.

    Args:
        data: JSON object/dict
        path: Dot-separated path (e.g., "user.address.city")
        default: Value if path not found

    Example:
        json data = {"user": {"name": "Alice", "tags": ["a", "b"]}};
        json::get(data, "user.name");         // "Alice"
        json::get(data, "user.tags.0");       // "a"
        json::get(data, "user.email", "N/A"); // "N/A"
    """
    ...

def json_set(data: Any, path: str, value: Any) -> Any:
    """Set value by dot-path in nested structure.

    Usage in CSSL: json::set(data, "user.name", "Bob")

    Creates intermediate objects if they don't exist.

    Returns:
        Modified data (new copy)

    Example:
        json data = {"user": {}};
        data = json::set(data, "user.name", "Alice");
        data = json::set(data, "user.profile.age", 30);
    """
    ...

def json_has(data: Any, path: str) -> bool:
    """Check if dot-path exists in structure.

    Usage in CSSL: json::has(data, "user.email")

    Example:
        if (json::has(config, "database.host")) {
            string host = json::get(config, "database.host");
        }
    """
    ...

def json_keys(data: Dict) -> List[str]:
    """Get all top-level keys from JSON object.

    Usage in CSSL: json::keys(data)

    Example:
        stack<string> k = json::keys(config);
        // ["name", "version", "settings"]
    """
    ...

def json_values(data: Dict) -> List[Any]:
    """Get all top-level values from JSON object.

    Usage in CSSL: json::values(data)
    """
    ...

def json_merge(*dicts: Dict) -> Dict:
    """Deep merge multiple JSON objects.

    Usage in CSSL: json::merge(obj1, obj2, obj3)

    Later objects override earlier ones. Nested objects are merged recursively.

    Example:
        json defaults = {"theme": "light", "lang": "en"};
        json user = {"theme": "dark"};
        json config = json::merge(defaults, user);
        // {"theme": "dark", "lang": "en"}
    """
    ...

# =============================================================================
# INSTANCE INTROSPECTION (instance:: namespace)
# =============================================================================

def instance_getMethods(obj: Any) -> List[str]:
    """Get all public method names from object/module.

    Usage in CSSL: instance::getMethods(@module)

    Returns list of callable method names (excludes private _ methods).

    Example:
        @tk = include("tkinter.cssl-mod");
        stack<string> methods = instance::getMethods(@tk);
        foreach (m in methods) {
            printl("Method: " + m);
        }
    """
    ...

def instance_getClasses(obj: Any) -> List[str]:
    """Get all class names from module.

    Usage in CSSL: instance::getClasses(@module)

    Example:
        stack<string> classes = instance::getClasses(@tk);
        // ["Tk", "Frame", "Button", "Label", ...]
    """
    ...

def instance_getVars(obj: Any) -> List[str]:
    """Get all public variable/attribute names (non-callable).

    Usage in CSSL: instance::getVars(@module)

    Example:
        stack<string> vars = instance::getVars(@config);
        // ["VERSION", "DEBUG", "API_URL", ...]
    """
    ...

def instance_getAll(obj: Any) -> Dict[str, List[str]]:
    """Get all attributes categorized by type.

    Usage in CSSL: instance::getAll(@module)

    Returns dict with keys: 'methods', 'classes', 'vars'

    Example:
        json all = instance::getAll(@module);
        printl("Methods: " + len(all.methods));
        printl("Classes: " + len(all.classes));
        printl("Variables: " + len(all.vars));
    """
    ...

def instance_call(obj: Any, method_name: str, *args: Any, **kwargs: Any) -> Any:
    """Dynamically call method on object by name.

    Usage in CSSL: instance::call(@module, "methodName", arg1, arg2)

    Example:
        // Instead of @module.process(data)
        result = instance::call(@module, "process", data);

        // Useful for dynamic method selection
        string action = "save";
        instance::call(@handler, action, document);
    """
    ...

def instance_has(obj: Any, name: str) -> bool:
    """Check if object has attribute (method or variable).

    Usage in CSSL: instance::has(@module, "methodName")

    Example:
        if (instance::has(@plugin, "initialize")) {
            instance::call(@plugin, "initialize");
        }
    """
    ...

def instance_type(obj: Any) -> str:
    """Get type name of object.

    Usage in CSSL: instance::type(@module)

    Example:
        string t = instance::type(@data);
        printl("Type: " + t);  // "dict", "list", "CSSLModule", etc.
    """
    ...

def isavailable(name_or_obj: Any) -> bool:
    """Check if shared instance exists.

    Can check by name string or by shared reference.

    Usage:
        isavailable("MyInstance")     // Check by name
        isavailable($MyInstance)      // Check if shared ref is not null
        instance::exists("Name")      // Alias

    Example:
        if (isavailable("DatabaseConnection")) {
            $DatabaseConnection.query("SELECT * FROM users");
        } else {
            error("Database not connected");
        }
    """
    ...

# =============================================================================
# FILTER REGISTRATION FUNCTIONS (filter:: namespace)
# =============================================================================
# Custom filters allow extending the BruteInjection system with user-defined
# filter types. Register filters that can then be used in injection syntax:
#   result <==[mytype::myhelper="value"] source;

def filter_register(filter_type: str, helper: str, callback: Callable[[Any, Any, Any], Any]) -> bool:
    """Register a custom filter.

    Usage in CSSL: filter::register("mytype", "helper", callback)

    Args:
        filter_type: The filter type name (e.g., "custom", "mytype")
        helper: The helper name (e.g., "where", "add") or "*" for catch-all
        callback: Function(source, filter_value, runtime) -> filtered_result

    Example:
        // Define a custom filter callback
        define addFilter(source, value, runtime) {
            return source + value;
        }

        // Register the filter
        filter::register("math", "add", addFilter);

        // Use the filter
        result <==[math::add=10] 5;  // result = 15

        // Register a catch-all filter
        define catchAll(source, value, runtime) {
            printl("Filter called with: " + str(value));
            return source;
        }
        filter::register("debug", "*", catchAll);
    """
    ...

def filter_unregister(filter_type: str, helper: str) -> bool:
    """Unregister a custom filter.

    Usage in CSSL: filter::unregister("mytype", "helper")

    Returns:
        True if filter was found and removed, False otherwise

    Example:
        filter::unregister("math", "add");
    """
    ...

def filter_list() -> List[str]:
    """List all registered custom filters.

    Usage in CSSL: filter::list()

    Returns:
        List of filter keys like ["math::add", "debug::*"]

    Example:
        stack<string> filters = filter::list();
        foreach (f in filters) {
            printl("Registered filter: " + f);
        }
    """
    ...

def filter_exists(filter_type: str, helper: str) -> bool:
    """Check if a custom filter exists.

    Usage in CSSL: filter::exists("mytype", "helper")

    Example:
        if (filter::exists("math", "add")) {
            result <==[math::add=5] 10;
        }
    """
    ...

# =============================================================================
# REGEX FUNCTIONS
# =============================================================================

def match(pattern: str, string: str) -> Optional[Dict]:
    """Match regex pattern at START of string.

    Args:
        pattern: Regular expression pattern
        string: String to match against

    Returns:
        Dict with 'match', 'groups', 'start', 'end' if matched, null otherwise

    Example:
        json m = match("\\d+", "123abc");
        if (m != null) {
            printl(m.match);   // "123"
            printl(m.start);   // 0
            printl(m.end);     // 3
        }
    """
    ...

def search(pattern: str, string: str) -> Optional[Dict]:
    """Search for regex pattern ANYWHERE in string.

    Returns:
        Dict with match info or null

    Example:
        json m = search("\\d+", "abc123def");
        printl(m.match);       // "123"
        printl(m.start);       // 3
    """
    ...

def findall(pattern: str, string: str) -> List[str]:
    """Find all non-overlapping matches of pattern.

    Returns:
        List of all matching strings

    Example:
        stack<string> nums = findall("\\d+", "a1b22c333");
        // ["1", "22", "333"]
    """
    ...

def sub(pattern: str, replacement: str, string: str, count: int = 0) -> str:
    """Replace regex matches with replacement string.

    Args:
        pattern: Regex pattern to find
        replacement: Replacement string
        string: Source string
        count: Max replacements (0 = unlimited)

    Example:
        sub("\\d+", "X", "a1b2c3");        // "aXbXcX"
        sub("\\d+", "X", "a1b2c3", 2);     // "aXbXc3"
    """
    ...

# =============================================================================
# HASH FUNCTIONS
# =============================================================================

def md5(s: str) -> str:
    """Calculate MD5 hash of string.

    Returns:
        32-character hexadecimal hash string

    Example:
        md5("hello");         // "5d41402abc4b2a76b9719d911017c592"
    """
    ...

def sha1(s: str) -> str:
    """Calculate SHA-1 hash of string.

    Returns:
        40-character hexadecimal hash string

    Example:
        sha1("hello");        // "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"
    """
    ...

def sha256(s: str) -> str:
    """Calculate SHA-256 hash of string.

    Returns:
        64-character hexadecimal hash string

    Example:
        sha256("hello");      // "2cf24dba5fb0a30e26e83b2ac5b9e29e..."
    """
    ...

# =============================================================================
# SYSTEM/CONTROL FUNCTIONS
# =============================================================================

def exit(code: int = 0) -> None:
    """Exit CSSL script execution.

    Can be intercepted with CodeInfusion for cleanup.

    Args:
        code: Exit code (0 = success, non-zero = error)

    Example:
        // Basic exit
        exit();
        exit(0);    // Success
        exit(1);    // Error

        // With cleanup via CodeInfusion
        exit() <<== {
            printl("Cleaning up...");
            // cleanup code
        }
    """
    ...

def input(prompt: str = "") -> str:
    """Read line of user input from console.

    Args:
        prompt: Optional prompt message to display

    Returns:
        User input string (without newline)

    Example:
        string name = input("Enter your name: ");
        printl("Hello, " + name);

        string answer = input("Continue? (y/n): ");
        if (answer == "y") {
            // continue
        }
    """
    ...

def env(name: str, default: str = None) -> Optional[str]:
    """Get environment variable value.

    Args:
        name: Environment variable name
        default: Default if not set

    Returns:
        Variable value or default/null

    Example:
        string home = env("HOME");
        string path = env("MY_APP_PATH", "/default/path");
    """
    ...

def setenv(name: str, value: str) -> None:
    """Set environment variable.

    Example:
        setenv("MY_VAR", "my_value");
    """
    ...

def clear() -> None:
    """Clear console screen.

    Example:
        clear();
        printl("Fresh screen!");
    """
    ...

def copy(obj: Any) -> Any:
    """Create shallow copy of object.

    For lists/dicts, creates new container but references same nested objects.

    Example:
        stack<int> original = [1, 2, 3];
        stack<int> copied = copy(original);
        copied.push(4);
        // original is still [1, 2, 3]
    """
    ...

def deepcopy(obj: Any) -> Any:
    """Create deep copy of object (recursively copies nested objects).

    Example:
        json original = {"nested": {"value": 1}};
        json copied = deepcopy(original);
        copied.nested.value = 2;
        printl(original.nested.value);  // Still 1
    """
    ...

def assert_condition(condition: bool, message: str = "Assertion failed") -> None:
    """Assert condition is true, raise error if false.

    Usage in CSSL: assert(condition, "message")

    Example:
        assert(x > 0, "x must be positive");
        assert(isstr(name), "name must be string");
    """
    ...

def pyimport(module_name: str) -> Any:
    """Import Python module for use in CSSL.

    Provides access to Python's standard library and installed packages.

    Args:
        module_name: Python module name

    Returns:
        Imported module object

    Example:
        @os = pyimport("os");
        string cwd = @os.getcwd();

        @re = pyimport("re");
        json match = @re.search("\\d+", "abc123");

        @datetime = pyimport("datetime");
        @datetime.datetime.now();
    """
    ...

def include(path: str) -> Any:
    """Import CSSL module or file.

    Supports .cssl files and .cssl-mod compiled modules.
    Returns module object with accessible functions and variables.

    Args:
        path: Path to module file

    Returns:
        Imported module object

    Example:
        // Import compiled Python module
        @Math = include("mathlib.cssl-mod");
        int result = @Math.add(5, 3);

        // Import CSSL file
        @Utils = include("utils.cssl");
        @Utils.formatDate(now());
    """
    ...

def payload(path_or_name: str) -> None:
    """Load CSSL payload file into current scope.

    Payloads are like headers - they define globals, functions, and
    can inject code into existing functions. All definitions become
    available in the current execution context.

    Supports:
    - File paths: "helpers.cssl-pl"
    - Registered names: payload registered via CSSL.code() in Python

    Args:
        path_or_name: Path to .cssl-pl file or registered payload name

    Example:
        // In helpers.cssl-pl:
        global DEBUG = true;
        void log(string msg) {
            if (@DEBUG) printl("[LOG] " + msg);
        }

        // In main.cssl:
        payload("helpers.cssl-pl");
        log("Hello!");    // Works - function from payload

        // From Python:
        CSSL.code("myhelper", "void greet() { printl('Hi'); }")
        CSSL.run('payload("myhelper"); greet();')
    """
    ...

def color(text: str, color_name: str) -> str:
    """Apply ANSI color to text for terminal output.

    Available colors:
        Basic: black, red, green, yellow, blue, magenta, cyan, white
        Bright: bright_black, bright_red, bright_green, etc.
        Styles: bold, dim, italic, underline, blink, reverse

    Example:
        printl(color("Error!", "red"));
        printl(color("Success", "green"));
        printl(color("Warning", "yellow"));
        printl(color("Important", "bold"));
    """
    ...

def original(func_name: str, *args: Any) -> Any:
    """Call the original version of a replaced function.

    Used within CodeInfusion to call the function that was replaced.

    Example:
        // Replace exit with custom behavior
        exit() <<== {
            printl("Custom cleanup...");
            original("exit");  // Call original exit
        }
    """
    ...

def delete(name: str) -> bool:
    """Delete a shared object by name.

    Removes object from shared instance registry.

    Args:
        name: Shared object name (without $ prefix)

    Returns:
        True if deleted, False if not found

    Example:
        // In Python: CSSL.share(myObj, "temp")
        // In CSSL:
        $temp.doSomething();
        delete("temp");  // Remove when done
        // $temp is now null
    """
    ...

def includecpp(cpp_proj: str, module: str) -> Any:
    """Import a pre-built C++ module from IncludeCPP project (v4.8.8).

    Loads compiled C++ modules directly into CSSL, enabling use of
    high-performance C++ functions from within CSSL scripts.

    Args:
        cpp_proj: Path to cpp.proj file or project directory
        module: Name of the compiled module to import

    Returns:
        Module proxy object with callable functions

    Example:
        // Import a compiled math module
        @FastMath = includecpp(
            cpp_proj="C:/Projects/QbbLibrary/cpp.proj",
            module="fastmath"
        );

        // Call C++ functions
        int result = @FastMath.fibonacci(40);
        printl("Fib(40) = " + result);

        // Import different module
        @Crypto = includecpp(cpp_proj="/path/to/crypto/cpp.proj", module="hashing");
        string hash = @Crypto.sha256("hello world");
    """
    ...

def snapshot(variable: Any, name: str = None) -> bool:
    """Capture variable state for later retrieval (v4.8.8).

    Creates a snapshot of the variable's current value that can be
    accessed using %name syntax even after the variable changes.

    Args:
        variable: Variable or function to snapshot
        name: Optional custom snapshot name (defaults to variable name)

    Returns:
        True if snapshot was created

    Example:
        string version = "1.0";
        snapshot(version);      // Capture current value

        version = "2.0";        // Modify
        printl(version);        // "2.0"
        printl(%version);       // "1.0" (snapshotted)

        // Named snapshot
        int counter = 100;
        snapshot(counter, "backup");
        counter = 500;
        printl(get_snapshot("backup"));  // 100

        // Snapshot functions for CodeInfusion
        snapshot(printl);
        embedded define override &printl {
            %printl("PREFIX: " + args[0]);  // Call original
        }
    """
    ...

def get_snapshot(name: str) -> Any:
    """Retrieve a snapshotted value by name.

    Example:
        snapshot(myVar, "saved");
        // ... later ...
        value = get_snapshot("saved");
    """
    ...

def has_snapshot(name: str) -> bool:
    """Check if a snapshot exists.

    Example:
        if (has_snapshot("backup")) {
            restore_snapshot("backup");
        }
    """
    ...

def clear_snapshot(name: str) -> bool:
    """Delete a specific snapshot.

    Example:
        clear_snapshot("temp");
    """
    ...

def clear_snapshots() -> int:
    """Delete all snapshots. Returns count deleted.

    Example:
        int removed = clear_snapshots();
        printl("Cleared " + removed + " snapshots");
    """
    ...

def list_snapshots() -> List[str]:
    """Get names of all active snapshots.

    Example:
        list names = list_snapshots();
        foreach (name in names) {
            printl("Snapshot: " + name);
        }
    """
    ...

def restore_snapshot(name: str) -> Any:
    """Restore and remove a snapshot (pop operation).

    Retrieves the snapshotted value and removes the snapshot.

    Example:
        myVar = restore_snapshot("backup");
    """
    ...

# =============================================================================
# PLATFORM DETECTION
# =============================================================================

def isLinux() -> bool:
    """Check if running on Linux operating system.

    Example:
        if (isLinux()) {
            string home = env("HOME");
        }
    """
    ...

def isWindows() -> bool:
    """Check if running on Windows operating system.

    Example:
        if (isWindows()) {
            string home = env("USERPROFILE");
        }
    """
    ...

def isMac() -> bool:
    """Check if running on macOS operating system.

    Example:
        if (isMac()) {
            printl("Running on Apple hardware");
        }
    """
    ...

# =============================================================================
# CSSL CONTAINER TYPES - Class-based with method documentation
# =============================================================================

class CSSLStack:
    """CSSL stack<T> container - LIFO (Last In, First Out) data structure.

    A stack is a collection where elements are added and removed from the same end
    (the "top"). The last element added is the first one removed.

    Declaration in CSSL:
        stack<string> names;
        stack<int> numbers;
        stack<dynamic> mixed;  // Can hold any type

    Example:
        stack<string> tasks;
        tasks.push("First task");
        tasks.push("Second task");
        tasks.push("Third task");

        printl(tasks);           // ['First task', 'Second task', 'Third task']
        printl(tasks.peek());    // "Third task" (view top without removing)
        printl(tasks.pop());     // "Third task" (removes and returns top)
        printl(tasks.length());  // 2
        printl(tasks[0]);        // "First task" (index access)
    """

    def push(self, value: T) -> 'CSSLStack':
        """Add element to top of stack.

        Args:
            value: Element to add

        Returns:
            The stack (for chaining)

        Example:
            stack<int> nums;
            nums.push(1).push(2).push(3);  // Chained calls
            printl(nums);  // [1, 2, 3]
        """
        ...

    def push_back(self, value: T) -> 'CSSLStack':
        """Alias for push(). Add element to top of stack."""
        ...

    def pop(self) -> T:
        """Remove and return top element.

        Returns:
            The removed element from top of stack

        Example:
            stack<string> names = ["Alice", "Bob", "Charlie"];
            string last = names.pop();  // "Charlie"
            printl(names);              // ["Alice", "Bob"]
        """
        ...

    def peek(self) -> T:
        """View top element without removing it.

        Returns:
            The top element (or None if empty)

        Example:
            stack<int> nums = [1, 2, 3];
            printl(nums.peek());  // 3
            printl(nums.peek());  // 3 (still there)
        """
        ...

    def isEmpty(self) -> bool:
        """Check if stack has no elements.

        Returns:
            True if stack is empty, False otherwise

        Example:
            stack<int> nums;
            printl(nums.isEmpty());  // true
            nums.push(1);
            printl(nums.isEmpty());  // false
        """
        ...

    def is_empty(self) -> bool:
        """Alias for isEmpty(). Check if stack is empty."""
        ...

    def size(self) -> int:
        """Get number of elements in stack.

        Returns:
            Number of elements

        Example:
            stack<string> names = ["A", "B", "C"];
            printl(names.size());  // 3
        """
        ...

    def length(self) -> int:
        """Alias for size(). Get number of elements."""
        ...

    def contains(self, value: T) -> bool:
        """Check if stack contains a specific value.

        Args:
            value: Value to search for

        Returns:
            True if found, False otherwise

        Example:
            stack<string> names = ["Alice", "Bob"];
            printl(names.contains("Alice"));  // true
            printl(names.contains("Carol"));  // false
        """
        ...

    def indexOf(self, value: T) -> int:
        """Find index of first occurrence of value.

        Args:
            value: Value to find

        Returns:
            Index (0-based), or -1 if not found

        Example:
            stack<string> names = ["A", "B", "C", "B"];
            printl(names.indexOf("B"));  // 1
            printl(names.indexOf("X"));  // -1
        """
        ...

    def toArray(self) -> List[T]:
        """Convert stack to plain array/list.

        Returns:
            List containing all stack elements

        Example:
            stack<int> nums = [1, 2, 3];
            array = nums.toArray();
            printl(array);  // [1, 2, 3]
        """
        ...

    def swap(self) -> 'CSSLStack':
        """Swap top two elements.

        Returns:
            The stack (for chaining)

        Example:
            stack<int> nums = [1, 2, 3];
            nums.swap();
            printl(nums);  // [1, 3, 2]
        """
        ...

    def dup(self) -> 'CSSLStack':
        """Duplicate top element.

        Returns:
            The stack (for chaining)

        Example:
            stack<int> nums = [1, 2, 3];
            nums.dup();
            printl(nums);  // [1, 2, 3, 3]
        """
        ...

    def begin(self) -> int:
        """Get iterator to first element (C++ style).

        Returns:
            Index 0
        """
        ...

    def end(self) -> int:
        """Get iterator past last element (C++ style).

        Returns:
            Length of stack
        """
        ...


class CSSLVector:
    """CSSL vector<T> container - Dynamic resizable array.

    A vector provides random access to elements by index and automatically
    grows as elements are added. Ideal for collections that need frequent
    access by position.

    Declaration in CSSL:
        vector<int> numbers;
        vector<string> names;
        vector<float> prices;

    Example:
        vector<int> nums;
        nums.push(10);
        nums.push(20);
        nums.push(30);

        printl(nums);         // [10, 20, 30]
        printl(nums.at(1));   // 20
        printl(nums.front()); // 10
        printl(nums.back());  // 30
        printl(nums.size());  // 3
    """

    def push(self, value: T) -> 'CSSLVector':
        """Add element to end of vector.

        Args:
            value: Element to add

        Returns:
            The vector (for chaining)

        Example:
            vector<string> items;
            items.push("A").push("B").push("C");
        """
        ...

    def push_back(self, value: T) -> 'CSSLVector':
        """Alias for push(). Add element to end."""
        ...

    def push_front(self, value: T) -> 'CSSLVector':
        """Add element to front of vector.

        Args:
            value: Element to add

        Returns:
            The vector (for chaining)

        Example:
            vector<int> nums = [2, 3];
            nums.push_front(1);
            printl(nums);  // [1, 2, 3]
        """
        ...

    def pop_back(self) -> T:
        """Remove and return last element.

        Returns:
            The removed element

        Example:
            vector<int> nums = [1, 2, 3];
            int last = nums.pop_back();  // 3
            printl(nums);                // [1, 2]
        """
        ...

    def pop_front(self) -> T:
        """Remove and return first element.

        Returns:
            The removed element

        Example:
            vector<int> nums = [1, 2, 3];
            int first = nums.pop_front();  // 1
            printl(nums);                  // [2, 3]
        """
        ...

    def at(self, index: int) -> T:
        """Get element at index.

        Args:
            index: Zero-based position

        Returns:
            Element at position (or None if out of bounds)

        Example:
            vector<string> names = ["Alice", "Bob", "Carol"];
            printl(names.at(1));  // "Bob"
        """
        ...

    def set(self, index: int, value: T) -> 'CSSLVector':
        """Set element at index.

        Args:
            index: Zero-based position
            value: New value

        Returns:
            The vector (for chaining)

        Example:
            vector<int> nums = [1, 2, 3];
            nums.set(1, 99);
            printl(nums);  // [1, 99, 3]
        """
        ...

    def size(self) -> int:
        """Get number of elements."""
        ...

    def length(self) -> int:
        """Alias for size()."""
        ...

    def empty(self) -> bool:
        """Check if vector is empty."""
        ...

    def isEmpty(self) -> bool:
        """Alias for empty()."""
        ...

    def front(self) -> T:
        """Get first element without removing.

        Example:
            vector<int> nums = [1, 2, 3];
            printl(nums.front());  // 1
        """
        ...

    def back(self) -> T:
        """Get last element without removing.

        Example:
            vector<int> nums = [1, 2, 3];
            printl(nums.back());  // 3
        """
        ...

    def contains(self, value: T) -> bool:
        """Check if vector contains value."""
        ...

    def indexOf(self, value: T) -> int:
        """Find first index of value (-1 if not found)."""
        ...

    def lastIndexOf(self, value: T) -> int:
        """Find last index of value (-1 if not found)."""
        ...

    def find(self, predicate: Callable[[T], bool]) -> T:
        """Find first element matching predicate.

        Args:
            predicate: Function returning True for match

        Returns:
            First matching element or None

        Example:
            vector<int> nums = [1, 5, 10, 15];
            int found = nums.find(x => x > 7);  // 10
        """
        ...

    def findIndex(self, predicate: Callable[[T], bool]) -> int:
        """Find index of first element matching predicate."""
        ...

    def slice(self, start: int, end: int = None) -> 'CSSLVector':
        """Get sub-vector from start to end.

        Args:
            start: Start index (inclusive)
            end: End index (exclusive), defaults to end

        Example:
            vector<int> nums = [1, 2, 3, 4, 5];
            vector<int> sub = nums.slice(1, 4);  // [2, 3, 4]
        """
        ...

    def join(self, separator: str = ",") -> str:
        """Join elements into string.

        Example:
            vector<string> words = ["hello", "world"];
            printl(words.join(" "));  // "hello world"
        """
        ...

    def map(self, func: Callable[[T], Any]) -> 'CSSLVector':
        """Apply function to each element, return new vector.

        Example:
            vector<int> nums = [1, 2, 3];
            vector<int> doubled = nums.map(x => x * 2);  // [2, 4, 6]
        """
        ...

    def filter(self, predicate: Callable[[T], bool]) -> 'CSSLVector':
        """Return new vector with elements matching predicate.

        Example:
            vector<int> nums = [1, 2, 3, 4, 5];
            vector<int> evens = nums.filter(x => x % 2 == 0);  // [2, 4]
        """
        ...

    def forEach(self, func: Callable[[T], None]) -> 'CSSLVector':
        """Execute function for each element.

        Example:
            vector<string> names = ["Alice", "Bob"];
            names.forEach(name => printl("Hello " + name));
        """
        ...

    def fill(self, value: T, start: int = 0, end: int = None) -> 'CSSLVector':
        """Fill range with value.

        Example:
            vector<int> nums = [1, 2, 3, 4, 5];
            nums.fill(0, 1, 4);
            printl(nums);  // [1, 0, 0, 0, 5]
        """
        ...

    def every(self, predicate: Callable[[T], bool]) -> bool:
        """Check if all elements match predicate.

        Example:
            vector<int> nums = [2, 4, 6];
            printl(nums.every(x => x % 2 == 0));  // true
        """
        ...

    def some(self, predicate: Callable[[T], bool]) -> bool:
        """Check if any element matches predicate.

        Example:
            vector<int> nums = [1, 2, 3];
            printl(nums.some(x => x > 2));  // true
        """
        ...

    def reduce(self, func: Callable[[Any, T], Any], initial: Any = None) -> Any:
        """Reduce vector to single value.

        Example:
            vector<int> nums = [1, 2, 3, 4];
            int sum = nums.reduce((acc, x) => acc + x, 0);  // 10
        """
        ...

    def toArray(self) -> List[T]:
        """Convert to plain list."""
        ...

    def begin(self) -> int:
        """Get iterator to first element (C++ style)."""
        ...

    def end(self) -> int:
        """Get iterator past last element (C++ style)."""
        ...


class CSSLArray:
    """CSSL array<T> container - Standard array with CSSL methods.

    Similar to vector but conceptually represents a fixed-purpose collection.
    Supports all standard array operations.

    Declaration in CSSL:
        array<string> items;
        array<int> scores;

    Example:
        array<string> colors;
        colors.push("red");
        colors.push("green");
        colors.push("blue");
        printl(colors.length());  // 3
        printl(colors.first());   // "red"
        printl(colors.last());    // "blue"
    """

    def push(self, value: T) -> 'CSSLArray':
        """Add element to end of array."""
        ...

    def push_back(self, value: T) -> 'CSSLArray':
        """Alias for push()."""
        ...

    def push_front(self, value: T) -> 'CSSLArray':
        """Add element to front of array."""
        ...

    def pop(self) -> T:
        """Remove and return last element."""
        ...

    def pop_back(self) -> T:
        """Alias for pop()."""
        ...

    def pop_front(self) -> T:
        """Remove and return first element."""
        ...

    def at(self, index: int) -> T:
        """Get element at index."""
        ...

    def set(self, index: int, value: T) -> 'CSSLArray':
        """Set element at index."""
        ...

    def size(self) -> int:
        """Get number of elements."""
        ...

    def length(self) -> int:
        """Alias for size()."""
        ...

    def empty(self) -> bool:
        """Check if array is empty."""
        ...

    def isEmpty(self) -> bool:
        """Alias for empty()."""
        ...

    def first(self) -> T:
        """Get first element."""
        ...

    def last(self) -> T:
        """Get last element."""
        ...

    def contains(self, value: T) -> bool:
        """Check if array contains value."""
        ...

    def indexOf(self, value: T) -> int:
        """Find first index of value."""
        ...

    def lastIndexOf(self, value: T) -> int:
        """Find last index of value."""
        ...

    def find(self, predicate: Callable[[T], bool]) -> T:
        """Find first element matching predicate."""
        ...

    def findIndex(self, predicate: Callable[[T], bool]) -> int:
        """Find index of first match."""
        ...

    def slice(self, start: int, end: int = None) -> 'CSSLArray':
        """Get sub-array from start to end."""
        ...

    def join(self, separator: str = ",") -> str:
        """Join elements into string."""
        ...

    def map(self, func: Callable[[T], Any]) -> 'CSSLArray':
        """Apply function to each element."""
        ...

    def filter(self, predicate: Callable[[T], bool]) -> 'CSSLArray':
        """Filter elements by predicate."""
        ...

    def forEach(self, func: Callable[[T], None]) -> 'CSSLArray':
        """Execute function for each element."""
        ...

    def fill(self, value: T, start: int = 0, end: int = None) -> 'CSSLArray':
        """Fill range with value."""
        ...

    def every(self, predicate: Callable[[T], bool]) -> bool:
        """Check if all elements match."""
        ...

    def some(self, predicate: Callable[[T], bool]) -> bool:
        """Check if any element matches."""
        ...

    def reduce(self, func: Callable[[Any, T], Any], initial: Any = None) -> Any:
        """Reduce to single value."""
        ...

    def toArray(self) -> List[T]:
        """Convert to plain list."""
        ...


class CSSLMap:
    """CSSL map<K, V> container - C++ style ordered key-value pairs.

    A map stores key-value pairs with keys maintained in sorted order.
    Provides efficient lookup, insertion, and deletion by key.

    Declaration in CSSL:
        map<string, int> ages;
        map<string, string> config;
        map<int, bool> flags;

    Example:
        map<string, int> ages;
        ages.insert("Alice", 30);
        ages.insert("Bob", 25);
        ages.insert("Carol", 28);

        printl(ages.find("Alice"));     // 30
        printl(ages.contains("Bob"));   // true
        printl(ages.size());            // 3

        ages.erase("Bob");
        printl(ages.size());            // 2
    """

    def insert(self, key: Any, value: Any) -> 'CSSLMap':
        """Insert or update key-value pair.

        Args:
            key: The key to insert
            value: The value to associate with the key

        Returns:
            The map (for chaining)

        Example:
            map<string, int> scores;
            scores.insert("Alice", 100);
            scores.insert("Bob", 95);
            scores.insert("Alice", 105);  // Updates Alice's score
            printl(scores.find("Alice")); // 105
        """
        ...

    def find(self, key: Any) -> Optional[Any]:
        """Find value by key.

        Args:
            key: The key to search for

        Returns:
            The value if found, None otherwise

        Example:
            map<string, int> ages;
            ages.insert("Alice", 30);
            printl(ages.find("Alice"));  // 30
            printl(ages.find("Bob"));    // null
        """
        ...

    def erase(self, key: Any) -> bool:
        """Remove key-value pair.

        Args:
            key: The key to remove

        Returns:
            True if key existed and was removed, False otherwise

        Example:
            map<string, int> data;
            data.insert("x", 1);
            bool removed = data.erase("x");  // true
            bool again = data.erase("x");    // false (already gone)
        """
        ...

    def contains(self, key: Any) -> bool:
        """Check if key exists.

        Args:
            key: The key to check

        Returns:
            True if key exists, False otherwise

        Example:
            map<string, int> ages;
            ages.insert("Alice", 30);
            printl(ages.contains("Alice"));  // true
            printl(ages.contains("Bob"));    // false
        """
        ...

    def count(self, key: Any) -> int:
        """Count occurrences of key (0 or 1 for map).

        Returns:
            1 if key exists, 0 otherwise
        """
        ...

    def size(self) -> int:
        """Get number of key-value pairs.

        Example:
            map<string, int> data;
            data.insert("a", 1);
            data.insert("b", 2);
            printl(data.size());  // 2
        """
        ...

    def empty(self) -> bool:
        """Check if map has no elements.

        Example:
            map<string, int> data;
            printl(data.empty());  // true
            data.insert("x", 1);
            printl(data.empty());  // false
        """
        ...

    def at(self, key: Any) -> Any:
        """Get value at key (throws if not found).

        Unlike find(), this throws an error if key doesn't exist.

        Args:
            key: The key to access

        Returns:
            The value at key

        Raises:
            KeyError if key not found

        Example:
            map<string, int> ages;
            ages.insert("Alice", 30);
            int age = ages.at("Alice");  // 30
            // ages.at("Bob");  // ERROR: Key not found
        """
        ...

    def begin(self) -> Tuple[Any, Any]:
        """Get first key-value pair (smallest key).

        Returns:
            Tuple of (key, value) or None if empty

        Example:
            map<string, int> data;
            data.insert("banana", 2);
            data.insert("apple", 1);
            data.insert("cherry", 3);
            tuple first = data.begin();  // ("apple", 1)
        """
        ...

    def end(self) -> Tuple[Any, Any]:
        """Get last key-value pair (largest key).

        Returns:
            Tuple of (key, value) or None if empty

        Example:
            map<string, int> data;
            data.insert("apple", 1);
            data.insert("cherry", 3);
            data.insert("banana", 2);
            tuple last = data.end();  // ("cherry", 3)
        """
        ...

    def lower_bound(self, key: Any) -> Optional[Any]:
        """Find first key >= given key.

        Useful for range queries on sorted keys.

        Args:
            key: The key to search from

        Returns:
            First key >= given key, or None if none found

        Example:
            map<int, string> data;
            data.insert(10, "ten");
            data.insert(20, "twenty");
            data.insert(30, "thirty");
            printl(data.lower_bound(15));  // 20
            printl(data.lower_bound(20));  // 20
        """
        ...

    def upper_bound(self, key: Any) -> Optional[Any]:
        """Find first key > given key.

        Args:
            key: The key to search from

        Returns:
            First key > given key, or None if none found

        Example:
            map<int, string> data;
            data.insert(10, "ten");
            data.insert(20, "twenty");
            data.insert(30, "thirty");
            printl(data.upper_bound(15));  // 20
            printl(data.upper_bound(20));  // 30
        """
        ...


class CSSLDataStruct:
    """CSSL datastruct<T> container - Universal flexible container.

    DataStruct is a lazy declarator that can hold any type of data.
    It's the primary target container for BruteInjection operations.

    Declaration in CSSL:
        datastruct<string> data;
        datastruct<int> numbers;
        datastruct<dynamic> anything;

    Usage with BruteInjection:
        stack<string> source = ["A", "B", "C"];
        datastruct<string> target;

        target +<== source;                         // Copy from source
        target +<== [string::contains="A"] source;  // Filtered copy

    Example:
        datastruct<string> names;
        names.add("Alice");
        names.add("Bob");
        printl(names.content());  // ["Alice", "Bob"]
    """

    def content(self) -> List[T]:
        """Get all elements as a list.

        Returns:
            List containing all elements

        Example:
            datastruct<int> data;
            data.add(1);
            data.add(2);
            printl(data.content());  // [1, 2]
        """
        ...

    def add(self, value: T) -> 'CSSLDataStruct':
        """Add an element to the datastruct.

        Args:
            value: Element to add

        Returns:
            The datastruct (for chaining)

        Example:
            datastruct<string> data;
            data.add("first").add("second");
        """
        ...

    def remove_where(self, predicate: Callable[[T], bool]) -> 'CSSLDataStruct':
        """Remove all elements matching predicate.

        Args:
            predicate: Function returning True for items to remove

        Returns:
            The datastruct (for chaining)

        Example:
            datastruct<int> nums;
            nums.add(1);
            nums.add(2);
            nums.add(3);
            nums.remove_where(x => x > 1);
            printl(nums.content());  // [1]
        """
        ...

    def find_where(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Find first element matching predicate.

        Args:
            predicate: Function returning True for match

        Returns:
            First matching element or None

        Example:
            datastruct<int> nums = [5, 10, 15];
            int found = nums.find_where(x => x > 7);  // 10
        """
        ...

    def convert(self, target_type: type) -> Any:
        """Convert first element to target type.

        Args:
            target_type: Type to convert to

        Returns:
            Converted value or None if empty
        """
        ...

    def begin(self) -> int:
        """Get iterator to first element (C++ style)."""
        ...

    def end(self) -> int:
        """Get iterator past last element (C++ style)."""
        ...


class CSSLIterator:
    """CSSL iterator<T, size> container - Advanced programmable iterator.

    Iterator provides positions within a data container with the ability
    to attach tasks (functions) to specific positions. Can be nested
    for multi-dimensional structures.

    Declaration in CSSL:
        iterator<int> it;
        iterator<int, 16> Map;              // 16 positions
        iterator<iterator<int, 16>> Map2D;  // 2D grid

    Example:
        // 2D grid example
        iterator<iterator<int, 16>> Map;
        Map.insert(3, 12);     // Set value 12 at position 3
        Map.fill(0);           // Fill all with 0
        int value = Map.at(3); // Get value at position 3
    """

    def insert(self, position: int, value: T) -> 'CSSLIterator':
        """Insert value at position.

        Args:
            position: Index position
            value: Value to insert

        Returns:
            The iterator (for chaining)

        Example:
            iterator<int> it;
            it.insert(0, 100);
            it.insert(1, 200);
        """
        ...

    def fill(self, value: T) -> 'CSSLIterator':
        """Fill all positions with value.

        Args:
            value: Value to fill with

        Returns:
            The iterator (for chaining)

        Example:
            iterator<int, 10> grid;
            grid.fill(0);  // All positions now 0
        """
        ...

    def at(self, position: int) -> T:
        """Get value at position.

        Args:
            position: Index position

        Returns:
            Value at position

        Example:
            iterator<int> it;
            it.insert(5, 42);
            printl(it.at(5));  // 42
        """
        ...

    def set(self, position: int, value: T) -> 'CSSLIterator':
        """Set value at iterator position.

        Args:
            position: Iterator index
            value: Value to set

        Returns:
            The iterator (for chaining)
        """
        ...

    def task(self, position: int, func: Callable) -> 'CSSLIterator':
        """Attach task (function) to iterator position.

        Args:
            position: Iterator index
            func: Function to attach

        Returns:
            The iterator (for chaining)

        Example:
            iterator<int> it;
            it.task(0, myHandler);  // Attach handler to position 0
        """
        ...


class CSSLShuffled:
    """CSSL shuffled<T> container - Multi-value return container.

    Shuffled is used with the 'shuffled' function keyword to enable
    functions to return multiple values. Values are unpacked using
    tuple assignment syntax.

    Declaration in CSSL:
        shuffled getValues() {
            return "Alice", 30, true;
        }

    Usage:
        shuffled string getNames() {
            return "first", "middle", "last";
        }

        // Unpack all values
        a, b, c = getNames();
        printl(a);  // "first"
        printl(b);  // "middle"
        printl(c);  // "last"

    Example with mixed types:
        shuffled getData() {
            return "name", 42, 3.14, true;
        }

        name, count, price, active = getData();
        printl(name);   // "name"
        printl(count);  // 42
        printl(price);  // 3.14
        printl(active); // true
    """
    pass


class CSSLCombo:
    """CSSL combo<T> container - Filter/search space for open parameters.

    Combo is used for creating filtered search spaces, often in
    conjunction with 'open' parameter functions.

    Declaration in CSSL:
        combo<string> searchSpace;
        combo<open&string> filter = combo<open&string>::like="pattern";

    Example:
        combo<string> names;
        names.add("Alice");
        names.add("Bob");
        names.add("Anna");

        // Use with filter pattern
        combo<open&string> filter = combo<open&string>::like="A*";
    """
    pass


class CSSLDataSpace:
    """CSSL dataspace<T> container - SQL-like data storage.

    DataSpace provides SQL-like operations for data manipulation.
    Used for complex data queries and transformations.

    Declaration in CSSL:
        dataspace<sql::table> table;

    Note: Advanced container for specialized data operations.
    """
    pass


def OpenFind(type_or_combo: Any, index: int = 0) -> Optional[Any]:
    """Find parameter by type from open parameters.

    Used inside functions declared with 'open' keyword to
    extract typed parameters from variadic argument list.

    Args:
        type_or_combo: The type to search for (e.g., string, int)
        index: Which occurrence to get (0 = first, 1 = second, etc.)

    Returns:
        The value at that index of that type, or None

    Usage in CSSL:
        open define flexibleFunc(open Params) {
            string name = OpenFind<string>(0);   // First string
            int num = OpenFind<int>(0);          // First int
            float val = OpenFind<float>(1);      // Second float

            printl("Name: " + name);
            printl("Number: " + num);
        }

        flexibleFunc("Hello", 42, 3.14, "World", 100);
        // name = "Hello" (first string)
        // num = 42 (first int)
        // val = (would need second float in args)
    """
    ...


# =============================================================================
# CONTAINER TYPE ALIASES (for direct lookup)
# =============================================================================
# These aliases allow looking up container methods directly by their CSSL name.
# Example: typing "stack." shows all stack methods with documentation.

stack = CSSLStack
"""stack<T> - LIFO (Last In, First Out) container.

Methods:
    .push(value)      Add element to top
    .pop()            Remove and return top element
    .peek()           View top without removing
    .isEmpty()        Check if empty
    .size()           Get element count
    .length()         Alias for size()
    .contains(value)  Check if value exists
    .indexOf(value)   Find index of value
    .toArray()        Convert to plain list
    .swap()           Swap top two elements
    .dup()            Duplicate top element

Example:
    stack<string> names;
    names.push("Alice");
    names.push("Bob");
    printl(names.pop());   // "Bob"
    printl(names.peek());  // "Alice"
"""

vector = CSSLVector
"""vector<T> - Dynamic resizable array with random access.

Methods:
    .push(value)          Add to end
    .push_front(value)    Add to front
    .pop_back()           Remove last
    .pop_front()          Remove first
    .at(index)            Get element at index
    .set(index, value)    Set element at index
    .front()              Get first element
    .back()               Get last element
    .size()               Get element count
    .contains(value)      Check if value exists
    .indexOf(value)       Find index of value
    .slice(start, end)    Get sub-vector
    .join(separator)      Join to string
    .map(func)            Transform elements
    .filter(predicate)    Filter elements
    .forEach(func)        Execute for each
    .every(predicate)     Check all match
    .some(predicate)      Check any match
    .reduce(func, init)   Reduce to single value

Example:
    vector<int> nums;
    nums.push(10).push(20).push(30);
    printl(nums.at(1));     // 20
    printl(nums.front());   // 10
    printl(nums.back());    // 30
"""

array = CSSLArray
"""array<T> - Standard array with CSSL methods.

Methods:
    .push(value)          Add to end
    .pop()                Remove last
    .at(index)            Get element at index
    .set(index, value)    Set element at index
    .first()              Get first element
    .last()               Get last element
    .size()               Get element count
    .length()             Alias for size()
    .contains(value)      Check if value exists
    .indexOf(value)       Find index of value
    .slice(start, end)    Get sub-array
    .join(separator)      Join to string
    .map(func)            Transform elements
    .filter(predicate)    Filter elements

Example:
    array<string> colors;
    colors.push("red");
    colors.push("green");
    printl(colors.first());   // "red"
    printl(colors.length());  // 2
"""

map = CSSLMap
"""map<K, V> - C++ style ordered key-value container.

Methods:
    .insert(key, value)   Insert or update key-value pair
    .find(key)            Find value by key (returns None if not found)
    .erase(key)           Remove key-value pair
    .contains(key)        Check if key exists
    .at(key)              Get value (throws if not found)
    .size()               Get pair count
    .empty()              Check if empty
    .begin()              Get first (key, value) pair
    .end()                Get last (key, value) pair
    .lower_bound(key)     Find first key >= given key
    .upper_bound(key)     Find first key > given key

Example:
    map<string, int> ages;
    ages.insert("Alice", 30);
    ages.insert("Bob", 25);
    printl(ages.find("Alice"));     // 30
    printl(ages.contains("Bob"));   // true
    ages.erase("Bob");
"""

datastruct = CSSLDataStruct
"""datastruct<T> - Universal container for BruteInjection operations.

Methods:
    .content()            Get all elements as list
    .add(value)           Add element
    .remove_where(pred)   Remove matching elements
    .find_where(pred)     Find first matching element
    .begin()              Iterator to start
    .end()                Iterator to end

Usage with BruteInjection:
    stack<string> source = ["A", "B", "C"];
    datastruct<string> target;
    target +<== source;                         // Copy all
    target +<== [string::contains="A"] source;  // Filtered copy

Example:
    datastruct<string> data;
    data.add("Alice").add("Bob");
    printl(data.content());  // ["Alice", "Bob"]
"""

iterator = CSSLIterator
"""iterator<T, size> - Advanced programmable iterator container.

Methods:
    .insert(pos, value)   Insert value at position
    .fill(value)          Fill all positions with value
    .at(pos)              Get value at position
    .set(pos, value)      Set value at position
    .task(pos, func)      Attach function to position

Example (2D grid):
    iterator<iterator<int, 16>> Map;
    Map.insert(3, 12);     // Set value 12 at position 3
    Map.fill(0);           // Fill all with 0
    int value = Map.at(3); // Get value at position 3
"""

shuffled = CSSLShuffled
"""shuffled<T> - Container for multi-value returns.

Used with 'shuffled' function keyword to return multiple values.
Values are unpacked using tuple assignment syntax.

Example:
    shuffled string getNames() {
        return "first", "middle", "last";
    }

    a, b, c = getNames();
    printl(a);  // "first"
    printl(b);  // "middle"
    printl(c);  // "last"

    // Mixed types
    shuffled getData() {
        return "name", 42, true;
    }
    name, count, flag = getData();
"""

combo = CSSLCombo
"""combo<T> - Filter/search space for open parameters.

Example:
    combo<string> searchSpace;
    combo<open&string> filter = combo<open&string>::like="A*";
"""

dataspace = CSSLDataSpace
"""dataspace<T> - SQL-like data storage container.

Example:
    dataspace<sql::table> table;
"""


# =============================================================================
# v4.8.4: C++ I/O STREAMS & TYPES
# =============================================================================

class OutputStream:
    """C++ style output stream (cout, cerr, clog equivalent).

    Supports << operator for chained output.

    Example:
        cout() << "Hello" << " World" << endl();
        cerr() << "Error: " << errMsg << endl();
        cout() << setprecision(4) << 3.14159;  // "3.1416"
    """

    def write(self, data: Any) -> 'OutputStream':
        """Write data to stream (equivalent to << operator).

        Args:
            data: Data to write (string, number, or 'endl'/'flush')

        Returns:
            The stream for chaining

        Example:
            cout().write("Hello").write(" World").write(endl());
        """
        ...

    def flush(self) -> 'OutputStream':
        """Flush the buffer to output."""
        ...

    def setprecision(self, n: int) -> 'OutputStream':
        """Set floating point precision."""
        ...

    def setw(self, n: int) -> 'OutputStream':
        """Set field width for next output."""
        ...

    def setfill(self, c: str) -> 'OutputStream':
        """Set fill character."""
        ...

    def fixed(self) -> 'OutputStream':
        """Use fixed-point notation for floats."""
        ...

    def scientific(self) -> 'OutputStream':
        """Use scientific notation for floats."""
        ...

    def hex(self) -> 'OutputStream':
        """Use hexadecimal for integers."""
        ...

    def oct(self) -> 'OutputStream':
        """Use octal for integers."""
        ...

    def dec(self) -> 'OutputStream':
        """Use decimal for integers (default)."""
        ...


class InputStream:
    """C++ style input stream (cin equivalent).

    Supports >> operator for reading input.

    Example:
        @name = cin().read(str);
        @age = cin().read(int);
        @line = getline();
    """

    def read(self, target_type: type = str) -> Any:
        """Read next token from stream.

        Args:
            target_type: Type to convert to (int, float, str, bool)

        Returns:
            The read and converted value

        Example:
            @num = cin().read(int);
            @name = cin().read(str);
        """
        ...

    def getline(self) -> str:
        """Read entire line."""
        ...

    def get(self) -> str:
        """Read single character."""
        ...

    def peek(self) -> str:
        """Peek at next character without consuming."""
        ...

    def eof(self) -> bool:
        """Check if end of stream."""
        ...

    def fail(self) -> bool:
        """Check if stream is in fail state."""
        ...

    def good(self) -> bool:
        """Check if stream is good."""
        ...

    def clear(self) -> 'InputStream':
        """Clear error flags."""
        ...


class FileStream:
    """C++ style file stream (fstream, ifstream, ofstream equivalent).

    Fast file I/O with << and >> operator support.

    Example:
        @file = fstream("data.txt", "r+");
        file << "Hello" << endl();
        @data = file.read(str);
        file.close();
    """

    def __init__(self, filename: str = None, mode: str = 'r'):
        """Create a file stream.

        Args:
            filename: Path to file
            mode: Open mode ('r', 'w', 'a', 'r+', etc.)
        """
        ...

    def open(self, filename: str, mode: str = 'r') -> 'FileStream':
        """Open a file."""
        ...

    def close(self) -> 'FileStream':
        """Close the file."""
        ...

    def is_open(self) -> bool:
        """Check if file is open."""
        ...

    def read(self, target_type: type = str) -> Any:
        """Read next token from file."""
        ...

    def write(self, data: Any) -> 'FileStream':
        """Write data to file."""
        ...

    def getline(self) -> str:
        """Read entire line."""
        ...

    def readlines(self) -> List[str]:
        """Read all lines."""
        ...

    def readall(self) -> str:
        """Read entire file."""
        ...

    def seekg(self, pos: int, whence: int = 0) -> 'FileStream':
        """Seek to position."""
        ...

    def tellg(self) -> int:
        """Get current position."""
        ...

    def eof(self) -> bool:
        """Check end of file."""
        ...

    def good(self) -> bool:
        """Check if stream is good."""
        ...


class Pipe:
    """Unix-style pipe for data transformation.

    Supports | operator for chaining transformations.

    Example:
        @result = pipe([1,2,3,4,5])
            | Pipe.filter(x => x > 2)
            | Pipe.map(x => x * 2)
            | collect();
    """

    def __init__(self, data: Any = None):
        """Create a pipe with initial data."""
        ...

    def collect(self) -> Any:
        """Collect final result."""
        ...

    def to_list(self) -> list:
        """Convert to list."""
        ...

    def to_string(self, sep: str = '') -> str:
        """Convert to string."""
        ...

    @staticmethod
    def filter(predicate: Callable) -> Callable:
        """Create filter transform."""
        ...

    @staticmethod
    def map(func: Callable) -> Callable:
        """Create map transform."""
        ...

    @staticmethod
    def reduce(func: Callable, initial: Any = None) -> Callable:
        """Create reduce transform."""
        ...

    @staticmethod
    def sort(key: Callable = None, reverse: bool = False) -> Callable:
        """Create sort transform."""
        ...

    @staticmethod
    def take(n: int) -> Callable:
        """Take first n elements."""
        ...

    @staticmethod
    def skip(n: int) -> Callable:
        """Skip first n elements."""
        ...

    @staticmethod
    def unique() -> Callable:
        """Remove duplicates."""
        ...

    @staticmethod
    def reverse() -> Callable:
        """Reverse order."""
        ...

    @staticmethod
    def grep(pattern: str) -> Callable:
        """Filter by regex pattern."""
        ...


class CStruct:
    """C-style struct with named fields.

    Fast, lightweight struct for performance-critical code.

    Example:
        struct Point { int x; int y; };
        Point p = {10, 20};
        p.x = 30;
        printl(sizeof(p));
    """

    def __init__(self, name: str, fields: Dict[str, str] = None):
        """Create a struct.

        Args:
            name: Struct name
            fields: Dict of field_name -> type
        """
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Convert struct to dictionary."""
        ...

    def sizeof(self) -> int:
        """Get estimated memory size."""
        ...

    def copy(self) -> 'CStruct':
        """Return a copy of the struct."""
        ...


# =============================================================================
# FUNCTION KEYWORDS (for defining functions)
# =============================================================================

class FunctionKeywords:
    """
    CSSL Function Keywords - Special modifiers for function definitions.

    These are not callable functions but keywords used when defining functions.
    """

    def void(self) -> None:
        """Function without return value.

        Example:
            void sayHello() {
                printl("Hello!");
            }
        """
        ...

    def define(self) -> None:
        """Constant function without type declaration.

        Does not require return type or 'void'. Used for simple procedures.

        Example:
            define LOG_MESSAGE() {
                printl("Log entry");
            }

            define processData() {
                // do something
            }
        """
        ...

    def undefined(self) -> None:
        """Function that silently ignores errors.

        Any exceptions during execution are caught and ignored.
        Useful for optional operations that may fail.

        Example:
            undefined void mayFail() {
                riskyOperation();  // Errors ignored
            }
            mayFail();  // Won't crash even if error occurs
        """
        ...

    def closed(self) -> None:
        """Function protected from EXTERNAL code injection.

        Prevents external scripts from using <<== to modify this function.
        Internal injections (same file) still work.

        Example:
            closed void protectedFunc() {
                printl("Protected from external injection");
            }

            // This will be BLOCKED if from different file:
            protectedFunc() <<== { printl("Blocked!"); }
        """
        ...

    def private(self) -> None:
        """Function with ALL injections blocked.

        Completely protects function from any CodeInfusion.
        No <<==, +<<==, or -<<== operations will work.

        Example:
            private void superSecure() {
                printl("Cannot be modified");
            }
        """
        ...

    def virtual(self) -> None:
        """Function safe for import cycles.

        Prevents infinite recursion when modules import each other.

        Example:
            virtual void safeForImport() {
                // Safe to call from circular imports
            }
        """
        ...

    def meta(self) -> None:
        """Function declared as source provider (must return).

        Indicates function provides metadata or source information.

        Example:
            meta string getSource() {
                return "source code here";
            }
        """
        ...

    def super_keyword(self) -> None:
        """Function that forces execution without exceptions.

        Function will complete even if errors occur internally.

        Example:
            super void forceRun() {
                printl("Will ALWAYS complete");
            }
        """
        ...

    def shuffled_keyword(self) -> None:
        """Function that can return multiple values.

        Return statement can have comma-separated values.
        Caller can unpack using tuple assignment.

        Example:
            shuffled string getNames() {
                return "Alice", "Bob", "Charlie";
            }

            // Unpack all values
            a, b, c = getNames();

            // Or with mixed types
            shuffled getValues() {
                return "hello", 42, true;
            }
            text, num, flag = getValues();
        """
        ...

    def open(self) -> None:
        """Function that accepts any number/type of parameters.

        Use with 'open Params' to accept variadic arguments.
        Use OpenFind<type>(index) to extract typed values.

        Example:
            open define flexibleFunc(open Params) {
                string name = OpenFind<string>(0);
                int count = OpenFind<int>(0);
                printl("Name: " + name + ", Count: " + count);
            }

            flexibleFunc("Alice", 42, true, "extra");
            // Extracts: name="Alice", count=42
        """
        ...

# =============================================================================
# CLASSES & OOP
# =============================================================================

class ClassSyntax:
    """
    CSSL Class Syntax - Object-Oriented Programming support.

    CSSL supports classes with constructors, members, and methods.
    Use 'this->' to access instance members inside methods.
    Use 'new' keyword to instantiate classes.
    """

    def class_definition(self) -> None:
        """Define a class with members and methods.

        Example:
            class Person {
                // Member variables
                string name;
                int age;

                // Constructor (same name as class)
                void Person(string n, int a) {
                    this->name = n;
                    this->age = a;
                }

                // Methods
                void greet() {
                    printl("Hello, I'm " + this->name);
                }

                string getName() {
                    return this->name;
                }

                void setAge(int a) {
                    this->age = a;
                }
            }
        """
        ...

    def new_keyword(self) -> None:
        """Instantiate a class using 'new' keyword.

        Example:
            Person p = new Person("Alice", 30);
            p.greet();                    // "Hello, I'm Alice"
            string name = p.getName();    // "Alice"
            p.setAge(31);
        """
        ...

    def this_keyword(self) -> None:
        """Access instance members with 'this->' inside methods.

        Example:
            class Counter {
                int count;

                void Counter() {
                    this->count = 0;
                }

                void increment() {
                    this->count = this->count + 1;
                }

                int get() {
                    return this->count;
                }
            }
        """
        ...

# =============================================================================
# SPECIAL SYNTAX REFERENCE
# =============================================================================

class SpecialSyntax:
    """
    CSSL Special Syntax Reference

    Reference for CSSL-specific syntax elements.
    """

    def global_variables(self) -> None:
        """Global variable syntax.

        Declare with 'global' keyword, access with '@' prefix.

        Example:
            // Declaration
            global myGlobal = "visible everywhere";
            r@anotherGlobal = "alternative syntax";

            // Access
            printl(@myGlobal);
            @myGlobal = "new value";

            // In functions
            void increment() {
                @counter = @counter + 1;
            }
        """
        ...

    def shared_objects(self) -> None:
        """Shared Python object syntax ($name).

        Access Python objects shared via CSSL.share().
        Changes reflect back to Python.

        Example:
            // Python: cssl.share(myObj, "data")

            // CSSL:
            $data.property = "value";
            $data.method();
            printl($data.result);

            // Delete when done
            delete("data");
        """
        ...

    def captured_references(self) -> None:
        """Value capture syntax (%identifier).

        Captures value at registration time, not execution time.
        Useful for saving original functions before replacement.

        Example:
            string version = "1.0";
            savedVersion <== { %version; }
            version = "2.0";
            printl(savedVersion);  // Still "1.0"

            // Save original function
            originalExit <<== { %exit(); }
            exit() <<== {
                printl("Custom exit");
                originalExit();  // Call saved original
            }
        """
        ...

    def code_infusion(self) -> None:
        """CodeInfusion operators for modifying functions.

        IMPORTANT: Write operators WITHOUT spaces!

        Operators:
            <<==   Replace function content
            +<<==  Add code BEFORE original
            -<<==  Remove matching code

        Example:
            void original() { printl("Original"); }

            // Replace
            original() <<== { printl("Replaced"); }

            // Add before
            original() +<<== { printl("Before"); }

            // Remove code
            original() -<<== { printl("Unwanted"); }
        """
        ...

    def brute_injection(self) -> None:
        """BruteInjection operators for data transfer.

        Operators:
            +<==   Copy data (source unchanged)
            -<==   Move data (removes from source)
            ==>    Replace target data
            ==>-   Remove matching items from target

        Example:
            stack<string> source = ["A", "B", "C"];
            datastruct<string> target;

            target +<== source;           // Copy
            target -<== source;           // Move (source empty)
            target ==> newData;           // Replace
            target ==>- ["A"];            // Remove "A" from target

            // With filters
            target +<== [string::contains="X"] source;
        """
        ...

    def filter_syntax(self) -> None:
        """Filter syntax for BruteInjection.

        Format: [type::filter=value]

        String filters:
            string::where="value"      Exact match
            string::not="value"        Exclude
            string::contains="sub"     Contains substring
            string::length=5           Exact length
            string::cut=3              First N chars
            string::cutAfter="sub"     After substring

        Example:
            stack<string> names = ["Alice", "Bob", "Anna"];
            datastruct<string> result;
            result +<== [string::contains="A"] names;
            // result = ["Alice", "Anna"]
        """
        ...

# =============================================================================
# DATA TYPES
# =============================================================================

class DataTypes:
    """
    CSSL Data Types Reference

    CSSL supports various primitive and compound data types for variable
    declarations and function parameters/returns.
    """

    def int_type(self) -> None:
        """Integer type - whole numbers.

        Range: Platform-dependent (typically 64-bit signed integer)

        Example:
            int x = 42;
            int negative = -100;
            int hex = 0xFF;          // Hexadecimal
            int binary = 0b1010;     // Binary (if supported)

            // Arithmetic
            int sum = x + 10;
            int product = x * 2;
            int quotient = x / 5;
            int remainder = x % 7;

            // Increment/decrement
            x++;
            x--;
        """
        ...

    def float_type(self) -> None:
        """Floating-point type - decimal numbers.

        Supports standard IEEE 754 double precision.

        Example:
            float pi = 3.14159;
            float negative = -2.5;
            float scientific = 1.5e10;   // 1.5 × 10^10

            // Arithmetic
            float result = pi * 2.0;
            float divided = 10.0 / 3.0;  // 3.333...

            // Conversion
            int rounded = int(pi);       // 3
            float fromInt = float(42);   // 42.0
        """
        ...

    def string_type(self) -> None:
        """String type - text sequences.

        Supports single quotes, double quotes, and string interpolation.

        Example:
            string name = "Alice";
            string alt = 'Bob';           // Single quotes work too

            // String interpolation (f-string style)
            string greeting = "Hello {name}!";     // "Hello Alice!"
            string altStyle = "Hello <name>!";     // Also works

            // Concatenation
            string full = "Hello" + " " + "World";
            string repeated = "ab" * 3;            // "ababab"

            // Methods/functions
            int length = len(name);                // 5
            string upper = upper(name);            // "ALICE"
            bool hasA = contains(name, "A");       // true

            // Indexing
            string first = name[0];                // "A"
            string slice = substr(name, 0, 3);     // "Ali"
        """
        ...

    def bool_type(self) -> None:
        """Boolean type - true/false values.

        Example:
            bool isActive = true;
            bool isComplete = false;

            // Logical operations
            bool and_result = true && false;       // false
            bool or_result = true || false;        // true
            bool not_result = !true;               // false

            // Comparisons return bool
            bool equal = (5 == 5);                 // true
            bool greater = (10 > 5);               // true
            bool notEqual = (3 != 4);              // true

            // In conditions
            if (isActive) {
                printl("Active!");
            }

            // Ternary operator
            string status = isActive ? "ON" : "OFF";
        """
        ...

    def dynamic_type(self) -> None:
        """Dynamic type - auto-typed, can hold any value.

        Similar to Python's duck typing. Type is determined at assignment.
        Can change type when reassigned.

        Example:
            dynamic x = 42;            // Currently int
            printl(typeof(x));         // "int"

            x = "hello";               // Now string
            printl(typeof(x));         // "str"

            x = [1, 2, 3];             // Now list
            printl(typeof(x));         // "list"

            // Useful for flexible functions
            dynamic result = getData();  // Unknown return type

            // Type checking
            if (isint(x)) {
                printl("It's a number!");
            }
        """
        ...

    def var_type(self) -> None:
        """Var type - type inference from assigned value.

        Type is inferred at assignment and remains fixed.
        More constrained than 'dynamic'.

        Example:
            var count = 100;           // Inferred as int
            var name = "Bob";          // Inferred as string
            var items = [1, 2, 3];     // Inferred as list

            // Type is determined by right-hand side
            var result = calculate();  // Type of function return
        """
        ...

    def list_type(self) -> None:
        """List type - ordered collection of values.

        Can contain mixed types. Zero-indexed.

        Example:
            // Declaration
            list items = [1, 2, 3, 4, 5];
            list mixed = ["hello", 42, true, 3.14];
            list empty = [];

            // Typed list (generic)
            list<int> numbers = [1, 2, 3];
            list<string> names = ["Alice", "Bob"];

            // Access
            int first = items[0];           // 1
            int last = items[len(items)-1]; // 5

            // Modification
            push(items, 6);                 // Add to end
            pop(items);                     // Remove from end
            items[0] = 100;                 // Set by index

            // Iteration
            foreach (item in items) {
                printl(item);
            }

            // Operations
            int length = len(items);
            bool hasValue = contains(items, 3);
            list sorted = sort(items);
            list reversed = reverse(items);
            list slice = slice(items, 1, 3);
        """
        ...

    def dict_type(self) -> None:
        """Dictionary type - key-value pairs.

        Keys are typically strings or integers. Values can be any type.
        Also available as 'dictionary' keyword.

        Example:
            // Declaration
            dict person = {
                "name": "Alice",
                "age": 30,
                "active": true
            };

            // Access
            string name = person["name"];       // "Alice"
            int age = person["age"];            // 30

            // Modification
            person["email"] = "alice@example.com";
            delkey(person, "active");

            // Methods
            list allKeys = keys(person);        // ["name", "age", "email"]
            list allValues = values(person);    // ["Alice", 30, "alice@..."]
            bool hasName = haskey(person, "name");  // true

            // Iteration
            foreach (key in keys(person)) {
                printl(key + ": " + person[key]);
            }

            // Safe access with default
            string value = getkey(person, "missing", "default");

            // Typed dictionary
            dictionary<string> data;
            data["key"] = "value";
        """
        ...

    def void_type(self) -> None:
        """Void type - no return value.

        Used for function declarations that don't return anything.

        Example:
            void sayHello() {
                printl("Hello!");
                // No return statement needed
            }

            void processData(int value) {
                // Do something with value
                // Returns nothing
            }

            // Calling
            sayHello();
        """
        ...

    def null_type(self) -> None:
        """Null type - absence of value.

        Represents no value or undefined state.
        Can be used with 'null' or 'None'.

        Example:
            dynamic x = null;
            var y = None;               // Same as null

            // Null checking
            if (x == null) {
                printl("No value");
            }

            if (isnull(x)) {
                printl("x is null");
            }

            // Default value pattern
            string result = value != null ? value : "default";
        """
        ...


# Data type aliases for direct lookup
int_t = DataTypes.int_type
"""int - Integer type for whole numbers.

Example:
    int count = 42;
    int negative = -100;
    count++;
"""

float_t = DataTypes.float_type
"""float - Floating-point type for decimal numbers.

Example:
    float pi = 3.14159;
    float result = 10.0 / 3.0;
"""

string_t = DataTypes.string_type
"""string - Text type with interpolation support.

Example:
    string name = "Alice";
    string msg = "Hello {name}!";
"""

bool_t = DataTypes.bool_type
"""bool - Boolean true/false type.

Example:
    bool active = true;
    bool done = false;
"""

dynamic_t = DataTypes.dynamic_type
"""dynamic - Auto-typed, can hold any value type.

Example:
    dynamic x = 42;
    x = "now a string";
"""

var_t = DataTypes.var_type
"""var - Type inference from assigned value.

Example:
    var count = 100;     // Inferred as int
    var name = "Bob";    // Inferred as string
"""

list_t = DataTypes.list_type
"""list - Ordered collection of values.

Example:
    list items = [1, 2, 3];
    list<string> names = ["Alice", "Bob"];
"""

dict_t = DataTypes.dict_type
"""dict - Key-value pair collection.

Example:
    dict data = {"name": "Alice", "age": 30};
    dict<string> config;
"""

void_t = DataTypes.void_type
"""void - No return value (function declaration).

Example:
    void sayHello() { printl("Hello!"); }
"""

null_t = DataTypes.null_type
"""null/None - Absence of value.

Example:
    dynamic x = null;
    if (isnull(x)) { printl("No value"); }
"""


# =============================================================================
# NON-NULL ASSERTIONS & TYPE EXCLUSION (v3.9.0)
# =============================================================================

class NonNullAndTypeExclusion:
    """
    CSSL Non-Null Assertions and Type Exclusion (v3.9.0)

    Special syntax for enforcing value constraints on functions and expressions.
    """

    def non_null_assertion(self) -> None:
        """Non-null assertion with * prefix.

        Assert that a value, function return, or class methods are never null.

        Syntax:
            *$variable          Assert shared object is non-null
            *@global            Assert global variable is non-null
            *expression         Assert expression result is non-null
            define *funcName()  Function must return non-null
            class *ClassName    All class methods return non-null

        Example - Value Assertion:
            // Assert shared object value is not null
            this->osName = *$System.os;  // Error if $System.os is null

            // Assert global is not null
            string value = *@config;

        Example - Non-null Function:
            // Function that must never return null/None
            define *alwaysReturns() {
                return "Always a value";
                // return null;  // Would cause error!
            }

            // Call - guaranteed non-null
            string result = alwaysReturns();

        Example - Non-null Class:
            // All methods in this class must return non-null
            class *MyClass {
                string getValue() {
                    return "Value";  // Must return something
                }

                int getNumber() {
                    return 42;  // Must return something
                }
            }

        Example - Non-null Parameter:
            // Filter out null values from open parameters
            define process(open *Params) {
                // Params will never contain null values
                foreach item in Params {
                    printl(item);  // Guaranteed non-null
                }
            }
        """
        ...

    def type_exclusion_filter(self) -> None:
        """Type exclusion filter with *[type] syntax.

        Specify that a function must NOT return a specific type.
        Particularly useful with shuffled functions that return multiple values.

        Syntax:
            define *[type]funcName()     Function must NOT return 'type'
            shuffled *[type]funcName()   Multi-return must NOT contain 'type'
            *[type]expression            Assert expression is NOT of 'type'

        Supported types:
            string, int, float, bool, null, none, list, array, dict, json

        Example - Exclude String:
            // Function must NOT return a string
            shuffled *[string] getNumbers() {
                return 1, 2, 3;       // OK - integers
                // return "text";     // Error! String not allowed
            }

        Example - Exclude Null:
            // Ensure function never returns null (alternative to *)
            define *[null] getValue() {
                return 42;           // OK
                // return null;      // Error!
            }

        Example - With Shuffled Functions:
            // Return multiple values, but none can be strings
            shuffled *[string] getMixedData() {
                return 100, 3.14, true;  // OK - int, float, bool
            }

            // Unpack the values
            num, decimal, flag = getMixedData();

        Example - Expression Assertion:
            // Assert the result is not a string
            dynamic result = *[string] getData();
            // Error if getData() returns a string

        Note:
            For tuple returns (shuffled), each value in the tuple is checked
            against the excluded type. If any value matches, an error is raised.
        """
        ...


# =============================================================================
# APPEND MODE (v3.8.9)
# =============================================================================

class AppendMode:
    """
    CSSL Append Mode (v3.8.9)

    The ++ append operator allows extending constructors and functions
    by keeping the original code and adding new code after it.
    """

    def function_append(self) -> None:
        """Append to a function with &FunctionName ++.

        Keeps original function code and adds new code after it.

        Syntax:
            define NewFunc() &OriginalFunc ++ {
                // New code runs AFTER OriginalFunc
            }

        Example:
            // Original function
            define BaseFunc() {
                printl("Base functionality");
            }

            // Append to BaseFunc - keeps original + adds new
            define ExtendedFunc() &BaseFunc ++ {
                printl("Extended functionality");
            }

            ExtendedFunc();
            // Output:
            // Base functionality
            // Extended functionality
        """
        ...

    def constructor_append(self) -> None:
        """Append to a constructor with &ClassName::constructor ++.

        Extend parent constructor while keeping its initialization.

        Syntax:
            constr Name() &ParentClass::ParentConstructor ++ {
                // Additional initialization
            }

        Example:
            class MyClass {
                constr MyClassConstructor() {
                    printl("MyClass constructor");
                    this->value = 10;
                }
            }

            class BetterClass :: extends MyClass {
                // Append to specific parent constructor
                constr BetterConstructor() &MyClass::MyClassConstructor ++ {
                    printl("BetterClass - added code");
                    this->extra = 20;
                }
            }

            $instance = new BetterClass();
            // Output:
            // MyClass constructor
            // BetterClass - added code
            printl($instance.value);  // 10
            printl($instance.extra);  // 20
        """
        ...

    def method_append(self) -> None:
        """Append to a class method with &ClassName::method ++.

        Example:
            class Parent {
                define greet() {
                    printl("Hello from Parent");
                }
            }

            class Child :: extends Parent {
                // Append to parent method
                define betterGreet() &Parent::greet ++ {
                    printl("And also from Child!");
                }
            }

            $child = new Child();
            $child.betterGreet();
            // Output:
            // Hello from Parent
            // And also from Child!
        """
        ...

    def instance_append(self) -> None:
        """Append using instance reference with &$instance::member ++.

        Example:
            global $myInstance = new SomeClass();

            class Extended {
                define extendedMethod() &$myInstance::originalMethod ++ {
                    printl("Added to instance method");
                }
            }
        """
        ...


# =============================================================================
# BINARY TYPES (v4.9.0)
# =============================================================================

class CSSLBit:
    """CSSL bit type - Single binary value (0 or 1).

    A bit represents the smallest unit of data - a single binary digit that
    can only be 0 or 1. Useful for flags, toggles, and binary operations.

    Declaration in CSSL:
        bit flag = 1;
        bit enabled = 0;

    Example:
        bit active = 1;
        printl(active);        // 1

        active.switch();       // Toggle: 1 -> 0
        printl(active);        // 0

        active.set(1);         // Set to 1
        printl(active);        // 1
    """

    def switch(self) -> 'CSSLBit':
        """Toggle the bit value (0 -> 1, 1 -> 0).

        Returns:
            The bit (for chaining)

        Example:
            bit flag = 1;
            flag.switch();     // Now 0
            flag.switch();     // Now 1 again
        """
        ...

    def toggle(self) -> 'CSSLBit':
        """Alias for switch(). Toggle the bit value."""
        ...

    def set(self, value: int = 1) -> 'CSSLBit':
        """Set the bit to a specific value.

        Args:
            value: 0 or 1 (default: 1)

        Returns:
            The bit (for chaining)

        Example:
            bit flag = 0;
            flag.set(1);       // Now 1
            flag.set(0);       // Now 0
            flag.set();        // Now 1 (default)
        """
        ...

    def clear(self) -> 'CSSLBit':
        """Clear the bit (set to 0).

        Returns:
            The bit (for chaining)

        Example:
            bit flag = 1;
            flag.clear();      // Now 0
        """
        ...

    def is_set(self) -> bool:
        """Check if the bit is set (equals 1).

        Returns:
            True if bit is 1, False if 0

        Example:
            bit flag = 1;
            if (flag.is_set()) {
                printl("Flag is active");
            }
        """
        ...

    def is_clear(self) -> bool:
        """Check if the bit is clear (equals 0).

        Returns:
            True if bit is 0, False if 1
        """
        ...

    def copy(self) -> 'CSSLBit':
        """Create a copy of this bit.

        Returns:
            A new bit with the same value

        Example:
            bit a = 1;
            bit b = a.copy();
            a.switch();
            printl(a);  // 0
            printl(b);  // 1 (unchanged)
        """
        ...


class CSSLByte:
    """CSSL byte type - 8-bit value with x^y notation.

    A byte represents 8 bits with a special notation: base^weight where
    base is 0 or 1 (determines signed/unsigned interpretation) and
    weight is the value (0-255).

    Declaration in CSSL:
        byte b = 1^200;    // Unsigned: value = 200
        byte s = 0^100;    // Signed: value = 100

    The x^y notation provides clear semantics:
        - 1^n: Unsigned byte, value = n (0-255)
        - 0^n: Signed interpretation context

    Example:
        byte data = 1^255;
        printl(data.value());      // 255
        printl(data.to_str());     // "11111111" (binary)
        printl(data.info());       // Full byte info dict

        byte flags = 1^0;
        flags.set(7, 1);           // Set bit 7
        printl(flags.to_str());    // "10000000"
    """

    def value(self) -> int:
        """Get the numeric value of the byte.

        Returns:
            Integer value (0-255)

        Example:
            byte b = 1^200;
            printl(b.value());  // 200
        """
        ...

    def raw(self) -> int:
        """Get raw weight value. Alias for value()."""
        ...

    def unsigned(self) -> int:
        """Get unsigned interpretation of the byte.

        Returns:
            Unsigned integer value (0-255)
        """
        ...

    def to_bits(self) -> List[int]:
        """Get list of individual bits (LSB first).

        Returns:
            List of 8 integers, each 0 or 1

        Example:
            byte b = 1^200;
            printl(b.to_bits());  // [0, 0, 0, 1, 0, 0, 1, 1] (200 = 11001000)
        """
        ...

    def to_str(self) -> str:
        """Get binary string representation.

        Returns:
            8-character string of 0s and 1s

        Example:
            byte b = 1^200;
            printl(b.to_str());  // "11001000"
        """
        ...

    def reverse(self) -> 'CSSLByte':
        """Reverse the bit order.

        Returns:
            New byte with reversed bits

        Example:
            byte b = 1^200;           // 11001000
            byte r = b.reverse();     // 00010011 (19)
        """
        ...

    def copy(self) -> 'CSSLByte':
        """Create a copy of this byte.

        Returns:
            A new byte with the same base and weight
        """
        ...

    def get(self, index: int) -> 'CSSLBit':
        """Get bit at specified index.

        Args:
            index: Bit position (0-7, where 0 is LSB)

        Returns:
            Bit object at that position

        Example:
            byte b = 1^200;  // 11001000
            printl(b.get(3));  // 1 (bit 3 is set)
            printl(b.get(0));  // 0 (bit 0 is clear)
        """
        ...

    def at(self, index: int) -> int:
        """Get bit value at index. Returns int directly.

        Args:
            index: Bit position (0-7)

        Returns:
            0 or 1
        """
        ...

    def set(self, index: int, value: int) -> 'CSSLByte':
        """Set bit at index to specific value.

        Args:
            index: Bit position (0-7)
            value: 0 or 1

        Returns:
            The byte (for chaining)

        Example:
            byte b = 1^0;
            b.set(7, 1);        // Set MSB
            b.set(0, 1);        // Set LSB
            printl(b.value());  // 129
        """
        ...

    def change(self, index: int, value: int) -> 'CSSLByte':
        """Alias for set(). Set bit at index."""
        ...

    def switch(self, index: int) -> 'CSSLByte':
        """Toggle bit at specified index.

        Args:
            index: Bit position to toggle (0-7)

        Returns:
            The byte (for chaining)

        Example:
            byte b = 1^200;     // 11001000
            b.switch(7);        // 01001000 (toggle bit 7)
        """
        ...

    def write(self, index: int, count: int) -> 'CSSLByte':
        """Set 'count' consecutive bits starting at index to 1.

        Args:
            index: Starting bit position
            count: Number of bits to set

        Returns:
            The byte (for chaining)

        Example:
            byte b = 1^0;
            b.write(0, 4);      // Set bits 0-3
            printl(b.value());  // 15 (00001111)
        """
        ...

    def info(self) -> Dict[str, Any]:
        """Get detailed byte information.

        Returns:
            Dictionary with: base, weight, value, unsigned, binary, hex, bits

        Example:
            byte b = 1^200;
            printl(b.info());
            // {'base': 1, 'weight': 200, 'value': 200, 'unsigned': 200,
            //  'binary': '11001000', 'hex': '0xc8',
            //  'bits': [0, 0, 0, 1, 0, 0, 1, 1]}
        """
        ...

    def len(self) -> int:
        """Get number of bits (always 8).

        Returns:
            8
        """
        ...

    @staticmethod
    def from_bits(bits: List[int]) -> 'CSSLByte':
        """Create byte from list of bits.

        Args:
            bits: List of 8 integers (0 or 1)

        Returns:
            New byte with those bit values

        Example:
            byte b = Byte.from_bits([1, 0, 0, 0, 0, 0, 0, 0]);  // 1
        """
        ...


class CSSLAddress:
    """CSSL address type - Memory reference (pointer-like).

    An address stores a memory reference to an object and can be used to
    retrieve the object later using reflect(). Works like a pointer but
    with Python's reference semantics.

    Declaration in CSSL:
        address addr = address(someObject);
        address ptr = memory(obj).get("address");

    Example:
        string text = "Hello";
        address addr = address(text);

        // Later, in another function:
        obj = addr.reflect();  // or reflect(addr)
        printl(obj);  // "Hello"
    """

    @property
    def value(self) -> str:
        """Get the address value as a hex string.

        Returns:
            Address string (e.g., "0x7fff3adb4ed8")

        Example:
            address addr = address(obj);
            printl(addr.value);  // "0x7fff3adb4ed8"
        """
        ...

    def reflect(self) -> Any:
        """Reflect the address to get the original object.

        Returns:
            The object at this address, or None if not found

        Example:
            string text = "Hello";
            address addr = address(text);

            // In another function:
            obj = addr.reflect();
            printl(obj);  // "Hello"
        """
        ...

    def is_null(self) -> bool:
        """Check if this is a null address.

        Returns:
            True if address is null (0x0)

        Example:
            address addr;  // Null address
            if (addr.is_null()) {
                printl("No address set");
            }
        """
        ...

    def copy(self) -> 'CSSLAddress':
        """Create a copy of this address.

        Returns:
            A new address pointing to the same location
        """
        ...

    @staticmethod
    def from_object(obj: Any) -> 'CSSLAddress':
        """Create an Address from any object.

        Args:
            obj: Object to get address of

        Returns:
            Address pointing to the object
        """
        ...


# Type aliases for quick access
bit = CSSLBit
byte = CSSLByte
address = CSSLAddress


# =============================================================================
# ASYNC MODULE (v4.9.3)
# =============================================================================

class CSSLFuture:
    """Future - represents the result of an async operation.

    A Future is returned when you call an async function or use async.run().
    Use await or async.wait() to get the result.

    States:
        pending   - Not started
        running   - Currently executing
        completed - Finished successfully
        cancelled - Cancelled before completion
        failed    - Finished with error

    Example:
        async define fetchData(url) {
            return http.get(url);
        }

        // Calling async function returns Future immediately
        future f = fetchData("http://example.com");

        // Wait for result with await
        data = await f;

        // Or check state
        if (f.is_done()) {
            result = f.result();
        }
    """

    PENDING: str
    RUNNING: str
    COMPLETED: str
    CANCELLED: str
    FAILED: str

    def result(self, timeout: Optional[float] = None) -> Any:
        """Get the result, blocking until complete.

        Args:
            timeout: Optional timeout in seconds

        Returns:
            The result of the async operation

        Raises:
            Exception if operation failed or timed out
        """
        ...

    def is_done(self) -> bool:
        """Check if the operation has completed (success, fail, or cancel)."""
        ...

    def cancel(self) -> bool:
        """Cancel the operation if not yet complete."""
        ...

    def then(self, callback: Callable[[Any], Any]) -> 'CSSLFuture':
        """Chain a callback to run when complete.

        Example:
            fetchData("url").then(lambda data: printl(data));
        """
        ...


class CSSLGenerator:
    """Generator - lazy iteration via yield.

    Generators produce values on-demand using yield statements.
    Created by calling a generator function (one that uses yield).

    Example - Basic Generator:
        generator<int> define Range(int n) {
            int i = 0;
            while (i < n) {
                yield i;
                i = i + 1;
            }
        }

        gen = Range(5);
        while (gen.has_next()) {
            printl(gen.next());  // 0, 1, 2, 3, 4
        }

        // Or convert to list
        numbers = Range(10).to_list();  // [0,1,2,...,9]

    Example - Generator with send():
        generator<int> define Counter() {
            int value = 0;
            while (true) {
                received = yield value;
                if (received != null) {
                    value = received;
                } else {
                    value = value + 1;
                }
            }
        }

        counter = Counter();
        printl(counter.next());   // 0
        printl(counter.next());   // 1
        counter.send(100);        // Resume with value 100
        printl(counter.next());   // 101
    """

    def next(self) -> Any:
        """Get the next yielded value.

        Returns:
            The next value from the generator, or None when exhausted
        """
        ...

    def has_next(self) -> bool:
        """Check if more values are available."""
        ...

    def send(self, value: Any) -> Any:
        """Send a value into the generator.

        The sent value becomes the result of the yield expression in the generator.
        Use this to communicate with coroutine-style generators.

        Args:
            value: The value to send into the generator

        Returns:
            The next yielded value

        Example:
            received = yield current_value;  // received gets the sent value
        """
        ...

    def to_list(self) -> List[Any]:
        """Consume all remaining values into a list.

        Warning: Do not use on infinite generators (while true)!
        """
        ...

    def take(self, n: int) -> List[Any]:
        """Take up to n values. Safe for infinite generators."""
        ...

    def skip(self, n: int) -> 'CSSLGenerator':
        """Skip n values and return self for chaining."""
        ...


class AsyncModule:
    """Async module - utilities for async/await operations.

    Access via: async.run(), async.wait(), etc.
    Or: Async.run(), Async.wait(), etc.

    Example:
        async define slowTask() {
            async.sleep(1000);
            return "Done!";
        }

        future f = async.run(slowTask);
        result = await f;

        // Or wait for multiple:
        results = async.all([f1, f2, f3]);

        // First to complete:
        winner = async.race([f1, f2, f3]);
    """

    @staticmethod
    def run(func: Callable, *args, **kwargs) -> CSSLFuture:
        """Run a function asynchronously.

        Args:
            func: Function to run (async or regular)
            *args: Arguments to pass
            **kwargs: Keyword arguments

        Returns:
            Future representing the operation
        """
        ...

    @staticmethod
    def stop(future_or_name: Union[CSSLFuture, str]) -> bool:
        """Cancel an async operation.

        Args:
            future_or_name: Future to cancel or function name

        Returns:
            True if cancelled successfully
        """
        ...

    @staticmethod
    def wait(future: CSSLFuture, timeout: Optional[float] = None) -> Any:
        """Wait for a future to complete.

        Args:
            future: The future to wait for
            timeout: Optional timeout in seconds

        Returns:
            The result of the future
        """
        ...

    @staticmethod
    def all(futures: List[CSSLFuture], timeout: Optional[float] = None) -> List[Any]:
        """Wait for all futures to complete.

        Args:
            futures: List of futures to wait for
            timeout: Optional timeout in seconds

        Returns:
            List of results in same order as input
        """
        ...

    @staticmethod
    def race(futures: List[CSSLFuture], timeout: Optional[float] = None) -> Any:
        """Return result of first completed future.

        Args:
            futures: List of futures to race
            timeout: Optional timeout in seconds

        Returns:
            Result of first completed future
        """
        ...

    @staticmethod
    def sleep(ms: int) -> CSSLFuture:
        """Async sleep for milliseconds.

        Args:
            ms: Milliseconds to sleep

        Returns:
            Future that completes after delay
        """
        ...


# Type aliases for async
future = CSSLFuture
generator = CSSLGenerator


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Output
    "print", "printl", "println", "debug", "error", "warn", "log",
    # Type conversion
    "int", "float", "str", "bool", "list", "dict",
    # Type checking
    "typeof", "isinstance", "isint", "isfloat", "isstr", "isbool",
    "islist", "isdict", "isnull",
    # String
    "len", "upper", "lower", "trim", "ltrim", "rtrim", "split", "join",
    "replace", "substr", "contains", "startswith", "endswith", "format",
    "concat", "repeat", "reverse", "indexof", "lastindexof", "padleft",
    "padright", "capitalize", "title", "swapcase", "center", "zfill",
    "chars", "ord", "chr", "isalpha", "isdigit", "isalnum", "isspace",
    "sprintf",
    # Array/List
    "push", "pop", "shift", "unshift", "slice", "sort", "rsort",
    "unique", "flatten", "filter", "map", "reduce", "find", "findindex",
    "every", "some", "range", "enumerate", "zip", "reversed", "count",
    "first", "last", "take", "drop", "chunk", "shuffle", "sample",
    # Dictionary
    "keys", "values", "items", "haskey", "getkey", "setkey", "delkey",
    "merge", "update", "fromkeys", "invert", "pick", "omit", "groupby",
    # Math
    "abs", "min", "max", "sum", "avg", "round", "floor", "ceil",
    "pow", "sqrt", "mod", "random", "randint", "sin", "cos", "tan",
    "asin", "acos", "atan", "atan2", "log", "log10", "exp", "pi", "e",
    "radians", "degrees",
    # Date/Time
    "now", "timestamp", "sleep", "delay", "date", "time", "datetime",
    "strftime",
    # File System
    "read", "readline", "write", "writeline", "appendfile", "readlines",
    "pathexists", "isfile", "isdir", "listdir", "makedirs", "removefile",
    "removedir", "copyfile", "movefile", "filesize", "basename", "dirname",
    "joinpath", "abspath", "normpath", "splitpath",
    # JSON (json:: namespace)
    "json_read", "json_write", "json_parse", "json_stringify", "json_pretty",
    "json_get", "json_set", "json_has", "json_keys", "json_values", "json_merge",
    # Instance (instance:: namespace)
    "instance_getMethods", "instance_getClasses", "instance_getVars",
    "instance_getAll", "instance_call", "instance_has", "instance_type",
    "isavailable",
    # Regex
    "match", "search", "findall", "sub",
    # Hash
    "md5", "sha1", "sha256",
    # System/Control
    "exit", "input", "env", "setenv", "clear", "copy", "deepcopy",
    "assert_condition", "pyimport", "include", "payload", "color",
    "original", "delete",
    # Platform
    "isLinux", "isWindows", "isMac",
    # Container Classes (with methods)
    "CSSLStack", "CSSLVector", "CSSLArray", "CSSLMap", "CSSLDataStruct",
    "CSSLIterator", "CSSLShuffled", "CSSLCombo", "CSSLDataSpace", "OpenFind",
    # Container Type Aliases (use these for quick method lookup)
    "stack", "vector", "array", "map", "datastruct", "iterator", "shuffled", "combo", "dataspace",
    # Syntax Reference Classes
    "FunctionKeywords", "ClassSyntax", "SpecialSyntax",
    # Data Types Reference
    "DataTypes", "int_t", "float_t", "string_t", "bool_t", "dynamic_t",
    "var_t", "list_t", "dict_t", "void_t", "null_t",
    # v3.8.9 & v3.9.0 Features
    "AppendMode", "NonNullAndTypeExclusion",
    # Filter functions (filter:: namespace)
    "filter_register", "filter_unregister", "filter_list", "filter_exists",
    # v4.8.4: C++ I/O Streams & Import
    "cppimport", "include", "cout", "cin", "cerr", "clog", "endl", "flush",
    "getline", "fstream", "ifstream", "ofstream",
    "setprecision", "setw", "setfill", "fixed", "scientific",
    # v4.8.4: Struct & Memory operations
    "sizeof", "memcpy", "memset", "struct",
    # v4.8.4: Pipe operations
    "pipe", "contains_fast",
    # v4.8.4: Stream types
    "OutputStream", "InputStream", "FileStream", "Pipe", "CStruct",
    # v4.9.0: Binary types and address pointer
    "CSSLBit", "CSSLByte", "CSSLAddress", "bit", "byte", "address", "reflect",
    # v4.9.3: Async types
    "CSSLFuture", "CSSLGenerator", "AsyncModule", "future", "generator",
    "async", "await", "yield",
]
