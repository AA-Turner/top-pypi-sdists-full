"""
cvc.agent.scaffolder — Deterministic project scaffolding engine.

Instead of asking the LLM to create files one-by-one, this module runs
the *official* CLI scaffolding commands for each tech stack (e.g.
``uv init``, ``npx create-next-app``, ``cargo init``, ``flutter create``).

Key design decisions
--------------------
* ``stdin=DEVNULL`` on all subprocesses — prevents interactive prompts from
  hanging when the terminal is occupied by the Rich UI.
* ``scaffold_subdir`` pattern — npm/npx create commands that balk at a
  non-empty directory are told to scaffold into a fresh ``__cvc_init``
  subdirectory first; we then move all files up to the workspace root
  (skipping ``.git`` which CVC already created).  This avoids the
  "directory is not empty" interactive prompt entirely.
* ``extra_commands`` — commands to run *after* the subdir move (e.g.
  ``npm install`` after the scaffold files have been moved up).
* Streaming output via a dedicated reader thread so the UI can show live
  progress instead of a silent spinner.
"""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("cvc.agent.scaffolder")

# ── Subdirectory used when we need to scaffold into a fresh dir ──────────────
_SCAFFOLD_SUBDIR = "cvc-scaffold"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ScaffoldRecipe:
    """
    One recipe = prerequisite check + ordered shell commands.

    Execution order
    ---------------
    1. ``commands`` run in the workspace root.
    2. If ``scaffold_subdir`` is set, Python moves files from
       ``workspace/scaffold_subdir`` → ``workspace/`` (skipping ``.git``).
    3. ``extra_commands`` run in the workspace root (e.g. ``npm install``).
    4. ``post_files`` are written only if they don't already exist.
    """

    prerequisite: str            # Tool name to check (e.g. "uv", "node", "cargo")
    commands: list[str]          # Commands run before optional subdir move
    scaffold_subdir: str | None = None  # If set, move this subdir up after commands
    extra_commands: list[str] = field(default_factory=list)  # Commands after move
    post_files: dict[str, str] = field(default_factory=dict)  # Extra files (path → content)
    install_hint: str = ""       # Shown when prerequisite is missing


@dataclass
class ScaffoldResult:
    success: bool
    output: str  # Combined stdout/stderr from all commands
    files_created: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Recipes
# ---------------------------------------------------------------------------
# NOTE: All npm/npx "create" commands that target an existing directory use
# ``scaffold_subdir=_SCAFFOLD_SUBDIR`` so they scaffold into a fresh empty
# subdirectory first (avoiding the "Directory is not empty" interactive
# prompt).  Python then moves the files to the workspace root.

