"""Installed replay command that loads a project-owned registry module."""

from __future__ import annotations

import os
import runpy
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, TextIO

from bitfab.cloud_replay_cli import HINT as CLOUD_HINT
from bitfab.cloud_replay_cli import is_cloud_command, run_cloud_command
from bitfab.replay import ReplayResult
from bitfab.replay_registry import (
    SIGINT_EXIT_CODE,
    ReplayRegistry,
    record_child_command_context,
    run_replay_cli,
)

RegistryLoader = Callable[[str], ReplayRegistry]
ReplayRunner = Callable[..., ReplayResult]

USAGE = "Usage: bitfab-replay --registry <path> <pipeline> [replay options]"
HELP = f"{USAGE}\nRun bitfab-replay --registry <path> --help to list replay options.\n{CLOUD_HINT}"


def _parse_command_args(argv: Sequence[str]) -> tuple[str, list[str]]:
    try:
        registry_index = argv.index("--registry")
    except ValueError as error:
        raise ValueError(USAGE) from error

    try:
        registry_path = argv[registry_index + 1]
    except IndexError as error:
        raise ValueError(USAGE) from error
    if registry_path.startswith("--"):
        raise ValueError(USAGE)

    replay_args = [
        value
        for index, value in enumerate(argv)
        if index not in (registry_index, registry_index + 1)
    ]
    if not replay_args:
        raise ValueError(USAGE)
    return str(Path(registry_path).resolve()), replay_args


def _registry_import_hint(path: str) -> str:
    return "\n".join(
        [
            f"The replay registry '{path}' could not load one of its imports.",
            "A registry belongs in the project that builds the traced function's call and already depends on everything it imports (its tools, clients, and config), and bitfab-replay runs from that project's directory.",
            "bitfab-replay adds only the registry file's own folder to the import path, so when the registry imports the app by package name, install the app in the active environment or run with PYTHONPATH=. from the project root.",
            "When the traced function lives in a lower-level library that an app calls, put the registry in the app and add bitfab to its dependencies. Copying the app's dependencies into the library is the wrong fix.",
            'See "When the traced function needs the app\'s dependencies" at https://docs.bitfab.ai/python-sdk.',
        ]
    )


def _load_registry(path: str) -> ReplayRegistry:
    registry_directory = str(Path(path).parent)
    sys.path.insert(0, registry_directory)
    try:
        namespace = runpy.run_path(path)
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            f"{error}\n\n{_registry_import_hint(path)}", name=error.name
        ) from error
    finally:
        sys.path.remove(registry_directory)
    registry: Any = namespace.get("registry")
    if not isinstance(registry, ReplayRegistry):
        raise ValueError(
            f"Replay registry '{path}' must define a ReplayRegistry named 'registry'."
        )
    return registry


def run_replay_command(
    argv: Sequence[str],
    *,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    loader: RegistryLoader = _load_registry,
    runner: ReplayRunner = run_replay_cli,
) -> ReplayResult:
    """Load the passed registry module and run the SDK-owned replay command."""
    registry_path, replay_args = _parse_command_args(argv)
    record_child_command_context(registry_path, replay_args, os.environ)
    return runner(loader(registry_path), replay_args, stdout=stdout, stderr=stderr)


def run_replay_main(
    argv: Sequence[str], *, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr
) -> int:
    """Run the console entry point and return its process exit code."""
    if is_cloud_command(argv):
        return run_cloud_command(argv)
    if any(value in ("--help", "-h") for value in argv) and "--registry" not in argv:
        print(HELP, file=stdout)
        return 0
    try:
        run_replay_command(argv, stdout=stdout, stderr=stderr)
    except SystemExit as error:
        return int(error.code or 0)
    except KeyboardInterrupt:
        return SIGINT_EXIT_CODE
    except Exception as error:
        print(str(error), file=stderr)
        return 1
    return 0


def main() -> int:
    """Console-script entry point."""
    return run_replay_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
