"""PTY-backed regression tests for bare-slash command palette acquisition (#1429, #1496)."""

from __future__ import annotations

import sys
import textwrap

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for PTY tests")

_PYTHON = sys.executable


def _palette_driver_script() -> str:
    return textwrap.dedent(
        """\
        import asyncio, os, sys
        from prompt_toolkit import PromptSession
        from prompt_toolkit.completion import Completer, Completion
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.patch_stdout import patch_stdout

        from anteroom.cli.command_palette import get_command_palette_suggestions, should_open_command_palette

        _raw = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw(msg):
            _raw.write(msg + "\\n")
            _raw.flush()

        class PaletteCompleter(Completer):
            def get_completions(self, document, complete_event):
                text = document.text_before_cursor
                stripped = text.lstrip()
                if not stripped.startswith("/") or " " in stripped:
                    return
                word = document.get_word_before_cursor(WORD=True)
                query = word.lstrip("/")
                for entry in get_command_palette_suggestions(query, limit=8):
                    raw(f"PTY_MENU: {entry.display_text} | {entry.meta_text}")
                    yield Completion(
                        entry.insert_text,
                        start_position=-len(word),
                        display=entry.display_text,
                        display_meta=entry.meta_text,
                    )

        kb = KeyBindings()

        def _accept_completion(buf):
            if buf.complete_state and buf.complete_state.current_completion:
                saved_completer = buf.completer
                buf.completer = None
                try:
                    buf.apply_completion(buf.complete_state.current_completion)
                finally:
                    buf.completer = saved_completer
                raw(f"PTY_BUFFER: {buf.text!r}")
                return True
            return False

        @kb.add("enter")
        def _submit(event):
            buf = event.current_buffer
            if _accept_completion(buf):
                return
            buf.validate_and_handle()

        async def main():
            with patch_stdout(raw=True):
                session = PromptSession(
                    completer=PaletteCompleter(),
                    key_bindings=kb,
                    multiline=True,
                    reserve_space_for_menu=8,
                )

                def _on_insert(buf):
                    if should_open_command_palette(buf.text):
                        try:
                            buf.start_completion(select_first=False)
                        except Exception:
                            pass

                session.default_buffer.on_text_insert += _on_insert
                raw("PTY_READY")
                try:
                    result = await session.prompt_async("> ")
                    raw(f"PTY_RESULT: {result!r}")
                except (EOFError, KeyboardInterrupt):
                    raw("PTY_CANCELLED")

        asyncio.run(main())
        """
    )


def _history_driver_script() -> str:
    return textwrap.dedent(
        """\
        import asyncio, os, sys, tempfile
        from prompt_toolkit import PromptSession
        from prompt_toolkit.completion import Completer, Completion
        from prompt_toolkit.history import FileHistory
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.patch_stdout import patch_stdout

        from anteroom.cli.command_palette import get_command_palette_suggestions, should_open_command_palette

        _raw = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw(msg):
            _raw.write(msg + "\\n")
            _raw.flush()

        class PaletteCompleter(Completer):
            def get_completions(self, document, complete_event):
                text = document.text_before_cursor
                stripped = text.lstrip()
                if not stripped.startswith("/") or " " in stripped:
                    return
                word = document.get_word_before_cursor(WORD=True)
                query = word.lstrip("/")
                for entry in get_command_palette_suggestions(query, limit=8):
                    raw(f"PTY_MENU: {entry.display_text} | {entry.meta_text}")
                    yield Completion(
                        entry.insert_text,
                        start_position=-len(word),
                        display=entry.display_text,
                        display_meta=entry.meta_text,
                    )

        kb = KeyBindings()

        def _accept_completion(buf):
            if buf.complete_state and buf.complete_state.current_completion:
                saved_completer = buf.completer
                buf.completer = None
                try:
                    buf.apply_completion(buf.complete_state.current_completion)
                finally:
                    buf.completer = saved_completer
                raw(f"PTY_BUFFER: {buf.text!r}")
                return True
            return False

        @kb.add("enter")
        def _submit(event):
            buf = event.current_buffer
            if _accept_completion(buf):
                return
            buf.validate_and_handle()

        async def main():
            with tempfile.TemporaryDirectory() as tmpdir:
                history_path = os.path.join(tmpdir, "history.txt")
                with patch_stdout(raw=True):
                    session = PromptSession(
                        completer=PaletteCompleter(),
                        key_bindings=kb,
                        multiline=True,
                        reserve_space_for_menu=8,
                        history=FileHistory(history_path),
                    )

                    def _on_insert(buf):
                        if should_open_command_palette(buf.text):
                            try:
                                buf.start_completion(select_first=False)
                            except Exception:
                                pass

                    session.default_buffer.on_text_insert += _on_insert
                    raw("PTY_READY")
                    for idx in range(1, 4):
                        try:
                            result = await session.prompt_async("> ")
                        except (EOFError, KeyboardInterrupt):
                            raw("PTY_CANCELLED")
                            return
                        raw(f"PTY_RESULT[{idx}]: {result!r}")

        asyncio.run(main())
        """
    )


