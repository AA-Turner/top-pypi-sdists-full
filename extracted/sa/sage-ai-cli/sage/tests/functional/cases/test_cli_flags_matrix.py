"""CLI Flag Matrix Tests — combinatorial testing of `sage run` and `sage ask` flags.

Tests flag combinations like --model, --temperature, --max-tokens, --verbose,
--quiet, --output, --no-color, --raw, --no-agent, --image, --file.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SAGE = [sys.executable, "-m", "sage"]
API_BASE = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TIMEOUT = 120

MODELS = [
    "cloud:qwen3-coder",
    "cloud:llama-3-2",
    "cloud:deepseek-r1-7b",
    "cloud:gemma-4",
    "cloud:phi-4-reasoning",
    "cloud:mistral-small",
    "cloud:yi-coder-9b",
]


def _run(args: list[str], timeout: int = TIMEOUT) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["SAGE_DISABLE_RAG"] = "1"
    env["SAGE_API_BASE"] = API_BASE

    project_root = str(Path(__file__).resolve().parent.parent.parent.parent.parent)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{project_root}:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = project_root

    cwd = tempfile.mkdtemp(prefix="sage-flag-matrix-")
    return subprocess.run(
        SAGE + args, capture_output=True, text=True, timeout=timeout, env=env, cwd=cwd,
    )


# ── sage ask flag combos ─────────────────────────────────────────────────

class TestAskFlags:
    """Test `sage ask` with various flag combinations."""

    def test_ask_raw(self):
        r = _run(["ask", "What is 2+2?", "--raw", "--model", "cloud:qwen3-coder"])
        assert r.returncode == 0
        assert len(r.stdout.strip()) > 0

    def test_ask_no_agent(self):
        r = _run(["ask", "What is Python?", "--no-agent", "--model", "cloud:qwen3-coder"])
        assert r.returncode == 0

    def test_ask_agent(self):
        """--agent triggers the full agentic loop via `sage run --prompt`."""
        r = _run(["ask", "Write hello world to hello.txt and stop", "--agent", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0

    def test_ask_temperature_low(self):
        r = _run(["ask", "What is 1+1?", "--raw", "--model", "cloud:qwen3-coder", "--temperature", "0.0"])
        assert r.returncode == 0

    def test_ask_temperature_high(self):
        r = _run(["ask", "Tell me a joke", "--raw", "--model", "cloud:qwen3-coder", "--temperature", "1.5"])
        assert r.returncode == 0

    def test_ask_max_tokens_small(self):
        r = _run(["ask", "Say hello", "--raw", "--model", "cloud:qwen3-coder", "--max-tokens", "50"])
        assert r.returncode == 0
        # Should be short due to token limit
        assert len(r.stdout.strip()) < 500

    def test_ask_max_tokens_large(self):
        r = _run(["ask", "Explain quantum computing", "--raw", "--model", "cloud:qwen3-coder", "--max-tokens", "1024"])
        assert r.returncode == 0

    def test_ask_with_file(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False)
        tmp.write("This is test content for file attachment.")
        tmp.close()
        r = _run(["ask", "Summarize this file", "--raw", "--model", "cloud:qwen3-coder", "--file", tmp.name])
        assert r.returncode == 0
        os.unlink(tmp.name)

    def test_ask_with_image(self):
        """Create a tiny valid PNG and pass it via --image."""
        import struct, zlib
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        # Minimal 1x1 red PNG
        def _png_chunk(chunk_type, data):
            c = chunk_type + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

        signature = b"\x89PNG\r\n\x1a\n"
        ihdr = _png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        raw = b"\x00\xff\x00\x00"  # filter byte + RGB
        idat = _png_chunk(b"IDAT", zlib.compress(raw))
        iend = _png_chunk(b"IEND", b"")
        tmp.write(signature + ihdr + idat + iend)
        tmp.close()

        r = _run(["ask", "What do you see in this image?", "--raw", "--model", "cloud:llava-llama-3", "--image", tmp.name])
        # Vision model may or may not be available — accept 0 or 1
        assert r.returncode in (0, 1)
        os.unlink(tmp.name)


# ── sage run flag combos ─────────────────────────────────────────────────

class TestRunFlags:
    """Test `sage run` with various flag combinations."""

    def test_run_prompt_quiet(self):
        r = _run(["run", "--prompt", "Create a file test.txt with content hello and stop", "--quiet", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0

    def test_run_prompt_verbose(self):
        r = _run(["run", "--prompt", "Say hello and stop", "--verbose", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0

    def test_run_output_quiet(self):
        r = _run(["run", "--prompt", "print hello and stop", "--output", "quiet", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0

    def test_run_output_verbose(self):
        r = _run(["run", "--prompt", "print hello and stop", "--output", "verbose", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0

    def test_run_no_color(self):
        r = _run(["run", "--prompt", "print hello and stop", "--no-color", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0
        # No ANSI escape codes
        assert "\033[" not in r.stdout

    def test_run_no_auto_run(self):
        """--no-auto-run should prompt before executing bash — but with --prompt it still works."""
        r = _run(["run", "--prompt", "say hello and stop", "--no-auto-run", "--model", "cloud:qwen3-coder"], timeout=300)
        assert r.returncode == 0


# ── Model flag across all models ─────────────────────────────────────────

class TestModelFlagMatrix:
    """Ensure every registered cloud model can be selected via --model."""

    @pytest.mark.parametrize("model_id", MODELS)
    def test_ask_with_model(self, model_id: str):
        r = _run(["ask", "What is 1+1?", "--raw", "--model", model_id])
        assert r.returncode == 0, f"Model {model_id} failed: {r.stderr[:300]}"
        assert len(r.stdout.strip()) > 0, f"Model {model_id} returned empty response"
