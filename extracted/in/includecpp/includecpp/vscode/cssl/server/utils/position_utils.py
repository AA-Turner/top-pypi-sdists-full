"""
Position utilities for the CSSL Language Server.

Provides functions for converting between different position representations
(line/column, offset) and finding words at positions.
"""

from typing import Tuple, Optional, List


def position_to_offset(text: str, line: int, column: int) -> int:
    """
    Convert a line/column position to a character offset.

    Args:
        text: The source text
        line: 0-based line number
        column: 0-based column number

    Returns:
        Character offset from the start of the text
    """
    lines = text.splitlines(keepends=True)
    offset = 0

    for i, line_text in enumerate(lines):
        if i == line:
            return offset + min(column, len(line_text))
        offset += len(line_text)

    return len(text)


def offset_to_position(text: str, offset: int) -> Tuple[int, int]:
    """
    Convert a character offset to a line/column position.

    Args:
        text: The source text
        offset: Character offset from the start

    Returns:
        Tuple of (line, column), both 0-based
    """
    line = 0
    column = 0

    for i, char in enumerate(text):
        if i == offset:
            return (line, column)
        if char == '\n':
            line += 1
            column = 0
        else:
            column += 1

    return (line, column)


def get_word_at_position(text: str, line: int, column: int) -> Optional[Tuple[str, int, int]]:
    """
    Get the word at the given position.

    Args:
        text: The source text
        line: 0-based line number
        column: 0-based column number

    Returns:
        Tuple of (word, start_column, end_column) or None if no word found
    """
    try:
        lines = text.splitlines()

        if line < 0 or line >= len(lines):
            return None

        line_text = lines[line]

        if column < 0 or column > len(line_text):
            return None

        if len(line_text) == 0:
            return None

        # Handle special prefixes (?, @, $, %)
        # Case 1: Cursor is ON the prefix character
        if column < len(line_text) and line_text[column] in '?@$%':
            start = column
            end = column + 1
            # Expand to include the variable name after prefix
            while end < len(line_text) and _is_word_char(line_text[end]):
                end += 1
            if end > start + 1:  # prefix + at least one char
                return (line_text[start:end], start, end)
            return None

        # Case 2: Cursor is right after the prefix character
        if column > 0 and line_text[column - 1] in '?@$%':
            start = column - 1
            end = column
            # Expand to include the variable name after prefix
            while end < len(line_text) and _is_word_char(line_text[end]):
                end += 1
            if end > start + 1:  # prefix + at least one char
                return (line_text[start:end], start, end)
            return None

        # Case 3: Cursor is inside the identifier part after prefix
        # Check if there's a prefix before the word
        start = column
        while start > 0 and _is_word_char(line_text[start - 1]):
            start -= 1

        # Check for prefix before the word
        if start > 0 and line_text[start - 1] in '?@$%':
            start -= 1

        # Find end of word
        end = column
        while end < len(line_text) and _is_word_char(line_text[end]):
            end += 1

        if start == end:
            return None

        word = line_text[start:end]
        return (word, start, end)
    except Exception:
        return None


def get_word_before_position(text: str, line: int, column: int) -> Optional[str]:
    """
    Get the word immediately before the cursor position.

    Args:
        text: The source text
        line: 0-based line number
        column: 0-based column number

    Returns:
        The word before the cursor, or None
    """
    lines = text.splitlines()

    if line < 0 or line >= len(lines):
        return None

    line_text = lines[line]

    if column <= 0 or column > len(line_text):
        return None

    # Move back past any whitespace
    end = column
    while end > 0 and line_text[end - 1].isspace():
        end -= 1

    if end == 0:
        return None

    # Find the start of the word
    start = end
    while start > 0 and _is_word_char(line_text[start - 1]):
        start -= 1

    # Check for special prefixes
    if start > 0 and line_text[start - 1] in '?@$%':
        start -= 1

    if start == end:
        return None

    return line_text[start:end]


def get_trigger_character(text: str, line: int, column: int) -> Optional[str]:
    """
    Get the trigger character at the given position.

    Trigger characters are: . :: ? @ $ %

    Args:
        text: The source text
        line: 0-based line number
        column: 0-based column number

    Returns:
        The trigger character or sequence, or None
    """
    lines = text.splitlines()

    if line < 0 or line >= len(lines):
        return None

    line_text = lines[line]

    if column <= 0:
        return None

    # Check for ::
    if column >= 2 and line_text[column-2:column] == '::':
        return '::'

    # Check for single character triggers
    char = line_text[column - 1] if column <= len(line_text) else ''
    if char in '.?@$%':
        return char

    return None


def get_context_before(text: str, line: int, column: int) -> Tuple[Optional[str], Optional[str]]:
    """
    Get the context before a trigger character.

    For member access (var.method), returns (trigger, base_expression).
    For namespace access (ns::member), returns (trigger, namespace).
    For reference (?, @, $, %), returns (trigger, None).

    Args:
        text: The source text
        line: 0-based line number
        column: 0-based column number

    Returns:
        Tuple of (trigger, context) or (None, None)
    """
    trigger = get_trigger_character(text, line, column)

    if not trigger:
        return (None, None)

    lines = text.splitlines()
    line_text = lines[line]

    if trigger == '.':
        # Find the expression before the dot
        end = column - 1
        start = end
        paren_depth = 0

        while start > 0:
            char = line_text[start - 1]
            if char == ')':
                paren_depth += 1
            elif char == '(':
                if paren_depth > 0:
                    paren_depth -= 1
                else:
                    break
            elif not _is_word_char(char) and paren_depth == 0:
                break
            start -= 1

        if start < end:
            return ('.', line_text[start:end])

    elif trigger == '::':
        # Find the namespace before ::
        end = column - 2
        start = end

        while start > 0 and _is_word_char(line_text[start - 1]):
            start -= 1

        if start < end:
            return ('::', line_text[start:end])

    elif trigger in '?@$%':
        return (trigger, None)

    return (trigger, None)


def _is_word_char(char: str) -> bool:
    """Check if a character can be part of an identifier."""
    return char.isalnum() or char == '_'


def get_line_text(text: str, line: int) -> str:
    """Get the text of a specific line."""
    lines = text.splitlines()
    if 0 <= line < len(lines):
        return lines[line]
    return ""


def get_lines(text: str) -> List[str]:
    """Get all lines from the text."""
    return text.splitlines()
