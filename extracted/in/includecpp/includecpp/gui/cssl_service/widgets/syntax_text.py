"""
CSSL Service Manager - Text widget with CSSL syntax highlighting.
"""
import re
import tkinter as tk
from .. import theme


class SyntaxText(tk.Text):
    """A Text widget with CSSL/Python syntax highlighting and line coloring."""

    # CSSL keywords
    KEYWORDS = {
        'if', 'else', 'elif', 'for', 'while', 'do', 'return', 'break', 'continue',
        'function', 'class', 'new', 'delete', 'import', 'from', 'export',
        'try', 'catch', 'finally', 'throw', 'in', 'of', 'as', 'is',
        'true', 'false', 'null', 'undefined', 'void', 'const', 'let', 'var',
        'switch', 'case', 'default', 'foreach', 'print', 'println', 'printl',
        'typeof', 'sizeof', 'address', 'reflect', 'async', 'await', 'yield',
    }

    TYPES = {
        'int', 'float', 'string', 'bool', 'list', 'dict', 'set', 'tuple',
        'byte', 'address', 'object', 'array', 'map', 'number',
    }

    BUILTINS = {
        'print', 'println', 'printl', 'typeof', 'sizeof', 'len', 'range',
        'str', 'int', 'float', 'bool', 'list', 'dict', 'input', 'type',
        'abs', 'min', 'max', 'sum', 'sorted', 'reversed', 'enumerate',
    }

    def __init__(self, parent, readonly: bool = False, **kwargs):
        defaults = {
            "bg": theme.SURFACE,
            "fg": theme.TEXT,
            "insertbackground": theme.TEXT,
            "selectbackground": theme.HOVER,
            "selectforeground": theme.TEXT,
            "font": theme.FONT_CODE,
            "wrap": "word",
            "borderwidth": 0,
            "highlightthickness": 0,
            "padx": 8,
            "pady": 4,
            "undo": True,
        }
        defaults.update(kwargs)
        super().__init__(parent, **defaults)

        if readonly:
            self.configure(state="disabled")

        self._setup_tags()
        self._readonly = readonly

    def _setup_tags(self):
        """Configure syntax highlighting tags."""
        self.tag_configure("keyword", foreground=theme.SYNTAX["keyword"])
        self.tag_configure("string", foreground=theme.SYNTAX["string"])
        self.tag_configure("number", foreground=theme.SYNTAX["number"])
        self.tag_configure("comment", foreground=theme.SYNTAX["comment"])
        self.tag_configure("function", foreground=theme.SYNTAX["function"])
        self.tag_configure("type", foreground=theme.SYNTAX["type"])
        self.tag_configure("operator", foreground=theme.SYNTAX["operator"])
        self.tag_configure("builtin", foreground=theme.SYNTAX["builtin"])

        # Output coloring tags
        self.tag_configure("output", foreground=theme.TEXT)
        self.tag_configure("command", foreground=theme.GREEN)
        self.tag_configure("error", foreground=theme.RED)
        self.tag_configure("system", foreground=theme.TEXT_MUTED)
        self.tag_configure("warning", foreground=theme.YELLOW)
        self.tag_configure("success", foreground=theme.GREEN)
        self.tag_configure("info", foreground=theme.BLUE)
        self.tag_configure("accent", foreground=theme.ACCENT)
        self.tag_configure("dim", foreground=theme.TEXT_DIM)

        # Timestamp tag
        self.tag_configure("timestamp", foreground=theme.TEXT_MUTED,
                           font=theme.FONT_CODE_SMALL)

    def append_text(self, text: str, tag: str = "output"):
        """Append text with a specific tag (for output/log mode)."""
        was_disabled = str(self.cget("state")) == "disabled"
        if was_disabled:
            self.configure(state="normal")

        self.insert("end", text, tag)
        self.see("end")

        if was_disabled:
            self.configure(state="disabled")

    def append_line(self, text: str, tag: str = "output"):
        """Append a line of text with tag."""
        self.append_text(text + "\n", tag)

    def clear(self):
        """Clear all text."""
        was_disabled = str(self.cget("state")) == "disabled"
        if was_disabled:
            self.configure(state="normal")
        self.delete("1.0", "end")
        if was_disabled:
            self.configure(state="disabled")

    def highlight_all(self):
        """Apply syntax highlighting to all text."""
        content = self.get("1.0", "end")
        # Remove existing highlights
        for tag in ("keyword", "string", "number", "comment", "function",
                    "type", "operator", "builtin"):
            self.tag_remove(tag, "1.0", "end")

        self._highlight_comments(content)
        self._highlight_strings(content)
        self._highlight_numbers(content)
        self._highlight_keywords(content)
        self._highlight_types(content)
        self._highlight_builtins(content)
        self._highlight_functions(content)

    def _highlight_pattern(self, pattern: str, tag: str, content: str):
        """Apply tag to all matches of pattern."""
        for match in re.finditer(pattern, content):
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.tag_add(tag, start_idx, end_idx)

    def _highlight_keywords(self, content: str):
        pattern = r'\b(' + '|'.join(re.escape(k) for k in self.KEYWORDS) + r')\b'
        self._highlight_pattern(pattern, "keyword", content)

    def _highlight_types(self, content: str):
        pattern = r'\b(' + '|'.join(re.escape(t) for t in self.TYPES) + r')\b'
        self._highlight_pattern(pattern, "type", content)

    def _highlight_builtins(self, content: str):
        pattern = r'\b(' + '|'.join(re.escape(b) for b in self.BUILTINS) + r')\b'
        self._highlight_pattern(pattern, "builtin", content)

    def _highlight_strings(self, content: str):
        self._highlight_pattern(r'"(?:[^"\\]|\\.)*"', "string", content)
        self._highlight_pattern(r"'(?:[^'\\]|\\.)*'", "string", content)

    def _highlight_numbers(self, content: str):
        self._highlight_pattern(r'\b\d+\.?\d*\b', "number", content)
        self._highlight_pattern(r'\b0x[0-9a-fA-F]+\b', "number", content)
        self._highlight_pattern(r'\b0b[01]+\b', "number", content)

    def _highlight_comments(self, content: str):
        self._highlight_pattern(r'//[^\n]*', "comment", content)
        self._highlight_pattern(r'/\*.*?\*/', "comment", content)
        self._highlight_pattern(r'#[^\n]*', "comment", content)

    def _highlight_functions(self, content: str):
        self._highlight_pattern(r'\b([a-zA-Z_]\w*)\s*\(', "function", content)
