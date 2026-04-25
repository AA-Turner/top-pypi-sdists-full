"""PTY-backed integration tests for REPL busy-state prompt stability (#1134).

These tests spawn a real Python process via pexpect (with a PTY) to verify
that type-ahead text survives concurrent async toolbar invalidation.

NOTE: prompt_toolkit's bottom_toolbar rendering requires terminal CPR support
(cursor position requests) which PTY subprocesses don't provide.  Toolbar
*callback* invocation and *content rendering* are therefore tested at the unit
level (TestFormatStatusToolbar, TestBusyToolbarTheme, TestFooterModeLifecycle)
where we can call the functions directly.  PTY tests focus on what only a real
terminal process can verify: input integrity under concurrent async redraws.
"""

from __future__ import annotations

import sys
import textwrap

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for PTY tests")

_PYTHON = sys.executable


def _concurrent_invalidation_script() -> str:
    """Script with concurrent async tasks: one reads input, one fires redraws.

    This exercises the core stability guarantee: a background task calling
    app.invalidate() rapidly while prompt_async is waiting for input must
    not lose, corrupt, or interleave the typed text.

    The script uses patch_stdout(raw=True) and a bottom_toolbar callback —
    the same architecture as the real REPL.  Even though the PTY test can't
    verify visual toolbar content (prompt_toolkit needs CPR for that), it
    verifies that the asyncio concurrency model (background invalidation +
    foreground prompt) doesn't break input delivery.
    """
    return textwrap.dedent("""\
        import asyncio, sys, os
        from prompt_toolkit.patch_stdout import patch_stdout
        from prompt_toolkit import PromptSession

        _raw_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw_print(text):
            _raw_stderr.write(text + "\\n")
            _raw_stderr.flush()

        _busy_text = ""
        _invalidation_count = 0

        def _bottom_toolbar():
            if _busy_text:
                return [("class:bottom-toolbar", f" {_busy_text} ")]
            return [("class:bottom-toolbar", " idle ")]

        async def main():
            global _busy_text, _invalidation_count
            with patch_stdout(raw=True):
                session = PromptSession(bottom_toolbar=_bottom_toolbar)
                input_result = []

                async def prompt_task():
                    try:
                        result = await session.prompt_async("> ")
                        input_result.append(result)
                    except (EOFError, KeyboardInterrupt):
                        input_result.append("EOF")

                async def invalidation_task():
                    global _busy_text, _invalidation_count
                    # Rapid invalidation: 20 cycles at 0.1s intervals
                    for tick in range(20):
                        _busy_text = f"Thinking... {tick + 1}s"
                        if session.app:
                            session.app.invalidate()
                            _invalidation_count += 1
                        await asyncio.sleep(0.1)
                    _busy_text = ""
                    if session.app:
                        session.app.invalidate()

                prompt = asyncio.create_task(prompt_task())
                await asyncio.sleep(0.3)

                invalidator = asyncio.create_task(invalidation_task())
                while _invalidation_count < 5 and not invalidator.done():
                    await asyncio.sleep(0.02)
                raw_print("PTY_READY")

                # Wait for prompt to complete (user submits input)
                try:
                    await asyncio.wait_for(prompt, timeout=10.0)
                except asyncio.TimeoutError:
                    input_result.append("TIMEOUT")
                    prompt.cancel()
                    try:
                        await prompt
                    except asyncio.CancelledError:
                        pass

                # Cancel invalidator if still running
                if not invalidator.done():
                    invalidator.cancel()
                    try:
                        await invalidator
                    except asyncio.CancelledError:
                        pass

                if input_result:
                    raw_print(f"PTY_INPUT: {input_result[0]}")
                raw_print(f"PTY_INVALIDATIONS: {_invalidation_count}")

        asyncio.run(main())
    """)


def _multiline_typeahead_script() -> str:
    """Script that tests longer input during invalidation.

    Sends a multi-word string character by character (via sendline) while
    invalidation fires, verifying the full string arrives intact.
    """
    return textwrap.dedent("""\
        import asyncio, sys, os
        from prompt_toolkit.patch_stdout import patch_stdout
        from prompt_toolkit import PromptSession

        _raw_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw_print(text):
            _raw_stderr.write(text + "\\n")
            _raw_stderr.flush()

        _busy_text = ""

        def _bottom_toolbar():
            if _busy_text:
                return [("class:bottom-toolbar", f" {_busy_text} ")]
            return [("class:bottom-toolbar", " idle ")]

        async def main():
            global _busy_text
            with patch_stdout(raw=True):
                session = PromptSession(bottom_toolbar=_bottom_toolbar)

                async def prompt_task():
                    try:
                        result = await session.prompt_async("> ")
                        raw_print(f"PTY_INPUT: {result}")
                    except (EOFError, KeyboardInterrupt):
                        raw_print("PTY_INPUT: EOF")

                async def invalidation_task():
                    global _busy_text
                    for tick in range(15):
                        _busy_text = f"read_file {tick + 1}s"
                        if session.app:
                            session.app.invalidate()
                        await asyncio.sleep(0.15)

                prompt = asyncio.create_task(prompt_task())
                await asyncio.sleep(0.3)
                raw_print("PTY_READY")

                invalidator = asyncio.create_task(invalidation_task())

                # Wait for prompt to complete
                try:
                    await asyncio.wait_for(prompt, timeout=8.0)
                except asyncio.TimeoutError:
                    raw_print("PTY_INPUT: TIMEOUT")
                    prompt.cancel()
                    try:
                        await prompt
                    except asyncio.CancelledError:
                        pass

                invalidator.cancel()
                try:
                    await invalidator
                except asyncio.CancelledError:
                    pass

        asyncio.run(main())
    """)


