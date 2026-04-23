"""PTY-backed integration coverage for compact sub-agent CLI UX (#1460)."""

from __future__ import annotations

import io
import sys
import textwrap

import pytest

pexpect = pytest.importorskip("pexpect", reason="pexpect required for PTY tests")

_PYTHON = sys.executable


def _render_script() -> str:
    return textwrap.dedent("""\
        from pathlib import Path
        import sys
        from rich.console import Console

        sys.path.insert(0, str((Path.cwd() / "src").resolve()))
        from anteroom.cli import renderer

        plain = Console(file=sys.stdout, force_terminal=False, color_system=None, width=120)
        renderer.console = plain
        renderer._stdout_console = plain
        renderer.clear_subagent_state()
        renderer.render_subagent_start(
            "agent-12345678",
            "Inspect the renderer flow across two files and report back.",
            "gpt-test",
            1,
        )
        renderer.render_subagent_tool("agent-12345678", "read_file")
        renderer.render_subagent_tool("agent-12345678", "bash")
        renderer.render_subagent_end("agent-12345678", 2.3, ["read_file", "bash"])
        print("PTY_DONE")
    """)


def _detached_script() -> str:
    return textwrap.dedent("""\
        from pathlib import Path
        import sys
        import types
        from rich.console import Console

        sys.path.insert(0, str((Path.cwd() / "src").resolve()))
        sys.modules.setdefault("filetype", types.SimpleNamespace(guess=lambda *_a, **_k: None))
        from anteroom.cli import renderer
        from anteroom.cli.repl import poll_detached_agents

        class FakeDetachManager:
            def poll_completed(self):
                return [
                    {
                        "id": "12345678abcdef00",
                        "status": "completed",
                        "metadata": {
                            "task_result": {
                                "summary": "Found three files that need follow-up edits.",
                                "tool_calls": ["read_file", "bash"],
                                "duration_seconds": 4.2,
                            }
                        },
                    },
                    {
                        "id": "87654321fedcba00",
                        "status": "failed",
                        "metadata": {
                            "task_result": {
                                "error": "permission denied while opening config\\ntraceback omitted",
                                "tool_calls": [],
                                "duration_seconds": 0.5,
                            }
                        },
                    },
                ]

        plain = Console(file=sys.stdout, force_terminal=False, color_system=None, width=140)
        renderer.console = plain
        renderer._stdout_console = plain
        poll_detached_agents(FakeDetachManager(), plain)
        print("PTY_DONE")
    """)


@pytest.mark.integration
class TestReplSubagentLivePTY:
    def test_foreground_subagent_surface_is_compact(self) -> None:
        buf = io.StringIO()
        child = pexpect.spawn(_PYTHON, ["-c", _render_script()], timeout=15, encoding="utf-8")
        child.logfile_read = buf

        child.expect("PTY_DONE", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
        output = buf.getvalue()

        assert "▶ agent-12345678" in output
        assert "Inspect the renderer flow across two files and report back." in output
        assert "done · 2.3s · 2 tools" in output
        assert "read_file" not in output
        assert "bash" not in output

    def test_detached_completion_notification_includes_status_fields(self) -> None:
        buf = io.StringIO()
        child = pexpect.spawn(_PYTHON, ["-c", _detached_script()], timeout=15, encoding="utf-8")
        child.logfile_read = buf

        child.expect("PTY_DONE", timeout=10)
        child.expect(pexpect.EOF, timeout=5)
        output = buf.getvalue()

        assert "[agent 12345678]" in output
        assert "done · 4.2s · 2 tools" in output
        assert "Found three files that need follow-up edits." in output
        assert "[agent 87654321]" in output
        assert "failed · 0.5s" in output
        assert "permission denied while opening config" in output
