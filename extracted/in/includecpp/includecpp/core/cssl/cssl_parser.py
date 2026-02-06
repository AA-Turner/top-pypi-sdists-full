"""
CSSL Parser - Lexer and Parser for CSSL Language

Features:
- Complete tokenization of CSSL syntax
- AST (Abstract Syntax Tree) generation
- Enhanced error reporting with line/column info
- Support for service files and standalone programs
- Special operators: <== (inject), ==> (receive), -> <- (flow)
- Module references (@Module) and self-references (s@Struct)
"""

import re
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union


class CSSLSyntaxError(Exception):
    """Syntax error with detailed location information"""

    def __init__(self, message: str, line: int = 0, column: int = 0, source_line: str = ""):
        self.line = line
        self.column = column
        self.source_line = source_line

        # Build detailed error message
        location = f" at line {line}" if line else ""
        if column:
            location += f", column {column}"

        full_message = f"CSSL Syntax Error{location}: {message}"

        if source_line:
            full_message += f"\n  {source_line}"
            if column > 0:
                full_message += f"\n  {' ' * (column - 1)}^"

        super().__init__(full_message)


class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    STRING = auto()
    STRING_INTERP = auto()  # <variable> in strings
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()
    TYPE_LITERAL = auto()  # list, dict as type literals
    TYPE_GENERIC = auto()  # datastruct<T>, shuffled<T>, iterator<T>, combo<T>
    OPERATOR = auto()
    # Basic injection operators
    INJECT_LEFT = auto()        # <==
    INJECT_RIGHT = auto()       # ==>
    # BruteForce Injection operators - Copy & Add
    INJECT_PLUS_LEFT = auto()   # +<==
    INJECT_PLUS_RIGHT = auto()  # ==>+
    # BruteForce Injection operators - Move & Remove
    INJECT_MINUS_LEFT = auto()  # -<==
    INJECT_MINUS_RIGHT = auto() # ===>-
    # BruteForce Injection operators - Code Infusion
    INFUSE_LEFT = auto()        # <<==
    INFUSE_RIGHT = auto()       # ==>>
    INFUSE_PLUS_LEFT = auto()   # +<<==
    INFUSE_PLUS_RIGHT = auto()  # ==>>+
    INFUSE_MINUS_LEFT = auto()  # -<<==
    INFUSE_MINUS_RIGHT = auto() # ==>>-
    # Flow operators
    FLOW_RIGHT = auto()
    FLOW_LEFT = auto()
    EQUALS = auto()
    COMPARE_EQ = auto()
    COMPARE_NE = auto()
    COMPARE_LT = auto()
    COMPARE_GT = auto()
    COMPARE_LE = auto()
    COMPARE_GE = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    TILDE = auto()  # ~ for destructors (v4.8.8)
    CARET = auto()  # ^ for byte notation (v4.9.0)
    QUESTION = auto()  # ? for pointer references (v4.9.0)
    AMPERSAND = auto()  # & for references
    BLOCK_START = auto()
    BLOCK_END = auto()
    PAREN_START = auto()
    PAREN_END = auto()
    BRACKET_START = auto()
    BRACKET_END = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOUBLE_COLON = auto()  # :: for injection helpers (string::where, json::key, etc)
    COMMA = auto()
    DOT = auto()
    AT = auto()
    GLOBAL_REF = auto()  # r@<name> global variable declaration
    SELF_REF = auto()    # s@<name> self-reference to global struct
    SHARED_REF = auto()  # $<name> shared object reference
    CAPTURED_REF = auto()  # %<name> captured reference (for infusion)
    POINTER_REF = auto()  # ?<name> pointer reference (v4.9.0)
    POINTER_SNAPSHOT_REF = auto()  # ?%<name> pointer to snapshot reference (v4.9.4)
    THIS_REF = auto()      # this-><name> class member reference
    LOCAL_REF = auto()     # local::<name> hooked function local variable access (v4.9.2)
    PACKAGE = auto()
    PACKAGE_INCLUDES = auto()
    AS = auto()
    COMMENT = auto()
    NEWLINE = auto()
    EOF = auto()
    # Super-functions for .cssl-pl payload files (v3.8.0)
    SUPER_FUNC = auto()    # #$run(), #$exec(), #$printl() - pre-execution hooks
    # Append operator for constructor/function extension
    PLUS_PLUS = auto()     # ++ for constructor/function append (keeps old + adds new)
    MINUS_MINUS = auto()   # -- for potential future use
    # Multi-language support (v4.1.0)
    LANG_INSTANCE_REF = auto()  # cpp$InstanceName, py$Object - cross-language instance access
    # v4.8.4: Pipe operator and stream operators
    PIPE = auto()               # | for data piping
    STREAM_OUT = auto()         # << for stream output (cout << x)
    STREAM_IN = auto()          # >> for stream input (cin >> x)
    IN = auto()                 # 'in' keyword for containment check


KEYWORDS = {
    # Service structure
    'service-init', 'service-run', 'service-include', 'struct', 'define', 'class', 'namespace', 'constr', 'extends', 'overwrites', 'new', 'this', 'super', 'enum',
    # Control flow
    'if', 'else', 'elif', 'while', 'for', 'foreach', 'in', 'range',
    'switch', 'case', 'default', 'break', 'continue', 'return',
    'try', 'catch', 'finally', 'throw', 'raise',
    'except', 'always',  # v4.2.5: param switch keywords
    # Literals
    'True', 'False', 'null', 'None', 'true', 'false',
    # Logical operators
    'and', 'or', 'not',
    # Async/Events
    'start', 'stop', 'wait_for', 'on_event', 'emit_event', 'await',
    'async', 'yield', 'generator', 'future',  # v4.9.3: Full async/generator support
    # Package system
    'package', 'package-includes', 'exec', 'as', 'global',
    # CSSL Type Keywords
    'int', 'string', 'float', 'bool', 'void', 'json', 'array', 'vector', 'stack',
    'list', 'dictionary', 'dict', 'instance', 'map', 'queue',  # Python-like types + queue (v4.7)
    'bit', 'byte', 'address', 'ptr', 'pointer',  # v4.9.0: Binary types, address, ptr/pointer
    'auto', 'python',  # v4.9.8: auto type inference, python:: namespace types
    'local',  # v4.9.2: Hook local variable access (local::varname)
    'freezed',  # v4.9.4: Immutable variable (cannot be reassigned)
    'dynamic',      # No type declaration (slow but flexible)
    'undefined',    # Function errors ignored
    'open',         # Accept any parameter type
    'datastruct',   # Universal container (lazy declarator)
    'dataspace',    # SQL/data storage container
    'shuffled',     # Unorganized fast storage (multiple returns)
    'bytearrayed',  # Function-to-byte mapping with pattern matching (v4.2.5)
    'iterator',     # Advanced iterator with tasks
    'combo',        # Filter/search spaces
    'structure',    # Advanced C++/Py Class
    'openquote',    # SQL openquote container
    # CSSL Function Modifiers
    'const',        # Immutable function (like C++)
    'meta',         # Source function (must return)
    'super',        # Force execution (no exceptions)
    'closed',       # Protect from external injection
    'private',      # Disable all injections
    'virtual',      # Import cycle safe
    'sqlbased',     # SQL-based function
    'public',       # Explicitly public (default)
    'static',       # Static method/function
    'embedded',     # Immediate &target replacement at registration (v4.2.5)
    'native',       # Force C++ execution (no Python fallback)
    'unative',      # Force Python execution (no C++ - opposite of native)
    'secure',       # v4.8.8: Constructor runs only on exception
    'callable',     # v4.8.8: Constructor must be manually called
    # CSSL Include Keywords
    'include',  # v4.8.6: Removed 'get' from keywords - it's a builtin function, not keyword
    # Multi-language support (v4.1.0)
    'supports', 'libinclude',
    # Memory binding (v4.9.0)
    'uses', 'memory',
    # Memory copying (v4.9.9)
    'copies',
}

# Function modifiers that can appear in any order before function name
FUNCTION_MODIFIERS = {
    'undefined', 'open', 'meta', 'super', 'closed', 'private', 'virtual',
    'sqlbased', 'const', 'public', 'static', 'global', 'shuffled', 'embedded',
    'native',  # Force C++ execution
    'unative',  # Force Python execution (opposite of native)
    'bytearrayed',  # v4.7: Function-to-byte mapping with pattern matching
    'async',  # v4.9.3: Async function modifier
}

# Type literals that create empty instances
TYPE_LITERALS = {'list', 'dict'}

# Generic type keywords that use <T> syntax
TYPE_GENERICS = {
    'datastruct', 'dataspace', 'shuffled', 'iterator', 'combo',
    'vector', 'stack', 'array', 'openquote', 'list', 'dictionary', 'map',
    'queue',  # v4.7: Thread-safe queue with multi-iterator support
    'generator', 'future',  # v4.9.3: Async types
}

# Functions that accept type parameters: FuncName<type>(args)
TYPE_PARAM_FUNCTIONS = {
    'OpenFind'  # OpenFind<string>(0)
}

# Injection helper prefixes (type::helper=value)
INJECTION_HELPERS = {
    'string', 'integer', 'json', 'array', 'vector', 'combo', 'dynamic', 'sql'
}

# Language identifiers for multi-language support (v4.1.0)
# Used in lang$instance patterns like cpp$MyClass, py$Object
LANGUAGE_IDS = {
    'cpp', 'py', 'python', 'java', 'csharp', 'js', 'javascript'
}


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int


