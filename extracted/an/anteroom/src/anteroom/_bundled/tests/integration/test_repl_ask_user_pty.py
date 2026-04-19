"""PTY-backed integration tests for the ask_user cancel semantics (#1437).

Drives the real ``_make_ask_user_callback`` (from ``anteroom.cli.repl``)
inside a patch_stdout + PromptSession architecture that mirrors the REPL,
over a real pseudo-terminal via pexpect. Verifies that:

* typing ``x`` cancels (callback returns ``None``, cancel_event set)
* Ctrl-D cancels
* Ctrl-C cancels
* options with ``A.``/``B.`` leading prefixes render without
  double-numbering (the CLI strips the prefix, adds its own ``1.``/``2.``)
* pressing Enter with no content is a real empty answer (not a cancel)
* typing a digit resolves to the 1-based option
* typing the stripped option text resolves to that option
"""

from __future__ import annotations

import sys
import textwrap

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for PTY tests")

_PYTHON = sys.executable


def _callback_driver_script(*, question: str, options: list[str] | None) -> str:
    """Script that wires ``_make_ask_user_callback`` into a real PTY.

    Writes key markers to a dup'd stderr fd (visible to pexpect without
    going through prompt_toolkit's patch_stdout buffer).
    """
    opts_repr = "None" if options is None else repr(options)
    return textwrap.dedent(
        f"""\
        import asyncio, sys, os
        from prompt_toolkit.patch_stdout import patch_stdout
        from prompt_toolkit import PromptSession
        from anteroom.cli.repl import _make_ask_user_callback

        _raw_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw_print(text):
            _raw_stderr.write(text + "\\n")
            _raw_stderr.flush()

        async def sub_prompt_async(prompt_text):
            raw_print(f"PTY_PROMPT: {{prompt_text.strip()}}")
            raw_print("PTY_READY")
            try:
                _sub = PromptSession()
                answer = await _sub.prompt_async(prompt_text)
                return answer.strip() if answer is not None else None
            except (EOFError, KeyboardInterrupt):
                return None

        cancel_ref = [asyncio.Event()]
        printed = []

        def console_print(msg):
            printed.append(msg)
            # Emit rendered list items (strip Rich markup) so pexpect can
            # observe the enumeration the CLI actually rendered.
            import re as _re
            plain = _re.sub(r"\\[[^\\]]*\\]", "", msg)
            raw_print(f"PTY_RENDER: {{plain}}")

        callback = _make_ask_user_callback(
            sub_prompt_async=sub_prompt_async,
            cancel_event_ref=cancel_ref,
            console_print=console_print,
        )

        async def drive():
            result = await callback({question!r}, {opts_repr})
            raw_print(f"PTY_CANCEL_SET: {{cancel_ref[0].is_set()}}")
            if result is None:
                raw_print("PTY_RESULT: None")
            else:
                raw_print(f"PTY_RESULT: repr={{result!r}}")

        async def main():
            with patch_stdout(raw=True):
                session = PromptSession()
                async def fake_main():
                    try:
                        await session.prompt_async("> ")
                    except (EOFError, KeyboardInterrupt):
                        pass
                main_task = asyncio.create_task(fake_main())
                await asyncio.sleep(0.3)
                await drive()
                main_task.cancel()
                try:
                    await main_task
                except asyncio.CancelledError:
                    pass

        asyncio.run(main())
        """
    )


@pytest.mark.integration
class TestAskUserCallbackPTY:
    """Drive the real ``_make_ask_user_callback`` through a PTY."""

    def test_typed_x_cancels(self) -> None:
        script = _callback_driver_script(question="Pick one:", options=["Alpha", "Beta"])
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.sendline("x")
        child.expect("PTY_CANCEL_SET: True", timeout=5)
        child.expect("PTY_RESULT: None", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_ctrl_d_cancels(self) -> None:
        script = _callback_driver_script(question="Question?", options=None)
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.sendeof()
        child.expect("PTY_CANCEL_SET: True", timeout=5)
        child.expect("PTY_RESULT: None", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_ctrl_c_cancels(self) -> None:
        script = _callback_driver_script(question="Question?", options=None)
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.sendintr()
        child.expect("PTY_CANCEL_SET: True", timeout=5)
        child.expect("PTY_RESULT: None", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_options_with_prefixes_render_single_enumeration(self) -> None:
        """Options like 'A. Alpha' must render as '1. Alpha', not '1. A. Alpha'.

        The RETURN value is the original 'A. Alpha' — stripping is display-only
        so the CLI/web agree on the tool-level answer.
        """
        script = _callback_driver_script(question="Pick:", options=["A. Alpha", "B. Beta"])
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        # Scan the rendered output — the CLI's "1." should appear, but
        # never as "1. A. Alpha" (which would be the double-numbering bug).
        output_so_far = child.before or ""
        assert "1. A. Alpha" not in output_so_far, f"Double-numbering detected in PTY output:\n{output_so_far}"
        child.sendline("1")
        # Return value is the ORIGINAL "A. Alpha" — prefix preserved for
        # CLI/web parity (web button click posts the original string).
        child.expect(r"PTY_RESULT: repr='A\. Alpha'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_empty_enter_is_real_answer(self) -> None:
        """Pressing Enter with no content returns '' — not a cancel."""
        script = _callback_driver_script(question="Anything to add?", options=None)
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.sendline("")
        child.expect("PTY_CANCEL_SET: False", timeout=5)
        child.expect(r"PTY_RESULT: repr=''", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_digit_resolves_to_option(self) -> None:
        script = _callback_driver_script(question="Pick:", options=["Alpha", "Beta"])
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.sendline("2")
        child.expect(r"PTY_RESULT: repr='Beta'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)

    def test_stripped_text_matches_option_returns_original(self) -> None:
        """Typing 'Alpha' matches the stripped form, returns the ORIGINAL 'A. Alpha'.

        CLI/web parity: the web UI's 'A. Alpha' button posts 'A. Alpha';
        the CLI must produce the same value when the user types 'Alpha'
        (which matches the stripped form).
        """
        script = _callback_driver_script(question="Pick:", options=["A. Alpha", "B. Beta"])
        child = pexpect.spawn(_PYTHON, ["-c", script], timeout=15, encoding="utf-8")
        child.expect("PTY_READY", timeout=10)
        child.sendline("Alpha")
        child.expect(r"PTY_RESULT: repr='A\. Alpha'", timeout=5)
        child.expect(pexpect.EOF, timeout=5)
