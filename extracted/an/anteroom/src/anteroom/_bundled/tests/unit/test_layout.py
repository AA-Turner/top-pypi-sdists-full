"""Tests for the CLI layout utilities module."""

from __future__ import annotations

from unittest.mock import MagicMock

from anteroom.cli.layout import (
    InputLexer,
    _shorten_path,
    build_input_toolbar_fragments,
    get_editing_mode_badge,
    get_input_hint,
    input_line_prefix,
    set_approval_mode,
)

# ---------------------------------------------------------------------------
# _shorten_path
# ---------------------------------------------------------------------------


class TestShortenPath:
    def test_home_replaced(self, monkeypatch):
        monkeypatch.setenv("HOME", "/Users/alice")
        assert _shorten_path("/Users/alice/projects/foo") == "~/projects/foo"

    def test_non_home_unchanged(self, monkeypatch):
        monkeypatch.setenv("HOME", "/Users/alice")
        assert _shorten_path("/opt/data") == "/opt/data"


# ---------------------------------------------------------------------------
# set_approval_mode / input_line_prefix
# ---------------------------------------------------------------------------


class TestInputLinePrefix:
    def test_default_prompt(self):
        set_approval_mode("")
        result = input_line_prefix(0, 0)
        assert result == [("class:prompt", "> ")]

    def test_auto_mode(self):
        set_approval_mode("auto")
        result = input_line_prefix(0, 0)
        assert result == [("class:prompt.auto", "> ")]

    def test_ask_mode(self):
        set_approval_mode("ask")
        result = input_line_prefix(0, 0)
        assert result == [("class:prompt.strict", "> ")]

    def test_continuation_line(self):
        set_approval_mode("auto")
        result = input_line_prefix(1, 0)
        assert result == [("class:prompt.continuation", ". ")]


# ---------------------------------------------------------------------------
# InputLexer
# ---------------------------------------------------------------------------


class TestInputLexer:
    def _make_doc(self, text: str) -> MagicMock:
        doc = MagicMock()
        doc.lines = text.split("\n")
        return doc

    def test_slash_command_highlighted(self):
        lexer = InputLexer()
        doc = self._make_doc("/help some args")
        get_line = lexer.lex_document(doc)
        result = get_line(0)
        assert result == [("class:input.command", "/help"), ("", " some args")]

    def test_bang_command_highlighted(self):
        lexer = InputLexer()
        doc = self._make_doc("!git status")
        get_line = lexer.lex_document(doc)
        result = get_line(0)
        assert result == [("class:input.command", "!git"), ("", " status")]

    def test_bare_bang_highlighted(self):
        lexer = InputLexer()
        doc = self._make_doc("!")
        get_line = lexer.lex_document(doc)
        result = get_line(0)
        assert result == [("class:input.command", "!"), ("", "")]

    def test_plain_text(self):
        lexer = InputLexer()
        doc = self._make_doc("hello world")
        get_line = lexer.lex_document(doc)
        result = get_line(0)
        assert result == [("", "hello world")]

    def test_continuation_no_highlight(self):
        lexer = InputLexer()
        doc = self._make_doc("/cmd\n/not-a-cmd")
        get_line = lexer.lex_document(doc)
        result = get_line(1)
        assert result == [("", "/not-a-cmd")]

    def test_empty_line(self):
        lexer = InputLexer()
        doc = self._make_doc("")
        get_line = lexer.lex_document(doc)
        result = get_line(0)
        assert result == [("", "")]


class _ViState:
    def __init__(self, input_mode: str) -> None:
        self.input_mode = input_mode


class _App:
    def __init__(self, input_mode: str) -> None:
        self.vi_state = _ViState(input_mode)


class TestInputToolbarHelpers:
    def test_mode_badge_hidden_when_disabled(self):
        assert get_editing_mode_badge("emacs", show_mode_badge=False) is None

    def test_vi_navigation_badge(self):
        assert get_editing_mode_badge("vi", app=_App("InputMode.NAVIGATION")) == "VI NAV"

    def test_vi_insert_badge(self):
        assert get_editing_mode_badge("vi", app=_App("InputMode.INSERT")) == "VI INSERT"

    def test_emacs_badge(self):
        assert get_editing_mode_badge("emacs") == "EMACS"

    def test_hint_for_idle(self):
        assert get_input_hint(hint_context="idle") == "Tab complete Alt+Enter newline Ctrl+D exit"

    def test_hint_for_multiline_paste(self):
        assert get_input_hint(hint_context="multiline", paste_line_count=8) == "8 pasted lines review before Enter"

    def test_toolbar_fragments_include_mode_and_hint(self):
        result = build_input_toolbar_fragments(
            editing_mode="vi",
            app=_App("InputMode.INSERT"),
            hint_context="multiline",
            paste_line_count=6,
        )
        assert result == [
            ("class:bottom-toolbar.mode", "VI INSERT"),
            ("class:bottom-toolbar.sep", " · "),
            ("class:bottom-toolbar.hint", "6 pasted lines review before Enter"),
        ]

    def test_toolbar_fragments_only_include_hint_when_badge_disabled(self):
        result = build_input_toolbar_fragments(
            editing_mode="emacs",
            show_mode_badge=False,
            hint_context="idle",
        )
        assert result == [
            ("class:bottom-toolbar.hint", "Tab complete Alt+Enter newline Ctrl+D exit"),
        ]
