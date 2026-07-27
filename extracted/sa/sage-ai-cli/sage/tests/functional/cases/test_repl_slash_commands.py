"""REPL Slash Command Tests — every `/slash` command exercised via `sage run --prompt`.

Each test feeds a slash command through the `--prompt` flag which enters the
REPL, executes the command, and exits.  NO MOCKS.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SAGE = [sys.executable, "-m", "sage"]
TIMEOUT = 120
MODEL = "cloud:qwen3-coder"


def _run_repl(slash_cmd: str, timeout: int = TIMEOUT) -> subprocess.CompletedProcess:
    """Feed *slash_cmd* as the initial prompt — the REPL will execute it, then `--prompt` exits."""
    env = os.environ.copy()
    env["SAGE_DISABLE_RAG"] = "1"
    env["SAGE_API_BASE"] = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
    cwd = tempfile.mkdtemp(prefix="sage-repl-")

    # Use stdin to feed the slash command, then EOF to exit
    proc = subprocess.run(
        SAGE + ["run", "--model", MODEL],
        input=f"{slash_cmd}\nexit\n",
        capture_output=True, text=True, timeout=timeout, env=env, cwd=cwd,
    )
    return proc


# ── Information commands ─────────────────────────────────────────────────

class TestREPLInfoCommands:
    def test_help(self):
        r = _run_repl("/help")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "help" in combined.lower() or "command" in combined.lower()

    def test_version(self):
        r = _run_repl("/version")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        # Should contain a version string
        assert "sage" in combined.lower() or "version" in combined.lower()

    def test_status(self):
        r = _run_repl("/status")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "model" in combined.lower() or "active" in combined.lower()

    def test_context(self):
        r = _run_repl("/context")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "token" in combined.lower() or "message" in combined.lower()

    def test_history(self):
        r = _run_repl("/history")
        assert r.returncode == 0

    def test_files_empty(self):
        r = _run_repl("/files")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "no files" in combined.lower() or "written" in combined.lower()


# ── Model commands ───────────────────────────────────────────────────────

class TestREPLModelCommands:
    def test_model_show_current(self):
        r = _run_repl("/model")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "model" in combined.lower()

    def test_model_switch(self):
        r = _run_repl("/model cloud:llama-3-2")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "llama" in combined.lower() or "changed" in combined.lower() or "model" in combined.lower()

    def test_models_list(self):
        r = _run_repl("/models")
        assert r.returncode == 0


# ── Toggle commands ──────────────────────────────────────────────────────

class TestREPLToggleCommands:
    def test_think_on(self):
        r = _run_repl("/think on")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "thinking" in combined.lower() or "verbose" in combined.lower() or "enabled" in combined.lower()

    def test_think_off(self):
        r = _run_repl("/think off")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "thinking" in combined.lower() or "disabled" in combined.lower() or "normal" in combined.lower()

    def test_tdd_on(self):
        r = _run_repl("/tdd on")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "tdd" in combined.lower() or "enabled" in combined.lower()

    def test_tdd_off(self):
        r = _run_repl("/tdd off")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "tdd" in combined.lower() or "disabled" in combined.lower()


# ── Context management ───────────────────────────────────────────────────

class TestREPLContextCommands:
    def test_clear(self):
        r = _run_repl("/clear")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "clear" in combined.lower()

    def test_compact(self):
        r = _run_repl("/compact")
        assert r.returncode == 0

    def test_system_show(self):
        r = _run_repl("/system")
        assert r.returncode == 0

    def test_system_set(self):
        r = _run_repl("/system You are a helpful assistant.")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "system" in combined.lower() or "updated" in combined.lower()


# ── File commands ────────────────────────────────────────────────────────

class TestREPLFileCommands:
    def test_read_nonexistent(self):
        r = _run_repl("/read nonexistent_file.txt")
        assert r.returncode == 0
        combined = r.stdout + r.stderr
        assert "not found" in combined.lower() or "error" in combined.lower()

    def test_read_existing(self):
        # Create a file first, then read it
        tmp = tempfile.mkdtemp(prefix="sage-read-")
        (Path(tmp) / "testfile.txt").write_text("hello from test")
        env = os.environ.copy()
        env["SAGE_DISABLE_RAG"] = "1"
        env["SAGE_API_BASE"] = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
        proc = subprocess.run(
            SAGE + ["run", "--model", MODEL],
            input="/read testfile.txt\nexit\n",
            capture_output=True, text=True, timeout=TIMEOUT, env=env, cwd=tmp,
        )
        assert proc.returncode == 0
        combined = proc.stdout + proc.stderr
        assert "read" in combined.lower() or "testfile" in combined.lower()


# ── Test command ─────────────────────────────────────────────────────────

class TestREPLTestCommand:
    def test_slash_test(self):
        r = _run_repl("/test echo hello")
        assert r.returncode == 0


# ── RAG commands ─────────────────────────────────────────────────────────

class TestREPLRagCommands:
    def test_rag_status(self):
        r = _run_repl("/rag status")
        assert r.returncode == 0

    def test_rag_index(self):
        r = _run_repl("/rag index")
        assert r.returncode == 0

    def test_rag_query(self):
        r = _run_repl("/rag query test query")
        assert r.returncode == 0