@pytest.mark.integration
class TestReplCommandPalettePTY:
    def test_bare_slash_enter_submits_literal_without_selecting(self) -> None:
        """Bare / + Enter must NOT auto-accept /new — palette opens unselected (#1496)."""
        child = pexpect.spawn(_PYTHON, ["-c", _palette_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("/")
        child.expect(r"PTY_MENU: /new <note\|document\|title> \| Conversation .*", timeout=10)
        child.send("\r")
        # No PTY_BUFFER line — no completion was applied
        child.expect(r"PTY_RESULT: '/'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_query_can_rank_by_action_words_and_insert_subcommand_scaffold(self) -> None:
        child = pexpect.spawn(_PYTHON, ["-c", _palette_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("/switch")
        child.expect(r"PTY_MENU: /space <subcommand> \| Workspace .*switch.*", timeout=10)
        # Use explicit down-arrow navigation rather than relying on select_first timing.
        # select_first correctness is verified via the mock tests in test_repl_completions.py;
        # this test verifies that the palette surfaces the correct entry and insertion works.
        child.send("\x1b[B")  # down arrow — move to first completion
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\r")
        child.expect(r"PTY_BUFFER: '/space '", timeout=5)
        child.send("\r")
        child.expect(r"PTY_RESULT: '/space '", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_slash_n_enter_submits_literal(self) -> None:
        """/n + Enter must submit '/n', not auto-expand to /new-issue (#1501)."""
        child = pexpect.spawn(_PYTHON, ["-c", _palette_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("/n")
        child.expect(r"PTY_MENU:", timeout=10)
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\r")
        # No PTY_BUFFER line — no completion was applied
        child.expect(r"PTY_RESULT: '/n'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_slash_n_backspace_leaves_slash(self) -> None:
        """Backspace after /n must remove 'n' leaving '/', not strip from a pre-selected completion (#1501)."""
        child = pexpect.spawn(_PYTHON, ["-c", _palette_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("/n")
        child.expect(r"PTY_MENU:", timeout=10)
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\x7f")  # Backspace
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\r")
        child.expect(r"PTY_RESULT: '/'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_slash_n_continued_typing_refines_buffer(self) -> None:
        """Continued typing after /n must append to the literal buffer, not overwrite a selection (#1501)."""
        child = pexpect.spawn(_PYTHON, ["-c", _palette_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("/n")
        child.expect(r"PTY_MENU:", timeout=10)
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("e")
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\r")
        child.expect(r"PTY_RESULT: '/ne'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_history_recall_of_slash_command_does_not_block_previous_history(self) -> None:
        child = pexpect.spawn(_PYTHON, ["-c", _history_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("alpha\r")
        child.expect(r"PTY_RESULT\[1\]: 'alpha'", timeout=10)
        child.send("/help\r")
        child.expect(r"PTY_MENU:", timeout=10)
        child.expect(r"PTY_RESULT\[2\]: '/help'", timeout=10)
        child.send("\x1b[A")
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\x1b[A")
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\r")
        child.expect(r"PTY_RESULT\[3\]: 'alpha'", timeout=10)
        child.expect(pexpect.EOF, timeout=5)

    def test_recalled_slash_command_remains_editable(self) -> None:
        child = pexpect.spawn(_PYTHON, ["-c", _history_driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.send("alpha\r")
        child.expect(r"PTY_RESULT\[1\]: 'alpha'", timeout=10)
        child.send("/help\r")
        child.expect(r"PTY_MENU:", timeout=10)
        child.expect(r"PTY_RESULT\[2\]: '/help'", timeout=10)
        child.send("\x1b[A")
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\x7f")
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("x")
        child.expect(pexpect.TIMEOUT, timeout=0.3)
        child.send("\r")
        child.expect(r"PTY_RESULT\[3\]: '/helx'", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
