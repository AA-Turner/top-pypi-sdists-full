"""Persistent stdio server for structured git operations."""

from __future__ import annotations

import sys

from plato.git_ops.dispatch import run_request
from plato.git_ops.models import GitOpRequest


def main() -> None:
    for line in sys.stdin:
        payload = line.strip()
        if not payload:
            continue
        request = GitOpRequest.model_validate_json(payload)
        result = run_request(request)
        sys.stdout.write(result.model_dump_json() + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