class CSSLLexer:
    """Tokenizes CSSL source code into a stream of tokens."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        # Store source lines for error messages
        self.source_lines = source.split('\n')

    def get_source_line(self, line_num: int) -> str:
        """Get a specific source line for error reporting"""
        if 0 < line_num <= len(self.source_lines):
            return self.source_lines[line_num - 1]
        return ""

    def error(self, message: str):
        """Raise a syntax error with location info"""
        raise CSSLSyntaxError(
            message,
            line=self.line,
            column=self.column,
            source_line=self.get_source_line(self.line)
        )

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break

            char = self.source[self.pos]

            # Super-functions (#$) or Comments (# and // style)
            if char == '#':
                if self._peek(1) == '$':
                    # Super-function: #$run(), #$exec(), #$printl()
                    self._read_super_function()
                else:
                    # Regular comment
                    self._skip_comment()
            elif char == '/' and self._peek(1) == '/':
                # C-style // comment - NEW
                self._skip_comment()
            elif char == '\n':
                self._add_token(TokenType.NEWLINE, '\n')
                self._advance()
                self.line += 1
                self.column = 1
            elif char in '"\'':
                self._read_string(char)
            elif char == '`':
                # Raw string (no escape processing) - useful for JSON
                self._read_raw_string()
            elif char.isdigit() or (char == '-' and self._peek(1).isdigit()):
                self._read_number()
            elif char == 'r' and self._peek(1) == '@':
                # r@<name> global variable declaration (same as 'global')
                self._read_global_ref()
            elif char == 's' and self._peek(1) == '@':
                # s@<name> self-reference to global struct
                self._read_self_ref()
            elif char.isalpha() or char == '_':
                # v4.8.6: Detect f-string syntax and throw clear error
                if char == 'f' and self._peek(1) in ('"', "'"):
                    raise CSSLSyntaxError(
                        f"f-string syntax is not supported in CSSL. Use string concatenation instead:\n"
                        f"  Instead of: f\"Hello {{name}}\"\n"
                        f"  Use: \"Hello \" + name",
                        line=self.line
                    )
                self._read_identifier()
            elif char == '@':
                self._add_token(TokenType.AT, '@')
                self._advance()
            elif char == '$':
                # $<name> shared object reference
                self._read_shared_ref()
            elif char == '%':
                # Check if this is %<name> captured reference or % modulo operator
                next_char = self._peek(1)
                if next_char and (next_char.isalpha() or next_char == '_'):
                    # %<name> captured reference (for infusion)
                    self._read_captured_ref()
                else:
                    # % modulo operator
                    self._add_token(TokenType.MODULO, '%')
                    self._advance()
            elif char == '&':
                # & for references
                if self._peek(1) == '&':
                    self._add_token(TokenType.AND, '&&')
                    self._advance()
                    self._advance()
                else:
                    self._add_token(TokenType.AMPERSAND, '&')
                    self._advance()
            elif char == '{':
                self._add_token(TokenType.BLOCK_START, '{')
                self._advance()
            elif char == '}':
                self._add_token(TokenType.BLOCK_END, '}')
                self._advance()
            elif char == '(':
                self._add_token(TokenType.PAREN_START, '(')
                self._advance()
            elif char == ')':
                self._add_token(TokenType.PAREN_END, ')')
                self._advance()
            elif char == '[':
                self._add_token(TokenType.BRACKET_START, '[')
                self._advance()
            elif char == ']':
                self._add_token(TokenType.BRACKET_END, ']')
                self._advance()
            elif char == ';':
                self._add_token(TokenType.SEMICOLON, ';')
                self._advance()
            elif char == ':':
                # Check for :: (double colon for injection helpers)
                if self._peek(1) == ':':
                    self._add_token(TokenType.DOUBLE_COLON, '::')
                    self._advance()
                    self._advance()
                else:
                    self._add_token(TokenType.COLON, ':')
                    self._advance()
            elif char == ',':
                self._add_token(TokenType.COMMA, ',')
                self._advance()
            elif char == '.':
                self._add_token(TokenType.DOT, '.')
                self._advance()
            elif char == '+':
                # Check for ++ (append operator for constructor/function extension)
                if self._peek(1) == '+':
                    self._add_token(TokenType.PLUS_PLUS, '++')
                    self._advance()
                    self._advance()
                # Check for BruteForce Injection: +<== or +<<==
                elif self._peek(1) == '<' and self._peek(2) == '<' and self._peek(3) == '=' and self._peek(4) == '=':
                    self._add_token(TokenType.INFUSE_PLUS_LEFT, '+<<==')
                    for _ in range(5): self._advance()
                elif self._peek(1) == '<' and self._peek(2) == '=' and self._peek(3) == '=':
                    self._add_token(TokenType.INJECT_PLUS_LEFT, '+<==')
                    for _ in range(4): self._advance()
                else:
                    self._add_token(TokenType.PLUS, '+')
                    self._advance()
            elif char == '*':
                self._add_token(TokenType.MULTIPLY, '*')
                self._advance()
            elif char == '/':
                # Check for // comment, /* block comment */, /d docstring, or division
                if self._peek(1) == '/':
                    # Single-line comment
                    self._skip_comment()
                elif self._peek(1) == '*':
                    # Block comment /* ... */
                    self._skip_block_comment()
                elif self._peek(1) == 'd' and (self.pos + 2 >= len(self.source) or not self.source[self.pos + 2].isalnum()):
                    # /d docstring comment - skip like a regular comment
                    self._skip_comment()
                else:
                    self._add_token(TokenType.DIVIDE, '/')
                    self._advance()
            elif char == '<':
                self._read_less_than()
            elif char == '>':
                self._read_greater_than()
            elif char == '=':
                self._read_equals()
            elif char == '!':
                self._read_not()
            elif char == '-':
                self._read_minus()
            elif char == '|':
                if self._peek(1) == '|':
                    self._add_token(TokenType.OR, '||')
                    self._advance()
                    self._advance()
                else:
                    # v4.8.4: Single | is pipe operator
                    self._add_token(TokenType.PIPE, '|')
                    self._advance()
            elif char == '~':
                # v4.8.8: Tilde for destructors (constr ~Name())
                self._add_token(TokenType.TILDE, '~')
                self._advance()
            elif char == '^':
                # v4.9.0: Caret for byte notation (1^250, 0^102)
                self._add_token(TokenType.CARET, '^')
                self._advance()
            elif char == '?':
                # v4.9.0: Check if this is ?<name> pointer reference
                next_char = self._peek(1)
                if next_char and (next_char.isalpha() or next_char == '_'):
                    # ?<name> pointer reference
                    self._read_pointer_ref()
                else:
                    # Just ? (ternary operator or other use)
                    self._add_token(TokenType.QUESTION, '?')
                    self._advance()
            else:
                self._advance()

        self._add_token(TokenType.EOF, '')
        return self.tokens

    def _advance(self):
        self.pos += 1
        self.column += 1

    def _peek(self, offset=0) -> str:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return ''

    def _add_token(self, token_type: TokenType, value: Any):
        self.tokens.append(Token(token_type, value, self.line, self.column))

    def _skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos] in ' \t\r':
            self._advance()

    def _skip_comment(self):
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self._advance()

    def _skip_block_comment(self):
        """Skip block comment /* ... */ including nested comments"""
        self._advance()  # skip /
        self._advance()  # skip *
        depth = 1
        while self.pos < len(self.source) and depth > 0:
            if self.source[self.pos] == '/' and self._peek(1) == '*':
                depth += 1
                self._advance()
                self._advance()
            elif self.source[self.pos] == '*' and self._peek(1) == '/':
                depth -= 1
                self._advance()
                self._advance()
            else:
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.column = 0
                self._advance()

    def _read_string(self, quote_char: str):
        self._advance()
        start = self.pos
        result = []
        while self.pos < len(self.source) and self.source[self.pos] != quote_char:
            if self.source[self.pos] == '\\' and self.pos + 1 < len(self.source):
                # Handle escape sequences
                next_char = self.source[self.pos + 1]
                if next_char == 'n':
                    result.append('\n')
                elif next_char == 't':
                    result.append('\t')
                elif next_char == 'r':
                    result.append('\r')
                elif next_char == '\\':
                    result.append('\\')
                elif next_char == quote_char:
                    result.append(quote_char)
                elif next_char == '"':
                    result.append('"')
                elif next_char == "'":
                    result.append("'")
                else:
                    result.append(self.source[self.pos])
                    result.append(next_char)
                self._advance()
                self._advance()
            else:
                result.append(self.source[self.pos])
                self._advance()
        value = ''.join(result)
        self._add_token(TokenType.STRING, value)
        self._advance()

    def _read_raw_string(self):
        """Read raw string with backticks - no escape processing.

        Useful for JSON: `{"id": "2819e1", "name": "test"}`
        """
        self._advance()  # Skip opening backtick
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '`':
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 0
            self._advance()
        value = self.source[start:self.pos]
        self._add_token(TokenType.STRING, value)
        self._advance()  # Skip closing backtick

    def _read_number(self):
        start = self.pos
        if self.source[self.pos] == '-':
            self._advance()

        # Check for hex number: 0x... or 0X...
        if (self.pos < len(self.source) and self.source[self.pos] == '0' and
            self.pos + 1 < len(self.source) and self.source[self.pos + 1] in 'xX'):
            self._advance()  # skip '0'
            self._advance()  # skip 'x' or 'X'
            # Read hex digits
            while self.pos < len(self.source) and self.source[self.pos] in '0123456789abcdefABCDEF':
                self._advance()
            value = self.source[start:self.pos]
            self._add_token(TokenType.NUMBER, int(value, 16))
            return

        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            self._advance()
        value = self.source[start:self.pos]
        if '.' in value:
            self._add_token(TokenType.NUMBER, float(value))
        else:
            self._add_token(TokenType.NUMBER, int(value))

    def _read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()
        value = self.source[start:self.pos]

        # Check for language$instance pattern (v4.1.0)
        # e.g., cpp$MyClass, py$Object, java$Service
        if value.lower() in LANGUAGE_IDS and self.pos < len(self.source) and self.source[self.pos] == '$':
            lang_id = value
            self._advance()  # skip '$'
            # Read instance name
            instance_start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self._advance()
            instance_name = self.source[instance_start:self.pos]
            if instance_name:
                self._add_token(TokenType.LANG_INSTANCE_REF, {'lang': lang_id, 'instance': instance_name})
                return
            # If no instance name, revert and treat as normal identifier
            self.pos = start
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self._advance()
            value = self.source[start:self.pos]

        if value in ('True', 'true'):
            self._add_token(TokenType.BOOLEAN, True)
        elif value in ('False', 'false'):
            self._add_token(TokenType.BOOLEAN, False)
        elif value in ('null', 'None', 'none'):
            self._add_token(TokenType.NULL, None)
        elif value in TYPE_LITERALS:
            # NEW: list and dict as type literals (e.g., cache = list;)
            self._add_token(TokenType.TYPE_LITERAL, value)
        elif value == 'as':
            # NEW: 'as' keyword for foreach ... as ... syntax
            self._add_token(TokenType.AS, value)
        elif value in KEYWORDS:
            # v4.9.2: Check for local:: syntax for hook local variable access
            if value == 'local' and self.pos + 1 < len(self.source) and self.source[self.pos:self.pos+2] == '::':
                self._advance()  # skip first :
                self._advance()  # skip second :
                # Read the local variable/function name
                local_start = self.pos
                while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                    self._advance()
                local_name = self.source[local_start:self.pos]
                if local_name:
                    self._add_token(TokenType.LOCAL_REF, local_name)
                    return
                # If no name, revert to keyword
                self.pos = start + len(value)
            self._add_token(TokenType.KEYWORD, value)
        else:
            self._add_token(TokenType.IDENTIFIER, value)

    def _read_super_function(self):
        """Read #$<name>(...) super-function call for .cssl-pl payloads.

        Super-functions are pre-execution hooks that run when a payload is loaded.
        Valid super-functions: #$run(), #$exec(), #$printl()

        Syntax:
            #$run(initFunction);        // Call a function at load time
            #$exec(setup());            // Execute expression at load time
            #$printl("Payload loaded"); // Print at load time
        """
        start = self.pos
        self._advance()  # skip '#'
        self._advance()  # skip '$'

        # Read the super-function name (run, exec, printl, etc.)
        name_start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()
        func_name = self.source[name_start:self.pos]

        # Store as #$<name> token value
        value = f'#${func_name}'
        self._add_token(TokenType.SUPER_FUNC, value)

    def _read_self_ref(self):
        """Read s@<name> or s@<name>.<member>... self-reference"""
        start = self.pos
        self._advance()  # skip 's'
        self._advance()  # skip '@'

        # Read the identifier path (Name.Member.SubMember)
        path_parts = []
        while self.pos < len(self.source):
            # Read identifier part
            part_start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self._advance()
            if self.pos > part_start:
                path_parts.append(self.source[part_start:self.pos])

            # Check for dot to continue path
            if self.pos < len(self.source) and self.source[self.pos] == '.':
                self._advance()  # skip '.'
            else:
                break

        value = '.'.join(path_parts)
        self._add_token(TokenType.SELF_REF, value)

    def _read_global_ref(self):
        """Read r@<name> global variable declaration (equivalent to 'global')"""
        start = self.pos
        self._advance()  # skip 'r'
        self._advance()  # skip '@'

        # Read the identifier
        name_start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()

        value = self.source[name_start:self.pos]
        self._add_token(TokenType.GLOBAL_REF, value)

    def _read_shared_ref(self):
        """Read $<name> shared object reference"""
        self._advance()  # skip '$'

        # Read the identifier (shared object name)
        name_start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()

        value = self.source[name_start:self.pos]
        if not value:
            self.error("Expected identifier after '$'")
        self._add_token(TokenType.SHARED_REF, value)

    def _read_captured_ref(self):
        """Read %<name> captured reference (captures value at definition time for infusions)"""
        self._advance()  # skip '%'

        # Read the identifier (captured reference name)
        name_start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()

        value = self.source[name_start:self.pos]
        if not value:
            self.error("Expected identifier after '%'")
        self._add_token(TokenType.CAPTURED_REF, value)

    def _read_pointer_ref(self):
        """Read ?<name> pointer reference (v4.9.0) or ?%<name> pointer-snapshot reference (v4.9.4)"""
        self._advance()  # skip '?'

        # v4.9.4: Check for ?%<name> pointer-snapshot reference
        if self.pos < len(self.source) and self.source[self.pos] == '%':
            self._advance()  # skip '%'
            name_start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self._advance()
            value = self.source[name_start:self.pos]
            if not value:
                self.error("Expected identifier after '?%'")
            self._add_token(TokenType.POINTER_SNAPSHOT_REF, value)
            return

        # Read the identifier (pointer reference name)
        name_start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self._advance()

        value = self.source[name_start:self.pos]
        if not value:
            self.error("Expected identifier after '?'")
        self._add_token(TokenType.POINTER_REF, value)

    def _read_less_than(self):
        # Check for <<== (code infusion left)
        if self._peek(1) == '<' and self._peek(2) == '=' and self._peek(3) == '=':
            self._add_token(TokenType.INFUSE_LEFT, '<<==')
            for _ in range(4): self._advance()
        # v4.8.4: Check for << (stream output operator) - but NOT <<==
        elif self._peek(1) == '<' and self._peek(2) != '=':
            self._add_token(TokenType.STREAM_OUT, '<<')
            self._advance()
            self._advance()
        # Check for <== (basic injection left)
        elif self._peek(1) == '=' and self._peek(2) == '=':
            self._add_token(TokenType.INJECT_LEFT, '<==')
            for _ in range(3): self._advance()
        elif self._peek(1) == '=':
            self._add_token(TokenType.COMPARE_LE, '<=')
            self._advance()
            self._advance()
        elif self._peek(1) == '-':
            self._add_token(TokenType.FLOW_LEFT, '<-')
            self._advance()
            self._advance()
        else:
            self._add_token(TokenType.COMPARE_LT, '<')
            self._advance()

    def _read_greater_than(self):
        if self._peek(1) == '=':
            self._add_token(TokenType.COMPARE_GE, '>=')
            self._advance()
            self._advance()
        # v4.8.4: Check for >> (stream input operator)
        elif self._peek(1) == '>':
            self._add_token(TokenType.STREAM_IN, '>>')
            self._advance()
            self._advance()
        else:
            self._add_token(TokenType.COMPARE_GT, '>')
            self._advance()

    def _read_equals(self):
        # Check for ==>>+ (code infusion right plus)
        if self._peek(1) == '=' and self._peek(2) == '>' and self._peek(3) == '>' and self._peek(4) == '+':
            self._add_token(TokenType.INFUSE_PLUS_RIGHT, '==>>+')
            for _ in range(5): self._advance()
        # Check for ==>>- (code infusion right minus)
        elif self._peek(1) == '=' and self._peek(2) == '>' and self._peek(3) == '>' and self._peek(4) == '-':
            self._add_token(TokenType.INFUSE_MINUS_RIGHT, '==>>-')
            for _ in range(5): self._advance()
        # Check for ==>> (code infusion right)
        elif self._peek(1) == '=' and self._peek(2) == '>' and self._peek(3) == '>':
            self._add_token(TokenType.INFUSE_RIGHT, '==>>')
            for _ in range(4): self._advance()
        # Check for ==>+ (injection right plus)
        elif self._peek(1) == '=' and self._peek(2) == '>' and self._peek(3) == '+':
            self._add_token(TokenType.INJECT_PLUS_RIGHT, '==>+')
            for _ in range(4): self._advance()
        # Check for ==>- (injection right minus - moves & removes)
        elif self._peek(1) == '=' and self._peek(2) == '>' and self._peek(3) == '-':
            self._add_token(TokenType.INJECT_MINUS_RIGHT, '==>-')
            for _ in range(4): self._advance()
        # Check for ==> (basic injection right)
        elif self._peek(1) == '=' and self._peek(2) == '>':
            self._add_token(TokenType.INJECT_RIGHT, '==>')
            for _ in range(3): self._advance()
        elif self._peek(1) == '=':
            self._add_token(TokenType.COMPARE_EQ, '==')
            self._advance()
            self._advance()
        else:
            self._add_token(TokenType.EQUALS, '=')
            self._advance()

    def _read_not(self):
        if self._peek(1) == '=':
            self._add_token(TokenType.COMPARE_NE, '!=')
            self._advance()
            self._advance()
        else:
            self._add_token(TokenType.NOT, '!')
            self._advance()

    def _read_minus(self):
        # Check for -<<== (code infusion minus left)
        if self._peek(1) == '<' and self._peek(2) == '<' and self._peek(3) == '=' and self._peek(4) == '=':
            self._add_token(TokenType.INFUSE_MINUS_LEFT, '-<<==')
            for _ in range(5): self._advance()
        # Check for -<== (injection minus left - move & remove)
        elif self._peek(1) == '<' and self._peek(2) == '=' and self._peek(3) == '=':
            self._add_token(TokenType.INJECT_MINUS_LEFT, '-<==')
            for _ in range(4): self._advance()
        # Check for -==> (injection right minus)
        elif self._peek(1) == '=' and self._peek(2) == '=' and self._peek(3) == '>':
            self._add_token(TokenType.INJECT_MINUS_RIGHT, '-==>')
            for _ in range(4): self._advance()
        elif self._peek(1) == '>':
            self._add_token(TokenType.FLOW_RIGHT, '->')
            self._advance()
            self._advance()
        else:
            self._add_token(TokenType.MINUS, '-')
            self._advance()


@dataclass
class ASTNode:
    type: str
    value: Any = None
    children: List['ASTNode'] = field(default_factory=list)
    line: int = 0
    column: int = 0


class CSSLParser:
    """Parses CSSL tokens into an Abstract Syntax Tree."""

    def __init__(self, tokens: List[Token], source_lines: List[str] = None, source: str = None):
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.pos = 0
        self.source_lines = source_lines or []
        self.source = source or '\n'.join(self.source_lines)  # v4.2.0: Full source for raw extraction

    def get_source_line(self, line_num: int) -> str:
        """Get a specific source line for error reporting"""
        if 0 < line_num <= len(self.source_lines):
            return self.source_lines[line_num - 1]
        return ""

    def _skip_to_next_statement(self):
        """Skip tokens until we find a safe synchronization point (next statement boundary).
        Used for error recovery in undefined functions."""
        depth = 0
        while not self._is_at_end():
            tok = self._current()
            if tok.type == TokenType.BLOCK_START:
                depth += 1
            elif tok.type == TokenType.BLOCK_END:
                if depth == 0:
                    return  # Don't consume the closing brace
                depth -= 1
            elif depth == 0 and tok.type == TokenType.SEMICOLON:
                self._advance()  # consume the ;
                return
            self._advance()

    def error(self, message: str, token: Token = None):
        """Raise a syntax error with location info"""
        if token is None:
            token = self._current()
        raise CSSLSyntaxError(
            message,
            line=token.line,
            column=token.column,
            source_line=self.get_source_line(token.line)
        )

    def parse(self) -> ASTNode:
        """Parse a service file (wrapped in braces)"""
        root = ASTNode('service', children=[])

        if not self._match(TokenType.BLOCK_START):
            self.error(f"Expected '{{' at start of service, got {self._current().type.name}")

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._match_keyword('service-init'):
                root.children.append(self._parse_service_init())
            elif self._match_keyword('service-include'):
                root.children.append(self._parse_service_include())
            elif self._match_keyword('service-run'):
                root.children.append(self._parse_service_run())
            # NEW: package block support
            elif self._match_keyword('package'):
                root.children.append(self._parse_package())
            # NEW: package-includes block support
            elif self._match_keyword('package-includes'):
                root.children.append(self._parse_package_includes())
            # NEW: struct at top level
            elif self._match_keyword('struct'):
                root.children.append(self._parse_struct())
            # NEW: define at top level
            elif self._match_keyword('define'):
                root.children.append(self._parse_define())
            else:
                self._advance()

        self._match(TokenType.BLOCK_END)
        return root

    def _is_function_modifier(self, value: str) -> bool:
        """Check if a keyword is a function modifier"""
        return value in FUNCTION_MODIFIERS

    def _is_type_keyword(self, value: str) -> bool:
        """Check if a keyword is a type declaration"""
        return value in ('int', 'string', 'float', 'bool', 'void', 'json', 'array', 'vector', 'stack',
                        'list', 'dictionary', 'dict', 'instance', 'map', 'openquote', 'parameter',
                        'dynamic', 'datastruct', 'dataspace', 'shuffled', 'iterator', 'combo', 'structure',
                        'queue',  # v4.7: Thread-safe queue
                        'bit', 'byte', 'address', 'ptr', 'pointer',  # v4.9.0: Binary types, address, ptr/pointer
                        'auto', 'python')  # v4.9.8: auto type, python:: namespace types

    def _parse_generic_type_content(self) -> str:
        """Parse generic type content including nested generics.

        Handles: <int>, <string, dynamic>, <map<string, dynamic>>, etc.
        Returns the full type string including nested generics.

        Called AFTER consuming the opening '<'.
        """
        parts = []
        depth = 1  # Already inside first <

        while depth > 0 and not self._is_at_end():
            if self._check(TokenType.COMPARE_LT):
                parts.append('<')
                depth += 1
                self._advance()
            elif self._check(TokenType.COMPARE_GT):
                depth -= 1
                if depth > 0:  # Only add > if not the final closing >
                    parts.append('>')
                self._advance()
            # v4.9.4: Handle >> token (STREAM_IN) for nested generics like array<map<K,V>>
            elif self._check(TokenType.STREAM_IN):
                # >> is two > characters - handle both
                # First > closes one level
                depth -= 1
                if depth > 0:
                    parts.append('>')
                # Second > closes another level
                depth -= 1
                if depth > 0:
                    parts.append('>')
                self._advance()
            elif self._check(TokenType.COMMA):
                parts.append(', ')
                self._advance()
            elif self._check(TokenType.KEYWORD) or self._check(TokenType.IDENTIFIER):
                parts.append(self._advance().value)
            elif self._check(TokenType.NUMBER):
                # v4.7: For queue<type, size> where size is a number
                parts.append(str(int(self._advance().value)))
            elif self._check(TokenType.STRING):
                # For instance<"name">
                parts.append(f'"{self._advance().value}"')
            else:
                # Skip whitespace/other tokens
                self._advance()

        return ''.join(parts)

    def _looks_like_function_declaration(self) -> bool:
        """Check if current position looks like a C-style function declaration.

        Supports flexible ordering of modifiers, types, non-null (*), and global (@):

        Patterns:
        - int funcName(...)
        - undefined int funcName(...)
        - vector<string> funcName(...)
        - undefined void funcName(...)
        - private super virtual meta FuncName(...)
        - private string *@Myfunc(...)
        - const define myFunc(...)
        - global private const void @Func(...)
        - shuffled *[string] getNumbers(...)
        - datastruct<dynamic> HelloCode(...)
        - datastruct<dynamic> HelloCode() : extends @MyFunc { }

        Distinguishes functions from variables:
        - datastruct<dynamic> MyVar;           <- variable (no () { })
        - datastruct<dynamic> HelloCode() { }  <- function (has () { })
        """
        saved_pos = self.pos
        has_modifiers = False
        has_type = False

        try:
            # Skip modifiers in any order (global, private, const, undefined, etc.)
            while self._check(TokenType.KEYWORD) and self._is_function_modifier(self._current().value):
                self._advance()
                has_modifiers = True

            # Check for 'define' keyword (special case: const define myFunc())
            if self._check(TokenType.KEYWORD) and self._current().value == 'define':
                self.pos = saved_pos
                return False  # Let _parse_define handle this

            # Check for type keyword (int, string, void, vector, datastruct, etc.)
            # v4.8: Also handle TYPE_LITERAL (dict, list) and custom class types (IDENTIFIER)
            if (self._check(TokenType.KEYWORD) and self._is_type_keyword(self._current().value)) or \
               self._check(TokenType.TYPE_LITERAL):
                self._advance()
                has_type = True
                # v4.9.8: Skip python::type composite (3 tokens)
                if self._check(TokenType.DOUBLE_COLON):
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                        self._advance()

                # Skip generic type parameters <T> or <T, U>
                if self._check(TokenType.COMPARE_LT):
                    depth = 1
                    self._advance()
                    while depth > 0 and not self._is_at_end():
                        if self._check(TokenType.COMPARE_LT):
                            depth += 1
                        elif self._check(TokenType.COMPARE_GT):
                            depth -= 1
                        self._advance()

            # v4.8: Check for custom class type (IDENTIFIER followed by another IDENTIFIER)
            # Pattern: CustomClass funcName() { } where CustomClass is a user-defined class
            elif self._check(TokenType.IDENTIFIER):
                # Save position and check if this is "Type Name(" pattern
                inner_saved = self.pos
                self._advance()  # Skip potential type

                # Skip generic type parameters if present
                if self._check(TokenType.COMPARE_LT):
                    depth = 1
                    self._advance()
                    while depth > 0 and not self._is_at_end():
                        if self._check(TokenType.COMPARE_LT):
                            depth += 1
                        elif self._check(TokenType.COMPARE_GT):
                            depth -= 1
                        self._advance()

                # Check if followed by another identifier (function name)
                if self._check(TokenType.IDENTIFIER):
                    # v4.9.9: For custom class types, verify this is actually a function
                    # declaration by scanning past params to check for { or :
                    # This prevents "leftover_var printl(...)" from being misread as
                    # "CustomType funcName(...)" after expression parsing
                    verify_pos = self.pos
                    self._advance()  # skip function name
                    if self._check(TokenType.PAREN_START):
                        self._advance()  # skip (
                        paren_depth = 1
                        while paren_depth > 0 and not self._is_at_end():
                            if self._check(TokenType.PAREN_START):
                                paren_depth += 1
                            elif self._check(TokenType.PAREN_END):
                                paren_depth -= 1
                            self._advance()
                        # After ), must see { or : for a real declaration
                        if self._check(TokenType.BLOCK_START) or self._check(TokenType.COLON):
                            has_type = True
                        # else: not a real declaration, fall through
                    self.pos = verify_pos
                    if not has_type:
                        self.pos = inner_saved
                else:
                    # Not a "Type Name" pattern, restore position
                    self.pos = inner_saved

            # Check for * prefix (non-null) or *[type] (type exclusion)
            if self._check(TokenType.MULTIPLY):
                self._advance()
                # Check for type exclusion: *[string], *[int], etc.
                if self._check(TokenType.BRACKET_START):
                    self._advance()  # [
                    while not self._check(TokenType.BRACKET_END) and not self._is_at_end():
                        self._advance()
                    if self._check(TokenType.BRACKET_END):
                        self._advance()  # ]

            # Check for @ prefix (global function)
            if self._check(TokenType.AT):
                self._advance()

            # Now we should be at the function name (identifier)
            if self._check(TokenType.IDENTIFIER):
                self._advance()

                # Check if followed by (
                # IMPORTANT: Only a function declaration if we have modifiers OR type
                # Plain identifier() is a function CALL, not a declaration
                if self._check(TokenType.PAREN_START):
                    if has_modifiers or has_type:
                        self.pos = saved_pos
                        return True
                    else:
                        # No modifiers/type = function call, not declaration
                        self.pos = saved_pos
                        return False

                # If we have a type and identifier but no (, it's a variable
                if has_type and not self._check(TokenType.PAREN_START):
                    self.pos = saved_pos
                    return False

            self.pos = saved_pos
            return False

        except Exception:
            self.pos = saved_pos
            return False

    def _looks_like_typed_variable(self) -> bool:
        """Check if current position looks like a typed variable declaration.

        Patterns:
        - int x;
        - stack<string> myStack;
        - vector<int> nums = [1,2,3];
        - list<int> myList;  (v4.8.7: list/dict are TYPE_LITERAL tokens)

        Distinguishes from function declarations by checking for '(' after identifier.
        """
        saved_pos = self.pos

        # Check for type keyword
        # v4.8.7: Also check TYPE_LITERAL (list, dict) which are tokenized differently
        is_type_token = ((self._check(TokenType.KEYWORD) and self._is_type_keyword(self._current().value)) or
                         (self._check(TokenType.TYPE_LITERAL) and self._current().value in ('list', 'dict')))
        if is_type_token:
            self._advance()
            # v4.9.8: Skip python::type composite
            if self._check(TokenType.DOUBLE_COLON):
                self._advance()
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                    self._advance()

            # Skip generic type parameters <T>
            if self._check(TokenType.COMPARE_LT):
                depth = 1
                self._advance()
                while depth > 0 and not self._is_at_end():
                    if self._check(TokenType.COMPARE_LT):
                        depth += 1
                    elif self._check(TokenType.COMPARE_GT):
                        depth -= 1
                    self._advance()

            # Check for identifier NOT followed by ( (that would be a function)
            # v4.9.4: Also accept 'this' keyword for class member declarations like: ptr this->member = value
            if self._check(TokenType.IDENTIFIER) or (self._check(TokenType.KEYWORD) and self._current().value == 'this'):
                self._advance()
                # If followed by '(' it's a function, not a variable
                is_var = not self._check(TokenType.PAREN_START)
                self.pos = saved_pos
                return is_var

        self.pos = saved_pos
        return False

    def _parse_typed_function(self, is_global: bool = False, is_embedded: bool = False, modifiers: list = None) -> ASTNode:
        """Parse C-style typed function declaration with flexible modifier ordering.

        Supports any order of modifiers, types, non-null (*), and global (@):

        Patterns:
        - int Add(int a, int b) { }
        - global int Add(int a, int b) { }
        - int @Add(int a, int b) { }
        - undefined int Func() { }
        - open void Handler(open Params) { }
        - vector<string> GetNames() { }
        - private string *@Myfunc() { }
        - const define myFunc() { }
        - global private const void @Func() { }
        - shuffled *[string] getNumbers() { }
        - datastruct<dynamic> HelloCode() { }
        - meta datastruct<string> MyData() { }  // meta allows any returns
        - datastruct<dynamic> HelloCode() : extends @MyFunc { }

        Typed functions (with return type like int, string, void) MUST return that type.
        Functions with 'meta' modifier can return any type regardless of declaration.
        Functions with 'define' are dynamic (any return type allowed).
        """
        modifiers = modifiers if modifiers is not None else []
        return_type = None
        generic_type = None
        non_null = False
        exclude_type = None
        is_const = False
        # v4.2.5: embedded = immediate &target replacement (can come from param or modifier)
        _is_embedded = is_embedded

        # Phase 1: Collect all modifiers, type, non-null, and global indicators
        # These can appear in any order before the function name

        parsing_prefix = True
        while parsing_prefix and not self._is_at_end():
            # Check for modifiers (global, private, const, undefined, etc.)
            if self._check(TokenType.KEYWORD) and self._is_function_modifier(self._current().value):
                mod = self._advance().value
                if mod == 'global':
                    is_global = True
                elif mod == 'const':
                    is_const = True
                    modifiers.append(mod)
                elif mod == 'embedded':
                    _is_embedded = True
                    modifiers.append(mod)
                else:
                    modifiers.append(mod)
                continue

            # Check for type keyword (int, string, void, vector, datastruct, etc.)
            # v4.8: Also handle TYPE_LITERAL (dict, list) as return types
            if ((self._check(TokenType.KEYWORD) and self._is_type_keyword(self._current().value)) or
                self._check(TokenType.TYPE_LITERAL)) and return_type is None:
                return_type = self._advance().value
                # v4.9.8: Handle python::type composite return types
                if return_type == 'python' and self._check(TokenType.DOUBLE_COLON):
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                        return_type = 'python::' + self._advance().value
                    else:
                        return_type = 'python::object'

                # Check for generic type <T> or <T, U>
                if self._check(TokenType.COMPARE_LT):
                    self._advance()  # skip <
                    generic_parts = []
                    depth = 1
                    while depth > 0 and not self._is_at_end():
                        if self._check(TokenType.COMPARE_LT):
                            depth += 1
                            generic_parts.append('<')
                        elif self._check(TokenType.COMPARE_GT):
                            depth -= 1
                            if depth > 0:
                                generic_parts.append('>')
                        elif self._check(TokenType.COMMA):
                            generic_parts.append(',')
                        else:
                            generic_parts.append(str(self._current().value))
                        self._advance()
                    generic_type = ''.join(generic_parts)
                continue

            # v4.8: Check for custom class type as return type (IDENTIFIER followed by another IDENTIFIER)
            # Pattern: CustomClass funcName() { } where CustomClass is a user-defined class
            if self._check(TokenType.IDENTIFIER) and return_type is None:
                # Look ahead to see if this is "Type Name(" pattern
                saved_inner = self.pos
                potential_type = self._advance().value

                # Skip generic type parameters if present
                if self._check(TokenType.COMPARE_LT):
                    self._advance()
                    depth = 1
                    while depth > 0 and not self._is_at_end():
                        if self._check(TokenType.COMPARE_LT):
                            depth += 1
                        elif self._check(TokenType.COMPARE_GT):
                            depth -= 1
                        self._advance()

                # Check if followed by another identifier (function name)
                if self._check(TokenType.IDENTIFIER):
                    return_type = potential_type
                    continue
                else:
                    # Not a "Type Name" pattern, restore position
                    self.pos = saved_inner

            # Check for * prefix (non-null) or *[type] (type exclusion)
            if self._check(TokenType.MULTIPLY):
                self._advance()
                # Check for type exclusion filter: *[string], *[int], etc.
                if self._check(TokenType.BRACKET_START):
                    self._advance()  # consume [
                    exclude_type = self._advance().value  # get type name
                    self._expect(TokenType.BRACKET_END)
                else:
                    non_null = True
                continue

            # Check for @ prefix (global function)
            if self._check(TokenType.AT):
                self._advance()
                is_global = True
                continue

            # If we've reached an identifier, we're at the function name
            if self._check(TokenType.IDENTIFIER):
                parsing_prefix = False
            else:
                # Unknown token in prefix, break out
                parsing_prefix = False

        # Phase 2: Get function name
        if not self._check(TokenType.IDENTIFIER):
            self.error(f"Expected function name, got {self._current().type.name}")
        name_token = self._advance()
        name = name_token.value
        func_line = name_token.line
        func_column = name_token.column

        # Phase 3: Parse parameters
        params = []
        self._expect(TokenType.PAREN_START)

        while not self._check(TokenType.PAREN_END) and not self._is_at_end():
            param_info = {}

            # Handle 'open' keyword for open parameters
            if self._match_keyword('open'):
                param_info['open'] = True

            # Handle const parameters
            if self._match_keyword('const'):
                param_info['const'] = True

            # Handle type annotations (builtin types like int, string, etc.)
            # v4.8: Also handle TYPE_LITERAL (dict, list) which are tokenized differently
            if (self._check(TokenType.KEYWORD) and self._is_type_keyword(self._current().value)) or \
               self._check(TokenType.TYPE_LITERAL):
                type_val = self._advance().value
                # v4.9.8: Handle python::type composite types
                if type_val == 'python' and self._check(TokenType.DOUBLE_COLON):
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                        type_val = 'python::' + self._advance().value
                    else:
                        type_val = 'python::object'
                param_info['type'] = type_val

                # Check for generic type parameter <T>
                if self._check(TokenType.COMPARE_LT):
                    self._advance()
                    generic_parts = []
                    depth = 1
                    while depth > 0 and not self._is_at_end():
                        if self._check(TokenType.COMPARE_LT):
                            depth += 1
                            generic_parts.append('<')
                        elif self._check(TokenType.COMPARE_GT):
                            depth -= 1
                            if depth > 0:
                                generic_parts.append('>')
                        elif self._check(TokenType.COMMA):
                            generic_parts.append(',')
                        else:
                            generic_parts.append(str(self._current().value))
                        self._advance()
                    param_info['generic'] = ''.join(generic_parts)

            # Handle custom class types (identifier followed by another identifier = type + name)
            elif self._check(TokenType.IDENTIFIER):
                saved_pos = self.pos
                potential_type = self._advance().value

                # Check for generic type parameter <T> on custom type
                if self._check(TokenType.COMPARE_LT):
                    self._advance()
                    generic_parts = []
                    depth = 1
                    while depth > 0 and not self._is_at_end():
                        if self._check(TokenType.COMPARE_LT):
                            depth += 1
                            generic_parts.append('<')
                        elif self._check(TokenType.COMPARE_GT):
                            depth -= 1
                            if depth > 0:
                                generic_parts.append('>')
                        elif self._check(TokenType.COMMA):
                            generic_parts.append(',')
                        else:
                            generic_parts.append(str(self._current().value))
                        self._advance()
                    param_info['generic'] = ''.join(generic_parts)

                # If followed by identifier, this is "Type name" pattern
                if self._check(TokenType.IDENTIFIER):
                    param_info['type'] = potential_type
                else:
                    # Not a type, restore position - this is just a param name
                    self.pos = saved_pos

            # Handle * prefix for non-null parameters
            if self._match(TokenType.MULTIPLY):
                param_info['non_null'] = True

            # Handle reference operator &
            if self._match(TokenType.AMPERSAND):
                param_info['ref'] = True

            # Get parameter name
            if self._check(TokenType.IDENTIFIER):
                param_name = self._advance().value
                if param_info:
                    params.append({'name': param_name, **param_info})
                else:
                    params.append(param_name)
            elif self._check(TokenType.KEYWORD):
                # Parameter name could be a keyword like 'Params'
                param_name = self._advance().value
                if param_info:
                    params.append({'name': param_name, **param_info})
                else:
                    params.append(param_name)

            self._match(TokenType.COMMA)

        self._expect(TokenType.PAREN_END)

        # Phase 4: Check for extends/overwrites and append mode
        extends_func = None
        extends_is_python = False
        extends_class_ref = None
        extends_method_ref = None
        overwrites_func = None
        overwrites_is_python = False
        overwrites_class_ref = None
        overwrites_method_ref = None
        append_mode = False
        append_ref_class = None
        append_ref_member = None

        # Check for &ClassName::member or &ClassName.member or &function reference
        if self._match(TokenType.AMPERSAND):
            if self._check(TokenType.IDENTIFIER):
                append_ref_class = self._advance().value
            elif self._check(TokenType.AT):
                self._advance()
                if self._check(TokenType.IDENTIFIER):
                    append_ref_class = '@' + self._advance().value
            elif self._check(TokenType.SHARED_REF):
                append_ref_class = f'${self._advance().value}'

            # Check for ::member or .member (support both syntaxes)
            if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.DOT):
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                    append_ref_member = self._advance().value

        # Check for ++ append operator
        if self._match(TokenType.PLUS_PLUS):
            append_mode = True

        # Check for : or :: extends/overwrites
        if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON):
            while True:
                if self._match_keyword('extends'):
                    # Parse target: @ModuleName, $PythonObject, Parent::method, Parent.method
                    if self._check(TokenType.AT):
                        self._advance()
                        extends_func = '@' + self._advance().value
                    elif self._check(TokenType.SHARED_REF):
                        extends_is_python = True
                        extends_func = self._advance().value
                    elif self._check(TokenType.IDENTIFIER):
                        first_part = self._advance().value
                        # Support both :: and . for class method access
                        if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.DOT):
                            extends_class_ref = first_part
                            extends_method_ref = self._advance().value
                        else:
                            extends_func = first_part
                    # Skip optional ()
                    if self._match(TokenType.PAREN_START):
                        self._expect(TokenType.PAREN_END)
                elif self._match_keyword('overwrites'):
                    if self._check(TokenType.AT):
                        self._advance()
                        overwrites_func = '@' + self._advance().value
                    elif self._check(TokenType.SHARED_REF):
                        overwrites_is_python = True
                        overwrites_func = self._advance().value
                    elif self._check(TokenType.IDENTIFIER):
                        first_part = self._advance().value
                        # Support both :: and . for class method access
                        if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.DOT):
                            overwrites_class_ref = first_part
                            overwrites_method_ref = self._advance().value
                        else:
                            overwrites_func = first_part
                    if self._match(TokenType.PAREN_START):
                        self._expect(TokenType.PAREN_END)
                else:
                    break
                if not (self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON)):
                    break

        # Phase 5: Parse function body
        node = ASTNode('function', value={
            'name': name,
            'is_global': is_global,
            'is_const': is_const,
            'is_embedded': _is_embedded,  # v4.2.5: immediate &target replacement
            'params': params,
            'return_type': return_type,
            'generic_type': generic_type,
            'modifiers': modifiers,
            'non_null': non_null,
            'exclude_type': exclude_type,
            'extends': extends_func,
            'extends_is_python': extends_is_python,
            'extends_class': extends_class_ref,
            'extends_method': extends_method_ref,
            'overwrites': overwrites_func,
            'overwrites_is_python': overwrites_is_python,
            'overwrites_class': overwrites_class_ref,
            'overwrites_method': overwrites_method_ref,
            'append_mode': append_mode,
            'append_ref_class': append_ref_class,
            'append_ref_member': append_ref_member,
            # v4.3.2: Also disable strict return type enforcement for 'shuffled' modifier (returns tuple)
            'enforce_return_type': return_type is not None and 'meta' not in modifiers and 'shuffled' not in modifiers and return_type != 'shuffled'
        }, children=[], line=func_line, column=func_column)

        self._expect(TokenType.BLOCK_START)

        is_undefined = 'undefined' in modifiers
        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if is_undefined:
                try:
                    stmt = self._parse_statement()
                    if stmt:
                        node.children.append(stmt)
                except (CSSLSyntaxError, Exception):
                    self._skip_to_next_statement()
            else:
                stmt = self._parse_statement()
                if stmt:
                    node.children.append(stmt)

        self._expect(TokenType.BLOCK_END)
        return node

    def _looks_like_namespace_call(self) -> bool:
        """Check if current position looks like a namespace function call.

        Pattern: keyword::identifier(...) like json::write(), string::cut()
        This allows type keywords to be used as namespace prefixes for function calls.
        """
        if not self._check(TokenType.KEYWORD):
            return False

        # Save position
        saved_pos = self.pos

        self._advance()  # Skip keyword

        # Must be followed by ::
        result = self._check(TokenType.DOUBLE_COLON)

        # Restore position
        self.pos = saved_pos
        return result

    def _looks_like_typed_variable(self) -> bool:
        """Check if current position looks like a typed variable declaration:
        type_name varName; or type_name<T> varName; or type_name varName = value;
        v4.9.4: Also supports local/static modifiers: local int x; static array<int> arr;
        """
        # Save position
        saved_pos = self.pos

        # v4.9.4: Skip optional local/static/freezed modifiers
        var_modifiers = {'local', 'static', 'freezed'}
        while self._check(TokenType.KEYWORD) and self._current().value in var_modifiers:
            self._advance()

        # Must start with a type keyword (int, string, stack, vector, etc.)
        # v4.8.7: Also check TYPE_LITERAL (list, dict) which are tokenized differently
        if not self._check(TokenType.KEYWORD) and not self._check(TokenType.TYPE_LITERAL):
            self.pos = saved_pos
            return False

        type_name = self._current().value

        # Skip known type keywords
        type_keywords = {'int', 'string', 'float', 'bool', 'dynamic', 'void',
                        'stack', 'vector', 'datastruct', 'dataspace', 'shuffled',
                        'iterator', 'combo', 'array', 'openquote', 'json',
                        'list', 'dictionary', 'dict', 'instance', 'map',
                        'queue',  # v4.7: Added queue
                        'bit', 'byte', 'address', 'ptr', 'pointer',  # v4.9.0: Binary types, address, ptr/pointer
                        'auto', 'python'}  # v4.9.8: auto type, python:: namespace types
        if type_name not in type_keywords:
            self.pos = saved_pos
            return False

        self._advance()
        # v4.9.8: Skip python::type composite (3 tokens)
        if type_name == 'python' and self._check(TokenType.DOUBLE_COLON):
            self._advance()
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                self._advance()

        # Check for optional generic <T>
        if self._match(TokenType.COMPARE_LT):
            # Skip until > - handle nested generics and >> token
            depth = 1
            while depth > 0 and not self._is_at_end():
                if self._check(TokenType.COMPARE_LT):
                    depth += 1
                elif self._check(TokenType.COMPARE_GT):
                    depth -= 1
                # v4.9.4: Handle >> token (STREAM_IN) which is two > characters
                # This happens with nested generics like array<map<K,V>>
                elif self._check(TokenType.STREAM_IN):
                    depth -= 2
                self._advance()

        # v4.8.6: Check for @ prefix (global variable marker)
        if self._check(TokenType.AT):
            self._advance()

        # Next should be an identifier (variable name) or 'this' (for this->member), not '(' (function) or ';'
        # v4.9.4: Also accept 'this' keyword for class member declarations like: ptr this->member = value
        result = self._check(TokenType.IDENTIFIER) or (self._check(TokenType.KEYWORD) and self._current().value == 'this')

        # Restore position
        self.pos = saved_pos
        return result

    def _parse_typed_variable(self) -> Optional[ASTNode]:
        """Parse a typed variable declaration: type varName; or type<T> *varName = value;

        The * prefix indicates a non-nullable variable (can never be None/null).
        Example: vector<dynamic> *MyVector - can never contain None values.
        Supports nested generics: datastruct<map<string, dynamic>> zipped;

        v4.9.4: Supports local/static modifiers:
        - local: cannot be accessed via @varName (global ref), can be snapshotted via %varName
        - static: can be accessed via @varName, cannot be snapshotted via %varName
        - local static: forbids both @ and % access
        - freezed: creates immutable variable (cannot be reassigned or modified)
        """
        # v4.9.4: Parse optional local/static/freezed modifiers
        is_local = False
        is_static = False
        is_freezed = False
        var_modifiers = {'local', 'static', 'freezed'}
        while self._check(TokenType.KEYWORD) and self._current().value in var_modifiers:
            mod = self._advance().value
            if mod == 'local':
                is_local = True
            elif mod == 'static':
                is_static = True
            elif mod == 'freezed':
                is_freezed = True

        # Get type name
        type_token = self._advance()  # Consume type keyword
        type_name = type_token.value
        decl_line = type_token.line
        decl_column = type_token.column

        # Check for generic type <T> or instance<"name"> or nested <map<K,V>>
        element_type = None
        if self._match(TokenType.COMPARE_LT):
            # Use helper to parse nested generic content
            element_type = self._parse_generic_type_content()

        # Check for * prefix (non-nullable indicator)
        non_null = False
        if self._match(TokenType.MULTIPLY):
            non_null = True

        # v4.8.6: Check for @ prefix (global variable marker)
        is_global_ref = False
        if self._match(TokenType.AT):
            is_global_ref = True

        # Get variable name - can be identifier or this->member
        # v4.9.2: Support this->member syntax for class member declarations
        is_this_member = False
        if self._check(TokenType.KEYWORD) and self._current().value == 'this':
            self._advance()  # consume 'this'
            if self._match(TokenType.FLOW_RIGHT):
                if self._check(TokenType.IDENTIFIER):
                    var_name = self._advance().value
                    is_this_member = True
                else:
                    return None
            else:
                return None
        elif not self._check(TokenType.IDENTIFIER):
            return None
        else:
            var_name = self._advance().value

        # v4.8.6: Store @ prefix in var_name for global reference
        if is_global_ref:
            var_name = '@' + var_name

        # Check for assignment or just declaration
        value = None
        if self._match(TokenType.EQUALS):
            value = self._parse_expression()

        self._match(TokenType.SEMICOLON)

        # For instance<"name">, create a special UniversalInstance node
        # But for plain "instance varName", treat as regular type annotation (like dynamic)
        if type_name == 'instance' and element_type:
            # instance<"containerName"> - creates/gets UniversalInstance
            return ASTNode('instance_declaration', value={
                'instance_name': element_type,
                'name': var_name,
                'value': value,
                'non_null': non_null,
                'is_local': is_local,    # v4.9.4: Cannot be accessed via @varName
                'is_static': is_static,  # v4.9.4: Cannot be snapshotted via %varName
                'is_freezed': is_freezed # v4.9.4: Immutable - cannot be reassigned
            })
        # v4.8.8: Plain "instance varName = new Class()" is a type annotation
        # allowing any CSSLInstance to be stored (like dynamic but for objects)

        # v4.7: For queue<type, size>, extract size from element_type string
        queue_size = 'dynamic'
        if type_name == 'queue' and element_type and ', ' in element_type:
            parts = element_type.split(', ', 1)
            element_type = parts[0].strip()
            size_str = parts[1].strip()
            if size_str.isdigit():
                queue_size = int(size_str)
            else:
                queue_size = size_str  # 'dynamic' or other

        return ASTNode('typed_declaration', value={
            'type': type_name,
            'element_type': element_type,
            'name': var_name,
            'value': value,
            'non_null': non_null,
            'size': queue_size,  # v4.7: For queue<T, size>
            'is_this_member': is_this_member,  # v4.9.2: this->member declaration
            'is_local': is_local,    # v4.9.4: Cannot be accessed via @varName
            'is_static': is_static,  # v4.9.4: Cannot be snapshotted via %varName
            'is_freezed': is_freezed # v4.9.4: Immutable - cannot be reassigned
        }, line=decl_line, column=decl_column)

    def parse_program(self) -> ASTNode:
        """Parse a standalone program (no service wrapper)"""
        root = ASTNode('program', children=[])

        while not self._is_at_end():
            if self._match_keyword('struct'):
                root.children.append(self._parse_struct())
            elif self._match_keyword('class'):
                root.children.append(self._parse_class())
            elif self._match_keyword('namespace'):
                root.children.append(self._parse_namespace())
            elif self._match_keyword('enum'):
                root.children.append(self._parse_enum())
            # v4.7: bytearrayed can be a modifier (bytearrayed define) or standalone block
            elif self._check(TokenType.KEYWORD) and self._current().value == 'bytearrayed':
                # Peek ahead: if next token is 'define', treat as modifier and handle in-place
                next_tok = self._peek(1)
                if next_tok.type == TokenType.KEYWORD and next_tok.value == 'define':
                    # Handle bytearrayed define directly
                    self._advance()  # consume 'bytearrayed'
                    self._advance()  # consume 'define'
                    root.children.append(self._parse_define(modifiers=['bytearrayed']))
                else:
                    self._advance()  # consume 'bytearrayed'
                    root.children.append(self._parse_bytearrayed())
            elif self._match_keyword('define'):
                root.children.append(self._parse_define())
            # v4.5.1: Handle function modifiers (private, const, static, etc.) before define
            elif self._check(TokenType.KEYWORD) and self._is_function_modifier(self._current().value):
                modifiers = []
                is_embedded = False
                is_global = False
                has_open_params = False
                while self._check(TokenType.KEYWORD) and self._is_function_modifier(self._current().value):
                    mod = self._advance().value
                    modifiers.append(mod)
                    if mod == 'embedded':
                        is_embedded = True
                    elif mod == 'global':
                        is_global = True
                    elif mod == 'open':
                        has_open_params = True
                # Now check what follows
                if self._match_keyword('define'):
                    root.children.append(self._parse_define(
                        is_global=is_global, is_embedded=is_embedded,
                        has_open_params=has_open_params, modifiers=modifiers
                    ))
                elif self._match_keyword('class'):
                    # v4.8.6: Support 'global class @ClassName' syntax
                    root.children.append(self._parse_class(is_global=is_global, is_embedded=is_embedded))
                elif self._looks_like_function_declaration():
                    root.children.append(self._parse_typed_function(modifiers=modifiers))
                elif self._looks_like_typed_variable():
                    # v4.8.6: Support 'global int @varname = value' syntax
                    decl = self._parse_typed_variable()
                    if decl and isinstance(decl.value, dict):
                        # v4.9.8: Apply consumed modifiers to the typed declaration
                        if 'static' in modifiers:
                            decl.value['is_static'] = True
                        if 'local' in [m for m in modifiers if m == 'local']:
                            decl.value['is_local'] = True
                        if 'freezed' in modifiers:
                            decl.value['is_freezed'] = True
                    if decl and is_global:
                        # Wrap in global_assignment to mark as global variable
                        global_stmt = ASTNode('global_assignment', value=decl)
                        root.children.append(global_stmt)
                    elif decl:
                        root.children.append(decl)
                elif is_global:
                    # v4.8.6: Handle 'global @varname = value' or 'global varname = value'
                    stmt = self._parse_expression_statement()
                    if stmt:
                        global_stmt = ASTNode('global_assignment', value=stmt)
                        root.children.append(global_stmt)
                else:
                    self.error(f"Expected 'define', 'class', function, or variable declaration after modifiers: {modifiers}")
            # Check for C-style typed function declarations
            elif self._looks_like_function_declaration():
                root.children.append(self._parse_typed_function())
            # Check for typed variable declarations (int x;, stack<string> s;)
            elif self._looks_like_typed_variable():
                decl = self._parse_typed_variable()
                if decl:
                    root.children.append(decl)
            # Handle service blocks
            elif self._match_keyword('service-init'):
                root.children.append(self._parse_service_init())
            elif self._match_keyword('service-include'):
                root.children.append(self._parse_service_include())
            elif self._match_keyword('service-run'):
                root.children.append(self._parse_service_run())
            elif self._match_keyword('package'):
                root.children.append(self._parse_package())
            elif self._match_keyword('package-includes'):
                root.children.append(self._parse_package_includes())
            # Handle global declarations
            # v4.2.5: Handle 'embedded' keyword for immediate &target replacement
            # v4.3.2: Extended to support enums: embedded EnumName &TargetEnum { ... }
            # v4.3.2: Support 'open embedded define' syntax
            elif self._match_keyword('open'):
                # open can be followed by embedded or define
                if self._match_keyword('embedded'):
                    if self._match_keyword('define'):
                        root.children.append(self._parse_define(is_embedded=True, has_open_params=True))
                    elif self._looks_like_function_declaration():
                        root.children.append(self._parse_typed_function(is_embedded=True, has_open_params=True))
                    else:
                        self.error("Expected 'define' or function declaration after 'open embedded'")
                elif self._match_keyword('define'):
                    root.children.append(self._parse_define(has_open_params=True))
                else:
                    self.error("Expected 'embedded' or 'define' after 'open'")
            elif self._match_keyword('embedded'):
                # v4.3.2: Support both 'embedded open define' and 'embedded define'
                if self._match_keyword('open'):
                    # embedded open define ...
                    if self._match_keyword('define'):
                        root.children.append(self._parse_define(is_embedded=True, has_open_params=True))
                    elif self._looks_like_function_declaration():
                        root.children.append(self._parse_typed_function(is_embedded=True, has_open_params=True))
                    else:
                        self.error("Expected 'define' or function declaration after 'embedded open'")
                elif self._match_keyword('class'):
                    root.children.append(self._parse_class(is_embedded=True))
                elif self._match_keyword('enum'):
                    root.children.append(self._parse_enum(is_embedded=True))
                elif self._match_keyword('define'):
                    root.children.append(self._parse_define(is_embedded=True))
                elif self._looks_like_function_declaration():
                    root.children.append(self._parse_typed_function(is_embedded=True))
                elif self._check(TokenType.IDENTIFIER):
                    # embedded Name &Target { ... } - could be enum override
                    root.children.append(self._parse_embedded_override())
                else:
                    self.error("Expected 'class', 'enum', 'open', 'define', function declaration, or identifier after 'embedded'")
            elif self._match_keyword('global'):
                # Check if followed by class or define (global class/function)
                if self._match_keyword('class'):
                    root.children.append(self._parse_class(is_global=True))
                elif self._match_keyword('define'):
                    root.children.append(self._parse_define(is_global=True))
                elif self._looks_like_function_declaration():
                    # global void MyFunc() { } or global int MyFunc() { }
                    root.children.append(self._parse_typed_function(is_global=True))
                else:
                    stmt = self._parse_expression_statement()
                    if stmt:
                        # Wrap in global_assignment to mark as global variable
                        global_stmt = ASTNode('global_assignment', value=stmt)
                        root.children.append(global_stmt)
            elif self._check(TokenType.GLOBAL_REF):
                stmt = self._parse_expression_statement()
                if stmt:
                    # Wrap in global_assignment to mark as global variable (same as 'global' keyword)
                    global_stmt = ASTNode('global_assignment', value=stmt)
                    root.children.append(global_stmt)
            # Control flow keywords must be checked BEFORE generic KEYWORD handling
            elif self._match_keyword('if'):
                root.children.append(self._parse_if())
            elif self._match_keyword('while'):
                root.children.append(self._parse_while())
            elif self._match_keyword('for'):
                root.children.append(self._parse_for())
            elif self._match_keyword('foreach'):
                root.children.append(self._parse_foreach())
            # v4.3.2: Add try/catch and switch at top-level
            elif self._match_keyword('try'):
                root.children.append(self._parse_try())
            elif self._match_keyword('switch'):
                root.children.append(self._parse_switch())
            # Handle statements - keywords like 'instance', 'list', 'map' can be variable names
            # v4.2.1: Added LANG_INSTANCE_REF for lang$instance statements (js$GameData.score = 1337)
            # v4.8.8: Added CAPTURED_REF for %snapshot(args) function calls
            # v4.9.0: Added POINTER_REF for ?name = value pointer assignments
            elif (self._check(TokenType.IDENTIFIER) or self._check(TokenType.AT) or
                  self._check(TokenType.SELF_REF) or self._check(TokenType.SHARED_REF) or
                  self._check(TokenType.KEYWORD) or self._check(TokenType.LANG_INSTANCE_REF) or
                  self._check(TokenType.CAPTURED_REF) or self._check(TokenType.POINTER_REF) or
                  self._check(TokenType.POINTER_SNAPSHOT_REF) or
                  self._check(TokenType.STRING) or self._check(TokenType.NUMBER) or
                  self._check(TokenType.PAREN_START)):
                saved_pos = self.pos
                stmt = self._parse_expression_statement()
                if stmt:
                    root.children.append(stmt)
                # Safety: if parsing didn't advance, skip token to prevent infinite loop
                if self.pos == saved_pos:
                    self._advance()
            # Skip comments and newlines
            elif self._check(TokenType.COMMENT) or self._check(TokenType.NEWLINE):
                self._advance()
            else:
                self._advance()

        return root

    def _current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, '', 0, 0)

    def _peek(self, offset=0) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return Token(TokenType.EOF, '', 0, 0)

    def _advance(self) -> Token:
        token = self._current()
        self.pos += 1
        return token

    def _is_at_end(self) -> bool:
        return self._current().type == TokenType.EOF

    def _check(self, token_type: TokenType) -> bool:
        return self._current().type == token_type

    def _match(self, token_type: TokenType) -> bool:
        if self._check(token_type):
            self._advance()
            return True
        return False

    def _match_keyword(self, keyword: str) -> bool:
        if self._current().type == TokenType.KEYWORD and self._current().value == keyword:
            self._advance()
            return True
        return False

    def _expect(self, token_type: TokenType, message: str = None):
        if not self._match(token_type):
            msg = message or f"Expected {token_type.name}, got {self._current().type.name}"
            self.error(msg)
        return self.tokens[self.pos - 1]

    def _parse_service_init(self) -> ASTNode:
        node = ASTNode('service-init', children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                key = self._advance().value
                self._expect(TokenType.COLON)
                value = self._parse_value()
                node.children.append(ASTNode('property', value={'key': key, 'value': value}))
                self._match(TokenType.SEMICOLON)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_service_include(self) -> ASTNode:
        """Parse service-include block for importing modules and files

        Syntax:
        service-include {
            @KernelClient <== get(include(cso_root('/root32/etc/tasks/kernel.cssl')));
            @Time <== get('time');
            @Secrets <== get('secrets');
        }
        """
        node = ASTNode('service-include', children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Parse module injection statements like @ModuleName <== get(...);
            if self._check(TokenType.AT):
                stmt = self._parse_expression_statement()
                if stmt:
                    node.children.append(stmt)
            elif self._check(TokenType.IDENTIFIER):
                # Also support identifier-based assignments: moduleName <== get(...);
                stmt = self._parse_expression_statement()
                if stmt:
                    node.children.append(stmt)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_service_run(self) -> ASTNode:
        node = ASTNode('service-run', children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._match_keyword('struct'):
                node.children.append(self._parse_struct())
            elif self._match_keyword('define'):
                node.children.append(self._parse_define())
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_package(self) -> ASTNode:
        """Parse package {} block for service metadata - NEW

        Syntax:
        package {
            service = "ServiceName";
            exec = @Start();
            version = "1.0.0";
            description = "Beschreibung";
        }
        """
        node = ASTNode('package', children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                key = self._advance().value
                self._expect(TokenType.EQUALS)
                value = self._parse_expression()
                node.children.append(ASTNode('package_property', value={'key': key, 'value': value}))
                self._match(TokenType.SEMICOLON)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_package_includes(self) -> ASTNode:
        """Parse package-includes {} block for imports - NEW

        Syntax:
        package-includes {
            @Lists = get('list');
            @OS = get('os');
            @Time = get('time');
            @VSRam = get('vsramsdk');
        }
        """
        node = ASTNode('package-includes', children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Parse module injection statements like @ModuleName = get(...);
            if self._check(TokenType.AT):
                stmt = self._parse_expression_statement()
                if stmt:
                    node.children.append(stmt)
            elif self._check(TokenType.IDENTIFIER):
                # Also support identifier-based assignments
                stmt = self._parse_expression_statement()
                if stmt:
                    node.children.append(stmt)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_struct(self) -> ASTNode:
        name = self._advance().value
        is_global = False

        # Check for (@) decorator: struct Name(@) { ... }
        if self._match(TokenType.PAREN_START):
            if self._check(TokenType.AT):
                self._advance()  # skip @
                is_global = True
            self._expect(TokenType.PAREN_END)

        node = ASTNode('struct', value={'name': name, 'global': is_global}, children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._match_keyword('define'):
                node.children.append(self._parse_define())
            elif self._check(TokenType.IDENTIFIER):
                # Look ahead to determine what kind of statement this is
                saved_pos = self.pos
                var_name = self._advance().value

                if self._match(TokenType.INJECT_LEFT):
                    # Injection: var <== expr
                    value = self._parse_expression()
                    node.children.append(ASTNode('injection', value={'name': var_name, 'source': value}))
                    self._match(TokenType.SEMICOLON)
                elif self._match(TokenType.EQUALS):
                    # Assignment: var = expr
                    value = self._parse_expression()
                    node.children.append(ASTNode('assignment', value={'name': var_name, 'value': value}))
                    self._match(TokenType.SEMICOLON)
                elif self._check(TokenType.PAREN_START):
                    # Function call: func(args)
                    self.pos = saved_pos  # Go back to parse full expression
                    stmt = self._parse_expression_statement()
                    if stmt:
                        node.children.append(stmt)
                elif self._match(TokenType.DOT):
                    # Method call: obj.method(args)
                    self.pos = saved_pos  # Go back to parse full expression
                    stmt = self._parse_expression_statement()
                    if stmt:
                        node.children.append(stmt)
                else:
                    self._match(TokenType.SEMICOLON)
            elif self._check(TokenType.AT):
                # Module reference statement
                stmt = self._parse_expression_statement()
                if stmt:
                    node.children.append(stmt)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_enum(self, is_embedded: bool = False) -> ASTNode:
        """Parse enum declaration.

        Syntax:
            enum EnumName {
                VALUE1,         // Auto value 0
                VALUE2,         // Auto value 1
                VALUE3 = 10,    // Explicit value 10
                VALUE4          // Auto value 11
            }

            embedded enum NewEnum &OldEnum { ... }  // Replace OldEnum with NewEnum values

        Access values via EnumName::VALUE1
        """
        # v4.9.9: Support 'enum this->EnumName' for class member enums
        this_ref = False
        if self._check(TokenType.KEYWORD) and self._current().value == 'this':
            self._advance()  # consume 'this'
            self._expect(TokenType.FLOW_RIGHT)  # consume '->'
            this_ref = True
        enum_name = self._advance().value

        # v4.3.2: Check for &Target reference (enum replacement)
        replace_target = None
        if self._match(TokenType.AMPERSAND):
            if self._check(TokenType.IDENTIFIER):
                replace_target = self._advance().value
            elif self._check(TokenType.AT):
                self._advance()
                if self._check(TokenType.IDENTIFIER):
                    replace_target = '@' + self._advance().value

        self._expect(TokenType.BLOCK_START)

        members = []
        current_value = 0

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Skip newlines/whitespace between enum values
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue

            # Get member name
            if self._check(TokenType.IDENTIFIER):
                member_name = self._advance().value

                # Check for explicit value: VALUE = 10
                if self._match(TokenType.EQUALS):
                    value_node = self._parse_expression()
                    if isinstance(value_node, ASTNode) and value_node.type == 'literal':
                        val = value_node.value
                        if isinstance(val, dict) and 'value' in val:
                            current_value = val['value']
                        else:
                            current_value = val
                    else:
                        current_value = value_node

                members.append({'name': member_name, 'value': current_value})
                current_value = current_value + 1 if isinstance(current_value, int) else current_value

                # Skip comma if present
                self._match(TokenType.COMMA)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)

        return ASTNode('enum', value={
            'name': enum_name,
            'members': members,
            'is_embedded': is_embedded,
            'replace_target': replace_target,
            'this_ref': this_ref
        })

    def _parse_embedded_override(self) -> ASTNode:
        """Parse embedded override for enums/structs without explicit type keyword.

        Syntax:
            embedded __NewName &OldEnum { ... }      // Replace OldEnum
            embedded __NewName &OldEnum ++ { ... }   // Add to OldEnum
            embedded __NewName &OldEnum -- { ... }   // Remove from OldEnum

        This creates a new definition that modifies the target.
        """
        # Get the new name
        new_name = self._advance().value

        # Expect &Target
        if not self._match(TokenType.AMPERSAND):
            self.error("Expected '&' followed by target name after embedded identifier")

        # Get target name
        target_name = None
        if self._check(TokenType.IDENTIFIER):
            target_name = self._advance().value
        elif self._check(TokenType.AT):
            self._advance()
            if self._check(TokenType.IDENTIFIER):
                target_name = '@' + self._advance().value
        else:
            self.error("Expected target name after '&'")

        # Check for mode modifier: ++ (add) or -- (remove)
        mode = 'replace'
        if self._match(TokenType.PLUS_PLUS):
            mode = 'add'
        elif self._match(TokenType.MINUS_MINUS):
            mode = 'remove'

        self._expect(TokenType.BLOCK_START)

        # Parse members (enum-style: NAME = value, NAME, etc.)
        members = []
        current_value = 0

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue

            if self._check(TokenType.IDENTIFIER):
                member_name = self._advance().value

                # Check for explicit value
                if self._match(TokenType.EQUALS):
                    value_node = self._parse_expression()
                    if isinstance(value_node, ASTNode) and value_node.type == 'literal':
                        val = value_node.value
                        if isinstance(val, dict) and 'value' in val:
                            current_value = val['value']
                        else:
                            current_value = val
                    else:
                        current_value = value_node

                members.append({'name': member_name, 'value': current_value})
                if isinstance(current_value, int):
                    current_value = current_value + 1

                self._match(TokenType.COMMA)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)

        return ASTNode('enum', value={
            'name': new_name,
            'members': members,
            'is_embedded': True,
            'replace_target': target_name,
            'mode': mode  # 'replace', 'add', or 'remove'
        })

    def _parse_bytearrayed(self) -> ASTNode:
        """Parse bytearrayed declaration - function-to-byte mapping with pattern matching.

        Syntax:
            bytearrayed MyBytes {
                &func1;              // Position 0x0
                &func2;              // Position 0x1
                &func3;              // Position 0x2
                case {0, 1, 0} {     // Pattern match on return values
                    // Execute if func1=0, func2=1, func3=0
                }
                case {1, _, _} {     // Wildcards with _
                    // Execute if func1=1, others any value
                }
                default {
                    // Execute if no case matches
                }
            }

        Access:
            MyBytes()            // Execute pattern matching
            MyBytes["0x0"]       // Get value at position 0
            MyBytes[0]           // Get value at position 0
        """
        bytearrayed_name = self._advance().value
        self._expect(TokenType.BLOCK_START)

        func_refs = []       # List of function references at each byte position
        cases = []           # List of case blocks with patterns
        default_block = None # Default block if no case matches

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Skip newlines
            if self._check(TokenType.NEWLINE):
                self._advance()
                continue

            # Parse case block
            if self._match_keyword('case'):
                pattern = []
                self._expect(TokenType.BLOCK_START)

                # Parse pattern: {value, value, value, ...}
                while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                    if self._check(TokenType.COMMA):
                        self._advance()
                        continue
                    if self._check(TokenType.NEWLINE):
                        self._advance()
                        continue

                    # Parse pattern element
                    if self._check(TokenType.IDENTIFIER) and self._current().value == '_':
                        # Wildcard - matches any value
                        pattern.append({'type': 'wildcard'})
                        self._advance()
                    elif self._check(TokenType.BRACKET_START):
                        # v4.3.2: List pattern - matches a list value: ["read", "write"]
                        self._advance()  # consume [
                        list_elements = []
                        while not self._check(TokenType.BRACKET_END) and not self._is_at_end():
                            if self._check(TokenType.COMMA):
                                self._advance()
                                continue
                            if self._check(TokenType.STRING):
                                list_elements.append(self._advance().value)
                            elif self._check(TokenType.NUMBER):
                                list_elements.append(self._advance().value)
                            elif self._check(TokenType.KEYWORD):
                                kw = self._current().value
                                if kw in ('true', 'True'):
                                    list_elements.append(True)
                                elif kw in ('false', 'False'):
                                    list_elements.append(False)
                                self._advance()
                            else:
                                self._advance()
                        self._expect(TokenType.BRACKET_END)
                        pattern.append({'type': 'list', 'values': list_elements})
                    elif self._check(TokenType.NUMBER):
                        # Check for hex format like 0x28
                        token = self._current()
                        value = token.value
                        if isinstance(value, dict) and 'value' in value:
                            value = value['value']
                        # Check for position=value syntax: 0x28="Gut"
                        self._advance()
                        if self._match(TokenType.EQUALS):
                            match_value = self._parse_expression()
                            pattern.append({'type': 'indexed', 'index': value, 'value': match_value})
                        else:
                            pattern.append({'type': 'value', 'value': value})
                    elif self._check(TokenType.STRING):
                        value = self._advance().value
                        pattern.append({'type': 'value', 'value': value})
                    elif self._check(TokenType.BOOLEAN):
                        # v4.3.2: Handle true/false which are tokenized as BOOLEAN
                        value = self._advance().value
                        pattern.append({'type': 'value', 'value': value})
                    elif self._check(TokenType.KEYWORD):
                        kw = self._current().value
                        if kw in ('true', 'True'):
                            pattern.append({'type': 'value', 'value': True})
                            self._advance()
                        elif kw in ('false', 'False'):
                            pattern.append({'type': 'value', 'value': False})
                            self._advance()
                        elif kw in TYPE_GENERICS or kw in ('int', 'string', 'float', 'bool', 'dynamic'):
                            # Type pattern: vector<string>, int, etc.
                            type_name = self._advance().value
                            if self._check(TokenType.COMPARE_LT):
                                # Generic type
                                self._advance()
                                inner = self._parse_generic_type_content()
                                type_name = f"{type_name}<{inner}>"
                            pattern.append({'type': 'type_match', 'type_name': type_name})
                        else:
                            # Skip unknown keywords
                            self._advance()
                    elif self._check(TokenType.IDENTIFIER):
                        # Could be a variable reference or type
                        ident = self._advance().value
                        # Check for indexed syntax: 2x35="value"
                        if self._check(TokenType.IDENTIFIER) and ident.isdigit():
                            # Pattern like 2x35 (position 2, repeat 35)
                            second = self._advance().value
                            if self._match(TokenType.EQUALS):
                                match_value = self._parse_expression()
                                pattern.append({'type': 'repeat', 'pos': int(ident), 'repeat': second, 'value': match_value})
                            else:
                                pattern.append({'type': 'repeat', 'pos': int(ident), 'repeat': second, 'value': None})
                        else:
                            pattern.append({'type': 'variable', 'name': ident})
                    else:
                        self._advance()

                self._expect(TokenType.BLOCK_END)

                # Parse case body - supports both:
                # case {pattern}: statement;  (colon syntax)
                # case {pattern} { statements }  (block syntax)
                body_children = []
                if self._match(TokenType.COLON):
                    # Colon syntax: single statement or until next case/default/}
                    stmt = self._parse_statement()
                    if stmt:
                        body_children.append(stmt)
                elif self._check(TokenType.BLOCK_START):
                    self._advance()  # consume {
                    while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)
                    self._expect(TokenType.BLOCK_END)

                cases.append({'pattern': pattern, 'body': body_children})

            # Parse default block - supports both:
            # default: statement;  (colon syntax)
            # default { statements }  (block syntax)
            elif self._match_keyword('default'):
                body_children = []
                if self._match(TokenType.COLON):
                    # Colon syntax: single statement
                    stmt = self._parse_statement()
                    if stmt:
                        body_children.append(stmt)
                elif self._check(TokenType.BLOCK_START):
                    self._advance()  # consume {
                    while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)
                    self._expect(TokenType.BLOCK_END)
                default_block = body_children

            # v4.9.4: Parse except block - matches when pattern does NOT match
            # except {pattern}: statement;  (colon syntax)
            # except {pattern} { statements }  (block syntax)
            elif self._match_keyword('except'):
                pattern = []
                self._expect(TokenType.BLOCK_START)

                # Parse pattern (same as case)
                while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                    if self._check(TokenType.COMMA):
                        self._advance()
                        continue
                    if self._check(TokenType.NEWLINE):
                        self._advance()
                        continue
                    if self._check(TokenType.NUMBER):
                        token = self._current()
                        value = token.value
                        if isinstance(value, dict) and 'value' in value:
                            value = value['value']
                        self._advance()
                        pattern.append({'type': 'value', 'value': value})
                    elif self._check(TokenType.STRING):
                        value = self._advance().value
                        pattern.append({'type': 'value', 'value': value})
                    elif self._check(TokenType.KEYWORD):
                        kw = self._current().value
                        if kw in ('true', 'True'):
                            pattern.append({'type': 'value', 'value': True})
                        elif kw in ('false', 'False'):
                            pattern.append({'type': 'value', 'value': False})
                        self._advance()
                    else:
                        self._advance()

                self._expect(TokenType.BLOCK_END)

                # Parse except body
                body_children = []
                if self._match(TokenType.COLON):
                    stmt = self._parse_statement()
                    if stmt:
                        body_children.append(stmt)
                elif self._check(TokenType.BLOCK_START):
                    self._advance()
                    while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)
                    self._expect(TokenType.BLOCK_END)

                # Mark as except (inverted match)
                cases.append({'pattern': pattern, 'body': body_children, 'except': True})

            # Parse function reference: &funcName; or &funcName(arg1, arg2);
            elif self._check(TokenType.AMPERSAND):
                self._advance()  # consume &
                if self._check(TokenType.IDENTIFIER):
                    func_name = self._advance().value
                    # v4.3.2: Support function references with parameters: &testfunc(1, 2)
                    func_args = []
                    if self._check(TokenType.PAREN_START):
                        self._advance()  # consume (
                        while not self._check(TokenType.PAREN_END) and not self._is_at_end():
                            arg = self._parse_expression()
                            func_args.append(arg)
                            if not self._check(TokenType.PAREN_END):
                                self._expect(TokenType.COMMA)
                        self._expect(TokenType.PAREN_END)
                    func_refs.append({
                        'position': len(func_refs),
                        'hex_pos': f"0x{len(func_refs):x}",
                        'func_ref': func_name,
                        'args': func_args  # v4.3.2: Store arguments for simulation
                    })
                self._match(TokenType.SEMICOLON)

            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)

        return ASTNode('bytearrayed', value={
            'name': bytearrayed_name,
            'func_refs': func_refs,
            'cases': cases,
            'default': default_block
        })

    def _parse_bytearrayed_body(self) -> List[ASTNode]:
        """Parse body of a bytearrayed define function (v4.7).

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

        Returns list of AST nodes: case nodes with func_refs, and default node.
        """
        children = []

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Handle case blocks: case "value": &FuncRef() { body }
            if self._match_keyword('case'):
                case_values = []
                func_refs = []

                # Parse case values (comma-separated): case "en", "de": ...
                # v4.8.8: Also support tuple patterns: case {0, 0}: for matching multiple byte values
                while True:
                    if self._check(TokenType.STRING):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.NUMBER):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.BOOLEAN):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.IDENTIFIER):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.BLOCK_START):
                        # v4.8.8: Tuple pattern {val1, val2, ...} for matching multiple byte values
                        self._advance()  # consume {
                        tuple_values = []
                        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                            if self._check(TokenType.NUMBER):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.STRING):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.BOOLEAN):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.IDENTIFIER):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.COMMA):
                                self._advance()  # skip comma
                            else:
                                break
                        self._expect(TokenType.BLOCK_END)  # consume }
                        case_values.append(tuple(tuple_values))  # Store as tuple
                    else:
                        break
                    if not self._match(TokenType.COMMA):
                        break

                # Expect colon after case values
                self._expect(TokenType.COLON)

                # Parse function references: &FuncRef(), &FuncRef2(), ...
                while self._check(TokenType.AMPERSAND):
                    self._advance()  # consume &
                    if self._check(TokenType.IDENTIFIER):
                        func_name = self._advance().value
                        func_args = []
                        if self._match(TokenType.PAREN_START):
                            while not self._check(TokenType.PAREN_END) and not self._is_at_end():
                                if self._check(TokenType.COMMA):
                                    self._advance()
                                    continue
                                arg = self._parse_expression()
                                func_args.append(arg)
                            self._expect(TokenType.PAREN_END)
                        func_refs.append({'name': func_name, 'args': func_args})
                    if not self._match(TokenType.COMMA):
                        break

                # Parse case body - either block { } or inline statements until next case/default
                body_children = []
                if self._check(TokenType.BLOCK_START):
                    # Block syntax: case val: { ... }
                    self._advance()  # consume {
                    while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)
                    self._expect(TokenType.BLOCK_END)
                else:
                    # v4.8.8: Inline syntax: case val: stmt1; stmt2; return x; (until next case/default/})
                    while not self._is_at_end():
                        # Stop at next case, default, except, or block end
                        # v4.9.4: Added 'except' to stop keywords
                        if self._check(TokenType.KEYWORD) and self._current().value in ('case', 'default', 'except'):
                            break
                        if self._check(TokenType.BLOCK_END):
                            break
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)

                children.append(ASTNode('case', value={
                    'patterns': case_values,
                    'func_refs': func_refs,
                    'body': body_children
                }))

            # Handle default block: default: { body } or default: stmt (inline)
            elif self._match_keyword('default'):
                self._match(TokenType.COLON)  # Optional colon
                body_children = []
                if self._check(TokenType.BLOCK_START):
                    # Block syntax
                    self._advance()  # consume {
                    while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)
                    self._expect(TokenType.BLOCK_END)
                else:
                    # v4.8.8: Inline syntax: default: stmt1; return x; (until block end)
                    while not self._is_at_end():
                        if self._check(TokenType.BLOCK_END):
                            break
                        # Also stop at next case/except (shouldn't happen after default, but be safe)
                        # v4.9.4: Added 'except' to stop keywords
                        if self._check(TokenType.KEYWORD) and self._current().value in ('case', 'except'):
                            break
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)

                children.append(ASTNode('default', value={
                    'body': body_children
                }))

            # v4.9.4: Handle except block - matches when pattern does NOT match
            # except {pattern}: { body } or except {pattern}: stmt (inline)
            elif self._match_keyword('except'):
                case_values = []

                # Parse except values (same as case)
                while True:
                    if self._check(TokenType.STRING):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.NUMBER):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.BOOLEAN):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.IDENTIFIER):
                        case_values.append(self._advance().value)
                    elif self._check(TokenType.BLOCK_START):
                        # Tuple pattern {val1, val2, ...}
                        self._advance()  # consume {
                        tuple_values = []
                        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                            if self._check(TokenType.NUMBER):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.STRING):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.BOOLEAN):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.IDENTIFIER):
                                tuple_values.append(self._advance().value)
                            elif self._check(TokenType.COMMA):
                                self._advance()
                            else:
                                break
                        self._expect(TokenType.BLOCK_END)
                        case_values.append(tuple(tuple_values))
                    else:
                        break
                    if not self._match(TokenType.COMMA):
                        break

                # Expect colon after except values
                self._expect(TokenType.COLON)

                # Parse except body
                body_children = []
                if self._check(TokenType.BLOCK_START):
                    self._advance()
                    while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)
                    self._expect(TokenType.BLOCK_END)
                else:
                    # Inline syntax
                    while not self._is_at_end():
                        if self._check(TokenType.KEYWORD) and self._current().value in ('case', 'default', 'except'):
                            break
                        if self._check(TokenType.BLOCK_END):
                            break
                        stmt = self._parse_statement()
                        if stmt:
                            body_children.append(stmt)

                # Mark as except (inverted match) using 'case' node type with except flag
                children.append(ASTNode('case', value={
                    'patterns': case_values,
                    'func_refs': [],
                    'body': body_children,
                    'except': True  # Inverted matching
                }))

            # v4.8.8: Handle func_ref statements (&func; or &func(args);)
            elif self._check(TokenType.AMPERSAND):
                self._advance()  # consume &
                if self._check(TokenType.IDENTIFIER):
                    func_name = self._advance().value
                    func_args = []
                    # Check for arguments
                    if self._match(TokenType.PAREN_START):
                        while not self._check(TokenType.PAREN_END) and not self._is_at_end():
                            if self._check(TokenType.COMMA):
                                self._advance()
                                continue
                            arg = self._parse_expression()
                            func_args.append(arg)
                        self._expect(TokenType.PAREN_END)
                    self._match(TokenType.SEMICOLON)  # Optional semicolon
                    children.append(ASTNode('func_ref', value={
                        'name': func_name,
                        'args': func_args
                    }))
                else:
                    self.error("Expected identifier after '&' in bytearrayed body")

            # Handle other statements (e.g., expressions, function calls)
            else:
                stmt = self._parse_statement()
                if stmt:
                    children.append(stmt)

        return children

    def _parse_namespace(self) -> ASTNode:
        """Parse namespace definition.

        Syntax:
            namespace mylib {
                void myFunc() { ... }
                class MyClass { ... }
                namespace nested { ... }
            }

        Access: mylib::myFunc(), mylib::MyClass, mylib::nested::innerFunc()
        """
        # Get namespace name
        if not self._check(TokenType.IDENTIFIER):
            self.error("Expected namespace name after 'namespace'")
        name = self._advance().value

        # Expect opening brace
        if not self._match(TokenType.BLOCK_START):
            self.error(f"Expected '{{' after 'namespace {name}'")

        # Parse namespace contents
        members = []
        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._match_keyword('namespace'):
                # Nested namespace
                members.append(self._parse_namespace())
            elif self._match_keyword('class'):
                members.append(self._parse_class())
            elif self._match_keyword('struct'):
                members.append(self._parse_struct())
            elif self._match_keyword('enum'):
                members.append(self._parse_enum())
            elif self._match_keyword('define'):
                members.append(self._parse_define())
            elif self._looks_like_function_declaration():
                members.append(self._parse_typed_function())
            elif self._check(TokenType.COMMENT):
                self._advance()  # Skip comments
            else:
                stmt = self._parse_expression_statement()
                if stmt:
                    members.append(stmt)

        # Expect closing brace
        if not self._match(TokenType.BLOCK_END):
            self.error(f"Expected '}}' to close namespace '{name}'")

        return ASTNode('namespace', value={'name': name}, children=members)

    def _parse_class(self, is_global: bool = False, is_embedded: bool = False) -> ASTNode:
        """Parse class declaration with members and methods.

        Syntax:
            class ClassName { ... }           // Local class
            global class ClassName { ... }    // Global class
            class @ClassName { ... }          // Global class (alternative)
            class *ClassName { ... }          // Non-null class
            embedded class ClassName &$Target { ... }  // Immediate replacement (v4.2.5)

        Non-null class (all methods return non-null):
            class *MyClass { ... }
        """
        # Check for * prefix (non-null class - all methods return non-null)
        non_null = False
        if self._match(TokenType.MULTIPLY):
            non_null = True

        # Check for @ prefix (global class): class @ClassName
        if self._check(TokenType.AT):
            self._advance()  # consume @
            is_global = True

        class_name_token = self._advance()
        class_name = class_name_token.value
        class_line = class_name_token.line
        class_column = class_name_token.column

        # Check for class-level constructor parameters: class MyClass (int x, string y) { ... }
        class_params = []
        if self._match(TokenType.PAREN_START):
            class_params = self._parse_parameter_list()
            self._expect(TokenType.PAREN_END)

        # v4.2.5: Check for &target reference for class replacement
        # Syntax: embedded class BetterGame() &$Game { ... }
        #         class NewClass &OldClass { ... }
        append_ref_class = None
        append_ref_member = None
        if self._match(TokenType.AMPERSAND):
            if self._check(TokenType.IDENTIFIER):
                append_ref_class = self._advance().value
            elif self._check(TokenType.AT):
                self._advance()
                if self._check(TokenType.IDENTIFIER):
                    append_ref_class = '@' + self._advance().value
            elif self._check(TokenType.SHARED_REF):
                append_ref_class = f'${self._advance().value}'
            else:
                raise CSSLSyntaxError("Expected class name after '&' in class reference")

            # Check for ::member or .member (for targeting specific members)
            if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.DOT):
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                    append_ref_member = self._advance().value

        # Check for inheritance and overwrites:
        # class Child : extends Parent { ... }
        # class Child : extends $PythonObject { ... }
        # class Child : extends Parent : overwrites Parent { ... }
        # class Child : extends Parent (param1, param2) { ... }  <- constructor args for parent
        extends_class = None
        extends_is_python = False
        extends_lang_ref = None  # v4.1.0: Cross-language inheritance (cpp$ClassName)
        extends_args = []
        overwrites_class = None
        overwrites_is_python = False
        supports_language = None  # v4.1.0: Multi-language syntax support
        uses_memory = None  # v4.9.0: Memory binding for deferred execution

        # v4.8.8: Support C++ style "class Child extends Parent" without colon
        if self._match_keyword('extends'):
            # Direct extends without colon: class Dog extends Animal
            if self._check(TokenType.LANG_INSTANCE_REF):
                ref = self._advance().value
                extends_lang_ref = ref
                extends_class = ref['instance']
            elif self._check(TokenType.IDENTIFIER):
                extends_class = self._advance().value
            elif self._check(TokenType.SHARED_REF):
                extends_class = self._advance().value
                extends_is_python = True
            else:
                raise CSSLSyntaxError("Expected parent class name after 'extends'")
            # Check for constructor arguments: extends Parent(arg1, arg2)
            if self._match(TokenType.PAREN_START):
                while not self._check(TokenType.PAREN_END):
                    arg = self._parse_expression()
                    extends_args.append(arg)
                    self._match(TokenType.COMMA)
                self._expect(TokenType.PAREN_END)
        elif self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON):
            # Parse extends and/or overwrites (can be chained with : or ::)
            while True:
                if self._match_keyword('extends'):
                    # v4.1.0: Check for cross-language inheritance: extends cpp$ClassName
                    if self._check(TokenType.LANG_INSTANCE_REF):
                        ref = self._advance().value
                        extends_lang_ref = ref  # {'lang': 'cpp', 'instance': 'ClassName'}
                        extends_class = ref['instance']
                    elif self._check(TokenType.IDENTIFIER):
                        extends_class = self._advance().value
                    elif self._check(TokenType.SHARED_REF):
                        extends_class = self._advance().value
                        extends_is_python = True
                    else:
                        raise CSSLSyntaxError("Expected parent class name after 'extends'")
                    # Check for constructor arguments: extends Parent (arg1, arg2)
                    if self._match(TokenType.PAREN_START):
                        while not self._check(TokenType.PAREN_END):
                            arg = self._parse_expression()
                            extends_args.append(arg)
                            self._match(TokenType.COMMA)
                        self._expect(TokenType.PAREN_END)
                elif self._match_keyword('overwrites'):
                    if self._check(TokenType.IDENTIFIER):
                        overwrites_class = self._advance().value
                    elif self._check(TokenType.SHARED_REF):
                        overwrites_class = self._advance().value
                        overwrites_is_python = True
                    else:
                        raise CSSLSyntaxError("Expected class name after 'overwrites'")
                    # Skip optional () after class name
                    if self._match(TokenType.PAREN_START):
                        self._expect(TokenType.PAREN_END)
                # v4.1.0: Parse 'supports' keyword for multi-language syntax
                elif self._match_keyword('supports'):
                    if self._check(TokenType.AT):
                        self._advance()  # consume @
                        if self._check(TokenType.IDENTIFIER):
                            supports_language = '@' + self._advance().value
                        else:
                            raise CSSLSyntaxError("Expected language identifier after '@' in 'supports'")
                    elif self._check(TokenType.IDENTIFIER):
                        supports_language = self._advance().value
                    else:
                        raise CSSLSyntaxError("Expected language identifier after 'supports'")
                # v4.9.0: Parse 'uses' keyword for memory binding (deferred execution)
                # Syntax: class MyClass : uses memory(address) { }
                elif self._match_keyword('uses'):
                    if (self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD)) and self._current().value == 'memory':
                        self._advance()  # consume 'memory'
                        self._expect(TokenType.PAREN_START)
                        uses_memory = self._parse_expression()  # Parse the address expression
                        self._expect(TokenType.PAREN_END)
                    else:
                        raise CSSLSyntaxError("Expected 'memory(address)' after 'uses'")
                else:
                    raise CSSLSyntaxError("Expected 'extends', 'overwrites', 'supports', or 'uses' after ':' or '::' in class declaration")
                # Check for another : or :: for chaining
                if not (self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON)):
                    break

        # v4.2.0: If supports_language is set, capture raw body for runtime transformation
        raw_body = None
        if supports_language:
            raw_body = self._extract_raw_block_body()

        node = ASTNode('class', value={
            'name': class_name,
            'is_global': is_global,
            'is_embedded': is_embedded,  # v4.2.5: immediate &target replacement
            'non_null': non_null,
            'class_params': class_params,
            'extends': extends_class,
            'extends_is_python': extends_is_python,
            'extends_lang_ref': extends_lang_ref,  # v4.1.0
            'extends_args': extends_args,
            'overwrites': overwrites_class,
            'overwrites_is_python': overwrites_is_python,
            'supports_language': supports_language,  # v4.1.0
            'raw_body': raw_body,  # v4.2.0: Raw body for language transformation
            'append_ref_class': append_ref_class,  # v4.2.5: &target class reference
            'append_ref_member': append_ref_member,  # v4.2.5: &target member reference
            'uses_memory': uses_memory  # v4.9.0: Memory binding for deferred execution
        }, children=[], line=class_line, column=class_column)

        # v4.2.0: If we have raw_body for language transformation, skip regular parsing
        if raw_body is not None:
            # Skip the block entirely - runtime will transform and parse
            self._expect(TokenType.BLOCK_START)
            brace_count = 1
            while brace_count > 0 and not self._is_at_end():
                if self._check(TokenType.BLOCK_START):
                    brace_count += 1
                elif self._check(TokenType.BLOCK_END):
                    brace_count -= 1
                if brace_count > 0:
                    self._advance()
            self._expect(TokenType.BLOCK_END)
            return node

        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Check for typed function (method) declaration
            if self._looks_like_function_declaration():
                method = self._parse_typed_function()
                method_info = method.value
                method_name = method_info.get('name')

                # Mark constructor (same name as class or __init__)
                if method_name == class_name or method_name == '__init__':
                    method.value['is_constructor'] = True

                node.children.append(method)

            # Check for typed member variable declaration
            elif self._looks_like_typed_variable():
                member = self._parse_typed_variable()
                if member:
                    # Mark as class member
                    member.value['is_member'] = True
                    node.children.append(member)

            # Check for define-style method
            elif self._match_keyword('define'):
                method = self._parse_define()
                node.children.append(method)

            # v4.7: Check for function modifiers before define (e.g., bytearrayed define, private define)
            elif self._check(TokenType.KEYWORD) and self._is_function_modifier(self._current().value):
                modifiers = []
                is_embedded = False
                is_global = False
                while self._check(TokenType.KEYWORD) and self._is_function_modifier(self._current().value):
                    mod = self._advance().value
                    modifiers.append(mod)
                    if mod == 'embedded':
                        is_embedded = True
                    elif mod == 'global':
                        is_global = True
                # After modifiers, expect 'define' or typed function
                if self._match_keyword('define'):
                    method = self._parse_define(
                        is_global=is_global, is_embedded=is_embedded,
                        modifiers=modifiers
                    )
                    node.children.append(method)
                elif self._looks_like_function_declaration():
                    method = self._parse_typed_function(modifiers=modifiers)
                    node.children.append(method)
                else:
                    self.error(f"Expected 'define' or function after modifiers in class: {modifiers}")

            # Check for constr keyword (constructor declaration)
            # Syntax: constr ConstructorName() { ... }
            # or: constr ConstructorName() : extends Parent::ConstructorName { ... }
            # v4.8.8: Also supports: secure constr Name(), callable constr Name()
            # v4.9.9: ~Name() is shorthand for constr ~Name() (destructor)
            elif self._match(TokenType.TILDE):
                # Shorthand destructor: ~Name() { ... } without constr keyword
                # Put tilde back so _parse_constructor can consume it
                self.pos -= 1
                constructor = self._parse_constructor(class_name, modifiers=[])
                node.children.append(constructor)
            elif self._match_keyword('constr'):
                constructor = self._parse_constructor(class_name, modifiers=[])
                node.children.append(constructor)
            # v4.8.8: Check for secure/callable modifiers before constr
            elif self._match_keyword('secure') or self._match_keyword('callable'):
                constr_modifier = self.tokens[self.pos - 1].value  # 'secure' or 'callable'
                if self._match_keyword('constr'):
                    constructor = self._parse_constructor(class_name, modifiers=[constr_modifier])
                    node.children.append(constructor)
                else:
                    self.error(f"Expected 'constr' after '{constr_modifier}'")

            # v4.9.11: Handle this->member = value initialization in class body
            elif self._check(TokenType.KEYWORD) and self._current().value == 'this':
                stmt = self._parse_expression_statement()
                if stmt:
                    wrapped = ASTNode('class_body_init', value={'statement': stmt})
                    node.children.append(wrapped)

            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_constructor(self, class_name: str, modifiers: list = None) -> ASTNode:
        """Parse constructor or destructor declaration inside a class.

        Syntax:
            constr ConstructorName() { ... }
            constr ~ClassName() { ... }  // v4.8.8: Destructor (cleanup code)
            constr ConstructorName() ++ { ... }  // Append: keeps parent constructor + adds new code
            constr ConstructorName() &ParentClass::constructors ++ { ... }  // Append specific parent constructor
            constr ConstructorName() : extends ParentClass::ConstructorName { ... }
            constr ConstructorName() : extends ParentClass::ConstructorName : overwrites ParentClass::ConstructorName { ... }

        v4.8.8 Modifiers:
            secure constr Name() { ... }   - Only runs on exception in class
            callable constr Name() { ... } - Must be manually called, not auto-run

        The ++ operator means: execute parent's version first, then execute this code (append mode).
        The &ClassName::member syntax references a specific member from the overwritten class.
        Destructor (~Name) is called when instance is deleted or goes out of scope.
        """
        modifiers = modifiers or []
        # v4.8.8: Check for destructor prefix ~
        is_destructor = False
        if self._match(TokenType.TILDE):  # ~ operator for destructors
            is_destructor = True

        # Get constructor/destructor name
        if not self._check(TokenType.IDENTIFIER):
            raise CSSLSyntaxError("Expected constructor name after 'constr'" + (" ~" if is_destructor else ""))
        constr_token = self._advance()
        constr_name = constr_token.value
        constr_line = constr_token.line
        constr_column = constr_token.column

        # v4.8.8: Destructor name should match class name
        if is_destructor:
            constr_name = f"~{constr_name}"  # Store with ~ prefix

        # Parse method-level extends/overwrites with :: syntax
        extends_target = None
        extends_class_ref = None
        extends_method_ref = None
        overwrites_target = None
        overwrites_class_ref = None
        overwrites_method_ref = None

        # New: Append mode and reference tracking
        append_mode = False  # ++ operator: keep parent code + add new
        append_ref_class = None  # &ClassName part
        append_ref_member = None  # ::member part (constructors, functionName, etc.)

        # Parse parameters
        params = []
        if self._match(TokenType.PAREN_START):
            params = self._parse_parameter_list()
            self._expect(TokenType.PAREN_END)

        # Check for &ClassName::member reference (for targeting specific parent member)
        # Syntax: constr Name() &ParentClass::constructors ++ { ... }
        if self._match(TokenType.AMPERSAND):
            # Parse the class reference
            if self._check(TokenType.IDENTIFIER):
                append_ref_class = self._advance().value
            elif self._check(TokenType.SHARED_REF):
                append_ref_class = f'${self._advance().value}'
            else:
                raise CSSLSyntaxError("Expected class name after '&' in constructor reference")

            # Check for ::member
            if self._match(TokenType.DOUBLE_COLON):
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                    append_ref_member = self._advance().value
                else:
                    raise CSSLSyntaxError("Expected member name after '::' in constructor reference")

        # Check for ++ append operator
        if self._match(TokenType.PLUS_PLUS):
            append_mode = True

        # Check for method-level extends/overwrites with :: or :
        if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON):
            while True:
                if self._match_keyword('extends'):
                    # Parse Parent::method or just method
                    extends_target = self._parse_qualified_method_ref()
                    if '::' in extends_target:
                        parts = extends_target.split('::')
                        extends_class_ref = parts[0]
                        extends_method_ref = parts[1]
                    else:
                        extends_method_ref = extends_target
                elif self._match_keyword('overwrites'):
                    # Parse Parent::method or just method
                    overwrites_target = self._parse_qualified_method_ref()
                    if '::' in overwrites_target:
                        parts = overwrites_target.split('::')
                        overwrites_class_ref = parts[0]
                        overwrites_method_ref = parts[1]
                    else:
                        overwrites_method_ref = overwrites_target
                else:
                    break
                # Check for another :: or : for chaining
                if not (self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON)):
                    break

        # Parse constructor body
        self._expect(TokenType.BLOCK_START)
        body = []
        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                body.append(stmt)
        self._expect(TokenType.BLOCK_END)

        return ASTNode('constructor', value={
            'name': constr_name,
            'class_name': class_name,
            'params': params,
            'is_constructor': not is_destructor,  # v4.8.8: False for destructors
            'is_destructor': is_destructor,  # v4.8.8: True for ~Name()
            'is_secure': 'secure' in modifiers,  # v4.8.8: Only run on exception
            'is_callable': 'callable' in modifiers,  # v4.8.8: Manual call only
            'extends_target': extends_target,
            'extends_class': extends_class_ref,
            'extends_method': extends_method_ref,
            'overwrites_target': overwrites_target,
            'overwrites_class': overwrites_class_ref,
            'overwrites_method': overwrites_method_ref,
            # New append mode fields
            'append_mode': append_mode,
            'append_ref_class': append_ref_class,
            'append_ref_member': append_ref_member
        }, children=body, line=constr_line, column=constr_column)

    def _parse_qualified_method_ref(self) -> str:
        """Parse a qualified method reference like 'ParentClass::methodName' or just 'methodName'.

        Returns the qualified name as a string (e.g., 'Parent::init' or just 'init').
        """
        # Check for $PythonObject
        if self._check(TokenType.SHARED_REF):
            class_ref = self._advance().value  # Gets the name without $
            class_ref = f'${class_ref}'
        elif self._check(TokenType.IDENTIFIER):
            class_ref = self._advance().value
        else:
            raise CSSLSyntaxError("Expected class or method name in extends/overwrites")

        # Check for :: to get method part
        if self._match(TokenType.DOUBLE_COLON):
            if self._check(TokenType.IDENTIFIER):
                method_ref = self._advance().value
                return f'{class_ref}::{method_ref}'
            else:
                raise CSSLSyntaxError("Expected method name after '::'")

        # Just method name, no class qualifier
        return class_ref

    def _parse_parameter_list(self) -> list:
        """Parse a list of parameters (without the surrounding parentheses).

        Returns a list of parameter definitions, each can be:
        - Simple string name: "paramName"
        - Dict with type info: {'name': 'paramName', 'type': 'string', 'ref': True, ...}
        """
        params = []
        while not self._check(TokenType.PAREN_END) and not self._is_at_end():
            param_info = {}

            # Handle 'open' keyword for open parameters
            if self._match_keyword('open'):
                param_info['open'] = True

            # Handle type annotations (e.g., string, int, dynamic, python::list, etc.)
            if self._check(TokenType.KEYWORD):
                type_val = self._advance().value
                # v4.9.8: Handle python::type composite types (python::list, python::dict, etc.)
                if type_val == 'python' and self._check(TokenType.DOUBLE_COLON):
                    self._advance()  # consume ::
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                        type_val = 'python::' + self._advance().value
                    else:
                        type_val = 'python::object'
                param_info['type'] = type_val

            # Handle reference operator &
            if self._match(TokenType.AMPERSAND):
                param_info['ref'] = True

            # Handle * prefix for non-null parameters
            if self._match(TokenType.MULTIPLY):
                param_info['non_null'] = True

            # Get parameter name
            if self._check(TokenType.IDENTIFIER):
                param_name = self._advance().value
                if param_info:
                    params.append({'name': param_name, **param_info})
                else:
                    params.append(param_name)
                self._match(TokenType.COMMA)
            elif self._check(TokenType.KEYWORD):
                # Parameter name could be a keyword like 'Params'
                param_name = self._advance().value
                if param_info:
                    params.append({'name': param_name, **param_info})
                else:
                    params.append(param_name)
                self._match(TokenType.COMMA)
            else:
                break

        return params

    def _parse_define(self, is_global: bool = False, is_embedded: bool = False, has_open_params: bool = False, modifiers: list = None) -> ASTNode:
        """Parse define function declaration.

        Syntax:
            define MyFunc(args) { }                    // Local function
            global define MyFunc(args) { }             // Global function
            private define MyFunc(args) { }            // Private function (v4.5.1)
            define @MyFunc(args) { }                   // Global function (alternative)
            define *MyFunc(args) { }                   // Non-null: must never return None
            define MyFunc(args) : extends OtherFunc { }     // Inherit local vars
            define MyFunc(args) : overwrites OtherFunc { }  // Replace OtherFunc
            define MyFunc(args) : supports python { }       // Multi-language syntax
            define MyFunc(args) :: extends Parent::Method { }  // Method-level inheritance
            embedded define MyFunc(args) &target { }       // Immediate &target replacement
            open embedded define MyFunc(open Input) &target { }  // Open params + embedded
        """
        # Check for * prefix (non-null function - must return non-null)
        # Also *[type] for type exclusion (must NOT return that type)
        non_null = False
        exclude_type = None
        if self._match(TokenType.MULTIPLY):
            # Check for type exclusion filter: *[string], *[int], etc.
            if self._check(TokenType.BRACKET_START):
                self._advance()  # consume [
                exclude_type = self._advance().value  # get type name
                self._expect(TokenType.BRACKET_END)
            else:
                non_null = True

        # Check for @ prefix (global function): define @FuncName
        if self._check(TokenType.AT):
            self._advance()  # consume @
            is_global = True

        name_token = self._advance()
        name = name_token.value
        func_line = name_token.line
        func_column = name_token.column

        # Parse parameters FIRST (before :extends/:overwrites/:supports)
        # Syntax: define funcName(params) : extends/overwrites/supports { }
        params = []

        if self._match(TokenType.PAREN_START):
            while not self._check(TokenType.PAREN_END):
                param_info = {}
                # Handle 'open' keyword for open parameters
                if self._match_keyword('open'):
                    param_info['open'] = True
                # Handle type annotations (e.g., string, int, dynamic, python::list, etc.)
                # v4.9.2: Also handle TYPE_LITERAL (dict, list) which are tokenized differently
                if (self._check(TokenType.KEYWORD) and self._is_type_keyword(self._current().value)) or \
                   self._check(TokenType.TYPE_LITERAL):
                    type_val = self._advance().value
                    # v4.9.8: Handle python::type composite types
                    if type_val == 'python' and self._check(TokenType.DOUBLE_COLON):
                        self._advance()  # consume ::
                        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                            type_val = 'python::' + self._advance().value
                        else:
                            type_val = 'python::object'
                    param_info['type'] = type_val
                # Handle reference operator &
                if self._match(TokenType.AMPERSAND):
                    param_info['ref'] = True
                # Handle * prefix for non-null parameters
                if self._match(TokenType.MULTIPLY):
                    param_info['non_null'] = True
                # Get parameter name
                if self._check(TokenType.IDENTIFIER):
                    param_name = self._advance().value
                    # v4.2.0: Handle default parameter values (param = value)
                    if self._match(TokenType.EQUALS):
                        default_value = self._parse_expression()
                        param_info['default'] = default_value
                    if param_info:
                        params.append({'name': param_name, **param_info})
                    else:
                        params.append(param_name)
                    self._match(TokenType.COMMA)
                elif self._check(TokenType.KEYWORD):
                    # Parameter name could be a keyword like 'Params'
                    param_name = self._advance().value
                    # v4.2.0: Handle default parameter values (param = value)
                    if self._match(TokenType.EQUALS):
                        default_value = self._parse_expression()
                        param_info['default'] = default_value
                    if param_info:
                        params.append({'name': param_name, **param_info})
                    else:
                        params.append(param_name)
                    self._match(TokenType.COMMA)
                else:
                    break
            self._expect(TokenType.PAREN_END)

        # Check for extends/overwrites/supports AFTER parameters
        # Syntax: define func(params) : extends/overwrites target { }
        # Also supports method-level :: syntax: define func() :: extends Parent::method
        extends_func = None
        overwrites_func = None
        extends_is_python = False
        overwrites_is_python = False
        extends_class_ref = None
        extends_method_ref = None
        overwrites_class_ref = None
        overwrites_method_ref = None
        supports_language = None  # v4.1.0: Multi-language syntax support
        uses_memory = None  # v4.9.0: Memory binding for deferred execution
        copies_memory_target = None  # v4.9.9: Copy another function's local scope
        overwrites_memory_target = None  # v4.9.9: Overwrite another function's local scope

        if self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON):
            # Parse extends and/or overwrites (supports :: method-level syntax)
            while True:
                if self._match_keyword('extends'):
                    # Check for qualified reference: Parent::method
                    if self._check(TokenType.SHARED_REF):
                        extends_is_python = True
                        extends_func = self._advance().value
                        # Check for ::method
                        if self._match(TokenType.DOUBLE_COLON):
                            extends_class_ref = f'${extends_func}'
                            if self._check(TokenType.IDENTIFIER):
                                extends_method_ref = self._advance().value
                            else:
                                raise CSSLSyntaxError("Expected method name after '::'")
                    elif self._check(TokenType.IDENTIFIER):
                        first_part = self._advance().value
                        # Check for ::method (qualified reference)
                        if self._match(TokenType.DOUBLE_COLON):
                            extends_class_ref = first_part
                            if self._check(TokenType.IDENTIFIER):
                                extends_method_ref = self._advance().value
                            else:
                                raise CSSLSyntaxError("Expected method name after '::'")
                        else:
                            extends_func = first_part
                    else:
                        raise CSSLSyntaxError("Expected function name after 'extends'")
                    # Skip optional () after function/method name
                    if self._match(TokenType.PAREN_START):
                        self._expect(TokenType.PAREN_END)
                elif self._match_keyword('overwrites'):
                    # v4.9.9: Check for 'overwrites memory(FuncName)' - overwrite another function's local scope
                    if (self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD)) and self._current().value == 'memory':
                        self._advance()  # consume 'memory'
                        self._expect(TokenType.PAREN_START)
                        overwrites_memory_target = self._advance().value  # Get function name
                        self._expect(TokenType.PAREN_END)
                    # Check for qualified reference: Parent::method
                    elif self._check(TokenType.SHARED_REF):
                        overwrites_is_python = True
                        overwrites_func = self._advance().value
                        # Check for ::method
                        if self._match(TokenType.DOUBLE_COLON):
                            overwrites_class_ref = f'${overwrites_func}'
                            if self._check(TokenType.IDENTIFIER):
                                overwrites_method_ref = self._advance().value
                            else:
                                raise CSSLSyntaxError("Expected method name after '::'")
                    elif self._check(TokenType.IDENTIFIER):
                        first_part = self._advance().value
                        # Check for ::method (qualified reference)
                        if self._match(TokenType.DOUBLE_COLON):
                            overwrites_class_ref = first_part
                            if self._check(TokenType.IDENTIFIER):
                                overwrites_method_ref = self._advance().value
                            else:
                                raise CSSLSyntaxError("Expected method name after '::'")
                        else:
                            overwrites_func = first_part
                    else:
                        raise CSSLSyntaxError("Expected function name after 'overwrites'")
                    # Skip optional () after function/method name
                    if self._match(TokenType.PAREN_START):
                        self._expect(TokenType.PAREN_END)
                # v4.1.0: Parse 'supports' keyword for multi-language syntax
                elif self._match_keyword('supports'):
                    if self._check(TokenType.AT):
                        self._advance()  # consume @
                        if self._check(TokenType.IDENTIFIER):
                            supports_language = '@' + self._advance().value
                        else:
                            raise CSSLSyntaxError("Expected language identifier after '@' in 'supports'")
                    elif self._check(TokenType.IDENTIFIER):
                        supports_language = self._advance().value
                    else:
                        raise CSSLSyntaxError("Expected language identifier after 'supports'")
                # v4.9.0: Parse 'uses' keyword for memory binding (deferred execution)
                # Syntax: define func() : uses memory(address) { }
                elif self._match_keyword('uses'):
                    if (self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD)) and self._current().value == 'memory':
                        self._advance()  # consume 'memory'
                        self._expect(TokenType.PAREN_START)
                        uses_memory = self._parse_expression()  # Parse the address expression
                        self._expect(TokenType.PAREN_END)
                    else:
                        raise CSSLSyntaxError("Expected 'memory(address)' after 'uses'")
                # v4.9.9: Parse 'copies memory(FuncName)' - copy another function's local scope
                # Syntax: define func() : copies memory(SecureMethod) { }
                elif self._match_keyword('copies'):
                    if (self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD)) and self._current().value == 'memory':
                        self._advance()  # consume 'memory'
                        self._expect(TokenType.PAREN_START)
                        copies_memory_target = self._advance().value  # Get function name
                        self._expect(TokenType.PAREN_END)
                    else:
                        raise CSSLSyntaxError("Expected 'memory(FuncName)' after 'copies'")
                else:
                    break
                # Check for another :: or : for chaining extends/overwrites
                if not (self._match(TokenType.DOUBLE_COLON) or self._match(TokenType.COLON)):
                    break

        # New: Append mode and reference tracking for functions
        # Syntax: define XYZ(int zahl) &overwrittenclass::functionyouwanttokeep ++ { ... }
        append_mode = False
        append_ref_class = None
        append_ref_member = None
        append_position = None  # v4.9.2: Optional position for hook placement (e.g., &name[-1])

        # Check for &ClassName::member or &builtinName reference
        # v4.9.2: Support &builtinName ++ for hooking into builtin functions
        if self._match(TokenType.AMPERSAND):
            if self._check(TokenType.IDENTIFIER):
                ref_name = self._advance().value
            elif self._check(TokenType.KEYWORD):
                # v4.9.2: Allow keywords as function names (e.g., &reflect, &address)
                ref_name = self._advance().value
            elif self._check(TokenType.SHARED_REF):
                ref_name = f'${self._advance().value}'
            elif self._check(TokenType.AT):
                # &@globalFunc reference
                self._advance()  # consume @
                if self._check(TokenType.IDENTIFIER):
                    ref_name = '@' + self._advance().value
                else:
                    raise CSSLSyntaxError("Expected identifier after '&@'")
            elif self._check(TokenType.TYPE_LITERAL):
                # v4.9.2: Allow type literals as function names (dict, list)
                ref_name = self._advance().value
            else:
                # Debug: show what token we got
                cur = self._current()
                raise CSSLSyntaxError(f"Expected function/class name after '&' in function reference, got {cur.type.name}='{cur.value}'")

            # Check for ::member (class method reference)
            if self._match(TokenType.DOUBLE_COLON):
                # It's a class::member reference
                append_ref_class = ref_name
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                    append_ref_member = self._advance().value
                else:
                    raise CSSLSyntaxError("Expected member name after '::' in function reference")
            else:
                # v4.9.2: No ::, it's a builtin function reference like &reflect
                # Store as special builtin reference (class=None, member=builtinName)
                append_ref_class = '__builtins__'
                append_ref_member = ref_name

            # v4.9.2: Check for position syntax [index] (e.g., &name[-1] to place hook before last statement)
            if self._match(TokenType.BRACKET_START):
                # Parse the position expression (usually a number, can be negative)
                pos_expr = self._parse_expression()
                self._expect(TokenType.BRACKET_END)
                # Store the position expression - will be evaluated at runtime
                append_position = pos_expr

        # Check for ++ append operator
        if self._match(TokenType.PLUS_PLUS):
            append_mode = True

        # v4.2.0: Allow 'supports' AFTER &Class::member reference
        # Syntax: define func() &$pyclass::method : supports python { }
        if self._match(TokenType.COLON) or self._match(TokenType.DOUBLE_COLON):
            if self._match_keyword('supports'):
                if self._check(TokenType.AT):
                    self._advance()
                    if self._check(TokenType.IDENTIFIER):
                        supports_language = '@' + self._advance().value
                    else:
                        raise CSSLSyntaxError("Expected language identifier after '@' in 'supports'")
                elif self._check(TokenType.IDENTIFIER):
                    supports_language = self._advance().value
                else:
                    raise CSSLSyntaxError("Expected language identifier after 'supports'")

        self._expect(TokenType.BLOCK_START)

        # v4.2.0: Extract raw body when supports_language is set for transformation
        raw_body = None
        children = []
        if supports_language:
            raw_body = self._extract_raw_block_body()
            # _extract_raw_block_body positions cursor at BLOCK_END
        # v4.7: Special parsing for bytearrayed functions
        elif modifiers and 'bytearrayed' in modifiers:
            children = self._parse_bytearrayed_body()
        else:
            is_undefined = modifiers and 'undefined' in modifiers
            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                if is_undefined:
                    try:
                        stmt = self._parse_statement()
                        if stmt:
                            children.append(stmt)
                    except (CSSLSyntaxError, Exception):
                        self._skip_to_next_statement()
                else:
                    stmt = self._parse_statement()
                    if stmt:
                        children.append(stmt)

        self._expect(TokenType.BLOCK_END)

        node = ASTNode('function', value={
            'name': name,
            'is_global': is_global,
            'is_embedded': is_embedded,  # v4.2.5: immediate &target replacement (v4.3.2: use param)
            'has_open_params': has_open_params,  # v4.3.2: open embedded define support
            'params': params,
            'non_null': non_null,
            'exclude_type': exclude_type,  # *[type] - must NOT return this type
            'extends': extends_func,
            'extends_is_python': extends_is_python,
            'overwrites': overwrites_func,
            'overwrites_is_python': overwrites_is_python,
            # Method-level inheritance (Parent::method syntax)
            'extends_class': extends_class_ref,
            'extends_method': extends_method_ref,
            'overwrites_class': overwrites_class_ref,
            'overwrites_method': overwrites_method_ref,
            # New append mode fields
            'append_mode': append_mode,
            'append_ref_class': append_ref_class,
            'append_ref_member': append_ref_member,
            'append_position': append_position,  # v4.9.2: Position for hook placement
            # v4.1.0: Multi-language support
            'supports_language': supports_language,
            # v4.2.0: Raw body for language transformation
            'raw_body': raw_body,
            # v4.5.1: Function modifiers (private, const, static, etc.)
            'modifiers': modifiers or [],
            # v4.9.0: Memory binding for deferred execution
            'uses_memory': uses_memory,
            # v4.9.9: Copy another function's local scope
            'copies_memory': copies_memory_target,
            # v4.9.9: Overwrite another function's local scope
            'overwrites_memory': overwrites_memory_target
        }, children=children, line=func_line, column=func_column)

        return node

    def _parse_statement(self) -> Optional[ASTNode]:
        if self._match_keyword('if'):
            return self._parse_if()
        elif self._match_keyword('while'):
            return self._parse_while()
        elif self._match_keyword('for'):
            return self._parse_for()
        elif self._match_keyword('foreach'):
            return self._parse_foreach()
        elif self._match_keyword('switch'):
            return self._parse_switch()
        elif self._match_keyword('return'):
            return self._parse_return()
        elif self._match_keyword('break'):
            self._match(TokenType.SEMICOLON)
            return ASTNode('break')
        elif self._match_keyword('continue'):
            self._match(TokenType.SEMICOLON)
            return ASTNode('continue')
        # v4.5.1: Add throw statement parsing
        elif self._match_keyword('throw'):
            return self._parse_throw()
        # v4.8: Add raise statement (Python-style: raise ExceptionType("message"))
        elif self._match_keyword('raise'):
            return self._parse_raise()
        elif self._match_keyword('try'):
            return self._parse_try()
        elif self._match_keyword('await'):
            return self._parse_await()
        elif self._match_keyword('yield'):
            return self._parse_yield()
        elif self._match_keyword('supports'):
            # v4.2.0: Standalone supports block for multi-language syntax
            return self._parse_supports_block()
        elif self._match_keyword('enum'):
            return self._parse_enum()
        elif self._match_keyword('define'):
            # Nested define function
            return self._parse_define()
        elif self._match_keyword('global'):
            # v4.9.2: Global variable inside function: global int x = 1; or global x = 1;
            if self._looks_like_typed_variable():
                # global type varName = value;
                typed_node = self._parse_typed_variable()
                if typed_node and typed_node.type == 'typed_declaration':
                    # Add 'global' to modifiers
                    modifiers = typed_node.value.get('modifiers', [])
                    modifiers.append('global')
                    typed_node.value['modifiers'] = modifiers
                return typed_node
            else:
                # global varName = value; (dynamic type)
                stmt = self._parse_expression_statement()
                if stmt:
                    return ASTNode('global_assignment', value=stmt)
                return None
        elif self._check(TokenType.KEYWORD) and self._current().value == 'freezed':
            # v4.9.7: Handle freezed as standalone modifier
            # freezed %var        — freeze existing snapshot
            # freezed snapshot(x) — snapshot and freeze
            saved_pos = self.pos
            self._advance()  # consume 'freezed'

            if self._check(TokenType.CAPTURED_REF):
                # freezed %var — freeze an existing snapshot variable
                snap_name = self._advance().value
                self._match(TokenType.SEMICOLON)
                return ASTNode('freeze_snapshot', value={'name': snap_name})
            elif self._check(TokenType.IDENTIFIER) and self._current().value == 'snapshot':
                # freezed snapshot(x) — snapshot and freeze
                expr = self._parse_expression_statement()
                return ASTNode('freeze_snapshot_call', value={'call': expr})
            else:
                # Fall back to typed variable: freezed int x = 5;
                self.pos = saved_pos
                if self._looks_like_typed_variable():
                    return self._parse_typed_variable()
                # Unknown — parse as expression
                self._advance()  # re-consume 'freezed'
                return self._parse_expression_statement()
        elif self._looks_like_typed_variable():
            # Typed variable declaration (e.g., stack<string> myStack;)
            return self._parse_typed_variable()
        elif self._looks_like_function_declaration():
            # Nested typed function (e.g., void Level2() { ... })
            return self._parse_typed_function()
        elif self._check(TokenType.SUPER_FUNC):
            # Super-function for .cssl-pl payload files
            return self._parse_super_function()
        elif (self._check(TokenType.KEYWORD) and self._current().value == 'super' and
              (self._peek(1).type == TokenType.PAREN_START or
               self._peek(1).type == TokenType.DOUBLE_COLON)):
            # super() or super::method() call - calls parent constructor/method
            return self._parse_super_call()
        # v4.2.1: Added LANG_INSTANCE_REF for lang$instance statements
        # v4.9.0: Allow KEYWORD tokens followed by ( to be treated as function calls (memory, uses, etc.)
        # v4.9.0: Added POINTER_REF for ?name = value pointer assignments
        # v4.9.4: Added POINTER_SNAPSHOT_REF for ?%name pointer-snapshot references
        elif (self._check(TokenType.IDENTIFIER) or self._check(TokenType.AT) or
              self._check(TokenType.CAPTURED_REF) or self._check(TokenType.SHARED_REF) or
              self._check(TokenType.POINTER_REF) or self._check(TokenType.POINTER_SNAPSHOT_REF) or
              self._check(TokenType.GLOBAL_REF) or self._check(TokenType.SELF_REF) or
              self._check(TokenType.LANG_INSTANCE_REF) or
              (self._check(TokenType.KEYWORD) and self._current().value in ('this', 'new')) or
              (self._check(TokenType.KEYWORD) and self._peek(1) and self._peek(1).type == TokenType.PAREN_START) or
              self._looks_like_namespace_call()):
            return self._parse_expression_statement()
        else:
            self._advance()
            return None

    def _parse_super_call(self) -> ASTNode:
        """Parse super() call to invoke parent constructor or method.

        Syntax:
            super()              - Call parent constructor with no args
            super(arg1, arg2)    - Call parent constructor with args
            super::method()      - Call specific parent method
            super::method(args)  - Call specific parent method with args

        Used inside constructors (constr) and methods to call parent implementations.
        """
        # Consume 'super' keyword
        self._advance()

        # Check for ::method syntax
        target_method = None
        if self._match(TokenType.DOUBLE_COLON):
            if not self._check(TokenType.IDENTIFIER):
                raise CSSLSyntaxError("Expected method name after 'super::'")
            target_method = self._advance().value

        # Parse arguments
        args = []
        self._expect(TokenType.PAREN_START)
        while not self._check(TokenType.PAREN_END):
            arg = self._parse_expression()
            args.append(arg)
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.PAREN_END)
        self._match(TokenType.SEMICOLON)

        return ASTNode('super_call', value={
            'method': target_method,  # None for constructor, method name for specific method
            'args': args
        })

    def _parse_if(self) -> ASTNode:
        """Parse if statement with support for else if AND elif syntax."""
        self._expect(TokenType.PAREN_START)
        condition = self._parse_expression()
        self._expect(TokenType.PAREN_END)

        node = ASTNode('if', value={'condition': condition}, children=[])

        self._expect(TokenType.BLOCK_START)
        then_block = ASTNode('then', children=[])
        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                then_block.children.append(stmt)
        self._expect(TokenType.BLOCK_END)
        node.children.append(then_block)

        # Support both 'else if' AND 'elif' syntax
        if self._match_keyword('elif'):
            # elif is shorthand for else if
            else_block = ASTNode('else', children=[])
            else_block.children.append(self._parse_if())
            node.children.append(else_block)
        elif self._match_keyword('else'):
            else_block = ASTNode('else', children=[])
            if self._match_keyword('if'):
                else_block.children.append(self._parse_if())
            else:
                self._expect(TokenType.BLOCK_START)
                while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                    stmt = self._parse_statement()
                    if stmt:
                        else_block.children.append(stmt)
                self._expect(TokenType.BLOCK_END)
            node.children.append(else_block)

        return node

    def _parse_while(self) -> ASTNode:
        self._expect(TokenType.PAREN_START)
        condition = self._parse_expression()
        self._expect(TokenType.PAREN_END)

        node = ASTNode('while', value={'condition': condition}, children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                node.children.append(stmt)

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_for(self) -> ASTNode:
        """Parse for loop - supports both syntaxes:

        Python-style: for (i in range(0, n)) { }
        C-style: for (int i = 0; i < n; i = i + 1) { }
                 for (i = 0; i < n; i++) { }
        """
        self._expect(TokenType.PAREN_START)

        # Detect C-style by checking for semicolons in the for header
        # Look ahead without consuming tokens
        is_c_style = self._detect_c_style_for()

        if is_c_style:
            # C-style: for (init; condition; update) { }
            return self._parse_c_style_for()
        else:
            # Python-style: for (var in range(start, end)) { }
            return self._parse_python_style_for()

    def _detect_c_style_for(self) -> bool:
        """Detect if this is a C-style for loop by looking for semicolons."""
        # Scan the tokens list directly without modifying self.pos
        pos = self.pos
        paren_depth = 1

        while pos < len(self.tokens) and paren_depth > 0:
            token = self.tokens[pos]
            if token.type == TokenType.PAREN_START:
                paren_depth += 1
            elif token.type == TokenType.PAREN_END:
                paren_depth -= 1
            elif token.type == TokenType.SEMICOLON and paren_depth == 1:
                # Found semicolon at top level - C-style
                return True
            elif token.type == TokenType.KEYWORD and token.value == 'in':
                # Found 'in' keyword - Python-style
                return False
            pos += 1

        return False  # Default to Python-style

    def _parse_c_style_for(self) -> ASTNode:
        """Parse C-style for loop: for (init; condition; update) { }"""
        # Parse init statement
        init = None
        if not self._check(TokenType.SEMICOLON):
            # Check if it's a typed declaration: int i = 0
            if self._check(TokenType.KEYWORD) and self._peek().value in ('int', 'float', 'string', 'bool', 'dynamic'):
                type_name = self._advance().value
                var_name = self._advance().value
                self._expect(TokenType.EQUALS)
                value = self._parse_expression()
                init = ASTNode('c_for_init', value={
                    'type': type_name,
                    'var': var_name,
                    'value': value
                })
            else:
                # Could be simple assignment (i = 0) or bare expression (i < n.size())
                saved_pos = self.pos
                var_name = self._advance().value
                if self._check(TokenType.EQUALS):
                    # Simple assignment: i = 0
                    self._advance()  # consume =
                    value = self._parse_expression()
                    init = ASTNode('c_for_init', value={
                        'type': None,
                        'var': var_name,
                        'value': value
                    })
                else:
                    # Bare expression as init (e.g. i < n.size(), or just i)
                    self.pos = saved_pos
                    expr = self._parse_expression()
                    init = ASTNode('c_for_init', value={
                        'type': None,
                        'var': None,
                        'expr': expr
                    })

        self._expect(TokenType.SEMICOLON)

        # Parse condition
        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._parse_expression()

        self._expect(TokenType.SEMICOLON)

        # Parse update statement
        update = None
        if not self._check(TokenType.PAREN_END):
            # Could be: i = i + 1, i++, ++i, i += 1
            update = self._parse_c_for_update()

        self._expect(TokenType.PAREN_END)

        node = ASTNode('c_for', value={
            'init': init,
            'condition': condition,
            'update': update
        }, children=[])

        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                node.children.append(stmt)

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_c_for_update(self) -> ASTNode:
        """Parse the update part of a C-style for loop.

        Supports: i = i + 1, i++, ++i, i += 1, i -= 1
        """
        # Check for prefix increment/decrement: ++i or --i (as single PLUS_PLUS/MINUS_MINUS token)
        if self._check(TokenType.PLUS_PLUS):
            self._advance()
            var_name = self._advance().value
            return ASTNode('c_for_update', value={'var': var_name, 'op': 'increment'})
        elif self._check(TokenType.MINUS_MINUS):
            self._advance()
            var_name = self._advance().value
            return ASTNode('c_for_update', value={'var': var_name, 'op': 'decrement'})

        # Regular variable assignment or postfix
        var_name = self._advance().value

        # Check for postfix increment/decrement: i++ or i-- (as single PLUS_PLUS/MINUS_MINUS token)
        if self._check(TokenType.PLUS_PLUS):
            self._advance()
            return ASTNode('c_for_update', value={'var': var_name, 'op': 'increment'})
        elif self._check(TokenType.MINUS_MINUS):
            self._advance()
            return ASTNode('c_for_update', value={'var': var_name, 'op': 'decrement'})
        # i += value
        elif self._check(TokenType.PLUS):
            self._advance()
            if self._check(TokenType.EQUALS):
                self._advance()
                value = self._parse_expression()
                return ASTNode('c_for_update', value={'var': var_name, 'op': 'add', 'value': value})
        # i -= value
        elif self._check(TokenType.MINUS):
            self._advance()
            if self._check(TokenType.EQUALS):
                self._advance()
                value = self._parse_expression()
                return ASTNode('c_for_update', value={'var': var_name, 'op': 'subtract', 'value': value})

        # Regular assignment: i = expression
        if self._check(TokenType.EQUALS):
            self._advance()
            value = self._parse_expression()
            return ASTNode('c_for_update', value={'var': var_name, 'op': 'assign', 'value': value})

        # Just the variable (shouldn't happen but handle it)
        return ASTNode('c_for_update', value={'var': var_name, 'op': 'none'})

    def _parse_python_style_for(self) -> ASTNode:
        """Parse Python-style for loop: for (i in range(...)) { } or for (item in collection) { }

        Supports:
            for (i in range(n)) { }           - 0 to n-1
            for (i in range(start, end)) { }  - start to end-1
            for (i in range(start, end, step)) { }
            for (item in collection) { }      - iterate over list/vector
            for (item in @global_collection) { } - iterate over global
        """
        var_name = self._advance().value
        self._expect(TokenType.KEYWORD)  # 'in'

        # Check if this is range() or collection iteration
        is_range = False
        if self._check(TokenType.KEYWORD) and self._peek().value == 'range':
            self._advance()  # consume 'range' keyword
            is_range = True
        elif self._check(TokenType.IDENTIFIER) and self._peek().value == 'range':
            self._advance()  # consume 'range' identifier
            is_range = True

        # If not range, parse as collection iteration
        if not is_range:
            iterable = self._parse_expression()
            self._expect(TokenType.PAREN_END)

            node = ASTNode('foreach', value={'var': var_name, 'iterable': iterable}, children=[])
            self._expect(TokenType.BLOCK_START)

            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    node.children.append(stmt)

            self._expect(TokenType.BLOCK_END)
            return node

        self._expect(TokenType.PAREN_START)
        first_arg = self._parse_expression()

        # Check if there are more arguments
        start = None
        end = None
        step = None

        if self._check(TokenType.COMMA):
            # range(start, end) or range(start, end, step)
            self._advance()  # consume comma
            start = first_arg
            end = self._parse_expression()

            # Optional step parameter
            if self._check(TokenType.COMMA):
                self._advance()  # consume comma
                step = self._parse_expression()
        else:
            # range(n) - single argument means 0 to n-1
            start = ASTNode('literal', value={'type': 'int', 'value': 0})
            end = first_arg

        self._expect(TokenType.PAREN_END)
        self._expect(TokenType.PAREN_END)

        node = ASTNode('for', value={'var': var_name, 'start': start, 'end': end, 'step': step}, children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                node.children.append(stmt)

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_foreach(self) -> ASTNode:
        """Parse foreach loop - supports both syntaxes:

        Traditional: foreach (var in iterable) { }
        Traditional with assertion: foreach ([case]*[default]var in iterable) { }
        New 'as' syntax: foreach iterable as var { }
        """
        # Check if this is the new 'as' syntax or traditional syntax
        if self._check(TokenType.PAREN_START):
            # Traditional syntax: foreach (var in iterable) { }
            self._expect(TokenType.PAREN_START)

            # v4.9.7: Support non-null/conditional assertion on loop variable
            # e.g., foreach ([10]*[9]x in n) { }
            # Parse [case]*[default] prefix manually, then grab var name
            var_assertion = None
            if self._check(TokenType.BRACKET_START):
                # Parse [condition]
                self._advance()  # consume [
                condition = self._parse_expression()
                self._expect(TokenType.BRACKET_END)

                # Check for *[fallback] pattern
                if self._check(TokenType.MULTIPLY):
                    self._advance()  # consume *
                    self._expect(TokenType.BRACKET_START)
                    fallback = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)

                    # Now grab the variable name
                    var_name = self._advance().value
                    var_assertion = ASTNode('conditional_assert', value={
                        'condition': condition,
                        'fallback': fallback,
                        'operand': ASTNode('identifier', value=var_name)
                    })
                else:
                    # Just [fallback] without condition — treat as non-null fallback
                    var_name = self._advance().value
                    var_assertion = ASTNode('non_null_assert_fallback', value={
                        'fallback': condition,
                        'operand': ASTNode('identifier', value=var_name)
                    })
            else:
                var_name = self._advance().value

            # Support key-value iteration: foreach (k, v in dict) { }
            value_var = None
            if self._match(TokenType.COMMA):
                value_var = self._advance().value

            self._match_keyword('in')
            iterable = self._parse_expression()
            self._expect(TokenType.PAREN_END)
        else:
            # NEW: 'as' syntax: foreach iterable as var { }
            var_assertion = None
            value_var = None
            iterable = self._parse_expression()
            if self._check(TokenType.AS):
                self._advance()  # consume 'as'
            else:
                self._match_keyword('as')  # try keyword match as fallback
            var_name = self._advance().value

        foreach_value = {'var': var_name, 'iterable': iterable}
        # Key-value iteration: foreach (k, v in dict)
        if value_var is not None:
            foreach_value['value_var'] = value_var
        # v4.9.7: Include assertion info if present
        if var_assertion is not None:
            foreach_value['var_assertion'] = var_assertion
        node = ASTNode('foreach', value=foreach_value, children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                node.children.append(stmt)

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_switch(self) -> ASTNode:
        self._expect(TokenType.PAREN_START)
        value = self._parse_expression()
        self._expect(TokenType.PAREN_END)

        # v4.2.5: Check if this is a param switch (switch on open params)
        # Syntax: switch(Params): case name: ... except age: ... always: ... finally: ...
        # v4.3.2: Detect param_switch by:
        #   1. Explicit "Params" identifier, OR
        #   2. Any identifier if case uses param-style conditions (& / not)
        is_param_switch = (value.type == 'identifier' and value.value == 'Params')

        # v4.3.2: Also check if case syntax uses param-style conditions
        # Look ahead to see if first case uses & or 'not' operators
        if not is_param_switch and value.type == 'identifier':
            saved_pos = self.pos
            # Skip optional : and {
            if self._check(TokenType.COLON):
                self._advance()
            if self._check(TokenType.BLOCK_START):
                self._advance()
            # Check for 'case' keyword
            if self._check_keyword('case'):
                self._advance()  # skip 'case'
                # Look for & or 'not' before : (indicates param switch)
                depth = 0
                while not self._is_at_end():
                    if self._check(TokenType.COLON) and depth == 0:
                        break
                    if self._check(TokenType.PAREN_START):
                        depth += 1
                    if self._check(TokenType.PAREN_END):
                        depth -= 1
                    if self._check(TokenType.AMPERSAND) or self._check_keyword('not') or self._check(TokenType.NOT):
                        is_param_switch = True
                        break
                    self._advance()
            self.pos = saved_pos  # Restore position

        if is_param_switch:
            return self._parse_param_switch(value)

        # Regular switch
        node = ASTNode('switch', value={'value': value}, children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._match_keyword('case'):
                case_value = self._parse_expression()
                self._expect(TokenType.COLON)
                case_node = ASTNode('case', value={'value': case_value}, children=[])

                while not self._check_keyword('case') and not self._check_keyword('default') and not self._check(TokenType.BLOCK_END):
                    stmt = self._parse_statement()
                    if stmt:
                        case_node.children.append(stmt)
                    if self._check_keyword('break'):
                        break

                node.children.append(case_node)
            elif self._match_keyword('default'):
                self._expect(TokenType.COLON)
                default_node = ASTNode('default', children=[])

                while not self._check(TokenType.BLOCK_END):
                    stmt = self._parse_statement()
                    if stmt:
                        default_node.children.append(stmt)

                node.children.append(default_node)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_param_switch(self, params_identifier: ASTNode) -> ASTNode:
        """Parse param switch for open parameters.

        v4.2.5: Switch on which parameters were provided.

        Syntax:
            switch(Params): or switch(Params) {
                case name:              // if 'name' param exists
                    ...
                    break;
                case name & age:        // if both 'name' AND 'age' exist
                    ...
                    break;
                case name & not age:    // if 'name' exists but 'age' doesn't
                    ...
                    break;
                except name:            // if 'name' does NOT exist (alias for 'case not name')
                    ...
                    break;
                default:                // fallback if no case matches
                    ...
                always:                 // always runs after a matching case
                    ...
                finally:                // cleanup, runs last regardless
                    ...
            }
        """
        # Allow both : and { as block start
        if self._match(TokenType.COLON):
            pass  # Python-style with :
        self._expect(TokenType.BLOCK_START)

        node = ASTNode('param_switch', value={
            'params': params_identifier.value  # The open params variable name
        }, children=[])

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._match_keyword('case'):
                # Parse param condition: name, name & age, name & not age
                condition = self._parse_param_condition()
                self._expect(TokenType.COLON)

                case_node = ASTNode('param_case', value={'condition': condition}, children=[])
                self._parse_case_body(case_node)
                node.children.append(case_node)

            elif self._match_keyword('except'):
                # except name: is alias for case not name:
                param_name = self._advance().value
                self._expect(TokenType.COLON)

                condition = {'type': 'not', 'param': param_name}
                case_node = ASTNode('param_case', value={'condition': condition}, children=[])
                self._parse_case_body(case_node)
                node.children.append(case_node)

            elif self._match_keyword('default'):
                self._expect(TokenType.COLON)
                default_node = ASTNode('param_default', children=[])
                self._parse_case_body(default_node)
                node.children.append(default_node)

            elif self._match_keyword('always'):
                self._expect(TokenType.COLON)
                always_node = ASTNode('param_always', children=[])
                self._parse_case_body(always_node)
                node.children.append(always_node)

            elif self._match_keyword('finally'):
                self._expect(TokenType.COLON)
                finally_node = ASTNode('param_finally', children=[])
                self._parse_case_body(finally_node)
                node.children.append(finally_node)

            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_param_condition(self) -> dict:
        """Parse param switch condition.

        v4.3.2: Enhanced to support multiple styles:
            name            -> {'type': 'exists', 'param': 'name'}
            not name        -> {'type': 'not', 'param': 'name'}
            !name           -> {'type': 'not', 'param': 'name'}
            name & age      -> {'type': 'and', 'left': {...}, 'right': {...}}
            name & not age  -> {'type': 'and', 'left': {...}, 'right': {'type': 'not', ...}}
            name & !age     -> {'type': 'and', 'left': {...}, 'right': {'type': 'not', ...}}
            name || age     -> {'type': 'or', 'left': {...}, 'right': {...}}
        """
        # Check for 'not' or '!' prefix
        negated = self._match_keyword('not') or self._match(TokenType.NOT)
        param_name = self._advance().value

        if negated:
            condition = {'type': 'not', 'param': param_name}
        else:
            condition = {'type': 'exists', 'param': param_name}

        # Check for & (AND) or || (OR) combinations
        while True:
            if self._match(TokenType.AMPERSAND):
                # AND operator - check for 'not' or '!' prefix on right side
                right_negated = self._match_keyword('not') or self._match(TokenType.NOT)
                right_param = self._advance().value

                if right_negated:
                    right_condition = {'type': 'not', 'param': right_param}
                else:
                    right_condition = {'type': 'exists', 'param': right_param}

                condition = {'type': 'and', 'left': condition, 'right': right_condition}

            elif self._match(TokenType.OR):
                # OR operator (||) - check for 'not' or '!' prefix on right side
                right_negated = self._match_keyword('not') or self._match(TokenType.NOT)
                right_param = self._advance().value

                if right_negated:
                    right_condition = {'type': 'not', 'param': right_param}
                else:
                    right_condition = {'type': 'exists', 'param': right_param}

                condition = {'type': 'or', 'left': condition, 'right': right_condition}
            else:
                break

        return condition

    def _parse_case_body(self, case_node: ASTNode):
        """Parse the body of a case/except/default/always/finally block."""
        stop_keywords = ['case', 'except', 'default', 'always', 'finally']

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Check if we hit another case keyword
            if any(self._check_keyword(kw) for kw in stop_keywords):
                break

            stmt = self._parse_statement()
            if stmt:
                case_node.children.append(stmt)

            # Check for break
            if self._check_keyword('break'):
                break_stmt = self._parse_statement()
                if break_stmt:
                    case_node.children.append(break_stmt)
                break

    def _parse_return(self) -> ASTNode:
        """Parse return statement, supporting multiple values for shuffled functions.

        Syntax:
            return;                    // Return None
            return value;              // Return single value
            return a, b, c;            // Return multiple values (for shuffled)
        """
        values = []
        if not self._check(TokenType.SEMICOLON) and not self._check(TokenType.BLOCK_END):
            values.append(self._parse_expression())

            # Check for comma-separated return values (shuffled return)
            while self._check(TokenType.COMMA):
                self._advance()  # consume comma
                values.append(self._parse_expression())

        self._match(TokenType.SEMICOLON)

        if len(values) == 0:
            return ASTNode('return', value=None)
        elif len(values) == 1:
            return ASTNode('return', value=values[0])
        else:
            # Multiple return values - create tuple return
            return ASTNode('return', value={'multiple': True, 'values': values})

    def _parse_super_function(self) -> ASTNode:
        """Parse super-function for .cssl-pl payload files.

        Syntax:
            #$run(initFunction);           // Call function at load time
            #$exec(setup());               // Execute expression at load time
            #$printl("Payload loaded");    // Print at load time

        These are pre-execution hooks that run when payload() loads the file.
        """
        token = self._advance()  # Get the SUPER_FUNC token
        super_name = token.value  # e.g., "#$run", "#$exec", "#$printl"

        # Parse the arguments
        self._expect(TokenType.PAREN_START)
        args = []
        if not self._check(TokenType.PAREN_END):
            args.append(self._parse_expression())
            while self._match(TokenType.COMMA):
                args.append(self._parse_expression())
        self._expect(TokenType.PAREN_END)
        self._match(TokenType.SEMICOLON)

        return ASTNode('super_func', value={'name': super_name, 'args': args})

    def _parse_try(self) -> ASTNode:
        node = ASTNode('try', children=[])

        try_block = ASTNode('try-block', children=[])
        self._expect(TokenType.BLOCK_START)
        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                try_block.children.append(stmt)
        self._expect(TokenType.BLOCK_END)
        node.children.append(try_block)

        # v4.2.6: Skip optional semicolons between try block and catch
        # v4.5.1: Also skip comments for better .cssl-pl file support
        while self._match(TokenType.SEMICOLON) or self._check(TokenType.COMMENT):
            if self._check(TokenType.COMMENT):
                self._advance()

        if self._match_keyword('catch'):
            error_var = None
            if self._match(TokenType.PAREN_START):
                error_var = self._advance().value
                self._expect(TokenType.PAREN_END)

            catch_block = ASTNode('catch-block', value={'error_var': error_var}, children=[])
            self._expect(TokenType.BLOCK_START)
            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    catch_block.children.append(stmt)
            self._expect(TokenType.BLOCK_END)
            node.children.append(catch_block)

        # v4.2.6: Skip optional semicolons between catch and finally
        # v4.5.1: Also skip comments for better .cssl-pl file support
        while self._match(TokenType.SEMICOLON) or self._check(TokenType.COMMENT):
            if self._check(TokenType.COMMENT):
                self._advance()

        # v4.2.6: Add finally support
        if self._match_keyword('finally'):
            finally_block = ASTNode('finally-block', children=[])
            self._expect(TokenType.BLOCK_START)
            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    finally_block.children.append(stmt)
            self._expect(TokenType.BLOCK_END)
            node.children.append(finally_block)

        return node

    def _parse_throw(self) -> ASTNode:
        """Parse throw statement: throw expression;

        v4.5.1: Added throw statement for exception handling.

        Syntax:
            throw "Error message";
            throw error_variable;
            throw MyException("details");
        """
        # Parse the expression to throw (can be string, variable, or function call)
        if self._check(TokenType.SEMICOLON):
            # throw; - re-throw current exception
            self._advance()
            return ASTNode('throw', value=None)

        expr = self._parse_expression()
        self._match(TokenType.SEMICOLON)
        return ASTNode('throw', value=expr)

    def _parse_raise(self) -> ASTNode:
        """Parse raise statement (Python-style exceptions).

        v4.8: Added raise statement for Python-style exception raising.

        Syntax:
            raise;                              # Re-raise current exception
            raise "Error message";              # Simple message
            raise ValueError("message");        # Python exception type
            raise CustomError("msg", code);     # Custom exception with args

        Supported Python exception types:
            ValueError, TypeError, KeyError, IndexError, AttributeError,
            RuntimeError, IOError, OSError, FileNotFoundError, NameError,
            ZeroDivisionError, OverflowError, StopIteration, AssertionError
        """
        # Check for re-raise (just raise;)
        if self._check(TokenType.SEMICOLON):
            self._advance()
            return ASTNode('raise', value={'type': None, 'message': None})

        # Get the exception expression
        # This could be: "message", ExceptionType("message"), or variable
        expr = self._parse_expression()

        self._match(TokenType.SEMICOLON)

        # Check if it's a function call (ExceptionType("message"))
        if isinstance(expr, ASTNode) and expr.type == 'call':
            callee = expr.value.get('callee')
            args = expr.value.get('args', [])
            if isinstance(callee, ASTNode) and callee.type == 'identifier':
                exc_type = callee.value
                return ASTNode('raise', value={
                    'type': exc_type,
                    'args': args
                })

        # Simple expression (string or variable)
        return ASTNode('raise', value={
            'type': 'Error',  # Default exception type
            'message': expr
        })

    def _parse_await(self) -> ASTNode:
        """Parse await statement: await expression;"""
        expr = self._parse_expression()
        self._match(TokenType.SEMICOLON)
        return ASTNode('await', value=expr)

    def _parse_yield(self) -> ASTNode:
        """Parse yield statement: yield expression; or yield;

        v4.9.3: Generator yield statement for lazy iteration.

        Syntax:
            yield value;     // Yield a value and pause
            yield;           // Yield None and pause

        Example:
            generator<int> define CountUp(int limit) {
                int i = 0;
                while (i < limit) {
                    yield i;
                    i = i + 1;
                }
            }
        """
        # Check for yield with no value (yield;)
        if self._check(TokenType.SEMICOLON):
            self._advance()
            return ASTNode('yield', value=None)

        expr = self._parse_expression()
        self._match(TokenType.SEMICOLON)
        return ASTNode('yield', value=expr)

    def _parse_supports_block(self) -> ASTNode:
        """Parse standalone supports block for multi-language syntax.

        v4.2.0: Allows 'supports' to be used anywhere, not just in class/function.

        Syntax:
            supports py { }               // Python syntax block
            supports @py { }              // With @ prefix
            supports python { }           // Full language name
            supports cpp { }              // C++ syntax block
            supports javascript { }       // JavaScript syntax block

        Example:
            supports py {
                for i in range(10):
                    print(i)
            }

            supports cpp {
                std::cout << "Hello" << std::endl;
                int x = 42;
            }
        """
        # Parse language identifier
        language = None
        if self._check(TokenType.AT):
            self._advance()
            if self._check(TokenType.IDENTIFIER):
                language = '@' + self._advance().value
            else:
                raise CSSLSyntaxError("Expected language identifier after '@' in 'supports'")
        elif self._check(TokenType.IDENTIFIER):
            language = self._advance().value
        else:
            raise CSSLSyntaxError("Expected language identifier after 'supports'")

        # Extract raw block source for language transformation (preserves indentation)
        raw_source = None
        if self._check(TokenType.BLOCK_START):
            raw_source = self._extract_raw_block_body()

        # Skip parsing body if we have raw_source - runtime will transform and parse
        body = []
        self._expect(TokenType.BLOCK_START)
        if raw_source is None:
            # No raw source (e.g., already CSSL syntax), parse normally
            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                stmt = self._parse_statement()
                if stmt:
                    body.append(stmt)
        else:
            # Skip the block - runtime will transform and parse
            brace_count = 1
            while brace_count > 0 and not self._is_at_end():
                if self._check(TokenType.BLOCK_START):
                    brace_count += 1
                elif self._check(TokenType.BLOCK_END):
                    brace_count -= 1
                if brace_count > 0:
                    self._advance()
        self._expect(TokenType.BLOCK_END)

        return ASTNode('supports_block', value={
            'language': language,
            'raw_source': raw_source
        }, children=body)

    def _extract_raw_block_source(self) -> Optional[str]:
        """Extract raw source code from a {} block before parsing.

        Used for 'supports' blocks to allow language transformation.
        """
        if not self._check(TokenType.BLOCK_START):
            return None

        # Find the matching block end by counting braces
        start_pos = self.pos
        brace_count = 0
        found_start = False

        # Walk through tokens to find matching close brace
        temp_pos = self.pos
        while temp_pos < len(self.tokens):
            token = self.tokens[temp_pos]
            if token.type == TokenType.BLOCK_START:
                if not found_start:
                    found_start = True
                brace_count += 1
            elif token.type == TokenType.BLOCK_END:
                brace_count -= 1
                if brace_count == 0:
                    break
            temp_pos += 1

        # Build source from tokens between braces (excluding braces)
        source_parts = []
        for i in range(start_pos + 1, temp_pos):
            token = self.tokens[i]
            if token.type == TokenType.STRING:
                source_parts.append(f'"{token.value}"')
            elif token.type == TokenType.NEWLINE:
                source_parts.append('\n')
            else:
                source_parts.append(str(token.value))

        return ' '.join(source_parts)

    def _extract_raw_block_body(self) -> Optional[str]:
        """Extract raw source code body from a {} block for language transformation.

        v4.2.0: Used for 'supports' blocks to preserve original source (including indentation).
        This extracts the raw text between { and } from the original source string.

        Returns the raw body content without the surrounding braces.
        """
        if not self._check(TokenType.BLOCK_START):
            return None

        # Get the { token's position
        start_token = self._current()
        start_line = start_token.line
        start_col = start_token.column

        # Find the { character position in source
        # Line numbers are 1-indexed, columns are 1-indexed
        brace_start_pos = 0
        current_line = 1
        for i, char in enumerate(self.source):
            if current_line == start_line:
                # Found the right line, now find the column
                col_in_line = i - brace_start_pos + 1
                if col_in_line >= start_col:
                    # Search for { from here
                    for j in range(i, len(self.source)):
                        if self.source[j] == '{':
                            brace_start_pos = j
                            break
                    break
            if char == '\n':
                current_line += 1
                brace_start_pos = i + 1

        # Now find the matching closing brace
        brace_count = 1
        pos = brace_start_pos + 1
        while pos < len(self.source) and brace_count > 0:
            char = self.source[pos]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            pos += 1

        # Extract the body (everything between { and })
        body = self.source[brace_start_pos + 1:pos - 1]
        return body.strip()

    def _parse_action_block(self) -> ASTNode:
        """Parse an action block { ... } containing statements for createcmd"""
        node = ASTNode('action_block', children=[])
        self._expect(TokenType.BLOCK_START)

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Check for define statements inside action block
            if self._match_keyword('define'):
                node.children.append(self._parse_define())
            # Check for typed function definitions (nested functions)
            elif self._looks_like_function_declaration():
                node.children.append(self._parse_typed_function())
            else:
                stmt = self._parse_statement()
                if stmt:
                    node.children.append(stmt)

        self._expect(TokenType.BLOCK_END)
        return node

    def _parse_local_injection(self, local_node: ASTNode) -> ASTNode:
        """Parse local::func injection operations.

        Syntax:
            local::func -<<== { code }                    // Remove matching code
            local::func +<<== { code }                    // Add code
            local::func -<<==[injection::innerline(3)] null;  // Remove specific line
            local::func +<<==[injection::innerline(3)] code;  // Add at specific line

        Args:
            local_node: The local_ref ASTNode (e.g., local::func)

        Returns:
            ASTNode for the local injection operation
        """
        local_name = local_node.value

        # Determine injection mode
        mode = None
        if self._match(TokenType.INFUSE_MINUS_LEFT):
            mode = 'remove'
        elif self._match(TokenType.INFUSE_PLUS_LEFT):
            mode = 'add'
        elif self._match(TokenType.INFUSE_LEFT):
            mode = 'replace'
        else:
            raise CSSLSyntaxError("Expected -<<==, +<<==, or <<== after local::func")

        # Parse optional filter: [injection::innerline(n)]
        filters = self._parse_injection_filter()

        # Parse the value/code block
        code_block = None
        if self._check(TokenType.BLOCK_START):
            # Block form: local::func +<<== { code }
            self._advance()
            children = []
            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                if self._check(TokenType.NEWLINE):
                    self._advance()
                    continue
                stmt = self._parse_statement()
                if stmt:
                    children.append(stmt)
            self._expect(TokenType.BLOCK_END)
            code_block = ASTNode('block', children=children)
        elif self._match_keyword('null') or self._match_keyword('None'):
            # null; for removal without replacement
            code_block = None
        else:
            # Expression form: local::func +<<== expression;
            code_block = self._parse_expression()

        return ASTNode('local_injection', value={
            'target': local_name,
            'mode': mode,
            'filters': filters,
            'code': code_block
        }, line=local_node.line, column=local_node.column)

    def _parse_injection_filter(self) -> Optional[list]:
        """Parse injection filter(s): [type::helper=value] or [f1][f2][f3]...

        Returns a list of filter dictionaries to support chained filters.
        """
        if not self._check(TokenType.BRACKET_START):
            return None

        filters = []

        # Parse multiple consecutive filter brackets
        while self._match(TokenType.BRACKET_START):
            filter_info = {}
            # Parse type::helper=value patterns within this bracket
            while not self._check(TokenType.BRACKET_END) and not self._is_at_end():
                # Accept IDENTIFIER, KEYWORD, or TYPE_LITERAL (dict, list) as filter type
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                    filter_type = self._advance().value
                    if self._match(TokenType.DOUBLE_COLON):
                        helper = self._advance().value
                        if self._match(TokenType.EQUALS):
                            value = self._parse_expression()
                            filter_info[f'{filter_type}::{helper}'] = value
                        else:
                            filter_info[f'{filter_type}::{helper}'] = True
                    else:
                        filter_info['type'] = filter_type
                elif self._check(TokenType.COMMA):
                    self._advance()
                else:
                    break

            self._expect(TokenType.BRACKET_END)
            if filter_info:
                filters.append(filter_info)

        return filters if filters else None

    def _is_injection_operator(self) -> bool:
        """Check if the current token is any injection/infusion operator."""
        if self._is_at_end():
            return False
        t = self.tokens[self.pos].type
        return t in (
            TokenType.INJECT_LEFT, TokenType.INJECT_RIGHT,
            TokenType.INJECT_PLUS_LEFT, TokenType.INJECT_PLUS_RIGHT,
            TokenType.INJECT_MINUS_LEFT, TokenType.INJECT_MINUS_RIGHT,
            TokenType.INFUSE_LEFT, TokenType.INFUSE_RIGHT,
            TokenType.INFUSE_PLUS_LEFT, TokenType.INFUSE_PLUS_RIGHT,
            TokenType.INFUSE_MINUS_LEFT, TokenType.INFUSE_MINUS_RIGHT,
        )

    def _parse_expression_statement(self) -> Optional[ASTNode]:
        expr = self._parse_expression()

        # === LEFT-SIDE FILTER: expr [filter] <operator> [filter] source ===
        # Try to parse left-side filter brackets before injection operators.
        # e.g. x [dynamic::content=10] ==> [string::where="test"] target
        source_filter = None
        if self._check(TokenType.BRACKET_START) and not self._is_injection_operator():
            saved_pos = self.pos
            try:
                left_filter = self._parse_injection_filter()
                if left_filter and self._is_injection_operator():
                    source_filter = left_filter
                else:
                    # Not a filter + injection combo, restore position
                    self.pos = saved_pos
            except Exception:
                self.pos = saved_pos

        # === TUPLE UNPACKING: a, b, c = shuffled_func() ===
        # Check if we have comma-separated identifiers before =
        if expr.type == 'identifier' and self._check(TokenType.COMMA):
            targets = [expr]
            while self._match(TokenType.COMMA):
                next_expr = self._parse_expression()
                if next_expr.type == 'identifier':
                    targets.append(next_expr)
                else:
                    # Not a simple identifier list, this is something else
                    # Restore and fall through to normal parsing
                    break

            # Check if followed by =
            if self._match(TokenType.EQUALS):
                value = self._parse_expression()
                self._match(TokenType.SEMICOLON)
                return ASTNode('tuple_assignment', value={'targets': targets, 'value': value})

        # === BASIC INJECTION: <== (replace target with source) ===
        if self._match(TokenType.INJECT_LEFT):
            # Check if this is a createcmd injection with a code block
            is_createcmd = (
                expr.type == 'call' and
                expr.value.get('callee') and
                expr.value.get('callee').type == 'identifier' and
                expr.value.get('callee').value == 'createcmd'
            )

            if is_createcmd and self._check(TokenType.BLOCK_START):
                action_block = self._parse_action_block()
                self._match(TokenType.SEMICOLON)
                return ASTNode('createcmd_inject', value={'command_call': expr, 'action': action_block})
            else:
                # Check for injection filter [type::helper=value]
                filter_info = self._parse_injection_filter()
                source = self._parse_expression()
                self._match(TokenType.SEMICOLON)
                return ASTNode('inject', value={'target': expr, 'source': source, 'mode': 'replace', 'filter': filter_info, 'source_filter': source_filter})

        # === PLUS INJECTION: +<== (copy & add to target) ===
        if self._match(TokenType.INJECT_PLUS_LEFT):
            filter_info = self._parse_injection_filter()
            source = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('inject', value={'target': expr, 'source': source, 'mode': 'add', 'filter': filter_info, 'source_filter': source_filter})

        # === MINUS INJECTION: -<== or -<==[n] (move & remove from source) ===
        if self._match(TokenType.INJECT_MINUS_LEFT):
            # Check for indexed deletion: -<==[n] (only numbers, not filters)
            remove_index = None
            if self._check(TokenType.BRACKET_START):
                # Peek ahead to see if this is an index [n] or a filter [type::helper=...]
                # Only consume if it's a simple number index
                saved_pos = self.pos
                self._advance()  # consume [
                if self._check(TokenType.NUMBER):
                    remove_index = int(self._advance().value)
                    self._expect(TokenType.BRACKET_END)
                else:
                    # Not a number - restore position for filter parsing
                    self.pos = saved_pos

            filter_info = self._parse_injection_filter()
            source = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('inject', value={'target': expr, 'source': source, 'mode': 'move', 'filter': filter_info, 'index': remove_index, 'source_filter': source_filter})

        # === CODE INFUSION: <<== (inject code into function) ===
        if self._match(TokenType.INFUSE_LEFT):
            if self._check(TokenType.BLOCK_START):
                code_block = self._parse_action_block()
                self._match(TokenType.SEMICOLON)
                return ASTNode('infuse', value={'target': expr, 'code': code_block, 'mode': 'replace'})
            else:
                source = self._parse_expression()
                self._match(TokenType.SEMICOLON)
                return ASTNode('infuse', value={'target': expr, 'source': source, 'mode': 'replace'})

        # === CODE INFUSION PLUS: +<<== (add code to function) ===
        if self._match(TokenType.INFUSE_PLUS_LEFT):
            if self._check(TokenType.BLOCK_START):
                code_block = self._parse_action_block()
                self._match(TokenType.SEMICOLON)
                return ASTNode('infuse', value={'target': expr, 'code': code_block, 'mode': 'add'})
            else:
                source = self._parse_expression()
                self._match(TokenType.SEMICOLON)
                return ASTNode('infuse', value={'target': expr, 'source': source, 'mode': 'add'})

        # === CODE INFUSION MINUS: -<<== or -<<==[n] (remove code from function) ===
        if self._match(TokenType.INFUSE_MINUS_LEFT):
            # Check for indexed deletion: -<<==[n] (only numbers)
            remove_index = None
            if self._check(TokenType.BRACKET_START):
                # Peek ahead to see if this is an index [n] or something else
                saved_pos = self.pos
                self._advance()  # consume [
                if self._check(TokenType.NUMBER):
                    remove_index = int(self._advance().value)
                    self._expect(TokenType.BRACKET_END)
                else:
                    # Not a number - restore position
                    self.pos = saved_pos

            if self._check(TokenType.BLOCK_START):
                code_block = self._parse_action_block()
                self._match(TokenType.SEMICOLON)
                return ASTNode('infuse', value={'target': expr, 'code': code_block, 'mode': 'remove', 'index': remove_index})
            else:
                source = self._parse_expression()
                self._match(TokenType.SEMICOLON)
                return ASTNode('infuse', value={'target': expr, 'source': source, 'mode': 'remove', 'index': remove_index})

        # === RIGHT-SIDE OPERATORS ===

        # === BASIC RECEIVE: ==> (move source to target) ===
        if self._match(TokenType.INJECT_RIGHT):
            filter_info = self._parse_injection_filter()
            target = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('receive', value={'source': expr, 'target': target, 'mode': 'replace', 'filter': filter_info, 'source_filter': source_filter})

        # === PLUS RECEIVE: ==>+ (copy source to target) ===
        if self._match(TokenType.INJECT_PLUS_RIGHT):
            filter_info = self._parse_injection_filter()
            target = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('receive', value={'source': expr, 'target': target, 'mode': 'add', 'filter': filter_info, 'source_filter': source_filter})

        # === MINUS RECEIVE: -==> (move & remove from source) ===
        if self._match(TokenType.INJECT_MINUS_RIGHT):
            filter_info = self._parse_injection_filter()
            target = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('receive', value={'source': expr, 'target': target, 'mode': 'move', 'filter': filter_info, 'source_filter': source_filter})

        # === CODE INFUSION RIGHT: ==>> ===
        if self._match(TokenType.INFUSE_RIGHT):
            target = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('infuse_right', value={'source': expr, 'target': target, 'mode': 'replace'})

        # === FLOW OPERATORS ===
        if self._match(TokenType.FLOW_RIGHT):
            target = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('flow', value={'source': expr, 'target': target})

        if self._match(TokenType.FLOW_LEFT):
            source = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('flow', value={'source': source, 'target': expr})

        # === BASIC ASSIGNMENT ===
        if self._match(TokenType.EQUALS):
            value = self._parse_expression()
            self._match(TokenType.SEMICOLON)
            return ASTNode('assignment', value={'target': expr, 'value': value},
                           line=getattr(expr, 'line', 0), column=getattr(expr, 'column', 0))

        self._match(TokenType.SEMICOLON)
        return ASTNode('expression', value=expr)

    def _parse_expression(self) -> ASTNode:
        return self._parse_inject_expr()

    def _parse_inject_expr(self) -> ASTNode:
        """Parse injection operators as right-associative expression operators.

        v4.9.9: Allows chaining like: a +<== b +<== c  →  a +<== (b +<== c) → "abc"
        Also supports: a <== b, x ==> y, x ==>+ y in expression context.
        Parentheses and right-to-left evaluation (mathematical rules).
        """
        left = self._parse_or()

        # Check for injection/receive operators
        inject_op = None
        if self._check(TokenType.INJECT_PLUS_LEFT):
            inject_op = 'add'
            self._advance()
        elif self._check(TokenType.INJECT_MINUS_LEFT):
            inject_op = 'move'
            self._advance()
        elif self._check(TokenType.INJECT_LEFT):
            inject_op = 'replace'
            self._advance()
        elif self._check(TokenType.INJECT_RIGHT):
            inject_op = 'receive_replace'
            self._advance()
        elif self._check(TokenType.INJECT_PLUS_RIGHT):
            inject_op = 'receive_add'
            self._advance()
        elif self._check(TokenType.INJECT_MINUS_RIGHT):
            inject_op = 'receive_move'
            self._advance()

        if inject_op:
            # Parse optional filter [type::helper=value] after the operator
            filter_info = self._parse_injection_filter()
            # Right-associative: recurse into _parse_inject_expr for the right side
            right = self._parse_inject_expr()
            return ASTNode('inject_expr', value={'op': inject_op, 'left': left, 'right': right, 'filter': filter_info})

        return left

    def _parse_or(self) -> ASTNode:
        left = self._parse_and()

        while self._match(TokenType.OR) or self._match_keyword('or'):
            right = self._parse_and()
            left = ASTNode('binary', value={'op': 'or', 'left': left, 'right': right})

        return left

    def _parse_and(self) -> ASTNode:
        left = self._parse_comparison()

        while self._match(TokenType.AND) or self._match_keyword('and'):
            right = self._parse_comparison()
            left = ASTNode('binary', value={'op': 'and', 'left': left, 'right': right})

        return left

    def _parse_comparison(self) -> ASTNode:
        left = self._parse_stream()

        while True:
            if self._match(TokenType.COMPARE_EQ):
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': '==', 'left': left, 'right': right})
            elif self._match(TokenType.COMPARE_NE):
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': '!=', 'left': left, 'right': right})
            elif self._match(TokenType.COMPARE_LT):
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': '<', 'left': left, 'right': right})
            elif self._match(TokenType.COMPARE_GT):
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': '>', 'left': left, 'right': right})
            elif self._match(TokenType.COMPARE_LE):
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': '<=', 'left': left, 'right': right})
            elif self._match(TokenType.COMPARE_GE):
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': '>=', 'left': left, 'right': right})
            elif self._check(TokenType.KEYWORD) and self._peek().value == 'not':
                # Check for 'not in' compound operator: item not in list
                next_tok = self._peek(1)
                if next_tok and next_tok.type == TokenType.KEYWORD and next_tok.value == 'in':
                    self._advance()  # consume 'not'
                    self._advance()  # consume 'in'
                    right = self._parse_stream()
                    left = ASTNode('binary', value={'op': 'not in', 'left': left, 'right': right})
                else:
                    break
            elif self._check(TokenType.KEYWORD) and self._peek().value == 'in':
                # 'in' operator for containment: item in list
                self._advance()  # consume 'in'
                right = self._parse_stream()
                left = ASTNode('binary', value={'op': 'in', 'left': left, 'right': right})
            else:
                break

        return left

    def _parse_stream(self) -> ASTNode:
        """Parse stream operators: << (stream out) and >> (stream in).

        v4.9.8: Enables C++ style stream syntax:
            cout << "Hello" << " World" << endl;
            cin >> variable;
        """
        left = self._parse_term()

        while True:
            if self._match(TokenType.STREAM_OUT):
                right = self._parse_term()
                left = ASTNode('binary', value={'op': '<<', 'left': left, 'right': right})
            elif self._check(TokenType.STREAM_IN):
                # >> can conflict with nested generics, only parse as stream
                # when left side is a known stream type or identifier
                self._advance()
                right = self._parse_term()
                left = ASTNode('binary', value={'op': '>>', 'left': left, 'right': right})
            else:
                break

        return left

    def _parse_term(self) -> ASTNode:
        left = self._parse_factor()

        while True:
            if self._match(TokenType.PLUS):
                right = self._parse_factor()
                left = ASTNode('binary', value={'op': '+', 'left': left, 'right': right})
            elif self._match(TokenType.MINUS):
                right = self._parse_factor()
                left = ASTNode('binary', value={'op': '-', 'left': left, 'right': right})
            else:
                break

        return left

    def _parse_factor(self) -> ASTNode:
        left = self._parse_unary()

        while True:
            if self._match(TokenType.MULTIPLY):
                right = self._parse_unary()
                left = ASTNode('binary', value={'op': '*', 'left': left, 'right': right})
            elif self._match(TokenType.DIVIDE):
                right = self._parse_unary()
                left = ASTNode('binary', value={'op': '/', 'left': left, 'right': right})
            elif self._match(TokenType.MODULO):
                right = self._parse_unary()
                left = ASTNode('binary', value={'op': '%', 'left': left, 'right': right})
            else:
                break

        return left

    def _parse_conditional_pattern(self) -> ASTNode:
        """Parse a condition pattern inside [condition]*[fallback] syntax.

        v4.9.4: Supports multiple condition patterns:
          - null                           - matches null/None
          - int 2                          - matches specific int value
          - string "hello"                 - matches specific string
          - vector<int>                    - matches type
          - vector<int> = {reflect(@x)}    - matches exact pattern

        Returns an AST node representing the condition.
        """
        # Check for 'null' keyword
        if self._check(TokenType.NULL) or (self._check(TokenType.KEYWORD) and self._current().value in ('null', 'None', 'none')):
            self._advance()
            return ASTNode('condition_null', value=None)

        # Check for type with optional value: int 2, string "hello", vector<int>
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
            type_name = self._current().value

            if self._is_type_keyword(type_name) or self._check(TokenType.TYPE_LITERAL):
                self._advance()  # consume type name

                # Check for generic type: type<...>
                element_type = None
                if self._check(TokenType.COMPARE_LT):
                    self._advance()  # consume <
                    element_type = self._parse_generic_type_content()

                # Check for = pattern value
                if self._check(TokenType.EQUALS):
                    self._advance()  # consume =
                    # Parse value but stop at ] - use primary to avoid consuming too much
                    pattern_value = self._parse_condition_value()
                    return ASTNode('condition_typed_pattern', value={
                        'type': type_name,
                        'element_type': element_type,
                        'pattern': pattern_value
                    })

                # Check for literal value after type (int 2, string "hello")
                if not self._check(TokenType.BRACKET_END):
                    # Parse value but stop at ] - use primary to avoid consuming too much
                    match_value = self._parse_condition_value()
                    return ASTNode('condition_type_value', value={
                        'type': type_name,
                        'element_type': element_type,
                        'match_value': match_value
                    })

                # Just type check (vector<int>, string, etc.)
                return ASTNode('condition_type', value={
                    'type': type_name,
                    'element_type': element_type
                })

        # v4.9.8: Negated condition: [!expr] — matches if value does NOT equal expr
        if self._check(TokenType.NOT):
            self._advance()  # consume !
            inner = self._parse_condition_value()
            return ASTNode('condition_negated', value={'inner': inner})

        # Default: parse as expression (for complex conditions)
        return self._parse_condition_value()

    def _parse_condition_value(self) -> ASTNode:
        """Parse a value inside [...] condition/fallback brackets.

        v4.9.4: This is a restricted expression parser that stops at ] to avoid
        consuming the bracket and subsequent operators like *.

        Supports:
          - Literals: "string", 123, true, null
          - Identifiers: varName
          - Function calls: reflect(%x), getDefault()
          - Brace initializers: {1, 2, 3}
          - Member access: obj.prop
        """
        # Handle brace initializers { ... }
        if self._check(TokenType.BLOCK_START):
            self._advance()  # consume {
            elements = []
            while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                elements.append(self._parse_expression())
                if not self._check(TokenType.BLOCK_END):
                    if self._check(TokenType.COMMA):
                        self._advance()
                    else:
                        break
            self._expect(TokenType.BLOCK_END)
            return ASTNode('array', value=elements)

        # Handle literals
        if self._check(TokenType.STRING):
            return ASTNode('literal', value=self._advance().value)
        if self._check(TokenType.NUMBER):
            return ASTNode('literal', value=self._advance().value)
        if self._check(TokenType.BOOLEAN):
            return ASTNode('literal', value=self._advance().value)
        if self._check(TokenType.NULL):
            self._advance()
            return ASTNode('literal', value=None)

        # Handle captured reference %name
        if self._check(TokenType.CAPTURED_REF):
            token = self._advance()
            node = ASTNode('captured_ref', value=token.value)
            # Allow function call on captured ref: reflect(%x)
            if self._check(TokenType.PAREN_START):
                self._advance()
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
                node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
            return node

        # Handle pointer reference ?name
        if self._check(TokenType.POINTER_REF):
            token = self._advance()
            return ASTNode('pointer_ref', value=token.value)

        # v4.9.11: Handle 'this' keyword — delegate to _parse_primary for proper this-> support
        if self._check(TokenType.KEYWORD) and self._current().value == 'this':
            return self._parse_primary()

        # Handle identifiers and function calls
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            name = self._advance().value
            node = ASTNode('identifier', value=name)

            # v4.9.4: Handle nameof() at parse time - like C#'s nameof operator
            # nameof(identifier) returns the literal name as a string
            if name == 'nameof' and self._check(TokenType.PAREN_START):
                self._advance()  # consume (
                # Get the identifier/expression inside nameof()
                if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                    inner_name = self._advance().value
                    # Handle member access: nameof(obj.member) -> "member"
                    while self._check(TokenType.DOT):
                        self._advance()  # consume .
                        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                            inner_name = self._advance().value
                        else:
                            break
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('literal', value=inner_name)
                elif self._check(TokenType.POINTER_REF):
                    # nameof(?ptr) -> "ptr"
                    token = self._advance()
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('literal', value=token.value)
                elif self._check(TokenType.GLOBAL_REF):
                    # nameof(@global) -> "global"
                    token = self._advance()
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('literal', value=token.value)
                elif self._check(TokenType.SHARED_REF):
                    # nameof($shared) -> "shared"
                    token = self._advance()
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('literal', value=token.value)
                elif self._check(TokenType.CAPTURED_REF):
                    # nameof(%captured) -> "captured"
                    token = self._advance()
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('literal', value=token.value)
                else:
                    # For complex expressions, fall through to runtime nameof
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})

            # Check for function call
            if self._check(TokenType.PAREN_START):
                self._advance()
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
                node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})

            # Check for member access (. and ::)
            while self._check(TokenType.DOT) or self._check(TokenType.DOUBLE_COLON):
                if self._match(TokenType.DOUBLE_COLON):
                    # :: enum/namespace access on result of member access
                    member = self._advance().value
                    node = ASTNode('scope_access', value={'object': node, 'member': member})
                else:
                    self._advance()  # consume .
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                # Check for method call
                if self._check(TokenType.PAREN_START):
                    self._advance()
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})

            return node

        # Fallback: try to parse primary expression
        return self._parse_primary()

    def _parse_non_null_fallback(self) -> ASTNode:
        """Parse fallback value inside *[...] non-null assertion.

        v4.9.4: Supports multiple fallback patterns:
          - Simple value: 3, "default", true
          - Function call: reflect(%NULLPTR), getDefault()
          - Typed value: vector<int> = {0, 2}
          - Typed value: datastruct<dynamic> = { 1, 2 }
          - Tuple/object: (bit H=0, string n="j")

        Returns an AST node representing the fallback value.
        """
        # Check if this looks like a typed fallback: type<...> = value
        # Save position for backtracking
        saved_pos = self.pos

        # Try to parse as typed fallback first
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
            type_name = self._current().value

            # Check if it's a known type (including user types like vector, queue, list, dict)
            if self._is_type_keyword(type_name) or self._check(TokenType.TYPE_LITERAL):
                self._advance()  # consume type name

                # Check for generic type: type<...>
                element_type = None
                if self._check(TokenType.COMPARE_LT):
                    self._advance()  # consume <
                    element_type = self._parse_generic_type_content()

                # Check for = initializer
                if self._check(TokenType.EQUALS):
                    self._advance()  # consume =
                    # Parse the initializer value - use restricted parser to stop at ]
                    init_value = self._parse_condition_value()
                    return ASTNode('typed_fallback', value={
                        'type': type_name,
                        'element_type': element_type,
                        'init': init_value
                    })

                # Not a typed fallback with =, backtrack
                self.pos = saved_pos

        # Check for tuple/object literal: (bit H=0, string n="j")
        if self._check(TokenType.PAREN_START):
            # For parenthesized expressions, we need the full parser
            # Save pos and consume (
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.PAREN_END)
            return expr

        # Parse as regular expression (simple value, function call, etc.)
        # Use restricted parser to stop at ]
        return self._parse_condition_value()

    def _parse_unary(self) -> ASTNode:
        # v4.9.4: Conditional assertion with pattern: [condition]*[fallback]variable
        # Examples:
        #   [int 2]*[string "2"]x      - if x is int 2, return "2"
        #   [null]*[{0}]x              - if x is null, return {0}
        #   [vector<int>]*[{1,2}]x     - if x matches type, use fallback
        if self._check(TokenType.BRACKET_START):
            # Look ahead to see if this is [condition]*[fallback] pattern
            saved_pos = self.pos
            self._advance()  # consume [

            # Parse the condition
            condition = self._parse_conditional_pattern()

            if self._check(TokenType.BRACKET_END):
                self._advance()  # consume ]

                # Check for *[ which indicates this is the conditional assertion pattern
                if self._check(TokenType.MULTIPLY):
                    next_tok = self._peek(1)
                    if next_tok and next_tok.type == TokenType.BRACKET_START:
                        self._advance()  # consume *
                        self._advance()  # consume [

                        # Parse the fallback value
                        fallback = self._parse_non_null_fallback()

                        self._expect(TokenType.BRACKET_END)
                        operand = self._parse_unary()

                        return ASTNode('conditional_assert', value={
                            'condition': condition,
                            'fallback': fallback,
                            'operand': operand
                        })

            # Not a conditional assertion, backtrack
            self.pos = saved_pos

        if self._match(TokenType.NOT) or self._match_keyword('not'):
            operand = self._parse_unary()
            return ASTNode('unary', value={'op': 'not', 'operand': operand})
        # v4.9.3: await as unary prefix for expressions
        if self._match_keyword('await'):
            operand = self._parse_unary()
            return ASTNode('await', value=operand)
        # v4.9.3: yield as unary prefix for expressions (received = yield value)
        if self._match_keyword('yield'):
            # yield can be used with or without a value
            if self._check(TokenType.SEMICOLON) or self._check(TokenType.PAREN_END) or self._check(TokenType.COMMA):
                return ASTNode('yield_expr', value=None)
            operand = self._parse_unary()
            return ASTNode('yield_expr', value=operand)
        if self._match(TokenType.MINUS):
            operand = self._parse_unary()
            return ASTNode('unary', value={'op': '-', 'operand': operand})
        # Prefix increment: ++i
        if self._match(TokenType.PLUS_PLUS):
            operand = self._parse_unary()
            return ASTNode('increment', value={'op': 'prefix', 'operand': operand})
        # Prefix decrement: --i
        if self._match(TokenType.MINUS_MINUS):
            operand = self._parse_unary()
            return ASTNode('decrement', value={'op': 'prefix', 'operand': operand})
        if self._match(TokenType.AMPERSAND):
            # Reference operator: &variable or &@module
            operand = self._parse_unary()
            return ASTNode('reference', value=operand)

        # Non-null assertion: *$var, *@module, *identifier
        # Also type exclusion filter: *[type]expr - exclude type from return
        # v4.9.0: Pointer syntax: *<expr> to get address
        if self._check(TokenType.MULTIPLY):
            next_token = self._peek(1)

            # v4.9.0: Pointer address: *<expr> - get address of expression
            if next_token and next_token.type == TokenType.COMPARE_LT:
                self._advance()  # consume *
                self._advance()  # consume <
                operand = self._parse_expression()
                self._expect(TokenType.COMPARE_GT)  # expect >
                return ASTNode('pointer_address', value={'operand': operand})

            # v4.9.4: Non-null assertion with fallback: *[fallback]variable
            # Supports:
            #   *[3]x                              - simple fallback value
            #   *[datastruct<dynamic> = {1,2}]x   - typed fallback with init
            #   *[vector<int> = {0, 2}]x          - generic type with init
            #   *[reflect(%NULLPTR)]x             - function call as fallback
            #   *[(bit H=0, string n="j")]x       - tuple/object literal
            if next_token and next_token.type == TokenType.BRACKET_START:
                self._advance()  # consume *
                self._advance()  # consume [

                # Parse the fallback value inside brackets
                fallback = self._parse_non_null_fallback()

                self._expect(TokenType.BRACKET_END)
                operand = self._parse_unary()
                return ASTNode('non_null_assert_fallback', value={'fallback': fallback, 'operand': operand})

            # Non-null assertion when followed by $ (shared ref), @ (global), or identifier
            if next_token and next_token.type in (TokenType.SHARED_REF, TokenType.AT, TokenType.IDENTIFIER):
                self._advance()  # consume *
                operand = self._parse_unary()
                return ASTNode('non_null_assert', value={'operand': operand})

        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        # Handle 'this->' member access
        if self._check(TokenType.KEYWORD) and self._current().value == 'this':
            self._advance()  # consume 'this'
            if self._match(TokenType.FLOW_RIGHT):  # ->
                member = self._advance().value
                node = ASTNode('this_access', value={'member': member})
                # Continue to check for calls, member access, indexing
                while True:
                    if self._match(TokenType.PAREN_START):
                        # Method call: this->method()
                        args, kwargs = self._parse_call_arguments()
                        self._expect(TokenType.PAREN_END)
                        node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                    elif self._match(TokenType.DOT):
                        # Chained access: this->obj.method
                        member = self._advance().value
                        node = ASTNode('member_access', value={'object': node, 'member': member})
                    elif self._match(TokenType.BRACKET_START):
                        # Index access: this->arr[0]
                        index = self._parse_expression()
                        self._expect(TokenType.BRACKET_END)
                        node = ASTNode('index_access', value={'object': node, 'index': index})
                    elif self._match(TokenType.FLOW_RIGHT):
                        # Chained this->a->b style access
                        member = self._advance().value
                        node = ASTNode('this_access', value={'member': member, 'object': node})
                    else:
                        break
                return node
            # v4.7: Handle this.member syntax (using DOT instead of ->)
            elif self._match(TokenType.DOT):
                member = self._advance().value
                node = ASTNode('member_access', value={
                    'object': ASTNode('identifier', value='this'),
                    'member': member
                })
                # Continue to check for chained calls, member access, indexing
                while True:
                    if self._match(TokenType.PAREN_START):
                        args, kwargs = self._parse_call_arguments()
                        self._expect(TokenType.PAREN_END)
                        node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                    elif self._match(TokenType.DOT):
                        member = self._advance().value
                        node = ASTNode('member_access', value={'object': node, 'member': member})
                    elif self._match(TokenType.BRACKET_START):
                        index = self._parse_expression()
                        self._expect(TokenType.BRACKET_END)
                        node = ASTNode('index_access', value={'object': node, 'index': index})
                    else:
                        break
                return node
            else:
                # Just 'this' keyword alone - return as identifier for now
                return ASTNode('identifier', value='this')

        # Handle 'new ClassName(args)' or 'new @ClassName(args)' or 'new Namespace::ClassName(args)' instantiation
        if self._check(TokenType.KEYWORD) and self._current().value == 'new':
            self._advance()  # consume 'new'
            # Check for @ prefix (global class reference)
            is_global_ref = False
            if self._check(TokenType.AT):
                self._advance()  # consume @
                is_global_ref = True
            class_name = self._advance().value  # get class name or namespace/module
            # v4.2.6: Handle Namespace::ClassName syntax
            namespace = None
            if self._check(TokenType.DOUBLE_COLON):
                self._advance()  # consume ::
                namespace = class_name
                class_name = self._advance().value  # get actual class name
            # Support new Module.ClassName() — dot-access for classes from included modules
            elif self._check(TokenType.DOT) and self._peek(1) and self._peek(1).type == TokenType.IDENTIFIER:
                self._advance()  # consume .
                namespace = class_name
                class_name = self._advance().value  # get actual class name
            args = []
            kwargs = {}
            if self._match(TokenType.PAREN_START):
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
            node = ASTNode('new', value={'class': class_name, 'namespace': namespace, 'args': args, 'kwargs': kwargs, 'is_global_ref': is_global_ref})
            # Continue to check for member access, calls on the new object
            while True:
                if self._match(TokenType.DOT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                    if self._match(TokenType.PAREN_START):
                        args, kwargs = self._parse_call_arguments()
                        self._expect(TokenType.PAREN_END)
                        node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        if self._match(TokenType.AT):
            # Check for @* (global non-null reference): @*name
            is_non_null = False
            if self._check(TokenType.MULTIPLY):
                self._advance()  # consume *
                is_non_null = True

            node = self._parse_module_reference()

            # Wrap in non_null_assert if @* was used
            if is_non_null:
                node = ASTNode('non_null_assert', value={'operand': node, 'is_global': True})

            # Continue to check for calls, indexing, member access on module refs
            while True:
                if self._match(TokenType.PAREN_START):
                    # Function call on module ref: @Module.method() - with kwargs support
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT):
                    # Member access: @Module.property
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    # Index access: @Module[index]
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        if self._check(TokenType.SELF_REF):
            # s@<name> self-reference to global struct
            token = self._advance()
            node = ASTNode('self_ref', value=token.value, line=token.line, column=token.column)
            # Check for function call: s@Backend.Loop.Start() - with kwargs support
            if self._match(TokenType.PAREN_START):
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
                node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
            return node

        if self._check(TokenType.GLOBAL_REF):
            # r@<name> global variable reference/declaration
            token = self._advance()
            node = ASTNode('global_ref', value=token.value, line=token.line, column=token.column)
            # Check for member access, calls, indexing - with kwargs support
            # Support both . and -> for member access
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        if self._check(TokenType.SHARED_REF):
            # $<name> shared object reference
            token = self._advance()
            node = ASTNode('shared_ref', value=token.value, line=token.line, column=token.column)
            # Check for member access, calls, indexing - with kwargs support
            # Support both . and -> for member access (like this->member)
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    # Support both $obj.member and $obj->member syntax
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        if self._check(TokenType.CAPTURED_REF):
            # %<name> captured reference (captures value at infusion registration time)
            token = self._advance()
            node = ASTNode('captured_ref', value=token.value, line=token.line, column=token.column)
            # Check for member access, calls, indexing - with kwargs support
            # Support both . and -> for member access
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        # v4.9.0: Pointer reference: ?name (dereferences pointer)
        if self._check(TokenType.POINTER_REF):
            token = self._advance()
            node = ASTNode('pointer_ref', value=token.value, line=token.line, column=token.column)
            # Check for member access, calls, indexing
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        # v4.9.4: Pointer-snapshot reference: ?%name (pointer to snapshotted value)
        if self._check(TokenType.POINTER_SNAPSHOT_REF):
            token = self._advance()
            node = ASTNode('pointer_snapshot_ref', value=token.value, line=token.line, column=token.column)
            # Check for member access, calls, indexing
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        # v4.9.2: Local reference for hook variable access: local::varname, local::func
        if self._check(TokenType.LOCAL_REF):
            token = self._advance()
            local_name = token.value  # The local variable/function name
            node = ASTNode('local_ref', value=local_name, line=token.line, column=token.column)
            # Check for injection operations on local::func
            if self._check(TokenType.INFUSE_MINUS_LEFT) or self._check(TokenType.INFUSE_PLUS_LEFT) or \
               self._check(TokenType.INFUSE_LEFT):
                # local::func -<<== {...} or local::func +<<== {...}
                return self._parse_local_injection(node)
            # Check for assignment: local::varname = value
            if self._match(TokenType.EQUALS):
                value = self._parse_expression()
                return ASTNode('local_assign', value={'name': local_name, 'value': value})
            # Check for member access, calls, indexing
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        # v4.1.0: Cross-language instance reference: cpp$ClassName, py$Object
        if self._check(TokenType.LANG_INSTANCE_REF):
            token = self._advance()
            ref = token.value  # {'lang': 'cpp', 'instance': 'ClassName'}
            node = ASTNode('lang_instance_ref', value=ref, line=token.line, column=token.column)
            # Check for member access, calls, indexing
            # Support both . and -> for member access
            while True:
                if self._match(TokenType.PAREN_START):
                    args, kwargs = self._parse_call_arguments()
                    self._expect(TokenType.PAREN_END)
                    node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
                elif self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                    member = self._advance().value
                    node = ASTNode('member_access', value={'object': node, 'member': member})
                elif self._match(TokenType.BRACKET_START):
                    index = self._parse_expression()
                    self._expect(TokenType.BRACKET_END)
                    node = ASTNode('index_access', value={'object': node, 'index': index})
                else:
                    break
            return node

        if self._check(TokenType.NUMBER):
            num_token = self._advance()
            num_value = num_token.value
            # v4.9.0: Check for byte notation x^y (0^102, 1^250)
            if self._check(TokenType.CARET):
                self._advance()  # consume ^
                if not self._check(TokenType.NUMBER):
                    raise CSSLSyntaxError("Expected number after '^' in byte literal", num_token.line)
                weight = self._advance().value
                if num_value not in (0, 1):
                    raise CSSLSyntaxError(f"Byte base must be 0 or 1, got {num_value}", num_token.line)
                if not (0 <= weight <= 255):
                    raise CSSLSyntaxError(f"Byte weight must be 0-255, got {weight}", num_token.line)
                return ASTNode('byte_literal', value={'base': num_value, 'weight': weight})
            return ASTNode('literal', value=num_value)

        if self._check(TokenType.STRING):
            return ASTNode('literal', value=self._advance().value)

        if self._check(TokenType.BOOLEAN):
            return ASTNode('literal', value=self._advance().value)

        if self._check(TokenType.NULL):
            self._advance()
            return ASTNode('literal', value=None)

        # NEW: Type literals (list, dict) - create empty instances
        if self._check(TokenType.TYPE_LITERAL):
            type_name = self._advance().value
            return ASTNode('type_literal', value=type_name)

        if self._match(TokenType.PAREN_START):
            # v4.8.9: Check for typed expression: (type name = value)
            # This creates a typed variable and returns its value
            # Used with snapshot assignment: %xyz = (int number = 200)
            saved_pos = self.pos
            is_typed_expr = False

            # Check pattern: type identifier =
            if ((self._check(TokenType.KEYWORD) and self._is_type_keyword(self._current().value)) or
                self._check(TokenType.IDENTIFIER)):
                potential_type = self._current().value
                self._advance()  # consume type
                # v4.9.8: Handle python::type composite
                if potential_type == 'python' and self._check(TokenType.DOUBLE_COLON):
                    self._advance()
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD) or self._check(TokenType.TYPE_LITERAL):
                        potential_type = 'python::' + self._advance().value

                # Check for generic type like vector<int>
                if self._check(TokenType.COMPARE_LT):
                    self._advance()  # consume <
                    self._parse_generic_type_content()  # consume generic content
                    potential_type += '<...>'  # mark as generic

                if self._check(TokenType.IDENTIFIER):
                    var_name = self._advance().value
                    if self._check(TokenType.EQUALS):
                        # This is a typed expression!
                        is_typed_expr = True
                        self._advance()  # consume =
                        value = self._parse_expression()
                        self._expect(TokenType.PAREN_END)
                        return ASTNode('typed_expression', value={
                            'type': potential_type.replace('<...>', ''),  # clean generic marker
                            'name': var_name,
                            'value': value
                        })

            # Not a typed expression, restore position and parse normally
            if not is_typed_expr:
                self.pos = saved_pos
                expr = self._parse_expression()
                # v4.9.2: Check for tuple literal (expr, expr, ...)
                if self._check(TokenType.COMMA):
                    # This is a tuple - collect all elements
                    elements = [expr]
                    while self._match(TokenType.COMMA):
                        if self._check(TokenType.PAREN_END):
                            # Trailing comma allowed: (a, b,)
                            break
                        elements.append(self._parse_expression())
                    self._expect(TokenType.PAREN_END)
                    return ASTNode('tuple', value=elements)
                self._expect(TokenType.PAREN_END)
                return expr

        if self._match(TokenType.BLOCK_START):
            # Distinguish between:
            # 1. Object literal { key = value } - for dict-like initialization
            # 2. Array literal { 1, 2, 3 } - for vector/array initialization (v4.9.2)
            # 3. Action block { expr; } - for code blocks that return last value
            if self._is_object_literal():
                return self._parse_object()
            elif self._is_array_literal():
                # v4.9.2: Parse as array for vector<T> i = { 1, 2, 3 } initialization
                return self._parse_brace_array()
            else:
                return self._parse_action_block_expression()

        if self._match(TokenType.BRACKET_START):
            return self._parse_array()

        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            return self._parse_identifier_or_call()

        # Fallback: consume the unrecognized token to prevent infinite loops
        self._advance()
        return ASTNode('literal', value=None)

    def _parse_module_reference(self) -> ASTNode:
        """Parse @name, handling method calls and property access.

        @name alone -> module_ref
        @name.method() -> call with member_access
        @name.property -> member_access
        """
        # Get base name
        name = self._advance().value
        node = ASTNode('module_ref', value=name)

        # Continue to handle member access, calls, and indexing
        while True:
            if self._match(TokenType.DOT):
                member = self._advance().value
                node = ASTNode('member_access', value={'object': node, 'member': member})
            elif self._match(TokenType.PAREN_START):
                # Function call - use _parse_call_arguments for kwargs support
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
                node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
            elif self._match(TokenType.BRACKET_START):
                # Index access
                index = self._parse_expression()
                self._expect(TokenType.BRACKET_END)
                node = ASTNode('index_access', value={'object': node, 'index': index})
            else:
                break

        return node

    def _parse_call_arguments(self) -> tuple:
        """Parse function call arguments, supporting both positional and named (key=value).

        Returns: (args, kwargs) where:
            args = list of positional argument expressions
            kwargs = dict of {name: expression} for named arguments
        """
        args = []
        kwargs = {}

        while not self._check(TokenType.PAREN_END) and not self._is_at_end():
            # Check for named argument: identifier = expression
            if self._check(TokenType.IDENTIFIER):
                saved_pos = self.pos  # Save token position
                name_token = self._advance()

                if self._check(TokenType.EQUALS):
                    # Named argument: name=value
                    self._advance()  # consume =
                    value = self._parse_expression()
                    kwargs[name_token.value] = value
                else:
                    # Not named, restore and parse as expression
                    self.pos = saved_pos  # Restore token position
                    args.append(self._parse_expression())
            else:
                args.append(self._parse_expression())

            if not self._check(TokenType.PAREN_END):
                self._expect(TokenType.COMMA)

        return args, kwargs

    def _parse_identifier_or_call(self) -> ASTNode:
        name = self._advance().value

        # Check for namespace syntax: json::read, string::cut, namespace::inner::func, etc.
        # v4.8: Support multiple levels of :: for nested namespace access
        while self._match(TokenType.DOUBLE_COLON):
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                namespace_member = self._advance().value
                name = f"{name}::{namespace_member}"
            else:
                break

        # Check for instance<"name"> syntax - gets/creates shared instance
        if name == 'instance' and self._check(TokenType.COMPARE_LT):
            self._advance()  # consume <
            # Expect string literal for instance name
            if self._check(TokenType.STRING):
                instance_name = self._advance().value
            elif self._check(TokenType.IDENTIFIER):
                instance_name = self._advance().value
            else:
                raise CSSLParserError("Expected instance name (string or identifier)", self._current_line())
            self._expect(TokenType.COMPARE_GT)  # consume >
            return ASTNode('instance_ref', value=instance_name)

        # Check for type generic instantiation: stack<string>, vector<int>, map<string, int>, etc.
        # This creates a new instance of the type with the specified element type
        if name in TYPE_GENERICS and self._check(TokenType.COMPARE_LT):
            self._advance()  # consume <
            element_type = 'dynamic'
            value_type = None  # For map<K, V>
            queue_size = 'dynamic'  # v4.7: For queue<T, size>

            if self._check(TokenType.KEYWORD) or self._check(TokenType.IDENTIFIER):
                element_type = self._advance().value

            # Check for second type parameter (map<K, V>)
            if name == 'map' and self._check(TokenType.COMMA):
                self._advance()  # consume ,
                if self._check(TokenType.KEYWORD) or self._check(TokenType.IDENTIFIER):
                    value_type = self._advance().value
                else:
                    value_type = 'dynamic'

            # v4.7: Check for second parameter for queue<T, size>
            if name == 'queue' and self._check(TokenType.COMMA):
                self._advance()  # consume ,
                if self._check(TokenType.NUMBER):
                    queue_size = int(self._advance().value)
                elif self._check(TokenType.KEYWORD) and self._current().value == 'dynamic':
                    self._advance()  # consume 'dynamic'
                    queue_size = 'dynamic'
                elif self._check(TokenType.IDENTIFIER) and self._current().value == 'dynamic':
                    self._advance()  # consume 'dynamic'
                    queue_size = 'dynamic'
                else:
                    queue_size = 'dynamic'

            self._expect(TokenType.COMPARE_GT)  # consume >

            # Check for inline initialization: map<K,V>{"key": "value", ...}
            init_values = None
            if self._check(TokenType.BLOCK_START):
                self._advance()  # consume {
                init_values = {}

                while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
                    # Parse key
                    if self._check(TokenType.STRING):
                        key = self._advance().value
                    elif self._check(TokenType.IDENTIFIER):
                        key = self._advance().value
                    else:
                        key = str(self._parse_expression().value) if hasattr(self._parse_expression(), 'value') else 'key'

                    # Expect : or =
                    if self._check(TokenType.COLON):
                        self._advance()
                    elif self._check(TokenType.EQUALS):
                        self._advance()

                    # Parse value
                    value = self._parse_expression()
                    init_values[key] = value

                    # Optional comma
                    if self._check(TokenType.COMMA):
                        self._advance()

                self._expect(TokenType.BLOCK_END)  # consume }

            # Check for array-style initialization: vector<int>[1, 2, 3], array<string>["a", "b"]
            elif self._check(TokenType.BRACKET_START):
                self._advance()  # consume [
                init_values = []

                while not self._check(TokenType.BRACKET_END) and not self._is_at_end():
                    init_values.append(self._parse_expression())

                    # Optional comma
                    if self._check(TokenType.COMMA):
                        self._advance()

                self._expect(TokenType.BRACKET_END)  # consume ]

            return ASTNode('type_instantiation', value={
                'type': name,
                'element_type': element_type,
                'value_type': value_type,
                'queue_size': queue_size,  # v4.7: For queue<T, size>
                'init_values': init_values
            })

        # Check for type-parameterized function call: OpenFind<string>(0) or OpenFind<dynamic, "name">
        if name in TYPE_PARAM_FUNCTIONS and self._check(TokenType.COMPARE_LT):
            self._advance()  # consume <
            type_param = 'dynamic'
            param_name = None  # Optional: named parameter search

            if self._check(TokenType.KEYWORD) or self._check(TokenType.IDENTIFIER):
                type_param = self._advance().value

            # Check for second parameter: OpenFind<type, "name">
            if self._check(TokenType.COMMA):
                self._advance()  # consume comma
                # Expect a string literal for the parameter name
                if self._check(TokenType.STRING):
                    param_name = self._advance().value
                elif self._check(TokenType.IDENTIFIER):
                    param_name = self._advance().value

            self._expect(TokenType.COMPARE_GT)  # consume >

            # Optional () - for named parameter search, () is not required
            args = []
            if self._check(TokenType.PAREN_START):
                self._advance()  # consume (
                while not self._check(TokenType.PAREN_END):
                    args.append(self._parse_expression())
                    if not self._check(TokenType.PAREN_END):
                        self._expect(TokenType.COMMA)
                self._expect(TokenType.PAREN_END)

            # Return as typed function call (works with or without ())
            # v4.2.5: OpenFind<type, "name"> now works without ()
            return ASTNode('typed_call', value={
                'name': name,
                'type_param': type_param,
                'param_name': param_name,  # Named parameter for OpenFind
                'args': args
            })

        # v4.9.4: Handle nameof() at parse time - like C#'s nameof operator
        # nameof(identifier) returns the literal name as a string
        if name == 'nameof' and self._check(TokenType.PAREN_START):
            self._advance()  # consume (
            # Get the identifier/expression inside nameof()
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                inner_name = self._advance().value
                # Handle member access: nameof(obj.member) -> "member"
                while self._check(TokenType.DOT):
                    self._advance()  # consume .
                    if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
                        inner_name = self._advance().value
                    else:
                        break
                self._expect(TokenType.PAREN_END)
                return ASTNode('literal', value=inner_name)
            elif self._check(TokenType.POINTER_REF):
                # nameof(?ptr) -> "ptr"
                token = self._advance()
                self._expect(TokenType.PAREN_END)
                return ASTNode('literal', value=token.value)
            elif self._check(TokenType.GLOBAL_REF):
                # nameof(@global) -> "global"
                token = self._advance()
                self._expect(TokenType.PAREN_END)
                return ASTNode('literal', value=token.value)
            elif self._check(TokenType.SHARED_REF):
                # nameof($shared) -> "shared"
                token = self._advance()
                self._expect(TokenType.PAREN_END)
                return ASTNode('literal', value=token.value)
            elif self._check(TokenType.CAPTURED_REF):
                # nameof(%captured) -> "captured"
                token = self._advance()
                self._expect(TokenType.PAREN_END)
                return ASTNode('literal', value=token.value)
            else:
                # For complex expressions, fall through to runtime nameof
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
                return ASTNode('call', value={'callee': ASTNode('identifier', value=name), 'args': args, 'kwargs': kwargs})

        node = ASTNode('identifier', value=name)

        while True:
            # v4.8.5: Support both . and -> for member access (C++ style)
            if self._match(TokenType.DOT) or self._match(TokenType.FLOW_RIGHT):
                member = self._advance().value
                node = ASTNode('member_access', value={'object': node, 'member': member})
            elif self._match(TokenType.DOUBLE_COLON):
                # :: scope access on result of member access (e.g., obj.enumMember::VALUE)
                member = self._advance().value
                node = ASTNode('scope_access', value={'object': node, 'member': member})
            elif self._check(TokenType.PAREN_START):
                # v4.9.11: Prevent cross-line call chaining after completed calls
                # f(x)(y) on same line = intentional chaining
                # f(x)\n(y...) = separate statement, not chaining
                if node.type == 'call' and self.pos > 0:
                    prev_token = self.tokens[self.pos - 1]
                    curr_token = self._current()
                    if (hasattr(prev_token, 'line') and hasattr(curr_token, 'line')
                            and curr_token.line > prev_token.line):
                        break
                self._advance()  # consume (
                args, kwargs = self._parse_call_arguments()
                self._expect(TokenType.PAREN_END)
                node = ASTNode('call', value={'callee': node, 'args': args, 'kwargs': kwargs})
            elif self._match(TokenType.BRACKET_START):
                index = self._parse_expression()
                self._expect(TokenType.BRACKET_END)
                node = ASTNode('index_access', value={'object': node, 'index': index})
            # Postfix increment: i++
            elif self._match(TokenType.PLUS_PLUS):
                node = ASTNode('increment', value={'op': 'postfix', 'operand': node})
            # Postfix decrement: i--
            elif self._match(TokenType.MINUS_MINUS):
                node = ASTNode('decrement', value={'op': 'postfix', 'operand': node})
            else:
                break

        return node

    def _is_object_literal(self) -> bool:
        """Check if current position is an object literal { key = value } vs action block { expr; }

        Object literal: { name = value } or { "key" = value } or { "key": value } (Python-style)
        Action block: { %version; } or { "1.0.0" } or { call(); }

        v4.9.4: Empty block {} is treated as empty object/dict, not action block
        """
        # v4.9.4: Empty block is now empty object (dict), not action block
        # This makes {} = {} work as expected for dict initialization
        if self._check(TokenType.BLOCK_END):
            return True

        # Save position for lookahead
        saved_pos = self.pos

        # Check if it looks like key = value or key: value pattern
        is_object = False
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING):
            self._advance()  # skip key
            if self._check(TokenType.EQUALS) or self._check(TokenType.COLON):
                # Looks like object literal: { key = ... } or { "key": ... }
                is_object = True

        # Restore position
        self.pos = saved_pos
        return is_object

    def _is_array_literal(self) -> bool:
        """Check if current position is an array literal { 1, 2, 3 } for vector/array initialization.

        v4.9.2: Array literal: { value, value, ... } - comma-separated values
        NOT array literal: { expr; } - semicolon-separated (action block)
        """
        # Empty block is not array literal
        if self._check(TokenType.BLOCK_END):
            return False

        # Save position for lookahead
        saved_pos = self.pos

        is_array = False
        # Try to parse first expression and check if followed by comma
        try:
            # Check for simple value followed by comma
            if (self._check(TokenType.NUMBER) or self._check(TokenType.STRING) or
                self._check(TokenType.BOOLEAN) or self._check(TokenType.IDENTIFIER) or
                self._check(TokenType.BRACKET_START) or self._check(TokenType.PAREN_START)):
                # Skip the first value (could be simple or complex)
                depth = 0
                while not self._is_at_end():
                    if self._check(TokenType.PAREN_START) or self._check(TokenType.BRACKET_START) or self._check(TokenType.BLOCK_START):
                        depth += 1
                        self._advance()
                    elif self._check(TokenType.PAREN_END) or self._check(TokenType.BRACKET_END) or self._check(TokenType.BLOCK_END):
                        if depth > 0:
                            depth -= 1
                            self._advance()
                        else:
                            break
                    elif self._check(TokenType.COMMA) and depth == 0:
                        # Found comma at top level - this is an array literal
                        is_array = True
                        break
                    elif self._check(TokenType.SEMICOLON) and depth == 0:
                        # Found semicolon - this is an action block
                        is_array = False
                        break
                    else:
                        self._advance()
        except Exception:
            pass

        # Restore position
        self.pos = saved_pos
        return is_array

    def _parse_brace_array(self) -> ASTNode:
        """Parse brace-enclosed array literal { 1, 2, 3 } for vector/array initialization.

        v4.9.2: Returns an 'array' node, same as [ 1, 2, 3 ] bracket arrays.
        """
        elements = []

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Parse expression
            expr = self._parse_expression()
            elements.append(expr)

            # Expect comma or end
            if not self._match(TokenType.COMMA):
                break

        self._expect(TokenType.BLOCK_END)
        return ASTNode('array', value=elements)

    def _parse_action_block_expression(self) -> ASTNode:
        """Parse an action block expression: { expr; expr2; } returns last value

        Used for: v <== { %version; } or v <== { "1.0.0" }
        """
        children = []

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            # Parse statement or expression
            # v4.2.1: Added LANG_INSTANCE_REF for lang$instance statements
            if (self._check(TokenType.IDENTIFIER) or self._check(TokenType.AT) or
                self._check(TokenType.CAPTURED_REF) or self._check(TokenType.SHARED_REF) or
                self._check(TokenType.GLOBAL_REF) or self._check(TokenType.SELF_REF) or
                self._check(TokenType.LANG_INSTANCE_REF) or
                self._check(TokenType.STRING) or self._check(TokenType.NUMBER) or
                self._check(TokenType.BOOLEAN) or self._check(TokenType.NULL) or
                self._check(TokenType.PAREN_START)):
                # Parse as expression and wrap in expression node for _execute_node
                expr = self._parse_expression()
                self._match(TokenType.SEMICOLON)
                children.append(ASTNode('expression', value=expr))
            elif self._check(TokenType.KEYWORD):
                # Parse as statement
                stmt = self._parse_statement()
                if stmt:
                    children.append(stmt)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return ASTNode('action_block', children=children)

    def _parse_object(self) -> ASTNode:
        """Parse object/dict literal.

        Supports both CSSL-style and Python-style syntax:
            { key = value }       // CSSL style
            { "key" = value }     // CSSL style with string key
            { "key": value }      // Python style
            { key: value }        // Python style with identifier key
        """
        properties = {}

        while not self._check(TokenType.BLOCK_END) and not self._is_at_end():
            if self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING):
                key = self._advance().value
                # Accept both = (CSSL) and : (Python) as key-value separator
                if not self._match(TokenType.EQUALS) and not self._match(TokenType.COLON):
                    self.error(f"Expected '=' or ':' after key '{key}' in object literal")
                value = self._parse_expression()
                properties[key] = value
                self._match(TokenType.SEMICOLON)
                self._match(TokenType.COMMA)
            else:
                self._advance()

        self._expect(TokenType.BLOCK_END)
        return ASTNode('object', value=properties)

    def _parse_array(self) -> ASTNode:
        elements = []

        while not self._check(TokenType.BRACKET_END) and not self._is_at_end():
            elements.append(self._parse_expression())
            if not self._check(TokenType.BRACKET_END):
                self._expect(TokenType.COMMA)

        self._expect(TokenType.BRACKET_END)
        return ASTNode('array', value=elements)

    def _parse_value(self) -> Any:
        if self._check(TokenType.STRING):
            return self._advance().value
        if self._check(TokenType.NUMBER):
            return self._advance().value
        if self._check(TokenType.BOOLEAN):
            return self._advance().value
        if self._check(TokenType.NULL):
            self._advance()
            return None
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.KEYWORD):
            return self._advance().value
        return None

    def _check_keyword(self, keyword: str) -> bool:
        return self._current().type == TokenType.KEYWORD and self._current().value == keyword


def parse_cssl(source: str) -> ASTNode:
    """Parse CSSL source code into an AST - auto-detects service vs program format"""
    lexer = CSSLLexer(source)
    tokens = lexer.tokenize()
    parser = CSSLParser(tokens, lexer.source_lines, source)  # v4.2.0: Pass source for raw extraction

    # Auto-detect: if first token is '{', it's a service file
    # Otherwise treat as standalone program (whitespace is already filtered by lexer)
    if tokens and tokens[0].type == TokenType.BLOCK_START:
        return parser.parse()  # Service file format
    else:
        return parser.parse_program()  # Standalone program format


def parse_cssl_program(source: str) -> ASTNode:
    """Parse standalone CSSL program (no service wrapper) into an AST"""
    lexer = CSSLLexer(source)
    tokens = lexer.tokenize()
    parser = CSSLParser(tokens, lexer.source_lines, source)  # v4.2.0: Pass source for raw extraction
    return parser.parse_program()


def tokenize_cssl(source: str, use_cpp: bool = True) -> List[Token]:
    """
    Tokenize CSSL source code (useful for syntax highlighting).

    Args:
        source: CSSL source code
        use_cpp: If True, use C++ acceleration when available (default True)

    Returns:
        List of Token objects
    """
    # Try C++ tokenization if available and requested
    if use_cpp:
        try:
            from . import _CPP_AVAILABLE, _cpp_module
            if _CPP_AVAILABLE and _cpp_module and hasattr(_cpp_module, 'Lexer'):
                lexer = _cpp_module.Lexer(source)
                cpp_tokens = lexer.tokenize()
                # Convert C++ tokens to Python Token objects
                return _convert_cpp_tokens(cpp_tokens)
        except (ImportError, Exception):
            pass

    # Fall back to Python lexer
    lexer = CSSLLexer(source)
    return lexer.tokenize()


def _convert_cpp_tokens(cpp_tokens: list) -> List[Token]:
    """Convert C++ Token objects to Python Token objects."""
    result = []
    for ct in cpp_tokens:
        # Map C++ token type to Python TokenType
        token_type = _map_cpp_token_type(ct.type)

        # Get value based on value_type
        if ct.value_type == 'string':
            value = ct.str_value
        elif ct.value_type == 'number':
            value = ct.num_value
        elif ct.value_type == 'bool':
            value = ct.bool_value
        else:
            value = ct.str_value

        result.append(Token(token_type, value, ct.line, ct.column))

    return result


def _map_cpp_token_type(cpp_type: int) -> TokenType:
    """Map C++ token type integer to Python TokenType enum."""
    # This mapping must match the C++ TokenType enum in cssl_core.cpp
    type_map = {
        0: TokenType.KEYWORD,
        1: TokenType.IDENTIFIER,
        2: TokenType.STRING,
        3: TokenType.NUMBER,
        4: TokenType.BOOLEAN,
        5: TokenType.NULL,
        6: TokenType.OPERATOR,
        7: TokenType.INJECT_LEFT,
        8: TokenType.INJECT_RIGHT,
        9: TokenType.INJECT_PLUS_LEFT,
        10: TokenType.INJECT_PLUS_RIGHT,
        11: TokenType.INJECT_MINUS_LEFT,
        12: TokenType.INJECT_MINUS_RIGHT,
        13: TokenType.INFUSE_LEFT,
        14: TokenType.INFUSE_RIGHT,
        15: TokenType.FLOW_RIGHT,
        16: TokenType.FLOW_LEFT,
        17: TokenType.EQUALS,
        18: TokenType.COMPARE_EQ,
        19: TokenType.COMPARE_NE,
        20: TokenType.COMPARE_LT,
        21: TokenType.COMPARE_GT,
        22: TokenType.COMPARE_LE,
        23: TokenType.COMPARE_GE,
        24: TokenType.PLUS,
        25: TokenType.MINUS,
        26: TokenType.MULTIPLY,
        27: TokenType.DIVIDE,
        28: TokenType.MODULO,
        29: TokenType.AND,
        30: TokenType.OR,
        31: TokenType.NOT,
        32: TokenType.AMPERSAND,
        33: TokenType.BLOCK_START,
        34: TokenType.BLOCK_END,
        35: TokenType.PAREN_START,
        36: TokenType.PAREN_END,
        37: TokenType.BRACKET_START,
        38: TokenType.BRACKET_END,
        39: TokenType.SEMICOLON,
        40: TokenType.COLON,
        41: TokenType.DOUBLE_COLON,
        42: TokenType.COMMA,
        43: TokenType.DOT,
        44: TokenType.AT,
        45: TokenType.GLOBAL_REF,
        46: TokenType.SNAPSHOT_REF,
        47: TokenType.ARROW,
        48: TokenType.LAMBDA,
        49: TokenType.TERNARY,
        50: TokenType.INCREMENT,
        51: TokenType.DECREMENT,
        52: TokenType.EOF,
    }
    return type_map.get(cpp_type, TokenType.IDENTIFIER)


# Export public API
__all__ = [
    'TokenType', 'Token', 'ASTNode',
    'CSSLLexer', 'CSSLParser', 'CSSLSyntaxError',
    'parse_cssl', 'parse_cssl_program', 'tokenize_cssl',
    'KEYWORDS', 'TYPE_LITERALS'
]
