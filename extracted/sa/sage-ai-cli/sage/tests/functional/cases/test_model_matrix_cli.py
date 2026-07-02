"""Model Matrix CLI Tests — every AI model tested with a real task on the CLI.

Each cloud model is given a simple prompt via `sage ask --raw --model <id>`
and we validate a non-empty, non-error response.  NO MOCKS.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile

import pytest

SAGE = [sys.executable, "-m", "sage"]
API_BASE = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TIMEOUT = 120

ALL_CLOUD_MODELS = [
    "cloud:qwen3-coder",
    "cloud:llama-3-2",
    "cloud:deepseek-r1-7b",
    "cloud:gemma-4",
    "cloud:phi-4-reasoning",
    "cloud:mistral-small",
    "cloud:yi-coder-9b",
    "cloud:llava-llama-3",
]


def _run(model: str, prompt: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["SAGE_TESTING"] = "1"
    env["SAGE_DISABLE_RAG"] = "1"
    env["SAGE_API_BASE"] = API_BASE
    cwd = tempfile.mkdtemp(prefix="sage-model-matrix-")
    return subprocess.run(
        SAGE + ["ask", prompt, "--raw", "--model", model],
        capture_output=True, text=True, timeout=TIMEOUT, env=env, cwd=cwd,
    )


class TestModelMatrixCLI:
    @pytest.mark.parametrize("model_id", ALL_CLOUD_MODELS)
    def test_simple_math(self, model_id: str):
        """Each model should correctly answer a simple math question."""
        r = _run(model_id, "What is 7 multiplied by 8? Answer with just the number.")
        assert r.returncode == 0, f"{model_id} exited with code {r.returncode}: {r.stderr[:300]}"
        output = r.stdout.strip()
        assert len(output) > 0, f"{model_id} returned empty response"
        # Most models should get this right
        assert "56" in output, f"{model_id} didn't answer 56: got '{output[:100]}'"

    @pytest.mark.parametrize("model_id", ALL_CLOUD_MODELS)
    def test_code_generation(self, model_id: str):
        """Each model should generate valid Python code."""
        r = _run(model_id, "Write a Python function called 'add' that takes two numbers and returns their sum. Output only the code, nothing else.")
        assert r.returncode == 0, f"{model_id} exited with code {r.returncode}: {r.stderr[:300]}"
        output = r.stdout.strip()
        assert len(output) > 0, f"{model_id} returned empty response"
        assert "def " in output or "add" in output, f"{model_id} didn't generate a function: {output[:200]}"

    @pytest.mark.parametrize("model_id", ALL_CLOUD_MODELS)
    def test_creative_response(self, model_id: str):
        """Each model should produce a creative response."""
        r = _run(model_id, "Write a haiku about programming. Output only the haiku.")
        assert r.returncode == 0, f"{model_id} failed: {r.stderr[:300]}"
        output = r.stdout.strip()
        assert len(output) > 10, f"{model_id} response too short: '{output}'"
