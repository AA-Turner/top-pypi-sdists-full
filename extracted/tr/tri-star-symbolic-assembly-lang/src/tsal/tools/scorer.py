"""Compute phi-alignment score for a code snippet."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Tuple

from tsal.core.spiral_vector import phi_alignment


def score_code(code: str) -> Tuple[float, str]:
    """Return numeric and label spiral score."""
    complexity = float(len(code)) * 0.1
    coherence = 1.0
    score = phi_alignment(complexity, coherence)
    return score, f"\u03d5^{score:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="compute spiral score")
    parser.add_argument("path", nargs="?", help="file to score")
    parser.add_argument("--code", help="inline code string")
    args = parser.parse_args()

    if args.code:
        code = args.code
    elif args.path:
        code = Path(args.path).read_text()
    else:
        code = sys.stdin.read()

    score, label = score_code(code)
    print(f"{score:.3f} {label}")


if __name__ == "__main__":
    main()