SCAFFOLD_RECIPES: dict[str, ScaffoldRecipe] = {
    # ── Web Applications ──────────────────────────────────────────────
    "React with TypeScript (Vite)": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npm create vite@latest {_SCAFFOLD_SUBDIR} -- --template react-ts"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        extra_commands=["npm install"],
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Next.js (React framework)": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npx create-next-app@latest {_SCAFFOLD_SUBDIR} --yes"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Vue 3 with Vite": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npm create vite@latest {_SCAFFOLD_SUBDIR} -- --template vue-ts"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        extra_commands=["npm install"],
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Angular with TypeScript": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npx @angular/cli@latest new {_SCAFFOLD_SUBDIR} --skip-git --defaults"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "SvelteKit": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npx sv create {_SCAFFOLD_SUBDIR} --template minimal --types ts --no-install"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        extra_commands=["npm install"],
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Flask web app": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add flask"],
        post_files={
            "app.py": (
                "from flask import Flask\n\n"
                "app = Flask(__name__)\n\n\n"
                '@app.route("/")\n'
                "def index():\n"
                '    return "Hello, World!"\n'
            ),
        },
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "Django web app": ScaffoldRecipe(
        prerequisite="uv",
        commands=[
            "uv init",
            "uv add django",
            "uv run django-admin startproject config .",
        ],
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "FastAPI with Jinja2 templates": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", 'uv add "fastapi[standard]" jinja2'],
        post_files={
            "app.py": (
                "from fastapi import FastAPI\n\n"
                "app = FastAPI()\n\n\n"
                '@app.get("/")\n'
                "def root():\n"
                '    return {"message": "Hello, World!"}\n'
            ),
        },
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),

    # ── API / Backend ─────────────────────────────────────────────────
    "FastAPI REST API": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", 'uv add "fastapi[standard]"'],
        post_files={
            "app.py": (
                "from fastapi import FastAPI\n\n"
                "app = FastAPI()\n\n\n"
                '@app.get("/")\n'
                "def root():\n"
                '    return {"message": "Hello, World!"}\n'
            ),
        },
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "Flask REST API": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add flask flask-cors"],
        post_files={
            "app.py": (
                "from flask import Flask\nfrom flask_cors import CORS\n\n"
                "app = Flask(__name__)\nCORS(app)\n\n\n"
                '@app.route("/")\n'
                "def index():\n"
                '    return {"message": "Hello, World!"}\n'
            ),
        },
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "Express.js API": ScaffoldRecipe(
        # npm init -y works fine in a non-empty dir; no scaffold_subdir needed
        prerequisite="node",
        commands=["npm init -y", "npm install express cors"],
        post_files={
            "index.js": (
                'const express = require("express");\n'
                'const cors = require("cors");\n\n'
                "const app = express();\n"
                "app.use(cors());\n"
                "app.use(express.json());\n\n"
                'app.get("/", (req, res) => {\n'
                '  res.json({ message: "Hello, World!" });\n'
                "});\n\n"
                "const PORT = process.env.PORT || 3000;\n"
                "app.listen(PORT, () => {\n"
                '  console.log(`Server running on port ${PORT}`);\n'
                "});\n"
            ),
        },
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Gin HTTP API": ScaffoldRecipe(
        prerequisite="go",
        commands=[
            "go mod init project",
            "go get github.com/gin-gonic/gin",
        ],
        post_files={
            "main.go": (
                'package main\n\nimport "github.com/gin-gonic/gin"\n\n'
                "func main() {\n"
                "\tr := gin.Default()\n"
                '\tr.GET("/", func(c *gin.Context) {\n'
                '\t\tc.JSON(200, gin.H{"message": "Hello, World!"})\n'
                "\t})\n"
                '\tr.Run(":8080")\n'
                "}\n"
            ),
        },
        install_hint="Install Go from https://go.dev/dl/",
    ),
    "Actix-web API": ScaffoldRecipe(
        prerequisite="cargo",
        commands=[
            "cargo init",
            "cargo add actix-web serde tokio --features tokio/full,serde/derive",
        ],
        install_hint="Install Rust from https://rustup.rs/",
    ),
    "ASP.NET Core Web API": ScaffoldRecipe(
        prerequisite="dotnet",
        commands=[f"dotnet new webapi -o {_SCAFFOLD_SUBDIR}"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install .NET SDK from https://dotnet.microsoft.com/download",
    ),

    # ── CLI Tools ─────────────────────────────────────────────────────
    "Click CLI app": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add click"],
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "Typer CLI app": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add typer"],
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "Commander.js CLI": ScaffoldRecipe(
        prerequisite="node",
        commands=["npm init -y", "npm install commander"],
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Go CLI with cobra": ScaffoldRecipe(
        prerequisite="go",
        commands=[
            "go mod init project",
            "go get github.com/spf13/cobra@latest",
        ],
        install_hint="Install Go from https://go.dev/dl/",
    ),
    "Rust CLI with clap": ScaffoldRecipe(
        prerequisite="cargo",
        commands=["cargo init", "cargo add clap --features derive"],
        install_hint="Install Rust from https://rustup.rs/",
    ),

    # ── Library / Package ─────────────────────────────────────────────
    "Python library with pyproject.toml": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init --lib"],
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "TypeScript npm package": ScaffoldRecipe(
        prerequisite="node",
        commands=[
            "npm init -y",
            "npm install -D typescript @types/node",
            "npx tsc --init",
        ],
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Rust library crate": ScaffoldRecipe(
        prerequisite="cargo",
        commands=["cargo init --lib"],
        install_hint="Install Rust from https://rustup.rs/",
    ),
    "Go library module": ScaffoldRecipe(
        prerequisite="go",
        commands=["go mod init project"],
        install_hint="Install Go from https://go.dev/dl/",
    ),

    # ── AI Agent / Chatbot ────────────────────────────────────────────
    "OpenAI chat agent": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add openai python-dotenv"],
        post_files={".env.example": "OPENAI_API_KEY=sk-...\n"},
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "LangChain agent": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add langchain langchain-openai python-dotenv"],
        post_files={".env.example": "OPENAI_API_KEY=sk-...\n"},
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "AutoGen multi-agent": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add autogen-agentchat"],
        post_files={".env.example": "OPENAI_API_KEY=sk-...\n"},
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    "Vercel AI SDK bot": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npx create-next-app@latest {_SCAFFOLD_SUBDIR} --yes"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        extra_commands=["npm install ai @ai-sdk/openai"],
        post_files={".env.example": "OPENAI_API_KEY=sk-...\n"},
        install_hint="Install Node.js from https://nodejs.org/",
    ),

    # ── Mobile Application ────────────────────────────────────────────
    "React Native (Expo)": ScaffoldRecipe(
        prerequisite="node",
        commands=[f"npx create-expo-app@latest {_SCAFFOLD_SUBDIR}"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Flutter app": ScaffoldRecipe(
        prerequisite="flutter",
        commands=[f"flutter create --project-name myapp {_SCAFFOLD_SUBDIR}"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install Flutter from https://docs.flutter.dev/get-started/install",
    ),

    # ── Desktop Application ───────────────────────────────────────────
    "Electron desktop app": ScaffoldRecipe(
        # npm init -y works fine in non-empty dir; no scaffold_subdir needed
        prerequisite="node",
        commands=["npm init -y", "npm install electron --save-dev"],
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "Tauri desktop app": ScaffoldRecipe(
        prerequisite="node",
        commands=[
            f"npm create tauri-app@latest {_SCAFFOLD_SUBDIR} -- "
            "--template vanilla-ts --manager npm"
        ],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install Node.js from https://nodejs.org/",
    ),
    "PyQt6 desktop app": ScaffoldRecipe(
        prerequisite="uv",
        commands=["uv init", "uv add pyqt6"],
        install_hint="Install uv: pip install uv  (or see https://docs.astral.sh/uv/)",
    ),
    ".NET MAUI cross-platform app": ScaffoldRecipe(
        prerequisite="dotnet",
        commands=[f"dotnet new maui -o {_SCAFFOLD_SUBDIR}"],
        scaffold_subdir=_SCAFFOLD_SUBDIR,
        install_hint="Install .NET SDK from https://dotnet.microsoft.com/download",
    ),
}


# ---------------------------------------------------------------------------
# Prerequisite checking
# ---------------------------------------------------------------------------

def check_prerequisite(tool: str) -> bool:
    """Return True if *tool* is found on PATH."""
    return shutil.which(tool) is not None


def _install_hint_for(tool: str) -> str:
    """Return a user-friendly install instruction for common tools."""
    hints = {
        "uv": "pip install uv  (or see https://docs.astral.sh/uv/)",
        "node": "https://nodejs.org/",
        "cargo": "https://rustup.rs/",
        "go": "https://go.dev/dl/",
        "flutter": "https://docs.flutter.dev/get-started/install",
        "dotnet": "https://dotnet.microsoft.com/download",
    }
    return hints.get(tool, f"Install '{tool}' and make sure it's on your PATH.")


# ---------------------------------------------------------------------------
# Shell runner — streaming via Popen + reader thread
# ---------------------------------------------------------------------------

def _run_shell(
    command: str,
    workspace: Path,
    timeout: int = 180,
    on_output: "callable | None" = None,
) -> tuple[int, str]:
    """
    Run a single shell command in *workspace* and return ``(exit_code, output)``.

    * ``stdin=DEVNULL`` — interactive prompts get EOF immediately instead of
      hanging the process waiting for input that can never arrive.
    * A dedicated reader thread drains stdout+stderr so the caller can receive
      live output via *on_output* while ``process.wait(timeout=…)`` runs on
      the main thread.
    """
    if sys.platform == "win32":
        utf8_prefix = (
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
            "$OutputEncoding = [System.Text.Encoding]::UTF8; "
        )
        shell_cmd = [
            "powershell", "-NoProfile", "-NonInteractive",
            "-Command", utf8_prefix + command,
        ]
    else:
        shell_cmd = ["bash", "-c", command]

    try:
        process = subprocess.Popen(
            shell_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,   # merge stderr → stdout
            stdin=subprocess.DEVNULL,   # no interactivity — prevents prompt hangs
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(workspace),
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                    **HIDDEN_KW,
        )
    except FileNotFoundError as exc:
        return 1, f"Shell not found: {exc}"
    except OSError as exc:
        return 1, f"Failed to start process: {exc}"

    all_lines: list[str] = []

    def _reader() -> None:
        assert process.stdout is not None
        for raw in iter(process.stdout.readline, ""):
            stripped = raw.rstrip()
            all_lines.append(stripped)
            if on_output and stripped:
                try:
                    on_output(stripped)
                except Exception:
                    pass

    reader = threading.Thread(target=_reader, daemon=True)
    reader.start()

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        all_lines.append(f"\n⏱  Command timed out after {timeout}s: {command}")
        reader.join(timeout=2)
        return 1, "\n".join(all_lines)

    reader.join(timeout=5)  # drain any last output
    return process.returncode, "\n".join(all_lines)


# ---------------------------------------------------------------------------
# File-move helper
# ---------------------------------------------------------------------------

def _move_subdir_to_workspace(subdir: Path, workspace: Path) -> None:
    """
    Move every item inside *subdir* into *workspace*, then remove *subdir*.

    Rules
    -----
    * ``.git`` in the scaffold output is skipped — CVC already initialised
      the workspace's own git repo.
    * If a destination path already exists it is overwritten.
    """
    for item in list(subdir.iterdir()):
        if item.name == ".git":
            # Don't clobber CVC's git repo
            shutil.rmtree(str(item), ignore_errors=True)
            continue
        dest = workspace / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(str(dest))
            else:
                dest.unlink()
        shutil.move(str(item), str(workspace))

    # Subdir should now be empty; remove it
    try:
        subdir.rmdir()
    except OSError:
        shutil.rmtree(str(subdir), ignore_errors=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_scaffold(
    workspace: Path,
    stack_id: str,
    *,
    on_command: "callable | None" = None,
    on_output: "callable | None" = None,
) -> ScaffoldResult:
    """
    Execute the scaffold recipe for *stack_id* in *workspace*.

    Parameters
    ----------
    workspace : Path
        Directory to scaffold into (must already exist).
    stack_id : str
        Key into ``SCAFFOLD_RECIPES`` — matches the second element of each
        ``stack_map`` tuple in ``chat.py``.
    on_command : callable, optional
        ``on_command(cmd, index, total)`` — called before each command runs.
    on_output : callable, optional
        ``on_output(line)`` — called for each output line (live streaming).

    Returns
    -------
    ScaffoldResult
    """
    recipe = SCAFFOLD_RECIPES.get(stack_id)
    if recipe is None:
        return ScaffoldResult(
            success=False,
            output=(
                f"No scaffold recipe found for '{stack_id}'. "
                "Falling back to AI-assisted scaffolding."
            ),
        )

    # ── Prerequisite check ────────────────────────────────────────────
    if not check_prerequisite(recipe.prerequisite):
        hint = recipe.install_hint or _install_hint_for(recipe.prerequisite)
        return ScaffoldResult(
            success=False,
            output=(
                f"Required tool '{recipe.prerequisite}' is not installed.\n"
                f"Install it: {hint}"
            ),
        )

    all_output: list[str] = []
    total = len(recipe.commands) + len(recipe.extra_commands)
    cmd_idx = 0

    # ── Phase 1: init commands ────────────────────────────────────────
    for cmd in recipe.commands:
        cmd_idx += 1
        if on_command:
            on_command(cmd, cmd_idx, total)
        logger.info("scaffold cmd %d/%d: %s", cmd_idx, total, cmd)
        exit_code, output = _run_shell(cmd, workspace, on_output=on_output)
        if output:
            all_output.append(output)
        if exit_code != 0:
            all_output.append(f"\n✗ Command failed (exit {exit_code}): {cmd}")
            return ScaffoldResult(success=False, output="\n".join(all_output))

    # ── Phase 2: move subdir → workspace root ────────────────────────
    if recipe.scaffold_subdir:
        subdir = workspace / recipe.scaffold_subdir
        if subdir.is_dir():
            logger.info("moving scaffold subdir '%s' to workspace root", recipe.scaffold_subdir)
            _move_subdir_to_workspace(subdir, workspace)
        else:
            all_output.append(
                f"Warning: expected scaffold directory '{recipe.scaffold_subdir}' not found; "
                "the init command may have failed silently."
            )

    # ── Phase 3: extra commands (e.g. npm install) ────────────────────
    for cmd in recipe.extra_commands:
        cmd_idx += 1
        if on_command:
            on_command(cmd, cmd_idx, total)
        logger.info("scaffold extra cmd %d/%d: %s", cmd_idx, total, cmd)
        exit_code, output = _run_shell(cmd, workspace, on_output=on_output)
        if output:
            all_output.append(output)
        if exit_code != 0:
            all_output.append(f"\n✗ Command failed (exit {exit_code}): {cmd}")
            return ScaffoldResult(success=False, output="\n".join(all_output))

    # ── Phase 4: post-scaffold files ──────────────────────────────────
    for rel_path, content in recipe.post_files.items():
        target = workspace / rel_path
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    # ── Collect created files ─────────────────────────────────────────
    created: list[str] = []
    try:
        for entry in sorted(workspace.rglob("*")):
            rel = entry.relative_to(workspace)
            parts = rel.parts
            if any(
                p in (
                    ".git", ".cvc", "node_modules", "__pycache__",
                    ".venv", "venv", "target", _SCAFFOLD_SUBDIR,
                )
                for p in parts
            ):
                continue
            if entry.is_file():
                created.append(str(rel))
    except OSError:
        pass

    return ScaffoldResult(
        success=True,
        output="\n".join(all_output),
        files_created=created,
    )
