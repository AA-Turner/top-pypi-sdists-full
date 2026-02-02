from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_CANDIDATES = ('.yamloom.py', 'yamloom.py')
ENV_VAR = 'YAMLOOM_FILE'


def resolve_target(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)

    env_value = os.getenv(ENV_VAR)
    if env_value:
        return Path(env_value)

    for candidate in DEFAULT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path

    candidates = ', '.join(DEFAULT_CANDIDATES)
    raise FileNotFoundError(
        f'Could not find workflow generator. Tried: {candidates}. '
        f'Set --file or {ENV_VAR} to override.'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description='Run yamloom workflow generator.')
    parser.add_argument(
        '--file',
        dest='file',
        help='Path to workflow generator script (overrides defaults).',
    )
    args = parser.parse_args()

    try:
        target = resolve_target(args.file)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not target.exists():
        print(f'Workflow generator not found: {target}', file=sys.stderr)
        return 2

    result = subprocess.run([sys.executable, str(target)])
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
