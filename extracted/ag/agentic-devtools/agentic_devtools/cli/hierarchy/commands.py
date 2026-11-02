"""CLI entry points for hierarchy commands.

Provides ``agdt-detect-hierarchy``, ``agdt-enforce-parent``, and
``agdt-cascade-trigger`` commands.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agentic_devtools.cli.hierarchy.helpers import resolve_owner_repo
from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.hierarchy.cascade import CascadeApiRetryExhaustedError, CascadeProcessor
from agentic_devtools.hierarchy.enforcement import enforce_parent_specked, reject_trigger
from agentic_devtools.hierarchy.github_detector import GitHubHierarchyDetector
from agentic_devtools.hierarchy.metadata_io import write_hierarchy_yml
from agentic_devtools.hierarchy.models import HierarchyLevel
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path


def _collect_ancestors(
    detector: GitHubHierarchyDetector,
    issue_number: int,
) -> list[int]:
    """Collect ancestors ordered from root to immediate parent."""
    ancestors: list[int] = []
    seen: set[int] = set()
    parent = detector.detect_parent(issue_number)

    while parent is not None and parent not in seen:
        seen.add(parent)
        ancestors.append(parent)
        parent = detector.detect_parent(parent)

    ancestors.reverse()
    return ancestors


def detect_hierarchy_command() -> None:
    """CLI entry point for ``agdt-detect-hierarchy``.

    Detects hierarchy for a GitHub issue, classifies it, and writes
    hierarchy.yml to the appropriate spec directory.
    """
    parser = argparse.ArgumentParser(
        description="Detect hierarchy for a GitHub issue and write hierarchy.yml.",
    )
    parser.add_argument("--issue", type=int, required=True, help="GitHub issue number")
    parser.add_argument("--owner", type=str, default=None, help="GitHub repo owner")
    parser.add_argument("--repo", type=str, default=None, help="GitHub repo name")
    parser.add_argument(
        "--specs-root",
        type=str,
        default="specs",
        help="Root directory for specs (default: specs)",
    )
    args = parser.parse_args()

    try:
        owner, repo = resolve_owner_repo(owner=args.owner, repo=args.repo)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    specs_root = Path(args.specs_root)

    detector = GitHubHierarchyDetector(owner=owner, repo=repo)
    metadata = detector.build_metadata(args.issue)
    ancestors = _collect_ancestors(detector, args.issue)

    # Resolve spec path
    spec_path = resolve_spec_path(
        args.issue,
        metadata,
        specs_root,
        ancestors=ancestors,
    )

    # Write hierarchy.yml (skipped for STANDALONE; also skip creating the directory)
    written = False
    enforcement_rejected = False
    if metadata.level != HierarchyLevel.STANDALONE:
        # Compute ancestors for the parent lookup (strip the immediate parent from the
        # tail of the chain so check_parent_specked receives grandparent-and-above
        # ancestors, not the parent itself — ancestors are root→parent ordered, so the
        # direct parent is always the last element when present).
        parent_ancestors = ancestors
        if metadata.parent is not None and ancestors and ancestors[-1] == metadata.parent:
            parent_ancestors = ancestors[:-1]

        enforcement = enforce_parent_specked(
            args.issue,
            metadata,
            specs_root,
            ancestors=parent_ancestors,
        )
        if not enforcement.allowed:
            enforcement_rejected = True
        else:
            spec_path.mkdir(parents=True, exist_ok=True)
            yml_path = spec_path / "hierarchy.yml"
            written = write_hierarchy_yml(yml_path, metadata)

    # Output result
    result = {
        "issue": args.issue,
        "level": metadata.level.value,
        "parent": metadata.parent,
        "children": [c.number for c in metadata.children],
        "spec_path": str(spec_path),
        "hierarchy_yml_written": written,
        "enforcement_rejected": enforcement_rejected,
    }
    print(json.dumps(result, indent=2))


def enforce_parent_command() -> None:
    """CLI entry point for ``agdt-enforce-parent``.

    Checks whether a child issue's parent has been specked.
    Exits with code 0 if allowed, code 1 if rejected.
    """
    parser = argparse.ArgumentParser(
        description="Enforce parent-first processing for a child issue.",
    )
    parser.add_argument("--issue", type=int, required=True, help="Child issue number")
    parser.add_argument("--owner", type=str, default=None, help="GitHub repo owner")
    parser.add_argument("--repo", type=str, default=None, help="GitHub repo name")
    parser.add_argument(
        "--specs-root",
        type=str,
        default="specs",
        help="Root directory for specs (default: specs)",
    )
    args = parser.parse_args()

    try:
        owner, repo = resolve_owner_repo(owner=args.owner, repo=args.repo)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    specs_root = Path(args.specs_root)

    detector = GitHubHierarchyDetector(owner=owner, repo=repo)
    metadata = detector.build_metadata(args.issue)
    ancestors = _collect_ancestors(detector, args.issue)
    parent_ancestors = ancestors
    if metadata.parent is not None and ancestors and ancestors[-1] == metadata.parent:
        parent_ancestors = ancestors[:-1]

    enforcement = enforce_parent_specked(
        args.issue,
        metadata,
        specs_root,
        ancestors=parent_ancestors,
    )

    result = {
        "issue": args.issue,
        "action": enforcement.action.value,
        "reason": enforcement.reason,
        "parent_issue": enforcement.parent_issue,
        "parent_path": str(enforcement.parent_path) if enforcement.parent_path else None,
    }
    print(json.dumps(result, indent=2))

    if not enforcement.allowed:
        # Post rejection comment
        comment = reject_trigger(args.issue, enforcement.parent_issue or 0, owner=owner, repo=repo)
        print(f"\nRejection comment:\n{comment}", file=sys.stderr)
        try:
            comment_result = run_safe(
                [
                    "gh",
                    "issue",
                    "comment",
                    str(args.issue),
                    "--repo",
                    f"{owner}/{repo}",
                    "--body",
                    comment,
                ],
                capture_output=True,
                text=True,
                shell=False,
            )
            if comment_result.returncode != 0:
                print(
                    f"Warning: failed to post rejection comment: {comment_result.stderr}",
                    file=sys.stderr,
                )
        except FileNotFoundError as exc:
            print(
                f"Warning: failed to post rejection comment: {exc}",
                file=sys.stderr,
            )

        try:
            label_result = run_safe(
                [
                    "gh",
                    "issue",
                    "edit",
                    str(args.issue),
                    "--repo",
                    f"{owner}/{repo}",
                    "--remove-label",
                    "speckit",
                ],
                capture_output=True,
                text=True,
                shell=False,
            )
            if label_result.returncode != 0:
                print(
                    f"Warning: failed to remove 'speckit' label: {label_result.stderr}",
                    file=sys.stderr,
                )
        except FileNotFoundError as exc:
            print(
                f"Warning: failed to remove 'speckit' label: {exc}",
                file=sys.stderr,
            )
        sys.exit(1)


def cascade_trigger_command() -> None:
    """CLI entry point for ``agdt-cascade-trigger``.

    Triggers cascade after a final-phase merge. Supports both parent→child
    and sibling→sibling cascade.
    """
    parser = argparse.ArgumentParser(
        description="Trigger SpecKit cascade after final-phase merge.",
    )
    parser.add_argument("--issue", type=int, required=True, help="Completed issue number")
    parser.add_argument("--owner", type=str, default=None, help="GitHub repo owner")
    parser.add_argument("--repo", type=str, default=None, help="GitHub repo name")
    parser.add_argument(
        "--hierarchy-yml",
        type=str,
        required=True,
        help="Path to the hierarchy.yml file",
    )
    parser.add_argument(
        "--mode",
        choices=["first-child", "next-sibling"],
        required=True,
        help="Cascade mode: first-child (parent→child) or next-sibling (sibling→sibling)",
    )
    parser.add_argument(
        "--pipeline-failed",
        action="store_true",
        default=False,
        help="Indicate that the pipeline failed (halts cascade)",
    )
    args = parser.parse_args()

    if args.pipeline_failed and args.mode == "first-child":
        print(
            "Error: --pipeline-failed is only valid with --mode next-sibling",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        owner, repo = resolve_owner_repo(owner=args.owner, repo=args.repo)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    hierarchy_yml_path = Path(args.hierarchy_yml)
    processor = CascadeProcessor(owner=owner, repo=repo)

    try:
        if args.mode == "first-child":
            result = processor.trigger_first_child(args.issue, hierarchy_yml_path)
        else:
            result = processor.trigger_next_sibling(
                args.issue,
                hierarchy_yml_path,
                pipeline_failed=args.pipeline_failed,
            )
    except CascadeApiRetryExhaustedError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    output = {
        "issue": args.issue,
        "action": result.action.value,
        "comment": result.comment,
        "skipped_issues": result.skipped_issues,
    }
    if result.event:
        output["event"] = {
            "source_issue": result.event.source_issue,
            "target_issue": result.event.target_issue,
            "direction": result.event.direction.value,
        }

    print(json.dumps(output, indent=2))
