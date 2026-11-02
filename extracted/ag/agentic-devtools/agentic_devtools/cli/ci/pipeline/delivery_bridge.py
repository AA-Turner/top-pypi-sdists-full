"""Expose initial-delivery evidence to a trusted workflow caller.

The trusted caller must first admit successful task completion and correlate the
PR and head. Only that admission permits ``completion_confirmed=True`` here.
No authoritative initial-plan SHA is available, so ``None`` leaves a zero diff
UNKNOWN and cannot authorize no-delivery recovery.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Sequence

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.delivery import (
    InitialDeliveryOutcome,
    classify_initial_delivery_with_head,
)


def _parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    """Parse and validate the trusted caller's repository, PR number and head."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--pr-number", required=True, type=int)
    parser.add_argument("--head-sha", required=True)
    args = parser.parse_args(argv)
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository) is None:
        parser.error("--repository must be in owner/repo form")
    if args.pr_number <= 0:
        parser.error("--pr-number must be a positive integer")
    if re.fullmatch(r"[A-Fa-f0-9]{40}", args.head_sha) is None:
        parser.error("--head-sha must contain exactly 40 hexadecimal characters")
    return args


def _run_bridge(repository: str, pr_number: int, head_sha: str) -> dict[str, object]:
    """Return only delivery proven for the requested head by the shared authority."""
    provider = GitHubActionsProvider(repo=repository, token=None)
    observed_head, outcome = classify_initial_delivery_with_head(
        provider,
        pr_number,
        completion_confirmed=True,
        initial_plan_sha=None,
    )
    requested_head = head_sha.lower()
    delivered = observed_head.lower() == requested_head and outcome is InitialDeliveryOutcome.DELIVERED
    return {
        "repository": repository,
        "prNumber": pr_number,
        "headSha": requested_head,
        "outcome": "DELIVERED" if delivered else "UNKNOWN",
        "complete": delivered,
        "diffEvidence": "NON_ZERO_DIFF" if delivered else "UNKNOWN",
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Print the compact JSON evidence envelope, letting failures propagate."""
    args = _parse_arguments(argv)
    result = _run_bridge(args.repository, args.pr_number, args.head_sha)
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