def _tool_registry_busy_script() -> str:
    """Drive the real ToolRegistry.call_tool path during prompt_async()."""
    return textwrap.dedent("""\
        import asyncio, os, sys, tempfile, time
        from prompt_toolkit.patch_stdout import patch_stdout
        from prompt_toolkit import PromptSession
        from anteroom.tools import ToolRegistry, register_default_tools
        from anteroom.tools import glob_tool

        _raw_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw_print(text):
            _raw_stderr.write(text + "\\n")
            _raw_stderr.flush()

        def _bottom_toolbar():
            return [("class:bottom-toolbar", " busy ")]

        async def main():
            with tempfile.TemporaryDirectory() as tmpdir:
                open(os.path.join(tmpdir, "a.txt"), "w").write("hello\\n")
                open(os.path.join(tmpdir, "b.txt"), "w").write("world\\n")

                original = glob_tool._glob_matches

                def slow_glob(base, pattern):
                    time.sleep(1.5)
                    return original(base, pattern)

                glob_tool._glob_matches = slow_glob
                registry = ToolRegistry()
                register_default_tools(registry, working_dir=tmpdir)

                with patch_stdout(raw=True):
                    session = PromptSession(bottom_toolbar=_bottom_toolbar)

                    async def prompt_task():
                        try:
                            result = await session.prompt_async("> ")
                            raw_print(f"PTY_INPUT: {result}")
                        except KeyboardInterrupt:
                            raw_print("PTY_INPUT: KEYBOARD_INTERRUPT")
                        except EOFError:
                            raw_print("PTY_INPUT: EOF")

                    async def tool_task():
                        result = await registry.call_tool("glob_files", {"pattern": "**/*"})
                        raw_print(f"TOOL_DONE: {result.get('count', -1)}")

                    prompt = asyncio.create_task(prompt_task())
                    await asyncio.sleep(0.2)
                    tool = asyncio.create_task(tool_task())
                    raw_print("PTY_READY")

                    try:
                        await asyncio.wait_for(prompt, timeout=10.0)
                    except asyncio.TimeoutError:
                        raw_print("PTY_INPUT: TIMEOUT")
                        prompt.cancel()
                        try:
                            await prompt
                        except asyncio.CancelledError:
                            pass

                    await tool

        asyncio.run(main())
    """)


def _renderer_tool_ticker_prompt_script() -> str:
    """Drive the renderer tool ticker while prompt_async is accepting queued input."""
    return textwrap.dedent("""\
        import asyncio, os, sys, time
        from prompt_toolkit.patch_stdout import patch_stdout
        from prompt_toolkit import PromptSession
        import anteroom.cli.renderer as renderer

        _raw_stderr = os.fdopen(os.dup(sys.stderr.fileno()), "w", newline="")

        def raw_print(text):
            _raw_stderr.write(text + "\\n")
            _raw_stderr.flush()

        def _bottom_toolbar():
            # Keep toolbar content stable in this PTY test. prompt_toolkit's
            # CPR-dependent toolbar rendering is covered elsewhere; here any
            # visible ticker label before PTY_TICKER_READY means raw output
            # repainted over the prompt.
            return [("class:bottom-toolbar", " busy ")]

        async def main():
            with patch_stdout(raw=True):
                session = PromptSession(bottom_toolbar=_bottom_toolbar)
                renderer.use_stdout_console()

                def invalidate():
                    if session.app:
                        session.app.invalidate()

                renderer._toolbar_invalidator = invalidate
                renderer._toolbar_is_active = lambda: bool(session.app and session.app.is_running)
                prompt_active = [False]
                renderer._prompt_is_active = lambda: prompt_active[0]

                async def prompt_task():
                    prompt_active[0] = True
                    try:
                        result = await session.prompt_async("> ")
                        raw_print(f"PTY_INPUT: {result}")
                    except KeyboardInterrupt:
                        raw_print("PTY_INPUT: KEYBOARD_INTERRUPT")
                    except EOFError:
                        raw_print("PTY_INPUT: EOF")
                    finally:
                        prompt_active[0] = False

                prompt = asyncio.create_task(prompt_task())
                await asyncio.sleep(0.3)
                raw_print("PTY_READY")

                renderer._tool_start = time.monotonic() - 5.0
                renderer.start_tool_ticker("Finding **/config.yaml")
                await asyncio.sleep(0.8)
                raw_print("PTY_TICKER_READY")

                try:
                    await asyncio.wait_for(prompt, timeout=8.0)
                except asyncio.TimeoutError:
                    raw_print("PTY_INPUT: TIMEOUT")
                    prompt.cancel()
                    try:
                        await prompt
                    except asyncio.CancelledError:
                        pass
                finally:
                    renderer.stop_tool_ticker_sync()
                    renderer._tool_start = 0
                    renderer._toolbar_invalidator = None
                    renderer._toolbar_is_active = None
                    renderer._prompt_is_active = None
                    renderer._footer_mode = False

        asyncio.run(main())
    """)


