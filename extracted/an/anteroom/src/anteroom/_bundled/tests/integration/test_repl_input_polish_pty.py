"""PTY-backed prompt-toolkit tests for CLI input polish (#1369)."""

from __future__ import annotations

import sys
import textwrap

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for PTY tests")

_PYTHON = sys.executable


def _driver_script() -> str:
    return textwrap.dedent(
        """\
        import asyncio, os, sys, time
        from prompt_toolkit import PromptSession
        from prompt_toolkit.enums import EditingMode
        from prompt_toolkit.key_binding import KeyBindings
        from anteroom.cli.layout import build_input_toolbar_fragments
        from anteroom.cli.repl import _detect_large_paste, _is_paste

        raw = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw_print(msg):
            raw.write(msg + "\\n")
            raw.flush()

        kb = KeyBindings()
        last_text_change = [0.0]
        previous_text = [""]
        large_paste_lines = [0]
        toolbar_text = [""]

        @kb.add("enter")
        def _submit(event):
            if _is_paste(last_text_change[0]):
                event.current_buffer.insert_text("\\n")
            else:
                event.current_buffer.validate_and_handle()

        @kb.add("escape", eager=True)
        def _escape(event):
            event.app.vi_state.input_mode = event.app.vi_state.input_mode.NAVIGATION
            event.app.invalidate()

        def _bottom_toolbar():
            context = "multiline" if (large_paste_lines[0] or "\\n" in session.default_buffer.text) else "idle"
            fragments = build_input_toolbar_fragments(
                editing_mode="vi",
                app=session.app,
                hint_context=context,
                paste_line_count=large_paste_lines[0],
            )
            plain = "".join(part[1] for part in fragments)
            if plain != toolbar_text[0]:
                toolbar_text[0] = plain
                raw_print(f"PTY_TOOLBAR:{plain}")
            return fragments

        session = PromptSession(
            multiline=True,
            editing_mode=EditingMode.VI,
            key_bindings=kb,
            bottom_toolbar=_bottom_toolbar,
        )

        def _on_change(buf):
            last_text_change[0] = time.monotonic()
            pasted = _detect_large_paste(previous_text[0], buf.text, min_lines=5)
            if pasted:
                large_paste_lines[0] = pasted
                raw_print(f"PTY_PASTE:{pasted}")
            elif not buf.text:
                large_paste_lines[0] = 0
            previous_text[0] = buf.text

        session.default_buffer.on_text_changed += _on_change

        async def main():
            raw_print("PTY_READY")
            result = await session.prompt_async("> ")
            raw_print("PTY_RESULT:" + result.replace("\\n", "|"))

        asyncio.run(main())
        """
    )


@pytest.mark.integration
class TestReplInputPolishPTY:
    def test_large_paste_stays_reviewable_until_explicit_enter(self) -> None:
        child = pexpect.spawn(_PYTHON, ["-c", _driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.expect("PTY_TOOLBAR:VI INSERT", timeout=10)
        child.send("one\\ntwo\\nthree\\nfour\\nfive\\nsix")
        child.expect("PTY_PASTE:6", timeout=10)
        child.expect("PTY_TOOLBAR:VI INSERT · 6 pasted lines review before Enter", timeout=10)
        with pytest.raises(pexpect.TIMEOUT):
            child.expect("PTY_RESULT:", timeout=0.5)
        child.sendline("")
        child.expect("PTY_RESULT:one\\|two\\|three\\|four\\|five\\|six", timeout=10)
        child.expect(pexpect.EOF, timeout=5)

    def test_vi_mode_badge_switches_to_navigation(self) -> None:
        child = pexpect.spawn(_PYTHON, ["-c", _driver_script()], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.expect("PTY_TOOLBAR:VI INSERT", timeout=10)
        child.send("\x1b")
        child.expect("PTY_TOOLBAR:VI NAV", timeout=10)
        child.sendline("done")
        child.expect("PTY_RESULT:done", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
