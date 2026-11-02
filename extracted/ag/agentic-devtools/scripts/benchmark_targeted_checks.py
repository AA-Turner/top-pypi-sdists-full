"""Run reproducible targeted-check benchmarks."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    from agentic_devtools.cli.checks.benchmark import main as benchmark_main

    return benchmark_main()


if __name__ == "__main__":
    raise SystemExit(main())
