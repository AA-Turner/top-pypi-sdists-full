"""Linting for emake."""

import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from .config import ProjectConfig
from .venv import (
    SPINNER_FRAMES,
    VirtualEnvironment,
)

MODULE_PATH = os.path.dirname(os.path.dirname(__file__))


def run_lint_async(
    venv: VirtualEnvironment,
    tool: str,
    *args: str,
) -> tuple[int, str, str]:
    """Run a linting tool in background.

    Args:
        venv: VirtualEnvironment instance.
        tool: Tool name to run.
        *args: Arguments to pass to the tool.

    Returns:
        Tuple of (tool name, success, returncode, output).
    """
    if tool == "emake":
        env = os.environ.copy()
        path = env.get("PYTHONPATH", "").split(os.pathsep)
        env["PYTHONPATH"] = os.pathsep.join([MODULE_PATH] + path)
        proc = subprocess.run(
            [
                *([] if "__compiled__" in globals() else [sys.executable, "-um"]),
                tool,
                *args,
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    else:
        proc = venv.run("-um", tool, *args, capture_output=True)

    return proc.returncode, proc.stdout, proc.stderr


def run_lint(
    venv: VirtualEnvironment,
    config: ProjectConfig,
    fix: bool,
    workflow: bool,
    colour: bool,
) -> int:
    """Run linting tools concurrently.

    Args:
        venv: VirtualEnvironment instance.
        fix: If True, automatically fix issues where supported.

    Returns:
        Exit code - number of tools that failed.
    """
    venv.ensure_lint_tools(list((config.extras or {}).keys()))
    extras = config.extras if config.extras is not None else {}
    venv.install(*[x for x in extras if x in ("test", "dev", "lint")])
    tools = [
        ("ruff", "check", *(["--fix"] if fix else [])),
        ("basedpyright", "--project=pyproject.toml"),
        ("dodgy", "--zero-exit"),
        ("pyroma", "."),
        (
            "emake",
            "config-diff",
            *(["--workflow"] if workflow else []),
            *(["--colour"] if colour else []),
        ),
    ]

    failed = 0
    spinner_idx = 0
    with ThreadPoolExecutor(max_workers=len(tools)) as executor:
        futures = {
            tool: executor.submit(
                run_lint_async,
                venv,
                tool,
                *args,
            )
            for tool, *args in tools
        }
        if not sys.stdout.isatty():
            print("Running linters...")

        while not all(x.done() for x in futures.values()):
            if not sys.stdout.isatty():
                time.sleep(0.1)
                continue

            spinner_idx = (spinner_idx + 1) % len(SPINNER_FRAMES)
            for tool, future in futures.items():
                print("\r", end="")
                if future.done():
                    returncode, _, _ = future.result()
                    print(
                        f"{tool}: {'PASS' if not returncode else f'FAIL ({returncode})'}"
                    )
                    continue

                print(f"{tool}: [{SPINNER_FRAMES[spinner_idx]}]")

            print("", end="", flush=True)
            time.sleep(0.1)
            print("\x1b[2K\x1b[1A" * len(tools), end="")

    for tool, future in futures.items():
        returncode, stdout, stderr = future.result()
        print(f"{tool}: {'PASS' if not returncode else f'FAIL ({returncode})'}")

        if returncode:
            print(stdout)
            print(stderr, file=sys.stderr)
            failed += 1

    if failed:
        print(f"{failed} failed")

    return failed
