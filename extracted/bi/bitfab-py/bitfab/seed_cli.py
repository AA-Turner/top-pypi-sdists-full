from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import Any, TextIO

from bitfab.replay_cli import _load_registry, _parse_command_args
from bitfab.replay_registry import run_seed_cli

USAGE = (
    "Usage: bitfab-seed --registry <path> <pipeline> --from-trace <id>[,<id>...]\n"
    "       bitfab-seed --registry <path> <pipeline> --cases <cases.jsonl>"
)
HELP = f"{USAGE}\nRun bitfab-seed --registry <path> <pipeline> --help for details."


def run_seed_command(
    argv: Sequence[str],
    *,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> dict[str, Any]:
    registry_path, seed_args = _parse_command_args(argv)
    return run_seed_cli(
        _load_registry(registry_path), seed_args, stdout=stdout, stderr=stderr
    )


def run_seed_main(
    argv: Sequence[str], *, stdout: TextIO = sys.stdout, stderr: TextIO = sys.stderr
) -> int:
    if any(value in ("--help", "-h") for value in argv) and "--registry" not in argv:
        print(HELP, file=stdout)
        return 0
    try:
        run_seed_command(argv, stdout=stdout, stderr=stderr)
    except SystemExit as error:
        return int(error.code or 0)
    except Exception as error:
        print(str(error), file=stderr)
        return 1
    return 0


def main() -> int:
    return run_seed_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
