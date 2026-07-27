"""Sandboxed Python REPL tool.

Why: small models hallucinate numerical and structural answers. Giving them
a Python REPL to *compute* the answer eliminates a huge class of mistakes:
"how many items match X?", "what's the structure of this JSON?", "what's
the sum of column Y?" — all become deterministic when the model can run
code instead of guessing.

Sandboxing approach:
  - subprocess isolation (so RuntimeError in user code can't corrupt sage)
  - hard timeout (default 5s)
  - hard memory cap (default 256MB) via resource.setrlimit on POSIX
  - output cap (default 16KB)
  - `python -I` (isolated mode) to block site-packages by default
  - cwd defaults to a temp dir, not the user's project

This is NOT a security boundary against malicious users — sage runs as
the user. It is a safety boundary against the *model* writing infinite
loops, fork bombs, or runaway memory allocation.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass

__all__ = ["PythonReplResult", "PythonRepl", "run_python"]


@dataclass
class PythonReplResult:
    ok: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_s: float
    truncated: bool = False

    def to_text(self) -> str:
        parts = []
        if self.stdout:
            parts.append(f"STDOUT:\n{self.stdout}")
        if self.stderr:
            parts.append(f"STDERR:\n{self.stderr}")
        if self.truncated:
            parts.append("(output truncated)")
        if not self.ok:
            parts.append(f"EXIT: {self.exit_code}")
        return "\n".join(parts) if parts else "(no output)"


_PRELUDE = """\
import sys, json, math, statistics, re, os, itertools, functools, collections
from pathlib import Path
"""


def _set_resource_limits(memory_mb: int) -> None:
    """Best-effort POSIX-only memory cap. No-op on Windows."""
    try:
        import resource
        bytes_cap = memory_mb * 1024 * 1024
        # RLIMIT_AS = total virtual memory. Tighter than RLIMIT_DATA on many systems.
        resource.setrlimit(resource.RLIMIT_AS, (bytes_cap, bytes_cap))
    except (ImportError, ValueError, OSError):
        pass


class PythonRepl:
    """Run user/model-provided Python code in an isolated subprocess."""

    def __init__(
        self,
        *,
        timeout_s: float = 5.0,
        memory_mb: int = 256,
        max_output_bytes: int = 16 * 1024,
        allow_network: bool = False,
    ):
        self.timeout_s = timeout_s
        self.memory_mb = memory_mb
        self.max_output_bytes = max_output_bytes
        self.allow_network = allow_network

    def run(self, code: str, *, cwd: str | None = None, env: dict | None = None) -> PythonReplResult:
        import time
        if not code.strip():
            return PythonReplResult(ok=True, stdout="", stderr="", exit_code=0, duration_s=0.0)

        full_code = _PRELUDE + "\n" + code
        run_env = dict(os.environ) if env is None else dict(env)
        # Strip network-related env if explicitly disallowed (best-effort, not a sandbox)
        if not self.allow_network:
            for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
                run_env.pop(k, None)
        run_env["PYTHONDONTWRITEBYTECODE"] = "1"
        run_env["PYTHONIOENCODING"] = "utf-8"

        tmp_dir = cwd or tempfile.mkdtemp(prefix="sage-repl-")
        cleanup_tmp = cwd is None

        t0 = time.time()
        try:
            proc = subprocess.Popen(
                [sys.executable, "-I", "-c", full_code],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=tmp_dir,
                env=run_env,
                preexec_fn=(lambda: _set_resource_limits(self.memory_mb))
                if os.name == "posix" else None,
            )
            try:
                out_bytes, err_bytes = proc.communicate(timeout=self.timeout_s)
                exit_code = proc.returncode
                timed_out = False
            except subprocess.TimeoutExpired:
                proc.kill()
                out_bytes, err_bytes = proc.communicate()
                exit_code = -9
                timed_out = True

            stdout = out_bytes.decode("utf-8", errors="replace")
            stderr = err_bytes.decode("utf-8", errors="replace")
            truncated = False
            if len(stdout) > self.max_output_bytes:
                stdout = stdout[: self.max_output_bytes]
                truncated = True
            if len(stderr) > self.max_output_bytes:
                stderr = stderr[: self.max_output_bytes]
                truncated = True
            if timed_out:
                stderr += f"\n[TIMEOUT after {self.timeout_s}s]"
            return PythonReplResult(
                ok=(exit_code == 0 and not timed_out),
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                duration_s=time.time() - t0,
                truncated=truncated,
            )
        finally:
            if cleanup_tmp:
                try:
                    shutil.rmtree(tmp_dir, ignore_errors=True)
                except OSError:
                    pass


def run_python(code: str, *, timeout_s: float = 5.0) -> PythonReplResult:
    return PythonRepl(timeout_s=timeout_s).run(code)
