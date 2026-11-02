"""Smoke-test the built wheel in clean environments."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

BASE_SMOKE = r"""
import importlib.util
import use_computer

def has(name):
    try:
        return importlib.util.find_spec(name) is not None
    except ModuleNotFoundError:
        return False

assert "site-packages" in (use_computer.__file__ or ""), use_computer.__file__
for name in ["PIL", "openai", "anthropic", "google.genai", "litellm"]:
    assert not has(name), name
"""

AGENTS_SMOKE = r"""
import asyncio
import importlib
import importlib.util
import tempfile
from pathlib import Path

assert importlib.util.find_spec("PIL") is not None
for name in ["openai", "anthropic", "google.genai", "litellm"]:
    assert importlib.util.find_spec(name) is not None, name
for path in ["use_computer.agents", "use_computer.agents.debug"]:
    importlib.import_module(path)

from use_computer.agents import (
    AnthropicComputerAgent,
    GeminiComputerAgent,
    GenericComputerAgent,

    OpenAIComputerAgent,
)
from use_computer.agents.debug import DebugComputerAgent
from use_computer.core.models import ExecResult

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff"
    b"\xff?\x00\x05\xfe\x02\xfeA\xe2`\\\x00\x00\x00\x00IEND\xaeB`\x82"
)

class Recording:
    async def start(self, name="trial"):
        raise RuntimeError("recording disabled")

class Screenshot:
    async def take_full_screen(self):
        return PNG_BYTES

class Display:
    async def get_windows(self):
        return [{"role": "window", "title": "Fake"}]

class Mouse:
    def __init__(self):
        self.clicks = []

    async def click(self, x, y, button="left", double=False):
        self.clicks.append((x, y, button, double))

class Sandbox:
    def __init__(self):
        self.sandbox_id = "fake"
        self.screenshot = Screenshot()
        self.recording = Recording()
        self.display = Display()
        self.mouse = Mouse()
        self.commands = []

    async def exec_ssh(self, command, timeout=120):
        self.commands.append(command)
        return ExecResult(return_code=0, stdout="ok", stderr="")

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    sandbox = Sandbox()
    result = asyncio.run(
        DebugComputerAgent(max_steps=1).run(
            "smoke",
            sandbox=sandbox,
            logs_dir=root / "agent",
            task_dir=root / "task",
        )
    )
    assert sandbox.mouse.clicks == [(960, 540, "left", False)]
    assert sandbox.commands == ["echo hello world"]
    assert result.final_message == "smoke"

for agent_cls, model_name in [
    (AnthropicComputerAgent, "anthropic/claude-sonnet-4-6"),
    (OpenAIComputerAgent, "openai/gpt-5.5"),
    (GeminiComputerAgent, "gemini/gemini-2.5-computer-use-preview-10-2025"),
    (GenericComputerAgent, "openai/gpt-4o"),

]:
    assert agent_cls(model_name=model_name, max_steps=1).max_steps == 1
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()

    wheel = args.wheel.resolve()
    if not wheel.name.endswith(".whl"):
        raise SystemExit(f"expected a wheel path, got {wheel}")

    _check_wheel_contents(wheel)
    _check_metadata(wheel)
    _smoke_install(wheel, None, BASE_SMOKE)
    _smoke_install(wheel, "agents", AGENTS_SMOKE)


def _check_wheel_contents(wheel: Path) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())

    required = {
        "use_computer/py.typed",
        "use_computer/agents/prompts/anthropic.txt",
        "use_computer/agents/prompts/gemini.txt",
        "use_computer/agents/prompts/openai.txt",
        "use_computer/agents/prompts/pyautogui.txt",
    }
    missing = sorted(required - names)
    if missing:
        raise SystemExit(f"wheel is missing files: {missing}")

    forbidden = [name for name in names if "__pycache__" in name or name.startswith("tests/")]
    if forbidden:
        raise SystemExit(f"wheel contains generated/test files: {sorted(forbidden)[:10]}")


def _check_metadata(wheel: Path) -> None:
    with zipfile.ZipFile(wheel) as archive:
        metadata_name = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        metadata = archive.read(metadata_name).decode()

    required = [
        "Provides-Extra: agents",
        "Requires-Dist: pillow>=10; extra == 'agents'",
        "Requires-Dist: openai>=1; extra == 'agents'",
        "Requires-Dist: anthropic>=0.86; extra == 'agents'",
        "Requires-Dist: litellm>=1; extra == 'agents'",
        "Requires-Dist: google-genai>=1; extra == 'agents'",
    ]
    missing = [line for line in required if line not in metadata]
    if missing:
        raise SystemExit(f"wheel metadata is missing: {missing}")

    forbidden = [
        f"Provides-Extra: agents-{name}"
        for name in ("openai", "anthropic", "litellm", "gemini", "all")
    ]
    present = [line for line in forbidden if line in metadata]
    if present:
        raise SystemExit(f"wheel metadata still has provider-specific extras: {present}")


def _smoke_install(wheel: Path, extra: str | None, code: str) -> None:
    with tempfile.TemporaryDirectory(prefix="use-computer-wheel-") as tmp:
        tmp_path = Path(tmp)
        venv = tmp_path / "venv"
        _run(["uv", "venv", "--python", sys.executable, str(venv)], cwd=tmp_path)
        python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        requirement = f"{wheel}[{extra}]" if extra else str(wheel)
        _run(["uv", "pip", "install", "--python", str(python), requirement], cwd=tmp_path)
        _run([str(python), "-c", code], cwd=tmp_path)


def _run(cmd: list[str], *, cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


if __name__ == "__main__":
    main()