@pytest.mark.integration
class TestReplBusyPty:
    """PTY tests for input stability under concurrent async invalidation (#1134).

    These tests verify that prompt_toolkit's prompt_async delivers typed input
    correctly when a concurrent background task fires app.invalidate()
    repeatedly — the same concurrency pattern used by the 0.5s thinking/tool
    ticker in the real REPL.

    Toolbar *content rendering* is verified at the unit level (see
    TestFormatStatusToolbar, TestBusyToolbarTheme) since prompt_toolkit's
    toolbar rendering requires terminal CPR support unavailable in PTY tests.
    """

    def test_input_survives_rapid_invalidation(self) -> None:
        """Typed text arrives intact despite 20 rapid invalidation cycles."""
        child = pexpect.spawn(
            _PYTHON,
            ["-c", _concurrent_invalidation_script()],
            timeout=15,
            encoding="utf-8",
        )
        try:
            child.expect("PTY_READY", timeout=10)
            # Type while rapid invalidation is running
            child.sendline("fix the login bug")
            # Input must arrive exactly as typed
            child.expect("PTY_INPUT: fix the login bug", timeout=10)
            # At least some invalidations should have fired
            child.expect(r"PTY_INVALIDATIONS: (\d+)", timeout=5)
            count = int(child.match.group(1))
            assert count >= 5, f"Expected >=5 invalidations, got {count}"
            child.expect(pexpect.EOF, timeout=5)
        finally:
            if child.isalive():
                child.terminate(force=True)

    def test_longer_input_survives_invalidation(self) -> None:
        """A longer multi-word input survives 15 invalidation cycles."""
        child = pexpect.spawn(
            _PYTHON,
            ["-c", _multiline_typeahead_script()],
            timeout=15,
            encoding="utf-8",
        )
        try:
            child.expect("PTY_READY", timeout=10)
            child.sendline("add API coverage for failed workflow runs too")
            child.expect(
                "PTY_INPUT: add API coverage for failed workflow runs too",
                timeout=10,
            )
            child.expect(pexpect.EOF, timeout=5)
        finally:
            if child.isalive():
                child.terminate(force=True)

    def test_input_survives_real_tool_registry_call(self) -> None:
        """Typed input should land before a slow built-in tool call finishes."""
        child = pexpect.spawn(
            _PYTHON,
            ["-c", _tool_registry_busy_script()],
            timeout=15,
            encoding="utf-8",
        )
        try:
            child.expect("PTY_READY", timeout=10)
            child.sendline("queued while glob runs")
            child.expect("PTY_INPUT: queued while glob runs", timeout=5)
            child.expect(r"TOOL_DONE: (\d+)", timeout=10)
            assert int(child.match.group(1)) >= 1
            child.expect(pexpect.EOF, timeout=5)
        finally:
            if child.isalive():
                child.terminate(force=True)

    def test_renderer_tool_ticker_does_not_raw_repaint_active_prompt(self) -> None:
        """A tool-only ticker should not write its label over the queued-input prompt."""
        child = pexpect.spawn(
            _PYTHON,
            ["-c", _renderer_tool_ticker_prompt_script()],
            timeout=15,
            encoding="utf-8",
        )
        try:
            child.expect("PTY_READY", timeout=10)
            matched = child.expect([r"Finding \*\*/config\.yaml", "PTY_TICKER_READY"], timeout=5)
            assert matched == 1, "tool ticker label leaked as raw prompt-overwriting output"
            child.sendline("queued while ticker runs")
            child.expect("PTY_INPUT: queued while ticker runs", timeout=5)
            child.expect(pexpect.EOF, timeout=5)
        finally:
            if child.isalive():
                child.terminate(force=True)

    def test_ctrl_c_survives_real_tool_registry_call(self) -> None:
        """Ctrl-C should still reach the prompt while a built-in tool runs."""
        child = pexpect.spawn(
            _PYTHON,
            ["-c", _tool_registry_busy_script()],
            timeout=15,
            encoding="utf-8",
        )
        try:
            child.expect("PTY_READY", timeout=10)
            child.sendcontrol("c")
            child.expect("PTY_INPUT: KEYBOARD_INTERRUPT", timeout=5)
            child.expect(r"TOOL_DONE: (\d+)", timeout=10)
            child.expect(pexpect.EOF, timeout=5)
        finally:
            if child.isalive():
                child.terminate(force=True)
